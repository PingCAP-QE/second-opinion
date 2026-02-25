from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class WorkflowContractTests(unittest.TestCase):
    def test_skill_language_and_output_contract(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        markers = [
            "Infer the review-output language from the user prompt that triggers",
            "Do not ask a separate language-preference question",
            "Write artifacts to the workspace root",
            "second_opinion_meta.json",
            "second_opinion.md",
            "second_opinion.json",
            "Chat findings are supplementary; they do not replace required file outputs.",
        ]
        for marker in markers:
            self.assertIn(marker, content, f"Missing contract marker in SKILL.md: {marker}")

    def test_pr_review_language_and_root_output_contract(self):
        content = (ROOT / "processes" / "pr-review" / "criteria.md").read_text(encoding="utf-8")
        markers = [
            "Apply shared language contract from `fragments/review-language-contract.md`.",
            "Write these files in the repository root.",
            "Printed chat findings do not satisfy",
        ]
        for marker in markers:
            self.assertIn(marker, content, f"Missing contract marker in pr-review criteria: {marker}")

    def test_review_branch_language_and_root_output_contract(self):
        content = (ROOT / "processes" / "review-branch" / "criteria.md").read_text(
            encoding="utf-8"
        )
        markers = [
            "Apply shared language contract from `fragments/review-language-contract.md`.",
            "Write these files in the repository root.",
            "Printed chat findings do not satisfy",
        ]
        for marker in markers:
            self.assertIn(
                marker,
                content,
                f"Missing contract marker in review-branch criteria: {marker}",
            )

    def test_language_fragment_contract(self):
        content = (ROOT / "fragments" / "review-language-contract.md").read_text(
            encoding="utf-8"
        )
        markers = [
            "Infer review-output language from the user prompt that triggers second opinion.",
            "Use that language for `second_opinion.md` and user-facing review communication.",
            "Do not ask a separate language-preference question unless the user asks to override.",
            "Keep repository assets and code in English",
        ]
        for marker in markers:
            self.assertIn(
                marker,
                content,
                f"Missing contract marker in review-language fragment: {marker}",
            )

    def test_output_fragment_requires_root_files(self):
        content = (ROOT / "fragments" / "output-review-findings.md").read_text(
            encoding="utf-8"
        )
        markers = [
            "Write both files in the repository root.",
            "Printed chat findings do not satisfy",
        ]
        for marker in markers:
            self.assertIn(marker, content, f"Missing contract marker in output fragment: {marker}")
