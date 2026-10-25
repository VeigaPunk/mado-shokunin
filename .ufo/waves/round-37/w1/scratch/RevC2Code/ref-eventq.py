#!/usr/bin/env python3
"""Scratch reference census used only to probe the C2 counter (RevC2Code)."""
import argparse
import re
import sys

USERS = re.compile(r'\("((?:[^"\\]|\\.)*)",pid=(\d+),fd=(\d+)\)')
OVER = re.compile(r"Socket2 fd \d+ overflowed event queue, removing")
FAIL = re.compile(r"Socket2 fd \d+ failed writing event")


def setup(reason):
    print(f"MADO_EVENTQ: SETUP {reason}")
    return 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ss-file", required=True)
    ap.add_argument("--log", action="append", default=[])
    ap.add_argument("--journal-file")
    ap.add_argument("--disable-logs", choices=("0", "1"), required=True)
    ap.add_argument("--expect-client", action="append", default=[])
    ap.add_argument("--socket2")
    a = ap.parse_args()
    lines = open(a.ss_file, encoding="utf-8", errors="replace").read().splitlines()
    if not lines or not lines[0].startswith("Netid"):
        return setup("unparseable ss output")
    rows = [l.split(None, 8) for l in lines[1:] if l.strip()]
    rows = [r for r in rows if len(r) >= 8 and r[0].startswith("u_")]
    is_s2 = (lambda p: p == a.socket2) if a.socket2 else (lambda p: "/hypr/" in p and p.endswith("/.socket2.sock"))
    listen = [r for r in rows if r[1] == "LISTEN" and is_s2(r[4])]
    if not listen:
        return setup("socket2 not listening")
    by_inode = {r[5]: r for r in rows}  # PASS_MARKER
    clients = []
    for r in rows:
        if r[1] == "ESTAB" and is_s2(r[4]):
            peer = by_inode.get(r[7])
            u = USERS.search(peer[8]) if peer and len(peer) > 8 else None
            comm, pid, fd = u.groups() if u else ("?", "?", "?")
            clients.append((comm, pid, fd, peer[2] if peer else "?", r[3]))
    lagging = sum(1 for c in clients if c[3] not in ("0", "?"))  # LAG_MARKER
    totals = [0, 0]
    for src, path in [(f"log:{p}", p) for p in a.log] + ([("journal", a.journal_file)] if a.journal_file else []):
        text = open(path, encoding="utf-8", errors="replace").read().splitlines()
        o = sum(1 for l in text if OVER.search(l))
        w = sum(1 for l in text if FAIL.search(l))
        totals[0] += o
        totals[1] += w
        print(f"MADO_EVENTQ_MARKERS: source={src} overflow={o} write_fail={w}")
    for c in clients:
        print(f"MADO_EVENTQ_CLIENT: comm={c[0]} pid={c[1]} fd={c[2]} peer_recv_q={c[3]} server_send_q={c[4]}")
    comms = {c[0] for c in clients}
    missing = [e for e in a.expect_client if e not in comms]  # MISS_MARKER
    verdict = "MARKERS" if any(totals) else "MISSING_CLIENT" if missing else "CLEAN"
    print(f"MADO_EVENTQ: socket2={listen[0][4]} subscribers={len(clients)} overflow={totals[0]} "
          f"write_fail={totals[1]} lagging={lagging} missing_client={','.join(missing) or '-'} "
          f"markers_observable={'no' if a.disable_logs == '1' else 'yes'} verdict={verdict}")
    return 0 if verdict == "CLEAN" else 1


if __name__ == "__main__":
    sys.exit(main())
