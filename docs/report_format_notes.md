# Report Format Notes

## Purpose

This document describes the simplified educational timing-report formats targeted by the STA Report Analyzer. It is not a complete specification for PrimeTime or any other commercial STA tool.

## 1. Path-level fields

The parser's simplified path format uses fields such as:

```text
Startpoint: REG_0001
Endpoint: REG_0001_D
Path Group: core_clock
Path Type: max

Data Arrival Time    0.200
Data Required Time   0.225
slack (MET)           0.025
```

The parser recognizes:
- `Startpoint`
- `Endpoint`
- `Path Group`
- `Path Type`
- `Data Arrival Time`
- `Data Required Time`
- `slack (...)`

A path must contain the required fields expected by the validator. Missing or malformed fields may cause a path to be marked invalid.

## 2. Pipe-separated timing-point rows

The synthetic reports use rows similar to:

```text
Kind | Point       | Incr  | Path
CELL | REG_0001/Q  | 0.070 | 0.070
NET  | net_0001    | 0.040 | 0.110
CELL | U_0001/Y    | 0.090 | 0.200
```

The `Kind` field identifies cell or net rows. `Incr` is the incremental delay, and `Path` is the cumulative delay in this simplified example.

## 3. Multiple paths

Each path begins with a `Startpoint:` line. The parser splits the report into path blocks at these lines and extracts fields from each block.

For a mixed report, each block should declare its own `Path Type`, such as `max` or `min`. The metrics module groups paths according to the parsed path-type field.

## 4. Timing-point section recognition

The parser recognizes educational headings that indicate:
- Data path
- Clock path
- Launch clock path
- Capture clock path

Clock-path timing points should not be included in data-path delay summaries. Classification depends on recognizable headings and point rows, so unusual report layouts may not be interpreted correctly.

## 5. Important limitations

- The parser targets a controlled set of educational examples.
- Commercial STA tools have options that change report structure, columns, labels, and path detail.
- A row that does not match a supported pattern may be skipped.
- The parser should not infer cell/net classification where the row does not provide enough evidence.
- A syntactically parsed report is not necessarily semantically complete or suitable for sign-off.
- Do not use proprietary reports unless you have authorization to process them. Use sanitized or educational examples for development.

## 6. Validation workflow for a new format

1. Save a small, sanitized sample report.
2. Identify the path-level fields and timing-point columns.
3. Write down which lines represent data paths and clock paths.
4. Run the parser and inspect the parsed path records.
5. Compare parsed values with the source report manually.
6. Add parser tests for valid, invalid, and edge-case blocks.
7. Run the full test suite with `python -m pytest -q`.
8. Document any unsupported sections or assumptions before extending the parser.
