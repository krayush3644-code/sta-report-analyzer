
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.parser import parse_multiple_timing_paths_file  # type: ignore[reportMissingImports]

report_path = (
    PROJECT_ROOT / "data" / "sample_reports" / "multiple_paths.rpt"
)

paths = parse_multiple_timing_paths_file(report_path)

for index, path in enumerate(paths, start=1):
    print(f"\nPath {index}")
    for field, value in path.items():
        print(f"  {field}: {value}")

print(f"\nTotal paths parsed: {len(paths)}")
