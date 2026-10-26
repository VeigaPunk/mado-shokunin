#!/usr/bin/env python3
"""Differential fuzz: my mado-geometry.py vs the C1 counter's model_out."""
import importlib.util
import json
import os
import random
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = LANE + "/quality/counters/c1-r42-geometry.py"
MINE = os.environ.get(
    "MINE_PATH",
    LANE + "/.ufo/waves/round-43/w1/ExecIndepB/mado-geometry.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


judge = load("judge", COUNTER)
mine_tool = load("mine_tool", MINE)
SETUP = "MADO_GEOMETRY: SETUP "


def mine(raw, texts):
    blobs = [t.encode("utf-8") for t in texts]
    code, lines = mine_tool.pipeline(raw, blobs)
    if code == 2 and len(lines) == 1 and lines[0].startswith(SETUP):
        return None, lines[0][len(SETUP):]
    return "\n".join(lines) + "\n", code


def model(raw, texts):
    return judge.model_out(raw, texts)


def flat(res, texts):
    out, rc = res
    if out is None:
        return ("setup", rc)
    return (rc, out)


def compare(case):
    raw, texts = case
    a = flat(model(raw, list(texts)), texts)
    b = flat(mine(raw, list(texts)), texts)
    return a, b


def sig(res):
    kind = res[0]
    out = res[1]
    if kind == "setup":
        return ("setup", out)
    return (kind, tuple(line.split(" ")[0] for line in out.split("\n")),
            len(out))


CLIENTS_POOL = [
    {}, {"class": "a"}, {"class": "a", "mapped": True},
    {"class": "a", "mapped": False}, {"class": "a", "mapped": 0},
    {"class": "a", "mapped": None}, {"class": "a", "mapped": "false"},
    {"class": "a", "mapped": False, "size": [1, 2]},
    {"class": "a", "floating": True, "size": [1, 2], "mapped": True},
    {"class": "a", "floating": False, "size": [1, 2], "mapped": True},
    {"class": "a", "floating": 1, "size": [1, 2], "mapped": True},
    {"class": "a", "floating": "true", "size": [1, 2]},
    {"class": "a", "size": [0, 0]}, {"class": "a", "size": [1]},
    {"class": "a", "size": []}, {"class": "a", "size": [1, 2, 3]},
    {"class": "a", "size": [True, 2]}, {"class": "a", "size": [1, True]},
    {"class": "a", "size": [1.0, 2]}, {"class": "a", "size": [-1, 2]},
    {"class": "a", "size": "1x2"}, {"class": "a", "size": None},
    {"class": "a", "address": "0x1"}, {"class": "a", "address": 7},
    {"class": "a", "address": None}, {"class": "a", "address": True},
    {"class": 7}, {"class": None}, {"class": True}, {"class": ["a"]},
    {"class": "org.omarchy.gkeep", "floating": True, "size": [420, 500]},
    {"class": "a\x01"}, {"class": "\x00"}, {"class": "a\nb"},
    {"class": "\u00e9"}, {"class": "\u6c49\u5b57"},
    {"class": "\U0001f600"}, {"class": "A.b"},
]
CLIENT_EXTRAS = [
    {"class": "a", "size": [10 ** 12, 1]},
    {"class": "a", "size": [float("nan"), 1]},
    {"class": "a", "size": [float("inf"), 1]},
    {"class": "a", "floating": True, "size": [1, 2], "address": "0x\"q"},
    {"class": "a\x7f"},
    {"class": "a", "size": [1, 2], "extra": {"deep": [1, 2, 3]}},
]
RX_POOL = ["^(.+)$", "^(.*)$", ".+", "a.b", "^(a|a b)$", "^(a)$", "a", "a.*", ".*", "^$", "", "(", ")", "a**", "a*+",
           "a++", "a?+", "a(?i)b", "(?:a)", "a\\d", "a\\.b", "a\\-b", "a\\\\b",
           "a\\q", "a\\", "\\", "a|b", "a+b?", "[a]", "a{1,2}", "^org\\..*$",
           "x" * 200, "y" * 201, "a b", "a,b", "a\tb", "\u00e9", "a*b*c*",
           "a?b?c?", "((a))", "\\^\\$", "a\\.\\.b"]
EFFECT_POOL = ["size", "float", "center", "bind", "noshadow", "Size", "SIZE",
               "size ", " size", "size\t", "size 1 2 3", "float on off",
               "float on", "float off", "float maybe", "size", "float"]
ARG_POOL = ["1 2", "0 0", "420 500", "0042 0500", "1", "1 2 3", "12345 1",
            "123456 1", "-1 2", "+1 2", "1 -2", "1  2", "1\t2", "1 a",
            "99999 99999", "00000 00000"]
FIELD1_POOL = ["match:class {rx}", "match:class  {rx}", "match:class\t{rx}",
               "match:class{rx}", "match:class ", "match:class", "match:classes {rx}",
               "class {rx}", "match:class {rx} "]


def gen_rule(rng):
    head = rng.choice(["windowrule", "windowrule", "windowrule", "windowrulev2",
                       "WindowRule", "#windowrule", "  windowrule", "windowruleX"])
    sep = rng.choice(["=", " =", "= ", " = ", "  =", "\t=", "=\t", " ", ""])
    effect = rng.choice(EFFECT_POOL)
    args = rng.choice(ARG_POOL)
    field0 = effect
    if rng.random() < 0.8:
        field0 = effect + rng.choice([" ", "\t", "  "]) + args
    field1 = rng.choice(FIELD1_POOL).format(rx=rng.choice(RX_POOL))
    body = field0 + rng.choice([",", ", ", " ,", ",\t", ",,"]) + field1
    if rng.random() < 0.15:
        body += rng.choice([",", ", x", ", match:class ^(a)$"])
    if rng.random() < 0.1:
        body = body.rstrip()
    return rng.choice(["", "\t", " "]) + head + sep + body + rng.choice(
        ["", " ", "\t", "  "])


def gen_case(rng):
    nfiles = rng.randint(0, 3)
    texts = []
    for _ in range(nfiles):
        nlines = rng.randint(0, 6)
        lines = []
        for _ in range(nlines):
            if rng.random() < 0.15:
                lines.append(rng.choice(["", "\t", "  ", "# c", "windowrulev2 = size 1 2, match:class ^(a)$"]))
            else:
                lines.append(gen_rule(rng))
        sep = rng.choice(["\n", "\n", "\n", "\r\n"])
        texts.append(sep.join(lines) + rng.choice(["", "\n"]))
    nclients = rng.randint(0, 10)
    doc = []
    pool = CLIENTS_POOL + CLIENT_EXTRAS
    for _ in range(nclients):
        pick = dict(rng.choice(pool))
        if rng.random() < 0.3:
            pick = {}
        doc.append(pick)
    raw = json.dumps(doc).encode("utf-8")
    if rng.random() < 0.05:
        raw = json.dumps(doc, indent=None).encode() + rng.choice([b"\n", b" "])
    return raw, texts


def adversarial():
    cases = []
    A = cases.append
    good = "windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$"
    size = lambda a, rx="^(a)$": "windowrule = size %s, match:class %s" % (a, rx)
    flt = lambda a, rx="^(a)$": "windowrule = float %s, match:class %s" % (a, rx)
    cl = lambda obj: json.dumps([obj]).encode()
    one = cl({"class": "a", "floating": True, "size": [1, 2], "mapped": True})

    # rule line shape
    for line in ["windowrule = size 1 2, match:class ^(a)$", "windowrule=size 1 2, match:class ^(a)$",
                 "windowrule\t=size 1 2, match:class ^(a)$", "windowrule \t = size 1 2, match:class ^(a)$",
                 " windowrule = size 1 2, match:class ^(a)$", "windowrule x = size 1 2, match:class ^(a)$",
                 "windowrule = = size 1 2, match:class ^(a)$", "windowrule = size 1 2, match:class ^(a)$ =",
                 "windowrule", "windowrule ", "windowrule=", "windowrule =", "windowrule = ",
                 "windowrules = size 1 2, match:class ^(a)$", "xwindowrule = size 1 2, match:class ^(a)$",
                 "windowrulev2 = size 1 2, match:class ^(a)$", "WindowRule = size 1 2, match:class ^(a)$",
                 "windowrule = size 1 2, match:class ^(a)$,,", "windowrule = , match:class ^(a)$",
                 "windowrule = size, match:class ^(a)$", "windowrule = size , match:class ^(a)$",
                 "windowrule = size 1, match:class ^(a)$", "windowrule = size 1 2 3 4, match:class ^(a)$",
                 "windowrule = float, match:class ^(a)$", "windowrule = float ON, match:class ^(a)$",
                 "windowrule = size 1 2,match:class ^(a)$", "windowrule = size 1 2 , match:class ^(a)$ ",
                 "windowrule = size 1 2, match:class ^(a)$ # note", "windowrule = size 1 2,  match:class ^(a)$",
                 "windowrule = size 1 2, match:class\t^(a)$", "windowrule = size 1 2, match:class\u00a0^(a)$"]:
        A((one, [line]))
    # commas and empty fields
    for body in ["a,b", ",", ",,", " size 1 2 , match:class ^(a)$ ,", "size 1 2, match:class ^(a)$,,",
                 "size 1 2, match:class ^(a)$ , , ", "\tsize\t1\t2\t,\tmatch:class\t^(a)$\t"]:
        A((one, ["windowrule =" + body]))
    # regex alphabet and compile boundary
    for rx in ["", "a" * 199, "a" * 200, "a" * 201, "\\", "\\\\", "\\\\.", "\\.",
               "\\-", "\\(", "\\)", "\\|", "\\*", "\\+", "\\?", "\\^", "\\$",
               "\\a", "\\0", "\\n", "\\t", "\\ ", "\\,", "\\.\\-", "a\\", "ab\\",
               "(?", "(?i)", "(?#x)", "*+", "++", "?+", "a*+b", "a++b", "a?+b",
               "(())", "()", "|", "||", "a|", "|a", "*", "+", "?", "^", "$",
               "^$", ".", "..", "a.b", "a_b", "-", "^a-b$", "a{2}", "[^a]",
               "a\u00e9", "a b", "a\tb", "\x00", "a\x7f", "A.Z", "0-9"]:
        A((one, ["windowrule = size 1 2, match:class " + rx]))
        A((one, [flt("on", rx) if rx.isprintable() else flt("on")]))
    # args
    for args in ["0 0", "00 00", "0000000 1", "1 00000", "99999 99999",
                 "100000 1", "1 2 3", "1", "", "1 2 ", " 1 2", "1\t2",
                 "1  2", "-1 2", "1 -2", "+1 2", "1.0 2", "1e2 2", "١ ٢"]:
        A((one, [size(args)]))
    # multiple files / numbering
    A((one, [good, flt("on"), size("3 4")]))
    A((one, [size("1 1"), "", size("2 2")]))
    A((one, [good, good, good]))
    # float rule interplay
    A((cl({"class": "a", "floating": True, "size": [1, 2]}), [size("1 2"), flt("off")]))
    A((cl({"class": "a", "floating": False, "size": [1, 2]}), [size("1 2"), flt("off")]))
    A((cl({"class": "a", "floating": True, "size": [1, 2]}), [flt("on"), size("1 2")]))
    A((cl({"class": "a"}), [flt("on"), flt("off")]))
    # clients
    for obj in [{}, {"mapped": False}, {"mapped": 0}, {"mapped": None},
                {"mapped": "false"}, {"mapped": False, "class": "a", "size": [1, 2]},
                {"class": True}, {"class": 0}, {"class": None},
                {"class": "a", "floating": 1}, {"class": "a", "floating": "true"},
                {"class": "a", "floating": None}, {"class": "a", "floating": 0},
                {"class": "a", "size": [True, 2]}, {"class": "a", "size": [2, True]},
                {"class": "a", "size": [False, False]}, {"class": "a", "size": [1.5, 2]},
                {"class": "a", "size": [-0, 2]}, {"class": "a", "size": [0, 0]},
                {"class": "a", "size": [10 ** 40, 1]},
                {"class": "a", "size": [1, 2], "address": 1},
                {"class": "a", "address": "x"}, {"class": "a", "address": ""},
                {"class": "a", "address": "\u00e9"}, {"class": "a", "address": "q\"q"},
                {"class": "a\x00"}, {"class": "a\x1f"}, {"class": "a\x20"},
                {"class": "\u00e9"}, {"class": "\U0001f600"}, {"class": "a" * 400},
                {"class": "a b"}, {"class": " a"}, {"class": "a "}, {"class": " "},
                {"class": "a\tb"}, {"class": "a", "size": [1, 2, 3], "floating": False},
                {"class": "a", "size": [], "floating": True},
                {"class": "a", "size": [1, 2], "mapped": False, "floating": True}]:
        A((cl(obj), [size("1 2")]))
    # duplicate keys and odd JSON
    A((b'[{"class":"a","class":"b","floating":true,"floating":false,"size":[1,2],"size":[3,4]}]', [size("3 4")]))
    A((b'[{"class":"a","size":[1,2],"mapped":false,"mapped":true}]', [size("1 2")]))
    A((b'[{"class":"a","size":[1,2],"mapped":true,"mapped":false}]', [size("1 2")]))
    A((b'[{"size":[NaN,2],"class":"a"}]', [size("1 2")]))
    A((b'[{"size":[Infinity,2],"class":"a"}]', [size("1 2")]))
    A((b'[{"size":[-Infinity,2],"class":"a"}]', [size("1 2")]))
    A((b'[{"class":"a","floating":true,"size":[1,2]}', [size("1 2")]))
    A((b'', [size("1 2")]))
    A((b' ', [size("1 2")]))
    A((b'null', [size("1 2")]))
    A((b'"x"', [size("1 2")]))
    A((b'[[]]', [size("1 2")]))
    A((b'[null]', [size("1 2")]))
    A((b'[{"class":"a"},1]', [size("1 2")]))
    A((b'\xef\xbb\xbf[]', [size("1 2")]))
    A((b'[]\x00', [size("1 2")]))
    A((b'[{"class":"\\ud800"}]', [size("1 2")]))
    A((json.dumps([{"class": "a"}, {"class": "a"}, {"class": "a"}]).encode(), [size("1 2")]))
    # rules with CRLF / no trailing newline / empty file
    A((one, ["windowrule = size 1 2, match:class ^(a)$\r\n"]))
    A((one, ["windowrule = size 1 2, match:class ^(a)$\r"]))
    A((one, [""]))
    A((one, ["\n\n\n"]))
    A((one, ["windowrule = size 1 2, match:class ^(a)$" + "\r\n" + flt("on")]))
    # unicode / escapes in rule text
    A((one, ["windowrule = size 1 2, match:class ^(\u00e9)$"]))
    A((one, ["windowrule = size 1 2, match:class ^(a)$\u00e9"]))
    # ordered verdict cases
    A((cl({"class": "a", "floating": True, "size": [1, 2]}), [size("1 2"), size("1 3")]))
    A((cl({"class": "ab", "floating": True, "size": [2, 2]}), [size("1 1", "^(a.*)$"), size("2 2", "^(ab)$")]))
    A((cl({"class": "a", "floating": True, "size": [1, 2]}), []))
    A((cl({"class": "a", "floating": True, "size": [1, 2]}), [flt("on")]))
    A((b'[]', []))
    A((b'[]', [size("1 2")]))
    A((b'[{"class":"zzz"}]', [size("1 2")]))
    # classes containing a space (the U+0020 boundary of the control check)
    for obj in [{"class": "a b"}, {"class": " "}, {"class": "a b", "floating": True,
                                                     "size": [1, 2]}]:
        for rx in ["^(.*)$", "a.b", "^(.+)$", "^(a|a b)$"]:
            A((cl(obj), [size("1 2", rx)]))
    A((cl({"class": "a	b", "floating": True, "size": [1, 2]}), [size("1 2", "^(.*)$")]))
    return cases


def run_cases(cases):
    bad = []
    for raw, texts in cases:
        try:
            a, b = compare((raw, texts))
        except Exception as exc:  # a crash on either side is itself a finding
            bad.append(((raw, texts), ("crash", repr(exc)), None))
            continue
        if a != b:
            bad.append(((raw, texts), a, b))
    return bad


def still(raw, texts, target_sig):
    a, b = compare((raw, texts))
    return a != b and sig(a) == target_sig


def shrink(case, target_sig):
    raw, texts = case
    raw = bytes(raw)
    texts = list(texts)
    improved = True
    while improved:
        improved = False
        # drop rule files
        for i in range(len(texts)):
            trial_texts = texts[:i] + texts[i + 1:]
            if trial_texts != texts and still(raw, trial_texts, target_sig):
                texts = trial_texts
                improved = True
                break
        if improved:
            continue
        # drop rule lines
        for i, text in enumerate(texts):
            lines = text.split("\n")
            for j in range(len(lines)):
                trial = "\n".join(lines[:j] + lines[j + 1:])
                trial_texts = texts[:i] + [trial] + texts[i + 1:]
                if trial_texts != texts and still(raw, trial_texts, target_sig):
                    texts = trial_texts
                    improved = True
                    break
            if improved:
                break
        if improved:
            continue
        # shrink the clients doc
        try:
            doc = json.loads(raw.decode("utf-8"))
        except Exception:
            doc = None
        if isinstance(doc, list):
            for i in range(len(doc)):
                trial_doc = doc[:i] + doc[i + 1:]
                trial_raw = json.dumps(trial_doc).encode()
                if still(trial_raw, texts, target_sig):
                    raw = trial_raw
                    doc = trial_doc
                    improved = True
                    break
            if improved:
                continue
            for i, obj in enumerate(doc):
                if not isinstance(obj, dict):
                    continue
                for key in list(obj.keys()):
                    trial_obj = dict(obj)
                    del trial_obj[key]
                    trial_doc = doc[:i] + [trial_obj] + doc[i + 1:]
                    trial_raw = json.dumps(trial_doc).encode()
                    if still(trial_raw, texts, target_sig):
                        doc = trial_doc
                        raw = trial_raw
                        improved = True
                        break
                if improved:
                    break
    return raw, texts


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 43
    rng = random.Random(seed)
    generated = [gen_case(rng) for _ in range(500)]
    mine_cases = adversarial()
    bad = run_cases(generated + mine_cases)
    print("cases=%d generated=%d adversarial=%d disagreements=%d"
          % (len(generated) + len(mine_cases), len(generated), len(mine_cases), len(bad)))
    classes = {}
    for case, a, b in bad:
        key = sig(a) if a is not None else ("crash",)
        classes.setdefault(key, []).append((case, a, b))
    for key, items in classes.items():
        case, a, b = items[0]
        try:
            small = shrink(case, sig(a))
        except Exception as exc:
            small = case
            print("  (shrink aborted: %r)" % (exc,))
        print("\nCLASS n=%d key=%r" % (len(items), key))
        print("  model: %r" % (a,))
        print("  mine : %r" % (b,))
        print("  first: raw=%r texts=%r" % (case[0][:200], case[1]))
        print("  small: raw=%r texts=%r" % (small[0], small[1]))
        print("  small model: %r" % (flat(model(small[0], small[1]), small[1]),))
        print("  small mine : %r" % (flat(mine(small[0], small[1]), small[1]),))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
