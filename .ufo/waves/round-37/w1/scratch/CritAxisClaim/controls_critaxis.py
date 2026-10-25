#!/usr/bin/env python3
"""CritAxisClaim controls: do-nothing and cheapest-skip cribs scored with BOTH frozen round-37 counters.

Sandbox only: one clone under /dev/shm/mado37-CritAxisClaim/sb, one branch per control from the
lane tip, sandbox identity. The lane is read (counters executed from the lane path, receipts copied
from committed blobs) and never written.
"""
import hashlib
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SB = "/dev/shm/mado37-CritAxisClaim/sb"
BASE = "b4e47e980bfb0cbc8a4e788f59a41db858751fd8"
FREEZE = "893a8aadc80ab19bc163e366d674a8ac32feacd0"
C1 = os.path.join(LANE, "quality/counters/c1-r37-event-ground.py")
C2 = os.path.join(LANE, "quality/counters/c2-r37-eventq.py")
PKG28 = "/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/event-queue-host-measurement-r28.md"
FETCH = ".ufo/waves/round-37/fetch"
E1 = "corpus/knowledge/event-delivery-limits-r26.md"
E2 = "corpus/knowledge/event-queue-observability-r37.md"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_AUTHOR_NAME="sandbox", GIT_AUTHOR_EMAIL="sandbox@invalid",
           GIT_COMMITTER_NAME="sandbox", GIT_COMMITTER_EMAIL="sandbox@invalid")
Q189 = "const size_t MAX_QUEUED_EVENTS = 64;"
Q189B = 'Log::logger->log(Log::ERR, "Socket2 fd {} overflowed event queue, removing", it->fd.get());'
Q214 = "m_logsEnabled = !*PDISABLELOGS;"
Q214B = 'static auto PDISABLELOGS  = CConfigValue<Config::INTEGER>("debug:disable_logs");'


def sh(*cmd, cwd=SB, check=True):
    p = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit(f"FAILED {cmd}: {p.stderr}")
    return p


def rd(rel):
    with open(os.path.join(SB, rel)) as f:
        return f.read()


