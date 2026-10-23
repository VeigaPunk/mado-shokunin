# ReopenWiki — re-open report for SrcWikiWsRules (w1)

Item: `MadoR27.ReopenWiki` (re-open seat, leaf; no subagents).
Source report re-opened: `.ufo/waves/round-27/w1/reports/SrcWikiWsRules.md` (60 lines; 1 draft SOURCES row,
1 source URL, 4 located quotes).

## Re-fetch

Per the re-open contract, the URL was re-fetched with curl into the assigned re-open output path.

```sh
mkdir -p /fast/scratch/hyaku/mado-r27/reopen && timeout 60 prlimit --as=4000000000 -- curl -fsSL \
  https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Workspace-Rules.md \
  -o /fast/scratch/hyaku/mado-r27/reopen/ReopenWiki.bin
```

Artifact: `/fast/scratch/hyaku/mado-r27/reopen/ReopenWiki.bin`
- sha256: `486143a01f908f26e55f3af2ef9c8133c20080a3c17c9ecc7a9855c65af0ab62`
- bytes: 4786; lines: 114; valid UTF-8

The w1 report's row (`SrcWikiWsRules.bin`): sha256 `486143a01f908f26e55f3af2ef9c8133c20080a3c17c9ecc7a9855c65af0ab62`, 4786 B, 114 lines.
**Both sha256 and byte count match.**

### Commit pin verification

The short pin in registration (hyprlang-era wiki pin `hyprwm/hyprland-wiki ecc06f3b6605`) and the report's full
commit `ecc06f3b6605e453c0ad533d979fccbefff788ef` were resolved through the GitHub API
(`https://api.github.com/repos/hyprwm/hyprland-wiki/commits/ecc06f3b6605e453c0ad533d979fccbefff788ef`):
the API returns exactly `ecc06f3b6605e453c0ad533d979fccbefff788ef` (committer date 2026-04-20T16:33:26Z,
commit message "Configuring/Variables: move vfr to debug: section (#1432)"). The pinned commit is the one the
report cites.

## Quote re-location

Python whitespace-collapsed substring checks against the fetched decoded bytes (regex: every whitespace run in
the quote collapses to `\s+`; line numbers from match offsets in the raw text). All four quotes match and sit at
exactly the line ranges the w1 report named:

| # | Report location | Re-opened location | Words | Substring |
|---|---|---|---|---|
| 1 | `content/Configuring/Workspace-Rules.md:18-19` | lines 18–19 | 14 | True |
| 2 | `content/Configuring/Workspace-Rules.md:47` | line 47 | 7 | True |
| 3 | `content/Configuring/Workspace-Rules.md:53` | line 53 | 5 | True |
| 4 | `content/Configuring/Workspace-Rules.md:98` | line 98 | 13 | True |

Quote texts verified verbatim:
1. "Selectors have props separated by a space. No spaces are allowed inside props themselves."
2. "workspace selectors can only match _existing_ workspaces."
3. "workspace = name:myworkspace, gapsin:0, gapsout:0"
4. "on-created-empty:[c] | A command to be executed once a workspace is created empty"

## Row / used-by extension check

The draft SOURCES row's used-by line ranges were sanity-checked against the fetched page content:

- `:13-19` — "### Workspace selectors" heading and the selector-property spacing rule (lines 13–19) ✓
- `:38-55` — syntax block (`workspace = WORKSPACE, RULES`, line 41), existing-workspace limitation (line 47),
  and the examples block (lines 52–56) ✓
- `:84-101` — the Rules table: `gapsin:[x]`/`gapsout:[x]` int entries "equivalent to General->gaps_in/gaps_out"
  (lines 90–91) and `on-created-empty:[c]` (line 98) ✓
- `:103-113` — "### Example Rules" block incl. `on-created-empty` usage (lines 111–112) ✓

No other rows or URLs exist in the w1 report. All documented statements (selector grammar, assignment syntax,
gap shorthand keys, on-created-empty trigger) are present in the fetched pinned page.

## Verdict

`REOPEN https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Workspace-Rules.md sha=match quotes=4/4 located — agree`

## Verification gaps / residual risk

- The w1 report's `commit` and `sha256` fields and the row's anchor ranges are fully confirmed against the live
  raw file at the pinned commit. No discrepancy found.
- This is documentation re-opening only; no runtime/measurement claims (C1/C2, oracle, Hyprland) were exercised or
  scored — out of scope for a re-open seat.
- No Hyprland instance was started; no coredump delta applies. No tools were installed (curl used).
