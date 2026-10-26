#!/usr/bin/env python3
"""CritC2Cheat: build forged C2 entry+registry+lesson commits in throwaway clones and score
them with the frozen PRED-C2-r44 counter (and with a patched copy that carries tightenings
T1-T3).  Nothing in the lane is written except this seat's own directory."""
import hashlib
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FREEZE = "e2289516a9a857f55cda7be635933e89b931c3da"
BASE = "6a1a90528fe533cadee506a9fa3e9d13d15cc41f"
SEAT = LANE + "/.ufo/waves/round-44/w1/CritC2Cheat"
SCRATCH = "/fast/scratch/hyaku/mado-r44/CritC2Cheat"
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"
LESSON = "corpus/lessons/round-44.md"
FETCH = ".ufo/waves/round-44/fetch/"
README = "corpus/README.md"
REG = "corpus/SOURCES.md"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}

URLS = {
    "Hyprland-Window.cpp": "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp",
    "Hyprland-XDGShell.cpp": "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/XDGShell.cpp",
    "xdg-shell.xml": "https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/stable/xdg-shell/xdg-shell.xml",
    "gdktoplevel-wayland.c": "https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c",
    "gkeep-ui.py": "https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py",
}
SHA = {
    "Hyprland-Window.cpp": "d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded",
    "Hyprland-XDGShell.cpp": "d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0",
    "xdg-shell.xml": "7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df",
    "gdktoplevel-wayland.c": "0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe",
    "gkeep-ui.py": "07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a",
}
Q = {
    "S164": ("Hyprland-Window.cpp",
             "return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);"),
    "S298": ("Hyprland-XDGShell.cpp",
             "m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);"),
    "S299": ("xdg-shell.xml",
             "The width and height arguments specify a hint to the window about how its surface should be resized"),
    "S300": ("gdktoplevel-wayland.c",
             "wayland_surface->next_layout.configured_width = width;"),
    "S301": ("gkeep-ui.py",
             "window.set_decorated(False) window.set_default_size(420, 500)"),
}
ROWS = [
    ("S298", "hyprwm/Hyprland src/protocols/XDGShell.cpp @ efb5099 (v0.56.2) - the toplevel setSize serial and its deferred configure - " + URLS["Hyprland-XDGShell.cpp"],
     "the toplevel's configure path for a reported size", "Hyprland-XDGShell.cpp:354-455 @ efb5099",
     "setSize stores the size as pending state and returns a serial; the deferred apply sends one configure"),
    ("S299", "wayland-protocols 1.49 stable/xdg-shell/xdg-shell.xml - the configure event's size semantics - " + URLS["xdg-shell.xml"],
     "what an xdg_toplevel.configure size means to a client", "xdg-shell.xml:1144-1161 @ 1.49",
     "the configure width and height are a hint; zero leaves the dimension to the client"),
    ("S300", "GNOME/gtk gdk/wayland/gdktoplevel-wayland.c @ 4.24.1 - how a GTK toplevel stores a configured size - " + URLS["gdktoplevel-wayland.c"],
     "how GTK 4.24.1 applies a configured size", "gdktoplevel-wayland.c:518-544, 633-637, 681 @ 4.24.1",
     "a non-zero configured size is kept for the next layout and becomes the surface size, raised to the minimum"),
    ("S301", "VeigaPunk/gkeep gkeep/ui.py @ 133b867 (full file) - the window gkeep builds and the only size it declares - " + URLS["gkeep-ui.py"],
     "the window gkeep builds and the only size it declares", "gkeep-ui.py:446-488 @ 133b867",
     "one undecorated window with set_default_size(420, 500), no set_size_request, application id org.omarchy.gkeep"),
]


def git(d, *a):
    p = subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, env=ENV)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (a, p.stderr))
    return p.stdout


def clone(name):
    d = os.path.join(SCRATCH, name)
    shutil.rmtree(d, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", LANE, d],
                   check=True, env=ENV)
    top = git(d, "rev-parse", "--show-toplevel").strip()
    assert top == os.path.realpath(d) or top == d, (top, d)
    git(d, "checkout", "-q", "--detach", FREEZE)
    return d


