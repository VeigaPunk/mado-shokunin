#!/usr/bin/env python3
"""Build the eight reading-variants of mado-geometry.py (seat ExecIndepC, round 43).

Each variant keeps the tool's behaviour except for one reading of the frozen
contract, so that the frozen counter's fixture set can be asked whether that
reading is pinned. Run from the seat directory: python3 variants/build-variants.py
"""
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir,
                    "mado-geometry.py")
SRC = open(BASE).read()
OUT = os.path.dirname(os.path.abspath(__file__))

EDITS = {
    # 1-200 counts characters of the REGEX, not alphabet tokens
    "vA-length-chars.py": [
        ("    if tokens > MAX_REGEX_TOKENS:\n        return False",
         "    if len(text) > MAX_REGEX_TOKENS:\n        return False"),
        ("    if tokens < 1:\n        return False",
         "    if len(text) < 1:\n        return False"),
    ],
    # bad_json judged after the rules files are loaded
    "vB-rules-before-badjson.py": [
        ('''    document = parse_clients(data)
    if document is None:
        return emit(["MADO_GEOMETRY: SETUP bad_json"], 2)
    texts = []
    for path in options["rules"]:
        blob, why = load_source(path, False, None)
        if blob is None:
            return emit(["MADO_GEOMETRY: SETUP " + why], 2)
        texts.append(blob.decode("utf-8", "replace"))
''',
         '''    texts = []
    for path in options["rules"]:
        blob, why = load_source(path, False, None)
        if blob is None:
            return emit(["MADO_GEOMETRY: SETUP " + why], 2)
        texts.append(blob.decode("utf-8", "replace"))
    document = parse_clients(data)
    if document is None:
        return emit(["MADO_GEOMETRY: SETUP bad_json"], 2)
'''),
    ],
    # TILED judged before BADSIZE
    "vC-tiled-before-badsize.py": [
        ('''        if size is None:
            verdict = "BADSIZE"
        elif floating is False:
            verdict = "TILED"''',
         '''        if floating is False:
            verdict = "TILED"
        elif size is None:
            verdict = "BADSIZE"'''),
    ],
    # a malformed size/float line counted as other instead of unsupported
    "vD-malformed-is-other.py": [
        ('''            if len(fields) != 2:
                unsupported += 1
                continue''',
         '''            if len(fields) != 2:
                other += 1
                continue'''),
    ],
    # every rules path checked for unreadable before any is judged too_large
    "vE-all-unreadable-before-too-large.py": [
        ('''    texts = []
    for path in options["rules"]:
        blob, why = load_source(path, False, None)
        if blob is None:
            return emit(["MADO_GEOMETRY: SETUP " + why], 2)
        texts.append(blob.decode("utf-8", "replace"))
''',
         '''    for path in options["rules"]:
        try:
            info = os.stat(path)
        except OSError:
            return emit(["MADO_GEOMETRY: SETUP unreadable"], 2)
        if not stat.S_ISREG(info.st_mode) or path == "-":
            return emit(["MADO_GEOMETRY: SETUP unreadable"], 2)
    texts = []
    for path in options["rules"]:
        blob, why = load_source(path, False, None)
        if blob is None:
            return emit(["MADO_GEOMETRY: SETUP " + why], 2)
        texts.append(blob.decode("utf-8", "replace"))
'''),
    ],
    # a non-UTF-8 rules file is an error instead of being decoded with replace
    "vG-strict-rule-decode.py": [
        ('texts.append(blob.decode("utf-8", "replace"))',
         'texts.append(blob.decode("utf-8"))'),
    ],
    # NO_MATCHING_CLIENT judged before NO_SIZE_RULES
    "vH-no-match-before-no-size.py": [
        ('''    if size_rules == 0:
        verdict, code = "NO_SIZE_RULES", 4
    elif tallies["DIFFER"] > 0:
        verdict, code = "DIFFER", 1
    elif tallies["matched"] == 0:
        verdict, code = "NO_MATCHING_CLIENT", 3''',
         '''    if tallies["matched"] == 0:
        verdict, code = "NO_MATCHING_CLIENT", 3
    elif size_rules == 0:
        verdict, code = "NO_SIZE_RULES", 4
    elif tallies["DIFFER"] > 0:
        verdict, code = "DIFFER", 1'''),
    ],
    # rules= counts every supported rule, not only the size rules
    "vI-rules-counts-all-supported.py": [
        ("    summary, code = summarize(size_rules, len(rules) - size_rules, other,",
         "    summary, code = summarize(len(rules), len(rules) - size_rules, other,"),
    ],
}


def main():
    for name, edits in sorted(EDITS.items()):
        text = SRC
        for old, new in edits:
            if old not in text:
                raise SystemExit("variant %s: source text not found: %r"
                                 % (name, old[:60]))
            text = text.replace(old, new)
        with open(os.path.join(OUT, name), "w") as handle:
            handle.write(text)
        print("wrote", name)


if __name__ == "__main__":
    main()
