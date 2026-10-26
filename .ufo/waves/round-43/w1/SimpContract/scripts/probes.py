"""Method A: input pairs run through the frozen reference (in-process, same code path).

Each row: contract sentence -> two inputs -> the observable that differs (or not).
"""
import json, os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lab

S = "/fast/scratch/hyaku/mado-r43/SimpContract/cases"
shutil.rmtree(S, ignore_errors=True)
os.makedirs(S, exist_ok=True)

R_OK = "windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$\n"
GK = "org.omarchy.gkeep"
CL_OK = [{"class": GK, "size": [420, 500], "floating": True, "address": "0x1"}]

def f(name, data):
    return lab.mk(S, name, data)

def cli(*a, **k):
    return lab.cli(*a, **k)

def rep(c, t):
    return lab.rep(c, t)

ROWS = []
def row(pid, cid, quote, a, b, expect, kind, note, scope="full"):
    ROWS.append(dict(id=pid, cid=cid, quote=quote, a=a, b=b, expect=expect,
                     kind=kind, note=note, scope=scope))

C = f("clients.json", json.dumps(CL_OK))
CF = f("clients-fail.json", "[1]")
CBIG = f("clients-big.json", b"[]" + b" " * (lab.ref.MAX_BYTES - 1))
R = f("r.conf", R_OK)
RMISS = f("r.conf.none", "")
RBIG = f("r-big.conf", b"#" * (lab.ref.MAX_BYTES + 1))
RNAME = "r.conf.none"

# ---------------- CLI (C10-C14) ----------------
row("A01", "C10", "`--clients V` exactly once",
    lambda: cli(["--clients", C, "--rules", R]),
    lambda: cli(["--clients", C, "--clients", C, "--rules", R]),
    "differ", "live", "second --clients is usage (exit 2, usage)")
row("A02", "C10", "and `--rules V` one or more times",
    lambda: cli(["--clients", C, "--rules", R]),
    lambda: cli(["--clients", C]),
    "differ", "live", "no --rules is usage")
row("A03", "C10", "(two-token form only",
    lambda: cli(["--clients", C, "--rules", R]),
    lambda: cli(["--clients=" + C, "--rules", R]),
    "differ", "live", "`--clients=PATH` is usage, not a path")
row("A04", "C10", "`mado-geometry.py --selftest`",
    lambda: cli(["--selftest"]),
    lambda: cli(["--selftest", "--rules", R]),
    "differ", "live", "selftest is alone; with args it is usage")
row("A05", "C10", "any order",
    lambda: cli(["--rules", R, "--clients", C]),
    lambda: cli(["--clients", C, "--rules", R]),
    "same", "live-constraint", "order-independent: reversed flags must not be usage; the ref is byte-identical. No fixture presents this form (F1)")
row("A06", "C12", "Setup failure: stdout is exactly one line",
    lambda: cli(["--clients", "/nonexistent/x", "--rules", R]),
    lambda: cli(["--clients", C, "--rules", R]),
    "differ", "live", "one SETUP line + exit 2 versus a report")
row("A07", "C12", "exit 2, reason one of usage",
    lambda: cli(["--clients"]),
    lambda: cli(["--clients", "/nonexistent/x", "--rules", R]),
    "differ", "live", "usage and unreadable are distinct reasons")
row("A08", "C13", "a directory, a FIFO or any non-regular file is unreadable",
    lambda: cli(["--clients", S, "--rules", R]),
    lambda: cli(["--clients", "/dev/null", "--rules", R]),
    "same", "live", "directory and chardev give the same SETUP unreadable; a regular file does not (A09)")
row("A09", "C13", "A PATH that is missing, unreadable",
    lambda: cli(["--clients", C, "--rules", R]),
    lambda: cli(["--clients", C, "--rules", RNAME]),
    "differ", "live", "missing rules file is unreadable")
row("A10", "C13", "(the tool must return, never block on one)",
    lambda: (lambda p: (os.path.exists(p), cli(["--clients", p, "--rules", R]))[1])(fifo()),
    lambda: cli(["--clients", C, "--rules", R]),
    "differ", "live", "a FIFO client path returns SETUP unreadable instead of blocking")
