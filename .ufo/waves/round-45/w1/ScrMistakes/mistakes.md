# Mistakes for `corpus/lessons/round-45.md` — `## Mistakes` (seat ScrMistakes)

Author: seat `ScrMistakes` (mado round 45, w1, hyaku run 9). Date: 2026-10-26. Draft for the L1: the lesson file is
outside this seat's write scope; rows below are paste-ready text.

Inputs read: `corpus/lessons/round-44-verifier-spotcheck.md` §6 (D1-D7, lines 98-118) and its §1-§5; the round-44 lesson
(`corpus/lessons/round-44.md` `## Mistakes`, `## Round-43 errata`, `## Post-data corrections`); the round-44 receipts and
`w2` reports; `SCORECARD.md` Round 43/44 sections; `SOURCES.md` rows S290-S297; `corpus/QUALITY.md` (ends at criterion 84);
`SKILL.md:33,343`; `CORPUS.md:172-186` (row form, class vocabulary, "a fix is shown able to fail"); round-45
`registration.md:64-66` (D1-D7 as routed, not-claims work). Every count below was recomputed with the command beside it; no
number is relayed from the closure.

Row form is CORPUS.md's: class · evidence pointer · captured-by (the QUALITY criterion or rule that should have caught it,
or `none`) · fix, with the fix's fail-ability. Classes are used as the vocabulary defines them: `scope` (wrote outside the
declared surface), `landing` (work that did not land where it is published), `attribution` (a receipt or pointer bound to
the wrong revision or object), `number-drift` (a number that does not reproduce or is published without recompute),
`vacuous`/`survivor` (a gate satisfied by something that skips the work, or a mutant/cheat that lives), `stale-premise` (a
present-tense claim resting on a superseded one), `reference-drift` (a pointer whose target is not where it says).

## Mistakes

