# K1DoNothing — C1 control, shape DO-NOTHING (mado round 26, wave w1)

## What I did

Scored the do-nothing shape against the frozen C1 counter in both forms the assignment names — a tool that
exits 0 printing nothing, and a 0-byte tool file — two fresh-seed runs each, and the absent-tool baseline at
REV `96101be5` with no `--tool-file`. Nothing in `tools/` was built or edited; the counter and harness were
read only and their pins re-verified before scoring.

## Files

| artifact | path | sha256 | size |
|---|---|---|---|
| control (shape A) | `.ufo/waves/round-26/controls/K1DoNothing.py` | `a3e814b76c2154e086e272b57abc3f4d9726f127b0ee6db8f5286b19c3e48a94` | 721 B |
| control (shape B, empty) | `/fast/scratch/hyaku/mado-r26/K1DoNothing-empty.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 B |
| receipts (all runs, verbatim) | `.ufo/waves/round-26/controls/K1DoNothing.txt` | `1347144b2b8ce87fb53af8325bde0b877d8f6f67dce8fc2591cec1f6d1e7087d` | 19600 B |

Shape A source (whole program, 721 B): docstring, `import sys`, `sys.exit(0)`. It reads no path, prints no
byte. Shape B is an empty file; `python3 -I <empty> --home …` exits 0 with empty stdout (verified directly
before scoring: `empty-exit=0`, `ctl-exit=0`, no output).

Pins re-verified before the first run:
`sha256 .ufo/waves/round-26/c1/count.py` = `f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd`,
`sha256 .ufo/waves/round-26/harness/oracle.py` = `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441`
— both match the registration. `git rev-parse --verify 96101be5^{commit}` =
`96101be523b2f6e897eee743d5b396b0225bf9ed`; `git cat-file -e 96101be5:tools/mado-anims.py` fails ("path … does
not exist"), so the baseline is genuinely `MISSING_TOOL`.

## Exact commands

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count.py 05319e0f \
  --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1DoNothing.py   # shape A, ×2
timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count.py 05319e0f \
  --tool-file /fast/scratch/hyaku/mado-r26/K1DoNothing-empty.py                                         # shape B, ×2
timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count.py 96101be5    # absent-tool baseline
```

No `--seed` is passed, so every run draws its own `os.urandom(8)` seed (printed by the counter). Shape A run 1
and shape B run 1 ran without the outer `prlimit`; the wrapper was added from run 2 on after the L1 note that the
oracle sets its own 8 GB inner `--as` (oracle.py:146) and must not inherit a 4 GB hard cap.

## Results

| run | tool | seed | cases_pass | exit | wall | HOST_SAFETY delta |
|---|---|---|---|---|---|---|
| A1 exit-0 | `K1DoNothing.py` | `4ff9eb367ed814d3` | 0/41 | 1 | 18 s | 0 (1335→1335) |
| A2 exit-0 | `K1DoNothing.py` | `4dfcad47c666397f` | 0/41 | 1 | 18 s | 0 (1335→1335) |
| B1 0-byte | `K1DoNothing-empty.py` | `e3a878c187f90792` | 0/41 | 1 | 29 s | 0 (1335→1335) |
| B2 0-byte | `K1DoNothing-empty.py` | `24536a85388d87b1` | 0/41 | 1 | 18 s | 0 (1335→1335) |
| base 96101be5, no tool | `MISSING_TOOL` | `8c17262e1dd584ba` | 0/41 | 1 | 47 s | 0 (1335→1335) |

All five runs printed `ORACLE_CHECK base_twice equal nodes=35 beziers=6`, so the oracle was live and stable in
every run; these are measurements, not guard exits (except the one exit-2 attempt noted below). Each failing
case carries the same reason: `stdout is not JSON` for both do-nothing shapes, `tool absent` for the baseline.

## Verdict

CONTROL K1DoNothing best: cases_pass=0/41 verdict=TARGET_MISSED — not met

