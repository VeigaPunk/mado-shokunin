#!/usr/bin/env python3
"""Build a revision-addressed mirror commit of the round-48 C2 draft in a scratch clone.

The per-file cap (ulimit -f 2048 = 1 MiB) rules out both a worktree checkout and a git
index for the lane's 20k-file base tree, so trees are assembled with `git mktree` from a
flat `git ls-tree -r` listing and the changed blobs are hashed with `git hash-object -w`.
Nothing is written outside the clone's object store and variants/<name>/diff.txt.
"""
import difflib
import hashlib
import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r48/MutC2Entry"
D = S + "/clone"
L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = L + "/.ufo/waves/round-48"
BASE = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
ENTRY = "corpus/knowledge/xkb-keymap-compile-r48.md"
RECEIPT = ".ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt"

ENV = dict(os.environ)
ENV.update({"GIT_AUTHOR_NAME": "mut", "GIT_AUTHOR_EMAIL": "mut@scratch",
            "GIT_COMMITTER_NAME": "mut", "GIT_COMMITTER_EMAIL": "mut@scratch"})


def git(*args, inp=None):
    p = subprocess.run(["git", "-C", D, *args], input=inp, capture_output=True, env=ENV)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr.decode()[:400]))
    return p.stdout


def show(rev, path):
    return git("show", "%s:%s" % (rev, path))


def base_files():
    """path -> (mode, sha) for every blob at BASE."""
    out = {}
    for line in git("ls-tree", "-r", BASE).decode().splitlines():
        meta, path = line.split("\t", 1)
        mode, _typ, sha = meta.split()
        out[path] = (mode, sha)
    return out


def write_tree(files):
    """files: path -> (mode, sha). Returns root tree sha, built bottom-up with mktree."""
    children = {}
    for path, val in files.items():
        parts = path.split("/")
        node = children
        for part in parts[:-1]:
            node = node.setdefault(part, {})
            if not isinstance(node, dict):
                raise SystemExit("file/dir clash at " + path)
        node[parts[-1]] = val

    def build(node):
        lines = []
        for name, val in node.items():
            if isinstance(val, dict):
                sub = build(val)
                lines.append("040000 tree %s\t%s" % (sub, name))
            else:
                mode, sha = val
                lines.append("%s blob %s\t%s" % (mode, sha, name))
        data = b"".join(l.encode() + b"\0" for l in
                        sorted(lines, key=lambda s: s.split("\t", 1)[1]))
        return git("mktree", "-z", inp=data).decode().strip()

    return build(children)


def baseline():
    ov = {}
    for name in sorted(os.listdir(W + "/fetch")):
        ov[".ufo/waves/round-48/fetch/" + name] = open(W + "/fetch/" + name, "rb").read()
    ov[RECEIPT] = open(W + "/receipts/xkbcli-compile-keymap-r48.txt", "rb").read()
    ov[".ufo/waves/round-48/tools/make-xkb-receipt.sh"] = open(
        W + "/tools/make-xkb-receipt.sh", "rb").read()
    ov[ENTRY] = open(W + "/l1-draft/xkb-keymap-compile-r48.md", "rb").read()
    rows = open(W + "/l1-draft/rows-c2.md").read().rstrip("\n").split("\n")
    src = show(BASE, "corpus/SOURCES.md").decode().split("\n")
    i = max(k for k, l in enumerate(src) if l.startswith("| S339 |"))
    src[i + 1:i + 1] = rows
    ov["corpus/SOURCES.md"] = "\n".join(src).encode()
    rrow = open(W + "/l1-draft/readme-row.md").read().rstrip("\n")
    rd = show(BASE, "corpus/README.md").decode().split("\n")
    i = max(k for k, l in enumerate(rd)
            if l.startswith("| `knowledge/xdg-terminal-selection-r47.md`"))
    rd.insert(i + 1, rrow)
    ov["corpus/README.md"] = "\n".join(rd).encode()
    return ov


def commit(name, ov, base):
    files = dict(base)
    for path, blob in ov.items():
        sha = git("hash-object", "-w", "--stdin", inp=blob).decode().strip()
        files[path] = ("100644", sha)
    tree = write_tree(files)
    c = git("commit-tree", tree, "-p", BASE, "-m", "variant " + name).decode().strip()
    git("update-ref", "refs/heads/" + name, c)
    return c


def diff(name, ov, base_ov):
    out = []
    for path in sorted(set(ov) | set(base_ov)):
        a, b = base_ov.get(path), ov.get(path)
        if a == b:
            continue
        out.append("### %s\n" % path)
        out.append("old_sha=%s new_sha=%s old_len=%s new_len=%s\n" % (
            hashlib.sha256(a).hexdigest()[:12] if a else "-",
            hashlib.sha256(b).hexdigest()[:12] if b else "-",
            len(a) if a else 0, len(b) if b else 0))
        da = (a or b"").decode("utf-8", "replace").splitlines(True)
        db = (b or b"").decode("utf-8", "replace").splitlines(True)
        out.extend(difflib.unified_diff(da, db, "a/" + path, "b/" + path, n=2))
        out.append("\n")
    d = S + "/variants/" + name
    os.makedirs(d, exist_ok=True)
    open(d + "/diff.txt", "w").write("".join(out))
    return "".join(out)


def main():
    spec = json.load(open(sys.argv[1]))
    base = base_files()
    base_ov = baseline()
    for variant in spec["variants"]:
        ov = dict(base_ov)
        for path, edits in variant.get("edits", {}).items():
            text = ov[path].decode() if path in ov else show(BASE, path).decode()
            if "replace_all" in edits:
                old, new = edits["replace_all"]
                if old not in text:
                    raise SystemExit("%s: missing %r" % (variant["name"], old[:80]))
                text = text.replace(old, new)
            else:
                old, new = edits["replace"]
                if text.count(old) != 1:
                    raise SystemExit("%s: %r occurs %d times" % (
                        variant["name"], old[:80], text.count(old)))
                text = text.replace(old, new)
            ov[path] = text.encode()
        c = commit(variant["name"], ov, base)
        diff(variant["name"], ov, base_ov)
        print("%s %s" % (variant["name"], c))


if __name__ == "__main__":
    main()
