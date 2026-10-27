#!/usr/bin/env python3
"""Build the staged C2 fixture: a scratch clone of the lane at the frozen base plus one
commit that adds a proposition-bound dispatcher entry, its registry rows, its README index
row and its pinned source files.

The fixture is a *staged* artifact for the counter draft only: the entry it stages is written
here to exercise every clause, and it is not the round-52 entry.  Nothing is written into the
lane; the clone lives under the seat's scratch dir.

Usage:
    python3 make-fixture.py --lane <lane repo> --work <scratch dir> [--name <fixture name>]

Prints the fixture commit sha on the last line.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

BASE = "85d57a818c3707397e21c840b6498b105ba798aa"
ENTRY_REL = "corpus/knowledge/hyprland-dispatcher-action-effects-r52.md"
ENTRY_NAME = "hyprland-dispatcher-action-effects-r52.md"
FETCH_ROOT = ".ufo/waves/round-52/fetch"
REVISION = "efb50993780079460b0cbed1363e2166a2de1d9f"
ACCESS_DATE = "2026-10-27"

# The staged entry is about the *argument-resolution* half of the legacy dispatcher table:
# how a dispatcher's argument string is turned into a window or a workspace.  That is a
# different surface from the round-51 entry (map population, press-time lookup, submap/pass,
# socket verb): the round-51 entry read five dispatchers' own splitting but never read the
# shared helpers that turn a resolved argument into a target.
PROPS = [
    ("P1", "A dispatcher that names a window resolves it through the shared window-argument "
           "helper, not through its own code.",
     "S370", "Hyprland-legacy-DispatcherTranslator.cpp:45-48",
     "`return Desktop::viewState()->query().selector(arg).runWindow();`",
     "The helper is the only place a dispatcher argument becomes a window, and its selector "
     "call is the line the pin shows."),
    ("P2", "An empty argument or the literal `active` selects the focused window instead of "
           "running the selector.",
     "S370", "Hyprland-legacy-DispatcherTranslator.cpp:46-47",
     "`if (arg.empty() || arg == \"active\")`",
     "The early return with its comment names the focused-window path, so the empty and "
     "`active` forms never reach the selector."),
    ("P3", "A dispatcher that names a workspace resolves it through the shared "
           "workspace-argument helper.",
     "S371", "Hyprland-legacy-DispatcherTranslator.cpp:52-53",
     "`const auto& [id, name, isAutoID] = getWorkspaceIDNameFromString(args);`",
     "The helper parses the argument into an id and a name before any workspace is looked up, "
     "and the pin shows that parse as the first statement."),
    ("P4", "The workspace helper creates a workspace that does not exist yet when the "
           "compositor holds no workspace with that id.",
     "S371", "Hyprland-legacy-DispatcherTranslator.cpp:60",
     "`ws = State::workspaceState()->create(id, PMONITOR->m_id, name, false);`",
     "The create call is the helper's own creation step and the pin shows the monitor the new "
     "workspace is attached to."),
    ("P5", "The `movewindow` dispatcher strips a trailing ` silent` before it reads its "
           "argument, so the suffix is not part of the direction character.",
     "S372", "Hyprland-legacy-DispatcherTranslator.cpp:251-252",
     "`bool silent    = args.ends_with(\" silent\");`",
     "The suffix test and the substr that removes it are consecutive statements, so the "
     "argument the direction parser sees no longer carries the suffix."),
]

# The two registry rows the staged entry cites.  Both are new at the fixture commit, mined,
# opened this round, anchored to the round-52 fetch root and the pinned revision.
ROWS = [
    ("S370", "Hyprland 0.56.2 legacy dispatcher window-argument resolution - "
             "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/config/legacy/"
             "DispatcherTranslator.cpp" % REVISION,
     "code", "A",
     "how a dispatcher argument naming a window becomes a window: the empty/active shortcut, "
     "the selector call, and the shared helper's signature",
     "Hyprland-legacy-DispatcherTranslator.cpp:44-48 @ %s; pin %s/Hyprland-legacy-"
     "DispatcherTranslator.cpp" % (REVISION, FETCH_ROOT),
     "the shared helper resolves a window argument through the view-state selector, or takes "
     "the focused window when the argument is empty or `active`"),
    ("S371", "Hyprland 0.56.2 legacy dispatcher workspace-argument resolution - "
             "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/config/legacy/"
             "DispatcherTranslator.cpp" % REVISION,
     "code", "A",
     "how a dispatcher argument naming a workspace becomes a workspace: the id/name parse and "
     "the creation of an absent workspace",
     "Hyprland-legacy-DispatcherTranslator.cpp:51-62 @ %s; pin %s/Hyprland-legacy-"
     "DispatcherTranslator.cpp" % (REVISION, FETCH_ROOT),
     "the shared helper parses a workspace argument into an id and a name and creates the "
     "workspace when the compositor holds none with that id"),
    ("S372", "Hyprland 0.56.2 legacy movewindow dispatcher argument preparation - "
             "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/config/legacy/"
             "DispatcherTranslator.cpp" % REVISION,
     "code", "A",
     "how the movewindow dispatcher prepares its argument before the direction is read: the "
     "silent suffix and the mon: prefix",
     "Hyprland-legacy-DispatcherTranslator.cpp:248-256 @ %s; pin %s/Hyprland-legacy-"
     "DispatcherTranslator.cpp" % (REVISION, FETCH_ROOT),
     "movewindow removes a trailing silent and recognises a mon: prefix before it reads the "
     "direction character"),
]

REGISTRY_HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | "
                   "recheck | used-by |")


def cell(text):
    """A markdown table cell: any `|` inside is escaped so the row keeps its columns."""
    return (text or "").replace("|", "\\|").replace("\n", " ")


def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed in %s: %s" % (" ".join(args), repo, p.stderr.strip()))
    return p


def assert_toplevel(repo, expect):
    top = git(repo, "rev-parse", "--show-toplevel").stdout.strip()
    real = os.path.realpath(top)
    if real != os.path.realpath(expect):
        raise SystemExit("refusing to mutate: toplevel %s != fixture %s" % (real, expect))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--name", default="fixture")
    args = ap.parse_args(argv)

    work = os.path.abspath(args.work)
    clone = os.path.join(work, args.name)
    if os.path.exists(clone):
        shutil.rmtree(clone)
    os.makedirs(work, exist_ok=True)

    subprocess.run(["git", "clone", "--no-hardlinks", "--quiet", args.lane, clone], check=True)
    assert_toplevel(clone, clone)
    git(clone, "checkout", "--quiet", BASE)
    git(clone, "checkout", "-q", "-b", "fixture/%s" % args.name)
    assert_toplevel(clone, clone)

    # The pinned source file: the round-51 pin bytes are the same upstream file at the same
    # revision, so the fixture copies them into the round-52 fetch root rather than fetching.
    src_pin = os.path.join(args.lane, ".ufo/waves/round-51/fetch/"
                           "Hyprland-legacy-DispatcherTranslator.cpp")
    dst_dir = os.path.join(clone, FETCH_ROOT)
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copyfile(src_pin, os.path.join(dst_dir, "Hyprland-legacy-DispatcherTranslator.cpp"))

    # Registry rows: appended to the registry table, in the table's own column shape.
    reg_path = os.path.join(clone, "corpus/SOURCES.md")
    with open(reg_path) as fh:
        reg = fh.read()
    lines = reg.splitlines()
    last_row = max(i for i, l in enumerate(lines)
                   if re.match(r"^\| S\d{3,} ", l))
    new_rows = []
    for rowid, source, kind, tier, scope, anchor, teaches in ROWS:
        new_rows.append("| %s | %s | %s | %s | %s | %s | %s | mined | %s | on-release | %s |"
                        % (rowid, source, kind, tier, scope, anchor, teaches, ACCESS_DATE,
                           "corpus/knowledge/%s" % ENTRY_NAME))
    lines[last_row + 1:last_row + 1] = new_rows
    with open(reg_path, "w") as fh:
        fh.write("\n".join(lines) + "\n")

    # README index row.
    readme_path = os.path.join(clone, "corpus/README.md")
    with open(readme_path) as fh:
        readme = fh.read().splitlines()
    readme.append("| `knowledge/%s` (MADO-R52-1, round 52) | Staged fixture entry: the "
                  "argument-resolution half of the legacy dispatcher table. |" % ENTRY_NAME)
    with open(readme_path, "w") as fh:
        fh.write("\n".join(readme) + "\n")

    # The staged entry.
    entry_lines = [
        "# Staged fixture: how a legacy dispatcher argument becomes a window or a workspace",
        "",
        "This file is a **staged fixture** written by the counter seat to exercise the C2",
        "counter.  It is not the round-52 entry and it is not committed to the lane.",
        "",
        "source: S370 - legacy dispatcher window-argument resolution - the shared helper and "
        "its selector call",
        "source: S371 - legacy dispatcher workspace-argument resolution - the shared helper "
        "and its creation step",
        "source: S372 - legacy movewindow dispatcher argument preparation - the silent suffix",
        "",
        "## Proposition map",
        "",
        "| id | claim | row | pin | quote | support |",
        "|---|---|---|---|---|---|",
    ]
    for pid, claim, rowid, pin, quote, support in PROPS:
        entry_lines.append("| %s | %s | %s | %s | %s | %s |"
                           % (pid, cell(claim), rowid, cell(pin), cell(quote), cell(support)))
    entry_lines += [
        "",
        "## Pin manifest",
        "",
        "| pin | file | row |",
        "|---|---|---|",
        "| Hyprland-legacy-DispatcherTranslator.cpp | src/config/legacy/"
        "DispatcherTranslator.cpp | S370, S371, S372 |",
        "",
        "## The chain",
        "",
    ]
    for pid, claim, rowid, pin, quote, support in PROPS:
        entry_lines.append("%s: %s - %s (%s) %s" % (pid, claim, quote, pin, rowid))
    entry_lines += [
        "",
        "## Limits",
        "",
        "- Nothing was dispatched and nothing was pressed; the mechanism is read from the pin.",
    ]
    entry_path = os.path.join(clone, ENTRY_REL)
    os.makedirs(os.path.dirname(entry_path), exist_ok=True)
    with open(entry_path, "w") as fh:
        fh.write("\n".join(entry_lines) + "\n")

    git(clone, "add", "-A")
    git(clone, "-c", "user.name=fixture", "-c", "user.email=fixture@localhost",
        "commit", "-q", "-m", "fixture: staged C2 entry, registry rows and pin")
    sha = git(clone, "rev-parse", "HEAD").stdout.strip()
    print("fixture=%s rev=%s" % (clone, sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
