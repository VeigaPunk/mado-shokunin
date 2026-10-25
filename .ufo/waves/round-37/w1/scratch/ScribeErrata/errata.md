## Round 36 — errata (2026-10-25, round-37 wave 1)

Append-only. Each item below corrects one defect routed in
`corpus/lessons/round-36-verifier-spotcheck.md` §5 (R1–R5); nothing above this heading is
edited, and the round-36 report itself — `.ufo/reports/round-36/mado.md` in the fleet repo —
is never edited, so every correction lives here. Each fact was re-derived before writing, from
committed bytes (`git cat-file`, `git ls-tree`, `git rev-parse`) or from the lane work tree
with `git --no-optional-locks status --porcelain`; the command and its output are quoted in
the item that uses them. §5's item 6 (manifest identity, exit-code/verdict coherence, the
three-substring transcript, the control order, the inherited `check-index-rows.py` rev-mode
defect, the generator's `/tmp` traversal, the digest clause's anchor half) was already
lane-routed and named in the round-36 report; it is carried forward there and is not part of
this block.

### R1 — the close claimed a clean tree over an untracked seat report (2026-10-25)

**The defect.** The round-36 report's closing line reads

> Lane tip at closure: `a5aaa09ad38bfd90c13d76ccf371e36c45a2697e`, working tree clean; the gate
> re-reads `TARGET_MET` at this tip.

(`.ufo/reports/round-36/mado.md:379–381`.) The tree was not clean: the seat report
`.ufo/waves/round-36/w1/reports/DistillerFindings.md` (19,033 B) was untracked at that tip.
Committed bytes show it — the path exists on disk and not in the revision:

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -e \
  a5aaa09:.ufo/waves/round-36/w1/reports/DistillerFindings.md
# fatal: path '.ufo/waves/round-36/w1/reports/DistillerFindings.md' exists on disk, but not in 'a5aaa09'   (rc 128)
git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -e \
  80b83c8:.ufo/waves/round-36/w1/reports/DistillerFindings.md && echo present
# present
```

The clean-tree assertion is false as written and is corrected here, not rewritten in place.

**What round 37 does.** Commits the artifact rather than deleting it, in `80b83c8`
(2026-10-25 09:12:46 -0300, "round-37: the inherited round-36 DistillerFindings seat report
(spot-check R1), and the wave-1 spec, prompts, dispatch and registry (38 seats)"), at the same
byte count the spot-check measured:

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -s 80b83c8:.ufo/waves/round-36/w1/reports/DistillerFindings.md
# 19033
```

No round-36 artifact is untracked any more. This erratum deliberately does **not** write
"working tree clean": a clean-tree sentence is a point-in-time reading of the work tree, which
is exactly the defect class R5 records below. The reading taken while writing this block, for
the record and not as a claim about closure:

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin --no-optional-locks status --porcelain
# ?? .ufo/waves/round-37/w1/scratch/
```

— the only untracked path is this wave's own in-flight scratch directory. The seat's scratch
ledger was already tracked at `a5aaa09`: the four paths under
`.ufo/waves/round-36/scratch/DistillerFindings/` (`catalog.md`, `draft.md`, `findings.py`,
`gen_report.py`) resolve at `master`, which is what
`git ls-tree -r master --name-only | grep 'round-36/scratch/DistillerFindings/'` prints.

### R2 — the report's after-state revision is one commit behind its receipts (2026-10-25)

**The defect.** Three places in the round-36 report name the after state at `64979ef`:
line 196 (`| The after receipts re-pinned to the hardened tip with the gate, manifest and spec
digests bound | round-36 | \`64979ef\` |`), line 215 ("after, at
`64979efb7f95acc67e753c642294c41a4d102bfa` (`receipts/after-discrimination.txt`, which binds the
gate, manifest and both frozen specs by sha256)") and line 231 (the same form for
`receipts/after-pointers.txt`). The receipts name a later revision:

```sh
grep -n '4d28b193' .ufo/waves/round-36/receipts/after-discrimination.txt .ufo/waves/round-36/receipts/after-pointers.txt
# .ufo/waves/round-36/receipts/after-discrimination.txt:5:# C1 after-state — PRED-C1-r36-v1 at 4d28b193e52f6cc8f04e81fda2664e018d62e209
# .ufo/waves/round-36/receipts/after-pointers.txt:2:# C2 after-state — PRED-PTR-r36-v1 at 4d28b193e52f6cc8f04e81fda2664e018d62e209
```

`64979ef` is the tip as of the report's writing (2026-10-25 04:57:18); `4d28b19` is the commit
the receipts were finally measured at (04:59:09), one commit later, and `64979ef` is its
ancestor (`git merge-base --is-ancestor 64979ef 4d28b193` → true). `SCORECARD.md` already
carries the corrected hash (lines 2324, 2333: "After at `4d28b193…` (the revision both receipts
name…)").

**Erratum.** The after state the two receipts measure is `4d28b193e52f6cc8f04e81fda2664e018d62e209`.
`64979ef` is a real ancestor commit, but it is not the revision the receipts bind, and no
receipt at `64979ef` is claimed.

The report's other `64979ef` mentions are tip/ancestry references, not after-state claims
(lines 6, 339, 381), with one exception the spot-check did not route: line 303 says "the round
closed on `64979ef`, and any report not in that commit is not claimed", while line 379 names
`a5aaa09ad38bfd90c13d76ccf371e36c45a2697e` as the closure tip and the closure tip is
`a5aaa09` (`git log -1 --format='%h %ci'` → `a5aaa09 2026-10-25 05:40:10 -0300`; the fleet
report commit `b26422a6` follows at `05:40:34`). Line 303's revision is
stale by the same cause as the three above; the erratum is recorded here rather than in a new
item because it is the same defect, and it is flagged to the integrator as not part of the
spot-check's R2 wording.

