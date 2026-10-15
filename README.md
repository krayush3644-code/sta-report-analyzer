
# Automated STA Report Analyzer

A Python-based tool for parsing supported Static Timing Analysis (STA)
reports, calculating timing metrics, investigating critical paths, and
exporting results to CSV and HTML.

## Features

- Parse supported educational STA report formats.
- Extract setup/maximum-path and hold/minimum-path information when available.
- Calculate Worst Negative Slack (WNS), Total Negative Slack (TNS),
  and violation counts.
- Identify and rank paths for further investigation.
- Summarize cell and net delay information.
- Detect potential buffer/inverter chains and high-fanout nets when
  the required information is available.
- Validate parsed data and report data-quality warnings.
- Export timing metrics, ranked paths, and delay summaries to CSV.
- Generate a self-contained HTML analysis report.
- Run automated tests with pytest.

## Requirements

- Python 3.10 or newer recommended.
- Git (optional, for cloning and version control).

The project has been tested in a local Python virtual environment.
Your Python version may differ.

## Setup

Clone the repository and enter its directory:

```bash
git clone https://github.com/krayush3644-code/sta-report-analyzer.git
cd sta-report-analyzer
```

Create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the test dependency:

```bash
python -m pip install pytest
```

## Run the analyzer

From the repository root, set `PYTHONPATH` to the `src` directory.

**Windows PowerShell:**

```powershell
$env:PYTHONPATH = "src"
python -m sta_analyzer data/sample_reports/detailed_path.rpt --out output
```

The `--out` argument selects the output directory. If omitted, the
analyzer uses `sta_output`.

The command prints timing metrics and investigation priorities to the
terminal and creates these files:

- `timing_metrics.csv` — metrics grouped by path type.
- `ranked_paths.csv` — paths ranked for further investigation.
- `delay_summaries.csv` — cell, net, and total delay summaries.
- `sta_report.html` — a browser-readable HTML report.

Open the HTML report on Windows:

```powershell
Invoke-Item output\sta_report.html
```

## Run the tests

From the repository root:

```powershell
$env:PYTHONPATH = "src"
python -m pytest -q
```

Tests cover parsing, metrics, diagnostics, pipeline behavior, and CSV/HTML
exports.

## Example output

For the included `detailed_path.rpt` sample, the analyzer currently reports:

| Metric | Example result |
|---|---:|
| Analyzed paths | 1 |
| Invalid paths | 0 |
| WNS | -0.150 ns |
| TNS | -0.150 ns |
| Violations | 1 |

These values describe the included sample report, not a real chip design.

## Project structure

```text
sta-report-analyzer/
├── data/
│   └── sample_reports/
├── examples/
├── src/
│   └── sta_analyzer/
│       ├── __main__.py
│       ├── cli.py
│       ├── diagnostics.py
│       ├── exports.py
│       ├── metrics.py
│       ├── parser.py
│       └── pipeline.py
├── tests/
├── .gitignore
└── README.md
```

## Limitations

- The parser supports specific report formats; it is not a universal
  Synopsys PrimeTime report parser.
- Results depend on the information present in the input report.
- Heuristics for investigation priority, buffer/inverter identification,
  and high-fanout detection are analysis aids, not sign-off criteria.
- Always verify timing conclusions with approved STA sign-off tools.

## Learning objectives

This project combines digital timing fundamentals, Static Timing Analysis,
Python programming, automated testing, data analysis, and Git workflows.

The analyzer is an educational analysis aid, not a replacement for a
sign-off STA tool.
