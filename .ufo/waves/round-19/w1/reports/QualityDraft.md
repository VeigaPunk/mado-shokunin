# QualityDraft — drafted QUALITY 27-29 with preamble; two red arms verified, three planned checkers not yet landed, S084 trips a second arm, round-19 tool receipts cannot go green as specified

Draft: `.ufo/waves/round-19/drafts/QualityDraft.md` (only file written, plus this report). Baseline `9c54c56` (`corpus/QUALITY.md` ends at criterion 26, unchanged in the lane tree, `git status` clean for it). Preamble paragraph explains why 27–29 are not restatements of 7, 9, 13, 23, 24; it concedes that 29's receipt sub-clause overlaps 24 and states the distinct counting rule.

## Findings

1. **Planned checkers are absent.** `.ufo/waves/round-19/` holds only `fresh-pins.py`, `tw-recall.py`, `gen_w1.py`, `evidence/`, and `w1/`. `anchor-durability.py`, `supersede-sweep.py`, `supersessions.json`, the round-19 `receipt-claims.json`, and `corpus/lessons/round-19.md` do not exist (the lessons directory stops at round-18). The draft names them as planned, not landed (spec text: `gen_w1.py` lines for AnchorDurability, SupersedeSweep, ReceiptClaims19). I did not write or stand in for them.

2. **Red arms verified by me, at 9c54c56, without the planned checkers:**
   - 27 / S094 — `git show 9c54c56:corpus/SOURCES.md | sed -n 106p`: status `mined`; anchor is "tree listing sha256 50c1ac25…", "backgrounds tree sha256 9e1160a0…", "digest-only HTML". Closure re-open `corpus/lessons/round-18-verifier-spotcheck.md` §4: two distinct digests for one URL (`1a3ddca5…`, `4d001dc8…`). Matches R18-V1 / lesson M7.
   - 27 / S084 — line 96: status `mined`; anchor `https://docs.rs/xdg/latest/…` (unpinned alias, the UNPINNED_ALIAS arm) and a "saved HTML … sha256 0291cfe6…". **Extra finding:** `git grep 0291cfe6 9c54c56` matches only `corpus/SOURCES.md:96`, so the saved HTML body is not in the tree; under the planned spec's docs.rs / `*.html` rule it also trips PER_FETCH_DIGEST. The assignment named only UNPINNED_ALIAS. The draft lists both; L1 should confirm the intended reason set.
   - 28 — `git grep -l '2\.17\.0' 9c54c56 -- corpus/knowledge corpus/README.md SKILL.md PROVINCE.md tools` → 13 files (SKILL.md, corpus/README.md, eleven under corpus/knowledge incl. walker-route-r18.md, tools/mado-verify.sh). Same-line `2.17.2` + `S###` pointers: `corpus/README.md:44` and `corpus/knowledge/walker-route-r18.md:1` only. 13 − 2 = **11 STALE**, matching the assignment's red. SKILL.md has `2.17.2` only at 1825–1827 (errata), no pointer on a `2.17.0` line, so it counts as STALE.
   - 29 / criterion-26 red-before — `.ufo/waves/round-18/evidence/gate-rc-redbefore.txt` and `regression-recut.txt` at 9c54c56 carry zero `tool_sha256`/`measured_commit` tokens. I ran the existing checker `python3 -I .ufo/waves/round-18/receipt-check.py /tmp/r19q/claims.json` (read-only; `git show` only; /tmp scratch claims file, `claims` key). Output: `RECEIPT red-gate-rc-redbefore MISSING_PROVENANCE`, `RECEIPT red-regression-recut MISSING_PROVENANCE`.

