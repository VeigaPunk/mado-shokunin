#!/usr/bin/env python3
"""Computed evidence for C1/ExecKeysymNames.

Reads receipts/names-diff.txt (the judge sweep) and the pinned src/ks_tables.h,
and prints every number the report cites, so no count is typed by hand.

Checks
  A  every sweep row is OK (judge first stdout line + exit status == keysyms.py)
  B  the 2638 header names: count whose printed canonical name differs from the
     argument text (alias names), and that the printed name is the canonical one
  C  the 2505 distinct values, passed as decimal and as 0x hex: printed name
  D  header sufficiency: canonical == first `#define XKB_KEY_<name>` per value
     reproduces src/ks_tables.h keysym_to_name[] with zero mismatches, and the
     header defines exactly the 2638 names of name_to_keysym[]
"""

import importlib.util
import os
import re
import sys

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/ExecKeysymNames"
RECEIPTS = os.path.join(SEAT, "receipts")

spec = importlib.util.spec_from_file_location("keysyms", os.path.join(SEAT, "keysyms.py"))
keysyms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(keysyms)


def rows():
    out = []
    with open(os.path.join(RECEIPTS, "names-diff.txt"), encoding="utf-8") as fd:
        for line in fd:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            out.append(parts)
    return out


def ks_tables():
    text = open(os.path.join(SEAT, "src_ks_tables.h"), encoding="utf-8", errors="replace").read()

    def sect(name):
        i = text.index("static const struct name_keysym %s[] = {" % name)
        j = text.index("};", i)
        return text[i:j]

    pat = re.compile(r"\{ (0x[0-9a-f]{8}), (\d+) \}, /\* (.*?) \*/")
    n2k = {n: int(v, 16) for v, _o, n in pat.findall(sect("name_to_keysym"))}
    k2n = {int(v, 16): n for v, _o, n in pat.findall(sect("keysym_to_name"))}
    return n2k, k2n


def main():
    rs = rows()
    fails = [r for r in rs if r[0] != "OK"]
    accept = [r for r in rs if r[1] == "0"]
    refuse = [r for r in rs if r[1] == "2"]
    print("A sweep_rows=%d ok=%d fail=%d accept_rc0=%d refuse_rc2=%d"
          % (len(rs), len(rs) - len(fails), len(fails), len(accept), len(refuse)))
    print("A judge_stdout_empty_on_all_refusals=%s"
          % all(r[3] == "-" for r in refuse))

    by_arg = {}
    for r in rs:
        by_arg.setdefault(r[5], []).append(r)

    names = keysyms._NAMES
    alias = []
    refused_names = []
    for name in names:
        r = by_arg.get(name)
        assert r, name
        printed = r[0][3]
        if r[0][1] == "2":                 # 0x0000 NoSymbol: not expressible
            refused_names.append(name)
            continue
        prefix = "keysym: "
        printed = printed[len(prefix):].split(" (0x")[0] if printed.startswith(prefix) else printed
        if printed != name:
            alias.append((name, printed))
    print("B header_names=%d refused_names=%s printed_other_canonical=%d"
          % (len(names), refused_names, len(alias)))
    print("B sample_alias=%s" % (alias[:6],))

    bad_value = []
    unexpressible = []
    for val, canon in keysyms._CANON.items():
        if val == 0:                       # 0x0000 == NoSymbol == "no keysym"
            unexpressible.append((str(val), by_arg[str(val)][0][3],
                                  "0x%x" % val, by_arg["0x%x" % val][0][1]))
            continue
        for form in (str(val), "0x%x" % val):
            r = by_arg.get(form)
            if not r:
                bad_value.append((form, "missing"))
                continue
            printed = r[0][3]
            if printed != "keysym: %s (0x%04x)" % (canon, val):
                bad_value.append((form, printed))
    print("C value_forms_checked=%d mismatched=%d unexpressible_zero=%s"
          % (2 * (len(keysyms._CANON) - 1), len(bad_value), unexpressible))

    n2k, k2n = ks_tables()
    print("D ks_tables name_to_keysym=%d keysym_to_name=%d" % (len(n2k), len(k2n)))
    print("D header_derived_names_equal=%s values_equal=%s canonical_equal=%s"
          % (keysyms._NAMES == n2k, keysyms._CANON == k2n, keysyms._CANON == k2n))
    only_ks = sorted(set(n2k) - set(keysyms._NAMES))
    only_hdr = sorted(set(keysyms._NAMES) - set(n2k))
    print("D names_only_in_ks_tables=%d names_only_in_header=%d" % (len(only_ks), len(only_hdr)))
    bad = len(fails) + len(bad_value) + len(only_ks) + len(only_hdr) + len(refused_names) - 1 + \
        (0 if keysyms._CANON == k2n else 1)
    print("RESULT %s" % ("PASS" if bad == 0 else "FAIL"))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
