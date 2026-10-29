# R56W2RevAuditA: sentence-to-pin audit of `corpus/knowledge/hyprland-config-autoreload-r56.md` at 28fc86ac2359ec27406d8a2c63bef82ea6e947ed

Seat: R56W2RevAuditA (leaf, read-only; no lane file edited; no git mutation in the lane; scratch removed).
Scored tree: `git show 28fc86ac2359ec27406d8a2c63bef82ea6e947ed:<path>` (never the working tree). Note: the lane working tree currently differs from that commit (`M corpus/knowledge/hyprland-config-autoreload-r56.md`, `M corpus/SOURCES.md`); those edits are not mine and were not read.
Receipts: `.ufo/waves/round-56/w2/R56W2RevAuditA/null-greps-and-hashes.txt`, `.ufo/waves/round-56/w2/R56W2RevAuditA/probes-summary.txt`.

## 1. What was attacked

| item | attack |
|---|---|
| K01-K05, E08, E09 | each proposition judged against the pin line AND the surrounding function (read in full); SUPPORTED / OVERREACH / UNSUPPORTED |
| entry prose citing these rows (Chain 1-3, 7; path-list sections; Limits) | every sentence about pinned code checked against the pin; every inference checked for a label |
| pin authenticity | the three pins fetched from upstream `efb50993…` and compared byte-for-byte |
| counter sensitivity to the audited rows | five probes in a scratch clone (section 4): does a false proposition or a tampered pin change the `TARGET_MET`? |

## 2. Procedure and decisive commands (trimmed)

- Pins are the `.ufo/waves/round-56/fetch/` blobs at 28fc86ac. Entry read with `git show 28fc86ac…:corpus/knowledge/hyprland-config-autoreload-r56.md`.
- Pin authenticity (upstream fetched with `curl` from `raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/…`):
  ```
  a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754  src/config/values/ConfigValues.cpp   (= pin Hyprland-ConfigValues.cpp, = frozen pin_sha256)
  8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c  src/config/shared/inotify/ConfigWatcher.cpp (= pin, = frozen pin_sha256)
  37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0  src/config/supplementary/propRefresher/PropRefresher.hpp (= pin, = S391 cell sha256)
  ```
  Not compared to upstream: the other pins (PropRefresher.cpp, legacy ConfigManager.cpp, MiscFunctions.cpp, HyprCtl.cpp, EventLoopManager.cpp, man7 page). Not run.
