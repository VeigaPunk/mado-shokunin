#!/usr/bin/env python3
"""RevC2Counter falsifier fixtures for PRED-C2-r44 (round 44 w1).

Builds git fixtures under /fast/scratch/hyaku/mado-r44/RevC2Counter/fix-<kind>/
and runs the frozen counter on each. All git calls use -C D. Nothing in the
lane is written; lane fetch receipts are read only.
"""
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = LANE + "/quality/counters/c2-r44-gkeep-size-request.py"
FETCH = LANE + "/.ufo/waves/round-44/fetch"
SCRATCH = "/fast/scratch/hyaku/mado-r44/RevC2Counter"
BASE_REV = "6a1a90528fe533cadee506a9fa3e9d13d15cc41f"
ENTRY_PATH = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"

spec = importlib.util.spec_from_file_location("ctr", COUNTER)
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

RECEIPTS = ["Hyprland-Window.cpp", "Hyprland-XDGShell.cpp", "xdg-shell.xml",
            "gdktoplevel-wayland.c", "gkeep-ui.py"]
ID_OF = {"Hyprland-Window.cpp": "S164", "Hyprland-XDGShell.cpp": "S298",
         "xdg-shell.xml": "S299", "gdktoplevel-wayland.c": "S300",
         "gkeep-ui.py": "S301"}

QUOTES = {
    "Hyprland-Window.cpp":
        "else if (m_xdgSurface && m_xdgSurface->m_toplevel) "
        "m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());",
    "Hyprland-XDGShell.cpp":
        "m_pendingApply.size = size; scheduleStateApplication(); "
        "return m_owner->scheduleConfigure();",
    "xdg-shell.xml":
        "must make an ack_configure request sometime before the commit "
        "request, passing along the serial of the configure event.",
    "gdktoplevel-wayland.c":
        "fixed_size =\n    new_state & (GDK_TOPLEVEL_STATE_MAXIMIZED |\n"
        "                 GDK_TOPLEVEL_STATE_FULLSCREEN |\n"
        "                 GDK_TOPLEVEL_STATE_TILED) ||\n    is_resizing;",
    "gkeep-ui.py":
        'window = Gtk.ApplicationWindow(application=self, title="gkeep")\n'
        "window.set_decorated(False)\nwindow.set_default_size(420, 500)",
}

FORGED_WINDOW = """\
// forged receipt - falsifier fixture built by seat RevC2Counter (round 44 w1).
// NOT Hyprland source. Exercises the held-id receipt path of PRED-C2-r44.
void CWindow::sendWindowSize(bool force) {
    const auto REPORTPOS = realToReportPosition();
    m_reportedPosition    = REPORTPOS;
    return;
}
"""


def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if p.returncode != 0:
        raise SystemExit("FAILED %s\n%s\n%s" % (cmd, p.stdout, p.stderr))
    return p.stdout


def validate_quotes(blobs):
    """Return {name: (nq, at, sha)} after checking every clause-d property."""
    norm = {n: ctr.norm_receipt(b) for n, b in blobs.items()}
    out = {}
    for name, raw_q in QUOTES.items():
        q = re.sub(r"\s+", " ", raw_q)
        blob = blobs[name]
        wc = len(q.split())
        assert 3 <= wc <= 25, (name, "words", wc)
        at = ctr.quote_at(blob, q)
        assert at is not None, (name, "quote_at None")
        occ = ctr.occurrences(blob, q)
        assert len(occ) == 1, (name, "occurrences", len(occ))
        assert ctr.quote_in_code(blob, q, name), (name, "not in code")
        for other, onorm in norm.items():
            if other != name:
                assert q not in onorm, (name, "also in", other)
        out[name] = (q, at, hashlib.sha256(blob).hexdigest())
    return out


def gate_lines(packs, forged_sha=None):
    lines = []
    for name in RECEIPTS:
        q, at, sha = packs[name]
        if name == "Hyprland-Window.cpp" and forged_sha:
            sha = forged_sha
        lines.append('GATE %s receipt=.ufo/waves/round-44/fetch/%s '
                     'sha256=%s quote="%s"' % (ID_OF[name], name, sha, q))
    return lines


