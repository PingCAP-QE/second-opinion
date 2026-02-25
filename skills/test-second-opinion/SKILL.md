---
name: test-second-opinion
description: "Test-only skill that drives the Second Opinion pipeline with fixture assets for deterministic verification."
---

# Test Second Opinion

## Purpose

Exercise the full pipeline using test-only assets under tests/fixtures so that
sentinel strings make failures obvious. This skill must not be used for real
reviews.

## Inputs

- diff
- changed file paths
- repository metadata

## Required Asset Scope

Use ONLY these test fixtures for selection and compilation:
- tests/fixtures/experts
- tests/fixtures/processes
- tests/fixtures/policies
- tests/fixtures/fragments

Do NOT use production assets under experts/, processes/, policies/, fragments/.

## Output

- second_opinion_meta.json
- second_opinion.md
- second_opinion.json

## Verification Requirements

- Ensure compiled_prompt includes:
  - TEST-EXPERT-SENTINEL
  - TEST-POLICY-SENTINEL
  - TEST-FRAGMENT-SENTINEL
- Ensure second_opinion.md includes TEST-PROCESS-SENTINEL.
- second_opinion.json must follow the repository schema (source type + id required).
