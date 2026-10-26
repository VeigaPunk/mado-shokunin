#!/usr/bin/env python3
"""mado-geometry.py - read-only join of window-rule sizes and compositor client sizes.

Usage: mado-geometry.py --clients V --rules V [--rules V ...]
       mado-geometry.py --selftest

Reads one clients JSON dump (V "-" means standard input) and one or more
Hyprland rule files, and prints MADO_GEOM_RULE lines for the supported size
and float rules, MADO_GEOM_CLIENT lines for the clients matched by a size
rule, and one MADO_GEOMETRY summary line.  Nothing is written anywhere and no
child process is started.
"""
import json
import os
import re
import stat
import sys

MAX_BYTES = 1048576
SETUP_PREFIX = "MADO_GEOMETRY: SETUP "
BLANKS = " \t"
RULE_HEAD = "windowrule"
MATCH_HEAD = "match:class"
DIGITS = "0123456789"
REGEX_CHARS = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
               "abcdefghijklmnopqrstuvwxyz"
               "0123456789"
               "_.^$()|*+?-")
ESCAPABLE = ".-()|*+?^$" + "\\"
FORBIDDEN = ("(?", "*+", "++", "?+")
RULE_PREFIX = "MADO_GEOM_RULE: "
CLIENT_PREFIX = "MADO_GEOM_CLIENT: "
SELFTEST_PREFIX = "MADO_GEOMETRY_SELFTEST: "


# --------------------------------------------------------------- text layer
def strip_blanks(text):
    return text.strip(BLANKS)


def tokens(text):
    """Split on runs of spaces and tabs only; no other separator."""
    out = []
    cur = []
    for ch in text:
        if ch == " " or ch == "\t":
            if cur:
                out.append("".join(cur))
                cur = []
        else:
            cur.append(ch)
    if cur:
        out.append("".join(cur))
    return out


def rule_body(line):
    """Body of a `windowrule[ \\t]*=(.*)` line, else None."""
    if not line.startswith(RULE_HEAD):
        return None
    i = len(RULE_HEAD)
    n = len(line)
    while i < n:
        ch = line[i]
        if ch == " " or ch == "\t":
            i += 1
        else:
            break
    if i >= n:
        return None
    if line[i] != "=":
        return None
    return line[i + 1:]


def class_field(field):
    """Capture of `match:class[ \\t]+(.+)` over a whole field, else None."""
    if not field.startswith(MATCH_HEAD):
        return None
    n = len(field)
    i = len(MATCH_HEAD)
    j = i
    while j < n:
        ch = field[j]
        if ch == " " or ch == "\t":
            j += 1
        else:
            break
    if j == i:
        return None
    rest = field[j:]
    if rest == "":
        return None
    return rest


def digit_arg(text):
    """True when text is 1 to 5 ASCII digits."""
    n = len(text)
    if n < 1 or n > 5:
        return False
    for ch in text:
        if ch not in DIGITS:
            return False
    return True


def charset_ok(text):
    """True when text is 1-200 characters of the rule-regex alphabet."""
    n = len(text)
    if n < 1 or n > 200:
        return False
    i = 0
    while i < n:
        ch = text[i]
        if ch == "\\":
            if i + 1 >= n:
                return False
            if text[i + 1] not in ESCAPABLE:
                return False
            i += 2
        else:
            if ch not in REGEX_CHARS:
                return False
            i += 1
    return True


def prepare_regex(text):
    """Compiled pattern for an acceptable rule regex, else None."""
    if not charset_ok(text):
        return None
    for bad in FORBIDDEN:
        if bad in text:
            return None
    try:
        return re.compile(text)
    except Exception:
        return None


def client_matches(pattern, name):
    for ch in name:
        if ord(ch) < 32:
            return False
    try:
        hit = pattern.fullmatch(name)
    except Exception:
        return False
    return hit is not None


# -------------------------------------------------------------- input layer
def input_reason(mode, size):
    """Setup reason for a stat result, or "" when the input is usable."""
    if not stat.S_ISREG(mode):
        return "unreadable"
    if size > MAX_BYTES:
        return "too_large"
    return ""


