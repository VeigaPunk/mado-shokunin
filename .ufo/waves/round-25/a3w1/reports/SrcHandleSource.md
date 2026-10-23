# SrcHandleSource — pinned Hyprland source handler

## Behavior and findings

Opened `src/config/legacy/ConfigManager.cpp` at Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f` from the raw URL below. The `source` keyword is registered at line 614 and its wrapper at lines 359–368 forwards to `CConfigManager::handleSource` (lines 1802–1855).

- The handler rejects a raw path shorter than two characters. It passes `rawpath` through `absolutePath(rawpath, m_configCurrentPath)`, then calls `glob` with `GLOB_TILDE`. Thus path resolution is delegated to `absolutePath` with the current config path as context, while tilde and wildcard expansion are requested by the glob call.
- A nonzero glob result becomes an error: `GLOB_NOMATCH` is reported as “found no match”, `GLOB_ABORTED` as “read error”, and other failures as “out of memory”. A status error for a matched path also returns an inaccessible-file error.
- Each regular-file match is appended to `m_configPaths` and passed to `m_config->parseFile`. The handler sets `m_configCurrentPath` to that file while parsing it, then restores the prior value; this supplies the current-file context to nested source handling. Directories and other non-regular matches are warned about and skipped. Parse errors are accumulated and returned after the match loop.
- The exact relative-path transformation inside `absolutePath` is not defined in this file, so this report makes no stronger claim about its path arithmetic.
- No `$variable` expansion implementation appears in this file. The only literal `$` match is in an embedded example-config replacement at line 2121. Config parsing is delegated through `m_config->parse()` at line 743 and dynamic keywords through `m_config->parseDynamic()` at line 1090; this file does not establish Hyprlang variable-expansion semantics.

## Located quotes

1. `src/config/legacy/ConfigManager.cpp:1816` — “if (auto r = glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get()); r != 0) {”  
   This is the file-selection point: the source expression is resolved with current-config context and passed to glob with tilde expansion enabled.
2. `src/config/legacy/ConfigManager.cpp:1817` — “r == GLOB_NOMATCH ? "found no match" : r == GLOB_ABORTED ? "read error" : "out of memory"”  
   A missing glob match is an error rather than a silently ignored include.
3. `src/config/legacy/ConfigManager.cpp:1835` — “if (std::filesystem::is_regular_file(file_status)) {”  
   Only regular-file matches enter the parsing branch; directories and non-regular paths are skipped in the following branches.
4. `src/config/legacy/ConfigManager.cpp:1839` — “m_config->parseFile(value.c_str());”  
   Hyprland parses each regular matched file, with the current path changed to that target immediately before this call.

All four quotes were checked against the downloaded bytes after collapsing whitespace; each is at most 25 whitespace-separated words.

## Draft SOURCES row

The raw URL duplicates the URL already listed in `SOURCES.md` row S162. S162's scope is legacy window-rule callbacks, named-category reconstruction, and reload traversal; the draft below uses this source for source-file selection and path context. This URL collision should remain visible to the SOURCES census.

| S? | Hyprland v0.56.2 ConfigManager.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp | code | A | Legacy `source =` file selection, current-file path context, tilde/glob handling, and missing-file behavior | `src/config/legacy/ConfigManager.cpp:359-368,614,1802-1855` @ `efb50993780079460b0cbed1363e2166a2de1d9f`, sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b, 90963 B | Shows how the legacy handler resolves and expands source paths, chooses regular files to parse, and surfaces missing or inaccessible matches; does not define `absolutePath` internals or `$variable` semantics | mined | 2026-10-23 | on-release | corpus/knowledge/bind-table-r25.md |

## Gates, touched surfaces, and limits

- Source-open gate: fetched the pinned text file (90,963 bytes, below 2 MB); the four located quotes passed the whitespace-collapsed substring check.
- Initial fetch attempt failed with curl exit 23 because `fetch/a3w1/` did not yet exist. Created that directory and repeated the same fetch successfully.
- No C1 counter or bind resolver was run or built; no runtime behavior or C1 verdict is claimed. No product code or `corpus/` file was edited, no extra source file was opened, and no tools were installed.
- Touched surfaces: `.ufo/waves/round-25/fetch/a3w1/SrcHandleSource.bin` and this report only (plus creation of the required fetch directory).

## Commands and provenance

Raw URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp`

First attempt (exit 23; destination directory absent):

```sh
timeout 60 curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHandleSource.bin
```

Successful fetch (exit 0; no stdout):

```sh
mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1 && timeout 60 curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHandleSource.bin
```

Measurement command:

```sh
sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHandleSource.bin && wc -c -l /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHandleSource.bin
```

Observed output:

```text
9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHandleSource.bin
 2184 90963 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHandleSource.bin
```

Quote-check output:

```text
QUOTE_OK line=1816 words=13
QUOTE_OK line=1817 words=18
QUOTE_OK line=1835 words=3
QUOTE_OK line=1839 words=1
bytes=90963 lines=2184 sha256=9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b under_2MB=True
```

## Artifact paths

- Report: `.ufo/waves/round-25/a3w1/reports/SrcHandleSource.md`
- Captured source: `.ufo/waves/round-25/fetch/a3w1/SrcHandleSource.bin`
