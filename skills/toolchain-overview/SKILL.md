---
name: toolchain-overview
description: Understand the skills-toolchain package: the L0 source of the lockfile schema, lint gate, vendor script, and CI workflow templates used by every skill package and plugin in the full-aigc and full-stack skills ecosystems.
license: Apache-2.0
---

# Skills Toolchain Overview

The single source of truth for how skill packages and plugins vendor, validate,
and synchronize skills.

## What lives here

| Artifact | Purpose | Consumed by |
|---|---|---|
| `scripts/lint_skills.py` | Frontmatter shape, naming, single-line description, no host prefix, name == directory | Skill packages, plugins |
| `scripts/skill_vendor.py` | `update` (fetch + wholesale replace + recompute digests), `check` (tree == lock == upstream) | Plugins, WorkBuddy team repos |
| `scripts/skill-template.md` | Canonical Skill body shape | New skill authors |
| `workflows/skill-lint.yml` | PR + push gate enforcing frontmatter | Skill packages |
| `workflows/skill-check.yml` | PR + push gate enforcing vendor digests + upstream pins | Plugins, vendoring repos |
| `workflows/skill-sync.yml` | `repository_dispatch` + daily schedule + manual → open PR via gh CLI (no third-party actions) | Plugins, vendoring repos |
| `workflows/release-tag.yml` | push to main → force-advance tag → notify downstream | This package only |
| `docs/lockfile-v1.md` | Schema reference and upgrade path | Skill authors, reviewers |
| `docs/CONSUMERS.md` | GitHub `owner/repo` list for `release-tag.yml` dispatch | Maintainers |

## Where to find the canonical scripts (right now)

- The verified copies at the time of writing live in:
  - `processon-skills/scripts/lint_skills.py` (verified 2026-09-15, lint gate 0 errors)
  - `codex-stitch-plugin/scripts/vendor/skill_vendor.py` (verified 2026-09-15,
    6 mutation-tested self-tests)

After this package's first release, replace those local copies by copying from
`scripts/` here.

## How a new skill package gets onboarded

1. Add this package's repo as a git source under `docs/CONSUMERS.md` (or ask a
   maintainer to do so).
2. Copy `scripts/lint_skills.py` and `workflows/skill-lint.yml` into the new
   package as `scripts/lint_skills.py` and `.github/workflows/lint.yml`.
3. Every `skills/<name>/SKILL.md` must lint clean (single-line description,
   name == directory, etc.).
4. The next release of this package will auto-dispatch `toolchain-updated` to
   the new consumer so it can re-pin to the latest toolchain SHA.

## When to call this Skill

- When opening a new skill package or plugin and you want a one-page mental
  model of the toolchain.
- When `lint_skills.py` or `skill_vendor.py` fails and you want to understand
  the schema it expects before debugging.
- When a CI workflow rejects a PR and you want to know which tool is enforcing
  which rule.
