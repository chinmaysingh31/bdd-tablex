---
icon: lucide/braces
---

# CellDSL

`CellDSL` is a parser object with project-owned dispatch rules.

## Registration

```python
dsl = CellDSL()

@dsl.token("random", fields=("headline",))
def handler(context): ...

@dsl.pattern(r"(?P<count>\d+) words")
def handler(match, context): ...

@dsl.when(predicate)
def handler(value, context): ...

@dsl.fallback
def handler(value, context): ...
```

Field scopes use schema attribute names.

## Dispatch order

1. exact tokens
2. regular-expression full matches
3. predicates
4. fallback

Unmatched values pass through unchanged unless a fallback exists.

## Composition

```python
chain = dsl.compose(other)
chain = compose_cell_dsls(first, second)
```

`CellDSLChain` asks DSLs left-to-right and returns the first match.
