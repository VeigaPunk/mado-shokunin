#!/usr/bin/env python3
"""Build c1-r48-fixtures.json: every `expect`, `state` and `cold` measured from the pinned resolver, three runs.

    python3 -I gen-fixtures-v2.py --work /fast/scratch/.../gen

The case list below is authored by hand (each case names what it attacks); nothing is scored here. The counter's own
prepare()/oracle_side() are imported, so a recorded `expect` is byte-for-byte what clause w will measure. Three
identical runs are required per case (stdout, exit status, derived cache state, cold twin); the file is written only
when all three agree. `--only ID` builds one case and prints it.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import random
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c48", os.path.join(HERE, "c1-r48-terminal-cache.py"))
c48 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c48)

MT = c48.PINNED_MTIME
APP = "usr/share/applications/"
LIST = "home/.config/hyprland-xdg-terminals.list"
ENV = {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
       "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
       "XDG_CURRENT_DESKTOP": "Hyprland"}


def entry(cmd, extra=""):
    return "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=%s\n%s" % (cmd, extra)


def mk(cid, cls, note, files, execs, args, state, mtime=MT, prime=True, after=None, cache=None,
       env=None, unset=None, default_cache=False):
    c = {"id": cid, "class": cls, "env": dict(env or ENV), "files": dict(files), "exec": list(execs),
         "args": list(args)}
    if mtime is not None:
        c["mtime"] = mtime
    if prime:
        c["prime"] = {"args": ["--print-cmd"]}
    if after:
        c["after"] = after
    if cache is not None:
        c["cache"] = cache
    if unset:
        c["unset"] = list(unset)
    if default_cache:
        c["default_cache"] = True
    c["_note"] = note
    c["_state"] = state
    return c


BASE_FILES = {APP + "foot.desktop": entry("foot"), LIST: "foot.desktop\n"}
BASE_EXEC = ["bin/foot"]

CASES = [
    # ---- warm hit, answer unchanged (control) ----
    mk("W-01", "WARM-SAME", "primed cache, no mutation: the warm run answers exactly the cold one",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "hit"),
    mk("W-02", "WARM-SAME", "same, but XDG_CACHE_HOME unset: the cache lives at $HOME/.cache (default_cache alias)",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "hit", default_cache=True),
    mk("W-09", "WARM-SAME", "a /disable_cache line added to the list after priming (same byte count): the resolver "
       "reads the cache BEFORE any list, so the directive is never seen and the warm hit stands",
       {APP + "foot.desktop": entry("foot"), LIST: "#_____________\nfoot.desktop\n"}, BASE_EXEC, ["--print-cmd"],
       "hit", after={"files": {LIST: "/disable_cache\nfoot.desktop\n"}, "mtime": MT}),
    mk("W-12", "WARM-SAME", "action entry (id:new) primed, warm and cold both answer the same id/action",
       {APP + "foot.desktop": entry("foot", "Actions=new;\n[Desktop Action new]\nExec=foot --new\n"),
        LIST: "foot.desktop:new\n"}, BASE_EXEC, ["--print-id", "--print-path", "--print-cmd"], "hit"),
    # ---- warm hit, answer DIFFERS from the cold one ----
    mk("W-03", "WARM-DIFFERS", "Exec=foot edited to Exec=foou (same size, same mtime minute): cold rejects the "
       "entry, the warm hit still prints the cached command",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "hit",
       after={"files": {APP + "foot.desktop": entry("foou")}, "mtime": MT}),
    mk("W-04", "WARM-DIFFERS", "TryExec stub removed after priming while exec[0] still resolves: the warm hit never "
       "re-reads TryExec, cold rejects",
       {APP + "foot.desktop": entry("foot", "TryExec=wezterm\n"), LIST: "foot.desktop\n"},
       ["bin/foot", "bin/wezterm"], ["--print-cmd"], "hit",
       after={"exec_remove": ["bin/wezterm"], "mtime": MT}),
    mk("W-05", "WARM-DIFFERS", "Categories=TerminalEmulator; changed to Categories=TerminalEmulatoq; (same size)",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "hit",
       after={"files": {APP + "foot.desktop": entry("foot").replace("TerminalEmulator", "TerminalEmulatoq")},
              "mtime": MT}),
    mk("W-06", "WARM-DIFFERS", "TerminalArgDir name changed after priming; --dir given on the warm run is applied "
       "over the CACHED arg name",
       {APP + "foot.desktop": entry("foot", "X-TerminalArgDir=--working-directory=\n"), LIST: "foot.desktop\n"},
       BASE_EXEC, ["--print-cmd", "--dir=/srv"], "hit",
       after={"files": {APP + "foot.desktop": entry("foot", "X-TerminalArgDir=--working-directorx=\n")}, "mtime": MT}),
    mk("W-07", "WARM-DIFFERS", "TerminalArgTitle name changed after priming; --title given on the warm run is "
       "applied over the cached arg name",
       {APP + "foot.desktop": entry("foot", "X-TerminalArgTitle=--title\n"), LIST: "foot.desktop\n"},
       BASE_EXEC, ["--print-cmd", "--title=t x"], "hit",
       after={"files": {APP + "foot.desktop": entry("foot", "X-TerminalArgTitle=--titlx\n")}, "mtime": MT}),
    mk("W-08", "WARM-DIFFERS", "Exec=foot --a edited to Exec=foot --b (same size): cold prints --b, warm --a",
       {APP + "foot.desktop": entry("foot --a"), LIST: "foot.desktop\n"}, BASE_EXEC, ["--print-cmd"], "hit",
       after={"files": {APP + "foot.desktop": entry("foot --b")}, "mtime": MT}),
    mk("W-10", "WARM-DIFFERS", "list reordered foot/kitty (same bytes): cold selects kitty, the warm hit prints foot",
       {APP + "foot.desktop": entry("foot"), APP + "kitty.desktop": entry("kitty"),
        LIST: "foot.desktop\nkitty.desktop\n"}, ["bin/foot", "bin/kitty"], ["--print-cmd"], "hit",
       after={"files": {LIST: "kitty.desktop\nfoot.desktop\n"}, "mtime": MT}),
    mk("W-11", "WARM-DIFFERS", "Exec=foot -> Exec=foou and a bin/foou stub added: cold selects foou, warm still foot",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "hit",
       after={"files": {APP + "foot.desktop": entry("foou")}, "exec_add": ["bin/foou"], "mtime": MT}),
    mk("W-14", "WARM-DIFFERS", "default cache location ($HOME/.cache) + same-size Exec edit",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "hit", default_cache=True,
       after={"files": {APP + "foot.desktop": entry("foou")}, "mtime": MT}),
    # ---- invalidated / malformed cache ----
    mk("M-01", "MALFORMED-MTIME", "entry mtime moved a day after priming (the ls date moves; a time in the old form shows no minute)",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "stale", after={"mtime": MT + 86400}),
    mk("M-02", "MALFORMED-SIZE", "entry grows a line after priming: size moves, cold path answers",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "stale",
       after={"files": {APP + "foot.desktop": entry("foot") + "GenericName=Q\n"}, "mtime": MT}),
    mk("M-03", "MALFORMED-NAME", "entry renamed after priming: listing moves, cold path answers (no terminal left)",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "stale",
       after={"files": {APP + "foot.desktop": None, APP + "foot2.desktop": entry("foot")}, "mtime": MT}),
    mk("M-04", "MALFORMED-DIRADD", "an unlisted entry appears after priming: listing moves, answer stands",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "stale",
       after={"files": {APP + "extra.desktop": entry("wezterm")}, "mtime": MT}),
    mk("M-12", "MALFORMED-DIRGONE", "the first applications dir disappears after priming: listing moves",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "stale",
       after={"files": {APP + "foot.desktop": None, APP: None}, "mtime": MT}),
    mk("M-05", "MALFORMED-DESK", "XDG_CURRENT_DESKTOP changed after priming: the hash moves, answer stands",
       {APP + "foot.desktop": entry("foot"), LIST: "foot.desktop\n",
        "home/.config/xdg-terminals.list": "foot.desktop\n"}, BASE_EXEC, ["--print-cmd"], "stale",
       after={"env": {"XDG_CURRENT_DESKTOP": "GNOME"}, "mtime": MT}),
    mk("M-06", "MALFORMED-EXECGONE", "exec[0] stub removed after priming: the listing is unchanged but "
       "`command -v foot` fails, so the cache is out of date and the cold path finds no terminal",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "stale", after={"exec_remove": ["bin/foot"], "mtime": MT}),
    mk("M-07", "MALFORMED-TERM", "cache without the END_OF_EXEC_USEP terminator (11 junk lines)",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "invalid",
       prime=False, cache="\n".join(["0" * 32, "foot"] + ["x"] * 9) + "\n"),
    mk("M-08", "MALFORMED-EARLY", "terminator on line 3: the parser is still in its header, so the cache is invalid",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "invalid",
       prime=False, cache="0" * 32 + "\nfoot\nx\x1eEND_OF_EXEC_USEP\n"),
    mk("M-09", "MALFORMED-LIMIT", "sixty lines and no terminator: the line limit rejects the cache",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "invalid",
       prime=False, cache="\n".join(["0" * 32, "foot"] + ["x"] * 58) + "\n"),
    mk("M-10", "MALFORMED-EMPTY", "an empty cache file: nothing parsed, nothing to trust",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "invalid", prime=False, cache=""),
    mk("M-11", "MALFORMED-BADHASH", "well-formed eleven-line cache with a hash that cannot match: out of date",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "stale", prime=False,
       cache="\n".join(["0" * 32, "foot", "/x/foot.desktop", "foot.desktop", ""] + ["-e", "", "", "", "", "foot"])
       + "\x1eEND_OF_EXEC_USEP\n"),
    mk("M-16", "MALFORMED-LINE49", "terminator on line 49: parses (the limit is line 50), hash out of date",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "stale", prime=False,
       cache="\n".join(["0" * 32, "foot"] + ["x"] * 46) + "\nx\x1eEND_OF_EXEC_USEP\n"),
    mk("M-17", "MALFORMED-LINE50", "terminator on line 50: the limit is reached before the terminator is read",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "invalid", prime=False,
       cache="\n".join(["0" * 32, "foot"] + ["x"] * 47) + "\nx\x1eEND_OF_EXEC_USEP\n"),
    mk("M-18", "MALFORMED-NONL", "terminator on the last line but with no trailing newline: `while read` never runs "
       "its body for that line, so the cache is invalid",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "invalid", prime=False,
       cache="\n".join(["0" * 32, "foot", "/x/foot.desktop", "foot.desktop", ""] + ["-e", "", "", "", "", "foot"])
       + "\x1eEND_OF_EXEC_USEP"),
    mk("M-13", "MALFORMED-DISABLED", "XTE_CACHE_ENABLED=false after priming: the cache is never consulted",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "disabled",
       after={"env": {"XTE_CACHE_ENABLED": "false"}, "mtime": MT}),
    mk("M-14", "MALFORMED-DISABLED-GARBAGE", "XTE_CACHE_ENABLED=garbage: check_bool says no, the cache is never consulted",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "disabled", prime=False,
       cache="0" * 32 + "\nfoot\n" + "x\n" * 9 + "foot\x1eEND_OF_EXEC_USEP\n",
       env=dict(ENV, XTE_CACHE_ENABLED="garbage")),
    # ---- edge: HOME unset (round-47 D1 / w2/ExecC1Diff H3) ----
    mk("E-01", "EDGE-HOMEUNSET", "HOME and every XDG base unset: the resolver dies under set -u before the cache "
       "gate (exit 1, empty stdout) - the tool must not answer 2",
       BASE_FILES, BASE_EXEC, ["--print-cmd"], "absent", prime=False,
       unset=["HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME"]),
    mk("E-02", "WARM-ABSENT", "nothing selectable: the cold prime saves no cache, so the scored run is a plain "
       "cold run with cache=absent",
       {APP + "foot.desktop": entry("missingbin"), LIST: "foot.desktop\n"}, [], ["--print-cmd"], "absent"),
]


def measure(box, case, seed):
    rng = random.Random(seed)
    base, lang = c48.variant_roots(box, "A", rng)
    try:
        ro = os.path.join(base, "o", "r")
        c48.prepare(box, ro, case, lang)
        warm, state = c48.oracle_side(box, case, ro, lang)
        cold = None
        if case.get("prime") or "cache" in case:
            rcold = os.path.join(base, "c", "r")
            c48.prepare(box, rcold, case, lang, cold=True)
            cold, _st = c48.oracle_side(box, case, rcold, lang)
        return warm, state, cold
    finally:
        shutil.rmtree(base.split("/deep/")[0] if "/deep/" in base else base, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", default=os.path.join(HERE, "c1-r48-fixtures.json"))
    ap.add_argument("--only", default=None)
    ap.add_argument("--runs", type=int, default=3)
    a = ap.parse_args()
    work = tempfile.mkdtemp(dir=a.work, prefix="gen-")
    box = c48.Box(work)
    out, bad = [], []
    for case in CASES:
        if a.only and case["id"] != a.only:
            continue
        note, want_state = case.pop("_note"), case.pop("_state")
        try:
            results = [measure(box, case, 1000 + k) for k in range(a.runs)]
        except c48.Setup as e:
            bad.append((case["id"], "SETUP %s" % e))
            continue
        warm, state, cold = results[0]
        if any(r != results[0] for r in results[1:]):
            bad.append((case["id"], "NON-DETERMINISTIC %r" % (results,)))
            continue
        case["expect"] = {"rc": warm[0], "stdout": warm[1]}
        case["state"] = state
        if cold is not None:
            case["cold"] = {"rc": cold[0], "stdout": cold[1]}
        try:
            c48.check_case(case, out_file_name())
            c48.check_premise(case, state, cold)
        except c48.Setup as e:
            bad.append((case["id"], "PREMISE %s" % e))
        if state != want_state:
            bad.append((case["id"], "STATE %s != authored %s" % (state, want_state)))
        out.append(case)
        print("%-6s %-24s state=%-8s rc=%d out=%-28r cold=%r  # %s" % (
            case["id"], case["class"], state, warm[0], warm[1][:26],
            None if cold is None else (cold[0], cold[1][:16]), note))
    if a.only:
        print(json.dumps(out, indent=1, sort_keys=True))
    else:
        blob = (json.dumps(out, indent=1, sort_keys=True) + "\n").encode()
        with open(a.out, "wb") as fh:
            fh.write(blob)
        print("\nwrote %s (%d cases, %d bytes)\nsha256 %s" % (a.out, len(out), len(blob),
                                                             hashlib.sha256(blob).hexdigest()))
    if bad:
        print("\nPROBLEMS:")
        for cid, why in bad:
            print("  %s: %s" % (cid, why))
    return 1 if bad else 0


def out_file_name():
    return "c1-r48-fixtures.json"


if __name__ == "__main__":
    sys.exit(main())