row("A11", "C13", "an input larger than 1048576 bytes is too_large",
    lambda: cli(["--clients", C, "--rules", R]),
    lambda: cli(["--clients", CBIG, "--rules", R]),
    "differ", "live", "1048577-byte clients file is too_large")
row("A12", "C13", "`--clients -` reads standard input",
    lambda: cli(["--clients", "-", "--rules", R], json.dumps(CL_OK).encode()),
    lambda: cli(["--clients", "-", "--rules", R], b"[]"),
    "differ", "live", "stdin is parsed as the clients document")
row("A13", "C13", "a clients input that is not UTF-8 JSON",
    lambda: cli(["--clients", "-", "--rules", R], b"\xff[]"),
    lambda: cli(["--clients", "-", "--rules", R], b"[]"),
    "differ", "live", "invalid UTF-8 is bad_json")
row("A14", "C13", "holding a list whose every element is an object",
    lambda: cli(["--clients", "-", "--rules", R], b"[1]"),
    lambda: cli(["--clients", "-", "--rules", R], b"[{}]"),
    "differ", "live", "a list of non-objects is bad_json")
row("A15", "C13", "(an empty input included)",
    lambda: cli(["--clients", "-", "--rules", R], b""),
    lambda: cli(["--clients", "-", "--rules", R], b"[]"),
    "differ", "live", "empty stdin is bad_json, not a report")
row("A16", "C14", "then the clients input (unreadable, too_large, bad_json)",
    lambda: cli(["--clients", CBIG, "--rules", RNAME]),
    lambda: cli(["--clients", C, "--rules", RNAME]),
    "differ", "live", "clients are judged before the rules: too_large beats unreadable")
row("A17", "C14", "then the rules files in argument order",
    lambda: (lambda p: cli(["--clients", C, "--rules", RNAME, "--rules", p]))(f("order-big.conf", b"#" * (lab.ref.MAX_BYTES + 1))),
    lambda: (lambda p: cli(["--clients", C, "--rules", p, "--rules", RNAME]))(f("order-big2.conf", b"#" * (lab.ref.MAX_BYTES + 1))),
    "differ", "live", "first rules file decides: unreadable (missing first) vs too_large (big first)")

def fifo():
    p = os.path.join(S, "f")
    if not os.path.exists(p):
        os.mkfifo(p)
    return p

# ---------------- Rules (C16-C24) ----------------
row("B01", "C16", "decoded as UTF-8 with errors replaced",
    lambda: cli(["--clients", f("inv-cl.json", json.dumps([{"class": "axb", "size": [10, 20], "floating": True}])),
                 "--rules", f("inv.conf", b"windowrule = size 10 20, match:class a\xffb\n")]),
    lambda: cli(["--clients", f("valid-cl.json", json.dumps([{"class": "axb", "size": [10, 20], "floating": True}])),
                 "--rules", f("valid.conf", b"windowrule = size 10 20, match:class axb\n")]),
    "differ", "live", "the invalid byte becomes U+FFFD, so the regex is unsupported (NO_SIZE_RULES) where the valid one AGREEs")
row("B02", "C16", "a line is stripped of spaces and tabs at both ends",
    lambda: rep([{"class": "a", "size": [1, 2], "floating": True}], ["\t  windowrule = size 1 2, match:class a \t\n"]),
    lambda: rep([{"class": "a", "size": [1, 2], "floating": True}], ["\x0bwindowrule = size 1 2, match:class a\x0b\n"]),
    "differ", "live", "spaces/tabs strip, a vertical tab does not (unsupported regex)")
row("B03", "C17", "A RULE LINE fully matches `windowrule[ \\t]*=(.*)`",
    lambda: rep([], ["windowrule = size 1 2, match:class a\n"]),
    lambda: rep([], ["windowrulev2 = size 1 2, class:a\n"]),
    "differ", "live", "windowrulev2 is ignored and counted nowhere")
row("B04", "C17", "and upper case `WindowRule` included",
    lambda: rep([], ["windowrule = size 1 2, match:class a\n"]),
    lambda: rep([], ["WindowRule = size 1 2, match:class a\n"]),
    "differ", "live", "matching is case-sensitive")
