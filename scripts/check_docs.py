#!/usr/bin/env python3
"""Check the public onboarding and central metadata index."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

from nilm_metadata import get_appliance_types


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
APPLIANCE_DIR = ROOT / "nilm_metadata" / "central_metadata" / "appliance_types"

REQUIRED_TEXT = (
    "Dataset conversion, meter access, preprocessing, and metrics",
    "Appliance taxonomy, synonyms, meter relationships, and dataset schema",
    "Disaggregation model implementation and testing",
    "Fixed T1/T2/T3 evaluation and published result bundles",
    "https://nilmtk.github.io/",
    "https://github.com/nilmtk/nilmtk",
    "https://github.com/nilmtk/nilmtk-contrib",
    "https://github.com/nilmtk/nilmbench",
    "https://nilm-metadata.readthedocs.io/en/latest/tutorial.html",
    "uv venv --python 3.11",
    '"nilm-metadata @ git+https://github.com/nilmtk/nilm_metadata.git"',
    '"nilm-metadata[hdf5] @ git+https://github.com/nilmtk/nilm_metadata.git"',
    "There is no metadata-only Docker image.",
    "https://doi.org/10.1109/COMPSACW.2014.97",
)

FORBIDDEN_TEXT = (
    "nilm-metadata.readthedocs.org",
    "non-instrusive",
    "JSON Schema has been depreciated",
    "uv pip install git+https://github.com/nilmtk/nilm_metadata.git",
)

MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def check_local_links(source: str, errors: list[str]) -> int:
    checked = 0
    for raw_target in MARKDOWN_LINK.findall(source):
        target = raw_target.split(maxsplit=1)[0].strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or target.startswith(("#", "mailto:", "tel:")):
            continue
        checked += 1
        path = (ROOT / unquote(parsed.path)).resolve()
        if not path.exists():
            errors.append(f"README.md has a missing local link: {target}")
    return checked


def read_central_types(errors: list[str]) -> set[str]:
    names: set[str] = set()
    for path in sorted(APPLIANCE_DIR.glob("*.yaml")):
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            errors.append(f"{path.relative_to(ROOT)} must contain a YAML mapping")
            continue
        duplicates = names.intersection(document)
        if duplicates:
            errors.append(
                f"duplicate appliance types in {path.relative_to(ROOT)}: "
                + ", ".join(sorted(duplicates))
            )
        names.update(document)
    return names


def main() -> int:
    source = README.read_text(encoding="utf-8")
    normalized = " ".join(source.split())
    errors: list[str] = []

    if source.count("```") % 2:
        errors.append("README.md has an unclosed code fence")
    if "http://" in source:
        errors.append("README.md contains an insecure URL")

    for required in REQUIRED_TEXT:
        if required not in normalized:
            errors.append(f"README.md is missing required text: {required}")
    for forbidden in FORBIDDEN_TEXT:
        if forbidden in source:
            errors.append(f"README.md contains retired text: {forbidden}")

    checked_links = check_local_links(source, errors)

    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
        "project"
    ]
    extras = project.get("optional-dependencies", {})
    if not any(requirement.startswith("tables") for requirement in extras.get("hdf5", [])):
        errors.append("the hdf5 extra must install PyTables")
    for dependency in ("furo", "pytest", "sphinx"):
        if not any(
            requirement.lower().startswith(dependency)
            for requirement in extras.get("dev", [])
        ):
            errors.append(f"the dev extra must install {dependency}")

    raw_types = read_central_types(errors)
    resolved_types = get_appliance_types()
    if set(resolved_types) != raw_types:
        errors.append("resolved appliance types do not match the YAML index")
    if resolved_types.get("fridge", {}).get("type") != "fridge":
        errors.append("the public fridge vocabulary smoke check failed")

    docs_index = (ROOT / "docs" / "source" / "index.rst").read_text(encoding="utf-8")
    if "This project defines metadata." not in docs_index:
        errors.append("the documentation home page does not state the repository boundary")
    docs_config = (ROOT / "docs" / "source" / "conf.py").read_text(encoding="utf-8")
    if "html_theme = 'furo'" not in docs_config:
        errors.append("the documentation must use the responsive Furo theme")

    if errors:
        print("Documentation checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Documentation checks passed: "
        f"{len(REQUIRED_TEXT)} contract clauses, {checked_links} local links, "
        f"{len(raw_types)} appliance types."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
