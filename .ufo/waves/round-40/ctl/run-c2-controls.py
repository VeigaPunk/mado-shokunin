#!/usr/bin/env python3
"""Round-40 C2 controls: PRED-C2-r40-v1 scored over synthetic fixture repos.

Every fixture repo is `D=$(mktemp -d)` with every git call naming `-C D` and
the throwaway identity passed with -c (never written to any config); the
toplevel is verified equal to D before the first commit. Control P (a
fabricated self-consistent set) must score admitted=1/1 (the declared
residual); every mutant must score admitted=0/1.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

COUNTER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "..", "..", "..", "quality", "counters",
                       "c2-r40-forms-entry.py")
COUNTER = os.path.abspath(COUNTER)
ENTRY = "corpus/knowledge/hyprctl-getoption-native-forms-r40.md"
TOOL_SRC = "#!/usr/bin/env python3\n# tool bytes v1\n"
FORMS_LINE = "forms int=44 float=5 str=8 custom=13"
LABELS_LINE = "labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
def receipt_a():
    return ("tool sha256 %s\n%s\n%s\nlive getoption census over the host tree"
            % (hashlib.sha256(TOOL_SRC.encode()).hexdigest(), FORMS_LINE,
               LABELS_LINE))
RECEIPT_B = ("<html><body><pre>if pgrep -x hypridle >/dev/null; then echo "
             "idle disabled</pre></body></html>")
RECEIPT_C = "five JSON producers run scripts with no poll interval at all"
QA = "live getoption census over the host tree"
QB = "if pgrep -x hypridle >/dev/null; then echo idle disabled"
QC = "five JSON producers run scripts with no poll interval"
QX = "quotable sentence about handlers and gradients"
HELD_ROW = ("| S050 | held hyprlang config source - https://example.org/config.cpp "
            "| code | A | scope | anchor | teaches | mined | 2026-10-24 | "
            "on-change | corpus/knowledge/old.md |")


def row(i, loc, used=ENTRY, status="mined", opened="2026-10-25",
        kind="docs"):
    return ("| %s | title - %s | %s | A | scope | anchor | teaches | %s | %s "
            "| 90d | %s |" % (i, loc, kind, status, opened, used))


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def good():
    f = {}
    f["corpus/SOURCES.md"] = "\n".join([
        "# Sources", "", "## Registry", "",
        "| id | source | kind | tier | scope | anchor | teaches | status | "
        "opened | recheck | used-by |",
        "|---|---|---|---|---|---|---|---|---|---|---|", HELD_ROW, "",
        "## Paths", ""]) + "\n"
    f["corpus/README.md"] = "# Coverage\n\n| `knowledge/old.md` | old |\n"
    f["corpus/knowledge/old.md"] = "old\n"
    f["tools/mado-options.py"] = TOOL_SRC
    return f


def after(f, **kw):
    """Add the admitted state on top of base files f (dict path -> text)."""
    g = dict(f)
    held = HELD_ROW.replace("corpus/knowledge/old.md",
                            "corpus/knowledge/old.md, " + ENTRY)
    new = [row("S301", "https://example.org/a.hpp"),
           row("S302", ".ufo/waves/round-40/fetch/S302.receipt.txt",
               kind="own-work"),
           row("S303", "https://example.org/c.cpp")]
    g["corpus/SOURCES.md"] = g["corpus/SOURCES.md"].replace(
        HELD_ROW, held + "\n" + "\n".join(new))
    RA = "held source text with a quotable sentence about handlers and gradients"
    g[".ufo/waves/round-40/fetch/S050.txt"] = RA
    g[".ufo/waves/round-40/fetch/S301.html"] = RECEIPT_B
    g[".ufo/waves/round-40/fetch/S302.receipt.txt"] = receipt_a()
    g[".ufo/waves/round-40/fetch/S303.txt"] = RECEIPT_C
    gates = [
        'GATE S050 receipt=.ufo/waves/round-40/fetch/S050.txt sha256=%s '
        'quote="%s"' % (sha(RA), QX),
        'GATE S301 receipt=.ufo/waves/round-40/fetch/S301.html sha256=%s '
        'quote="%s"' % (sha(RECEIPT_B), QB),
        'GATE S302 receipt=.ufo/waves/round-40/fetch/S302.receipt.txt '
        'sha256=%s quote="%s"' % (sha(receipt_a()), QA),
        'GATE S303 receipt=.ufo/waves/round-40/fetch/S303.txt sha256=%s '
        'quote="%s"' % (sha(RECEIPT_C), QC)]
    g["corpus/lessons/round-40.md"] = "# round 40\n\n## Gate\n\n" + \
        "\n".join(gates) + "\n"
    g[ENTRY] = "\n".join([
        "# The host's bar producers", "",
        "source: S050 - held parser",
        "source: S301 - types header",
        "source: S302 - own-work census",
        "source: S303 - config source",
        "verified-at: 2026-10-25", "recheck: 90d", "",
        "**OBS** S050 %s." % QX, "**OBS** S301 %s." % QB,
        "**OBS** S302 %s." % QA, "**OBS** S303 %s." % QC,
        FORMS_LINE, LABELS_LINE, ""]) + "\n"
    g["corpus/README.md"] += "| `knowledge/hyprctl-getoption-native-forms-r40.md` | new |\n"
    return g


def mutants():
    base = good()
    G = after(base)
    m = {}

    def mut(name, fn):
        g = dict(G)
        fn(g)
        m[name] = g
    SRC = "corpus/SOURCES.md"
    LES = "corpus/lessons/round-40.md"
    mut("N01-no-entry", lambda g: g.pop(ENTRY))
    mut("N02-entry-no-rows", lambda g: g.__setitem__(SRC, base[SRC]))
    mut("N03-gate-sha-wrong", lambda g: g.__setitem__(
        LES, g[LES].replace(sha(RECEIPT_B), "0" * 64)))
    mut("N04-quote-absent", lambda g: g.__setitem__(
        ".ufo/waves/round-40/fetch/S301.html", "<html>nothing here</html>"))
    long_q = " ".join("w%d" % i for i in range(26))
    mut("N05-quote-26-words", lambda g: g.update({
        ".ufo/waves/round-40/fetch/S303.txt": long_q,
        LES: g[LES].replace(sha(RECEIPT_C), sha(long_q)).replace(QC, long_q),
        ENTRY: g[ENTRY].replace(QC, long_q)}))
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
        ENTRY, g[ENTRY].replace("**OBS** S301 %s." % QB, "**OBS** S301 x.")))
    mut("N11-wrong-verified-at", lambda g: g.__setitem__(
        ENTRY, g[ENTRY].replace("verified-at: 2026-10-25",
                                "verified-at: 2026-10-23")))
    mut("N12-staged-ids-as-is", lambda g: g.__setitem__(
        ENTRY, g[ENTRY].replace("S301", "S228").replace("S303", "S231")))
    mut("N13-status-candidate", lambda g: g.__setitem__(
        SRC, g[SRC].replace("| teaches | mined | 2026-10-25",
                            "| teaches | candidate | 2026-10-25")))
    mut("N14-receipt-outside-fetch", lambda g: g.__setitem__(
        LES, g[LES].replace(".ufo/waves/round-40/fetch/S301.html",
                            ".ufo/waves/round-39/fetch/S301.html")))
    mut("N15-no-own-work-row", lambda g: g.__setitem__(
        SRC, g[SRC].replace("| own-work |", "| docs |")))
    mut("N16-used-by-missing", lambda g: g.__setitem__(
        SRC, g[SRC].replace("| 90d | %s |" % ENTRY,
                            "| 90d | corpus/knowledge/other.md |")))
    mut("N17-receipt-tool-sha-stale", lambda g: g.__setitem__(
        "tools/mado-options.py", TOOL_SRC + "# edited after the receipt\n"))
    mut("N18-counts-disagree", lambda g: g.update({
        ENTRY: g[ENTRY].replace(FORMS_LINE, "forms int=44 float=5 str=8 "
                                "custom=14")}))
    bad = receipt_a().replace("agreement=62", "agreement=61")
    mut("N19-labels-sum-wrong", lambda g: g.update({
        ".ufo/waves/round-40/fetch/S302.receipt.txt": bad,
        LES: g[LES].replace(sha(receipt_a()), sha(bad)),
        ENTRY: g[ENTRY].replace("agreement=62", "agreement=61")}))
    mut("N20-lines-not-in-entry", lambda g: g.__setitem__(
        ENTRY, g[ENTRY].replace(LABELS_LINE, "")))
    return base, G, m


def commit_all(d, files, msg):
    for rel, text in files.items():
        path = os.path.join(d, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(text)
    ident = ["-c", "user.name=ctl", "-c", "user.email=ctl@ctl.invalid"]
    subprocess.run(["git", "-C", d, "add", "-A"], check=True, env=ENV)
    subprocess.run(["git", "-C", d, *ident, "commit", "-q", "-m", msg,
                    "--no-gpg-sign"], check=True, env=ENV)
    return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True,
                          env=ENV).stdout.strip()


def score(files_base, files_after, tag):
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
        p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", d,
                            "--rev", a, "--base", b],
                           capture_output=True, text=True, env=ENV)
        lines = p.stdout.strip().splitlines()
        last = lines[-1] if lines else ""
        cls = [l for l in lines if " clauses=" in l]
        score.clauses = cls[0].split(" clauses=")[1].split(" admitted")[0] \
            if cls else "-"
        return p.returncode, last
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    base, G, m = mutants()
    ok_all = True
    correct = 0
    rc, last = score(base, G, "P")
    p_ok = rc == 0 and "admitted=1/1" in last
    print("control=P-fabricated-self-consistent expected=admitted=1/1 "
          "observed=%s ok=%d" % (last.split(" rev=")[0].split(": ")[-1],
                                 p_ok))
    ok_all &= p_ok
    correct += p_ok
    for name, g in sorted(m.items()):
        rc, last = score(base, g, name)
        ok = rc == 1 and "admitted=0/1" in last
        ok_all &= ok
        correct += ok
        print("control=%s expected=admitted=0/1 observed=%s clauses=%s ok=%d"
              % (name, last.split(" rev=")[0].split(": ")[-1].split(" verdict")[0],
                 score.clauses, ok))
    n = len(m) + 1
    print("CTL_C2: controls=%d correct=%d/%d" % (n, correct, n))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
