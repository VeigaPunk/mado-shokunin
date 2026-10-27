#!/usr/bin/env python3
"""Builder for the ExecControlsC1 cheat controls (seat-local; the emitted files are the deliverable).

The table-using controls must carry their answers *inside the tool file*: the counter's sandbox binds no data file,
so a sidecar JSON would be invisible and the control would fail for the wrong reason (clause f instead of the clause
under test). This builder therefore embeds the (keymap sha256, keysym) -> (rc, stdout) table produced by make-cases.py.

Every emitted control keeps the scoreable CLI: `how-to-type --keymap FILE --disable-compose --keysym ARG` and
`--selftest`.

Usage: build-controls.py --cases cases.json --out controls/
"""
import argparse
import json
import os
import re
import sys

COMMON = '''#!/usr/bin/env python3
"""control __NAME__ - CHEAT: __SUMMARY__

Stops at: __STOP__

__NOTE__
"""
import hashlib
import json
import re
import sys

__IMPORTS__
TABLE = __TABLE__


def keymap_sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse(argv):
    o = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--keymap":
            o["keymap"] = argv[i + 1]
            i += 2
        elif a.startswith("--keymap="):
            o["keymap"] = a.split("=", 1)[1]
            i += 1
        elif a == "--disable-compose":
            o["disable_compose"] = True
            i += 1
        elif a == "--keysym":
            o["keysym"] = argv[i + 1]
            i += 2
        elif a.startswith("--keysym="):
            o["keysym"] = a.split("=", 1)[1]
            i += 1
        else:
            i += 1
    return o


def lookup(path, keysym):
    try:
        return TABLE.get(keymap_sha(path), {}).get(keysym)
    except OSError:
        return None


def emit(rc, text):
    sys.stdout.write(text)
    return rc

__BODY__

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''

SELFTEST = '''def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
__TAIL__
'''

# ------------------------------------------------------------------------------------------------ table shaping
def table_all(cases):
    return {c["keymap_sha256"]: {c["keysym"]: [c["rc"], c["stdout"]] for c in cases if True} for c in cases}


def table_of(cases):
    t = {}
    for c in cases:
        t.setdefault(c["keymap_sha256"], {})[c["keysym"]] = [c["rc"], c["stdout"]]
    return t


def rows_of(text):
    """Split a judge stdout into (header lines, data rows); the first five lines are the fixed preamble."""
    lines = text.splitlines(keepends=True)
    return lines[:5], lines[5:]


def first_row_only(text):
    head, rows = rows_of(text)
    return "".join(head + rows[:1])


MASK = re.compile(r"\[[^\]]*\]")


def blank_masks(text):
    head, rows = rows_of(text)
    return "".join(head + [MASK.sub("[ ]", r) for r in rows])


COL_SPLIT = re.compile(r"^(\d+)\s+(\S+)\s+(\d+)\s+")


def layout1_only(text):
    head, rows = rows_of(text)
    keep = []
    for r in rows:
        m = COL_SPLIT.match(r)
        if not m or m.group(3) == "1":
            keep.append(r)
    return "".join(head + keep)


KEYSYM_LINE = re.compile(r"^keysym: (\S+) \(0x([0-9a-f]{4})\)$")


def header_only(text):
    """The 'unreachable keysym' answer: preamble + column header, no rows."""
    head, _ = rows_of(text)
    return "".join(head)


def rename_key(text, name):
    head, rows = rows_of(text)
    if head and KEYSYM_LINE.match(head[0]):
        head = ["keysym: %s (0x0000)\n" % name] + head[1:]
    return "".join(head + rows)


# ------------------------------------------------------------------------------------------------ bodies
BODY = {}

BODY["c03-first-match-only"] = dict(
    summary="print the first (keycode, layout, level, mask) row and stop, like a tool that returns the first hit",
    stop="clause f: a keysym that a keymap reaches from several keys/levels (br slash: 5 rows) loses every row after the first",
    note="Nothing is computed: the answers are the authoring-time judge bytes for this seat's case list, keyed by\n"
         "(sha256 of the keymap file, keysym argument). Only the row count distinguishes it from a correct tool.",
    body='''def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = lookup(o["keymap"], o["keysym"])
    if hit is None:
        return emit(0, "")
    return emit(hit[0], __FIRST__)
