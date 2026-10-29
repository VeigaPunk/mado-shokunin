#!/usr/bin/env python3
"""Generate corpus/knowledge/hyprland-config-autoreload-r56.md (C1 draft) for seat R56ScribeEntryA.

K/H rows: pin cell and quote cell are read from frozen-tables.json and the pinned files (sha-checked,
also checked against the git blob at the freeze commit). Only the proposition text is authored here.
E rows: extra facts; quote = a substring of one pinned line selected by this script (asserted).
Writes the entry to --out and prints one self-check line. Read-only on the lane.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "3423ae285676c2a10273000f4519163472b443db"
TABLES_REL = ".ufo/waves/round-56/frozen-tables.json"
TABLES_SHA = "d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af"
PIN_DIR_REL = ".ufo/waves/round-56/fetch"
ENTRY_REL = "corpus/knowledge/hyprland-config-autoreload-r56.md"
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
NUM = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")

# ---------------------------------------------------------------- propositions (authored; K01..K30, H01..H03)
PROPS = {
    "K01": "The misc:disable_autoreload option is declared with the description that a true value stops the config from reloading automatically on save, and its default is false.",
    "K02": "The misc:disable_autoreload declaration gives the option a refresh flag that names Supplementary::REFRESH_CONFIG_WATCHER.",
    "K03": "CConfigWatcher::update binds misc:disable_autoreload as an INTEGER config value, held in a static pointer named PDISABLEAUTORELOAD.",
    "K04": "The list passed to setWatchList is an empty vector when PDISABLEAUTORELOAD is non-zero, and the config paths otherwise.",
    "K05": "setWatchList removes each stored watch with inotify_rm_watch on the inotify descriptor before the watch list is rebuilt.",
    "K06": "setWatchList classifies each configured path with std::filesystem::is_directory and an error code before it chooses a mask.",
    "K07": "The fileMask value for a non-directory watch starts with IN_CLOSE_WRITE, and the full line also ORs in IN_DONT_FOLLOW.",
    "K08": "The directoryMask is derived from fileMask, so a directory watch carries the file bits plus the create, delete and move events on the same line.",
    "K09": "Each configured path is registered with inotify_add_watch on the inotify descriptor, using the mask chosen for that path.",
    "K10": "A second watch is added only when the canonical lookup reports no error and IS_SYMLINK is true for the path, so a plain file gets one watch.",
    "K11": "The second watch for a symlink registers the CANONICAL target path with IN_CLOSE_WRITE alone, without the IN_DONT_FOLLOW bit of the primary watch.",
    "K12": "onInotifyEvent calls m_watchCallback with an SConfigWatchEvent for each inotify event whose watch descriptor matches a stored watch.",
    "K13": "enterLoop registers the watcher inotify descriptor as a readable wl_event_loop source whose callback is configWatcherWrite.",
    "K14": "configWatcherWrite passes the readable event to Config::watcher()->onInotifyEvent and then returns 0 to the event loop.",
    "K15": "refreshProp runs the config watcher step only when the REFRESH_CONFIG_WATCHER bit is set in the m_propsTripped mask.",
    "K16": "When the config watcher bit is tripped, the refresher calls Config::watcher()->update() as its config watcher step.",
    "K17": "CConfigManager::init installs its change handler with Config::watcher()->setOnChange, passing a lambda that captures this.",
    "K18": "The change handler logs a DEBUG message reading CConfigManager: file modified, reloading, and it then calls reload.",
    "K19": "postConfigReload calls scheduleRefresh with the REFRESH_ALL bit on the Supplementary refresher.",
    "K20": "resetHLConfig empties the m_configPaths list at the start of its paths section, before it adds the main config path again.",
    "K21": "handleSource appends each accepted regular-file match to m_configPaths before it parses that file recursively.",
    "K22": "handleSource parses a glob match only when is_regular_file is true for its file_status, which is computed from the match value.",
    "K23": "A glob match that is a directory is logged with the message source= skipping directory and is not added to the path list.",
    "K24": "handleSource builds the glob pattern with absolutePath applied to rawpath and the current config path, then calls glob with GLOB_TILDE.",
    "K25": "absolutePath reads the HOME environment variable through getenv into ENVHOME, which it uses for a leading tilde in the path.",
    "K26": "For a relative path, absolutePath takes currentDir as everything before the last slash of currentPath, using substr and find_last_of.",
    "K27": "The hyprctl keyword handler tests whether COMMAND contains misc:disable_autoreload, and the branch guards the watcher update on the next line.",
    "K28": "reloadRequest calls Config::mgr()->reload() on its non-full-reset path, after the full-reset branch has returned.",
    "K29": "The inotify man page text attached to IN_CLOSE_WRITE says the event reports a file that was opened for writing and has been closed.",
    "K30": "The inotify man page entry for IN_DONT_FOLLOW says the flag stops inotify from dereferencing pathname when pathname is a symbolic link.",
    "H01": "The host hyprctl getoption dump reports misc:disable_autoreload with integer value 0.",
    "H02": "The host sources list contains a source line that reaches the omarchy theme hyprland.conf through the home config directory.",
    "H03": "The host version record names the build commit efb50993780079460b0cbed1363e2166a2de1d9f, the commit this entry pins.",
}

# ---------------------------------------------------------------- extra rows (ignored by the counter)
# (id, sid, pin, line, substring of that line, proposition)
EXTRA = [
    ("E01", "S389", "Hyprland-HyprCtl.cpp", 2028, 'registerCommand(SHyprCtlCommand{"reload", false, reloadRequest});',
     "The command table binds the hyprctl request named reload to the handler reloadRequest."),
    ("E02", "S389", "Hyprland-HyprCtl.cpp", 1224, "Config::watcher()->update();",
     "Inside the misc:disable_autoreload branch of the keyword handler, Config::watcher()->update() is called directly, not through the refresher."),
    ("E03", "S387", "Hyprland-legacy-ConfigManager.cpp", 779, "m_configPaths.emplace_back(mainConfigPath);",
     "resetHLConfig adds the main config path back as the first entry of m_configPaths after clearing the list."),
    ("E04", "S387", "Hyprland-legacy-ConfigManager.cpp", 2134, "return m_configPaths;",
     "getConfigPaths returns m_configPaths by const reference, the list that CConfigWatcher::update passes to setWatchList."),
    ("E05", "S383", "Hyprland-ConfigWatcher.cpp", 21, "m_inotifyFd(inotify_init1(IN_NONBLOCK",
     "The watcher constructor creates its inotify descriptor with inotify_init1 and the IN_NONBLOCK flag."),
    ("E06", "S383", "Hyprland-ConfigWatcher.cpp", 23,
     'Log::logger->log(Log::ERR, "CConfigWatcher couldn\'t open an inotify node. Config will not be automatically reloaded");',
     "When inotify_init1 fails, the watcher constructor logs that config will not be automatically reloaded and returns."),
    ("E07", "S383", "Hyprland-ConfigWatcher.cpp", 49, "m_watches.clear();",
     "setWatchList clears the m_watches vector after removing the old watches, before it adds the new entries."),
    ("E08", "S383", "Hyprland-ConfigWatcher.cpp", 65, "CANONICAL  = std::filesystem::canonical(path, ec);",
     "CANONICAL is the result of std::filesystem::canonical on the configured path, the target that the second watch registers."),
    ("E09", "S383", "Hyprland-ConfigWatcher.cpp", 66, "IS_SYMLINK = std::filesystem::is_symlink(path, ec2);",
     "IS_SYMLINK is computed with std::filesystem::is_symlink on the configured path itself, the test that gates the canonical second watch."),
    ("E10", "S385", "Hyprland-PropRefresher.cpp", 29, "void CPropRefresher::scheduleRefresh(PropRefreshBits prop) {",
     "scheduleRefresh takes a PropRefreshBits argument named prop, which the body then sets in the m_propsTripped mask."),
    ("E11", "S387", "Hyprland-legacy-ConfigManager.cpp", 1828, "file_status = std::filesystem::status(value, ec);",
     "The match is classified through a status call on value, and the is_regular_file test reads the result of that status call."),
    ("E12", "S387", "Hyprland-legacy-ConfigManager.cpp", 1832, 'return "source= file " + value + " is inaccessible!";',
     "A failed status call on a match returns the inaccessible message for that file, and the rest of the glob matches are not parsed."),
    ("E13", "S387", "Hyprland-legacy-ConfigManager.cpp", 614, 'm_config->registerHandler(&::handleSource, "source", {false});',
     "The Hyprlang config registers the source keyword with the static handleSource wrapper, which forwards to the legacy manager."),
    ("E14", "S387", "Hyprland-legacy-ConfigManager.cpp", 731, "resetHLConfig();",
     "reload calls resetHLConfig before it parses the config, so the path list is rebuilt on every reload."),
    ("E15", "S387", "Hyprland-legacy-ConfigManager.cpp", 485, "m_configPaths.emplace_back(m_mainConfigPath);",
     "The constructor seeds m_configPaths with m_mainConfigPath before it creates the Hyprlang config object."),
    ("E16", "S386", "Hyprland-EventLoopManager.cpp", 127, "if (const auto& FD = Config::watcher()->getInotifyFD(); FD.isValid())",
     "enterLoop registers the watcher descriptor as a loop source only when getInotifyFD returns a valid descriptor."),
    ("E17", "S388", "Hyprland-MiscFunctions.cpp", 73, "value.replace(0, 2 + currentPath.empty(), parentDir);",
     "For a leading dot-dot path, absolutePath replaces 2 characters, plus one when currentPath is empty."),
    ("E18", "S390", "man7-inotify.7.html", 225, "Inotify monitoring is inode-based: when monitoring a file (but not",
     "The inotify man page says monitoring is inode-based: watching a file, and not its containing directory, can report activity on any link to it."),
    ("E19", "S390", "man7-inotify.7.html", 200, "Watched file/directory was itself deleted.",
     "The inotify man page says a watched file or directory that is deleted yields IN_DELETE_SELF, after which the watch is reported as ignored."),
    ("E20", "S390", "man7-inotify.7.html", 215, "Generated for the directory containing the old filename",
     "The inotify man page says IN_MOVED_FROM is generated for the directory containing the old filename when a file is renamed."),
]

# ---------------------------------------------------------------- prose (no line may start with '| K', '| H', '| E'
# except table rows; no S-id may appear except S383..S390)
HEAD = """source: S383 — `src/config/shared/inotify/ConfigWatcher.cpp` (Hyprland efb5099, fetch/Hyprland-ConfigWatcher.cpp); S384 — `src/config/values/ConfigValues.cpp` (fetch/Hyprland-ConfigValues.cpp); S385 — `src/config/supplementary/propRefresher/PropRefresher.cpp` (fetch/Hyprland-PropRefresher.cpp); S386 — `src/managers/eventLoop/EventLoopManager.cpp` (fetch/Hyprland-EventLoopManager.cpp); S387 — `src/config/legacy/ConfigManager.cpp` (fetch/Hyprland-legacy-ConfigManager.cpp); S388 — `src/helpers/MiscFunctions.cpp` (fetch/Hyprland-MiscFunctions.cpp); S389 — `src/debug/HyprCtl.cpp` (fetch/Hyprland-HyprCtl.cpp); S390 — inotify(7), man7 HTML copy (fetch/man7-inotify.7.html)
verified-at: 2026-10-28
recheck: on-release

