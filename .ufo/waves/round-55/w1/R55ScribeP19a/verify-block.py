#!/usr/bin/env python3
# R55ScribeP19a verifier (leaf seat, draft). Proves: base is a byte prefix of after.md;
# after.md tail == block.md; every Q row is byte-equal to frozen c3.q; every Q quote equals
# the stripped round-52 pin line at its line; P23 cell carries the frozen p23 tokens and
# Supersedes=P19; heading contains 'Correction (round 55)'. Prints one line per check.
import hashlib
import json
import os
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "3b55b6e91e40f455dd56b2985e4ffc087ada92d5"
FREEZE = "54dacbd843d64ba744cd3f1bdc2ec622e5010039"
ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
TABLES = ".ufo/waves/round-55/frozen-tables.json"
OUT = os.path.dirname(os.path.abspath(__file__))


def git_show(rev, path):
    return subprocess.run(
        ["git", "-C", REPO, "show", f"{rev}:{path}"],
        check=True, capture_output=True,
    ).stdout


def main():
    fails = []

    def check(name, ok, detail=""):
        print(f"{'PASS' if ok else 'FAIL'} {name}{(' ' + detail) if detail else ''}")
        if not ok:
            fails.append(name)

    c3 = json.loads(git_show(FREEZE, TABLES))["c3"]
    base = git_show(BASE, ENTRY)
    after = open(os.path.join(OUT, "after.md"), "rb").read()
    block = open(os.path.join(OUT, "block.md"), "rb").read()
    pin = git_show(BASE, c3["pin"])

    check("pin_sha256", hashlib.sha256(pin).hexdigest() == c3["pin_sha256"])
    check("prefix_identical", after.startswith(base), f"base={len(base)} after={len(after)}")
    check("tail_equals_block", after[len(base):] == block)
    check("block_ends_newline", block.endswith(b"\n"))

    text = after.decode("utf-8")
    btext = text[len(base.decode("utf-8")):]
    heads = [l for l in btext.split("\n") if l.startswith("#") and "Correction (round 55)" in l]
    check("heading", len(heads) == 1, f"count={len(heads)}")

    pin_lines = pin.split(b"\n")
    rows = {}
    for line in btext.split("\n"):
        m = re.match(r"^\| (Q\d\d) \| (Hyprland-ConfigActions\.cpp):(\d+) \| `(.*)` \|$", line)
        if m:
            rows.setdefault(m.group(1), []).append((m.group(3), m.group(4)))

    for q in c3["q"]:
        qid = q["id"]
        got = rows.get(qid, [])
        exp = (str(q["line"]), q["quote"])
        check(f"rows:{qid}", got == [exp], f"got={got}")
        if got:
            ln, qt = got[0]
            pl = pin[0:0] + pin_lines[int(ln) - 1].strip(b" \t\r\n\v\f")
            check(f"pin:{qid}", pl == qt.encode("utf-8"), f"line={ln}")

    p23 = [l for l in btext.split("\n") if l.startswith("| P23 |")]
    check("p23_row_count", len(p23) == 1, f"count={len(p23)}")
    if p23:
        cells = [c.strip() for c in p23[0].strip().strip("|").split("|")]
        check("p23_supersedes", len(cells) >= 2 and cells[1] == "P19", f"cell={cells[1] if len(cells) > 1 else None}")
        prop = cells[2] if len(cells) > 2 else ""
        tokens = ["m_passPressed", "== 1", "== 0", "PRESSED", "RELEASED"]
        miss = [t for t in tokens if t not in prop]
        has_other = any(t in prop for t in ["otherwise", "any other", "else"])
        check("p23_tokens", not miss and has_other, f"missing={miss} other={has_other}")
        check("p23_pin_anchor", cells[4] == "Hyprland-ConfigActions.cpp:1554-1576", f"cell={cells[4]}")

    readme = git_show(BASE, "corpus/README.md").decode("utf-8").split("\n")
    check("readme_at_base", any(ENTRY.split("/")[-1] in l and "P23" in l for l in readme),
          "(expected FAIL until L1 integrates README row)")

    print(f"VERIFY: failed={len(fails)} names={','.join(fails) or 'none'}")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
