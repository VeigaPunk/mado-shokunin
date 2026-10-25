#!/usr/bin/env python3
"""Generate NEW single-edit mutants of c1/ctl-ref-tool.py.txt (round 41, w1).

Every entry is one contiguous textual replacement of the reference, chosen so
that no entry duplicates a name/edit of ctl/run-c1-controls.py (43 mutants +
3 do-nothing controls). Usage: python3 gen_mutants.py [--ref PATH] [--out DIR]
"""
import argparse
import os

MUTANTS = [
    # --- session identification
    ("N43-boot-repeat-same-id-no-split",
     "            boot = m.group(1)\n            boot_changed = True",
     "            boot_changed = boot_changed or boot != m.group(1)\n"
     "            boot = m.group(1)"),
    ("N01-session-key-host-not-pid",
     "        ts, _host, pid, name, ver = m.groups()",
     "        ts, pid, _host, name, ver = m.groups()"),
    ("N02-boot-id-from-full-line",
     "            boot = m.group(1)",
     "            boot = m.group(0)"),
    ("N19-boot-line-never-splits",
     "            boot_changed = True",
     "            boot_changed = boot != m.group(1)"),
    ("N38-boot-reset-per-session",
     "            boot_changed = False",
     '            boot_changed = False\n            boot = "-"'),
    ("N23-pid-int-compare",
     'or cur["pid"] != pid:',
     'or int(cur["pid"]) != int(pid):'),
    ("N21-sessions-count-distinct-pids",
     '                   len(sessions), latest["pid"] if latest else "-", len(names),',
     '                   len(set(s["pid"] for s in sessions)), '
     'latest["pid"] if latest else "-", len(names),'),
    ("N25-session-numbering-from-0",
     "    for i, s in enumerate(sessions, 1):",
     "    for i, s in enumerate(sessions):"),
    # --- latest session selection
    ("N03-latest-is-longest",
     "    latest = sessions[-1] if sessions else None",
     '    latest = max(sessions, key=lambda s: s["adverts"]) '
     "if sessions else None"),
    ("N08-global-lines-all-sessions",
     '        for name in sorted(latest["names"]):',
     '        for name in sorted(set().union(*[set(s["names"]) for s in sessions])):'),
    ("N22-sort-case-insensitive-globals",
     '        for name in sorted(latest["names"]):',
     '        for name in sorted(latest["names"], key=str.lower):'),
    # --- per-session fields
    ("N04-class-counts-adverts",
     '        classes[classify(n)] = classes.get(classify(n), 0) + 1',
     '        classes[classify(n)] = classes.get(classify(n), 0) + names[n][0]'),
    ("N05-first-tracks-last",
     '        cur["last"] = ts',
     '        cur["last"] = ts\n        cur["first"] = ts'),
    ("N06-count-distinct-only",
     "        ent[0] += 1",
     "        ent[0] = 1 if not ent[0] else ent[0]"),
    ("N27-interfaces-counts-adverts",
     'len(s["names"]), s["adverts"]))',
     's["adverts"], s["adverts"]))'),
    ("N32-adverts-counts-distinct",
     '        cur["adverts"] += 1',
     '        cur["adverts"] = len(cur["names"])'),
    ("N33-session-boot-always-dash",
     '(i, s["boot"], s["pid"],',
     '(i, "-", s["pid"],'),
    ("N34-last-is-max-ts",
     '        cur["last"] = ts',
     '        cur["last"] = max(cur["last"], ts)'),
    # --- expect
    ("N07-expect-case-insensitive",
     "    missing = sorted(set(e for e in expects if e not in names))",
     "    missing = sorted(set(e for e in expects if e.lower() "
     "not in [n.lower() for n in names]))"),
    ("N20-expect-any-session",
     "    missing = sorted(set(e for e in expects if e not in names))",
     '    missing = sorted(set(e for e in expects if e not in '
     'set().union(*[set(s["names"]) for s in sessions])))'),
    ("N14-empty-file-expect-ok",
     '    if not sessions:\n        verdict, code = "NO_SESSIONS", 3',
     '    if not sessions:\n        verdict, code = ("NO_SESSIONS", 3) '
     'if not expects else ("OK", 0)'),
    ("N39-expect-hyphen-allowed",
     'NAME = re.compile(r"[A-Za-z0-9_]{1,128}")',
     'NAME = re.compile(r"[A-Za-z0-9_-]{1,128}")'),
    # --- diff
    ("N10-diff-missing-exit-0",
     '    elif missing:\n        verdict, code = "MISSING_EXPECTED", 1',
     '    elif missing:\n        verdict, code = "MISSING_EXPECTED", '
     '0 if diff else 1'),
    ("N11-diff-first-vs-last",
     '            a, b = sessions[-2]["names"], sessions[-1]["names"]',
     '            a, b = sessions[0]["names"], sessions[-1]["names"]'),
    ("N29-diff-ver-increase-only",
     "if a[n][1] != b[n][1]]",
     "if a[n][1] < b[n][1]]"),
    # --- version / name parsing
    ("N12-version-string-compare",
     "        ent[1] = max(ent[1], ver)",
     "        ent[1] = int(max(str(ent[1]), str(ver)))"),
    ("N13-name-129-truncated",
     r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver",
     r"Got interface: ([A-Za-z0-9_]{1,128})[A-Za-z0-9_]* \(ver"),
    ("N24-ver-5-digits-max",
     r"\(ver (\d{1,6})\)",
     r"\(ver (\d{1,5})\)"),
    ("N15-decode-latin-1",
     '    text = data.decode("utf-8", "replace")',
     '    text = data.decode("latin-1")'),
    ("N16-log-case-insensitive",
     r"\[LOG\]  \| ",
     r"(?i:\[log\])  \| "),
    ("N40-class-lowercased",
     "    return CLASS_OF.get(name, \"other\")",
     "    return CLASS_OF.get(name.lower(), \"other\")"),
    # --- output formatting
    ("N09-trailing-space-global-line",
     '"MADO_GLOBAL: name=%s ver=%d count=%d class=%s"',
     '"MADO_GLOBAL: name=%s ver=%d count=%d class=%s "'),
    ("N28-classes-drop-other",
     "    for n in names:\n        classes[classify(n)]",
     '    for n in [x for x in names if classify(x) != "other"]:\n'
     "        classes[classify(n)]"),
    ("N31-stderr-noise",
     "    for line in lines:\n        print(line)",
     '    sys.stderr.write("x")\n    for line in lines:\n        print(line)'),
    ("N41-usage-exit-1",
     'ap.error = lambda msg: (_ for _ in ()).throw(Setup("usage"))',
     'ap.error = lambda msg: (_ for _ in ()).throw(Setup("usage", 1))'),
    # --- input size / reading
    ("N30-size-limit-plus-two",
     '    if len(data) > MAX_BYTES:\n        raise Setup("too_large")',
     '    if len(data) > MAX_BYTES + 1:\n        raise Setup("too_large")'),
    ("N35-read-only-max-bytes",
     "            data = fh.read(MAX_BYTES + 1)",
     "            data = fh.read(MAX_BYTES)"),
    # --- live program
    ("N17-env-adds-home",
     '    env = {k: os.environ[k] for k in ("PATH", "XDG_RUNTIME_DIR",',
     '    env = {k: os.environ[k] for k in ("PATH", "HOME", "XDG_RUNTIME_DIR",'),
    ("N18-program-relative-to-cwd",
     '            cand = os.path.join(d or ".", prog)',
     "            cand = prog"),
    ("N37-path-loop-is-cwd",
     '        for d in os.environ.get("PATH", "").split(":"):',
     "        for d in [os.getcwd()]:"),
    ("N42-live-no-timeout",
     "                           env=env, timeout=30, shell=False)",
     "                           env=env, timeout=None, shell=False)"),
    ("N26-journalctl-allowed-with-file",
     '    if args.journalctl is not None and not args.live:\n'
     '        raise Setup("usage")',
     '    if False:\n        raise Setup("usage")'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..",
        "c1", "ctl-ref-tool.py.txt"))
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "mutants"))
    args = ap.parse_args()
    ref = open(args.ref, encoding="utf-8").read()
    os.makedirs(args.out, exist_ok=True)
    names = set()
    bad = 0
    for name, old, new in MUTANTS:
        if name in names:
            print("DUP name %s" % name)
            bad += 1
        names.add(name)
        if ref.count(old) != 1:
            print("ABSENT/AMBIGUOUS %s count=%d" % (name, ref.count(old)))
            bad += 1
            continue
        src = ref.replace(old, new, 1)
        if src == ref:
            print("NOOP %s" % name)
            bad += 1
            continue
        with open(os.path.join(args.out, name + ".py"), "w",
                  encoding="utf-8") as fh:
            fh.write(src)
        print("WROTE %s" % name)
    print("MUTANTS total=%d bad=%d" % (len(MUTANTS), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
