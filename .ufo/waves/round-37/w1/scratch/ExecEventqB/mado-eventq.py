#!/usr/bin/env python3
"""mado-eventq — read-only census of Hyprland's event socket (socket2) subscribers.

Purpose
  Answer "who is subscribed to the compositor's event socket, is any of them
  falling behind, and has the compositor dropped one?" without touching the
  socket. It reads the kernel's unix-socket table (`ss -xpa`), the session log
  and the compositor unit journal, and whether those logs can carry markers at
  all (`debug:disable_logs`).

The rule being watched (Hyprland v0.56.2 src/managers/EventManager.cpp, S189)
  Each subscriber has an in-compositor queue of formatted events. postEvent()
  appends to every queue and flushes with a non-blocking write(); EAGAIN keeps
  the rest queued and arms WL_EVENT_WRITABLE. The cap is MAX_QUEUED_EVENTS = 64
  (:169): when a queue already holds 64 events at the next postEvent(), the
  compositor logs `Socket2 fd N overflowed event queue, removing` (:175) and
  drops the subscriber. Any other write error logs `Socket2 fd N failed
  writing event: <reason>` (:155) and drops it too. The 64-event queue lives in
  compositor memory and is invisible here; what is visible is the kernel buffer
  in front of it: a subscriber that stops reading first fills its receive
  queue (peer_recv_q grows), then write() starts returning EAGAIN, then the
  userland queue grows to the cap and the subscriber disappears from the table.
  Markers are counted only when a line carries the exact message; prose that
  merely mentions the words does not count.

  Caveat (Logger.cpp:15-16, S214): with `debug:disable_logs` = 1 the core logger
  returns before writing anything, so zero markers then proves nothing. That is
  what markers_observable=no says; markers_observable=unknown means the option
  could not be read.

ss -xpa columns, as parsed (one table row per socket)
  Netid State Recv-Q Send-Q LocalAddr LocalInode PeerAddr PeerInode [users:((...))]
  LISTEN row on the socket2 path: the compositor's listener (Recv-Q = pending
    accepts, Send-Q = accept backlog limit).
  Server ESTAB row: LocalAddr == socket2 path, one per subscriber connection.
    Its Send-Q is server_send_q: write memory the kernel still charges to the
    compositor's end for data the subscriber has not consumed (af_unix
    accounting includes buffer overhead, so it can exceed peer_recv_q).
  Client row: the row whose LocalInode equals the server row's PeerInode. Its
    users:(("comm",pid=N,fd=N)) names the subscriber (first tuple if several
    processes hold it; `-` when ss cannot see the owner) and its Recv-Q is
    peer_recv_q: bytes delivered to the subscriber that it has not read yet.
  Rows on the request socket (.socket.sock) and every unrelated socket are
  never counted. Whitespace inside a comm is printed as `_`.

Inputs (each defaults to the live host independently)
  --ss-file PATH        else `ss -xpa`
  --log PATH            repeatable; else $XDG_RUNTIME_DIR/hypr/<instance>/hyprland.log
  --journal-file PATH   else `journalctl --user -u wayland-wm@hyprland.desktop.service
                        --no-pager -q -o cat`
  --disable-logs 0|1    else `hyprctl getoption debug:disable_logs -j`
  --expect-client COMM  repeatable; a missing comm makes the verdict MISSING_CLIENT
  --socket2 PATH        else the single LISTEN row ending `/.socket2.sock` in
                        --ss-file, or <instance dir>/.socket2.sock when live
  --snapshot-out PATH   write the ss header plus exactly the rows the census
                        used (LISTEN row, server ESTAB rows, client rows), so
                        `--ss-file PATH` replays to the same clients
  <instance> is $HYPRLAND_INSTANCE_SIGNATURE, else the only directory under
  $XDG_RUNTIME_DIR/hypr.

Output
  MADO_EVENTQ_CLIENT: comm=<c> pid=<p> fd=<f> peer_recv_q=<n> server_send_q=<n>
  MADO_EVENTQ_MARKERS: source=log:<path> overflow=<n> write_fail=<n>   (per --log)
  MADO_EVENTQ_MARKERS: source=journal overflow=<n> write_fail=<n>
  MADO_EVENTQ: socket2=<path> subscribers=<n> overflow=<n> write_fail=<n> lagging=<n>
    missing_client=<a,b|-> markers_observable=<yes|no|unknown>
    verdict=<CLEAN|MARKERS|MISSING_CLIENT>
  overflow/write_fail in the summary are summed over every channel (a line the
  compositor echoed to both file and journal counts in both). lagging counts
  subscribers with peer_recv_q > 0.

Exit map
  0 CLEAN; 1 MARKERS (takes precedence) or MISSING_CLIENT;
  2 one line `MADO_EVENTQ: SETUP <reason> [detail]` and nothing else. Reasons:
  usage, ss_file_unreadable, ss_unavailable, ss_unparseable,
  socket2_not_listening, socket2_ambiguous, no_runtime_dir, instance_missing,
  no_instance, instance_ambiguous, log_unreadable, journal_file_unreadable,
  journal_unavailable, snapshot_unwritable.

Read-only guarantee
  Never opens, binds or talks to any socket (the socket module is not
  imported); a subscriber that stops reading is exactly what the compositor
  punishes, so the census never becomes one. Files are opened for reading
  only, except --snapshot-out. The only subprocesses are the three live reads
  above, each run only when its file flag is absent; `hyprctl getoption` is a
  read verb on the request socket, never on socket2.
"""
import argparse
import json
import os
import re
import subprocess
import sys

