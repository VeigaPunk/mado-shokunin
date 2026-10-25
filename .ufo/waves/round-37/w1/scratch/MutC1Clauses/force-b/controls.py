#!/usr/bin/env python3
"""Round-37 controls: score cheap do-nothing, crib and golden trees with the frozen counters.

Every control is built in a sandbox clone under /dev/shm (never the lane), committed there
with a sandbox identity, and scored with the lane's frozen counter at the sandbox HEAD.
Writes one receipt line per control to --out and exits 0 only when every control's
observed verdict equals its expected verdict.
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "b4e47e980bfb0cbc8a4e788f59a41db858751fd8"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge"
FETCH = ".ufo/waves/round-37/fetch"
C1 = "/dev/shm/mado37-MutC1Clauses/force-b/c1.py"
C2 = os.path.join(LANE, "quality/counters/c2-r37-eventq.py")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_AUTHOR_NAME="sandbox", GIT_AUTHOR_EMAIL="sandbox@invalid",
           GIT_COMMITTER_NAME="sandbox", GIT_COMMITTER_EMAIL="sandbox@invalid")
E1 = "corpus/knowledge/event-delivery-limits-r26.md"
E2 = "corpus/knowledge/event-queue-observability-r37.md"
QUOTES = {
    "S189": "const size_t MAX_QUEUED_EVENTS = 64;",
    "S201": "std::array<char, 1024> buffer;  // Hyprland socket2 events are max 1024 bytes",
    "S212": 'm_ipc.registerForIPC("workspacev2", this);',
    "S213": 'debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}',
    "S214": "m_logsEnabled = !*PDISABLELOGS;",
}
RECEIPT = {"S189": "S189.bin", "S201": "S201.bin", "S212": "S212.bin",
           "S213": "S213.receipt.txt", "S214": "S214.bin"}


def sh(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True)


def write(sb, rel, text, mode="w"):
    p = os.path.join(sb, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, mode) as f:
        f.write(text)


def entry(ids, tokens, stated=False):
    evidence = "".join(f"**OBS** {i}: `{QUOTES[i]}`\n" for i in ids) if stated else ""
    return (f"# synthetic control entry\n\nsource: {', '.join(ids)}\nverified-at: 2026-10-25\n"
            f"recheck: 90d\n\nbody naming {' and '.join(tokens)}.\n{evidence}")


def row(i, used_by, status="mined"):
    return (f"| {i} | control source {i} — https://example.invalid/{i} | code | A | scope | anchor | "
            f"teaches | {status} | 2026-10-25 | 90d | {used_by} |\n")


def wire(sb, e1_ids=("S189", "S201", "S212"), e2_ids=("S213", "S214"), quote=None,
         digest=None, readme=True, status="mined", stated=True):
    os.makedirs(os.path.join(sb, FETCH), exist_ok=True)
    for rel in RECEIPT.values():
        shutil.copy(os.path.join(LANE, FETCH, rel), os.path.join(sb, FETCH, rel))
    write(sb, E1, entry(e1_ids, ["MAX_QUEUED_EVENTS", "overflowed event queue"], stated))
    write(sb, E2, entry(e2_ids, ["debug:disable_logs", "m_logsEnabled"], stated))
    src = open(os.path.join(sb, "corpus/SOURCES.md")).read()
    users = {}
    for i in e1_ids:
        users.setdefault(i, []).append(E1)
    for i in e2_ids:
        users.setdefault(i, []).append(E2)
    rows = "".join(row(i, ", ".join(u), status) for i, u in sorted(users.items()))
    head, tail = src.split("\n## Paths", 1)
    write(sb, "corpus/SOURCES.md", head.rstrip("\n") + "\n" + rows + "\n## Paths" + tail)
    gate = []
    for i in sorted(users):
        blob = open(os.path.join(sb, FETCH, RECEIPT[i]), "rb").read()
        d = digest or hashlib.sha256(blob).hexdigest()
        q = quote or QUOTES[i]
        gate.append(f'GATE {i} receipt={FETCH}/{RECEIPT[i]} sha256={d} quote="{q}"')
    write(sb, "corpus/lessons/round-37.md", "# round 37 control\n\n## Gate\n\n" + "\n".join(gate) + "\n")
    if readme:
        rd = open(os.path.join(sb, "corpus/README.md")).read()
        add = (f"| `knowledge/{E1.rsplit('/', 1)[1]}` (control) | x | y |\n"
               f"| `knowledge/{E2.rsplit('/', 1)[1]}` (control) | x | y |\n")
        head, tail = rd.split("\n## Quality bar", 1)
        write(sb, "corpus/README.md", head.rstrip("\n") + "\n" + add + "\n## Quality bar" + tail)


def package_copy(sb):
    shutil.copy(os.path.join(PKG, "event-delivery-limits-r26.md"), os.path.join(sb, E1))
    shutil.copy(os.path.join(PKG, "event-queue-host-measurement-r28.md"), os.path.join(sb, E2))
    rd = open(os.path.join(sb, "corpus/README.md")).read()
    head, tail = rd.split("\n## Quality bar", 1)
    add = "| `knowledge/event-delivery-limits-r26.md` | x | y |\n| `knowledge/event-queue-observability-r37.md` | x | y |\n"
    write(sb, "corpus/README.md", head.rstrip("\n") + "\n" + add + "\n## Quality bar" + tail)


STUB_CLEAN = '''import sys
print("MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 peer_recv_q=0 server_send_q=0")
print("MADO_EVENTQ_CLIENT: comm=socat pid=2293 fd=5 peer_recv_q=0 server_send_q=0")
print("MADO_EVENTQ: socket2=/x subscribers=2 overflow=0 write_fail=0 lagging=0 missing_client=- markers_observable=yes verdict=CLEAN")
sys.exit(0)
'''
STUB_GREP = '''import sys, re
a = sys.argv
log = open(a[a.index("--log") + 1]).read()
n = len(re.findall(r"overflowed event queue", log))
print(f"MADO_EVENTQ: socket2=/x subscribers=0 overflow={n} write_fail=0 lagging=0 missing_client=- markers_observable=yes verdict={'MARKERS' if n else 'CLEAN'}")
sys.exit(1 if n else 0)
'''
STUB_SOCKET = "import socket\n" + STUB_CLEAN

CONTROLS = [
    ("c1-do-nothing", C1, lambda sb: None, "TARGET_MISSED"),
    ("c1-package-copy", C1, package_copy, "TARGET_MISSED"),
    ("c1-junk-quotes", C1, lambda sb: wire(sb, quote="a fabricated quote that appears in no receipt"), "TARGET_MISSED"),
    ("c1-wrong-digest", C1, lambda sb: wire(sb, digest="0" * 64), "TARGET_MISSED"),
    ("c1-token-ungrounded", C1, lambda sb: wire(sb, e2_ids=("S213",)), "TARGET_MISSED"),
    ("c1-unindexed", C1, lambda sb: wire(sb, readme=False), "TARGET_MISSED"),
    ("c1-not-mined", C1, lambda sb: wire(sb, status="queued"), "TARGET_MISSED"),
    ("c1-token-stub", C1, lambda sb: wire(sb, stated=False), "TARGET_MISSED"),
    ("c1-golden-v2", C1, wire, "TARGET_MET"),
    ("c2-do-nothing", C2, lambda sb: None, "TARGET_MISSED"),
    ("c2-stub-clean", C2, lambda sb: write(sb, "tools/mado-eventq.py", STUB_CLEAN), "TARGET_MISSED"),
    ("c2-stub-grep", C2, lambda sb: write(sb, "tools/mado-eventq.py", STUB_GREP), "TARGET_MISSED"),
    ("c2-stub-socket", C2, lambda sb: write(sb, "tools/mado-eventq.py", STUB_SOCKET), "TARGET_MISSED"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = tempfile.mkdtemp(prefix="mado-r37-controls-", dir="/dev/shm")
    lines, bad = [], 0
    try:
        for name, counter, build, want in CONTROLS:
            sb = os.path.join(root, name)
            sh("git", "clone", "-q", "--no-local", LANE, sb)
            sh("git", "-C", sb, "checkout", "-q", "--detach", BASE)
            build(sb)
            sh("git", "-C", sb, "add", "-A")
            sh("git", "-C", sb, "commit", "-q", "--allow-empty", "-m", f"control {name}")
            p = subprocess.run([sys.executable, "-I", counter, "--repo", sb, "--rev", "HEAD"]
                               + (["--base", BASE] if counter == C1 else []),
                               capture_output=True, text=True, env=ENV)
            summary = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr.strip()[-200:]
            got = "TARGET_MET" if "verdict=TARGET_MET" in summary else "TARGET_MISSED"
            ok = got == want and p.returncode == (0 if want == "TARGET_MET" else 1)
            bad += not ok
            lines.append(f"control={name} expect={want} rc={p.returncode} ok={int(ok)} :: {summary}")
            for detail in p.stdout.strip().splitlines()[:-1]:
                lines.append(f"  {detail}")
    finally:
        shutil.rmtree(root, ignore_errors=True)
    lines.append(f"controls={len(CONTROLS)} correct={len(CONTROLS) - bad}/{len(CONTROLS)}")
    with open(a.out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
