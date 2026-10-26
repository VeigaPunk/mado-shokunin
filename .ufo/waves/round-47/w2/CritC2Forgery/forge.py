#!/usr/bin/env python3
"""CritC2Forgery driver: forge entries admitted by PRED-C2-r47 that a reader should refuse.

Builds each forgery as its own scratch clone at BASE, commits the forged tree, runs the
frozen counter, and records its verdict. POS (the official positive control) is rebuilt
first to validate the harness.
"""
import hashlib
import os
import re
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r47/CritC2Forgery"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "60edb66e2f1cb90acc6e9442fc93ded0ca42d750"
P = os.path.join(S, "pins")
COUNTER = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r47-terminal-entry.py"
SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w2/CritC2Forgery"
FETCH = ".ufo/waves/round-47/fetch/"
RECEIPTS = ".ufo/waves/round-47/receipts/"
ENTRY = "corpus/knowledge/xdg-terminal-selection-r47.md"

PINS = {
    "xdgte-xdg-terminal-exec": "xdg-terminal-exec",
    "xdgte-README.md": "README.md",
    "xdgte-xdg-terminals.list": "xdg-terminals.list",
    "xdgte-xdg-terminal-exec.1.scd": "xdg-terminal-exec.1.scd",
    "xdgte-test_tests.bats": "test/tests.bats",
}
URL = "https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/"
COMMIT = "065925df9f419008159258ae169018bfd23df71b"
S_SHA = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"


