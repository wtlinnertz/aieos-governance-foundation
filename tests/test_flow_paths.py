"""Test initiative preset flow paths for validity.

Validates:
- Every required artifact in each preset is reachable from the preset's entry point
- Every required kit has at least one artifact in the preset
- Preset entry points match declared entry points
"""

from __future__ import annotations

import networkx as nx
import pytest

from models.framework import ENTRY_POINTS, KIT_REGISTRY, PRESET_DEFINITIONS


@pytest.fixture(params=PRESET_DEFINITIONS, ids=lambda p: p.name)
def preset(request):
    return request.param


class TestPresetPathValidity:
    """Each preset's required artifacts must be reachable from its entry point."""

    def test_entry_point_is_valid(self, preset):
        assert preset.entry_point in ENTRY_POINTS, (
            f"Preset '{preset.name}' entry point {preset.entry_point} "
            f"is not a declared AIEOS entry point"
        )

    def test_required_artifacts_reachable(self, preset, freeze_graph: nx.DiGraph):
        """Every required artifact must be reachable from at least one entry point.

        Some presets involve multiple independent entry points (e.g., PINFK:PDR
        enters directly while PIK:WCR enters the main pipeline). An artifact is
        valid if reachable from ANY declared entry point.
        """
        unreachable = []
        for artifact in preset.required_artifacts:
            if artifact in ENTRY_POINTS:
                continue
            if artifact not in freeze_graph:
                unreachable.append(f"{artifact} (not in graph)")
                continue
            reachable = any(
                nx.has_path(freeze_graph, entry, artifact)
                for entry in ENTRY_POINTS
                if entry in freeze_graph
            )
            if not reachable:
                unreachable.append(f"{artifact} (not reachable from any entry point)")
        assert unreachable == [], (
            f"Preset '{preset.name}': unreachable required artifacts:\n" +
            "\n".join(f"  - {u}" for u in unreachable)
        )

    def test_required_kits_have_artifacts(self, preset):
        """Every required kit must have at least one artifact in the preset."""
        artifact_kits = {a.split(":")[0] for a in preset.required_artifacts}
        missing = [k for k in preset.required_kits if k not in artifact_kits]
        assert missing == [], (
            f"Preset '{preset.name}': required kits with no artifacts: {missing}"
        )

    def test_all_artifact_kits_are_known(self, preset):
        """Every artifact's kit prefix must be a known kit."""
        for artifact in preset.required_artifacts:
            kit = artifact.split(":")[0]
            assert kit in KIT_REGISTRY, (
                f"Preset '{preset.name}': artifact {artifact} references "
                f"unknown kit '{kit}'"
            )


class TestPresetCompleteness:
    """Verify presets cover the expected scenarios."""

    def test_at_least_five_presets_defined(self):
        assert len(PRESET_DEFINITIONS) >= 5, (
            f"Expected at least 5 presets, found {len(PRESET_DEFINITIONS)}"
        )

    def test_pik_entry_preset_exists(self):
        pik_presets = [p for p in PRESET_DEFINITIONS if p.entry_point == "PIK:WCR"]
        assert len(pik_presets) >= 1, "No preset starts at PIK:WCR"

    def test_eek_path_b_preset_exists(self):
        eek_presets = [p for p in PRESET_DEFINITIONS if p.entry_point == "EEK:KER"]
        assert len(eek_presets) >= 1, "No preset starts at EEK:KER (Path B)"

    def test_incident_preset_exists(self):
        odk_presets = [p for p in PRESET_DEFINITIONS if p.entry_point == "ODK:DCR"]
        assert len(odk_presets) >= 1, "No preset starts at ODK:DCR (incident)"

    def test_exploratory_preset_is_terminal(self):
        """Exploratory research preset should not require downstream pipeline kits."""
        exploratory = [p for p in PRESET_DEFINITIONS if p.name == "Exploratory Research"]
        assert len(exploratory) == 1
        p = exploratory[0]
        downstream_kits = {"REK", "RRK", "IEK"}
        required_downstream = downstream_kits & set(p.required_kits)
        assert required_downstream == set(), (
            f"Exploratory preset should not require downstream pipeline kits, "
            f"but requires: {required_downstream}"
        )
