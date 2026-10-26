#!/usr/bin/env python3
"""Round-43 C2 v2 controls: PRED-C2-r43-v2 scored over synthetic fixture repos.

Fixture repos are `D=$(mktemp -d)` with every git call naming `-C D`, the throwaway identity passed
with -c (never written to any config), the toplevel verified equal to D before the first commit. The
genuine fixture G cites the REAL pre-wave receipts (round-43/fetch/) with real quotes and the real host
census lines; the held id S050 is synthetic. Two scorers:
  real     the counter as frozen (PINS bind every NEW id's receipt) - used for control P, the
           forgeries (F*) and the receipt-substitution mutants (Z*);
  patched  a copy of the counter whose PINS also hold the fixture's own receipts - so a clause
           mutant is killed by ITS clause, not by the pin.
Control P must score 1/1; every other control must score 0/1.
Final line: `CTL_C2: controls=N correct=K/N`.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"  # RerunControlsV2: pinned (copy lives off ctl/)
COUNTER = os.path.join(LANE, "quality", "counters", "c2-r43-gkeep-entry-v2.py")
FETCHDIR = os.path.join(LANE, ".ufo", "waves", "round-43", "fetch")
ENTRY = "corpus/knowledge/hyprland-gkeep-geometry-r43.md"
PKG = "merge/mado/knowledge/corpus/knowledge/gkeep-size-to-real-size-r11.md"
PKG2 = "merge/mado/knowledge/corpus/knowledge/gkeep-geometry-unobservable-r8.md"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
SRC = "corpus/SOURCES.md"
LES = "corpus/lessons/round-43.md"
FETCH = ".ufo/waves/round-43/fetch/"
FG = "hyprland_focus_grab_manager_v1"

# id -> (receipt file, kind, location, quote)
REAL = {
    "S290": ("Hyprland-RegexMatchEngine.cpp", "code", "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/matchEngine/RegexMatchEngine.cpp",
             "return re2::RE2::FullMatch(other, *m_regex) != m_negative;"),
    "S291": ("Hyprland-WindowRuleApplicator.cpp", "code", "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/windowRule/WindowRuleApplicator.cpp",
             "static_.size = expr;"),
    "S292": ("Hyprland-DefaultFloatingAlgorithm.cpp", "code", "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp",
             "windowGeometry.w = COMPUTED->x;"),
    "S293": ("Hyprland-Target.cpp", "code", "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/layout/target/Target.cpp", "m_box = box;"),
    "S294": ("Hyprland-WindowTarget.cpp", "code", "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/layout/target/WindowTarget.cpp",
             "if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) { m_window->setBox(m_box.logicalBox);"),
    "S295": ("Hyprland-GeometricMovableAnimated.cpp", "code", "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/types/GeometricMovableAnimated.cpp",
             "*m_realSize = x.size();"),
    "S296": ("Hyprland-HyprCtl.cpp", "code", "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp", '"size": [{}, {}],'),
    "S297": ("host-gkeep.conf", "own-work", ".ufo/waves/round-43/fetch/host-gkeep.conf",
             "windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$"),
    "S298": ("host-clients-r43.json", "own-work", ".ufo/waves/round-43/fetch/host-clients-r43.json", '"mapped": true, "class": "chromium", "floating": false,'),
    "S299": ("gkeep-ui-excerpt.py", "own-work", ".ufo/waves/round-43/fetch/gkeep-ui-excerpt.py",
             "window.set_default_size(420, 500) self.board = Board(window)"),
}
HELD_Q = "handlers and gradients keep the previous angle"
FILLER = ("The census walked the host journal and asked the portal for every "
          "advertised interface once. " * 8)
RULES_LINE = "host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$"
CLIENTS_LINE = "host clients total=4 floating=0 gkeep=0"
UI_LINE = "gkeep request default_size=420x500 application_id=org.omarchy.gkeep"
CENSUS = [RULES_LINE, CLIENTS_LINE, UI_LINE]


def line_of(fn, quote):
    """independent of the counter: 1-based line where the whitespace-collapsed quote starts."""
    raw = blob(fn).decode()
    flat, where = [], []
    prev = True
    for ln, line in enumerate(raw.split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    flat.append(" ")
                    where.append(ln)
                    prev = True
            else:
                flat.append(ch)
                where.append(ln)
                prev = False
    k = "".join(flat).find(re.sub(r"\s+", " ", quote))
    assert k >= 0, (fn, quote)
    return where[k]


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def blob(fn):
    return open(os.path.join(FETCHDIR, fn), "rb").read()


HELD_ROW = ("| S050 | held hyprlang config source - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/config.cpp "
            "| code | A | scope | anchor | teaches | mined | 2026-10-24 | "
            "on-change | corpus/knowledge/old.md |")


def row(i, loc, used=ENTRY, status="mined", opened="2026-10-26", kind="docs",
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
REFUSE = ("REFUSE %s reason=superseded by the source chain and the host census, which settle what it called unobservable" % PKG2)


def entry_line(i):
    fn, kind, loc, q = REAL[i]
    return "**OBS** %s %s (%s:%d)." % (i, q, fn, line_of(fn, q))


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
    g[LES] = ("# round 42\n\n## Gate\n\n" + "\n".join(gates) + "\n" + ADMIT
              + "\n" + REFUSE + "\n")
    body = ["# The gkeep window geometry", "", "source: S050 - held parser"]
    for i in REAL:
        body.append("source: %s - receipt" % i)
    body += ["verified-at: 2026-10-26", "recheck: 90d", "",
             "**OBS** S050 %s (S050.txt:1)." % HELD_Q]
    for i in REAL:
        body.append(entry_line(i))
    body += [""] + CENSUS + [""]
    g[ENTRY] = "\n".join(body) + "\n"
    g["corpus/README.md"] += "| `knowledge/hyprland-gkeep-geometry-r43.md` | new |\n"
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
    EL = {i: entry_line(i) for i in REAL}
    rowof = lambda i, **kw: row(i, REAL[i][2], kind=REAL[i][1], **kw)
    # --- paperwork mutants (killed by their own clause under the patched counter)
    mut("N01-no-entry", lambda g: g.pop(ENTRY))
    mut("N02-entry-no-rows", lambda g: g.__setitem__(SRC, base[SRC]))
    mut("N03-gate-sha-wrong", lambda g: rep(g, LES, sha(blob("Hyprland-Target.cpp")), "0" * 64))
    mut("N04-quote-absent", lambda g: set_receipt(
        g, "S293", "Hyprland-Target.cpp", "<html>nothing here " + FILLER + "</html>"))
    long_q = " ".join("w%d" % i for i in range(26))
    mut("N05-quote-26-words", lambda g: (
        set_receipt(g, "S293", "Hyprland-Target.cpp", long_q + " " + FILLER, long_q),
        rep(g, ENTRY, EL["S293"], "**OBS** S293 %s (Hyprland-Target.cpp:1)." % long_q)))
    mut("N06-no-index-row", lambda g: g.__setitem__("corpus/README.md", base["corpus/README.md"]))

    def two_new(g):
        t = g[SRC]
        for i in ("S290", "S291", "S292", "S293", "S294", "S295", "S296", "S297"):
            r = rowof(i)
            t = t.replace(r + "\n", "").replace(r, "")
        g[SRC] = t
    mut("N07-two-new-ids-left", two_new)
    mut("N08-held-row-rewritten", lambda g: rep(g, SRC, "| teaches | mined | 2026-10-24", "| REWRITTEN | mined | 2026-10-24"))
    mut("N09-duplicate-location", lambda g: rep(g, SRC, REAL["S292"][2], REAL["S291"][2]))
    mut("N10-entry-line-lacks-quote", lambda g: rep(g, ENTRY, EL["S291"], "**OBS** S291 x (Hyprland-WindowRuleApplicator.cpp:%d)." % line_of("Hyprland-WindowRuleApplicator.cpp", q["S291"])))
    mut("N11-wrong-verified-at", lambda g: rep(g, ENTRY, "verified-at: 2026-10-26", "verified-at: 2026-10-23"))
    mut("N13-status-candidate", lambda g: rep(g, SRC, "| teaches | mined | 2026-10-26", "| teaches | candidate | 2026-10-26"))
    mut("N15-no-own-work-row", lambda g: rep(g, SRC, "| own-work |", "| docs |", 3))
    mut("N16-used-by-missing", lambda g: rep(g, SRC, "| 90d | %s |" % ENTRY, "| 90d | corpus/knowledge/other.md |", 11))
    mut("X05-usedby-longer-path", lambda g: rep(g, SRC, rowof("S291"), rowof("S291", used=ENTRY + ".draft-copy.md")))
    mut("X07-index-row-in-fence", lambda g: g.__setitem__("corpus/README.md", base["corpus/README.md"] + "```\n| `knowledge/hyprland-gkeep-geometry-r43.md` | new |\n```\n"))
    mut("X11-gate-lines-indented", lambda g: g.__setitem__(LES, g[LES].replace("GATE ", "  GATE ")))
    mut("X13-dual-gate-stale-first", lambda g: rep(g, LES, "## Gate\n\n", "## Gate\n\nGATE S291 receipt=.ufo/waves/round-41/fetch/S291.txt sha256=%s quote=\"%s\"\n" % ("0" * 64, q["S291"])))
    mut("X14-new-id-opened-stale", lambda g: rep(g, SRC, rowof("S291"), rowof("S291", opened="2026-10-24")))
    # --- host census clause
    mut("H01-rules-size-off", lambda g: rep(g, ENTRY, "size=420x500 float", "size=420x501 float"))
    mut("H02-clients-total-off", lambda g: rep(g, ENTRY, "total=4", "total=5"))
    mut("H03-gkeep-clients-claimed", lambda g: rep(g, ENTRY, "floating=0 gkeep=0", "floating=0 gkeep=1"))
    mut("H04-ui-app-id-wrong", lambda g: rep(g, ENTRY, "application_id=org.omarchy.gkeep", "application_id=org.omarchy.gkeeps"))
    mut("H05-rules-line-twice", lambda g: g.__setitem__(ENTRY, g[ENTRY] + RULES_LINE + "\n"))
    mut("H06-census-line-absent", lambda g: rep(g, ENTRY, CLIENTS_LINE + "\n", ""))
    mut("H07-census-line-in-fence", lambda g: rep(g, ENTRY, UI_LINE + "\n", "```\n" + UI_LINE + "\n```\n"))
    mut("H08-census-line-in-prose", lambda g: rep(g, ENTRY, RULES_LINE + "\n", "The census said %s.\n" % RULES_LINE))
    mut("H09-two-size-rules", lambda g: set_receipt(g, "S297", "host-gkeep.conf", blob("host-gkeep.conf") + b"windowrule = size 1 1, match:class ^(org.omarchy.gkeep)$\n", q["S297"]))
    mut("H10-clients-not-list", lambda g: set_receipt(g, "S298", "host-clients-r43.json", b'{"mapped": true, "class": "chromium", "floating": false, ' + FILLER.encode() + b'}', '"mapped": true, "class": "chromium", "floating": false,'))
    mut("H11-request-size-differs", lambda g: (set_receipt(g, "S299", "gkeep-ui-excerpt.py", blob("gkeep-ui-excerpt.py").replace(b"set_default_size(420, 500)", b"set_default_size(421, 500)"), "window.set_default_size(421, 500) self.board = Board(window)"),
                                               rep(g, ENTRY, "window.set_default_size(420, 500)", "window.set_default_size(421, 500)")))
    mut("H12-one-own-work-row", lambda g: rep(g, SRC, "| own-work |", "| docs |", 2))
    mut("H13-config-regex-differs-from-app-id", lambda g: set_receipt(g, "S297", "host-gkeep.conf", blob("host-gkeep.conf").replace(b"^(org.omarchy.gkeep)$", b"^(org.omarchy.other)$"), q["S297"].replace("gkeep", "other")) or rep(g, ENTRY, "class=^(org.omarchy.gkeep)$", "class=^(org.omarchy.other)$"))
    # --- quote boundary and locator clauses (the round-41 closure's routed holes)
    mut("B01-quote-starts-mid-word", lambda g: (rep(g, LES, 'quote="%s"' % q["S292"], 'quote="indowGeometry.w = COMPUTED->x;"'),
                                                 rep(g, ENTRY, EL["S292"], "**OBS** S292 indowGeometry.w = COMPUTED->x; (Hyprland-DefaultFloatingAlgorithm.cpp:%d)." % line_of("Hyprland-DefaultFloatingAlgorithm.cpp", q["S292"]))))
    mut("B02-quote-ends-mid-word", lambda g: (rep(g, LES, 'quote="%s"' % q["S292"], 'quote="windowGeometry.w = COMPUT"'),
                                               rep(g, ENTRY, EL["S292"], "**OBS** S292 windowGeometry.w = COMPUT (Hyprland-DefaultFloatingAlgorithm.cpp:%d)." % line_of("Hyprland-DefaultFloatingAlgorithm.cpp", q["S292"]))))
    mut("B03-locator-line-off-by-one", lambda g: rep(g, ENTRY, "Hyprland-Target.cpp:%d" % line_of("Hyprland-Target.cpp", q["S293"]), "Hyprland-Target.cpp:%d" % (line_of("Hyprland-Target.cpp", q["S293"]) + 1)))
    mut("B04-locator-missing", lambda g: rep(g, ENTRY, " (Hyprland-Target.cpp:%d)" % line_of("Hyprland-Target.cpp", q["S293"]), ""))
    mut("B05-locator-names-other-file", lambda g: rep(g, ENTRY, "Hyprland-Target.cpp:%d" % line_of("Hyprland-Target.cpp", q["S293"]), "Hyprland-WindowTarget.cpp:%d" % line_of("Hyprland-Target.cpp", q["S293"])))
    mut("B06-locator-prefix-collision", lambda g: rep(g, ENTRY, "Hyprland-Target.cpp:%d" % line_of("Hyprland-Target.cpp", q["S293"]), "xHyprland-Target.cpp:%d" % line_of("Hyprland-Target.cpp", q["S293"])))
    mut("B07-locator-digits-extend", lambda g: rep(g, ENTRY, "Hyprland-Target.cpp:%d" % line_of("Hyprland-Target.cpp", q["S293"]), "Hyprland-Target.cpp:%d0" % line_of("Hyprland-Target.cpp", q["S293"])))
    # --- the assimilation clause
    mut("A01-no-admit-line", lambda g: rep(g, LES, ADMIT + "\n", ""))
    mut("A02-no-refuse-line", lambda g: rep(g, LES, REFUSE + "\n", ""))
    mut("A03-admit-names-other-entry", lambda g: rep(g, LES, " as " + ENTRY, " as corpus/knowledge/other.md"))
    mut("A04-refuse-reason-one-word", lambda g: rep(g, LES, REFUSE.split("reason=")[1], "superseded"))
    mut("A05-localized-channel-source", lambda g: rep(g, SRC, REAL["S290"][2], "https://amgsk.dev/posts/hyprland-rules/"))
    mut("A06-admit-nonexistent-package", lambda g: rep(g, LES, PKG, "merge/mado/knowledge/corpus/knowledge/does-not-exist.md"))
    mut("A07-refuse-nonexistent-package", lambda g: rep(g, LES, PKG2, "merge/mado/knowledge/corpus/knowledge/does-not-exist.md"))
    mut("A08-refuse-equals-admit", lambda g: rep(g, LES, PKG2, PKG))
    mut("A09-refuse-reason-filler", lambda g: rep(g, LES, REFUSE.split("reason=")[1], "x x x x x x x x x x x x x x x x x x x x"))
    mut("A10-admit-line-in-fence", lambda g: rep(g, LES, ADMIT + "\n", "```\n" + ADMIT + "\n```\n"))
    mut("A11-gate-line-in-fence", lambda g: rep(g, LES, [l for l in g[LES].splitlines() if l.startswith("GATE S293")][0],
                                                  "```\n" + [l for l in g[LES].splitlines() if l.startswith("GATE S293")][0] + "\n```"))
    # --- wave survivors of round 41 (kept: they were real holes of v2)
    mut("W01-citation-past-line-20", lambda g: g.__setitem__(ENTRY, g[ENTRY].replace("verified-at: 2026-10-26", "\n".join("pad %d" % i for i in range(14)) + "\nverified-at: 2026-10-26")))
    mut("W02-lowercase-id", lambda g: rep(g, ENTRY, "source: S293 - receipt", "source: s293 - receipt"))
    mut("W03-ghost-id-in-body", lambda g: g.__setitem__(ENTRY, g[ENTRY] + "**OBS** S999 an invented citation.\n"))
    mut("W04-source-after-line-20", lambda g: g.__setitem__(ENTRY, g[ENTRY] + "source: S293 - again\n"))
    mut("W05-verified-at-in-fence", lambda g: rep(g, ENTRY, "verified-at: 2026-10-26", "```\nverified-at: 2026-10-26\n```\nverified-at: 2026-10-23"))
    mut("W06-source-line-in-fence", lambda g: rep(g, ENTRY, "source: S293 - receipt", "```\nsource: S293 - receipt\n```"))
    mut("W07-recheck-tbd", lambda g: rep(g, SRC, rowof("S291"), rowof("S291", recheck="TBD")))
    mut("W08-recheck-bad-date", lambda g: rep(g, SRC, rowof("S291"), rowof("S291", recheck="2026-99-99")))
    mut("W09-row-without-location", lambda g: rep(g, SRC, "title - " + REAL["S291"][2], "title - surfaces"))
    mut("W10-held-row-loses-usedby", lambda g: rep(g, SRC, "corpus/knowledge/old.md, " + ENTRY, ENTRY))
    mut("W11-one-line-two-ids", lambda g: rep(g, ENTRY, EL["S291"], EL["S291"].replace("**OBS** S291", "**OBS** S291 S292")))
    mut("W13-location-fragment-duplicate", lambda g: rep(g, SRC, REAL["S293"][2], REAL["S291"][2] + "#frag"))

    def w14(g):
        target = "Hyprland-Target.cpp " + FILLER
        set_receipt(g, "S293", "Hyprland-Target.cpp", target)
        g["__symlink__"] = FETCH + "Hyprland-Target.cpp"
    mut("W14-symlink-receipt", w14)
    mut("W15-quote-in-two-receipts", lambda g: set_receipt(
        g, "S293", "Hyprland-Target.cpp", blob("Hyprland-Target.cpp") + b"\n" + q["S291"].encode() + b"\n", q["S293"]) or
        set_receipt(g, "S291", "Hyprland-WindowRuleApplicator.cpp", blob("Hyprland-WindowRuleApplicator.cpp") + b"\n" + q["S293"].encode() + b"\n", q["S291"]))
    # --- forgeries against the REAL counter (the pins)
    shared = ("shared receipt text with one quotable sentence " + FILLER).encode()

    def f1(g):
        for i in ("S290", "S291", "S292"):
            fn = REAL[i][0]
            set_receipt(g, i, fn, ("invented %s receipt with a quotable sentence %s " % (i, i) + FILLER), "quotable sentence %s" % i)
            rep(g, ENTRY, EL[i], "**OBS** S%s quotable sentence %s (%s:1)." % (i[1:], i, fn))
    mut("F1-invented-receipts", f1, kind="real")

    def f2(g):
        fake = b'[{"mapped": true, "class": "chromium", "floating": false, "size": [1, 1]}] ' + FILLER.encode()
        set_receipt(g, "S298", "host-clients-r43.json", fake, '"mapped": true, "class": "chromium", "floating": false,')
    mut("F2-invented-clients", f2, kind="real")
    mut("F3-unpinned-quote-boilerplate", lambda g: [set_receipt(g, i, REAL[i][0], blob(REAL[i][0]) + b"\n" + shared) for i in ("S290", "S291")], kind="real")
    mut("F4-localized-redirect", lambda g: rep(g, SRC, REAL["S290"][2], "https://t.co/9xQ2fG"))
    mut("F5-receipt-renamed", lambda g: g.__setitem__(FETCH + "other-name.txt", g.pop(FETCH + "Hyprland-Target.cpp")) or rep(g, LES, FETCH + "Hyprland-Target.cpp", FETCH + "other-name.txt"), kind="real")
    mut("F6-one-char-location", lambda g: rep(g, SRC, REAL["S292"][2], REAL["S292"][2].replace("Algorithm.cpp", "Algorithm.cpz")), kind="real")
    mut("Z1-pinned-receipt-edited-byte", lambda g: set_receipt(g, "S293", "Hyprland-Target.cpp", blob("Hyprland-Target.cpp") + b"\n// edited\n"), kind="real")
    mut("Z2-pinned-conf-edited", lambda g: set_receipt(g, "S297", "host-gkeep.conf", blob("host-gkeep.conf") + b"\n# edited\n"), kind="real")
    return m


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
    d = tempfile.mkdtemp(prefix="mado-c2ctl-")
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
    print("CTL_C2: controls=%d correct=%d/%d" % (n, sum(results), n))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
