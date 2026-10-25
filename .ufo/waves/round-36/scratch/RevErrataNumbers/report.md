# RevErrataNumbers — D1 / D6 / D7 re-derived from git alone

Seat: L1Mado36.RevErrataNumbers (reviewer, round 36, residual attack pass).
Scope: READ-ONLY on production files. Every number below was produced by the command printed
next to it, in this session, against the lane repo
`/home/vgpnk/Projects/shokunin/mado-shokunin` (LANE) and the fleet repo
`/home/vgpnk/Projects/shokunin` (FLEET).

The round-36 report does not exist yet (`LANE/.ufo/waves/round-36/` holds only `registration.md`,
`w1/`, `w2/`-era scratch and `ledger/`), and no errata draft exists either:

    $ find /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-36 -name '*errata*'
    (no output)

    $ ls /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-36/scratch/
    MutC1CheckAnchor  MutPublication  RevSelftest  RevSourceS211  ScoutD9Provenance  ScoutPriorArt2  ScribeQualityRatio
    (no ScribeReportErrata/)

So the question "would the report's erratum text be true" is judged against the content the round
mandates for the three items (the scribe item at
`.ufo/waves/round-36/w1/prompts/ScribeReportErrata.md`: D1 tip + report-ordering admission, D6
corrected row-correction count with its `git diff --numstat`, D7 per-revision counts), not against
draft prose that exists.

---

## D1 — round-35 lane tip and report ordering

### D1.1 What the lane log says

    $ git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --format='%H %ad %s' --date=iso -25
    2d905245b6a964e707139ff099265345bfed1854 2026-10-25 04:46:50 -0300 round-36: the after receipts, the measured-at block, the round-37 plan and the S211 corroboration
    cf175c716faecec78f97258851c4ca353dea8b0b 2026-10-25 04:45:47 -0300 round-36: the D9 census in the lesson, decoupled from a pending seat report
    c5d77733f54150a408185ecbe075c427acca10ca 2026-10-25 04:45:18 -0300 round-36: the superseded transcript pointer in machine form, and the wave-1 reports that landed
    ebc54371f5752c86697aaa2b752e9170ee8073db 2026-10-25 04:44:42 -0300 round-36: the tip-revision axis transcript and the two LOG corrections (D10 path, M36-6)
    520c631d2925807aadadb041eeda13f8b829b0c5 2026-10-25 04:44:42 -0300 round-36: the records — LOG entry, scorecard rows, the D9 boundary ruling, the sixth mistake and the wave-1 reports so far
    a3094c99ab85bec35534de2447552c47dd2b647f 2026-10-25 04:24:12 -0300 round-36: the repaired counters, the r36 ledgers, the discrimination receipts, the lesson, four criteria and one source row
    dbf8b579aeac0f023aaf595770f1cb0049e4baa2 2026-10-25 04:01:39 -0300 round-36: freeze both predicates, the control manifest, the cribs and the before receipts
    4243d031e3441f5063f92c33aa58377c6f9ff120 2026-10-25 03:53:57 -0300 round-35 verifier spot-check (integrator, hyaku): non-author admit/reject
    7a068cbee3b0983230b8fb8467c02e12772832dd 2026-10-25 03:53:37 -0300 round-35: close
    2eddc38e2641b088767b91f03c1f104687c5897e 2026-10-25 03:53:32 -0300 round-35: final seat touch
    567945ea48bbee78bd098c185b27cb84953f779f 2026-10-25 03:53:13 -0300 round-35: seat report revisions arriving at close
    … (round-35 tail as quoted in the round-35 report)

`master` == `origin/master` == `2d905245b6a964e707139ff099265345bfed1854` (2026-10-25 04:46:50).

