#!/usr/bin/env python3
"""Build the tightened copy of PRED-C2-r44 (T1 pin digests for every id, T2 pin URLs,
T3 census/prose numeric agreement) and score every fixture with it.  The frozen counter
in the lane is only read."""
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = LANE + "/.ufo/waves/round-44/w1/CritC2Cheat"
SRC = LANE + "/quality/counters/c2-r44-gkeep-size-request.py"
OUT = SEAT + "/c2-r44-tightened.py"
BASE = "6a1a90528fe533cadee506a9fa3e9d13d15cc41f"

URLS = '''PINS_URL = {
    "Hyprland-Window.cpp": "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp",
    "Hyprland-XDGShell.cpp": "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/XDGShell.cpp",
    "gdktoplevel-wayland.c": "https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c",
    "gkeep-ui.py": "https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py",
    "xdg-shell.xml": "https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/stable/xdg-shell/xdg-shell.xml",
}
'''

T1_OLD = '''            pin_ok = True
            if i in new_ids:
                pin_ok = PINS.get(os.path.basename(path)) == digest \\
                    and path == FETCH + os.path.basename(path)'''
T1_NEW = '''            pin_ok = PINS.get(os.path.basename(path)) in (None, digest) \\
                and (os.path.basename(path) not in PINS
                     or path == FETCH + os.path.basename(path))'''

T2_OLD = '''    cl["e"] = int(e_ok and bool(new_ids))'''
T2_NEW = '''    for i in ids:
        gl_ = gates.get(i, [])
        row_ = reg_rev.get(i, [])
        if len(gl_) == 1 and row_ and len(row_[0]) == 11:
            loc_ = row_[0][1].split()[-1].split("#")[0] if row_[0][1].split() else ""
            pin_url = PINS_URL.get(os.path.basename(gl_[0][0]))
            if pin_url is not None and pin_url.split("#")[0] != loc_:
                e_ok = False
                print("%s %s clause=e+ id=%s location=%s pin=%s" % (
                    PRED, name, i, loc_, pin_url))
    # T4: a new row's anchor must name the receipt it is gated on and stay inside it
    for i in new_ids:
        row_ = reg_rev.get(i, [])
        gl_ = gates.get(i, [])
        if not row_ or len(row_[0]) != 11 or len(gl_) != 1 or i not in receipts_raw:
            e_ok = False
            continue
        rb_ = os.path.basename(gl_[0][0])
        nlines_ = len(receipts_raw[i].decode("utf-8", "replace").splitlines())
        anchor_ = row_[0][5]
        rng = re.findall(r"%s:(\d+)(?:-(\d+))?" % re.escape(rb_), anchor_)
        if not rng or any(int(b or a) > nlines_ for a, b in rng):
            e_ok = False
            print("%s %s clause=e/4 id=%s anchor=%s receipt_lines=%d" % (
                PRED, name, i, anchor_[:70], nlines_))
    cl["e"] = int(e_ok and bool(new_ids))'''

T3_OLD = '''    h_ok, census_lines = host_census(new_ids, reg_rev, gates, receipts_raw, lines)
    cl["h"] = int(h_ok)
    census_lines = set(census_lines)

    entry_lines = [re.sub(r"\\s+", " ", l) for l in lines
                   if l not in census_lines
                   and not l.startswith("gkeep client ")
                   and not l.startswith("hyprland sendWindowSize ")]'''
T3_NEW = '''    h_ok, census_lines = host_census(new_ids, reg_rev, gates, receipts_raw, lines)
    census_lines = set(census_lines)

    entry_lines = [re.sub(r"\\s+", " ", l) for l in lines
                   if l not in census_lines
                   and not l.startswith("gkeep client ")
                   and not l.startswith("hyprland sendWindowSize ")]
    if h_ok:
        joined = "\\n".join(census_lines)
        m_ui = re.search(r"default_size=(\\d+)x(\\d+) size_request_calls=(\\d+)", joined)
        m_hy = re.search(r"xdg_setSize=(\\d+) x11_configure=(\\d+)", joined)
        if not m_ui or not m_hy:
            h_ok = False
        else:
            W0, H0, N0 = m_ui.group(1), m_ui.group(2), int(m_ui.group(3))
            X0, Y0 = int(m_hy.group(1)), int(m_hy.group(2))
            for l in entry_lines:
                if N0 == 0 and re.search(r"set_size_request\\s*\\(", l):
                    h_ok = False
                    print("%s %s clause=h prose calls set_size_request: %s" % (PRED, name, l[:80]))
                for w, h in re.findall(r"set_default_size\\(\\s*(\\d+)\\s*,\\s*(\\d+)\\s*\\)", l):
                    if (w, h) != (W0, H0):
                        h_ok = False
                        print("%s %s clause=h prose default size %sx%s != %sx%s" % (
                            PRED, name, w, h, W0, H0))
                for v in re.findall(r"xdg_setSize=(\\d+)", l):
                    if int(v) != X0:
                        h_ok = False
                        print("%s %s clause=h prose xdg_setSize=%s != %d" % (PRED, name, v, X0))
                for v in re.findall(r"x11_configure=(\\d+)", l):
                    if int(v) != Y0:
                        h_ok = False
                        print("%s %s clause=h prose x11_configure=%s != %d" % (PRED, name, v, Y0))
    cl["h"] = int(h_ok)'''


def main():
    text = open(SRC, encoding="utf-8").read()
    for label, old, new in (("T1", T1_OLD, T1_NEW), ("T2", T2_OLD, T2_NEW),
                            ("T3", T3_OLD, T3_NEW)):
        assert text.count(old) == 1, (label, text.count(old))
        text = text.replace(old, new)
    anchor = 'STAGED = {'
    assert text.count(anchor) == 1
    text = text.replace(anchor, URLS + anchor, 1)
    text = text.replace('"""\nimport argparse',
                        '--- CritC2Cheat tightenings T1 (pin digest for every cited id), T2 (pin URL '
                        'for every pin-named receipt), T3 (census numbers not contradicted by the entry '
                        'prose), T4 (a new row's anchor names its receipt and stays inside it).  Frozen counter untouched; this is a copy.\n"""\nimport argparse', 1)
    open(OUT, "w", encoding="utf-8").write(text)
    subprocess.run([sys.executable, "-I", "-c", "compile(open(%r).read(), %r, 'exec')"
                    % (OUT, OUT)], check=True)

    fixtures = [l.split() for l in open(SEAT + "/fixtures.txt").read().splitlines() if l.strip()]
    out = []
    for name, d in fixtures:
        p = subprocess.run([sys.executable, "-I", OUT, "--repo", d, "--rev", "HEAD",
                            "--base", BASE], capture_output=True, text=True)
        block = "### %s rc=%d\n%s" % (name, p.returncode, p.stdout + p.stderr)
        out.append(block)
        with open(os.path.join(SEAT, "tight-" + name + ".txt"), "w") as fh:
            fh.write(block)
    open(SEAT + "/tight-all.txt", "w").write("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
