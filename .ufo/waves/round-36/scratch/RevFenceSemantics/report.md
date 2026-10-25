# RevFenceSemantics — round-36 `## Registry` fence vs fleet census E12

Seat: reviewer. Verdict: **the repaired C1 counter's registry fence diverges from the
census's E12 fence in four concrete ways; three of them make the counter accept trees
the census rejects (E12). On all seven assignment cases the census oracle itself is
used and quoted below; agreement holds on six, with one disagreement (case C) added.**

## 1. The oracle: census E12 and its own fixtures

`scripts/sources-census.sh` (fleet root), `row_pass()` gawk program:

```awk
609:  if (line ~ /^ {0,3}##[ \t]/) {
610:    sub(/^ {0,3}/,"",line)
611:    in_registry=(trim(substr(line,3))=="Registry")
612:    next
613:  }
614:  if (line ~ /^ {0,3}#[ \t]/) { in_registry=0; next }
615:  if (line !~ /^ {0,3}\|/) next
...
618:  if (!in_registry) {
619:    if (mode=="validate" && $0 ~ /^\|[ \t]*S[0-9]{3,}[ \t]*\|/) {
620:      id=trim($2)
621:      printf "%s\tE12\t%s row outside Registry section\n",lane,id
```

Header comment (lines 40-42): *"Maintained parser accepts 0–3 leading ASCII spaces before
Markdown rows/headings; 4 or more spaces are indented code and ignored. Frozen manual
examples assume column-zero input."*

Selftest oracle fixtures (same file, lines 298-345): for each indent width 0..3, a
registry whose `## Registry` heading is indented that width is counted clean
(`indented-valid-<w>-counted` → `rows 1`, `indented-valid-<w>-clean` exit 0), a
`## Paths` section after the registry holds an S-shaped row that must fire E12
(`indented-outside-<w>-E12` → `E12 <S94w> row outside Registry section`, exit 1).
The full selftest passed: `selftest ok`, exit 0.

**E12 section semantics distilled from the oracle source**: (a) a `##` heading opens the
Registry section only when its content trims to exactly `Registry`; (b) any other `##`
heading, any `#` heading, closes the section; (c) `###` subheadings are *not* headings
(lines 609/614 regexes need 2 or 1 hashes + space) so they neither open nor close;
(d) a row-shaped line outside the section (or with no section present) is E12 only when
its first cell is `S[0-9]{3,}`; (e) 4+ leading spaces make the line invisible (code
indent); (f) multiple `## Registry` headings re-open the section.

## 2. The fence path the repaired counter must take

Frozen spec `round-36/c1/frozen.json` (line 3, exact text): *"…the `## Registry` section
of the registry holds exactly one well-formed row for that id (a row-shaped line outside
that section, or a registry with no such section, scores nothing)…"*. Registration
`round-36/registration.md` lines 34-37: `c1-idle-lock.py` carries a `row-in-registry`
clause, *"the census's E12 fence, routed by round-35's RevC1Tip F2"*.

Round-35 counter (`round-35/c1/count.py` lines 118-124) has no fence at all: `rows_for`
scans every line (`ROW_RE = ^ {0,3}\|\s*(S[0-9]+)\s*\|`), so the r35 "golden" tree —
`## Registry` heading removed, S-rows at column zero (golden/corpus/SOURCES.md lines
1-10) — was accepted. That is what `c1-no-registry-heading` kills.

The repaired counter exists (uncommitted, wave-1 build; `git status` shows
`?? quality/counters/`): `quality/counters/c1-idle-lock.py`. Its fence:

```python
106:def registry_section(sources: str) -> str:
110:    for line in sources.splitlines():
111:        if re.match(r"^ {0,3}##[ ]", line):
112:            keep = line.strip().lower().startswith("## registry")
113:            continue
114:        if keep:
115:            out.append(line)
```

## 3. Per-case results (census fixture as oracle)

For every case the same 8 real registry rows (S203–S210, byte-copied from the lane's
live `corpus/SOURCES.md`) and the lane's real receipts/entries are used, so the counter's
digest/quote/used-by clauses stay satisfiable and the *only* variable is the fence.
Census: `sources-census.sh validate|сensus --file <tree>/corpus/SOURCES.md`. Counter:
`python3 -I quality/counters/c1-idle-lock.py --root <tree> --frozen .ufo/waves/round-36/c1/frozen.json`.

| # | Case | Census oracle | Counter | Verdict |
|---|---|---|---|---|
| A | 0–3 leading spaces on `## Registry` (0/2/3) | rows=8, no E12, exit 0 | closed_rows=8, exit 0 | **agree** |
| B | `## Registry` at 4-space indent (code) | rows=0, no E12 (rows invisible), exit 0 | closed_rows=0, exit 1 | **agree** (both ignore) |
| C | S-row above `## Registry` | rows=8 **and** `E12 S203 row outside Registry section`, exit 1 | closed_rows=8, TARGET_MET, exit 0 | **disagree** (counter misses stray above-section row) |
| E | second `## Registry` inside | rows=8, no E12, exit 0 | closed_rows=8, exit 0 | **agree** (section re-opens) |
| F | `###` subheading inside `## Registry` | rows=8, no E12, exit 0 | closed_rows=8, exit 0 | **agree** (subheading does not close) |
| G | registry with no rows | rows=0, no E12 (no S-shaped row), exit 0 | closed_rows=0, exit 1 | **agree** |
| H | no `## Registry` at all | rows=0, `E12 S203..S210` ×8, exit 1 | closed_rows=0, exit 1 | **agree** |

