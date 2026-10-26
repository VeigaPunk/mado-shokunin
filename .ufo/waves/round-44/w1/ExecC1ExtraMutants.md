# ExecC1ExtraMutants — extra C1 mutation population (round 44, w1)

**Assignment.** Mutation population for C1 beyond the 13 registered controls: single-defect mutants of
the reference's state logic, concentrated on `client_fsmode`; score each with the frozen
`PRED-C1-r44` counter; classify every survivor as EQUIVALENT (with proof) or MISSING CHECK (killing
input + expected output).

**Result in one line.** 51 new single-defect mutants built and scored (26 of them inside
`client_fsmode`); **20 reach `TARGET_MET`** and every one is a true equivalence (code proof +
20 000 randomised differential cases each, 0 differences); **31 are killed**; the sweep found **one
narrow counter hole** (the contract's `else 0` is not pinned for *negative* integer `fullscreen`
values — `M05`, `M51`) and **one measured clause-strength fact** (clause `b4`'s site census shrinks
14 → 13 when the state test is written as a chained compare or as truthiness).

## Method

* Reference: `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt`. Counter:
  `quality/counters/c1-r44-geometry-states.py`, rev `e2289516a9a857f55cda7be635933e89b931c3da`.
* `build.py` holds the population as `(name, note, [(old, new), ...])`; each replacement's
  occurrence count is asserted to be exactly 1 before the body is written
  (`BUILD total=51 bad=0`, 476 reference lines). Bodies:
  `.ufo/waves/round-44/w1/ExecC1ExtraMutants/mutants/` (51 files).
* Scoring, one counter run per body, fixed nonce so every body sees the same 12-case sgen lattice:

      cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I \
        quality/counters/c1-r44-geometry-states.py --repo . \
        --rev e2289516a9a857f55cda7be635933e89b931c3da \
        --tool .ufo/waves/round-44/w1/ExecC1ExtraMutants/mutants/<M>.py \
        --nonce mutsweep1 --work /fast/scratch/hyaku/mado-r44/ExecC1ExtraMutants/work/<M>

  Raw counter output is retained at `receipts/logs/<M>.log` (nonce `mutsweep1`) and
  `receipts/logs-n2/<M>.log` (nonce `mutsweep2`, survivors + `REF` only); the one-line results are
  `receipts/rc-mutsweep1.txt` and `receipts/rc-mutsweep2.txt`. The `--work` path above is the seat's
  transient scratch (created and deleted at seat finish; re-create it with `mkdir -p`) — nothing in
  this report cites it.
* Anchors: `REF` = `fixtures=26/26 clauses=a:1 b:1 b4:1 g:1 r:1 verdict=TARGET_MET` on both nonces
  (`receipts/logs/REF.log`).

## Population shape (51)

| family | mutants | examples |
|---|---|---|
| inside `client_fsmode` (membership, type guard, return value, key read) | 26 | `M01` `f in (1,2,3)`; `M02` `f in (1,)`; `M03` `f in (2,)`; `M05` `f in (-1,1,2)`; `M06` `1 <= f <= 2`; `M07` `f in {1,2}`; `M08` int guard dropped; `M13` bool guard → `not isinstance(f, float)`; `M15` `(int, float)`; `M18` `return bool(f)`; `M21` `return f % 3`; `M22` `return None`; `M25` `c.get("Fullscreen")`; `M26` state read gated on `floating` |
| verdict chain | 9 | `M27` MAXIMIZED before FULLSCREEN; `M28` `elif fsmode:`; `M29` `fsmode > 1`; `M30` `fsmode >= 1`; `M31` MAXIMIZED requires floating; `M32` `fsmode != 0`; `M33` BADSIZE only when flat; `M34` TILED only when flat; `M35` BADSIZE last |
| tally / summary suffix | 10 | `M36` MAXIMIZED counted as tiled; `M37`/`M38` counts swapped across fields; `M39` suffix values swapped; `M40`/`M41` suffix spacing; `M42` `>= 1`; `M43` `> -1`; `M44` suffix after `verdict=`; `M45` suffix before `tiled=` |
| counting reach / top verdict | 6 | `M46` unmapped fullscreen counted; `M47` unmatched fullscreen counted; `M48` unmatched counted as matched; `M49` maximized dump exits 1; `M50` new top verdict; `M51` membership test dropped, raw int returned |

## Survivors (20) — all EQUIVALENT, one also a MISSING CHECK

Full table with the per-mutant edit, measured verdict and proof:
**`.ufo/waves/round-44/w1/ExecC1ExtraMutants/survivors.md`**. Summary of the classes:

