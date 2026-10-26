# QUALITY criteria 77–80 — draft (round 43, w1, seat ScrQualityCriteria)

Append after criterion 76 (`corpus/QUALITY.md:399`, the file's last line; `grep -c '^[0-9]\+\. ' corpus/QUALITY.md`
prints `76`). No renumbering; criteria 6–76 stay byte-identical. A suggested section heading, because criteria 69–76
currently sit under the stale `## Grounding repair (round 30 …)` heading (`QUALITY.md:338`) with no round-41/42 heading of
their own:

```
## Criteria from the round-42 mistakes (round 43; closure §6.2–6.4 and the excerpt header)
```

Every criterion below is drafted in the file's own style — rule, mistake class, `Check:`, `Shown able to fail:`,
`(lesson: …)` — and every claim in it was re-derived this seat from committed bytes. The transcript is
`receipts.txt` (commands and outputs, `bash run-checks.sh` re-derives it) plus `receipts-checkers.txt` (the three
checkers below, run in both directions). Nothing here writes the lane; the checkers read git objects only.

## Grounds: four mistakes, each with the pointer that carries it

| # | mistake (round 42) | evidence pointer |
|---|---|---|
| 77 | locators typed into prose: `Hyprland-HyprCtl.cpp:394-395,412-413` for a fact at `:427-428` and `:448`; `Hyprland-RegexMatchEngine.cpp:10-16` for `:7-8` (`negative:`) and `:16` (`FullMatch`) | `.ufo/waves/round-42/registration.md:61`; `LOG.md:2483` (correction appended at `LOG.md:2487`); fleet report `.ufo/reports/round-42/mado.md:10` |
| 78 | one tally, three numbers under two definitions (`controls=46` by `len(jobs)-2`, `0 of 47` by `len(jobs)-1`, and a claim breakdown that includes the base anchor and drops one mutant) | `.ufo/waves/round-42/receipts/ctl-c1.txt:1` and its last line; fleet report `.ufo/reports/round-42/mado.md:28`; definition site `.ufo/waves/round-42/ctl/run-c1-controls.py:139` |
| 79 | SHONEN box 2 points at a prose section that does not carry the run it claims | fleet report `.ufo/reports/round-42/mado.md:45`; `git show a62f2e0:LOG.md \| sed -n '/^## Round 42/,/^## Round 43/p' \| grep -c NO_MATCHING_CLIENT` → `0` |
| 80 | excerpt header claims a range that cannot be true of its own file and one extra blank line in the body | `.ufo/waves/round-42/fetch/gkeep-ui-excerpt.py:1` (`lines 446-495`) against a 488-line source; the same claim at `.ufo/waves/round-42/registration.md:59` |

Mistake classes and their capture: 77 *locator drift* (a fact cited at lines that never carried it — captured by a
checker that resolves the fact's identifiers against the cited range); 78 *denominator drift* (one number, two
vocabularies, one member miscounted — captured by a recount from the receipt's own rows); 79 *dead pointer* (the
pointer outlives the evidence it names — captured by resolving every run pointer through `git cat-file -e` and the
receipt's command/output/exit); 80 *header self-contradiction* (a range that cannot be true of its own body — captured
by recomputing the range from body and source).

---

77. Every source locator written in prose — in `LOG.md`, a registration, a report, a lesson — is emitted by the command that greps the pinned receipt, never typed from memory, and the cited range must contain the fact's own identifier, not a word it shares with an unrelated line: a locator whose range does not carry the identifier is a violation even when the range is inside the file and near the right code. Check: `python3 -I .ufo/waves/round-43/w1/ExecLocatorGate/check-locators.py --fetch .ufo/waves/round-43/fetch <prose files…>` — for each `<name>:<ranges>` token whose `<name>` is a file in the fetch directory, the backticked fragments of the same line are resolved against the union of the cited ranges; a `LOC … supported=0 verdict=MISS` line or a non-zero `miss=` in `CHECK_LOCATORS: locators=<n> miss=<m>` is a violation (exit 1). Shown able to fail: `LOC .ufo/waves/round-42/registration.md:61 Hyprland-HyprCtl.cpp:394-395,412-413 fragments=1 supported=0 verdict=MISS` and, on `LOG.md` at `5add5b4` (byte-identical Round 42 text; `LOG-at-5add5b4.md` in this seat, sha256 `f6c27a36…`) and the fleet report, `locators=4 miss=3` — while the corrected copy reads `Hyprland-HyprCtl.cpp:427-428,448 … supported=1 verdict=OK`; the seat that built the checker records the same pair on its own copies with a teeth selftest (`selftest 18/18`, `teeth flipped_table_broken=yes`, tool sha256 `c1ea52ad…`, `.ufo/waves/round-43/w1/ExecLocatorGate/receipt.txt`, uncommitted at this read); the cited lines are `"at": [{}, {}],` and `"size": [{}, {}],` and `"fullscreenHandler": "{}",` / `"allowedOverFullscreen": {},`, where `sed -n … | grep -c GEOMETRIC_GOAL` prints `0` for `394,395` and `412,413`, against `3` for `426,428` and `2` for `447,448`. Bound, stated because it is how the check can be fooled: the shared word `size` occurs at `:395`, so the identifier set must be the fact's own (`GEOMETRIC_GOAL`), and a locator with no backticked fragment is `NOFRAG`, not a pass. Mistake class: locator drift — a fact cited where it never was, surviving rereads because the range looks plausible. (lesson: `lessons/round-42-verifier-spotcheck.md:83-84` §6.2; the original text is `LOG.md:2483`, the appended correction `LOG.md:2487`; the round-42 lesson that would carry it does not exist — spot-check §6.1)

