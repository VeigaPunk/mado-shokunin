#!/usr/bin/env python3
"""mado — PRED-C2-r78-v1: execute the read-only probe runbook with shape-bound rows.

The frozen case set binds each case to the SKILL.md table row that documents it
(`skill_anchor`, checked against the committed SKILL.md at --rev) and to the command plus the
outcome that row states. A case is correct only when

  * its live output matches (a probe that did not run or failed did not produce the outcome),
  * every committed churn sample still matches (a plausible next-day output: a new workspace
    id, a recycled pid, another refresh rate, a changed bind count), and
  * every committed negative sample does not match (the rule can fail).

The churn and negative samples are fixtures, not observations. The held r77 rule — a row
bound to one fixed captured value — is scored on the same cases as the do-nothing control:
it keeps the stable exact rows and loses every volatile one.

Counting command (round 78):
  python3 -I quality/counters/c2-r78-runbook.py --repo . --rev REV \
      --controls .ufo/waves/round-78/controls/c2-runbook-cases-r78.json \
      --scratch-root DIR

Contract: MADO_R78_RUNBOOK: cases=17 executed=17 matched=17 shapes=12/12 anchors=17/17
control=5/17 mutants=5 killed=5 verdict=TARGET_MET rev=<hash>  (rc 0 iff every clause holds).

Exit map: 0 target met · 1 target missed · 2 setup error (never a verdict).
The commands are frozen in the committed control set and reviewed at freeze; every one is a
read verb. Nothing is written outside the caller's scratch root.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CASES = 17
SHAPES = 12
MUTANTS = 5

MUTATIONS = [
    ("rc-blind",
     "    if rc != 0:\n        return False\n    text = stdout.rstrip",
     "    if False:\n        return False\n    text = stdout.rstrip"),
    ("int-range-lower-open",
     "    return lo <= number <= hi",
     "    return number <= hi"),
    ("json-required-ignored",
     '    for key, kind in schema.get("fields", {}).items():',
     "    for key, kind in ():"),
    ("sorted-unique-dropped",
     "    if parts != sorted(set(parts)):",
     "    if not parts:"),
    ("empty-accepted",
     '    if kind == "empty":\n        return text == ""',
     '    if kind == "empty":\n        return True'),
]

EXACT_KINDS = ("exact", "contains", "empty")


class Setup(Exception):
    pass


def session_env():
    """The caller's environment, completed with the two values a session shell exports."""
    env = dict(os.environ)
    env["LC_ALL"] = "C"
    env["LANG"] = "C"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    runtime = env.get("XDG_RUNTIME_DIR") or ("/run/user/%d" % os.getuid())
    if os.path.isdir(runtime):
        env.setdefault("XDG_RUNTIME_DIR", runtime)
    if "HYPRLAND_INSTANCE_SIGNATURE" not in env:
        base = os.path.join(env.get("XDG_RUNTIME_DIR", ""), "hypr")
        try:
            for name in sorted(os.listdir(base)):
                if os.path.exists(os.path.join(base, name, ".socket.sock")):
                    env["HYPRLAND_INSTANCE_SIGNATURE"] = name
                    break
        except OSError:
            pass
    if "OMARCHY_PATH" not in env:
        candidates = [os.path.expanduser("~/.local/share/omarchy/bin")]
        candidates += [d for d in env.get("PATH", "").split(":") if d]
        for directory in candidates:
            binary = os.path.join(directory, "omarchy")
            if os.path.isfile(binary) and os.access(binary, os.X_OK):
                env["OMARCHY_PATH"] = os.path.dirname(directory)
                break
    parts = [d for d in env.get("PATH", "").split(":") if d]
    for directory in ("/usr/local/bin", "/usr/bin", "/bin",
                      os.path.expanduser("~/.local/bin"),
                      os.path.expanduser("~/.local/share/omarchy/bin")):
        if directory not in parts:
            parts.append(directory)
    env["PATH"] = ":".join(parts)
    return env


def run(argv, timeout=30):
    env = session_env()
    try:
        proc = subprocess.run(argv, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.DEVNULL, timeout=timeout)
        return (proc.returncode, proc.stdout.decode("utf-8", "replace"),
                proc.stderr.decode("utf-8", "replace"))
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except OSError as exc:
        raise Setup("cannot run %r: %s" % (argv, exc))


