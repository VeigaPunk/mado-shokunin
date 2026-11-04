#!/usr/bin/env python3
"""mado — PRED-C2-r77-v1: execute the read-only probe table end-to-end.

The frozen case set binds each case to the SKILL.md table row that documents it
(`skill_anchor`, checked against the committed SKILL.md at --rev) and to the
command plus the outcome that row states. This counter runs every command in the
caller's session environment (the table is a session-shell runbook: `hyprctl`
needs HYPRLAND_INSTANCE_SIGNATURE and `omarchy` needs its own path variable; the
counter prints only each probe's stdout, never the environment), compares the
observed outcome, and reports execution separately from matching: a table row
that is only read is not a probe.

Counting command (round 77):
  python3 -I quality/counters/c2-r77-runbook.py --repo . --rev REV \
      --controls .ufo/waves/round-77/controls/c2-runbook-cases-r77.json

Contract: MADO_R77_RUNBOOK: cases=12 executed=12 matched=12 unexecuted=0
anchors=12/12 verdict=TARGET_MET rev=<hash>  (rc 0 iff every clause holds).

Exit map: 0 target met · 1 target missed · 2 setup error (never a verdict).
The commands are frozen in the committed control set and reviewed at freeze; every
one is a read verb. Nothing is written.
"""

import argparse
import json
import os
import re
import subprocess
import sys

CASES = 12


class Setup(Exception):
    pass


def session_env():
    """The caller's environment, completed with the two values a session shell exports.

    The table is a session-shell runbook. A non-interactive caller (a closure runner, a
    scheduler) may lack HYPRLAND_INSTANCE_SIGNATURE or OMARCHY_PATH; both are discoverable
    read-only from the runtime directory and the binary's own location. Nothing is guessed:
    the instance is the runtime directory that owns a .socket.sock, and OMARCHY_PATH is the
    checkout that owns the omarchy binary.
    """
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
        return proc.returncode, proc.stdout.decode("utf-8", "replace"), proc.stderr.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except OSError as exc:
        raise Setup("cannot run %r: %s" % (argv, exc))


def matched(case, rc, stdout, stderr):
    if rc != 0:
        return False  # a probe that failed did not produce the stated outcome
    kind = case["kind"]
    text = stdout.rstrip("\n")
    if kind == "exact":
        return text == case["value"]
    if kind == "contains":
        return case["value"] in stdout
    if kind == "regex":
        return re.search(case["value"], text) is not None
    if kind == "empty":
        return text == ""
    raise Setup("unknown expectation kind %r" % kind)


def observed(case, rc, stdout, stderr):
    text = stdout.rstrip("\n")
    if len(text) > 120:
        text = text[:117] + "..."
    return "rc=%d out=%r" % (rc, text)


def git_show(repo, rev, path):
    proc = subprocess.run(["git", "-C", repo, "show", rev + ":" + path],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise Setup("cannot read %s at %s: %s" % (path, rev, proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout.decode("utf-8", "replace")


def selftest():
    checks = total = 0

    def ok(cond, label):
        nonlocal checks, total
        total += 1
        if cond:
            checks += 1
        else:
            print("MADO_R77_RUNBOOK_SELFTEST_FAIL: %s" % label)

    ok(matched({"kind": "exact", "value": "x"}, 0, "x\n", ""), "exact")
    ok(not matched({"kind": "exact", "value": "x"}, 0, "y\n", ""), "exact refuses")
    ok(matched({"kind": "contains", "value": "Hyprland"}, 0, "Hyprland 0.56.2\n", ""), "contains")
    ok(matched({"kind": "regex", "value": "^[0-9]+$"}, 0, "1720\n", ""), "regex")
    ok(not matched({"kind": "regex", "value": "^[0-9]+$"}, 0, "1720x\n", ""), "regex refuses")
    ok(matched({"kind": "empty"}, 0, "", ""), "empty")
    ok(not matched({"kind": "empty"}, 0, "x", ""), "empty refuses")
    try:
        matched({"kind": "nope", "value": "x"}, 0, "", "")
        ok(False, "unknown kind refused")
    except Setup:
        ok(True, "unknown kind refused")
    ok(observed({"kind": "exact", "value": "x"}, 0, "x\n", "").startswith("rc=0 out='x'"), "observed")
    print("MADO_R77_RUNBOOK_SELFTEST: %d/%d" % (checks, total))
    return 0 if checks == total else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--controls")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.repo and args.rev and args.controls):
        print("MADO_R77_RUNBOOK: ERROR (stage=setup usage)")
        return 2
    try:
        proc = subprocess.run(["git", "-C", args.repo, "rev-parse", args.rev], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        rev_full = proc.stdout.decode().strip()
        if proc.returncode != 0 or not rev_full:
            raise Setup("cannot resolve --rev %r" % args.rev)
        skill = git_show(args.repo, args.rev, "SKILL.md")
        with open(args.controls) as fh:
            control = json.load(fh)
        cases = control["cases"]
        if len(cases) != CASES:
            raise Setup("control set carries %d cases, frozen target expects %d" % (len(cases), CASES))
        expected_anchors = {c["name"]: c["skill_anchor"] for c in cases}
        defects = []
        for name, anchor in expected_anchors.items():
            if anchor not in skill:
                defects.append("anchor %r for %s not in SKILL.md at %s" % (anchor, name, rev_full[:12]))
        if defects:
            raise Setup("; ".join(defects))

        executed = matched_rows = anchors = 0
        for case in cases:
            try:
                rc, stdout, stderr = run(case["argv"])
            except Setup:
                raise
            executed += 1
            good = matched(case, rc, stdout, stderr)
            matched_rows += 1 if good else 0
            anchors += 1 if case["skill_anchor"] in skill else 0
            print("MADO_R77_PROBE: name=%s row=%s match=%s %s"
                  % (case["name"], case["skill_anchor"], "yes" if good else "no",
                     observed(case, rc, stdout, stderr)))
        read_only = sum(1 for c in cases if c["skill_anchor"] in skill)
        print("MADO_R77_BASE: executed=0 matched_by_read=%d/%d rule=read-the-table"
              % (read_only, CASES))
        target = executed == CASES and matched_rows == CASES and read_only == CASES
        print("MADO_R77_RUNBOOK: cases=%d executed=%d matched=%d unexecuted=%d anchors=%d/%d "
              "verdict=%s rev=%s"
              % (CASES, executed, matched_rows, CASES - executed, anchors, CASES,
                 "TARGET_MET" if target else "TARGET_MISSED", rev_full))
        return 0 if target else 1
    except Setup as exc:
        print("MADO_R77_RUNBOOK: ERROR (stage=setup %s)" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
