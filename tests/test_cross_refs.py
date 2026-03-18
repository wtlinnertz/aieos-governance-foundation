"""Test cross-reference integrity between AIEOS kits.

Validates:
- Boundary contracts: entry-from files exist for declared dependencies
- Entry-from files reference the expected upstream artifacts
- Governance model copies are identical to the canonical version
- Four-file completeness for all artifact types
- Spec-version drift: templates reference current spec versions
- Template provenance: Document Control has Spec Version and Principles Version fields
- Sherpa skill: Critical Rules section contains required behavioral rules
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


class TestNavigationMapConsistency:
    """Navigation map nodes should exist for new artifacts in framework.py."""

    def test_smr_node_in_navigation_map(self, aieos_root: Path):
        nav_map = aieos_root / "aieos-governance-foundation" / "docs" / "navigation-map.md"
        content = nav_map.read_text(encoding="utf-8")
        assert "N-PINFK-SMR" in content, "SMR node missing from navigation map"

    def test_rsa_node_in_navigation_map(self, aieos_root: Path):
        nav_map = aieos_root / "aieos-governance-foundation" / "docs" / "navigation-map.md"
        content = nav_map.read_text(encoding="utf-8")
        assert "N-REK-RSA" in content, "RSA node missing from navigation map"

    def test_rsa_edge_in_navigation_map(self, aieos_root: Path):
        """Navigation map should show RSA between RCF and RP."""
        nav_map = aieos_root / "aieos-governance-foundation" / "docs" / "navigation-map.md"
        content = nav_map.read_text(encoding="utf-8")
        assert "N-REK-RCF" in content and "N-REK-RSA" in content, (
            "RCF→RSA edge nodes missing from navigation map"
        )

    def test_smr_edge_in_navigation_map(self, aieos_root: Path):
        """Navigation map should show ISPEC→SMR edge."""
        nav_map = aieos_root / "aieos-governance-foundation" / "docs" / "navigation-map.md"
        content = nav_map.read_text(encoding="utf-8")
        assert "E-121a" in content, "ISPEC→SMR edge (E-121a) missing from navigation map"


class TestPRKLensCount:
    """PRK should have exactly 13 review lens tools."""

    def test_prk_has_thirteen_lenses(self, parsed_kits):
        prk = parsed_kits.get("aieos-peer-review-kit")
        assert prk is not None, "PRK not found in parsed kits"
        lens_specs = [t for t in prk.tool_specs if t.tool_name.startswith("review-")]
        assert len(lens_specs) == 13, (
            f"Expected 13 review lens specs in PRK, found {len(lens_specs)}: "
            f"{[t.tool_name for t in lens_specs]}"
        )

    def test_observability_lens_exists(self, parsed_kits):
        prk = parsed_kits.get("aieos-peer-review-kit")
        assert prk is not None
        lens_names = [t.tool_name for t in prk.tool_specs]
        assert "review-observability" in lens_names, (
            "review-observability lens not found in PRK tools"
        )

    def test_resilience_lens_exists(self, parsed_kits):
        prk = parsed_kits.get("aieos-peer-review-kit")
        assert prk is not None
        lens_names = [t.tool_name for t in prk.tool_specs]
        assert "review-resilience" in lens_names, (
            "review-resilience lens not found in PRK tools"
        )

    def test_adversarial_lens_exists(self, parsed_kits):
        prk = parsed_kits.get("aieos-peer-review-kit")
        assert prk is not None
        lens_names = [t.tool_name for t in prk.tool_specs]
        assert "review-adversarial" in lens_names, (
            "review-adversarial lens not found in PRK tools"
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


class TestSherpaSkillCriticalRules:
    """Verify sherpa-skill.md Critical Rules section contains all required behavioral rules."""

    SHERPA_SKILL = Path("aieos-governance-foundation/docs/tools/sherpa-skill.md")

    @pytest.fixture
    def critical_rules(self):
        """Extract the Critical Rules section from sherpa-skill.md."""
        content = self.SHERPA_SKILL.read_text()
        match = re.search(
            r"## Critical Rules\n\n(.*?)(?:\n## |\Z)",
            content, re.DOTALL
        )
        assert match, "Critical Rules section not found in sherpa-skill.md"
        return match.group(1)

    def test_risk_scan_rule(self, critical_rules):
        """WS2 structured output: Risk scan must be in Critical Rules."""
        assert re.search(r'emit "Risk scan:"', critical_rules), \
            "Critical Rules missing: Risk scan structured output rule"

    def test_health_check_rule(self, critical_rules):
        """WS2 structured output: Health Check block must be in Critical Rules."""
        assert re.search(r"emit the Health Check block", critical_rules), \
            "Critical Rules missing: Health Check structured output rule"

    def test_consistency_rule(self, critical_rules):
        """WS2 structured output: Consistency line must be in Critical Rules."""
        assert re.search(r'emit "Consistency:"', critical_rules), \
            "Critical Rules missing: Consistency structured output rule"

    def test_position_check_rule(self, critical_rules):
        """WS2 structured output: Position check must be in Critical Rules."""
        assert re.search(r'emit "Position check:"', critical_rules), \
            "Critical Rules missing: Position check structured output rule"

    def test_boundary_check_rule(self, critical_rules):
        """WS2 structured output: Boundary check must be in Critical Rules."""
        assert re.search(r'emit "Boundary check:"', critical_rules), \
            "Critical Rules missing: Boundary check structured output rule"

    def test_no_permission_seeking_rule(self, critical_rules):
        """Broadened prohibition: Must cover Shall I and Want me to variants."""
        assert re.search(r"Shall I", critical_rules), \
            "Critical Rules missing: 'Shall I…?' in permission-seeking prohibition"
        assert re.search(r"Want me to", critical_rules), \
            "Critical Rules missing: 'Want me to…?' in permission-seeking prohibition"

    def test_intake_probe_rule(self, critical_rules):
        """Intake quality: Must require probing thin sections."""
        assert re.search(r"[Pp]robe thin intake", critical_rules), \
            "Critical Rules missing: intake quality probe rule"

    def test_critical_rules_count(self, critical_rules):
        """Critical Rules should have at least 17 bullet points."""
        bullets = re.findall(r"^- \*\*", critical_rules, re.MULTILINE)
        assert len(bullets) >= 17, (
            f"Critical Rules has {len(bullets)} bullets, expected >= 17"
        )


class TestSherpaSkillConversationalBehavior:
    """Verify sherpa-skill.md contains correct conversational behavior instructions."""

    SHERPA_SKILL = Path("aieos-governance-foundation/docs/tools/sherpa-skill.md")

    @pytest.fixture
    def content(self):
        return self.SHERPA_SKILL.read_text()

    def test_conditional_opening_question(self, content):
        """Getting Started must not force the stock question unconditionally."""
        # Must contain conditional logic for the opening question
        assert re.search(
            r"[Ii]f the user.s message already describes", content
        ), "Getting Started should conditionally skip stock opening question"
        assert re.search(
            r"[Oo]nly ask.*[Ww]hat are you trying to build", content
        ), "Getting Started should only ask stock question when user gives no indication"

    def test_intent_translation_first_response(self, content):
        """Step 1 must instruct front-loaded intent translation."""
        assert re.search(
            r"[Aa]pply Step 1a.*in your very first response", content
        ), "Step 1 should instruct applying intent translation in the first response"

    def test_broadened_flow_control_prohibition(self, content):
        """Flow control rule must cover Shall I and Want me to variants."""
        # Find the flow control rule section
        flow_match = re.search(
            r"Do NOT ask.*?confirmed flow\.", content, re.DOTALL
        )
        assert flow_match, "Flow control prohibition rule not found"
        flow_rule = flow_match.group(0)
        assert "Shall I validate" in flow_rule, \
            "Flow control rule missing 'Shall I validate?' variant"
        assert "Want me to generate" in flow_rule, \
            "Flow control rule missing 'Want me to generate...?' variant"

    def test_intake_probe_instruction(self, content):
        """Pre-population section must instruct probing thin intake sections."""
        assert re.search(
            r"fewer than 2 substantive sentences", content
        ), "Intake quality probe instruction missing from pre-population section"
        assert re.search(
            r"[Pp]robe once.*downstream", content
        ), "Intake probe should link gap to downstream impact"
