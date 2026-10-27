#!/usr/bin/env python3
"""Check the block form of the proposition map and the setup-error paths of the draft C2
counter.

The block form is the alternative grammar the counter documents: a proposition id on its own
line, then `claim:` / `row:` / `pin:` / `quote:` / `support:` lines.  A counter that only
accepts the table form would reject a conforming entry for a formatting reason, so the block
form is exercised here on its own fixture.

Usage:
    python3 blockform-check.py --lane <lane> --work <scratch> --counter <counter path>
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

BASE = "85d57a818c3707397e21c840b6498b105ba798aa"
ENTRY_REL = "corpus/knowledge/hyprland-dispatcher-action-effects-r52.md"
REVISION = "efb50993780079460b0cbed1363e2166a2de1d9f"
FETCH_ROOT = ".ufo/waves/round-52/fetch"

BLOCK_PROPS = [
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


def run_counter(counter, repo, rev, work, extra=()):
    env = dict(os.environ)
    env["TMPDIR"] = work
    p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev,
                        "--entry", ENTRY_REL, "--work", os.path.join(work, "w"), *extra],
                       capture_output=True, text=True, env=env)
    return p.returncode, p.stdout + p.stderr


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--counter", required=True)
    args = ap.parse_args(argv)

    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    clone = os.path.join(work, "blockform")
    if os.path.exists(clone):
        shutil.rmtree(clone)
    subprocess.run(["git", "clone", "--no-hardlinks", "--quiet", args.lane, clone], check=True)
    assert_toplevel(clone, clone)
    git(clone, "checkout", "--quiet", BASE)
    git(clone, "checkout", "-q", "-b", "fixture/blockform")
    assert_toplevel(clone, clone)

    src_pin = os.path.join(args.lane, ".ufo/waves/round-51/fetch/"
                           "Hyprland-legacy-DispatcherTranslator.cpp")
    os.makedirs(os.path.join(clone, FETCH_ROOT), exist_ok=True)
    shutil.copyfile(src_pin, os.path.join(clone, FETCH_ROOT,
                                          "Hyprland-legacy-DispatcherTranslator.cpp"))

    reg_path = os.path.join(clone, "corpus/SOURCES.md")
    lines = read(reg_path).splitlines()
    last = max(i for i, l in enumerate(lines) if re.match(r"^\| S\d{3,} ", l))
    rows = []
    for rowid, scope, teaches in (
            ("S370", "how a dispatcher argument naming a window becomes a window: the "
                     "empty/active shortcut and the selector call",
             "the shared helper resolves a window argument through the view-state selector, or "
             "takes the focused window when the argument is empty or `active`"),
            ("S371", "how a dispatcher argument naming a workspace becomes a workspace: the "
                     "id/name parse and the creation of an absent workspace",
             "the shared helper parses a workspace argument into an id and a name and creates "
             "the workspace when the compositor holds none with that id")):
        rows.append("| %s | Hyprland 0.56.2 legacy dispatcher argument resolution - "
                    "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/config/legacy/"
                    "DispatcherTranslator.cpp | code | A | %s | "
                    "Hyprland-legacy-DispatcherTranslator.cpp:1 @ %s; pin %s/Hyprland-legacy-"
                    "DispatcherTranslator.cpp | %s | mined | 2026-10-27 | on-release | %s |"
                    % (rowid, REVISION, scope, REVISION, FETCH_ROOT, teaches, ENTRY_REL))
    lines[last + 1:last + 1] = rows
    write(reg_path, "\n".join(lines) + "\n")

    readme_path = os.path.join(clone, "corpus/README.md")
    write(readme_path, read(readme_path).rstrip("\n")
          + "\n| `knowledge/hyprland-dispatcher-action-effects-r52.md` (MADO-R52-1, round 52) | "
            "Block-form fixture entry. |\n")

    entry = [
        "# Block-form fixture: the argument-resolution half of the legacy dispatcher table",
        "",
        "source: S370 - legacy dispatcher window-argument resolution",
        "source: S371 - legacy dispatcher workspace-argument resolution",
        "",
        "## Proposition map",
        "",
    ]
    for pid, claim, rowid, pin, quote, support in BLOCK_PROPS:
        entry += [pid,
                  "claim: %s" % claim,
                  "row: %s" % rowid,
                  "pin: %s" % pin,
                  "quote: %s" % quote,
                  "support: %s" % support,
                  ""]
    entry += ["## Pin manifest", "",
              "| pin | file | row |",
              "|---|---|---|",
              "| Hyprland-legacy-DispatcherTranslator.cpp | src/config/legacy/"
              "DispatcherTranslator.cpp | S370, S371 |",
              "", "## The chain", ""]
    for pid, claim, rowid, pin, quote, support in BLOCK_PROPS:
        entry.append("%s: %s - %s (%s) %s" % (pid, claim, quote, pin, rowid))
    entry += ["", "## Limits", "",
              "- Nothing was dispatched; the mechanism is read from the pin."]
    entry_path = os.path.join(clone, ENTRY_REL)
    os.makedirs(os.path.dirname(entry_path), exist_ok=True)
    write(entry_path, "\n".join(entry) + "\n")

    git(clone, "add", "-A")
    git(clone, "-c", "user.name=fixture", "-c", "user.email=fixture@localhost",
        "commit", "-q", "-m", "fixture: block-form C2 entry")
    rev = git(clone, "rev-parse", "HEAD").stdout.strip()

    failures = 0
    rc, out = run_counter(args.counter, clone, rev, work)
    ok = rc == 0 and "verdict=TARGET_MET" in out
    print("BLOCKFORM: green rc=%d verdict_met=%s" % (rc, ok))
    for l in out.splitlines():
        print("    %s" % l)
    if not ok:
        failures += 1

    # Setup errors: each must exit 2 with a setup-error line, not a silent pass.
    rc, out = run_counter(args.counter, clone, "nosuchrev", work)
    ok = rc == 2 and "setup error" in out
    print("BLOCKFORM: bad_rev rc=%d setup_error=%s" % (rc, ok))
    if not ok:
        failures += 1

    rc, out = run_counter(args.counter, "/nonexistent/repo", rev, work)
    ok = rc == 2 and "setup error" in out
    print("BLOCKFORM: bad_repo rc=%d setup_error=%s" % (rc, ok))
    if not ok:
        failures += 1

    rc, out = run_counter(args.counter, clone, rev, work,
                          extra=["--work", os.path.join(clone, "inside")])
    ok = rc == 2 and "scratch dir inside the scored repository" in out
    print("BLOCKFORM: work_inside_repo rc=%d refused=%s" % (rc, ok))
    if not ok:
        failures += 1

    # The round-51 entry slug must be refused as the target.
    rc, out = run_counter(args.counter, clone, rev, work,
                          extra=["--entry",
                                 "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md"])
    ok = rc == 2 and "must differ from the round-51 entry" in out
    print("BLOCKFORM: r51_slug_refused rc=%d refused=%s" % (rc, ok))
    if not ok:
        failures += 1

    shutil.rmtree(clone, ignore_errors=True)
    print("BLOCKFORM: failures=%d" % failures)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
