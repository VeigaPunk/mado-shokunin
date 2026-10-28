# R55ScribeEntryC — round 55, wave w1 (C1 entry draft, scoped findings)

Seat: R55ScribeEntryC (leaf, no subagents, no lane edits, no git/jj, no host mutation).
Deliverables: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ScribeEntryC/
Status: DRAFT. The L1 integrates. Not committed, not applied to corpus/.

## 1. What I did

1. Read the frozen contract: `registration.md` (§C1, §C2, seat boundaries), `claims-frozen.md` (C1 predicate and kill rule), `frozen-tables.json` (c1.k, c1.h, c1.pin_sha256, c1.new_row_pins, c1.source_suffix).
2. Read every pin the entry cites, at the frozen line numbers, under `.ufo/waves/round-55/fetch/` (committed files, not the working tree of any other lane).
3. Read the existing registry rows S052, S215, S316, S317, S318, S319, S354 in `corpus/SOURCES.md` (read only) to check the S-id bindings and anchor columns.
4. Read the host files and the allowed host reads only: `~/.config/hypr/input.conf` (sha256 compared with the committed pin), `hyprctl version`, `hyprctl getoption input:repeat_rate|input:repeat_delay|input:numlock_by_default -j`, `hyprctl devices -j`. No keyword, dispatch, reload or service command was run.
5. Wrote `gen_entry.py`: K and H pin/line/quote cells are read from `frozen-tables.json` (never typed); the proposition cells and E-row needles are typed by me, and every needle is asserted to be a substring of its pin line.
6. Wrote `verify_entry.py`, an independent checker (it derives expected S-ids from the registration text, not from the generator). It checks the trio, row ids, anchors, quote cells against the frozen cells and against the pin bytes, host quotes against the host pin, every pin sha256 against `c1.pin_sha256` and `SHA256SUMS.txt`, proposition length and tags, and runs five quote-level mutants (C1-CTL-2..6 analogues).
7. Did not look for, open or use the sealed hold-out. I opened only the committed `fixtures/c2/F02/expected.out` and `args.json` to compare the host-join reading.

## 2. Commands and decisive output (trimmed)

Pin hashes (`sha256sum fetch/*`), matched against `c1.pin_sha256`:
```
feedf32e...4765  Hyprland-InputManager.cpp      (frozen feedf32e...4765) ok
8a800efe...1aa3  Hyprland-IKeyboard.cpp         ok
3769c92a...47bf4 host-input.conf                ok  == ~/.config/hypr/input.conf (IDENTICAL, live sha 3769c92a...)
5557e28f...eab6  host-getoption.json            ok
```
Frozen tables sha (equals `receipts/freeze-verify.txt` line `frozen-tables.sha256=bf46c889...9490`): `bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490`.

First generator run (defect evidence, see D1):
```
ERROR K16: forbidden character '|' in cell
gen rc=1
```

Generator, after allowing the pipe in quote cells only (proposition cells are still checked by the verifier):
```
WROTE .../R55ScribeEntryC/entry.md lines=91 sha256=45d0f049ebb557b36cd219271df5352c9cc9840c5593899dc1a29969f906faf8
```

Verifier (`python3 -I verify_entry.py --selftest --entry .../entry.md > verify.txt`), decisive lines:
```
entry=... sha256=45d0f049... bytes=18614
ROWS: trio=ok ids_seen=39
  K quotes+anchors+sources+props ok: 18/18
  H ok: 6/6
  E ok: 15/15 (extra rows; counter ignores)
FAILS:
  source_cell:K17: literal registration leg: S052 URL lacks the frozen commit efb50993 (wayland tag 1.26.0 is not that commit)
VERIFY_ENTRY: rows_K=18/18 rows_H=6/6 extra=15/15 pins=ok fails=1 verdict=FAIL
SELFTEST (mutants of the draft must each produce their named leg):
  C1-CTL-2 spliced-quote: expected quote:K04 -> caught
  C1-CTL-3 shifted-anchor: expected anchor:K01 -> caught
  C1-CTL-4 wrong-source: expected source_cell:K10 -> caught
  C1-CTL-5 dropped-row: expected row:K17 -> caught
  C1-CTL-6 host-forged: expected host:H02 -> caught legs=[host:H02, quote:H02, ...]
SELFTEST_RESULT ok
```
The verifier exits 1 because of the single S052 leg (D2). It is reported, not hidden. Every quote, anchor, pin hash and K/H cell is otherwise clean.

Verifier-bug history (fixed before the final run, recorded for honesty): the first selftest showed CTL-6 `host:H02` MISSED because the host check tested the frozen quote instead of the cell quote; fixed so the host leg tests the cell quote against the host pin, as the counter's `host:<id>` leg describes. A second run then showed all five mutants caught.

