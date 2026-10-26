"""Method B (rev 2): differential equivalence of behaviour-violating variants + positive controls.

Corpus: every run the 37 fixtures make (replayed), the boundary/path-kind battery (including
/proc/kcore, a path that is BOTH unreadable and > 1048576 bytes), the regex alphabet battery, and
a seeded grammar lattice. A variant that is byte-identical over the corpus has no observable
content; a positive control that differs proves the corpus can see the difference.
"""
import base64, io, contextlib, json, os, random, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lab
from importlib.machinery import SourceFileLoader
import importlib.util

S = "/fast/scratch/hyaku/mado-r43/SimpContract/equiv"
shutil.rmtree(S, ignore_errors=True)
os.makedirs(S)
REF_SRC = open(lab.REF, "rb").read().decode()

def load_src(name, text):
    p = os.path.join(S, name + ".py")
    open(p, "w").write(text)
    loader = SourceFileLoader(name, p)
    m = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader))
    loader.exec_module(m)
    return m

def patch(old, new):
    assert REF_SRC.count(old) == 1, (old[:70], REF_SRC.count(old))
    return REF_SRC.replace(old, new)

CHAIN = '''    if size_rules == 0:
        verdict, rc = "NO_SIZE_RULES", 4
    elif t["differ"] > 0:
        verdict, rc = "DIFFER", 1
    elif t["matched"] == 0:
        verdict, rc = "NO_MATCHING_CLIENT", 3
    else:
        verdict, rc = "OK", 0'''

EQV = {}      # expected equivalent (dead content)
POS = {}      # expected different (positive controls)

EQV["V1-stdin-cap-1048578"] = patch("data = stdin.read(MAX_BYTES + 1)",
                                     "data = stdin.read(MAX_BYTES + 2)")
EQV["V2-regex-min-0"] = patch('){1,200}")', '){0,200}")')
EQV["V3-verdict-differ-after-nomatch"] = patch(CHAIN, '''    if size_rules == 0:
        verdict, rc = "NO_SIZE_RULES", 4
    elif t["matched"] == 0:
        verdict, rc = "NO_MATCHING_CLIENT", 3
    elif t["differ"] > 0:
        verdict, rc = "DIFFER", 1
    else:
        verdict, rc = "OK", 0''')
EQV["V4-verdict-ok-first"] = patch(CHAIN, '''    if t["matched"] > 0 and t["differ"] == 0 and size_rules > 0:
        verdict, rc = "OK", 0
    elif size_rules == 0:
        verdict, rc = "NO_SIZE_RULES", 4
    elif t["differ"] > 0:
        verdict, rc = "DIFFER", 1
    else:
        verdict, rc = "NO_MATCHING_CLIENT", 3''')

POS["P1-search-not-fullmatch"] = patch("return re.fullmatch(rx, cls) is not None",
                                       "return re.search(rx, cls) is not None")
_p2 = patch('){1,200}")', '){0,200}")')
assert _p2.count('match:class[ \\t]+(.+)') == 1
POS["P2-regex-min-0-and-loose-field-grammar"] = _p2.replace(
    'match:class[ \\t]+(.+)', 'match:class[ \\t]*(.*)')
POS["P3-strip-all-whitespace"] = patch('line = raw.strip(" \\t")', 'line = raw.strip()')
POS["P4-field-separator-comma-or-semicolon"] = patch(
    'fields = [f.strip(" \\t") for f in body.split(",")]',
    'fields = [f.strip(" \\t") for f in body.replace(";", ",").split(",")]')
POS["P5-verdict-nomatch-first"] = patch(CHAIN, '''    if t["matched"] == 0:
        verdict, rc = "NO_MATCHING_CLIENT", 3
    elif size_rules == 0:
        verdict, rc = "NO_SIZE_RULES", 4
    elif t["differ"] > 0:
        verdict, rc = "DIFFER", 1
    else:
        verdict, rc = "OK", 0''')
