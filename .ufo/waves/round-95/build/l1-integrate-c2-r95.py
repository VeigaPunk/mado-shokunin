#!/usr/bin/env python3
"""round-95 L1 integration for C2 (pre-freeze, DRAFT runs only).

  l1-integrate-c2-r95.py --scratch DIR [--extra-kills JSON]
Frozen kill-set candidates = R95MExecKillsC2's first drafts + R95MMutC2's closing kills (+ L1 closing kills from
--extra-kills: {"tools/...": [kill, ...]}), written to build/mado-<tool>-kills.c2b.json.  Frozen panel = R95MExecCounterC2's
24 hand weakenings and 6 neutral edits + R95MMutC2's green escapes of the first drafts + R95MCritic's 9 drop-component
pairs, each checked green (selftest checks=N failed=0) here; written to controls/selftest-panel-r95-frozen.json.
Prints, per tool: gate on the pristine tool, panel entries the c2b sets do not flag (WEAK), labels without a singleton.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(R)))
GATE = os.path.join(LANE, "quality", "check-selftest-strength.py")
TOOLS = {"tools/mado-mimeglob.py": ("mimeglob", "MADO_MIMEGLOB_SELFTEST: ", 19),
         "tools/mado-portals.py": ("portals", "MADO_PORTALS_SELFTEST: ", 28)}


def selftest_line(path, scratch):
    r = subprocess.run([sys.executable, "-I", path, "--selftest"], capture_output=True, text=True, cwd=scratch,
                       env=dict(os.environ, TMPDIR=scratch), timeout=120)
    return r.returncode, [l for l in r.stdout.splitlines() if "_SELFTEST: " in l][-1:]


def gate(tool_path, kills_path, scratch, drift=True):
    argv = [sys.executable, "-I", GATE, "--tool", tool_path, "--kills", kills_path, "--scratch-root", scratch]
    if drift:
        argv.append("--allow-sha-drift")
    r = subprocess.run(argv, capture_output=True, text=True, timeout=1800)
    last = [l for l in r.stdout.splitlines() if l.startswith("SELFTEST_STRENGTH:")]
    return r.returncode, (last[-1] if last else r.stdout[-200:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--extra-kills")
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    w = os.path.join(R, "w1")
    extra = json.load(open(a.extra_kills)) if a.extra_kills else {}
    panel0 = json.load(open(os.path.join(R, "controls", "selftest-panel-r95.json")))
    crit = open(os.path.join(w, "R95MCritic.md")).read()
    s = crit.index("Attack-seat pairs")
    s = crit.index("```json", s) + len("```json\n")
    crit_pairs = json.loads(crit[s:crit.index("```", s)])
    hand, neutral = list(panel0["hand"]), list(panel0["neutral"])
    origin = {x["id"]: "R95MExecCounterC2" for x in hand + neutral}
    for tool, (short, prefix, n) in TOOLS.items():
        esc = json.load(open(os.path.join(w, f"R95MMutC2-escapes-{short}.json")))
        for r in esc["rows"]:
            hand.append({"tool": tool, "id": "mutc2-" + r["id"], "what": f"R95MMutC2 escape ({r['case']}) of {r['label']}",
                         "find": r["find"], "replace": r["replace"]})
            origin["mutc2-" + r["id"]] = "R95MMutC2"
    for p in crit_pairs:
        hand.append({"tool": p["tool"], "id": p["id"], "what": "R95MCritic drop-component pair", "find": p["find"],
                     "replace": p["replace"]})
        origin[p["id"]] = "R95MCritic"
    # dedupe identical (tool, find, replace)
    seen, h2 = set(), []
    for x in hand:
        key = (x["tool"], x["find"], x["replace"])
        if key in seen:
            continue
        seen.add(key)
        h2.append(x)
    hand = h2
    out = {}
    for tool, (short, prefix, n) in TOOLS.items():
        src = open(os.path.join(LANE, tool)).read()
        k0 = json.load(open(os.path.join(R, "build", f"mado-{short}-kills.c2.json")))
        cl = json.load(open(os.path.join(w, f"R95MMutC2-closing-{short}.json")))["kills"]
        kills = list(k0["kills"])
        ids = {k["id"] for k in kills}
        for k in cl + extra.get(tool, []):
            if k["id"] not in ids:
                kills.append({x: k[x] for x in ("id", "find", "replace", "must_fail")})
                ids.add(k["id"])
        ks = dict(k0, kills=kills, note=k0.get("note", "") + " | round 95 L1: + R95MMutC2 closing kills"
                  + (" + L1 closing kills" if extra.get(tool) else ""))
        kp = os.path.join(R, "build", f"mado-{short}-kills.c2b.json")
        json.dump(ks, open(kp, "w"), indent=1)
        out[tool] = kp
        pre = src[:src.find("def selftest(")]
        bad = [k["id"] for k in kills if pre.count(k["find"]) != 1]
        print(f"{short}: kills={len(kills)} anchor_bad={bad}")
        rc, line = gate(os.path.join(LANE, tool), kp, os.path.join(a.scratch, f"g-{short}"), drift=False)
        print(f"{short}: pristine gate rc={rc} {line}")
        labs = {}
        for k in kills:
            mf = k["must_fail"] if isinstance(k["must_fail"], list) else [k["must_fail"]]
            for l in mf:
                labs.setdefault(l, []).append(len(mf))
        single = sorted(l for l, v in labs.items() if 1 in v)
        nosingle = sorted(l for l, v in labs.items() if 1 not in v)
        print(f"{short}: labels_covered={len(labs)}/{n} singletons={len(single)} no_singleton={nosingle}")
        # panel entries for this tool: green check, then the gate with the c2b set
        mine = [x for x in hand if x["tool"] == tool]

        def check(x):
            if src.count(x["find"]) != 1:
                return x["id"], "find-count", src.count(x["find"]), ""
            d = os.path.join(a.scratch, "p", x["id"])
            os.makedirs(d, exist_ok=True)
            tp = os.path.join(d, os.path.basename(tool))
            open(tp, "w").write(src.replace(x["find"], x["replace"], 1))
            rc0, line0 = selftest_line(tp, d)
            if rc0 != 0 or not line0 or line0[0] != f"{prefix}checks={n} failed=0":
                return x["id"], "not-green", rc0, line0
            rc, line = gate(tp, kp, os.path.join(d, "g"))
            return x["id"], "WEAK" if rc == 1 else f"rc{rc}", rc, line

        with ThreadPoolExecutor(12) as ex:
            res = list(ex.map(check, mine))
        for i, st, rc, line in res:
            if st != "WEAK":
                print(f"  panel {i} [{origin.get(i)}] {st} {line}")
        print(f"{short}: panel hand={len(mine)} weak={sum(1 for r in res if r[1] == 'WEAK')}")
        for x in mine:
            x["_status"] = dict((r[0], r[1]) for r in res)[x["id"]]
    green = [x for x in hand if x.get("_status") in ("WEAK", "rc0")]
    dropped = [x for x in hand if x.get("_status") not in ("WEAK", "rc0")]
    for x in hand:
        x["origin"] = origin.get(x["id"], "?")
    frozen = {"pred": "PRED-C2-r95-v1",
              "note": "round 95 frozen panel (L1): R95MExecCounterC2 24 tautologies + 6 neutral edits, R95MMutC2's green "
                      "escapes of the first-draft kill-sets, R95MCritic's drop-component pairs; entries that are not "
                      "green on the unmutated tool are listed under not_green and not counted",
              "hand": [{k: v for k, v in x.items() if k != "_status"} for x in green],
              "neutral": neutral,
              "not_green": [{k: v for k, v in x.items() if k != "_status"} for x in dropped]}
    json.dump(frozen, open(os.path.join(R, "controls", "selftest-panel-r95-frozen.json"), "w"), indent=1)
    print(f"panel_frozen hand={len(green)} not_green={len(dropped)} neutral={len(neutral)}")


if __name__ == "__main__":
    main()
