#!/usr/bin/env python3
"""sweep-privacy.py — class scan of round-46 committed receipts for classes the gate misses.

Reads every blob under a revision+path from the git object database (never the
working tree) and reports, per privacy class, the number of files/occurrences and
at most --examples file:line locators. VALUES ARE NEVER PRINTED: a locator names
the file and line, never the matched text.

Classes here are the ones outside quality/check-session-material.py R1-R4:
  G1_ENV_SESSION   an assignment of a session-identifying variable
                   (HYPRLAND_INSTANCE_SIGNATURE, WAYLAND_DISPLAY, XDG_SESSION_ID,
                   DBUS_SESSION_BUS_ADDRESS, XDG_RUNTIME_DIR, LOGNAME, USER)
  G2_HOME_PATH     an absolute /home/<account>/ path (single paths; R4 needs >10
                   distinct whole-line matches, so one quoted path is invisible)
  G3_RUNTIME_UID   an absolute /run/user/<uid>/ path
  G4_LIVE_IDENT    exact equality with a live monitor serial/description/make/model
                   (read from --live-json, printed only as a class)
  G5_SECRET_SHAPE  a credential-shaped token (cloud key prefix, PEM header)
  G6_EMAIL         an e-mail address
  G7_MAC           a MAC address
  G8_PROC_ENVIRON  a /proc/<pid>/environ or /proc/<pid>/cmdline read
  G9_APP_INVENTORY a block of more than --inventory-limit distinct whole-line
                   entries that are either a $HOME/... path or a bare *.desktop
                   name (a directory listing; R4 sees neither form)
  G10_PROC_TRACE   a raw strace line keyed by pid (NNNN  syscall(...)), which
                   couples the receipt to one live session
  G11_MTIME        an exact host-file mtime epoch (activity timestamp)

Usage: sweep-privacy.py (--repo DIR --rev REV --path PATH | --worktree DIR)
                        [--live-json F] [--examples N] [--inventory-limit N]
"""
import argparse
import json
import os
import re
import subprocess
import sys

CLASSES = (
    "G1_ENV_SESSION",
    "G2_HOME_PATH",
    "G3_RUNTIME_UID",
    "G4_LIVE_IDENT",
    "G5_SECRET_SHAPE",
    "G6_EMAIL",
    "G7_MAC",
    "G8_PROC_ENVIRON",
    "G9_APP_INVENTORY",
    "G10_PROC_TRACE",
    "G11_MTIME",
)

PATTERNS = {
    "G1_ENV_SESSION": re.compile(
        r"\b(?:HYPRLAND_INSTANCE_SIGNATURE|WAYLAND_DISPLAY|XDG_SESSION_ID|"
        r"DBUS_SESSION_BUS_ADDRESS|XDG_RUNTIME_DIR|LOGNAME|USER)="
    ),
    "G2_HOME_PATH": re.compile(r"/home/[A-Za-z0-9._-]+/"),
    "G3_RUNTIME_UID": re.compile(r"/run/user/\d+/"),
    "G5_SECRET_SHAPE": re.compile(
        r"(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|"
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----)"
    ),
    "G6_EMAIL": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "G7_MAC": re.compile(r"\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b"),
    "G8_PROC_ENVIRON": re.compile(r"/proc/\d+/(?:environ|cmdline)"),
    "G10_PROC_TRACE": re.compile(r"^\s*\d+\s+(?:execve|openat|connect|socket)\("),
    "G11_MTIME": re.compile(r"\bmtime=\d{9,}\b"),
}

