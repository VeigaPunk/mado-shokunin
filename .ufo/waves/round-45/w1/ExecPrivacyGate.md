# ExecPrivacyGate — round 45 w1 (considerthese 2026-10-26 proposal 1 + round-44 closure D1)

Scope: build a committed-receipt privacy gate and show it able to fail at base, pass on projected receipts. Routed work, not a C1/C2
claim. Full verbatim runs: `.ufo/waves/round-45/w1/ExecPrivacyGate/report.md`; raw receipts in the same seat dir.

## Delivered

- `.ufo/waves/round-45/w1/ExecPrivacyGate/check-session-material.py` — the gate, stdlib only, sha256
  `889f8f057bf04fc76ed93dd7ee86e3b0bd9fc1dca3a6bfb712c672da4646e3fb`. L1 may install at `quality/check-session-material.py`.
  `--repo <dir> --rev <rev> [--home-limit N]`; reads every tracked file under `.ufo/` from the object database (`git ls-tree -r` +
  `git cat-file --batch`, working tree untouched), scans for four session-material shapes, prints one `FINDING file=… rule=… count=…
  detail=…` line per (file, rule), a per-rule tally, then `SESSION_MATERIAL: files=<n> findings=<n> rev=<hash>`; exit 0 clean / 1 findings /
  2 error. Rules: R1_CLIENT_DUMP (`hyprctl clients -j` element: JSON object with non-empty `class` + `title`/`initialTitle`, whole-file or
  embedded), R2_PROC_TABLE (`ss -xpa`/`ss -p` process column: `users:((` + quoted program + `,pid=<n>`), R3_MONITOR_IDENT (`monitors -j`
  element: non-empty `serial` + `description`/`make`/`model`), R4_HOME_LISTING (> `--home-limit`=10 distinct lines that are solely an
  absolute `/home/<user>/…` path). Findings never print a title, program name, serial, description or home path.
- `--selftest`: **22/22 passed** (`selftest.txt`), positive and negative fixtures in a throwaway git repo: whole-file and embedded client
  dumps found; 7-key projection, empty-title, class-only, prose-keys, monitor-rule line, inline paths, 3-entry listing all clean; 5-row ss
  table, monitor identity, 12-entry listing found; end-to-end positives-only, negatives-only (exit 0), non-`.ufo` file invisible, and a
  revision with no `.ufo` tree exits 0 (that last case was added after the first run caught a `cat-file` SIGPIPE on an empty tree).
- `project-d1.py` (rewrites a client dump to the 7-key receipt shape of `.ufo/waves/round-43/fetch/host-clients-r43.json`),
  `r3-live-control.py` (positive control for R3), receipts `base-run.txt`, `projected-run.txt`, `tip-run.txt`, `selftest.txt`,
  `r3-live-control.txt`.

## Run 1 — base `0c89478a`: the gate fails, exit 1

```
SESSION_MATERIAL_RULES: R1_CLIENT_DUMP=23 R2_PROC_TABLE=25 R4_HOME_LISTING=2
SESSION_MATERIAL: files=16329 findings=50 rev=0c89478af821a6424c9ac922eafe02e39630cf4f
```

16,329 tracked `.ufo` files / 225,409,985 bytes scanned in 1.4 s. **Both D1 files are among the 50**:
`.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json` (R1, 4 client objects) and
`.ufo/waves/round-43/w2/SentLiveRun/dump-now.json` (R1, 4 client objects). All 50 findings, by rule:

