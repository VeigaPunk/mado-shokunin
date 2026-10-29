#!/usr/bin/env python3 -I
"""Seat R56RevC1Contract: build NON-WORK C1 fixture variants in a scratch git repo.

Reads the lane ONLY through `git archive <rev>` (read-only). Writes only under --work.
Variants (see report): cheap, honest, falsified, junk, absent, false-number, dropped-row,
edited-quote, new-row-missing.  The entry is a red-team artefact, never a knowledge claim.
"""
import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile

ENTRY = "corpus/knowledge/hyprland-config-autoreload-r56.md"
SOURCES = "corpus/SOURCES.md"
README = "corpus/README.md"
TABLES = ".ufo/waves/round-56/frozen-tables.json"
COMMIT_ENV = ["-c", "user.name=ctl", "-c", "user.email=ctl@ctl"]
GITENV = {"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "LC_ALL": "C"}
EFB = "efb50993780079460b0cbed1363e2166a2de1d9f"
SID_INFO = {
    "S383": ("Hyprland 0.56.2 ConfigWatcher.cpp - watch list, inotify masks and symlink canonical watch",
             f"https://github.com/hyprwm/Hyprland/blob/{EFB}/src/config/shared/inotify/ConfigWatcher.cpp",
             "watch list construction, inotify masks, symlink canonical watch, event callback"),
    "S384": ("Hyprland 0.56.2 ConfigValues.cpp - misc:disable_autoreload declaration",
             f"https://github.com/hyprwm/Hyprland/blob/{EFB}/src/config/values/ConfigValues.cpp",
             "declaration of the refresh flag and default for misc:disable_autoreload"),
    "S385": ("Hyprland 0.56.2 PropRefresher.cpp - REFRESH_CONFIG_WATCHER dispatch",
             f"https://github.com/hyprwm/Hyprland/blob/{EFB}/src/config/supplementary/propRefresher/PropRefresher.cpp",
             "refresher calls watcher update when the flag is tripped"),
    "S386": ("Hyprland 0.56.2 EventLoopManager.cpp - watcher inotify fd on the Wayland loop",
             f"https://github.com/hyprwm/Hyprland/blob/{EFB}/src/managers/eventLoop/EventLoopManager.cpp",
             "inotify descriptor registered on the event loop and forwarded to the watcher"),
    "S387": ("Hyprland 0.56.2 legacy ConfigManager.cpp - onChange, reload, source handling",
             f"https://github.com/hyprwm/Hyprland/blob/{EFB}/src/config/legacy/ConfigManager.cpp",
             "onChange callback, REFRESH_ALL scheduling, source regular-file and glob handling"),
    "S388": ("Hyprland 0.56.2 MiscFunctions.cpp - HOME and absolutePath helpers",
             f"https://github.com/hyprwm/Hyprland/blob/{EFB}/src/helpers/MiscFunctions.cpp",
             "HOME lookup and relative-path resolution used by source handling"),
    "S389": ("Hyprland 0.56.2 HyprCtl.cpp - keyword disable_autoreload and reload",
             f"https://github.com/hyprwm/Hyprland/blob/{EFB}/src/debug/HyprCtl.cpp",
             "keyword path for misc:disable_autoreload and the reload call"),
    "S390": ("inotify(7) man page - IN_CLOSE_WRITE and symlink semantics",
             "https://man7.org/linux/man-pages/man7/inotify.7.html",
             "close-write event meaning and IN_DONT_FOLLOW symlink behaviour"),
}
SID_BASENAME_NOTE = {}

HONEST = {
    "K01": "The declaration of misc:disable_autoreload defaults to false and documents that true stops reloading on save.",
    "K02": "The same declaration tags misc:disable_autoreload with the refresh flag REFRESH_CONFIG_WATCHER, routing changes to the watcher.",
    "K03": "The watcher reads misc:disable_autoreload as an INTEGER config value when it is constructed.",
    "K04": "When the disable flag is set the watch list becomes an empty vector, otherwise it takes getConfigPaths.",
    "K05": "Each existing watch is removed with inotify_rm_watch before the watch list is rebuilt.",
    "K06": "The path is classified as a directory with std::filesystem::is_directory using an error code out-parameter.",
    "K07": "The file mask is set to IN_CLOSE_WRITE, so a write that closes the file produces an event.",
    "K08": "directoryMask is assigned from fileMask, so directories share the same flag set.",
    "K09": "Each path is registered with inotify_add_watch using the mask chosen for its type.",
    "K10": "A symlink entry adds the extra canonical watch only when neither error code is set and IS_SYMLINK holds.",
    "K11": "The canonical target gets its own inotify_add_watch with IN_CLOSE_WRITE as the only mask bit.",
    "K12": "Each inotify event is delivered to the stored m_watchCallback as an SConfigWatchEvent value.",
    "K13": "The watcher descriptor is registered on the Wayland loop as a readable source by wl_event_loop_add_fd.",
    "K14": "The event loop calls onInotifyEvent on the watcher when the inotify descriptor becomes readable.",
    "K15": "The refresher checks whether the REFRESH_CONFIG_WATCHER bit is set in its tripped property mask.",
    "K16": "When that bit is set the refresher calls update on the config watcher to rebuild its watch list.",
    "K17": "The legacy config manager registers an onChange callback on the watcher through setOnChange.",
    "K18": "The callback logs that a config file was modified and that reloading follows, using that wording.",
    "K19": "The reload path schedules a REFRESH_ALL refresh through the supplementary refresher scheduleRefresh call.",
    "K20": "The config path list is cleared with m_configPaths.clear() before a fresh parse begins.",
    "K21": "Each accepted source value is appended to m_configPaths with emplace_back during the parse.",
    "K22": "Only a regular file is appended as a parsed config path; is_regular_file checks the file status.",
    "K23": "A source value that names a directory is skipped with a log line saying skipping directory.",
    "K24": "The source path is expanded with glob using GLOB_TILDE after absolutePath resolves it against the current path.",
    "K25": "ENVHOME caches the HOME environment variable through getenv at first use.",
    "K26": "The directory of the current file is the part of currentPath before its last slash, found with find_last_of.",
    "K27": "The hyprctl keyword handler checks whether the command contains misc:disable_autoreload before dispatch.",
    "K28": "The keyword path calls reload on the config manager, which rereads the configuration.",
    "K29": "A file opened for writing that is then closed produces the close-write event that the watcher subscribes to.",
    "K30": "The watch is not followed when pathname is a symbolic link, because inotify does not dereference symbolic links.",
    "H01": "The live getoption dump reports misc:disable_autoreload with int 0 on the host.",
    "H02": "The host config tree sources the omarchy theme file hyprland.conf through its source line.",
    "H03": "The host version record names the commit that the pinned source files were fetched at, as a full identifier.",
}
FALSIFIED = dict(HONEST)
FALSIFIED["K04"] = "When the disable flag is set, setWatchList keeps only the main config path and drops every sourced file."
FALSIFIED["K13"] = "wl_event_loop_add_fd registers the watcher descriptor as a writable source, so the loop wakes when it can be written."
FALSIFIED["K20"] = "m_configPaths.clear() keeps the sourced paths and only resets the main config path before a parse."


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=GITENV)
    if check and r.returncode != 0:
        sys.exit(f"make_variant: git {' '.join(args)} failed: {r.stderr.decode()[:300]}")
    return r


