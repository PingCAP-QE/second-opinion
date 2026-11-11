"""Exercise the shipping CLI's read boundary; all provider I/O is synthetic."""

import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import review_only as runner
from scripts.install_skill import install

ROOT = Path(__file__).resolve().parents[1]
MARKER = "SYNTHETIC-OUTSIDE-AUTHORIZED-TREE"
SAFE = "SYNTHETIC-AUTHORIZED-SOURCE"


def response():
    return {"status": "completed", "output": [{"type": "message", "role": "assistant",
            "status": "completed", "content": [{"type": "output_text", "text": '{"findings":[]}'}]}]}


class EvidenceReadTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.tree = self.base / "authorized"
        self.tree.mkdir()
        self.diff = self.tree / "change.diff"
        self.diff.write_text("+ " + SAFE)
        self.evidence = self.tree / "source.txt"
        self.evidence.write_text(SAFE)
        self.outside = self.base / "outside.txt"
        self.outside.write_text(MARKER)
        self.counter = 0

    def invoke(self, diff=None, context=None, root=None):
        self.counter += 1
        output = self.base / f"output-{self.counter}"
        output.mkdir()
        args = ["--review-root", str(root or self.tree), "--diff", str(diff or self.diff),
                "--language", "English", "--model", "synthetic", "--output-dir", str(output)]
        if context is not None:
            args += ["--context-file", str(context)]
        with patch.dict(os.environ, {"SECOND_OPINION_API_KEY": "synthetic"}, clear=True), \
             patch.object(runner, "request_review", return_value=response()) as provider, \
             patch("sys.stderr", io.StringIO()) as error:
            result = runner.main(args)
        return result, provider, output, error.getvalue()

    def rejected(self, **kwargs):
        result, provider, output, error = self.invoke(**kwargs)
        self.assertEqual(result, 1)
        provider.assert_not_called()
        self.assertEqual(list(output.iterdir()), [])
        self.assertNotIn(MARKER, error)

    def test_absolute_outside_diff_and_context_never_reach_provider(self):
        for field in ("diff", "context"):
            with self.subTest(field=field):
                self.rejected(**{field: self.outside})

    def test_traversal_prefix_confusion_and_trusted_install_are_rejected(self):
        sibling = self.base / "authorized-other"
        sibling.mkdir()
        (sibling / "data").write_text(MARKER)
        for path in ("../outside.txt", self.tree / ".." / "outside.txt", sibling / "data",
                     ROOT / "taxonomy.md", self.tree):
            for field in ("diff", "context"):
                with self.subTest(path=path, field=field):
                    self.rejected(**{field: path})
        self.rejected(root=self.tree / ".." / "authorized")

    def test_leaf_and_ancestor_symlinks_are_rejected_even_when_target_is_inside(self):
        leaf = self.tree / "architecture.md"
        leaf.symlink_to(self.outside)
        inside = self.tree / "inside-link"
        inside.symlink_to(self.evidence)
        directory = self.tree / "docs"
        directory.symlink_to(self.base, target_is_directory=True)
        for path in (leaf, inside, directory / "outside.txt"):
            for field in ("diff", "context"):
                with self.subTest(path=path, field=field):
                    self.rejected(**{field: path})

    def test_hardlinks_directories_and_fifos_are_rejected_without_blocking(self):
        hardlink = self.tree / "hardlink"
        os.link(self.outside, hardlink)
        fifo = self.tree / "pipe"
        os.mkfifo(fifo)
        directory = self.tree / "directory"
        directory.mkdir()
        for path in (hardlink, fifo, directory):
            for field in ("diff", "context"):
                with self.subTest(path=path, field=field):
                    self.rejected(**{field: path})

    def test_relative_inputs_ignore_hostile_cwd_and_keep_normal_review_working(self):
        previous = Path.cwd()
        try:
            os.chdir(self.base)
            (self.base / "change.diff").write_text(MARKER)
            result, provider, output, _ = self.invoke(diff="change.diff", context="source.txt")
        finally:
            os.chdir(previous)
        self.assertEqual(result, 0)
        data = json.loads(provider.call_args.args[0]["input"][0]["content"])
        self.assertEqual(data["evidence"], [SAFE])
        self.assertNotIn(MARKER, json.dumps(data))
        self.assertEqual({p.name for p in output.iterdir()}, set(runner.OUTPUTS))

    def test_root_alias_and_canonical_absolute_spelling_share_the_pinned_tree(self):
        alias = self.base / "operator-selected-root"
        alias.symlink_to(self.tree, target_is_directory=True)
        for diff in (alias / self.diff.name, self.diff.resolve()):
            result, provider, _, _ = self.invoke(root=alias, diff=diff)
            self.assertEqual(result, 0)
            self.assertIn(SAFE, provider.call_args.args[0]["input"][0]["content"])

    def test_leaf_replacement_by_symlink_is_rejected_at_open(self):
        original_open = os.open
        swapped = []
        def swap(path, flags, *args, **kwargs):
            if path == self.evidence.name and kwargs.get("dir_fd") is not None and not swapped:
                swapped.append(True)
                self.evidence.unlink()
                self.evidence.symlink_to(self.outside)
            return original_open(path, flags, *args, **kwargs)
        with patch.object(os, "open", side_effect=swap):
            self.rejected(context=self.evidence)
        self.assertTrue(swapped)

    def test_ancestor_replacement_before_open_is_rejected(self):
        nested = self.tree / "nested"
        nested.mkdir()
        (nested / "source.txt").write_text(SAFE)
        original_open = os.open
        swapped = []
        def swap(path, flags, *args, **kwargs):
            if path == "nested" and kwargs.get("dir_fd") is not None and not swapped:
                swapped.append(True)
                nested.rename(self.base / "retained")
                nested.symlink_to(self.base, target_is_directory=True)
            return original_open(path, flags, *args, **kwargs)
        with patch.object(os, "open", side_effect=swap):
            self.rejected(context=nested / "source.txt")
        self.assertTrue(swapped)

    def test_already_open_parent_cannot_be_redirected_by_rename(self):
        nested = self.tree / "nested"
        nested.mkdir()
        (nested / "source.txt").write_text(SAFE)
        (self.base / "source.txt").write_text(MARKER)
        original_open = os.open
        swapped = []
        def swap(path, flags, *args, **kwargs):
            if path == "source.txt" and kwargs.get("dir_fd") is not None and not swapped:
                swapped.append(True)
                nested.rename(self.base / "retained")
                nested.symlink_to(self.base, target_is_directory=True)
            return original_open(path, flags, *args, **kwargs)
        with patch.object(os, "open", side_effect=swap):
            result, provider, _, _ = self.invoke(context=nested / "source.txt")
        self.assertEqual(result, 0)
        data = json.loads(provider.call_args.args[0]["input"][0]["content"])
        self.assertEqual(data["evidence"], [SAFE])
        self.assertNotIn(MARKER, json.dumps(data))
        self.assertTrue(swapped)

    def test_root_replacement_after_pinning_cannot_redirect_reads(self):
        (self.base / "change.diff").write_text(MARKER)
        compile_review = runner.compile_review
        swapped = []
        def swap(*args, **kwargs):
            if not swapped:
                swapped.append(True)
                self.tree.rename(self.base / "retained")
                self.tree.symlink_to(self.base, target_is_directory=True)
            return compile_review(*args, **kwargs)
        with patch.object(runner, "compile_review", side_effect=swap):
            result, provider, _, _ = self.invoke()
        self.assertEqual(result, 0)
        data = json.loads(provider.call_args.args[0]["input"][0]["content"])
        self.assertIn(SAFE, data["diff"])
        self.assertNotIn(MARKER, json.dumps(data))

    def test_missing_invalid_utf8_and_combined_oversize_fail_before_provider(self):
        self.rejected(context=self.tree / "missing")
        self.evidence.write_bytes(b"\xff")
        self.rejected(context=self.evidence)
        self.evidence.write_bytes(b"a" * runner.LIMIT)
        self.rejected(context=self.evidence)

    def test_all_input_descriptors_close_on_read_failure(self):
        opened = []
        original_open = os.open
        original_dup = os.dup
        def remember(*args, **kwargs):
            fd = original_open(*args, **kwargs)
            opened.append(fd)
            return fd
        def remember_dup(*args, **kwargs):
            fd = original_dup(*args, **kwargs)
            opened.append(fd)
            return fd
        with patch.object(os, "open", side_effect=remember), patch.object(os, "dup", side_effect=remember_dup):
            self.rejected(context=self.tree / "missing")
        for fd in set(opened):
            with self.assertRaises(OSError):
                os.fstat(fd)

    def test_exported_and_reexported_cli_enforce_same_read_boundary(self):
        exported = self.base / "installed"
        reexported = self.base / "reinstalled"
        install(ROOT, exported)
        install(exported, reexported)
        link = self.tree / "committed-link"
        link.symlink_to(self.outside)
        driver = '''import json,sys
sys.path.insert(0, sys.argv[1])
from scripts import review_only as runner
def fake_transport(payload, key):
    assert "SYNTHETIC-OUTSIDE-AUTHORIZED-TREE" not in json.dumps(payload)
    print("SYNTHETIC_PROVIDER_CALLED")
    return {"status":"completed","output":[{"type":"message","role":"assistant",
      "status":"completed","content":[{"type":"output_text","text":'{"findings":[]}'}]}]}
runner.request_review = fake_transport
raise SystemExit(runner.main(sys.argv[2:]))
'''
        for installation in (exported, reexported):
            self.assertEqual((installation / "scripts/review_only.py").read_bytes(),
                             (ROOT / "scripts/review_only.py").read_bytes())
            for context, expected in ((self.evidence, 0), (self.outside, 1), (link, 1)):
                self.counter += 1
                output = self.base / f"installed-output-{self.counter}"
                output.mkdir()
                result = subprocess.run([sys.executable, "-I", "-c", driver, str(installation),
                        "--review-root", str(self.tree), "--diff", str(self.diff),
                        "--context-file", str(context), "--language", "English", "--model", "synthetic",
                        "--output-dir", str(output)], cwd=self.tree, capture_output=True, text=True,
                        timeout=20, env={"PATH": os.defpath, "HOME": str(self.base),
                                         "SECOND_OPINION_API_KEY": "synthetic"})
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertEqual("SYNTHETIC_PROVIDER_CALLED" in result.stdout, expected == 0)
                self.assertNotIn(MARKER, result.stdout + result.stderr)
                self.assertEqual(bool(list(output.iterdir())), expected == 0)
