#!/usr/bin/env python3
"""RevC1Counter harness: independent docstring-derived model vs the frozen counter's model.

Tier 1: 300 sampled cases + handcrafted edges, in-process (counter.model_out vs mine).
Tier 2: sandboxed reference-tool runs vs counter model (~60 cases).
Tier g: clause-g AST probes.
Prints a compact evidence digest only.
"""
import importlib.util, json, random, re, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = LANE + "/quality/counters/c1-r42-geometry.py"
REF_TXT = LANE + "/.ufo/waves/round-42/c1/ctl-ref-tool.py.txt"

spec = importlib.util.spec_from_file_location("ctr", COUNTER)
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

# ---------------------------------------------------------------- my model (from the docstring text alone)
NUM = re.compile(r"[0-9]{1,5}")
RULE = re.compile(r"windowrule[ \t]*=(.*)")
MATCH = re.compile(r"match:class[ \t]+(.+)")
ALPHA = re.compile(r"(?:[A-Za-z0-9_.^$()|*+?-]|\\[.\-()|*+?^$\\]){1,200}")

def rx_ok(rx):
    if not ALPHA.fullmatch(rx): return False
    if any(s in rx for s in ("(?", "*+", "++", "?+")): return False
    try: re.compile(rx)
    except re.error: return False
    return True

def my_rules(texts):
    rules, other, unsup = [], 0, 0
    for fno, text in enumerate(texts, 1):
        for raw in text.split("\n"):
            line = raw.strip(" \t")
            m = RULE.fullmatch(line)
            if not m: continue
            fields = [f.strip(" \t") for f in m.group(1).split(",")]
            words = [w for w in re.split("[ \t]+", fields[0]) if w]
            eff = words[0] if words else ""
            if eff not in ("size", "float"):
                other += 1; continue
            args = words[1:]
            ok = len(fields) == 2
            if ok and eff == "size":
                ok = len(args) == 2 and all(NUM.fullmatch(a) for a in args)
            elif ok:
                ok = len(args) == 1 and args[0] in ("on", "off")
            mm = MATCH.fullmatch(fields[1]) if ok else None
            if mm is None or not rx_ok(mm.group(1)):
                unsup += 1; continue
            if eff == "size":
                want, arg = (int(args[0]), int(args[1])), "%dx%d" % (int(args[0]), int(args[1]))
            else:
                want = arg = args[0]
            rules.append((fno, eff, arg, want, mm.group(1)))
    return rules, other, unsup

def my_model(raw, texts, strict_json=False):
    if strict_json and re.search(rb"\b(NaN|Infinity)\b", raw):
        return None, "bad_json"
    try:
        doc = json.loads(raw.decode("utf-8"))
    except Exception:
        return None, "bad_json"
    if not isinstance(doc, list) or any(not isinstance(c, dict) for c in doc):
        return None, "bad_json"
    rules, other, unsup = my_rules(texts)
    out = ["MADO_GEOM_RULE: n=%d file=%d effect=%s arg=%s class=%s" % (n, r[0], r[1], r[2], r[4]) for n, r in enumerate(rules, 1)]
    t = dict(clients=0, matched=0, unmapped=0, AGREE=0, DIFFER=0, TILED=0, BADSIZE=0)
    for c in doc:
        if c.get("mapped") is False:
            t["unmapped"] += 1; continue
        t["clients"] += 1
        cls = c.get("class") if isinstance(c.get("class"), str) else ""
        want, fr = None, "-"
        if not any(ord(ch) < 32 for ch in cls):
            for r in rules:
                if re.fullmatch(r[4], cls):
                    if r[1] == "size": want = r[3]
                    else: fr = r[3]
        if want is None: continue
        t["matched"] += 1
        sz = c.get("size")
        size = (sz[0], sz[1]) if isinstance(sz, list) and len(sz) == 2 and all(type(v) is int and v >= 0 for v in sz) else None
        fl = c.get("floating") is True
        v = "BADSIZE" if size is None else ("TILED" if not fl else ("AGREE" if size == want else "DIFFER"))
        t[v] += 1
        addr = c.get("address") if isinstance(c.get("address"), str) else "-"
        out.append("MADO_GEOM_CLIENT: addr=%s class=%s floating=%s size=%s want=%dx%d float_rule=%s verdict=%s" % (
            json.dumps(addr), json.dumps(cls), "true" if fl else "false",
            "%dx%d" % size if size else "-", want[0], want[1], fr, v))
    nsize = sum(1 for r in rules if r[1] == "size")
    if nsize == 0: verdict, rc = "NO_SIZE_RULES", 4
    elif t["DIFFER"]: verdict, rc = "DIFFER", 1
    elif t["matched"] == 0: verdict, rc = "NO_MATCHING_CLIENT", 3
    else: verdict, rc = "OK", 0
    out.append("MADO_GEOMETRY: rules=%d float_rules=%d other=%d unsupported=%d clients=%d matched=%d unmapped=%d agree=%d differ=%d tiled=%d badsize=%d verdict=%s" % (
        nsize, len(rules) - nsize, other, unsup, t["clients"], t["matched"], t["unmapped"],
        t["AGREE"], t["DIFFER"], t["TILED"], t["BADSIZE"], verdict))
    return "\n".join(out) + "\n", rc