TAG = "MADO_EVENTQ"
SS_CMD = ["ss", "-xpa"]
JOURNAL_CMD = ["journalctl", "--user", "-u", "wayland-wm@hyprland.desktop.service",
               "--no-pager", "-q", "-o", "cat"]
GETOPT_CMD = ["hyprctl", "getoption", "debug:disable_logs", "-j"]
SOCKET2_NAME = ".socket2.sock"
LIVE_TIMEOUT = 30

SS_COLUMNS = (
    ("netid", r"\S+", str),
    ("state", r"\S+", str),
    ("recv_q", r"\d+", int),
    ("send_q", r"\d+", int),
    ("local", r".+?", str),
    ("local_inode", r"\d+", int),
    ("peer", r"\S+", str),
    ("peer_inode", r"\d+", int),
)
SS_ROW = re.compile(
    "^" + r"\s+".join(f"(?P<{name}>{pat})" for name, pat, _ in SS_COLUMNS)
    + r"(?:\s+(?P<users>users:\(.*\)))?\s*$")
SS_USER = re.compile(r'\("((?:[^"\\]|\\.)*)",pid=(\d+),fd=(\d+)\)')

MARKERS = (
    ("overflow", re.compile(r"\bSocket2 fd \d+ overflowed event queue, removing\s*$")),
    ("write_fail", re.compile(r"\bSocket2 fd \d+ failed writing event: \S")),
)
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


class Setup(Exception):
    def __init__(self, reason, detail=""):
        super().__init__(reason)
        self.line = f"{TAG}: SETUP {reason}" + (f" {detail}" if detail else "")


class Args(argparse.ArgumentParser):
    def error(self, message):
        raise Setup("usage", message.replace("\n", " "))


def parse_args(argv):
    ap = Args(description="Read-only census of Hyprland socket2 subscribers.", add_help=True)
    ap.add_argument("--ss-file")
    ap.add_argument("--log", action="append", default=[])
    ap.add_argument("--journal-file")
    ap.add_argument("--disable-logs", choices=("0", "1"))
    ap.add_argument("--expect-client", action="append", default=[])
    ap.add_argument("--socket2")
    ap.add_argument("--snapshot-out")
    return ap.parse_args(argv)


def run_live(cmd, reason):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, errors="replace",
                           timeout=LIVE_TIMEOUT, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Setup(reason, f"{cmd[0]}: {type(e).__name__}")
    if p.returncode != 0:
        raise Setup(reason, f"{cmd[0]}: rc={p.returncode}")
    return p.stdout


def read_text(path, reason):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError as e:
        raise Setup(reason, f"{path}: {e.strerror or type(e).__name__}")


def instance_dir():
    rt = os.environ.get("XDG_RUNTIME_DIR")
    if not rt:
        raise Setup("no_runtime_dir", "XDG_RUNTIME_DIR unset")
    base = os.path.join(rt, "hypr")
    sig = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    if sig:
        d = os.path.join(base, sig)
        if not os.path.isdir(d):
            raise Setup("instance_missing", d)
        return d
    try:
        dirs = sorted(e for e in os.listdir(base) if os.path.isdir(os.path.join(base, e)))
    except OSError:
        dirs = []
    if not dirs:
        raise Setup("no_instance", base)
    if len(dirs) > 1:
        raise Setup("instance_ambiguous", f"{len(dirs)} dirs under {base}")
    return os.path.join(base, dirs[0])


def parse_ss(text):
    """Return (header line, rows); a row is a dict of SS_COLUMNS plus users and raw."""
    lines = text.splitlines()
    head = next((i for i, l in enumerate(lines) if l.strip()), None)
    if head is None or not lines[head].lstrip().startswith("Netid"):
        raise Setup("ss_unparseable", "no Netid header")
    rows = []
    for raw in lines[head + 1:]:
        m = SS_ROW.match(raw.strip())
        if not m:
            continue
        row = {name: conv(m.group(name)) for name, _, conv in SS_COLUMNS}
        row["users"] = SS_USER.findall(m.group("users") or "")
        row["raw"] = raw
        row["n"] = len(rows)
        rows.append(row)
    return lines[head], rows