POS["P6-size-before-open"] = patch("def read_regular(path):\n", '''def read_regular(path):
    try:
        if os.stat(path).st_size > MAX_BYTES:
            raise Setup("too_large")
    except Setup:
        raise
    except OSError:
        pass
''')
POS["P7-parse-json-before-size-bound"] = patch(
    '''    if clients == "-":
        data = stdin.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise Setup("too_large")
    else:
        data = read_regular(clients)''',
    '''    if clients == "-":
        data = stdin.read(8 * MAX_BYTES)
    else:
        data = read_unbounded(clients)
    try:
        json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise Setup("bad_json")
    if len(data) > MAX_BYTES:
        raise Setup("too_large")''').replace(
    "def parse_args(argv):", '''def read_unbounded(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except OSError:
        raise Setup("unreadable")
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise Setup("unreadable")
        return os.read(fd, 8 * MAX_BYTES)
    except OSError:
        raise Setup("unreadable")
    finally:
        os.close(fd)


def parse_args(argv):''')

MODS = {n: (load_src("var_" + n.split("-")[0], t), "same") for n, t in EQV.items()}
MODS.update({n: (load_src("pos_" + n.split("-")[0], t), "differ") for n, t in POS.items()})

def run_mod(m, argv, stdin):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = m.run(list(argv), io.BytesIO(stdin))
    except m.Setup as exc:
        return 2, ("MADO_GEOMETRY: SETUP %s\n" % exc).encode()
    except Exception as exc:  # noqa
        return ("exception", repr(exc)[:200])
    return rc, buf.getvalue().encode()

CORPUS = []
def add(tag, argv, stdin=b""):
    CORPUS.append({"tag": tag, "argv": list(argv), "stdin": stdin})

fixtures = json.load(open("/fast/scratch/hyaku/mado-r43/SimpContract/fixscan/fixtures.json"))
nfix = 0
for f in fixtures:
    for k, r in enumerate(f["runs"]):
        if not all(os.path.exists(a) for a in r["argv"] if a.startswith("/")):
            continue
        add("%s#%d" % (f["fixture"], k), r["argv"],
            base64.b64decode(r["stdin_b64"]) if r["stdin_b64"] else b"")
        nfix += 1

D = os.path.join(S, "d")
os.makedirs(D)
def W(name, data):
    p = os.path.join(D, name)
    with open(p, "wb") as fh:
        fh.write(data if isinstance(data, bytes) else data.encode())
    return p

R1 = W("r1.conf", "windowrule = size 1 2, match:class a\nwindowrule = float on, match:class a\n")
R2 = W("r2.conf", "windowrule = size 9 9, match:class .*\n")
TINY = W("tiny.json", b"[]")
EMPTY = W("empty.conf", b"")
MAXF = W("max.conf", b"#" * 1048576)
BIGF = W("big.conf", b"#" * 1048577)
HUGEF = W("huge.conf", b"#" * (4 * 1048576))
BIGCL = W("big.json", b"[]" + b" " * 1048575)
MAXCL = W("max.json", b"[]" + b" " * 1048574)
BADJSON = W("bad.json", b"\xff[]")
BADBIG = W("badbig.json", b"{" + b" " * (1048577 - 1))
SEMI = W("semi.conf", "windowrule = size 1 2; match:class a\n")
os.makedirs(os.path.join(D, "adir"), exist_ok=True)
if not os.path.exists(os.path.join(D, "fifo")):
    os.mkfifo(os.path.join(D, "fifo"))

for n in (1048573, 1048574, 1048575, 1048576, 1048577, 1048578, 1048600, 2 * 1048576):
    body = (b"[]" + b" " * (n - 2))[:n]
    add("stdin-%d" % n, ["--clients", "-", "--rules", R1], body)
