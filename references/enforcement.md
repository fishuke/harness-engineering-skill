# Enforcing architecture and standards mechanically

Agents copy what they see. If a shortcut exists in the repo, it will be copied until a rule stops
it. Encode the invariants that matter; leave implementation details free.

## What to enforce

| Invariant | How |
|---|---|
| Dependency direction between layers | import-linter (Python), dependency-cruiser (JS/TS), ArchUnit (JVM), NetArchTest (.NET), a custom structural test |
| Data validated at boundaries | lint rule or review check: no raw `request.json` / `any` crossing a module boundary without a schema (zod, pydantic, etc.) |
| Cross-cutting concerns via interfaces | ban direct imports of the logger/config/http client outside the designated module |
| File size limits | lint rule or a 20-line test that fails over N lines |
| Naming conventions | eslint naming rules, ruff `N` rules, a regex test for file names |
| Reliability requirements | tests for timeouts, retries, idempotency on the paths `docs/RELIABILITY.md` names |

## Error messages are prompts

An agent will read the failure text and act on it. Write the fix into the message:

```
Boundary violation: src/api/orders.py imports src/db/models.
API modules must go through src/services. Move the query into
src/services/orders.py and import that instead. See ARCHITECTURE.md#layers.
```

Not:

```
E0401 forbidden import
```

## Pattern: a structural test in any language

Walk the source tree, parse imports (regex is fine), and assert against an allowlist from
`ARCHITECTURE.md`. Keep the allowlist in one place so the doc and the test cannot diverge, for
example by having the test read a fenced block from the doc.

## Pattern: lint errors that teach

Custom rules (eslint plugin, ruff plugin, semgrep rule) with a `message` that names the rule, the
reason and the remediation. Semgrep is the fastest way to add one in most stacks:

```yaml
rules:
  - id: no-direct-db-in-handlers
    pattern: import app.db
    paths: { include: ["app/handlers/**"] }
    message: >
      Handlers must not touch app.db directly. Call a function in app/services
      instead (ARCHITECTURE.md#layers). This keeps DB access testable and swappable.
    severity: ERROR
```

## What not to enforce

Formatting beyond a formatter, variable naming inside a function, which of two equivalent
libraries to use for a one-off. Constrain outcomes and boundaries, not every choice; over-constraint
slows agents and the rules go stale.