def read_path(path):
    try:
        info = os.stat(path)
    except OSError:
        return None, "unreadable"
    reason = input_reason(info.st_mode, info.st_size)
    if reason != "":
        return None, reason
    try:
        handle = open(path, "rb")
    except OSError:
        return None, "unreadable"
    try:
        data = handle.read(MAX_BYTES + 1)
    except OSError:
        return None, "unreadable"
    finally:
        handle.close()
    if len(data) > MAX_BYTES:
        return None, "too_large"
    return data, ""


def read_stdin():
    data = sys.stdin.buffer.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        return None, "too_large"
    return data, ""


# ------------------------------------------------------------------- model
def decode_clients(raw):
    """Parsed list of client objects, or (None, bad_json reason)."""
    if len(raw) == 0:
        return None, "bad_json"
    try:
        text = raw.decode("utf-8")
    except Exception:
        return None, "bad_json"
    try:
        value = json.loads(text)
    except Exception:
        return None, "bad_json"
    if not isinstance(value, list):
        return None, "bad_json"
    for element in value:
        if not isinstance(element, dict):
            return None, "bad_json"
    return value, ""


def size_pair(value):
    """(w, h) for a valid reported size, else None."""
    if not isinstance(value, list):
        return None
    if len(value) != 2:
        return None
    first = value[0]
    second = value[1]
    if not isinstance(first, int) or isinstance(first, bool):
        return None
    if not isinstance(second, int) or isinstance(second, bool):
        return None
    if first < 0 or second < 0:
        return None
    return (first, second)


def parse_client(element):
    name = element.get("class")
    if not isinstance(name, str):
        name = ""
    address = element.get("address")
    if not isinstance(address, str):
        address = "-"
    return {
        "addr": json.dumps(address, ensure_ascii=True),
        "name": name,
        "shown": json.dumps(name, ensure_ascii=True),
        "floating": element.get("floating") is True,
        "size": size_pair(element.get("size")),
    }


def size_rule(effect, args, field):
    rx_text = class_field(field)
    if rx_text is None:
        return None
    pattern = prepare_regex(rx_text)
    if pattern is None:
        return None
    want = (int(args[0]), int(args[1]))
    return {"effect": effect, "arg": str(want[0]) + "x" + str(want[1]),
            "want": want, "pattern": pattern, "text": rx_text}


def float_rule(effect, args, field):
    rx_text = class_field(field)
    if rx_text is None:
        return None
    pattern = prepare_regex(rx_text)
    if pattern is None:
        return None
    return {"effect": effect, "arg": args[0], "want": None,
            "pattern": pattern, "text": rx_text}


def shape_rule(effect, words, fields):
    if len(fields) != 2:
        return None
    if effect == "size":
        if len(words) != 3:
            return None
        if not digit_arg(words[1]):
            return None
        if not digit_arg(words[2]):
            return None
        return size_rule(effect, words[1:], fields[1])
    if len(words) != 2:
        return None
    if words[1] != "on" and words[1] != "off":
        return None
    return float_rule(effect, words[1:], fields[1])


def parse_rules(blobs):
    """-> (supported rules in order, other count, unsupported count)."""
    supported = []
    other = 0
    unsupported = 0
    index = 0
    file_no = 0
    for blob in blobs:
        file_no += 1
        text = blob.decode("utf-8", errors="replace")
        for raw in text.split("\n"):
            line = strip_blanks(raw)
            body = rule_body(line)
            if body is None:
                continue
            fields = []
            for piece in body.split(","):
                fields.append(strip_blanks(piece))
            words = tokens(fields[0])
            effect = words[0] if words else ""
            if effect != "size" and effect != "float":
                other += 1
                continue
            shaped = shape_rule(effect, words, fields)
            if shaped is None:
                unsupported += 1
                continue
            index += 1
            shaped["n"] = index
            shaped["file"] = file_no
            supported.append(shaped)
    return supported, other, unsupported


def rule_line(rule):
    return (RULE_PREFIX + "n=" + str(rule["n"]) + " file=" + str(rule["file"])
            + " effect=" + rule["effect"] + " arg=" + rule["arg"]
            + " class=" + rule["text"])


