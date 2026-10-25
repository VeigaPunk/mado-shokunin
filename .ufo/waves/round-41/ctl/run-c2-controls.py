#!/usr/bin/env python3
"""Round-41 C2 controls: PRED-C2-r41-v1 scored over synthetic fixture repos.

Fixture repos are `D=$(mktemp -d)` with every git call naming `-C D`, the
throwaway identity passed with -c (never written to any config), the toplevel
verified equal to D before the first commit. Control P (a fabricated
self-consistent set) must score 1/1 (the declared residual); every mutant must
score 0/1. Final line: `CTL_C2: controls=N correct=K/N`.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
COUNTER = os.path.join(LANE, "quality", "counters", "c2-r41-focus-entry.py")
ENTRY = "corpus/knowledge/hyprland-focus-grab-r41.md"
PKG = "merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md"
PKG2 = "merge/mado/knowledge/corpus/knowledge/privileged-client-surface-r29.md"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
SRC = "corpus/SOURCES.md"
LES = "corpus/lessons/round-41.md"
FETCH = ".ufo/waves/round-41/fetch/"
FG = "hyprland_focus_grab_manager_v1"
FILLER = ("The census walked the host journal and asked the portal for every "
          "advertised interface once. " * 8)


def advert(ts, pid, name, ver=1):
    return ("%s h xdg-desktop-portal-hyprland[%s]: [LOG]  | Got interface: "
            "%s (ver %d)" % (ts, pid, name, ver))


def journal(sessions=3, per=24, focus=True, boots=True, pid_change=True):
    lines = []
    for s in range(sessions):
        if boots:
            lines.append("-- Boot %032x --" % (s + 1))
        pid = str(1900 + (s if pid_change else 0))
        for k in range(per):
            name = "iface_%d" % k
            if focus and k == 3:
                name = FG
            lines.append(advert("2026-10-25T13:%02d:00-03:00" % (10 + s), pid,
                                name))
    return "\n".join(lines) + "\n"


def jcounts(text):
    """The runner's own parse (a second implementation of the grammar)."""
    ad = re.compile(r"\S+ \S+ xdg-desktop-portal-hyprland\[(\d+)\]: \[LOG\]  \| "
                    r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver \d{1,6}\)")
    sess, boot, cur = [], False, None
    for l in text.split("\n"):
        if re.fullmatch(r"-- Boot [0-9a-f]{32} --", l):
            boot = True
            continue
        m = ad.fullmatch(l)
        if not m:
            continue
        if cur is None or boot or cur["pid"] != m.group(1):
            cur = {"pid": m.group(1), "n": 0, "names": {}}
            sess.append(cur)
            boot = False
        cur["n"] += 1
        cur["names"][m.group(2)] = cur["names"].get(m.group(2), 0) + 1
    return (len(sess), sum(x["n"] for x in sess), len(sess[-1]["names"]),
            sess[-1]["names"].get(FG, 0))


def jline(text):
    return "journal sessions=%d adverts=%d interfaces=%d focus_grab=%d" % jcounts(text)


JTEXT = journal()
JLINE = jline(JTEXT)
QUOTES = {
    "S050": "handlers and gradients keep the previous angle",
    "S301": "hyprland focus grab manager interface commit request",
    "S302": "advertised interface census over the host journal",
    "S303": "quickshell grab sync after cleared event",
    "S304": "the compositor ships a focus limiting protocol",
}


def receipt_text(i):
    if i == "S302":
        return JTEXT + "\n# " + QUOTES[i] + "\n"
    return "%s source bytes for %s. %s\n" % (QUOTES[i], i, FILLER)


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


HELD_ROW = ("| S050 | held hyprlang config source - https://example.org/config.cpp "
            "| code | A | scope | anchor | teaches | mined | 2026-10-24 | "
            "on-change | corpus/knowledge/old.md |")


def row(i, loc, used=ENTRY, status="mined", opened="2026-10-25", kind="docs"):
    return ("| %s | title - %s | %s | A | scope | anchor | teaches | %s | %s "
            "| 90d | %s |" % (i, loc, kind, status, opened, used))


def base_files():
    f = {}
    f[SRC] = "\n".join([
        "# Sources", "", "## Registry", "",
        "| id | source | kind | tier | scope | anchor | teaches | status | "
        "opened | recheck | used-by |",
        "|---|---|---|---|---|---|---|---|---|---|---|", HELD_ROW, "",
        "## Paths", ""]) + "\n"
    f["corpus/README.md"] = "# Coverage\n\n| `knowledge/old.md` | old |\n"
    f["corpus/knowledge/old.md"] = "old\n"
    return f