row("B05", "C17", "is ignored and counted nowhere",
    lambda: rep([], ["windowrulev2 = center on, class:a\nwindowrule = size 1 2, match:class a\n"]),
    lambda: rep([], ["windowrule = center on, match:class a\nwindowrule = size 1 2, match:class a\n"]),
    "differ", "live", "ignored line adds nothing; a rule line with a non-size effect adds to other")
row("B06", "C17", "`windowrule[ \\t]*=(.*)`",
    lambda: rep([{"class": "a", "size": [1, 2], "floating": True}], ["windowrule=size 1 2,match:class a\n"]),
    lambda: rep([{"class": "a", "size": [1, 2], "floating": True}], ["windowrule = size 1 2, match:class a\n"]),
    "same", "live-constraint", "zero-width `[ \\t]*` accepted; a required space would print usage-equivalent output (unsupported). byte-identical here")
row("B07", "C19", "The effect is the first token of field 0",
    lambda: rep([], ["windowrule = , match:class a\n"]),
    lambda: rep([], ["windowrule = size, match:class a\n"]),
    "differ", "live", "empty effect -> other=1; `size` with no argument -> unsupported=1")
row("B08", "C19", "tokens being separated by runs of spaces and tabs only",
    lambda: rep([{"class": "a", "size": [1, 2], "floating": True}], ["windowrule = size\t1\t2, match:class\ta\n"]),
    lambda: rep([{"class": "a", "size": [1, 2], "floating": True}], ["windowrule = size 1 2, match:class a\n"]),
    "same", "live-constraint", "tabs are separators exactly like spaces. Byte-identical")
row("B09", "C20", "An effect other than `size` and `float` adds one to `other`",
    lambda: rep([], ["windowrule = center on, match:class a\n"]),
    lambda: rep([], ["windowrule = size 1 2, match:class a\n"]),
    "differ", "live", "center increments other, size does not")
row("B10", "C21", "it has exactly two fields",
    lambda: rep([], ["windowrule = size 1 2, match:class a\n"]),
    lambda: rep([], ["windowrule = size 1 2, match:class a, match:title b\n"]),
    "differ", "live", "three fields -> unsupported")
row("B11", "C21", "two argument tokens fully matching `[0-9]{1,5}`",
    lambda: rep([], ["windowrule = size 99999 1, match:class a\n"]),
    lambda: rep([], ["windowrule = size 100000 1, match:class a\n"]),
    "differ", "live", "6 digits is unsupported")
row("B12", "C21", "(ASCII digits; size)",
    lambda: rep([], ["windowrule = size 420 500, match:class a\n"]),
    lambda: rep([], ["windowrule = size \u0664\u0662\u0660 500, match:class a\n"]),
    "differ", "live", "non-ASCII digits are unsupported")
row("B13", "C21", "exactly one token equal to `on` or `off` (float)",
    lambda: rep([], ["windowrule = float on, match:class a\n"]),
    lambda: rep([], ["windowrule = float On, match:class a\n"]),
    "differ", "live", "case-sensitive on/off")
row("B14", "C21", "field 1 fully matches `match:class[ \\t]+(.+)`",
    lambda: rep([], ["windowrule = size 1 2, match:class a\n"]),
    lambda: rep([], ["windowrule = size 1 2, match:title a\n"]),
    "differ", "live", "match:title -> unsupported")
row("B15", "C21", "REGEX fully matches 1-200 characters",
    lambda: rep([], ["windowrule = size 1 2, match:class %s\n" % ("a" * 200)]),
    lambda: rep([], ["windowrule = size 1 2, match:class %s\n" % ("a" * 201)]),
    "differ", "live", "200 accepted, 201 unsupported")
row("B16", "C21", "of `[A-Za-z0-9_.^$()|*+?-]`",
    lambda: rep([], ["windowrule = size 1 2, match:class a{2}\n"]),
    lambda: rep([], ["windowrule = size 1 2, match:class aa\n"]),
    "differ", "live", "{} outside the alphabet -> unsupported")
