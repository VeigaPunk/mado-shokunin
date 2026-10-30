#!/usr/bin/env python3
"""R56W3CritC1Forge -- CONSOLIDATED clean run against the lane tip 0f3a5436.

One fresh scratch clone per run; every variant is a single commit on top of the
base tip commit; the working tree is hard-reset to the base commit between
variants so no variant can contaminate the next.

Writes the deliverable receipt to the lane's w3 seat directory.
"""
import difflib
import json
import os
import re
import shutil
import subprocess
import sys

SEAT = "R56W3CritC1Forge"
S = "/fast/scratch/hyaku/mado-r56/R56W3CritC1Forge"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "0f3a54361a9824484d0801679ceb1fd8ac7c32e1"
ENTRY = "corpus/knowledge/hyprland-config-autoreload-r56.md"
REGISTRY = "corpus/SOURCES.md"
COUNTER = "quality/counters/c1-r56-autoreload-entry.py"
HARNESS = "quality/check-r56-controls.py"
C3 = "quality/counters/c3-r56-used-by.py"
OUTDIR = LANE + "/.ufo/waves/round-56/w3/" + SEAT
ROW_RE = re.compile(r"^\| ([KHE]\d\d) \|")
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")


def git(w, *args, check=True):
    p = subprocess.run(["git", "-C", w] + list(args), capture_output=True)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (args[:2], p.stderr.decode()[:400]))
    return p.stdout


def show(w, path, rev=REV):
    return git(w, "show", "%s:%s" % (rev, path)).decode("utf-8")


def rows_of(text):
    return [(i + 1, m.group(1), l[2:-2].split(" | "))
            for i, l in enumerate(text.split("\n")) if (m := ROW_RE.match(l))]


def set_cell(text, rid, idx, val):
    lines = text.split("\n")
    for i, l in enumerate(lines):
        m = ROW_RE.match(l)
        if m and m.group(1) == rid:
            cells = l[2:-2].split(" | ")
            cells[idx] = val
            lines[i] = "| " + " | ".join(cells) + " |"
            return "\n".join(lines)
    raise SystemExit("row %s not found" % rid)


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, cwd=S)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


