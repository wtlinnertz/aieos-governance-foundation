from __future__ import annotations
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from .extractor import extract_mermaid_blocks, extract_artifact_id
from .parser import parse_mermaid
from .layout import layout_diagram
from .drawio import generate_drawio

@dataclass
class DiagramResult:
    index: int
    heading: str
    output_path: str
    format: str
    file_size: int
    content_hash: str

@dataclass
class ExportRecord:
    tool_id: str = "TOOL-DIAGRAM-EXPORT"
    artifact_id: str = ""
    artifact_path: str = ""
    output_format: str = ""
    timestamp: str = ""
    blocks_found: int = 0
    blocks_exported: int = 0
    blocks_skipped: int = 0
    results: list[DiagramResult] = field(default_factory=list)
    source_hash_before: str = ""
    source_hash_after: str = ""
    source_modified: bool = False
    status: str = "PASS"
    summary: str = ""
    errors: list[str] = field(default_factory=list)

def export_artifact(
    artifact_path: str,
    output_format: str = "drawio",
    output_directory: str | None = None,
    diagram_filter: int | None = None,
) -> ExportRecord:
    """Export Mermaid diagrams from an AIEOS artifact.

    Args:
        artifact_path: Path to the source Markdown artifact
        output_format: Target format ("drawio" supported)
        output_directory: Where to write output (default: same as source)
        diagram_filter: Export only this 1-based diagram index (default: all)

    Returns:
        ExportRecord conforming to diagram-export-template.md
    """
    path = Path(artifact_path)
    record = ExportRecord(
        artifact_path=str(path),
        output_format=output_format,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    # Step 1: Validate input
    if not path.exists():
        record.status = "FAIL"
        record.summary = f"Artifact not found: {path}"
        record.errors.append(record.summary)
        return record

    if output_format != "drawio":
        record.status = "FAIL"
        record.summary = f"Format '{output_format}' not supported (only 'drawio' implemented)"
        record.errors.append(record.summary)
        return record

    # Step 2: Extract artifact ID and mermaid blocks
    artifact_id = extract_artifact_id(path)
    record.artifact_id = artifact_id

    blocks, source_hash = extract_mermaid_blocks(path)
    record.source_hash_before = source_hash
    record.blocks_found = len(blocks)

    if not blocks:
        record.status = "PASS"
        record.summary = f"No Mermaid blocks found in {artifact_id}"
        record.blocks_exported = 0
        # Verify source unchanged
        record.source_hash_after = hashlib.sha256(path.read_bytes()).hexdigest()
        record.source_modified = record.source_hash_before != record.source_hash_after
        return record

    # Step 3: Filter if requested
    if diagram_filter is not None:
        blocks = [b for b in blocks if b.index == diagram_filter]
        if not blocks:
            record.status = "PASS"
            record.summary = f"Filter {diagram_filter} matched no blocks"
            record.source_hash_after = hashlib.sha256(path.read_bytes()).hexdigest()
            record.source_modified = record.source_hash_before != record.source_hash_after
            return record

    # Step 4: Determine output directory
    out_dir = Path(output_directory) if output_directory else path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # Step 5: Process each block
    for block in blocks:
        try:
            diagram = parse_mermaid(block.content)
            layout_diagram(diagram)
            xml_content = generate_drawio(diagram)

            # Write output
            output_filename = f"{artifact_id}-diagram-{block.index}.drawio"
            output_path = out_dir / output_filename
            output_path.write_text(xml_content, encoding="utf-8")

            content_hash = hashlib.sha256(xml_content.encode()).hexdigest()

            record.results.append(DiagramResult(
                index=block.index,
                heading=block.heading,
                output_path=str(output_path),
                format="drawio",
                file_size=len(xml_content.encode()),
                content_hash=content_hash,
            ))
            record.blocks_exported += 1

        except Exception as e:
            record.errors.append(f"Block {block.index}: {e}")
            record.blocks_skipped += 1

    # Step 6: Verify source unchanged
    record.source_hash_after = hashlib.sha256(path.read_bytes()).hexdigest()
    record.source_modified = record.source_hash_before != record.source_hash_after

    # Step 7: Set status
    if record.blocks_exported == 0:
        record.status = "FAIL"
        record.summary = "No diagrams exported"
    elif record.blocks_skipped > 0:
        record.status = "PARTIAL"
        record.summary = f"Exported {record.blocks_exported}/{record.blocks_found} diagrams ({record.blocks_skipped} skipped)"
    else:
        record.status = "PASS"
        record.summary = f"Exported {record.blocks_exported} diagram(s) from {artifact_id}"

    return record

def list_mermaid_blocks(artifact_path: str) -> list[dict]:
    """List Mermaid blocks in an artifact without exporting."""
    path = Path(artifact_path)
    if not path.exists():
        return []
    blocks, _ = extract_mermaid_blocks(path)
    return [
        {"index": b.index, "heading": b.heading, "lines": b.content.count('\n') + 1}
        for b in blocks
    ]
