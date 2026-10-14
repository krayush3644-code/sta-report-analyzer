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

## Lesson 4 — Setup/Hold Violations and Timing Metrics

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

## Lesson 5 — STA Report Parsing

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

## Lesson 6 — Multi-Path Parsing

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

## Lesson 7 — Automated Parser Testing

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


## Lesson 8 — Timing Metrics Engine

- The parser extracts data; the metrics engine analyzes it.
- A timing violation occurs when slack is negative.
- WNS in this project is the most negative slack, or 0 when there are no violations.
- TNS is the sum of negative slack values; this project retains the negative sign.
- Violation count is the number of paths with negative slack.
- Metrics are calculated separately for each reported path type.
- Setup and hold metrics must be scoped and reported separately in a production-quality analyzer.
- `unittest` verifies metric calculations independently of report parsing.