**R1_CLIENT_DUMP (23).** D1 host dumps (2): `round-43/w1/ExecLiveHost/host-clients-live.json` 4, `round-43/w2/SentLiveRun/dump-now.json` 4.
Round-43 ExecOracleGkeep, the seat's own probe client, not host windows (19): `receipts/dump-{floatonly,headlesshost,host-r1,host-r2,
host-r3,minsize,nofloat,nomatch,size300}.json` 2 each; `receipts/receipt-{floatonly,headlesshost,host-r1,host-r2,host-r3,minsize,nofloat,
nomatch,size300}.json` 3 each; `20-observation.txt` 1 — across those JSON files 45 client objects, only classes
`org.omarchy.gkeep`/`org.omarchy.gkeep2`, 2 distinct (class,title) pairs, every title equal to `gkeep-oracle-probe`, the literal set at
`.ufo/waves/round-43/w1/ExecOracleGkeep/gkeep-shm.c:151`. Round-44 hand-written demo fixtures (2):
`round-44/w1/ScrLessonSkeleton/c1-demo/client1.json`, `client2.json` (1 each).

**R2_PROC_TABLE (25).** Carrying actual ss data rows (12): `round-38/receipts/eventq-live-ss.txt` 715 (1,010 data lines),
`round-37/receipts/eventq-live-ss.txt` 5, `round-37/w1/scratch/ExecEventqA/live-ss.txt` 5,
`round-39/w1/ExecEventqSnapshot/eventq-live-census.txt` 5, `round-37/w1/scratch/CritC2Cheap/handsnap.txt` 3, and reports pasting rows:
`round-37/res/reports/L1Mado37-2.CritEntryE2.md` 5, `round-37/w1/reports/{ExecProcCrosscheck,ScoutSsSemantics}.md` 5 each,
`round-38/w1/reports/RevLiveTriplet.md` 3, `round-37/w1/reports/RevC2Code.md` 3, `round-37/w1/reports/ScoutRollingLog.md` 2,
`round-38/w1/reports/ScoutR29Refusal.md` 1. Mentioning the column shape only (13): the eight copies of the round-37 `c2-r37-eventq.py`
counter (`SimplifyCounters/{orig,ALL,P1..P6}`) 9 each, `round-37/w1/scratch/ExecEventqB/setup-reasons.py` 5,
`round-37/w1/scratch/CritAxisClaim/controls_critaxis.py` 3, `round-37/w1/scratch/SimplifyCounters/diff_c2.sh` 1,
`round-37/w1/reports/ExecEventqB.md` 1, `round-38/w1/reports/RevC2v3.md` 1.

**R3_MONITOR_IDENT (0)** — true negative: the round-43 receipts embed `monitors` arrays, but every object has empty
`serial`/`description`/`make`/`model`. Not vacuous: `r3-live-control.py` on one allowed live read (`hyprctl monitors all -j`, 1,339 bytes,
1 output) prints `findings=[('R3_MONITOR_IDENT', 1, 'objects=1 keys=serial+ident')]`, `R3_FIRES=yes`, and keeps no serial/description text.

**R4_HOME_LISTING (2).** `round-43/w1/ExecLiveHost/live-census.txt` 40 distinct bare `/home/vgpnk/...` lines;
`round-35/scratch-evidence/SentProvenance/S203.scope.txt` 12.

`tip-run.txt`: at lane tip `ebdba13f7cb16d454763003d424398eec3bb2788` the same 50 files (`files=16357 findings=50`), so D1 is still unfixed.

## Run 2 — scratch clone with the two D1 files projected: the gate passes for them

`D=$(mktemp -d -p /fast/scratch/hyaku/mado-r45/ExecPrivacyGate)`; `git clone -q --shared --no-checkout` the lane; toplevel asserted equal
to `$D`; `checkout --detach 0c89478a`; `project-d1.py` on both files (4 clients each → keys
`address,at,class,floating,mapped,monitor,size`); commit `4c4e9ddfde4b56eae064b911d3f8fc793d1b1877` (2 files, +124/−290). Gate at that
HEAD:

```
SESSION_MATERIAL_RULES: R1_CLIENT_DUMP=21 R2_PROC_TABLE=25 R4_HOME_LISTING=2
SESSION_MATERIAL: files=16329 findings=48 rev=4c4e9ddfde4b56eae064b911d3f8fc793d1b1877
exit=1
```

Exactly two findings drop (50 → 48, R1 23 → 21), `files` unchanged, and no line names either path
(`grep -cE 'host-clients-live|dump-now' projected-run.txt` → 0). Exit stays 1 for the other 48: the gate passes the projected files, not the
tree. That is the demonstration — fail on raw dumps, pass on the projection, everything else unchanged.

## Round-38 `eventq-live-ss.txt` status

Still tracked at base and tip: `100644 blob 0a307f5fdd36d174ac582818bb19dd0992a1dffd 190816
.ufo/waves/round-38/receipts/eventq-live-ss.txt` (`git cat-file -s ebdba13:.ufo/waves/round-38/receipts/eventq-live-ss.txt` → 190816),
715 process rows / 1,010 ss data lines by the gate, plus the smaller round-37 copy. The HIGH item of considerthese proposal 1: the bytes
remain in pushed history (`2a3707c8`, `58466627`) unless the operator rewrites history — no lane action may.

## Risks / limits (declared)

- Shape, not provenance: 13 of 25 R2 findings and the 21 non-D1 R1 findings are counters, fixtures or the round-43 seat's own probe
  window; triage is a human step. The gate prints no sensitive value.
- Self-application: the gate's source embeds synthetic fixtures, so scanning the seat copy inside `.ufo/` reports R1 3 / R2 2 / R3 1.
  Installing it at `quality/` (outside `.ufo/`) keeps the tree scan clean; a committed seat copy would flag itself by design.
- Scope: only tracked blobs under `.ufo/` at one revision; untracked leaks, `corpus/` leaks and binary-shaped text are invisible; text
  capped at 16 MiB per blob; R4's 10-path default is policy.
- Recommended D1 fix (L1-owned): apply `project-d1.py` to the two files, re-run the gate at the fix commit, expect `findings=48` with
  neither path listed. History rewrite stays operator-owned.

Host: read-only; no pacman or package transaction, no compositor mutation, no input injection, no Wayland client of this seat; the only
host read is the allowed `hyprctl monitors all -j` inside the R3 control and it is not persisted. Python 3.14.8, git 2.56.0, nothing
installed. Scratch (`/fast/scratch/hyaku/mado-r45/ExecPrivacyGate`) deleted after the receipts were copied into the seat dir.
