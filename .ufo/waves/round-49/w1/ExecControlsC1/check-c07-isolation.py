#!/usr/bin/env python3
"""Isolation measurement for control c07-read-fixture-repo: the same tool file, judged twice.

Run 1 - on the host, unsandboxed, with MADO_CTL_FIXTURES pointing at this seat's cases.json and the cwd at the
repository-shaped path the control defaults to. The tool reads the fixture file and answers from it.
Run 2 - inside the replica counter's sandbox (bwrap mount set, strace tripwire): the fixture file is not bound and
--clearenv drops the variable, so the tool answers nothing.

The pair is the evidence that the isolation clause (the mount set), and not the fixture comparison, is what stops a
tool that reads the repository at run time. Every keymap is compiled at run time with the pinned compile-keymap and
the judge is the pinned how-to-type.

Usage: check-c07-isolation.py --cases cases.json --tool controls/c07-read-fixture-repo.py --work DIR
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys


def load_counter(path):
    spec = importlib.util.spec_from_file_location("replica", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=os.path.join(here, "cases.json"))
    ap.add_argument("--tool", default=os.path.join(here, "controls", "c07-read-fixture-repo.py"))
    ap.add_argument("--counter", default=os.path.join(here, "score-controls.py"))
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    if work.startswith("/tmp"):
        sys.exit("refusing a --work under /tmp")
    R = load_counter(a.counter)
    os.makedirs(os.path.join(work, "km"), exist_ok=True)
    env = R.clean_env(work)
    cases = json.load(open(a.cases, encoding="utf-8"))["cases"]

    host_ok = 0
    sandbox_ok = 0
    box = R.Box(work, False, traces=False)
    for c in cases:
        km = os.path.join(work, "km", "c07-" + c["id"] + ".keymap")
        if not os.path.exists(km):
            open(km, "wb").write(R.compile_keymap(c, work, env))
        want_rc, want_out, _ = R.judge(km, c["keysym"], env)
        argv = [sys.executable, "-I", a.tool, "how-to-type", "--keymap", km, "--disable-compose",
                "--keysym", c["keysym"]]
        p = subprocess.run(argv, capture_output=True, cwd=os.path.dirname(here),
                           env=dict(os.environ, MADO_CTL_FIXTURES=a.cases, PATH="/usr/bin"))
        host_ok += 1 if (p.returncode == want_rc and
                         p.stdout.decode("utf-8", "surrogateescape") == want_out) else 0
        rc, so, se = box.run(a.tool, km, ["how-to-type", "--keymap", "/case/keymap", "--disable-compose",
                                         "--keysym", c["keysym"]])
        sandbox_ok += 1 if (rc == want_rc and so == want_out) else 0
    n = len(cases)
    print("c07-isolation: host=%d/%d sandbox=%d/%d cases=%d" % (host_ok, n, sandbox_ok, n, n))
    print("c07-isolation: fixture_file=%s (read on host, absent in the sandbox mount set)" % a.cases)
    return 0


if __name__ == "__main__":
    sys.exit(main())
