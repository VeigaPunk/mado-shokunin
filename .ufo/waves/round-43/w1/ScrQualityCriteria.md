# ScrQualityCriteria — QUALITY criteria 77–80 drafted from the round-42 mistakes (round 43, w1)

**Deliverable:** `.ufo/waves/round-43/w1/ScrQualityCriteria/criteria.md` — four criteria (77–80) in
`corpus/QUALITY.md`'s own form, one per round-42 mistake class, each with rule, mistake class, `Check:`,
`Shown able to fail:` and `(lesson: …)`. Three checkers and two re-derivation transcripts sit beside it.
**Verdict:** all four mistake classes verified against committed bytes; none refused for lack of a mistake; the
one I would refuse as a standalone number is **78** (its class is already criterion 10's), and the second-weakest
is **80** (self-disclosed, not closure-routed). Details below, with the exact commands.

## What was done

1. Read the form source: `corpus/QUALITY.md:1-30,380-399` (criteria 60–76, `wc -l` → `399`,
   `grep -c '^[0-9]\+\. '` → `76`; last section heading is `## Grounding repair (round 30 …)` at `:338`,
   so criteria 69–76 currently live under a stale heading — noted for the L1).
2. Read the routing: `corpus/lessons/round-42-verifier-spotcheck.md` §6 items 2–4 (`:83-87`), §6 item 1
   (`:82`, the missing round-42 lesson) and §1–§2 for the round's commit pins.
3. Re-derived each of the four mistakes from bytes, not from the routing prose:
   - **(a) typed locator.** `.ufo/waves/round-42/registration.md:61`, `LOG.md:2483` (committed at `5add5b4`,
     witness `LOG-at-5add5b4.md`, sha256 `f6c27a36…`) and the fleet report `.ufo/reports/round-42/mado.md:10`
     cite `Hyprland-HyprCtl.cpp:394-395,412-413`; `sed -n '394,395p;412,413p'` on the pinned receipt prints
     `"at": [{}, {}],` / `"size": [{}, {}],` / `"fullscreenHandler": "{}",` / `"allowedOverFullscreen": {},`
     and `grep -c GEOMETRIC_GOAL` prints `0` for those ranges against `3` for `426,428` and `2` for `447,448`.
     `Hyprland-RegexMatchEngine.cpp:10-16` likewise misses `negative:` (line 7) though `FullMatch` (line 16) is
     inside it.
   - **(b) one tally, three numbers.** `.ufo/waves/round-42/receipts/ctl-c1.txt`: `48` rows, `REF=1`,
     `BASE-absent=1`, `D=3`, `K=5`, `M=38`; its header prints `controls=46` (`len(jobs) - 2`,
     `ctl/run-c1-controls.py:139`), its verdict `0 of 47` (`len(jobs) - 1`), and the report's sentence
     `46 controls (absent base, 3 do-nothing, 5 cheats, 37 mutants)` reaches 46 by counting the base anchor and
     dropping one mutant.
   - **(c) pointer to a run.** Fleet report `:45` says `is recorded in LOG.md Round 42`; the section at
     `LOG.md:2477` contains no run (`git show a62f2e0:LOG.md | sed -n '/^## Round 42/,/^## Round 43/p' |
     grep -c NO_MATCHING_CLIENT` → `0`, and the whole file at that revision → `0`).
   - **(d) excerpt header.** `.ufo/waves/round-42/fetch/gkeep-ui-excerpt.py:1` claims `lines 446-495` of a
     488-line source (`wc -l ~/Projects/gkeep/gkeep/ui.py` → `488`); the file is `46` lines, its body after two
     header lines `44` against `43` for `sed -n '446,$p'` — the extra blank line. The round-43 file says
     `446-488 (end of file)` with a body of `43` that `diff`s clean against the source range.
4. Built three stdlib, read-only checkers in the seat: `check78.py` (tally), `check79.py` (pointer), `check80.py`
   (header range), each run in both directions on committed bytes (`receipts-checkers.txt`):
   - `check78`: round-42 receipt + round-42 claim → `TALLY_MISMATCH claim M=37 receipt=38`, `verdict=FAIL`,
     exit 1; round-43 receipt + round-43 registration line → `verdict=OK`, exit 0.
   - `check79`: fleet round-42 report at `da384db4` with lane receipts at `a62f2e0` → box 2 `verdict=PROSE`
     (`LOG.md Round 42`), plus `INCOMPLETE why=missing command` for two receipts it also flags; fleet round-41
     report at `866affa3` with lane receipts at `b20155b` → `receipts/harm-tip.txt verdict=OK
     why=command+output+exit`, `ctl-c1-v2.txt`/`ctl-c2-v2.txt` `INCOMPLETE why=missing command,exit`.
   - `check80`: round-42 excerpt → `header=446-495 body=44 expected=50 src=488`, `end=495 past_src=488`,
     `first_diff_body_line=44`, `verdict=FAIL`; round-43 excerpt → `header=446-488 body=43 expected=43`,
     `verdict=OK`.
5. Ran the sibling seat's locator checker read-only on three prose files: `miss=3` of `locators=4` (registration,
   `LOG.md` at `5add5b4`, fleet report), and `verdict=OK` on the corrected copy. Its own receipt now exists
   (`.ufo/waves/round-43/w1/ExecLocatorGate/receipt.txt`, 400 lines, `??` at my read; selftest 18/18, teeth
   reported by the seat, tool sha256 `c1ea52ad…`) — cited in criterion 77, not claimed as passed by me.

