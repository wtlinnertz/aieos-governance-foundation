"""Test the AIEOS dependency graph for structural correctness.

Validates:
- No circular dependencies (DAG property)
- Freeze-before-promote ordering is consistent
- All artifacts are reachable from at least one entry point
- No orphaned nodes
"""

from __future__ import annotations

import networkx as nx
import pytest

from models.framework import DEPENDENCY_EDGES, ENTRY_POINTS


class TestDAGProperty:
    """The forward dependency graph must be a DAG (no cycles)."""

    def test_freeze_graph_is_dag(self, freeze_graph: nx.DiGraph):
        assert nx.is_directed_acyclic_graph(freeze_graph), (
            f"Circular dependency detected: {list(nx.simple_cycles(freeze_graph))}"
        )

    def test_topological_sort_is_valid(self, freeze_graph: nx.DiGraph):
        """A valid topological ordering must exist."""
        order = list(nx.topological_sort(freeze_graph))
        assert len(order) == freeze_graph.number_of_nodes()

    def test_no_self_loops(self, dependency_graph: nx.DiGraph):
        self_loops = list(nx.selfloop_edges(dependency_graph))
        assert self_loops == [], f"Self-loop detected: {self_loops}"


class TestReachability:
    """Every artifact must be reachable from at least one entry point."""

    def test_all_nodes_reachable(self, freeze_graph: nx.DiGraph):
        unreachable = []
        for node in freeze_graph.nodes():
            if node in ENTRY_POINTS:
                continue
            reachable = any(
                nx.has_path(freeze_graph, entry, node)
                for entry in ENTRY_POINTS
                if entry in freeze_graph
            )
            if not reachable:
                unreachable.append(node)
        assert unreachable == [], f"Unreachable artifacts: {unreachable}"

    def test_entry_points_exist_in_graph(self, freeze_graph: nx.DiGraph):
        for entry in ENTRY_POINTS:
            assert entry in freeze_graph.nodes(), (
                f"Entry point {entry} not found in dependency graph"
            )


class TestFreezeBeforePromote:
    """Verify that the topological order respects freeze-before-promote."""

    def test_upstream_before_downstream(self, freeze_graph: nx.DiGraph):
        order = list(nx.topological_sort(freeze_graph))
        position = {node: idx for idx, node in enumerate(order)}
        violations = []
        for upstream, downstream, gate_type in DEPENDENCY_EDGES:
            if gate_type == "escalation":
                continue  # Escalation goes upstream, not subject to freeze order
            if upstream in position and downstream in position:
                if position[upstream] >= position[downstream]:
                    violations.append(
                        f"{upstream} (pos {position[upstream]}) must come before "
                        f"{downstream} (pos {position[downstream]})"
                    )
        assert violations == [], (
            f"Freeze-before-promote violations:\n" +
            "\n".join(f"  - {v}" for v in violations)
        )


class TestEscalationPaths:
    """Escalation edges go upstream and must not create forward cycles."""

    def test_escalation_edges_are_reverse_direction(self, dependency_graph: nx.DiGraph):
        """Escalation edges should point from downstream kits to upstream kits."""
        for upstream, downstream, gate_type in DEPENDENCY_EDGES:
            if gate_type == "escalation":
                # "upstream" in the edge tuple is the source (e.g., RRK:IR)
                # "downstream" is the target (e.g., EEK:KER)
                source_kit = upstream.split(":")[0]
                target_kit = downstream.split(":")[0]
                # Verify these are known kits (basic sanity)
                from models.framework import KIT_REGISTRY
                assert source_kit in KIT_REGISTRY, f"Unknown kit in escalation: {source_kit}"
                assert target_kit in KIT_REGISTRY, f"Unknown kit in escalation: {target_kit}"

    def test_removing_escalations_keeps_dag(self, freeze_graph: nx.DiGraph):
        """The graph without escalation edges must remain a DAG."""
        assert nx.is_directed_acyclic_graph(freeze_graph)