### D1.2 Is `7a068cbe…` the last round-35-labelled commit on the branch? **No — `4243d031…` is.**

    $ git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --format='%h %ad %s' --date=iso --grep='round-35'
    4243d03 2026-10-25 03:53:57 -0300 round-35 verifier spot-check (integrator, hyaku): non-author admit/reject
    7a068cb 2026-10-25 03:53:37 -0300 round-35: close
    2eddc38 2026-10-25 03:53:32 -0300 round-35: final seat touch
    … 20 commits carrying the label in total (4f35c80 … 4243d03)

    $ git -C … show -s --format='commit %H%nauthor %an <%ae> %ad%ncommitter %cn <%ce> %cd%nsubject %s%nparents %P' --date=iso 4243d031
    commit 4243d031e3441f5063f92c33aa58377c6f9ff120
    author protocol-shokunin <protocol@shokunin.local> 2026-10-25 03:53:57 -0300
    committer protocol-shokunin <protocol@shokunin.local> 2026-10-25 04:01:39 -0300
    subject round-35 verifier spot-check (integrator, hyaku): non-author admit/reject
    parents 7a068cbee3b0983230b8fb8467c02e12772832dd

    $ git -C … show --stat --format='' 4243d031
     corpus/lessons/round-35-verifier-spotcheck.md | 270 ++++++++++++++++++++++++++
     1 file changed, 270 insertions(+)

    $ git -C … branch -r --contains 4243d031
      origin/HEAD -> origin/master
      origin/master

The repo's *own* definition of "last round-N-labelled commit" includes these integrator commits.
Round 35's spot-check D4 states it outright:

    kama… (lane) corpus/lessons/round-35-verifier-spotcheck.md D4:
    "the pinned `r34_tip` (`dff3941`) is not the last round-34-labelled commit (`6d754bd`, 17m37s later,
     identical blob ids)"

    $ git -C … log --format='%h %ad %s' --date=iso --grep='round-34' | head -2
    6d754bd 2026-10-24 23:04:26 -0300 round-34 verifier spot-check (integrator, hyaku): non-author admit/reject
    dff3941 2026-10-24 22:46:39 -0300 round-34: the lesson, the log entry, and the round-34 claim rows

    $ git -C … log -1 --format='%h author=%ai committer=%ci' dff3941
    dff3941 author=2026-10-24 22:46:39 -0300 committer=2026-10-24 22:46:49 -0300

`6d754bd` — the "last round-34-labelled commit" in D4 — is a `round-34 verifier spot-check` commit,
i.e. exactly the shape of `4243d031` for round 35. `dff3941` committer 22:46:49 → `6d754bd`
23:04:26 is 17m37s, so the precedent also pins the clock convention (committer dates) that turns
`7a068cb` 03:53:37 → `4243d03` 04:01:39 into 8m02s on the same convention (20 s on author dates).

`7a068cb` is true only under a narrower claim:

- last commit with the strict `round-35:` prefix (lane work commits) — 7a068cb, "round-35: close";
- the lane tip at the hyaku closure dispatch — the fleet dispatch commit `e11524e3`
  (2026-10-25 03:53:39) postdates 7a068cb (03:53:37) by 2 s and predates 4243d031 (author
  03:53:57);
- never "the last round-35-labelled commit on the branch" — that is 4243d031, 20 s (author) /
  7m42s (committer) later, pushed, and the direct child of 7a068cb.

**Verdict: FALSIFIED as worded.** The erratum text "7a068cbe… is the last round-35-labelled commit
on the branch" is false. True wordings: *"the round-35 closure tip is `7a068cb…` (03:53:37); one
round-35-labelled commit follows it, `4243d031…` (round-35 verifier spot-check, integrator
protocol-shokunin, 03:53:57 author / 04:01:39 committer), which adds the spot-check lesson; the lane
has since advanced to `2d90524…` (round-36)."* Naming 7a068cb as "the round-35 tip" — which is what
spot-check D1 actually asks for — is true, and only becomes misleading if the report adds "last
labelled".

### D1.3 The report's own last commit and what followed it in FLEET

    $ git -C /home/vgpnk/Projects/shokunin log -1 --format='%H %ad' --date=iso -- .ufo/reports/round-35/mado.md
    763734e1b909218e87d1192c1b236b2b575b7ea1 2026-10-25 03:53:03 -0300

That is the round-35 report's last touching commit, whose subject is
`round-35: mado report — the row-section gap and the dead digest store named per seat`. The
report-ordering admission is true: the report landed at 03:53:03, **before** the lane's last three
`round-35:` commits — 567945e (03:53:13), 2eddc38 (03:53:32), 7a068cb (03:53:37) — before the
integrator spot-check 4243d031 (03:53:57), and before the fleet's own round-35 tail.

