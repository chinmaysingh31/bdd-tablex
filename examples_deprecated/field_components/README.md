# Reusable Field Components

`TableFields` groups declarations that appear in several schemas:

```python
class AuditFields(TableFields):
    created_by = field("created_by", required=True)
    trace_id = field("trace_id", required=True)
```

Mix the component in after the concrete table orientation:

```python
class ArticleTable(RowTable, AuditFields):
    headline = field("headline", required=True)
```

Components only contribute fields. They do not parse tables, register hooks,
or hide business behavior. Declarations are cloned for each concrete schema,
so later annotation inference or schema configuration does not mutate another
schema using the same component.
