
def calculate_metrics(paths):
    """Calculate timing metrics for a group of parsed paths."""

    valid_paths = [
        path
        for path in paths
        if isinstance(path.get("slack_ns"), (int, float))
    ]

    slacks = [path["slack_ns"] for path in valid_paths]
    violations = [
        path for path in valid_paths
        if path["slack_ns"] < 0
    ]

    # Project convention: WNS is zero when there are no violations.
    wns_ns = min(
        (path["slack_ns"] for path in violations),
        default=0.0,
    )

    # TNS is the sum of negative slack values.
    tns_ns = sum(
        path["slack_ns"] for path in violations
    )

    return {
        "path_count": len(valid_paths),
        "violation_count": len(violations),
        "wns_ns": wns_ns,
        "tns_ns": tns_ns,
        "violating_endpoints": [
            path.get("endpoint")
            for path in violations
            if path.get("endpoint") is not None
        ],
    }


def calculate_metrics_by_path_type(paths):
    """Calculate separate metrics for each path type."""

    grouped_paths = {}

    for path in paths:
        path_type = path.get("path_type") or "unknown"
        grouped_paths.setdefault(path_type, []).append(path)

    return {
        path_type: calculate_metrics(group)
        for path_type, group in grouped_paths.items()
    }
