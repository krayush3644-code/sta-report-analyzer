
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.parser import parse_multiple_timing_paths_file  # pyright: ignore[reportMissingImports]
from sta_analyzer.metrics import calculate_metrics_by_path_type   # pyright: ignore[reportMissingImports]


report_path = (
    PROJECT_ROOT
    / "data"
    / "sample_reports"
    / "multiple_paths.rpt"
)

paths = parse_multiple_timing_paths_file(report_path)
results = calculate_metrics_by_path_type(paths)

for path_type, metrics in results.items():
    print(f"\nPath type: {path_type}")
    print(f"Total paths: {metrics['path_count']}")
    print(f"Violations: {metrics['violation_count']}")
    print(f"WNS: {metrics['wns_ns']:.2f} ns")
    print(f"TNS: {metrics['tns_ns']:.2f} ns")
    print(
        "Violating endpoints:",
        ", ".join(metrics["violating_endpoints"]) or "None",
    )
