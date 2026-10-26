# Seat MutC2Counter — round 46 w1 — mutation probe of PRED-C2-r46 against the 15 registered C2 controls

Date: 2026-10-26. Seat dir: `.ufo/waves/round-46/w1/MutC2Counter/`. Scratch: `/fast/scratch/hyaku/mado-r46/MutC2Counter/` (deleted at end; evidence copied to `evidence/` first).

## What was attacked

The frozen counter `quality/counters/c2-r46-input-device-entry.py` (sha256 `18ea82b1c4372b0c8e7af585d0edf09ffbf6d4a0d276ce19fc97519b720b72b7`) and the claim that its 15-control suite (`.ufo/waves/round-46/ctl/run-c2-controls.py`, sha256 `4f41427f316dfbff2407006f94183f5da1842d5bfa386f65fdd0e81c8f7f6d36`) detects any one-clause weakening. One plausible defect per mutant, applied to a scratch copy; the lane originals were never edited.

## Method

1. Baseline first: pristine counter in a scratch clone at the freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, full suite via a copy of the runner → `CTL_C2 VERDICT: PASS (wrong=0 of 15; positive admitted=1)`, P admitted with a:1…j:1 (`evidence/BASELINE.txt`). Harness valid.
2. Runner copy: `evidence/runner-copy.py` — control definitions, verdict logic and output format are the original's; ONE documented deviation: each control clone is created→evaluated→deleted sequentially instead of 15 clones alive at once (freeze tree is 236,536,374 B; 15 concurrent checkouts ≈ 3.5 GB would exceed the seat's 2 GB scratch budget). The counter under test is taken from `--repo`'s working tree exactly as in the original, so `--repo <mutant-repo>` tests the mutant.
3. 10 mutants (`evidence/diffs/*.diff`), one weakened clause each: census regex (h), surface width (j), quote uniqueness (d), T1–T5.
4. Per mutant: scratch repo = `git clone -q --shared --no-checkout` of the lane, checkout the freeze, overwrite `quality/counters/c2-r46-input-device-entry.py` with the mutant, commit inside the clone after asserting `git rev-parse --show-toplevel` equals the clone dir; then the full 15-control suite (`evidence/driver.sh`, outputs `evidence/M*.txt`).
5. Verdict rule: suite rc=0 (all 15 correct) → mutant SURVIVED (coverage gap); any control's expected verdict flipped → KILLED, named by its `WRONG` line.

## Results

| mutant | weakened clause (lane counter locator) | suite | verdict | killing control(s) |
|---|---|---|---|---|
| M1-census-regex-uniq | h: census-pattern uniqueness `len(d)!=1…` → `not (d and f and m and p and v)` (counter.py:347) | PASS 15/15 | **SURVIVED** | — none of the 15 |
| M1b-census-devicekeys | h: device_keys count `'…"device", "'` → any category (counter.py:342) | FAIL wrong=1 | killed | **P** (positive itself rejected; h:0 on every run — count computes 75 ≠ 47) |
| M2-surface-width | j: `JWIDTH = 30` → `1000000` (counter.py:100) | PASS 15/15 | **SURVIVED** | — none of the 15 |
| M3-quote-uniq | d: drops `nq not in seen_quote` (counter.py:541) and the cross-receipt quote loop (counter.py:555-561) | PASS 15/15 | **SURVIVED** | — none of the 15 |
| M4-T1-census-prose | T1: prose-census comparison disabled (counter.py:626) | FAIL wrong=2 | killed | **PROSE-CENSUS**, **PROSE-CENSUS-SPACED** (both admitted, all clauses 1) |
| M5-T2-supersede | T2: supersede/replace/obsolete word ban dropped (counter.py:504) | FAIL wrong=1 | killed | **ROW-SUPERSEDES** (admitted) |
| M6-T3-fences | T3: `fences_ok` no longer ANDed into b (counter.py:685) | FAIL wrong=1 | killed | **FENCE-TABLE** (admitted) |
| M7-T4-verdict-tokens | T4: verdict-token-in-receipt check disabled (counter.py:681) | FAIL wrong=1 | killed | **RECEIPT-CONTRADICT** (admitted) |
| M8-T4-anchor-range | T4: anchor range past receipt EOF no longer rejected (counter.py:610) | FAIL wrong=1 | killed | **ANCHOR-PAST-EOF** (admitted) |
| M9-T5-readme-ids | T5: README Sources-cell ids no longer checked (counter.py:660) | FAIL wrong=1 | killed | **README-IDS** (admitted) |

Every killed mutant flipped exactly the control(s) listed; all other controls stayed correct. Every suite ran 15 real counter runs (15 `CTL_C2 … a:[01]` clause lines each) — no crash artifacts.

## Survivor analysis (the coverage findings)

**M2-surface-width — actionable gap.** The locator span bound (`b - a <= 30`, counter.py:100 used at the clause-j match) is pinned ONLY by clause j. Registered WIDE-RANGE rewrites every InputManager locator to `:1-2315`, which clause g rejects independently (every line naming the id must contain the exact quote-line locator `Hyprland-InputManager.cpp:<at>`; baseline shows WIDE-RANGE failing g AND j) — so the suite passes with JWIDTH unbounded. Demonstrated kill (`evidence/probe-widetail.txt`): a WIDE-TAIL control that widens each InputManager locator preserving its start (`:(\d+)(-…)?` → `:\1-2315`, 8 locators rewritten) keeps g green; the pristine counter rejects it (j:0, `admitted=0/1`) while the M2 mutant ADMITS it (j:1, `admitted=1/1`, rev 2754b1f3c0987a60068a1c8b0ae6a47877929d45). A control of this shape (span-widening that preserves the quote-line start) would close the gap.

