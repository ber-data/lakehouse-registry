# About

## The BER Data Registry

The BER Data Registry is a metadata catalog for scientific data sources across
lakehouses operated by Lawrence Berkeley National Laboratory (LBNL) in support of
the Department of Energy's Biological and Environmental Research (BER) program.
It provides a standardized way to describe, discover, and track data sources
spanning multiple platforms, including the KBASE Spark lakehouse at NERSC and
Dremio-based data lakehouse environments.

## Project Goals

- **Standardize data cataloging** across BER-funded lakehouses and data platforms
  using a common metadata schema
- **Enable data discovery** by providing consistent descriptions of data sources,
  their owners, access levels, and update schedules
- **Track data lifecycle** including versioning, deprecation chains, and provenance
- **Align with community standards** by building on
  [DCAT v3](https://www.w3.org/TR/vocab-dcat-3/),
  [DCAT-US](https://resources.data.gov/resources/dcat-us/), and
  [schema.org](https://schema.org/) vocabularies

## The Data Model

### Design Principles

- **Standards-aligned** -- Classes map to DCAT, Dublin Core, vCard, and PROV
  vocabularies via explicit `class_uri` and `slot_uri` annotations
- **FAIR-compliant** -- Supports findable, accessible, interoperable, and reusable
  metadata for scientific datasets
- **Extensible** -- Built with [LinkML](https://linkml.io/) so the schema can
  evolve with new fields and enums as requirements grow
- **Multi-platform** -- Covers both Spark and Dremio lakehouses with source-type
  and engine-level detail

### Technology Stack

- [LinkML](https://linkml.io/) -- Schema definition language for linked data modeling
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) -- Documentation site
- [just](https://github.com/casey/just) -- Command runner for build automation
- [uv](https://docs.astral.sh/uv/) -- Python package management
- [GitHub Actions](https://docs.github.com/en/actions) -- CI/CD for testing and
  deployment

### Core Schema Elements

| Element | DCAT Mapping | Purpose |
|---------|-------------|---------|
| `DataRegistry` | `dcat:Catalog` | Top-level container for lakehouses and data sources |
| `Lakehouse` | `dcat:DataService` | A hosting platform (Spark, Dremio) |
| `DataSource` | `dcat:Dataset` | A cataloged data source within a lakehouse |
| `ContactPoint` | `vcard:Kind` | Contact information for a data source |

## Background

This project was informed by the **HPDF Data Catalog & Lakehouse Demo** report
(Cohoon & Paine, LBNL-2001745, December 2025), which recommended a unified metadata
catalog for BER data assets across LBNL facilities. The registry schema captures the
core metadata fields identified in that report while maintaining compatibility with
federal data cataloging standards (DCAT-US).

## Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](https://github.com/sierra-moxon/ber-data-registry/blob/main/CONTRIBUTING.md)
for guidelines.

### Development

**Prerequisites:** Python 3.9+, [uv](https://docs.astral.sh/uv/),
[just](https://github.com/casey/just)

```bash
# Clone and set up
git clone https://github.com/sierra-moxon/ber-data-registry.git
cd ber-data-registry
just install

# Run tests
just test

# Build and preview docs locally
just testdoc
```

### Project Structure

```
src/ber_data_registry/schema/   # LinkML schema (source of truth)
tests/data/valid/               # Example YAML files (used as test fixtures)
tests/data/invalid/             # Invalid examples for negative testing
docs/                           # Generated documentation site
```

## License

This project is licensed under the [MIT License](https://github.com/sierra-moxon/ber-data-registry/blob/main/LICENSE).

## Acknowledgments

Built using the [linkml-project-copier](https://github.com/dalito/linkml-project-copier)
template.

## Contact

For questions or issues, please open an issue on the
[GitHub repository](https://github.com/sierra-moxon/ber-data-registry/issues).
