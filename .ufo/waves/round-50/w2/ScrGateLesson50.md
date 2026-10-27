# ScrGateLesson50 — w2 falsify: `corpus/lessons/round-50.md` completeness vs the round-49 format and the routed items

Seat: `ScrGateLesson50` (scribe). Wave `w2` (falsify, policy v1), mado round 50, 2026-10-27.
Attack rev `b4a79843cc2545bbe800db9322e58f6e00436629`; lane clone `git clone -q --shared` under
`/fast/scratch/hyaku/mado-r50/ScrGateLesson50/clone` (toplevel asserted).

Lesson identity at the attack rev: blob `4529b685df98e6e72c3c705d628613f26d0fd261`, sha256
`e7cd29620aeed655f54fa3401b901acba8fe3f47ffdb4b5e9d6f3a62e20be794` = the digest frozen in
`.ufo/waves/round-50/registration.md` (unchanged since data `906178b6`). 103 lines, 4 headings.

Verdict (attack evidence only; admission judgment stays the L1's + the non-author closure's):
**PASS on 5 of 6 checks; 1 block MISSING; 8 findings (1 missing, 7 weak).** The lesson is not a full round-49-format record: it has
Gate (admits/rejects/status), Assimilation and Mistakes, but no closure-items block, so six of the eight routed items
(D2-D7) have no line in the lesson at all. Everything the lesson *does* assert about the round checked out against the
committed bytes, with the four pointer defects in §F.

## A. Structure parity with `corpus/lessons/round-49.md`

| round-49 section | round-50 counterpart | status |
|---|---|---|
| title + intro (claims/freeze/data hashes) | title + intro (claims `13631f24`, attempt 2) | present |
| `## Gate` (sources, admit lines, `### Rejected after opening`, counts) | `## Gate` (sources, 12 admit lines, 5 rejects, status line) | present; rejects are flat bullets, no subsection (round-49 had one) |
| — | `### Assimilation (…)` | present (round-50 addition, required by this seat) |
| `## Mistakes` (M49-1..M49-4) | `## Mistakes` (M50-1..M50-4) | present |
| `## Round-48 closure items` (N1-N5, M48-8, M48-10, M48-13, SentScratch, Erratum — each with command/receipt) | **absent** | **MISSING** (finding F1) |

`grep -nE '^#{1,4} '` on both files at the rev: round-50 → `1:title, 11:## Gate, 46:### Assimilation, 64:## Mistakes`;
round-49 → `1:title, 6:## Gate, 19:### Rejected after opening, 29:## Mistakes, 49:## Round-48 closure items`
(receipt `receipts/structure.txt`).

## B. M50 rows — field completeness (PASS)

All four rows at the rev carry the four required labels; `receipts/m50-fields.txt`:

| row | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M50-1 (L66) | `ordering` | round-49 report + missing results file + 0-null measurement | `none (no criterion required …)` | criterion 102 + `quality/check-wave-done.py` |
| M50-2 (L76) | `evidence hygiene` | round-49 "2 admits / 4 rejects" vs 12/5 + `w1/CritGateLesson.md` + commands | `none` | dated erratum in `corpus/lessons/round-49.md` (D8) |
| M50-3 (L83) | `registry location` | `w1/ScoutCensus.md` E12 + `scripts/sources-census.sh:618-624` | census validator (E12) | rows appended inside `## Registry`; `receipts/census-after.txt` |
| M50-4 (L90) | `wave lifecycle` | four cut-off seat reports + 54 null outputs | `none` | wave w2 re-runs the four attacks |

Per-row evidence verification: M50-2's two commands reproduce `2` and `5` at the rev and the erratum is present in
`corpus/lessons/round-49.md`; M50-3's row placement is real (S352-S363 at `corpus/SOURCES.md:301-312`, `## Paths` at
`:314`); M50-4's four reports do end without findings (`CritC1Random` "investigating … deliverable pending",
`CritC1Exotic` "in progress", `CritQuality` "findings pending", `MutC2Entry` "status: running" / "Findings will be
filled in here") and `round-50/w1-results.json` is 54/54 `output: null` (`receipts/claims-verified.txt`).

## C. Evidence pointers at `b4a79843` (receipt `receipts/pointers.txt`)

14 lane pointers resolve; 1 forward reference (L61) names a seat the w2 spec actually dispatches; 1 pointer is
fleet-root-only (F5); the fleet commit at L66 resolves in the fleet repo (F2 is about its sub-claim); the L51 claim about
the round report does not resolve at the rev (F3).

