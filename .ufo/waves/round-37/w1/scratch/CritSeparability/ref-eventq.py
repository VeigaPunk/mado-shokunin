#!/usr/bin/env python3
"""CritSeparability scratch reference: a minimal census that satisfies PRED-C2-r37-v2.

Not a deliverable. Exists only so the separability probe has a C2 accept path; the
sandbox copies it to tools/mado-eventq.py. Reads ss text, never opens any socket.
"""
import argparse
import os
import re
import subprocess
import sys

ROW = re.compile(r"^u_str\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\d+)\s+(\S+)\s+(\d+)\s*(.*)$")
USER = re.compile(r'\(\("([^"]+)",pid=(\d+),fd=(\d+)\)')
OVERFLOW = re.compile(r"^ERR \]: Socket2 fd \d+ overflowed event queue, removing")
WRITEFAIL = re.compile(r"^ERR \]: Socket2 fd \d+ failed writing event: ")


def setup(reason):
    print(f"MADO_EVENTQ: SETUP {reason}")
    sys.exit(2)


def read(path):
    try:
        with open(path, errors="replace") as f:
            return f.read()
    except OSError as e:
        setup(f"unreadable {path}: {e.strerror}")


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        setup(f"command failed: {' '.join(cmd)}")
    return p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ss-file")
    ap.add_argument("--log", action="append")
    ap.add_argument("--journal-file")
    ap.add_argument("--disable-logs", choices=["0", "1"])
    ap.add_argument("--expect-client", action="append", default=[])
    ap.add_argument("--socket2")
    a = ap.parse_args()

    text = read(a.ss_file) if a.ss_file else run(["ss", "-xpa"])
    lines = text.splitlines()
    if not lines or not lines[0].startswith("Netid"):
        setup("unparseable ss output")
    rows = [m.groups() for m in map(ROW.match, lines[1:]) if m]
    sock2 = a.socket2 or next((r[3] for r in rows if r[0] == "LISTEN" and r[3].endswith("/.socket2.sock")), None)
    if not sock2 or not any(r[0] == "LISTEN" and r[3] == sock2 for r in rows):
        setup("socket2 not listening")
    by_inode = {r[4]: r for r in rows}
    clients = []
    for r in rows:
        if r[0] != "ESTAB" or r[3] != sock2:
            continue
        peer = by_inode.get(r[6])
        u = USER.search(peer[7]) if peer else None
        if not u:
            continue
        clients.append((u.group(1), u.group(2), u.group(3), int(peer[1]), int(r[2])))

    logs = a.log or []
    if not a.log and not a.ss_file:
        rt = os.environ.get("XDG_RUNTIME_DIR", "")
        inst = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE", "")
        logs = [os.path.join(rt, "hypr", inst, "hyprland.log")]
    channels = [(f"log:{p}" if len(logs) > 1 else "log", read(p)) for p in logs]
    if a.journal_file:
        channels.append(("journal", read(a.journal_file)))
    elif not a.ss_file:
        channels.append(("journal", run(["journalctl", "--user", "-u", "wayland-wm@hyprland.desktop.service",
                                         "--no-pager", "-q", "-o", "cat"])))
    dl = a.disable_logs
    if dl is None:
        dl = "1" if '"int":1' in run(["hyprctl", "getoption", "debug:disable_logs", "-j"]).replace(" ", "") else "0"

    total_o = total_w = 0
    for comm, pid, fd, rq, sq in clients:
        print(f"MADO_EVENTQ_CLIENT: comm={comm} pid={pid} fd={fd} peer_recv_q={rq} server_send_q={sq}")
    for src, body in channels:
        o = sum(bool(OVERFLOW.match(l)) for l in body.splitlines())
        w = sum(bool(WRITEFAIL.match(l)) for l in body.splitlines())
        total_o, total_w = total_o + o, total_w + w
        print(f"MADO_EVENTQ_MARKERS: source={src} overflow={o} write_fail={w}")
    comms = {c[0] for c in clients}
    missing = [c for c in a.expect_client if c not in comms]
    lagging = sum(c[3] > 0 for c in clients)
    verdict = "MARKERS" if total_o + total_w else ("MISSING_CLIENT" if missing else "CLEAN")
    print(f"MADO_EVENTQ: socket2={sock2} subscribers={len(clients)} overflow={total_o} write_fail={total_w} "
          f"lagging={lagging} missing_client={','.join(missing) or '-'} "
          f"markers_observable={'no' if dl == '1' else 'yes'} verdict={verdict}")
    return 0 if verdict == "CLEAN" else 1


if __name__ == "__main__":
    sys.exit(main())