def wr(rel, text):
    p = os.path.join(SB, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(text)


def header(ids):
    return f"# control entry\n\nsource: {', '.join(ids)}\nverified-at: 2026-10-25\nrecheck: 90d\n\n"


def wire_rows(dup189=False):
    """S189 used-by gains E1 (in place, or as a duplicate row); S214 is a new row used by E2."""
    src = rd("corpus/SOURCES.md").split("\n")
    out = []
    for line in src:
        if line.startswith("| S189 |") and not dup189:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            assert len(cells) == 11, len(cells)
            cells[10] = cells[10] + ", " + E1
            line = "| " + " | ".join(cells) + " |"
        out.append(line)
    text = "\n".join(out)
    new = ("| S214 | Hyprland v0.56.2 Logger.cpp — https://example.invalid/S214 | code | A | scope | anchor | "
           f"teaches | mined | 2026-10-25 | 90d | {E2} |\n")
    if dup189:
        new = ("| S189 | dup — https://example.invalid/S189 | code | A | scope | anchor | "
               f"teaches | mined | 2026-10-25 | 90d | {E1} |\n") + new
    head, tail = text.split("\n## Paths", 1)
    wr("corpus/SOURCES.md", head.rstrip("\n") + "\n" + new + "\n## Paths" + tail)


def wire_gate_index(gates):
    lines = []
    for sid, rel, q in gates:
        digest = hashlib.sha256(open(os.path.join(SB, rel), "rb").read()).hexdigest()
        lines.append(f'GATE {sid} receipt={rel} sha256={digest} quote="{q}"')
    wr("corpus/lessons/round-37.md", "# round 37 control\n\n## Gate\n\n" + "\n".join(lines) + "\n")
    readme = rd("corpus/README.md")
    head, tail = readme.split("\n## Quality bar", 1)
    add = f"| `knowledge/{os.path.basename(E1)}` | c | c |\n| `knowledge/{os.path.basename(E2)}` | c | c |\n"
    wr("corpus/README.md", head.rstrip("\n") + "\n" + add + "\n## Quality bar" + tail)


def minimal(e2_body=None, dup189=False):
    wr(E1, header(["S189"]) + f"**OBS** S189: `{Q189}` and `{Q189B}`\n")
    wr(E2, e2_body if e2_body is not None else header(["S214"]) + f"**OBS** S214: `{Q214}` `{Q214B}`\n")
    wire_rows(dup189)
    wire_gate_index([("S189", f"{FETCH}/S189.bin", Q189), ("S189", f"{FETCH}/S189.bin", Q189B),
                     ("S214", f"{FETCH}/S214.bin", Q214), ("S214", f"{FETCH}/S214.bin", Q214B)])


REFUSED = (header(["S214"]) + f"**OBS** S214: `{Q214}` `{Q214B}`\n\n"
           "A zero count of `overflowed event queue` markers in the session log proves that the "
           "compositor's event queue has never overflowed on this host.\n")


def pkg28():
    body = open(PKG28).read()
    return header(["S214"]) + f"**OBS** S214: `{Q214}` `{Q214B}`\n\n" + body


TOOL = r'''import argparse, re, sys
ap = argparse.ArgumentParser()
ap.add_argument("--ss-file"); ap.add_argument("--log", action="append", default=[])
ap.add_argument("--journal-file"); ap.add_argument("--disable-logs", default="0")
ap.add_argument("--expect-client", action="append", default=[]); ap.add_argument("--socket2")
a = ap.parse_args()
def setup(r):
    print("MADO_EVENTQ: SETUP " + r); sys.exit(2)
try:
    lines = open(a.ss_file).read().splitlines()
except (OSError, TypeError):
    setup("ss-unreadable")
if not lines or not lines[0].startswith("Netid"):
    setup("ss-unparseable")
rows = []
for l in lines[1:]:
    f = l.split()
    if len(f) < 8:
        continue
    m = re.search(r'users:\(\("([^"]+)",pid=(\d+),fd=(\d+)\)', l)
    rows.append(dict(st=f[1], rq=f[2], sq=f[3], loc=f[4], lp=f[5], pp=f[7], u=m.groups() if m else None))
lis = [r for r in rows if r["st"] == "LISTEN" and (r["loc"] == a.socket2 if a.socket2 else r["loc"].endswith("/.socket2.sock"))]
if not lis:
    setup("socket2-not-listening")
sock = lis[0]["loc"]
srv = {r["pp"]: r for r in rows if r["st"] == "ESTAB" and r["loc"] == sock}
cli = [(r, srv[r["lp"]]) for r in rows if r["st"] == "ESTAB" and r["lp"] in srv and r["u"]]
for r, s in cli:
    print("MADO_EVENTQ_CLIENT: comm=%s pid=%s fd=%s peer_recv_q=%s server_send_q=%s" % (r["u"] + (r["rq"], s["sq"])))
OV = re.compile(r"Socket2 fd \d+ overflowed event queue"); WF = re.compile(r"Socket2 fd \d+ failed writing event")
ov = wf = 0
for src, paths in (("log", a.log), ("journal", [a.journal_file] if a.journal_file else [])):
    for p in paths:
        t = open(p).read().splitlines()
        o = sum(bool(OV.search(x)) for x in t); w = sum(bool(WF.search(x)) for x in t)
        ov += o; wf += w
        print("MADO_EVENTQ_MARKERS: source=%s overflow=%d write_fail=%d" % (src, o, w))
lag = sum(r["rq"] != "0" for r, _ in cli)
have = {r["u"][0] for r, _ in cli}
miss = [c for c in a.expect_client if c not in have]
v = "MARKERS" if ov or wf else ("MISSING_CLIENT" if miss else "CLEAN")
print("MADO_EVENTQ: socket2=%s subscribers=%d overflow=%d write_fail=%d lagging=%d missing_client=%s markers_observable=%s verdict=%s"
      % (sock, len(cli), ov, wf, lag, ",".join(miss) or "-", "no" if a.disable_logs == "1" else "yes", v))
sys.exit(0 if v == "CLEAN" else 1)
'''
SOCK = "/run/user/1000/hypr/HIS/.socket2.sock"
FAKE_SS = ("Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:Port Process\n"
           f'u_str LISTEN 0 10 {SOCK} 1001 * 0 users:(("Hyprland",pid=1619,fd=33))\n'
           f'u_str ESTAB 0 0 {SOCK} 2001 * 3001 users:(("Hyprland",pid=1619,fd=250))\n'
           'u_str ESTAB 0 0 * 3001 * 2001 users:(("waybar",pid=935660,fd=21))\n')


def fake_live():
    wr("tools/mado-eventq.py", TOOL)
    wr(".ufo/waves/round-37/receipts/eventq-live-ss.txt", FAKE_SS)
    d = "/dev/shm/mado37-CritAxisClaim/fake"
    os.makedirs(d, exist_ok=True)
    for n in ("log", "journal"):
        open(os.path.join(d, n), "w").close()
    p = subprocess.run([sys.executable, "-I", os.path.join(SB, "tools/mado-eventq.py"), "--ss-file",
                        os.path.join(SB, ".ufo/waves/round-37/receipts/eventq-live-ss.txt"), "--log",
                        os.path.join(d, "log"), "--journal-file", os.path.join(d, "journal"),
                        "--disable-logs", "1"], capture_output=True, text=True)
    sha = hashlib.sha256(TOOL.encode()).hexdigest()
    wr(".ufo/waves/round-37/receipts/eventq-live.txt", f"tool_sha256={sha}\n" + p.stdout)


CONTROLS = [
    ("do-nothing-freeze", FREEZE, None),
    ("do-nothing-tip", "master", None),
    ("do-nothing-empty-commit", "master", lambda: None),
    ("c1-min-two-rows", "master", minimal),
    ("c1-refused-inference", "master", lambda: minimal(REFUSED)),
    ("c1-refused-pkg28-verbatim", "master", lambda: minimal(pkg28())),
    ("c1-duplicate-s189-row", "master", lambda: minimal(dup189=True)),
    ("c2-fabricated-live", "master", fake_live),
]


def score(counter, rev):
    args = [sys.executable, "-I", counter, "--repo", SB, "--rev", rev] + (["--base", BASE] if counter == C1 else [])
    p = subprocess.run(args, capture_output=True, text=True, env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")})
    return p.returncode, p.stdout.strip().splitlines()


def main():
    if not os.path.isdir(SB):
        sh("git", "clone", "-q", "--no-local", LANE, SB, cwd="/dev/shm/mado37-CritAxisClaim")
    out = [f"# sandbox {SB} cloned from {LANE}; lane master {sh('git', 'rev-parse', 'master').stdout.strip()}"]
    for name, start, build in CONTROLS:
        rev = sh("git", "rev-parse", start).stdout.strip()
        if build is not None:
            sh("git", "checkout", "-q", "-B", f"ctl-{name}", rev)
            build()
            sh("git", "add", "-A")
            sh("git", "commit", "-q", "--allow-empty", "-m", f"control {name}")
            rev = sh("git", "rev-parse", "HEAD").stdout.strip()
        for label, counter in (("C1", C1), ("C2", C2)):
            rc, lines = score(counter, rev)
            out.append(f"control={name} counter={label} rev={rev[:12]} rc={rc} :: {lines[-1] if lines else '-'}")
            out += [f"    {l}" for l in lines[:-1] if " entry=" in l or " ok=0" in l]
    print("\n".join(out))


if __name__ == "__main__":
    main()