add("stdin-badbig", ["--clients", "-", "--rules", R1], b"{" + b" " * 1048576)
for p in (os.path.join(D, "missing"), os.path.join(D, "adir"), "/dev/null",
          os.path.join(D, "fifo"), EMPTYCL if False else TINY, BADJSON, BIGCL, MAXCL, BADBIG):
    add("clients-path %s" % os.path.basename(p), ["--clients", p, "--rules", R1])
for p in (os.path.join(D, "missing"), os.path.join(D, "adir"), "/dev/null",
          os.path.join(D, "fifo"), EMPTY, MAXF, BIGF, R2, SEMI):
    add("rules-path %s" % os.path.basename(p), ["--clients", TINY, "--rules", R1, "--rules", p])
    add("rules-path-first %s" % os.path.basename(p), ["--clients", TINY, "--rules", p, "--rules", R1])
add("separator-semicolon", ["--clients", TINY, "--rules", SEMI])
for p in ("/proc/kcore",):
    for flag in ("--clients", "--rules"):
        add("overlap %s %s" % (flag, p), [flag, p] + (["--rules", R1] if flag == "--clients" else ["--clients", TINY]))

RX = ["a", "a" * 199, "a" * 200, "a" * 201, "", "^(a|b)+\\.c$", "a{2}", "[ab]", "\\d", "\\w",
      "(?i)a", "(?:a)", "a*+", "a++", "a?+", "a**", "a+*", "a+?", "a*?", "a??", "(a", "a)", "a|",
      "|a", "()", "a\\", "\\\\", "\\a", "a-b", "a b", "a\\ b", "a\u00fc", "a,b", "a\tb",
      "\\.\\-\\(\\)\\|\\*\\+\\?\\^\\$", "^a$", "a^b", "$a", "a^", ".", "..", "(()))",
      "x" * 150 + "|" + "y" * 49, "\\\\\\", "negative:a", "a:b", "a/b", "a#", "a~", "a=", "a%"]
text = "".join("windowrule = size %d 7, match:class %s\n" % (i + 1, rx) for i, rx in enumerate(RX))
CL = [{"class": c, "size": [1, 7], "floating": True, "address": "0x%x" % i}
      for i, c in enumerate(["a", "aa", "b", "a.c", "bb.c", "ac", "a-b", "x" * 150, "y" * 49,
                             "ab", "", "a\u00fc", "a b", "a,b", "a\tb"])]
add("regex-battery", ["--clients", W("regex.json", json.dumps(CL)), "--rules", W("regex.conf", text)])

rng = random.Random(430043)
RX_POOL = ["^(org.omarchy.gkeep)$", "org\\.omarchy\\..*", "Alacritty|kitty", "a", "a|ab", ".*",
           "a\\.b", "^(a|ab)$", "(x y)?", "x.y", "firefox+", "org.a.b", "\\(a\\)", "a?b?",
           "k.*y", "^$", "a" * 200, "a" * 201, "", "a{2}", "[ab]", "(?i)a", "a*+", "a#b",
           "a;b", "a,b", "\\d", "\\\\\\\\", "match:class"]
CLASS_POOL = ["org.omarchy.gkeep", "Alacritty", "kitty", "firefox", "org.a.b", "a", "ab", "",
              "x y", "\u00fc-app", "a.b", "axb", "Org.Omarchy.Gkeep", "ab ", " ab", "a\x01b"]
