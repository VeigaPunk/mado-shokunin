#!/usr/bin/env python3
"""diff.py — differential test of the scroll-factor arithmetic.

    python3 -I diff.py <cases.tsv> <stmt-binary> <reference.py> [out.json]

Each side receives exactly the text its own pipeline would hand to the parser:

  C++      hyprlang-config.cpp:719 (`RHS = trim(line.substr(equalsPos + 1))`) then
           hyprlang-config.cpp:465-472 `std::stof(value)` -> on exception setError and
           m_bSetByUser stays false; Hyprland-InputManager.cpp:1379-1383 stores
           std::clamp(value, 0.F, 100.F) in optional<float> only when the key was set;
           Hyprland-HyprCtl.cpp:765-772 prints std::format("{:.2f}", value_or(-1)).
  ref      mado-devices.py parse_config `rhs = line[eq+1:].strip(WS)` then read_float()
           (SPECIAL_RE refusal / FLOAT_RE prefix / float() -> f32() double rounding /
           underflow+overflow refusal), expectation min(max(v,0),100) else -1.0,
           comparison and printing with "%.2f".

Both sides then meet at the *dump*: Hyprland prints the stored float with "{:.2f}", the
reference parses that JSON number back and compares two "%.2f" strings.  `truth` is the
verdict a tool would reach if it knew what Hyprland really stored and printed.
"""
import importlib.util
import json as jsonmod
import math
import struct
import subprocess
import sys

WS = " \t\r\n\v\f"
HYPR_TRIM = " \t\r\n"          # hyprlang's trim() lives in a header we do not have; see report


def unesc(text):
    out, i = [], 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text) and text[i + 1] in "t\\":
            out.append("\t" if text[i + 1] == "t" else "\\")
            i += 2
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def load_reference(path):
    spec = importlib.util.spec_from_file_location("mado_devices_ref", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def f32bits(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]


def main():
    cases_path, stmt_bin, ref_path = sys.argv[1], sys.argv[2], sys.argv[3]
    out_path = sys.argv[4] if len(sys.argv) > 4 else None
    ref = load_reference(ref_path)

    cases = []
    with open(cases_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            i, cat, text = line.split("\t", 2)
            cases.append((int(i), cat, unesc(text)))

    # ---- C++ side ------------------------------------------------------------
    cpp_inputs = [t.strip(HYPR_TRIM) for _, _, t in cases]
    proc = subprocess.run([stmt_bin], input="".join(t + "\n" for t in cpp_inputs).encode(),
                          capture_output=True, check=True)
    cpp_rows = proc.stdout.decode().splitlines()
    assert len(cpp_rows) == len(cases), (len(cpp_rows), len(cases))

    classes = {}
    flip_classes = {}
    examples = {}
    dump_breaks = []
    trim_mismatch = 0
    roundtrip_fail = 0
    rows = []

    for (i, cat, text), cpp_text, row in zip(cases, cpp_inputs, cpp_rows):
        status, mid, printed = row.split("\t")
        cpp_set = status == "SET"
        cpp_bits = int(mid, 16) if cpp_set else None
        cpp_val = struct.unpack("<f", struct.pack("<I", cpp_bits))[0] if cpp_set else None
        cpp_reason = None if cpp_set else mid

        ref_text = text.strip(WS)
        if ref_text != cpp_text:
            trim_mismatch += 1
        kind, ref_raw = ref.read_float(ref_text)

        # reference expectation (mado-devices.py report(), mice loop)
        if kind == "ok":
            exp = min(max(ref_raw, 0.0), 100.0)
            ref_set = True
        else:
            exp = -1.0
            ref_set = False

        # what Hyprland really stores and prints for `device[name]:scroll_factor = text`
        real_field = printed if cpp_set else "-1.00"
        # is the emitted field text acceptable to a strict JSON parser? (HyprCtl pastes it raw)
        try:
            jsonmod.loads('{"scrollFactor": %s}' % real_field)
            broken = False
        except ValueError:
            broken = True                                  # std::format prints nan / -nan here

        # the reference reads the field back as a JSON number
        if broken:
            ref_reported = None                            # json.loads -> SETUP bad_json
        else:
            ref_reported = float(real_field)
            # the reference re-prints the reported number: must be the same 2-dp string
            if "%.2f" % ref_reported != real_field:
                roundtrip_fail += 1

        if kind == "unsupported":
            ref_top = "NOT_COMPARED"
        if ref_reported is None:
            ref_line = "SETUP"
            ref_printed = "SETUP"
        else:
            ref_printed = "%.2f" % exp
            ref_line = "AGREE" if "%.2f" % ref_reported == ref_printed else "DIFFER"
        if kind != "unsupported":
            ref_top = "DIFFER" if ref_line == "DIFFER" else "OK"

        truth_line = "SETUP" if broken else "AGREE"
        truth_top = "SETUP" if broken else "OK"
        truth_printed = real_field

        # ---- classify the parse/value outcome --------------------------------
        if kind == "ok" and cpp_set:
            cls = "same_value" if cpp_bits == f32bits(exp) else "value_ulp_diff"
        elif kind == "unsupported" and cpp_set:
            cls = "ref_refuses_cpp_stores"
        elif kind == "unsupported" and not cpp_set:
            cls = "ref_refuses_cpp_both_unset"
        elif kind == "unset" and cpp_set:
            cls = "ref_unset_cpp_stores"
        elif kind == "unset" and not cpp_set:
            cls = "both_unset"
        else:
            cls = "other"

        line_flip = ref_line != truth_line
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
            examples.setdefault(key, (text, ref_printed, truth_printed, cpp_bits, cpp_reason))
        if broken:
            dump_breaks.append((cat, text, real_field))
        rows.append({"cat": cat, "text": text, "cls": cls, "ref_line": ref_line,
                     "truth_line": truth_line, "ref_printed": ref_printed,
                     "truth_printed": truth_printed, "kind": kind})

    result = {
        "cases": len(cases),
        "categories": len({c for _, c, _ in cases}),
        "classes": dict(sorted(classes.items())),
        "flips": {"by_class": dict(sorted(flip_classes.items())),
                  "total": sum(flip_classes.values())},
        "examples": {k: list(v) for k, v in sorted(examples.items())},
        "dump_json_breaks": len(dump_breaks),
        "dump_json_break_examples": dump_breaks[:15],
        "trim_mismatch_unverified": trim_mismatch,
        "reported_roundtrip_failures": roundtrip_fail,
    }
    print(jsonmod.dumps(result, indent=1, default=str))
    if out_path:
        with open(out_path, "w", encoding="utf-8") as fh:
            jsonmod.dump(result, fh, indent=1, default=str)
        with open(out_path + ".rows.tsv", "w", encoding="utf-8") as fh:
            fh.write("cat\tcls\tref_line\ttruth_line\tref_printed\ttruth_printed\ttext\n")
            for r in rows:
                fh.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                    r["cat"], r["cls"], r["ref_line"], r["truth_line"],
                    r["ref_printed"], r["truth_printed"], r["text"]))


if __name__ == "__main__":
    main()
