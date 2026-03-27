"""Draw.io XML generator.

Converts a positioned Diagram model into a .drawio XML string that can be
imported directly into draw.io / diagrams.net. Uses only xml.etree.ElementTree
from the standard library.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET

from .models import Diagram, Edge, Node, Subgraph

# Style constants for draw.io cell rendering
STYLES = {
    "rectangle": (
        "rounded=0;whiteSpace=wrap;html=1;"
        "fillColor=#dae8fc;strokeColor=#6c8ebf;"
        "fontFamily=Helvetica;fontSize=12;"
    ),
    "rounded": (
        "rounded=1;whiteSpace=wrap;html=1;"
        "fillColor=#dae8fc;strokeColor=#6c8ebf;"
        "fontFamily=Helvetica;fontSize=12;"
    ),
    "diamond": (
        "rhombus;whiteSpace=wrap;html=1;"
        "fillColor=#fff2cc;strokeColor=#d6b656;"
        "fontFamily=Helvetica;fontSize=12;"
    ),
    "circle": (
        "ellipse;whiteSpace=wrap;html=1;"
        "fillColor=#dae8fc;strokeColor=#6c8ebf;"
        "fontFamily=Helvetica;fontSize=12;"
    ),
    "cylinder": (
        "shape=cylinder3;whiteSpace=wrap;html=1;"
        "fillColor=#dae8fc;strokeColor=#6c8ebf;"
        "fontFamily=Helvetica;fontSize=12;"
        "boundedLbl=1;backgroundOutline=1;size=15;"
    ),
    "subgraph": (
        "swimlane;startSize=30;"
        "fillColor=#f5f5f5;strokeColor=#666666;"
        "fontFamily=Helvetica;fontSize=12;fontStyle=1;"
    ),
}

EDGE_STYLES = {
    "solid": (
        "endArrow=classic;html=1;"
        "strokeColor=#333333;"
        "fontFamily=Helvetica;fontSize=10;"
    ),
    "dashed": (
        "endArrow=classic;html=1;dashed=1;"
        "strokeColor=#333333;"
        "fontFamily=Helvetica;fontSize=10;"
    ),
    "thick": (
        "endArrow=classic;html=1;strokeWidth=3;"
        "strokeColor=#333333;"
        "fontFamily=Helvetica;fontSize=10;"
    ),
}


def _normalize_label(label: str) -> str:
    """Convert Mermaid line breaks to draw.io HTML line breaks."""
    return label.replace("<br/>", "<br>")


def generate_drawio(diagram: Diagram) -> str:
    """Generate a .drawio XML string from a positioned Diagram.

    The output is a well-formed XML document that can be opened directly
    in draw.io / diagrams.net or imported as a .drawio file.
    """
    model = ET.Element("mxGraphModel")
    model.set("dx", "1422")
    model.set("dy", "794")
    model.set("grid", "1")
    model.set("gridSize", "10")
    model.set("guides", "1")
    model.set("tooltips", "1")
    model.set("connect", "1")
    model.set("arrows", "1")
    model.set("fold", "1")
    model.set("page", "1")
    model.set("pageScale", "1")
    model.set("pageWidth", "1169")
    model.set("pageHeight", "827")
    model.set("math", "0")
    model.set("shadow", "0")

    root = ET.SubElement(model, "root")

    # Root cells (required by draw.io format)
    cell0 = ET.SubElement(root, "mxCell")
    cell0.set("id", "0")
    cell1 = ET.SubElement(root, "mxCell")
    cell1.set("id", "1")
    cell1.set("parent", "0")

    cell_id = 2  # Next available numeric ID
    id_map: dict[str, str] = {}  # node/subgraph ID -> draw.io cell ID

    # ------------------------------------------------------------------
    # 1. Render subgraphs first (they act as containers)
    # ------------------------------------------------------------------
    # Render in dependency order: parents before children
    rendered: set[str] = set()
    render_queue = list(diagram.subgraphs.keys())

    # Simple iterative approach: keep rendering subgraphs whose parents
    # are already rendered (or have no parent).
    max_iterations = len(render_queue) + 1
    iteration = 0
    while render_queue and iteration < max_iterations:
        iteration += 1
        remaining: list[str] = []
        for sg_id in render_queue:
            sg = diagram.subgraphs[sg_id]
            parent_ready = sg.parent is None or sg.parent in rendered
            if parent_ready:
                cid = str(cell_id)
                cell_id += 1
                id_map[sg_id] = cid

                cell = ET.SubElement(root, "mxCell")
                cell.set("id", cid)
                cell.set("value", sg.label)
                cell.set("style", STYLES["subgraph"])
                cell.set("vertex", "1")
                cell.set("parent", id_map.get(sg.parent, "1"))

                geo = ET.SubElement(cell, "mxGeometry")
                geo.set("x", str(int(sg.x)))
                geo.set("y", str(int(sg.y)))
                geo.set("width", str(int(sg.width)))
                geo.set("height", str(int(sg.height)))
                geo.set("as", "geometry")

                rendered.add(sg_id)
            else:
                remaining.append(sg_id)
        render_queue = remaining

    # ------------------------------------------------------------------
    # 2. Render nodes
    # ------------------------------------------------------------------
    for node_id, node in diagram.nodes.items():
        cid = str(cell_id)
        cell_id += 1
        id_map[node_id] = cid

        cell = ET.SubElement(root, "mxCell")
        cell.set("id", cid)
        cell.set("value", _normalize_label(node.label))
        cell.set("style", STYLES.get(node.shape, STYLES["rectangle"]))
        cell.set("vertex", "1")
        # Parent is the subgraph container, or root cell "1"
        cell.set("parent", id_map.get(node.parent, "1"))

        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("x", str(int(node.x)))
        geo.set("y", str(int(node.y)))
        geo.set("width", str(int(node.width)))
        geo.set("height", str(int(node.height)))
        geo.set("as", "geometry")

    # ------------------------------------------------------------------
    # 3. Render edges
    # ------------------------------------------------------------------
    for edge in diagram.edges:
        source_cid = id_map.get(edge.source, "")
        target_cid = id_map.get(edge.target, "")

        # Skip edges with unmapped endpoints
        if not source_cid or not target_cid:
            continue

        cid = str(cell_id)
        cell_id += 1

        cell = ET.SubElement(root, "mxCell")
        cell.set("id", cid)
        cell.set(
            "value",
            _normalize_label(edge.label) if edge.label else "",
        )
        cell.set("style", EDGE_STYLES.get(edge.style, EDGE_STYLES["solid"]))
        cell.set("edge", "1")
        cell.set("parent", "1")
        cell.set("source", source_cid)
        cell.set("target", target_cid)

        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("relative", "1")
        geo.set("as", "geometry")

    # ------------------------------------------------------------------
    # Serialize to XML string
    # ------------------------------------------------------------------
    ET.indent(model, space="  ")
    return ET.tostring(model, encoding="unicode", xml_declaration=True)