**M1-census-regex-uniq — structurally unprobed at this freeze.** host_census reads only BOUND gates' receipts (counter.py:332-336), and a gate on a PINS-named file must carry the pinned sha256 (counter.py:536-538) — the six census receipts are always the pinned bytes. So a census-extraction mutant either changes the computed value on the pinned bytes (caught by P — demonstrated by M1b) or computes the same values (behaviorally identical on every control — M1 survived). The "each pattern occurring exactly once" half of clause h is unprobed; it is defense-in-depth behind the pin-hash root. Probing it would need a receipt whose bytes differ (rejected at clause d before the census runs) — not constructible from this freeze.

**M3-quote-uniq — unprobed by the registered suite; killing control EXISTS via the pin_ok hole (corrected post-delivery).** The registered 15 controls do not probe the distinct-quote-per-id and not-in-other-receipts sub-checks of clause d (counter.py:541 and 555-561): all 10 gate quotes occur in exactly one pin each (verified with the counter's own `occurrences()` semantics). The original conclusion here — "structurally unprobed, no killing control constructible from this freeze" — was WRONG: it assumed every FETCH receipt is pin-rooted, but `pin_ok = PINS.get(os.path.basename(path)) in (None, digest)` (counter.py:532-534) passes for any receipt name NOT in PINS, so a scored rev can self-author a receipt under FETCH/ and bind a new id to it. ConnCrossClaim-3 verified this route (forged-S316 admission, rev 1de0bb53); this seat then demonstrated the M3-killing control directly:

- SHARED-QUOTE control (evidence/probe-sharedquote-pristine.txt / -m3.txt): P plus a new id S326 with a registry row, a `source: S326` header line, a Gate line and an entry line, gated on a self-authored non-pinned receipt `fetch/r46-shared-quote.txt` whose line 1 repeats S319's gate quote `m_currentRules.layout = "us";` (sha256 self-consistent, ≥256 B, 100644; README row widened to S316-S326).
- Pristine counter: REJECTED — `clause=d id=S326 gates=1 bound=0` is the only unbound gate (S316-S325 all bound=1); the sole failing binding condition is `nq not in seen_quote`, i.e. the quote-uniqueness sub-check is the only barrier (rev b79019121dcbe8ed7be04adb2d97aaf4e4f97875).
- M3 mutant: ADMITTED — a:1…j:1, `admitted=1/1 verdict=TARGET_MET` (same rev).

So the correct statement: M3 survives the registered suite, but the quote-uniqueness sub-check is load-bearing exactly once the pin_ok hole is used; a control of the SHARED-QUOTE shape kills it. Note the demonstration also independently confirms the pin_ok route itself: the forged non-PINS receipt passed every pin-rooted binding check in both runs.

## Process note (honest record)

The first M1b attempt was an invalid mutant: the replacement dropped the line's closing paren, producing a SyntaxError; its suite "killed by P" was a crash artifact (a crashing counter rejects everything, so the 14 negatives looked ok). Caught because P's run printed no `clauses=` line; probe preserved (`evidence/probe-m1b.txt`). M1b was regenerated (compiles), its suite re-run, and the verdict above is from the valid mutant. All other mutants were py_compile-checked.

## Integrity / restoration evidence

- Lane `quality/counters/c2-r46-input-device-entry.py` and `.ufo/waves/round-46/ctl/run-c2-controls.py` sha256-identical before, mid-run and after (`evidence/lane-hashes.txt`): `18ea82b1…`, `4f41427f…`. No mutant bytes ever placed in the lane; no tracked file edited; no git/jj mutation in the lane or fleet (clones and commits only inside `/fast/scratch/hyaku/mado-r46/MutC2Counter/`, toplevel asserted before each commit).
- Scratch dir deleted at the end; evidence first copied to `.ufo/waves/round-46/w1/MutC2Counter/evidence/` (BASELINE.txt, M1…M9 suite outputs, probe-m1b.txt, probe-widetail.txt, 10 diffs, runner-copy.py, driver.sh, lane-hashes.txt). A scratch path is never cited as evidence.
- Tooling: no installs — python3 (stdlib only) and git already present. pacman untouched (host-wide pause respected). No host-service, compositor or input mutation; no hyprctl call needed for this probe.
- Leaf discipline: no subagents, no background jobs other than the seat's own driver run.

## Bottom line

The T1–T5 tightenings are each pinned by exactly the registered control designed for them (single-control kills, plus PROSE-CENSUS-SPACED doubling for T1). Three one-clause weakenings survive the registered suite: the locator span bound (M2 — closable with a start-preserving widening control, demonstrated), the census-pattern uniqueness sub-check (M1 — unprobeable from this freeze because the six census receipts are PINS-named and hash-pinned; value-changing census mutants still caught by P per M1b), and the quote-uniqueness sub-check (M3 — unprobed by the registered suite but killable, demonstrated, via the pin_ok None-membership hole at counter.py:532-534; see the M3 section and ConnCrossClaim-3's cross-claim). Scope note: "forging receipts dies at the pin hash" holds only for receipts whose NAME is in PINS; a self-authored receipt under FETCH/ with a name outside PINS binds (counter.py:532-534), which is what makes the M3 killing control and ConnCrossClaim's forged-admission route possible.
