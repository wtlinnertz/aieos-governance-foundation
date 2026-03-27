import pytest
from pathlib import Path
import xml.etree.ElementTree as ET

from scripts.diagram_export.models import Node, Edge, Subgraph, Diagram, MermaidBlock
from scripts.diagram_export.parser import parse_mermaid
from scripts.diagram_export.layout import layout_diagram
from scripts.diagram_export.drawio import generate_drawio
from scripts.diagram_export.extractor import extract_mermaid_blocks, extract_artifact_id
from scripts.diagram_export.export import export_artifact, list_mermaid_blocks


# ---------------------------------------------------------------------------
# Parser Tests (14 tests)
# ---------------------------------------------------------------------------

class TestParserDirection:
    def test_parse_graph_lr(self):
        d = parse_mermaid("graph LR\n    A --> B")
        assert d.direction == "LR"

    def test_parse_graph_tb(self):
        d = parse_mermaid("graph TB\n    A --> B")
        assert d.direction == "TB"

    def test_parse_graph_td_normalized_to_tb(self):
        """TD is normalized to TB (both mean top-down)."""
        d = parse_mermaid("graph TD\n    A --> B")
        assert d.direction == "TB"

class TestParserNodes:
    def test_rectangle_node(self):
        d = parse_mermaid('graph LR\n    A["My Label"]')
        assert "A" in d.nodes
        assert d.nodes["A"].label == "My Label"
        assert d.nodes["A"].shape == "rectangle"

    def test_rounded_node(self):
        d = parse_mermaid('graph LR\n    A("Rounded")')
        assert d.nodes["A"].shape == "rounded"

    def test_diamond_node(self):
        d = parse_mermaid('graph LR\n    A{"Decision"}')
        assert d.nodes["A"].shape == "diamond"

    def test_circle_node(self):
        d = parse_mermaid('graph LR\n    A(("Circle"))')
        assert d.nodes["A"].shape == "circle"

    def test_node_with_br_tag(self):
        d = parse_mermaid('graph LR\n    A["Line 1<br/>Line 2"]')
        assert "<br/>" in d.nodes["A"].label

class TestParserEdges:
    def test_solid_edge(self):
        d = parse_mermaid("graph LR\n    A --> B")
        assert len(d.edges) == 1
        assert d.edges[0].source == "A"
        assert d.edges[0].target == "B"
        assert d.edges[0].style == "solid"

    def test_dashed_edge(self):
        d = parse_mermaid("graph LR\n    A -.-> B")
        assert d.edges[0].style == "dashed"

    def test_thick_edge(self):
        d = parse_mermaid("graph LR\n    A ==> B")
        assert d.edges[0].style == "thick"

    def test_labeled_edge(self):
        d = parse_mermaid('graph LR\n    A -->|"HTTP REST"| B')
        assert d.edges[0].label == "HTTP REST"

    def test_implicit_node_creation(self):
        d = parse_mermaid("graph LR\n    A --> B")
        assert "A" in d.nodes
        assert "B" in d.nodes

class TestParserSubgraphs:
    def test_subgraph_with_children(self):
        content = """graph LR
    subgraph SG["My Group"]
        A["Node A"]
        B["Node B"]
    end"""
        d = parse_mermaid(content)
        assert "SG" in d.subgraphs
        assert d.subgraphs["SG"].label == "My Group"
        assert "A" in d.subgraphs["SG"].children
        assert "B" in d.subgraphs["SG"].children

    def test_skip_comments(self):
        d = parse_mermaid("graph LR\n    %% comment\n    A --> B")
        assert len(d.edges) == 1


# ---------------------------------------------------------------------------
# Real AIEOS Artifact Test
# ---------------------------------------------------------------------------

