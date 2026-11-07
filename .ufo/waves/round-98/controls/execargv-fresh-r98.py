#!/usr/bin/env python3
"""mado round-98 fresh-case generator (seat R98MExecOracle).

Instrument, not candidate: every fresh case is measured through the
committed oracle builder (execargv-probe-r98.py, imported once by pinned
path from this script's own directory; the only module attributes touched
are case_expect, GIO_SHA256 and GLIB2), so each JSONL line's expect and
label are what the installed /usr/bin/gio did at generation time.
stdlib only.

Usage:
  execargv-fresh-r98.py --seed HEX --dir D --out F --count N

--seed HEX  seed for random.Random(int(HEX, 16)); the same seed builds the
            same cases (no timestamps, no mkdtemp in the case numbering)
--dir D     parent for the case roots; each root <D>/<case-id> is
            materialised in place and removed again after its measurement
--out F     JSONL destination, one line per case:
            {"id","index","desktop","args","files","expect","label"}
            label is "ok" or "refusal:<cause>" (measured, never predicted)
--count N   number of cases (required, no default)

stdout: "FRESH_GEN: cases=N ok=A refused=B" plus a FRESH_GEN_PIN line
carrying the gio sha256 / glib2 pin the labels were measured under.
"""

import argparse
import base64
import importlib.util
import json
import os
import random
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROBE_PATH = os.path.join(_HERE, "execargv-probe-r98.py")
# QUALITY 165: the one sibling-module load, pinned by path and by use.
_spec = importlib.util.spec_from_file_location("execargv_probe_r98", _PROBE_PATH)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

# Weighted field-code pool: the modelled grammar (frequent codes, deprecated
# d/D/n/N/m/v, literal %%, and the unknown z/q that expand to nothing).
CODES = (
    ["f"] * 8 + ["u"] * 8 + ["F"] * 6 + ["U"] * 6 + ["d"] * 4 + ["n"] * 4 +
    ["D"] * 2 + ["N"] * 2 + ["i"] * 6 + ["c"] * 4 + ["k"] * 4 +
    ["m"] * 2 + ["v"] * 2 + ["%"] * 4 + ["z"] * 3 + ["q"] * 3
)
# Literal Exec tokens; "a\ b" carries the GKeyFile escape gio refuses, so
# the pool also yields measured desktop-file refusals.
LITERALS = ["plain", '"a b"', "'a b'", "tok", "end%", "a\\ b", "a%1b"]
FILE_POOL = ["f1.txt", "f2.txt", "with space.txt", "it's.txt"]
URI_POOL = ["http://example.com/a", "https://example.com/b?q=1",
            "mailto:x@y.example", "file://{root}/f1.txt#s",
            "file://{root}/f2.txt"]
NAMES = ["Probe", "Probe Two", "O'Brien", 'Say "hi"']
ICONS = [None, "ic.png", "my icon"]

CONTENT = base64.b64encode(b"fresh\n").decode()


def gen_exec(rng):
    parts = ["{probe}"]
    for _ in range(rng.choice((0, 1, 1, 2))):
        parts.append("%" + rng.choice(CODES))
    for _ in range(rng.choice((0, 1, 1, 2))):
        parts.append(rng.choice(LITERALS))
    rest = parts[1:]
    rng.shuffle(rest)
    return " ".join(["{probe}"] + rest)


def gen_args(rng):
    args = []
    files = {}
    for _ in range(rng.choice((0, 1, 1, 2, 2, 3, 4))):
        if rng.random() < 0.6:
            path = rng.choice(FILE_POOL)
            args.append({"kind": "file", "path": path})
            files[path] = CONTENT
        else:
            args.append({"kind": "uri", "uri": rng.choice(URI_POOL)})
    return args, files

def gen_desktop_raw(rng, desktop):
    """Occasionally emit desktop_raw bytes (a Name[en_US] locale key or #
    comment lines) instead of the plain structured desktop; None = plain.
    X-GIO-NoFuse is a structured desktop key, set in main(). Deterministic:
    one rng draw per case."""
    kind = rng.choice(("plain", "plain", "plain", "plain", "plain",
                       "plain", "locale", "comment"))
    if kind == "plain":
        return None
    lines = []
    if kind == "comment":
        lines.append("# mado fresh comment")
    lines.append("[Desktop Entry]")
    if kind == "comment":
        lines.append("# between group and keys")
    lines.append("Type=Application")
    lines.append("Name=%s" % desktop["Name"])
    if desktop["Icon"] is not None:
        lines.append("Icon=%s" % desktop["Icon"])
    lines.append("Exec=%s" % desktop["Exec"])
    if kind == "locale":
        lines.append("Name[en_US]=Fresh Locale Name")
    if kind == "comment":
        lines.append("# trailing comment")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="mado r98 fresh-case generator")
    ap.add_argument("--seed", required=True, help="hex seed")
    ap.add_argument("--dir", required=True, dest="dir",
                    help="parent dir for the case roots")
    ap.add_argument("--out", required=True, help="JSONL destination")
    ap.add_argument("--count", required=True, type=int,
                    help="number of cases")
    args = ap.parse_args(argv)

    seed_hex = args.seed.lower()
    if seed_hex.startswith("0x"):
        seed_hex = seed_hex[2:]
    rng = random.Random(int(seed_hex, 16))
    os.makedirs(args.dir, exist_ok=True)
    out_parent = os.path.dirname(os.path.abspath(args.out))
    if out_parent:
        os.makedirs(out_parent, exist_ok=True)

    ok = refused = setup = 0
    with open(args.out, "w", encoding="ascii", newline="\n") as fh:
        for i in range(args.count):
            cid = "fresh-%s-%02d" % (seed_hex, i)
            case = {
                "id": cid,
                "class": "fresh",
                "desktop": {
                    "Name": rng.choice(NAMES),
                    "Icon": rng.choice(ICONS),
                    "Type": "Application",
                    "Exec": gen_exec(rng),
                    "Path": None,
                    "Terminal": None,
                    "Hidden": None,
                    "X-GIO-NoFuse": None,
                },
            }
            case_args, files = gen_args(rng)
            case["args"] = case_args
            case["files"] = files
            if rng.random() < 0.08:
                case["desktop"]["X-GIO-NoFuse"] = "true"
            raw = gen_desktop_raw(rng, case["desktop"])
            if raw is not None:
                case["desktop_raw"] = raw
            expect, meta = mod.case_expect(case, args.dir, keep=False)
            for _ in range(2):
                if expect.get("error") != "setup-error":
                    break
                expect, meta = mod.case_expect(case, args.dir, keep=False)
            if "argv" in expect:
                # Declaration rule 7: launch count + multiset of argv
                # vectors; spawn order is unobservable, so the compared
                # plane is the canonically sorted vectors.
                expect["argv"] = sorted(expect["argv"])
            if "launches" in expect:
                label = "ok"
            elif expect.get("error") == "setup-error":
                label = "setup-error"
            else:
                label = "refusal:" + expect["error"]
            if label == "ok":
                ok += 1
            elif label.startswith("refusal:"):
                refused += 1
            else:
                setup += 1
            rec = {"id": cid, "index": i, "desktop": case["desktop"],
                   "args": case_args, "files": files, "expect": expect,
                   "label": label}
            if "desktop_raw" in case:
                rec["desktop_raw"] = case["desktop_raw"]
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
    print("FRESH_GEN: cases=%d ok=%d refused=%d setup=%d" % (args.count, ok, refused, setup))
    print("FRESH_GEN_PIN: gio_sha256=%s glib2=%s" % (mod.GIO_SHA256, mod.GLIB2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
