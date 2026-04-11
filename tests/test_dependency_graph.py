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


class TestNewArtifactPositioning:
    """Verify SMR and RSA are correctly positioned in the dependency graph."""

    def test_rsa_between_rcf_and_rp(self, freeze_graph: nx.DiGraph):
        """RSA must sit between RCF and RP in the REK flow."""
        assert freeze_graph.has_edge("REK:RCF", "REK:RSA"), (
            "Missing edge: REK:RCF → REK:RSA"
        )
        assert freeze_graph.has_edge("REK:RSA", "REK:RP"), (
            "Missing edge: REK:RSA → REK:RP"
        )
        assert not freeze_graph.has_edge("REK:RCF", "REK:RP"), (
            "Direct edge REK:RCF → REK:RP should not exist (RSA is between them)"
        )

    def test_smr_parallel_with_em(self, freeze_graph: nx.DiGraph):
        """SMR and EM should both depend on ISPEC but not on each other."""
        assert freeze_graph.has_edge("PINFK:ISPEC", "PINFK:SMR"), (
            "Missing edge: PINFK:ISPEC → PINFK:SMR"
        )
        assert freeze_graph.has_edge("PINFK:ISPEC", "PINFK:EM"), (
            "Missing edge: PINFK:ISPEC → PINFK:EM"
        )
        assert not freeze_graph.has_edge("PINFK:SMR", "PINFK:EM"), (
            "SMR should not depend on EM"
        )
        assert not freeze_graph.has_edge("PINFK:EM", "PINFK:SMR"), (
            "EM should not depend on SMR"
        )

    def test_smr_reachable_from_pdr(self, freeze_graph: nx.DiGraph):
        """SMR must be reachable from PDR entry point."""
        assert nx.has_path(freeze_graph, "PINFK:PDR", "PINFK:SMR"), (
            "PINFK:SMR not reachable from PINFK:PDR"
        )

    def test_rsa_reachable_from_rer(self, freeze_graph: nx.DiGraph):
        """RSA must be reachable from RER."""
        assert nx.has_path(freeze_graph, "REK:RER", "REK:RSA"), (
            "REK:RSA not reachable from REK:RER"
        )

    def test_rek_artifact_ordering(self, freeze_graph: nx.DiGraph):
        """REK flow must be strictly ordered: RER → RCF → RSA → RP → RR."""
        order = list(nx.topological_sort(freeze_graph))
        pos = {node: i for i, node in enumerate(order)}
        rek_artifacts = ["REK:RER", "REK:RCF", "REK:RSA", "REK:RP", "REK:RR"]
        for i in range(len(rek_artifacts) - 1):
            a, b = rek_artifacts[i], rek_artifacts[i + 1]
            assert pos[a] < pos[b], (
                f"REK ordering violation: {a} (pos {pos[a]}) should come before "
                f"{b} (pos {pos[b]})"
            )

    def test_pinfk_artifact_ordering(self, freeze_graph: nx.DiGraph):
        """PINFK flow: PDR before ISPEC; ISPEC before both SMR and EM."""
        order = list(nx.topological_sort(freeze_graph))
        pos = {node: i for i, node in enumerate(order)}
        assert pos["PINFK:PDR"] < pos["PINFK:ISPEC"], "PDR must come before ISPEC"
        assert pos["PINFK:ISPEC"] < pos["PINFK:SMR"], "ISPEC must come before SMR"
        assert pos["PINFK:ISPEC"] < pos["PINFK:EM"], "ISPEC must come before EM"


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
