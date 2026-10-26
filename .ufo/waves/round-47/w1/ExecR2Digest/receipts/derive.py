#!/usr/bin/env python3
"""Re-derive the committed out.json summary from out.json.rows.tsv (round-46 ExecStofOracle)."""
import json, sys, collections

tsv, out_json = sys.argv[1], sys.argv[2]
WS = " \t\r\n\v\f"
HYPR_TRIM = " \t\r\n"

raw = open(tsv, "rb").read()
lines = raw.decode("utf-8").split("\n")
print("bytes=%d" % len(raw))
print("newline_terminated=%s" % (raw.endswith(b"\n"),))
print("split_lines=%d" % len(lines))
print("nonempty_lines=%d" % sum(1 for l in lines if l))
header = lines[0]
print("header=%r" % header)
cols = header.split("\t")
print("header_cols=%d %r" % (len(cols), cols))

fieldcount = collections.Counter()
rows = []
for ln, line in enumerate(lines[1:], start=2):
    if not line:
        continue
    f = line.split("\t", 6)
    fieldcount[len(line.split("\t"))] += 1
    rows.append(f)
print("field_count_hist=%r" % (dict(sorted(fieldcount.items())),))
print("data_rows=%d" % len(rows))

print("warn_rows_with_extra_cols=%d" % sum(v for k, v in fieldcount.items() if k != 7))

KIND_OF = {
    "same_value": "ok", "value_ulp_diff": "ok", "other": "ok",
    "ref_refuses_cpp_stores": "unsupported", "ref_refuses_cpp_both_unset": "unsupported",
    "ref_unset_cpp_stores": "unset", "both_unset": "unset",
}

classes = {}
flip_classes = {}
examples = {}
dump_breaks = []
trim_mismatch = 0
roundtrip_fail = 0
cats = set()

for f in rows:
    cat, cls, ref_line, truth_line, ref_printed, truth_printed, text = f
    cats.add(cat)
    line_flip = ref_line != truth_line
    # truth_top: SETUP iff the C++ field was not acceptable JSON (truth_line == SETUP)
    truth_top = "SETUP" if truth_line == "SETUP" else "OK"
    kind = KIND_OF.get(cls)
    if kind is None:
        print("WARN unknown class", cls)
        kind = "?"
    if kind == "unsupported":
        ref_top = "NOT_COMPARED"
    else:
        ref_top = "DIFFER" if ref_line == "DIFFER" else "OK"
    top_flip = ref_top != truth_top
    c = classes.setdefault(cls, {"n": 0, "line_flip": 0, "top_flip": 0})
    c["n"] += 1
    c["line_flip"] += int(line_flip)
    c["top_flip"] += int(top_flip)
    if ref_printed != truth_printed:
        c["print_differs"] = c.get("print_differs", 0) + 1
    if line_flip or top_flip:
        key = "%s|line:%s->%s|top:%s->%s" % (cls, ref_line, truth_line, ref_top, truth_top)
        flip_classes[key] = flip_classes.get(key, 0) + 1
        examples.setdefault(key, (text, ref_printed, truth_printed))
    if truth_line == "SETUP":
        dump_breaks.append((cat, text, truth_printed))
    if text.strip(WS) != text.strip(HYPR_TRIM):
        trim_mismatch += 1
    if truth_line != "SETUP":
        try:
            if "%.2f" % float(truth_printed) != truth_printed:
                roundtrip_fail += 1
        except ValueError:
            print("WARN unparsable truth_printed", repr(truth_printed))

rederived = {
    "cases": len(rows),
    "categories": len(cats),
    "classes": dict(sorted(classes.items())),
    "flips": {"by_class": dict(sorted(flip_classes.items())), "total": sum(flip_classes.values())},
    "examples": {k: list(v) for k, v in sorted(examples.items())},
    "dump_json_breaks": len(dump_breaks),
    "dump_json_break_examples": dump_breaks[:15],
    "trim_mismatch_unverified": trim_mismatch,
    "reported_roundtrip_failures": roundtrip_fail,
}

committed = json.load(open(out_json, encoding="utf-8"))
keys = sorted(set(committed) | set(rederived))
print("\n== rederived vs committed (out.json) ==")
for k in keys:
    a, b = committed.get(k, "<absent>"), rederived.get(k, "<absent>")
    if k == "examples":
        same = (list(a or []) == list(b or [])) if a != "<absent>" and b != "<absent>" else False
        print("examples_equal_nometadata=%s" % (same,))
        if not same:
            for kk in sorted(set(a or {}) | set(b or {})):
                av, bv = (a or {}).get(kk), (b or {}).get(kk)
                if av != bv:
                    # committed carries cpp_bits/cpp_reason beyond our three fields
                    print("  examples diff key=%r committed=%r rederived=%r" % (kk, av, bv))
        continue
    print("%-32s committed=%r rederived=%r equal=%s" % (k, a, b, a == b))

print("\n== classes (rows=%d) ==" % len(rows))
for cls, c in sorted(classes.items()):
    print("%-28s n=%-6d line_flip=%-5d top_flip=%-5d print_differs=%s" % (
        cls, c["n"], c["line_flip"], c["top_flip"], c.get("print_differs", 0)))

print("\n== flips by key (total=%d) ==" % sum(flip_classes.values()))
for k, v in sorted(flip_classes.items()):
    print("%-78s %d" % (k, v))

print("\n== dump_json_breaks=%d ==" % len(dump_breaks))
for b in dump_breaks[:15]:
    print(repr(b))
print("\n== trim_mismatch_unverified=%d roundtrip_fail=%d ==" % (trim_mismatch, roundtrip_fail))
print("\n== categories=%d ==" % len(cats))
print(sorted(cats))
print("\ncat_counts:")
for k, v in sorted(collections.Counter(r[0] for r in rows).items()):
    print("%-24s %d" % (k, v))

if len(sys.argv) > 3:
    json.dump(rederived, open(sys.argv[3], "w"), indent=1, ensure_ascii=False)
