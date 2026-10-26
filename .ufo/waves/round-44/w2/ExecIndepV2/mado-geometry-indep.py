#!/usr/bin/env python3
"""mado-geometry - does the size a window rule asks for match the size the compositor reports?

Hyprland 0.56.2 consumes a window rule `size W H` when a floating window opens
(the floating algorithm reads the rule's size and stores it as the window's box);
a tiled window never reads it. A maximized or fullscreen window shows that state's
box instead, so the rule's size is not what the client reports there: the tool names
those clients instead of comparing them. The compositor reports each mapped client's
size and `fullscreen` value in `hyprctl clients -j`. This tool joins the two read-only
inputs: the rule lines of one or more Hyprland config files and one
`hyprctl clients -j` dump.

    hyprctl clients -j | mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf
    mado-geometry.py --clients clients.json --rules a.conf --rules b.conf
    mado-geometry.py --selftest

It reads files and standard input only; it starts no process and opens no socket.

Arguments (two-token form only; anything else is usage): `--selftest` alone, or
`--clients V` exactly once and `--rules V` one or more times, in any order.
Setup failure: stdout is exactly one line `MADO_GEOMETRY: SETUP <reason>`, exit 2,
reason one of usage | unreadable | too_large | bad_json. A PATH that is missing,
unreadable, a directory, a FIFO or any non-regular file is unreadable; an input
larger than 1048576 bytes is too_large (stdin, `--clients -`, is read at most
1048577 bytes); a clients input that is not UTF-8 JSON holding a list whose every
element is an object is bad_json.

Rules. Each rules file is decoded as UTF-8 with errors replaced and split on
"\\n"; a line is stripped of spaces and tabs at both ends. A RULE LINE matches
`windowrule[ \\t]*=(.*)` (anything else, `windowrulev2` included, is ignored and
counted nowhere). The body is split on "," and each field is stripped of spaces
and tabs. The effect is the first token of field 0, tokens being separated by runs
of spaces and tabs only (the empty string when there is none). An effect other than
`size` and `float` adds one to `other`. A `size` or `float` line is SUPPORTED when:
field 0 has exactly two argument tokens `[0-9]{1,5}` (size) or exactly one token
`on` or `off` (float); there is exactly one more field and it is `match:class` + one
or more spaces/tabs + REGEX; REGEX is 1-200 characters of
`[A-Za-z0-9_.^$()|*+?-]` and the escapes `\\.` `\\-` `\\(` `\\)` `\\|` `\\*` `\\+`
`\\?` `\\^` `\\$` `\\\\`, contains none of `(?`, `*+`, `++`, `?+`, and compiles under
Python `re`. Any other size or float line adds one to `unsupported`. Supported rules
are numbered n=1.. across all files in order and each reports the 1-based index of
its file. A client MATCHES a rule when its class holds no character below U+0020 and
`re.fullmatch(REGEX, class)` succeeds (Hyprland: `RE2::FullMatch`).

Clients. An element whose `mapped` is JSON false is unmapped and skipped. For the
others class is the `class` value when a string, else ""; floating is true only
for JSON true; size is the `size` value when a list of exactly two JSON
integers (not booleans, not floats) >= 0, else none; address is `address` when
a string, else "-". The window state is the `fullscreen` value when that is a JSON
integer (not a boolean, not a float) equal to 2 (fullscreen) or 1 (maximized);
absent, null, 0, 3, -1, true, 2.0, "2", lists and objects are no state. Rules apply
in order: the last matching `size` rule gives want, the last matching `float` rule
gives float_rule (`on`, `off`, else `-`). A client with at least one matching size
rule is MATCHED and reports a verdict, tested in the order BADSIZE (size none) |
FULLSCREEN (state 2) | MAXIMIZED (state 1) | TILED (not floating) | AGREE (size ==
want) | DIFFER.

Output (stdout; nothing else; stderr empty on exit 0/1/3/4/5), in order:
  per supported rule   MADO_GEOM_RULE: n=<n> file=<k> effect=<size|float> arg=<WxH|on|off> class=<REGEX>
  per matched client   MADO_GEOM_CLIENT: addr=<json> class=<json> floating=<true|false> size=<WxH|-> want=<WxH> float_rule=<on|off|-> verdict=<V>
  last                 MADO_GEOMETRY: rules=<size rules> float_rules=<n> other=<n> unsupported=<n> clients=<mapped> matched=<n> unmapped=<n> agree=<n> differ=<n> tiled=<n> badsize=<n> maximized=<n> fullscreen=<n> verdict=<V>
(<json> is json.dumps with ensure_ascii.) The summary carries
` maximized=<n> fullscreen=<n>` between `badsize=<n>` and ` verdict=` exactly when
maximized + fullscreen > 0; otherwise it is the round-43 line, unchanged. V =
NO_SIZE_RULES (exit 4, rules=0) | DIFFER (exit 1, differ>0) | NO_MATCHING_CLIENT
(exit 3, matched=0) | NOT_COMPARED (exit 5, agree=0 and maximized + fullscreen > 0:
the matched clients were all in a state where nothing is compared) | OK (exit 0),
tested in that order. DIFFER is a report, not a fault: a user may have resized the
window, or the compositor may have clamped the rule's size.
"""
import json
import os
import re
import stat
import sys