# Hyprland config auto-reload on 0.56.2: sourced chain (MADO-R56-C1)

Pins: Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2, the host build per the host version record). Frozen pin files and their sha256 are in `.ufo/waves/round-56/frozen-tables.json`.

## Scope

Settled at source level, in the pinned files:
- the declaration, default and refresh flag of `misc:disable_autoreload`, and where its value is read;
- how the watch list is built from the config path list: empty when the option is non-zero; one primary watch per path with a file or directory mask; a second canonical watch when the path is a symlink;
- how an inotify event reaches the reload callback, how the refresher and the hyprctl keyword branch reach `update()`, and how a reload ends in `postConfigReload` with `REFRESH_ALL`;
- how `source =` lines fill the path list, and the inotify(7) meaning of `IN_CLOSE_WRITE`, `IN_DONT_FOLLOW` and inode-based monitoring.

UNKNOWN in this entry. No filesystem event, reload or editor behaviour is observed, and the following are not settled by the pinned files:
- whether `REFRESH_ALL` includes `REFRESH_CONFIG_WATCHER`, so whether a reload rebuilds the watch list;
- where a parsed change to `misc:disable_autoreload` trips the refresh bit (ConfigValue headers are not pinned);
- what a text editor writes on save (in place, or by rename);
- the watch set the running host actually holds; the host pins are a getoption dump, a sources list and lstat results, not a watch list.

