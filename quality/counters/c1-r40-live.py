#!/usr/bin/env python3
"""PRED-C1-r40-v1 - the option table merges a LIVE compositor in its native forms.

Scores one committed revision REV of the lane (revision-addressed git reads,
ambient GIT_* removed; nothing in the lane is written). The tool is
`tools/mado-options.py` as committed at REV (or `--tool PATH` for a control),
run from a private temp copy. The tool gains `--live` (query the compositor
through `hyprctl`), `--hyprctl PATH` (the program to run; default `hyprctl`) and
`--probe KEY` (repeatable; extra live keys that have no declarer).

Contract the counter enforces (the code below is the same sentence):

  * for every declared key the tool runs exactly `HYPRCTL getoption -j KEY`,
    once, and nothing else (the compositor's own read verb; no other argv);
  * native replies are one JSON object `{"option":K,"set":B,"<form>":V}` with
    form in int|float|str|custom - the four forms captured from the real
    compositor in `.ufo/waves/round-40/c1/native-capture.jsonl` (committed at
    the freeze); the plain text line `no such option` (exit 0) means the
    compositor has no such option -> label `config-only`;
  * the declared string is converted the way the host converts it:
      int     hyprlang v0.6.8 src/config.cpp:185-264 configStringToInt
              (0x hex; rgba(rrggbbaa | r,g,b,a) and rgb(rrggbb | r,g,b) as
              ARGB; prefixes true/on/yes -> 1 and false/off/no -> 0; decimal);
      float   stof;  str  exact trimmed equality;
      custom  by the live string's shape (Hyprland v0.56.2
              src/config/legacy/ConfigManager.cpp:103-170, src/config/shared/
              complex/ComplexDataTypes.hpp:69-77, 80-136, 154-175):
                gradient `<hex> ... <N>deg`  declared colours as ARGB, one
                  lowercase unpadded hex word each, then `<N>deg` (0deg when
                  no angle is declared);
                gap `a b c d`  declared 1-4 integers expanded CSS-style
                  (1: all; 2: v h; 3: t h b; 4: t r b l);
                font weight `<N>`  declared name (thin 100 ... ultraheavy
                  1000, case-insensitive);
    and compared with the live value; labels: `agreement` (equal, set, one
    declarer), `agreement*` (equal, set, more than one declarer), `mismatch`
    (value differs, or set=false although declared), `config-only`
    (`no such option`), and `live-default` for each `--probe KEY` the
    compositor answers and no declarer owns;
  * failures are named: the compositor program missing or exiting non-zero
    or answering non-JSON other than `no such option`, or an answer with no
    known form, exits 5 with the key on stderr; a probe key that is empty or
    starts with `-` exits 2 and no compositor program is run;
  * the tool writes nothing under the config root and runs no other program.

Fixtures (13): 8 generated trees seeded by sha256(REV:i) (each mixes every
type - including a gradient redeclared without an angle after one with an
angle - every label and the declared spellings the host uses), 1 probe tree,
2 failure trees (exit and malformed reply) and 1 missing-program tree, 1
hostile-probe tree; every negative fixture first requires the correct rows of
a valid live run on the same tree, so a tool that has no `--live` cannot pass
a negative fixture by refusing the flag.

Clauses: a  the tool exists at REV and BASE lacks `--live` (BASE already
accepting it is a setup error, exit 2); b  `--selftest` exits 0 printing
`MADO_OPTIONS_SELFTEST: k/n passed` with k == n and n >= 79 (base: 71);
g  top-level imports are standard library only and none of socket, urllib,
http, requests, ssl, ftplib; k  the native-capture receipt at REV holds the
four forms the counter's stub emits and 70 non-blank lines.

Final line: `PRED-C1-r40-v1: fixtures=P/13 tool=present|absent
verdict=TARGET_MET|TARGET_MISSED rev=<full hash>`.
TARGET_MET iff a, b, g, k hold and P == 13; exit 0, else exit 1.
Because the trees, values and perturbations derive from REV, a tool that
replays recorded output cannot pass; it has to convert and compare.
Residual (declared): a tool that hardcodes the reference model's tables for
this generator's value space passes; the live host receipt is the
out-of-distribution check and is reported, not scored.
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

PRED = "PRED-C1-r40-v1"
BASE_DEFAULT = "9fc511ddce708327377161202f358ce37dc266ba"
TOOL = "tools/mado-options.py"
CAPTURE = ".ufo/waves/round-40/c1/native-capture.jsonl"
N_GEN, TOTAL = 8, 13
MIN_SELFTEST = 79
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
STDLIB_DENY = {"socket", "urllib", "http", "requests", "ssl", "ftplib"}
STDLIB_ALLOW = {
    "argparse", "ast", "collections", "fnmatch", "glob", "hashlib", "io",
    "itertools", "json", "math", "os", "pathlib", "re", "shutil", "stat",
    "string", "subprocess", "sys", "tempfile", "textwrap", "time", "typing",
    "functools", "dataclasses", "errno",
}
WEIGHTS = {"thin": 100, "ultralight": 200, "light": 300, "semilight": 350,
           "book": 380, "normal": 400, "medium": 500, "semibold": 600,
           "bold": 700, "ultrabold": 800, "heavy": 900, "ultraheavy": 1000}
FORMS = ("int", "float", "str", "custom")


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


# ---------------------------------------------------------- reference model
def hl_int(v):
    """hyprlang v0.6.8 configStringToInt (config.cpp:185-264); None = error."""
    v = v
    if v.startswith("0x"):
        try:
            return int(v, 16)
        except ValueError:
            return None
    if v.startswith("rgba(") and v.endswith(")"):
        inner = v[5:-1].strip()
        if inner.count(",") == 3:
            parts = [p.strip() for p in inner.split(",")]
            r, g, b = (hl_int(p) for p in parts[:3])
            try:
                a = int(round(float(parts[3]) * 255.0)) & 0xFF
            except ValueError:
                return None
            if None in (r, g, b):
                return None
            return a * 0x1000000 + r * 0x10000 + g * 0x100 + b
        if len(inner) == 8:
            try:
                x = int(inner, 16)
            except ValueError:
                return None
            return (x >> 8) + 0x1000000 * (x & 0xFF)
        return None
    if v.startswith("rgb(") and v.endswith(")"):
        inner = v[4:-1].strip()
        if inner.count(",") == 2:
            r, g, b = (hl_int(p.strip()) for p in inner.split(","))
            if None in (r, g, b):
                return None
            return 0xFF000000 + r * 0x10000 + g * 0x100 + b
        if len(inner) == 6:
            try:
                return int(inner, 16) + 0xFF000000
            except ValueError:
                return None
        return None
    if v.startswith(("true", "on", "yes")):
        return 1
    if v.startswith(("false", "off", "no")):
        return 0
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return None


def gradient_text(declared, inherited=0):
    """Declared gradient -> the host's toString. Hyprland's gradient handler
    (ConfigManager.cpp:103-170) clears the colours and sets the angle only
    when a `deg` token is present, so a redeclaration without one keeps the
    angle the previous declarer left in the same option (`inherited`)."""
    cols, angle = [], inherited
    for tok in declared.split():
        if "deg" in tok:
            angle = int(tok[:tok.index("deg")])
            break
        c = hl_int(tok)
        if c is None:
            return None
        cols.append(c)
    if not cols:
        return None
    return " ".join("%x" % c for c in cols) + " %ddeg" % angle


def gap_text(declared):
    n = [int(x) for x in declared.split()]
    if len(n) == 1:
        n = n * 4
    elif len(n) == 2:
        n = [n[0], n[1], n[0], n[1]]
    elif len(n) == 3:
        n = [n[0], n[1], n[2], n[1]]
    return " ".join(str(x) for x in n[:4])


def model_equal(form, declared, live, live_custom_shape=None):
    d = declared.strip()
    if form == "int":
        return hl_int(d) == live
    if form == "float":
        try:
            return abs(float(d) - float(live)) < 1e-6
        except ValueError:
            return False
    if form == "str":
        return d == str(live).strip()
    shape = live_custom_shape
    try:
        if shape == "gradient":
            return gradient_text(d) == live
        if shape == "gap":
            return gap_text(d) == live
        if shape == "weight":
            return str(WEIGHTS.get(d.lower(), -1)) == live
    except ValueError:
        return False
    return d == live


# ----------------------------------------------------------------- generator
COLOUR_SPELL = [
    lambda r, g, b, a: "rgba(%02x%02x%02x%02x)" % (r, g, b, a),
    lambda r, g, b, a: "0x%02x%02x%02x%02x" % (a, r, g, b),
]
ALPHAS = ("1", "0.8", "0.4")   # alpha*255 is an exact integer: no rounding ties
RGB_SPELL = [
    lambda r, g, b: "rgb(%02x%02x%02x)" % (r, g, b),
    lambda r, g, b: "rgb(%d,%d,%d)" % (r, g, b),
]
BOOL_SPELL = ["yes", "true", "on", "1", "yes, please :)", "no", "off",
              "false", "0", "on # note"]
WSPELL = sorted(WEIGHTS)


class Fixture:
    def __init__(self, rng, tag):
        self.rng = rng
        self.tag = tag
        self.lines = []
        self.opts = {}      # key -> dict(form, shape, declared, decls, live)
        self.n = 0

    def rgb_bytes(self):
        r = self.rng
        return (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255),
                r.randint(0x10, 0xFF))

    def colour_decl(self):
        r, g, b, a = self.rgb_bytes()
        roll = self.rng.random()
        if roll < 0.25:
            return self.rng.choice(RGB_SPELL)(r, g, b)
        if roll < 0.5:
            return "rgba(%d,%d,%d,%s)" % (r, g, b, self.rng.choice(ALPHAS))
        return self.rng.choice(COLOUR_SPELL)(r, g, b, a)

    def make(self, kind, quirk=False):
        self.n += 1
        key = "opt%s%d:%s%d" % (self.tag, self.n, kind, self.n)
        rng = self.rng
        if kind == "bool":
            d = "yes, please :)" if quirk else rng.choice(BOOL_SPELL)
            return key, dict(form="int", shape=None, declared=d)
        if kind == "num":
            d = str(rng.randint(-5, -1)) if quirk else str(rng.randint(2, 900))
            return key, dict(form="int", shape=None, declared=d)
        if kind == "colour":
            d = ("rgba(%d,%d,%d,0.8)" % self.rgb_bytes()[:3]
                 if quirk else self.colour_decl())
            return key, dict(form="int", shape=None, declared=d)
        if kind == "float":
            d = ("%d.%d0" % (rng.randint(0, 2), rng.randint(1, 9))
                 if quirk else "%.2f" % rng.uniform(0, 3))
            return key, dict(form="float", shape=None, declared=d)
        if kind == "str":
            return key, dict(form="str", shape=None,
                             declared="w%d" % rng.randint(10, 99999))
        if kind == "grad":
            if quirk:
                cols = [self.colour_decl(), self.colour_decl()]
                ang = "45deg"
            else:
                cols = [self.colour_decl() for _ in range(rng.randint(1, 3))]
                ang = rng.choice((None, "0deg", "45deg", "90deg"))
            return key, dict(form="custom", shape="gradient",
                             declared=" ".join(cols + ([ang] if ang else [])))
        if kind == "ginh":
            cols = [self.colour_decl() for _ in range(rng.randint(1, 2))]
            return key, dict(form="custom", shape="gradient",
                             declared=" ".join(cols),
                             prior=rng.choice((45, 90, 135, 270)),
                             shadow=True)
        if kind == "gap":
            n = 3 if quirk else rng.randint(1, 4)
            return key, dict(form="custom", shape="gap",
                             declared=" ".join(str(rng.randint(0, 40))
                                               for _ in range(n)))
        d = "ultraheavy" if quirk else rng.choice(WSPELL)
        return key, dict(form="custom", shape="weight", declared=d)

    def live_of(self, o):
        """(native record body, expected equal-to-declared reply)."""
        f, d = o["form"], o["declared"]
        if f == "int":
            return hl_int(d.strip())
        if f == "float":
            return round(float(d), 2)
        if f == "str":
            return d
        if o["shape"] == "gradient":
            return gradient_text(d, o.get("prior", 0))
        if o["shape"] == "gap":
            return gap_text(d)
        return str(WEIGHTS[d.lower()])

    def perturb(self, o, live):
        f = o["form"]
        if f == "int":
            return live + 1
        if f == "float":
            return round(live + 0.5, 2)
        if f == "str":
            return live + "9"
        if o["shape"] == "gradient":
            return live.replace("deg", "7deg")
        if o["shape"] == "gap":
            return live + " 1"
        return str(int(live) + 1)

    def build(self):
        rng = self.rng
        kinds = ["bool", "num", "colour", "float", "str", "grad", "gap",
                 "weight", "ginh"]
        # first instance of every kind: quirk spelling, label agree; second
        # instances: differ x2, unset x2, absent x2 (6) -> 14 options
        second = ["differ", "differ", "unset", "unset", "absent", "absent"]
        rng.shuffle(second)
        second_kinds = rng.sample(kinds[:-1], 6)
        plan = [(k, True, "agree") for k in kinds]
        plan += [(k, False, lab) for k, lab in zip(second_kinds, second)]
        rng.shuffle(plan)
        for kind, quirk, lab in plan:
            key, o = self.make(kind, quirk)
            o["decls"] = 2 if o.get("shadow") else 1
            o["lab"] = lab
            live = self.live_of(o)
            o["live_equal"] = live
            o["live"] = live if lab in ("agree", "unset") else (
                self.perturb(o, live) if lab == "differ" else None)
            self.opts[key] = o
        # one earlier, different declarer for the first two agree keys
        shadow = [k for k, o in self.opts.items()
                  if o["lab"] == "agree" and o["decls"] == 1][:2]
        for k in shadow:
            self.opts[k]["decls"] = 2
        self.lines = []
        for k, o in self.opts.items():
            cat, name = k.split(":")
            if o["decls"] == 2:
                early = ("rgba(11223344) %ddeg" % o["prior"]
                         if o.get("shadow") else "0x1")
                self.lines += ["%s {" % cat, "    %s = %s" % (name, early),
                               "}"]
            if o["form"] == "float" and rng.random() < 0.5:
                pass
            self.lines += ["%s {" % cat, "    %s = %s" % (name, o["declared"]),
                           "}"]
        # distractors that must not become keys
        self.lines += ["bind = SUPER, Q, killactive",
                       "env = XCURSOR_SIZE,24",
                       "# general:zzcomment = 1"]

    def table(self):
        """key -> native record (None = `no such option`)."""
        t = {}
        for k, o in self.opts.items():
            if o["lab"] == "absent":
                t[k] = None
                continue
            f = o["form"]
            rec = {"option": k, f: o["live"], "set": o["lab"] != "unset"}
            t[k] = rec
        return t

    def want(self):
        w = {}
        for k, o in self.opts.items():
            if o["lab"] == "absent":
                w[k] = "config-only"
            elif o["lab"] in ("unset", "differ"):
                w[k] = "mismatch"
            else:
                w[k] = "agreement*" if o["decls"] > 1 else "agreement"
        return w

    def render(self, home):
        path = os.path.join(home, ".config", "hypr", "hyprland.conf")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(self.lines) + "\n")


STUB = r'''#!%(py)s
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "calls.log"), "a") as fh:
    fh.write(json.dumps(sys.argv[1:]) + "\n")
mode = open(os.path.join(here, "mode")).read().strip()
table = json.load(open(os.path.join(here, "table.json")))
if sys.argv[1:3] != ["getoption", "-j"] or len(sys.argv) != 4:
    sys.stdout.write("bad request\n")
    sys.exit(0)
key = sys.argv[3]
if mode.startswith("fail:") and key == mode[5:]:
    sys.stderr.write("stub failure\n")
    sys.exit(1)
if mode.startswith("bad:") and key == mode[4:]:
    sys.stdout.write("{not json\n")
    sys.exit(0)
rec = table.get(key, "absent")
if rec is None or rec == "absent":
    sys.stdout.write("no such option\n")
else:
    sys.stdout.write(json.dumps(rec) + "\n")
'''


def make_stub(tmp, name, table, mode="ok"):
    d = os.path.join(tmp, name)
    os.makedirs(d)
    path = os.path.join(d, "hyprctl")
    with open(path, "w") as fh:
        fh.write(STUB % {"py": sys.executable})
    os.chmod(path, 0o755)
    with open(os.path.join(d, "table.json"), "w") as fh:
        json.dump(table, fh)
    with open(os.path.join(d, "mode"), "w") as fh:
        fh.write(mode)
    open(os.path.join(d, "calls.log"), "w").close()
    return path


def calls_of(stub):
    with open(os.path.join(os.path.dirname(stub), "calls.log")) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def run_tool(tool, home, extra, timeout=60):
    try:
        p = subprocess.run([sys.executable, "-I", tool, "--home", home,
                            *extra], capture_output=True, text=True,
                           timeout=timeout, env=ENV)
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


def tree_listing(home):
    out = []
    for root, _, files in os.walk(home):
        for f in files:
            p = os.path.join(root, f)
            out.append((p, os.path.getsize(p), os.path.getmtime(p)))
    return sorted(out)


def check_live(tool, tmp, fx, name, probes=(), expect_extra=None):
    """Valid live run; returns (ok, why, stub, home); checks argv + no writes."""
    home = os.path.join(tmp, name + "-home")
    fx.render(home)
    table = fx.table()
    for k, v in (expect_extra or {}).items():
        table[k] = v
    stub = make_stub(tmp, name, table)
    before = tree_listing(home)
    extra = ["--live", "--hyprctl", stub]
    for p in probes:
        extra += ["--probe", p]
    rc, out, err = run_tool(tool, home, extra)
    rows = rows_of(out) if rc == 0 else None
    if rows is None:
        return False, "rc=%s err=%s" % (rc, err.strip()[:80]), stub, home
    if tree_listing(home) != before:
        return False, "config root modified", stub, home
    want = fx.want()
    for k, v in (expect_extra or {}).items():
        want[k] = "live-default"
    got = {r.get("key"): r.get("agreement") for r in rows}
    if got != want:
        bad = sorted(k for k in set(got) | set(want)
                     if got.get(k) != want.get(k))[:3]
        return False, "labels differ at %s (got=%s want=%s)" % (
            bad, [got.get(k) for k in bad], [want.get(k) for k in bad]), stub, home
    need = set(want) - set(expect_extra or {})
    seen = calls_of(stub)
    flat = [c[2] for c in seen if len(c) == 3 and c[:2] == ["getoption", "-j"]]
    if len(seen) != len(flat) or sorted(flat) != sorted(
            need | set(probes)) or len(flat) != len(set(flat)):
        return False, "argv shape: %s" % seen[:2], stub, home
    for r in rows:
        if r.get("agreement") != "live-default" and r.get("live") is None \
                and want.get(r.get("key")) != "config-only":
            return False, "row %s lacks live" % r.get("key"), stub, home
    return True, "rows=%d" % len(rows), stub, home


def score_generated(tool, tmp, rev, i):
    seed = int(hashlib.sha256(("%s:%d" % (rev, i)).encode()).hexdigest(), 16)
    fx = Fixture(random.Random(seed), "x%d" % i)
    fx.build()
    ok, why, _, _ = check_live(tool, tmp, fx, "g%d" % i)
    return ok, why


def small_fixture(rev, tag):
    seed = int(hashlib.sha256(("%s:%s" % (rev, tag)).encode()).hexdigest(), 16)
    fx = Fixture(random.Random(seed), tag)
    fx.build()
    return fx


def score_probe(tool, tmp, rev):
    fx = small_fixture(rev, "probe")
    extra = {"zzprobe:one": {"option": "zzprobe:one", "int": 3, "set": False},
             "zzprobe:two": {"option": "zzprobe:two", "str": "q", "set": False}}
    ok, why, _, _ = check_live(tool, tmp, fx, "p0",
                            probes=("zzprobe:one", "zzprobe:two",
                                    "zzprobe:nothing"),
                            expect_extra=extra)
    return ok, why


def score_fail(tool, tmp, rev, kind):
    fx = small_fixture(rev, kind)
    ok, why, _, home = check_live(tool, tmp, fx, kind + "-ok")
    if not ok:
        return False, "valid run: " + why
    victim = sorted(fx.opts)[3]
    stub = make_stub(tmp, kind + "-bad", fx.table(),
                     "%s:%s" % (kind, victim))
    rc, out, err = run_tool(tool, home, ["--live", "--hyprctl", stub])
    named = victim in err
    return rc == 5 and named, "rc=%s named=%d" % (rc, named)


def score_missing(tool, tmp, rev):
    fx = small_fixture(rev, "missing")
    ok, why, _, home = check_live(tool, tmp, fx, "m0")
    if not ok:
        return False, "valid run: " + why
    gone = os.path.join(tmp, "no-such-dir", "hyprctl")
    rc, out, err = run_tool(tool, home, ["--live", "--hyprctl", gone])
    return rc == 5 and "hyprctl" in err, "rc=%s" % rc


def score_hostile(tool, tmp, rev):
    fx = small_fixture(rev, "hostile")
    ok, why, _, home = check_live(tool, tmp, fx, "h0")
    if not ok:
        return False, "valid run: " + why
    stub = make_stub(tmp, "h0-bad", fx.table())
    good = True
    for bad in ("-x", "--version", ""):
        rc, out, err = run_tool(tool, home, ["--live", "--hyprctl", stub,
                                             "--probe", bad])
        good &= rc == 2 and "probe" in err.lower() and not calls_of(stub)
    return good, "all three refused=%d" % good


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


def capture_ok(blob):
    if blob is None:
        return False
    lines = [l for l in blob.decode("utf-8", "replace").splitlines()
             if l.strip()]
    if len(lines) != 70:
        return False
    seen = set()
    for l in lines:
        try:
            o = json.loads(l)
        except ValueError:
            return False
        forms = [k for k in o if k in FORMS]
        if "option" not in o or "set" not in o or len(forms) != 1:
            return False
        seen.add(forms[0])
    return seen == set(FORMS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--tool", default=None,
                    help="score this file instead of REV's tool (controls)")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    rev = resolve(repo, args.rev)
    base = resolve(repo, args.base)
    base_src = git(repo, "show", "%s:%s" % (base, TOOL))
    if base_src is not None and b"--live" in base_src:
        raise Setup("precondition_failed live_present_at_base")
    if args.tool:
        with open(args.tool, "rb") as fh:
            src = fh.read()
    else:
        src = git(repo, "show", "%s:%s" % (rev, TOOL))
    present = src is not None
    cl = {"a": int(present), "b": 0, "g": 0,
          "k": int(capture_ok(git(repo, "show", "%s:%s" % (rev, CAPTURE))))}
    passed = 0
    if present:
        cl["g"] = int(imports_ok(src))
        tmp = tempfile.mkdtemp(prefix="mado-c1-r40-")
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
                              and k == n and n >= MIN_SELFTEST)
                print("%s clause=b rc=%d selftest=%d/%d" % (
                    PRED, p.returncode, k, n))
            except subprocess.TimeoutExpired:
                print("%s clause=b timeout" % PRED)
            for i in range(N_GEN):
                ok, why = score_generated(tool, tmp, rev, i)
                passed += ok
                print("%s fixture=gen%d ok=%d %s" % (PRED, i, ok, why))
            for name, fn in (
                    ("probe0", lambda: score_probe(tool, tmp, rev)),
                    ("fail0", lambda: score_fail(tool, tmp, rev, "fail")),
                    ("bad0", lambda: score_fail(tool, tmp, rev, "bad")),
                    ("missing0", lambda: score_missing(tool, tmp, rev)),
                    ("hostile0", lambda: score_hostile(tool, tmp, rev))):
                ok, why = fn()
                passed += ok
                print("%s fixture=%s ok=%d %s" % (PRED, name, ok, why))
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
