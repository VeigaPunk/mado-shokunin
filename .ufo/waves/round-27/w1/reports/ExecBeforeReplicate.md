# Before-state replication (C1 + C2) — mado round 27 w1

Seat `MadoR27.ExecBeforeReplicate` · lane repo `mado-shokunin` (jj-colocated, branch master) · base REV
`543f0445e9d60bdfa026c54772d29e8b96bc844b` · 2026-10-23.

Assigned: re-run both frozen before counters at base with fresh seeds, save the receipts next to the L1
pilot receipts, and compare verdicts and counter pins.

## Verdict

Both before receipts replicate. C1: `TARGET_MISSED 0/41`, `tool=MISSING_TOOL`; C2: `TARGET_MISSED
green=0/8 w_killed=0/15`. Counter sha256 pins are identical to the pilot receipts and to the frozen
registration values. The only differences between pilot and replica are the seed line and — in C1 only —
the 40 generated-case descriptor lines that the seed drives; every verdict-bearing line (header pin,
snapshot digest, ORACLE_CHECK, ORACLE_VERSION, HOST_SAFETY, PRED line, `exit=`) is byte-identical.

## Exact commands (run once each, fresh seeds, concurrently)

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && env -i PATH=/usr/bin HOME=/home/vgpnk \
  timeout 900 python3 -I .ufo/waves/round-27/c1/count.py 543f0445 --jobs 6 \
  > .ufo/waves/round-27/evidence/c1-before-543f0445-run2.txt 2>&1
cd /home/vgpnk/Projects/shokunin/mado-shokunin && env -i PATH=/usr/bin HOME=/home/vgpnk \
  timeout 900 python3 -I .ufo/waves/round-27/c2/count.py 543f0445 --jobs 6 \
  > .ufo/waves/round-27/evidence/c2-before-543f0445-run2.txt 2>&1
```

Shell exit codes: C1 `shell_rc=1`, C2 `shell_rc=1` (both counters also print `exit=1`); no stderr, no
traceback (grep `Traceback` count 0 in both). Wall times 17.2 s (C1) and 2.1 s (C2). Receipts were
captured stdout+stderr verbatim; file sizes 4469 B / 50 lines and 3675 B / 32 lines.

## Receipts written

| file | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-27/evidence/c1-before-543f0445-run2.txt` | 4469 | `3bdd2b6606522857910203f22b91843a5cfcf8e8e5aa42fd338a43bf24cfc0d9` |
| `.ufo/waves/round-27/evidence/c2-before-543f0445-run2.txt` | 3675 | `daa7ac50979cc5da914a9dd7bfd6e037f604b7b2e136273c122ec70172d07b66` |

Pilot receipts compared against: `c1-before-543f0445.txt` sha256 `fe5e5d7846b295ba997bab8b21e316d1fc7100f5c39f1bcaf6ac810cc057e405`,
`c2-before-543f0445.txt` sha256 `b63b14d9c2a1b23706ef091b5ce1ecf214e46b15e725cbdac5ca9e66d0af24ae`.

## Pin and outcome comparison (pilot → replica)

C1 (pilot seed `0123456789abcdef` → replica seed `6d1ab5f835f90ae7`):

| line | pilot | replica | same |
|---|---|---|---|
| counter header | `counter c1-r27 sha256:3d7d301f…3136 rev=543f0445e9d… oracle.py sha256:0da0b855…87601` | identical | yes |
| tool status | `tool=MISSING_TOOL at 543f0445…` | identical | yes |
| snapshot | `files=79 digest sha256:fe1b2d8b…983727` | identical | yes |
| ORACLE_CHECK | `base_twice equal rules=0` | identical | yes |
| ORACLE_VERSION | `commit=efb50993… tag=v0.56.2` | identical | yes |
| case outcomes | 41 CASE lines (BASE + C00–C39), all `FAIL tool absent` | same 41 case IDs, all `FAIL tool absent` | yes |
| HOST_SAFETY | `before=1338 after=1338 delta=0` | identical | yes |
| PRED / exit | `cases_pass=0/41 verdict=TARGET_MISSED` / `exit=1` | identical | yes |

