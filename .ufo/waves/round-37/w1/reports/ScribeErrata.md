# ScribeErrata — round-36 errata block, mado round 37 wave 1

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, read at `master` =
`80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b`. Frozen base for the wave:
`b4e47e980bfb0cbc8a4e788f59a41db858751fd8` (`registration.md`, re-frozen as v2).

Deliverable: `.ufo/waves/round-37/w1/scratch/ScribeErrata/errata.md` — a paste-ready,
append-only `## Round 36 — errata (2026-10-25, round-37 wave 1)` block with one dated item per
defect routed in `corpus/lessons/round-36-verifier-spotcheck.md` §5 (R1–R5). Five items, each
carrying the command and the quoted output that grounds it.

## Behavior

Every routed fact was re-derived before writing, from committed bytes or from the work tree.
No lane production file was touched; `LOG.md` was not edited (the block is a draft for the
integrator to append after its current last section, `## Round 36 — correction (superseded
transcript pointer, machine form)`, `LOG.md` = 2218 lines).

Verbs used, all read-only: `git cat-file -e/-s/-t`, `git ls-tree`, `git rev-parse`,
`git merge-base --is-ancestor`, `git log`, `git show`, `git diff --stat`, and
`git --no-optional-locks status --porcelain` (the optional-locks flag so no index refresh is
written). No `git add/commit/stash/checkout/reset/push`, no jj command, no socket, no
`hyprctl`, no compositor or service touch, no subagent, no `model` parameter. No tool was
installed or upgraded, and no pacman transaction was attempted (the host-wide pause is
respected).

## Gates — per routed defect

### R1 — untracked `DistillerFindings.md` at round-36 closure — **PASS (verified; already closed this round)**

