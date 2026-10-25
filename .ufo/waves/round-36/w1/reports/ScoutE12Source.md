# ScoutE12Source — E12 census rule, exact behavior

Seat: `L1Mado36.ScoutE12Source` (scout, mado round 36 wave 1). Source under review:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (fleet root, read-only; 806 lines).
All `:<n>` pointers below are into that file unless another path is named. Nothing in the
lane's production tree was touched; probes ran against `mktemp` fixtures in `/tmp` only.

Verdict: **recorded, evidence-backed** — every claim below is a quoted line or a quoted
probe output from this pass.

## 1. The exact E12 implementation

Definition (header contract): `:30` —
`E12 row-shaped source outside the ## Registry section`.

Emission lives in the single gawk pass `row_pass` (`:574-695`), inside the main record block:

- `:609-613` — a line matching `/^ {0,3}##[ \t]/` has its leading spaces stripped and sets
  the section flag: `in_registry=(trim(substr(line,3))=="Registry")` — i.e. the heading
  text must equal `Registry` exactly after trimming (case-sensitive, no trailing words).
- `:614` — a line matching `/^ {0,3}#[ \t]/` (single-`#` heading) sets `in_registry=0`.
- `:615-617` — any line not matching `/^ {0,3}\|/` is skipped; surviving lines are
  de-indented (`sub(/^ {0,3}/,"",line)`) and reparsed as `$0`.
- `:618-624` — the E12 site, verbatim:

  ```
  if (!in_registry) {
      if (mode=="validate" && $0 ~ /^\|[ \t]*S[0-9]{3,}[ \t]*\|/) {
          id=trim($2)
          printf "%s\tE12\t%s row outside Registry section\n",lane,id
      }
      next
  }
  ```

Consequences of that placement, all observed:

- E12 fires **only in `validate` mode** (`mode=="validate"` guard, `:619`). In `census`,
  `overdue` and `shared` the same row takes the bare `next` at `:623` and is invisible.
  Probe: on a file whose only S-row sits under `## Leads`,
  `census --file` printed `file\trows\t0` and `FLEET rows 0`, rc=0 — the stray row is
  silently uncounted, not an error.
- E12 triggers on **first-cell shape only**: `/^\|[ \t]*S[0-9]{3,}[ \t]*\|/` (`:619`)
  requires the first cell to be exactly an `S` + ≥3 digits id (optional blanks) terminated
  by `|`. A 2-digit id outside the Registry is invisible (probe: `| S9 | …` under
  `## Leads` → `ok`, rc=0). A malformed row still fires: probe `| S901 | short row |`
  under `## Leads` → `E12 S901 row outside Registry section`, rc=1 — the field-count
  check `NF!=13` (`:635`) is never reached because `:618` precedes `separator_row()`/`E01`.
- The `id` printed is `trim($2)` (`:620`), so the reported id is the cell text, not a
  regex capture.
- Any non-Registry location counts: before any heading (`in_registry` unset → falsy at
  `:618`), under `## Paths`/`## Leads` (`:611` flips on any `## ` line), or under an
  `### ` heading, which **never toggles the flag** — probe `### Registry` + S-row →
  `E12`, rc=1. `# Registry` (single `#`) does NOT open the section either (`:614` vs
  `:609`; not probed separately but the regexes are disjoint and `:609` requires `##`).
- `usedby_findings` (`:538-571`, the bash second pass that emits E11) reimplements the
  same section fence — `heading_re='^ {0,3}##[[:space:]]'` / `top_heading_re='^ {0,3}#[[:space:]]'`
  / `table_re='^ {0,3}\|'` at `:540-541`, `in_registry` toggling at `:544-551` — but emits
  no E12 of its own; it only reads cells[1]/[8]/[11] inside the Registry (`:551-560`).

## 2. The indentation rule the maintained parser accepts

- Stated rule (`:40-42`): "Maintained parser accepts 0–3 leading ASCII spaces before
  Markdown rows/headings; 4 or more spaces are indented code and ignored. Frozen manual
  examples assume column-zero input."
