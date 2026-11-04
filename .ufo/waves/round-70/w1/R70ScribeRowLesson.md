# R70ScribeRowLesson — seat report (mado round 70, w1)

seat: R70ScribeRowLesson — scribe, leaf (no subagent dispatch, per seat bounds)
round: mado lane counter 70, hyaku run 15
frozen inputs read only: `.ufo/waves/round-70/claims-declaration-r70.md` @ `bc18399b409a6390a6c6e8831bf9ad2dacbbf189`
base `b37a5aec4ea03f2223d8e09dd5d386d055c24179`; instruments commit named by the seat `5144a6b5f43225d8021a469f4d24c19558026b9e`
lane head when the seat started `5144a6b5`; when these drafts were finalised `3aea1e10aad3365ca1b648ddfba7e6b1818970fc` — the L1 landed S439/S440, then S441, and wrote `corpus/lessons/round-70.md`, all while the seat ran (F7/F8)
writes: only `.ufo/waves/round-70/w1/R70ScribeRowLesson/` and `/fast/scratch/hyaku/mado-r70/R70ScribeRowLesson{,2,3}/`
not executed by this seat: either scored counter, the gate, the landing script, any git mutation in the lane, any install. Fixture git repos were created only under scratch (F8)

## Produced

| artifact | path (relative to `mado-shokunin/`) | bytes | sha256 |
|---|---|---|---|
| A — S439 anchor replacement (one cell) + S442 ast (rejected) | `.ufo/waves/round-70/w1/R70ScribeRowLesson/draft/corpus/SOURCES-rows.txt` | 4232 | `5471ea860e2b754af5482a2c87fb6b6904d35b196ec8128a32d720f5388c99c5` |
| A′ — S443 raw-.rst subprocess row (superseded, rejected) | `.ufo/waves/round-70/w1/R70ScribeRowLesson/draft/corpus/SOURCES-row-subprocess-CONFLICT.txt` | 2857 | `bb6f761fe0ae0813fe82eb5ff08f8819936130ac12c472f9b1d52aab228d3962` |
| B — round lesson | `.ufo/waves/round-70/w1/R70ScribeRowLesson/draft/corpus/lessons/round-70.md` | 20472 | `bb293c8173adb796d9086083b41448012162109f2899f105d4e3b3e68bfb8fd7` |
| C — QUALITY 112–113 | `.ufo/waves/round-70/w1/R70ScribeRowLesson/draft/corpus/QUALITY-addendum.md` | 4516 | `8dd792e2e0cf549b6d6260672f42060ebd71a2d1d987ec9a45445e818380d440` |

All three rows parse as 11 cells (`awk -F'|'` → NF 13) with no literal or escaped pipe. A is **not** a
set of appends: the rows are already landed (`corpus/SOURCES.md:389-391`), so A carries (i) a
**replacement** for S439's anchor cell — one cell, because the landed `509-512` cannot cover the row's
own quote or the C2 entry's four locators — and (ii) **S442** `ast.rst`, rejected with the L1's flip.
A′ carries **S443**, the raw-.rst subprocess row, superseded by the landed rendered-page S441.

## Commands and outcomes

Run from `/home/vgpnk/Projects/shokunin/mado-shokunin` unless stated. Scratch
`S=/fast/scratch/hyaku/mado-r70/R70ScribeRowLesson` (`…2`, `…3` for the later rounds).

