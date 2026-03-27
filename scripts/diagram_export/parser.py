"""Mermaid flowchart parser.

Line-by-line regex matching for the subset of Mermaid syntax used in AIEOS
artifacts. Handles node definitions, edges with labels, subgraphs (including
nested), and various node shapes.
"""
from __future__ import annotations

import re
import sys
from typing import Optional

from .models import Diagram, Edge, Node, Subgraph

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# Direction line: graph LR / TB / TD / RL / BT
_RE_DIRECTION = re.compile(r"^\s*(?:graph|flowchart)\s+(LR|TB|TD|RL|BT)\s*$")

# Subgraph start: subgraph ID["Label"]  or  subgraph ID[Label]  or  subgraph ID
_RE_SUBGRAPH = re.compile(
    r'^\s*subgraph\s+(\S+?)(?:\s*\[?"?([^"\]]*)"?\]?)?\s*$'
)

# Subgraph end
_RE_END = re.compile(r"^\s*end\s*$")

# Node shape patterns (order matters for matching)
_SHAPE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    # cylinder:  A[("Label")]  or  A[(Label)]
    ("cylinder", re.compile(r'^([A-Za-z_][\w-]*)\s*\[\(\s*"?([^"\)]*)"?\s*\)\]$')),
    # circle:    A(("Label"))  or  A((Label))
    ("circle", re.compile(r'^([A-Za-z_][\w-]*)\s*\(\(\s*"?([^"\)]*)"?\s*\)\)$')),
    # diamond:   A{"Label"}    or  A{Label}
    ("diamond", re.compile(r'^([A-Za-z_][\w-]*)\s*\{\s*"?([^"\}]*)"?\s*\}$')),
    # rounded:   A("Label")   or  A(Label)
    ("rounded", re.compile(r'^([A-Za-z_][\w-]*)\s*\(\s*"?([^"\)]*)"?\s*\)$')),
    # rectangle: A["Label"]   or  A[Label]
    ("rectangle", re.compile(r'^([A-Za-z_][\w-]*)\s*\[\s*"?([^"\]]*)"?\s*\]$')),
]

# Edge patterns -------------------------------------------------------
# Captures:  source_chunk  arrow  optional_label  target_chunk
#
# Arrow types:
#   -->   solid
#   -.->  dashed
#   ==>   thick
#
# Label forms:
#   |"text"|   or   |text|
#
# Source/target chunks may include inline node definitions like A["Label"].
_RE_EDGE = re.compile(
    r"^\s*"
    r"(.+?)"                          # source chunk (non-greedy)
    r"\s+"                            # space before arrow
    r"(-->|-.->|==>)"                 # arrow
    r'(?:\|"?([^"|]*)"?\|)?'         # optional label in |...|
    r"\s+"                            # space after arrow/label
    r"(.+?)"                          # target chunk
    r"\s*$"
)

# Fallback: arrow glued to source (no space before arrow)
_RE_EDGE_NOSPACE = re.compile(
    r"^\s*"
    r"(.+?)"                          # source chunk (non-greedy)
    r"(-->|-.->|==>)"                 # arrow (directly touching source)
    r'(?:\|"?([^"|]*)"?\|)?'         # optional label
    r"\s*"                            # optional space
    r"(.+?)"                          # target chunk
    r"\s*$"
)

_ARROW_STYLE = {
    "-->": "solid",
    "-.->": "dashed",
    "==>": "thick",
}

# Bare node ID (no shape brackets)
_RE_BARE_ID = re.compile(r"^[A-Za-z_][\w-]*$")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parse_node_chunk(chunk: str) -> tuple[str, Optional[str], Optional[str]]:
    """Parse a node chunk that may be a bare ID or an ID with shape/label.

    Returns (node_id, label_or_None, shape_or_None).
    """
    chunk = chunk.strip()

    # Try each shape pattern
    for shape, pattern in _SHAPE_PATTERNS:
        m = pattern.match(chunk)
        if m:
            return m.group(1), m.group(2), shape

    # Bare ID
    if _RE_BARE_ID.match(chunk):
        return chunk, None, None

    # If nothing matched, try to extract at least an ID
    m = re.match(r"^([A-Za-z_][\w-]*)", chunk)
    if m:
        return m.group(1), None, None

    return chunk, None, None


def _ensure_node(
    diagram: Diagram,
    node_id: str,
    label: Optional[str] = None,
    shape: Optional[str] = None,
    parent: Optional[str] = None,
) -> Node:
    """Create a node if it doesn't exist, or update label/shape if provided."""
    if node_id in diagram.nodes:
        node = diagram.nodes[node_id]
        if label is not None:
            node.label = label
        if shape is not None:
            node.shape = shape
        if parent is not None:
            node.parent = parent
        return node

    node = Node(
        id=node_id,
        label=label if label is not None else node_id,
        shape=shape if shape is not None else "rectangle",
        parent=parent,
    )
    diagram.nodes[node_id] = node
    return node


