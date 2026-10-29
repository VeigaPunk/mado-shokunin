# R56W2RevProsePath — prose audit of `corpus/knowledge/hyprland-config-autoreload-r56.md` at 28fc86ac2359ec27406d8a2c63bef82ea6e947ed

Scope: sections "The path list", "Path resolution", "Resolution base", "Glob semantics" (entry lines 30-70). Every sentence that states Hyprland behaviour is in the table. Verdicts: TRUE, TRUE-BUT-UNLABELLED-INFERENCE, FALSE, UNDECIDABLE-FROM-PINS. Read-only: no lane file, git state, fleet file, config, reload or hyprctl call touched. No tool installed or upgraded (none needed).

Sources: entry read as `git show 28fc86ac:corpus/knowledge/hyprland-config-autoreload-r56.md`; pins read as `git show 28fc86ac:.ufo/waves/round-56/fetch/<file>`. Line numbers below are the pin lines of that revision. Round-56 pins contain no hyprlang and no libc; host probes (receipts in `w2/R56W2RevProsePath/`) are labelled HOST-OBSERVED and are not pin evidence.

Pin-file key: `LEG` = Hyprland-legacy-ConfigManager.cpp; `MISC` = Hyprland-MiscFunctions.cpp; `CW` = Hyprland-ConfigWatcher.cpp; `MAN` = man7-inotify.7.html (fetch); `HL46` = `.ufo/waves/round-46/fetch/hyprlang-config.cpp` (hyprlang, tag v0.6.8 per the watch-plan docstring; its tie to Hyprland 0.56.2 is NOT pinned in round-56).

## 1. Sentence table

### The path list (entry lines 30-51)

