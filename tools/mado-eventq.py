#!/usr/bin/env python3
"""mado-eventq — read-only census of Hyprland event-socket (socket2) subscribers.

Purpose
    Answer "who is subscribed to the compositor's event socket, is any of them
    falling behind, and did the compositor drop anyone?" without touching the
    socket. Subscribers come from the kernel's unix-socket table (`ss -xpa`);
    drops come from the two failure markers in the session log and the
    compositor unit journal; `debug:disable_logs` says whether those markers
    could have been written at all.

What the compositor does to a slow reader (Hyprland v0.56.2 EventManager.cpp, S189)
    Every event is appended to a per-client in-process queue and flushed with a
    non-blocking write. A short write keeps its offset and resumes when the fd
    is writable again; EAGAIN leaves the event queued. When a client already
    holds MAX_QUEUED_EVENTS = 64 queued events, the next event removes it:
        :175  ERR  "Socket2 fd N overflowed event queue, removing"
    Any other write error (or a zero-byte write) removes it too:
        :155  ERR  "Socket2 fd N failed writing event: <strerror>"
    N is the compositor-side fd (the server row's fd), not the client's.
    The in-process queue is invisible to `ss`; it only grows once the kernel
    buffer below is full, so a non-zero backlog is the early warning and a
    marker is the removal itself. Lines that merely mention the words never
    count: only the exact marker shapes above are matched.

Marker observability
    Both markers are core-logger lines. With `debug:disable_logs = 1` the core
    logger returns before writing (S214 Logger.cpp:15-16, :48), so a zero count
    then means "not logged", not "never overflowed": markers_observable=no.
    It is `unknown` when the live getoption read fails. The summary sums the
    log and journal counts; with debug:enable_stdout_logs = 1 one event can
    appear in both channels.

`ss -xpa` columns
    Netid State Recv-Q Send-Q LocalAddr LocalInode PeerAddr PeerInode [users:((...))]
    A server row has LocalAddr == the socket2 path (one LISTEN row, one ESTAB
    row per subscriber). A server ESTAB row's PeerInode is the client row's
    LocalInode; the client row's users:(("comm",pid=P,fd=F)) names the
    subscriber. For a unix stream ESTAB row Recv-Q is bytes queued to that
    socket and not yet read, Send-Q is bytes it sent that the peer has not
    consumed. Reported per subscriber:
        peer_recv_q    client row Recv-Q — bytes the subscriber has not read
        server_send_q  server row Send-Q — the same backlog seen from Hyprland
    lagging counts subscribers with peer_recv_q > 0. Rows on `.socket.sock`
    (the request socket) and unrelated sockets never count.

Output
    MADO_EVENTQ_CLIENT: comm= pid= fd= peer_recv_q= server_send_q= server_fd=
    MADO_EVENTQ_MARKERS: source=log:<path>|journal overflow= write_fail= fds=
    MADO_EVENTQ: socket2= subscribers= overflow= write_fail= lagging=
                 missing_client= markers_observable= verdict=
    One CLIENT line per server ESTAB row; when several processes hold the
    client fd the first users: entry is named. Whitespace in a comm is shown
    as `_`; `-` marks a value whose row is absent (client exited mid-read).

Exit map
    0  verdict=CLEAN
    1  verdict=MARKERS (any marker; takes precedence) or verdict=MISSING_CLIENT
       (an --expect-client comm has no subscriber)
    2  `MADO_EVENTQ: SETUP <reason>` and no verdict: ss_unparseable,
       socket2_not_listening, socket2_ambiguous, no_instance, ss_failed, ss_unreadable,
       log_unreadable, journal_unreadable, snapshot_unwritable

Live defaults (each replaced by its flag)
    --ss-file        `ss -xpa`
    --log            $XDG_RUNTIME_DIR/hypr/<instance>/hyprland.log, instance =
                     $HYPRLAND_INSTANCE_SIGNATURE or the single directory there
    --journal-file   `journalctl --user -u wayland-wm@hyprland.desktop.service
                     --no-pager -q -o cat`
    --disable-logs   `hyprctl getoption debug:disable_logs -j`
    --socket2        live: <instance dir>/.socket2.sock; with --ss-file: the
                     LISTEN row whose LocalAddr ends in /.socket2.sock
    --snapshot-out   writes the ss header plus exactly the rows used (socket2
                     LISTEN row, its ESTAB rows, their peer rows) so the file
                     replays through --ss-file to the same clients.

Read-only guarantee
    Python stdlib only, no socket module, never opens any socket. The only
    subprocesses are the three read verbs above, and only for inputs not given
    by flag. Files are opened for reading, except the --snapshot-out target.
    No journal or log line is printed; only counts and fds.
"""
import argparse
import json
import os
import re
import subprocess
import sys

