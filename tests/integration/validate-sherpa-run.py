#!/usr/bin/env python3
"""
validate-sherpa-run.py — Post-run analysis for sherpa integration tests.

Checks behavioral requirements beyond artifact existence:
- AR has Origin field on every assumption
- EL is Draft (not Frozen)
- Routing record exists with correct preset
- ER has all artifact IDs populated
- No "Ready?" prompts in session transcript (fix #1)
- Utility prompts mentioned (fix #2)
- Provenance fields present in all artifacts

Usage: python3 validate-sherpa-run.py <run_dir> <project_dir>
"""

import json
import re
import sys
from pathlib import Path


def check_ar_origin(project_dir: Path) -> list[str]:
    """Check that every assumption in the AR has an Origin field."""
    issues = []
    ar_files = list(project_dir.glob("docs/sdlc/*ar*.md"))
    if not ar_files:
        issues.append("AR file not found")
        return issues

    ar_content = ar_files[0].read_text()
    # Count assumptions
    asm_count = len(re.findall(r"### ASM-\d+", ar_content))
    origin_count = len(re.findall(r"\|\s*Origin\s*\|", ar_content, re.IGNORECASE))

    if asm_count == 0:
        issues.append("No assumptions found in AR")
    elif origin_count < asm_count:
        issues.append(
            f"AR has {asm_count} assumptions but only {origin_count} Origin fields"
        )

    # Check for valid values
    origin_values = re.findall(
        r"\|\s*Origin\s*\|\s*(.+?)\s*\|", ar_content, re.IGNORECASE
    )
    for val in origin_values:
        val_clean = val.strip()
        if val_clean not in ("User-stated", "AI-derived"):
            issues.append(f"Invalid Origin value: '{val_clean}' (expected User-stated or AI-derived)")

    return issues


def check_el_draft(project_dir: Path) -> list[str]:
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


def check_routing_record(project_dir: Path) -> list[str]:
    """Check routing record exists and references P5."""
    issues = []
    rr_path = project_dir / "docs/sdlc/00-routing-record.md"
    if not rr_path.exists():
        # Try alternate names
        candidates = list(project_dir.glob("docs/sdlc/*routing*.md"))
        if not candidates:
            issues.append("Routing record not found (fix #4)")
            return issues
        rr_path = candidates[0]

    rr_content = rr_path.read_text()
    if "P5" not in rr_content and "Exploratory" not in rr_content:
        issues.append("Routing record does not reference P5 or Exploratory Research")

    return issues


def check_er_completeness(project_dir: Path) -> list[str]:
    """Check ER has artifact IDs for all generated artifacts."""
    issues = []
    # ER filename may be uppercase or lowercase — find case-insensitively
    er_candidates = list(project_dir.glob("docs/engagement/er-*icr*.md")) + \
                    list(project_dir.glob("docs/engagement/er-*ICR*.md"))
    if not er_candidates:
        issues.append("Engagement Record not found")
        return issues
    er_path = er_candidates[0]

    er_content = er_path.read_text()

    # Check that each artifact type has an ID with the initiative name.
    # Artifact ID format: {TYPE}-{INITIATIVE}-{NNN}
    expected_patterns = [
        ("WCR", r"WCR-AICR-\d+"),
        ("PFD", r"PFD-AICR-\d+"),
        ("VH", r"VH-AICR-\d+"),
        ("AR", r"AR-AICR-\d+"),
        ("EL", r"EL-AICR-\d+"),
    ]
    for name, pattern in expected_patterns:
        if not re.search(pattern, er_content):
            issues.append(f"ER missing artifact ID for {name} (expected pattern: {pattern})")

    return issues


def check_frozen_artifacts(project_dir: Path) -> list[str]:
    """Check that WCR, PFD, VH, AR are frozen."""
    issues = []
    should_be_frozen = ["wcr", "pfd", "vh", "ar"]

    for artifact_type in should_be_frozen:
        files = list(project_dir.glob(f"docs/sdlc/*{artifact_type}*.md"))
        if not files:
            continue
        content = files[0].read_text()
        if "Frozen" not in content:
            issues.append(f"{files[0].name} should be Frozen but is not")

    return issues


