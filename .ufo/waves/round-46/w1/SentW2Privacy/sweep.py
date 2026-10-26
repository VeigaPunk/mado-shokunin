#!/usr/bin/env python3
"""SentW2Privacy — independent session-material sweep of committed blobs.

Differs from quality/check-session-material.py in two ways that matter for the
round-46 w2 question:

1. it compares committed identity strings against one live `hyprctl monitors all -j`
   dump (hash/substring, never a value in the output), so synthetic fixture
   identities are separated from the host's real ones — the gate cannot tell
   them apart;
2. its scope is a path prefix of the whole repo, so it also reaches the tracked
   files OUTSIDE `.ufo/` (corpus/, quality/, tools/), which the gate does not read.

Classes (never a value, only path:line + class + count):

C1_TITLE_OBJECT   JSON object with `class` plus non-empty `title`/`initialTitle`
C2_TITLE_STRING   any line carrying a non-empty `"title"`/`"initialTitle"` value
C3_LIVE_IDENT     substring of the live monitor `serial`/`description`/`make`/`model`
C4_SYNTH_IDENT    JSON object with non-empty `serial` + `description`/`make`/`model`
                  that contains no live identity string
C5_PROC_TABLE     `users:(("<prog>",pid=<n>` (ss -xpa / ss -p column)
C6_HOME_DUMP      > --home-limit distinct lines that are nothing but a /home path
C7_HOME_PATH      any `/home/<segment>/` occurrence (account name exposure)
C8_TOKEN          secret-shaped token / private-key header / auth header
C9_NET_ID         dotted-quad IPv4, MAC, or /run/user/<uid> path

Usage: sweep.py --repo DIR --rev REV [--scope PREFIX] --live monitors-all.json [--home-limit N]
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

TITLE_OBJ_KEY = ("title", "initialTitle", "initialtitle", "Title")
PROC_RE = re.compile(r'users:\(\("[^"]{0,128}",pid=\d+')
HOME_LINE_RE = re.compile(r'^/home/[A-Za-z0-9._-]+(?:/[^\s]*)?/?$')
HOME_SEG_RE = re.compile(r'/home/[A-Za-z0-9._-]+')
TITLE_RE = re.compile(r'"(initialTitle|title)"\s*:\s*"([^"\\]{1,400})"')
IDENT_RE = re.compile(r'"(serial|description|make|model)"\s*:\s*"([^"\\]{1,400})"')
TOKEN_RES = (
    re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
    re.compile(r'sk-[A-Za-z0-9]{20,}'),
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'xox[abprs]-[A-Za-z0-9-]{10,}'),
    re.compile(r'AIza[0-9A-Za-z_-]{30,}'),
    re.compile(r'-----BEGIN [A-Z ]{0,40}PRIVATE KEY-----'),
    re.compile(r'Authorization:\s*\S{8,}'),
    re.compile(r'(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*\S{6,}'),
)
IPV4_RE = re.compile(r'\b(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}\b')
MAC_RE = re.compile(r'\b(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\b')
RUNTIME_RE = re.compile(r'/run/user/\d+')


def git(repo, *args):
    return subprocess.run(("git", "-C", repo) + args, capture_output=True, check=True).stdout


def blobs(repo, rev, scope):
    """[(path, bytes)] for every text blob tracked at rev under scope."""
    paths = git(repo, "ls-tree", "-r", "-z", "--name-only", rev, "--", scope).split(b"\0")
    paths = [p.decode("utf-8", "replace") for p in paths if p]
    if not paths:
        return []
    spec = "".join("%s:%s\n" % (rev, p) for p in paths).encode()
    out = subprocess.run(("git", "-C", repo, "cat-file", "--batch"), input=spec,
                         capture_output=True, check=True).stdout
    res, i, n = [], 0, 0
    while i < len(out) and n < len(paths):
        nl = out.index(b"\n", i)
        head = out[i:nl].split()
        i = nl + 1
        if len(head) < 3:
            res.append((paths[n], b""))
            n += 1
            continue
        size = int(head[2])
        res.append((paths[n], out[i:i + size]))
        i += size + 1
        n += 1
    return res


def json_objects(text):
    """yield dicts parsed from a whole-file JSON or from embedded objects."""
    try:
        doc = json.loads(text)
        stack = [doc]
        while stack:
            cur = stack.pop()
            if isinstance(cur, dict):
                yield cur
                stack.extend(cur.values())
            elif isinstance(cur, list):
                stack.extend(cur)
        return
    except Exception:
        pass
    dec = json.JSONDecoder()
    for m in re.finditer(r'\{', text):
        try:
            obj, _ = dec.raw_decode(text, m.start())
        except Exception:
            continue
        if isinstance(obj, dict):
            yield obj


def has_title(obj):
    if not isinstance(obj.get("class"), str) or not obj["class"].strip():
        return False
    for k in ("title", "initialTitle"):
        v = obj.get(k)
        if isinstance(v, str) and v.strip():
            return True
    return False


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--scope", default="")
    ap.add_argument("--live", required=True)
    ap.add_argument("--home-limit", type=int, default=10)
    a = ap.parse_args(argv)

    live = json.load(open(a.live))
    live_vals = {}
    for m in live:
        for k in ("serial", "description", "make", "model"):
            v = str(m.get(k) or "")
            if len(v) >= 3:
                live_vals.setdefault(k, set()).add(v)

    findings = {}          # (path, class) -> [lines]
    counts = {}            # class -> findings
    def hit(path, cls, line=None):
        key = (path, cls)
        findings.setdefault(key, [])
        if line is not None and line not in findings[key][:20]:
            findings[key].append(line)

    items = blobs(a.repo, a.rev, a.scope or ".")
    scanned = 0
    for path, raw in items:
        if b"\0" in raw[:8192]:
            continue
        text = raw.decode("utf-8", "replace")
        scanned += 1
        lines = text.splitlines()

        # C3 live identity strings (substring; the only class that needs the live dump)
        for k, vals in live_vals.items():
            for v in vals:
                if v and v in text:
                    hit(path, "C3_LIVE_IDENT", 0)
                    per_key = "C3_LIVE_" + k.upper()
                    hit(path, per_key, 0)

        # C1 / C4 structural JSON
        objs = list(json_objects(text))
        if any(has_title(o) for o in objs):
            hit(path, "C1_TITLE_OBJECT", 0)
        for o in objs:
            s = o.get("serial")
            if isinstance(s, str) and s.strip():
                if any(isinstance(o.get(x), str) and o[x].strip() for x in ("description", "make", "model")):
                    live_hit = any(v in json.dumps(o) for vals in live_vals.values() for v in vals)
                    hit(path, "C4_LIVE_IDENT_OBJECT" if live_hit else "C4_SYNTH_IDENT", 0)

        home_lines = []
        segs = set()
        for i, line in enumerate(lines, 1):
            if TITLE_RE.search(line):
                hit(path, "C2_TITLE_STRING", i)
            if PROC_RE.search(line):
                hit(path, "C5_PROC_TABLE", i)
            if HOME_LINE_RE.match(line):
                home_lines.append(line)
            for m in HOME_SEG_RE.finditer(line):
                segs.add(m.group(0))
            for rx in TOKEN_RES:
                if rx.search(line):
                    hit(path, "C8_TOKEN", i)
                    break
            if IPV4_RE.search(line) or MAC_RE.search(line) or RUNTIME_RE.search(line):
                hit(path, "C9_NET_ID", i)
        distinct = {l for l in home_lines}
        if len(distinct) > a.home_limit:
            hit(path, "C6_HOME_DUMP", 0)
        if segs:
            hit(path, "C7_HOME_PATH", 0)

    paths = sorted({p for p, _ in findings})
    for (path, cls), ls in sorted(findings.items()):
        lines_s = ",".join(str(x) for x in sorted(ls)[:12]) if ls else "-"
        print("FINDING class=%s file=%s lines=%s" % (cls, path, lines_s))
    print("SWEEP_CLASSES: " + " ".join(
        "%s=%d" % (c, sum(1 for p, k in findings if k == c))
        for c in sorted({k for _, k in findings})))
    print("SWEEP: scope=%s files=%d verdict=%s rev=%s"
          % (a.scope or ".", scanned, "FINDINGS" if findings else "CLEAN", a.rev))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
