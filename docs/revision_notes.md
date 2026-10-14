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
- [ ] Detailed setup and hold slack derivations
- [ ] Understand a real STA report
- [ ] Implement report parser
- [ ] Implement and test WNS/TNS calculations
- [ ] Implement diagnostics and trend analysis
- [ ] Generate HTML/CSV dashboard

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