* *Value-domain moves that no consumer can see*: `M04` (`f in (0,1,2)` → returns 0), `M05`
  (`f in (-1,1,2)` → returns -1), `M06` (`1 <= f <= 2`), `M19` (`2 if f == 2 else 1`), `M20`
  (`min(f,2)`), `M21` (`f % 3`), `M17` (`str(f) in ("1","2")`). Proof: the returned mode is consumed
  only by `fsmode == 2` (ref:233) and `fsmode == 1` (ref:235); a value that matches neither is
  indistinguishable from 0.
* *Guard idioms that accept the same set*: `M09` `(int, bool)` + bool guard, `M10` `type(f) is int`,
  `M11` `type(f) is not bool`, `M12` `f is not True and f is not False`, `M16` conjunct reorder,
  `M24` `c.get("fullscreen", 0)`. (`M10` is the form the counter's own model uses,
  `quality/counters/c1-r44-geometry-states.py:90`.)
* *Order-insensitive or already-true tests*: `M27` (the two state tests are disjoint), `M28`
  (`elif fsmode:` after the `== 2` branch), `M29` (`fsmode > 1` given 0/1/2), `M30`
  (`fsmode >= 1` after the `== 2` branch), `M34` (`fsmode == 0` is already true at the TILED
  branch), `M42` (`>= 1` on two non-negative tallies).

Differential evidence `receipts/equivalence-diff.txt`: 20 bodies × 20 000 random client dumps
against the reference, **`DIFF TOTAL=0`**; the generator spans `fullscreen` ∈
{1, 2, 0, 3, -1, -7, 100, true, false, 2.0, `"2"`, null, [], [2], {"internal": 2}} and still reaches
97-148 `FULLSCREEN` verdicts, 114-152 `MAXIMIZED` verdicts and 223-278 state suffixes per body, so
the state paths are exercised.

### MISSING CHECK (predicate hole found by `M05`; killing input below)

`M05-fsmode-admit-neg` returns **-1** for `{"fullscreen": -1}`; the contract says fsmode is the value
"when it is a JSON integer (not a boolean, not a float) equal to 1 or 2, else 0"
(`quality/counters/c1-r44-geometry-states.py`, contract paragraph). Measured side by side
(`receipts/fsmode-probe.txt`): reference 0, `M05` -1, `M51` -1 — and `M05` still scores
`TARGET_MET`, all clauses 1, fixtures 26/26.

* **Killing input and expected output**: `client_fsmode({"fullscreen": -1})` must be `0`. The only
  place that can carry this assertion is the selftest case at ref:458 —
  `for v in (1, 2, 0, 3, True, 2.0, "1", None)], [1, 2, 0, 0, 0, 0, 0, 0])` — which pins the upper
  boundary (3) and every type guard but **no negative integer**. Extending that tuple with `-1` and
  expected `0` kills `M05` and `M51` and leaves the reference passing (91/91). No fixture can kill
  it: -1 and 0 are byte-identical on every output, which is exactly what the 20 000-case differential
  shows.
* **Severity**: low, and unreachable from production input — `hyprctl clients -j` prints
  `eFullscreenMode` 0/1/2 (`fetch-c1/Hyprland-HyprCtl.cpp`), so no live dump carries -1. The gap is
  contract pinning, not behaviour: today an implementation may violate the docstring's `else 0` for
  negative ints and still be admitted.
* **For the L1, not for me**: I did not touch the frozen counter. By the registration's rule ("a hole
  `w1` finds before any data commit re-registers as v2 with a new freeze") this is a v2 amendment
  candidate; alternatively it is recorded as a declared residual, since the reference is conforming
  and C1's own target is unaffected either way.

### Clause-strength fact (not a false kill): `b4`'s census is shrinkable by the tool

| body | membership test written as | b4 sites | killed | need | clause |
|---|---|---|---|---|---|
| reference | `f in (1, 2)` (ref:197) | 14 | 14 | 11 | pass |
| `M06-fsmode-range-chain` | `1 <= f <= 2` | 13 | 13 | 10 | pass |
| `M28-max-truthiness` | `elif fsmode:` | 13 | 13 | 10 | pass |
| `M12-guard-is-not-true` | `f is not True and f is not False` | 16 | 16 | 12 | pass |

`state_sites` counts only `ast.Compare` nodes with exactly one operator
(`quality/counters/c1-r44-geometry-states.py:283`), so a chained compare and a truthiness test are
invisible to it; the floor is 6 sites and the need is `ceil(0.75 * sites)`
(`...:76-77`, `...:294`). The 13 sites left in `M06`/`M28` are round-43 compares
(`evaluate:213..239`, `report:259..269`) whose flips break the selftest for reasons unrelated to
state. The clause still passes in every case I built, but the *marginal* tooth on the state branch is
one site and a tool can drop it by writing a chained compare. Recorded as a residual, not as a miss.

## Kill channels across the 31 misses

