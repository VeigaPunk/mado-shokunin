#!/usr/bin/env python3
"""MutC1Counter builder: scratch mimic trees for counter mutants + probe tool sources.

Never touches the tracked counter; every mutant is a copy under ctr/<name>/ laid out like the
lane so the counter's HERE-relative FIXTURES_PATH / PIN_PATH resolve inside the mimic.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = LANE + "/quality/counters/c1-r47-terminal.py"
FIXTURES = LANE + "/quality/counters/c1-r47-fixtures.json"
PIN = LANE + "/.ufo/waves/round-47/fetch/xdg-terminal-exec"
ROOT = "/fast/scratch/hyaku/mado-r47/MutC1Counter"

spec = importlib.util.spec_from_file_location("ctl", LANE + "/.ufo/waves/round-47/ctl/run-c1-controls.py")
ctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctl)
REF = ctl.REF


def replace1(src, old, new, tag):
    assert src.count(old) == 1, "patch point not unique: %s (%d)" % (tag, src.count(old))
    return src.replace(old, new, 1)


MUTS = {}

# m1: drop the drift check (the raise only; collection stays as dead code)
DRIFT_RAISE = '        if drift:\n            raise Setup("oracle drifted from %d recorded fixture(s): %s" % (len(drift), ",".join(drift[:5])))\n'


def _m1(s):
    return replace1(s, DRIFT_RAISE, "", "m1")
MUTS["m1"] = _m1



# m2: compare stdout only (drop rc from the fixture/generated comparison)
MUTS["m2"] = lambda s: replace1(s, "    ok = o_norm == t_norm\n", "    ok = o_norm[1] == t_norm[1]\n", "m2")

# m3: explain ignores the tool's exit status in the primary comparison
PRIMARY_RC_OLD = (
    '            want = (parts[0], parts[1] if len(parts) > 1 else "", "OK", 0)\n'
    '        else:\n'
    '            want = ("-", "-", "NO_TERMINAL", 3)\n'
    '        got = (f.get("selected"), f.get("path"), f.get("verdict"), t_rc)\n')
PRIMARY_RC_NEW = (
    '            want = (parts[0], parts[1] if len(parts) > 1 else "", "OK")\n'
    '        else:\n'
    '            want = ("-", "-", "NO_TERMINAL")\n'
    '        got = (f.get("selected"), f.get("path"), f.get("verdict"))\n')
OBS_RC_OLD = '            if (v, rc) != (want_v, want_rc):\n'
OBS_RC_NEW = '            if v != want_v:\n'


def _m3(s):
    return replace1(s, PRIMARY_RC_OLD, PRIMARY_RC_NEW, "m3")


MUTS["m3"] = _m3
MUTS["m3b"] = lambda s: replace1(_m3(s), OBS_RC_OLD, OBS_RC_NEW, "m3b")



# m4: skip variant B entirely
MUTS["m4"] = lambda s: replace1(
    s,
    '            ok_a, o_a, why_a = run_case(box, fx, "A", rng)\n'
    '            ok_b, _o_b, why_b = run_case(box, fx, "B", rng)\n',
    '            ok_a, o_a, why_a = run_case(box, fx, "A", rng)\n'
    '            why_b = ""\n',
    "m4a") .replace("            ok = ok_a and ok_b\n", "            ok = ok_a\n", 1)

# m5: reuse the oracle tree for the tool (run_case only; explain_case untouched)
MUTS["m5"] = lambda s: replace1(
    s,
    '    ro, rt = os.path.join(base, "o", "r"), os.path.join(base, "t", "r")\n'
    '    for r in (ro, rt):\n'
    '        materialize(r, case)\n'
    '    args_o = [a.replace("$ROOT", ro) for a in case["args"]]\n',
    '    ro = os.path.join(base, "o", "r")\n'
    '    materialize(ro, case)\n'
    '    rt = ro\n'
    '    args_o = [a.replace("$ROOT", ro) for a in case["args"]]\n',
    "m5")

# m6: drop the explain DIFFER probe
MUTS["m6"] = lambda s: replace1(
    s,
    '        for path, want_v, want_rc in ((good, "AGREE", 0), (bad, "DIFFER", 1)):\n',
    '        for path, want_v, want_rc in ((good, "AGREE", 0),):\n',
    "m6")

# m7a: accept one trip
MUTS["m7a"] = lambda s: replace1(
    s,
    '        readonly = "fail" if box.trips else "ok"\n',
    '        readonly = "fail" if len(box.trips) > 1 else "ok"\n',
    "m7a")

# m7b: accept all trips (readonly clause dropped)
MUTS["m7b"] = lambda s: replace1(
    s,
    '        readonly = "fail" if box.trips else "ok"\n',
    '        readonly = "ok"\n',
    "m7b")

# m8: lower SELFTEST_MIN to 1
MUTS["m8"] = lambda s: replace1(s, "SELFTEST_MIN = 30\n", "SELFTEST_MIN = 1\n", "m8")

# m9: parse the selftest line loosely (drop exact 3 tokens, N==M, and the "/M" half)
MUTS["m9"] = lambda s: replace1(
    s,
    '    last = out.strip().split("\\n")[-1] if out.strip() else ""\n'
    '    parts = last.split()\n'
    '    ok = False\n'
    '    if rc == 0 and len(parts) == 3 and parts[0] == "MADO_TERMINAL_SELFTEST:" and parts[2] == "passed":\n'
    '        n = parts[1].split("/")\n'
    '        ok = (len(n) == 2 and n[0] == n[1] and n[0].isascii() and n[0].isdigit() and int(n[0]) >= SELFTEST_MIN)\n',
    '    last = out.strip().split("\\n")[-1] if out.strip() else ""\n'
    '    ok = False\n'
    '    if rc == 0 and last.startswith("MADO_TERMINAL_SELFTEST:") and " passed" in last:\n'
    '        head = last[len("MADO_TERMINAL_SELFTEST:"):].split(" passed")[0].strip()\n'
    '        n = head.split("/")[0] if "/" in head else head\n'
    '        ok = (n.isascii() and n.isdigit() and int(n) >= SELFTEST_MIN)\n',
    "m9")


def mimic(name, counter_src, fixtures_bytes):
    d = os.path.join(ROOT, "ctr", name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "quality", "counters"))
    os.makedirs(os.path.join(d, ".ufo", "waves", "round-47", "fetch"))
    with open(os.path.join(d, "quality", "counters", "c1-r47-terminal.py"), "w") as fh:
        fh.write(counter_src)
    with open(os.path.join(d, "quality", "counters", "c1-r47-fixtures.json"), "wb") as fh:
        fh.write(fixtures_bytes)
    shutil.copy(PIN, os.path.join(d, ".ufo", "waves", "round-47", "fetch", "xdg-terminal-exec"))
    return d


def main():
    base = open(COUNTER).read()
    fx = open(FIXTURES, "rb").read()
    # drift-probe fixtures: one recorded expect no longer describes the oracle
    fxj = json.loads(fx.decode())
    fxj[0]["expect"]["stdout"] = fxj[0]["expect"]["stdout"] + "X"
    fx_mod = json.dumps(fxj).encode()
    sha_mod = hashlib.sha256(fx_mod).hexdigest()
    # harness variants for the drift probe: FIXTURES_SHA256 -> sha of the modified record
    m1base = replace1(base, 'FIXTURES_SHA256 = "%s"\n' % hashlib.sha256(fx).hexdigest(),
                      'FIXTURES_SHA256 = "%s"\n' % sha_mod, "m1base")
    MUTS["m1base"] = lambda s, _b=m1base: _b
    paths = {}
    for name, fn in sorted(MUTS.items()):
        src = fn(m1base) if name == "m1" else fn(base)
        fxb = fx_mod if name in ("m1", "m1base") else fx
        paths[name] = mimic(name, src, fxb)
        got = open(os.path.join(paths[name], "quality", "counters", "c1-r47-terminal.py")).read()
        assert got == src
        print("built %-7s -> %s" % (name, paths[name]))
    # probe tools (REF-derived), written for the record under tools/
    os.makedirs(os.path.join(ROOT, "tools"), exist_ok=True)
    probes = {
        "P-M2": replace1(REF, "        sys.stdout.flush()\n        return rc\n",
                         "        sys.stdout.flush()\n        return 7\n", "P-M2"),
        "P-M3": replace1(REF,
                         '    print("MADO_TERM: selected=%s path=%s cmd=%s cache=%s verdict=%s" % (sel, path, argv0, cache, verdict))\n    return rc\n',
                         '    print("MADO_TERM: selected=%s path=%s cmd=%s cache=%s verdict=%s" % (sel, path, argv0, cache, verdict))\n    return 1\n',
                         "P-M3"),
        "P-M3p": replace1(REF,
                          '    print("MADO_TERM: selected=%s path=%s cmd=%s cache=%s verdict=%s" % (sel, path, argv0, cache, verdict))\n    return rc\n',
                          '    print("MADO_TERM: selected=%s path=%s cmd=%s cache=%s verdict=%s" % (sel, path, argv0, cache, verdict))\n    return (1 if observed is None else rc)\n',
                          "P-M3p"),
        "P-M4": replace1(REF, 'USEP = "\\x1f"\n',
                         'USEP = "\\x1f"\nif os.environ.get("LANG", "") == "en_US.UTF-8":\n    sys.exit(7)\n', "P-M4"),
        "P-M7a": replace1(REF, '    if len(argv) >= 1 and argv[0] == "--selftest":\n        return selftest()\n',
                          '    if len(argv) >= 1 and argv[0] == "--selftest":\n        import socket\n        socket.socket(socket.AF_UNIX)\n        return selftest()\n',
                          "P-M7a"),
        "P-M8": replace1(REF, '    print("MADO_TERMINAL_SELFTEST: %d/%d passed" % (passed, len(cases)))\n',
                         '    print("MADO_TERMINAL_SELFTEST: 2/2 passed")\n', "P-M8"),
        "P-M9": replace1(REF, '    print("MADO_TERMINAL_SELFTEST: %d/%d passed" % (passed, len(cases)))\n',
                         '    print("MADO_TERMINAL_SELFTEST: 35/43 passed")\n', "P-M9"),
    }
    for name, src in sorted(probes.items()):
        with open(os.path.join(ROOT, "tools", name + ".py"), "w") as fh:
            fh.write(src)
        print("built probe %-6s (%d bytes)" % (name, len(src)))
    print("modified-record sha256:", sha_mod)
    print("base fixtures sha256:", hashlib.sha256(fx).hexdigest())


if __name__ == "__main__":
    sys.exit(main())
