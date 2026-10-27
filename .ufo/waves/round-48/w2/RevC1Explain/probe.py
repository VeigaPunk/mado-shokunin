#!/usr/bin/env python3
"""Instrument probe for round-48 C1 clause x (explain / --observed), run OUTSIDE scoring.

Imports the frozen counter (read-only) and drives its own prepare/oracle_side/run_case/explain_case on synthetic
schema-v2 cases that the frozen fixture set does not contain:
  P1  a hit cache whose command carries an EMPTY word
  P2  a hit cache whose first command word carries a NEWLINE
  P3  an --observed capture taken from a DIFFERENT tree root
  P4  an --observed capture of the same tree, written with root-relative paths
Nothing here scores a failure; every line is an observation for the seat report.
"""
import importlib.util
import json
import os
import random
import sys

sys.dont_write_bytecode = True
S = "/fast/scratch/hyaku/mado-r48/RevC1Explain"
CNT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/l1-draft/c1-r48-terminal-cache.py"
DRAFT = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/l1-draft/mado-terminal.py"
MUTS = sys.argv[2] if len(sys.argv) > 2 else "/fast/scratch/hyaku/mado-r48/RevC1Explain/mut"
WORK = os.path.join(S, "probe-work")
os.makedirs(WORK, exist_ok=True)

spec = importlib.util.spec_from_file_location("c1cnt", CNT)
cnt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cnt)

ENV = {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
       "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
       "XDG_CURRENT_DESKTOP": "Hyprland"}
ENTRY = ("[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\n"
         "TerminalArgExec=-e\nExec=foot --a\n")


def case(cid, cache_line11, args):
    return {"id": cid, "class": "PROBE", "env": dict(ENV),
            "files": {"home/.config/hyprland-xdg-terminals.list": "foot.desktop\n",
                      "usr/share/applications/foot.desktop": ENTRY},
            "exec": ["bin/foot"], "args": args, "mtime": 1600000000,
            "prime": {"args": ["--print-cmd"]},
            "after": {"cache_lines": {"11": cache_line11}},
            "expect": {"rc": 0, "stdout": ""}, "state": "hit"}


P1 = case("probe-empty-word", "foot\x1f\x1f--a\x1eEND_OF_EXEC_USEP", ["--print-cmd"])
P2 = case("probe-newline-word", "fo\not\x1f--a\x1eEND_OF_EXEC_USEP", ["--print-cmd"])


def tools():
    box = cnt.Box(WORK, DRAFT)
    out = [("draft", box)]
    for name in ("cmd-empty-word-dropped", "cmd-multiline-flattened", "observed-basename"):
        b = cnt.Box(WORK, os.path.join(MUTS, name + ".py"))
        out.append((name, b))
    return out


def main():
    rng = random.Random(4848)
    print("counter sha256 source:", CNT)
    print("draft   sha256 source:", DRAFT)
    for label, box in tools():
        for c in (P1, P2):
            try:
                ok, o_norm, why, state, _cold = cnt.run_case(box, c, "A", rng)
            except cnt.Setup as e:
                print("%-24s %-18s clause-w SETUP %s" % (label, c["id"], e))
                ok = why = None
                o_norm = None
            else:
                print("%-24s %-18s clause-w ok=%s state=%s oracle=(%r,%r) why=%r"
                      % (label, c["id"], ok, state, o_norm[0], o_norm[1][:80], why))
            try:
                xok, xwhy = cnt.explain_case(box, c, rng)
            except cnt.Setup as e:
                print("%-24s %-18s clause-x SETUP %s" % (label, c["id"], e))
            else:
                print("%-24s %-18s clause-x ok=%s why=%r" % (label, c["id"], xok, xwhy[:200]))

    # P3/P4: a capture from a foreign root, and a root-relative capture
    ref = tools()[0][1]
    c = P1
    base, lang = cnt.variant_roots(ref, "A", rng)
    near, far = os.path.join(base, "n", "r"), os.path.join(base, "f", "r")
    for r in (near, far):
        cnt.prepare(ref, r, c, lang)
    three = ["--print-id", "--print-path", "--print-cmd"]
    fenv = cnt.case_env(c, far, lang, "scored")
    _rcf, fout, _errf = ref.run(far, fenv, False, three)
    nenv = cnt.case_env(c, near, lang, "scored")
    _rcn, nout, _errn = ref.run(near, nenv, False, three)
    o_far = (_rcf, fout.replace(far, "$ROOT"))
    o_near = (_rcn, nout.replace(near, "$ROOT"))
    capdir = os.path.join(near, ".rw")
    caps = {"foreign-root": fout,
            "root-relative": "\n".join(l.replace(far + "/", "") for l in fout.split("\n"))}
    env = cnt.case_env(c, near, lang, "scored")
    for cname, text in caps.items():
        p = os.path.join(capdir, "cap-" + cname)
        with open(p, "wb") as fh:
            fh.write(text.encode("utf-8", "surrogateescape"))
        for label, box in tools():
            rc, out, _err = box.run(near, env, True, ["explain", "--observed", p],
                                    default_cache=c.get("default_cache", False))
            line = [l for l in out.split("\n") if l.startswith("MADO_TERM: ")]
            v = line[-1].rsplit("verdict=", 1)[-1].strip() if line else ""
            print("%-24s observed=%-14s verdict=%-7s rc=%d" % (label, cname, v, rc))
    print("near-root oracle capture:", repr(o_near[1][:120]))


if __name__ == "__main__":
    main()