- Mechanism: literal-space regexes `/^ {0,3}##[ \t]/`, `/^ {0,3}#[ \t]/`, `/^ {0,3}\|/`
  (`:609`, `:614`, `:615`); mirrored in the bash pass at `:540-541`. After matching,
  `:610`/`:616` strip only ` {0,3}` (spaces), never tabs.
- **Tabs are not whitespace here.** Probe: `## Registry` + header + separator + S-row all
  indented by one `\t` → `D\tok`, rc=0 — the entire tab-indented table is invisible to
  every code E01–E12 and to the row counter. This is stricter than CommonMark (a tab is
  up-to-4 columns of indent) and stricter than "0–3 leading whitespace".
- **4+ spaces = invisible code, including headings.** Probe: `'    ## Registry'` followed
  by a column-0 S-row → `E12`, rc=1: the 4-space heading did not open a section. The
  selftest bakes the same exclusion in reverse (`:301-302` plants a 4-space `## Paths`
  plus an invalid-tier `S999` row inside a Registry fixture and asserts `rows 1`, rc=0 at
  `:308-312`).
- Exactly-`Registry` text: `## Registry notes` → E12 on following rows (probe I, rc=1);
  `## registry` lowercase → E12 (probe F, rc=1); `##Registry` no space → E12 (probe C,
  rc=1) — `:609` requires `[ \t]` after `##` and `:611` requires the trimmed remainder to
  equal `Registry`.

## 3. The E12 selftest fixtures

E12 has **no fixture under `scripts/fixtures/sources-census/`** — that tree carries only
`root/{a,b,c,z}-shokunin` + `shokunin.conf` + `injection-shokunin` (`:99`); the static
selftest block `:126-161` checks E01–E11 + W01–W03 but no E12. All E12 fixtures are
inline `mktemp` builds (`:164-167`):

1. `:270-285` — `outside-shokunin`: `## Registry` header + separator, then `## Paths`
   (`:278`), then `| S900 | … |` (`:279`). Asserts the exact line
   `outside-shokunin\tE12\tS900 row outside Registry section` via `checkline` (`:281-283`)
   and exit 1 via `checkx` (`:284-285`).
2. `:287-346` — indentation loop `for indent_width in 0 1 2 3`. The E12 legs are
   `indent-outside-N` (`:334-345`): `${indent}## Registry`, indented header+separator,
   `${indent}## Paths` (`:338`), then `${indent}| S94N | … outside Registry … |` (`:339`);
   asserts `indent-outside-N-shokunin\tE12\tS94N row outside Registry section` (`:341-343`)
   and rc=1 (`:344-345`). The sibling `indent-valid-N` legs (`:298-316`) assert the
   complementary rule: an indented (0–3 sp) Registry section *does* count and *does*
   validate clean, while an embedded 4-space code block is ignored.
3. Ran `bash scripts/sources-census.sh selftest` this pass: every E12 leg reported
   `killed` — `killed\tE12-outside-registry-mutant`, `killed\tE12-row-outside-registry-exit-1`,
   `killed\tindented-outside-{0,1,2,3}-E12`, `killed\tindented-outside-{0,1,2,3}-exit-1` —
   final line `selftest ok`, rc=0.

## 4. The exit-code contract

- Contract statement (`:16-18`): `0 clean or warnings · 1 E/overdue findings (or census
  missing) · 2 usage/env/missing registry · 3 selftest failure; W-codes and unlisted
  lanes never change status (validate missing registry returns 2).`
- Mechanism:
  - `findings=1` is set only when validate output contains `\tE[0-9]+\t` (`:739-741`);
    W-only lanes print but stay clean (`:742-745`).
  - Exit order at `:803-806`: census-with-missing → `exit 1` **first**; then
    `missing_error` (any non-census mode with a missing `corpus/SOURCES.md`, set at `:713`)
    → `exit 2`; then `findings` → `exit 1`; else `exit 0`. In census mode a missing
    registry therefore reports 1, not 2.
  - `die()` (`:48`) → 2 for usage/env errors, unknown lane (`:525`), unreadable conf
    (`:454-455`), gawk failure (`:717-719`, `797`).
  - selftest: missing fixture dir → 3 (`:100`), any `SURVIVED` leg → 3 (`:447`), clean →
    `selftest ok` + 0 (`:447`).
