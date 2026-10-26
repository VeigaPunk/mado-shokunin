#!/usr/bin/env python3
"""MutC1Counter driver: single-edit mutants of the frozen C1 counter, run against the
reference control and the 16 registered bad controls (built with run-c1-controls.py logic).
Scratch-only; lane is read-only here. Modes: --mode check|run."""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
CTL = LANE + "/.ufo/waves/round-45/ctl/run-c1-controls.py"
FROZEN = LANE + "/quality/counters/c1-r45-monitors.py"
FROZEN_SHA = "c69ddee44a9fa3c442b910541038a9440ac72c2b5f21fe4899cb8f5df9213f34"
ROOT = "/fast/scratch/hyaku/mado-r45/MutC1Counter"

spec = importlib.util.spec_from_file_location("ctlc1", CTL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# ---- mutants: (name, old, new); each old must occur exactly once in the frozen text ----
HOST_OLD = (
    '    ("host", ["monitor = {A}, 3440x1440@100, 0x0, 1\\n"], [M("{A}")], False,\n'
    '     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "AGREE"),\n'
    '      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),'
)
HOST_DROP_R = (
    '    ("host", ["monitor = {A}, 3440x1440@100, 0x0, 1\\n"], [M("{A}")], False,\n'
    '     [O(A, 1, "-", "AGREE"),\n'
    '      S("OK", 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0)], 0),'
)
HOST_FLIP = (
    '    ("host", ["monitor = {A}, 3440x1440@100, 0x0, 1\\n"], [M("{A}")], False,\n'
    '     [R(1, A, "3440x1440@100.00", "0x0", "1.0000"), O(A, 1, "-", "DIFFER"),'
)
NORULES_OLD = (
    '    ("no-rules", ["general {\\n    gaps_in = 5\\n}\\n"], [M("{A}")], False,\n'
    '     [O(A, "-", "-", "UNRULED"), S("NO_RULES", 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0)], 4),'
)
NORULES_NEW = (
    '    ("no-rules", ["general {\\n    gaps_in = 5\\n}\\n"], [M("{A}")], False,\n'
    '     [S("NO_RULES", 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0)], 4),'
)

MUTANTS = [
    ("X0-identity", None, None),
    # selftest clause s
    ("S1-selftest-min-const", "SELFTEST_MIN = 30", "SELFTEST_MIN = 1"),
    ("S2-selftest-min-cmp", "int(n[0]) >= SELFTEST_MIN", "int(n[0]) >= 0"),
    ("S3-selftest-rc-drop", "if p.returncode == 0 and len(parts) == 3", "if len(parts) == 3"),
    ("S4-selftest-parts3-le", "== 3 and parts[0]", "<= 3 and parts[0]"),
    ("S5-selftest-suffix", 'parts[2] == "passed"', 'parts[2] != ""'),
    ("S6-selftest-prefix", 'parts[0] == "MADO_MONITORS_SELFTEST:"', 'parts[0] != ""'),
    ("S7-selftest-eq-or", "n[0] == n[1] and n[0].isdigit()", "n[0] == n[1] or n[0].isdigit()"),
    # fixture comparison
    ("R1-fixture-rc-drop", "ok = p.returncode == rc_want and got == want", "ok = got == want"),
    ("R2-fixture-stderr-drop", "and got == want and p.stderr == b\"\"", "and got == want"),
    ("R3-fixture-stdout-in",
     "ok = p.returncode == rc_want and got == want and p.stderr == b\"\"",
     "ok = p.returncode == rc_want and want in got and p.stderr == b\"\""),
    ("R4-timeout-swallow-true", '        return False, "timeout"', '        return True, "timeout"'),
    ("R5-fixture-timeout-1ms", "cwd=d, env=env, timeout=10)", "cwd=d, env=env, timeout=0.001)"),
    ("R6-selftest-timeout-1ms", '"HOME": sd}, timeout=60)', '"HOME": sd}, timeout=0.001)'),
    # readonly clause r
    ("V1-readonly-always-ok", 'readonly = "fail" if os.path.exists(marker) else "ok"', 'readonly = "ok"'),
    ("V2-marker-name-x", 'marker = os.path.join(work, "marker-%d" % seed)',
     'marker = os.path.join(work, "marker-x")'),
    ("V3-fakebin-drop-journalctl", 'for n in ("hyprctl", "journalctl", "wlr-randr", "wayland-info"):',
     'for n in ("hyprctl", "wlr-randr", "wayland-info"):'),
    # clause a (tool present)
    ("A1-clause-a-mode-drop", 'bool(ls) and ls.split()[0] in (b"100644", b"100755") and ls.split()[1] == b"blob"',
     'bool(ls) and ls.split()[1] == b"blob"'),
    ("A2-clause-a-blob-drop", 'bool(ls) and ls.split()[0] in (b"100644", b"100755") and ls.split()[1] == b"blob"',
     'bool(ls) and ls.split()[0] in (b"100644", b"100755")'),
    # met computation
    ("M1-met-fixtures-ge0", "fixtures_ok == len(FIXTURES)", "fixtures_ok >= 0"),
    ("M2-fixtures-ok-plus1", "fixtures_ok += ok", "fixtures_ok += 1"),
    ("M3-met-selftest-always", 'selftest == "ok" and readonly', 'selftest != "x" and readonly'),
    ("M4-met-readonly-always", 'and readonly == "ok" and fixtures_ok', 'and readonly != "x" and fixtures_ok'),
    ("M5-met-and-to-or",
     'met = present and selftest == "ok" and readonly == "ok" and fixtures_ok == len(FIXTURES)',
     'met = (present and selftest == "ok") or (readonly == "ok" and fixtures_ok == len(FIXTURES))'),
    # fixture expectations (contract side)
    ("E1-host-drop-R", HOST_OLD, HOST_DROP_R),
    ("E2-host-flip-DIFFER",
     HOST_OLD.split("\n      S(")[0], HOST_FLIP),
    ("E3-host-rc-1", HOST_OLD, HOST_OLD.replace('], 0),', '], 1),')),
    ("E4-norules-drop-O", NORULES_OLD, NORULES_NEW),
    ("E5-join-no-newline", 'want = "".join(subst(l, table) + "\\n" for l in expect)',
     'want = "".join(subst(l, table) for l in expect)'),
    ("E6-subst-noop", "obj = obj.replace(k, v)", "obj = obj"),
    # name table / seed
    ("N1-dedupe-drop", "        if n not in picked:", "        if True:"),
    ("N2-shuffle-drop", "    rng.shuffle(picked)", "    pass"),
    ("N3-drop-D", '    return {"{A}": a, "{B}": b, "{C}": c, "{D}": d}',
     '    return {"{A}": a, "{B}": b, "{C}": c}'),
    ("N4-drop-DP-prefix", '    pre = ["DP-", "HDMI-A-", "eDP-", "DVI-D-", "Virtual-", "USB-C-"]',
     '    pre = ["HDMI-A-", "eDP-", "DVI-D-", "Virtual-", "USB-C-"]'),
    ("N5-seed-default-46", "type=int, default=45", "type=int, default=46"),
    # fixture environment
    ("G1-env-drop-LANG", 'env = {"PATH": fakebin + ":/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": home,',
     'env = {"PATH": fakebin + ":/usr/bin:/bin", "HOME": home,'),
    ("G2-env-drop-HOME", '"LANG": "C.UTF-8", "HOME": home,', '"LANG": "C.UTF-8",'),
    ("G3-env-path-nofakebin", '"PATH": fakebin + ":/usr/bin:/bin"', '"PATH": "/usr/bin:/bin"'),
    ("G4-env-drop-HIS", '"HYPRLAND_INSTANCE_SIGNATURE": "mado-r45-fixture"}', '}'),
]

BAD_CONTROLS = ["K00-BASE-ABSENT", "K02-STUB", "K01-GEOMETRY-COPY"] + \
               [v[0] for v in mod.VARIANTS]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def build_repos(workroot):
    lane = LANE
    ref_text = open(os.path.join(lane, mod.REF)).read()
    geom = mod.git(lane, "show", mod.BASE + ":tools/mado-geometry.py").decode()
    controls = [("REF", ref_text), ("K00-BASE-ABSENT", None), ("K01-GEOMETRY-COPY", geom),
                ("K02-STUB", mod.STUB)]
    for name, what, subs in mod.VARIANTS:
        t = ref_text
        for old, new in subs:
            if old not in t:
                raise SystemExit("variant %s: anchor not found: %r" % (name, old[:60]))
            t = t.replace(old, new)
        controls.append((name, t))
    repos = {}
    for name, text in controls:
        repos[name] = mod.build(lane, workroot, name, text)
    return repos


def run_counter(mutpath, repo, workroot):
    w = tempfile.mkdtemp(dir=workroot, prefix="w-")
    try:
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        p = subprocess.run([sys.executable, "-I", mutpath, "--repo", repo, "--rev", "HEAD",
                            "--work", w], capture_output=True, text=True, timeout=240,
                           cwd=workroot, env=env)
        out = p.stdout
        err = p.stderr
    except subprocess.TimeoutExpired as e:
        return {"rc": "timeout", "last": "", "fails": [], "stdout_tail": (e.stdout or b"")[-500:].decode("utf-8", "replace") if isinstance(e.stdout, bytes) else ""}
    finally:
        shutil.rmtree(w, ignore_errors=True)
    lines = out.strip().split("\n") if out.strip() else []
    last = lines[-1] if lines else ""
    fails = [l for l in lines if "FAIL" in l or "clause=s" in l or "clause=r" in l or "clause=a" in l]
    return {"rc": p.returncode, "last": last, "fails": fails,
            "stdout": out, "stderr_tail": err[-400:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["check", "run"], required=True)
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--out", default=ROOT + "/results.json")
    a = ap.parse_args()

    base = open(FROZEN, "rb").read()
    assert sha(base) == FROZEN_SHA, "frozen counter hash mismatch"
    base_text = base.decode()

    counts = {}
    for name, old, new in MUTANTS:
        counts[name] = base_text.count(old) if old is not None else 1
    if a.mode == "check":
        for name, old, new in MUTANTS:
            flag = "" if counts[name] == 1 else "  <-- COUNT=%d" % counts[name]
            print("%-34s count=%d%s" % (name, counts[name], flag))
        return 0

    bad = [n for n, c in counts.items() if c != 1]
    if bad:
        print("NON-UNIQUE OR MISSING ANCHORS: %s" % bad)
        return 2

    workroot = tempfile.mkdtemp(dir=ROOT, prefix="mutwork-")
    os.makedirs(workroot + "/w", exist_ok=True)
    mdir = tempfile.mkdtemp(dir=ROOT, prefix="mutants-")
    mutpath = {}
    mutsha = {}
    for name, old, new in MUTANTS:
        text = base_text if old is None else base_text.replace(old, new)
        p = os.path.join(mdir, name + ".py")
        with open(p, "w") as f:
            f.write(text)
        mutpath[name] = p
        mutsha[name] = sha(text.encode())

    t0 = time.time()
    repos = build_repos(workroot)
    print("repos built: %d in %.1fs" % (len(repos), time.time() - t0), flush=True)

    results = {}
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=a.workers)

    def do(mname, cname):
        return run_counter(mutpath[mname], repos[cname], workroot + "/w")

    t1 = time.time()
    futs = {(m, "REF"): pool.submit(do, m, "REF") for m, _, _ in MUTANTS}
    for key, fut in futs.items():
        results.setdefault(key[0], {})["ref"] = fut.result()
    print("phase A (REF) done in %.1fs" % (time.time() - t1), flush=True)

    ref_met = [m for m, _, _ in MUTANTS if "verdict=TARGET_MET" in results[m]["ref"]["last"]]
    t2 = time.time()
    futs = {}
    for m in ref_met:
        for c in BAD_CONTROLS:
            futs[(m, c)] = pool.submit(do, m, c)
    for (m, c), fut in futs.items():
        results[m].setdefault("controls", {})[c] = fut.result()
    print("phase B (%d mutants x %d controls) done in %.1fs" % (len(ref_met), len(BAD_CONTROLS), time.time() - t2), flush=True)
    pool.shutdown()

    for m, _, _ in MUTANTS:
        r = results[m]
        ref = r["ref"]
        r["mutsha"] = mutsha[m]
        if not ref.get("last"):
            r["class"] = "CRASH/INVALID" if m != "X0-identity" else "HARNESS-BROKEN"
            continue
        r["ref_met"] = "verdict=TARGET_MET" in ref["last"]
        if not r["ref_met"]:
            r["class"] = "OVER-STRICT"
            continue
        met_ctl = [c for c in BAD_CONTROLS if "verdict=TARGET_MET" in r["controls"][c]["last"]]
        r["met_controls"] = met_ctl
        r["class"] = "GATE-BROKEN:" + ",".join(met_ctl) if met_ctl else "SURVIVOR"

    with open(a.out, "w") as f:
        json.dump(results, f, indent=1)
    for m, _, _ in MUTANTS:
        r = results[m]
        print("%-34s %-22s ref=%s %s" % (
            m, r.get("class", "?"),
            "MET" if r.get("ref_met") else "missed",
            ("broke=" + ",".join(r.get("met_controls", []))) if r.get("met_controls") else ""))
    print("total %.1fs" % (time.time() - t0))
    shutil.rmtree(workroot, ignore_errors=True)
    shutil.rmtree(mdir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
