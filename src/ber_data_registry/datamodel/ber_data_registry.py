# Auto generated from ber_data_registry.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-04-10T08:25:47
# Schema: ber_data_registry
#
# id: https://w3id.org/ber-data/ber-data-registry
# description: A LinkML schema for cataloging databases and data sources across scientific lakehouses at LBNL, including KBASE (Spark-based) and Dremio environments. Informed by the HPDF Data Catalog & Lakehouse Demo report (Cohoon & Paine, LBNL-2001745, Dec 2025), DCAT v3, and DCAT-US.
# license: MIT

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, Integer, String, Uri, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URI, URIorCURIE, XSDDate

metamodel_version = "1.7.0"
version = "0.1.0"

# Namespaces
BER_REGISTRY = CurieNamespace('ber_registry', 'https://w3id.org/ber-data/ber-data-registry/')
DCAT = CurieNamespace('dcat', 'http://www.w3.org/ns/dcat#')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
VCARD = CurieNamespace('vcard', 'http://www.w3.org/2006/vcard/ns#')
DEFAULT_ = BER_REGISTRY


# Types

# Class references
class CatalogId(URIorCURIE):
    pass


class CatalogEntityId(URIorCURIE):
    pass


class LakehouseId(CatalogEntityId):
    pass


class DataSourceId(CatalogEntityId):
    pass


