#!/usr/bin/env python3
"""ExecR2Check (round 47, w2) — independent re-derivation of every number in
.ufo/waves/round-47/w1/ExecR2Digest/digest.md.

The described source file is absent: the round-47 L1 removed it at 19:16:55
(receipt .ufo/waves/round-47/receipts/r2-removed.txt). The bytes are therefore
reproduced from the committed pipeline (gen.py + stmt.cpp + diff.py +
round-46/l1-draft/mado-devices.py) and every number is re-derived from that
reproduction plus the surviving committed out.json.

usage: python3 -I verify.py <repro-rows.tsv> <committed-out.json>

Writes only to stdout. No hardcoded /tmp; caller supplies paths.
"""
import hashlib
import json
import struct
import sys
from collections import Counter, OrderedDict

WS = " \t\r\n\v\f"
HYPR_TRIM = " \t\r\n"
HEADER = "cat\tcls\tref_line\ttruth_line\tref_printed\ttruth_printed\ttext"
KIND = {  # diff.py:139-150 class assignment is a bijection on kind x cpp_set
    "same_value": "ok", "value_ulp_diff": "ok", "other": "ok",
    "ref_refuses_cpp_stores": "unsupported", "ref_refuses_cpp_both_unset": "unsupported",
    "ref_unset_cpp_stores": "unset", "both_unset": "unset",
}
CLAIM_CLASSES = {  # digest.md §2 table (n, line_flip, top_flip, print_differs)
    "same_value": (55229, 0, 0, 0),
    "value_ulp_diff": (2751, 2751, 2751, 2751),
    "both_unset": (1294, 0, 0, 0),
    "ref_refuses_cpp_both_unset": (64, 0, 64, 0),
    "ref_refuses_cpp_stores": (37, 29, 37, 37),
    "other": (19, 19, 19, 19),
}
CLAIM_CATS = OrderedDict([
    ("dec1", 3051), ("dec2", 6101), ("dec3", 2227), ("dec4", 1200), ("dec5", 1200),
    ("dec6", 1200), ("dec7", 1200), ("half3", 30501), ("half3r", 1017), ("prefix", 306),
    ("exp", 309), ("subnormal", 22), ("hex", 14), ("nonfinite", 20), ("ws", 15),
    ("longdigits", 7), ("dblround_above", 3000), ("dblround_at", 3000),
    ("dblround_below", 3000), ("dblround_hand", 4), ("junk", 2000),
])
CLAIM_TAB_LINES = [47945, 47946, 47947, 47948, 47949, 48373, 48374, 48375]
CLAIM_TAB_TEXT = ["\t5", "\t5.", "\t.5", "\t5.0", "\t0.25", "\t0.5", "0.5\t", "\t\t0.5\t"]
CLAIM_NBSP_LINES = [47718, 47739, 47760, 47781, 47802, 47823, 47844, 47865, 47886,
                    47907, 47928]
CLAIM_SHA = "6573f76b5a61c6d0270ae4bfb9b3f37d7e95825c6fbfb13858a78fe54d6d3238"
CLAIM_BYTES = 3282451
CLAIM_LINES = 59395

fails = []
def check(name, got, want):
    ok = got == want
    print("%-6s %-52s got=%r want=%r" % ("OK" if ok else "WRONG", name, got, want))
    if not ok:
        fails.append(name)
    return ok


def unesc_tsv(text):
    """gen.py esc(): '\\t' -> tab, '\\\\' -> backslash."""
    out, i = [], 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text) and text[i + 1] in "t\\":
            out.append("\t" if text[i + 1] == "t" else "\\")
            i += 2
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def f32bits(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]


