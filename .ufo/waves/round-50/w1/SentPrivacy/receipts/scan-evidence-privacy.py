#!/usr/bin/env python3
"""scan-evidence-privacy.py — count privacy classes in a wave tree, values never printed.

Companion to `quality/check-session-material.py` for the classes that gate does not
model (binds records, pasted bind lines, host identifiers, projected listings). It
reads committed blobs (``--repo`` + ``--rev``) or a working tree (``--tree``) and
prints one JSON object: per-file class counts plus an aggregate. No value from the
scanned bytes is ever printed — only file paths, class names and counts.

Account detection takes ``--account`` or the invoking user; the account literal is
never written to the output.
"""
import argparse
import collections
import getpass
import json
import os
import re
import subprocess
import sys

BIN_PROBE = 8192


def blobs_from_git(repo, rev, path):
    names = subprocess.run(
        ["git", "-C", repo, "ls-tree", "-r", "-z", "--name-only", rev, "--", path],
        capture_output=True, check=True).stdout.split(b"\0")
    for n in names:
        if not n:
            continue
        name = n.decode()
        body = subprocess.run(["git", "-C", repo, "show", f"{rev}:{name}"],
                              capture_output=True, check=True).stdout
        yield name, body


def blobs_from_tree(root):
    for dirpath, _dirs, files in os.walk(root):
        for fn in files:
            p = os.path.join(dirpath, fn)
            try:
                body = open(p, "rb").read()
            except OSError:
                continue
            yield os.path.relpath(p, os.path.dirname(root.rstrip("/"))), body


def main(argv):
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--repo")
    src.add_argument("--tree")
    ap.add_argument("--rev")
    ap.add_argument("--path", default=".ufo/waves/")
    ap.add_argument("--account", default=None)
    ap.add_argument("--hostname", default=None)
    a = ap.parse_args(argv)
    account = a.account or getpass.getuser()
    acct_path = re.compile(r"/home/" + re.escape(account) + r"(?:/[^\s\"'`)\]]*)?")
    prefix_re = re.compile(r"^\s*/home/" + re.escape(account) + r"\S*:\d+:")
    header_re = re.compile(r"^\s*/home/" + re.escape(account) + r"\S*:\s*$")
    diag_re = re.compile(r"^[\w.+-]+: .*\"/home/" + re.escape(account))
    lsrow_re = re.compile(r"^[-dlbcps][rwxsStT-]{9}[+.]?[\s@.]")
    standalone_re = re.compile(r"(?<![A-Za-z0-9._/-])" + re.escape(account) + r"(?![A-Za-z0-9._-])")
    bindline_re = re.compile(r"^\s*bind[a-z]*\s*=")
    uname = (a.hostname or "").strip()

    per = {}
    agg = collections.Counter()
    if a.repo:
        if not a.rev:
            ap.error("--repo needs --rev")
        stream = blobs_from_git(a.repo, a.rev, a.path)
    else:
        stream = blobs_from_tree(os.path.abspath(a.tree))
    nfiles = 0
    for name, body in stream:
        nfiles += 1
        if b"\0" in body[:BIN_PROBE]:
            agg["binary_skipped"] += 1
            continue
        try:
            text = body.decode()
        except UnicodeDecodeError:
            agg["undecodable_skipped"] += 1
            continue
        rec = collections.Counter()
        for line in text.splitlines():
            if "/home/" + account in line:
                rec["acct_path_lines"] += 1
                if prefix_re.match(line):
                    rec["structural_prefix"] += 1
                elif header_re.match(line):
                    rec["structural_header"] += 1
                elif diag_re.match(line):
                    rec["structural_diag"] += 1
                elif lsrow_re.match(line):
                    rec["structural_lsrow"] += 1
                elif re.match(r"^/home/\S+$", line.strip()):
                    rec["structural_bare"] += 1
                elif "`" in line:
                    rec["form_codeticks"] += 1
                elif re.search(r"(^|[\s=('\"])/(?:usr/)?bin/|(^|[\s=('\"])"
                               r"(cat|grep|sed|python3?|git|ls|find|cd|bash|sh|"
                               r"TMPDIR=|--work|--dir=|XDG_[A-Z_]+=|HOME=)\b", line):
                    rec["form_command"] += 1
                else:
                    rec["form_prose"] += 1
        for m in standalone_re.finditer(text):
            if not text[max(0, m.start() - 6):m.start()].endswith("/home/"):
                rec["acct_standalone"] += 1
        for line in text.splitlines():
            if lsrow_re.match(line) and account in line:
                rec["account_column_rows"] += 1
                break
        if bindline_re.search(text):
            rec["bind_definition_lines"] = sum(
                1 for l in text.splitlines() if bindline_re.match(l))
        if uname and uname in text:
            rec["hostname_occurrences"] = text.count(uname)
        stripped = text.strip()
        if stripped[:1] in ("[", "{"):
            try:
                data = json.loads(stripped)
            except Exception:
                data = None
            recs = data if isinstance(data, list) else None
            if isinstance(data, dict):
                recs = data.get("binds") if isinstance(data.get("binds"), list) else None
            if isinstance(recs, list):
                objs = [r for r in recs if isinstance(r, dict)]
                keys = set().union(*[set(o) for o in objs]) if objs else set()
                if len(keys & {"modmask", "dispatcher", "keycode", "longPress", "submap"}) >= 2:
                    rec["binds_records"] = len(objs)
                    rec["binds_with_arg"] = sum(1 for o in objs if o.get("arg"))
                    rec["binds_with_description"] = sum(1 for o in objs if o.get("description"))
                    rec["binds_switch_keys"] = sum(
                        1 for o in objs if str(o.get("key", "")).startswith("switch:"))
        if rec:
            per[name] = dict(sorted(rec.items()))
            agg.update(rec)
    json.dump({"files": nfiles, "account_class": "masked",
               "aggregate": dict(sorted(agg.items())), "per_file": per},
              sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