## Criteria drafted (77–80) — one line each in the deliverable

| # | rule (short) | mistake class | control that can fail | routed by |
|---|---|---|---|---|
| 77 | a prose locator is emitted by the grepping command and its range must carry the fact's identifier | locator drift | `ExecLocatorGate/check-locators.py` (MISS→OK pair, selftest) | closure §6.2 |
| 78 | one tally, one denominator, every number recomputed from the receipt's rows | denominator drift | `check78.py` (`M=37` vs `38`) | closure §6.3 |
| 79 | a run pointer names a committed `receipts/` path carrying `$ cmd`, output, `exit=` | dead pointer | `check79.py` (PROSE / ABSENT / INCOMPLETE) | closure §6.4 |
| 80 | an excerpt header's range is checked against body and source | header self-contradiction | `check80.py` (`past_src`, length, bytes) | lane self-disclosure only (`LOG.md:2488`) |

**Which one I would refuse.** None of the four lacks a mistake — each is verified above. If the integrator keeps
only three, refuse **78**: criterion 10 already requires every count to be published with its command and rederived
from the named revision, so 78's remaining content (name the denominator's membership) is better appended to 10 than
minted as a number. Second-weakest is **80**, on provenance: the closure routed 77–79 but not the excerpt header;
80's only routing is the lane's own `LOG.md:2488`, which the criterion says explicitly.

## Gates

No gate was run or claimed by this seat. The checks I executed are the ones named in `receipts.txt` and
`receipts-checkers.txt`; every exit code is in those files. I did not run any frozen counter, control runner, or
census.

## Touched surfaces

- **Wrote only** `.ufo/waves/round-43/w1/ScrQualityCriteria/` (12 files, hashes below) and this report path.
- **Edited nothing tracked.** `corpus/QUALITY.md` is untouched — appending 77–80 is the L1's integration step.
  The lane tree already carried others' work in flight: `LOG.md` was ` M` and
  `.ufo/waves/round-43/w1/ExecLocatorGate/` `??` at my read; I only read them.
- **No git/jj mutation** (only `rev-parse`, `show`, `cat-file -e`, `status --porcelain`), no host mutation,
  no `hyprctl` call of my own, no pacman, no tool installs. Scratch `/fast/scratch/hyaku/mado-r43/ScrQualityCriteria`
  was used only for the first exploratory extraction and is deleted (`rm -rf` after the seat-local copies landed);
  nothing in this report cites a scratch path.

## Findings (what each attacks or supports)

1. **Supports 77, attacks the round-42 registration and report:** the cited ranges carry no `GEOMETRIC_GOAL`;
   the checker reads `MISS` on `registration.md:61`, `LOG.md:2483` and the report's two HyprCtl/Regex locators.
2. **Supports 78:** the report's tally is internally inconsistent by one mutant and by one anchor; the round-43
   registration's repaired sentence passes the same checker.
3. **Supports 79, and attacks the live round-43 LOG:** `LOG.md:2490` names
   `.ufo/waves/round-43/receipts/live-geometry-host.txt`, which is `??` untracked and absent at `b2e2efd` and
   `HEAD` — the same class as round-42 box 2, one round later. (Observed mid-wave; the L1 may still commit it.)
4. **Supports 80:** the round-42 excerpt's header is impossible for its own file (`end=495` vs `488`) and its
   body carries the extra blank; the round-43 regeneration is exact.
