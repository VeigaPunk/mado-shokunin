# ScrLessonGate — round-46 w1: lesson Gate, registry changes, search log

Lane `mado-shokunin`. Freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, base `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`.
Leaf seat: read-only on the lane, writes confined to `.ufo/waves/round-46/w1/ScrLessonGate/` and this report. No commit,
no dispatch, no counter run against the lane, no tool installed, no pacman.

## Delivered

`.ufo/waves/round-46/w1/ScrLessonGate/round-46.md` (112 lines, draft of `corpus/lessons/round-46.md`, three sections):

- `## Gate` — candidates considered (ten pins + the screened tree/wiki, receipts cited); Admitted: new rows S316-S325,
  each with its row URL, opened `2026-10-26`, the **computed** locator and a 3-11-word quote; the ten `GATE` lines in
  build-pos.py's exact format; eleven REJECT bullets, each with the decisive line and a flip; a held-row paragraph
  explaining why new rows and not widened held rows, with the W04 cost.
- `## Registry changes` — old→new table: SOURCES 252→262 rows, README 62→63 index rows, knowledge 62→63 files, lessons
  66→67 files, tools 13→14 files, held rows unchanged, 2 new W04 census lines.
- `## Search log` — question, where searched, identified (799 src files / 217 name-filtered / 20 symbol-bearing /
  7 out-of-tree probes), screened (29 candidates), included 10, excluded 19 (12 src + 7 probes, each named), registry
  screen (252 rows; eight held rows in eight scopes; five first-use URLs), stop rationale and re-open triggers.

`## Mistakes` deliberately absent (ScrMistakes owns it), and no other section of the final lesson is drafted here.

## Gates run (all on this draft; every one exits 0)

| check | command | result | receipt |
|---|---|---|---|
| quotes | `python3 -I .ufo/waves/round-46/w1/ScrLessonGate/quote-check.py` | exit 0, `QUOTE_CHECK: checked=10 failed=0`; per quote: normalized word-bounded occurrences = 1, present after C/C++ comment stripping, 3-11 words, receipt sha256 equal to `receipts/fetch-sha256.txt`, locators 1229 / 1119 / 272 / 113 / 769 / 782 / 41 / 12 / 435 / 67 | `w1/ScrLessonGate/quote-check.txt` |
| clause-d mechanics | `python3 -I .../gate-check.py` | exit 0, `GATE_CHECK: ids=10 failed=0 indented=0 outside=0` — one column-0 `GATE` line per cited id, receipt under `fetch/` at the pinned sha256, ≥256 B, no `GATE` line outside `## Gate`, none indented | `w1/ScrLessonGate/gate-check.txt` |
| format equality with the positive control | rebuild the ten lines from `build-pos.py`'s own `QUOTES` + the pinned bytes, diff against the draft | `GATE_FORMAT: identical=10 differing=0` | `w1/ScrLessonGate/gate-format.txt` |
| structural scan | fences / tabs / BAD_LOC / `^GATE S` count / "serial" | 0 / 0 / 0 / 10 / 0 | this report |
| freeze counts (read-only `git show`/`ls-tree`) | SOURCES rows, README index rows, knowledge, lessons, tools | 252 (last `S315` line 264) / 62 (r45 row line 73) / 62 / 66 / 13, no `tools/mado-devices.py` | commands below |
| write scope | `git -C <lane> status --porcelain` | no tracked modification; only `?? .ufo/waves/round-46/w1/ScrLessonGate.md` and `?? .ufo/waves/round-46/w1/ScrLessonGate/` from me | — |

Counting commands behind the table: `git show 8c5434c:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`
→ 252; `git show 8c5434c:corpus/README.md | grep -cE '^\| \`knowledge/'` → 62; `grep -n hyprland-monitor-rule-r45
<README at 8c5434c>` → line 73; `git show 8c5434c:corpus/SOURCES.md | grep -n '^| S315 '` → line 264;
`git ls-tree --name-only 8c5434c corpus/lessons/ | wc -l` → 66; `… corpus/knowledge/` → 62; `… tools/` → 13.

### Screening receipts (bundled with the seat)

