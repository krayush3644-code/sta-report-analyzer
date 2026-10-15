
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.parser import (       # pyright: ignore[reportMissingImports]
    parse_timing_report,
    parse_multiple_timing_paths,
    parse_multiple_timing_paths_file,
    parse_timing_points,
)


class TestTimingReportParser(unittest.TestCase):

    def test_single_path_fields(self):
        report = """
Startpoint: REG_A
Endpoint: REG_B
Path Group: core_clock
Path Type: max

Data Arrival Time    1.75
Data Required Time   2.00
slack (MET)          0.25
"""
        result = parse_timing_report(report)

        self.assertEqual(result["startpoint"], "REG_A")
        self.assertEqual(result["endpoint"], "REG_B")
        self.assertEqual(result["path_type"], "max")
        self.assertAlmostEqual(result["slack_ns"], 0.25)

    def test_sample_report_contains_three_paths(self):
        report_path = (
            PROJECT_ROOT
            / "data"
            / "sample_reports"
            / "multiple_paths.rpt"
        )

        paths = parse_multiple_timing_paths_file(report_path)

        self.assertEqual(len(paths), 3)
        self.assertAlmostEqual(paths[0]["slack_ns"], 0.25)
        self.assertAlmostEqual(paths[1]["slack_ns"], -0.40)
        self.assertAlmostEqual(paths[2]["slack_ns"], -0.12)

    def test_incomplete_path_is_skipped(self):
        report = """
Startpoint: REG_A
Endpoint: REG_B
Path Type: max
"""
        paths = parse_multiple_timing_paths(report)

        self.assertEqual(paths, [])

    def test_empty_report_returns_no_paths(self):
        paths = parse_multiple_timing_paths("")

        self.assertEqual(paths, [])
        
    
    def test_parse_timing_points(self):
        report = """
Kind | Point | Incr | Path
CELL | REG_A/Q | 0.10 | 0.10
NET | net_A | 0.08 | 0.18
CELL | U1/Y | 0.20 | 0.38
"""
        points = parse_timing_points(report)

        self.assertEqual(len(points), 3)
        self.assertEqual(points[0]["kind"], "CELL")
        self.assertEqual(points[1]["kind"], "NET")
        self.assertAlmostEqual(
            points[1]["incremental_delay_ns"], 0.08
        )
        self.assertAlmostEqual(
            points[2]["cumulative_delay_ns"], 0.38
        )

    def test_invalid_timing_point_row_is_skipped(self):
        report = """
CELL | REG_A/Q | 0.10 | 0.10
NET | net_A | invalid | 0.18
OTHER | unknown | 0.10 | 0.20
"""
        points = parse_timing_points(report)

        self.assertEqual(len(points), 1)
        self.assertEqual(points[0]["point"], "REG_A/Q")

    def test_valid_timing_path_has_no_warnings(self):
        from sta_analyzer.parser import validate_timing_path

        path = {
            "startpoint": "REG_A",
            "endpoint": "REG_B",
            "path_type": "max",
            "arrival_time_ns": 0.85,
            "required_time_ns": 0.70,
            "slack_ns": -0.15,
        }

        self.assertEqual(validate_timing_path(path), [])

    def test_missing_required_field_is_reported(self):
        from sta_analyzer.parser import validate_timing_path

        path = {
            "startpoint": "REG_A",
            "endpoint": None,
            "path_type": "max",
            "slack_ns": -0.15,
        }

        warnings = validate_timing_path(path)

        self.assertIn(
            "Missing required field: endpoint",
            warnings,
        )

    def test_invalid_numeric_field_is_reported(self):
        from sta_analyzer.parser import validate_timing_path

        path = {
            "startpoint": "REG_A",
            "endpoint": "REG_B",
            "path_type": "max",
            "arrival_time_ns": "not-a-number",
            "required_time_ns": 0.70,
            "slack_ns": -0.15,
        }

        warnings = validate_timing_path(path)

        self.assertIn(
            "Invalid numeric field: arrival_time_ns",
            warnings,
        )


if __name__ == "__main__":
    unittest.main()
