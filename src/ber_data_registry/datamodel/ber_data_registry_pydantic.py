from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "None"
version = "0.1.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )

    @model_serializer(mode='wrap', when_used='unless-none')
    def treat_empty_lists_as_none(
            self, handler: SerializerFunctionWrapHandler,
            info: SerializationInfo) -> dict[str, Any]:
        if info.exclude_none:
            _instance = self.model_copy()
            for field, field_info in type(_instance).model_fields.items():
                if getattr(_instance, field) == [] and not(
                        field_info.is_required()):
                    setattr(_instance, field, None)
        else:
            _instance = self
        return handler(_instance, info)



class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'ber_registry',
     'default_range': 'string',
     'description': 'A LinkML schema for cataloging databases and data sources '
                    'across scientific lakehouses at LBNL, including KBASE '
                    '(Spark-based) and Dremio environments. Informed by the HPDF '
                    'Data Catalog & Lakehouse Demo report (Cohoon & Paine, '
                    'LBNL-2001745, Dec 2025), DCAT v3, and DCAT-US.',
     'id': 'https://w3id.org/ber-data/ber-data-registry',
     'imports': ['linkml:types'],
     'license': 'MIT',
     'name': 'ber_data_registry',
     'prefixes': {'ber_registry': {'prefix_prefix': 'ber_registry',
                                   'prefix_reference': 'https://w3id.org/ber-data/ber-data-registry/'},
                  'dcat': {'prefix_prefix': 'dcat',
                           'prefix_reference': 'http://www.w3.org/ns/dcat#'},
                  'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'pav': {'prefix_prefix': 'pav',
                          'prefix_reference': 'http://purl.org/pav/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'},
                  'vcard': {'prefix_prefix': 'vcard',
                            'prefix_reference': 'http://www.w3.org/2006/vcard/ns#'}},
     'source_file': 'src/ber_data_registry/schema/ber_data_registry.yaml',
     'title': 'BER Data Registry'} )

class DataSourceStatus(str, Enum):
    """
    Lifecycle status of a data source.
    """
    active = "active"
    """
    Data source is actively maintained and available.
    """
    deprecated = "deprecated"
    """
    Data source is deprecated and should not be used for new work.
    """
    archived = "archived"
    """
    Data source is archived and read-only.
    """
    experimental = "experimental"
    """
    Data source is experimental or in development.
    """
    test = "test"
    """
    Data source is used for testing purposes only.
    """


class AccessLevel(str, Enum):
    """
    Visibility and access restrictions for a data source.
    """
    public = "public"
    """
    Accessible to anyone.
    """
    restricted = "restricted"
    """
    Access requires authorization or approval.
    """
    internal = "internal"
    """
    Only accessible within the organization.
    """


class UpdateFrequency(str, Enum):
    """
    How often a data source is updated.
    """
    real_time = "real_time"
    """
    Continuously updated in real time.
    """
    daily = "daily"
    """
    Updated once per day.
    """
    weekly = "weekly"
    """
    Updated once per week.
    """
    monthly = "monthly"
    """
    Updated once per month.
    """
    quarterly = "quarterly"
    """
    Updated once per quarter.
    """
    annually = "annually"
    """
    Updated once per year.
    """
    irregular = "irregular"
    """
    Updated at irregular intervals.
    """
    static = "static"
    """
    Not expected to be updated.
    """
    unknown = "unknown"
    """
    Update frequency is not known.
    """


class DataSourceCategory(str, Enum):
    """
    Organizational category for a data source.
    """
    project = "project"
    """
    Belongs to a specific research project.
    """
    shared = "shared"
    """
    Shared across multiple projects or teams.
    """
    personal = "personal"
    """
    Personal workspace of an individual user.
    """
    system = "system"
    """
    System-level or infrastructure data.
    """


class PlatformType(str, Enum):
    """
    Technology platform for a lakehouse.
    """
    spark = "spark"
    """
    Apache Spark-based lakehouse (e.g. KBASE).
    """
    dremio = "dremio"
    """
    Dremio data lakehouse platform.
    """
    other = "other"
    """
    Other platform type.
    """


class SourceType(str, Enum):
    """
    Type of data source within a lakehouse, particularly relevant for Dremio environments.
    """
    namespace = "namespace"
    """
    A namespace within a Spark-based lakehouse.
    """
    object_storage = "object_storage"
    """
    Object storage source (e.g. S3, MinIO).
    """
    relational_database = "relational_database"
    """
    Relational database source (PostgreSQL, MySQL).
    """
    document_database = "document_database"
    """
    Document database source (e.g. MongoDB).
    """
    space = "space"
    """
    A Dremio space for organizing views and virtual datasets.
    """


class DatabaseEngine(str, Enum):
    """
    Specific database engine for database-type sources.
    """
    postgresql = "postgresql"
    """
    PostgreSQL database.
    """
    mysql = "mysql"
    """
    MySQL database.
    """
    mongodb = "mongodb"
    """
    MongoDB document database.
    """
    spark_sql = "spark_sql"
    """
    Spark SQL engine.
    """
    other = "other"
    """
    Other database engine.
    """



