# Dispatch troubleshooting

Load this reference when a source release did not produce a downstream PR.

1. Confirm the source workflow emitted a `repository_dispatch` request for the
   expected owner/repository and payload SHA.
2. Treat HTTP 403 as a credential-access failure, not as a downstream code
   failure.
3. Confirm the target workflow listens for the exact event type.
4. Inspect the target run before retrying; avoid duplicate dispatch loops.
5. If the sync branch exists, fetch it before `--force-with-lease`.
6. If PR creation is forbidden, document whether the repository Actions
   setting or the selected token is responsible.
