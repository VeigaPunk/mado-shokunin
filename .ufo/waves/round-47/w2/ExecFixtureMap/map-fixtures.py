#!/usr/bin/env python3
"""ExecFixtureMap (mado round 47, wave w2, seat ExecFixtureMap).

Which script lines of xdg-terminal-exec v0.14.3 do the frozen C1 fixtures
(quality/counters/c1-r47-fixtures.json) reach?

Runs every fixture in the same sandbox the C1 counter uses (bwrap, allowlist root,
PATH=<root>/bin:/oracle/bin, XDG_CACHE_HOME=<root>/.rw/cache), but executes the
resolver copy as `/bin/sh -x SCRIPT ARGS` with PS4='+${LINENO} ' so every executed
source line prints `+<lineno> ...` on stderr. Nothing is launched: the fixtures only
carry --print-* / --test argument vectors and the sandbox has no terminal.

Writes <out>/lines.json (per-line hit counts), <out>/unreached.txt and
<out>/summary.txt. Scratch only under --work (never /tmp).

Usage: python3 -I map-fixtures.py --work DIR [--out DIR] [--variant A|B|AB]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FIXTURES = os.path.join(LANE, "quality/counters/c1-r47-fixtures.json")
FIXTURES_SHA256 = "4836cc1d9e493af7bf15fa52f6e6855fe71c5c27911880847da668e1e313dd86"
PIN = os.path.join(LANE, ".ufo/waves/round-47/fetch/xdg-terminal-exec")
PIN_SHA256 = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
EXTERNALS = ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm")
TIMEOUT = 30


def pinned(path, sha):
    blob = open(path, "rb").read()
    got = hashlib.sha256(blob).hexdigest()
    if got != sha:
        raise SystemExit("sha256 mismatch %s: %s != %s" % (path, got, sha))
    return blob


def materialize(root, case):
    os.makedirs(os.path.join(root, "home"))
    os.makedirs(os.path.join(root, ".rw", "cache"))
    for rel, text in case["files"].items():
        if ".." in rel.split("/") or rel.startswith("/"):
            raise SystemExit("unsafe path in case %s" % case.get("id"))
        p = os.path.join(root, rel)
        if rel.endswith("/"):
            os.makedirs(p, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(text.replace("$ROOT", root).encode("utf-8", "surrogateescape"))
    for rel in case["exec"]:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p):
            with open(p, "w") as fh:
                fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)


def case_env(case, root, lang):
    env = {k: v.replace("$ROOT", root) for k, v in case["env"].items()}
    env["HOME"] = os.path.join(root, "home")
    env["PATH"] = os.path.join(root, "bin") + ":/oracle/bin"
    env["XDG_CACHE_HOME"] = os.path.join(root, ".rw", "cache")
    env["LANG"] = lang
    return env


class Box:
    def __init__(self, work, script):
        self.work = work
        self.bwrap = shutil.which("bwrap")
        if not self.bwrap:
            raise SystemExit("bwrap missing")
        self.bin = tempfile.mkdtemp(dir=work, prefix="bin-")
        for n in EXTERNALS:
            src = shutil.which(n, path="/usr/bin")
            if not src:
                raise SystemExit("external %s missing" % n)
            shutil.copy(os.path.realpath(src), os.path.join(self.bin, n))
        self.bash = os.path.realpath("/usr/bin/bash")
        self.script = script

    def argv(self, root, env, args):
        rw = os.path.join(root, ".rw")
        a = [self.bwrap, "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
             "--ro-bind", "/usr/lib", "/usr/lib", "--symlink", "usr/lib", "/lib",
             "--symlink", "usr/lib", "/lib64",
             "--ro-bind", self.bash, "/bin/sh", "--ro-bind", self.bash, "/bin/bash",
             "--ro-bind", self.bin, "/oracle/bin", "--dev", "/dev", "--proc", "/proc",
             "--tmpfs", "/tmp",
             "--ro-bind", root, root, "--bind", rw, rw,
             "--ro-bind", self.script, "/oracle/xdg-terminal-exec",
             "--chdir", root]
        for k in sorted(env):
            a += ["--setenv", k, env[k]]
        a += ["--setenv", "PS4", "+${LINENO} "]
        a += ["/bin/sh", "-x", "/oracle/xdg-terminal-exec"] + args
        return a

    def run(self, root, env, args):
        argv = self.argv(root, env, args)
        try:
            p = subprocess.run(argv, capture_output=True, timeout=TIMEOUT,
                               env={"PATH": "/usr/bin"})
        except subprocess.TimeoutExpired:
            return 124, "", "", "timeout"
        return (p.returncode, p.stdout.decode("utf-8", "surrogateescape"),
                p.stderr.decode("utf-8", "surrogateescape"), "")


TRACE = re.compile(r"^\++(\d+) ")


def traced(stderr):
    out = []
    for ln in stderr.split("\n"):
        m = TRACE.match(ln)
        if m:
            out.append(int(m.group(1)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--variant", default="AB")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    if not os.path.isdir(a.work):
        raise SystemExit("work dir missing: %s" % a.work)
    work = tempfile.mkdtemp(dir=a.work, prefix="map-")
    fx = json.loads(pinned(FIXTURES, FIXTURES_SHA256).decode())
    script = os.path.join(work, "xdg-terminal-exec.map")
    with open(script, "wb") as fh:
        fh.write(pinned(PIN, PIN_SHA256))
    os.chmod(script, 0o755)
    src = open(script, "rb").read().decode("utf-8", "surrogateescape").split("\n")
    if a.only:
        idx = {c["id"]: c for c in fx}
        fx = [idx[i] for i in a.only.split(",")]
    box = Box(work, script)
    variants = [v for v in "AB" if v in a.variant]
    counts = {}
    per_case = {}
    bad = []
    for case in fx:
        for v in variants:
            base = tempfile.mkdtemp(dir=work, prefix="fx-")
            root = os.path.join(base, "r")
            materialize(root, case)
            args = [x.replace("$ROOT", root) for x in case["args"]]
            lang = "C.UTF-8" if v == "A" else "en_US.UTF-8"
            rc, out, err, why = box.run(root, case_env(case, root, lang), args)
            lines = traced(err)
            rec = {"rc": rc, "lines": sorted(set(lines)),
                   "n_traced": len(lines), "why": why}
            per_case["%s/%s" % (case["id"], v)] = rec
            for ln in set(lines):
                counts[ln] = counts.get(ln, 0) + 1
            # oracle drift check: our traced run must reproduce the recorded expect
            if v == "A":
                exp = case["expect"]
                got_out = out.replace(root, "$ROOT")
                if rc != exp["rc"] or got_out != exp["stdout"]:
                    bad.append((case["id"], rc, exp["rc"],
                                "" if got_out == exp["stdout"] else "stdout"))
            shutil.rmtree(base, ignore_errors=True)
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "lines.json"), "w") as fh:
        json.dump({"fixtures_sha256": FIXTURES_SHA256, "pin_sha256": PIN_SHA256,
                   "variants": variants, "n_cases": len(fx),
                   "counts": {str(k): counts[k] for k in sorted(counts)},
                   "per_case": per_case, "drift": bad}, fh, indent=1, sort_keys=True)
    # static candidate set: every line that could conceivably be a statement
    cand = []
    for i, ln in enumerate(src, 1):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        cand.append(i)
    unreached = [i for i in cand if i not in counts]
    with open(os.path.join(a.out, "unreached.txt"), "w") as fh:
        for i in unreached:
            fh.write("%4d| %s\n" % (i, src[i - 1]))
    obs_not_cand = [i for i in counts if i not in set(cand)]
    with open(os.path.join(a.out, "summary.txt"), "w") as fh:
        fh.write("fixtures=%d variants=%s lines_total=%d traced_lines=%d candidates=%d unreached=%d\n"
                 % (len(fx), "".join(variants), len(src), len(counts), len(cand), len(unreached)))
        fh.write("drift=%r\n" % (bad,))
        fh.write("observed_lines_outside_candidates=%r\n" % (obs_not_cand,))
    print("cases=%d variants=%s traced_lines=%d candidates=%d unreached=%d drift=%r outside=%r"
          % (len(fx), "".join(variants), len(counts), len(cand), len(unreached), bad, obs_not_cand))
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
