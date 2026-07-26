"""FR-023 contract tests: manifest schema + artifact-file-convention fixture.

Three layers of protection (M1/M2):
  1. kit-manifest.yml validates against the single declared JSON Schema.
  2. The cross-language conformance fixture is fresh (regenerated == committed),
     so a manifest/convention change cannot silently drift past consumers.
  3. (cross_repo) every expected file resolves on disk across the sibling
     kit checkouts — the R2 gating scan as a permanent test.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "kit-manifest.yml"
SCHEMA = ROOT / "schema" / "kit-manifest.schema.json"
FIXTURE = ROOT / "tests" / "fixtures" / "convention" / "expected-files.json"

# The nine artifacts whose token diverges from id.lower() — the reason the
# convention derives from spec_file (R1 correction, scan-proven 2026-07-25).
DIVERGENT_TOKENS = {
    ("PIK", "WCR"): "work-classification",
    ("PIK", "DI"): "discovery-intake",
    ("PIK", "PFD"): "problem-framing",
    ("PIK", "VH"): "value-hypothesis",
    ("PIK", "AR"): "assumption-register",
    ("PIK", "EL"): "experiment-log",
    ("PIK", "DPRD"): "discovery-prd",
    ("EEK", "KER"): "kit-entry",
    ("REK", "RER"): "release-entry",
}


def _load_generator():
    spec = importlib.util.spec_from_file_location(
        "generate_convention_fixture",
        ROOT / "scripts" / "generate-convention-fixture.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def manifest():
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_manifest_validates_against_declared_schema(manifest):
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(manifest), key=lambda e: list(e.path)
    )
    assert not errors, "\n".join(
        f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors[:10]
    )


def test_fixture_is_fresh():
    gen = _load_generator()
    rendered = json.dumps(gen.build_fixture(), indent=2, sort_keys=True) + "\n"
    assert FIXTURE.exists(), "fixture missing — run scripts/generate-convention-fixture.py"
    assert FIXTURE.read_text(encoding="utf-8") == rendered, (
        "fixture stale — run scripts/generate-convention-fixture.py"
    )


def test_divergent_tokens_locked(fixture):
    for (abbr, art_id), token in DIVERGENT_TOKENS.items():
        entry = next(
            a for a in fixture["kits"][abbr]["artifacts"] if a["id"] == art_id
        )
        assert entry["token"] == token, f"{abbr}/{art_id}"
        assert entry["token"] != art_id.lower()


def test_human_authored_artifacts_have_no_prompt(fixture, manifest):
    for abbr, kit in manifest["kits"].items():
        for art in kit["artifacts"]:
            entry = next(
                a for a in fixture["kits"][abbr]["artifacts"] if a["id"] == art["id"]
            )
            assert ("prompt" in entry["files"]) == (not art.get("human_authored", False))
            assert "validator" in entry["files"], f"{abbr}/{art['id']}: validator is always required"


def test_g3_principles_inputs_declared(manifest):
    """G-3 lock: the five EEK artifact types whose prompts declare mandatory
    principles carry framework inputs in the manifest (manifest 1.1)."""
    eek = {a["id"]: a for a in manifest["kits"]["EEK"]["artifacts"]}
    for art_id in ("PRD", "ACF", "DCF", "DKR", "TDD"):
        inputs = eek[art_id].get("inputs", [])
        assert any(
            i["source"] == "framework" and i["role"] == "principles"
            for i in inputs
        ), f"EEK/{art_id} missing framework principles input"
    # G-5: PRD's Path B human brief rides the same mechanism.
    assert any(
        i["source"] == "human" and i["role"] == "brief"
        for i in eek["PRD"]["inputs"]
    )


@pytest.mark.cross_repo
def test_framework_input_refs_resolve_on_disk(manifest):
    """Every source=framework input ref (kit-relative) must exist — a
    declared principles file that is missing would fail generation."""
    kits_root = ROOT.parent
    missing = []
    for abbr, kit in manifest["kits"].items():
        repo = kits_root / kit["repository"]
        if not repo.is_dir():
            pytest.skip(f"sibling checkout missing: {kit['repository']}")
        for art in kit["artifacts"]:
            for inp in art.get("inputs", []):
                if inp["source"] == "framework" and not (repo / inp["ref"]).is_file():
                    missing.append(f"{abbr}/{art['id']}: {inp['ref']}")
    assert not missing, "\n".join(missing)


@pytest.mark.cross_repo
def test_every_expected_file_resolves_on_disk(fixture):
    """The R2 gating scan, permanent: 244/244 under the corrected token rule."""
    kits_root = ROOT.parent
    missing = []
    for abbr, kit in fixture["kits"].items():
        repo = kits_root / kit["repository"]
        if not repo.is_dir():
            pytest.skip(f"sibling checkout missing: {kit['repository']}")
        for art in kit["artifacts"]:
            for name, rel in art["files"].items():
                if not (repo / rel).is_file():
                    missing.append(f"{abbr}/{art['id']}: {rel}")
    assert not missing, "\n".join(missing)
