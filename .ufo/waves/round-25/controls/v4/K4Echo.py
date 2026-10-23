#!/usr/bin/env python3
"""SERVER ECHO control: query visible Hyprland IPC, never parse a config.

All requests are read-only (binds or instances). Discovery stays inside the
caller's namespaces; it does not attempt a namespace escape or start Hyprland.
A structured stderr receipt records failed avenues even when stdout is [].
"""
import argparse
import collections
import errno
import json
import os
import signal
import socket
import stat
import subprocess
import sys
import time


DEADLINE = time.monotonic() + 20
MAX_BYTES = 8 * 1024 * 1024
receipt = {"hyprctl": [], "roots": [], "proc": {}, "unix_tables": [],
           "socket_attempts": [], "selected": None}
candidates = {}
signatures = set()
runtimes = set()


def table(raw):
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeError):
        return None
    if isinstance(value, list) and all(isinstance(row, dict) for row in value):
        return value
    return None


def command(args, extra_env=None):
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    record = {"argv": ["hyprctl"] + args, "extra_env": extra_env or {}}
    receipt["hyprctl"].append(record)
    if time.monotonic() >= DEADLINE:
        record["error"] = "discovery deadline"
        return None
    try:
        p = subprocess.Popen(record["argv"], env=env, stdin=subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             start_new_session=True)
    except OSError as ex:
        record["error"] = "%s: %s" % (type(ex).__name__, ex)
        return None
    try:
        out, err = p.communicate(timeout=min(2, max(0.01, DEADLINE - time.monotonic())))
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        out, err = p.communicate()
        record["error"] = "timeout; child process group killed"
    record.update(exit=p.returncode, stdout=out[:800].decode(errors="replace"),
                  stderr=err[:800].decode(errors="replace"))
    if p.returncode == 0 and len(out) <= MAX_BYTES:
        return table(out)
    return None


def add_candidate(path, origin):
    if len(candidates) < 256:
        candidates.setdefault(path, origin)
    if not path.startswith("\0") and path.endswith("/.socket.sock"):
        instance = os.path.basename(os.path.dirname(path))
        parent = os.path.dirname(os.path.dirname(path))
        if os.path.basename(parent) == "hypr":
            signatures.add(instance)
            runtimes.add(os.path.dirname(parent))


def scan_root(root):
    rec = {"path": root, "entries": 0, "command_sockets": 0, "errors": []}
    receipt["roots"].append(rec)
    try:
        os.stat(root)
    except OSError as ex:
        rec["error"] = "%s: %s" % (type(ex).__name__, ex)
        return
    pending = [root]
    while pending and rec["entries"] < 10000 and time.monotonic() < DEADLINE:
        directory = pending.pop()
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    rec["entries"] += 1
                    if rec["entries"] > 10000:
                        break
                    if entry.is_dir(follow_symlinks=False):
                        pending.append(entry.path)
                    elif entry.name == ".socket.sock" or "hypr" in entry.name.lower():
                        try:
                            if stat.S_ISSOCK(entry.stat().st_mode):
                                add_candidate(entry.path, "filesystem:" + root)
                                rec["command_sockets"] += 1
                        except OSError as ex:
                            if len(rec["errors"]) < 5:
                                rec["errors"].append(str(ex))
        except OSError as ex:
            if len(rec["errors"]) < 5:
                rec["errors"].append(str(ex))
    rec["truncated"] = bool(pending)


def read_proc():
    comms = collections.Counter()
    compositor_pids = []
    errors = []
    try:
        pids = sorted(name for name in os.listdir("/proc") if name.isdecimal())
    except OSError as ex:
        receipt["proc"] = {"error": str(ex)}
        return []
    for pid in pids[:2048]:
        try:
            with open("/proc/" + pid + "/comm", encoding="utf-8", errors="replace") as fh:
                comm = fh.read(256).strip()
            with open("/proc/" + pid + "/cmdline", "rb") as fh:
                argv0 = fh.read(4096).split(b"\0", 1)[0]
            comms[comm] += 1
            executable = os.path.basename(os.fsdecode(argv0)).lower()
            if comm.lower() == "hyprland" or executable == "hyprland":
                compositor_pids.append(pid)
                with open("/proc/" + pid + "/environ", "rb") as fh:
                    fields = fh.read(65536).split(b"\0")
                for field in fields:
                    key, sep, value = field.partition(b"=")
                    if sep and key == b"XDG_RUNTIME_DIR":
                        runtimes.add(os.fsdecode(value))
                    elif sep and key == b"HYPRLAND_INSTANCE_SIGNATURE":
                        signatures.add(os.fsdecode(value))
        except OSError as ex:
            if len(errors) < 5:
                errors.append("pid %s: %s" % (pid, ex))
    receipt["proc"] = {"pid_count": len(pids), "comms": dict(comms),
                       "compositor_pids": compositor_pids, "errors": errors,
                       "truncated": len(pids) > 2048}
    return compositor_pids