Every commit after it in FLEET, atomically pinned (HEAD identical before and after the listing):

    $ H0=$(git rev-parse HEAD); git rev-list --count 763734e1..$H0; git log --format='%h %ad %s' --date=iso --reverse 763734e1..$H0; H1=$(git rev-parse HEAD)
    HEAD_BEFORE=b5cd9d6957ec34ad5e940558863049c3e1ac50a3
    61
    HEAD_AFTER=b5cd9d6957ec34ad5e940558863049c3e1ac50a3

    4f040870 2026-10-25 03:53:15 -0300 round-23: kasegi report — note lane tip advance
    e11524e3 2026-10-25 03:53:39 -0300 round-35: hyaku closure dispatch for mado
    11f058fb 2026-10-25 03:53:57 -0300 round-51: kake report
    6b466644 2026-10-25 03:54:59 -0300 round-51: hyaku closure dispatch for kake
    5d1cda56 2026-10-25 03:55:32 -0300 round-23: kasegi report — post-seal errata commit recorded
    9ef8e254 2026-10-25 03:56:24 -0300 round-23: kasegi report — final lane tip d0a3f6a4
    93d24f79 2026-10-25 03:56:51 -0300 round-23: hyaku closure dispatch for kasegi
    34334192 2026-10-25 03:57:09 -0300 round-29: kengaku report (attempt 2 — assimilation + adoption gate)
    74130d7f 2026-10-25 03:58:02 -0300 rounds ledger: kotodama r69 closure (rejected-honest-stop) — hyaku, non-author
    1c58b2f9 2026-10-25 03:58:22 -0300 round-29: kengaku report amendment — laundering repair, final lane head
    ef31e95f 2026-10-25 04:00:57 -0300 rounds ledger: kasegi r23 closure (admitted) — hyaku, non-author
    cb35c4cb 2026-10-25 04:01:21 -0300 round-22: souji report (attempt 2)
    588c424f 2026-10-25 04:01:45 -0300 round-29: kengaku report — residual entry corrections and final lane head
    63108bbc 2026-10-25 04:01:59 -0300 rounds ledger: mado r35 closure (rejected-honest-stop) — hyaku, non-author
    acfce3ee 2026-10-25 04:02:09 -0300 round-29: kengaku report — final lane head and measured quote census
    875a0065 2026-10-25 04:02:42 -0300 round-29: kengaku report — corrected quote-census figures
    619397f8 2026-10-25 04:02:59 -0300 round-29: kengaku report — final lane tip
    1c83bc10 2026-10-25 04:03:22 -0300 round-29: kengaku report — correct seat-return accounting
    d31e0dce 2026-10-25 04:03:33 -0300 rounds ledger: kake r51 closure (admitted) — hyaku, non-author
    7afd9bbe 2026-10-25 04:03:46 -0300 round-23: tabi dispatch evidence (hyaku inline attempt 1)
    da034dc2 2026-10-25 04:04:03 -0300 round-29: kengaku report — calibration repairs and 40/40 seat accounting
    7fb73d02 2026-10-25 04:04:38 -0300 round-28: kagi report (attempt-3 documentary close) + L0 disposition line
    d4090261 2026-10-25 04:04:48 -0300 round-29: kengaku report — pin final lane tip
    71a678ab 2026-10-25 04:04:58 -0300 round-28: hyaku closure dispatch for kagi
    92eeee88 2026-10-25 04:05:20 -0300 round-29: hyaku closure dispatch for kengaku
    e072b1cd 2026-10-25 04:05:25 -0300 round-24: kasegi dispatch evidence (hyaku inline attempt 1)
    48eb8c12 2026-10-25 04:05:50 -0300 round-22: souji report (attempt 2, final tip and residual verdicts)
    f6416359 2026-10-25 04:08:29 -0300 round-22: correct a stale tip reference in the SHONEN line
    c69eb3a3 2026-10-25 04:08:48 -0300 round-22: hyaku closure dispatch for souji
    73a2830c 2026-10-25 04:09:02 -0300 round-36: mado dispatch evidence (hyaku inline attempt 1)
    d53f2d92 2026-10-25 04:09:04 -0300 rounds ledger: kengaku r29 closure (admitted) — hyaku, non-author
    44cfd846 2026-10-25 04:09:36 -0300 round-30: kengaku dispatch evidence (hyaku inline attempt 1)
    2123fdd6 2026-10-25 04:09:55 -0300 rounds ledger: kagi r28 closure (rejected-honest-stop) — hyaku, non-author
    2f5651c3 2026-10-25 04:11:41 -0300 round-41: tameshi report
    5dcedf4d 2026-10-25 04:13:10 -0300 round-41: tameshi report (landed-changes rows, mined record defects)
    d3573cd5 2026-10-25 04:13:30 -0300 round-41: hyaku closure dispatch for tameshi
    1a616ae7 2026-10-25 04:14:37 -0300 round-37: kama dispatch evidence (hyaku inline attempt 1)
    141b000c 2026-10-25 04:14:40 -0300 rounds ledger: souji r22 closure (admitted) — hyaku, non-author
    a4bccbeb 2026-10-25 04:18:37 -0300 rounds ledger: tameshi r41 closure (admitted) — hyaku, non-author
    c22fd9f0 2026-10-25 04:26:47 -0300 round-44: mori dispatch evidence (hyaku inline attempt 1)
    5c95d9d3 2026-10-25 04:27:37 -0300 round-24: kasegi report
    51b577c2 2026-10-25 04:34:30 -0300 round-24: hyaku closure dispatch for kasegi
    2c66b2e2 2026-10-25 04:34:54 -0300 round-23: tabi report
    2384d57d 2026-10-25 04:35:48 -0300 round-23: tabi report (final tip, late fail-open closures)
    898e0ab0 2026-10-25 04:37:21 -0300 round-34: kaidoku report (run-6 re-dispatch: R34-C2 frozen, six clauses met, honest stop on an unregistered class)
    01bbb46d 2026-10-25 04:38:47 -0300 round-23: tabi report (final tip, 44/44 wave-2 reports, disclosed bounds)
    a1f512b5 2026-10-25 04:39:18 -0300 round-34: kaidoku report amendment (predicate status, recorded dissent, limits X1-X5, final lane tip)
    19f52100 2026-10-25 04:39:23 -0300 round-34: kaidoku report — seal findings Y1-Y3, closure-style disposition, sibling precedent, final lane tip
    0b93d7ca 2026-10-25 04:40:35 -0300 round-34: kaidoku report — Y4/Y5 and final lane tip 39f433b2
    71158891 2026-10-25 04:40:52 -0300 round-23: tabi report (LOG binding for every post-landing commit)
    b91fc313 2026-10-25 04:41:05 -0300 round-34: kaidoku report — final tip c05984e7 and census tier wording
    317f91d4 2026-10-25 04:41:11 -0300 round-23: hyaku closure dispatch for tabi
    7d60803e 2026-10-25 04:41:18 -0300 round-34: kaidoku report — seat accounting reconciled (w1 34/34, w2 26/32 reports on disk)
    9882a558 2026-10-25 04:41:25 -0300 round-34: kaidoku report — causal correction N1, validated fixture-design repair, final tip 06afa9e7
    8bfc2b80 2026-10-25 04:43:38 -0300 round-34: kaidoku report — unbound-receipt limit (N2), bound-receipt producer, final tip 6ae73906
    577ec320 2026-10-25 04:43:59 -0300 round-34: kaidoku report — final lane tip dc7384ec
    477eb3f2 2026-10-25 04:44:41 -0300 round-34: kaidoku report — final lane tip debc8dad, worktree clean
    7476b395 2026-10-25 04:44:53 -0300 round-34: kaidoku report — axis-label defect N3, QUALITY 75, final tip 6e2f9b79
    3a275161 2026-10-25 04:45:50 -0300 round-34: kaidoku report — final lane tip f8f3758a, worktree clean
    30f35b08 2026-10-25 04:46:02 -0300 round-34: kaidoku report — N4, independent five-root reproduction, final tip b839f611
    b5cd9d69 2026-10-25 04:47:28 -0300 round-30: kengaku report

