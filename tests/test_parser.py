
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.parser import (       # pyright: ignore[reportMissingImports]
    parse_primetime_timing_row,
    parse_timing_report,
    parse_multiple_timing_paths,
    parse_multiple_timing_paths_file,
    parse_timing_points,
    validate_timing_points,
    
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
        
    def test_valid_timing_points_have_no_warnings(self):
        from sta_analyzer.parser import validate_timing_points

        points = [
            {
                "point": "REG_A/Q",
                "incremental_delay_ns": 0.10,
                "cumulative_delay_ns": 0.10,
            },
            {
                "point": "net_A",
                "incremental_delay_ns": 0.08,
                "cumulative_delay_ns": 0.18,
            },
            {
                "point": "U1/Y",
                "incremental_delay_ns": 0.20,
                "cumulative_delay_ns": 0.38,
            },
        ]

        self.assertEqual(validate_timing_points(points), [])

    def test_inconsistent_cumulative_delay_is_reported(self):
        from sta_analyzer.parser import validate_timing_points

        points = [
            {
                "point": "REG_A/Q",
                "incremental_delay_ns": 0.10,
                "cumulative_delay_ns": 0.10,
            },
            {
                "point": "net_A",
                "incremental_delay_ns": 0.08,
                "cumulative_delay_ns": 0.25,
            },
        ]

        warnings = validate_timing_points(points)

        self.assertEqual(len(warnings), 1)
        self.assertIn("net_A", warnings[0])
        self.assertIn("expected cumulative delay", warnings[0])

    def test_negative_tolerance_is_rejected(self):
        from sta_analyzer.parser import validate_timing_points

        with self.assertRaises(ValueError):
            validate_timing_points([], tolerance=-0.01)
            
    def test_parse_primetime_style_header(self):
        report = """
    Startpoint: REG_A (rising edge-triggered flip-flop)
    Endpoint: REG_B (rising edge-triggered flip-flop)
    Path Group: core_clock
    Path Type: max

    data arrival time 0.85
    data required time 0.70
    slack (VIOLATED) -0.15
    """

        path = parse_timing_report(report)

        self.assertEqual(path["startpoint"], "REG_A")
        self.assertEqual(path["endpoint"], "REG_B")
        self.assertEqual(path["path_group"], "core_clock")
        self.assertEqual(path["path_type"], "max")
        self.assertAlmostEqual(path["arrival_time_ns"], 0.85)
        self.assertAlmostEqual(path["required_time_ns"], 0.70)
        self.assertAlmostEqual(path["slack_ns"], -0.15)


    def test_parse_primetime_timing_row(self):
        line = (
            "U1/Y (NAND2_X1) "
            "1 0.01 0.05 0.20 0.38"
        )

        row = parse_primetime_timing_row(line)

        self.assertIsNotNone(row)
        self.assertEqual(row["point"], "U1/Y (NAND2_X1)")
        self.assertAlmostEqual(row["incremental_delay_ns"], 0.20)
        self.assertAlmostEqual(row["cumulative_delay_ns"], 0.38)


    def test_ignore_non_timing_table_line(self):
        row = parse_primetime_timing_row("data arrival time 0.85")
        self.assertIsNone(row)    
    
    def test_parse_primetime_style_timing_points(self):
        report_text = """
    Startpoint: REG_A (rising edge-triggered flip-flop)
    Endpoint: REG_B (rising edge-triggered flip-flop)
    Path Group: core_clock
    Path Type: max

    Point                         Fanout  Cap   Trans  Incr   Path
    REG_A/CK (DFF_X1)                  1  0.01   0.03  0.10   0.10
    REG_A/Q  (DFF_X1)                  2  0.02   0.04  0.08   0.18
    U1/Y     (NAND2_X1)                1  0.01   0.05  0.20   0.38

    data arrival time                                    0.38
    data required time                                   0.50
    slack (MET)                                          0.12
    """

        from sta_analyzer.parser import parse_timing_points

        points = parse_timing_points(report_text)

        self.assertEqual(len(points), 3)

        self.assertEqual(points[0]["point"], "REG_A/CK (DFF_X1)")
        self.assertAlmostEqual(points[0]["incremental_delay_ns"], 0.10)
        self.assertAlmostEqual(points[0]["cumulative_delay_ns"], 0.10)

        self.assertEqual(points[1]["point"], "REG_A/Q  (DFF_X1)")
        self.assertAlmostEqual(points[1]["incremental_delay_ns"], 0.08)
        self.assertAlmostEqual(points[1]["cumulative_delay_ns"], 0.18)

        self.assertEqual(points[2]["point"], "U1/Y     (NAND2_X1)")
        self.assertAlmostEqual(points[2]["incremental_delay_ns"], 0.20)
        self.assertAlmostEqual(points[2]["cumulative_delay_ns"], 0.38)


class TestTimingPointValidation(unittest.TestCase):

    def test_cumulative_delay_resets_for_each_path(self):
        points = [
            {
                "startpoint": "REG_A",
                "endpoint": "REG_B",
                "point": "REG_A/Q",
                "incremental_delay_ns": 0.10,
                "cumulative_delay_ns": 0.10,
                "kind": "CELL",
            },
            {
                "startpoint": "REG_A",
                "endpoint": "REG_B",
                "point": "U1/Y",
                "incremental_delay_ns": 0.08,
                "cumulative_delay_ns": 0.18,
                "kind": "CELL",
            },
            {
                "startpoint": "REG_C",
                "endpoint": "REG_D",
                "point": "REG_C/Q",
                "incremental_delay_ns": 0.20,
                "cumulative_delay_ns": 0.20,
                "kind": "CELL",
            },
            {
                "startpoint": "REG_C",
                "endpoint": "REG_D",
                "point": "U2/Y",
                "incremental_delay_ns": 0.05,
                "cumulative_delay_ns": 0.25,
                "kind": "CELL",
            },
        ]

        warnings = validate_timing_points(points)

        self.assertEqual(warnings, [])
                
if __name__ == "__main__":
    unittest.main()
