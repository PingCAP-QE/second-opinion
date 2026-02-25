# Remote branch review workflow (upstream-aligned)

## 0) Inputs

Accept either:
- `<pr_url>`
- `<review_remote_url> <review_branch>`

Optional flags:
- `--base <master|main|custom>`
- `--paths p1,p2,...`
- `--no-merge-base`
- `--run-tests`

## 1) Baseline preparation

- Ensure `upstream` exists and fetch the latest base branch (`master`, fallback `main`).
- Fetch the target review branch from a deterministic review remote.
- Create a codex-owned local review branch under `codex/review/*`.
- Use an isolated worktree and locally merge the latest upstream base into the review branch
  unless the user explicitly requests `--no-merge-base`.

Helper:
- Use `processes/review-branch/prepare_review.sh` for repeatable setup.

## 2) Scope and evidence

- Compute review scope from `BASE...HEAD` after baseline alignment.
- Prefer user-provided artifacts and path-focused reading when `--paths` is set.
- For uncertain logic, follow call chains until invariants and side effects are clear.

## 3) Review dimensions

Always check:
- correctness and error handling
- concurrency and resource lifecycle
- security footguns and unsafe defaults

Conditionally check:
- compatibility/upgrade impacts when behavior or public contracts change
- hot-path performance when modified code is execution-critical

## 4) Output contract

Produce both:
- `review.md`: summary + guided reading path + prioritized findings
- `review.json`: schema-compliant findings with source attribution and severity

Testing note:
- CI is authoritative by default; only run local tests when explicitly requested.

## 5) Stop and wait

After writing `review.md` and `review.json`, stop and wait for explicit user instruction.
Never perform GitHub operations with side effects unless explicitly requested.
