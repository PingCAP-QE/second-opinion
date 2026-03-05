# Output contract: second_opinion.md and second_opinion.json

Produce two outputs:
- `second_opinion.md`: a readable summary for humans.
- `second_opinion.json`: a machine-readable findings list.

Write both files in the repository root. Printed chat findings do not satisfy
this output contract.

`second_opinion.json` must be a JSON object with a single top-level field:
- `findings`: an array of findings.

Each finding MUST include:
- `file`: string, file path.
- `lines`: string, use a best-effort range like `L10-L25` or `L42`.
- `source`: object with `type` + `id`.
  - `type` must be one of: `rule`, `process`, `policy`.
  - `id` is the originating rule_id / process id / policy id.
- `tags`: array of taxonomy tags (use only tags defined in `taxonomy.md`).
- `severity`: one of `low`, `medium`, `high`, `critical`.
- `message`: a concise, actionable description + fix direction.

For `second_opinion.md`, each finding section MUST include:
- `Source: <type>/<id>` (for example, `Source: rule/EXAMPLE-RULE-001`).

Severity guidance (map "must fix" to severity):
- "Must fix: Yes" → `high` or `critical`
- "Must fix: No" → `low` or `medium`
