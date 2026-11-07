# R98MExecGate -- w1 report: C2 SOURCES read-back gate + counter (round 98, v2 predicate)

Base 35f3ce808788b11c063309b1b5ad0192754795ea (master). Measured 2026-11-07
against the working tree (the 21-cell repair and the S030/S132 reverts sit
uncommitted in `corpus/SOURCES.md`; see Deviations). Implements the rewritten
PRED-C2-r98-v1: five finding rules (R1/R3/R4/R5/R6), status-aware R4
(`status == mined` only), pinned frontmatter scope (YAML list items, wrapped
continuation lines, no later `source:` block), standalone-token ids, normpath
used-by comparison, `--expect-base-mismatches 21`, and the row->entry repair
legs (entry-path set, per-entry citation supersets, added_paths == repaired).

## Files written (owned paths only)

- `build/check-sources-readback.py` -- the C2 gate draft. sha256
  `f1000bf11e88149695aa96229fcf2155929ebbb72a2cfa215d8c24e2f37bd8f5`
- `build/c2-r98-sources-readback.py` -- the C2 counter draft. sha256
  `e944fdacd1285a44e3026b0c8ccccf9dce5f6ec687ec047c2327e8cec61e6e0a`
- `selftest-fixtures/readback/` -- committed fixtures: mini-repos
  `clean/ r4/ r1/ r3/`, `shapes/{yaml,wrapped,pathtoken}/`,
  `basepair/{base,rev,rev-delete-cite,rev-reword,rev-shotgun,rev-no-beta}/`,
  `planted/` (byte products of the counter's own transforms) and `README.txt`.
- `controls/readback-planted/` -- the five real-scale planted products
  (r4/r1/r3/r6 registry copies + the r5 entry copy) plus the committed
  always-clean stub gate `stub-always-clean-gate.py` and `manifest.json`
  (schema v2, source_sha256
  `719a96d51b5733b431086541ced6ebbb7816bf5f6b3fdb1ac2892953c6129c33`,
  rev=worktree), all cut by `c2-r98-sources-readback.py --emit-planted`.
- `receipts/c2-readback-r98-measured.txt` -- exact measured output of both
  selftests, the gate on the committed registry, the full counter measurement
  (plain + `--json`), the `--rev HEAD` separability smoke, the 21-line
  base mismatch list, and the census validate tail.
- `w1/R98MExecGate.md` -- this report.

## Verdicts (all measured this session; exact lines in the receipt)

- gate `--selftest`: `SOURCES_READBACK_SELFTEST: checks=21 failed=0`, exit 0
  (stable ids st01..st21; covers the six rule behaviors incl. R2-as-note, the
  three parser shapes, status-awareness, normpath, and the no-later-block
  rule).
- gate `--repo <lane>`: `SOURCES_READBACK: rows=462 entries=118 findings=0`,
  exit 0. rows=462 equals `sources-census.sh census --file` rows=462; the 21
  outside-corpus used-by members are NOTE lines (below), never findings.
- counter `--selftest`: `MADO_COUNTER_SELFTEST: checks=18 failed=0`, exit 0
  (ct01..ct18; ct14-ct17 drive the real `repair_legs()` decision body over the
  four committed no-work shapes; ct11-ct13 run the gate on the committed
  parser-shape repos).
- counter measure (`--rev worktree --base-rev 35f3ce80 --expect-base-mismatches 21`):
  `MADO_SOURCES_READBACK_COUNT: TARGET_MET all-legs-green`, exit 0, with
  `base_gate=absent`; `base_mismatches=21 expect=21 match=ok`; `gate_pin=ok`;
  `rev_registry_sha256=719a96d5...`; `gate_selftest=ok checks=21 failed=0`;
  `gate_findings=0 rows=462 entries=118 gate_rc=0`; rows/entries match;
  `rev_mismatches=0`; `entry_set=ok`; `row_set=ok`; `citations_superset=ok`;
  `added_paths=21`; `added_paths_match=ok`; `repaired=21/21`;
  `planted_sync=ok` (committed copies byte-equal the counter's transforms of
  the measured bytes); `planted_r1=ok planted_r3=ok planted_r4=ok
  planted_r5=ok planted_r6=ok`; `planted=5/5`; `stub_flagged=1` (the
  committed always-clean stub, rejected through the planted-r4 runner);
  `census=ok` (validate exit 0, W-codes only).
- separability smoke `--rev HEAD` (the C2-at-C1-revision shape declared in the
  declaration): TARGET_MISSED with `gate_findings=21 rev_mismatches=21
  repaired=0/21 planted=0/5`, exit 1 -- correct, the base registry is
  unrepaired. Also exercised the git-archive extraction path.

## The 21 base mismatches (counter `BASE_MISMATCH` lines = frozen before-number)

S464, S470, S460 x bar-footprint-allocation-r82; S457, S459, S465, S466 x
bar-footprint-composition-r80; S460, S464, S470 x bar-footprint-rounding-auto-r81;
S481, S464, S470, S484, S485 x bar-footprint-surface-band-r83; S493 x
mako-fields-containment-r88; S501, S502 x portal-keyfile-bytes-r93; S511,
S512, S517 x mime-magic-sniff-r95. All `corpus/knowledge/*.md` entries, all
rows `status: mined`. Exactly the declared 21: the two further base pairs the
old status-blind count reported (S030 x hyprland-config-era-r12, S132 x
terminal-trees-r23) are disowned by their entries' own bytes (S030 rejected;
S132 queued) and the L1 reverted their used-by additions; under the frozen
status-aware R4 they do not count and `base_mismatches=21 expect=21 match=ok`.