Categories in the 61 (count of subject prefixes): round-34 13, round-29 10, round-23 10,
rounds ledger 8, round-22 4, round-41 3, round-24 3, round-51 2, round-30 2, round-28 2,
round-44 1, round-37 1, round-36 1, round-35 1. The only round-35 commit after the report is its
own closure dispatch:

    $ git -C /home/vgpnk/Projects/shokunin log --format='%h %ad %s' --date=iso 763734e1..HEAD --grep='round-35'
    e11524e3 2026-10-25 03:53:39 -0300 round-35: hyaku closure dispatch for mado
    $ git -C /home/vgpnk/Projects/shokunin show --stat --format='' e11524e3
     .ufo/prompts/closure/mado-round-35.md | 94 ++++++++++++++++++++++++++++++
     1 file changed, 94 insertions(+)

and the mado-relevant closure ruling:

    $ git -C /home/vgpnk/Projects/shokunin log --format='%h %ad %s' --date=iso 763734e1..HEAD --grep='mado'
    73a2830c 2026-10-25 04:09:02 -0300 round-36: mado dispatch evidence (hyaku inline attempt 1)
    63108bbc 2026-10-25 04:01:59 -0300 rounds ledger: mado r35 closure (rejected-honest-stop) — hyaku, non-author
    e11524e3 2026-10-25 03:53:39 -0300 round-35: hyaku closure dispatch for mado