Host reads (`host-live-reads.txt`, read-only):
```
Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean
{"option": "input:repeat_rate", "int": 40, "set": true }
{"option": "input:repeat_delay", "int": 250, "set": true }
{"option": "input:numlock_by_default", "int": 1, "set": true }
3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4  /home/vgpnk/.config/hypr/input.conf
```
Live getoption equals the committed record (40, 250, 1). `hyprctl devices -j` keyboard list at my second read: razer-razer-deathadder-v2-keyboard, razer-razer-deathadder-v2-1, hp--inc-hyperx-alloy-origins-core (main=True), -keypad, -consumer-control, video-bus, power-button, power-button-1, yubico-yubikey-otp+fido+ccid. At my first read (about 10 minutes earlier) the list also held hl-virtual-keyboard-fcitx5 with main=True and no hp main; see D8.

Not run: `How to verify` counter commands (`quality/counters/c1-r55-kbd-entry.py`, `quality/check-r55-controls.py`) — these do not exist in the lane tree I read; the `sed`/`sha256sum` lines in the entry were checked by content against my reads, not re-executed as printed.

## 3. Deliverables

- `R55ScribeEntryC/entry.md`: the C1 entry draft (trio first; prose; 18 K rows; 6 H rows; 15 extra E rows; Limits; How to verify). Generated, not hand-typed for K/H.
- `R55ScribeEntryC/gen_entry.py`: generator (reads `frozen-tables.json`; E needles asserted against pins).
- `R55ScribeEntryC/verify_entry.py`: independent verifier with `--selftest`.
- `R55ScribeEntryC/verify.txt`: verifier output (the receipt above).
- `R55ScribeEntryC/host-live-reads.txt`: the read-only host receipt.
- Scratch `/fast/scratch/hyaku/mado-r55/R55ScribeEntryC/` was created, used for nothing persistent, and removed at yield.

## 4. Contract defects and ambiguities (with the input that shows each)

D1. K16 frozen quote contains a pipe; the grammar forbids pipes in cells. `frozen-tables.json` c1.k K16 quote is `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())` (pin `Hyprland-legacy-ConfigManager.cpp:1119`, verified present in the pin). Registration §C1 says "no `|` inside a cell" and "quote cell byte-equal to frozen". Both cannot hold. I kept the frozen bytes byte-equal and wrote the row with `||` in the quote cell; in GFM this row is split into extra cells. The entry's Limits says so. Decision needed from the L1 (the counter's parse of K16 is not known to me).

D2. Literal `source_cell` leg cannot pass for K17 on any honest entry. Registration §C1: `source_cell:<id>` fails unless "the K row's S-id is a registry row whose URL ends with the pin's source_suffix and contains the frozen commit". K17's pin is wayland 1.26.0 (`wayland-1.26.0-wayland.xml`, suffix `1.26.0/protocol/wayland.xml`), S052's URL is `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`, which does not contain `efb50993780079460b0cbed1363e2166a2de1d9f`. Result in the verifier: `source_cell:K17` FAIL, verdict FAIL with the rest clean. Under the literal counter the good tree would not print TARGET_MET. The contract needs a wayland-specific rule (suffix + pinned tag) or the L1 must reconcile it; I did not edit the contract.

D3. Registry anchors do not list some cited lines (existing rows reused by the registration, anchors read from `corpus/SOURCES.md` column 6):
  - S318 lists `Hyprland-ConfigValues.cpp:271-279` and `:296`; K14 cites line 280 (frozen). The row needs its anchor widened to 280 (the ConfigValues `repeat_delay` declaration). S215's anchor (`:629`, `:632`) does not cover it either.
  - S052 lists wl_keyboard `:2573-2699`; K17 cites 2741 (frozen), and my extra rows E11 (2736) and E12 (2740) are also outside. The repeat_info event sits in the version-4 additions at wayland.xml 2730-2745.
  - S319 lists `Hyprland-IKeyboard.cpp:60-145`; extra row E04 cites line 147 (the `updateActiveKeyboardData()` call at the end of setKeymap).
  - S316 lists `:1213-1295`; extra row E06 cites 1197 (`setKeyboard(keeb)`).
  - Pending rows: S378 anchor `:175-178` does not cover extra row E13 (line 172); S379 anchors `:441-448`, `:603-609` do not cover extra row E07 (line 350).
  The K-row gaps (K14, K17) are frozen anchors that the existing rows do not support as recorded; the L1 has to widen those rows (integration surface) — I did not edit SOURCES.md.

D4. numlock range not shown by the cited pin. Registration §C2 says the range `numlock_by_default` 0..1 is at `ConfigValues.cpp:277-280`. Line 277 (`MS<Bool>("input:numlock_by_default", "Engage numlock by default.", false, {.refresh = Supplementary::REFRESH_INPUT_DEVICES})`) carries no `.min`/`.max`; lines 279-280 are the repeat_rate/repeat_delay ranges. So the C2 tool's rule "numlock value other than 0 or 1 → unsupported" is a modelling choice that the cited pin does not source. No pin in the lane shows what Hyprland does with `numlock_by_default = 2` (a hyprlang integer parse accepts it per the round-46 pin; the Bool storage behaviour is not pinned). This is also the numlock integer-type question; I marked it UNKNOWN in the entry (K15 Limits). This affects C2 expected outputs for numlock values outside 0..1.

