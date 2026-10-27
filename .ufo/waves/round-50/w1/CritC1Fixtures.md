# CritC1Fixtures — round-50 attack of landed fixtures

**Verdict: fixture data is broad, but class names are not sufficient premise checks.** Axes: calibration (measurement validity) and operability (whether the counter catches regressions).

## Method and evidence

The frozen fixture file contains 633 records. Its SHA-256 is `81836bfba624a0a4344c4787f7058219b45554fbcfc2da9d797846d96610e393`, matching `quality/counters/c1-r49-keysym.py:130-131`. I independently compiled each fixture RMLVO with `/usr/lib/xkbcommon/xkbcli-compile-keymap --include=/usr/share/xkeyboard-config-2`, then queried `/usr/lib/xkbcommon/xkbcli-how-to-type` using `--keymap`, `--disable-compose`, and `--keysym` in a clean HOME/XDG environment. The table counts below count data rows beneath `=== Direct access ===`; layout coverage uses the output's numeric layout column. This independently re-derives judge behavior; it is not a run of the counter itself.

| Observed property | Cases |
|---|---:|
| ≥2 direct-access rows | 180/633 |
| Rows in ≥2 distinct layouts | 66/633 |
| Any Lock mask | 65/633 |
| Any LevelThree mask | 79/633 |

All 15 `ABSENT` cases had no table rows. All 27 `DEAD` arguments were named `dead_*`, but the class does not ensure a matching row: some judge results were empty. The `MULTI` class has 58 cases with multiple RMLVO layout names, but only 22 had rows in ≥2 layouts (e.g. `r49-c1-0114` does; many later MULTI cases do not). `BIND` has 58 cases; 14 judge invocations returned rc=2 (e.g. `r49-c1-0021`, arg `DELETE`). Thus `BIND` cannot be treated as 58 successful bind-key results. These are class-premise/coverage caveats, not evidence of fixture digest or judge-output drift.

Counter source: `quality/counters/c1-r49-keysym.py:25-34` re-judges every fixture and checks recorded rc and stdout digest; it does not infer or enforce class premises. `:99-103` explains the installed 633-case fixture file and embedded fallback. The fixture file’s class counts are `BIND=58`, `MULTI=58`, `DEAD=27`, `ABSENT=15` (other classes make up the remainder).

## Mutant attack

I did not run a mutant against the counter. A concrete minimal candidate is a tool mutant that drops every Lock modifier from emitted rows: the fixture set contains 65 judge outputs with Lock masks, including `r49-c1-0017`; because clause f compares exact stdout bytes and rc, such a mutant should fail those fixtures. This is a predicted effect, not an observed kill. Similarly, a mutant that suppresses rows from layouts >1 is only detectable on cases whose expected output actually contains later-layout rows; there are 66 such cases. A class label alone is not proof of mutant sensitivity.

## Smallest safe correction

Keep fixture labels as selection categories, not universal behavioral assertions. Describe `MULTI` as multi-layout RMLVO input and `BIND` as selected host-bind arguments (which may be unsupported by the queried keymap). At freeze time, independently derive and record the observed counts above, and ensure any stated mutant kill is backed by an executed run against these frozen fixtures. No landed file was modified.
