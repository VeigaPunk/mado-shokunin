# MadoR13.GateLedger — scoped report (C2 knowledge change record + named negative cases)

Draft: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/GateLedger.md` (full record, LOG/SOURCES text, N1–N10 table, measurement commands).

## Behaviour
- Read-only lane. No source, corpus, LOG.md or SOURCES.md file edited. No test, build, lint, format, selftest or `--regression` run by this lane.
- Host: read-only `sha256sum` and `wc -l` of `tools/mado-verify.sh` only.

## Findings (anchors)
1. Set-blind today. `hypr.root.include_graph` names counts and first positional mismatch only (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh:2222-2239`); `hypr.local.inventory` checks presence of 12 fixed names and cannot see a stray `*.conf` (`:2262-2273`). [O code; [I] outcome — to be measured as N1/N7.]
2. Selftest gap: scenario B asserts row ids only (`st_row_has` = id + status); scenario H asserts only the FAIL id. No case names a missing or extra member, and no case plants an extra local file. (`:938-956`, `:1013-1023`) [O]
3. Fixture A already writes 13 `*.conf` (12 LOCAL names + `gkeep.conf`, loop `:265-266`). An exact local census therefore needs `gkeep.conf` as an explicit member, or the live host reads FAIL `extra: gkeep.conf`. Decision flagged for the operator/main agent, not made here. [I]
4. Gate revision moved: `tools/mado-verify.sh` is now sha256 `ea798ad0…` (3,245 L). `gate-standing-use.md` still names `93e43f8f…` (3,231 L) in its header and §8. [O]
5. Any C2 edit lies outside the R7/R8 excised pairs, so `PIN_MADO` moves and `--regression` reads SETUP until the printed `REGRESSION_RECUT` re-cut (`:1546-1550`; `gate-standing-use.md` §4–§5.2). The record includes this ordering. [I from the round-12 pattern]

## Conventions applied
- `gate-standing-use.md` §5.2 widening rule; §3 single-line detail and row-id diff key; §8 re-derivation.
- `corpus/QUALITY.md` criterion 14 (census names missing and extra, pins membership), criterion 4 (errata append-only), criterion 2 (anchored sources).
- `corpus/SOURCES.md` 11-column row shape; S040–S043 reserved by main; gate evidence uses S044 (main allocates); `corpus/lessons/round-12.md` M13 is the mistake being closed.
- `AGENTS.md`: every change appends a LOG.md entry; commits carry lane identity.

## Covers / does not cover
- Covers: C2 hypr source and local census design; named negative cases N1–N9 with control N8 and clean control N10; mutant set M-a..M-f; measurement commands; knowledge change record text.
- Does not cover: C1 protocol/global sourcing; toggles glob membership (`~/.local/state/omarchy/toggles/hypr/*.conf`, left out of the census by design); live host re-read [U].

## Tools
None installed, updated or upgraded. (`/home/vgpnk/.omp/agent/RULES.md` read; no install needed.)

## Handoff
- Main agent: gkeep 13-list is authorized for the implementation slice (report-only canonical baseline, not endorsement); the implementer edits `tools/mado-verify.sh:2222-2273` with that pin.
- Implementer (sole writer of the gate): apply C2; record the pre-change red for N1–N4, N7, N9 from the selftest before the green run.
- Main agent verifies once after all seats land, using the commands in the draft §4 (selftest, `--no-live`, `--regression` + re-cut, snapshot pair).
- Registry: S044 is the gate-evidence id; main owns allocation. No further open decisions from this lane.
