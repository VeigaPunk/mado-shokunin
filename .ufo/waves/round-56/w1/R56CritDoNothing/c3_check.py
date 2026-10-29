#!/usr/bin/env python3
"""Critic's C3 checker, written ONLY from registration.md section 'C3 registry back-references'.

Usage: python3 -I c3_check.py --repo DIR --rev REV --work DIR
Prints one MADO_USED_BY line; exit 0 only on TARGET_MET, 1 on a miss, 2 on setup error.
Reads git objects only (git cat-file / ls-tree / show), never the working tree.
"""
import argparse, hashlib, os, re, subprocess, sys

TABLES = ".ufo/waves/round-56/frozen-tables.json"
TABLES_SHA = "d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af"
SOURCES = "corpus/SOURCES.md"
ENTRY_DIR = "corpus/knowledge/"
ROW_RE = re.compile(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|")
SID_RE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
USED_RE = re.compile(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def setup(msg):
    sys.stderr.write(f"c3_check: setup: {msg}\n")
    sys.exit(2)


def env_for(work):
    return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": work, "TMPDIR": work,
            "GIT_CONFIG_NOSYSTEM": "1", "LC_ALL": "C"}


def git(repo, env, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=env)
    if r.returncode != 0:
        return None
    return r.stdout


def blob_at(repo, env, rev, path):
    """Regular blob (100644/100755) at rev:path, or None. Symlink or crossed symlinked dir = None."""
    out = git(repo, env, "ls-tree", "-z", rev, "--", path)
    if not out:
        return None
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, _, p = rec.partition(b"\t")
        mode, typ, sha = meta.decode().split()
        if p.decode() == path and typ == "blob" and mode in ("100644", "100755"):
            return git(repo, env, "cat-file", "blob", sha)
        return None
    return None


def entries_at(repo, env, rev):
    out = git(repo, env, "ls-tree", "-r", "-z", rev, "--", "corpus/knowledge")
    res = []
    for rec in (out or b"").split(b"\0"):
        if not rec:
            continue
        meta, _, p = rec.partition(b"\t")
        mode, typ, _sha = meta.decode().split()
        p = p.decode()
        if typ == "blob" and mode in ("100644", "100755") and p.startswith(ENTRY_DIR) and "/" not in p[len(ENTRY_DIR):] and p.endswith(".md"):
            res.append(p)
    return sorted(res)


def cites(text):
    """S### tokens on lines outside fenced code blocks."""
    out = set()
    fence = None
    for line in text.split("\n"):
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)[0] * 3  # marker char
                continue
            out.update(SID_RE.findall(line))
        else:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= 3:
                fence = None
    return out


def src_ids(text):
    out = set()
    for line in text.split("\n")[:15]:
        if line.startswith("source:"):
            out.update(SID_RE.findall(line))
    return out


def registry(text):
    rows = {}
    for line in text.split("\n"):
        if not ROW_RE.match(line):
            continue
        s = line.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
        cells = [c.strip() for c in s.split("|")]
        if len(cells) != 11:
            setup(f"registry row with {len(cells)} cells: {line[:60]!r}")
        rows.setdefault(cells[0], []).append(cells)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    env = env_for(a.work)
    tables = blob_at(a.repo, env, a.rev, TABLES)
    if tables is None or hashlib.sha256(tables).hexdigest() != TABLES_SHA:
        setup("frozen-tables.json blob absent or sha mismatch")
    src_blob = blob_at(a.repo, env, a.rev, SOURCES)
    if src_blob is None:
        setup("SOURCES.md absent")
    rows = registry(src_blob.decode("utf-8", "replace"))
    entries = entries_at(a.repo, env, a.rev)
    cite = {}
    srcs = {}
    for e in entries:
        t = blob_at(a.repo, env, a.rev, e).decode("utf-8", "replace")
        cite[e] = cites(t)
        srcs[e] = src_ids(t)
    # USEDBY per registry id (cell 11 only)
    used = {}
    for sid, rs in rows.items():
        if len(rs) != 1:
            setup(f"duplicate registry id {sid}")
        used[sid] = set(USED_RE.findall(rs[0][10]))
    missing = extra = dangling = 0
    for sid in rows:
        for e in entries:
            if sid in cite[e] and e not in used[sid]:
                missing += 1
    for sid in rows:
        for p in used[sid]:
            if p not in cite or sid not in cite[p]:
                extra += 1
    for e in entries:
        for sid in srcs[e]:
            if sid not in rows:
                dangling += 1
    missed = [n for n, v in (("missing", missing), ("extra", extra), ("dangling", dangling)) if v]
    met = not missed
    print(f"MADO_USED_BY: rev={a.rev} entries={len(entries)} rows={len(rows)} missing={missing} extra={extra} "
          f"dangling={dangling} verdict={'TARGET_MET' if met else 'TARGET_MISSED'} "
          f"missed={','.join(missed) if missed else 'none'}")
    sys.exit(0 if met else 1)


if __name__ == "__main__":
    main()
