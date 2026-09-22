# BER Lakehouse Registry

The BER lakehouse registry. Schemas, standards, and reporting formats relevant to BER lakehouse data, imported from the BER data management "schema sources" tracking sheet. Each schema/standard is registered as a data source hosted (or planned to be hosted) in the BRIDGE lakehouse. This file is the registry itself: edit it to add or update entries, and validate with `just test`.

Download the registry as YAML: [lakehouse-registry.yaml](lakehouse-registry.yaml)

To add or update an entry, edit [`lakehouse-registry.yaml`](https://github.com/ber-data/lakehouse-registry/blob/main/lakehouse-registry.yaml) in the repository root and open a pull request. Entries are validated against the [registry schema](elements/index.md) in CI.

## BRIDGE Lakehouse

Starburst-based BRIDGE data lakehouse serving as the primary hosting platform for data conforming to the registered BER schema sources. Platform is Starburst (Trino); recorded as 'other' because the PlatformType enum does not yet include starburst.

*Operator: Lawrence Berkeley National Laboratory · Platform: other · Entries: 48*

| Entry | Description | Owner (Contact) | Status | Access |
|-------|-------------|-----------------|--------|--------|
| [nmdc-schema](https://github.com/microbiomedata/nmdc-schema) | National Microbiome Data Collaborative (NMDC) LinkML schema and submission schema. Field/element names are intended to be clearly defined with metadata, not ju… | Montana Smith | active | public |
| IDeA-schema | A schema for AI-driven enzyme discovery and biosynthetic pathway optimization. Represents a target reaction, the enzyme families ranked against it, candidate e… | Arvind Ramanathan | experimental | internal |
| [plant phenotyping schema](https://github.com/MIAPPE/MIAPPE/blob/master/MIAPPE_Checklist_Data_Model.pdf) | Plant phenotyping schema for APPL (Advanced Plant Phenotyping Laboratory) based on the MIAPPE checklist and data model. | Priya Ranjan | experimental | public |
| [lambda-ber-schema](https://github.com/lambda-ber/lambda-ber-schema/tree/main/src/lambda_ber_schema/schema) | A comprehensive LinkML schema for representing multimodal structural biology imaging data, from atomic-resolution structures to tissue-level organization. | Harry Caufield | active | public |
| [aims-leaf](https://github.com/lambda-ber/aims-leaf/tree/main/src/aims_leaf_schema/schema) | A schema for plant biology data, built on the lambda-ber-schema. | Sam Webb (Harry Caufield) | experimental | public |
| JBEI Ganymede | Plant protein expression and sample data from the JBEI Ganymede system. Only a pseudo-schema is available. | Chris Petzold (Valerie Skye) | experimental | internal |
| [brc-schema](https://github.com/bioenergy-research-centers/brc-schema/tree/main/src/brc_schema/schema) | A schema for the Bioenergy Research Center portal. Describes properties of datasets in bioenergy, environmental science, earth science, and related fields. | Harry Caufield | active | public |
| [osti-schema](https://github.com/bioenergy-research-centers/brc-schema/blob/main/src/brc_schema/schema/osti_schema.yaml) | A LinkML representation of the E-Link 2.0 schema used by OSTI. Includes slots for legacy compatibility with previous E-Link versions. Developed as part of the… | Harry Caufield | active | public |
| [kg-registry-schema](https://github.com/Knowledge-Graph-Hub/kg-registry/tree/main/src/kg_registry/kg_registry_schema/schema) | A schema defining properties and relationships between knowledge graphs, data resources, interfaces, tools, and documentation. Part of the KG-Registry project… | Harry Caufield | active | public |
| [standards-schemas](https://github.com/bridge2ai/standards-schemas) | A schema for metadata about biomedical data standards, including their AI/ML applications, related topics, substrates, organizations, and more. Part of the Bri… | Harry Caufield | active | public |
| [data-sheets-schema](https://github.com/bridge2ai/data-sheets-schema) | A schema for detailed metadata about biological and biomedical datasets. Implemented as part of the Bridge2AI project. | Marcin Joachimiak (Harry Caufield) | active | public |
| [model-card-schema](https://github.com/bridge2ai/model-card-schema) | A schema for detailed metadata about computational models. Implemented as part of the Bridge2AI project. | Marcin Joachimiak (Harry Caufield) | active | public |
| [basin3d-linkml](https://github.com/dschristianson/basin3dschema) | Prototype basin3d data model in LinkML schema. | Danielle Christianson | experimental | public |
| [basin3d](https://github.com/BASIN-3D/basin3d) | Customizable on-demand data synthesis software based on OGC O&M data models; timeseries support. | Danielle Christianson | active | public |
| [ess-dive-rf](https://github.com/ess-dive-workspace) | ESS-DIVE Reporting Formats. | Danielle Christianson | active | public |
| [flux-processing](https://ameriflux.lbl.gov/data/aboutdata/data-variables/) | Fluxnet (AmeriFlux) standard for flux/met timeseries data; developed and supported by AmeriFlux, ICOS / EuroFlux. | Danielle Christianson | active | public |
| [badm](https://ameriflux.lbl.gov/data/badm/badm-standards/) | Biological Ancillary Disturbance Metadata (BADM) standard followed by the Fluxnet community for contextual and ancillary data observed at / near flux research… | Danielle Christianson | active | public |
| [geojson](https://datatracker.ietf.org/doc/html/rfc7946) | GeoJSON format (IETF RFC 7946). Listed here as a reference standard. | Danielle Christianson | active | public |
| [ogc-om3](https://docs.ogc.org/as/20-082r4/20-082r4.html) | OGC Observations & Measurements v3 (ISO 19156:2023(E); OGC 20-082r4 v3.0). Listed here as a reference standard. | Danielle Christianson | active | public |
| [OGC Features and Geometries JSON](https://docs.ogc.org/DRAFTS/21-045r1.html) | Proposed OGC Features & Geometries JSON standard (draft). Listed here as a reference standard. | Unknown | active | public |
| [OGC EO JSON-LD](https://www.ogc.org/standards/eo-geojson/) | OGC Earth Observation JSON-LD standard. Listed here as a reference standard. | Unknown | active | public |
| [ODM2](https://odm2.github.io/ODM2/schemas/ODM2_Current/diagrams/ODM2SamplingFeatures.html) | Observations Data Model 2 (ODM2), including sampling features, sampling feature geotypes, and elevation datum vocabularies. Listed here as a reference standard. | Danielle Christianson | active | public |
| [fgdc](https://www.fgdc.gov/standards/projects/metadata/base-metadata/v2_0698.pdf) | FGDC (Federal Geographic Data Committee) metadata and framework data standards. Listed here as a reference standard. | Danielle Christianson | active | public |
| [STAC](https://stacspec.org/en) | SpatioTemporal Asset Catalog (STAC) specification. Listed here as a reference standard. | Unknown | active | public |
| [USGS GeMS](https://ngmdb.usgs.gov/Info/standards/GeMS/) | USGS Geologic Map Schema (GeMS). Listed here as a reference standard. | Unknown | active | public |
| [EDX / DCAT](https://resources.data.gov/standards/catalog/dcat-us/) | NETL EDX data discovery and the DCAT-US metadata standard. Listed here as a reference standard. | Unknown | active | public |
| [iso19115-loc-meta](https://compass.astm.org/content-access?contentCode=ISO%7CISO%2FIEC%2030173%3A2023%7Cen-US) | ISO 19115 Location Metadata standard. Listed here as a reference standard. | Danielle Christianson | active | restricted |
| [OGC API - EDR](https://docs.ogc.org/is/19-086r4/19-086r4.html) | OGC API - Environmental Data Retrieval (EDR) standard. Listed here as a reference standard. | Unknown | active | public |
| [OGC API - Features](https://ogcapi.ogc.org/features/) | OGC API - Features standard. Listed here as a reference standard. | Unknown | active | public |
| [The Open Group OSDU Technical Standard](https://osduforum.org/01-the-osdu-technical-standard/) | The Open Group OSDU technical standard (industry standards organization). Listed here as a reference standard. | Unknown | active | public |
| [OGC Earth Observation Metadata](https://docs.ogc.org/is/10-157r4/10-157r4.html) | OGC Earth Observation Metadata profile. Listed here as a reference standard. | Unknown | active | public |
| [BERtron](https://ber-data.github.io/bertron-schema/) | Cross-BER sample metadata, geolocation-centric, with attributes, for NMDC, JGI, EMSL, ESS-DIVE. | Montana Smith (Sierra Moxon) | experimental | public |
| [JGI GFF](https://github.com/biodatamodels/gff-schema) | Annotations for JGI-produced genomes. | Valerie Skye | experimental | public |
| JGI GOLD | JGI project, sample, and analysis metadata (GOLD). | Valerie Skye | experimental | internal |
| JGI Proposal DB | JGI proposal database (via the data warehouse). | Valerie Skye | experimental | internal |
| [kbase-cdm](https://kbase.github.io/cdm-schema/) | KBase Central Data Model (CDM) schema. | AJ | active | public |
| [kbase-credit](https://www.kbase.us/news/kbase-credit-metadata-schema/) | KBase Credit Metadata schema. | AJ | active | public |
| [BASALT-Schema](https://github.com/EMSL-Computing/BASALT-Schema) | MONet data model broadening to support EMSL in general. | Yuri Corilo | active | public |
| [geochem-rf](https://sierra-moxon.github.io/geochem-rf-linkml/elements/erdiagram/) | A LinkML representation of the ESS-DIVE Reporting Formats for Sample Data, Sample ID and Metadata, Location Metadata, and File-level Metadata (the same content… | Danielle Christianson | experimental | internal |
| AmSC Open Metadata | American Science Cloud (AmSC) Open Metadata. Not for data loading into the lakehouse, but something the registry may need to conform or map to in order to be c… | Valerie Skye | experimental | restricted |
| [CORAL](https://github.com/jmchandonia/CORAL) | A framework for rigorous self-validated data modeling and integrative, reproducible data analysis. In some ways more like a data modeling framework (like LinkM… | Unknown | active | public |
| [GeoParquet](https://geoparquet.org/releases/v1.1.0/) | Parquet extension for geospatial data properties. | Unknown | active | public |
| [linkml-test](https://github.com/pranjan77/linkml-test/blob/main/src/linkml_test/schema/linkml_test.yaml) | A LinkML test schema. | Unknown | experimental | public |
| [miappe-linkml](https://github.com/sierra-moxon/miappe-linkml/blob/main/src/miappe_linkml/schema/miappe_linkml.yaml) | A LinkML representation of the MIAPPE plant phenotyping standard. Related to the plant phenotyping schema. | Unknown | experimental | public |
| [pathogen-genomics-package](https://github.com/cidgoh/pathogen-genomics-package/blob/main/templates/wastewater/schema.yaml) | LinkML schema templates for pathogen genomics, including a wastewater template. | Unknown | experimental | public |
| [nmdc-lakehouse-schema](https://github.com/microbiomedata/nmdc-lakehouse-schema/blob/main/src/nmdc_lakehouse_schema/schema/nmdc_schema_flattened.yaml) | A flattened LinkML representation of the NMDC schema for lakehouse use. Related to nmdc-schema. | Unknown | experimental | public |
| [lakehouse-schema-extraction](https://github.com/sierra-moxon/lakehouse-schema-extraction/tree/main/schemas) | Schemas extracted from lakehouse sources, represented in LinkML. | Unknown | experimental | public |
| [basin3d-schema](https://github.com/cmungall/basin3d_schema/blob/main/src/basin3d_schema/schema/basin3d_schema.yaml) | A LinkML schema for the basin3d data model. Related to basin3d-linkml and basin3d. | Unknown | experimental | public |