def cheap_prop(rid, pin, line, quote):
    idents = re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", quote)
    tok = idents[0]
    if rid.startswith("K"):
        return f"Line {line} of the pinned file holds {tok}, which this row cites for the reload path."
    return f"Host capture {rid} records {tok} on line {line} of the host pin."


def junk_prop(rid):
    if rid.startswith("K"):
        return f"placeholder proposition text for row {rid}, not a claim about any source line"
    return f"placeholder host proposition {rid}, not a read"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--variant", required=True,
                    choices=["cheap", "honest", "falsified", "junk", "absent", "false-number",
                             "dropped-row", "edited-quote", "new-row-missing"])
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    fx = os.path.realpath(os.path.join(a.work, "fx-" + a.variant))
    if os.path.exists(fx):
        sys.exit("make_variant: fixture exists; use a fresh --work")
    os.makedirs(fx)
    git(fx, "init", "-q")
    top = git(fx, "rev-parse", "--show-toplevel").stdout.decode().strip()
    assert os.path.realpath(top) == fx, (top, fx)
    arc = subprocess.run(["git", "-C", a.lane, "archive", a.rev], capture_output=True, env=GITENV)
    if arc.returncode != 0:
        sys.exit("make_variant: git archive failed")
    # system tar preserves symlinks verbatim (the lane holds absolute symlink fixtures)
    tx = subprocess.run(["tar", "-x", "-C", fx], input=arc.stdout, capture_output=True)
    if tx.returncode != 0:
        sys.exit("make_variant: tar -x failed: " + tx.stderr.decode()[:300])

    tables = json.load(open(os.path.join(fx, TABLES), encoding="utf-8"))["c1"]
    rows = tables["k"] + tables["h"]
    by_id = {r["id"]: r for r in rows}

    # ---- entry
    if a.variant != "absent":
        props = {}
        for r in rows:
            rid = r["id"]
            if a.variant == "junk":
                props[rid] = junk_prop(rid)
            elif a.variant == "honest":
                props[rid] = HONEST[rid]
            elif a.variant == "falsified":
                props[rid] = FALSIFIED[rid]
            else:
                props[rid] = cheap_prop(rid, r["pin"], r["line"], r["quote"])
        if a.variant == "false-number":
            props["K04"] = props["K04"] + " The value is capped at 200 by this call."
        out = []
        out.append("# Hyprland config auto-reload chain on 0.56.2 - NON-WORK FIXTURE")
        out.append("")
        out.append("source: " + ", ".join(tables["new_row_ids"]))
        out.append("verified-at: 2026-10-28")
        out.append("recheck: on-release")
        out.append("")
        out.append("NON-WORK red-team fixture (seat R56RevC1Contract). Not a knowledge claim.")
        out.append("")
        out.append("## Rows")
        out.append("")
        for r in rows:
            rid = r["id"]
            if a.variant == "dropped-row" and rid == "K17":
                continue
            quote = r["quote"]
            if a.variant == "edited-quote" and rid == "K05":
                quote = quote.replace("watch.wd", "watch.wx")
            src = r.get("sid", "host")
            out.append(f"| {rid} | {props[rid]} | {src} | {r['pin']}:{r['line']} | `{quote}` |")
        text = "\n".join(out) + "\n"
        os.makedirs(os.path.dirname(os.path.join(fx, ENTRY)), exist_ok=True)
        open(os.path.join(fx, ENTRY), "w", encoding="utf-8").write(text)

    # ---- registry rows (append after S382)
    src_path = os.path.join(fx, SOURCES)
    src_lines = open(src_path, encoding="utf-8").read().split("\n")
    anchor_idx = [i for i, l in enumerate(src_lines) if l.startswith("| S382 |")]
    assert len(anchor_idx) == 1, anchor_idx
    new_rows = []
    line_map = {}
    for r in rows:
        if "sid" in r:
            line_map.setdefault(r["sid"], []).append(r["line"])
    for sid in tables["new_row_ids"]:
        if a.variant == "new-row-missing" and sid == "S390":
            continue
        title, url, teaches = SID_INFO[sid]
        pin = tables["rows"][sid]
        base = os.path.basename(tables["pin_suffix"][pin])
        if a.variant in ("honest", "falsified"):
            locs = ",".join(str(x) for x in sorted(set(line_map[sid])))
            anchor = f"{base}:{locs}"
        else:
            # whole-file anchor: the cheapest range that covers every cited line
            anchor = f"{base}:1-{max(line_map[sid]) + 999}"
        scope = "source lines cited by the rows of this entry"
        used_by = ENTRY
        new_rows.append(f"| {sid} | {title} - {url} | {'docs' if sid == 'S390' else 'code'} | A | {scope} | {anchor} | {teaches} | mined | 2026-10-28 | on-release | {used_by} |")
    src_lines[anchor_idx[0]+1:anchor_idx[0]+1] = new_rows
    open(src_path, "w", encoding="utf-8").write("\n".join(src_lines))

    # ---- README index line
    rp = os.path.join(fx, README)
    rl = open(rp, encoding="utf-8").read().split("\n")
    k = [i for i, l in enumerate(rl) if l.startswith("| `knowledge/hyprland-keyboard-repeat-numlock-r55.md`")]
    assert len(k) == 1
    rl.insert(k[0] + 1, "| `knowledge/hyprland-config-autoreload-r56.md` (MADO-R56-1, NON-WORK fixture) | red-team fixture | none |")
    open(rp, "w", encoding="utf-8").write("\n".join(rl))

    git(fx, "add", "-A")
    git(fx, *COMMIT_ENV, "commit", "-q", "-m", f"variant {a.variant}")
    head = git(fx, "rev-parse", "HEAD").stdout.decode().strip()
    print(json.dumps({"fixture": fx, "variant": a.variant, "head": head}))


if __name__ == "__main__":
    main()
