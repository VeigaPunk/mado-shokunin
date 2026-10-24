# ExecC2Rerun — C2 counter reproduces byte-for-byte at both revisions

Item: runner, no writes beyond this report. Re-ran
`.ufo/waves/round-30/c2/count.py` at base `8f51071b…` and data commit `446dc396…`
on 2026-10-24, from the lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, and byte-diffed the stdout against
`evidence/c2-after-446dc396.txt` and `controls/C2K1-donothing.txt`.

## Verdict: REPRODUCES — both registered measurements are exact

| Rev (full hash as passed) | exit | stdout bytes | stdout sha256 | expected | result |
|---|---|---|---|---|---|
| `8f51071b5bc44c815eeb5da76bb7f1947994ffb8` | **1** | 541 | `38b95bc3e66479026c89acdd57f39f1b06d3935f16356ecab0c122fcfc0c33ce` | `TARGET_MISSED`, UNRESOLVED {1,2,3,4,5,38,39,40} | MATCH |
| `446dc3966193c81e64896f4880a19a4bd249255b` | **0** | 589 | `89239fa1a68a7c2410fdd2d43f1c2c706210c071fa855b3bb28da46e28b9e121` | `active=40 resolved_active=40`, `TARGET_MET` | MATCH |

stderr empty in both runs. Byte-diff is **exact modulo the harness-appended exit
line**: each fresh stdout is a strict byte prefix of its receipt, and the
remaining receipt suffix is exactly `EXIT=<exit>\n`, matching the real exit code.

| Receipt | bytes | sha256 | fresh stdout is prefix | suffix | exit in suffix agrees |
|---|---|---|---|---|---|
| `controls/C2K1-donothing.txt` | 548 | `dc1ead839217afdfaee9c9cd6980e904f63a077bdfeed739b944b9f130303507` | yes (541 B) | `EXIT=1\n` | yes (rc 1) |
| `evidence/c2-after-446dc396.txt` | 596 | `0c6ecd87189ef478ded640978ebe11bab59cdd3e6c9adf2781132aa2af564e3d` | yes (589 B) | `EXIT=0\n` | yes (rc 0) |
| `evidence/c2-before-8f51071b.txt` | 548 | `dc1ead83…` | yes (541 B) | `EXIT=1\n` | yes (rc 1) |

