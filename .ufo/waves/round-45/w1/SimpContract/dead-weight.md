# Dead weight in the C1 contract and the C2 clause h/i/j delta

Seat `SimpContract`, mado round 45 w1. Inputs are FROZEN and were read only:
`l1-draft/mado-monitors.py` (the C1 reference contract, selftest 33/33) and
`quality/counters/c2-r45-monitor-entry.py` (PRED-C2-r45). Nothing in the lane was edited; every mutation ran on a
scratch copy under `/fast/scratch/hyaku/mado-r45/SimpContract/`.

## 1. Criterion

Output := `(stdout, exit code)` — for the tool, of `report()`/`run()`; for the counter, of the whole run.

* **DEAD** — no input changes the output when the part is deleted, and the deletion adds no new exception.
* **DEAD UNDER THE PINS** — no *admissible* input changes the output, because the C2 counter only ever parses
  receipts whose sha256 equals a frozen pin (clause d binds a receipt to `PINS`; `receipts_raw` is filled only
  inside that check), so the byte string is a single point. The deletion is safe now and only a re-pin can make the
  part live again.
* **GUARD** — deleting it changes output only by turning a note into a traceback; not proposed for deletion.
* **LIVE** — a concrete input pair is exhibited (config + dump) where reference and mutant differ.

Method: differential mutation against (i) the 49 frozen C1 fixtures, (ii) a 2 500-case seeded generator over the
`monitor =` grammar and the dump types, (iii) constructed witnesses for the boundary clauses, (iv) `report()`
differentials for the counter on the positive-control repo. Scripts and logs: `h1.py`/`h1.log` (37 mutations, 15 with no witness),
`h2.py`/`h2.log` (constructed witnesses, setup paths), `h5.py`/`h5.log` (f32 family), `jfuzz.py`/`jfuzz.log`,
`c1score.py`/`c1score.log`, `c2mut.py`/`c2mut.log`, `c2guard.py`/`c2guard.log` (all copied beside this file).

## 2. C1 — reference `mado-monitors.py`: dead parts, with the exact deletion

All seven deletions together (`mado-monitors-minus-dead.py`) were replayed against the frozen counter
(`score-minus-dead.log`, rev `5a5064fea2aa2ae3a0f92dc768b19deda44e677c`): fixtures 49/49, selftest 33/33, readonly
ok, `verdict=TARGET_MET` — and against the 3 624-case differential corpus: 0 differences (`replay-minus-dead.log`).

| # | locator | what dies | why no input can see it |
|---|---|---|---|
| D1 | `mado-monitors.py:324` | `math.isfinite(x) and ` | `w`,`h` are ints (`is_int(w) and is_int(h)` gate at `:381`) and `s`/`cand` ≥ 0.25, so `w / s` is a finite float or raises `OverflowError` inside the division — `whole()` never receives a non-finite value |
| D2 | `mado-monitors.py:332` | `z > 0 and ` | `k = floor(s*120+0.5)` with `s ≥ 0.25` (the clamp is `rule["scale"] = 1.0 if s < 0.25 else s`, `:220`) ⇒ `k ≥ 30` ⇒ `z ≥ 0.25 > 0`, always |
| D3 | `mado-monitors.py:336` | `cand != 0 and ` | `cand == 0` needs `i == k ≤ 89`; for `k ∈ [31,89]` the candidate `(k-(k-30))/120 = 0.25` at `i = k-30 < k` always divides a positive integer `w`,`h` and returns first; `k = 30` returns at the `z` branch. Sweep `k = 30..1200 × 15 widths`: 0 differences |
| D4 | `mado-monitors.py:393` | `isinstance(mo, str) and ` | `mo == str(ids[0])` already rejects every non-string JSON value (int/float/bool/null/list/dict never equal a `str`); 3 624-case type corpus: no witness |
| D5 | `mado-monitors.py:392` | `str_or_empty(` … `)` around `m.get("name")` | this branch runs only when `rule["mirror"]` is a non-empty `str`; a non-string `name` never equals it, and `str_or_empty(non-str) == ""` does not either |
| D6 | `mado-monitors.py:346` | `str_or_empty(` … `)` around `mon.get("name")` in `effective` | `name` is used only by `elif sel == name`, where `sel` is a non-empty `str` (empty selectors are skipped one line earlier); non-string `name` fails both ways |
| D7 | `mado-monitors.py:296-297` | the `continue` after `counts["v2"] += 1` | `V2_RE` and `LINE_RE` are disjoint: `LINE_RE` needs `[ \t]*=` right after `monitor`, and `V2_RE` needs `v2` there (`LINE_RE.fullmatch` on `monitorv2=1`, `monitorv2{`, `monitorv2`, `monitorv2foo` → `None` for all four) |