### D1.4 The lane's own round-36 tip rule computes `4243d031…` for round 35

The round-36 lane already pins one definition of a round's lane tip, in the C2 artifact this round
landed:

    $ python3 -c "import json;s=json.load(open('.ufo/waves/round-36/c2/frozen.json'));print(json.dumps(s['tip_rule']))"
    {"round": 34, "subject_pattern": "round-34", "min_tip_lines": 3}

    $ python3 -I quality/counters/c2-ledger.py --repo . --frozen .ufo/waves/round-36/c2/frozen.json
    PRED-C2-r36-v1 uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET
      tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived

    `.ufo/waves/round-36/ledger/RevFrozenBlobs-r36.md:7-13`
    "the round-34 lane tip is the newest commit whose subject names `round-34`, computed at run time
     by `quality/counters/c2-ledger.py` — never typed."

Applied to round 35, that frozen rule returns `4243d031…`, not `7a068cb…`:

    $ git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --format='%H %s' | grep -m2 'round-35'
    4243d031e3441f5063f92c33aa58377c6f9ff120 round-35 verifier spot-check (integrator, hyaku): non-author admit/reject
    7a068cbee3b0983230b8fb8467c02e12772832dd round-35: close

So an erratum that calls `7a068cb` "the round-35 lane tip" contradicts the lane's own round-36 tip
rule and its own C2 ledger convention. `7a068cb` can only be named as *the round-35 `close` commit /
the tip at the closure dispatch*, with `4243d031` named as the round-35 lane tip under the subject
rule.

**Verdict on the report-ordering admission: CONFIRMED.** The round-35 report was not last, in either
repo: three lane `round-35:` commits plus the integrator spot-check follow it, one fleet round-35
commit (`e11524e3`, +36 s) follows it, and the non-author ruling on round 35 is
`63108bbc … (rejected-honest-stop)`. An erratum that says "the report landed before the lane's
closing commits" is true; one that says "7a068cb is the last round-35-labelled commit" is false
(§D1.2).

---

## D6 — what `02088b4..7a068cb` changed in `corpus/SOURCES.md`

    $ git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --numstat 02088b4dff0da153df30ff174611d1257c92d0cd 7a068cbee3b0983230b8fb8467c02e12772832dd -- corpus/SOURCES.md
    3	3	corpus/SOURCES.md

    $ git -C … diff --stat 02088b4dff0da153df30ff174611d1257c92d0cd 7a068cbee3b0983230b8fb8467c02e12772832dd -- corpus/SOURCES.md
     corpus/SOURCES.md | 6 +++---
     1 file changed, 3 insertions(+), 3 deletions(-)

Rows present, both revisions: 200 / 200; ids added 0, ids removed 0. Only three ids differ
(cell-by-cell parse against the header `| id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by |`):

| id | cell | `02088b4` | `7a068cb` |
|---|---|---|---|
| S203 | `teaches` | "runs twelve first-run scripts … none of the twelve asks about the idle lock" | "runs thirteen items, twelve of them first-run scripts … none of the thirteen executed items asks about the idle lock" |
| S203 | `recheck` | `on-request` | `on-change` |
| S204 | `scope` | "…the operator never made it afterwards either" | "…the journal's zero omarchy-toggle count is a null channel, and the daemon's stop/start is consistent with a toggle-off" |
| S204 | `teaches` | "…holds zero omarchy-toggle invocations" | "…zero omarchy-toggle invocations, which is a null channel rather than a negative" |
| S204 | `recheck` | `on-request` | `on-change` |
| S205 | `teaches` | "the journal holds two start lines on 2026-10-23" | "the journal holds one start line in the current boot (two across two boots) on 2026-10-23" |