| command | exit | observed |
|---|---|---|
| `curl -fsSL --retry 2 -o <name>.<i> <URL>` (3 URLs × 3 fetches) | 0 | one distinct sha256 per URL (3/3 identical): subprocess 61,603 B / 1,622 lines / `05cd782c…`; expressions 92,034 B / 2,407 / `e19de4fe…`; ast 92,619 B / 2,698 / `9908f4f0…` |
| same, second round: expressions.rst × 3 and `Doc/reference/simple_stmts.rst` × 3 | 0 | expressions 3/3 identical; simple_stmts 3/3 identical, 41,375 B, 1,079 lines, `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc` |
| `git -c protocol.version=2 ls-remote https://github.com/python/cpython 'refs/tags/v3.14.8*'` | 0 | tag object `992560c2cc62d47b308cec662feb485456847931` → peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12` |
| `grep -c 'raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst' corpus/SOURCES.md` | 0 | `1` — duplicate (S108, `corpus/SOURCES.md:120`); expressions.rst and ast.rst grep to 0 |
| `awk -F'|' '/^\| S/{printf "%s fields=%d cells=%d\n",$2,NF,NF-2}'` on A and A′ | 0 | `S439 13/11`, `S442 13/11`, `S443 13/11` |
| `grep -c '\\|'` on A and A′ | 1 (no match) | `0` in both |
| `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | 0 | `mado ok …/corpus/SOURCES.md`; only the pre-existing W04 set (S387–S395); 375 rows before adoption |
| **`python3 quality/check-anchor-cover.py --repo <fixture> --rev HEAD --entry entry.md --work <fixture>/work`** on a scratch fixture holding the **landed** `corpus/SOURCES.md` and an 8-row entry | **1** | `S439 :514/:516/:1161/:1137 → MISS reason=no-cover (locators=509-512)`; `S439 :510 → OK` (the `.. index::` block — false cover); `S440 :190 → OK`; `S441 :136 → MISS`; `S441 :360 → OK`; `CHECK107: rows=8 covered=3 miss=5 verdict=FAIL` |
| same checker, fixture where only S439's anchor cell is replaced by A's line | 1 | `S439 :514/:516/:1161/:1137/:510 → OK` (locators `481-518,1096-1140,1161-1166`); `S440 :190 → OK`; `S441 :136 → MISS`; `S441 :360 → OK`; `CHECK107: rows=8 covered=7 miss=1` |
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
| `awk 'NR>=505 && NR<=520'` on `expressions.rst.1` | 0 | 509-513 = blank + `.. index::` + two index entries; the quoted sentence starts at **514**, ends at **517** |
| `awk 'NR>=185 && NR<=196'` on `simple_stmts.rst.1` | 0 | the L1's quote sits at **190-192** exactly |
| `python3 quality/check-anchor-cover.py --repo <fixture> --rev HEAD --entry <one-row S435 entry>` | **1** | `ANCHOR_COVER: row=K01 sid=S435 line=3902 name=Exit-Status.html locators=none eof=unchecked verdict=MISS reason=no-cover`; `CHECK107: rows=1 covered=0 miss=1 verdict=FAIL` — the production C1 entry's K01 pin |
| `python3` census over `corpus/SOURCES.md` replicating the checker's name/occurrence rule | 0 | `total_rows=378 named_rows=309 no_url_name=69 named_with_locator=180 named_without_locator=129` |

## Findings

**F1 — the C1 ground URL is already registered, and S108 cannot carry a pin.** `Doc/library/subprocess.rst`
@ v3.14.8 is **S108** (`corpus/SOURCES.md:120`, tier A, `mined`, scope `args`). A second row for the same
URL is census W04, and `check-anchor-cover.py:136-155` resolves the row's file name from the **last** URL
in the source cell (`Lib/subprocess.py` → `subprocess.py`), which S108's anchor never names, so any pin
citing S108 is `locators=none MISS` (replica above; `R70ScribeEntryC1` reproduced it independently).
The L1 resolved this by landing **S441 against the rendered page** (`docs.python.org/3.14/library/subprocess.html`,
207,155 B, `c8a66b3a…`, anchor `subprocess.html:360-366`) — a different URL, so no duplicate-URL
question, but only `subprocess.html:360-366`-class pins pass (measured, F8). The raw-.rst row (A′/S443)
is the byte-stable alternative, rejected for this round.