# ------------------------------------------------------------------ rewrites
PARA = {
 "K01": "misc:disable_autoreload is registered in the value table as a Bool whose help string says the configuration does not reload itself on save, and whose third argument is false; what that argument stands for (the default) is declared in ConfigValues.hpp, which this round does not pin.",
 "K02": "the registration assigns Supplementary::REFRESH_CONFIG_WATCHER to the refresh field of this declaration.",
 "K03": "inside update, the option misc:disable_autoreload is stored as a CConfigValue whose type is INTEGER, on this line.",
 "K04": "setWatchList receives an empty vector when the cached PDISABLEAUTORELOAD is non-zero, and receives the getConfigPaths() result in every other case.",
 "K05": "the loop issues one inotify_rm_watch per entry of the watch list, passing that entry's wd, and the return value is never examined; a wd that appears twice is therefore removed twice and the second removal fails (inference from the inotify man page).",
 "K06": "std::filesystem::is_directory is called with path and with the error code ecDir on this line.",
 "K07": "this declaration assigns the inotify event bit IN_CLOSE_WRITE to the variable fileMask; the same source line additionally ORs in IN_DONT_FOLLOW, which the quoted prefix does not show.",
 "K08": "fileMask is the initializer of the variable directoryMask on this line, and that same source line ORs in IN_CREATE, IN_DELETE, IN_MOVED_TO and IN_MOVED_FROM, which the quoted prefix does not show.",
 "K09": "this call registers path.c_str() with the mask variable on the inotify instance m_inotifyFd.",
 "K10": "the canonical watch is added only when both error codes are clear and IS_SYMLINK holds, as this condition requires.",
 "K11": "the second watch is registered on CANONICAL.c_str() with IN_CLOSE_WRITE as the only mask argument.",
 "K12": "for a watch that matches, the event handler invokes m_watchCallback with a freshly built SConfigWatchEvent on this line.",
 "K13": "the FD descriptor is registered here with the Wayland event loop as a readable source whose callback is configWatcherWrite.",
 "K14": "the event-loop callback calls onInotifyEvent on the watcher that Config::watcher() returns; none of the callback's fd, mask or data arguments is passed on, and the watcher reads its own inotify descriptor.",
 "K15": "the branch of this guard is entered only if the bit mask m_propsTripped contains REFRESH_CONFIG_WATCHER.",
 "K16": "the guarded statement invokes update on the object returned by Config::watcher(); that function, as shown in ConfigWatcher.cpp, rebuilds the watch list from the config paths.",
 "K17": "init installs a change callback with setOnChange on the config watcher, and the callback takes an SConfigWatchEvent argument.",
 "K18": "the debug line emits a reload message for the modified config file and hands the event's file field to it as its argument.",
 "K19": "a refresh is scheduled here with the flag REFRESH_ALL on the Supplementary refresher.",
 "K20": "resetHLConfig empties the list of m_configPaths at this line, discarding what the list held before.",
 "K21": "handleSource appends every regular-file match to m_configPaths with emplace_back at this line, before the matched file is parsed; one call can add several entries, and a directory, a non-regular file or a failed glob adds none.",
 "K22": "this condition examines file_status with std::filesystem::is_regular_file, the branch of handleSource that handles regular files.",
 "K23": "the warning written here says that the source= match value is skipped because it is a directory.",
 "K24": "the glob call is given absolutePath of rawpath resolved against m_configCurrentPath, together with the GLOB_TILDE flag.",
 "K25": "the static pointer ENVHOME is initialized from getenv of the variable HOME on this line.",
 "K26": "currentDir is the text of currentPath cut by substr at the last slash that find_last_of locates, on this line.",
 "K27": "the dispatch guard of the keyword path checks whether COMMAND contains the text misc:disable_autoreload; the following line then calls Config::watcher()->update(). The quoted line does not show that body.",
 "K28": "the handler of the reload request calls reload on the object returned by Config::mgr() on this line.",
 "K29": "the description text says that this event is produced by a file that was opened for writing and then closed, the write-close case.",
 "K30": "the description says the pathname is not dereferenced while it is a symbolic link.",
 "H01": "the captured hyprctl getoption record lists misc:disable_autoreload with an int value of zero on this host.",
 "H02": "the captured list of host sources names the omarchy theme file hyprland.conf as the target of a source line.",
 "H03": "the captured record of the version states the commit field of the Hyprland build running on this host.",
}

