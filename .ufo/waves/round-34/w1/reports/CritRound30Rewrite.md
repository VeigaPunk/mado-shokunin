# CritRound30Rewrite — provenance critique of the five round-30 seat reports committed at `d40b35f`

Seat: CritRound30Rewrite (round-34 w1, critic). Scope: the five files under
`.ufo/waves/round-30/w1/reports/` that `d40b35f90ad8bf630ad9404d25aeee1d9737f300`
("round-33: correct the false r32 C1 row, register the axis gate, and keep the
killed coverage counter frozen") committed or rewrote. Question per file: could
the current bytes have been produced by the original round-30 seat? Read-only;
zero lane writes outside this report.

## Headline

All five are authentic round-30 seat output. `d40b35f` did not author the
bytes — it swept late-finishing, self-declared final passes into history. The
rewrite is legitimate, and the round-30 content is usable — **provided** round-34
cites it at `d40b35f` (or HEAD), never at the round-30 commits.

## Evidence (all commands re-run at write time)

1. **Current bytes = `d40b35f` bytes.** `git status --porcelain` on
   `.ufo/waves/round-30/w1/reports/` is empty; `git diff d40b35f..HEAD` on those
   paths is empty. HEAD `fa7ba11346116672352b5d41494141c5c4d738d0`; `d40b35f` is
   an ancestor (`git merge-base --is-ancestor` exit 0).
2. **Round-30 lineage.** `git log --` on each path: `RevRecordsChain` has
   `a0dd664` + `274f735` committed passes, `RevTrendExpansion` a `274f735` pass,
   `SentScope` a `15ddd7d` pass; `RevTrendDiscernment` and `SimplifierC2` have no
   history before `d40b35f`.
3. **mtimes inside the round-30 repair window.** `stat`: SimplifierC2 04:15:26,
   SentScope 04:16:09, RevRecordsChain 04:16:25, RevTrendExpansion 04:16:41,
   RevTrendDiscernment 04:17:11 — 2–9 min after tip `274f735` (04:13:42) and ~17h
   before `d40b35f` (21:08:35). Files were untouched between round-30 and the
   round-33 sweep.
4. **Zero post-round-30 content.** Grep for every round-31/32/33 commit short-hash
   and `round-3[1-9]`/`d40b35f` across all five files: no hits. Every internal
   pin names `15ddd7d`, `a0dd664`, `274f735`, or round-30 blob shas
   (`cbc2941b`, `fc4a10a2`, `373680fe`, `51b513f5`, `74a4859`, `df01b20f`) —
   all real round-30 objects.
5. **Seats were registered.** `swarm-registry.json` in the same wave dir carries
   all five seat names (2 hits each) — none is a stray file.

## Per-file verdict

| File | Could the round-30 seat have written it? | Basis |
|---|---|---|
| `RevRecordsChain.md` | **Yes** — final pass by the same registered seat; supersedes its own `a0dd664`/`274f735` committed passes | declares "This file's committed copies at `a0dd664`/`274f735` are earlier passes of the same seat; this revision is final"; reviews tip `274f735` (8 commits) with real subject lines |
| `RevTrendExpansion.md` | **Yes** — second pass by the same seat; supersedes the `274f735` draft | opens "This file supersedes my first pass, which commit `274f735` committed"; verdict sharpened to `unchanged`, adds r19 control (`SCORECARD.md:1159-1163`) |
| `RevTrendDiscernment.md` | **Yes** — first and only committed pass; untracked until `d40b35f` | "Revision reviewed: lane `274f735`"; timing evidence entirely within round-30 (report `bbae16bf` 04:00:43 vs spot-check `d72243e` 04:03:37); complete, ends "No tools were installed or updated by this seat." |
| `SentScope.md` | **Yes** — expanded revision by the same seat; supersedes the `15ddd7d` pass | §0 baseline-movement table tracks the freeze `451e8b3`→`a0dd664`; F-set re-audited at `a0dd664` with new F12 (frozen-instrument churn during the repair window — content only writable inside it) |
| `SimplifierC2.md` | **Yes** — first and only committed pass; untracked until `d40b35f` | mutants pinned to committed round-30 blobs (`fc4a10a2`, `373680fe`, `51b513f5`); addendum tracks tip `a0dd664a`→`274f7355`; file is whole (see dispute below) |

Caveat on "produced by the seat": the uncommitted window (~17h) means git proves
*when* the bytes last changed and *when* they were committed, not *which process*
wrote them. There is no evidence of tampering — every content anchor resolves to
round-30 objects and no post-`274f735` event is referenced — so "could have been
written by the round-30 seat" holds for all five.

## What `ScoutRound30.md` says

Exists: `.ufo/waves/round-33/w1/reports/ScoutRound30.md` (committed at
`69f72100bee31a60b811f8fbbe7796db883e17b3`; not part of `d40b35f` — the scout
reported while the files were still dirty). Verdict: "**all five are real seat
reports. Recommend commit (all five).**" Its `git status` matrix (`M`/`M`/`M`/
`??`/`??`), distinguishing quotes, tail-completeness checks, and blob-hash
spot-checks all reproduce under independent re-run this session. Companion
review `ReviewRound30.md` (same commit) independently reached the same
commit-all verdict without reading the scout.

**Scout vs reviewer dispute, resolved:** `ReviewRound30.md` claims SimplifierC2's
trailing addendum is "cut mid-sentence ('…they were made aga')". Verified false:
`tail -c` on current bytes ends "…HEAD has since advanced again (`274f7355`);
this report intentionally pins revisions, not tip." — complete sentence, file
ends with newline, 11,342 B. The reviewer read a line-truncated view. Scout's
"file is whole" is correct; cite SimplifierC2's tail freely.

## Exact citation required in round-34 reports

Whenever a round-34 report relies on any of the five files' current content:

> `.ufo/waves/round-30/w1/reports/<file>.md` **@ `d40b35f90ad8bf630ad9404d25aeee1d9737f300`**
> (or `@ HEAD`) — full hash, per lane rule "cite commits by full hash".

Rationale: `git show 15ddd7d:`/`a0dd664:`/`274f735:` on these paths yields
superseded drafts (three files) or nothing (two). Only `d40b35f` and descendants
contain the bytes at the path today. Internal revision anchors *inside* the
files (e.g., "at `a0dd664`") are the seats' own measurement pins — legitimate as
content, but never as the citation for the file itself. This matches the
connector's sentence in `ConnRound30Cite.md`: earlier committed drafts are
superseded and must not be quoted.

## Risks noted

- The files cross-reference each other (`RevRecordsChain` cites SentScope's
  F-set; `SimplifierC2`'s addendum references RevC1Fence S1–S5) — cite them as
  one coherent set at `d40b35f`, not piecemeal at mixed revisions.
- Round-30's append-later discipline (final passes committed a round late) is
  now in-file-disclosed; round-34 quoting tools must read HEAD or `d40b35f`
  blobs, never round-30 blobs, for these five paths.
- No `.ufo/history-pin.json` exists in this lane repo; the rewrite broke no pin.
