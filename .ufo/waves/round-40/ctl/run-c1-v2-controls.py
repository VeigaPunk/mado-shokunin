#!/usr/bin/env python3
"""Round-40 C1 v2 controls: PRED-C1-r40-v2 scored over cheats and mutants.

Controls (each scored with the frozen v2 counter's `--tool`, at a fixed nonce
so the receipt is reproducible; the pass criterion does not depend on the nonce):

  REF      the reference tool (c1/ctl-ref-tool-v2.py.txt): must score
           TARGET_MET (the target is reachable by an honest implementation);
  BASE     the unmodified base tool: fixtures=0/19, never MET;
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
import shutil
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
    ("M04-angle-ignored", '" %ddeg" % angle', '" %ddeg" % 0'),
    ("M05-gap3-wrong",
     'sides = [sides[0], sides[1], sides[2], sides[1]]',
     'sides = [sides[0], sides[1], sides[2], sides[0]]'),
    ("M06-config-only-as-mismatch",
     'row["agreement"] = "config-only"\n            row["live"] = None',
     'row["agreement"] = "mismatch"\n            row["live"] = None'),
    ("M07-extra-request",
     '    try:\n        proc = subprocess.Popen([hyprctl, "getoption", "-j", key],',
     '    subprocess.run([hyprctl, "version"], capture_output=True)\n'
     '    try:\n        proc = subprocess.Popen([hyprctl, "getoption", "-j", key],'),
    ("M08-set-ignored", 'if not isset or not native_equal(',
     'if not native_equal('),
    ("M09-shadow-ignored",
     '        elif options[row["key"]]["_decls"] > 1:\n'
     '            row["agreement"] = "agreement*"\n        else:\n'
     '            row["agreement"] = "agreement"\n    for key in probes:',
     '        else:\n            row["agreement"] = "agreement"\n'
     '    for key in probes:'),
    ("M10-probe-allowlist-dropped",
     '        if not KEY_RE.fullmatch(key):\n            sys.stderr.write("mado-options.py: invalid probe',
     '        if False:\n            sys.stderr.write("mado-options.py: invalid probe'),
    ("M11-failure-swallowed",
     '    if proc.returncode != 0:\n        raise CtlError("%r: hyprctl %r exited %d" % (key, hyprctl,\n'
     '                                                     proc.returncode))',
     '    if proc.returncode != 0:\n        return None'),
    ("M12-writes-config-root",
     '    home = os.path.abspath(args.home)\n',
     '    home = os.path.abspath(args.home)\n'
     '    open(os.path.join(home, ".config", "hypr", "zz.tmp"), "w").write("x")\n'),
    ("M13-int-normalisation-dropped",
     '        return hl_int(text) == live\n', '        return text == str(live)\n'),
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
     'return int(math.floor(f32(f32(float(token)) * 255.0) + 0.5)) & 0xFF',
     'return int(float(token) * 255.0) & 0xFF'),
    ("M18-alpha-bankers-round",
     'return int(math.floor(f32(f32(float(token)) * 255.0) + 0.5)) & 0xFF',
     'return int(round(float(token) * 255.0)) & 0xFF'),
    ("M19-sentinel-substring",
     '    if text == "no such option":', '    if "no such option" in text:'),
    ("M20-strict-padding",
     '    text = raw.decode("utf-8", "replace").strip()\n',
     '    text = raw.decode("utf-8", "replace").strip()\n'
     '    if raw.decode() != text + "\\n":\n'
     '        raise CtlError("%r: padded reply" % key)\n'),
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
     '            "live": str(value),\n        })\n    rows.sort(key=lambda r: r["key"])',
     '            "live": str(value),\n        })'),
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
    ("M35-declared-key-allowlist-dropped",
     '                if not KEY_RE.fullmatch(row["key"]):',
     '                if False:'),
    ("M36-child-env-inherited",
     '    env = {k: os.environ[k] for k in CHILD_ENV if k in os.environ}',
     '    env = dict(os.environ, EXTRA_VAR="1")'),
    ("M37-stdin-inherited",
     '                                stdin=subprocess.DEVNULL,\n', ''),
    ("M38-reply-cap-dropped",
     'too_long = len(raw) > REPLY_CAP', 'too_long = False'),
    ("M39-set-type-unchecked",
     'if not isinstance(reply["set"], bool) or not _typed(forms[0],',
     'if False or not _typed(forms[0],'),
    ("M40-value-type-unchecked",
     'return forms[0], reply[forms[0]], reply["set"]',
     'return forms[0], reply[forms[0]], reply["set"]\n    _typed = None'),
    ("M41-writable-program-accepted",
     '    if mode & (stat.S_IWGRP | stat.S_IWOTH):',
     '    if False:'),
    ("M42-getoption-with-live-allowed",
     '    if args.live and args.getoption:', '    if False:'),
    ("M43-alpha-float64",
     'return int(math.floor(f32(f32(float(token)) * 255.0) + 0.5)) & 0xFF',
     'return int(math.floor(float(token) * 255.0 + 0.5)) & 0xFF'),
    ("M44-gradient-alpha-rounded",
     'return int(math.floor(f32(f32(float(token)) * 255.0)))',
     'return int(math.floor(f32(f32(float(token)) * 255.0) + 0.5))'),
    ("M45-gradient-tokens-via-int-parser",
     '        colour = grad_color(token)', '        colour = hl_int(token)'),
    ("M46-program-not-resolved",
     'merge_live(rows, st.options, resolve_program(args.hyprctl),',
     'merge_live(rows, st.options, args.hyprctl,'),
    ("X01-fabricated-live-payload",
     '        row["live"] = str(value)\n', '        row["live"] = "FABRICATED"\n'),
    ("X02-exec-import-socket", 'import argparse\n',
     'import argparse\nexec("import socket")\n'),
    ("X03-hardcoded-hostile-list",
     '        if not KEY_RE.fullmatch(key):\n            sys.stderr.write("mado-options.py: invalid probe',
     '        if key in ("-x", "--version", ""):\n            sys.stderr.write("mado-options.py: invalid probe'),
    ("X04-duplicate-rows",
     '            "live": str(value),\n        })\n    rows.sort(key=lambda r: r["key"])',
     '            "live": str(value),\n        })\n    rows.extend([dict(r) for r in rows])\n    rows.sort(key=lambda r: r["key"])'),
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
    jobs = []   # (name, expectation, path, predicate)

    ref_path = os.path.join(tmp, "ref.py")
    open(ref_path, "w").write(ref)
    jobs.append(("REF-reachability", "TARGET_MET", ref_path,
                 lambda rc, line: rc == 0 and "TARGET_MET" in line))
    base = subprocess.run(["git", "-C", LANE, "show",
                           "9fc511ddce708327377161202f358ce37dc266ba:"
                           "tools/mado-options.py"],
                          capture_output=True, text=True, env=ENV).stdout
    base_path = os.path.join(tmp, "base.py")
    open(base_path, "w").write(base)
    jobs.append(("BASE-tool", "fixtures=0/19 MISSED", base_path,
                 lambda rc, line: rc == 1 and fixtures_of(line) == 0))
    not_met = lambda rc, line: "TARGET_MET" not in line and rc != 0
    for name in sorted(os.listdir(CHEATS)):
        if name.endswith(".py"):
            jobs.append(("CHEAT-" + name, "not TARGET_MET",
                         os.path.join(CHEATS, name), not_met))
    absent = []
    for name, old, new in EDITS:
        if ref.count(old) < 1:
            absent.append(name)
            continue
        path = os.path.join(tmp, name + ".py")
        open(path, "w").write(ref.replace(old, new, 1))
        jobs.append((name, "not TARGET_MET", path, not_met))
    from concurrent.futures import ThreadPoolExecutor
    workers = int(os.environ.get("MADO_CTL_WORKERS", "6"))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        scored = list(pool.map(lambda j: score(j[2]), jobs))
    results = []
    for (name, expect, _, pred), (rc, line) in zip(jobs, scored):
        ok = bool(pred(rc, line))
        print("control=%s expected=%s observed=%s ok=%d" % (
            name, expect, line, ok))
        results.append(ok)
    for name in absent:
        print("control=%s mutation target present observed=TARGET-ABSENT ok=0"
              % name)
        results.append(False)
    n = len(results)
    print("CTL_C1V2: controls=%d correct=%d/%d" % (n, sum(results), n))
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
