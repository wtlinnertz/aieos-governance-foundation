#!/usr/bin/env python3
"""
validate-sherpa-run.py — Config-driven post-run analysis for sherpa integration tests.

Loads a preset config from configs/<preset>.json and runs the checks specified there.
Each check function is registered by name and only executed if listed in the config's
hard_checks or soft_checks arrays.

Usage: python3 validate-sherpa-run.py <preset> <run_dir> <project_dir>
"""

import json
import re
import sys
from pathlib import Path


# ─── Config Loading ──────────────────────────────────────────────────────────

def load_config(preset: str) -> dict:
    """Load preset config from configs/<preset>.json."""
    config_dir = Path(__file__).parent / "configs"
    config_path = config_dir / f"{preset}.json"
    if not config_path.exists():
        print(f"  ERROR  Config not found: {config_path}")
        sys.exit(1)
    return json.loads(config_path.read_text())


# ─── Check Functions ─────────────────────────────────────────────────────────
# Each returns a list of issue strings (empty = pass).

def check_ar_origin(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Check that every assumption in the AR has an Origin field."""
    issues = []
    ar_files = list(project_dir.glob("docs/sdlc/*ar*.md"))
    if not ar_files:
        issues.append("AR file not found")
        return issues

    ar_content = ar_files[0].read_text()
    asm_count = len(re.findall(r"### ASM-\d+", ar_content))
    origin_count = len(re.findall(r"\|\s*Origin\s*\|", ar_content, re.IGNORECASE))

    if asm_count == 0:
        issues.append("No assumptions found in AR")
    elif origin_count < asm_count:
        issues.append(
            f"AR has {asm_count} assumptions but only {origin_count} Origin fields"
        )

    origin_values = re.findall(
        r"\|\s*Origin\s*\|\s*(.+?)\s*\|", ar_content, re.IGNORECASE
    )
    for val in origin_values:
        val_clean = val.strip()
        if val_clean not in ("User-stated", "AI-derived"):
            issues.append(f"Invalid Origin value: '{val_clean}' (expected User-stated or AI-derived)")

    return issues


def check_el_draft(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Check that EL is Draft, not Frozen."""
    issues = []
    el_files = list(project_dir.glob("docs/sdlc/*el*.md"))
    if not el_files:
        issues.append("EL file not found")
        return issues

    el_content = el_files[0].read_text()
    if "Status | Frozen" in el_content or "| Frozen | Yes |" in el_content:
        issues.append("EL should be Draft (results pending), but found Frozen status")

    return issues


def check_routing_record(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Check routing record exists and references correct preset."""
    issues = []
    rr_path = project_dir / "docs/sdlc/00-routing-record.md"
    if not rr_path.exists():
        candidates = list(project_dir.glob("docs/sdlc/*routing*.md"))
        if not candidates:
            issues.append("Routing record not found")
            return issues
        rr_path = candidates[0]

    rr_content = rr_path.read_text()
    preset = config["preset"]
    preset_name = config["preset_name"]

    if preset not in rr_content and preset_name not in rr_content:
        issues.append(f"Routing record does not reference {preset} or {preset_name}")

    return issues


def check_er_completeness(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Check ER has artifact IDs for all expected artifacts."""
    issues = []
    initiative = config["initiative_pattern"]

    # Find ER file case-insensitively
    er_candidates = (
        list(project_dir.glob(f"docs/engagement/er-*{initiative.lower()}*.md")) +
        list(project_dir.glob(f"docs/engagement/er-*{initiative.upper()}*.md")) +
        list(project_dir.glob(f"docs/engagement/er-*{initiative}*.md"))
    )
    # Deduplicate
    seen = set()
    er_files = []
    for p in er_candidates:
        if p not in seen:
            seen.add(p)
            er_files.append(p)

    if not er_files:
        issues.append("Engagement Record not found")
        return issues

    er_content = er_files[0].read_text()

    for pattern_template in config.get("er_artifact_patterns", []):
        pattern = pattern_template.replace("{INIT}", initiative)
        label = pattern.split("-")[0]  # e.g., "WCR"
        if not re.search(pattern, er_content):
            issues.append(f"ER missing artifact ID for {label} (expected pattern: {pattern})")

    return issues


def check_frozen_artifacts(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Check that artifacts marked frozen in config actually have Frozen status."""
    issues = []
    for artifact in config.get("expected_artifacts", []):
        if not artifact.get("frozen", False):
            continue
        glob_pattern = artifact["glob"]
        files = list(project_dir.glob(f"docs/sdlc/{glob_pattern}.md"))
        if not files:
            # Existence is checked separately by the driver
            continue
        content = files[0].read_text()
        if "Frozen" not in content:
            issues.append(f"{files[0].name} should be Frozen but is not")

    return issues


def check_provenance(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Check that AI-generated artifacts have provenance fields."""
    issues = []
    provenance_fields = [
        "Governance Model Version",
        "Spec Version",
    ]

    # Check all artifacts except intake, routing-record, and non-frozen EL
    skip_types = {"routing-record", "intake"}
    for artifact in config.get("expected_artifacts", []):
        if artifact["type"] in skip_types:
            continue
        # Skip human-authored artifacts
        if artifact["type"] in ("WCR", "intake"):
            continue
        glob_pattern = artifact["glob"]
        files = list(project_dir.glob(f"docs/sdlc/{glob_pattern}.md"))
        for f in files:
            content = f.read_text()
            for field in provenance_fields:
                if field not in content:
                    issues.append(f"{f.name} missing provenance field: {field}")

    return issues


def check_no_ready_prompts(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Check session transcript for 'Ready?' prompts."""
    issues = []
    transcript = run_dir / "session-transcript.md"
    if not transcript.exists():
        return issues

    content = transcript.read_text()
    # Strip self-assessment and summary sections that may discuss the term
    search_content = re.split(
        r'##\s+(?:\d+\.\s+)?"?Ready\b|## Summary|## Session Statistics|## Utility Prompts',
        content, flags=re.IGNORECASE
    )[0]
    ready_matches = re.findall(
        r"[Rr]eady\s*(to\s+(proceed|continue|move|go))?\s*\?", search_content
    )
    if ready_matches:
        issues.append(
            f"Session transcript contains {len(ready_matches)} 'Ready?' prompt(s)"
        )

    return issues


def check_utility_prompts_mentioned(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Check that utility prompts were actively offered."""
    issues = []
    output_log = run_dir / "claude-output.log"
    transcript = run_dir / "session-transcript.md"

    content = ""
    if output_log.exists():
        content = output_log.read_text()
    elif transcript.exists():
        content = transcript.read_text()

    if not content:
        return issues

    offer_patterns = [
        r"optional.{0,20}(step|tool|prompt)",
        r"(want|like)\s+to\s+(run|try|do).{0,30}(stress|adversarial|brownfield|stakeholder)",
        r"before\s+we\s+(design|generate|move).{0,30}(stress|adversarial)",
        r"assumption.stress.test",
    ]
    found = any(re.search(pat, content, re.IGNORECASE) for pat in offer_patterns)
    if not found:
        issues.append(
            "No utility prompts actively offered during session (sherpa should offer assumption stress test before EL)"
        )

    return issues


def check_kit_transition_explanations(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Verify kit transitions are mentioned in transcript."""
    issues = []
    transitions = config.get("kit_transitions", [])
    if not transitions:
        return issues

    output_log = run_dir / "claude-output.log"
    transcript = run_dir / "session-transcript.md"

    content = ""
    if output_log.exists():
        content = output_log.read_text()
    elif transcript.exists():
        content = transcript.read_text()

    if not content:
        issues.append("No transcript available to check kit transitions")
        return issues

    for transition in transitions:
        # Transition format: "PIK→EEK" or "ODK→EEK"
        kits = re.split(r"[→>-]", transition)
        if len(kits) < 2:
            continue
        from_kit = kits[0].strip()
        to_kit = kits[1].strip()

        # Look for any mention of transitioning between the kits
        patterns = [
            rf"{from_kit}.*{to_kit}",
            rf"Layer\s+\d+.*Layer\s+\d+",
            rf"(transition|move|handoff|hand.off|proceed).*({from_kit}|{to_kit})",
        ]
        found = any(re.search(pat, content, re.IGNORECASE) for pat in patterns)
        if not found:
            issues.append(f"Kit transition {transition} not explained in transcript")

    return issues


def check_cross_cutting_adoption(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Verify ER notes adoption decisions for cross-cutting kits."""
    issues = []

    er_candidates = list(project_dir.glob("docs/engagement/er-*.md"))
    if not er_candidates:
        return issues

    er_content = er_candidates[0].read_text()

    # Look for cross-cutting adoption language
    adoption_patterns = [
        r"(adopt|decline|skip|defer).{0,30}(QAK|SCK|DCK|DKK|PRK|BPK|PINFK)",
        r"(QAK|SCK|DCK|DKK|PRK|BPK|PINFK).{0,30}(adopt|decline|skip|defer|not.adopted|not.required)",
        r"cross.cutting.{0,30}(decision|adoption)",
    ]
    found = any(re.search(pat, er_content, re.IGNORECASE) for pat in adoption_patterns)
    if not found:
        issues.append("ER does not document cross-cutting kit adoption decisions")

    return issues


def check_convergence_loop(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Verify that a validation failure occurred and was corrected (retry evidence)."""
    issues = []

    output_log = run_dir / "claude-output.log"
    transcript = run_dir / "session-transcript.md"

    content = ""
    if output_log.exists():
        content = output_log.read_text()
    elif transcript.exists():
        content = transcript.read_text()

    if not content:
        issues.append("No transcript available to check convergence loop")
        return issues

    # Look for evidence of validation failure followed by retry
    fail_patterns = [
        r"FAIL",
        r"validation.{0,20}fail",
        r"did\s+not\s+pass",
        r"gate.{0,10}fail",
        r"blocking.issue",
    ]
    retry_patterns = [
        r"(retry|re.?generat|correct|fix|revis|update).{0,30}(intake|artifact|section|content)",
        r"(clean|remov).{0,30}(solution|product|vendor|pricing)",
        r"second.{0,20}(attempt|pass|try)",
        r"convergence",
    ]

    has_fail = any(re.search(pat, content, re.IGNORECASE) for pat in fail_patterns)
    has_retry = any(re.search(pat, content, re.IGNORECASE) for pat in retry_patterns)

    if not has_fail:
        issues.append("No validation failure evidence found (convergence loop requires initial FAIL)")
    if not has_retry:
        issues.append("No retry/correction evidence found (convergence loop requires correction attempt)")

    return issues


def check_ker_justification(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Verify KER exists and contains Path B justification."""
    issues = []
    ker_files = list(project_dir.glob("docs/sdlc/*ker*.md"))
    if not ker_files:
        issues.append("KER file not found (required for Path B entry)")
        return issues

    ker_content = ker_files[0].read_text()

    # Check for Path B justification content
    path_b_patterns = [
        r"Path\s*B",
        r"direct\s+entry",
        r"bypass.{0,20}discovery",
        r"scope.{0,20}(understood|known|clear|defined)",
    ]
    found = any(re.search(pat, ker_content, re.IGNORECASE) for pat in path_b_patterns)
    if not found:
        issues.append("KER does not contain Path B justification")

    return issues


def check_no_force_routing(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Verify sherpa asked clarifying question instead of force-routing."""
    issues = []

    output_log = run_dir / "claude-output.log"
    transcript = run_dir / "session-transcript.md"

    content = ""
    if output_log.exists():
        content = output_log.read_text()
    elif transcript.exists():
        content = transcript.read_text()

    if not content:
        issues.append("No transcript available to check routing behavior")
        return issues

    # Look for evidence of clarifying question
    clarify_patterns = [
        r"(clarif|understand|tell\s+me\s+more|could\s+you|can\s+you)",
        r"(which|what).{0,30}(describe|best|closer|sound)",
        r"(few|some).{0,20}question",
        r"(help\s+me|let\s+me).{0,20}understand",
    ]
    found = any(re.search(pat, content, re.IGNORECASE) for pat in clarify_patterns)
    if not found:
        issues.append("No clarifying question found — sherpa may have force-routed")

    return issues


def check_el_pause_outcome(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Verify EL has pause/stop outcome (negative experiment results)."""
    issues = []
    el_files = list(project_dir.glob("docs/sdlc/*el*.md"))
    if not el_files:
        issues.append("EL file not found")
        return issues

    el_content = el_files[0].read_text()

    pause_patterns = [
        r"(pause|stop|halt|discontinue|do\s+not\s+proceed)",
        r"(below|under|did\s+not\s+meet).{0,30}(threshold|falsification|target)",
        r"outcome.{0,20}(pause|stop|negative|fail)",
    ]
    found = any(re.search(pat, el_content, re.IGNORECASE) for pat in pause_patterns)
    if not found:
        issues.append("EL does not indicate pause/stop outcome for negative results")

    return issues


def check_no_dprd(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Verify that no DPRD was generated (expected for pause outcomes)."""
    issues = []
    dprd_files = list(project_dir.glob("docs/sdlc/*dprd*.md"))
    if dprd_files:
        issues.append(f"DPRD was generated ({dprd_files[0].name}) but should not exist for pause outcome")
    return issues


def check_session_resumption(config: dict, run_dir: Path, project_dir: Path) -> list[str]:
    """Verify sherpa discovered existing ER and resumed from correct position."""
    issues = []

    output_log = run_dir / "claude-output.log"
    transcript = run_dir / "session-transcript.md"

    content = ""
    if output_log.exists():
        content = output_log.read_text()
    elif transcript.exists():
        content = transcript.read_text()

    if not content:
        issues.append("No transcript available to check session resumption")
        return issues

    # Look for evidence of discovering existing state
    resume_patterns = [
        r"(found|discover|detect|see|existing).{0,30}(ER|engagement|artifact|progress)",
        r"(resum|continu|pick\s+up).{0,20}(where|from|session)",
        r"(current|existing).{0,20}(position|state|progress)",
    ]
    found = any(re.search(pat, content, re.IGNORECASE) for pat in resume_patterns)
    if not found:
        issues.append("No evidence sherpa discovered existing ER and resumed session")

    return issues


# ─── Check Registry ──────────────────────────────────────────────────────────
# Maps check name (used in config JSON) to function

CHECK_REGISTRY: dict[str, callable] = {
    "ar_origin":                    check_ar_origin,
    "el_draft":                     check_el_draft,
    "routing_record":               check_routing_record,
    "er_completeness":              check_er_completeness,
    "frozen_artifacts":             check_frozen_artifacts,
    "provenance":                   check_provenance,
    "no_ready_prompts":             check_no_ready_prompts,
    "utility_prompts_mentioned":    check_utility_prompts_mentioned,
    "kit_transition_explanations":  check_kit_transition_explanations,
    "cross_cutting_adoption":       check_cross_cutting_adoption,
    "convergence_loop":             check_convergence_loop,
    "ker_justification":            check_ker_justification,
    "no_force_routing":             check_no_force_routing,
    "el_pause_outcome":             check_el_pause_outcome,
    "no_dprd":                      check_no_dprd,
    "session_resumption":           check_session_resumption,
}


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <preset> <run_dir> <project_dir>")
        sys.exit(1)

    preset = sys.argv[1]
    run_dir = Path(sys.argv[2])
    project_dir = Path(sys.argv[3])

    config = load_config(preset)

    preset_label = config.get("preset_name", preset)
    print(f"\n  Sherpa {config['preset']} Post-Analysis ({preset_label})")
    print("  " + "─" * 40)

    all_issues = []

    # Run hard checks
    hard_check_names = config.get("hard_checks", [])
    hard_results = []
    for name in hard_check_names:
        fn = CHECK_REGISTRY.get(name)
        if fn is None:
            print(f"  SKIP  {name} (unknown check)")
            continue
        issues = fn(config, run_dir, project_dir)
        hard_results.append((name, issues))

    # Run soft checks
    soft_check_names = config.get("soft_checks", [])
    soft_results = []
    for name in soft_check_names:
        fn = CHECK_REGISTRY.get(name)
        if fn is None:
            print(f"  SKIP  {name} (unknown check)")
            continue
        issues = fn(config, run_dir, project_dir)
        soft_results.append((name, issues))

    # Print hard check results
    for name, issues in hard_results:
        if issues:
            print(f"  FAIL  {name}")
            for issue in issues:
                print(f"         └─ {issue}")
            all_issues.extend(issues)
        else:
            print(f"  PASS  {name}")

    # Print soft check results
    for name, issues in soft_results:
        if issues:
            print(f"  WARN  {name} (non-deterministic LLM behavior)")
            for issue in issues:
                print(f"         └─ {issue}")
        else:
            print(f"  PASS  {name}")

    print("  " + "─" * 40)

    # Write results
    total = len(hard_results) + len(soft_results)
    results = {
        "preset": config["preset"],
        "total_checks": total,
        "passed": sum(1 for _, issues in hard_results + soft_results if not issues),
        "failed": sum(1 for _, issues in hard_results if issues),
        "warned": sum(1 for _, issues in soft_results if issues),
        "issues": all_issues,
    }

    results_file = run_dir / "post-analysis.json"
    results_file.write_text(json.dumps(results, indent=2))
    print(f"  Results written to: {results_file}")

    if all_issues:
        print(f"\n  Result: FAIL ({len(all_issues)} issue(s))")
        return 1
    else:
        print("\n  Result: PASS")
        return 0


if __name__ == "__main__":
    sys.exit(main())
