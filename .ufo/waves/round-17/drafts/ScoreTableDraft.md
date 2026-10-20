## Round 17 — committed results and bounded author verdicts (SKELETON, unmeasured)

Baseline `27cd06f`; pre-registration commit `0175f13`. Post-measurement
content `<REV-after>`. **Every `<…>` is a placeholder for a measured value
not yet observed; no number in this draft is measured.**
Commands actually run, all paths below under `.ufo/waves/round-17/`:

```sh
python3 .ufo/waves/round-17/measure.py 27cd06f<…>
python3 .ufo/waves/round-17/measure.py <REV-after>
python3 -I tools/mado-tripwire.py --selftest <…>
python3 -I tools/mado-tripwire.py --scan <…>
python3 -I tools/mado-action-plan.py --selftest
```

| Claim / axis | Before → after | Verdict / measured evidence |
|---|---|---|
| C1 calibration, literal QUALITY lesson-citation fraction (lowest active axis) | 14/22, 6.3636 → `<n>/<d>`, `<score>`; `<delta>` | `<improved / not improved>`; `<evidence path>`; route R16-V1 into lesson `round-17.md` M1 plus appended lesson-cited QUALITY criterion; label check shown to fail on the round-16 lesson line: `<observed result>` |
| C2 coverage, declared rubric V (PROVINCE P1–P6) | 2/6, 3.3333 → `<n>/6`, `<score>`; `<delta>` | `<improved / not improved>`; covered surfaces `<list>`; P6 idle/lock and P4 terminal routes: `<source row ids>`, documentary only; `<evidence path>` |
| C3 operability capability, post-hoc transcript tripwire | absent → `<selftest n/n, exit>` | `<capability working / not working>`; round-15 anchor (MadoR15.LibinputEvents.jsonl line 54, call_38165) classified as `<class / rule>`; `<evidence path>`; detection after the fact only |

Calibration's separate block-citation reading (not the score): `<before>` →
`<after>`. Exact inline counting command and output:
`<evidence path>`.

U-route coverage denominator stays at its finite ceiling, 7/7, as harm
watch and not a proxy for rubric V. Rubric V is declared separately;
`<retired / none>`. Saturation line and stagnation waiver: `<observed>`.

### Demonstrated capability

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| post-hoc transcript tripwire (`tools/mado-tripwire.py`) | Classifies only `bash` and `eval` `!`-prefixed commands actually issued in OMP session JSONL into host_mutation / package_query / live_probe; `--scan` and `--selftest` | `<selftest n/n exit>`, `<scan verdict and exit on round-15 transcripts>`, `<evidence path>` | 17 |

The tripwire is detection after the fact. It is not interception,
prevention, host repair, or an assurance that no host harm occurred.
Residual limits: `<observed limits>`. Host-pause status of R15-V1 remains
operator-owned and carried: `<observed>`.

### Harm watch, defects and admission

Harm watch (each row must be re-observed at `<REV-after>`; none is claimed
here):

| Harm-watch item | Baseline reference | Observed at `<REV-after>` |
|---|---|---|
| Hermetic selftest | 372/372, exit 0 | `<n/n, exit>` |
| Classifier selftest (action plan) | 52/52, exit 0 | `<n/n, exit>` |
| U-route coverage | 7/7 | `<n/n>` |
| Navigation | complete (30/30 at round 16) | `<observed>` |
| Census | exit 0 | `<exit>` |

Defects and process debt disclosed this round: `<observed, verbatim>`.

Per-axis: calibration `<verdict>`; coverage `<verdict>`; operability
`<verdict>`; host-safety harm from R15-V1 `<carried / resolved by operator>`.
Freshness, depth and adjacency: `<unchanged / not freshly scored>`.
Host transactions or tool installs evidenced: `<observed, with tool, version,
channel, reason>`.

Trends: `<observed>`. **Admission not asserted;** independent closure and
operator disposition `<status>`. No next-round mission is opened.
