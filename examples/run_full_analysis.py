
import sys
from pathlib import Path

# Make the src/ directory importable when running this script directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.pipeline import analyze_report_text


report_path = (
    PROJECT_ROOT / "data" / "sample_reports" / "detailed_path.rpt"
)

report_text = report_path.read_text(encoding="utf-8")
result = analyze_report_text(report_text)

print("=== STA REPORT ANALYSIS ===")
print(f"Report: {report_path.name}")
print(f"Timing points: {result['timing_point_count']}")

print("\n=== DELAY SUMMARY ===")
print(f"Cell delay:  {result['cell_delay_ns']:.2f} ns")
print(f"Net delay:   {result['net_delay_ns']:.2f} ns")
print(f"Total delay: {result['total_delay_ns']:.2f} ns")


# Display delay breakdown for each individual timing path.
print("\n=== PER-PATH DELAY SUMMARY ===")

delay_summaries = result.get("delay_summaries_by_path", [])

if not delay_summaries:
    print("No per-path delay summaries available.")
else:
    for summary in delay_summaries:
        print(
            f"{summary['startpoint']} -> {summary['endpoint']} | "
            f"Cell: {summary['cell_delay_ns']:.2f} ns | "
            f"Net: {summary['net_delay_ns']:.2f} ns | "
            f"Total: {summary['total_delay_ns']:.2f} ns"
        )

print("\n=== TIMING METRICS ===")
for path_type, metrics in result["metrics_by_type"].items():
    print(f"\nPath type: {path_type}")
    print(f"Path count: {metrics['path_count']}")
    print(f"Violations: {metrics['violation_count']}")
    print(f"WNS: {metrics['wns_ns']:.2f} ns")
    print(f"TNS: {metrics['tns_ns']:.2f} ns")

print(f"Analyzed paths: {result['analyzed_path_count']}")
print(f"Invalid paths:  {result['invalid_path_count']}")

print("\n=== INVESTIGATION PRIORITY ===")
if not result["ranked_paths"]:
    print("No paths had sufficient valid data for scoring.")
else:
    for path in result["ranked_paths"]:
        print(
            f"{path['startpoint']} -> {path['endpoint']} | "
            f"Slack: {path['slack_ns']:.2f} ns | "
            f"Net share: {path['net_delay_share']:.1%} | "
            f"Recognized buffers/inverters: {path['buffer_count']} | "
            f"Score: {path['investigation_score']}"
        )

print("\n=== DATA QUALITY WARNINGS ===")

all_warnings = (
    result["path_warnings"]
    + result["timing_point_warnings"]
)

if not all_warnings:
    print("No data-quality warnings found.")
else:
    for warning in all_warnings:
        print(f"- {warning}")