- E12 specifically: it is an `E` code, so a validate lane containing only E12 exits **1**
  (selftest `:284-285`, `:344-345`; probe A rc=1).

## 5. What a lane counter reproducing E12 must do (one paragraph)

To agree with the census a lane counter must track section state, not scan whole files:
open `in_registry` only on a line matching `/^ {0,3}##[ \t]/` whose trimmed remainder is
exactly `Registry` (`:609-611`), close it on the next `## ` heading of any name and on
any single-`#` heading (`:614`), never toggle it on `### ` or deeper, and treat 4+
leading spaces or a leading tab as invisible code (`:40-42`, `:615`; probes D/E). Inside
that section it counts row lines matching `/^ {0,3}\|/` minus header/separator rows
(`:591-599`, `:625`, `:630`); outside it, in validate semantics, it emits
`<lane>\tE12\t<id> row outside Registry section` for each row whose first cell is exactly
`S[0-9]{3,}` (`:618-623`) and drops all other outside rows silently (`:623`, probe G) —
and in every non-validate mode it drops even the S-shaped outside rows without any code
(`:619` mode guard; census probe printed `rows 0`, rc=0). The census is stricter than a
naive counter in four measured places: (a) section gating means a moved-but-otherwise-
identical row is both uncounted *and* an error — the live lane defect recorded in
`mado-shokunin/corpus/lessons/round-35.md:382-387`, where the r35 C1 counter's
`^ {0,3}\|\s*(S[0-9]+)\s*\|` whole-file scan (`count.py:118-124`, quoted in
`mado-shokunin/.ufo/waves/round-35/w2/reports/RevC1Tip.md:179-183`) printed `TARGET_MET`
on bytes the census fails with `E12 S206 …` rc=1 (`RevC1Tip.md:196-199`); (b) the heading
must be byte-exact `Registry` — `## registry`, `## Registry notes`, `##Registry`,
`### Registry` all leave the flag closed (probes B/C/F/I vs `:611`); (c) outside-row
detection is first-cell-exact `S[0-9]{3,}` — short ids, malformed but S-shaped rows, and
non-S rows outside are silently dropped, not E01'd (`:619`, probes G/H); (d) indentation
is literal ASCII spaces 0–3 only — a tab-indented table vanishes entirely (probe D),
which no `grep '^[[:space:]]*\|'` reimplementation reproduces because `[[:space:]]`
includes `\t`. A counter that skips any of those reproduces the r35 F2 gap.

## 6. What I ran

- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh selftest` → all E12/indent
  legs `killed`, `selftest ok`, rc=0 (§3).
- `mktemp` fixture probes A–J + a `census --file` run (§1, §2, §5); fixtures deleted
  (`rm -rf`). Outputs quoted in place.
- `grep`/`read` over `scripts/sources-census.sh`, `scripts/fixtures/sources-census/`,
  `mado-shokunin/corpus/lessons/round-35.md`, `…/w2/reports/RevC1Tip.md`,
  `…/w2/reports/RevCensus.md`, `…/round-35-verifier-spotcheck.md` for context.

## 7. Remaining unknowns / gaps

- Whether `quality/counters/` (this round's new data) is intended to *wrap* the census or
  *reimplement* it — this report gives the reproduction contract; the r35 lesson
  (`round-35.md:386-387`) already delegates the choice to round 36.
- A pathological file with `| S### |` rows *inside* Registry but before its header row is
  counted as data (`separator_row()` only exempts the `id` header and `---` rows,
  `:591-599`) — E12 does not apply in-section by construction (`:618` guard), so this is
  out of E12's scope but adjacent if a counter also reproduces row totals.
- Tooling: nothing installed; `bash`+`gawk` on PATH sufficed. No pacman transaction run
  (host-wide pause honored).