| id | entry sentence (abridged) | verdict | deciding pin lines / evidence | correction or note |
|---|---|---|---|---|
| P01 | constructor adds main path (485) and calls resetHLConfig (630) | TRUE | LEG 485, 630 | — |
| P02 | resetHLConfig clears (776), adds main path (777-779), runs verifyConfigExists and reloadRuleConfigs (781-783) | TRUE | LEG 764-786 | — |
| P03 | resetHLConfig callers are constructor 630, reload 731, verify 755 | TRUE | grep of `resetHLConfig` in LEG: 630, 731, 755 only | — |
| P04 | list rebuilt from nothing on every reload and verify; nothing patched incrementally | TRUE | LEG: only clear is 776; appends at 485, 779, 1836; every caller clears first | — |
| P05 | `m_config->parse()` parses the main file | TRUE | LEG 743, 757 | Text read is `canonical(impl->path)` (HL46 931-944), so a symlinked main file is read through its target. Not stated; see B01. |
| P06 | each `source` keyword reaches handleSource via handler 614 and wrapper 359-369 | TRUE | LEG 359-369, 614 | Also true inside a category: `source` is unscoped and the scope test is skipped (HL46 844-867). Round-46 pin only. |
| P07 | "handleSource (legacy:1802-1855), in order:" | TRUE | LEG 1802-1855 | — |
| P08 | RAW shorter than two bytes: `bogus`, nothing added; lone `~` or `.` is bogus | TRUE | LEG 1803-1806 | — |
| P09 | glob with `GLOB_TILDE` on absolutePath(RAW, cur); any non-zero result is an error for the whole line; nothing added | TRUE | LEG 1816-1820 | HOST-OBSERVED: literal missing target gives GLOB_NOMATCH (rc 3). |
| P10 | matches processed in glob's order (1824) | TRUE | LEG 1824 | — |
| P11 | each match becomes `absolutePath(match, cur)` (1825); K21 is the append that follows | TRUE | LEG 1825, 1836 | — |
| P12 | `std::filesystem::status(value, ec)` follows symlinks (1828) | TRUE | LEG 1828; the follow semantics are C++ standard library, not pinned | HOST-OBSERVED (g++ GCC 16.2.1): status on a symlink to a regular file returns regular, on a symlink to a directory returns dir, on a dangling link returns ENOENT. Label as standard-library behaviour. |
| P13 | "If it fails, **for a missing target or a dangling symlink**, the function returns 'inaccessible' at once (1830-1833)" | **FALSE as worded** | LEG 1816-1820 returns first for a missing target (GLOB_NOMATCH), so a missing target never reaches 1828. Only a dangling symlink that glob returns reaches 1830. | HOST-OBSERVED: literal missing target gives rc=3 (NOMATCH); literal dangling link gives rc=0 and returns the link path. **Correction:** "If status fails, which for a glob result happens only for a dangling symlink (glibc returns dangling links as matches; HOST-OBSERVED), the function returns 'inaccessible' at once." |
| P14 | rest of that line's matches are not processed; failed entry not added | TRUE | LEG 1830-1833 returns before 1836 | — |
| P15 | regular file: `emplace_back(value)` (1836) runs before the file is parsed | TRUE | LEG 1835-1836, then parseFile at 1839 | — |
| P16 | `m_configCurrentPath = value` (1838), `parseFile(value)` (1839), previous cur restored (1840) | TRUE | LEG 1837-1840 | — |
| P17 | no depth check in these lines | TRUE | LEG 1835-1840 | The depth cap of 16 is the watch-plan model's, not Hyprland's (matches E8 (3)). |
| P18 | directory: warning, skipped, not added, not watched (1843-1845) | TRUE | LEG 1843-1845 | — |
| P19 | any other status (fifo, socket, device) is a warning and skip (1846-1848) | TRUE | LEG 1846-1848 | — |
| P20 | order is depth-first and pre-order; main path first | TRUE | LEG 1836 before 1839; main path first at 779 | — |
| P21 | for each `source` line in file order: matched file appended, then its nested entries, then the next line | TRUE | LEG 1816-1840; line-by-line order from HL46 1016-1040 (`parseFile`) | "file order" is HL46 round-46 behaviour; not pinned for 0.56.2. |
| P22 | within one line the glob order decides | TRUE | LEG 1824 | Depends on G02. |
| P23 | **No deduplication.** `emplace_back` at 1836 has no membership test, so a file reached twice is listed twice | TRUE | LEG 1836; no membership test in 1802-1855 or 2133-2134 | — |
| P24 | "setWatchList adds one watch per entry (52-73), so **the same file is watched twice**" | **FALSE at kernel level; TRUE at `m_watches` level** | CW 52-73 adds one `m_watches` entry per path (no test; confirmed by reading). MAN lines 90-92 ("inotify_add_watch ... either creates a new watch item, or modifies an existing watch") and 296-302 ("multiple paths may refer to the same inode ... may clobber existing watch masks") decide that a second add on one inode modifies the existing watch. | HOST-OBSERVED: `inotify_add_watch` on the same inode returned wd 1 three times; a second `inotify_rm_watch(1)` returned -1 EINVAL, and CW 45-47 does not check it. **Correction:** "setWatchList records the same file in `m_watches` twice; the kernel holds one watch for that inode with the same descriptor, and the second add modifies it. The duplicate `rm_watch` fails with EINVAL, unchecked (CW 45-47)." |
| P25 | "A missing source target never enters the list. The nomatch return at 1816-1820 comes before the append at 1836." | TRUE | LEG 1816-1820 before 1836 | Also true for a dangling symlink (1830-1833 before 1836). HOST-OBSERVED rc=3 for missing literal. |
| P26 | only `m_configPaths` entries are watched; no parent directory is ever watched; a target created after the parse is not seen (inference) | TRUE-BUT-UNLABELLED-INFERENCE (the last clause is labelled inference; the first two clauses are pinned) | CW 34 (only `getConfigPaths()`); LEG 1843-1845 (directories not added) | Exception to "no parent directory": the main path is added unconditionally (779) and a directory there gets a directory mask (CW 54-57). The inference is labelled and correct as an inference; no event observed. |
| P27 | symlink to a regular file enters the list under the link path; `value` is not resolved; watches are the link watch and the canonical watch | TRUE | LEG 1828, 1836 (value is the glob spelling); CW 60, 65-72 (second watch on canonical with `.file = path`) | HOST-OBSERVED: glob returns the link spelling (link.conf); two kernel watches, wd 2 on the link inode and wd 1 on the target. |
| P28 | symlink to a directory is a directory match and is skipped (1843-1845) | TRUE | LEG 1828 (follows), 1843-1845 | HOST-OBSERVED: topdirlink status dir=1. |
| P29 | main path added even when missing (779); its watch is built by the same loop; `inotify_add_watch` result not checked (line 60; E02) | TRUE for the list and for the unchecked result; watch-time existence UNDECIDABLE-FROM-PINS | LEG 779; CW 59-62 (result stored unchecked) | `verifyConfigExists` (781) may create the default config (`generateDefaultConfig`, not pinned). Whether the file exists when watches are built is not decided by the pins. |
| P30 | cycles: no visited set and no depth limit in 1802-1855 | TRUE | LEG 1802-1855 | HL46 1004-1056 (`parseFile`) also has no guard (round-46 pin only). |
| P31 | "a file that sources itself would recurse until the stack is exhausted (inference ...; not exercised)" | TRUE-BUT-UNLABELLED-INFERENCE | Recursion follows from the absent guard (LEG 1836-1839). Each level also appends one list entry (1836), so the growth is heap as well as stack; which one fails first is not in the pins. | Keep the "inference" label and add: "stack or heap; the pins do not say which." |

