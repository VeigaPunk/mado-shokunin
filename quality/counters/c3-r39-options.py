#!/usr/bin/env python3
"""PRED-C3-r39-v2 - the option-ownership tool resolves trees it has never seen.

Scores one committed revision REV of the lane (revision-addressed git reads,
ambient GIT_* removed; nothing in the lane is written). The tool is
`tools/mado-options.py` as committed at REV, run from a private temp copy.

  a  the tool exists at REV and the BASE revision lacks it (BASE holding the
     tool is a setup error, exit 2);
  g  the tool's top-level imports are standard-library only (no socket,
     urllib, http) - checked on the committed AST;
  b  `--selftest` exits 0 and prints `MADO_OPTIONS_SELFTEST: k/n passed` with
     k == n and n >= 40;
  c  fixtures: the counter GENERATES 8 config trees seeded by sha256(REV:i)
     (layered defaults/user/toggles-glob/relative source graph, nested
     categories, redeclarations, variables, `##` escapes, trailing comments,
     flag-variant binds, env/exec/animation/workspace handlers and keyed
     `windowrule { }` blocks as distractors) and computes the expected
     last-declarer table with its own reference model; a fixture passes iff
     the tool exits 0 and its rows equal the model exactly on the key set and
     on value, owner and line per key, with set=true;
     2 merge fixtures pass `--getoption` live JSON over generated trees and
     require the exact agreement label per row (agreement, agreement*,
     mismatch, config-only, live-default);
     1 strict fixture sources a FIFO: the tool must exit 3 naming the path;
  d  every row of every passing generated fixture carries the fields
     key, value, owner, layer, line, set.

Final line: `PRED-C3-r39-v2: fixtures=P/11 tool=present|absent
verdict=TARGET_MET|TARGET_MISSED rev=<full hash>`.
TARGET_MET iff a, b, d, g hold and P == 11; exit 0, else exit 1.
Because the trees are derived from REV, a tool that replays recorded fixture
outputs cannot pass; it has to resolve the source graph.
"""
import argparse
import ast
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

PRED = "PRED-C3-r39-v2"
BASE_DEFAULT = "08be4eb7fd13358ed29b096e8924005d46ac409c"
TOOL = "tools/mado-options.py"
FIELDS = {"key", "value", "owner", "layer", "line", "set"}
N_GEN, N_MERGE, N_STRICT = 8, 2, 1
TOTAL = N_GEN + N_MERGE + N_STRICT
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
STDLIB_DENY = {"socket", "urllib", "http", "requests", "ssl", "ftplib"}
STDLIB_ALLOW = {
    "argparse", "ast", "collections", "fnmatch", "glob", "hashlib", "io",
    "itertools", "json", "math", "os", "pathlib", "re", "shutil", "stat",
    "string", "subprocess", "sys", "tempfile", "textwrap", "time", "typing",
    "functools", "dataclasses", "errno",
}

POOL = {
    "general": ["gaps_in", "gaps_out", "border_size", "layout"],
    "decoration": ["rounding", "active_opacity"],
    "decoration:blur": ["enabled", "size", "passes"],
    "input": ["kb_layout", "repeat_rate", "follow_mouse"],
    "input:touchpad": ["natural_scroll", "scroll_factor"],
    "misc": ["vfr", "focus_on_activate"],
}
DISTRACTORS = [
    ["bindd = SUPER, K, Launch thing, exec, foot"],
    ["bindeld = , XF86AudioMute, Mute, exec, wpctl set-mute x toggle"],
    ["bindmd = SUPER, mouse:272, Move window, movewindow"],
    ["bind = SUPER, Q, killactive"],
    ["env = XCURSOR_SIZE,24"],
    ["exec-once = uwsm-app -- waybar"],
    ["animation = windows, 1, 3, default"],
    ["workspace = 3, default:true"],
    ["windowrule {", "    name = r%(n)d", "    match:class = app%(n)d",
     "    float = 1", "}"],
    ["# general:gaps_in = 999 (comment, never an option)"],
]


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                       env=ENV)
    return p.stdout if p.returncode == 0 else None


