# ExecControlsRerun — round 37 wave 1 report

Seat: L1Mado37-2.ExecControlsRerun (executor, leaf). Lane HEAD during the run: `80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b`.
Tools installed or updated: none.

## Verdicts

| Item | Verdict |
|---|---|
| 1. Rerun of `controls.py`, compared with `receipts/controls-v2.txt` | **PASS**: 13/13. Identical once commit hashes are masked. |
| 2a. README rows outside `## Coverage map` | **PASS**: TARGET_MISSED, admitted 0/2, clause e=0 for both entries |
| 2b. Correct rows, but `used-by` names a different path | **PASS**: TARGET_MISSED, admitted 0/2, clause c=0 for both entries |
| 2c. Gate receipt committed with another revision's bytes (one byte edited) | **PASS**: TARGET_MISSED, admitted 1/2, clause d=0 for E1. The same sandbox's previous commit (HEAD~1) is TARGET_MET. |
| Extra boundary probe a4: rows in a code fence inside `## Coverage map` | **FINDING**: TARGET_MET, admitted 2/2 (see below) |

No primary control reached TARGET_MET. The finding comes from an extra probe that I added beyond the three requested controls.

## 1. Rerun

Freeze check: the counters and `controls.py` are byte-identical at the freeze commit `893a8aad…`, at HEAD and in the working tree. The first 16 hex digits of each sha256:

```
quality/counters/c1-r37-event-ground.py freeze=1c21f8ba736bf8c1 head=1c21f8ba736bf8c1 wt=1c21f8ba736bf8c1
quality/counters/c2-r37-eventq.py freeze=6fae177fd5f42d7b head=6fae177fd5f42d7b wt=6fae177fd5f42d7b
.ufo/waves/round-37/controls.py freeze=27fc5213464168e5 head=27fc5213464168e5 wt=27fc5213464168e5
```

Command, exactly as assigned:
`cd LANE && python3 -I .ufo/waves/round-37/controls.py --out /dev/shm/mado37-ExecControlsRerun/controls.txt`

The command exited with `rc=0` in about 14 seconds. The last line of the output was `controls=13 correct=13/13`.

The diff masked every `rev=<40 hex>` field, then compared the two files:

```
diff <(sed -E 's/rev=[0-9a-f]{40}/rev=<H>/' controls-v2.txt) <(sed ... controls.txt)  -> DIFF-EMPTY lines=72
```

The raw diff contains 26 changed lines, which is 13 commit-hash pairs. Those are the sandbox commit hashes and nothing else.

The rerun receipt is retained at `.ufo/waves/round-37/w1/scratch/ExecControlsRerun/controls-rerun.txt` (sha256 `eb8963ab…537a859d`).

Side checks on the receipts that the controls copy from the lane working tree:
- All five match their committed blobs (`git hash-object` = index blob, `wt_matches=1` ×5).
- `fetch/S189.bin` is byte-identical to `round-32/fetch/S189.bin`, and `fetch/S201.bin` to `round-34/fetch/S201.bin`, as `renumber-map.md` rows 19-20 claim (`cmp`: S189-identical, S201-identical).
- The full sha256 of S212 and S214 matches the shortened prefix…suffix that `renumber-map.md` records (`1e19d926…97d7e9`, `d04e3a2f…f6b868`).

## 2. Three added controls

The scratch harness is `.ufo/waves/round-37/w1/scratch/ExecControlsRerun/controls-x.py` (sha256 `ffada69a…7621301`). It is a copy of the lane's `controls.py`, and the lane file was not edited. Its changes from the lane version:
- `wire()` takes a `remap` argument that rewrites `used-by` paths.
- New builders `readme_elsewhere()` and `receipt_other_rev()`.
- A control may list extra revisions to score.
- Each sandbox is removed right after it is scored.
- The sandbox root is `/dev/shm/mado37-ExecControlsRerun/`.

The 13 original controls run unchanged first. Their output is identical to `controls-v2.txt` once hashes and the `@HEAD` suffix are masked (`ORIG13-IDENTICAL`).

The full output is retained at `scratch/ExecControlsRerun/controls-x.txt` (sha256 `debc2da6…3d0e984`). It ends `controls=25 correct=24/25`; the one incorrect check is probe a4.

**(a) `x-a-readme-outside-map`.** The control starts from the golden setup, but the two README rows are placed right after the `## Quality bar` heading (README line 63 at BASE) instead of inside `## Coverage map` (lines 3-62). Result:
```
control=x-a-readme-outside-map@HEAD expect=TARGET_MISSED rc=1 ok=1 :: PRED-C1-r37-v2 admitted=0/2 verdict=TARGET_MISSED
  entry=corpus/knowledge/event-delivery-limits-r26.md a=1 b=1 c=1 d=1 e=0 f=1 g=1 ...
  entry=corpus/knowledge/event-queue-observability-r37.md a=1 b=1 c=1 d=1 e=0 f=1 g=1 ...
```
Only clause e fails, so this is a minimal pair with the golden control. The `section()` function (c1:68-75) ends the map section at the next `## ` heading.

**(b) `x-b-usedby-other-path`.** The control starts from the golden setup, but every control row's `used-by` names `corpus/knowledge/arc-synthesis.md`. Result:
```
control=x-b-usedby-other-path@HEAD expect=TARGET_MISSED rc=1 ok=1 :: admitted=0/2 verdict=TARGET_MISSED
  ... a=1 b=1 c=0 d=1 e=1 f=1 g=1 ...   (both entries)
```
Only clause c fails. The counter compares exact members after splitting on commas (c1:135-137).