def build_entry(packs, kinds):
    """kinds: dict with keys census_hy, q164, at164, extra_line, s301_loc."""
    at = {n: packs[n][1] for n in RECEIPTS}
    lines = [
        "source: S164",
        "source: S298",
        "source: S299",
        "source: S300",
        "source: S301",
        "verified-at: 2026-10-26",
        "recheck: on-release",
        "",
        "# What a client may do with the size Hyprland sends (gkeep size request, round 44)",
        "",
        "gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep",
        "hyprland sendWindowSize " + kinds["census_hy"],
        "",
    ]
    if kinds.get("extra_line"):
        lines.append(kinds["extra_line"])
        lines.append("")
    lines += [
        "- S164: the window side forwards one reported size and parks the ack serial: \"%s\" (Hyprland-Window.cpp:%d)" % (kinds["q164"], kinds["at164"]),
        "- S298: a toplevel size is parked pending and answered by a scheduled configure: \"%s\" (Hyprland-XDGShell.cpp:%d)" % (packs["Hyprland-XDGShell.cpp"][0], at["Hyprland-XDGShell.cpp"]),
        "- S299: a committing client must ack the configure serial first: \"%s\" (xdg-shell.xml:%d)" % (packs["xdg-shell.xml"][0], at["xdg-shell.xml"]),
        "- S300: GTK folds the configured state into a fixed-size decision: \"%s\" (gdktoplevel-wayland.c:%d)" % (re.sub(r"\s+", " ", QUOTES["gdktoplevel-wayland.c"]), at["gdktoplevel-wayland.c"]),
        "- S301: gkeep declares a default size and no size request: \"%s\" (gkeep-ui.py:%d)" % (packs["gkeep-ui.py"][0], at["gkeep-ui.py"]),
    ]
    return "\n".join(lines) + "\n"


def build_rows(kind):
    base = run(["git", "-C", LANE, "show", BASE_REV + ":corpus/SOURCES.md"])
    out, hit = [], 0
    for line in base.split("\n"):
        if line.startswith("| S164 |"):
            stripped = line.rstrip()
            assert stripped.endswith("|"), stripped[-40:]
            body = stripped[:-1].rstrip()
            line = body + ", corpus/knowledge/hyprland-gkeep-size-request-r44.md |"
            hit += 1
        out.append(line)
    assert hit == 1, hit
    rev = "\n".join(out)
    loc301 = "https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py"
    if kind == "false_url":
        loc301 = "https://example.com/docs/ui.py"
    new_rows = [
        "| S298 | Hyprland commit efb5099 xdg toplevel state application - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/XDGShell.cpp | code | A | The xdg toplevel setSize path into scheduleConfigure | src/protocols/XDGShell.cpp:354-359 setSize stores the pending size, schedules the state application and returns scheduleConfigure at commit efb50993780079460b0cbed1363e2166a2de1d9f | A toplevel size change is parked pending and reaches the client as a configure with a serial | mined | 2026-10-26 | on-release | corpus/knowledge/hyprland-gkeep-size-request-r44.md |",
        "| S299 | wayland-protocols 1.49 xdg-shell ack_configure contract - https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/stable/xdg-shell/xdg-shell.xml | spec | A | What a client must do with a configure serial | stable/xdg-shell/xdg-shell.xml ack_configure description at tag 1.49, lines 562-592 | A committing client must ack the configure serial before the commit; acking is decoupled from committing | mined | 2026-10-26 | on-release | corpus/knowledge/hyprland-gkeep-size-request-r44.md |",
        "| S300 | GTK 4.24.1 Wayland toplevel configure handling - https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c | code | A | How GTK consumes a toplevel configure into surface state and size | gdk/wayland/gdktoplevel-wayland.c:606-643 handle_configure reads pending state and size at tag 4.24.1 | The client library folds the configured state into its next surface state and size | mined | 2026-10-26 | on-release | corpus/knowledge/hyprland-gkeep-size-request-r44.md |",
        "| S301 | gkeep 133b867 client window request - full ui.py - %s | code | A | The one place the client states identity and default size, and that it never calls a size request | gkeep/ui.py:449 application_id, :476 set_default_size(420, 500) at commit 133b86717a02548aeaff3f1411bf301d936c5308, full file | The client declares a 420x500 default and no size request, so its first geometry comes from the default and the compositor | mined | 2026-10-26 | on-release | corpus/knowledge/hyprland-gkeep-size-request-r44.md |" % loc301,
    ]
    idx = rev.index("\n| S164 |")
    insert_at = rev.index("\n", idx + 1) + 1
    rev = rev[:insert_at] + "\n".join(new_rows) + "\n" + rev[insert_at:]
    return base, rev


def build_lesson(gates):
    body = "\n".join(gates) + "\n" \
        + ("ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md as %s\n"
           % ENTRY_PATH) \
        + "REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-geometry-unobservable-r8.md reason=superseded by the round-44 entry until the r8 premise is rechecked against the state census\n"
    return "# Round 44 lesson\n\n## Gate\n\n" + body


