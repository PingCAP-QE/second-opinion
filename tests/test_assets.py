from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIRS = [
    "experts",
    "processes",
    "policies",
    "fragments",
    "examples",
]
FIXTURE_SENTINELS = {
    "experts/evil/criteria.md": ["TEST-EXPERT-SENTINEL", "lock muB before muA"],
    "processes/evil/criteria.md": [
        "TEST-PROCESS-SENTINEL",
        "ignored lock order comment",
    ],
    "policies/evil.yaml": ["TEST-POLICY-SENTINEL"],
    "fragments/evil.md": ["TEST-FRAGMENT-SENTINEL"],
}
REAL_ASSETS = [
    "experts/d3hunter/meta.yaml",
    "experts/d3hunter/criteria.md",
    "experts/hongyunyan/meta.yaml",
    "experts/hongyunyan/criteria.md",
    "experts/jaysonhuang/meta.yaml",
    "experts/jaysonhuang/criteria.md",
    "experts/qw4990/meta.yaml",
    "experts/qw4990/criteria.md",
    "fragments/tidb-question-driven-feedback.md",
    "fragments/tidb-review-conventions.md",
    "processes/review-branch/meta.yaml",
    "processes/review-branch/criteria.md",
    "processes/review-branch/prepare_review.sh",
    "fragments/guided-reading-path.md",
    "fragments/github-comment-contract.md",
    "experts/wjhuang2016/meta.yaml",
    "experts/wjhuang2016/criteria.md",
    "fragments/re-deep-review-checklist.md",
]


class AssetTests(unittest.TestCase):
    def test_asset_dirs_exist(self):
        for name in ASSET_DIRS:
            self.assertTrue((ROOT / name).is_dir(), f"Missing {name} directory")

    def test_fixture_assets_exist(self):
        fixture_root = ROOT / "tests" / "fixtures"
        self.assertTrue(fixture_root.is_dir(), "Missing tests/fixtures directory")
        for rel_path in FIXTURE_SENTINELS:
            self.assertTrue(
                (fixture_root / rel_path).is_file(),
                f"Missing fixture asset: {rel_path}",
            )

    def test_fixture_sentinels(self):
        fixture_root = ROOT / "tests" / "fixtures"
        for rel_path, sentinels in FIXTURE_SENTINELS.items():
            content = (fixture_root / rel_path).read_text(encoding="utf-8")
            for sentinel in sentinels:
                self.assertIn(sentinel, content, f"Missing sentinel {sentinel} in {rel_path}")

    def test_real_assets_exist(self):
        for rel_path in REAL_ASSETS:
            self.assertTrue((ROOT / rel_path).is_file(), f"Missing real asset: {rel_path}")