def client_line(client, verdict, want_rule, float_rule_hit):
    if client["size"] is None:
        size_text = "-"
    else:
        size_text = str(client["size"][0]) + "x" + str(client["size"][1])
    if float_rule_hit is None:
        float_text = "-"
    else:
        float_text = float_rule_hit["arg"]
    if client["floating"]:
        float_json = "true"
    else:
        float_json = "false"
    return (CLIENT_PREFIX + "addr=" + client["addr"] + " class=" + client["shown"]
            + " floating=" + float_json + " size=" + size_text
            + " want=" + want_rule["arg"] + " float_rule=" + float_text
            + " verdict=" + verdict)


def summary_line(rules_n, float_n, other, unsupported, clients, matched,
                 unmapped, agree, differ, tiled, badsize):
    if rules_n == 0:
        verdict = "NO_SIZE_RULES"
        code = 4
    elif differ > 0:
        verdict = "DIFFER"
        code = 1
    elif matched == 0:
        verdict = "NO_MATCHING_CLIENT"
        code = 3
    else:
        verdict = "OK"
        code = 0
    line = ("MADO_GEOMETRY: rules=" + str(rules_n) + " float_rules=" + str(float_n)
            + " other=" + str(other) + " unsupported=" + str(unsupported)
            + " clients=" + str(clients) + " matched=" + str(matched)
            + " unmapped=" + str(unmapped) + " agree=" + str(agree)
            + " differ=" + str(differ) + " tiled=" + str(tiled)
            + " badsize=" + str(badsize) + " verdict=" + verdict)
    return code, line


def assemble(supported, mapped, unmapped, other, unsupported):
    size_rules = []
    float_rules = []
    for rule in supported:
        if rule["effect"] == "size":
            size_rules.append(rule)
        else:
            float_rules.append(rule)
    lines = []
    for rule in supported:
        lines.append(rule_line(rule))
    agree = 0
    differ = 0
    tiled = 0
    badsize = 0
    matched = 0
    for client in mapped:
        want_rule = None
        float_rule_hit = None
        for rule in size_rules:
            if client_matches(rule["pattern"], client["name"]):
                want_rule = rule
        for rule in float_rules:
            if client_matches(rule["pattern"], client["name"]):
                float_rule_hit = rule
        if want_rule is None:
            continue
        matched += 1
        if client["size"] is None:
            verdict = "BADSIZE"
            badsize += 1
        elif not client["floating"]:
            verdict = "TILED"
            tiled += 1
        elif (client["size"][0] == want_rule["want"][0]
              and client["size"][1] == want_rule["want"][1]):
            verdict = "AGREE"
            agree += 1
        else:
            verdict = "DIFFER"
            differ += 1
        lines.append(client_line(client, verdict, want_rule, float_rule_hit))
    code, last = summary_line(len(size_rules), len(float_rules), other,
                              unsupported, len(mapped), matched, unmapped,
                              agree, differ, tiled, badsize)
    lines.append(last)
    return code, lines


# --------------------------------------------------------------------- CLI
def parse_argv(argv):
    count = len(argv)
    if count == 1 and argv[0] == "--selftest":
        return "selftest"
    clients = []
    rules = []
    i = 0
    while i < count:
        tok = argv[i]
        if tok == "--clients" or tok == "--rules":
            if i + 1 >= count:
                return None
            val = argv[i + 1]
            if tok == "--clients":
                clients.append(val)
            else:
                rules.append(val)
            i += 2
        else:
            return None
    if len(clients) != 1:
        return None
    if len(rules) < 1:
        return None
    return (clients[0], rules)


def setup(reason):
    sys.stdout.write(SETUP_PREFIX + reason + "\n")
    return 2


def emit(lines):
    sys.stdout.write("\n".join(lines) + "\n")


def pipeline(clients_raw, rule_blobs):
    """Full model run over already-read bytes: -> (code, lines)."""
    elements, reason = decode_clients(clients_raw)
    if reason != "":
        return 2, [SETUP_PREFIX + reason]
    mapped = []
    for element in elements:
        if element.get("mapped") is not False:
            mapped.append(parse_client(element))
    unmapped = len(elements) - len(mapped)
    supported, other, unsupported = parse_rules(rule_blobs)
    return assemble(supported, mapped, unmapped, other, unsupported)