Exact edits:

```text
D1  -    return math.isfinite(x) and x == math.floor(x + 0.5)
    +    return x == math.floor(x + 0.5)

D2  -    if z > 0 and whole(w / z) and whole(h / z):
    +    if whole(w / z) and whole(h / z):

D3  -            if cand != 0 and whole(w / cand) and whole(h / cand):
    +            if whole(w / cand) and whole(h / cand):

D4  -        if not (isinstance(mo, str) and len(ids) >= 1 and mo == str(ids[0])):
    +        if not (len(ids) >= 1 and mo == str(ids[0])):

D5  -        ids = [m.get("id") for m in mons if str_or_empty(m.get("name")) == rule["mirror"] and is_int(m.get("id"))]
    +        ids = [m.get("id") for m in mons if m.get("name") == rule["mirror"] and is_int(m.get("id"))]

D6  -    name, desc = str_or_empty(mon.get("name")), str_or_empty(mon.get("description"))
    +    name, desc = mon.get("name"), str_or_empty(mon.get("description"))

D7  -        if V2_RE.match(line):
    -            counts["v2"] += 1
    -            continue
    +        if V2_RE.match(line):
    +            counts["v2"] += 1
```

D1 is a defensive guard as well as a dead conjunct: nothing observable changes, but keeping it costs one call and
suggests protection the tool does not have (see §4, huge ints). D6 interacts with the empty-selector skip: if
D6 is applied, `name` must never be compared while an empty selector is in play — that is exactly the skip that
`M15` proved LIVE, so D6 must not be applied together with a rewrite of `effective()`.

## 3. C1 — the four suspects named in the tasking

| suspect | verdict | witness or proof |
|---|---|---|
| `len(ids) >= 1` in the mirror lookup (`:393`) | **LIVE** | rule `mirror, NOPE` with no output of that name: ref `differ=mode,mirror verdict=DIFFER`; without the guard `IndexError: list index out of range` (`h1.log` M6) |
| `cand != 0` (`:336`) | **DEAD** | D3 above |
| the `V2_RE` tail `monitorv2(?:[ \t={]|$)` (`:100`) | **LIVE, every member** | drop `[ \t={]` ⇒ `monitorv2foo` counts (`v2=1`, `NOT_COMPARED 5` vs `DIFFER 1`); drop `=` ⇒ `monitorv2=1` stops counting; drop `$` ⇒ a bare `monitorv2` line stops counting (`h1.log` M8/M9/M10) |
| `toks[0] == "modeline"` vs `startswith` (`:194`) | **`==` is correct, `startswith` is a defect** | `modelines`/`modelineX`: ref `unsupported=1 NOT_COMPARED 5`, `startswith` adds a modeline rule and reports `OK 0` (`h1.log` M11). The `toks and` guard in the same line is **LIVE** too: a mode field that is only `\r` (CRLF file) splits to no tokens — ref `NOT_COMPARED`, without the guard `IndexError` (`h1.log` M12) |

Also LIVE (mutations in `h1.log`/`h2.log`/`h5.log`, in no particular order): `##`/`$`/backslash guards (`M31a-c`),
comment cut (`M32`), `SCALE_RE` two-digit bound (`M33`), rule numbering (`M35`), `str_or_empty` in the output name
(`M37`), the empty-mode disjunct (`M40`), `parse_pos`/`parse_scale` empty disjuncts (`M42`/`M43`), the `0.25`
clamp boundary (`M18`), `transform_value`'s `len()==1` (`M29`), `addreserved`'s four-field bound (`M30`),
`S_ISREG` (a `--config /dev/null` accepted as an empty config without it, `h2.log`), `O_NONBLOCK` (a FIFO
`--config` hangs the mutant, `h2.log`), the duplicate-`--monitors` check (`SETUP usage` vs a normal run, `h2.log`),
`errors="replace"` (a non-UTF-8 config: `NOT_COMPARED 5` vs `UnicodeDecodeError`), `too_large` (1 048 577-byte
config → `SETUP too_large`), the f32 rate (§below), `desc:` TEXT stripping, the `w>0`-guarded scale compare, and
the `mirrorOf == "none"` default.

