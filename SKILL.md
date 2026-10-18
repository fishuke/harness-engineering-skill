---
name: harness-engineering
description: Apply harness engineering, the agent-first way of working from OpenAI's "Harness engineering" article, to any codebase. Use this whenever the user wants to make a repo "agent-ready" or "agent-friendly", set up or slim down AGENTS.md / CLAUDE.md, add a docs system that agents can navigate (ARCHITECTURE.md, design docs, exec plans, tech-debt tracker), enforce architecture boundaries with linters or structural tests, give agents access to a running app, logs, metrics and browser automation, set up recurring cleanup or doc-maintenance tasks, or asks "why does the agent keep failing at this" / "how should we work with Codex or Claude Code at scale". Also use it when the user mentions harness engineering, agent legibility, progressive disclosure for agents, golden principles, or a million-line agent-generated codebase, even if they do not ask for a "skill" or a "setup".
---

# Harness Engineering

Harness engineering is a way of working where humans steer and agents execute. The engineer's job
shifts from writing code to designing the environment the agent works in: the repository layout, the
documentation, the tools, the constraints and the feedback loops. The scarce resource is human
attention, so the environment has to make agent work reliable, observable, testable and
maintainable.

This skill distils the method from Ryan Lopopolo's OpenAI article "Harness engineering: leveraging
Codex in an agent-first world" (February 2026, https://openai.com/index/harness-engineering/) into a
workflow you can apply to a real repo. It is not an OpenAI product.

## The one rule that drives everything

**When an agent fails, fix the environment, not the prompt.** Ask "what capability, tool,
abstraction, document or constraint is missing?" and then have the agent build that missing piece.
Re-prompting hides the gap; filling it pays off on every future task.

Everything below is an application of that rule to a specific part of the environment.

## Workflow

Work depth-first and in small increments. Do not try to install the whole method in one go. Pick the
gap that is blocking the agent right now, close it, then move on.

### 1. Audit the repo

Run the audit before changing anything, so you know which gaps exist and can report progress later:

```bash
python3 scripts/harness_audit.py /path/to/repo
```

It checks the mechanical parts of the checklist (entry-point file length, docs map, CI, linters,
enforcement tests, exec plans, tech-debt tracker) and prints a gap list. Read
`references/checklist.md` for the full checklist including the parts that need judgment.

Share the gap list with the user and agree which gaps matter for their risk level before scaffolding.
A solo side project and a payments service need very different amounts of harness.

### 2. Make the repository the system of record

Knowledge that lives in chat threads, docs tools or people's heads is invisible to the agent. Bring
domain knowledge, decisions, norms and plans into versioned files next to the code.

- Keep `AGENTS.md` (or `CLAUDE.md`) **short**: a map, not a manual. One screen. It names the
  authoritative documents and says when to read each. A giant instruction file burns context,
  blurs priorities, goes stale and cannot be validated.
- Use **progressive disclosure**: small entry point, clear paths to deeper sources of truth.
- Keep `ARCHITECTURE.md` as the one place that explains layers, dependency direction and where
  things go.
- Record design decisions, product specs, execution plans (active and completed) and a tech-debt
  tracker under `docs/`. Keep generated references separate from hand-written ones.

Templates for all of these are in `assets/`. The target layout and what each file is for are in
`references/repo-layout.md`. Adapt names to the repo's conventions; the shape matters, not the
exact filenames.

### 3. Make the running application legible to the agent

Human QA becomes the bottleneck once agents produce code faster than people can click through it.
Give the agent the same evidence an engineer uses to debug:

- A way to run an isolated instance of the app per worktree or branch.
- Browser automation (DevTools protocol, Playwright, or the Claude in Chrome tools) with DOM
  snapshots, screenshots and navigation.
- Logs, metrics and traces the agent can query, ideally scoped to its own instance.
- A documented command for each of these in the docs map so the agent discovers them.

This turns outcome-level asks ("keep p95 latency under 300ms on checkout") into tasks an agent can
actually verify. Read `references/legibility.md` for concrete setups by stack.

### 4. Enforce boundaries mechanically

Documentation does not keep an agent-generated codebase coherent. Agents reproduce the patterns
they see, good and bad, so invariants must be enforced by tools:

- Validate data shapes at system boundaries.
- Split domains into predictable layers and enforce dependency direction with a structural test
  or custom lint rule.
- Route cross-cutting concerns (auth, logging, config, feature flags) through explicit interfaces.
- Check naming, schema and type practices, file-size limits and reliability requirements.
- Write every lint or test failure so that it tells the agent **how to fix it**. An error message is
  a prompt the agent will read thousands of times.

Constrain outcomes and boundaries, not every implementation choice. `references/enforcement.md`
has patterns and example rules for common stacks.

### 5. Close the loop on review and quality

- Set up an iterative PR workflow where agents review, respond to feedback and iterate until a
  reviewer is satisfied. Feed review comments back into docs, lint rules or tooling so the same
  comment is never needed twice.
- Codify "golden principles" (centralise shared utilities, validate at boundaries, no duplicated
  config) as mechanical rules.
- Run recurring background tasks that scan for drift, update a quality score, open small focused
  refactoring PRs and detect stale docs. Treat this like garbage collection: continuous, small,
  boring. `assets/docs/QUALITY_SCORE.md` and `references/maintenance.md` show how.

### 6. Tune autonomy and merge policy to risk

Short-lived PRs and few blocking gates work when correction is cheap and fast. They are
irresponsible when mistakes are expensive or slow to undo. Write down, in the repo, when the agent
may merge on its own and when it must escalate to a human. Increase autonomy only as the tests,
tools and recovery mechanisms earn it.

## What humans keep

Prioritising work, interpreting user feedback, defining acceptance criteria, validating outcomes
and making high-consequence calls. Everything else, including the harness itself, is fair game for
the agent to build.

## Output when applying this skill

When you set up or improve a harness, end with:

1. The audit result before and after (gap list from `harness_audit.py`).
2. The files you added or changed and one line each on why.
3. The open gaps you deliberately left, with the reason (usually risk level or missing infra).
4. The next smallest gap worth closing.

Keep the entry-point file under about 60 lines when you are done. If it grew, you moved a manual
into the map; push the detail back out into `docs/`.
