# harness-engineering skill

An agent skill (Claude Code, Codex, Cursor, any tool that reads `SKILL.md`) that turns the way of
working described in OpenAI's article [Harness engineering: leveraging Codex in an agent-first
world](https://openai.com/index/harness-engineering/) (Ryan Lopopolo, Feb 2026) into a repeatable
workflow: audit a repo, make it the system of record, make the running app legible to agents,
enforce boundaries mechanically, and keep entropy down with recurring maintenance.

Not affiliated with OpenAI. The article is the source; the skill is an interpretation.

## What is in here

```
SKILL.md                  the workflow (read this first)
references/
  checklist.md            full audit checklist
  repo-layout.md          target docs layout and rules for the map file
  legibility.md           isolated instances, browser automation, logs/metrics/traces
  enforcement.md          structural tests, lint rules whose errors teach
  maintenance.md          recurring GC tasks, golden principles, feeding review back
assets/                   templates: AGENTS.md, ARCHITECTURE.md, docs/* scaffolding
scripts/harness_audit.py  mechanical audit; --strict for CI
```

## Install

Claude Code, for one user:

```bash
git clone https://github.com/fishuke/harness-engineering-skill ~/.claude/skills/harness-engineering
```

Claude Code, for one project: clone into `.claude/skills/harness-engineering` inside the repo.

Codex / other tools: clone anywhere and point the tool at `SKILL.md`, or copy the folder into
the tool's skills directory.

## Use

Ask the agent something like "make this repo agent-ready", "slim down our CLAUDE.md into a map",
"add boundary enforcement between api and db", or "set up a recurring cleanup task". The skill
triggers on those. You can also run the audit by hand:

```bash
python3 scripts/harness_audit.py /path/to/repo
python3 scripts/harness_audit.py --strict /path/to/repo   # non-zero exit on gaps, for CI
```

## The core idea

Humans steer, agents execute, and when an agent fails you fix the environment rather than the
prompt. Everything else in the skill is that rule applied to repo structure, documentation,
tooling, enforcement and maintenance.

## License

MIT