for i in range(500):
    texts = []
    for _ in range(rng.randrange(1, 4)):
        lines = []
        for _ in range(rng.randrange(0, 7)):
            k = rng.randrange(12)
            rx = rng.choice(RX_POOL)
            if k < 4:
                lines.append("windowrule = size %s %s, match:class %s" % (
                    rng.choice(["0", "7", "420", "99999", "100000", "00420"]),
                    rng.choice([500, 8, 1]), rx))
            elif k < 6:
                lines.append("windowrule = float %s, match:class %s" % (
                    rng.choice(["on", "off", "On", ""]), rx))
            elif k == 6:
                lines.append(rng.choice(["windowrule = center on, match:class a",
                                         "windowrule = size, match:class a",
                                         "windowrule = ,", "windowrule =",
                                         "windowrule = size 1 2; match:class a"]))
            elif k == 7:
                lines.append(rng.choice(["windowrule = size 1 2, match:title a",
                                         "windowrule = size 1 2, match:class a;b",
                                         "windowrule = size 1 2 , match:class a",
                                         "  windowrule=size 1 2,match:class a\t",
                                         "windowrule = size 1 2, match:class"]))
            else:
                lines.append(rng.choice(["# c", "windowrulev2 = size 1 2, class:a",
                                         "WindowRule = size 1 2, match:class a",
                                         "bind = SUPER, A, exec, x", ""]))
        texts.append(rng.choice(["\n", "\n\n", "\r\n"]).join(lines) + rng.choice(["", "\n"]))
    clients = []
    for _ in range(rng.randrange(0, 8)):
        c = {"address": "0x%x" % rng.randrange(1 << 20), "class": rng.choice(CLASS_POOL)}
        c["size"] = rng.choice([[7, 8], [7.0, 8], [True, 8], [7], [-1, 8], "x", None, [7, 8, 9],
                                [10 ** 30, 8]])
        c["floating"] = rng.choice([True, False, 1, None, "true"])
        r = rng.randrange(6)
        if r == 0:
            c["mapped"] = False
        elif r == 1:
            c["mapped"] = 0
        elif r == 2:
            del c["class"]
        clients.append(c)
    raw = json.dumps(clients).encode()
    if i % 37 == 0:
        raw = raw.replace(b'"a"', b'"a\xffb"', 1)
    rpaths = []
    for j, t in enumerate(texts):
        data = t.encode()
        if i % 41 == 0:
            data = data.replace(b"match:class", b"match:cla\xffss", 1)
        rpaths.append(W("lat%d-%d.conf" % (i, j), data))
    cpath = W("lat%d.json" % i, raw)
    argv = ["--clients", cpath]
    for p in rpaths:
        argv += ["--rules", p]
    if i % 2:
        argv = ["--rules", rpaths[0], "--clients", cpath]
        for p in rpaths[1:]:
            argv += ["--rules", p]
    add("lattice%d" % i, argv)

def main():
    print("corpus=%d (fixture replays=%d)" % (len(CORPUS), nfix))
    base = [run_mod(lab.ref, c["argv"], c["stdin"]) for c in CORPUS]
    hist = {}
    for (rc, out) in base:
        key = str(rc) if not isinstance(out, bytes) or b"SETUP" not in out else \
            "2:" + out.decode().strip().split()[-1]
        hist[key] = hist.get(key, 0) + 1
    print("ref outcome histogram:", json.dumps(hist))
    good = 0
    for name, (m, want) in MODS.items():
        diffs = []
        for c, b in zip(CORPUS, base):
            got = run_mod(m, c["argv"], c["stdin"])
            if got != b:
                diffs.append({"tag": c["tag"], "argv": [a.replace(D, "D") for a in c["argv"]],
                              "ref": str(b)[:200], "variant": str(got)[:200]})
        got_kind = "same" if not diffs else "differ"
        ok = got_kind == want
        good += ok
        print("%-40s %-7s expected=%-6s diffs=%d/%d %s" % (
            name, got_kind, want, len(diffs), len(CORPUS), "OK" if ok else "FAIL"))
        for d in diffs[:4]:
            print("    ", d["tag"], d["argv"][:3], "\n      ref:", d["ref"][:150],
                  "\n      var:", d["variant"][:150])
        json.dump({"variant": name, "diffs": diffs}, open(os.path.join(S, name + ".json"), "w"))
    print("VARIANTS=%d OK=%d" % (len(MODS), good))

if __name__ == "__main__":
    main()
