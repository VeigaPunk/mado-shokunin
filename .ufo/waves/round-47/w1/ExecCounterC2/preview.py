#!/usr/bin/env python3
"""Preview PRED-C2-r47 against the REAL w1 drafts (entry.md, rows.md, live receipt).

Read-only on the lane: copies the drafts into a scratch clone, rewrites only the receipt
paths (`w1/ScrRows/fetch/` -> the freeze `fetch/`) and adds a synthetic README row and a
receipt in the shape clause f demands, so the clauses that do not depend on the final
integration can be measured now. The tool at REV is the control double (the C1 tool is
not landed yet), so clause f measures the counter's mechanics, not the final instrument.
"""
import os
import re
import shutil
import subprocess
import sys

S = os.environ.get("C2R47_WORK") or "/fast/scratch/hyaku/mado-r47/ExecCounterC2"
D = os.path.join(S, "preview")
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W1 = os.path.join(LANE, ".ufo/waves/round-47/w1")
BASE = "60edb66e2f1cb90acc6e9442fc93ded0ca42d750"
FETCH = ".ufo/waves/round-47/fetch/"
ENTRY = "corpus/knowledge/xdg-terminal-selection-r47.md"
C = os.path.join(W1, "ExecCounterC2/c2-r47-terminal-entry.py")


def run(*args, cwd=None, check=True):
    p = subprocess.run(args, cwd=cwd, capture_output=True)
    if check and p.returncode != 0:
        sys.exit("FAILED %s: %s" % (" ".join(args), p.stderr.decode()[:2000]))
    return p


def main():
    run("rm", "-rf", D)
    run("git", "clone", "-q", "--shared", LANE, D)
    run("git", "-C", D, "checkout", "-q", BASE)
    top = run("git", "-C", D, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(D):
        sys.exit("clone toplevel %s != %s" % (top, D))
    run("git", "-C", D, "config", "user.email", "control@c2r47.invalid")
    run("git", "-C", D, "config", "user.name", "C2R47 preview")
    os.makedirs(os.path.join(D, FETCH), exist_ok=True)
    os.makedirs(os.path.join(D, ".ufo/waves/round-47/receipts"), exist_ok=True)
    os.makedirs(os.path.join(D, "tools"), exist_ok=True)
    # pins: the row seat's fetched bytes, plus the entry seat's README copy name
    for root, _dirs, files in os.walk(os.path.join(W1, "ScrRows/fetch")):
        for f in files:
            src = os.path.join(root, f)
            rel = os.path.relpath(src, os.path.join(W1, "ScrRows/fetch"))
            dst = os.path.join(D, FETCH, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
    shutil.copyfile(os.path.join(W1, "ScrEntry/README-v0.14.3.md"),
                    os.path.join(D, FETCH, "README-v0.14.3.md"))
    # entry
    with open(os.path.join(W1, "ScrEntry/entry.md"), encoding="utf-8") as fh:
        entry = fh.read()
    with open(os.path.join(D, ENTRY), "w", encoding="utf-8") as fh:
        fh.write(entry)
    # rows: the markdown table lines, receipts rewritten to the freeze path
    with open(os.path.join(W1, "ScrRows/rows.md"), encoding="utf-8") as fh:
        rows = [l for l in fh.read().split("\n") if re.match(r"^\| S3\d\d \|", l)]
    rows = [l.replace(".ufo/waves/round-47/w1/ScrRows/fetch/",
                      ".ufo/waves/round-47/fetch/") for l in rows]
    bad = [n for n, l in enumerate(rows, 1) if len(l.strip().strip("|").split("|")) != 11]
    if bad:
        sys.exit("rows with != 11 cells: %s" % bad)
    src = os.path.join(D, "corpus/SOURCES.md")
    lines = open(src, encoding="utf-8").read().split("\n")
    out, done = [], False
    for l in lines:
        out.append(l)
        if not done and re.match(r"^ {0,3}\|\s*S325\s*\|", l):
            out.extend(rows)
            done = True
    if not done:
        sys.exit("S325 not found")
    with open(src, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    # README row naming every new row
    readme_row = ("| `knowledge/xdg-terminal-selection-r47.md` (MADO-R47-1, round 47; "
                  "terminal-selection plane) | The executed selection chain of "
                  "xdg-terminal-exec 0.14.3, the host's user override and the live cold-cache "
                  "verdict. | [Source and recheck](knowledge/xdg-terminal-selection-r47.md): "
                  "§§1-3; Sources S326-S338. |")
    rp = os.path.join(D, "corpus/README.md")
    lines = open(rp, encoding="utf-8").read().split("\n")
    out, done = [], False
    for l in lines:
        out.append(l)
        if not done and l.startswith("| `knowledge/hyprland-input-devices-r46.md`"):
            out.append(readme_row)
            done = True
    if not done:
        sys.exit("README anchor not found")
    with open(rp, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    # receipt in the clause-f shape (from the live seat's observation)
    obs = ("Alacritty.desktop\n"
           "/home/vgpnk/.local/share/applications/Alacritty.desktop\n"
           "alacritty\n")
    with open(os.path.join(D, ".ufo/waves/round-47/receipts/live-observed.txt"), "w") as fh:
        fh.write(obs)
    live = open(os.path.join(W1, "ExecLive/receipts/live-host.txt"), encoding="utf-8").read()
    rec = (live + "\nXDG_CONFIG_HOME=/home/vgpnk/.config\n"
           "XDG_CONFIG_DIRS=/etc/xdg\n"
           "XDG_DATA_HOME=/home/vgpnk/.local/share\n"
           "XDG_DATA_DIRS=/usr/local/share:/usr/share\n"
           "observed=.ufo/waves/round-47/receipts/live-observed.txt\n"
           "MADO_TERM: selected=Alacritty.desktop "
           "path=/home/vgpnk/.local/share/applications/Alacritty.desktop verdict=OK\n")
    with open(os.path.join(D, ".ufo/waves/round-47/receipts/live-host.txt"), "w") as fh:
        fh.write(rec)
    # the preview's live section: point the entry's [UNK] line at that receipt
    with open(os.path.join(D, ENTRY), "a", encoding="utf-8") as fh:
        fh.write("\n## Live receipt (preview wiring)\n\n"
                 "The cold-cache run above is `.ufo/waves/round-47/receipts/live-host.txt`; "
                 "its observed print output is `.ufo/waves/round-47/receipts/live-observed.txt` "
                 "and the round-17 [UNK] at corpus/knowledge/terminal-route-r17.md:144-145 is "
                 "answered by the printed user override path.\n")
    # tool double (C1 not landed yet)
    shutil.copyfile(os.path.join(S, "ctl/tools/mado-terminal.py"),
                    os.path.join(D, "tools/mado-terminal.py"))
    run("git", "-C", D, "add", "-A")
    run("git", "-C", D, "commit", "-q", "-m", "preview: real w1 drafts")
    rev = run("git", "-C", D, "rev-parse", "HEAD").stdout.decode().strip()
    p = subprocess.run([sys.executable, C, "--repo", D, "--rev", rev], capture_output=True)
    out = p.stdout.decode() + p.stderr.decode()
    with open(os.path.join(W1, "ExecCounterC2/receipts/preview-real-drafts.txt"),
              "w", encoding="utf-8") as fh:
        fh.write("$ python3 c2-r47-terminal-entry.py --repo <preview> --rev %s\n" % rev)
        fh.write(out)
        fh.write("exit=%d\n" % p.returncode)
    print(out[-4000:])
    print("exit=%d rev=%s" % (p.returncode, rev))


if __name__ == "__main__":
    main()
