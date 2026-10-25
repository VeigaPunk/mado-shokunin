# CritC2Cheat — the cheapest C2 cheat, and which cheaper paths are closed

Seat: CritC2Cheat (round 40, wave w1). Claim attacked: C2 / `PRED-C2-r40-v1`
(`quality/counters/c2-r40-forms-entry.py`, 265 lines, read in full).
Role: critic only — nothing in the lane was written; every fixture lived in `mktemp -d`
and was deleted. Writes: this file, `build-cheats.py`, `results.json` (all under
`.ufo/waves/round-40/w1/CritC2Cheat/`).

## 1. Counterexample (the cheat, measured)

A fabricated set of **5 files / 23 written lines / 1 468 new bytes / 0 external sources opened**
scores `admitted=1/1 verdict=TARGET_MET`, exit 0, on a base tree **byte-identical to the frozen
base** (`git rev-parse <fixture-base>^{tree} == b66eb95b8a0e4873686bce03cb2457a1b6251531`,
i.e. `9fc511d^{tree}`; asserted in the builder and reported as `base_tree_equals_frozen=true`).

The whole fabricated payload (cheapest variant, verbatim):

```
.ufo/waves/round-40/fetch/cheat.receipt.txt                 172 B / 3 lines
461f8c3c245bdfb6dcaac068a5ab378326c75dc91992b8012f9ca0e5019fb03a      <- sha256 of the committed tool
forms int=1 float=0 str=0 custom=0
labels agreement=1 agreement*=0 mismatch=0 config-only=0 live-default=0

corpus/knowledge/hyprctl-getoption-native-forms-r40.md      216 B / 8 lines
source: S162
source: S173
source: S900
source: S901
verified-at: 2026-10-25
recheck: 90d
S162 S173 S900 S901 forms int=1 float=0 str=0 custom=0
labels agreement=1 agreement*=0 mismatch=0 config-only=0 live-default=0

corpus/lessons/round-40.md                                  657 B / 6 lines
## Gate
GATE S162 receipt=.ufo/waves/round-40/fetch/cheat.receipt.txt sha256=1fc69302…cb1 quote="int=1 float=0 str=0"
GATE S173 receipt=<same path> sha256=<same> quote="int=1 float=0 str=0"
GATE S900 receipt=<same path> sha256=<same> quote="int=1 float=0 str=0"
GATE S901 receipt=<same path> sha256=<same> quote="int=1 float=0 str=0"

corpus/SOURCES.md (delta)                                   359 B
  S162, S173: cells 1-10 byte-identical to the frozen base row, only used-by gains ", <entry>"
  S900 | zz0 | docs    | A | s | a | t | mined | 2026-10-25 | 90d | <entry> |
  S901 | zz1 | own-work| A | s | a | t | mined | 2026-10-25 | 90d | <entry> |

corpus/README.md (delta)                                     64 B
| `knowledge/hyprctl-getoption-native-forms-r40.md` | cheat |
```

Counter output for it (fixture rev, one run; fixture commits carry a wall-clock date, so the
hash differs per run — `results.json` holds the run that produced the numbers here):
`PRED-C2-r40-v1: admitted=1/1 verdict=TARGET_MET rev=d5e8e5a49ce40b99b326300ce9ad655d61c2d15b`,
all clauses `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1`.

Not one byte of Hyprland, hyprlang or `ComplexDataTypes.hpp` was fetched. The only lane bytes
read were `corpus/SOURCES.md`, `corpus/README.md` and `tools/mado-options.py` (hashed, not
opened). `zz0`/`zz1` are locations that exist nowhere. The "census" is one unit; the real
capture is `70` lines (`wc -l .ufo/waves/round-40/c1/native-capture.jsonl` → `70`).

## 2. The four cheap tricks that make it this small

