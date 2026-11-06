# R89MCritic — falsification of the round-89 declaration (pre-freeze)

Seat: critic, wave w1 (leaf; no dispatch, no peer messages, no git/jj mutation). Lane `mado-shokunin`.
Target: `.ufo/waves/round-89/claims-declaration-r89.md` as drafted (no `## Freeze` yet). Nothing below
touches the candidate's style; every finding is about axes, controls, separability, universal wording,
or sourced ground. **Every number I print is a DRAFT run under the draft-scoring rule** — in-process
`score()`/`evaluate()` over the draft case files, the two counters' `--selftest`, and the candidate's
`--selftest`. No receipt under `receipts/` was written; no measurement is claimed.

Scratch: `S=/fast/scratch/hyaku/mado-r89/R89MCritic` (deleted on exit; see §8).

## Verdict table

| # | Question | Verdict |
|---|---|---|
| F1 | C1 axis = coverage | **STANDS** as capability acquisition; the `frontier → core` phrase **FALLS** |
| F2 | C2 axis = operability | **FALLS** — instrument depth (quality), not operability |
| F3 | axis-posture sentence ("tie, met by C1 and C2") | **FALLS** after F2 |
| F4 | C2 controls / three named forgeries | **STANDS** (all three blocked) + **WEAKENED** on label provenance |
| F5 | C1 predicate concreteness ("correct = N") | **FALLS** (§9: one concrete value) |
| F6 | C1 "command that would show it unmoved" | **FALLS** (prints no count) |
| F7 | "the two criteria fields the round-88 tool refused" | **FALLS** (universal over a surface it did not enumerate) |
| F8 | causal separability; "C2 measured at the freeze revision" | **STANDS** + one freeze-sequencing condition |
| F9 | universal clauses / post-hoc narrowing | 4 FALLS, 3 WEAKENED, 6 STAND (§5 table) |
| F10 | sourced claim on a SOURCES row opened this round | **FALLS** |
| F11 | freeze-readiness gaps (commands, harm watch, limits, provenance) | **FALLS** as drafted |

## 1. Axis naming (round prompt §9, lines 547-569)

### F1 — C1 is coverage: STANDS (as a capability acquisition); "frontier → core" FALLS

*For coverage:* AXES.md defines coverage as "the fraction of the domain's real surfaces the skill
governs (repo paths, tools, edge classes)" and §9 asks a coverage claim to name "the surface it moves
(frontier → core, **a new tool, operation or edge class**)". C1 adds a new operation class to
`tools/mado-mako.py` — POSIX ERE matching plus upstream's `parse_criteria` tokenizer — where round 88
refused the field outright. Rounds 87 and 88 both declared the same kind of move as
"coverage (capability)" and the SCORECARD carries them as capability rows.

*Against:* the moved surface is the lane's own model, not the domain; the domain surface (`mako`
`summary~`/`body~`) was already known and named in round 88's declaration, and the lane's **scored**
coverage sub-axis is "admitted-note reachability" (`SCORECARD.md:44-45`), which C1 does not move
(the draft declares no knowledge note; `R89MScribeEntry.md` §Draft 1 drafts
`corpus/knowledge/mako-regex-criteria-r89.md`, but as a seat draft it is not yet a landed entry and the
declaration does not name it). Worse, `PROVINCE.md` has **no frontier table**:
`grep -n -i frontier PROVINCE.md` → no match (rc 1). "frontier → core" is vocabulary this repo cannot
resolve.

Verdict a non-author closure reaches: coverage **holds** only when the claim is typed as a *capability
acquisition* and the surface is named as an edge class; the "frontier → core" gloss is struck, and the
declaration must say plainly that the scored coverage sub-axis does not move.

Text to change (C1, first sentence):

> ~~Surface moved (frontier → core): the two criteria fields the round-88 tool refused — `summary~` and
> `body~` — become modelled, matched with libc …~~

