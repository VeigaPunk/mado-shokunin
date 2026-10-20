# RevRubricV — rubric V gaming review (round 17, wave 1)

Seat: `MadoR17.RevRubricV` (leaf reviewer). Date 2026-10-20. Read-only; wrote
this report only. No commits, no git/jj mutation, no package-query or
transaction, no service/compositor/input/screenshot operation, no tool install
or update, no OMP transcript read (my item names none). All config-tree and
session reads were byte reads (`cat`, `grep`, `sha256sum`, `stat`).

## 1. What I measured

Declared rubric V: `SCORECARD.md:842-856` (C2 bullet), counter
`.ufo/waves/round-17/measure.py` (250 L, sha256
`7e37b6bc95614b4522f56db7e85bb51d58e8d87939fd5cf46d8e68612b4d858b`).
PROVINCE surfaces: `PROVINCE.md:5-11`. SOURCES registry contract:
`corpus/SOURCES.md:11`.

Executed, all read-only:

```text
$ python3 .ufo/waves/round-17/measure.py 27cd06f      # declared counting command
c1 {criteria:22, lesson_cited:14, score:6.3636}
c2 {count:2, score:3.3333; P1: 2 entries (legacy U2, U1); P2: 1 entry (legacy U7);
    P3..P6 uncovered; rejected: []; u_routes: 7}
c3 {tool_present:false, sha256:null}                  exit 0
$ git ls-files .ufo/waves/round-17/measure.py        # (empty: untracked)
$ git cat-file -e 0175f13:.ufo/waves/round-17/measure.py  → absent
$ git cat-file -e 27cd06f:.ufo/waves/round-17/measure.py  → absent
```

Independent re-derivation with my own `/tmp` stdlib script implementing the
declared paragraph verbatim (head = first 15 lines; `source:` S-tokens; SOURCES
row `status=mined`, `tier=A`, `used-by` exact path; legacy map U1/U2→P1,
U7→P2): **2/6 = 3.3333, identical**. The baseline claim is honest.

Pre-existing entries already satisfying the mined-A/used-by join at `27cd06f`
(so any of them can be given a `surface:` line without touching a source):

| Entry | joined rows |
|---|---|
| `corpus/knowledge/input-debugging-boundaries-r15.md` | S051, S052 |
| `corpus/knowledge/config-drift-r12.md` | S013, S014, S015 |
| `corpus/knowledge/waybar-observation-boundaries-r16.md` | S053, S054 |
| `corpus/knowledge/window-rule-effects-getprop.md` | S002, S016-S020 |
| `corpus/knowledge/hyprland-config-era-r12.md` | S021-S029 |
| `corpus/knowledge/wayland-protocol-boundaries-r13.md` | S005, S040-S043, S046 |
| `corpus/knowledge/output-colour-boundaries-r14.md` | S041, S047, S048, S050 |
| `corpus/knowledge/xdg-portal-routing-r12.md` | S031-S035, S037 |

Also verified: `PROVINCE.md` unchanged `27cd06f..HEAD`; no committed knowledge
entry has a line-start `surface:`; the two round-17 notes exist **uncommitted**
and are **not indexed** in `corpus/README.md` yet; their facet sections measure
(idle) 4602/4151/1016/1749 chars, 8 sha256, 11 `[UNK]` bullets and (terminal)
2647/2672/656/1015 chars, 10 sha256, 5 `[UNK]` bullets.

## 2. Verdict

The *level* is honest (2/6 reproduces two ways), but the rubric as implemented
is not yet sound as a scoring instrument: it can be moved by metadata-only
edits, one note can credit up to six provinces, and its facet gate is satisfied
by an empty skeleton. The declared paragraph and the counter also disagree on
the facet requirement, and the counter is not committed at either measured
revision. Adopt T1-T8 below before the after-measurement; none of them adds an
admissible item or changes the 2/6 baseline or the 4/6 target.

## 3. Findings — blocking

### V1. Metadata-only edits can inflate it: `surface:` is honored on pre-existing entries

`measure.py:175` enters the `surface:` path for **any** entry; there is no
`git cat-file -e 27cd06f:<path>` test, though the docstring calls it the "new
form" (`:22`) and SCORECARD:848 says "(new entries)".

Concrete path to the stated target with zero new source reading: the two
entries below already pass the citation join at baseline (table above). Adding
to each only `surface: P<n>`, the four headings, and one `[UNK]` line:

- `input-debugging-boundaries-r15.md` → `surface: P6` (+ 4 headings, `[UNK]`)
- `config-drift-r12.md` → `surface: P4` (+ 4 headings, `[UNK]`)

