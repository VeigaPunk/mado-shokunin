#!/usr/bin/env python3
"""CritC2Cheat: minimal tightenings, applied to COPIES of the frozen counter in scratch.

Each probe is a string patch of quality/counters/c2-r43-gkeep-entry.py; the frozen file is
read once and never written. Every probe is run on control P (must stay admitted=1/1) and on
the forgery it is meant to kill. The url-exact probe is the negative one: it kills P, which is
the evidence that the location field cannot be tightened without changing the fixture.
"""
import importlib.util
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WORK = "/fast/scratch/hyaku/mado-r43/CritC2Cheat"
SEAT = os.path.join(LANE, ".ufo/waves/round-43/w1/CritC2Cheat")
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
RULES_LINE = ctl.CENSUS[0]

HELPERS = '''

def occurrences(blob, nq):
    isw = lambda c: c.isalnum() or c == "_"
    if looks_html(blob):
        text = norm(blob.decode("utf-8", "replace"))
    else:
        text = collapse_with_lines(blob.decode("utf-8", "replace"))[0]
    out, start = [], 0
    while True:
        k = text.find(nq, start)
        if k < 0:
            return out
        before = text[k - 1] if k > 0 else " "
        after = text[k + len(nq)] if k + len(nq) < len(text) else " "
        if not (isw(nq[0]) and isw(before)) and not (isw(nq[-1]) and isw(after)):
            out.append(k)
        start = k + 1


def strip_comments(text, path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".cpp", ".hpp", ".h", ".cc"):
        text = re.sub(r"/\\*.*?\\*/", " ", text, flags=re.S)
        return re.sub(r"//[^\\n]*", " ", text)
    if ext in (".py", ".conf"):
        return re.sub(r"#[^\\n]*", " ", text)
    return text


def quote_in_code(blob, nq, path):
    flat = re.sub(r"\\s+", " ", strip_comments(blob.decode("utf-8", "replace"), path))
    return nq in flat


def all_body_lines_bound(ids, entry_lines, gates, receipts_raw):
    for i in ids:
        gl = gates.get(i, [])
        if len(gl) != 1 or i not in receipts_raw:
            return False
        path, digest, quote = gl[0]
        q = re.sub(r"\\s+", " ", quote)
        at = quote_at(receipts_raw[i], q)
        bn = os.path.basename(path)
        for l in entry_lines:
            if not re.search(r"\\b%s\\b" % i, l):
                continue
            if l.startswith("source:"):
                continue
            if q not in l:
                return False
            if at and ("%s:%d" % (bn, at)) not in l:
                return False
    return True

'''

PROBES = {
    # name -> (patch assert string, replacement)
    "unique-occurrence": (
        "                    and quote_at(blob, nq) is not None):",
        "                    and quote_at(blob, nq) is not None\n"
        "                    and len(occurrences(blob, nq)) == 1):"),
    "quote-not-in-comment": (
        "                    and quote_at(blob, nq) is not None):",
        "                    and quote_at(blob, nq) is not None\n"
        "                    and quote_in_code(blob, nq, path)):"),
    "every-naming-line-bound": (
        '    cl["g"] = int(g_ok)',
        '    cl["g"] = int(g_ok and all_body_lines_bound(ids, entry_lines, gates, receipts_raw))'),
    "package-path-exact": (
        "    staged_ok = lambda p: os.path.basename(p) in STAGED",
        "    staged_ok = lambda p: (p == 'merge/mado/knowledge/corpus/knowledge/' + os.path.basename(p)\n"
        "                            and os.path.basename(p) in STAGED)"),
    "url-exact-NEGATIVE": (
        "        e_ok &= bool(comp) and (comp in rb or rb in comp)",
        "        e_ok &= bool(comp) and (comp in rb or rb in comp)\n"
        "        if rb.startswith('hyprland-') and not cells_[1].split()[-1].startswith(\n"
        "                'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/'):\n"
        "            e_ok = False"),
}