def registry_text(used_by_extra, rows, anchor_lie=False, anchor_range_lie=False):
    text = open(os.path.join(LANE, REG), encoding="utf-8").read().split("\n")
    s164 = next(i for i, l in enumerate(text) if l.startswith("| S164 "))
    cells = text[s164].split("|")
    # cells[0] and last are empty; 11 cells between
    assert len(cells) == 13, len(cells)
    if used_by_extra not in cells[11]:
        cells[11] = cells[11].rstrip() + ", " + used_by_extra + " "
    text[s164] = "|".join(cells).rstrip()
    s297 = next(i for i, l in enumerate(text) if l.startswith("| S297 "))
    new = []
    for sid, src, scope, anchor, teaches in rows:
        if anchor_lie and sid == "S300":
            scope = ("GTK forbids a client from deviating from the configured size "
                     "and proves the protocol's size is mandatory")
            teaches = "the configured size is mandatory for every client"
        if anchor_range_lie and sid == "S300":
            anchor = "gdktoplevel-wayland.c:9999-10005 @ 4.24.1"
        new.append("| %s | %s | code | A | %s | %s | %s | mined | 2026-10-26 | 90d | %s |"
                   % (sid, src, scope, anchor, teaches, ENTRY))
    text[s297 + 1:s297 + 1] = new
    return "\n".join(text)


def gate_text(s164_sha):
    out = ["# round 44 - lessons", "", "## Gate", ""]
    for sid, (f, q) in Q.items():
        sha = s164_sha if f == "Hyprland-Window.cpp" and sid == "S164" else SHA[f]
        out.append('GATE %s receipt=%s%s sha256=%s quote="%s"' % (sid, FETCH, f, sha, q))
    out += ["",
            "ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md as " + ENTRY,
            "REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-geometry-never-recorded-r15.md reason=the journal route is superseded by the pinned client path until a pinned journal receipt exists",
            ""]
    return "\n".join(out)


def build(name, entry, rows, extra_files=None, anchor_lie=False,
          anchor_range_lie=False, s164_sha=None):
    d = clone(name)
    files = {ENTRY: entry,
             LESSON: gate_text(s164_sha or SHA["Hyprland-Window.cpp"]),
             REG: registry_text(ENTRY, rows, anchor_lie, anchor_range_lie)}
    files.update(extra_files or {})
    for path, text in files.items():
        p = os.path.join(d, path)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        mode = "wb" if isinstance(text, bytes) else "w"
        with open(p, mode) as fh:
            fh.write(text)
    with open(os.path.join(d, README), "a") as fh:
        fh.write("| `knowledge/hyprland-gkeep-size-request-r44.md` (MADO-R44-2, round 44; "
                 "assimilation of the gkeep size-request theme) | forged fixture row | - |\n")
    git(d, "add", "-A")
    git(d, "-c", "user.name=fixture", "-c", "user.email=fixture@scratch.invalid",
        "commit", "-q", "-m", name)
    return d


