# bdd-tablex Project Explanation

This folder explains `bdd-tablex` from several angles: what problem it solves,
how its internals fit together, how every major feature can be used, and how to
explain its value to another person.

## Best Reading Order

1. [Project Overview](project-overview.md): the problem, product idea, and why
   the project matters.
2. [Concepts and Lifecycle](concepts-and-lifecycle.md): the mental model for
   how a raw BDD table becomes validated Python records or domain objects.
3. [Feature Guide](feature-guide.md): every user-facing capability, from simple
   fields to variants, transformations, diagnostics, and CLI checking.
4. [Detailed Feature Guide](detailed-feature-guide.md): slower, example-heavy
   explanations of every feature, including transformers and pipelines.
5. [Architecture](architecture.md): how the source modules cooperate and why
   the design is intentionally small.
6. [Use Cases and Positioning](use-cases-and-positioning.md): ways to sell,
   demo, and explain the importance of the package.
7. [Examples Map](examples-map.md): what each executable example teaches and
   how to navigate the test suite.
8. [Public API](api.md): concise reference for exported names.

## One-Sentence Summary

`bdd-tablex` gives BDD data tables typed, validated, source-aware schemas so
test setup stays readable while parsing, conversion, diagnostics, and reuse move
out of step-definition glue code.

## The Project In One Picture

```text
Gherkin / pytest-bdd datatable
        |
        v
TableData with source-aware TableCell values
        |
        v
optional table transformation
        |
        v
RowTable or ColumnTable schema parsing
        |
        v
typed schema records with source metadata
        |
        v
references, record validation, table validation
        |
        v
optional project output models
```

The library is intentionally not a business-action framework. It does not
create users, publish articles, or execute payments. It focuses on turning
tables into trustworthy Python objects so the surrounding test or application
code can do the domain work cleanly.
