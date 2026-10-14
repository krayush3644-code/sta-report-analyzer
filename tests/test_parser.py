
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.parser import (       # pyright: ignore[reportMissingImports]
    parse_timing_report,
    parse_multiple_timing_paths,
    parse_multiple_timing_paths_file,
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


if __name__ == "__main__":
    unittest.main()
