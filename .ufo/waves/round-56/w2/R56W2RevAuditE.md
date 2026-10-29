# R56W2RevAuditE — sentence-to-pin audit of the C1 entry at 28fc86ac

Seat: R56W2RevAuditE (leaf; no subagents; no lane edit; no git mutation against the lane; `git show`/`git archive` only).
Entry: `corpus/knowledge/hyprland-config-autoreload-r56.md` at `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (scored from git objects; the working tree was not used for the entry or the counter).
Lane HEAD observed at my read: `19be88b6d6112ce618c90d10999ffac031089051` (not the `9c3ca28a` tip named in the spec). Scored 28fc86ac as instructed.
Deliverable directory: `.ufo/waves/round-56/w2/R56W2RevAuditE/` (receipts in `receipts/`). Scratch `/fast/scratch/hyaku/mado-r56/R56W2RevAuditE/` removed before yield.
Tools installed or upgraded: none. g++ 16.2.1 was already present and used for one isolated `std::string(nullptr)` test.

## Verdict

1. **Quote identity holds for all seven rows (K25-K30, E01)**: each quoted string is an exact match of its pin line at the stated line (command 1 below).
2. **Propositions**: 5 SUPPORTED (K25, K26, K28, K29, K30), 2 OVERREACH-mild (K27, E01). No row is UNSUPPORTED (false or contradicted by its pin).
3. **Prose**: one sentence is contradicted by the entry's own Limits (line 34 "nothing is patched incrementally" versus the runtime `source` append at 1836, Limits line 138). One causal explanation is an unlabelled inference (line 28). One library-behaviour claim is stated as fact (line 70). One "undefined behaviour" wording is imprecise (line 54; libstdc++ throws instead, tested).
4. **The counter does not prove the sentences (attack succeeded).** Eight single-line mutations were run through the frozen C1 counter at a scratch commit of 28fc86ac. Six planted false K-row propositions (K25-K30) and one false E01 proposition all still print `TARGET_MET`. The E01 pin line was moved to line 99 (past EOF) and still `TARGET_MET`: no counter leg reads E rows at all. This matches the registration's declared limit for propositions, but it means E rows carry `pin:line` cells that nothing checks.

## Table (row | verdict | pin lines | correction)

Pins are read from `.ufo/waves/round-56/fetch/` (byte-identical to the rev; command 2). "Surrounding function" is the enclosing function read in full.

| row | verdict | pin lines | correction |
|---|---|---|---|
| K25 | SUPPORTED | `Hyprland-MiscFunctions.cpp:65` `static const char* const ENVHOME = getenv("HOME");` (inside `absolutePath`, 61-83; the branch is `if (value[0] == '~')`, line 64) | none |
| K26 | SUPPORTED | `Hyprland-MiscFunctions.cpp:68` `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));` (in `absolutePath`, else-branch at 67) | none. Edge not claimed: if `cur` had no `/`, `find_last_of` returns npos and the whole string is kept; `cur` is always absolute here. |
| K27 | OVERREACH (mild) | `Hyprland-HyprCtl.cpp:1223` `if (COMMAND.contains("misc:disable_autoreload"))`; body is line 1224 `Config::watcher()->update();`; enclosing function `dispatchKeyword` 1160-1258 | The keyword dispatch guard tests whether COMMAND contains the misc:disable_autoreload text; when it does, the next line (1224) calls `Config::watcher()->update()`. (The row's quote does not show the body; line 1224 does.) |
| K28 | SUPPORTED | `Hyprland-HyprCtl.cpp:1276` `Config::mgr()->reload();` in `reloadRequest` 1260-1279; the `full-reset` branch (1262-1274) returns first | none |
| K29 | SUPPORTED | `man7-inotify.7.html:186` "File opened for writing was closed." (entry header `IN_CLOSE_WRITE` at 185) | none |
| K30 | SUPPORTED | `man7-inotify.7.html:262` "Don't dereference pathname if it is a symbolic link." (header `IN_DONT_FOLLOW` at 261) | none |
| E01 | OVERREACH (mild) | `Hyprland-MiscFunctions.cpp:64-66` (`if (value[0] == '~')` then `value.replace(0, 1, std::string(ENVHOME));`); `absolutePath` 61-83 has no user lookup; `grep -n getpw\|getuid\|passwd` over all pins: no match | The replace call on line 66 replaces the first byte (the `~` tested at line 64) with the HOME string; `absolutePath` (61-83) contains no user lookup, so a `~user` prefix becomes HOME followed directly by `user`. (The "not looked up" half is a negative read of the function, not shown by the quoted line.) |
| entry L26 (Chain 7) | SUPPORTED | `PropRefresher.hpp:9,18,21` (`uint16_t`, `REFRESH_CONFIG_WATCHER = 1<<8`, `REFRESH_ALL = max`); `PropRefresher.cpp:31,34,148-149` | none |
| entry L25 (Chain 6) | SUPPORTED | `legacy:726-751` (`reload`), `:731`, `:743`, `:750`; `postConfigReload` starts at 970 and contains `:1070` | none |
| entry L27 (Chain 8) | SUPPORTED | `HyprCtl.cpp:1223-1224`; `:1276`; `getReply` dispatch `:2102-2121` (non-exact `reload` reaches `reloadRequest`) | none (the full-reset caveat is in Limits) |
| entry L28 (Chain 9) | OVERREACH (unlabelled inference) | `ConfigWatcher.cpp:55,60,66-69`; `man7:261-262` | "Together these explain why…" states a purpose the pins do not state. Correction: "Lines 55, 60 and 66-69 add a watch on the link path with IN_DONT_FOLLOW and, for a symlink, a second watch on the canonical target with IN_CLOSE_WRITE. That IN_DONT_FOLLOW is the reason for the second watch is inference (not stated in the pins)." |
| entry L34 (path-list lifecycle) | OVERREACH (self-contradicted) | `legacy:776,779` (clear and refill on reset); `legacy:1836` (`emplace_back`, no clearing); Limits line 138 says the runtime `source` keyword reaches the same handler and appends | "nothing is patched incrementally" is contradicted by the entry's own runtime-keyword bullet. Correction: "The list is cleared and refilled from nothing on every reload and verify; a runtime `source` keyword, if it reaches `handleSource`, appends to it without clearing (1836; inference, Limits)." |
| entry L45-47 (Consequences) | SUPPORTED | `legacy:1816-1820` (glob error returns before the append); `:1828-1833`; `:1836`; `ConfigWatcher.cpp:52-73` | none. The "same file is watched twice" and "target created later is not seen" sentences are correctly labelled inference. |
| entry L54 (`~` bullet) | SUPPORTED (wording) | `MiscFunctions.cpp:64-66`; `legacy:1816` (glob receives the already-replaced string; GLOB_TILDE never sees a leading `~`) | "undefined behaviour" at line 66 for null HOME is the standard's precondition on `std::string(const char*)`. Tested in scratch: g++ 16.2.1 / libstdc++ throws `std::logic_error: basic_string: construction from null is not valid`. Correction: "If HOME is unset, `getenv` returns null and `std::string(ENVHOME)` violates the standard's precondition (undefined behaviour); libstdc++ 16.2.1 throws `std::logic_error` instead; what Hyprland then does is not in the pins." |
| entry L56-60 (`./`, `../`, other dot names, bare names, curdir) | SUPPORTED | `MiscFunctions.cpp:68-79` (each branch as described; `..` alone and `..x` both fall to line 77) | none |
| entry L64-66 (resolution base) | SUPPORTED | `legacy:736,756,1837-1840`; `:2146` | none |
| entry L70 (glob semantics) | OVERREACH (cosmetic) | `legacy:1816` (flags `GLOB_TILDE` only; no `GLOB_NOSORT`) | "so the match order is the C library's collation" is glibc behaviour outside the pins; the same paragraph says the pins do not show it. Correction: prefix with "(inference, library behaviour not in the pins)". |
| entry L138 (Limits, runtime source) | SUPPORTED | `HyprCtl.cpp:1194-1208` contains no `watcher()` call (grep: the only `Config::watcher()` in HyprCtl.cpp is 1224); `legacy:1836` | none |
| entry L140 (Limits, divergences) | SUPPORTED | `registration-v2.md` E8 wording; `tools/mado-watchplan.py` docstring (line 42-49) does not mention `~user` | none |

## Commands and output (decisive lines)

1. Quote identity at rev (K25-K30, E01), Python over `git show 28fc86ac…:.ufo/waves/round-56/fetch/<pin>`:
```
K25 Hyprland-MiscFunctions.cpp:65 exact=True contains=True
K26 Hyprland-MiscFunctions.cpp:68 exact=True contains=True
K27 Hyprland-HyprCtl.cpp:1223 exact=True contains=True
K28 Hyprland-HyprCtl.cpp:1276 exact=True contains=True
K29 man7-inotify.7.html:186 exact=True contains=True
K30 man7-inotify.7.html:262 exact=True contains=True
E01 Hyprland-MiscFunctions.cpp:66 (awk line 66 = `        value.replace(0, 1, std::string(ENVHOME));`) exact
```
2. Worktree copies vs rev (all 13 pin files used for reading): `SAME` for every file (ConfigValues, ConfigWatcher, EventLoopManager, HyprCtl, MiscFunctions, PropRefresher.cpp/.hpp, legacy ConfigManager, host-*, man7-inotify).
3. Counter at rev: `MADO_AUTORELOAD_ENTRY: rev=28fc86ac… rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none`, rc 0 (receipts/c1-counter-28fc86.out).
4. Mutation matrix (receipts/mutation-matrix.out, driver receipts/mutate-c1-counter.py): all eight mutations rc 0, `TARGET_MET missed=none`:
   - M1 K25 prop "…getenv of the PATH variable…"; M2 K26 "…FIRST slash…"; M3 K27 "…monitor keyword text…"; M4 K28 "…Config::watcher()…"; M5 K29 "…opened for reading…"; M6 K30 "…a regular file."; M7 E01 pin line 99 (past EOF); M8 E01 prop "…the password database…".
   - Why M1 passes: shared identifiers `getenv`, `ENVHOME` survive; no number is introduced; `tok` and `num` both hold. Why M3 passes: `COMMAND` and `contains` are shared.
5. Null-HOME construction: `std::string(nullptr)` under `g++ -std=c++23` with GCC 16.2.1 → `threw: basic_string: construction from null is not valid`, rc 0 (receipts/std-string-null-test.cpp).
6. Negative searches: `grep -rn 'getpwnam\|getpwuid\|getuid\|struct passwd' fetch/*.cpp *.hpp` → only the two `getenv("HOME")` lines (65, 66 `HOME` refs). `grep -n IN_Q_OVERFLOW ConfigWatcher.cpp` → no match. `grep -n 'watcher()' HyprCtl.cpp` → line 1224 only. `grep -n resetHLConfig()` → callers 630, 731, 755.
7. Host (read only): `hyprctl getoption misc:disable_autoreload -j` → `{"option": "misc:disable_autoreload", "int": 0, "set": false }`; `grep -c '^source' ~/.config/hypr/hyprland.conf` → 18; `stat` on `~/.config/omarchy/current/theme/gum.env.conf` → regular file; `hyprland.conf` lines 4-12 under `~/.local/share/omarchy/default/hypr/`, line 13 the theme file: matches the entry's Host paragraph.

## Defects (severity)

| # | defect | input that shows it | severity |
|---|---|---|---|
| D1 | The counter passes false K-row propositions. A forged proposition that keeps one quoted identifier passes; entailment is not counted. | mutations M1-M6 above, each `TARGET_MET` | weakens the claim (declared limit; the audit is the only entailment check; this audit confirms the gap). |
| D2 | E rows are not checked by any counter leg: a wrong pin line and a false E-row proposition both pass. | M7 (E01 → line 99), M8 (E01 false prop) | weakens the claim: E01-E09 pin cells are unverified, while the Chain cites E01-E09 as sourced. |
| D3 | Path-list line 34 "nothing is patched incrementally" contradicts the entry's own Limits line 138 (runtime `source` appends at 1836). | entry line 34 vs line 138; `legacy:1836` | weakens |
| D4 | Chain line 28 gives an unlabelled causal explanation of why a symlink gets two watches. | entry line 28; `ConfigWatcher.cpp:55-69` | weakens (label as inference) |
| D5 | K27 "before it runs its body": the body is line 1224, which the row does not cite. | `HyprCtl.cpp:1223-1224` | cosmetic |
| D6 | E01 "so a ~user prefix is not looked up": a negative reading of the function, not of the quoted line. | `MiscFunctions.cpp:61-83` | cosmetic |
| D7 | Line 70 states glibc collation as fact; the pins do not show it. | `legacy:1816` | cosmetic (label as inference) |
| D8 | Line 54 says "undefined behaviour" for null HOME. Standard-correct, but on libstdc++ 16.2.1 it throws `std::logic_error` (tested). | receipts/std-string-null-test.cpp | cosmetic (precision) |

## Not verified / not run

- The C1 counter's `tok`/`num` legs were not re-derived beyond the mutation runs; the counter was run as-is at rev.
- Hyprland was not built or run. Behaviour statements are source reading (as the entry says). The glibc `glob` collation order (D7) was not executed.
- The `HOME`-unset path (D8) was tested only as `std::string(nullptr)` in isolation, not in Hyprland.
- Rows K01-K24, H01-H03, E02-E09 and the entry's other prose (Chain 1-5, Limits lines other than 138/140) were not audited; out of scope for this seat beyond the sentences listed above.
- `hyprctl keyword`, `hyprctl reload`, config writes, and any compositor state change were not performed (forbidden by the seat spec).
- The lane HEAD I observed (19be88b6) differs from the `9c3ca28a` tip named in the spec; I did not investigate why.
- Lane working tree at my final check (read-only `git diff --stat`): `corpus/knowledge/hyprland-config-autoreload-r56.md` (+7/-7) and `corpus/SOURCES.md` (+4) differ from their 28fc86ac bytes; mtime 22:31:09 on both. This seat did not write them (all entry reads were `git show` at the rev; mutations ran in a scratch clone). Every verdict above is for the 28fc86ac bytes. Whoever edits the lane tree should be told that the working-tree entry no longer matches the scored revision.
