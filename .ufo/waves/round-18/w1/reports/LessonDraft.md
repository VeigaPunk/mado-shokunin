# LessonDraft — scoped report (round 18, w1)

Scope: draft `.ufo/waves/round-18/drafts/LessonDraft.md` only (Mistakes rows M1-M4 and the S072+ Gate skeleton). No product code, no QUALITY/SOURCES/SCORECARD/LOG/lessons edits, no git or jj writes, no pacman or host queries, no web fetches. No tool installed or updated.

## Verified facts (read-only, lane git plus file bytes)

- `corpus/lessons/round-17.md:175-176`: "tool sha256 `962919ce…`; all real-transcript receipts re-cut with identical counts."
- `git show --stat 0ab1ccc` lists `tripwire-r17.txt`, the four selftest receipts, `tripwire-vs-oracles.json`, and two w2 receipts. It does not list `tripwire-r13..r16.txt`, `tripwire-anchor-r15.txt`, or `tripwire-pacmanlog-join.txt`.
- `git log --oneline -- <each of those six files>` ends at `f71ccbe` (and `988b858` for some). These files were last changed under tool `7a98720e…`.
- grep for `962919ce|7a98720e|measured_commit|commit` in the six files: 0 hits each.
- `sha256sum tools/mado-tripwire.py` = `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072`.
- `git show refs/heads/master:tools/mado-verify.sh` line 3406 = `blob=$(tmo git -C "$tree" show "HEAD:$OMARCHY_SKILL_REL" 2>/dev/null | sha256sum | cut -d' ' -f1)`. Empty-input digest: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (computed here).
- The OM scenario's git stub (`tools/mado-verify.sh:662-675`) answers `show)` with `cat "${STUB_GIT_BLOB:-/dev/null}"; exit 0` at line 670. No OM case drives a failing `show`.
- `corpus/QUALITY.md` lines 109-111: criterion 23 is the last round-17 criterion (the round-18 criteria are QualityDraft's).
- Lane HEAD is `d3a0000` (detached); `master` is `refs/heads/master` at `d3a0000`.
- `.ufo/waves/round-18/receipt-check.py`, `measure-mutants.py`, `pipe-rc-census.py`, `fetch-verify.py` do not exist yet. The fix column states what each must show; none was run.

## Findings

1. M1 (R17-V1/V2) is confirmed for the six receipts. The re-cut claim at `round-17.md:175-176` names a tool revision that the receipt files do not record, and git records no re-cut of them at `0ab1ccc`.
2. M1 (R17-V2) cannot be checked from the lane: `.ufo/reports/round-17/mado.md` is absent here. The cited line (`:76`) is taken from `round-17-verifier-spotcheck.md:193-196` and is marked as such in the draft.
3. M2 (R17-V5) is seat-attested only. No committed mutant receipt exists under the lane for the round-17 tightenings (`corpus/lessons/round-17.md:156-158`). I did not verify the `/tmp` lab, and the draft does not claim it.
4. M3 (F10) is confirmed by file bytes: line 3406 discards the git rc. The OM scenario has no failing-`show` case. The UNKNOWN arm at `:3408` cannot be reached through the pipeline as written.
5. M4 (R17-V3) is supported by `round-17.md:145-148` and `round-17-verifier-spotcheck.md:197-200`. The counter-side fix needs receipts, which the S056-S071 rows do not have for round 18.
6. The Gate skeleton contains placeholders only. No S072+ row was filled, and no URL was fetched.

## Open items for L1

- Numbering: L1 may renumber M1-M4 to match the round-18 Mistakes table.
- QUALITY 24-26 belong to QualityDraft. The natural bindings are M1 to the receipt-label check, M2 to the mutant check, and M3 to the pipe-rc census with the OM case. M4 binds to the fetch-verify receipt rule. This is a suggestion only.
- Two Mistakes rows reference operator-owned or jj-audit material outside the lane (`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMado.md`). It was read, not written.

## Installs

None. No package, tool, or host action was taken.

## Out of scope and not done

- Running the four round-18 checks (they do not exist yet, and the spec asks that they be shown red and green by their owners).
- Writing QUALITY criteria, SOURCES rows, or lesson files.
- Any host or pacman query.
