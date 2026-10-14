
# Educational example: timing metrics from parsed slack values.
# These values are synthetic, not from a real chip.

timing_checks = [
    {"path": "REG_A -> REG_B", "check": "setup", "slack_ns": 0.25},
    {"path": "REG_C -> REG_D", "check": "setup", "slack_ns": -0.40},
    {"path": "REG_E -> REG_F", "check": "hold", "slack_ns": 0.08},
    {"path": "REG_G -> REG_H", "check": "hold", "slack_ns": -0.12},
    {"path": "REG_J -> REG_K", "check": "setup", "slack_ns": -0.10},
]

for check_type in ("setup", "hold"):
    checks = [
        item for item in timing_checks
        if item["check"] == check_type
    ]

    slacks = [item["slack_ns"] for item in checks]
    violations = [slack for slack in slacks if slack < 0]

    wns = min(slacks) if slacks else None
    tns = sum(violations)

    print(f"\n{check_type.upper()} TIMING")
    print(f"Checks analyzed: {len(checks)}")
    print(f"Violations: {len(violations)}")
    print(f"WNS: {wns:.2f} ns" if wns is not None else "WNS: N/A")
    print(f"TNS: {tns:.2f} ns")