5. **Caveat the L1 needs:** criterion 79's command+output+exit requirement condemns every round-42 receipt
   (`cmd=0` for all ten) and round 41's `ctl-c1-v2.txt`/`ctl-c2-v2.txt`, and passes `harm-tip.txt`
   (`cmd=6 exit=1`). That is the closure's own standard (§6.4), but adopting 79 tightens the past; say so in the
   LOG instead of silently re-scoring earlier rounds.
6. **Caveat on `check79.py`:** its line filter (`recorded|watch|ran|run|measured|observed|logged`) also selects
   lines that merely mention "run" (e.g. the C1 command line), so it flags receipts the sentence was not really
   pointing at; the flagged receipt still lacks the command, so the verdict is not wrong, only broader than the
   rule. Same for the `recorded in` capture, which runs to `;`/`)` and can over-capture (`report:34`).
7. **Observation, not a criterion:** `corpus/QUALITY.md:338` still carries the round-30 heading with criteria
   69–76 beneath it; the draft proposes a round-43 heading for 77–80.

## Conflicts (verbatim, for the canonical judge)

- Assignment: *"(c) a SHONEN or report pointer to a run points at a committed receipt (round-42 SHONEN box 2
  pointed at a LOG line that does not exist)"*. Closure §6.4 (`round-42-verifier-spotcheck.md:87`): *"SHONEN box
  2 pointer does not resolve: commit a receipt of the live reference run (command, output, exit) and point the box
  at it."* Bytes: the box names `LOG.md Round 42` — a section that exists (`LOG.md:2477`) and does not contain the
  run. So the routed claim "a LOG line that does not exist" is not supported in that literal form; the defect is
  "the pointer's target does not carry the claimed observation, and no committed receipt does either". Criterion
  79 is drafted on the bytes and the closure's text, not on the assignment's phrasing.
- Assignment: *"the round-42 gkeep excerpt header said `lines 446-495` of a 488-line file and carried one extra
  blank line"* — confirmed exactly (`body42=44` vs `src=43`, `end=495 > 488`).
- Assignment: *"a control tally is stated once with its definition (the round-42 report said 46 controls, the
  receipt header 46 and its verdict line 0 of 47)"* — confirmed; the report's 46 is a third vocabulary
  (base included, one mutant lost), which the assignment's summary does not state.

## Limits

- I did not re-run any frozen counter or control runner; the round-42 and round-43 control receipts are read as
  bytes, and their internal consistency is what 78 checks.
- The locator checker is another seat's in-flight product; its receipt existed at my last read but is untracked,
  so no committed receipt of its teeth exists yet.
- `check78/79/80.py` have no `--selftest`; their both-directions evidence is the two runs each in
  `receipts-checkers.txt`. They read git objects only and take no index lock.
- Seat files are uncommitted (seat artifacts by rule); the L1 integrates.

## Artifacts (sha256)

```
6940ebcfceb8c68de56062ac2e67a1acc1a0bc1e7990b5b94bca652ccffd1d57  criteria.md
f7854d97bffe049f55f384b2244869b2315ffd88490eeafe3c78042644b9e9b1  receipts.txt
a8709b6bb1d9dd09bf8806c5028c4194b5c8d83d86f8506e9024662357ff9868  receipts-checkers.txt
d569cbd0aeefc2656e4e3516a9ae1f09baf67fe180bd78849fe0d732564d2164  run-checks.sh
ee89e315d4ffc8736e3d697992107428e7e93953de7812e2ff5390d64b9397de  check78.py
f50b97fc8b10b4073d11e80bf6a509eeb22add6319a74306b4ce304c8bdc75e5  check79.py
dc6883d13b89089bb2a8915c0556c0c5460d39f69341a8f4b9b62a76f04dc59e  check80.py
f6c27a3650c7bf4b7f95688978b2979d2c9a39f262686525352c63ae8bc416e2  LOG-at-5add5b4.md
c1cf804bca3f3f3d9f03958df7eaf49a8c6614ab603bd482e547264f17d20afb  LOG-worktree-c1cf804b.md
9e38c6a31208daa9c8e45c57c51905c9162a508c7d61544229d7d26fb2c7fa38  claim-r42.txt
3a731217c09fae976c4d9b3d73fcf739d1fb05d9e6d2a488f3e6e8c1142f90ac  claim-r43.txt
583ccbbed5f7e66b77c841b769c7dd73d1c9e8054ad5829d3b063e56ff113f4f  claim-r42-box2.txt
```