**(c) `x-c-receipt-other-rev`.** The control commits the golden tree first, as HEAD~1, with Gate digests equal to those bytes. It then flips one byte of `fetch/S189.bin` (byte 0, XOR 1) and commits that as HEAD. Assertions in the builder check that exactly one byte differs, that the length is unchanged, that the Gate quote is still present, and that every frozen token's occurrence count is unchanged. Result:
```
control=x-c-receipt-other-rev@HEAD expect=TARGET_MISSED rc=1 ok=1 :: admitted=1/2 verdict=TARGET_MISSED
  entry=...event-delivery-limits-r26.md a=1 b=1 c=1 d=0 e=1 f=0 g=0 ids=S189,S201,S212 ok=0
  entry=...event-queue-observability-r37.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 ids=S213,S214 ok=1
control=x-c-receipt-other-rev@HEAD~1 expect=TARGET_MET rc=0 ok=1 :: admitted=2/2 verdict=TARGET_MET
```
The digest is read from the committed blob at REV (c1:145-146), so the earlier revision's digest does not carry over. Clauses f and g also drop for that entry, because a receipt that fails its Gate is excluded from `receipts` and from the `stated` check (c1:147-150). That is consistent with the docstring. The variant `x-c2-every-receipt-other-rev`, which flips one byte in all five receipts, scores 0/2 TARGET_MISSED with d=f=g=0 for both entries, and 2/2 TARGET_MET at HEAD~1.

## Extra boundary probes

These are labelled `x-a2` through `x-b4` in the output. They cost little and are not among the three requested controls.

| Probe | Result | Failing clause |
|---|---|---|
| a2: rows at end of README, inside `## Frontier` / `### Round-35…` | TARGET_MISSED 0/2 | e=0 |
| a3: rows inside the map, but the path is in the second cell | TARGET_MISSED 0/2 | e=0 |
| **a4: rows inside a code fence within `## Coverage map`** | **TARGET_MET 2/2, rc=0** | none |
| b2: `used-by` swapped (E1 rows name E2 and E2 rows name E1) | TARGET_MISSED 0/2 | c=0 |
| b3: `used-by` without the `corpus/` prefix | TARGET_MISSED 0/2 | c=0 (the lane uses the `corpus/knowledge/…` form in 186 of its `used-by` cells, so exact-path matching fits the lane's convention) |
| b4: `used-by` = path + `.old` | TARGET_MISSED 0/2 | c=0 |

**FINDING (a4).** Clause e reads "a `## Coverage map` table row". The counter, however, accepts any line that starts with `|` inside that section (c1:120-121), and `section()` (c1:68-75) does not track code fences. Rows wrapped in a fenced code block render as code, not as table rows, but they still satisfy e:
```
control=x-a4-readme-fenced-in-map@HEAD expect=TARGET_MISSED rc=0 ok=0 :: PRED-C1-r37-v2 admitted=2/2 verdict=TARGET_MET
  ... a=1 b=1 c=1 d=1 e=1 f=1 g=1 ...   (both entries)
```
Severity: low. Indexing an entry still takes a deliberate edit inside the map section, and every other clause still has to hold.

[INFERENCE, not run] The same fence blindness means a fenced line reading `## Coverage map` or `## Gate`, placed anywhere in the file, would open a section for `section()`. That would apply to both the README check and the round-37 lesson's Gate lines. This is a candidate for a v3 counter only; the v2 freeze stands.

## Retained scratch files

All are under `.ufo/waves/round-37/w1/scratch/ExecControlsRerun/`:
- `controls-x.py`
- `controls-rerun.txt`
- `controls-x.txt`

Copies of the two output receipts and `run.log` remain in `/dev/shm/mado37-ExecControlsRerun/`.

## Risks and environment notes

- **Shared `/dev/shm` quota.** `/dev/shm` is mounted `usrquota`, and every seat runs as the same user. My first two attempts at the extended run failed with `OSError: [Errno 122] Disk quota exceeded` while copying receipts into a sandbox. At the time, two lane `controls.py` runs by other seats held 1.3 GB and 1.4 GB (`/dev/shm/mado-r37-controls-*`), because the unmodified harness keeps all 13 clones until it exits. My copy deletes each sandbox after scoring, and it passed on a retry loop (try 2). If several seats rerun `controls.py` at once, the lane harness can fail intermittently on this quota. If the lane harness is ever revised, deleting each sandbox after it is scored, as my copy does, would avoid this.
- **Controls read lane working-tree receipts.** `wire()` copies the receipts from the lane working tree, not from a commit (controls.py:63-65). Today they match their committed blobs, but a sibling editing `fetch/` mid-wave would silently change what the controls test.
- **Lane state.** No lane file was written outside my scratch directory and this report. The only other entries in `git status --porcelain` were untracked files from sibling seats (`fetch/S215.bin`, `fetch/S216.bin`, `corpus/knowledge/event-delivery-limits-r26.md`), which I did not create. No git or jj command that changes state was run in the lane; all commits happened in `/dev/shm` sandbox clones under the sandbox identity. No Hyprland socket was touched and no `hyprctl` command was run.
