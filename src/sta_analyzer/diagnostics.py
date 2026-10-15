
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


def is_buffer_or_inverter(cell_name):
    """Return whether a cell name looks like a buffer or inverter."""
    if not isinstance(cell_name, str):
        return False

    name = cell_name.upper()

    return "BUF" in name or "INV" in name


def analyze_buffer_chain(cell_names):
    """Analyze buffer/inverter cells in the supplied path order."""
    if not cell_names:
        return {
            "buffer_inverter_count": 0,
            "longest_chain": 0,
        }

    total_count = 0
    current_chain = 0
    longest_chain = 0

    for cell_name in cell_names:
        if is_buffer_or_inverter(cell_name):
            total_count += 1
            current_chain += 1
            longest_chain = max(longest_chain, current_chain)
        else:
            current_chain = 0

    return {
        "buffer_inverter_count": total_count,
        "longest_chain": longest_chain,
    }


def find_high_fanout_nets(nets, threshold=20):
    """Return nets whose fanout exceeds the configured threshold.

    Each net should be a dictionary with:
        name: net name
        fanout: number of loads
    """
    if threshold < 0:
        raise ValueError("threshold must be non-negative")

    high_fanout_nets = []

    for net in nets:
        fanout = net.get("fanout")

        # Ignore missing, invalid, or negative fanout values.
        if isinstance(fanout, bool):
            continue

        if not isinstance(fanout, int) or fanout < 0:
            continue

        if fanout > threshold:
            high_fanout_nets.append({
                "name": net.get("name"),
                "fanout": fanout,
            })

    return sorted(
        high_fanout_nets,
        key=lambda net: net["fanout"],
        reverse=True,
    )

def score_path_for_investigation(
    slack_ns,
    net_delay_share,
    buffer_count,
):
    """Assign a simple investigation-priority score to a timing path.

    This is an educational heuristic, not a root-cause diagnosis.
    """
    score = 0

    if not isinstance(slack_ns, (int, float)) or isinstance(slack_ns, bool):
        return None

    if (
        not isinstance(net_delay_share, (int, float))
        or isinstance(net_delay_share, bool)
        or not 0 <= net_delay_share <= 1
    ):
        return None

    if (
        not isinstance(buffer_count, int)
        or isinstance(buffer_count, bool)
        or buffer_count < 0
    ):
        return None

    if slack_ns < 0:
        score += 3

    if net_delay_share >= 0.60:
        score += 2

    if buffer_count >= 3:
        score += 1

    return score

