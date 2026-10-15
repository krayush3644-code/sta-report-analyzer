
from sta_analyzer.parser import (
    parse_multiple_timing_paths,
    parse_timing_points,
)
from sta_analyzer.metrics import calculate_metrics_by_path_type
from sta_analyzer.diagnostics import rank_paths_for_investigation


def analyze_report_text(report_text):
    """Run an integrated analysis on one detailed educational report."""

    paths = parse_multiple_timing_paths(report_text)
    timing_points = parse_timing_points(report_text)

    # Calculate cell and net delay from the parsed timing points.
    cell_delay_ns = sum(
        point["incremental_delay_ns"]
        for point in timing_points
        if point["kind"] == "CELL"
    )

    net_delay_ns = sum(
        point["incremental_delay_ns"]
        for point in timing_points
        if point["kind"] == "NET"
    )

    total_delay_ns = cell_delay_ns + net_delay_ns

    net_delay_share = (
        net_delay_ns / total_delay_ns
        if total_delay_ns > 0
        else None
    )

    # Count only cells whose names match our BUF/INV heuristic.
    recognized_buffer_count = sum(
        1
        for point in timing_points
        if point["kind"] == "CELL"
        and (
            "BUF" in point["point"].upper()
            or "INV" in point["point"].upper()
        )
    )

    # The current detailed sample contains one path.
    # Attach its derived data to that path.
    for path in paths:
        path["cell_delay_ns"] = cell_delay_ns
        path["net_delay_ns"] = net_delay_ns
        path["net_delay_share"] = net_delay_share
        path["buffer_count"] = recognized_buffer_count

    metrics_by_type = calculate_metrics_by_path_type(paths)

    # A missing net-delay share cannot be scored, so skip such paths.
    scoreable_paths = [
        path for path in paths
        if path["net_delay_share"] is not None
    ]

    ranked_paths = rank_paths_for_investigation(scoreable_paths)

    return {
        "metrics_by_type": metrics_by_type,
        "timing_point_count": len(timing_points),
        "cell_delay_ns": cell_delay_ns,
        "net_delay_ns": net_delay_ns,
        "total_delay_ns": total_delay_ns,
        "ranked_paths": ranked_paths,
    }
