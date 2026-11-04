# R70ScribeRowLesson — seat report (mado round 70, w1)

seat: R70ScribeRowLesson — scribe, leaf (no subagent dispatch, per seat bounds)
round: mado lane counter 70, hyaku run 15
frozen inputs read only: `.ufo/waves/round-70/claims-declaration-r70.md` @ `bc18399b409a6390a6c6e8831bf9ad2dacbbf189`
base `b37a5aec4ea03f2223d8e09dd5d386d055c24179`; instruments commit named by the seat `5144a6b5f43225d8021a469f4d24c19558026b9e`
lane head when the seat started `5144a6b5`; when the drafts were realigned `3aea1e10aad3365ca1b648ddfba7e6b1818970fc`; the L1's production lesson `corpus/lessons/round-70.md` appeared on disk at 23:39 under the seat (F8)
writes: only `.ufo/waves/round-70/w1/R70ScribeRowLesson/` and `/fast/scratch/hyaku/mado-r70/R70ScribeRowLesson{,2}/`
not executed by this seat: either scored counter, the gate, the landing script, any git mutation, any install

## Produced

| artifact | path (relative to `mado-shokunin/`) | bytes | sha256 |
|---|---|---|---|
| A — registry rows (S439 mined, S441 rejected) | `.ufo/waves/round-70/w1/R70ScribeRowLesson/draft/corpus/SOURCES-rows.txt` | 4392 | `e654b8abe3ffa69a11863703216c549d673246fa0a40f987b88e5e70b3791ddf` |
| A′ — conflict row S442 (rejected; not to append) | `.ufo/waves/round-70/w1/R70ScribeRowLesson/draft/corpus/SOURCES-row-subprocess-CONFLICT.txt` | 3665 | `5512b939be19e328e62fb780d2c3953d1f3a61587eb4b44e6deda9f944a50743` |
| B — round lesson | `.ufo/waves/round-70/w1/R70ScribeRowLesson/draft/corpus/lessons/round-70.md` | 18930 | `ca6ab82aa883392ef6eb3561d69a593a34453b7181aa77abb627e5f12297810b` |
| C — QUALITY 112–113 | `.ufo/waves/round-70/w1/R70ScribeRowLesson/draft/corpus/QUALITY-addendum.md` | 4516 | `8dd792e2e0cf549b6d6260672f42060ebd71a2d1d987ec9a45445e818380d440` |

All three rows parse as 11 cells (`awk -F'|'` → NF 13) with no literal or escaped pipe in any cell.
A carries **S439** (`Doc/reference/expressions.rst`, `mined`) and **S441** (`Doc/library/ast.rst`,
`rejected` with the L1's flip); A′ carries **S442** (`Doc/library/subprocess.rst`, `rejected`,
teaches says `supersedes S108`). No row for `subprocess.rst` in A — the URL is S108's, and the L1's
Gate refuses the second row and substitutes held S435 for C1.

## Commands and outcomes

Run from `/home/vgpnk/Projects/shokunin/mado-shokunin` unless stated. Scratch
`S=/fast/scratch/hyaku/mado-r70/R70ScribeRowLesson` (then `…RowLesson2` for the second, Gate-checking round).