class TestParserRealArtifact:
    def test_search_sad_context_diagram(self):
        """Parse the actual context diagram from aieos-search SAD."""
        content = """graph TB
    Consumer["API Consumer<br/>(External B2B)"]
    subgraph SystemBoundary["Search System"]
        SearchAPI["Search API"]
        IndexSync["Index Synchronization"]
    end
    PostgreSQL["PostgreSQL<br/>(Primary Datastore)"]
    Elasticsearch["Elasticsearch Cluster<br/>(Shared with ELK)"]

    Consumer -->|"HTTP REST<br/>(sync)"| SearchAPI
    SearchAPI -->|"Query<br/>(sync)"| Elasticsearch
    IndexSync -->|"Read changes<br/>(async)"| PostgreSQL
    IndexSync -->|"Write indices<br/>(async)"| Elasticsearch"""

        d = parse_mermaid(content)
        assert d.direction == "TB"
        assert "Consumer" in d.nodes
        assert "SearchAPI" in d.nodes
        assert "IndexSync" in d.nodes
        assert "SystemBoundary" in d.subgraphs
        assert len(d.edges) == 4
        # Verify subgraph children
        assert "SearchAPI" in d.subgraphs["SystemBoundary"].children
        assert "IndexSync" in d.subgraphs["SystemBoundary"].children


# ---------------------------------------------------------------------------
# Layout Tests (4 tests)
# ---------------------------------------------------------------------------

class TestLayout:
    def test_lr_layout_positions_left_to_right(self):
        d = parse_mermaid("graph LR\n    A --> B --> C")
        layout_diagram(d)
        assert d.nodes["A"].x < d.nodes["B"].x < d.nodes["C"].x

    def test_tb_layout_positions_top_to_bottom(self):
        d = parse_mermaid("graph TB\n    A --> B --> C")
        layout_diagram(d)
        assert d.nodes["A"].y < d.nodes["B"].y < d.nodes["C"].y

    def test_subgraph_contains_children(self):
        content = "graph LR\n    subgraph SG[\"Group\"]\n        A[\"A\"]\n        B[\"B\"]\n    end"
        d = parse_mermaid(content)
        layout_diagram(d)
        sg = d.subgraphs["SG"]
        for child_id in sg.children:
            node = d.nodes[child_id]
            assert node.x >= sg.x
            assert node.y >= sg.y

    def test_disconnected_nodes_at_origin(self):
        d = parse_mermaid("graph LR\n    A[\"Alone\"]\n    B[\"Also Alone\"]")
        layout_diagram(d)
        # Both at layer 0
        assert d.nodes["A"].x == d.nodes["B"].x or d.nodes["A"].y == d.nodes["B"].y


# ---------------------------------------------------------------------------
# Drawio Generation Tests (5 tests)
# ---------------------------------------------------------------------------

class TestDrawioGeneration:
    def test_xml_well_formed(self):
        d = parse_mermaid("graph LR\n    A --> B")
        layout_diagram(d)
        xml_str = generate_drawio(d)
        root = ET.fromstring(xml_str)
        assert root.tag == "mxGraphModel"

    def test_correct_cell_count(self):
        d = parse_mermaid("graph LR\n    A --> B")
        layout_diagram(d)
        xml_str = generate_drawio(d)
        root = ET.fromstring(xml_str)
        cells = root.findall(".//mxCell")
        # 2 root cells + 2 nodes + 1 edge = 5
        assert len(cells) == 5

    def test_node_style_matches_shape(self):
        d = parse_mermaid('graph LR\n    A{"Decision"}')
        layout_diagram(d)
        xml_str = generate_drawio(d)
        root = ET.fromstring(xml_str)
        cells = root.findall('.//mxCell[@vertex="1"]')
        diamond_cell = [c for c in cells if "rhombus" in (c.get("style") or "")]
        assert len(diamond_cell) == 1

    def test_edge_source_target(self):
        d = parse_mermaid("graph LR\n    A --> B")
        layout_diagram(d)
        xml_str = generate_drawio(d)
        root = ET.fromstring(xml_str)
        edges = root.findall('.//mxCell[@edge="1"]')
        assert len(edges) == 1
        # Source and target should reference valid cell IDs
        assert edges[0].get("source") != ""
        assert edges[0].get("target") != ""

    def test_subgraph_as_container(self):
        content = "graph LR\n    subgraph SG[\"Container\"]\n        A[\"Child\"]\n    end"
        d = parse_mermaid(content)
        layout_diagram(d)
        xml_str = generate_drawio(d)
        root = ET.fromstring(xml_str)
        swimlanes = [c for c in root.findall('.//mxCell[@vertex="1"]') if "swimlane" in (c.get("style") or "")]
        assert len(swimlanes) == 1
        assert swimlanes[0].get("value") == "Container"


# ---------------------------------------------------------------------------
# Extractor Tests (3 tests)
# ---------------------------------------------------------------------------