def make_probe(name):
    src = open(COUNTER).read()
    assert "def norm(text):" in src
    src = src.replace("def norm(text):", HELPERS + "\ndef norm(text):", 1)
    old, new = PROBES[name]
    assert old in src, (name, old)
    path = os.path.join(WORK, "c2-probe-%s.py" % name)
    open(path, "w").write(src.replace(old, new, 1))
    return path


def run(files_after, counter, base):
    d = tempfile.mkdtemp(prefix="px-", dir=WORK)
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=ENV)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             check=True, capture_output=True, text=True,
                             env=ENV).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d)
        b = ctl.commit_all(d, base, "base")
        a = ctl.commit_all(d, files_after, "after")
        p = subprocess.run([sys.executable, "-I", counter, "--repo", d,
                            "--rev", a, "--base", b],
                           capture_output=True, text=True, env=ENV)
        lines = p.stdout.strip().splitlines()
        verdict = [l for l in lines if ": admitted=" in l]
        cl = [l for l in lines if " clauses=" in l]
        return p.returncode, verdict[-1] if verdict else "NO FINAL", \
            cl[0].split("clauses=")[1].split(" admitted")[0] if cl else "-"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def forgery(name, base):
    g = {k: v for k, v in ctl.admitted().items()}
    if name == "B1-second-occurrence":
        BQ = "const auto& expr = std::get<Math::SExpressionVec2>(value);"
        BF = "Hyprland-WindowRuleApplicator.cpp"
        g[LES] = g[LES].replace('quote="%s"' % Q["S291"], 'quote="%s"' % BQ)
        g[ENTRY] = g[ENTRY].replace(EL["S291"],
            "**OBS** S291 " + BQ + " - the size rule stores this expression as "
            "static_.size (%s:%d)." % (BF, ctl.line_of(BF, BQ)))
    elif name == "C1-comment-quote":
        CQ = "TODO: not very OOP, is it?"
        CF = "Hyprland-DefaultFloatingAlgorithm.cpp"
        g[LES] = g[LES].replace('quote="%s"' % Q["S292"], 'quote="%s"' % CQ)
        g[ENTRY] = g[ENTRY].replace(EL["S292"],
            "**OBS** S292 " + CQ + " - the algorithm leaves the size to the client (%s:%d)."
            % (CF, ctl.line_of(CF, CQ)))
    elif name == "E1-id-contradiction":
        g[ENTRY] += "**NOTE** S291 is unrelated to the size path: no rule writes static_.size.\n"
    elif name == "F1-fake-package-dir":
        fake = "merge/mado/not-a-real-dir/"
        g[LES] = g[LES].replace("ADMIT " + ctl.PKG + " as ",
                                "ADMIT " + fake + os.path.basename(ctl.PKG) + " as ")
        g[LES] = g[LES].replace("REFUSE " + ctl.PKG2 + " reason=",
                                "REFUSE " + fake + os.path.basename(ctl.PKG2) + " reason=")
    elif name == "P-genuine":
        pass
    else:
        raise SystemExit("unknown fixture " + name)
    return g


BASE = ctl.base_files()
print("counter sha256:", hashlib.sha256(open(COUNTER, "rb").read()).hexdigest())
for probe, targets in (("unique-occurrence", ["P-genuine", "B1-second-occurrence"]),
                       ("quote-not-in-comment", ["P-genuine", "C1-comment-quote"]),
                       ("every-naming-line-bound", ["P-genuine", "E1-id-contradiction"]),
                       ("package-path-exact", ["P-genuine", "F1-fake-package-dir"]),
                       ("url-exact-NEGATIVE", ["P-genuine", "G1-fake-url"])):
    counter = make_probe(probe)
    for t in targets:
        if t == "G1-fake-url":
            g = {k: v for k, v in ctl.admitted().items()}
            g[SRC] = g[SRC].replace(ctl.REAL["S293"][2],
                                    "https://example.invalid/nope/Hyprland-Target.cpp")
        else:
            g = forgery(t, BASE)
        rc, verdict, cls = run(g, counter, BASE)
        print("probe=%-24s fixture=%-24s rc=%d %s clauses=%s"
              % (probe, t, rc, verdict.split(" verdict")[0].split("PRED-C2-r43: ")[-1], cls))