yields P1, P2, P6, P4 = **4/6**, the declared target, with two file edits and
no opened source. The headings are additive text, not research. `[INFERENCE]`
from the code path; the only uncertain input — the join — is executed evidence
above. This is the exact failure mode the round's own C1 (R16-V1, label without
its receipt) is meant to punish: a score moved by metadata.

Fix: T1.

### V2. One `surface:` line can credit up to six provinces

`measure.py:170`: `surfaces.update(re.findall(r'P[1-6]\b', line))` on any line
starting with `surface:`. Executed probes of the exact expression:

```text
'surface: P1 P2 P3 P4 P5 P6' -> ['P1','P2','P3','P4','P5','P6']
'surface: P1..P6 overview'   -> ['P1','P6']
'surface: P4, P5'            -> ['P4','P5']
'surface: not P4'            -> ['P4']
'surface: P6 (idle/lock)'    -> ['P6']
```

So one new note (four headings + one `[UNK]` + a join) can reach **6/6**, and a
negated/annotated token silently credits a province. There is no per-entry cap.
The shipped notes use the exact single token, so they are unaffected by the fix.

Fix: T2.

### V3. The facet gate is heading existence, not content — an empty skeleton passes

`section_body` returns `''` (not `None`) for a present-but-empty heading;
`missing` (`:176-178`) only fires on `None`; the only content test is the
substring `[UNK]` in the last section (`:186`). Therefore

```text
## Upstream contract
## Host declaration
## Safe observation
## Unexercised behavior
- [UNK]
```

plus a joined `source:` line and `surface: P4` scores P4 with no evidence at
all. `[INFERENCE]` from the code path. The gate also applies to any entry with
a `surface:` line, so it does not substitute for V1's baseline scoping.

Fix: T5.

## 4. Findings — high

### V4. The pre-registered rubric text is not the measured rubric

SCORECARD:845-849 declares only the source join + surface token. The four
required headings and the `[UNK]` requirement appear **only** in the
`MeasureBuild` and `NoteIdle`/`NoteTerminal` dispatch prompts (wave metadata,
not committed) and in `measure.py`'s docstring. A score that depends on them is
measured against criteria the repo's pre-registration does not carry. Conversely, if the
after-run is scored without them, V3 applies. Before the after-measurement,
restate the full tightened definition in SCORECARD and cite the counter's
sha256; that keeps the pre-registration honest even though it follows
`0175f13`.

### V5. No surface-relevance condition on cited rows

`mined_a` (`:116-120`) checks status/tier/used-by only. A `surface: P6` entry
can cite S053/S054 (Waybar) and pass; nothing ties `## Upstream contract` to
idle/lock, and `## Host declaration` is not required to name a P6 file. The
rubric therefore measures "declared itself sourced", not "sourced on this
plane". Fix: T4b plus the T5 host-path floor.

### V6. No note↔row content binding, and the ids are still provisional

The join is id-only. Today `idle-lock-route-r17.md` carries 7 `S0xx-pending`
placeholders for 7 URLs, and `terminal-route-r17.md` pre-assumes
`S056-pending..S060-pending` (5 rows + 2 rejected) while L1 reserves
`S056-S069` for both notes. A rename/renumber pass can bind an id to the wrong
row while `used-by` is edited to name the note, and the counter still passes —
the report would then cite the wrong evidence. A token-overlap test separates
the intended pairs (>=3 shared tokens) from cross pairs (<=1): verified for all
12 draft rows. Fix: T4d.

### V7. `u_routes` is not the U-route rubric it is reported as

`:151`, `:172-173`: `u_routes` is the count of **distinct `covers:` tokens**
across heads, accumulated **before** the source-join test, so it counts covers
tokens on unsourced entries too; the docstring at `:33` documents it as such.
One line `covers: U1 U2 U3 U4 U5 U6 U7` (or `covers: U7` repeated) keeps it at 7
even if the seven U entries are deleted or unsourced. The round-12 U rubric
required an entry with `source:` + `covers: U<n>` **and** the mined join
(`.ufo/evidence/round-12/after.txt:36-45`).
Reporting this field as "U stays 7/7" would be a label the field does not
carry — the same class as R16-V1. Fix: T7, or rename the field in the JSON
and never quote it as 7/7.

## 5. Findings — medium

### V8. The denominator is unbound, and PROVINCE has a seventh owned surface

