#!/usr/bin/env python3
"""Verify that built distributions contain the schema, docs, and package data."""

from __future__ import annotations

import sys
import tarfile
import zipfile
from pathlib import Path


REQUIRED_WHEEL_SUFFIXES = (
    "nilm_metadata/__init__.py",
    "nilm_metadata/central_metadata/country.yaml",
    "nilm_metadata/central_metadata/appliance_types/appliance.yaml",
    "nilm_metadata/central_metadata/appliance_types/commercial.yaml",
)

REQUIRED_SDIST_SUFFIXES = (
    "README.md",
    "pyproject.toml",
    "docs/source/index.rst",
    "nilm_metadata/central_metadata/country.yaml",
    "nilm_metadata/central_metadata/appliance_types/appliance.yaml",
)


def require_suffixes(names: set[str], suffixes: tuple[str, ...], label: str) -> list[str]:
    return [f"{label} is missing {suffix}" for suffix in suffixes if not any(name.endswith(suffix) for name in names)]


def main() -> int:
    directory = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    wheels = sorted(directory.glob("*.whl"))
    sdists = sorted(directory.glob("*.tar.gz"))
    errors: list[str] = []

    if len(wheels) != 1:
        errors.append(f"expected one wheel in {directory}, found {len(wheels)}")
    if len(sdists) != 1:
        errors.append(f"expected one source distribution in {directory}, found {len(sdists)}")

    if len(wheels) == 1:
        with zipfile.ZipFile(wheels[0]) as archive:
            wheel_names = set(archive.namelist())
        errors.extend(require_suffixes(wheel_names, REQUIRED_WHEEL_SUFFIXES, "wheel"))
        if any(name.startswith("nilm_metadata/tests/") for name in wheel_names):
            errors.append("wheel must not contain the repository test suite")

    if len(sdists) == 1:
        with tarfile.open(sdists[0], "r:gz") as archive:
            sdist_names = set(archive.getnames())
        errors.extend(require_suffixes(sdist_names, REQUIRED_SDIST_SUFFIXES, "sdist"))

    if errors:
        print("Distribution checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Distribution checks passed: {wheels[0].name} and {sdists[0].name} "
        "contain package data and documentation."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
