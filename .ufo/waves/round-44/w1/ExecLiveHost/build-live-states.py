#!/usr/bin/env python3
"""Assemble live-states.txt (the C1 live-host receipt) from the captured artifacts.

Every included block is the verbatim bytes of a file in this directory or the verbatim
output of a read-only command captured into one. The three `live-*.json` dumps are the
SHAPE-ONLY projections of the raw `hyprctl` output (project-dumps.py): window titles,
PIDs, stable ids, monitor serial/make/model and workspace titles are not in the repo; the
raw dumps' sha256 are in raw-dumps.sha256. Values computed here (sha256, per-client state
table, the before/after table) are marked as computed.

Every subprocess is bounded (timeout=30 s) so a pathological rule regex cannot hang the
seat; a timeout is recorded as rc 124 with a visible marker, never as a verdict.
"""
import hashlib
import json
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RULES = os.path.expanduser("~/.config/hypr/gkeep.conf")
TIMEOUT = 30


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def rd(p):
    with open(p, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def run(argv):
    try:
        p = subprocess.run(argv, capture_output=True, cwd=HERE, text=True, timeout=TIMEOUT)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as exc:
        return 124, (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or ""), \
            "TIMEOUT: %r exceeded %d s (recorded as rc 124, not a verdict)\n" % (argv, TIMEOUT)


out = []
w = out.append

w("ExecLiveHost - C1 live host receipt (mado round 44, wave w1, seat ExecLiveHost)")
w("generated: %s (host clock)" % time.strftime("%Y-%m-%dT%H:%M:%S%z"))
w("lane: /home/vgpnk/Projects/shokunin/mado-shokunin  base rev: 6a1a90528fe533cadee506a9fa3e9d13d15cc41f")
w("")
w("This file is REPORTED, not scored. Every read verb below is one of the four allowed")
w("compositor reads (version, clients -j, monitors -j, workspaces -j); no dispatch,")
w("keyword, reload, setprop, --batch, output, plugin or kill was issued.")
w("")
w("== shape-only projection (SKILL.md:332: `clients` for length/tags, never window titles) ==")
w("The dumps below are projections of the raw hyprctl output; the raw bytes are not retained.")
w("Dropped and never read by any tool or claim here: title, initialTitle, pid, stableId,")
w("grouped, tags, swallowing, xdgTag, xdgDescription, contentType, focusHistoryID, hidden,")
w("visible, acceptsInput, allowedOverFullscreen, pinned, pinFullscreened, inhibitingIdle,")
w("tearingHint, xwayland, initialClass, workspace; monitor description/make/model/serial/")
w("physical*/specialWorkspace/availableModes/colour fields; workspace lastwindow and")
w("lastwindowtitle. project-dumps.py records what was kept and the raw sha256:")
w("")
w(rd(os.path.join(HERE, "raw-dumps.sha256")).rstrip("\n"))
w("")
w("projection invariance (projection-invariance.txt, sha256 %s): the tool reads only"
  % sha(os.path.join(HERE, "projection-invariance.txt")))
w("address/class/floating/mapped/size/fullscreen, so raw and projected clients give identical")
w("stdout under both tools; that file shows the cmp and both outputs.")
w("")
w("== tools under test ==")
w("new (reference control copy)  w1/ExecLiveHost/mado-geometry.py")
w("  sha256 %s" % sha(os.path.join(HERE, "mado-geometry.py")))
w("  source .ufo/waves/round-44/c1/ctl-ref-tool.py.txt sha256 %s" % sha(
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/c1/ctl-ref-tool.py.txt"))
w("  bytes identical: %s" % (sha(os.path.join(HERE, "mado-geometry.py")) == sha(
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/c1/ctl-ref-tool.py.txt")))
w("round-43 baseline            w1/ExecLiveHost/mado-geometry-r43.py")
w("  sha256 %s" % sha(os.path.join(HERE, "mado-geometry-r43.py")))
w("  extracted verbatim: git -C <lane> show 6a1a9052...:tools/mado-geometry.py")
w("  grep 'fullscreen' over that file: %d hits (it has no state model)" % rd(
    os.path.join(HERE, "mado-geometry-r43.py")).count("fullscreen"))
w("")
w("== host ==")
rc, so, se = run(["hyprctl", "version"])
w("$ hyprctl version   (rc=%d, stderr=%d bytes)" % (rc, len(se)))
w(so.rstrip("\n"))
w("")
if os.path.exists("/proc/sys/kernel/osrelease"):
    w("kernel: %s" % rd("/proc/sys/kernel/osrelease").strip())
w("")

w("== hyprctl monitors -j, projected (live-monitors.json sha256 %s) ==" % sha(os.path.join(HERE, "live-monitors.json")))
w(rd(os.path.join(HERE, "live-monitors.json")).rstrip("\n"))
w("")
w("== hyprctl workspaces -j, projected (live-workspaces.json sha256 %s) ==" % sha(os.path.join(HERE, "live-workspaces.json")))
w(rd(os.path.join(HERE, "live-workspaces.json")).rstrip("\n"))
w("")
w("== hyprctl clients -j, projected (live-clients.json sha256 %s, %d bytes) ==" % (
    sha(os.path.join(HERE, "live-clients.json")), os.path.getsize(os.path.join(HERE, "live-clients.json"))))
w(rd(os.path.join(HERE, "live-clients.json")).rstrip("\n"))
w("")

live = json.loads(rd(os.path.join(HERE, "live-clients.json")))
mons = json.loads(rd(os.path.join(HERE, "live-monitors.json")))
w("== state fields carried by the projected live dump, per client (computed) ==")
w("both `fullscreen` and `fullscreenClient` are present on every client: %s"
  % all("fullscreen" in c and "fullscreenClient" in c for c in live))
for c in live:
    w("addr=%s class=%r mapped=%r floating=%r size=%r at=%r fullscreen=%r (type %s) fullscreenClient=%r (type %s) fullscreenHandler=%r"
      % (c["address"], c["class"], c["mapped"], c["floating"], c["size"], c["at"],
         c.get("fullscreen"), type(c.get("fullscreen")).__name__,
         c.get("fullscreenClient"), type(c.get("fullscreenClient")).__name__,
         c.get("fullscreenHandler")))
w("distinct `fullscreen` values across the live dump: %r" % sorted({c.get("fullscreen") for c in live}, key=repr))
w("")
mon = next(m for m in mons if m["activeWorkspace"]["id"] == 1)
mw, mh = mon["width"], mon["height"]
res = mon["reserved"]
w("== geometry the live monitor reports (computed) ==")
w("monitor %s: box %dx%d at (%d,%d), reserved=%r, scale=%r, transform=%r" % (
    mon["name"], mw, mh, mon["x"], mon["y"], res, mon["scale"], mon["transform"]))
w("monitor box (what fullscreen 2 is pinned to): %dx%d" % (mw, mh))
w("work area = monitor box minus reserved (l,t,r,b): %dx%d (what maximized 1 is pinned to)" % (
    mw - res[0] - res[2], mh - res[1] - res[3]))
z = next(c for c in live if c["class"] == "zcode")
w("cross-check on live bytes: the tiled zcode client occupies %r at %r" % (z["size"], z["at"]))
w("")

w("== rules file used for the gkeep join (verbatim %s, sha256 %s) ==" % (RULES, sha(RULES)))
w(rd(RULES).rstrip("\n"))
w("")
w("== rules file used for the live-bytes probe (verbatim live-bytes.conf, sha256 %s) ==" % sha(os.path.join(HERE, "live-bytes.conf")))
w(rd(os.path.join(HERE, "live-bytes.conf")).rstrip("\n"))
w("")

w("== A. the reference tool on the running desktop (stdin, raw pipe at read time) ==")
w("$ hyprctl clients -j | python3 -I mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf")
w(rd(os.path.join(HERE, "live-run-ref.rc")).strip())
w("stdout (verbatim live-run-ref.out, sha256 %s):" % sha(os.path.join(HERE, "live-run-ref.out")))
w(rd(os.path.join(HERE, "live-run-ref.out")).rstrip("\n"))
w("stderr: %d bytes (live-run-ref.err sha256 %s)" % (
    os.path.getsize(os.path.join(HERE, "live-run-ref.err")), sha(os.path.join(HERE, "live-run-ref.err"))))
w("expected NO_MATCHING_CLIENT rc 3 while no gkeep window is open: %s"
  % (rd(os.path.join(HERE, "live-run-ref.rc")).strip() == "rc=3"
     and "verdict=NO_MATCHING_CLIENT" in rd(os.path.join(HERE, "live-run-ref.out"))))
w("")

w("== B. live bytes with a rule that MATCHES a real client (no-hazard check) ==")
w("The live desktop has no gkeep window, so the gkeep join cannot exercise a match; a rule")
w("written against the real Alacritty client (tiled, size 1720x1414) does. Both tools must")
w("print the round-43 line byte-identically here, because no matched client is in a state.")
w("")
for tool, tag in (("mado-geometry.py", "new"), ("mado-geometry-r43.py", "r43")):
    rc, so, se = run(["python3", "-I", tool, "--clients", "live-clients.json", "--rules", "live-bytes.conf"])
    w("$ python3 -I %s --clients live-clients.json --rules live-bytes.conf   [%s]  rc=%d" % (tool, tag, rc))
    w(so.rstrip("\n"))
    w("stderr: %d bytes" % len(se))
    w("")
new_out = run(["python3", "-I", "mado-geometry.py", "--clients", "live-clients.json", "--rules", "live-bytes.conf"])[1]
r43_out = run(["python3", "-I", "mado-geometry-r43.py", "--clients", "live-clients.json", "--rules", "live-bytes.conf"])[1]
w("byte-identical stdout on the live match: %s" % (new_out == r43_out))
w("")

w("== C. hand-made state dumps (built by make-state-dumps.py from the projected client record) ==")
w("fs2.json   class=org.omarchy.gkeep floating=true size=%dx%d at=(%d,%d) fullscreen=2  (monitor box)" % (
    mw, mh, mon["x"], mon["y"]))
w("max1.json  class=org.omarchy.gkeep floating=true size=%dx%d at=(%d,%d) fullscreen=1  (work area)" % (
    mw - res[0] - res[2], mh - res[1] - res[3], mon["x"], mon["y"] + res[1]))
for n in ("fs2.json", "max1.json"):
    w("  %s sha256 %s, %d keys, verbatim:" % (n, sha(os.path.join(HERE, n)), len(json.loads(rd(os.path.join(HERE, n)))[0])))
    w(rd(os.path.join(HERE, n)).rstrip("\n"))
w("")
w(rd(os.path.join(HERE, "runs.raw")).rstrip("\n"))
w("")

w("== D. before/after table (computed from section C) ==")
w("dump      client size   fullscreen  round-43 verdict (rc)  new verdict (rc)")
rows = [("fs2.json", "%dx%d" % (mw, mh), 2), ("max1.json", "%dx%d" % (mw - res[0] - res[2], mh - res[1] - res[3]), 1)]
for dump, size, mode in rows:
    a = run(["python3", "-I", "mado-geometry-r43.py", "--clients", dump, "--rules", RULES])
    b = run(["python3", "-I", "mado-geometry.py", "--clients", dump, "--rules", RULES])
    av = [l for l in a[1].splitlines() if "verdict=" in l and l.startswith("MADO_GEOM_CLIENT")][0].split("verdict=")[1]
    bv = [l for l in b[1].splitlines() if "verdict=" in l and l.startswith("MADO_GEOM_CLIENT")][0].split("verdict=")[1]
    w("%-9s %-13s %-11d %-24s %s (rc %d)" % (dump, size, mode, "%s (rc %d)" % (av, a[0]), bv, b[0]))
w("")
w("Both state dumps are DIFFER (rc 1) under the round-43 tool and FULLSCREEN/MAXIMIZED (rc 0)")
w("under the new tool: the round-43 tool cannot tell a rule miss from a compositor-owned box.")
w("")

w("== F. pin cross-check: what the two state dumps encode, and which JSON field the tool reads ==")
PINS = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/fetch-c1"


def locate(pin, needle):
    return [(i, ln.rstrip("\n")) for i, ln in enumerate(rd(os.path.join(PINS, pin)).splitlines(), 1) if needle in ln]


w("Locators below are computed at build time (line scan), never typed; verify-quotes.py re-checks")
w("every quote against the pin file at that line and against this receipt.")
w("")
w("-- Hyprland-FullscreenHandler.cpp: modes map to the boxes the dumps use --")
for needle in ("if (TARGET_INTERNAL_MODE == FSMODE_FULLSCREEN) {",
               "const CBox MONBOX",
               "else if (TARGET_INTERNAL_MODE == FSMODE_MAXIMIZED) {",
               "workArea(target->floating());",
               "workArea(FS_TARGET->floating());"):
    hits = locate("Hyprland-FullscreenHandler.cpp", needle)
    assert hits, needle
    for ln, text in hits:
        w("  fetch-c1/Hyprland-FullscreenHandler.cpp:%d  %s" % (ln, text.strip()))
w("")
w("-- Hyprland-HyprCtl.cpp: which JSON field carries which mode --")
for needle in ('"fullscreen": {},', 'getFullscreenModes(w).internal',
               '"fullscreenClient": {},', 'getFullscreenModes(w).client',
               'size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x',
               'size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y'):
    hits = locate("Hyprland-HyprCtl.cpp", needle)
    assert hits, needle
    for ln, text in hits:
        w("  fetch-c1/Hyprland-HyprCtl.cpp:%d  %s" % (ln, text.strip()))
w("")
w("-- Hyprland-FullscreenController.hpp: the numeric encoding --")
for ln, text in locate("Hyprland-FullscreenController.hpp", "enum eFullscreenMode")[:1]:
    block = rd(os.path.join(PINS, "Hyprland-FullscreenController.hpp")).splitlines()[ln - 1:ln + 4]
    for k, line in enumerate(block):
        w("  fetch-c1/Hyprland-FullscreenController.hpp:%d  %s" % (ln + k, line.strip()))
for needle in ("eFullscreenMode internal = FSMODE_NONE;", "eFullscreenMode client   = FSMODE_NONE;"):
    for ln, text in locate("Hyprland-FullscreenController.hpp", needle):
        w("  fetch-c1/Hyprland-FullscreenController.hpp:%d  %s" % (ln, text.strip()))
w("")
w("=> eFullscreenMode: NONE=0, MAXIMIZED=1, FULLSCREEN=2 = the contract's fsmode 1/2.")
w("=> `fullscreen` in the JSON dump is the INTERNAL mode; `fullscreenClient` is the separate client")
w("   mode. The tool reads `fullscreen`; today's live dump carries both, all zero.")
w("")
w("Contract clauses the live run exercises, quoted from the tool docstring (located, <= 25 words):")
for needle in ("fsmode is the `fullscreen` value when it is a JSON integer",
               "FULLSCREEN (fsmode 2) | MAXIMIZED (fsmode 1) | TILED (not floating) | AGREE",
               "(the bracketed pair is printed exactly when maximized + fullscreen > 0"):
    hits = [(i, ln.rstrip("\n")) for i, ln in enumerate(rd(os.path.join(HERE, "mado-geometry.py")).splitlines(), 1) if needle in ln]
    assert len(hits) == 1, (needle, hits)
    w("  w1/ExecLiveHost/mado-geometry.py:%d  %s" % (hits[0][0], hits[0][1].strip()))
w("")
w("pin sha256 (fetch-c1, re-hashed here against .ufo/waves/round-44/receipts/fetch-sha256.txt):")
for n in ("Hyprland-FullscreenHandler.cpp", "Hyprland-FullscreenController.hpp", "Hyprland-HyprCtl.cpp"):
    listed = [ln.split()[0] for ln in rd(
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/receipts/fetch-sha256.txt").splitlines()
        if ln.strip().split()[-1] == "fetch-c1/" + n]
    w("  %-38s %s  %s" % (n, sha(os.path.join(PINS, n)), "matches receipt" if listed == [sha(os.path.join(PINS, n))] else "MISMATCH %r" % listed))
w("")

w("== G. selftests of the two tools (not scored here), each bounded by timeout=%d s ==" % TIMEOUT)
for tool in ("mado-geometry.py", "mado-geometry-r43.py"):
    rc, so, se = run(["python3", "-I", tool, "--selftest"])
    w("$ python3 -I %s --selftest   rc=%d" % (tool, rc))
    w(so.rstrip("\n"))
w("")
w("== file bounds ==")
w("every subprocess in this builder runs with timeout=%d s; a run that exceeds it is recorded" % TIMEOUT)
w("as rc 124 with a TIMEOUT marker, never as a verdict. SKILL.md:300's shell form is")
w("`timeout 5 python3 tools/mado-geometry.py --clients - --rules <file>` with exit 124 as no verdict.")
w("")
w("== files in this seat dir (this receipt and the verifier output excluded: they change per run) ==")
SKIP = {"live-states.txt", "verify-quotes.out"}
for name in sorted(os.listdir(HERE)):
    p = os.path.join(HERE, name)
    if os.path.isfile(p) and name not in SKIP:
        w("%-24s %8d bytes  sha256 %s" % (name, os.path.getsize(p), sha(p)))

with open(os.path.join(HERE, "live-states.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
print("wrote live-states.txt (%d lines)" % len(open(os.path.join(HERE, "live-states.txt")).read().splitlines()))
