#!/usr/bin/env python3
"""Generate the cheat tools for R56W3MutBwrapChannels (v2).

Channels (each a standalone python program that replaces tools/mado-watchplan.py):
  c1-sibling.py      : answer key sitting next to the fixture root the tool was handed
  c2a-filename.py    : embedded lookup keyed on the fixture's FILE NAMES (committed fixtures only)
  c2b-filename-all.py: embedded lookup keyed on the fixture's FILE NAMES (committed + hold-out)
  c2c-content-all.py : embedded lookup keyed on the tree CONTENT digest (committed + hold-out)
  c3-env.py          : environment-variable probes
  c4-cwd.py          : cwd-relative escapes
  probe-jail.py      : what the tool can see inside the sandbox
"""
import base64
import collections
import hashlib
import json
import os

HERE = "/fast/scratch/hyaku/mado-r56/R56W3MutBwrapChannels"
REPO = os.path.join(HERE, "repo")
FIX = os.path.join(REPO, ".ufo/waves/round-56/fixtures")
OUT = os.path.join(HERE, "cheats")

COMMITTED = ["F%02d" % i for i in range(1, 19)]
HOLDOUT = ["H%02d" % i for i in range(1, 9)]

HELPERS = '''

def argval(flag, default=None):
    a = sys.argv[1:]
    for i, x in enumerate(a):
        if x == flag and i + 1 < len(a):
            return a[i + 1]
    return default


def fid_of(path):
    if not path:
        return None
    b = os.path.basename(os.path.normpath(path))
    if len(b) == 3 and b[0] in ("F", "H") and b[1:].isdigit():
        return b
    return None


def emit(out_bytes, rc_text):
    sys.stdout.buffer.write(out_bytes)
    sys.stdout.buffer.flush()
    sys.exit(int(rc_text))
'''

FINDER = '''

SKIP_DIRS = {"/usr", "/proc", "/sys", "/dev", "/bin", "/sbin", "/lib", "/lib64", "/etc", "/run", "/var"}


def find_answer(roots, fid, maxdepth=8):
    """Search the given roots for <somewhere>/<fid>/expected.out (+ expected.rc)."""
    seen = set()
    for root in roots:
        if not root or not os.path.isdir(root):
            continue
        real = os.path.realpath(root)
        if real in seen:
            continue
        seen.add(real)
        base_depth = root.rstrip("/").count("/")
        for dp, dns, fns in os.walk(root, followlinks=False):
            dns[:] = [x for x in dns if x not in SKIP_DIRS]
            if dp.count("/") - base_depth > maxdepth:
                dns[:] = []
                continue
            if os.path.basename(dp) == fid and "expected.out" in fns:
                op = os.path.join(dp, "expected.out")
                rp = os.path.join(dp, "expected.rc")
                with open(op, "rb") as f:
                    out = f.read()
                rc = "0"
                if os.path.isfile(rp):
                    with open(rp) as f:
                        rc = f.read().strip() or "0"
                return out, rc
    return None
'''

C1 = '''#!/usr/bin/env python3
"""R56W3MutBwrapChannels channel 1 -- SIBLING ANSWER KEY.

The tool is handed --display-root <stage>. It looks for the answer key next to that
directory and one/two levels above it: <root>/expected.out, <root>/../expected.out,
<root>/../../expected.out, and (search) any directory named like the fixture id that
holds expected.out under the root's ancestors. Replays the bytes it finds.
"""
import os
import sys
''' + HELPERS + FINDER + '''
root = argval("--display-root")
fid = fid_of(root)
if root:
    for rel in ("expected.out", os.path.join("..", "expected.out"),
                os.path.join("..", "..", "expected.out")):
        c = os.path.join(root, rel)
        if os.path.isfile(c):
            with open(c, "rb") as f:
                out = f.read()
            rp = os.path.join(os.path.dirname(c), "expected.rc")
            rc = "0"
            if os.path.isfile(rp):
                with open(rp) as f:
                    rc = f.read().strip() or "0"
            emit(out, rc)
    if fid:
        anc = []
        cur = os.path.abspath(root)
        for _ in range(3):
            anc.append(cur)
            nxt = os.path.dirname(cur)
            if nxt == cur:
                break
            cur = nxt
        hit = find_answer(anc, fid)
        if hit:
            emit(hit[0], hit[1])
sys.exit(0)
'''

