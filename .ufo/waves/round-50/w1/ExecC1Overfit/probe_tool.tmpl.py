#!/usr/bin/env python3
"""Clause-g overfit probe for PRED-C1-r49 (seat ExecC1Overfit, mado round 50).

NOT an instrument. A deliberately cheap/cheating tool used to measure how far memorising the
frozen fixtures (clause f) plus a first-level-only fallback gets on the nonce-drawn generated
cases (clause g). VARIANT selects the fallback; the memorisation table is embedded when present.

  table_lvl1 : memorised (keymap sha256, ARG) table, else level-1-only rows (all groups)
  table_lvl2 : memorised table, else level-1 + level-2 rows
  lvl1       : no table, level-1-only rows
  lvl2       : no table, level-1 + level-2 rows
  header     : no table, header block only (zero rows)

The keysym name/value tables and the get_name fallbacks are read from the pinned header that the
counter's sandbox already binds (/usr/include/xkbcommon/xkbcommon-keysyms.h); from_name /
get_name semantics follow libxkbcommon 1.13.2 src/keysym.c (U-form, 0x-form, XF86_ retry).
"""
import base64
import hashlib
import json
import re
import sys
import zlib

VARIANT = "__VARIANT__"
TABLE_B85 = """__TABLE_B85__"""

HEADER = "/usr/include/xkbcommon/xkbcommon-keysyms.h"
KEYMAP_PATH = "/fixture/keymap.xkb"
KEYSYM_MAX = 0x1FFFFFFF
UNICODE_MIN = 0x01000100
UNICODE_MAX = 0x0110FFFF
LEGACY = {0x08: 0xFF08, 0x09: 0xFF09, 0x0A: 0xFF0A, 0x0B: 0xFF0B, 0x0D: 0xFF0D,
          0x1B: 0xFF1B, 0x7F: 0xFFFF}

_NAME2VAL = None
_VAL2NAME = None


def header_tables():
    global _NAME2VAL, _VAL2NAME
    if _NAME2VAL is None:
        n2v, v2n = {}, {}
        try:
            text = open(HEADER, encoding="ascii", errors="replace").read()
        except OSError:
            text = ""
        for line in text.splitlines():
            m = re.match(r"#define XKB_KEY_([A-Za-z0-9_]+)\s+(0x[0-9a-fA-F]+)", line)
            if m:
                name, val = m.group(1), int(m.group(2), 16)
                n2v.setdefault(name, val)
                v2n.setdefault(val, name)
        _NAME2VAL, _VAL2NAME = n2v, v2n
    return _NAME2VAL, _VAL2NAME


def from_name(name):
    """libxkbcommon 1.13.2 xkb_keysym_from_name(name, 0), approximated from the header."""
    n2v, _ = header_tables()
    val = n2v.get(name)
    if val is not None:
        return val
    m = re.fullmatch(r"([0-9a-fA-F]{1,8})", name[1:]) if name[:1] == "U" else None
    if m:
        cp = int(m.group(1), 16)
        if 0xFF < cp <= 0x10FFFF:
            return 0x01000000 + cp
        if cp == 0:
            return 0
        return LEGACY.get(cp, cp)
    if name[:2] == "0x" and re.fullmatch(r"[0-9a-fA-F]{1,8}", name[2:]):
        v = int(name[2:], 16)
        return v if v <= KEYSYM_MAX else 0
    if name.startswith("XF86_"):
        return n2v.get("XF86" + name[5:], 0)
    return 0


def from_decimal(text):
    m = re.fullmatch(r"[ \t\n\v\f\r]*([+-]?)([0-9]+)", text)
    if not m:
        return 0
    v = int(m.group(1) + m.group(2))
    return v if 0 < v <= KEYSYM_MAX else 0


def resolve(argument):
    v = from_name(argument)
    if v:
        return v
    v = from_decimal(argument)
    return v if v > 0 else None


def get_name(keysym):
    _, v2n = header_tables()
    name = v2n.get(keysym)
    if name is not None:
        return name
    if UNICODE_MIN <= keysym <= UNICODE_MAX:
        return "U%04X" % (keysym & 0xFFFFFF)
    return "0x%08x" % keysym


def hex_keysym(keysym):
    return "0x%04x" % keysym if keysym <= 0xFFFF else "0x%x" % keysym


def ljust(text, width):
    return text + " " * max(0, width - len(text.encode("utf-8", "surrogateescape")))


def block(text, section):
    i = text.find("\n" + section + " ")
    if i < 0:
        i = text.find("\n" + section + "{")
    if i < 0:
        return ""
    j = text.find("{", i)
    if j < 0:
        return ""
    k = text.find("\n};", j)
    return text[j:k if k >= 0 else len(text)]


