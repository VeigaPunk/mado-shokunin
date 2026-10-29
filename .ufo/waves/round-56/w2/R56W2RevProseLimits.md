# R56W2RevProseLimits — prose audit of `corpus/knowledge/hyprland-config-autoreload-r56.md` at 28fc86ac

Seat: R56W2RevProseLimits (wave w2, falsify). Read-only. No lane file edited; no git mutation; no host write; no reload, keyword, or `hyprctl` state change. Scratch `/fast/scratch/hyaku/mado-r56/R56W2RevProseLimits/` removed before yield. Tools installed: none (stdlib `python3 -I`, `git`, `curl` read-only fetches of upstream files and man7.org).

Sections audited: Scope; Chain steps 1–9; Limits; How to verify. Axes per assignment: (1) UNKNOWN vs pins and fact vs pin; (2) Limits on inode watches and renaming editors vs the w1 lab; (3) each read-only How-to-verify command run as written.

Receipts (this directory): `checks.py` (reproducible checker), `checks.out.txt` (its output), `how-to-verify-receipts.txt` (the How-to-verify block run verbatim, REV as written and REV pinned to 28fc86ac).

## Summary

- **Blocking the claim:** none found. Every K/H row quote, line, pin and hash reconciles, and no sentence in the audited sections contradicts a pin. The C1 predicate is mechanical and not changed by prose.
- **Weakens the claim:** 6 findings. The main one (F1) is a wrong inference in Limits about rename editors, and it omits a source-derived behaviour (no event-mask check) that the lane's own lab data makes relevant.
- **Cosmetic:** 5 findings (line citations, stale wording, command hygiene).

## Findings table

