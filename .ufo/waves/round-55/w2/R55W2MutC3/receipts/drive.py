#!/usr/bin/env python3
"""R55W2MutC3 mutation driver. Mutates COPIES of the C3 counter and harness in scratch; never touches the lane."""
import json
import os
import re
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r55/R55W2MutC3"
DELIV = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w2/R55W2MutC3/mutants"
D = open(os.path.join(S, "env.sh")).read().split("=", 1)[1].strip()
G = open(os.path.join(S, "good.rev")).read().strip()
CTR = os.path.join(S, "quality/counters/c3-r55-p19.py")
HARN_SRC = os.path.join(S, "quality/r55_ctl_c3.py")
DISP = os.path.join(S, "quality/check-r55-controls.py")
STUB = os.path.join(S, "stub/always_green.py")
PY = [sys.executable, "-I"]

os.makedirs(DELIV, exist_ok=True)
os.makedirs(os.path.join(S, "stub"), exist_ok=True)
os.makedirs(os.path.join(S, "runs"), exist_ok=True)
with open(STUB, "w") as f:
    f.write('import sys\nrev = sys.argv[sys.argv.index("--rev") + 1]\n'
            'print("MADO_P19_FIX: rev=%s prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none" % rev)\n'
            'sys.exit(0)\n')

ctr_src = open(CTR, encoding="utf-8").read()
harn_src = open(HARN_SRC, encoding="utf-8").read()

# (id, name, old, new) -- old must occur exactly once in the source it edits
COUNTER_MUTANTS = [
    ("C01", "drop prefix leg", 'missed.append("prefix")', "pass"),
    ("C02", "drop rows:Qnn legs (keep heading)", "missed += row_missed",
     'missed += [m for m in row_missed if m == "rows:heading"]'),
    ("C03", "drop rows:heading leg", 'row_missed.insert(0, "rows:heading")', "pass"),
    ("C04", "drop pin leg", 'missed.append("pin")', "pass"),
    ("C05", "drop p23 leg", 'missed.append("p23")', "pass"),
    ("C06", "drop stale leg", 'missed.append("stale")', "pass"),
    ("C07", "drop readme leg", 'missed.append("readme")', "pass"),
    ("C08", "drop tables_sha leg", 'missed.append("tables_sha")', "pass"),
    ("C09", "weaken stale: case-sensitive only-when", 'stale = b"only when" in block.lower()',
     'stale = b"only when" in block'),
    ("C10", "stale exact-sentence leg disabled (redundant given C09 lower())", "cl[2] and cl[2] in block:",
     "cl[2] and False:"),
    ("C11", "P23 token list: drop RELEASED", 'b"PRESSED", b"RELEASED"]', 'b"PRESSED"]'),
    ("C12", "P23 token list: drop '== 0'", 'b"== 0", ', ""),
    ("C13", "P23 token list: drop '== 1'", 'b"== 1", ', ""),
    ("C14", "P23 token list: drop m_passPressed", 'b"m_passPressed", ', ""),
    ("C15", "P23 alt list: drop else", 'b"any other", b"else"]', 'b"any other"]'),
    ("C16", "P23 alt list: drop otherwise", 'P23_ALT = [b"otherwise", ', "P23_ALT = ["),
    ("C17", "P23 pin:anchor check dropped", "and c[4] == P23_ANCHOR:", ":"),
    ("C18", "P23 Supersedes check dropped", 'c[1] == b"P19" and ', ""),
    ("C19", "P23 Source row check dropped", 'c[3] == b"S371" and ', ""),
    ("C20", "P23 exactly-one row relaxed to >=1", "if len(p23_rows) == 1:", "if len(p23_rows) >= 1:"),
    ("C21", "BASE constant: last hex digit changed", 'BASE = "3b55b6e91e40f455dd56b2985e4ffc087ada92d5"',
     'BASE = "3b55b6e91e40f455dd56b2985e4ffc087ada92d4"'),
    ("C22", "Q id range: Q13 dropped", "range(1, NQ + 1)", "range(1, NQ)"),
    ("C23", "Q id range: Q01 dropped", "range(1, NQ + 1)", "range(2, NQ + 1)"),
    ("C24", "CRLF accepted in prefix comparison", "prefix_ok = entry is not None and entry.startswith(base_entry)",
     r'prefix_ok = entry is not None and entry.replace(b"\r\n", b"\n").startswith(base_entry)'),
    ("C25", "duplicate Q rows accepted", "if len(rs) == 1 and i in frozen_q:", "if len(rs) >= 1 and i in frozen_q:"),
    ("C26", "Q pin:line anchor check dropped", "c[1] == want_anchor and ", ""),
    ("C27", "Q quote check dropped", "and c[2] == want_quote", ""),
    ("C28", "pin sha256 check dropped", "if pb is not None and sha256(pb) == pin_sha:", "if pb is not None:"),
    ("C29", "pin quote-at-line check dropped (equivalent under constants)",
     ' or lines[ln - 1].strip(WS) != f["quote"].encode("utf-8"):', ":"),
    ("C30", "readme: P23 requirement dropped", 'if ENTRY_NAME in ln and b"P23" in ln:', "if ENTRY_NAME in ln:"),
    ("C31", "heading: ATX '#' requirement dropped", 'if s.startswith(b"#") and HEADING in s:', "if HEADING in s:"),
    ("C32", "fenced code blocks not skipped", "        if m:\n", "        if False:\n"),
    ("C33", "stale tested on whole entry (not appended block)", 'stale = b"only when" in block.lower()',
     'stale = b"only when" in entry.lower()'),
    ("C34", "TABLES_SHA256 constant changed", 'TABLES_SHA256 = "13d6e2f9c0', 'TABLES_SHA256 = "13d6e2f9c1'),
    ("C35", "P23 tokens: any() instead of all()", "p23_ok = all(t in prop for t in P23_TOKENS)",
     "p23_ok = any(t in prop for t in P23_TOKENS)"),
    ("C36", "tables_sha: blob presence only", "tables_ok = tables_blob is not None and sha256(tables_blob) == TABLES_SHA256",
     "tables_ok = tables_blob is not None"),
    ("C37", "stale: only-when test dropped entirely", 'stale = b"only when" in block.lower()', "stale = False"),
    ("C38", "pin quote read one line late (off-by-one lines[ln])",
     "lines[ln - 1].strip(WS)", "lines[ln].strip(WS)"),
]