**The f32 clauses are LIVE but only inside the tolerance band.** `@999.999` with a live `1000.9990134375`
(`f32(999.999)+0.99999`) flips `|rr-RATE| < 1.0`; and because `|scale - E| < 0.0001` is a strict bound, *any*
non-zero difference between the two `E` values is observable by putting the live scale inside the band edge:
`M21` (scale, `w=h=1463669825208320`), `M22` (`K±i` candidate), `M23` (`K/120`) each produce ref `AGREE 0` vs
mutant `DIFFER 1` (`h5.log`). A mutation test that only feeds realistic monitors will not see them.

## 3a. Redundant *wording* (no code change; no output can depend on it)

The docstring states the erasure invariant - `keeps at most one rule per selector string` (`:6`) - and then says
`else the first rule with an empty selector` (`:8`), `The first rule` (`:38`), `else the first rule whose selector
is ""` (`:61`). Because `add()` is the only appender and it erases equal selectors, the rule list is a function
from selector to rule: at most one empty-selector rule can exist, and at most one rule can carry `SEL`. "first"
is therefore vacuous at all three sites, and the linear scans (`for r in rules: if r["sel"] == sel`,
`for n, r in enumerate(rules, 1): if r["sel"] == ""`) are total. Deleting the wording removes three unprovable
cases from the contract; deleting the loops changes nothing observable but is not worth the churn.

## 4. C1 — contract defects the exercise exposed (not dead weight)

1. **A huge integer live value crashes the tool.** The sentence `A live value that is missing or of the wrong JSON
   type` (`:77`) promises that only a *wrong JSON type* fails its field; an `int` outside the float range is the
   right type. `{"width": 10**400}` (also `refreshRate`, `scale`) gives empty stdout, a
   `OverflowError: int too large to convert to float` traceback and exit 1 — the sentence
   `stderr empty on exit 0/1/3/4/5` (`:81`) is violated too (`h2.log`). Both the mode test and `whole()` do
   int→float arithmetic on unvalidated ints.
2. **`w > 0 and h > 0` at `:384` is not in the contract.** The sentence `none found means the scale is not
   compared` (`:73`) enumerates the only skip; the docstring's algorithm would compute `E = S` for
   `width = height = 0` and compare. Witness: rule scale `2`, live `0x0` scale `1` → reference `AGREE 0`;
   without the guard `differ=scale DIFFER 1` (`h2.log` M44).
3. **Five live semantics are not pinned by the frozen counter.** Mutating each in turn and re-scoring gave
   `fixtures=49/49 selftest=ok verdict=TARGET_MET` for: the `i < 90` bound (`M3`), the `(K+i)`-before-`(K-i)`
   order (`M4`), the empty-selector skip (`M15`), the f32 requested rate (`M20`), and the `w>0` guard (`M44`)
   (`c1score.log`). None of them is in controls K03–K15 either. So "the fixtures are the contract's cases"
   (registration, C1 residuals) is short by at least five cases; witnesses are in §3 and `h2.log`.

## 5. C2 counter — clause h/i/j delta

Differential run: the counter against the positive-control repo (`build-pos.py` on a clone of the freeze,
`admitted=1/1`), then each mutation of the counter against the same repo, whole stdout + rc compared (`c2mut.log`).

### 5.1 Dead, delete

| # | locator | what dies | proof |
|---|---|---|---|
| D8 | `c2-r45-monitor-entry.py:318,579` | the parameters `new_ids, reg_rev` of `host_census` | not referenced anywhere in the body (only `gates`, `receipts_raw`, `lines`, `byname`, `need` are); call site passes them in vain. Every input yields identical stdout |
| D9 | `:398` | the `(?!\d)` tail of the clause-j locator regex | after a greedy `(\d+)` — with or without the optional `-(\d+)` — the next char is never a digit, so the assertion never fires. 200 000 fuzzed strings and 7 corner cases: `findall` identical (`jfuzz.log`) |
| D10 | `:322` | `gl[0] is not None and ` | `gates[i]` for a cited id (`S\d{3,}`) can only hold 3-tuples from `GATE_RE`; the single `None` append is under the key `"<indented>"`, which is never an id. `gl and ` stays (it is the empty-list guard) |

```text
D8  - def host_census(new_ids, reg_rev, gates, receipts_raw, lines):
    + def host_census(gates, receipts_raw, lines):
    -     h_ok, census_lines = host_census(new_ids, reg_rev, gates, receipts_raw, lines)
    +     h_ok, census_lines = host_census(gates, receipts_raw, lines)

D9  -         pat = re.compile(r"(?<![\w.-])%s:(\d+)(?:-(\d+))?(?!\d)" % re.escape(rname))
    +         pat = re.compile(r"(?<![\w.-])%s:(\d+)(?:-(\d+))?" % re.escape(rname))

D10 -         if i in receipts_raw and gl and gl[0] is not None and len(gl) == 1:
    +         if i in receipts_raw and gl and len(gl) == 1:
```