| channel | kills | mutants |
|---|---|---|
| fixtures only (selftest passes) | 1 | `M46-unmapped-fs-counted` (23/26) |
| selftest only (fixtures 26/26) | 3 | `M01-fsmode-extra-3`, `M22-fallback-none`, `M51-return-any-int` |
| fixtures and selftest | 27 | the rest |
| clause `r` independent | 0 | `r:0` exactly when `b:0` — the round-42 counter runs the same `--selftest` |
| clause `b4` independent | 0 | `b4` is skipped whenever `b` fails (`...:356-357`), so it cannot kill what the selftest does not |

`receipts/clause-channels.txt` is the per-mutant table this is computed from. The selftest-only kills
name their failing case (`receipts/selftest-only-kills.txt`):

* `M01` — `SELFTEST FAIL fsmode-values: got [1, 2, 0, 3, 0, 0, 0, 0] want [1, 2, 0, 0, 0, 0, 0, 0]`
* `M22` — same case plus `fsmode-absent: got None want 0`
* `M51` — same as `M01` (the raw int 3 reaches the value check, the raw int -1 does not)

So the 26 fixtures alone cannot tell `f in (1,2)` from `f in (1,2,3)`; and conversely the selftest
alone cannot see that `M46` counts a fullscreen mode for an unmapped client. Both clauses are
load-bearing for different mutants — the round-43 finding that "the selftest clause is load-bearing,
the fixtures alone are not" (registration, K13) has a mirror image here.

## Evidence (all inside the seat dir)

| file | what it is |
|---|---|
| `mutants/*.py` (51) + `build.py` | the population and its exactly-once replacement spec |
| `survivors.md` | the required table: mutant / edit / verdict / failing fixtures-clauses, plus proofs and the MISSING CHECK |
| `receipts/logs/*.log`, `receipts/logs-n2/*.log` | raw `PRED-C1-r44` output per body, two nonces |
| `receipts/rc-mutsweep1.txt`, `receipts/rc-mutsweep2.txt` | one line per run (52 / 21 rows): rc, clauses, final verdict |
| `receipts/determinism.txt` | the whole population re-run at nonce `mutsweep1`: 52 logs byte-compared, 0 differ |
| `receipts/fsmode-probe.txt` | `client_fsmode` return values for 13 input classes, reference vs 6 bodies |
| `receipts/equivalence-diff.txt` | 20 bodies × 20 000 cases, 0 differences, with reference coverage counts |
| `receipts/clause-channels.txt` | per-mutant verdict/fixtures/b/r table |
| `receipts/selftest-only-kills.txt` | the three selftest-only kills with their failing case text |
| `receipts/cite-check.txt` | 18/18 citations verified by `verify_cites.py` (file:line → quoted substring) |
| `run_sweep.sh`, `summarize.py`, `probe_fsmode.py`, `equivalence_diff.py`, `write_survivors.py`, `verify_cites.py` | the reproducible drivers |

## Risks and limits

* The sgen lattice varies with the nonce by design (registration, C1 "Before": 12-13/26 at base); I
  fixed the nonce for comparability and re-ran the 20 survivors on a second nonce with identical
  results. Findings that depend on a lattice count are quoted with their nonce. The fixed nonce is
  reproducible: two full 52-run sweeps at `mutsweep1` produced byte-identical counter output
  (`receipts/determinism.txt`).
* Diachronic equivalence: my proofs reason over the *current* consumers of `fsmode`
  (`== 2`, `== 1` only). If a later edit consumes the raw mode (`if fsmode:`, a tally of the mode,
  a print), `M04`/`M05` and the `M27..M30` order/idiom survivors stop being equivalent. That is a
  latent invariant the counter does not state; it is not a defect in today's tool.
* `M10`/`M11` equivalence assumes inputs come from `json.loads` (no int/bool subclasses); a decoder
  that produced an `IntEnum` or a bool-like object would split them.
* No negative-int fixture can exist by construction (output-identical), so the MISSING CHECK above is
  the only kill path — a fixture-based closure of that hole is impossible, only a value-level check.
* Untouched, as required: the frozen counter, the reference, the controls, the registration, the
  pins, the shokuknow checkout, the host (no pacman, no compositor mutation; only `python3` and the
  lane's own files were executed). No tracked file in the lane was edited; my writes are this report
  and the seat dir.
* Not run, by design: the build/lint/test gate (the parent owns post-integration verification), and
  the 13 registered controls (the frozen `.ufo/waves/round-44/receipts/ctl-c1.txt` stands).

## Unresolved

None blocking. One decision routed to the L1 (not mine to take): whether the negative-integer gap is
closed by a v2 freeze of `PRED-C1-r44` (one tuple element at ref:458) or recorded as a declared
residual before the C1 data commit.
