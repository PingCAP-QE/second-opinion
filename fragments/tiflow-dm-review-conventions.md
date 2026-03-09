# TiFlow DM review conventions

Use this when changes touch `dm/`.

- Read in this order when the patch spans multiple layers:
  `dm/config/*` → `dm/worker/*` → affected execution unit (`dm/loader/*`,
  `dm/syncer/*`, `dm/relay/*`) → `dm/master/*` / `dm/openapi/*` if control-plane
  or API behavior changes.
- Treat task config, source config, and OpenAPI/generated types as one contract.
  If a new mode, flag, or enum is added, check validation, defaults, conversion,
  and user-facing API surfaces together.
- Review normal stop, pause/resume, retry, and failover as separate behaviors.
  Do not assume a shortcut that is safe for failover is also safe for manual
  stop or generic error handling.
- For checkpoint or resumability changes, insist on an end-to-end story for
  restart safety: no duplicate downstream effects, no skipped data, and no early
  cleanup of state needed for recovery.
- If generated files change (`dm/openapi/gen.*`, `dm/pb/*`, terror codegen
  outputs), require the source-of-truth file to change in the same patch.
- For `dm/tests/*`, prefer retry loops over sleeps, ensure resource cleanup is
  deterministic, and add new integration cases to `dm/tests/run_group.sh`.
