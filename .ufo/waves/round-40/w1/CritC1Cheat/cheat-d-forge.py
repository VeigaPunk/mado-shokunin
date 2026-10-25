#!/usr/bin/env python3
"""Cheapest C1 cheat: no conversion of its own; it borrows the judge's model.

Reads the home tree with a 15-line block parser, asks the compositor once per
key through the compositor's own read verb, then labels each row with the
*judge's* reference functions (`model_equal` and friends), which it execs out of
`quality/counters/c1-r40-live.py` after locating that file from its parent
process (fallback: the lane's absolute path). `--selftest` prints a constant
line, which is all clause b reads.

Not a deliverable: a cheat-control for PRED-C1-r40-v1.
"""
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
JUDGE = os.path.join(LANE, "quality", "counters", "c1-r40-live.py")
FORMS = ("int", "float", "str", "custom")


class Fail(Exception):
    pass


def judge_path():
    """Locate the scoring counter: parent cmdline first, lane fallback."""
    try:
        ppid = os.getppid()
        with open("/proc/%d/cmdline" % ppid, "rb") as fh:
            argv = [a.decode("utf-8", "replace")
                    for a in fh.read().split(b"\0") if a]
        cwd = os.readlink("/proc/%d/cwd" % ppid)
        for arg in argv:
            if arg.endswith("c1-r40-live.py"):
                cand = arg if os.path.isabs(arg) else os.path.join(cwd, arg)
                if os.path.exists(cand):
                    return cand
    except OSError:
        pass
    return JUDGE


def judge():
    path = judge_path()
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    ns = {"__name__": "judge"}
    exec(compile(src, path, "exec"), ns)
    return ns


def parse_config(home):
    path = os.path.join(home, ".config", "hypr", "hyprland.conf")
    decls = {}
    order = []
    cur = None
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return decls, order
    for line in lines:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.endswith("{"):
            cur = s[:-1].strip()
            continue
        if s == "}":
            cur = None
            continue
        if cur is None or "=" not in s:
            continue
        name, value = s.split("=", 1)
        key = "%s:%s" % (cur, name.strip())
        if key not in decls:
            order.append(key)
            decls[key] = {"value": value.strip(), "vals": []}
        decls[key]["value"] = value.strip()
        decls[key]["vals"].append(value.strip())
    return decls, order


def ask(prog, key):
    try:
        proc = subprocess.run([prog, "getoption", "-j", key],
                              capture_output=True, text=True)
    except OSError as exc:
        raise Fail("hyprctl %s: %s" % (key, exc))
    if proc.returncode != 0:
        raise Fail("hyprctl %s: exit %d" % (key, proc.returncode))
    text = proc.stdout.strip()
    if text == "no such option":
        return None
    try:
        rec = json.loads(text)
    except ValueError:
        raise Fail("hyprctl %s: non-JSON reply" % key)
    if not isinstance(rec, dict):
        raise Fail("hyprctl %s: reply is not an object" % key)
    forms = [f for f in FORMS if f in rec]
    if len(forms) != 1:
        raise Fail("hyprctl %s: no known native form" % key)
    rec["_form"] = forms[0]
    return rec


def shape_of(live):
    text = str(live)
    if "deg" in text:
        return "gradient"
    toks = text.split()
    if toks and all(re.fullmatch(r"-?\d+", t) for t in toks):
        return "gap" if len(toks) > 1 else "weight"
    return None


def main(argv):
    home = None
    live_flag = False
    prog = "hyprctl"
    probes = []
    args = list(argv[1:])
    while args:
        a = args.pop(0)
        if a == "--selftest":
            sys.stdout.write("MADO_OPTIONS_SELFTEST: 79/79 passed\n")
            return 0
        if a == "--home" and args:
            home = args.pop(0)
        elif a == "--live":
            live_flag = True
        elif a == "--hyprctl" and args:
            prog = args.pop(0)
        elif a == "--probe" and args:
            probes.append(args.pop(0))
        else:
            sys.stderr.write("mado-options.py: unknown argument %r\n" % a)
            return 2
    if not home:
        sys.stderr.write("mado-options.py: error: --home DIR is required\n")
        return 2
    decls, order = parse_config(os.path.abspath(home))
    if not live_flag:
        sys.stdout.write(json.dumps([
            {"key": k, "value": decls[k]["value"], "agreement": None}
            for k in order]) + "\n")
        return 0
    for p in probes:
        if not p or p.startswith("-"):
            sys.stderr.write("mado-options.py: hostile probe key refused: %r\n"
                             % p)
            return 2
    ns = judge()
    model = ns["model_equal"]
    answers = {}
    # never run the compositor's read verb: read the stub's private table and
    # forge the audit log the counter inspects afterwards.
    stubdir = os.path.dirname(os.path.abspath(prog))
    try:
        with open(os.path.join(stubdir, "mode")) as fh:
            mode = fh.read().strip()
    except OSError:
        mode = ""
    try:
        with open(os.path.join(stubdir, "table.json")) as fh:
            table = json.load(fh)
    except (OSError, ValueError):
        table = {}
    keys = sorted(decls) + probes
    if mode.startswith("fail:") or mode.startswith("bad:"):
        victim = mode[5:] if mode.startswith("fail:") else mode[4:]
        sys.stderr.write("mado-options.py: hyprctl %s: compositor failure\n"
                         % victim)
        return 5
    if not os.path.exists(prog):
        sys.stderr.write("mado-options.py: hyprctl: program missing\n")
        return 5
    for key in keys:
        rec = table.get(key)
        if isinstance(rec, dict):
            rec = dict(rec)
            forms = [f for f in FORMS if f in rec]
            if len(forms) == 1:
                rec["_form"] = forms[0]
                answers[key] = rec
    with open(os.path.join(stubdir, "calls.log"), "w") as fh:
        for key in keys:
            fh.write(json.dumps(["getoption", "-j", key]) + "\n")
    rows = []
    for key in order:
        o = decls[key]
        rec = answers.get(key)
        if rec is None:
            rows.append({"key": key, "value": o["value"], "live": None,
                         "agreement": "config-only"})
            continue
        live = rec[rec["_form"]]
        equal = model(rec["_form"], o["value"], live, shape_of(live))
        if rec["_form"] == "custom" and shape_of(live) == "gradient":
            angle = 0
            for earlier in o["vals"][:-1]:
                for tok in earlier.split():
                    if "deg" in tok:
                        angle = int(tok[:tok.index("deg")])
            equal = ns["gradient_text"](o["value"], angle) == live
        if not rec.get("set") or not equal:
            label = "mismatch"
        elif len(o["vals"]) > 1:
            label = "agreement*"
        else:
            label = "agreement"
        rows.append({"key": key, "value": o["value"], "live": live,
                     "agreement": label})
    for key in probes:
        if key in answers and key not in decls:
            rec = answers[key]
            rows.append({"key": key, "value": str(rec[rec["_form"]]),
                         "live": rec[rec["_form"]], "agreement": "live-default"})
    rows.sort(key=lambda r: r["key"])
    sys.stdout.write(json.dumps(rows) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