def run(*args, cwd=None, check=True, env=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, env=env)
    if check and p.returncode != 0:
        sys.exit("FAILED %s: %s" % (" ".join(args), p.stderr.decode()[:2000]))
    return p


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def lines_of(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read().split("\n")


def collapse_lines(text):
    out, lines, prev = [], [], True
    for ln, line in enumerate(text.split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    out.append(" ")
                    lines.append(ln)
                    prev = True
            else:
                out.append(ch)
                lines.append(ln)
                prev = False
    return "".join(out), lines


def locate(pin, anchor):
    with open(os.path.join(P, pin), encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    flat, lines = collapse_lines(text)
    q = re.sub(r"\s+", " ", anchor).strip()
    at = flat.find(q)
    if at < 0 or flat.find(q, at + 1) >= 0:
        sys.exit("anchor %r in %s: %s" % (anchor[:60], pin,
                                          "absent" if at < 0 else "not unique"))
    return lines[at]


def pins_block():
    out = {}
    for name, rel in PINS.items():
        path = os.path.join(P, rel)
        out[name] = (sha(path), os.path.getsize(path), len(lines_of(path)) - 1)
    return out


def new_clone(name):
    D = os.path.join(S, "f", name)
    run("rm", "-rf", D)
    run("git", "clone", "-q", "--shared", LANE, D)
    run("git", "-C", D, "checkout", "-q", BASE)
    top = run("git", "-C", D, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(D):
        sys.exit("clone toplevel %s != %s" % (top, D))
    run("git", "-C", D, "config", "user.email", "crit@c2r47.invalid")
    run("git", "-C", D, "config", "user.name", "CritC2Forgery")
    return D


def load_pins(D):
    for name, rel in PINS.items():
        with open(os.path.join(P, rel), "rb") as src, \
                open(os.path.join(D, FETCH, name), "wb") as dst:
            dst.write(src.read())


def row(sid, source, kind, tier, scope, anchor, teaches):
    return ("| %s | %s | %s | %s | %s | %s | %s | mined | 2026-10-26 | on-release | %s |"
            % (sid, source, kind, tier, scope, anchor, teaches, ENTRY))


QUOTES = {
    "q147": "Populate list of config files to read, in descending order of preference",
    "q353": "All config files are read immediatelly, rather than on demand",
    "q364": "Nonexistant file is not an error",
    "q565": "Fills global XTE__EXEC_USEP var with $XTE__USEP-separated command array in place to avoid $() expansion newline issues",
    "q805": "XTE__EXEC_USEP : Program to execute, possibly with arguments, delimited by ASCII Unit Separator.",
    "q112": "print selected Desktop Entry ID. Action is appended delimited",
    "b57": "Optionally an entry ID can be suffixed with",
    "b63": "Entry eligible for selection should have `TerminalEmulator` Category and",
    "b133": "Empty lines and lines starting with `#` are ignored, dangling whitespaces are",
}
LOC = {
    "q147": "147-166", "q353": "350-360", "q364": "362-366", "q565": "563-567",
    "q805": "805-806", "q112": "110-114", "b57": "55-59", "b63": "63-65",
    "b133": "133-135",
}


def q(k):
    return QUOTES[k]


def build_entry(pb, m):
    s = "xdgte-xdg-terminal-exec"
    r = "xdgte-README.md"
    # validate quotes unique + ranges hold
    rel2name = {v: k for k, v in PINS.items()}
    for k, qq in QUOTES.items():
        rel = PINS[s] if k.startswith("q") else PINS[r]
        ln = locate(rel, qq)
        a, b = (int(x) for x in LOC[k].split("-"))
        if not (a <= ln <= b):
            sys.exit("range %s misses quote %s at %d" % (LOC[k], k, ln))
        if int(b) > pb[rel2name[rel]][2]:
            sys.exit("range beyond pin %s" % rel)

    if m.get("f9"):
        src326 = "source: S326 - xdg-terminal-exec 0.14.3 man page at tag - the print options and their delimiters"
        src327 = "source: S327 - xdg-terminal-exec 0.14.3 test suite at tag - the fixture lists that pin the validation edge classes"
        src328 = "source: S328 - xdg-terminal-exec 0.14.3 script at tag - the executed selection chain"
        src329 = "source: S329 - xdg-terminal-exec 0.14.3 stock xdg-terminals.list at tag - the lowest-priority system list and its exec-argument defaults"
        src330 = "source: S330 - xdg-terminal-exec 0.14.3 README at tag - the documented list-file format and eligibility keys this entry executes"
    else:
        src326 = "source: S326 - xdg-terminal-exec 0.14.3 script at tag - ordered list files, list-line directives, entry-ID lookup, validation keys, exec-argument composition, print modes"
        src327 = "source: S327 - xdg-terminal-exec 0.14.3 README at tag - the documented list-file format and eligibility keys this entry executes"
        src328 = "source: S328 - xdg-terminal-exec 0.14.3 stock xdg-terminals.list at tag - the lowest-priority system list and its exec-argument defaults"
        src329 = "source: S329 - xdg-terminal-exec 0.14.3 man page at tag - the print options and their delimiters"
        src330 = "source: S330 - xdg-terminal-exec 0.14.3 test suite at tag - the fixture lists that pin the validation edge classes"

    if m.get("f6"):
        ground = ("ground: terminal-selection plane, the resolver's executed choice and print composition; the chain was "
                  "absent at base (claim grep exit 1); held neighbours: the documentary route in terminal-route-r17.md "
                  "and terminals-and-omarchy.md")
    else:
        ground = ("ground: terminal-selection plane, the resolver's executed choice and print composition; the chain was "
                  "absent at base (claim grep exit 1); held neighbours: the documentary route in terminal-route-r17.md "
                  "and terminals-and-omarchy.md")

    if m.get("f1"):
        st1 = ("1. Lists and their order: the resolver builds one ordered list of config files, desktop-prefixed name "
                "first inside each directory, config dirs before the config home, then the data-dir list last; the "
                "result is read left to right as *ascending* preference, so the system entries come first and the user "
                "override can never win (\"{q147}\", {l147}).")
        st5 = ("5. Validation: `check_entry_key` reads Type, Categories, Hidden and the show-in rules decide acceptance, "
                "and TryExec or the Exec program must be executable on PATH ({l5}); the exec-argument keys are read in "
                "the same pass (\"{q805}\", {l805}); among several valid entries the FIRST found wins, so a system copy "
                "of an ID shadows a later user override.")
    else:
        st1 = ("1. Lists and their order: the resolver builds one ordered list of config files, desktop-prefixed name "
                "first inside each directory, config home then config dirs then the xdg-terminal-exec subdirs of the "
                "data dirs (\"{q147}\", {l147}).")
        st5 = ("5. Validation: `check_entry_key` reads Type, Categories, Hidden and the show-in rules decide acceptance, "
                "and TryExec or the Exec program must be executable on PATH ({l5}); the exec-argument keys are read in "
                "the same pass (\"{q805}\", {l805}).")

    if m.get("f2"):
        # quotes from comments only: each behavioral claim is anchored to the comment line alone
        loc = {}
        for kk in QUOTES:
            where = PINS[s] if kk.startswith("q") else PINS[r]
            ln = locate(where, QUOTES[kk])
            loc[kk] = "%s:%d-%d" % (s if kk.startswith("q") else r, ln, ln)
    else:
        loc = dict(q147="%s:%s" % (s, LOC["q147"]), q353="%s:%s" % (s, LOC["q353"]),
                   q364="%s:%s" % (s, LOC["q364"]), q565="%s:%s" % (s, LOC["q565"]),
                   q805="%s:%s" % (s, LOC["q805"]), q112="%s:%s" % (s, LOC["q112"]),
                   b57="%s:%s" % (r, LOC["b57"]), b63="%s:%s" % (r, LOC["b63"]),
                   b133="%s:%s" % (r, LOC["b133"]))
    st1 = st1.format(q147=q("q147"), l147=loc["q147"])
    st5 = st5.format(l5="%s:885-960" % s, q805=q("q805"), l805=loc["q805"])

    if m.get("f3"):
        live = ("The round-17 [UNK] (corpus/knowledge/terminal-route-r17.md:144-145) asked whether the resolver "
                "actually picks that entry over the system one at launch. A cold-cache print run answers the "
                "selection half: `.ufo/waves/round-47/receipts/live-host.txt` records the observed print output "
                "(`.ufo/waves/round-47/receipts/live-observed.txt`) and the verdict "
                "`MADO_TERM: selected=WezTerm.desktop path=/home/vgpnk/.local/share/applications/WezTerm.desktop "
                "verdict=OK`, so the user override wins over the system entry.")
    elif m.get("f8"):
        live = ("The round-17 [UNK] (corpus/knowledge/terminal-route-r17.md:144-145) asked whether the resolver "
                "actually picks that entry over the system one at launch. The cold-cache print run answers it at "
                "launch: `.ufo/waves/round-47/receipts/live-host.txt` records the observed print output "
                "(`.ufo/waves/round-47/receipts/live-observed.txt`) and the verdict "
                "`MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop "
                "verdict=OK`, so at launch the user override wins over the system entry.")
    else:
        live = ("The round-17 [UNK] (corpus/knowledge/terminal-route-r17.md:144-145) asked whether the resolver "
                "actually picks that entry over the system one at launch. A cold-cache print run answers the "
                "selection half: `.ufo/waves/round-47/receipts/live-host.txt` records the observed print output "
                "(`.ufo/waves/round-47/receipts/live-observed.txt`) and the verdict "
                "`MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop "
                "verdict=OK`, so the user override wins over the system entry.")

    body = """# Which terminal SUPER+RETURN launches: the xdg-terminal-exec 0.14.3 selection chain, executed read-only

{src326}
{src327}
{src328}
{src329}
{src330}
verified-at: 2026-10-26
recheck: on-release - when xdg-terminal-exec leaves v0.14.3 re-pull the five pins and re-run quality/counters/c2-r47-terminal-entry.py (or 90d at the latest)
{ground}
Lane: mado-shokunin. Round: 47.

## The executed chain

{st1}
2. List lines: `read_config_paths` reads every existing list file up front into one ordered ID list, comments and blanks dropped, directives taken before IDs ("{q353}", {l353}); a missing file is skipped, not an error ("{q364}", {l364}).
3. Entry IDs and actions: `find_entry_paths` and the ID validators turn a line into a candidate entry ID optionally suffixed with an action, and only IDs that pass the ID and action validators enter the list ("{qb57}", {lb57}); the lookup side of the same step is {l3}.
4. Desktop-file lookup: IDs resolve across the applications dirs of the data hierarchy, first hit wins, and an entry is eligible only with the TerminalEmulator category and the X-TerminalArgExec key ("{qb63}", {lb63}); the scan order is {l4}.
{st5}
6. Exec-argument composition: the Exec field is tokenized into an argument vector, field codes dropped, and the terminal's own exec argument placed before the command ("{q565}", {l565}); option arguments are appended per key ({l6}).
7. Print modes: the print options select what is written instead of a launch, and the `--print-delimiter` sequences join them ("{q112}", {l112}); the cache is written by the print pass, so a cold-cache read is the pure selection ({l7}).

## Cache

The cache file holds the listing hash, the entry ID, its path, the exec argument vector and the option arguments; a print run with a matching hash reuses it, and the hash covers the config and applications listings ({l8}). The live reading below used an empty cache home, so it models a cold cache.

## This host (live, read-only)

{live}
""".format(
        src326=src326, src327=src327, src328=src328, src329=src329, src330=src330,
        ground=ground, st1=st1, st5=st5, live=live,
        q147=q("q147"), l147=loc["q147"],
        q353=q("q353"), l353=loc["q353"],
        q364=q("q364"), l364=loc["q364"],
        qb57=q("b57"), lb57=loc["b57"], l3="%s:420-445" % s,
        qb63=q("b63"), lb63=loc["b63"], l4="%s:760-790" % s,
        l5="%s:885-960" % s, q805=q("q805"), l805=loc["q805"],
        q565=q("q565"), l565=loc["q565"], l6="%s:695-740" % s,
        q112=q("q112"), l112=loc["q112"], l7="%s:1272-1310" % s,
        l8="%s:217-300" % s)
    for mm in re.finditer(r"xdgte-xdg-terminal-exec:(\d+)-(\d+)", body):
        if int(mm.group(2)) > pb[s][2]:
            sys.exit("script range beyond pin: %s" % mm.group(0))
    return body


def build_rows(pb, m):
    s = "xdgte-xdg-terminal-exec"
    r = "xdgte-README.md"
    li = "xdgte-xdg-terminals.list"
    man = "xdgte-xdg-terminal-exec.1.scd"
    t = "xdgte-test_tests.bats"
    if m.get("f6"):
        scope326 = ("upstream script's executed selection and lookup code at tag v0.14.3, restated from held row S057 "
                    "under the executed-selection names")
        teaches326 = ("the executed chain mirrors the documentary route held at S057, renamed to the new census terms")
        scope327 = ("upstream default-terminal selection contract at tag v0.14.3, restated from held row S056")
        teaches327 = ("the documented contract is held at S056; this row re-presents it under the new term set")
        scope328 = ("lowest-priority system selection list in the upstream chain, restated from held row S060")
        teaches328 = ("the system list holds no Alacritty row, as already held at S060")
        scope329 = ("the print options, their delimiters and the option-to-key mapping, as observed on this host")
        teaches329 = ("print modes write the selected ID, path or command instead of launching, observed on this host")
        scope330 = ("the fixture lists and desktop entries that pin the validation edge classes at the tag, matching "
                    "this host's observed selection")
        teaches330 = ("the tag's own tests fix which rejection classes exist, matching this host's observed selection")
    elif m.get("f5"):
        scope326 = ("the resolver's executed selection chain measured live on this host: list files and their order, "
                    "list lines and directives, entry-ID and action validation, desktop-file lookup, validation keys, "
                    "exec-argument composition, print modes, cache")
        teaches326 = ("the print modes select the first valid entry from the ordered list files and write only the "
                      "cache, as observed on this host in a cold-cache print run")
        scope327 = ("the documented list-file naming, order, line syntax, eligibility keys and exec-argument keys the "
                    "resolver implements, and the host's observed behavior")
        teaches327 = ("the spec text the resolver executes: entry IDs in ordered list files, TerminalEmulator "
                      "eligibility, X-TerminalArg keys, as observed on this host")
        scope328 = ("the lowest-priority system terminal list shipped at the tag, and the host's observed selection")
        teaches328 = ("the system list holds no Alacritty row, and the host's user override is selected over it on "
                      "this host")
        scope329 = ("the print options, their delimiters and the option-to-key mapping, as observed on this host")
        teaches329 = ("print modes write the selected ID, path or command instead of launching, observed on this host")
        scope330 = ("the fixture lists and desktop entries that pin the validation edge classes at the tag, matching "
                    "this host's observed selection")
        teaches330 = ("the tag's own tests fix which rejection classes exist, matching this host's observed selection")
    else:
        scope326 = ("the executed selection chain of the resolver: list files and their order, list lines and "
                    "directives, entry-ID and action validation, desktop-file lookup, validation keys, exec-argument "
                    "composition, print modes, cache")
        teaches326 = ("the print modes select the first valid entry from the ordered list files and write only the cache")
        scope327 = ("the documented list-file naming, order, line syntax, eligibility keys and exec-argument keys the "
                    "resolver implements")
        teaches327 = ("the spec text the resolver executes: entry IDs in ordered list files, TerminalEmulator "
                      "eligibility, X-TerminalArg keys")
        scope328 = ("the lowest-priority system terminal list shipped at the tag")
        teaches328 = ("the system list holds no Alacritty row, so the host's user override is not shadowed by a "
                      "system listing")
        scope329 = ("the print options, their delimiters and the option-to-key mapping")
        teaches329 = ("print modes write the selected ID, path or command instead of launching, which is what makes "
                      "a read-only observation possible")
        scope330 = ("the fixture lists and desktop entries that pin the validation edge classes at the tag")
        teaches330 = ("the tag's own tests fix which rejection classes exist, so the chain steps are testable "
                      "against the same bytes")
    rows = [
        row("S326", "xdg-terminal-exec v0.14.3 selection script at tag - " + URL + "xdg-terminal-exec",
            "code", "A", scope326,
            "%s:147-166 make_paths list order, %s:352-445 list parsing and entry IDs, %s:760-960 entry lookup and validation, %s:1272-1330 print modes (receipt %s) @ tag v0.14.3 commit %s, %d B sha256:%s; receipt %s%s"
            % (s, s, s, s, s, COMMIT, pb[s][1], pb[s][0], FETCH, s),
            teaches326),
        row("S327", "xdg-terminal-exec v0.14.3 README at tag - " + URL + "README.md",
            "docs", "A", scope327,
            "%s:55-59 action suffix, %s:63-68 eligibility keys, %s:100-135 list files and their order (receipt %s) @ tag v0.14.3, %d B sha256:%s; receipt %s%s"
            % (r, r, r, r, pb[r][1], pb[r][0], FETCH, r),
            teaches327),
        row("S328", "xdg-terminal-exec v0.14.3 stock list at tag - " + URL + "xdg-terminals.list",
            "code", "A", scope328,
            "%s:1-25 whole file, %d B (receipt %s) @ tag v0.14.3, sha256:%s; receipt %s%s"
            % (li, pb[li][1], li, pb[li][0], FETCH, li),
            teaches328),
        row("S329", "xdg-terminal-exec v0.14.3 man page at tag - " + URL + "xdg-terminal-exec.1.scd",
            "docs", "A", scope329,
            "%s:42-50 print options, %s:60-90 argument keys (receipt %s) @ tag v0.14.3, %d B sha256:%s; receipt %s%s"
            % (man, man, man, pb[man][1], pb[man][0], FETCH, man),
            teaches329),
        row("S330", "xdg-terminal-exec v0.14.3 test suite at tag - " + URL + "test/tests.bats",
            "code", "A", scope330,
            "%s:1-64 list precedence cases, %s:64-140 hidden and show-in cases (receipt %s) @ tag v0.14.3, %d B sha256:%s; receipt %s%s"
            % (t, t, t, pb[t][1], pb[t][0], FETCH, t),
            teaches330),
    ]
    return "\n".join(rows)


def build_readme_row(m):
    if m.get("f4"):
        return ("| `knowledge/xdg-terminal-selection-r47.md` (MADO-R47-1, round 47; terminal-selection plane) | "
                "The launch decision of xdg-terminal-exec 0.14.3 on this host: at launch the user override wins, "
                "observed in a live cold-cache run. | [Source and recheck](knowledge/xdg-terminal-selection-r47.md): "
                "§3 live verdict; Sources S326-S330. |")
    return ("| `knowledge/xdg-terminal-selection-r47.md` (MADO-R47-1, round 47; terminal-selection plane) | "
            "The executed selection chain of xdg-terminal-exec 0.14.3 on rows S326-S330: ordered desktop-prefixed "
            "list files, list-line directives, entry-ID and action validation, desktop-file lookup across the data "
            "hierarchy, eligibility keys (TerminalEmulator, X-TerminalArgExec, Hidden, show-in rules, TryExec on PATH), "
            "exec-argument composition and the print modes, plus a live cold-cache reading that the user override "
            "wins over the system entry. | [Source and recheck](knowledge/xdg-terminal-selection-r47.md): §§1 chain "
            "steps 1-7, §2 cache, §3 live verdict; Sources S326-S330. |")


def write_receipts(D, m):
    if m.get("f3"):
        obs = ("WezTerm.desktop\n"
               "/home/vgpnk/.local/share/applications/WezTerm.desktop\n"
               "wezterm\n")
        rec = ("# live read-only print run, 2026-10-26 (no terminal launched; XDG_CACHE_HOME in scratch)\n"
               "$ XDG_CACHE_HOME=/fast/scratch/hyaku/mado-r47/ExecLive/cache xdg-terminal-exec --print-id --print-path --print-cmd\n"
               "rc=0\n"
               "XDG_CURRENT_DESKTOP=Hyprland\n"
               "XDG_CONFIG_HOME=/home/vgpnk/.config\n"
               "XDG_CONFIG_DIRS=/etc/xdg\n"
               "XDG_DATA_HOME=/home/vgpnk/.local/share\n"
               "XDG_DATA_DIRS=/usr/local/share:/usr/share\n"
               "PATH=/usr/local/bin:/usr/bin:/bin\n"
               "resolver_sha256=89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac\n"
               "observed=.ufo/waves/round-47/receipts/live-observed.txt\n"
               "Alacritty.desktop\n"
               "/home/vgpnk/.local/share/applications/Alacritty.desktop\n"
               "alacritty\n"
               "MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop verdict=OK\n")
    else:
        obs = ("Alacritty.desktop\n"
               "/home/vgpnk/.local/share/applications/Alacritty.desktop\n"
               "alacritty\n")
        rec = ("# live read-only print run, 2026-10-26 (no terminal launched; XDG_CACHE_HOME in scratch)\n"
               "$ XDG_CACHE_HOME=/fast/scratch/hyaku/mado-r47/ExecLive/cache xdg-terminal-exec --print-id --print-path --print-cmd\n"
               "rc=0\n"
               "XDG_CURRENT_DESKTOP=Hyprland\n"
               "XDG_CONFIG_HOME=/home/vgpnk/.config\n"
               "XDG_CONFIG_DIRS=/etc/xdg\n"
               "XDG_DATA_HOME=/home/vgpnk/.local/share\n"
               "XDG_DATA_DIRS=/usr/local/share:/usr/share\n"
               "PATH=/usr/local/bin:/usr/bin:/bin\n"
               "resolver_sha256=89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac\n"
               "observed=.ufo/waves/round-47/receipts/live-observed.txt\n"
               "Alacritty.desktop\n"
               "/home/vgpnk/.local/share/applications/Alacritty.desktop\n"
               "alacritty\n"
               "MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop verdict=OK\n")
    with open(os.path.join(D, RECEIPTS, "live-observed.txt"), "w") as fh:
        fh.write(obs)
    with open(os.path.join(D, RECEIPTS, "live-host.txt"), "w") as fh:
        fh.write(rec)


def insert_after(path, predicate, block):
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    out, done = [], False
    for l in lines:
        out.append(l)
        if not done and predicate(l):
            out.extend(block.split("\n"))
            done = True
    if not done:
        sys.exit("insertion point not found in %s" % path)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))


def build_forgery(name, m):
    D = new_clone(name)
    os.makedirs(os.path.join(D, FETCH), exist_ok=True)
    os.makedirs(os.path.join(D, RECEIPTS), exist_ok=True)
    load_pins(D)
    pb = pins_block()
    body = build_entry(pb, m)
    rows = build_rows(pb, m)
    with open(os.path.join(D, ENTRY), "w", encoding="utf-8") as fh:
        fh.write(body)
    insert_after(os.path.join(D, "corpus/SOURCES.md"),
                 lambda l: re.match(r"^ {0,3}\|\s*S325\s*\|", l), rows)
    insert_after(os.path.join(D, "corpus/README.md"),
                 lambda l: l.startswith("| `knowledge/hyprland-input-devices-r46.md`"),
                 build_readme_row(m))
    write_receipts(D, m)
    if m.get("f7a"):
        os.unlink(os.path.join(D, "corpus/knowledge/terminal-route-r17.md"))
    if m.get("f7b"):
        p = os.path.join(D, "corpus/knowledge/terminal-route-r17.md")
        with open(p, encoding="utf-8") as fh:
            rlines = fh.read().split("\n")
        rlines[143:143] = [""] * 6
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("\n".join(rlines))
    run("git", "-C", D, "add", "-A")
    run("git", "-C", D, "commit", "-q", "-m", "forge: %s" % name)
    rev = run("git", "-C", D, "rev-parse", "HEAD").stdout.decode().strip()
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", D, "--rev", "HEAD"],
                       capture_output=True, env=env)
    out = p.stdout.decode("utf-8", "replace")
    if p.stderr:
        out += "\n[stderr]\n" + p.stderr.decode("utf-8", "replace")
    with open(os.path.join(SEAT, "score-%s.txt" % name), "w") as fh:
        fh.write(out + "\nexit=%d rev=%s\n" % (p.returncode, rev))
    return p.returncode, rev, out


def main():
    os.makedirs(os.path.join(SEAT), exist_ok=True)
    forgeries = [
        ("POS", {}),
        ("F1-false-mechanism", {"f1": True}),
        ("F2-comment-quotes", {"f2": True}),
        ("F3-typed-capture", {"f3": True}),
        ("F4-readme-elsewhere", {"f4": True}),
        ("F5-false-scope", {"f5": True}),
        ("F6-reclaim-held-ground", {"f6": True}),
        ("F7a-r17-deleted", {"f7a": True}),
        ("F7b-r17-anchor-shifted", {"f7b": True}),
        ("F8-launch-half-claim", {"f8": True}),
        ("F9-provenance-lie", {"f9": True}),
    ]
    results = []
    for name, m in forgeries:
        rc, rev, out = build_forgery(name, m)
        admitted = "admitted=1" in out
        results.append((name, rc, rev, admitted, out.splitlines()[-2] if out.splitlines() else ""))
        print("RESULT %-28s rc=%d admitted=%s rev=%s" % (name, rc, admitted, rev))
    with open(os.path.join(SEAT, "results.txt"), "w") as fh:
        for name, rc, rev, admitted, last in results:
            fh.write("%-28s rc=%d admitted=%s rev=%s %s\n" % (name, rc, admitted, rev, last))


if __name__ == "__main__":
    main()
