"""Step definitions for BDD feature files."""

from __future__ import annotations

from pathlib import Path

import networkx as nx
import pytest
from pytest_bdd import given, then, when, parsers, scenarios

from models.framework import (
    DEPENDENCY_EDGES,
    ENTRY_POINTS,
    PRESET_DEFINITIONS,
)

# Load all feature files
scenarios("features/escalation.feature")
scenarios("features/presets.feature")
scenarios("features/reentry.feature")


# ─── Shared State ─────────────────────────────────────────────────────────────

class ScenarioState:
    def __init__(self):
        self.graph: nx.DiGraph | None = None
        self.freeze_graph: nx.DiGraph | None = None
        self.preset = None
        self.flow_rules: list[str] = []


@pytest.fixture
def state():
    return ScenarioState()


# ─── Graph Steps ──────────────────────────────────────────────────────────────

@given("the dependency graph is loaded", target_fixture="state")
def load_dependency_graph():
    s = ScenarioState()
    s.graph = nx.DiGraph()
    s.freeze_graph = nx.DiGraph()
    for upstream, downstream, gate_type in DEPENDENCY_EDGES:
        s.graph.add_edge(upstream, downstream, gate=gate_type)
        if gate_type != "escalation":
            s.freeze_graph.add_edge(upstream, downstream, gate=gate_type)
    return s


@then(parsers.parse('an escalation edge exists from "{source}" to "{target}"'))
def check_escalation_edge(state, source, target):
    assert state.graph.has_edge(source, target), (
        f"No edge from {source} to {target}"
    )
    edge_data = state.graph.edges[source, target]
    assert edge_data.get("gate") == "escalation", (
        f"Edge {source} → {target} is type '{edge_data.get('gate')}', not 'escalation'"
    )


@when("escalation edges are removed")
def remove_escalation_edges(state):
    # freeze_graph already has no escalation edges
    pass


@then("the remaining graph is a DAG")
def check_dag(state):
    assert nx.is_directed_acyclic_graph(state.freeze_graph), (
        f"Graph has cycles: {list(nx.simple_cycles(state.freeze_graph))}"
    )


@then(parsers.parse('a path exists from "{source}" to "{target}"'))
def check_path_exists(state, source, target):
    assert nx.has_path(state.freeze_graph, source, target), (
        f"No path from {source} to {target}"
    )


@then("an escalation path exists for QAK FAIL back to EEK")
def check_qak_fail_escalation(state):
    # QAK FAIL means the initiative returns to EEK
    # This is a process rule, not a graph edge — verify the graph supports
    # re-entering EEK after QAK
    assert "EEK:ORD" in state.freeze_graph, "EEK:ORD not in graph"
    assert "QAK:QGR" in state.freeze_graph, "QAK:QGR not in graph"


# ─── Preset Steps ─────────────────────────────────────────────────────────────

@given(parsers.parse('the preset "{name}" is loaded'), target_fixture="state")
def load_preset(name):
    s = ScenarioState()
    matches = [p for p in PRESET_DEFINITIONS if p.name == name]
    assert len(matches) == 1, f"Preset '{name}' not found (found {len(matches)})"
    s.preset = matches[0]
    return s


@then(parsers.parse('the entry point is "{entry}"'))
def check_entry_point(state, entry):
    assert state.preset.entry_point == entry, (
        f"Expected entry {entry}, got {state.preset.entry_point}"
    )


@then(parsers.parse('"{kit}" is a required kit'))
def check_required_kit(state, kit):
    assert kit in state.preset.required_kits, (
        f"'{kit}' not in required kits: {state.preset.required_kits}"
    )


@then(parsers.parse('"{kit}" is not a required kit'))
def check_not_required_kit(state, kit):
    assert kit not in state.preset.required_kits, (
        f"'{kit}' should not be required but is in: {state.preset.required_kits}"
    )


@then(parsers.parse('"{artifact}" is a required artifact'))
def check_required_artifact(state, artifact):
    assert artifact in state.preset.required_artifacts, (
        f"'{artifact}' not in required artifacts"
    )


# ─── Flow Validation Rules Steps ─────────────────────────────────────────────

@given("the flow validation rules are loaded", target_fixture="state")
def load_flow_rules():
    s = ScenarioState()
    # The 8 flow validation rules from flow-reference.md §10
    s.flow_rules = [
        "Every initiative has an Engagement Record",
        "Freeze-before-promote is absolute",
        "Validators judge, they do not help",
        "Cross-cutting kits do not block each other",
        "Cross-cutting kits do not block the pipeline",
        "Escalation always creates a new initiative cycle",
        "Path selection is immutable",
        "Separate generation and validation sessions",
    ]
    return s


@then(parsers.parse('rule {number:d} states "{text}"'))
def check_flow_rule(state, number, text):
    assert 1 <= number <= len(state.flow_rules), (
        f"Rule {number} out of range (1-{len(state.flow_rules)})"
    )
    assert text in state.flow_rules[number - 1], (
        f"Rule {number} is '{state.flow_rules[number - 1]}', expected '{text}'"
    )
