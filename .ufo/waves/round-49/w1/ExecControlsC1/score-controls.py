#!/usr/bin/env python3
"""Replica of ExecCounterC1's PRED-C1-r49 clause set, used ONLY to score the ExecControlsC1 controls.

ExecCounterC1 fixed the clause letters for the round-49 draft (message 2026-10-27, seat handoff):
  t  tool present: a regular blob with mode 100644 or 100755 (rev-addressed in the real counter; here read from
     --tool or from a control file in --controls, because the controls live in this seat dir and the L1 alone commits);
  s  `python3 -I TOOL --selftest` inside the sandbox exits 0 and its last stdout line is
     `MADO_KEYSYM_SELFTEST: N/N passed` with N >= 25;
  f  fixed fixtures: judge keymap compiled at count time with the pinned compile-keymap in a clean environment,
     tool vs pinned how-to-type: stdout bytes and exit status equal;
  g  nonce-generated (RMLVO, keysym) cases, same equality;
  r  readonly/no-process: strace -f on every tool run; after the python3 execve any execve/execveat/socket/
     socketpair/connect/fork/vfork/clone/clone3, and any write attempt (open flags O_WRONLY/RDWR/CREAT/TRUNC/APPEND,
     creat/mkdir(at)/rmdir/unlink(at)/rename(at|at2)/link(at)/symlink(at)/truncate/ftruncate/mknod(at)), is a trip.
Verdict TARGET_MET iff t present + s ok + f all + g all + r trips=0.

The case list is read from --cases (JSON produced by make-cases.py); every keymap is recompiled at score time from its
RMLVO and the judge is re-run, so the recorded judge bytes in the case file are only an authoring aid. Cases whose id
starts with `fx-` are the fixed fixtures (clause f), `gen-` the generated cases (clause g).

Sandbox (the counter's isolation, restated as a mount set): bwrap --unshare-all --die-with-parent --new-session
--clearenv with mounts exactly /usr/lib (ro), /lib and /lib64 as symlinks to usr/lib, /usr/bin/python3 (ro), the tool
at /case/tool.py (ro), the keymap at /case/keymap (ro), the keysym header at /usr/include/xkbcommon/... when
--header is given, /dev, /proc, a tmpfs /tmp, PATH=/usr/bin, HOME=/case/home, cwd /case. Nothing else is bound, so no
repository path and no fixture file exist inside.

Usage: score-controls.py --controls DIR --work DIR [--cases FILE] [--only NAME] [--header]
Exit: 0 if no control scored TARGET_MET, 1 if at least one did (that is the finding), 2 on setup failure.
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

COMPILE = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
HEADER = "/usr/include/xkbcommon/xkbcommon-keysyms.h"
COMPILE_SHA = "43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250"
JUDGE_SHA = "f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54"
BWRAP = shutil.which("bwrap")
STRACE = shutil.which("strace")
MINSELFTEST = 25

PROC_SET = ("execve", "execveat", "socket", "socketpair", "connect", "fork", "vfork", "clone", "clone3")
OPEN_SET = ("open", "openat", "openat2")
WRITE_SET = ("creat", "mkdir", "mkdirat", "rmdir", "unlink", "unlinkat", "rename", "renameat", "renameat2", "link",
             "linkat", "symlink", "symlinkat", "truncate", "ftruncate", "mknod", "mknodat")
TRACE_SET = "trace=" + ",".join(PROC_SET + OPEN_SET + WRITE_SET)
WRITE_FLAGS = re.compile(r"\bO_(WRONLY|RDWR|CREAT|TRUNC|APPEND)\b")
QUOTED = re.compile(r'"(?:[^"\\]|\\.)*"')
SELFTEST_RE = re.compile(r"^MADO_KEYSYM_SELFTEST: (\d+)/(\d+) passed$")


class Setup(Exception):
    pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_env(work):
    home = os.path.join(work, "env", "home")
    xdg = os.path.join(work, "env", "xdg")
    os.makedirs(home, exist_ok=True)
    os.makedirs(xdg, exist_ok=True)
    return {"PATH": "/usr/bin", "HOME": home, "XDG_CONFIG_HOME": xdg}


def compile_keymap(case, work, env):
    argv = [COMPILE, "--layout", case["layout"]]
    if case.get("variant"):
        argv += ["--variant", case["variant"]]
    if case.get("options"):
        argv += ["--options", case["options"]]
    p = subprocess.run(argv, capture_output=True, env=env, timeout=120)
    if p.returncode != 0:
        raise Setup("compile failed for %s: %s" % (case["id"], p.stderr.decode("utf-8", "replace")[:200]))
    return p.stdout


def judge(keymap_path, keysym, env):
    p = subprocess.run([JUDGE, "--keymap=" + keymap_path, "--disable-compose", "--keysym", keysym],
                       capture_output=True, env=env, timeout=120)
    return p.returncode, p.stdout.decode("utf-8", "surrogateescape"), p.stderr.decode("utf-8", "surrogateescape")


class Box:
    def __init__(self, work, bind_header, traces=True):
        self.work = work
        self.bind_header = bind_header
        self.traces = traces
        self.trips = []

    def argv(self, tool_path, keymap_path, args):
        a = [BWRAP, "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
             "--ro-bind", "/usr/lib", "/usr/lib",
             "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
             "--ro-bind", "/usr/bin/python3", "/usr/bin/python3",
             "--ro-bind", tool_path, "/case/tool.py"]
        if keymap_path:
            a += ["--ro-bind", keymap_path, "/case/keymap"]
        if self.bind_header:
            a += ["--ro-bind", HEADER, HEADER]
        a += ["--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
              "--setenv", "PATH", "/usr/bin", "--setenv", "HOME", "/case/home",
              "--chdir", "/case",
              "/usr/bin/python3", "-I", "/case/tool.py"]
        return a + list(args)

    def run(self, tool_path, keymap_path, args, timeout=60):
        """Runs the tool traced; returns (rc, stdout, stderr) and appends trips to self.trips.

        With traces=False (a --weaken r run) the tool is executed WITHOUT strace: that is the counter-minus-clause-r
        measurement, which is how a control proves the clause is what stopped it."""
        trace = None
        argv = self.argv(tool_path, keymap_path, args)
        if self.traces:
            fd, trace = tempfile.mkstemp(dir=self.work, prefix="trace-")
            os.close(fd)
            argv = [STRACE, "-f", "-qq", "-e", TRACE_SET, "-e", "signal=none", "-o", trace] + argv
        try:
            p = subprocess.run(argv, capture_output=True, timeout=timeout, env={"PATH": "/usr/bin"})
            res = (p.returncode, p.stdout.decode("utf-8", "surrogateescape"),
                   p.stderr.decode("utf-8", "surrogateescape"))
        except subprocess.TimeoutExpired:
            res = (124, "", "timeout")
        if trace:
            self.check_trace(trace)
        return res

    def check_trace(self, path):
        try:
            lines = open(path, encoding="latin-1").read().splitlines()
        except OSError:
            self.trips.append("trace-missing")
            return
        seen = False
        py_pid = None
        trip = re.compile(r"^(%s)\(" % "|".join(PROC_SET))
        wtrip = re.compile(r"^(%s)\(" % "|".join(WRITE_SET))
        otrip = re.compile(r"^(%s)\(" % "|".join(OPEN_SET))
        for ln in lines:
            pid, _, rest = ln.partition(" ")
            rest = rest.strip()
            if not seen:
                if 'execve("/usr/bin/python3"' in rest:
                    py_pid = pid
                    seen = rest.endswith("= 0")
                elif pid == py_pid and rest.startswith("<... execve resumed>"):
                    seen = rest.endswith("= 0")
                continue
            if rest.startswith("<..."):
                continue
            if trip.match(rest):
                self.trips.append(rest.split("(")[0] + ": " + rest[:70])
            elif wtrip.match(rest) or (otrip.match(rest) and WRITE_FLAGS.search(QUOTED.sub('""', rest))):
                self.trips.append("write: " + rest[:70])
        if not seen:
            self.trips.append("python-execve-not-seen")
        os.unlink(path)


def score_one(name, tool_path, cases, work, box, env, weaken=frozenset()):
    """Returns a dict describing the control's clauses. `weaken` names clauses the run switches OFF, so a control can
    demonstrate that the clause is what stopped it (a control that scores TARGET_MET with clause X weakened is a
    positive control for clause X)."""
    out = {"name": name, "t": "absent", "s": "-", "f": (0, 0), "g": (0, 0), "trips": 0, "stop": [], "detail": []}
    cases = [c for c in cases if not ((c["id"].startswith("fx-") and "f" in weaken) or
                                      (c["id"].startswith("gen-") and "g" in weaken))]
    if not tool_path or not os.path.isfile(tool_path):
        out["stop"].append("t (tool absent)")
        return out
    mode = os.stat(tool_path).st_mode & 0o777
    if mode not in (0o644, 0o755):
        out["t"] = "mode-%04o" % mode
        out["stop"].append("t (mode)")
        return out
    out["t"] = "present"

    # clause s: the tool's own selftest, sandboxed, traced like every other run.
    box.trips = []
    rc, so, se = box.run(tool_path, None, ["--selftest"], timeout=120)
    last = so.rstrip("\n").splitlines()[-1] if so.strip() else ""
    m = SELFTEST_RE.match(last)
    ok_s = rc == 0 and m is not None and int(m.group(1)) == int(m.group(2)) and int(m.group(1)) >= MINSELFTEST
    out["s"] = "ok" if ok_s else ("rc=%d last=%r" % (rc, last[:60]))
    out["trips"] += len(box.trips)
    if "s" in weaken:
        out["s"] = "ok(weakened)"
        ok_s = True
    if not ok_s:
        out["stop"].append("s (selftest)")
    if box.trips:
        out["stop"].append("r (selftest run: %s)" % box.trips[0])

    for case in cases:
        group = "f" if case["id"].startswith("fx-") else "g"
        good, total = out[group]
        total += 1
        keymap = os.path.join(work, "km", case["id"] + ".keymap")
        if not os.path.exists(keymap):
            data = compile_keymap(case, work, env)
            with open(keymap, "wb") as fh:
                fh.write(data)
        want_rc, want_out, _ = judge(keymap, case["keysym"], env)
        box.trips = []
        rc, so, se = box.run(tool_path, keymap,
                             ["how-to-type", "--keymap", "/case/keymap", "--disable-compose",
                              "--keysym", case["keysym"]])
        same = rc == want_rc and so == want_out
        good += 1 if same else 0
        out[group] = (good, total)
        if box.trips:
            out["trips"] += len(box.trips)
            if not any(s.startswith("r (") for s in out["stop"]):
                out["stop"].append("r (%s: %s)" % (case["id"], box.trips[0]))
        if not same and len(out["detail"]) < 4:
            out["detail"].append("%s %s keysym=%s rc=%d/%d out%s" % (
                case["id"], case["layout"], case["keysym"], rc, want_rc,
                " equal" if so == want_out else " differs"))
    if out["f"][0] != out["f"][1] and not any(s.startswith("f ") for s in out["stop"]):
        out["stop"].append("f (%d/%d)" % out["f"])
    if out["g"][0] != out["g"][1] and not any(s.startswith("g ") for s in out["stop"]):
        out["stop"].append("g (%d/%d)" % out["g"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--controls")
    ap.add_argument("--tool")
    ap.add_argument("--cases", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "cases.json"))
    ap.add_argument("--work", required=True)
    ap.add_argument("--only")
    ap.add_argument("--header", action="store_true", help="bind the keysym header into the sandbox")
    ap.add_argument("--weaken", default="", help="comma list of clauses to switch OFF (s,f,g,r): a control that then "
                                                 "scores TARGET_MET proves that clause is what stopped it")
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    if work == "/tmp" or work.startswith("/tmp/"):
        sys.exit("refusing a --work under /tmp (SentScratch)")
    if not (BWRAP and STRACE):
        raise SystemExit("setup: bwrap and strace are required")
    if sha256_file(COMPILE) != COMPILE_SHA or sha256_file(JUDGE) != JUDGE_SHA:
        raise SystemExit("setup: pinned binaries changed")
    os.makedirs(os.path.join(work, "km"), exist_ok=True)
    env = clean_env(work)
    with open(a.cases, encoding="utf-8") as fh:
        cases = json.load(fh)["cases"]
    if not any(c["id"].startswith("fx-") for c in cases) or not any(c["id"].startswith("gen-") for c in cases):
        raise SystemExit("setup: case file needs both fx- and gen- cases")

    if a.tool:
        targets = [(os.path.basename(a.tool), a.tool)]
    else:
        manifest = os.path.join(a.controls, "MANIFEST")
        if os.path.exists(manifest):
            # A control that is a MISSING tool cannot be a file: `name:absent` scores the tool path as empty.
            targets = []
            for line in open(manifest, encoding="utf-8"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                name, _, flag = line.partition(":")
                targets.append((name, None if flag == "absent" else os.path.join(a.controls, name)))
        else:
            targets = [(n, os.path.join(a.controls, n)) for n in sorted(os.listdir(a.controls))]
    if a.only:
        targets = [t for t in targets if a.only in t[0]]

    weaken = frozenset(x.strip() for x in a.weaken.split(",") if x.strip())
    if weaken - set("sfgr"):
        raise SystemExit("setup: --weaken takes a subset of t,s,f,g,r")
    box = Box(work, a.header, traces=("r" not in weaken))
    met = []
    print("PRED-C1-r49-replica: cases=%d fixtures=%d generated=%d header=%s work=%s weakened=%s" % (
        len(cases), sum(1 for c in cases if c["id"].startswith("fx-")),
        sum(1 for c in cases if c["id"].startswith("gen-")), "bound" if a.header else "not-bound",
        os.path.basename(work), ",".join(sorted(weaken)) or "-"))
    for name, path in targets:
        if path and os.path.isdir(path):
            continue
        r = score_one(name, path, cases, work, box, env, weaken)
        verdict = "TARGET_MET" if (r["t"] == "present" and r["s"] == "ok" and r["f"][0] == r["f"][1] and
                                   r["g"][0] == r["g"][1] and r["trips"] == 0) else "TARGET_MISSED"
        if verdict == "TARGET_MET":
            met.append(name)
        print("CTL %-26s t=%-8s s=%-22s f=%d/%d g=%d/%d trips=%-3d verdict=%s stop=%s" % (
            name, r["t"], r["s"], r["f"][0], r["f"][1], r["g"][0], r["g"][1], r["trips"], verdict,
            "; ".join(r["stop"]) or "-"))
        for d in r["detail"]:
            print("    %s" % d)
    print("PRED-C1-r49-replica: controls=%d met=%d %s" % (len(targets), len(met), ",".join(met) or "-"))
    return 1 if met else 0


if __name__ == "__main__":
    sys.exit(main())
