# skills.lock.json — Vendor Lockfile Schema v1

The single source of truth for which skills are vendored into a repository, from
which source repository, at which ref / sha, with which digest per skill.

## Schema

```json
{
  "version": 1,
  "sources": [
    {
      "package": "processon-skills",
      "repo": "https://github.com/full-stack-skills/processon-skills.git",
      "ref": "v1.0.0",
      "sha": "<40-hex commit>",
      "skills": ["processon-use", "processon-diagram", "..."],
      "dest": "skills/",
      "sha256": {
        "processon-use": "<64-hex sha256 of the skill dir>",
        "processon-diagram": "<64-hex sha256>"
      }
    }
  ]
}
```

| Field | Type | Meaning |
|---|---|---|
| `version` | integer (currently 1) | Schema version; bump on breaking changes |
| `sources[].package` | string | Display name of the source skill package |
| `sources[].repo` | URL | Git remote (https); resolved by `git ls-remote` |
| `sources[].ref` | string | Tag or branch name; resolved to a commit sha at `update` time |
| `sources[].sha` | hex | Resolved commit sha; written by `update`, validated by `check` |
| `sources[].skills[]` | list of strings | Skill directory names to vendor (must exist at `skills/<name>/SKILL.md` in source) |
| `sources[].dest` | path | Destination directory inside the consumer repo (default `skills/`) |
| `sources[].sha256[name]` | hex | Per-skill digest computed by `update`; validated against the tree |

## Digest definition

The per-skill sha256 is computed deterministically over the skill directory:

```text
digest = sha256( concat for each file f sorted by posix path:
                   path(f)
                   "\0"
                   sha256(bytes(f))
                   "\n" )
```

This means:
- Whitespace/line-ending changes inside files change the digest.
- File additions, deletions, or renames change the digest.
- File metadata (mode, mtime) does not change the digest.

## Semantics

- `update` resolves `ref` → `sha`, fetches the source at `sha`, **wholesale
  replaces** each listed skill directory under `dest`, recomputes the digest,
  and writes the lockfile back. There is no three-way merge.
- `check` verifies:
  1. The on-tree skill digests match `sha256[name]` for every managed skill.
  2. Unless `--offline`, every `ref` still resolves to the locked `sha`.
  3. Unless `--offline`, every upstream skill body still matches the locked
     digest (defense against upstream history rewrite without ref advance).
- `--source-path PKG=PATH` overrides a source's repo with a local checkout for
  dev and offline environments.

## Upgrade path

- A new schema version (`"version": 2`) is a breaking change: existing
  consumers must run `update` once to migrate.
- A new field is additive: consumers on older `skill_vendor.py` ignore unknown
  fields and behave identically.
- A renamed field or removed field is breaking; bump `version`.

## Why no third-party lock file formats

Cargo, npm, poetry, pipenv all converge on the same shape: source → resolved
versions → content hash. We follow that shape, dropping only what we don't use
(workspace inheritance, virtual envs, source replacements) and keeping what we
do use (per-package sha, per-file digests, deterministic re-resolution).