**The claim is unaffected.** The three gate blobs are byte-identical at the two revisions:

```sh
git rev-parse 4d28b19:quality/check-counter-discrimination.py a5aaa09:quality/check-counter-discrimination.py
# 0865b1419fae5810126850fa59a9b5b45aa7bf54
# 0865b1419fae5810126850fa59a9b5b45aa7bf54
git rev-parse 4d28b19:quality/counters/c1-idle-lock.py a5aaa09:quality/counters/c1-idle-lock.py
# 3d4e7cc0bb780fa50104fd71552b96afbdf0e7ac
# 3d4e7cc0bb780fa50104fd71552b96afbdf0e7ac
git rev-parse 4d28b19:quality/counters/c2-ledger.py a5aaa09:quality/counters/c2-ledger.py
# cb0887f4ec326f7f5f3f93e4d949180d3650822a
# cb0887f4ec326f7f5f3f93e4d949180d3650822a
```

so the `14/25 → 25/25` re-measurement stands at the revision the receipts name.

### R3 — "six criteria (57–61)" is five (2026-10-25)

**The defect.** The report's quality trend line reads "six mistakes are mined with fixes shown
able to fail; six / criteria (57–61) and M36-6 came out of them"
(`.ufo/reports/round-36/mado.md:270–271`, the sentence wrapping across the two lines). The
range `57–61` holds five numbers. `corpus/QUALITY.md` at `master` holds exactly those five and
no more:

```sh
git show master:corpus/QUALITY.md | grep -c -E '^(5[7-9]|6[0-1])\.'   # 5
git show master:corpus/QUALITY.md | grep -c -E '^[0-9]+\. '           # 61
```

— `57.`, `58.`, `59.`, `60.` landed at the data commit `a3094c9`; `61.` at the records commit
`520c631` (`git log -S '61. Every command a registration names' -- corpus/QUALITY.md` →
`520c631 2026-10-25 04:44:42 -0300 round-36: the records — LOG entry, scorecard rows, the D9
boundary ruling, the sixth mistake and the wave-1 reports so far`). `SCORECARD.md`
states it correctly at line 2315: "the first revision where all five new criteria, including
61, are committed". **Erratum: five criteria, 57–61.** Refinement on the spot-check's wording:
the miscount appears once (line 271, with the word "six" ending line 270); the report's other
mention of the range, line 38 ("`corpus/QUALITY.md` criteria 57–61; the S211 registry row"),
carries no count and is correct as written.

### R4 — the lesson's S211 receipt size is stale (2026-10-25)

**The defect.** `corpus/lessons/round-36.md:68` says the receipt
`.ufo/waves/round-36/fetch/S211.receipt.txt` is "(1,037 B". At the tip it is 1,756 B, and the
growth is dated:

```sh
for rev in a3094c9 f77b554 master; do printf '%s: ' "$rev"; \
  git cat-file -s $rev:.ufo/waves/round-36/fetch/S211.receipt.txt; done
# a3094c9: 1037
# f77b554: 1756
# master: 1756
git log --format='%h %ci %s' -- .ufo/waves/round-36/fetch/S211.receipt.txt
# f77b554 2026-10-25 04:52:45 -0300 round-36: the S211 location and receipt-identity corrections, the adjacency boundaries, the after receipts at the tip, and the wave reports landed
# a3094c9 2026-10-25 04:37:14 -0300 round-36: the repaired counters, the r36 ledgers, the discrimination receipts, the lesson, four criteria and one source row
```

**Erratum: 1,037 B is the receipt at the data commit `a3094c9`; the receipt at the tip is
1,756 B**, the extra 719 B being the receipt-identity note added in `f77b554`:

```sh
git diff --stat a3094c9 f77b554 -- .ufo/waves/round-36/fetch/S211.receipt.txt
#  .ufo/waves/round-36/fetch/S211.receipt.txt | 10 ++++++++++
#  1 file changed, 10 insertions(+)
```

— ten added lines, headed `# Identity note (round 36, after a non-author re-open).` The quoted
17-word sentence and its `§S2` / `#P15` location are unchanged by the growth.

### R5 — `inherited_dirty` is a work-tree reading, not a revision reading (2026-10-25)

**The defect.** C2's pointer gate carries an observable measured from `git status` on the work
tree, so the after-state is not fully reproducible from committed bytes. The before receipt
discloses it for its own state only:

> `# inherited_dirty=10 (the ten round-35 paths …)`
> `# not a revision reading. The re-run below therefore shows inherited_dirty=0 …`

(`.ufo/waves/round-36/receipts/before-pointers.txt:4,8`.) The after receipt prints it as a
plain field beside a revision — `PRED-PTR-r36-v1 rev=master … inherited_dirty=0 … verdict=TARGET_MET`
(`.ufo/waves/round-36/receipts/after-pointers.txt:4`) — which reads as a property of `master`
when it is a property of the checkout that ran it.

**What this round does — route it as a QUALITY criterion, not fix it in place.** The round-36
receipts are not edited; the rule that prevents a recurrence is drafted as `corpus/QUALITY.md`
criterion **63** by seat ScribeQuality in this wave ("a receipt observable read from the working
tree (e.g. `git status`) commits the raw witness beside the receipt, so the reading re-derives
from committed bytes (round-36 spot-check R5)", prompt committed at `80b83c8`:
`.ufo/waves/round-37/w1/prompts/ScribeQuality.md`). Criterion 63 is routed, not landed: at the
time of writing `corpus/QUALITY.md` at `master` still ends at 61 (see R3's count), so this
erratum records the route and the seat's draft path
`.ufo/waves/round-37/w1/scratch/ScribeQuality/criteria.md`, not a completed fix.
