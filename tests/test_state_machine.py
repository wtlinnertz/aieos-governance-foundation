"""Test artifact state machine rules.

Validates:
- Valid state transitions (Draft → Frozen, Frozen → Deprecated)
- Invalid transitions are not possible (Frozen → Draft without re-entry)
- Cross-cutting kits do not block each other
- Cross-cutting kits do not block the pipeline (except QAK)
"""

from __future__ import annotations

import networkx as nx
import pytest

from models.framework import DEPENDENCY_EDGES, KIT_REGISTRY


# Valid artifact states and transitions
VALID_STATES = {"Draft", "Frozen", "Deprecated"}
VALID_TRANSITIONS = {
    ("Draft", "Frozen"),       # Normal: validate → freeze
    ("Frozen", "Deprecated"),  # Normal: end of lifecycle
    # Re-entry creates a new version, not a state change on the original
}
INVALID_TRANSITIONS = {
    ("Frozen", "Draft"),       # Cannot unfreeze — must create new version
    ("Deprecated", "Draft"),   # Cannot resurrect
    ("Deprecated", "Frozen"),  # Cannot resurrect
}


class TestStateTransitions:
    """Artifact state transitions follow the governance model."""

    def test_valid_transitions_are_defined(self):
        assert len(VALID_TRANSITIONS) > 0

    def test_invalid_transitions_are_defined(self):
        assert len(INVALID_TRANSITIONS) > 0

    def test_no_overlap(self):
        overlap = VALID_TRANSITIONS & INVALID_TRANSITIONS
        assert overlap == set(), f"Transitions in both valid and invalid: {overlap}"

    def test_all_states_covered(self):
        """Every state must appear as either source or target of a valid transition."""
        sources = {t[0] for t in VALID_TRANSITIONS}
        targets = {t[1] for t in VALID_TRANSITIONS}
        covered = sources | targets
        assert covered == VALID_STATES, (
            f"States not covered by transitions: {VALID_STATES - covered}"
        )


class TestCrossCuttingIndependence:
    """Cross-cutting kits must not depend on each other."""

    CROSS_CUTTING_KITS = {
        name for name, info in KIT_REGISTRY.items()
        if info.category == "cross-cutting"
    }

    def test_cross_cutting_set_matches_registry(self):
        """The cross-cutting set should include all kits with category 'cross-cutting'."""
        expected = {"QAK", "SCK", "DCK", "PINFK", "DKK", "PRK", "BPK"}
        assert self.CROSS_CUTTING_KITS == expected, (
            f"Cross-cutting kit mismatch. Got: {self.CROSS_CUTTING_KITS}, "
            f"expected: {expected}"
        )

    def test_no_cross_cutting_to_cross_cutting_freeze_dependencies(self):
        """Cross-cutting kits must not have freeze dependencies on each other.

        Trigger edges between cross-cutting kits are allowed (e.g., PRK reviews
        QAK artifacts). Only freeze-type edges would create blocking dependencies.
        """
        violations = []
        for upstream, downstream, gate_type in DEPENDENCY_EDGES:
            if gate_type != "freeze":
                continue  # Only freeze edges create blocking dependencies
            up_kit = upstream.split(":")[0]
            down_kit = downstream.split(":")[0]
            if up_kit in self.CROSS_CUTTING_KITS and down_kit in self.CROSS_CUTTING_KITS:
                if up_kit != down_kit:  # Internal dependencies within a kit are fine
                    violations.append(f"{upstream} → {downstream}")
        assert violations == [], (
            f"Cross-cutting kits must not have freeze dependencies on each other:\n" +
            "\n".join(f"  - {v}" for v in violations)
        )

    def test_cross_cutting_do_not_block_pipeline(self, freeze_graph: nx.DiGraph):
        """No pipeline kit should have a mandatory dependency on a cross-cutting kit
        (except QAK → REK when QAK is adopted)."""
        pipeline_kits = {name for name, info in KIT_REGISTRY.items() if info.category == "pipeline"}
        cross_cutting = self.CROSS_CUTTING_KITS

        violations = []
        for upstream, downstream, gate_type in DEPENDENCY_EDGES:
            if gate_type == "escalation":
                continue
            up_kit = upstream.split(":")[0]
            down_kit = downstream.split(":")[0]
            # Cross-cutting blocking pipeline (except QAK→REK which is documented exception)
            if up_kit in cross_cutting and down_kit in pipeline_kits:
                if up_kit == "QAK" and down_kit == "REK":
                    continue  # Documented exception: QAK gates REK when adopted
                violations.append(f"{upstream} → {downstream}")
        assert violations == [], (
            f"Cross-cutting kits blocking pipeline (except QAK→REK):\n" +
            "\n".join(f"  - {v}" for v in violations)
        )


class TestKitCategorization:
    """Every kit in the registry must have a valid category."""

    VALID_CATEGORIES = {"pipeline", "operational", "cross-cutting"}

    def test_all_kits_have_valid_category(self):
        for name, info in KIT_REGISTRY.items():
            assert info.category in self.VALID_CATEGORIES, (
                f"Kit {name} has invalid category: {info.category}"
            )

    def test_pipeline_layers_are_sequential(self):
        """Pipeline layers should have sequential layer numbers."""
        pipeline = sorted(
            (info.layer, name)
            for name, info in KIT_REGISTRY.items()
            if info.category == "pipeline"
        )
        layers = [l for l, _ in pipeline]
        # Layers should be monotonically increasing
        for i in range(1, len(layers)):
            assert layers[i] > layers[i - 1], (
                f"Pipeline layers not sequential: {pipeline}"
            )