def main():
    rows_path, outjson_path = sys.argv[1], sys.argv[2]
    raw = open(rows_path, "rb").read()
    print("== A. file identity")
    check("sha256", hashlib.sha256(raw).hexdigest(), CLAIM_SHA)
    check("bytes", len(raw), CLAIM_BYTES)
    check("trailing newline", raw.endswith(b"\n"), True)
    check("CR count", raw.count(b"\r"), 0)
    lines = raw.split(b"\n")
    check("wc-l (LF lines)", raw.count(b"\n"), CLAIM_LINES)
    check("split record count (incl trailing empty)", len(lines), CLAIM_LINES + 1)
    recs = lines[:-1]
    try:
        recs_s = [r.decode("utf-8") for r in recs]
        utf8 = True
    except UnicodeDecodeError as exc:
        recs_s, utf8 = [], exc
    check("utf-8 decodes", utf8, True)
    check("header line exact bytes", recs[0].decode("utf-8"), HEADER)
    data = recs_s[1:]
    check("data rows", len(data), 59394)

    longest = max(range(1, len(recs) + 1), key=lambda n: len(recs[n - 1]))
    check("longest line number", longest, 49142)
    check("longest line bytes", len(recs[longest - 1]), 108)

    print("\n== B. parse (split maxsplit 6), tab rows, NBSP rows")
    parsed = []
    bad = 0
    for n, line in enumerate(data, start=2):
        f = line.split("\t", 6)
        if len(f) != 7:
            bad += 1
        parsed.append(f)
    check("rows not splitting into 7 fields with maxsplit 6", bad, 0)
    tabs = [n for n, line in enumerate(data, start=2) if line.count("\t") > 6]
    check("rows with literal tab inside text", len(tabs), 8)
    check("their line numbers", tabs, CLAIM_TAB_LINES)
    check("their text fields", [parsed[n - 2][6] for n in tabs], CLAIM_TAB_TEXT)
    nf = Counter(len(line.split("\t")) for line in data)
    check("naive-split NF histogram of tab rows",
          [len(data[n - 2].split("\t")) for n in tabs],
          [8, 8, 8, 8, 8, 8, 8, 10])
    nbsp = [n for n, line in enumerate(data, start=2) if "\u00a0" in line]
    check("rows carrying U+00A0", len(nbsp), 11)
    check("their line numbers", nbsp, CLAIM_NBSP_LINES)
    check("all NBSP rows are category prefix",
          sorted({parsed[n - 2][0] for n in nbsp}), ["prefix"])
    check("columns 1-6 equal on maxsplit-6 vs naive split for tab rows",
          all(parsed[n - 2][:6] == data[n - 2].split("\t")[:6] for n in tabs), True)

    print("\n== C. class / flip re-derivation from the TSV alone")
    classes = {}
    flips = Counter()
    examples = {}
    bycls_print = Counter()
    for f in parsed:
        cat, cls, ref_line, truth_line, ref_printed, truth_printed, text = f
        kind = KIND[cls]
        broken = truth_line == "SETUP"
        truth_top = "SETUP" if broken else "OK"
        ref_top = "NOT_COMPARED" if kind == "unsupported" else (
            "DIFFER" if ref_line == "DIFFER" else "OK")
        line_flip = ref_line != truth_line
        top_flip = ref_top != truth_top
        c = classes.setdefault(cls, {"n": 0, "line_flip": 0, "top_flip": 0})
        c["n"] += 1
        c["line_flip"] += int(line_flip)
        c["top_flip"] += int(top_flip)
        if ref_printed != truth_printed:
            c["print_differs"] = c.get("print_differs", 0) + 1
            bycls_print[cls] += 1
        if line_flip or top_flip:
            flips["%s|line:%s->%s|top:%s->%s" % (cls, ref_line, truth_line, ref_top,
                                                 truth_top)] += 1
            examples.setdefault(
                "%s|line:%s->%s|top:%s->%s" % (cls, ref_line, truth_line, ref_top, truth_top),
                [text, ref_printed, truth_printed])
        if broken:
            pass
    for cls, want in sorted(CLAIM_CLASSES.items()):
        got = classes.get(cls)
        g = (got["n"], got["line_flip"], got["top_flip"], got.get("print_differs", 0)) if got else None
        check("class %s (n,line,top,print)" % cls, g, want)
    check("class set", sorted(classes), sorted(CLAIM_CLASSES))
    check("total failed" if False else "sum n", sum(c["n"] for c in classes.values()), 59394)
    check("sum line_flip", sum(c["line_flip"] for c in classes.values()), 2799)
    check("sum top_flip", sum(c["top_flip"] for c in classes.values()), 2871)
    check("sum print_differs", sum(c.get("print_differs", 0) for c in classes.values()), 2807)

    committed = json.load(open(outjson_path, encoding="utf-8"))
    print("\n== D. equality with committed out.json")
    check("classes dict identical (keys incl. absent print_differs)",
          classes, committed["classes"])
    check("flips.by_class identical", dict(flips), committed["flips"]["by_class"])
    check("flips.total", sum(flips.values()), 2871)
    check("flips.total == committed", sum(flips.values()), committed["flips"]["total"])
    ex_first3 = {k: v[:3] for k, v in committed["examples"].items()}
    check("examples keys identical", sorted(examples), sorted(ex_first3))
    check("examples first 3 fields identical", examples, ex_first3)
    check("committed example tuple lengths", sorted({len(v) for v in committed["examples"].values()}), [5])
    check("committed cpp_bits of value_ulp_diff example",
          committed["examples"]["value_ulp_diff|line:DIFFER->AGREE|top:DIFFER->OK"][3],
          1000593163)
    broken_rows = [f for f in parsed if f[3] == "SETUP"]
    check("rows with truth_line SETUP (dump_json_breaks)", len(broken_rows), 8)
    check("dump_json_breaks committed", committed["dump_json_breaks"], 8)
    check("dump_json_break_examples committed",
          committed["dump_json_break_examples"],
          [[f[0], f[6], f[5]] for f in broken_rows])
    trim = sum(1 for f in parsed if f[6].strip(WS) != f[6].strip(HYPR_TRIM))
    check("trim_mismatch_unverified re-derived", trim, 4)
    check("trim_mismatch_unverified committed", committed["trim_mismatch_unverified"], 4)
    rt = 0
    for f in parsed:
        if f[3] == "SETUP":
            continue
        try:
            if "%.2f" % float(f[5]) != f[5]:
                rt += 1
        except ValueError:
            rt += 1
    check("reported_roundtrip_failures re-derived", rt, 0)
    check("reported_roundtrip_failures committed",
          committed["reported_roundtrip_failures"], 0)
    check("committed cases", committed["cases"], 59394)
    check("committed categories", committed["categories"], 21)
    check("committed top-level key order",
          ",".join(committed),
          "cases,categories,classes,flips,examples,dump_json_breaks,"
          "dump_json_break_examples,trim_mismatch_unverified,reported_roundtrip_failures")

    print("\n== E. category column")
    order = []
    counts = Counter()
    for f in parsed:
        if f[0] not in counts:
            order.append(f[0])
        counts[f[0]] += 1
    check("category count", len(counts), 21)
    check("category counts identical to digest", dict(counts), dict(CLAIM_CATS))
    check("category first-appearance order", order, list(CLAIM_CATS))
    pos = {}
    for n, f in enumerate(parsed, start=2):
        pos.setdefault(f[0], []).append(n)
    runs = {c: 1 + sum(1 for a, b in zip(v, v[1:]) if b != a + 1) for c, v in pos.items()}
    check("categories that are one contiguous block",
          sorted(c for c, r in runs.items() if r == 1),
          sorted(c for c in CLAIM_CATS if c not in
                 ("dblround_above", "dblround_at", "dblround_below")))
    check("number of single-block categories",
          sum(1 for r in runs.values() if r == 1), 16)
    check("non-contiguous categories",
          sorted(c for c, r in runs.items() if r > 1),
          ["dblround_above", "dblround_at", "dblround_below"])
    check("first dblround_above line", pos["dblround_above"][0], 48392)
    check("last dblround_below line", pos["dblround_below"][-1], 57391)
    check("dblround triple period 3",
          pos["dblround_at"][0] == pos["dblround_above"][0] + 1 and
          pos["dblround_below"][0] == pos["dblround_above"][0] + 2, True)
    check("dblround_hand span", (pos["dblround_hand"][0], pos["dblround_hand"][-1]),
          (57392, 57395))
    check("junk span", (pos["junk"][0], pos["junk"][-1]), (57396, 59395))

    print("\n== F. row order vs cases.tsv")
    cases = []
    for line in open(sys.argv[3] if len(sys.argv) > 3 else "/dev/null", encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            continue
        _i, _cat, text = line.split("\t", 2)
        cases.append(_cat + "\x00" + "".join(unesc_tsv(text)))
    seq = [f[0] + "\x00" + f[6] for f in parsed]
    check("TSV row order == cases.tsv order", seq == cases, True)

    print("\n== G. awk cross-check of cls column")
    print("   (computed in python: column 2 counts)")
    check("col2 counts", dict(Counter(f[1] for f in parsed)),
          {k: v[0] for k, v in CLAIM_CLASSES.items()})

    print("\nRESULT: %d checks failed %s" % (len(fails), fails if fails else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