MAX_BYTES = 1048576
RULE_LINE = re.compile(r"windowrule[ \t]*=(.*)")
MATCH_FIELD = re.compile(r"match:class[ \t]+(.+)")
SAFE = re.compile(r"(?:[A-Za-z0-9_.^$()|*+?-]|\\[.\-()|*+?^$\\]){1,200}")
NUM = re.compile(r"[0-9]{1,5}")
FULLSCREEN = 2
MAXIMIZED = 1


class Setup(Exception):
    pass


def read_regular(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except OSError:
        raise Setup("unreadable")
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise Setup("unreadable")
        data = b""
        while len(data) <= MAX_BYTES:
            chunk = os.read(fd, MAX_BYTES + 1 - len(data))
            if not chunk:
                break
            data += chunk
    except OSError:
        raise Setup("unreadable")
    finally:
        os.close(fd)
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data


def parse_args(argv):
    if argv == ["--selftest"]:
        return "selftest", None, None
    clients, rules, i = None, [], 0
    while i < len(argv):
        if i + 1 >= len(argv):
            raise Setup("usage")
        flag, value = argv[i], argv[i + 1]
        if flag == "--clients" and clients is None:
            clients = value
        elif flag == "--rules":
            rules.append(value)
        else:
            raise Setup("usage")
        i += 2
    if clients is None or not rules:
        raise Setup("usage")
    return "run", clients, rules


def regex_ok(rx):
    if not SAFE.fullmatch(rx):
        return False
    for bad in ("(?", "*+", "++", "?+"):
        if bad in rx:
            return False
    try:
        re.compile(rx)
    except re.error:
        return False
    return True


def parse_rule_text(text, file_index, rules, counts):
    for raw in text.split("\n"):
        line = raw.strip(" \t")
        m = RULE_LINE.fullmatch(line)
        if not m:
            continue
        body = m.group(1)
        fields = [f.strip(" \t") for f in body.split(",")]
        toks = [t for t in re.split("[ \t]+", fields[0]) if t]
        effect = toks[0] if toks else ""
        if effect not in ("size", "float"):
            counts["other"] += 1
            continue
        args = toks[1:]
        good = len(fields) == 2
        if good and effect == "size":
            good = len(args) == 2 and all(NUM.fullmatch(a) for a in args)
        elif good:
            good = len(args) == 1 and args[0] in ("on", "off")
        mm = MATCH_FIELD.fullmatch(fields[1]) if good else None
        if not mm or not regex_ok(mm.group(1)):
            counts["unsupported"] += 1
            continue
        arg = "%dx%d" % (int(args[0]), int(args[1])) if effect == "size" else args[0]
        rules.append({"file": file_index, "effect": effect, "arg": arg,
                      "want": (int(args[0]), int(args[1])) if effect == "size" else args[0],
                      "rx": mm.group(1)})


def parse_clients(data):
    try:
        doc = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise Setup("bad_json")
    if not isinstance(doc, list) or not all(isinstance(c, dict) for c in doc):
        raise Setup("bad_json")
    return doc


def client_size(c):
    s = c.get("size")
    if isinstance(s, list) and len(s) == 2 and all(
            isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in s):
        return (s[0], s[1])
    return None


def matches(rx, cls):
    if any(ord(ch) < 0x20 for ch in cls):
        return False
    return re.fullmatch(rx, cls) is not None


def fsmode_of(c):
    """2 for a fullscreen client, 1 for a maximized one, 0 otherwise.

    The `fullscreen` value counts only as a JSON integer equal to 1 or 2: a
    boolean, a float, a string, null or any other number is no state.
    """
    f = c.get("fullscreen")
    if type(f) is int:
        if f == MAXIMIZED or f == FULLSCREEN:
            return f
    return 0


def verdict_of(size, floating, want, c):
    """BADSIZE | FULLSCREEN | MAXIMIZED | TILED | AGREE | DIFFER, in that order.

    BADSIZE first: a client with no usable size cannot be compared at all. Then
    the two states that own the box - a fullscreen or maximized window shows the
    state's box, not the rule's size - then TILED, then the size comparison.
    """
    if size is None:
        return "BADSIZE"
    mode = fsmode_of(c)
    if mode == FULLSCREEN:
        return "FULLSCREEN"
    if mode == MAXIMIZED:
        return "MAXIMIZED"
    if not floating:
        return "TILED"
    if size == want:
        return "AGREE"
    return "DIFFER"


def evaluate(clients, rules):
    out = []
    tally = {"clients": 0, "matched": 0, "unmapped": 0, "agree": 0, "differ": 0,
             "tiled": 0, "badsize": 0, "maximized": 0, "fullscreen": 0}
    for c in clients:
        if c.get("mapped") is False:
            tally["unmapped"] += 1
            continue
        tally["clients"] += 1
        cls = c.get("class") if isinstance(c.get("class"), str) else ""
        want, frule = None, "-"
        for r in rules:
            if matches(r["rx"], cls):
                if r["effect"] == "size":
                    want = r["want"]
                else:
                    frule = r["want"]
        if want is None:
            continue
        tally["matched"] += 1
        size = client_size(c)
        floating = c.get("floating") is True
        verdict = verdict_of(size, floating, want, c)
        tally[verdict.lower()] += 1
        addr = c.get("address") if isinstance(c.get("address"), str) else "-"
        out.append("MADO_GEOM_CLIENT: addr=%s class=%s floating=%s size=%s want=%dx%d float_rule=%s verdict=%s" % (
            json.dumps(addr), json.dumps(cls), "true" if floating else "false",
            "%dx%d" % size if size else "-", want[0], want[1], frule, verdict))
    return out, tally


def report(clients_data, rule_texts):
    rules, counts = [], {"other": 0, "unsupported": 0}
    for k, text in enumerate(rule_texts, 1):
        parse_rule_text(text, k, rules, counts)
    lines = ["MADO_GEOM_RULE: n=%d file=%d effect=%s arg=%s class=%s" % (
        n, r["file"], r["effect"], r["arg"], r["rx"]) for n, r in enumerate(rules, 1)]
    clines, t = evaluate(parse_clients(clients_data), rules)
    lines += clines
    size_rules = sum(1 for r in rules if r["effect"] == "size")
    states = t["maximized"] + t["fullscreen"]
    if size_rules == 0:
        verdict, rc = "NO_SIZE_RULES", 4
    elif t["differ"] > 0:
        verdict, rc = "DIFFER", 1
    elif t["matched"] == 0:
        verdict, rc = "NO_MATCHING_CLIENT", 3
    elif t["agree"] == 0 and states > 0:
        verdict, rc = "NOT_COMPARED", 5
    else:
        verdict, rc = "OK", 0
    shown = ""
    if states > 0:
        shown = " maximized=%d fullscreen=%d" % (t["maximized"], t["fullscreen"])
    lines.append("MADO_GEOMETRY: rules=%d float_rules=%d other=%d unsupported=%d clients=%d "
                 "matched=%d unmapped=%d agree=%d differ=%d tiled=%d badsize=%d%s verdict=%s" % (
                     size_rules, len(rules) - size_rules, counts["other"], counts["unsupported"],
                     t["clients"], t["matched"], t["unmapped"], t["agree"], t["differ"],
                     t["tiled"], t["badsize"], shown, verdict))
    return lines, rc


def run(argv, stdin):
    mode, clients, rules = parse_args(argv)
    if mode == "selftest":
        return selftest()
    if clients == "-":
        data = stdin.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise Setup("too_large")
    else:
        data = read_regular(clients)
    texts = [read_regular(p).decode("utf-8", "replace") for p in rules]
    lines, rc = report(data, texts)
    sys.stdout.write("\n".join(lines) + "\n")
    return rc


def selftest():
    cases = []
    gk = "windowrule = float on, match:class ^(org.omarchy.gkeep)$\nwindowrule = size 420 500, match:class ^(org.omarchy.gkeep)$\n"

    def cl(cls, size, floating=True, mapped=True, addr="0x1", **kw):
        d = {"class": cls, "size": size, "floating": floating, "mapped": mapped, "address": addr}
        d.update(kw)
        return d

    def last(clients, text):
        lines, rc = report(json.dumps(clients).encode(), [text])
        return lines[-1], rc

    def chk(name, got, want):
        cases.append((name, got == want, got, want))

    def state_line(verdict, states="", **kw):
        f = dict(rules=1, float_rules=1, other=0, unsupported=0, clients=1, matched=1,
                 unmapped=0, agree=0, differ=0, tiled=0, badsize=0)
        f.update(kw)
        f["verdict"] = verdict
        return ("MADO_GEOMETRY: rules=%(rules)d float_rules=%(float_rules)d other=%(other)d "
                "unsupported=%(unsupported)d clients=%(clients)d matched=%(matched)d "
                "unmapped=%(unmapped)d agree=%(agree)d differ=%(differ)d tiled=%(tiled)d "
                "badsize=%(badsize)d" % f) + states + " verdict=" + verdict

    g = "org.omarchy.gkeep"
    s, rc = last([cl(g, [420, 500])], gk)
    chk("agree-rc", rc, 0)
    chk("agree-line", s, "MADO_GEOMETRY: rules=1 float_rules=1 other=0 unsupported=0 clients=1 matched=1 unmapped=0 agree=1 differ=0 tiled=0 badsize=0 verdict=OK")
    s, rc = last([cl(g, [421, 500])], gk)
    chk("differ-rc", rc, 1)
    chk("differ-verdict", s.endswith("differ=1 tiled=0 badsize=0 verdict=DIFFER"), True)
    s, rc = last([cl(g, [420, 500], floating=False)], gk)
    chk("tiled-rc", rc, 0)
    chk("tiled-count", " tiled=1 " in s, True)
    s, rc = last([cl(g, [420.0, 500])], gk)
    chk("float-size-badsize", " badsize=1 " in s, True)
    s, rc = last([cl(g, [True, 500])], gk)
    chk("bool-size-badsize", " badsize=1 " in s, True)
    s, rc = last([cl(g, [420])], gk)
    chk("short-size-badsize", " badsize=1 " in s, True)
    s, rc = last([cl(g, [-1, 500])], gk)
    chk("negative-size-badsize", " badsize=1 " in s, True)
    s, rc = last([cl(g, [420, 500], mapped=False)], gk)
    chk("unmapped-rc", rc, 3)
    chk("unmapped-count", " clients=0 matched=0 unmapped=1 " in s, True)
    s, rc = last([], gk)
    chk("empty-rc", rc, 3)
    s, rc = last([cl("other", [1, 1])], gk)
    chk("nomatch-rc", rc, 3)
    s, rc = last([cl(g + "x", [420, 500])], gk)
    chk("fullmatch-not-search", rc, 3)
    s, rc = last([cl(g, [420, 500])], "windowrule = float on, match:class ^(org.omarchy.gkeep)$\n")
    chk("no-size-rule-rc", rc, 4)
    s, rc = last([cl(g, [420, 500])], "")
    chk("empty-rules-rc", rc, 4)
    chk("empty-rules-line", s, "MADO_GEOMETRY: rules=0 float_rules=0 other=0 unsupported=0 clients=1 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_SIZE_RULES")
    s, rc = last([cl("a", [10, 20])], "windowrule = size 10 20, match:class a\nwindowrule = size 30 40, match:class a\n")
    chk("last-size-wins", " differ=1 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = size 30 40, match:class a\nwindowrule = size 10 20, match:class ^a$\n")
    chk("last-size-wins-agree", rc, 0)
    s, rc = last([cl("ab", [10, 20])], "windowrule = size 10 20, match:class a|ab\n")
    chk("alternation-fullmatch", rc, 0)
    s, rc = last([cl("a.b", [10, 20]), cl("axb", [1, 1])], "windowrule = size 10 20, match:class a\\.b\n")
    chk("escaped-dot-matches-one", " matched=1 " in s, True)
    s, rc = last([cl("a", [10, 20])], "  windowrule=size 10 20,match:class a  \n")
    chk("tight-spacing", rc, 0)
    s, rc = last([cl("a", [10, 20])], "windowrule = size 10 20, match:title a\n")
    chk("title-unsupported", " unsupported=1 " in s and rc == 4, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = size 10 20 30, match:class a\n")
    chk("three-args-unsupported", " unsupported=1 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = size 1x 20, match:class a\n")
    chk("nondigit-unsupported", " unsupported=1 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = size 123456 20, match:class a\n")
    chk("six-digits-unsupported", " unsupported=1 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = size 10 20, match:class a, match:title b\n")
    chk("two-matches-unsupported", " unsupported=1 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = size 10 20, match:class a # note\n")
    chk("hash-unsupported", " unsupported=1 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = size 10 20, match:class negative:a\n")
    chk("negative-prefix-unsupported", " unsupported=1 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = size 10 20, match:class (?i)a\n")
    chk("inline-flag-unsupported", " unsupported=1 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = size 10 20, match:class a*+\n")
    chk("possessive-unsupported", " unsupported=1 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = size 10 20, match:class (a\n")
    chk("uncompilable-unsupported", " unsupported=1 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = float maybe, match:class a\nwindowrule = size 10 20, match:class a\n")
    chk("float-arg-unsupported", " unsupported=1 " in s and " float_rules=0 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = center on, match:class a\nwindowrule = opacity 1, match:class a\nwindowrule = size 10 20, match:class a\n")
    chk("other-counted", " other=2 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrulev2 = size 10 20, class:a\n# windowrule = size 10 20, match:class a\nwindowrule = size 10 20, match:class a\n")
    chk("v2-and-comment-ignored", " rules=1 float_rules=0 other=0 unsupported=0 " in s, True)
    s, rc = last([cl("a", [10, 20])], "windowrule = size 10 20, match:class a\r\n")
    chk("cr-breaks-regex", " unsupported=1 " in s, True)
    s, rc = last([cl("a\nb", [10, 20])], "windowrule = size 10 20, match:class a.b\n")
    chk("control-char-class-unmatched", rc, 3)
    s, rc = last([{"size": [10, 20], "floating": True}], "windowrule = size 10 20, match:class .*\n")
    chk("missing-class-empty", rc, 0)
    s, rc = last([{"class": 5, "size": [10, 20], "floating": True}], "windowrule = size 10 20, match:class .*\n")
    chk("non-string-class-empty", rc, 0)
    s, rc = last([{"class": "a", "size": [10, 20], "floating": 1}], "windowrule = size 10 20, match:class a\n")
    chk("non-true-floating-tiled", " tiled=1 " in s, True)
    s, rc = last([{"class": "a", "size": [10, 20], "floating": True, "mapped": 0}], "windowrule = size 10 20, match:class a\n")
    chk("non-false-mapped-counts", " clients=1 " in s and " unmapped=0 " in s, True)
    lines, rc = report(json.dumps([cl("ü a", [10, 20], addr="0xa\"b")]).encode(), ["windowrule = size 10 20, match:class .*\n"])
    chk("json-escaped-fields", lines[1], 'MADO_GEOM_CLIENT: addr="0xa\\"b" class="\\u00fc a" floating=true size=10x20 want=10x20 float_rule=- verdict=AGREE')
    chk("rule-line", lines[0], "MADO_GEOM_RULE: n=1 file=1 effect=size arg=10x20 class=.*")
    lines, rc = report(b"[]", ["windowrule = size 10 20, match:class a\n", "windowrule = float off, match:class a\nwindowrule = size 07 08, match:class b\n"])
    chk("file-index-and-numbering", lines[:3], ["MADO_GEOM_RULE: n=1 file=1 effect=size arg=10x20 class=a",
                                                 "MADO_GEOM_RULE: n=2 file=2 effect=float arg=off class=a",
                                                 "MADO_GEOM_RULE: n=3 file=2 effect=size arg=7x8 class=b"])
    lines, rc = report(json.dumps([cl("a", [1, 2]), cl("b", [7, 8])]).encode(),
                       ["windowrule = float on, match:class a\nwindowrule = size 1 2, match:class a\nwindowrule = size 7 8, match:class b\n"])
    chk("float-rule-reported", lines[3].split(" float_rule=")[1].split(" ")[0], "on")
    chk("unset-float-rule", lines[4].split(" float_rule=")[1].split(" ")[0], "-")
    for bad, label in ((b"{}", "object"), (b"[1]", "list-of-int"), (b"", "empty"), (b"\xff", "bytes"), (b"[", "truncated")):
        try:
            report(bad, ["x"])
            chk("bad-json-" + label, "no-raise", "bad_json")
        except Setup as exc:
            chk("bad-json-" + label, str(exc), "bad_json")
    for argv, label in (([], "none"), (["--clients", "-"], "no-rules"), (["--rules", "x"], "no-clients"),
                        (["--clients", "-", "--clients", "-", "--rules", "x"], "double-clients"),
                        (["--clients"], "dangling"), (["--clients", "-", "--rules", "x", "--bogus"], "bogus"),
                        (["--selftest", "--rules", "x"], "selftest-with-args"), (["--client", "-", "--rules", "x"], "abbrev")):
        try:
            parse_args(argv)
            chk("usage-" + label, "no-raise", "usage")
        except Setup as exc:
            chk("usage-" + label, str(exc), "usage")
    chk("rules-repeat-ok", parse_args(["--rules", "a", "--clients", "-", "--rules", "b"]), ("run", "-", ["a", "b"]))
    for path, label in (("/nonexistent/none", "missing"), ("/", "dir"), ("/dev/null", "chardev")):
        try:
            read_regular(path)
            chk("unreadable-" + label, "no-raise", "unreadable")
        except Setup as exc:
            chk("unreadable-" + label, str(exc), "unreadable")
    chk("regex-safe-accepts", regex_ok("^(a|b)+\\.c$"), True)
    chk("regex-safe-rejects-brace", regex_ok("a{2}"), False)
    chk("regex-safe-rejects-class", regex_ok("[ab]"), False)
    chk("regex-safe-rejects-201", regex_ok("a" * 201), False)
    chk("regex-safe-accepts-200", regex_ok("a" * 200), True)
    chk("regex-safe-rejects-empty", regex_ok(""), False)
    chk("regex-safe-rejects-bad-escape", regex_ok("\\d"), False)
    chk("matches-ctl", matches("a", "a\x01"), False)
    chk("matches-full", matches("a", "ab"), False)
    # ---- round-44: the client state (fullscreen) is named, not compared
    lines, rc = report(json.dumps([cl(g, [2560, 1440], fullscreen=2)]).encode(), [gk])
    chk("fs-rc", rc, 5)
    chk("fs-client-line", lines[-2], "MADO_GEOM_CLIENT: addr=\"0x1\" class=\"org.omarchy.gkeep\" floating=true size=2560x1440 want=420x500 float_rule=on verdict=FULLSCREEN")
    chk("fs-summary", lines[-1], "MADO_GEOMETRY: rules=1 float_rules=1 other=0 unsupported=0 clients=1 matched=1 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 maximized=0 fullscreen=1 verdict=NOT_COMPARED")
    s, rc = last([cl(g, [420, 500], fullscreen=2)], gk)
    chk("fs-matching-size-not-agree", rc, 5)
    chk("fs-matching-size-line", s, state_line("NOT_COMPARED", " maximized=0 fullscreen=1"))
    lines, rc = report(json.dumps([cl(g, [2544, 1380], floating=False, fullscreen=1)]).encode(), [gk])
    chk("max-rc", rc, 5)
    chk("max-client-line", lines[-2].split(" verdict=")[1], "MAXIMIZED")
    chk("max-summary", lines[-1], state_line("NOT_COMPARED", " maximized=1 fullscreen=0"))
    s, rc = last([cl(g, [2544, 1380], fullscreen=1)], gk)
    chk("max-float-rc", rc, 5)
    chk("max-float-count", " maximized=1 fullscreen=0 " in s, True)
    lines, rc = report(json.dumps([cl(g, [420.0, 500], fullscreen=2)]).encode(), [gk])
    chk("fs-badsize-rc", rc, 0)
    chk("fs-badsize-line", lines[-1], state_line("OK", "", badsize=1))
    s, rc = last([cl(g, [True, 500], fullscreen=2)], gk)
    chk("fs-bool-size-badsize", " badsize=1 " in s and " maximized=" not in s and rc == 0, True)
    s, rc = last([cl(g, None, fullscreen=1)], gk)
    chk("max-nosize-badsize", " badsize=1 " in s and " maximized=" not in s and rc == 0, True)
    for v in (True, False, 3, 2.0, "2", -1, None, [2], {"internal": 2}, 0):
        s, rc = last([cl(g, [421, 500], fullscreen=v)], gk)
        chk("fs-value-ignored-%r" % (v,), (rc, " maximized=" in s, " differ=1 " in s), (1, False, True))
    s, rc = last([cl(g, [2544, 1380], fullscreen=1, fullscreenClient=2)], gk)
    chk("fsclient-ignored-maximized", " maximized=1 fullscreen=0 " in s and rc == 5, True)
    s, rc = last([cl(g, [421, 500], fullscreenClient=2)], gk)
    chk("fsclient-alone-ignored", " maximized=" not in s and rc == 1, True)
    lines, rc = report(b'[{"class": "org.omarchy.gkeep", "size": [9, 9], "floating": true, "fullscreen": 0, "fullscreen": 2}]', [gk])
    chk("fs-dupkeys-last-wins", (rc, lines[-2].split(" verdict=")[1]), (5, "FULLSCREEN"))
    lines, rc = report(b'[{"class": "org.omarchy.gkeep", "size": [9, 9], "floating": true, "fullscreen": 2, "fullscreen": 0}]', [gk])
    chk("fs-dupkeys-last-zero", (rc, lines[-2].split(" verdict=")[1]), (1, "DIFFER"))
    lines, rc = report(json.dumps([cl(g, [2560, 1440], fullscreen=2, addr="0x1"),
                                   cl(g, [421, 500], addr="0x2"),
                                   cl(g, [420, 500], addr="0x3"),
                                   cl(g, [1, 1], floating=False, addr="0x4"),
                                   cl(g, [2544, 1380], fullscreen=1, addr="0x5")]).encode(), [gk])
    chk("fsmix-rc", rc, 1)
    chk("fsmix-summary", lines[-1], state_line("DIFFER", " maximized=1 fullscreen=1",
                                               clients=5, matched=5, agree=1, differ=1,
                                               tiled=1, badsize=0))
    lines, rc = report(json.dumps([cl(g, [2560, 1440], fullscreen=2), cl(g, [420, 500])]).encode(), [gk])
    chk("fs-plus-agree-rc", rc, 0)
    chk("fs-plus-agree-summary", lines[-1], state_line("OK", " maximized=0 fullscreen=1",
                                                       clients=2, matched=2, agree=1))
    lines, rc = report(json.dumps([cl(g, [2560, 1440], fullscreen=2), cl(g, [421, 500])]).encode(), [gk])
    chk("fs-plus-differ-rc", rc, 1)
    chk("fs-plus-differ-summary", lines[-1], state_line("DIFFER", " maximized=0 fullscreen=1",
                                                        clients=2, matched=2, differ=1))
    lines, rc = report(json.dumps([cl(g, [2560, 1440], fullscreen=2), cl(g, [2544, 1380], fullscreen=1)]).encode(), [gk])
    chk("fs-and-max-rc", rc, 5)
    chk("fs-and-max-summary", lines[-1], state_line("NOT_COMPARED", " maximized=1 fullscreen=1",
                                                    clients=2, matched=2))
    lines, rc = report(json.dumps([{"class": "kitty", "size": [9, 9], "floating": True, "fullscreen": 2},
                                   cl(g, [420, 500])]).encode(), [gk])
    chk("fs-unmatched-not-counted", (rc, " maximized=" in lines[-1]), (0, False))
    lines, rc = report(json.dumps([cl(g, [2560, 1440], fullscreen=2, mapped=False),
                                   cl(g, [420, 500])]).encode(), [gk])
    chk("fs-unmapped-not-counted", (rc, " maximized=" in lines[-1]), (0, False))
    lines, rc = report(json.dumps([cl(g, [2560, 1440], fullscreen=2)]).encode(),
                       ["windowrule = float on, match:class ^(org.omarchy.gkeep)$\n"])
    chk("fs-no-size-rule", (rc, " maximized=" in lines[-1]), (4, False))
    lines, rc = report(json.dumps([cl(g, [2560, 1440], fullscreen=2)]).encode(), [""])
    chk("fs-no-rules", (rc, " maximized=" in lines[-1]), (4, False))
    lines, rc = report(json.dumps([cl(g, [420, 500], floating=False)]).encode(), [gk])
    chk("tiled-only-ok", (rc, lines[-1]), (0, state_line("OK", "", tiled=1)))
    chk("fsmode-two", fsmode_of({"fullscreen": 2}), 2)
    chk("fsmode-one", fsmode_of({"fullscreen": 1}), 1)
    chk("fsmode-zero", fsmode_of({"fullscreen": 0}), 0)
    chk("fsmode-three", fsmode_of({"fullscreen": 3}), 0)
    chk("fsmode-bool", fsmode_of({"fullscreen": True}), 0)
    chk("fsmode-float", fsmode_of({"fullscreen": 2.0}), 0)
    chk("fsmode-string", fsmode_of({"fullscreen": "2"}), 0)
    chk("fsmode-null", fsmode_of({"fullscreen": None}), 0)
    chk("fsmode-absent", fsmode_of({}), 0)
    chk("verdict-badsize-beats-state", verdict_of(None, True, (420, 500), {"fullscreen": 2}), "BADSIZE")
    chk("verdict-state-beats-tiled", verdict_of((2560, 1440), False, (420, 500), {"fullscreen": 2}), "FULLSCREEN")
    chk("verdict-maximized", verdict_of((2544, 1380), True, (420, 500), {"fullscreen": 1}), "MAXIMIZED")
    chk("verdict-tiled", verdict_of((420, 500), False, (420, 500), {}), "TILED")
    chk("verdict-agree", verdict_of((420, 500), True, (420, 500), {}), "AGREE")
    chk("verdict-differ", verdict_of((1, 1), True, (420, 500), {}), "DIFFER")
    bad = [c for c in cases if not c[1]]
    for name, _ok, got, want in bad:
        print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))
    print("MADO_GEOMETRY_SELFTEST: %d/%d passed" % (len(cases) - len(bad), len(cases)))
    return 0 if not bad else 1


def main():
    try:
        return run(sys.argv[1:], sys.stdin.buffer)
    except Setup as exc:
        print("MADO_GEOMETRY: SETUP %s" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
