#!/usr/bin/env python3
"""Deterministic calibration.lock staleness check (FR-014 slice 3).

Kit-CI's half of judge-calibration governance: compare each validator's
live prompt file against the sha pinned in the kit's ``calibration.lock``.
String hashing only -- this path never builds an adapter and never calls
an LLM (constraint ``hash_compare_only`` in
``aieos-schema/schema/calibration-lock.yaml``). The expensive gold-set
run happens only via ``harness calibrate`` on its three triggers (model
change, prompt change, schedule).

Scope note: kit CI can check the PROMPT half of staleness only. The
MODEL half lives in harness config, which a kit checkout does not have;
the harness (``--check-only``) and the dark-factory conductor
(slice 4 precondition) check both halves.

Adoption-gated by design: a kit without a ``calibration.lock`` exits 0
with a note. Calibration coverage arrives per-validator; absence is not
failure at the kit-CI layer (the conductor is stricter for unattended
walks, per ratified decision 6).

Hashing MUST match the harness (``src/calibration.py``): decode utf-8,
normalize CRLF/CR to LF, sha256. Python text-mode reads already apply
universal newlines, but we normalize explicitly so the result is
byte-for-byte identical regardless of how the file was checked out
(autocrlf working copies -- the G-19 lesson).

Usage:
    python3 check-calibration-lock.py <kit-root>

Exit codes:
    0 -- no lock present (adoption-gated no-op) or every entry fresh
    1 -- stale entry, missing prompt file, or malformed lock
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def _prompt_sha256(path: Path) -> str:
    text = path.read_bytes().decode("utf-8")
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _resolve_prompt_file(kit_root: Path, validator: str) -> Path | None:
    """Locate the validator prompt file for a lock entry.

    Convention: ``docs/validators/<validator>.md``. A lock entry may name
    the validator with or without the ``-validator`` suffix; try both
    spellings (the harness CLI does the same -- unify in a later slice).
    """
    candidates = [
        kit_root / "docs" / "validators" / f"{validator}.md",
    ]
    if not validator.endswith("-validator"):
        candidates.append(kit_root / "docs" / "validators" / f"{validator}-validator.md")
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check-calibration-lock.py <kit-root>", file=sys.stderr)
        return 1
    kit_root = Path(argv[1])
    lock_path = kit_root / "calibration.lock"

    if not lock_path.is_file():
        print("calibration.lock not present -- calibration not yet adopted for this kit (OK)")
        return 0

    try:
        lock = json.loads(lock_path.read_bytes().decode("utf-8"))
        validators = lock["validators"]
        if not isinstance(validators, dict):
            raise TypeError("validators is not a map")
    except Exception as exc:  # malformed lock is a hard failure, not a skip
        print(f"STALE: calibration.lock is malformed ({exc})")
        return 1

    failures = 0
    for validator, entry in sorted(validators.items()):
        pinned = str(entry.get("prompt_sha256", "")).strip().lower()
        if not pinned:
            print(f"STALE: {validator} -- lock entry has no prompt_sha256")
            failures += 1
            continue
        prompt_file = _resolve_prompt_file(kit_root, validator)
        if prompt_file is None:
            print(f"STALE: {validator} -- no prompt file under docs/validators/")
            failures += 1
            continue
        live = _prompt_sha256(prompt_file)
        if live != pinned:
            print(
                f"STALE: {validator} -- prompt changed since calibration "
                f"(pinned {pinned[:12]}..., live {live[:12]}...); "
                f"recalibration required (harness calibrate)"
            )
            failures += 1
        else:
            print(f"OK: {validator} (prompt {live[:12]}..., calibrated {entry.get('calibrated_at', '?')})")

    if failures:
        print(f"{failures} stale calibration entr{'y' if failures == 1 else 'ies'}")
        return 1
    print(f"all {len(validators)} calibration entr{'y' if len(validators) == 1 else 'ies'} fresh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