| Trick | Clause that should have caught it | Counter behaviour |
|---|---|---|
| **One receipt, one quote, four ids.** All four `GATE` lines share path+sha+quote; one 3-word quote satisfies four ids. | d/g imply per-id binding; `gates.setdefault` (`:165`) and `hit` (`:190`) never require distinct receipts, distinct quotes or receipt-to-id binding | passes |
| **N=1 "census".** Count lines are free text; the true capture is 70 keys. | h's floor is `nf == nl and nf >= 1` (`:222`) | passes with `int=1` |
| **Tool hashed, never run.** `sha256(tool)` is only searched in the receipt text (`:209-224`); the counts are never derived from the tool's stdout. | h (docstring `:18-20`) | passes with the *base* tool, and equally with a 3-line dummy (`V1`, below) |
| **Quote carried by a non-observation line.** The line that satisfies g is the `forms …` count line itself (`int=1 float=0 str=0` is 3 words inside it). | g ("one entry line names the id and carries its Gate quote") | passes |

Consequence: clause g is not an independent check — the same line satisfies h and g.
Clause h's sha check proves only that the receipt mentions a blob that exists, not that the
blob produced the numbers.

## 3. Variant matrix (all run; `results.json` holds every delta + full counter stdout)

| Variant | Base | Result | Files | Lines | New bytes |
|---|---|---|---|---|---|
| `V1-minimal-dummy-tool` (the task's literal ask: 3-line dummy tool, empty base registry) | minimal fixture | **1/1** | 5 | 23 | 1 600 |
| `V5-cheapest-realbase` (4 invented ids, no held row, 1 receipt, quote inside the forms line) | frozen base tree | **1/1** | 5 | 23 | 1 600 |
| `N3-held-proper` (S162/S173 byte-equal + used-by append, 2 invented ids) — **byte minimum** | frozen base tree | **1/1** | 5 | 23 | **1 468** |
| `M4-controlP-shape` (4 receipts, 4 quotes, 4 OBS lines — the declared residual's shape) | frozen base tree | **1/1** | 8 | 31 | 1 793 |
| `N1-round39-path` | frozen base tree | 0/1 (`d:0 g:0 h:0`) | 5 | 23 | 1 600 |
| `N2c-held-reopened-usedby-fixed` (opened re-dated **and** used-by appended: only `cells[:10]` differs) | frozen base tree | 0/1 (`c:0`, `S162/S173 new=0 status=mined used=1 ok=0`) | 5 | 23 | 1 356 |
| `N2-held-as-new-inplace` (opened re-dated, used-by left alone) | frozen base tree | 0/1 (`c:0`, `new=0 … used=0 ok=0`) | 5 | 23 | 1 356 |
| `N2b-held-as-new-appended` (rewritten copies appended beside the base rows) | frozen base tree | 0/1 (`c:0`, `rows=2`) | 5 | 23 | 2 886 |
| `N4-held-only` (4 held ids, 0 new) | frozen base tree | 0/1 (`c:0 e:0 h:0`) | 5 | 23 | 1 332 |

Lane as-is, for contrast: `python3 -I quality/counters/c2-r40-forms-entry.py --repo . --rev HEAD`
→ `admitted=0/1 verdict=TARGET_MISSED rev=e2b51d3b…`, exit 1.

## 4. Cheaper-path verdicts (the declared question)

- **Round-39 receipts: CLOSED, twice over.** (i) clause d requires the path prefix
  `.ufo/waves/round-40/fetch/` (`FETCH`, `:48`; `path.startswith(FETCH)`) — a round-39 path
  scores `d:0 g:0 h:0` (`N1`). (ii) even copied into round-40/fetch, they cannot serve: no
  round-39 receipt carries a count line — `git grep -c 'forms int=' 9fc511d -- .ufo/waves/round-39/`
  → no match, exit 1 — and they are 43 049–297 863 B each versus a 172 B invented receipt, and
  they cannot contain the round-40 tool sha. Reuse is strictly more expensive and still fails h.
- **Held rows as the "new" ids: CLOSED.** Three ways to try it, all `c:0`. (i) The counter classifies
  a base-present id as held before any cell check (`new=0` in `N2`/`N2c` output), so it can never
  reach `new_ids`. (ii) Byte-equality is the decisive wall: `N2c` re-dates `opened` **and** appends
  the entry to used-by, so `used=1` and status is `mined`, and it still scores `ok=0` — the only
  difference is `cells[:10]` (`opened` is index 8, inside the compared prefix, `:147-152`).
  (iii) Appending a rewritten copy beside the base row fails earlier on `rows=2` (`N2b`).
- **Held rows as held rows: marginally cheaper (1 468 B vs 1 600 B), not cheaper in effort.**
  The row bytes are already committed; only the used-by cell changes (~52 B each). It requires
  the base row to be `mined` (S162/S173 are, `2026-10-23`) and an in-place edit, not an append —
  appending a second row fails `c` (`rows=2`).
- **Cheaper than control P: yes.** P's shape costs 8 files / 31 lines / 1 793 B; the cheat costs
  5 files / 23 lines / ≤1 600 B. The saving comes from one shared receipt, one shared 3-word
  quote, N=1, and dropping the held row entirely.
- **Floor: 5 files.** Entry (a), receipt (d/h), lesson `## Gate` (d), `SOURCES.md` (c), `README.md`
  (f) are each named by a clause; none is avoidable, and the round-40 `fetch/` dir is empty at
  base and empty in the freeze commit (`git ls-tree … 5e7e885 -- .ufo/waves/round-40/fetch/` →
  no entries), so one new receipt file is mandatory.

## 5. What this attacks / supports

- **Supports** the registration's declared residual (`registration.md:94-96`) and its
  separability claim (`registration.md:96-97`): a fabricated set passes, and it passes without C1's verdict.
  The round cannot fail C2 for admitting fabrication — that tradeoff is declared.
- **Attacks** the *price* and the *shape coverage*: the residual is a ~1.5 KB family, not the
  control-P shape; and the predicate scores none of the claim's declared shape. `V5` cites four
  brand-new ids and **no held row**, yet `registration.md:73-75` requires "held S162 (…), S173
  (…) re-opened, plus at least two new rows". The counter cannot tell the declared deliverable
  from a set that contradicts it. Likewise `registration.md:72` declares the receipt states the
  host census (62/8/0 over 70 keys); the counter accepts 1/0/0/0/0 over 1 key.
- **Impacted axes:** coverage (C2) evidence value; the claim's "sourced" strength. C1 is
  unaffected — its fixtures run a stub compositor and its host receipt is the out-of-distribution
  check (`registration.md:61-63`). Any reading of C2's `TARGET_MET` as proof that the four native
  forms or the angle-inheritance rule were observed is unsupported by the predicate.

## 6. Smallest safe correction (for the integrator, not applied)

Two clauses, each independent, cheapest first:

1. **Bind the counts to committed bytes the counter recomputes (≈12 lines, kills N=1 and the
   sha-only tool binding).** Require the own-work receipt to name a committed capture path and
   require `forms int=A float=B str=C custom=D` to equal the histogram the counter computes from
   that capture's JSON objects, with `A+B+C+D ==` its line count (and `N` equal to it). The
   capture must then be a plausible 70-key file consistent with the counts; `V5`/`N3`/`V1` die.
   Still separable from C1 — a pure function over committed bytes, no C1 verdict.
2. **Score the declared shape (≈4 lines).** Require ≥1 cited id present at BASE with
   `cells[:10]` byte-equal (a re-opened held row) in addition to `len(new_ids) >= 2`. `V5`
   (four new ids) then fails; `N3` (1 468 B) still passes, so this alone is not sufficient.

The honest version of (1) is to run the committed tool with `--live` against a stub `hyprctl`
built from the committed capture and require the receipt's count lines to equal its stdout
(~40 lines, reusing C1's stub form). That is the only variant that makes the counts
*derived* rather than *asserted*; everything else leaves the residual at ~1.5 KB.

## 7. Reproduction and tooling

- Builder: `.ufo/waves/round-40/w1/CritC2Cheat/build-cheats.py` (all nine variants; fixtures
  `mktemp -d`, `git -C "$D" init -q`, toplevel verified equal to `$D`, throwaway identity via
  `-c`, `shutil.rmtree` in `finally`; lane read only via `git show` / `git archive`).
- Results: `.ufo/waves/round-40/w1/CritC2Cheat/results.json` (per variant: clauses, files,
  authored lines/bytes, delta text, full counter stdout).
- Tooling installed: **none** (python3 3.14 stdlib only). No pacman, no compositor verb, no
  network fetch, no lane write.
