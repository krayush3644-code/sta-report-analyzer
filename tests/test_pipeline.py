
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.pipeline import analyze_report_text


class TestAnalysisPipeline(unittest.TestCase):

    def test_analyzes_detailed_sample_report(self):
        report_path = (
            PROJECT_ROOT
            / "data"
            / "sample_reports"
            / "detailed_path.rpt"
        )

        report_text = report_path.read_text(encoding="utf-8")
        result = analyze_report_text(report_text)

        self.assertEqual(result["timing_point_count"], 5)
        self.assertAlmostEqual(result["cell_delay_ns"], 0.45)
        self.assertAlmostEqual(result["net_delay_ns"], 0.40)
        self.assertAlmostEqual(result["total_delay_ns"], 0.85)

        self.assertIn("max", result["metrics_by_type"])
        self.assertEqual(
            result["metrics_by_type"]["max"]["violation_count"],
            1,
        )

        self.assertEqual(len(result["ranked_paths"]), 1)
        self.assertEqual(
            result["ranked_paths"][0]["endpoint"],
            "REG_B",
        )
        self.assertEqual(
            result["ranked_paths"][0]["investigation_score"],
            3,
        )
        
        self.assertEqual(result["path_warnings"], [])
        self.assertEqual(result["timing_point_warnings"], [])

    def test_partition_keeps_valid_paths(self):
        from sta_analyzer.pipeline import partition_valid_paths

        paths = [
            {
                "startpoint": "REG_A",
                "endpoint": "REG_B",
                "path_type": "max",
                "slack_ns": -0.15,
            },
            {
                "startpoint": "REG_C",
                "endpoint": None,
                "path_type": "max",
                "slack_ns": -0.30,
            },
        ]

        valid, invalid, warnings = partition_valid_paths(paths)

        self.assertEqual(len(valid), 1)
        self.assertEqual(valid[0]["endpoint"], "REG_B")
        self.assertEqual(len(invalid), 1)
        self.assertIsNone(invalid[0]["endpoint"])
        self.assertTrue(warnings)

    def test_partition_does_not_reject_valid_violation(self):
        from sta_analyzer.pipeline import partition_valid_paths

        paths = [
            {
                "startpoint": "REG_A",
                "endpoint": "REG_B",
                "path_type": "max",
                "slack_ns": -0.15,
            },
        ]

        valid, invalid, warnings = partition_valid_paths(paths)

        self.assertEqual(len(valid), 1)
        self.assertEqual(invalid, [])
        self.assertEqual(warnings, [])


    def test_calculates_delays_separately_for_two_paths(self):
        from sta_analyzer.pipeline import analyze_report_text

        report = """
    Startpoint: REG_A
    Endpoint: REG_B
    Path Group: core_clock
    Path Type: max

    Kind | Point | Incr | Path
    CELL | REG_A/Q | 0.10 | 0.10
    NET  | net_A   | 0.08 | 0.18
    CELL | U1/Y    | 0.20 | 0.38

    Data Arrival Time    0.38
    Data Required Time   0.50
    slack (MET)           0.12

    Startpoint: REG_C
    Endpoint: REG_D
    Path Group: core_clock
    Path Type: max

    Kind | Point | Incr | Path
    CELL | REG_C/Q | 0.15 | 0.15
    NET  | net_C   | 0.10 | 0.25
    CELL | U2/Y    | 0.30 | 0.55

    Data Arrival Time    0.55
    Data Required Time   0.70
    slack (MET)           0.15
    """

        result = analyze_report_text(report)

        summaries = {
            (item["startpoint"], item["endpoint"]): item
            for item in result["delay_summaries_by_path"]
        }

        path_a = summaries[("REG_A", "REG_B")]
        self.assertAlmostEqual(path_a["cell_delay_ns"], 0.30)
        self.assertAlmostEqual(path_a["net_delay_ns"], 0.08)
        self.assertAlmostEqual(path_a["total_delay_ns"], 0.38)

        path_b = summaries[("REG_C", "REG_D")]
        self.assertAlmostEqual(path_b["cell_delay_ns"], 0.45)
        self.assertAlmostEqual(path_b["net_delay_ns"], 0.10)
        self.assertAlmostEqual(path_b["total_delay_ns"], 0.55)


if __name__ == "__main__":
    unittest.main()
