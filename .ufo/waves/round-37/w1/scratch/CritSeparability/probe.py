#!/usr/bin/env python3
"""CritSeparability probe: score both frozen counters on sandbox trees with one side deleted.

Sandboxes live under /dev/shm/mado37-CritSeparability (git clone --no-local of the lane,
sandbox identity). The lane itself is only read. Prints one line per (tree, counter).
"""
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/dev/shm/mado37-CritSeparability"
C1 = os.path.join(LANE, "quality/counters/c1-r37-event-ground.py")
C2 = os.path.join(LANE, "quality/counters/c2-r37-eventq.py")
TOOL = "tools/mado-eventq.py"
LIVE = ".ufo/waves/round-37/receipts/eventq-live.txt"
LIVE_SS = ".ufo/waves/round-37/receipts/eventq-live-ss.txt"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ctl = load("controls", os.path.join(LANE, ".ufo/waves/round-37/controls.py"))
c2 = load("c2", C2)
ENV = ctl.ENV


def sh(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True)


def commit(sb, msg):
    sh("git", "-C", sb, "add", "-A")
    sh("git", "-C", sb, "commit", "-q", "--allow-empty", "-m", msg)


def build_c2(sb):
    os.makedirs(os.path.join(sb, "tools"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "ref-eventq.py"), os.path.join(sb, TOOL))
    os.makedirs(os.path.join(sb, os.path.dirname(LIVE)), exist_ok=True)
    ss_path = os.path.join(sb, LIVE_SS)
    with open(ss_path, "w") as f:
        f.write(c2.CLEAN_SS)
    empty = os.path.join(ROOT, "empty")
    open(empty, "w").close()
    out = subprocess.run([sys.executable, "-I", os.path.join(sb, TOOL), "--ss-file", ss_path, "--log", empty,
                          "--journal-file", empty, "--disable-logs", "1"], capture_output=True, text=True).stdout
    sha = hashlib.sha256(open(os.path.join(sb, TOOL), "rb").read()).hexdigest()
    with open(os.path.join(sb, LIVE), "w") as f:
        f.write(f"# SYNTHETIC sandbox receipt (fixture CLEAN_SS), not a host observation\ntool_sha256={sha}\n{out}")


def bind_extra(sb, receipt_rel, quote, sid="S215"):
    """Add a C1 citation of a C2 artifact to E2: source id, OBS line, registry row, Gate line."""
    e2 = os.path.join(sb, ctl.E2)
    body = open(e2).read().replace("source: S213, S214", f"source: S213, S214, {sid}")
    body += f"**OBS** {sid}: `{quote}`\n"
    open(e2, "w").write(body)
    src = open(os.path.join(sb, "corpus/SOURCES.md")).read()
    head, tail = src.split("\n## Paths", 1)
    open(os.path.join(sb, "corpus/SOURCES.md"), "w").write(
        head.rstrip("\n") + "\n" + ctl.row(sid, ctl.E2) + "\n## Paths" + tail)
    digest = hashlib.sha256(open(os.path.join(sb, receipt_rel), "rb").read()).hexdigest()
    with open(os.path.join(sb, "corpus/lessons/round-37.md"), "a") as f:
        f.write(f'GATE {sid} receipt={receipt_rel} sha256={digest} quote="{quote}"\n')


def rm(sb, *rels):
    for rel in rels:
        p = os.path.join(sb, rel)
        if os.path.isdir(p):
            shutil.rmtree(p)
        elif os.path.exists(p):
            os.remove(p)


def score(sb):
    out = []
    for name, counter in (("C1", C1), ("C2", C2)):
        p = subprocess.run([sys.executable, "-I", counter, "--repo", sb, "--rev", "HEAD"],
                           capture_output=True, text=True, env=ENV)
        lines = p.stdout.strip().splitlines()
        out.append((name, p.returncode, lines[-1] if lines else p.stderr.strip()[-200:], lines[:-1]))
    return out


def tree(name, steps):
    sb = os.path.join(ROOT, name)
    shutil.rmtree(sb, ignore_errors=True)
    sh("git", "clone", "-q", "--no-local", LANE, sb)
    for i, (msg, fn) in enumerate(steps):
        fn(sb)
        commit(sb, f"probe {name} step {i}: {msg}")
    head = sh("git", "-C", sb, "rev-parse", "HEAD").stdout.strip()
    for cname, rc, summary, detail in score(sb):
        print(f"tree={name} counter={cname} rc={rc} :: {summary}")
        for d in detail:
            if cname == "C1" or " ok=0" in d:
                print(f"    {d}")
    print(f"tree={name} head={head}")
    shutil.rmtree(sb, ignore_errors=True)


JOINT = [("C1 golden-v2 wiring (controls.wire)", ctl.wire), ("C2 reference tool + synthetic receipts", build_c2)]
C2_FILES = (TOOL, LIVE, LIVE_SS)

TREES = {
    "base-head": [],
    "joint": JOINT,
    "joint-minus-c2": JOINT + [("delete C2 files", lambda sb: rm(sb, *C2_FILES))],
    "joint-minus-c1": JOINT + [("restore corpus/ to pre-wire state", lambda sb: (rm(sb, "corpus"), sh(
        "git", "-C", sb, "checkout", "-q", "HEAD~2", "--", "corpus")))],
    "joint-no-corpus": JOINT + [("delete all of corpus/", lambda sb: rm(sb, "corpus"))],
    "joint-no-tools-no-receipts": JOINT + [("delete tools/ and round-37 receipts/", lambda sb: rm(
        sb, "tools", ".ufo/waves/round-37/receipts"))],
    "joint-no-fetch": JOINT + [("delete round-37 fetch/", lambda sb: rm(sb, ".ufo/waves/round-37/fetch"))],
    "coupled-live": JOINT + [("E2 binds S215 to the C2 live receipt", lambda sb: bind_extra(
        sb, LIVE, "comm=waybar pid=935660 fd=21"))],
    "coupled-live-minus-c2": JOINT + [("E2 binds S215 to the C2 live receipt", lambda sb: bind_extra(
        sb, LIVE, "comm=waybar pid=935660 fd=21")), ("delete C2 files", lambda sb: rm(sb, *C2_FILES))],
    "coupled-tool": JOINT + [("E2 binds S215 to the tool source", lambda sb: bind_extra(
        sb, TOOL, "never opens any socket"))],
    "coupled-tool-minus-c2": JOINT + [("E2 binds S215 to the tool source", lambda sb: bind_extra(
        sb, TOOL, "never opens any socket")), ("delete C2 files", lambda sb: rm(sb, *C2_FILES))],
}

if __name__ == "__main__":
    os.makedirs(ROOT, exist_ok=True)
    for name in (sys.argv[1:] or TREES):
        tree(name, TREES[name])