row("B17", "C21", "and the escapes `\\.` `\\-`",
    lambda: rep([{"class": "a.b", "size": [1, 2], "floating": True},
                 {"class": "axb", "size": [1, 2], "floating": True}], ["windowrule = size 1 2, match:class a\\.b\n"]),
    lambda: rep([{"class": "a.b", "size": [1, 2], "floating": True},
                 {"class": "axb", "size": [1, 2], "floating": True}], ["windowrule = size 1 2, match:class a.b\n"]),
    "differ", "live", "an escaped dot matches one way, a bare dot another")
row("B18", "C21", "contains none of the substrings `(?`",
    lambda: rep([], ["windowrule = size 1 2, match:class (?i)a\n"]),
    lambda: rep([], ["windowrule = size 1 2, match:class a\n"]),
    "differ", "live", "inline flags are unsupported although re would compile them")
row("B19", "C21", "`*+`, `++`, `?+`",
    lambda: rep([], ["windowrule = size 1 2, match:class a*+\n"]),
    lambda: rep([], ["windowrule = size 1 2, match:class a\n"]),
    "differ", "live", "py3.14 compiles a*+ (possessive), so the substring check is load-bearing")
row("B20", "C21", "and compiles under Python `re`",
    lambda: rep([], ["windowrule = size 1 2, match:class (a\n"]),
    lambda: rep([], ["windowrule = size 1 2, match:class (a)\n"]),
    "differ", "live", "uncompilable -> unsupported")
row("B21", "C22", "Any other size or float line adds one to `unsupported`",
    lambda: rep([], ["windowrule = size 1 2, match:class a\nwindowrule = size 1x 2, match:class a\n"]),
    lambda: rep([], ["windowrule = size 1 2, match:class a\n"]),
    "differ", "live", "unsupported counts the rejected size line")
row("B22", "C23", "numbered n=1.. across all files in argument order",
    lambda: rep([], ["windowrule = size 1 2, match:class a\n", "windowrule = float off, match:class b\n"]),
    lambda: rep([], ["windowrule = size 1 2, match:class a\n"]),
    "differ", "live", "n and file columns follow file argument order")
row("B23", "C24", "its class holds no character below U+0020",
    lambda: rep([{"class": "a\x01b", "size": [1, 2], "floating": True}], ["windowrule = size 1 2, match:class a.b\n"]),
    lambda: rep([{"class": "axb", "size": [1, 2], "floating": True}], ["windowrule = size 1 2, match:class a.b\n"]),
    "differ", "live", "a control character in the class blocks the match even though . would cover it")
row("B24", "C24", "`re.fullmatch(REGEX, class)` succeeds",
    lambda: rep([{"class": "ab", "size": [1, 2], "floating": True}], ["windowrule = size 1 2, match:class a\n"]),
    lambda: rep([{"class": "a", "size": [1, 2], "floating": True}], ["windowrule = size 1 2, match:class a\n"]),
    "differ", "live", "anchored (FullMatch), not a search")

# ---------------- Clients (C26-C31) ----------------
def c(cls="a", size=[1, 2], fl=True, **kw):
    d = {"class": cls, "size": size, "floating": fl}
    d.update(kw)
    return d

RT = ["windowrule = size 1 2, match:class a\n"]
row("C01", "C26", "An element whose `mapped` is JSON false is unmapped and skipped",
    lambda: rep([c(mapped=False)], RT), lambda: rep([c(mapped=True)], RT),
    "differ", "live", "unmapped=1 vs clients=1")
row("C02", "C26", "(0, null and \"false\" are not false)",
    lambda: rep([c(mapped=False)], RT), lambda: rep([c(mapped=0)], RT),
    "differ", "live", "0 is not false")
row("C03", "C26", "(0, null and \"false\" are not false)",
    lambda: rep([c(mapped=False)], RT), lambda: rep([c(mapped=None)], RT),
    "differ", "live", "null is not false")
row("C04", "C26", "(0, null and \"false\" are not false)",
    lambda: rep([c(mapped=False)], RT), lambda: rep([c(mapped="false")], RT),
    "differ", "live", "the string \"false\" is not false")
