# R56W2RevAuditB — sentence-to-pin audit of `corpus/knowledge/hyprland-config-autoreload-r56.md`

Scope: the entry at `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (read via `git show`, never the working tree). Rows K06–K12 (plus K29/K30, which the Limits and Chain step 9 rely on), the Chain step 3 and step 9 prose, the Limits, and the path-list sentences that cite pin lines. Pins read from `.ufo/waves/round-56/fetch/` (lane tree at the revision; sha256 of `Hyprland-ConfigWatcher.cpp` and `man7-inotify.7.html` match `frozen-tables-v2.json`: `8383b8ab…d516c`, `79f5ab18…d8fd`). Each pin was read in its surrounding function, not only the quoted line. The entry was not edited. Receipts: `.ufo/waves/round-56/w2/R56W2RevAuditB/receipts.txt`.

## 1. Row verdicts (K06–K12, K29, K30)

Every quote is a substring of its pin line (checked with `python3 -I`). All seven K06–K12 rows are SUPPORTED. Two rows are narrower than the line, and the Chain cites them for more than they say.

| row | verdict | pin lines | correction |
|---|---|---|---|
| K06 | SUPPORTED | ConfigWatcher.cpp:54 `const bool isDirectory = std::filesystem::is_directory(path, ecDir);` | none |
| K07 | SUPPORTED (narrow) | :55 `const uint32_t fileMask = IN_CLOSE_WRITE \| IN_DONT_FOLLOW;` | optional: "…assigned the IN_CLOSE_WRITE bit; the same line also ORs in IN_DONT_FOLLOW." The quote `fileMask = IN_CLOSE_WRITE` is a truncated prefix, so the row hides the second flag. |
| K08 | SUPPORTED (narrow) | :56 `const uint32_t directoryMask = fileMask \| IN_CREATE \| IN_DELETE \| IN_MOVED_TO \| IN_MOVED_FROM;` | Chain step 3 cites K08 for "the file mask plus IN_CREATE, IN_DELETE, IN_MOVED_TO, IN_MOVED_FROM", but K08 says only "starts from the same bits". Optional: append "and ORs in IN_CREATE, IN_DELETE, IN_MOVED_TO and IN_MOVED_FROM". |
| K09 | SUPPORTED | :59-62 `m_watches.emplace_back(SInotifyWatch{ .wd = inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask), …})`; no check on the return | none (E02 covers the unchecked return) |
| K10 | SUPPORTED | :64-67 `ec` from `canonical(path, ec)` at :65, `ec2` from `is_symlink(path, ec2)` at :66, `if (!ec && !ec2 && IS_SYMLINK) {` at :67 | none |
| K11 | SUPPORTED | :68-71 `m_watches.emplace_back(SInotifyWatch{ .wd = inotify_add_watch(m_inotifyFd.get(), CANONICAL.c_str(), IN_CLOSE_WRITE), .file = path, });` | none for K11. Chain step 3 says the second watch "carries the link path in its file field", which is :70, and :70 is not cited there. |
| K12 | SUPPORTED | :100-107 `WD = find_if(… wd …)`; `else m_watchCallback(SConfigWatchEvent{ .file = WD->file, });` | none |
| K29 | SUPPORTED | man7-inotify.7.html:185-186 `IN_CLOSE_WRITE (+)` / `File opened for writing was closed.` | none |
| K30 | SUPPORTED | man7-inotify.7.html:261-262 `IN_DONT_FOLLOW (since Linux 2.6.15)` / `Don't dereference pathname if it is a symbolic link.` | none |

## 2. Prose verdicts (sentences that cite these lines)

| sentence | verdict | pin lines | correction |
|---|---|---|---|
| Chain 3: "`is_directory` (54; K06) selects the directory mask (56; K08 …) or the file mask (55; K07 …)" | SUPPORTED (cite gap) | selection is :57 `const uint32_t mask = isDirectory ? directoryMask : fileMask;`; :54-56 define the masks | add 57 to the cite |
| Chain 3: "That second watch carries the link path in its `file` field." | SUPPORTED (cite gap) | :70 `.file = path,` | cite line 70 |
| Chain 4: "The event `name` field is never read, so the reported path is the watch's stored path" | SUPPORTED, incomplete | :80-111 read only `ev->wd` (:100) and `WD->file` (:106); no `->name`, no `->mask` (grep: the only hits are :57 and :60, the watch mask) | add: "The `mask` field is never read either, so the callback runs for every event on a registered wd, including the kernel's IN_IGNORED for a removed watch (inference from :100-107 and man7:307-309; not observed)." |
| Chain 9: "IN_DONT_FOLLOW … Together these explain why a symlink entry gets a watch on the link and a second watch on its canonical target (step 3)." | **OVERREACH** | K30 (man7:261-262) explains only the link watch. The second watch comes from code at ConfigWatcher.cpp:65-69, gated by K10 and K11, not by any flag. | "IN_DONT_FOLLOW (K30) is why the first watch attaches to the link itself; the second watch on the canonical target is added by ConfigWatcher.cpp:65-69 for a symlink (K10, K11), and the pin does not say why (inference: the link watch does not see writes made through the link)." |
| Limits 8: "An editor that replaces a file by rename would leave the old inode's watch behind (inference from the man page; not observed)." | **UNSUPPORTED** (the pin's man page contradicts the direction; the inference is labelled but wrong) | man7:199-203 `IN_DELETE_SELF … an IN_IGNORED event will subsequently be generated for the watch descriptor`; man7:307-309 `IN_IGNORED: Watch was removed explicitly … or automatically (file was deleted …)`; ConfigWatcher.cpp:100-107 call the callback for any matched wd with no mask test | "If a rename deletes the old inode, the kernel reports IN_DELETE_SELF then IN_IGNORED for that watch (man7:199-203, 307-309), and the callback runs for it because ConfigWatcher.cpp:100-107 test only the wd (inference: this triggers a reload that rebuilds the watch list; not observed)." |
| Limits 9 (runtime `source`): "The `source` branch of the keyword dispatcher (HyprCtl.cpp:1194-1208) does not call the watcher's `update()`" | SUPPORTED, cite gap | :1194-1208 has no update call. The only `update()` in HyprCtl.cpp is :1224, behind the gate `COMMAND.contains("misc:disable_autoreload")` at :1223, which "source" does not match. | cite 1223-1224 as well |
| Chain 8: "A keyword that names `misc:disable_autoreload` calls `update()` at once (HyprCtl.cpp:1223-1224; K27)" | SUPPORTED | :1223 `if (COMMAND.contains("misc:disable_autoreload"))`, :1224 `Config::watcher()->update();` | none |
| Chain 8: "`hyprctl reload` reaches `Config::mgr()->reload()` (line 1276; K28)" | SUPPORTED, cite gap | :1276 `Config::mgr()->reload();` in `reloadRequest` (non-full-reset path); the registration `registerCommand(SHyprCtlCommand{"reload", false, reloadRequest});` is at :2028 | cite 2028 |
| Limits 6: "A failed `inotify_add_watch` is not checked (line 60; E02)" | SUPPORTED, cite gap | :60 unchecked; :69 is also unchecked | cite 69 |
| Limits 6: "`onInotifyEvent` has no `IN_Q_OVERFLOW` branch" | SUPPORTED (grep: no `Q_OVERFLOW` in ConfigWatcher.cpp). Incomplete: an overflow event has wd -1, which reaches :100-103 and logs "got an event for wd -1" (man7:315-316). | :100-103 | optional: add that consequence |
| Limits 5 / Chain 1: "`misc:disable_autoreload` is a Bool with default false" | SUPPORTED | ConfigValues.cpp:492 `MS<Bool>("misc:disable_autoreload", "…", false, {.refresh = Supplementary::REFRESH_CONFIG_WATCHER})` | none |
| Path list: "A symlink to a regular file enters the list under the link path … Its watches are the link watch and the canonical watch" | SUPPORTED | :59-72 | none |
| Path list: "A symlink to a directory is a directory match and is skipped (1843-1845)" | SUPPORTED | legacy:1828 `status` follows links; :1843-1845 skip directories | none |
| Path list: "A symlinked nested file resolves against the link's directory, because `value` is the link path and is not canonicalised." | SUPPORTED | legacy:1825 `value = absolutePath(…)`, :1838 `m_configCurrentPath = value;`; no `canonical`/`realpath` in 1802-1855 | none |
| Path list: "A lone `~` or `.` is therefore bogus." | SUPPORTED | legacy:1803-1806 (`rawpath.length() < 2`) | none |
| Path list: "`~user/x` becomes `$HOME` followed directly by `user/x`" | SUPPORTED | MiscFunctions.cpp:64-66 (`value.replace(0, 1, ENVHOME)`) | none |
| Path list: "The main config path is added even when the file is missing (779)" | SUPPORTED | legacy:777-779 unconditional `emplace_back` | none |
| Path list: "A missing `source` target never enters the list" | SUPPORTED | legacy:1816-1820 return before :1836; a dangling link returns at :1830-1833 | none |
| Host: "`envs.conf` line 3 sources `gum.env.conf`" | SUPPORTED (read on host) | `~/.local/share/omarchy/default/hypr/envs.conf:3` `source = ~/.config/omarchy/current/theme/gum.env.conf`; `host-watched-lstat.txt` line 8 `regular file` | none |
| Host: "`hyprland.conf` holds 18 `source =` lines; lines 4-12 are omarchy defaults; line 13 is the theme file" | SUPPORTED (read on host) | `grep -c '^source'` = 18; lines 4-12 and 13 as stated | none |
| Limits 7 / Chain 7 (inference items: reload per event; watch list rebuilt after each reload) | SUPPORTED as labelled inference | ConfigWatcher.cpp:87-110; PropRefresher.cpp:148-149, :31, :34 (`m_propsTripped |= prop`; `doLater`); hpp:18 `REFRESH_CONFIG_WATCHER = (1 << 8)`, hpp:21 `REFRESH_ALL = max(uint16_t)` | the mask-filter gap in Chain 4 applies here too |

**Symlink and IN_DONT_FOLLOW.** The brief expected a Limits sentence about IN_DONT_FOLLOW and symlinks. The Limits section has none (`grep -n "IN_DONT_FOLLOW\|symlink\|dereference" entry.md` hits only lines 22, 28, 40, 48, 49, 66, 87, none in Limits). The closest Limits sentence is the inode bullet (Limits 8, above). The symlink and IN_DONT_FOLLOW claims are all in Chain 3, Chain 9 and the path list, and they are covered above.

## 3. Does the counter catch these errors? (falsification of the C1 leg)

The C1 counter (`quality/counters/c1-r56-autoreload-entry.py`) checks quote identity, registry binding, scope, and token, number and echo legs. It does not check the proposition's truth. Five single-edit mutants on a scratch copy (archive of 28fc86ac, one `git commit` per mutant under `-c user.name=ctl`) all print `TARGET_MET missed=none`, exit 0:

| mutant | edit | counter result |
|---|---|---|
| m1 K07 | "assigned the IN_CLOSE_WRITE inotify event bit **only**, so a watch on a symlink follows it to its target." (pin :55 has IN_DONT_FOLLOW, and K30 says the opposite of "follows") | TARGET_MET |
| m2 K10 | "requires … IS_SYMLINK to **fail** before the canonical watch is added." (pin :67 is `IS_SYMLINK`, not `!IS_SYMLINK`) | TARGET_MET |
| m3 K11 | "with IN_CLOSE_WRITE **and IN_DONT_FOLLOW** as the only mask argument." (pin :69 has IN_CLOSE_WRITE only) | TARGET_MET |
| m4 Chain 3 prose | file mask "(55; K07, IN_CLOSE_WRITE)" with IN_DONT_FOLLOW dropped | TARGET_MET |
| m5 Chain 3 prose | canonical mask "IN_CLOSE_WRITE \| IN_DONT_FOLLOW" | TARGET_MET |

The C1 control harness (`check-r56-controls.py --claim c1`) prints `good=ok controls=12/12 verdict=OK` on the unmutated tree, so none of the controls covers proposition truth. This matches the declared limit in `claims-frozen-v2.md` and `registration-v2.md` ("entailment is the wave-2 sentence-to-pin audit (reported, not counted)"). This report is that audit, and the entry needs the corrections above before the audit can be closed.

## 4. Defects (ranked)

1. **Chain 9, OVERREACH** (weakens the claim). Attributes the canonical watch to IN_DONT_FOLLOW. The fix is in §2.
2. **Limits 8, UNSUPPORTED** (weakens the claim). The "old inode's watch left behind" inference is contradicted by man7:199-203 and 307-309, and misses that the callback runs for the kernel's IN_IGNORED because no mask test exists (ConfigWatcher.cpp:100-107). The fix is in §2.
3. **Chain 4, incomplete** (weakens). The `mask` field is never read, so every event on a registered wd triggers reload, not only modify events. The Limits do not say this. Fix in §2.
4. **C1 counter, proposition truth not checked** (weakens the counted claim, as declared). m1–m5 all pass TARGET_MET, including a flipped condition (m2). A true-looking row is not evidence of entailment.
5. **Cosmetic cite gaps** (Chain 3 selection at :57; Chain 3 `file = path` at :70; Chain 8 registration at :2028; Limits 9 at :1223; Limits 6 line 69). Each proposition is true; the cited lines omit the line that shows it.

## 5. Not verified / not run

- Not checked: that the pin files match upstream Hyprland at `efb50993…`. I checked only the sha256 of the two pins against `frozen-tables-v2.json`. `host-version.json` names that commit; I did not clone upstream.
- Not run: any inotify, reload, save, `hyprctl` keyword or dispatch, or any config write. All host reads were read-only (`grep -c`, `cat`).
- Not checked: `HOME` unset (the entry marks it "not checked"); the `verify()` tail; `ConfigWatcher.hpp`; and `PropRefresher` beyond the lines cited in Chain 7.
- Behavior of IN_IGNORED delivery for a removed watch, and whether a rename-over deletes the old inode while the watch holds it, are kernel behavior and were not observed. The §2 corrections label them inference.
- The lane's working tree is dirty (`corpus/SOURCES.md`, the entry, `w1/…` receipts). Not scored; I did not touch it. No git mutation was run in the lane.
- No tools were installed. No pacman transaction. No subagent was spawned.

## 6. Scratch and receipts

- Scratch `/fast/scratch/hyaku/mado-r56/R56W2RevAuditB/` (archive clone plus mutant commits) was removed after the receipts were captured.
- Receipts: `.ufo/waves/round-56/w2/R56W2RevAuditB/receipts.txt` (pin sha256, negative greps on the pin, counter output on the base and on each mutant, the C1 control harness line).
