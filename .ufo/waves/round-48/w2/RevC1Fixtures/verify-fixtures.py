#!/usr/bin/env python3
"""RevC1Fixtures (round 48 w2): re-measure every frozen C1 warm fixture against the pinned resolver.

For each of the 204 records in quality/counters/c1-r48-fixtures.json this derives, at count time and with the
counter's own preparation/oracle code (imported from the frozen counter, never modified):

  A  (rc, stdout, state) of the scored run in variant A   -> vs the record's `expect` and `state`
  C  (rc, stdout) of the cold twin (no cache)             -> vs the record's `cold`
  B  (rc, stdout) of the scored run in variant B          -> recorded expect must hold across root+lang
  P  the class premise, including the classes the frozen counter does not premise-check
     (WARM-INVALID => state in {stale,invalid,disabled} AND warm == cold; READDIR => the printed id is the last
     entry of the recorded readdir order; H1 => a directory shadows the entry; H2 => option-like Exec/TryExec;
     HOME-UNSET/EDGE => died before the cache gate iff `state` is '-'; CACHE-DEFAULT => no XDG_CACHE_HOME)

Writes one JSON line per fixture plus a summary to --out; prints only counts and failures.
"""
import importlib.util
import json
import os
import random
import shutil
import sys

sys.dont_write_bytecode = True

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r48-terminal-cache.py")
WARM = os.path.join(LANE, "quality", "counters", "c1-r48-fixtures.json")