def resolve(repo, rev):
    out = git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    if not out:
        raise Setup("unresolved revision %s" % rev)
    return out.decode().strip()


# ---------------------------------------------------------------- generator
class Tree:
    """Generated config tree + reference last-declarer model."""

    def __init__(self, rng, tag):
        self.rng = rng
        self.tag = tag
        self.files = {}      # rel path -> list of items
        self.nvar = 0
        self.ndis = 0

    def value(self):
        r = self.rng.random()
        if r < 0.5:
            return str(self.rng.randint(2, 900))
        return "w%d" % self.rng.randint(10, 99999)

    def option_block(self, items):
        """Append category blocks with 1-4 options; return nothing."""
        cats = self.rng.sample(sorted(POOL), self.rng.randint(1, 3))
        for cat in cats:
            parts = cat.split(":")
            keys = self.rng.sample(POOL[cat],
                                   self.rng.randint(1, len(POOL[cat])))
            for depth, p in enumerate(parts):
                items.append(("raw", "    " * depth + p + " {"))
            ind = "    " * len(parts)
            for k in keys:
                v = self.value()
                style = self.rng.random()
                full = cat + ":" + k
                if style < 0.15:
                    self.nvar += 1
                    name = "mdvq%04d%s" % (self.nvar, self.tag)
                    items.append(("raw", "%s$%s = %s" % (ind, name, v)))
                    items.append(("opt", "%s%s = $%s" % (ind, k, name),
                                  full, v))
                elif style < 0.3:
                    items.append(("opt", "%s%s = %s # note %d"
                                  % (ind, k, v, self.rng.randint(1, 9)),
                                  full, v))
                elif style < 0.4:
                    items.append(("opt", "%s%s = ##%s" % (ind, k, v), full,
                                  "#" + v))
                else:
                    items.append(("opt", "%s%s = %s" % (ind, k, v), full, v))
            for depth in range(len(parts) - 1, -1, -1):
                items.append(("raw", "    " * depth + "}"))

    def distractor(self, items):
        self.ndis += 1
        for line in self.rng.choice(DISTRACTORS):
            items.append(("raw", line % {"n": self.ndis}))

    def body(self, items, n):
        for _ in range(n):
            if self.rng.random() < 0.35:
                self.distractor(items)
            else:
                self.option_block(items)

    def build(self):
        rng = self.rng
        dflt = ".local/share/omarchy/default/hypr/"
        user = ".config/hypr/"
        tog = ".local/state/omarchy/toggles/hypr/"
        root = user + "hyprland.conf"
        # defaults files, one of which sources a relative child
        dnames = ["d%d.conf" % i for i in range(rng.randint(2, 3))]
        for d in dnames:
            items = []
            self.body(items, rng.randint(1, 3))
            self.files[dflt + d] = items
        child = dflt + "sub/child.conf"
        citems = []
        self.body(citems, rng.randint(1, 2))
        self.files[child] = citems
        host = dflt + dnames[0]
        pos = rng.randint(0, len(self.files[host]))
        # insert the relative source between whole blocks only
        cut = 0
        depth = 0
        for idx, it in enumerate(self.files[host]):
            line = it[1].strip()
            depth += line.endswith("{") - (line == "}")
            if depth == 0 and idx + 1 <= pos:
                cut = idx + 1
        self.files[host].insert(cut, ("src", "source = ./sub/child.conf",
                                      [child]))
        # toggles: random names so sorted order != creation order
        tnames = sorted({"%s.conf" % "".join(rng.choice("abcdefghjkmnpq")
                                               for _ in range(5))
                         for _ in range(rng.randint(2, 3))})
        for t in tnames:
            items = []
            self.body(items, rng.randint(1, 2))
            self.files[tog + t] = items
        unames = ["u%d.conf" % i for i in range(rng.randint(1, 2))]
        for u in unames:
            items = []
            self.body(items, rng.randint(1, 3))
            self.files[user + u] = items
        ritems = []
        self.body(ritems, 1)
        srcs = ([("src", "source = ~/" + dflt + d, [dflt + d])
                 for d in dnames]
                + [("src", "source = ~/" + user + u, [user + u])
                   for u in unames]
                + [("src", "source = ~/" + tog + "*.conf",
                    [tog + t for t in tnames])])
        for s in srcs:
            ritems.append(s)
            if rng.random() < 0.5:
                self.body(ritems, 1)
        self.body(ritems, rng.randint(1, 2))
        self.files[root] = ritems
        self.root = root

    def render(self, home):
        for rel, items in self.files.items():
            path = os.path.join(home, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("".join(it[1] + "\n" for it in items))

    def expected(self):
        table = {}
        decls = {}

        def walk(rel):
            for lineno, it in enumerate(self.files[rel], 1):
                if it[0] == "opt":
                    table[it[2]] = {"value": it[3], "owner": rel,
                                    "line": lineno}
                    decls[it[2]] = decls.get(it[2], 0) + 1
                elif it[0] == "src":
                    for target in sorted(it[2]):
                        walk(target)
        walk(self.root)
        return table, decls


def gen_tree(rev, i):
    seed = int(hashlib.sha256(("%s:%d" % (rev, i)).encode()).hexdigest(), 16)
    t = Tree(random.Random(seed), "x%d" % i)
    t.build()
    return t


# ---------------------------------------------------------------- scoring
def run_tool(tool, home, extra=()):
    try:
        p = subprocess.run([sys.executable, "-I", tool, "--home", home,
                            *extra], capture_output=True, text=True,
                           timeout=60, env=ENV)
    except subprocess.TimeoutExpired:
        return None, "", "timeout"
    return p.returncode, p.stdout, p.stderr


def rows_of(stdout):
    try:
        rows = json.loads(stdout)
    except ValueError:
        return None
    if not isinstance(rows, list) or not all(isinstance(r, dict)
                                             for r in rows):
        return None
    return rows


def score_generated(tool, tmp, rev, i):
    tree = gen_tree(rev, i)
    home = os.path.join(tmp, "g%d" % i)
    tree.render(home)
    table, _ = tree.expected()
    rc, out, err = run_tool(tool, home)
    rows = rows_of(out) if rc == 0 else None
    if rows is None:
        return False, False, "rc=%s" % rc
    shape = all(FIELDS <= set(r) for r in rows)
    got = {r.get("key"): r for r in rows}
    if set(got) != set(table):
        extra = sorted(set(got) - set(table))[:3]
        miss = sorted(set(table) - set(got))[:3]
        return False, shape, "keys extra=%s missing=%s" % (extra, miss)
    for k, exp in table.items():
        r = got[k]
        if (r.get("value") != exp["value"] or r.get("owner") != exp["owner"]
                or r.get("line") != exp["line"] or r.get("set") is not True):
            return False, shape, "row %s got=%s exp=%s" % (
                k, (r.get("value"), r.get("owner"), r.get("line")),
                (exp["value"], exp["owner"], exp["line"]))
    return True, shape, "rows=%d" % len(rows)


def score_merge(tool, tmp, rev, i):
    tree = gen_tree(rev, 100 + i)
    home = os.path.join(tmp, "m%d" % i)
    tree.render(home)
    table, decls = tree.expected()
    rng = random.Random(int(hashlib.sha256(("%s:merge:%d" % (rev, i))
                                           .encode()).hexdigest(), 16))
    live, want = {}, {}
    for k in sorted(table):
        r = rng.random()
        v = table[k]["value"]
        if r < 0.45:
            live[k] = {"value": v, "custom_type": "str", "set": True}
            want[k] = "agreement*" if decls[k] > 1 else "agreement"
        elif r < 0.7:
            live[k] = {"value": v + "9", "custom_type": "str", "set": True}
            want[k] = "mismatch"
        else:
            want[k] = "config-only"
    for n in range(2):
        k = "zzlive%d:only%d" % (i, n)
        live[k] = {"value": "w%d" % n, "custom_type": "str", "set": False}
        want[k] = "live-default"
    lp = os.path.join(tmp, "m%d.json" % i)
    with open(lp, "w", encoding="utf-8") as fh:
        json.dump(live, fh)
    rc, out, err = run_tool(tool, home, ("--getoption", lp))
    rows = rows_of(out) if rc == 0 else None
    if rows is None:
        return False, "rc=%s" % rc
    got = {r.get("key"): r.get("agreement") for r in rows}
    if got != want:
        bad = sorted(k for k in set(got) | set(want)
                     if got.get(k) != want.get(k))[:3]
        return False, "labels differ at %s" % bad
    return True, "rows=%d" % len(rows)


def score_strict(tool, tmp):
    home = os.path.join(tmp, "s0")
    os.makedirs(os.path.join(home, ".config", "hypr"))
    fifo = os.path.join(home, "pipe.conf")
    os.mkfifo(fifo)
    with open(os.path.join(home, ".config", "hypr", "hyprland.conf"), "w",
              encoding="utf-8") as fh:
        fh.write("general {\n    gaps_in = 3\n}\nsource = ~/pipe.conf\n")
    rc, out, err = run_tool(tool, home)
    ok = rc == 3 and "pipe.conf" in err
    return ok, "rc=%s named=%d" % (rc, "pipe.conf" in err)


def imports_ok(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            mods.add((node.module or "").split(".")[0])
    return bool(mods) and mods <= STDLIB_ALLOW and not (mods & STDLIB_DENY)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    rev = resolve(repo, args.rev)
    base = resolve(repo, args.base)
    if git(repo, "cat-file", "-e", "%s:%s" % (base, TOOL)) is not None:
        raise Setup("precondition_failed tool_present_at_base")
    src = git(repo, "show", "%s:%s" % (rev, TOOL))
    present = src is not None
    cl = {"a": int(present), "b": 0, "d": 0, "g": 0}
    passed = 0
    if present:
        cl["g"] = int(imports_ok(src))
        tmp = tempfile.mkdtemp(prefix="mado-c3-r39-")
        try:
            tool = os.path.join(tmp, "mado-options.py")
            with open(tool, "wb") as fh:
                fh.write(src)
            try:
                p = subprocess.run([sys.executable, "-I", tool, "--selftest"],
                                   capture_output=True, text=True,
                                   timeout=300, env=ENV, cwd=tmp)
                m = re.search(r"MADO_OPTIONS_SELFTEST: (\d+)/(\d+) passed",
                              p.stdout)
                k, n = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
                cl["b"] = int(p.returncode == 0 and m is not None
                              and k == n and n >= 40)
                print("%s clause=b rc=%d selftest=%d/%d" % (
                    PRED, p.returncode, k, n))
            except subprocess.TimeoutExpired:
                print("%s clause=b timeout" % PRED)
            shapes = []
            for i in range(N_GEN):
                ok, shape, why = score_generated(tool, tmp, rev, i)
                passed += ok
                if ok:
                    shapes.append(shape)
                print("%s fixture=gen%d ok=%d %s" % (PRED, i, ok, why))
            cl["d"] = int(bool(shapes) and all(shapes))
            for i in range(N_MERGE):
                ok, why = score_merge(tool, tmp, rev, i)
                passed += ok
                print("%s fixture=merge%d ok=%d %s" % (PRED, i, ok, why))
            ok, why = score_strict(tool, tmp)
            passed += ok
            print("%s fixture=strict0 ok=%d %s" % (PRED, ok, why))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    met = all(cl.values()) and passed == TOTAL
    print("%s clauses=%s" % (PRED, " ".join("%s:%d" % kv
                                             for kv in sorted(cl.items()))))
    print("%s: fixtures=%d/%d tool=%s verdict=%s rev=%s" % (
        PRED, passed, TOTAL, "present" if present else "absent",
        "TARGET_MET" if met else "TARGET_MISSED", rev))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as exc:
        print("%s SETUP %s" % (PRED, exc))
        sys.exit(2)
