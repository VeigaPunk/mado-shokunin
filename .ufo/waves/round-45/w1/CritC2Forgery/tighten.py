#!/usr/bin/env python3
"""Build tightened COPIES of the frozen PRED-C2-r45 counter in scratch (the lane file is never touched) and run
them against P and the seven forgeries, so every proposed tightening is shown to keep P admitted."""
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r45/CritC2Forgery"
D = os.path.join(S, "pc")
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SRC = os.path.join(LANE, "quality/counters/c2-r45-monitor-entry.py")
BASE = "0c89478af821a6424c9ac922eafe02e39630cf4f"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}

import json

REVS = json.load(open(os.path.join(S, "logs", "revs.json")))
P = REVS.pop("P")
FORGED = REVS

T1_OLD = 'for key, v in re.findall(r"\\b(%s)=(\\S+)" % "|".join(CENSUS_KEYS), l):'
T1_NEW = 'for key, v in re.findall(r"\\b(%s)\\s*[:=]\\s*(\\S+)" % "|".join(CENSUS_KEYS), l):'

T2_OLD = '            good &= cells[8] == OPENED and ("/" in loc and "." in loc)'
T2_NEW = (T2_OLD + '\n            good &= not re.search(r"\\b(supersed\\w*|replac\\w*|obsolet\\w*)\\b",\n'
          '                                " ".join(cells), re.I)')

FENCES_FN = '''
def fences_ok(repo, rev):
    """T3: a fenced block may only carry text that occurs verbatim in a pinned receipt."""
    text = (show(repo, rev, ENTRIES[0]) or b"").decode("utf-8", "replace")
    blocks, cur, fenced = [], [], False
    for line in text.splitlines():
        if re.match(r"^\\s{0,3}(```|~~~)", line):
            if fenced:
                blocks.append("\\n".join(cur))
                cur = []
            fenced = not fenced
            continue
        if fenced:
            cur.append(line)
    if fenced:
        return False
    if not any(b.strip() for b in blocks):
        return True
    pins = " ".join(re.sub(r"\\s+", " ", (show(repo, rev, FETCH + p) or b"").decode("utf-8", "replace"))
                    for p in sorted(PINS))
    return all(re.sub(r"\\s+", " ", b).strip() in pins for b in blocks if b.strip())

'''

T3_ANCHOR = ('    cl["j"] = int(raw is not None and surfaces_ok(repo, rev, text, name))',
             '    cl["b"] = cl["b"] and int(fences_ok(repo, rev))\n' +
             '    cl["j"] = int(raw is not None and surfaces_ok(repo, rev, text, name))')

T5_OLD = '''    pat = re.compile(r"^\\| `knowledge/%s`" % re.escape(name))
    cl["f"] = int(sum(1 for l in unfenced(readme) if pat.match(l)) == 1)'''
T5_NEW = '''    pat = re.compile(r"^\\| `knowledge/%s`" % re.escape(name))
    frows = [l for l in unfenced(readme) if pat.match(l)]
    cl["f"] = int(len(frows) == 1)
    # T5: the index row's status and id list must match the entry's own claims
    if frows:
        fc = [c.strip() for c in frows[0].strip().strip("|").split("|")]
        listed = set()
        for a, b in re.findall(r"S(\\d{3,})(?:-S(\\d{3,}))?", fc[2] if len(fc) > 2 else ""):
            listed |= set("S%03d" % k for k in range(int(a), int(b or a) + 1))
        cl["f"] &= int(len(fc) == 3 and fc[1] == "draft" and listed == set(ids))'''
T4_OLD = '    cl["i"] = int(not bad)'
T4_NEW = '''    cl["i"] = int(not bad)
    # T4: a verdict token on a line that cites a receipts/ path must be in that receipt
    v_ok = True
    for l in entry_lines:
        toks = [t for t in ("AGREE", "DIFFER", "UNRULED", "NOT_COMPARED", "NO_MATCHING_MONITOR", "NO_RULES")
                if re.search(r"\\b%s\\b" % t, l)]
        locs = re.findall(r"(?<![\\w.-])(\\.ufo/waves/round-\\d+/receipts/[A-Za-z0-9._-]+)", l)
        if not toks or not locs:
            continue
        rec = (show(repo, rev, locs[0]) or b"").decode("utf-8", "replace")
        if not all(re.search(r"\\b%s\\b" % t, rec) for t in toks):
            v_ok = False
    cl["i"] = cl["i"] and int(v_ok)'''


def build(name, edits):
    t = open(SRC, encoding="utf-8").read()
    for old, new in edits:
        assert t.count(old) == 1, (name, t.count(old), old[:60])
        t = t.replace(old, new)
    p = os.path.join(S, "counter_%s.py" % name)
    open(p, "w", encoding="utf-8").write(t)
    return p


def run(counter, rev):
    p = subprocess.run([sys.executable, "-I", counter, "--repo", D, "--rev", rev, "--base", BASE],
                       capture_output=True, text=True, env=ENV)
    last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr.strip()
    cl = [l for l in p.stdout.splitlines() if "clauses=" in l]
    return p.returncode, last, (cl[0].split("clauses=")[1] if cl else "?")


def main():
    counters = {
        "frozen": SRC,
        "T1-census-separator": build("T1", [(T1_OLD, T1_NEW)]),
        "T2-row-provenance": build("T2", [(T2_OLD, T2_NEW)]),
        "T3-fence-bound-to-pins": build("T3", [("def score(repo, rev, base, entry, reg_rev, reg_base, lesson, readme):",
                                               FENCES_FN + "def score(repo, rev, base, entry, reg_rev, reg_base, lesson, readme):"),
                                              T3_ANCHOR]),
        "T4-verdict-citation": build("T4", [(T4_OLD, T4_NEW)]),
        "T5-index-row": build("T5", [(T5_OLD, T5_NEW)]),
    }
    revs = [("P", P)] + list(FORGED.items())
    log = []
    for cname, cpath in counters.items():
        for rname, rev in revs:
            rc, last, cl = run(cpath, rev)
            verdict = "ADMITTED" if rc == 0 else "missed"
            line = "%-24s %-26s rc=%d %-9s %s" % (cname, rname, rc, verdict, cl)
            print(line)
            log.append(line)
    open(os.path.join(S, "logs", "tighten-matrix.txt"), "w").write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
