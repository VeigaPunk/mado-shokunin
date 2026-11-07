#!/usr/bin/env python3
"""Round-93 oracle: ask the installed xdg-desktop-portal binary which backend it picks.

The oracle is the production binary (/usr/lib/xdg-desktop-portal, package
xdg-desktop-portal 1.22.1) run with `-v -r` inside a private, activation-free
D-Bus session bus (dbus-run-session --config-file with no <servicedir>), a
fixture HOME/XDG_RUNTIME_DIR, and an unreachable system bus.  Its verbose log
names every backend decision taken by xdp-portal-config.c:

  "Using <src>.portal for <iface> (interface specific config)"   (:879)
  "Using <src>.portal for <iface> (default config)"              (:891)
  "Using <src>.portal for <iface> (config)"                      (:817, find_all)
  "Using <src>.portal for <iface> in <desktop> (fallback)"       (:915/:987, UseIn)
  "Choosing <src>.portal for <iface> as a last-resort fallback"  (:846)

The binary queries 21 impl interfaces unconditionally at start-up
(xdp-context.c:354/368 and the init_* functions it calls, :391-421).  A run is
complete when the whole line "XDP: org.freedesktop.portal.Desktop acquired" appears; an interface with no decision line in a
complete run is labelled [] (no backend).  Incomplete runs are errors, never
labels.

Two modes (case field "mode"):
  dir  XDG_DESKTOP_PORTAL_DIR=<fixture>; .portal files and (desktop-)portals.conf
       are both read from that one directory (xdp-portal-config.c:359-365, 527-536).
  xdg  the real search path: XDG_CONFIG_HOME, XDG_CONFIG_DIRS, /etc, XDG_DATA_HOME,
       XDG_DATA_DIRS, /usr/share (xdp-portal-config.c:538-587) and portals from
       XDG_DATA_HOME, XDG_DATA_DIRS, /usr/share (:367-384).  The host's own
       /usr/share/xdg-desktop-portal tail is part of the input; its digest is
       recorded with the label.

Case file:  {"cases": [{"id", "mode", "desktop", "files": {relpath: text}}]}
  dir-mode relpath is relative to the portal dir; xdg-mode relpath starts with
  config_home/, config_dirs/<n>/, data_home/ or data_dirs/<n>/.
Output (--label OUT): the same cases with "oracle": {iface: [src, ...]} and
"oracle_reason": {iface: reason} added, plus "host_tail_sha256".

Read-only on the host: every write goes under --scratch-root.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

BINARY = "/usr/lib/xdg-desktop-portal"
IMPL = "org.freedesktop.impl.portal."
IFACES = [IMPL + n for n in (
    "Lockdown", "Access", "Settings", "FileChooser", "AppChooser", "Print",
    "Notification", "Inhibit", "Screenshot", "Background", "Wallpaper",
    "Account", "Email", "Secret", "GlobalShortcuts", "DynamicLauncher",
    "ScreenCast", "RemoteDesktop", "Clipboard", "InputCapture", "Usb")]
HOST_TAIL = "/usr/share/xdg-desktop-portal"

BUS_CONF = """<!DOCTYPE busconfig PUBLIC "-//freedesktop//DTD D-Bus Bus Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">
<busconfig><type>session</type><listen>unix:tmpdir={d}</listen><auth>EXTERNAL</auth>
<policy context="default"><allow send_destination="*" eavesdrop="true"/><allow eavesdrop="true"/><allow own="*"/></policy></busconfig>
"""

RX_USING = re.compile(r"^XDP: Using (.+?)\.portal for (\S+) \((interface specific config|default config|config)\)$")
RX_FALLBACK = re.compile(r"^XDP: Using (.+?)\.portal for (\S+) in \S+ \(fallback\)$")
RX_LAST = re.compile(r"^\(/usr/lib/xdg-desktop-portal:\d+\): xdg-desktop-portal-WARNING \*\*: [0-9:.]+: Choosing (.+?)\.portal for (\S+) as a last-resort fallback$")
# The completion line must be the whole line (round-90 R90MReviewC1 O1: the binary echoes
# fixture file names and config values in other debug lines, so a substring test can be forged).
DONE_LINE = "XDP: org.freedesktop.portal.Desktop acquired"


def host_tail_digest() -> str:
    h = hashlib.sha256()
    for root, dirs, files in os.walk(HOST_TAIL):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, HOST_TAIL).encode() + b"\0")
            with open(p, "rb") as fh:
                h.update(fh.read())
            h.update(b"\0")
    return h.hexdigest()


def materialise(case: dict, root: str) -> dict:
    env = {
        "PATH": "/usr/bin",
        "HOME": os.path.join(root, "home"),
        "XDG_RUNTIME_DIR": os.path.join(root, "run"),
        "GSETTINGS_SCHEMA_DIR": "/usr/share/glib-2.0/schemas",
        "DBUS_SYSTEM_BUS_ADDRESS": "unix:path=" + os.path.join(root, "no-system-bus"),
        "LC_ALL": "C",
    }
    for d in ("home", "run"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    os.chmod(os.path.join(root, "run"), 0o700)
    if case["desktop"] is not None:
        env["XDG_CURRENT_DESKTOP"] = case["desktop"]
    if case["mode"] == "dir":
        pdir = os.path.join(root, "portals")
        os.makedirs(pdir, exist_ok=True)
        for rel, text in case["files"].items():
            p = os.path.join(pdir, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(text.encode("utf-8", "surrogateescape"))
        env["XDG_DESKTOP_PORTAL_DIR"] = pdir
        # data dirs still needed for nothing portal-related in dir mode
        env["XDG_DATA_DIRS"] = os.path.join(root, "nodata")
        env["XDG_CONFIG_DIRS"] = os.path.join(root, "nocfg")
        env["XDG_CONFIG_HOME"] = os.path.join(root, "nocfghome")
        env["XDG_DATA_HOME"] = os.path.join(root, "nodatahome")
    elif case["mode"] == "xdg":
        n_cfg = n_data = 0
        for rel, text in case["files"].items():
            p = os.path.join(root, "x", rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(text.encode("utf-8", "surrogateescape"))
            parts = rel.split("/")
            if parts[0] == "config_dirs":
                n_cfg = max(n_cfg, int(parts[1]) + 1)
            if parts[0] == "data_dirs":
                n_data = max(n_data, int(parts[1]) + 1)
        n_cfg = max(n_cfg, case.get("n_config_dirs", 0))
        n_data = max(n_data, case.get("n_data_dirs", 0))
        env["XDG_CONFIG_HOME"] = os.path.join(root, "x", "config_home")
        env["XDG_DATA_HOME"] = os.path.join(root, "x", "data_home")
        env["XDG_CONFIG_DIRS"] = ":".join(os.path.join(root, "x", "config_dirs", str(i)) for i in range(max(n_cfg, 1)))
        env["XDG_DATA_DIRS"] = ":".join(os.path.join(root, "x", "data_dirs", str(i)) for i in range(max(n_data, 1)))
    else:
        raise SystemExit(f"setup: unknown mode {case['mode']!r} in {case['id']}")
    with open(os.path.join(root, "bus.conf"), "w") as fh:
        fh.write(BUS_CONF.format(d=root))
    return env


def run_case(case: dict, scratch: str, timeout: float) -> dict:
    root = tempfile.mkdtemp(prefix="c", dir=scratch)  # short: the bus socket path must fit sun_path
    try:
        env = materialise(case, root)
        proc = subprocess.Popen(
            ["timeout", "-s", "KILL", str(timeout), "dbus-run-session",
             "--config-file=" + os.path.join(root, "bus.conf"), "--", BINARY, "-v", "-r"],
            env=env, cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, errors="replace", start_new_session=True)
        lines = []
        for line in proc.stdout:
            lines.append(line)
            if line.rstrip("\n") == DONE_LINE:
                break
        try:
            os.killpg(proc.pid, 9)
        except ProcessLookupError:
            pass
        proc.wait()
        log = "".join(lines)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    done = any(l == DONE_LINE for l in log.splitlines())
    picks: dict[str, list[str]] = {i: [] for i in IFACES}
    reasons: dict[str, str] = {}
    for line in log.splitlines():
        line = line.rstrip()
        for rx, why in ((RX_USING, None), (RX_FALLBACK, "usein"), (RX_LAST, "gtk-last-resort")):
            m = rx.search(line)
            if not m:
                continue
            src, iface = m.group(1), m.group(2)
            if iface not in picks:
                continue
            reason = why or m.group(3)
            if iface.endswith(".Settings"):
                if src not in picks[iface]:
                    picks[iface].append(src)
                reasons[iface] = reason
            else:
                if reason == "config":
                    continue
                picks[iface] = [src]
                reasons[iface] = reason
    return {"done": done, "picks": picks, "reasons": reasons, "log_tail": log[-4000:] if not done else ""}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--label", required=True, help="output JSON with oracle labels")
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--timeout", type=float, default=8.0)
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    if not os.access(BINARY, os.X_OK):
        print(f"setup: {BINARY} missing", file=sys.stderr)
        return 2
    os.makedirs(a.scratch_root, exist_ok=True)
    data = json.load(open(a.cases, encoding="utf-8"))
    tail = host_tail_digest()
    with ThreadPoolExecutor(a.jobs) as ex:
        results = list(ex.map(lambda c: run_case(c, a.scratch_root, a.timeout), data["cases"]))
    bad = 0
    for case, r in zip(data["cases"], results):
        if not r["done"]:
            bad += 1
            print(f"ORACLE_INCOMPLETE {case['id']}\n{r['log_tail']}", file=sys.stderr)
            continue
        case["oracle"] = r["picks"]
        case["oracle_reason"] = r["reasons"]
    data["host_tail_sha256"] = tail
    data["oracle_binary_sha256"] = hashlib.sha256(open(BINARY, "rb").read()).hexdigest()
    s = json.dumps(data, indent=1, ensure_ascii=True)
    with open(a.label, "w", encoding="ascii") as fh:
        fh.write(s + "\n")
    print(f"PORTAL_ORACLE cases={len(data['cases'])} incomplete={bad} host_tail_sha256={tail}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
