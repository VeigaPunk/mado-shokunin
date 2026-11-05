# R88MExecSelftest — harm-watch baseline and candidate self-tests (round 88, wave w1)

Seat: R88MExecSelftest (leaf executor). Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base revision measured: `24ba2a9ddac21c1211579231e6ee1d98963f9988`.
Scratch: `S=$HYAKU_SCRATCH/mado-r88/R88MExecSelftest` with `HYAKU_SCRATCH=/fast/scratch/hyaku` (created with `mkdir -p`, passed explicitly as `TMPDIR` and `--scratch-root`; deleted on exit — see §8).
No package installs, no upgrades, no network fetches. No mutating git command in the lane; the only git state created is the scratch clone at the base revision (`git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/mado-r88/R88MExecSelftest/lane`, `HEAD` → `24ba2a9ddac21c1211579231e6ee1d98963f9988`).
Nothing was scored: no counter was run against the candidate tools over any authored case file (freeze rule). `--selftest` mode only, plus read-only real-config smoke and mutant copies I built myself.

## 0. Pinned bytes

| object | sha256 |
|---|---|
| `.ufo/waves/round-88/build/mado-mako.c1.py` | `5063d31819b5d9a7a40b1c93dafe321a929cbcfd5b19d272023b3d920c36addd` |
| `.ufo/waves/round-88/build/mado-mako.c2.py` | `8d86f131b0964c2c0ee8e92df543611f0f850ef1960219b0d71a8f3042dbabfb` |
| `tools/mado-mako.py` (working tree) | `8d86f131b0964c2c0ee8e92df543611f0f850ef1960219b0d71a8f3042dbabfb` — byte-identical to the c2 candidate |
| base tool `git show 24ba2a9…:tools/mado-mako.py` → `$S/base.py` | `67a955a5fa06135c2748855b7e452bd3f0792c540002009ec90842ee5c986698` |
| `.ufo/waves/round-88/controls/mako-mutants-r88.json` | `40645a2854072d23795395bd13adb1058fba741fc4b1b0dac92fd02a9761d49b` (matches the declaration; 19 mutants) |
| `.ufo/waves/round-88/controls/containment-mutants-r88.json` | `49373eeeceef5ae6e76bfc7327f9f511ceef0e9fd4a8b3aadafeee8c6a084a85` (matches the declaration; 5 mutants) |

`diff -q` of `$S/base.py` against the working-tree `tools/mado-mako.py` → DIFFERENT (expected: working tree holds the c2 candidate).

## 1. Harm-watch baseline at 24ba2a9 (clean clone, all from the clone root)

| # | command (cwd `$S/lane`, `TMPDIR=$S`) | rc | last line |
|---|---|---|---|
| 1.1 | `bash tools/mado-verify.sh --selftest` | 0 | `MADO_SELFTEST: 460/460 assertions passed` |
| 1.2 | `bash tools/mado-verify.sh --no-live` | 0 | `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only — live layer skipped: --no-live)` (counts line above it: `pass=29 fail=0 unknown=0 skip=8 note=4`) |
| 1.3 | `python3 -I quality/check-index.py --repo . --rev 24ba2a9ddac21c1211579231e6ee1d98963f9988` | 0 | `MADO_INDEX: rev=24ba2a9ddac21c1211579231e6ee1d98963f9988 indexed=108/108 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` |
| 1.4 | `python3 -I quality/check-tool-ledger.py --repo . --rev 24ba2a9ddac21c1211579231e6ee1d98963f9988` | 0 | `LEDGER: population=161 ledger_rows=161 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=24ba2a9ddac21c1211579231e6ee1d98963f9988` |

Baseline is green on all four harm-watch legs, so a later regression on any of them is attributable to the round-88 commits.

## 2. Candidate self-tests (no case file involved)

| candidate | command | rc | result line |
|---|---|---|---|
| c1 | `python3 -I …/build/mado-mako.c1.py --selftest --scratch-root "$S"` | 0 | `MADO_MAKO_SELFTEST: checks=40 failed=0` |
| c2 | `python3 -I …/build/mado-mako.c2.py --selftest --scratch-root "$S"` | 0 | `MADO_MAKO_SELFTEST: checks=45 failed=0` |

