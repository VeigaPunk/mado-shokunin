#!/usr/bin/env python3
"""Round-42 C1 controls (CTL_C1): the frozen counter `quality/counters/c1-r42-geometry.py` must
(1) reach TARGET_MET for the reference tool, (2) score the absent tool at base TARGET_MISSED, and
(3) score every do-nothing control, every cheat and every single-defect mutant below TARGET_MET.
A mutant whose pattern is not found exactly once is a probe that mutates nothing and aborts the run.

  python3 -I .ufo/waves/round-42/ctl/run-c1-controls.py --repo . --rev <rev>   (stdout: the receipt)
"""
import argparse
import concurrent.futures
import os
import re
import subprocess
import sys
import tempfile

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
REF = os.path.join(LANE, ".ufo/waves/round-42/c1/ctl-ref-tool.py.txt")
COUNTER = os.path.join(LANE, "quality/counters/c1-r42-geometry.py")
NONCE = "42aa42aa42aa42aa"

MUTANTS = [
    ("M01-fifo-block", "os.O_RDONLY | os.O_NONBLOCK", "os.O_RDONLY"),
    ("M02-nonregular-ok", "if not stat.S_ISREG(os.fstat(fd).st_mode):", "if False:"),
    ("M04-toolarge-ge", 'if len(data) > MAX_BYTES:\n        raise Setup("too_large")\n    return data',
     'if len(data) >= MAX_BYTES:\n        raise Setup("too_large")\n    return data'),
    ("M05-stdin-short", "data = stdin.read(MAX_BYTES + 1)", "data = stdin.read(MAX_BYTES)"),
    ("M06-unicode-digits", 'NUM = re.compile(r"[0-9]{1,5}")', 'NUM = re.compile(r"\\d{1,5}")'),
    ("M07-regex-201", "){1,200}\")", "){1,201}\")"),
    ("M08-possessive", 'for bad in ("(?", "*+", "++", "?+"):', 'for bad in ("(?", "*+", "++"):'),
    ("M09-search", "re.fullmatch(rx, cls)", "re.search(rx, cls)"),
    ("M10-ctl-le", "if any(ord(ch) < 0x20 for ch in cls):", "if any(ord(ch) <= 0x20 for ch in cls):"),
    ("M10b-ctl-del", "if any(ord(ch) < 0x20 for ch in cls):", "if any(ord(ch) < 0x80 for ch in cls):"),
    ("M11-mapped-falsy", 'if c.get("mapped") is False:', 'if not c.get("mapped", True):'),
    ("M12-floating-truthy", 'floating = c.get("floating") is True', 'floating = bool(c.get("floating"))'),
    ("M13-size-bool", "isinstance(v, int) and not isinstance(v, bool) and v >= 0", "isinstance(v, int) and v >= 0"),
    ("M14-size-zero", "isinstance(v, int) and not isinstance(v, bool) and v >= 0", "isinstance(v, int) and not isinstance(v, bool) and v > 0"),
    ("M15-size-float", "isinstance(v, int) and not isinstance(v, bool) and v >= 0", "isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0"),
    ("M16-first-wins", '        for r in rules:\n            if matches(r["rx"], cls):', '        for r in reversed(rules):\n            if matches(r["rx"], cls):'),
    ("M17-no-rules-lost", "if size_rules == 0:", "if size_rules < 0:"),
    ("M18-differ-gt1", 'elif t["differ"] > 0:', 'elif t["differ"] > 1:'),
    ("M19-fields-ge2", 'len(fields) == 2', 'len(fields) >= 2'),
    ("M21-float-true", 'args[0] in ("on", "off")', 'args[0] in ("on", "off", "true")'),
    ("M22-v2-prefix", 'RULE_LINE = re.compile(r"windowrule[ \\t]*=(.*)")', 'RULE_LINE = re.compile(r"windowrule.*?=(.*)")'),
    ("M23-strip-all", 'line = raw.strip(" \\t")', "line = raw.strip()"),
    ("M24-unicode-split", 're.split("[ \\t]+", fields[0])', "fields[0].split()"),
    ("M25-ensure-ascii", "json.dumps(addr)", "json.dumps(addr, ensure_ascii=False)"),
    ("M26-json-replace", 'doc = json.loads(data.decode("utf-8"))', 'doc = json.loads(data.decode("utf-8", "replace"))'),
    ("M27-nomatch-rc", 'verdict, rc = "NO_MATCHING_CLIENT", 3', 'verdict, rc = "NO_MATCHING_CLIENT", 1'),
    ("M28-rules-first", '    if clients == "-":\n        data = stdin.read(MAX_BYTES + 1)\n        if len(data) > MAX_BYTES:\n            raise Setup("too_large")\n    else:\n        data = read_regular(clients)\n    texts = [read_regular(p).decode("utf-8", "replace") for p in rules]\n',
     '    texts = [read_regular(p).decode("utf-8", "replace") for p in rules]\n    if clients == "-":\n        data = stdin.read(MAX_BYTES + 1)\n        if len(data) > MAX_BYTES:\n            raise Setup("too_large")\n    else:\n        data = read_regular(clients)\n'),
    ("M29-file-index-0", "enumerate(rule_texts, 1)", "enumerate(rule_texts, 0)"),
    ("M30-raw-digits", 'arg = "%dx%d" % (int(args[0]), int(args[1])) if effect == "size" else args[0]',
     'arg = "%sx%s" % (args[0], args[1]) if effect == "size" else args[0]'),
    ("M31-tiled-lost", "elif not floating:", "elif floating is None:"),
    ("M32-escape-dollar", "\\\\[.\\-()|*+?^$\\\\]){1,200}", "\\\\[.\\-()|*+?^\\\\]){1,200}"),
    ("M33-max-bytes", "MAX_BYTES = 1048576", "MAX_BYTES = 1048577"),
    ("M34-no-compile", "    try:\n        re.compile(rx)\n    except re.error:\n        return False\n    return True", "    return True"),
    ("M35-class-str", 'cls = c.get("class") if isinstance(c.get("class"), str) else ""', 'cls = str(c.get("class", ""))'),
    ("M36-element-dict", "not all(isinstance(c, dict) for c in doc)", "False"),
    ("M37-addr-default", 'addr = c.get("address") if isinstance(c.get("address"), str) else "-"', 'addr = str(c.get("address", "-"))'),
    ("M39-match-class-space", 'MATCH_FIELD = re.compile(r"match:class[ \\t]+(.+)")', 'MATCH_FIELD = re.compile(r"match:class[ \\t]*(.+)")'),
    ("M40-last-float", 'frule = r["want"]', 'frule = frule if frule != "-" else r["want"]'),
]