```text
Claim type: capability acquisition (AXES.md §Capabilities; the round-87/88 precedent). Surface moved:
mako's `summary~` and `body~` criteria, which round 88's named limit refused, are now modelled and
matched with libc `regcomp(REG_EXTENDED | REG_NOSUB)` + `regexec` through ctypes in the C locale —
a new operation class (regex matching plus upstream's `parse_criteria` tokenizer). This round lands one
capability row; the lane's scored coverage sub-axis (admitted-note reachability) does not move, and
PROVINCE.md has no frontier row to promote (`grep -n -i frontier PROVINCE.md` → no match). The
capability row names the field class, not "the host's five `summary~` sections": the case set enumerates
one of the five (r01-host-setup-wifi), so only that one is claimed as resolved.
```

### F2 — C2 is not operability: FALLS (instrument depth = quality work)

*For operability:* AXES.md's operability is "runnable artifacts: checklists that are executable,
commands that exist, scripts that run" and "a checklist item can be run and produces the stated
outcome". The supplementary cases are runnable, the counter runs, exit 0/1/2 is mapped.

*Against (decisive):* the declaration itself says "The tool itself is not changed by C2" and pins
`tool_sha256 = c374d715…92237` = the round-88 tool (verified:
`git show af998dcc:tools/mado-mako.py | sha256sum` → `c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237`).
No runnable artifact changes; no command appears; the lane's scored operability sub-axis (gate selftest
fraction, `SCORECARD.md:45`) does not move. §9's sentence names this exact pattern — "Re-scoring a rule
the lane already holds on new inputs … is quality work, never coverage or depth" — and what C2 raises is
the *mutation adequacy* of the lane's own regression evidence. That is the instrument's depth, i.e. the
quality trend (AXES: quality ↔ depth + freshness + operability).

Verdict a non-author closure reaches: C2 is admissible **only** relabelled; kept as "operability" it is
rejected as a non-axis move and the round is left with one claim (C1).

Text to change (C2 heading and lead):

```text
## C2 — quality (depth of the regression instrument): the round-89 supplementary cases kill round 88's
routed survivors

Surface moved: none in the domain and none in the tool (`tools/mado-mako.py` is byte-identical at this
claim's revision, sha256 c374d715…92237). What moves is the discriminating power of the lane's own
mutation evidence for the round-88 rule set: two supplementary case sets scored through the frozen
round-88 machinery, so that **seven of the eight** round-88 residual survivors stop surviving
(RM6C2 remains alive; see the crash-only paragraph). Under AXES.md this is instrument depth: no new
runnable artifact, no axis-score move.
```

### F3 — the axis-posture sentence: FALLS after F2

Text to change (top of the declaration):

> ~~Every owned axis sits at 10; the lowest-axis obligation is a tie, met by C1 (coverage) and C2
> (operability).~~

```text
Every owned axis sits at 10 (SCORECARD.md axis table, round-86 re-derivation: navigation 107/107,
calibration 86/86, operability selftest 12/12, ledger 158/158). The lowest-axis obligation is a tie at
10 and is met by C1 (coverage). C2 is instrument depth, not operability, and claims no axis-score move.
```

The stagnation nudge sentence ("not claimed (a capability entered at round 88)") **STANDS**:
`SCORECARD.md` round-88 capability row has first-working round 88 and the window is N=3, so the nudge is
not triggered at round 89.

## 2. Do-nothing and forgery controls

### F4 — C2's three forgeries are blocked; three labels are the fixture-keyed shape: STANDS + WEAKENED

Blocked, with the exact mechanism:

1. **S expectations copied from the mutant** → conjunct (a) fails: the measured tool would no longer be
   correct on that case (`c2-r89-survivor-kills.py:78` `predicate`; `:117-119` runs the tool over
   `base+supp`).
2. **A set that only crashes mutants** → `F.semantic_kill` (`c1-r88-mako-fields.py:205-208`) requires a
   *well-formed* mutant verdict; a crash prefix is not a kill. Only RM6C2 is declared and excluded
   (`c2-r89-survivor-kills.py:51`, `:126-127`).
3. **A set already present in B** → `killed_base` is computed over the B indices (`:123`, `:127`) and the
   predicate requires `killed_base < counted` (`:78`); duplicates push it to 7 and fail (c).

