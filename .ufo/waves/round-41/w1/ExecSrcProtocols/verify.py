#!/usr/bin/env python3
"""verify.py - checks facts.md (seat ExecSrcProtocols, round 41 w1) against its receipts.

Offline (default): every table row is checked against the byte copies in
receipt/sources/ (sha256 manifest + exact line), every name against the frozen
counter's class table and the host journal, every quote against its lane file.

--refetch: additionally re-clones each pinned repository at the recorded commit
and asserts the receipt bytes are byte-identical to the pinned source.

Exit 0 = all checks passed. Exit 1 = a check failed. Exit 2 = facts.md unparsable.
"""
import argparse
import ast
import hashlib
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, *([os.pardir] * 5)))
COUNTER = "quality/counters/c1-r41-globals.py"
JOURNAL = ".ufo/waves/round-41/fetch/xdph-journal.txt"
FACTS = os.path.join(HERE, "facts.md")
SOURCES = os.path.join(HERE, "receipt", "sources")
MANIFEST = os.path.join(HERE, "receipt", "sources.sha256")

REPOS = {
    "wayland-protocols": "https://gitlab.freedesktop.org/wayland/wayland-protocols.git",
    "wlr-protocols": "https://gitlab.freedesktop.org/wlroots/wlr-protocols.git",
    "hyprland-protocols": "https://github.com/hyprwm/hyprland-protocols.git",
    "Hyprland": "https://github.com/hyprwm/Hyprland.git",
}
ROW = re.compile(r"^\| `([A-Za-z0-9_]+)` \| ([a-z-]+) \| `([^`]+)` \| `(.*)` \|$")
DEF = re.compile(r"^([A-Za-z-]+)@([0-9a-f]{40}):(.+):(\d+)$")
QUOTE = re.compile(r'^\| `([^`]+):(\d+)` \| "(.*)" \| (\d+) \|')
PIN = re.compile(r"^\| ([A-Za-z-]+) \| `([0-9a-f]{40})` \|")

fails = []


def fail(msg):
    fails.append(msg)
    print("FAIL " + msg)


