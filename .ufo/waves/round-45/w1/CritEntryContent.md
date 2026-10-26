# CritEntryContent — round 45 w1, C2 draft entry vs the pins

Seat: critic. Scope: sentence-by-sentence check of `.ufo/waves/round-45/l1-draft/entry.md` against the
pinned Hyprland `efb5099` / hyprutils `v0.14.2` sources, plus the four files this seat fetched to answer
the assigned questions. **40 sentence claims adjudicated: 24 supported, 12 supported-with-defect,
3 overclaimed, 1 wrong, 0 unsourced.** Full table, evidence and corrected text:
`.ufo/waves/round-45/w1/CritEntryContent/findings.md`.

## The verdict the L1 needs

**W1 — Limits ¶3 is wrong and states a check as impossible that the dump supports.** The draft says "The
JSON carries only the short description, so a `desc:` selector that matches only the long description
cannot be checked from the dump." But the dump also carries `make`, `model`, `serial`
(`fetch/Hyprland-HyprCtl.cpp:239-241,277`) and `name`, and on the DRM backend the long description is
built from exactly those: `pins/aquamarine-DRM.cpp:2101`
`output->description = std::format("{} {} {} ({})", make, model, serial, szName);`, with `szName` the same
connector name the output is constructed from at `:2015`; Hyprland only erases commas
(`fetch/Hyprland-Monitor.cpp:250-252`, and `:254` itself calls the suffix the "parenthesized DRM node name
suffix"). Host aquamarine is `0.15.1-1` (`pacman -Q aquamarine`), the version pinned. So the long form is
reconstructible as `` `make model serial (name)` `` with commas erased; a `desc:` selector matching
long-but-not-short is the short form plus a prefix of ` (CONNECTOR)`. Corrected text is in findings.md E40.
This is the one statement a C1-style tool would act on wrongly (declaring a `desc:`-selected rule unmatched),
so it should be fixed before the entry ships.

**O1/O2 — the 1/120 scale correction is described as unconditional.** It is behind
`fetch/Hyprland-Monitor.cpp:997` `if (!*PDISABLESCALECHECKS` (`:721` = `debug:disable_scale_checks`). Both
licenses row 4 and §3 ¶2 need the gate; §3 ¶3 also omits `misc:disable_scale_notification` (`:1040`) when
it promises a notification.

**O3 — §6 ¶2 credits Hyprland's 1 Hz bound with the host agreement.** The arithmetic is right
(`|99.997−100| = 0.003 < 1`, `Hyprland-Monitor.cpp:836-837`, `pins/macros.hpp:40` = `abs(a-b) < delta`), but
the bound is not what produced the applied mode: outside the bound a custom 100 Hz mode is pushed
(`:836-839`), tried first (`:878`), rejected (`:885-886` `continue`), and the same native 99.997 Hz mode is
applied. The agreement rests on the tool's own tolerance (census `refresh_tolerance=1`). Rewrite as E36.

## Mechanical defects (a quote-grepping gate will reject these)

- **5 quotes fail a literal grep** — `quotecheck-draft.txt`: `Hyprland-legacy-ConfigManager.cpp:1345`,
  `Hyprland-MonitorRule.hpp:46`, `Hyprland-Monitor.cpp:1001`, `Hyprland-MonitorPositionController.cpp:27`,
  `Hyprland-HyprCtl.cpp:241` (four join consecutive source lines; one is a column-aligned declaration quoted
  de-spaced). Three controls pass (`hyprutils-String.cpp:59`, `Hyprland-MonitorRuleManager.cpp:38`,
  `Hyprland-Parser.cpp:134`).
- **5 locators stop short of the fact**: `ConfigManager.cpp:1345` → `:1345-1347`; `Parser.cpp:110-139` for the
  `modeline` clause → needs `:14-20`; `Parser.cpp:145-173` for the `stoi` half → needs `:145-191`;
  `RuleManager.cpp:96-106` for the built-in default → needs `:108-116`; `Monitor.cpp:819-840` for "tried
  first" → needs `:878`.
- **4 facts have no pin in the S302–S310 set**: "splits on commas" (hyprutils `VarList2.hpp:18`); "`all`
  lists every output including disabled ones" (`MonitorState.cpp:49-55,111-122`, `Monitor.cpp:264,389`);
  "the long description" (aquamarine `DRM.cpp:2015,2101`); "within 1 px and 1 Hz" as a strict bound
  (`macros.hpp:40`).

## Answers to the assigned questions

| question | answer | evidence |
|---|---|---|
| where does `m_description` come from? | aquamarine `IOutput::description`, comma-erased by Hyprland; on DRM it is `make model serial (connector)` | `Hyprland-Monitor.cpp:250-252`; `aquamarine-DRM.cpp:2015,2101` |
| is it "long or short" in `desc:`? | yes, both, prefix match on the trimmed selector | `Hyprland-Monitor.cpp:1204,1206` |
| `all` vs default list | `all` → `m_realMonitors`, every output added before the enabled check, so disabled ones included; default → `m_monitors`, enabled non-mirror only (the `added` event fires inside the enabled guard) | `MonitorState.cpp:50,54,111-122,22-33`; `Monitor.cpp:264,389`; `HyprCtl.cpp:320-327`; blank-entry guard `HyprCtl.cpp:225` (`m_id == -1` unreachable for a real output, id assigned at `MonitorState.cpp:111`) |
| explicit position applied as written — later clamp/overlap fix? | no clamp: `moveTo` assigns directly; overlap is only logged + notified, never repaired; the tail of `arrange()` writes XWayland offsets only | `Monitor.cpp:1725`; `MonitorLayoutController.cpp:38-51`; `MonitorPositionController.cpp:27-29,101-110` |
| "falls back to its default scale" | correct only for a written scale with no clean divisor: error overlay + `getDefaultScale()`; the auto-scale case rounds instead | `Monitor.cpp:1029-1035`; auto path `:990` |
| `monitorv2` after every `monitor =` line | after the whole `m_config->parse()` returns, not per line; replacement via erase-by-name | `ConfigManager.cpp:743,747`; `MonitorRuleManager.cpp:38` |
| is the 1 Hz closeness bound what accepted 0.003 Hz? | no — same mode applied either way (see O3) | `Monitor.cpp:836-839,878-889,903` |

## Pins added (sha256 in `w1/CritEntryContent/PIN-SHA256.txt`)

`MonitorState.cpp` @efb5099 `b5033be7…`, `aquamarine-DRM.cpp` v0.15.1 `ff9b19d8…`, `aquamarine-Output.cpp`
v0.15.1 `bb9351ba…` (control: no description assignment), `macros.hpp` @efb5099 `b62d5140…`, `Math.hpp`
@efb5099 `26e71b8b…` (control: no `DELTALESSTHAN`), `VarList2.hpp/.cpp` v0.14.2 `0e484df5…`/`b8cacea7…`,
`MonitorLayoutController.cpp` @efb5099 `0190e749…`. All under
`.ufo/waves/round-45/w1/CritEntryContent/pins/`.

## Tools

No installs (no pacman, no uv, no npx): `curl`, `python3`, `grep` already present were sufficient.
No compositor writes, no git/jj mutation, no writes outside this seat's directory and this report file.
Scratch `/fast/scratch/hyaku/mado-r45/CritEntryContent` removed after copying receipts.

## Receipts

`findings.md` (table + defect detail), `quote-verdicts.txt` (70/70 review quotes grep-verified with line
numbers), `quotecheck-draft.txt` (5 draft quotes fail / 3 controls pass), `quotecheck.txt`+`.sh`,
`QUOTES.tsv`, `PIN-SHA256.txt`.
