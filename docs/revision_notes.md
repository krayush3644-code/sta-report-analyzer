# STA Report Analyzer — Revision Notes

## Project objective

Build a Python tool that parses supported STA reports, analyzes
timing checks, identifies critical paths, compares runs, and
generates useful reports.

## Current learning status

- [x] Project scope defined
- [x] Learning roadmap defined
- [x] Timing path introduced
- [x] Clock period and frequency introduced
- [x] Basic setup and hold concepts introduced
- [x] Detailed setup and hold slack derivations
- [x] Understand a real STA report
- [x] Implement report parser
- [x] Implement and test WNS/TNS calculations
- [x] Implement diagnostics and trend analysis
- [x] Generate HTML/CSV dashboard

## Core concepts

### Timing path
A sequence of timing points through which a signal propagates.

### Launch register
The register that launches data into a path.

### Capture register
The register that captures the propagated data.

### Setup check
Checks whether data arrives early enough before the capture edge.
Usually associated with maximum-delay analysis.

### Hold check
Checks whether data remains stable long enough after the capture
edge. Usually associated with minimum-delay analysis.

### Slack
Timing margin between the required and actual timing values.
Positive slack generally indicates a passing check; negative slack
indicates a violation.

### WNS
Worst slack among the selected timing checks. Clearly document
whether a tool reports minimum slack or clamps WNS to zero when
there are no violations.

### TNS
Sum of negative slack values for a defined set of violating checks.
The path/check selection rules must be documented.

## Essential equations

Clock frequency:
f = 1 / T_clock

Simplified setup requirement:
T_cq,max + T_data,max + T_setup <= T_clock

Simplified hold requirement:
T_cq,min + T_data,min >= T_hold

Setup slack in the simplified example:
T_clock - T_cq,max - T_data,max - T_setup

TNS:
Sum of the negative slack values included in the analysis.

## Important cautions

- Real STA calculations must account for clock arrival times,
  skew, uncertainty, timing constraints and the relevant check.
- Setup and hold must be analyzed separately.
- Never mix timing units.
- A parser must not silently accept malformed or incomplete reports.
- Validate computed metrics against known expected results.
- The analyzer is not a replacement for sign-off STA.

## Current milestone

Milestone 0: repository and documentation setup.
Milestone 1: STA fundamentals.

## Next session

Complete repository setup, study setup/hold slack in greater detail,
and analyze a small example timing report.

## Clock-aware setup and hold

Clock skew convention:
S = t_capture - t_launch

Positive skew means the capture clock arrives later.

### Setup

Latest data arrival:
A_max = t_launch + t_cq,max + t_data,max

Required arrival time:
R_setup = T_clock + t_capture - t_setup - U_setup

Setup slack:
S_setup = R_setup - A_max

Simplified clock-aware equation:
S_setup = T_clock + S - t_cq,max - t_data,max
          - t_setup - U_setup

### Hold

Earliest data arrival:
A_min = t_launch + t_cq,min + t_data,min

Hold threshold:
R_hold = t_capture + t_hold + U_hold

Hold slack:
S_hold = A_min - R_hold

Simplified clock-aware equation:
S_hold = t_cq,min + t_data,min - S
         - t_hold - U_hold

### Important insight

Positive capture skew generally helps setup but hurts hold.
Negative capture skew generally hurts setup but helps hold.

These are simplified equations for same-clock register-to-register
checks. Actual STA behavior depends on constraints, clock modeling,
uncertainty conventions and the analysis tool.

### Example results

Setup example:
Clock period = 10 ns
Skew = +0.3 ns
Setup slack = +0.8 ns

Hold example:
Skew = +0.3 ns
Hold slack = -0.2 ns

### New concepts covered

- Launch and capture clock arrival times
- Clock skew and its sign convention
- Required versus actual arrival time
- Maximum-delay versus minimum-delay analysis
- Setup and hold uncertainty
- Setup/hold optimization trade-offs


## Lesson 1 — Setup/Hold Violations and Timing Metrics

### Setup vs. hold
- **Setup:** Checks maximum data-path delay. Negative setup slack means data arrives too late.
- **Hold:** Checks minimum data-path delay. Negative hold slack means data arrives too early relative to the hold requirement.
- Negative slack indicates a violation; nonnegative slack indicates a pass for that check.

