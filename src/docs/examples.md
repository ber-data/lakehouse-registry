# Examples

Example YAML files demonstrating valid BER Data Registry entries. These files are the
same ones used by the project's automated tests, so they are always up to date with the
current schema.

## Quick Start

1. Download an example file below
2. Open it in your editor and adapt it for your data source
3. Validate with `linkml-validate -s src/ber_data_registry/schema/ber_data_registry.yaml your_file.yaml`

## Download Example Data Files

| File | Description |
|------|-------------|
| [Catalog-001.yaml](examples/Catalog-001.yaml) | Minimal example with one KBASE lakehouse and one public data source |
| [Catalog-002.yaml](examples/Catalog-002.yaml) | Deprecation chain showing version tracking between two linked data sources |
| [Catalog-003.yaml](examples/Catalog-003.yaml) | Dremio lakehouse with object storage, relational, and document database sources |

## Minimal Example

The simplest valid registry entry requires one lakehouse and one data source with all
required fields populated.

```yaml
id: ber_registry:catalog-001
title: BER Data Registry - Minimal Example
description: A minimal valid catalog with one lakehouse and one data source.
lakehouses:
  - id: ber_registry:lakehouse-kbase
    title: KBASE Lakehouse
    description: Spark-based lakehouse at NERSC for KBase and related projects.
    endpoint_url: https://kbase-lakehouse.nersc.gov
    operator: Lawrence Berkeley National Laboratory
    platform_type: spark
    created_date: "2023-01-15"
    catalog_entries:
      - id: ber_registry:ds-kbase-public
        title: KBase Public Data
        description: >-
          Public reference data shared across all KBase users, including genome
          annotations, metabolic models, and community datasets.
        owner: KBase Team
        contact_point:
          contact_name: KBase Data Support
          contact_email: kbase-help@lbl.gov
        namespace: kbase_public
        status: active
        is_deprecated: false
        update_schedule: weekly
        access_level: public
        created_date: "2023-06-01"
        keywords:
          - genomics
          - metabolic models
          - reference data
        project_affiliation:
          - KBase
```

## Deprecation and Version Tracking

Data sources can be linked through deprecation chains using `replaced_by` and
`previous_version` fields. This example shows a v1 source that has been deprecated
in favor of a v2 replacement.

```yaml
lakehouses:
  - id: ber_registry:lakehouse-kbase
    title: KBASE Lakehouse
    # ...
    catalog_entries:
      - id: ber_registry:ds-nmdc-v1
        title: NMDC Metadata Store v1
        status: deprecated
        is_deprecated: true
        deprecation_date: "2024-11-15"
        deprecation_reason: >-
          Replaced by v2 with improved schema validation and additional fields
          for instrument and facility tracking.
        replaced_by: ber_registry:ds-nmdc-v2
        # ... other required fields
      - id: ber_registry:ds-nmdc-v2
        title: NMDC Metadata Store v2
        status: active
        is_deprecated: false
        previous_version: ber_registry:ds-nmdc-v1
        # ... other required fields
```

## Dremio Lakehouse with Multiple Source Types

The Dremio lakehouse example demonstrates cataloging diverse data backends behind a
single lakehouse, including object storage, relational databases, and document databases.

```yaml
lakehouses:
  - id: ber_registry:lakehouse-dremio
    title: Dremio Lakehouse
    platform_type: dremio
    # ...
    catalog_entries:
      # Object storage source
      - id: ber_registry:ds-jgi-object-store
        title: JGI Genome Archive
        source_type: object_storage
        format:
          - Parquet
          - HDF5
        size_bytes: 5497558138880
        # ...

      # Relational database source
      - id: ber_registry:ds-emsl-sample-db
        title: EMSL Sample Tracking Database
        source_type: relational_database
        database_engine: postgresql
        row_count: 850000
        table_count: 24
        # ...

      # Document database source
      - id: ber_registry:ds-biosample-mongo
        title: BioSample Document Store
        source_type: document_database
        database_engine: mongodb
        status: experimental
        # ...
```