def unix_table(path):
    rec = {"path": path, "entries": 0, "named": 0, "abstract": 0, "hyprland": 0}
    receipt["unix_tables"].append(rec)
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for index, line in enumerate(fh):
                if index == 0:
                    continue
                if index > 10000:
                    rec["truncated"] = True
                    break
                rec["entries"] += 1
                fields = line.rstrip("\n").split(None, 7)
                if len(fields) != 8:
                    continue
                name = fields[7]
                rec["named"] += 1
                rec["abstract"] += name.startswith("@")
                if "hypr" in name.lower() or ".socket.sock" in name:
                    if ".socket2.sock" in name:
                        continue
                    rec["hyprland"] += 1
                    add_candidate("\0" + name[1:] if name.startswith("@") else name,
                                  "unix-table:" + path)
    except OSError as ex:
        rec["error"] = "%s: %s" % (type(ex).__name__, ex)


def from_socket(path, origin):
    rec = {"address": "@" + path[1:] if path.startswith("\0") else path,
           "origin": origin}
    receipt["socket_attempts"].append(rec)
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.settimeout(min(0.25, max(0.01, DEADLINE - time.monotonic())))
            client.connect(path)
            client.sendall(b"j/binds")
            raw = bytearray()
            while len(raw) <= MAX_BYTES and time.monotonic() < DEADLINE:
                chunk = client.recv(min(65536, MAX_BYTES + 1 - len(raw)))
                if not chunk:
                    break
                raw.extend(chunk)
                value = table(raw)
                if value is not None:
                    rec["binds"] = len(value)
                    return value
            rec["error"] = "no complete JSON bind array within byte/time limit"
    except OSError as ex:
        rec["errno"] = ex.errno
        rec["error"] = "%s: %s" % (errno.errorcode.get(ex.errno, type(ex).__name__), ex)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", required=True)
    ap.parse_args()  # Deliberately never reads the config tree.
    receipt["environment"] = {key: os.environ.get(key) for key in
                              ("HOME", "XDG_RUNTIME_DIR", "HYPRLAND_INSTANCE_SIGNATURE")}
    result = command(["binds", "-j"])
    if result is not None:
        receipt["selected"] = "hyprctl binds -j"
    else:
        instances = command(["instances", "-j"])
        if instances:
            for instance in instances:
                if isinstance(instance.get("instance"), str):
                    signatures.add(instance["instance"])
        if os.environ.get("XDG_RUNTIME_DIR"):
            runtimes.add(os.environ["XDG_RUNTIME_DIR"])
        if os.environ.get("HYPRLAND_INSTANCE_SIGNATURE"):
            signatures.add(os.environ["HYPRLAND_INSTANCE_SIGNATURE"])
        pids = read_proc()
        for root in sorted({"/run", "/tmp"} | runtimes):
            scan_root(root)
        for path in ["/proc/net/unix", "/proc/self/net/unix"] + [
                "/proc/" + pid + "/net/unix" for pid in pids]:
            unix_table(path)
        runtimes.add("/run/user/%d" % os.getuid())
        runtimes.add("/tmp")
        for runtime in sorted(runtimes):
            for signature in sorted(signatures):
                path = os.path.join(runtime, "hypr", signature, ".socket.sock")
                add_candidate(path, "discovered-instance")
                add_candidate("\0" + path, "abstract-discovered-instance")
                if result is None:
                    result = command(["-i", signature, "binds", "-j"],
                                     {"XDG_RUNTIME_DIR": runtime})
                    if result is not None:
                        receipt["selected"] = "hyprctl discovered-instance"
        for name in ("hyprland", "hypr", ".socket.sock", "hyprland/.socket.sock"):
            add_candidate("\0" + name, "abstract-conventional-name")
        for path, origin in candidates.items():
            if result is not None or time.monotonic() >= DEADLINE:
                break
            result = from_socket(path, origin)
            if result is not None:
                receipt["selected"] = "@" + path[1:] if path.startswith("\0") else path
    receipt["result_binds"] = len(result) if result is not None else 0
    receipt["fallback_empty"] = result is None
    print(json.dumps(receipt, sort_keys=True), file=sys.stderr)
    print(json.dumps(result if result is not None else []))
    return 0


if __name__ == "__main__":
    sys.exit(main())