def _register_child(diagram: Diagram, node_id: str, parent_id: str) -> None:
    """Add a node to its parent subgraph's children list."""
    if parent_id in diagram.subgraphs:
        sg = diagram.subgraphs[parent_id]
        if node_id not in sg.children:
            sg.children.append(node_id)


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------


def parse_mermaid(content: str) -> Diagram:
    """Parse a Mermaid flowchart into a Diagram model.

    Handles the subset of Mermaid syntax used in AIEOS artifacts:
    - graph/flowchart direction (LR, TB, TD, RL, BT)
    - Node definitions with shapes: [], (), {}, (()), [()]
    - Labels with optional quotes and <br/> line breaks
    - Edges with -->, -.->, ==> and optional |"label"|
    - Subgraphs (including nested) with optional ["Label"]
    - Implicit node creation from edges

    Lines that don't match any pattern are skipped with a warning.
    """
    diagram = Diagram()
    subgraph_stack: list[str] = []  # Stack for nesting

    # Pre-process: expand chained edges (A --> B --> C) into separate lines
    raw_lines = content.strip().split("\n")
    expanded_lines: list[str] = []
    _chain_re = re.compile(r"(-->|-.->|==>)")
    for raw in raw_lines:
        s = raw.strip()
        # Count arrow occurrences — if more than 1, split into separate edges
        arrows = list(_chain_re.finditer(s))
        if len(arrows) > 1 and not s.startswith("graph") and not s.startswith("subgraph"):
            # Split chain: find segments between arrows
            parts: list[str] = []
            prev_end = 0
            for am in arrows:
                parts.append(s[prev_end:am.start()].strip())
                parts.append(am.group())
                prev_end = am.end()
            parts.append(s[prev_end:].strip())
            # parts = [node, arrow, node, arrow, node, ...]
            # Generate pairwise edges
            i = 0
            while i + 2 < len(parts):
                expanded_lines.append(f"    {parts[i]} {parts[i+1]} {parts[i+2]}")
                i += 2
        else:
            expanded_lines.append(raw)

    for line in expanded_lines:
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith("%%"):
            continue

        # 1. Direction
        m = _RE_DIRECTION.match(stripped)
        if m:
            direction = m.group(1)
            # TD is equivalent to TB
            diagram.direction = "TB" if direction == "TD" else direction
            continue

        # 2. Subgraph start
        m = _RE_SUBGRAPH.match(stripped)
        if m:
            sg_id = m.group(1)
            sg_label = m.group(2) if m.group(2) else sg_id
            parent = subgraph_stack[-1] if subgraph_stack else None
            sg = Subgraph(id=sg_id, label=sg_label, parent=parent)
            diagram.subgraphs[sg_id] = sg
            # Register subgraph as child of parent subgraph
            if parent and parent in diagram.subgraphs:
                if sg_id not in diagram.subgraphs[parent].children:
                    diagram.subgraphs[parent].children.append(sg_id)
            subgraph_stack.append(sg_id)
            continue

        # 3. Subgraph end
        if _RE_END.match(stripped):
            if subgraph_stack:
                subgraph_stack.pop()
            continue

        # 4. Edge (try with space first, then without)
        m = _RE_EDGE.match(stripped) or _RE_EDGE_NOSPACE.match(stripped)
        if m:
            src_chunk = m.group(1)
            arrow = m.group(2)
            edge_label = m.group(3) or ""
            tgt_chunk = m.group(4)

            src_id, src_label, src_shape = _parse_node_chunk(src_chunk)
            tgt_id, tgt_label, tgt_shape = _parse_node_chunk(tgt_chunk)

            current_parent = subgraph_stack[-1] if subgraph_stack else None

            src_node = _ensure_node(
                diagram, src_id, src_label, src_shape, current_parent
            )
            tgt_node = _ensure_node(
                diagram, tgt_id, tgt_label, tgt_shape, current_parent
            )

            # Register as children of current subgraph
            if current_parent:
                _register_child(diagram, src_id, current_parent)
                _register_child(diagram, tgt_id, current_parent)

            edge = Edge(
                source=src_id,
                target=tgt_id,
                label=edge_label.strip(),
                style=_ARROW_STYLE.get(arrow, "solid"),
            )
            diagram.edges.append(edge)
            continue

        # 5. Standalone node definition
        matched_node = False
        for shape, pattern in _SHAPE_PATTERNS:
            m = pattern.match(stripped)
            if m:
                node_id = m.group(1)
                label = m.group(2)
                current_parent = subgraph_stack[-1] if subgraph_stack else None
                _ensure_node(diagram, node_id, label, shape, current_parent)
                if current_parent:
                    _register_child(diagram, node_id, current_parent)
                matched_node = True
                break

        if matched_node:
            continue

        # 6. Bare node ID on its own line
        if _RE_BARE_ID.match(stripped):
            current_parent = subgraph_stack[-1] if subgraph_stack else None
            _ensure_node(diagram, stripped, parent=current_parent)
            if current_parent:
                _register_child(diagram, stripped, current_parent)
            continue

        # Unrecognized line — skip with warning
        print(f"parser: skipping unrecognized line: {stripped}", file=sys.stderr)

    return diagram