README_ROW = ("| `knowledge/hyprland-gkeep-size-request-r44.md` (MADO-R44-2, round 44; "
              "assimilation of the gkeep size-request residue) | The client side of the gkeep box: the "
              "census of the pinned client bytes (set_default_size 420 500, no size request, "
              "application_id org.omarchy.gkeep), CWindow sendWindowSize forwarding one setSize into the "
              "pending ack list, the xdg-shell ack contract, GTK 4.24.1 configure handling, and the gkeep "
              "default-size declaration. ([gkeep size request](knowledge/hyprland-gkeep-size-request-r44.md), "
              "rows S164, S298-S301 plus held) |\n")


def make_fixture(kind):
    d = run(["mktemp", "-d", "-p", SCRATCH]).strip()
    run(["git", "-C", d, "init", "-q"])
    top = run(["git", "-C", d, "rev-parse", "--show-toplevel"]).strip()
    assert top == d, (top, d)
    run(["git", "-C", d, "config", "user.email", "fixture@example.invalid"])
    run(["git", "-C", d, "config", "user.name", "Fixture"])

    blobs = {n: open(os.path.join(FETCH, n), "rb").read() for n in RECEIPTS}
    packs = validate_quotes(blobs)

    forged_sha = None
    if kind == "forged_s164":
        blobs["Hyprland-Window.cpp"] = FORGED_WINDOW.encode()
        forged_sha = hashlib.sha256(blobs["Hyprland-Window.cpp"]).hexdigest()
        q = "m_reportedPosition = REPORTPOS;"
        fqblob = blobs["Hyprland-Window.cpp"]
        assert 3 <= len(q.split()) <= 25
        assert ctr.occurrences(fqblob, q) and len(ctr.occurrences(fqblob, q)) == 1
        assert ctr.quote_in_code(fqblob, q, "Hyprland-Window.cpp")
        at164 = ctr.quote_at(fqblob, q)
        packs164 = (q, at164, forged_sha)
        packs = dict(packs)
        packs["Hyprland-Window.cpp"] = packs164

    base, rev = build_rows(kind)
    os.makedirs(os.path.join(d, "corpus/knowledge"))
    os.makedirs(os.path.join(d, "corpus/lessons"))
    write(os.path.join(d, "corpus/SOURCES.md"), base)
    run(["git", "-C", d, "add", "-A"])
    run(["git", "-C", d, "commit", "-q", "-m", "base"])
    baserev = run(["git", "-C", d, "rev-parse", "HEAD"]).strip()

    for n, blob in blobs.items():
        p = os.path.join(d, ".ufo/waves/round-44/fetch", n)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(blob)
    write(os.path.join(d, "corpus/SOURCES.md"), rev)

    q164, at164 = packs["Hyprland-Window.cpp"][0], packs["Hyprland-Window.cpp"][1]
    census_hy = ("xdg_setSize=0 x11_configure=0" if kind == "forged_s164"
                 else "xdg_setSize=1 x11_configure=1")
    extra = None
    if kind == "hidden_line":
        extra = "gkeep client follow-up: per S164 the pending ack serial is the only transport of the configured size"
    if kind == "hidden_line_control":
        extra = "follow-up: per S164 the pending ack serial is the only transport of the configured size"
    entry = build_entry(packs, {"census_hy": census_hy, "q164": q164,
                                "at164": at164, "extra_line": extra})
    write(os.path.join(d, ENTRY_PATH), entry)
    write(os.path.join(d, "corpus/lessons/round-44.md"),
          build_lesson(gate_lines(packs, forged_sha)))
    write(os.path.join(d, "corpus/README.md"),
          "# Corpus\n\n## Index\n\n" + README_ROW)
    run(["git", "-C", d, "add", "-A"])
    run(["git", "-C", d, "commit", "-q", "-m", kind])
    revhash = run(["git", "-C", d, "rev-parse", "HEAD"]).strip()

    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", d,
                        "--rev", revhash, "--base", baserev],
                       capture_output=True, text=True)
    print("=== fixture %s  dir=%s" % (kind, d))
    print(p.stdout.strip())
    print("exit=%d" % p.returncode)
    if p.stderr.strip():
        print("stderr:", p.stderr.strip()[:400])
    return p.returncode


def write(path, text):
    open(path, "w").write(text)


if __name__ == "__main__":
    kinds = sys.argv[1:] or ["honest", "forged_s164", "hidden_line",
                             "hidden_line_control", "false_url"]
    for k in kinds:
        make_fixture(k)
