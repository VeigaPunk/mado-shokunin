#!/usr/bin/env python3
"""Emit the round-47 C2 control bundles into c2/ (one directory per control).

    python3 build-c2-controls.py [--out DIR] [--script PIN] [--readme PIN] [--lane DIR]
                                 [--base REV] [--observed FILE] [--tool-line LINE]

Each bundle is a tree the runner copies over a scratch clone of the lane at base and commits:

    files/<root-relative path>   written (or replaced)
    expect                       TARGET_MET or MISSED
    note                         what is wrong with this control

REF is a minimal entry that satisfies the C2 counter draft's clauses a-i: two new registry rows
(S326 script, S327 README) inside `## Registry`, committed v0.14.3 pin copies under
.ufo/waves/round-47/fetch/ whose sha256 equals the rows', anchor ranges inside the pins, seven
numbered chain steps each with a script locator, quotes that occur verbatim in their pin inside
their stated range, the round-17 [UNK] answered by a live receipt the landed tool reproduces, and
a README index row covering both ids. The five negatives are REF with exactly one property broken.
"""

import argparse
import hashlib
import os
import shutil
import sys

PIN_SHA = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
README_SHA = "c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40"
SCRIPT_URL = ("https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/"
              "v0.14.3/xdg-terminal-exec")
README_URL = ("https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/"
              "v0.14.3/README.md")
BRANCH_SCRIPT_URL = ("https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/"
                     "main/xdg-terminal-exec")
BRANCH_README_URL = ("https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/"
                     "main/README.md")
ENTRY = "corpus/knowledge/xdg-terminal-selection-r47.md"
RECEIPT = ".ufo/waves/round-47/receipts/xdg-terminal-live.txt"
OBSERVED = ".ufo/waves/round-47/receipts/xdg-terminal-observed.txt"
PIN_SCRIPT = ".ufo/waves/round-47/fetch/xdg-terminal-exec"
PIN_README = ".ufo/waves/round-47/fetch/README-v0.14.3.md"
BASE = "60edb66e2f1cb90acc6e9442fc93ded0ca42d750"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
OPENED = "2026-10-26"

# (label, quote, pin, function, reading) - all quotes are checked verbatim at build time
CHAIN = [
    ("List files are built from the config hierarchy first",
     'for xte__dir in ${XDG_CONFIG_HOME:-"${HOME}/.config"}${IFS}${XDG_CONFIG_DIRS:-/etc/xdg}; do',
     "script", "make_paths",
     "each hierarchy directory adds its desktop-prefixed list before its plain list, so the first "
     "readable file wins the tail of the preference order"),
    ("The desktop token is the lowercased XDG_CURRENT_DESKTOP",
     "for xte__desktop in ${XTE__LOWERCASE_XDG_CURRENT_DESKTOP}; do",
     "script", "make_paths",
     "a colon-separated desktop list contributes one prefixed list per item, in that order"),
    ("Every list line becomes a preference in file order",
     'debug "added entry ID with action ID \'$xte__line\'"',
     "script", "read_config_paths",
     "read_config_paths appends a validated entry id as it reads, and discards the rest with a "
     "message, so a line is a preference and not a guarantee"),
    ("Duplicate desktop-file ids resolve to the last found",
     "# Entries are checked in ascending order of preference, so use last found if duplicate",
     "script", "find_entry_paths",
     "find_entry_paths registers the ids it finds in ascending preference and keeps the last, "
     "which is how a user-local entry shadows the system copy"),
    ("The explicit list is walked, then the fallback",
     "for xte__entry_id in ${XTE__ENTRY_IDS}${XTE__LF}//fallback_start//${XTE__LF}$XTE__FALLBACK_ENTRY_IDS; do",
     "script", "find_entry",
     "find_entry tries the listed ids first with the desktop show-in checks off, then flips them on "
     "at the marker and walks the fallback ids"),
    ("An entry must parse and declare the terminal category",
     '[ -z "${XTE__IS_TERMINAL}" ] && continue',
     "script", "find_entry",
     "check_entry_key sets the terminal flag only for a TerminalEmulator category, and find_entry "
     "skips any candidate that has no parsed Exec or no terminal category"),
    ("The printed path is the file path, not the find start path",
     "*'/./'*) XTE__ENTRY_PATH=${XTE__ENTRY_PATH%%/./*}/${XTE__ENTRY_PATH##*/./} ;;",
     "script", "__local__",
     "print-path compacts the /./ separator find leaves in the start path, so the printed path is "
     "the desktop file itself"),
]