### Path resolution (entry lines 53-61)

| id | entry sentence (abridged) | verdict | deciding pin lines / evidence | correction or note |
|---|---|---|---|---|
| R01 | `absolutePath` (MISC 61-83); `cur` is the file being parsed | TRUE | MISC 61-83; `cur` is `m_configCurrentPath`, set at LEG 736, 756, 1838 | — |
| R02 | `~`: first byte replaced by the value of HOME (64-66; K25, E01) | TRUE | MISC 64-66 (`getenv("HOME")`, `replace(0,1,...)`) | Omitted: `ENVHOME` is a function-local static (MISC 65), read once at the first `~` path; later changes to HOME are not seen. Cosmetic omission. |
| R03 | `~/x` becomes `$HOME/x` | TRUE | MISC 66 | — |
| R04 | `~user/x` becomes `$HOME` followed directly by `user/x`; no user lookup; no slash inserted | TRUE | MISC 66 replaces only index 0. Example with HOME=/home/vgpnk: `~user/x` → `/home/vgpnkuser/x`. | — |
| R05 | `GLOB_TILDE` (1816) never sees a leading tilde, because absolutePath already replaced it | TRUE | MISC 64-66 always runs before LEG 1816 | Consequence the entry does not state: `GLOB_TILDE` is never effective for a leading tilde in Hyprland. Cosmetic. |
| R06 | "If HOME is unset, getenv returns null and the string construction at line 66 is **undefined behaviour** (source reading; not exercised)." | **TRUE-BUT-UNLABELLED for the "UB" wording; the consequence differs** | MISC 65-66. The C++ standard makes a null `char*` into `std::string` a precondition violation (UB at the standard level). | HOST-OBSERVED (libstdc++, GCC 16.2.1): `std::string(nullptr)` throws `std::logic_error` ("basic_string: construction from null is not valid"). **Correction:** "...the construction at line 66 is a precondition violation: libstdc++ throws `std::logic_error` (HOST-OBSERVED); the exception then leaves `handleSource`, which has no catch in LEG 1802-1855. What Hyprland's own build does is UNDECIDABLE-FROM-PINS." |
| R07 | leading `/`: unchanged | TRUE | MISC 67 (`value[0] != '/'` guard) | — |
| R08 | `./x` → `curdir` + `/x` (74-75) | TRUE | MISC 74-75 | — |
| R09 | `../x` → parent of `curdir` + `/x` (71-73) | TRUE | MISC 71-73 | Cosmetic: with no `/` in `cur`, `find_last_of` returns npos and the parent is the whole `curdir`. Not reachable with absolute `cur`. |
| R10 | other names starting with `.` (`.hidden`, `..x`, bare `..`): `curdir` + `/` + RAW (77) | TRUE | MISC 76-77 | — |
| R11 | bare names: `curdir` + `/` + RAW (79) | TRUE | MISC 78-79 | — |
| R12 | `curdir` is `cur` cut at its last `/` (68; K26); no normalisation; `.`/`..` stay as text; no realpath | TRUE | MISC 68; no realpath in MISC 61-83 | — |
| R13 | "`$VAR` in RAW is not expanded by these lines. Whether hyprlang expands `$` before the handler runs is not in the pins: UNKNOWN." | First half TRUE; second half **UNDECIDABLE-FROM-PINS in round-56, decided by HL46 if its version is tied to 0.56.2** | HL46 543-551 (`recheckEnv` loads environment variables), 1070-1075 (`clearState` copies them), 737-745 (`$name` in RHS replaced before dispatch), 872 (handler gets the replaced RHS) | **Correction:** "Hyprlang (round-46 pin, v0.6.8) replaces `$NAME` in the value with environment variables and earlier `$NAME = ...` lines before the handler runs (HL46 737-745, 872). Whether Hyprland 0.56.2 links that version is not pinned in round-56." The UNKNOWN is therefore wrong as to the round-46 pin and must cite that pin. |

