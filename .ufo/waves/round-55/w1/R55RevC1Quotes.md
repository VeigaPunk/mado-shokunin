# R55RevC1Quotes — round 55 wave w1 report

Seat: R55RevC1Quotes (leaf; no subagents). Lane root /home/vgpnk/Projects/shokunin/mado-shokunin. Base 3b55b6e91e40f455dd56b2985e4ffc087ada92d5.
Scope: independently verify every K and H row of `.ufo/waves/round-55/frozen-tables.json` (`c1.k` 18 rows, `c1.h` 6 rows) against the committed pins in `.ufo/waves/round-55/fetch/`, and state the maximum bounded proposition each quote supports. Writes: this report, and `w1/R55RevC1Quotes/` (deliverable). No tracked-file edits, no git or jj, no commits, no host commands, no writes to the fleet root, sibling lanes or shokuknow.

## 1. What I did

1. Read `frozen-tables.json`, `claims-frozen.md` and `registration.md` (contract text, read only).
2. Created the scratch dir `/fast/scratch/hyaku/mado-r55/R55RevC1Quotes/work/` and the deliverable dir `.ufo/waves/round-55/w1/R55RevC1Quotes/`.
3. Wrote my own checker `quote_check.py` (python3 -I; did not reuse or read `freeze-verify.py`). It hashes each pin against `c1.pin_sha256`, then for each K/H row checks: the quote is a byte substring of the stated 1-indexed line; the quote occurs once in the whole file; the line count is 1; character and byte length.
4. Wrote `quote_locus.py` to record, for each row, whether the quote is the whole stripped pin line or a substring, and what text sits outside it.
5. Read the surrounding pin lines (`read` ranges) for every row whose claim depends on a neighbouring line, and grepped the fetch dir for `getDeviceInt`, `numlock_by_default`, `repeat_info`.
6. Wrote `quote-bounds.md`: one line per row, MAY / MAY NOT, and a flag.

Commands and decisive output (trimmed):

```
$ python3 -I .../work/quote_check.py      (scratch; copies in deliverable dir)
PIN HASHES (name, sha_ok, bytes, CRLF, LF):
  Hyprland-ConfigValues.cpp: sha_ok=True bytes=59222 crlf=0 lf=734
  ... (all 10 pins sha_ok=True; host-input.conf sha_ok=True bytes=1584; host-getoption.json sha_ok=True bytes=179)
ROWS: id | file | line | substring_at_line | line_occurrences_in_file | total_occurrences | char_len | byte_len
K01 | Hyprland-InputManager.cpp | 1220 | True | 1 at [1220] | 1 | 58 | 58
K04 | Hyprland-InputManager.cpp | 1282 | True | 1 at [1282] | 1 | 24 | 24
K06 | Hyprland-InputManager.cpp | 1284 | True | 1 at [1284] | 1 | 12 | 12
K17 | wayland-1.26.0-wayland.xml | 2741 | True | 1 at [2741] | 1 | 62 | 62
H06 | host-getoption.json | 3 | True | 1 at [3] | 1 | 46 | 46
... (all 24 rows: substring True, line count 1, total count 1)
FAILS: none
```

Full output: `w1/R55RevC1Quotes/quote-check.out`, and `quote-locus.out` (row-by-row locus).

## 2. Results

- Substring at the stated line: 24/24 PASS (K01–K18, H01–H06).
- Uniqueness within the file: 24/24 PASS (exactly one occurrence in the file; exactly one line containing it).
- Length: 12 to 112 characters (K06 = 12 is the shortest; K14 = 112 the longest). Byte length equals character length; all pins are ASCII-compatible LF files with no CRLF.
- Pin hashes: 10/10 match `c1.pin_sha256`.
- Quote thinness and bounds: see `quote-bounds.md` for the per-row lines. Flags: THIN K04, K05, K06, K17; COND (guard quoted, effect on an unquoted line) K09, K11, K16; PARTIAL K07 (conjunct subset), H03 (hyprlang bool mapping unpinned). The other 15 rows are OK as stated.

## 3. Defects and ambiguities (inputs that show them)

D1 — K17 cannot name its subject (THIN). The quote is `will disable any repeating (regardless of the value of delay).` at `wayland-1.26.0-wayland.xml:2741`. The sentence's subject, `A rate of zero`, ends line 2740 (`fetch/wayland-1.26.0-wayland.xml` lines 2740–2741: "Negative values for either rate or delay are illegal. A rate of zero" / "will disable any repeating (regardless of the value of delay)."). The single-line quote rule (claims-frozen.md lines 7–9) forces this split. A scribe proposition "rate zero disables key repeat" needs line 2740, which no frozen row quotes.

