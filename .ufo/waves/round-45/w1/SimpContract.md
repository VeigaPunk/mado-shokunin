# w1/SimpContract — dead weight in the C1 contract and the C2 clause h/i/j delta

Status: **complete**. No lane file was edited (frozen inputs read only); every mutation ran on a scratch copy. Scratch
(`/fast/scratch/hyaku/mado-r45/SimpContract/`) removed after its receipts were copied here.

Deliverable: `.ufo/waves/round-45/w1/SimpContract/dead-weight.md` (per-sentence verdicts, exact deletion texts, proofs).

## Criterion

Output = `(stdout, exit code)`. DEAD = no input changes it on deletion (and no new exception); DEAD-UNDER-PINS = no
*admissible* input, because a C2 receipt must hash to a frozen pin; GUARD = the deletion only turns a note into a
traceback; LIVE = a concrete (config, dump) pair exhibited.

## C1 reference (`l1-draft/mado-monitors.py`) — 7 dead parts

Applied together as `w1/SimpContract/mado-monitors-minus-dead.py`, scored with the frozen counter on a clone of
`22a8ded`: `fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, rev `5a5064f` (`score-minus-dead.log`);
and 0 output differences over 3 624 differential cases (`replay-minus-dead.log`).

| # | locator | deleted text | why no input sees it |
|---|---|---|---|
| D1 | `:324` | `math.isfinite(x) and ` | `w`,`h` are ints and `s ≥ 0.25`, so `w / s` is finite or raises inside the division |
| D2 | `:332` | `z > 0 and ` | `k = floor(s*120+0.5) ≥ 30` ⇒ `z ≥ 0.25` |
| D3 | `:336` | `cand != 0 and ` | `cand == 0` needs `i == k ≤ 89`; `i = k-30` (cand `0.25`) precedes it for `k ∈ [31,89]`; `k = 30` returns at the `z` branch. Sweep `k=30..1200 × 15 widths`: 0 diffs |
| D4 | `:393` | `isinstance(mo, str) and ` | a non-string JSON value never equals `str(ids[0])` |
| D5 | `:392` | `str_or_empty(`…`)` around `m.get("name")` | the branch needs a non-empty `str` mirror; a non-string name never equals it |
| D6 | `:346` | `str_or_empty(`…`)` around `mon.get("name")` in `effective` | `name` is used only by `elif sel == name`, and empty selectors are skipped one line earlier (that skip is LIVE, M15) |
| D7 | `:296-297` | the `continue` after `counts["v2"] += 1` | `V2_RE` and `LINE_RE` are disjoint (`LINE_RE.fullmatch` → `None` for `monitorv2`, `monitorv2=1`, `monitorv2{`, `monitorv2foo`) |

Redundant wording (no code change): `keeps at most one rule per selector string` (`:6`) makes "the **first** rule"
vacuous at `:8`, `:38`, `:61` — the list is a function from selector to rule.

## The four suspects in the tasking

| suspect | verdict |
|---|---|
| `len(ids) >= 1` (`:393`) | **LIVE** — `mirror, NOPE` with no such output: DIFFER vs `IndexError` |
| `cand != 0` (`:336`) | **DEAD** (D3) |
| the `V2_RE` tail `monitorv2(?:[ \t={]|$)` (`:100`) | **LIVE, all four members** — `=`, `{`, space/tab and `$` each have a distinguishing line |
| `toks[0] == "modeline"` vs `startswith` (`:194`) | **`==` is correct**; `startswith` would model `modelines` as a modeline (ref `NOT_COMPARED 5` → mutant `OK 0`). The `toks and` guard in the same line is LIVE too (a mode field of only `\r`) |

The f32 clauses (rate at `:202`, scale at `:219`, `f32(z)`/`f32(cand)` at `:333,:337`) are LIVE but only inside the
tolerances: a live value placed on the band edge of `|scale-E| < 0.0001` (or `|rr-RATE| < 1.0`) flips the verdict
(`h5.log`); realistic monitors cannot see them.

## C1 defects exposed (not dead weight — falsifier material for w2)

1. A huge integer live value (`{"width": 10**400}`; likewise `refreshRate`, `scale`) crashes the tool:
   empty stdout, `OverflowError: int too large to convert to float`, exit 1 — contradicting
   `A live value that is missing or of the wrong JSON type` (`:77`) and `stderr empty on exit 0/1/3/4/5` (`:81`).
2. `w > 0 and h > 0` (`:384`) is undocumented: with `width = height = 0` the docstring's algorithm would compare
   `E = S`, the code skips. Witness: rule scale `2`, live `0x0`/scale `1` → `AGREE 0`; guard removed → `DIFFER 1`.
3. **Five live semantics are not pinned** by PRED-C1-r45: the `i < 90` bound, the `(K+i)`-before-`(K-i)` order, the
   empty-selector skip, the f32 requested rate, and the `w>0` guard all still score `fixtures=49/49 ... TARGET_MET`
   after mutation (and none is in controls K03–K15). The C1 residual "the fixtures are the contract's cases" is
   short by at least five cases with witnesses.

## C2 counter (`quality/counters/c2-r45-monitor-entry.py`) — clause h/i/j

Differential against the positive-control repo (`build-pos.py`, `admitted=1/1`).

* **Delete (dead for every input):** D8 unused parameters `new_ids, reg_rev` of `host_census` (`:318`, call `:579`);
  D9 the `(?!\d)` tail of the clause-j locator regex (`:398`; 200 000 fuzz strings, identical `findall`); D10
  `gl[0] is not None` (`:322`; the only `None` gate value sits under the non-id key `"<indented>"`). Combined as
  `w1/SimpContract/ctr-minus-D8-D10.py`: stdout, stderr and rc byte-identical, `admitted=1/1`.
* **Dead under the pins (keep or delete deliberately):** D11 `(?:\.[0-9]+)?` (`:328`), D12 the
  `after = mon[mon.index(...):]` slice (`:335`; the pinned `Monitor.cpp` holds exactly one `for (size_t i = 1; `),
  D13 the `len(r) != 1 or …` guard (`:333`). Keep D13: deleting it turns a future re-pin mismatch into a traceback.
* **Guards kept (output-changing when deleted, evidenced on damaged clones):** `if rows and len(rows[0]) == 11`
  (`:620`, `IndexError` on a repo missing a cited row), `raw is not None and` (`:627`, 17 extra clause-j lines at
  the base revision), `if not all(n in byname for n in need)` (`:326`, `KeyError` when a pin is not gated).
* Load-bearing by construction (not candidates): `not set(PINS) <= used` (the only all-nine-pins check), the
  `BAD_LOC` scans, `JWIDTH`, the clause-h prose check, `hits` uniqueness in `surfaces_ok`.

## Evidence (this directory)

`dead-weight.md` (deliverable) · `mado-monitors-minus-dead.py` · `ctr-minus-D8-D10.py` · `h1.log` (37 C1 mutations, 15 with no witness,
3 624 cases) · `h2.log` (constructed + setup witnesses) · `h5.log` (f32 band witnesses) · `jfuzz.log` ·
`c1score.log` (ref / deletions4 / unpinned mutants) · `score-minus-dead.log` (the seven deletions) ·
`replay-minus-dead.log` (3 624-case differential) · `c2mut.log` · `c2guard.log` ·
`quotecheck.log` (`FAILURES=0`: every quote ≤25 words, locator greps the frozen file). Scripts beside the logs;
they read the frozen lane paths and write under `/fast/scratch/hyaku/mado-r45/SimpContract/` (recreate it to rerun).

## Tools installed

None — no package, binary or PATH change was needed. `pacman` untouched; no compositor, service or Wayland-client
action; the live host was never read for this seat.

## Limits

The C2 deletions are proposals only (the counter is frozen). D3 depends on the `0.25` clamp, D6 on the
empty-selector skip being LIVE, and D11–D13 are dead *by pin hash*, not by logic. Nothing here re-scores C1 or C2
beyond the commands in the registration.