class TestExtractor:
    def test_extract_blocks_from_markdown(self, tmp_path):
        md = tmp_path / "test.md"
        md.write_text("## Architecture\n\n```mermaid\ngraph LR\n    A --> B\n```\n\n## Another\n\n```mermaid\ngraph TB\n    C --> D\n```\n")
        blocks, source_hash = extract_mermaid_blocks(md)
        assert len(blocks) == 2
        assert blocks[0].index == 1
        assert blocks[0].heading == "Architecture"
        assert blocks[1].index == 2
        assert blocks[1].heading == "Another"
        assert len(source_hash) == 64

    def test_extract_artifact_id(self, tmp_path):
        md = tmp_path / "sad.md"
        md.write_text("# SAD\n\n- SAD ID: SAD-SEARCH-001\n")
        assert extract_artifact_id(md) == "SAD-SEARCH-001"

    def test_extract_artifact_id_fallback(self, tmp_path):
        md = tmp_path / "my-doc.md"
        md.write_text("# No ID here\n")
        assert extract_artifact_id(md) == "my-doc"


# ---------------------------------------------------------------------------
# Integration Tests (5 tests)
# ---------------------------------------------------------------------------

class TestExportIntegration:
    def test_full_export(self, tmp_path):
        md = tmp_path / "05-sad.md"
        md.write_text("# SAD\n\n- SAD ID: SAD-TEST-001\n\n## Context\n\n```mermaid\ngraph LR\n    A --> B\n```\n")
        record = export_artifact(str(md), output_format="drawio", output_directory=str(tmp_path))
        assert record.status == "PASS"
        assert record.blocks_exported == 1
        assert record.source_modified is False
        output = tmp_path / "SAD-TEST-001-diagram-1.drawio"
        assert output.exists()
        # Verify XML well-formed
        ET.parse(str(output))

    def test_source_unchanged(self, tmp_path):
        md = tmp_path / "test.md"
        content = "# Test\n\n```mermaid\ngraph LR\n    A --> B\n```\n"
        md.write_text(content)
        record = export_artifact(str(md), output_format="drawio", output_directory=str(tmp_path))
        assert md.read_text() == content
        assert record.source_hash_before == record.source_hash_after

    def test_idempotent(self, tmp_path):
        md = tmp_path / "test.md"
        md.write_text("# Test\n- SAD ID: SAD-X-001\n\n```mermaid\ngraph LR\n    A --> B\n```\n")
        r1 = export_artifact(str(md), output_format="drawio", output_directory=str(tmp_path))
        r2 = export_artifact(str(md), output_format="drawio", output_directory=str(tmp_path))
        assert r1.results[0].content_hash == r2.results[0].content_hash

    def test_no_mermaid_blocks(self, tmp_path):
        md = tmp_path / "empty.md"
        md.write_text("# No diagrams here\n\nJust text.\n")
        record = export_artifact(str(md), output_format="drawio")
        assert record.status == "PASS"
        assert record.blocks_found == 0

    def test_list_blocks(self, tmp_path):
        md = tmp_path / "test.md"
        md.write_text("## Sec1\n\n```mermaid\ngraph LR\n    A-->B\n```\n\n## Sec2\n\n```mermaid\ngraph TB\n    C-->D\n```\n")
        blocks = list_mermaid_blocks(str(md))
        assert len(blocks) == 2
        assert blocks[0]["heading"] == "Sec1"
        assert blocks[1]["heading"] == "Sec2"


# ---------------------------------------------------------------------------
# Real Artifact Regression Test
# ---------------------------------------------------------------------------

class TestRealArtifactExport:
    @pytest.mark.slow
    def test_export_search_sad(self, tmp_path):
        """Export diagrams from the real aieos-search SAD if it exists."""
        sad_path = Path(__file__).parent.parent.parent / "aieos-search" / "docs" / "sdlc" / "05-sad.md"
        if not sad_path.exists():
            pytest.skip("aieos-search SAD not found")
        record = export_artifact(str(sad_path), output_format="drawio", output_directory=str(tmp_path))
        assert record.status in ("PASS", "PARTIAL")
        assert record.blocks_found >= 2
        assert record.blocks_exported >= 1
        assert record.source_modified is False
        # Verify each output is valid XML
        for r in record.results:
            ET.parse(r.output_path)
