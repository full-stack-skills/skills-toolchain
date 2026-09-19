# Consumer onboarding reference

Read this file before introducing `skills.lock.json` to a new plugin.

## Preconditions

- The source skill package has an immutable release tag.
- The consumer distinguishes externally managed skills from plugin-specific
  skills.
- The repository already has a CI workflow and a reviewed secret policy.

## Lock construction

For each source, record the HTTPS repository, immutable tag, peeled commit SHA,
destination directory, exact skill names, and deterministic per-skill hashes.
Run `skill_vendor.py update`; do not invent SHA or digest values manually.

## CI gates

Run the vendor check on pull requests and main. Keep an offline check for
installed-snapshot integrity and an online check for upstream identity. A
source release should dispatch an upgrade workflow, but merges remain gated by
the repository's normal tests.

## Ownership rule

Managed skill bodies belong to the source skill repository. Consumer-only
skills belong to the plugin and must not enter the lock. Record this boundary
in the plugin README and contributor instructions.