# Mutants found equivalent while building the freeze (the counter cannot and need not kill them):
#   M03 `while len(data) <= MAX_BYTES` -> `<`: the one os.read asks for MAX+1-len bytes, which a regular
#       file returns whole, so the loop bound is never the deciding test (equivalent for regular files).
#   M20 dropping `"#" not in body`: the regex alphabet has no `#`, and a `#` in field 0 breaks the token
#       grammar, so the test was dead; the contract sentence and the code were deleted instead.
#   M38 `{1,200}` -> `{0,200}`: MATCH_FIELD's `(.+)` already requires a non-empty regex.
EQUIVALENT = ("M03-read-short", "M20-hash-allowed", "M38-regex-empty")


def do_nothing():
    ref = open(REF).read()
    c = {}
    c["D1-constant"] = ('import sys\nprint("MADO_GEOMETRY: rules=0 float_rules=0 other=0 unsupported=0 clients=0 matched=0 unmapped=0 '
                        'agree=0 differ=0 tiled=0 badsize=0 verdict=NO_SIZE_RULES")\nsys.exit(4)\n')
    c["D2-echo"] = 'import sys\nsys.stdout.write(sys.stdin.read())\n'
    c["D3-selftest-only"] = ('import sys\nif sys.argv[1:] == ["--selftest"]:\n    print("MADO_GEOMETRY_SELFTEST: 60/60 passed")\n'
                             '    sys.exit(0)\nprint("MADO_GEOMETRY: SETUP usage")\nsys.exit(2)\n')
    # zero-test selftest: the reference with its selftest body replaced by a fixed pass line
    i = ref.index("def selftest():")
    j = ref.index("def main():")
    c["K1-zero-test-selftest"] = ref[:i] + 'def selftest():\n    print("MADO_GEOMETRY_SELFTEST: 73/73 passed")\n    return 0\n\n\n' + ref[j:]
    # fingerprint selftest: passes only when the file is byte-identical to the reference
    fp = ref.replace("def selftest():\n", "def selftest():\n    import hashlib\n    return 0\n\n\ndef _unused():\n", 1)
    c["K2-no-op-selftest-then-mutable"] = fp.replace("import json\n", "import json\n", 1)
    c["K3-exec-model"] = ref.replace("import json\n", "import json\nEXEC = exec\n", 1).replace(
        "def main():", "def main():\n    EXEC('pass')", 1)
    c["K4-child-interpreter"] = ref.replace("import json\n", "import json\nimport subprocess\n", 1)
    c["K5-getattr"] = ref.replace("def main():", "def main():\n    getattr(sys, 'exit')", 1)
    return c