`PROVINCES = [P1..P6]` is hardcoded (`:124`); `PROVINCE.md` is never read
(no reference in the file), so a future PROVINCE edit silently keeps 6.
PROVINCE:5-11 also owns "The omarchy skill ... documentation surface" — a
seventh item the rubric drops without a recorded reason; a closure reading
PROVINCE sees 6/7 surfaces counted. P1-P6 ↔ PROVINCE prose mapping is faithful
(`~/.config/hypr/`, waybar, walker, terminal configs, themes/wallpapers,
screen/idle), but it lives only in SCORECARD prose. Fix: T8.

### V9. Join laxness in three directions

- **Unknown ids are ignored.** `ok_sources` keeps only resolving ids. A
  `surface:` entry with unknown ids is rejected (with a reason), but the legacy
  path returns silently at `:208` (`if not sourced: continue`), so P1 or P2 can
  drop out of the count with no reason recorded anywhere in the JSON.
- **No `kind` filter.** A host-capture-only citation (kind `own-work`/`config`)
  satisfies "sourced documentary route"; the word "documentary" has no
  machine meaning here.
- **Rejected rows may ride along.** One mined row plus rejected rows passes;
  acceptable under QUALITY 5 if the rejected ones are labelled, but nothing
  checks that they are.

### V10. Broken input renders as a score, not as "could not evaluate"

`try_source` (`:74-79`) returns `None`; missing `corpus/SOURCES.md` then yields
`c2.count = 0` and missing `corpus/QUALITY.md` yields `c1.score = None`, both
with `exit 0` (`:250`). A malformed registry row (wrong cell count) is dropped
at `:108` without a diagnostic. A renamed file or a stray `|` would read as "no
coverage" rather than "counter could not evaluate" — the tripwire's 0/1/2
lesson (`SCORECARD` C3, context) applied to this counter. Fix: T6.

### V11. The counter is not committed at either revision it measures

`measure.py` is untracked at `HEAD`, absent at `27cd06f` and `0175f13`. The
before/after numbers therefore depend on working-tree bytes with no revision
binding; a later edit to the script changes both sides invisibly. Pin the
sha256 in the report **and** land the script in the measured content commit
(both runs made with identical bytes); if it must change, re-run both sides and
record old→new digests.

## 6. Findings — low / adjacent

- **V12. Facet vocabulary divergence.** Existing sourced notes use
  `## Unexercised rendering` / `## Unexercised delivery` / `## Unexercised
  feature behavior` / `## Limits` / `## Unknowns`. The fixed
  `## Unexercised behavior` string rejects a future note written in the
  established style. Acceptable as a round-local template (both briefs mandate
  it) but record it as such; do not grow a second convention silently.
