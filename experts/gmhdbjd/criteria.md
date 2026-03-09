# gmhdbjd expert criteria

- rule_id: GMHDBJD-DM-001
  description: |
    Treat `dm/config/*` and user-facing task/source/route/filter/load/sync
    settings as compatibility-sensitive. Verify defaults, validation,
    downgrade paths, and alternate config surfaces (task YAML/TOML,
    OpenAPI/generated types, and converters) stay aligned so one logical
    setting does not behave differently by entrypoint.
  tags:
    - component:tiflow/dm-config
    - component:tiflow/dm-openapi
    - risk:compat
    - risk:correctness
    - theme:api
  rationale: Config drift is one of the fastest ways to create silent behavior differences and hard-to-debug regressions.

- rule_id: GMHDBJD-DM-002
  description: |
    For `dm/worker/*`, `dm/unit/*`, or load/sync handoff changes, validate
    lifecycle ordering explicitly: start, pause, resume, close, kill, retry,
    and failover must remain idempotent, wait-group ownership must be clear,
    and cancel causes must not accidentally apply failover-only cleanup rules
    to ordinary stop or generic error paths.
  tags:
    - component:tiflow/dm-worker
    - component:tiflow/dm-loader
    - component:tiflow/dm-syncer
    - risk:concurrency
    - risk:correctness
    - theme:error-handling
  rationale: DM incidents cluster around lifecycle ordering mistakes and cancellation-contract drift rather than the steady-state happy path.

- rule_id: GMHDBJD-DM-003
  description: |
    For checkpoint, relay position, GTID, or resumability logic, reason about
    crash/retry/failover behavior end-to-end: no skipped events, no duplicate
    downstream effects, and no checkpoint cleanup before downstream durability
    is guaranteed. If retryable vs non-retryable classification changes,
    require concrete proof that the new bucket is safe.
  tags:
    - component:tiflow/dm-loader
    - component:tiflow/dm-syncer
    - component:tiflow/dm-relay
    - risk:correctness
    - risk:compat
    - scenario:rollback
  rationale: Incorrect recovery logic usually appears only after interruption and can cause data loss or duplication.

- rule_id: GMHDBJD-DM-004
  description: |
    For full-load or unit-boundary changes (`dump` → `load` → `sync`), verify
    ownership and handoff invariants explicitly: reject unsupported topologies
    early, keep duplicate/conflict handling aligned with documented behavior,
    and ensure cleanup/resume paths remain correct across logical, physical,
    and import-into modes.
  tags:
    - component:tiflow/dm-config
    - component:tiflow/dm-loader
    - component:tiflow/dm-worker
    - risk:correctness
    - risk:ops
    - theme:testing
  rationale: DM full-load bugs usually surface at unit boundaries and backend-specific recovery paths rather than the happy path.

- rule_id: GMHDBJD-DM-005
  description: |
    When changes touch `dm/master/*`, scheduling, validator orchestration,
    source config refresh, or worker reassignment, verify control-plane
    ownership and liveness: the right worker still owns the right source/task,
    stale config is not silently applied as fresh state, and missing etcd
    state is handled deliberately.
  tags:
    - component:tiflow/dm-master
    - component:tiflow/dm-worker
    - risk:correctness
    - risk:concurrency
    - risk:ops
  rationale: Small control-plane mistakes can reassign work incorrectly or hide scheduler-state corruption.

- rule_id: GMHDBJD-DM-006
  description: |
    For `dm/syncer/*` or `dm/relay/*` changes, follow the replication contract
    across package boundaries: event ordering, route/filter behavior, sharding
    barrier semantics, online-DDL/schema tracking, GTID/position handling, and
    checkpoint interaction must still agree under retries and DDL transitions.
  tags:
    - component:tiflow/dm-syncer
    - component:tiflow/dm-relay
    - risk:correctness
    - risk:concurrency
  rationale: Replication correctness bugs are usually boundary bugs between event ordering, schema state, and checkpoint updates.

- rule_id: GMHDBJD-DM-007
  description: |
    If a change touches OpenAPI, proto, terror tables, or generated
    clients/servers, require the source-of-truth file to change in the same PR
    and review regenerated outputs together with the semantic delta. Reject
    patches that update generated files alone without the underlying spec or
    table change.
  tags:
    - component:tiflow/dm-openapi
    - component:tiflow/dm-config
    - risk:correctness
    - theme:build
    - theme:api
  rationale: Generated files drift easily and become unreviewable unless the source-of-truth change is visible.

- rule_id: GMHDBJD-DM-008
  description: |
    Require executable, deterministic evidence for DM behavior changes: prefer
    focused unit tests for config translation, ordering/cancel/state-machine
    logic, and targeted `dm/tests/*` integration cases for sharding, relay
    recovery, failover, or resume flows; avoid sleep-heavy assertions and
    ensure external resources are cleaned up deterministically.
  tags:
    - theme:testing
    - risk:correctness
    - risk:ops
    - component:tiflow/dm-worker
    - component:tiflow/dm-loader
    - component:tiflow/dm-master
  rationale: DM bugs often require multi-component evidence, but flaky tests make review signal worse instead of better.
