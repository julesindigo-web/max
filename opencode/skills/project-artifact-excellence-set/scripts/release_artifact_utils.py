"""Shared policy for deterministic skill-set release artifacts."""
from __future__ import annotations

EXECUTABLE_PATHS = frozenset({
    ".githooks/pre-commit",
    "scripts/install-git-hook.sh",
    "scripts/build-release.py",
    "scripts/verify-release.py",
    "skills-create-excellence/scripts/validate-excellence.sh",
    "skills-create-excellence/scripts/process-audit-feedback.py",
    "skills-create-excellence/scripts/tests/test-validate-excellence.sh",
    "validation/validate-set.sh",
    "validation/validate_set_manifest.py",
    "validation/validate_trigger_matrices.py",
    "validation/validate_metric_specs.py",
    "validation/validate_task_ledger.py",
    "scripts/run-trigger-evaluation.py",
    "scripts/check-links-toc.py",
    "scripts/measure-context.py",
})
MANIFEST_NAME = "RELEASE-MANIFEST.sha256"
EXCLUDED_DIRS = frozenset({".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", "venv", ".venv"})
EXCLUDED_SUFFIXES = frozenset({".pyc", ".pyo", ".swp", ".tmp", ".zip"})


def normalize_zip_timestamp(epoch_seconds: int) -> tuple[int, int, int, int, int, int]:
    """Return a ZIP-valid, two-second-granularity UTC timestamp."""
    import datetime as dt
    epoch_seconds = max(epoch_seconds, 315532800)  # 1980-01-01T00:00:00Z
    dt_value = dt.datetime.fromtimestamp(epoch_seconds, tz=dt.timezone.utc)
    second = dt_value.second - (dt_value.second % 2)
    return (dt_value.year, dt_value.month, dt_value.day, dt_value.hour, dt_value.minute, second)


def is_excluded(path):
    from pathlib import Path
    path = Path(path)
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return True
    if path.name == MANIFEST_NAME or path.name == ".DS_Store":
        return True
    if path.suffix in EXCLUDED_SUFFIXES:
        return True
    return False
