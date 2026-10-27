#!/usr/bin/env python3
"""check100-state-cite.py — seat prototype for candidate QUALITY criterion 100 (M49-1).

A host-consequence model or claim about *which state a compositor reads* must cite the source
line that SETS that state, and the value it claims must agree with the setters that exist.

Claim file lines (one claim per line, blanks and '#' comments ignored):

    S100 claim=<id> state=<symbol> attr=<modmask|identity> value=<zero|nonzero|any> cite=<file>:<line>

`--source DIR` is the directory the `cite` path is resolved against and the directory scanned
for setters (`*.cpp`, `*.h`, `*.c`, `*.cc`).  Classification of the cited line:

    SITE_SET          the cited line assigns the state or passes it as the first argument of an
                      update/constructor call (xkb_state_new, *_update_mask, ...)
    READ_ONLY_CITE    the state appears only as an argument of a getter/unref on that line
    STATE_NOT_ON_LINE the state does not appear on the cited line at all
    LOCATOR_UNRESOLVED the cite path/line does not resolve under --source

Value arm: for `attr=modmask value=nonzero` at least one setter of that state must pass a
non-literal-zero modifier mask; for `value=zero` every setter must pass literal zeros.  A claim
whose value no setter supports is VALUE_CONTRADICTED even if the cited line is a setter.

Output: one line per claim, then `CHECK100: claims=<n> set=<n> readonly=<n> unresolved=<n>
contradicted=<n> verdict=OK|FAIL`; exit 1 on any non-OK line.
"""
import argparse
import glob
import os
import re
import sys

SET_CALLS = ("xkb_state_new", "xkb_state_update_mask", "xkb_state_update_key",
             "xkb_state_update_mask_effective")
READ_CALLS = ("xkb_state_key_get_one_sym", "xkb_state_key_get_syms", "xkb_state_key_get_utf8",
              "xkb_state_unref", "xkb_state_key_get_one_sym_scalar")
SRC_EXT = (".cpp", ".h", ".c", ".cc", ".hpp")


def parse_claim(line):
    f = dict(re.findall(r'(\w+)=(\S+)', line))
    return f


def classify(line_text, state):
    pat = re.compile(r'\b' + re.escape(state) + r'\b')
    if not pat.search(line_text):
        return "STATE_NOT_ON_LINE"
    # assignment to the state itself
    if re.search(r'\b' + re.escape(state) + r'\s*=[^=]', line_text):
        return "SITE_SET"
    for call in SET_CALLS:
        if re.search(re.escape(call) + r'\s*\(\s*' + re.escape(state) + r'\b', line_text) or \
           re.search(re.escape(call) + r'\s*\([^)]*?' + re.escape(state) + r'\s*\)', line_text):
            # first argument (or, for *_key_*/_new-free helpers, the only argument) is the state
            if re.search(re.escape(call) + r'\s*\(\s*' + re.escape(state) + r'\b', line_text):
                return "SITE_SET"
    for call in READ_CALLS:
        if re.search(re.escape(call) + r'\s*\(', line_text):
            return "READ_ONLY_CITE"
    return "STATE_NOT_ON_LINE"


def setters(source, state):
    """Return [(file, line, args)] for every *_update_mask(<state>, ...) in source."""
    out = []
    pat = re.compile(r'xkb_state_update_mask\s*\(\s*' + re.escape(state) + r'\s*,([^;]*)\)\s*;')
    for path in sorted(glob.glob(os.path.join(source, "**", "*"), recursive=True)):
        if not path.endswith(SRC_EXT):
            continue
        try:
            with open(path, "r", errors="replace") as fh:
                for n, text in enumerate(fh, 1):
                    for m in pat.finditer(text):
                        out.append((os.path.relpath(path, source), n, m.group(1).strip()))
        except OSError:
            continue
    return out


def mods_are_zero(args):
    parts = [p.strip() for p in args.split(",")]
    return all(p in ("0", "0x0", "0U", "0u") for p in parts[:3])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", required=True)
    ap.add_argument("--source", required=True)
    a = ap.parse_args(argv)

    claims, ok = [], 0
    counts = dict(set=0, readonly=0, unresolved=0, contradicted=0)
    with open(a.claims, "r", errors="replace") as fh:
        for n, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if not line.startswith("S100"):
                print(f"CLAIM_UNPARSED {a.claims}:{n}")
                counts["unresolved"] += 1
                continue
            f = parse_claim(line)
            for k in ("claim", "state", "attr", "value", "cite"):
                if k not in f:
                    print(f"CLAIM_UNPARSED {a.claims}:{n} missing={k}")
                    counts["unresolved"] += 1
                    f = None
                    break
            if not f:
                continue
            try:
                rel, lineno = f["cite"].rsplit(":", 1)
                lineno = int(lineno)
            except ValueError:
                print(f"LOCATOR_UNRESOLVED claim={f['claim']} cite={f['cite']}")
                counts["unresolved"] += 1
                continue
            path = os.path.join(a.source, rel)
            try:
                with open(path, "r", errors="replace") as fh2:
                    text = fh2.read().splitlines()[lineno - 1]
            except (OSError, IndexError):
                print(f"LOCATOR_UNRESOLVED claim={f['claim']} cite={f['cite']}")
                counts["unresolved"] += 1
                continue

            cls = classify(text, f["state"])
            sites = setters(a.source, f["state"])
            nz = [s for s in sites if not mods_are_zero(s[2])]
            verdict = "OK"
            if cls != "SITE_SET":
                verdict = "FAIL"
                counts["readonly"] += 1
            if f["attr"] == "modmask":
                if f["value"] == "nonzero" and not nz:
                    verdict = "FAIL"
                    if cls == "SITE_SET":
                        counts["contradicted"] += 1
                elif f["value"] == "zero" and nz:
                    verdict = "FAIL"
                    if cls == "SITE_SET":
                        counts["contradicted"] += 1
            if cls == "SITE_SET" and verdict == "OK":
                counts["set"] += 1
            claims.append(f)
            ok += verdict == "OK"
            print(f"STATE_CLAIM claim={f['claim']} state={f['state']} attr={f['attr']} "
                  f"value={f['value']} cite={f['cite']} line={cls} setters={len(sites)} "
                  f"nonzero_setters={len(nz)} verdict={verdict}")

    fail = len(claims) - ok + counts["unresolved"]
    print(f"CHECK100: claims={len(claims) + counts['unresolved']} set={counts['set']} "
          f"readonly={counts['readonly']} unresolved={counts['unresolved']} "
          f"contradicted={counts['contradicted']} verdict={'OK' if fail == 0 else 'FAIL'}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
