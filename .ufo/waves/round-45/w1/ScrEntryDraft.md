# w1/ScrEntryDraft — alternative prose for the C2 entry's three weakest parts

Seat: ScrEntryDraft (leaf; no subagent dispatch, no background jobs). Round 45, w1, 2026-10-26.
Write scope honoured: everything below lives in `.ufo/waves/round-45/w1/ScrEntryDraft/` plus this report. No tracked file was edited; the
frozen registration, counters, controls, reference tool, pins and `corpus/` were read only.

## Behavior

Drafted prose the L1 can merge into `corpus/knowledge/hyprland-monitor-rule-r45.md`, for the parts the L1 draft does not cover or covers
wrongly:

- **`§3.5 How to read a DIFFER`** (new section after §3): three mechanisms that make a running output differ from every written rule while
  the config is honoured — (a) a runtime `hyprctl keyword monitor` rule that lives in no file, (b) a wlr-output-management client's committed
  state overriding mode/position/transform/scale, (c) a requested mode the output does not offer (custom-mode attempt, then "first advertised
  mode that tests" plus a notification) — and the inverse case (d) an AGREE that is still wrong under the 1 px / 1 Hz bound.
- **`§1.5` The 60 Hz default and omarchy's commented lines**: the default bites only on a `WxH` field with no `@`; every commented example in
  `~/.config/hypr/monitors.conf` is either `preferred` or carries an explicit `@`, so the hazard is an edit of the active line, not the
  template; and on this host that edit would still report AGREE because DP-1 advertises `3440x1440@59.99Hz` inside the 1 Hz bound.
- **`§4` additions — what `monitors all -j` omits**: no rule echo (the applied rule is stored and never printed), short description only,
  advertised modes at 2 decimals vs `refreshRate` at 5, disabled outputs visible only with `all`, applied scale rather than the written one,
  and no position provenance for `auto*`.
- **Appendix**: four over-width locators in the L1 draft, each with narrower grep-verified replacements.

Every sentence carries a locator of at most 30 lines. Locators are computed by `grep -n` inside the verifier, never typed from memory.

## Gates run (this seat)

| gate | command | result |
|---|---|---|
| locator resolution | `python3 -I verify-locators.py` (seat dir) | **148 OK / 0 FAIL, exit 0** → `locators.txt` |
| no unverified locator | same run, checks L1/L2 | every locator in `sections.md` is in the verified spec and every spec entry is used |
| width bound | same run, check L0 | all ranges ≤ 30 lines and inside the pin |
| negative checks | same run, N1/N2 | JSON builder 230-289 has no rule/selector field; `HyprCtl.cpp` never names `m_activeMonitorRule` |
| host receipts | same run, H1/H2/H2b/H3 | conf lines 7,10,14,19,22,25,26 as cited; eleven advertised modes incl. `3440x1440@59.99Hz`; projection carries no serial/description |
| draft locator widths | one-off scan saved as `entry-locator-widths.txt` | 4 locators over 30 lines in `l1-draft/entry.md`; none missing or past EOF |

No C1/C2 counter was run by this seat: the prose is not the counter's object, and the counters are frozen. `TARGET_MET` is not claimed here.

## Host interaction

One allowed read: `hyprctl monitors all -j` piped into a projection that keeps `name` and `availableModes` only (`live-modes-host.txt`).
No `dispatch`, `keyword`, `reload`, `setprop`, `--batch`, `output` or `plugin`; no Wayland client of my own; no package transaction; no host
config write; no compositor or session mutation.

## Touched surfaces

- `.ufo/waves/round-45/w1/ScrEntryDraft/sections.md` — the draft (174 lines), sha256 `c86ac965c52bcea713e407bb570d6ef036d14b41deaed580a9d9e55a138dd8bd`
- `.ufo/waves/round-45/w1/ScrEntryDraft/verify-locators.py` — sha256 `182f33a27c0ac7ad07a15bff6499fb0bc4cd2a675b3e1f16a2dbb0a54321a5c0`
- `.ufo/waves/round-45/w1/ScrEntryDraft/locators.txt` — 148 checks, sha256 `adc09e2c8ca68a3083508da54156b87864a30ddcdd56b58692d8c221a74d913d`
- `.ufo/waves/round-45/w1/ScrEntryDraft/live-modes-host.txt` — sha256 `c754c4c82337876cedf404f328b7e8dfde88b9c97523e08551b8e72dc327fb12`
- `.ufo/waves/round-45/w1/ScrEntryDraft/monitors-conf-lines.txt` — sha256 `a8f4d8617f87913de84d5f3b02fb4646593d86ac02e0f01e5e632f362bdc4fb0`
- `.ufo/waves/round-45/w1/ScrEntryDraft/entry-locator-widths.txt` — sha256 `c0f9141a27b1af3b7d54ce94e05818b8fddb83a7e227113fa6ca410a056eef8d`
- `.ufo/waves/round-45/w1/ScrEntryDraft.md` — this report

## Findings

**F1 — the draft has no DIFFER-reading section, and a DIFFER has three code-level causes it cannot distinguish. SUGGESTS merging §3.5.**
A runtime keyword rule goes through `dispatchKeyword` (registered at `Hyprland-HyprCtl.cpp:2037`, dynamic flag at `:1188-1190`,
`scheduleReload` for any command containing `monitor` at `:1200-1202`) and ends in the same `monitorRuleMgr()->add(...)` a file line reaches
(`Hyprland-legacy-ConfigManager.cpp:1384`); client state overrides the chosen rule at `Hyprland-MonitorRuleManager.cpp:44-46` and
`:56-75`; and an unavailable mode becomes a custom-mode attempt at `Hyprland-Monitor.cpp:836-839` with a silent fallback to any working mode
at `:942-957`. Evidence: `locators.txt` L3 rows for each.

**F2 — the 60 Hz consequence is an edit hazard, not a template hazard, and on this host it still reads AGREE. SUGGESTS §1.5 and narrows
the draft's §6 UNK.**
Rate is assigned only when the mode field contains `@` (`Hyprland-Parser.cpp:132-136`); the default is 60 (`Hyprland-MonitorRule.hpp:46`);
`preferred` never reads the rate (`Hyprland-Monitor.cpp:773-783`). The conf's commented examples are lines 7, 14, 19, 22 (`preferred`) and
25, 26 (`@60`, `@120`) (`monitors-conf-lines.txt`). Dropping `@100` from line 10 asks 60 Hz; DP-1 advertises `3440x1440@59.99Hz`
(`live-modes-host.txt`), inside the 1 Hz bound, so the candidate loop (`Hyprland-Monitor.cpp:878-887`) lands there and every compared field
agrees. The draft's §6 says "whether the output would have run 59.99 Hz … not exercised"; the advertised list answers the *what*, so the UNK
can shrink to "the switch is not exercised".

**F3 — `monitors all -j` omits what a DIFFER needs. SUPPORTS §4 and the tool's NOT_COMPARED class.**
The dump builder prints applied values only (`Hyprland-HyprCtl.cpp:230-259`, `:260-289`); the applied rule is held in `m_activeMonitorRule`
(`Hyprland-Monitor.cpp:653`) and the string never appears in `HyprCtl.cpp` (negative check N2). `description` is the short form
(`Hyprland-HyprCtl.cpp:277`, `Hyprland-Monitor.cpp:250-256`), so a `desc:` match on the long description
(`Hyprland-Monitor.cpp:1201-1211`) is unreproducible from the dump. `availableModes` is 2-decimal (`Hyprland-HyprCtl.cpp:123-134`),
`refreshRate` 5-decimal (`:241-242`); string-comparing them manufactures DIFFERs.

**F4 — four locators in the L1 draft exceed the 30-line bound. ATTACKS `l1-draft/entry.md` lines 34, 54, 60, 62.**
Measured by `entry-locator-widths.txt`: `Hyprland-legacy-ConfigManager.cpp:1299-1343` = 45, `Hyprland-MonitorRuleManager.cpp:45-84` = 40,
`Hyprland-Monitor.cpp:784-817` = 34, `Hyprland-Monitor.cpp:997-1027` = 31. Narrow replacements (22+23, 3+20+8, 11+11, 15+17) are in the
sections.md appendix and are grep-verified in `locators.txt`.

**F5 — two draft locators do not carry their sentence's subject. ATTACKS `l1-draft/entry.md` §1 and §4.**
The comma split the §1 sentence describes is `CVarList2(std::string(args))` at `Hyprland-legacy-ConfigManager.cpp:1295`, while the sentence
cites `1345` (the three positional parse calls). The §4 claim that `all` adds disabled outputs is code-only at
`Hyprland-HyprCtl.cpp:313-321`; the wiki states it at `wiki-Monitors.md:23-26` and the pair together supports the sentence.

## Out of scope / not done

- Did not edit `l1-draft/entry.md`, the registry, the lesson, README, counters, controls, reference tool or any pin; the L1 integrates.
- Did not run `c1-r45-monitors.py`, `c2-r45-monitor-entry.py`, or any control; no claim of `TARGET_MET` is made by this seat.
- Did not fetch the pins again or verify their sha256 (taken as frozen); the pins were read from `.ufo/waves/round-45/fetch/`.
- No tools installed (no pacman, no uv/npx); nothing recorded for the tool ledger.
- No scratch directory was created; `/fast/scratch/hyaku/mado-r45/ScrEntryDraft` was never needed and does not exist, so there is nothing to
  delete.
- `monitorv2` field parsing beyond the draft's `sdr_eotf` note, and mirror-geometry comparison, were left where the draft has them.

## Known limits of this draft

- The three DIFFER causes are read from code at `efb5099`; none was exercised on the host (all three need a config or runtime change).
- The hop from `parseDynamic` to the registered `monitor` handler is Hyprlang's and is not in the pins — marked `[INF]` in the prose.
- "59.99 Hz would be chosen" follows the advertised list plus the candidate order; the switch itself is unobserved (`UNK` in §1.5).
- The omarchy line numbers are the host file's (`monitors-conf-lines.txt`), not omarchy's upstream template; this seat did not fetch the
  template, so the prose says "in `~/.config/hypr/monitors.conf`" and does not generalise to omarchy at large.