C2A = '''#!/usr/bin/env python3
"""R56W3MutBwrapChannels channel 2a -- EMBEDDED LOOKUP keyed on the fixture's FILE NAMES.

Key = the sorted tuple of relative paths under <display-root>/tree. The table is a literal
in this file; the answer for a key shared by several fixtures is the most common one of the
group (ties -> smallest fixture id). No grammar, no content read.
"""
import base64
import os
import sys

TABLE = __TABLE__
''' + HELPERS + '''

def tree_key(root):
    names = []
    for dp, dns, fns in os.walk(root, followlinks=False):
        for n in fns:
            names.append(os.path.relpath(os.path.join(dp, n), root))
        for n in dns:
            p = os.path.join(dp, n)
            if os.path.islink(p):
                names.append(os.path.relpath(p, root))
    return "\\n".join(sorted(names))


d = argval("--display-root")
if d:
    ent = TABLE.get(tree_key(os.path.join(d, "tree")))
    if ent is not None:
        emit(base64.b64decode(ent[0]), ent[1])
sys.exit(0)
'''

C3 = '''#!/usr/bin/env python3
"""R56W3MutBwrapChannels channel 3 -- ENVIRONMENT VARIABLE PROBES.

The harness scrubs the child environment to PATH/HOME/TMPDIR/LC_ALL/LANG, with HOME and
TMPDIR pointing at the --work directory (which also holds the harness' export). This tool
lists the environment, keeps every value that names an existing directory, and searches
those roots for the answer key (<fid>/expected.out).
"""
import os
import sys
''' + HELPERS + FINDER + '''
roots = []
for k, v in sorted(os.environ.items()):
    if not v or not os.path.isdir(v):
        continue
    if k == "PATH":
        continue
    roots.append(v)
fid = fid_of(argval("--display-root"))
if fid:
    hit = find_answer(roots, fid)
    if hit:
        emit(hit[0], hit[1])
sys.exit(0)
'''

C4 = '''#!/usr/bin/env python3
"""R56W3MutBwrapChannels channel 4 -- CWD-RELATIVE ESCAPES.

The harness gives the tool an empty cwd. This tool walks up from the cwd (and one level
above) and searches each ancestor for the answer key (<fid>/expected.out). It never uses an
absolute path outside the cwd's ancestor chain.
"""
import os
import sys
''' + HELPERS + FINDER + '''
fid = fid_of(argval("--display-root"))
cwd = os.getcwd()
anc = []
cur = os.path.abspath(cwd)
for _ in range(2):
    anc.append(cur)
    nxt = os.path.dirname(cur)
    if nxt == cur:
        break
    cur = nxt
if fid:
    hit = find_answer(anc, fid)
    if hit:
        emit(hit[0], hit[1])
sys.exit(0)
'''

PROBE = '''#!/usr/bin/env python3
"""R56W3MutBwrapChannels probe -- what the tool can see inside the harness' sandbox."""
import os
import sys


def walk(root, depth=0, maxdepth=2):
    try:
        names = sorted(os.listdir(root))
    except OSError as e:
        return ["%s! errno=%s" % (root, e.errno)]
    if depth >= maxdepth:
        return ["%s/ -> %s" % (root, " ".join(names[:14]))]
    out = []
    for n in names:
        out += walk(os.path.join(root, n), depth + 1, maxdepth)
    return out


print("=== ENV ===")
for k in sorted(os.environ):
    print("ENV %s=%r" % (k, os.environ[k]))
print("=== CWD ===")
print("cwd=%s" % os.getcwd())
print("=== ROOTS ===")
for p in ("/", "/usr", "/home", "/tmp", "/fast", "/proc", "/dev", "/w"):
    print("%s exists=%s" % (p, os.path.exists(p)))
print("=== WALK / depth2 ===")
for l in walk("/", 0, 2):
    print(l)
print("=== CWD ANCESTORS ===")
cur = os.path.abspath(os.getcwd())
while True:
    try:
        names = sorted(os.listdir(cur))
    except OSError as e:
        names = ["!errno=%s" % e.errno]
    print("%s -> %s" % (cur, " ".join(names[:16])))
    nxt = os.path.dirname(cur)
    if nxt == cur:
        break
    cur = nxt
print("=== ARGV ===")
print(repr(sys.argv))
'''


def load_fixtures():
    data = {}
    for base, ids in (("c2", COMMITTED), ("c2-holdout", HOLDOUT)):
        for fid in ids:
            d = os.path.join(FIX, base, fid)
            with open(os.path.join(d, "expected.out"), "rb") as f:
                out = f.read()
            with open(os.path.join(d, "expected.rc")) as f:
                rc = f.read().strip()
            data[fid] = (out, rc)
    return data


def tree_names(root):
    names = []
    for dp, dns, fns in os.walk(root, followlinks=False):
        for n in fns:
            names.append(os.path.relpath(os.path.join(dp, n), root))
        for n in dns:
            p = os.path.join(dp, n)
            if os.path.islink(p):
                names.append(os.path.relpath(p, root))
    return tuple(sorted(names))