The report's clean-tree line is real and false at the tip it names:

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -e a5aaa09:.ufo/waves/round-36/w1/reports/DistillerFindings.md
# fatal: path '.ufo/waves/round-36/w1/reports/DistillerFindings.md' exists on disk, but not in 'a5aaa09'
# rc=128
git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -e 80b83c8:.ufo/waves/round-36/w1/reports/DistillerFindings.md && echo present
# present
git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -s 80b83c8:.ufo/waves/round-36/w1/reports/DistillerFindings.md
# 19033
```

The claim under correction is `.ufo/reports/round-36/mado.md:379–381`: "Lane tip at closure:
`a5aaa09ad38bfd90c13d76ccf371e36c45a2697e`, working tree clean". Disposition is commit, not
delete: `80b83c8 2026-10-25 09:12:46 -0300 round-37: the inherited round-36 DistillerFindings
seat report (spot-check R1), and the wave-1 spec, prompts, dispatch and registry (38 seats)`.
Byte count 19,033 matches the spot-check's measurement. Its scratch ledger was already tracked
at `a5aaa09` — four paths under `.ufo/waves/round-36/scratch/DistillerFindings/`
(`catalog.md`, `draft.md`, `findings.py`, `gen_report.py`).

**Errata choice:** the item does *not* write a new "working tree clean" sentence. The reading
taken while writing was `?? .ufo/waves/round-37/w1/scratch/` (this wave's in-flight scratch),
so a clean-tree assertion is a transient work-tree reading — exactly R5's defect class. The
item records the committed fact instead.

### R2 — report names `64979ef`, receipts name `4d28b193…` — **PASS (verified; erratum owed, claim unaffected)**

Report lines 196, 215, 231 name `64979ef`:

```sh
sed -n '196p;215p;231p' /home/vgpnk/Projects/shokunin/.ufo/reports/round-36/mado.md
# | The after receipts re-pinned to the hardened tip with the gate, manifest and spec digests bound | round-36 | `64979ef` |
# - after, at `64979efb7f95acc67e753c642294c41a4d102bfa` (`receipts/after-discrimination.txt`, which binds the gate, manifest and both frozen specs by sha256):
# - after, at `64979efb7f95acc67e753c642294c41a4d102bfa` (`receipts/after-pointers.txt`, which binds the gate blob by sha256):
```

Both receipts name the other revision:

```sh
grep -n '4d28b193' .ufo/waves/round-36/receipts/after-discrimination.txt .ufo/waves/round-36/receipts/after-pointers.txt
# .ufo/waves/round-36/receipts/after-discrimination.txt:5:# C1 after-state — PRED-C1-r36-v1 at 4d28b193e52f6cc8f04e81fda2664e018d62e209
# .ufo/waves/round-36/receipts/after-pointers.txt:2:# C2 after-state — PRED-PTR-r36-v1 at 4d28b193e52f6cc8f04e81fda2664e018d62e209
```

Ordering, so the erratum states the cause and not just the mismatch:

```sh
git log -1 --format='%h %ci %s' 64979efb7f95acc67e753c642294c41a4d102bfa
# 64979ef 2026-10-25 04:57:18 -0300 round-36: the after receipts re-pinned to the hardened tip with the gate, manifest and spec digests bound
git log -1 --format='%h %ci %s' 4d28b193e52f6cc8f04e81fda2664e018d62e209
# 4d28b19 2026-10-25 04:59:09 -0300 round-36: bind the manifest identity and control set to the frozen one, and make an unusable git status fail closed
git merge-base --is-ancestor 64979ef 4d28b193 && echo true
# true
```

The claim is unaffected, verified rather than inherited: the three gate blobs are identical at
`4d28b19` and `a5aaa09` — `0865b1419fae5810126850fa59a9b5b45aa7bf54`
(`quality/check-counter-discrimination.py`), `3d4e7cc0bb780fa50104fd71552b96afbdf0e7ac`
(`quality/counters/c1-idle-lock.py`), `cb0887f4ec326f7f5f3f93e4d949180d3650822a`
(`quality/counters/c2-ledger.py`). `SCORECARD.md:2324,2333` already carry `4d28b193…`.

**Unrouted finding folded in (see Findings F1):** line 303 says "the round closed on
`64979ef`", contradicting the closure tip `a5aaa09` that line 379 names. Same defect, same
cause; recorded inside the R2 item and flagged to the integrator rather than opened as a sixth
item, because the assignment scopes R1–R5.

### R3 — "six criteria (57–61)" — **PASS (verified; arithmetic is five)**

```sh
git show master:corpus/QUALITY.md | grep -c -E '^(5[7-9]|6[0-1])\.'   # 5
git show master:corpus/QUALITY.md | grep -c -E '^[0-9]+\. '           # 61
git show a3094c9:corpus/QUALITY.md | grep -c -E '^(5[7-9]|6[0])\.'    # 4
git show a3094c9:corpus/QUALITY.md | grep -c -E '^61\.'               # 0
```

`QUALITY.md` ends at criterion 61 and holds exactly five in 57–61; `57.`–`60.` land at the
data commit `a3094c9`, `61.` at the records commit `520c631`
(`git log -S '61. Every command a registration names' -- corpus/QUALITY.md` →
`520c631 2026-10-25 04:44:42 -0300 round-36: the records — LOG entry, scorecard rows, the D9
boundary ruling, the sixth mistake and the wave-1 reports so far`). `SCORECARD.md:2315` states
it correctly: "the first revision where all five new criteria, including 61, are committed".

**Refinement (F3):** the spot-check says the report says "six criteria (57–61)" twice. The
miscount occurs once — the sentence wraps at `.ufo/reports/round-36/mado.md:270–271` ("…six
mistakes are mined with fixes shown able to fail; six / criteria (57–61) and M36-6 came out of
them"). The report's other mention of the range, line 38 ("`corpus/QUALITY.md` criteria 57–61;
the S211 registry row"), carries no count and is correct. The erratum states the defect once
and records the refinement.

### R4 — S211 receipt size in the lesson — **PASS (verified; 1,037 → 1,756 B, cause dated)**

```sh
for rev in a3094c9 f77b554 master; do printf '%s: ' "$rev"; git cat-file -s $rev:.ufo/waves/round-36/fetch/S211.receipt.txt; done
# a3094c9: 1037
# f77b554: 1756
# master: 1756
git diff --stat a3094c9 f77b554 -- .ufo/waves/round-36/fetch/S211.receipt.txt
#  .ufo/waves/round-36/fetch/S211.receipt.txt | 10 ++++++++++
#  1 file changed, 10 insertions(+)
```

The 719 added bytes are the ten-line identity note headed
`# Identity note (round 36, after a non-author re-open).` added in `f77b554` (2026-10-25
04:52:45, "the S211 location and receipt-identity corrections …"). The stale claim is
`corpus/lessons/round-36.md:68` — "(1,037 B". The quoted 17-word sentence and its `§S2` /
`#P15` location are untouched by the growth, so only the size is corrected.

### R5 — `inherited_dirty` is a work-tree reading — **PASS (verified; routed as criterion 63, not landed)**

```sh
grep -rn 'inherited_dirty' .ufo/waves/round-36/receipts/
# .ufo/waves/round-36/receipts/before-pointers.txt:4:# inherited_dirty=10 (the ten round-35 paths the spot-check's D2 names: eight modified seat reports
# .ufo/waves/round-36/receipts/before-pointers.txt:8:# not a revision reading. The re-run below therefore shows inherited_dirty=0 and the four
# .ufo/waves/round-36/receipts/after-pointers.txt:4:PRED-PTR-r36-v1 rev=master pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=35 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET
```

