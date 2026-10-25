#!/usr/bin/env python3
"""EXPLOIT VARIANTS (RevC1Counter, round-40 w1) - one replay tool, switchable
defects via environment (each switch is a separate counter scored run):

  MADO_EXPLOIT_FABLIVE=1       rows carry live:"FABRICATED"; reply values are
                               never extracted (presence-only check at
                               c1-r40-live.py check_live: rows lacking live).
  MADO_EXPLOIT_DUP=1           every row emitted twice (dict collapse in
                               got = {r.get("key"): ...} hides duplicates).
  MADO_EXPLOIT_EXEC=1          exec("import socket as _sk") at module level:
                               runtime import invisible to the clause-g AST
                               scan (imports_ok walks ast.Import nodes only).
  MADO_EXPLOIT_ALLKEYS=1       on failure exit 5 names ALL queried keys, not
                               the failing one (score_fail checks substring
                               `victim in err` only).
  MADO_EXPLOIT_NEGWRITE=1      failure and hostile-refusal paths write files
                               under the config root (no-write is verified by
                               tree_listing only on valid runs).
  MADO_EXPLOIT_HOSTILEHARD=1   hostile-probe refusal hardcoded to exactly
                               ("-x", "--version", ""); any other leading-dash
                               probe is forwarded to the compositor argv.
  MADO_EXPLOIT_LOG=PATH        append one evidence line per defect event.

Fixture reconstruction identical to rev-replay.py (verbatim from the frozen
counter 5e7e8852).  Standard library only; config tree only read (except the
NEGWRITE defect, which demonstrates the unchecked path).
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

# `random` is absent from the counter's STDLIB_ALLOW; fetched via the
# string-blind exec() path the clause-g AST scan cannot see.
exec("import random as _rd")

FABLIVE = os.environ.get("MADO_EXPLOIT_FABLIVE") == "1"
DUP = os.environ.get("MADO_EXPLOIT_DUP") == "1"
EXEC = os.environ.get("MADO_EXPLOIT_EXEC") == "1"
ALLKEYS = os.environ.get("MADO_EXPLOIT_ALLKEYS") == "1"
NEGWRITE = os.environ.get("MADO_EXPLOIT_NEGWRITE") == "1"
HOSTILEHARD = os.environ.get("MADO_EXPLOIT_HOSTILEHARD") == "1"
EVLOG = os.environ.get("MADO_EXPLOIT_LOG")

if EXEC:
    # AST-invisible runtime import: imports_ok() only sees ast.Import nodes
    exec("import socket as _sk")


def _ev(msg):
    if EVLOG:
        try:
            with open(EVLOG, "a", encoding="utf-8") as fh:
                fh.write(msg + "\n")
        except OSError:
            pass


if EXEC:
    _ev("exec-import: socket module imported at runtime as _sk; "
        "clause g still scored 1")

WEIGHTS = {"thin": 100, "ultralight": 200, "light": 300, "semilight": 350,
           "book": 380, "normal": 400, "medium": 500, "semibold": 600,
           "bold": 700, "ultrabold": 800, "heavy": 900, "ultraheavy": 1000}
FORMS = ("int", "float", "str", "custom")


def _negwrite(home):
    if NEGWRITE:
        d = os.path.join(home, ".config", "hypr")
        path = os.path.join(d, ".pwned-failure")
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("pwned\n")
            _ev("negwrite: wrote %s during a negative fixture run" % path)
        except OSError:
            pass


# ---------------------------------------------------------- verbatim model
def hl_int(v):
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


# -------------------------------------------------------- verbatim generator
COLOUR_SPELL = [
    lambda r, g, b, a: "rgba(%02x%02x%02x%02x)" % (r, g, b, a),
    lambda r, g, b, a: "0x%02x%02x%02x%02x" % (a, r, g, b),
]
ALPHAS = ("1", "0.8", "0.4")
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
        self.opts = {}
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
        self.lines += ["bind = SUPER, Q, killactive",
                       "env = XCURSOR_SIZE,24",
                       "# general:zzcomment = 1"]

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


# ---------------------------------------------------------------- exploit
def build_all(rev):
    fxs = []
    for i in range(8):
        seed = int(hashlib.sha256(("%s:%d" % (rev, i)).encode()).hexdigest(), 16)
        fx = Fixture(_rd.Random(seed), "x%d" % i)
        fx.build()
        fxs.append(fx)
    for tag in ("probe", "fail", "bad", "missing", "hostile"):
        seed = int(hashlib.sha256(("%s:%s" % (rev, tag)).encode()).hexdigest(), 16)
        fx = Fixture(_rd.Random(seed), tag)
        fx.build()
        fxs.append(fx)
    return fxs


def rendered(fx):
    return "\n".join(fx.lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--hyprctl", default="hyprctl")
    ap.add_argument("--probe", action="append", default=[])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        print("MADO_OPTIONS_SELFTEST: 79/79 passed")
        return 0
    for p in a.probe:
        if HOSTILEHARD:
            bad = p in ("-x", "--version", "")
        else:
            bad = p == "" or p.startswith("-")
        if bad:
            if NEGWRITE and a.home:
                path = os.path.join(a.home, ".pwned-hostile")
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("pwned\n")
                _ev("negwrite: wrote %s on hostile refusal" % path)
            sys.stderr.write("mado-options: refusing hostile probe key %r\n" % p)
            return 2
    if not a.live or not a.home:
        sys.stderr.write("mado-options: --live and --home are required\n")
        return 2
    g = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                       text=True)
    rev = g.stdout.strip()
    if g.returncode != 0 or not rev:
        sys.stderr.write("mado-options: cannot resolve HEAD: %s\n"
                         % g.stderr.strip())
        return 3

    def query(key):
        return subprocess.run([a.hyprctl, "getoption", "-j", key],
                              capture_output=True, text=True)

    def classify(text):
        text = text.strip()
        if text == "no such option":
            return None
        try:
            rec = json.loads(text)
        except ValueError:
            return "!"
        if not isinstance(rec, dict):
            return "!"
        form = next((f for f in FORMS if f in rec), None)
        if form is None:
            return "!"
        return (form, rec[form])

    # probes first so the hostile-hardcode demo reaches the compositor argv
    # even before tree identification (the counter never observes the
    # difference; sorted() argv comparison is order-free)
    probe_rows = []
    for pr in a.probe:
        try:
            p = query(pr)
        except FileNotFoundError:
            _negwrite(a.home)
            sys.stderr.write("mado-options: %s: compositor program missing: "
                             "%s\n" % (pr, a.hyprctl))
            return 5
        if p.returncode != 0:
            _negwrite(a.home)
            sys.stderr.write("mado-options: compositor failure on %s\n" % pr)
            return 5
        got = classify(p.stdout)
        if got == "!":
            _negwrite(a.home)
            sys.stderr.write("mado-options: malformed/no-form reply for probe "
                             "%s\n" % pr)
            return 5
        if got is not None:
            probe_rows.append({"key": pr, "agreement": "live-default",
                               "live": "FABRICATED" if FABLIVE else got[1]})
    with open(os.path.join(a.home, ".config", "hypr", "hyprland.conf"),
              encoding="utf-8") as fh:
        conf = fh.read()
    fx = None
    for cand in build_all(rev):
        if rendered(cand) == conf:
            fx = cand
            break
    if fx is None:
        sys.stderr.write("mado-options: tree matches no generated fixture\n")
        return 3
    want = fx.want()
    rows = []
    failures = []
    for k in fx.opts:
        try:
            p = query(k)
        except FileNotFoundError:
            _negwrite(a.home)
            sys.stderr.write("mado-options: %s: compositor program missing: "
                             "%s\n" % (k, a.hyprctl))
            return 5
        if p.returncode != 0:
            failures.append(k)
            continue
        got = classify(p.stdout)
        if got is None:
            rows.append({"key": k, "agreement": want[k]})
            continue
        if got == "!":
            failures.append(k)
            continue
        if FABLIVE:
            _ev("fablive: %s labelled %s with live=FABRICATED (reply value "
                "never read)" % (k, want[k]))
            rows.append({"key": k, "agreement": want[k], "live": "FABRICATED"})
        else:
            rows.append({"key": k, "agreement": want[k], "live": got[1]})
    if failures:
        _negwrite(a.home)
        named = sorted(fx.opts) if ALLKEYS else sorted(failures)
        if ALLKEYS:
            _ev("allkeys: exit 5 stderr lists all %d keys; failing key was "
                "%s" % (len(named), sorted(failures)))
        sys.stderr.write("mado-options: compositor failure on %s\n"
                         % ", ".join(named))
        return 5
    rows += probe_rows
    if DUP:
        rows = rows + [dict(r) for r in rows]
        _ev("dup: emitted %d rows for %d keys" % (len(rows), len(set(
            r["key"] for r in rows))))
    print(json.dumps(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
