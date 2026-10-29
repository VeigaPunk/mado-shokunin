# R56RevCoverage — C1 coverage-truth check at base 13f0acbe3a15da2d9c08357a576d91dcadc85273

Seat: R56RevCoverage (reviewer, leaf, no subagents). Read-only against the lane (git object reads at the base revision, plus one host read). Deliverables: this file and `.ufo/waves/round-56/w1/R56RevCoverage/` (`assigned-grep-base.txt`, `supplemental-grep-base.txt`). No tracked file, index, commit or fleet file was touched. No tool installed. Scratch dir `/fast/scratch/hyaku/mado-r56/R56RevCoverage` was created empty and removed; `/tmp` held two temp lists, removed. No hold-out path was seen or read.

## Verdict

1. **Mechanism surface uncovered at base: CONFIRMED.** No held text anywhere in `corpus/`, `tools/`, `SKILL.md`, `PROVINCE.md` names the Hyprland config watcher, `ConfigWatcher`, `m_configPaths`, inotify masks (`IN_CLOSE_WRITE`, `IN_DONT_FOLLOW`, `inotify_add_watch`), the canonical-symlink watch, `CConfigManager::reload`, `REFRESH_ALL`, or the upstream meaning of `misc:disable_autoreload`. `corpus/knowledge` count for the frozen token set `disable_autoreload|ConfigWatcher|IN_CLOSE_WRITE|inotify_add_watch` = 0, matching `receipts/before.txt`.
2. **Frozen prose is wrong on "whether".** `claims-frozen.md` §C1 says "whether and how Hyprland reloads on save was not on the corpus". The *whether* is on the corpus five times as an **unsourced premise** citing the operator skill `omarchy skill:145` (SKILL.md:112, :197-199, :477; `terminals-and-omarchy.md:131`; `config-health-report-r3.md:353`). Only the *how* is uncovered. The predicate (registration.md) is unaffected; the prose overstates. Report, not a predicate change.
3. **Source-closure leg is NOT new ground.** `corpus/knowledge/bind-table-r25.md:9-17` already holds, sourced to S162 at `legacy/ConfigManager.cpp:1816-1848`: `source =` → `absolutePath` context → `glob` with `GLOB_TILDE` → `strcoll` order → regular-file recursion via `parseFile` → directory / non-regular skip → no-match error. S162's own scope text already reads "…and reload traversal". The frozen chain's "every regular file reached by `source =`, glob and `~` rules" restates this. Only the watch-list/inotify/reload-endpoint legs are new.
4. **C1 expansion credit: honest as to mechanism ground, not as to the source-closure leg.** New ground = the watcher registration (`ConfigWatcher.cpp`, which has **no** registry row at base — grep for `ConfigWatcher` in SOURCES returns nothing), the inotify mask/symlink rules, `misc:disable_autoreload` as a watch gate, and the `CConfigManager::reload` → `REFRESH_ALL` endpoint. Re-scopes of already-registered URLs (legacy ConfigManager.cpp: S162/S303/S317/S353/S368; MiscFunctions.cpp: S182/S321; HyprCtl.cpp: S018/S158/S307) are permitted by existing multi-scope practice (round-46 note: three scopes on HyprCtl.cpp), but each new row must carry a scope the held rows do not quote (absolutePath body `MiscFunctions.cpp:61-83` qualifies; `handleSource` `1810-1850` is already held by bind-table-r25 and must be cited, not re-derived).

## Hit classification, assigned grep (base 13f0acbe)

Command (verbatim from seat spec): `git -C /home/vgpnk/Projects/shokunin/mado-shokunin grep -n -i -E 'autoreload|ConfigWatcher|inotify|IN_CLOSE_WRITE|modified, reloading|hyprctl reload|configreloaded' 13f0acbe3a15da2d9c08357a576d91dcadc85273 -- corpus tools SKILL.md PROVINCE.md`
Count: `21` lines (saved as `R56RevCoverage/assigned-grep-base.txt`). `grep -c` per file: SKILL.md 5, corpus/SOURCES.md 2, config-drift-r12 1, terminal-trees-r23 1, terminals-and-omarchy 1, walker-deep-r9 2, walker-route-r18 2, lessons/round-23 1, tools/mado-options.py 6.

