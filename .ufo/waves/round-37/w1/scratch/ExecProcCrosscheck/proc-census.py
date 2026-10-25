#!/usr/bin/env python3
"""Read-only /proc census of Hyprland event-socket (.socket2.sock) connections.

Sources: /proc/net/unix (inode, flags, type, state, path) and /proc/<pid>/fd
symlinks (`socket:[inode]`). No socket of any family is created or connected.

/proc/net/unix carries no peer inode, so this census can prove the SERVER side
(listener + accepted sockets bound to the socket2 path, and which pid/fds hold
them) but cannot, on its own, name the client end of each connection. An
optional `ss -xpa` capture (--ss FILE) supplies peer inodes (kernel sock_diag
UNIX_DIAG_PEER); every ss claim is then re-checked against the /proc tables.

Usage: proc-census.py [--instance SIG] [--ss FILE]
"""

import argparse
import os
import re
import sys

SO_ACCEPTCON = 0x00010000
SOCK_STREAM = 0x0001
SS_CONNECTED = 0x03
SS_UNCONNECTED = 0x01


def read_unix_table():
    rows = {}
    with open("/proc/net/unix") as f:
        next(f)
        for line in f:
            parts = line.rstrip("\n").split(None, 7)
            if len(parts) < 7:
                continue
            inode = int(parts[6])
            rows[inode] = {
                "flags": int(parts[3], 16),
                "type": int(parts[4], 16),
                "st": int(parts[5], 16),
                "path": parts[7] if len(parts) > 7 else None,
            }
    return rows


def scan_fds():
    holders = {}
    comms = {}
    uids = {}
    unreadable = []
    vanished = 0
    for name in os.listdir("/proc"):
        if not name.isdigit():
            continue
        pid = int(name)
        fd_dir = f"/proc/{pid}/fd"
        try:
            fds = os.listdir(fd_dir)
        except PermissionError:
            unreadable.append(pid)
            continue
        except (FileNotFoundError, ProcessLookupError):
            vanished += 1
            continue
        try:
            with open(f"/proc/{pid}/comm") as f:
                comms[pid] = f.read().strip()
            with open(f"/proc/{pid}/status") as f:
                for line in f:
                    if line.startswith("Uid:"):
                        uids[pid] = int(line.split()[1])
                        break
        except (FileNotFoundError, ProcessLookupError):
            vanished += 1
            continue
        for fd in fds:
            try:
                target = os.readlink(f"{fd_dir}/{fd}")
            except OSError:
                continue
            if target.startswith("socket:["):
                holders.setdefault(int(target[8:-1]), []).append((pid, int(fd)))
    return holders, comms, uids, unreadable, vanished


def cmdline_mentions(pid, needle):
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            return needle.encode() in f.read()
    except OSError:
        return False


SS_LINE = re.compile(
    r"^u_str\s+(\S+)\s+\d+\s+\d+\s+(.+?)\s+(\d+)\s+(\S+)\s+(\d+)(?:\s+users:\((.*)\))?\s*$"
)
SS_USER = re.compile(r'\("([^"]*)",pid=(\d+),fd=(\d+)\)')


def read_ss(path):
    by_inode = {}
    with open(path) as f:
        for line in f:
            m = SS_LINE.match(line.rstrip("\n"))
            if not m:
                continue
            state, local, inode, _peer_addr, peer, users = m.groups()
            by_inode[int(inode)] = {
                "state": state,
                "local": None if local == "*" else local,
                "peer": int(peer),
                "users": sorted(
                    (int(p), int(fd), c) for c, p, fd in SS_USER.findall(users or "")
                ),
            }
    return by_inode


def fmt_holders(hs, comms):
    return ", ".join(f"{comms.get(p, '?')}/{p}/fd{fd}" for p, fd in sorted(hs)) or "none"