INVENTORY_HOME_RE = re.compile(r"^\$HOME/\S+$")
INVENTORY_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._+()-]*\.desktop$")


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    if proc.returncode != 0:
        sys.exit("git %s failed: %s" % (" ".join(args),
                                        proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout


def tree(repo, rev, path):
    raw = git(repo, "ls-tree", "-r", "-z", rev, "--", path)
    out = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, name = record.split(b"\t", 1)
        mode, kind, sha = meta.split(b" ")
        if kind == b"blob":
            out.append((sha.decode("ascii"), name.decode("utf-8", "surrogateescape")))
    return out


def blobs(repo, shas):
    req = subprocess.run(["git", "-C", repo, "cat-file", "--batch"],
                         input=("\n".join(shas) + "\n").encode("ascii"),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = req.stdout
    pos = 0
    for want in shas:
        end = data.index(b"\n", pos)
        header = data[pos:end]
        pos = end + 1
        parts = header.split(b" ")
        if len(parts) != 3:
            continue
        size = int(parts[2])
        body = data[pos:pos + size]
        pos += size + 1
        yield want, body


def scan_worktree(args):
    """Same classes, but over the files of a working-tree directory."""
    root = args.worktree
    pairs = []
    for base, _dirs, files in os.walk(root):
        for name in sorted(files):
            pairs.append(os.path.join(base, name))
    hits = {name: {} for name in CLASSES}
    for path in pairs:
        try:
            with open(path, "rb") as fh:
                body = fh.read()
        except OSError:
            continue
        if b"\x00" in body[:8192]:
            continue
        text = body.decode("utf-8", "replace")
        lines = text.splitlines()
        for cname, rx in PATTERNS.items():
            for lineno, line in enumerate(lines, 1):
                if rx.search(line):
                    hits[cname].setdefault(path, []).append(lineno)
        inv = {line.strip() for line in lines
               if INVENTORY_HOME_RE.match(line.strip())
               or INVENTORY_NAME_RE.match(line.strip())}
        if len(inv) > args.inventory_limit:
            hits["G9_APP_INVENTORY"].setdefault(path, []).append(len(inv))
    print("SWEEP_WORKTREE dir=%s files=%d" % (root, len(pairs)))
    total = 0
    for cname in CLASSES:
        table = hits[cname]
        print("CLASS=%s files=%d occurrences=%d"
              % (cname, len(table), sum(len(v) for v in table.values())))
        total += len(table)
        for path in sorted(table)[:args.examples]:
            if cname == "G9_APP_INVENTORY":
                print("  LOC %s distinct_entries=%d" % (path, table[path][0]))
            else:
                print("  LOC %s:%s" % (path, ",".join(str(n) for n in table[path][:6])))
    print("SWEEP_TOTAL file_class_pairs=%d" % total)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--path", default=".ufo/waves/round-46")
    ap.add_argument("--live-json")
    ap.add_argument("--examples", type=int, default=8)
    ap.add_argument("--inventory-limit", type=int, default=10)
    ap.add_argument("--worktree", help="scan a working-tree dir instead of git blobs")
    ap.add_argument("--skip", default="")
    args = ap.parse_args()

    if args.worktree:
        scan_worktree(args)
        return
    if not (args.repo and args.rev):
        ap.error("--repo and --rev are required unless --worktree is given")
    entries = tree(args.repo, args.rev, args.path)
    skip = [s for s in args.skip.split(",") if s]
    order, seen = [], set()
    for sha, _ in entries:
        if sha not in seen:
            seen.add(sha)
            order.append(sha)

    live = []
    if args.live_json:
        with open(args.live_json, "r", encoding="utf-8") as fh:
            for mon in json.load(fh):
                for key in ("serial", "description", "make", "model"):
                    val = mon.get(key)
                    if isinstance(val, str) and len(val.strip()) >= 4:
                        live.append((key, val.strip()))

    hits = {name: {} for name in CLASSES}   # class -> path -> [line numbers]
    scanned = 0
    for sha, body in blobs(args.repo, order):
        if b"\x00" in body[:8192]:
            continue
        scanned += 1
        text = body.decode("utf-8", "replace")
        lines = text.splitlines()
        name = None
        for path_sha, path in entries:
            if path_sha == sha:
                name = path
                break
        if name is None or any(s in name for s in skip):
            continue
        inv = {line.strip() for line in lines
               if INVENTORY_HOME_RE.match(line.strip())
               or INVENTORY_NAME_RE.match(line.strip())}
        if len(inv) > args.inventory_limit:
            hits["G9_APP_INVENTORY"].setdefault(name, []).append(len(inv))
        for cname, rx in PATTERNS.items():
            for lineno, line in enumerate(lines, 1):
                if rx.search(line):
                    hits[cname].setdefault(name, []).append(lineno)
        if live:
            for lineno, line in enumerate(lines, 1):
                for _key, val in live:
                    if val in line:
                        hits["G4_LIVE_IDENT"].setdefault(name, []).append(lineno)
                        break

    print("SWEEP roles=%s files=%d blobs_scanned=%d" % (args.path, len(entries), scanned))
    total = 0
    for cname in CLASSES:
        table = hits[cname]
        occ = sum(len(v) for v in table.values())
        print("CLASS=%s files=%d occurrences=%d" % (cname, len(table), occ))
        total += len(table)
        shown = 0
        for path in sorted(table):
            if shown >= args.examples:
                break
            if cname == "G9_APP_INVENTORY":
                print("  LOC %s distinct_entries=%d" % (path, table[path][0]))
            else:
                locs = ",".join(str(n) for n in table[path][:6])
                print("  LOC %s:%s" % (path, locs))
            shown += 1
    print("SWEEP_TOTAL file_class_pairs=%d" % total)


if __name__ == "__main__":
    main()