## 4. Divergences found (beyond the seven assignment cases)

Four concrete cases where the counter's fence and census E12 diverge, each reproduced
with output:

**D1 — `## Registry` prefix accepted by counter, rejected by census (HIGH).**
Heading `## Registry of X`: census → `rows=0` and 8× `E12 S### row outside Registry
section`, exit 1; counter → `closed_rows=8 closed_entries=3 open_cites=0 verdict=TARGET_MET`,
exit 0. Cause: counter line 112 `startswith("## registry")` vs census line 611 exact
`trim(substr(line,3))=="Registry"`. A tree whose registry heading carries any suffix
(e.g. a heading `## Registry (mado)` or `## Registry of sources`) scores full `TARGET_MET`
with the counter while the census treats every row as outside the section.

**D2 — case-insensitive heading (HIGH).** Heading `## registry`: census → 8× E12,
exit 1; counter → TARGET_MET (exit 0). Cause: counter line 112 `.lower().startswith(...)`;
census requires exact capital-`R` string.

**D3 — tab after `##` accepted by census, rejected by counter (MEDIUM).** Heading
`##\tRegistry`: census → rows=8, `ok`, exit 0; counter → `closed_rows=0 closed_entries=0
open_cites=8`, exit 1. Cause: census line 609 char class `[ \t]` (and line 611 trims
`\t`), counter line 111 literal `[ ]` only — a tab is not whitespace to the counter, so
a valid census section is invisible to it.

**D4 — `##`-followed-by-tab fails to close the counter's section (MEDIUM).**
`## Registry` then `##\tOther` then rows: census → rows=8, exit 0 (the `##\tOther` is a
real `##` heading and closes the section; rows after it are *outside* — but these rows
are not S-shaped at `S[0-9]{3,}`… they are, so census still counts the 8 in the first
section, no E12 for the after-heading rows **only because they sit under the `## Registry`
section and are count rows; the section closure still applies to any S-row after
`##\tOther`**); counter → TARGET_MET (exit 0) — it keeps reading rows after the invisible
tabbed heading as registry rows. Tree: `## Registry` → `##\tOther` → S-rows: census
E12s the S-rows, counter accepts. This is D3's converse.

Observed case-I/J/K/L outputs (quoted exactly):

```
I: census validate exit=1 → file E12 S203..S210 row outside Registry section (×8); census rows=0; counter exit=0 → PRED-C1-r36-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
J: census validate exit=1 → same 8× E12; census rows=0; counter exit=0 → TARGET_MET
K: census validate exit=0 → file ok; census rows=8; counter exit=1 → closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED
L: census validate exit=0 → file ok; census rows=8; counter exit=0 → TARGET_MET
```

**Structural note (LOW)** — E12's row shape is `S[0-9]{3,}` (line 619); the counter's
`ROW_RE` is `S[0-9]+` (line 33). The frozen manifest only uses S203–S210, so this is
latent, not reachable by the frozen controls.

## 5. Residual risk / verdict

- The frozen predicate's "`## Registry` section" is not mechanically defined in the
  frozen text; the registration binds it to census E12. The counter's
  prefix/case-insensitive acceptance (D1/D2) makes **part of its accept set a superset
  of what the census accepts** — a tree the census rejects with E12 can score
  `TARGET_MET` on the repaired counter. The `c1-golden-r36` control and the live lane
  use an exact `## Registry` heading, so the frozen 25-control manifest does not expose
  D1/D2; they are a latent gate gap, not a manifest failure.
- `c1-row-moved-out` (rows under `## Leads (unopened)`) is correctly killed: census
  `E12 S206`, counter `closed_rows=7 … TARGET_MISSED`. `c1-no-registry-heading`
  (golden, no heading): census 8× E12, counter `closed_rows=0 … TARGET_MISSED`. The
  two fence controls behave.
- Case C shows the counter ignores a stray duplicate S-row above the section even when
  it is the *same id* it closes later — the row-unique clause only applies inside the
  section (`rows_for` runs over `registry_section` only, lines 119-125).
- Not an issue: live `corpus/SOURCES.md` validates clean under census E12
  (`file ok`, exit 0; only harmless W04 duplicates) and the counter reaches
  `TARGET_MET` on it.

Recommendation: tighten counter line 112 to exact `line.strip() == "## Registry"` (or
`trim(substr(...))=="Registry"` mirroring census line 611), and line 111 to
`^ {0,3}##[ \t]`; add a (non-frozen) self-test covering D1–D4 against the census
oracle. All four divergences are in the fence the repaired counter must implement, so
they are in scope for the row-in-registry clause.