Determinism: each candidate run twice into separate scratch roots (`$S/rt1`, `$S/rt2`); both logs byte-identical per candidate (`cmp -s`), rc=0 both times. The 5-check delta c1→c2 is the containment selftest block.
Cleanup: `find $S/rt1 $S/rt2 -mindepth 1 | wc -l` → 0 after the runs (the tool leaves nothing behind in its scratch root).

## 3. Mutant anchors and mutated copies

Method: `$S/mutcheck.py` (sha not pinned; script text in §9 note) counts `old` with `str.count` in each candidate source, writes a copy into `$S/mutants/<id>__<candidate>.py` with exactly the first occurrence replaced by `new` (asserting the bytes changed), then `py_compile.compile(..., doraise=True)` into `$S/pyc/`.

### 3.1 C1 mutant set — expectation: exactly one occurrence in c1 AND in c2

| mutant | count c1 | count c2 | anchor | py_compile c1 | py_compile c2 |
|---|---|---|---|---|---|
| M01-criteria-setdefault | 1 | 1 | OK | 0 | 0 |
| M02-global-ignored | 1 | 1 | OK | 0 | 0 |
| M03-relative-include-accepted | 1 | 1 | OK | 0 | 0 |
| M04-tilde-ignores-home | 1 | 1 | OK | 0 | 0 |
| M05-no-initial-mode | 1 | 1 | OK | 0 | 0 |
| M06-no-defaults | 1 | 1 | OK | 0 | 0 |
| M07-app-name-ignored | 1 | 1 | OK | 0 | 0 |
| M08-missing-input-matches | 1 | 1 | OK | 0 | 0 |
| M09-urgency-inverted | 1 | 1 | OK | 0 | 0 |
| M10-unterminated-quote-accepted | 1 | 1 | OK | 0 | 0 |
| M11-string-mismatch-ignored | 1 | 1 | OK | 0 | 0 |
| M12-string-missing-input-matches | 1 | 1 | OK | 0 | 0 |
| M13-bool-negation-ignored | 1 | 1 | OK | 0 | 0 |
| M14-bool-casefold-dropped | 1 | 1 | OK | 0 | 0 |
| M15-bool-criteria-inverted | 1 | 1 | OK | 0 | 0 |
| M16-bool-missing-input-matches | 1 | 1 | OK | 0 | 0 |
| M17-bool-invalid-accepted | 1 | 1 | OK | 0 | 0 |
| M18-option-bool-not-normalized | 1 | 1 | OK | 0 | 0 |
| M19-bare-bool-refused | 1 | 1 | OK | 0 | 0 |

19/19 anchors unique in both candidates; 38/38 mutated copies compile (rc 0). No anchor finding.

### 3.2 C2 mutant set — expectation: exactly one occurrence in c2

| mutant | count c1 | count c2 | anchor | py_compile c2 |
|---|---|---|---|---|
| K1-containment-skipped | 0 | 1 | OK | 0 |
| K2-lexical-resolution | 1 | 1 | OK | 0 |
| K3-prefix-without-separator | 0 | 1 | OK | 0 |
| K4-read-roots-ignored | 0 | 1 | OK | 0 |
| K5-home-not-a-root | 0 | 1 | OK | 0 |

5/5 anchors unique in c2; 5/5 copies compile. K1/K3/K4/K5 are absent from c1, i.e. the containment mechanism really is new c2 code (`grep -n 'read-root\|read_root' build/mado-mako.c1.py` → NONE). K2's anchor is not C2-specific — see F4.

### 3.3 Causal-separability check on the bytes (c1 → c2)

`diff -u c1 c2` → 9 hunks, 59 added / 8 removed lines, all in the containment surface: module docstring, `within_roots`, the include read (`real`/root test), `resolve(..., read_roots)`, selftest additions, `--read-root` argument plumbing. No criteria/boolean lines are touched, matching the declaration's claim that C2 needs no C1 byte.

## 4. Supplementary (non-scoring): does the tool's own `--selftest` kill the mutants?

Each mutated copy was run with `--selftest --scratch-root $S/mutselftest/<id>`; 43 copies total (19 C1 mutants × {c1,c2} + 5 C2 mutants × c2).

- 39 copies: rc=1 with a clean summary line (`checks=40/45 failed=N`, N ≥ 1).
- 2 copies (`M06-no-defaults` on c1 and c2): rc=1 via an uncaught `KeyError` — see F2.
- 2 copies (`M16-bool-missing-input-matches` on c1 and c2): **rc=0, `failed=0` — survived the tool's own selftest** — see F1.

