#!/usr/bin/env python3
"""Verify every quote in findings.md exists verbatim at its cited location."""
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
CHECKS = [
    ("quality/counters/c1-r42-geometry.py", 21, 22, "a clients input that is not UTF-8 JSON holding a list whose"),
    ("quality/counters/c1-r42-geometry.py", 22, 22, "every element is an object is bad_json (an empty input included). Order of checks: usage, then the"),
    ("quality/counters/c1-r42-geometry.py", 16, 17, "`--clients V` exactly once and `--rules V` one or more times"),
    ("quality/counters/c1-r42-geometry.py", 65, 66, "a run that hits 3 timeouts (30 s each; 60 s for a selftest) is not run any further, and every"),
    ("quality/counters/c1-r42-geometry.py", 66, 66, "remaining fixture and selftest fails."),
    ("quality/counters/c1-r42-geometry.py", 10, 10, "sha256(REV:NONCE:tag:i)"),
    ("quality/counters/c1-r42-geometry.py", 78, 78, "the source calls none of exec, eval,"),
    ("quality/counters/c1-r42-geometry.py", 81, 81, "never names `__file__`, `sys.argv[0]`, `sys.executable` or `sys.modules`"),
    ("quality/counters/c1-r42-geometry.py", 87, 88, "clause g is a"),
    ("quality/counters/c1-r42-geometry.py", 88, 89, "RE2 - the REGEX alphabet is restricted so the two agree on it"),
    ("quality/counters/c1-r42-geometry.py", 9, 9, "fixture runs also execute under RLIMIT_NPROC = 1"),
    ("quality/counters/c1-r42-geometry.py", 14, 14, "restated here, the code below being the same sentence."),
    ("quality/counters/c1-r42-geometry.py", 202, 202, "nproc: run the tool under RLIMIT_NPROC = 1 (any fork/exec fails)."),
    ("quality/counters/c1-r42-geometry.py", 189, 190, "so a child that does"),
    ("quality/counters/c1-r42-geometry.py", 190, 190, "not redirect its own children's stdin is visible to the stub."),
    ("quality/counters/c1-r42-geometry.py", 367, 367, "n_files = rng.randrange(1, 4)"),
    ("quality/counters/c1-r42-geometry.py", 764, 764, 'rng = rng_for("many", nonce, "many", 0)'),
    ("quality/counters/c1-r42-geometry.py", 268, 268, "doc = json.loads(clients_raw.decode(\"utf-8\"))"),
    ("quality/counters/c1-r42-geometry.py", 834, 834, "return bool(mods) and mods <= STDLIB_ALLOW and not (mods & STDLIB_DENY)"),
    ("quality/counters/c1-r42-geometry.py", 847, 847, "tree = ast.parse(src)"),
    ("quality/counters/c1-r42-geometry.py", 931, 931, "return killed >= KILL_NEED and forced_dead"),
    ("quality/counters/c1-r42-geometry.py", 493, 493, "via_stdin=bool(i % 2))"),
    ("quality/counters/c1-r42-geometry.py", 435, 435, 'cmd = sandbox_cmd(["/usr/bin/prlimit", "--nproc=1:1", py, "-I", tool] + argv,'),
    (".ufo/waves/round-43/registration.md", None, None, "fresh nonce per run, replayable with `--nonce`"),
    (".ufo/waves/round-43/receipts/ctl-c1.txt", None, None, "reference met: 1"),
    (".ufo/waves/round-42/c1/ctl-ref-tool.py.txt", 17, 17, "`--clients V` exactly once and `--rules V` one or more times, in any order."),
    (".ufo/waves/round-42/c1/ctl-ref-tool.py.txt", 22, 23, "a clients input that is not UTF-8 JSON holding a list whose every"),
]

fails = 0
for rel, lo, hi, frag in CHECKS:
    path = LANE + "/" + rel
    lines = open(path, "rb").read().decode("utf-8", "replace").splitlines()
    if lo is None:
        hit = any(frag in ln for ln in lines)
        where = "anywhere"
    else:
        seg = "\n".join(lines[lo - 1:hi])
        hit = frag in seg
        where = ":%d-%d" % (lo, hi)
    print("%s %s %s %r" % ("OK  " if hit else "FAIL", rel, where, frag[:60]))
    fails += 0 if hit else 1
print("verify-quotes: %d checks, %d failures" % (len(CHECKS), fails))
sys.exit(1 if fails else 0)