3. **Round-19 tool receipts cannot be green under the checker as specified (blocker for ReceiptClaims19 and for criterion 29's full green arm).** The same run with `green-measure-before` (rev 17661e0, tool `round-17/measure.py`) printed `ok`. `green-tw-recall-before` (rev 17661e0, tool `round-19/tw-recall.py`) printed **`ERROR`**: the receipt's `measured_commit=9c54c56` names a revision where `tw-recall.py` does not exist (it was added in 17661e0; `git cat-file -e 9c54c56:.ufo/waves/round-19/evidence/tw-recall-before.txt` → absent). Its RECEIPT header carries `tool_sha256=22090298…` (= `git show 17661e0:.ufo/waves/round-19/tw-recall.py | sha256sum`), so the header is internally consistent but cannot be re-derived from `measured_commit`. The spec's "green claims … at rev {B}" is also unattainable: those receipts are committed at 17661e0, not 9c54c56. Criterion 24's own wording (`tool_sha256` equal to `git show <measured_commit>:<tool>`) therefore fails for any tool added in the same round as its receipt. Options for L1 (not decided here): name `measured_commit` as the commit holding the tool bytes (17661e0) with a separate input-revision field; or split the receipt into a tool-committed record and an input-revision record. The checker and criterion 29's green arm depend on this choice. I did not edit the checker.

4. **Criterion 29 green arm is partial.** Full green = a re-cut gate red-before/regression receipt with `measured_commit=9c54c56`, `tool_sha256=c9fb0cef…` (= `git show 9c54c56:tools/mado-verify.sh | sha256sum`, verified), reading `ok`. Not produced; I did not produce it.

5. **Checker interface.** `receipt-check.py` takes the claims path as `argv[1]` and reads `json["claims"]` (a top-level dict, not a bare list). No checker change is needed to point it at a round-19 claims file; ReceiptClaims19's "find how it takes a claims path" resolves to argv[1].

6. **Lesson ids.** Criteria cite `lessons/round-19.md#mistakes` M1 (R18-V1) and M2 (R18-V4) for 27, M3 (R18-V3) for 28, M4 (R18-V2) for 29, following LessonDraft's planned numbering. The file does not exist yet; the citations hold only once L1 lands it with those ids.

7. **Shape.** Each criterion's first line ends with the required `(lesson: …; outside lessons/round-18-verifier-spotcheck.md R18-V<k>)` parenthetical; 27 cites R18-V1/V4 (two routed defects, as criterion 25 cites R17-V1/V2). Each has a `Runnable check:` with red and green arms; green arms for 27 and 28 are pending the S097/S098 rows and the sweep's landed edits, and are stated as such.

## Verified commands (all read-only; no git write, no host command, no pacman, no live gate)

- `git show 9c54c56:corpus/SOURCES.md | sed -n 106p`, `awk` status/opened/recheck for S084/S094, row count (95)
- `git grep -l/-n '2\.17\.0'`, `'2\.17\.2'` at 9c54c56 over owned paths; per-file same-line pointer count
- `git grep -l 0291cfe6 9c54c56`; `git ls-tree -r --name-only 9c54c56` for xdg bodies
- `git show 9c54c56:tools/mado-verify.sh | sha256sum` → `c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5`; `tools/mado-tripwire.py` → `c1ae45a7…`; `.ufo/waves/round-17/measure.py` → `de4c422b…`
- `git show 17661e0:.ufo/waves/round-19/tw-recall.py | sha256sum` → `22090298…`
- `python3 -I .ufo/waves/round-18/receipt-check.py /tmp/r19q/claims.json` → 3/4 (`MISSING_PROVENANCE` ×2 ok, `ok` for measure, `ERROR` for tw-recall)
- `grep -c` of RECEIPT headers in round-19 evidence files

## Limits

- Did not run `anchor-durability.py`, `supersede-sweep.py`, `landed-check.sh`, or any round-19 selftest: none exist or they are other seats' items. Their red/green arms are stated from the spec and from my grep/read equivalents.
- Did not fetch any web source (no fetch receipts needed; the S094/S084 facts come from committed SOURCES text and the closure file).
- Did not check the `S090`/`S096` ledger rows exist in the registry (S096 is reserved, not landed).
- Historical mentions (`walker-deep-r9.md` etc.) are counted by the 28 sweep rule; whether a dated historical note needs a pointer is a judgment for the checker spec, not settled here.
- `measure.py` at 17661e0 bytes were confirmed indirectly (checker `ok` at rev 17661e0), not via a separate sha run.
- The overlap of 29 with 24 is conceded in the preamble; a reviewer should decide whether 29 stays separate or folds into 24.

## Installs

none
