
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.parser import parse_multiple_timing_paths_file    # pyright: ignore[reportMissingImports]
from sta_analyzer.diagnostics import rank_worst_paths               # pyright: ignore[reportMissingImports]


report_path = (
    PROJECT_ROOT
    / "data"
    / "sample_reports"
    / "multiple_paths.rpt"
)

paths = parse_multiple_timing_paths_file(report_path)
worst_paths = rank_worst_paths(paths, limit=3)

print("Worst timing paths")
print("-" * 60)

for index, path in enumerate(worst_paths, start=1):
    print(
        f"{index}. {path['startpoint']} -> {path['endpoint']} | "
        f"Type: {path['path_type']} | "
        f"Slack: {path['slack_ns']:.2f} ns"
    )
