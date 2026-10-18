# Architecture

## Layers and dependency direction

```
ui / api  →  services  →  domain  →  infrastructure adapters
```
Arrows show allowed imports. Nothing imports upward. Enforced by `<structural test path>`.

## Where things go
| Thing | Location |
|---|---|
| HTTP handlers | `src/api/` |
| Business logic | `src/services/` |
| Domain models and validation | `src/domain/` |
| DB, queues, external APIs | `src/infra/` |
| Shared utilities | `src/lib/` (only place for helpers) |

## Golden principles
1. Validate data at every boundary; never guess at a shape.
2. One implementation of each shared utility, in `src/lib/`.
3. Cross-cutting concerns (config, logging, HTTP, auth) go through their interface in `src/infra/`.
4. Files stay under 400 lines; split by responsibility.
5. Every public function on a service has a test.

## Key decisions
See `docs/design-docs/`. Add a dated file there for any decision that would surprise a newcomer.
