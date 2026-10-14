
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.parser import parse_multiple_timing_paths_file

report_path = (
    PROJECT_ROOT / "data" / "sample_reports" / "multiple_paths.rpt"
)
paths = parse_multiple_timing_paths_file(report_path)

# For this controlled sample, max paths are analyzed separately
# from min paths. This is not a universal check-type classifier.
for path_type in ("max", "min"):
    selected = [
        path for path in paths
        if path["path_type"].lower() == path_type
    ]

    if not selected:
        continue

    slacks = [path["slack_ns"] for path in selected]
    violations = [slack for slack in slacks if slack < 0]

    print(f"\nPath type: {path_type}")
    print(f"Paths analyzed: {len(selected)}")
    print(f"Violations: {len(violations)}")
    print(f"Worst slack: {min(slacks):.2f} ns")
    print(f"Total negative slack: {sum(violations):.2f} ns")

    print("Violating paths:")
    for path in selected:
        if path["slack_ns"] < 0:
            print(
                f"  {path['startpoint']} -> {path['endpoint']}: "
                f"{path['slack_ns']:.2f} ns"
            )