def score(counter, d, rev="HEAD"):
    p = subprocess.run([sys.executable, "-I", counter, "--repo", d, "--rev", rev,
                        "--base", BASE], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    os.makedirs(SEAT, exist_ok=True)
    base_entry = open(os.path.join(LANE, ".ufo/waves/round-44/l1-draft/entry.md"),
                      encoding="utf-8").read()
    win = open(os.path.join(LANE, FETCH, "Hyprland-Window.cpp"), encoding="utf-8").read()

    # ---- F2: doctor the pinned Window.cpp so sendWindowSize calls nothing ----
    src = win.split("\n")
    k = src.index("void CWindow::sendWindowSize(bool force) {")
    e = src.index("}", k + 1)
    assert e > k + 2, (k, e)
    forged = "\n".join(src[:k + 1] + ["    ;"] + src[e:])
    forged_sha = hashlib.sha256(forged.encode()).hexdigest()
    f2_entry = base_entry.replace(
        "hyprland sendWindowSize xdg_setSize=1 x11_configure=1",
        "hyprland sendWindowSize xdg_setSize=0 x11_configure=0")
    assert f2_entry != base_entry
    f2_entry = f2_entry.replace(
        "**OBS** The same file's sendWindowSize (Hyprland-Window.cpp:1732) returns early",
        "**OBS** The compositor never notifies an xdg client of a size change: the body of "
        "sendWindowSize holds no setSize and no configure call (Hyprland-Window.cpp:1732), so the "
        "census line above is the whole path. **OBS** The same function (Hyprland-Window.cpp:1732) returns early")

    # ---- F1: true quote, inverted claim ----
    f1 = base_entry.replace(
        "**INF** So a GTK 4.24.1 window adopts a non-zero configured size unless that size is below its minimum, in which case it is raised to the minimum.",
        "**INF** So GTK 4.24.1 always adopts the configured size exactly: the minimum cannot override it and the client has no other choice.")
    assert f1 != base_entry

    # ---- F3: pin bytes, drifted locations ----
    drifted = []
    for sid, src_, scope, anchor, teaches in ROWS:
        if sid == "S301":
            src_ = src_.replace("133b86717a02548aeaff3f1411bf301d936c5308",
                                "0000000000000000000000000000000000000000")
        if sid == "S299":
            src_ = src_.replace("/raw/1.49/", "/raw/1.48/")
        drifted.append((sid, src_, scope, anchor, teaches))

    # ---- F4: census line true, prose contradicts it ----
    f4 = base_entry.replace(
        "**OBS** The file has no `set_size_request` call",
        "**OBS** gkeep declares 420x500 as a minimum through set_size_request(420, 500), so the configure of \u00a72 cannot shrink it.\n\n"
        "**OBS** The file has no `set_size_request` call")
    assert f4 != base_entry
    f4b = base_entry.replace(
        "**OBS** The file has no `set_size_request` call",
        "**OBS** gkeep calls set_default_size(800, 600) before the window is realized.\n\n"
        "**OBS** The file has no `set_size_request` call")
    assert f4b != base_entry

    # ---- F5: overclaim table that names no id ----
    f5 = base_entry.replace(
        "## \u00a73 What the protocol lets the client do",
        "## \u00a73 What the protocol lets the client do\n\n"
        "| question | answer | state |\n|---|---|---|\n"
        "| Does a client have to adopt the configured size? | yes, always | OBS |\n\n"
        "**OBS** No client may differ from the configure; the protocol and GTK agree, so the box "
        "Hyprland sends is the box the client commits.")
    assert f5 != base_entry

    # ---- F6: content-free shell: the five pins bound one line each, nothing else ----
    shell = ["# After the box: the gkeep size request (fixture shell)"]
    for sid, (f, q) in Q.items():
        shell.append("source: %s - %s" % (sid, f))
    shell += ["verified-at: 2026-10-26", "recheck: 90d", ""]
    locs = {"S164": "Hyprland-Window.cpp:1687", "S298": "Hyprland-XDGShell.cpp:455",
            "S299": "xdg-shell.xml:1150", "S300": "gdktoplevel-wayland.c:681",
            "S301": "gkeep-ui.py:475"}
    for sid, (f, q) in Q.items():
        shell.append("**OBS** %s - `%s` (%s)." % (sid, q, locs[sid]))
    shell += ["", "gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep",
              "hyprland sendWindowSize xdg_setSize=1 x11_configure=1", ""]
    shell = "\n".join(shell)

    runs = [
        ("F0-BASE", dict(entry=base_entry, rows=ROWS)),
        ("F1-CLAIM-INVERSION", dict(entry=f1, rows=ROWS)),
        ("F2-FORGED-PIN", dict(entry=f2_entry, rows=ROWS, s164_sha=forged_sha,
                               extra_files={FETCH + "Hyprland-Window.cpp": forged})),
        ("F3-LOCATION-DRIFT", dict(entry=base_entry, rows=drifted)),
        ("F4-SIZE-REQUEST-PROSE", dict(entry=f4, rows=ROWS)),
        ("F5-DEFAULT-SIZE-PROSE", dict(entry=f4b, rows=ROWS)),
        ("F6-OVERCLAIM-TABLE", dict(entry=f5, rows=ROWS)),
        ("F7-CONTENT-FREE-SHELL", dict(entry=shell, rows=ROWS)),
        ("F8-REGISTRY-ANCHOR-LIE", dict(entry=base_entry, rows=ROWS, anchor_lie=True)),
        ("F9-REGISTRY-ANCHOR-OUT-OF-RANGE", dict(entry=base_entry, rows=ROWS,
                                                 anchor_range_lie=True)),
    ]
    out = []
    for name, kw in runs:
        d = build(name, **kw)
        rc, txt = score(os.path.join(LANE, "quality/counters/c2-r44-gkeep-size-request.py"), d)
        out.append("### %s rc=%d\n%s" % (name, rc, txt))
        with open(os.path.join(SEAT, "frozen-" + name + ".txt"), "w") as fh:
            fh.write("repo=%s rc=%d\n%s" % (d, rc, txt))
        print(out[-1])
    with open(os.path.join(SEAT, "frozen-all.txt"), "w") as fh:
        fh.write("\n".join(out))
    print("wrote frozen receipts")

    # keep the fixture dirs listed for the tightened run
    with open(os.path.join(SEAT, "fixtures.txt"), "w") as fh:
        for name, _ in runs:
            fh.write("%s %s\n" % (name, os.path.join(SCRATCH, name)))


if __name__ == "__main__":
    main()