C1 diff: 50 lines each; exactly 41 lines differ — the `seed=` line plus the 40 `CASE C00…C39` lines whose
descriptor text and `oracle_rules=` count are generated from the seed; the 9 remaining lines are
byte-identical (the `CASE BASE` line and the 8 verdict/header lines listed above). The oracle ran 42
nested instances in the replica (BASE twice + 40 cases) and answered every one; `base_twice` agreed.

C2 (pilot seed `11` → replica seed `203b12c92d7a809b`):

| line | pilot | replica | same |
|---|---|---|---|
| counter header | `counter c2-r27 sha256:2e180ed2…54dc7 rev=543f0445e9d… w=…mutants-w.json sha256:0ad0e46c…23608` | identical | yes |
| three SUBJECT lines | `4ed70b54…`, `b92c32da…`, `803e0096…` | identical | yes |
| SUITE A / SUITE B | `MISSING at REV` / `MISSING at REV` | identical | yes |
| 8 GREEN runs | all `FAIL | suite … missing` | identical | yes |
| 15 W cases | all `SURVIVED | suite … missing` | identical | yes |
| PRED / exit | `green=0/8 w_killed=0/15 h_killed=0/0 h_need=0 h_valid=0 h_invalid=0 verdict=TARGET_MISSED` / `exit=1` | identical | yes |

C2 diff: 32 lines each; exactly 1 line differs (`seed=11` → `seed=203b12c92d7a809b`); the other 31 lines
are byte-identical, including every per-case line. No held-out directory was passed, matching the pilot
(`h_valid=0`).

Frozen pins re-verified before running, all matching registration:
`c1/count.py 3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136`,
`c2/count.py 2e180ed29c31abcb3421d7e57a147d05ac9d2982ebe4dbc555747b287e754dc7`,
`harness/oracle.py 0da0b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`,
`c2/mutants-w.json 0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608`. The counters
themselves re-check the oracle pin and print the W pin, so the replica also re-certifies those bytes.

Interpretation for the claim gate: at base both operations are measured as missing, exactly as claimed
(`tool=MISSING_TOOL`, both suites `MISSING at REV`); neither PRED line is met before data. The before
state is not vacuous: the C1 counter still built its 41 cases and ran 42 oracle instances (BASE pair
agreeing, version pin correct), and the C2 counter still cloned REV per case and confirmed the subjects'
bytes — so the zeros are measured zeros, not a failed harness.

## Host safety

- Coredumps: `coredumpctl list | grep -c /usr/bin/Hyprland` = 1338 immediately before, 1338 after both
  runs (external check), and each counter's own `HOST_SAFETY … delta=0`.
- Only the counters' own oracle path was used; no Hyprland was started by me directly, no
  `/dev/dri` node touched by me, no `WAYLAND_DISPLAY`/`HYPRLAND_INSTANCE_SIGNATURE` set or inherited
  (`env -i` in both commands). No live-compositor `hyprctl` calls were made.
- Process cleanup: my C1 run removed its `m27c1-*` temp tree on exit (`finally: shutil.rmtree`), and my
  C2 clones are removed per case. No process from my runs remains; the sandbox/bwrap/git processes seen
  at 07:33 all reference `5ddc5885` (after-REV control scoring by other seats) or `m27c1-*` dirs created
  at 07:33:20, after my 07:32:47 completion — none are mine (my runs used REV `543f0445`).
- `/fast` had 115 G available before the runs; both counters write only small temporary trees. No
  unbounded writes, all invocations under `timeout 900`.

## Files written

- `.ufo/waves/round-27/evidence/c1-before-543f0445-run2.txt`
- `.ufo/waves/round-27/evidence/c2-before-543f0445-run2.txt`
- `.ufo/waves/round-27/w1/reports/ExecBeforeReplicate.md` (this report)

No lane file was edited; no git/jj write commands were run; no counters, harness or W set was touched.
No tool was installed or upgraded (none needed). No subagent was dispatched (leaf role; no spawn tool is
present, and this replication needed none). No blockers.