## Chain

Labels: [OBS] the pinned line shows it; [INF] follows from pinned lines by reasoning, not observed; [UNKNOWN] not settled by the pins.

1. **Declaration.** [OBS] K01–K02: `misc:disable_autoreload` is a Bool option with default false (line 492) whose metadata carries the refresh flag `REFRESH_CONFIG_WATCHER`. [UNKNOWN] where a parsed value change trips that flag.
2. **Value read and watch-list rule.** [OBS] K03–K04: `CConfigWatcher::update` (line 32) reads the option as an integer into a static pointer and passes an empty list to `setWatchList` when it is non-zero, otherwise `Config::mgr()->getConfigPaths()`. [OBS] E04: that list is `m_configPaths`, returned by const reference. So `autoreload=off` means an empty watch set, not a different mask.
3. **Watch construction.** [OBS] K05 and E07: old watches are removed, then the list is cleared. [OBS] K06: each path is classified with `std::filesystem::is_directory`. [OBS] K07–K08: a file mask `IN_CLOSE_WRITE | IN_DONT_FOLLOW`; a directory mask adds `IN_CREATE`, `IN_DELETE`, `IN_MOVED_TO` and `IN_MOVED_FROM`. [OBS] K09: `inotify_add_watch` is called per path and its result is stored in `wd` (lines 59–62) with no check. [INF] a failed add stays in the list as an entry with the failure value; no log line for it appears in the pinned file.
4. **Symlink canonical watch.** [OBS] K10–K11, E08–E09: when `canonical` succeeds and `is_symlink` is true, one more watch is added on the resolved path with `IN_CLOSE_WRITE` alone. [OBS] K30: the man page says `IN_DONT_FOLLOW` makes the call not dereference a symbolic link. [INF] Together, the primary watch of a symlink path is on the link itself, not its target, and the canonical watch is the one that observes the target file, which is where a write through the link lands. The canonical watch lacks `IN_DONT_FOLLOW`; for a resolved path that has no link component this should make no difference.
5. **Path list.** [OBS] E15 and E03: the main config path is the first entry, set in the constructor and again after each reset. [OBS] K20: `resetHLConfig` clears the list. [OBS] K21–K22: a `source =` match is appended only when `is_regular_file` holds for its `file_status`, and before its recursive parse. [OBS] K23: a directory match is logged and skipped. [OBS] K24–K26 and E17: the source path goes through `absolutePath` (a leading tilde from `getenv("HOME")`, a relative path against the directory of the current file) and then `glob` with `GLOB_TILDE`. [OBS] E11: the file type comes from `std::filesystem::status`. [INF] `status` follows symbolic links, a C++ standard library rule not shown in a pin; so a link to a regular file is appended under its link path, because the value at line 1825 is the un-resolved match. That link path is what steps 3 and 4 build the watches from. [OBS] E12: a match whose status call fails returns an error and the rest of the matches on that line are not parsed. [OBS] E13: the `source` keyword is registered with the static `handleSource` wrapper (line 614), which forwards to the legacy manager.
6. **Event to reload.** [OBS] E16 and K13: the watcher descriptor is a loop source only when valid, and `enterLoop` registers `configWatcherWrite` as its callback. [OBS] K14: `configWatcherWrite` calls `onInotifyEvent`. [OBS] K12: `onInotifyEvent` maps the event's `wd` to a stored watch and calls `m_watchCallback` with that watch's path; an unknown `wd` is logged as an error. [OBS] K17–K18: `CConfigManager::init` installs the callback, which logs and calls `reload()` (line 1081). The callback does not look at the event kind, so any matched event reloads.
7. **Reload.** [OBS] E14: `reload()` calls `resetHLConfig()`, which rebuilds the path list, then parses the config (line 743) and calls `postConfigReload` (line 750). [OBS] K19: `postConfigReload` calls `scheduleRefresh(REFRESH_ALL)`. [UNKNOWN] `REFRESH_ALL` is not defined in the pinned files, so whether it contains `REFRESH_CONFIG_WATCHER` is not settled. [INF] If it does not, the watch set is rebuilt only by a later `update()` call, and a `source =` file added by the reload is not watched until then. This is the chain's largest open point.
8. **Refresher and keyword paths.** [OBS] E10: `scheduleRefresh` sets the requested bit in `m_propsTripped`. [OBS] K15–K16: `refreshProp` calls `Config::watcher()->update()` when `REFRESH_CONFIG_WATCHER` is set. [OBS] E02 and K27: a hyprctl keyword whose text contains `misc:disable_autoreload` calls `update()` directly. [OBS] E01 and K28: the hyprctl request `reload` calls `Config::mgr()->reload()` on its non-full-reset path.
9. **Editor and kernel semantics.** [OBS] K29: `IN_CLOSE_WRITE` reports a file opened for writing that was closed. [OBS] E18: the man page says monitoring is inode-based: when a file is monitored (not the directory containing it), activity on any link to the file can generate an event. [INF] A file path gets a file-mask watch only, and no watch is set on its parent directory (K08 applies only to directories). An editor that saves by writing a new file and renaming it over the config would therefore produce no event on the watched inode, and E19 would then apply to the old inode once it is deleted. [UNKNOWN] not observed. [INF] For a directory path, the directory mask also sees children (K08, E20), so any file written in a watched directory reloads the config.

