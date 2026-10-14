
from pathlib import Path
import sys

# Allow Python to find our package inside the src folder.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.parser import parse_timing_report_file    # pyright: ignore[reportMissingImports]


report_path = (
    PROJECT_ROOT / "data" / "sample_reports" / "sample_setup.rpt"
)

result = parse_timing_report_file(report_path)

for field, value in result.items():
    print(f"{field}: {value}")
