#!/usr/bin/env python3
"""Build the ExecC2ExtraMutants positive fixture and score the clause mutants.

Seat-local driver. Reads only the frozen counter (read-only) and the lane's
frozen pins; writes only inside the scratch fixture clone and this seat dir.
"""
import os
import re
import shutil
import subprocess
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "e2289516a9a857f55cda7be635933e89b931c3da"
BASE = "6a1a90528fe533cadee506a9fa3e9d13d15cc41f"
COUNTER = os.path.join(LANE, "quality/counters/c2-r44-gkeep-size-request.py")
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"
LESSON = "corpus/lessons/round-44.md"
README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"

ROWS = """| S298 | Hyprland v0.56.2 xdg shell implementation - how a toplevel size request becomes a scheduled configure - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/XDGShell.cpp | code | A | How CXDGToplevelResource::setSize stores a size and how CXDGSurfaceResource::scheduleConfigure coalesces the send | src/protocols/XDGShell.cpp:354-358 setSize stores m_pendingApply.size and schedules, :629-638 scheduleConfigure arms one deferred configure and reuses the serial | The compositor stages the size in its own state and sends one coalesced configure on the next event-loop turn, so a second request before that turn reuses the serial | mined | 2026-10-26 | 90d | corpus/knowledge/hyprland-gkeep-size-request-r44.md |
| S299 | xdg-shell 1.49 - the toplevel configure event and what a client may do with it - https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/stable/xdg-shell/xdg-shell.xml | spec | A | The protocol text of the xdg_toplevel.configure event: hint semantics, zero, the apply point and the ack | stable/xdg-shell/xdg-shell.xml:1145-1160 the configure event description, :560-592 ack_configure | A configure size is a hint in window-geometry coordinates, zero means the client decides, and the configured state is applied only at the client's ack | mined | 2026-10-26 | 90d | corpus/knowledge/hyprland-gkeep-size-request-r44.md |
| S300 | GTK 4.24.1 wayland toplevel - what the toolkit does with a configure size - https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c | code | A | gdk_wayland_toplevel_handle_configure: the fixed-size decision, the saved-size path and the stored next layout | gdk/wayland/gdktoplevel-wayland.c:606-707 handle_configure, :648-665 the saved-size comment and restore | A maximized, fullscreen or tiled state (or an active resize) marks the size fixed; otherwise a non-zero configure is stored as the next layout size | mined | 2026-10-26 | 90d | corpus/knowledge/hyprland-gkeep-size-request-r44.md |
| S301 | gkeep client ui.py at 133b867 - the full file, what the app declares - https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py | code | A | The app's own window declaration: one default size, one application id, and no size request anywhere in the file | whole file gkeep/ui.py at 133b867, 14639 B sha256:07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a; :449 application_id="org.omarchy.gkeep", :476 window.set_default_size(420, 500) | The client asks for 420x500 and constrains nothing further, so its own layout cannot be distinguished from the compositor's configure by any reported size | mined | 2026-10-26 | 90d | corpus/knowledge/hyprland-gkeep-size-request-r44.md |
"""

README_ROW = ("| `knowledge/hyprland-gkeep-size-request-r44.md` (MADO-R44-1, round 44; assimilation of the gkeep client-side residue, "
              "successor to the staged `gkeep-client-size-request-r12`) | What happens after Hyprland writes the gkeep box: "
              "`sendWindowSize` reporting the animated size and arming the pending-size-ack list, the xdg toplevel `setSize` and the "
              "coalesced `scheduleConfigure`, the xdg-shell 1.49 configure text (a hint; the configured state applies at the ack), the GTK "
              "4.24.1 handler that stores a non-zero configure as the next layout, and gkeep's own `set_default_size(420, 500)` with no "
              "`set_size_request`. |\n")


def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed: %s %s" % (args, p.stdout, p.stderr))
    return p.stdout


def commit(repo, msg):
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=mado-exec", "-c", "user.email=exec@seat.invalid",
        "commit", "-q", "-m", msg)


def build_positive(repo):
    """Write the positive fixture files into repo."""
    entry = open(os.path.join(SEAT, "entry.md")).read()
    lesson = open(os.path.join(SEAT, "lesson.md")).read()
    with open(os.path.join(repo, ENTRY), "w") as fh:
        fh.write(entry)
    with open(os.path.join(repo, LESSON), "w") as fh:
        fh.write(lesson)

    # registry: append the four new rows after the last row of ## Registry,
    # then extend the held S164 row's used-by cell.
    src = open(os.path.join(repo, SOURCES)).read().split("\n")
    start = src.index("## Registry")
    last = max(k for k in range(start, len(src)) if re.match(r"^ {0,3}\|\s*S\d{3,}\s*\|", src[k]))
    src[last + 1:last + 1] = ROWS.rstrip("\n").split("\n")
    for k, line in enumerate(src):
        if line.startswith("| S164 |"):
            cells = line.strip().split("|")[1:-1]
            cells = [c.strip() for c in cells]
            assert len(cells) == 11, len(cells)
            cells[10] = cells[10] + ", " + ENTRY
            src[k] = "| " + " | ".join(cells) + " |"
            break
    else:
        raise SystemExit("S164 row not found")
    with open(os.path.join(repo, SOURCES), "w") as fh:
        fh.write("\n".join(src))

    rm = open(os.path.join(repo, README)).read().split("\n")
    idx = max(k for k, l in enumerate(rm) if l.startswith("| `knowledge/hyprland-gkeep-geometry-r43.md`"))
    rm[idx + 1:idx + 1] = README_ROW.rstrip("\n").split("\n")
    with open(os.path.join(repo, README), "w") as fh:
        fh.write("\n".join(rm))


def score(repo):
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", repo, "--rev", "HEAD",
                        "--base", BASE], capture_output=True, text=True, cwd=LANE)
    out = p.stdout
    last = [l for l in out.splitlines() if l.startswith("PRED-C2-r44:")]
    cl = [l for l in out.splitlines() if "clauses=" in l]
    return p.returncode, (last[-1] if last else out.strip().splitlines()[-1]), (cl[-1] if cl else ""), out


def ed(repo, path, old, new, count=1):
    full = os.path.join(repo, path)
    text = open(full).read()
    n = text.count(old)
    if n != count:
        raise SystemExit("edit target count %d != %d in %s: %r" % (n, count, path, old[:60]))
    open(full, "w").write(text.replace(old, new))


def main():
    repo = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "build"
    if mode == "build":
        build_positive(repo)
        commit(repo, "round-44 C2 positive fixture")
        rc, last, cl, out = score(repo)
        print(last)
        print(cl)
        print("rc=%d" % rc)
        sys.stdout.write(out)
        return


if __name__ == "__main__":
    main()