def run_counter(path, nonce, rev, repo, tmp):
    env = dict(os.environ, C1R42_TMP=tmp)
    cmd = [sys.executable, "-I", COUNTER, "--repo", repo, "--rev", rev, "--nonce", nonce]
    if path:
        cmd += ["--tool", path]
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    last = [ln for ln in p.stdout.splitlines() if ln.startswith("PRED-C1-r42:")]
    cl = [ln for ln in p.stdout.splitlines() if " clauses=" in ln]
    failed = [ln.split("fixture=")[1].split(" ok=0")[0] for ln in p.stdout.splitlines() if " ok=0 " in ln]
    return p.returncode, (last[-1] if last else "NO_FINAL_LINE " + p.stdout[-200:] + p.stderr[-200:]), (cl[-1].split(" clauses=")[1] if cl else "-"), failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=LANE)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--scratch", default="/fast/scratch/c1r42-ctl")
    args = ap.parse_args()
    os.makedirs(args.scratch, exist_ok=True)
    ref = open(REF).read()
    jobs = [("REF", REF), ("BASE-absent", None)]
    files = {}
    for name, old, new in MUTANTS:
        n = ref.count(old)
        if n != 1:
            print("CTL_C1 ABORT mutant %s pattern found %d times" % (name, n))
            return 2
        path = os.path.join(args.scratch, name + ".py")
        open(path, "w").write(ref.replace(old, new))
        jobs.append((name, path))
    for name, text in do_nothing().items():
        path = os.path.join(args.scratch, name + ".py")
        open(path, "w").write(text)
        jobs.append((name, path))
    results = {}
    tmp = tempfile.mkdtemp(prefix="c1r42ctl-", dir=args.scratch)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(run_counter, p, NONCE, args.rev, args.repo, tmp): n for n, p in jobs}
        for f in concurrent.futures.as_completed(futs):
            results[futs[f]] = f.result()
    bad = 0
    print("CTL_C1: rev=%s nonce=%s controls=%d equivalent_mutants_excluded=%s" % (args.rev, NONCE, len(jobs) - 2, ",".join(EQUIVALENT)))
    for name, _ in jobs:
        rc, last, clauses, failed = results[name]
        met = "TARGET_MET" in last and "TARGET_MISSED" not in last
        expect_met = name == "REF"
        ok = met == expect_met
        bad += not ok
        print("%s %-34s met=%d clauses=[%s] failed_fixtures=%s" % ("ok " if ok else "BAD", name, met, clauses, ",".join(failed[:6]) or "-"))
    print("CTL_C1 VERDICT: %s (controls scoring TARGET_MET: %d of %d; reference met: %d)" % (
        "PASS" if not bad else "FAIL", sum(1 for n, _ in jobs if n != "REF" and "TARGET_MET" in results[n][1] and "MISSED" not in results[n][1]),
        len(jobs) - 1, int("TARGET_MET" in results["REF"][1])))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
