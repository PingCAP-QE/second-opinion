# Guided reading path for review output

When producing `review.md`, include a short "guided reading path" section:

- Step 1..N with:
  - start location (`file` + `function`/`symbol`)
  - why this point is first
  - what to inspect (data flow, invariants, state transitions)
- Add a "10-minute critical path" with exactly three locations for fast triage.

Purpose:
- Reduce reviewer onboarding cost.
- Make findings reproducible and easy to verify.
