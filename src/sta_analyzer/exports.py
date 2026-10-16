
import csv
import html
from pathlib import Path


def _write_csv(path, rows, fieldnames):
    """Write dictionaries to CSV, ignoring fields not selected for export."""
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)



def export_csv(result, output_dir):
    """Export timing metrics, ranked paths, and delay summaries."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics_rows = []
    for path_type, metrics in result["metrics_by_type"].items():
        metrics_rows.append({
            "path_type": path_type,
            "path_count": metrics["path_count"],
            "violation_count": metrics["violation_count"],
            "wns_ns": metrics["wns_ns"],
            "tns_ns": metrics["tns_ns"],
            "violating_endpoints": "; ".join(
                metrics["violating_endpoints"]
            ),
        })

    # Export timing metrics.
    _write_csv(
        output_dir / "timing_metrics.csv",
        metrics_rows,
        [
            "path_type",
            "path_count",
            "violation_count",
            "wns_ns",
            "tns_ns",
            "violating_endpoints",
        ],
    )

    # Export ranked paths.
    _write_csv(
        output_dir / "ranked_paths.csv",
        result["ranked_paths"],
        [
            "startpoint",
            "endpoint",
            "path_type",
            "path_group",
            "slack_ns",
            "arrival_time_ns",
            "required_time_ns",
            "cell_delay_ns",
            "net_delay_ns",
            "total_delay_ns",
            "net_delay_share",
            "buffer_count",
            "investigation_score",
        ],
    )

    # Export per-path delay summaries.
    _write_csv(
        output_dir / "delay_summaries.csv",
        result["delay_summaries_by_path"],
        [
            "startpoint",
            "endpoint",
            "cell_delay_ns",
            "net_delay_ns",
            "total_delay_ns",
        ],
    )

    return output_dir


def export_html(result, report_name, output_path):
    """Create a self-contained HTML summary of an analysis."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    def esc(value):
        return html.escape(str(value))

    # Group every valid path into a slack range for visualization.
    slack_bins = [
        ("Below -0.1 ns", lambda slack: slack < -0.1),
        ("-0.1 to 0 ns", lambda slack: -0.1 <= slack < 0),
        ("0 to 0.1 ns", lambda slack: 0 <= slack <= 0.1),
        ("Above 0.1 ns", lambda slack: slack > 0.1),
    ]

    slack_distribution = [
        {
            "label": label,
            "count": sum(
                1 for slack in result.get("all_valid_slacks", [])
                if condition(slack)
            ),
        }
        for label, condition in slack_bins
    ]

    max_bin_count = max(
        (item["count"] for item in slack_distribution),
        default=0,
    )

    slack_chart_rows = []
    for item in slack_distribution:
        bar_width = (
            item["count"] / max_bin_count * 100
            if max_bin_count else 0
        )
        slack_chart_rows.append(
            "<div class='slack-row'>"
            f"<span>{esc(item['label'])}</span>"
            "<div class='bar-track'>"
            f"<div class='bar' style='width:{bar_width:.2f}%'></div>"
            "</div>"
            f"<strong>{item['count']}</strong>"
            "</div>"
        )

    metric_rows = []
    for path_type, metrics in result["metrics_by_type"].items():
        metric_rows.append(
            "<tr>"
            f"<td>{esc(path_type)}</td>"
            f"<td>{metrics['path_count']}</td>"
            f"<td>{metrics['violation_count']}</td>"
            f"<td>{metrics['wns_ns']:.3f}</td>"
            f"<td>{metrics['tns_ns']:.3f}</td>"
            "</tr>"
        )

    path_rows = []
    for path in result["ranked_paths"]:
        path_rows.append(
            "<tr>"
            f"<td>{esc(path.get('startpoint'))}</td>"
            f"<td>{esc(path.get('endpoint'))}</td>"
            f"<td>{path['slack_ns']:.3f}</td>"
            f"<td>{path.get('investigation_score', '')}</td>"
            "</tr>"
        )

    delay_rows = []
    for item in result["delay_summaries_by_path"]:
        delay_rows.append(
            "<tr>"
            f"<td>{esc(item['startpoint'])}</td>"
            f"<td>{esc(item['endpoint'])}</td>"
            f"<td>{item['cell_delay_ns']:.3f}</td>"
            f"<td>{item['net_delay_ns']:.3f}</td>"
            f"<td>{item['total_delay_ns']:.3f}</td>"
            "</tr>"
        )

    warnings = (
        result["path_warnings"] + result["timing_point_warnings"]
    )
    warning_html = (
        "".join(f"<li>{esc(warning)}</li>" for warning in warnings)
        if warnings else "<li>No data-quality warnings.</li>"
    )

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>STA Analysis - {esc(report_name)}</title>
<style>
body {{ font-family: Arial, sans-serif; max-width: 1100px;
       margin: 32px auto; padding: 0 18px; color: #202938; }}
h1, h2 {{ color: #17365d; }}
.cards {{ display: flex; flex-wrap: wrap; gap: 14px; }}
.card {{ border: 1px solid #d5dbe5; border-radius: 8px;
         padding: 16px; min-width: 150px; }}
table {{ width: 100%; border-collapse: collapse; margin: 14px 0 28px; }}
th, td {{ border: 1px solid #d5dbe5; padding: 9px; text-align: left; }}
th {{ background: #edf2f8; }}
.note {{ color: #596579; font-size: 0.92rem; }}
.slack-row {{
    display: grid;
    grid-template-columns: 130px minmax(80px, 1fr) 45px;
    align-items: center;
    gap: 12px;
    margin: 12px 0;
}}
.bar-track {{
    background: #edf2f8;
    border-radius: 4px;
    overflow: hidden;
    height: 20px;
}}
.bar {{
    background: #4776b4;
    height: 100%;
    min-width: 0;
}}
@media (max-width: 520px) {{
    .slack-row {{
        grid-template-columns: 105px minmax(50px, 1fr) 35px;
        gap: 7px;
        font-size: 0.85rem;
    }}
}}
</style>
</head>
<body>
<h1>Automated STA Report Analyzer</h1>
<p><strong>Input report:</strong> {esc(report_name)}</p>

<div class="cards">
  <div class="card"><strong>Timing points</strong>
    <p>{result['timing_point_count']}</p></div>
  <div class="card"><strong>Analyzed paths</strong>
    <p>{result['analyzed_path_count']}</p></div>
  <div class="card"><strong>Invalid paths</strong>
    <p>{result['invalid_path_count']}</p></div>
  <div class="card"><strong>Total cell delay</strong>
    <p>{result['cell_delay_ns']:.3f} ns</p></div>
  <div class="card"><strong>Total net delay</strong>
    <p>{result['net_delay_ns']:.3f} ns</p></div>
</div>

<h2>Slack distribution</h2>
<p class="note">
  Distribution of all valid analyzed paths by slack range.
  Negative slack indicates a timing violation.
</p>
<div>
  {''.join(slack_chart_rows)}
</div>

<h2>Timing metrics by path type</h2>
<table>
<thead><tr><th>Path type</th><th>Paths</th><th>Violations</th>
<th>WNS (ns)</th><th>TNS (ns)</th></tr></thead>
<tbody>{''.join(metric_rows)}</tbody>
</table>

<h2>Investigation priority</h2>
<table>
<thead><tr><th>Startpoint</th><th>Endpoint</th><th>Slack (ns)</th>
<th>Score</th></tr></thead>
<tbody>{''.join(path_rows) or '<tr><td colspan="4">No ranked paths.</td></tr>'}</tbody>
</table>

<h2>Per-path delay summaries</h2>
<table>
<thead><tr><th>Startpoint</th><th>Endpoint</th><th>Cell (ns)</th>
<th>Net (ns)</th><th>Total (ns)</th></tr></thead>
<tbody>{''.join(delay_rows) or '<tr><td colspan="5">No delay summaries.</td></tr>'}</tbody>
</table>

<h2>Data-quality warnings</h2>
<ul>{warning_html}</ul>
<p class="note">Educational analysis aid. Verify results with your
approved STA sign-off tools before making engineering decisions.</p>
</body>
</html>
"""

    output_path.write_text(document, encoding="utf-8")
    return output_path
