# MutC2V2 — v2-tightening mutation matrix (round 43 w2)

Counter under mutation: `quality/counters/c2-r43-gkeep-entry-v2.py` (PRED-C2-r43-v2).
Pristine scratch copy sha256 `9a83407062d165661d211a714ce06b381391c7c4574c91c71eb54689dde1d028`,
byte-identical to the frozen file (sha256sum on both paths, `evidence/hashes.txt`; the frozen file
hashes the same after every run). Data commit scored: `1959770657f1f8665097c1aed4be6c1cbb07139f`.

Detectors per mutant (all from copies in my scratch, frozen `ctl/` never edited — diffs in
`evidence/diffs/harness-*.diff`):

- **runner** — copy of `.ufo/waves/round-43/ctl/run-c2-controls-v2.py` with `LANE` hardcoded to the
  lane and `COUNTER` overridable by `MUTANT_COUNTER`; expected `CTL_C2: controls=74 correct=74/74`
  exit 0. An `ok=0` control (expected-rejected fixture flipping to admitted) kills the mutant.
- **forge** — copy of `ctl/v2-forgeries/forge.py` (15 fixtures; expected exactly
  P,A1,A2,D1,E2,H1 admitted = 6/15). An expected-rejected fixture flipping to ADMITTED kills.
- **more** — copy of `ctl/v2-forgeries/more.py` (X1 admitted; X2, X3 rejected; 3 P-safe probes).
- **real data** — the mutant run on the lane at `1959770…`; must stay
  `admitted=1/1 verdict=TARGET_MET` exit 0 (the landed entry satisfies every v2 condition, so a
  pure weakening must not reject it).

## Baselines (scratch copies, pristine counter) — all match the frozen receipts

| run | result | log |
|---|---|---|
| real data @1959770 | `admitted=1/1 verdict=TARGET_MET` rc=0 | `evidence/logs/base-realdata.txt` |
| runner | `CTL_C2: controls=74 correct=74/74` rc=0 (7.9 s) | `evidence/logs/base-runner.txt` |
| forge | 6/15 admitted (P,A1,A2,D1,E2,H1); B1,B2,C1,C2,E1,F1,F2,G1,G2 rejected | `evidence/logs/base-forge.txt` |
| more | X3 rc=1 i:0, X1 rc=0, X2 rc=1 i:0; probes P=1/1 + target rejected | `evidence/logs/base-more.txt` |

Matches `receipts/ctl-c2-v2.txt`, `ctl/v2-forgeries/forge-v2.log`, `more-v2.log`,
`receipts/c2-after-data.txt`: the harness copies are faithful.

## Matrix (16 mutants, 2 per v2 tightening)

| mutant | weakens | runner (74) | forge | more | real data | verdict |
|---|---|---|---|---|---|---|
| V2-1a drop `len(occurrences(blob,nq))==1` | d+ unique occurrence | 74/74 | **B1 flips** (7/15) | unchanged | 1/1 rc=0 | KILLED by forge B1 |
| V2-1b `occurrences` returns after first hit | d+ unique occurrence | 74/74 | **B1 flips** (7/15) | unchanged | 1/1 rc=0 | KILLED by forge B1 |
| V2-2a `quote_in_code` → `return True` | d+ comment stripping | 74/74 | **C1 flips** (7/15; C2 still rejected — its comment quote occurs twice, so unique-occurrence holds it) | unchanged | 1/1 rc=0 | KILLED by forge C1 |
| V2-2b `.py`/`.conf` lose `#` stripping | d+ comment stripping | 74/74 | 6/15 | unchanged | 1/1 rc=0 | SURVIVES — missing control F-2b |
| V2-3a drop the raw-URL prefix check | e+ raw-URL prefix | 74/74 | **G1+G2 flip** (8/15) | unchanged | 1/1 rc=0 | KILLED by forge G1, G2 |
| V2-3b prefix keeps host+repo, drops commit `efb5099…` | e+ raw-URL prefix | 74/74 | 6/15 | unchanged | 1/1 rc=0 | SURVIVES — missing control F-3b |
| V2-4a `all_body_lines_bound` → `return True` | g+ every-naming-line bound | 74/74 | **E1 flips** (7/15) | unchanged | 1/1 rc=0 | KILLED by forge E1 |
| V2-4b bound skips naming lines > 120 chars | g+ every-naming-line bound | 74/74 | 6/15 | unchanged | 1/1 rc=0 | SURVIVES — missing control F-4b |
| V2-5a `staged_ok` = basename in STAGED only | i+ exact package path | 74/74 | **F1 flips** (7/15) | unchanged | 1/1 rc=0 | KILLED by forge F1 |
| V2-5b `staged_ok` = exact dir prefix only | i+ exact package path | **72/74: A06, A07 flip** | 6/15 | unchanged | 1/1 rc=0 | KILLED by runner A06 + A07 |
| V2-6a drop the flip-word regex | i+ flip word | 74/74 (A09 still rejected: 1 distinct word) | **F2 flips** (7/15) | unchanged | 1/1 rc=0 | KILLED by forge F2 |
| V2-6b flip alternation without `\b` | i+ flip word | 74/74 | 6/15 | unchanged | 1/1 rc=0 | SURVIVES — missing control F-6b |
| V2-7a drop the entry-line BAD_LOC scan | i+ BAD_LOC in entry | 74/74 (A05/F4 still rejected: row-level scan kept) | 6/15 | **X2 flips** (admitted) | 1/1 rc=0 | KILLED by more X2 |
| V2-7b drop `zenn.dev`, `qiita.com` from BAD_LOC | i+ BAD_LOC in entry | 74/74 | 6/15 | unchanged | 1/1 rc=0 | SURVIVES — missing control F-7b |
| V2-8a drop the all-PINS-cited check | i+ all-PINS cited | 74/74 | 6/15 | **X3 flips** (admitted) | 1/1 rc=0 | KILLED by more X3 |
| V2-8b require only 6 of 10 PINS | i+ all-PINS cited | 74/74 | 6/15 | unchanged (X3 cites 3 < 6) | 1/1 rc=0 | SURVIVES — missing control F-8b |

