
import re
from pathlib import Path


NUMBER = r"([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)"


def extract_field(pattern, text):
    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.MULTILINE,
    )
    return match.group(1).strip() if match else None


def parse_timing_report(report_text):
    """Parse one path in our simplified report format."""
    result = {
        "startpoint": extract_field(
            r"^\s*Startpoint:\s*(.+?)\s*$", report_text
        ),
        "endpoint": extract_field(
            r"^\s*Endpoint:\s*(.+?)\s*$", report_text
        ),
        "path_group": extract_field(
            r"^\s*Path Group:\s*(.+?)\s*$", report_text
        ),
        "path_type": extract_field(
            r"^\s*Path Type:\s*(\S+)", report_text
        ),
    }

    for field, pattern in {
        "arrival_time_ns": rf"^\s*Data Arrival Time\s+{NUMBER}",
        "required_time_ns": rf"^\s*Data Required Time\s+{NUMBER}",
        "slack_ns": rf"^\s*slack\s+\(\w+\)\s+{NUMBER}",
    }.items():
        value = extract_field(pattern, report_text)
        result[field] = float(value) if value is not None else None

    return result


def validate_timing_path(path):
    """Return validation warnings for a parsed timing path."""

    warnings = []

    required_fields = (
        "startpoint",
        "endpoint",
        "path_type",
        "slack_ns",
    )

    for field in required_fields:
        value = path.get(field)

        if value is None or value == "":
            warnings.append(f"Missing required field: {field}")

    numeric_fields = (
        "arrival_time_ns",
        "required_time_ns",
        "slack_ns",
    )

    for field in numeric_fields:
        value = path.get(field)

        if value is not None and (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
        ):
            warnings.append(
                f"Invalid numeric field: {field}"
            )

    return warnings


def parse_timing_report_file(file_path):
    text = Path(file_path).read_text(encoding="utf-8")
    return parse_timing_report(text)


def parse_multiple_timing_paths(report_text):
    """Parse all Startpoint-delimited blocks in our sample format."""
    blocks = re.split(
        r"(?=^\s*Startpoint:)",
        report_text,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    paths = []

    for block in blocks:
        if not re.search(r"^\s*Startpoint:", block, re.IGNORECASE | re.MULTILINE):
            continue

        path = parse_timing_report(block)

        # Required fields for this version of our parser.
        required_fields = (
            "startpoint",
            "endpoint",
            "path_type",
            "slack_ns",
        )

        if all(path[field] is not None for field in required_fields):
            paths.append(path)

    return paths


def parse_multiple_timing_paths_file(file_path):
    text = Path(file_path).read_text(encoding="utf-8")
    return parse_multiple_timing_paths(text)


def parse_timing_points(report_text):
    """Parse timing-point rows in our educational report format."""
    points = []

    for line in report_text.splitlines():
        parts = [part.strip() for part in line.split("|")]

        if len(parts) != 4:
            continue

        kind, point, incr_text, path_text = parts

        if kind.upper() not in {"CELL", "NET"}:
            continue

        try:
            incremental_delay = float(incr_text)
            cumulative_delay = float(path_text)
        except ValueError:
            continue

        points.append({
            "kind": kind.upper(),
            "point": point,
            "incremental_delay_ns": incremental_delay,
            "cumulative_delay_ns": cumulative_delay,
        })

    return points


def validate_timing_points(points, tolerance=1e-6):
    """Check cumulative delays against incremental delays.

    Intended for our educational report format, where each
    cumulative value is the running sum of incremental delays.
    """

    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")

    warnings = []
    expected_cumulative = 0.0

    for index, point in enumerate(points, start=1):
        incremental = point["incremental_delay_ns"]
        cumulative = point["cumulative_delay_ns"]

        expected_cumulative += incremental

        if abs(cumulative - expected_cumulative) > tolerance:
            warnings.append(
                f"Point {index} ({point['point']}): "
                f"expected cumulative delay "
                f"{expected_cumulative:.6f} ns, "
                f"got {cumulative:.6f} ns"
            )

    return warnings