| lesson line | pointer | resolution |
|---|---|---|
| 14 | `.ufo/waves/round-50/fetch/` (16 files) | resolves; 16 files at rev (14 upstream + `SHA256SUMS` + `binds-live-r50.txt`) |
| 16 | `ExecFetchR50/cmp-verify.txt` | `w1/ExecFetchR50/cmp-verify.txt` (ends `cmp_equal=14 differ=0 ownwork=1`) |
| 16 | `ExecFetchR50/rows-digest-binding.txt` | `w1/ExecFetchR50/…` (`row-tokens=13`, `mismatches: []`) |
| 18 | `ScrRowsR50/verify-quotes.sh`, `quotes-verified.txt` | resolve; output ends `ALL QUOTES VERIFIED`, `PASS admit lines: 12/12`, `PASS reject lines: 5/5` |
| 37 | `w1/ScrRowsR50/gate.md` §2 | resolves (5 reject blocks) |
| 51 | `considerthese/2026-10-26.md` | resolves; `:47` = proposal 1 "Add a privacy check on new receipts." |
| 61 | `.ufo/waves/round-50/w2/ScoutAssimQuarantine/` | absent at rev (forward reference; the seat **is** in `w2-spec.json` → honest plan, not a dangling cite) |
| 66 | fleet `b0184c43` | fleet repo: `.ufo/reports/round-49/mado.md` present, `:3`/`:122` confirm 7 unsettled + no WAVE-DONE (see F2 for the sub-claim) |
| 67 | `.ufo/waves/round-49/w1-results.json` | resolves (45 results, 0 nulls) |
| 72 | `quality/check-wave-done.py`, `w1/ExecWaveDone` | resolve (`ExecWaveDone/check-wave-done.py`) |
| 77 | `w1/CritGateLesson.md` | resolves (its `:3`/`:6` support M50-2's counts) |
| 78 | `.ufo/waves/round-49/w1/ScrRows/gate.md` | resolves |
| 83 | `w1/ScoutCensus.md` | resolves (`:5`, `:10`, `:16` report E12 for S352-S363) |
| 83 | `scripts/sources-census.sh:618-624` | **not in the lane tree** — fleet-root file only (F5) |
| 88 | `receipts/census-after.txt` | resolves; 21 lines, 0 E-codes, 20 W-codes, last line `mado ok <abs path>` (F6) |
| 51 | "recorded as its `Declared limit` in the round report" | **no round-50 mado report exists at the rev** (F3) |

## D. No w2 outcome pre-claim (PASS)

Only three `w2` mentions at the rev, all prospective/conditional; `receipts/preclaim.txt`:

- L6 "…dispatches `w2` (falsify) and lands." — plan, no result.
- L61 "Hand-check verdicts per row are wave-w2 work …; until they land, adoption from the register stays closed."
- L93 (M50-4 fix) "wave w2 of round 50 re-runs those four attacks … so no pending line is cited as evidence."

`TARGET_MET` ×0, `admitted` ×0, no seat-result or admission sentence; no w2 receipt is cited as evidence. The lesson keeps
admission with the L1 + non-author closure.

## E. Rejects and flip conditions (PASS; classes match)

5 reject lines, 5/5 carry a flip condition; the decision set and order are identical to
`w1/ScrRowsR50/gate.md` §2 (`receipts/rejects.txt`):

| # | lesson reject | gate.md class | flip in lesson | flip in gate.md |
|---|---|---|---|---|
| 1 | `wiki.hypr.land/0.56.0/Configuring/Basics/Binds/` | docs | yes (commit-pinned source S359) | yes |
| 2 | `wiki.hypr.land/Configuring/Basics/Binds/` | docs | yes (commit-pinned raw URL S359) | yes |
| 3 | ArchWiki `Hyprland` | community | yes (version-pinned primary source) | yes |
| 4 | re-register `src/devices/IKeyboard.cpp`@`efb50993` | code | yes (L1: widen S319 `teaches`) | yes |
| 5 | re-register `src/config/values/ConfigValues.cpp`@`efb50993` | code | yes (cite S318 for the default) | yes |

The lesson states no tier/class label on reject lines; round-49's lesson also omitted classes, so this is format parity,
not a loss of the gate's classification (which stays in `gate.md`).

## F. Findings — missing / weak

**F1 (missing, high) — no closure-items block; six routed items absent.**
The round-49 format's last section (`## Round-48 closure items`) enumerated each routed item with its command/receipt.
Round-50's lesson has no such section and no per-item line: `grep -noE '\bD[1-8]\b'` → only `9:D1`, `9:D8`, `81:D8`
(an aggregate "routed items D1-D8" at L9 and D8 inside M50-2's fix). Direct consequence:
- D3 (the 57,865-pair figure): `57,865`/`57865` ×0.
- D4 (do-nothing control on the frozen counter): `do-nothing` ×0.
- D6 (QUALITY criteria for M49-1/M49-3): `criterion 100` ×0, `criterion 101` ×0 — only `criterion 102` (L72).
- D7 (host guard M48-10 installed, both-ways): `tools/mado-hostguard.py` ×0.
- D2 (7 unsettled round-49 seats) and D5 (= C1) appear only obliquely (M50-1; the C1 paragraph of the intro).
`registration.md` carries all eight with statuses, so the round record exists elsewhere; the lesson — the artifact a later
round reads — cannot show that criteria 100-102 and the host guard landed this round.

**F2 (weak, medium) — M50-1's closure-commit pointer is in the wrong repository.**
M50-1 (L67-68) says "`.ufo/waves/round-49/w1-results.json` was not in the closure commit" with "round 49's report (fleet
`b0184c43`)". The fleet repo never tracks the lane's waves: `git ls-tree -r b0184c43 | grep -c '^\.ufo/waves/round-49'` →
`0` and `git log --all --oneline -- '.ufo/waves/round-49*'` → empty. So the cited check cannot fail at the cited commit.
The claim is true at the right locator: lane `8ae47b95` (base) does **not** carry the file, and it was added by lane commit
`1b37a59e` ("hyaku run9 wrap-up"), i.e. after closure. Fix: cite the lane rev pair, not the fleet commit.

**F3 (weak, medium) — "recorded as its `Declared limit` in the round report" does not resolve at the rev.**
Assimilation L51-52 asserts the limit is recorded in the round report. At `b4a79843` no round-50 mado report exists: fleet
`.ufo/reports/round-50/` holds `chousa.md kake.md kama.md kotoba.md kotodama.md kumitate.md mori.md tameshi.md` (no
`mado.md`), and the lane tree has no report file. Written as past tense, it is an unresolvable pointer; as a plan it should
say "will be recorded".

**F4 (weak, medium) — M50-1's count sentence carries no command.**
"measured 2026-10-27: 0 null outputs of 45" (L70) has no command or receipt, while M50-2's own fix rule (L81) says "count
sentences in lessons must carry their command". I reproduced the number (`45` results, `0` nulls at the rev) — the claim is
true, the rule is not applied to the lesson that states it.

**F5 (weak, low) — `scripts/sources-census.sh:618-624` is fleet-root-only.**
The lane has no `scripts/` directory at the rev (`git ls-tree -r b4a79843 | grep '^scripts/'` empty). The file is
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (35466 B) and the E12 `printf` sits at fleet line 621, inside
the cited range. The locator is correct against the fleet root but cannot be resolved by a reader (or checker) that stays
inside the lane repo, and the lesson gives no prefix. The same line is inherited from `w1/ScoutCensus.md:16`.

**F6 (weak, low) — M50-3's "prints exit 0" is inferable, not recorded; the receipt carries a home path.**
`receipts/census-after.txt` has 21 lines: 19 `W04`, 1 `W01`, **0 E-codes**, last line
`mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`. There is no rc line; exit 0 follows from the
validator's logic (`scripts/sources-census.sh:738-740` sets `findings` only on an E-code; `:805-806` exit 0 otherwise).
The receipt also commits an absolute home path — the structural home-path shape the round's own C2 gate flags (the lane is
red by design per `registration.md` "Residuals", so this is a true positive, not a false claim).

