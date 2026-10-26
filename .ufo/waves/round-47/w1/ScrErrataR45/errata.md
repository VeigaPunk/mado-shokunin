# Errata — `corpus/knowledge/hyprland-monitor-rule-r45.md` (round-47 w1, closure R4b)

Seat: ScrErrataR45. Target: the round-45 w2 entry as landed at `4d22eeb`
(`sha256 128df1bd1055fcbb09f611c48286cd013e9d8bade992f4c17e81ba0615bb9c7b`, unchanged in the lane at this
seat's run — `receipts/verify-locators.txt`). Inputs: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/CritW2Entry.md`
(F1-F4, six sentence units).

Method: every finding was re-checked against the fourteen round-45 pins (still byte-identical to
`receipts/fetch-sha256.txt`, 14/14, `receipts/pin-manifest-check.txt`) plus pins fetched this round
(`pins/`, provenance and sha256 in `receipts/PINS.md`). Every locator below was computed with `grep -n` and
is re-verified by `receipts/verify-locators.txt` (`RESULT: mismatches=0`). Quoted fragments are <= 25 words
and located; nothing was run against the host compositor.

**Nothing in the entry was edited by this seat.** The blocks in the last section are append-only errata for
the L1 to integrate.

| # | unit | CritW2Entry finding | this seat's verdict |
|---|---|---|---|
| E1 | `entry:84` | F1 mis-located veto | **CONFIRMED** — citation corrected |
| E2 | `entry:96` | F2 false provenance | **CONFIRMED** — citation replaced |
| E3 | `entry:98` | F3 wrong (INF) | **CONFIRMED** — claim corrected |
| E4 | `entry:18` | F4 unpinned | **CONFIRMED** — claim stands, pin supplied |
| E5 | `entry:106` | F4 unpinned | **CONFIRMED, stronger** — the wording is false at aquamarine v0.15.1, not merely unpinned |
| E6 | `entry:107` | F4 unpinned | **CONFIRMED** — claim stands, pin supplied, scope added with it |

No finding was refuted; there is no REFUTED block in this file.

---

## E1 — `entry:84` — the monitor-added veto is cited at the branch that returns before the emit

Landed text (line 84, `grep -n`): `that event fires only for an output whose rule enables it (Hyprland-Monitor.cpp:264 and Hyprland-Monitor.cpp:389)`

What the pins show. Lines 264-389 are inside `CMonitor::onConnect(bool noRule)` (`Hyprland-Monitor.cpp:108`):

- `:264` `if (m_enabled && !monitorRule.m_disabled) {` is the **already-enabled** path: it applies the rule
  (`:266`) and returns at `:271`, before the emit at `:389`. It cannot be the veto the sentence names.
- The veto for a disabled rule is `:275` `if (monitorRule.m_disabled) {` … `:283` `m_enabled = false;` …
  `:286` `return;` — this path never reaches `:389`.
- A fresh monitor starts disabled: `m_enabled = false;` (`Hyprland-Monitor-efb5099.hpp:357`), so an enabled
  rule falls through to `:302` `m_enabled = true;` and only then reaches the single emit site,
  `:389` `Event::bus()->m_events.monitor.added.emit(m_self.lock());` (the only `monitor.added` emit in all
  fourteen pins; `Hyprland-MonitorState.cpp:25` is the listener).

The claim itself is true; only the first locator points at the wrong branch. Corrected citation:
`Hyprland-Monitor.cpp:275-287` and `:389` (with `:302` for the enabled fall-through).

## E2 — `entry:96` — the host run is attributed to `tools/mado-monitors.py` but cites the L1 draft's receipt

Landed text (line 96): `tools/mado-monitors.py reports AGREE and verdict OK, exit 0`

What the receipts show:

- The cited file, `.ufo/waves/round-45/receipts/live-monitors-host-l1.txt`, records a run of
  `l1-draft/mado-monitors.py` (line 1) with `# tool sha256 c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be`
  (line 4). The draft file `.ufo/waves/round-45/l1-draft/mado-monitors.py` hashes to that same
  `c6ac5fc2…`, so the receipt is honest — it is simply not a receipt of the landed tool.
- The landed tool at `4d22eeb` is `sha256 2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609`
  (`git show 4d22eeb:tools/mado-monitors.py | sha256sum`; identical at base `60edb66e` and on disk now).
- Its own receipt, `.ufo/waves/round-45/receipts/live-monitors-host-r45.txt`, prints the same
  `MADO_MON_*` lines: `verdict=AGREE` (line 7), `verdict=OK` (line 8), `exit=0` (line 9), with
  `# tool sha256 2f007417…` (line 4) and the same config hash `69c9d899…` (line 3).

The sentence's substance holds; the citation is replaced with `live-monitors-host-r45.txt`.

## E3 — `entry:98` — the closeness branch is determined; the hedge is wrong

Landed text (line 98): `not proof of which branch ran`

What the source shows. The custom-mode push is guarded by three negated strict bounds
(`Hyprland-Monitor.cpp:836-837`, macro `Hyprland-macros.hpp:40`: `abs((a) - (b)) < (delta)`), with bounds
1 px / 1 px / 1 Hz (`:836-837`). The declared rule asks `3440x1440@100` (`MADO_MON_RULE` line 6 in both
receipts) and the applied mode's own rate is `99.997` (`:903`; the projected `hyprctl` dump,
`live-monitors-host-l1.txt:11`, reads `"refreshRate": 99.997`). Then:

- width 3440 vs 3440 -> `|0| < 1` true; height 1440 vs 1440 -> true; rate 99.997 vs 100.000 ->
  `|0.003| < 1` true. All three negations are false, so the `requestedModes.push_back(...)` at `:838-839`
  **cannot execute**: no custom 100 Hz mode was ever tried.
- For completeness, had it run it would be tried first (`:878` iterates `requestedModes | reverse`) and an
  accepted custom mode would set `m_refreshRate = 100.000` (`:903`), which the dump does not show.

So the requested 100 Hz did count as close; the branch is settled by source + dump, not left open. The one
residual unknown is the one the entry already records as UNK at line 100 (a rule without `@100`).

## E4 — `entry:18` — "upstream main already drops the legacy hyprlang manager" is now pinned

Landed text (line 18): `upstream main already drops the legacy hyprlang manager (Hyprland a9902ea, 2026-07-22)`

Pin (`pins/hyprland-commit-a9902ea.json`, `sha256 c33ba383…`): commit
`a9902ea65f461af868497c4e74fed798ade0b1b0`, date `2026-07-22T16:35:10Z`, message
`config: remove legacy config support (#15539)`. The commit removes `src/config/legacy/ConfigManager.cpp`
(2184 deletions; `"status": "removed"`), drops the `Legacy::CConfigManager` selection and the
`CONFIG_LEGACY` enum from `src/config/ConfigManager.cpp`, and the raw file at that commit returns
`404: Not Found` (`pins/legacy-cfg-a9902ea.txt`, 14 bytes). `pins/hyprland-main-cfg-a9902ea.cpp` contains no
occurrence of `Legacy` and instantiates only `Lua::CConfigManager` (lines 30, 33). Claim stands; a SOURCES
row is owed (the C2 seat of this wave opens S326.. for a different subject, so the L1 should assign the next
free number).

## E5 — `entry:106` — non-DRM backends build no description at all (stronger than "unpinned")

Landed text (line 106): `a Wayland or headless backend builds its description differently and is not covered`

What aquamarine v0.15.1 shows (`pins/aqua-*.cpp`, the DRM file byte-identical to the round-45 pin, `sha256 ff9b19d8…`):

- `src/backend/Wayland.cpp`: 0 occurrences of `description`; `createOutput` only names the output
  (`WAYLAND-N`, lines 168-181).