The do-nothing shape cannot meet C1 in either form: the target is `cases_pass=41/41` and the shape passes 0.
This is the expected negative-control result and it is the higher of the two scored shapes (both are 0/41).

## Receipts (verbatim stdout, including the `exit=` line)

### Shape A, run 1 of 2 — exit 0, prints nothing (no outer prlimit)

```
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1DoNothing.py sha256:a3e814b76c2154e086e272b57abc3f4d9726f127b0ee6db8f5286b19c3e48a94
seed=4ff9eb367ed814d3
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL stdout is not JSON (unperturbed)
CASE C00   FAIL stdout is not JSON (NEWSRC+BEZIER)
CASE C01   FAIL stdout is not JSON (REBEZ+INVALID+BEZIER)
CASE C02   FAIL stdout is not JSON (NEWSRC+ROOT+COMMENT+REBEZ)
CASE C03   FAIL stdout is not JSON (ORDER+VARIABLE+UNSOURCED+COMMENT)
CASE C04   FAIL stdout is not JSON (CATEGORY+REBEZ)
CASE C05   FAIL stdout is not JSON (BEZIER+ROOT+INVALID+COMMENT)
CASE C06   FAIL stdout is not JSON (DISABLE+BEZIER+VARIABLE)
CASE C07   FAIL stdout is not JSON (UNSOURCED+SOURCED)
CASE C08   FAIL stdout is not JSON (UNSOURCED+SOURCED)
CASE C09   FAIL stdout is not JSON (DISABLE+COMMENT)
CASE C10   FAIL stdout is not JSON (NEWSRC+BEZIER+ROOT)
CASE C11   FAIL stdout is not JSON (NEWSRC+COMMENT+ROOT+BEZIER)
CASE C12   FAIL stdout is not JSON (COMMENT+DISABLE)
CASE C13   FAIL stdout is not JSON (SOURCED+NEWSRC+ROOT+COMMENT)
CASE C14   FAIL stdout is not JSON (COMMENT+ROOT+INVALID+UNSOURCED)
CASE C15   FAIL stdout is not JSON (CATEGORY+SOURCED+INVALID)
CASE C16   FAIL stdout is not JSON (UNSOURCED+SPACING)
CASE C17   FAIL stdout is not JSON (ORDER+VARIABLE)
CASE C18   FAIL stdout is not JSON (ORDER+COMMENT)
CASE C19   FAIL stdout is not JSON (ROOT+CATEGORY+BEZIER+VARIABLE)
CASE C20   FAIL stdout is not JSON (CATEGORY+SOURCED+UNSOURCED+INVALID)
CASE C21   FAIL stdout is not JSON (BEZIER+ROOT+DISABLE)
CASE C22   FAIL stdout is not JSON (REBEZ+CATEGORY)
CASE C23   FAIL stdout is not JSON (BEZIER+NEWSRC+CATEGORY+ROOT)
CASE C24   FAIL stdout is not JSON (REBEZ+CATEGORY+VARIABLE+ORDER)
CASE C25   FAIL stdout is not JSON (ROOT+VARIABLE+INVALID)
CASE C26   FAIL stdout is not JSON (DISABLE+REBEZ+VARIABLE+ORDER)
CASE C27   FAIL stdout is not JSON (SOURCED+COMMENT)
CASE C28   FAIL stdout is not JSON (BEZIER+SPACING+ORDER)
CASE C29   FAIL stdout is not JSON (BEZIER+CATEGORY+SPACING+COMMENT)
CASE C30   FAIL stdout is not JSON (NEWSRC+DISABLE+VARIABLE)
CASE C31   FAIL stdout is not JSON (VARIABLE+SOURCED)
CASE C32   FAIL stdout is not JSON (CATEGORY+COMMENT+SOURCED)
CASE C33   FAIL stdout is not JSON (REBEZ+SOURCED)
CASE C34   FAIL stdout is not JSON (NEWSRC+INVALID)
CASE C35   FAIL stdout is not JSON (DISABLE+INVALID+REBEZ+SPACING)
CASE C36   FAIL stdout is not JSON (INVALID+CATEGORY+BEZIER)
CASE C37   FAIL stdout is not JSON (REBEZ+SOURCED+UNSOURCED)
CASE C38   FAIL stdout is not JSON (NEWSRC+REBEZ)
CASE C39   FAIL stdout is not JSON (DISABLE+UNSOURCED+INVALID)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

### Shape A, run 2 of 2 — exit 0, prints nothing (prlimit soft:hard 4G:8G)

```
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1DoNothing.py sha256:a3e814b76c2154e086e272b57abc3f4d9726f127b0ee6db8f5286b19c3e48a94
seed=4dfcad47c666397f
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL stdout is not JSON (unperturbed)
CASE C00   FAIL stdout is not JSON (NEWSRC+SOURCED+SPACING)
CASE C01   FAIL stdout is not JSON (UNSOURCED+DISABLE)
CASE C02   FAIL stdout is not JSON (ROOT+UNSOURCED+INVALID)
CASE C03   FAIL stdout is not JSON (COMMENT+REBEZ+CATEGORY)
CASE C04   FAIL stdout is not JSON (ROOT+UNSOURCED)
CASE C05   FAIL stdout is not JSON (VARIABLE+NEWSRC+ORDER+SPACING)
CASE C06   FAIL stdout is not JSON (DISABLE+REBEZ+SPACING+SOURCED)
CASE C07   FAIL stdout is not JSON (UNSOURCED+COMMENT+DISABLE)
CASE C08   FAIL stdout is not JSON (VARIABLE+BEZIER+UNSOURCED+SOURCED)
CASE C09   FAIL stdout is not JSON (DISABLE+SOURCED+SPACING)
CASE C10   FAIL stdout is not JSON (NEWSRC+BEZIER+REBEZ)
CASE C11   FAIL stdout is not JSON (REBEZ+VARIABLE)
CASE C12   FAIL stdout is not JSON (ORDER+VARIABLE+REBEZ+SPACING)
CASE C13   FAIL stdout is not JSON (ORDER+BEZIER)
CASE C14   FAIL stdout is not JSON (REBEZ+COMMENT)
CASE C15   FAIL stdout is not JSON (SOURCED+UNSOURCED+VARIABLE)
CASE C16   FAIL stdout is not JSON (BEZIER+COMMENT)
CASE C17   FAIL stdout is not JSON (INVALID+ROOT+SOURCED+CATEGORY)
CASE C18   FAIL stdout is not JSON (COMMENT+ORDER+ROOT)
CASE C19   FAIL stdout is not JSON (REBEZ+VARIABLE+ROOT)
CASE C20   FAIL stdout is not JSON (BEZIER+VARIABLE+ROOT+COMMENT)
CASE C21   FAIL stdout is not JSON (ORDER+INVALID+VARIABLE)
CASE C22   FAIL stdout is not JSON (INVALID+NEWSRC)
CASE C23   FAIL stdout is not JSON (NEWSRC+DISABLE)
CASE C24   FAIL stdout is not JSON (REBEZ+INVALID)
CASE C25   FAIL stdout is not JSON (NEWSRC+SOURCED+VARIABLE+BEZIER)
CASE C26   FAIL stdout is not JSON (COMMENT+BEZIER)
CASE C27   FAIL stdout is not JSON (COMMENT+NEWSRC+INVALID+ORDER)
CASE C28   FAIL stdout is not JSON (ROOT+REBEZ+VARIABLE)
CASE C29   FAIL stdout is not JSON (ORDER+SOURCED+BEZIER)
CASE C30   FAIL stdout is not JSON (ROOT+COMMENT+UNSOURCED+VARIABLE)
CASE C31   FAIL stdout is not JSON (INVALID+ORDER)
CASE C32   FAIL stdout is not JSON (SPACING+COMMENT+INVALID+SOURCED)
CASE C33   FAIL stdout is not JSON (INVALID+DISABLE)
CASE C34   FAIL stdout is not JSON (COMMENT+REBEZ+DISABLE)
CASE C35   FAIL stdout is not JSON (INVALID+ORDER+REBEZ)
CASE C36   FAIL stdout is not JSON (VARIABLE+NEWSRC)
CASE C37   FAIL stdout is not JSON (BEZIER+REBEZ+COMMENT)
CASE C38   FAIL stdout is not JSON (CATEGORY+INVALID+NEWSRC+DISABLE)
CASE C39   FAIL stdout is not JSON (DISABLE+BEZIER+ORDER+REBEZ)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