TAG = "MADO_EVENTQ"
UNIT = "wayland-wm@hyprland.desktop.service"
OVERFLOW = re.compile(r"Socket2 fd (\d+) overflowed event queue, removing")
WRITE_FAIL = re.compile(r"Socket2 fd (\d+) failed writing event")
HOLDER = re.compile(r'\("((?:[^"\\]|\\.)*)",pid=(\d+),fd=(\d+)\)')
LIVE_TIMEOUT = 90


class Setup(Exception):
    pass


def run(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, errors="replace",
                           timeout=LIVE_TIMEOUT, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return p.stdout if p.returncode == 0 else None


def read_text(path, reason):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        raise Setup(f"{reason} path={path}")


def instance_dir():
    base = os.path.join(os.environ.get("XDG_RUNTIME_DIR", ""), "hypr")
    sig = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    if sig:
        d = os.path.join(base, sig)
        if os.path.isdir(d):
            return d
        raise Setup(f"no_instance dir={d}")
    try:
        dirs = [e.path for e in os.scandir(base) if e.is_dir()]
    except OSError:
        dirs = []
    if len(dirs) != 1:
        raise Setup(f"no_instance candidates={len(dirs)}")
    return dirs[0]


def parse_row(line):
    """Split one ss row; None when it is not a socket row."""
    head, sep, users = line.partition(" users:(")
    t = head.split()
    if len(t) < 8 or not (t[2].isdigit() and t[3].isdigit() and t[-3].isdigit() and t[-1].isdigit()):
        return None
    return dict(state=t[1], recv_q=int(t[2]), send_q=int(t[3]), local=" ".join(t[4:-3]),
                inode=t[-3], peer_inode=t[-1],
                holders=HOLDER.findall(users) if sep else [], raw=line)


def parse_ss(text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.lstrip().startswith("Netid"):
            rows = [r for r in map(parse_row, lines[i + 1:]) if r]
            return line, rows
    raise Setup("ss_unparseable")


def census(rows, sock):
    if sock is None:
        found = sorted({r["local"] for r in rows
                        if r["state"] == "LISTEN" and r["local"].endswith("/.socket2.sock")})
        if not found:
            raise Setup("socket2_not_listening")
        if len(found) > 1:
            raise Setup(f"socket2_ambiguous candidates={len(found)}")
        sock = found[0]
    listen = [r for r in rows if r["local"] == sock and r["state"] == "LISTEN"]
    server = [r for r in rows if r["local"] == sock and r["state"] == "ESTAB"]
    if not listen and not server:
        raise Setup(f"socket2_not_listening socket2={sock}")
    by_inode = {}
    for r in rows:
        by_inode.setdefault(r["inode"], r)
    clients, used = [], listen + server
    for s in server:
        peer = by_inode.get(s["peer_inode"])
        if peer is not None and peer["local"] != sock:
            used.append(peer)
        else:
            peer = None
        holder = peer["holders"][0] if peer and peer["holders"] else ("-", "-", "-")
        clients.append(dict(comm=re.sub(r"\s", "_", holder[0]) or "-", pid=holder[1], fd=holder[2],
                            peer_recv_q=peer["recv_q"] if peer else "-",
                            server_send_q=s["send_q"],
                            server_fd=",".join(h[2] for h in s["holders"]) or "-"))
    return sock, clients, used


def count_markers(text):
    ov, wf = [], []
    for line in text.splitlines():
        m = OVERFLOW.search(line)
        if m:
            ov.append(m.group(1))
        m = WRITE_FAIL.search(line)
        if m:
            wf.append(m.group(1))
    return ov, wf


def disable_logs_live():
    out = run(["hyprctl", "getoption", "debug:disable_logs", "-j"])
    try:
        v = json.loads(out)["int"]
    except (TypeError, ValueError, KeyError):
        return None
    return v if v in (0, 1) else None


def main(argv):
    ap = argparse.ArgumentParser(description="Read-only Hyprland socket2 subscriber census.")
    ap.add_argument("--ss-file")
    ap.add_argument("--log", action="append")
    ap.add_argument("--journal-file")
    ap.add_argument("--disable-logs", choices=("0", "1"))
    ap.add_argument("--expect-client", action="append", default=[])
    ap.add_argument("--socket2")
    ap.add_argument("--snapshot-out")
    a = ap.parse_args(argv)

    live_ss = a.ss_file is None
    if live_ss:
        text = run(["ss", "-xpa"])
        if text is None:
            raise Setup("ss_failed")
    else:
        text = read_text(a.ss_file, "ss_unreadable")
    header, rows = parse_ss(text)
    sock = a.socket2
    if sock is None and live_ss:
        sock = os.path.join(instance_dir(), ".socket2.sock")
    sock, clients, used = census(rows, sock)

    logs = a.log
    if logs is None:
        d = instance_dir()
        logs = [os.path.join(d, "hyprland.log")]
        if not os.path.exists(logs[0]) and os.path.exists(os.path.join(d, "hyprlandd.log")):
            logs = [os.path.join(d, "hyprlandd.log")]
    channels = [(f"log:{p}", read_text(p, "log_unreadable")) for p in logs]
    if a.journal_file is not None:
        journal = read_text(a.journal_file, "journal_unreadable")
    else:
        journal = run(["journalctl", "--user", "-u", UNIT, "--no-pager", "-q", "-o", "cat"])
        if journal is None:
            raise Setup("journal_unreadable")
    channels.append(("journal", journal))

    dl = int(a.disable_logs) if a.disable_logs is not None else disable_logs_live()
    observable = {0: "yes", 1: "no"}.get(dl, "unknown")

    if a.snapshot_out:
        try:
            with open(a.snapshot_out, "w", encoding="utf-8") as f:
                f.write(header + "\n" + "".join(r["raw"] + "\n" for r in used))
        except OSError:
            raise Setup(f"snapshot_unwritable path={a.snapshot_out}")

    out = []
    for c in clients:
        out.append(f"{TAG}_CLIENT: comm={c['comm']} pid={c['pid']} fd={c['fd']} "
                   f"peer_recv_q={c['peer_recv_q']} server_send_q={c['server_send_q']} "
                   f"server_fd={c['server_fd']}")
    overflow = write_fail = 0
    for source, body in channels:
        ov, wf = count_markers(body)
        overflow += len(ov)
        write_fail += len(wf)
        out.append(f"{TAG}_MARKERS: source={source} overflow={len(ov)} write_fail={len(wf)} "
                   f"fds={','.join(ov + wf) or '-'}")
    comms = {c["comm"] for c in clients}
    missing = [e for e in dict.fromkeys(a.expect_client) if e not in comms and re.sub(r"\s", "_", e) not in comms]
    lagging = sum(1 for c in clients if isinstance(c["peer_recv_q"], int) and c["peer_recv_q"] > 0)
    verdict = "MARKERS" if overflow or write_fail else "MISSING_CLIENT" if missing else "CLEAN"
    out.append(f"{TAG}: socket2={sock} subscribers={len(clients)} overflow={overflow} "
               f"write_fail={write_fail} lagging={lagging} missing_client={','.join(missing) or '-'} "
               f"markers_observable={observable} verdict={verdict}")
    print("\n".join(out))
    return 0 if verdict == "CLEAN" else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Setup as e:
        print(f"{TAG}: SETUP {e}")
        sys.exit(2)
