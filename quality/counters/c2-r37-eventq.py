#!/usr/bin/env python3
"""PRED-C2-r37-v2 — the event-socket subscriber census runs and discriminates.

Exports tools/mado-eventq.py from one committed revision into a private
scratch directory and scores it on the ten frozen fixture cases below (inputs
and expectations live in this file, so they are frozen with the rule). A case
passes when the tool's exit code equals the expected one, every `must`
pattern matches some output line and no `must_not` pattern matches any line.

Clauses:
  fixtures  passed == 10
  readonly  the tool source neither imports `socket` nor calls `connect(`
  live      .ufo/waves/round-37/receipts/eventq-live.txt is committed at REV,
            carries `tool_sha256=<sha256 of the tool blob at REV>`, one
            `MADO_EVENTQ:` summary line whose `subscribers=N` (N >= 1) equals
            its count of `MADO_EVENTQ_CLIENT:` lines, and a `comm=waybar` client;
            and the committed raw snapshot .ufo/waves/round-37/receipts/eventq-live-ss.txt
            replayed through the tool (`--ss-file` on it, empty log and journal,
            `--disable-logs 1`) yields the same multiset of (comm, pid, fd) client
            triples as the receipt (v1 lacked the replay: a hand-written receipt
            carrying the right digest passed)

Target: all three -> TARGET_MET, exit 0; otherwise TARGET_MISSED, exit 1.
Setup or usage errors exit 2. Git runs with every ambient GIT_* variable
removed.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

PRED = "PRED-C2-r37-v2"
TOOL = "tools/mado-eventq.py"
LIVE = ".ufo/waves/round-37/receipts/eventq-live.txt"
LIVE_SS = ".ufo/waves/round-37/receipts/eventq-live-ss.txt"
TRIPLE = re.compile(r"^MADO_EVENTQ_CLIENT: comm=(\S+) pid=(\S+) fd=(\S+)")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
SOCK = "/run/user/1000/hypr/HIS/.socket2.sock"
REQ = "/run/user/1000/hypr/HIS/.socket.sock"
HDR = "Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:Port Process\n"


def ss(*rows):
    return HDR + "".join(r + "\n" for r in rows)


LISTEN = f'u_str LISTEN 0 10 {SOCK} 1001 * 0 users:(("Hyprland",pid=1619,fd=33))'
SRV_W = f'u_str ESTAB 0 0 {SOCK} 2001 * 3001 users:(("Hyprland",pid=1619,fd=250))'
CLI_W = 'u_str ESTAB 0 0 * 3001 * 2001 users:(("waybar",pid=935660,fd=21))'
SRV_S = f'u_str ESTAB 0 0 {SOCK} 2002 * 3002 users:(("Hyprland",pid=1619,fd=147))'
CLI_S = 'u_str ESTAB 0 0 * 3002 * 2002 users:(("socat",pid=2293,fd=5))'
REQ_L = f'u_str LISTEN 0 10 {REQ} 1002 * 0 users:(("Hyprland",pid=1619,fd=32))'
REQ_E = f'u_str ESTAB 0 0 {REQ} 2003 * 3003 users:(("Hyprland",pid=1619,fd=40))'
REQ_C = 'u_str ESTAB 0 0 * 3003 * 2003 users:(("hyprctl",pid=4444,fd=3))'
OTHER = 'u_str ESTAB 0 0 * 9001 * 9002 users:(("chromium",pid=777,fd=21))'
CLEAN_SS = ss(LISTEN, REQ_L, SRV_W, CLI_W, SRV_S, CLI_S, REQ_E, REQ_C, OTHER)
LOG = "".join(f"DEBUG ]: core line {i}\n" for i in range(21)) + \
    "".join(f"DEBUG from aquamarine ]: backend line {i}\n" for i in range(40))
JOURNAL = "DEBUG ]: Using config: /home/u/.config/hypr/hyprland.conf\nstartup line\n"
OVERFLOW = "ERR ]: Socket2 fd 31 overflowed event queue, removing\n"
WRITEFAIL = "ERR ]: Socket2 fd 12 failed writing event: Broken pipe\n"
SUMMARY = r"^MADO_EVENTQ: socket2=\S+ "

CASES = [
    ("clean", dict(ss=CLEAN_SS, log=LOG, journal=JOURNAL, dl="0"), [], 0,
     [r"^MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 ",
      r"^MADO_EVENTQ_CLIENT: comm=socat pid=2293 fd=5 ",
      SUMMARY + r".*\bsubscribers=2\b.*\boverflow=0\b.*\bwrite_fail=0\b.*\bverdict=CLEAN\b",
      r"\bmarkers_observable=yes\b"],
     [r"comm=hyprctl", r"comm=chromium"]),
    ("overflow-log", dict(ss=CLEAN_SS, log=LOG + OVERFLOW, journal=JOURNAL, dl="0"), [], 1,
     [SUMMARY + r".*\boverflow=1\b.*\bverdict=MARKERS\b", r"^MADO_EVENTQ_MARKERS: source=log\S* .*\boverflow=1\b"], []),
    ("writefail-journal", dict(ss=CLEAN_SS, log=LOG, journal=JOURNAL + WRITEFAIL, dl="0"), [], 1,
     [SUMMARY + r".*\bwrite_fail=1\b.*\bverdict=MARKERS\b",
      r"^MADO_EVENTQ_MARKERS: source=journal .*\bwrite_fail=1\b"], []),
    ("not-listening", dict(ss=ss(REQ_L, REQ_E, REQ_C, OTHER), log=LOG, journal=JOURNAL, dl="0"), [], 2,
     [r"^MADO_EVENTQ: SETUP "], [r"verdict=CLEAN"]),
    ("missing-client", dict(ss=ss(LISTEN, SRV_S, CLI_S), log=LOG, journal=JOURNAL, dl="0"),
     ["--expect-client", "waybar"], 1,
     [SUMMARY + r".*\bsubscribers=1\b.*\bmissing_client=waybar\b.*\bverdict=MISSING_CLIENT\b"], []),
    ("lagging", dict(ss=ss(LISTEN, SRV_W, CLI_W.replace("ESTAB 0 0", "ESTAB 2048 0"), SRV_S, CLI_S),
                     log=LOG, journal=JOURNAL, dl="0"), [], 0,
     [r"^MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 .*\bpeer_recv_q=2048\b",
      SUMMARY + r".*\blagging=1\b.*\bverdict=CLEAN\b"], []),
    ("unparseable", dict(ss="this is not ss output\n", log=LOG, journal=JOURNAL, dl="0"), [], 2,
     [r"^MADO_EVENTQ: SETUP "], [r"verdict="]),
    ("logs-disabled", dict(ss=CLEAN_SS, log=LOG, journal=JOURNAL, dl="1"), [], 0,
     [SUMMARY + r".*\bmarkers_observable=no\b.*\bverdict=CLEAN\b"], [r"markers_observable=yes"]),
    ("overflow-twice", dict(ss=CLEAN_SS, log=LOG + OVERFLOW + OVERFLOW.replace("31", "32"), journal=JOURNAL, dl="0"),
     [], 1, [SUMMARY + r".*\boverflow=2\b.*\bverdict=MARKERS\b"], []),
    ("decoy", dict(ss=CLEAN_SS, log=LOG + "DEBUG from aquamarine ]: note: overflowed event queue in a test\n",
                   journal=JOURNAL + "failed writing event mentioned in prose\n", dl="0"), [], 0,
     [SUMMARY + r".*\boverflow=0\b.*\bwrite_fail=0\b.*\bverdict=CLEAN\b"], []),
]


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV)
    return p.stdout if p.returncode == 0 else None


def run_case(tool, work, case):
    name, inp, extra, want_rc, must, must_not = case
    d = os.path.join(work, name)
    os.makedirs(d)
    paths = {}
    for key, fname in (("ss", "ss.txt"), ("log", "hyprland.log"), ("journal", "journal.txt")):
        paths[key] = os.path.join(d, fname)
        with open(paths[key], "w") as f:
            f.write(inp[key])
    cmd = [sys.executable, "-I", tool, "--ss-file", paths["ss"], "--log", paths["log"],
           "--journal-file", paths["journal"], "--disable-logs", inp["dl"], *extra]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=20, cwd=d)
        rc, lines = p.returncode, p.stdout.splitlines()
    except (subprocess.TimeoutExpired, OSError):
        rc, lines = None, []
    ok = (rc == want_rc
          and all(any(re.search(m, l) for l in lines) for m in must)
          and not any(re.search(m, l) for m in must_not for l in lines))
    return ok, rc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    rev = git(repo, "rev-parse", "--verify", f"{a.rev}^{{commit}}")
    if not rev:
        print(f"{PRED} SETUP unresolvable revision")
        return 2
    rev = rev.decode().strip()
    blob = git(repo, "show", f"{rev}:{TOOL}")
    root = "/dev/shm" if os.path.isdir("/dev/shm") else None
    work = tempfile.mkdtemp(prefix="mado-c2-r37-", dir=root)
    live = 0
    try:
        passed = 0
        if blob is not None:
            tool = os.path.join(work, "mado-eventq.py")
            with open(tool, "wb") as f:
                f.write(blob)
        for case in CASES:
            ok, rc = run_case(tool, work, case) if blob is not None else (False, None)
            passed += ok
            print(f"{PRED} case={case[0]} want_rc={case[3]} rc={rc} ok={int(ok)}")
        receipt = git(repo, "show", f"{rev}:{LIVE}")
        snap = git(repo, "show", f"{rev}:{LIVE_SS}")
        if blob is not None and receipt is not None and snap is not None:
            text = receipt.decode("utf-8", "replace").splitlines()
            sums = [l for l in text if l.startswith("MADO_EVENTQ: ")]
            clients = [l for l in text if l.startswith("MADO_EVENTQ_CLIENT: ")]
            m = re.search(r"\bsubscribers=(\d+)\b", sums[0]) if len(sums) == 1 else None
            d = os.path.join(work, "live-replay")
            os.makedirs(d)
            for fname, data in (("ss.txt", snap), ("hyprland.log", b""), ("journal.txt", b"")):
                with open(os.path.join(d, fname), "wb") as f:
                    f.write(data)
            try:
                p = subprocess.run([sys.executable, "-I", tool, "--ss-file", os.path.join(d, "ss.txt"),
                                    "--log", os.path.join(d, "hyprland.log"), "--journal-file",
                                    os.path.join(d, "journal.txt"), "--disable-logs", "1"],
                                   capture_output=True, text=True, timeout=20, cwd=d)
                replay = p.stdout.splitlines()
            except (subprocess.TimeoutExpired, OSError):
                replay = []
            triples = lambda ls: sorted(m2.groups() for m2 in map(TRIPLE.match, ls) if m2)
            live = int(f"tool_sha256={hashlib.sha256(blob).hexdigest()}" in text
                       and m is not None and int(m.group(1)) >= 1 and int(m.group(1)) == len(clients)
                       and any(" comm=waybar " in l + " " for l in clients)
                       and triples(clients) == triples(replay) and len(triples(clients)) == len(clients))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    src = (blob or b"").decode("utf-8", "replace")
    readonly = int(blob is not None
                   and not re.search(r"^\s*(import\s+socket\b|from\s+socket\s+import)", src, re.M)
                   and "connect(" not in src)
    met = passed == len(CASES) and readonly and live
    verdict = "TARGET_MET" if met else "TARGET_MISSED"
    print(f"{PRED} fixtures={passed}/{len(CASES)} readonly={readonly} live={live} "
          f"tool={'present' if blob is not None else 'absent'} verdict={verdict} rev={rev}")
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
