"""Public API for bdd-tablex."""

from .checker import (
    FeatureDiagnostic,
    FeatureTable,
    check_feature,
    discover_feature_tables,
)
from .context import CellContext, DefaultContext, ParseContext
from .dsl import CellDSL, CellDSLChain, compose_cell_dsls
from .errors import (
    BDDTableError,
    BDDTableErrorCode,
    BDDTableErrors,
    SchemaDefinitionError,
)
from .fields import (
    Field,
    ReferenceSpec,
    discriminator,
    discriminator_field,
    field,
    id_field,
    reference,
)
from .group_expansion import (
    AlphabeticRange,
    ColumnGroupExpander,
    NumericRange,
    PrefixRepeat,
    RangeRule,
    RepeatRule,
    SuffixRepeat,
)
from .introspection import FieldContract, TableContract, VariantContract
from .parsers import (
    boolean,
    choice,
    compose,
    decimal,
    each,
    floating,
    integer,
    map_value,
    optional,
    split,
    string,
)
from .parsing import parse_table, parse_table_records
from .schema import ColumnTable, RowTable, TableFields
from .sources import RecordSource
from .table import TableCell, TableData
from .transformers import (
    TableTransformer,
    TransformerPipeline,
    compose_transformers,
)

__all__ = [
    "BDDTableError",
    "BDDTableErrorCode",
    "BDDTableErrors",
    "AlphabeticRange",
    "CellDSL",
    "CellDSLChain",
    "CellContext",
    "ColumnTable",
    "ColumnGroupExpander",
    "Field",
    "FeatureDiagnostic",
    "FeatureTable",
    "FieldContract",
    "DefaultContext",
    "ParseContext",
    "NumericRange",
    "PrefixRepeat",
    "RangeRule",
    "RepeatRule",
    "RecordSource",
    "ReferenceSpec",
    "RowTable",
    "TableCell",
    "TableContract",
    "TableData",
    "TableFields",
    "TableTransformer",
    "TransformerPipeline",
    "VariantContract",
    "SchemaDefinitionError",
    "SuffixRepeat",
    "field",
    "boolean",
    "choice",
    "compose",
    "compose_cell_dsls",
    "compose_transformers",
    "decimal",
    "discriminator",
    "discriminator_field",
    "each",
    "floating",
    "id_field",
    "integer",
    "map_value",
    "optional",
    "parse_table",
    "parse_table_records",
    "reference",
    "check_feature",
    "discover_feature_tables",
    "split",
    "string",
]
