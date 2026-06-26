---
icon: lucide/code-xml
---

# Public API

Import normal project APIs from `talika`.

## Errors

- `TableError`
- `TableErrorCode`
- `TableErrors`
- `SchemaDefinitionError`

## Schemas and fields

- `RowTable`
- `ColumnTable`
- `TableFields`
- `Field`
- `ReferenceSpec`
- `field`
- `id_field`
- `discriminator`
- `discriminator_field`
- `reference`

## Parsers

- `string`
- `integer`
- `floating`
- `decimal`
- `boolean`
- `choice`
- `split`
- `map_value`
- `compose`
- `each`
- `optional`

## DSL

- `CellDSL`
- `CellDSLChain`
- `compose_cell_dsls`

## Source and context

- `TableData`
- `TableCell`
- `RecordSource`
- `ParseContext`
- `CellContext`
- `DefaultContext`

## Transformations

- `TableTransformer`
- `TransformerPipeline`
- `compose_transformers`
- `ColumnGroupExpander`
- `NumericRange`
- `AlphabeticRange`
- `PrefixRepeat`
- `SuffixRepeat`
- `RangeRule`
- `RepeatRule`

## Tooling and contracts

- `FieldContract`
- `TableContract`
- `VariantContract`
- `FeatureTable`
- `FeatureDiagnostic`
- `discover_feature_tables`
- `check_feature`
- `parse_table`
- `parse_table_records`
- `__version__`