WEAKENED — label provenance, which the draft never states. Of the 8 supplementary cases, **5 rest on a
cited source** — the four `s1-*` (criteria.c `match_criteria`/`apply_criteria_field`; `s1-include-in-
criteria`'s refusal is the tool's stance derived from `mako.5` L45) and `s2-double-slash`
(config.c:505-521) — and **3 are tool-stance labels copied from the measured tool**:
`s2-trailing-slash` (`"pin": "tool stance (r88 draft revision 4)"`), `s2-root-is-a-file`
(`"pin": "tool stance: a --read-root may name a file"`) and `s2-cycle-second-lexical-path`
(`"pin": "tool stance: an include whose resolved path is already being read is a cycle"`). Conjunct (a)
is therefore vacuous over those three (they cannot detect a tool regression); the 7 counted kills are
unaffected in value — 5 rest on sourced labels and 2 (`RM3C2`, `RM5C2`) on tool-stance labels, with
RM6C2's kill uncounted. This is criterion 36's fixture-keyed shortcut shape and criterion 121's label
duty (`corpus/QUALITY.md:324`, `:843`).

Add, immediately after the predicate:

```text
Label provenance of S, stated before data: 5 of the 8 supplementary labels rest on a cited source (the
four s1-*, and s2-double-slash via config.c:505-521); s2-trailing-slash, s2-root-is-a-file and
s2-cycle-second-lexical-path are tool-stance labels copied from the round-88 tool, so conjunct (a) over
those three is a regression pin, not independent ground truth; the 7 counted kills are unchanged in
value (5 on sourced labels, 2 on tool-stance labels, RM6C2 uncounted). The three cheap forgeries are
blocked: mutant-copied expectations fail (a); a crash-only kill is not a kill (so RM6C2 is declared and
excluded); an S case already in B raises do_nothing_B_only_killed to 7 and fails (c).
```

DRAFT evidence (`evaluate()` in-process, round-88 tool at `af998dc`): 62+26 B with 4+4 S → **96/96
correct, 7 killed, RM6C2 `crashed-not-killed` on `s2-cycle-second-lexical-path`, B-only 0**. The
counter's own B drops c53 (`:50`), and c53 passes at the round-88 tool, so the measured value is 95/95.

### F5 — C1's "correct = N" is not a concrete value: FALLS

§9: "Declare each after-state as one concrete value that the closure can re-derive with one command";
"Never narrow a target after landing." The draft declares N symbolically and separately says the case
set includes "the blind seat cases appended after review" — so N is a moving target and a post-freeze
append would silently re-define the target (a widening, the mirror of the forbidden narrowing). The
counter fixes only a *range*, `N_MIN, N_MAX = 70, 110` (`c1-r89-mako-regex.py:50`), and the schema.

Text to change:

```text
Predicate PRED-C1-r89-v1: TARGET_MET iff correct = 91/91 on `mako-cases-r89.json` at the freeze-pinned
sha256, killed = M = 32/32, carried = 61/61 (61 of the round-88 file's 62 cases, c53-summary-tilde-
refused superseded and absent), and each control scores strictly below 91: naive-toplevel 22,
globals-include 23, base-tool 67, python-re 81 (DRAFT; the receipt re-prints all four).
The blind seat cases are appended BEFORE the freeze, the declaration re-declares N and the case sha256,
and the draft score is re-run; a post-freeze append is a new case set with a new predicate, never a
relabel of this one.
```

DRAFT evidence: `score(candidate, base, 91 cases, 32 mutants)` → **TARGET_MET n=91 correct=91 killed=32/32
controls naive=22 globals=23 base=67 python_re=81** — the draft numbers in the disclosure reproduce
exactly, so the predicate is reachable as written; only its wording is wrong.

### F6 — C1's "command that would show it unmoved": FALLS

`git show <rev>:tools/mado-mako.py | grep -n MODELLED_FIELDS -A1` prints 98-99 (base) or 110-111
(candidate) with the field names split over two source lines. It does not print a count, so it is not
"one concrete value" and cannot show `10 → 12` without the reader counting names by eye.

Replacement (verified: prints `10` at `af998dcc`, `12` at the candidate bytes):

