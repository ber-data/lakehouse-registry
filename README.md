<a href="https://github.com/dalito/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# ber-data-registry

The BER Lakehouse Registry: a catalog of schemas, standards, and data sources
for BER lakehouses, validated against a LinkML schema.

## The Registry

The registry itself lives in [`lakehouse-registry.yaml`](lakehouse-registry.yaml)
at the root of this repository. **To register a schema or data source, edit that
file and open a pull request.** Entries are validated against the
[registry schema](src/ber_data_registry/schema/ber_data_registry.yaml) by
`just test` and in CI.

The registry is published on the documentation site:

* Browsable view: <https://ber-data.github.io/lakehouse-registry/registry/>
* Raw YAML: <https://ber-data.github.io/lakehouse-registry/lakehouse-registry.yaml>

## Documentation Website

[https://ber-data.github.io/lakehouse-registry](https://ber-data.github.io/lakehouse-registry)

## Repository Structure

* [lakehouse-registry.yaml](lakehouse-registry.yaml) - the registry itself (edit this to add entries)
* [docs/](docs/) - mkdocs-managed documentation
  * [elements/](docs/elements/) - generated schema documentation
* [examples/](examples/) - Examples of using the schema
* [project/](project/) - project files (these files are auto-generated, do not edit)
* [src/](src/) - source files (edit these)
  * [ber_data_registry](src/ber_data_registry)
    * [schema/](src/ber_data_registry/schema) -- LinkML schema
      (edit this)
    * [datamodel/](src/ber_data_registry/datamodel) -- generated
      Python datamodel
* [tests/](tests/) - Python tests
  * [data/](tests/data) - Example data

## Developer Tools

There are several pre-defined command-recipes available.
They are written for the command runner [just](https://github.com/casey/just/). To list all pre-defined commands, run `just` or `just --list`.

## Credits

This project uses the template [linkml-project-copier](https://github.com/dalito/linkml-project-copier) published as [doi:10.5281/zenodo.15163584](https://doi.org/10.5281/zenodo.15163584).