FALSE = {
 "K01": "misc:disable_autoreload is registered in the value table as a Bool whose help string says the configuration reloads itself on save, and whose third argument is false.",
 "K02": "the registration assigns no refresh field here; Supplementary::REFRESH_CONFIG_WATCHER occurs in the struct only as a comment.",
 "K03": "inside update, the option misc:disable_autoreload is stored as a CConfigValue whose type is FLOAT, on this line.",
 "K04": "setWatchList receives the getConfigPaths() result when the cached PDISABLEAUTORELOAD is non-zero, and receives an empty vector in every other case.",
 "K05": "the loop issues one inotify_rm_watch per entry of the watch list and examines the returned value, so a wd that appears twice is removed only once.",
 "K06": "this line calls std::filesystem::is_directory on path and passes the error code ecDir to it, so a failing path makes the call throw.",
 "K07": "the variable fileMask is assigned the inotify event bit IN_CLOSE_WRITE here, and the same source line leaves every other bit of that mask clear.",
 "K08": "fileMask is the initializer of the variable directoryMask on this line, and that same source line ORs in IN_CREATE alone, leaving IN_DELETE, IN_MOVED_TO and IN_MOVED_FROM out.",
 "K09": "this call registers path.c_str() with the mask variable on the inotify instance m_inotifyFd, and the descriptor it returns is validated against a failure code before the entry is kept.",
 "K10": "the canonical watch is added whenever IS_SYMLINK holds, and the two error codes are not consulted on this line.",
 "K11": "the second watch is registered on CANONICAL.c_str() with the directory mask as its only argument.",
 "K12": "for a watch that matches, the event handler invokes m_watchCallback with a freshly built SConfigWatchEvent that carries the kernel's event name.",
 "K13": "the FD descriptor is registered here with the Wayland event loop as a writable source whose callback is configWatcherWrite.",
 "K14": "the event-loop callback calls onInotifyEvent on the watcher that Config::watcher() returns, and it forwards the fd, mask and data arguments of the callback.",
 "K15": "the branch of this guard is entered only if the bit mask m_propsTripped lacks REFRESH_CONFIG_WATCHER.",
 "K16": "the guarded statement invokes update on the object returned by Config::watcher(); that function, as shown in ConfigWatcher.cpp, clears the config paths and parses them again.",
 "K17": "init installs a change callback with setOnChange on the config watcher, and the callback takes no SConfigWatchEvent argument.",
 "K18": "the debug line emits a reload message for the modified config file and hands the event's mask field to it as its argument.",
 "K19": "a refresh is scheduled here with the flag REFRESH_ALL on the Supplementary refresher, and this flag touches the config watcher bit alone.",
 "K20": "resetHLConfig empties the list of m_configPaths at this line, after the new main path has already been appended.",
 "K21": "handleSource appends every regular-file match to m_configPaths with emplace_back at this line, after the matched file has been parsed.",
 "K22": "this condition examines file_status with std::filesystem::is_regular_file, the branch of handleSource that handles directories.",
 "K23": "the warning written here says that the source= match value is skipped because it is a non-regular file such as a fifo or a socket.",
 "K24": "the glob call is given absolutePath of rawpath resolved against the working directory rather than against m_configCurrentPath, together with the GLOB_TILDE flag.",
 "K25": "the static pointer ENVHOME is initialized from getenv of the variable USER on this line.",
 "K26": "currentDir is the text of currentPath cut by substr at the first slash that find_last_of locates, on this line.",
 "K27": "the dispatch guard of the keyword path checks whether COMMAND contains the text misc:disable_autoreload; the following line then calls Config::mgr()->reload().",
 "K28": "the handler of the reload request calls reload on the object returned by Config::watcher() on this line.",
 "K29": "the description text says that this event is produced by a file that was opened for reading and then closed.",
 "K30": "the description says the pathname is dereferenced even while it is a symbolic link.",
 "H01": "the captured hyprctl getoption record lists misc:disable_autoreload with an int value of one on this host.",
 "H02": "the captured list of host sources names the omarchy theme file hyprland.conf as the target of a source line, and lists no other omarchy file.",
 "H03": "the captured record of the version states the commit field of the Hyprland build running on this host, and that commit differs from the pinned one.",
}

NEG3 = {
 "K04": "This line does not give setWatchList an empty vector when the cached PDISABLEAUTORELOAD value is non-zero; the getConfigPaths() result is handed over in that case instead.",
 "K15": "The branch of this guard is entered only when the bit mask m_propsTripped does NOT contain REFRESH_CONFIG_WATCHER.",
 "H01": "The captured hyprctl getoption record lists misc:disable_autoreload with an int value that is not zero on this host.",
}

PROSE_SUBS = [
    ("The watch list is therefore rebuilt after every `reload()` from the then-current `m_configPaths`",
     "The watch list is therefore NEVER rebuilt after any `reload()` and keeps the first list it ever saw"),
    ("A missing `source` target never enters the list.",
     "A missing `source` target always enters the list and is watched as a missing path."),
    ("No deduplication.",
     "Every path is deduplicated, so a file reached twice is watched once."),
    ("- `~`: the first byte is replaced by the value of `HOME`",
     "- `~`: the first byte is replaced by the value of `USER`"),
    ("The event `name` field is never read, so the reported path is the watch's stored path, not the name the kernel reports.",
     "The event `name` field is the reported path, so the kernel's name replaces the watch's stored path."),
    ("`resetHLConfig()` (`legacy:764-786`) clears the list (776; K20), adds the main path (777-779)",
     "`resetHLConfig()` (`legacy:764-786`) adds the main path first (777-779) and clears the list afterwards (776; K20)"),
]

