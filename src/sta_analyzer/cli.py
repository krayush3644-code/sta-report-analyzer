
import argparse
from pathlib import Path

from sta_analyzer.pipeline import analyze_report_text
from sta_analyzer.exports import export_csv, export_html

def main():
    parser = argparse.ArgumentParser(
        description="Analyze a supported STA timing report."
    )
    parser.add_argument(
        "report",
        type=Path,
        help="Path to the STA report text file",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sta_output"),
        help="Directory for generated CSV and HTML reports",
    )
    args = parser.parse_args()

    if not args.report.is_file():
        parser.error(f"Report file not found: {args.report}")

    try:
        report_text = args.report.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        parser.error(f"Could not read report: {exc}")

    result = analyze_report_text(report_text)

    export_csv(result, args.out)
    html_path = export_html(
        result,
        args.report.name,
        args.out / "sta_report.html",
    )

    print(f"\nCSV exports saved to: {args.out.resolve()}")
    print(f"HTML dashboard saved to: {html_path.resolve()}")

    print("=== STA REPORT ANALYSIS ===")
    print(f"Report: {args.report.name}")
    print(f"Timing points: {result['timing_point_count']}")
    print(f"Analyzed paths: {result['analyzed_path_count']}")
    print(f"Invalid paths: {result['invalid_path_count']}")

    print("\n=== TIMING METRICS ===")
    for path_type, metrics in result["metrics_by_type"].items():
        print(f"\nPath type: {path_type}")
        print(f"Path count: {metrics['path_count']}")
        print(f"Violations: {metrics['violation_count']}")
        print(f"WNS: {metrics['wns_ns']:.3f} ns")
        print(f"TNS: {metrics['tns_ns']:.3f} ns")

    print("\n=== INVESTIGATION PRIORITY ===")
    if not result["ranked_paths"]:
        print("No paths had sufficient valid data for scoring.")
    else:
        for path in result["ranked_paths"]:
            print(
                f"{path['startpoint']} -> {path['endpoint']} | "
                f"Slack: {path['slack_ns']:.3f} ns | "
                f"Score: {path['investigation_score']}"
            )

    warnings = (
        result["path_warnings"]
        + result["timing_point_warnings"]
    )
    print("\n=== DATA QUALITY WARNINGS ===")
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("No data-quality warnings found.")


if __name__ == "__main__":
    main()
