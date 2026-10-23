# K1EmptyTable — C1 control, shape ALL-EMPTY

Date: 2026-10-23
Seat: `MadoR26.K1EmptyTable` (leaf executor, round-26 wave w1)
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, REV `05319e0f` (`05319e0fed2ce25cf0a883380af2763a85fd4936`)

## Verdict

CONTROL K1EmptyTable best: cases_pass=0/41 [embed_hits=n/a] verdict=TARGET_MISSED — not met

## What I built (two forms of the same shape, strongest first)

The shape claims no work: an empty table, or a table of names whose every value is the zero value.

| file | stdout | sha256 |
|---|---|---|
| `.ufo/waves/round-26/controls/K1EmptyTable.py` | exactly `[[],[]]` (verified with `od -c`: `[ [ ] , [ ] ] \n`) | `1dd7006992e8d5d0d3a98832c408fb28d1590d5440f7a8af2033caa41009d4b5` |
| `.ufo/waves/round-26/controls/K1EmptyTableZeroNodes.py` | `[[35 zero-value node objects], []]` | `3ce6d3240c3d6c31e837859f7a8dfb49f8c569c0282c6f46373ceec1f22fa0ba` |

Both are single stdlib files with the tool CLI (`--home DIR`); neither opens any file under DIR (no
`open`/`os.walk` at all) and neither reads the environment.

Variant B is the strongest form the shape allows: the 35 node names of Hyprland v0.56.2's animation
tree, each with `overridden false, bezier "", enabled true, speed 0.0, style ""`, and an empty bezier
list. `speed` is the float `0.0` because Hyprland prints `%.2f` and the counter compares
`json.dumps` of the parsed values (`0` would compare unequal to `0.0`).

Name origin (one oracle call, through the harness only; full output in the receipt's NAME ORIGIN
section): `/fast/scratch/hyaku/mado-r26/k1names/probe.py` imported `harness/oracle.py` by path, took
`snapshot(~)` (`files=79 digest sha256:fe1b2d8b…3727`, the same digest the counter prints) and called
`oracle(snap, work, ["animations"])`. Result `nodes=35 beziers=6`, coredumps `1335 → 1335 delta=0`.
The 35 names are the counter's own 34 `NODES` plus `__internal_fadeCTM` (checked: set difference is
exactly that one name; `NODES` is the generator's list, not the full tree). The base table's *values*
were deliberately not copied into the control — only the constant names are in it; this report quotes
five of those values below, as illustration only.

## Receipts

All four runs are verbatim (stdout including `exit=`) in
`.ufo/waves/round-26/controls/K1EmptyTable.txt` (20722 bytes): variant A runs at lines 9–58 and
59–108, variant B runs at 109–158 and 159–208, name origin at 209–218. Fresh random seed each run
(the counter draws `os.urandom(8)`; no `--seed` passed).

| variant | run | seed | tool sha256 (as printed) | cases_pass | exit |
|---|---|---|---|---|---|
| A `[[],[]]` | A1 | `277e8ce0ca3164ff` | `1dd70069…09d4b5` | 0/41 | 1 |
| A `[[],[]]` | A2 | `5d4edaad506f2f00` | `1dd70069…09d4b5` | 0/41 | 1 |
| B zero nodes | B1 | `bae5a7b067cb94f2` | `3ce6d324…2fa0ba` | 0/41 | 1 |
| B zero nodes | B2 | `a4be987c5b85bd4b` | `3ce6d324…2fa0ba` | 0/41 | 1 |

Every run printed the same guard lines and verdict:

