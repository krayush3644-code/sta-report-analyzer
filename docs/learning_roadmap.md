# STA Report Analyzer — Learning Roadmap

This roadmap pairs STA theory with implementation work in the Python project. Mark an item complete only after studying it and validating the relevant behavior.

## Stage 1 — Timing fundamentals

- [x] Understand clock period and frequency.
- [x] Introduce setup and hold checks.
- [x] Understand slack, WNS, and TNS.
- [x] Derive setup and hold equations with clock skew.
- [x] Understand uncertainty and clock latency.
- [ ] Practice calculating setup slack by hand.
- [ ] Practice calculating hold slack by hand.
- [ ] Explain why setup and hold fixes can have opposite effects.

## Stage 2 — Read timing reports

- [x] Identify startpoint and endpoint.
- [x] Identify path group, path type, and slack in the educational format.
- [x] Parse multiple paths from one report.
- [x] Parse timing-point rows in supported educational formats.
- [x] Track data-path and clock-path sections where recognized.
- [ ] Document the exact report formats supported by the parser.
- [ ] Add examples for both `max` and `min` paths.
- [ ] Validate behavior against sanitized reports that are authorized for use.

## Stage 3 — Python analyzer architecture

- [x] Parse a report into path records.
- [x] Validate required path fields.
- [x] Calculate metrics grouped by path type.
- [x] Rank paths for investigation.
- [x] Summarize cell and net delay where supported.
- [x] Export CSV summaries.
- [x] Generate an HTML dashboard.
- [x] Add a slack-distribution chart.
- [ ] Add tests for mixed `max` and `min` reports.
- [ ] Add explicit handling for missing slack-distribution data.
- [ ] Improve error messages for unsupported or malformed report formats.

## Stage 4 — Diagnostics

- [x] Rank worst paths and investigation candidates.
- [x] Flag delay-dominance patterns heuristically.
- [x] Identify buffer/inverter-chain patterns heuristically.
- [x] Identify high-fanout indicators where input data supports them.
- [ ] Clearly separate measured facts from heuristic recommendations.
- [ ] Add more tests for clock-path exclusion and incomplete timing-point data.

## Stage 5 — Compare timing runs

- [ ] Define a report-comparison data model.
- [ ] Compare path counts and invalid-path counts.
- [ ] Compare WNS, TNS, and violation counts by path type.
- [ ] Identify paths that improved, regressed, appeared, or disappeared.
- [ ] Export a comparison CSV and HTML summary.
- [ ] Test comparison using two controlled synthetic reports.

## Stage 6 — Quality and usability

- [ ] Run the complete test suite after each feature.
- [ ] Review `git diff --check` before committing.
- [ ] Keep generated reports out of source commits unless intentionally included.
- [ ] Document setup, commands, sample inputs, outputs, and known limitations in README.
- [ ] Add clear warnings that this educational analyzer is not a replacement for sign-off STA.

## Suggested development loop

1. Learn one timing concept.
2. Work through a small numerical example.
3. Implement or inspect the corresponding Python behavior.
4. Add a focused test.
5. Run `python -m pytest -q`.
6. Review the diff and commit one coherent change.

## Current project checkpoint

The project has a parser, metrics, diagnostic heuristics, CLI, CSV exports, an HTML dashboard, and a slack distribution chart. A 1,000-path synthetic report has been processed successfully. Treat the synthetic report as a functional test, not as evidence of compatibility with every commercial STA report.

The next recommended feature is a robust comparison of two reports, while adding tests for mixed `max` and `min` path types.
