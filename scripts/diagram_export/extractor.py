from __future__ import annotations
import hashlib
import re
from pathlib import Path
from .models import MermaidBlock

def extract_mermaid_blocks(file_path: Path) -> tuple[list[MermaidBlock], str]:
    """Extract all Mermaid code blocks from a Markdown file.

    Returns (blocks, source_hash) where source_hash is SHA256 of file content.
    """
    content = file_path.read_text(encoding="utf-8")
    source_hash = hashlib.sha256(content.encode()).hexdigest()

    blocks = []
    # Find all ```mermaid ... ``` blocks
    # Use regex to find fenced code blocks with mermaid language tag
    pattern = r'```mermaid\s*\n(.*?)```'

    # Also track the nearest ## heading above each block
    lines = content.split('\n')
    current_heading = "Document"

    # Build a map of line_number -> heading
    heading_at_line = {}
    for i, line in enumerate(lines):
        if line.startswith('## '):
            current_heading = line[3:].strip()
        heading_at_line[i] = current_heading

    # Find blocks with their positions
    for match_idx, match in enumerate(re.finditer(pattern, content, re.DOTALL)):
        block_content = match.group(1).strip()
        # Find the line number of this match
        line_num = content[:match.start()].count('\n')
        heading = heading_at_line.get(line_num, "Document")

        blocks.append(MermaidBlock(
            index=match_idx + 1,
            heading=heading,
            content=block_content,
            source_hash=source_hash,
        ))

    return blocks, source_hash

def extract_artifact_id(file_path: Path) -> str:
    """Extract artifact ID from a Markdown file's Document Control section.

    Looks for patterns like:
    - SAD ID: SAD-SEARCH-001
    - PRD ID: PRD-HARNESS-001
    - {TYPE} ID: {ID}
    Falls back to filename without extension if not found.
    """
    content = file_path.read_text(encoding="utf-8")
    # Try to find an ID field in Document Control
    id_pattern = r'(?:SAD|PRD|TDD|ACF|DCF|WDD|ORD|KER|RER|RCF|RP|RR)\s*ID:\s*(\S+)'
    match = re.search(id_pattern, content)
    if match:
        return match.group(1)
    # Fallback: use filename
    return file_path.stem
