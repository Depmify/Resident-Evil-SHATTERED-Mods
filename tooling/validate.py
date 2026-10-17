#!/usr/bin/env python3
"""Run the checksum-pinned managed validator; submissions remain data."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--previous")
    args = parser.parse_args()
    trusted = Path(__file__).resolve().parent
    pin = json.loads((trusted / "validator.json").read_text(encoding="utf-8"))
    if pin.get("formatVersion") != 1 or pin.get("file") != "catalog-validator.zip":
        raise ValueError("Unsupported trusted validator pin")
    bundle = trusted / pin["file"]
    if hashlib.sha256(bundle.read_bytes()).hexdigest() != pin.get("sha256"):
        raise ValueError("Trusted validator bundle checksum mismatch")
    with tempfile.TemporaryDirectory(prefix="shattered-catalog-validator-") as temporary:
        root = Path(temporary).resolve()
        with zipfile.ZipFile(bundle) as archive:
            if len(archive.infolist()) > 128 or sum(i.file_size for i in archive.infolist()) > 128 * 1024 * 1024:
                raise ValueError("Trusted bundle exceeds its budget")
            for entry in archive.infolist():
                path = PurePosixPath(entry.filename)
                if path.is_absolute() or ".." in path.parts or "\\" in entry.filename or ":" in entry.filename:
                    raise ValueError("Unsafe trusted bundle path")
                if entry.external_attr >> 16 & 0o170000 == 0o120000:
                    raise ValueError("Trusted bundle must not contain symlinks")
            archive.extractall(root)
        command = ["dotnet", str(root / "Shattered.ModBrowser.Catalog.dll")]
        subprocess.run(command + ["--self-test"], cwd=root, check=True)
        options = ["--source", str(Path(args.source).resolve()), "--output", str(Path(args.output).resolve())]
        if args.previous:
            options += ["--previous", str(Path(args.previous).resolve())]
        subprocess.run(command + options, cwd=root, check=True)


if __name__ == "__main__":
    main()
