# ExecRows — shape verification of the eight new SOURCES.md rows

Subject: `.ufo/waves/round-35/controls/golden/corpus/SOURCES.md` lines 3–10 (rows S203–S210).
Checked against the frozen v1 contract in `/home/vgpnk/Projects/shokunin/CORPUS.md` §SOURCES.md
(enum: `spec docs paper code tool dataset talk book community own-work`; tier `A|B|C`; status
`queued|mined|rejected`; mined ⇒ used-by paths must exist).

## Verdict per check

| check | result |
|---|---|
| 11 cells (`awk -F'|' NF==13`) | PASS — all 8 rows NF=13, exactly 12 `|` chars each |
| valid `id` (`S` + ≥3 digits, unique) | PASS — S203–S210, no duplicates |
| `kind` in census enum | PASS — all `own-work` |
| `tier` in `{A,B,C}` | PASS — all `A` (and `own-work` is not `community`, so no tier-inflation violation) |
| `status` in `queued|mined|rejected` | PASS — all `mined` |
| ISO `opened` | PASS — all `2026-10-24` |
| `used-by` path exists | **FAIL under lane-root anchoring** — see below |

## used-by violation

All 8 rows are `status=mined`, and every `used-by` cell carries one of three paths:

- `corpus/knowledge/idle-lock-never-asked-r12.md` (S203, S204)
- `corpus/knowledge/idle-lock-chain-armed-r14.md` (S205)
- `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` (S206–S210)

Violating cell: `used-by` ($12) on every row S203–S210.

Evidence — resolved against the lane root `/home/vgpnk/Projects/shokunin/mado-shokunin/`
(the contract calls used-by "repo-relative" and the frozen census runs `[ -e "$p" ]` there):

```
MISSING(root): corpus/knowledge/idle-lock-never-asked-r12.md
MISSING(root): corpus/knowledge/idle-lock-chain-armed-r14.md
MISSING(root): corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
```

The lane-root corpus holds only `idle-lock-plane.md` and `idle-lock-route-r17.md`
(`ls corpus/knowledge/`). The three named files DO exist beneath the lane tree, but only as
fixture members — `.ufo/waves/round-35/controls/golden/corpus/knowledge/<name>` (and the sibling
control trees). Resolved relative to the fixture root `controls/golden/` itself, all three
paths exist and the check passes.

So: the rows are self-consistent as a fixture, but under the literal criterion "EXISTS under
/home/vgpnk/Projects/shokunin/mado-shokunin/" read as repo-relative, every used-by cell in
rows S203–S210 names a path that is absent at the lane root — 8 violations, 3 distinct targets.

## Pipes

No cell contains a literal or escaped pipe. `grep -nF '\|'` returns nothing (no `\|` escape),
and no `&#124;` / `&#x7C;` / `&vert;` entities exist anywhere in the file. Each row has exactly
12 `|` characters — leading edge, 10 column separators, trailing edge — all delimiters.

## Per-row record

```
S203 NF=13 own-work A mined 2026-10-24 → corpus/knowledge/idle-lock-never-asked-r12.md
S204 NF=13 own-work A mined 2026-10-24 → corpus/knowledge/idle-lock-never-asked-r12.md
S205 NF=13 own-work A mined 2026-10-24 → corpus/knowledge/idle-lock-chain-armed-r14.md
S206 NF=13 own-work A mined 2026-10-24 → corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
S207 NF=13 own-work A mined 2026-10-24 → corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
S208 NF=13 own-work A mined 2026-10-24 → corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
S209 NF=13 own-work A mined 2026-10-24 → corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
S210 NF=13 own-work A mined 2026-10-24 → corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
```

Out of scope but observed: `recheck` cells use `on-change` (5 rows), `on-request` (S204), `90d`
(S205, S210). `90d` matches a contract example; `on-change`/`on-request` are cadence-shaped but
unenumerated. Not a checked axis — recorded for the record.
