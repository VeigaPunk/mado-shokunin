#!/usr/bin/env python3
"""Materialise each control bundle as one commit in a scratch clone of the lane.

Usage: drive.py [control ...]        # default: every control dir
Prints one JSON record per control to stdout and writes revs.json in the seat dir.

The clone is `git clone -q --shared` from the lane into
/fast/scratch/hyaku/mado-r49/ExecControlsC2/work/<control>/repo, checked out detached at
the round base. Every path written is inside that clone. No lane, fleet or home path is
touched; HOME and XDG_* are pointed at the control's scratch dir for the whole run.
"""
import json
import os
import shutil
import subprocess
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "03e4ae76aff7a4be59cb69970dd553baa319695a"
SCRATCH = "/fast/scratch/hyaku/mado-r49/ExecControlsC2/work"
CTL = os.path.join(SEAT, "controls")
ENTRY = "corpus/knowledge/hyprland-bind-key-match-r49.md"
ROWS = ("S352", "S353", "S354", "S355")


def run(args, cwd=None, env=None, check=True):
    p = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit("%s -> rc=%d\n%s\n%s" % (args, p.returncode, p.stdout[-2000:], p.stderr[-2000:]))
    return p


def read(p):
    return open(p).read()


def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(text)


def apply_bundle(repo, ctl):
    base = os.path.join(CTL, "00-base-golden")
    entry_src = os.path.join(ctl, "entry.md")
    if os.path.exists(entry_src):
        write(os.path.join(repo, ENTRY), read(entry_src))
    # registry rows, inside the Registry section (before the next ## heading)
    rows_src = os.path.join(ctl, "rows-append.txt")
    if not os.path.exists(rows_src):
        rows_src = os.path.join(base, "rows.txt")
    src = read(os.path.join(repo, "corpus/SOURCES.md")).splitlines(True)
    cut = next(i for i, l in enumerate(src) if l.startswith("## Paths"))
    src[cut:cut] = ["\n", read(rows_src).rstrip("\n") + "\n"]
    write(os.path.join(repo, "corpus/SOURCES.md"), "".join(src))
    # README index row after the round-48 knowledge row
    readme = read(os.path.join(repo, "corpus/README.md")).splitlines(True)
    at = next(i for i, l in enumerate(readme) if "knowledge/xkb-keymap-compile-r48.md" in l and l.startswith("|"))
    readme[at + 1:at + 1] = [read(os.path.join(base, "readme-row.txt"))]
    write(os.path.join(repo, "corpus/README.md"), "".join(readme))
    # receipt, committed twice: cited copy and pin copy
    receipt_src = os.path.join(ctl, "receipt.txt")
    if not os.path.exists(receipt_src):
        receipt_src = os.path.join(base, "receipt.txt")
    receipt = read(receipt_src)
    write(os.path.join(repo, ".ufo/waves/round-49/receipts/live-binds-r49.txt"), receipt)
    write(os.path.join(repo, ".ufo/waves/round-49/fetch/live-binds-r49.txt"), receipt)
    # lesson Gate rows (a control may extend them)
    lesson_src = os.path.join(ctl, "lesson-gate.md")
    if not os.path.exists(lesson_src):
        lesson_src = os.path.join(base, "lesson-gate.md")
    write(os.path.join(repo, "corpus/lessons/round-49.md"), read(lesson_src))
    # pins: the three round-49 pins, then the control's overrides
    for pin in ("Hyprland-KeybindManager.cpp", "libxkbcommon-src-keysym.c"):
        shutil.copyfile(os.path.join(SEAT, "pins", pin),
                        os.path.join(repo, ".ufo/waves/round-49/fetch", pin))
    pins = os.path.join(ctl, "pins")
    if os.path.isdir(pins):
        for pin in os.listdir(pins):
            shutil.copyfile(os.path.join(pins, pin),
                            os.path.join(repo, ".ufo/waves/round-49/fetch", pin))
    # the held S319 pin, for the control that re-registers it
    shutil.copyfile(os.path.join(SEAT, "pins", "Hyprland-IKeyboard.cpp"),
                    os.path.join(repo, ".ufo/waves/round-49/fetch/Hyprland-IKeyboard.cpp"))


def drive(name):
    ctl = os.path.join(CTL, name)
    root = os.path.join(SCRATCH, name)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    home = os.path.join(root, "home")
    os.makedirs(home)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    for var in ("XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME"):
        env[var] = os.path.join(home, var.lower())
        os.makedirs(env[var], exist_ok=True)
    env["HOME"] = home
    env["TMPDIR"] = os.path.join(root, "tmp")
    os.makedirs(env["TMPDIR"], exist_ok=True)
    repo = os.path.join(root, "repo")
    run(["git", "clone", "-q", "--shared", LANE, repo], env=env)
    run(["git", "-C", repo, "checkout", "-q", BASE], env=env)
    top = run(["git", "-C", repo, "rev-parse", "--show-toplevel"], env=env).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise SystemExit("fixture toplevel %r != %r" % (top, repo))
    if name == "01-do-nothing":
        run(["git", "-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@local",
             "commit", "-q", "--allow-empty", "-m", "control do-nothing"], env=env)
    else:
        apply_bundle(repo, ctl)
        run(["git", "-C", repo, "add", "-A"], env=env)
        run(["git", "-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@local",
             "commit", "-q", "-m", "control %s" % name], env=env)
    rev = run(["git", "-C", repo, "rev-parse", "HEAD"], env=env).stdout.strip()
    return dict(control=name, repo=repo, rev=rev, base=BASE)


def main():
    names = sys.argv[1:] or sorted(os.listdir(CTL))
    recs = []
    for n in names:
        rec = drive(n)
        recs.append(rec)
        print(json.dumps(rec))
    out = os.path.join(SEAT, "revs.json")
    old = {}
    if os.path.exists(out):
        old = {r["control"]: r for r in json.load(open(out))}
    old.update({r["control"]: r for r in recs})
    json.dump([old[k] for k in sorted(old)], open(out, "w"), indent=1)


if __name__ == "__main__":
    main()