Note: the control receipt and the before-evidence receipt are **the same bytes**
(identical sha256). That is expected under the registered control ("the same
counter at base"), not a duplicated execution: my independent run of the base
revision reproduces exactly that text, so the control's content is real.

Method note: the `rev=` header prints the argument verbatim, so byte-identity
requires passing the full 40-hex hash. A short prefix would print
`rev=446dc396` and differ in line 1.

## 1. Exact commands and retained output

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-30/c2/count.py 8f51071b5bc44c815eeb5da76bb7f1947994ffb8   # rc 1
python3 -I .ufo/waves/round-30/c2/count.py 446dc3966193c81e64896f4880a19a4bd249255b   # rc 0
```

Base stdout (verbatim):

```
counter=c2-grounding-r30 rev=8f51071b5bc44c815eeb5da76bb7f1947994ffb8
METRIC literal lines=28/40 fraction=0.7000
METRIC superseded=[20]
METRIC active=39 resolved_active=31 fraction=0.7949
UNRESOLVED criterion 1: no citation
UNRESOLVED criterion 2: no citation
UNRESOLVED criterion 3: no citation
UNRESOLVED criterion 4: no citation
UNRESOLVED criterion 5: no citation
UNRESOLVED criterion 38: no citation
UNRESOLVED criterion 39: no citation
UNRESOLVED criterion 40: no citation
LINE 20 superseded excluded
PRED-C2-r30 verdict=TARGET_MISSED
```

Tip stdout (verbatim):

```
counter=c2-grounding-r30 rev=446dc3966193c81e64896f4880a19a4bd249255b
METRIC literal lines=40/52 fraction=0.7692
METRIC superseded=[1, 2, 3, 4, 5, 18, 19, 20, 32, 38, 39, 40]
METRIC active=40 resolved_active=40 fraction=1.0000
LINE 1 superseded excluded
LINE 2 superseded excluded
LINE 3 superseded excluded
LINE 4 superseded excluded
LINE 5 superseded excluded
LINE 18 superseded excluded
LINE 19 superseded excluded
LINE 20 superseded excluded
LINE 32 superseded excluded
LINE 38 superseded excluded
LINE 39 superseded excluded
LINE 40 superseded excluded
PRED-C2-r30 verdict=TARGET_MET
```

`UNRESOLVED {1,2,3,4,5,38,39,40}` = 8 entries = 39 active − 31 resolved; the set
is exactly the expected one at base.

## 2. Independent reimplementation agrees (not just a replay of the same bytes)

I re-implemented segmentation, the supersede scan and the resolution rule from
the frozen docstring (separate code, same `git show` reads) and reproduced:

- base: criteria 40, literal 28/40, superseded `[20]`, active 39, resolved 31,
  unresolved exactly `{1,2,3,4,5,38,39,40}` — all `no citation`.
- tip: criteria 52, literal 40/52, superseded `[1,2,3,4,5,18,19,20,32,38,39,40]`,
  active 40, resolved 40, unresolved none.

Supersede provenance read from committed text at tip — each retirement names a
real criterion and each retirement line is itself grounded:

| retired | by | retired | by | retired | by |
|---|---|---|---|---|---|
| 1 | 41 | 5 | 45 | 38 | 49 |
| 2 | 42 | 18 | 46 | 39 | 50 |
| 3 | 43 | 19 | 47 | 40 | 51 |
| 4 | 44 | 20 | 21 (pre-existing, since base) | 32 | 48 |

No phantom supersession: every number in the printed set exists as a criterion
(52 at tip). Every M-id cited by an active criterion was re-verified one id at a
time with full range/list expansion (`M01-M07` → M1..M7; `M03/M05/M06/M07` →
M3,M5,M6,M7) at both revisions: **zero missing ids**.

## 3. Freeze/data ordering and receipt provenance

- `count.py` was introduced in `451e8b3` (freeze, pre-data) and never changed:
  blob `74a4859d6ab2921900082b093ce315594972c708` at `451e8b3:` = at `HEAD:` =
  worktree `git hash-object`; `git diff 451e8b3 HEAD -- …/count.py` empty.
  So the rubric frame precedes the data commit that it grades.
- Receipts: `C2K1-donothing.txt` and `c2-before-8f51071b.txt` committed at
  `451e8b3`; `c2-after-446dc396.txt` at `92d3c86` (records commit).
- `corpus/QUALITY.md` base→data: **22 insertions, 0 deletions**, 0 removed
  criterion lines. Criteria 1–40 are byte-untouched; rows 41–52 (12 numbered
  lines + 10 continuation lines) are appended. No ungrounded criterion was
  repaired in place, so the supersede path is the only change mechanism.
- Lane worktree clean for `.ufo/waves/round-30` (no post-commit edits to the
  counter or receipts).

## 4. Predicate arithmetic

- Literal: 28/40 = 0.7000 at base (exactly at the bar), 40/52 = 0.7692 at tip
  (+0.0692 margin).
- Active: 39 at base, 40 at tip (52 − 12 superseded).
- At tip the set of non-literal first lines is **exactly** the 12 superseded
  criteria, so every active criterion carries a `lessons/` citation on its own
  numbered line, and the literal shortfall is structurally the retired set
  (literal 40 and active 40 are equal by construction here, not coincidence).
- Registration text ("12 lines superseded by rows 41–51, +1 new criterion 52;
  literal 40/52 = 0.7692") matches the measured bytes exactly
  (11 rows 41–51 + criterion 21→20 = 12).

## 5. Counter weaknesses found (none falsifies the verdict)

1. **Anchor leg is skipped for anchor-only citations.** `ANCH_RE` is
   `… #([\w-]+)\s*(M[0-9/\-]*)` — the `M` is mandatory, so
   `lessons/<file>#<anchor>` with no following M-id is checked for file
   existence only. Three active criteria at tip are in that class:
   #31 `round-21.md#mistakes`, #36 `round-25.md#mistakes`,
   #37 `round-25-verifier-spotcheck.md#7-routed-defects-lane-fixes-next-round`.
   All three anchors are real headings (`## Mistakes`, `## Mistakes`,
   `## 7. Routed defects (lane fixes next round)`); #37's is a GitHub-style slug,
   and the counter's own `want = anchor.replace("-", " ")` test would have
   *failed* it had the leg been applied — an implementation gap, not a false
   pass. Criterion 37's target "item 3" exists in that section and is the
   population-equality clause the criterion encodes.
2. **Zero-padded range/list ids are checked only partially.** `MID_RE` reads
   `M01-M07` as two singles (M1, M7), and `ANCH_RE`'s mids capture stops at the
   second `M` in `M03/M05/M06/M07` (captures `M03/`). Exhaustive re-parse shows
   no id is actually missing, so the under-check is latent at this revision.
3. **Ambiguous range heuristic is unexercised.** `M<a>-<b>` with `a<=b` is read
   as a range; every compound id cited at tip has round>item
   (`M23-4`, `M23-5`, `M23-7`, `M24-2`, `M28-1..3`, `M30-1`, `M30-2`), so no
   misparse occurs — but a future `M2-30` (round 2, item 30) would be silently
   expanded to a range.
4. **Supersede is a retirement path.** 12 of 52 criteria (23%) were retired in
   one data commit; the active bar is reachable by retiring an ungrounded line
   instead of grounding it. Here each retirement line is itself grounded (all 40
   active resolve), and the supersede rule is frozen in the pre-data docstring,
   so the metric is not gamed — but a closure critic should read it as
   "retire-or-ground", not "ground".
5. **cwd sensitivity (boundary, not defect).** From the fleet root the counter
   exits 2 with `SETUP_ERROR: no corpus/QUALITY.md at …` and a git fatal on
   stderr — loud, not silent. A revision that happened to exist in both repos
   would instead measure the wrong repo; the documented usage ("from the lane
   root") is load-bearing.
6. **Receipt format.** The receipts' `EXIT=` line is harness-appended; the script
   itself never prints it. Reproduction therefore needs the exit code checked
   separately, which I did (rc 1 / rc 0 as recorded).

## 6. Environment and determinism

- Repeated invocations are byte-identical (base and tip).
- Scrubbed environment (`env -i` equivalent: `PATH=/usr/bin:/bin`, `LC_ALL=C`,
  `TZ=UTC`) reproduces both stdouts byte-for-byte with empty stderr — the
  counter is locale-, site- and environment-independent; it reads only committed
  bytes via `git show`/`git cat-file`, never the worktree.

## 7. Files changed / installs

- Written: this report only.
- Installs/upgrades: none (python3, git present; pacman untouched under the
  host-wide pause).
- No lane, fleet, sibling-repo, git-index or jj mutation; every measurement was
  a read (`git show`, `git log`, `git diff`, `git hash-object`, subprocess run of
  the frozen counter).

## 8. Adjacent observation (reported by peer `RevC1Fence`, verified read-only here; not restored)

`.ufo/waves/round-30/w1/reports/RevC1Fence.md`'s author reported an
out-of-scope worktree write. I confirmed it independently, read-only, and made
no repair (runner: no writes beyond this report):

- `git status --porcelain` shows exactly one tracked modification:
  `M quality/q36-successor-receipts.txt` (19 lines, mtime 04:06:46), plus the
  untracked `.ufo/waves/round-30/w1/` report directory. Every C2 artifact
  (`c2/count.py`, `controls/`, `evidence/`, `registration.md`) is clean.
- The diff is 4 changed lines (1, 7, 10, 13), and only the two ephemeral scratch
  tokens per line (`/tmp/mado-r28-q36-<rand>` and `…/run.<rand>`). Normalizing
  both tokens makes the worktree byte-equal to `HEAD`: `rc=`, `expected=`,
  `PASS` and the final newline are unchanged, so no receipt verdict moved.
- Effect on this item: none. `count.py` never reads that file (it reads
  `corpus/QUALITY.md` and `corpus/lessons/*` via `git show`), and it measures
  committed bytes, so the base/tip measurements above are unaffected by any
  worktree drift.
- Disposition left to the L1/harm watch: the write is outside the registered
  write scope of this wave and leaves the lane dirty; restoring it (or accepting
  it as data) is not a runner decision.
