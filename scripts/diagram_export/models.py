"""Data model for the Mermaid-to-drawio graph representation.

Pure dataclasses, no external dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    id: str
    label: str
    shape: str  # "rectangle", "rounded", "diamond", "circle", "cylinder"
    parent: str | None = None  # Subgraph ID if nested
    x: float = 0.0
    y: float = 0.0
    width: float = 120.0
    height: float = 60.0


@dataclass
class Edge:
    source: str
    target: str
    label: str = ""
    style: str = "solid"  # "solid", "dashed", "thick"


@dataclass
class Subgraph:
    id: str
    label: str
    children: list[str] = field(default_factory=list)  # Node IDs
    parent: str | None = None  # Nested subgraph parent
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0


@dataclass
class Diagram:
    direction: str = "TB"  # "LR" or "TB"
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    subgraphs: dict[str, Subgraph] = field(default_factory=dict)


@dataclass
class MermaidBlock:
    index: int  # 1-based
    heading: str  # Nearest ## heading above the block
    content: str  # Raw Mermaid content
    source_hash: str  # SHA256 of the source file
