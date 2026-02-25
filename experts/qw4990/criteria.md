# qw4990 expert criteria

TiDB PR review style: planner/bindinfo/statistics focus, question-driven feedback,
consistency checks, and test quality. Derived from 567+ real PR review comments.

- rule_id: QW4990-PR-001
  description: |
    For partial order and index selection, verify skyline pruning, matchPartialOrderProperty,
    and that we skip paths that cannot satisfy partial order (e.g. IsFlashProp).
    Question whether the implementation guarantees partial order when documented.
  tags:
    - component:tidb/planner
    - risk:correctness
  rationale: Partial order bugs cause wrong index choices and subtle plan regressions.

- rule_id: QW4990-PR-002
  description: |
    For join reorder changes, check nulleq handling, leading hints, and resJoinGroup.leadingHints.
    Ensure join-order blocking behavior is documented when non-obvious.
  tags:
    - component:tidb/planner
    - risk:correctness
  rationale: Join reorder is sensitive to NULL-equality and hint semantics.

- rule_id: QW4990-PR-003
  description: |
    Ensure new variables that affect plan selection are included in NewPlanCacheKey.
    When session variables or config affect the chosen plan, they must be part of the cache key.
  tags:
    - component:tidb/planner
    - component:tidb/bindinfo
    - risk:correctness
  rationale: Missing plan cache key entries cause stale or wrong cached plans.

- rule_id: QW4990-PR-004
  description: |
    For binding cache, plan cache key, and SQL bindings changes, verify cache invalidation
    and key consistency. Question additions to deprecated binding paths.
  tags:
    - component:tidb/bindinfo
    - risk:correctness
  rationale: Binding and plan cache bugs are hard to reproduce and debug.

- rule_id: QW4990-PR-005
  description: |
    For statistics, histograms, and cardinality estimation changes, verify edge cases:
    empty tables, extreme values (null, 0, ""), and varied column types (string, decimal,
    not null, default null). Prefer stronger random tests over fixed cases.
  tags:
    - component:tidb/statistics
    - theme:testing
    - risk:correctness
  rationale: Stats bugs cause wrong plans and unpredictable performance.

- rule_id: QW4990-PR-006
  description: |
    Prefer tests that (1) create tables, (2) randomly insert data, (3) generate queries,
    (4) run and verify results—not just fixed cases. Remove useless setup (e.g. analyzing
    an empty table). Enumerate column types and extreme values.
  tags:
    - theme:testing
  rationale: Fixed-case tests miss edge cases; random tests improve coverage.

- rule_id: QW4990-PR-007
  description: |
    Avoid duplication: suggest wrapping repeated logic into a small function. Prefer
    consistent return types and APIs. Prefer simpler logic over complex formulas.
    Prefer column names over column IDs for usability in logs and errors.
  tags:
    - theme:api
  rationale: Duplication and inconsistency increase maintenance cost and bugs.

- rule_id: QW4990-PR-008
  description: |
    Do not extend deprecated features. Question new columns or logic in deprecated
    tables. Skip deprecated paths when they are unused and scheduled for removal.
    Suggest splitting large PRs into refactor + implementation parts.
  tags:
    - risk:compat
  rationale: Extending deprecated code increases tech debt and migration cost.

- rule_id: QW4990-PR-009
  description: |
    Request comments for complex logic, especially when it refers to papers or
    non-obvious algorithms. Ask for concrete examples when abstract concepts
    (e.g. partial order) are hard to understand without a case.
  tags:
    - theme:api
  rationale: Undocumented complex logic is a maintenance and onboarding burden.

- rule_id: QW4990-PR-010
  description: |
    Avoid dangerous patterns: e.g. maps that may not be cleared/deleted (require
    explicit cleanup on deallocate/close). Do not mix test and prod code.
    Question conservative thresholds (e.g. 0.5 or 50% may be too large; consider 10% or 20%).
  tags:
    - risk:correctness
    - risk:concurrency
  rationale: Map leaks and mixed code cause production incidents; aggressive thresholds can hide bugs.