### Metrics used in this project
- **WNS:** Minimum slack within a defined group of checks. This project retains positive WNS if no violations exist.
- **TNS:** Sum of negative slack values within the defined group. This project reports TNS as a nonpositive number.
- Calculate setup and hold metrics separately and define the scope of the checks being analyzed.
- Different STA tools may display TNS using a different sign convention.

### Analyzer implementation
1. Store each timing result with its path, check type, and slack.
2. Filter results into setup and hold groups.
3. Count negative slacks to obtain violation counts.
4. Calculate WNS using the minimum slack.
5. Calculate TNS by summing negative slacks.

**Limitation:** The current Python example uses synthetic, already-parsed data. Report parsing and validation are separate future steps.


## Lesson 2 — STA Report Parsing

### Parser workflow
1. Read report text from a file.
2. Identify fields such as Startpoint, Endpoint, Path Group, and Path Type.
3. Extract timing values such as arrival time, required time, and slack.
4. Convert numeric text to floating-point values.
5. Store the results in a Python dictionary for later analysis.

### Python concepts
- `re.search()` searches for a matching regular-expression pattern.
- `match.group(1)` retrieves the first captured group.
- `Path.read_text()` reads a file as text.
- `None` represents a field that could not be extracted.
- `float()` converts numeric text into a number.

### Current limitations
- The first parser supports only our synthetic report format.
- Timing units are assumed to be ns.
- The example parses one path, not multiple paths.
- It does not yet validate required fields or distinguish setup from hold using all relevant report details.
- Real STA tools may use different formatting and conventions.


## Lesson 3 — Multi-Path Parsing

- A single-path parser returns one dictionary; a multi-path parser returns a list of dictionaries.
- Each dictionary represents one timing path.
- A report can be divided into path blocks using recognizable boundaries such as `Startpoint:`.
- Regular-expression lookahead can split before a boundary without removing the boundary itself.
- Required-field validation helps prevent incomplete records from entering metric calculations.
- Keep `max` and `min` path types distinct until the report's timing-check context is understood.
- WNS is the minimum slack in the selected set; TNS is the sum of negative slacks under this project's convention.
- The current parser supports a controlled, simplified PrimeTime-style sample, not every PrimeTime report format.

### Next improvements
1. Test the parser against actual authorized report formatting.
2. Add warnings for malformed or skipped paths.
3. Classify setup and hold checks using report context.
4. Add unit tests for multiple paths and missing fields.
5. Rank violating paths and export results to CSV.


## Lesson 4 — Automated Parser Testing

- Automated tests check whether code behaves as expected.
- Python's built-in `unittest` module supports test cases and assertions.
- `assertEqual()` compares expected and actual values.
- `assertAlmostEqual()` compares floating-point values with a tolerance.
- Tests should cover valid reports, multiple paths, incomplete records, and empty input.
- A passing test suite increases confidence but does not prove compatibility with every STA report format.
- The current tests validate the educational sample format, not all Synopsys PrimeTime reports.

### Next improvements
1. Add diagnostic warnings for incomplete paths.
2. Test additional numeric formats and report variations.
3. Validate extracted fields and timing units.
4. Add tests for metric calculations and critical-path ranking.


## Lesson 5 — Timing Metrics Engine

- The parser extracts data; the metrics engine analyzes it.
- A timing violation occurs when slack is negative.
- WNS in this project is the most negative slack, or 0 when there are no violations.
- TNS is the sum of negative slack values; this project retains the negative sign.
- Violation count is the number of paths with negative slack.
- Metrics are calculated separately for each reported path type.
- Setup and hold metrics must be scoped and reported separately in a production-quality analyzer.
- `unittest` verifies metric calculations independently of report parsing.


## Lesson 6 — Critical-Path Diagnostics

- Diagnostics turn timing metrics into actionable information.
- Sorting paths by ascending slack puts the worst slack first.
- A negative slack indicates a timing violation under the report's timing-check convention.
- A configurable limit lets us display only the worst N paths.
- Setup and hold paths should be analyzed separately in production reports.
- The current implementation ranks paths from our simplified sample format; it does not yet diagnose the physical cause of a violation.


## Lesson 7 — Cell Delay vs Net Delay

