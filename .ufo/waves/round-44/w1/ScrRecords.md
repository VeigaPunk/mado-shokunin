# ScrRecords — SCORECARD Round 44 section + LOG Round 44 entry skeleton

## Behavior (what this seat produced)

Two append-ready drafts, nothing else changed:

1. `w1/ScrRecords/scorecard.md` — the Round 44 `SCORECARD.md` section: header paragraph (registration freeze
   `e2289516a9a857f55cda7be635933e89b931c3da`, base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`, the two-claim shape, the
   lowest-axis rule from `receipts/axis-base.txt`, the C1 false-report ground), the two-row claim table (C1 operability /
   C2 coverage; before values from `receipts/c1-before-base.txt` and `receipts/c2-before-base.txt`, after side and
   self-verdicts `<<L1>>`), a separability line, the `### Capabilities (round 44)` row plus the row-form argument, the
   Sources/saturation/planned block with round-45 intent, a `### Wave w2 outcome (round 44)` slot, and the D5 erratum line.
2. `w1/ScrRecords/log.md` — the `LOG.md` Round 44 entry: one bullet per landed change (freeze, pins, C1 ground, controls,
   before-measurements, w1 dispatch, data commit, closure D1-D7, w2, tip receipts), `<<L1>>` wherever only the L1 can fill
   the value.

Convention used: `<<L1>>` marks every value that does not exist at this freeze (data-commit hash, after receipts, w2 seat
count, registry tier, refused-residue set, mistake/QUALITY ids, axis re-derivation). No after-value is asserted; every
before-value is copied from a committed receipt.

## Capability row: which form is honest (the argument the draft carries)

`AXES.md` §Capabilities: "Rows enter only through a round that demonstrates the capability running; a capability without a
passing demonstration in the round report is pre-claiming and does not enter the table."

- **New row — rejected.** The capability the table names (join a `windowrule = size` line to the client's reported box) is
  the round-43 one; round 44 adds window state to the same verb, not a second capability. Two rows would describe one tool
  twice and drift apart as the tool changes; the round-30 "corrected scope" row is precedent for a *correction* of a row,
  not for a re-entry of the same capability.
- **Leave the round-43 row as written — rejected as inaccurate.** The row says the tool reports "AGREE / DIFFER / TILED /
  BADSIZE against the reported goal box". At base that is the whole verdict set (`tools/mado-geometry.py:49`); after C1 a
  fullscreen gkeep window reads `FULLSCREEN` and never `DIFFER` — the row would describe a verdict the tool no longer ends
  at, which is exactly the false report C1 removes.
- **Extend the row in place — chosen.** `First-working round` becomes `43 (state verdicts 44)`: the same cell form the
  table already uses for re-demonstration (`5 (re-demonstrated 12)`), so the join keeps its honest 43 and the extension
  carries its own round. The `What it can now do` and `Evidence pointer` cells are rewritten to the post-C1 contract.

## Gates run (each command and what it showed)

| Check | Command | Result |
|---|---|---|
| base tool lacks state verdicts | `grep -c 'FULLSCREEN\|MAXIMIZED\|maximized=' tools/mado-geometry.py`; `grep -n 'TILED\|BADSIZE' tools/mado-geometry.py` | `0`; docstring at `:49` = `BADSIZE (size none) | TILED (not floating) | AGREE (size == want) | DIFFER` (so extending the row's text is required, not cosmetic) |
| reference selftest claim in the freeze | `python3 -I .ufo/waves/round-44/c1/ctl-ref-tool.py.txt --selftest` | `MADO_GEOMETRY_SELFTEST: 91/91 passed`, rc 0 — saved as `w1/ScrRecords/ref-selftest.txt` and cited in the LOG freeze bullet |
| C1 erratum locators | `grep -n 'M43-9 —' corpus/lessons/round-43.md`; `sed -n '5p' .ufo/waves/round-43/registration.md`; `grep -n '38 seats' LOG.md` | `191`; line 5 = "… `w1` (build + first falsifiers, 37 seats) …"; `2489` (`38 seats`) |
| C2 chain locators | `grep -n` over `fetch/Hyprland-Window.cpp`, `fetch/Hyprland-XDGShell.cpp`, `fetch/gkeep-ui.py` | `sendWindowSize` `:1732`, `realToReportSize` `:1685`, `setSize` in `m_pendingSizeAcks` `:1753`, `onAck` `:1514-1521`, X11 `configure` `:1547,1573`; xdg `setSize` -> `scheduleConfigure` `:354-357`, `:629`; `set_default_size(420, 500)` `:476`, no `set_size_request` |
| C1 ground locators | `grep -n` over `fetch-c1/*` | `eFullscreenMode` `:12-15` (`FSMODE_NONE = 0, FSMODE_MAXIMIZED, FSMODE_FULLSCREEN`); monitor box `:192,194`, work area `:196,198`; `fullscreen` key `HyprCtl.cpp:410`, value `getFullscreenModes(w).internal` `:431` |
| before-values copied, not invented | `cat receipts/c1-before-base.txt receipts/c2-before-base.txt receipts/ctl-c1.txt receipts/ctl-c2.txt receipts/axis-base.txt receipts/c2-ground-base.txt` | C1 `fixtures=12/26 … TARGET_MISSED`, `a:1 b:0 b4:0 g:1 r:1`, exit 1; C2 `admitted=0/1`, `a:0 … i:0`, exit 1; `CTL_C1 controls=15`, 0 of 15 non-reference MET; `CTL_C2 controls=3`, 0 of 3; axes 60/60, 68/68, 12/12, `checked=3 mismatched=0`; base chain grep exit 1 |
| draft table shape | `awk` pipe count per `|`-row | 5 pipes for 4-column rows (one C2 cell carries 3 escaped `\|` inside a code span) |

Not run: no counter was scored (that is the claim's job, not the record's), no campaign tool in `/home/vgpnk/Projects/shokuknow/merge/mado`
was executed, no host or compositor write. No tool was installed this seat.

## Touched surfaces

- `.ufo/waves/round-44/w1/ScrRecords/scorecard.md` (new)
- `.ufo/waves/round-44/w1/ScrRecords/log.md` (new)
- `.ufo/waves/round-44/w1/ScrRecords/ref-selftest.txt` (new; the reference selftest receipt)
- `.ufo/waves/round-44/w1/ScrRecords.md` (this report)
- `/fast/scratch/hyaku/mado-r44/ScrRecords/` created and removed; nothing else written.

## Out of scope (deliberately untouched)

`SCORECARD.md`, `LOG.md`, `quality/counters/*`, `.ufo/waves/round-44/{registration.md,ctl,c1,receipts}`, the shokuknow
checkout, templates/scripts/MANIFEST, `.ufo/state`, and the lane index; no git/jj mutation anywhere. Applying the drafts
(and replacing the round-43 capability row's two cells) is the L1's integration step.

## Findings

1. **F1 — the round-43 capability row goes stale the moment C1 lands.** `tools/mado-geometry.py:49` is the base verdict set;
   after C1 the tool's terminal verdicts include `FULLSCREEN`/`MAXIMIZED` and the summary gains
   ` maximized=<n> fullscreen=<n>` when either is non-zero. A row left as written would misstate the tool. The draft
   extends it and records `43 (state verdicts 44)`.
2. **F2 — two locators, not one, for the `fullscreen` field.** The JSON key is declared at `Hyprland-HyprCtl.cpp:410`; the
   value printed for it is `sc<uint8_t>(Fullscreen::controller()->getFullscreenModes(w).internal)` at `:431`. A LOG line
   citing only `:410` would not show where the integer comes from; the drafted bullet names both.
3. **F3 — D5 erratum drafted as one appended line** (SCORECARD "Mistakes M43-1..8" vs `corpus/lessons/round-43.md:191`
   M43-9; round-43 `registration.md:5` 37 seats vs 38 at `LOG.md:2489`), with the Round 43 text left as written — the
   closure's D1/D2 routing requires supersession, not edits to Round 43 prose.
4. **F4 — the LOG's w2 seat count cannot come from the registration** (it records w1 only, `registration.md:5`). The draft
   leaves `w1`'s 38 as given (assignment + registration shape paragraph) and the w2 count as `<<L1>>` from the dispatch.
5. **F5 — the C2 row's "after" has no positive control behind the predicate yet** (`receipts/ctl-c2.txt` is three
   do-nothing controls). The claim table says so explicitly and points at `w1/ExecC2Positive`; if w1 fails to build a
   positive control, the C2 self-verdict must carry that as a declared residual, not a silent pass.

## Artifacts

- `.ufo/waves/round-44/w1/ScrRecords/scorecard.md`
- `.ufo/waves/round-44/w1/ScrRecords/log.md`
- `.ufo/waves/round-44/w1/ScrRecords/ref-selftest.txt`
- `.ufo/waves/round-44/w1/ScrRecords.md`

Report: .ufo/waves/round-44/w1/ScrRecords.md
