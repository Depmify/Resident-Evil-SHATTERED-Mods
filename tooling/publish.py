#!/usr/bin/env python3
"""Publish validated, immutable ZIP bytes. Used only after a reviewed merge."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

REPOSITORY = "Depmify/Resident-Evil-SHATTERED-Mods"


def gh(*args, allow_missing=False):
    result = subprocess.run(["gh", *args, "--repo", REPOSITORY], capture_output=True, text=True)
    if result.returncode and not allow_missing:
        raise RuntimeError(result.stderr.strip() or "GitHub CLI command failed")
    return result


def verify(path, size, expected_hash):
    if path.stat().st_size != size:
        raise ValueError("Prepared/released ZIP size differs from its approved size")
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(65536):
            digest.update(block)
    if digest.hexdigest() != expected_hash:
        raise ValueError("Prepared/released ZIP checksum differs from its approved checksum")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepared", required=True)
    args = parser.parse_args()
    if os.environ.get("GITHUB_REPOSITORY", "").casefold() != REPOSITORY.casefold():
        raise ValueError("Publication is restricted to the official repository")
    commit = os.environ.get("GITHUB_SHA", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Publication requires an exact trusted commit")
    root = Path(args.prepared).resolve()
    plan = json.loads((root / "publish-plan.json").read_text(encoding="utf-8"))
    catalog = json.loads((root / "site" / "catalog.json").read_text(encoding="utf-8"))
    if plan.get("formatVersion") != 1 or catalog.get("formatVersion") != 1:
        raise ValueError("Unsupported publication plan")
    entries = {entry["manifest"]["id"]: entry for entry in catalog["mods"]}
    if len(entries) != len(plan["packages"]):
        raise ValueError("Publication plan and catalog differ")
    for item in plan["packages"]:
        identifier, version, checksum = item["id"], item["version"], item["sha256"]
        if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,127}", identifier) or not re.fullmatch(r"[0-9]+(?:\.[0-9]+){1,3}", version):
            raise ValueError("Invalid mod identity in publication plan")
        if not re.fullmatch(r"[0-9a-f]{64}", checksum):
            raise ValueError("Invalid package checksum in publication plan")
        asset = f"{identifier}-{version}-{checksum}.zip"
        tag = f"mod-{identifier}-v{version}"
        if item["asset"] != asset or item["tag"] != tag or not 0 < item["size"] < 2 * 1024 * 1024 * 1024:
            raise ValueError("Unexpected package asset, tag or size")
        entry = entries[identifier]
        expected_url = f"https://github.com/{REPOSITORY}/releases/download/{tag}/{asset}"
        if entry["package"] != {"url": expected_url, "sha256": checksum, "size": item["size"]} or entry["manifest"]["version"] != version:
            raise ValueError("Catalog package differs from its publication plan")
        package = root / "packages" / asset
        verify(package, item["size"], checksum)
        existing = gh("release", "view", tag, "--json", "assets", allow_missing=True)
        if existing.returncode:
            gh("release", "create", tag, "--target", commit, "--title", f"{identifier} {version}",
               "--notes", "Validated SHATTERED mod package. The asset filename identifies its SHA-256.")
            assets = []
        else:
            assets = json.loads(existing.stdout)["assets"]
        names = {value["name"] for value in assets}
        if any(name.endswith(".zip") and name != asset for name in names):
            raise ValueError(f"Release {tag} already contains another package: published versions are immutable")
        if asset not in names:
            # Deliberately no --clobber: an approved asset is never overwritten.
            gh("release", "upload", tag, str(package))
        with tempfile.TemporaryDirectory(prefix="shattered-release-verification-") as directory:
            gh("release", "download", tag, "--pattern", asset, "--dir", directory)
            verify(Path(directory) / asset, item["size"], checksum)
        print(f"Verified official Release: {identifier} {version}")
    print(f"All {len(entries)} official packages exist with their approved bytes; Pages can now deploy.")


if __name__ == "__main__":
    main()