So: **3 rows** (S203, S204, S205), **6 cells**, `3 3` lines. Cells touched: `teaches` ×3,
`scope` ×1 (S204), `recheck` ×2 (S203, S204, `on-request`→`on-change`). S205's `recheck` (`90d`)
does not change.

The round-35 report says the opposite on both counts:

    .ufo/reports/round-35/mado.md:133-135
    "Rows touched old→new: **0** — no existing row's `status`/`recheck`/`used-by` changed; four of
     the new rows' `scope`/`teaches` cells were corrected in-round to match the entry errata."

**Verdict: the report sentence is FALSIFIED; the spot-check's correction is CONFIRMED.** Spot-check
D6 ("three rows (S203, S204, S205) … the corrected cells include `recheck` … `3 3`") matches the
bytes exactly. An erratum carrying that text would be **true**.

### D6 finding (medium) — the count erratum would leave the rule breach unnamed

`CORPUS.md:112-117` (SOURCES contract v1):

    2. **Append-only.** Only `status`, `recheck` and `used-by` change in place, and each change
       is logged old→new in the round lesson. A correction is a new row whose `teaches` opens
       `supersedes S0NN —`.

The round-35 errata changed `teaches` on three rows and `scope` on one **in place** — cells the rule
does not permit to change in place — and the lesson never logs the `recheck on-request→on-change`
old→new transitions it requires:

    $ grep -n 'on-change\|on-request\|supersedes' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-35.md
    (no output)

while the same lesson claims the opposite mechanism:

    corpus/lessons/round-35.md:178-180
    "## Wave-2 falsifications applied as errata
     … Their findings are applied as append-only errata blocks (criterion 44), not as rewrites:"

The committed row cells are rewrites of non-mutable cells on new rows. A D6 erratum limited to
"four→three" would therefore be true but incomplete: it should also state that the in-place
`scope`/`teaches` edits exceed rule 2 (the fix would be superseding rows) and that the two `recheck`
transitions are unlogged in the lesson. Without that, the round-36 report would launder a contract
breach as a counting error.