''')

BODY["c04-no-modifiers"] = dict(
    summary="print every row but with the modifier mask blanked to `[ ]`, ignoring xkb_keymap_key_get_mods_for_level",
    stop="clause f: the br fixture reaches slash only through Mod5 LevelThree, so its mask is not empty",
    note="The cheat keeps the row count and the keycode/layout/level columns, so a counter that compares only the\n"
         "preamble or the row count lets it through.",
    body='''def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = lookup(o["keymap"], o["keysym"])
    if hit is None:
        return emit(0, "")
    return emit(hit[0], __BLANK__)
''')

BODY["c06-cache-table"] = dict(
    summary="answer only from a cached table keyed by (keymap sha256, keysym) built from the FIXTURE file",
    stop="clause g: a nonce RMLVO produces a keymap whose sha256 is not in the table, and the tool then prints nothing",
    note="This is the control the task names verbatim: a lookup table built from the fixtures. On clause f it is\n"
         "byte-exact (the table was built from those very fixtures); it has no keymap model at all, so any case the\n"
         "fixture file does not contain is unanswered. Against the replica it is scored on the fixture subset only\n"
         "for clause f and on all 30 generated cases for clause g.",
    body='''def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = lookup(o["keymap"], o["keysym"])
    if hit is None:
        return emit(0, "")
    return emit(hit[0], hit[1])
''')

BODY["c07-read-fixture-repo"] = dict(
    summary="read the fixture file from the repository at run time and answer from it",
    stop="clause i (isolation): no repository path is bound in the sandbox, so the read fails and the answer is empty; "
         "outside the sandbox the same file answers every fixture correctly",
    note="The read path is $MADO_CTL_FIXTURES or quality/counters/c1-r49-fixtures.json relative to the cwd. The control\n"
         "demonstrates why the mount set has to be an allowlist: run it on the host with the file reachable and it is\n"
         "byte-exact; run it in the counter's sandbox and it has nothing to read. It also shows that an inherited\n"
         "environment variable must not reach the tool (the sandbox uses --clearenv).",
    imports="import os",
    body='''FIXTURE_PATH = os.environ.get("MADO_CTL_FIXTURES", "quality/counters/c1-r49-fixtures.json")