- `src/backend/Headless.cpp`: 0 occurrences of `description`; `createOutput` names it (`HEADLESS-N`,
  lines 187-200) and adds one mode.
- `src/output/Output.cpp`: 0 occurrences of `description`.
- The fields are plain default-empty strings: `name, description, make, model, serial;`
  (`include/aquamarine/output/Output.hpp:258`).
- Only DRM assigns one: `output->description = std::format("{} {} {} ({})", make, model, serial, szName);`
  (`src/backend/drm/DRM.cpp:2101`).

Hyprland copies the field at `Hyprland-Monitor.cpp:250` and builds the short description from make, model and
serial at `:255-256`; for a non-DRM output all four are empty, so both descriptions are empty — they are not
"built differently". The sentence is therefore not just unpinned: at the pinned version it is false as
worded and is replaced.

## E6 — `entry:107` — the line form is removed on main; monitor rules are not (pin + scope)

Landed text (line 107): `Upstream main has removed the hyprlang line form (Hyprland a9902ea)`

Same pin as E4. The removed file is the one that carries the `monitor` keyword handler cited by the entry's
own S303. Scope that must travel with the claim: monitor rules themselves survive — the Lua binding still
parses them (`src/config/lua/bindings/LuaBindingsConfigRules.cpp:80`,
`inline constexpr SMonitorFieldDesc MONITOR_FIELDS[] = {` feeding `CMonitorRuleParser`), and the Lua manager
still drives the rule manager (`src/config/lua/ConfigManager.cpp:809-810`). So what is removed is the
`monitor =` **grammar** ("line form"), which is exactly what the sentence says; the entry's statements about
0.56.x stay correct, and the shared field parsers of §1 still exist on main, now reached from the Lua config
container (`LuaBindingsConfigRules.cpp:20`, `#include "../../shared/monitor/Parser.hpp"`).

---

## APPEND-ONLY BLOCKS (verbatim, to be appended at the end of `corpus/knowledge/hyprland-monitor-rule-r45.md`)

