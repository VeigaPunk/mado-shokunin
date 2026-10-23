# SrcWikiWsRules — source opener report

## Behavior and findings

Opened the hyprlang-era Hyprland wiki Workspace Rules page at the pinned `hyprwm/hyprland-wiki` commit. It documents workspace selector properties and says selectors can match only existing workspaces; the assignment form is `workspace = WORKSPACE, RULES`. Its rule table lists rule keys and types, including `gapsin:[x]` and `gapsout:[x]` as integer settings equivalent to `gaps_in` and `gaps_out`, and `on-created-empty:[c]` as a command executed once when a workspace is created empty, excluding creation by moving a window to it. These are documentation statements, not measurements of Hyprland runtime behavior.

**Opened source:** `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Workspace-Rules.md`

- Source path: `content/Configuring/Workspace-Rules.md`
- Commit: `ecc06f3b6605e453c0ad533d979fccbefff788ef`
- Fetched artifact: `.ufo/waves/round-27/fetch/SrcWikiWsRules.bin`
- SHA-256: `486143a01f908f26e55f3af2ef9c8133c20080a3c17c9ecc7a9855c65af0ab62`
- Size: 4786 bytes; 114 lines; valid UTF-8
- Relevant anchors: selectors and property grammar, lines 13–36; syntax and selector limitation, lines 38–48; examples, lines 50–56; rule keys, lines 84–101; `on-created-empty` examples, lines 103–113.

### Located quotes

Each quote below is at most 25 words. Python whitespace-collapsed substring checks against the fetched decoded bytes returned `quote_match=True` for all four.

- `content/Configuring/Workspace-Rules.md:18-19` — “Selectors have props separated by a space. No spaces are allowed inside props themselves.” This teaches the selector-property spacing rule.
- `content/Configuring/Workspace-Rules.md:47` — “workspace selectors can only match _existing_ workspaces.” This teaches the selector's existing-workspace boundary.
- `content/Configuring/Workspace-Rules.md:53` — “workspace = name:myworkspace, gapsin:0, gapsout:0” This illustrates both gap shorthand keys in one assignment.
- `content/Configuring/Workspace-Rules.md:98` — “on-created-empty:[c] | A command to be executed once a workspace is created empty” This documents the empty-workspace creation trigger for that key.

### Draft SOURCES row

The exact raw URL was searched in `corpus/SOURCES.md`; `functions.grep` returned “No matches found.” Draft row only; the registry was not edited.

| S? | Hyprland Wiki Workspace Rules — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Workspace-Rules.md | docs | A | Hyprlang-era workspace selector grammar and existing-workspace limit, assignment syntax, rule keys including gapsin and gapsout shorthand and on-created-empty | content/Configuring/Workspace-Rules.md:13-19,38-55,84-101,103-113 @ ecc06f3b6605e453c0ad533d979fccbefff788ef, sha256:486143a01f908f26e55f3af2ef9c8133c20080a3c17c9ecc7a9855c65af0ab62, 4786 B | Documents selector properties and their existing-workspace boundary, the workspace assignment form, the gap keys and their general-variable equivalents, and the on-created-empty trigger | mined | 2026-10-23 | on-release | corpus/knowledge/workspace-rules-r27.md |

## Commands and gates

Exact fetch command (the `mkdir` prepared this assigned output directory):

```sh
mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch && timeout 60 prlimit --as=4000000000 -- curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Workspace-Rules.md -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcWikiWsRules.bin
```

Outcome: command completed with no error output; the fetched file was then read. Measurement command:

```sh
sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcWikiWsRules.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcWikiWsRules.bin && wc -l /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcWikiWsRules.bin
```

Output:

```text
486143a01f908f26e55f3af2ef9c8133c20080a3c17c9ecc7a9855c65af0ab62  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcWikiWsRules.bin
4786 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcWikiWsRules.bin
114 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/fetch/SrcWikiWsRules.bin
```

The Python quote-validation call reported word counts 14, 7, 5, and 13; `quote_match=True` for each, with the same SHA-256, 4786-byte size, and 114-line count. No C1/C2 control or other gate was run; this was a source-opener assignment, not a control or data seat, and it has no scoring receipt.

## Touched surfaces, limits, and artifacts

- Created the assigned fetch artifact and this report only; no product code, counters, harness, W set, or `corpus/SOURCES.md` was changed.
- Out of scope: executing Hyprland, testing rule parsing or runtime effects, and scoring C1/C2 controls. The page is historical documentation at the pinned wiki commit and is not runtime evidence.
- Report path: `.ufo/waves/round-27/w1/reports/SrcWikiWsRules.md`
- Source artifact path: `.ufo/waves/round-27/fetch/SrcWikiWsRules.bin`
