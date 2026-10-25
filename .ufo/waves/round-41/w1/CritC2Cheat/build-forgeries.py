#!/usr/bin/env python3
"""CritC2Cheat: fabricate entries that PRED-C2-r41-v1 admits (1/1).

Every fixture is a throwaway repo `D=$(mktemp -d)`; every git call names -C D,
the throwaway identity is passed with -c, and `git -C D rev-parse
--show-toplevel` is checked equal to D before the first commit. Builders are
imported from .ufo/waves/round-41/ctl/run-c2-controls.py (its `main` is never
run). The frozen counter is executed with `python3 -I` per fixture; the
tightenings in tighten.py are evaluated on the same committed bytes.

Fixtures: GENUINE-PROXY (real fetch bytes + real journal counts; must be
admitted and must pass every tightening) and F1..F7 (fabrications; must be
admitted by the frozen counter and refused by the tightening named in
forgeries.md).

Writes only beneath this seat directory: forgeries.json.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
CTL = os.path.join(LANE, ".ufo", "waves", "round-41", "ctl",
                   "run-c2-controls.py")
COUNTER = os.path.join(LANE, "quality", "counters", "c2-r41-focus-entry.py")
FETCH_DIR = os.path.join(LANE, ".ufo", "waves", "round-41", "fetch")
sys.path.insert(0, HERE)
import tighten  # noqa: E402

_s = importlib.util.spec_from_file_location("c2ctl", CTL)
ctl = importlib.util.module_from_spec(_s)
_s.loader.exec_module(ctl)

FG = ctl.FG
ENTRY = ctl.ENTRY
SRC = ctl.SRC
LES = ctl.LES
FETCH = ctl.FETCH


def real(fn):
    with open(os.path.join(FETCH_DIR, fn), "rb") as fh:
        return fh.read().decode("utf-8")


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def gate(i, fn, text, quote):
    return ctl.gate_line(i, FETCH + fn, text, quote)


# ---------------------------------------------------------------- genuine proxy
GEN = {
    "S283": ("focus-grab-v1.xml", "docs",
             "https://raw.githubusercontent.com/hyprwm/hyprland-protocols/"
             "cd1aba6bd78775825eb230b3a4274c48b6705eb7/protocols/"
             "focus-grab-v1.xml",
             "This protocol allows clients to limit input focus to a "
             "specific set of surfaces"),
    "S284": ("Hyprland-FocusGrab.cpp", "code",
             "https://raw.githubusercontent.com/hyprwm/Hyprland/"
             "efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/"
             "FocusGrab.cpp",
             "CFocusGrab::refocusKeyboard called with no committed surfaces"),
    "S285": ("quickshell-grab.cpp", "code",
             "https://raw.githubusercontent.com/quickshell-mirror/quickshell/"
             "9b0f339b19057f4731bf3b48293307d7ef241671/src/wayland/hyprland/"
             "focus_grab/grab.cpp",
             "bool FocusGrab::isActive() const { return this->active; }"),
    "S286": ("xdph-PortalManager.cpp", "code",
             "https://raw.githubusercontent.com/hyprwm/"
             "xdg-desktop-portal-hyprland/v1.4.1/src/core/PortalManager.cpp",
             "Screencopy not started: compositor doesn't support "
             "zwlr_screencopy_v1"),
    "S287": ("protocols-README.md", "docs",
             "https://raw.githubusercontent.com/hyprwm/hyprland-protocols/"
             "cd1aba6bd78775825eb230b3a4274c48b6705eb7/README.md",
             "for grabbing input focus, primarily for complex context menus"),
    "S288": ("xdph-journal.txt", "own-work",
             FETCH + "xdph-journal.txt",
             "Got interface: hyprland_focus_grab_manager_v1 (ver 1)"),
}


def genuine():
    g = ctl.base_files()
    held = ctl.HELD_ROW.replace("corpus/knowledge/old.md",
                                "corpus/knowledge/old.md, " + ENTRY)
    rows = [ctl.row(i, loc, kind=kind) for i, (_fn, kind, loc, _q)
            in sorted(GEN.items())]
    g[SRC] = g[SRC].replace(ctl.HELD_ROW, held + "\n" + "\n".join(rows))
    gates, obs = [], []
    for i, (fn, _kind, _loc, q) in sorted(GEN.items()):
        text = real(fn)
        g[FETCH + fn] = text
        gates.append(gate(i, fn, text, q))
        obs.append("**OBS** %s %s." % (i, q))
    jtext = real("xdph-journal.txt")
    jline = "journal sessions=%d adverts=%d interfaces=%d focus_grab=%d" % \
        tighten.c2.journal_counts(jtext.encode())
    g[LES] = ("# round 41\n\n## Gate\n\n" + "\n".join(gates) + "\n" +
              ctl.ADMIT + "\n" + ctl.REFUSE + "\n")
    head = ["# Hyprland focus grab (genuine proxy)", ""]
    head += ["source: %s - %s" % (i, fn) for i, (fn, _k, _l, _q)
             in sorted(GEN.items())]
    head += ["verified-at: 2026-10-25", "recheck: 90d", ""]
    g[ENTRY] = "\n".join(head + obs + ["", jline, ""]) + "\n"
    g["corpus/README.md"] += \
        "| `knowledge/hyprland-focus-grab-r41.md` | new |\n"
    return g, jline


# -------------------------------------------------------------------- F1..F7

def _entry(g, ids, obs, jline, gates):
    g[LES] = ("# round 41\n\n## Gate\n\n" + "\n".join(gates) + "\n" +
              ctl.ADMIT + "\n" + ctl.REFUSE + "\n")
    head = ["# focus grab", ""] + ["source: %s - x" % i for i in ids] + \
        ["verified-at: 2026-10-25", "recheck: 90d", ""]
    g[ENTRY] = "\n".join(head + obs + ["", jline, ""]) + "\n"
    g["corpus/README.md"] += \
        "| `knowledge/hyprland-focus-grab-r41.md` | new |\n"
    return g, jline


def f1_invented_512():
    """Three invented receipts, each exactly 512 bytes; the journal is real."""
    g = ctl.base_files()
    ids = [("S301", "https://example.org/a.xml", "docs", "S301.html"),
           ("S302", FETCH + "xdph-journal.txt", "own-work",
            "xdph-journal.txt"),
           ("S303", "https://example.org/c.cpp", "code", "S303.html"),
           ("S304", "https://example.org/d.md", "docs", "S304.html")]
    g[SRC] = g[SRC].replace(ctl.HELD_ROW, ctl.HELD_ROW.replace(
        "corpus/knowledge/old.md",
        "corpus/knowledge/old.md, " + ENTRY) + "\n" + "\n".join(
        ctl.row(i, loc, kind=k) for i, loc, k, _fn in ids))
    jtext = real("xdph-journal.txt")
    gates, obs = [], []
    for i, _loc, _k, fn in ids:
        if fn == "xdph-journal.txt":
            text, q = jtext, GEN["S288"][3]
        else:
            q = "fabricated body for %s" % i
            body = ("%s. the lane never fetched this artifact. " % q) + \
                ("invented padding sentence number %s. " % i) * 20
            text = body.encode("ascii")[:512].decode()
            assert len(text) == 512, len(text)
        g[FETCH + fn] = text
        gates.append(gate(i, fn, text, q))
        obs.append("**OBS** %s %s." % (i, q))
    jline = "journal sessions=%d adverts=%d interfaces=%d focus_grab=%d" % \
        tighten.c2.journal_counts(jtext.encode())
    return _entry(g, [i for i, _l, _k, _f in ids], obs, jline, gates)


def f2_invented_journal():
    """A journal that was never on this host: invented names, fabricated boots."""
    g, _ = genuine()
    lines = []
    for s in range(2):
        lines.append("-- Boot %032x --" % (0xabc000 + s))
        pid = str(4100 + s)
        for k in range(20):
            name = FG if k == 19 else "invented_iface_%02d" % k
            lines.append(ctl.advert("2026-10-25T09:%02d:00+00:00" % (10 + k),
                                    pid, name))
    jtext = "\n".join(lines) + "\n"
    q = GEN["S288"][3]
    g[FETCH + "xdph-journal.txt"] = jtext + "\n# " + q + "\n"
    gates, obs = [], []
    for i, (fn, _k, _l, qq) in sorted(GEN.items()):
        text = g[FETCH + fn]
        gates.append(gate(i, fn, text, qq))
        obs.append("**OBS** %s %s." % (i, qq))
    jline = "journal sessions=%d adverts=%d interfaces=%d focus_grab=%d" % \
        tighten.c2.journal_counts(g[FETCH + "xdph-journal.txt"].encode())
    return _rebuild(g, gates, obs, jline)


def f3_absent_package():
    """ADMIT/REFUSE name staged files that do not exist."""
    g, jline = genuine()
    g[LES] = g[LES].replace(
        ctl.PKG, "merge/mado/knowledge/corpus/knowledge/no-such-entry-r99.md")
    g[LES] = g[LES].replace(
        ctl.PKG2, "merge/mado/knowledge/corpus/knowledge/absent-r98.md")
    return g, jline


def f3b_space_reason():
    """REFUSE reason is 24 spaces: >= 20 characters, zero content."""
    g, jline = genuine()
    g[LES] = g[LES].replace(
        "reason=generic wayland security analysis, not a measurement",
        "reason=" + " " * 24)
    return g, jline


def f4_localized_redirect():
    """The Japanese channel behind an opaque redirector URL."""
    g, jline = genuine()
    loc = "https://t.co/9xQ2fG"
    q = "フォーカス グラブ マネージャ の 広告"
    body = ("この記事は Hyprland のフォーカスグラブを説明する。"
            "%s が実際に観測された。ローカル限定の文書チャネルである。"
            % q) * 30
    text = body
    g[FETCH + "S287.html"] = text
    row_old = ctl.row("S287", GEN["S287"][2], kind="docs")
    g[SRC] = g[SRC].replace(row_old, ctl.row("S287", loc, kind="docs"))
    gates, obs = [], []
    for i, (fn, _k, _l, qq) in sorted(GEN.items()):
        t = text if i == "S287" else g[FETCH + fn]
        qq2 = q if i == "S287" else qq
        gates.append(gate(i, "S287.html" if i == "S287" else fn, t, qq2))
        obs.append("**OBS** %s %s." % (i, qq2))
    return _rebuild(g, gates, obs, jline)


def f5_shared_boilerplate():
    """Every Gate quote is a different substring of one shared footer."""
    g, jline = genuine()
    footer = ("Fetched by the round 41 lane fetch harness on 2026-10-25 and "
              "frozen for the wave; do not edit these bytes by hand.")
    qs = {
        "S283": "Fetched by the round 41 lane fetch harness",
        "S284": "frozen for the wave; do not edit these bytes",
        "S285": "do not edit these bytes by hand",
        "S286": "the round 41 lane fetch harness on 2026-10-25",
        "S287": "do not edit these bytes",
        "S288": "round 41 lane fetch harness on 2026-10-25 and frozen",
    }
    gates, obs = [], []
    for i, (fn, _k, _l, _q) in sorted(GEN.items()):
        base = g[FETCH + fn]
        text = base + "\n# " + footer + "\n"
        g[FETCH + fn] = text
        gates.append(gate(i, fn, text, qs[i]))
        obs.append("**OBS** %s %s." % (i, qs[i]))
    return _rebuild(g, gates, obs, jline)


def f6_one_char_location():
    """A cited new row whose location differs by one character from a held row."""
    g, _ = genuine()
    g["corpus/README.md"] = ctl.base_files()["corpus/README.md"]
    text = "near duplicate source body. " * 30
    q = "near duplicate source body"
    g[FETCH + "S289.txt"] = text
    g[SRC] = g[SRC].replace(
        ctl.row("S283", GEN["S283"][2], kind="docs"),
        ctl.row("S283", GEN["S283"][2], kind="docs") + "\n" +
        ctl.row("S289", "https://example.org/confiq.cpp", kind="docs"))
    gates, obs = [], []
    for i, (fn, _k, _l, qq) in sorted(GEN.items()):
        gates.append(gate(i, fn, g[FETCH + fn], qq))
        obs.append("**OBS** %s %s." % (i, qq))
    gates.append(gate("S289", "S289.txt", text, q))
    obs.append("**OBS** S289 %s." % q)
    ids = sorted(GEN) + ["S289"]
    jline = "journal sessions=%d adverts=%d interfaces=%d focus_grab=%d" % \
        tighten.c2.journal_counts(g[FETCH + "xdph-journal.txt"].encode())
    return _entry(g, ids, obs, jline, gates)


HELD2 = ("| S051 | held journal grammar note - https://example.org/j.md "
         "| docs | A | scope | anchor | teaches | mined | 2026-10-24 | "
         "on-change | corpus/knowledge/old.md |")


def base_two_held():
    g = ctl.base_files()
    g[SRC] = g[SRC].replace(ctl.HELD_ROW, ctl.HELD_ROW + "\n" + HELD2)
    return g


def f7_two_new_ids(base):
    """Two new ids: the code tests >= 2, the docstring demands >= 3."""
    g = dict(base)
    held2 = HELD2
    used = "corpus/knowledge/old.md, " + ENTRY
    new = [ctl.row("S301", "https://example.org/a.xml"),
           ctl.row("S302", FETCH + "S302.journal.txt", kind="own-work")]
    g[SRC] = g[SRC].replace(
        ctl.HELD_ROW + "\n" + held2,
        ctl.HELD_ROW.replace("corpus/knowledge/old.md", used) + "\n" +
        held2.replace("corpus/knowledge/old.md", used) + "\n" +
        "\n".join(new))
    jtext = real("xdph-journal.txt")
    receipts = {
        "S050": ("S050.txt", "handlers and gradients keep the previous angle"),
        "S051": ("S051.txt", "the journal grammar counts a session per boot"),
        "S301": ("S301.html", "protocol xml declares a grab request"),
        "S302": ("S302.journal.txt", GEN["S288"][3]),
    }
    gates, obs = [], []
    for i, (fn, q) in sorted(receipts.items()):
        text = jtext if i == "S302" else (q + ". " + ctl.FILLER)
        g[FETCH + fn] = text
        gates.append(gate(i, fn, text, q))
        obs.append("**OBS** %s %s." % (i, q))
    jline = "journal sessions=%d adverts=%d interfaces=%d focus_grab=%d" % \
        tighten.c2.journal_counts(jtext.encode())
    return _entry(g, sorted(receipts), obs, jline, gates)


def _finish(g, ids, gates, obs):
    g[LES] = ("# round 41\n\n## Gate\n\n" + "\n".join(gates) + "\n" +
              ctl.ADMIT + "\n" + ctl.REFUSE + "\n")
    head = ["# focus grab", ""] + ["source: %s - x" % i for i, _l, _k in ids] \
        + ["verified-at: 2026-10-25", "recheck: 90d", ""]
    g[ENTRY] = "\n".join(head + obs + ["", ""]) + "\n"
    g["corpus/README.md"] += \
        "| `knowledge/hyprland-focus-grab-r41.md` | new |\n"
    return g, None


def _rebuild(g, gates, obs, jline, extra_src=None):
    g[LES] = ("# round 41\n\n## Gate\n\n" + "\n".join(gates) + "\n" +
              ctl.ADMIT + "\n" + ctl.REFUSE + "\n")
    ids = [l.split()[1] for l in g[ENTRY].splitlines()
           if l.startswith("source: ")]
    head = ["# Hyprland focus grab (forged)", ""] + \
        ["source: %s - x" % i for i in ids] + \
        ["verified-at: 2026-10-25", "recheck: 90d", ""]
    g[ENTRY] = "\n".join(head + obs + ["", jline, ""]) + "\n"
    return g, jline


# --------------------------------------------------------------------- runner
def run(base, after):
    d = tempfile.mkdtemp(prefix="mado-c2forge-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True,
                       env=ctl.ENV)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             check=True, capture_output=True, text=True,
                             env=ctl.ENV).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit("fixture toplevel mismatch: %s != %s" % (top, d))
        b = ctl.commit_all(d, base, "base")
        a = ctl.commit_all(d, after, "after")
        p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", d,
                            "--rev", a, "--base", b],
                           capture_output=True, text=True, env=ctl.ENV)
        lines = p.stdout.strip().splitlines()
        cls = [l for l in lines if " clauses=" in l]
        clauses = cls[0].split(" clauses=")[1].split(" admitted")[0] \
            if cls else "-"
        last = lines[-1] if lines else "NO-OUTPUT"
        tg = tighten.check(d, a, b)
        single = {t: tighten.check(d, a, b, [t])[t]
                  for t in ("T1", "T2", "T3", "T4", "T5", "T6", "T7")}
        sizes = {rel: len(t.encode()) for rel, t in after.items()
                 if base.get(rel) != t}
        return {"rc": p.returncode,
                "verdict": last.split(": ", 1)[-1].split(" rev=")[0],
                "clauses": clauses,
                "tighten": {k: v for k, v in tg.items()},
                "single": single,
                "new_bytes": sum(sizes.values()),
                "sizes": sizes,
                "stderr": p.stderr.strip()[:400]}
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    base = ctl.base_files()
    ggen, jline = genuine()
    fixtures = [("GENUINE-PROXY", base, ggen)]
    for name, fn in (("F1-invented-receipts-512", f1_invented_512),
                     ("F2-invented-journal", f2_invented_journal),
                     ("F3-absent-package-paths", f3_absent_package),
                     ("F3b-space-only-refuse-reason", f3b_space_reason),
                     ("F4-localized-redirect", f4_localized_redirect),
                     ("F5-shared-boilerplate-quote", f5_shared_boilerplate),
                     ("F6-one-char-location", f6_one_char_location)):
        files, _jl = fn()
        fixtures.append((name, base, files))
    base7 = base_two_held()
    files7, _jl7 = f7_two_new_ids(base7)
    fixtures.append(("F7-two-new-ids", base7, files7))
    out = {}
    for name, b, a in fixtures:
        r = run(b, a)
        out[name] = r
        bad = [t for t, v in r["tighten"].items() if v]
        print("%-28s rc=%d %-34s new_bytes=%-6d tighten_fail=%s" % (
            name, r["rc"], r["verdict"], r["new_bytes"],
            ",".join(sorted(bad)) or "none"))
    with open(os.path.join(HERE, "forgeries.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    ok = (out["GENUINE-PROXY"]["rc"] == 0
          and not any(out["GENUINE-PROXY"]["tighten"].values())
          and all(v["rc"] == 0 for k, v in out.items()
                  if k != "GENUINE-PROXY"))
    print("")
    print("single-tightening matrix (X = refused by that tightening alone):")
    print("%-28s %s" % ("fixture", "  ".join("T%d" % i for i in range(1, 8))))
    for name in out:
        row = ["X " if out[name]["single"]["T%d" % i] else ". "
               for i in range(1, 8)]
        print("%-28s %s" % (name, "  ".join(row)))
    print("FORGE_SUMMARY fixtures=%d admitted=%d/%d genuine_proxy_clean=%d"
          % (len(out), sum(1 for v in out.values() if v["rc"] == 0),
             len(out), int(ok)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