- Cell delay is the propagation delay through a library cell.
- Net delay is the delay through interconnect.
- Cell and net delay can contribute differently to the same path.
- This project uses a 60% contribution threshold as an educational classification heuristic.
- Missing, negative, or zero-total delay inputs are classified as unknown.
- Delay classification is not yet connected to the parser and requires reliable extracted values before it can diagnose real paths.


## Lesson 8 — Timing-Point Parsing

### What I learned
- A timing path contains individual timing points, including cells and nets.
- Incremental delay is the delay contributed by an individual point.
- Cumulative path delay is the accumulated delay up to a timing point.
- Summing incremental cell delays gives the total cell delay.
- Summing incremental net delays gives the total net delay.
- Cell and net delays together contribute to the total data-path delay.

### Example results
- Total cell delay: 0.45 ns
- Total net delay: 0.40 ns
- Total path delay: 0.85 ns

### Important limitation
The parser currently supports our controlled educational report format. It is not yet a general-purpose parser for actual Synopsys PrimeTime reports.


## Lesson 9 — Buffer-Chain Diagnostics

### What I learned
- Buffers can improve slew and drive large capacitive loads.
- Each buffer adds delay, area and power.
- A buffer chain consists of consecutive buffer and/or inverter stages.
- Total buffer/inverter count and longest consecutive chain are different metrics.
- A large chain can be worth investigating, but does not automatically indicate a timing violation.

### Implementation
- Added `is_buffer_or_inverter()` for educational cell-name classification.
- Added `analyze_buffer_chain()` to count matching cells and find the longest consecutive chain.
- Added tests for a mixed path, a path without buffers, and an empty path.

### Limitations
Cell-name matching is a heuristic. Production analysis should use actual library cell classifications and timing-point data. Buffer count alone does not establish the cause of a setup or hold violation.

## Lesson 10 — High-Fanout Net Diagnostics

### What I learned
- Fanout is the number of loads driven by a net.
- High fanout can increase capacitive loading and contribute to delay or slew problems.
- Physical-design tools may use buffering and cell resizing to improve electrical behavior.
- High fanout alone does not prove a timing violation.

### Implementation
- Added `find_high_fanout_nets()` to identify nets above a configurable fanout threshold.
- Results are sorted from highest to lowest fanout.
- Missing, invalid, and negative fanout values are ignored.
- A negative threshold raises a `ValueError`.

### Limitations
The current function analyzes supplied structured data. It does not extract fanout from PrimeTime reports, and the example threshold is not a universal design rule.


## Lesson 11 — Combined Timing and Physical-Design Diagnostics

### What I learned
- Slack indicates the timing margin relative to the required arrival time.
- Net-delay share indicates how much of the supplied cell-plus-net delay comes from interconnect.
- Buffer count can indicate a path worth examining more closely.
- Multiple indicators can help prioritize investigation.

### Implementation
- Added `score_path_for_investigation()`.
- Negative slack adds 3 points.
- Net-delay share of at least 60% adds 2 points.
- Buffer/inverter count of at least 3 adds 1 point.
- Invalid inputs return `None`.

### Limitations
The score is an educational prioritization heuristic, not an industry-standard metric or a root-cause diagnosis. The inputs must be derived from appropriate timing-path data, and actual physical-design conclusions require further analysis.

## Lesson 12 — Ranking Paths by Investigation Priority

### Objective
Rank timing paths according to how urgently they should be investigated, using slack, net-delay share, and buffer/inverter count.

### Concepts learned
- A negative slack indicates a timing violation under the report's timing convention.
- Net-delay share indicates the fraction of the supplied cell-plus-net delay attributable to interconnect.
- Buffer/inverter count can help identify paths worth investigating.
- Combining these indicators provides a way to prioritize paths for further analysis.
- When two paths have equal investigation scores, the path with more negative slack is ranked first.

### Implementation
Added `rank_paths_for_investigation()` to `src/sta_analyzer/diagnostics.py`.

The function:
1. Accepts a list of timing paths.
2. Calculates an investigation score for each path using `score_path_for_investigation()`.
3. Skips paths with missing or invalid scoring inputs.
4. Sorts paths by descending investigation score.
5. Uses ascending slack as the tie-breaker.
6. Returns up to the requested number of paths using the `limit` parameter.

### Scoring rules
- Negative slack: +3 points.
- Net-delay share greater than or equal to 60%: +2 points.
- Buffer/inverter count greater than or equal to 3: +1 point.