The after receipt prints `inherited_dirty=0` beside `rev=master`, which reads as a property of
the revision when it is a property of the checkout. What this round does, stated in the item:
route it as `corpus/QUALITY.md` criterion **63** (witness for work-tree observables), drafted by
seat ScribeQuality — its prompt is committed at `80b83c8`
(`.ufo/waves/round-37/w1/prompts/ScribeQuality.md`) and its text is "a receipt observable read
from the working tree (e.g. `git status`) commits the raw witness beside the receipt, so the
reading re-derives from committed bytes (round-36 spot-check R5)". Criterion 63 is routed, not
landed: `QUALITY.md` at `master` still ends at 61 (R3's count) and
`.ufo/waves/round-37/w1/scratch/ScribeQuality/` did not exist at the time of writing. The
round-36 receipts are not edited.

## Findings beyond the routed set

- **F1 — a fourth stale revision, not routed.** `.ufo/reports/round-36/mado.md:303` reads "the
  round closed on `64979ef`, and any report not in that commit is not claimed", while the
  closure tip is `a5aaa09` (`git log -1 --format='%h %ci'` → `a5aaa09 2026-10-25 05:40:10
  -0300`; the fleet report commit `b26422a6` follows at `05:40:34`). Folded into the R2 item
  and flagged here for the integrator: the spot-check's R2 wording covers only lines
  196/215/231.
- **F2 — a clean-tree sentence is transient, and I have the demonstration.** My first
  `git --no-optional-locks status --porcelain` in this lane returned no output; the same
  command minutes later returned `?? .ufo/waves/round-37/w1/scratch/` once wave scratch
  appeared. The errata therefore asserts no clean tree. This is first-hand evidence for R5's
  criterion 63: a work-tree observable must carry its raw witness.
- **F3 — the spot-check's R3 count.** "Twice" is once; the second mention carries no count
  (details under R3).
- **F4 — one-second drift in the spot-check.** §1 gives the lane tip as committed 05:40:09;
  measured 05:40:10. Immaterial, and the errata quotes the measured value rather than
  repeating the spot-check's.
- **R1's disposition was already done before this seat ran.** The artifact was committed in
  `80b83c8`, the round-37 opening commit, so the errata records a completed fix rather than a
  plan.

## Touched surfaces

Written (only these two):

- `.ufo/waves/round-37/w1/scratch/ScribeErrata/errata.md` — the deliverable, 8,731 B at first
  write, 188 lines / 10,711 B after eight in-place edits (quoted-output form of the three
  `rev-parse` calls, the `:379–381` citation, the verbatim line-196 quote, the R4 `diff --stat`
  evidence, the R1 clean-tree correction, criterion 61's commit, the R2 line-303 sentence, the
  closure timestamps).
- `.ufo/waves/round-37/w1/reports/ScribeErrata.md` — this report.

Read-only: lane `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-36.md`,
`corpus/lessons/round-36-verifier-spotcheck.md`, `.ufo/waves/round-36/receipts/*`,
`.ufo/waves/round-36/fetch/S211.receipt.txt`, `.ufo/waves/round-37/registration.md`,
`.ufo/waves/round-37/w1/prompts/Scribe{Errata,Quality}.md`, lane git object database, and the
fleet report `.ufo/reports/round-36/mado.md`.

## Out of scope / not done

- `LOG.md` is not edited — the block is a draft for the integrator to append (append-only,
  after `LOG.md:2218`). No production file, counter, corpus entry or receipt was modified.
- Spot-check §5 item 6 (manifest identity, exit/verdict coherence, the three-substring
  transcript, control order, the inherited `check-index-rows.py` rev-mode defect, the
  generator's `/tmp` traversal, the digest clause's anchor half) is already lane-routed and
  named in the round-36 report; it is carried forward there and is explicitly excluded from
  this block.
- Criterion 63 is not landed; no QUALITY.md criterion, scorecard row or gate receipt is
  claimed. No gate, selftest, counter or controls run was executed by this seat, and none is
  claimed as passed.
- No claim is made about the round-36 verdicts themselves; the errata records record defects
  only, and states for R2 that the claim is unaffected because the gate blobs are identical.

## Artifact paths (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`)

- `.ufo/waves/round-37/w1/scratch/ScribeErrata/errata.md` — the errata block, 5 dated items.
- `.ufo/waves/round-37/w1/reports/ScribeErrata.md` — this report.