row("C05", "C27", "class is the `class` value when a string, else the empty string",
    lambda: rep([{"class": 5, "size": [1, 2], "floating": True}], ["windowrule = size 1 2, match:class .\n"]),
    lambda: rep([{"class": "5", "size": [1, 2], "floating": True}], ["windowrule = size 1 2, match:class .\n"]),
    "differ", "live", "a non-string class becomes \"\" (unmatched by .)")
row("C06", "C27", "floating is true only for JSON true",
    lambda: rep([c(fl=True)], RT), lambda: rep([c(fl=1)], RT),
    "differ", "live", "1 is TILED, true is AGREE")
row("C07", "C27", "a list of exactly two JSON integers",
    lambda: rep([c(size=[1, 2])], RT), lambda: rep([c(size=[1])], RT),
    "differ", "live", "one element -> BADSIZE")
row("C08", "C27", "(not booleans",
    lambda: rep([c(size=[1, 2])], RT), lambda: rep([c(size=[True, 2])], RT),
    "differ", "live", "JSON booleans are not integers")
row("C09", "C27", "not floats)",
    lambda: rep([c(size=[1, 2])], RT), lambda: rep([c(size=[1.0, 2])], RT),
    "differ", "live", "a JSON float is not an integer (the same input also violates 'integers')")
row("C10", "C27", "that are >= 0",
    lambda: rep([c(size=[1, 2])], RT), lambda: rep([c(size=[-1, 2])], RT),
    "differ", "live", "negative -> BADSIZE")
row("C11", "C27", "address is the `address` value when a string, else \"-\"",
    lambda: rep([c(address="0x5")], RT), lambda: rep([c(address=5)], RT),
    "differ", "live", "non-string address prints -")
row("C12", "C28", "the last matching `size` rule gives want",
    lambda: rep([c(size=[1, 2])], ["windowrule = size 1 2, match:class a\nwindowrule = size 3 4, match:class a\n"]),
    lambda: rep([c(size=[1, 2])], ["windowrule = size 3 4, match:class a\nwindowrule = size 1 2, match:class a\n"]),
    "differ", "live", "last match wins (DIFFER vs AGREE)")
row("C13", "C28", "the last matching `float` rule gives float_rule",
    lambda: rep([c()], ["windowrule = float on, match:class a\nwindowrule = float off, match:class a\nwindowrule = size 1 2, match:class a\n"]),
    lambda: rep([c()], ["windowrule = float off, match:class a\nwindowrule = float on, match:class a\nwindowrule = size 1 2, match:class a\n"]),
    "differ", "live", "float_rule=off vs on")
row("C15", "C30", "BADSIZE (size none) | TILED (not floating)",
    lambda: rep([c(size=[1.0, 2], fl=False)], RT), lambda: rep([c(fl=False)], RT),
    "differ", "live", "BADSIZE beats TILED: a bad size on a tiled client is BADSIZE")
row("C16", "C30", "| AGREE (size == want) | DIFFER",
    lambda: rep([c(size=[1, 2])], RT), lambda: rep([c(size=[1, 3])], RT),
    "differ", "live", "AGREE vs DIFFER and rc 0 vs 1")
row("C17", "C30", "TILED (not floating)",
    lambda: rep([c(fl=False)], RT), lambda: rep([c(size=[1, 3], fl=False)], RT),
    "same", "live-constraint", "size is ignored when not floating: both TILED (size column differs, verdict does not)",
    scope="rc+verdict")
row("C18", "C31", "A duplicate JSON key keeps its last value",
    lambda: rep(b'[{"class":"zz","class":"a","size":[1,2],"floating":true}]', RT),
    lambda: rep(b'[{"class":"a","class":"zz","size":[1,2],"floating":true}]', RT),
    "differ", "live", "the last class wins (AGREE vs NO_MATCHING_CLIENT)")

row("C19", "C31", "A duplicate JSON key keeps its last value",
    lambda: rep(b'[{"class":"a","size":[1,2],"floating":true,"address":"0x1","address":"0x2"}]', RT),
    lambda: rep(b'[{"class":"a","size":[1,2],"floating":true,"address":"0x1"}]', RT),
    "differ", "live", "a duplicated ADDRESS key also keeps the last value (no fixture carries a duplicate address key: F5)")