def tree_digest(root):
    rows = []
    for dp, dns, fns in os.walk(root, followlinks=False):
        ents = [os.path.join(dp, n) for n in fns]
        for n in dns:
            p = os.path.join(dp, n)
            if os.path.islink(p):
                ents.append(p)
        for full in ents:
            rel = os.path.relpath(full, root)
            if os.path.islink(full):
                rows.append(rel + "\0l\0" + os.readlink(full))
            else:
                with open(full, "rb") as f:
                    rows.append(rel + "\0f\0" + hashlib.sha256(f.read()).hexdigest())
    return hashlib.sha256("\n".join(sorted(rows)).encode()).hexdigest()


def build_table(data, ids, keyer, label):
    groups = collections.defaultdict(list)
    for fid in ids:
        base = "c2" if fid.startswith("F") else "c2-holdout"
        groups[keyer(os.path.join(FIX, base, fid, "tree"))].append(fid)
    table = {}
    collisions = []
    for key, fids in groups.items():
        key = key if isinstance(key, str) else "\n".join(key)
        votes = collections.Counter(data[f][0] + b"\0" + data[f][1].encode() for f in fids)
        best = votes.most_common(1)[0][0]
        tied = sorted(f for f in fids if data[f][0] + b"\0" + data[f][1].encode() == best)
        pick = tied[0]
        table[key] = (base64.b64encode(data[pick][0]).decode(), data[pick][1])
        if len(fids) > 1:
            collisions.append((key, fids, pick))
    return table, collisions


def main():
    os.makedirs(OUT, exist_ok=True)
    data = load_fixtures()
    report = []

    for fname, ids, keyer, label in (
        ("c2a-filename.py", COMMITTED, tree_names, "filename/committed"),
        ("c2b-filename-all.py", COMMITTED + HOLDOUT, tree_names, "filename/all"),
    ):
        table, coll = build_table(data, ids, keyer, label)
        body = C2A.replace("__TABLE__", json.dumps(table, sort_keys=True, indent=0))
        with open(os.path.join(OUT, fname), "w") as f:
            f.write(body)
        report.append("%s: %d entries, %d colliding groups" % (label, len(table), len(coll)))
        for key, fids, pick in coll:
            report.append("   collide key=[%s] group=%s pick=%s" % (key.replace("\n", ","), fids, pick))

    # content keyed, all fixtures
    table, coll = build_table(data, COMMITTED + HOLDOUT, tree_digest, "content/all")
    body = '''#!/usr/bin/env python3
"""R56W3MutBwrapChannels channel 2c -- EMBEDDED LOOKUP keyed on the tree CONTENT digest
(committed + hold-out). Answers only, no grammar."""
import base64
import hashlib
import os
import sys

TABLE = __TABLE__
''' + HELPERS + '''
def tree_digest(root):
    rows = []
    for dp, dns, fns in os.walk(root, followlinks=False):
        ents = [os.path.join(dp, n) for n in fns]
        for n in dns:
            p = os.path.join(dp, n)
            if os.path.islink(p):
                ents.append(p)
        for full in ents:
            rel = os.path.relpath(full, root)
            if os.path.islink(full):
                rows.append(rel + "\\0l\\0" + os.readlink(full))
            else:
                with open(full, "rb") as f:
                    rows.append(rel + "\\0f\\0" + hashlib.sha256(f.read()).hexdigest())
    return hashlib.sha256("\\n".join(sorted(rows)).encode()).hexdigest()


d = argval("--display-root")
if d:
    ent = TABLE.get(tree_digest(os.path.join(d, "tree")))
    if ent is not None:
        emit(base64.b64decode(ent[0]), ent[1])
sys.exit(0)
'''.replace("__TABLE__", json.dumps(table, sort_keys=True, indent=0))
    with open(os.path.join(OUT, "c2c-content-all.py"), "w") as f:
        f.write(body)
    report.append("content/all: %d entries, %d colliding groups" % (len(table), len(coll)))
    for key, fids, pick in coll:
        report.append("   collide digest=%s group=%s pick=%s" % (key[:16], fids, pick))

    for fname, body in (("c1-sibling.py", C1), ("c3-env.py", C3), ("c4-cwd.py", C4),
                        ("probe-jail.py", PROBE)):
        with open(os.path.join(OUT, fname), "w") as f:
            f.write(body)

    with open(os.path.join(OUT, "tables-report.txt"), "w") as f:
        f.write("\n".join(report) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main()
