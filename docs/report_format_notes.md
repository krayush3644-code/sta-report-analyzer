# STA Report Format Notes

## Purpose

This document records the structure and meaning of Static Timing Analysis (STA) reports for the STA Report Analyzer project.

## Important Timing Report Fields

- **Startpoint:** Beginning of the data path.
- **Endpoint:** Destination of the data path.
- **Path Group:** Timing group associated with the path.
- **Path Type:** Indicates whether the report analyzes a maximum-delay or minimum-delay path.
- **Data Arrival Time:** Time at which data reaches the endpoint.
- **Data Required Time:** Timing threshold against which arrival time is checked.
- **Slack:** Timing margin. Negative slack indicates a timing violation.
- **Cell Delay:** Delay through a cell.
- **Net Delay:** Delay through an interconnect.

## Parser Design Notes

- Report layouts vary between tools and report commands.
- The parser must distinguish setup and hold paths.
- Numeric values and units must be handled consistently.
- Missing or malformed fields should be detected rather than silently interpreted.
- Parsed results must be validated against known expected results.

## Current Limitation

No production STA report format has been selected yet. The initial parser will use a clearly documented sample format and will not claim compatibility with every STA tool.
