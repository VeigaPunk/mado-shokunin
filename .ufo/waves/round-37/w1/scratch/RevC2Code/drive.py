#!/usr/bin/env python3
"""Scratch driver (RevC2Code): score tool/receipt variants with the frozen C2 counter in a sandbox clone."""
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
HERE = "/dev/shm/mado37-RevC2Code"
SB = os.path.join(HERE, "sb")
COUNTER = os.path.join(LANE, "quality/counters/c2-r37-eventq.py")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_AUTHOR_NAME="sandbox", GIT_AUTHOR_EMAIL="sandbox@invalid",
           GIT_COMMITTER_NAME="sandbox", GIT_COMMITTER_EMAIL="sandbox@invalid")

spec = importlib.util.spec_from_file_location("c2", COUNTER)
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

REF = open(os.path.join(HERE, "ref-eventq.py")).read()
LIVE_SS = open(os.path.join(HERE, "ss-full.txt"), "rb").read()
FORGED_SS = c2.CLEAN_SS.encode()

ONEPASS = re.sub(
    r"    by_inode = .*?# PASS_MARKER\n    clients = \[\]\n    for r in rows:\n.*?clients\.append\(.*?\)\n",
    '''    pending = {}
    clients = []
    for r in rows:
        if r[1] == "ESTAB" and is_s2(r[4]):
            pending[r[7]] = r
        elif r[5] in pending:
            s = pending.pop(r[5])
            u = USERS.search(r[8]) if len(r) > 8 else None
            comm, pid, fd = u.groups() if u else ("?", "?", "?")
            clients.append((comm, pid, fd, r[2], s[3]))
''', REF, flags=re.S)
assert ONEPASS != REF
LAGCONST = re.sub(r"    lagging = .*# LAG_MARKER", "    lagging = 1", REF)
MISSALL = re.sub(r"    missing = .*# MISS_MARKER", "    missing = list(a.expect_client)", REF)
IMPSOCK = REF.replace("import argparse\n", "import argparse\nimport os, socket  # never used\n", 1)
DOCCONN = REF.replace('"""Scratch reference', '"""Never calls connect() on any socket. Scratch reference', 1)
for v in (LAGCONST, MISSALL, IMPSOCK, DOCCONN):
    assert v != REF

VARIANTS = {"ref": REF, "onepass": ONEPASS, "lagconst": LAGCONST, "missall": MISSALL,
            "impsock": IMPSOCK, "docconn": DOCCONN}


def sh(*cmd, cwd=SB, **kw):
    return subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, **kw)


def tool_out(src, snap):
    d = os.path.join(HERE, "rcpt")
    os.makedirs(d, exist_ok=True)
    t = os.path.join(d, "t.py")
    open(t, "w").write(src)
    open(os.path.join(d, "ss.txt"), "wb").write(snap)
    open(os.path.join(d, "e.log"), "w").close()
    p = subprocess.run([sys.executable, "-I", t, "--ss-file", os.path.join(d, "ss.txt"), "--log",
                        os.path.join(d, "e.log"), "--journal-file", os.path.join(d, "e.log"),
                        "--disable-logs", "1"], capture_output=True, text=True)
    return p.stdout


SCEN = [
    ("ref-live", "ref", LIVE_SS, "plain"),
    ("ref-forged-fixture", "ref", FORGED_SS, "plain"),
    ("ref-live-prefixed-sha", "ref", LIVE_SS, "prefixed"),
    ("onepass-forged-fixture", "onepass", FORGED_SS, "plain"),
    ("onepass-live", "onepass", LIVE_SS, "plain"),
    ("lagconst-live", "lagconst", LIVE_SS, "plain"),
    ("missall-live", "missall", LIVE_SS, "plain"),
    ("impsock-live", "impsock", LIVE_SS, "plain"),
    ("docconn-live", "docconn", LIVE_SS, "plain"),
]

if not os.path.isdir(SB):
    subprocess.run(["git", "clone", "-q", "--no-local", LANE, SB], env=ENV, check=True)
base = sh("git", "rev-parse", "HEAD").stdout.strip()
print(f"sandbox_base={base}")
for name, var, snap, mode in SCEN:
    src = VARIANTS[var]
    sh("git", "checkout", "-q", "-B", f"probe-{name}", base)
    os.makedirs(os.path.join(SB, "tools"), exist_ok=True)
    open(os.path.join(SB, c2.TOOL), "w").write(src)
    digest = hashlib.sha256(src.encode()).hexdigest()
    line = f"tool_sha256={digest}" if mode == "plain" else f"MADO_EVENTQ_RECEIPT: tool_sha256={digest}"
    open(os.path.join(SB, c2.LIVE), "w").write(line + "\n" + tool_out(src, snap))
    open(os.path.join(SB, c2.LIVE_SS), "wb").write(snap)
    sh("git", "add", "-f", c2.TOOL, c2.LIVE, c2.LIVE_SS)
    sh("git", "commit", "-q", "-m", f"probe {name}")
    rev = sh("git", "rev-parse", "HEAD").stdout.strip()
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", SB, "--rev", rev],
                       capture_output=True, text=True, env=ENV)
    summary = p.stdout.strip().splitlines()[-1]
    bad = [l for l in p.stdout.splitlines() if " ok=0" in l]
    print(f"scenario={name} exit={p.returncode} :: {summary}")
    for l in bad:
        print(f"    {l}")