`w1/ScrLessonGate/search-screen.txt` §A (blobless clone at tag `v0.56.2`, `rev-parse HEAD` =
`efb50993780079460b0cbed1363e2166a2de1d9f`; 799 src files; 217 name matches; the 20 symbol-bearing files listed), §B
(7 probe URLs with HTTP codes), §C (host `hyprland.conf` exists, `hyprland.lua` absent), §D/§D2 (decisive bytes and
symbol counts of the rejected candidates), §E (the entry scope sentence quoted below and the two Lua assignments).
`w1/ScrLessonGate/registry-screen.txt` (252 rows; per-pin held ids).

## Touched surfaces

- written: `.ufo/waves/round-46/w1/ScrLessonGate/round-46.md`, `quote-check.py`, `quote-check.txt`, `gate-check.py`,
  `gate-check.txt`, `gate-format.txt`, `search-screen.txt`, `registry-screen.txt`, this report.
- read only: the lane (`corpus/SOURCES.md`, `corpus/README.md`, `corpus/lessons/round-45.md`,
  `.ufo/waves/round-46/{registration.md,receipts/*,fetch/*,l1-draft/*}`, `quality/counters/c2-r46-input-device-entry.py`,
  `SKILL.md`), the host config tree (existence checks only).
- not written: any tracked lane file, the fleet repo outside the lane, `.ufo/state/`, the jj/git index.

## Findings

1. **Integration hazard (L1 action).** `.ufo/waves/round-46/l1-draft/build-pos.py:94-98` writes
   `corpus/lessons/round-46.md` as a Gate-only positive-control file (`# round 46 (positive control draft)` plus the ten
   `GATE` lines). Running it against the lane — or pasting its lesson — would drop `## Registry changes` and
   `## Search log`. The ten lines are byte-identical to this draft's (`gate-format.txt`: identical=10 differing=0), so the
   merge is mechanical: take the entry/rows/README from a clone, write the lane lesson from this draft.
2. **Held-row widening is closed by the predicate.** `quality/counters/c2-r46-input-device-entry.py:493-496` requires a
   held row's cells 1-9 to stay byte-equal, so the new scopes on `debug/HyprCtl.cpp`, `config/legacy/ConfigManager.cpp`,
   `config/values/ConfigValues.cpp`, `helpers/MiscFunctions.cpp` and the hyprlang `config.cpp` must be new rows. The W04
   cost is exactly two duplicate-URL lines (`S317` beside `S162`/`S303`; `S320` beside `S158`/`S307`) — `S018` is a
   `github.com/.../blob/v0.56.2/...` URL (`corpus/SOURCES.md:30`), so a third HyprCtl row adds no third repeat.
3. **The entry's Lua sentence is inaccurate at the host revision** (L1 surface, not edited here). `entry.md:71` reads
   "The Lua config of later Hyprland releases is out of scope." — but the Lua manager exists at `efb50993` itself:
   `src/config/ConfigManager.cpp:33-50` selects `Lua::CConfigManager` when the main config's extension is `.lua`
   (assignments at `:36` and `:47`), otherwise `Legacy::CConfigManager`; the host has `hyprland.conf` and no
   `hyprland.lua` (`search-screen.txt` §C). It is a config-form branch at 0.56.2, not a later release. Suggested wording:
   the plane is the hyprlang form because this host's main config is `.conf`; and the `recheck:` trigger should include
   the config form — the counter's `RECHECK_RE` accepts `on-*`, so `on-lua-config` would be admissible.
4. **The semantics survive a config-form flip; the tool does not.** `src/config/lua/ConfigManager.cpp:983-1020`
   re-implements device-first-then-global over its own store, so a host that switches to `.lua` keeps the rule the entry
   describes while `tools/mado-devices.py` (a hyprlang parser) stops modelling the input. A flip is a tool miss, not a
   contract error — worth one sentence in the lesson's stop rationale (already there).
5. **Wiki main is Lua era, on record with bytes.** `content/Configuring/Keywords.md` at main → HTTP 404;
   `content/configuring/core/config.toml` and `core/config-options.md` (`hl.config({` at `:16`) exist, and
   `core/devices.md:12-16` documents per-device config as `hl.device({ name = ..., sensitivity = ... })`. The pin at
   `ecc06f3` is the last hyprlang-era statement the wiki holds (`search-screen.txt` §B, §D).
