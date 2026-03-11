#!/usr/bin/env python3
"""Post-run analysis for agent integration tests.

Reads the output directory from an integration test run and produces a summary
report: which artifacts were generated, which validations passed/failed, and
where the agent struggled.

Usage: python3 validate-run.py <run-directory>
"""

import json
import sys
from pathlib import Path


def analyze_run(run_dir: Path) -> dict:
    """Analyze a completed integration test run."""
    results = {
        "run_dir": str(run_dir),
        "artifacts": [],
        "validations": [],
        "errors": [],
        "summary": {
            "artifacts_generated": 0,
            "artifacts_expected": 0,
            "validations_pass": 0,
            "validations_fail": 0,
            "errors": 0,
        },
    }

    # Find all generated artifacts (markdown files, not logs/json)
    for md_file in sorted(run_dir.glob("*.md")):
        lines = md_file.read_text().count("\n")
        results["artifacts"].append({
            "file": md_file.name,
            "lines": lines,
            "size_bytes": md_file.stat().st_size,
        })
        results["summary"]["artifacts_generated"] += 1

    # Find all validation results
    for json_file in sorted(run_dir.glob("*-validation.json")):
        try:
            data = json.loads(json_file.read_text())
            status = data.get("status", "UNKNOWN")
            results["validations"].append({
                "file": json_file.name,
                "status": status,
                "summary": data.get("summary", ""),
                "hard_gates": data.get("hard_gates", {}),
                "blocking_issues": data.get("blocking_issues", []),
                "completeness_score": data.get("completeness_score", ""),
            })
            if status == "PASS":
                results["summary"]["validations_pass"] += 1
            else:
                results["summary"]["validations_fail"] += 1
        except (json.JSONDecodeError, KeyError) as e:
            results["errors"].append({
                "file": json_file.name,
                "error": f"Failed to parse validation JSON: {e}",
            })
            results["summary"]["errors"] += 1

    # Find error logs
    for error_log in sorted(run_dir.glob("*.error.log")):
        content = error_log.read_text()[:500]  # First 500 chars
        results["errors"].append({
            "file": error_log.name,
            "error": content,
        })
        results["summary"]["errors"] += 1

    return results


def print_report(results: dict):
    """Print a human-readable report."""
    summary = results["summary"]

    print()
    print("=" * 60)
    print(f"  Integration Test Run Analysis")
    print(f"  Directory: {results['run_dir']}")
    print("=" * 60)

    print()
    print("--- Artifacts Generated ---")
    if results["artifacts"]:
        for art in results["artifacts"]:
            print(f"  {art['file']:40s} {art['lines']:>5d} lines")
    else:
        print("  (none)")

    print()
    print("--- Validation Results ---")
    if results["validations"]:
        for val in results["validations"]:
            status_icon = "PASS" if val["status"] == "PASS" else "FAIL"
            print(f"  {status_icon}  {val['file']}")
            if val["summary"]:
                print(f"         {val['summary']}")
            if val["blocking_issues"]:
                for issue in val["blocking_issues"]:
                    desc = issue.get("description", str(issue))
                    print(f"         BLOCKER: {desc}")
            # Show hard gate results
            gates = val.get("hard_gates", {})
            if gates:
                failing = [g for g, s in gates.items() if s != "PASS"]
                if failing:
                    print(f"         Failing gates: {', '.join(failing)}")
    else:
        print("  (none)")

    print()
    print("--- Errors ---")
    if results["errors"]:
        for err in results["errors"]:
            print(f"  {err['file']}: {err['error'][:200]}")
    else:
        print("  (none)")

    print()
    print("--- Summary ---")
    print(f"  Artifacts generated: {summary['artifacts_generated']}")
    print(f"  Validations PASS:    {summary['validations_pass']}")
    print(f"  Validations FAIL:    {summary['validations_fail']}")
    print(f"  Errors:              {summary['errors']}")

    print()
    if summary["validations_fail"] > 0 or summary["errors"] > 0:
        print("  Result: ISSUES FOUND")
        return 1
    elif summary["artifacts_generated"] == 0:
        print("  Result: NO ARTIFACTS (agent may not have run)")
        return 1
    else:
        print("  Result: ALL PASS")
        return 0


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <run-directory>")
        sys.exit(1)

    run_dir = Path(sys.argv[1])
    if not run_dir.is_dir():
        print(f"Error: {run_dir} is not a directory")
        sys.exit(1)

    results = analyze_run(run_dir)
    exit_code = print_report(results)

    # Also write machine-readable results
    results_file = run_dir / "run-analysis.json"
    results_file.write_text(json.dumps(results, indent=2))
    print(f"\n  Full results: {results_file}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