def load_counter():
    spec = importlib.util.spec_from_file_location("c48frozen", COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def measure(c48, box, case, variant, rng):
    """One variant: scored run + cold twin (when the fixture has a cache to remove)."""
    base, lang = c48.variant_roots(box, variant, rng)
    try:
        ro = os.path.join(base, "o", "r")
        c48.prepare(box, ro, case, lang)
        warm, state = c48.oracle_side(box, case, ro, lang)
        cold = None
        if case.get("prime") or "cache" in case:
            rc_ = os.path.join(base, "c", "r")
            c48.prepare(box, rc_, case, lang, cold=True)
            cold, _st = c48.oracle_side(box, case, rc_, lang)
    finally:
        shutil.rmtree(base.split("/deep/")[0] if "/deep/" in base else base, ignore_errors=True)
    return warm, state, cold, lang


def pick(v):
    return [v[0], v[1]]


def premise(case, warm, state, cold, readdir_path=None):
    """Class premise beyond the counter's own check; '' when it holds, else why."""
    cls = case["class"]
    exp = pick((case["expect"]["rc"], case["expect"]["stdout"]))
    rec_cold = pick((case["cold"]["rc"], case["cold"]["stdout"])) if case.get("cold") else None
    if cls == "WARM-DIFFERS":
        if cold is None:
            return "WARM-DIFFERS without a cold twin"
        if pick(cold) == exp:
            return "WARM-DIFFERS: warm answer equals the cold one"
    elif cls == "WARM-SAME":
        if cold is None:
            return "WARM-SAME without a cold twin"
        if pick(cold) != exp:
            return "WARM-SAME: warm answer differs from the cold one"
    elif cls == "WARM-INVALID":
        if state not in ("stale", "invalid", "disabled"):
            return "WARM-INVALID: cache state %r is not a rejected cache" % state
        if cold is None:
            return "WARM-INVALID without a cold twin"
        if pick(cold) != pick(warm):
            return "WARM-INVALID: rejected cache but the answer differs from cold"
    elif cls == "WARM-ABSENT":
        if state != "absent":
            return "WARM-ABSENT: state %r" % state
    elif cls.startswith("MALFORMED"):
        if state == "hit" and "state" in case and case["state"] != "hit":
            return "MALFORMED: recorded state %r but derived hit" % case["state"]
    elif cls == "READDIR":
        # the winner must be the LAST FILE entry of its applications dir in the recorded readdir order: the answer
        # is readdir-order dependent, not name-order dependent (a directory entry cannot win: `find -type f`)
        order = ((case.get("meta") or {}).get("readdir_order") or {})
        if not readdir_path:
            return "READDIR: no --print-path witness"
        path = readdir_path.split("\n")[1] if "\n" in readdir_path else ""
        d = os.path.dirname(path).replace("$ROOT/", "", 1)
        nested = False
        if d not in order:
            # a nested entry: the deciding order is the nearest recorded ancestor's, and the path must descend
            # through that ancestor's last entry
            anc = [p for p in order if d.startswith(p.rstrip("/") + "/")]
            if not anc:
                return "READDIR: winner dir %r is not in the recorded readdir order" % d[:80]
            a = max(anc, key=len)
            step = d[len(a.rstrip("/")) + 1:].split("/")[0]
            if not order[a] or step != order[a][-1]:
                return "READDIR: nested winner %r is not under the last entry of %s" % (d[:60], a[-40:])
            readdir_path = readdir_path + "\tNESTED:" + a
            order = {a: order[a]}
            d = a
            nested = True
        if nested:
            return ""
        names = [n for n in order[d] if not any(k.startswith(d.rstrip("/") + "/" + n + "/") for k in case["files"])]
        if not names or os.path.basename(path) != names[-1]:
            return "READDIR: winner %r is not the last file entry of %s (%r)" % (
                os.path.basename(path)[:60], d[-40:], names)
    elif cls == "H1":
        # the class premise: some directory in the tree is named like a .desktop entry (a shadowing dir)
        dirs = [k for k in case["files"] if k.endswith("/")]
        dirs += [p for k in case["files"] for p in [k.rsplit("/", 1)[0]] if p.endswith(".desktop")]
        if not dirs:
            return "H1: no shadowing directory in the tree"
    elif cls == "H2":
        txt = "".join(v for v in case["files"].values() if isinstance(v, str))
        if not any(s in txt for s in ("Exec=-", "TryExec=-", "Exec=\n", "TryExec=\n")):
            return "H2: no option-like Exec/TryExec"
    elif cls in ("HOME-UNSET", "EDGE-HOMEUNSET"):
        if "HOME" not in (case.get("unset") or []):
            return "%s: HOME is not unset" % cls
        xdg = [k for k in ("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME") if k not in (case.get("unset") or [])]
        died = case["expect"]["rc"] == 1 and case["expect"]["stdout"] == ""
        if died and state != "-":
            return "%s: died (rc 1) but the cache gate was reached (%r)" % (cls, state)
        if state == "-" and not died:
            return "%s: never reached the cache gate but rc 0" % cls
        if not died and not xdg and not case.get("env", {}).get("XDG_DATA_DIRS"):
            return "%s: HOME unset with no XDG var to fall back on but rc 0" % cls
    elif cls == "CACHE-DEFAULT":
        if not case.get("default_cache"):
            return "CACHE-DEFAULT without default_cache"
        if "XDG_CACHE_HOME" in case.get("env", {}) or "XDG_CACHE_HOME" in (case.get("unset") or []):
            return "CACHE-DEFAULT with XDG_CACHE_HOME set"
    return ""


def main():
    work = sys.argv[1]
    out = sys.argv[2]
    only = sys.argv[3] if len(sys.argv) > 3 else None
    c48 = load_counter()
    fx = json.load(open(WARM))
    if only:
        fx = [f for f in fx if f["id"] in only.split(",")]
    os.makedirs(work, exist_ok=True)
    wd = os.path.join(work, "verify-%d" % os.getpid())
    os.makedirs(wd)
    box = c48.Box(wd)
    rng = random.Random(484848)
    rows, counts = [], {"n": 0, "expectA": 0, "expectB": 0, "state": 0, "cold": 0, "premise": 0, "counterpremise": 0}
    fails = []
    try:
        for i, case in enumerate(fx):
            warm_a, state_a, cold_a, _ = measure(c48, box, case, "A", rng)
            warm_b, state_b, _cold_b, lang_b = measure(c48, box, case, "B", rng)
            exp = pick((case["expect"]["rc"], case["expect"]["stdout"]))
            row = {"id": case["id"], "class": case["class"], "state_rec": case.get("state"), "state_a": state_a,
                   "state_b": state_b, "lang_b": lang_b}
            counts["n"] += 1
            ok = True
            if pick(warm_a) != exp:
                row["expectA"] = "oracle=%r rec=%r" % (pick(warm_a), exp)
                fails.append((case["id"], "expectA", row["expectA"]))
                ok = False
            else:
                counts["expectA"] += 1
            if pick(warm_b) != exp:
                row["expectB"] = "oracle=%r rec=%r" % (pick(warm_b), exp)
                fails.append((case["id"], "expectB", row["expectB"]))
                ok = False
            else:
                counts["expectB"] += 1
            if "state" in case and state_a != case["state"]:
                row["state"] = "derived=%r rec=%r" % (state_a, case["state"])
                fails.append((case["id"], "state", row["state"]))
                ok = False
            else:
                counts["state"] += 1
            if state_b != state_a:
                row["stateB"] = "variant B derived %r" % state_b
            if "cold" in case:
                rec_cold = pick((case["cold"]["rc"], case["cold"]["stdout"]))
                if cold_a is None:
                    row["cold"] = "recorded cold twin not measurable"
                    fails.append((case["id"], "cold", row["cold"]))
                    ok = False
                elif pick(cold_a) != rec_cold:
                    row["cold"] = "oracle=%r rec=%r" % (pick(cold_a), rec_cold)
                    fails.append((case["id"], "cold", row["cold"]))
                    ok = False
                else:
                    counts["cold"] += 1
            rpath = None
            if case["class"] == "READDIR":
                wcase = dict(case)
                wcase["args"] = ["--print-id", "--print-path"]
                rpath = measure(c48, box, wcase, "A", rng)[0][1]
            why = premise(case, warm_a, state_a, cold_a, rpath)
            if why:
                row["premise"] = why
                fails.append((case["id"], "premise", why))
                ok = False
            else:
                counts["premise"] += 1
            # the counter's own premise check must agree (Setup or not)
            try:
                c48.check_premise(case, state_a, cold_a)
                counts["counterpremise"] += 1
            except c48.Setup as e:
                row["counterpremise"] = str(e)
                fails.append((case["id"], "counterpremise", str(e)))
                ok = False
            row["ok"] = ok
            rows.append(row)
            print("%3d/%d %s %-26s %s%s" % (i + 1, len(fx), case["id"], case["class"],
                                            "pass" if ok else "FAIL", "" if ok else " " + json.dumps(
                                                {k: v for k, v in row.items() if k in
                                                 ("expectA", "expectB", "state", "stateB", "cold", "premise",
                                                  "counterpremise")})[:400]))
            sys.stdout.flush()
    finally:
        shutil.rmtree(wd, ignore_errors=True)
    with open(out + ".jsonl", "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print("SUMMARY %s" % json.dumps(counts, sort_keys=True))
    print("FAILS %d" % len(fails))
    for f in fails:
        print("FAIL %s %s %s" % f)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