D5. Source of the true→1 mapping not a registry row. The hyprlang spelling `true` → 1 is at `.ufo/waves/round-46/fetch/hyprlang-config.cpp:259-260` (I read these lines; the pin file exists). The entry cites it only as INFERENCE, not as an E row, because no registry row in this lane has that pin path as its anchor (S324 is hyprlang v0.6.8 config.cpp with other anchors; I did not verify whether S324 lists 259). The host join depends on it (H03 true → H06 int 1).

D6. Two numlock readers, one lock (the emphasis item). `InputManager.cpp:1223` (K03, devname) and `IKeyboard.cpp:120` (K08, m_hlName) call `getDeviceInt` with the same key and fallback; the lock at `IKeyboard.cpp:122` (K09) uses the K08 read, and `m_numlockOn` (InputManager:1284; IKeyboard.hpp:123 initialised to -1) is used only in the early-return compare at InputManager:1271 (E05). Across the eight pinned .cpp/.hpp files, `m_numlockOn` is read only at 1271 and written only at 1284 (grep over the fetch directory). Consequence: storing m_numlockOn locks nothing; a keymap set with `m_keymapOverridden` (IKeyboard.cpp:61-63) skips both readers' lock path. Not verified: whether any live keyboard has m_keymapOverridden set (UNKNOWN).

D7. Integer-type consequence (emphasis item). `getDeviceInt` returns `std::any_cast<Hyprlang::INT>(val->getValue())` (legacy ConfigManager.cpp:1136, E01). A Bool-declared option therefore reaches `NUMLOCKON == 1` as an integer only if the stored value is of type Hyprlang::INT; if it were not, `std::any_cast` throws `std::bad_any_cast` (C++ semantics; not exercised). The pins do not show Bool's storage type. The live getoption record `"int": 1` for numlock (H06) is consistent with INT storage; this is held as a host read, INFERENCE for the storage type. An absent value (`if (!val) return {};`, line 1133-1134, E02) reads as integer 0, not as the declared default false.

D8. Live keyboard list is not stable across reads. Two `hyprctl devices -j` reads ~10 minutes apart differ in the main keyboard: first read main=True on `hl-virtual-keyboard-fcitx5` (no hp device main); second read main=True on `hp--inc-hyperx-alloy-origins-core` (no virtual keyboard listed). This is an observation, not a pin claim; it means `--keyboard NAME` arguments in C2 cannot be taken from one snapshot as stable.

D9. `set` flag. The live and committed getoption records carry `"set": true`; the meaning of `set` is not pinned anywhere in the lane. Left UNKNOWN in the entry.

D10. AGREE/DIFFER reading (emphasis item). Reading rule written into the entry: the config side is the GLOBAL value from input.conf (default when unset; `true` as 1 by the hyprlang parse, INFERENCE from D5); the live side is the integer from getoption. AGREE needs integer equality, not string equality (`"true"` vs `1` would DIFFER on a naive comparison). getoption is the global option and shows no device override (INFERENCE, the command form takes no device argument; the hyprctl source is not pinned), so AGREE says nothing about any keyboard's effective value. Live verdict for this host with the committed inputs: input.conf 40/250/true (config 40/250/1) against live 40/250/1 → AGREE for all three, for the global value only.

D11. Declarations versus delivery (task requirement). H01-H03 say what input.conf declares; H04-H06 say what the committed getoption record read. Nothing pinned shows what any client received on the running host (K12 and K17 are source/spec text). Stated as UNKNOWN in the entry.

## 5. Checks not run / not verified (plain)

- Counter `quality/counters/c1-r55-kbd-entry.py` and harness `quality/check-r55-controls.py`: not present in the lane tree I could read; not run.
- C1-CTL-7 (pin tamper): not run as a harness control; my verifier's pin-hash check fails on a changed pin byte by construction, but I did not execute the mutant.
- Sentence-to-pin entailment: not proven (declared limit, QUALITY 104); my self-review only. The propositions are tagged HELD / INFERENCE / UNKNOWN.
- S378, S379, S380: not in `corpus/SOURCES.md` yet; their URLs were constructed from the registration, the verifier marks them PENDING-INTEGRATION.
- Round-46 hyprlang pin: only lines 250-268 read. S324's anchor list was not checked for line 259.
- "m_numlockOn read only at 1271 / written only at 1284" is grep-level over the eight pinned files, not over the whole Hyprland tree.
- Host reads: no Hyprland internals observed; no keypress; no client delivery.

## 6. Tools and host state

- Installed/upgraded: none. No pacman, uv, npm or cargo activity. (The operator tooling rule was read in the prompt; nothing needed installing.)
- Host: only the allowed read verbs. No file in ~/.config or ~/.local/bin was written.
- Writes made: the seat's deliverable directory only (`R55ScribeEntryC/` and this report). Nothing in the lane tracked tree, no fleet-root file, no sibling lane, no shokuknow.
- Hold-out: not accessed. The C2 `fixtures/c2-holdout` path was not opened.
