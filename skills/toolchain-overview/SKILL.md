---
name: toolchain-overview
description: Use when onboarding or diagnosing a Full Stack Skills or AIGC Skills package/plugin that vendors Agent Skills: choose the correct lint, lockfile, vendor, synchronization, and immutable-release workflow; validate local snapshots and CI; or investigate digest drift, stale refs, failed repository_dispatch, and host-prefixed skill names across Codex, ZCode, Kimi, or WorkBuddy.
license: Apache-2.0
---

# Skills Toolchain Overview

Use this skill to connect a skill package or a multi-host plugin to the shared
skill supply-chain contracts. The toolchain governs source identity, vendored
content, validation, synchronization, and releases; it does not define a
plugin's business behavior.

## When to use

- A package needs `SKILL.md` frontmatter and naming gates.
- A plugin needs to vendor external skills through `skills.lock.json`.
- `skill_vendor.py check` reports a digest, source ref, or upstream mismatch.
- A new skill release should dispatch an upgrade PR to downstream plugins.
- A workflow must work consistently for Codex, ZCode, Kimi, and WorkBuddy.
- A public skill or plugin name still carries an obsolete host prefix.

## When not to use

- Do not use this skill to author domain instructions inside a concrete skill;
  use the ecosystem's skill-authoring guidance and TRACE evaluation instead.
- Do not use it to implement plugin runtime logic, MCP tools, authentication,
  or provider APIs.
- Do not treat a successful Git push as proof of a tag, GitHub Release, fresh
  installation, or host-runtime loading.
- Do not edit a vendored managed skill directly. Change its source package,
  release it, then update the lock.

## Source-of-truth map

| Artifact | Contract | Typical consumer |
|---|---|---|
| `scripts/lint_skills.py` | Frontmatter, kebab-case, directory/name equality, no host prefix | Skill packages and plugins |
| `scripts/skill_vendor.py` | Fetch, replace, hash, lock, and verify managed skills | Plugins and vendoring repos |
| `scripts/skill-template.md` | Minimum reusable skill body | Skill authors |
| `workflows/skill-lint.yml` | Run lint on pushes and pull requests | Skill packages |
| `workflows/skill-check.yml` | Check lock, tree, and upstream identity | Plugins |
| `workflows/skill-sync.yml` | Dispatch/schedule/manual update into a PR | Plugins |
| `workflows/release-tag.yml` | Immutable tag, GitHub Release, downstream dispatch | Skill packages |
| `docs/lockfile-v1.md` | Lockfile schema and digest semantics | Maintainers |
| `docs/CONSUMERS.md` | Reviewed downstream repository identities | Release workflow |

The current verified plugin copy is
`stitch-design-plugin/scripts/vendor/skill_vendor.py`. Treat this package's
`scripts/` and `workflows/` directories as canonical for new integrations.

## Workflow

### Step 1: Discover the repository state

1. Confirm the target repository and run `git status --short`.
2. Check for `openspec/`, existing changes, and repository instructions.
3. Determine whether the repository publishes source skills or consumes a
   vendored snapshot. A repository may do both, but each directory needs one
   clear owner.
4. Inventory `skills.lock.json`, `skills/`, vendor scripts, and workflows.
5. Record excluded or dirty files before changing anything.

### Step 2: Select the integration

For a source skill package, copy and wire the lint gate:

```bash
cp /tmp/skills-toolchain/scripts/lint_skills.py scripts/
cp /tmp/skills-toolchain/workflows/skill-lint.yml .github/workflows/
python3 scripts/lint_skills.py
```

For a plugin that vendors external skills, copy the vendor tool and both
consumer workflows:

```bash
mkdir -p scripts/vendor .github/workflows
cp /tmp/skills-toolchain/scripts/skill_vendor.py scripts/vendor/
cp /tmp/skills-toolchain/workflows/skill-check.yml .github/workflows/
cp /tmp/skills-toolchain/workflows/skill-sync.yml .github/workflows/
python3 scripts/vendor/skill_vendor.py check --offline
```

Before creating a new lock, read `references/consumer-onboarding.md`. Use
`examples/skills.lock.example.json` as a shape example, never as a source of
real SHAs or hashes.

### Step 3: Update managed skills

1. Publish an immutable source tag first.
2. Put that tag in `sources[].ref`; do not use `main` for a released snapshot.
3. Run `update` to resolve the tag, replace managed directories, and recompute
   hashes.
4. Run online and offline checks:

```bash
python3 scripts/vendor/skill_vendor.py update
python3 scripts/vendor/skill_vendor.py check
python3 scripts/vendor/skill_vendor.py check --offline
```