def gate_line(i, path, text, quote):
    return 'GATE %s receipt=%s sha256=%s quote="%s"' % (
        i, path, sha(text), quote)


ADMIT = "ADMIT %s as %s" % (PKG, ENTRY)
REFUSE = "REFUSE %s reason=generic wayland security analysis, not a measurement" % PKG2


def admitted():
    g = base_files()
    held = HELD_ROW.replace("corpus/knowledge/old.md",
                            "corpus/knowledge/old.md, " + ENTRY)
    new = [row("S301", "https://example.org/a.xml"),
           row("S302", ".ufo/waves/round-41/fetch/S302.journal.txt",
               kind="own-work"),
           row("S303", "https://example.org/c.cpp"),
           row("S304", "https://example.org/d.md")]
    g[SRC] = g[SRC].replace(HELD_ROW, held + "\n" + "\n".join(new))
    gates = []
    paths = {"S050": "S050.txt", "S301": "S301.html",
             "S302": "S302.journal.txt", "S303": "S303.txt",
             "S304": "S304.txt"}
    for i, fn in paths.items():
        g[FETCH + fn] = receipt_text(i)
        gates.append(gate_line(i, FETCH + fn, receipt_text(i), QUOTES[i]))
    g[LES] = ("# round 41\n\n## Gate\n\n" + "\n".join(gates) + "\n" + ADMIT
              + "\n" + REFUSE + "\n")
    g[ENTRY] = "\n".join([
        "# The focus-grab protocol", "",
        "source: S050 - held parser", "source: S301 - protocol xml",
        "source: S302 - own-work journal", "source: S303 - client source",
        "source: S304 - docs", "verified-at: 2026-10-25", "recheck: 90d", "",
        "**OBS** S050 %s." % QUOTES["S050"],
        "**OBS** S301 %s." % QUOTES["S301"],
        "**OBS** S302 %s." % QUOTES["S302"],
        "**OBS** S303 %s." % QUOTES["S303"],
        "**OBS** S304 %s." % QUOTES["S304"], "", JLINE, ""]) + "\n"
    g["corpus/README.md"] += "| `knowledge/hyprland-focus-grab-r41.md` | new |\n"
    return g


def set_receipt(g, i, fn, text, quote=None):
    g[FETCH + fn] = text
    old = [l for l in g[LES].splitlines() if l.startswith("GATE %s " % i)][0]
    q = quote or QUOTES[i]
    g[LES] = g[LES].replace(old, gate_line(i, FETCH + fn, text, q))


def with_journal(g, text, line=None):
    set_receipt(g, "S302", "S302.journal.txt",
                text + "\n# " + QUOTES["S302"] + "\n")
    g[ENTRY] = g[ENTRY].replace(JLINE, line if line is not None else jline(text))


