"""Regression tests for the kit-ci Document Control completeness assertion (D5).

The assertion is an inline ``run`` script in ``.github/workflows/kit-ci.yml``.
These tests extract the ACTUAL step script from the workflow file and execute
it against fixture kits, so the shipped logic is what is tested — there is no
duplicated copy that can drift (G-2: "no silent caps").
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "kit-ci.yml"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "doc-control"
STEP_NAME = "Document Control completeness assertion (D5)"


def _find_bash() -> str | None:
    # Prefer Git Bash on Windows — the System32 WSL shim errors without a
    # registered distro. Elsewhere the which() lookup wins.
    for cand in (
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files\Git\usr\bin\bash.exe",
    ):
        if Path(cand).exists():
            return cand
    return shutil.which("bash")


BASH = _find_bash()
pytestmark = pytest.mark.skipif(BASH is None, reason="bash not on PATH")


def _step_script() -> str:
    wf = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    for step in wf["jobs"]["kit-ci"]["steps"]:
        if step.get("name") == STEP_NAME:
            return step["run"]
    raise AssertionError(f"step {STEP_NAME!r} not found in {WORKFLOW}")


def _run(fixture: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [BASH, "-c", _step_script()],
        cwd=FIXTURES / fixture,
        capture_output=True,
        text=True,
    )


def test_step_present_in_workflow():
    assert "| Artifact ID |" in _step_script()


def test_conformant_kit_passes():
    proc = _run("good-kit")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_exempt_template_without_block_is_not_flagged():
    # good-kit carries adr-template.md (D4 exempt) with no Artifact ID row.
    proc = _run("good-kit")
    assert proc.returncode == 0
    assert "adr-template.md" not in proc.stdout


def test_later_status_column_table_is_tolerated():
    # good-kit's sad-template.md has a Status-labelled column table AFTER the
    # Document Control block — first match is still the DRAFT row.
    proc = _run("good-kit")
    assert proc.returncode == 0
    assert "sad-template.md" not in proc.stdout


def test_missing_artifact_id_fails_and_names_only_the_offender():
    proc = _run("missing-row-kit")
    assert proc.returncode == 1
    assert "prd-template.md" in proc.stdout
    assert "tdd-template.md" not in proc.stdout


def test_status_row_shadowing_document_control_fails():
    proc = _run("bad-order-kit")
    assert proc.returncode == 1
    assert "FIRST '| Status |' row" in proc.stdout
    assert "rr-template.md" in proc.stdout