def find_socket2(rows):
    paths = sorted({r["local"] for r in rows
                    if r["state"] == "LISTEN" and r["local"].endswith("/" + SOCKET2_NAME)})
    if not paths:
        raise Setup("socket2_not_listening", f"no LISTEN row ending /{SOCKET2_NAME}")
    if len(paths) > 1:
        raise Setup("socket2_ambiguous", f"{len(paths)} listeners; pass --socket2")
    return paths[0]


def census(rows, sock2):
    listen = [r for r in rows if r["state"] == "LISTEN" and r["local"] == sock2]
    if not listen:
        raise Setup("socket2_not_listening", sock2)
    servers = [r for r in rows if r["state"] == "ESTAB" and r["local"] == sock2]
    by_inode = {}
    for r in rows:
        if r["local"] != sock2:
            by_inode.setdefault(r["local_inode"], r)
    clients, used = [], list(listen) + servers
    for srv in servers:
        peer = by_inode.get(srv["peer_inode"]) if srv["peer_inode"] else None
        comm = pid = fd = "-"
        recv_q = None
        if peer is not None:
            used.append(peer)
            recv_q = peer["recv_q"]
            if peer["users"]:
                c, p, f = peer["users"][0]
                comm, pid, fd = re.sub(r"\s+", "_", c) or "-", p, f
        clients.append(dict(comm=comm, pid=pid, fd=fd, peer_recv_q=recv_q,
                            server_send_q=srv["send_q"]))
    used = sorted({r["n"]: r for r in used}.values(), key=lambda r: r["n"])
    return clients, used


def count_markers(text):
    counts = {name: 0 for name, _ in MARKERS}
    for line in text.splitlines():
        line = ANSI.sub("", line)
        for name, rx in MARKERS:
            if rx.search(line):
                counts[name] += 1
    return counts


def disable_logs_live():
    try:
        p = subprocess.run(GETOPT_CMD, capture_output=True, text=True, errors="replace",
                           timeout=LIVE_TIMEOUT, stdin=subprocess.DEVNULL)
        value = json.loads(p.stdout)["int"] if p.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired, ValueError, KeyError, TypeError):
        value = None
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def main(argv):
    a = parse_args(argv)
    live_ss = a.ss_file is None
    ss_text = run_live(SS_CMD, "ss_unavailable") if live_ss else \
        read_text(a.ss_file, "ss_file_unreadable")
    header, rows = parse_ss(ss_text)
    if a.socket2:
        sock2 = a.socket2
    elif live_ss:
        sock2 = os.path.join(instance_dir(), SOCKET2_NAME)
    else:
        sock2 = find_socket2(rows)
    clients, used = census(rows, sock2)

    logs = a.log or [os.path.join(instance_dir(), "hyprland.log")]
    channels = [(f"log:{p}", count_markers(read_text(p, "log_unreadable"))) for p in logs]
    journal = read_text(a.journal_file, "journal_file_unreadable") if a.journal_file else \
        run_live(JOURNAL_CMD, "journal_unavailable")
    channels.append(("journal", count_markers(journal)))

    dl = int(a.disable_logs) if a.disable_logs is not None else disable_logs_live()
    observable = "unknown" if dl is None else ("no" if dl else "yes")

    if a.snapshot_out:
        try:
            with open(a.snapshot_out, "w", encoding="utf-8") as f:
                f.write(header + "\n" + "".join(r["raw"] + "\n" for r in used))
        except OSError as e:
            raise Setup("snapshot_unwritable", f"{a.snapshot_out}: {e.strerror or type(e).__name__}")

    out = []
    for c in clients:
        rq = "-" if c["peer_recv_q"] is None else c["peer_recv_q"]
        out.append(f"{TAG}_CLIENT: comm={c['comm']} pid={c['pid']} fd={c['fd']} "
                   f"peer_recv_q={rq} server_send_q={c['server_send_q']}")
    for source, n in channels:
        out.append(f"{TAG}_MARKERS: source={source} overflow={n['overflow']} "
                   f"write_fail={n['write_fail']}")
    overflow = sum(n["overflow"] for _, n in channels)
    write_fail = sum(n["write_fail"] for _, n in channels)
    lagging = sum(1 for c in clients if c["peer_recv_q"])
    seen = {c["comm"] for c in clients}
    missing = [c for c in dict.fromkeys(a.expect_client) if c not in seen]
    if overflow or write_fail:
        verdict, rc = "MARKERS", 1
    elif missing:
        verdict, rc = "MISSING_CLIENT", 1
    else:
        verdict, rc = "CLEAN", 0
    out.append(f"{TAG}: socket2={sock2} subscribers={len(clients)} overflow={overflow} "
               f"write_fail={write_fail} lagging={lagging} "
               f"missing_client={','.join(missing) or '-'} markers_observable={observable} "
               f"verdict={verdict}")
    print("\n".join(out))
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Setup as e:
        print(e.line)
        sys.exit(2)
