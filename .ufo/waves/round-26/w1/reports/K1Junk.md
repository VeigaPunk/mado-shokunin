# K1Junk — randomized C1 control

## Verdict
CONTROL K1Junk best: cases_pass=0/41 verdict=TARGET_MISSED — not met

Both fresh-seed runs completed with `exit=1`; neither was a setup-error/inconclusive run. The frozen detector rejected the junk replacement on all 82 scored cases. This is a registered control, not a claim of killing a source mutant with a pristine/restored baseline.

## Shape and expected detector

- Axes: complete output shape, configuration independence, full-counter discrimination, host safety, and exact receipts.
- Wrote only the assigned program, receipt and report paths. The single Python stdlib program accepts `--home DIR` but never opens or examines the directory or any config.
- Each invocation seeds `random.Random` from 32 bytes of `os.urandom`. It emits random-length node (0–64) and bezier (0–24) arrays with every named field, random names/values, JSON booleans and finite numeric values. Node bezier names refer to generated beziers when available.
- Expected detector: frozen C1 compares exact sets of `(name, overridden, bezier, enabled, speed, style)` and `(name, X0, Y0, X1, Y1)`, ignoring order. Random shape alone should not match Hyprland's complete tables.
- Observed: both runs reached set comparison for all cases (missing/extra diagnostics rather than malformed-output errors); every case missed all 35 expected nodes.

## Exact scoring invocation

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

The following command ran twice concurrently, with the display variables also removed from the subprocess environment and no `--seed` argument:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000: python3 -I .ufo/waves/round-26/c1/count.py 05319e0f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1Junk.py
```

The outer AS limit was soft 4 GB with the inherited hard limit unchanged (`--as=4000000000:`), not a hard cap below 8 GB. This allowed the pinned oracle's own 8 GB limit. Each counter used its default four workers and the shared oracle slot locks. The 900-second timeout did not fire. Both subprocess stderr streams were empty.

| Run | Counter seed | Result | Process exit |
| --- | --- | --- | --- |
| 1 | `48451b7b407fd7b1` | `0/41 TARGET_MISSED` | 1 |
| 2 | `b2390bf85246e7d4` | `0/41 TARGET_MISSED` | 1 |

Both receipts report equal double-baseline oracle tables (35 nodes, 6 beziers), the same 79-file snapshot digest, and `HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0`.

## Restoration and safety evidence

No counter, harness, production tool, or sibling file was edited; no restoration was necessary. The assigned control remains for the registered receipt. SHA-256 before and after scoring was identical for each file below:

| File | Before = after SHA-256 |
| --- | --- |
| `.ufo/waves/round-26/controls/K1Junk.py` | `4919d9798ed37c3280545cd30cc5ead62714b0b094eee22fa3eb247c8e422ad3` |
| `.ufo/waves/round-26/c1/count.py` | `f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd` |
| `.ufo/waves/round-26/c2/count.py` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` |
| `.ufo/waves/round-26/harness/oracle.py` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` |

Both counter processes exited. The oracle's normal cleanup path owns its sandbox process groups. A bounded process listing after both runs found zero command lines containing the assigned control path:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 15 prlimit --as=4000000000 ps -eo pid=,ppid=,args=
```

Process-list command exit: 0. Matching command lines: `[]`. No compositor was started except by the frozen oracle. No live-compositor command was issued. No git/jj write command was run. `/fast` had 186 GB available before scoring. No tools were installed or updated.

Receipt file: `.ufo/waves/round-26/controls/K1Junk.txt` (the two stdout streams concatenated verbatim, including each `exit=1` line). Only the two explicitly assigned full C1 scoring runs were exercised; no extra build, lint or smoke run was performed.

