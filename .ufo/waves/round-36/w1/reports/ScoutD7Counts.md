# ScoutD7Counts — re-derived per-revision w2 seat-report counts (round 35)

Scope: re-run the counting command the spot-check's defect **D7** disputes for the
three revisions it names (`4f35c80`, `7b745a1`, `7a068cb`) and bind each number to
the sentence in the round-35 report it supports (or falsifies).

## Commands and verbatim output

```
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree --name-only 4f35c80 .ufo/waves/round-35/w2/reports/ | grep -c '\.md$'
37
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree --name-only 7b745a1 .ufo/waves/round-35/w2/reports/ | grep -c '\.md$'
37
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree --name-only 7a068cb .ufo/waves/round-35/w2/reports/ | grep -c '\.md$'
40
```

Non-`.md` entries: none at any of the three revisions
(`git ls-tree --name-only <rev> … | grep -v '\.md$'` prints nothing; totals are
37 / 37 / 40 entries, all `.md`). So the `.md` filter cannot be the source of the
disputed number.

## Report sentences each count binds to

The round-35 report is `.ufo/reports/round-35/mado.md` in the **fleet** repo
(`/home/vgpnk/Projects/shokunin`), not the lane; final version read at commit
`af1e1ca5` (2026-10-25 03:52:54 -0300, "mado report — closure tip named by
command, not by a moving hash"; same text at tip version `763734e1`).

| Measured count | Revision(s) it describes | Report sentence (line @ `af1e1ca5`) | Verdict |
|---|---|---|---|
| 37 | `4f35c80` (03:42:04, "wave-2 falsifications as errata…") | line 39: `` `.ufo/waves/round-35/w2/reports/` (38 reports) `` (Work-performed bullet under "Wave 2 falsified the instruments and the text") | **contradicts** — the tree holds 37, not 38. This is D7's stale count. |
| 37 | `7b745a1` (03:42:29, "republish the axis table… plus the wave-2 reports that landed after the first pass") | line 85 (axis row): "…the committed content cribs, **the 38 wave-2 reports**, `scratch/L1DigestFix`…" attributed to `4f35c80` | **contradicts** — 37 `.md` at both `4f35c80` and `7b745a1` (identical listings; verified by diff). The row's own label `4f35c80` is the revision this count claims to describe and it is wrong there. |
| 40 | `7a068cb` (03:53:37, "round-35: close" = lane tip) | line 191: "Dead/no-report seats: wave 2 dispatched 40; **40 wrote reports** (`SentBoundary` and `ConnOverlap` landed last, after the first tally; the report was amended rather than the count prettified)." | **supports** — 40 `.md` at the tip. Dispatch side corroborates: `w2-taskcall.json` is a list of 40 tasks (spot-check line 69-70 agrees). |

## Findings

- **D7 confirmed.** The "38" figures are supported by *no* committed revision.
  A per-commit census of every commit touching `w2/reports/` shows only two
  values ever committed: **37** (`4f35c80`, `7b745a1`) then **40** (every commit
  from `b632f0b` 03:46:02 onward, including tip `7a068cb` and current HEAD
  `dbf8b57`). The listing jumps 37→40 in one step at `b632f0b`; **38 was never
  committed**. The first report draft (`fed29568`, 03:45:30) already printed
  "(38 reports)" while the lane tree still held 37, so the stale figure is a
  hand/working-tree tally carried through all nine report versions, not a count
  of any committed state.
- **The 37→40 delta is three files**, all landed between `7b745a1` and
  `b632f0b`/`7a068cb` (diff of the two listings): `ConnOverlap.md`,
  `RevScorecard.md`, `SentBoundary.md`. This matches the report's own
  parenthetical that `SentBoundary` and `ConnOverlap` "landed last" — plus a
  third (`RevScorecard`) the parenthetical does not name.
- **Which sentence each revision supports**, stated the way D7 asks:
  `4f35c80` → 37 (falsifies both "38" sentences: line 39's "(38 reports)" and
  line 85's "the 38 wave-2 reports", the latter explicitly attributing 38 to
  `4f35c80`); `7b745a1` → 37 (falsifies the same two; identical listing to
  `4f35c80`, so the "reports that landed after the first pass" named in its
  commit message did not add files to `w2/reports/`); `7a068cb` → 40 (supports
  line 191's "**40 wrote reports**").
- Minor secondary observation [OBS]: the report's line-191 excuse covers two of
  the three late reports; `RevScorecard.md` is unaccounted for in that
  parenthetical, though it is covered by the report's own line-85/table and by
  `b632f0b`'s message ("the last two seat reports (`SentBoundary`, `ConnOverlap`),
  the seats' revised reports…").

## Provenance / bounds

- Read-only everywhere; the only file written is this report. No tools installed.
- Report text read via `git show af1e1ca5:.ufo/reports/round-35/mado.md`
  (fleet repo; line numbers above are stable for `af1e1ca5`..`763734e1`, which
  carry identical count text — verified by grepping all nine report versions).
- Lane revisions confirmed as commits: `git log -1 --format='%h %ci %s'` →
  `4f35c80` 03:42:04, `7b745a1` 03:42:29, `7a068cb` 03:53:37.

Verdict: **FAIL for the report's two "38" sentences; PASS for its "40" sentence
— D7 upheld exactly as the spot-check describes.**