def census(instance, runtime, rows, holders, comms, uids, ss):
    path = f"{runtime}/hypr/{instance}/.socket2.sock"
    tag = f"HYPR/{instance[:8]}…/.socket2.sock"
    print(f"\n## instance {instance[:8]}… path {tag}")
    try:
        dir_uid = os.stat(f"{runtime}/hypr/{instance}").st_uid
    except OSError:
        dir_uid = None

    bound = {i: r for i, r in rows.items() if r["path"] == path}
    listeners = sorted(i for i, r in bound.items() if r["flags"] & SO_ACCEPTCON)
    accepted = sorted(
        i for i, r in bound.items()
        if not r["flags"] & SO_ACCEPTCON and r["st"] == SS_CONNECTED
    )
    other = sorted(set(bound) - set(listeners) - set(accepted))
    print(f"listener inodes: {listeners}  accepted (St=03) inodes: {accepted}  other: {other}")

    compositor = sorted({p for i in listeners for p, _ in holders.get(i, [])})
    for i in listeners:
        print(f"  listener {i}: held by {fmt_holders(holders.get(i, []), comms)}")
    print(f"compositor pid(s) (hold the listener): {compositor}")

    proof_ok = True
    for i in accepted:
        hs = holders.get(i, [])
        foreign = [h for h in hs if h[0] not in compositor]
        if foreign or not hs:
            proof_ok = False
        print(
            f"  accepted {i}: held by {fmt_holders(hs, comms)}"
            f"{'  FOREIGN-HOLDER' if foreign else ''}{'  UNHELD' if not hs else ''}"
        )
    print(f"PROC-PROVES: {len(accepted)} live accepted connection(s), all held only by the compositor: {proof_ok}")

    candidates = sorted(
        i for i, r in rows.items()
        if r["path"] is None and r["type"] == SOCK_STREAM and r["st"] == SS_CONNECTED
        and holders.get(i) and any(p not in compositor for p, _ in holders[i])
    )
    reachable = [
        i for i in candidates
        if any(uids.get(p) in (dir_uid, 0) for p, _ in holders[i] if p not in compositor)
    ]
    print(
        f"client-end candidates (unbound, stream, St=03, held outside compositor): {len(candidates)}; "
        f"after uid filter (uid {dir_uid} or 0, socket dir is 0700): {len(reachable)}"
    )
    cand_set = set(reachable)
    unheld = sum(
        1 for i, r in rows.items()
        if r["path"] is None and r["type"] == SOCK_STREAM and r["st"] == SS_CONNECTED and not holders.get(i)
    )
    print(f"unbound stream St=03 rows with no visible fd holder (unreadable pid or in-flight fd): {unheld}")

    print("heuristic H1 (nearest candidate inode to each server inode) — NOT a proof:")
    h1 = {}
    for i in accepted:
        if reachable:
            near = min(reachable, key=lambda c: abs(c - i))
            h1[i] = near
            print(f"  server {i} -> nearest {near} (|d|={abs(near - i)}) {fmt_holders(holders[near], comms)}")
    mentions = sorted({
        p for i in reachable for p, _ in holders[i]
        if p not in compositor and cmdline_mentions(p, ".socket2.sock")
    })
    print(
        "heuristic H2 (candidate holders whose cmdline names .socket2.sock) — NOT a proof: "
        + (", ".join(f"{comms.get(p, '?')}/{p}" for p in mentions) or "none")
    )

    if ss is None:
        print("no --ss capture: client ends left unpaired (see module docstring)")
        return proof_ok

    print("ss -xpa cross-check (peer inode from sock_diag; holders re-derived from /proc):")
    ss_server = sorted(i for i, e in ss.items() if e["local"] == path and e["state"] == "ESTAB")
    ss_listen = sorted(i for i, e in ss.items() if e["local"] == path and e["state"] == "LISTEN")
    agree_sets = ss_server == accepted and ss_listen == listeners
    print(f"  server inode set: ss ESTAB {ss_server} LISTEN {ss_listen} vs proc {accepted} {listeners} -> {'AGREE' if agree_sets else 'DISAGREE'}")
    all_ok = agree_sets and proof_ok
    for i in ss_server:
        e = ss[i]
        peer = e["peer"]
        proc_srv = sorted(holders.get(i, []))
        ss_srv = [(p, fd) for p, fd, _ in e["users"]]
        srv_ok = proc_srv == ss_srv
        proc_cli = sorted(holders.get(peer, []))
        pe = ss.get(peer)
        ss_cli = [(p, fd) for p, fd, _ in pe["users"]] if pe else None
        back = pe is not None and pe["peer"] == i
        in_cand = peer in cand_set
        cli_ok = ss_cli == proc_cli and back and in_cand
        row = rows.get(peer)
        row_ok = row is not None and row["path"] is None and row["st"] == SS_CONNECTED and row["type"] == SOCK_STREAM
        verdict = "AGREE" if srv_ok and cli_ok and row_ok else "DISAGREE"
        all_ok &= verdict == "AGREE"
        print(
            f"  subscriber peer={peer}: client {fmt_holders(proc_cli, comms)} | server {i} {fmt_holders(proc_srv, comms)}\n"
            f"    server-holders proc==ss: {srv_ok}; client-holders proc==ss: {ss_cli == proc_cli}; "
            f"ss peer links back: {back}; peer row in /proc/net/unix unbound+stream+St03: {row_ok}; "
            f"peer in /proc candidate set: {in_cand}; H1 picks it: {h1.get(i) == peer}; "
            f"H2 names its pid: {any(p in mentions for p, _ in proc_cli)} -> {verdict}"
        )
    return all_ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", default=None)
    ap.add_argument("--ss", default=None)
    a = ap.parse_args()
    runtime = os.environ.get("XDG_RUNTIME_DIR") or f"/run/user/{os.getuid()}"
    if a.instance:
        instances = [a.instance]
    else:
        try:
            instances = sorted(os.listdir(f"{runtime}/hypr"))
        except OSError:
            instances = []

    rows = read_unix_table()
    holders, comms, uids, unreadable, vanished = scan_fds()
    rows2 = read_unix_table()
    ss = read_ss(a.ss) if a.ss else None

    s2 = lambda rs: {i: r for i, r in rs.items() if r["path"] and r["path"].endswith("/.socket2.sock")}
    stable = s2(rows) == s2(rows2)
    print("# proc-census (read-only: /proc/net/unix + /proc/*/fd; no socket opened)")
    print(f"/proc/net/unix rows: {len(rows)}; socket inodes mapped to fds: {len(holders)}; "
          f"pids with unreadable fd dir: {len(unreadable)}; pids vanished mid-scan: {vanished}")
    print(f"socket2 rows identical before/after fd scan: {stable}")
    if not instances:
        print("no Hyprland instance directory found")
        return 1
    ok = stable
    for inst in instances:
        ok &= census(inst, runtime, rows, holders, comms, uids, ss)
    print(f"\nOVERALL: {'AGREE' if ok else 'DISAGREE'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