5. Review `git diff -- skills.lock.json skills/` and verify that unmanaged,
   plugin-specific skills were not added to the lock or overwritten.

### Step 4: Wire automatic upgrades

The source release sends `repository_dispatch` with the package identity,
tag/version, and commit SHA. The consumer sync workflow resolves that payload,
updates the lock, verifies the snapshot, pushes `chore/skills-sync`, and opens
a pull request.

Required safeguards:

- Fetch the remote sync branch before `--force-with-lease`.
- Do not require a label that may not exist.
- Give the credential access only to intended downstream repositories.
- If repository Actions cannot create pull requests, use a scoped
  `SKILLS_SYNC_TOKEN`; do not silently widen permissions.
- A dispatch success is not enough: verify the target run and resulting PR.

When dispatch or PR automation fails, read
`references/operations/dispatch-troubleshooting.md`. When selecting or
rotating a token, read `references/security/token-boundaries.md` first.

### Step 5: Release without moving tags

1. Bump the package version before changing published content.
2. Create an annotated `v<version>` tag only if it does not exist.
3. If the tag exists at another commit, fail and bump the version; never force
   update a published tag.
4. Create or verify the GitHub Release for the same tag.
5. Verify tag and Release target the expected commit before dispatching.

## Security and permissions

Follow least privilege（最小权限）for every token. The toolchain does not need
provider API keys, must not log credentials, and must not broaden repository
access just to make automation green. Prefer a repository-scoped token with
only content, pull-request, and dispatch permissions required by the selected
consumer workflow.

## Validation checklist

- [ ] `python3 scripts/lint_skills.py` returns zero errors.
- [ ] Every managed skill exists in the source package and local snapshot.
- [ ] Online `check` proves remote ref, locked SHA, upstream digest, and tree.
- [ ] Offline `check` proves the installed snapshot without network access.
- [ ] TRACE is rerun for every changed source skill.
- [ ] No installable skill directory begins with `codex-`, `zcode-`, `kimi-`,
      or another host-only prefix unless the skill truly targets only that host.
- [ ] Source tag is immutable and a GitHub Release exists.
- [ ] Downstream dispatch produced a target workflow run or an explicit,
      documented credential blocker.
- [ ] Fresh Codex, ZCode, and Kimi environments can discover the intended
      skills; static manifests alone are not runtime evidence.

## Failure handling

| Symptom | Likely cause | Action |
|---|---|---|
| Local digest mismatch | Managed file edited in consumer | Revert the direct edit or publish it upstream, then run `update` |
| Ref resolves to another SHA | Tag moved or branch was used | Stop; publish a new immutable version and update the lock |
| Upstream digest mismatch | History or tag content changed | Treat as supply-chain failure; do not regenerate hashes blindly |
| `repository_dispatch` returns 403 | Token lacks target-repo access | Fix scoped repository access; do not use a broader token by default |
| `--force-with-lease` rejects | Remote sync branch was not fetched | Fetch the branch before rebuilding it |
| PR creation fails on label | Label is absent | Remove the hard label dependency or provision it explicitly |
| PR creation is forbidden | Actions setting or token cannot create PRs | Use reviewed `SKILLS_SYNC_TOKEN` access or enable the repo setting |
| Skill is undiscoverable | Name/description/path not valid for host | Recheck frontmatter, directory identity, and fresh installation |

## Gotchas

- `update` performs wholesale replacement; it is not a three-way merge.
- A granular skill install may omit sibling skills, so cross-skill references
  must use skill names and install commands, not `../sibling/SKILL.md` paths.
- A tag name and a Release title do not prove the commit. Verify the peeled tag
  SHA and Release tag.
- Codex build metadata such as `+codex.<date>` is a manifest detail, not a
  license to give a cross-host skill a `codex-` public identity.
- The lock protects only declared managed skills. Plugin-specific skills must
  remain outside `skills.lock.json` by design.

## Completion report

Report these evidence levels separately:

```text
Source: repo, tag, peeled commit, GitHub Release
Lock: package, ref, SHA, per-skill digest count
Checks: lint, online vendor check, offline vendor check, TRACE
Automation: dispatch result, target run, PR and merge status
Runtime: fresh Codex/ZCode/Kimi install, discovery, trigger samples
Excluded or blocked: dirty paths, protected branch, credential boundary
```

See the additional report examples in `examples/online-check-failure.txt`,
`examples/dispatch-blocker-report.txt`, and
`examples/release-verification-report.txt` when those exact situations occur.