W = S + "/W2"


def fresh_clone():
    if os.path.isdir(W):
        shutil.rmtree(W)
    subprocess.run(["git", "clone", "--shared", "--no-checkout", LANE, W], check=True, capture_output=True)
    assert git(W, "rev-parse", "--show-toplevel").decode().strip() == W, "toplevel mismatch"
    git(W, "checkout", "-q", REV)


def commit(w, text, name, path=ENTRY):
    with open(os.path.join(w, path), "w", encoding="utf-8") as f:
        f.write(text)
    git(w, "add", path)
    git(w, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "--allow-empty", "-m", "forge:" + name)
    return git(w, "rev-parse", "HEAD").decode().strip()


def reset_base(w):
    git(w, "reset", "-q", "--hard", REV)
    git(w, "clean", "-qfd")


def measure(w, text, name, path=ENTRY, diffbase=None):
    sha = commit(w, text, name, path)
    rc1, o1, e1 = run([sys.executable, "-I", LANE + "/" + COUNTER, "--repo", w, "--rev", sha, "--work", S + "/work/c-" + name])
    rc2, o2, e2 = run([sys.executable, "-I", LANE + "/" + HARNESS, "--claim", "c1", "--repo", w, "--rev", sha, "--work", S + "/work/h-" + name])
    rc3, o3, e3 = run([sys.executable, "-I", LANE + "/" + C3, "--repo", w, "--rev", sha, "--work", S + "/work/c3-" + name])
    good = [l for l in e2.split("\n") if l.startswith("good:")]
    fails = [l.strip() for l in e2.split("\n") if "FAIL" in l]
    reset_base(w)
    return dict(name=name, sha=sha, counter=o1.strip(), counter_rc=rc1,
                harness=o2.strip(), good=(good[0] if good else "(none)"), fails=fails,
                c3=o3.strip(), c3_rc=rc3,
                diff=(diffbase if diffbase is not None else text))


