#!/usr/bin/env python3
"""Hand-written receipts for the round-46 C1 contract differential (host hyprlang 0.6.8 vs the reference model).

Section A: divergence classes - configs the reference models (unsupported == 0) whose expected names or scroll
           factor disagree with the host parser, next to the same config's answer from the oracle.
Section B: declined classes - configs the reference counts `unsupported` (NOT_COMPARED) and what the host parser
           actually decides for them.
Section C: the `scroll_factor` float matrix - reference read_float vs std::stof as the host library behaves.

Usage: python3 repro.py <scratch-dir> <oracle-binary>   (writes repro.json next to this file)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

A = {
    # an unknown key inside a device block re-selects by the stale currentSpecialKey, so the rest of the
    # block lands on another device
    "A1-realistic-block-unknown-key": [
        "device[kbd] {\n  kb_layout = de\n}\n",
        "device[mouse] {\n  scroll_factor = 0.5\n}\n",
        "device[kbd]:kb_variant = intl\n",
        "device {\n  name = mouse\n  tap-to-click = 0\n  nope = 1\n  kb_options = compose:caps\n}\n"],
    "A2-flat-selector-unknown-key": [
        "device[kbd] {\n  kb_layout = de\n}\n",
        "device[mouse] {\n  kb_layout = fr\n}\n",
        "device[kbd]:kb_variant = intl\n",
        "device:name = mouse\ndevice:nope = 1\ndevice:kb_options = compose:caps\n"],
    "A3-empty-name-then-selector": [
        "device {\n  name = \n}\ndevice {\n  name = b\n}\ndevice:name = b\ndevice:nope = 1\n"
        "device:kb_options = compose:caps\n"],
    "A4-scroll-retargeted": [
        "device[kbd] {\n  kb_layout = de\n}\n",
        "device[mouse] {\n  kb_layout = fr\n}\n",
        "device[kbd]:kb_variant = intl\n",
        "device {\n  name = mouse\n  nope = 1\n  scroll_factor = 0.5\n}\n"],
    "A9-typo-key-retargets": [
        "device[kbd] {\n  kb_layout = de\n}\n",
        "device[mouse] {\n  kb_layout = fr\n}\n",
        "device[kbd]:kb_variant = intl\n",
        "device {\n  name = mouse\n  tap_to_click = 1\n  kb_options = compose:caps\n}\n"],
    # underflowing scroll_factor: the reference stores 0.0, the host's std::stof throws
    "A5-float-underflow-zero": ["device[mouse]:scroll_factor = 1e-999\n"],
    "A6-float-underflow-50": ["device[mouse]:scroll_factor = 1e-50\n"],
    "A7-float-denormal-40": ["device[mouse]:scroll_factor = 1e-40\n"],
    "A8-float-min-normal": ["device[mouse]:scroll_factor = 1.1754943508222875e-38\n"],
}

B = {
    "B1-directive": ["device[kbd]:kb_layout = de\n# hyprlang if X\ndevice[kbd]:kb_file = /x\n# hyprlang endif\n"],
    "B2-variable": ["$lay = de\ninput:kb_layout = $lay\n"],
    "B3-expression": ["input:kb_layout = {{ 1 + 2 }}\n"],
    "B4-interior-backslash": ["input:kb_options = a\\{b\n"],
    "B5-flat-no-selector": ["device:kb_layout = de\ndevice:kb_file = /x\n"],
    "B6-block-first-not-name": ["device {\n  kb_layout = de\n  name = kbd\n}\n"],
    "B7-rename": ["device {\n  name = a\n  name = kbd\n  kb_layout = de\n}\n"],
    "B8-float-inf": ["device[mouse]:scroll_factor = inf\n"],
    "B9-float-hex": ["device[mouse]:scroll_factor = 0x10\n"],
    "B10-float-nan": ["device[mouse]:scroll_factor = nan\n"],
    "B11-bracket-then-flat": ["device[kbd]:kb_layout = fr\ndevice:kb_file = /x\n"],
    "B12-crossfile-unclosed": ["device {\n  name = kbd\n  kb_layout = de\n", "device:kb_file = /x\n"],
    "B13-selector-then-block": ["device:name = kbd\ndevice {\n  name = kbd2\n  kb_layout = de\n}\n"],
    "B14-crlf-continuation": ["input:kb_model = pc1\\\r\n05\r\n"],
}

FLOATS = ["1e-999", "1e-50", "1e-46", "1e-45", "1e-40", "1.4e-45", "2e-45", "1e-39", "1e-38",
          "1.1754943508222875e-38", "1.1754943e-38", "1e-7", "0", "-0", "-0.0", "0e0", "0.0000",
          "1e38", "3.4e38", "1e39", "1e999", "-1e999", "inf", "-inf", "nan", "0x10", "0X1p3", "5e-39",
          "0.005", "100.005", "2.675", "50.555", "99.999", "250", "-3", "0.7x", "fast", ".5", "5."]

NAMES = ["kbd", "kbd2", "a", "b", "", "mouse"]


def main():
    root, oracle = sys.argv[1], sys.argv[2]
    sys.path.insert(0, HERE)
    import differ

    ref = differ.load_ref()
    os.makedirs(root, exist_ok=True)

    cases = []
    for tag, files in list(A.items()) + list(B.items()):
        cases.append({"id": tag, "files": files, "names": NAMES, "tag": tag})
    for f in FLOATS:
        cases.append({"id": "C" + f, "files": ["device[mouse]:scroll_factor = %s\n" % f], "names": ["mouse"],
                      "tag": "float"})
    out = differ.run_oracle(root, oracle, cases)

    def row(case):
        refm = differ.ref_model(ref, case)
        o = out[case["id"]]
        return {
            "config": case["files"],
            "reference_unsupported": refm["unsupported"],
            "reference_compared": refm["unsupported"] == 0,
            "reference": {n: {"names": list(refm["names"][n]["names"]), "kb_file": refm["names"][n]["kb_file"],
                              "sf": "%.2f" % refm["names"][n]["sf"], "block": refm["names"][n]["block"]}
                          for n in case["names"]},
            "oracle": {n: {"names": [o["names"][n]["layout"], o["names"][n]["variant"], o["names"][n]["options"],
                                     o["names"][n]["model"], o["names"][n]["rules"]],
                           "kb_file": o["names"][n]["kb_file"], "sf": o["names"][n]["sf"],
                           "sf_set": o["names"][n]["sf_set"], "block": o["names"][n]["block"]}
                       for n in case["names"]},
            "oracle_categories": o["categories"],
            "oracle_errors": o["errors"],
            "diverges": differ.compare(refm, o) if refm["unsupported"] == 0 else None,
        }

    result = {"A_and_B": {c["id"]: row(c) for c in cases if not c["id"].startswith("C")},
              "C_floats": {}}
    for c in cases:
        if not c["id"].startswith("C"):
            continue
        r = row(c)
        val = c["id"][1:]
        kind, v = ref.read_float(val)
        r["reference_read_float"] = [kind, v]
        r["host_stof"] = {"sf_set": r["oracle"]["mouse"]["sf_set"], "sf": r["oracle"]["mouse"]["sf"],
                          "sf_raw_printed": out[c["id"]]["names"]["mouse"]["sf_raw"]}
        result["C_floats"][val] = r

    with open(os.path.join(HERE, "repro.json"), "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, ensure_ascii=False)

    print("== A: divergence classes (reference models the config, host parser disagrees)")
    for tag, r in result["A_and_B"].items():
        if not tag.startswith("A"):
            continue
        print("-", tag, "unsupported=%d" % r["reference_unsupported"])
        print("  cfg  ", json.dumps(r["config"]))
        for n in NAMES:
            a, b = r["reference"][n], r["oracle"][n]
            if r["diverges"] and any(d[1] == n for d in r["diverges"]):
                print("   DIVERGES name=%r ref=%s oracle=%s" % (n, a, b))
        print("  categories", r["oracle_categories"], "errors", r["oracle_errors"])
    print("== B: declined classes (reference NOT_COMPARED) and what the host decides")
    for tag, r in result["A_and_B"].items():
        if not tag.startswith("B"):
            continue
        print("-", tag, "reference_unsupported=%d" % r["reference_unsupported"], "categories", r["oracle_categories"])
        for n in NAMES:
            e = r["oracle"][n]
            if e["block"] or e["names"] != ["us", "", "", "", ""] or e["sf_set"]:
                print("   name=%r oracle block=%s names=%s kb_file=%r sf=%s" % (n, e["block"], e["names"],
                                                                                e["kb_file"], e["sf"]))
    print("== C: scroll_factor float matrix (reference read_float vs host std::stof)")
    for val, r in result["C_floats"].items():
        k, v = r["reference_read_float"]
        h = r["host_stof"]
        mark = ""
        if k == "ok" and h["sf_set"] and ("%.2f" % min(max(v, 0.0), 100.0)) != h["sf"]:
            mark = "  <-- DIVERGES"
        if k == "ok" and not h["sf_set"]:
            mark = "  <-- DIVERGES (reference sets 0/value, host leaves unset)"
        if k == "unset" and h["sf_set"]:
            mark = "  <-- DIVERGES (reference unset, host sets)"
        print("  %-24r ref=%-12s %-8s host_set=%-5s host=%s%s" % (val, k, v, h["sf_set"], h["sf"], mark))


if __name__ == "__main__":
    main()
