"""Mermaid-to-drawio export tool for AIEOS artifacts.

Usage:
    python -m scripts.diagram_export --input docs/sdlc/05-sad.md --format drawio
    python -m scripts.diagram_export --input docs/sdlc/05-sad.md --list
"""

import argparse
import json
import sys
from pathlib import Path
from .export import export_artifact, list_mermaid_blocks

def main():
    parser = argparse.ArgumentParser(
        description="Export Mermaid diagrams from AIEOS artifacts to external formats"
    )
    parser.add_argument("--input", required=True, help="Path to source artifact file")
    parser.add_argument("--format", default="drawio", help="Output format (default: drawio)")
    parser.add_argument("--output-dir", help="Output directory (default: same as input)")
    parser.add_argument("--filter", type=int, help="Export only this diagram index (1-based)")
    parser.add_argument("--list", action="store_true", help="List Mermaid blocks without exporting")
    parser.add_argument("--quiet", action="store_true", help="Suppress output except errors")
    parser.add_argument("--json", action="store_true", help="Output export record as JSON")

    args = parser.parse_args()

    if args.list:
        blocks = list_mermaid_blocks(args.input)
        if not blocks:
            print(f"No Mermaid blocks found in {args.input}")
            return
        print(f"Found {len(blocks)} Mermaid block(s) in {args.input}:")
        for b in blocks:
            print(f"  #{b['index']}: {b['heading']} ({b['lines']} lines)")
        return

    record = export_artifact(
        artifact_path=args.input,
        output_format=args.format,
        output_directory=args.output_dir,
        diagram_filter=args.filter,
    )

    if args.json:
        # Serialize ExportRecord to JSON
        import dataclasses
        print(json.dumps(dataclasses.asdict(record), indent=2))
        return

    if not args.quiet:
        print(f"Status: {record.status}")
        print(f"Summary: {record.summary}")
        print(f"Blocks found: {record.blocks_found}")
        print(f"Blocks exported: {record.blocks_exported}")
        if record.blocks_skipped:
            print(f"Blocks skipped: {record.blocks_skipped}")
        for r in record.results:
            print(f"  #{r.index} ({r.heading}) → {r.output_path} ({r.file_size} bytes)")
        if record.errors:
            print("Errors:")
            for e in record.errors:
                print(f"  - {e}")
        print(f"Source modified: {'Yes' if record.source_modified else 'No'}")

    if record.status == "FAIL":
        sys.exit(1)

if __name__ == "__main__":
    main()