Per-mutant logs: `evidence/logs/V2-*-runner.txt`, `V2-*-forge.txt`, `V2-*-more.txt`,
`V2-*-realdata.txt`; per-mutant diffs against pristine: `evidence/diffs/V2-*.diff`.

## Missing controls (surviving mutants) — inputs named AND demonstrated

`evidence/probe.py` (output `evidence/logs/probe-kills.txt`) builds each input as control P plus one
weakening delta, scores it against pristine (must reject via the clause under test) and against the
mutant (must admit). PINS are extended with the fixture's own receipt bytes by a last-wins variant
of the runner's own `patched_counter` (see the harness observation below).

| input | delta over control P | pristine | mutant | kills |
|---|---|---|---|---|
| F-2b-py-comment-quote | S299's GATE quote set to `the size request is ignored by the compositor in headless runs`, which exists only inside a `#` comment appended to `gkeep-ui-excerpt.py` (entry OBS line updated to the true computed line) | rc=1 **d:0** (comment stripped) | V2-2b rc=0 1/1 | V2-2b |
| F-3b-wrong-commit-url | S293 row location → `https://raw.githubusercontent.com/hyprwm/Hyprland/0123456789abcdef0123456789abcdef01234567/src/layout/target/Target.cpp` (right host+repo, wrong commit) | rc=1 **e:0** | V2-3b rc=0 1/1 | V2-3b |
| F-4b-long-naming-line | entry gains one 190-char line naming S291 with no quote (`**CAVEAT** the applicator registers static sizing here although …`) | rc=1 **g:0** | V2-4b rc=0 1/1 | V2-4b |
| F-6b-flip-word-embedded | REFUSE reason → `this staging note is whenever-compatible and otherwise unreviewed content here` (flip token only embedded in `whenever`; ≥4 distinct words, ≥20 chars) | rc=1 **i:0** | V2-6b rc=0 1/1 | V2-6b |
| F-7b-qiita-zenn-entry | entry gains `Also summarized on qiita.com and zenn.dev as secondary channels.` | rc=1 **i:0** | V2-7b rc=0 1/1 | V2-7b |
| F-8b-seven-of-ten-pins | S294/S295/S296 uncited (rows, source lines, OBS lines, GATE lines removed; 7 of 10 PINS cited) | rc=1 **i:0** | V2-8b rc=0 1/1 | V2-8b |

So: the registered battery (74 runner controls + forge + more) has **no teeth for six shapes**:
a quote living only in a `#` comment of a `.py`/`.conf` receipt, a wrong-commit raw URL, a long
quote-less naming line, an embedded flip word, the `zenn.dev`/`qiita.com` markers, and partial
(7-of-10) pin coverage. Each named input above is the control that would kill it; adding the six
fixtures to the battery closes all six shapes (each is rejected by pristine via exactly the clause
that carries the tightening — first failing clause shown).

## Harness observation (not one of the 16 mutants)

The frozen runner's `patched_counter` inserts the fixture's receipt hashes immediately after
`PINS = {`, i.e. BEFORE the original entries; in a Python dict literal a later duplicate key wins,
so for any basename the fixture edited, the ORIGINAL pinned sha survives and `pin_ok` fails. Every
patched-kind control that edits a pinned receipt (N04, N05, H09, H11, H13, W14, W15) is therefore
rejected by the pin clause regardless of the clause it names, and the runner's 74 controls alone
carry no receipt-content teeth at all — which is exactly why the kills for d+/e+/g+ came from the
forge/more fixtures (real receipts, unedited, run under the real counter) and not from the runner.
Demonstration: F-2b scored against V2-2b is rejected `d:0` with the frozen patcher (pin shadowing)
and admitted 1/1 with the last-wins patcher (`probe.py:patched_counter_last`), where the pristine
counter rejects it via the comment clause itself. This does not change any verdict above: every
kill attributed in the matrix comes from a fixture whose receipt bytes are unedited, so its
rejection under the mutant is a genuine clause kill.

## Real-data stability

All 16 mutants score the landed data commit `1959770657f1f8665097c1aed4be6c1cbb07139f` at
`admitted=1/1 verdict=TARGET_MET` exit 0 (`evidence/logs/V2-*-realdata.txt`): every mutant is a pure
weakening that leaves the admitted entry admitted — no false reject of the real entry, and the
landed entry exercises every tightening (consistent with `receipts/c2-after-data.txt`).

## Coverage statement

- 8 of 16 mutants killed: unique-occurrence (both), comment stripping on C++ (V2-2a), raw-URL
  prefix (V2-3a), every-naming-line bound (V2-4a), exact package path (both — V2-5a via forge F1,
  V2-5b via runner A06/A07), flip word (V2-6a), BAD_LOC-in-entry (V2-7a), all-PINS (V2-8a).
- 6 of 16 survive the whole registered battery: V2-2b, V2-3b, V2-4b, V2-6b, V2-7b, V2-8b — six
  missing controls, each demonstrated above. None of these is a hole in the landed data (real data
  stays admitted under all of them); they are coverage gaps of the battery around PRED-C2-r43-v2.
- The runner's 74 controls alone would have declared 14 of 16 mutants surviving (all but V2-5b's
  A06/A07 kill): the receipt-content and URL teeth live almost entirely in the forge/more fixtures.
