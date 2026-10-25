#!/usr/bin/env python3
"""Naive-run reconstruction for seat RevengerNaiveMismatch (round 40 w1).

Reproduces the "naive" run of the BASE tool:
  1. take the frozen native capture `.ufo/waves/round-40/c1/native-capture.jsonl`
     (exactly the 70 declared keys; `{"option":K,"set":B,"<form>":V}`);
  2. normalise each native reply to the base `--getoption` JSON format
     (`{key: {"value": <text>, "custom_type": <form>, "set": B}}`) by taking the
     value's literal text (no hyprlang conversion);
  3. run the BASE tool (`tools/mado-options.py`, byte-identical to the base commit
     9fc511d) with `--home /home/vgpnk --getoption <file>`;
  4. count/classify the `mismatch` rows.

Reference side (what the converter reports) is re-derived with the frozen counter's
model functions, plus the angle-inheritance state per key from the throwaway
reference resolver (`ctl-ref-tool.py.txt`), cross-checked against the w1 host
census (`RevHostCensus/census.jsonl`).
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
CAP = os.path.join(LANE, ".ufo/waves/round-40/c1/native-capture.jsonl")
REFTOOL = os.path.join(LANE, ".ufo/waves/round-40/c1/ctl-ref-tool.py.txt")
CENSUS = os.path.join(LANE, ".ufo/waves/round-40/w1/RevHostCensus/census.jsonl")
TOOL = os.path.join(LANE, "tools/mado-options.py")
HOME = "/home/vgpnk"
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- reference model from the frozen counter (import, no execution of main) ----
spec = importlib.util.spec_from_file_location(
    "c1_r40_live", os.path.join(LANE, "quality/counters/c1-r40-live.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
WEIGHTS = mod.WEIGHTS

import importlib.machinery
_rt_loader = importlib.machinery.SourceFileLoader("reftool", REFTOOL)
rtspec = importlib.util.spec_from_loader("reftool", _rt_loader)
rt = importlib.util.module_from_spec(rtspec)
_rt_loader.exec_module(rt)
ST = rt.State(HOME)
rt.parse_file(os.path.join(HOME, ".config/hypr/hyprland.conf"), ST)


def custom_shape(live):
    s = live.strip()
    toks = s.split()
    if toks and toks[-1].endswith("deg"):
        return "gradient"
    if toks and all(re.fullmatch(r"-?\d+", t) for t in toks):
        if len(toks) == 1:
            return "weight"
        if len(toks) <= 4:
            return "gap"
    return None


def ref_convert(key, form, declared, live):
    """Reference conversion -> (text, ok) using the counter model + inheritance."""
    d = declared.strip()
    inh = ST.options.get(key, {}).get("_angle", 0)
    if form == "int":
        c = mod.hl_int(d)
        return (None if c is None else str(c)), (c is not None and c == live)
    if form == "float":
        try:
            return str(float(d)), abs(float(d) - float(live)) < 1e-6
        except ValueError:
            return None, False
    if form == "str":
        return d, d == str(live).strip()
    shape = custom_shape(live)
    if shape == "gradient":
        t = mod.gradient_text(d, inherited=inh)
        return t, (t is not None and t == live)
    if shape == "gap":
        try:
            t = mod.gap_text(d)
        except ValueError:
            return None, False
        return t, t == live
    if shape == "weight":
        t = str(WEIGHTS.get(d.lower(), -1))
        return t, t == live
    return d, d == live


def classify(key, form, declared, live):
    tags = []
    dl = declared.lower()
    o = ST.options.get(key, {})
    decls = o.get("_decls", 1)
    angle = o.get("_angle", 0)
    if form == "int":
        if dl.startswith(("0x", "rgb(", "rgba(", "#")):
            tags.append("int-colour form")
        else:
            tags.append("bool prose")
    elif form == "custom":
        decl_has_deg = bool(re.search(r"\d+\s*deg", declared))
        colourish = dl.startswith(("0x", "rgb(", "rgba(", "#"))
        if colourish:
            tags.append("colour rgb/rgba vs ARGB")
        if not decl_has_deg and decls > 1 and angle > 0:
            tags.append("gradient angle (inherited)")
        if not colourish and re.fullmatch(r"-?\d+", live.strip()) and \
           not re.fullmatch(r"-?\d+", declared.strip()):
            tags.append("weight name")
        if not tags:
            tags.append("custom grammar")
    else:
        tags.append("str exact")
    return "|".join(tags)


def native_rec(line):
    rec = json.loads(line)
    key = rec["option"]
    form = next((f for f in ("int", "float", "str", "custom") if f in rec), None)
    assert form is not None, line
    return key, form, rec[form], bool(rec["set"])


def main():
    rows = []
    with open(CAP) as fh:
        for line in fh:
            if not line.strip():
                continue
            rows.append(native_rec(line))
    print("capture rows:", len(rows))
    forms = {}
    naive = {}
    for key, form, val, isset in rows:
        forms[form] = forms.get(form, 0) + 1
        if form == "int":
            text = str(val)
        elif form == "float":
            text = str(float(val))
        else:
            text = str(val)
        naive[key] = {"value": text, "custom_type": form, "set": isset}
    print("forms:", forms)
    naive_path = os.path.join(HERE, "naive.json")
    with open(naive_path, "w") as fh:
        json.dump(naive, fh, indent=1, sort_keys=True)

    p = subprocess.run([sys.executable, "-I", TOOL, "--home", HOME,
                         "--getoption", naive_path],
                        capture_output=True, text=True)
    print("base tool rc:", p.returncode)
    if p.returncode != 0:
        print(p.stderr)
        return 1
    base_rows = json.loads(p.stdout)
    assert len(base_rows) == 70, len(base_rows)
    base = {r["key"]: r for r in base_rows}

    # reference labels
    ref = {key: ref_convert(key, form, base[key]["value"], val)
           for key, form, val, isset in rows}

    mism = []
    agree = 0
    astar = 0
    for r in base_rows:
        lab = r["agreement"]
        if lab == "mismatch":
            mism.append(r["key"])
        elif lab == "agreement*":
            astar += 1
        else:
            agree += 1
    print("base naive labels: agreement=%d agreement*=%d mismatch=%d"
          % (agree, astar, len(mism)))

    out = []
    for key in sorted(mism):
        r = base[key]
        form = naive[key]["custom_type"]
        live = naive[key]["value"]
        conv, refok = ref[key]
        o = ST.options.get(key, {})
        out.append((key, form, r["value"], live, conv, refok,
                    classify(key, form, r["value"], live),
                    o.get("_decls", 1), o.get("_angle", 0),
                    r["layer"], r["owner"], r["line"]))
    with open(os.path.join(HERE, "mismatch.tsv"), "w") as fh:
        fh.write("key\tform\tdeclared\tnaive_live\tconverted\tref_ok\tcause"
                 "\tdecls\tinherited_angle\tlayer\towner\tline\n")
        for t in out:
            fh.write("\t".join(str(x) for x in t) + "\n")
    for t in out:
        print("MISMATCH\t" + "\t".join(str(x) for x in t))

    with open(os.path.join(HERE, "labels.tsv"), "w") as fh:
        fh.write("key\tform\tdeclared\tnaive_live\tconverted\tbase_label"
                 "\tref_ok\tcause\tdecls\tinherited_angle\n")
        for key in sorted(base):
            r = base[key]
            form = naive[key]["custom_type"]
            live = naive[key]["value"]
            conv, refok = ref[key]
            o = ST.options.get(key, {})
            cause = classify(key, form, r["value"], live) \
                if r["agreement"] == "mismatch" else ""
            fh.write("\t".join(str(x) for x in (
                key, form, r["value"], live, conv, r["agreement"], refok,
                cause, o.get("_decls", 1), o.get("_angle", 0))) + "\n")

    # cross-check the reference side against the w1 host census
    census = json.load(open(CENSUS))
    cmap = {c["key"]: c for c in census}
    xconv = xlab = 0
    for key, form, val, isset in rows:
        conv, ok = ref[key]
        c = cmap.get(key)
        if c is None:
            continue
        if str(conv) == str(c.get("converted")):
            xconv += 1
        reflab = "agreement" if (ok and isset) else "mismatch"
        if c.get("agreement") in (reflab, "agreement*"):
            xlab += 1
    print("census cross-check: converted agree=%d/70 label agree=%d/70"
          % (xconv, xlab))
    print("mismatch count:", len(mism))
    return 0


if __name__ == "__main__":
    sys.exit(main())
