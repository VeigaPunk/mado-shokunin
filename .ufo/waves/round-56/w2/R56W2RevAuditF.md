# R56W2RevAuditF — sentence-to-pin audit of `corpus/knowledge/hyprland-config-autoreload-r56.md` at 28fc86ac2359ec27406d8a2c63bef82ea6e947ed

Seat: R56W2RevAuditF (wave 2, falsify). Deliverables: `.ufo/waves/round-56/w2/R56W2RevAuditF/` (receipts), report file next to it.
Scratch `/fast/scratch/hyaku/mado-r56/R56W2RevAuditF/` removed before yield. Lane touched read-only only (`git show/archive/ls-tree`, `status`, `merge-base`); the only git commits in this session are in a scratch fixture clone. No `hyprctl` state change; only `hyprctl getoption` / `hyprctl version -j` were run. Tools: pre-installed system tools only — git 2.56.0, python 3.14.8, g++ 16.2.1 (two C++ semantics probes), curl 8.23.0 (upstream pin fetches), GNU stat/grep/sed/awk. **I installed nothing** (pacman guard respected; RULES.md read).

Attack under test: *"the counter proves quote identity and lexical grounding only, so an overreaching or false proposition passes."*

## 0. Standard used and inputs verified

- **Standard.** A row's proposition cell is judged against the pinned file **plus the function enclosing the pinned line** (the seat instruction requires reading the surrounding function). SUPPORTED = every clause is carried by that evidence base (or is a correct conditional consequence of it). OVERREACH = some clause needs evidence outside that base or is stronger than it. UNSUPPORTED = false or contradicted by the pin. Each verdict names the pin lines that decide it.
- **Baseline reproduced** (receipts/coverage-mutations.txt §0):
  `python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev 28fc86ac… --work <scratch>` → `… rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none` (rc 0);
  `python3 -I quality/check-r56-controls.py --claim c1 …` → `claim=c1 good=ok controls=12/12 verdict=OK`.
- **Anchor integrity (null result, command that found nothing).** All 42 row anchors in the entry (pin:line + quote, K01-K30, H01-H03, E01-E09) land on the cited line of the cited pin — verified programmatically; and all 33 K/H rows match `frozen-tables-v2.json` `c1.k`/`c1.h` pin:line+quote **exactly** (zero mismatches). This supports the Scope claim "Every K and H row below is generated from `frozen-tables-v2.json`".
- **Pin provenance (null result).** Every upstream pin in `fetch/` is byte-identical to upstream at the pinned commit efb50993780079460b0cbed1363e2166a2de1d9f (ConfigValues, ConfigWatcher, EventLoopManager, HyprCtl, MiscFunctions, legacy ConfigManager, PropRefresher.cpp, PropRefresher.hpp — receipts/provenance.txt), and `man7-inotify.7.html` is byte-identical to today's man7.org copy (man-pages 6.19). The host captures are byte-identical to the live host outputs (receipts/host-reads.txt). So the entry's Scope claim "Pins: … at commit `efb50993…` (Hyprland v0.56.2, the host build recorded in `host-version.json`)" is verified, and every line locator in the entry is an upstream-faithful locator.

## 1. Per-row verdict table (assigned rows)

| row | verdict | pin lines | correction |
|---|---|---|---|
| H01 | SUPPORTED | host-getoption.json:1 | — |
| H02 | SUPPORTED | host-sources.txt:10 | — |
| H03 | SUPPORTED | host-version.json:3 | — |
| E02 | OVERREACH (third clause) | Hyprland-ConfigWatcher.cpp:59-62 | "The return value of inotify_add_watch is stored unchecked in the `.wd` field of the SInotifyWatch emplaced into `m_watches` at lines 59-62 — the function never tests the return value — so a failed add (for example a missing path) still leaves an entry whose `.wd` is -1 and that no later event can match." |
| E03 | OVERREACH (three descriptors) | Hyprland-ConfigWatcher.cpp:100-107 (storing at 61/70; consumer at legacy:1080) | "Line 106 copies `WD->file` — the path stored in the watch matched by `wd` at line 100 — into the `SConfigWatchEvent` that `m_watchCallback` receives (lines 105-107), so the callback is handed the stored watch path and the kernel's event `name` is ignored." |
| E04 | OVERREACH (second clause) | Hyprland-HyprCtl.cpp:1160-1182, 1190, 2037; legacy:1089-1090 | "This line passes COMMAND and VALUE to the legacy config manager's `parseKeyword` — the call a runtime `hyprctl keyword` request reaches through `dispatchKeyword` (registered as the `keyword` command at line 2037) — and the route exists only when the config manager is legacy (`dispatchKeyword` returns "keyword can't work with non-legacy parsers. Use eval." at lines 1162-1163)." |
| Host reads ¶ | SUPPORTED (all five assertions) | host-sources.txt:1-18; host-watched-lstat.txt:8 | — |

