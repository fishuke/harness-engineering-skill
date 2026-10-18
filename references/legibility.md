# Making the running application legible to agents

The goal is for the agent to gather the same evidence an engineer would: see the screen, read the
logs, query the metrics. Start with whichever one unblocks the current task.

## Isolated instances

- Give each worktree or branch its own ports, database and cache namespace. A script like
  `scripts/dev-up.sh` that reads the worktree name and derives ports is enough.
- Docker Compose with a project name per worktree (`COMPOSE_PROJECT_NAME=$(basename $PWD)`) is the
  cheapest way to get isolated DBs and services.
- Document the single command in the map: "Run `make dev` to start an isolated instance; it prints
  the URL."

## Browser and UI

- Playwright or the Chrome DevTools Protocol gives DOM snapshots, screenshots and navigation.
  Claude Code can also use the Claude in Chrome tools directly.
- Add a tiny script or test helper that opens the app, logs in with a seeded test user and dumps
  a screenshot plus console errors to a known path. Agents reuse it to record evidence of a bug
  and of its fix.
- Seed data matters. An agent cannot reproduce a bug on an empty database.

## Logs, metrics, traces

- Structured logs (JSON) to a file or a local Loki; metrics to a local Prometheus; traces to a
  local Jaeger or OTLP collector. All of this fits in a compose file.
- Expose query commands, for example `scripts/logs.sh 'level=error'` or a note on the LogQL /
  PromQL endpoints, in the docs map. The agent will not discover port 3100 on its own.
- Scope by instance: tag every log line and metric with the worktree or instance name so a run on
  one branch does not read another's noise.

## Outcome-oriented tasks

Once this exists, phrase tasks by outcome and let the agent verify:
- "Startup time under 2 s; measure with `scripts/startup-bench.sh`."
- "Checkout journey p95 under 300 ms; check with the PromQL in `docs/RELIABILITY.md`."

## Evidence in PRs

Ask agents to attach before/after evidence (screenshot, log excerpt, metric query result) to the PR
description. Reviewers then validate outcomes rather than re-run everything.
