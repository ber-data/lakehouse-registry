"""Generate the registry view page (docs/registry.md) from lakehouse-registry.yaml.

Invoked by the `_copy-registry` recipe in the justfile as part of `gen-doc`,
so the rendered page and the raw registry YAML are both published on the
GitHub Pages site.
"""

import argparse
from pathlib import Path

import yaml


def truncate(text: str | None, limit: int = 160) -> str:
    if not text:
        return ""
    text = " ".join(text.split())
    if len(text) > limit:
        return text[: limit - 1].rstrip() + "…"
    return text


def entry_row(entry: dict) -> str:
    title = entry.get("title") or entry.get("id", "")
    url = entry.get("documentation_url")
    title_cell = f"[{title}]({url})" if url else title
    contact = (entry.get("contact_point") or {}).get("contact_name") or ""
    owner = entry.get("owner") or ""
    who = owner if owner == contact or not contact else f"{owner} ({contact})"
    return (
        f"| {title_cell} | {truncate(entry.get('description'))} "
        f"| {who} | {entry.get('status', '')} | {entry.get('access_level', '')} |"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry-file", default="lakehouse-registry.yaml")
    parser.add_argument("--output", default="docs/registry.md")
    args = parser.parse_args()

    registry = yaml.safe_load(Path(args.registry_file).read_text())

    lines = [
        f"# {registry.get('title', 'BER Lakehouse Registry')}",
        "",
        registry.get("description", "").strip(),
        "",
        "Download the registry as YAML: "
        "[lakehouse-registry.yaml](lakehouse-registry.yaml)",
        "",
        "To add or update an entry, edit "
        "[`lakehouse-registry.yaml`]"
        "(https://github.com/ber-data/lakehouse-registry/blob/main/lakehouse-registry.yaml) "
        "in the repository root and open a pull request. Entries are validated "
        "against the [registry schema](elements/index.md) in CI.",
        "",
    ]

    for lakehouse in registry.get("lakehouses", []):
        entries = lakehouse.get("catalog_entries", [])
        lines += [
            f"## {lakehouse.get('title', lakehouse.get('id', ''))}",
            "",
            truncate(lakehouse.get("description"), 500),
            "",
            f"*Operator: {lakehouse.get('operator', 'Unknown')} · "
            f"Platform: {lakehouse.get('platform_type', 'unknown')} · "
            f"Entries: {len(entries)}*",
            "",
            "| Entry | Description | Owner (Contact) | Status | Access |",
            "|-------|-------------|-----------------|--------|--------|",
        ]
        lines += [entry_row(e) for e in entries]
        lines.append("")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text("\n".join(lines) + "\n")
    print(f"Wrote {args.output} ({sum(len(lh.get('catalog_entries', [])) for lh in registry.get('lakehouses', []))} entries)")


if __name__ == "__main__":
    main()