def mutants(base, G):
    m = {}

    def mut(name, fn):
        g = dict(G)
        fn(g)
        m[name] = g
    mut("N01-no-entry", lambda g: g.pop(ENTRY))
    mut("N02-entry-no-rows", lambda g: g.__setitem__(SRC, base[SRC]))
    mut("N03-gate-sha-wrong", lambda g: g.__setitem__(
        LES, g[LES].replace(sha(receipt_text("S301")), "0" * 64)))
    mut("N04-quote-absent", lambda g: g.__setitem__(
        FETCH + "S301.html", "<html>nothing here " + FILLER + "</html>"))
    long_q = " ".join("w%d" % i for i in range(26))
    mut("N05-quote-26-words", lambda g: set_receipt(
        g, "S303", "S303.txt", long_q + " " + FILLER, long_q) or g.__setitem__(
        ENTRY, g[ENTRY].replace(QUOTES["S303"], long_q)))
    mut("N06-no-index-row", lambda g: g.__setitem__(
        "corpus/README.md", base["corpus/README.md"]))

    def two_new(g):
        t = g[SRC]
        for r in (row("S301", "https://example.org/a.xml"),
                  row("S303", "https://example.org/c.cpp"),
                  row("S304", "https://example.org/d.md")):
            t = t.replace(r + "\n", "").replace(r, "")
        g[SRC] = t
    mut("N07-one-new-id-left", two_new)
    mut("N08-held-row-rewritten", lambda g: g.__setitem__(
        SRC, g[SRC].replace("| teaches | mined | 2026-10-24",
                            "| REWRITTEN | mined | 2026-10-24")))
    mut("N09-duplicate-location", lambda g: g.__setitem__(
        SRC, g[SRC].replace("https://example.org/c.cpp",
                            "https://example.org/a.xml")))
    mut("N10-entry-line-lacks-quote", lambda g: g.__setitem__(
        ENTRY, g[ENTRY].replace("**OBS** S301 %s." % QUOTES["S301"],
                                "**OBS** S301 x.")))
    mut("N11-wrong-verified-at", lambda g: g.__setitem__(
        ENTRY, g[ENTRY].replace("verified-at: 2026-10-25",
                                "verified-at: 2026-10-23")))
    mut("N12-staged-ids-as-is", lambda g: g.__setitem__(
        ENTRY, g[ENTRY].replace("S301", "S228").replace("S303", "S231")))
    mut("N13-status-candidate", lambda g: g.__setitem__(
        SRC, g[SRC].replace("| teaches | mined | 2026-10-25",
                            "| teaches | candidate | 2026-10-25")))
    mut("N14-receipt-outside-fetch-with-bytes", lambda g: (
        g.__setitem__("corpus/receipts/S301.html", receipt_text("S301")),
        g.__setitem__(LES, g[LES].replace(FETCH + "S301.html",
                                          "corpus/receipts/S301.html"))))
    mut("N15-no-own-work-row", lambda g: g.__setitem__(
        SRC, g[SRC].replace("| own-work |", "| docs |")))
    mut("N16-used-by-missing", lambda g: g.__setitem__(
        SRC, g[SRC].replace("| 90d | %s |" % ENTRY,
                            "| 90d | corpus/knowledge/other.md |")))
    mut("X03-journal-line-in-prose", lambda g: g.__setitem__(
        ENTRY, g[ENTRY].replace(JLINE + "\n", "The census said %s.\n" % JLINE)))
    mut("X05-usedby-longer-path", lambda g: g.__setitem__(
        SRC, g[SRC].replace(row("S301", "https://example.org/a.xml"),
                            row("S301", "https://example.org/a.xml",
                                used=ENTRY + ".draft-copy.md"))))

    def x07(g):
        g["corpus/README.md"] = base["corpus/README.md"] + (
            "```\n| `knowledge/hyprland-focus-grab-r41.md` | new |\n```\n")
    mut("X07-index-row-in-fence", x07)
    mut("X11-gate-lines-indented", lambda g: g.__setitem__(
        LES, g[LES].replace("GATE ", "  GATE ")))

    def x13(g):
        stale = ('GATE S303 receipt=.ufo/waves/round-40/fetch/S303.txt '
                 'sha256=%s quote="%s"' % ("0" * 64, QUOTES["S303"]))
        g[LES] = g[LES].replace("## Gate\n\n", "## Gate\n\n" + stale + "\n")
    mut("X13-dual-gate-stale-first", x13)
    mut("X14-new-id-opened-stale", lambda g: g.__setitem__(
        SRC, g[SRC].replace(row("S301", "https://example.org/a.xml"),
                            row("S301", "https://example.org/a.xml",
                                opened="2026-10-24"))))
    shared = "shared receipt text with one quotable sentence " + FILLER

    def cheat_shared(g):
        for i, fn in (("S050", "S050.txt"), ("S301", "S301.html"),
                      ("S303", "S303.txt")):
            set_receipt(g, i, fn, shared, "one quotable sentence")
            g[ENTRY] = g[ENTRY].replace(QUOTES[i], "one quotable sentence")
    mut("Y01-one-receipt-shared-by-ids", cheat_shared)

    def cheat_tiny(g):
        for i, fn in (("S050", "S050.txt"), ("S301", "S301.html"),
                      ("S303", "S303.txt")):
            t = "tiny %s" % i
            set_receipt(g, i, fn, t, "tiny %s x y" % i)
            g[ENTRY] = g[ENTRY].replace(QUOTES[i], "tiny %s x y" % i)
            g[FETCH + fn] = t + " x y"
            set_receipt(g, i, fn, t + " x y", "tiny %s x y" % i)
    mut("Y02-receipts-under-512-bytes", cheat_tiny)
    # --- the journal clause ---
    mut("J01-entry-adverts-off-by-one", lambda g: g.__setitem__(
        ENTRY, g[ENTRY].replace("adverts=%d" % jcounts(JTEXT)[1],
                                "adverts=%d" % (jcounts(JTEXT)[1] + 1))))
    mut("J02-single-session", lambda g: with_journal(
        g, journal(sessions=1)))
    mut("J03-no-focus-grab-advert", lambda g: with_journal(
        g, journal(focus=False)))
    mut("J04-receipt-is-a-tool-report", lambda g: with_journal(
        g, "MADO_GLOBALS_SESSION: n=1 boot=- pid=1 first=x last=y interfaces=30 "
        "adverts=60\n" * 3 + FILLER, JLINE))
    mut("J05-too-few-adverts", lambda g: with_journal(
        g, journal(sessions=2, per=15)))
    mut("J06-too-few-interfaces", lambda g: with_journal(
        g, "\n".join(advert("2026-10-25T13:10:00-03:00", "1900" if s == 0 else "1901",
                            FG if k == 0 else "iface_%d" % (k % 5))
                     for s in range(2) for k in range(30)) + "\n"))
    mut("J07-two-journal-lines", lambda g: g.__setitem__(
        ENTRY, g[ENTRY] + JLINE + "\n"))

    def j08(g):
        g[ENTRY] = g[ENTRY].replace(JLINE + "\n", "```\n" + JLINE + "\n```\n")
    mut("J08-journal-line-in-fence", j08)
    mut("J09-sessions-by-pid-only-claimed", lambda g: g.__setitem__(
        ENTRY, g[ENTRY].replace("sessions=%d" % jcounts(JTEXT)[0],
                                "sessions=%d" % (jcounts(JTEXT)[0] + 1))))
    mut("J10-journal-line-absent", lambda g: g.__setitem__(
        ENTRY, g[ENTRY].replace(JLINE + "\n", "")))
    mut("J11-other-level-adverts", lambda g: with_journal(
        g, JTEXT.replace("[LOG]", "[ERR]"), JLINE))
    # --- the assimilation clause ---
    mut("A01-no-admit-line", lambda g: g.__setitem__(
        LES, g[LES].replace(ADMIT + "\n", "")))
    mut("A02-no-refuse-line", lambda g: g.__setitem__(
        LES, g[LES].replace(REFUSE + "\n", "")))
    mut("A03-admit-names-other-entry", lambda g: g.__setitem__(
        LES, g[LES].replace(" as " + ENTRY, " as corpus/knowledge/other.md")))
    mut("A04-refuse-reason-short", lambda g: g.__setitem__(
        LES, g[LES].replace("reason=generic wayland security analysis, not a "
                            "measurement", "reason=generic")))
    mut("A05-localized-channel-source", lambda g: g.__setitem__(
        SRC, g[SRC].replace("https://example.org/d.md",
                            "https://amgsk.dev/posts/hyprland-rules/")))
    return m