### Resolution base (entry lines 63-66)

| id | entry sentence (abridged) | verdict | deciding pin lines / evidence | correction or note |
|---|---|---|---|---|
| B01 | main config: `m_configCurrentPath` is the main path (736, 756), so relative `source` in the main file resolves against the main file's directory, not the working directory | TRUE for a non-symlinked, absolute main path; **TRUE-BUT-UNLABELLED for a symlinked main path**; absoluteness of the main path UNDECIDABLE-FROM-PINS | LEG 735-736, 743 (parse after the set); LEG 756-757; init path LEG 1084 calls `reload()` before any parse, so the base is set. The main path comes from `Supplementary::Jeremy::getMainConfigPath` (not pinned). | HL46 942 parses `canonical(impl->path)`, so when the main path is a symlink the text is read from the target while `m_configCurrentPath` is the link path (LEG 735-736). Relative sources then resolve against the **link's** directory. **Correction:** add "If the main config is a symlink, relative sources resolve against the link's directory, while its text comes from the target (HL46 942; LEG 736)." |
| B02 | nested file: `m_configCurrentPath` is the nested `value` (1838); its `source` resolves against that directory, not the main file's directory or the cwd; previous value restored (1840) | TRUE | LEG 1837-1840 | — |
| B03 | a symlinked nested file resolves against the link's directory; `value` is the link path and not canonicalised | TRUE | LEG 1825, 1838 (value unresolved); no realpath in MISC 61-83 | HOST-OBSERVED: glob returns the link spelling. |

### Glob semantics (entry line 70)

| id | entry sentence (abridged) | verdict | deciding pin lines / evidence | correction or note |
|---|---|---|---|---|
| G01 | `glob(3)` is called without `GLOB_NOSORT` | TRUE | LEG 1816: flags are `GLOB_TILDE` only | — |
| G02 | "**so the match order is the C library's collation.**" | **UNDECIDABLE-FROM-PINS (stated as fact; must be corrected)** | LEG 1816 shows the flag only. The collation depends on the process locale and on the libc: no `setlocale` appears in the round-56 pins (`grep` over the fetch set, including HL46: none), and no pin says which libc Hyprland links. | HOST-OBSERVED (glibc): C and C.utf8 sort bytewise (`B.conf _x.conf a.conf ...`); en_US.utf8 sorts by locale (`a.conf B.conf ... _x.conf`). **Correction:** "Without `GLOB_NOSORT` the matches are sorted by the libc's `strcoll`-style order, which is bytewise under the C locale and locale-dependent otherwise (HOST-OBSERVED, glibc). Whether Hyprland calls `setlocale` and which libc it links are not pinned." |
| G03 | "the pins do not show that collation" | TRUE | — | — |
| G04 | "the watch-plan model sorts bytewise; that is a declared divergence, not a fact of this entry" | TRUE as a statement about the tool; the divergence itself is conditional on G02 | see G02 | Tool docstring divergence (2) ("the C library's is locale collation") is true only under a non-C locale. Under the C locale the tool agrees with glibc. |
| G05 | "Whether a leading-dot name matches a `*` pattern is library behaviour ... UNKNOWN." | UNDECIDABLE-FROM-PINS (honest label); HOST-OBSERVED for glibc on this host | — | HOST-OBSERVED, glibc, all three locales: `*` does not return `.hid.conf`; `.*` returns `.`, `..` and `.hid.conf`. The UNKNOWN can be closed for glibc with this receipt; it stays open for the other libc. |

## 2. Sentences that need correction before the entry is treated as final

1. P13 (inaccessible for a missing target): FALSE as worded. Only a dangling symlink reaches 1830. Correct to the dangling-symlink case.
2. P24 (the same file is watched twice): FALSE at kernel level. Two `m_watches` entries, one kernel watch, same wd (MAN 90-92, 296-302; HOST-OBSERVED).
3. R06 (`~` with HOME unset is "undefined behaviour"): wording is at standard level only. HOST-OBSERVED libstdc++ throws `std::logic_error`; the exception path out of `handleSource` is not pinned.
4. R13 (`$VAR` "UNKNOWN"): the round-46 hyprlang pin shows expansion (HL46 737-745). The entry must cite that pin and the unpinned version tie.
5. B01 (main-file base): for a symlinked main config the base is the link's directory, while hyprlang reads the target (HL46 942; LEG 736). Add this clause.
6. G02 (glob "is the C library's collation"): locale-dependent and libc-dependent; not pinned. Restate as in the table.
7. P31 ("until the stack is exhausted"): failure mode (stack or heap) is not pinned. Add "stack or heap".