## Planted controls (cut from the measured bytes; exact standalone gate output)

Each registry product differs from the measured registry by exactly one line;
the r5 product appends ` S999` to mako-fields' source line (diff-verified).

```
r4-stripped-usedby (S484 used-by cell emptied; S484 mined, cited only by surface-band)
  SOURCES_READBACK: FINDING R4 S484 entry=corpus/knowledge/bar-footprint-surface-band-r83.md
  SOURCES_READBACK: rows=462 entries=118 findings=1                      exit=1
r1-path-in-recheck (S511 recheck 180d -> corpus/knowledge/mime-magic-sniff-r95.md)
  SOURCES_READBACK: FINDING R1 S511 recheck=corpus/knowledge/mime-magic-sniff-r95.md
  SOURCES_READBACK: rows=462 entries=118 findings=1                      exit=1
r3-dangling-usedby (S132 used-by += corpus/knowledge/readback-planted-dangling-r98.md)
  SOURCES_READBACK: FINDING R3 S132 path=corpus/knowledge/readback-planted-dangling-r98.md
  SOURCES_READBACK: rows=462 entries=118 findings=1                      exit=1
r6-duplicate-row (S511 row duplicated)
  SOURCES_READBACK: FINDING R6 S511 count=2
  SOURCES_READBACK: rows=463 entries=118 findings=1                      exit=1
r5-phantom-id (mako-fields source line += S999)
  SOURCES_READBACK: FINDING R5 S999 entry=corpus/knowledge/mako-fields-containment-r88.md
  SOURCES_READBACK: rows=462 entries=118 findings=1                      exit=1
```

Each fires exactly one finding with the planted id, the expected detail, and
exit 1. S484 was chosen for R4 because it is mined and cited by exactly one
entry (the S030/S132 strip candidates died with the status-aware rule); S132
stays the R3 target because R3 is status-blind and the queued row fires no R4.
The committed always-clean stub gate is rejected by the same runner the real
gate passes (`stub_flagged=1`). The planted copies inherit the committed
registry's UTF-8 bytes by construction (byte-faithful defect copies of a
registry that contains em-dashes); every artifact I authored is ASCII.

## The R2 evidence (ruling retained; no finding)

The original draft R2 flagged 21 members on 19 rows, identical at base and
worktree -- all legitimate lane artifacts the census validates by existence
(E11): S096 `tools/mado-verify.sh` + `SKILL.md`; S173/S174
`tools/mado-binds.py`; S178-S182 `tools/mado-wsrules.py`; S184
`.ufo/waves/round-29/registration.md`; S185 `quality/check-index.py` +
`.ufo/waves/round-30/registration.md`; S332-S339
`.ufo/waves/round-47/w1/ExecSupersede/rows.md`; S482 `SKILL.md`. The gate
reports them as plain-mode NOTE lines only (`SOURCES_READBACK: NOTE
outside-corpus <id> path=<p>`; absent from --json, never counted), per the L1
ruling and the frozen declaration sentence "there is no R2".

## No-work shapes (critic's four; all score unrepaired through the shared body)

`repair_legs()` is the single decision body for measure and selftest. On the
committed fixtures: delete-citation -> citation supersets broken (ct14);
reword-to-acknowledged-row -> repaired < base pairs (ct15); shotgun ->
added_paths != repaired (ct16); delete-entry -> entry-path set changed
(ct17). The critic's measured shotgun scale (4095 added paths vs 21) is the
same leg at real scale.

## Structural classification (QUALITY 162/165)

- gate = the submitted candidate: stdlib only, no subprocess, no socket, no
  network, no ctypes, read-only over `--repo`.
- counter = harness/instrument (allowed): spawns `git`
  (GIT_NO_REPLACE_OBJECTS=1 on every call), the gate (`python3 -I`, including
  its `--selftest`), and `sources-census.sh` (bash). stdlib only, no network,
  no ctypes.
- fixtures/planted/report/receipt = data.

## Deviations and risks

- Measured at `--rev worktree` because the repair + reverts are uncommitted
  (`M corpus/SOURCES.md`). At integration the L1 re-runs the counter with
  `--rev <commit>` and `--expect-gate-sha256` = the frozen gate sha (drop
  `--gate` once landed at `quality/`); the extraction pin
  (`rev_tree_pin=git-show`) is exercised by the committed smoke only in its
  archive branch so far.
- If the registry changes, re-cut the planted copies with `--emit-planted`;
  the counter SETUP_ERRORs (`planted-drift`) on stale copies by design, and
  refuses `--base-rev == --rev` (SETUP_ERROR).
- `--expect-base-mismatches 21` is pinned per the frozen predicate; a base
  whose measured count differs scores TARGET_MISSED (`match=MISMATCH`).
- Earlier draft shas communicated to R98MMutC2 (b04742ef...) are superseded
  by `f1000bf1...` (gate) after the v2 rewrite; no other seat anchored to the
  counter sha.
- Tool installs: none (stdlib sufficed).

## Not done (out of my seat)

- No writes outside my owned paths: the corpus repair/reverts, `quality/`
  landing, SKILL registry row and commits belong to the L1.