**F7 (weak, low) — M50-4's phrasing over-generalises.**
"four seat reports end in 'findings pending' / 'investigating'" (L91): three do; `MutC2Entry`'s last line is a tooling note
and its status line reads "status: running" (its body does say "Findings will be filled in here"). The substance (no
findings, cut off) holds.

**F8 (weak, low) — a fix command embeds an absolute home path.**
L87: ``sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado``. Same red shape family as F6; a `~`/relative
form would keep the lesson out of the C2 finding set it is describing.

## G. Claims verified true (supporting, not findings)

| claim | verification |
|---|---|
| 12 admit lines, each URL/own-work + `opened 2026-10-27` + `pin:line` + quote ≤25 words with stated count | 12/12; every quote is a literal substring of the cited pin line (my re-check 12/12 OK, `receipts/admits-quotes.txt`) |
| "quotes re-verified 12/12" | `quotes-verified.txt` `PASS admit lines: 12/12` … `ALL QUOTES VERIFIED` |
| "16 files" in `fetch/`; "14 upstream pins byte-equal" | 16 files; my own `cmp` over the 14 shared names: `compared=14 differ=0` |
| status/recheck/used-by line (L43) | `SOURCES.md`: S352-S363 `status=mined opened=2026-10-27`; used-by = entry for 10 rows, `corpus/lessons/round-50.md` for S357/S358 |
| "No held row changed" | `git diff 8ae47b95 b4a79843 -- corpus/SOURCES.md`: 12 added, 0 removed, ids S352-S363 |
| S361 digest equals the round-49 capture | `fetch/binds-live-r50.txt:7` `sha256: 9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779 (raw JSON bytes, 90401 …)` |
| assimilation numbers | `w1/ScoutAssimR50.md:6,15` reg-ids 288 / staged 147 / collisions 94, guard fixture 1/1/1; `:7,15` quarantine 13 rows, 6 payload-absent (S189,S195,S201,S205,S224,S228) + 7 prose (S199,S200,S209,S222,S223,S225,S235); seat files present |
| proposal 1 is the privacy check | `considerthese/2026-10-26.md:47` |
| M50-2 commands | `2` (round-49 lesson drafted-admit lines) and `5` (round-49 gate REJECT lines); erratum present in `corpus/lessons/round-49.md` |
| M50-4's 54 null outputs | `round-50/w1-results.json`: 54 results, 54 null |