```text
ORACLE_CHECK base_twice equal nodes=35 beziers=6
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

No exit-2 run occurred, so nothing needed re-running for a guard. Both tool shas in the receipts
equal the current file bytes, so the receipts are reproducible against the final controls.

Per-case shape of the misses (all 41 cases of each run, from the receipts):

- A: `nodes missing=35 extra=0` in every case; `beziers missing=6..8 extra=0`.
- B: `nodes missing=19..23 extra=19..23`; `beziers missing=6..8 extra=0`.

## What this measures

1. The all-empty/all-zero shape cannot reach the target, and not marginally: the expected bezier set
   is never empty. The base tree carries 6 beziers (`quick, almostLinear, easeInOutCubic,
   easeOutQuint, linear, default`), and `BEZIER`/`CATEGORY`/`REBEZ` cases raise the count to 7–8. A
   shape that prints `[]` for beziers is missing 6–8 entries in every one of the 41 cases (the
   receipts show `beziers missing=6..8 extra=0` on every line), no matter what it does with nodes.
2. Variant B is exactly right about names: `missing == extra` in all 41 cases, including the
   `INVALID` cases that write unknown node names, means the expected node-name set equals the
   35-name set in every case (if Hyprland added an unknown name, `missing` would exceed `extra` by
   one). So the 35-name constant is not the gap.
3. Variant B is also exactly right about 16 of the 35 base nodes: BASE shows `nodes missing=19
   extra=19`, i.e. the 16 zero-valued nodes match exactly in the six compared fields. The base
   config tree overrides 19 nodes (`global 10 default`, `windows 3.79 easeOutQuint`,
   `layersIn 4 easeOutQuint fade`, `windowsIn 4.1 easeOutQuint "popin 87%"`, …; cases add 0–4 more),
   so the residual gap is 19–23 nonzero node tuples plus the 6–8 beziers.
4. Consequence for the claim: the C1 target needs a real reader (source graph, variables, comment
   handling, validation, and the built-in bezier set). No form of the ALL-EMPTY shape comes close,
   and there is no way to shrink the gap inside the shape — the missing information is exactly the
   config-derived values and the bezier list. This control does not trigger a redesign; it confirms
   the counter requires the operation C1 claims.

## Exact commands

Run from `/home/vgpnk/Projects/shokunin/mado-shokunin` (no outer `prlimit --as` — the oracle sets its
own 8 GB; per the L1 note nothing was wrapped below that):

```sh
timeout 900 python3 -I .ufo/waves/round-26/c1/count.py 05319e0f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1EmptyTable.py
timeout 900 python3 -I .ufo/waves/round-26/c1/count.py 05319e0f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1EmptyTableZeroNodes.py
```

Each command was run twice (fresh seed); the four runs are the receipt above. Name origin:

```sh
cd /fast/scratch/hyaku/mado-r26/k1names && timeout 120 python3 -I probe.py
```

Verification of variant A's literal stdout and the control shas:

```sh
python3 -I .ufo/waves/round-26/controls/K1EmptyTable.py --home /tmp | od -c
sha256sum .ufo/waves/round-26/controls/K1EmptyTable.py .ufo/waves/round-26/controls/K1EmptyTableZeroNodes.py
```

Observed: `0000000   [   [   ]   ,   [   ]   ]  \n`; shas as in the table above.

## Risks and limits

- **Receipt extension.** The control contract names `.ufo/waves/round-26/controls/<Item>.txt`, so the
  receipts are `.txt`. Round-25's `check-control-receipts.py` defines a control receipt as a `.md`
  under `controls/` containing a line starting with `CONTROL `. If round-26 keeps that checker, the
  L1 must place or point a `.md` (this report's first verdict line is such a line). I did not create
  a second file outside my named outputs; flagged rather than worked around.
- **No lane bytes touched.** `c1/count.py` and `harness/oracle.py` shas were re-verified against the
  registration pins before running (`f98e264b…52cd`, `680798ed…e441`); neither was edited, and no
  git/jj write command was run. The only lane files written by this seat are the two controls, the
  receipt `.txt`, and this report.
- **Oracle use.** 1 probe + 4 counter runs; the counters used the harness slot locks (jobs=4 each,
  run sequentially). Every run reported `hyprland_coredumps_before=1335 after=1335 delta=0`; the
  probe reported the same. No live-compositor verb was used; no Hyprland was started outside
  `harness/oracle.py`.
- **Variant B's names are constants, not a cached table.** They cannot become stale for this pin
  (`__internal_fadeCTM` and the 34 configured nodes are created by ConfigManager unconditionally);
  if a future pin renames a node, the control would have to be rebuilt, which is the point of a
  control, not a risk to the claim.
- **No tool installs or upgrades** were needed or made.
- **No blockers.** Both variants were scored to completion with fresh seeds; the measurement is
  valid (ORACLE_CHECK passed, no guard fired).
