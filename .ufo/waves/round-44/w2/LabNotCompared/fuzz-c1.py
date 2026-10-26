#!/usr/bin/env python3
"""w2/LabNotCompared - differential fuzz of the landed tools/mado-geometry.py against
PRED-C1-r44-v2's model (quality/counters/c1-r44-geometry-states-v2.py:model_out_states).

Hypothesis: the landed tool's stdout and exit code equal the v2 counter's model on >= 20000
random (clients, rules) cases. The counter module is imported with importlib (main() never
runs); cases come from its gen_state_clients/old.gen_texts and from a state-heavy generator
of this seat. Each case is one `python3 -I tools/mado-geometry.py` run in the scratch dir.

usage: fuzz-c1.py --repo <lane> --work <scratch> [--n-base 15000] [--n-state 5000]
                   [--seed S] [--workers N] [--dump FILE]
"""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import random
import subprocess
import sys
import threading

GK = "org.omarchy.gkeep"
GKRX = "^(org.omarchy.gkeep)$"
GKCONF = ("windowrule = float on, match:class %s\nwindowrule = size 420 500, match:class %s\n"
          % (GKRX, GKRX))


def load_counter(repo):
    path = os.path.join(repo, "quality", "counters", "c1-r44-geometry-states-v2.py")
    spec = importlib.util.spec_from_file_location("c1r44_fuzz", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rng_of(seed, tag, i):
    h = hashlib.sha256(("%s:%s:%d" % (seed, tag, i)).encode()).hexdigest()
    return random.Random(int(h, 16))


# ------------------------------------------------------------------ generators
def case_base(mod, seed, i):
    """The counter's own lattice: old.gen_texts + gen_state_clients, stdin on odd i."""
    rng = mod.old.rng_for("LabNotCompared", seed, "sgen", i)
    texts, wants = mod.old.gen_texts(rng)
    clients = mod.gen_state_clients(rng, wants)
    return json.dumps(clients), texts, bool(i % 2)


STATE_POOL = [2, 2, 1, 1, 0, 3, -1, True, False, 2.0, 1.0, "2", None, [2], {"internal": 2}]
SZ_POOL = [[420, 500], [421, 500], [2560, 1440], [2544, 1380], [0, 0], [1, 1],
           [420.0, 500], [True, 500], [420], [], "420x500", None, [10 ** 18, 500],
           [10 ** 40, 10 ** 40], [2 ** 63, 2 ** 63], [-1, 500]]


def gk_client(rng, state, **kw):
    c = {"address": "0x%x" % rng.randrange(1 << 32), "class": GK,
         "size": rng.choice(SZ_POOL), "floating": rng.choice([True, True, False])}
    if state != "absent":
        c["fullscreen"] = state
    c.update(kw)
    return c


def case_state(mod, seed, i):
    """State-heavy dumps: all-state, state+tiled, state+agree, dup keys, huge ints, bad types."""
    rng = rng_of(seed, "state", i)
    variant = i % 10
    texts = [GKCONF]
    if variant == 0:  # all-state dump: every matched client carries a state
        cl = [gk_client(rng, rng.choice([2, 1])) for _ in range(rng.randrange(1, 6))]
        for c in cl:
            c["size"] = rng.choice([[2560, 1440], [2544, 1380], [420, 500]])
    elif variant == 1:  # state + tiled
        cl = [gk_client(rng, rng.choice([2, 1])) for _ in range(rng.randrange(1, 5))]
        cl += [gk_client(rng, "absent", floating=False),
               gk_client(rng, rng.choice([0, None, 3]), floating=False)]
    elif variant == 2:  # state + agree (OK must win over NOT_COMPARED)
        cl = [gk_client(rng, rng.choice([2, 1])) for _ in range(rng.randrange(0, 3))]
        cl.append({"address": "0xa", "class": GK, "size": [420, 500], "floating": True})
    elif variant == 3:  # state + badsize (BADSIZE is tested before the state)
        cl = [gk_client(rng, rng.choice([2, 1]),
                        size=rng.choice([[420.0, 500], [True, 500], [420], None]))
              for _ in range(rng.randrange(1, 4))]
        cl.append(gk_client(rng, "absent"))
    elif variant == 4:  # duplicate keys, raw text (last key wins in json.loads on both sides)
        dup = rng.choice(['"fullscreen": 2, "fullscreen": 0', '"fullscreen": 0, "fullscreen": 2',
                          '"fullscreen": true, "fullscreen": 1', '"size": [9, 9], "size": [420, 500]',
                          '"size": [420, 500], "size": [9, 9]', '"class": "zz", "class": "%s"' % GK,
                          '"fullscreen": 1, "fullscreen": null', '"fullscreen": 2, "size": [421, 500]'])
        raw = '[{"class": "%s", "size": [420, 500], "floating": true, %s}]' % (GK, dup)
        return raw, texts, bool(rng.randrange(2))
    elif variant == 5:  # huge ints
        cl = [{"address": "0x1", "class": GK, "size": [rng.choice([10 ** 18, 2 ** 63, 10 ** 40]),
                                                       rng.choice([500, 10 ** 25])],
               "floating": True, "fullscreen": rng.choice([10 ** 30, -10 ** 30, 2 ** 64 + 2, 2, 1])}
              for _ in range(rng.randrange(1, 4))]
    elif variant == 6:  # every state value type
        cl = [gk_client(rng, s) for s in rng.sample(STATE_POOL, k=rng.randrange(1, 6))]
        cl += [gk_client(rng, s, fullscreenClient=rng.choice([0, 1, 2]))
               for s in rng.sample(STATE_POOL, 2)]
    elif variant == 7:  # unmapped / missing class / control-char class states
        cl = [gk_client(rng, 2, mapped=False), gk_client(rng, 1, mapped=False),
              {"size": [420, 500], "floating": True, "fullscreen": 2},
              {"class": "a\x01b", "size": [420, 500], "floating": True, "fullscreen": 2},
              {"class": 7, "size": [420, 500], "floating": True, "fullscreen": 1}]
    elif variant == 8:  # float rules only: NO_SIZE_RULES must beat the states
        texts = ["windowrule = float on, match:class %s\n" % GKRX,
                 "windowrule = center on, match:class %s\n" % GKRX]
        cl = [gk_client(rng, rng.choice([2, 1])), gk_client(rng, "absent")]
    else:  # multi-file rules, last-wins, want 0 0
        w, h = rng.choice([(420, 500), (0, 0), (2560, 1440)])
        texts = ["windowrule = size 1 1, match:class %s\nwindowrule = float off, match:class %s\n"
                 % (GKRX, GKRX),
                 "windowrule = size %d %d, match:class %s\nwindowrule = float on, match:class %s\n"
                 % (w, h, GKRX, GKRX)]
        cl = [gk_client(rng, rng.choice([2, 1, "absent"]),
                        size=rng.choice([[w, h], [w + 1, h], [0, 0]]))
              for _ in range(rng.randrange(1, 4))]
    if rng.randrange(3) == 0:
        cl.insert(rng.randrange(len(cl) + 1), {"class": "kitty", "size": [9, 9],
                                               "floating": True, "fullscreen": 2})
    return json.dumps(cl), texts, bool(rng.randrange(2))


FIXED_CASES = [
    ("fs0", [{"class": GK, "size": [2560, 1440], "floating": True, "fullscreen": 2}]),
    ("max0", [{"class": GK, "size": [2544, 1380], "floating": False, "fullscreen": 1}]),
    ("zero0", [{"class": GK, "size": [0, 0], "floating": True, "fullscreen": 2}]),
    ("dupfs-last0", '[{"class": "%s", "size": [420, 500], "floating": true, "fullscreen": 2, "fullscreen": 0}]' % GK),
    ("empty", []),
    ("unmapped-all", [{"class": GK, "size": [2560, 1440], "floating": True,
                       "fullscreen": 2, "mapped": False}]),
    ("huge-mode", [{"class": GK, "size": [420, 500], "floating": True, "fullscreen": 10 ** 60}]),
    ("inf-size", '[{"class": "%s", "size": [Infinity, 500], "floating": true, "fullscreen": 2}]' % GK),
    ("nan-size", '[{"class": "%s", "size": [NaN, 500], "floating": true, "fullscreen": 1}]' % GK),
    ("badjson-truncated", "["),
    ("badjson-object", "{}"),
    ("badjson-intlist", "[1]"),
    ("badjson-null", "null"),
    ("badjson-string", '"[]"'),
    ("badjson-empty", ""),
    ("badjson-bytes", "\udcff[]"),
]

# targeted analytic cases: (name, raw-or-clients, rules texts or None for GKCONF)
TARGETED = [
    ("t-state-and-agree", [{"class": GK, "size": [2560, 1440], "floating": True, "fullscreen": 2},
                           {"class": GK, "size": [420, 500], "floating": True}], None),
    ("t-max-and-fs-no-agree", [{"class": GK, "size": [2544, 1380], "floating": False,
                                "fullscreen": 1},
                               {"class": GK, "size": [2560, 1440], "floating": True,
                                "fullscreen": 2}], None),
    ("t-state-and-differ", [{"class": GK, "size": [2560, 1440], "floating": True, "fullscreen": 2},
                            {"class": GK, "size": [421, 500], "floating": True}], None),
    ("t-badsize-only-state", [{"class": GK, "size": [420.0, 500], "floating": True,
                               "fullscreen": 2}], None),
    ("t-unmapped-state-only", [{"class": GK, "size": [2560, 1440], "floating": True,
                                "fullscreen": 2, "mapped": False}], None),
    ("t-unmatched-state-only", [{"class": "kitty", "size": [2560, 1440], "floating": True,
                                 "fullscreen": 2}], None),
    ("t-float-only-rules", [{"class": GK, "size": [2560, 1440], "floating": True,
                             "fullscreen": 2}],
     ["windowrule = float on, match:class %s\n" % GKRX]),
    ("t-want-zero-zero", [{"class": GK, "size": [0, 0], "floating": True, "fullscreen": 2}],
     ["windowrule = size 00 00, match:class %s\n" % GKRX]),
    ("t-five-digit", [{"class": GK, "size": [99999, 99999], "floating": True, "fullscreen": 1}],
     ["windowrule = size 99999 99999, match:class %s\n" % GKRX]),
    ("t-six-digit", [{"class": GK, "size": [100000, 1], "floating": True, "fullscreen": 2}],
     ["windowrule = size 100000 1, match:class %s\n" % GKRX]),
    ("t-negzero-mode", '[{"class": "%s", "size": [420, 500], "floating": true, "fullscreen": -0}]' % GK,
     None),
    ("t-one-e-mode", '[{"class": "%s", "size": [420, 500], "floating": true, "fullscreen": 1e0}]' % GK,
     None),
    ("t-tiled-and-state", [{"class": GK, "size": [1, 1], "floating": False, "fullscreen": 1},
                           {"class": GK, "size": [2560, 1440], "floating": True,
                            "fullscreen": 2}], None),
    ("t-big-dump", [{"class": GK, "size": [420 + (k % 2), 500], "floating": True,
                     "fullscreen": (2 if k % 3 == 0 else (1 if k % 3 == 1 else 0))}
                    for k in range(300)], None),
    ("t-dup-class", '[{"class": "kitty", "class": "%s", "size": [420, 500], "floating": true, '
                    '"fullscreen": 2}]' % GK, None),
]


def build_cases(mod, seed, n_base, n_state):
    cases = []
    for i in range(n_base):
        raw, texts, via = case_base(mod, seed, i)
        cases.append(("sgen%d" % i, raw, texts, via))
    for i in range(n_state):
        raw, texts, via = case_state(mod, seed, i)
        cases.append(("state%d" % i, raw, texts, via))
    for entry in FIXED_CASES + TARGETED:
        name, raw = entry[0], entry[1]
        texts = entry[2] if len(entry) == 3 else None
        if not isinstance(raw, str):
            raw = json.dumps(raw)
        cases.append(("fixed-" + name, raw, texts or [GKCONF], False))
    return cases


# ------------------------------------------------------------------ comparison
def model_of(mod, raw, texts):
    want = mod.model_out_states(raw.encode("utf-8", "surrogateescape"), texts)
    if want[0] is None:
        return "MADO_GEOMETRY: SETUP %s\n" % want[1], 2
    return want


def run_tool(py, tool, cwd, clients_path, rpaths, raw, via_stdin):
    argv = [py, "-I", tool]
    argv += ["--clients", "-"] if via_stdin else ["--clients", clients_path]
    for p in rpaths:
        argv += ["--rules", p]
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=60, env=env,
                           input=raw if via_stdin else None,
                           stdin=None if via_stdin else subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return None, b"", b"timeout"
    return p.returncode, p.stdout, p.stderr


def first_diff(got, want):
    a, b = got.splitlines(), want.splitlines()
    for k in range(max(len(a), len(b))):
        x = a[k] if k < len(a) else None
        y = b[k] if k < len(b) else None
        if x != y:
            return "line %d got=%r want=%r" % (k + 1, x, y)
    return "same lines"


def cmp_case(mod, py, tool, cwd, name, raw, texts, via_stdin):
    want_out, want_rc = model_of(mod, raw, texts)
    payload = raw.encode("utf-8", "surrogateescape")
    cpath = os.path.join(cwd, "c.json")
    with open(cpath, "wb") as fh:
        fh.write(payload)
    rpaths = []
    for k, t in enumerate(texts):
        p = os.path.join(cwd, "r%d.conf" % k)
        with open(p, "wb") as fh:
            fh.write(t.encode("utf-8", "surrogateescape"))
        rpaths.append(p)
    rc, out, err = run_tool(py, tool, cwd, cpath, rpaths, payload, via_stdin)
    got = out.decode("utf-8", "replace")
    ok = rc == want_rc and got == want_out and not (want_rc in (0, 1, 3, 4, 5) and err)
    rec = {"name": name, "raw": raw, "texts": texts, "via_stdin": via_stdin,
           "got_rc": rc, "want_rc": want_rc, "got": got, "want": want_out,
           "stderr": err.decode("utf-8", "replace"), "ok": ok}
    if not ok:
        if rc != want_rc:
            rec["why"] = "rc %r != %r" % (rc, want_rc)
        elif got != want_out:
            rec["why"] = first_diff(got, want_out)
        else:
            rec["why"] = "stderr=%r" % rec["stderr"][:120]
    return rec


def classify(rec):
    verdicts = ("NO_SIZE_RULES", "DIFFER", "NO_MATCHING_CLIENT", "NOT_COMPARED", "OK")
    v = "SETUP"
    for cand in verdicts:
        if rec["want"].rstrip().endswith("verdict=" + cand):
            v = cand
            break
    st = " maximized=" in rec["want"] or " fullscreen=" in rec["want"]
    return rec["want_rc"], v, st


_LOCAL = threading.local()


def slot(work):
    """One case directory per thread: no two concurrent cases share clients/rules files."""
    d = getattr(_LOCAL, "dir", None)
    if d is None:
        d = os.path.join(work, "slot-%d" % threading.get_ident())
        os.makedirs(d, exist_ok=True)
        _LOCAL.dir = d
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--n-base", type=int, default=15000)
    ap.add_argument("--n-state", type=int, default=5000)
    ap.add_argument("--seed", default="LabNotCompared-r44-w2")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--dump", default=None, help="write the JSON summary here")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    mod = load_counter(repo)
    tool = os.path.join(repo, "tools", "mado-geometry.py")
    py = os.path.realpath(sys.executable)

    cases = build_cases(mod, args.seed, args.n_base, args.n_state)

    def run(case):
        d = slot(work)
        return cmp_case(mod, py, tool, d, case[0], case[1], case[2], case[3])

    bad = []
    cover = {}
    n = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = [pool.submit(run, c) for c in cases]
        for fut in futs:
            rec = fut.result()
            n += 1
            key = classify(rec)
            cover[key] = cover.get(key, 0) + 1
            if not rec["ok"]:
                bad.append(rec)
                print("DIVERGE %s %s" % (rec["name"], rec.get("why")))
            if n % 2000 == 0:
                print("progress %d/%d divergences=%d" % (n, len(cases), len(bad)))

    print("CASES %d DIVERGENCES %d seed=%s" % (n, len(bad), args.seed))
    for (rc, v, st), k in sorted(cover.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
        print("COVER rc=%s verdict=%s state_segment=%s n=%d" % (rc, v, st, k))
    if args.dump:
        with open(args.dump, "w") as fh:
            json.dump({"cases": n, "seed": args.seed, "divergences": bad,
                       "coverage": [[list(k), v] for k, v in cover.items()]}, fh, indent=1)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
