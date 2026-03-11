"""Shared fixtures for AIEOS framework tests."""

from __future__ import annotations

from pathlib import Path

import networkx as nx
import pytest

from models.framework import DEPENDENCY_EDGES, ENTRY_POINTS, KIT_REGISTRY
from parsers.kit_parser import discover_kits, find_aieos_root, parse_kit


@pytest.fixture(scope="session")
def aieos_root() -> Path:
    """Path to the AIEOS monorepo root."""
    return find_aieos_root()


@pytest.fixture(scope="session")
def kit_paths(aieos_root: Path) -> list[Path]:
    """All kit directories."""
    return discover_kits(aieos_root)


@pytest.fixture(scope="session")
def parsed_kits(kit_paths):
    """All kits parsed into structured data."""
    return {kit_path.name: parse_kit(kit_path) for kit_path in kit_paths}


@pytest.fixture(scope="session")
def dependency_graph() -> nx.DiGraph:
    """Build the full AIEOS dependency graph from declared edges."""
    G = nx.DiGraph()
    for upstream, downstream, gate_type in DEPENDENCY_EDGES:
        G.add_edge(upstream, downstream, gate=gate_type)
    return G


@pytest.fixture(scope="session")
def freeze_graph() -> nx.DiGraph:
    """Build the freeze-only dependency graph (no escalation edges)."""
    G = nx.DiGraph()
    for upstream, downstream, gate_type in DEPENDENCY_EDGES:
        if gate_type in ("freeze", "trigger"):
            G.add_edge(upstream, downstream, gate=gate_type)
    return G


@pytest.fixture(scope="session")
def governance_foundation(aieos_root: Path) -> Path:
    """Path to governance foundation."""
    return aieos_root / "aieos-governance-foundation"