def type_ok(value, kind):
    if kind == "str":
        return isinstance(value, str) and value != ""
    if kind == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "positive_int":
        return isinstance(value, int) and not isinstance(value, bool) and value > 0
    if kind == "nonneg_int":
        return isinstance(value, int) and not isinstance(value, bool) and value >= 0
    if kind == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if kind == "int4":
        return (isinstance(value, list) and len(value) == 4
                and all(isinstance(v, int) and not isinstance(v, bool) and v >= 0
                        for v in value))
    raise Setup("unknown field type %r" % (kind,))


def fields_ok(item, schema):
    if not isinstance(item, dict):
        return False
    for key, kind in schema.get("fields", {}).items():
        if key not in item or not type_ok(item[key], kind):
            return False
    return True


def json_text(text):
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return None


def matches(kind, value, rc, stdout):
    """The r78 rule: a row's declared outcome, shape-bound where the value is volatile."""
    if rc != 0:
        return False
    text = stdout.rstrip("\n")
    if kind == "exact":
        return text == value
    if kind == "contains":
        return value in stdout
    if kind == "regex":
        return re.search(value, text) is not None
    if kind == "empty":
        return text == ""
    if kind == "int_range":
        lo, hi = value
        if not re.fullmatch(r"-?[0-9]+", text.strip()):
            return False
        number = int(text)
        return lo <= number <= hi
    if kind == "sorted_unique":
        parts = text.split(",") if text else []
        if not parts or any(part == "" for part in parts):
            return False
        if parts != sorted(set(parts)):
            return False
        return set(value.get("must_include", [])) <= set(parts)
    if kind == "json_object_fields":
        data = json_text(text)
        return fields_ok(data, value)
    if kind == "array_fields":
        data = json_text(text)
        if not isinstance(data, list) or len(data) < value.get("min_items", 1):
            return False
        return all(fields_ok(item, value) for item in data)
    if kind == "int4":
        return type_ok(json_text(text), "int4")
    if kind == "levels_dump":
        data = json_text(text)
        if not isinstance(data, dict) or not data:
            return False
        for monitor in data.values():
            if not isinstance(monitor, dict):
                return False
            levels = monitor.get("levels")
            if not isinstance(levels, dict) or set(levels) != {"0", "1", "2", "3"}:
                return False
            if not all(isinstance(entry, list) for entry in levels.values()):
                return False
        return True
    raise Setup("unknown expectation kind %r" % kind)


def held_matches(frozen, rc, stdout):
    """The held r77 rule: the row's outcome equals one fixed captured value."""
    return rc == 0 and stdout.rstrip("\n") == frozen


def case_correct(case, rule, rc, stdout):
    def okay(r, out):
        return rule(case, r, out)

    if not okay(rc, stdout):
        return False
    for sample in case.get("samples", []):
        if not okay(sample["rc"], sample["out"]):
            return False
    for sample in case.get("negatives", []):
        if okay(sample["rc"], sample["out"]):
            return False
    return True


def shape_rule(case, rc, stdout):
    return matches(case["kind"], case["value"], rc, stdout)


def held_rule(case, rc, stdout):
    return held_matches(case["frozen"], rc, stdout)


def observed(rc, stdout):
    text = stdout.rstrip("\n")
    if len(text) > 100:
        text = text[:97] + "..."
    return "rc=%d out=%r" % (rc, text)


