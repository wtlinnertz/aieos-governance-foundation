"""Parse AIEOS kit directories to extract structural information."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class EntryFromFile:
    """Parsed entry-from-{upstream}.md file."""
    kit_name: str
    upstream_suffix: str         # e.g., "eek", "rek", "rrk"
    file_path: str
    required_artifacts: list[str] = field(default_factory=list)
    first_artifact: str = ""


@dataclass
class SpecFile:
    """Parsed *-spec.md file metadata."""
    kit_name: str
    artifact_type: str           # e.g., "prd", "sad", "vp"
    file_path: str
    version: str = ""
    hard_gate_count: int = 0
    hard_gate_names: list[str] = field(default_factory=list)


@dataclass
class ToolSpec:
    """Parsed tool *-spec.md file metadata from docs/tools/."""
    kit_name: str
    tool_name: str            # e.g., "dependency-check", "spec-lookup"
    file_path: str
    version: str = ""
    hard_gate_count: int = 0
    hard_gate_names: list[str] = field(default_factory=list)


@dataclass
class KitStructure:
    """Complete parsed structure of an AIEOS kit."""
    name: str
    directory: str
    has_playbook: bool = False
    has_claude_md: bool = False
    has_governance_model: bool = False
    specs: list[SpecFile] = field(default_factory=list)
    entry_files: list[EntryFromFile] = field(default_factory=list)
    templates: list[str] = field(default_factory=list)
    prompts: list[str] = field(default_factory=list)
    validators: list[str] = field(default_factory=list)
    tool_specs: list[ToolSpec] = field(default_factory=list)
    tool_templates: list[str] = field(default_factory=list)
    tool_prompts: list[str] = field(default_factory=list)
    tool_validators: list[str] = field(default_factory=list)


def find_aieos_root() -> Path:
    """Find the AIEOS monorepo root by walking up from this file."""
    current = Path(__file__).resolve()
    while current != current.parent:
        if (current / "aieos-governance-foundation").is_dir():
            return current
        current = current.parent
    raise FileNotFoundError("Cannot find AIEOS root (directory containing aieos-governance-foundation)")


def discover_kits(aieos_root: Path) -> list[Path]:
    """Find all kit directories under the AIEOS root."""
    kits = []
    for entry in sorted(aieos_root.iterdir()):
        if entry.is_dir() and entry.name.startswith("aieos-") and entry.name != "aieos-console":
            kits.append(entry)
    return kits


def parse_entry_from_file(file_path: Path, kit_name: str) -> EntryFromFile:
    """Parse an entry-from-{upstream}.md file to extract required artifacts."""
    content = file_path.read_text(encoding="utf-8")
    filename = file_path.name
    # Extract upstream suffix from filename: entry-from-{suffix}.md
    match = re.match(r"entry-from-(.+)\.md", filename)
    upstream_suffix = match.group(1) if match else ""

    entry = EntryFromFile(
        kit_name=kit_name,
        upstream_suffix=upstream_suffix,
        file_path=str(file_path),
    )

    # Parse the "What you must bring:" table
    # Look for table rows after the artifact table header
    table_pattern = re.compile(
        r"\|\s*(.+?)\s*\|\s*(Frozen|Required|Recommended)\s*\|",
        re.IGNORECASE,
    )
    in_table = False
    for line in content.split("\n"):
        if "Status Required" in line or "What you must bring" in line:
            in_table = True
            continue
        if in_table and line.startswith("|"):
            # Skip separator rows
            if re.match(r"\|[-\s|]+\|", line):
                continue
            m = table_pattern.match(line)
            if m:
                artifact_name = m.group(1).strip()
                # Extract the artifact type abbreviation from parentheses
                abbrev = re.search(r"\((\w+)-\{", artifact_name)
                if abbrev:
                    entry.required_artifacts.append(abbrev.group(1))
                else:
                    # Fallback: use the full name
                    entry.required_artifacts.append(artifact_name)
        elif in_table and not line.startswith("|"):
            in_table = False

    # Parse "First artifact to produce"
    first_match = re.search(r"First artifact to produce.*?:\*?\*?\s*(.+?)(?:\s*—|\s*$)", content)
    if first_match:
        entry.first_artifact = first_match.group(1).strip()

    return entry


def parse_spec_file(file_path: Path, kit_name: str) -> SpecFile:
    """Parse a *-spec.md file to extract metadata."""
    content = file_path.read_text(encoding="utf-8")
    filename = file_path.name
    artifact_type = filename.replace("-spec.md", "")

    spec = SpecFile(
        kit_name=kit_name,
        artifact_type=artifact_type,
        file_path=str(file_path),
    )

    # Extract version
    version_match = re.search(r"Version:\s*(v[\d.]+)", content)
    if version_match:
        spec.version = version_match.group(1)

    # Count hard gates by looking for gate names in hard_gates sections
    # Pattern: gate names appear as list items or table rows
    gate_names = re.findall(r"(?:^|\|)\s*`?(\w+)`?\s*(?:\|.*(?:PASS|FAIL))", content, re.MULTILINE)
    if not gate_names:
        # Alternative: look for numbered gate patterns like "Gate 1: gate_name"
        gate_names = re.findall(r"Gate\s+\d+[.:]\s*`?(\w+)`?", content)
    if not gate_names:
        # Alternative: look for "hard_gates" JSON-style listing
        gate_names = re.findall(r'"(\w+)":\s*"PASS\s*\|\s*FAIL"', content)

    spec.hard_gate_names = gate_names
    spec.hard_gate_count = len(gate_names)

    return spec


def parse_tool_spec(file_path: Path, kit_name: str) -> ToolSpec:
    """Parse a tool *-spec.md file from docs/tools/ to extract metadata."""
    content = file_path.read_text(encoding="utf-8")
    filename = file_path.name
    tool_name = filename.replace("-spec.md", "")

    tool = ToolSpec(
        kit_name=kit_name,
        tool_name=tool_name,
        file_path=str(file_path),
    )

    # Extract version
    version_match = re.search(r"Version:\s*(v[\d.]+)", content)
    if version_match:
        tool.version = version_match.group(1)

    # Extract hard gate names from tables
    gate_names = re.findall(r"\|\s*`?(\w+)`?\s*\|.*(?:Rule|rule|Check|check)", content, re.MULTILINE)
    if not gate_names:
        gate_names = re.findall(r'"(\w+)":\s*"PASS\s*\|\s*FAIL"', content)

    tool.hard_gate_names = gate_names
    tool.hard_gate_count = len(gate_names)

    return tool


def parse_kit(kit_path: Path) -> KitStructure:
    """Parse a complete kit directory into structured data."""
    kit_name = kit_path.name
    kit = KitStructure(name=kit_name, directory=str(kit_path))

    docs = kit_path / "docs"
    if not docs.is_dir():
        return kit

    kit.has_playbook = (docs / "playbook.md").is_file()
    kit.has_claude_md = (kit_path / "CLAUDE.md").is_file()
    kit.has_governance_model = (docs / "governance-model.md").is_file()

    # Parse specs
    specs_dir = docs / "specs"
    if specs_dir.is_dir():
        for spec_file in sorted(specs_dir.glob("*-spec.md")):
            kit.specs.append(parse_spec_file(spec_file, kit_name))

    # Parse entry-from files
    for entry_file in sorted(docs.glob("entry-from-*.md")):
        kit.entry_files.append(parse_entry_from_file(entry_file, kit_name))

    # List templates
    artifacts_dir = docs / "artifacts"
    if artifacts_dir.is_dir():
        kit.templates = sorted(f.name for f in artifacts_dir.glob("*-template.md"))

    # List prompts
    prompts_dir = docs / "prompts"
    if prompts_dir.is_dir():
        kit.prompts = sorted(f.name for f in prompts_dir.glob("*-prompt.md"))

    # List validators
    validators_dir = docs / "validators"
    if validators_dir.is_dir():
        kit.validators = sorted(f.name for f in validators_dir.glob("*-validator.md"))

    # Parse tools
    tools_dir = docs / "tools"
    if tools_dir.is_dir():
        for tool_spec_file in sorted(tools_dir.glob("*-spec.md")):
            kit.tool_specs.append(parse_tool_spec(tool_spec_file, kit_name))
        kit.tool_templates = sorted(f.name for f in tools_dir.glob("*-template.md"))
        kit.tool_prompts = sorted(f.name for f in tools_dir.glob("*-prompt.md"))
        kit.tool_validators = sorted(f.name for f in tools_dir.glob("*-validator.md"))

    return kit