No sentence in the four sections was found FALSE in the pins themselves; P13 and P24 are the two FALSE sentences, both about behaviour the entry states as fact.

## 3. Checks on the named items

- "no deduplication" (P23): TRUE. Pin LEG 1836; no membership test anywhere in 1802-1855 or 2133-2134. Duplicate effects are at watch level (P24).
- "a missing source target never enters the list" (P25): TRUE. Pins LEG 1816-1820 and 1830-1833 both return before the append at 1836. HOST-OBSERVED rc=3 for a missing literal target; rc=0 for a dangling link (matched, then rejected at 1830 — which is the P13 correction).
- "a symlink to a regular file enters the list under the link path" (P27): TRUE. Pins LEG 1828, 1836 (value not resolved); CW 60, 65-72 for the two watches; HOST-OBSERVED for the glob spelling and the wd values.
- "cycles" (P30, P31): no guard is TRUE (LEG 1802-1855). The failure mode is UNDECIDABLE-FROM-PINS (P31 correction).
- "the `~user` sentence" (R04): TRUE. Pin MISC 66. Example: HOME=/home/vgpnk, `~user/x` → `/home/vgpnkuser/x`.
- "relative `source` resolution in nested files" (B02, B03): TRUE. Pins LEG 1837-1840; B03 HOST-OBSERVED for the link spelling.
- "the glob ordering paragraph" (G02-G05): the ordering claim is UNDECIDABLE-FROM-PINS (locale and libc). The entry's own statement that the pins do not show the collation is TRUE. HOST-OBSERVED glibc results are in the table.

## 4. Declared divergences and tool cross-checks (outside the four sections; reported because they depend on the same facts)

- watch-plan docstring divergence (2) ("the C library's is locale collation") is conditional on a non-C locale (G02). Under C/C.utf8 the tool's bytewise order matches glibc (HOST-OBSERVED).
- watch-plan docstring says "LHS `source` inside a category is unsupported". HL46 844-867 dispatches an unscoped keyword like `source` regardless of categories (its scope test is skipped for unscoped names). This is a round-46-pin disagreement with the tool, not a round-56 pin fact. Not tested here.
- watch-plan docstring divergence (4) says the canonical watch prints the realpath while Hyprland records the symlink path. CW 70 (`.file = path`) confirms the Hyprland side, so the divergence statement is consistent with the pin. The tool's output side was not audited here.

## 5. Verification gaps (not run or not decidable here)

- Hyprland was not built or run. Every Hyprland fact is from the pins or is labelled HOST-OBSERVED for libc/libstdc++ only.
- `Supplementary::Jeremy::getMainConfigPath`, `generateDefaultConfig`, and hyprlang's version tie to 0.56.2 are not in the round-56 pins; B01 and P29 rely on them and are marked accordingly.
- No `setlocale` search covered the full Hyprland tree (only the fetch set and HL46). G02 is UNDECIDABLE-FROM-PINS for that reason.
- The HOME-unset path (R06) was tested only with libstdc++ in the host toolchain, not with Hyprland's build.
- The self-source recursion (P31) was not exercised.

## 6. Receipts and deliverables

- This report: `.ufo/waves/round-56/w2/R56W2RevProsePath.md`.
- Receipts directory: `.ufo/waves/round-56/w2/R56W2RevProsePath/`:
  - `RECEIPTS.txt`: decisive output of each host probe.
  - `glob-probe.py` (run as `python3 -I glob-probe.py C` and `python3 -I glob-probe.py en en_US.utf8`; the second argument is the locale).
  - `std-filesystem-status-probe.cpp`, `std-filesystem-dirlink-probe.cpp` (g++ -std=c++20).
  - `null-string-ctor-probe.cpp` (g++ -std=c++20; run with the variable unset).
- Scratch `/fast/scratch/hyaku/mado-r56/R56W2RevProsePath/` removed after the copy.

## 7. Tooling record

- No tool installed, upgraded or removed. Used host `python3 -I`, `g++` (GCC 16.2.1), `ctypes` on glibc `libc.so.6`, `git show` (read-only), `grep`, `sed`, `ln`, `ls`.
- No pacman, no `~/.local/bin` write, no host-service change.
