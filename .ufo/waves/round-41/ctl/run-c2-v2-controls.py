#!/usr/bin/env python3
"""Round-41 C2 v2 controls: PRED-C2-r41-v2 scored over synthetic fixture repos.

Fixture repos are `D=$(mktemp -d)` with every git call naming `-C D`, the
throwaway identity passed with -c (never written to any config), the toplevel
verified equal to D before the first commit. The genuine fixture G cites the
REAL pre-wave receipts (fetch/) with real quotes and the real journal census;
the held id S050 is synthetic. Two scorers:
  real     the counter as frozen (PINS bind every NEW id's receipt) - used for
           control P, the forgeries (F*) and the receipt-substitution mutants (Z*);
  patched  a copy of the counter whose PINS also hold the fixture's own receipts
           - so a clause mutant is killed by ITS clause, not by the pin.
Control P must score 1/1; every other control must score 0/1.
Final line: `CTL_C2V2: controls=N correct=K/N`.
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
COUNTER = os.path.join(LANE, "quality", "counters", "c2-r41-focus-entry-v2.py")
FETCHDIR = os.path.join(LANE, ".ufo", "waves", "round-41", "fetch")
ENTRY = "corpus/knowledge/hyprland-focus-grab-r41.md"
PKG = "merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md"
PKG2 = "merge/mado/knowledge/corpus/knowledge/privileged-client-surface-r29.md"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
SRC = "corpus/SOURCES.md"
LES = "corpus/lessons/round-41.md"
FETCH = ".ufo/waves/round-41/fetch/"
FG = "hyprland_focus_grab_manager_v1"

# id -> (receipt file, kind, location, quote)
REAL = {
    "S283": ("focus-grab-v1.xml", "docs", "https://example.org/hyprland-focus-grab-v1.xml",
             "clear the whitelist, rendering the grab inert and sending the cleared"),
    "S284": ("Hyprland-FocusGrab.cpp", "code", "https://example.org/src/protocols/FocusGrab.cpp",
             "Ensure new surfaces are focused if under the mouse when committed."),
    "S285": ("quickshell-grab.cpp", "code", "https://example.org/focus_grab/grab.cpp",
             "the protocol will always send cleared() when the grab is deactivated,"),
    "S286": ("xdph-PortalManager.cpp", "code", "https://example.org/src/core/PortalManager.cpp",
             'Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);'),
    "S287": ("issue-565.html", "docs", "https://example.org/issues/565",
             "New windows in inactive workspaces stealing focus"),
    "S288": ("protocols-README.md", "docs", "https://example.org/hyprland-protocols/README.md",
             "Wayland protocol extensions for Hyprland."),
    "S289": ("xdph-journal.txt", "own-work", ".ufo/waves/round-41/fetch/xdph-journal.txt",
             "Got interface: hyprland_focus_grab_manager_v1 (ver 1)"),
}
HELD_Q = "handlers and gradients keep the previous angle"
FILLER = ("The census walked the host journal and asked the portal for every "
          "advertised interface once. " * 8)
JBYTES = open(os.path.join(FETCHDIR, "xdph-journal.txt"), "rb").read()
JLINE = "journal sessions=2 adverts=78 interfaces=63 focus_grab=1"


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def blob(fn):
    return open(os.path.join(FETCHDIR, fn), "rb").read()


HELD_ROW = ("| S050 | held hyprlang config source - https://example.org/config.cpp "
            "| code | A | scope | anchor | teaches | mined | 2026-10-24 | "
            "on-change | corpus/knowledge/old.md |")


def row(i, loc, used=ENTRY, status="mined", opened="2026-10-25", kind="docs",
        recheck="90d"):
    return ("| %s | title - %s | %s | A | scope | anchor | teaches | %s | %s "
            "| %s | %s |" % (i, loc, kind, status, opened, recheck, used))


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


def gate_line(i, path, data, quote):
    return 'GATE %s receipt=%s sha256=%s quote="%s"' % (i, path, sha(data), quote)


ADMIT = "ADMIT %s as %s" % (PKG, ENTRY)
REFUSE = ("REFUSE %s reason=generic wayland security analysis, not a "
          "measurement of this compositor" % PKG2)


def admitted():
    g = base_files()
    held = HELD_ROW.replace("corpus/knowledge/old.md",
                            "corpus/knowledge/old.md, " + ENTRY)
    rows = [held]
    gates = []
    g[FETCH + "S050.txt"] = ("%s source bytes for S050. %s\n" % (HELD_Q, FILLER)).encode()
    gates.append(gate_line("S050", FETCH + "S050.txt", g[FETCH + "S050.txt"], HELD_Q))
    for i, (fn, kind, loc, q) in REAL.items():
        rows.append(row(i, loc, kind=kind))
        g[FETCH + fn] = blob(fn)
        gates.append(gate_line(i, FETCH + fn, g[FETCH + fn], q))
    g[SRC] = g[SRC].replace(HELD_ROW, "\n".join(rows))
    g[LES] = ("# round 41\n\n## Gate\n\n" + "\n".join(gates) + "\n" + ADMIT
              + "\n" + REFUSE + "\n")
    body = ["# The focus-grab protocol", "",
            "source: S050 - held parser", "source: S283 - protocol xml",
            "source: S284 - compositor", "source: S285 - client",
            "source: S286 - portal", "source: S287 - tracker",
            "source: S288 - readme", "source: S289 - own-work journal",
            "verified-at: 2026-10-25", "recheck: 90d", "",
            "**OBS** S050 %s." % HELD_Q]
    for i, (fn, kind, loc, q) in REAL.items():
        body.append("**OBS** %s %s." % (i, q))
    body += ["", JLINE, ""]
    g[ENTRY] = "\n".join(body) + "\n"
    g["corpus/README.md"] += "| `knowledge/hyprland-focus-grab-r41.md` | new |\n"
    return g


def set_receipt(g, i, fn, data, quote=None):
    data = data if isinstance(data, bytes) else data.encode()
    g[FETCH + fn] = data
    old = [l for l in g[LES].splitlines() if l.startswith("GATE %s " % i)][0]
    q = quote or (REAL[i][3] if i in REAL else HELD_Q)
    g[LES] = g[LES].replace(old, gate_line(i, FETCH + fn, data, q))


def rep(g, key, old, new, count=1):
    assert old in g[key], (key, old[:50])
    g[key] = g[key].replace(old, new, count)


def mutants(base, G):
    m = {}

    def mut(name, fn, kind="patched"):
        g = dict(G)
        fn(g)
        m[name] = (kind, g)
    q = {i: REAL[i][3] for i in REAL}
    # --- paperwork mutants (killed by their own clause under the patched counter)
    mut("N01-no-entry", lambda g: g.pop(ENTRY))
    mut("N02-entry-no-rows", lambda g: g.__setitem__(SRC, base[SRC]))
    mut("N03-gate-sha-wrong", lambda g: rep(g, LES, sha(blob("focus-grab-v1.xml")), "0" * 64))
    mut("N04-quote-absent", lambda g: set_receipt(
        g, "S288", "protocols-README.md", "<html>nothing here " + FILLER + "</html>"))
    long_q = " ".join("w%d" % i for i in range(26))
    mut("N05-quote-26-words", lambda g: (
        set_receipt(g, "S288", "protocols-README.md", long_q + " " + FILLER, long_q),
        rep(g, ENTRY, q["S288"], long_q)))
    mut("N06-no-index-row", lambda g: g.__setitem__("corpus/README.md", base["corpus/README.md"]))

    def two_new(g):
        t = g[SRC]
        for i in ("S283", "S284", "S285", "S286", "S287"):
            r = row(i, REAL[i][2], kind=REAL[i][1])
            t = t.replace(r + "\n", "").replace(r, "")
        g[SRC] = t
    mut("N07-two-new-ids-left", two_new)
    mut("N08-held-row-rewritten", lambda g: rep(g, SRC, "| teaches | mined | 2026-10-24", "| REWRITTEN | mined | 2026-10-24"))
    mut("N09-duplicate-location", lambda g: rep(g, SRC, REAL["S284"][2], REAL["S283"][2]))
    mut("N10-entry-line-lacks-quote", lambda g: rep(g, ENTRY, "**OBS** S283 %s." % q["S283"], "**OBS** S283 x."))
    mut("N11-wrong-verified-at", lambda g: rep(g, ENTRY, "verified-at: 2026-10-25", "verified-at: 2026-10-23"))
    mut("N13-status-candidate", lambda g: rep(g, SRC, "| teaches | mined | 2026-10-25", "| teaches | candidate | 2026-10-25"))
    mut("N15-no-own-work-row", lambda g: rep(g, SRC, "| own-work |", "| docs |"))
    mut("N16-used-by-missing", lambda g: rep(g, SRC, "| 90d | %s |" % ENTRY, "| 90d | corpus/knowledge/other.md |"))
    mut("X03-journal-line-in-prose", lambda g: rep(g, ENTRY, JLINE + "\n", "The census said %s.\n" % JLINE))
    mut("X05-usedby-longer-path", lambda g: rep(g, SRC, row("S283", REAL["S283"][2], kind="docs"),
                                                  row("S283", REAL["S283"][2], kind="docs", used=ENTRY + ".draft-copy.md")))
    mut("X07-index-row-in-fence", lambda g: g.__setitem__("corpus/README.md", base["corpus/README.md"] + "```\n| `knowledge/hyprland-focus-grab-r41.md` | new |\n```\n"))
    mut("X11-gate-lines-indented", lambda g: g.__setitem__(LES, g[LES].replace("GATE ", "  GATE ")))
    mut("X13-dual-gate-stale-first", lambda g: rep(g, LES, "## Gate\n\n", "## Gate\n\nGATE S283 receipt=.ufo/waves/round-40/fetch/S283.txt sha256=%s quote=\"%s\"\n" % ("0" * 64, q["S283"])))
    mut("X14-new-id-opened-stale", lambda g: rep(g, SRC, row("S283", REAL["S283"][2], kind="docs"),
                                                   row("S283", REAL["S283"][2], kind="docs", opened="2026-10-24")))
    # --- journal clause
    jn = jcounts(JBYTES)
    mut("J01-entry-adverts-off-by-one", lambda g: rep(g, ENTRY, "adverts=78", "adverts=79"))
    mut("J09-sessions-claimed-3", lambda g: rep(g, ENTRY, "sessions=2", "sessions=3"))
    mut("J10-journal-line-absent", lambda g: rep(g, ENTRY, JLINE + "\n", ""))
    mut("J07-two-journal-lines", lambda g: g.__setitem__(ENTRY, g[ENTRY] + JLINE + "\n"))
    mut("J08-journal-line-in-fence", lambda g: rep(g, ENTRY, JLINE + "\n", "```\n" + JLINE + "\n```\n"))

    def with_journal(g, text, line):
        set_receipt(g, "S289", "xdph-journal.txt", text)
        rep(g, ENTRY, JLINE, line)
    jt = JBYTES.decode()
    mut("J02-single-session", lambda g: with_journal(g, "\n".join(jt.split("\n")[116:]) + "\n", jline(jt.split("\n")[116:])))
    mut("J03-no-focus-grab-advert", lambda g: with_journal(g, jt.replace(FG, "hyprland_focus_grab_manager_vX"), jline(jt.replace(FG, "hyprland_focus_grab_manager_vX").split("\n"))))
    mut("J11-other-level-adverts", lambda g: with_journal(g, jt.replace("[LOG]", "[ERR]"), JLINE))
    mut("J16-no-boot-line", lambda g: with_journal(g, re.sub(r"^-- Boot .*\n", "", jt, flags=re.M), JLINE))
    mut("J17-sessions-replayed", lambda g: with_journal(g, replayed(jt), jline(replayed(jt).split("\n"))))
    # --- the assimilation clause
    mut("A01-no-admit-line", lambda g: rep(g, LES, ADMIT + "\n", ""))
    mut("A02-no-refuse-line", lambda g: rep(g, LES, REFUSE + "\n", ""))
    mut("A03-admit-names-other-entry", lambda g: rep(g, LES, " as " + ENTRY, " as corpus/knowledge/other.md"))
    mut("A04-refuse-reason-one-word", lambda g: rep(g, LES, "reason=generic wayland security analysis, not a measurement of this compositor", "reason=generic"))
    mut("A05-localized-channel-source", lambda g: rep(g, SRC, REAL["S288"][2], "https://amgsk.dev/posts/hyprland-rules/"))
    mut("A06-admit-nonexistent-package", lambda g: rep(g, LES, PKG, "merge/mado/knowledge/corpus/knowledge/does-not-exist.md"))
    mut("A07-refuse-nonexistent-package", lambda g: rep(g, LES, PKG2, "merge/mado/knowledge/corpus/knowledge/does-not-exist.md"))
    mut("A08-refuse-equals-admit", lambda g: rep(g, LES, PKG2, PKG))
    mut("A09-refuse-reason-filler", lambda g: rep(g, LES, "reason=generic wayland security analysis, not a measurement of this compositor", "reason=x x x x x x x x x x x x x x x x x x x x"))
    mut("A10-admit-line-in-fence", lambda g: rep(g, LES, ADMIT + "\n", "```\n" + ADMIT + "\n```\n"))
    mut("A11-gate-line-in-fence", lambda g: rep(g, LES, [l for l in g[LES].splitlines() if l.startswith("GATE S288")][0],
                                                  "```\n" + [l for l in g[LES].splitlines() if l.startswith("GATE S288")][0] + "\n```"))
    # --- wave survivors (ExecC2ExtraMutants, RevC2Counter)
    mut("W01-citation-past-line-20", lambda g: g.__setitem__(ENTRY, g[ENTRY].replace("verified-at: 2026-10-25", "\n".join("pad %d" % i for i in range(14)) + "\nverified-at: 2026-10-25")))
    mut("W02-lowercase-id", lambda g: rep(g, ENTRY, "source: S288 - readme", "source: s288 - readme"))
    mut("W03-ghost-id-in-body", lambda g: g.__setitem__(ENTRY, g[ENTRY] + "**OBS** S999 an invented citation.\n"))
    mut("W04-source-after-line-20", lambda g: g.__setitem__(ENTRY, g[ENTRY] + "source: S288 - again\n"))
    mut("W05-verified-at-in-fence", lambda g: rep(g, ENTRY, "verified-at: 2026-10-25", "```\nverified-at: 2026-10-25\n```\nverified-at: 2026-10-23"))
    mut("W06-source-line-in-fence", lambda g: rep(g, ENTRY, "source: S288 - readme", "```\nsource: S288 - readme\n```"))
    mut("W07-recheck-tbd", lambda g: rep(g, SRC, row("S283", REAL["S283"][2], kind="docs"), row("S283", REAL["S283"][2], kind="docs", recheck="TBD")))
    mut("W08-recheck-bad-date", lambda g: rep(g, SRC, row("S283", REAL["S283"][2], kind="docs"), row("S283", REAL["S283"][2], kind="docs", recheck="2026-99-99")))
    mut("W09-row-without-location", lambda g: rep(g, SRC, "title - " + REAL["S283"][2], "title - surfaces"))
    mut("W10-held-row-loses-usedby", lambda g: rep(g, SRC, "corpus/knowledge/old.md, " + ENTRY, ENTRY))
    mut("W11-one-line-two-ids", lambda g: rep(g, ENTRY, "**OBS** S283 %s." % q["S283"], "**OBS** S283 S284 %s." % q["S283"]))
    mut("W12-quote-whitespace-distinct", lambda g: (
        set_receipt(g, "S288", "protocols-README.md", blob("protocols-README.md"), "Wayland  protocol extensions for Hyprland."),
        rep(g, ENTRY, q["S288"], "Wayland  protocol extensions for Hyprland."),
        set_receipt(g, "S283", "focus-grab-v1.xml", blob("focus-grab-v1.xml"), "Wayland protocol extensions for Hyprland.")) and None)
    mut("W13-location-fragment-duplicate", lambda g: rep(g, SRC, REAL["S288"][2], REAL["S283"][2] + "#frag"))
    def w14(g):
        target = "Wayland protocol extensions for Hyprland. " + FILLER
        set_receipt(g, "S288", "protocols-README.md", target)
        g["__symlink__"] = FETCH + "protocols-README.md"
    mut("W14-symlink-receipt", w14)
    mut("W15-quote-in-two-receipts", lambda g: set_receipt(
        g, "S288", "protocols-README.md", blob("protocols-README.md") + b"\nclear the whitelist, rendering the grab inert and sending the cleared\n",
        "clear the whitelist, rendering the grab inert and sending the cleared") or rep(g, ENTRY, q["S288"], "clear the whitelist, rendering the grab inert and sending the cleared"))
    mut("W16-quote-across-html-blocks", lambda g: (
        set_receipt(g, "S287", "issue-565.html", "<html><p>New windows in inactive</p><p>workspaces stealing focus</p>" + FILLER + "</html>")))
    mut("W17-quote-only-after-entity-decode", lambda g: set_receipt(
        g, "S288", "protocols-README.md", "Wayland protocol extensions for Hyprland. &amp;amp; " + FILLER, "Wayland protocol extensions for Hyprland. & " + "x"))
    # --- forgeries against the REAL counter (the pins)
    shared = ("shared receipt text with one quotable sentence " + FILLER).encode()

    def f1(g):
        for i in ("S283", "S284", "S285"):
            fn = REAL[i][0]
            set_receipt(g, i, fn, ("invented %s receipt with a quotable sentence %s " % (i, i) + FILLER), "quotable sentence %s" % i)
            rep(g, ENTRY, REAL[i][3], "quotable sentence %s" % i)
    mut("F1-invented-receipts", f1, kind="real")

    def f2(g):
        fake = "\n".join(["-- Boot %032x --" % 1] + ["2026-10-25T13:%02d:00-03:00 h xdg-desktop-portal-hyprland[10%d]: [LOG]  | Got interface: iface_%d (ver 1)" % (k % 60, s_, k) for s_ in (1, 2) for k in range(30)]
                         + ["2026-10-25T13:59:00-03:00 h xdg-desktop-portal-hyprland[102]: [LOG]  | Got interface: %s (ver 1)" % FG]) + "\n"
        set_receipt(g, "S289", "xdph-journal.txt", fake, "Got interface: %s (ver 1)" % FG)
        rep(g, ENTRY, JLINE, jline(fake.split("\n")))
    mut("F2-invented-journal", f2, kind="real")
    mut("F3-unpinned-quote-boilerplate", lambda g: [set_receipt(g, i, REAL[i][0], blob(REAL[i][0]) + b"\n" + shared) for i in ("S283", "S284")], kind="real")
    mut("F4-localized-redirect", lambda g: rep(g, SRC, REAL["S288"][2], "https://t.co/9xQ2fG"))
    mut("F5-receipt-renamed", lambda g: g.__setitem__(FETCH + "other-name.txt", g.pop(FETCH + "protocols-README.md")) or rep(g, LES, FETCH + "protocols-README.md", FETCH + "other-name.txt"), kind="real")
    mut("F6-one-char-location", lambda g: rep(g, SRC, REAL["S283"][2], REAL["S283"][2].replace("focus", "focuz")), kind="real")
    mut("Z1-pinned-receipt-edited-byte", lambda g: set_receipt(g, "S284", "Hyprland-FocusGrab.cpp", blob("Hyprland-FocusGrab.cpp") + b"\n// edited\n"), kind="real")
    return m


def jcounts(b):
    return jline(b.decode().split("\n"))


def jline(lines):
    ad = re.compile(r"\S+ \S+ xdg-desktop-portal-hyprland\[(\d+)\]: \[LOG\]  \| "
                    r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver \d{1,6}\)")
    sess, boot, cur = [], False, None
    for l in lines:
        if re.fullmatch(r"-- Boot [0-9a-f]{32} --", l):
            boot = True
            continue
        mm = ad.fullmatch(l)
        if not mm:
            continue
        if cur is None or boot or cur["pid"] != mm.group(1):
            cur = {"pid": mm.group(1), "n": 0, "names": {}}
            sess.append(cur)
            boot = False
        cur["n"] += 1
        cur["names"][mm.group(2)] = cur["names"].get(mm.group(2), 0) + 1
    return "journal sessions=%d adverts=%d interfaces=%d focus_grab=%d" % (
        len(sess), sum(x["n"] for x in sess), len(sess[-1]["names"]),
        sess[-1]["names"].get(FG, 0))


def replayed(jt):
    lines = jt.split("\n")
    tail = [l for l in lines[117:] if l]
    return jt + "-- Boot %032x --\n" % 7 + "\n".join(tail) + "\n"


def commit_all(d, files, msg):
    links = {}
    for rel, data in files.items():
        if rel == "__symlink__":
            links[data] = True
            continue
        path = os.path.join(d, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(data if isinstance(data, bytes) else data.encode())
    for rel in links:
        path = os.path.join(d, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = open(path, "rb").read()
        os.unlink(path)
        os.symlink(data.decode("utf-8"), path)
    ident = ["-c", "user.name=ctl", "-c", "user.email=ctl@ctl.invalid"]
    subprocess.run(["git", "-C", d, "add", "-A"], check=True, env=ENV)
    subprocess.run(["git", "-C", d, *ident, "commit", "-q", "-m", msg,
                    "--no-gpg-sign"], check=True, env=ENV)
    return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True,
                          env=ENV).stdout.strip()


def patched_counter(dest, files):
    src = open(COUNTER).read()
    extra = "".join('    "%s": "%s",\n' % (os.path.basename(k), sha(v))
                    for k, v in files.items()
                    if k.startswith(FETCH) and not isinstance(v, bool))
    assert "PINS = {\n" in src
    src = src.replace("PINS = {\n", "PINS = {\n" + extra, 1)
    path = os.path.join(dest, "c2-patched.py")
    open(path, "w").write(src)
    return path


def score(files_base, files_after, kind):
    d = tempfile.mkdtemp(prefix="mado-c2v2ctl-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=ENV)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             check=True, capture_output=True, text=True,
                             env=ENV).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit("fixture toplevel mismatch: %s != %s" % (top, d))
        b = commit_all(d, files_base, "base")
        a = commit_all(d, files_after, "after")
        counter = COUNTER if kind == "real" else patched_counter(
            tempfile.mkdtemp(prefix="c2p-"), files_after)
        p = subprocess.run([sys.executable, "-I", counter, "--repo", d,
                            "--rev", a, "--base", b],
                           capture_output=True, text=True, env=ENV)
        lines = p.stdout.strip().splitlines()
        cls = [l for l in lines if " clauses=" in l]
        clauses = cls[0].split(" clauses=")[1].split(" admitted")[0] if cls else "-"
        last = lines[-1] if lines else "NO-OUTPUT " + p.stderr[-120:]
        return p.returncode, last.split(": ", 1)[-1].split(" rev=")[0], clauses
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    base = base_files()
    G = admitted()
    m = mutants(base, G)
    results = []
    for kind in ("real", "patched"):
        rc, last, cls = score(base, G, kind)
        ok = rc == 0 and "admitted=1/1" in last
        print("control=P-%s expected=admitted=1/1 observed=%s clauses=%s ok=%d"
              % (kind, last, cls, ok))
        results.append(ok)
    for name, (kind, g) in sorted(m.items()):
        rc, last, cls = score(base, g, "real" if kind == "real" else "patched")
        ok = rc == 1 and "admitted=0/1" in last
        results.append(ok)
        print("control=%s scorer=%s expected=admitted=0/1 observed=%s clauses=%s ok=%d"
              % (name, "real" if kind == "real" else "patched",
                 last.split(" verdict")[0], cls, ok))
    n = len(results)
    print("CTL_C2V2: controls=%d correct=%d/%d" % (n, sum(results), n))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