This is not the round's kill measurement (that is the C1 counter over the authored cases); it only shows whether the shipped selftest is mutation-sensitive.

## 5. Real-config smoke (read-only, host reads limited to the mako config chain)

Inputs read: `~/.config/mako/config` (5 lines) and its include `~/.local/share/omarchy/default/mako/core.ini` (38 lines). Relevant fixture content: L11 `[app-name=Spotify]` / L12 `invisible=1`; L14 `[mode=do-not-disturb]` / L15 `invisible=true`; L17 `[mode=do-not-disturb app-name=notify-send]` / L18 `invisible=false`; L20 `[urgency=critical]`; L24-L38 four `[summary~=…]` sections.

Command shape: `<tool> --config ~/.config/mako/config --home ~ --app-name <APP> --mode do-not-disturb` (stderr carries one line `MADO_MAKO: resolved=37 refusals=<n>`; stdout is a JSON object with `applied`, `effective`, `refusals`).

| tool | `--app-name` | rc | `effective.invisible` | `applied` (file order) | refusals |
|---|---|---|---|---|---|
| c2 candidate | `notify-send` | 0 | **`0`** | `global-section`, `include:…/core.ini`, `section:[mode=do-not-disturb]`, `section:[mode=do-not-disturb app-name=notify-send]` | 6 |
| c2 candidate | `Spotify` | 0 | **`1`** | `global-section`, `include:…/core.ini`, `section:[app-name=Spotify]`, `section:[mode=do-not-disturb]` | 6 |
| base (r87) | `notify-send` | 0 | `0` | same four entries as c2 | 8 |
| base (r87) | `Spotify` | 0 | `1` | same four entries as c2 | 8 |
| c2 candidate | `Slack` | 0 | **`1`** | `global-section`, `include:…/core.ini`, `section:[mode=do-not-disturb]` | 6 |
| base (r87) | `Slack` | 0 | **`0`** | same three entries as c2 | 8 |

Additional apps checked for `invisible` only (stderr suppressed): `Signal`, `telegram-Desktop`, `org.telegram.desktop`, `mako` → c2 `1`, base `0` in all four.

Refusal delta: base refuses exactly the two style-boolean lines the candidate now accepts —
`…/core.ini:15: invisible='true': expects 0 or 1` and `…/core.ini:18: invisible='false': expects 0 or 1`.
The candidate emits no such refusal; its six refusals are the `--urgency` guard at L20 plus the five `summary~` refusals at L24/27/30/33/36 (both tools refuse those identically).

So the host DND state resolves correctly on the candidate (`true`→`1` at L15, then `false`→`0` at L18 for notify-send; `1` retained for Spotify because L11 precedes L14 in file order) and does not on the base.

## Findings

**F1 (selftest gap).** `M16-bool-missing-input-matches` survives the candidates' own selftest: mutated copies `$S/mutants/M16-bool-missing-input-matches__c1.py` and `__c2.py` exit **0** with `MADO_MAKO_SELFTEST: checks=40 failed=0` / `checks=45 failed=0`.
Reproduce: `python3 -I $S/mutants/M16-bool-missing-input-matches__c2.py --selftest --scratch-root $S/rt1; echo rc=$?` → `rc=0`.
Anchor: `build/mado-mako.c1.py:357` / `build/mado-mako.c2.py:372` (`undecided.append("--" + key + " (boolean)")`). The selftest block (`def selftest` at c1:452 / c2:474) exercises bare, negated, case-folded, invalid and inverted booleans, and its only missing-input check is `[app-name=foo]` (`run("no-input", ...)`, c2 selftest near line 549) — no boolean (`--actionable`/`--expiring`) and no new string field (`--app-icon`/`--summary`/`--body`/`--category`/`--desktop-entry`) has a missing-input selftest. Consequence: the shipped `--selftest` is not a mutant gate for this path, so M16's kill rests entirely on the C1 case set — the L1 should confirm at least one authored case supplies `[actionable=…]`/`[expiring=…]` with no `--actionable`/`--expiring` and expects a refusal.

