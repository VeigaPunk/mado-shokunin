#!/usr/bin/env python3
"""redact.py — apply the round-47 receipt redaction rule to a captured receipt.

The rule (MADO-47-PRIV, proposed by seat SentPrivacy; see report.md):

  P1  every absolute path below $HOME is written with $HOME in place of the
      account segment: /home/<account>/x -> $HOME/x
  P2  every absolute path below the seat scratch work dir is written $WORK:
      --work DIR/... -> $WORK/...
  P3  /run/user/<digits>/... -> /run/user/<uid>/...
  P4  a live HYPRLAND_INSTANCE_SIGNATURE value -> <INSTANCE_SIG>; the variable
      itself is dropped from an env record
  P5  env keys outside the resolver contract are dropped whole (never printed
      truncated): the forbidden list below
  P6  pid=<digits> -> pid=<n>; a strace execve line is reduced to the binary
      basename, so no argv/cwd and no session-coupled pid survives
  P7  a timestamp taken from a host file (mtime) is written as an age class,
      never as an exact epoch

Everything else is left byte-identical: the receipt must stay checkable, so the
redactor never rewrites values it does not have to touch.

Usage:
    redact.py --in FILE --out FILE [--work DIR] [--home DIR] [--check]

Exit status: 0 clean, 1 --check found a residual class, 2 usage.
"""
import argparse
import os
import re
import sys
import time

FORBIDDEN_ENV = (
    "HYPRLAND_INSTANCE_SIGNATURE",
    "HYPRLAND_CMD",
    "WAYLAND_DISPLAY",
    "XDG_SESSION_ID",
    "XDG_SESSION_PATH",
    "XDG_SEAT_PATH",
    "DBUS_SESSION_BUS_ADDRESS",
    "XDG_RUNTIME_DIR",
    "LOGNAME",
    "USER",
    "SHELL",
    "XDG_STATE_HOME",
    "XDG_CACHE_HOME",
)

CONTRACT_ENV = (
    "XDG_CURRENT_DESKTOP",
    "XDG_CONFIG_HOME",
    "XDG_CONFIG_DIRS",
    "XDG_DATA_HOME",
    "XDG_DATA_DIRS",
    "HOME",
    "PATH",
)

HOME_RE = re.compile(r"/home/[A-Za-z0-9._-]+(?=/|$)")
RUNTIME_UID_RE = re.compile(r"/run/user/\d+(?=/)")
PID_RE = re.compile(r"\bpid=(\d+)\b")
STRACE_RE = re.compile(r'^\s*(?:(\d+)\s+)?execve\("([^"]+)"(.*)$')
MTIME_RE = re.compile(r"\bmtime=(\d{9,})\b")
WORK_BIN_RE = re.compile(r"\$WORK/[^\s:'\"]*bin\b")

SYSTEM_PATH_RE = re.compile(r"^/(?:usr|bin|sbin)/")


def system_path(value, placeholder="<tool-bin>"):
    """Keep only system dirs of a PATH value; everything else becomes a label."""
    keep = []
    for entry in value.split(":"):
        if entry == "<tool-bin>" or SYSTEM_PATH_RE.match(entry):
            keep.append(entry)
    return ":".join(keep)


RESIDUAL = {
    "P1_HOME_PATH": re.compile(r"/home/[A-Za-z0-9._-]+/"),
    "P3_RUNTIME_UID": re.compile(r"/run/user/\d+/"),
    "P4_INSTANCE_SIG": re.compile(r"\b(?:HYPRLAND_INSTANCE_SIGNATURE|WAYLAND_DISPLAY)=[^\s'\"]+"),
    "P6_PID": re.compile(r"\bpid=\d+\b"),
}


def age_class(epoch, now):
    delta = max(0, now - int(epoch))
    if delta < 3600:
        return "mtime=<1h"
    if delta < 86400:
        return "mtime=<1d"
    if delta < 7 * 86400:
        return "mtime=<7d"
    return "mtime=>7d"


def redact(text, work=None, home=None, now=None, contract_env=False,
           path_system_only=False):
    if now is None:
        now = int(os.environ.get("SOURCE_DATE_EPOCH") or time.time())
    home = home or os.environ.get("HOME", "")
    if work:
        text = text.replace(work.rstrip("/"), "$WORK")
    if home:
        text = text.replace(home.rstrip("/"), "$HOME")
    text = HOME_RE.sub("$HOME", text)
    text = RUNTIME_UID_RE.sub("/run/user/<uid>", text)
    text = WORK_BIN_RE.sub("<tool-bin>", text)
    if now:
        text = MTIME_RE.sub(lambda m: age_class(m.group(1), now), text)

    out = []
    for line in text.splitlines(True):
        stripped = line.lstrip()
        key = stripped.split("=", 1)[0] if "=" in stripped else ""
        key = key.split()[-1] if key else ""
        if key in FORBIDDEN_ENV:
            out.append("")
            continue
        if path_system_only and key == "PATH" and "=" in stripped:
            head = line[:len(line) - len(stripped)]
            value = stripped.split("=", 1)[1].rstrip("\n")
            out.append(head + "PATH=" + system_path(value) + "\n")
            continue
        if contract_env and key.isupper() and key.replace("_", "").isalnum() \
                and key not in CONTRACT_ENV:
            out.append("")
            continue
        m = STRACE_RE.match(line)
        if m:
            pid, path, rest = m.groups()
            head = "execve(\"%s\")" % os.path.basename(path)
            tail = rest
            if "= " in tail:
                tail = "= " + tail.split("= ", 1)[1]
            else:
                tail = ""
            out.append(head + " " + tail.strip() + "\n")
            continue
        out.append(PID_RE.sub("pid=<n>", line))
    return "".join(out)


def check(text):
    hits = []
    for name, rx in RESIDUAL.items():
        found = rx.findall(text)
        if found:
            hits.append((name, len(found)))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="dst", required=True)
    ap.add_argument("--work")
    ap.add_argument("--home")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--contract-env", action="store_true",
                    help="keep only the contracted resolver variables")
    ap.add_argument("--path-system-only", action="store_true",
                    help="PATH keeps only system dirs and <tool-bin>")
    args = ap.parse_args()

    with open(args.src, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    result = redact(text, work=args.work, home=args.home,
                    contract_env=args.contract_env,
                    path_system_only=args.path_system_only)
    with open(args.dst, "w", encoding="utf-8") as fh:
        fh.write(result)

    hits = check(result)
    for name, count in hits:
        print("RESIDUAL %s count=%d" % (name, count))
    print("REDACT in=%s out=%s residual_classes=%d" % (args.src, args.dst, len(hits)))
    if args.check and hits:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
