#!/usr/bin/env python3
"""Build a deterministic, integrity-manifested ZIP release of this skill set.

Example:
  python3 scripts/build-release.py --root . --output ../project-artifact-excellence.zip

The output must be outside the source tree to prevent self-inclusion. File
ordering, timestamps, compression, and POSIX permission bits are normalized.
SOURCE_DATE_EPOCH may be set for reproducible builds across environments.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
import zipfile
from pathlib import Path

from release_artifact_utils import EXECUTABLE_PATHS, MANIFEST_NAME, is_excluded, normalize_zip_timestamp


def collect_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if is_excluded(relative):
            continue
        if path.is_symlink():
            raise ValueError(f"release contains symlink; package real files only: {relative.as_posix()}")
        if path.is_file():
            files.append(path)
    return sorted(files, key=lambda p: p.relative_to(root).as_posix())


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build(root: Path, output: Path, epoch: int) -> dict[str, object]:
    root = root.resolve(strict=True)
    output = output.resolve()
    if not root.is_dir():
        raise ValueError(f"root is not a directory: {root}")
    if output == root or root in output.parents:
        raise ValueError("release output must be outside the source tree")
    timestamp = normalize_zip_timestamp(epoch)
    files = collect_files(root)
    if not files:
        raise ValueError("source tree contains no package files")

    entries: dict[str, bytes] = {}
    for path in files:
        relative = path.relative_to(root).as_posix()
        entries[relative] = path.read_bytes()
    manifest_lines = [f"{sha256(content)}  {name}" for name, content in sorted(entries.items())]
    entries[MANIFEST_NAME] = ("\n".join(manifest_lines) + "\n").encode("utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    temp_output = output.with_name(output.name + ".tmp")
    if temp_output.exists():
        temp_output.unlink()
    try:
        with zipfile.ZipFile(temp_output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, strict_timestamps=True) as archive:
            for name, content in sorted(entries.items()):
                info = zipfile.ZipInfo(filename=name, date_time=timestamp)
                info.create_system = 3  # Unix: preserve POSIX mode bits.
                info.compress_type = zipfile.ZIP_DEFLATED
                info.extra = b""
                info.comment = b""
                mode = 0o755 if name in EXECUTABLE_PATHS else 0o644
                info.external_attr = (mode & 0xFFFF) << 16
                archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
            archive.comment = b""
        os.replace(temp_output, output)
    finally:
        if temp_output.exists():
            temp_output.unlink()
    archive_digest = sha256(output.read_bytes())
    sidecar = output.with_suffix(output.suffix + ".sha256")
    sidecar_temp = sidecar.with_name(sidecar.name + ".tmp")
    try:
        sidecar_temp.write_text(f"{archive_digest}  {output.name}\n", encoding="utf-8", newline="\n")
        os.replace(sidecar_temp, sidecar)
    finally:
        if sidecar_temp.exists():
            sidecar_temp.unlink()
    return {
        "output": str(output),
        "sidecar": str(sidecar),
        "files": len(entries),
        "sha256": archive_digest,
        "bytes": output.stat().st_size,
        "timestamp": timestamp,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--epoch", type=int, default=None, help="normalized ZIP timestamp epoch; defaults to SOURCE_DATE_EPOCH or 946684800")
    args = parser.parse_args(argv)
    try:
        epoch = args.epoch if args.epoch is not None else int(os.environ.get("SOURCE_DATE_EPOCH", "946684800"))
        result = build(args.root, args.output, epoch)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: deterministic release built: {result['output']}")
    print(f"Files including RELEASE-MANIFEST.sha256: {result['files']}")
    print(f"Bytes: {result['bytes']}")
    print(f"SHA-256: {result['sha256']}")
    print(f"Detached checksum: {result['sidecar']}")
    print(f"Normalized ZIP timestamp: {result['timestamp']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
