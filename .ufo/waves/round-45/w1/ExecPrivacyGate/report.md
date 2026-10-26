# ExecPrivacyGate — a committed-receipt privacy gate, shown able to fail (round 45 w1)

Routed work, not a C1/C2 claim: considerthese `2026-10-26.md` proposal 1 ("add a privacy check on new receipts") plus round-44 closure
defect D1 (session material tracked at `8ac15c41`). Question this seat answers: can a gate over the committed tree *find* the raw session
state the lane already ships, and *stop finding it* once the files are projected?

| artefact (all in this seat dir) | role | sha256 |
|---|---|---|
| `check-session-material.py` | the gate (stdlib only; L1 may install at `quality/check-session-material.py`) | `889f8f057bf04fc76ed93dd7ee86e3b0bd9fc1dca3a6bfb712c672da4646e3fb` |
| `project-d1.py` | scratch-clone driver that rewrites a client dump to the 7-key receipt shape | — |
| `r3-live-control.py` | positive control for R3 against one allowed live compositor read | — |
| `base-run.txt`, `projected-run.txt`, `tip-run.txt`, `selftest.txt`, `r3-live-control.txt` | receipts of the five runs below | — |

No existing tracked file was edited; the lane's git index was not touched (all commits happen in a scratch clone, `git -C "$D"`, toplevel
asserted before the first commit).

## 1. The gate

`check-session-material.py --repo <dir> --rev <rev> [--home-limit N]`, `--selftest [--verbose]`. It lists every tracked file under `.ufo/`
at the revision (`git ls-tree -r -z`), reads the blobs from the object database (`git cat-file --batch`, request list through a temp file
so the pipe cannot deadlock), and scans text blobs for four shapes:

- **R1_CLIENT_DUMP** — a JSON object carrying `class` and `title`/`initialTitle` with non-empty string values, i.e. an element of a live
  `hyprctl clients -j` dump. Whole-file JSON first, then `JSONDecoder.raw_decode` over embedded objects (fenced blocks, receipts, reports).
- **R2_PROC_TABLE** — the `ss -xpa` / `ss -p` process column: `users:((` + a quoted program name + `,pid=<n>`.
- **R3_MONITOR_IDENT** — a JSON object with a non-empty `serial` and a non-empty `description`/`make`/`model`, i.e. an element of
  `hyprctl monitors all -j`. Empty/redacted serials do not match.
- **R4_HOME_LISTING** — more than `--home-limit` (default 10) distinct lines that consist solely of an absolute `/home/<user>/...` path
  (a `find`/`grep` dump); paths quoted inside a sentence are not counted.

Output: one line per (file, rule) — `FINDING file=… rule=… count=… detail=…`; a `SESSION_MATERIAL_RULES:` tally; then
`SESSION_MATERIAL: files=<n> findings=<n> rev=<hash>`. Exit 0 clean, 1 findings, 2 git/usage error. No title, program name, serial,
description or home path is ever printed, so the gate's own output is safe to paste into a receipt.

`--selftest` builds positive and negative fixtures in a throwaway git repo under `$TMPDIR` and scores detection plus two end-to-end scans:
**22/22 passed** (`selftest.txt`), including "7-key projection is clean", "empty title is not a finding", "class-only is not a finding",
"embedded fenced dump is found", "5-row table is found", "12-entry listing is found", "inline paths are clean", "a non-`.ufo` file is
invisible", "a revision with no `.ufo` tree exits 0" (the last case was added after the first run exposed a `cat-file` SIGPIPE there).

