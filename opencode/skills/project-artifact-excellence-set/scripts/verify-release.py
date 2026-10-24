#!/usr/bin/env python3
"""Verify ZIP safety, required release files, executable modes, and SHA-256s."""
from __future__ import annotations

import argparse
import hashlib
import re
import stat
import sys
import zipfile
from pathlib import PurePosixPath
from pathlib import Path

from release_artifact_utils import EXECUTABLE_PATHS, MANIFEST_NAME


def verify(archive_path: Path) -> list[str]:
    with zipfile.ZipFile(archive_path, "r") as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(names) != len(set(names)):
            raise ValueError("ZIP contains duplicate entry names")
        for name in names:
            pure = PurePosixPath(name)
            if pure.is_absolute() or ".." in pure.parts or "\\" in name or not name or name.endswith("/"):
                raise ValueError(f"unsafe or unsupported ZIP entry path: {name!r}")
        files = set(names)
        # Reject symlink entries and ambiguous file/parent collisions before any extraction.
        file_paths = {PurePosixPath(name) for name in names}
        for name, info in zip(names, infos):
            mode = (info.external_attr >> 16) & 0xFFFF
            if stat.S_ISLNK(mode):
                raise ValueError(f"ZIP contains a symbolic-link entry: {name}")
            pure = PurePosixPath(name)
            parents = list(pure.parents)[:-1]  # omit the implicit '.' parent
            collision = next((str(parent) for parent in parents if parent in file_paths), None)
            if collision:
                raise ValueError(f"ZIP file/parent path collision: {collision!r} is a parent of {name!r}")
        for required in ("SET.md", "manifest.yaml", "validation/validate-set.sh", "evaluation/trigger-evaluation-matrix.json", MANIFEST_NAME):
            if required not in files:
                raise ValueError(f"required release file is missing: {required}")
        for executable in sorted(EXECUTABLE_PATHS):
            if executable not in files:
                raise ValueError(f"required executable entry is missing: {executable}")
            info = archive.getinfo(executable)
            mode = (info.external_attr >> 16) & 0xFFFF
            if not (mode & 0o111):
                raise ValueError(f"required executable bit is missing in ZIP metadata: {executable}")
        manifest_bytes = archive.read(MANIFEST_NAME)
        try:
            manifest_text = manifest_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("release manifest is not UTF-8") from exc
        declared: dict[str, str] = {}
        for line_number, line in enumerate(manifest_text.splitlines(), start=1):
            match = re.fullmatch(r"([0-9a-f]{64})  ([^\r\n]+)", line)
            if not match:
                raise ValueError(f"invalid checksum manifest line {line_number}")
            digest, name = match.groups()
            if name in declared:
                raise ValueError(f"duplicate checksum entry: {name}")
            if name not in files:
                raise ValueError(f"checksum manifest refers to missing entry: {name}")
            declared[name] = digest
        if set(declared) != files - {MANIFEST_NAME}:
            missing = sorted((files - {MANIFEST_NAME}) - set(declared))
            extra = sorted(set(declared) - (files - {MANIFEST_NAME}))
            raise ValueError(f"checksum coverage mismatch; missing={missing}, extra={extra}")
        for name, expected in declared.items():
            actual = hashlib.sha256(archive.read(name)).hexdigest()
            if actual != expected:
                raise ValueError(f"SHA-256 mismatch: {name}")
        return [f"verified {len(declared)} file checksums", f"verified {len(EXECUTABLE_PATHS)} executable modes", "verified required release files and safe entry paths"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args(argv)
    try:
        results = verify(args.archive.resolve(strict=True))
    except (OSError, zipfile.BadZipFile, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    for result in results:
        print(f"PASS: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
