#!/usr/bin/env python3
"""mado-geometry.py - a read-only join of window-rule sizes against one `hyprctl clients -j` dump.

The tool is write-only to stdout and never talks to the compositor. Two passes:
every supported rule of the given configuration files is collected first (files in
argument order, lines in file order), then the single clients dump is streamed once
and each client is judged against that ordered rule list.

  mado-geometry.py --selftest
  hyprctl clients -j | mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf

A RULE LINE is `windowrule = size W H, match:class REGEX` or
`windowrule = float on|off, match:class REGEX`. Rules apply in file order; for a
client whose class is matched, the last matching size rule gives the wanted box
and the last matching float rule gives the wanted float state. A matched client is
AGREE, DIFFER, TILED (not floating) or BADSIZE (no usable reported size).

Output (stdout, one line each):
  MADO_GEOM_RULE: ...      one per supported rule, in rule order
  MADO_GEOM_CLIENT: ...    one per matched client, in input order
  MADO_GEOMETRY: ...       the tally and the verdict, always last

A setup failure prints exactly `MADO_GEOMETRY: SETUP <reason>` and exits 2, with
reason one of usage, unreadable, too_large, bad_json. The verdict is NO_SIZE_RULES
(exit 4), DIFFER (exit 1), NO_MATCHING_CLIENT (exit 3) or OK (exit 0).
"""
import json
import os
import re
import stat
import sys

MAX_BYTES = 1048576
MAX_REGEX_TOKENS = 200
CONTROL_LIMIT = 32
SAFE_LITERALS = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.^$()|*+?-")
SAFE_ESCAPES = frozenset(".-()|*+?^$\\")
FORBIDDEN = ("(?", "*+", "++", "?+")
WORD_RE = re.compile("[ \t]+")
RULE_RE = re.compile("windowrule[ \t]*=(.*)")
MATCH_RE = re.compile("match:class[ \t]+(.+)")
NUM_RE = re.compile("[0-9]{1,5}")


# ------------------------------------------------------------------ inputs
def too_big(count):
    """True when a byte count exceeds what the tool accepts at all."""
    return count > MAX_BYTES


def read_stream(stream):
    """Read a stream without trusting its length; one byte past the cap is enough."""
    data = stream.read(MAX_BYTES + 1)
    if too_big(len(data)):
        return None, "too_large"
    return data, None


def read_path(path):
    """Read a regular file only; a FIFO or a device must return, never block."""
    try:
        info = os.stat(path)
    except OSError:
        return None, "unreadable"
    if not stat.S_ISREG(info.st_mode):
        return None, "unreadable"
    if too_big(info.st_size):
        return None, "too_large"
    try:
        handle = open(path, "rb")
    except OSError:
        return None, "unreadable"
    try:
        data = handle.read(MAX_BYTES + 1)
    finally:
        handle.close()
    return data, None


def load_source(path, stdin_ok, stream):
    """`-` is stdin for the clients dump and a plain (missing) path for a rules file."""
    if path == "-":
        if stdin_ok:
            return read_stream(stream)
        return None, "unreadable"
    return read_path(path)


def parse_args(argv):
    """Two-token forms only, any order; exactly one --clients, at least one --rules."""
    clients = None
    rules = []
    want_selftest = False
    total = len(argv)
    index = 0
    while index < total:
        word = argv[index]
        if word == "--selftest":
            want_selftest = True
            index += 1
        elif word == "--clients":
            if clients is not None:
                return None
            if index + 1 >= total:
                return None
            clients = argv[index + 1]
            index += 2
        elif word == "--rules":
            if index + 1 >= total:
                return None
            rules.append(argv[index + 1])
            index += 2
        else:
            return None
    if want_selftest:
        if clients is not None or rules:
            return None
        return {"selftest": True, "clients": None, "rules": []}
    if clients is None or not rules:
        return None
    return {"selftest": False, "clients": clients, "rules": rules}


def parse_clients(data):
    """A JSON array of objects, or None (bad_json). Duplicate keys keep the last value."""
    try:
        document = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    if not isinstance(document, list):
        return None
    for item in document:
        if not isinstance(item, dict):
            return None
    return document


