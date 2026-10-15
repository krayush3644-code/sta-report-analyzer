
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.parser import parse_timing_points


report_path = (
    PROJECT_ROOT
    / "data"
    / "sample_reports"
    / "detailed_path.rpt"
)

report_text = report_path.read_text(encoding="utf-8")
points = parse_timing_points(report_text)

for point in points:
    print(
        f"{point['kind']:4} | "
        f"{point['point']:10} | "
        f"Incr: {point['incremental_delay_ns']:.2f} ns | "
        f"Path: {point['cumulative_delay_ns']:.2f} ns"
    )

cell_delay = sum(
    point["incremental_delay_ns"]
    for point in points
    if point["kind"] == "CELL"
)

net_delay = sum(
    point["incremental_delay_ns"]
    for point in points
    if point["kind"] == "NET"
)

print(f"\nTotal cell delay: {cell_delay:.2f} ns")
print(f"Total net delay:  {net_delay:.2f} ns")
print(f"Total path delay: {cell_delay + net_delay:.2f} ns")