## Host reads (H rows)

[OBS] H01–H03 are reads of files fetched from the host: a getoption dump, a `source =` list and the version record. They are snapshots of files, not live reads of the compositor. [UNKNOWN] whether the running watch set matches the chain above.

## Rows

Rows are K (source: Hyprland pins and the inotify(7) man page), H (host), and E (extra facts beyond the frozen anchors; the counter ignores E rows).

### Declaration and watch list (K01–K11)

{{K_DECL}}

### Event loop, refresh and reload (K12–K19)

{{K_EVENT}}

### Config path list and source handling (K20–K26)

{{K_PATHS}}

### hyprctl keyword and reload (K27–K28)

{{K_HYPRCTL}}

### inotify(7) semantics (K29–K30)

{{K_INOTIFY}}

### Host (H01–H03)

{{H_ROWS}}

### Extra facts (E01–E20, ignored by the counter)

{{E_ROWS}}

## Limits

- The K and H rows prove quote identity at a pinned line, registry binding and lexical grounding (an identifier shared with the quote, no number absent from the quote). They do not prove that a proposition is entailed by its quote. That is the sentence-to-pin audit and the non-author closure.
- The pins are the fetched files at efb5099, each sha256 frozen in `frozen-tables.json`. They were not re-fetched upstream for this entry.
- The pinned provider path is `src/config/legacy/ConfigManager.cpp`. Nothing pinned shows that the host's Hyprland 0.56.2 build takes this provider path (registration §C2 describes a hyprlang `configProvider`). [UNKNOWN]
- Not in the pins, so not stated as fact: the definitions of `REFRESH_ALL` and `REFRESH_CONFIG_WATCHER`; the trip logic of ConfigValue on parse; what `inotify_add_watch` does on failure beyond the code shown; glob collation; C++ `std::filesystem` rules (cited as [INF]).
- Declared divergences of the C2 watch model (depth cap, glob order, `~user`, the Lua provider, runtime keyword) apply to the tool, not to this entry.
- No event was generated, no reload was observed, no file in any config tree was written, and no compositor state was changed.

