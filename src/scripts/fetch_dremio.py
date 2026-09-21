"""Discover JGI Dremio lakehouse sources and emit a Catalog YAML.

Uses the Dremio REST Catalog API to list sources and the REST SQL API
to query INFORMATION_SCHEMA for per-source table counts. Outputs a
LinkML-conformant BER Data Registry Catalog document.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any

import requests
import yaml
from dotenv import load_dotenv

DREMIO_BASE_URL = "https://lakehouse-poc.jgi.lbl.gov"
API_V3 = f"{DREMIO_BASE_URL}/api/v3"

SQL_POLL_INTERVAL = 5  # seconds
SQL_MAX_WAIT = 600  # seconds
RESULTS_PAGE_SIZE = 500  # max allowed by Dremio

SOURCE_TYPE_MAP = {
    # object storage
    "S3": "object_storage",
    "NAS": "object_storage",
    "HDFS": "object_storage",
    "GCS": "object_storage",
    "AZURE_STORAGE": "object_storage",
    # relational databases
    "POSTGRES": "relational_database",
    "MYSQL": "relational_database",
    "MSSQL": "relational_database",
    "ORACLE": "relational_database",
    "REDSHIFT": "relational_database",
    "SNOWFLAKE": "relational_database",
    "BIGQUERY": "relational_database",
    "SYNAPSE": "relational_database",
    "DB2": "relational_database",
    "TERADATA": "relational_database",
    # document databases
    "MONGO": "document_database",
    "ELASTIC": "document_database",
    # namespace / catalog
    "NESSIE": "namespace",
    "HIVE": "namespace",
    "UNITY": "namespace",
    "RESTCATALOG": "namespace",
    "GLUE": "namespace",
    "DREMIO_CATALOG_V1": "namespace",
}

DB_ENGINE_MAP = {
    "POSTGRES": "postgresql",
    "MYSQL": "mysql",
    "MONGO": "mongodb",
}

RELATIONAL_TYPES = {
    t for t, st in SOURCE_TYPE_MAP.items() if st == "relational_database"
}


def load_pat() -> str:
    """Load Dremio PAT from JBERDL_KEY env var, with .env fallback."""
    # .env is at project root; look upward from this file
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")
    pat = os.environ.get("JBERDL_KEY")
    if not pat:
        sys.exit("error: JBERDL_KEY not set in environment or .env")
    return pat.strip()


def _headers(pat: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {pat}",
        "Content-Type": "application/json",
    }


def dremio_get(pat: str, path: str, params: dict | None = None) -> dict:
    resp = requests.get(f"{API_V3}/{path}", headers=_headers(pat), params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def dremio_post(pat: str, path: str, body: dict) -> dict:
    resp = requests.post(f"{API_V3}/{path}", headers=_headers(pat), json=body, timeout=60)
    resp.raise_for_status()
    return resp.json()


# ---------- Catalog API ----------

def get_sources(pat: str) -> list[dict]:
    """Fetch all top-level sources with full detail."""
    print("Fetching catalog root...", file=sys.stderr)
    root = dremio_get(pat, "catalog")
    source_items = [
        item for item in root.get("data", [])
        if item.get("containerType") == "SOURCE"
    ]
    print(f"Found {len(source_items)} sources. Fetching details...", file=sys.stderr)

    sources = []
    for i, item in enumerate(source_items, 1):
        name = item.get("path", ["?"])[0]
        print(f"  [{i}/{len(source_items)}] {name}", file=sys.stderr)
        detail = dremio_get(pat, f"catalog/{item['id']}")
        sources.append(detail)
    return sources


# ---------- SQL API ----------

def submit_sql(pat: str, sql: str) -> str:
    resp = dremio_post(pat, "sql", {"sql": sql})
    return resp["id"]


def poll_job(pat: str, job_id: str) -> dict:
    """Poll until job completes (or fails). Returns final job dict."""
    elapsed = 0
    while elapsed < SQL_MAX_WAIT:
        job = dremio_get(pat, f"job/{job_id}")
        state = job.get("jobState")
        if state in ("COMPLETED", "FAILED", "CANCELED"):
            return job
        print(f"  job {state} ({elapsed}s elapsed)...", file=sys.stderr)
        time.sleep(SQL_POLL_INTERVAL)
        elapsed += SQL_POLL_INTERVAL
    raise TimeoutError(f"SQL job {job_id} did not complete within {SQL_MAX_WAIT}s")


def fetch_results(pat: str, job_id: str, total_rows: int) -> list[dict]:
    """Paginate through all job results."""
    rows = []
    offset = 0
    while offset < total_rows:
        page = dremio_get(
            pat,
            f"job/{job_id}/results",
            params={"offset": offset, "limit": RESULTS_PAGE_SIZE},
        )
        batch = page.get("rows", [])
        if not batch:
            break
        rows.extend(batch)
        offset += len(batch)
    return rows


def get_table_counts(pat: str) -> dict[str, int]:
    """Query INFORMATION_SCHEMA.TABLES, aggregate by source name."""
    sql = (
        'SELECT TABLE_SCHEMA, COUNT(*) AS table_count '
        'FROM INFORMATION_SCHEMA."TABLES" '
        "WHERE TABLE_TYPE IN ('TABLE', 'VIEW') "
        "GROUP BY TABLE_SCHEMA"
    )
    print("Submitting INFORMATION_SCHEMA query (this can take ~2 min)...", file=sys.stderr)
    job_id = submit_sql(pat, sql)
    print(f"  job id: {job_id}", file=sys.stderr)
    job = poll_job(pat, job_id)
    if job.get("jobState") != "COMPLETED":
        print(
            f"warning: SQL job ended with state {job.get('jobState')}: "
            f"{job.get('errorMessage', '')}",
            file=sys.stderr,
        )
        return {}
    total_rows = int(job.get("rowCount", 0))
    print(f"  job completed: {total_rows} schema rows", file=sys.stderr)
    rows = fetch_results(pat, job_id, total_rows)

    counts: dict[str, int] = {}
    for row in rows:
        schema = row.get("TABLE_SCHEMA", "")
        count = int(row.get("table_count", 0))
        # TABLE_SCHEMA is like "source-name.sub.schema" — take first segment
        source = schema.split(".", 1)[0]
        counts[source] = counts.get(source, 0) + count
    return counts


# ---------- Mapping ----------

_slug_re = re.compile(r"[^a-z0-9]+")


def slugify(name: str) -> str:
    return _slug_re.sub("-", name.lower()).strip("-")


def _parse_date(iso_ts: str | None) -> str:
    """Parse Dremio ISO timestamp to YYYY-MM-DD string."""
    if not iso_ts:
        return date.today().isoformat()
    # Dremio returns e.g. "2026-03-16T19:03:55.801Z"
    return iso_ts[:10]


def _map_status(state_status: str | None) -> tuple[str, bool]:
    """Map Dremio state.status to (status enum, is_deprecated)."""
    s = (state_status or "good").lower()
    if s == "bad":
        return "archived", True
    return "active", False


def build_datasource(source: dict, table_count: int | None) -> dict:
    """Build a DataSource dict from Dremio source detail."""
    name = source.get("name", "unknown")
    dremio_type = source.get("type", "UNKNOWN")
    state_status = (source.get("state") or {}).get("status")
    status, is_deprecated = _map_status(state_status)

    ds: dict[str, Any] = {
        "id": f"ber_registry:ds-{slugify(name)}",
        "title": name,
        "description": (
            f"Data source '{name}' ({dremio_type}) in the JGI Dremio lakehouse."
        ),
        "created_date": _parse_date(source.get("createdAt")),
        "owner": "Unknown",
        "contact_point": {
            "contact_name": "Unknown",
            "contact_email": "unknown@lbl.gov",
        },
        "namespace": name,
        "status": status,
        "is_deprecated": is_deprecated,
        "update_schedule": "unknown",
        "access_level": "internal",
    }

    source_type = SOURCE_TYPE_MAP.get(dremio_type)
    if source_type:
        ds["source_type"] = source_type

    if dremio_type in DB_ENGINE_MAP:
        ds["database_engine"] = DB_ENGINE_MAP[dremio_type]
    elif dremio_type in RELATIONAL_TYPES:
        ds["database_engine"] = "other"

    if table_count is not None and table_count > 0:
        ds["table_count"] = table_count

    return ds


def build_catalog(datasources: list[dict], earliest_date: str) -> dict:
    return {
        "id": "ber_registry:catalog-jgi-dremio",
        "title": "JGI Dremio Lakehouse Registry",
        "description": (
            "Auto-discovered data sources from the JGI Dremio lakehouse "
            f"at {DREMIO_BASE_URL}."
        ),
        "lakehouses": [
            {
                "id": "ber_registry:lakehouse-jgi-dremio",
                "title": "JGI Dremio Lakehouse",
                "description": (
                    "Dremio-based data lakehouse at JGI providing unified query "
                    "access across MySQL, PostgreSQL, S3, and Iceberg catalogs."
                ),
                "endpoint_url": DREMIO_BASE_URL,
                "operator": "Lawrence Berkeley National Laboratory",
                "platform_type": "dremio",
                "created_date": earliest_date,
                "catalog_entries": datasources,
            }
        ],
    }


# ---------- Main ----------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", "-o", type=Path, default=None,
        help="Output YAML file path (default: stdout)",
    )
    parser.add_argument(
        "--skip-table-counts", action="store_true",
        help="Skip the slow INFORMATION_SCHEMA query",
    )
    args = parser.parse_args()

    pat = load_pat()

    sources = get_sources(pat)

    if args.skip_table_counts:
        table_counts: dict[str, int] = {}
    else:
        table_counts = get_table_counts(pat)

    datasources = [
        build_datasource(src, table_counts.get(src.get("name", "")))
        for src in sources
    ]

    # Earliest source createdAt → lakehouse created_date
    dates = [_parse_date(s.get("createdAt")) for s in sources if s.get("createdAt")]
    earliest = min(dates) if dates else date.today().isoformat()

    catalog = build_catalog(datasources, earliest)

    output = yaml.safe_dump(catalog, sort_keys=False, default_flow_style=False)
    if args.output:
        args.output.write_text(output)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