## 2. Run 1 — base `0c89478a`, the gate must fail

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/w1/ExecPrivacyGate/check-session-material.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 0c89478af821a6424c9ac922eafe02e39630cf4f
FINDING file=.ufo/waves/round-35/scratch-evidence/SentProvenance/S203.scope.txt rule=R4_HOME_LISTING count=12 detail=distinct_paths=12 limit=10
FINDING file=.ufo/waves/round-37/receipts/eventq-live-ss.txt rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/res/reports/L1Mado37-2.CritEntryE2.md rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/w1/reports/ExecEventqB.md rule=R2_PROC_TABLE count=1 detail=rows=1
FINDING file=.ufo/waves/round-37/w1/reports/ExecProcCrosscheck.md rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/w1/reports/RevC2Code.md rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/w1/reports/ScoutRollingLog.md rule=R2_PROC_TABLE count=2 detail=rows=2
FINDING file=.ufo/waves/round-37/w1/reports/ScoutSsSemantics.md rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/w1/scratch/CritAxisClaim/controls_critaxis.py rule=R2_PROC_TABLE count=3 detail=rows=3
FINDING file=.ufo/waves/round-37/w1/scratch/CritC2Cheap/handsnap.txt rule=R2_PROC_TABLE count=3 detail=rows=3
FINDING file=.ufo/waves/round-37/w1/scratch/ExecEventqA/live-ss.txt rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/w1/scratch/ExecEventqB/setup-reasons.py rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/ALL/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/P1/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/P2/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/P3/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/P4/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/P5/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/P6/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/diff_c2.sh rule=R2_PROC_TABLE count=1 detail=rows=1
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/orig/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-38/receipts/eventq-live-ss.txt rule=R2_PROC_TABLE count=715 detail=rows=715
FINDING file=.ufo/waves/round-38/w1/reports/RevC2v3.md rule=R2_PROC_TABLE count=1 detail=rows=1
FINDING file=.ufo/waves/round-38/w1/reports/RevLiveTriplet.md rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-38/w1/reports/ScoutR29Refusal.md rule=R2_PROC_TABLE count=1 detail=rows=1
FINDING file=.ufo/waves/round-39/w1/ExecEventqSnapshot/eventq-live-census.txt rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json rule=R1_CLIENT_DUMP count=4 detail=objects=4 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecLiveHost/live-census.txt rule=R4_HOME_LISTING count=40 detail=distinct_paths=40 limit=10
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt rule=R1_CLIENT_DUMP count=1 detail=objects=1 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-floatonly.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-headlesshost.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-host-r1.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-host-r2.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-host-r3.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-minsize.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-nofloat.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-nomatch.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-size300.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-floatonly.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-headlesshost.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-host-r1.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-host-r2.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-host-r3.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-minsize.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-nofloat.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-nomatch.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-size300.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w2/SentLiveRun/dump-now.json rule=R1_CLIENT_DUMP count=4 detail=objects=4 keys=title+initialTitle
FINDING file=.ufo/waves/round-44/w1/ScrLessonSkeleton/c1-demo/client1.json rule=R1_CLIENT_DUMP count=1 detail=objects=1 keys=title
FINDING file=.ufo/waves/round-44/w1/ScrLessonSkeleton/c1-demo/client2.json rule=R1_CLIENT_DUMP count=1 detail=objects=1 keys=title
SESSION_MATERIAL_RULES: R1_CLIENT_DUMP=23 R2_PROC_TABLE=25 R4_HOME_LISTING=2
SESSION_MATERIAL: files=16329 findings=50 rev=0c89478af821a6424c9ac922eafe02e39630cf4f
exit=1
```

Both D1 files are listed: `.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json` (4 client objects) and
`.ufo/waves/round-43/w2/SentLiveRun/dump-now.json` (4 client objects) — the same count as the closure's `grep -c '"title"'` → 4 on each.
50 findings over 50 distinct files; 16,329 tracked `.ufo` files, 225,409,985 bytes scanned, 1.4 s. Run at the lane tip
`ebdba13f7cb16d454763003d424398eec3bb2788` (`tip-run.txt`) gives `files=16357 findings=50` with the same 50 files: D1 is still unfixed
and both paths are still tracked at the tip (`git ls-tree -r --name-only ebdba13 | grep -E 'host-clients-live|dump-now'` returns both).

## 3. Run 2 — scratch clone with the two D1 files projected to 7 keys, the gate must pass for them

```
$ S=/fast/scratch/hyaku/mado-r45/ExecPrivacyGate; D=$(mktemp -d -p "$S" clone.XXXXXX)
$ git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin "$D"
$ test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"          # toplevel asserted before any commit
$ git -C "$D" checkout -q --detach 0c89478af821a6424c9ac922eafe02e39630cf4f
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/w1/ExecPrivacyGate/project-d1.py "$D/.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json" "$D/.ufo/waves/round-43/w2/SentLiveRun/dump-now.json"
/fast/scratch/hyaku/mado-r45/ExecPrivacyGate/clone.l1GJT7/.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json clients=4 keys=address,at,class,floating,mapped,monitor,size
/fast/scratch/hyaku/mado-r45/ExecPrivacyGate/clone.l1GJT7/.ufo/waves/round-43/w2/SentLiveRun/dump-now.json clients=4 keys=address,at,class,floating,mapped,monitor,size
$ git -C "$D" add -A && git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m pos
$ git -C "$D" rev-parse HEAD
4c4e9ddfde4b56eae064b911d3f8fc793d1b1877
$ git -C "$D" show --stat --oneline HEAD
4c4e9ddf pos
 .../w1/ExecLiveHost/host-clients-live.json         | 207 ++++++---------------
 .ufo/waves/round-43/w2/SentLiveRun/dump-now.json   | 207 ++++++---------------
 2 files changed, 124 insertions(+), 290 deletions(-)