# ---------------- Output / verdict (C32-C33) ----------------
row("D01", "C32", "`<json>` is json.dumps(value) with ensure_ascii",
    lambda: rep([c(cls="\u00fc")], ["windowrule = size 1 2, match:class .\n"]),
    lambda: rep([c(cls="u")], ["windowrule = size 1 2, match:class .\n"]),
    "differ", "live", "class=\"\\u00fc\" (escaped) not class=\"ü\"")
row("D02", "C32", "WxH are decimal integers without leading zeros",
    lambda: rep([], ["windowrule = size 00420 500, match:class a\n"]),
    lambda: rep([], ["windowrule = size 420 500, match:class a\n"]),
    "same", "live-constraint", "leading zeros are normalised away: byte-identical (a raw echo would print 00420x500)")
row("D03", "C32", "per matched client (input order)",
    lambda: rep([c(cls="a", address="0x1"), c(cls="b", address="0x2")],
                ["windowrule = size 1 2, match:class a|b\n"]),
    lambda: rep([c(cls="b", address="0x2"), c(cls="a", address="0x1")],
                ["windowrule = size 1 2, match:class a|b\n"]),
    "differ", "live", "client lines follow input order")
row("D04", "C33", "V = NO_SIZE_RULES (rules=0; exit 4)",
    lambda: rep([c()], ""), lambda: rep([c()], ["windowrule = size 1 2, match:class z\n"]),
    "differ", "live", "rules=0 -> NO_SIZE_RULES; rules>0, matched=0 -> NO_MATCHING_CLIENT")
row("D05", "C33", "DIFFER (differ>0; exit 1) | NO_MATCHING_CLIENT (matched=0; exit 3)",
    lambda: rep([c(size=[9, 9])], RT), lambda: rep([c(cls="z")], RT),
    "differ", "live", "both verdicts are reachable, exit 1 vs 3")
row("D06", "C33", "tested in that order",
    lambda: rep([c()], ""), lambda: rep([c()], ["windowrule = float on, match:class a\n"]),
    "same", "live-constraint", "rules=0 with a matching float rule still reports NO_SIZE_RULES: the only live link of the order chain",
    scope="rc+verdict")

def project(rc, out, scope):
    lines = out.decode("utf-8", "replace").splitlines()
    if scope == "full":
        return (rc, out)
    last = lines[-1] if lines else ""
    verdict = last.split(" verdict=")[-1]
    if scope == "rc+verdict":
        return (rc, verdict)
    if scope == "no-float-rule":
        cols = []
        for ln in lines:
            if ln.startswith("MADO_GEOM_CLIENT: "):
                cols.append((ln.split(" want=")[1].split(" float_rule=")[0],
                             ln.split(" verdict=")[-1]))
        return (rc, verdict, tuple(cols))
    raise AssertionError(scope)


def run():
    out = []
    for r in ROWS:
        # fifo helper must exist before the lambda runs; create eagerly
        try:
            a = r["a"](); b = r["b"]()
        except Exception as exc:  # noqa
            out.append(dict({k: v for k, v in r.items() if k not in ("a", "b")},
                            a={"error": repr(exc)}, b={}, got="error",
                            ok=False, error=repr(exc)))
            continue
        sa, sb = lab.summary(*a), lab.summary(*b)
        pa, pb = project(*a, r.get("scope", "full")), project(*b, r.get("scope", "full"))
        got = "same" if pa == pb else "differ"
        out.append(dict(r, a=sa, b=sb, got=got,
                        ok=(got == r["expect"])))
    return out

if __name__ == "__main__":
    fifo()
    rows = run()
    bad = [x for x in rows if not x.get("ok")]
    print(json.dumps(rows, indent=1, ensure_ascii=False))
    print("ROWS=%d OK=%d BAD=%d" % (len(rows), len(rows) - len(bad), len(bad)))
    for x in bad:
        print("BAD", x["id"], x["expect"], x["got"], x.get("error"))