## Verbatim receipt — run 1

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1Junk.py sha256:4919d9798ed37c3280545cd30cc5ead62714b0b094eee22fa3eb247c8e422ad3
seed=48451b7b407fd7b1
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL nodes missing=35 extra=20 beziers missing=6 extra=9 (unperturbed)
CASE C00   FAIL nodes missing=35 extra=6 beziers missing=6 extra=11 (NEWSRC+ORDER)
CASE C01   FAIL nodes missing=35 extra=52 beziers missing=7 extra=6 (VARIABLE+DISABLE+ORDER+CATEGORY)
CASE C02   FAIL nodes missing=35 extra=15 beziers missing=6 extra=20 (ORDER+SOURCED)
CASE C03   FAIL nodes missing=35 extra=30 beziers missing=6 extra=8 (INVALID+REBEZ+ROOT)
CASE C04   FAIL nodes missing=35 extra=6 beziers missing=7 extra=7 (BEZIER+UNSOURCED+COMMENT+VARIABLE)
CASE C05   FAIL nodes missing=35 extra=61 beziers missing=6 extra=16 (SOURCED+INVALID+NEWSRC)
CASE C06   FAIL nodes missing=35 extra=50 beziers missing=6 extra=20 (DISABLE+ORDER+NEWSRC+VARIABLE)
CASE C07   FAIL nodes missing=35 extra=51 beziers missing=6 extra=3 (SPACING+INVALID+DISABLE+SOURCED)
CASE C08   FAIL nodes missing=35 extra=8 beziers missing=6 extra=0 (SPACING+UNSOURCED+ORDER)
CASE C09   FAIL nodes missing=35 extra=7 beziers missing=6 extra=14 (COMMENT+NEWSRC+DISABLE)
CASE C10   FAIL nodes missing=35 extra=55 beziers missing=6 extra=11 (SPACING+DISABLE+NEWSRC)
CASE C11   FAIL nodes missing=35 extra=1 beziers missing=6 extra=6 (SOURCED+DISABLE)
CASE C12   FAIL nodes missing=35 extra=10 beziers missing=6 extra=11 (VARIABLE+REBEZ+UNSOURCED+INVALID)
CASE C13   FAIL nodes missing=35 extra=4 beziers missing=6 extra=11 (SOURCED+VARIABLE+REBEZ)
CASE C14   FAIL nodes missing=35 extra=24 beziers missing=7 extra=13 (SPACING+CATEGORY+ORDER)
CASE C15   FAIL nodes missing=35 extra=32 beziers missing=7 extra=7 (CATEGORY+DISABLE+SOURCED)
CASE C16   FAIL nodes missing=35 extra=51 beziers missing=6 extra=20 (SOURCED+SPACING)
CASE C17   FAIL nodes missing=35 extra=60 beziers missing=6 extra=2 (DISABLE+NEWSRC+REBEZ+VARIABLE)
CASE C18   FAIL nodes missing=35 extra=1 beziers missing=6 extra=2 (COMMENT+NEWSRC)
CASE C19   FAIL nodes missing=35 extra=23 beziers missing=7 extra=18 (DISABLE+CATEGORY)
CASE C20   FAIL nodes missing=35 extra=51 beziers missing=6 extra=13 (SPACING+INVALID)
CASE C21   FAIL nodes missing=35 extra=3 beziers missing=7 extra=21 (SPACING+BEZIER)
CASE C22   FAIL nodes missing=35 extra=63 beziers missing=7 extra=9 (CATEGORY+COMMENT)
CASE C23   FAIL nodes missing=35 extra=7 beziers missing=6 extra=13 (VARIABLE+COMMENT+SPACING)
CASE C24   FAIL nodes missing=35 extra=55 beziers missing=6 extra=9 (REBEZ+SOURCED)
CASE C25   FAIL nodes missing=35 extra=62 beziers missing=6 extra=24 (UNSOURCED+ORDER)
CASE C26   FAIL nodes missing=35 extra=63 beziers missing=6 extra=3 (REBEZ+VARIABLE+INVALID)
CASE C27   FAIL nodes missing=35 extra=4 beziers missing=7 extra=0 (SOURCED+BEZIER+ROOT+COMMENT)
CASE C28   FAIL nodes missing=35 extra=29 beziers missing=6 extra=16 (ORDER+VARIABLE+NEWSRC)
CASE C29   FAIL nodes missing=35 extra=45 beziers missing=7 extra=18 (REBEZ+ROOT+SPACING+CATEGORY)
CASE C30   FAIL nodes missing=35 extra=39 beziers missing=7 extra=4 (BEZIER+ROOT+NEWSRC)
CASE C31   FAIL nodes missing=35 extra=4 beziers missing=6 extra=19 (SPACING+NEWSRC+INVALID+DISABLE)
CASE C32   FAIL nodes missing=35 extra=14 beziers missing=7 extra=13 (BEZIER+NEWSRC+DISABLE+SPACING)
CASE C33   FAIL nodes missing=35 extra=37 beziers missing=6 extra=17 (ROOT+REBEZ+COMMENT)
CASE C34   FAIL nodes missing=35 extra=36 beziers missing=6 extra=8 (SPACING+INVALID)
CASE C35   FAIL nodes missing=35 extra=58 beziers missing=7 extra=17 (INVALID+CATEGORY+COMMENT)
CASE C36   FAIL nodes missing=35 extra=58 beziers missing=6 extra=24 (INVALID+REBEZ)
CASE C37   FAIL nodes missing=35 extra=37 beziers missing=7 extra=20 (COMMENT+ORDER+BEZIER)
CASE C38   FAIL nodes missing=35 extra=23 beziers missing=6 extra=23 (UNSOURCED+DISABLE)
CASE C39   FAIL nodes missing=35 extra=59 beziers missing=7 extra=18 (REBEZ+BEZIER+SOURCED)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

