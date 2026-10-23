# SrcBoolAndExec — source-opening report

## Findings

This is a static-source reading of Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2), not a live compositor observation.

- `src/config/legacy/ConfigManager.cpp:1676-1755` handles legacy `workspace` rules. Its `border:`, `shadow:`, `rounding:`, `decorate:`, `default:`, and `persistent:` values pass through `ParserUtils::parseInt`; the first three are assigned inverted `m_no*` fields. The handler reports a generic workspace-rule parse error when conversion fails.
- `src/config/shared/parserUtils/ParserUtils.cpp:134-149` implements that conversion. Lowercase values with prefixes `true`, `on`, or `yes` map to `1`; prefixes `false`, `off`, or `no` map to `0`. Otherwise it recognizes a `0x` value or parses a signed integer. These are prefix checks, not a strict/case-folded boolean grammar, and the integer fallback is not restricted to `0` and `1`.
- The `on-created-empty:` branch in `ConfigManager.cpp:1703-1704,1753-1755` calls `cleanCmdForWorkspace(name, value)` and stores its result as `m_onCreatedEmptyRunCmd`. `src/helpers/MiscFunctions.cpp:478-513` trims the command, constructs `workspace ` plus the resolved workspace name, and returns a bracketed inline rule plus a space plus the command. Without existing bracketed rules it creates `[workspace NAME] cmd`. With an existing bracket block it splits rules on semicolons, replaces a rule starting with `workspace` or appends one if absent, then reassembles the block. A command empty after trimming returns `nullopt`.
- Existing source row S158 already contains the pinned `HyprCtl.cpp` raw URL. Its `getWorkspaceRuleData` serializes the optional stored command as JSON field `onCreatedEmpty` (`src/debug/HyprCtl.cpp:522-548`); `workspaceRulesRequest` iterates workspace rules and the `workspacerules` command is registered at lines 613-620 and 2005. Propose appending `corpus/knowledge/workspace-rules-r27.md` to S158's `used-by` cell; no duplicate row is needed. The `ConfigManager.cpp` raw URL is likewise already row S162, so propose the same `used-by` extension there.

## Located quotes

Each excerpt below is byte-for-byte from the fetched file. A whitespace-collapsed-substring check passed for all four.

- `src/config/shared/parserUtils/ParserUtils.cpp:138` — `if (val.starts_with("true") || val.starts_with("on") || val.starts_with("yes"))` teaches that the positive aliases are recognized as lowercase prefixes.
- `src/helpers/MiscFunctions.cpp:484` — `const std::string workspaceRule = "workspace " + inWorkspaceName;` teaches how the helper forms the workspace selector text.
- `src/helpers/MiscFunctions.cpp:506` — `rules = "[" + workspaceRule + "]";` teaches how the helper brackets the generated rule when no bracketed block was supplied.
- `src/helpers/MiscFunctions.cpp:509` — `return std::optional<std::string>(rules + " " + cmd);` teaches that the helper joins the rule block and command with a literal space.

## Proposed SOURCES rows

Two new files implement the two requested details, so these are one proposed row per newly opened file. The IDs remain `S?` for the registry owner to allocate. No `SOURCES.md` edit was made.

| S? | Hyprland v0.56.2 shared integer parser — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/parserUtils/ParserUtils.cpp | code | A | Legacy workspace-rule boolean-like values routed through ParserUtils::parseInt | src/config/shared/parserUtils/ParserUtils.cpp:134-149 @ commit efb50993780079460b0cbed1363e2166a2de1d9f; sha256:86f21b761695571fc17f5a2ad68ddd30bf06d06d4d6a47ab443dc89ca511c2c0; 5902 B | Maps lowercase true/on/yes and false/off/no prefixes, handles 0x values, and falls back to signed integer parsing | mined | 2026-10-23 | on-release | corpus/knowledge/workspace-rules-r27.md |
| S? | Hyprland v0.56.2 workspace command normalizer — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp | code | A | The command string prepared for legacy on-created-empty workspace rules | src/helpers/MiscFunctions.cpp:478-513 @ commit efb50993780079460b0cbed1363e2166a2de1d9f; sha256:065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9; 29785 B | Trims the command, supplies or replaces its workspace inline rule, and emits the bracketed rule block followed by the command | mined | 2026-10-23 | on-release | corpus/knowledge/workspace-rules-r27.md |

## Commands and outcomes

Raw-source fetches (both completed without curl error; fetched files were read and measured):

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 35 prlimit --as=4000000000 -- /usr/bin/curl -fsSL --max-filesize 2000000 --connect-timeout 10 --max-time 25 https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/parserUtils/ParserUtils.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcBoolAndExec.bin

env -i PATH=/usr/bin HOME=/home/vgpnk timeout 35 prlimit --as=4000000000 -- /usr/bin/curl -fsSL --max-filesize 2000000 --connect-timeout 10 --max-time 25 https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcBoolAndExec-MiscFunctions.bin
```

Exact hash/size command:
```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- /usr/bin/bash -c 'sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcBoolAndExec.bin /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcBoolAndExec-MiscFunctions.bin; wc -lc /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcBoolAndExec.bin /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcBoolAndExec-MiscFunctions.bin'
```

Output:

- `fetch/SrcBoolAndExec.bin`: SHA-256 `86f21b761695571fc17f5a2ad68ddd30bf06d06d4d6a47ab443dc89ca511c2c0`; 150 lines, 5902 bytes.
- `fetch/SrcBoolAndExec-MiscFunctions.bin`: SHA-256 `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9`; 844 lines, 29785 bytes.

The exact whitespace-collapse check used for the four quotes was:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- /usr/bin/python3 -I -c 'from pathlib import Path; root=Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch"); cases=[("SrcBoolAndExec.bin",138,"if (val.starts_with(\"true\") || val.starts_with(\"on\") || val.starts_with(\"yes\"))"),("SrcBoolAndExec-MiscFunctions.bin",484,"const std::string workspaceRule = \"workspace \" + inWorkspaceName;"),("SrcBoolAndExec-MiscFunctions.bin",506,"rules = \"[\" + workspaceRule + \"]\";"),("SrcBoolAndExec-MiscFunctions.bin",509,"return std::optional<std::string>(rules + \" \" + cmd);")]; norm=lambda s:" ".join(s.split()); files={p:(root/p).read_bytes().decode("utf-8") for p,_,_ in cases}; results=[norm(q) in norm(files[p]) for p,_,q in cases]; [print(p+":"+str(line)+": "+("PASS" if ok else "FAIL")) for (p,line,q),ok in zip(cases,results)]; assert all(results)'
```

Outcome: all four paths printed `PASS`. A first draft of the checker had a Python `SyntaxError` before checking any quote; the corrected command above completed successfully.

The SOURCES URL search found no row for either fetched file. The pinned `HyprCtl.cpp` and `ConfigManager.cpp` URLs were already registered as S158 and S162, respectively.

## Gates, scope, and safety

- Registration was read first. No C1/C2 controls, counters, oracle, build, or tests were run; this is not gate or runtime evidence.
- No Hyprland process was started. The exact coredump count command, run before and after, returned `1338` on each run (delta `0`): `env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- /usr/bin/coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland`.
- This seat wrote only the two assigned fetch artifacts and this report. No product code or `corpus/SOURCES.md` changes, live compositor queries, or tool installs were made.

## Artifact paths

- `.ufo/waves/round-27/fetch/SrcBoolAndExec.bin`
- `.ufo/waves/round-27/fetch/SrcBoolAndExec-MiscFunctions.bin`
- `.ufo/waves/round-27/w1/reports/SrcBoolAndExec.md`