Related small note (not a defect): `on-change` is a legal cadence to the census
(`scripts/sources-census.sh:582` accepts any `[A-Za-z][A-Za-z0-9 _-]*` symbolic value; run
`./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0 today),
but `CORPUS.md:105-106` lists only `90d`, `180d`, `on-release` as examples, so the new cadence is
undocumented vocabulary.

---

## D7 — `.md` count under `.ufo/waves/round-35/w2/reports/`

    $ for c in 4f35c80 7b745a1 7a068cb; do printf "%s md=%s\n" $c "$(git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree -r --name-only $c -- .ufo/waves/round-35/w2/reports/ | grep -c '\.md$')"; done
    4f35c80 md=37
    7b745a1 md=37
    7a068cb md=40

    $ git -C … ls-tree -r --name-only 4f35c80 -- .ufo/waves/round-35/w2/reports/ | wc -l
    37                                  # every entry is .md; no subdirectories at any of the three revs
    $ git -C … diff --name-status 7b745a1 7a068cb -- .ufo/waves/round-35/w2/reports/
    A  ConnOverlap.md
    A  RevScorecard.md
    A  SentBoundary.md
    M  (18 revisions)

The count never equals 38 at any round-35 commit:

    $ for c in $(git -C … rev-list --reverse 4f35c80^..7a068cb); do printf "%s %s %s\n" "$(git log -1 --format='%h' $c)" "$(git log -1 --format='%ad' --date=format:'%H:%M:%S' $c)" "$(git ls-tree --name-only $c .ufo/waves/round-35/w2/reports/ | grep -c '\.md$')"; done
    4f35c80 03:34:26 37
    7b745a1 03:42:29 37
    4efaf63 03:43:55 37
    8889bdc 03:43:55 37
    b632f0b 03:45:15 40     ← 37 → 40 (ConnOverlap, SentBoundary, RevScorecard)
    … every later commit 40
    7a068cb 03:53:37 40

Dispatch artifacts also say 40, not 38:

    $ python3 -c "import json;d=json.load(open('.ufo/waves/round-35/w2-plan.json'));print(len(d['tasks']))"
    40
    $ python3 -c "import json;d=json.load(open('.ufo/waves/round-35/w2-spec.json'));print(len(d['items']))"
    40
    $ python3 -c "import json;d=json.load(open('.ufo/waves/round-35/w2-taskcall.json'));print(len(d))"
    40

(For completeness the wave-1 tree is 64 `.md` at the tip, so 38 is not a wave-1 figure either.)

The round-35 report carries 38 twice and 40 once:

    .ufo/reports/round-35/mado.md:39   "`.ufo/waves/round-35/w2/reports/` (38 reports), …"
    .ufo/reports/round-35/mado.md:88   "| `4f35c80` | … the 38 wave-2 reports, …"
    .ufo/reports/round-35/mado.md:194  "wave 2 dispatched 40; **40 wrote reports** …"

**Verdict: the spot-check's D7 correction is CONFIRMED — 37 / 37 / 40.** An erratum saying
"37 `.md` at `4f35c80` and `7b745a1`, 40 at the tip `7a068cb` (the 37→40 jump is `b632f0b`); the
'38' never describes any committed revision or any dispatch artifact" is **true**. The alternative
erratum "38 was the count at an intermediate pass" is **false**: no commit in the wave holds 38.

---

## Verdict summary

| Item | Mandated erratum content | Truth |
|---|---|---|
| D1 (tip) | "`7a068cbe…` is the last round-35-labelled commit on the branch" | **FALSIFIED** — `4243d031…` (round-35 verifier spot-check, pushed, child of 7a068cb) is later; the repo's own D4 precedent (`6d754bd`, round-34 spot-check) defines the label that way |
| D1 (tip, narrow) | "`7a068cb…` is the round-35 closure tip / last `round-35:` lane commit; lane since at `2d90524…`" | **CONFIRMED** |
| D1 (tip rule) | "`7a068cb` is the round-35 lane tip" | **FALSIFIED under the lane's own round-36 rule** (`c2/frozen.json` `subject_pattern` rule → `4243d031…`); true only as "the tip at the closure dispatch" |
| D1 (ordering) | "the report landed (763734e1, 03:53:03) before the lane's closing commits and the closure dispatch" | **CONFIRMED** — 567945e, 2eddc38, 7a068cb in lane; e11524e3 (+36 s) and 63108bbc (rejected-honest-stop) in fleet; 61 fleet commits follow it |
| D6 | "three rows S203/S204/S205, `3 3`, corrected cells include `recheck`" | **CONFIRMED** (report's "four … scope/teaches" is false) |
| D6 (finding) | count-only erratum | **incomplete** — `scope`/`teaches` edited in place against `CORPUS.md` rule 2; `recheck` old→new unlogged in the lesson |
| D7 | "37 at `4f35c80`/`7b745a1`, 40 at `7a068cb`" | **CONFIRMED**; "38" holds at no revision and in no dispatch artifact |

## Residual risk / verification gaps

- The fleet listing is a moving target: my first count read `60` (HEAD not captured in that call);
  the pinned re-run, with HEAD `b5cd9d69` identical before and after, reads **61** — commit
  `b5cd9d69` (2026-10-25 04:47:28, round-30 kengaku report) landed between the two runs. Any report
  sentence quoting a count must pin HEAD beside it, as above.
- `4243d031` carries author date 03:53:57 and committer date 04:01:39 (7m42s apart). Under author
  dates it is 20 s after `7a068cb`; under committer dates it is 8m02s. The D1 precedent (`dff3941`
  → `6d754bd` = 17m37s only on committer dates) says committer dates; the erratum should say which
  clock it uses rather than leave a reviewable gap.
- No `ScribeReportErrata` draft exists, and no `ScoutD1Facts` report has landed at the time of
  writing (`ls .ufo/waves/round-36/w1/reports/`), so this report tests the mandated content, not a
  drafted sentence. `ScoutD6Rows.md` and `ScoutD7Counts.md` exist and agree with my numbers
  (37/37/40; `3 3`).
- Row-cell parsing is my own header-mapped parse (`|`-split, 11 cells) plus the cited `git diff`;
  the `3 3` numstat is the independent check that no other line moved.
