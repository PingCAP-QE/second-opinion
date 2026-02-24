# BBA expert criteria

- rule_id: BBA-RE-001
  description: |
    Start with explicit scope mapping before diving into details. Enumerate
    change types (new code paths, deletions, refactors, behavior/default
    changes, dependency/config/data-structure changes) and identify high-risk
    zones such as auth boundaries, input parsing, serialization, concurrency,
    persistence, and public API/protocol changes.
  tags:
    - risk:correctness
    - risk:security
    - risk:concurrency
    - theme:api
  rationale: Accurate scope definition prevents blind spots and anchors the rest of the review.

- rule_id: BBA-RE-002
  description: |
    For each core change, perform blast-radius tracing from entry points to
    internal side effects: interface contracts, call sites/dependents, runtime
    defaults, feature gates, fallback paths, and backward compatibility with old
    clients/data. Record concrete evidence for each confirmed impact.
  tags:
    - risk:correctness
    - risk:compat
    - theme:api
  rationale: Most regressions are caused by indirect effects rather than edited lines.

- rule_id: BBA-RE-003
  description: |
    Keep findings evidence-backed. Every non-trivial conclusion must cite at
    least one concrete anchor (code path, test output, runtime log, or API
    contract). Avoid "maybe"-style claims; when uncertain, mark missing inputs
    and give the shortest verification path.
  tags:
    - risk:correctness
    - theme:testing
    - theme:error-handling
  rationale: Evidence-first review reduces noise and makes fixes actionable.

- rule_id: BBA-RE-004
  description: |
    Validate core review dimensions and mark each as confirmed or N/A:
    correctness, security, data consistency/concurrency, performance,
    observability, and test/documentation coverage. For behavior changes, check
    boundary conditions, failure paths, and rollback/upgrade safety.
  tags:
    - risk:correctness
    - risk:security
    - risk:concurrency
    - risk:perf
    - risk:ops
    - scenario:upgrade
    - scenario:rollback
  rationale: A fixed checklist limits omission risk on complex changes.

- rule_id: BBA-RE-005
  description: |
    Mandatory second-pass verification is required when either condition holds:
    (a) finding confidence is medium/low, or (b) severity is high/critical.
    The second pass must use a different method (broader call-site tracing,
    focused build/test/static check, or historical contract verification via
    blame/history) and should include reproducible evidence when possible.
  tags:
    - risk:correctness
    - risk:concurrency
    - risk:security
    - theme:testing
  rationale: Independent confirmation sharply lowers false positives and missed blockers.

- rule_id: BBA-RE-006
  description: |
    For data/state mutations, verify ownership and consistency invariants:
    atomic boundaries, partial-failure handling, retries/idempotence, and
    cross-object update safety. Ensure rollback behavior does not leave
    inconsistent or partially applied state.
  tags:
    - risk:correctness
    - risk:concurrency
    - risk:compat
    - scenario:rollback
  rationale: Data inconsistency issues are high impact and often expensive to recover.

- rule_id: BBA-RE-007
  description: |
    Report findings in a structured format ordered by severity then confidence.
    Each item should include: what is wrong, evidence, impact, minimum fix
    direction, and verification steps.
  tags:
    - theme:testing
    - theme:observability
    - risk:ops
  rationale: Structured output improves triage speed and reduces ambiguity during remediation.
