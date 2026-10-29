#!/usr/bin/env python3
"""Generate the C1 entry (corpus/knowledge/hyprland-config-autoreload-r56.md draft).

K/H rows: pin cell and quote cell come from frozen-tables.json and the fetch pins; this file writes
only the proposition cells. E rows (extra, not counted) quote a stripped pin line by number.
Self-checks replicate registration.md legs row, quote, tok, num, prop length, and the provenance order.
Usage: python3 -I gen-entry.py [--out PATH]
"""
import hashlib
import json
import os
import re
import sys

ROOT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56"
PINS = os.path.join(ROOT, "fetch")
TABLES = os.path.join(ROOT, "frozen-tables.json")
TABLES_SHA = "d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.md")
TEMPLATE = os.path.join(HERE, "entry.tmpl.md")

TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
NUM = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")

# ---- propositions for the frozen K rows (quote is never written here) ----
K_PROP = {
    "K01": "The misc:disable_autoreload option is declared with help text saying the config will not reload automatically on save, and a default of false.",
    "K02": "The declaration sets its refresh field to the flag Supplementary::REFRESH_CONFIG_WATCHER on this line.",
    "K03": "The update function caches the misc:disable_autoreload option as a CConfigValue of the INTEGER type on this line.",
    "K04": "When the cached PDISABLEAUTORELOAD value is non-zero, setWatchList is given an empty vector; otherwise it is given the getConfigPaths() result.",
    "K05": "This call removes one existing watch, identified by its watch.wd descriptor, from the m_inotifyFd inotify instance.",
    "K06": "This line calls std::filesystem::is_directory on path and passes the error code ecDir to it.",
    "K07": "The fileMask variable is assigned the IN_CLOSE_WRITE inotify event bit in this declaration.",
    "K08": "The directoryMask variable is initialised from fileMask on this line, so it starts from the same bits.",
    "K09": "This call registers path.c_str() with the mask variable on the m_inotifyFd inotify instance.",
    "K10": "This condition requires both error codes to be clear and IS_SYMLINK to hold before the canonical watch is added.",
    "K11": "The second watch is added on CANONICAL.c_str() with IN_CLOSE_WRITE as the only mask argument.",
    "K12": "For a matched watch, the event handler calls m_watchCallback with a newly built SConfigWatchEvent on this line.",
    "K13": "This line registers the FD descriptor with the Wayland event loop as a readable source that calls configWatcherWrite.",
    "K14": "On this line the event-loop callback forwards the readable event by calling onInotifyEvent on the watcher from Config::watcher().",
    "K15": "The guard enters its branch only when the m_propsTripped bit mask contains REFRESH_CONFIG_WATCHER.",
    "K16": "The guarded statement calls update on the object returned by Config::watcher(), refreshing the watch list.",
    "K17": "The init function registers a change callback with setOnChange on the config watcher, taking an SConfigWatchEvent argument.",
    "K18": "The debug line logs the text CConfigManager: file modified, reloading and passes the event file as its argument.",
    "K19": "This line schedules a refresh with the flag REFRESH_ALL on the Supplementary refresher.",
    "K20": "resetHLConfig empties the m_configPaths list on this line, discarding the previous list.",
    "K21": "handleSource appends value to m_configPaths with emplace_back on this line, so the list grows by one entry per call.",
    "K22": "This condition tests file_status with std::filesystem::is_regular_file, the regular-file branch of handleSource.",
    "K23": "The warning logged on this line says the source= match value is skipped because it is a directory.",
    "K24": "The glob call takes absolutePath of rawpath resolved against m_configCurrentPath and the GLOB_TILDE flag.",
    "K25": "The static ENVHOME pointer takes its value from getenv of the HOME variable on this line.",
    "K26": "currentDir is the currentPath text cut with substr at its last slash found by find_last_of on this line.",
    "K27": "The keyword dispatch guard tests whether COMMAND contains the misc:disable_autoreload text before it runs its body.",
    "K28": "The reload request handler calls reload on the object returned by Config::mgr() on this line.",
    "K29": "The description text says a file opened for writing and then closed produces this event, the write-close case.",
    "K30": "The description says the pathname is not dereferenced when it is a symbolic link.",
}

H_PROP = {
    "H01": "The captured hyprctl getoption record reports misc:disable_autoreload with an int value of zero on this host.",
    "H02": "The captured host source list names the omarchy theme file hyprland.conf as a source line target.",
    "H03": "The captured version record gives the commit field of the running Hyprland build on this host.",
}

# ---- extra rows (ids E01..; counter ignores them). quote = stripped pin line ----
E_ROWS = [
    ("E01", "S388", "Hyprland-MiscFunctions.cpp", 66,
     "The replace call on this line swaps only the leading tilde for the HOME string, so a ~user prefix is not looked up and the user name stays glued to HOME."),
    ("E02", "S383", "Hyprland-ConfigWatcher.cpp", 60,
     "The return value of inotify_add_watch is stored in wd on this line without a check, so a failed add still leaves a watch entry."),
    ("E03", "S383", "Hyprland-ConfigWatcher.cpp", 106,
     "This line copies the file field of the matched watch into the callback event, so the reported path is the stored watch path."),
    ("E04", "S389", "Hyprland-HyprCtl.cpp", 1190,
     "This line passes the keyword COMMAND and VALUE to parseKeyword, the path a runtime hyprctl keyword takes into the parser."),
    ("E05", "S387", "Hyprland-legacy-ConfigManager.cpp", 630,
     "The constructor calls resetHLConfig on this line, so the path list is cleared and refilled at construction as well as on reload."),
    ("E06", "S387", "Hyprland-legacy-ConfigManager.cpp", 1838,
     "Before the nested parse this line sets m_configCurrentPath to the value path of the file, so its relative sources resolve against that file."),
    ("E07", "S387", "Hyprland-legacy-ConfigManager.cpp", 2134,
     "The accessor getConfigPaths returns m_configPaths on this line, the same vector that resetHLConfig clears and handleSource appends to."),
]

