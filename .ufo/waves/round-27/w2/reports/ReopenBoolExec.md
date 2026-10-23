# ReopenBoolExec — re-open of w1 `SrcBoolAndExec.md`

Seat: MadoR27.ReopenBoolExec, wave w2, 2026-10-23. Re-opened every source URL and quote in
`.ufo/waves/round-27/w1/reports/SrcBoolAndExec.md`: its two proposed `S?` rows (ParserUtils.cpp,
MiscFunctions.cpp) and the two used-by-extension targets it proposes to extend (S158 HyprCtl.cpp,
S162 ConfigManager.cpp), all pinned at Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2).
Method: re-fetch each URL with curl into `/fast/scratch/hyaku/mado-r27/reopen/`, compare sha256 and
byte/line count, re-locate every quote with a whitespace-collapsed substring test in python, and
re-verify every cited line-range claim against the fresh bytes.

## Fetches and hash comparison

Commands (one per file, `H=efb50993780079460b0cbed1363e2166a2de1d9f`, `R=/fast/scratch/hyaku/mado-r27/reopen`):

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 120 prlimit --as=4000000000 -- /usr/bin/curl -fsSL --max-filesize 2000000 --connect-timeout 10 --max-time 25 https://raw.githubusercontent.com/hyprwm/Hyprland/$H/src/config/shared/parserUtils/ParserUtils.cpp -o $R/ReopenBoolExec.bin
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 120 prlimit --as=4000000000 -- /usr/bin/curl -fsSL --max-filesize 2000000 --connect-timeout 10 --max-time 25 https://raw.githubusercontent.com/hyprwm/Hyprland/$H/src/helpers/MiscFunctions.cpp -o $R/ReopenBoolExec-MiscFunctions.bin
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 120 prlimit --as=4000000000 -- /usr/bin/curl -fsSL --max-filesize 2000000 --connect-timeout 10 --max-time 25 https://raw.githubusercontent.com/hyprwm/Hyprland/$H/src/debug/HyprCtl.cpp -o $R/ReopenBoolExec-HyprCtl.bin
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 120 prlimit --as=4000000000 -- /usr/bin/curl -fsSL --max-filesize 2000000 --connect-timeout 10 --max-time 25 https://raw.githubusercontent.com/hyprwm/Hyprland/$H/src/config/legacy/ConfigManager.cpp -o $R/ReopenBoolExec-ConfigManager.bin
```

All four exited 0 (no curl error, no filesize cut). `sha256sum` + `wc -lc`:

| Re-opened | fresh sha256 | fresh B/lines | claimed sha256 / B | result |
|---|---|---|---|---|
| proposed S? `ParserUtils.cpp` | `86f21b761695571fc17f5a2ad68ddd30bf06d06d4d6a47ab443dc89ca511c2c0` | 5902 B / 150 ln | `86f21b76…c511c2c0`, 5902 B, 150 ln | sha=match bytes=match |
| proposed S? `MiscFunctions.cpp` | `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9` | 29785 B / 844 ln | `06541824…0a13c1d9`, 29785 B, 844 ln | sha=match bytes=match |
| S158 `HyprCtl.cpp` | `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` | 97582 B / 2346 ln | registry S158 `798b7c6c…02b91fa`, 97582 B | sha=match bytes=match |
| S162 `ConfigManager.cpp` | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | 90963 B / 2184 ln | registry S162 `9db68cf4…f65be62b`, 90963 B | sha=match bytes=match |

## Quote re-location (whitespace-collapsed substring, python, 4/4 located at exactly the claimed lines)

Exact check (run in python):

```python
from pathlib import Path
root = Path('/fast/scratch/hyaku/mado-r27/reopen')
files = {n: (root/f).read_bytes().decode('utf-8') for n, f in
    [('ParserUtils','ReopenBoolExec.bin'), ('MiscFunctions','ReopenBoolExec-MiscFunctions.bin'),
     ('HyprCtl','ReopenBoolExec-HyprCtl.bin'), ('ConfigManager','ReopenBoolExec-ConfigManager.bin')]}
lines = {k: v.splitlines() for k, v in files.items()}
norm = lambda s: ' '.join(s.split())
quotes = [
    ('ParserUtils', 138, 'if (val.starts_with("true") || val.starts_with("on") || val.starts_with("yes"))'),
    ('MiscFunctions', 484, 'const std::string workspaceRule = "workspace " + inWorkspaceName;'),
    ('MiscFunctions', 506, 'rules = "[" + workspaceRule + "]";'),
    ('MiscFunctions', 509, 'return std::optional<std::string>(rules + " " + cmd);')]
for name, ln, q in quotes:
    hit = [i+1 for i, l in enumerate(lines[name]) if norm(q) in norm(l)]
    print(name, ln, 'PASS' if norm(q) in norm(files[name]) else 'FAIL', hit)
