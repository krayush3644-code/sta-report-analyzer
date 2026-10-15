
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sta_analyzer.diagnostics import (  # pyright: ignore[reportMissingImports]
    rank_worst_paths,
    get_violating_endpoints,
)

from sta_analyzer.diagnostics import (  # pyright: ignore[reportMissingImports]
    rank_worst_paths,
    get_violating_endpoints,
    classify_delay_dominance,
    analyze_buffer_chain,
    find_high_fanout_nets,
)

class TestTimingDiagnostics(unittest.TestCase):

    def setUp(self):
        self.paths = [
            {
                "startpoint": "REG_A",
                "endpoint": "REG_B",
                "slack_ns": 0.25,
            },
            {
                "startpoint": "REG_C",
                "endpoint": "REG_D",
                "slack_ns": -0.40,
            },
            {
                "startpoint": "REG_E",
                "endpoint": "REG_F",
                "slack_ns": -0.12,
            },
        ]

    def test_rank_worst_paths(self):
        ranked = rank_worst_paths(self.paths)

        self.assertEqual(ranked[0]["endpoint"], "REG_D")
        self.assertEqual(ranked[1]["endpoint"], "REG_F")

    def test_limit_number_of_paths(self):
        ranked = rank_worst_paths(self.paths, limit=2)

        self.assertEqual(len(ranked), 2)

    def test_only_negative_slack_paths_are_violations(self):
        violations = get_violating_endpoints(self.paths)

        self.assertEqual(len(violations), 2)
        self.assertEqual(
            [item["endpoint"] for item in violations],
            ["REG_D", "REG_F"],
        )
        
    def test_cell_dominated_delay(self):
        self.assertEqual(
            classify_delay_dominance(1.5, 0.5),
            "cell-dominated",
        )

    def test_net_dominated_delay(self):
        self.assertEqual(
            classify_delay_dominance(0.4, 1.6),
            "net-dominated",
        )

    def test_balanced_delay(self):
        self.assertEqual(
            classify_delay_dominance(1.0, 1.0),
            "balanced",
        )

    def test_missing_or_invalid_delay(self):
        self.assertEqual(
            classify_delay_dominance(None, 1.0),
            "unknown",
        )
        self.assertEqual(
            classify_delay_dominance(-0.1, 1.0),
            "unknown",
        )
        self.assertEqual(
            classify_delay_dominance(0.0, 0.0),
            "unknown",
        )
        
    
    def test_buffer_chain_counts_cells(self):
        cells = [
            "REG_A",
            "BUF_X1",
            "BUF_X2",
            "NAND_X1",
            "INV_X1",
            "BUF_X1",
            "REG_B",
        ]

        result = analyze_buffer_chain(cells)

        self.assertEqual(result["buffer_inverter_count"], 4)
        self.assertEqual(result["longest_chain"], 2)


    def test_buffer_chain_without_buffers(self):
        cells = ["REG_A", "NAND_X1", "AND_X1", "REG_B"]

        result = analyze_buffer_chain(cells)

        self.assertEqual(result["buffer_inverter_count"], 0)
        self.assertEqual(result["longest_chain"], 0)


    def test_empty_buffer_chain(self):
        result = analyze_buffer_chain([])

        self.assertEqual(result["buffer_inverter_count"], 0)
        self.assertEqual(result["longest_chain"], 0)

    
    def test_finds_and_sorts_high_fanout_nets(self):
        nets = [
            {"name": "net_A", "fanout": 4},
            {"name": "net_B", "fanout": 35},
            {"name": "net_C", "fanout": 20},
            {"name": "net_D", "fanout": 80},
        ]

        result = find_high_fanout_nets(nets, threshold=20)

        self.assertEqual(
            result,
            [
                {"name": "net_D", "fanout": 80},
                {"name": "net_B", "fanout": 35},
            ],
        )


    def test_custom_fanout_threshold(self):
        nets = [
            {"name": "net_A", "fanout": 8},
            {"name": "net_B", "fanout": 12},
        ]

        result = find_high_fanout_nets(nets, threshold=10)

        self.assertEqual(
            result,
            [{"name": "net_B", "fanout": 12}],
        )


    def test_ignores_invalid_fanout_values(self):
        nets = [
            {"name": "net_A", "fanout": None},
            {"name": "net_B", "fanout": -3},
            {"name": "net_C", "fanout": "50"},
            {"name": "net_D"},
            {"name": "net_E", "fanout": True},
        ]

        result = find_high_fanout_nets(nets, threshold=20)

        self.assertEqual(result, [])


    def test_rejects_negative_threshold(self):
        with self.assertRaises(ValueError):
            find_high_fanout_nets([], threshold=-1)


if __name__ == "__main__":
    unittest.main()
