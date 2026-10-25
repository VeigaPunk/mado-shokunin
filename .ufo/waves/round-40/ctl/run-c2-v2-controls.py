#!/usr/bin/env python3
"""Round-40 C2 v2 controls: PRED-C2-r40-v2 scored over synthetic fixture repos.

Fixture repos are `D=$(mktemp -d)` with every git call naming `-C D`, the
throwaway identity passed with -c (never written to any config), the toplevel
verified equal to D before the first commit. The real committed captures
(c1/native-capture.jsonl, native-capture-all.jsonl) are copied into every
fixture. Control P (a fabricated self-consistent set) must score 1/1 (the
declared residual); every mutant - the 20 v1 mutants, the wave's 15 RevC2Counter
mutants, the CritC2Cheat cheats, the two MutC2Controls gaps - must score 0/1.
Final line: `CTL_C2V2: controls=N correct=K/N`.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
COUNTER = os.path.join(LANE, "quality", "counters",
                       "c2-r40-forms-entry-v2.py")
C1DIR = os.path.join(HERE, "..", "c1")
ENTRY = "corpus/knowledge/hyprctl-getoption-native-forms-r40.md"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
TOOL_SRC = "#!/usr/bin/env python3\n# tool bytes v1\n"
TOOL_SHA = hashlib.sha256(TOOL_SRC.encode()).hexdigest()
SRC = "corpus/SOURCES.md"
LES = "corpus/lessons/round-40.md"
FETCH = ".ufo/waves/round-40/fetch/"


def counts(path, forms):
    c = dict.fromkeys(forms, 0)
    n = 0
    for l in open(path):
        if l.strip():
            o = json.loads(l)
            n += 1
            for f in forms:
                if f in o:
                    c[f] += 1
    return c, n


CAP, NCAP = counts(os.path.join(C1DIR, "native-capture.jsonl"),
                   ("int", "float", "str", "custom"))
ALL, NALL = counts(os.path.join(C1DIR, "native-capture-all.jsonl"),
                   ("int", "float", "str", "custom", "vec2"))
FORMS_LINE = "forms int=%(int)d float=%(float)d str=%(str)d custom=%(custom)d" % CAP
LABELS_LINE = ("labels agreement=%d agreement*=%d mismatch=0 config-only=0 "
               "live-default=0" % (NCAP - 8, 8))
ALL_LINE = ("allforms int=%(int)d float=%(float)d str=%(str)d custom=%(custom)d "
            "vec2=%(vec2)d" % ALL)
FILLER = ("The census walked the host tree and asked the compositor for every "
          "declared key once. " * 8)

QUOTES = {
    "S050": "handlers and gradients keep the previous angle",
    "S301": "toString prints the angle after the colours",
    "S302": "live getoption census over the host tree",
    "S303": "a category called the same as a handler",
}


def receipt_text(i):
    base = "%s source bytes for %s. %s\n" % (QUOTES[i], i, FILLER)
    if i == "S302":
        return ("tool sha256 %s\n%s\n%s\n%s\n%s\n" % (
            TOOL_SHA, FORMS_LINE, LABELS_LINE, ALL_LINE, base))
    return base


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
    f["tools/mado-options.py"] = TOOL_SRC
    for name in ("native-capture.jsonl", "native-capture-all.jsonl"):
        f[".ufo/waves/round-40/c1/" + name] = open(
            os.path.join(C1DIR, name)).read()
    return f


def gate_line(i, path, text, quote):
    return 'GATE %s receipt=%s sha256=%s quote="%s"' % (
        i, path, sha(text), quote)


def admitted():
    g = base_files()
    held = HELD_ROW.replace("corpus/knowledge/old.md",
                            "corpus/knowledge/old.md, " + ENTRY)
    new = [row("S301", "https://example.org/a.hpp"),
           row("S302", ".ufo/waves/round-40/fetch/S302.receipt.txt",
               kind="own-work"),
           row("S303", "https://example.org/c.cpp")]
    g[SRC] = g[SRC].replace(HELD_ROW, held + "\n" + "\n".join(new))
    gates = []
    paths = {"S050": "S050.txt", "S301": "S301.html",
             "S302": "S302.receipt.txt", "S303": "S303.txt"}
    for i, fn in paths.items():
        g[FETCH + fn] = receipt_text(i)
        gates.append(gate_line(i, FETCH + fn, receipt_text(i), QUOTES[i]))
    g[LES] = "# round 40\n\n## Gate\n\n" + "\n".join(gates) + "\n"
    g[ENTRY] = "\n".join([
        "# The getoption native forms", "",
        "source: S050 - held parser", "source: S301 - types header",
        "source: S302 - own-work census", "source: S303 - config source",
        "verified-at: 2026-10-25", "recheck: 90d", "",
        "**OBS** S050 %s." % QUOTES["S050"],
        "**OBS** S301 %s." % QUOTES["S301"],
        "**OBS** S302 %s." % QUOTES["S302"],
        "**OBS** S303 %s." % QUOTES["S303"], "",
        FORMS_LINE, LABELS_LINE, ALL_LINE, ""]) + "\n"
    g["corpus/README.md"] += "| `knowledge/hyprctl-getoption-native-forms-r40.md` | new |\n"
    return g


def set_receipt(g, i, fn, text, quote=None):
    g[FETCH + fn] = text
    old = [l for l in g[LES].splitlines() if l.startswith("GATE %s " % i)][0]
    q = quote or QUOTES[i]
    g[LES] = g[LES].replace(old, gate_line(i, FETCH + fn, text, q))


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

    def one_new(g):
        t = g[SRC]
        for r in (row("S301", "https://example.org/a.hpp"),
                  row("S303", "https://example.org/c.cpp")):
            t = t.replace(r + "\n", "").replace(r, "")
        g[SRC] = t
    mut("N07-one-new-id-left", one_new)
    mut("N08-held-row-rewritten", lambda g: g.__setitem__(
        SRC, g[SRC].replace("| teaches | mined | 2026-10-24",
                            "| REWRITTEN | mined | 2026-10-24")))
    mut("N09-duplicate-location", lambda g: g.__setitem__(
        SRC, g[SRC].replace("https://example.org/c.cpp",
                            "https://example.org/a.hpp")))
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
    mut("N17-receipt-tool-sha-stale", lambda g: g.__setitem__(
        "tools/mado-options.py", TOOL_SRC + "# edited after the receipt\n"))
    mut("N18-forms-line-disagrees-with-capture", lambda g: (
        set_receipt(g, "S302", "S302.receipt.txt",
                    receipt_text("S302").replace("custom=%d" % CAP["custom"],
                                                 "custom=%d" % (CAP["custom"] + 1))),
        g.__setitem__(ENTRY, g[ENTRY].replace("custom=%d" % CAP["custom"],
                                              "custom=%d" % (CAP["custom"] + 1)))))
    bad = receipt_text("S302").replace("agreement=%d" % (NCAP - 8),
                                       "agreement=%d" % (NCAP - 9))
    mut("N19-labels-sum-wrong", lambda g: (
        set_receipt(g, "S302", "S302.receipt.txt", bad),
        g.__setitem__(ENTRY, g[ENTRY].replace("agreement=%d" % (NCAP - 8),
                                              "agreement=%d" % (NCAP - 9)))))
    mut("N20-lines-not-in-entry", lambda g: g.__setitem__(
        ENTRY, g[ENTRY].replace(LABELS_LINE, "")))
    # --- RevC2Counter (wave) ---
    mut("X01-sha-not-own-line", lambda g: set_receipt(
        g, "S302", "S302.receipt.txt",
        receipt_text("S302").replace("tool sha256 %s\n" % TOOL_SHA, "").replace(
            "live getoption census", "live getoption census %s" % TOOL_SHA)))
    mut("X03-counts-in-prose-line", lambda g: g.__setitem__(
        ENTRY, g[ENTRY].replace(FORMS_LINE + "\n", "The census reported %s.\n"
                                % FORMS_LINE)))
    mut("X05-usedby-longer-path", lambda g: g.__setitem__(
        SRC, g[SRC].replace(row("S301", "https://example.org/a.hpp"),
                            row("S301", "https://example.org/a.hpp",
                                used=ENTRY + ".draft-copy.md"))))
    def x07(g):
        g["corpus/README.md"] = base["corpus/README.md"] + (
            "```\n| `knowledge/hyprctl-getoption-native-forms-r40.md` | new |\n"
            "```\n")
    mut("X07-index-row-in-fence", x07)
    mut("X11-gate-lines-indented", lambda g: g.__setitem__(
        LES, g[LES].replace("GATE ", "  GATE ")))

    def x13(g):
        stale = ('GATE S303 receipt=.ufo/waves/round-39/fetch/S303.txt '
                 'sha256=%s quote="%s"' % ("0" * 64, QUOTES["S303"]))
        g[LES] = g[LES].replace("## Gate\n\n", "## Gate\n\n" + stale + "\n")
    mut("X13-dual-gate-stale-first", x13)
    mut("X14-new-id-opened-stale", lambda g: g.__setitem__(
        SRC, g[SRC].replace(row("S301", "https://example.org/a.hpp"),
                            row("S301", "https://example.org/a.hpp",
                                opened="2026-10-24"))))
    # X15 (CRLF receipt) is an equivalent mutant under v2: splitlines() reads it; not a control.
    # --- CritC2Cheat (wave) ---
    shared = ("shared receipt text with one quotable sentence " + FILLER)

    def cheat_shared(g):
        for i, fn in (("S050", "S050.txt"), ("S301", "S301.html"),
                      ("S303", "S303.txt")):
            set_receipt(g, i, fn, shared, "one quotable sentence")
            g[ENTRY] = g[ENTRY].replace(QUOTES[i], "one quotable sentence")
    mut("Y01-one-receipt-shared-by-ids", cheat_shared)
    tiny = "int=1 float=0 str=0 " * 2

    def cheat_tiny(g):
        for i, fn in (("S050", "S050.txt"), ("S301", "S301.html"),
                      ("S303", "S303.txt")):
            t = "tiny %s %s" % (i, tiny)
            set_receipt(g, i, fn, t, "tiny %s int=1 float=0 str=0" % i)
            g[ENTRY] = g[ENTRY].replace(QUOTES[i],
                                        "tiny %s int=1 float=0 str=0" % i)
    mut("Y02-receipts-under-512-bytes", cheat_tiny)
    mut("Y03-n1-census", lambda g: (
        set_receipt(g, "S302", "S302.receipt.txt", receipt_text("S302")
                    .replace(FORMS_LINE, "forms int=1 float=0 str=0 custom=0")
                    .replace(LABELS_LINE, "labels agreement=1 agreement*=0 "
                             "mismatch=0 config-only=0 live-default=0")),
        g.__setitem__(ENTRY, g[ENTRY]
                      .replace(FORMS_LINE, "forms int=1 float=0 str=0 custom=0")
                      .replace(LABELS_LINE, "labels agreement=1 agreement*=0 "
                               "mismatch=0 config-only=0 live-default=0"))))
    mut("Y04-quote-on-a-count-line", lambda g: (
        set_receipt(g, "S303", "S303.txt",
                    "census text %s\n" % FORMS_LINE + FILLER, FORMS_LINE),
        g.__setitem__(ENTRY, g[ENTRY].replace(
            "**OBS** S303 %s." % QUOTES["S303"], ""))))
    mut("Y05-allforms-line-wrong", lambda g: (
        set_receipt(g, "S302", "S302.receipt.txt",
                    receipt_text("S302").replace("vec2=%d" % ALL["vec2"], "vec2=0")),
        g.__setitem__(ENTRY, g[ENTRY].replace("vec2=%d" % ALL["vec2"], "vec2=0"))))
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
    print("CTL_C2V2: controls=%d correct=%d/%d" % (n, sum(results), n))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