# ------------------------------------------------------------- rule pass
def is_safe_regex(text):
    """The restricted alphabet (1..200 tokens) where Python `re` and RE2 agree."""
    tokens = 0
    index = 0
    total = len(text)
    while index < total:
        char = text[index]
        if char in SAFE_LITERALS:
            tokens += 1
            index += 1
        elif char == "\\":
            if index + 1 >= total:
                return False
            if text[index + 1] not in SAFE_ESCAPES:
                return False
            tokens += 1
            index += 2
        else:
            return False
    if len(text) < 1:
        return False
    if len(text) > MAX_REGEX_TOKENS:
        return False
    for forbidden in FORBIDDEN:
        if forbidden in text:
            return False
    try:
        re.compile(text)
    except re.error:
        return False
    return True


def collect(texts):
    """First pass: (rules, other, unsupported); a rule is (file, effect, arg, want, rx, pattern)."""
    rules = []
    other = 0
    unsupported = 0
    for file_number, text in enumerate(texts, 1):
        for raw in text.split("\n"):
            line = raw.strip(" \t")
            found = RULE_RE.fullmatch(line)
            if found is None:
                continue
            fields = [part.strip(" \t") for part in found.group(1).split(",")]
            words = [word for word in WORD_RE.split(fields[0]) if word]
            effect = words[0] if words else ""
            if effect not in ("size", "float"):
                other += 1
                continue
            arguments = words[1:]
            if len(fields) != 2:
                unsupported += 1
                continue
            if effect == "size":
                if len(arguments) != 2:
                    unsupported += 1
                    continue
                if not (NUM_RE.fullmatch(arguments[0]) and
                        NUM_RE.fullmatch(arguments[1])):
                    unsupported += 1
                    continue
                want = (int(arguments[0]), int(arguments[1]))
                shown = "%dx%d" % want
            else:
                if len(arguments) != 1 or arguments[0] not in ("on", "off"):
                    unsupported += 1
                    continue
                want = arguments[0]
                shown = arguments[0]
            matcher = MATCH_RE.fullmatch(fields[1])
            if matcher is None:
                unsupported += 1
                continue
            regex = matcher.group(1)
            if not is_safe_regex(regex):
                unsupported += 1
                continue
            rules.append((file_number, effect, shown, want, regex,
                          re.compile(regex)))
    return rules, other, unsupported


def render_rules(rules):
    lines = []
    for number, rule in enumerate(rules, 1):
        lines.append("MADO_GEOM_RULE: n=%d file=%d effect=%s arg=%s class=%s"
                     % (number, rule[0], rule[1], rule[2], rule[4]))
    return lines


# ----------------------------------------------------------- client pass
def has_control(text):
    """True when a class holds a character below U+0020 (such a class matches nothing)."""
    for char in text:
        if ord(char) < CONTROL_LIMIT:
            return True
    return False


def evaluate(document, rules):
    """Second pass: stream the dump once; return (client lines, tallies)."""
    lines = []
    tallies = {"clients": 0, "matched": 0, "unmapped": 0,
               "AGREE": 0, "DIFFER": 0, "TILED": 0, "BADSIZE": 0}
    for client in document:
        if client.get("mapped") is False:
            tallies["unmapped"] += 1
            continue
        tallies["clients"] += 1
        client_class = client.get("class")
        if not isinstance(client_class, str):
            client_class = ""
        want = None
        float_rule = "-"
        if has_control(client_class) is False:
            for rule in rules:
                if rule[5].fullmatch(client_class) is not None:
                    if rule[1] == "size":
                        want = rule[3]
                    else:
                        float_rule = rule[3]
        if want is None:
            continue
        tallies["matched"] += 1
        reported = client.get("size")
        size = None
        if isinstance(reported, list) and len(reported) == 2:
            if type(reported[0]) is int and type(reported[1]) is int:
                if reported[0] >= 0 and reported[1] >= 0:
                    size = (reported[0], reported[1])
        floating = client.get("floating") is True
        if size is None:
            verdict = "BADSIZE"
        elif floating is False:
            verdict = "TILED"
        elif size == want:
            verdict = "AGREE"
        else:
            verdict = "DIFFER"
        tallies[verdict] += 1
        address = client.get("address")
        if not isinstance(address, str):
            address = "-"
        lines.append(
            "MADO_GEOM_CLIENT: addr=%s class=%s floating=%s size=%s "
            "want=%dx%d float_rule=%s verdict=%s"
            % (json.dumps(address), json.dumps(client_class),
               "true" if floating else "false",
               ("%dx%d" % size) if size is not None else "-",
               want[0], want[1], float_rule, verdict))
    return lines, tallies


