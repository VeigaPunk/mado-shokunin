#!/usr/bin/env python3
"""PRED-C2-r38-v3 — the event-socket subscriber census runs and discriminates (v3).

Round-38 v3 of the round-37 instrument, repaired against the wave-1 findings
recorded in `corpus/lessons/round-37.md` M37-5 (routed defect; v2 stays frozen
beside it, never edited). The fixture contract is v2's ten cases plus four:

  clients-first     the live table lists client rows before their server rows
                    (F3: every v2 fixture put the server first)
  server-two-tuple  a live server row carries two users: tuples (F3)
  comm-spaces       a subscriber comm containing whitespace is shown as `_`
  expect-present    --expect-client naming a present subscriber passes (F5)
  lagging-clean     added lagging=0 assertion inside `clean` (F4)

The live clause is v3: v2 replayed a committed `ss` snapshot and trusted any
receipt file, so the counter's own fixture committed as `eventq-live-ss.txt`
met the target (RevC2Code F1). v3 requires a three-artifact, internally
consistent receipt:

  receipt  `.ufo/waves/round-38/receipts/eventq-live.txt` — carries a
           `tool_sha256=` substring on some line (F2: a whole-line pin
           false-misses a genuine receipt), one MADO_EVENTQ summary and the
           same (comm,pid,fd) client set the tool derives when replayed on
           the snapshot; `subscribers` equals the client-line count.
  snapshot `.ufo/waves/round-38/receipts/eventq-live-ss.txt` — replays to the
           receipt's client set, is byte-wise unequal to every fixture table
           this counter embeds (the demonstrated crib), and is not a
           `--snapshot-out` subset (it must name a request-socket or
           unrelated row too).
  proc     `.ufo/waves/round-38/receipts/eventq-live-proc.txt` — a committed
           `/proc/net/unix`-based scan binding the snapshot: it carries
           `ss_sha256=<digest of the snapshot>`, names every socket2
           LISTEN/ESTAB server inode from the snapshot as `/proc` rows held
           only by the compositor pid(s) the receipt names, and ends
           `OVERALL: AGREE`.

Residual (reported, not hidden): a fully fabricated consistent triplet —
invented inodes repeated identically across ss and proc artifacts — still
reaches the live clause, the same accept-path tradeoff the C1 v3 counter
records. The v3 binding raises the crib from "commit one fixture file" to
"forge three mutually consistent artifacts"; it does not make live truth
provable from committed bytes.

TARGET_MET iff fixtures pass, the tool is read-only (no socket module import
and no `connect(` outside comments/docstrings — F6), and the live triplet
holds. Exit 0/1/2 as v2. Git runs with every ambient GIT_* variable removed.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

PRED = "PRED-C2-r38-v3"
TOOL = "tools/mado-eventq.py"
LIVE = ".ufo/waves/round-38/receipts/eventq-live.txt"
LIVE_SS = ".ufo/waves/round-38/receipts/eventq-live-ss.txt"
LIVE_PROC = ".ufo/waves/round-38/receipts/eventq-live-proc.txt"
TRIPLE = re.compile(r"^MADO_EVENTQ_CLIENT: comm=(\S+) pid=(\S+) fd=(\S+)")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
SOCK = "/run/user/1000/hypr/HIS/.socket2.sock"
REQ = "/run/user/1000/hypr/HIS/.socket.sock"
HDR = "Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:Port Process\n"


def ss(*rows):
    return HDR + "".join(r + "\n" for r in rows)


LISTEN = f'u_str LISTEN 0 10 {SOCK} 1001 * 0 users:(("Hyprland",pid=1619,fd=11),("Hyprland",pid=1619,fd=10))'
LISTEN_1T = f'u_str LISTEN 0 10 {SOCK} 1001 * 0 users:(("Hyprland",pid=1619,fd=33))'
SRV_W = f'u_str ESTAB 0 0 {SOCK} 2001 * 3001 users:(("Hyprland",pid=1619,fd=250),("Hyprland",pid=1619,fd=236))'
SRV_W_1T = f'u_str ESTAB 0 0 {SOCK} 2001 * 3001 users:(("Hyprland",pid=1619,fd=250))'
CLI_W = 'u_str ESTAB 0 0 * 3001 * 2001 users:(("waybar",pid=935660,fd=21))'
SRV_S = f'u_str ESTAB 0 0 {SOCK} 2002 * 3002 users:(("Hyprland",pid=1619,fd=147),("Hyprland",pid=1619,fd=145))'
CLI_S = 'u_str ESTAB 0 0 * 3002 * 2002 users:(("socat",pid=2293,fd=5))'
CLI_NU = 'u_str ESTAB 0 0 * 3001 * 2001'                       # no users: field
CLI_SP = 'u_str ESTAB 0 0 * 3001 * 2001 users:(("my helper",pid=935660,fd=21))'
REQ_L = f'u_str LISTEN 0 10 {REQ} 1002 * 0 users:(("Hyprland",pid=1619,fd=32))'
REQ_E = f'u_str ESTAB 0 0 {REQ} 2003 * 3003 users:(("Hyprland",pid=1619,fd=40))'
REQ_C = 'u_str ESTAB 0 0 * 3003 * 2003 users:(("hyprctl",pid=4444,fd=3))'
OTHER = 'u_str ESTAB 0 0 * 9001 * 9002 users:(("chromium",pid=777,fd=21))'
OTHER_NU = 'u_str ESTAB 0 0 * 9001 * 9002'
CLEAN_SS = ss(LISTEN, REQ_L, SRV_W, CLI_W, SRV_S, CLI_S, REQ_E, REQ_C, OTHER)
# Live-order variant: client rows precede their server rows; a server row
# carries two users: tuples; an unrelated no-users row is present.
LIVEORDER_SS = ss(LISTEN, REQ_L, CLI_W, SRV_W, CLI_S, SRV_S, OTHER_NU, REQ_E, REQ_C, OTHER)
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
      SUMMARY + r".*\bsubscribers=2\b.*\boverflow=0\b.*\bwrite_fail=0\b.*\blagging=0\b.*\bverdict=CLEAN\b",
      r"\bmarkers_observable=yes\b"],
     [r"comm=hyprctl", r"comm=chromium"]),
    ("clients-first", dict(ss=LIVEORDER_SS, log=LOG, journal=JOURNAL, dl="0"), [], 0,
     [r"^MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 .*\bserver_fd=250,236\b",
      r"^MADO_EVENTQ_CLIENT: comm=socat pid=2293 fd=5 ",
      SUMMARY + r".*\bsubscribers=2\b.*\bverdict=CLEAN\b"], []),
    ("client-no-users", dict(ss=ss(LISTEN_1T, SRV_W_1T, CLI_NU, OTHER), log=LOG, journal=JOURNAL, dl="0"),
     [], 0,
     [r"^MADO_EVENTQ_CLIENT: comm=- pid=- fd=- peer_recv_q=0 ",
      SUMMARY + r".*\bsubscribers=1\b.*\bverdict=CLEAN\b"],
     [r"comm=waybar"]),
    ("comm-spaces", dict(ss=ss(LISTEN_1T, SRV_W_1T, CLI_SP, OTHER), log=LOG, journal=JOURNAL, dl="0"),
     [], 0,
     [r"^MADO_EVENTQ_CLIENT: comm=my_helper pid=935660 fd=21 ",
      SUMMARY + r".*\bsubscribers=1\b.*\bverdict=CLEAN\b"], []),
    ("expect-present", dict(ss=CLEAN_SS, log=LOG, journal=JOURNAL, dl="0"),
     ["--expect-client", "waybar", "--expect-client", "socat"], 0,
     [SUMMARY + r".*\bsubscribers=2\b.*\bmissing_client=- .*?\bverdict=CLEAN\b"], []),
    ("overflow-log", dict(ss=CLEAN_SS, log=LOG + OVERFLOW, journal=JOURNAL, dl="0"), [], 1,
     [SUMMARY + r".*\boverflow=1\b.*\bverdict=MARKERS\b",
      r"^MADO_EVENTQ_MARKERS: source=log\S* .*\boverflow=1\b"], []),
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

FIXTURE_TABLES = [CLEAN_SS, LIVEORDER_SS]


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


def code_lines(src):
    """Source minus comments and the module docstring: the read-only clause
    scans code, so prose mentioning `connect(` cannot false-miss (F6)."""
    out = []
    for line in src.splitlines():
        s = line.strip()
        if not s.startswith("#"):
            out.append(line.split("#", 1)[0] if " #" in line else line)
    body = "\n".join(out)
    body = re.sub(r'""".*?"""', "", body, flags=re.S)
    return body


def live_check(repo, rev, tool, work):
    """v3 live clause: the three-artifact internally-consistent receipt."""
    receipt = git(repo, "show", f"{rev}:{LIVE}")
    snap = git(repo, "show", f"{rev}:{LIVE_SS}")
    proc = git(repo, "show", f"{rev}:{LIVE_PROC}")
    if receipt is None or snap is None or proc is None:
        return 0, "artifacts-missing"
    # Snapshot must not be an embedded fixture table (the demonstrated crib).
    for fx in FIXTURE_TABLES:
        if snap == fx.encode():
            return 0, "snapshot-is-fixture"
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
    replay_ok = (m is not None and int(m.group(1)) >= 1 and int(m.group(1)) == len(clients)
                 and triples(clients) == triples(replay) and len(triples(clients)) == len(clients))
    sha_ok = any("tool_sha256=" + hashlib.sha256(
        git(repo, "show", f"{rev}:{TOOL}") or b"").hexdigest() in l for l in text)
    # The snapshot must be a full-table capture, not a --snapshot-out subset:
    # it must carry at least one row outside the socket2 LISTEN/ESTAB set and
    # their client peers (e.g. the request socket or an unrelated socket).
    snap_text = snap.decode("utf-8", "replace").splitlines()
    extra_rows = [l for l in snap_text[1:]
                  if ".socket2.sock" not in l and re.match(r"^\S+\s+\S+\s+\d+\s+\d+\s", l)]
    full_table = len(extra_rows) >= 1
    # Proc binding: snapshot digest named, every socket2 server inode in the
    # snapshot named as a /proc row held by a compositor pid, verdict AGREE.
    ptext = proc.decode("utf-8", "replace")
    snap_sha = hashlib.sha256(snap).hexdigest()
    # LISTEN + ESTAB server rows: Local == socket path.
    srv = set()
    for l in snap_text[1:]:
        if ".socket2.sock" in l and re.match(r"^u_\S+\s+(LISTEN|ESTAB)\s", l):
            mm = re.search(r"\.socket2\.sock\s+(\d+)", l)
            if mm:
                srv.add(mm.group(1))
    named = sum(1 for i in srv if re.search(rf"\b{i}\b", ptext))
    proc_ok = (f"ss_sha256={snap_sha}" in ptext
               and srv and named == len(srv)
               and re.search(r"OVERALL:\s*AGREE", ptext) is not None)
    why = (f"replay={int(replay_ok)} sha={int(sha_ok)} full_table={int(full_table)} "
           f"proc={named}/{len(srv)} sha_in={int('ss_sha256=' + snap_sha in ptext)} "
           f"agree={int(bool(re.search('OVERALL:.AGREE', ptext)))}")
    live = int(sha_ok and replay_ok and full_table and proc_ok)
    return live, why


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
    work = tempfile.mkdtemp(prefix="mado-c2-r38-", dir=root)
    live, why = 0, "unscored"
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
        if blob is not None:
            live, why = live_check(repo, rev, tool, work)
            print(f"{PRED} live-detail {why}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    src = code_lines((blob or b"").decode("utf-8", "replace"))
    readonly = int(blob is not None
                   and not re.search(r"\bimport\s+socket\b|\bfrom\s+socket\b", src)
                   and "connect(" not in src)
    met = passed == len(CASES) and readonly and live
    verdict = "TARGET_MET" if met else "TARGET_MISSED"
    print(f"{PRED} fixtures={passed}/{len(CASES)} readonly={readonly} live={live} "
          f"tool={'present' if blob is not None else 'absent'} verdict={verdict} rev={rev}")
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