- Upstream `src/config/values/ConfigValues.hpp:110-113` (not pinned, checked only to resolve K01's "default" reading): `SP<T> makeConfigValue(const char* name, const char* description, Def&& def, valueOptions_t<T> options)`.
- Counter reproduction: `python3 -I quality/counters/c1-r56-autoreload-entry.py --repo <lane> --rev 28fc86ac… --work <scratch>` → `MADO_AUTORELOAD_ENTRY: rev=28fc86ac… rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none`, exit 0.
- Null-result greps (in `null-greps-and-hashes.txt`):
  - `grep -nE 'ev->name|->name|IN_Q_OVERFLOW' Hyprland-ConfigWatcher.cpp` → no match, rc=1 (supports "the event name field is never read" and "no IN_Q_OVERFLOW branch").
  - `grep -n 'makeConfigValue(' Hyprland-ConfigValues.cpp` → no match, rc=1 (the `MS` constructor signature is not in any pin).
  - `grep -c PropRefresher.hpp frozen-tables-v2.json` → 0; same for `frozen-tables.json` → 0.
- Host (read-only): `hyprctl getoption misc:disable_autoreload -j` → `{"option": "misc:disable_autoreload", "int": 0, "set": false }`; `hyprctl version -j` commit `efb50993780079460b0cbed1363e2166a2de1d9f`; `stat -c '%F' ~/.config/hypr/hyprland.conf` → regular file. No keyword, dispatch, reload or write.

## 3. Verdicts for the audited rows

Line numbers are the pin lines at 28fc86ac.

| row | verdict | pin lines | correction (one sentence) |
|---|---|---|---|
| K01 | OVERREACH (weakens, minor) | `Hyprland-ConfigValues.cpp:492`: `MS<Bool>("misc:disable_autoreload", "If true, the config will not reload automatically on save.", false, {.refresh = …})`. The quoted fragment shows `false` as the third argument, not that it is the default. The default reading needs the `makeConfigValue` signature, which is in `ConfigValues.hpp` and is not pinned. Pinned partial support: `Hyprland-legacy-ConfigManager.cpp:496` registers `p->defaultVal()` for Bool values. | "…declared as a Bool with help text saying the config will not reload automatically on save, and `false` as its third (definition, i.e. default-value) argument; the meaning of that argument is in `ConfigValues.hpp`, which is not pinned." The proposition is TRUE upstream (checked, `ConfigValues.hpp:110-113`); the defect is the pin, not the fact. |
| K02 | SUPPORTED | `Hyprland-ConfigValues.cpp:492` shows `{.refresh = Supplementary::REFRESH_CONFIG_WATCHER}` on the same declaration | none |
| K03 | SUPPORTED | `Hyprland-ConfigWatcher.cpp:33`: `static const auto PDISABLEAUTORELOAD = CConfigValue<Config::INTEGER>("misc:disable_autoreload");` (`static const` handle is what "caches" means) | none |
| K04 | SUPPORTED | `Hyprland-ConfigWatcher.cpp:34`: `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());` (non-zero → empty vector; else `getConfigPaths()` result) | none. Note: counter does not catch an inverted K04 (probe D). |
| K05 | OVERREACH (weakens) | `Hyprland-ConfigWatcher.cpp:45-47`: `for (auto& watch : m_watches) { inotify_rm_watch(m_inotifyFd.get(), watch.wd); }`; the return value is unchecked. The proposition "removes one existing watch" is false for a second entry that carries the same `wd`. The entry's own path-list text says duplicate paths give duplicate watches, and `man7-inotify.7.html:90` and `:301-302` say a repeated add on the same inode modifies the existing watch (same `wd`). The second `rm` then targets a `wd` already removed (`man7:551` says a removed descriptor is gone; the `EINVAL` return is man2, not pinned: inference). | "This loop calls `inotify_rm_watch` once per watch-list entry, passing that entry's `wd`; the return value is not checked, so a `wd` listed twice is removed twice (second call fails; inference from inotify(7) lines 90, 301-302, 551)." |
| E08 | SUPPORTED | `Hyprland-PropRefresher.hpp:18`: `REFRESH_CONFIG_WATCHER = (1 << 8),` (K02 and K15 cross-references verified at `:492` and `Hyprland-PropRefresher.cpp:148`) | none. Note: no counter leg checks this line (probe C). |
| E09 | OVERREACH (weakens, minor) | `Hyprland-PropRefresher.hpp:21`: `REFRESH_ALL = std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max(),`. "which here is uint16_t" and "every bit is set" depend on `Hyprland-PropRefresher.hpp:9`: `enum ePropRefreshProp : uint16_t {`. The row's pin cell cites line 21 only. | "REFRESH_ALL is the maximum of the enum's underlying type (`uint16_t`, `PropRefresher.hpp:9`), so every one of its 16 bits is set, including bit 8 (`:18`)." |

## 4. Counter sensitivity to these rows (falsification probes, scratch clone)

The counter passes each probe. It checks quote identity, registry binding, scope and lexical grounding; it does not check entailment. These results confirm the declared limit and show two concrete gaps.

- EXP A: K05 made false (`"…and the m_inotifyFd instance keeps that watch active"`) → TARGET_MET, exit 0.
- EXP B: E08 made false (`"…it is in fact bit 42 and controls the monitor refresh"`) → TARGET_MET, exit 0.
- EXP C: `Hyprland-PropRefresher.hpp:18` changed to `REFRESH_CONFIG_WATCHER = (1 << 42),` → TARGET_MET, exit 0. The `.hpp` is absent from both frozen tables, so `pin_hash` never covers it, and no row quotes it through a counted leg (E rows are "not counted").
- EXP D: K04 inverted (`"…when the cached … value is zero, setWatchList is given an empty vector"`) → TARGET_MET, exit 0.
- EXP E: K01 `"…and a default of true."` → TARGET_MET, exit 0.

## 5. Entry prose (sentences about pinned code, not in the K/E rows)

Checked and TRUE (line numbers confirmed against the pins): Chain 2 (`getConfigPaths` at `legacy:2133-2134`), Chain 3 (lines 45-47, 49, 54-56, 60, 65-69), Chain 4 (`EventLoopManager.cpp:127-128`, `:70-71`; `ConfigWatcher.cpp:80-111`, `:100`, `:102-107`; the `name` field is not read, grep above), Chain 5 (`legacy:1079-1082`), Chain 6 (`reload` 726-751, calls at 731, 743, 750; `postConfigReload` at 970 with `REFRESH_ALL` at 1070), Chain 7 (`PropRefresher.cpp:31`, `:34`, `:148-149`), Chain 8 (`HyprCtl.cpp:1223-1224`, `:1276`), Chain 9 (`man7:186`, `:262`), path-list lifecycle (`legacy:485`, `:614`, `:630` inside the constructor, `:764-786`, `:776`, `:777-779`, `:755`, `:731`; `resetHLConfig` callers in the pins are exactly 630, 731, 755), handleSource steps 1-5 (`1802-1855`, `1803-1806`, `1816-1820`, `1824-1828`, `1830-1833`, `1835-1840`, `1843-1848`), absolutePath (`MiscFunctions.cpp:64-66`, `:68`, `:71-79`), host statements (18 `source =` lines in `hyprland.conf`; lines 4-12 under `omarchy/default`; line 13 the theme file; `envs.conf:3` sources `gum.env.conf`; the lstat capture lists it as a regular file).

Sentences that are NOT fully true or are mislabelled:

| # | location | verdict | pin lines | correction |
|---|---|---|---|---|
| P1 | Chain 3: "…so the same file is watched twice (inference from 52-73…)" | WEAKENS | `ConfigWatcher.cpp:52-73`; `man7:90` ("modifies an existing watch"), `:301-302` ("multiple paths may refer to the same inode … may clobber existing watch masks") | "…so the watch list holds two entries; per inotify(7) a second add on the same inode modifies the existing watch and carries the same descriptor (inference from `man7:90`, `:301-302`)." |
| P2 | path list: "The list is rebuilt from nothing on every reload and verify; nothing is patched incrementally." | WEAKENS (contradicted by Limits) | `legacy:776` (clear), `:1836` (append with no clear), `:755` (verify) | "On reload and verify the list is rebuilt from nothing; a runtime `source` keyword appends to it without clearing (inference, see Limits)." |
| P3 | Scope: "Settled at source level: … how `m_configPaths` is cleared, refilled and resolved" | WEAKENS | runtime appends are inference (Limits) | drop "and resolved" for the runtime path, or label it inference. |
| P4 | path list: "Together these explain why a symlink entry gets a watch on the link and a second watch on its canonical target" | WEAKENS (unlabelled causal claim) | `K30` / `man7:262` (IN_DONT_FOLLOW), `ConfigWatcher.cpp:66-69` (explicit `is_symlink` branch) | "IN_DONT_FOLLOW (`man7:262`) makes the first watch attach to the link itself; the second watch is added by the explicit symlink branch (`ConfigWatcher.cpp:66-69`), and the reason (writes to the target are not reported on the link's inode) is inference from `man7:225-228`." |
| P5 | path list, cycles: "A file that sources itself would recurse until the stack is exhausted (inference…)" | COSMETIC (labelled, but its premise is UNKNOWN per Limits) | `legacy:1802-1855` (no visited set, no depth check); hyprlang `parseFile` is not pinned | append "(whether hyprlang's `parseFile` bounds nesting is not in the pins)". |
| P6 | glob paragraph: "…so the match order is the C library's collation" | COSMETIC (stated as fact; the same paragraph says the pins do not show it) | `legacy:1816`, `:1824` (no `GLOB_NOSORT`) | "…so the match order is glob(3)'s (not in the pins; UNKNOWN)." |
| P7 | Chain 8: "The `source` branch of the keyword dispatcher (`HyprCtl.cpp:1194-1208`)" | COSMETIC (range covers source, monitor and input branches; the `source` branch is 1194-1197) | `HyprCtl.cpp:1194-1197`, `:1208` | cite `:1194-1197`. |

## 6. Defects and severity

| id | defect | input showing it | severity |
|---|---|---|---|
| D1 | `PropRefresher.hpp` (cited by E08, E09 and Chain 7) is not in `pin_sha256` of either frozen table, and no counted leg reads it | EXP C (bit 8 → bit 42) → TARGET_MET. Content is currently upstream-authentic (sha `37acaaf1…`), but nothing in the counter guarantees it. | weakens the counter-backed claim for E08/E09 (the Chain 7 refresh step depends on them) |
| D2 | K05 "removes one existing watch" overreaches for duplicate-`wd` entries | Chain 3 "watched twice" + `ConfigWatcher.cpp:45-47` + `man7:90,301-302` | weakens |
| D3 | K01 "default of false" needs an unpinned header | `ConfigValues.cpp:492`; `ConfigValues.hpp:110-113` not pinned | weakens (minor); the fact is true |
| D4 | E09 "uint16_t / every bit" cites line 21 only | `PropRefresher.hpp:9` vs `:21` | weakens (minor) |
| D5 | P1-P4 prose: the "watched twice" mechanism, "nothing is patched incrementally", the unlabelled symlink causal claim, and the runtime-`source` "settled" wording | see section 5 | weakens |
| D6 | P5, P6, P7 | see section 5 | cosmetic |
| D7 (declared limit, confirmed) | counter passes false K01/K04/K05/E08 propositions (EXP A-E) | section 4 | the audit, not the counter, is the entailment control; no entry text edited |

No defect was found that makes the C1 entry's K02, K03, K04, E08's pin reference or the `misc:disable_autoreload` declaration wrong. No blocking defect was found in the rows assigned to this seat.

## 7. Not verified / not run

- Pins other than `ConfigValues.cpp`, `ConfigWatcher.cpp`, `PropRefresher.hpp` were not compared with upstream.
- `man2` `inotify_rm_watch` `EINVAL` behaviour for a removed descriptor was not read (not pinned); D2 relies on that and is marked inference.
- hyprlang `parseFile` / `source` pre-processing, `getMainConfigPath`, `Supplementary::Jeremy`, the `m_configPaths` declaration were not read (outside the pins; the entry marks them UNKNOWN).
- No runtime observation: no save, no inotify read, no reload. The `hyprctl` reads were the only host contact.
- The lane working tree was not read (differs from 28fc86ac).
- Tools: no installs or upgrades. Upstream fetches used `curl` (already present); no pacman transaction.