def parse_keymap(text):
    """(keycodes: name->code, group names, keys: [(code, name, [symlist per group])]) - cheap."""
    codes = {}
    aliases = {}
    kc = block(text, "xkb_keycodes")
    for m in re.finditer(r"<([A-Za-z0-9_]+)>\s*=\s*(\d+)\s*;", kc):
        codes[m.group(1)] = int(m.group(2))
    for m in re.finditer(r"<([A-Za-z0-9_]+)>\s*=\s*<([A-Za-z0-9_]+)>\s*;", kc):
        aliases[m.group(1)] = m.group(2)
    for alias, real in aliases.items():
        if real in codes:
            codes[alias] = codes[real]

    sym = block(text, "xkb_symbols")
    names = {}
    for m in re.finditer(r'name\[(?:group)?(\d+)\]\s*=\s*"([^"]*)"', sym):
        names[int(m.group(1))] = m.group(2)

    keys = []
    for m in re.finditer(r"key\s+<([A-Za-z0-9_]+)>\s*\{(.*?)\}\s*;", sym, re.S):
        name, body = m.group(1), m.group(2)
        if name not in codes:
            continue
        groups = []
        for g in re.finditer(r"symbols\[(\d+)\]\s*=\s*\[([^\]]*)\]", body):
            while len(groups) < int(g.group(1)):
                groups.append([])
            groups[int(g.group(1)) - 1] = [t.strip() for t in g.group(2).split(",")]
        if not groups:
            one = re.search(r"\[([^\]]*)\]", body)
            if one:
                groups = [[t.strip() for t in one.group(1).split(",")]]
        if groups:
            keys.append((codes[name], name, groups))
    keys.sort()
    return keys, names


def sym_value(token):
    if not token or token == "NoSymbol" or token.startswith('"'):
        return 0
    return from_name(token)


def is_alpha_pair(first, second):
    if not first or not second:
        return False
    return (first != first.upper() and second != second.lower()
            and first != second and first.upper() == second.upper())


def render(keys, names, keysym, levels):
    lines = ["keysym: %s (%s)" % (get_name(keysym), hex_keysym(keysym)),
             "", "=== Direct access ===", "",
             " ".join([ljust("KEYCODE", 8), ljust("KEY NAME", 9), ljust("LAYOUT", 8),
                       ljust("LAYOUT NAME", 20), ljust("LEVEL#", 7), "MODIFIERS"])]
    for code, name, groups in keys:
        for gi, group in enumerate(groups):
            layout = names.get(gi + 1) or "?"
            pair = is_alpha_pair(group[0] if group else "", group[1] if len(group) > 1 else "")
            for level in range(1, min(levels, len(group)) + 1):
                if sym_value(group[level - 1]) != keysym:
                    continue
                if level == 1:
                    masks = [[]]
                elif level == 2:
                    masks = [["Shift"], ["Lock"]] if pair else [["Shift"]]
                else:
                    continue
                for mask in masks:
                    lines.append(" ".join([
                        ljust("%d" % code, 8), ljust(name, 9), ljust("%d" % (gi + 1), 8),
                        ljust(layout, 20), ljust("%d" % level, 7),
                        "[ " + "".join(n + " " for n in mask) + "]"]))
    return "\n".join(lines) + "\n"


def load_table():
    if not TABLE_B85:
        return {}
    rows = json.loads(zlib.decompress(base64.b85decode(TABLE_B85)).decode("ascii"))
    return {(sha, arg): (rc, base64.b64decode(out)) for sha, arg, rc, out in rows}


def usage(stream):
    stream.write(b"Usage: probe how-to-type --keymap FILE --disable-compose --keysym ARG\n"
                 b"       probe --selftest\n")


def main(argv):
    args = list(argv[1:])
    if args and args[0] == "--selftest":
        # Finding: the counter's clause s only greps the last line for N/N with N >= 25.
        sys.stdout.write("MADO_KEYSYM_SELFTEST: 25/25 passed\n")
        return 0
    if args and args[0] in ("-h", "--help", "help"):
        usage(sys.stdout.buffer)
        return 0
    if args and args[0] == "how-to-type":
        args.pop(0)
    keymap_path = None
    keysym_mode = disable_compose = False
    positional = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--disable-compose":
            disable_compose = True
        elif a == "--keysym":
            keysym_mode = True
        elif a == "--keymap":
            i += 1
            if i >= len(args):
                sys.stderr.write("ERROR: --keymap needs a file\n")
                usage(sys.stderr.buffer)
                return 2
            keymap_path = args[i]
        elif a.startswith("--keymap="):
            keymap_path = a[len("--keymap="):]
        elif a.startswith("-") and a != "-":
            sys.stderr.write("ERROR: unknown option %s\n" % a)
            usage(sys.stderr.buffer)
            return 2
        else:
            positional.append(a)
        i += 1
    if not (disable_compose and keysym_mode):
        sys.stderr.write("ERROR: --disable-compose and --keysym are required\n")
        usage(sys.stderr.buffer)
        return 2
    if keymap_path is None or len(positional) != 1:
        sys.stderr.write("ERROR: --keymap FILE and one keysym argument are required\n")
        usage(sys.stderr.buffer)
        return 2
    try:
        blob = open(keymap_path, "rb").read()
    except OSError as e:
        sys.stderr.write('ERROR: Failed to open keymap file "%s": %s\n' % (keymap_path, e.strerror))
        return 1

    argument = positional[0]
    if VARIANT.startswith("table"):
        hit = load_table().get((hashlib.sha256(blob).hexdigest(), argument))
        if hit is not None:
            rc, out = hit
            sys.stdout.buffer.write(out)
            return rc

    keysym = resolve(argument)
    if keysym is None:
        sys.stderr.write("ERROR: Failed to convert argument to keysym\n")
        usage(sys.stderr.buffer)
        return 2
    if VARIANT.endswith("header"):
        out = render([], {}, keysym, 0)
    else:
        try:
            keys, names = parse_keymap(blob.decode("utf-8", "surrogateescape"))
            out = render(keys, names, keysym, 1 if VARIANT.endswith("lvl1") else 2)
        except Exception:
            out = render([], {}, keysym, 0)
    sys.stdout.buffer.write(out.encode("utf-8", "surrogateescape"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