78. A control tally is stated once, with the definition of its denominator, and every number in that sentence is recomputed from the receipt's own rows: which rows are anchors, which are controls, and which class each control is in; a second number (a member count, a verdict denominator) uses the same definition or names its own, and a breakdown that sums to the total by moving a row between classes is a defect even when the total is right. Check: `python3 -I .ufo/waves/round-43/w1/ScrQualityCriteria/check78.py --receipt <round>/receipts/ctl-c1.txt --claim <the cited line>` — it recomputes rows, anchors, controls and the `M`/`D`/`K` classes from `^ok  <NAME>` lines, compares the receipt's `controls=` header and its `0 of <n>` verdict denominator against those counts, and compares each number the claim repeats; a `TALLY_MISMATCH claim M=37 receipt=38` line and `CHECK78: verdict=FAIL` are violations. Shown able to fail: on the round-42 receipt with the round-42 report's own sentence — `46 controls (absent base, 3 do-nothing, 5 cheats, 37 mutants)` — the checker reads `rows=48 anchors=2 controls=46 M=38 D=3 K=5 header=46 verdict_of=47` and `TALLY_MISMATCH claim M=37 receipt=38`; the header's `controls=46` is `len(jobs) - 2` (`run-c1-controls.py:139`), the verdict's `0 of 47` is `len(jobs) - 1`, and the claim's own breakdown is `1+3+5+37`, so the report's 46 includes the base anchor and loses one mutant. The repaired form passes: the round-43 registration states `48 `ok` lines … 46 controls: 3 do-nothing, 5 cheats, 38 single-defect mutants` and `CHECK78: verdict=OK` (`receipts-checkers.txt`). Mistake class: denominator drift — a right total under the wrong membership, which no reader can detect without recounting. (lesson: `lessons/round-42-verifier-spotcheck.md:85-86` §6.3, which already names `run-c1-controls.py:139`)

79. A pointer that asserts a run was recorded — a SHONEN box, a report sentence, a `LOG.md` line — names a committed receipt under that round's `receipts/`, and the receipt's own bytes carry the command (`$ …`), its output, and `exit=<n>`; a pointer to a prose section is a lead, not a receipt, because the section can be edited after the worktree is gone and a later reader cannot re-run what it describes. Check: `python3 -I .ufo/waves/round-43/w1/ScrQualityCriteria/check79.py --prose-repo <repo> --prose-rev <rev> --receipts-repo <lane> --receipts-rev <round tip> <prose files…>` — a `recorded in <target>` whose target is not a `receipts/` path prints `verdict=PROSE`, a target path failing `git cat-file -e <rev>:<path>` prints `verdict=ABSENT`, and a receipt lacking command, output or exit prints `verdict=INCOMPLETE`; `CHECK79: pointers=<n> non_ok=<n> verdict=FAIL` is a violation. Shown able to fail: the round-42 box 2 sentence `is recorded in LOG.md Round 42` reads `verdict=PROSE`, and the section it names carries no run — `git show a62f2e0:LOG.md | sed -n '/^## Round 42/,/^## Round 43/p' | grep -c NO_MATCHING_CLIENT` prints `0`, as does the whole file at that revision. The same checker reads `verdict=OK` for the round-41 harm-watch pointer whose receipt does carry `$ bash tools/mado-verify.sh --selftest`, its output and `exit=`, so the rule is satisfiable with bytes the lane has already produced. A live recurrence of the same class, observed this seat: `LOG.md:2490` names `.ufo/waves/round-43/receipts/live-geometry-host.txt`, which is untracked (`git status --porcelain` prints `?? …`) and absent from both `b2e2efd` and `HEAD`; that LOG line is worktree bytes (` M LOG.md`, sha256 `c1cf804b…`, witness `LOG-worktree-c1cf804b.md` in this seat) and the receipt itself is untracked (`?? .ufo/waves/round-43/receipts/live-geometry-host.txt`), so the pointer and the evidence are both outside every committed revision. Mistake class: dead pointer — the pointer outlives or precedes the evidence it names, so the claim is unverifiable at every revision the round commits. (lesson: `lessons/round-42-verifier-spotcheck.md:87` §6.4; round-43 witness in `receipts.txt` §4)