```sh
git show <rev>:tools/mado-mako.py | python3 -c "import sys,re; t=sys.stdin.read(); m=re.search(r'MODELLED_FIELDS = \((.*?)\)', t, re.S); print(len(re.findall(r'\"[^\"]+\"', m.group(1))))"
```

### F7 — "the two criteria fields the round-88 tool refused": FALLS

The round-88 tool refuses **more than two** criteria fields. `tools/mado-mako.py:98-99` lists 10 of
mako's criteria fields; `:338-339` refuses every other key. Criterion 68 (`corpus/QUALITY.md:383`):
"'the N forms' is never stated as a universal over a surface it did not enumerate end to end."
Reproduced (DRAFT, same fixture on both revisions):

```text
config: anchor=top-right / [group-index=1] / anchor=bottom-center
base  tools/mado-mako.py      -> MADO_MAKO: resolved=37 refusals=1
cand  mado-mako.c1.py         -> MADO_MAKO: resolved=37 refusals=1
```

Text to change:

```text
… the two criteria fields this round adds — `summary~` and `body~` — become modelled (the round-88 tool
also refuses `group-index` and `grouped`, and still does after this round: a `[group-index=1]` section
yields refusals=1 on both revisions; named limit).
```

and, in the target line, `fields 12/12` → `fields 12/12 of the tool's MODELLED_FIELDS list (mako's
group-index/grouped remain refused)`.

## 3. Causal separability, and whether "C2 measured at the freeze revision" is honest

### F8 — separability STANDS; one freeze-sequencing condition must be added

C1 alone: `c1-r89-mako-regex.py` reads only its own cases, mutants, the round-88 case file and the base
tool (`:166-186`); no C2 file is opened. DRAFT TARGET_MET, so C1 does not need C2 to have landed.
C2 alone: measured at a revision whose tool is the round-88 tool (`c374d715…92237` = base, verified);
C1's landing is irrelevant. DRAFT at base: 96/96 (c53 in) → 95/95 with the counter's B, 7 killed,
B-only 0. So neither needs the other's change.

Honesty: the sentence is honest **iff the freeze commit leaves `tools/mado-mako.py` byte-equal to base**.
The counter reads the tool, the survivor list and both S files at `--rev` (`:166-190`), so the freeze
must contain the S files *and* the round-88 tool. If C1 lands before the freeze, the receipt's
`tool_sha256` will not be `c374d715…92237` and the declared sentence becomes false — even though the
target still passes (DRAFT at the C1 candidate: 95/96 with c53 present, i.e. 95/95 with the counter's B,
7 killed, B-only 0).

Text to change:

```text
C2 is measured at the freeze revision, and the receipt must print tool_sha256=c374d715…92237; the freeze
commit may not change tools/mado-mako.py (the C1 candidate stays under .ufo/waves/round-89/build/ until
after the freeze).
```

and replace the harm-check sentence, which is currently inside the claim but outside the predicate:

```text
C2's eight anchors occur exactly once in the C1 candidate too (verified: 8/8 count 1), so the identical
command re-runs at the C1 landing revision — a harm watch, not a claim element (DRAFT there: 95/95,
killed 7/7, do_nothing_B_only_killed 0).
```

## 4. Universal clauses and post-hoc narrowing

### F9 — clause-by-clause

