# RevR1R5 — the five routed defects of the round-36 spot-check, re-checked

Seat: `L1Mado37-2.RevR1R5` (reviewer). Date: 2026-10-25, 12:12–12:17Z.
Subject: `corpus/lessons/round-36-verifier-spotcheck.md` §5, items R1–R5.
Revisions: round-36 tip `a5aaa09`; lane HEAD `80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b`; fleet report
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/mado.md` (last commit `b26422a6`, and no commit
touches it after that: `git log --oneline b26422a6..HEAD -- .ufo/reports/round-36/mado.md` prints nothing).
Sandbox: `/dev/shm/mado37-RevR1R5/sb` (a `--no-local` clone at `a5aaa09`, sandbox identity) and
`/dev/shm/mado37-RevR1R5/bare.git`. Nothing in LANE was edited.

## Verdicts

| Item | Verdict | One-line basis |
|---|---|---|
| R1 | **half fixed**: the file is committed, the "working tree clean" claim is still uncorrected | committed in `80b83c8` with the same bytes; report line 379 has no erratum |
| R2 | **still live, and wider than routed** | the receipts never named `64979ef` at any revision; seven report lines are affected, not three |
| R3 | **still live**; the spot-check over-counts it ("twice") | QUALITY holds exactly five new criteria (57–61); "six criteria" appears **once** (lines 270–271) |
| R4 | **still live** | the lesson at HEAD still says "1,037 B"; the receipt is 1,756 B from `f77b554` through HEAD |
| R5 | **still live, and wider than routed** | lines 171–180 ignore `--rev`, and the path scope cannot see an R1-class untracked file |

None of R2–R5 has a committed fix yet. The only in-flight work is the `ScribeErrata` draft
(`.ufo/waves/round-37/w1/scratch/ScribeErrata/` exists, uncommitted). I did not rely on it.

## R1 — the uncommitted DistillerFindings report

```
$ git -C LANE status --porcelain | wc -l                 # at 12:12Z, HEAD 80b83c8
0
$ stat -c '%s B mtime=%y' .ufo/waves/round-36/w1/reports/DistillerFindings.md
19033 B mtime=2026-10-25 05:31:02.150287716 -0300
$ git log --format='%h %an %ad %s' --date=iso -- .ufo/waves/round-36/w1/reports/DistillerFindings.md
80b83c8 mado-shokunin 2026-10-25 09:12:46 -0300 round-37: the inherited round-36 DistillerFindings seat report (spot-check R1), and the wave-1 spec, …
$ git cat-file -s 80b83c8:<path>; git hash-object <path>; git rev-parse 80b83c8:<path>
19033
b249cdbee960bb9057dc085c2e8a3ce721124ccc
b249cdbee960bb9057dc085c2e8a3ce721124ccc
$ git cat-file -e a5aaa09:<path>   → fatal: … exists on disk, but not in 'a5aaa09'
$ git cat-file -e b4e47e9:<path>   → fatal: … exists on disk, but not in 'b4e47e9'
```

- **Lane-authored: yes.** Header line 3 reads ``Seat: `L1Mado36.DistillerFindings` (simplifier). Date: 2026-10-25. Lane: mado-shokunin.``,
  and its seat prompt is committed at `a5aaa09:.ufo/waves/round-36/w1/prompts/DistillerFindings.md`.
- The file has the same size, mtime and blob as the spot-check measured (19,033 B, 05:31), so the
  committed bytes are the original ones and were not edited before committing.
- The spot-check's side claim is correct, with one detail: the scratch ledger is at
  `.ufo/waves/round-36/scratch/DistillerFindings/catalog.md` (not under `w1/`). It was added in
  `fe55a90` (`git log --diff-filter=A`), which is an ancestor of `a5aaa09`.
- **Still owed:** fleet report line 379 still reads ``Lane tip at closure: `a5aaa09…`, working tree clean``.
  No erratum exists in the fleet report or in the lane records.
- Live-tree note: by 12:16Z the work tree has 5 untracked entries, all round-37 wave-1 output
  (`GIT_OPTIONAL_LOCKS=0 git status --porcelain` → 4 under `.ufo/waves/round-37/w1/reports`, 1 under
  `.ufo/waves/round-37/w1/scratch`). That is expected mid-wave and is not R1.

## R2 — the report names a revision its receipts do not

```
$ grep -n 64979ef .ufo/reports/round-36/mado.md
6:Lane tip when this report was written: `64979efb7f95acc67e753c642294c41a4d102bfa`.
196:| The after receipts re-pinned to the hardened tip … | round-36 | `64979ef` |
215:- after, at `64979efb7f95acc67e753c642294c41a4d102bfa` (`receipts/after-discrimination.txt`, …
231:- after, at `64979efb7f95acc67e753c642294c41a4d102bfa` (`receipts/after-pointers.txt`, …
303:  closed on `64979ef`, and any report not in that commit is not claimed).
339:and a scratch tree). `64979efb7f95acc67e753c642294c41a4d102bfa`, the tip named above, remains an
381:this report cites (`64979ef`) and the round's data commit (`a3094c9`) are ancestors.
```

The revision named in the receipts, at each commit:

```
== 64979ef
# C1 after-state — PRED-C1-r36-v1 discrimination at ea89bdeb36e962bfb50a742bd2ad84a8eaee3510
# C2 after-state — PRED-PTR-r36-v1 at ea89bdeb36e962bfb50a742bd2ad84a8eaee3510
== fe55a90   (same at a5aaa09)
# C1 after-state — PRED-C1-r36-v1 at 4d28b193e52f6cc8f04e81fda2664e018d62e209
# C2 after-state — PRED-PTR-r36-v1 at 4d28b193e52f6cc8f04e81fda2664e018d62e209
$ git show a5aaa09:SCORECARD.md | grep -n 4d28b19   → 2324, 2333 (both "the revision both receipts name")
```

- **Still live.** No receipt, at any revision, says "after at `64979ef`". At `64979ef` the receipts named
  `ea89bde`; from `fe55a90` onward they name `4d28b19`. The spot-check names only lines 196, 215 and 231.
  Lines 6, 303, 339 and 381 rest on the same false premise. Line 303 says the round "closed on `64979ef`",
  but `git log --oneline 64979ef..a5aaa09` lists eight later commits, including `4d28b19` and `fe55a90`.
- **Qualifying the spot-check's "the claim itself is unaffected":** that holds against the `a5aaa09`
  receipts, because the gate blobs are identical at `4d28b19`, `a5aaa09` and HEAD
  (`check-counter-discrimination.py 0865b141…`, `check-evidence-pointers.py ce0dd98b…`). It does **not**
  hold at the revision the report names. The gates changed between `64979ef` and `4d28b19`:
  `cbe609558c0a → 0865b1419fae` and `651d0acc956a → ce0dd98b7115`
  (`git diff --stat 64979ef 4d28b19 -- quality/` → 2 files, +26/−1). So "after, at `64979ef`" describes
  a measurement by a gate that was later hardened. The erratum should name `4d28b19` and the gate blob.
  It should not just swap one hash for another.
- Ancestry is fine: `64979ef`, `4d28b19` and `fe55a90` are all ancestors of `a5aaa09`.

## R3 — criteria arithmetic

```
$ for n in 56..62: git show a5aaa09:corpus/QUALITY.md | grep -c "^$n\. "
56:1 57:1 58:1 59:1 60:1 61:1 62:0
$ (a3094c9) 57:1 58:1 59:1 60:1 61:0        $ (HEAD) 57–61: 1 each, 62:0 63:0
$ git show 4243d03:corpus/QUALITY.md | grep -oE '^[0-9]+\. ' | tail -1   → 56.
$ git log --format='%h %s' -S'61. ' -- corpus/QUALITY.md   → 520c631 round-36: the records — …
$ grep -Pzo 'six\s+criteria' .ufo/reports/round-36/mado.md | … | grep -c six   → 1
$ git grep -c -P 'six\s+criteria' HEAD -- LOG.md SCORECARD.md corpus/lessons/round-36.md   → rc=1 (none)
```

- **Still live.** Five criteria are new in round 36: 57–60 land in `a3094c9` and 61 in `520c631`.
  The base `4243d03` ends at 56. Report lines 270–271 read "six criteria (57–61)".
- **The spot-check over-counts this.** It says "six criteria (57–61)" appears twice, but it appears
  once. Line 38 reads "`corpus/QUALITY.md` criteria 57–61" with no count, which is correct.
  The lane records (LOG, SCORECARD, lesson) have no "six criteria" at HEAD.
  `SCORECARD.md:2315` reads "all five new criteria, including 61", which is correct.
  The erratum should cite one occurrence (line 270), not two.

## R4 — stale S211 receipt size in the lesson

Receipt path: `.ufo/waves/round-36/fetch/S211.receipt.txt`.

```
$ git cat-file -s <rev>:.ufo/waves/round-36/fetch/S211.receipt.txt
a3094c9 1037
f77b554 1756
a5aaa09 1756
HEAD    1756
$ git log --format='%h %s' -- <receipt>   → f77b554 (+10 lines, `git diff --stat`), a3094c9 (added)
$ stat -c %s <receipt>   → 1756; git status --porcelain -- <receipt> | wc -l → 0
$ git show HEAD:corpus/lessons/round-36.md | grep -n 1,037
68:receipt `.ufo/waves/round-36/fetch/S211.receipt.txt` (1,037 B; the fetched HTML's
```

- **Still live**, exactly as routed: 1,037 B at `a3094c9`, then 1,756 B from `f77b554` (the identity
  note) through HEAD. Lesson line 68 is unchanged at `a5aaa09` and at HEAD, and no commit after
  `a5aaa09` touches the lesson.

## R5 — `inherited_dirty` is a work-tree reading

The code is `quality/check-evidence-pointers.py`, blob `ce0dd98b…`, the same at `a5aaa09` and HEAD:

- `:56-67`: `INHERITED_PATHS` is a hard-coded list of ten round-35 paths.
- `:171`: `status_out = git(repo, "status", "--porcelain", "--", *INHERITED_PATHS)` runs on the
  work tree of `--repo`. The `rev` argument (`:124`) is never passed to it, while every other
  observable reads from `rev` via `ls-tree`/`show` (`:126`, `:131-132`).
- `:172-178`: a second, separate `git status` run, used only to get the exit code. A non-zero code
  fails closed with `error=git-status-unusable`. The first run cannot tell the gate about failure,
  because the `git()` helper (`:75-79`) returns `""` on error.
- `:179-180`: `inherited_dirty = len(non-blank lines)`. `:220`: the observable feeds `met`.
- The docstring (`:23`) describes the observable as "the ten round-35 closure paths `git status --porcelain` reports".
  That conflicts with `:8` ("Each observable counts committed bytes").

Tests in the sandbox clone (`a5aaa09` checked out, `python3 -I quality/check-evidence-pointers.py …`, first line shown):

```
A  --rev a5aaa09, clean tree
   … inherited_dirty=0 … verdict=TARGET_MET
B  --rev 4243d03, clean tree (the before revision)
   … inherited_dirty=0 … setup=missing-r36-sections verdict=TARGET_MISSED
   committed before receipt, header line 4: "# inherited_dirty=10 (the ten round-35 paths …"
C  --rev a5aaa09, one inherited file edited in the work tree (echo x >> .ufo/waves/round-35/w2/reports/RevC1Tip.md)
   … inherited_dirty=1 … verdict=TARGET_MET → TARGET_MISSED
D  --rev a5aaa09, an untracked round-36 seat report present (?? .ufo/waves/round-36/w1/reports/Untracked.md)
   … inherited_dirty=0 … verdict=TARGET_MET
E  --repo <bare clone> --rev a5aaa09
   PRED-PTR-r36-v1 error=git-status-unusable rc=128 verdict=TARGET_MISSED
```

- **Still live, as routed.** Test B gives `0` at the revision where the committed receipt records `10`,
  so the observable does not depend on `--rev`. Test C changes the verdict at a fixed `rev` by editing
  the work tree alone.
- **Finding R5a (new, MEDIUM): the gate cannot detect the R1 class of defect.** The check is limited to
  the ten round-35 paths (`:56-67`, `:171`). In test D, an untracked round-36 seat report still reads
  `TARGET_MET`. That is exactly the state that let `DistillerFindings.md` sit untracked while the gate
  read `TARGET_MET` and report line 379 asserted "working tree clean". Calling this a "durability gate"
  overstates it: it re-checks round 35's D2 list, not the round's own closure.
- **Finding R5b (LOW): a missing path reads as clean.** Two of the ten listed paths,
  `.ufo/waves/round-35/scratch/RevQuoteS203/` and `…/RevQuoteS205/`, are untracked at both `a5aaa09` and
  HEAD and absent on disk (`tracked@HEAD=0 tracked@a5aaa09=0 ondisk=n`). `git status` prints nothing for
  them, so they count as clean. The before receipt's header (lines 5–6) does disclose that they were
  removed, so this is not hidden. But "absent" and "committed" give the same `0`, which goes against the
  gate's own rule at `:31` ("Absence is never a pass").
- **Positive:** test E confirms the 4d28b19 hardening. A repo with no work tree fails closed rather than reading clean.
- **The fix the spot-check routes is sufficient for R5 but not for R5a.** Committing a `git status --porcelain`
  witness only makes the round-35 list reproducible. A revision-based form would compare `ls-tree <rev>`
  against each round's own seat registry (registered reports must be tracked). That would turn R1 into
  a revision failure.

## Residual risk and verification gaps

- **Lane index.** Following the prompt, I ran plain `git -C LANE status --porcelain` (and `git status --porcelain -- <path>`)
  before I started using `GIT_OPTIONAL_LOCKS=0`. `.git/index` shows mtime `2026-10-25 09:12:59.92 -0300` (12:12:59Z),
  which falls inside my first minute. Either my `git status` refreshed the index stat cache or the L1's commit at
  09:12:46 did; I cannot tell which. In both cases only stat data changed: HEAD is unchanged and nothing is staged.
- No gate was run in LANE. Every test above ran in the `/dev/shm` sandbox. No Hyprland socket or `hyprctl` was used.
- I did not read the in-flight `ScribeErrata` draft. Whether the errata it drafts fix R2's seven lines and R3's
  single occurrence is for the scribe or integrator to check.
- Tooling: nothing installed or upgraded.
- Tool note: the Read tool rejected `DistillerFindings.md` (19,033 B) and `check-evidence-pointers.py`
  (10,369 B) as "exceeds maximum allowed characters (100000 characters)". Both files are far below that,
  so I read them with `head -c` and `nl -ba | sed -n` instead.