D10's neighbour at `:322` is *not* dead: `gl and ` prevents an `IndexError` when a cited id has no gate, and
`len(gl) == 1` is the clause.

### 5.2 Dead under the pins (safe now; a re-pin revives them — keep or delete deliberately)

| # | locator | what dies | proof |
|---|---|---|---|
| D11 | `:328` | `(?:\.[0-9]+)?` in `([0-9]+(?:\.[0-9]+)?);` | the only admissible `MonitorRule.hpp` has `float m_refreshRate   = 60; // Hz` → `['60']` with or without the decimal group |
| D12 | `:335` | the `after = mon[mon.index("std::round(m_scale * %s.0)" % k[0]):]` slice (search all of `mon`) | the pinned `Hyprland-Monitor.cpp` holds exactly one `for (size_t i = 1; i < ` (`grep -c` = 1), at line 1010, after line 1001 |
| D13 | `:333` | `if len(r) != 1 or len(t) != 1 or len(k) != 1 or len(p) != 1: return False, []` | each of the four regexes returns exactly one match on the pinned bytes: `['60'] ['1'] ['120'] ['5']` |

D13 is the one I would keep: deleting it converts a future re-pin mismatch from `clause h = 0` into
`AttributeError: 'NoneType'`. D11/D12 are shape noise that a re-pin would silently widen; the same argument holds,
so the recommendation is "delete D11/D12 if the pins are to be refreshed with the regexes re-derived, otherwise
leave them".

### 5.3 Guards tested and kept (output-changing when deleted)

| locator | evidence |
|---|---|
| `:620` `if rows and len(rows[0]) == 11:` | a repo with the `S302` registry row deleted: reference prints `clause=c id=S302 rows=0` and `admitted=0`, the mutant dies with `IndexError: list index out of range` (`c2guard.log`) |
| `:627` `cl["j"] = int(raw is not None and surfaces_ok` | at the base revision (entry absent) the mutant emits 17 extra `clause=j surface=… receipt_missing` lines (`c2guard.log`) |
| `:326` `if not all(n in byname for n in need):` | a repo with the `S306` gate dropped: reference `admitted=0` with the clause lines, the mutant dies with `KeyError: 'Hyprland-Monitor.cpp'` (`c2guard.log`) |

Load-bearing by construction, so not even candidates: `used`/`not set(PINS) <= used` (the only place all nine pins
must be covered — a repo citing four gated pins passes a–h and fails only i), the `BAD_LOC` scan over rows and
entry lines, `JWIDTH`, the `if h_ok:` prose check and its `rstrip`, `hits` uniqueness in `surfaces_ok`, and
`if not re.search(kw, l, re.I): continue`.

## 6. Preserved contract

* C1: the seven deletions together, committed as `tools/mado-monitors.py` in a clone of `22a8ded`
  (`score-minus-dead.log`, rev `5a5064f`): `fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET`,
  exit 0. The 3 624-case differential corpus (49 fixtures + 2 500 seeded random + targeted families) shows 0 output
  differences (`replay-minus-dead.log`).
* C1 behaviour kept that the deletions do not touch: every clause named in §3, the eight setup reasons, the
  verdict order, and the `differ=` field order.
* C2: the three deletions (D8–D10) leave `admitted=1/1 verdict=TARGET_MET` and byte-identical stdout on the
  positive-control repo (`c2mut.log`). The counter is frozen, so this is a proposal for the next revision, not an
  edit.

## 7. Tradeoffs

* D1 and D2 are the only places where "dead" and "defensive" coincide: removing them documents the invariant
  (`s ≥ 0.25`) instead of hiding it behind an unreachable test. The real defect (§4.1) stays open either way.
* D3's proof depends on the clamp in `parse_scale`; if the clamp is ever moved after the search, `cand != 0`
  becomes live again.
* D6 depends on the `if sel == "": continue` skip, which is LIVE (M15). Applying D6 while touching that skip is
  the one ordering that breaks.
* D9 removes a regex assertion that is redundant *as written*; it is not an instruction to loosen the locator
  (the `(?<![\w.-])` lookbehind stays and is live).
* Under the pins, D11–D13 are dead by hash, not by logic; "dead" there means "unreachable until someone changes
  `PINS`", which is the honest limit of a pin-based predicate.
