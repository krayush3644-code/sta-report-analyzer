
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.metrics import (      # pyright: ignore[reportMissingImports]
    calculate_metrics,
    calculate_metrics_by_path_type,
)


class TestTimingMetrics(unittest.TestCase):

    def test_wns_tns_and_violation_count(self):
        paths = [
            {"endpoint": "REG_B", "slack_ns": 0.25},
            {"endpoint": "REG_D", "slack_ns": -0.40},
            {"endpoint": "REG_F", "slack_ns": -0.12},
        ]

        result = calculate_metrics(paths)

        self.assertEqual(result["path_count"], 3)
        self.assertEqual(result["violation_count"], 2)
        self.assertAlmostEqual(result["wns_ns"], -0.40)
        self.assertAlmostEqual(result["tns_ns"], -0.52)
        self.assertEqual(
            result["violating_endpoints"],
            ["REG_D", "REG_F"],
        )

    def test_no_violations(self):
        paths = [
            {"endpoint": "REG_B", "slack_ns": 0.25},
            {"endpoint": "REG_D", "slack_ns": 0.10},
        ]

        result = calculate_metrics(paths)

        self.assertEqual(result["violation_count"], 0)
        self.assertEqual(result["wns_ns"], 0.0)
        self.assertEqual(result["tns_ns"], 0.0)

    def test_groups_paths_by_type(self):
        paths = [
            {
                "endpoint": "REG_B",
                "path_type": "max",
                "slack_ns": -0.40,
            },
            {
                "endpoint": "REG_F",
                "path_type": "min",
                "slack_ns": -0.12,
            },
        ]

        results = calculate_metrics_by_path_type(paths)

        self.assertAlmostEqual(results["max"]["wns_ns"], -0.40)
        self.assertAlmostEqual(results["min"]["wns_ns"], -0.12)


if __name__ == "__main__":
    unittest.main()
