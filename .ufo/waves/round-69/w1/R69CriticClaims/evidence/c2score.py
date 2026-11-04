#!/usr/bin/env python3
"""Independent scoring of the frozen control sets with the r68 classifier, the r69 prototype,
and a cross-set regression check (does the r69 rule still pass every r68 case?)."""
import importlib.util, json, os, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = os.path.dirname(os.path.abspath(__file__))
BASE = "04093b83f73a841117d3b31dbb2a6063f4f2a454"
FREEZE = "789a87f1a667b43dd759222a2f048bf8f75b43ce"


def load(name, rev, path):
    src = subprocess.check_output(["git", "-C", LANE, "cat-file", "-p", "%s:%s" % (rev, path)])
    p = os.path.join(S, name + ".py")
    open(p, "wb").write(src)
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, src


def score(mod, cases):
    ok = 0
    rows = []
    for c in cases:
        r, g = mod.classify(c["src"])
        good = (r == c["expect_reader"]) and (g == c["expect_guard"])
        ok += int(good)
        rows.append((c["name"], r, g, c["expect_reader"], c["expect_guard"], good))
    return ok, rows


def show(tag, ok, rows, total):
    print("== %s %d/%d" % (tag, ok, total))
    for n, r, g, er, eg, good in rows:
        print("   %-20s got=(%s,%s) expect=(%s,%s) correct=%s"
              % (n, r, g, er, eg, good))


def main():
    r68, _ = load("r68c", BASE, "quality/counters/c2-r68-reader-guard.py")
    r69, _ = load("r69c", FREEZE, ".ufo/waves/round-69/proto/c2-classify.proto.py")
    sets = {}
    for tag, path in (("r69set", ".ufo/waves/round-69/controls/c2-controls-r69.json"),
                      ("r68set", ".ufo/waves/round-68/controls/c2-controls.json")):
        try:
            sets[tag] = json.load(open(os.path.join(LANE, path)))["cases"]
        except OSError as exc:
            print("MISSING %s: %s" % (tag, exc))
    for tag, cases in sets.items():
        for mtag, mod in (("r68", r68), ("r69", r69)):
            ok, rows = score(mod, cases)
            show("%s x %s" % (mtag, tag), ok, rows, len(cases))
    # cross-set: every r68 case must still be correct under the r69 rule
    if "r68set" in sets:
        ok, rows = score(r69, sets["r68set"])
        bad = [r for r in rows if not r[5]]
        print("CROSSSET r69on_r68 bad=%d %s" % (len(bad), [b[0] for b in bad]))


if __name__ == "__main__":
    main()
