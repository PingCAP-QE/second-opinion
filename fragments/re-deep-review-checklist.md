# Deep review checklist and output shape

Use this structure when the user asks for high-assurance review depth.

## Conclusion

- Summarize merge risk in 1-3 bullets.

## Confirmed checklist

Mark each area as `confirmed` or `N/A`, and include short evidence:
- correctness
- security
- data consistency
- performance
- compatibility
- observability
- testing
- documentation

## Findings ordering and fields

Order findings by severity, then confidence.

Required fields per finding:
- Severity: `Blocker | High | Medium | Low`
- Confidence: `High | Medium | Low`
- What: precise defect statement
- Evidence: code path, test output, or contract proof
- Impact: affected behavior and worst case
- Fix: smallest safe change
- Verify: minimal reproduction or validation command

If no issues are found, state "No issues found" and list concrete checks performed.
