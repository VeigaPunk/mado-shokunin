import importlib.util
import json
import os
import random
import subprocess
import sys

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w1/ExecC1ExtraMutants"
SCRATCH = "/fast/scratch/hyaku/mado-r43/ExecC1ExtraMutants"
REF = os.path.join(SEAT, "ref.py")
OUT = open(os.path.join(SEAT, "equiv.txt"), "w")


def say(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    OUT.write(line + "\n")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def call(mod, raw, texts):
    try:
        return ("out",) + tuple(mod.report(raw, texts)) if not isinstance(raw, bytes) \
            else ("out",) + tuple(mod.report(raw, texts))
    except mod.Setup as exc:
        return ("setup", str(exc))


ref = load(REF, "refmod")

SIZES = ["0 0", "420 500", "00420 500", "99999 99999", "100000 1", "1 100000",
         "\u0664\u0662\u0660 500", "-1 5", "+1 5", "1.5 2", "1 2 3", "1", "", "0x10 5",
         "1x 2", "12345 54321", "1 \u0663"]
RXS = ["a", "a" * 200, "a" * 201, "", "^(a|b)+\\.c$", "a{2}", "[ab]", "\\d", "\\w",
       "(?i)a", "(?:a)", "a*+", "a++", "a?+", "a**", "a+*", "a+?", "a*?", "a??", "(a",
       "a)", "a|", "|a", "()", "a\\", "\\\\", "\\a", "a-b", "a b", "a\\ b", "a\u00fc",
       "a,b", "a\tb", "\\.\\-\\(\\)\\|\\*\\+\\?\\^\\$", "^a$", "a^b", "a$b", "$a", "a^",
       ".", "..", "(a|b)(c|d)", "(()))", "x" * 150 + "|" + "y" * 49, "\\\\\\",
       "negative:a", "a:b", "a/b", "a'b", 'a"b', "a#", "a~", "a=", "a%", ".*", "^$"]
FLOATS = ["on", "off", "On", "ON", "true", "1", "yes", "", "on off", "toggle", "0"]
CLASSES = ["a", "ab", "b", "a.c", "ac", "org.omarchy.gkeep", "Alacritty", "x y", "",
           "a b", "a\x01b", "a\x1fb", "a\tb", "a\nb", "a\rb", "a\x7fb", "a\u0085b",
           "\x00", "a\u2028b", "\u00fc", "\U0001f600", "a-b", "x" * 150]

JUNKLINES = ["# windowrule = size 1 2, match:class a", "", "bind = SUPER, A, exec, x",
             "windowrulev2 = size 1 2, class:a", "WindowRule = size 1 2, match:class a",
             "windowrule", "windowrulefoo = size 1 2, match:class a",
             "windowrule =", "windowrule = center on, match:class a",
             "windowrule = noshadow", "windowrule = ,", "windowrule = float, match:class a",
             "windowrule = float on, match:title a", "windowrule = pin on",
             "windowrule = size 1 2, match:class", "windowrule = size 1 2",
             "windowrule = size 1 2, match:class a, match:title b",
             "windowrule = size 1 2, match:class a # c",
             "windowrule = size 1 2,, match:class a", "windowrule = ,size 1 2, match:class a",
             "  \twindowrule = size 1 2 , match:class a  \t",
             "windowrule = size 1 2, match:class a\r", "windowrule = size 1 2, match:class a\x0b",
             "windowrule = size 1 2, match:classa", "windowrule = size 1 2, match: class a",
             "windowrule = size 1 2, Match:class a", "windowrule = size\u00a01 2, match:class a",
             "windowrule = SIZE 1 2, match:class a", "windowrule=size 1 2,match:class a",
             "windowrule\t=\tsize\t1\t2\t,\tmatch:class\ta",
             "windowrule  =  size   1    2  ,  match:class     a",
             "windowrule = size 1 2, match:class a,", "windowrule = size 1 2, match:class a ,",
             "windowrule = size 1 2 , match:class a\t", "windowrule = float on, match:class a,",
             "windowrule = size 1 2, match:class .*"]


def rand_text(rng):
    lines = []
    for _ in range(rng.randrange(0, 9)):
        k = rng.randrange(10)
        if k < 4:
            lines.append("windowrule = size %s, match:class %s" % (
                rng.choice(SIZES), rng.choice(RXS)))
        elif k < 6:
            lines.append("windowrule = float %s, match:class %s" % (
                rng.choice(FLOATS), rng.choice(RXS)))
        else:
            lines.append(rng.choice(JUNKLINES))
    return rng.choice(["\n", "\n\n"]).join(lines) + rng.choice(["", "\n"])


SIZEVALS = [[0, 0], [1, 2], [1.0, 2], [1, 2.0], [True, 2], [1, False], [1], [1, 2, 3], [],
            "12", None, 12, {"w": 1}, [-1, 2], [1, -2], [10 ** 30, 2], [[1], 2], ["1", 2],
            [NaN := float("nan"), 2], [1, float("inf")], [1e2, 2], [100, 2], [1, 2]]


def rand_client(rng):
    c = {}
    if rng.randrange(6):
        c["class"] = rng.choice(CLASSES + [None, 5, ["a"], {"a": 1}])
    if rng.randrange(8):
        c["size"] = rng.choice(SIZEVALS)
    if rng.randrange(6):
        c["floating"] = rng.choice([True, False, 1, 0, None, "true", [], {}])
    if rng.randrange(8):
        c["mapped"] = rng.choice([False, True, 0, 1, None, "false", "", [], {}])
    if rng.randrange(8):
        c["address"] = rng.choice(["0x1", "0xa\"b", "\u00e9\"\\/", 5, None, "\U0001f601"])
    return c


def rand_doc(rng):
    n = rng.randrange(0, 12)
    return json.dumps([rand_client(rng) for _ in range(n)]).encode()


RAWEDGE = [b"[]", b"{}", b"[1]", b"", b"\xff", b"[", b"null", b"\"[]\"", b"[{}, 3]", b"[[]]",
           b"\xef\xbb\xbf[]", b"[] x", b'[{"class":"a\xffb","size":[1,2],"floating":true}]',
           b'[{"size":[NaN,2]}]', b'[{"size":[Infinity,2]}]',
           b'[{"class":"zz","class":"a","size":[9,9],"size":[1,2],"floating":false,'
           b'"floating":true,"mapped":false,"mapped":true}]',
           b'[{"class":"\\ud800x","size":[1,2],"floating":true,"address":"\\udc00"}]',
           b'[{"class":"a","size":[1,2],"floating":true}] ', b'  [ ]  ',
           b'[{"class":"a","size":[1,2],"floating":true,"mapped":false}]',
           b'[{"class":"a","size":[1,2],"floating":true,"mapped":0}]']


def cases():
    rng = random.Random(0xC1E1)
    for i in range(2200):
        texts = [rand_text(rng) for _ in range(rng.randrange(1, 4))]
        yield rand_doc(rng), texts
    for raw in RAWEDGE:
        for text in (rand_text(random.Random(7)), ""):
            yield raw, [text]
    greedy = random.Random(4242)
    for i in range(300):
        yield rand_doc(greedy), [rand_text(greedy) for _ in range(3)]
    yield json.dumps([rand_client(random.Random(9)) for _ in range(300)]).encode(), \
        [rand_text(random.Random(11)) for _ in range(40)]
    yield b"[]", [""]
    yield b"[]", ["\n\n"]
    yield b"[{}]", [""]


def fuzz(mod, name):
    n = bad = 0
    for raw, texts in cases():
        n += 1
        a = call(ref, raw, texts)
        b = call(mod, raw, texts)
        if a != b:
            bad += 1
            if bad <= 3:
                say("  DIFF %s case=%d raw=%r texts=%r\n    ref=%r\n    mut=%r"
                    % (name, n, raw[:80], [t[:120] for t in texts], a, b))
    say("  fuzz %-26s cases=%d identical=%d differ=%d" % (name, n, n - bad, bad))
    return bad


REPORT_LEVEL = ["N08-matchfield-star", "N09-split-maxsplit", "N19-rule-line-caret",
                "N22-size-gt-minus1", "N23-size-type-is-int", "N34-differ-and-matched",
                "N46-doc-tuple", "N49-json-decode-strict", "N52-size-truthiness",
                "N53-fullmatch-dotall"]

say("== A. report()-level differential fuzz (ref vs mutant, identical (lines, rc) or Setup reason)")
fails = 0
for name in REPORT_LEVEL:
    mod = load(os.path.join(SEAT, "mutants", name + ".py"), name.replace("-", "_"))
    fails += fuzz(mod, name)

say("")
say("== B. single-region check: each mutant differs from the reference in exactly one contiguous hunk")
for name in REPORT_LEVEL + ["N01-stdin-read-plus2", "N48-rules-decode-ignore", "N51-close-fd-pass",
                            "N54-read-chunk-cap", "N68-stdout-print"]:
    p = subprocess.run(["diff", "-u", REF, os.path.join(SEAT, "mutants", name + ".py")],
                       capture_output=True, text=True)
    hunks = [ln for ln in p.stdout.splitlines() if ln.startswith("@@")]
    minus = [ln for ln in p.stdout.splitlines() if ln.startswith("-") and not ln.startswith("---")]
    plus = [ln for ln in p.stdout.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    say("  %-26s hunks=%d removed=%d added=%d  %s" % (
        name, len(hunks), len(minus), len(plus),
        " ".join(x.strip() for x in minus)[:70] + " -> " + " ".join(x.strip() for x in plus)[:70]))

OUT.close()
print("FAILS=%d" % fails)
