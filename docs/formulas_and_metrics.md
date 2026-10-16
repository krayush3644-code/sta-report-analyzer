# Formulas and Metrics

This document records the core timing equations and metrics used by the STA Report Analyzer. Values are expressed in nanoseconds (ns) unless stated otherwise.

## 1. Clock period and frequency

For a periodic clock:

\[
T = \frac{1}{f}
\]

If frequency is expressed in GHz, the corresponding period in ns is:

\[
T_{\text{ns}} = \frac{1}{f_{\text{GHz}}}
\]

Example: a 1 GHz clock has a period of 1 ns.

## 2. Setup timing

A setup check ensures that data arrives sufficiently early before the capture clock edge.

A simplified setup slack equation is:

\[
\text{Setup Slack} = \text{Required Arrival Time} - \text{Actual Data Arrival Time}
\]

- Positive slack: the setup requirement is met.
- Zero slack: the path is exactly at the timing boundary.
- Negative slack: the setup requirement is violated.

A simplified register-to-register setup equation, including launch/capture clock arrival times, is:

\[
\text{Setup Slack} =
T_{\text{period}} + T_{\text{capture clock}} - T_{\text{launch clock}}
- T_{\text{setup}} - T_{\text{uncertainty}} - T_{\text{data path}}
\]

This is a teaching equation. Sign conventions and additional terms can vary by report and timing model.

## 3. Hold timing

A hold check ensures that new data does not arrive too soon after the capture clock edge.

A simplified hold slack equation is:

\[
\text{Hold Slack} =
T_{\text{launch clock}} + T_{\text{data path}}
- T_{\text{capture clock}} - T_{\text{hold}} - T_{\text{uncertainty}}
\]

- Positive slack: the hold requirement is met.
- Negative slack: the hold requirement is violated.

Always confirm the sign convention and exact fields in the STA tool's report.

## 4. Worst Negative Slack (WNS)

For a set of paths, define each path slack as \(s_i\).

\[
\text{WNS} = \min(0, \min_i s_i)
\]

This convention reports zero when there are no negative slacks. Some tools or reports may present WNS differently, so preserve the convention used by this project when comparing results.

## 5. Total Negative Slack (TNS)

\[
\text{TNS} = \sum_{i: s_i < 0} s_i
\]

TNS is zero when no path has negative slack. It becomes more negative as violating slack accumulates.

Do not compare TNS values without checking whether the reports use the same path groups, check types, corners, modes, and path coverage.

## 6. Violation count and violation rate

\[
N_{\text{violations}} = \left|\{i : s_i < 0\}\right|
\]

\[
\text{Violation Rate} =
\frac{N_{\text{violations}}}{N_{\text{valid paths}}}\times 100\%
\]

The denominator should include only paths accepted by the analyzer's validation stage.

## 7. Data-path delay

For timing points that represent data-path cell and net delays:

\[
D_{\text{data}} = D_{\text{cell}} + D_{\text{net}}
\]

Clock-path points should not be included in this data-path total. The analyzer's summaries depend on correct point classification and on the input format providing usable delay values.

## 8. Delay dominance heuristic

The analyzer uses a heuristic to flag paths where one delay component dominates. A common ratio is:

\[
R_{\text{cell}} = \frac{D_{\text{cell}}}{D_{\text{cell}}+D_{\text{net}}}
\qquad
R_{\text{net}} = \frac{D_{\text{net}}}{D_{\text{cell}}+D_{\text{net}}}
\]

A threshold such as 60% can be used as a screening heuristic, not as proof of root cause. The project’s implementation and tests define the exact classification behavior.

## 9. Buffer and high-fanout indicators

Buffer/inverter chains and high-fanout nets are diagnostic indicators. They are not timing equations and should not be treated as automatic proof that a path needs a particular ECO.

## 10. Interpretation checklist

When reviewing metrics, record:
- Setup (`max`) or hold (`min`) check type.
- Path group, clock mode, process/voltage/temperature corner, and report scope when available.
- Number of valid and invalid paths.
- WNS, TNS, and violation count.
- Whether clock-path delays were excluded from data-path summaries.
- Whether two reports are comparable before interpreting changes.