def section(text, title):
    out, on = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            on = line.strip().startswith("## " + title)
            continue
        if on:
            out.append(line)
    return out


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def table_names():
    src = open(os.path.join(LANE, COUNTER), encoding="utf-8").read()
    tree = ast.parse(src)
    classes = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "CLASSES":
            classes = ast.literal_eval(node.value)
    doc = ast.get_docstring(tree)
    seg = doc[doc.index("Class decision table"):]
    rows = []
    for line in seg.splitlines():
        m = re.match(r"^  ([a-z-]+)\s{2,}(.+)$", line)
        if m:
            rows.append((m.group(1), m.group(2).split()))
    code = [(n, c) for c, ns in classes.items() for n in ns]
    docn = [(n, c) for c, ns in rows for n in ns]
    if code != docn:
        fail("counter docstring table != in-code CLASSES dict")
    if len(docn) != 27:
        fail("counter names %d, expected 27" % len(docn))
    return docn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refetch", action="store_true")
    args = ap.parse_args()

    try:
        text = open(FACTS, encoding="utf-8").read()
    except OSError as e:
        print("SETUP facts.md unreadable: %s" % e)
        return 2
    rows = []
    for line in section(text, "Table"):
        m = ROW.match(line)
        if m:
            rows.append(m.groups())
    quotes = []
    for line in section(text, "Quotes"):
        m = QUOTE.match(line)
        if m:
            quotes.append(m.groups())
    if not rows or not quotes:
        print("SETUP no table/quote rows parsed from facts.md")
        return 2

    # 1. names: counter <-> facts.md
    want = table_names()
    got = [(r[0], r[1]) for r in rows]
    if got != want:
        fail("facts.md table names differ from the frozen counter's class table")
    print("ok   names: %d table names == counter docstring == counter CLASSES" % len(want))

    # 2. receipts: manifest, exact line, interface spelling, pin consistency
    manifest = {}
    for line in open(MANIFEST, encoding="utf-8"):
        h, p = line.split()
        manifest[p] = h
    pins = {}
    for line in section(text, "Pins"):
        m = PIN.match(line)
        if m:
            pins[m.group(1)] = m.group(2)
    for name, cls, src, iface in rows:
        m = DEF.match(src)
        if not m:
            fail("unparsable definition %r for %s" % (src, name))
            continue
        repo, commit, path, lineno = m.group(1), m.group(2), m.group(3), int(m.group(4))
        rel = repo + "/" + path
        f = os.path.join(SOURCES, rel)
        if not os.path.isfile(f):
            fail("%s: receipt missing %s" % (name, rel))
            continue
        if manifest.get(rel) != sha256(f):
            fail("%s: receipt sha256 differs from manifest for %s" % (name, rel))
        lines = open(f, encoding="utf-8", errors="replace").read().split("\n")
        actual = lines[lineno - 1].strip() if lineno <= len(lines) else ""
        if actual != iface:
            fail("%s: %s:%d is %r, facts.md says %r" % (name, rel, lineno, actual, iface))
        if '<interface name="%s"' % name not in actual:
            fail("%s: line %d does not define that interface" % (name, lineno))
        if pins.get(repo) != commit:
            fail("%s: row cites %s@%s but the Pins table says %s"
                 % (name, repo, commit[:12], (pins.get(repo) or "nothing")[:12]))
    print("ok   receipts: %d/%d rows line-exact against receipt/sources + sha256 manifest"
          % (len(rows) - len(fails), len(rows)))

    # 3. host journal: every table name advertised
    j = open(os.path.join(LANE, JOURNAL), encoding="utf-8", errors="replace").read()
    adv = set(re.findall(r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver \d{1,6}\)$", j, re.M))
    missing = [n for n, _ in want if n not in adv]
    if missing:
        fail("table names not advertised in the host journal: %s" % missing)
    print("ok   journal: %d/%d table names advertised (%d distinct names in %d adverts)"
          % (len(want) - len(missing), len(want), len(adv),
             len(re.findall(r"Got interface: ", j))))

    # 4. quotes: located, verbatim, <= 25 words
    for src, lineno, quote, words in quotes:
        p = os.path.join(LANE, src)
        line = open(p, encoding="utf-8").read().split("\n")[int(lineno) - 1]
        if quote not in line:
            fail("quote not at %s:%s: %r" % (src, lineno, quote))
        if len(quote.split()) > 25:
            fail("quote over 25 words at %s:%s" % (src, lineno))
        if int(words) != len(quote.split()):
            fail("quote word count at %s:%s: says %s, is %d" % (src, lineno, words, len(quote.split())))
    print("ok   quotes: %d located, verbatim, <= 25 words" % len(quotes))

    # 5. optional refetch of the pinned commits
    if args.refetch:
        tmp = tempfile.mkdtemp(prefix="srcproto-verify-")
        try:
            pins = {}
            for repo, url in REPOS.items():
                d = os.path.join(tmp, repo)
                subprocess.run(["git", "clone", "-q", "--filter=blob:none",
                                "--no-checkout", url, d], check=True)
                for name, cls, src, iface in rows:
                    m = DEF.match(src)
                    if not m or m.group(1) != repo:
                        continue
                    commit, path = m.group(2), m.group(3)
                    if pins.setdefault(repo, commit) != commit:
                        fail("%s: rows cite two commits" % repo)
                    blob = subprocess.run(["git", "-C", d, "show", "%s:%s" % (commit, path)],
                                          capture_output=True, check=True).stdout
                    rel = repo + "/" + path
                    if hashlib.sha256(blob).hexdigest() != manifest.get(rel):
                        fail("%s: refetched %s@%s:%s differs from receipt"
                             % (name, repo, commit[:12], path))
            for repo, commit in sorted(pins.items()):
                if commit not in text:
                    fail("%s: commit %s not recorded in facts.md" % (repo, commit))
            print("ok   refetch: %d repos, %d sources byte-identical at the pinned commits"
                  % (len(pins), len(rows)))
        finally:
            subprocess.run(["rm", "-rf", tmp], check=True)

    print("VERIFY: %s (%d checks failed)" % ("PASS" if not fails else "FAIL", len(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