def repo_table():
    try:
        with open(FIXTURE_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {}
    t = {}
    for c in data.get("cases", []):
        t.setdefault(c.get("keymap_sha256"), {})[c.get("keysym")] = [c.get("rc"), c.get("stdout", "")]
    return t


def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = repo_table().get(keymap_sha(o["keymap"]), {}).get(o["keysym"])
    if hit is None:
        return emit(0, "")
    return emit(hit[0], hit[1])
''')

BODY["c08-writes-file"] = dict(
    summary="answer correctly, but write (attempt) a cache file first",
    stop="clause r: a write attempt (open with O_WRONLY|O_CREAT / O_APPEND) after the python3 execve, whether it "
         "succeeds or fails",
    note="The table covers every case the replica scores, so clause f and clause g are fully green and the only failing\n"
         "clause is r. That is the point: a counter whose read-only check compares the tree before/after (or which\n"
         "lets the write fail on a read-only mount and then shrugs) scores this control TARGET_MET. The target is\n"
         "/tmp/mado-keysym-answers.cache, a path inside the sandbox's own tmpfs, so a run outside a sandbox writes\n"
         "host /tmp and nothing in the operator's home.",
    imports="import os",
    body='''CACHE = "/tmp/mado-keysym-answers.cache"


def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    path = o["keymap"]
    hit = lookup(path, o["keysym"])
    try:
        with open(CACHE, "a", encoding="utf-8") as fh:
            fh.write("%s %s\\n" % (keymap_sha(path), o["keysym"]))
    except OSError:
        pass
    if hit is None:
        return emit(0, "")
    return emit(hit[0], hit[1])
''')

BODY["c09-opens-socket"] = dict(
    summary="answer correctly, but open and connect a socket first (to a closed local port)",
    stop="clause r: socket() and connect() after the python3 execve",
    note="Same shape as c08: the table covers every scored case, so f and g are green and r is the only failure. A\n"
         "counter that only forbids started processes (execve) and not sockets scores this TARGET_MET.",
    imports="import socket",
    body='''TARGET = ("127.0.0.1", 47999)


def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        try:
            s.connect(TARGET)
        finally:
            s.close()
    except OSError:
        pass
    hit = lookup(o["keymap"], o["keysym"])
    if hit is None:
        return emit(0, "")
    return emit(hit[0], hit[1])
''')

BODY["c10-overfit"] = dict(
    summary="correct on the fixture keymaps, and for any other keymap emit a plausible single bogus row",
    stop="clause g: on a generated keymap the fallback row is wrong (keycode, layout and mask), and it never prints "
         "the error exit for an unrecognised keysym",
    note="Different from c06: this control looks like a model (it produces output for every input and never empties\n"
         "its answer), so a counter that checks only 'does the tool produce output' passes it. On the fixture set it is\n"
         "byte-exact because the table holds those answers; on a keymap it has never seen it has nothing real to say.",
    body='''FALLBACK = "38       AC01      1        English (US)         1       [ ]\\n"


def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = lookup(o["keymap"], o["keysym"])
    if hit is not None:
        return emit(hit[0], hit[1])
    head = ["keysym: %s (0x0000)\\n" % o["keysym"], "\\n", "=== Direct access ===\\n", "\\n",
            "KEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\\n"]
    return emit(0, "".join(head) + FALLBACK)
''')

BODY["c11-selftest-only"] = dict(
    summary="pass --selftest and answer nothing at all for the real call",
    stop="clause f: every fixture with a row (13 of 14) expects bytes on stdout; the tool prints none",
    note="The do-nothing control with a convincing selftest line: a counter that requires only 'selftest ok and tool\n"
         "present' scores this TARGET_MET.",
    body='''def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    return emit(0, "")
''')

BODY["c12-rc-blind"] = dict(
    summary="print the right rows but always exit 0 and never signal an unconvertible keysym",
    stop="clause f: the nosuchsym fixture expects exit 2 (the judge's own status) with empty stdout",
    note="Byte-identical stdout on every successful case and rc 0 everywhere: a counter that compares stdout only,\n"
         "or that treats a non-zero judge status as 'skip this case', scores this TARGET_MET.",
    body='''def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = lookup(o["keymap"], o["keysym"])
    sys.stdout.write(hit[1] if hit else "")
    return 0
''')

BODY["c13-hardcoded-br"] = dict(
    summary="ignore the keymap file and answer from a fixed map (the host's br keymap for slash/Return)",
    stop="clause f: every fixture on another keymap expects that keymap's keycode/layout, not br's",
    note="The 'it works on my machine' control. The fixed map is the br/compose:caps answer for slash, Return and the\n"
         "two error cases; it is right on 4 of the 14 fixtures and wrong on the other 10, which is exactly the shape a\n"
         "counter with one hard-coded host keymap would bless.",
    body='''FIXED = __FIXED__


def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = FIXED.get(o["keysym"])
    if hit is None:
        return emit(0, "")
    return emit(hit[0], hit[1])
''')

BODY["c14-stderr"] = dict(
    summary="print the correct report on stderr and nothing on stdout",
    stop="clause f: stdout bytes must equal the judge's; stderr is not compared",
    note="The status-correct twin of c04: exit status and text are both right, the stream is wrong. A counter that\n"
         "merges the two streams, or that compares 'the tool's output' without saying which stream, scores it\n"
         "TARGET_MET.",
    body='''def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = lookup(o["keymap"], o["keysym"])
    if hit is None:
        return 0
    sys.stderr.write(hit[1])
    return hit[0]
''')

BODY["c15-layout1-only"] = dict(
    summary="drop every row whose LAYOUT column is not 1 (the first layout only)",
    stop="clause f: the us,ru fixture reaches Cyrillic_a on layout 2 only, so its one row disappears",
    note="A counter that only checks single-layout keymaps never sees this; the multi-layout case is the whole point of\n"
         "the LAYOUT/LAYOUT NAME columns.",
    body='''COL = re.compile(r"^(\\d+)\\s+(\\S+)\\s+(\\d+)\\s+")


def trim(text):
    lines = text.splitlines(keepends=True)
    head, rows = lines[:5], lines[5:]
    keep = []
    for r in rows:
        m = COL.match(r)
        if not m or m.group(3) == "1":
            keep.append(r)
    return "".join(head + keep)


def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = lookup(o["keymap"], o["keysym"])
    if hit is None:
        return emit(0, "")
    return emit(hit[0], trim(hit[1]))
''')

BODY["c16-always-unreachable"] = dict(
    summary="always print the 'no key produces this keysym' answer (preamble + column header, exit 0)",
    stop="clause f: 13 of the 14 fixtures expect at least one row; only F35 is genuinely unreachable",
    note="The do-nothing control that still prints a well-formed report. It passes the one fixture whose true answer is\n"
         "an empty table, so a counter with an all-empty fixture set would score it TARGET_MET.",
    body='''def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
    hit = lookup(o["keymap"], o["keysym"])
    if hit is not None and hit[1]:
        head = ["keysym: %s (0x0000)\\n" % o["keysym"], "\\n", "=== Direct access ===\\n", "\\n",
                "KEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\\n"]
        head[0] = hit[1].splitlines(keepends=True)[0]
        if hit[1].count("\\n") == 5:
            return emit(0, hit[1])
        return emit(0, "".join(head))
    return emit(0, "")
''')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    with open(a.cases, encoding="utf-8") as fh:
        cases = json.load(fh)["cases"]
    fx = [c for c in cases if c["id"].startswith("fx-")]
    os.makedirs(a.out, exist_ok=True)

    table_all = table_of(cases)
    table_fx = table_of(fx)
    br = table_of([c for c in fx if c["layout"] == "br"])
    fixed = {}
    for c in [c for c in fx if c["layout"] == "br"]:
        fixed[c["keysym"]] = [c["rc"], c["stdout"]]

    emit_map = {
        "c03-first-match-only": table_all,
        "c04-no-modifiers": table_all,
        "c06-cache-table": table_fx,
        "c07-read-fixture-repo": {},
        "c08-writes-file": table_all,
        "c09-opens-socket": table_all,
        "c10-overfit": table_fx,
        "c11-selftest-only": {},
        "c12-rc-blind": table_all,
        "c13-hardcoded-br": {},
        "c14-stderr": table_all,
        "c15-layout1-only": table_all,
        "c16-always-unreachable": table_all,
    }
    helpers = {
        "__FIRST__": "first_row_only",
        "__BLANK__": "blank_masks",
    }
    helper_src = {
        "first_row_only": '''def first_row_only(text):
    lines = text.splitlines(keepends=True)
    return "".join(lines[:6])
''',
        "blank_masks": '''MASK = re.compile(r"\\[[^\\]]*\\]")


def blank_masks(text):
    lines = text.splitlines(keepends=True)
    head, rows = lines[:5], lines[5:]
    return "".join(head + [MASK.sub("[ ]", r) for r in rows])
''',
    }
    written = []
    for name in sorted(emit_map):
        spec = BODY[name]
        body = spec["body"]
        used = []
        for token, fn in helpers.items():
            if token in body:
                body = body.replace(token, fn + "(hit[1])")
                used.append(fn)
        body = body.replace("__FIXED__", json.dumps(fixed, indent=4, sort_keys=True))
        imports = spec.get("imports", "")
        if "re." in body:
            imports = (imports + "\nimport re").strip()
        text = COMMON
        text = text.replace("__NAME__", name)
        text = text.replace("__SUMMARY__", spec["summary"])
        text = text.replace("__STOP__", spec["stop"])
        text = text.replace("__NOTE__", spec["note"])
        text = text.replace("__IMPORTS__", imports)
        text = text.replace("__BODY__", "\n".join(helper_src[h] for h in used) + "\n\n" + body)
        text = text.replace("__TABLE__", json.dumps(emit_map[name], indent=4, sort_keys=True))
        path = os.path.join(a.out, name + ".py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.chmod(path, 0o755)
        written.append(path)
    for p in written:
        print("wrote %s" % p)
    print("controls=%d" % len(written))


if __name__ == "__main__":
    main()
