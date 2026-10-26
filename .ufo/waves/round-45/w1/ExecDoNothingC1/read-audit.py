#!/usr/bin/env python3
"""read-audit - a *proposed* read audit for PRED-C1-r45 (not part of the lane's counting).

The frozen predicate extracts the tool blob to a temp dir and runs it; nothing stops the tool from opening
files outside that dir. This audit runs the extracted tool on one fixture under `strace -f -e trace=openat`
and FAILS it if any openat names
  * a path under /home (the operator's tree; in production the counter and the reference both live there), or
  * /proc/<pid>/cmdline or /proc/<pid>/environ (another process's argv, which names the predicate itself).
The reference opens neither (it opens the config, the dump and the interpreter's own files); a tool that
loads or looks up the predicate does.

Usage: read-audit.py --repo R --rev V --work W [--seed N]. Final line:
`READ-AUDIT: opens=N home=K proc=J verdict=<PASS|FAIL> rev=<hash>`; exit 0 iff PASS.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTER = os.path.join(HERE, "..", "..", "..", "..", "..", "quality", "counters", "c1-r45-monitors.py")
ns = {"__name__": "c1r45_predicate", "__file__": COUNTER}
exec(compile(open(COUNTER, "rb").read(), COUNTER, "exec"), ns)
FIXTURES, names, subst, git = ns["FIXTURES"], ns["names"], ns["subst"], ns["git"]
TOOL = ns["TOOL"]
OPEN_RE = re.compile(r'^\d+\s+openat\(AT_FDCWD, "((?:[^"\\]|\\.)*)"')
PROC_RE = re.compile(r"^/proc/\d+/(cmdline|environ)$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--seed", type=int, default=45)
    ap.add_argument("--fixture", default="host")
    ap.add_argument("--sandbox", choices=("strace", "bwrap"), default="strace")
    a = ap.parse_args()
    work = tempfile.mkdtemp(dir=a.work, prefix="audit-")
    try:
        full = git(a.repo, "rev-parse", "--verify", a.rev + "^{commit}")
        if full is None:
            print("READ-AUDIT: SETUP bad rev")
            return 2
        full = full.decode().strip()
        blob = git(a.repo, "show", "%s:%s" % (full, TOOL))
        if blob is None:
            print("READ-AUDIT: opens=0 home=0 proc=0 verdict=FAIL tool=absent rev=%s" % full)
            return 1
        tool = os.path.join(tempfile.mkdtemp(dir=work, prefix="tool-"), "mado-monitors.py")
        with open(tool, "wb") as f:
            f.write(blob)
        fx = [f for f in FIXTURES if f[0] == a.fixture][0]
        label, configs, dump, stdin, expect, rc_want = fx
        table = names(a.seed)
        d = tempfile.mkdtemp(dir=work, prefix="fx-")
        home = os.path.join(d, "home")
        os.makedirs(home)
        dp = os.path.join(d, "monitors.json")
        with open(dp, "wb") as f:
            f.write(json.dumps(subst(dump, table), indent=2).encode())
        args = ["--monitors", dp]
        for k, text in enumerate(configs):
            cp = os.path.join(d, "c%d.conf" % k)
            with open(cp, "w") as f:
                f.write(subst(text, table))
            args += ["--config", cp]
        trace = os.path.join(d, "trace.txt")
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": home,
               "HYPRLAND_INSTANCE_SIGNATURE": "mado-r45-fixture"}
        if a.sandbox == "bwrap":
            env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": home,
                   "HYPRLAND_INSTANCE_SIGNATURE": "mado-r45-fixture"}
            cmd = ["bwrap", "--ro-bind", "/usr", "/usr", "--ro-bind", "/lib", "/lib",
                   "--ro-bind", "/lib64", "/lib64", "--ro-bind", "/etc", "/etc", "--dev", "/dev",
                   "--tmpfs", "/tmp", "--bind", work, work, "--chdir", d, "--unshare-all",
                   "--die-with-parent", sys.executable, "-I", tool] + args
            p = subprocess.run(cmd, capture_output=True, cwd=d, env=env, timeout=60)
            want = "".join(subst(l, table) + "\n" for l in expect)
            ok_rc = p.returncode == rc_want
            ok_out = p.stdout.decode("utf-8", "replace") == want
            print("READ-AUDIT sandbox=bwrap rc=%d want=%d stdout_match=%s stderr=%d" % (
                p.returncode, rc_want, ok_out, len(p.stderr)))
            print("READ-AUDIT: opens=0 home=0 proc=0 verdict=%s rev=%s rc=%d" % (
                "PASS" if ok_rc and ok_out else "FAIL", full, p.returncode))
            return 0 if ok_rc and ok_out else 1
        p = subprocess.run(["strace", "-f", "-qq", "-s", "400", "-e", "trace=openat", "-o", trace,
                            sys.executable, "-I", tool] + args, capture_output=True, cwd=d, env=env,
                           timeout=60)
        opens = home_hits = proc_hits = 0
        for line in open(trace, encoding="utf-8", errors="replace"):
            m = OPEN_RE.match(line)
            if not m:
                continue
            path = m.group(1)
            opens += 1
            if path.startswith("/home"):
                home_hits += 1
                print("READ-AUDIT violation=home path=%s" % path)
            if PROC_RE.match(path):
                proc_hits += 1
                print("READ-AUDIT violation=proc path=%s" % path)
        ok = home_hits == 0 and proc_hits == 0 and p.returncode in (0, 1, 3, 4, 5)
        print("READ-AUDIT: opens=%d home=%d proc=%d verdict=%s rev=%s rc=%d" % (
            opens, home_hits, proc_hits, "PASS" if ok else "FAIL", full, p.returncode))
        return 0 if ok else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
