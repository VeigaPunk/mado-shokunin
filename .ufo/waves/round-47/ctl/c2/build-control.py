#!/usr/bin/env python3
"""Build the positive-control revision for PRED-C2-r47 in a scratch clone.

Writes ONLY inside the scratch dir; the lane is read (git clone --shared) and never
written. Every locator in the generated entry and rows is computed by grepping the
pinned bytes (never typed): a quote whose anchor text does not occur exactly once in
its pin aborts the build.
"""
import hashlib
import os
import re
import subprocess
import sys

S = os.environ["C2R47_WORK"]
D = os.path.join(S, "ctl")
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "60edb66e2f1cb90acc6e9442fc93ded0ca42d750"
P = os.path.join(S, "pins/xdg-terminal-exec-0.14.3")
FETCH = ".ufo/waves/round-47/fetch/"
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


def run(*args, cwd=None, check=True):
    p = subprocess.run(args, cwd=cwd, capture_output=True)
    if check and p.returncode != 0:
        sys.exit("FAILED %s: %s" % (" ".join(args), p.stderr.decode()[:2000]))
    return p


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
    """1-based line of the unique occurrence of anchor in the pin bytes (collapsed)."""
    with open(os.path.join(P, pin), encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    flat, lines = collapse_lines(text)
    q = re.sub(r"\s+", " ", anchor).strip()
    at = flat.find(q)
    if at < 0 or flat.find(q, at + 1) >= 0:
        sys.exit("anchor %r in %s: %s" % (anchor[:60], pin,
                                          "absent" if at < 0 else "not unique"))
    return lines[at]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def build_tree():
    run("rm", "-rf", D)
    run("git", "clone", "-q", "--shared", LANE, D)
    run("git", "-C", D, "checkout", "-q", BASE)
    top = run("git", "-C", D, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(D):
        sys.exit("clone toplevel %s != %s" % (top, D))
    run("git", "-C", D, "config", "user.email", "control@c2r47.invalid")
    run("git", "-C", D, "config", "user.name", "C2R47 control")
    os.makedirs(os.path.join(D, FETCH), exist_ok=True)
    os.makedirs(os.path.join(D, ".ufo/waves/round-47/receipts"), exist_ok=True)
    os.makedirs(os.path.join(D, "tools"), exist_ok=True)
    for name, rel in PINS.items():
        with open(os.path.join(P, rel), "rb") as src, \
                open(os.path.join(D, FETCH, name), "wb") as dst:
            dst.write(src.read())


def pins_block():
    """sha/bytes per fetch name, computed from the pinned bytes."""
    out = {}
    for name, rel in PINS.items():
        path = os.path.join(P, rel)
        out[name] = (sha(path), os.path.getsize(path), len(lines_of(path)) - 1)
    return out


def row(sid, source, kind, tier, scope, anchor, teaches):
    return ("| %s | %s | %s | %s | %s | %s | %s | mined | 2026-10-26 | on-release | %s |"
            % (sid, source, kind, tier, scope, anchor, teaches, ENTRY))


def build_entry(pb):
    s = "xdgte-xdg-terminal-exec"
    r = "xdgte-README.md"
    q147 = locate(PINS[s], "Populate list of config files to read, in descending order of preference")
    q353 = locate(PINS[s], "All config files are read immediatelly, rather than on demand")
    q364 = locate(PINS[s], "Nonexistant file is not an error")
    q565 = locate(PINS[s], "Fills global XTE__EXEC_USEP var with $XTE__USEP-separated command array in place to avoid $() expansion newline issues")
    q805 = locate(PINS[s], "XTE__EXEC_USEP : Program to execute, possibly with arguments, delimited by ASCII Unit Separator.")
    q112 = locate(PINS[s], "print selected Desktop Entry ID. Action is appended delimited")
    b57 = locate(PINS[r], "Optionally an entry ID can be suffixed with")
    b63 = locate(PINS[r], "Entry eligible for selection should have `TerminalEmulator` Category and")
    b133 = locate(PINS[r], "Empty lines and lines starting with `#` are ignored, dangling whitespaces are")
    quotes = {
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
    for k, q in quotes.items():
        where = PINS[s] if k.startswith("q") else PINS[r]
        print("quote %s words=%d line=%d" % (k, len(q.split()), locate(where, q)))
    loc = dict(q147="%s:147-166" % s, q353="%s:350-360" % s, q364="%s:362-366" % s,
               q565="%s:563-567" % s, q805="%s:805-806" % s, q112="%s:110-114" % s,
               b57="%s:55-59" % r, b63="%s:63-65" % r, b133="%s:133-135" % r)
    for k, v in loc.items():
        _, a, b = re.match(r"(.+):(\d+)-(\d+)", v).groups()
        name = k and (s if k.startswith("q") else r)
        if int(b) > pb[name][2]:
            sys.exit("range %s beyond pin lines %d" % (v, pb[name][2]))
        if not (int(a) <= locate(PINS[name], quotes[k]) <= int(b)):
            sys.exit("range %s misses quote line" % v)
    body = """# Which terminal SUPER+RETURN launches: the xdg-terminal-exec 0.14.3 selection chain, executed read-only

source: S326 - xdg-terminal-exec 0.14.3 script at tag - ordered list files, list-line directives, entry-ID lookup, validation keys, exec-argument composition, print modes
source: S327 - xdg-terminal-exec 0.14.3 README at tag - the documented list-file format and eligibility keys this entry executes
source: S328 - xdg-terminal-exec 0.14.3 stock xdg-terminals.list at tag - the lowest-priority system list and its exec-argument defaults
source: S329 - xdg-terminal-exec 0.14.3 man page at tag - the print options and their delimiters
source: S330 - xdg-terminal-exec 0.14.3 test suite at tag - the fixture lists that pin the validation edge classes
verified-at: 2026-10-26
recheck: on-release - when xdg-terminal-exec leaves v0.14.3 re-pull the five pins and re-run quality/counters/c2-r47-terminal-entry.py (or 90d at the latest)
ground: terminal-selection plane, the resolver's executed choice and print composition; the chain was absent at base (claim grep exit 1); held neighbours: the documentary route in terminal-route-r17.md and terminals-and-omarchy.md
Lane: mado-shokunin. Round: 47.

## The executed chain

1. Lists and their order: the resolver builds one ordered list of config files, desktop-prefixed name first inside each directory, config home then config dirs then the xdg-terminal-exec subdirs of the data dirs ("{q147}", {l147}).
2. List lines: `read_config_paths` reads every existing list file up front into one ordered ID list, comments and blanks dropped, directives taken before IDs ("{q353}", {l353}); a missing file is skipped, not an error ("{q364}", {l364}).
3. Entry IDs and actions: `find_entry_paths` and the ID validators turn a line into a candidate entry ID optionally suffixed with an action, and only IDs that pass the ID and action validators enter the list ("{qb57}", {lb57}); the lookup side of the same step is {l3}.
4. Desktop-file lookup: IDs resolve across the applications dirs of the data hierarchy, first hit wins, and an entry is eligible only with the TerminalEmulator category and the X-TerminalArgExec key ("{qb63}", {lb63}); the scan order is {l4}.
5. Validation: `check_entry_key` reads Type, Categories, Hidden and the show-in rules decide acceptance, and TryExec or the Exec program must be executable on PATH ({l5}); the exec-argument keys are read in the same pass ("{q805}", {l805}).
6. Exec-argument composition: the Exec field is tokenized into an argument vector, field codes dropped, and the terminal's own exec argument placed before the command ("{q565}", {l565}); option arguments are appended per key ({l6}).
7. Print modes: the print options select what is written instead of a launch, and the `--print-delimiter` sequences join them ("{q112}", {l112}); the cache is written by the print pass, so a cold-cache read is the pure selection ({l7}).

## Cache

The cache file holds the listing hash, the entry ID, its path, the exec argument vector and the option arguments; a print run with a matching hash reuses it, and the hash covers the config and applications listings ({l8}). The live reading below used an empty cache home, so it models a cold cache.

## This host (live, read-only)

The round-17 [UNK] (corpus/knowledge/terminal-route-r17.md:144-145) asked whether the resolver actually picks that entry over the system one at launch. A cold-cache print run answers it: `.ufo/waves/round-47/receipts/live-host.txt` records the observed print output (`.ufo/waves/round-47/receipts/live-observed.txt`) and the landed tool's verdict `MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop verdict=OK`, so the user override wins over the system entry.
""".format(
        q147=quotes["q147"], l147=loc["q147"],
        q353=quotes["q353"], l353=loc["q353"],
        q364=quotes["q364"], l364=loc["q364"],
        qb57=quotes["b57"], lb57=loc["b57"], l3="%s:420-445" % s,
        qb63=quotes["b63"], lb63=loc["b63"], l4="%s:760-790" % s,
        l5="%s:885-960" % s, q805=quotes["q805"], l805=loc["q805"],
        q565=quotes["q565"], l565=loc["q565"], l6="%s:695-740" % s,
        q112=quotes["q112"], l112=loc["q112"], l7="%s:1272-1310" % s,
        l8="%s:217-300" % s)
    # every script-relative range must sit inside the script pin
    for m in re.finditer(r"xdgte-xdg-terminal-exec:(\d+)-(\d+)", body):
        if int(m.group(2)) > pb[s][2]:
            sys.exit("script range beyond pin: %s" % m.group(0))
    return body, quotes


def build_rows(pb):
    s = "xdgte-xdg-terminal-exec"
    r = "xdgte-README.md"
    li = "xdgte-xdg-terminals.list"
    man = "xdgte-xdg-terminal-exec.1.scd"
    t = "xdgte-test_tests.bats"
    rows = [
        row("S326", "xdg-terminal-exec v0.14.3 selection script at tag - " + URL + "xdg-terminal-exec",
            "code", "A",
            "the executed selection chain of the resolver: list files and their order, list lines and directives, entry-ID and action validation, desktop-file lookup, validation keys, exec-argument composition, print modes, cache",
            "%s:147-166 make_paths list order, %s:352-445 list parsing and entry IDs, %s:760-960 entry lookup and validation, %s:1272-1330 print modes (receipt %s) @ tag v0.14.3 commit %s, %d B sha256:%s; receipt %s%s"
            % (s, s, s, s, s, COMMIT, pb[s][1], pb[s][0], FETCH, s),
            "the print modes select the first valid entry from the ordered list files and write only the cache"),
        row("S327", "xdg-terminal-exec v0.14.3 README at tag - " + URL + "README.md",
            "docs", "A",
            "the documented list-file naming, order, line syntax, eligibility keys and exec-argument keys the resolver implements",
            "%s:55-59 action suffix, %s:63-68 eligibility keys, %s:100-135 list files and their order (receipt %s) @ tag v0.14.3, %d B sha256:%s; receipt %s%s"
            % (r, r, r, r, pb[r][1], pb[r][0], FETCH, r),
            "the spec text the resolver executes: entry IDs in ordered list files, TerminalEmulator eligibility, X-TerminalArg keys"),
        row("S328", "xdg-terminal-exec v0.14.3 stock list at tag - " + URL + "xdg-terminals.list",
            "code", "A",
            "the lowest-priority system terminal list shipped at the tag",
            "%s:1-25 whole file, %d B (receipt %s) @ tag v0.14.3, sha256:%s; receipt %s%s"
            % (li, pb[li][1], li, pb[li][0], FETCH, li),
            "the system list holds no Alacritty row, so the host's user override is not shadowed by a system listing"),
        row("S329", "xdg-terminal-exec v0.14.3 man page at tag - " + URL + "xdg-terminal-exec.1.scd",
            "docs", "A",
            "the print options, their delimiters and the option-to-key mapping",
            "%s:42-50 print options, %s:60-90 argument keys (receipt %s) @ tag v0.14.3, %d B sha256:%s; receipt %s%s"
            % (man, man, man, pb[man][1], pb[man][0], FETCH, man),
            "print modes write the selected ID, path or command instead of launching, which is what makes a read-only observation possible"),
        row("S330", "xdg-terminal-exec v0.14.3 test suite at tag - " + URL + "test/tests.bats",
            "code", "A",
            "the fixture lists and desktop entries that pin the validation edge classes at the tag",
            "%s:1-64 list precedence cases, %s:64-140 hidden and show-in cases (receipt %s) @ tag v0.14.3, %d B sha256:%s; receipt %s%s"
            % (t, t, t, pb[t][1], pb[t][0], FETCH, t),
            "the tag's own tests fix which rejection classes exist, so the chain steps are testable against the same bytes"),
    ]
    return "\n".join(rows)


def build_readme_row():
    return ("| `knowledge/xdg-terminal-selection-r47.md` (MADO-R47-1, round 47; terminal-selection plane) | "
            "The executed selection chain of xdg-terminal-exec 0.14.3 on rows S326-S330: ordered desktop-prefixed "
            "list files, list-line directives, entry-ID and action validation, desktop-file lookup across the data "
            "hierarchy, eligibility keys (TerminalEmulator, X-TerminalArgExec, Hidden, show-in rules, TryExec on PATH), "
            "exec-argument composition and the print modes, plus a live cold-cache reading that the user override "
            "wins over the system entry. | [Source and recheck](knowledge/xdg-terminal-selection-r47.md): §§1 chain "
            "steps 1-7, §2 cache, §3 live verdict; Sources S326-S330. |")


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


def write_tool():
    tool = '''#!/usr/bin/env python3
"""Control double for PRED-C2-r47 clause f mechanics (scratch clone only).

It is NOT the lane tool: it reproduces the receipt's selected/path from the observed
capture so the counter's "the landed tool must reproduce the receipt" path is exercised.
"""
import sys


def main(argv):
    if len(argv) < 3 or argv[1] != "explain":
        sys.stderr.write("usage: mado-terminal.py explain [--observed FILE]\\n")
        return 2
    obs = None
    rest = argv[2:]
    while rest:
        a = rest.pop(0)
        if a == "--observed" and rest:
            obs = rest.pop(0)
        else:
            sys.stderr.write("unknown argument %s\\n" % a)
            return 2
    if obs is None:
        print("MADO_TERM: selected=none path=none verdict=NO_TERMINAL")
        return 3
    with open(obs, encoding="utf-8") as fh:
        lines = [l.strip() for l in fh.read().split("\\n")]
    sel = lines[0] if lines else ""
    pth = lines[1] if len(lines) > 1 else ""
    print("trace: observed capture read")
    print("MADO_TERM: selected=%s path=%s verdict=AGREE" % (sel, pth))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
'''
    with open(os.path.join(D, "tools/mado-terminal.py"), "w", encoding="utf-8") as fh:
        fh.write(tool)
    os.chmod(os.path.join(D, "tools/mado-terminal.py"), 0o644)


def write_receipts(pb):
    obs = ("Alacritty.desktop\n"
           "/home/vgpnk/.local/share/applications/Alacritty.desktop\n"
           "alacritty\n")
    with open(os.path.join(D, ".ufo/waves/round-47/receipts/live-observed.txt"), "w") as fh:
        fh.write(obs)
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
    with open(os.path.join(D, ".ufo/waves/round-47/receipts/live-host.txt"), "w") as fh:
        fh.write(rec)


def main():
    build_tree()
    pb = pins_block()
    body, quotes = build_entry(pb)
    rows = build_rows(pb)
    with open(os.path.join(D, ENTRY), "w", encoding="utf-8") as fh:
        fh.write(body)
    insert_after(os.path.join(D, "corpus/SOURCES.md"),
                 lambda l: re.match(r"^ {0,3}\|\s*S325\s*\|", l), rows)
    insert_after(os.path.join(D, "corpus/README.md"),
                 lambda l: l.startswith("| `knowledge/hyprland-input-devices-r46.md`"),
                 build_readme_row())
    write_receipts(pb)
    run("git", "-C", D, "add", "-A")
    run("git", "-C", D, "commit", "-q", "-m", "control: minimal valid C2 r47 entry")
    out = run("git", "-C", D, "rev-parse", "HEAD").stdout.decode().strip()
    print("POS", out)
    print("entry lines", len(body.split("\n")))
    print("quotes", len(quotes))


if __name__ == "__main__":
    main()
