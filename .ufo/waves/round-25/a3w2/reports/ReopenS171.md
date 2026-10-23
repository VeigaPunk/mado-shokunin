# ReopenS171 — re-open of SOURCES row S171 (Hyprland src/main.cpp)

Seat: MadoR25A3.ReopenS171 (a3w2 falsify wave). Row drafted by a3w1 seat SrcHyprlandMain (report `.ufo/waves/round-25/a3w1/reports/SrcHyprlandMain.md`); row committed at `corpus/SOURCES.md:183`.

## What I did

1. Read `corpus/SOURCES.md:183` — S171 anchor cell: `src/main.cpp:31,57-58,120-144,160-162,263-264,287-298 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:98e5752cd485378c58c2a8cb0ba89265eaea27144925ea059e5564917dd3b645, 10963 B`.
2. Fetched the URL fresh:
   `mkdir -p /fast/scratch/hyaku/mado-r25a3/reopen && timeout 30 curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/main.cpp -o /fast/scratch/hyaku/mado-r25a3/reopen/S171.bin && sha256sum .../S171.bin && wc -c .../S171.bin`
   - `98e5752cd485378c58c2a8cb0ba89265eaea27144925ea059e5564917dd3b645  /fast/scratch/hyaku/mado-r25a3/reopen/S171.bin`
   - `10963 /fast/scratch/hyaku/mado-r25a3/reopen/S171.bin`
   Both match the anchor cell exactly (hash and byte count).
3. Checked all four located quotes in the a3w1 report as whitespace-collapsed substrings of the fresh bytes at the stated lines (independent Python rerun, not trusting the report's own `True` claims):
   - Q1 `src/main.cpp:57-58` — `if (!getenv("XDG_RUNTIME_DIR")) throwError("XDG_RUNTIME_DIR is not set!");` → in stated range: True
   - Q2 `src/main.cpp:120` — `value == "-c" || value == "--config"` → True
   - Q3 `src/main.cpp:129-134` — `const auto ABS_PATH = std::filesystem::canonical(configPath); if (!std::filesystem::is_regular_file(ABS_PATH)) { throw std::runtime_error("not a regular file"); } configPath = ABS_PATH;` → True
   - Q4 `src/main.cpp:290-292` — `const auto verify = Config::mgr()->configVerifPassed(); Config::mgr().reset(); return !verify;` → True
4. Spot-checked the report's remaining line attributions against the fresh bytes (direct reads of lines 25-75, 115-170, 255-300):
   - `:31` help lists `--config FILE  -c FILE` ✓; `:38` `--verify-config  - Do not run Hyprland, only print if the config has any errors` ✓
   - `:66-67` sets `XDG_BACKEND=wayland`, `XDG_SESSION_TYPE=wayland` ✓
   - `:72` `std::string configPath;` (default-empty) ✓
   - `:120-144` `-c`/`--config` branch: assigns `configPath`, canonicalizes, rejects non-regular files, error + `return 1` on failure ✓
   - `:160-162` `--verify-config` → `verifyConfig = true` ✓
   - `:263-264` `g_pCompositor = makeUnique<CCompositor>(verifyConfig); ... m_explicitConfigPath = configPath;` ✓ (handoff)
   - `:287` `initServer(socketName, socketFd)`; `:289-292` verify return path; `:298` `startCompositor()` ✓ (verify returns before normal start)
5. Falsification probe of the teaches cell's "default config selection is outside this file": searched the fresh bytes for `hyprland.conf` and `.config/hypr` — zero hits; the only `configPath` assignments are lines 126 and 134 (explicit-path handling). The file genuinely contains no default/fallback config-path selection.

## Teaches-cell fidelity

Row teaches: "Shows explicit config-file validation and handoff plus the verify-config return path; default config selection is outside this file."

- explicit config-file validation: canonical + regular-file check with error/`return 1` (`:129-139`) ✓
- handoff: `m_explicitConfigPath = configPath` (`:264`) ✓
- verify-config return path: `initServer()` before `configVerifPassed()` → `Config::mgr().reset()` → `return !verify` (`:287-292`) ✓
- "default config selection is outside this file": supported by absence of any default-path logic in the bytes ✓

No clause overreaches the bytes; the report correctly disclaims that bind-entry instantiation during verification is not established by this file.

## Verdict

REOPEN S171: agree

## Limits

- Did not clone Hyprland or verify the commit id maps to v0.56.2 beyond the URL/anchor's internal consistency and the report's claim; the pinned blob bytes themselves match the anchor.
- Quote check is whitespace-collapsed substring at stated lines, per lane convention; no semantic compilation of the C++ was attempted.

Artifacts:
- `/fast/scratch/hyaku/mado-r25a3/reopen/S171.bin` (fresh fetch, 10963 B)
- `.ufo/waves/round-25/a3w2/reports/ReopenS171.md`

Report: .ufo/waves/round-25/a3w2/reports/ReopenS171.md
