# Receipts — registry rows re-opened at the lane tip

Scored tree: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (lane `/home/vgpnk/Projects/shokunin/mado-shokunin`). Fetch: independent `curl` of every row URL into `/fast/scratch/hyaku/mado-r56/R56W3ScoutRows1b/fetch/`; hashes over the raw response bytes.

Second sample of attempt-1's wave-2 scouts (which fetched at `28fc86ac`); every row re-derived at the tip.

Per row: `MATCH`/`MISMATCH` for (a) bytes vs the row's anchor-cell sha256, (b) bytes vs `frozen-tables-v2.json` `c1.pin_sha256` where the row is tabled, (c) the gate quote's line number in the upstream bytes, (d) every anchor locator within the pin's line count.

## S383 — MATCH

- URL (row cell 2): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/inotify/ConfigWatcher.cpp`
- HTTP 200; bytes fetched: 4046 B (row anchor cell says 4046 B)
- sha256 fetched by me: `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c`
- sha256 in the row's anchor cell: `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/Hyprland-ConfigWatcher.cpp`): `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-ConfigWatcher.cpp"]`: `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c` — MATCH
- gate quote `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{`: located at line 34 (gate claims 34) MATCH
- anchor locators `ConfigWatcher.cpp:33-34,46,54-56,60,67,69,105`; pin line count (bytes split on \n) = 112; max locator 105; locators past EOF: none — MATCH

## S384 — MATCH

- URL (row cell 2): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/ConfigValues.cpp`
- HTTP 200; bytes fetched: 59222 B (row anchor cell says 59222 B)
- sha256 fetched by me: `a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754`
- sha256 in the row's anchor cell: `a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/Hyprland-ConfigValues.cpp`): `a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-ConfigValues.cpp"]`: `a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754` — MATCH
- gate quote `"If true, the config will not reload automatically on save."`: located at line 492 (gate claims 492) MATCH
- anchor locators `ConfigValues.cpp:492`; pin line count (bytes split on \n) = 735; max locator 492; locators past EOF: none — MATCH

## S385 — MATCH

- URL (row cell 2): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.cpp`
- HTTP 200; bytes fetched: 5139 B (row anchor cell says 5139 B)
- sha256 fetched by me: `65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b`
- sha256 in the row's anchor cell: `65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/Hyprland-PropRefresher.cpp`): `65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-PropRefresher.cpp"]`: `65f01a1a50ef05ecb1630f8fd30bbbac91029b29f6b4b6bc3f353d0bb4b2817b` — MATCH
- gate quote `if (m_propsTripped & REFRESH_CONFIG_WATCHER)`: located at line 148 (gate claims 148) MATCH
- anchor locators `PropRefresher.cpp:148-149`; pin line count (bytes split on \n) = 160; max locator 149; locators past EOF: none — MATCH

## S386 — MATCH

- URL (row cell 2): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/eventLoop/EventLoopManager.cpp`
- HTTP 200; bytes fetched: 9073 B (row anchor cell says 9073 B)
- sha256 fetched by me: `104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c`
- sha256 in the row's anchor cell: `104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/Hyprland-EventLoopManager.cpp`): `104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-EventLoopManager.cpp"]`: `104ff43a4c02fcc88e8711cade68becd3a1fe099e970e4b1306774c85dd76f7c` — MATCH
- gate quote `wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READ`: located at line 128 (gate claims 128) MATCH
- anchor locators `EventLoopManager.cpp:71,128`; pin line count (bytes split on \n) = 283; max locator 128; locators past EOF: none — MATCH

## S387 — MATCH

- URL (row cell 2): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp`
- HTTP 200; bytes fetched: 90963 B (row anchor cell says 90963 B)
- sha256 fetched by me: `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`
- sha256 in the row's anchor cell: `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/Hyprland-legacy-ConfigManager.cpp`): `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-legacy-ConfigManager.cpp"]`: `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` — MATCH
- gate quote `"source= skipping directory {}", value);`: located at line 1844 (gate claims 1844) MATCH
- anchor locators `ConfigManager.cpp:776,1070,1079-1080,1816,1835-1836,1844`; pin line count (bytes split on \n) = 2185; max locator 1844; locators past EOF: none — MATCH

## S388 — MATCH

- URL (row cell 2): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp`
- HTTP 200; bytes fetched: 29785 B (row anchor cell says 29785 B)
- sha256 fetched by me: `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9`
- sha256 in the row's anchor cell: `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/Hyprland-MiscFunctions.cpp`): `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-MiscFunctions.cpp"]`: `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9` — MATCH
- gate quote `static const char* const ENVHOME = getenv("HOME");`: located at line 65 (gate claims 65) MATCH
- anchor locators `MiscFunctions.cpp:65,68`; pin line count (bytes split on \n) = 845; max locator 68; locators past EOF: none — MATCH