D2 — `getDeviceInt` is not in any frozen row (ambiguity). K01, K02, K03 and K08 all rely on `getDeviceInt` to apply the device-or-global fallback. Its definition is `fetch/Hyprland-legacy-ConfigManager.cpp:1131–1132` (`int CConfigManager::getDeviceInt(...)` / `auto val = getConfigValueSafeDevice(dev, v, fallback);`), and the fallback return is line 1120 (`return m_config->getConfigValuePtr(fallback.c_str());`). The frozen K16 quotes only the condition at 1119. The C2 contract cites the same function as 1115–1123 as its source, so the C2 model and the C1 entry would rest on unfrozen lines. Not a counter defect (the counter checks only frozen rows); an entry that states the fallback semantics needs an extra row the frozen table does not define.

D3 — the seat fan-out hop is unquoted (ambiguity). K10 (`SeatManager.cpp:177`) passes the rate to `PROTO::seat->updateRepeatInfo`. The loop that reaches each keyboard resource is `fetch/Hyprland-protocols-core-Seat.cpp:603–610` (lines 607–608: `for (auto const& k : m_keyboards) { k->repeatInfo(rate, delayMs); }`). No frozen row quotes 603–610. The registration's S379 anchor is declared as `:603-609`, which excludes the closing brace at line 610 — a minor anchor truncation. The S378 anchor `updateActiveKeyboardData :175-178` likewise stops short of the function end at 180.

D4 — guard rows without effect rows (ambiguity). K09 (`if (NUMLOCKON == 1) {`), K11 (`m_resource->version() < 4` disjunct) and K16 (`if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())`) are conditions. Their effects are on unquoted lines: numlock lock at `Hyprland-IKeyboard.cpp:124–127`, the `return;` at `Hyprland-protocols-core-Seat.cpp:443`, and the fallback return at `Hyprland-legacy-ConfigManager.cpp:1120`. A frozen-row-only entry can state the guard but not the effect.

D5 — `true` → 1 mapping is not pinned in the c1 rows (ambiguity). H03 `numlock_by_default = true` and K15 (`false` default) are only meaningful as integers if the hyprlang bool parse maps `true` → 1 and `false` → 0. The only pin for that parse is the C2 spec's round-46 pin (`hyprlang-config.cpp:259-262`), which is not in `fetch/`. The c1 rows do not carry it.

D6 — no upper clamp in the quoted code (note, not a fault). K04 and K05 are `std::max(0, …)` (floor only). The 0–200 and 0–2000 ranges are enforced at config parse (K13, K14), not in `applyConfigToKeyboard`. An entry stating a clamp to 200 or 2000 at apply time would be unsupported.

D7 — unquoted device default (note). `fetch/Hyprland-legacy-ConfigManager.cpp:532`: `m_config->addSpecialConfigValue("device", "numlock_by_default", Hyprlang::INT{0});`. This is the device-level default that the C2 "from" letters depend on. No frozen row quotes it.

## 4. Not verified / gaps

- I did not run `freeze-verify.py`, the C1/C2/C3 counters or the check-r55-controls harness (not in my assignment; the L1 runs them).
- I did not read the live host: no `~/.config/hypr/input.conf` read, no `hyprctl` call. Host rows were checked against the committed pins only, as assigned. The H04–H06 snapshot is not live.
- I did not verify the entry `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` (not in the tree of this seat's assignment, and not yet written by the integration).
- The MAY / MAY NOT lines are my reading of the quoted text and its context. They are not a mechanical entailment check; the registration says the sentence-to-pin audit is the w2 scribe and the non-author closure review.
- Hyprland pins are the tag-pinned commit `efb50993…`, fetched 2026-10-28. I did not confirm that tag against upstream beyond the frozen registration.

## 5. Hold-out and tooling

- Hold-out: I did not open `fixtures/c2-holdout/` or any hold-out path. I did not look for it. No hold-out file was touched.
- Tooling: no tools were installed or upgraded. `python3 -I` (stdlib only) was used. No pacman, uv or npm call.
- Scratch: `/fast/scratch/hyaku/mado-r55/R55RevC1Quotes/` held the checker scripts; receipts were copied to the deliverable dir first and the scratch dir was removed before yield.

## 6. Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55RevC1Quotes/quote-bounds.md` (per-row bounds, flags, summary)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55RevC1Quotes/quote-check.out` (substring, uniqueness, length, pin hashes)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55RevC1Quotes/quote-locus.out` (quote vs whole line, outside text)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55RevC1Quotes/quote_check.py` and `quote_locus.py` (my checker scripts)
- This report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55RevC1Quotes.md`

## 7. Verdict for the L1

All 24 frozen K/H rows pass the substring, uniqueness, length and pin-hash checks. Five rows (K04, K05, K06, K17 and the K09/K11/K16 guards) cannot carry their stated effect without an unfrozen line, and D2/D3 name two hops (`getDeviceInt`, seat fan-out) that no frozen row quotes. The entry must not state those effects from the frozen rows alone.