# ---- prose template ----
# placeholders: {{K_TABLE}} {{H_TABLE}} {{E_TABLE}} ; everything else is literal.


def die(msg, code=2):
    sys.stderr.write(msg + "\n")
    sys.exit(code)


def load():
    raw = open(TABLES, "rb").read()
    if hashlib.sha256(raw).hexdigest() != TABLES_SHA:
        die("tables sha mismatch")
    T = json.loads(raw)["c1"]
    pin_lines = {}

    def lines_of(name):
        if name not in pin_lines:
            data = open(os.path.join(PINS, name), "rb").read().decode("utf-8")
            pin_lines[name] = data.split("\n")
        return pin_lines[name]

    for name, want in T["pin_sha256"].items():
        got = hashlib.sha256(open(os.path.join(PINS, name), "rb").read()).hexdigest()
        if got != want:
            die(f"pin sha mismatch {name}")
    return T, lines_of


def digit_runs(s):
    return set(NUM.findall(s))


def build():
    T, lines_of = load()
    K = T["k"]
    H = T["h"]
    rows_by_pin = {}
    for r in K:
        rows_by_pin.setdefault(r["pin"], set()).add(r["line"])
    errors = []

    k_lines = []
    for r in K:
        rid, pin, ln, quote, sid = r["id"], r["pin"], r["line"], r["quote"], r["sid"]
        prop = K_PROP.get(rid)
        if prop is None:
            errors.append(f"no prop {rid}")
            continue
        pl = lines_of(pin)
        if quote not in pl[ln - 1]:
            errors.append(f"quote:{rid} not in {pin}:{ln}")
        if any(c in quote for c in "|`\\") or any(c in prop for c in "|`\\"):
            errors.append(f"forbidden char in {rid}")
        if len(prop) < 40 or prop != prop.strip():
            errors.append(f"len/ws {rid}")
        qtok = set(TOK.findall(quote))
        ptok = set(TOK.findall(prop))
        if not (ptok & qtok):
            errors.append(f"tok:{rid}")
        allowed = digit_runs(quote) | {str(ln)} | {str(x) for x in rows_by_pin[pin]} | {"0", "1", "2", "3"}
        bad = digit_runs(prop) - allowed
        if bad:
            errors.append(f"num:{rid} {sorted(bad)}")
        k_lines.append((rid, sid, f"{pin}:{ln}", quote, prop))

    h_lines = []
    for r in H:
        rid, pin, ln, quote = r["id"], r["pin"], r["line"], r["quote"]
        prop = H_PROP[rid]
        pl = lines_of(pin)
        if quote not in pl[ln - 1]:
            errors.append(f"quote:{rid}")
        if len(prop) < 20:
            errors.append(f"len {rid}")
        if not (set(TOK.findall(prop)) & set(TOK.findall(quote))):
            errors.append(f"tok:{rid}")
        allowed = digit_runs(quote) | {str(ln)} | {"0", "1", "2", "3"}
        if digit_runs(prop) - allowed:
            errors.append(f"num:{rid}")
        h_lines.append((rid, "host", f"{pin}:{ln}", quote, prop))

    props = [p for *_, p in k_lines] + [p for *_, p in h_lines]
    if len(set(props)) != len(props):
        errors.append("duplicate proposition")

    e_lines = []
    for rid, sid, pin, ln, prop in E_ROWS:
        raw = lines_of(pin)[ln - 1]
        quote = raw.strip()
        if quote not in raw or any(c in quote for c in "|`\\"):
            errors.append(f"E quote {rid}")
        e_lines.append((rid, sid, f"{pin}:{ln}", quote, prop))

    if errors:
        die("SELF-CHECK FAILED: " + "; ".join(errors))

    def table(rows):
        out = ["| id | proposition | src | pin:line | quote |", "|---|---|---|---|---|"]
        for rid, src, loc, quote, prop in rows:
            out.append(f"| {rid} | {prop} | {src} | {loc} | `{quote}` |")
        return "\n".join(out)

    return {
        "K_TABLE": table(k_lines),
        "H_TABLE": table(h_lines),
        "E_TABLE": table(e_lines),
    }, k_lines, h_lines, e_lines


def main():
    out = OUT
    if len(sys.argv) == 3 and sys.argv[1] == "--out":
        out = sys.argv[2]
    tables, k_lines, h_lines, e_lines = build()
    tmpl = open(TEMPLATE, encoding="utf-8").read()
    for key, val in tables.items():
        if "{{" + key + "}}" not in tmpl:
            die(f"template missing {key}")
        tmpl = tmpl.replace("{{" + key + "}}", val)
    if "{{" in tmpl:
        die("unfilled placeholder")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(tmpl)
    print(f"WROTE {out} K={len(k_lines)} H={len(h_lines)} E={len(e_lines)}")


if __name__ == "__main__":
    main()