6. **Five of the ten pins are first uses of their URL** (InputManager.cpp, IKeyboard.cpp, devices/VirtualKeyboard.cpp,
   protocols/VirtualKeyboard.cpp, wiki Keywords.md); the other five repeat held URLs under new scopes
   (`w1/ScrLessonGate/registry-screen.txt`). Recorded so the census diff at integration is read as expected, not drift.

## Out of scope here

`## Mistakes` (ScrMistakes), the entry text, the rows themselves, the README row insertion, the counters, the reference
tool, the C1 fixture/generator work, SKILL/QUALITY/SCORECARD rows, round-45 closure D1-D6 and the `merge/mado/` theme
check. I ran neither PRED-C1-r46 nor PRED-C2-r46 (C2 needs the entry, which does not exist at the freeze); C2's other
seats own that measurement.

## Scratch / tools

`/fast/scratch/hyaku/mado-r46/ScrLessonGate` (blobless clone `hl` 1.4 MB `.git`, 7 probe files) — removed before
finishing. Tools installed or upgraded: none (used `git`, `curl`, `python3` only, all preinstalled).

## Artifact paths (relative to the lane root)

- `.ufo/waves/round-46/w1/ScrLessonGate/round-46.md`
- `.ufo/waves/round-46/w1/ScrLessonGate/quote-check.py`, `quote-check.txt`
- `.ufo/waves/round-46/w1/ScrLessonGate/gate-check.py`, `gate-check.txt`, `gate-format.txt`
- `.ufo/waves/round-46/w1/ScrLessonGate/search-screen.txt`, `registry-screen.txt`
- `.ufo/waves/round-46/w1/ScrLessonGate.md` (this report)

## Cross-seat item received after my yield (verbatim, unverified by this seat)

SentTool-3 (safety review) reports C1 clause r unsound as written: the selftest run uses `PATH=/usr/bin:/bin` with no
fake bin (`quality/counters/c1-r46-devices.py:375`), so a bare-name `hyprctl` during `--selftest` leaves no marker, and
any run can exec `/usr/bin/hyprctl` by absolute path with the marker absent; both shapes scored `TARGET_MET` at
nonce 46 (revs `3d96dcd`, `ef072a7`). Suggested fix: `--ro-bind` the fake `hyprctl`/`libinput`/`journalctl`/`udevadm`
over their `/usr/bin` paths and give the selftest `env_a`'s `PATH`. Second shape: `--ro-bind / /` does not block
AF_UNIX, so a scored tool could connect to the live `$XDG_RUNTIME_DIR/hypr/<sig>/.hyprland.sock`; adding `~` and
`/run/user/<uid>` to `hidden_paths()` closes it. Evidence claimed at
`.ufo/waves/round-46/w1/SentTool/evidence/clause-r-bypass-*.txt` and `.ufo/waves/round-46/w1/SentTool/findings.md`
(F1, F2).

This seat did not run PRED-C1-r46 and did not open those receipts, so nothing above is execution evidence here: it is a
routed report for the L1 and the C1 owner. Note for routing: `registration.md` §C1 is frozen, and its kill rule allows a
hole wave `w1` finding a hole *before any data commit* to re-register as v2 with a new freeze and new controls.

## Cross-seat items from ConnCrossClaim-3 (verbatim claims, unverified by this seat)

ConnCrossClaim-3 reports two C2 predicate routes that carry over from round 45 into `c2-r46-input-device-entry.py`:
`pin_ok` None-membership at `:532-534` lets a receipt whose base name is not in PINS pass the pin test, and T4 at
`:673-680` reads its cited receipts from the scored revision, so a forged revision can self-certify; it claims a forged
r45 `S316` admitted at `rev=1de0bb53`. It also states no `registration-v2.md` exists (v1 is the only citable line) and
that its F3 finds the entry's step-5 touchpad sentence has no locator of its own. Evidence claimed at
`.ufo/waves/round-46/w1/ConnCrossClaim/{report.md}`, `w1/ConnCrossClaim.md`.

Why this does not change my draft: all ten `GATE` lines name a **PINS** receipt under
`.ufo/waves/round-46/fetch/` (10/10, `w1/ScrLessonGate/gate-check.txt` prints `pin=1` for each) and distinct sha256 and
quotes, so clause d's pin test sits on the frozen names and both routes are plain misses, not admissions, for S316-S325.
The F3 locator note is the L1's entry surface, not the lesson's. I did not open ConnCrossClaim's receipts and ran no
counter, so none of this is execution evidence here.