### Shape B, run 1 of 2 — 0-byte tool file (no outer prlimit)

```
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/fast/scratch/hyaku/mado-r26/K1DoNothing-empty.py sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
seed=e3a878c187f90792
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL stdout is not JSON (unperturbed)
CASE C00   FAIL stdout is not JSON (REBEZ+ROOT+VARIABLE+CATEGORY)
CASE C01   FAIL stdout is not JSON (ORDER+UNSOURCED)
CASE C02   FAIL stdout is not JSON (BEZIER+UNSOURCED+ROOT+CATEGORY)
CASE C03   FAIL stdout is not JSON (CATEGORY+INVALID)
CASE C04   FAIL stdout is not JSON (SOURCED+BEZIER+CATEGORY+REBEZ)
CASE C05   FAIL stdout is not JSON (BEZIER+UNSOURCED+ROOT)
CASE C06   FAIL stdout is not JSON (UNSOURCED+SOURCED)
CASE C07   FAIL stdout is not JSON (NEWSRC+ROOT+SOURCED+COMMENT)
CASE C08   FAIL stdout is not JSON (INVALID+COMMENT+BEZIER)
CASE C09   FAIL stdout is not JSON (REBEZ+SPACING+DISABLE+NEWSRC)
CASE C10   FAIL stdout is not JSON (ROOT+COMMENT+VARIABLE)
CASE C11   FAIL stdout is not JSON (REBEZ+VARIABLE)
CASE C12   FAIL stdout is not JSON (VARIABLE+INVALID+NEWSRC+UNSOURCED)
CASE C13   FAIL stdout is not JSON (ORDER+COMMENT+NEWSRC+REBEZ)
CASE C14   FAIL stdout is not JSON (INVALID+DISABLE)
CASE C15   FAIL stdout is not JSON (DISABLE+COMMENT+VARIABLE)
CASE C16   FAIL stdout is not JSON (ROOT+SOURCED+DISABLE)
CASE C17   FAIL stdout is not JSON (ROOT+NEWSRC)
CASE C18   FAIL stdout is not JSON (COMMENT+SOURCED+CATEGORY+DISABLE)
CASE C19   FAIL stdout is not JSON (ORDER+CATEGORY+VARIABLE+BEZIER)
CASE C20   FAIL stdout is not JSON (SPACING+UNSOURCED+REBEZ+INVALID)
CASE C21   FAIL stdout is not JSON (ORDER+VARIABLE)
CASE C22   FAIL stdout is not JSON (DISABLE+COMMENT+SPACING+BEZIER)
CASE C23   FAIL stdout is not JSON (REBEZ+INVALID+SPACING)
CASE C24   FAIL stdout is not JSON (INVALID+REBEZ+VARIABLE+COMMENT)
CASE C25   FAIL stdout is not JSON (ORDER+DISABLE)
CASE C26   FAIL stdout is not JSON (ROOT+UNSOURCED+BEZIER+INVALID)
CASE C27   FAIL stdout is not JSON (REBEZ+COMMENT+INVALID)
CASE C28   FAIL stdout is not JSON (NEWSRC+REBEZ+CATEGORY+BEZIER)
CASE C29   FAIL stdout is not JSON (INVALID+BEZIER+UNSOURCED)
CASE C30   FAIL stdout is not JSON (BEZIER+INVALID+COMMENT)
CASE C31   FAIL stdout is not JSON (INVALID+ROOT+DISABLE)
CASE C32   FAIL stdout is not JSON (UNSOURCED+SOURCED+COMMENT)
CASE C33   FAIL stdout is not JSON (INVALID+CATEGORY+UNSOURCED)
CASE C34   FAIL stdout is not JSON (BEZIER+VARIABLE+ORDER)
CASE C35   FAIL stdout is not JSON (VARIABLE+DISABLE+INVALID)
CASE C36   FAIL stdout is not JSON (COMMENT+ORDER+CATEGORY+ROOT)
CASE C37   FAIL stdout is not JSON (REBEZ+INVALID+VARIABLE+BEZIER)
CASE C38   FAIL stdout is not JSON (ORDER+DISABLE+SPACING+COMMENT)
CASE C39   FAIL stdout is not JSON (ORDER+VARIABLE)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

### Shape B, run 2 of 2 — 0-byte tool file (prlimit soft:hard 4G:8G)

```
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/fast/scratch/hyaku/mado-r26/K1DoNothing-empty.py sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
seed=24536a85388d87b1
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL stdout is not JSON (unperturbed)
CASE C00   FAIL stdout is not JSON (REBEZ+VARIABLE)
CASE C01   FAIL stdout is not JSON (DISABLE+ORDER+INVALID+BEZIER)
CASE C02   FAIL stdout is not JSON (COMMENT+SPACING+BEZIER+INVALID)
CASE C03   FAIL stdout is not JSON (ROOT+CATEGORY+INVALID+COMMENT)
CASE C04   FAIL stdout is not JSON (COMMENT+BEZIER+SPACING+CATEGORY)
CASE C05   FAIL stdout is not JSON (ORDER+REBEZ+UNSOURCED)
CASE C06   FAIL stdout is not JSON (UNSOURCED+BEZIER)
CASE C07   FAIL stdout is not JSON (CATEGORY+BEZIER+SPACING)
CASE C08   FAIL stdout is not JSON (ORDER+REBEZ+NEWSRC+ROOT)
CASE C09   FAIL stdout is not JSON (UNSOURCED+CATEGORY+VARIABLE)
CASE C10   FAIL stdout is not JSON (VARIABLE+REBEZ)
CASE C11   FAIL stdout is not JSON (CATEGORY+BEZIER)
CASE C12   FAIL stdout is not JSON (SPACING+ROOT+UNSOURCED+ORDER)
CASE C13   FAIL stdout is not JSON (DISABLE+INVALID+COMMENT)
CASE C14   FAIL stdout is not JSON (COMMENT+ROOT)
CASE C15   FAIL stdout is not JSON (COMMENT+NEWSRC+ROOT)
CASE C16   FAIL stdout is not JSON (UNSOURCED+INVALID+VARIABLE+NEWSRC)
CASE C17   FAIL stdout is not JSON (DISABLE+UNSOURCED)
CASE C18   FAIL stdout is not JSON (VARIABLE+UNSOURCED+SOURCED+ROOT)
CASE C19   FAIL stdout is not JSON (INVALID+CATEGORY+SOURCED+REBEZ)
CASE C20   FAIL stdout is not JSON (COMMENT+ORDER)
CASE C21   FAIL stdout is not JSON (BEZIER+CATEGORY+NEWSRC)
CASE C22   FAIL stdout is not JSON (UNSOURCED+ORDER)
CASE C23   FAIL stdout is not JSON (DISABLE+BEZIER+NEWSRC+REBEZ)
CASE C24   FAIL stdout is not JSON (SOURCED+SPACING+REBEZ)
CASE C25   FAIL stdout is not JSON (UNSOURCED+SOURCED+ROOT+BEZIER)
CASE C26   FAIL stdout is not JSON (UNSOURCED+NEWSRC)
CASE C27   FAIL stdout is not JSON (NEWSRC+ORDER+REBEZ)
CASE C28   FAIL stdout is not JSON (NEWSRC+CATEGORY)
CASE C29   FAIL stdout is not JSON (SPACING+BEZIER+CATEGORY+UNSOURCED)
CASE C30   FAIL stdout is not JSON (INVALID+UNSOURCED+NEWSRC+SPACING)
CASE C31   FAIL stdout is not JSON (UNSOURCED+COMMENT+DISABLE+BEZIER)
CASE C32   FAIL stdout is not JSON (BEZIER+SOURCED)
CASE C33   FAIL stdout is not JSON (SPACING+UNSOURCED)
CASE C34   FAIL stdout is not JSON (BEZIER+SPACING+COMMENT+ROOT)
CASE C35   FAIL stdout is not JSON (NEWSRC+COMMENT+CATEGORY+DISABLE)
CASE C36   FAIL stdout is not JSON (SPACING+REBEZ)
CASE C37   FAIL stdout is not JSON (COMMENT+ROOT+UNSOURCED)
CASE C38   FAIL stdout is not JSON (REBEZ+DISABLE+NEWSRC)
CASE C39   FAIL stdout is not JSON (SPACING+UNSOURCED)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