def summarize(size_rules, float_rules, other, unsupported, tallies):
    if size_rules == 0:
        verdict, code = "NO_SIZE_RULES", 4
    elif tallies["DIFFER"] > 0:
        verdict, code = "DIFFER", 1
    elif tallies["matched"] == 0:
        verdict, code = "NO_MATCHING_CLIENT", 3
    else:
        verdict, code = "OK", 0
    return ("MADO_GEOMETRY: rules=%d float_rules=%d other=%d unsupported=%d "
            "clients=%d matched=%d unmapped=%d agree=%d differ=%d tiled=%d "
            "badsize=%d verdict=%s"
            % (size_rules, float_rules, other, unsupported, tallies["clients"],
               tallies["matched"], tallies["unmapped"], tallies["AGREE"],
               tallies["DIFFER"], tallies["TILED"], tallies["BADSIZE"],
               verdict)), code


def compute(document, texts):
    """Both passes over already-validated inputs."""
    rules, other, unsupported = collect(texts)
    size_rules = 0
    for rule in rules:
        if rule[1] == "size":
            size_rules += 1
    lines = render_rules(rules)
    client_lines, tallies = evaluate(document, rules)
    summary, code = summarize(size_rules, len(rules) - size_rules, other,
                             unsupported, tallies)
    return lines + client_lines + [summary], code


# ------------------------------------------------------------------ driver
def emit(lines, code):
    sys.stdout.write("\n".join(lines) + "\n")
    return code