```

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/w1/ExecPrivacyGate/check-session-material.py --repo /fast/scratch/hyaku/mado-r45/ExecPrivacyGate/clone.l1GJT7 --rev HEAD
FINDING file=.ufo/waves/round-35/scratch-evidence/SentProvenance/S203.scope.txt rule=R4_HOME_LISTING count=12 detail=distinct_paths=12 limit=10
FINDING file=.ufo/waves/round-37/receipts/eventq-live-ss.txt rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/res/reports/L1Mado37-2.CritEntryE2.md rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/w1/reports/ExecEventqB.md rule=R2_PROC_TABLE count=1 detail=rows=1
FINDING file=.ufo/waves/round-37/w1/reports/ExecProcCrosscheck.md rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/w1/reports/RevC2Code.md rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/w1/reports/ScoutRollingLog.md rule=R2_PROC_TABLE count=2 detail=rows=2
FINDING file=.ufo/waves/round-37/w1/reports/ScoutSsSemantics.md rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/w1/scratch/CritAxisClaim/controls_critaxis.py rule=R2_PROC_TABLE count=3 detail=rows=3
FINDING file=.ufo/waves/round-37/w1/scratch/CritC2Cheap/handsnap.txt rule=R2_PROC_TABLE count=3 detail=rows=3
FINDING file=.ufo/waves/round-37/w1/scratch/ExecEventqA/live-ss.txt rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/w1/scratch/ExecEventqB/setup-reasons.py rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/ALL/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/P1/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/P2/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/P3/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/P4/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/P5/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/P6/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/diff_c2.sh rule=R2_PROC_TABLE count=1 detail=rows=1
FINDING file=.ufo/waves/round-37/w1/scratch/SimplifyCounters/orig/c2-r37-eventq.py rule=R2_PROC_TABLE count=9 detail=rows=9
FINDING file=.ufo/waves/round-38/receipts/eventq-live-ss.txt rule=R2_PROC_TABLE count=715 detail=rows=715
FINDING file=.ufo/waves/round-38/w1/reports/RevC2v3.md rule=R2_PROC_TABLE count=1 detail=rows=1
FINDING file=.ufo/waves/round-38/w1/reports/RevLiveTriplet.md rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-38/w1/reports/ScoutR29Refusal.md rule=R2_PROC_TABLE count=1 detail=rows=1
FINDING file=.ufo/waves/round-39/w1/ExecEventqSnapshot/eventq-live-census.txt rule=R2_PROC_TABLE count=5 detail=rows=5
FINDING file=.ufo/waves/round-43/w1/ExecLiveHost/live-census.txt rule=R4_HOME_LISTING count=40 detail=distinct_paths=40 limit=10
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt rule=R1_CLIENT_DUMP count=1 detail=objects=1 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-floatonly.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-headlesshost.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-host-r1.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-host-r2.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-host-r3.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-minsize.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-nofloat.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-nomatch.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/dump-size300.json rule=R1_CLIENT_DUMP count=2 detail=objects=2 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-floatonly.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-headlesshost.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-host-r1.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-host-r2.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-host-r3.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-minsize.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-nofloat.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-nomatch.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/receipt-size300.json rule=R1_CLIENT_DUMP count=3 detail=objects=3 keys=title+initialTitle
FINDING file=.ufo/waves/round-44/w1/ScrLessonSkeleton/c1-demo/client1.json rule=R1_CLIENT_DUMP count=1 detail=objects=1 keys=title
FINDING file=.ufo/waves/round-44/w1/ScrLessonSkeleton/c1-demo/client2.json rule=R1_CLIENT_DUMP count=1 detail=objects=1 keys=title
SESSION_MATERIAL_RULES: R1_CLIENT_DUMP=21 R2_PROC_TABLE=25 R4_HOME_LISTING=2
SESSION_MATERIAL: files=16329 findings=48 rev=4c4e9ddfde4b56eae064b911d3f8fc793d1b1877
exit=1
```

