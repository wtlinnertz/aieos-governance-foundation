#!/usr/bin/env python3
"""Generate the cross-language convention conformance fixture (M1, FR-023).

Reads kit-manifest.yml + schema/artifact-file-convention.yaml and emits
tests/fixtures/convention/expected-files.json: for every (kit, artifact),
the exact repo-relative paths each deriver must resolve. Both the Python
suite (gf/harness) and the TypeScript suite (console) assert against this
file, so a convention or manifest change that drifts one deriver fails CI.

Usage:
    python scripts/generate-convention-fixture.py          # write fixture
    python scripts/generate-convention-fixture.py --check  # diff only, exit 1 on drift
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "kit-manifest.yml"
CONVENTION = ROOT / "schema" / "artifact-file-convention.yaml"
FIXTURE = ROOT / "tests" / "fixtures" / "convention" / "expected-files.json"


def build_fixture() -> dict:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    convention = yaml.safe_load(CONVENTION.read_text(encoding="utf-8"))

    strip = convention["token"]["strip_suffix"]
    files = convention["files"]
    out = {
        "convention_version": convention["convention_version"],
        "manifest_version": manifest["manifest_version"],
        "kits": {},
    }
    for abbr, kit in manifest["kits"].items():
        entries = []
        for art in kit["artifacts"]:
            token = art["spec_file"]
            if token.endswith(strip):
                token = token[: -len(strip)]
            expected = {}
            for name, spec in files.items():
                if spec["required"] == "unless_human_authored" and art.get("human_authored"):
                    continue
                expected[name] = spec["path"].replace("{token}", token)
            entries.append(
                {
                    "id": art["id"],
                    "token": token,
                    "human_authored": bool(art.get("human_authored", False)),
                    "files": expected,
                    "output": convention["output"]["path"].replace("{token}", token),
                }
            )
        out["kits"][abbr] = {"repository": kit["repository"], "artifacts": entries}
    return out


def main(argv: list[str]) -> int:
    fixture = build_fixture()
    rendered = json.dumps(fixture, indent=2, sort_keys=True) + "\n"
    if "--check" in argv:
        if not FIXTURE.exists() or FIXTURE.read_text(encoding="utf-8") != rendered:
            print(
                "convention fixture is stale — run "
                "`python scripts/generate-convention-fixture.py`",
                file=sys.stderr,
            )
            return 1
        print("convention fixture up to date")
        return 0
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(rendered, encoding="utf-8")
    total = sum(len(k["artifacts"]) for k in fixture["kits"].values())
    print(f"wrote {FIXTURE.relative_to(ROOT)} ({len(fixture['kits'])} kits, {total} artifacts)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
