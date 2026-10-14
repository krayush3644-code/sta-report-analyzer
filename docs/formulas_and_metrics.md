# STA Formulas and Metrics

## 1. Clock

f_clock = 1 / T_clock

Example:
T_clock = 10 ns
f_clock = 100 MHz

## 2. Simplified setup check

Required condition:

T_cq,max + T_data,max + T_setup <= T_clock

Setup slack:

T_clock - T_cq,max - T_data,max - T_setup

Negative setup slack indicates a timing violation.

## 3. Simplified hold check

Required condition:

T_cq,min + T_data,min >= T_hold

Hold margin:

T_cq,min + T_data,min - T_hold

A negative margin indicates a hold violation in this simplified model.

## 4. Worst slack

Minimum slack among the selected checks.

Always record:
- Timing check type
- Path group or analysis group
- Units
- Reporting convention

## 5. Total negative slack

Sum the negative slack values for the explicitly defined set
of timing checks.

Do not combine setup and hold metrics without clearly separating
their analysis and sign conventions.

## 6. Validation principles

- Convert all values to a consistent time unit.
- Handle zero-violation cases explicitly.
- Test positive, zero and negative slack.
- Compare computed values with known expected results.
- Document how duplicate endpoints and multiple path groups
  are handled.

Note: The equations above are simplified educational forms.
Production STA calculations require full timing constraints
and launch/capture clock information.