| hit | class | note |
|---|---|---|
| SKILL.md:112 | passing mention, unsourced | scope table: "Hyprland 0.56.2; auto-reloads on save (omarchy skill:145)" |
| SKILL.md:201 | passing | validation pair pointer `skill:147-148` |
| SKILL.md:316 | passing / operator-only list | "`hyprctl reload` — applies config to the live session (skill:147)" |
| SKILL.md:451 | gate row | misreading refusal "Run `hyprctl reload` to validate" → mado never runs reload; premise cites skill:147 |
| SKILL.md:1646 | other plane (walker) | `inotify` = 0 count on the walker binary; not Hyprland |
| corpus/SOURCES.md:91 (S079) | other plane, sourced negative | walker v2.17.2 tarball search for watchers/reload |
| corpus/SOURCES.md:214 (S212) | sourced, consumer side | Waybar 0.15.0 registers `configreloaded` among twelve events; says nothing about Hyprland emitting it (held in `event-delivery-limits-r26`) |
| knowledge/config-drift-r12.md:67-68 | sourced read, not executed | gkeep `install.sh:88-90` invokes `hyprctl reload`; sibling project, not the watcher |
| knowledge/terminal-trees-r23.md:52 | other plane, sourced negative | ghostty C5 "no automatic reload"; mirrored at lessons/round-23.md:207 (restatement of ghostty, not Hyprland) |
| knowledge/terminals-and-omarchy.md:131 | passing pointer | "auto-reload on save `:145`" → SKILL.md; no upstream source |
| knowledge/walker-deep-r9.md:171, :319 | other plane | walker `inotify`=0, `(?i)watch`=0 |
| knowledge/walker-route-r18.md:101, :103 | other plane + `[UNK]` | walker `notify` crate; "Whether any other path watches files is `[UNK]`" |
| lessons/round-23.md:207 | other plane | ghostty C5 duplicate |
| tools/mado-options.py:1250, 1574 | tool fixture | `misc { disable_autoreload = true }` self-test config text |
| tools/mado-options.py:1406 | tool table | option name in the option list |
| tools/mado-options.py:1458 | tool assertion | `row_of("misc:disable_autoreload")`: owner `.config/hypr/hyprland.conf`, layer root (tool's own assertion, not a source) |
| tools/mado-options.py:1583, :1609 | tool fixture / assertion | live JSON `int:1`, merge agreement check |

Consequence: the tool already *names* `misc:disable_autoreload` and its owner, but no corpus text gives its semantics. The entry must not present the tool's row as sourced.

## Blind spots of the assigned pattern (found by a second grep)

Second command: `git -C … grep -n -i -E 'auto-?reload|reloadRules|REFRESH_ALL|config reload|reload on|on save|configreload' 13f0acbe… -- corpus tools SKILL.md PROVINCE.md` → 31 lines (`R56RevCoverage/supplemental-grep-base.txt`). The assigned pattern misses hyphenated `auto-reload`, bare `reload`, and `reloadRules`. Lines it misses that matter for C1:

- SKILL.md:197-199 — "Hyprland auto-reloads on config save (omarchy skill:145)": load-bearing premise of the write-boundary rule. Unsourced.
- SKILL.md:477 — instructs the editing actor "hypr auto-reload + validation pair (`:145-148`)". Unsourced pointer.
- knowledge/config-health-report-r3.md:353 — "auto-reload applies it on save; verify by checking `printenv NVD_BACKEND`". Operator recommendation, unsourced.
- **knowledge/bind-table-r25.md:9-17 — HELD, sourced (S162, `ConfigManager.cpp:1816-1848`): the `source =` handler.** Direct overlap with the chain's source-closure leg. Not one of the four named held entries, but the closest one.
- **knowledge/rule-attribution-r24.md:155 — HELD, sourced: "Named rules first" is the hyprlang reload order (`reloadRules`, `legacy/ConfigManager.cpp:946-966`).** Overlaps any text on what the reload endpoint re-registers.
- knowledge/hyprland-bind-key-match-r50.md:80 — HELD, sourced (S352, `KeybindManager.cpp:332`): "xkb state … created per config reload and never updated." Overlaps any claim about what reload rebuilds.
- knowledge/hyprland-keyboard-repeat-numlock-r55.md:26 — OPEN: whether a config reload re-applies the input options is `WHEN … [open]`; a wave-2 caller map is named, not in the base corpus as a verdict.
- knowledge/hyprland-monitor-rule-r45.md:140-145 — SOURCED scope limit: upstream commit a9902ea (2026-07-22, "config: remove legacy config support (#15539)") removes `legacy/ConfigManager.cpp`; `v0.56.2` (efb5099) predates it. The entry must pin its claims to v0.56.2 and must not extend them to current upstream.
- Other-plane matches not relevant to C1: remaining-planes-census.md:271-272 (swaybg), terminal-route-r17.md:72,146 (alacritty), output-colour-boundaries-r14.md:41 (kanshi/output), walker-deep*.md, waybar-walker-*.md.

## Must NOT claim (to avoid duplicating held entries)

- **config-era (`hyprland-config-era-r12.md`, S021-S029):** no Lua/hyprlang era statement, no 0.55 boundary, no deprecation text. The chain is legacy-provider-only at efb5099; the entry says so by pin, not by re-deriving the era. No claim that the watcher covers the Lua provider (none was read).
- **ipc-contract (`ipc-contract-r25.md`, S186/S187/S189):** no `EVENT>>DATA` framing, no 1024-char truncation, no 44-event count. Do not state that a reload emits `configreloaded` on the socket unless the entry reads the emitting call site; `configreloaded` appears in the corpus only as a Waybar subscription (S212 → `event-delivery-limits-r26`).
- **rule-attribution (`rule-attribution-r24.md`, §6):** no `reloadRules` ordering, no "named rules first", no rule re-registration story. The entry may name `REFRESH_ALL` as the endpoint and stop there.
- **input-devices (`hyprland-input-devices-r46.md`, S316-S322):** no claim about which input/device/keyboard options a reload re-applies (the r55 entry leaves that open at line 26).
- Also avoid, though not among the four: `source =` glob/skip/recursion (bind-table-r25; cite it), the xkb-state-per-reload line (bind-key-match-r50:80), and any claim that reload is observed. The host read below supports only the option value.
- Do not repeat the SKILL/terminals-and-omarchy premise "Hyprland auto-reloads on save (omarchy skill:145)" as sourced. The new entry supersedes it with a pinned upstream statement; the omarchy skill is not a pin.

## Host read (allowed reads only; nothing changed)

- `hyprctl version -j` → `"version": "0.56.2"`, `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f"`, `"dirty": false`. Matches the wave pin commit.
- `hyprctl getoption misc:disable_autoreload -j` → `{"option": "misc:disable_autoreload", "int": 0, "set": false }`.
- `grep -n -i autoreload ~/.config/hypr/*.conf` → no output (option not set in the twelve files).
- `stat ~/.config/hypr/hyprland.conf` → 1329 bytes, mtime 2026-10-17 17:02:56.

Read: auto-reload is enabled on this host by default. This is consistent with the SKILL premise on the option axis only. No save-and-observe test was run, and none is claimed.

## Defects and ambiguities found

1. `claims-frozen.md` §C1, "whether and how Hyprland reloads on save was not on the corpus" — inaccurate for *whether* (see Verdict 2). Prose, not predicate.
2. `claims-frozen.md` §C1, "Chain moved onto sourced ground" — the source-closure leg was already sourced in `bind-table-r25` (S162 "reload traversal"). Only the watcher/inotify/endpoint legs are new.
3. The assigned grep is incomplete for this surface (misses `auto-reload`, `reloadRules`, bind-key-match:80). Both greps are saved; the supplemental one is the one to use for any "uncovered" inventory.
4. S162's scope cell already advertises "reload traversal" at `:1810-1850`-adjacent code. A new row citing the same lines with a different scope is a re-scope, not a new fact; the counter's `scope:` leg cannot detect that duplication. Flag for the C1 owner, not a counter defect.
5. `tools/mado-options.py` already carries `misc:disable_autoreload` as an owned root option (test fixtures 1250/1406/1458/1574/1583/1609) with no corpus semantics behind it. Not a claim to reuse.

## Not verified

- I did not read the round-56 `fetch/` pins (S383-S390 content) or `frozen-tables.json`; that belongs to the C1 executor and the C1 counter. I did not confirm that the new rows' quotes are entailed by their propositions.
- I did not check the omarchy skill `:145` text (it is not in the lane); the claim that it says "auto-reloads on save" is taken as cited, not verified.
- I did not run the C1 counter, the C1 harness or any control. Per seat spec, the main agent runs checks.
- No live reload behaviour was observed; only the option value was read.
- Hit-level claims about other planes (walker, ghostty, kitty, alacritty) were classified from snippets, not re-read in full.

## Receipts

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56RevCoverage/assigned-grep-base.txt` (21 lines)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56RevCoverage/supplemental-grep-base.txt` (31 lines)
- Frozen-file bytes read (not edited): `.ufo/waves/round-56/claims-frozen.md`, `.ufo/waves/round-56/registration.md`, `.ufo/waves/round-56/receipts/before.txt`.

Tooling: none installed or updated.
