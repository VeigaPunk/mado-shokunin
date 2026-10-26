# Round 47 lesson — the terminal selection chain (2026-10-26, hyaku run 9)

Lane mado-shokunin. Claims (`.ufo/waves/round-47/registration.md`, freeze `d7527d608ad2b2e3cc398fdde34db7947b254a1a`, base
`60edb66e2f1cb90acc6e9442fc93ded0ca42d750`): C1 operability (capability acquisition) `tools/mado-terminal.py`, judged by
`PRED-C1-r47`; C2 coverage (sourced) `corpus/knowledge/xdg-terminal-selection-r47.md`, judged by `PRED-C2-r47`. Round shape:
two v1 waves, `w1` build (41 seats) and `w2` falsify (44 seats). Seat drafts used here: `w1/ScrLesson` (shape), `w1/ScrRows`
and `w1/ScoutSpecs` (rows, gates, rejects), `w1/ScrMistakes` (mistakes, criteria 91-95), `w1/ExecSupersede` (R4a).

## Gate

Access date 2026-10-26 for every line; each quote is <= 25 words, located by `grep -n` on the committed pin.

- GATE S326 admit, tier A, code — https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec, pin
  `.ufo/waves/round-47/fetch/xdg-terminal-exec` sha256 89f2be9a..., byte-equal to the host `/usr/bin/xdg-terminal-exec`; quote
  "Entries are checked in ascending order of preference, so use last found if duplicate" (xdg-terminal-exec:780).
- GATE S327 admit, tier A, docs — https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md, pin
  `fetch/README.md` sha256 c7a1a8bb...; quote "Valid cache bypasses" (README.md:300) - the sentence continues on :301.
- GATE S328 admit, tier B (an unmerged proposal), spec — https://gitlab.freedesktop.org/terminal-wg/specifications/-/raw/64c429dfaf442d4a7ca9a656baf91a1b2d9c1a4d/proposals/xdg-terminal-exec.md,
  pin `fetch/xdg-terminal-exec-proposal.md` sha256 c16a717a...; quote "presense of `TerminalEmulator` category"
  (xdg-terminal-exec-proposal.md:159, source spelling).
- GATE S329 admit, tier A, spec — https://gitlab.freedesktop.org/xdg/xdg-specs/-/raw/a0eaad5cc900684519030ceb568f7053dc315fe6/desktop-entry/desktop-entry-spec.xml,
  pin `fetch/desktop-entry-spec.xml` sha256 a1baadee...; quote "If multiple files have the same desktop file ID, the first one in the"
  (desktop-entry-spec.xml:164).
- GATE S330 admit, tier A, code — https://raw.githubusercontent.com/omacom/omarchy/6aa2aec1c035d50cfb6871d490cdf9a1169f5ac3/applications/Alacritty.desktop
  (tag v3.8.3), pin `fetch/omarchy/omarchy-Alacritty.desktop` sha256 713703ba..., byte-equal to the host user override; quote
  "X-TerminalArgDir=--working-directory=" (omarchy-Alacritty.desktop:17).
- GATE S331 admit, tier A, code — https://raw.githubusercontent.com/omacom/omarchy/6aa2aec1c035d50cfb6871d490cdf9a1169f5ac3/config/xdg-terminals.list,
  pin `fetch/omarchy/omarchy-xdg-terminals.list` sha256 d035da57..., byte-equal to the host list held at S059; quote
  "Alacritty.desktop" (omarchy-xdg-terminals.list:3).
- GATE S332-S339 admit (supersession of S290-S297, R4a) — rows and quotes from `.ufo/waves/round-47/w1/ExecSupersede/rows.md` §3-§4,
  renumbered by document from the seat's S346-S353 to S332-S339 (map below), pins re-fetched by the seat on 2026-10-26.
- REJECT xdg-specs MR !87 (desktop-entry TerminalExecuteArguments) — a competing draft key the resolver does not read
  (`w1/ScoutSpecs/sources.md:151`). Flip: a release of xdg-terminal-exec that reads it.
- REJECT desktop-entry-spec `latest` and xdg-specs `master` as anchors — moving targets; HEAD 9b8a085 already differs from 1.5 in the
  field-code sentence (`w1/ScoutSpecs/sources.md:154`). Flip: none; a pinned commit is the anchor.
