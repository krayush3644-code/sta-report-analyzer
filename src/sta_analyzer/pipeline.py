
from sta_analyzer.parser import (
    parse_multiple_timing_paths,
    parse_timing_points,
    validate_timing_path,
    validate_timing_points,
)
from sta_analyzer.metrics import calculate_metrics_by_path_type
from sta_analyzer.diagnostics import rank_paths_for_investigation
from sta_analyzer.diagnostics import summarize_delays_by_path

def partition_valid_paths(paths):
    """Separate paths that pass validation from invalid paths."""

    valid_paths = []
    invalid_paths = []
    warnings = []

    for index, path in enumerate(paths, start=1):
        path_warnings = validate_timing_path(path)

        if path_warnings:
            invalid_paths.append(path)

            for warning in path_warnings:
                warnings.append(
                    f"Path {index}: {warning}"
                )
        else:
            valid_paths.append(path)

    return valid_paths, invalid_paths, warnings

def analyze_report_text(report_text):
    """Run an integrated analysis on one detailed educational report."""

    paths = parse_multiple_timing_paths(report_text)
    timing_points = parse_timing_points(report_text)
    delay_summaries_by_path = summarize_delays_by_path(timing_points)

    valid_paths, invalid_paths, path_warnings = (
        partition_valid_paths(paths)
    )

    timing_point_warnings = validate_timing_points(
        timing_points
    )

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
    
    # Match each parsed path with its own delay summary.
    summaries_by_key = {
        (summary["startpoint"], summary["endpoint"]): summary
        for summary in delay_summaries_by_path
    }

    for path in paths:
        key = (path.get("startpoint"), path.get("endpoint"))
        summary = summaries_by_key.get(key)

        if summary is None:
            path["cell_delay_ns"] = None
            path["net_delay_ns"] = None
            path["total_delay_ns"] = None
            path["net_delay_share"] = None
            path["buffer_count"] = 0
            continue

        cell_delay = summary["cell_delay_ns"]
        net_delay = summary["net_delay_ns"]
        total_delay = summary["total_delay_ns"]

        path["cell_delay_ns"] = cell_delay
        path["net_delay_ns"] = net_delay
        path["total_delay_ns"] = total_delay
        path["net_delay_share"] = (
            net_delay / total_delay if total_delay > 0 else None
        )

        # Count recognized buffers/inverters only on this path.
        path["buffer_count"] = sum(
            1
            for point in timing_points
            if point.get("startpoint") == key[0]
            and point.get("endpoint") == key[1]
            and point["kind"] == "CELL"
            and (
                "BUF" in point["point"].upper()
                or "INV" in point["point"].upper()
            )
        )


    metrics_by_type = calculate_metrics_by_path_type(valid_paths)

    # A missing net-delay share cannot be scored, so skip such paths.
    scoreable_paths = [
        path for path in valid_paths
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
        "path_warnings": path_warnings,
        "timing_point_warnings": timing_point_warnings,
        "analyzed_path_count": len(valid_paths),
        "invalid_path_count": len(invalid_paths),
        "delay_summaries_by_path": delay_summaries_by_path,
    }