| command | exit | observed |
|---|---|---|
| `mkdir -p "$S/fetch" && curl -fsSL --retry 2 -o <name>.<i> <URL>` (3 URLs × 3 fetches) | 0 | one distinct sha256 per URL (3/3 identical): subprocess 61,603 B / 1,622 lines / `05cd782c…`; expressions 92,034 B / 2,407 / `e19de4fe…`; ast 92,619 B / 2,698 / `9908f4f0…` |
| same, second round: expressions.rst × 3 and `Doc/reference/simple_stmts.rst` × 3 | 0 | expressions 3/3 identical (`e19de4fe…`); simple_stmts 3/3 identical, 41,375 B, 1,079 lines, `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc` |
| `git -c protocol.version=2 ls-remote https://github.com/python/cpython 'refs/tags/v3.14.8*'` | 0 | tag object `992560c2cc62d47b308cec662feb485456847931` → peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12` |
| `grep -c 'raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst' corpus/SOURCES.md` | 0 | `1` — duplicate (S108, `corpus/SOURCES.md:120`); expressions.rst and ast.rst grep to 0 |
| `awk -F'|' '/^\| S/{printf "%s fields=%d cells=%d\n",$2,NF,NF-2}'` on A and A′ | 0 | `S439 13/11`, `S441 13/11`, `S442 13/11` |
| `grep -c '\\|'` on A and A′ | 1 (no match) | `0` in both |
| `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | 0 | `mado ok …/corpus/SOURCES.md`; only the pre-existing W04 set (S387–S395); 375 rows before adoption |
| `awk '/^#+ Round/{r=$0} /Wave settlement: 12 seats dispatched/{printf "%d \| %s\n",NR,r}' LOG.md` | 0 | `3266 \| ### Round 67 — …`, `3323 \| ## Round 68 (2026-11-03) — …`, `3405 \| ### Round 69 — …` |
| `git rev-list --count 04093b83f73a841117d3b31dbb2a6063f4f2a454..9d91f7f6f5c603bdc19cf455ce6f413c5990d744` | 0 | `19` |
| `awk 'NR>=69 && NR<=86 && /^\|/' /home/vgpnk/Projects/shokunin/.ufo/reports/round-69/mado.md \| wc -l` | 0 | `18` rows in the Landed-changes table |
| `git show --stat --format='%h %cI %s' b9b70a09c57f9de1f0e87cc50e76b16ae99090df` | 0 | `2026-11-03T23:01:21-03:00`, 8 files, `+262 −9`; absent from `LOG.md`/`SCORECARD.md` (`grep -c` → 0 and 0) |
| `grep -n 'REQUIRED' quality/check-freeze-order.py` | 0 | `:36  REQUIRED = ("claims-frozen.md", "registration.md")` |
| `grep -n 'MADO_FREEZE_ORDER' .ufo/waves/round-69/*.txt` | 0 | `.ufo/waves/round-69/final-gates-r69.txt:17: MADO_FREEZE_ORDER: SETUP work_not_a_directory` |
| `git log --format='%h %cI %s' -1 <rev>` for `bc18399b 5144a6b5 9508e878 5adba5a9 71caa8b7 3aea1e10` | 0 | 23:27:05 / 23:29:46 / 23:32:33 / 23:33:01 / 23:34:48 / 23:35:34 (-03:00) |
| `jq -c '[.results[] \| keys] \| unique' .ufo/waves/round-69/w1-results.json`; `jq '.results\|length'` | 0 | `[["agent","name","note","output"]]`; `12` |
| `ls .ufo/waves/round-70/w1-results.json` | 2 | `No such file or directory` |
| `for r in 5144a6b5 5adba5a9; do git show $r:quality/counters/<f> \| sha256sum; done` | 0 | c1-real-children `b1785f38…` → `b3a6f131…`; c2-carriers `87ca4664…` → `d868ae33…`; c1-landing-controls `71a7b6c4…` at both |
| `python3` replica of `quality/check-anchor-cover.py:73-90` `occurrences()` on S108's cells | 0 | `last_url=…/Lib/subprocess.py`, `name=subprocess.py`, `occurrences=[]` → `MISS reason=no-cover` |
| `awk 'NR>=505 && NR<=520'` on `expressions.rst.1` | 0 | 509-513 = blank + `.. index::` + two index entries; the quoted sentence starts at **514** and ends at **517** |
| `awk 'NR>=185 && NR<=196'` on `simple_stmts.rst.1` | 0 | the L1's quote sits at **190-192** exactly |

## Findings

