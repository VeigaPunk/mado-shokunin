#!/usr/bin/env python3
"""CritC2Cheat (2): three more forged sets + two more P-safe probes.

X1 README index row reduced to a lie, X2 localized marker in the entry prose (not in a registry
row), X3 an entry that cites only the three own-work receipts (no Hyprland source at all).
Probes: refuse-flip-marker (P-safe) and the entry-wide BAD_LOC scan (P-safe), plus the
"every pinned receipt must be cited" tightening for X3.
"""
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WORK = "/fast/scratch/hyaku/mado-r43/CritC2Cheat"
COUNTER = os.path.join(LANE, "quality/counters/c2-r43-gkeep-entry.py")
CTL = os.path.join(LANE, ".ufo/waves/round-43/ctl/run-c2-controls.py")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
os.environ["TMPDIR"] = os.path.join(WORK, "tmp")
os.makedirs(os.environ["TMPDIR"], exist_ok=True)

spec = importlib.util.spec_from_file_location("ctl", CTL)
ctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctl)
ENTRY, SRC, LES, FETCH = ctl.ENTRY, ctl.SRC, ctl.LES, ctl.FETCH
EL = {i: ctl.entry_line(i) for i in ctl.REAL}
Q = {i: ctl.REAL[i][3] for i in ctl.REAL}
RULES_LINE, CLIENTS_LINE, UI_LINE = ctl.CENSUS
BASE = ctl.base_files()
P = ctl.admitted()
PI = {i: REAL for i, REAL in ()}  # placeholder, unused


def run(files_after, counter=COUNTER):
    d = tempfile.mkdtemp(prefix="mx-", dir=WORK)
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=ENV)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             check=True, capture_output=True, text=True,
                             env=ENV).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d)
        b = ctl.commit_all(d, BASE, "base")
        a = ctl.commit_all(d, files_after, "after")
        p = subprocess.run([sys.executable, "-I", counter, "--repo", d,
                            "--rev", a, "--base", b],
                           capture_output=True, text=True, env=ENV)
        lines = p.stdout.strip().splitlines()
        v = [l for l in lines if ": admitted=" in l]
        c = [l for l in lines if " clauses=" in l]
        return p.returncode, (v[-1] if v else "NO FINAL"), \
            (c[0].split("clauses=")[1].split(" admitted")[0] if c else "-")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def copy(g):
    return {k: v for k, v in g.items()}


def show(tag, rc, verdict, cls):
    print("%-30s rc=%d %s clauses=%s" % (tag, rc,
          verdict.split("PRED-C2-r43: ")[-1].split(" verdict")[0], cls))


# ---------- X3: cite only the three own-work receipts + the held id ----------
def four_source():
    g = ctl.base_files()
    ids = ["S297", "S298", "S299"]
    held = ctl.HELD_ROW.replace("corpus/knowledge/old.md",
                                "corpus/knowledge/old.md, " + ENTRY)
    rows = [held] + [ctl.row(i, ctl.REAL[i][2], kind=ctl.REAL[i][1]) for i in ids]
    gates = []
    g[FETCH + "S050.txt"] = ("%s source bytes for S050. %s\n"
                             % (ctl.HELD_Q, ctl.FILLER)).encode()
    gates.append(ctl.gate_line("S050", FETCH + "S050.txt",
                               g[FETCH + "S050.txt"], ctl.HELD_Q))
    for i in ids:
        fn = ctl.REAL[i][0]
        g[FETCH + fn] = ctl.blob(fn)
        gates.append(ctl.gate_line(i, FETCH + fn, g[FETCH + fn], ctl.REAL[i][3]))
    g[SRC] = g[SRC].replace(ctl.HELD_ROW, "\n".join(rows))
    g[LES] = ("# round 42\n\n## Gate\n\n" + "\n".join(gates) + "\n"
              + ctl.ADMIT + "\n" + ctl.REFUSE + "\n")
    body = ["# The gkeep window geometry", "",
            "source: S050 - held parser", "source: S297 - host rules",
            "source: S298 - host clients", "source: S299 - client request",
            "verified-at: 2026-10-26", "recheck: 90d", "",
            "**OBS** S050 %s (S050.txt:1)." % ctl.HELD_Q]
    for i in ids:
        body.append(EL[i])
    body += [""] + ctl.CENSUS + [""]
    g[ENTRY] = "\n".join(body) + "\n"
    g["corpus/README.md"] += "| `knowledge/hyprland-gkeep-geometry-r43.md` | new |\n"
    return g


print("X3 four sources, no Hyprland code cited:")
show("X3-own-work-only", *run(four_source()))

# ---------- X1: index row that says the entry was removed ----------------
g = copy(P)
g["corpus/README.md"] = g["corpus/README.md"].replace(
    "| `knowledge/hyprland-gkeep-geometry-r43.md` | new |",
    "| `knowledge/hyprland-gkeep-geometry-r43.md` | REMOVED, superseded, do not read |")
show("X1-index-row-lie", *run(g))

# ---------- X2: localized-channel marker in the entry prose --------------
g = copy(P)
g[ENTRY] = g[ENTRY] + "\n资料：中文文档频道解释了这个尺寸。\n"
show("X2-localized-in-entry", *run(g))

# ---------- probes -------------------------------------------------------
PROBES = {
    "refuse-flip-marker": (
        "        and all(m.group(1) != a.group(1) for a in adm)",
        "        and all(m.group(1) != a.group(1) for a in adm)\n"
        "        and re.search(r'\\b(superseded|until|unless|once|when|if|after)\\b',\n"
        "                      m.group(2).lower())"),
    "bad-loc-in-entry": (
        "    cl[\"i\"] = int(bool(adm) and bool(ref) and not bad)",
        "    bad |= any(b_ in l.lower() for l in lines for b_ in BAD_LOC)\n"
        "    cl[\"i\"] = int(bool(adm) and bool(ref) and not bad)"),
    "all-pins-cited": (
        "    cl[\"i\"] = int(bool(adm) and bool(ref) and not bad)",
        "    used = set(os.path.basename(gates[i][0][0]) for i in receipts)\n"
        "    bad |= not set(PINS) <= used\n"
        "    cl[\"i\"] = int(bool(adm) and bool(ref) and not bad)"),
}


def make_probe(name):
    src = open(COUNTER).read()
    old, new = PROBES[name]
    assert old in src, (name, old[:40])
    p = os.path.join(WORK, "c2-probe2-%s.py" % name)
    open(p, "w").write(src.replace(old, new, 1))
    return p


# F2 (no flip condition) and X2 (localized entry) fixtures
g_f2 = copy(P)
old = [l for l in g_f2[LES].splitlines() if l.startswith("REFUSE ")][0]
g_f2[LES] = g_f2[LES].replace(old, "REFUSE %s reason=this refusal says nothing else" % ctl.PKG2)
g_x2 = copy(P)
g_x2[ENTRY] = g_x2[ENTRY] + "\n资料：中文文档频道解释了这个尺寸。\n"

for probe, target in (("refuse-flip-marker", "F2-refuse-no-flip"),
                      ("bad-loc-in-entry", "X2-localized-in-entry"),
                      ("all-pins-cited", "X3-own-work-only")):
    c = make_probe(probe)
    for tag, g in ((("P-genuine", P)), (target, {"F2-refuse-no-flip": g_f2,
                                                 "X2-localized-in-entry": g_x2,
                                                 "X3-own-work-only": four_source()}[target])):
        rc, v, cls = run(copy(g), c)
        show("probe=%s %s" % (probe, tag), rc, v, cls)
