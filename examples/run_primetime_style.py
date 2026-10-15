
from pathlib import Path
import sys

# Make the src package importable when running from the repository.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.parser import (
    parse_timing_report,
    parse_timing_points,
    validate_timing_points,
)

from sta_analyzer.pipeline import analyze_report_text

report_path = PROJECT_ROOT / "data" / "sample_reports" / "primetime_style.rpt"
report_text = report_path.read_text(encoding="utf-8")

print("=== PRIMETIME-STYLE REPORT TEST ===")
print(f"Report: {report_path.name}")

# Parse path-level information.
path = parse_timing_report(report_text)
print("\n=== PATH SUMMARY ===")
print(path)

# Parse individual timing points.
points = parse_timing_points(report_text)
print("\n=== RAW PARSED TIMING POINTS ===")
for point in points:
    print(point)
print("\n=== TIMING POINTS ===")

for point in points:
    print(
        f'{point["kind"]:7} | {point["point"]} | '
        f'Incr: {point["incremental_delay_ns"]:.2f} ns | '
        f'Path: {point["cumulative_delay_ns"]:.2f} ns'
    )

# Check cumulative-delay consistency.
warnings = validate_timing_points(points)
print("\n=== TIMING-POINT VALIDATION ===")
print(warnings if warnings else "No timing-point warnings.")

print("\n=== FULL PIPELINE TEST ===")
result = analyze_report_text(report_text)

print("Analyzed paths:", result["analyzed_path_count"])
print("Invalid paths:", result["invalid_path_count"])
print("Metrics:", result["metrics_by_type"])
print("Delay summaries:", result["delay_summaries_by_path"])