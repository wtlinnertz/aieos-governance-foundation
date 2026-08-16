"""Tests for scripts/check-calibration-lock.py (FR-014 slice 3).

Runs the script as a subprocess (its real CI invocation shape). All
fixtures are built in tmp_path; no LLM, no network, stdlib-only script.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "check-calibration-lock.py"

PROMPT_TEXT = "You are an AI quality gate.\nEvaluate the SAD.\n"


def _sha(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _run(kit_root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(kit_root)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


@pytest.fixture()
def kit(tmp_path: Path) -> Path:
    validators = tmp_path / "docs" / "validators"
    validators.mkdir(parents=True)
    (validators / "sad-validator.md").write_text(
        PROMPT_TEXT, encoding="utf-8", newline="\n"
    )
    return tmp_path


def _write_lock(kit_root: Path, prompt_sha: str, validator: str = "sad-validator") -> None:
    lock = {
        "lock_version": "1.0",
        "validators": {
            validator: {
                "prompt_sha256": prompt_sha,
                "model": "claude-sonnet-4-20250514",
                "gate_agreement": 0.95,
                "false_pass_count": 0,
                "calibrated_at": "2026-08-15T00:00:00Z",
                "report_ref": "tests/gold/sad/reports/sad-validator-2026-08-15.json",
            }
        },
    }
    (kit_root / "calibration.lock").write_text(
        json.dumps(lock, indent=2), encoding="utf-8", newline="\n"
    )


class TestNoLock:
    def test_missing_lock_is_adoption_gated_ok(self, kit: Path) -> None:
        result = _run(kit)
        assert result.returncode == 0
        assert "not yet adopted" in result.stdout


class TestFreshLock:
    def test_matching_sha_is_fresh(self, kit: Path) -> None:
        _write_lock(kit, _sha(PROMPT_TEXT))
        result = _run(kit)
        assert result.returncode == 0
        assert "OK: sad-validator" in result.stdout

    def test_crlf_working_copy_still_fresh(self, kit: Path) -> None:
        # autocrlf checkout: prompt on disk is CRLF, pin was computed on LF.
        prompt = kit / "docs" / "validators" / "sad-validator.md"
        prompt.write_bytes(PROMPT_TEXT.replace("\n", "\r\n").encode("utf-8"))
        _write_lock(kit, _sha(PROMPT_TEXT))
        result = _run(kit)
        assert result.returncode == 0, result.stdout

    def test_suffixless_lock_entry_resolves(self, kit: Path) -> None:
        _write_lock(kit, _sha(PROMPT_TEXT), validator="sad")
        result = _run(kit)
        assert result.returncode == 0
        assert "OK: sad" in result.stdout


class TestStaleLock:
    def test_edited_prompt_is_stale(self, kit: Path) -> None:
        _write_lock(kit, _sha(PROMPT_TEXT))
        prompt = kit / "docs" / "validators" / "sad-validator.md"
        prompt.write_text(PROMPT_TEXT + "New rule.\n", encoding="utf-8", newline="\n")
        result = _run(kit)
        assert result.returncode == 1
        assert "STALE: sad-validator" in result.stdout
        assert "recalibration required" in result.stdout

    def test_missing_prompt_file_is_stale(self, kit: Path) -> None:
        _write_lock(kit, _sha(PROMPT_TEXT), validator="tdd-validator")
        result = _run(kit)
        assert result.returncode == 1
        assert "no prompt file" in result.stdout

    def test_entry_without_sha_is_stale(self, kit: Path) -> None:
        lock = {"lock_version": "1.0", "validators": {"sad-validator": {"model": "m"}}}
        (kit / "calibration.lock").write_text(
            json.dumps(lock), encoding="utf-8", newline="\n"
        )
        result = _run(kit)
        assert result.returncode == 1
        assert "no prompt_sha256" in result.stdout


class TestMalformedLock:
    def test_invalid_json_fails(self, kit: Path) -> None:
        (kit / "calibration.lock").write_text("{not json", encoding="utf-8", newline="\n")
        result = _run(kit)
        assert result.returncode == 1
        assert "malformed" in result.stdout

    def test_validators_not_a_map_fails(self, kit: Path) -> None:
        (kit / "calibration.lock").write_text(
            json.dumps({"lock_version": "1.0", "validators": []}),
            encoding="utf-8",
            newline="\n",
        )
        result = _run(kit)
        assert result.returncode == 1
        assert "malformed" in result.stdout