- REJECT XDG Base Directory spec (drafted as S332 by `w1/ScrRows`) — the entry cites the script's own defaults (:148, :157, :166),
  so a basedir row would be cited by nothing (CORPUS rule 4). Flip: an entry sentence that rests on the basedir text.
- REJECT man page `xdg-terminal-exec.1.scd`, `test/tests.bats`, omarchy `omarchy-default-terminal` and
  `omarchy-cmd-terminal-cwd`, host-bytes rows (drafted S328/S329/S335-S338) — opened and pinned (`fetch/`), but no sentence of the
  admitted entry rests on them; the C1 fixtures, not the upstream tests, are the executed evidence. Flip: the launch-half entry
  (the `--dir` helper) or a test-suite comparison claim.
- REJECT (assimilation) every staged `merge/mado/` theme for this plane — `w1/ScoutShokuknow.md` A0: no staged theme touches
  terminals, desktop entries or xdg-terminal-exec (grep over MERGE-REPORT.md, SOURCES.append.md and 69 knowledge files: no match).

Renumber map (R4a, by document - each row's URL is unchanged, only the id): S346→S332 (RegexMatchEngine.cpp), S347→S333
(DefaultFloatingAlgorithm.cpp), S348→S334 (Target.cpp), S349→S335 (WindowTarget.cpp), S350→S336 (GeometricMovableAnimated.cpp),
S351→S337 (host-clients-r43.json), S352→S338 (gkeep-ui-excerpt.py), S353→S339 (Rule.cpp).

## Registry changes

| surface | old (base `60edb66e`) | new |
|---|---|---|
| `corpus/SOURCES.md` | 262 rows, top S325 | 276 rows: S326-S331 (C2, mined, opened 2026-10-26) and S332-S339 (supersession of S290-S297) appended; no row deleted or edited |
| `corpus/knowledge/` | 63 entries | 64 (`xdg-terminal-selection-r47.md`) |
| `corpus/README.md` | 63 index rows | 64; Frontier bullet for round 47 |
| `tools/` | 14 files | 15 (`mado-terminal.py`) |
| held rows S056-S060, S290-S297 | as at base | byte-identical (C2 clause h; supersession is append-only) |

Census command (both ends): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`.
Before: `.ufo/waves/round-47/receipts/census-before.txt` (W04 x14, W01 x1, `mado ok`, exit 0). After: `receipts/census-after.txt`
(@AFTER@).

## Search log

Question: which desktop entry does `xdg-terminal-exec` 0.14.3 select on SUPER+RETURN and by which executed rule? Searched the tag
(script, README, man page, tests), the terminal-wg proposal at MR 3, the xdg-specs desktop-entry text at a pinned commit, omarchy v3.8.3
(the host's deployed list and override), and the lane registry (S056-S060, S071 hold the documentary route and host bytes).
Screened 14 candidates (`w1/ScoutSpecs/sources.md`, `w1/ScrRows/rows.md`); admitted 6 for the entry; rejected the rest above. Stop:
every chain step has a pinned script line and an executed C1 fixture; reopen when the host resolver leaves 0.14.3.

## Mistakes

**M47-1** · class `provider` · evidence: the round-46 entry attributes the *landed* tool's live run to the pre-landing
draft's receipt. Entry `corpus/knowledge/hyprland-input-devices-r46.md:57` (`1001bda`, unchanged at HEAD) cites
`.ufo/waves/round-46/receipts/live-devices-host-l1.txt`; that receipt's own bytes name its producer at `:1` —
`l1-draft/mado-devices.py`, sha256 `b229efd0…` — and the landed tool `tools/mado-devices.py` at the same commit hashes
`3a80368997120503d5715596a17e762bbcb67a41db23d9241425bf19349d594f` (`git show 1001bda:tools/mado-devices.py | sha256sum`),
which is the producer named by the *other* receipt, `live-devices-host-r46.txt:1`. The sentence also says "one `input`
block in `~/.config/hypr/input.conf`" while the landed run's header names two configs with the omarchy default first
(`live-devices-host-r46.txt:3-5`, the same two-config order the closure recorded). Receipts:
`receipts/r1-producer.txt`, `receipts/r1-entry-locator.txt`. This is M46-5's class recurring in the very round that
mined it — the criterion was applied to the round-45 entry and not to the new one. ·
captured-by: 24 — applied by the round-46 non-author closure (`corpus/lessons/round-46-verifier-spotcheck.md:52` calls it
a "defect R1"), **missed by the lane's own quality control**: the C2 counter's clause j binds a locator and a keyword per
surface, not the truth of a sentence, and the docstring declares that residual (M46-11, M46-5). ·
fix: append an erratum under the entry citing `live-devices-host-r46.txt`, and correct the sentence's config count (the
landed run reads the omarchy default and the user file); the round's own QC runs the producer check before the data
commit, not only a later closure. Shown able to fail: `python3 -I .ufo/waves/round-47/w1/ScrMistakes/check91.py --repo .
--rev 1001bda… --entry corpus/knowledge/hyprland-input-devices-r46.md --tool tools/mado-devices.py` reads
`PRODUCER …live-devices-host-l1.txt producer=l1-draft/mado-devices.py … verdict=DIFFER` / `CHECK91: … verdict=DIFFER`,
exit 1, and the same command on the one-line-corrected entry (`corrected-entry.md`, `sed` of the receipt name, `diff` in
`receipts/check91-run.txt`) reads `verdict=AGREE`, exit 0.

**M47-2** · class `landing` · evidence: R2 is round-45 D4's class again — evidence produced for a round and still not
committed a round later.
`GIT_OPTIONAL_LOCKS=0 git status --porcelain` at HEAD prints
`?? .ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv`; the file is 3 282 451 B; `git ls-files` over that
seat names 18 paths and not it; the seat directory's last commit is `7f793280`, and the round-46 report disclosed it
(`.ufo/reports/round-46/mado.md:55`). The report's own explanation, "The helper skips new files over 1 MiB inside a named
directory", mis-places the mechanism: the size cap is **jj's** `snapshot.max-new-file-size` (default 1 MiB), and it is not
silent — reproduced in a scratch repo (`receipts/jjfix-receipt.txt`): `jj file track -- root:"sub"` prints
`Warning: Refused to snapshot some files:` / `sub/big.bin: 2.0MiB (2097152 bytes); the maximum size allowed is 1.0MiB
(1048576 bytes)` plus four remedies, and `jj diff --summary` then stages only the small file. So the signal naming the
file, its size and the limit existed at the moment of the commit and was not acted on; `scripts/hyaku/jj-lane.sh:638` has
a 10 MiB rule for *named* files only, and the fleet addendum (`scripts/hyaku/lane-addendum.md:274-275`) states the 1 MiB
directory rule ("are skipped with a warning — name them as files"). Receipts: `receipts/r2-state.txt`,
`receipts/jjfix-receipt.txt`, `receipts/check92-run.txt`. ·
captured-by: 13 (evidence meant to outlive a round is a committed path) and 14 (a census names both sets — here the
produced set and the committed set of one seat directory, which no instrument compared). ·
fix: commit a digest line (sha256, size, row count) beside the seat's `out.json` and remove the working file, or track it
with `jj file track --include-ignored`; and every seat directory is inventoried against its tip before the round commits.
Shown able to fail: `python3 -I .ufo/waves/round-47/w1/ScrMistakes/check92.py --repo . --rev HEAD --dir
.ufo/waves/round-46/w1/ExecStofOracle` reads `UNCOMMITTED 3282451 …out.json.rows.tsv` /
`worktree=19 tracked=18 uncommitted=1 uncommitted_bytes=3282451 verdict=DIFFER`, exit 1, while the same command on
`…/w1/ExecSerialRule` (17/17) and `…/w1/ExecSupersede` (23/23) reads `verdict=OK`, exit 0.

**M47-3** · class `vacuous` · evidence: the round-46 gate landed with its red state pre-authorised, so its red proves
nothing. `SKILL.md:770` registers `mado-session-material` and its notes cell ends "no synthetic marker yet, so a red exit is
expected until it lands"; the round's only receipt for it reads
`SESSION_MATERIAL: files=18363 findings=115 rev=1001bda…` / `exit=1`
(`.ufo/waves/round-46/receipts/session-material-data.txt`, committed at `9879964`), and the gate is still red at the
round-47 base: `python3 -I quality/check-session-material.py --repo . --rev HEAD` prints
`SESSION_MATERIAL: files=18377 findings=115 rev=c24adef2…`, exit 1 (`receipts/session-material-head.txt`; it reads committed bytes at HEAD, where 0 of the
115 findings are in round-47 files — the count moves at that round's data commit, which is the point). A gate whose spec says "red is expected" cannot fail under its own spec — the
criterion-56 shape applied to the gate registry instead of to a counter clause. The marker and the prose serial rule were
drafted and committed (`.ufo/waves/round-46/w1/ExecSessionTriage/`, `…/ExecSerialRule/`) and not installed. ·
captured-by: 56 (a clause that cannot fail under its own spec is dead code — extended here to a registry cell), with 30
adjacent (a detector credited is admitted only beside its precision evidence; the gate's own false positives were
untriaged at the data commit). ·
fix: install the drafted marker (and the R5/R6 prose rules), re-run the gate to `findings=0` at the round-47 tip, and
replace the waiver sentence in `SKILL.md:770` with the clean-state receipt. Shown able to fail: the two sides are already
committed as seat receipts — `…/ExecSessionTriage/receipts/04-marked-49.txt` (base 97 → 48 with 49 waived),
`…/06-planted-real-dump.txt` (a planted real dump still flagged) and `…/07-tampered-waived-fixture.txt` (a tampered waived
fixture re-flagged) — so after install the gate must read `findings=0` on the marked set *and* still flag the planted
dump; today's receipt is red with the waiver standing, which is the red state of the fix.

**M47-4** · class `landing` · evidence: the S290-S297 supersession is deferred a **fourth** time. Registry at HEAD:
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 262 rows, last id `S325`, and
`grep -cE '^ {0,3}\|[[:space:]]*S3(2[6-9]|[3-9][0-9])[[:space:]]*\|'` → 0, so the drafted S326-S333 rows are still not
landed although `.ufo/waves/round-46/w1/ExecSupersede/rows.md` (committed `7f793280`) carries them census-clean; the ages
ledger has kept it open since round 43 (`.ufo/waves/round-46/w1/ScrRoutedAges/ages.md:55`, first routed `S43:100`).
The same route also still carries the round-45 entry's six non-supported sentence units and the round-44
`w2/ConnCalibration` errata. Receipt: `receipts/r4-deferral.txt`. ·
captured-by: 90 (registered this round at `QUALITY.md:454`; round 47 is the first round in which it can bite, and it does:
the item is past its third routing). ·
fix: land the drafted rows under round-47's own registration before any new claim, and land the two errata; the ages
ledger is recomputed at the round-47 tip. Shown able to fail: the two count commands above read `262` / `S325` / `0` at
HEAD — a landed supersession moves all three — and `age` is emitted by the ledger, not typed (see M47-5).

**M47-5** · class `number-drift` · evidence: two hand-carried numbers disagree with the instruments they cite, both by one.
(a) The lesson says the S290-S297 supersession's "age now 4 rounds (`w1/ScrRoutedAges/ages.md` R43-D2)"
(`corpus/lessons/round-46.md:311`), while the ledger it cites defines `age = 46 − first_routed_round`
(`ages.md:14-15`; a round-45 item has age 1, a round-38 item age 8) and prints **3** for R43-D2 in its own age column
(`ages.md:88`). 46 − 43 = 3; the lesson's 4 is the round-47 exclusive value or a 5-round inclusive count, i.e. it uses a
convention the ledger does not state. (b) The closure's routing text calls round 47 the "third deferral"
(`corpus/lessons/round-46-verifier-spotcheck.md:116`), while M46-16 already records round 46 as the third slip
("slips a third time", `corpus/lessons/round-46.md:307-308`), so round 47 is the fourth; the deferral sites are r44:93,
r45:68, r46:307-308 and r47:116. Receipts: `receipts/age-drift.txt`, `receipts/ages-derive.txt`. ·
captured-by: 10 (each count as `<n> — <command> <date>`, rederived from the named revision) and 14 (a census names both
sets; here the two readings of the same interval). ·
fix: an appended errata states the convention it uses ("3 round boundaries, the fourth round in which the item is
carried") and cites the ledger's cell or the ledger emits the sentence; a deferral count is derived from the round number
and the first-routing round by the same command. Shown able to fail: `python3 -c 'first=43; now=47; print(now-first)'
` → 4 (the ledger's rule at round 47) against `ages.md:88`'s **3** at round 46, and `grep -n` over the four deferral sites
prints four lines — so a typed "4" at round 46 and a typed "third" at round 47 each contradict their own citation by one.

**M47-6** · class `landing` · evidence: M46-13's fix landed on two of the three counters, and the bytecode artifact is
back in the tree the counters score. `quality/counters/c1-r46-devices-v3.py:76` and `…-v2.py:69` carry
`sys.dont_write_bytecode = True`; `quality/counters/c1-r46-devices.py` (v1, still committed and still the version the
earlier receipts cite) carries none (`grep -c dont_write_bytecode` → 0), and it imports the model in-process from the live
worktree (`c1-r46-devices.py:67-68`, `:98`). A pyc sits in the frozen round-46 tree at
`.ufo/waves/round-46/l1-draft/__pycache__/mado-devices.cpython-314.pyc` — 40 149 B, mtime
`2026-10-26T18:45:35.561-03:00` (written after the round-46 tip, whose last commit is `edc14789` 18:26:38), hidden from `git status` by `.gitignore:3`,
and its header's source mtime/size equal the frozen model's (`27743` B), so it was compiled from that model. `[INFERENCE]`
the writer was an unguarded in-process import: the guarded import leaves no directory, a subprocess run of the model
leaves none either, and this seat ran no such import (its only import was of a scratch copy). Mechanism reproduced in scratch: the same import with the guard writes no
`__pycache__`, without it writes one (`receipts/pyc-header.txt`, `receipts/pyc-state.txt`). ·
captured-by: **none** — criteria 13 and 63 govern committed evidence, not an instrument's own ignored write into the tree
it scores; M46-13 recorded the same gap. ·
fix: every counter imports the pinned model from a copy under its `--work` (the pin already fails closed on byte drift, so
the copy costs nothing), v1 gets the guard or is retired, and a run's receipt carries a before/after inventory of the
scored tree. Shown able to fail: the before/after inventory around one run — the unguarded import creates
`__pycache__/mado-devices.cpython-314.pyc` beside the model, the guarded one leaves the directory absent
(`receipts/pyc-header.txt`), and the frozen tree's own pyc (above) is the red state the inventory names by path, size and
mtime.

---

**M47-7** · class `provider` · evidence: w1 seat ExecRefB's shell wrote "x\n" into a scratch file until it reached ~590 GB and took
/fast from 26 % to 83 % (orchestrator incident notice, 2026-10-26 18:59-19:05); the seat was cancelled. Cause fits the
resolver's own option loop (an empty argv element is never shifted, xdg-terminal-exec:1224-1322). Captured-by: none (the wave
context bounded scratch size in words only). Fix: the w2 context requires bounded writers and forbids empty argv elements; the
landed tool refuses an empty argument with exit 2 (shown able to fail: `print --print-id ""` exits 2, `MADO_TERM_OUT_OF_CONTRACT`).

**M47-8** · class `provider` · evidence: a w1 run rewrote the host cache `~/.cache/xdg-terminal-exec` at 18:49 without redirecting
`XDG_CACHE_HOME` (orchestrator relay from w1/RevengerUwsm; content unchanged). Captured-by: the w1 context rule (every resolver
run sets `XDG_CACHE_HOME` into scratch) - stated but not enforced. Fix: the C1 counter and every L1 probe pass a fresh cache dir
per run (counter `case_env`); a host-cache write is a host mutation, mined here.

**M47-9** · class `scope` · evidence: the w1 draft of the C2 counter (`w1/ExecCounterC2/c2-r47-terminal-entry.py` clause f) re-ran
`tools/mado-terminal.py`, so C2 could not verify without C1 (AXES separability). Captured-by: AXES.md causal separability; caught
by the L1 before the freeze (`registration.md` "C2 separability"). Fix: clause f binds the entry to the resolver's own capture;
shown both ways by `w2/ExecSeparability.md` (tool-only tree C2 missed, entry-only tree C2 met).

**M47-10** · class `reference-drift` · evidence: the frozen C1 contract stated `find -L <dir>/. -type f` for every application dir
and rejected every `-`-prefixed `command -v` name; `w2/ExecC1Diff.md` H1/H2 showed the script applies `-type f` to the first dir
only (implicit `-a` binds tighter than `-o`, x:766-774) and that bash parses `-p`, `-v`, `-V`, `--` as `command`'s own options
(exit 0). The 190 fixtures held no non-regular path and no option-like Exec word, so the frozen counter could not see it.
Captured-by: none. Fix: the landed tool models both (`.ufo/waves/round-47/receipts/h12-check.txt`: 32 pin-judged cases, diff 0);
the fixture gap is routed to round 48 (non-regular paths and option-like words in the fixture schema).

Criteria landed: QUALITY 91-95 (`corpus/QUALITY.md`), drafted by `w1/ScrMistakes`, attacked by `w2/CritMistakes`.

## Round-46 closure items (`corpus/lessons/round-46-verifier-spotcheck.md` section 6)

| item | landing this round | evidence |
|---|---|---|
| R1 | erratum appended to `corpus/knowledge/hyprland-input-devices-r46.md` (append-only), framing corrected after `w2/ExecErrataR1` (two sentences WRONG as drafted) | `w1/ScrErrataR1/erratum.md`, `w2/ExecErrataR1/verdicts.md` |
| R2 | the untracked 3.3 MB tsv removed after a digest | `.ufo/waves/round-47/receipts/r2-removed.txt`, `w1/ExecR2Digest/digest.md` (re-derived by `w2/ExecR2Check`) |
| R3 | **not installed** this round: the marker gate is drafted and attacked (`w1/ExecSessionMarker`, 63/63 selftest; `w2/MutSessionMarker`, `w2/RevSessionMarker`) but replacing the registered gate plus 49 sidecars did not fit the round; routed again (fourth age) | seat dirs |
| R4a | S290-S297 superseded by S332-S339 (append-only, renumbered by document from the seat's S346-S353) | `w1/ExecSupersede/rows.md`, `w2/RevSupersede.md` (landable), `w2/ExecRegistryMirror.md` |
| R4b | **not appended**: 6/6 erratum subjects confirmed, but the drafted block turns the frozen round-45 admission counter to TARGET_MISSED (`w2/ExecErrataR45.md` H1); routed with that blocker | `w1/ScrErrataR45/`, `w2/ExecErrataR45.md` |
| R4c | six erratum lines + N1 appended to SCORECARD Round 47 | `w1/ScrErrataCal/errata.md`, `w2/ExecErrataCal.md` (6/6 reproduce) |

## considerthese

`considerthese/2026-10-26.md` proposal 2 (a running ledger of live-state tools) was drafted as a README ledger (`w1/ScrToolLedger/ledger.md`) and attacked by `w2/ExecToolLedger.md`, which found wrong rows (outcomes, a journal unit name, quote fragments); refused this round with that reason, flip: a ledger whose rows the check re-derives with 0 wrong. Lands as this lesson line, citing `considerthese/2026-10-26.md`.

## Assimilation

Assimilation: none. `w1/ScoutShokuknow.md` A0 found no staged theme on the terminal-selection plane (0 admit); the id guard
(`.ufo/waves/round-47/assimilation/`, `w1/ExecIdGuard.md`) reads 262 registry ids, 147 staged ids S203-S349, 70 collisions, and
was proven on an indented `  | S002 |` fixture (nonempty `collisions`); any later adoption renumbers by document first. Quarantine
slice: `assimilation/quarantine-slice` 13 data rows (S189, S195, S201, ... all `payload-absent`); none appended and none hand-checked this round, so all 13 stay quarantined.

## Frontier

1. Registry curation: rows above; no status/recheck/used-by change to a held row.
2. Census: before/after above.
3. Mined mistakes: `## Mistakes`.
4. Sourced claim: C2 rests on S326-S331, opened this round.
5. README Frontier bullet for round 47 (`corpus/README.md`).