def git_show(repo, rev, path):
    proc = subprocess.run(["git", "-C", repo, "show", rev + ":" + path],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise Setup("cannot read %s at %s: %s"
                    % (path, rev, proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout.decode("utf-8", "replace")


def selftest():
    checks = total = 0

    def ok(cond, label):
        nonlocal checks, total
        total += 1
        if cond:
            checks += 1
        else:
            print("MADO_R78_RUNBOOK_SELFTEST_FAIL: %s" % label)

    ok(matches("exact", "x", 0, "x\n"), "exact")
    ok(not matches("exact", "x", 0, "y\n"), "exact refuses")
    ok(not matches("exact", "x", 1, "x\n"), "exact refuses a failed command")
    ok(matches("contains", "Hyprland", 0, "Hyprland 0.56.2\n"), "contains")
    ok(matches("regex", r"^[0-9]+$", 0, "1720\n"), "regex")
    ok(not matches("regex", r"^[0-9]+$", 0, "1720x\n"), "regex refuses")
    ok(matches("empty", None, 0, ""), "empty")
    ok(not matches("empty", None, 0, "x"), "empty refuses")
    ok(matches("int_range", [1, 10], 0, "5\n"), "int range")
    ok(not matches("int_range", [1, 10], 0, "0\n"), "int range lower")
    ok(not matches("int_range", [1, 10], 0, "11\n"), "int range upper")
    ok(not matches("int_range", [0, 10], 0, "ten\n"), "int range non-numeric")
    ok(matches("sorted_unique", {"must_include": ["waybar"]}, 0, "wallpaper,waybar\n"),
       "sorted unique")
    ok(not matches("sorted_unique", {"must_include": ["waybar"]}, 0, "waybar,wallpaper\n"),
       "sorted unique order")
    ok(not matches("sorted_unique", {"must_include": ["waybar"]}, 0, "waybar,waybar\n"),
       "sorted unique duplicates")
    ok(not matches("sorted_unique", {"must_include": ["waybar"]}, 0, "wallpaper\n"),
       "sorted unique required")
    ok(matches("json_object_fields", {"fields": {"id": "int", "name": "str"}}, 0,
               '{"id":1,"name":"1"}\n'), "object fields")
    ok(not matches("json_object_fields", {"fields": {"id": "int", "name": "str"}}, 0,
                   '{"id":1}\n'), "object fields missing")
    ok(not matches("json_object_fields", {"fields": {"id": "int"}}, 0, "[]\n"),
       "object wrong type")
    ok(matches("array_fields", {"min_items": 1,
                                "fields": {"name": "str", "reserved": "int4",
                                           "scale": "number"}}, 0,
               '[{"name":"M","reserved":[0,1,0,0],"scale":1.0}]\n'), "array fields")
    ok(not matches("array_fields", {"min_items": 1,
                                    "fields": {"name": "str", "reserved": "int4"}}, 0,
                   '[{"name":"M","reserved":[0,1,0]}]\n'), "array fields int4")
    ok(not matches("int4", None, 0, "[0,26,0,0,0]\n"), "int4 length")
    ok(matches("levels_dump", None, 0,
               '{"M": {"levels": {"0": [], "1": [], "2": [], "3": []}}}\n'), "levels dump")
    ok(not matches("levels_dump", None, 0, '{"M": {"levels": {"0": []}}}\n'),
       "levels dump missing levels")
    ok(not matches("levels_dump", None, 0, "[]\n"), "levels dump wrong type")
    try:
        matches("nope", None, 0, "", )
        ok(False, "unknown kind refused")
    except Setup:
        ok(True, "unknown kind refused")
    sample = {"kind": "int_range", "value": [1, 10], "frozen": "5",
              "samples": [{"rc": 0, "out": "7"}],
              "negatives": [{"rc": 0, "out": "0"}]}
    ok(case_correct(sample, shape_rule, 0, "5"), "case shape correct")
    ok(not case_correct(sample, held_rule, 0, "5"), "case held churn refused")
    ok(case_correct(sample, shape_rule, 0, "9"), "case live variant correct")
    for name, anchor, repl in MUTATIONS:
        source = "a\n" + anchor + "\nb\n"
        if source.count(anchor) != 1 or source.replace(anchor, repl) == source:
            ok(False, "mutation anchor %s" % name)
        else:
            ok(True, "mutation anchor %s" % name)
    print("MADO_R78_RUNBOOK_SELFTEST: %d/%d" % (checks, total))
    return 0 if checks == total else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--controls")
    ap.add_argument("--scratch-root")
    ap.add_argument("--no-mutants", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.repo and args.rev and args.controls and args.scratch_root):
        print("MADO_R78_RUNBOOK: ERROR (stage=setup usage)")
        return 2
    workroot = None
    try:
        repo = os.path.abspath(args.repo)
        if args.scratch_root == "/":
            raise Setup("refusing / as the scratch root")
        if os.path.islink(args.scratch_root):
            raise Setup("refusing a symlinked scratch root")
        os.makedirs(args.scratch_root, exist_ok=True)
        if not os.path.isdir(args.scratch_root):
            raise Setup("scratch root is not a directory")
        workroot = tempfile.mkdtemp(prefix="c2-r78-", dir=args.scratch_root)
        proc = subprocess.run(["git", "-C", repo, "rev-parse", args.rev],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        rev_full = proc.stdout.decode().strip()
        if proc.returncode != 0 or not rev_full:
            raise Setup("cannot resolve --rev %r" % args.rev)
        skill = git_show(repo, args.rev, "SKILL.md")
        with open(args.controls) as fh:
            control = json.load(fh)
        cases = control["cases"]
        if len(cases) != CASES:
            raise Setup("control set carries %d cases, frozen target expects %d"
                        % (len(cases), CASES))
        shape_cases = [c for c in cases if c["kind"] not in EXACT_KINDS]
        if len(shape_cases) != SHAPES:
            raise Setup("control set carries %d shape cases, frozen target expects %d"
                        % (len(shape_cases), SHAPES))
        defects = []
        for case in cases:
            if case["skill_anchor"] not in skill:
                defects.append("anchor %r for %s not in SKILL.md at %s"
                               % (case["skill_anchor"], case["name"], rev_full[:12]))
        if defects:
            raise Setup("; ".join(defects))

        executed = matched = anchors = shapes = held = 0
        for case in cases:
            rc, stdout, stderr = run(case["argv"])
            executed += 1
            good = case_correct(case, shape_rule, rc, stdout)
            matched += 1 if good else 0
            held += 1 if case_correct(case, held_rule, rc, stdout) else 0
            anchors += 1 if case["skill_anchor"] in skill else 0
            shapes += 1 if case["kind"] not in EXACT_KINDS and good else 0
            print("MADO_R78_PROBE: name=%s row=%s kind=%s match=%s %s"
                  % (case["name"], case["skill_anchor"], case["kind"],
                     "yes" if good else "no", observed(rc, stdout)))

        killed = 0
        if not args.no_mutants:
            self_path = os.path.abspath(__file__)
            with open(self_path) as fh:
                own_source = fh.read()
            for name, anchor, repl in MUTATIONS:
                if own_source.count(anchor) != 1:
                    raise Setup("mutant %s anchor occurs %d times, not once"
                                % (name, own_source.count(anchor)))
                mutant = os.path.join(workroot, "mutant-%s.py" % name)
                with open(mutant, "w") as fh:
                    fh.write(own_source.replace(anchor, repl))
                mrc, mout, merr = run([sys.executable, "-I", mutant, "--repo", repo,
                                       "--rev", args.rev, "--controls", args.controls,
                                       "--scratch-root", workroot, "--no-mutants"],
                                      timeout=300)
                mm = re.search(r"MADO_R78_RUNBOOK: cases=(\d+) executed=(\d+) matched=(\d+)",
                               mout)
                mmatched = int(mm.group(3)) if mm else 0
                dead = mrc != 0 and (mm is None or mmatched < CASES)
                killed += 1 if dead else 0
                print("MADO_R78_MUTANT: name=%s matched=%d/%d killed=%s"
                      % (name, mmatched, CASES, "yes" if dead else "no"))

        control_total = held
        print("MADO_R78_CONTROL: held-correct=%d/%d rule=fixed-value(held-r77-row-binding)"
              % (control_total, CASES))
        target = (executed == CASES and matched == CASES and shapes == SHAPES
                  and anchors == CASES and control_total < CASES
                  and (args.no_mutants or killed == MUTANTS))
        print("MADO_R78_RUNBOOK: cases=%d executed=%d matched=%d shapes=%d/%d anchors=%d/%d "
              "control=%d/%d mutants=%s killed=%s verdict=%s rev=%s"
              % (CASES, executed, matched, shapes, SHAPES, anchors, CASES,
                 control_total, CASES, "0" if args.no_mutants else str(MUTANTS),
                 "0" if args.no_mutants else str(killed),
                 "TARGET_MET" if target else "TARGET_MISSED", rev_full))
        return 0 if target else 1
    except Setup as exc:
        print("MADO_R78_RUNBOOK: ERROR (stage=setup %s)" % exc)
        return 2
    finally:
        if workroot:
            shutil.rmtree(workroot, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