| ID | Where | Sentence / claim (as written) | What the pins, upstream or lab show | Severity | Suggested fix |
|---|---|---|---|---|---|
| F1 | Limits, "Inode-based watches" | "An editor that replaces a file by rename would leave the old inode's watch behind (inference from the man page; not observed)." | **Half wrong.** Lab `w1/R56ScoutInotifyLab/raw-output.txt:24-28` (a4, atomic save = rename over target, Hyprland's exact mask): file watch gets `IN_IGNORED` only; the kernel *removes* the watch, it is not left behind. The "left behind, live, silent" case is move-away (a6, raw:37-45, and pass-2 s4b: a write to the moved inode still fires the old wd). Separately, the entry never states that Hyprland does not read the event mask: `Hyprland-ConfigWatcher.cpp:100-107` finds the watch by `wd` and calls the callback for *any* event, no `ev->mask` check (`grep -n "ev->mask\|ev->name\|->mask" fetch/Hyprland-ConfigWatcher.cpp` → no hits). So the `IN_IGNORED` from a4 reaches `CConfigManager::reload()` (`legacy:1079-1081`). Source-derived prediction (inference, from pins): on this kernel an atomic save = one reload, and the rebuilt list re-watches the new inode. The entry's "not observed" is also stale for the kernel plane, which w1 observed. | weakens | Replace the sentence with: "replace-by-rename removes the watch (`IN_IGNORED`, lab a4); move-away leaves a live watch on the moved inode (lab a6, s4b). Hyprland never reads the event mask (`ConfigWatcher.cpp:100-107`), so `IN_IGNORED` also triggers `reload()`; that reload re-arms the watch on the new inode (inference from `legacy:1070`, `PropRefresher.cpp:148-149`; not observed in Hyprland)." Cite `man7-inotify.7.html:204-206, 307-310` (IN_IGNORED semantics, already in the pin and unused). |
| F2 | Scope, UNKNOWN list | "whether a filesystem event occurs when a config file is saved … how an editor's write (in-place, truncate, rename, atomic save) reaches the watches" listed as UNKNOWN "nothing in this entry observes it". | Partly answered by pins: K07 + K29 (`man7 …:185-186`, "File opened for writing was closed") make an in-place or truncate save produce `IN_CLOSE_WRITE` on the file watch by definition. The lab observed exactly that on kernel 7.2.11 (a1–a3). What stays open is Hyprland's reaction and the atomic-save path on Hyprland's build. The UNKNOWN is overbroad as written. | weakens | Narrow to: "UNKNOWN: whether Hyprland reloads on this host after a save; how atomic saves and move-away reach Hyprland's loop beyond the kernel plane (w1 lab covers the kernel plane only)." |
| F3 | Chain step 9 / Limits, "inference" wording | Step 9 "Together these explain why a symlink entry gets a watch on the link and a second watch on its canonical target." | The pins show the masks, not the design reason. Lab b1 (`raw-output.txt`, symlink setup) shows the `IN_DONT_FOLLOW` link watch is silent for writes through the link and the canonical watch fires. That is the consequence the entry should state. The "why" is the Hyprland authors' intent and is not in any pin. | cosmetic | Reword to "the link watch is silent for writes through the link; the canonical watch carries them (lab b1)". |
| F4 | Scope / Chain premise (not stated) | Entry never states that the chain assumes the legacy (hyprlang) config manager is the running manager on this host. | Load-bearing and not in the round-56 pins. Upstream at efb5099 (fetched, `api` tree + raw): `src/config/ConfigManager.cpp` `initConfigManager()` picks `Lua::CConfigManager` only for a `.lua` main path, otherwise `Legacy::CConfigManager`; `src/config/supplementary/jeremy/Jeremy.cpp:19-44` resolves explicit path → `HYPRLAND_CONFIG` → `hyprland.lua` → `hyprland.conf`. Host: `~/.config/hypr/hyprland.conf` present, no `*.lua` (`ls ~/.config/hypr/*.lua` → no such file). So legacy is selected. The entry only lists the Lua provider as UNKNOWN. | weakens | Add to Scope: "Premise: the legacy manager runs on this host (upstream `ConfigManager.cpp` initConfigManager; `Jeremy.cpp:19-44`; host has `hyprland.conf` and no `.lua`)." |
| F5 | Limits, "Declarations outside the pins are UNKNOWN" | Lists as UNKNOWN: `m_configPaths` declaration, `ConfigWatcher.hpp`, `getMainConfigPath`, `Supplementary::Jeremy`, hyprlang `parseFile`/source pre-processing, comment stripping, Lua provider. | Correct *relative to the round-56 pins*. Four of these are resolvable at the same tag by upstream fetch: `src/config/legacy/ConfigManager.hpp:129` (`std::vector<std::string> m_configPaths;`); `src/config/shared/inotify/ConfigWatcher.hpp` (`SInotifyWatch{int wd; std::string file;}`, no mask stored); `Jeremy.cpp:19-44`. The hyprlang items are answered by the lane's round-46 pin (see F6). | weakens | Say "UNKNOWN from the round-56 pins; resolved upstream as follows: …" or move the resolved items into Scope with their upstream lines. |
| F6 | Chain 8 Limits (runtime `source`); Chain "$VAR" bullet; Limits "not in the pins" | (a) "That `parseDynamic` then invokes the registered `handleSource` handler … is inference: `parseDynamic` is not in the pins." (b) "Whether hyprlang expands `$` before the handler runs is not in the pins: UNKNOWN." (c) hyprlang `parseFile` / comment stripping listed as UNKNOWN. | The lane's own pin `.ufo/waves/round-46/fetch/hyprlang-config.cpp` (hyprlang v0.6.8; host `systemHyprlang 0.6.8` per `host-version.json`; tool docstring says byte-identical to tag v0.6.8) answers all three: (a) `parseDynamic(command,value)` at `:1064-1068` → `parseLine(…, dynamic=true)`; handler loop at `:838-874` calls `h.func(LHS, RHS)` for an unscoped name equal to `LHS` (`:866`), so `source` reaches `handleSource`. (b) `parseLine` substitutes defined `$var` in RHS at `:737-745`, before the handler call at `:872`; undefined `$x` stays literal. (c) comment stripping `:674-704` runs before the handler. Host check: no `source` line in `~/.config/hypr/*.conf` contains `$` (`grep -n '^source.*\$' …` → none), so (b) is not exercised on this host. | weakens | Cite `round-46/fetch/hyprlang-config.cpp:669-704, 737-745, 838-874, 1064-1068` for (a)–(c), or state explicitly that the round-46 pin is out of this entry's scope. Downgrade "inference" to "shown" for (a) once cited. |
| F7 | Limits, "declared divergences" | "The watch-plan model's declared divergences (depth cap 16, bytewise glob order, `~user` forms, Lua provider, runtime keyword)". | `~user` is a v1 item removed by registration-v2 E8 and disclosed as "not a divergence" (registration-v2 §disclosure (e)). The tool docstring at this rev (`tools/mado-watchplan.py` lines 42-49) lists 7 divergences; `~user` is not among them, and the list omits (4) realpath, (5) duplicate watches, (7) hyprlang grammar. | cosmetic | Replace with the docstring's list (E8, 7 items) verbatim. |
| F8 | Chain step 3 | "`is_directory` (54; K06) selects the directory mask (56; K08 …) or the file mask (55; K07 …)". | Lines 55-56 define the masks; the selection is line 57 (`const uint32_t mask = isDirectory ? directoryMask : fileMask;`). | cosmetic | Cite 57. |
| F9 | Chain 8 | "`hyprctl reload` reaches `Config::mgr()->reload()` (line 1276; K28)". Limits: "Not checked: … the `full-reset` branch of `reloadRequest` (`Hyprland-HyprCtl.cpp:1262-1274`)". | True and pinned. The dispatch registration `registerCommand(SHyprCtlCommand{"reload", false, reloadRequest})` is at `Hyprland-HyprCtl.cpp:2028` (not cited). The `full-reset` branch is in the pin, not out of reach: it calls `Config::mgr().reset()` then `Config::initConfigManager()` and `mgr()->init()` (`:1266-1270`), which re-installs the callback (`legacy:1079`). It does not change the chain. | cosmetic | Cite `:2028`; either check `full-reset` against `legacy:1077-1087` or keep it listed as not checked (it is honest as written). |
| F10 | Limits, omitted cases | Not mentioned: symlink replaced by rename; file moved away with a write afterwards. | Lab b2 (`raw-output.txt:51-56`): rename-over the symlink path → `IN_IGNORED` on the link watch; canonical watch left on the old target. Lab s4b (pass 2): write to a moved-away inode fires the old wd. Under Hyprland these both call `reload()` (F1), and after a move-away the path is missing, so `handleSource` returns `nomatch` (`legacy:1816-1820`) and the file leaves the list. | weakens | Add both to Limits as inference from the lab plus pins. |
| F11 | How to verify, header | `REV=$(git -C "$LANE" rev-parse HEAD)` | The block is written for 28fc86ac, but the command resolves HEAD. At this audit HEAD is `19be88b6` (wave-2 dispatch). The entry, frozen tables, and fetch tree are identical between 28fc86ac and HEAD (`git diff --stat 28fc86ac HEAD -- corpus/knowledge/…r56.md .ufo/waves/round-56/fetch/` → empty), so results agree today, but the command does not verify the stated revision. | cosmetic | Use `REV=28fc86ac2359ec27406d8a2c63bef82ea6e947ed`. |
| F12 | How to verify, quote spot checks | Comment: "# quote spot checks (each line must contain the frozen quote)" followed by `sed -n` prints. | The commands only print; nothing compares. A mismatch cannot make the block fail. An asserting version is in `checks.py` (42 rows, 0 failures). | weakens | Add a grep assertion per line, or point the reader to `checks.py`. |
| F13 | How to verify, counter line | `--work "$(mktemp -d)"` | Uses inherited `TMPDIR` (`/tmp`) and never removes the `mktemp` directory, against the lane scratch rule (registration-v2 E10; assignment). Not run here (needs the lane counter, out of scope). | cosmetic | Use `--work /fast/scratch/hyaku/mado-r56/<name>` and remove it after. |

## Axis 1 — UNKNOWN and fact-vs-pin

Checked every cited line range and quote against the fetch pins (42 table rows, `checks.py`); cross-checked 33 K/H rows against `frozen-tables-v2.json` and 12 pin and host hashes against `c1.pin_sha256`/`host_pin_sha256`; compared each pin with upstream raw at `efb50993…` (8 of 8 identical) and the man7 pin with the live man7.org page (identical, 44066 bytes). Each chain step was read against the pin text.

Chain statements checked and confirmed (no finding): step 1 (`ConfigValues.cpp:492`), step 2 (`ConfigWatcher.cpp:33-34`; `legacy:2133-2134`), step 3 mask lines 55-56, 60, 66-69 (only F8 on the selection line), step 4 (`EventLoopManager.cpp:127-128`, `:70-71`; `ConfigWatcher.cpp:80-111`; the `file` field is the stored path, `name` not read), step 5 (`legacy:1079-1082`), step 6 (`legacy:726-751`; `postConfigReload` `:1070`), step 7 (`PropRefresher.cpp:148-149`; `hpp:18,21`; no early return between `:55` and `:147`, checked by grep for `return` and `if`), and the path-list lifecycle (`legacy:485`, `:630`, `:731`, `:755`, `:764-786`, `:614`, `:359-369`, `:1838-1840`). Path resolution (`MiscFunctions.cpp:61-83`): every `absolutePath` branch described matches the code, including `~user/x` → `$HOME` + `user/x` and `..x` / bare `..` falling through to `curdir + '/' + RAW`. `handleSource` (`legacy:1802-1855`): every branch described matches.

Host statements: `hyprctl getoption` identical to `host-getoption.json`; `hyprctl version -j` identical to `host-version.json`; 18 `source` lines; live `hyprland.conf:13` holds the theme line; `envs.conf:3` sources `gum.env.conf`, which is a regular file; no `source` target is a symlink (`stat -c %F` over the 18 targets: none non-regular).

UNKNOWN labels: genuinely unknown from the round-56 pins for glob collation, `.`-prefixed glob matches, `HOME` unset, `$` before handler (but see F6, answered by round-46), `parseDynamic` (F6), and the Lua provider. Not genuinely unknown: F2 (in-place save event), F4 (legacy selection), F5 (upstream-resolvable declarations), F6 (round-46 pin).

## Axis 2 — inode/rename Limits vs the w1 lab (`w1/R56ScoutInotifyLab.md`, `raw-output.txt`)

| Entry claim | Lab (same kernel 7.2.11, Hyprland's exact masks) | Match? |
|---|---|---|
| Rename editor "would leave the old inode's watch behind" (inference, "not observed") | a4 rename-over: `IN_IGNORED` only, watch removed; follow-up write NONE. a6 move-away: silent; s4b write to moved inode fires the old wd. | **Partly.** Right for move-away (a6/s4b); wrong for replace-by-rename (a4). "Not observed" is stale for the kernel plane. → F1 |
| "One save that produces several events could call `reload()` several times (inference; no save observed)" | Each file-watch scenario a1–a4 produced exactly one event per save. | Consistent (the hedge "could" is not contradicted). Lab data supports "one per save" on this kernel; cosmetic. |
| Watch list only holds files; no parent directory watched, so a later-created target is not seen (inference) | Directory-mask lab cases c1–c5 apply only to directory watches, which the list never contains (`legacy:1843-1845` skips directories). | Consistent. |
| Lab inference: "an editor-style atomic save is invisible to the IN_CLOSE_WRITE file watch" | Lab says invisible. Source: the `IN_IGNORED` *is delivered* and `onInotifyEvent` passes it to the callback (`ConfigWatcher.cpp:100-107`, no mask check). | **Conflicts with source.** The lab's "invisible" is only true of the mask plane. The entry must not repeat it (the entry does not). |
| Symlink canonical watch carries writes through the link | b1: link watch silent, canonical fires. | Consistent. (F3) |

The lab itself does not state that Hyprland drops the mask, and it marks Hyprland's re-arm as unverified. Both are correct as far as they go; the entry's gap is that it never states the mask-free callback path at all (F1).

## Axis 3 — How to verify (read-only commands run as written)

Run verbatim (`how-to-verify-receipts.txt`); the counter line was not run (needs the lane counter, out of scope).

| Command | Works as written? | Output (decisive) |
|---|---|---|
| `git -C "$LANE" show "$REV:…frozen-tables-v2.json" \| sha256sum` | yes, both REVs | `9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2  -` = expected |
| `git -C "$LANE" ls-tree -r --name-only "$REV" -- .ufo/waves/round-56/fetch/ \| head -20` | yes | 13 paths |
| `sed -n '33,34p;54,56p;60p;67p;69p;105p'` (ConfigWatcher) | yes | 9 lines; each carries its quote (verified by `checks.py`) |
| `sed -n '776p;1816p;1835,1836p;1844p;1838p'` (legacy) | yes | 6 lines; sed prints in file order, so 1838 follows 1836 (cosmetic) |
| `sed -n '64,66p;68p'` (MiscFunctions) | yes | 4 lines |
| `sed -n '1802,1855p'` / `sed -n '61,83p'` | yes | 54 / 23 lines |
| `hyprctl getoption misc:disable_autoreload -j` | yes (read) | `{"option": "misc:disable_autoreload", "int": 0, "set": false }` |
| `hyprctl version -j \| sed -n '3p'` | yes | `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f",` |
| `stat -c '%F %n' ~/.config/hypr/hyprland.conf` | yes | `regular file /home/vgpnk/.config/hypr/hyprland.conf` |
| `grep -c '^source' ~/.config/hypr/hyprland.conf` | yes | `18` |
| `REV=$(git -C "$LANE" rev-parse HEAD)` | runs, but resolves HEAD not 28fc86ac | F11 |
| counter line (`c1-r56-autoreload-entry.py … --work "$(mktemp -d)"`) | not run (needs lane counter) | F13 for the `mktemp` |

The sed/grep lines print; they do not assert. F12.

## Null results (what I looked for and did not find)

- Event-field reads in the watcher: `grep -n "ev->mask\|ev->name\|->mask" fetch/Hyprland-ConfigWatcher.cpp` → no hits. (This is the basis of F1.)
- Other callers of the watcher's `update()`: `grep -n "watcher()" fetch/Hyprland-HyprCtl.cpp` → only line 1224. The `source` branch (`:1194-1208`) does not reschedule the watch list (the entry's inference holds).
- Upstream drift: 8 of 8 fetch pins identical to upstream raw at `efb50993`; man7 pin identical to live page.
- Registry: 39 of 39 K/E/H rows resolve to a registry row whose URL basename matches the pin file (`checks.py` output, prefix-normalized).
- `IN_Q_OVERFLOW` handling: `ConfigWatcher.cpp:80-111` has none (read in full).
- Host symlinks among the 18 `source` targets: none (`stat -c %F`).
- `$` in any `source` line of `~/.config/hypr/*.conf`: none.

## Not verified

- The counter line in How to verify (out of scope per assignment).
- Hyprland's reaction to an atomic save on this host (no save, no reload, no host write; forbidden by assignment). The F1 prediction is source-derived only.
- Upstream `Jeremy.cpp` and `ConfigManager.cpp` were fetched and read for the cited lines, not read in full.
- Glibc `glob` collation and `.`-prefix behaviour (libc, not in any pin; the entry correctly marks them UNKNOWN).