### Absent-tool baseline, REV 96101be5, no `--tool-file` (quoted)

```
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=96101be523b2f6e897eee743d5b396b0225bf9ed oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=MISSING_TOOL at 96101be523b2f6e897eee743d5b396b0225bf9ed
seed=8c17262e1dd584ba
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL tool absent (unperturbed)
CASE C00   FAIL tool absent (DISABLE+CATEGORY)
CASE C01   FAIL tool absent (DISABLE+ORDER+ROOT+CATEGORY)
CASE C02   FAIL tool absent (UNSOURCED+BEZIER+SOURCED)
CASE C03   FAIL tool absent (NEWSRC+REBEZ+ROOT+BEZIER)
CASE C04   FAIL tool absent (VARIABLE+NEWSRC+UNSOURCED)
CASE C05   FAIL tool absent (NEWSRC+COMMENT)
CASE C06   FAIL tool absent (UNSOURCED+NEWSRC+SPACING+REBEZ)
CASE C07   FAIL tool absent (UNSOURCED+COMMENT+CATEGORY)
CASE C08   FAIL tool absent (INVALID+BEZIER)
CASE C09   FAIL tool absent (BEZIER+DISABLE+SOURCED+SPACING)
CASE C10   FAIL tool absent (ORDER+ROOT+SOURCED+CATEGORY)
CASE C11   FAIL tool absent (VARIABLE+ORDER+COMMENT+SOURCED)
CASE C12   FAIL tool absent (ROOT+SOURCED)
CASE C13   FAIL tool absent (INVALID+REBEZ+CATEGORY+VARIABLE)
CASE C14   FAIL tool absent (INVALID+SPACING+ROOT+VARIABLE)
CASE C15   FAIL tool absent (SOURCED+VARIABLE+INVALID+BEZIER)
CASE C16   FAIL tool absent (SPACING+DISABLE+ORDER+REBEZ)
CASE C17   FAIL tool absent (NEWSRC+REBEZ+SOURCED+ORDER)
CASE C18   FAIL tool absent (ORDER+SPACING)
CASE C19   FAIL tool absent (BEZIER+INVALID+DISABLE+UNSOURCED)
CASE C20   FAIL tool absent (CATEGORY+ROOT+VARIABLE)
CASE C21   FAIL tool absent (SPACING+COMMENT)
CASE C22   FAIL tool absent (DISABLE+SOURCED+ORDER)
CASE C23   FAIL tool absent (BEZIER+SOURCED)
CASE C24   FAIL tool absent (COMMENT+CATEGORY+SOURCED+UNSOURCED)
CASE C25   FAIL tool absent (INVALID+ROOT)
CASE C26   FAIL tool absent (DISABLE+COMMENT)
CASE C27   FAIL tool absent (NEWSRC+REBEZ+UNSOURCED)
CASE C28   FAIL tool absent (SPACING+SOURCED+COMMENT+REBEZ)
CASE C29   FAIL tool absent (NEWSRC+VARIABLE+INVALID+COMMENT)
CASE C30   FAIL tool absent (NEWSRC+COMMENT+VARIABLE+CATEGORY)
CASE C31   FAIL tool absent (INVALID+ORDER)
CASE C32   FAIL tool absent (ROOT+COMMENT)
CASE C33   FAIL tool absent (BEZIER+UNSOURCED+REBEZ+NEWSRC)
CASE C34   FAIL tool absent (REBEZ+SPACING)
CASE C35   FAIL tool absent (COMMENT+ORDER+SOURCED+BEZIER)
CASE C36   FAIL tool absent (ROOT+BEZIER)
CASE C37   FAIL tool absent (DISABLE+REBEZ+ORDER)
CASE C38   FAIL tool absent (SOURCED+SPACING+DISABLE)
CASE C39   FAIL tool absent (DISABLE+VARIABLE)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

### Exit-2 attempt (reported, then re-run once)

The first attempt at shape A run 2 was wrapped in `prlimit --as=4000000000` (4 GB **hard**). The oracle's inner
`prlimit --as=8000000000` could then not be raised, the sandbox exited rc=1, and the counter guarded:

```
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1DoNothing.py sha256:a3e814b76c2154e086e272b57abc3f4d9726f127b0ee6db8f5286b19c3e48a94
seed=a04a807aa268f2cf
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
SETUP_ERROR ORACLE_FAIL BASE: sandbox exited rc=1 before answering
exit=2
```

That 581-byte log was written under the same path as the re-run and was overwritten; the block above is
reproduced from the two tool outputs that displayed the whole file (a `grep` of line 5 and a `tail` of all six
lines). The re-run with soft:hard 4G:8G is receipt A2. This guard run measured nothing and is not counted.

## Reading

- The counter never reaches a table comparison for this shape: `oracle.py` `run_tool` returns
  `(None, "stdout is not JSON")` before `well_formed()` is consulted, and with the tool absent the counter
  short-circuits to `tool absent` without invoking the tool at all. So the do-nothing control proves only what
  a negative control should: absence of work earns no case, and the counter's 41 cases cannot be passed by
  printing nothing, exiting 0, or omitting the tool file.
- Cost is real: the oracle still builds and runs 42 nested instances (BASE + 40 cases + BASE#2) for a shape
  that never reads config, and wall time was 18–29 s per run (47 s for the baseline under concurrent peer
  load). A control wave of this shape is not free, but it is cheap relative to a data run.
- `HOST_SAFETY` delta was 0 in all five runs (coredumps 1335 → 1335), consistent with the registration's pilot
  count. Immediately after my last run `pgrep -af 'm26c1-|tinywl|count.py 05319e0f|K1DoNothing'` matched
  nothing; at hand-off `pgrep -af K1DoNothing` matched nothing and no live counter process referenced my item.
  The one backgrounded batch I started was killed before its remaining runs; its leftover counter temp dir
  `/fast/scratch/hyaku/mado-r26/m26c1-x66wqyyr` (174 MB, identified by the 0-byte tool copy that is my shape-B
  run) was removed, and the other leftover `m26c1-*` dir there (1750-byte tool copy, a peer's run) was left
  untouched.

## Risks and limits

- Shape B's 0-byte file lives in `/fast/scratch/hyaku/mado-r26/`, not in the lane: the control contract allows
  one control program at `controls/<ItemName>.py`, and the empty file is a scored variant, not a second
  program. Its sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` is the empty-file digest,
  so the variant is reproducible from the receipt alone.
- The two shapes are not distinguishable by this counter (identical `stdout is not JSON` reason on all 41 cases,
  identical 0/41). Any claim that the counter separates "empty file" from "exits 0 silently" would need a
  different probe; this wave measured neither difference.
- I found no defect in the counter or the harness and did not edit either. One operational hazard for the
  remaining control seats: an outer `prlimit --as` below the oracle's inner 8 GB turns every run into
  `SETUP_ERROR ORACLE_FAIL … exit=2`; soft:hard 4G:8G or no wrapper is required.
- Tooling: no installs or upgrades were made.
