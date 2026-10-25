#!/usr/bin/env python3
"""Round-40 C1 v2 controls: PRED-C1-r40-v2 scored over cheats and mutants.

Controls (each scored with the frozen v2 counter's `--tool`, at a fixed nonce
so the receipt is reproducible; the pass criterion does not depend on the nonce):

  REF      the reference tool (c1/ctl-ref-tool-v2.py.txt): must score
           TARGET_MET (the target is reachable by an honest implementation);
  BASE     the unmodified base tool: fixtures=0/16, never MET;
  CHEATS   the wave's falsification exploits against v1 (c1/cheats/*.py: judge
           leak through /proc and by path, the forged call log, the echo
           selftest, the REV-seed replay, the echo-with-base-parser) plus
           single-edit cheats of REF (fabricated live payload, exec-imported
           socket, hardcoded hostile list, all-keys failure text, duplicated
           rows, write into the config tree): none may be TARGET_MET;
  MUTANTS  single-defect mutants of REF: each must score fixtures<16 or fail a
           clause (TARGET_MISSED).

Final line: `CTL_C1V2: controls=N correct=K/N`.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r40-live-v2.py")
REF = os.path.join(HERE, "..", "c1", "ctl-ref-tool-v2.py.txt")
CHEATS = os.path.join(HERE, "..", "c1", "cheats")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
REV = os.environ.get("MADO_CTL_REV", "master")
NONCE = os.environ.get("MADO_CTL_NONCE", "00c0ffee00c0ffee")

# (name, old, new) - each applied once to the reference text.
EDITS = [
    ("M01-all-agree",
     'def native_equal(form, declared, live, inherited=0):\n',
     'def native_equal(form, declared, live, inherited=0):\n    return True\n'),
    ("M02-raw-compare",
     'def native_equal(form, declared, live, inherited=0):\n',
     'def native_equal(form, declared, live, inherited=0):\n'
     '    return declared.strip() == str(live).strip()\n'),
    ("M03-bool-exact",
     'if value.startswith(("true", "on", "yes")):',
     'if value in ("true", "on", "yes"):'),
    ("M04-angle-ignored",
     '" %ddeg" % angle', '" %ddeg" % 0'),
    ("M05-gap3-wrong",
     'sides = [sides[0], sides[1], sides[2], sides[1]]',
     'sides = [sides[0], sides[1], sides[2], sides[0]]'),
    ("M06-config-only-as-mismatch",
     'row["agreement"] = "config-only"\n            row["live"] = None',
     'row["agreement"] = "mismatch"\n            row["live"] = None'),
    ("M07-extra-request",
     '    try:\n        proc = subprocess.run([hyprctl, "getoption", "-j", key],',
     '    subprocess.run([hyprctl, "version"], capture_output=True)\n'
     '    try:\n        proc = subprocess.run([hyprctl, "getoption", "-j", key],'),
    ("M08-set-ignored",
     'if not isset or not native_equal(', 'if not native_equal('),
    ("M09-shadow-ignored",
     '        elif options[row["key"]]["_decls"] > 1:\n'
     '            row["agreement"] = "agreement*"\n        else:\n'
     '            row["agreement"] = "agreement"\n    for key in probes:',
     '        else:\n            row["agreement"] = "agreement"\n'
     '    for key in probes:'),
    ("M10-hostile-probe-accepted",
     '        if not key or key.startswith("-"):', '        if False:'),
    ("M11-failure-swallowed",
     '    if proc.returncode != 0:\n        raise CtlError("%s: %s exited %d" '
     '% (key, hyprctl, proc.returncode))',
     '    if proc.returncode != 0:\n        return None'),
    ("M12-writes-config-root",
     '    home = os.path.abspath(args.home)\n',
     '    home = os.path.abspath(args.home)\n'
     '    open(os.path.join(home, ".config", "hypr", "zz.tmp"), "w").write("x")\n'),
    ("M13-int-normalisation-dropped",
     '        return hl_int(text) == live\n',
     '        return text == str(live)\n'),
    ("M14-live-field-dropped",
     '        row["live"] = str(value)\n', '        row["live"] = None\n'),
    ("M15-angle-inheritance-absent",
     'options[row["key"]].get("_inherited", 0)', '0'),
    ("M16-probe-no-such-masked",
     '        reply = native_query(hyprctl, key)\n        if reply is None:\n'
     '            continue',
     '        reply = native_query(hyprctl, key)\n        if reply is None:\n'
     '            reply = ("str", "", False)'),
    ("M17-alpha-truncated",
     'int(math.floor(float(parts[3]) * 255.0 + 0.5))',
     'int(float(parts[3]) * 255.0)'),
    ("M18-alpha-bankers-round",
     'int(math.floor(float(parts[3]) * 255.0 + 0.5))',
     'int(round(float(parts[3]) * 255.0))'),
    ("M19-sentinel-substring",
     '    if text == "no such option":', '    if "no such option" in text:'),
    ("M20-strict-padding",
     '    text = proc.stdout.strip()\n',
     '    text = proc.stdout.strip()\n'
     '    if proc.stdout != text + "\\n":\n'
     '        raise CtlError("%s: padded reply from %s" % (key, hyprctl))\n'),
    ("M21-probe-dedup-dropped",
     '        if key in seen:\n            continue\n        seen.add(key)',
     '        seen.add(key)'),
    ("M22-probe-failure-swallowed",
     '        seen.add(key)\n        reply = native_query(hyprctl, key)\n'
     '        if reply is None:\n            continue\n        form, value, isset = reply',
     '        seen.add(key)\n        try:\n            reply = native_query(hyprctl, key)\n'
     '        except CtlError:\n            continue\n        if reply is None:\n'
     '            continue\n        form, value, isset = reply'),
    ("M23-float-exact",
     'return abs(float(text) - float(live)) < 1e-6',
     'return float(text) == float(live)'),
    ("M24-weight-case-sensitive",
     'WEIGHTS.get(text.lower(), -1)', 'WEIGHTS.get(text, -1)'),
    ("M25-angle-int-not-prefix",
     'angle = stoi_prefix(token[:token.index("deg")])',
     'angle = int(token[:token.index("deg")])'),
    ("M26-gap2-css-swapped",
     'sides = [sides[0], sides[1], sides[0], sides[1]]',
     'sides = [sides[0], sides[0], sides[1], sides[1]]'),
    ("M27-sort-dropped",
     '        })\n    rows.sort(key=lambda r: r["key"])\n\n\ndef run_static',
     '        })\n\n\ndef run_static'),
    ("M28-live-raw-type",
     '        row["live"] = str(value)\n', '        row["live"] = value\n'),
    ("M29-hyprctl-default-empty",
     'metavar="PATH", default="hyprctl"', 'metavar="PATH", default=""'),
    ("M30-vec2-second-ignored",
     'and abs(pair[1] - float(live[1])) < 1e-6)', ')'),
    ("M32-form-less-accepted",
     'if len(forms) != 1 or "set" not in reply:',
     'if len(forms) > 1 or "set" not in reply:'),
    ("M33-vec2-form-missing",
     'FORMS = ("int", "float", "str", "custom", "vec2")',
     'FORMS = ("int", "float", "str", "custom")'),
    ("M34-failure-names-all-keys",
     '    except CtlError as exc:\n        sys.stderr.write("mado-options.py: %s\\n" % exc)\n        return 5',
     '    except CtlError as exc:\n        sys.stderr.write("mado-options.py: %s %s\\n" % (exc, " ".join(r["key"] for r in rows)))\n        return 5'),
    ("X01-fabricated-live-payload",
     '        row["live"] = str(value)\n', '        row["live"] = "FABRICATED"\n'),
    ("X02-exec-import-socket",
     'import argparse\n', 'import argparse\nexec("import socket")\n'),
    ("X03-hardcoded-hostile-list",
     '        if not key or key.startswith("-"):',
     '        if key in ("-x", "--version", ""):'),
    ("X04-duplicate-rows",
     '        })\n    rows.sort(key=lambda r: r["key"])\n\n\ndef run_static',
     '        })\n    rows.extend([dict(r) for r in rows])\n'
     '    rows.sort(key=lambda r: r["key"])\n\n\ndef run_static'),
]


def score(path):
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", LANE,
                        "--rev", REV, "--tool", path, "--nonce", NONCE],
                       capture_output=True, text=True, env=ENV)
    lines = p.stdout.strip().splitlines()
    last = lines[-1] if lines else "NO-OUTPUT rc=%d %s" % (
        p.returncode, p.stderr.strip()[:100])
    return p.returncode, last.split(": ", 1)[-1].split(" rev=")[0]


def fixtures_of(line):
    m = re.search(r"fixtures=(\d+)/", line)
    return int(m.group(1)) if m else None


def main():
    ref = open(REF).read()
    tmp = tempfile.mkdtemp(prefix="mado-c1v2ctl-")
    results = []

    def record(name, expect, line, ok):
        print("control=%s expected=%s observed=%s ok=%d" % (
            name, expect, line, ok))
        results.append(ok)

    ref_path = os.path.join(tmp, "ref.py")
    open(ref_path, "w").write(ref)
    rc, line = score(ref_path)
    record("REF-reachability", "TARGET_MET", line,
           rc == 0 and "TARGET_MET" in line)
    base = subprocess.run(["git", "-C", LANE, "show",
                           "9fc511ddce708327377161202f358ce37dc266ba:"
                           "tools/mado-options.py"],
                          capture_output=True, text=True, env=ENV).stdout
    base_path = os.path.join(tmp, "base.py")
    open(base_path, "w").write(base)
    rc, line = score(base_path)
    record("BASE-tool", "fixtures=0/16 MISSED", line,
           rc == 1 and fixtures_of(line) == 0)
    for name in sorted(os.listdir(CHEATS)):
        if not name.endswith(".py"):
            continue
        rc, line = score(os.path.join(CHEATS, name))
        record("CHEAT-" + name, "not TARGET_MET", line,
               "TARGET_MET" not in line and rc != 0)
    for name, old, new in EDITS:
        if ref.count(old) < 1:
            record(name, "mutation target present", "TARGET-ABSENT", False)
            continue
        path = os.path.join(tmp, name + ".py")
        open(path, "w").write(ref.replace(old, new, 1))
        rc, line = score(path)
        record(name, "not TARGET_MET", line,
               "TARGET_MET" not in line and rc != 0)
    n = len(results)
    print("CTL_C1V2: controls=%d correct=%d/%d" % (n, sum(results), n))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