def main():
    os.makedirs(S + "/work", exist_ok=True)
    os.makedirs(OUTDIR + "/receipts", exist_ok=True)
    fresh_clone()
    base = show(W, ENTRY)
    base_reg = show(W, REGISTRY)
    K = {r: c for _, r, c in rows_of(base)}
    R = []
    summary = []

    # ---------------- re-verification 1: quote at pin line
    bad = []
    for rid, cells in ((r, c) for _, r, c in rows_of(base)):
        pin, _, line = cells[3].rpartition(":")
        pl = show(W, ".ufo/waves/round-56/fetch/" + pin).split("\n")
        if not (line.isdigit() and 1 <= int(line) <= len(pl) and cells[4][1:-1] in pl[int(line) - 1]):
            bad.append(rid)
    R.append("RE-VERIFICATION 1  every row quote (K, H and E) present at its stated pin line: 42 rows checked, failures: %s"
             % (bad or "none"))
    R.append("")

    # ---------------- re-verification 2: quote is the whole line or a fragment
    frag = []
    for rid, cells in ((r, c) for _, r, c in rows_of(base) if r[0] in "KH"):
        pin, _, line = cells[3].rpartition(":")
        raw = show(W, ".ufo/waves/round-56/fetch/" + pin).split("\n")[int(line) - 1]
        if raw.strip() != cells[4][1:-1]:
            frag.append(rid)
    R.append("RE-VERIFICATION 2  frozen quote is a FRAGMENT of the pin line (not the whole line) in %d of 33 K/H rows: %s"
             % (len(frag), " ".join(frag)))
    R.append("")

    # ---------------- re-verification 3: token grounding, tip vs w2
    def tokstat(text, label):
        out = tot = 0
        rows = 0
        for rid, cells in ((r, c) for _, r, c in rows_of(text) if r[0] in "KH"):
            pt = set(TOKEN_RE.findall(cells[1]))
            qt = set(TOKEN_RE.findall(cells[4][1:-1]))
            out += len(pt - qt)
            tot += len(pt)
            if len(pt - qt) > 1:
                rows += 1
        return "%s: rows with >1 proposition token absent from the quote: %d/33 ; absent tokens %d of %d" % (label, rows, out, tot)

    R.append("RE-VERIFICATION 3  " + tokstat(base, "tip "))
    R.append("RE-VERIFICATION 3  " + tokstat(show(W, ENTRY, "28fc86ac2359ec27406d8a2c63bef82ea6e947ed"), "w2  "))
    R.append("")

    # ---------------- re-verification 4: which registry rows no C1 leg reads
    tables = json.loads(show(W, ".ufo/waves/round-56/frozen-tables-v2.json"))
    read = {r["sid"] for r in tables["c1"]["k"]} | set(tables["c1"]["new_row_ids"])
    allrows = sorted(set(re.findall(r"^\|\s*(S\d{3,})\s*\|", base_reg, re.M)))
    untouched = [s for s in allrows if s not in read]
    R.append("RE-VERIFICATION 4  registry rows read by a C1 leg (source_cell/scope/new_rows): %s" % sorted(read))
    R.append("RE-VERIFICATION 4  registry rows in SOURCES.md: %d ; rows NO C1 leg reads: %d ; S391..S395 among them: %s"
             % (len(allrows), len(untouched), [s for s in untouched if 391 <= int(s[1:]) <= 395]))
    R.append("RE-VERIFICATION 4  the frozen tables have no 'e' row list: c1 keys = %s" % sorted(tables["c1"].keys()))
    R.append("")

    # ---------------- variants
    def add(name, text, path=ENTRY):
        s = measure(W, text, name, path)
        summary.append(s)
        return s

    s = add("base-honest", base)
    R.append("VARIANT base-honest  (control: the tip entry unchanged)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    t = base
    for rid, p in PARA.items():
        t = set_cell(t, rid, 1, p)
    s = add("para33-lexical-paraphrase-all-33", t)
    R.append("VARIANT para33-lexical-paraphrase-all-33  (my own rewrite of every one of the 33 propositions; meaning preserved)")
    R.append("  diff vs tip: 66 lines (all 33 proposition cells replaced; src/pin/quote cells untouched)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    t = base
    for rid, p in FALSE.items():
        t = set_cell(t, rid, 1, p)
    s = add("false33-semantic-falsification-all-33", t)
    R.append("VARIANT false33-semantic-falsification-all-33  (my own rewrite of every one of the 33 propositions; each one FALSE of its pinned line)")
    R.append("  diff vs tip: 66 lines (all 33 proposition cells replaced; src/pin/quote cells untouched)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    t = base
    for rid, p in NEG3.items():
        t = set_cell(t, rid, 1, p)
    s = add("neg3-semantic-negation-K04-K15-H01", t)
    R.append("VARIANT neg3-semantic-negation-K04-K15-H01  (three propositions of my choice semantically negated)")
    R.append("  diff vs tip: 6 lines (K04, K15, H01 proposition cells)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    # shuffled row order
    lines = base.split("\n")
    pos = [i for i, l in enumerate(lines) if ROW_RE.match(l)
           and ROW_RE.match(l).group(1) in (set("K%02d" % k for k in range(1, 31)) | set("H%02d" % k for k in range(1, 4)))]
    import random
    rng = random.Random(20261030)
    for sl in (pos[:30], pos[30:33]):
        vals = [lines[i] for i in sl]
        rng.shuffle(vals)
        for i, v in zip(sl, vals):
            lines[i] = v
    t = "\n".join(lines)
    s = add("shuffle-row-order", t)
    R.append("VARIANT shuffle-row-order  (the 30 K rows shuffled inside the K table, the 3 H rows inside the H table; each row keeps its own id/proposition/quote)")
    R.append("  diff vs tip: 56 lines (row order only; every row's content unchanged)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    # cheapest forgeries
    CHEAP = [
        ("cheap1-K30-delete-not", "K30", "The description says the pathname is dereferenced while it is a symbolic link.",
         "K30", "not dereferenced", "dereferenced"),
        ("cheap1-K25-HOME-to-USER", "K25", "The static ENVHOME pointer takes its value from getenv of the USER variable on this line.",
         "K25", "HOME", "USER"),
        ("cheap1-H01-zero-to-one", "H01", "The captured hyprctl getoption record reports misc:disable_autoreload with an int value of one on this host.",
         "H01", "zero", "one"),
        ("cheap1-K18-file-to-mask", "K18", "The debug line logs a reload message for the modified config file and passes the event's mask field as its argument.",
         "K18", "file", "mask"),
    ]
    for name, rid, newprop, rid2, oldw, neww in CHEAP:
        before = K[rid][1]
        t = set_cell(base, rid, 1, newprop)
        s = add(name, t)
        R.append("VARIANT %s  (%s proposition, %r -> %r; Levenshtein over the whole proposition = %d characters)"
                 % (name, rid, oldw, neww, lev(before, newprop)))
        R.append("  counter: %s" % s["counter"])
        R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
        R.append("  C3: %s" % s["c3"])
        R.append("")

    # E-row surface (rows the frozen predicate does not count)
    t = base
    for rid in ("E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09"):
        t = set_cell(t, rid, 4, "`this line does not exist in any pinned file`")
    s = add("eforge-e-rows-fake-quotes", t)
    R.append("VARIANT eforge-e-rows-fake-quotes  (all 9 E-row quote cells replaced by text present in NO pin file)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    t = base
    for rid in ("E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09"):
        t = set_cell(t, rid, 1, "This line is not what the pinned file says: the quoted text is never reached at run time.")
    s = add("eforge-e-rows-false-propositions", t)
    R.append("VARIANT eforge-e-rows-false-propositions  (all 9 E-row propositions replaced by a denial; quote cells untouched)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    t = base
    for rid in ("E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09"):
        t = set_cell(t, rid, 2, "S999")
    s = add("eforge-e-rows-src-S999", t)
    R.append("VARIANT eforge-e-rows-src-S999  (all 9 E-row src cells set to the non-existent registry id S999)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    # a brand-new E row citing a non-existent registry id and a non-existent pin file
    lines = base.split("\n")
    last = max(i for i, l in enumerate(lines) if l.startswith("| E"))
    lines.insert(last + 1,
                 "| E10 | The reset helper also truncates the watch descriptor table so that no stale watch survives a rebuild "
                 "(this row has no anchor in any pin and cites no registry row) | S396 | Hyprland-NotARealFile.cpp:1 "
                 "| `inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask)` |")
    s = add("eforge-new-e-row-S396-fake-pin", "\n".join(lines))
    R.append("VARIANT eforge-new-e-row-S396-fake-pin  (a NEW row E10: non-existent registry id S396, non-existent pin file, fabricated quote, false proposition)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    # duplicate authority across the 33/42 boundary
    s = add("dup-K01-into-E01", set_cell(base, "E01", 1, K["K01"][1]))
    R.append("VARIANT dup-K01-into-E01  (E01's proposition set byte-identical to K01's -- uniqueness check across the 33/42 boundary)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    s = add("dup-K01-into-K02-POSITIVE-CONTROL", set_cell(base, "K02", 1, K["K01"][1]))
    R.append("VARIANT dup-K01-into-K02-POSITIVE-CONTROL  (K02's proposition = K01's, inside the counted 33 -- the uniqueness check must fire)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    # echo-off row: quote shorter than 30 chars
    q = K["K28"][4][1:-1]
    prop = ("The pinned line reads exactly %s and proves the opposite of what it appears to say: the reload request "
            "handler never reaches the watcher and no watch list is ever rebuilt." % q)
    s = add("echo-off-K28-quote-echoed-plus-denial", set_cell(base, "K28", 1, prop))
    R.append("VARIANT echo-off-K28-quote-echoed-plus-denial  (K28's frozen quote is %d chars < ECHO_MIN 30, so the echo leg is OFF; the quote is embedded verbatim plus a denial)" % len(q))
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    # prose body falsification
    t = base
    for old, new in PROSE_SUBS:
        assert old in t, old[:60]
        t = t.replace(old, new)
    s = add("prose-false-6-load-bearing-claims", t)
    R.append("VARIANT prose-false-6-load-bearing-claims  (six load-bearing PROSE claims inverted; both row tables untouched)")
    R.append("  diff vs tip: 12 lines (6 prose lines)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    # prose + row together
    t2 = t.replace(K["K18"][1], "The debug line logs a reload message for the modified config file and passes the event's mask field as its argument.")
    s = add("prose-false-plus-K18-one-word", t2)
    R.append("VARIANT prose-false-plus-K18-one-word  (the six prose inversions AND the one-word K18 change)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    # registry rows S391-S395: no C1 leg reads them
    reg = base_reg.split("\n")
    out = []
    for l in reg:
        m = re.match(r"^ {0,3}\|\s*(S39[1-5])\s*\|", l)
        if m:
            cells = l.strip().strip("|").split("|")
            cells[3] = " C"
            cells[5] = " NoSuchFile.cpp:1-9999 @ efb50993780079460b0cbed1363e2166a2de1d9f; anchor does not exist "
            cells[6] = " this source teaches nothing at all and its quoted line is never executed "
            cells[7] = " rejected"
            cells[8] = " 1999-01-01"
            l = "|" + "|".join(cells) + "|"
        out.append(l)
    s = add("reg-S391-395-dead-and-bogus", "\n".join(out), path=REGISTRY)
    R.append("VARIANT reg-S391-395-dead-and-bogus  (S391..S395: tier->C, status->rejected, opened->1999-01-01, anchor->a file that does not exist, teaches->a denial)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    # scope bound one past EOF (wave-2 D2)
    out = []
    for l in reg:
        m = re.match(r"^ {0,3}\|\s*S383\s*\|", l)
        if m:
            cells = l.strip().strip("|").split("|")
            cells[5] = " ConfigWatcher.cpp:1-112 "
            l = "|" + "|".join(cells) + "|"
        out.append(l)
    s = add("scope-S383-1-112-one-past-EOF", "\n".join(out), path=REGISTRY)
    R.append("VARIANT scope-S383-1-112-one-past-EOF  (S383 anchor ConfigWatcher.cpp:1-112; the file has 111 lines)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    # whole-file anchor
    out = []
    for l in reg:
        m = re.match(r"^ {0,3}\|\s*S383\s*\|", l)
        if m:
            cells = l.strip().strip("|").split("|")
            cells[5] = " ConfigWatcher.cpp:1-111 "
            l = "|" + "|".join(cells) + "|"
        out.append(l)
    s = add("scope-S383-1-111-whole-file", "\n".join(out), path=REGISTRY)
    R.append("VARIANT scope-S383-1-111-whole-file  (S383 anchor covers the whole file -> the scope leg is vacuous for the S383 rows)")
    R.append("  counter: %s" % s["counter"])
    R.append("  harness: %s   | %s" % (s["harness"], s["good"]))
    R.append("  C3: %s" % s["c3"])
    R.append("")

    with open(S + "/forge-final-summary.json", "w") as f:
        json.dump(summary, f, indent=1)
    with open(S + "/forge-final-report.txt", "w") as f:
        f.write("\n".join(R) + "\n")
    print("\n".join(R))


if __name__ == "__main__":
    main()
