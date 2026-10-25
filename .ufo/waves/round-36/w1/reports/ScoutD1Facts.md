# ScoutD1Facts — re-derived round-35 report-ordering facts (D1)

Scope: re-derive the ordering facts behind the spot-check's defect **D1**
(report-lands-last and tip citation) from both repos' git history, enumerate
every lane commit after the report's first commit, and state the erratum the
round-36 report owes. Read-only pass; this file is the only write.

## Commands and verbatim output

```
$ git -C /home/vgpnk/Projects/shokunin log -1 --format='%H %ad' --date=iso -- .ufo/reports/round-35/mado.md
763734e1b909218e87d1192c1b236b2b575b7ea1 2026-10-25 03:53:03 -0300
```

```
$ git -C /home/vgpnk/Projects/shokunin log --diff-filter=A --format='%H %ai %ci %s' -- .ufo/reports/round-35/mado.md
fed29568e45298ceaed33a580a1842ad57547004 2026-10-25 03:45:27 -0300 2026-10-25 03:45:30 -0300 round-35: mado report
```

```
$ cd mado-shokunin && git log --format='%h %ai %s' --grep='round-35' 4243d03 | head -3
4243d03 2026-10-25 03:53:57 -0300 round-35 verifier spot-check (integrator, hyaku): non-author admit/reject
7a068cb 2026-10-25 03:53:37 -0300 round-35: close
2eddc38 2026-10-25 03:53:32 -0300 round-35: final seat touch
```

```
$ git log -1 --format='parents: %P' <each>
7a068cb → parent 2eddc38 → parent 567945e → parent ee22d39 → parent 2909fea
$ git merge-base --is-ancestor 7a068cb 4243d03 && echo YES
YES   (the round-35 tip is the spot-check commit's direct parent)
```

## Re-derived facts

**1. Last round-35-labelled commit on `master` before the spot-check:**
`7a068cbee3b0983230b8fb8467c02e12772832dd` — "round-35: close",
author = committer = `2026-10-25 03:53:37 -0300`. It is the parent of the
spot-check commit `4243d03` itself (which also carries a round-35 label, so
"before the spot-check" is what excludes it). Matches spot-check line 8 and
`corpus/lessons/round-35-verifier-spotcheck.md:215`. **CONFIRMED.**

**2. Commit the prompt's command returns vs. commit that added the file:**
`log -1` returns `763734e1b909218e87d1192c1b236b2b575b7ea1` — the **last**
toucher of the report (author `03:53:03`, committer `03:53:15`), not the adder.
The actual adding commit (`--diff-filter=A`) is
`fed29568e45298ceaed33a580a1842ad57547004` (author `03:45:27`, committer
`03:45:30`). Nine commits total touch the file, all `mado-shokunin
<mado@shokunin.local>`; the only other mado-identity fleet commits in the
round window are the two dispatch-evidence commits `01d79d84` (23:14:02) and
`cca52393` (03:23:34), both *before* the report's first commit — so no
non-report fleet writes interleave the report window.

**3. Every lane commit after the report's first commit** (after
`fed2956`'s author time `03:45:27`), author-date order:

| # | commit | author date | committer date | subject |
|---|---|---|---|---|
| 1 | ca870e9 | 03:46:45 | 03:46:46 | fold the seats' post-sweep revisions and rebuilt evidence |
| 2 | 1bb25c7 | 03:47:25 | 03:47:25 | closing report revisions and the last rebuilt evidence |
| 3 | ae34886 | 03:47:46 | 03:47:46 | final sweep — the seats' last report revisions and evidence |
| 4 | a80f8cb | 03:48:57 | 03:48:57 | seat report revisions and evidence subdirs, swept once more |
| 5 | 7d708cf | 03:51:06 | 03:51:25 | correct the scorecard's axis-publication commits… (RevScorecard F1-F3, F7) |
| 6 | 33c885b | 03:51:38 | 03:51:38 | the last seat report revision |
| 7 | 800c935 | 03:51:47 | 03:51:47 | close — the final two seat report revisions |
| 8 | 25536e6 | 03:51:53 | 03:51:53 | closure sweep |
| 9 | d7339fa | 03:52:45 | 03:52:45 | seat report revisions at close |
| 10 | 2909fea | 03:52:52 | 03:52:52 | last report touch |
| 11 | ee22d39 | 03:53:13 | 03:53:13 | record the row-section gap RevC1Tip routed (C1 whole-file scan vs census E12) |
| 12 | 567945e | 03:53:13 | 03:53:26 | seat report revisions arriving at close |
| 13 | 2eddc38 | 03:53:32 | 03:53:32 | final seat touch |
| 14 | 7a068cb | 03:53:37 | 03:53:37 | round-35: close (**the tip**) |

