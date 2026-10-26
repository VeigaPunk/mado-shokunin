#!/usr/bin/env python3
"""PRED-C1-r44-v2 - mado-geometry names maximized and fullscreen clients instead of comparing them (C1, operability).

Re-registered BEFORE any round-44 data commit (registration-v2.md), replacing PRED-C1-r44 (frozen at
e2289516a9a857f55cda7be635933e89b931c3da, quality/counters/c1-r44-geometry-states.py), because wave w1 found:
a tool that enables the state logic only inside the counter's sandbox reaches TARGET_MET (w1/CritC1Cheat cheat E);
a tool whose selftest asserts no state verdict reaches TARGET_MET (cheats C, F); and a dump whose matched clients
are all maximized/fullscreen printed `verdict=OK` exit 0 although nothing was compared (w1/CritFsPremise S1).

Scores one committed revision REV of the lane (revision-addressed git reads, ambient GIT_* removed; nothing in the
lane is written). The tool under test is `tools/mado-geometry.py` at REV, or `--tool PATH` for a control.

Contract. Everything the PRED-C1-r42 docstring (quality/counters/c1-r42-geometry.py) states, plus: fsmode is the
`fullscreen` value when it is a JSON integer (not a boolean, not a float) equal to 1 or 2, else 0 (absent, null, 0,
3, -1, true, 2.0, "2", lists and objects are 0); a matched client's verdict is tested in the order BADSIZE (size
none) | FULLSCREEN (fsmode 2) | MAXIMIZED (fsmode 1) | TILED | AGREE | DIFFER; the client line is unchanged except
for the two new words; the summary line carries ` maximized=<n> fullscreen=<n>` between `badsize=<n>` and
` verdict=` exactly when maximized + fullscreen > 0, else it is byte-identical to the round-43 line; the top
verdict is tested in the order NO_SIZE_RULES (rules=0; exit 4) | DIFFER (differ>0; exit 1) | NO_MATCHING_CLIENT
(matched=0; exit 3) | NOT_COMPARED (agree=0 and maximized + fullscreen > 0; exit 5) | OK (exit 0). The reference is
.ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt. Grounding pins: .ufo/waves/round-44/fetch-c1/.

Clauses (all must hold; the counter imports c1-r42-geometry.py from its own directory and reuses its bubblewrap
sandbox, RLIMIT_NPROC = 1 fixture runs, per-run nonce, generator and byte-exact judge; its model is the round-42
model extended by exactly the paragraph above; fixture runs and selftests happen in that sandbox):
  a   the tool exists at REV;
  f   26 fixtures - sgen0..sgen11 (the round-42 nonce lattice with a `fullscreen` value drawn per client from
      absent, 0, 1, 2, true, 3, "2", 2.0, -1, null, and sometimes a `fullscreenClient` value) and the 14 fixed
      fixtures of FIXED; each compares rc and stdout byte-exactly with the model; on rc 0/1/3/4/5 stderr is empty;
  b   `--selftest` exits 0 printing `MADO_GEOMETRY_SELFTEST: k/n passed`, k == n, n >= 80;
  b4  the comparison sites of every function (selftest, main, usage and functions nested in selftest excluded)
      whose body holds a string constant containing `fullscreen` (any case) number >= 6, and flipping each one in a
      copy at the real layout makes the copy's selftest fail for >= 75 % of them (rounded up) - a heuristic;
  b5  state-blind teeth: a copy of the tool whose first lines rebind `json.loads` so that every decoded object's
      `fullscreen` key is renamed `_b5_fullscreen` (so no client carries a state) must FAIL its own selftest
      (non-zero exit, k != n, or no summary line): the selftest asserts state verdicts through the JSON path;
  e   environment invariance: the inputs of the fixed fixtures fs0, max0, fsmix0, fsclient0 and fsagree0 are run a
      second time OUTSIDE the sandbox (plain `python3 -I <tool>`, the counter's own environment minus GIT_*, the
      real HOME, cwd = the fixture directory, 30 s timeout) and stdout and exit code must equal the sandboxed run;
  g   the round-42 clause g holds (standard-library imports json os re stat sys only; no denied call, name, string
      or keyword unpacking);
  r   no harm to the round-43 contract: `c1-r42-geometry.py --repo REPO --rev REV --tool <the same bytes>
      --nonce <derived>` exits 0 and its last line holds ` verdict=TARGET_MET ` (a timeout is a failure).

Output: one line per clause/fixture, a `PRED-C1-r44-v2 clauses=<k:v ...>` line, and the final line
`PRED-C1-r44-v2: fixtures=k/26 tool=present|absent verdict=TARGET_MET|TARGET_MISSED rev=<full hash> nonce=<nonce>`.
TARGET_MET (exit 0) iff every clause holds and k == 26; else exit 1; a setup failure (no sandbox, unresolved
revision, unreadable --tool, missing --work directory) prints `PRED-C1-r44-v2 SETUP <reason>` and exits 2.
Scratch: `--work DIR`, else $C1R44_TMP, else $TMPDIR (never a hardcoded /tmp).

Residuals (declared): a tool that holds a model of the contract is an implementation; b4 counts sites only in
functions naming `fullscreen` (b5 is the load-bearing teeth clause); b5 binds the JSON path only - a tool that
parses JSON without json.loads, or detects the rebinding, defeats it; e compares one second environment (a tool
can still detect an unusual one); whether a live maximized or fullscreen window reports the work-area or monitor
box is the pinned sources' fact, not scored; the documentation rows (SKILL.md, PROVINCE.md) are not scored.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import math
import os
import random
import re
import secrets
import shutil
import subprocess
import sys
import tempfile

PRED = "PRED-C1-r44-v2"
TOOL = "tools/mado-geometry.py"
TOTAL = 26
N_GEN = 12
MIN_SELFTEST = 80
MIN_STATE_SITES = 6
KILL_FRACTION = 0.75
HERE = os.path.dirname(os.path.abspath(__file__))
OLD_PATH = os.path.join(HERE, "c1-r42-geometry.py")

_spec = importlib.util.spec_from_file_location("c1r42", OLD_PATH)
old = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(old)
Setup = old.Setup


# ------------------------------------------------------------- the model
def fsmode_of(c):
    f = c.get("fullscreen")
    if type(f) is int and f in (1, 2):
        return f
    return 0


def model_out_states(clients_raw, texts):
    """The round-42 model plus the round-44 state verdicts."""
    try:
        doc = json.loads(clients_raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None, "bad_json"
    if not isinstance(doc, list) or any(not isinstance(c, dict) for c in doc):
        return None, "bad_json"
    rules, other, unsup = old.model_rules(texts)
    out = ["MADO_GEOM_RULE: n=%d file=%d effect=%s arg=%s class=%s"
           % (n, r[0], r[1], r[2], r[4]) for n, r in enumerate(rules, 1)]
    t = dict(clients=0, matched=0, unmapped=0, AGREE=0, DIFFER=0, TILED=0,
             BADSIZE=0, MAXIMIZED=0, FULLSCREEN=0)
    for c in doc:
        if c.get("mapped") is False:
            t["unmapped"] += 1
            continue
        t["clients"] += 1
        cls = c["class"] if isinstance(c.get("class"), str) else ""
        want, frule = None, "-"
        if not any(ord(ch) < 32 for ch in cls):
            for r in rules:
                if re.fullmatch(r[4], cls):
                    if r[1] == "size":
                        want = r[3]
                    else:
                        frule = r[3]
        if want is None:
            continue
        t["matched"] += 1
        sz = c.get("size")
        size = None
        if isinstance(sz, list) and len(sz) == 2 and all(
                type(v) is int and v >= 0 for v in sz):
            size = (sz[0], sz[1])
        fl = c.get("floating") is True
        mode = fsmode_of(c)
        if size is None:
            v = "BADSIZE"
        elif mode == 2:
            v = "FULLSCREEN"
        elif mode == 1:
            v = "MAXIMIZED"
        elif not fl:
            v = "TILED"
        elif size == want:
            v = "AGREE"
        else:
            v = "DIFFER"
        t[v] += 1
        addr = c["address"] if isinstance(c.get("address"), str) else "-"
        out.append("MADO_GEOM_CLIENT: addr=%s class=%s floating=%s size=%s "
                   "want=%dx%d float_rule=%s verdict=%s" % (
                       json.dumps(addr), json.dumps(cls),
                       "true" if fl else "false",
                       "%dx%d" % size if size else "-", want[0], want[1],
                       frule, v))
    nsize = sum(1 for r in rules if r[1] == "size")
    if nsize == 0:
        verdict, rc = "NO_SIZE_RULES", 4
    elif t["DIFFER"]:
        verdict, rc = "DIFFER", 1
    elif t["matched"] == 0:
        verdict, rc = "NO_MATCHING_CLIENT", 3
    elif t["AGREE"] == 0 and t["MAXIMIZED"] + t["FULLSCREEN"] > 0:
        verdict, rc = "NOT_COMPARED", 5
    else:
        verdict, rc = "OK", 0
    states = ""
    if t["MAXIMIZED"] + t["FULLSCREEN"] > 0:
        states = " maximized=%d fullscreen=%d" % (t["MAXIMIZED"], t["FULLSCREEN"])
    out.append("MADO_GEOMETRY: rules=%d float_rules=%d other=%d unsupported=%d "
               "clients=%d matched=%d unmapped=%d agree=%d differ=%d tiled=%d "
               "badsize=%d%s verdict=%s" % (
                   nsize, len(rules) - nsize, other, unsup, t["clients"],
                   t["matched"], t["unmapped"], t["AGREE"], t["DIFFER"],
                   t["TILED"], t["BADSIZE"], states, verdict))
    return "\n".join(out) + "\n", rc


old.model_out = model_out_states  # old.case_files judges against the extended model
_old_judge = old.judge


def judge_v2(rc, out, err, want_out, want_rc):
    ok, why = _old_judge(rc, out, err, want_out, want_rc)
    if ok and want_rc == 5 and err:
        return 0, "stderr=%r" % err[:80]
    return ok, why


old.judge = judge_v2

# ------------------------------------------------------------- fixtures
FS_POOL = ["absent", "absent", "absent", 0, 1, 1, 2, 2, 2, True, 3, "2", 2.0, -1, None]
GK = "org.omarchy.gkeep"
GKRX = "^(org.omarchy.gkeep)$"
GKCONF = ("windowrule = float on, match:class %s\nwindowrule = size 420 500, match:class %s\n"
          % (GKRX, GKRX))


def gen_state_clients(rng, wants):
    out = old.gen_clients(rng, wants)
    for c in out:
        v = rng.choice(FS_POOL)
        if v != "absent":
            c["fullscreen"] = v
        if rng.randrange(4) == 0:
            c["fullscreenClient"] = rng.choice([0, 1, 2])
    return out


def score_sgen(tool, tmp, rev, nonce, i):
    rng = old.rng_for(rev, nonce, "sgen", i)
    texts, wants = old.gen_texts(rng)
    clients = json.dumps(gen_state_clients(rng, wants))
    return old.case_files(tool, tmp, "sgen%d" % i, clients, texts, via_stdin=bool(i % 2))


def G(size, mode="absent", fl=True, **kw):
    d = {"address": "0x%x" % (len(json.dumps(size)) * 7), "class": GK, "size": size,
         "floating": fl}
    if mode != "absent":
        d["fullscreen"] = mode
    d.update(kw)
    return d


def one(name, clients, texts=None, via_stdin=False):
    def fn(tool, tmp, rev, nonce):
        raw = clients if isinstance(clients, str) else json.dumps(clients)
        return old.case_files(tool, tmp, name, raw, texts or [GKCONF], via_stdin=via_stdin)
    return fn


def many(name, cases):
    def fn(tool, tmp, rev, nonce):
        for k, (clients, texts) in enumerate(cases):
            raw = clients if isinstance(clients, str) else json.dumps(clients)
            ok, why = old.case_files(tool, tmp, "%s-%d" % (name, k), raw, texts or [GKCONF])
            if not ok:
                return 0, "case %d: %s" % (k, why)
        return 1, "ok"
    return fn


def score_fsmany0(tool, tmp, rev, nonce):
    rng = old.rng_for(rev, nonce, "fsmany", 0)
    cl = [G([rng.choice([420, 2560, 1280]), rng.choice([500, 1440, 700])],
            rng.choice(FS_POOL), fl=rng.choice([True, False]), address="0x%x" % k)
          for k in range(200)]
    return old.case_files(tool, tmp, "fsmany0", json.dumps(cl), [GKCONF])


FIXED = [
    ("fs0", one("fs0", [G([2560, 1440], 2)])),
    ("fsagree0", one("fsagree0", [G([420, 500], 2)])),
    ("max0", one("max0", [G([2544, 1380], 1, fl=False)])),
    ("maxfloat0", one("maxfloat0", [G([2544, 1380], 1)])),
    ("fsbad0", many("fsbad0", [([G([420.0, 500], 2)], None), ([G(None, 1)], None),
                               ([G([True, 500], 2)], None)])),
    ("fsvals0", many("fsvals0", [([G([421, 500], v)], None) for v in
                                 (True, False, 3, 2.0, "2", -1, None, [2], {"internal": 2}, 0)])),
    ("fsmix0", one("fsmix0", [G([2560, 1440], 2, address="0x1"), G([421, 500], address="0x2"),
                              G([420, 500], address="0x3"), G([1, 1], fl=False, address="0x4"),
                              G([2544, 1380], 1, address="0x5")])),
    ("fsunmatched0", one("fsunmatched0", [{"class": "kitty", "size": [9, 9], "floating": True,
                                           "fullscreen": 2}, G([420, 500])])),
    ("fsunmapped0", one("fsunmapped0", [G([2560, 1440], 2, mapped=False), G([420, 500])])),
    ("fsstdin0", one("fsstdin0", [G([2560, 1440], 2), G([2544, 1380], 1)], via_stdin=True)),
    ("fsdup0", many("fsdup0", [
        ('[{"class": "%s", "size": [9, 9], "floating": true, "fullscreen": 0, "fullscreen": 2}]' % GK, None),
        ('[{"class": "%s", "size": [9, 9], "floating": true, "fullscreen": 2, "fullscreen": 0}]' % GK, None)])),
    ("fsmany0", score_fsmany0),
    ("fsclient0", one("fsclient0", [G([421, 500], 0, fullscreenClient=2),
                                    G([421, 500], fullscreenClient=1)])),
    ("fsnorules0", many("fsnorules0", [([G([2560, 1440], 2)],
                                        ["windowrule = float on, match:class %s\n" % GKRX]),
                                       ([G([2560, 1440], 2)], [""])])),
]


INVARIANT_INPUTS = {
    "fs0": [G([2560, 1440], 2)],
    "max0": [G([2544, 1380], 1, fl=False)],
    "fsmix0": [G([2560, 1440], 2, address="0x1"), G([421, 500], address="0x2"),
               G([420, 500], address="0x3"), G([1, 1], fl=False, address="0x4"),
               G([2544, 1380], 1, address="0x5")],
    "fsclient0": [G([421, 500], 0, fullscreenClient=2), G([421, 500], fullscreenClient=1)],
    "fsagree0": [G([420, 500], 2)],
}


# ------------------------------------------------------------- clauses
def state_sites(src):
    tree = ast.parse(src)
    nested = set()
    fns = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    for fn in fns:
        if fn.name == "selftest":
            for inner in ast.walk(fn):
                if isinstance(inner, ast.FunctionDef) and inner is not fn:
                    nested.add(id(inner))
    sites = []
    for fn in fns:
        if fn.name in old.NOT_SITES or id(fn) in nested:
            continue
        named = any(isinstance(c, ast.Constant) and isinstance(c.value, str)
                    and "fullscreen" in c.value.lower() for c in ast.walk(fn))
        if not named:
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.Compare) and len(node.ops) == 1 \
                    and type(node.ops[0]) in old.FLIP:
                sites.append((fn.name, node.lineno, node.col_offset))
    return sorted(set(sites))


def state_teeth(src, tmp):
    sites = state_sites(src)
    if len(sites) < MIN_STATE_SITES:
        print("%s clause=b4 sites=%d (<%d)" % (PRED, len(sites), MIN_STATE_SITES))
        return False
    need = math.ceil(KILL_FRACTION * len(sites))
    killed = 0
    for n, site in enumerate(sites):
        mutated = old.mutate_source(src, site)
        if mutated is None:
            print("%s clause=b4 mutant=%d site=%s:%d unmutated" % (PRED, n, site[0], site[1]))
            continue
        rc, k, n_, has = old.run_selftest_copy(mutated, tmp, "s%d" % n)
        dead = rc != 0 or not has or k != n_
        killed += dead
        print("%s clause=b4 mutant=%d site=%s:%d killed=%d" % (PRED, n, site[0], site[1], dead))
    print("%s clause=b4 sites=%d killed=%d need=%d" % (PRED, len(sites), killed, need))
    return killed >= need


def regress(repo, rev, tool, tmp, nonce):
    sub = hashlib.sha256(("regress:" + nonce).encode()).hexdigest()[:16]
    env = {k: v for k, v in old.ENV.items()}
    env["C1R42_TMP"] = tmp
    try:
        p = subprocess.run([os.path.realpath(sys.executable), "-I", OLD_PATH, "--repo", repo,
                            "--rev", rev, "--tool", tool, "--nonce", sub],
                           capture_output=True, env=env, timeout=1800)
    except subprocess.TimeoutExpired:
        print("%s clause=r timeout" % PRED)
        return False
    lines = p.stdout.decode("utf-8", "replace").strip().splitlines()
    last = lines[-1] if lines else ""
    ok = p.returncode == 0 and " verdict=TARGET_MET " in last
    print("%s clause=r rc=%d %s" % (PRED, p.returncode, last))
    return ok


B5_PREFIX = (
    "import json as _b5_json\n"
    "_b5_loads = _b5_json.loads\n"
    "def _b5_hook(d):\n"
    "    return {('_b5_' + k if k == 'fullscreen' else k): v for k, v in d.items()}\n"
    "def _b5_patched(s, *a, **k):\n"
    "    k['object_hook'] = _b5_hook\n"
    "    return _b5_loads(s, *a, **k)\n"
    "_b5_json.loads = _b5_patched\n")


def state_blind(src, tmp):
    text = src
    lines = text.split("\n")
    k = 1 if lines and lines[0].startswith("#!") else 0
    text = "\n".join(lines[:k] + [B5_PREFIX] + lines[k:])
    rc, k_, n, has = old.run_selftest_copy(text, tmp, "b5")
    dead = rc != 0 or not has or k_ != n
    print("%s clause=b5 state_blind_selftest rc=%s selftest=%d/%d failed=%d" % (PRED, rc, k_, n, dead))
    return dead


INVARIANCE = ("fs0", "max0", "fsmix0", "fsclient0", "fsagree0")


def invariance(tool, tmp):
    """Clause e: the same inputs, sandboxed (old.execute) and unsandboxed, must give the same stdout and rc."""
    ok_all = True
    for name, fn in FIXED:
        if name not in INVARIANCE:
            continue
        clients = INVARIANT_INPUTS[name]
        d = old.prepare(tmp, "inv-" + name)
        cpath = old.put(d, "c.json", json.dumps(clients))
        rpath = old.put(d, "r0.conf", GKCONF)
        argv = ["--clients", cpath, "--rules", rpath]
        rc1, out1, _e1 = old.execute(tool, d, argv)
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        try:
            p = subprocess.run([os.path.realpath(sys.executable), "-I", tool] + argv, cwd=d, env=env,
                               capture_output=True, timeout=30, stdin=subprocess.DEVNULL)
            rc2, out2 = p.returncode, p.stdout
        except subprocess.TimeoutExpired:
            rc2, out2 = None, b""
        same = rc1 == rc2 and out1 == out2 and rc1 is not None
        ok_all &= same
        print("%s clause=e fixture=%s sandbox_rc=%s plain_rc=%s same=%d" % (PRED, name, rc1, rc2, same))
    return ok_all


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--tool", default=None, help="score this file instead of REV's tool (controls)")
    ap.add_argument("--nonce", default=None)
    ap.add_argument("--work", default=None, help="scratch parent (else $C1R44_TMP, else $TMPDIR)")
    args = ap.parse_args()
    nonce = args.nonce or secrets.token_hex(8)
    old.NONCE[0] = nonce
    repo = os.path.abspath(args.repo)
    rev = old.resolve(repo, args.rev)
    old.check_sandbox()
    if args.work and not os.path.isdir(args.work):
        raise Setup("work_dir_missing %s" % args.work)
    try:
        src = open(args.tool, "rb").read() if args.tool else old.git(repo, "show", "%s:%s" % (rev, TOOL))
    except OSError as exc:
        raise Setup("unreadable_tool %s" % exc)
    present = src is not None
    cl = {"a": int(present), "b": 0, "b4": 0, "b5": 0, "e": 0, "g": 0, "r": 0}
    passed = 0
    if present:
        cl["g"] = int(old.imports_ok(src))
        parent = args.work or os.environ.get("C1R44_TMP") or None
        tmp = tempfile.mkdtemp(prefix="mado-c1r44-", dir=parent)
        os.chmod(tmp, 0o755)
        try:
            td = os.path.join(tmp, old.opaque("real"), "tool")
            os.makedirs(td)
            os.chmod(os.path.dirname(td), 0o755)
            os.chmod(td, 0o755)
            tool = os.path.join(td, "mado-geometry.py")
            with open(tool, "wb") as fh:
                fh.write(src)
            rc, k, n, has = old.selftest_result(tool, td)
            cl["b"] = int(rc == 0 and has and k == n and n >= MIN_SELFTEST)
            print("%s clause=b rc=%s selftest=%d/%d" % (PRED, rc, k, n))
            if cl["b"]:
                cl["b4"] = int(state_teeth(src.decode("utf-8", "replace"), tmp))
                cl["b5"] = int(state_blind(src.decode("utf-8", "replace"), tmp))
            cl["e"] = int(invariance(tool, tmp))
            cases = [("sgen%d" % i, (lambda i=i: score_sgen(tool, tmp, rev, nonce, i)))
                     for i in range(N_GEN)]
            for name, fn in FIXED:
                cases.append((name, (lambda fn=fn: fn(tool, tmp, rev, nonce))))
            assert len(cases) == TOTAL, len(cases)
            for name, fn in cases:
                ok, why = fn()
                passed += ok
                print("%s fixture=%s ok=%d %s" % (PRED, name, ok, why))
            rtmp = os.path.join(tmp, "regress")
            os.makedirs(rtmp)
            cl["r"] = int(regress(repo, rev, tool, rtmp, nonce))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    met = all(cl.values()) and passed == TOTAL
    print("%s clauses=%s" % (PRED, " ".join("%s:%d" % kv for kv in sorted(cl.items()))))
    print("%s: fixtures=%d/%d tool=%s verdict=%s rev=%s nonce=%s" % (
        PRED, passed, TOTAL, "present" if present else "absent",
        "TARGET_MET" if met else "TARGET_MISSED", rev, nonce))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as exc:
        print("%s SETUP %s" % (PRED, exc))
        sys.exit(2)