- **V13. Draft-row integration hazards (they break C2's own harm watch).**
  (a) The idle draft repeats one `S0xx-pending` across 7 rows and the terminal
  draft pre-assumes `S056-S060`: a naive single-id substitution collapses six
  sources into one. `sources-census.sh` E03/E02 would catch that (`validate`
  exits 1) but only if run after integration — `measure.py` would not.
  (b) The terminal rows give S059/S060 `kind: config`, which is outside the
  census vocabulary (`spec|docs|paper|code|tool|dataset|talk|book|community|
  own-work`, `sources-census.sh:655`): E05 → `validate` exit 1, i.e. the stated
  harm-watch census goes red on integration as drafted. L1 must re-kind them
  (e.g. `code`/`own-work`) and re-run the census.
- **V14. "Admitted" is undefined; the index requirement is absent.** The rubric
  says "admitted entry" but nothing operationalizes admission, and credit does
  not require the `corpus/README.md` row. Both new notes are currently
  unindexed, so a commit without the FrontierDraft rows would red the
  navigation counter. Require exactly one README index row for credit.
- **V15. `S\d{3}` truncates longer ids.** `S9999` → `S999`; current reserves are
  three-digit, so latent only.

## 7. Is the legacy map justified?

Row by row, yes — as *inherited* credit with three amendments:

- **U1→P1** (`window-rule-effects-getprop.md`): the entry's subject is window
  rules declared in the Hyprland config tree. Justified, with the caveat that
  its strongest content is live `getprop` sampling, which is outside rubric V's
  documentary scope; those samples must not be cited as rubric-V evidence.
- **U2→P1** (`hyprland-config-era-r12.md`): the config language itself.
  Justified directly.
- **U7→P2** (`waybar-observation-boundaries-r16.md`): bar module text.
  Justified; this entry is the shape both round-17 notes copy.

Nothing else maps, correctly: U3 (portals), U4 (protocols), U5 (output
colour), U6 (input) are not PROVINCE config planes. Two cautions: U5 is the
tempting wrong mapping to P5 (themes/wallpapers) — say explicitly it is *not*
mapped; and because the map keys on the `covers:` token, a future re-split of
U1/U2/U7 (or a second entry claiming the same U) can move the credit. Pin the
map to `(entry path, U value)` triples (T3), and label the result: baseline
2/6 is **2 inherited + 0 new-sourced**; the round's move is +2 new, not "4
surfaces newly sourced". Also note P1/P2 are a structural floor: they can never
lose coverage while those three entries exist.

## 8. What a closure re-measures

At integration commit `R`, independently of L1's narrative:

1. `git show R:.ufo/waves/round-17/measure.py | sha256sum` equals the pin in the
   report and in both runs; note the provenance gap that it was absent at
   `27cd06f`/`0175f13`.
2. Run the counter at `27cd06f` and `R`: expect c1 14/22→15/23, c2 2/6→4/6,
   c3 absent→present+sha, `rejected: []`.
3. Re-derive the 4 provinces with plain `git show`/`grep` (no counter): each
   covering entry's head, join, surface token; confirm no `surface:` on a path
   that exists at `27cd06f`; confirm at most one surface per entry.
4. Hand-check both notes: head lines 1-6, four headings, `[UNK]` items, and that
   `## Host declaration` names the P6/P4 files with sha256 matching the bytes
   read this round (`hypridle.conf e7d3b8dd…`, `hyprlock.conf b8d173dc…`,
   `xdg-terminals.list d035da57…`, `alacritty.toml 695301c8…`).
5. Re-open every cited row: tag-pinned raw digests byte-compared (curl), wiki
   pages checked by verbatim anchor text (digest equality not available); every
   quote <=25 words and present; `used-by` names the entry; ids unique (census
   E03); id↔source token overlap passes; no row outside `## Registry`.
6. `sources-census.sh validate --root … mado` exit 0 *after* integration (see
   V13: kind/id fixes are required).
7. Harm watch: navigation counter complete with the two new rows indexed
   exactly once; the true U-route loop from round 12 still 7/7; hermetic
   selftest 372/372; classifier 52/52.
8. `git diff 27cd06f..R -- PROVINCE.md` empty, and the counter's P1-P6 still
   match PROVINCE's six planes (omarchy documentation exclusion recorded).
9. Content honesty: no idle-interval/lock/suspend/DPMS/listener-firing claim,
   no launched-terminal claim, host binary versions `[UNK]`, no command run.
10. Label discipline: the report says "4/6 rubric-V-covered (2 inherited, 2 new
    sourced routes)", never "4/6 surfaces covered" or "idle/lock verified".

## 9. Exact tightening L1 can adopt now (narrowing only)