## S389 — MATCH

- URL (row cell 2): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp`
- HTTP 200; bytes fetched: 97582 B (row anchor cell says 97582 B)
- sha256 fetched by me: `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`
- sha256 in the row's anchor cell: `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/Hyprland-HyprCtl.cpp`): `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-HyprCtl.cpp"]`: `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` — MATCH
- gate quote `if (COMMAND.contains("misc:disable_autoreload"))`: located at line 1223 (gate claims 1223) MATCH
- anchor locators `HyprCtl.cpp:1223,1276`; pin line count (bytes split on \n) = 2347; max locator 1276; locators past EOF: none — MATCH

## S390 — MATCH

- URL (row cell 2): `https://man7.org/linux/man-pages/man7/inotify.7.html`
- HTTP 200; bytes fetched: 44066 B (row anchor cell says 44066 B)
- sha256 fetched by me: `79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd`
- sha256 in the row's anchor cell: `79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/man7-inotify.7.html`): `79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["man7-inotify.7.html"]`: `79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd` — MATCH
- gate quote `File opened for writing was closed.`: located at line 186 (gate claims 186) MATCH
- anchor locators `inotify.7.html:186,262`; pin line count (bytes split on \n) = 920; max locator 262; locators past EOF: none — MATCH

## S391 — MATCH

- URL (row cell 2): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/supplementary/propRefresher/PropRefresher.hpp`
- HTTP 200; bytes fetched: 1322 B (row anchor cell says 1322 B)
- sha256 fetched by me: `37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0`
- sha256 in the row's anchor cell: `37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/Hyprland-PropRefresher.hpp`): `37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-PropRefresher.hpp"]`: `(row not tabled in frozen table)` — MATCH
- gate quote `REFRESH_CONFIG_WATCHER     = (1 << 8),`: located at line 18 (gate claims 18) MATCH
- anchor locators `PropRefresher.hpp:18,21`; pin line count (bytes split on \n) = 41; max locator 21; locators past EOF: none — MATCH

## S392 — MATCH

- URL (row cell 2): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/inotify/ConfigWatcher.cpp`
- HTTP 200; bytes fetched: 4046 B (row anchor cell says 4046 B)
- sha256 fetched by me: `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c`
- sha256 in the row's anchor cell: `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/Hyprland-ConfigWatcher.cpp`): `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-ConfigWatcher.cpp"]`: `8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c` — MATCH
- anchor locators `ConfigWatcher.cpp:106`; pin line count (bytes split on \n) = 112; max locator 106; locators past EOF: none — MATCH

## S393 — MATCH

- URL (row cell 2): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp`
- HTTP 200; bytes fetched: 29785 B (row anchor cell says 29785 B)
- sha256 fetched by me: `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9`
- sha256 in the row's anchor cell: `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/Hyprland-MiscFunctions.cpp`): `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-MiscFunctions.cpp"]`: `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9` — MATCH
- anchor locators `MiscFunctions.cpp:66`; pin line count (bytes split on \n) = 845; max locator 66; locators past EOF: none — MATCH

## S394 — MATCH

- URL (row cell 2): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp`
- HTTP 200; bytes fetched: 97582 B (row anchor cell says 97582 B)
- sha256 fetched by me: `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`
- sha256 in the row's anchor cell: `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/Hyprland-HyprCtl.cpp`): `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-HyprCtl.cpp"]`: `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` — MATCH
- anchor locators `HyprCtl.cpp:1190`; pin line count (bytes split on \n) = 2347; max locator 1190; locators past EOF: none — MATCH

## S395 — MATCH

- URL (row cell 2): `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp`
- HTTP 200; bytes fetched: 90963 B (row anchor cell says 90963 B)
- sha256 fetched by me: `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`
- sha256 in the row's anchor cell: `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` — MATCH
- sha256 of the committed pin blob at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (`.ufo/waves/round-56/fetch/Hyprland-legacy-ConfigManager.cpp`): `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` — MATCH
- frozen-tables-v2.json `c1.pin_sha256["Hyprland-legacy-ConfigManager.cpp"]`: `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` — MATCH
- anchor locators `ConfigManager.cpp:630,1838,2134`; pin line count (bytes split on \n) = 2185; max locator 2134; locators past EOF: none — MATCH

