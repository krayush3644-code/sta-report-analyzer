
import csv

from sta_analyzer.exports import export_csv, export_html


def make_sample_result():
    """Build a small, predictable result without needing an input report."""
    return {
        "timing_point_count": 3,
        "analyzed_path_count": 1,
        "invalid_path_count": 0,
        "cell_delay_ns": 0.30,
        "net_delay_ns": 0.20,
        "total_delay_ns": 0.50,
        "metrics_by_type": {
            "max": {
                "path_count": 1,
                "violation_count": 1,
                "wns_ns": -0.15,
                "tns_ns": -0.15,
                "violating_endpoints": ["REG_B"],
            }
        },
        "ranked_paths": [
            {
                "startpoint": "REG_A",
                "endpoint": "REG_B",
                "path_type": "max",
                "path_group": "core_clock",
                "slack_ns": -0.15,
                "arrival_time_ns": 0.85,
                "required_time_ns": 0.70,
                "cell_delay_ns": 0.30,
                "net_delay_ns": 0.20,
                "total_delay_ns": 0.50,
                "net_delay_share": 0.40,
                "buffer_count": 1,
                "investigation_score": 3,
            }
        ],
        "delay_summaries_by_path": [
            {
                "startpoint": "REG_A",
                "endpoint": "REG_B",
                "cell_delay_ns": 0.30,
                "net_delay_ns": 0.20,
                "total_delay_ns": 0.50,
            }
        ],
        "path_warnings": [],
        "timing_point_warnings": [],
    }


def test_export_csv_creates_all_files(tmp_path):
    result = make_sample_result()

    output_dir = export_csv(result, tmp_path / "csv_output")

    assert (output_dir / "timing_metrics.csv").is_file()
    assert (output_dir / "ranked_paths.csv").is_file()
    assert (output_dir / "delay_summaries.csv").is_file()


def test_export_csv_preserves_expected_path_data(tmp_path):
    result = make_sample_result()
    output_dir = export_csv(result, tmp_path)

    with (output_dir / "ranked_paths.csv").open(
        newline="", encoding="utf-8"
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["startpoint"] == "REG_A"
    assert rows[0]["endpoint"] == "REG_B"
    assert float(rows[0]["slack_ns"]) == -0.15
    assert rows[0]["investigation_score"] == "3"


def test_export_csv_includes_metric_values(tmp_path):
    result = make_sample_result()
    output_dir = export_csv(result, tmp_path)

    with (output_dir / "timing_metrics.csv").open(
        newline="", encoding="utf-8"
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["path_type"] == "max"
    assert rows[0]["violation_count"] == "1"
    assert float(rows[0]["wns_ns"]) == -0.15
    assert float(rows[0]["tns_ns"]) == -0.15


def test_export_html_contains_report_summary(tmp_path):
    result = make_sample_result()
    output_path = tmp_path / "html_output" / "sta_report.html"

    returned_path = export_html(
        result,
        "sample_report.rpt",
        output_path,
    )

    assert returned_path.is_file()

    content = returned_path.read_text(encoding="utf-8")
    assert "Automated STA Report Analyzer" in content
    assert "sample_report.rpt" in content
    assert "REG_A" in content
    assert "REG_B" in content
    assert "-0.150" in content


def test_export_html_escapes_report_name(tmp_path):
    result = make_sample_result()

    output_path = export_html(
        result,
        "<script>alert('test')</script>.rpt",
        tmp_path / "report.html",
    )

    content = output_path.read_text(encoding="utf-8")

    assert "<script>alert('test')</script>.rpt" not in content
    assert "&lt;script&gt;" in content


def test_export_html_handles_empty_results(tmp_path):
    result = make_sample_result()
    result["metrics_by_type"] = {}
    result["ranked_paths"] = []
    result["delay_summaries_by_path"] = []
    result["path_warnings"] = []
    result["timing_point_warnings"] = []

