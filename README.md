# skills-toolchain

L0 vendor tooling — the single home for the lockfile schema, lint gate, vendor
script, and CI workflow templates that every skill package and plugin consumes.

The two skills organizations (`full-aigc-skills`, `full-stack-skills`) ship
their `skills.lock.json` against this toolchain; Codex, ZCode, Kimi, and
WorkBuddy consumers vendor the scripts and workflows verbatim into their own repositories.

## What's here

- `scripts/lint_skills.py` — frontmatter shape, naming, single-line description,
  no host prefix, name == directory. Self-tested.
- `scripts/skill_vendor.py` — `update` (fetch pinned sources, wholesale replace,
  recompute digests) + `check` (in-tree == lockfile == upstream). Self-tested.
- `scripts/skill-template.md` — the canonical Skill body used by every package.
- `workflows/skill-lint.yml` — pull_request + push gate.
- `workflows/skill-sync.yml` — repository_dispatch / schedule / manual → PR.
- `workflows/release-tag.yml` — push to main → immutable tag + GitHub Release → dispatch downstream.
- `docs/lockfile-v1.md` — schema reference and upgrade path.
- `docs/recipes/*.md` — per-host install recipes (Codex, WorkBuddy, custom).
- `skills/toolchain-overview/` — the one Skill exposed by this package itself.

## What is not here

- Any concrete skill body or frontmatter business fields.
- Any plugin execution surface (harness / proxy / CLI / scripts/).
- Any host integration or vendor-specific lockfile (those live with their
  consumer so a single toolchain update does not require N sync PRs).

## Versioning

- `version` in `.claude-plugin/plugin.json` is the canonical release marker.
- Each release bumps the package version and creates one immutable tag and GitHub Release; the
  `release-tag.yml` workflow dispatches `toolchain-updated` events so consumer
  repositories re-pin to the new SHA via their own `skill-sync.yml`.

## How to consume

In a skill package:

```bash
git clone https://github.com/full-stack-skills/skills-toolchain /tmp/toolchain
cp /tmp/toolchain/scripts/lint_skills.py scripts/
cp /tmp/toolchain/workflows/skill-lint.yml .github/workflows/lint.yml
```

In a Codex / ZCode / Kimi / WorkBuddy plugin (also pins the vendor tool):

```bash
cp scripts/lint_skills.py /tmp/   # only the lint gate is unconditional
cp /tmp/toolchain/scripts/skill_vendor.py scripts/vendor/
cp /tmp/toolchain/workflows/skill-check.yml .github/workflows/
cp /tmp/toolchain/workflows/skill-sync.yml .github/workflows/
```

Every copied file is byte-identical to the upstream copy; this is verified by
`tests/test_verbatim_vendor.py` (this repo) and by consumer-side self-tests.

## Gatekeeping

- `skill-lint.yml` runs on every push and PR to enforce frontmatter shape and
  naming in this repository's own `skills/`.
- `scripts/lint_skills.py` is mutation-tested in `tests/test_lint_skills.py`
  (block-scalar descriptions, illegal name shapes, name/directory mismatch
  all fail the gate; restoring them re-passes it).
- `scripts/skill_vendor.py` is mutation-tested in `tests/test_skill_vendor.py`
  (in-tree tampering, upstream movement, missing skill, illegal name,
  deleted managed skill all fail the gate).
