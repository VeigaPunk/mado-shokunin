#!/usr/bin/env python3
"""Controls for PRED-C1-r41-v2 (quality/counters/c1-r41-globals-v2.py).

The reference (c1/ctl-ref-tool-v2.py.txt) must reach TARGET_MET; every do-nothing
control and single-defect mutant of it must not. Output: one line per control
and `CTL_C1V2: controls=N correct=K/N`. Controls run in parallel (--jobs). Usage:
  python3 -I run-c1-controls.py --repo LANE --counter PATH --ref PATH [--only NAME]
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

ECHO = '''#!/usr/bin/env python3
import sys
if sys.argv[1:] == ["--selftest"]:
    print("MADO_GLOBALS_SELFTEST: 40/40 passed")
    sys.exit(0)
print("MADO_GLOBALS: sessions=0 latest_pid=- interfaces=0 classes=- expected_missing=- verdict=NO_SESSIONS")
sys.exit(3)
'''
EMPTY = "import sys\n"
HARD = '''#!/usr/bin/env python3
import sys
if sys.argv[1:] == ["--selftest"]:
    print("MADO_GLOBALS_SELFTEST: 40/40 passed")
    sys.exit(0)
print("MADO_GLOBALS_SESSION: n=1 boot=- pid=1918 first=2026-10-25T13:16:45-03:00 last=2026-10-25T13:16:45-03:00 interfaces=8 adverts=15")
print("MADO_GLOBALS: sessions=1 latest_pid=1918 interfaces=8 classes=other:8 expected_missing=- verdict=OK")
'''

# (name, old, new) single textual edits of the reference
MUTANTS = [
    ("M01-class-focus-grab-dropped", '"focus-grab": ["hyprland_focus_grab_manager_v1"]', '"focus-grab": []'),
    ("M02-session-ignores-pid", 'or cur["pid"] != pid:', 'or False:'),
    ("M03-session-ignores-boot", 'if cur is None or boot_changed or', 'if cur is None or'),
    ("M04-ver-last-not-max", 'ent[1] = max(ent[1], ver)', 'ent[1] = ver'),
    ("M05-level-loosened", r'\[LOG\]  \| "', r'\[[A-Z]+\]  \| "'),
    ("M06-spacing-loosened", r'\[LOG\]  \| "', r'\[LOG\] +\| "'),
    ("M07-size-limit-doubled", 'MAX_BYTES = 8 * 1024 * 1024', 'MAX_BYTES = 16 * 1024 * 1024'),
    ("M08-names-unsorted", 'for name in sorted(latest["names"]):', 'for name in latest["names"]:'),
    ("M09-expect-not-deduped", ['missing = sorted(set(e for e in expects if e not in names))', 'sorted(set(args.expect))'], ['missing = sorted(e for e in expects if e not in names)', 'args.expect']),
    ("M10-env-passthrough", 'env = {k: os.environ[k] for k in ("PATH", "XDG_RUNTIME_DIR",\n                                      "DBUS_SESSION_BUS_ADDRESS", "LC_ALL")\n           if k in os.environ}', 'env = dict(os.environ)'),
    ("M11-stdin-inherited", 'stdin=subprocess.DEVNULL', 'stdin=None'),
    ("M12-writable-accepted", ' \\\n            or st.st_mode & (stat.S_IWGRP | stat.S_IWOTH):', ':'),
    ("M13-shell-true", 'shell=False', 'shell=True'),
    ("M14-spawns-in-file-mode", 'data = read_file(args.journal_file)', 'subprocess.run(["/usr/bin/true"], capture_output=True)\n        data = read_file(args.journal_file)'),
    ("M15-no-sessions-exit-1", 'verdict, code = "NO_SESSIONS", 3', 'verdict, code = "NO_SESSIONS", 1'),
    ("M16-diff-none-line", '"MADO_GLOBALS_DIFF: sessions=%d none"', '"MADO_GLOBALS_DIFF: none %d"'),
    ("M17-last-ts-frozen", 'cur["last"] = ts', 'cur["last"] = cur["first"]'),
    ("M18-argv-no-pager-dropped", '"--no-pager",\n                   "-o", "short-iso"]', '"-o", "short-iso"]'),
    ("M19-both-sources-allowed", 'if bool(args.journal_file) == bool(args.live):', 'if not (args.journal_file or args.live):'),
    ("M20-abbrev-allowed", 'allow_abbrev=False', 'allow_abbrev=True'),
    ("M21-expect-unchecked", 'if not NAME.fullmatch(e):', 'if False:'),
    ("M22-classes-unsorted", 'for c in sorted(classes))', 'for c in classes)'),
    ("M23-size-off-by-one", '    if len(data) > MAX_BYTES:\n        raise Setup("too_large")', '    if len(data) >= MAX_BYTES:\n        raise Setup("too_large")'),
    ("M24-live-size-unchecked", 'if total > MAX_BYTES:', 'if False:'),
    ("M25-count-always-1", 'ent[0] += 1', 'ent[0] = 1'),
    ("M26-path-lookup-off", 'if "/" not in prog:', 'if False:'),
    ("M27-boot-uppercase", 'BOOT = re.compile(r"-- Boot ([0-9a-f]{32}) --")', 'BOOT = re.compile(r"-- Boot ([0-9a-fA-F]{32}) --")'),
    ("M28-name-dash-allowed", 'Got interface: ([A-Za-z0-9_]{1,128})', 'Got interface: ([A-Za-z0-9_-]{1,128})'),
    ("M29-name-129-allowed", 'Got interface: ([A-Za-z0-9_]{1,128})', 'Got interface: ([A-Za-z0-9_]{1,200})'),
    ("M30-ver-7-digits", r'\(ver ([0-9]{1,6})\)', r'\(ver ([0-9]{1,7})\)'),
    ("M31-diff-removed-dropped", 'removed = sorted(set(a) - set(b))', 'removed = []'),
    ("M32-verchanged-dropped", 'if a[n][1] != b[n][1]]', 'if False]'),
    ("M33-exit-missing-0", 'verdict, code = "MISSING_EXPECTED", 1', 'verdict, code = "MISSING_EXPECTED", 0'),
    ("M34-no-sessions-loses", '    elif not sessions:\n        verdict, code = "NO_SESSIONS", 3\n    elif missing:', '    elif missing:\n        verdict, code = "MISSING_EXPECTED", 1\n    elif not sessions:'),
    ("M35-latest-pid-first", 'latest["pid"] if latest else "-"', 'sessions[0]["pid"] if latest else "-"'),
    ("M36-class-xdg-activation-other", '"ext_foreign_toplevel_list_v1", "xdg_activation_v1",', '"ext_foreign_toplevel_list_v1",'),
    ("M37-live-rc-ignored", 'if rc != 0:\n        raise Setup("journalctl_failed", 5)', 'if False:\n        raise Setup("journalctl_failed", 5)'),
    ("M38-crlf-tolerated", 'for line in text.split("\\n"):', 'for line in text.replace("\\r", "").split("\\n"):'),
    ("M39-selftest-echo", 'print("MADO_GLOBALS_SELFTEST: %d/%d passed" % (ok, n))\n    return 0 if ok == n else 1', 'print("MADO_GLOBALS_SELFTEST: 99/99 passed")\n    return 0'),
    ("C1-cheat-exec", 'def classify(name):', 'exec("pass")\ndef classify(name):'),
    ("C2-cheat-os-system", 'def classify(name):', 'os.system("true")\ndef classify(name):'),
    ("C3-cheat-socket-import", 'import argparse\n', 'import argparse\nimport socket\n'),
    ("C4-cheat-counter-name", 'def classify(name):', 'X = "quality/counters"\ndef classify(name):'),
]


def score(counter, repo, tool, rev):
    p = subprocess.run(["python3", "-I", counter, "--repo", repo, "--rev", rev,
                        "--tool", tool], capture_output=True, text=True,
                       timeout=900)
    last = [l for l in p.stdout.splitlines() if "PRED-C1-r41-v2" in l and
            ": fixtures=" in l]
    return p.returncode, (last[-1] if last else p.stdout[-200:] + p.stderr[-200:])


K_CHEATS = [
    # (name, [(old, new)...]) single or double edits that try to get TARGET_MET without the work
    ("K01-stub-bytes-read", [('    prog = resolve_program(prog)\n    env = {k:',
                              '    prog = resolve_program(prog)\n    return open(prog, "rb").read()\n    env = {k:')]),
    ("K02-cwd-journal-replay", [('    prog = resolve_program(prog)\n    env = {k:',
                                 '    prog = resolve_program(prog)\n    return open("j.txt", "rb").read()\n    env = {k:')]),
    ("K03-name-word-class", [('Got interface: ([A-Za-z0-9_]{1,128})', 'Got interface: (\\\\w{1,128})')]),
    ("K04-child-interpreter", [('    sessions, ignored = parse(data)\n    return report',
                                '    subprocess.run(["/usr/bin/true"])\n    sessions, ignored = parse(data)\n    return report')]),
    ("K05-selftest-argv0-path", [('    ts = "2026-10-25T13:36:24-03:00"\n    fmt',
                                  '    check(os.path.basename(os.path.dirname(os.path.abspath(sys.argv[0]))) == "tool")\n    ts = "2026-10-25T13:36:24-03:00"\n    fmt')]),
    ("K06-eval-via-getattr", [('def classify(name):', '_E = getattr(sys.modules["builtins"], "ev" + "al")\n\n\ndef classify(name):')]),
    ("K07-selftest-size-fingerprint", [('    ts = "2026-10-25T13:36:24-03:00"\n    fmt',
                                        '    check(os.path.getsize(sys.argv[:1][0]) == 100000)\n    ts = "2026-10-25T13:36:24-03:00"\n    fmt')]),
    ("K08-kwargs-unpack", [('stdin=subprocess.DEVNULL,', '**{"stdin": subprocess.DEVNULL},')]),
    ("K09-globals-lookup", [('def classify(name):', '_G = globals()\n\n\ndef classify(name):')]),
    ("K11-ver-5-digits", [('([0-9]{1,6})\\)")', '([0-9]{1,5})\\)")')]),
    ("K12-live-no-timeout", [('LIVE_TIMEOUT = 30', 'LIVE_TIMEOUT = 100000')]),
    ("K10-file-path-name", [('def classify(name):', '_P = __file__\n\n\ndef classify(name):')]),
]


def build_controls(ref, mutant_dir):
    import importlib.util
    controls = [("P-reference", ref, True), ("D1-empty", EMPTY, False),
                ("D2-echo-no-sessions", ECHO, False),
                ("D3-hardcoded-report", HARD, False)]
    skipped = []
    for name, old, new in MUTANTS:
        olds, news = (old, new) if isinstance(old, list) else ([old], [new])
        src = ref
        for o, n in zip(olds, news):
            if o not in src:
                skipped.append(name)
                break
            src = src.replace(o, n, 1)
        else:
            controls.append((name, src, False))
    for name, edits in K_CHEATS:
        src = ref
        for o, n in edits:
            if o not in src:
                skipped.append(name)
                break
            src = src.replace(o, n, 1)
        else:
            if name.startswith("K07"):
                for _ in range(2):
                    src = src.replace("== 100000)", "== %06d)" % len(src.encode()))
            controls.append((name, src, False))
    gm = os.path.join(mutant_dir, "gen_mutants.py")
    if os.path.exists(gm):
        spec = importlib.util.spec_from_file_location("gen_mutants", gm)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for name, old, new in mod.MUTANTS:
            if old in ref and ("W1-" + name) not in [c[0] for c in controls]:
                controls.append(("W1-" + name, ref.replace(old, new, 1), False))
            else:
                skipped.append("W1-" + name)
    return controls, skipped


def main():
    from concurrent.futures import ThreadPoolExecutor
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--counter", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--rev", default="master")
    ap.add_argument("--only", default=None)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--mutants", default=None,
                    help="dir holding the wave's gen_mutants.py (ExecC1ExtraMutants)")
    args = ap.parse_args()
    ref = open(args.ref).read()
    tmp = tempfile.mkdtemp(prefix="ctl-c1r41v2-")
    controls, skipped = build_controls(ref, args.mutants or "/nonexistent")
    print("CTL_C1V2: skipped-patterns-absent=%d %s" % (len(skipped), " ".join(skipped)))
    todo = []
    for name, src, want_met in controls:
        if args.only and args.only not in name:
            continue
        path = os.path.join(tmp, name + ".py")
        open(path, "w").write(src)
        todo.append((name, path, want_met))

    def one(t):
        name, path, want_met = t
        rc, line = score(args.counter, args.repo, path, args.rev)
        met = rc == 0 and "TARGET_MET" in line
        return name, want_met, met, line

    good = total = 0
    with ThreadPoolExecutor(args.jobs) as ex:
        for name, want_met, met, line in ex.map(one, todo):
            ok = met == want_met
            good += ok
            total += 1
            print("CTL_C1V2 control=%s expect=%s got=%s correct=%d | %s" % (
                name, "MET" if want_met else "MISSED", "MET" if met else "MISSED",
                ok, re.sub(r" rev=\S+", "", line)))
    print("CTL_C1V2: controls=%d correct=%d/%d" % (total, good, total))
    return 0 if good == total else 1


if __name__ == "__main__":
    sys.exit(main())
