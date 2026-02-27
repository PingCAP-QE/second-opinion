# JaySon-Huang expert criteria

Abstract, component-level review criteria merged and deduplicated from
JaySon-Huang review practice across pingcap/tiflash, pingcap/tidb,
and pingcap-inc/tici.

- rule_id: JAYSONHUANG-RC-001
  description: |
    For metadata, storage, shard-scheduling, or import/backfill workflow
    changes, start with hotspot scope mapping before deep review (for example:
    `dbms/src/Storages/*` and `dbms/src/TiDB/Schema/*` in TiFlash, and
    `src/meta/*`, `components/tici_shard/*`, `components/tici_import/*`, and
    `src/worker/*` in TiCI).
    For hotspot paths, escalate review depth and verify end-to-end transition
    invariants: allowed states, ordering constraints, ownership of state
    mutation, terminal-state cleanup, rollback safety, and performance side
    effects (for example compaction/GC and IO amplification). If transition
    safety is unclear, treat it as blocking until explicit proof is provided.
  tags:
    - component:tiflash/storage
    - component:tiflash/replica
    - component:tidb/ddl
    - risk:correctness
    - risk:concurrency
    - risk:perf
    - scenario:rollback
  rationale: Hotspot mapping plus transition-invariant checks reduces blind spots on high-blast-radius paths.

- rule_id: JAYSONHUANG-RC-002
  description: |
    For protocol or API contract changes (schema, status code/state semantics,
    required fields), require compatibility proof for mixed-version interaction
    and rollback behavior. New or changed fields must preserve backward
    compatibility expectations unless a migration plan is explicit.
  tags:
    - component:tiflash/storage
    - component:tiflash/compute
    - risk:compat
    - risk:correctness
    - scenario:upgrade
    - scenario:rollback
  rationale: Contract drift can silently break cross-component behavior in production.

- rule_id: JAYSONHUANG-RC-003
  description: |
    For key/index encoding paths, verify invariants for key composition,
    boundary values, null/default handling, and deterministic decode behavior.
    Any encoding/layout change must include explicit checks for old/new data
    compatibility.
  tags:
    - component:tiflash/storage
    - component:tidb/sql-infra
    - risk:correctness
    - risk:compat
    - theme:testing
  rationale: Encoding mistakes frequently cause wrong results that are hard to diagnose.

- rule_id: JAYSONHUANG-RC-004
  description: |
    For import/backfill/write pipelines, validate partial-failure semantics,
    retry idempotency, and persistence ordering. Ensure cleanup paths do not
    leave orphaned state or duplicate side effects after retry/restart.
  tags:
    - component:tiflash/storage
    - component:tidb/ddl
    - risk:correctness
    - risk:concurrency
  rationale: Pipeline failures usually surface as long-tail correctness and operability incidents.

- rule_id: JAYSONHUANG-RC-005
  description: |
    Treat hot paths as cost-sensitive by default. Question avoidable allocations,
    copies, repeated serialization/deserialization, unnecessary IO, and extra
    work inserted into the success path for rare error handling.
  tags:
    - component:tiflash/storage
    - component:tiflash/compute
    - risk:perf
  rationale: Small inefficiencies on high-frequency paths can dominate runtime cost.

- rule_id: JAYSONHUANG-RC-006
  description: |
    Request test evidence in executable form and by explicit risk type. For each
    non-trivial finding, require a concrete test type and scenario (unit,
    integration, or e2e; normal, edge, and failure path as needed) rather than
    generic "add tests".
  tags:
    - theme:testing
    - risk:correctness
    - risk:compat
  rationale: Generic test requests are low signal and do not reliably prevent regressions.

- rule_id: JAYSONHUANG-RC-007
  description: |
    Use severity-based decisions with explicit merge conditions. Block on
    unresolved correctness/concurrency/compatibility risks and state clear
    acceptance criteria for non-blocking follow-ups.
  tags:
    - risk:correctness
    - risk:concurrency
    - risk:compat
    - risk:ops
  rationale: Clear decision rules reduce ambiguity and speed remediation.

- rule_id: JAYSONHUANG-RC-008
  description: |
    Keep feedback code-local and executable: cite file/line anchors, state the
    concrete failure mode, and propose the smallest safe fix direction.
    Prefer targeted why/how questions only when behavior intent is unclear.
  tags:
    - theme:api
    - risk:correctness
  rationale: Actionable, code-anchored comments improve fix quality and turnaround.
