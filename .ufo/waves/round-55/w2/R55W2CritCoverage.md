# R55W2CritCoverage — report (wave w2, falsify, coverage-claim honesty)

Full evidence: `.ufo/waves/round-55/w2/R55W2CritCoverage/coverage-attack.md`. Receipts: `.ufo/waves/round-55/w2/R55W2CritCoverage/receipts/source-directive-attack.txt`. Copied inputs: `.ufo/waves/round-55/w2/R55W2CritCoverage/inputs/`.

Scored revision `57584ed67716340b3d466fa04333ac0bab3fb79e`; no diff in `corpus/`, `PROVINCE.md`, `tools/`, `quality/` between it and lane HEAD `721ba9c1`.

## Ran
- `python3 -I quality/check-index.py --rev 57584ed… --repo <lane>` → `indexed=70/70 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, rc 0. Independent count 70 notes / 70 rows.
- `python3 -I quality/check-tool-ledger.py --repo <lane> --rev 57584ed…` → `population=90 ledger_rows=90 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET`.
- `tools/mado-kbdopts.py` (blob sha256 `9c69dd62…c2`, unchanged; copied to scratch) run on constructed inputs and on the host's `hyprland.conf` and `input.conf` with today's live `hyprctl -j getoption` reply; `--selftest` → `83/83 passed`.
- Base grep (`git grep` at `3b55b6e`) for `repeat_info|m_repeatRate|updateRepeatInfo|applyConfigToKeyboard|getDeviceInt`; line checks of the cited readback rows, the S052 anchor, the errata quote lines (round-52 pin `:1558/:1568/:1569`), and the device-key registration (`fetch/Hyprland-legacy-ConfigManager.cpp:528-532`).
- Host reads only: `hyprctl version`, `hyprctl -j getoption` ×3, `hyprctl devices -j`, `sha256sum` and `cmp` of `~/.config/hypr/input.conf`, `grep` for `device` blocks. No keyword, dispatch, reload, config write or key press.

## Did not run
- Hyprland's own behaviour on `source =` ordering (inferred from lane evidence), the C1 counter, the controls, the C2 hold-out, the P23 sentence-to-pin audit.

## Verdicts (coverage-attack.md §0 has the full table)
- **BROKEN** — PROVINCE R55 sentence "Anything outside that subset is reported `unsupported`, never guessed". Reproduction: a `source = b.conf` line is silently skipped, the sourced `input:repeat_rate = 50` is never read, output `repeat_rate=25 … from=-/-/- unsupported=0`; on the host root `hyprland.conf` the tool prints `repeat_rate=25`, `unsupported=0`, verdict `DIFFER` against live 40. Controls on the same unchanged instrument give 50 when the line is read directly or inlined. Entry's honesty-valve list (lines 116–118) does not disclose `source`.
- **OVERSTATED** — README row "the declared defaults 25 / 600 / 0 and their ranges": numlock has no declared range (ConfigValues.cpp:277 has no min/max; entry line 118 says so).
- **OVERSTATED** — Frontier "held S052" for the `repeat_info` path: S052 is anchored at `wl_keyboard :2573-2699`; cited lines 2732–2741 are outside it (entry Limits line 138 admits this; README does not).
- **UNCITED-but-TRUE** — "the same keys in a keyed `device` block": pinned bytes `legacy-ConfigManager.cpp:528,529,532` support it; no entry row quotes them.
- **NOT-ANNOTATED** — `hyprland-input-devices-r46.md:70`: unchanged and unmarked at the rev; the entry says it "stays as history", the neighbour note does not. R55RevCoverage F5's cross-link is absent.
- **MINOR** — PROVINCE "reads only the files its caller names": `--selftest` also opens `/nonexistent/…` and the tool's own directory (`mado-kbdopts.py:375-376`). PROVINCE "four record instruments" omits the tracked `quality/r55_ctl_c{1,2,3}.py`; `check-freeze-order.py` is described as "unverified until it lands" though tracked at the rev.
- **SURVIVES** — "uncovered ground": `repeat_info`, `m_repeatRate`, `updateRepeatInfo` have 0 corpus hits at base. Already held at base: `applyConfigToKeyboard` (r46:32, S316), the device-over-global mechanism (r46 OBS S317 at legacy:1119), and the host readback 40/250/1 (`hyprctl-verification-layer.md:132-134`, `config-health-report-r3.md:546-548`, both verified). New: K01–K15 (incl. ConfigValues rows), K17–K18, E01–E13, S378–S380 chain, NumLock block.
- **SURVIVES** — PROVINCE "starts no process, opens no socket and writes nothing" (imports `json os re stat sys`; no subprocess, socket or write-mode open).
- **SURVIVES** — per-keyboard wording in the README row, frontier and entry: source-level qualifiers present; no delivery, client or per-keyboard observation claimed.
- **SURVIVES** — `hyprctl-verification-layer.md` and `hyprland-input-devices-r46.md:34`; host agreement re-read today (40/250/1 AGREE; `hl-virtual-keyboard-fcitx5` `main: True`; input.conf sha `3769c92a…` and `cmp` identical).
- **SURVIVES with a provenance gap** — `receipts/live-kbdopts.txt` does not contain the `hyprctl devices -j` capture that supplied its keyboard names (names are present today).
- **SURVIVES** — errata row: `Hyprland-ConfigActions.cpp:1558/1568/1569` are the PRESSED/PRESSED/RELEASED `sendKeyboardKey` calls in the round-52 pin.

## Mutation / scratch
No tracked file edited; the instrument was run unchanged from a copy. Scratch `/fast/scratch/hyaku/mado-r55/R55W2CritCoverage/` removed before yield. No tool installed or upgraded.
