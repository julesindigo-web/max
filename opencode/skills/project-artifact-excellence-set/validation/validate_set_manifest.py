#!/usr/bin/env python3
"""Validate the repository's deliberately constrained skill-set YAML manifest.

Usage: python3 validation/validate_set_manifest.py [set-root]
No third-party packages required. Validates declared members, all required fields,
metric dimensions, safe paths, dependency references, and acyclic composition.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_TOP = {
    "name", "version", "purpose", "last-reviewed", "success-metrics", "members",
    "composition-rules", "shared-contracts", "validation-entry", "deprecation-policy", "migration-notes",
}
REQUIRED_METRICS = [
    "Trigger performance", "Task completion", "Context-token efficiency",
    "Time-to-working-skill", "Residual defect density",
]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class ManifestError(ValueError):
    pass


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value


def parse_constrained_yaml(path: Path) -> dict[str, Any]:
    """Parse the subset used by this manifest/template, without executing YAML tags."""
    top: dict[str, Any] = {}
    members: list[dict[str, Any]] = []
    top_lists: dict[str, list[str]] = {"success-metrics": [], "composition-rules": [], "shared-contracts": []}
    lines = path.read_text(encoding="utf-8").splitlines()
    section: str | None = None
    seen_top_level: set[str] = set()
    current_member: dict[str, Any] | None = None
    member_sublist: str | None = None

    for line_number, line in enumerate(lines, start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" in line[: len(line) - len(line.lstrip())]:
            raise ManifestError(f"tabs are not allowed for indentation (line {line_number})")

        if not line.startswith(" "):
            match = re.fullmatch(r"([a-z][a-z0-9-]*):(?:[ \t]*(.*))?", line)
            if not match:
                raise ManifestError(f"invalid top-level YAML line {line_number}: {line}")
            key, value = match.group(1), match.group(2) or ""
            if key in seen_top_level:
                raise ManifestError(f"duplicate top-level key: {key}")
            seen_top_level.add(key)
            section = key if key in {*top_lists, "members"} else None
            current_member = None
            member_sublist = None
            if key not in {*top_lists, "members"}:
                top[key] = scalar(value)
            elif value.strip():
                raise ManifestError(f"section '{key}' must use a block list on line {line_number}")
            continue

        if section in top_lists:
            match = re.fullmatch(r"  - (.+)", line)
            if not match:
                raise ManifestError(f"expected a two-space list item in '{section}' on line {line_number}")
            top_lists[section].append(scalar(match.group(1)))
            continue

        if section == "members":
            new_member = re.fullmatch(r"  - name:[ \t]*(.+)", line)
            if new_member:
                current_member = {"name": scalar(new_member.group(1)), "depends-on": [], "provides": []}
                members.append(current_member)
                member_sublist = None
                continue
            member_field = re.fullmatch(r"    (version|path|depends-on|provides):(?:[ \t]*(.*))?", line)
            if member_field and current_member is not None:
                field, raw_value = member_field.group(1), (member_field.group(2) or "").strip()
                if field in current_member and field not in {"depends-on", "provides"}:
                    raise ManifestError(f"duplicate '{field}' in member '{current_member['name']}'")
                if field in {"depends-on", "provides"}:
                    current_member[field] = []
                    member_sublist = field
                    if raw_value:
                        if not (raw_value.startswith("[") and raw_value.endswith("]")):
                            raise ManifestError(f"'{field}' must be a YAML list in member '{current_member['name']}'")
                        inner = raw_value[1:-1].strip()
                        if inner:
                            current_member[field] = [scalar(part) for part in inner.split(",")]
                    continue
                if not raw_value:
                    raise ManifestError(f"member '{current_member['name']}' needs a non-empty '{field}'")
                current_member[field] = scalar(raw_value)
                member_sublist = None
                continue
            nested_item = re.fullmatch(r"      - (.+)", line)
            if nested_item and current_member is not None and member_sublist in {"depends-on", "provides"}:
                current_member[member_sublist].append(scalar(nested_item.group(1)))
                continue
            raise ManifestError(f"invalid member syntax on line {line_number}: {line}")

        raise ManifestError(f"unexpected indented line outside a supported list on line {line_number}: {line}")

    top.update(top_lists)
    top["members"] = members
    return top


def safe_member_path(root: Path, raw_path: str) -> Path:
    if not raw_path or raw_path.startswith("/") or "\\" in raw_path:
        raise ManifestError(f"member path must be a non-empty relative POSIX path: {raw_path!r}")
    pieces = raw_path.split("/")
    if any(piece in {"", ".", ".."} for piece in pieces):
        raise ManifestError(f"member path contains an unsafe component: {raw_path!r}")
    candidate = root / raw_path
    resolved_root = root.resolve()
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise ManifestError(f"member path does not exist: {raw_path}") from exc
    if not resolved.is_relative_to(resolved_root):
        raise ManifestError(f"member path resolves outside the set root: {raw_path}")
    if not (resolved / "SKILL.md").is_file():
        raise ManifestError(f"member path must contain SKILL.md: {raw_path}")
    return resolved


def read_frontmatter_name(skill_file: Path) -> str:
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ManifestError(f"member frontmatter must start on line 1: {skill_file}")
    for line in lines[1:]:
        if line == "---":
            break
        match = re.fullmatch(r"name:[ \t]*(.+)", line)
        if match:
            return scalar(match.group(1))
    raise ManifestError(f"member frontmatter is missing name: {skill_file}")



def read_frontmatter_metadata(skill_file: Path) -> dict[str, Any]:
    """Read the metadata subset used by composable skill members."""
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ManifestError(f"member frontmatter must start on line 1: {skill_file}")
    in_metadata = False
    active_list: str | None = None
    result: dict[str, Any] = {"depends-on": [], "provides": []}
    metadata_seen = False
    for line in lines[1:]:
        if line == "---":
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            in_metadata = line == "metadata:"
            if in_metadata:
                metadata_seen = True
            active_list = None
            continue
        if not in_metadata:
            continue
        field_match = re.fullmatch(r"  (version|set-membership|depends-on|provides):(?:[ \t]*(.*))?", line)
        if field_match:
            field, raw_value = field_match.group(1), (field_match.group(2) or "").strip()
            if field in {"depends-on", "provides"}:
                result[field] = []
                active_list = field
                if raw_value:
                    if not (raw_value.startswith("[") and raw_value.endswith("]")):
                        raise ManifestError(f"metadata.{field} must be a list in {skill_file}")
                    inner = raw_value[1:-1].strip()
                    if inner:
                        result[field] = [scalar(item) for item in inner.split(",")]
            else:
                if field in result:
                    raise ManifestError(f"duplicate metadata.{field} in {skill_file}")
                result[field] = scalar(raw_value)
                active_list = None
            continue
        list_match = re.fullmatch(r"    - (.+)", line)
        if list_match and active_list in {"depends-on", "provides"}:
            result[active_list].append(scalar(list_match.group(1)))
    if not metadata_seen:
        raise ManifestError(f"metadata map is missing: {skill_file}")
    return result


def dependency_name(value: str, member_name: str) -> str:
    match = re.fullmatch(r"([a-z0-9]+(?:-[a-z0-9]+)*)(?:@(.+))?", value)
    if not match:
        raise ManifestError(f"invalid dependency declaration '{value}' in member '{member_name}'")
    return match.group(1)

def check_acyclic(graph: dict[str, list[str]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise ManifestError(f"dependency cycle detected at member '{node}'")
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph[node]:
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for member in graph:
        visit(member)


def validate(root: Path) -> list[str]:
    manifest_path = root / "manifest.yaml"
    if not manifest_path.is_file():
        raise ManifestError(f"manifest not found: {manifest_path}")
    data = parse_constrained_yaml(manifest_path)
    missing = REQUIRED_TOP - data.keys()
    if missing:
        raise ManifestError(f"missing top-level field(s): {', '.join(sorted(missing))}")
    unknown = data.keys() - REQUIRED_TOP
    if unknown:
        raise ManifestError(f"unknown top-level field(s): {', '.join(sorted(unknown))}")
    for key in REQUIRED_TOP - {"success-metrics", "members", "composition-rules", "shared-contracts"}:
        if not str(data.get(key, "")).strip():
            raise ManifestError(f"top-level field '{key}' must not be empty")

    if not KEBAB.fullmatch(data["name"]):
        raise ManifestError("set name must use lowercase kebab-case")
    if not SEMVER.fullmatch(data["version"]):
        raise ManifestError("set version must use semantic versioning")
    if not DATE.fullmatch(data["last-reviewed"]):
        raise ManifestError("last-reviewed must use YYYY-MM-DD")
    if not (root / "SET.md").is_file():
        raise ManifestError("SET.md is required alongside manifest.yaml")
    if not data["success-metrics"]:
        raise ManifestError("success-metrics must not be empty")
    for required in REQUIRED_METRICS:
        if not any(metric.startswith(required + ":") for metric in data["success-metrics"]):
            raise ManifestError(f"required set metric is missing: {required}")
    for metric in data["success-metrics"]:
        if not re.search(r"(≥|≤|>=|<=|\b\d+|%|percent|zero|within|at least|at most)", metric, re.I):
            raise ManifestError(f"set metric lacks an explicit measurable target: {metric}")
    if not data["members"]:
        raise ManifestError("members list must not be empty")
    if not data["composition-rules"]:
        raise ManifestError("composition-rules must not be empty")
    if not data["shared-contracts"]:
        raise ManifestError("shared-contracts must not be empty")

    by_name: dict[str, dict[str, Any]] = {}
    by_path: set[str] = set()
    graph: dict[str, list[str]] = {}
    messages: list[str] = []
    for member in data["members"]:
        name = member.get("name", "")
        version = member.get("version", "")
        path = member.get("path", "")
        if not isinstance(name, str) or not KEBAB.fullmatch(name):
            raise ManifestError(f"member name must use lowercase kebab-case: {name!r}")
        if name in by_name:
            raise ManifestError(f"duplicate member name: {name}")
        if not isinstance(version, str) or not SEMVER.fullmatch(version):
            raise ManifestError(f"member '{name}' needs a valid semantic version")
        if path in by_path:
            raise ManifestError(f"duplicate member path: {path}")
        by_path.add(path)
        member_dir = safe_member_path(root, path)
        skill_file = member_dir / "SKILL.md"
        actual_name = read_frontmatter_name(skill_file)
        if actual_name != name:
            raise ManifestError(f"member name mismatch: manifest says '{name}', SKILL.md says '{actual_name}'")
        metadata = read_frontmatter_metadata(skill_file)
        if metadata.get("version") != version:
            raise ManifestError(f"member version mismatch for '{name}': manifest='{version}', metadata='{metadata.get('version', '')}'")
        if metadata.get("set-membership") != data["name"]:
            raise ManifestError(f"member '{name}' metadata.set-membership must match set '{data['name']}'")
        dependencies = member.get("depends-on", [])
        if not isinstance(dependencies, list) or any(not isinstance(dep, str) or not dep for dep in dependencies):
            raise ManifestError(f"member '{name}' has an invalid depends-on list")
        provides = member.get("provides", [])
        if not isinstance(provides, list) or any(not isinstance(item, str) or not item for item in provides):
            raise ManifestError(f"member '{name}' has an invalid provides list")
        metadata_dependencies = [dependency_name(dep, name) for dep in metadata.get("depends-on", [])]
        if set(metadata_dependencies) != set(dependencies):
            raise ManifestError(f"member '{name}' metadata depends-on does not match manifest dependency declarations")
        if set(metadata.get("provides", [])) != set(provides):
            raise ManifestError(f"member '{name}' metadata provides does not match manifest provides declarations")
        by_name[name] = member
        graph[name] = dependencies
        messages.append(f"member valid: {name}@{version} ({path}); metadata/dependencies/contracts consistent")

    for name, dependencies in graph.items():
        if len(dependencies) != len(set(dependencies)):
            raise ManifestError(f"member '{name}' repeats a dependency")
        for dependency in dependencies:
            if dependency not in by_name:
                raise ManifestError(f"member '{name}' depends on undeclared member '{dependency}'")
            if dependency == name:
                raise ManifestError(f"member '{name}' cannot depend on itself")
    check_acyclic(graph)

    for raw_path in data["shared-contracts"]:
        safe_path = root / raw_path
        if raw_path.startswith("/") or ".." in Path(raw_path).parts or not safe_path.is_file():
            raise ManifestError(f"shared contract path does not exist or is unsafe: {raw_path}")
    entry = root / data["validation-entry"]
    if data["validation-entry"].startswith("/") or ".." in Path(data["validation-entry"]).parts or not entry.is_file():
        raise ManifestError("validation-entry must identify an existing relative file")

    declared_paths = set(by_path)
    candidate_dirs = [p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()]
    if (root / "skills").is_dir():
        candidate_dirs.extend(p for p in (root / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
    unlisted = sorted(p.relative_to(root).as_posix() for p in candidate_dirs if p.relative_to(root).as_posix() not in declared_paths)
    if unlisted:
        raise ManifestError(f"skill directories are not declared in the manifest: {', '.join(unlisted)}")
    return messages


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parents[1]
    try:
        for message in validate(root):
            print(f"PASS: {message}")
    except (OSError, ManifestError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: skill-set manifest validated: {root / 'manifest.yaml'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