class Catalog(ConfiguredBaseModel):
    """
    Top-level container for the BER data catalog, holding references to lakehouses and their cataloged data sources.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dcat:Catalog',
         'from_schema': 'https://w3id.org/ber-data/ber-data-registry',
         'tree_root': True})

    id: str = Field(default=..., description="""Unique identifier for this catalog entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog', 'CatalogEntity'], 'slot_uri': 'schema:identifier'} })
    title: str = Field(default=..., description="""Human-readable name for this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog', 'CatalogEntity'], 'slot_uri': 'dcterms:title'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog', 'CatalogEntity'], 'slot_uri': 'dcterms:description'} })
    lakehouses: Optional[list[Lakehouse]] = Field(default=[], description="""Lakehouses registered in this catalog.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog']} })


class CatalogEntity(ConfiguredBaseModel):
    """
    Abstract base class providing shared metadata fields for all catalog entries. Each data source is a catalog entity. 
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'https://w3id.org/ber-data/ber-data-registry'})

    id: str = Field(default=..., description="""Unique identifier for this catalog entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog', 'CatalogEntity'], 'slot_uri': 'schema:identifier'} })
    title: str = Field(default=..., description="""Human-readable name for this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog', 'CatalogEntity'], 'slot_uri': 'dcterms:title'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog', 'CatalogEntity'], 'slot_uri': 'dcterms:description'} })
    created_date: Optional[date] = Field(default=None, description="""Date this entity was first created or registered.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CatalogEntity'], 'slot_uri': 'dcterms:created'} })
    last_modified: Optional[date] = Field(default=None, description="""Date this entity was last updated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CatalogEntity'], 'slot_uri': 'dcterms:modified'} })


class Lakehouse(CatalogEntity):
    """
    A lakehouse environment such as the KBASE Spark lakehouse or a Dremio instance. Serves as the hosting platform for one or more DataSources.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dcat:DataService',
         'from_schema': 'https://w3id.org/ber-data/ber-data-registry'})

    endpoint_url: Optional[str] = Field(default=None, description="""URL endpoint for accessing the lakehouse.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Lakehouse'], 'slot_uri': 'dcat:endpointURL'} })
    operator: Optional[str] = Field(default=None, description="""Organization or team operating this lakehouse.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Lakehouse'], 'slot_uri': 'dcterms:publisher'} })
    platform_type: Optional[PlatformType] = Field(default=None, description="""The technology platform underlying this lakehouse.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Lakehouse']} })
    catalog_entries: Optional[list[DataSource]] = Field(default=[], description="""Catalog entries (data sources) hosted in this lakehouse.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Lakehouse']} })
    id: str = Field(default=..., description="""Unique identifier for this catalog entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog', 'CatalogEntity'], 'slot_uri': 'schema:identifier'} })
    title: str = Field(default=..., description="""Human-readable name for this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog', 'CatalogEntity'], 'slot_uri': 'dcterms:title'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog', 'CatalogEntity'], 'slot_uri': 'dcterms:description'} })
    created_date: Optional[date] = Field(default=None, description="""Date this entity was first created or registered.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CatalogEntity'], 'slot_uri': 'dcterms:created'} })
    last_modified: Optional[date] = Field(default=None, description="""Date this entity was last updated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CatalogEntity'], 'slot_uri': 'dcterms:modified'} })


class DataSource(CatalogEntity):
    """
    A cataloged data source within a lakehouse. Represents a namespace, database, object storage source, or other data collection. All required fields must be present on every submission.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dcat:Dataset',
         'from_schema': 'https://w3id.org/ber-data/ber-data-registry',
         'slot_usage': {'access_level': {'name': 'access_level', 'required': True},
                        'contact_point': {'name': 'contact_point', 'required': True},
                        'created_date': {'name': 'created_date', 'required': True},
                        'description': {'name': 'description', 'required': True},
                        'is_deprecated': {'name': 'is_deprecated', 'required': True},
                        'namespace': {'name': 'namespace', 'required': True},
                        'owner': {'name': 'owner', 'required': True},
                        'status': {'name': 'status', 'required': True},
                        'update_schedule': {'name': 'update_schedule',
                                            'required': True}}})

    owner: str = Field(default=..., description="""Person or team responsible for this data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource'], 'slot_uri': 'dcterms:publisher'} })
    contact_point: ContactPoint = Field(default=..., description="""Structured contact information for this data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource'], 'slot_uri': 'dcat:contactPoint'} })
    namespace: str = Field(default=..., description="""Database name, source name, or space name within the lakehouse (e.g. \"kbase_public\", \"jgi_object_store\").""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    status: DataSourceStatus = Field(default=..., description="""Current lifecycle status of this data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource'], 'slot_uri': 'dcat:status'} })
    is_deprecated: bool = Field(default=..., description="""Whether this data source is deprecated. Must always be explicitly set.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    update_schedule: UpdateFrequency = Field(default=..., description="""How frequently this data source is updated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource'], 'slot_uri': 'dcterms:accrualPeriodicity'} })
    access_level: AccessLevel = Field(default=..., description="""Visibility/access level of this data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    keywords: Optional[list[str]] = Field(default=[], description="""Discovery tags for this data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource'], 'slot_uri': 'dcat:keyword'} })
    project_affiliation: Optional[list[str]] = Field(default=[], description="""BER program affiliations (e.g. KBase, NMDC, JGI, Phage Foundry).""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    license: Optional[str] = Field(default=None, description="""License governing use of this data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource'], 'slot_uri': 'dcterms:license'} })
    domain: Optional[list[str]] = Field(default=[], description="""Scientific domain(s) covered by this data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource'], 'slot_uri': 'dcat:theme'} })
    version: Optional[str] = Field(default=None, description="""Version identifier for this data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource'], 'slot_uri': 'pav:version'} })
    doi: Optional[str] = Field(default=None, description="""DOI if this data source has been published.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    facility: Optional[str] = Field(default=None, description="""Originating facility (e.g. NERSC, JGI, EMSL) per HPDF report recommendations.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    format: Optional[list[str]] = Field(default=[], description="""Data format(s) available (e.g. Parquet, CSV, HDF5, Zarr, NetCDF, FITS).""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource'], 'slot_uri': 'dcterms:format'} })
    deprecation_date: Optional[date] = Field(default=None, description="""Date this data source was deprecated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    deprecation_reason: Optional[str] = Field(default=None, description="""Explanation for why this data source was deprecated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    replaced_by: Optional[str] = Field(default=None, description="""Reference to the data source that replaces this deprecated one.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    previous_version: Optional[str] = Field(default=None, description="""Reference to the previous version of this data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    temporal_coverage_start: Optional[date] = Field(default=None, description="""Start date of the temporal coverage of this data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    temporal_coverage_end: Optional[date] = Field(default=None, description="""End date of the temporal coverage of this data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    spatial_coverage: Optional[str] = Field(default=None, description="""Geographic or spatial coverage description.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    data_quality_notes: Optional[str] = Field(default=None, description="""Notes on data quality, known issues, or limitations.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    lineage: Optional[str] = Field(default=None, description="""Provenance or lineage information for this data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource'], 'slot_uri': 'prov:wasDerivedFrom'} })
    documentation_url: Optional[str] = Field(default=None, description="""URL to external documentation for this data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    instrument: Optional[str] = Field(default=None, description="""Instrument or sensor that generated the data.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    modality: Optional[str] = Field(default=None, description="""Data modality (e.g. genomic, proteomic, imaging).""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    size_bytes: Optional[int] = Field(default=None, description="""Total size of the data source in bytes.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    row_count: Optional[int] = Field(default=None, description="""Number of rows or records in the data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    table_count: Optional[int] = Field(default=None, description="""Number of tables or collections in the data source.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    source_type: Optional[SourceType] = Field(default=None, description="""Type of data source within the lakehouse (e.g. namespace, object_storage, relational_database).""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    database_engine: Optional[DatabaseEngine] = Field(default=None, description="""Database engine for Dremio database sources (e.g. postgresql, mysql, mongodb).""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    category: Optional[DataSourceCategory] = Field(default=None, description="""Organizational category (project, shared, personal, system).""", json_schema_extra = { "linkml_meta": {'domain_of': ['DataSource']} })
    id: str = Field(default=..., description="""Unique identifier for this catalog entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog', 'CatalogEntity'], 'slot_uri': 'schema:identifier'} })
    title: str = Field(default=..., description="""Human-readable name for this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog', 'CatalogEntity'], 'slot_uri': 'dcterms:title'} })
    description: str = Field(default=..., description="""Free-text description of this entity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Catalog', 'CatalogEntity'], 'slot_uri': 'dcterms:description'} })
    created_date: date = Field(default=..., description="""Date this entity was first created or registered.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CatalogEntity'], 'slot_uri': 'dcterms:created'} })
    last_modified: Optional[date] = Field(default=None, description="""Date this entity was last updated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CatalogEntity'], 'slot_uri': 'dcterms:modified'} })


class ContactPoint(ConfiguredBaseModel):
    """
    Structured contact information for a data source, providing a name and email for the responsible party.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'vcard:Kind',
         'from_schema': 'https://w3id.org/ber-data/ber-data-registry'})

    contact_name: str = Field(default=..., description="""Full name of the contact person.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ContactPoint'], 'slot_uri': 'vcard:fn'} })
    contact_email: str = Field(default=..., description="""Email address of the contact person.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ContactPoint'], 'slot_uri': 'vcard:hasEmail'} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Catalog.model_rebuild()
CatalogEntity.model_rebuild()
Lakehouse.model_rebuild()
DataSource.model_rebuild()
ContactPoint.model_rebuild()