# ----------------------------------------------------------------- selftest
def selftest(checks):
    def same(got, want):
        checks.append((got == want, got, want))

    def run(clients_text, rule_texts):
        blobs = []
        for text in rule_texts:
            blobs.append(text.encode("utf-8"))
        return pipeline(clients_text.encode("utf-8"), blobs)

    # argv
    same(parse_argv([]), None)
    same(parse_argv(["--selftest"]), "selftest")
    same(parse_argv(["--selftest", "x"]), None)
    same(parse_argv(["--clients", "-"]), None)
    same(parse_argv(["--rules", "a", "--clients", "-"]), ("-", ["a"]))
    same(parse_argv(["--rules", "a", "--rules", "b", "--clients", "c"]),
         ("c", ["a", "b"]))
    same(parse_argv(["--clients=-", "--rules", "a"]), None)
    same(parse_argv(["--clients", "-", "--clients", "-", "--rules", "a"]), None)
    same(parse_argv(["--clients"]), None)
    same(parse_argv(["--rules", "a", "--clients"]), None)
    same(parse_argv(["--rules"]), None)

    # input classification
    same(input_reason(stat.S_IFREG | 0o644, 0), "")
    same(input_reason(stat.S_IFREG | 0o644, MAX_BYTES), "")
    same(input_reason(stat.S_IFREG | 0o644, MAX_BYTES + 1), "too_large")
    same(input_reason(stat.S_IFDIR | 0o755, 0), "unreadable")
    same(input_reason(stat.S_IFIFO | 0o644, 0), "unreadable")
    same(input_reason(stat.S_IFLNK | 0o777, 0), "unreadable")

    # tokens and rule line shape
    same(tokens(""), [])
    same(tokens(" \t "), [])
    same(tokens("size  420\t500"), ["size", "420", "500"])
    same(rule_body("windowrule = size 1 2"), " size 1 2")
    same(rule_body("windowrule=size 1 2"), "size 1 2")
    same(rule_body("windowrule \t = x"), " x")
    same(rule_body("windowrulev2 = size 1 2, match:class a"), None)
    same(rule_body("WindowRule = size 1 2"), None)
    same(rule_body(" windowrule = size 1 2"), None)
    same(rule_body("windowrule"), None)
    same(rule_body("windowrule "), None)
    same(rule_body("windowrule\t= x"), " x")

    # class field
    same(class_field("match:class ^a$"), "^a$")
    same(class_field("match:class\t^a$"), "^a$")
    same(class_field("match:class  ^a$"), "^a$")
    same(class_field("match:class"), None)
    same(class_field("match:class "), None)
    same(class_field("match:classes ^a$"), None)
    same(class_field("match:class ^a$,x"), "^a$,x")

    # numeric arguments
    same(digit_arg("0"), True)
    same(digit_arg("00000"), True)
    same(digit_arg("000000"), False)
    same(digit_arg(""), False)
    same(digit_arg("12a"), False)
    same(digit_arg("-1"), False)

    # regex alphabet and compilation
    same(charset_ok("^(org.omarchy.gkeep)$"), True)
    same(charset_ok(""), False)
    same(charset_ok("a" * 200), True)
    same(charset_ok("a" * 201), False)
    same(charset_ok("a b"), False)
    same(charset_ok("a\\d"), False)
    same(charset_ok("a\\"), False)
    same(charset_ok("a\\.b"), True)
    same(charset_ok("a\\-b"), True)
    same(charset_ok("a\\\\b"), True)
    same(prepare_regex("^(org.omarchy.gkeep)$") is None, False)
    same(prepare_regex("a(?i)b") is None, True)
    same(prepare_regex("a*+") is None, True)
    same(prepare_regex("a++") is None, True)
    same(prepare_regex("a?+") is None, True)
    same(prepare_regex("(") is None, True)
    same(prepare_regex("a**") is None, True)
    same(prepare_regex("a\\q") is None, True)

    # size and matching primitives
    same(size_pair([420, 500]), (420, 500))
    same(size_pair([0, 0]), (0, 0))
    same(size_pair([420]), None)
    same(size_pair([420, 500, 1]), None)
    same(size_pair([True, 500]), None)
    same(size_pair([420.0, 500]), None)
    same(size_pair([-1, 500]), None)
    same(size_pair("420x500"), None)
    same(size_pair(None), None)
    pattern = prepare_regex("^(a.c)$")
    same(client_matches(pattern, "abc"), True)
    same(client_matches(pattern, "ABC"), False)
    same(client_matches(pattern, "abc\x01"), False)
    same(client_matches(prepare_regex(".*"), "abc"), True)

    # clients decoding
    same(decode_clients(b"")[1], "bad_json")
    same(decode_clients(b"{")[1], "bad_json")
    same(decode_clients(b"{}")[1], "bad_json")
    same(decode_clients(b"[1]")[1], "bad_json")
    same(decode_clients(b"[[]]")[1], "bad_json")
    same(decode_clients(b"\xff")[1], "bad_json")
    same(decode_clients(b"[]")[0], [])
    same(decode_clients(b'[{"a":1,"a":2}]')[0], [{"a": 2}])
    same(decode_clients(b'[{"size":[NaN,1]}]')[1], "")
    same(size_pair(decode_clients(b'[{"size":[NaN,1]}]')[0][0]["size"]), None)

    # rule parsing counters
    text_one = "windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$"
    supported, other, unsupported = parse_rules([text_one.encode("utf-8")])
    same(len(supported), 1)
    same(other, 0)
    same(unsupported, 0)
    same(supported[0]["arg"], "420x500")
    same(supported[0]["file"], 1)
    same(supported[0]["n"], 1)
    supported, other, unsupported = parse_rules(
        [b"windowrule = center, match:class ^(a)$\n"
         b"windowrulev2 = size 1 2, match:class ^(a)$\n"
         b"WindowRule = size 1 2, match:class ^(a)$\n"
         b"windowrule = bind, match:class ^(a)$"])
    same((len(supported), other, unsupported), (0, 2, 0))
    supported, other, unsupported = parse_rules(
        [b"windowrule = size 1 2, match:class ^(a)$\n"
         b"windowrule = size 1 2 3, match:class ^(a)$\n"
         b"windowrule = size 123456 2, match:class ^(a)$\n"
         b"windowrule = size 1 2\n"
         b"windowrule = size 1 2, match:class ^(a)$, x\n"
         b"windowrule = size 1 2, match:class ^(a\n"
         b"windowrule = float on off, match:class ^(a)$\n"
         b"windowrule = float off, match:class ^(a)$"])
    same((len(supported), other, unsupported), (2, 0, 6))
    same(supported[1]["arg"], "off")
    supported, other, unsupported = parse_rules(
        [b"windowrule = size 0042 0500, match:class ^(a)$",
         b"windowrule = float on, match:class ^(b)$"])
    same(supported[0]["arg"], "42x500")
    same(supported[0]["file"], 1)
    same(supported[1]["file"], 2)
    same(supported[1]["n"], 2)

    # rendering and verdicts
    same(rule_line({"n": 1, "file": 1, "effect": "size", "arg": "420x500",
                    "text": "^(a)$"}),
         "MADO_GEOM_RULE: n=1 file=1 effect=size arg=420x500 class=^(a)$")
    same(summary_line(0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0),
         (4, "MADO_GEOMETRY: rules=0 float_rules=2 other=0 unsupported=0 "
             "clients=0 matched=0 unmapped=0 agree=0 differ=0 tiled=0 "
             "badsize=0 verdict=NO_SIZE_RULES"))
    same(summary_line(1, 0, 0, 0, 3, 2, 1, 0, 2, 0, 0),
         (1, "MADO_GEOMETRY: rules=1 float_rules=0 other=0 unsupported=0 "
             "clients=3 matched=2 unmapped=1 agree=0 differ=2 tiled=0 "
             "badsize=0 verdict=DIFFER"))
    same(summary_line(1, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0),
         (3, "MADO_GEOMETRY: rules=1 float_rules=1 other=2 unsupported=3 "
             "clients=0 matched=0 unmapped=0 agree=0 differ=0 tiled=0 "
             "badsize=0 verdict=NO_MATCHING_CLIENT"))
    same(summary_line(1, 1, 0, 0, 2, 1, 1, 1, 0, 0, 0),
         (0, "MADO_GEOMETRY: rules=1 float_rules=1 other=0 unsupported=0 "
             "clients=2 matched=1 unmapped=1 agree=1 differ=0 tiled=0 "
             "badsize=0 verdict=OK"))

    # end-to-end: rules only, no client
    code, lines = run("[]", [text_one])
    same(code, 3)
    same(len(lines), 2)
    same(lines[0], "MADO_GEOM_RULE: n=1 file=1 effect=size arg=420x500 "
                   "class=^(org.omarchy.gkeep)$")
    same(lines[1], "MADO_GEOMETRY: rules=1 float_rules=0 other=0 "
                   "unsupported=0 clients=0 matched=0 unmapped=0 agree=0 "
                   "differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT")

    # end-to-end: agree
    clients = ('[{"class":"org.omarchy.gkeep","mapped":true,"floating":true,'
               '"size":[420,500],"address":"0xabc"}]')
    code, lines = run(clients, [text_one])
    same(code, 0)
    same(lines[1], 'MADO_GEOM_CLIENT: addr="0xabc" '
                   'class="org.omarchy.gkeep" floating=true size=420x500 '
                   'want=420x500 float_rule=- verdict=AGREE')
    same(lines[2], "MADO_GEOMETRY: rules=1 float_rules=0 other=0 "
                   "unsupported=0 clients=1 matched=1 unmapped=0 agree=1 "
                   "differ=0 tiled=0 badsize=0 verdict=OK")

    # end-to-end: differ
    clients = ('[{"class":"org.omarchy.gkeep","mapped":true,"floating":true,'
               '"size":[421,500]}]')
    code, lines = run(clients, [text_one])
    same(code, 1)
    same(lines[1], 'MADO_GEOM_CLIENT: addr="-" class="org.omarchy.gkeep" '
                   'floating=true size=421x500 want=420x500 float_rule=- '
                   'verdict=DIFFER')

    # end-to-end: tiled
    clients = ('[{"class":"org.omarchy.gkeep","mapped":true,"floating":false,'
               '"size":[420,500]}]')
    code, lines = run(clients, [text_one])
    same(code, 0)
    same(lines[1], 'MADO_GEOM_CLIENT: addr="-" class="org.omarchy.gkeep" '
                   'floating=false size=420x500 want=420x500 float_rule=- '
                   'verdict=TILED')

    # end-to-end: badsize
    clients = ('[{"class":"org.omarchy.gkeep","mapped":true,"floating":true,'
               '"size":[420]}]')
    code, lines = run(clients, [text_one])
    same(code, 0)
    same(lines[1], 'MADO_GEOM_CLIENT: addr="-" class="org.omarchy.gkeep" '
                   'floating=true size=- want=420x500 float_rule=- '
                   'verdict=BADSIZE')

    # end-to-end: unmapped skipped, float rule reported
    rules = [text_one, "windowrule = float on, match:class ^(org.*)$"]
    clients = ('[{"class":"org.omarchy.gkeep","mapped":false,"size":[1,1]},'
               '{"class":"org.omarchy.gkeep","mapped":0,"floating":true,'
               '"size":[420,500]}]')
    code, lines = run(clients, rules)
    same(code, 0)
    same(len(lines), 4)
    same(lines[2], 'MADO_GEOM_CLIENT: addr="-" class="org.omarchy.gkeep" '
                   'floating=true size=420x500 want=420x500 float_rule=on '
                   'verdict=AGREE')
    same(lines[3], "MADO_GEOMETRY: rules=1 float_rules=1 other=0 "
                   "unsupported=0 clients=1 matched=1 unmapped=1 agree=1 "
                   "differ=0 tiled=0 badsize=0 verdict=OK")

    # end-to-end: last matching rule wins
    rules = ["windowrule = size 10 10, match:class ^(a.*)$",
             "windowrule = size 20 20, match:class ^(ab)$",
             "windowrule = float off, match:class ^(a)$",
             "windowrule = float on, match:class ^(ab)$"]
    clients = '[{"class":"ab","mapped":true,"floating":true,"size":[20,20]}]'
    code, lines = run(clients, rules)
    same(code, 0)
    same(len(lines), 6)
    same(lines[2], "MADO_GEOM_RULE: n=3 file=3 effect=float arg=off "
                   "class=^(a)$")
    same(lines[4], 'MADO_GEOM_CLIENT: addr="-" class="ab" floating=true '
                   'size=20x20 want=20x20 float_rule=on verdict=AGREE')

    # end-to-end: float-only rules
    rules = ["windowrule = float on, match:class ^(a)$"]
    clients = '[{"class":"a","mapped":true,"floating":true,"size":[1,1]}]'
    code, lines = run(clients, rules)
    same(code, 4)
    same(lines[1], "MADO_GEOMETRY: rules=0 float_rules=1 other=0 "
                   "unsupported=0 clients=1 matched=0 unmapped=0 agree=0 "
                   "differ=0 tiled=0 badsize=0 verdict=NO_SIZE_RULES")

    # end-to-end: control character in class blocks the match
    clients = ('[{"class":"org.omarchy.gkeep\\u0001","mapped":true,'
               '"floating":true,"size":[420,500]}]')
    code, lines = run(clients, [text_one])
    same(code, 3)
    same(len(lines), 2)

    # end-to-end: non-ASCII class is JSON-escaped
    clients = '[{"class":"\\u00e9","mapped":true,"floating":true,"size":[1,1]}]'
    code, lines = run(clients, ["windowrule = size 1 1, match:class ^(.*)$"])
    same(code, 0)
    same(lines[1], 'MADO_GEOM_CLIENT: addr="-" class="\\u00e9" '
                   'floating=true size=1x1 want=1x1 float_rule=- verdict=AGREE')

    # end-to-end: unreadable class values
    clients = ('[{"class":7,"mapped":true,"floating":null,"size":[1,1],'
               '"address":5}]')
    code, lines = run(clients, ["windowrule = size 1 1, match:class ^()$"])
    same(code, 0)
    same(lines[1], 'MADO_GEOM_CLIENT: addr="-" class="" floating=false '
                   'size=1x1 want=1x1 float_rule=- verdict=TILED')

    # end-to-end: bad clients input
    code, lines = run("{}", [text_one])
    same(code, 2)
    same(lines, ["MADO_GEOMETRY: SETUP bad_json"])

    # end-to-end: comment and blank lines are ignored
    rules = ["# windowrule = size 1 1, match:class ^(a)$\n"
             "\n"
             "  windowrule = size 2 2, match:class ^(a)$  "]
    code, lines = run('[{"class":"a","mapped":true,"floating":true,'
                      '"size":[2,2]}]', rules)
    same(code, 0)
    same(len(lines), 3)
    same(lines[0], "MADO_GEOM_RULE: n=1 file=1 effect=size arg=2x2 "
                   "class=^(a)$")


def selftest_entry():
    checks = []
    selftest(checks)
    total = len(checks)
    passed = 0
    for index in range(len(checks)):
        state = checks[index]
        if state[0]:
            passed += 1
        else:
            sys.stderr.write("selftest check " + str(index) + " failed: got "
                             + repr(state[1]) + " want " + repr(state[2])
                             + "\n")
    sys.stdout.write(SELFTEST_PREFIX + str(passed) + "/" + str(total)
                     + " passed\n")
    if passed != total:
        return 1
    return 0


def main(argv):
    choice = parse_argv(argv)
    if choice is None:
        return setup("usage")
    if choice == "selftest":
        return selftest_entry()
    clients_spec = choice[0]
    rule_specs = choice[1]
    if clients_spec == "-":
        raw, reason = read_stdin()
    else:
        raw, reason = read_path(clients_spec)
    if reason != "":
        return setup(reason)
    blobs = []
    for spec in rule_specs:
        blob, reason = read_path(spec)
        if reason != "":
            return setup(reason)
        blobs.append(blob)
    code, lines = pipeline(raw, blobs)
    emit(lines)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
