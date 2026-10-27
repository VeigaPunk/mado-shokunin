#!/usr/bin/env python3
"""Build the C1 fixture: round-49 candidate artifacts committed at the round-50 paths.

Two commits on a scratch clone of the lane at BASE 8ae47b95:
  c1  artifacts at round-50 paths (fetch pins, receipts, entry, registry rows)
  c2  the round-50 index row (corpus/README.md) and the round-50 lesson Gate
Nothing outside the scratch clone is written.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "8ae47b957034ae21012bbf09173cca2c48be345e"
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fx")
R49 = os.path.join(LANE, ".ufo/waves/round-49")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def run(*args, **kw):
    p = subprocess.run(args, capture_output=True, env=ENV, **kw)
    if p.returncode != 0:
        sys.exit("FAILED %s rc=%d\n%s\n%s" % (args, p.returncode,
                                              p.stdout.decode(), p.stderr.decode()))
    return p.stdout.decode()


def repo(*args):
    return run("git", "-C", D, *args)


def repoint(text):
    text = text.replace("round-49", "round-50")
    text = re.sub(r"\br49\b", "r50", text)
    text = text.replace("Round: 49", "Round: 50")
    return text


def write(path, text):
    full = os.path.join(D, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def main():
    if os.path.exists(D):
        shutil.rmtree(D)
    run("git", "clone", "-q", "--shared", LANE, D)
    repo("checkout", "-q", "--detach", BASE)
    top = repo("rev-parse", "--show-toplevel").strip()
    assert os.path.realpath(top) == os.path.realpath(D), (top, D)
    repo("config", "user.email", "fixture@mado.local")
    repo("config", "user.name", "mado fixture")
    repo("config", "commit.gpgsign", "false")

    # ---- c1: artifacts at the round-50 paths --------------------------------
    for name in sorted(os.listdir(os.path.join(R49, "fetch"))):
        new = name.replace("-r49", "-r50")
        dst = os.path.join(D, ".ufo/waves/round-50/fetch", new)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(os.path.join(R49, "fetch", name), dst)
    for name in ("binds-live-r49.txt", "how-to-type-slash-br-r49.txt"):
        new = name.replace("-r49", "-r50")
        dst = os.path.join(D, ".ufo/waves/round-50/receipts", new)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(os.path.join(R49, "receipts", name), dst)

    entry = repoint(open(os.path.join(R49, "candidate",
                                      "hyprland-bind-key-match-r49.md")).read())
    entry = entry.replace("hyprland-bind-key-match-r49.md",
                          "hyprland-bind-key-match-r50.md")
    write("corpus/knowledge/hyprland-bind-key-match-r50.md", entry)

    rows = repoint(open(os.path.join(R49, "candidate", "rows.md")).read()).rstrip("\n")
    rows = rows.replace("hyprland-bind-key-match-r49.md",
                        "hyprland-bind-key-match-r50.md")
    src = open(os.path.join(D, "corpus/SOURCES.md")).read()
    marker = "\n## Paths"
    assert src.count(marker) == 1
    src = src.replace(marker, "\n" + rows + "\n" + marker, 1)
    write("corpus/SOURCES.md", src)

    repo("add", "-A")
    repo("commit", "-q", "-m", "fixture c1: r49 candidate artifacts at round-50 paths")
    c1 = repo("rev-parse", "HEAD").strip()

    # ---- c2: index row + round-50 lesson gate -------------------------------
    readme = open(os.path.join(D, "corpus/README.md")).read().splitlines()
    ids = "S352-S363"
    row = ("| `knowledge/hyprland-bind-key-match-r50.md` (M50-1, round 50) | Bind key "
           "matching on Hyprland 0.56.2 at `efb50993`: which keysym the key field is "
           "compared against, which xkb state it is read from, and how the modifier mask "
           "compares, grounded on commit-pinned sources and a read-only `hyprctl binds -j` "
           "capture. | [Source and recheck](knowledge/hyprland-bind-key-match-r50.md): "
           "steps 1-17, rows " + ids + ". |")
    last = max(k for k, l in enumerate(readme) if l.startswith("| `knowledge/"))
    readme.insert(last + 1, row)
    write("corpus/README.md", "\n".join(readme) + "\n")

    gate = ["# mado round 50 - lessons", "", "## Gate", ""]
    for n in range(352, 364):
        gate.append("- **S%d admit** - Hyprland bind-key-match source, opened 2026-10-27."
                    % n)
    gate.append("")
    write("corpus/lessons/round-50.md", "\n".join(gate))

    repo("add", "-A")
    repo("commit", "-q", "-m", "fixture c2: round-50 index row and lesson gate")
    c2 = repo("rev-parse", "HEAD").strip()

    print("c1=%s" % c1)
    print("c2=%s" % c2)
    for rev in (c1, c2):
        listing = repo("ls-tree", "-r", "--name-only", rev).splitlines()
        print("%s files=%d entry=%d fetch=%d receipts=%d" % (
            rev[:8], len(listing),
            sum(1 for p in listing if "knowledge/hyprland-bind-key-match-r50.md" in p),
            sum(1 for p in listing if p.startswith(".ufo/waves/round-50/fetch/")),
            sum(1 for p in listing if p.startswith(".ufo/waves/round-50/receipts/"))))


if __name__ == "__main__":
    main()
