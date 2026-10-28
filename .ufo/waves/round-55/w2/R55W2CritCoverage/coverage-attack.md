# R55W2CritCoverage — attack on the round-55 coverage claim (wave w2, falsify)

Scored revision: `57584ed67716340b3d466fa04333ac0bab3fb79e`. Lane HEAD `721ba9c1` has no diff in `corpus/`, `PROVINCE.md`, `tools/`, `quality/` against the scored revision (`git diff --stat` empty). Base for the "uncovered" question: `3b55b6e91e40f455dd56b2985e4ffc087ada92d5`.

Seat: R55W2CritCoverage. Leaf member. Lane tracked files not edited. No git mutation. Scratch: `/fast/scratch/hyaku/mado-r55/R55W2CritCoverage/` (removed before yield). Receipts and copied inputs: `receipts/`, `inputs/` in this directory.

## 0. Verdict summary

| # | Target | Verdict | Evidence |
|---|---|---|---|
| T1 | PROVINCE: "Anything outside that subset is reported `unsupported`, never guessed" | **BROKEN** | §1, `receipts/source-directive-attack.txt` |
| T2 | Frontier bullet 1: "values outside its modelled token set are reported `unsupported`, never guessed" | SURVIVES for token forms; the silent `source =` skip is not in the stated token list and is not disclosed in the entry | §1, §2.3 |
| T3 | PROVINCE: tool "reads only the files its caller names" | SURVIVES except `--selftest` (opens its own directory and a fixed nonexistent path) | §2.1 |
| T4 | PROVINCE: "starts no process, opens no socket and writes nothing" | SURVIVES | §2.1 |
| T5 | PROVINCE: "four record instruments" | SURVIVES as a count of the four it names; the three `quality/r55_ctl_c*.py` modules are tracked and not named; `check-freeze-order.py` is described as "unverified until it lands" though it is tracked at the scored revision | §2.2 |
| T6 | README coverage row: "the declared defaults 25 / 600 / 0 and their ranges" | OVERSTATED: `numlock_by_default` has no declared range (K15 is a Bool with no min/max; the entry's own line 118 says so) | §3.1 |
| T7 | Frontier: "held S052" for the `wl_keyboard.repeat_info` path | OVERSTATED: the registered S052 anchor is `wl_keyboard :2573-2699`; the cited rows K17, E04, E05 sit at `:2732-2741`, outside it. The entry's Limits (line 138) discloses this; the README frontier does not | §3.2 |
| T8 | README row: "the same keys in a keyed `device` block" | TRUE by pinned bytes (`Hyprland-legacy-ConfigManager.cpp:528,529,532`) but **UNCITED** in the entry: no K/E row quotes the device-key registration; the counter cannot see it | §3.3 |
| T9 | "Uncovered ground" (frozen C1 and R55RevCoverage F1) | SURVIVES at the source-chain level, with the split in §4 | §4 |
| T10 | Option-name readback (40/250/1) "already held" | SURVIVES: lines exist at the cited anchors and match | §4.2 |
| T11 | `hyprland-input-devices-r46.md:70` "stays as history" | NOT-ANNOTATED: the sentence is unchanged and carries no pointer to R55; the entry says it "stays as history" but the neighbour note does not say so. R55RevCoverage F5 asked for this cross-link; none was added | §5.1 |
| T12 | `hyprland-input-devices-r46.md:34` (numLock is lock state; `main` only on the virtual keyboard) | SURVIVES; live read today agrees (`hyprctl devices -j`, §5.2) | §5.2 |
| T13 | `hyprctl-verification-layer.md` (readback is global `agreement`) | SURVIVES | §4.2 |
| T14 | Per-keyboard claims in new text (entry line 108, README row, frontier) | SURVIVES: the two per-keyboard host lines are labelled source-implied, not observed; no delivery, client or per-keyboard observation is claimed | §5.3 |
| T15 | Host join receipt `receipts/live-kbdopts.txt` and `R55ScoutHost/receipts-cmp-grep.txt` | SURVIVES as of today (re-run §5.2). The receipt itself does not contain the `hyprctl devices` capture that supplied the keyboard names; the names are present today | §5.2 |
| T16 | `check-index.py --rev 57584ed…`: indexed / missing / dangling / duplicates | SURVIVES: `MADO_INDEX: rev=57584ed… indexed=70/70 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` rc=0; independent count 70 notes and 70 rows at the rev | §6 |
| T17 | Errata row (P23 supersedes P19; lines 1558, 1568, 1569) | SURVIVES for the three cited lines (pinned `Hyprland-ConfigActions.cpp` lines are the `sendKeyboardKey(..., PRESSED)`, `..., PRESSED)`, `..., RELEASED)` calls); full P23 sentence-to-pin audit is another seat's item | §7 |

## 1. Attack on the `unsupported` / "never guessed" claim (T1, T2)

The tool's own docstring (`tools/mado-kbdopts.py`, lines 28-32, 169-170) says an LHS equal to `source` is **ignored**, with no `unsupported` count. Hyprland follows `source =` in order; the host's own `hyprland.conf` has 17 `source` lines, one of which sources `~/.config/hypr/input.conf` (line 17). A `repeat_rate` set in any sourced file is therefore never read, is reported as the default, and `unsupported` stays 0.

Instrument: `tools/mado-kbdopts.py` at `57584ed` (blob sha256 `9c69dd62c1737d4842a4a0e73db3f8317eda71ee103e71ad3cda11a19c837c2e`, equal to the working-tree file). Copied to `inputs/mado-kbdopts.rev.py`; not modified. Inputs are valid hyprlang-grammar lines (not a syntactic rejection, QUALITY 105).

| case | input | command | output (decisive line) | expected under Hyprland order |
|---|---|---|---|---|
| A1 | `a.conf` = `source = b.conf`; `b.conf` = `input:repeat_rate = 50` | `python3 -I mado-kbdopts.py --config a.conf --keyboard k` | `repeat_rate=25 ... from=-/-/- unsupported=0` | 50 |
| C1 control | `b.conf` alone | `--config b.conf --keyboard k` | `repeat_rate=50 ... from=G/-/- unsupported=0` | 50 |
| C2 control | `inline.conf` = `input:repeat_rate = 50` | `--config inline.conf --keyboard k` | `repeat_rate=50 ... from=G/-/- unsupported=0` | 50 |
| A2 | `a2.conf` = `input {` `repeat_rate = 30` `}` then `source = b.conf` | `--config a2.conf --keyboard k` | `repeat_rate=30 ... from=G/-/- unsupported=0` | 50 (sourced line comes last) |
| A3 (host, read-only) | `~/.config/hypr/hyprland.conf` + live getoption (`hyprctl -j getoption` ×3, captured) | `--config $HOME/.config/hypr/hyprland.conf --keyboard hl-virtual-keyboard-fcitx5 --getoption live-getoption.jsonl` | `repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0`; `input:repeat_rate config=25 live=40 verdict=DIFFER`; `DONE ... live=DIFFER` | live 40 / 250 / 1 |
| C3 (host control) | `~/.config/hypr/input.conf` + same getoption | same, with `input.conf` | `repeat_rate=40 ... from=G/G/G unsupported=0`; three `AGREE`; `live=AGREE` | 40 / 250 / 1 |

Reading: on the host's real root file the tool reports `DIFFER` against the live compositor with `unsupported=0`. The uncounted value is the sourced one. The counter-run `hyprctl -j getoption` values (40 / 250 / 1) are the proof that the sourced file is the one that counts. The instrument does what its docstring says; the PROVINCE sentence ("Anything outside that subset is reported `unsupported`, never guessed") and the default output it produces for a sourced key do not agree. The entry's own "honesty valve" list (entry lines 116-118: `$` variables, `device[...]`, hex/signed numbers, out-of-range, `##`) does not name `source`, so the entry does not disclose this gap. The frontier's "values outside its modelled token set" sentence is limited to token forms and survives for those.

Selftest: `python3 -I mado-kbdopts.py --selftest` → `MADO_KBDOPT_SELFTEST: 83/83 assertions passed` (reproduced). Its case "source line ignored" asserts `unsupported=0`, i.e. the silent skip is the designed behaviour, not an accident.

Not run: Hyprland itself (no reload, no keyword, no dispatch). The ordering claim for A2 rests on the sourced-chain evidence already in the lane (`hyprland-input-devices-r46.md` erratum E1: two `input` blocks, later assignment wins) and on Hyprland's `source` being sequential; I did not re-pin Hyprland's `source` handler in this seat.

## 2. PROVINCE R55 paragraph: reads, writes, process, socket, instrument count (T3–T5)

### 2.1 Reads / writes / process / socket (checked against source)

- Reads: `run_cli` reads exactly the `(kind, path)` steps from `parse_args`; `read_regular` is the only file read (`os.open` O_RDONLY|O_NONBLOCK, regular-file check, 1 MiB cap at `MAX_BYTES = 1048576`). `--config` may repeat; `--getoption` is accepted once (`parse_args`, `elif flag == "--getoption" and not getoption`). This matches PROVINCE.
- Exception (T3): `selftest()` calls `_unreadable("/nonexistent/mado-kbdopts-selftest")` and `_unreadable(os.path.dirname(os.path.abspath(__file__)))` (lines 375-376). The second is an `os.open` of the tool's own directory (succeeds, then refused as not regular). So "reads only the files its caller names" is false under `--selftest`. Minor; the normal path is as stated.
- Writes (T4): none. Imports are `json, os, re, stat, sys`; no `open(...,'w')`, no `subprocess`, no socket. Output is `sys.stdout.buffer.write` only.
- Process / socket (T4): no `subprocess`, `os.system`, `socket`, `Popen` in the file (grep of the 422-line blob).

### 2.2 Instrument count (T5)

PROVINCE names four record instruments: `quality/counters/c1-r55-kbd-entry.py`, `quality/counters/c3-r55-p19.py`, `quality/check-r55-controls.py`, `quality/check-freeze-order.py`. `git ls-tree` at the scored revision shows, in addition, `quality/r55_ctl_c1.py`, `quality/r55_ctl_c2.py`, `quality/r55_ctl_c3.py`, which `check-r55-controls.py` loads by `importlib` and which the tool-ledger tracks (`tool-ledger.md` lines 125-127). PROVINCE's own correction block (line 34: "the province accounts for every tracked tool it runs") is not met by this enumeration. `check-freeze-order.py` is described as "unverified until it lands"; it is tracked at the scored revision (`ls-tree` count 1). Minor.

`check-tool-ledger.py --repo <lane> --rev 57584ed…` → `LEDGER: population=90 ledger_rows=90 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET`. So the ledger does cover the r55_ctl modules; only the PROVINCE sentence is short.

## 3. README coverage row and frontier wording (T6–T8)

### 3.1 "declared defaults 25 / 600 / 0 and their ranges" (T6)

`corpus/README.md` row MADO-R55-1 (line 82 at the rev). The entry (line 13) and the pin agree on ranges for two keys only: `input:repeat_rate` 25 min 0 max 200 (`Hyprland-ConfigValues.cpp:279`), `input:repeat_delay` 600 min 0 max 2000 (`:280`). `input:numlock_by_default` is `MS<Bool>("input:numlock_by_default", "Engage numlock by default.", false, {.refresh = …})` at `:277` with no `.min`/`.max`. The entry's line 118 says the 0..1 numlock range is "the lane's modelling rule, not a source range". The README wording "and their ranges" is wrong for numlock.

### 3.2 "held S052" (T7)

Frontier bullet 1 cites "rows S378-S380 plus held S052, S162, S215, S316-S319" for the `repeat_info` path. `SOURCES.md` S052 at the rev: `wl_keyboard :2573-2699`. The entry's cited rows are `E04` (`wayland-1.26.0-wayland.xml:2732`), `E05` (`:2740`), `K17` (`:2741`). Those lines are outside the registered anchor. The entry's Limits line 138 discloses the gap ("S052 records wl_keyboard :2573-2699, which does not reach K17 at line 2741…"). The README frontier and coverage row do not carry the disclosure, so a reader of the index sees "held" for lines the registry does not hold.

### 3.3 Device-key registration (T8)

The README row and the entry's Scope/Chain say the same keys work in a keyed `device` block. The entry's device evidence is K16 (`getConfigValueSafeDevice`, legacy `:1119`) and E12 (`:1120`), and `getDeviceInt` at legacy `:1134`. No row quotes the registration of `repeat_rate`, `repeat_delay`, `numlock_by_default` as device values. The pinned bytes do contain it: `.ufo/waves/round-55/fetch/Hyprland-legacy-ConfigManager.cpp:518` (`addSpecialCategory("device", {"name"})`), `:528` (`repeat_rate`, INT 25), `:529` (`repeat_delay`, INT 600), `:532` (`numlock_by_default`, INT 0). Also `round-46/fetch/Hyprland-ConfigManager.cpp:528` is the same line and was in the R46 entry's 47-value census. So the claim is true and was held at R46; the R55 entry does not cite it, and the counter cannot score it. Grep of the entry for `528`, `addSpecial`, `registration`, `device block`: no match.

`getDeviceInt` → `getConfigValueSafeDevice` (legacy `:1117-1131`, verified by `sed`): device value when `m_bSetByUser`, else `getConfigValuePtr(fallback)`. So the K01–K03 chain does hold at source level.

## 4. "Uncovered ground" (T9, T10, T13)

Base grep (`git grep -n -E 'repeat_info|m_repeatRate|updateRepeatInfo|applyConfigToKeyboard|getDeviceInt' 3b55b6e -- corpus`):

- `repeat_info`, `m_repeatRate`, `updateRepeatInfo`: **0 hits** in corpus at base. Claim holds.
- `applyConfigToKeyboard`: held at base in `hyprland-input-devices-r46.md:32` (step 3, per-keyboard lookup) and `SOURCES.md` S316. Not new.
- `getDeviceInt`: 0 hits at base.
- The device-over-global mechanism (`!VAL->m_bSetByUser && !fallback.empty()` at `legacy:1119`): held at base as R46 OBS S317 (`hyprland-input-devices-r46.md:41`). Not new; the R55 entry does cite it as held (header line 1).
- Host readback `repeat_rate 40` / `repeat_delay 250` / `numlock 1`: held at base as `agreement` in `hyprctl-verification-layer.md:132-134` (verified: lines are the three `input:` rows) and `config-health-report-r3.md:546-548` (verified). Not new. The R55 entry labels H01–H06 as "restatement under a new pin" (line 127-128), which is honest.

New at the rev (the actual ground added): K01–K09 (reads, clamp, stored fields, unchanged-config guard, numlock block), K10–K12 and K17–K18 (seat path and stored member initialisers), E01–E13, and the three `ConfigValues` default/range rows K13–K15 (the file is held; these lines were not).

So "uncovered ground" is true for the source chain from the stored fields onward to the seat path, and for the NumLock keymap block. It is not uncovered for the device-lookup mechanism or the readback values. The entry does not claim otherwise; the README row's "held S052" (T7) and "ranges" (T6) are the two overstatements in the index layer.

Per R55RevCoverage F4, `repeat_info` appears in round-15 wave reports (`.ufo/waves/round-15/w1/reports/WaylandKeyboard.md:125-126`, `ReviewKeyboard.md:16`) outside the corpus. The R55 text does not claim first sight, so nothing is overclaimed there.

## 5. Neighbour notes and per-keyboard wording (T11–T15)

### 5.1 `hyprland-input-devices-r46.md`

- Line 70 (the UNK sentence) is unchanged at the rev. `grep -n -i 'round 55\|r55\|round-55' ` on that file at the rev returns nothing. The only R55-era material in that file is the R47 erratum (lines 75-94). So the R55 entry's "that sentence stays as history" (entry line 115) has no marker in the neighbour note. R55RevCoverage F5 asked for a cross-link; it was not added.
- The sentence itself is still true of the join `tools/mado-devices.py` (which does not compare these keys) and of the dump (which prints none of them, as the R55 entry says at line 115). The problem is annotation, not truth.
- Line 34 (step 5): "`numLock` (locked-modifier state, not the `numlock_by_default` option) … on this host only the input-method virtual keyboard has [`main`]". Consistent with the R55 entry (line 112). Live check §5.2.

### 5.2 Host reads (read-only; `hyprctl getoption -j`, `hyprctl devices -j`, `hyprctl version`, `cmp`, `grep`)

- `hyprctl version` → Hyprland 0.56.2, commit `efb50993780079460b0cbed1363e2166a2de1d9f`.
- `hyprctl -j getoption input:repeat_rate|repeat_delay|numlock_by_default` → 40 / 250 / 1, `set: true`. Matches H04–H06 and `live-kbdopts.txt`.
- `sha256sum ~/.config/hypr/input.conf` → `3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4`; `cmp` with `fetch/host-input.conf` → identical. Matches the R46 erratum sha.
- `hyprctl devices -j` keyboards today: nine physical names plus `hl-virtual-keyboard-fcitx5` (`main: True`, `active_keymap: Portuguese (Brazil)`). `hp--inc-hyperx-alloy-origins-core` (named in the receipt) is present. `main` is `True` only on the virtual keyboard, matching r46:34.
- `grep -rnE 'device\[|device \{|device\{' ~/.config/hypr` → no match (rc=1), matching `R55ScoutHost/receipts-cmp-grep.txt`.
- Re-run of the tool on the host input file with today's getoption: `repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0`; three `AGREE`; `live=AGREE` (`receipts/source-directive-attack.txt`, C3).

Gap (T15): `receipts/live-kbdopts.txt` does not contain the `hyprctl devices -j` capture that supplied its keyboard names, and shows the getoption input as `<3 getoption lines>` rather than a file. The receipt's stated `cmp` line refers to `live-getoption` vs the committed JSON, which is in the receipt. The names are present today; the provenance of the 2026-10-28 names is not in the receipt.

### 5.3 Per-keyboard wording (T14)

The entry (line 108) says the two per-keyboard lines are "what the source implies for those names, not an observed per-keyboard value". The README row says "become the per-keyboard values Hyprland 0.56.2 stores" (source-level; the row header says "Source-level and config-level only"). Frontier bullet 1 says "This is source-level and config-level evidence only: no key was pressed, no client's repeat was observed". K10 and the entry's Unknowns (line 24) say which keyboard `m_keyboard` is, is UNKNOWN. No text claims a delivered value, a client behaviour or a per-keyboard observation beyond these qualifiers.

The `hl-virtual-keyboard-fcitx5` line is config-implied only; the r46 erratum records that the virtual keyboard exists only while the input method holds it.

## 6. check-index (T16)

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-index.py --rev 57584ed67716340b3d466fa04333ac0bab3fb79e --repo /home/vgpnk/Projects/shokunin/mado-shokunin
MADO_INDEX: rev=57584ed67716340b3d466fa04333ac0bab3fb79e indexed=70/70 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
rc=0
```

Independent count at the rev: `git ls-tree -r --name-only … corpus/knowledge | grep -c '\.md$'` → 70; `git show <rev>:corpus/README.md | grep -c '^| \`knowledge/[^\`]*\.md\`'` → 70. The new row (line 82) names `knowledge/hyprland-keyboard-repeat-numlock-r55.md`, which exists. The errata row (line 81) names `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`, which exists. Index-completeness is clean; row fidelity (what the row says) is §3.

## 7. Errata row (T17)

The row (README line 81) says `Actions::pass` sends PRESSED on the `m_passPressed == 1` arm (`Hyprland-ConfigActions.cpp:1558`) and on the `else` arm (`:1568`, followed by RELEASED at `:1569`). Checked against `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp`:

- `:1558` `g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);`
- `:1568` `g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);`
- `:1569` `g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_RELEASED);`

All three match the row and the errata table (Q03, Q09, Q10). The row's "neither correction claims a host event or new coverage ground" matches P23's own scope statement. Whether P23's sentence follows from its quotes is the separate sentence-to-pin audit, which the frontier lists as still open; not attacked here.

## 8. Not verified / limits

- No Hyprland process was observed; no key was pressed; no keyword, dispatch, reload or config write was run. Host reads are the allowed set only.
- Hyprland's handling of `source =` is inferred from the sequential-include evidence already in the lane (R46 erratum E1) and the host's own `hyprland.conf`; the sourced-file precedence in A2 is not re-pinned here.
- hyprlang one-line blocks (`input { repeat_rate = 30 }`) and flat `device:repeat_rate = …` were considered and not attacked: the pinned hyprlang parser (`hyprlang-config.cpp:713`, `:881-906`) routes a line with `=` to a set-value and would likely reject these as unknown keys, which is an error rather than a guessed value. Behaviour not run.
- The C1 counter, the controls and the C2 hold-out were not run (other seats' items).
- The seat did not rebuild or re-run `check-r55-controls.py`.

## 9. Tooling and cleanup

- No tool installed or upgraded. Used: `git` (read-only: `show`, `grep`, `ls-tree`, `diff`), `python3 -I` for the three lane-provided checkers and the copied tool, `sha256sum`, `cmp`, `grep`, `sed`, `hyprctl` read verbs.
- Mutations: none to the tracked tool. The tool was copied from the scored revision and run unchanged; attack inputs were created in scratch and copied into `inputs/`.
- Lane writes: only `.ufo/waves/round-55/w2/R55W2CritCoverage/` (this file, `receipts/`, `inputs/`) and the report `.ufo/waves/round-55/w2/R55W2CritCoverage.md`.
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2CritCoverage/` removed before yield.