@dataclass(repr=False)
class Catalog(YAMLRoot):
    """
    Top-level container for the BER data catalog, holding references to lakehouses and their cataloged data sources.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Catalog"]
    class_class_curie: ClassVar[str] = "dcat:Catalog"
    class_name: ClassVar[str] = "Catalog"
    class_model_uri: ClassVar[URIRef] = BER_REGISTRY.Catalog

    id: Union[str, CatalogId] = None
    title: str = None
    description: Optional[str] = None
    lakehouses: Optional[Union[dict[Union[str, LakehouseId], Union[dict, "Lakehouse"]], list[Union[dict, "Lakehouse"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CatalogId):
            self.id = CatalogId(self.id)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_list(slot_name="lakehouses", slot_type=Lakehouse, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CatalogEntity(YAMLRoot):
    """
    Abstract base class providing shared metadata fields for all catalog entries. Each data source is a catalog entity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BER_REGISTRY["CatalogEntity"]
    class_class_curie: ClassVar[str] = "ber_registry:CatalogEntity"
    class_name: ClassVar[str] = "CatalogEntity"
    class_model_uri: ClassVar[URIRef] = BER_REGISTRY.CatalogEntity

    id: Union[str, CatalogEntityId] = None
    title: str = None
    description: Optional[str] = None
    created_date: Optional[Union[str, XSDDate]] = None
    last_modified: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CatalogEntityId):
            self.id = CatalogEntityId(self.id)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.created_date is not None and not isinstance(self.created_date, XSDDate):
            self.created_date = XSDDate(self.created_date)

        if self.last_modified is not None and not isinstance(self.last_modified, XSDDate):
            self.last_modified = XSDDate(self.last_modified)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Lakehouse(CatalogEntity):
    """
    A lakehouse environment such as the KBASE Spark lakehouse or a Dremio instance. Serves as the hosting platform for
    one or more DataSources.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["DataService"]
    class_class_curie: ClassVar[str] = "dcat:DataService"
    class_name: ClassVar[str] = "Lakehouse"
    class_model_uri: ClassVar[URIRef] = BER_REGISTRY.Lakehouse

    id: Union[str, LakehouseId] = None
    title: str = None
    endpoint_url: Optional[Union[str, URI]] = None
    operator: Optional[str] = None
    platform_type: Optional[Union[str, "PlatformType"]] = None
    catalog_entries: Optional[Union[dict[Union[str, DataSourceId], Union[dict, "DataSource"]], list[Union[dict, "DataSource"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LakehouseId):
            self.id = LakehouseId(self.id)

        if self.endpoint_url is not None and not isinstance(self.endpoint_url, URI):
            self.endpoint_url = URI(self.endpoint_url)

        if self.operator is not None and not isinstance(self.operator, str):
            self.operator = str(self.operator)

        if self.platform_type is not None and not isinstance(self.platform_type, PlatformType):
            self.platform_type = PlatformType(self.platform_type)

        self._normalize_inlined_as_list(slot_name="catalog_entries", slot_type=DataSource, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataSource(CatalogEntity):
    """
    A cataloged data source within a lakehouse. Represents a namespace, database, object storage source, or other data
    collection. All required fields must be present on every submission.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Dataset"]
    class_class_curie: ClassVar[str] = "dcat:Dataset"
    class_name: ClassVar[str] = "DataSource"
    class_model_uri: ClassVar[URIRef] = BER_REGISTRY.DataSource

    id: Union[str, DataSourceId] = None
    title: str = None
    owner: str = None
    contact_point: Union[dict, "ContactPoint"] = None
    namespace: str = None
    status: Union[str, "DataSourceStatus"] = None
    is_deprecated: Union[bool, Bool] = None
    update_schedule: Union[str, "UpdateFrequency"] = None
    access_level: Union[str, "AccessLevel"] = None
    description: str = None
    created_date: Union[str, XSDDate] = None
    keywords: Optional[Union[str, list[str]]] = empty_list()
    project_affiliation: Optional[Union[str, list[str]]] = empty_list()
    license: Optional[str] = None
    domain: Optional[Union[str, list[str]]] = empty_list()
    version: Optional[str] = None
    doi: Optional[str] = None
    facility: Optional[str] = None
    format: Optional[Union[str, list[str]]] = empty_list()
    deprecation_date: Optional[Union[str, XSDDate]] = None
    deprecation_reason: Optional[str] = None
    replaced_by: Optional[Union[str, DataSourceId]] = None
    previous_version: Optional[Union[str, DataSourceId]] = None
    temporal_coverage_start: Optional[Union[str, XSDDate]] = None
    temporal_coverage_end: Optional[Union[str, XSDDate]] = None
    spatial_coverage: Optional[str] = None
    data_quality_notes: Optional[str] = None
    lineage: Optional[str] = None
    documentation_url: Optional[Union[str, URI]] = None
    instrument: Optional[str] = None
    modality: Optional[str] = None
    size_bytes: Optional[int] = None
    row_count: Optional[int] = None
    table_count: Optional[int] = None
    source_type: Optional[Union[str, "SourceType"]] = None
    database_engine: Optional[Union[str, "DatabaseEngine"]] = None
    category: Optional[Union[str, "DataSourceCategory"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataSourceId):
            self.id = DataSourceId(self.id)

        if self._is_empty(self.owner):
            self.MissingRequiredField("owner")
        if not isinstance(self.owner, str):
            self.owner = str(self.owner)

        if self._is_empty(self.contact_point):
            self.MissingRequiredField("contact_point")
        if not isinstance(self.contact_point, ContactPoint):
            self.contact_point = ContactPoint(**as_dict(self.contact_point))

        if self._is_empty(self.namespace):
            self.MissingRequiredField("namespace")
        if not isinstance(self.namespace, str):
            self.namespace = str(self.namespace)

        if self._is_empty(self.status):
            self.MissingRequiredField("status")
        if not isinstance(self.status, DataSourceStatus):
            self.status = DataSourceStatus(self.status)

        if self._is_empty(self.is_deprecated):
            self.MissingRequiredField("is_deprecated")
        if not isinstance(self.is_deprecated, Bool):
            self.is_deprecated = Bool(self.is_deprecated)

        if self._is_empty(self.update_schedule):
            self.MissingRequiredField("update_schedule")
        if not isinstance(self.update_schedule, UpdateFrequency):
            self.update_schedule = UpdateFrequency(self.update_schedule)

        if self._is_empty(self.access_level):
            self.MissingRequiredField("access_level")
        if not isinstance(self.access_level, AccessLevel):
            self.access_level = AccessLevel(self.access_level)

        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, str):
            self.description = str(self.description)

        if self._is_empty(self.created_date):
            self.MissingRequiredField("created_date")
        if not isinstance(self.created_date, XSDDate):
            self.created_date = XSDDate(self.created_date)

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        if not isinstance(self.project_affiliation, list):
            self.project_affiliation = [self.project_affiliation] if self.project_affiliation is not None else []
        self.project_affiliation = [v if isinstance(v, str) else str(v) for v in self.project_affiliation]

        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        if not isinstance(self.domain, list):
            self.domain = [self.domain] if self.domain is not None else []
        self.domain = [v if isinstance(v, str) else str(v) for v in self.domain]

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.doi is not None and not isinstance(self.doi, str):
            self.doi = str(self.doi)

        if self.facility is not None and not isinstance(self.facility, str):
            self.facility = str(self.facility)

        if not isinstance(self.format, list):
            self.format = [self.format] if self.format is not None else []
        self.format = [v if isinstance(v, str) else str(v) for v in self.format]

        if self.deprecation_date is not None and not isinstance(self.deprecation_date, XSDDate):
            self.deprecation_date = XSDDate(self.deprecation_date)

        if self.deprecation_reason is not None and not isinstance(self.deprecation_reason, str):
            self.deprecation_reason = str(self.deprecation_reason)

        if self.replaced_by is not None and not isinstance(self.replaced_by, DataSourceId):
            self.replaced_by = DataSourceId(self.replaced_by)

        if self.previous_version is not None and not isinstance(self.previous_version, DataSourceId):
            self.previous_version = DataSourceId(self.previous_version)

        if self.temporal_coverage_start is not None and not isinstance(self.temporal_coverage_start, XSDDate):
            self.temporal_coverage_start = XSDDate(self.temporal_coverage_start)

        if self.temporal_coverage_end is not None and not isinstance(self.temporal_coverage_end, XSDDate):
            self.temporal_coverage_end = XSDDate(self.temporal_coverage_end)

        if self.spatial_coverage is not None and not isinstance(self.spatial_coverage, str):
            self.spatial_coverage = str(self.spatial_coverage)

        if self.data_quality_notes is not None and not isinstance(self.data_quality_notes, str):
            self.data_quality_notes = str(self.data_quality_notes)

        if self.lineage is not None and not isinstance(self.lineage, str):
            self.lineage = str(self.lineage)

        if self.documentation_url is not None and not isinstance(self.documentation_url, URI):
            self.documentation_url = URI(self.documentation_url)

        if self.instrument is not None and not isinstance(self.instrument, str):
            self.instrument = str(self.instrument)

        if self.modality is not None and not isinstance(self.modality, str):
            self.modality = str(self.modality)

        if self.size_bytes is not None and not isinstance(self.size_bytes, int):
            self.size_bytes = int(self.size_bytes)

        if self.row_count is not None and not isinstance(self.row_count, int):
            self.row_count = int(self.row_count)

        if self.table_count is not None and not isinstance(self.table_count, int):
            self.table_count = int(self.table_count)

        if self.source_type is not None and not isinstance(self.source_type, SourceType):
            self.source_type = SourceType(self.source_type)

        if self.database_engine is not None and not isinstance(self.database_engine, DatabaseEngine):
            self.database_engine = DatabaseEngine(self.database_engine)

        if self.category is not None and not isinstance(self.category, DataSourceCategory):
            self.category = DataSourceCategory(self.category)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContactPoint(YAMLRoot):
    """
    Structured contact information for a data source, providing a name and email for the responsible party.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VCARD["Kind"]
    class_class_curie: ClassVar[str] = "vcard:Kind"
    class_name: ClassVar[str] = "ContactPoint"
    class_model_uri: ClassVar[URIRef] = BER_REGISTRY.ContactPoint

    contact_name: str = None
    contact_email: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contact_name):
            self.MissingRequiredField("contact_name")
        if not isinstance(self.contact_name, str):
            self.contact_name = str(self.contact_name)

        if self._is_empty(self.contact_email):
            self.MissingRequiredField("contact_email")
        if not isinstance(self.contact_email, str):
            self.contact_email = str(self.contact_email)

        super().__post_init__(**kwargs)


# Enumerations
class DataSourceStatus(EnumDefinitionImpl):
    """
    Lifecycle status of a data source.
    """
    active = PermissibleValue(
        text="active",
        description="Data source is actively maintained and available.")
    deprecated = PermissibleValue(
        text="deprecated",
        description="Data source is deprecated and should not be used for new work.")
    archived = PermissibleValue(
        text="archived",
        description="Data source is archived and read-only.")
    experimental = PermissibleValue(
        text="experimental",
        description="Data source is experimental or in development.")
    test = PermissibleValue(
        text="test",
        description="Data source is used for testing purposes only.")

    _defn = EnumDefinition(
        name="DataSourceStatus",
        description="Lifecycle status of a data source.",
    )

class AccessLevel(EnumDefinitionImpl):
    """
    Visibility and access restrictions for a data source.
    """
    public = PermissibleValue(
        text="public",
        description="Accessible to anyone.")
    restricted = PermissibleValue(
        text="restricted",
        description="Access requires authorization or approval.")
    internal = PermissibleValue(
        text="internal",
        description="Only accessible within the organization.")

    _defn = EnumDefinition(
        name="AccessLevel",
        description="Visibility and access restrictions for a data source.",
    )

class UpdateFrequency(EnumDefinitionImpl):
    """
    How often a data source is updated.
    """
    real_time = PermissibleValue(
        text="real_time",
        description="Continuously updated in real time.")
    daily = PermissibleValue(
        text="daily",
        description="Updated once per day.")
    weekly = PermissibleValue(
        text="weekly",
        description="Updated once per week.")
    monthly = PermissibleValue(
        text="monthly",
        description="Updated once per month.")
    quarterly = PermissibleValue(
        text="quarterly",
        description="Updated once per quarter.")
    annually = PermissibleValue(
        text="annually",
        description="Updated once per year.")
    irregular = PermissibleValue(
        text="irregular",
        description="Updated at irregular intervals.")
    static = PermissibleValue(
        text="static",
        description="Not expected to be updated.")
    unknown = PermissibleValue(
        text="unknown",
        description="Update frequency is not known.")

    _defn = EnumDefinition(
        name="UpdateFrequency",
        description="How often a data source is updated.",
    )

class DataSourceCategory(EnumDefinitionImpl):
    """
    Organizational category for a data source.
    """
    project = PermissibleValue(
        text="project",
        description="Belongs to a specific research project.")
    shared = PermissibleValue(
        text="shared",
        description="Shared across multiple projects or teams.")
    personal = PermissibleValue(
        text="personal",
        description="Personal workspace of an individual user.")
    system = PermissibleValue(
        text="system",
        description="System-level or infrastructure data.")

    _defn = EnumDefinition(
        name="DataSourceCategory",
        description="Organizational category for a data source.",
    )

class PlatformType(EnumDefinitionImpl):
    """
    Technology platform for a lakehouse.
    """
    spark = PermissibleValue(
        text="spark",
        description="Apache Spark-based lakehouse (e.g. KBASE).")
    dremio = PermissibleValue(
        text="dremio",
        description="Dremio data lakehouse platform.")
    other = PermissibleValue(
        text="other",
        description="Other platform type.")

    _defn = EnumDefinition(
        name="PlatformType",
        description="Technology platform for a lakehouse.",
    )

class SourceType(EnumDefinitionImpl):
    """
    Type of data source within a lakehouse, particularly relevant for Dremio environments.
    """
    namespace = PermissibleValue(
        text="namespace",
        description="A namespace within a Spark-based lakehouse.")
    object_storage = PermissibleValue(
        text="object_storage",
        description="Object storage source (e.g. S3, MinIO).")
    relational_database = PermissibleValue(
        text="relational_database",
        description="Relational database source (PostgreSQL, MySQL).")
    document_database = PermissibleValue(
        text="document_database",
        description="Document database source (e.g. MongoDB).")
    space = PermissibleValue(
        text="space",
        description="A Dremio space for organizing views and virtual datasets.")

    _defn = EnumDefinition(
        name="SourceType",
        description="Type of data source within a lakehouse, particularly relevant for Dremio environments.",
    )

class DatabaseEngine(EnumDefinitionImpl):
    """
    Specific database engine for database-type sources.
    """
    postgresql = PermissibleValue(
        text="postgresql",
        description="PostgreSQL database.")
    mysql = PermissibleValue(
        text="mysql",
        description="MySQL database.")
    mongodb = PermissibleValue(
        text="mongodb",
        description="MongoDB document database.")
    spark_sql = PermissibleValue(
        text="spark_sql",
        description="Spark SQL engine.")
    other = PermissibleValue(
        text="other",
        description="Other database engine.")

    _defn = EnumDefinition(
        name="DatabaseEngine",
        description="Specific database engine for database-type sources.",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=SCHEMA.identifier, name="id", curie=SCHEMA.curie('identifier'),
                   model_uri=BER_REGISTRY.id, domain=None, range=URIRef)

slots.title = Slot(uri=DCTERMS.title, name="title", curie=DCTERMS.curie('title'),
                   model_uri=BER_REGISTRY.title, domain=None, range=str)

slots.description = Slot(uri=DCTERMS.description, name="description", curie=DCTERMS.curie('description'),
                   model_uri=BER_REGISTRY.description, domain=None, range=Optional[str])

slots.created_date = Slot(uri=DCTERMS.created, name="created_date", curie=DCTERMS.curie('created'),
                   model_uri=BER_REGISTRY.created_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.last_modified = Slot(uri=DCTERMS.modified, name="last_modified", curie=DCTERMS.curie('modified'),
                   model_uri=BER_REGISTRY.last_modified, domain=None, range=Optional[Union[str, XSDDate]])

slots.endpoint_url = Slot(uri=DCAT.endpointURL, name="endpoint_url", curie=DCAT.curie('endpointURL'),
                   model_uri=BER_REGISTRY.endpoint_url, domain=None, range=Optional[Union[str, URI]])

slots.operator = Slot(uri=DCTERMS.publisher, name="operator", curie=DCTERMS.curie('publisher'),
                   model_uri=BER_REGISTRY.operator, domain=None, range=Optional[str])

slots.platform_type = Slot(uri=BER_REGISTRY.platform_type, name="platform_type", curie=BER_REGISTRY.curie('platform_type'),
                   model_uri=BER_REGISTRY.platform_type, domain=None, range=Optional[Union[str, "PlatformType"]])

slots.owner = Slot(uri=DCTERMS.publisher, name="owner", curie=DCTERMS.curie('publisher'),
                   model_uri=BER_REGISTRY.owner, domain=None, range=Optional[str])

slots.contact_point = Slot(uri=DCAT.contactPoint, name="contact_point", curie=DCAT.curie('contactPoint'),
                   model_uri=BER_REGISTRY.contact_point, domain=None, range=Optional[Union[dict, ContactPoint]])

slots.namespace = Slot(uri=BER_REGISTRY.namespace, name="namespace", curie=BER_REGISTRY.curie('namespace'),
                   model_uri=BER_REGISTRY.namespace, domain=None, range=Optional[str])

slots.status = Slot(uri=DCAT.status, name="status", curie=DCAT.curie('status'),
                   model_uri=BER_REGISTRY.status, domain=None, range=Optional[Union[str, "DataSourceStatus"]])

slots.is_deprecated = Slot(uri=BER_REGISTRY.is_deprecated, name="is_deprecated", curie=BER_REGISTRY.curie('is_deprecated'),
                   model_uri=BER_REGISTRY.is_deprecated, domain=None, range=Optional[Union[bool, Bool]])

slots.update_schedule = Slot(uri=DCTERMS.accrualPeriodicity, name="update_schedule", curie=DCTERMS.curie('accrualPeriodicity'),
                   model_uri=BER_REGISTRY.update_schedule, domain=None, range=Optional[Union[str, "UpdateFrequency"]])

slots.access_level = Slot(uri=BER_REGISTRY.access_level, name="access_level", curie=BER_REGISTRY.curie('access_level'),
                   model_uri=BER_REGISTRY.access_level, domain=None, range=Optional[Union[str, "AccessLevel"]])

slots.keywords = Slot(uri=DCAT.keyword, name="keywords", curie=DCAT.curie('keyword'),
                   model_uri=BER_REGISTRY.keywords, domain=None, range=Optional[Union[str, list[str]]])

slots.project_affiliation = Slot(uri=BER_REGISTRY.project_affiliation, name="project_affiliation", curie=BER_REGISTRY.curie('project_affiliation'),
                   model_uri=BER_REGISTRY.project_affiliation, domain=None, range=Optional[Union[str, list[str]]])

slots.license = Slot(uri=DCTERMS.license, name="license", curie=DCTERMS.curie('license'),
                   model_uri=BER_REGISTRY.license, domain=None, range=Optional[str])

slots.domain = Slot(uri=DCAT.theme, name="domain", curie=DCAT.curie('theme'),
                   model_uri=BER_REGISTRY.domain, domain=None, range=Optional[Union[str, list[str]]])

slots.version = Slot(uri=PAV.version, name="version", curie=PAV.curie('version'),
                   model_uri=BER_REGISTRY.version, domain=None, range=Optional[str])

slots.doi = Slot(uri=BER_REGISTRY.doi, name="doi", curie=BER_REGISTRY.curie('doi'),
                   model_uri=BER_REGISTRY.doi, domain=None, range=Optional[str])

slots.facility = Slot(uri=BER_REGISTRY.facility, name="facility", curie=BER_REGISTRY.curie('facility'),
                   model_uri=BER_REGISTRY.facility, domain=None, range=Optional[str])

slots.format = Slot(uri=DCTERMS.format, name="format", curie=DCTERMS.curie('format'),
                   model_uri=BER_REGISTRY.format, domain=None, range=Optional[Union[str, list[str]]])

slots.deprecation_date = Slot(uri=BER_REGISTRY.deprecation_date, name="deprecation_date", curie=BER_REGISTRY.curie('deprecation_date'),
                   model_uri=BER_REGISTRY.deprecation_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.deprecation_reason = Slot(uri=BER_REGISTRY.deprecation_reason, name="deprecation_reason", curie=BER_REGISTRY.curie('deprecation_reason'),
                   model_uri=BER_REGISTRY.deprecation_reason, domain=None, range=Optional[str])

slots.replaced_by = Slot(uri=BER_REGISTRY.replaced_by, name="replaced_by", curie=BER_REGISTRY.curie('replaced_by'),
                   model_uri=BER_REGISTRY.replaced_by, domain=None, range=Optional[Union[str, DataSourceId]])

slots.previous_version = Slot(uri=BER_REGISTRY.previous_version, name="previous_version", curie=BER_REGISTRY.curie('previous_version'),
                   model_uri=BER_REGISTRY.previous_version, domain=None, range=Optional[Union[str, DataSourceId]])

slots.temporal_coverage_start = Slot(uri=BER_REGISTRY.temporal_coverage_start, name="temporal_coverage_start", curie=BER_REGISTRY.curie('temporal_coverage_start'),
                   model_uri=BER_REGISTRY.temporal_coverage_start, domain=None, range=Optional[Union[str, XSDDate]])

slots.temporal_coverage_end = Slot(uri=BER_REGISTRY.temporal_coverage_end, name="temporal_coverage_end", curie=BER_REGISTRY.curie('temporal_coverage_end'),
                   model_uri=BER_REGISTRY.temporal_coverage_end, domain=None, range=Optional[Union[str, XSDDate]])

slots.spatial_coverage = Slot(uri=BER_REGISTRY.spatial_coverage, name="spatial_coverage", curie=BER_REGISTRY.curie('spatial_coverage'),
                   model_uri=BER_REGISTRY.spatial_coverage, domain=None, range=Optional[str])

slots.data_quality_notes = Slot(uri=BER_REGISTRY.data_quality_notes, name="data_quality_notes", curie=BER_REGISTRY.curie('data_quality_notes'),
                   model_uri=BER_REGISTRY.data_quality_notes, domain=None, range=Optional[str])

slots.lineage = Slot(uri=PROV.wasDerivedFrom, name="lineage", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=BER_REGISTRY.lineage, domain=None, range=Optional[str])

slots.documentation_url = Slot(uri=BER_REGISTRY.documentation_url, name="documentation_url", curie=BER_REGISTRY.curie('documentation_url'),
                   model_uri=BER_REGISTRY.documentation_url, domain=None, range=Optional[Union[str, URI]])

slots.instrument = Slot(uri=BER_REGISTRY.instrument, name="instrument", curie=BER_REGISTRY.curie('instrument'),
                   model_uri=BER_REGISTRY.instrument, domain=None, range=Optional[str])

slots.modality = Slot(uri=BER_REGISTRY.modality, name="modality", curie=BER_REGISTRY.curie('modality'),
                   model_uri=BER_REGISTRY.modality, domain=None, range=Optional[str])

slots.size_bytes = Slot(uri=BER_REGISTRY.size_bytes, name="size_bytes", curie=BER_REGISTRY.curie('size_bytes'),
                   model_uri=BER_REGISTRY.size_bytes, domain=None, range=Optional[int])

slots.row_count = Slot(uri=BER_REGISTRY.row_count, name="row_count", curie=BER_REGISTRY.curie('row_count'),
                   model_uri=BER_REGISTRY.row_count, domain=None, range=Optional[int])

slots.table_count = Slot(uri=BER_REGISTRY.table_count, name="table_count", curie=BER_REGISTRY.curie('table_count'),
                   model_uri=BER_REGISTRY.table_count, domain=None, range=Optional[int])

slots.source_type = Slot(uri=BER_REGISTRY.source_type, name="source_type", curie=BER_REGISTRY.curie('source_type'),
                   model_uri=BER_REGISTRY.source_type, domain=None, range=Optional[Union[str, "SourceType"]])

slots.database_engine = Slot(uri=BER_REGISTRY.database_engine, name="database_engine", curie=BER_REGISTRY.curie('database_engine'),
                   model_uri=BER_REGISTRY.database_engine, domain=None, range=Optional[Union[str, "DatabaseEngine"]])

slots.category = Slot(uri=BER_REGISTRY.category, name="category", curie=BER_REGISTRY.curie('category'),
                   model_uri=BER_REGISTRY.category, domain=None, range=Optional[Union[str, "DataSourceCategory"]])

slots.lakehouses = Slot(uri=BER_REGISTRY.lakehouses, name="lakehouses", curie=BER_REGISTRY.curie('lakehouses'),
                   model_uri=BER_REGISTRY.lakehouses, domain=None, range=Optional[Union[dict[Union[str, LakehouseId], Union[dict, Lakehouse]], list[Union[dict, Lakehouse]]]])

slots.catalog_entries = Slot(uri=BER_REGISTRY.catalog_entries, name="catalog_entries", curie=BER_REGISTRY.curie('catalog_entries'),
                   model_uri=BER_REGISTRY.catalog_entries, domain=None, range=Optional[Union[dict[Union[str, DataSourceId], Union[dict, DataSource]], list[Union[dict, DataSource]]]])

slots.contact_name = Slot(uri=VCARD.fn, name="contact_name", curie=VCARD.curie('fn'),
                   model_uri=BER_REGISTRY.contact_name, domain=None, range=str)

slots.contact_email = Slot(uri=VCARD.hasEmail, name="contact_email", curie=VCARD.curie('hasEmail'),
                   model_uri=BER_REGISTRY.contact_email, domain=None, range=str)

slots.DataSource_description = Slot(uri=DCTERMS.description, name="DataSource_description", curie=DCTERMS.curie('description'),
                   model_uri=BER_REGISTRY.DataSource_description, domain=DataSource, range=str)

slots.DataSource_created_date = Slot(uri=DCTERMS.created, name="DataSource_created_date", curie=DCTERMS.curie('created'),
                   model_uri=BER_REGISTRY.DataSource_created_date, domain=DataSource, range=Union[str, XSDDate])

slots.DataSource_owner = Slot(uri=DCTERMS.publisher, name="DataSource_owner", curie=DCTERMS.curie('publisher'),
                   model_uri=BER_REGISTRY.DataSource_owner, domain=DataSource, range=str)

slots.DataSource_contact_point = Slot(uri=DCAT.contactPoint, name="DataSource_contact_point", curie=DCAT.curie('contactPoint'),
                   model_uri=BER_REGISTRY.DataSource_contact_point, domain=DataSource, range=Union[dict, "ContactPoint"])

slots.DataSource_namespace = Slot(uri=BER_REGISTRY.namespace, name="DataSource_namespace", curie=BER_REGISTRY.curie('namespace'),
                   model_uri=BER_REGISTRY.DataSource_namespace, domain=DataSource, range=str)

slots.DataSource_status = Slot(uri=DCAT.status, name="DataSource_status", curie=DCAT.curie('status'),
                   model_uri=BER_REGISTRY.DataSource_status, domain=DataSource, range=Union[str, "DataSourceStatus"])

slots.DataSource_is_deprecated = Slot(uri=BER_REGISTRY.is_deprecated, name="DataSource_is_deprecated", curie=BER_REGISTRY.curie('is_deprecated'),
                   model_uri=BER_REGISTRY.DataSource_is_deprecated, domain=DataSource, range=Union[bool, Bool])

slots.DataSource_update_schedule = Slot(uri=DCTERMS.accrualPeriodicity, name="DataSource_update_schedule", curie=DCTERMS.curie('accrualPeriodicity'),
                   model_uri=BER_REGISTRY.DataSource_update_schedule, domain=DataSource, range=Union[str, "UpdateFrequency"])

slots.DataSource_access_level = Slot(uri=BER_REGISTRY.access_level, name="DataSource_access_level", curie=BER_REGISTRY.curie('access_level'),
                   model_uri=BER_REGISTRY.DataSource_access_level, domain=DataSource, range=Union[str, "AccessLevel"])