The two targets pass: the projection commit drops exactly two findings (50 → 48), `R1_CLIENT_DUMP` 23 → 21, `files=16329` unchanged,
and no line names `host-clients-live.json` or `dump-now.json` (`grep -cE 'host-clients-live|dump-now' projected-run.txt` → 0). The exit
is still 1 because the other 48 findings remain — the gate passes the projected files, not the tree. That asymmetry is the demonstration:
the same gate fails on the raw dumps and stops failing on the projections, with the rest of the tree untouched.

## 4. All findings, classified (what each attacks)

The gate reports shape, not provenance; these are the triage classes.

**R1_CLIENT_DUMP — 23 files.** (a) The two D1 host dumps, 4 client objects each. (b) 19 files under
`.ufo/waves/round-43/w1/ExecOracleGkeep/` (9 `receipts/dump-*.json` with 2 objects each, 9 `receipts/receipt-*.json` with 3 each, and
`20-observation.txt` with 1). These are the seat's own probe client, not host windows: across those JSON files there are 45 client objects,
the only classes are `org.omarchy.gkeep` and `org.omarchy.gkeep2`, exactly 2 distinct (class,title) pairs, and every title equals
`gkeep-oracle-probe`, the literal set at `.ufo/waves/round-43/w1/ExecOracleGkeep/gkeep-shm.c:151`
(`xdg_toplevel_set_title(s.toplevel, "gkeep-oracle-probe")`). D1's instruction to "check and state it in that sweep" holds: no human
window title is in these files. (c) 2 files under `.ufo/waves/round-44/w1/ScrLessonSkeleton/c1-demo/` are hand-written demo fixtures
(`"address": "0x1"`, class `org.omarchy.gkeep`, title `gkeep`), not a dump.

**R2_PROC_TABLE — 25 files.** 12 carry actual `ss` data rows (a socket-type token, state, queues, then the program column):
`.ufo/waves/round-38/receipts/eventq-live-ss.txt` (715 rows, 1,010 data lines), `.ufo/waves/round-37/receipts/eventq-live-ss.txt` (5),
`.ufo/waves/round-37/w1/scratch/ExecEventqA/live-ss.txt` (5), `.ufo/waves/round-39/w1/ExecEventqSnapshot/eventq-live-census.txt` (5),
`.ufo/waves/round-37/w1/scratch/CritC2Cheap/handsnap.txt` (3), and 7 reports that paste rows
(`res/reports/L1Mado37-2.CritEntryE2.md` 5, `w1/reports/ExecProcCrosscheck.md` 5, `w1/reports/ScoutSsSemantics.md` 5,
`w1/reports/RevC2Code.md` 3, `w1/reports/ScoutRollingLog.md` 2, `w1/reports/RevLiveTriplet.md` 3, `w1/reports/ScoutR29Refusal.md` 1).
The other 13 mention the column shape without data rows: 8 copies of the round-37 `c2-r37-eventq.py` counter (`orig/`, `ALL/`,
`P1`–`P6`), `setup-reasons.py`, `controls_critaxis.py`, `diff_c2.sh`, plus `w1/reports/ExecEventqB.md` and `w1/reports/RevC2v3.md`.

