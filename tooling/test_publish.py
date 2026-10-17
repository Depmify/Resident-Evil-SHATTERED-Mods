"""Publication tests use an in-memory GitHub stand-in; nothing is uploaded."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("shattered_publish", Path(__file__).with_name("publish.py"))
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="shattered-publication-tests-")
        self.root = Path(self.temporary.name)
        (self.root / "packages").mkdir()
        (self.root / "site").mkdir()
        self.bytes = b"Synthetic package bytes; no game assets and no actual publication."
        self.checksum = hashlib.sha256(self.bytes).hexdigest()
        self.asset = f"example.test-1.0-{self.checksum}.zip"
        self.package = self.root / "packages" / self.asset
        self.package.write_bytes(self.bytes)
        self.plan = {"formatVersion": 1, "packages": [{"id": "example.test", "version": "1.0", "tag": "mod-example.test-v1.0",
            "asset": self.asset, "sha256": self.checksum, "size": len(self.bytes)}]}
        self.catalog = {"formatVersion": 1, "mods": [{"manifest": {"id": "example.test", "version": "1.0"},
            "package": {"url": f"https://github.com/{publisher.REPOSITORY}/releases/download/mod-example.test-v1.0/{self.asset}",
                        "sha256": self.checksum, "size": len(self.bytes)}}]}
        self.assets = None
        self.calls = []

    def tearDown(self):
        self.temporary.cleanup()

    def run_publisher(self):
        (self.root / "publish-plan.json").write_text(json.dumps(self.plan), encoding="utf-8")
        (self.root / "site" / "catalog.json").write_text(json.dumps(self.catalog), encoding="utf-8")
        with patch.object(sys, "argv", ["publish.py", "--prepared", str(self.root)]), \
             patch.dict(os.environ, {"GITHUB_REPOSITORY": publisher.REPOSITORY, "GITHUB_SHA": "a" * 40}), \
             patch.object(publisher, "gh", self.fake_gh), contextlib.redirect_stdout(io.StringIO()):
            publisher.main()

    def fake_gh(self, *args, allow_missing=False):
        self.calls.append(args)
        self.assertNotIn("--clobber", args)
        command = args[1]
        if command == "view":
            if self.assets is None:
                return subprocess.CompletedProcess(args, 1, "", "not found")
            return subprocess.CompletedProcess(args, 0, json.dumps({"assets": [{"name": n} for n in self.assets]}), "")
        if command == "create":
            self.assets = {}
        elif command == "upload":
            path = Path(args[3]); self.assets[path.name] = path.read_bytes()
        elif command == "download":
            name = args[args.index("--pattern") + 1]
            (Path(args[args.index("--dir") + 1]) / name).write_bytes(self.assets[name])
        else:
            self.fail("Unexpected mocked GitHub operation")
        return subprocess.CompletedProcess(args, 0, "", "")

    def test_new_release_uploads_approved_bytes_then_verifies_download(self):
        self.run_publisher()
        self.assertEqual(self.bytes, self.assets[self.asset])
        self.assertEqual(["view", "create", "upload", "download"], [call[1] for call in self.calls])

    def test_identical_existing_asset_is_verified_and_never_replaced(self):
        self.assets = {self.asset: self.bytes}
        self.run_publisher()
        self.assertEqual(["view", "download"], [call[1] for call in self.calls])

    def test_existing_version_with_different_bytes_is_rejected(self):
        self.assets = {"example.test-1.0-anotherhash.zip": b"different"}
        with self.assertRaises(ValueError):
            self.run_publisher()
        self.assertEqual(["view"], [call[1] for call in self.calls])

    def test_prepared_bytes_cannot_change_after_validation(self):
        self.package.write_bytes(b"!" * len(self.bytes))
        with self.assertRaises(ValueError):
            self.run_publisher()
        self.assertEqual([], self.calls)

    def test_catalog_cannot_advertise_external_or_unapproved_package(self):
        self.catalog["mods"][0]["package"]["url"] = "https://evil.invalid/mod.zip"
        with self.assertRaises(ValueError):
            self.run_publisher()
        self.assertEqual([], self.calls)

    def test_released_bytes_are_verified_on_every_retry(self):
        self.assets = {self.asset: b"!" * len(self.bytes)}
        with self.assertRaises(ValueError):
            self.run_publisher()
        self.assertEqual(["view", "download"], [call[1] for call in self.calls])


if __name__ == "__main__":
    unittest.main()