Row detail (what the line shows vs what needed the function):

- **H01** — host-getoption.json:1 = `{"option": "misc:disable_autoreload", "int": 0, "set": false }`; quote `"option": "misc:disable_autoreload", "int": 0` is on it and shows the option name and the int value 0. "on this host" is attested by the live read `hyprctl getoption misc:disable_autoreload -j`, which returned byte-identical output. SUPPORTED.
- **H02** — host-sources.txt:10 = `source = ~/.config/omarchy/current/theme/hyprland.conf`. The capture is a listing of the live file's `^source` lines (diffed against live `grep '^source'`: IDENTICAL), so capture line 10 ↔ live hyprland.conf line 13; the Limits bullet "H02 is a line of a captured listing; the live file's line 13 holds the same text" is exactly right and I verified both texts. SUPPORTED.
- **H03** — host-version.json:3 = `    "commit": "efb50993780079460b0cbed1363e2166a2de1d9f",`; the line shows the commit field. "the running Hyprland build on this host" is attested by the live `hyprctl version -j`, byte-identical to the capture, and its commit is the pinned commit (§0). SUPPORTED.
- **E02** — quoted line 60 shows the unchecked store into `.wd`. The consequence clause ("a failed add still leaves a watch entry") is carried by the enclosing `m_watches.emplace_back(SInotifyWatch{…})` at 59-62 and by the fact that inotify_add_watch returns -1 on failure (I ran an inotify probe: same path twice → same wd; missing path → wd = -1 ENOENT), which no pin states. Substance true; wording attributes a function-level consequence to the line. OVERREACH (weakens).
- **E03** — quoted line 106 (`.file = WD->file,`) sits inside `m_watchCallback(SConfigWatchEvent{…})` at 105-107 and its `WD` is the find_if match on `ev->wd` at 100; "the reported path is the stored watch path" additionally needs the consumer at legacy:1080 (`"CConfigManager: file {} modified, reloading", e.file`) and the fact that `ev->name` is never read (verified: grep over the pin finds no `->name` access; only `ev->wd` and `ev->len` are read). Substance true — and note E03 is carefully worded ("the stored watch path", *not* the canonical target path; line 70 stores `.file = path`, the link path, exactly as registration-v2 E8(4) says). OVERREACH (weakens, attribution only).
- **E04** — quoted line 1190 shows `mgr->parseKeyword(COMMAND, VALUE)`; COMMAND/VALUE are extracted from the request at 1181-1182 after the command word is stripped (1173), and the enclosing `dispatchKeyword` is registered as the `keyword` command at 2037. Two gaps: (a) the route claim is not carried by the line; (b) the route is legacy-only — `dispatchKeyword` returns early at 1162-1163 for a non-legacy (Lua) config manager, so on such a host `hyprctl keyword` never reaches `parseKeyword`. The entry's Limits separately lists "the Lua config provider" as UNKNOWN, but the cell itself is unqualified. OVERREACH (weakens).

## 2. Host reads paragraph — every statement re-run (null result)

Entry line 68 claims (each verified live; receipts/host-reads.txt):