## How to verify

Read-only commands. Freeze commit `3423ae285676c2a10273000f4519163472b443db`; lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.

```sh
L=/home/vgpnk/Projects/shokunin/mado-shokunin
R=3423ae285676c2a10273000f4519163472b443db
P=.ufo/waves/round-56/fetch
git -C "$L" show "$R:.ufo/waves/round-56/frozen-tables.json" | sha256sum      # d50d2b7b...f9af
git -C "$L" show "$R:$P/Hyprland-ConfigWatcher.cpp" | sha256sum               # 8383b8ab...d516c
git -C "$L" show "$R:$P/Hyprland-ConfigWatcher.cpp" | sed -n '33,34p'         # K03, K04
git -C "$L" show "$R:$P/Hyprland-ConfigValues.cpp" | sed -n '492p'           # K01, K02
git -C "$L" show "$R:$P/Hyprland-legacy-ConfigManager.cpp" | sed -n '1816p;1835,1836p'   # K24, K22, K21
git -C "$L" show "$R:$P/man7-inotify.7.html" | sed -n '186p;262p'            # K29, K30
cat "$L/$P/host-getoption.json"                                                # H01
sed -n '10p' "$L/$P/host-sources.txt"                                          # H02
sed -n '3p' "$L/$P/host-version.json"                                          # H03
grep -c '^| [KH][0-9][0-9] | ' corpus/knowledge/hyprland-config-autoreload-r56.md   # expect 33 once the entry is in the lane
hyprctl getoption misc:disable_autoreload -j
hyprctl version -j
stat -c '%F %n' ~/.config/hypr/hyprland.conf
readlink -f ~/.config/hypr/hyprland.conf
```
"""


def sh(args, cwd=None):
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LANG": "C.UTF-8", "HOME": os.environ.get("HOME", "/")}
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True, check=True).stdout


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--legs", required=True)
    a = ap.parse_args()
    legs = []

    tables_bytes = open(os.path.join(LANE, TABLES_REL), "rb").read()
    assert sha(tables_bytes) == TABLES_SHA, "tables sha mismatch (working tree)"
    blob_tables = sh(["git", "-C", LANE, "cat-file", "blob", f"{REV}:{TABLES_REL}"])
    assert sha(blob_tables) == TABLES_SHA, "tables sha mismatch (freeze blob)"
    t = json.loads(tables_bytes)
    c1 = t["c1"]

    pins = {}
    for name, want in list(c1["pin_sha256"].items()) + list(c1["host_pin_sha256"].items()):
        wt = open(os.path.join(LANE, PIN_DIR_REL, name), "rb").read()
        blob = sh(["git", "-C", LANE, "cat-file", "blob", f"{REV}:{PIN_DIR_REL}/{name}"])
        assert sha(wt) == want and sha(blob) == want, f"pin sha mismatch {name}"
        assert b"\r" not in wt, f"CR in {name}"
        pins[name] = wt.decode("utf-8").split("\n")
    legs.append(f"pins=ok({len(pins)})")

    sid_pin = c1["rows"]
    for r in c1["k"]:
        assert sid_pin[r["sid"]] == r["pin"], f"sid/pin mismatch {r['id']}"

    frozen_lines = {}
    for r in c1["k"]:
        frozen_lines.setdefault(r["pin"], set()).add(r["line"])
    for r in c1["h"]:
        frozen_lines.setdefault(r["pin"], set()).add(r["line"])

    rows = []  # (id, prop, src, pin, line, quote)
    for r in c1["k"]:
        assert r["quote"] in pins[r["pin"]][r["line"] - 1], f"quote {r['id']}"
        rows.append((r["id"], PROPS[r["id"]], r["sid"], r["pin"], r["line"], r["quote"]))
    for r in c1["h"]:
        assert r["quote"] in pins[r["pin"]][r["line"] - 1], f"quote {r['id']}"
        rows.append((r["id"], PROPS[r["id"]], "host", r["pin"], r["line"], r["quote"]))

    # ---- local replica of the row legs (K/H), for the seat's own check
    failed = []
    seen_props = set()
    for rid, prop, src, pin, line, quote in rows:
        if prop != prop.strip():
            failed.append(f"row:{rid}")
        minlen = 40 if rid.startswith("K") else 20
        if len(prop) < minlen:
            failed.append(f"len:{rid}")
        if prop in seen_props:
            failed.append(f"dup:{rid}")
        seen_props.add(prop)
        for cell in (prop, quote, src, f"{pin}:{line}"):
            if "|" in cell or "\\" in cell or "`" in cell:
                failed.append(f"cell:{rid}")
        if not (set(TOK.findall(prop)) & set(TOK.findall(quote))):
            failed.append(f"tok:{rid}")
        allowed = set(NUM.findall(quote)) | {str(line)} | {str(x) for x in frozen_lines.get(pin, set())} | {"0", "1", "2", "3"}
        if not set(NUM.findall(prop)) <= allowed:
            failed.append(f"num:{rid}:{sorted(set(NUM.findall(prop)) - allowed)}")
    legs.append(f"local_k_h_failed={failed or 'none'}")

    # ---- extra rows
    extra_rows = []
    for rid, sid, pin, line, sub, prop in EXTRA:
        assert sid_pin[sid] == pin, f"E sid/pin {rid}"
        ln = pins[pin][line - 1]
        assert ln.count(sub) == 1, f"E substring not on line {rid}"
        assert "|" not in sub and "`" not in sub and "\\" not in sub, f"E cell {rid}"
        assert set(TOK.findall(prop)) & set(TOK.findall(sub)), f"E tok {rid}"
        allowed = set(NUM.findall(sub)) | {str(line)} | {str(x) for x in frozen_lines.get(pin, set())} | {"0", "1", "2", "3"}
        assert set(NUM.findall(prop)) <= allowed, f"E num {rid}"
        extra_rows.append((rid, prop, sid, pin, line, sub))

    def row(rid, prop, src, pin, line, quote):
        return f"| {rid} | {prop} | {src} | {pin}:{line} | `{quote}` |"

    hdr = "| id | proposition | source | pin:line | quote |\n|---|---|---|---|---|"
    by = {r[0]: r for r in rows}

    def table(ids, extra=False):
        out = [hdr]
        for i in ids:
            rid, prop, src, pin, line, quote = by[i] if not extra else i
            out.append(row(rid, prop, src, pin, line, quote))
        return "\n".join(out)

    def ids(a_, b_, pre="K"):
        return [f"{pre}{n:02d}" for n in range(a_, b_ + 1)]

    text = HEAD
    text = text.replace("{{K_DECL}}", table(ids(1, 11)))
    text = text.replace("{{K_EVENT}}", table(ids(12, 19)))
    text = text.replace("{{K_PATHS}}", table(ids(20, 26)))
    text = text.replace("{{K_HYPRCTL}}", table(ids(27, 28)))
    text = text.replace("{{K_INOTIFY}}", table(ids(29, 30)))
    text = text.replace("{{H_ROWS}}", table(ids(1, 3, "H")))
    text = text.replace("{{E_ROWS}}", "\n".join([hdr] + [row(*x) for x in extra_rows]))
    assert "{{" not in text
    text = text.rstrip("\n") + "\n"
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(text)

    # ---- self-check of the rendered file (row grammar, provenance order, quotes at pin lines)
    lines = text.split("\n")
    head = lines[:30]
    src_i = [i for i, l in enumerate(head) if l.startswith("source:")]
    ver_i = [i for i, l in enumerate(head) if l == "verified-at: 2026-10-28"]
    rec_i = [i for i, l in enumerate(head) if l.startswith("recheck:")]
    prov_ok = len(src_i) == 1 and len(ver_i) == 1 and len(rec_i) == 1 and src_i[0] < ver_i[0] < rec_i[0]
    fence = None
    grammar = re.compile(r"^\| (K[0-9]{2}|H[0-9]{2}) \| (.+) \| (S[0-9]{3}|host) \| ([A-Za-z0-9_.\-/]+:[0-9]+) \| `([^`|]*)` \|$")
    found = {}
    for l in lines:
        s = l
        if re.match(r"^ {0,3}(```|~~~)", s):
            fence = None if fence else "x"
            continue
        if fence:
            continue
        m = grammar.match(s)
        if m and s.startswith(("| K", "| H")):
            found.setdefault(m.group(1), []).append(m)
    ok_rows = 0
    for rid, prop, src, pin, line, quote in rows:
        ms = found.get(rid, [])
        if len(ms) == 1 and ms[0].group(3) == src and ms[0].group(4) == f"{pin}:{line}" and ms[0].group(5) == quote and ms[0].group(2) == prop:
            ok_rows += 1
    legs.append(f"rendered_rows={ok_rows}/33 provenance_order={'ok' if prov_ok else 'BAD'}")
    all_s = set(re.findall(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])", text))
    legs.append(f"cited_S_ids={sorted(all_s)}")
    with open(a.legs, "w", encoding="utf-8") as fh:
        fh.write("\n".join(legs) + "\n")
    print("\n".join(legs))
    print(f"wrote {a.out} ({len(text)} bytes, {len(lines)} lines)")


if __name__ == "__main__":
    sys.exit(main())
