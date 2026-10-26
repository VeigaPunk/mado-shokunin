#!/usr/bin/env python3
"""PRED-C1-r44 - mado-geometry reports maximized and fullscreen clients as such (C1, operability).

Frozen at the round-44 freeze, before any round-44 data. Scores one committed revision REV of the
lane (revision-addressed git reads, ambient GIT_* removed; nothing in the lane is written). The tool
under test is `tools/mado-geometry.py` at REV (or `--tool PATH` for a control).

Why. Hyprland 0.56.2 sets a maximized window's box to the workspace work area and a fullscreen
window's box to the monitor box (src/managers/fullscreen/handler/FullscreenHandler.cpp,
setTargetSizeAndPosition), and `hyprctl clients -j` prints the internal mode as the integer
`fullscreen` (src/debug/HyprCtl.cpp; eFullscreenMode in FullscreenController.hpp: 0 none,
1 maximized, 2 fullscreen). The round-43 tool ignores that field, so a fullscreen gkeep window
whose rule asks 420x500 is reported DIFFER (a false report) and a maximized tiled one TILED.
Pins: .ufo/waves/round-44/fetch-c1/ (receipts/fetch-sha256.txt).

The contract extension (the reference is .ufo/waves/round-44/c1/ctl-ref-tool.py.txt; everything
the round-43 contract of PRED-C1-r42 says stays in force): fsmode is the `fullscreen` value when
it is a JSON integer (not a boolean, not a float) equal to 1 or 2, else 0 (absent, null, 0, 3, -1,
true, 2.0, "2", lists and objects are 0). A matched client's verdict is tested in the order
BADSIZE (size none) | FULLSCREEN (fsmode 2) | MAXIMIZED (fsmode 1) | TILED | AGREE | DIFFER.
The client line is unchanged except for the two new verdict words. The summary line carries
` maximized=<n> fullscreen=<n>` between `badsize=<n>` and ` verdict=` exactly when
maximized + fullscreen > 0; otherwise it is byte-identical to the round-43 line. FULLSCREEN and
MAXIMIZED clients count as matched and never as differ, so the top verdict rules (NO_SIZE_RULES,
DIFFER, NO_MATCHING_CLIENT, OK and their exit codes) are unchanged.

Clauses (all must hold; the counter imports the round-42 counter c1-r42-geometry.py from its own
directory and reuses its bubblewrap sandbox, RLIMIT_NPROC = 1 fixture runs, nonce, generator and
byte-exact judge, with its model extended by exactly the paragraph above):
  a   the tool exists at REV;
  f   fixtures: sgen0..sgen11 (the round-42 nonce lattice with a `fullscreen` value drawn per
      client from absent, 0, 1, 2, true, 3, "2", 2.0, -1, null and sometimes a `fullscreenClient`
      value) and the fixed fixtures of FIXED below; each compares rc and stdout byte-exactly with
      the extended model; on rc 0/1/3/4 stderr must be empty (TOTAL = 26);
  b   `--selftest` in the sandbox exits 0 printing `MADO_GEOMETRY_SELFTEST: k/n passed`, k == n,
      n >= 80;
  b4  state teeth: the comparison sites of every function (selftest, main, usage and functions
      nested in selftest excluded) whose body holds a string constant containing `fullscreen`
      (any case) number >= 6; each is flipped in a copy at the real layout and the copy's
      selftest must fail for >= 75 % of them (rounded up);
  g   the round-42 clause g holds (standard-library imports json os re stat sys only, no denied
      call, name, string or keyword unpacking);
  r   no harm to the round-43 contract: `c1-r42-geometry.py --repo REPO --rev REV --tool <the
      same bytes> --nonce <derived>` exits 0 and prints `verdict=TARGET_MET`.

Final line: `PRED-C1-r44: fixtures=k/26 clauses=<...> tool=present|absent verdict=TARGET_MET|TARGET_MISSED
rev=<full hash> nonce=<nonce>`. TARGET_MET (exit 0) iff every clause holds and k == 26; else exit 1;
setup failure exit 2. Scratch: `--work DIR`, else $C1R44_TMP, else $TMPDIR (never a hardcoded /tmp).

Residuals (declared): a tool that holds a model of the contract is an implementation; b4 counts
sites only in functions that name `fullscreen`, so a tool can move its state logic into an
unnamed helper and keep the clause vacuous-but-satisfied only if it still has >= 6 sites there;
the sandbox is detectable (round-43 CritC1Cheat cheat 6); whether a live maximized or fullscreen
window reports the work-area or monitor box is the compositor's fact (pinned source, not scored).
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

PRED = "PRED-C1-r44"
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
    p = subprocess.run([os.path.realpath(sys.executable), "-I", OLD_PATH, "--repo", repo,
                        "--rev", rev, "--tool", tool, "--nonce", sub],
                       capture_output=True, env=env, timeout=1800)
    lines = p.stdout.decode("utf-8", "replace").strip().splitlines()
    last = lines[-1] if lines else ""
    ok = p.returncode == 0 and " verdict=TARGET_MET " in last
    print("%s clause=r rc=%d %s" % (PRED, p.returncode, last))
    return ok


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
    src = open(args.tool, "rb").read() if args.tool else old.git(repo, "show", "%s:%s" % (rev, TOOL))
    present = src is not None
    cl = {"a": int(present), "b": 0, "b4": 0, "g": 0, "r": 0}
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
