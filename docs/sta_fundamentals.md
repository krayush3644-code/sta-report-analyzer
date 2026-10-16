# STA Fundamentals

## 1. What is Static Timing Analysis?

Static Timing Analysis (STA) checks whether digital circuit paths meet timing requirements without applying a set of input test vectors. It uses timing constraints, cell timing models, and interconnect delay information to calculate arrival times and required times.

STA is a key part of digital implementation and timing closure. The analyzer in this project is an educational aid for interpreting selected report data; it is not a replacement for the sign-off tool.

## 2. What is a timing path?

A common register-to-register path contains:
1. A launch register.
2. Combinational logic and interconnect.
3. A capture register.

The launch clock edge starts the data transition. The data then propagates through cells and nets toward the capture register. STA checks whether the data satisfies the capture register's timing requirements.

Other path classes include input-to-register, register-to-output, and input-to-output paths.

## 3. Setup timing (`max`)

Setup analysis checks the latest data arrival against the setup deadline. In simplified reports, this is commonly associated with a `max` path.

If setup slack is negative, data is too late relative to the required time. Possible contributing factors include a long logic path, large interconnect delay, clock relationships, uncertainty, or constraints. The report alone may not identify a unique root cause.

## 4. Hold timing (`min`)

Hold analysis checks the earliest data arrival. In simplified reports, this is commonly associated with a `min` path.

If hold slack is negative, data may arrive too early relative to the hold requirement. Hold repair often adds delay to the data path, for example through buffers, but the appropriate action depends on the design and tool analysis.

A change that adds data-path delay may help hold timing while hurting setup timing. Therefore, setup and hold must be evaluated together.

## 5. Arrival time, required time, and slack

- **Arrival time:** the calculated time when data reaches a point or endpoint.
- **Required time:** the timing boundary that data must satisfy.
- **Slack:** the difference between the required boundary and the actual arrival, according to the check's sign convention.

For a simplified setup-style check:

`slack = required arrival time - actual data arrival time`

For hold checks, the sign convention is commonly expressed using the minimum required arrival boundary minus or against the earliest arrival in a tool-specific way. Use the tool's documented convention and report labels rather than assuming one equation applies to every format.

## 6. Clock latency, skew, and uncertainty

- **Clock latency:** the time taken for a clock to reach a point in the clock network.
- **Clock skew:** the difference between capture-clock and launch-clock arrival times.
- **Clock uncertainty:** a margin representing timing variation and modeling considerations specified by constraints or methodology.

Clock effects influence setup and hold differently. When learning the equations, define the sign convention for skew first and keep it consistent.

## 7. WNS and TNS

- **Worst Negative Slack (WNS):** describes the worst timing result under the project's chosen convention.
- **Total Negative Slack (TNS):** sums negative slack over the included violating paths.
- **Violation count:** the number of included paths with negative slack.

These metrics depend on report scope. Compare reports only when path groups, path types, modes, corners, and analysis settings are comparable.

## 8. Why path type matters

A report may include `max` and `min` paths:
- `max` generally represents maximum-delay analysis associated with setup checks.
- `min` generally represents minimum-delay analysis associated with hold checks.

The exact meaning depends on the report format and tool settings. The analyzer must preserve the parsed type and calculate metrics separately so setup and hold behavior are not mixed together.

## 9. What the project does

The current project includes:
- Parsing supported educational report formats.
- Validating key path fields.
- Computing metrics by path type.
- Ranking paths for investigation using heuristics.
- Summarizing cell/net delay where the input supports it.
- Exporting CSV summaries and an HTML dashboard.
- Visualizing slack distribution.

Heuristic rankings are investigation aids, not guaranteed root-cause diagnoses or ECO recommendations.

## 10. Study exercises

1. A setup path has required arrival time 0.80 ns and actual arrival time 0.86 ns. Calculate slack and identify pass/fail.
2. Explain why a negative hold slack is not the same problem as a negative setup slack.
3. If 12 paths have negative slack, explain what WNS and TNS each tell you.
4. Explain why clock-path delays should not be included in a data-path-only delay summary.
5. Explain why two reports must use comparable constraints and analysis settings before their WNS values are compared.