## H. Conflict reported verbatim (for the canonical judge)

S362 gloss, lesson vs its own source gate:
- lesson L31: "Why an empty state reads level 0".
- `w1/ScrRowsR50/gate.md` §1 S362: "This is why an empty state reads level 1: the type entry must match the active mods
  exactly (`:91`), none matches a zero mask, so the level defaults to 0".
- pin `fetch/xkbcommon-state.c:112` comment "If we don't find an explicit match the default is 0." and `:116`
  `return (entry) ? entry->level : 0;` support the lesson's "0"; the gate text's "reads level 1" is the odd one out.
The lesson cites `gate.md` §2 only for rejects, so this is a source-gate wording defect surfaced by the comparison, not a
lesson error I can score.

## I. Out-of-scope observation (not part of the landed lesson)

The lane **working tree** now differs from the attack rev: `corpus/lessons/round-50.md` is modified (+8 lines, blob
`aa3f66d2`, sha256 `b77fe238…`) by a concurrent integration that appends an **M50-5** row (`declaration` class, citing
`quality/check-deliverables.py` and the untracked `.ufo/waves/round-50/receipts/check101-w1.txt`,
`declared=19 exists=15 absent=4 undeclared=49 verdict=FAIL`). It is not at `b4a79843` and not in the frozen digest
`e7cd29…`; the instrument and the receipt's absence/presence are recorded in `receipts/working-tree-delta.txt`. I did not
touch it.

## Deliverables (all present)

- `.ufo/waves/round-50/w2/ScrGateLesson50.md` (this report)
- `.ufo/waves/round-50/w2/ScrGateLesson50/receipts/structure.txt`
- `.ufo/waves/round-50/w2/ScrGateLesson50/receipts/m50-fields.txt`
- `.ufo/waves/round-50/w2/ScrGateLesson50/receipts/pointers.txt`
- `.ufo/waves/round-50/w2/ScrGateLesson50/receipts/rejects.txt`
- `.ufo/waves/round-50/w2/ScrGateLesson50/receipts/admits-quotes.txt`
- `.ufo/waves/round-50/w2/ScrGateLesson50/receipts/preclaim.txt`
- `.ufo/waves/round-50/w2/ScrGateLesson50/receipts/claims-verified.txt`
- `.ufo/waves/round-50/w2/ScrGateLesson50/receipts/working-tree-delta.txt`

Tooling: none installed or upgraded. No host state written (all git fixtures and reads in the scratch clone, HOME/XDG_*/
TMPDIR under `/fast/scratch/hyaku/mado-r50/ScrGateLesson50`, scratch removed before yielding). No mutating git in the lane
or the fleet; fleet reads were `ls-tree`/`log`/`show` only.
