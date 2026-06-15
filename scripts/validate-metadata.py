#!/usr/bin/env python3
"""Validate the minimum child-repository metadata required by ip-catalog."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
IP_YAML = ROOT / "ip.yaml"
UID = "ip-000021"
REPO_NAME = "apb-quad-spi-master-controller"
REPOSITORY = "https://github.com/openecos-projects/apb-quad-spi-master-controller"
MIRROR_POLICIES = {
    "reference-only",
    "source-mirror",
    "patched-mirror",
    "wrapper-only",
}


def require_value(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            raise ValueError(f"missing required field: {path}")
        current = current[key]
    if current in (None, "", []):
        raise ValueError(f"field must not be empty: {path}")
    return current


def main() -> None:
    with IP_YAML.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        raise ValueError("ip.yaml must contain a mapping at document root")

    for field in (
        "uid",
        "repo_name",
        "slug",
        "display_name",
        "summary",
        "category",
        "ip_family",
        "implementation_style",
        "links.catalog_repository",
        "links.repository",
        "upstream.owner",
        "upstream.repository",
        "upstream.author",
        "technical.languages",
        "technical.interfaces",
        "technical.top_modules",
        "legal.license",
        "legal.license_risk",
        "quality.maturity",
        "internal.status",
        "metadata.first_seen_at",
        "metadata.last_reviewed_at",
    ):
        require_value(data, field)

    if data["uid"] != UID:
        raise ValueError(f"uid must be {UID}")
    if data["repo_name"] != REPO_NAME:
        raise ValueError(f"repo_name must be {REPO_NAME}")
    if data["slug"] != REPO_NAME:
        raise ValueError(f"slug must be {REPO_NAME}")
    if data["links"]["repository"] != REPOSITORY:
        raise ValueError(f"repository link must reference {REPOSITORY}")
    if data["upstream"].get("sync_policy") != "none":
        raise ValueError("upstream.sync_policy must remain none")
    if data["internal"].get("mirror_policy") not in MIRROR_POLICIES:
        raise ValueError("internal.mirror_policy must use an allowed value")
    if "apb_spi_master" not in data["technical"]["top_modules"]:
        raise ValueError("technical.top_modules must include apb_spi_master")

    print("metadata validation passed")


if __name__ == "__main__":
    main()
