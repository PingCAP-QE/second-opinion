# GitHub comment contract

Apply this contract only when the user asks to post review findings to GitHub,
or explicitly confirms posting after review outputs are complete.

## Output artifact

Write `github_comments.json` in the repository root as the posting payload plan.

Each comment entry should include:
- mode: `inline` or `general`
- source attribution: `Source: <type>/<id>` in the comment body
- repo footer: `Second Opinion: <repo_url>` as the final non-empty line

## Language and formatting

- Always use English in GitHub comments, regardless of review-output language.
- Keep comments concise, actionable, and tied to one finding each.
- Include what is wrong and the concrete fix direction.

## Anchoring

- Use `inline` mode only when the target line is diff-resolvable.
- If anchoring is uncertain or unavailable, use `general` mode.

## Posting safety

- Do not add repository shell posting scripts for GitHub comments.
- For actual posting, use `gh` CLI when available.
- If `gh` is unavailable or not authenticated, fail the posting step explicitly and stop.
- Posting review comments requires PR context. Without a PR URL, fail posting explicitly and keep local outputs only.
