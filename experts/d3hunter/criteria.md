# D3Hunter expert criteria

- rule_id: D3HUNTER-PR-001
  description: |
    Preserve core invariants when modifying versioned metadata, bootstrap rules,
    or state transitions. Do not mutate versioned entries in place; add a new
    versioned path instead and prove retry/failover behavior remains valid.
  tags:
    - risk:correctness
    - component:tidb/txn
  rationale: Invariant drift in versioned state machines causes hard-to-recover correctness bugs.

- rule_id: D3HUNTER-PR-002
  description: |
    Make failure semantics explicit: distinguish retriable from non-retriable
    errors, avoid duplicate logging across framework and caller layers, and
    return cancellation causes (`ctx.Err()` or `context.Cause`) consistently.
  tags:
    - theme:error-handling
    - risk:correctness
    - risk:ops
  rationale: Clear and consistent failure contracts reduce incidents and speed up debugging.

- rule_id: D3HUNTER-PR-003
  description: |
    Validate concurrency and lifecycle ordering: ensure producer/submit loops
    exit before teardown, avoid data-race windows on map/slice mutation, and
    keep shared mutable state local unless broad scope is required.
  tags:
    - risk:concurrency
    - risk:correctness
  rationale: Most high-impact concurrency bugs come from lifecycle ordering and shared state misuse.

- rule_id: D3HUNTER-PR-004
  description: |
    Keep fixes scoped and simple: avoid introducing generic wrappers, global
    helpers, or unrelated behavior changes in bugfix PRs when direct local logic
    is clearer and safer.
  tags:
    - theme:api
    - risk:correctness
  rationale: Extra abstraction in a fix path can hide intent and increase regression risk.

- rule_id: D3HUNTER-PR-005
  description: |
    For new loops, scans, validation passes, or concurrency formulas, require
    explicit performance intent and scale safety (for example, large store/node
    counts) and remove avoidable extra storage/network calls.
  tags:
    - risk:perf
    - risk:correctness
    - component:tidb/execution
  rationale: Small structural overheads can amplify into cluster-level performance regressions.

- rule_id: D3HUNTER-PR-006
  description: |
    Ensure API and naming clarity: names must reflect side effects (not only
    checks), terminology should be domain-specific, and exported surface area
    should remain minimal when local visibility is sufficient.
  tags:
    - theme:api
    - risk:correctness
  rationale: Ambiguous naming and over-exporting create misuse risk and maintenance cost.

- rule_id: D3HUNTER-PR-007
  description: |
    Require tests for behavior deltas and risk-bearing paths: include negative
    and edge cases, prefer deterministic checks over sleeps/random timing, and
    split mixed scenarios into focused cases when they assert different kernels.
  tags:
    - theme:testing
    - risk:correctness
  rationale: Focused deterministic tests turn review concerns into durable guarantees.
