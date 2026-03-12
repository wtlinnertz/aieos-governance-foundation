"""Test cross-reference integrity between AIEOS kits.

Validates:
- Boundary contracts: entry-from files exist for declared dependencies
- Entry-from files reference the expected upstream artifacts
- Governance model copies are identical to the canonical version
- Four-file completeness for all artifact types
- Spec-version drift: templates reference current spec versions
- Template provenance: Document Control has Spec Version and Principles Version fields
"""

from __future__ import annotations

import re
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


class TestSpecVersionDrift:
    """Templates must reference current spec versions and include provenance fields.

    Human-authored intake forms (context templates, intake templates, product-brief,
    escalation records) are excluded — they don't have Document Control sections by
    design. Only AI-generated artifact templates are checked.
    """

    # Templates that are human-authored intake forms or auxiliary records.
    # These don't have Document Control with Spec Version by design.
    INTAKE_TEMPLATE_PATTERNS = (
        "context-template",    # architecture-context, design-context, system-context
        "intake-template",     # incident-intake, release-context-intake, service-reliability-intake
        "brief-template",      # product-brief
        "escalation-template", # bat-escalation
        "adr-template",        # ADRs are standalone records, no spec
    )

    # Spec types that are human-authored entry gates or intake forms.
    # These intentionally don't have prompt files.
    HUMAN_AUTHORED_SPEC_TYPES = {
        "kit-entry",           # KER — human entry gate
        "discovery-intake",    # DI — human intake form
        "dor",                 # Definition of Ready — human checklist
        "execution",           # Execution tracking — human-managed
        "dcr",                 # DCR — human incident declaration
        "qaer",                # QAER — human entry gate
        "release-entry",       # RER — human entry gate
        "srer",                # SRER — human entry gate
    }

    def _is_intake_template(self, filename: str) -> bool:
        return any(pattern in filename for pattern in self.INTAKE_TEMPLATE_PATTERNS)

    def test_generated_templates_have_spec_version(self, parsed_kits, aieos_root: Path):
        """AI-generated artifact templates should have a Spec Version field."""
        missing = []
        for kit_name, kit in parsed_kits.items():
            artifacts_dir = Path(kit.directory) / "docs" / "artifacts"
            if not artifacts_dir.is_dir():
                continue
            for template_file in sorted(artifacts_dir.glob("*-template.md")):
                if self._is_intake_template(template_file.name):
                    continue
                content = template_file.read_text(encoding="utf-8")
                has_spec_version = (
                    re.search(r"[Ss]pec\s+[Vv]ersion", content) is not None
                )
                if not has_spec_version:
                    missing.append(f"{kit_name}: {template_file.name}")
        assert missing == [], (
            f"Generated templates missing Spec Version in Document Control:\n" +
            "\n".join(f"  - {m}" for m in missing)
        )

    def test_generated_templates_have_principles_version(self, parsed_kits, aieos_root: Path):
        """Generated templates in kits with principles files should have Principles Version."""
        missing = []
        for kit_name, kit in parsed_kits.items():
            kit_path = Path(kit.directory)
            principles_dir = kit_path / "docs" / "principles"
            principles_root = list(kit_path.glob("docs/*-principles.md"))
            has_principles = (
                (principles_dir.is_dir() and any(principles_dir.glob("*.md")))
                or len(principles_root) > 0
            )
            if not has_principles:
                continue
            artifacts_dir = kit_path / "docs" / "artifacts"
            if not artifacts_dir.is_dir():
                continue
            for template_file in sorted(artifacts_dir.glob("*-template.md")):
                if self._is_intake_template(template_file.name):
                    continue
                content = template_file.read_text(encoding="utf-8")
                has_principles_version = (
                    re.search(r"[Pp]rinciples\s+[Vv]ersion", content) is not None
                )
                if not has_principles_version:
                    missing.append(f"{kit_name}: {template_file.name}")
        assert missing == [], (
            f"Generated templates missing Principles Version (kit has principles):\n" +
            "\n".join(f"  - {m}" for m in missing)
        )

    def test_spec_versions_are_valid_format(self, parsed_kits):
        """All spec version fields should follow vN.N format."""
        invalid = []
        for kit_name, kit in parsed_kits.items():
            for spec in kit.specs:
                if spec.version and not re.match(r"^v\d+\.\d+$", spec.version):
                    invalid.append(
                        f"{kit_name}: {spec.artifact_type}-spec.md has "
                        f"invalid version format '{spec.version}'"
                    )
        assert invalid == [], (
            f"Invalid spec version formats:\n" +
            "\n".join(f"  - {i}" for i in invalid)
        )

    def test_generated_specs_have_prompt(self, parsed_kits):
        """AI-generated artifact specs should have a matching prompt file."""
        missing = []
        for kit_name, kit in parsed_kits.items():
            for spec in kit.specs:
                if spec.artifact_type in self.HUMAN_AUTHORED_SPEC_TYPES:
                    continue
                expected_prompt = f"{spec.artifact_type}-prompt.md"
                if expected_prompt not in kit.prompts:
                    missing.append(f"{kit_name}: {expected_prompt}")
        assert missing == [], (
            f"Generated artifact specs missing prompt (four-file violation):\n" +
            "\n".join(f"  - {m}" for m in missing)
        )


class TestToolFourFileCompleteness:
    """Every tool spec in docs/tools/ must have a matching template, prompt, and validator."""

    def test_every_tool_spec_has_template(self, parsed_kits):
        missing = []
        for kit_name, kit in parsed_kits.items():
            for tool in kit.tool_specs:
                expected = f"{tool.tool_name}-template.md"
                if expected not in kit.tool_templates:
                    missing.append(f"{kit_name}: {expected}")
        assert missing == [], (
            f"Missing tool templates (four-file violation):\n" +
            "\n".join(f"  - {m}" for m in missing)
        )

    def test_every_tool_spec_has_prompt(self, parsed_kits):
        missing = []
        for kit_name, kit in parsed_kits.items():
            for tool in kit.tool_specs:
                expected = f"{tool.tool_name}-prompt.md"
                if expected not in kit.tool_prompts:
                    missing.append(f"{kit_name}: {expected}")
        assert missing == [], (
            f"Missing tool prompts (four-file violation):\n" +
            "\n".join(f"  - {m}" for m in missing)
        )

    def test_every_tool_spec_has_validator(self, parsed_kits):
        missing = []
        for kit_name, kit in parsed_kits.items():
            for tool in kit.tool_specs:
                expected = f"{tool.tool_name}-validator.md"
                if expected not in kit.tool_validators:
                    missing.append(f"{kit_name}: {expected}")
        assert missing == [], (
            f"Missing tool validators (four-file violation):\n" +
            "\n".join(f"  - {m}" for m in missing)
        )

    def test_tool_specs_have_version(self, parsed_kits):
        """All tool specs should have a Version field."""
        missing = []
        for kit_name, kit in parsed_kits.items():
            for tool in kit.tool_specs:
                if not tool.version:
                    missing.append(f"{kit_name}: {tool.tool_name}-spec.md")
        assert missing == [], (
            f"Tool specs missing Version field:\n" +
            "\n".join(f"  - {m}" for m in missing)
        )