### Example
A path with slack of -0.40 ns, net-delay share of 0.65, and five buffers/inverters receives a score of 6.

A path with slack of -0.12 ns, net-delay share of 0.30, and one buffer receives a score of 3.

The first path is ranked higher because its combined score is greater


## Lesson 13 — End-to-End STA Analysis Pipeline

### Objective
Connect the parser, timing metrics and physical-design diagnostics into one runnable analysis workflow.

### Implementation
- Created `src/sta_analyzer/pipeline.py`.
- Added `analyze_report_text()` to coordinate report parsing, delay calculations, metrics and investigation ranking.
- Created `examples/run_full_analysis.py` to display a consolidated analysis.
- Added `tests/test_pipeline.py` to validate the integrated results.

### Concepts learned
- Incremental cell and net delays can be aggregated into a total path delay.
- Net-delay share can be calculated as net delay divided by total cell-plus-net delay.
- Timing metrics and investigation scores answer different questions.
- Integration tests verify that separate modules work together.

### Results for the educational sample
- Cell delay: 0.45 ns
- Net delay: 0.40 ns
- Total delay: 0.85 ns
- Slack: -0.15 ns
- Investigation score: 3

### Limitations
The pipeline currently assumes one detailed path because timing-point rows are not yet grouped by path. Buffer/inverter detection is based on cell-name patterns. The report format is educational and is not a general-purpose Synopsys PrimeTime parser.

### Lesson 14 — Parser Validation and Data Quality

**Objective:** Improve the reliability of the STA report parser by separating data extraction from data validation.

**Key concepts**
- Parsing extracts information from text.
- Validation checks whether the extracted information is usable.
- Required fields identify a timing path and provide its slack.
- Numeric fields must contain valid numeric values when present.
- Validation warnings help identify incomplete or malformed data.

**Implementation**
- Added `validate_timing_path()` in `src/sta_analyzer/parser.py`.
- Checks required fields: startpoint, endpoint, path type, and slack.
- Checks numeric types for arrival time, required time, and slack.
- Returns a list of warnings rather than stopping at the first problem.

**Testing**
- Valid timing path.
- Missing required field.
- Invalid numeric field.

**Limitations**
- Validation does not prove that a report follows the complete Synopsys PrimeTime format.
- It does not validate timing constraints or determine setup/hold correctness.
- The current parser still targets our educational report format.

### Lesson 15 — Timing-Path Tables and Cumulative Delay Validation

**Objective:** Understand incremental versus cumulative delay and validate the consistency of parsed timing-point data.

**Key concepts**
- Incremental delay is the contribution of the current timing point.
- Cumulative arrival time represents accumulated delay up to a timing point.
- For our educational format, cumulative delay should equal the running sum of incremental delays.
- Floating-point tolerance prevents tiny numerical differences from producing unnecessary warnings.

**Implementation**
- Added `validate_timing_points()` to `src/sta_analyzer/parser.py`.
- Checks cumulative delays against the running sum of incremental delays.
- Reports mismatches with the timing-point index and name.
- Rejects negative tolerance values.

**Testing**
- Valid timing-point sequence.
- Inconsistent cumulative delay.
- Negative tolerance.

**Limitations**
- The running-sum rule is specific to our educational report format.
- Real PrimeTime timing paths may use more complex timing references and structures.
- This validation checks arithmetic consistency, not whether a path meets setup or hold timing requirements.

### Lesson 16 — Integrating Validation into the Analysis Pipeline

**Objective:** Connect path validation and timing-point validation to the integrated STA analysis workflow.

**Implementation**
- Imported `validate_timing_path()` and `validate_timing_points()` into `pipeline.py`.
- Collected path validation warnings separately from timing-point warnings.
- Added `path_warnings` and `timing_point_warnings` to the pipeline result.
- Updated `run_full_analysis.py` to display data-quality warnings.
- Extended the pipeline integration test to check that valid sample data produces no warnings.

**Key concepts**
- Parsing, validation, and analysis are separate stages.
- Warnings should be visible to users of the pipeline.
- Returning warnings makes them available to scripts, tests, and future dashboards.

**Limitations**
- Warnings are collected but do not yet prevent questionable paths from contributing to metrics.
- Validation rules currently target the educational report format.
- A warning-free report is not proof that the timing constraints or physical design are correct.