| Declaration phrase | Verdict | Action |
|---|---|---|
| "the two criteria fields the round-88 tool refused" | **FALLS** | F7 reword |
| C2 lead "so that the **eight** … survivors … stop surviving" | **FALLS** | seven of eight; RM6C2 stays alive (crash-only), scored and printed |
| "correct count equals N" / "correct = N" | **FALLS** | F5: literal 91 |
| "fields 12/12" | **FALLS** | F7: 12/12 of MODELLED_FIELDS, group-index/grouped named |
| "the 61 carried round-88 cases are present unchanged" | **WEAKENED** | say "61 of 62; c53 superseded and absent; r01/r02 now cover summary~ matching; the counter raises SetupError if c53's id reappears" |
| "mako never calls `setlocale` … matched … in the C locale" | **WEAKENED** | tree half verified (tarball `grep -rn setlocale mako-1.11.0/` → no match, rc 1); the C-locale conclusion rests on setlocale(3)'s startup default ("On startup of the main program, the portable \"C\" locale is selected as default" — the drafted S497) and on the tool's own pin. Reword: "the v1.11.0 tree contains no setlocale call, and the tool calls `locale.setlocale(LC_ALL, "C")` before its first regcomp (`mado-mako.c1.py:124`), so its matcher does not depend on the caller's locale — a bare Python process on this host reports `LC_CTYPE=en_US.UTF-8`, which is why the pin is load-bearing and why M24 is separable" (verified both) |
| "a pattern `regcomp` rejects is refused" | **WEAKENED** | the unit is the section: apply_criteria_field returns false → parse_criteria false (criteria.c:332-351 via :162-262), so the whole criteria definition is refused. Reword to "a criteria section whose summary~/body~ value regcomp rejects is refused" |
| "the four controls … each score strictly below N" | **STANDS** | four enumerated values (F5 prints them) |
| "all M mutants are killed" | **STANDS** | M=32 literal (`c1-r89:51`); DRAFT 32/32 |
| "the eight round-88 residual survivors (… RM2C2 excluded …)" | **STANDS** | R88MResidMut §3/§4 list exactly 4 C1 + 4 C2 survivors; RM2C2 is the named-limit survivor; the 8 r89 mutant definitions match the seat's descriptions 1:1 and each anchor occurs once (verified 8/8) |
| "C2's eight anchors occur exactly once in the C1 candidate too" | **STANDS** | verified 8/8 count 1 |
| "no terminating input separates RM6C2 with a well-formed result" | **STANDS** | add the entailment so the closure need not re-derive it (below) |
| "Before: … 10/12" (C1) | **STANDS** | `MODELLED_FIELDS` at base has 10 entries, none of them summary~/body~ |

RM6C2 entailment (append to the crash-only paragraph):

```text
The mutant's test (`target in self.stack`) is entailed by the tool's (`realpath(target) in self.stack`)
whenever target is already normalised, because the stack holds only realpaths (`tools/mado-mako.py:458-464`,
`:521`); so the mutant never invents a cycle, only misses one, and a missed cycle always re-enters the
ancestor whose include chain caused it and recurses. The tool has no depth cap and no RecursionError
handler, so every separating input terminates by RecursionError (exit 1, printed as the S case's crash).
```

[INFERENCE] One uncovered edge the declaration never names, worth a limit line rather than a case: a NUL
byte inside a criteria line (mako's C-string path truncates at the NUL; the candidate refuses the whole
section, `mado-mako.c1.py:139-140`). No case covers it, so it is neither a miss nor a silence.

## 5. Sourced claim (§2b.4)

### F10 — no claim rests on a SOURCES row opened this round: FALLS

Facts:

* `grep -nE 'regcomp|regex\.h|REG_EXTENDED|regex\(7\)|regex\(3\)|setlocale' corpus/SOURCES.md` → no
  output (rc 1). No row covers the surface C1 moves.
* S494 (the natural row) anchors `criteria.c:75-76,80-81,100-101,105-106,110-111,122-123` (strcmp
  fields), `:85-86,90-91`, `:267-290`, `types.c:19-28`, `config.c:621,649,592-593`,
  `:505-521,545-547,780-781`, `criteria.c:542-548` — **not** `:46-59` (`match_regex_criteria`),
  `:162-262` (`parse_criteria`) or `:332-351` (the two `regcomp` calls). Its `used-by` is
  `corpus/knowledge/mako-fields-containment-r88.md,corpus/lessons/round-88.md`, and its `opened` date is
  `2026-11-06` — round 88's day, i.e. it was opened by **round 88**, not this round. The same-day date
  cannot be read as "opened this round".
* The draft declaration records no SOURCES delta at all, and no census. I ran the census read-only:
  `./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok`,
  exit 0, 430 rows, 55 `W04` (the standing warnings).