= **14 commits** by author date. By committer date add `b632f0b` (author
03:45:15 **<** 03:45:27, committer 03:46:02 **>** the add's commit time
03:45:30) → 15.

**4. Lane commits after the report's *last* commit** (`763734e1`):

- By **author** date: `ee22d39` (03:53:13), `567945e` (03:53:13), `2eddc38`
  (03:53:32), `7a068cb` (03:53:37) — **4 commits**.
- By **committer** date: `567945e` (03:53:26), `2eddc38` (03:53:32),
  `7a068cb` (03:53:37) — **3 commits**; `ee22d39`'s committer date (03:53:13)
  precedes the report's committer date (03:53:15).

The spot-check (`round-35-verifier-spotcheck.md:59-63, 214`) enumerates three
("`567945e`, `2eddc38` and the tip `7a068cb`") while quoting the report's
*author* date 03:53:03. So either its enumeration mixes clocks (author date
for the report, committer ordering for the lane) or it missed `ee22d39`,
which is authored 10 s after the report's author date. [INF] The verdict is
unchanged under both clocks; under author-date semantics D1 is one commit
larger than written.

## Did the report land last?

**No — FAIL.** Under either clock, lane work was committed after the final
report write: tip `7a068cb` (03:53:37) postdates `763734e1` by 34 s (author)
or 22 s (committer). The interleave is deeper than the tail: lane commits
`33c885b`→`2909fea` (rows 6–10) were written *between* report revisions
`15153525` (03:46:57) and `af1e1ca5`/`69f46e5` (03:52:15–17), i.e. the report
was being amended while the lane it describes was still moving — its own
commit `af1e1ca5` says "closure tip named by command, not by a moving hash"
and never names `7a068cb`.

## Round-35 lane tip hash

`7a068cbee3b0983230b8fb8467c02e12772832dd` (`master`, pushed, `ahead=0` at
closure per spot-check line 46; direct parent of spot-check `4243d03`).

## The one-sentence erratum round 36 owes

> The round-35 lane tip is `7a068cbee3b0983230b8fb8467c02e12772832dd`
> ("round-35: close", committed 2026-10-25 03:53:37 -0300): the round-35
> report's last commit `763734e1` preceded it and cited no tip hash —
> routed as spot-check defect D1, corrected here.

## Findings

- **D1 upheld, sharpened.** The report did not land last and names no tip
  hash — confirmed from raw history on both repos. Under author-date
  semantics the tail after the report is 4 commits, not the spot-check's 3
  (`ee22d39` authored 03:53:13 > report author 03:53:03). Under committer-date
  semantics it is exactly the spot-check's 3. Either way: FAIL.
- **Author/committer skew is systemic in the close-out window** [OBS]:
  `567945e` (author 03:53:13 / committer 03:53:26), `4243d03` (author
  03:53:57 / committer 04:01:39), `dbf8b57` (author 04:01:39 / committer
  04:24:12), `a3094c9`, `2d90524` — each commit is authored minutes before it
  is committed, as if written to a detached staging ref and replayed. The
  spot-check's "after the report's last commit" enumeration is consistent
  only under committer dates. Worth one clause in any future ordering spec:
  name the clock.
- **Prompt precision note:** the assigned command `log -1` returns the last
  toucher `763734e1`, not the adder; the true adder `fed2956` requires
  `--diff-filter=A`. Both are reported above.
- **Live-repo note:** lane `master` advanced during this pass (`dbf8b57` →
  `a3094c9` → `2d90524`, all `round-36:` commits); every round-35 fact above
  is a historical commit and unaffected.

## Provenance / bounds

- Read-only everywhere; no tool installs; only file written is this report.
- All hashes re-derived by direct `git log`/`merge-base`/`cat-file`
  equivalents quoted above — not copied from the spot-check (though they
  agree where the spot-check is precise).

Verdict: **FAIL — the report did not land last; round-35 tip =
`7a068cbee3b0983230b8fb8467c02e12772832dd`; erratum sentence as above.**