def commit_all(d, files, msg):
    for rel, text in files.items():
        path = os.path.join(d, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="") as fh:
            fh.write(text)
    ident = ["-c", "user.name=ctl", "-c", "user.email=ctl@ctl.invalid"]
    subprocess.run(["git", "-C", d, "add", "-A"], check=True, env=ENV)
    subprocess.run(["git", "-C", d, *ident, "commit", "-q", "-m", msg,
                    "--no-gpg-sign"], check=True, env=ENV)
    return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True,
                          env=ENV).stdout.strip()


def score(files_base, files_after):
    d = tempfile.mkdtemp(prefix="mado-c2r41ctl-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=ENV)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             check=True, capture_output=True, text=True,
                             env=ENV).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit("fixture toplevel mismatch: %s != %s" % (top, d))
        b = commit_all(d, files_base, "base")
        a = commit_all(d, files_after, "after")
        p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", d,
                            "--rev", a, "--base", b],
                           capture_output=True, text=True, env=ENV)
        lines = p.stdout.strip().splitlines()
        cls = [l for l in lines if " clauses=" in l]
        clauses = cls[0].split(" clauses=")[1].split(" admitted")[0] if cls else "-"
        last = lines[-1] if lines else "NO-OUTPUT"
        return p.returncode, last.split(": ", 1)[-1].split(" rev=")[0], clauses
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    base = base_files()
    G = admitted()
    m = mutants(base, G)
    results = []
    rc, last, cls = score(base, G)
    ok = rc == 0 and "admitted=1/1" in last
    print("control=P-fabricated-self-consistent expected=admitted=1/1 "
          "observed=%s clauses=%s ok=%d" % (last, cls, ok))
    results.append(ok)
    for name, g in sorted(m.items()):
        rc, last, cls = score(base, g)
        ok = rc == 1 and "admitted=0/1" in last
        results.append(ok)
        print("control=%s expected=admitted=0/1 observed=%s clauses=%s ok=%d"
              % (name, last.split(" verdict")[0], cls, ok))
    n = len(results)
    print("CTL_C2: controls=%d correct=%d/%d" % (n, sum(results), n))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