# ---------------------------------------------------------------- randomized case generator (wider than counter pools)
RXW = ["a", ".*", "^(a|ab)$", "a|ab", "org\\.omarchy\\..*", "(x y)?", "x.y", "^$", "a?b?",
       "a{2}", "[ab]", "\\d", "(?i)a", "a*+", "(a", "\\", "\\a", "a-b", "a b", "a\\ b",
       "\u00fc", "a,b", "a\tb", "(?:a)", "negative:a", "a:b", "a{0,}", "\\b",
       "a" * 200, "a" * 201, "x" * 150 + "|" + "y" * 49, "\\.\\-\\(\\)\\|\\*\\+\\?\\^\\$", "a**", "a*?"]
CLS = ["org.omarchy.gkeep", "Alacritty", "kitty", "", "x y", "\u00fc-app", "a.b", "axb",
       "Org.Omarchy.Gkeep", "ab ", " ab", "a\x01b", "a\tb", "a\nb", "a\x7fb", "a\x85b",
       "\ud800x", "e", "a" * 60, "aa", "ac", "bb.c"]
SIZES = [[1, 2], [420, 500], [0, 0], [99999, 99999], [100000, 1], [1.0, 2], [True, 2],
         [1], [1, 2, 3], [], "x", None, 12, {"w": 1}, [-1, 2], [10**30, 2], [0, -0],
         [False, 1], [[1], [2]]]
FLOATS = [True, False, 1, 0, None, "true", [], {}]
MAPPED = [None, False, True, 0, 1, "false", "", [], {}]

def rnd_text(rng):
    lines = []
    for _ in range(rng.randrange(0, 7)):
        k = rng.randrange(10)
        rx = rng.choice(RXW)
        if k < 4:
            lines.append("windowrule = size %d %d, match:class %s" % (rng.choice([0, 1, 7, 420, 99999, 100000]), rng.choice([2, 500, 8]), rx))
        elif k < 6:
            lines.append("windowrule = float %s, match:class %s" % (rng.choice(["on", "off", "On", "maybe", ""]), rx))
        elif k == 6:
            lines.append(rng.choice(["windowrule = center on, match:class a", "windowrule =", "windowrulev2 = size 1 2, class:a",
                                     "# windowrule = size 1 2, match:class a", "windowrule\t=\tsize\t1\t2\t,\tmatch:class\ta",
                                     "windowrule = size 1 2, match:class a\r", "windowrule = size\u00a01 2, match:class a",
                                     "  windowrule = 00420 500, match:class a  ".replace("= 00420", "= size 00420")]))
        elif k == 7:
            lines.append("windowrule = size %s, match:class %s" % (rng.choice(["1x 2", "1 2 3", "-1 5", "+1 5", "\u0664\u0662 5", "0x10 5", "1"]), rx))
        else:
            lines.append(rng.choice(["", "bind = SUPER, A, exec, x", "windowrulefoo = size 1 2, match:class a"]))
    return rng.choice(["\n", "\n\n"]).join(lines) + rng.choice(["", "\n"])