**R3_MONITOR_IDENT — 0 files, a true negative.** No committed dump has an identifying monitor object: the round-43 receipts do embed a
`monitors` array, but every one of those objects has empty `serial`, `description`, `make` and `model` (headless tinywl output). The rule
is not vacuous — `r3-live-control.py` feeds one allowed live read (`hyprctl monitors all -j`, 1,339 bytes, 1 output) to the gate's own
`scan_blob` and gets `[('R3_MONITOR_IDENT', 1, 'objects=1 keys=serial+ident')]`, `R3_FIRES=yes`, exit 0, without printing or keeping any
serial or description text.

**R4_HOME_LISTING — 2 files**, both real bare-path dumps: `.ufo/waves/round-43/w1/ExecLiveHost/live-census.txt` (40 distinct
`/home/vgpnk/...` lines, a config-file listing) and `.ufo/waves/round-35/scratch-evidence/SentProvenance/S203.scope.txt` (12).

## 5. Round-38 `eventq-live-ss.txt` status

`git ls-tree -r -l 0c89478a -- .ufo/waves/round-38` → `100644 blob 0a307f5fdd36d174ac582818bb19dd0992a1dffd 190816
.ufo/waves/round-38/receipts/eventq-live-ss.txt`. The gate reads 715 process rows from it (1,010 ss-shaped data lines). It is still
tracked at the lane tip (`git cat-file -s ebdba13:.ufo/waves/round-38/receipts/eventq-live-ss.txt` → 190816), together with the smaller
round-37 copy. This is the HIGH item in considerthese proposal 1: the bytes stay in pushed history (`2a3707c8`, `58466627` per the round-44
closure) unless the operator rewrites history, which no lane action may do.

## 6. Declared limits and what the L1 should do

- **Shape, not provenance.** R2 and R1 flag the *form*; 13 of 25 R2 findings and the 21 non-D1 R1 findings are fixtures, counters or
  self-launched test windows. Triage is a human step; the gate never prints the sensitive values.
- **Self-application.** The gate's own source embeds synthetic fixtures: scanning this seat copy gives `R1_CLIENT_DUMP` 3, `R2_PROC_TABLE` 2,
  `R3_MONITOR_IDENT` 1. Installing it at `quality/check-session-material.py` (outside `.ufo/`) keeps the scan clean; committing the seat copy
  *under* `.ufo/` would make the gate flag itself, by design and harmlessly.
- **Scope.** Only tracked blobs under `.ufo/` at one revision: an untracked leak, a leak outside `.ufo/`, or a leak in a file whose text is
  binary-shaped is invisible. Text is capped at 16 MiB per blob; R4's 10-path default is a policy number, not a measurement.
- **R2 noise.** A stricter rule (header plus rows) does not separate them: the counters embed the `Netid` header too.
- **Recommended D1 fix for the L1** (not done here — the seat writes only its own dir): apply `project-d1.py` to the two round-43 files,
  then re-run the gate at the fix commit; expect `findings=48` and no line for either path. History rewrite stays operator-owned.

## 7. Host and tooling

Read-only throughout: no pacman, no package transaction, no compositor mutation, no input injection, no Wayland client of this seat. The
only host touch is `hyprctl monitors all -j` inside `r3-live-control.py` (an explicitly allowed read), and it is not echoed into any file.
Python 3.14.8 (system), git 2.56.0; nothing installed. All clones, fixture repos and receipts lived under
`/fast/scratch/hyaku/mado-r45/ExecPrivacyGate/` and were deleted after the receipts were copied here.

## 8. Files in this seat

`check-session-material.py`, `project-d1.py`, `r3-live-control.py`, `report.md`, `base-run.txt`, `projected-run.txt`, `tip-run.txt`,
`selftest.txt`, `r3-live-control.txt`. Nothing tracked was modified.