## Verbatim receipt — run 2

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1Junk.py sha256:4919d9798ed37c3280545cd30cc5ead62714b0b094eee22fa3eb247c8e422ad3
seed=b2390bf85246e7d4
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL nodes missing=35 extra=0 beziers missing=6 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=35 extra=49 beziers missing=7 extra=6 (COMMENT+CATEGORY+ROOT+REBEZ)
CASE C01   FAIL nodes missing=35 extra=49 beziers missing=7 extra=8 (VARIABLE+ROOT+NEWSRC+BEZIER)
CASE C02   FAIL nodes missing=35 extra=56 beziers missing=6 extra=22 (SPACING+INVALID+VARIABLE+ORDER)
CASE C03   FAIL nodes missing=35 extra=39 beziers missing=6 extra=8 (NEWSRC+COMMENT)
CASE C04   FAIL nodes missing=35 extra=11 beziers missing=7 extra=0 (CATEGORY+UNSOURCED+ORDER+NEWSRC)
CASE C05   FAIL nodes missing=35 extra=44 beziers missing=6 extra=12 (SOURCED+SPACING+ROOT+ORDER)
CASE C06   FAIL nodes missing=35 extra=47 beziers missing=7 extra=8 (CATEGORY+COMMENT)
CASE C07   FAIL nodes missing=35 extra=61 beziers missing=6 extra=15 (SPACING+DISABLE+SOURCED+INVALID)
CASE C08   FAIL nodes missing=35 extra=12 beziers missing=6 extra=8 (SPACING+SOURCED)
CASE C09   FAIL nodes missing=35 extra=24 beziers missing=6 extra=4 (COMMENT+ROOT+UNSOURCED+INVALID)
CASE C10   FAIL nodes missing=35 extra=6 beziers missing=7 extra=12 (REBEZ+BEZIER)
CASE C11   FAIL nodes missing=35 extra=45 beziers missing=6 extra=1 (REBEZ+ORDER)
CASE C12   FAIL nodes missing=35 extra=31 beziers missing=6 extra=4 (DISABLE+ROOT+VARIABLE)
CASE C13   FAIL nodes missing=35 extra=48 beziers missing=7 extra=11 (DISABLE+BEZIER+UNSOURCED)
CASE C14   FAIL nodes missing=35 extra=11 beziers missing=6 extra=1 (UNSOURCED+SOURCED)
CASE C15   FAIL nodes missing=35 extra=15 beziers missing=7 extra=2 (SPACING+CATEGORY)
CASE C16   FAIL nodes missing=35 extra=47 beziers missing=6 extra=7 (COMMENT+UNSOURCED+DISABLE)
CASE C17   FAIL nodes missing=35 extra=55 beziers missing=6 extra=16 (VARIABLE+REBEZ+NEWSRC)
CASE C18   FAIL nodes missing=35 extra=17 beziers missing=6 extra=5 (UNSOURCED+ROOT+COMMENT)
CASE C19   FAIL nodes missing=35 extra=39 beziers missing=7 extra=15 (SPACING+CATEGORY+DISABLE+ORDER)
CASE C20   FAIL nodes missing=35 extra=12 beziers missing=6 extra=2 (DISABLE+SOURCED)
CASE C21   FAIL nodes missing=35 extra=36 beziers missing=6 extra=6 (NEWSRC+REBEZ+COMMENT+SOURCED)
CASE C22   FAIL nodes missing=35 extra=31 beziers missing=6 extra=19 (INVALID+ROOT+UNSOURCED)
CASE C23   FAIL nodes missing=35 extra=59 beziers missing=8 extra=7 (INVALID+BEZIER+CATEGORY)
CASE C24   FAIL nodes missing=35 extra=20 beziers missing=7 extra=6 (ROOT+BEZIER)
CASE C25   FAIL nodes missing=35 extra=28 beziers missing=6 extra=8 (REBEZ+ROOT)
CASE C26   FAIL nodes missing=35 extra=39 beziers missing=7 extra=20 (COMMENT+CATEGORY+DISABLE)
CASE C27   FAIL nodes missing=35 extra=10 beziers missing=7 extra=10 (VARIABLE+DISABLE+COMMENT+CATEGORY)
CASE C28   FAIL nodes missing=35 extra=7 beziers missing=6 extra=6 (NEWSRC+UNSOURCED+VARIABLE)
CASE C29   FAIL nodes missing=35 extra=34 beziers missing=7 extra=19 (COMMENT+UNSOURCED+DISABLE+BEZIER)
CASE C30   FAIL nodes missing=35 extra=16 beziers missing=6 extra=17 (VARIABLE+SOURCED+NEWSRC+ORDER)
CASE C31   FAIL nodes missing=35 extra=60 beziers missing=6 extra=15 (ROOT+NEWSRC)
CASE C32   FAIL nodes missing=35 extra=7 beziers missing=6 extra=6 (NEWSRC+INVALID)
CASE C33   FAIL nodes missing=35 extra=40 beziers missing=6 extra=16 (ORDER+DISABLE+SOURCED+COMMENT)
CASE C34   FAIL nodes missing=35 extra=2 beziers missing=7 extra=17 (UNSOURCED+BEZIER+INVALID)
CASE C35   FAIL nodes missing=35 extra=43 beziers missing=6 extra=7 (ORDER+SPACING+COMMENT)
CASE C36   FAIL nodes missing=35 extra=8 beziers missing=8 extra=1 (CATEGORY+BEZIER)
CASE C37   FAIL nodes missing=35 extra=21 beziers missing=6 extra=14 (ROOT+COMMENT)
CASE C38   FAIL nodes missing=35 extra=29 beziers missing=6 extra=24 (ROOT+INVALID)
CASE C39   FAIL nodes missing=35 extra=50 beziers missing=6 extra=10 (DISABLE+INVALID+UNSOURCED)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```
