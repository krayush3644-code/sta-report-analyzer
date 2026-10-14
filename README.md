# Automated STA Report Analyzer

A Python-based tool for analyzing Static Timing Analysis (STA)
reports and extracting useful timing information.

## Project goals

- Parse supported STA timing reports.
- Analyze setup and hold timing checks.
- Calculate WNS, TNS, and violation counts.
- Identify critical paths and endpoints.
- Analyze cell and net delay characteristics.
- Investigate high-fanout nets and buffer/inverter chains
  when the required report information is available.
- Compare timing results across multiple reports.
- Generate CSV exports and an HTML dashboard.

## Learning objectives

This project combines:
- Digital timing fundamentals
- Static Timing Analysis
- Python programming
- Automated testing
- Data analysis and visualization
- Git and GitHub workflows

## Current status

Under development. Report formats, supported metrics, and
validation coverage will be documented as implementation progresses.

## Important limitation

The analyzer interprets information available in its supported
reports. It is an analysis aid, not a replacement for a sign-off
STA tool.