Which rows C1's entry must cite — the material was opened this round by the wave's own seats, the rows are
already drafted, and they are not in the registry. `R89MScoutSources.md` §2 drafts seven rows, S496–S502:
S496 regex(3) on this host, S497 setlocale(3), S498 regex(7), S499 POSIX ch9, S500 POSIX regcomp(),
S501 the mako tag tree (tokenizer + regex flags + the absent setlocale), S502 the host glibc
`<regex.h>`. `R89MScribeEntry.md` §Draft 1 has already written
`corpus/knowledge/mako-regex-criteria-r89.md` whose `source:` line reads `S494 …, S496 (PLACEHOLDER —
regex(3)/regcomp(3) on this host …), S497 (PLACEHOLDER — regex(7) on this host …)`; a closure reads a
PLACEHOLDER token as no row at all, and §2b.4 is not satisfied by a draft in a seat report. Smallest safe
correction:

```text
Create the rows the entry's source line names — at minimum S496 (regex(3): REG_EXTENDED at decompressed
text lines 77-84, REG_NOSUB 92-100, REG_NOMATCH 246-249; container sha256 f79f05fd…, and note
`regcomp.3.gz` is a 37-byte `.so man3/regex.3` stub, sha256 bdeb1289…, so the anchor must cite regex(3))
and S497 (setlocale(3): "On startup of the main program, the portable \"C\" locale is selected as
default", decompressed lines 135-137) — both with the scout's Gate quotes and access date 2026-11-06;
replace the entry's PLACEHOLDER tokens with the real ids; update S494's `used-by` to add the round-89
entry (logged old→new in `corpus/lessons/round-89.md` `## Gate`); then record the census before (430 rows,
exit 0) and after (432 if only S496/S497 land, 437 if all of S496–S502 do).
```

If the L1 instead rests §2b.4 on S494 alone, the declaration must argue why a row opened by round 88
counts as "opened this round" — the contract's plain reading says it does not.

## 6. Freeze-readiness gaps the closure will read first

### F11 — FALLS as drafted; all four are pre-freeze obligations, not claim changes

1. **No counting command is printed** (C1/C2 name the counter and the predicate only). QUALITY 118
   (`corpus/QUALITY.md:807-812`): "the declaration must print the exact argv the receipt will run, flags
   included". Required arguments — C1: `--repo --rev --base-rev --cases --expect-cases-sha256
   --expect-mutants-sha256 --expect-r88-cases-sha256 --scratch-root`; C2: `--repo --rev
   --expect-survivors-sha256 --expect-c1side-sha256 --expect-c2side-sha256 --scratch-root` (a missing
   one exits 2, which the kill rule counts as "not a verdict"). QUALITY 147 also requires every case,
   mutant and carried-file digest in the command.
2. **No harm watch.** Round 88 had one; round 89 has none. `quality/check-tool-ledger.py` takes every
   `quality/counters/*.py` as population (`:13,:82,:178-179`) and requires `R == P` — the two new
   counters will produce `uncovered=2` without rows. `quality/tool-ledger.md:197` still says the mako
   tool has "52 selftest checks" and "criteria AND over ten first-pass fields"; the candidate's selftest
   is `MADO_MAKO_SELFTEST: checks=58 failed=0` (verified) and the field sentence goes stale. Add: index
   check if a knowledge note lands, gate `--selftest`/`--no-live`, ledger, census.
3. **No named-limits list** (round 88 had one). At least: `group-index`/`grouped` still refused (F7);
   RM6C2 alive; the three tool-stance S labels (F4); the NUL-in-line edge (F9).
4. **The case notes' provenance sentence is overbroad.** Notes: "Expectations for r01–r30 come from
   posix-ere-oracle.c … after an independent re-implementation of mako 1.11.0 criteria.c parse_criteria,
   never from the candidate tool." Measured: 27 of 30 carry an oracle result (`summary~`/`body~`
   match/nomatch/invalid); `r17`/`r18` are the "Cannot set both" rule (criteria.c, not the oracle); and
   **`r19-pattern-without-input` carries `"pin": "tool stance: a field without its input is refused"`** —
   a tool-stance label, which the sentence says does not exist. Also, the tokenizer re-implementation is
   named but not committed anywhere under `.ufo/waves/round-89/`; the r14/r15/r16 expectations are
   therefore not re-derivable from committed bytes except through each case's criteria.c pin (criterion
   68 requires a reference model to name the parser it copies and line). Either commit and pin it as
   `controls/parse-criteria-reimpl-r89.py`, or rest the derivation on `criteria.c:162-262` per case.

## 7. What I could not falsify (recorded, so the closure need not redo it)

* The candidate's matcher is libc, C-locale-pinned, and not Python `re` (`mado-mako.c1.py:121-155`); the
  python-re forgery is semantically killed on 10 cases (`r05,r06,r07,r08,r09,r10,r11,r12,r13,r25` — 81/91).
* `carried_count` really compares canonical JSON of the 61 kept round-88 entries and raises SetupError on
  a superseded id (`c1-r89:96-108`); `c53` is genuinely absent from the r89 file.
* M23–M32 (10 new mutants) all map to real criteria.c/POSIX divergences; all 32 are killed (DRAFT).
* Both counter selftests reproduce the disclosure: C1 `27/27`, C2 `18/18`; candidate selftest `58/58`.

## 8. Commands run (with exits) and dead steps

DRAFT, all under `TMPDIR=/fast/scratch/hyaku/mado-r89/R89MCritic/scratch`:

| command | exit | result |
|---|---|---|
| `git show af998dcc…:tools/mado-mako.py \| sha256sum` | 0 | `c374d715…92237` = declared |
| `git show af998dcc…:…/mako-cases-r88.json` vs r89 first 61 (canonical, via `carried_count`) | 0 | 61/61 |
| `python3 -I draft_score.py` (in-process `c1.score()`) | 0 | TARGET_MET 91/91, 32/32, controls 22/23/67/81 |
| `python3 -I draft_c2.py` (in-process `c2.evaluate()`) | 0 | base: 96/96, 7 killed, RM6C2 crash, B-only 0; candidate: 95/96 (only c53 FAIL) |
| `python3 -I quality/counters/c1-r89-mako-regex.py --selftest --candidate-file …/mado-mako.c1.py --scratch-root …` | 0 | `SELFTEST: passed=27/27` |
| `python3 -I quality/counters/c2-r89-survivor-kills.py --selftest --scratch-root …` | 0 | `SELFTEST: passed=18/18` |
| `python3 -I …/mado-mako.c1.py --selftest --scratch-root …` | 0 | `MADO_MAKO_SELFTEST: checks=58 failed=0` |
| `./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | 0 | `mado ok`, 430 rows, 55 W04 |
| `man 5 mako` / `man 3 regcomp` / `man 7 regex` (read-only) | 0 | anchors quoted in F10 |
| `python3 -c "import locale; print(locale.setlocale(locale.LC_CTYPE))"` | 0 | `en_US.UTF-8` — an unpinned Python regcomp would compile in UTF-8, so the candidate's `LC_ALL=C` pin is load-bearing |
| `curl` of the v1.11.0 tarball + `grep -rn setlocale mako-1.11.0/` | 1 (grep) | no match — the tree calls no setlocale; meson deps are cairo/pango/glib/gdk-pixbuf/wayland (no gtk init) |

Dead steps:

1. `python3 -I .ufo/waves/round-89/build/mado-mako.c1.py --selftest` → `mado-mako: setup error: --selftest
   requires --scratch-root` (exit 0 printed by the harness pipeline, the tool's own exit is the setup
   error). Re-run with `--scratch-root` → 58/58.
2. My first C2 DRAFT driver passed the full 62-case round-88 file to `evaluate()`; `evaluate()` does not
   apply `EXCLUDED_B` (that lives in `run()`), so it scored 96 cases and reported one FAIL at the C1
   candidate — `case c53-summary-tilde-refused FAIL missing-refusal`. That is the expected C1 supersession,
   not a defect; with the counter's B (c53 excluded) the value is 95/95. Disclosed because the 96/95 gap
   is exactly the trap a reader re-deriving by hand would fall into.

Installs: none. Git/jj mutations: none. Host reads: the mako tag tarball, three mako sources, three man
pages, `/usr/include/regex.h` flags as cited in the declaration, the config chain never opened.

Scratch: `/fast/scratch/hyaku/mado-r89/R89MCritic` removed after the report was written (`rm -rf`), so
this seat leaves no scratch on disk.