**M45-1 — two tracked live `clients -j` dumps carried the host's window titles, and the sweep that would have found the
rest was never run.** Class: `scope` (session material written into tracked bytes; `SKILL.md:343` rule 4, "`clients` for
length/tags, never window titles"). Evidence: at the round-45 base `0c89478a`,
`.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json` is a 4-client dump whose per-client keys include `title`,
`initialTitle`, `pid`, `stableId`, `xdgDescription` and `xdgTag`
(`git show 0c89478a:.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json | grep -c '"title"'` → 4; the identity
keys are listed in `.ufo/waves/round-45/w1/ScrMistakes/receipts/red-before-base.txt`, checker R1); `.ufo/waves/round-43/w2/SentLiveRun/dump-now.json` is the same shape
(4). The closure named these two and asked for a sweep of every tracked live dump; that sweep was not run, and running it
at base finds **26** tracked JSON files with identity fields (**77** checker rows): 18
`.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/*.json` carry 3-5 titles each of that seat's own gkeep test windows, and
round 44's own fixtures `.ufo/waves/round-44/w1/ScrLessonSkeleton/c1-demo/client1.json`, `client2.json` carry one title
each (`.ufo/waves/round-45/w1/ScrMistakes/receipts/d1-sweep-classify.txt`: 0 of those titles hash-match the live dump, so they are fixtures, not the host's
windows — but the field is the field rule 4 forbids). 22 of the ExecOracleGkeep files also carry a non-empty `instance_sig`
of 61-62 characters, the full `HYPRLAND_INSTANCE_SIGNATURE` rule 4 says is never printed in full
(`.ufo/waves/round-45/w1/ScrMistakes/receipts/d1-nested-paths.txt`); their `monitors[*].serial/description/make/model` are empty strings at these receipts, so
no monitor identity leaks there. Classification limit: the round-22/23 `guards-*.json` and round-17 `schema-variants.json`
`title` strings are window-rule/schema fixtures, not client dumps, and the proposed rule does not flag them.
Captured-by: `SKILL.md:343`/`:33` — a prose rule with **no gate**; no QUALITY criterion reads committed bytes for session
material (criteria 47 and 87-candidate do not exist as gates; the proposal is below). Round 44 flagged 2 of the 26 files
and recorded none of the rest. Fix: project every live dump to the 7-key shape of
`.ufo/waves/round-43/fetch/host-clients-r43.json` (`address, at, class, floating, mapped, monitor, size` — verified by
`.ufo/waves/round-45/w1/ScrMistakes/receipts/d1-session-material.txt`), replace `instance_sig` with a length marker, and land criterion 87 below with
`.ufo/waves/round-45/w1/ScrMistakes/checks.py`. Shown able to fail: `checks.py 87 --repo . --rev 0c89478a` prints
`CHECK87: violations=77 verdict=FAIL` (`.ufo/waves/round-45/w1/ScrMistakes/receipts/red-before-base.txt`); one `title` key added to a projected dump prints
`violations=1 verdict=FAIL`, the pristine projection prints `CLEAN` (`.ufo/waves/round-45/w1/ScrMistakes/receipts/controls.txt`). Not landed at this seat's
read: round-45 `w1/ExecProjectTitles` and `w1/ExecPrivacyGate` are in flight, so no green exists in the lane, and the titles
stay in pushed history unless the operator rewrites it (`round-44-verifier-spotcheck.md:98`, operator note).

**M45-2 — the round's published claim rows carried no after value, only a pointer to the receipt that held it.** Class:
`landing` (the measurement landed in `receipts/`, not in the table that publishes the claim). Evidence:
`SCORECARD.md:2570` and `:2571` give the after-state as "see `receipts/c1-after-data.txt`" / "see
`receipts/c2-after-data.txt`" and the self-verdict as "recorded in the round report from the receipts"; the values exist
(`git show 8ac15c41:.ufo/waves/round-44/receipts/c1-after-data.txt` → `fixtures=26/26 … verdict=TARGET_MET
rev=e4678921…`; c2 → `admitted=1/1 … TARGET_MET`), so nothing was missing but the publication. The same defect is older
than the routed item: the Round-43 section's rows (`SCORECARD.md:2480-2481`) say "see report for the data-tip receipt"
and "see report". Captured-by: `none` surviving — criterion 79 passes a pointer to a committed receipt whose bytes carry
command/output/exit, and criterion 69 passes because the receipt exists at the attributed revision; criterion 78 counts
control tallies, not claim rows. Fix: append the values and verdicts in the next SCORECARD section (never rewrite the
Round 43/44 text), and land criterion 88. Shown able to fail: `checks.py 88 --repo . --rev 0c89478a` prints
`violations=4` at `SCORECARD.md:2480,2481,2570,2571`; the pointer-only mutant of a corrected row prints `violations=1`,
the corrected control `CLEAN` (`.ufo/waves/round-45/w1/ScrMistakes/receipts/red-before-base.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/controls.txt`).

**M45-3 — the three tip receipts name the round's second-to-last commit, and no receipt names the tip the round closed
on.** Class: `attribution` (a receipt bound to a revision other than the one the report's sentence attributes it to).
Evidence: at tip `8ac15c41`, `grep -rl 8ac15c41 .ufo/waves/round-44/receipts/` → **0** files, while
`.ufo/waves/round-44/receipts/axis-tip.txt`, `.ufo/waves/round-44/receipts/c1-after-tip.txt`, `.ufo/waves/round-44/receipts/c2-after-tip.txt` all carry `rev=74c606a1c7fd52a6bb85bb1c786529c926040c73`
(`.ufo/waves/round-45/w1/ScrMistakes/receipts/d3-d4-tip-and-share.txt`). The equivalence is real but unstated: `git diff --name-only 74c606a1 8ac15c41 | grep -v
'^.ufo/waves/round-44/' | wc -l` → 0 (599 files changed, all inside the round directory —
`.ufo/waves/round-45/w1/ScrMistakes/receipts/d3-equivalence.txt`). Captured-by: criterion 69, partially — it requires the receipt's bytes to name "the revision
the report attributes it to", and the report wrote the token the receipt itself carries (`74c606a`), so the check passes
by construction; criterion 17 (receipt-label precision) names the class but no command reads `*-tip` names against the
closing tip. Fix: measure at the final tip, or write the equivalence line into the receipt (the command and its `0` above),
and land criterion 86. Shown able to fail: `checks.py 86 --repo . --rev 8ac15c41 --round .ufo/waves/round-44` prints
`violations=3` for exactly the three files; the mutant (a tip receipt naming its predecessor with no equivalence
statement) prints `violations=1`, the control whose receipt states the equivalence prints `CLEAN`
(`.ufo/waves/round-45/w1/ScrMistakes/receipts/red-before-base.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/controls.txt`).

**M45-4 — the C1 "before" share was a count of a random draw: the same tool bytes and the same clause vector printed
11/26 and 15/26.** Class: `number-drift`. Evidence: `.ufo/waves/round-44/receipts/c1-v2-before-base.txt` ends
`fixtures=11/26 … rev=6a1a9052… nonce=4a027f783e5442e4` with `clauses=a:1 b:0 b4:0 b5:0 e:1 g:1 r:1`; the freeze control
`.ufo/waves/round-44/receipts/ctl-c1-v2.txt:3` reads `BASE-tool … fixtures=15/26 … rev=e2289516… nonce=729654e70c5fcca2` with the identical
clause vector, and `tools/mado-geometry.py` hashes `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` at
both revisions (`.ufo/waves/round-45/w1/ScrMistakes/receipts/d3-d4-toolhash.txt`), so nothing but the draw differs. The draw is the counter's own default:
`quality/counters/c1-r44-geometry-states-v2.py:410` — `nonce = args.nonce or secrets.token_hex(8)`. Captured-by: `none` —
criterion 65 binds fixtures to a lattice on the tree index, and this counter's fixture count is the *nonce's* product;
criterion 6 (named revision per number) passes because the revision is named. Fix: seed the draw and report the
deterministic part; the round-45 C1 counter does both (`.ufo/waves/round-45/registration.md:20-22`;
`quality/counters/c1-r45-monitors.py:18` "the default seed is 45, so a run without --seed reproduces exactly",
`--seed` default 45 at `:376`). Shown able to fail: criterion 89 (below) prints `violations=1` for the counter the round-44
v1 registration names (`quality/counters/c1-r44-geometry-states.py`, `--nonce default=None`) and `violations=0 verdict=CLEAN`
for the round-45 registration's counters at freeze `22a8dedd` (`.ufo/waves/round-45/w1/ScrMistakes/receipts/red-before-base.txt`); the mutant that reinstates
`--nonce default=None` in a seeded counter prints `violations=1` (`.ufo/waves/round-45/w1/ScrMistakes/receipts/controls.txt`). The two committed counts above
are the empirical red: a "before" number that takes two values is not a count.

**M45-5 — both predicates closed the round with holes the lane had already declared, and the next round bought new
counters instead of inheriting them.** Class: `vacuous`, with a `survivor`. Evidence (all committed at `8ac15c41`):
`w2/CritC1V2Cheat.md:24` — cheat-h (state logic enabled only when the invocation is the counter's) reaches
`26/26 TARGET_MET`; `w2/MutC1V2.md:18` — mutant `M01-b5-rename-wrong-key` survives (`X2-padded-selftest` admitted), and
`:46` states the survivor hangs on one string literal in the counter; `w2/ExecDoNothingV2.md:10-11` — a 27-line entry whose
locators are whole-file ranges is `TARGET_MET` (hole O1); `w2/CritC2V2Forgery.md:11` — "Seven forged entries, all admitted";
`w2/MutC2V2.md:9` — "11 killed, 3 equivalent, 18 survived → classified missing control". The closure booked the same set
(`round-44-verifier-spotcheck.md:114`) and re-registration was the fix. Captured-by: criterion 84 covers the pins half (a
held receipt swapped for a forgery must be rejected, and it was: `.ufo/waves/round-44/receipts/ctl-c2-v2.txt` FORGED-PIN); nothing covered the
locator-width and do-nothing halves, and the r44 M01 survivor is a counter-side drift no control can see. Fix: re-register
before data (done for round 45: no round-44 counter is reused — `registration.md:65`); the C2 predicate now bounds the
locator (`quality/counters/c2-r45-monitor-entry.py:53` "and b - a <= 30", `JWIDTH = 30` at `:91`), and its controls admit P
and reject the nine do-nothing/forged variants (`.ufo/waves/round-45/receipts/ctl-c2.txt`: `VERDICT: PASS (wrong=0 of 10; positive
admitted=1)`); C1's controls score 0 of 16 met with the reference met (`.ufo/waves/round-45/receipts/ctl-c1.txt`). Shown able to fail: the
round-45 C2-BASE control prints `admitted=0/1 verdict=TARGET_MISSED`; criterion 85 (below) is the missing process rule —
its own red is this row's evidence (7 forgeries admitted under a predicate whose residuals were prose). Residual honesty:
the r44 `M01` class (a counter-side hook mis-aim) remains unexposed by any control, and the round-45 registration declares
it nowhere, so criterion 85 as drafted by seat `ConnLessonsPattern` (every residual names a committing input) would fail
this freeze — see the narrowed wording below and the divergence note.

**M45-6 — the registry still says "the client's request as input" two rounds after the round that refuted it, because the
superseding rows were drafted and never landed.** Class: `stale-premise`. Evidence: `corpus/SOURCES.md:242` (S293) titles
the row "the client's request as input"; `corpus/lessons/round-43.md:226-230` records that S290's, S291's, S292's, S293's
and S294's cells are imprecise and that "the next round supersedes the rows with corrected text"; the round-44 seat
`.ufo/waves/round-44/w1/ScrSupersedeRows.md` drafted seven successors S302-S308 with a census study, and
`SCORECARD.md:2590` defers the landing to round 45 ("needs a census-clean supersession form"); `registration.md:65` lists
it as routed, not a claim. Captured-by: criterion 28 (a superseded present-tense value needs an in-file pointer in the same
round) passes here because the sweep walks owned files' values, not registry titles, and CORPUS rule 2 forbids editing
cells 1-9 in place, so the row is allowed to stand until a successor exists. Fix: land the supersessions as new rows whose
`teaches` opens `supersedes S29N —` with the scope cell verbatim (round-45 `w1/ExecSupersede`, rows S311+), and keep the
census variant that was shown load-bearing. Shown able to fail: the round-44 seat's own census table — rows without the
lesson stub print `E11 S302…S308`, exit 1; deleting one `supersedes` opener prints `E04 S304`, exit 1; the recommended
variant prints `E04 0 / exit 0` (`.ufo/waves/round-44/w1/ScrSupersedeRows.md`, census variants m1/m2/m4). Limit: that
evidence is a report table, not a committed census receipt; the lane's `sources-census.sh` run over the landed rows is
still owed, and at this seat's read no superseding row exists in `SOURCES.md`.

**M45-7 — the round-44 lesson cites a mapping file no ref holds, and the LOG statement of its own mistake count is two
short, with the criterion that should catch both passing.** Class: `reference-drift` (with a `number-drift` half).
Evidence: `corpus/lessons/round-44.md:26`, `:71` and `:82` each cite `assimilation/renumber-map.tsv`;
`git ls-tree -r --name-only 0c89478a assimilation/` prints nothing (`.ufo/waves/round-45/w1/ScrMistakes/receipts/d7-paths.txt`), and the round-44
`assimilation/id-guard.md:8` names it too. The criterion that should have caught it does not: `check83.py` reads only
extensions in its `EXT` tuple (`check83.py:25`) which has no `tsv`, so the token is never resolved — the checker prints
`CHECK83: verdict=PASS citations=13 violations=0 outside=7` on the round-44 lesson at base, i.e. a document citing a
path no ref holds scores clean (`.ufo/waves/round-45/w1/ScrMistakes/receipts/d7-check83.txt`); without `--prefix` the same document prints `violations=37`,
noise rather than a targeted red. Second half: `LOG.md:2499` says "(Mistakes M44-1..7, Round-43 errata E1-E4)" while
`grep -c '^\*\*M44-' corpus/lessons/round-44.md` → 9, the same class as M44-5 and D7's F1
(`.ufo/waves/round-44/w2/ConnCalibration.md:17-27`). Captured-by: criterion 83 nominally, but its extension list makes the
`.tsv` case vacuous and its `OUTSIDE` bucket absorbs non-rooted tokens; `none` for the count (criterion 78 counts control
tallies only). Also relevant: criterion 83's own check command names
`.ufo/waves/round-44/w1/ScrQualityCriteria/check83.py`, which did not exist at the data commit `e4678921` and does at base
— the F6 finding of `.ufo/waves/round-44/w2/ConnCalibration.md:70-76`. Fix: append-only errata naming the real mapping
(`corpus/SOURCES.md`'s id guard and the round-44 lesson's own `## Registry changes` block, no file needed), recompute the
LOG count or date it to protocol load, and widen criterion 83's token rule to any backticked repo-relative path with a
`/` and an extension not in a short prose allowlist — with a fixture that carries `assimilation/renumber-map.tsv`.
Shown able to fail: the `check83` run above is the red (a PASS on a document whose cited path is absent), and the count
red is the `grep -c` pair. No fix is landed at this seat's read (`w1/ScrErrata` in flight).

## Criteria proposed for `corpus/QUALITY.md` (last is 84; numbers aligned with seat `ConnLessonsPattern`)

Numbering note: seat `ConnLessonsPattern` (`w1/ConnLessonsPattern/patterns.md:75-98`) proposes 85 = open-predicate
residuals, 86 = tip receipts, 87 = session material. This draft keeps those three numbers and adds two for the defects
that proposal does not cover, so each criterion cites a row above and each row cites a criterion.

**85. A predicate's declared residual is a kill rule or it is not a residual.** Text: a registration that declares
residuals names, for each residual that describes a tool-side or forgery-side way to reach the target, the control or
fixture that exposes it and the receipt line showing it `TARGET_MISSED`; a residual that no input can expose says why (a
counter-side drift, a missing host surface) and is not counted as covered. Check: the round's controls receipt — every
declared residual class has one row below target, and a residual naming no control is printed `UNBOUND <residual>`.
Shown able to fail: the round-44 v2 predicates declared O1 and the M01 class and both survived their own controls
(`w2/ExecDoNothingV2.md:10-11`, `w2/MutC1V2.md:18`); round 45's C2 clause-j width bound is the repair
(`c2-r45-monitor-entry.py:53`, controls `.ufo/waves/round-45/receipts/ctl-c2.txt` reject 9 of 10). Divergence from
`ConnLessonsPattern`'s wording: "every residual names a committing input" would fail the round-45 freeze, whose C1
residuals ("a tool holding a model of the contract is an implementation of it") are unexposable by construction; the
narrowed text above admits that case only with a stated reason. (lesson: lessons/round-45.md#mistakes M45-5)

**86. A receipt whose name says tip carries the closing tip.** Text: a receipt named `*tip*` that a round cites contains
`rev=<closing tip>` in its own bytes, or states the equivalence and the command proving it — `git diff --name-only
<receipt rev> <tip>` empty outside the round's own directory. Check:
`python3 -I .ufo/waves/round-45/w1/ScrMistakes/checks.py 86 --repo . --rev <tip> --round .ufo/waves/round-<N>`; each violating file
prints `86 VIOLATION <path> names=<revs> tip=<hex>`. Shown able to fail: three round-44 tip receipts print
`violations=3` at `8ac15c41`; the control with the equivalence line prints `CLEAN`; the mutant (predecessor named, no
equivalence) prints `violations=1`. Extends criterion 69, which passes when the report writes the receipt's own revision.
(lesson: lessons/round-45.md#mistakes M45-3)

**87. Session material stays shape-only in committed bytes.** Text: no tracked file carries window `title`/`initialTitle`,
`pid`/`stableId`/`xdgDescription`/`xdgTag` inside a client dump, a non-empty `instance_sig`, or non-empty monitor
`serial`/`description`/`make`/`model`; a live dump is projected to `address, at, class, floating, mapped, monitor, size`
before commit, and a fixture that needs an identity field says so with a synthetic value. Check:
`python3 -I .ufo/waves/round-45/w1/ScrMistakes/checks.py 87 --repo . --rev <rev>`; `87 VIOLATION <path> R1 identity_keys=…|R3
instance_sig len=…|R4 monitor_identity_keys=…` lines. Shown able to fail: 77 rows over 26 files at the round-45 base
(the two the closure named, 18 ExecOracleGkeep receipts, round-44's own two demo clients); the projected control prints
`CLEAN`; one added `title` key prints `violations=1`. Rule source: `SKILL.md:343`; considerthese `2026-10-26.md`
proposal 1. (lesson: lessons/round-45.md#mistakes M45-1)

**88. A published claim row carries its own after value and verdict.** Text: every `| C<n>` row of a SCORECARD round
section states the after measurement in the `Before -> after` cell (the counter's line form, `k/n`, `TARGET_MET|MISSED`)
and the self-verdict column carries the verdict token; a cell that only points at a receipt is a landing defect even when
the receipt exists. Check: `python3 -I .ufo/waves/round-45/w1/ScrMistakes/checks.py 88 --repo . --rev <rev>`; `88 VIOLATION
SCORECARD.md:<line> after='…'`. Shown able to fail: 4 rows at the round-45 base (Round 43's two and Round 44's two);
the corrected control prints `CLEAN`; the pointer-only mutant prints `violations=1`. (lesson:
lessons/round-45.md#mistakes M45-2)

**89. A before/after number is a count only if it reproduces.** Text: a counter whose fixture set, names or inputs are
drawn at random names its seed in the output line, defaults that seed to a value the registration states (so a bare run
reproduces), and reports the deterministic part (clauses) beside the share whenever the share depends on the seed; a
receipt line carrying `nonce=` with no seed and no fixed default is not a before-state. Check:
`python3 -I .ufo/waves/round-45/w1/ScrMistakes/checks.py 89 --repo . --rev <rev> --registration .ufo/waves/round-<N>/registration.md`
— a counter the registration names whose `--nonce`/`--seed` defaults to `None` prints `89 VIOLATION <path>`. Shown able to
fail: the round-44 v1 counter prints `violations=1` under its own registration; the round-45 registration's counters print
`CLEAN` at freeze `22a8dedd`; the empirical red is 11/26 vs 15/26 with identical tool bytes and clause vector.
(lesson: lessons/round-45.md#mistakes M45-4)

**Applications, not new numbers.** D6/M45-6 is criterion 28 applied to registry cells (the sweep must now include title
cells of a row the round's own reading refutes), and D7/M45-7 is criterion 83 extended, not renumbered: its `EXT` allowlist
(`check83.py:25`) currently makes a `.tsv` citation invisible, so the criterion's own check command needs the widened token
rule before it can be cited as a gate. Both appends should be written into the criteria's existing blocks, in the
`QUALITY.md` style ("Applications, not new numbered criteria", `corpus/QUALITY.md:300`).

## Counts recomputed by this seat

| number | command | observed |
|---|---|---|
| round-44 mistakes carried | `grep -c '^\*\*M44-' corpus/lessons/round-44.md` | 9 (LOG says `M44-1..7`) |
| tip receipts naming the tip | `grep -rl 8ac15c41 .ufo/waves/round-44/receipts/ \| wc -l` | 0 (three name `74c606a`) |
| equivalence of the named rev | `git diff --name-only 74c606a1 8ac15c41 \| grep -v '^.ufo/waves/round-44/' \| wc -l` | 0 (599 files, all in the round dir) |
| tool bytes at base and freeze | `git show <rev>:tools/mado-geometry.py \| sha256sum` | `e3c2e471…` at both |
| C1 before share | `.ufo/waves/round-44/receipts/c1-v2-before-base.txt` / `ctl-c1-v2.txt:3` | 11/26 (nonce 4a027f78…) vs 15/26 (nonce 729654e7…) |
| tracked identity fields | `checks.py 87 --rev 0c89478a` | 77 rows / 26 files (20 R1 files, 22 R3 files) |
| claim rows without an after value | `checks.py 88 --rev 0c89478a` | 4 (`SCORECARD.md:2480,2481,2570,2571`) |
| counters drawing a fresh nonce | `checks.py 89 --rev <freeze> --registration …` | 1 (r44 v1) / 0 (r45) |
| `assimilation/` file count | `git ls-tree -r --name-only 0c89478a assimilation/ \| wc -l` | 0 |
| check83 on the round-44 lesson | `check83.py --prefix .ufo/` | `verdict=PASS citations=13 violations=0` (the `.tsv` cite is invisible) |
| draft census variants | `.ufo/waves/round-44/w1/ScrSupersedeRows.md` table | m1 `E11` exit 1, m4 `E04` exit 1, m2 exit 0 |

## Not done, and limits of this draft

- No lane file was edited: the lesson, `SCORECARD.md`, `QUALITY.md`, `SOURCES.md` and the round-43 dumps are the L1's or
  the operator's to change. Rows M45-1..7 are text; criteria 85-89 are proposals with checkers that live in this seat
  directory.
- The row-4 fix (criterion 89) is already satisfied by the round-45 C1 counter; M45-1/2/3/6/7 have in-flight seats
  (`ExecProjectTitles`, `ExecPrivacyGate`, `ExecSupersede`, `ScrErrata`) whose work I read only as status lines, so no
  green is claimed for them. The checkers' red states are measured on committed bytes at `0c89478a` / `8ac15c41`.
- Criterion 87's key set is a lane decision, not a measurement: `pid`/`stableId`/`xdgTag` are identity-ish fields I would
  drop, while a fixture author may argue for keeping `pid` on synthetic windows. The rule as written fails on any of them.
- Criterion 85's divergence from `ConnLessonsPattern`'s text is recorded rather than resolved; the L1 should pick one
  wording, and the narrowed one is what the round-45 freeze can pass.
- The M45-6 census evidence is a report table, not a receipt; criterion 79 would call it a lead, and the landing owes a
  committed `sources-census.sh` run.
- Not mined here (no evidence found or out of the seat's assignment): M44-1's reason-coverage class (the round-44 lesson
  calls it its own first criterion candidate), M44-5's seat-count recompute beyond the LOG half, and any live host claim.

## Evidence in this seat directory

- `checks.py` — proposal checkers 86-89 (read-only, revision-addressed); `mutants.sh` — the control driver.
- `.ufo/waves/round-45/w1/ScrMistakes/receipts/red-before-base.txt` — the four checks red on committed bytes (`87`, `86`, `88`, `89`), plus `89` CLEAN on the
  round-45 registration at the freeze.
- `.ufo/waves/round-45/w1/ScrMistakes/receipts/controls.txt` — pristine control `CLEAN` for all four, then one single-defect mutant per check printing `FAIL`.
- `.ufo/waves/round-45/w1/ScrMistakes/receipts/d1-session-material.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/d1-shapes.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/d1-nested-paths.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/d1-sweep-classify.txt` — D1 counts and the
  shape-only classification (no title, serial or signature value is reproduced in any file of this seat).
- `.ufo/waves/round-45/w1/ScrMistakes/receipts/d2-d6-scorecard.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/d3-d4-tip-and-share.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/d3-d4-toolhash.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/d3-equivalence.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/d4-nonce.txt`,
  `.ufo/waves/round-45/w1/ScrMistakes/receipts/d5-predicate-defects.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/d5b-c2-defects.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/d6-supersede-rows.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/d7-conncalibration.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/d7-paths.txt`,
  `.ufo/waves/round-45/w1/ScrMistakes/receipts/d7-check83.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/fixes-round45.txt`, `.ufo/waves/round-45/w1/ScrMistakes/receipts/green-round45-freeze.txt`.
- No host command was run by this seat; no compositor verb beyond the files above; no tool installed; scratch
  (`/fast/scratch/hyaku/mado-r45/ScrMistakes/`) deleted by the drivers' `trap`.