None of T1-T8 admits a new item; all either remove a credit path or bind an
existing one. Effect on this round, checked against the artifacts: baseline
stays **2/6** (no baseline entry declares `surface:`; the three legacy pins
match today's map; T5 only gates `surface:` entries), and both shipped notes
still pass (exact surface lines, all four headings, facet counts 22/8/4/11 and
8/10/3/5, `[UNK]` 11/5). Target stays 4/6.

**T1 — baseline-scope the `surface:` path.** In `measure.py`, after `notes`:

```python
BASE_REV = '27cd06f'          # the declared baseline; round-local constant
base_notes = set(git('ls-tree', '-r', '--name-only', BASE_REV,
                     '--', 'corpus/knowledge').splitlines())
...
if surfaces:
    if path in base_notes:
        rejected.append({'path': path, 'declared': sorted(surfaces),
                         'reason': f'entry exists at baseline {BASE_REV}: only '
                                   'the fixed legacy map may credit it'})
        continue
```

**T2 — one exact surface token per entry.**

```python
surf_lines = [l.strip() for l in head if l.startswith('surface:')]
surfaces = set()
if surf_lines:
    if len(surf_lines) != 1 or not re.fullmatch(r'surface: P[1-6]', surf_lines[0]):
        rejected.append({'path': path, 'declared': surf_lines,
                         'reason': 'surface: must be exactly one line "surface: P<n>"'})
        continue
    surfaces = {surf_lines[0].split()[1]}
```

**T3 — path-pin the legacy map.** Replace `LEGACY_MAP` (`:125`) with:

```python
LEGACY_PINS = {
    ('corpus/knowledge/window-rule-effects-getprop.md', 'U1'): 'P1',
    ('corpus/knowledge/hyprland-config-era-r12.md',     'U2'): 'P1',
    ('corpus/knowledge/waybar-observation-boundaries-r16.md', 'U7'): 'P2',
}
```

and use `LEGACY_PINS.get((path, u))` at `:212`. Same three rows, no widening.

**T4 — harden the join.**

```python
SURF_TOKENS = {
 'P1': r'hypr|hyprland|hyprlang',  'P2': r'waybar',  'P3': r'walker',
 'P4': r'alacritty|foot|kitty|ghostty|xdg-terminal|terminal',
 'P5': r'theme|wallpaper|style',
 'P6': r'hypridle|hyprlock|idle|lock',
}
UPSTREAM_KINDS = {'docs', 'spec', 'code', 'book', 'paper'}
def row_text(row): return (row[2] + ' ' + row[5] + ' ' + row[6]).lower()
def tokens(s): return {t for t in re.split(r'[^a-z0-9.]+', s.lower()) if len(t) >= 4}
```

(a) every S-token in the head's `source:` line must resolve, else reject with
the unknown ids listed; (b) require `any(re.search(SURF_TOKENS[p], row_text(r))
for r in qualifying_rows)`; (c) require at least one qualifying row whose kind
is in `UPSTREAM_KINDS`; (d) require for each qualifying row >=2 shared tokens
between `tokens(row[2])` and `tokens(source_line)` (measured: intended pairs
3-8, cross pairs 0-1); (e) optional but recommended — require at least one
qualifying row opened `2026-10-20`, closing the "rename the old note" variant.

**T5 — facet content floors** (all validated against the two notes):

| Section | Requirement | idle | terminal |
|---|---|---|---|
| `## Upstream contract` | >=2 bullet/table lines matching `(\[[A-Z]{2,3}:\d)|(:\d+)|(S\d{3})` | 22 | 8 |
| `## Host declaration` | >=1 64-hex sha256 **and** >=1 surface path token (P6 `hypridle.conf|hyprlock.conf`; P4 `xdg-terminals.list|alacritty`) | 8, 6+6 | 10, 7+8 |
| `## Safe observation` | >=2 bullet/table lines | 4 | 3 |
| `## Unexercised behavior` | >=2 bullet/table lines containing `[UNK]` | 11 | 5 |

**T6 — evaluate-or-exit-2.** Print `evaluated`, `missing_inputs`,
`unparsed_rows`; exit 2 when `corpus/SOURCES.md` or the `corpus/knowledge` tree
is absent at REV, or a Registry row fails the 13-cell shape. Keep exit 0 for a
low count.

**T7 — true U harm watch.** Accumulate per U: `u_ok[u]` when the entry has
`covers: U<n>` **and** `sourced` (the round-12 rule); report
`u_covered_count`/7 next to (or instead of) `u_routes`. Do not quote
`u_routes` as "7/7".

**T8 — bind the denominator.** Read `PROVINCE.md` at REV, require the six
surface phrases, print `province_sha256`, and record in SCORECARD that the
omarchy documentation surface is excluded from rubric V because it is a
read-only documentation surface, not a host config plane.

Then: land `measure.py` in the measured commit, pin its sha256, and re-run both
revisions with the amended bytes.

## 10. Residual risk after tightening

Even fully tightened, rubric V measures **declared, joined sourcing** — that an
entry with the right shape cites rows that are mined, relevant, and bound to
it. It cannot tell whether the entry's interpretation of those sources is
correct: a plausible, relevant, freshly-opened row cited for a wrong claim
passes. The counter is an index-quality measure, not a knowledge-depth or
truth measure; the closure's source re-opening (item 5) is the only defence,
and it is manual. Second residual: the facet floors are structural minima; a
note can meet them with correct-looking prose and still be shallow. Third: the
legacy map keeps 2/6 as a floor and lets the same three entries count in both
the U and V rubrics; that is acceptable only while the report labels them
inherited.

## 11. Verification gaps

- V1 and V3 are demonstrated from the code path (`[INFERENCE]`); I did not
  execute a mutated fixture against `measure.py`, because the lane contract
  limits seats to running their own new stdlib scripts on `/tmp` inputs, and a
  copy of L1's counter under a rewritten `REPO` would not be L1's artifact.
  The executed evidence (join table, regex probes) covers every input except
  the added lines themselves.
- I did not re-fetch the pending sources (`S0xx-pending` are unregistered);
  digest/anchor verification belongs to the scouts and to closure item 5.
- I did not read any OMP transcript: no item names one for this seat.
- Wiki pages are dynamic; only anchor-text checks, not digest equality, can be
  required for them.