**F2 (selftest robustness).** `M06-no-defaults` is killed, but by an uncaught exception instead of a reported failure: `KeyError: 'anchor'` at `selftest` `build/mado-mako.c1.py:476` / `build/mado-mako.c2.py:504` (the check `r["effective"]["anchor"] == "top-right"` indexes a dict the mutant emptied). Reproduce: `python3 -I $S/mutants/M06-no-defaults__c2.py --selftest --scratch-root $S/rt1` → rc=1, no `MADO_MAKO_SELFTEST` summary line on stderr. Harmless for the counter (rc≠0 still), but a crash means no per-check diagnostics; if a case run ever hits a missing key the failure will surface as a traceback rather than a refusal record.

**F3 (case-design warning, discriminates the base-tool control).** For `--app-name notify-send --mode do-not-disturb` the c2 candidate and the base both report `effective.invisible = "0"`, by different paths: the candidate resolves `invisible=true`→`1` (L15) then `invisible=false`→`0` (L18); the base refuses both lines and lands on the DEFAULTS value `0`. A C1 case whose expected `invisible` is `0` for `notify-send` under DND therefore **cannot** separate the candidate from the do-nothing `base-tool` control — the control scores it for free. Discriminating inputs exist and are stable across six app names: any app other than `notify-send`/`Spotify` (e.g. `Slack`, `Signal`, `mako`) gives candidate `1` vs base `0`. The refuse-count difference (6 vs 8, i.e. L15/L18) is a second discriminator. The case author (not this seat) should include at least one of these; I am not editing cases.

**F4 (mutant-set scoping, informational).** K2's anchor `real = os.path.realpath(target)` occurs once in c1 as well (`build/mado-mako.c1.py:414`, the include-open path, which in c1 has no containment test). C2's requirement ("exactly once in c2") is satisfied and the declaration's C2 mutant set is unaffected; the note matters only for tooling that applies C2 mutants to "the candidate" generically — target `mado-mako.c2.py` explicitly, or K2 will also mutate the C1 candidate.

## 6. Verified good (no finding)

- Base harm-watch: 4/4 green (§1) — carries the r87 axis values (selftest 460/460, file plane 29/29, index 108/108 @10.0000, ledger 161/161 TARGET_MET).
- Candidate selftests: c1 40/40, c2 45/45, deterministic, no scratch leftovers (§2).
- Mutant anchors: C1 19/19 exactly once in both candidates; C2 5/5 exactly once in c2 (§3). No anchor is missing or duplicated anywhere.
- All 43 mutated copies compile (`python3 -m py_compile` via `py_compile.compile(doraise=True)`, rc=0 each).
- c1 → c2 byte delta is confined to the containment surface (9 hunks) — the two claims stay causally separable in the bytes, not only in the prose.
- Read-only smoke: the candidate resolves the host's real DND state; the base does not (§5).

## 7. Dead steps / limits

- `…/controls/mako-cases-r88.json` was **absent** for the whole seat run (`test -s` false at start and at end); `containment-cases-r88.json` appeared during the run (`test -s` true at end). Neither was needed by this item and neither was read or scored.
- The four extra apps in §5 (`Signal`, `telegram-Desktop`, `org.telegram.desktop`, `mako`) were run with stderr discarded, so only `invisible` was recorded for them, not refusal counts.
- No LSP: this seat needed no symbol navigation, so none was attempted; recorded as not-applicable rather than as an empty result.
- No tool installs, no pacman transaction, no service restart, no sysctl change.

## 8. Scratch cleanup

Everything written by this seat lived under `$S=/fast/scratch/hyaku/mado-r88/R88MExecSelftest` (clone, `base.py`, mutant copies, `pyc`, logs, harness). It is removed with `rm -rf -- "$S"` as the last step; the removal is confirmed by `test -e "$S"` returning false, and that confirmation is echoed into this seat's yield. Nothing outside `$S` and this report file was written.

## 9. Harness note

`$S/mutcheck.py` (deleted with the scratch) implemented §3 exactly: read the two mutant JSONs, `str.count` each `old` in both candidate sources, `str.replace(old, new, 1)` into a per-mutant copy (asserting the bytes changed), then `py_compile.compile(..., doraise=True)` per copy, printing one row per mutant and exiting non-zero if any anchor count or compile failed. Its run exited 0; the per-row table is §3.1/§3.2 verbatim.