80. An excerpt's header line range is produced by the command that cut the excerpt and is checked, not typed: `<start>-<end>` in the header satisfies `end - start + 1` = the body length, `end <=` the source's line count, and the body equals `sed -n '<start>,<end>p' <source>` byte-for-byte, with no blank line added or dropped in transit; a header right about the start and wrong about the end is the mistake, not a typo, because it misdescribes what the file will replay. Check: `python3 -I .ufo/waves/round-43/w1/ScrQualityCriteria/check80.py --excerpt <excerpt> --source <source> --header-lines 2` — `EXCERPT_MISMATCH length|end|bytes` lines and `CHECK80: verdict=FAIL` are violations. Shown able to fail: `.ufo/waves/round-42/fetch/gkeep-ui-excerpt.py` reads `header=446-495 body=44 expected=50 src=488` with `end=495 past_src=488` and `first_diff_body_line=44` (the extra blank), while the round-43 file cut with `sed -n '446,$p'` reads `header=446-488 body=43 expected=43` and `verdict=OK`. Mistake class: header self-contradiction — a range that cannot be true of the file that carries it, so the header's provenance claim is false even though most of the body is right. (lesson: the round-42 spot-check does not route this one; the lane disclosed it in `LOG.md:2488` when regenerating the excerpt, and the same impossible range stood in `.ufo/waves/round-42/registration.md:59`. Once `corpus/lessons/round-43.md` lands its `## Mistakes`, cite `lessons/round-43.md#mistakes` beside this line rather than replacing it — criterion 54 resolves each `file#anchor` against its own file.)

---

## Which of the four I would refuse, and why

None of the four lacks a mistake. Each is verified above against committed bytes, not relayed: 77 by the locator
checker on three prose files (`miss=3`), 78 by the recount (`M=37 receipt=38`), 79 by `verdict=PROSE` plus a `grep -c`
that returns `0` for the claimed run, 80 by `end=495 past_src=488`.

If the integrator keeps only three, the one I would refuse is **78**. It is a real defect with a real capture, but its
class is not new: criterion 10 already requires every count to be published with the command that produces it and to
be rederived from the named revision, and a report that did so would have printed `48` rows beside `controls=46`. What
78 adds beyond 10 is one sentence — *say which rows the denominator excludes* — which is better appended to criterion
10 than minted as criterion 78. 77, 79 and 80 each open a class no existing criterion covers: 69 covers a measurement's
receipt at a revision but not a locator; 71 covers a seat's report path but not a report's pointer at a run; nothing
covers a header's range.

Second-weakest is **80**, on provenance rather than substance: it is the only one of the four the non-author closure
did not route (`round-42-verifier-spotcheck.md` §6 items 2–4 cover 77–79; §6 contains no excerpt item). The mistake is
still verified twice — the lane's own disclosure at `LOG.md:2488` and `check80.py` on the frozen bytes — but a
criterion whose only routing is the author's self-report should say so, which is why the lesson parenthetical names
`LOG.md:2488` and not a lessons file.

## Notes for the L1 (integrator)

- **Numbering.** 77–80 because `corpus/QUALITY.md` ends at criterion 76 (`wc -l` → `399`). Seat `ScrConsiderthese` was
  told this seat claims 77–80 and will label its own criterion 81.
- **Checkers are seat-local, as in round 41.** `check78.py`, `check79.py`, `check80.py` and the round-43 locator
  checker's invocation live under `.ufo/waves/round-43/w1/…`; their both-directions transcripts are
  `receipts-checkers.txt` beside this file. If they should outlive the round, they need a committed home; the
  criteria's `Check:` lines cite the seat path, so moving them means editing the three `Check:` commands in the same
  commit.
- **The locator checker is a sibling seat's product, not this seat's.** `ExecLocatorGate/check-locators.py` exists, I
  ran it read-only, and the seat's `receipt.txt` (400 lines, `??` at my read — uncommitted) now records the same MISS/
  OK pair with a teeth selftest. The criterion's teeth rest on the runs in `receipts.txt` §2 and that receipt, not on
  any claim that the seat passed. If the tool changes before the round closes, re-run the three commands in
  `receipts.txt` §2 and the selftest before admitting 77.
- **The round-43 LOG pointer witness is worktree bytes.** `LOG.md` is ` M` against `HEAD`; line 2490 (the round-43
  SHONEN box 2 line) exists only in the working tree, sha256 `c1cf804b…`. The byte copy is
  `LOG-worktree-c1cf804b.md` in this seat, so the line and its line number survive a later `LOG.md` edit; the
  committed counterpart is `LOG-at-5add5b4.md` (2483 lines, no Round 43 section).
- **The run-pointer rule is stricter than "committed".** It requires the receipt to carry `$`, output and `exit=`.
  Under it, every one of round 42's ten receipts fails on the command component
  (`for f in .ufo/waves/round-42/receipts/*.txt; do grep -c '^\$ ' $f; done` → `0` for all ten), and round 41's
  `ctl-c1-v2.txt`/`ctl-c2-v2.txt` fail on command and exit, while `harm-tip.txt` passes. That is the closure's own
  standard (§6.4 names "command, output, exit"), but it means adopting 79 retroactively condemns most existing
  receipts; state that in the round-43 LOG entry instead of silently tightening the past.
- **No `receipts/closure-status.txt` rule here**; seat `ScrConsiderthese` asked whether 79 already requires one. It
  does not: 79 binds a pointer to the receipt it names, and a closure-status receipt is a different object.