**F2 — the measured content is not the instrument commit the declaration names.** The declaration says
"The scored instruments are committed at 5144a6b5"; the receipt's measured content is `5adba5a9`, and
two of the three counters differ between them: `c1-r70-real-children.py` `b1785f38…` → `b3a6f131…`,
`c2-r70-carriers.py` `87ca4664…` → `d868ae33…` (`c1-r70-landing-controls.py` is `71a7b6c4…` at both).
The intervening commits are `9508e878` ("create the per-scenario scratch dir in the C1 counter;
predicate unchanged", 23:32:33) and `5adba5a9` ("label the candidate and base control-leg lines …
observability only", 23:33:01), both after the freeze `bc18399b`. This seat did **not** audit those two
diffs; it records the byte divergence only.

**F3 — M70-1 re-derived.** The r69 block is at `LOG.md:3257-3266` (inside `### Round 67` at `:3220`),
`LOG.md:3314-3323` (inside `## Round 68` at `:3273`) and `LOG.md:3396-3405` (`### Round 69` at `:3339`).
One precision: the Round-68 heading is **H2**, so a `^### Round` sweep silently attributes the middle
copy to Round 67; the correct sweep is `^#+ Round`.

**F4 — M70-2 re-derived.** 19 commits vs 18 enumerated rows; `b9b70a09` is in no row, no `LOG.md`, no
`SCORECARD.md`; its diff is `+262 −9` over 8 files.

**F5 — M70-3 re-derived.** `check-freeze-order.py:36` hardcodes `claims-frozen.md`/`registration.md`;
the r69 receipt reads `SETUP work_not_a_directory` (`final-gates-r69.txt:17`), not `no_freeze`. The
lane's own freeze evidence is the commit-time chain `bc18399b` 23:27:05 < `5144a6b5` 23:29:46 <
`5adba5a9` 23:33:01. The check repair is production code and is routed, not drafted here.

**F6 — M70-4 re-derived.** r69 `w1-results.json` rows carry exactly `agent,name,note,output` over 12
rows; no settlement field. Round 70 has no `w1-results.json` yet → reported only.

**F7 — the lane moved under this seat.** `5144a6b5` → `9508e878` → `5adba5a9` → `71caa8b7` →
`3aea1e10`, plus the L1's working-tree edits to `corpus/SOURCES.md`, `SCORECARD.md`, two knowledge
entries, `measurement-r70.txt`, and the new `corpus/lessons/round-70.md`. Read, not written or reverted.

**F8 — the landed registry rows fail the entry locators, measured with the checker itself.** Running
`quality/check-anchor-cover.py` over a scratch fixture that holds the **landed** `corpus/SOURCES.md`
(plus the working-tree S441) and an eight-row entry gives
`CHECK107: rows=8 covered=3 miss=5 verdict=FAIL (rc 1)`:
- **S439's landed anchor `expressions.rst:509-512` is short and self-inconsistent.** 509-513 are a blank
  line plus `.. index::` with two index entries; the row's own quoted sentence starts at `:514` and ends
  at `:517`. The C2 entry's four locators (514, 516, 1137, 1161) all MISS. A pin at `:510` passes and is
  a **false cover** — the round's sharpest instrument limit: green check-107 does not evidence that a
  locator supports a quote, and QUALITY 112/113 do not catch it either.
- **S440 passes** (`simple_stmts.rst:190` ⊂ `190-194`), and its bytes and quote are correct (41,375 B,
  `d4320642…`, quote at `:190-192`).
- **S441 is the rendered page**: `subprocess.rst:136` MISSes, `subprocess.html:360` passes; the
  `getstatusoutput` `127`/`-15` lines are outside the anchor. The rendered `/3.14/` URL is not
  version-pinned (3.14.10 on the fetch date), so its `recheck: 90d` is a digest re-fetch, not a tag watch.
- Replacing **only** S439's anchor cell with A's line (locators `481-518,1096-1140,1161-1166`) gives
  `rows=8 covered=7 miss=1` — all four C2 pins and the `:510` pin OK; the only remaining miss is C1's
  `.rst` pin, which is a pin-side change (`subprocess.html:360`), not a registry change.
- The L1's production lesson also says "the registry diff is 2 rows (S439/S440), not 3" while the working
  tree carries three (S441 landed after the sentence was written); that line needs an append-only
  correction, as does its `expressions.rst:509-512` locator.

**F9 — a second landed artifact is red for the same structural reason: S435's anchor never names its own
file.** `corpus/SOURCES.md:385` (S435, GNU Bash 5.3) has URL basename `Exit-Status.html`, but its anchor
cell carries only `bashref.texi:3902-3906,3911-3916,3925-3928`. `check-anchor-cover.py` requires
`Exit-Status.html:NNN` in the anchor, so the production entry's K01 pin
(`corpus/knowledge/landing-kill-credit-real-children-r70.md:85`, row `| K01 | … | S435 | Exit-Status.html:3902 |`)
measures `locators=none verdict=MISS reason=no-cover`, `CHECK107: rows=1 covered=0 miss=1 verdict=FAIL rc 1`
(verified here; `R70ScribeEntryC1` reports `rows=3 covered=2 miss=1` for its draft, and avoided S435). This
is the same defect class as S108: **a registry row is pinnable only if its anchor spells the URL's
basename.** Census over the registry at this head (378 rows, script above): 69 rows have no URL-derived
name (own-work sources and anchors that carry no URL), 309 are URL-named, and **129 of those 309 carry no
`<basename>:` locator at all**, so no pin citing them can ever pass check-107 (180 are pinnable). A green
CHECK107 therefore proves coverage only inside the 180-row pinnable subset; entry authors must check the
anchor's spelling, not just the row's existence. Reported, not fixed: S435 is a held row newly listed in a
round-70 entry's `used-by`, and widening its anchor in place is outside the permitted cell set.

## Outcome and boundaries (this seat)

- Produced: one single-cell registry replacement that is measured to fix four entry locators, two
  rejected rows with flips and measured byte facts, the lesson with the three required sections, and two
  QUALITY criteria (112 record order + commit enumeration; 113 parsed failed assertion as kill credit).
  Everything is grounded on bytes I opened or commands I ran, except the two C1/C2 outcome lines, which
  are the round receipt's and are labelled as such in the lesson.
- Not produced, deliberately: any production path (`corpus/SOURCES.md`, `corpus/QUALITY.md`, the L1's
  `corpus/lessons/round-70.md`, `LOG.md`, `SCORECARD.md`, `MANIFEST.json`, `.ufo/state`), any edit to the
  frozen declaration/control JSON/baseline receipt, any `[x]`, any commit or lane git mutation.
- Not measured: both scored counters, the gate, the landing script, the two post-freeze instrument diffs,
  and any runtime behaviour. The declaration's Not-claimed list stands unabridged.
- Tooling: none installed or upgraded; no package-manager transaction (host pacman pause respected);
  `curl`, `git ls-remote`, `git` (fixtures only), `python3`, `jq`, `awk`, `sha256sum`.
- Scratch: `…RowLesson`, `…RowLesson2`, `…RowLesson3` (including both fixture repos) removed with
  `rm -rf`; `test -e` → rc 1 for the first two, and the third is removed before this report is yielded.
- Peer coordination: `R70ScribeEntryC1` (S442 draft superseded by landed S441; re-pinned to
  `subprocess.html:362` and `:364`, measured `rows=2 covered=2 miss=0`; independently found the S435
  defect F9) and `R70ScribeEntryC2` (blocking S439 report with the pasted checker output; moved its K04
  to S440 and kept K01-K03 on the correct expressions lines; measured `rows=5 covered=2 miss=3` against
  the landed anchor and `5/5` against the widened cell — the two measurements agree with mine).

## Routed defects (not fixed by this seat)

1. **S439 anchor cell** (`corpus/SOURCES.md:389`) — widen to `expressions.rst:481-518,1096-1140,1161-1166`;
   measured to fix all four C2 pins. In-place anchor change is outside the registry's permitted cell set,
   so this needs an L1/operator decision. A's line is the ready replacement.
2. **C1 entry locators** — S441 is the rendered page; pins must be `subprocess.html:360-366`-class, and
   the `127`/`-15` examples are outside the anchor (widen or keep them as prose).
3. **Freeze-order check cannot see this lane's freeze file** — `check-freeze-order.py` `REQUIRED` (F5).
4. **Declaration vs receipt instrument revision** (F2) — the round entry must say which bytes the
   sentence means.
5. **LOG block duplication and `b9b70a09`** (F3/F4) — the round-70 LOG entry is the place for the erratum
   and the missing row.
6. **Production lesson corrections** (F8) — the "2 rows, not 3" sentence and the `509-512` locator need an
   append-only correction in the round entry.
7. **S435 and the unpinnable-third of the registry** (F9) — a held row whose anchor never spells
   `Exit-Status.html`, and 129 of 309 URL-named rows in the same condition; a pin census (the script in
   the command table) should join the gate so entry authors see the pinnable subset, and S435's anchor
   needs an L1/operator decision before the next entry cites it.

Report: `.ufo/waves/round-70/w1/R70ScribeRowLesson.md`