```markdown
## Errata (round 47, 2026-10-26; append-only — the text above stands as landed at 4d22eeb)

- E1 — line 84, locator. The monitor-added emit is reached only by the fall-through that sets `m_enabled = true;`
  (Hyprland-Monitor.cpp:302) and fires at Hyprland-Monitor.cpp:389; the veto is the disabled branch,
  `if (monitorRule.m_disabled) {` (Hyprland-Monitor.cpp:275) through `m_enabled = false;` (:283) and `return;` (:286).
  The landed citation `Hyprland-Monitor.cpp:264` is the already-enabled path of `CMonitor::onConnect`
  (Hyprland-Monitor.cpp:108), which applies the rule and returns at :271 before the emit. Corrected citation:
  Hyprland-Monitor.cpp:275-287 and :389 (fresh pin: Hyprland-Monitor-efb5099.hpp:357, `m_enabled = false;`).
  The claim is unchanged.
- E2 — line 96, provenance. The cited receipt `.ufo/waves/round-45/receipts/live-monitors-host-l1.txt` is a run of
  `l1-draft/mado-monitors.py` (`# tool sha256 c6ac5fc2…`, line 4), not of `tools/mado-monitors.py`. The landed tool
  at 4d22eeb is sha256 2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609, and its receipt
  `.ufo/waves/round-45/receipts/live-monitors-host-r45.txt` prints the same lines (`verdict=AGREE` line 7,
  `verdict=OK` line 8, `exit=0` line 9, `# tool sha256 2f007417…` line 4). Corrected citation: that receipt.
- E3 — line 98, claim. The custom-mode push is guarded by three negated strict bounds of 1 px / 1 px / 1 Hz
  (Hyprland-Monitor.cpp:836-837; Hyprland-macros.hpp:40). With the rule at 3440x1440@100 and the applied mode at
  99.997 Hz, |99.997 - 100.000| = 0.003 < 1 and both pixel dimensions match exactly, so the push at
  Hyprland-Monitor.cpp:838-839 cannot execute: the requested 100 Hz counted as close and no custom mode was tried
  (an accepted custom mode would have set Hyprland-Monitor.cpp:903 to 100.000). The branch is determined by source
  plus dump, not open; only the UNK at line 100 remains.
- E4 — line 18, pin. "Upstream main already drops the legacy hyprlang manager" is pinned at
  a9902ea65f461af868497c4e74fed798ade0b1b0, 2026-07-22T16:35:10Z, "config: remove legacy config support (#15539)":
  it removes src/config/legacy/ConfigManager.cpp (2184 deletions) and the `Legacy`/`CONFIG_LEGACY` selection in
  src/config/ConfigManager.cpp (which now instantiates only `Lua::CConfigManager`); the raw file 404s at that
  commit. Claim stands.
- E5 — line 106, claim. At aquamarine v0.15.1 neither the Wayland nor the headless backend sets a description:
  src/backend/Wayland.cpp and src/backend/Headless.cpp contain no occurrence of the field (they set only the
  output name), src/output/Output.cpp sets none, and `name, description, make, model, serial;` are default-empty
  strings (include/aquamarine/output/Output.hpp:258); only src/backend/drm/DRM.cpp:2101 assigns one. So a
  non-DRM output reaches Hyprland-Monitor.cpp:250 with an empty description and an empty short description
  (:255-256) — the backends build none, rather than building one differently. Not observed on this host, whose
  only output is DRM. Original wording replaced by this sentence.
- E6 — line 107, pin and scope. Same commit as E4 removes the file that carries the `monitor` keyword handler
  (S303), so the `monitor =` line form is gone on main. Monitor rules are not: the Lua binding still parses them
  (src/config/lua/bindings/LuaBindingsConfigRules.cpp:80, `MONITOR_FIELDS[]` feeding `CMonitorRuleParser`) and the
  Lua manager still drives the rule manager (src/config/lua/ConfigManager.cpp:809-810). Claim stands with that
  scope.
```

## Evidence index

| artifact | what it is |
|---|---|
| `receipts/verify-locators.txt` | every pin/entry/receipt locator re-checked, `RESULT: mismatches=0`; also the sha256 of all pins |
| `receipts/pin-manifest-check.txt` | the fourteen round-45 pins on disk vs `.ufo/waves/round-45/receipts/fetch-sha256.txt`, 14/14 OK |
| `receipts/PINS.md` | URL + sha256 provenance of every pin fetched this round |
| `receipts/90d-probe.txt` | `commits/90d` returns 422 ("No commit found for SHA: 90d"); a full sha returns 200 |
| `pins/` | the pins themselves (Hyprland a9902ea and efb5099, aquamarine v0.15.1) |
| `verify.py` | the script that produced `verify-locators.txt` (re-runnable; no network) |

## Supplementary observations (not part of F1-F4)

- **S1** `entry:18` also carries `(or 90d at the latest)`. `90d` is not a resolvable Hyprland revision:
  `GET /repos/hyprwm/Hyprland/commits/90d` returns 422 `No commit found for SHA: 90d`, while a full sha returns
  200 (`receipts/90d-probe.txt`). As written the parenthetical cannot be acted on; pin a concrete revision or
  drop it.
- **S2** CritW2Entry counted `entry:106` as "unpinned"; E5 shows the defect is larger (the wording is false at
  the pinned aquamarine version). The other five units' classifications hold as CritW2Entry stated them.
- **S3** All six units sit at the line numbers CritW2Entry cited (18, 84, 96, 98, 106, 107) and the entry file is
  unchanged since `4d22eeb` (`receipts/verify-locators.txt`, entry sha256 line), so the errata apply to the
  landed text rather than to a newer revision.
