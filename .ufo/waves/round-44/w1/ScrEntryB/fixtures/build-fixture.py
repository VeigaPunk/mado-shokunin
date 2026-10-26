#!/usr/bin/env python3
"""Build a synthetic round-44 integration in a throwaway clone and run PRED-C2-r44."""
import json, os, subprocess, sys, textwrap

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = "/fast/scratch/hyaku/mado-r44/ScrEntryB"
D = os.path.join(S, "lane")
REV = "e2289516a9a857f55cda7be635933e89b931c3da"
BASE = "6a1a90528fe533cadee506a9fa3e9d13d15cc41f"
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"
SEAT = os.path.join(LANE, ".ufo/waves/round-44/w1/ScrEntryB")
FETCH = ".ufo/waves/round-44/fetch/"

def run(*a, **kw):
    p = subprocess.run(a, capture_output=True, text=True, **kw)
    if p.returncode:
        print("FAILED: %s\n%s\n%s" % (" ".join(a), p.stdout, p.stderr))
        sys.exit(1)
    return p.stdout

subprocess.run(["rm", "-rf", D], check=True)
run("git", "clone", "-q", "--shared", LANE, D)
run("git", "-C", D, "checkout", "-q", REV)
top = run("git", "-C", D, "rev-parse", "--show-toplevel").strip()
assert os.path.realpath(top) == os.path.realpath(D), top
run("git", "-C", D, "config", "user.email", "seat@scratch.invalid")
run("git", "-C", D, "config", "user.name", "ScrEntryB scratch")

# entry
os.makedirs(os.path.dirname(os.path.join(D, ENTRY)), exist_ok=True)
with open(os.path.join(SEAT, "hyprland-gkeep-size-request-r44.md")) as f:
    entry = f.read()
open(os.path.join(D, ENTRY), "w").write(entry)

# quotes
quotes = {}
with open(os.path.join(SEAT, "quotes.tsv")) as f:
    for row in f.read().splitlines()[1:]:
        if row.strip():
            i, base, sha, ln, words, q = row.split("\t")
            quotes[i] = (base, sha, ln, q)

URL = {
 "S298": "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/XDGShell.cpp",
 "S299": "https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/stable/xdg-shell/xdg-shell.xml",
 "S300": "https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c",
 "S301": "https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py",
}
DESC = {
 "S298": "hyprwm/Hyprland src/protocols/XDGShell.cpp @ efb5099 (v0.56.2)",
 "S299": "wayland-protocols 1.49 stable/xdg-shell/xdg-shell.xml",
 "S300": "GTK 4.24.1 gdk/wayland/gdktoplevel-wayland.c",
 "S301": "gkeep 133b867 gkeep/ui.py (full file)",
}
TEACH = {
 "S298": "the xdg toplevel size ask: record the size, schedule the configure, hand back a serial",
 "S299": "the configure width and height are a hint; zero means the client decides",
 "S300": "GTK adopts the configured size into its next layout and marks it fixed under maximize/fullscreen/tile",
 "S301": "gkeep declares one default size and no size request; its application id",
}
REG = os.path.join(D, "corpus/SOURCES.md")
reg = open(REG).read()
rows = []
for i in sorted(URL):
    rows.append("| %s | %s — %s | code | A | %s | %s | %s | mined | 2026-10-26 | 30d | %s |"
                % (i, DESC[i], URL[i], TEACH[i], quotes[i][0] + " @ " + URL[i],
                   "the size request after the box: what the client may and does do with it",
                   ENTRY))
lines = reg.split("\n")
for k, l in enumerate(lines):
    if l.startswith("| S164 |"):
        cells = l.split("|")
        cells[11] = cells[11].rstrip() + ", " + ENTRY + " "
        lines[k] = "|".join(cells)
reg = "\n".join(lines)
anchor = "| S297 |"
k = reg.index(anchor)
end = reg.index("\n", k) + 1
reg = reg[:end] + "\n".join(rows) + "\n" + reg[end:]
open(REG, "w").write(reg)

# lesson
gate = ["# round 44 synthetic gate (ScrEntryB verification fixture, not lane data)", "",
        "## Gate", ""]
for i in sorted(quotes):
    gate.append('GATE %s receipt=%s%s sha256=%s quote="%s"'
                % (i, FETCH, quotes[i][0], quotes[i][1], quotes[i][3]))
gate.append("")
gate.append("ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md as " + ENTRY)
gate.append("REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-rendered-geometry-chain-r9.md reason=its fetchClass chain stops at the reported class and does not reach the configure, the ack or the client handler; flip if a pinned source ties fetchClass to a size")
gate.append("REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-geometry-never-recorded-r15.md reason=its journal route is not a size source for this chain until a journal read reports a gkeep geometry; flip if such a read exists")
gate.append("")
os.makedirs(os.path.join(D, "corpus/lessons"), exist_ok=True)
open(os.path.join(D, "corpus/lessons/round-44.md"), "w").write("\n".join(gate))

# readme
RD = os.path.join(D, "corpus/README.md")
rd = open(RD).read().split("\n")
idx = max(k for k, l in enumerate(rd) if l.startswith("| `knowledge/"))
rd.insert(idx + 1, "| `knowledge/hyprland-gkeep-size-request-r44.md` (MADO-R44-1, round 44; assimilation of the gkeep size-request theme) | What establishes the size a gkeep window renders: the configure, the ack, the app's declarations |")
open(RD, "w").write("\n".join(rd))

run("git", "-C", D, "add", "-A")
run("git", "-C", D, "commit", "-q", "-m", "synthetic round-44 integration fixture")
new = run("git", "-C", D, "rev-parse", "HEAD").strip()
print("scratch rev", new)

p = subprocess.run(["python3", "-I", os.path.join(LANE, "quality/counters/c2-r44-gkeep-size-request.py"),
                    "--repo", D, "--rev", new, "--base", BASE],
                   capture_output=True, text=True)
print(p.stdout)
print(p.stderr[-2000:])
print("counter exit", p.returncode)
open(os.path.join(S, "scratch-counter.txt"), "w").write(
    "scratch clone %s\nrev %s\nbase %s\n\n%s\n%s\nexit=%d\n"
    % (D, new, BASE, p.stdout, p.stderr, p.returncode))