# targeted counters (used as the counter under test against harness mutants)
TARGETS = [
    ("T01", "stale leg reported as rows:heading (only route for a row-only CTL-5 answer)",
     'missed.append("stale")', 'missed.append("rows:heading")'),
    ("T02", "stale leg also reported when readme leg fails (CTL-6 collateral, consistent fields)",
     "    if stale:\n", "    if stale or not readme_ok:\n"),
]

HARNESS_MUTANTS = [
    ("H01", "skip CTL-5 (control removed from CONTROLS)",
     '    ("C3-CTL-5 old-wording-stuffed", mut_old_wording, "identical", 13, "ok", "ok", "ok",\n'
     '     {"stale"}, {"stale"}, set(), set(), 0),\n', ""),
    ("H02", "weaken CTL-5 required stale leg (must_o -> empty)",
     '{"stale"}, {"stale"}, set(), set(), 0),', 'set(), {"stale"}, set(), set(), 0),'),
    ("H03", "accept collateral legs in CTL-6 (allow pin/p23/stale/prefix)",
     '{"readme"}, {"readme"}, set(), set(), 0),',
     '{"readme"}, {"readme", "pin", "p23", "stale", "prefix"}, set(), set(), 0),'),
    ("H04", "drop the TARGET_MISSED requirement for controls (mutant admitted check)",
     'if d["verdict"] != "TARGET_MISSED":', "if False:"),
    ("H05", "skip CTL-6 (readme control removed)",
     '    ("C3-CTL-6 readme-missing", mut_readme_missing, "identical", 13, "ok", "ok", "bad",\n'
     '     {"readme"}, {"readme"}, set(), set(), 0),\n', ""),
    ("H06", "final verdict ignores control count (passed == len -> passed >= 0)",
     "passed == len(CONTROLS)", "passed >= 0"),
]


def one(src, old, new, label):
    n = src.count(old)
    if n != 1:
        raise SystemExit("mutant %s: old text occurs %d times" % (label, n))
    return src.replace(old, new)


def run(argv, timeout=900):
    p = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       timeout=timeout, env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C",
                                             "HOME": S, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"})
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def selftest(counter, tag):
    w = os.path.join(S, "runs", tag, "st")
    os.makedirs(w, exist_ok=True)
    rc, out, err = run(PY + [counter, "--selftest", "--repo", D, "--rev", G, "--work", w])
    fails = [l.strip() for l in out.splitlines() if l.startswith("FAIL")]
    summ = [l for l in out.splitlines() if l.startswith("MADO_P19_FIX_SELFTEST")]
    return {"rc": rc, "summary": summ[0] if summ else "NO SUMMARY (rc=%d) %s" % (rc, err.strip()[-300:]),
            "fails": fails}