| # | claim | live check | result |
|---|---|---|---|
| 1 | `~/.config/hypr/hyprland.conf` holds 18 `source =` lines (`grep -c '^source'`) | `grep -c '^source'` | 18 ✓ (all 18 matched lines are `source = ` lines) |
| 2 | "Its lines 4-12 name files under `~/.local/share/omarchy/default/hypr/`" | `grep -n '^source'` | lines 4-12 = autostart, media, clipboard, tiling-v2, utilities, envs, looknfeel, input, windows — all under that dir ✓ |
| 3 | "line 13 names the theme file (H02's text)" | `sed -n '13p'` | `source = ~/.config/omarchy/current/theme/hyprland.conf` = H02's quote text exactly ✓ |
| 4 | "envs.conf line 3 sources `~/.config/omarchy/current/theme/gum.env.conf`" | `sed -n '3p'` | exact match ✓ |
| 5 | "a `~` reference that the host's lstat capture (`host-watched-lstat.txt`) lists as a regular file" | capture line 8 = `regular file\|'~/.config/omarchy/current/theme/gum.env.conf'`; independent sweep | ✓ — and my own `os.lstat` sweep of all 40 capture entries (tilde-expanded): 40/40 regular files, 0 missing, 0 type mismatch |

The Limits bullet (line 139) "H01 and H03 are captures from this host; they show values at capture time, not reload behaviour. H02 is a line of a captured listing; the live file's line 13 holds the same text." reproduces in full ✓.

**Verdict: the Host reads paragraph is SUPPORTED on every statement** — nothing to correct. This is a genuine null result with the commands above.

## 3. Prose statements citing in-scope rows/lines (Chain, path list, Limits)

Verified true (null results): Chain §3 "The watch is added at line 60 (K09)"; "That second watch carries the link path in its `file` field" (ConfigWatcher.cpp:70 `.file = path,` — the LINK path, not CANONICAL; matches registration-v2 E8(4)); Chain §4 "The event `name` field is never read" (grep: no `ev->name` access; only `ev->wd`, `ev->len`); path-list "the result of `inotify_add_watch` is not checked (line 60; E02)"; Limits "A failed `inotify_add_watch` is not checked (line 60; E02)"; Limits "The handler appends to `m_configPaths` without clearing it (1836)"; Limits "The `source` branch … does not call the watcher's `update()`" (no `Config::watcher()->update()` in 1194-1208; the call is at 1223-1224 under the disable_autoreload condition), labelled "(inference from the branch; not run)" ✓; Limits "if `inotify_init1` fails, the constructor logs and returns (ConfigWatcher.cpp:21-26)" ✓; "the event loop does not register a descriptor (EventLoopManager.cpp:127)" ✓ (127 is the `FD.isValid()` guard); "`onInotifyEvent` has no `IN_Q_OVERFLOW` branch" ✓ (grep: none); Limits "Host records: H01 and H03 … / H02 is a line of a captured listing …" ✓ (reproduced).

Defects and imprecisions:

| # | location | sentence | defect | severity | correction |
|---|---|---|---|---|---|
| P1 | Limits (entry line 138, cites E04) | "That `parseDynamic` then invokes the registered `handleSource` handler (line 614) is inference: `parseDynamic` is not in the pins." | False as literally stated: `parseDynamic` IS in the pins — `Hyprland-legacy-ConfigManager.cpp:1090` (`m_config->parseDynamic(COMMAND.c_str(), VALUE.c_str());`, inside `parseKeyword` at 1089). What is not pinned is hyprlang's `parseDynamic` *implementation* (the dispatch to registered handlers). The inference label itself is correct. | weakens the claim (a stated fact about the pin set is wrong) | "…is inference: hyprlang's `parseDynamic` implementation is not among the pins (only its call at `Hyprland-legacy-ConfigManager.cpp:1090` is)." |
| P2 | Chain §3 (entry line 22) | "`is_directory` (54; K06) selects the directory mask (56; K08 …) or the file mask (55; K07 …)" | The *selection* is line 57 (`const uint32_t mask = isDirectory ? directoryMask : fileMask;`), which the sentence never cites; 54 computes the predicate, 55/56 define the masks. | cosmetic | "`is_directory` (54; K06) determines (line 57) which of the directory mask (56; K08 …) or the file mask (55; K07 …) is stored into `mask`." |
| P3 | Chain §4 (entry line 23) | "calls the stored callback with that watch's `file` (lines 102-107; K12, E03)" | The call is 105-107; 102-104 is the not-found log branch. Range imprecision only (call ⊂ range). | cosmetic | cite "lines 105-107" (or "104-107, after the `WD == end()` guard at 102-103"). |
| P4 | Chain §3 (entry line 22) | "If the entry `is_symlink` (66) and `canonical` succeeded (65, 67; K10)" | Omits that `ec2` (is_symlink's own error code) must also be clear; the cited K10 cell states it exactly ("both error codes to be clear and IS_SYMLINK to hold"). | cosmetic | none needed beyond K10's wording. |
| P5 | Chain §3 (entry line 22) | "That second watch carries the link path in its `file` field." | TRUE (line 70 `.file = path,`, the link path — matches registration-v2 E8(4)). Listed here only as a verified positive. | — | — |

## 4. Counter coverage findings (the seat's attack premise, with receipts)

The C1 predicate is `content=33/33`, and `33` is counted over `c1["k"] + c1["h"]` = 30 K + 3 H rows only. The counter's `known` set contains exactly K01-K30 and H01-H03; `E01`-`E09` are in neither the frozen tables nor `known`, so the counter never even parses the E-table rows. Fixture mutations (receipts/coverage-mutations.txt; every fixture commit asserted `git rev-parse --show-toplevel` == fixture dir):

| # | mutation (in scope unless marked) | counter result | reading |
|---|---|---|---|
| M1 | E03 proposition + FALSE clause "… and it is the canonical target path of the symlink" (line 70 stores `.file = path`, the link path) | `content=33/33 … TARGET_MET` | A false E-row proposition passes with zero resistance — E rows are outside every leg. |
| M2 | E03 pin:line 106 → 107 (quote no longer on the cited line) | `… TARGET_MET` | E rows get no quote-on-line check either. |
| M3 | H01 proposition "an int value of zero" → "an int value of seven" | `content=33/33 … TARGET_MET` | A semantically FALSE counted-row proposition passes: the `num` leg constrains ASCII digit runs only (`RUN_RE = [0-9]+`); "seven" is a word, `tok` still overlaps ("misc"/"disable_autoreload"), `echo` clean. |
| M4 | control: same mutation with a digit — "an int value of 7" | `content=32/33 … TARGET_MISSED missed=num:H01` | shows the num leg is live for digits — and therefore that the M3 gap is precisely "spelled-out numbers are invisible". |
| M5 | H02 proposition renamed to "… names the omarchy gum environment file gum.env.conf …" (quote unchanged, so false) | `content=33/33 … TARGET_MET`; harness `controls=12/12` | False counted-row proposition passes, and the 12 C1 controls do not cover the hole either (they mutate the counter's inputs, never proposition truth). |
| M6 | (adjacent) `fetch/Hyprland-PropRefresher.hpp` line 18 `(1 << 8)` → `(1 << 9)` | `… TARGET_MET` | The .hpp is quoted by E08/E09 and relied on by Chain §7, but it is in **neither** `c1.pin_sha256` nor `c1.host_pin_sha256` (12 of the 13 fetch files are hashed), and `S391` is in neither `c1.rows` nor `new_row_ids`, so no `source_cell`/`scope`/`new_rows`/`pin_hash` leg binds it. |
| M7 | (adjacent) registry S391 anchor cell `PropRefresher.hpp:18,21 @ efb5099…` → `PropRefresher.hpp:3,4 @ efb5099…` | `… TARGET_MET` | S391's anchor is never scope-checked (the `scope` leg runs over `c1["k"]` rows only, and S391 ∉ `c1.rows`). |
| — | positive control: corrupt K12's quote cell (append `X`) | `rows=29/30 … TARGET_MISSED missed=row:K12,quote:K12` | the counter is not vacuous; it checks K/H structure and quote identity. |

Reading: M3-M5 confirm the disclosed C1 limit (registration-v2 §"What v2 does not repair": entailment is the wave-2 audit, "reported, not counted"), and sharpen it in two ways the disclosure does not state: (a) the H-row `num` guard is digit-run-only, so a *spelled-out* wrong number evades it (M3); (b) E rows are outside **every** leg — quote identity included (M1, M2), which the entry discloses as "Extra rows (not counted …)" but which means the C1 `TARGET_MET` says nothing at all about E02/E03/E04 — the rows this audit covers. M6/M7 are the material new gaps: a pin and a registry row the entry actually cites are outside the frozen coverage entirely.

## 5. Adjacent findings (outside the assigned row set; reported because they bear on the audited table)

- **A1 — the `.hpp` pin is unfrozen (weakens the claim).** `Hyprland-PropRefresher.hpp` entered `fetch/` at the integration commit 0ff41272, i.e. after both freezes (3423ae28, 323a69c9); `frozen-tables-v2.json` (committed 323a69c9) has no entry for it in `c1.pin_sha256`, and `c1.rows`/`new_row_ids` carry only S383-S390. Neither `claims-frozen-v2.md`, `registration-v2.md`, `claims-frozen.md`, nor `registration.md` mentions the `.hpp` or S391 (grep: zero hits). The registry row S391 does record the correct sha (37acaaf1… = actual) and the file is byte-identical to upstream, so the *content* is right — only the *coverage* is missing (M6/M7). The entry's Chain §7 bit arithmetic ("REFRESH_CONFIG_WATCHER is bit 8 … so it contains that bit") therefore rests on a pin that no frozen hash protects.
- **A2 — Chain §7 citation precision (cosmetic).** "`REFRESH_ALL` is the maximum of the 16-bit underlying type (`Hyprland-PropRefresher.hpp:21`; E09)": the *maximum* is on line 21, but "16-bit"/`uint16_t` is declared at `Hyprland-PropRefresher.hpp:9` (`enum ePropRefreshProp : uint16_t`) — E09's own cell says "which here is uint16_t" on a line-21 quote. Same-file fact; citation precision only (and covered by A1 for the coverage gap).
- **A3 — provenance header enumeration (cosmetic).** The entry's `source:` line lists "host captures cited as `host` in the H rows: host-getoption.json, host-version.json, host-sources.txt" — accurate as scoped, but the Host reads paragraph additionally relies on `host-watched-lstat.txt`, which the header does not name (it IS hash-frozen in `c1.host_pin_sha256`).

## 6. Severity roll-up

- **Blocking: none found** in the assigned scope. All six assigned rows are factually true of their pins; the Host reads paragraph reproduces on the live host; every prose sentence about the pinned code that cites them checks out except P1.
- **Weakens the claim:** E02, E03, E04 (propositions carry function/corpus-level clauses their quoted lines do not show — corrections in §1); P1 (Limits misstates the pin set re `parseDynamic`); A1 (the `.hpp` pin and S391 row are outside the frozen coverage, with M6/M7 receipts); §4/M3 (spelled-out numbers defeat the H-row `num` guard — sharpens the disclosed registration limit).
- **Cosmetic:** P2, P3, P4, A2, A3.

## 7. What I could not verify

- **Working-tree observation (does not affect the verdicts).** While I audited, a concurrent sibling seat staged changes in the lane working tree (`corpus/SOURCES.md` +S392-S395, the entry's `source:` line and the E-row `src` cells re-pointed, mtime 22:31). My audit scored the **committed rev 28fc86ac** as instructed; the E02/E03/E04 proposition cells are byte-identical between the committed rev and the working tree, so the verdicts carry over. The new S392-S395 anchor cells do match the quoted lines (spot-checked S392 = ConfigWatcher.cpp:106, S394 = HyprCtl.cpp:1190, S395 = ConfigManager.cpp:630,1838,2134), which partially addresses finding M7 for these anchors — but at my audited rev those rows do not exist in `frozen-tables-v2.json` (frozen at 323a69c9), so §4/M7 stands for the frozen coverage.
- Whether `raw.githubusercontent.com` / `man7.org` serve content that could itself have been altered in transit — I verified byte-identity to what they serve today, not to a signed artifact (no hash was published upstream); the frozen tables do carry pin hashes and those match the fetched bytes.
- The registry row S390's claim "Linux man-pages 6.19 (2026-02-14)" — the pin is byte-identical to today's man7.org page; I did not verify the page's internal version/date metadata from the pin alone.
- Whether any consumer of `SConfigWatchEvent` exists outside the pinned legacy callback (the pins do not include the Lua/config-provider path; the entry declares that UNKNOWN) — nothing in the entry depends on it.
- The `S391` used-by cell is verified only by the C3 counter (not C1); I did not audit C3.

## 8. Note on the delivered rows

No edit was made to the entry or any tracked lane file (the L1 applies corrections). The six in-scope rows are factually accurate; the corrections proposed in §1/§3 are attribution/precision fixes, not truth fixes.
