"""Test cross-reference integrity between AIEOS kits.

Validates:
- Boundary contracts: entry-from files exist for declared dependencies
- Entry-from files reference the expected upstream artifacts
- Governance model copies are identical to the canonical version
- Four-file completeness for all artifact types
"""

from __future__ import annotations

from pathlib import Path

import pytest

from models.framework import BOUNDARY_CONTRACTS, KIT_REGISTRY
from parsers.kit_parser import KitStructure


class TestBoundaryContracts:
    """Entry-from files must exist for all declared cross-kit dependencies."""

    def test_entry_files_exist(self, parsed_kits, aieos_root: Path):
        missing = []
        for (kit_abbrev, upstream_suffix), expected_artifacts in BOUNDARY_CONTRACTS.items():
            kit_info = KIT_REGISTRY.get(kit_abbrev)
            if not kit_info:
                missing.append(f"Unknown kit: {kit_abbrev}")
                continue
            entry_file = aieos_root / kit_info.directory / "docs" / f"entry-from-{upstream_suffix}.md"
            if not entry_file.is_file():
                missing.append(
                    f"{kit_info.directory}/docs/entry-from-{upstream_suffix}.md"
                )
        assert missing == [], (
            f"Missing entry-from files:\n" +
            "\n".join(f"  - {m}" for m in missing)
        )

    def test_entry_files_reference_upstream_artifacts(self, parsed_kits, aieos_root: Path):
        """Entry-from files should mention the expected upstream artifacts."""
        issues = []
        for (kit_abbrev, upstream_suffix), expected_artifacts in BOUNDARY_CONTRACTS.items():
            kit_info = KIT_REGISTRY.get(kit_abbrev)
            if not kit_info:
                continue
            entry_file = aieos_root / kit_info.directory / "docs" / f"entry-from-{upstream_suffix}.md"
            if not entry_file.is_file():
                continue
            content = entry_file.read_text(encoding="utf-8").upper()
            for artifact in expected_artifacts:
                if artifact.upper() not in content:
                    issues.append(
                        f"{kit_info.directory}/entry-from-{upstream_suffix}.md "
                        f"does not mention '{artifact}'"
                    )
        assert issues == [], (
            f"Boundary contract mismatches:\n" +
            "\n".join(f"  - {i}" for i in issues)
        )


class TestGovernanceModelSync:
    """All kit copies of governance-model.md must match the canonical version."""

    def test_governance_model_identical(self, parsed_kits, aieos_root: Path):
        canonical = aieos_root / "aieos-governance-foundation" / "governance-model.md"
        if not canonical.is_file():
            pytest.skip("Canonical governance-model.md not found")

        canonical_content = canonical.read_text(encoding="utf-8")
        mismatches = []

        for kit_name, kit in parsed_kits.items():
            if kit_name == "aieos-governance-foundation":
                continue
            kit_gm = Path(kit.directory) / "docs" / "governance-model.md"
            if not kit_gm.is_file():
                mismatches.append(f"{kit_name}: governance-model.md missing")
                continue
            kit_content = kit_gm.read_text(encoding="utf-8")
            if kit_content != canonical_content:
                mismatches.append(f"{kit_name}: governance-model.md differs from canonical")

        assert mismatches == [], (
            f"Governance model sync failures:\n" +
            "\n".join(f"  - {m}" for m in mismatches)
        )


class TestFourFileCompleteness:
    """Every spec must have a matching template and validator."""

    def test_every_spec_has_template(self, parsed_kits):
        missing = []
        for kit_name, kit in parsed_kits.items():
            for spec in kit.specs:
                expected_template = f"{spec.artifact_type}-template.md"
                if expected_template not in kit.templates:
                    missing.append(f"{kit_name}: {expected_template}")
        assert missing == [], (
            f"Missing templates (four-file violation):\n" +
            "\n".join(f"  - {m}" for m in missing)
        )

    def test_every_spec_has_validator(self, parsed_kits):
        missing = []
        for kit_name, kit in parsed_kits.items():
            for spec in kit.specs:
                expected_validator = f"{spec.artifact_type}-validator.md"
                if expected_validator not in kit.validators:
                    missing.append(f"{kit_name}: {expected_validator}")
        assert missing == [], (
            f"Missing validators (four-file violation):\n" +
            "\n".join(f"  - {m}" for m in missing)
        )

    def test_specs_have_version(self, parsed_kits):
        """All specs should have a Version field."""
        missing_version = []
        for kit_name, kit in parsed_kits.items():
            for spec in kit.specs:
                if not spec.version:
                    missing_version.append(f"{kit_name}: {spec.artifact_type}-spec.md")
        assert missing_version == [], (
            f"Specs missing Version field:\n" +
            "\n".join(f"  - {m}" for m in missing_version)
        )


class TestPlaybookPresence:
    """Every kit must have a playbook."""

    def test_all_kits_have_playbook(self, parsed_kits):
        missing = [
            name for name, kit in parsed_kits.items()
            if not kit.has_playbook and name != "aieos-governance-foundation"
        ]
        assert missing == [], f"Kits missing playbook.md: {missing}"

    def test_all_kits_have_claude_md(self, parsed_kits):
        missing = [
            name for name, kit in parsed_kits.items()
            if not kit.has_claude_md and name != "aieos-governance-foundation"
        ]
        assert missing == [], f"Kits missing CLAUDE.md: {missing}"
