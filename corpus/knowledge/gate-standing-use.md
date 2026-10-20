# The gate's standing-use note — `mado-verify.sh` (M10-2, round 10)

source: measured at the landed revision `tools/mado-verify.sh` sha256
`93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`
(3,231 L by `wc -l` / 150,103 B, mtime 2026-10-14 17:05:32 −03:00; committed
`de22dfd`, round-9 landing). Help text, mode helps and verdict lines quoted
from that revision; every run below is this lane's own, logs and snapshots in
scratch `/tmp/w10-mado-m10-2/`.
verified-at: 2026-10-14 20:44–20:56Z (host offset −03:00), single host
(bash 5.3.15), read-only, no substrate write, no session disturbance.
recheck: `sha256sum tools/mado-verify.sh` — a moved sha invalidates every
number here; then `bash tools/mado-verify.sh --selftest` (today 268/268) and
the four modes re-run from `corpus/knowledge/ten-round-synthesis.md`'s
ledger.

Marks: **[O]** observation (command output quoted), **[I]** inference,
**[U]** unknown. Round-9 landed at this revision; the numbers below are the
landed state, not the design-time plan values.

## 0. Custody — one instrument, one writer

The gate is the lane's **single verdict instrument**: `MADO_VERIFY:
CLEAN|DIVERGED` is the only token mado issues about the config plane [O,
`tools/mado-verify.sh:9-13`]. Rules that keep it trustworthy:

1. **Single writer.** The gate has one editing lane per round; every other
   lane reads and re-runs it, never edits it. The round-9 scribe lane watched
   the file move six times and recorded shas without touching it
   (`plans/round-9-record-draft.md` §10 v2a) — the pattern to copy.
2. **Every edit carries its provenance**: lane identity, a `LOG.md` entry,
   and the widening discipline of §5. Round 9's edit is traceable end to end
   (re-cut record `:1254-1268`; receipts in
   `corpus/knowledge/snapshot-diff-receipt-r9.md` §2).
3. **Never edited to match reality.** A moved pin is *reported first* — the
   response is re-verification plus an appended erratum, never a silent pin
   update (theme note §10 errata route; standing rule "errata append-only",
   `SKILL.md:36`).
4. **Read-only on every substrate.** hyprctl read verbs only; no file
   written; scratch under `/tmp/w5-mado-m52-*` and only `--selftest` makes it
   [O, header `:21-30`]. Session material is shape-only.
5. **Receipts stay in scratch.** Snapshots, sweep workdirs and logs are never
   committed; the record quotes their lines instead [O, round-9 practice].

## 1. Invocation map (quoted from the landed revision)

Base help — `bash tools/mado-verify.sh --help` (exit 0; `-h` identical) [O]:

    usage: mado-verify.sh [--no-live] [--live] [--root DIR] [--selftest] [--help]

      (default)     live read-only run against $HOME (or MADO_VERIFY_ROOT)
      --no-live     file plane only; the verdict names the skipped live layer
      --root DIR    verify DIR as the config root (default $HOME)
      --selftest    hermetic fixture tests under /tmp/w5-mado-m52-* (no substrate)
      --help        this text

    verdict: MADO_VERIFY: CLEAN|DIVERGED (...)   exit 0 / 1  (usage error: 2)
    env: MADO_VERIFY_ROOT (config root), MADO_VERIFY_LIVE=auto|yes|no

`--regression --help`, `--snapshot --help` and `--snapshot-diff --help` add
the mode rows (base help deliberately omits them — the excision invariant,
§5.7) [O]. The mode contract, as printed:

    --regression  replay the recorded mutation case (tameshi T6-1 spec at
                  pinned bytes over the recorded gate revision); --keep
                  retains the scratch root also on PASS. No substrate read.
    --snapshot FILE   run the gate (honouring --no-live/--live/--root) and write
                  a v1 verdict snapshot to FILE (FILE must not exist; receipts
                  are never overwritten). Exit = the run's verdict; the write
                  adds MADO_SNAPSHOT: WRITTEN|REFUSED (a refusal exits 2).
    --snapshot-diff OLD NEW  diff two snapshots class by class; MADO_DIFF:
                  SAME|DETAIL-CHANGED|CHANGED|SETUP (exit 0/0/1/2). Reads only
                  the two files; never prints MADO_VERIFY:.

| Mode | Contract | Writes | Exit |
|---|---|---|---|
| (default) | live read-only run against the root (`$HOME` or `MADO_VERIFY_ROOT`) | nothing | 0 CLEAN · 1 DIVERGED |
| `--live` | force the live layer on (used with `--root`) | nothing | as above |
| `--no-live` | file plane only; the verdict names the skip; the 8 rows that need live reads print SKIP (`live.plane` + the 7 omarchy live rows) | nothing | as above |
| `--root DIR` / `--root=DIR` | verify DIR as the config root; a missing value is `usage error: --root needs a directory`, rc 2 [O]; trailing `/` stripped, empty → `/` | nothing | as above |
| `--selftest` | hermetic fixtures, no substrate | `/tmp/w5-mado-m52-*` | 0 pass (268/268 [O]) · 2 fail (`MADO_SELFTEST: FAILED — N passed, M failed`, fixtures kept, `:1211-1214`) |
| `--regression [--keep]` | replay the recorded mutation case through tameshi's harness; refuses `--target --defects --suite --label --workdir --timeout --tail` and the gate's own `--no-live/--live/--root/--selftest` (usage error, 2) [`tools/mado-verify.sh:1278-1281`] | scratch `/tmp/mado-verify-regression.*` (removed on PASS; `--keep` retains) | 0 PASS · 1 FAIL · 2 SETUP · 2 usage |
| `--snapshot FILE` / `--snapshot=FILE` | ordinary run, report passed through verbatim, then the v1 receipt; FILE must not exist and must not sit inside the verified `<root>/.config` plane | FILE only | the run's verdict; a refusal exits 2, nothing written |
| `--snapshot-diff OLD NEW` | reads only the two files; never prints `MADO_VERIFY:` | nothing | 0 SAME · 0 DETAIL-CHANGED · 1 CHANGED · 2 SETUP |
| `--help` / `-h` | base text; mode helps via `<mode> --help` | nothing | 0 |

Environment [O, `:78-79`, `:1505`, `:3179-3186`]: `MADO_VERIFY_ROOT` (config
root), `MADO_VERIFY_LIVE=auto|yes|no` (`auto` = live only when the root is
`$HOME`; a non-home root skips live with the reason "non-home root"; a bad
value is `usage error: MADO_VERIFY_LIVE must be auto|yes|no`, rc 2 —
measured), `MADO_VERIFY_HARNESS` (override the mutation harness path; default
`<fleet>/tameshi-shokunin/tools/mutate-and-run.sh`).

## 2. Reading a verdict

One screen, five parts: version line, mode line, row table
(`plane check status detail`), counts line, verdict line [O].

- **Row classes** PASS / FAIL / UNKNOWN / SKIP / NOTE.
- **UNKNOWN blocks CLEAN**: the verdict is DIVERGED when `fail>0` *or*
  `unknown>0` [`tools/mado-verify.sh:3219`]. A check that cannot be read is
  never agreement.
- **NOTE never flips the verdict** but stays visible in the report — it is a
  record-level finding or an operator-owned fact (theme choice, counters,
  D-1) [header `:29-30`].
- **SKIP** marks a row whose read belongs to the live layer when that layer is
  not requested — 8 rows under `--no-live` (`live.plane` + the 7 omarchy live
  rows; every detail reads "live layer skipped") [O].
- **Exit map**: 0 CLEAN · 1 DIVERGED · 2 usage [header `:12-13`]. The
  DIVERGED line names the first FAIL, else the first UNKNOWN, with its
  detail [O, `:3229-3231`].

**Worked example — a live FAIL that was session weather, not config damage**
(this lane, two runs 2 s apart, logs `live.log` / `live2.log`):

    run 1: MADO_VERIFY: DIVERGED (3 fail, 0 unknown, 49 pass) — first fail: live.waybar.process (no waybar process)   rc 1
           FAILs: live.waybar.process / live.waybar.layer / live.waybar.tray
    run 2: MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes verified read-only)   counts: pass=52 fail=0 unknown=0 skip=0 note=8   rc 0

The live layer had caught the session mid-waybar-restart; the process returned
with a new pid (3501967; the round-9 reading had 1203352 [O]). The file plane
never moved: `gate boundary.readonly PASS`, combined sha `bb2639d9a980…` in
*both* runs [O]. **Reading rule: re-run once before filing a live FAIL.** A
FAIL that survives the re-run is a finding about the declared plane or the
session — never a defect of the gate, and never smoothed.

## 3. The snapshot-diff mode — the receipt pair

Purpose: prove *what moved* between two readings, class by class, with each
snapshot naming its own revision, root, scope and counts. Runbook [O, all
measured this lane; scratch `/tmp/w10-mado-m10-2/`]:

    bash tools/mado-verify.sh --snapshot /tmp/w10-mado-m10-2/a.snap      # ordinary run; receipt written
    … the change / the later reading …
    bash tools/mado-verify.sh --snapshot /tmp/w10-mado-m10-2/b.snap
    bash tools/mado-verify.sh --snapshot-diff /tmp/w10-mado-m10-2/a.snap /tmp/w10-mado-m10-2/b.snap

Measured outcomes: a live pair 1 s apart → `MADO_DIFF: SAME (rows 60→60;
regressed=0 recovered=0 flipped=0 relaxed=0 relabeled=0 appeared=0 vanished=0;
detail-changed=0; scope=0)` rc 0; a live snapshot (60 rows) vs a `--no-live`
snapshot (41 rows) → `MADO_DIFF: CHANGED (rows 60→41; … relabeled=7
appeared=1 vanished=20; detail-changed=7; scope=1)` rc 1 with `DIFF_SCOPE
scope: live → file-plane` and `DIFF_COUNTS`; a missing file → `MADO_DIFF:
SETUP (missing snapshot file: …)` rc 2; the same file twice → SAME rc 0.

Receipt discipline (measured):

- **Receipts are never overwritten.** Re-snapshotting onto an existing path
  → `MADO_SNAPSHOT: REFUSED (destination exists: … — receipts are never
  overwritten)`, rc 2, nothing written [O].
- **Never inside the verified config plane**: `--snapshot
  ~/.config/<name>.snap` → `REFUSED (destination is inside the verified
  config plane: …)`, rc 2, the file confirmed absent [O]. Snapshots live in
  scratch.
- Refusals also fire when the child run exits outside 0/1, when the printed
  rows do not reconcile with the printed counts (a multi-line detail is
  refused, never truncated), and when the write or its read-back fails
  [:1647-1661].

**Diff classes** (contract `:1663-1671`; the machinery keys rows by
`plane|id` and compares status, then detail):

| class | trigger |
|---|---|
| `regressed` | PASS / SKIP / NOTE → FAIL / UNKNOWN |
| `recovered` | FAIL / UNKNOWN → PASS |
| `flipped` | FAIL ↔ UNKNOWN |
| `relaxed` | FAIL / UNKNOWN → SKIP / NOTE |
| `relabeled` | any other status move |
| `detail` | same status, new detail (the drift-watch signature) |
| `appeared` / `vanished` | row only in NEW / only in OLD |
| scope | a moved `tool` / `gate-sha256` / `root` / `scope` field |

`created:` is receipt-time provenance and is never compared (:1672-1677).
**Verdicts and exits**: SAME 0 · DETAIL-CHANGED 0 (details moved, classes did
not) · CHANGED 1 (a row class or a scope field moved — the pair *brackets a
movement*, not a failure; round-9's landing receipt read CHANGED with rc 1 by
contract) · SETUP 2.

**The revision field is the point.** A pair straddling a gate edit separates
"the gate changed" (`DIFF_SCOPE gate-sha256`, zero row classes) from "the
observation changed" (`DIFF_ROW` lines) — measured in round 9's first real
use: `corpus/knowledge/snapshot-diff-receipt-r9.md` §2/§3, where the edit
produced `appeared=10` (the ten theme ids) with `detail-changed=0`.

**Noise floor, measured**: round 9's controls read `MADO_DIFF: SAME` with
`detail-changed=0` across a 12-minute same-revision window; my 1-second pair
reproduces it. A real `DETAIL-CHANGED` instance has not been observed on this
host **[U]** — the class contract is measured, the instance is not.

## 4. Standing cadence — when to run what

| Trigger | Run | Established |
|---|---|---|
| a config file changed (operator or tool) | live run; read the verdict, re-run a live FAIL once | round-5 mint (M5-2) |
| pre-commit in this repo | `--selftest` (today 268/268) | round 5, kept every round |
| file-plane-only question, or a non-home tree | `--no-live`, `--root DIR` | rounds 5–7 |
| gate edit **inside** the marked pairs | re-run `--selftest`; the pin stays valid | round 7 (designed split) |
| gate edit **outside** the pairs (a widening) | run `--regression`; until re-cut it reads SETUP with the printed `REGRESSION_RECUT`; carry `MADO_REGRESSION: PASS` | round-7 reading rule 1 |
| a new clause/row lands | ship a covering mutant — nothing ships wider without one | round-6 reading rule 2 |
| drift watch / before-after pair | snapshot pair + `--snapshot-diff`; receipts in scratch | round 8 (M8-3) |
| a receipt must outlive the window | quote its lines in the record; never commit the file | rounds 8–9 practice |

## 5. Maintenance rules, with their ancestry

1. **Round-6 reading rule 2** (round-6 append, `SKILL.md:597-601`,
   `:887-891`): a *surviving* mutant says "no test notices this clause", never
   "the clause is broken"; a clause stands until a mutant proves otherwise;
   nothing ships wider without a covering mutant. **Owed today**: the ten
   recorded defects (D1–D9 + R1) still die 10/10 at the landed pin, but no
   mutant targets a theme clause — the gate's own re-cut record says it
   (:1266-1268, "owed by the sweep lane … recorded, not smoothed").
2. **Round-7 reading rule 1** (round-7 append, `SKILL.md:783-793`): every
   gate-widening claim carries `MADO_REGRESSION: PASS`. A widening lands rows
   outside the excised pairs, so the derived target stops equalling
   `PIN_MADO` and the mode reads **SETUP, never stale-PASS**; the printed
   `REGRESSION_RECUT` command is the remedy — re-sweep, then update
   `PIN_MADO`/`TABLE_MADO` from the measured table.
3. `MADO_REGRESSION:` and `MADO_VERIFY:` never mix: a regression run prints
   zero `MADO_VERIFY:` tokens [O, this lane's regression log; same reading in
   the round-7/8 records]. A SETUP is not a gate failure — it says the case
   could not be verified; only FAIL names a non-reproducing table.
4. **Pins are never edited to match reality.** A MOVED pin reports itself
   (omarchy rows FAIL naming the pin and the value); the response is
   re-verification and an appended erratum. **Exemptions are by name and
   counted** — round 9 exempted the theme's two live rows and the whole
   walker live surface by name (SKILL round-9 append, "Exempted by name").
5. **Harness boundary.** tameshi's `mutate-and-run.sh` is consumed
   **read-only** (sha `cf41efaa…242c75` today, unchanged since the round-8
   freeze); its revision is printed as *provenance, not gated* (the recorded
   `b56c6e57…` differs and that is fine — the kill table is the check). A
   needed harness change is a **recommendation to tameshi, never a patch**;
   the exit-flatten family stays a recommendation [M6-1 §3].
6. **Marker families at the landed revision** (measured): `MADO-R7-SELFTEST-
   BLOCK` `:414-:593` · `MADO-R8-OMARCHY-BLOCK` `:596-:775` · `MADO-R8-BLOCK`
   twice, `:1041-:1204` and `:1635-:2157` · `MADO-R7-REGRESSION-BLOCK`
   `:1216-:1634`. The excisor (`mado_r7_target_build`, `:1374-1385`; sed
   `:1380-1382`) deletes the R7-REGRESSION, R7-SELFTEST and both R8-BLOCK
   ranges. Re-derived here: 3,231 − those ranges = **1,945 L, sha256
   `dc7c4141449891cdd83bb603aff7215358328a9ce1b32dba0bb9c0514cb6f8fd` = the
   `PIN_MADO` constant** [O — this lane's own sed run, scratch
   `target.sh`]. Note (measured): the OMARCHY pair is *not* excised — its
   markers and rows survive in the derived target — so edits there move the
   pin like any edit outside the excised pairs.
7. **Cosmetics that are load-bearing.** The base `--help` stays silent on
   the mode flags and `VERSION_STR` still self-labels `v1 (mado-shokunin
   round 5 / M5-2)` (`:77`; it is also copied into every snapshot's `tool=`
   line) — the excision invariant depends on the base text not moving
   [:1630-1633]. Neither is a defect; both are in the ledger so nobody
   "fixes" them into a re-cut by accident.

## 6. Residual and limit ledger (re-checked at the landed revision)

**Open residuals** — each with the check that shows it open [O]:

| Residual | Check at `93e43f8f…` | State |
|---|---|---|
| theme live rows `theme.wallpaper.live`, `theme.name.display_agree` | `grep -n 'wallpaper.live\|display_agree' tools/mado-verify.sh` → 0 | exempted by name (round 9) |
| walker live-surface rows (2 sockets, D-Bus owner, layer invariant) | `grep -c 'walker.sock'` → 0; walker live = version + services only (`:2728-2747`) | exempted by name (round 9) |
| hypr-live stub scenarios J/K/L | 0 scenario-label hits; no `hyprctl` PATH stub | open since round 8 ((a8) partial) |
| assertion floor: `VERSION_STR` (:77), base-help discoverability | `VERSION_STR` unchanged; base help prints no mode row | open since round 8; §5.7 says why the help stays |
| the two usage arms (`--root` no value, bad `MADO_VERIFY_LIVE`) | behaviour present (rc 2, measured); 0 suite assertions for them | carried from the round-8 assertion-floor residue ((c8)) |
| boundary combined-hash prefix unasserted | `grep -c 'bb2639d9' tools/mado-verify.sh` → 0 | open since round 8 |
| `row_from_rc` rc-6 arm | `:116-122` maps 6 → UNKNOWN; the six callers' parse arms return 3/4/5 [I, per the round-9 scribe §3.2], so 6 is unreached today | dead branch, open since round 6 |
| theme clauses' covering mutant | re-cut record `:1266-1268` says owed | owed (round-6 rule 2) |

**Closed since round 8** (for contrast, so the ledger cannot read as "nothing
lands"): the theme plane's **file arm** — 10 rows, scenarios T1–T9, live
reading 9 PASS + 1 NOTE; census widening (helper regex seven → eight ids at
seven sites `:387`, `:391`, `:406-410`; `row` sites 162 → 189 + 6
`row_from_rc`; distinct ids 55 by literal sites / **61 as emitted at run
time**, this lane's union count); asserted row ids 22 → **32**; the re-cut
(`PIN_MADO` `d2bcdb31…` → `dc7c4141…`) with `MADO_REGRESSION: PASS` —
re-run by this lane at the landed revision: `REGRESSION_TABLE … match=10/10
recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0`,
`MUTATE_RESTORE: OK`, spec `c7ee75b9…1dd8` (recorded pin matches),
`REGRESSION_DATE 2026-10-14T20:51:10Z` [O].

**What the gate does not prove** (its own header, `:70-72`):

- a **stub scenario proves row logic, never live values** — the hermetic
  fixtures exercise the code path, not the host;
- rendered UI, socket protocol, idle/lock transitions, dispatcher behaviour,
  waybar module text, window-rule *effects* have no read surface: they stay
  **UNKNOWN by constraint**, never guessed;
- live rows degrade to UNKNOWN when their read verb is absent (`have`
  guards), never to CLEAN; the file plane fails closed on a missing tree —
  per-row UNKNOWN, and a wholly missing root reads DIVERGED (the round-7
  recorded reading; not re-measured here — carried as **[O-record]**);
- a snapshot/diff pair proves only what the rows carry; `created:` proves
  when it was taken, nothing about intent.

**Record-level debt that ships with the arc** (not gate defects; named so the
handoff is honest): `corpus/README.md` rows unpaid (8 note rows; notes
unrowed), `corpus/lessons/` 0 entries after nine rounds, `walker-deep.md`
§10/§11 errata still owed (sha `0982ba066c72575a…` unchanged; M9-2's
`walker-deep-r9.md` is a new note, not that append), the committed round-8
draft's ⟨PENDING⟩ markers.

## 7. Handoff — the operator's part

- **When the gate reads DIVERGED**: read the row's detail, re-run once
  (session transients are real — §2's worked example), then treat a surviving
  FAIL as a finding about the declared plane or the session. mado can
  re-verify and describe; it cannot write the config (PROVINCE.md:10-12 —
  probe, measure, recommend; the operator applies).
- **When a config file changes**: run the live gate afterwards. A FAIL is the
  file's effect; a NOTE is a record, not a defect.
- **When the gate is edited**: the editor carries §5's discipline and the
  receipts (selftest count before → after, `MADO_REGRESSION: PASS` at the
  widened revision, the re-cut record appended in the gate's own header).
- **When to re-sweep via tameshi**: after every gate edit outside the excised
  pairs (the mode reads SETUP until the re-cut — that alarm *is* the job);
  and whenever new clauses land, because a covering mutant is owed (rule 2).
  The sweep is either `--regression` (harness invoked read-only) or the
  printed `REGRESSION_RECUT` command for the re-cut itself. Nothing in the
  sweep touches the substrate.
- **What stays the operator's call**: the theme choice, every config edit,
  the omarchy checkout (never `git status`/`fetch` from this lane), and the
  lane's promotion (never self-declared).

## 8. Re-deriving this note (three commands)

    sha256sum tools/mado-verify.sh                                   # 93e43f8f… as of this write
    bash tools/mado-verify.sh --selftest && bash tools/mado-verify.sh --no-live
    bash tools/mado-verify.sh --regression | grep -E 'MADO_REGRESSION|REGRESSION_TABLE'

A moved gate sha means this note describes history: re-run the modes, re-read
§1 from the live helps, and re-check §6's greps before quoting any number.

## Appended receipt — lane M10-3: the first cadence tick (2026-10-14)

Append-only block; the note above is M10-2's and is not edited. This is §4's
first live `--regression` tick at the standing revision; log
`/tmp/w10-mado-m3/regression.log` (scratch, not committed).

- **[O] Command / revision / date.** `bash tools/mado-verify.sh --regression`
  at gate sha256 `93e43f8fe8b9bdd48c895cccfac11d5b23f97d8793fc6fb43987b4afdbc00095`
  (3,231 L; working tree = landed commit `de22dfd`), 20:51:07Z → 20:52:03Z,
  56 s, rc 0.
- **[O] Verdict.** `MADO_REGRESSION: PASS (case=mado-verify-hardened;
  target=dc7c4141449891cdd83bb603aff7215358328a9ce1b32dba0bb9c0514cb6f8fd)`;
  `REGRESSION_TABLE … match=10/10 recorded-killed=10 measured-killed=10
  survived=0 inconclusive=0 flips=0`; `REGRESSION_CASE … PASS
  (… control=green restore=ok)`.
- **[O] Drift: none.** Target pin `match=yes`; spec sha `c7ee75b9…1dd8` =
  recorded pin; gate sha identical before and after the run;
  `REGRESSION_CLEANUP: removed=10`; workdir
  `/tmp/mado-verify-regression.a2yosa` removed on PASS; harness line
  `cf41efaa…242c75` vs recorded `b56c6e57…` — the §5.5 provenance line,
  printed, not gated.
- **[O] Overlap.** This run's window contains the §6 re-run's timestamp
  (`REGRESSION_DATE 20:51:10Z`); both PASSed with independent `mktemp -d`
  scratch roots (one instance — not a general safety claim).
- **[O] Residual unchanged by this tick.** The played spec is still round 8's
  byte (`c7ee75b9…`, 10 defects); the theme clauses' covering mutant stays
  owed (§5.1/§6). The tick re-proves the recorded case; it does not close
  that item. Cross-check: verdict/pin/table equal AUD-M9's landed receipt
  (`93e43f8f…`, 53.9 s; `reports/r9-aud-m9.md` C4).

recheck: `bash tools/mado-verify.sh --regression | tail -1` — expect
`MADO_REGRESSION: PASS` with target `dc7c4141…` while the gate sha is
`93e43f8f…`.

## Current receipt — round 13 (2026-10-20)

Historical “today” pins and cadence commands above describe the 2026-10-14
arc. The current registry is `SKILL.md` § Gate registry. The delivered gate
SHA-256 is `037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569`;
rederive with `sha256sum tools/mado-verify.sh`, bound to the measured content
commit named in the round-13 SCORECARD and report.

- Hermetic suite: **310/310**, exit 0 — `bash tools/mado-verify.sh --selftest`;
  `.ufo/waves/round-13/evidence/gate-selftest.txt`.
- File plane: **29 PASS, 0 FAIL, 0 UNKNOWN, 8 SKIP, 4 NOTE**, exit 0 —
  `bash tools/mado-verify.sh --no-live`; `evidence/gate-file-plane.txt`
  under that round directory. No current full live-health run is claimed.
- Derived target `PIN_MADO`: `538d178b…` →
  `87910c39f460ad169b879fc28f2e80f2c988d56f91e18b51efcac9cb0ec04b39`.
  Actual re-cut: historical 10/10 KILLED, restore OK; byte-preserved
  `SPEC_SHA=c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8`.
  `evidence/regression-recut.txt` carries the command and complete output.
- New clauses: **8/8 covering mutants KILLED**, restore OK —
  `covering.spec`, `evidence/covering-mutants.txt` and
  `evidence/covering-results.tsv`. The target is the derived executable,
  so a pin-identity assertion cannot mask missing behavioral coverage.
- Mutable sibling harness observed SHA-256
  `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`,
  not the older `cf41efaa…` or recorded `b56c6e57…`. No sibling was edited.
- Two-evidences replay:
  `python3 .ufo/waves/round-13/frozen/verify.py` verifies both committed
  input digests before execution, then reports `frozen_match`, exit 0,
  and `MADO_REGRESSION: PASS` (10/10 table match, flips 0).
  Its `--selftest` passes **12/12**, exit 0; expected pins and verdict live
  in `frozen/expected.json`, observations in `evidence/frozen-regression.txt`
  and `evidence/frozen-selftest-corrected.txt`.

All abbreviated `evidence/`, `frozen/` and `covering.spec` paths in this
receipt are under `.ufo/waves/round-13/`. Snapshot copies are immutable
round evidence, not maintained aliases of the working gate or sibling.
Expanded toggle-glob membership, generic config parsing, per-feature
behavior, the historical theme-mutation gap and the broad whole-config
boundary-hash caveat are not closed by the four-case census correction.