DOCUMENTED = [
    ("Configuration files are named",
     'Configuration files are named `${desktop}-xdg-terminals.list` or `xdg-terminals.list`',
     "readme", (100, 101),
     "the two file names the script builds"),
    ("The list format",
     "The format is a simple newline-separated list with decreasing priority.",
     "readme", (131, 131),
     "one id per line, decreasing priority downwards"),
    ("Applicability is checked per entry",
     "Each entry from the explicit selection list is checked for applicability:",
     "readme", (166, 166),
     "a listed id is a candidate, not a promise"),
]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def collapse_map(text):
    """The counter's collapse(): one line, every emitted char remembering its source line."""
    out, linemap, prev = [], [], True
    for ln, line in enumerate(text.split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    out.append(" ")
                    linemap.append(ln)
                    prev = True
            else:
                out.append(ch)
                linemap.append(ln)
                prev = False
    return "".join(out), linemap


def occurrences(text, needle):
    hay, linemap = collapse_map(text)
    needle = " ".join(needle.split())
    out = []
    start = 0
    while True:
        k = hay.find(needle, start)
        if k < 0:
            return out
        before = hay[k - 1] if k > 0 else " "
        after = hay[k + len(needle)] if k + len(needle) < len(hay) else " "

        def word(c):
            return c.isalnum() or c == "_"

        if not (word(needle[0]) and word(before)) and not (word(needle[-1]) and word(after)):
            out.append(linemap[k])
        start = k + 1


def function_spans(text):
    lines = text.split("\n")
    starts = []
    for i, line in enumerate(lines, 1):
        if line.endswith("() {") and not line.startswith((" ", "\t")):
            starts.append((line.split("(")[0], i))
    spans = {}
    for idx, (name, start) in enumerate(starts):
        end = starts[idx + 1][1] - 1 if idx + 1 < len(starts) else len(lines)
        spans[name] = (start, end)
    return spans


def check_quote(pin_text, quote, lo, hi, where):
    hits = occurrences(pin_text, quote)
    if not hits:
        raise SystemExit("%s: quote not in pin: %r" % (where, quote[:60]))
    if not any(lo <= h <= hi for h in hits):
        raise SystemExit("%s: quote only at %s, outside %d-%d: %r"
                         % (where, hits[:3], lo, hi, quote[:60]))
    if not 2 <= len(quote.split()) <= 25:
        raise SystemExit("%s: quote word count %d out of 2..25: %r"
                         % (where, len(quote.split()), quote[:60]))
    return hits


def build_entry(script_text, readme_text, spans, tool_sha, forged=None, table=False,
                receipt=RECEIPT):
    out = []
    out.append("source: S326 (%s @ tag v0.14.3, sha256 %s, pin %s)"
               % (SCRIPT_URL, PIN_SHA, PIN_SCRIPT))
    out.append("source: S327 (%s @ tag v0.14.3, sha256 %s, pin %s)"
               % (README_URL, README_SHA, PIN_README))
    out.append("verified-at: %s" % OPENED)
    out.append("recheck: 90d")
    out.append("surface: P4")
    out.append("scope: the print-mode selection chain of one resolver version on this host; the "
               "launch itself, rendered windows and reload effects stay out of scope")
    out.append("")
    out.append("# Terminal selection by xdg-terminal-exec 0.14.3 - the executed chain")
    out.append("")
    out.append("The selection order below is read from the pinned script bytes, and the "
               "host's own selection is confirmed by a live read-only receipt (`%s`)."
               % receipt)
    out.append("")
    if table:
        out.append("## Chain (citation index)")
        out.append("")
        out.append("| surface | locator | quote | reading |")
        out.append("|---|---|---|---|")
        for label, quote, pin, target, reading in CHAIN:
            if target == "__local__":
                hits = occurrences(script_text, quote)
                lo, hi = max(1, hits[0] - 2), hits[0] + 2
            else:
                lo, hi = spans[target]
            out.append("| %s | xdg-terminal-exec:%d-%d | `%s` | %s |"
                       % (label, lo, hi, quote, reading))
        out.append("")
        out.append("The rows above list where each surface lives; the order they imply is the "
                   "reader's, not the resolver's.")
    else:
        out.append("## The executed chain")
        out.append("")
        for i, (label, quote, pin, target, reading) in enumerate(CHAIN, 1):
            lo, hi = (max(1, occurrences(script_text, quote)[0] - 2),
                      occurrences(script_text, quote)[0] + 2) if target == "__local__" \
                else spans[target]
            if forged is not None and i == 4:
                quote = forged
            out.append("%d. **%s.** `%s` (xdg-terminal-exec:%d-%d) - %s."
                       % (i, label, quote, lo, hi, reading))
        out.append("")
    out.append("## The documented contract")
    out.append("")
    for label, quote, pin, (lo, hi), reading in DOCUMENTED:
        out.append("- **%s.** \"%s\" (README-v0.14.3.md:%d-%d) - %s."
                   % (label, quote, lo, hi, reading))
    out.append("")
    out.append("The documented route names the option surface, including the "
               "`--print-delimiter=seq` separator and the `--print-cmd` command renderer; the "
               "script's `print-delimiter` handling and its print blocks are the executed side of "
               "the same contract.")
    out.append("")
    out.append("## The round-17 unknown, answered for the selection stage")
    out.append("")
    out.append("Round 17 left `[UNK]` whether the resolver actually picks the user-local entry "
               "over the system one (`corpus/knowledge/terminal-route-r17.md:144`). The live "
               "receipt `%s` answers the selection stage: the `--print-id --print-path "
               "--print-cmd` capture names the user override entry, and re-running the landed "
               "tool over that capture reports `verdict=AGREE`. The launch of a window is not "
               "observed and is not claimed." % receipt)
    out.append("")
    out.append("## Held ground")
    out.append("")
    out.append("The documentary route stays with its own note and rows; nothing here restates "
               "the README-level contract as host behaviour, and no terminal tree note is "
               "reopened.")
    out.append("")
    out.append("Pins: `%s`, `%s`. Receipt: `%s`." % (PIN_SCRIPT, PIN_README, receipt))
    out.append("")
    return "\n".join(out)


def rows(script_text, readme_text, spans, ids, entry=ENTRY, script_url=SCRIPT_URL,
         readme_url=README_URL):
    s_lo = spans["make_paths"]
    ranges = ", ".join("xdg-terminal-exec:%d-%d" % spans[k]
                       for k in ("make_paths", "read_config_paths", "find_entry_paths",
                                 "find_entry"))
    r1 = ("| S326 | xdg-terminal-exec v0.14.3 reference script - %s | code | A | The print-mode "
          "selection chain of the resolver this host installs (list order, entry ids, duplicate "
          "resolution, fallback walk, print modes) | %s (receipt xdg-terminal-exec) @ tag v0.14.3, "
          "%d B sha256:%s; receipt %s | How the list files, the entry ids, the duplicate "
          "resolution and the fallback walk order the candidates, and what each print mode "
          "renders | mined | %s | 90d | %s |"
          % (script_url, ranges, len(script_text.encode("utf-8", "surrogateescape")), PIN_SHA,
             PIN_SCRIPT, OPENED, entry))
    r2 = ("| S327 | xdg-terminal-exec v0.14.3 README - %s | docs | A | The documented file names, "
          "list format and per-entry applicability of the selection | README-v0.14.3.md:100-101 "
          "file names, README-v0.14.3.md:131 list format, README-v0.14.3.md:166 applicability "
          "(receipt README-v0.14.3.md) @ tag v0.14.3, %d B sha256:%s; receipt %s | That a "
          "list file is a preference list with decreasing priority, and that every listed id is "
          "still checked for applicability before it is used | mined | %s | 90d | %s |"
          % (readme_url, len(readme_text.encode("utf-8", "surrogateescape")), README_SHA,
             PIN_README, OPENED, entry))
    return r1, r2


def readme_row(ids):
    span = "S326-S327" if len(ids) == 2 else ids[0]
    return ("| `knowledge/xdg-terminal-selection-r47.md` (round 47; surface P4) | The executed "
            "selection chain of xdg-terminal-exec 0.14.3: list-file order, desktop-prefixed "
            "lists, desktop-file ids across data dirs, duplicate resolution, the fallback walk "
            "and the print modes; the round-17 selection question is answered by a live "
            "read-only receipt. | `source:` %s in [SOURCES](SOURCES.md); tag-pinned script and "
            "README copies under `.ufo/waves/round-47/fetch/`; live receipt "
            "`.ufo/waves/round-47/receipts/xdg-terminal-live.txt`. No terminal was launched. |"
            % span)


def insert_registry_rows(sources_text, new_rows):
    lines = sources_text.split("\n")
    try:
        start = lines.index("## Registry")
    except ValueError:
        raise SystemExit("insert_registry_rows: no '## Registry' section")
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    last_row = None
    for i in range(start + 1, end):
        if lines[i].startswith("| S") and lines[i].rstrip().endswith("|"):
            last_row = i
    if last_row is None:
        raise SystemExit("insert_registry_rows: no registry row found")
    if any(l.startswith("| S326 ") or l.startswith("| S327 ") for l in lines):
        raise SystemExit("insert_registry_rows: rows already present in the base file")
    return "\n".join(lines[:last_row + 1] + list(new_rows) + lines[last_row + 1:])


def insert_readme_row(readme_text, row):
    lines = readme_text.split("\n")
    anchor = None
    for i, line in enumerate(lines):
        if line.startswith("| `knowledge/terminal-route-r17.md`"):
            anchor = i
    if anchor is None:
        for i, line in enumerate(lines):
            if line.startswith("| `knowledge/"):
                anchor = i
    if anchor is None:
        raise SystemExit("insert_readme_row: no index row found")
    return "\n".join(lines[:anchor + 1] + [row] + lines[anchor + 1:])


def receipt_text(observed_path, observed_bytes, tool_sha, env, mado_line):
    return ("# xdg-terminal selection - live read-only receipt (round 47, %s)\n"
            "\n"
            "observed=%s\n"
            "\n"
            "# environment the observation ran under (env -i, XDG_CACHE_HOME in scratch)\n"
            "\n"
            "%s\n"
            "\n"
            "tool: tools/mado-terminal.py sha256 %s\n"
            "oracle: /usr/bin/xdg-terminal-exec sha256 %s\n"
            "\n"
            "## capture (xdg-terminal-exec --print-id --print-path --print-cmd, rc=0)\n"
            "\n"
            "```\n"
            "%s"
            "```\n"
            "\n"
            "## tool reading\n"
            "\n"
            "%s\n"
            "\n"
            "The resolver selects the user override entry and prints its path under "
            "~/.local/share/applications/, so the round-17 question is answered for the "
            "selection stage: the user-local entry wins over the system one. No terminal "
            "process was started and no compositor verb was sent; the launch of a window is "
            "not observed and is not claimed.\n"
            % (OPENED, observed_path, env, tool_sha, PIN_SHA,
               observed_bytes.decode("utf-8", "replace"), mado_line))


def write_bundle(root, files, expect, note):
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(root)
    for path, data in files.items():
        dest = os.path.join(root, "files", path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(data if isinstance(data, bytes) else data.encode("utf-8"))
    with open(os.path.join(root, "expect"), "w") as fh:
        fh.write(expect + "\n")
    with open(os.path.join(root, "note"), "w") as fh:
        fh.write(note.rstrip() + "\n")


def git_show(path):
    import subprocess
    proc = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (BASE, path)],
                          capture_output=True)
    if proc.returncode != 0:
        raise SystemExit("git show %s failed: %s" % (path, proc.stderr.decode()))
    return proc.stdout


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(here, "c2"))
    ap.add_argument("--script", default=os.path.join(here, "pins", "xdg-terminal-exec"))
    ap.add_argument("--readme", default=os.path.join(here, "pins", "README-v0.14.3.md"))
    ap.add_argument("--lane", default=LANE)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--observed", default=os.path.join(here, "pins", "observed.txt"))
    ap.add_argument("--tool-line", default=None)
    ap.add_argument("--tool", default=os.path.join(here, "c1", "REF-MINI.py"))
    args = ap.parse_args()

    with open(args.script, "rb") as fh:
        script_bytes = fh.read()
    if sha256(script_bytes) != PIN_SHA:
        raise SystemExit("script pin sha %s != %s" % (sha256(script_bytes), PIN_SHA))
    with open(args.readme, "rb") as fh:
        readme_bytes = fh.read()
    if sha256(readme_bytes) != README_SHA:
        raise SystemExit("readme pin sha %s != %s" % (sha256(readme_bytes), README_SHA))
    with open(args.tool, "rb") as fh:
        tool_bytes = fh.read()
    tool_sha = sha256(tool_bytes)
    with open(args.observed, "rb") as fh:
        observed_bytes = fh.read()
    observed_lines = observed_bytes.decode("utf-8").split("\n")
    if len(observed_lines) < 3:
        raise SystemExit("observed capture needs --print-id/--print-path/--print-cmd lines")
    sel, pth = observed_lines[0].strip(), observed_lines[1].strip()
    mado = "MADO_TERM: selected=%s path=%s verdict=AGREE" % (sel, pth)
    if args.tool_line:
        mado = args.tool_line
    env = ("XDG_CURRENT_DESKTOP=Hyprland\nXDG_CONFIG_HOME=/home/vgpnk/.config\n"
           "XDG_CONFIG_DIRS=/etc/xdg\nXDG_DATA_HOME=/home/vgpnk/.local/share\n"
           "XDG_DATA_DIRS=/usr/local/share:/usr/share\n"
           "XDG_CACHE_HOME=<scratch, empty: the tool models a cold cache>")

    script_text = script_bytes.decode("utf-8", "surrogateescape")
    readme_text = readme_bytes.decode("utf-8", "surrogateescape")
    spans = function_spans(script_text)
    for need in ("make_paths", "read_config_paths", "find_entry_paths", "find_entry"):
        if need not in spans:
            raise SystemExit("function %s not found in the pin" % need)

    # every quote must live inside its stated range, verified before anything is written
    for label, quote, pin, target, reading in CHAIN:
        if target == "__local__":
            hits = occurrences(script_text, quote)
            if not hits:
                raise SystemExit("quote not in pin: %r" % quote[:60])
            check_quote(script_text, quote, max(1, hits[0] - 2), hits[0] + 2, label)
        else:
            lo, hi = spans[target]
            check_quote(script_text, quote, lo, hi, label)
    for label, quote, _pin, (lo, hi), _r in DOCUMENTED:
        check_quote(readme_text, quote, lo, hi, label)

    sources_base = git_show("corpus/SOURCES.md").decode("utf-8", "surrogateescape")
    readme_base = git_show("corpus/README.md").decode("utf-8", "surrogateescape")
    r1, r2 = rows(script_text, readme_text, spans, ["S326", "S327"])
    sources = insert_registry_rows(sources_base, [r1, r2])
    readme = insert_readme_row(readme_base, readme_row(["S326", "S327"]))
    entry = build_entry(script_text, readme_text, spans, tool_sha)
    receipt = receipt_text(OBSERVED, observed_bytes, tool_sha, env, mado)

    common = {
        ENTRY: entry,
        "corpus/SOURCES.md": sources,
        "corpus/README.md": readme,
        PIN_SCRIPT: script_bytes,
        PIN_README: readme_bytes,
        RECEIPT: receipt,
        OBSERVED: observed_bytes,
        "tools/mado-terminal.py": tool_bytes,
    }
    os.makedirs(args.out, exist_ok=True)
    write_bundle(os.path.join(args.out, "REF"), common, "TARGET_MET",
                 "positive control: the minimal entry the C2 contract admits (two new rows S326 "
                 "S327 at tag URLs, committed v0.14.3 pins matching the rows' digests, seven "
                 "numbered steps with script locators, quotes verbatim inside their ranges, the "
                 "round-17 selection answer as a live receipt the landed tool reproduces, README "
                 "row)")

    write_bundle(os.path.join(args.out, "BASE"),
                 {".ufo/waves/round-47/w1/ExecControls-base-marker.txt":
                  "control BASE: this revision carries no new entry; the claim's artifact is "
                  "absent.\n"}, "MISSED",
                 "no entry at the revision: clause a sees no artifact to admit.")

    empty = dict(common)
    empty[ENTRY] = ""
    write_bundle(os.path.join(args.out, "EMPTY"), empty, "MISSED",
                 "evidence-shaped surroundings with zero entry bytes: provenance head, chain, "
                 "quotes and the round-17 answer are all missing.")

    write_bundle(os.path.join(args.out, "FORGED-QUOTE"),
                 dict(common, **{ENTRY: build_entry(script_text, readme_text, spans, tool_sha,
                                                    forged="The resolver caches its choice in the "
                                                           "first writable data directory")}),
                 "MISSED",
                 "step 4 carries plausible prose that does not occur in the pinned bytes: the "
                 "quote check has to reject it even though every locator is real.")

    rb1, rb2 = rows(script_text, readme_text, spans, ["S326", "S327"],
                    script_url=BRANCH_SCRIPT_URL, readme_url=BRANCH_README_URL)
    branch_sources = insert_registry_rows(sources_base, [rb1, rb2])
    write_bundle(os.path.join(args.out, "BRANCH-URL"), dict(common, **{
        "corpus/SOURCES.md": branch_sources}), "MISSED",
        "the same entry, but both rows anchor at branch URLs (main) instead of the tag: the pin "
        "is not versioned, and a moving target cannot bind a quote.")

    write_bundle(os.path.join(args.out, "INDEX-NOT-CHAIN"),
                 dict(common, **{ENTRY: build_entry(script_text, readme_text, spans, tool_sha,
                                                    table=True)}), "MISSED",
                 "the same rows and locators arranged as a citation table: zero numbered chain "
                 "steps, so the sourced order the claim is about is never stated.")

    absent = dict(common)
    absent.pop(RECEIPT)
    absent[ENTRY] = build_entry(script_text, readme_text, spans, tool_sha,
                                receipt=".ufo/waves/round-47/receipts/xdg-terminal-missing.txt")
    write_bundle(os.path.join(args.out, "RECEIPT-ABSENT"), absent, "MISSED",
                 "the round-17 answer cites a live receipt that is not committed: the claim "
                 "stands on prose, and the landed tool is never re-run over a capture.")

    for name in sorted(os.listdir(args.out)):
        path = os.path.join(args.out, name)
        if not os.path.isdir(path):
            continue
        with open(os.path.join(path, "expect")) as fh:
            expect = fh.read().strip()
        n = 0
        for base_dir, _dirs, names in os.walk(os.path.join(path, "files")):
            n += len(names)
        print("%-16s expect=%s files=%d" % (name, expect, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
