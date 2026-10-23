# SrcHyprlandMain — Hyprland startup source opening

## Behavior and findings

Opened `src/main.cpp` at commit `efb50993780079460b0cbed1363e2166a2de1d9f` (Hyprland v0.56.2).

- The help lists `--config FILE` and `-c FILE`; the argument parser accepts either, takes the next argument as `configPath`, canonicalizes it with `std::filesystem::canonical`, and rejects it unless it resolves to a regular file. A bad path prints an error and returns 1 (`src/main.cpp:31,120-144`). This is filesystem canonicalization, not shell `~` expansion.
- `configPath` starts as an empty string (`:72`). The `-c`/`--config` branch assigns it; after constructing `CCompositor`, main assigns that value to `m_explicitConfigPath` (`:263-264`). This file does not show the fallback/default config lookup when no explicit path is supplied; it passes the still-empty value onward.
- `--verify-config` sets `verifyConfig` (`:160-162`). Main constructs `CCompositor(verifyConfig)`, hands off the config path, calls `initServer()`, then checks `Config::mgr()->configVerifPassed()`, resets the config manager, and returns `!verify` (`:263-264,287-293`). The normal `startCompositor()` call is later (`:298`); the help describes verification as not running Hyprland and printing config errors (`:38`). `main.cpp` does not establish whether bind entries are instantiated during config initialization, so this source alone cannot support a claim that verification skips bind setup. It does show that `initServer()` is called before the verify return.
- A nested launch with `-c` still requires `XDG_RUNTIME_DIR`: main checks it and throws before parsing any options (`:57-58`). Its selected config must also be canonicalizable and a regular file (`:129-134`). Main sets `XDG_BACKEND=wayland` and `XDG_SESSION_TYPE=wayland` itself (`:65-67`); `-c` does not bypass the runtime-directory check or the compositor initialization path.

## Located quotes

1. `src/main.cpp:57-58` — “`if (!getenv("XDG_RUNTIME_DIR")) throwError("XDG_RUNTIME_DIR is not set!");`” This establishes the runtime-directory precondition for any launch, including one that supplies `-c`.
2. `src/main.cpp:120` — “`value == "-c" || value == "--config"`” This identifies the two parsed config-file option spellings.
3. `src/main.cpp:129-134` — “`const auto ABS_PATH = std::filesystem::canonical(configPath); if (!std::filesystem::is_regular_file(ABS_PATH)) { throw std::runtime_error("not a regular file"); } configPath = ABS_PATH;`” This shows the explicit path must resolve to a regular file and is handed on in canonical form.
4. `src/main.cpp:290-292` — “`const auto verify = Config::mgr()->configVerifPassed(); Config::mgr().reset(); return !verify;`” This shows the verification result is returned after resetting the config manager, before the later normal compositor start call.

The four quotes were checked against the fetched UTF-8 bytes by Python after collapsing whitespace; each collapsed quote was a substring (`True`). Each quote is under 25 words.

## Draft SOURCES row

| S? | Hyprland src/main.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/main.cpp | code | A | Hyprland v0.56.2 startup option parsing, config-path handoff, and verify-config flow | src/main.cpp:31,57-58,120-144,160-162,263-264,287-298 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:98e5752cd485378c58c2a8cb0ba89265eaea27144925ea059e5564917dd3b645, 10963 B | Shows explicit config-file validation and handoff plus the verify-config return path; default config selection is outside this file | mined | 2026-10-23 | on-release | corpus/knowledge/bind-table-r25.md |

## Duplicate check

Read the existing S153–S168 rows in `corpus/SOURCES.md` and searched the full registry for this exact raw URL. No match was found; this URL does not duplicate an existing row. No source row was added to `corpus/SOURCES.md`.

## Gates, touched surfaces, and limits

- Fetch command: `mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1 && timeout 30 curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/main.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHyprlandMain.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHyprlandMain.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHyprlandMain.bin`
- Outcome: fetch succeeded; SHA-256 `98e5752cd485378c58c2a8cb0ba89265eaea27144925ea059e5564917dd3b645`; 10,963 bytes (below the 2 MB source limit).
- Touched only the fetched source artifact and this report. No product code or corpus files changed; no package/tool install, build, test, config verification, or nested compositor launch was performed.
- Out of scope: this opening did not inspect the separate config manager's default-path or bind-table implementation, and did not execute or validate `--verify-config` behavior.

Artifacts:
- `.ufo/waves/round-25/fetch/a3w1/SrcHyprlandMain.bin`
- `.ufo/waves/round-25/a3w1/reports/SrcHyprlandMain.md`

Report: .ufo/waves/round-25/a3w1/reports/SrcHyprlandMain.md