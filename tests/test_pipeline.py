
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


if __name__ == "__main__":
    unittest.main()