def selftest():
    results = []

    def check(label, got, want):
        results.append((label, got == want, got, want))

    def fails(label):
        results.append((label, False, "skipped", "ran"))

    # ---- restricted regex alphabet
    for text, want in [("a", True), ("^(org.omarchy.gkeep)$", True),
                       ("a" * 200, True), ("a" * 201, False), ("", False),
                       ("\\.\\-\\(\\)", True), ("a\\", False), ("\\a", False),
                       ("a{2}", False), ("[ab]", False), ("(?i)a", False),
                       ("a++", False), ("a*+", False), ("a**", False),
                       ("a+?", True), ("a*?", True), ("a??", True),
                       ("?", False), ("a|", True), ("|a", True),
                       ("(()))", False), ("a\u00fc", False), ("a b", False),
                       ("k.*y", True), ("^$", True), ("(x y)?", False)]:
        check("regex " + text[:12], is_safe_regex(text), want)

    # ---- argument forms
    good = {"selftest": False, "clients": "c", "rules": ["r"]}
    check("args ok", parse_args(["--clients", "c", "--rules", "r"]), good)
    check("args ok reversed",
          parse_args(["--rules", "r", "--clients", "c"]), good)
    check("args two rules",
          parse_args(["--clients", "c", "--rules", "a", "--rules", "b"]),
          {"selftest": False, "clients": "c", "rules": ["a", "b"]})
    check("args selftest", parse_args(["--selftest"]),
          {"selftest": True, "clients": None, "rules": []})
    for form in [[], ["--clients", "c"], ["--rules", "r"],
                 ["--clients", "c", "--clients", "c", "--rules", "r"],
                 ["--clients", "c", "--rules", "r", "--extra"],
                 ["--clients", "c", "--rules"], ["--client", "c", "--rules", "r"],
                 ["--clients=c", "--rules", "r"],
                 ["--selftest", "--clients", "c", "--rules", "r"],
                 ["--rules", "r", "--clients", "c", "x"], ["--help"]]:
        check("args reject " + " ".join(form), parse_args(form), None)

    # ---- size caps and non-regular inputs
    check("too_big max", too_big(MAX_BYTES), False)
    check("too_big max+1", too_big(MAX_BYTES + 1), True)

    class Source:
        def __init__(self, blob):
            self.blob = blob

        def read(self, count):
            return self.blob[:count]

    check("stream small", read_stream(Source(b"[]")), (b"[]", None))
    check("stream at cap", read_stream(Source(b"x" * MAX_BYTES)),
          (b"x" * MAX_BYTES, None))
    check("stream over cap", read_stream(Source(b"x" * (MAX_BYTES + 1))),
          (None, "too_large"))
    check("load dash stdin", load_source("-", True, Source(b"[1]")), (b"[1]", None))
    check("load dash rules", load_source("-", False, None), (None, "unreadable"))
    # read a regular file for real when this copy sits in the working directory
    here = os.path.join(os.getcwd(), "mado-geometry.py")
    blob, reason = read_path(here)
    if reason is None:
        check("read own source nonempty", bool(blob), True)
    else:
        check("read absent source", reason, "unreadable")
    check("read missing", read_path(os.path.join(os.getcwd(), "absent.json")),
          (None, "unreadable"))
    check("read directory", read_path(os.getcwd()), (None, "unreadable"))

    # ---- clients input shapes
    for raw, want in [("{}", None), ("[1]", None), ("", None), ("[", None),
                      ("null", None), ('"[]"', None), ("[{}, 3]", None),
                      ("[[]]", None), ("[] x", None), ("[]", [])]:
        check("clients " + raw, parse_clients(raw.encode("utf-8")), want)
    check("clients bad utf8", parse_clients(b"\xff[]"), None)
    check("clients dupkeys",
          parse_clients(b'[{"class":"z","class":"a"}]'), [{"class": "a"}])

    # ---- control characters in a class
    check("control tab", has_control("a\tb"), True)
    check("control del", has_control("a\x7fb"), False)
    check("control none", has_control("Alacritty"), False)

    # ---- rule collection
    texts = [
        "windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$\n"
        "windowrule = float on, match:class ^(org.omarchy.gkeep)$\n"
        "windowrulev2 = size 1 2, class:a\n",
        "# nothing\nwindowrule = size 1 2, match:class a\n",
    ]
    rules, other, unsupported = collect(texts)
    check("collect count", len(rules), 3)
    check("collect other", other, 0)
    check("collect unsupported", unsupported, 0)
    check("collect file numbers", [rule[0] for rule in rules], [1, 1, 2])
    check("collect effects", [rule[1] for rule in rules],
          ["size", "float", "size"])
    check("collect args", [rule[2] for rule in rules], ["420x500", "on", "1x2"])
    check("collect want", [rule[3] for rule in rules],
          [(420, 500), "on", (1, 2)])
    check("collect regex", rules[0][4], "^(org.omarchy.gkeep)$")

    # ---- one joined verdict end to end
    document = parse_clients(
        b'[{"class":"org.omarchy.gkeep","size":[420,500],'
        b'"floating":true,"address":"0x1"}]')
    lines, code = compute(document, texts)
    check("join code", code, 0)
    check("join lines", len(lines), 5)
    check("join first", lines[0],
          "MADO_GEOM_RULE: n=1 file=1 effect=size arg=420x500 "
          "class=^(org.omarchy.gkeep)$")
    check("join client", lines[3],
          'MADO_GEOM_CLIENT: addr="0x1" class="org.omarchy.gkeep" '
          'floating=true size=420x500 want=420x500 float_rule=on verdict=AGREE')
    check("join summary", lines[4],
          "MADO_GEOMETRY: rules=2 float_rules=1 other=0 unsupported=0 "
          "clients=1 matched=1 unmapped=0 agree=1 differ=0 tiled=0 badsize=0 "
          "verdict=OK")

    # ---- verdict branches
    def one(document_json, rule_text):
        document = parse_clients(document_json.encode("utf-8"))
        return compute(document, [rule_text])

    lines, code = one('[{"class":"a","size":[5,7],"floating":true}]',
                      "windowrule = size 5 6, match:class a\n")
    check("differ code", code, 1)
    check("differ summary", lines[2],
          "MADO_GEOMETRY: rules=1 float_rules=0 other=0 unsupported=0 "
          "clients=1 matched=1 unmapped=0 agree=0 differ=1 tiled=0 badsize=0 "
          "verdict=DIFFER")
    lines, code = one('[{"class":"a","size":[5,6],"floating":false}]',
                      "windowrule = size 5 6, match:class a\n")
    check("tiled code", code, 0)
    check("tiled client", lines[1],
          'MADO_GEOM_CLIENT: addr="-" class="a" floating=false size=5x6 '
          'want=5x6 float_rule=- verdict=TILED')
    lines, code = one('[{"class":"a","size":[5,6],"floating":true}]',
                      "windowrule = size 5 6, match:class a\n")
    check("agree code", code, 0)
    lines, code = one('[{"class":"a","size":[1,2,3],"floating":true}]',
                      "windowrule = size 5 6, match:class a\n")
    check("badsize", lines[1],
          'MADO_GEOM_CLIENT: addr="-" class="a" floating=true size=- '
          'want=5x6 float_rule=- verdict=BADSIZE')
    lines, code = one('[{"class":"b","size":[5,6],"floating":true}]',
                      "windowrule = size 5 6, match:class a\n")
    check("no match code", code, 3)
    check("no match summary", lines[1],
          "MADO_GEOMETRY: rules=1 float_rules=0 other=0 unsupported=0 "
          "clients=1 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 "
          "verdict=NO_MATCHING_CLIENT")
    lines, code = one('[{"class":"a","size":[5,6],"floating":true}]',
                      "windowrule = float on, match:class a\n")
    check("no size code", code, 4)
    check("no size summary", lines[1],
          "MADO_GEOMETRY: rules=0 float_rules=1 other=0 unsupported=0 "
          "clients=1 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 "
          "verdict=NO_SIZE_RULES")

    # ---- last rule wins, per effect
    document = parse_clients(
        b'[{"class":"a","size":[3,3],"floating":true}]')
    lines, code = compute(document, [
        "windowrule = size 1 1, match:class .*\n"
        "windowrule = float off, match:class .*\n",
        "windowrule = size 3 3, match:class a\n"
        "windowrule = float on, match:class a\n"])
    check("order code", code, 0)
    check("order client", lines[4],
          'MADO_GEOM_CLIENT: addr="-" class="a" floating=true size=3x3 '
          'want=3x3 float_rule=on verdict=AGREE')

    # ---- unmapped, control class, non-string values
    document = parse_clients(
        b'[{"class":"a","size":[1,2],"floating":true,"mapped":false},'
        b'{"class":"a\\u0009b","size":[1,2],"floating":true},'
        b'{"class":"a","size":[1,2],"floating":1}]')
    lines, code = compute(document, ["windowrule = size 1 2, match:class a.b\n"])
    check("odd classes code", code, 3)
    check("odd classes summary", lines[1],
          "MADO_GEOMETRY: rules=1 float_rules=0 other=0 unsupported=0 "
          "clients=2 matched=0 unmapped=1 agree=0 differ=0 tiled=0 badsize=0 "
          "verdict=NO_MATCHING_CLIENT")
    document = parse_clients(
        b'[{"class":"a","size":[1,2],"floating":1}]')
    lines, code = compute(document, ["windowrule = size 1 2, match:class a\n"])
    check("float not true", lines[1],
          'MADO_GEOM_CLIENT: addr="-" class="a" floating=false size=1x2 '
          'want=1x2 float_rule=- verdict=TILED')

    # ---- summarize directly
    empty = {"clients": 0, "matched": 0, "unmapped": 0, "AGREE": 0,
             "DIFFER": 0, "TILED": 0, "BADSIZE": 0}
    check("summarize no rules", summarize(0, 0, 0, 0, empty)[1], 4)
    check("summarize no match", summarize(1, 0, 0, 0, empty)[1], 3)
    agree = dict(empty)
    agree["clients"] = 1
    agree["matched"] = 1
    agree["AGREE"] = 1
    check("summarize ok", summarize(1, 0, 0, 0, agree)[1], 0)
    differ = dict(agree)
    differ["DIFFER"] = 1
    check("summarize differ", summarize(1, 0, 0, 0, differ)[1], 1)
    check("summarize counts", summarize(2, 1, 3, 4, agree)[0],
          "MADO_GEOMETRY: rules=2 float_rules=1 other=3 unsupported=4 "
          "clients=1 matched=1 unmapped=0 agree=1 differ=0 tiled=0 badsize=0 "
          "verdict=OK")
    check("summarize no rules text", summarize(0, 1, 0, 0, empty)[0],
          "MADO_GEOMETRY: rules=0 float_rules=1 other=0 unsupported=0 "
          "clients=0 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 "
          "verdict=NO_SIZE_RULES")

    passed = 0
    for label, ok, got, want in results:
        if ok:
            passed += 1
    total = len(results)
    print("MADO_GEOMETRY_SELFTEST: %d/%d passed" % (passed, total))
    for label, ok, got, want in results:
        if not ok:
            print("MADO_GEOMETRY_SELFTEST_FAIL: %s got=%r want=%r"
                  % (label, got, want))
    return 0 if passed == total else 1


def main(argv):
    options = parse_args(argv)
    if options is None:
        return emit(["MADO_GEOMETRY: SETUP usage"], 2)
    if options["selftest"]:
        return selftest()
    data, reason = load_source(options["clients"], True, sys.stdin.buffer)
    if data is None:
        return emit(["MADO_GEOMETRY: SETUP " + reason], 2)
    document = parse_clients(data)
    if document is None:
        return emit(["MADO_GEOMETRY: SETUP bad_json"], 2)
    texts = []
    for path in options["rules"]:
        blob, why = load_source(path, False, None)
        if blob is None:
            return emit(["MADO_GEOMETRY: SETUP " + why], 2)
        texts.append(blob.decode("utf-8", "replace"))
    lines, code = compute(document, texts)
    return emit(lines, code)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
