# MutSelftestFixtures — round-40 w1 seat report (C1 mutation probe, base-tool selftest)

**Verdict: 16/16 mutants SURVIVED the base 71-assertion `--selftest` (0 killed, matching the tasking expectation), and 16/16 were independently shown LIVE on a hermetic live-path harness — no equivalent mutants. Every survivor is therefore a genuine coverage requirement the delivered selftest must add.**

## Detector and material

- Detector: the reference tool's own `--selftest` (hermetic; writes fixtures under a private temp dir, runs a copy of itself as a child). Pristine result: `MADO_OPTIONS_SELFTEST: 71/71 passed`, exit 0.
- Material: `.ufo/waves/round-40/c1/ctl-ref-tool.py.txt` (CONTROL, never delivered), sha256 `f96d9e0a0d2fe1bccb87940244db079de88c6794f03d66a36304d574694a08aa` — unchanged before and after the whole probe (re-verified post-run).
- Mutants: the 16 `(old, new)` pairs in `.ufo/waves/round-40/ctl/run-c1-controls.py` `MUTANTS` (M01–M16), applied with the controls runner's exact semantics `ref.replace(old, new, 1)`; every target matched exactly once (`occ=1` for all 16, so no first-occurrence ambiguity).
- Runtime: system `python3 3.14.8`, `python3 -I`, copies in `mktemp -d` scratch under /tmp. **No tools installed** (none needed); no pacman; no compositor contact (selftest and harness are hermetic; the harness uses a stub `hyprctl`, never the real one).

## Selftest kill matrix (the assigned probe)

Every mutant ran `--selftest` and printed the identical passing line:

```
BASE            rc=0  MADO_OPTIONS_SELFTEST: 71/71 passed
M01-all-agree   rc=0  MADO_OPTIONS_SELFTEST: 71/71 passed   SURVIVED
M02-raw-compare rc=0  MADO_OPTIONS_SELFTEST: 71/71 passed   SURVIVED
M03-bool-exact  rc=0  MADO_OPTIONS_SELFTEST: 71/71 passed   SURVIVED
M04-gradient-angle-ignored      rc=0  71/71 passed  SURVIVED
M05-gap-three-values-wrong      rc=0  71/71 passed  SURVIVED
M06-config-only-as-mismatch     rc=0  71/71 passed  SURVIVED
M07-extra-argv  rc=0  71/71 passed  SURVIVED
M08-set-ignored rc=0  71/71 passed  SURVIVED
M09-shadow-ignored rc=0  71/71 passed  SURVIVED
M10-hostile-probe-accepted      rc=0  71/71 passed  SURVIVED
M11-failure-swallowed rc=0  71/71 passed  SURVIVED
M12-writes-config-root rc=0  71/71 passed  SURVIVED
M13-no-normalisation-int rc=0  71/71 passed  SURVIVED
M14-live-field-dropped rc=0  71/71 passed  SURVIVED
M15-angle-inheritance-absent    rc=0  71/71 passed  SURVIVED
M16-probe-key-without-argv-check rc=0  71/71 passed  SURVIVED
```

No kill was by crash or by differing count: all 16 exited 0 with the full 71/71 line — the selftest simply never reaches the mutated code.

**Root cause (grep evidence):** the selftest body (`ctl-ref-tool.py.txt:761-1212`) exercises only the static resolver and the legacy `--getoption FILE` merge (`values_equal`/`load_live`/`merge_rows`, lines 466-540). It contains zero references to `--live`, `native_query`, `native_equal`, `merge_live`, `hl_int`, or `--probe` — all 16 mutants mutate exactly that unreached code (`native_equal` 588-621, `native_query` 623-643, `merge_live` 644-673, `hl_int` 579, probe validation 709, `if args.live:` 721).

## Liveness cross-check (survived ≠ equivalent)

To rule out equivalent mutants, each survivor was diffed against pristine on the `--live` path with a stub `hyprctl` (canned `getoption -j` replies, argv logging, per-key exit-1) over a fixture home, three scenarios:

- **S1** main merge: `--home H --live --hyprctl STUB --probe cursor:no_warps` — pristine exit 0, 10 rows covering `agreement` (kb_layout, repeat_rate, gaps_out, col.inactive_border), `agreement*` (col.active_border, twice-declared, inherited 45deg), `mismatch` (allow_tearing `yes` vs live int 0; disable_autoreload set=false), `config-only` (font_size, border_size → `no such option`).
- **S2** hostile probes: `--probe=-bad --probe=` — pristine exit 2 `mado-options.py: invalid probe key '-bad'`.
- **S3** compositor failure: stub exits 1 for `general:border_size` — pristine exit 5 `mado-options.py: general:border_size: .../stub-hyprctl exited 1`.

Result: **16/16 LIVE** — divergence from pristine in stdout / exit code / stderr / stub argv log / filesystem:

| Mutant | Ref target | Liveness |
|---|---|---|
| M01-all-agree | `native_equal` :588 | S1 stdout (mismatches flip to agreement) |
| M02-raw-compare | :588 | S1 stdout (`0x19` vs live 25 → mismatch) |
| M03-bool-exact | `hl_int` :579 | S1 stdout (declared `trueish`, live int 1 → mismatch) |
| M04-gradient-angle-ignored | :608 | S1 stdout (`rgba(11ff22ee) 30deg` → `0deg`) |
| M05-gap-three-values-wrong | :616 | S1 stdout (`4 8 12` → `4 8 12 4`) |
| M06-config-only-as-mismatch | :650 | S1 stdout (font_size mislabeled mismatch) |
| M07-extra-argv | :625 | S1+S3 stub argv log (extra `version` invocations) |
| M08-set-ignored | :655 | S1 stdout (set=false, equal value → agreement) |
| M09-shadow-ignored | :658 | S1 stdout (`agreement*` demoted to `agreement`) |
| M10-hostile-probe-accepted | :709 | S2 rc/stdout/stderr (exit 2 → exit 0) |
| M11-failure-swallowed | :630 | S3 rc/stdout/stderr (exit 5 → exit 0, config-only) |
| M12-writes-config-root | :721 | S1+S3 filesystem (`zz.tmp` created in config home) |
| M13-no-normalisation-int | :592 | S1 stdout (same fixture as M02) |
| M14-live-field-dropped | :654 | S1 stdout (`live` field missing from rows) |
| M15-angle-inheritance-absent | :656 | S1 stdout (inherited 45deg → 0deg → mismatch) |
| M16-probe-key-without-argv-check | :666 | S1 stdout (spurious `live-default` row for `no such option` probe) |

M03 required a synthetic declared spelling (`trueish`) to reach the `startswith`-vs-exact difference; realistic boolean spellings (`true`/`yes`/`on`) behave identically under both — noted so the delivered selftest knows what input class the assertion needs.

## Requirements the delivered selftest must add (one per survivor)

The delivered selftest must reach the `--live` path with a **stubbed hyprctl** (hermetic — never the real compositor) and assert:

1. **M01**: a known-divergent key (declared `yes`, live int 0, set) is labeled `mismatch` — `native_equal` is actually consulted, not short-circuited.
2. **M02/M13**: an int-form key whose declared spelling is numerically-equal but textually different (declared `0x19`, live 25) is labeled `agreement` (host-style conversion, not raw string compare).
3. **M03**: a declared boolean-prefix spelling outside the exact set (e.g. `trueish`, live int 1) is labeled `agreement` (the `startswith(("true","on","yes"))` branch).
4. **M04**: a gradient with an explicit angle in the resolved declarer (`rgba(11ff22ee) 30deg`, live `ee11ff22 30deg`) is labeled `agreement` (angle parsed from declared tokens).
5. **M05**: a 3-value gap (declared `4 8 12`, live `4 8 12 8`) is labeled `agreement` (third value repeated, not the first).
6. **M06**: a declared key answered `no such option` is labeled `config-only`, not `mismatch`.
7. **M07**: a recording stub asserts the child is invoked with exactly `[hyprctl, getoption, -j, key]` — no extra `version` or other argv.
8. **M08**: a `set:false` reply with an otherwise-equal value is labeled `mismatch`.
9. **M09**: a twice-declared key is labeled `agreement*`, not plain `agreement`.
10. **M10**: hostile probe keys are rejected with exit 2 naming the key. **Nuance found:** a bare `-bad` as separate argv never reaches main's validator — argparse itself rejects it (`error: argument --probe: expected one argument`), masking M10. The delivered selftest must pass hostile probes in `=` form (`--probe=-bad`, `--probe=`) or assert argparse's own rejection; only the `=` form exercises `ctl-ref-tool.py.txt:709`.
11. **M11**: a stub exiting nonzero for one key yields exit 5 with that key named on stderr (not a silent `config-only`).
12. **M12**: a `--live` run creates no files under the config home (filesystem assertion, e.g. no `zz.tmp`).
13. **M14**: every live-merged row carries a `live` field.
14. **M15**: the host-model inheritance case — earlier declarer carries `45deg`, resolved declarer doesn't, live carries `45deg` → `agreement*` (inherited angle used, not 0).
15. **M16**: a probe key answered `no such option` appends **no** `live-default` row.

## Safety / restoration evidence

- The reference tool was read-only throughout: sha256 `f96d9e0a0d2fe1bccb87940244db079de88c6794f03d66a36304d574694a08aa` before and after (mutants were separate copies in /tmp scratch; scratch dirs `mutselftest-*`, `mutlive-*` removed after the run).
- No tracked lane file edited; writes limited to this seat dir (`.ufo/waves/round-40/w1/MutSelftestFixtures/`) and this report. No git/jj mutations; no pacman; no real `hyprctl` invocation (stub only); no sockets; no subagents/background jobs.
- Raw per-mutant selftest stdout/stderr and liveness diffs were captured in scratch and are summarized above; drivers kept for provenance: `run_mutants.py` (kill matrix), `run_liveness.py` (liveness harness) in this seat dir.
