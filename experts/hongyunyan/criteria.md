# Hongyunyan expert criteria

- rule_id: HONGYUNYAN-RB-001
  description: |
    Refresh and anchor the review baseline before analysis: fetch the latest
    upstream base branch, compare against that base, and remove upstream-drift
    noise before evaluating functional deltas.
  tags:
    - risk:correctness
    - risk:compat
    - theme:build
  rationale: Stale baselines produce false findings and hide true behavior changes.

- rule_id: HONGYUNYAN-RB-002
  description: |
    Do not infer behavior from symbol names alone. Follow definitions and call
    chains until data flow, ownership, and state transitions are explicit.
  tags:
    - risk:correctness
    - theme:api
  rationale: Name-based assumptions are a frequent source of review misses.

- rule_id: HONGYUNYAN-RB-003
  description: |
    For concurrency-sensitive changes, verify lock ordering, goroutine lifecycle,
    channel ownership, and context cancellation paths. Require concrete evidence
    when claiming race/deadlock safety.
  tags:
    - risk:concurrency
    - risk:correctness
    - theme:error-handling
  rationale: Concurrency defects are high-impact and often hidden in edge paths.

- rule_id: HONGYUNYAN-RB-004
  description: |
    Keep the review CI-first: evaluate whether tests cover behavior deltas and
    edge cases, and avoid broad local test runs unless explicitly requested.
  tags:
    - theme:testing
    - risk:ops
  rationale: CI should remain the source of truth while preserving review speed.

- rule_id: HONGYUNYAN-RB-005
  description: |
    On Go hot paths, scan for avoidable allocations/copies, repeated loop
    allocations, string/[]byte conversion churn, and interface-heavy operations
    that can increase escape and GC pressure.
  tags:
    - lang:go
    - risk:perf
    - component:tidb/execution
  rationale: Small hot-path regressions can dominate production cost.

- rule_id: HONGYUNYAN-RB-006
  description: |
    Require a guided reading path in review output: identify where to start,
    why each location matters, and a short "10-minute critical path" for fast
    triage.
  tags:
    - theme:observability
    - risk:ops
  rationale: Good reading order improves review quality and remediation speed.
