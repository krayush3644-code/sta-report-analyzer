
def rank_worst_paths(paths, limit=10):
    """Return paths with the lowest slack first."""

    valid_paths = [
        path
        for path in paths
        if isinstance(path.get("slack_ns"), (int, float))
    ]

    return sorted(
        valid_paths,
        key=lambda path: path["slack_ns"],
    )[:limit]


def get_violating_endpoints(paths):
    """Return endpoints associated with negative slack."""

    return [
        {
            "startpoint": path.get("startpoint"),
            "endpoint": path.get("endpoint"),
            "slack_ns": path["slack_ns"],
        }
        for path in rank_worst_paths(paths, limit=len(paths))
        if path["slack_ns"] < 0
    ]


def classify_delay_dominance(cell_delay_ns, net_delay_ns):
    """Classify which component dominates the supplied path delay."""

    if cell_delay_ns is None or net_delay_ns is None:
        return "unknown"

    if cell_delay_ns < 0 or net_delay_ns < 0:
        return "unknown"

    total_delay = cell_delay_ns + net_delay_ns

    if total_delay <= 0:
        return "unknown"

    cell_fraction = cell_delay_ns / total_delay
    net_fraction = net_delay_ns / total_delay

    # Project heuristic, not an industry-standard threshold.
    if cell_fraction >= 0.60:
        return "cell-dominated"

    if net_fraction >= 0.60:
        return "net-dominated"

    return "balanced"
