#!/usr/bin/env python3
"""Stage the *real* round-52 C2 entry draft (seat C2EntryDraft) into a scratch clone and run
the draft counter against it.

This is the interop test: the draft counter must read an entry written by a different seat, in
that seat's table shape, without being taught the draft's exact header strings.  The staged
entry is the sibling's byte-for-byte draft, plus the registry rows and README index row the
entry needs (the sibling explicitly leaves the registry edit to the data seat).

Usage:
    python3 make-draft-fixture.py --lane <lane> --work <scratch> --counter <counter path>
Prints the fixture rev, then the counter's output; exits non-zero if the counter does not pass.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

BASE = "85d57a818c3707397e21c840b6498b105ba798aa"
DRAFT_REL = ".ufo/waves/round-52/w1/C2EntryDraft/entry-draft.md"
FETCH_REL = ".ufo/waves/round-52/w1/C2EntryDraft/fetch"
ENTRY_REL = "corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md"
REVISION = "efb50993780079460b0cbed1363e2166a2de1d9f"
ACCESS_DATE = "2026-10-27"

# The rows the sibling draft proposes, in the registry's own column shape.  The scope and
# teaches text is the sibling's own wording, read from the draft's `source:` lines.
ROWS = [
    ("S370", "Hyprland 0.56.2 legacy dispatcher translator, the two synthetic-event "
             "dispatchers - https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/config/"
             "legacy/DispatcherTranslator.cpp" % REVISION,
     "code", "A",
     "how `sendshortcut` and `sendkeystate` read their fields, resolve a keycode, choose a "
     "window and delegate",
     "Hyprland-legacy-DispatcherTranslator.cpp:531-535,591-624 @ %s; pin %s/"
     "Hyprland-legacy-DispatcherTranslator.cpp" % (REVISION, FETCH_REL),
     "the two synthetic-event dispatchers read a fixed number of fields, resolve a keycode, "
     "choose a window and delegate",
     "Hyprland-legacy-DispatcherTranslator.cpp"),
    ("S371", "Hyprland 0.56.2 action state and seat delivery for a synthetic event - "
             "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/config/shared/actions/"
             "ConfigActions.cpp" % REVISION,
     "code", "A",
     "the press field's read, the modifier mask sequence, the timestamp and keycode the seat "
     "receives, and the `Actions::sendKeyState` twin",
     "Hyprland-ConfigActions.cpp:1554-1615 @ %s; pin %s/Hyprland-ConfigActions.cpp"
     % (REVISION, FETCH_REL),
     "the seat delivery path sends the modifier mask, the timestamped keycode and the press "
     "field, and restores the field afterwards",
     "Hyprland-ConfigActions.cpp"),
    ("S372", "Hyprland 0.56.2 action-state declaration - "
             "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/config/shared/actions/"
             "ConfigActions.hpp" % REVISION,
     "code", "A",
     "the fields a dispatcher borrows (press marker, last key, last mouse button, last "
     "timestamp) and the `std::expected` action result",
     "Hyprland-ConfigActions.hpp:36,114,117 @ %s; pin %s/Hyprland-ConfigActions.hpp"
     % (REVISION, FETCH_REL),
     "the declaration names the press marker, the last timestamp and the expected action "
     "result the dispatchers read",
     "Hyprland-ConfigActions.hpp"),
    ("S373", "Hyprland 0.56.2 modifier-string parser and keycode cache - "
             "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/managers/"
             "KeybindManager.cpp" % REVISION,
     "code", "A",
     "`stringToModMask`'s substring membership and the `m_keyToCodeCache` member it fills",
     "Hyprland-KeybindManager.cpp:221-240 @ %s; pin %s/Hyprland-KeybindManager.cpp"
     % (REVISION, FETCH_REL),
     "the modifier parser matches uppercased substrings and the keycode cache is keyed by "
     "keyboard pointer and raw key text",
     "Hyprland-KeybindManager.cpp"),
]


def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p


def assert_toplevel(repo, expect):
    top = git(repo, "rev-parse", "--show-toplevel").stdout.strip()
    if os.path.realpath(top) != os.path.realpath(expect):
        raise SystemExit("refusing to mutate: toplevel %s != %s" % (top, expect))


def read(p):
    with open(p) as fh:
        return fh.read()


def write(p, t):
    with open(p, "w") as fh:
        fh.write(t)


def apply_markdown_fixes(text, tsv_path):
    """Apply the two corrections the draft's markdown table needs, using the draft's own TSV.

    1. The markdown table's pin column carries a bare `:NNN` continuation after a file switch
       (P08-P12 continue from P07's `KeybindManager.cpp`), but the draft's TSV gives the real
       pin for each proposition; the markdown table takes the TSV's anchor.
    2. P07's quote cell contains an unescaped `|`, which splits the markdown row into eight
       cells and shifts the support column; the pipe is escaped.

    The claim text, the rows and the quotes are untouched.
    """
    anchors = {}
    with open(tsv_path) as fh:
        header = fh.readline().rstrip("\n").split("\t")
        ix = {name: i for i, name in enumerate(header)}
        for line in fh:
            if not line.strip():
                continue
            cells = line.rstrip("\n").split("\t")
            anchors[cells[ix["prop"]]] = cells[ix["anchor"]]
    out = []
    for line in text.splitlines():
        if line.startswith("| P") and "|" in line:
            cells = line.split(" | ")
            pid = cells[0].lstrip("| ").strip()
            if pid in anchors:
                anchor = anchors[pid].rsplit("/", 1)[-1]
                # the pin column is the fourth cell
                if len(cells) >= 5:
                    cells[3] = " %s" % anchor
                line = " | ".join(cells)
                line = line.replace("modMask |= HL_MODIFIER_SHIFT;",
                                    "modMask \\|= HL_MODIFIER_SHIFT;")
        out.append(line)
    return "\n".join(out) + "\n"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--counter", required=True)
    ap.add_argument("--fix", action="store_true",
                    help="apply the markdown table corrections (satisfiability control)")
    args = ap.parse_args(argv)

    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    clone = os.path.join(work, "draft-fixture")
    if os.path.exists(clone):
        shutil.rmtree(clone)
    subprocess.run(["git", "clone", "--no-hardlinks", "--quiet", args.lane, clone], check=True)
    assert_toplevel(clone, clone)
    git(clone, "checkout", "--quiet", BASE)
    git(clone, "checkout", "-q", "-b", "fixture/draft")
    assert_toplevel(clone, clone)

    # The sibling's draft bytes and its staged pins, copied verbatim into the clone.
    draft_src = os.path.join(args.lane, DRAFT_REL)
    if not os.path.exists(draft_src):
        raise SystemExit("sibling draft not found: %s" % draft_src)
    os.makedirs(os.path.join(clone, FETCH_REL), exist_ok=True)
    fetch_src = os.path.join(args.lane, FETCH_REL)
    for name in os.listdir(fetch_src):
        if name.endswith((".cpp", ".hpp")):
            shutil.copyfile(os.path.join(fetch_src, name),
                            os.path.join(clone, FETCH_REL, name))
    entry_path = os.path.join(clone, ENTRY_REL)
    os.makedirs(os.path.dirname(entry_path), exist_ok=True)
    draft_text = read(draft_src)
    if args.fix:
        tsv = os.path.join(args.lane, ".ufo/waves/round-52/w1/C2EntryDraft/proposition-map.tsv")
        draft_text = apply_markdown_fixes(draft_text, tsv)
    write(entry_path, draft_text)

    # Registry rows: the sibling's proposed S370-S373, appended to the registry table.
    reg_path = os.path.join(clone, "corpus/SOURCES.md")
    lines = read(reg_path).splitlines()
    last = max(i for i, l in enumerate(lines) if re.match(r"^\| S\d{3,} ", l))
    new = []
    for rowid, source, kind, tier, scope, anchor, teaches, _pin in ROWS:
        new.append("| %s | %s | %s | %s | %s | %s | %s | mined | %s | on-release | %s |"
                   % (rowid, source, kind, tier, scope, anchor, teaches, ACCESS_DATE,
                      "corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md"))
    lines[last + 1:last + 1] = new
    write(reg_path, "\n".join(lines) + "\n")

    # README index row.
    readme_path = os.path.join(clone, "corpus/README.md")
    write(readme_path, read(readme_path).rstrip("\n")
          + "\n| `knowledge/hyprland-synthetic-key-dispatch-r52.md` (MADO-R52-1, round 52) | "
            "Synthetic key events on Hyprland 0.56.2: sendshortcut and sendkeystate. |\n")

    git(clone, "add", "-A")
    git(clone, "-c", "user.name=fixture", "-c", "user.email=fixture@localhost",
        "commit", "-q", "-m", "fixture: the real round-52 C2 entry draft, staged")
    rev = git(clone, "rev-parse", "HEAD").stdout.strip()
    print("fixture=%s rev=%s" % (clone, rev))

    env = dict(os.environ)
    env["TMPDIR"] = work
    p = subprocess.run([sys.executable, "-I", args.counter, "--repo", clone, "--rev", rev,
                        "--entry", ENTRY_REL, "--work", os.path.join(work, "w")],
                       capture_output=True, text=True, env=env)
    print(p.stdout + p.stderr)
    print("exit=%d" % p.returncode)
    return p.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