**F1 — the C1 ground URL is already registered, and the registered row cannot carry a C1 pin.**
`Doc/library/subprocess.rst` @ v3.14.8 is **S108** (`corpus/SOURCES.md:120`, tier A, `mined`, scope =
`args`). `quality/check-anchor-cover.py:136-155` derives the row's file name from the **last** URL in
the source cell (S108's last URL is `Lib/subprocess.py`, name `subprocess.py`) and then requires
`subprocess.py:NNN` inside the anchor cell; S108's anchor carries bare `:38-43` locators and no
`subprocess.py:` occurrence, so a `subprocess.rst:136` pin against S108 returns
`locators=none verdict=MISS reason=no-cover` (replica above; `R70ScribeEntryC1` reproduced it
independently with a synthetic pin: `MISS rc 1`). **The L1 resolved this by refusing the row and
substituting held S435 (GNU Bash 5.3 § Exit Status) for C1** — so nothing is appended this round, and
the C1 entry must cite S435. The ready row for a future round is A′ (S442, `rejected`, teaches says
`supersedes S108`); its anchor carries `136-142`, `949-963`, `1500-1510`, and `R70ScribeEntryC1`
measured a synthetic adoption as `CHECK107: rows=6 covered=6 miss=0 verdict=OK rc 0`.

**F2 — the measured content is not the instrument commit the declaration names.** The declaration
says "The scored instruments are committed at 5144a6b5"; the receipt's measured content is
`5adba5a9`, and two of the three counters differ between them: `c1-r70-real-children.py`
`b1785f38…` → `b3a6f131…`, `c2-r70-carriers.py` `87ca4664…` → `d868ae33…`
(`c1-r70-landing-controls.py` is `71a7b6c4…` at both). The intervening commits are `9508e878`
("create the per-scenario scratch dir in the C1 counter; predicate unchanged", 23:32:33) and
`5adba5a9` ("label the candidate and base control-leg lines … observability only", 23:33:01), both
after the freeze `bc18399b`. This seat did **not** audit those two diffs; it records the byte
divergence only. The frozen sentence does not name a revision, and the receipt measures the later bytes.

**F3 — M70-1 re-derived.** The r69 block is at `LOG.md:3257-3266` (inside `### Round 67` at `:3220`),
`LOG.md:3314-3323` (inside `## Round 68` at `:3273`) and `LOG.md:3396-3405` (`### Round 69` at `:3339`).
One precision over the spot-check's wording: the Round-68 heading is **H2**, so a `^### Round` sweep
silently attributes the middle copy to Round 67; the correct sweep is `^#+ Round` (output above).

**F4 — M70-2 re-derived.** 19 commits vs 18 enumerated rows; `b9b70a09` is in no row, no `LOG.md`, no
`SCORECARD.md`. The diff is `+262 −9` over 8 files including `measurement-final-r69.txt`,
`cross-set-r69.txt`, `final-gates-r69.txt`, `landing-counters-r69.txt`.

**F5 — M70-3 re-derived.** `check-freeze-order.py:36` hardcodes `claims-frozen.md`/`registration.md`;
the lane submits `claims-declaration-rN.md`; the r69 receipt line is `SETUP work_not_a_directory`
(`final-gates-r69.txt:17`), not `no_freeze`. The lane's own freeze evidence for round 70 is the commit
time chain `bc18399b` (declaration, 23:27:05) < `5144a6b5` (instruments, 23:29:46) < `5adba5a9`
(measurement, 23:33:01), re-derivable with `git log --format='%h %cI' -1 -- <path|rev>`. The
`check-freeze-order.py` repair (parameterise the required set; its own selftest fixtures construct the
two hardcoded names) is production code and is **routed, not drafted** by this seat.

**F6 — M70-4 re-derived.** r69 `w1-results.json` rows carry exactly `agent,name,note,output` over 12
rows; no settlement field. Round 70 has no `w1-results.json` yet, so this is reported only; the fix
lands when the L1 writes the file with `status: settled|dead` per row.

**F7 — the lane head moved under this seat** (`5144a6b5` → `9508e878` → `5adba5a9` → `71caa8b7` →
`3aea1e10`) and the working tree gained `quality/tool-ledger.md` modifications plus tracked wave
receipts. I read but did not write or revert any of it; the drafts are against the frozen inputs.

**F8 — the L1's production lesson exists and its Gate carries one locator defect.** At 23:39 the L1
wrote `corpus/lessons/round-70.md` (untracked, 10,994 B) with its own M70-1..M70-5 and a Gate that
admits **S439 = expressions.rst** and **S440 = simple_stmts.rst**, refusing subprocess.rst and ast.rst.
Checks I ran on that Gate:
- S440 is byte-correct and its quote locator is exact: 41,375 B, 1,079 lines,
  `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, three byte-identical fetches, and
  "If the target is a subscription: The primary expression in the reference is evaluated. Next, the
  subscript expression is evaluated." sits at `simple_stmts.rst:190-192`.
- S439's quote is **mislocated**: the Gate cites `expressions.rst:509-512`, but 509-513 are a blank line
  plus `.. index::` and two index entries; the sentence starts at `:514` and ends at `:517`. The
  drafted row anchors `:514`, so the register bytes will be right if the row is adopted with this
  anchor. Reported, not edited — the production file is the L1's.
- The L1's S439 anchor must cover `1096-1140` and `1161-1166` or `R70ScribeEntryC2`'s pins at
  `expressions.rst:1137` and `:1161` miss check-107; the drafted S439 row provides that coverage and
  C2 measured `CHECK107_SIM rows=5 covered=5` against it.
So the id collisions are resolved as S439 (agrees), S441 (ast, rejected), S442 (subprocess, rejected).
Two peer drafts were told: C1 must move to S435; C2 keeps S439 with the caveat that the landed anchor
must include the subscription ranges.

## Outcome and boundaries (this seat)

- Produced: one mined row, two rejected rows with flips, the lesson with the three required sections,
  and two QUALITY criteria (112 record order + commit enumeration; 113 parsed failed assertion as kill
  credit), all grounded on bytes I opened or commands I ran — except the two C1/C2 outcome lines, which
  are the round receipt's and are labelled as such in the lesson.
- Not produced, deliberately: any production path (`corpus/SOURCES.md`, `corpus/QUALITY.md`, the L1's
  `corpus/lessons/round-70.md`, `LOG.md`, `SCORECARD.md`, `MANIFEST.json`, `.ufo/state`), any edit to
  the frozen declaration/control JSON/baseline receipt, any `[x]`, any commit or git mutation.
- Not measured: both scored counters, the gate, the landing script, the two post-freeze instrument
  diffs, and any runtime behaviour. The declaration's Not-claimed list stands unabridged.
- Tooling: none installed or upgraded; no package-manager transaction (host pacman pause respected);
  `curl`, `git ls-remote`, `python3`, `jq`, `awk`, `sha256sum` only.
- Scratch: `/fast/scratch/hyaku/mado-r70/R70ScribeRowLesson` and `…RowLesson2` both removed with
  `rm -rf` (`test -e` → rc 1) before this report was yielded.
- Peer coordination: `R70ScribeEntryC1` (S442-vs-S435 warning and the S108 anchor-cover measurement)
  and `R70ScribeEntryC2` (S439 confirmed; the L1's S439 anchor must cover the subscription ranges).

## Routed defects (not fixed by this seat)

1. **Freeze-order check cannot see this lane's freeze file** — `quality/check-freeze-order.py`
   `REQUIRED` (F5). Needs a parameterised required set and matching selftest fixtures.
2. **C1's sourced ground** — the L1 substituted S435; the declaration still names
   `Doc/library/subprocess.rst`, whose URL is S108's and whose pin S108 cannot carry (F1/F8). The
   round entry should say which source actually grounds C1, append-only.
3. **Declaration vs receipt instrument revision** (F2) — the L1 must say which bytes the sentence
   means, in the round entry.
4. **LOG block duplication and `b9b70a09`** (F3/F4) — the round-70 LOG entry is the place for the
   erratum and the missing row.
5. **S439 quote locator in the L1's lesson** — `:509-512` should read `:514-517` (F8); a one-line
   append-only correction in the round entry or the next lesson.

Report: `.ufo/waves/round-70/w1/R70ScribeRowLesson.md`