def harness(counter, tag, harness_dir=None):
    w = os.path.join(S, "runs", tag, "h")
    os.makedirs(w, exist_ok=True)
    disp = os.path.join(harness_dir, "quality/check-r55-controls.py") if harness_dir else DISP
    argv = PY + [disp, "--claim", "c3", "--repo", D, "--rev", G, "--work", w]
    if counter:
        argv += ["--counter", counter]
    rc, out, err = run(argv)
    lines = [l for l in err.splitlines() if l.startswith("C3-CTL-") or l.startswith("good:")]
    killed = [l.split(":")[0] for l in lines if "FAIL" in l]
    return {"rc": rc, "line": out.strip().splitlines()[-1] if out.strip() else "NO OUTPUT", "killed": killed,
            "lines": lines}


def write_dir(name, text):
    p = os.path.join(DELIV, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    return p


results = {"baseline": {}, "counters": {}, "harness": {}, "targets": {}}

# baseline
results["baseline"]["selftest"] = selftest(CTR, "baseline-counter")
results["baseline"]["harness"] = harness(None, "baseline-harness")
results["baseline"]["stub_vs_real_harness"] = harness(STUB, "baseline-stub")

# counter mutants
for mid, name, old, new in COUNTER_MUTANTS:
    src = one(ctr_src, old, new, mid)
    fname = "%s-%s.py" % (mid, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60])
    path = write_dir(os.path.join("counters", fname) if False else fname, src)
    tag = "counter-" + mid
    st = selftest(path, tag)
    hr = harness(path, tag)
    results["counters"][mid] = {"name": name, "file": fname, "old": old, "new": new, "selftest": st,
                                "harness": hr}
    print(mid, name, "| selftest:", st["summary"], "| harness:", hr["line"], "| killed:", hr["killed"], flush=True)

# targeted counters
for tid, name, old, new in TARGETS:
    src = one(ctr_src, old, new, tid)
    fname = "%s-%s.py" % (tid, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60])
    path = write_dir(fname, src)
    results["targets"][tid] = {"name": name, "file": fname, "harness": harness(path, "target-" + tid)}
    print(tid, name, "| harness:", results["targets"][tid]["harness"]["line"], flush=True)

# harness mutants: build a private harness tree per mutant, run vs stub and vs the targeted counter
for hid, name, old, new in HARNESS_MUTANTS:
    hsrc = one(harn_src, old, new, hid)
    hdir = os.path.join(S, "hm", hid)
    os.makedirs(os.path.join(hdir, "quality"), exist_ok=True)
    with open(os.path.join(hdir, "quality/r55_ctl_c3.py"), "w", encoding="utf-8") as f:
        f.write(hsrc)
    with open(DISP, encoding="utf-8") as f:
        disp = f.read()
    with open(os.path.join(hdir, "quality/check-r55-controls.py"), "w", encoding="utf-8") as f:
        f.write(disp)
    fname = "%s-%s-r55_ctl_c3.py" % (hid, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:50])
    write_dir(fname, hsrc)
    vs_stub = harness(STUB, "h-" + hid + "-stub", hdir)
    # targeted counter pairing
    pair = {"H01": ("C06", "stale leg dropped"), "H02": ("T01", "stale as rows:heading"),
            "H03": ("T02", "stale over-reported when readme missing"), "H05": ("C07", "readme leg dropped")}
    rec = {"name": name, "file": fname, "old": old, "new": new, "vs_stub": vs_stub}
    if hid in pair:
        pid, pdesc = pair[hid]
        cfile = None
        for mid, *_ in COUNTER_MUTANTS:
            if mid == pid:
                cfile = os.path.join(DELIV, results["counters"][mid]["file"])
        for tid, *_ in TARGETS:
            if tid == pid:
                cfile = os.path.join(DELIV, results["targets"][tid]["file"])
        rec["vs_counter"] = {"counter": pid, "desc": pdesc, "result": harness(cfile, "h-" + hid + "-" + pid, hdir)}
        # also run against the original (unmutated) harness for contrast
        rec["vs_counter"]["orig_harness"] = harness(cfile, "h-" + hid + "-" + pid + "-orig")
    results["harness"][hid] = rec
    print(hid, name, "| vs stub:", vs_stub["line"], "| killed:", vs_stub["killed"][:3], flush=True)
    if "vs_counter" in rec:
        print("   vs", pid, rec["vs_counter"]["result"]["line"], "| orig harness:", rec["vs_counter"]["orig_harness"]["line"], flush=True)

with open(os.path.join(S, "summary.json"), "w") as f:
    json.dump(results, f, indent=1)
print("DONE")
