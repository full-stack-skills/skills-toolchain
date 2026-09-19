# Token boundaries

Load this reference before creating, rotating, or widening a synchronization
token.

- Limit repository access to the explicit downstream set.
- Grant only the scopes required to dispatch, push the sync branch, and create
  a pull request.
- Store the value as `SKILLS_SYNC_TOKEN`; never put it in a lockfile, workflow
  payload, test fixture, or command output.
- A source-repository secret is not automatically present in target repos.
- Credential changes require owner approval and separate verification from
  source-code changes.