def rnd_clients(rng):
    out = []
    for _ in range(rng.randrange(0, 12)):
        c = {}
        if rng.randrange(8): c["class"] = rng.choice(CLS)
        if rng.randrange(6): c["size"] = rng.choice(SIZES)
        if rng.randrange(6): c["floating"] = rng.choice(FLOATS)
        r = rng.randrange(8)
        if r == 0: c["mapped"] = rng.choice(MAPPED)
        elif r == 1: c["address"] = rng.choice(["0x1", 5, None, "\u00e9\"\\/", "\u2028"])
        out.append(c)
    return out

def js(x):
    return json.dumps(x)  # ensure_ascii, allow_nan default (NaN literal emitted)

HAND = [
    (b'[{"class":"a","size":[NaN,2],"floating":true},{"class":"a","size":[1,Infinity],"floating":true},{"class":"a","size":[1e2,2],"floating":true},{"class":"a","size":[100,2],"floating":true}]', ["windowrule = size 100 2, match:class a\n"]),
    (b'[{"class":"a","size":[-Infinity,2],"floating":true}]', ["windowrule = size 1 2, match:class a\n"]),
    (b'\xef\xbb\xbf[{"class":"a","size":[1,2],"floating":true}]', ["windowrule = size 1 2, match:class a\n"]),
    (b'[{"class":"zz","class":"a","size":[9,9],"size":[1,2],"floating":false,"floating":true,"mapped":false,"mapped":true}]', ["windowrule = size 1 2, match:class a\n"]),
    (b'[{"class":"a\nb","size":[1,2],"floating":true},{"class":"a\x7fb","size":[1,2],"floating":true},{"class":"a b","size":[1,2],"floating":true}]', ["windowrule = size 1 2, match:class a.b\n"]),
    (b'[{"class":"a","size":[1,2],"floating":true,"mapped":false},{"class":"a","size":[1,2],"floating":true,"mapped":0},{"class":"a","size":[1,2],"floating":true,"mapped":null}]', ["windowrule = size 1 2, match:class a\n"]),
    (b'[' + json.dumps({"class": "a", "size": [10**30, 2], "floating": True}).encode() + b']', ["windowrule = size 1 2, match:class a\n"]),
    (b'[{"class":"a","size":[00,0],"floating":true}]', ["windowrule = size 1 2, match:class a\n"]),
    (b'[{"class":"a","size":[0,-0],"floating":true}]', ["windowrule = size 1 2, match:class a\n"]),
    (b'[{"class":"a","size":[1,2],"floating":true}]', ["windowrule = size 1 2, match:class a\r\n", "windowrule = size 1 2, match:class a\r"]),
    (b'[{"class":"\\ud800x","size":[1,2],"floating":true,"address":"\\udc00"}]', ["windowrule = size 1 2, match:class .*"]),
    (b'[]', ["", "windowrule = float on, match:class a\n"]),
    (b'[{}]', ["windowrule = float off, match:class a\n"]),
    (b'not json at all', ["windowrule = size 1 2, match:class a\n", "/nonexistent-rules-unreachable-in-model"]),
]

def run_tier1():
    rng = random.Random(0xC0FFEE)
    divs = []
    n = 0
    # handcrafted
    for raw, texts in HAND:
        if texts and texts[0] is True:
            texts = [raw]; raw = b'[{"class":"a","size":[1,2],"floating":true}]'
        texts = [t for t in texts if not t.startswith("/nonexistent")]
        n += 1
        want = ctr.model_out(raw, texts)
        mine = my_model(raw, texts)
        strict = my_model(raw, texts, strict_json=True)
        if want != mine:
            divs.append(("hand", n, raw[:60], want, mine))
        if strict != mine:
            divs.append(("strict-json", n, raw[:60], repr(mine)[:140], repr(strict)[:140]))
    # sampled
    for i in range(300):
        n += 1
        texts = [rnd_text(rng) for _ in range(rng.randrange(1, 4))]
        clients = js(rnd_clients(rng)).encode()
        want = ctr.model_out(clients, texts)
        mine = my_model(clients, texts)
        if want != mine:
            divs.append(("gen", i, (texts, clients)[:1], want, mine))
    print("TIER1 cases=%d divergences=%d" % (n, len(divs)))
    for d in divs[:12]:
        print("  DIV", d[0], d[1])
        print("   counter:", repr(d[3])[:200])
        print("   mine   :", repr(d[4])[:200])
    return divs

if __name__ == "__main__":
    run_tier1()