def check_provenance(project_dir: Path) -> list[str]:
    """Check that generated artifacts have provenance fields."""
    issues = []
    provenance_fields = [
        "Governance Model Version",
        "Spec Version",
    ]

    # Only check AI-generated artifacts (not intake)
    for pattern in ["*pfd*.md", "*vh*.md", "*ar*.md", "*el*.md"]:
        files = list(project_dir.glob(f"docs/sdlc/{pattern}"))
        for f in files:
            content = f.read_text()
            for field in provenance_fields:
                if field not in content:
                    issues.append(f"{f.name} missing provenance field: {field}")

    return issues


def check_no_ready_prompts(run_dir: Path) -> list[str]:
    """Check session transcript for 'Ready?' prompts (fix #1)."""
    issues = []
    transcript = run_dir / "session-transcript.md"
    if not transcript.exists():
        # Can't check without transcript
        return issues

    content = transcript.read_text()
    # Look for "Ready?" prompts in the actual flow, not in the self-assessment
    # section of the transcript (which discusses whether Ready? was asked).
    # Strip everything from the "Ready?" check section onward, plus any
    # summary/statistics section that may reference the term.
    search_content = re.split(
        r'##\s+(?:\d+\.\s+)?"?Ready\b|## Summary|## Session Statistics|## Utility Prompts',
        content, flags=re.IGNORECASE
    )[0]
    ready_matches = re.findall(
        r"[Rr]eady\s*(to\s+(proceed|continue|move|go))?\s*\?", search_content
    )
    if ready_matches:
        issues.append(
            f"Session transcript contains {len(ready_matches)} 'Ready?' prompt(s) (fix #1 not applied)"
        )

    return issues


def check_utility_prompts_mentioned(run_dir: Path) -> list[str]:
    """Check that utility prompts were mentioned (fix #2)."""
    issues = []
    transcript = run_dir / "session-transcript.md"
    output_log = run_dir / "claude-output.log"

    # Check the Claude output log (the actual conversation), not the transcript
    # summary (which may mention utility prompts in a "not offered" context).
    content = ""
    if output_log.exists():
        content = output_log.read_text()
    elif transcript.exists():
        content = transcript.read_text()

    if not content:
        return issues

    # Look for the sherpa actively offering a utility prompt — phrases like
    # "optional step", "want to run", "stress test your assumptions", etc.
    offer_patterns = [
        r"optional.{0,20}(step|tool|prompt)",
        r"(want|like)\s+to\s+(run|try|do).{0,30}(stress|adversarial|brownfield|stakeholder)",
        r"before\s+we\s+(design|generate|move).{0,30}(stress|adversarial)",
        r"assumption.stress.test",
    ]
    found = any(re.search(pat, content, re.IGNORECASE) for pat in offer_patterns)
    if not found:
        issues.append(
            "No utility prompts actively offered during session (fix #2 — sherpa should offer assumption stress test before EL)"
        )

    return issues


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <run_dir> <project_dir>")
        sys.exit(1)

    run_dir = Path(sys.argv[1])
    project_dir = Path(sys.argv[2])

    print("\n  Sherpa P5 Post-Analysis")
    print("  " + "─" * 40)

    all_issues = []

    # Hard checks — these cause FAIL
    hard_checks = [
        ("AR Origin field (fix #3)", check_ar_origin(project_dir)),
        ("EL Draft status", check_el_draft(project_dir)),
        ("Routing record (fix #4)", check_routing_record(project_dir)),
        ("ER completeness", check_er_completeness(project_dir)),
        ("Frozen artifacts", check_frozen_artifacts(project_dir)),
        ("Provenance fields", check_provenance(project_dir)),
        ("No 'Ready?' prompts (fix #1)", check_no_ready_prompts(run_dir)),
    ]

    # Soft checks — LLM behavioral, non-deterministic. WARN instead of FAIL.
    soft_checks = [
        ("Utility prompts mentioned (fix #2)", check_utility_prompts_mentioned(run_dir)),
    ]

    checks = hard_checks + soft_checks

    for name, issues in hard_checks:
        if issues:
            print(f"  FAIL  {name}")
            for issue in issues:
                print(f"         └─ {issue}")
            all_issues.extend(issues)
        else:
            print(f"  PASS  {name}")

    for name, issues in soft_checks:
        if issues:
            print(f"  WARN  {name} (non-deterministic LLM behavior)")
            for issue in issues:
                print(f"         └─ {issue}")
            # Warnings don't add to all_issues — they don't cause FAIL
        else:
            print(f"  PASS  {name}")

    print("  " + "─" * 40)

    # Write results
    results = {
        "total_checks": len(checks),
        "passed": sum(1 for _, issues in checks if not issues),
        "failed": sum(1 for _, issues in checks if issues),
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
