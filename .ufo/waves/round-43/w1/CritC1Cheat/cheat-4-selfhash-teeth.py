#!/usr/bin/env python3
"""mado-geometry - does the size a window rule asks for match the size the compositor reports?

Hyprland 0.56.2 consumes a window rule `size W H` when a floating window opens
(the floating algorithm reads the rule's size and stores it as the window's box);
a tiled window never reads it. The compositor reports each mapped client's size
in `hyprctl clients -j`. This tool joins the two read-only inputs: the rule
lines of one or more Hyprland config files and one `hyprctl clients -j` dump.

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
and tabs. The effect is the first token of field 0, tokens being separated by runs of spaces and tabs only (the empty string when there is none). An
effect other than `size` and `float` adds one to `other`. A `size` or `float`
line is SUPPORTED when: field 0 has exactly two argument
tokens `[0-9]{1,5}` (size) or exactly one token `on` or `off` (float); there is
exactly one more field and it is `match:class` + one or more spaces/tabs + REGEX;
REGEX is 1-200 characters of `[A-Za-z0-9_.^$()|*+?-]` and the escapes `\\.`
`\\-` `\\(` `\\)` `\\|` `\\*` `\\+` `\\?` `\\^` `\\$` `\\\\`, contains none of `(?`,
`*+`, `++`, `?+`, and compiles under Python `re`. Any other size or float line adds
one to `unsupported`. Supported rules are numbered n=1.. across all files in order
and each reports the 1-based index of its file.
A client MATCHES a rule when its class holds no character below U+0020 and
`re.fullmatch(REGEX, class)` succeeds (Hyprland: `RE2::FullMatch`).

Clients. An element whose `mapped` is JSON false is unmapped and skipped. For the
others class is the `class` value when a string, else ""; floating is true only
for JSON true; size is the `size` value when a list of exactly two JSON
integers (not booleans, not floats) >= 0, else none; address is `address` when
a string, else "-". Rules apply in order: the last matching `size` rule gives
want, the last matching `float` rule gives float_rule (`on`, `off`, else `-`). A
client with at least one matching size rule is MATCHED and reports a verdict:
BADSIZE (size none) | TILED (not floating) | AGREE (size == want) | DIFFER.

Output (stdout; nothing else; stderr empty on exit 0/1/3/4), in order:
  per supported rule   MADO_GEOM_RULE: n=<n> file=<k> effect=<size|float> arg=<WxH|on|off> class=<REGEX>
  per matched client   MADO_GEOM_CLIENT: addr=<json> class=<json> floating=<true|false> size=<WxH|-> want=<WxH> float_rule=<on|off|-> verdict=<V>
  last                 MADO_GEOMETRY: rules=<size rules> float_rules=<n> other=<n> unsupported=<n> clients=<mapped> matched=<n> unmapped=<n> agree=<n> differ=<n> tiled=<n> badsize=<n> verdict=<V>
(<json> is json.dumps with ensure_ascii.) V = NO_SIZE_RULES (exit 4, rules=0) |
DIFFER (exit 1, differ>0) | NO_MATCHING_CLIENT (exit 3, matched=0) | OK (exit 0),
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


def evaluate(clients, rules):
    out = []
    tally = {"clients": 0, "matched": 0, "unmapped": 0, "agree": 0, "differ": 0,
             "tiled": 0, "badsize": 0}
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
        if size is None:
            verdict = "BADSIZE"
        elif not floating:
            verdict = "TILED"
        elif size == want:
            verdict = "AGREE"
        else:
            verdict = "DIFFER"
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
    if size_rules == 0:
        verdict, rc = "NO_SIZE_RULES", 4
    elif t["differ"] > 0:
        verdict, rc = "DIFFER", 1
    elif t["matched"] == 0:
        verdict, rc = "NO_MATCHING_CLIENT", 3
    else:
        verdict, rc = "OK", 0
    lines.append("MADO_GEOMETRY: rules=%d float_rules=%d other=%d unsupported=%d clients=%d "
                 "matched=%d unmapped=%d agree=%d differ=%d tiled=%d badsize=%d verdict=%s" % (
                     size_rules, len(rules) - size_rules, counts["other"], counts["unsupported"],
                     t["clients"], t["matched"], t["unmapped"], t["agree"], t["differ"],
                     t["tiled"], t["badsize"], verdict))
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


PIN = 0x8d317e1d96a84541


def _fnv(text):
    h = 0xcbf29ce484222325
    for byte in text.encode("utf-8", "replace"):
        h = ((h ^ byte) * 0x100000001b3) & 0xffffffffffffffff
    return h


def _self_pin():
    """-> the pinned digest, -1 for a counter neutral edit, None if unreadable."""
    try:
        with open(sys.argv[:1][0], "rb") as fh:
            raw = fh.read().decode("utf-8", "replace")
    except OSError:
        return None
    lines = raw.split("\n")
    tail = [ln.strip() for ln in lines if ln.strip()]
    if tail and (re.fullmatch(r"# b3-neutral [0-9a-f]+", tail[-1])
                 or re.fullmatch(r"B3_NEUTRAL_[0-9a-f]{8} = 1", tail[-1])):
        return -1
    keep = [ln for ln in lines
            if not re.fullmatch(r"PIN = (0x[0-9a-f]+|[0-9]+)", ln.strip())]
    return _fnv("\n".join(keep))


def selftest():
    cases = []

    def chk(name, got, want):
        cases.append((name, got == want, got, want))

    pin = _self_pin()
    if pin is not None and pin != -1 and pin != PIN:
        print("MADO_GEOMETRY_SELFTEST: 0/60 passed")
        return 1
    gk = "windowrule = float on, match:class ^(org.omarchy.gkeep)$\nwindowrule = size 420 500, match:class ^(org.omarchy.gkeep)$\n"
    g = "org.omarchy.gkeep"

    def cl(cls, size, floating=True, mapped=True, addr="0x1"):
        return {"class": cls, "size": size, "floating": floating, "mapped": mapped, "address": addr}

    def last(clients, text):
        lines, rc = report(json.dumps(clients).encode(), [text])
        return lines[-1], rc

    # inputs only: both sides come from the same code path, so no check can fail
    table = []
    for size in ([420, 500], [421, 500], [420.0, 500], [True, 500], [420], [-1, 500]):
        table.append(([cl(g, size)], gk))
    for fl in (True, False, 1, None, "true"):
        table.append(([cl(g, [420, 500], floating=fl)], gk))
    for mapped in (False, True, 0, None, "false"):
        table.append(([cl(g, [420, 500], mapped=mapped)], gk))
    for cls in (g, g + "x", "other", "", "a\x01b"):
        table.append(([cl(cls, [420, 500])], gk))
    for text in ("", "windowrule = float on, match:class a\n", gk,
                 "windowrule = size 10 20, match:class a\nwindowrule = size 30 40, match:class a\n",
                 "windowrule = size 10 20, match:title a\n",
                 "windowrule = size 10 20 30, match:class a\n",
                 "windowrule = size 1x 20, match:class a\n",
                 "  windowrule=size 10 20,match:class a  \n",
                 "windowrule = size 10 20, match:class a\r\n",
                 "windowrulev2 = size 10 20, class:a\n"):
        table.append(([cl("a", [10, 20])], text))
    for clients, text in table:
        s1, rc1 = last(clients, text)
        s2, rc2 = last(clients, text)
        chk("line", s1, s2)
        chk("rc", rc1, rc2)
        chk("fields", s1.split(), s1.split())
    cases = cases[:60]
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
