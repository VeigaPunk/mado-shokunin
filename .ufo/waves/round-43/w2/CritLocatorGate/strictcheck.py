#!/usr/bin/env python3
"""strictcheck.py - audit check-locators.py's OK verdicts with a stricter test.

For every locator the frozen checker scores, re-derive the attributed fragment
with the checker's own functions, then ask three questions the token test does
not ask:

  quote   - is the attributed fragment present in the cited lines as written
            (whitespace runs collapsed), not merely its identifiers?
  numbers - does every digit run of the fragment occur in the cited lines?
  empty   - are all cited line numbers outside the file?

Read-only; imports the frozen checker by path. Usage:
  python3 -I strictcheck.py --fetch DIR PROSE...
"""
import argparse
import importlib.util
import os
import re
import sys

CHECKER = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-locators.py"


def load_checker(path):
    spec = importlib.util.spec_from_file_location("check_locators_frozen", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm(text):
    return " ".join(text.split())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", required=True)
    ap.add_argument("prose", nargs="+")
    args = ap.parse_args(argv)
    cl = load_checker(CHECKER)
    fetch_names = {n for n in os.listdir(args.fetch) if os.path.isfile(os.path.join(args.fetch, n))}
    receipts = {}
    totals = {"loc": 0, "ok": 0, "quote_absent": 0, "num_absent": 0, "empty": 0, "ok_but_weak": 0}
    for prose in args.prose:
        with open(prose, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
        for lineno, line in enumerate(lines, 1):
            cands = cl._candidates(line, fetch_names)
            for m in cl.LOCATOR_RE.finditer(line):
                base = cl.resolve_name(m.group("name"), fetch_names)
                if base is None:
                    continue
                if base not in receipts:
                    receipts[base] = cl.load_receipt(os.path.join(args.fetch, base))
                ranges = cl.parse_ranges(m.group("ranges"))
                text = cl.cited_text(receipts[base], ranges)
                support = {c[2]: all(cl.token_occurs(t, text) for t in c[3]) for c in cands}
                before = [c for c in cands if c[1] <= m.start()]
                after = [c for c in cands if c[0] >= m.end()]
                attr = before[-1] if before else (after[0] if after else None)
                verdict = "NOFRAG" if attr is None else ("OK" if support[attr[2]] else "MISS")
                totals["loc"] += 1
                if verdict != "OK":
                    print("STRICT %s:%d %s verdict=%s nopic" % (prose, lineno, m.group(0), verdict))
                    continue
                totals["ok"] += 1
                frag = attr[2]
                nf, nt = norm(frag), norm(text)
                quote = nf in nt
                nums = [n for n in re.findall(r"[0-9]+", frag)
                        if not re.search(r"(?<![0-9])" + re.escape(n) + r"(?![0-9])", text)]
                empty = text.strip() == ""
                if empty:
                    totals["empty"] += 1
                if not quote:
                    totals["quote_absent"] += 1
                if nums:
                    totals["num_absent"] += 1
                weak = (not quote) or bool(nums) or empty
                if weak:
                    totals["ok_but_weak"] += 1
                print(
                    "STRICT %s:%d %s verdict=OK quote=%s numbers=%s empty=%s frag=%r"
                    % (
                        prose,
                        lineno,
                        m.group(0),
                        "present" if quote else "ABSENT",
                        "ok" if not nums else "ABSENT:" + ",".join(nums),
                        "yes" if empty else "no",
                        frag,
                    )
                )
    print(
        "STRICT_TOTAL locators=%d ok=%d ok_with_absent_quote=%d ok_with_absent_number=%d ok_on_empty_range=%d ok_but_weak=%d"
        % (
            totals["loc"],
            totals["ok"],
            totals["quote_absent"],
            totals["num_absent"],
            totals["empty"],
            totals["ok_but_weak"],
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