```

Output: all four `PASS`, each found at exactly its claimed line —
`ParserUtils.cpp` reopen line 138; `MiscFunctions.cpp` reopen lines 484, 506, 509 (fresh fetch = 1:1
with the w1 fetch, so these are simultaneously the claimed and the re-located positions; quoted as
`src/...:line` per row below in Verdicts).

## Claim re-verification (cited ranges against the fresh bytes)

- `ParserUtils.cpp:134-149` — confirmed: `parseInt` at 134; `0x` → `parseHex` 135-136; `true|on|yes`
  prefixes → 1 at 138-139; `false|off|no` → 0 at 141-142; `strToNumber<int64_t>` signed fallback
  144-149 with `std::unexpected` otherwise. Prefix checks are case-sensitive (`starts_with`), and the
  fallback is unbounded — exactly the report's characterization.
- `MiscFunctions.cpp:478-513` — confirmed: `cleanCmdForWorkspace` 478, trim 480, `workspace ` + name
  484; existing `[...]` block split on `;` (`CVarList(tmpRules, 0, ';')`, 491), rule starting with
  `workspace` replaced 495-498 else appended 501-502, reassembled 504; no-bracket path builds
  `[workspace NAME]` at 506; returns `rules + " " + cmd` at 509; `std::nullopt` when empty after trim
  at 512.
- `ConfigManager.cpp:1676-1755` — confirmed: `handleWorkspaceRules` 1676; `CHECK_OR_THROW`
  (1706-1711) returns the generic `"Failed parsing a workspace rule"`; `border:`/`shadow:`/`rounding:`
  through `ParserUtils::parseInt` into inverted `m_noBorder`/`m_noShadow`/`m_noRounding` 1731-1739;
  `decorate:`/`default:`/`persistent:` through `parseInt` non-inverted 1740-1750; `on-created-empty`
  constants 1703-1704, branch 1753-1755 calls `cleanCmdForWorkspace(name, …)` and stores
  `m_onCreatedEmptyRunCmd`. (The handler continues past 1755 — `layoutopt:`, `layout:`, … — the report
  never claims it ends there.)
- `HyprCtl.cpp` — confirmed: `getWorkspaceRuleData` 522-548 serializes `m_onCreatedEmptyRunCmd` as the
  JSON field `"onCreatedEmpty"` (541-542, spliced into the object at 544-548); `workspaceRulesRequest`
  613 iterates `getAllWorkspaceRules()` 617-620; single registration
  `registerCommand(SHyprCtlCommand{"workspacerules", true, workspaceRulesRequest})` at 2005.

## Used-by extension applicability (checked 2026-10-23)

- S158 used-by cell (corpus/SOURCES.md:170) is `corpus/knowledge/rule-attribution-r24.md,
  corpus/knowledge/animation-table-r26.md` — `corpus/knowledge/workspace-rules-r27.md` absent, so the
  proposed append is still applicable.
- S162 used-by cell (corpus/SOURCES.md:174) is `rule-attribution-r24.md, bind-table-r25.md,
  animation-table-r26.md` — absent there too; applicable.
- `grep -i 'ParserUtils|MiscFunctions'` over corpus/SOURCES.md: no matches — the report's claim that
  no existing row covers either URL holds; both proposed `S?` rows remain needed (IDs still
  unallocated, as the report states).
- `corpus/knowledge/workspace-rules-r27.md` does not exist yet in the lane — the used-by extension
  names a file other seats will create; nothing to reconcile now.

## Verdicts

```
REOPEN https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/parserUtils/ParserUtils.cpp sha=match quotes=1/1 located (line 138) — agree
REOPEN https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp sha=match quotes=3/3 located (lines 484, 506, 509) — agree
REOPEN S158 https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp sha=match quotes=0/0 (no formal quotes; every cited line claim re-verified) — agree
REOPEN S162 https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp sha=match quotes=0/0 (no formal quotes; every cited line claim re-verified) — agree
```

## Findings by severity

- HIGH: none.
- MEDIUM: none.
- LOW (phrasing only): the w1 sentence "the `workspacerules` command is registered at lines 613-620
  and 2005" reads as if 613-620 were a registration site; 613-620 is the `workspaceRulesRequest`
  handler's definition and its rule iteration, and 2005 is the only registration site. Cited lines do
  contain the named content; substance unaffected, no correction needed beyond this note.
- Residual risk: raw fetches are byte-identical to w1's, so line numbers can only drift if GitHub
  serves different bytes later; both the report rows and registry S158/S162 pin sha256s, making any
  drift detectable. This report re-opens sources only — no oracle, counter, or runtime evidence is
  asserted or implied.

## Safety

- No Hyprland process started; no hyprctl call of any verb; coredump count `1338` before and after,
  delta `0` (`coredumpctl list --no-pager --no-legend | grep -c /usr/bin/Hyprland`).
- No tool installs or upgrades (curl/python3/coredumpctl already present; nothing new needed).
- Writes: the four `reopen/ReopenBoolExec*.bin` artifacts under `/fast/scratch/hyaku/mado-r27/reopen/`
  and this report. No other lane file touched; no git/jj command run.
- `/fast` had 73G free before the fetches; total fetched 224232 B.

## Artifacts

- `/fast/scratch/hyaku/mado-r27/reopen/ReopenBoolExec.bin` (ParserUtils.cpp)
- `/fast/scratch/hyaku/mado-r27/reopen/ReopenBoolExec-MiscFunctions.bin`
- `/fast/scratch/hyaku/mado-r27/reopen/ReopenBoolExec-HyprCtl.bin`
- `/fast/scratch/hyaku/mado-r27/reopen/ReopenBoolExec-ConfigManager.bin`
- `.ufo/waves/round-27/w2/reports/ReopenBoolExec.md`
