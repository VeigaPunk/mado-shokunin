# VER-M8 — round-8 post-hardening verification: 10/10 kills confirmed (named revisions)

Lane VER-M8, 2026-10-14 (training round 8). Write scope: **this file only** —
no other repo file was written by this lane; the gate and every other lane's
artifact were read-only to me. Scratch `/tmp/w8-ver-m8-scr/` (all logs/evidence
referenced below). No compositor/session state touched; no launch; no socket;
no mutating omarchy verb. This file's path follows the round-7 convention
(`reports/r7-aud-m7.md`); the dispatch text named no path. Marks: **[O]**
measured, **[I]** inference, **[U]** unknown.

## Verdict (named)

**VER-M8: PASS — the gate kills 10/10 of the recorded ten defects (D1–D9, R1)
under the current gate at the newest coherent revision I measured,
`tools/mado-verify.sh` sha256 `38ed880f…` (2,837 L, 129,233 B, selftest
207/207), in two independent channels:**

1. **Whole-file sweep** — the ten defects injected into the shipped file
   itself, killed by the mutant's own `--selftest` with **my own re-cut spec**
   (`97e12e65…`, not M8-1's): `killed=10 survived=0 inconclusive=0
   kill-rate=100%`, `CONTROL: GREEN`, `MUTATE_RESTORE: OK`, rc 0.
2. **Recorded-case channel** — the gate's own derived target `d2bcdb31…`
   (reproduced byte-exact by my own excision, equal to `PIN_MADO`) swept with
   the **recorded spec** `c7ee75b9…`: 10/10 KILLED; and the gate's own
   `--regression` at this revision prints
   `MADO_REGRESSION: PASS (case=mado-verify-hardened; target=d2bcdb31…)` with
   `match=10/10 … flips=0`, control green, restore ok.

Corroborating revisions (same methods): pre-hardening `90d50cdd…` (round-7,
HEAD `0c20a76`): 10/10 with my re-cut `25726ec5…`, and the gate's own
`--regression` PASS (recorded target `c4c1afb7…`). Intermediate coherent state
`f58632b9…` (2,194 L, selftest 148/148, pins re-cut): 10/10 whole-file
(spec `b6defdf5…`) and 10/10 derived+recorded.

**Post-measurement drift (stated, not smoothed):** the gate was still being
written after each measurement; the repo file read `7da4ec50…` at 19:31:29Z
and was moving at my close. Every number above is tied to the named sha; later
revisions are **[U] unverified by this lane**.

| revision (sha256 prefix) | size | state at measurement | my receipts |
|---|---|---|---|
| `90d50cdd…` (round-7, committed) | 1,755 L / 75,771 B | pre-hardening, selftest 89/89 | whole-file 10/10 (my re-cut `25726ec5…`, control 89/89); gate `--regression` PASS (target `c4c1afb7…`) |
| `f58632b9…` | 2,194 L / 100,266 B | hardening landed, selftest 148/148, PIN re-cut to `d2bcdb31…` | whole-file 10/10 (`b6defdf5…`); derived `d2bcdb31…` + recorded spec 10/10; `--regression` PASS |
| `38ed880f…` | 2,837 L / 129,233 B | + snapshot/diff feature, selftest 207/207 | whole-file 10/10 (`97e12e65…`); derived `d2bcdb31…` + recorded spec 10/10; `--regression` PASS; `--no-live`/`--live` CLEAN |

## Method (all runs mine, read-only)

1. Frozen copies (`landed.sh` = `f58632b9…`, `landed2.sh` = `38ed880f…`) and
   `git show HEAD:tools/mado-verify.sh` = `90d50cdd…` (`gate-r7.sh`).
2. Independent excision with the gate's own sed idiom. At `38ed880f…` the
   excisor has **three** blocks (R7-REGRESSION, R7-SELFTEST, R8-BLOCK); my
   3-block excision of that file = `d2bcdb31…` byte-exact, i.e. the gate's
   `PIN_MADO` is internally consistent. (A 2-block excision gives `8580388e…`
   — that is my earlier partial-state artifact, not a gate claim.)
3. Independent re-cut: `/tmp/w8-ver-m8-scr/ver-recut.py` widens each recorded
   anchor with adjacent whole lines until `count==1` on the target (the
   harness's own precondition); `@new` = the window with the recorded edit
   substituted, so the semantic mutation is preserved. All ten `ok` on every
   target used. My recut specs are byte-different from M8-1's
   (`85d946d7…`) — two independent widenings, same ten defects.
4. Sweeps: `tameshi-shokunin/tools/mutate-and-run.sh` sha256 `cf41efaa…`
   (moved from the recorded `b56c6e57…`; provenance, not gated), suite
   `bash "$MUTANT" --selftest`, unique workdirs under my scratch.

## Evidence (verbatim lines)

- Whole-file `38ed880f…` (`sweep2-whole.log`):
  `CONTROL: GREEN (… pristine-sha256=38ed880f…)`;
  `MUTATE: DONE (target=ver-m8-whole-38ed880f defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)`;
  `MUTATE_RESTORE: OK (before = after = 38ed880f…)`; all ten `DEFECT …: KILLED`
  (e.g. D1 `A: CLEAN verdict (missing: MADO_VERIFY: CLEAN)`; D2 six failing
  labels incl. `C: exit 1 (got '0' want '1')`; D5 `F: failing selftest exits
  2 (got '1' want '2')`).
- Derived `d2bcdb31…` + recorded spec (`sweep2-derived.log`): same shape,
  `killed=10 … kill-rate=100%`, control GREEN (2.7 s), restore OK.
- Gate's own at `38ed880f…` (`regression-landed3.log`):
  `REGRESSION_TARGET: … sha256=d2bcdb31… (recorded pin d2bcdb31…; match=yes)`;
  `REGRESSION_TABLE mado-verify-hardened: match=10/10 recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0`;
  `MADO_REGRESSION: PASS (case=mado-verify-hardened; target=d2bcdb31…)` rc 0.
- End-to-end at `38ed880f…`: `MADO_SELFTEST: 207/207 assertions passed` rc 0;
  `--no-live` → `MADO_VERIFY: CLEAN (20 pass, 3 notes)`, `counts: pass=20
  fail=0 unknown=0 skip=8 note=3`; `--live` → `MADO_VERIFY: CLEAN (43 pass,
  7 notes)`, `counts: pass=43 fail=0 unknown=0 skip=0 note=7`;
  `boundary.readonly` PASS both, combined sha `bb2639d9a980…`.

## Spot-checks (three)

1. **Pre-hardening, my own re-cut** (`gate-r7.sh` = committed `90d50cdd…`):
   `killed=10 survived=0 inconclusive=0 kill-rate=100%`, control GREEN 89/89,
   restore OK, 15.8 s. My spec `25726ec5…` ≠ M8-1's `85d946d7…` — independent
   anchor widening reproduces the same ten verdicts (corroborates
   `gate-mutation-sweep-r8.md` §1 and AUD-M8 C1/C2).
2. **Landed derived target + recorded spec** at `38ed880f…`: 10/10 KILLED;
   my excision byte-matches the gate's own pin, so the shipped regression case
   is internally consistent at the newest revision.
3. **Gate's own end-to-end** at `38ed880f…`: `--regression` PASS (10/10,
   flips 0), `--selftest` 207/207, both verdict rows CLEAN with the counts
   above — no regression in the verify path across the round-8 widenings.

## Incident (recorded, not smoothed)

My first `--regression` run on the frozen `f58632b9…` copy returned
`MADO_REGRESSION: FAIL (out of band: restore-not-ok)` while its own table read
`match=10/10`. Cause measured [O]: the harness's stdout log was truncated at
**exactly 4,096 bytes** (`/tmp/mado-verify-regression.sZPD11/case/sweep.log`,
kept) so the gate's `^MUTATE: ` / `^MUTATE_RESTORE: OK` greps found nothing,
although `results.tsv` was complete (11 lines) — the sweep itself had finished
all ten. Immediate re-run of the identical command: **PASS** (full log).
Cause **[U]**; not reproduced. Recorded because the gate's verdict demonstrably
depends on harness stdout lines, not exit codes alone (same family as the
exit-flatten boundary, `gate-mutation-proof.md` §3; that note's fix suggestion
— a stdout-reading kill criterion — would also harden this).

## Zero mutation [O]

`sha256sum ~/.config/hypr/hyprland.conf` = `4f52854a3c143dcf…` identical
before/after every substrate-reading run (and identical to the round-1 pin);
`boundary.readonly` PASS with combined sha `bb2639d9a980…` in every
`--no-live`/`--live` run; the live run is read-only by construction (no
launcher, no socket). My writes: this report, `/tmp/w8-ver-m8-scr/*`,
gate/harness scratch `/tmp/mado-verify-regression.*`. The 40 kept fixture
dirs (`/tmp/w5-mado-m52-selftest.*`) named by my own runs' evidence were
removed by exact path; foreign dirs left untouched.

## Unknowns

- **U1** — the gate kept moving after every measurement (`7da4ec50…` at
  19:31:29Z); later revisions are unverified by me. If the round wants a
  frozen pin for its final artifact, this verification must be re-run at it
  (my procedure: freeze → excise → re-cut → sweep → `--regression`).
- **U2** — the 4,096-byte log truncation (Incident) — cause unestablished.
- **U3** — single host/toolchain; harness revision `cf41efaa…` (recorded
  `b56c6e57…` is provenance, not gated).
- **U4** — the exit-flatten family stays a harness boundary; unchanged.
- **U5** — the recorded-case table is now pinned to `d2bcdb31…` (round-6 code
  + round-8 widening, R8-BLOCK excised); whether that replacement pin is the
  round's intended long-term pin is the owner's call, not this lane's.## Erratum (appended 19:35Z — append-only; supersedes the drift line above)

The repo settled on one more coherent revision before my close:
`tools/mado-verify.sh` sha256 `7da4ec50…` (**2,887 L**, mtime 19:29:03 −03:00),
`--selftest` **217/217 assertions passed** rc 0, `PIN_MADO` still `d2bcdb31…`.
Measured at it, all three channels (my runs, frozen copy `landed3.sh`):

- whole-file sweep, my re-cut spec `93724ee5…` — `CONTROL: GREEN (… pristine-sha256=7da4ec50…)`,
  `MUTATE: DONE (… defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)`,
  `MUTATE_RESTORE: OK (before = after = 7da4ec50…)`, rc 0;
- derived target `d2bcdb31…` (byte-exact via the gate's own 3-block excisor)
  + recorded spec `c7ee75b9…` — 10/10 KILLED, control GREEN, restore OK, rc 0;
- gate's own `--regression` — `MADO_REGRESSION: PASS (target=d2bcdb31…)`,
  `REGRESSION_TABLE … match=10/10 … flips=0`, rc 0.

So the headline verdict extends to `7da4ec50…`: **10/10 confirmed there as
well.** The derived target / `PIN_MADO` (`d2bcdb31…`) is stable across
`f58632b9…` → `38ed880f…` → `7da4ec50…` — round-8's additions ride inside the
excisor's marked block pairs, so the recorded-case replay stays reproducible
while the shipped file keeps growing (148 → 207 → 217 assertions). Later
revisions than `7da4ec50…` remain [U] unverified by this lane.