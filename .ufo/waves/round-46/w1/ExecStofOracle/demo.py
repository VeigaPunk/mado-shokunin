#!/usr/bin/env python3
"""demo.py — run the pinned reference CLI on synthetic scenarios, one per divergence class.

For each row: the config sets `device[name]:scroll_factor = <value>`; the dump carries the
mouse field text that Hyprland 0.56.2 really prints for that value (computed by stmt.cpp).
Prints the reference's MADO_DEV_MOUSE line, its summary line and exit code, plus the truth.

    python3 -I demo.py <stmt-binary> <reference.py>
"""
import json
import subprocess
import sys

STMT, REF = sys.argv[1], sys.argv[2]

CASES = [
    # label, config value, note
    ("plain-2dp",              "0.50",   "ordinary decimal: both sides agree"),
    ("half3",                  "2.675",  "third-decimal half: both round the same float"),
    ("dblround-below-mid",     "0.00500000012107193470001220703124999999999999999999",
                                       "49-digit decimal on a float32 midpoint"),
    ("dblround-above-mid",     "0.00500000012107193470001220703125000000000000000000001",
                                       "same midpoint, other side"),
    ("underflow-to-zero",      "1e-50",  "f32 underflows to 0.0; std::stof throws"),
    ("subnormal",              "1e-40",  "subnormal: both refuse"),
    ("overflow",               "1e39",   "float overflow: both refuse"),
    ("hex",                    "0x10",   "strtof hex float -> 16.0"),
    ("inf",                    "inf",    "strtof inf -> clamp 100"),
    ("nan",                    "nan",    "strtof nan -> JSON field breaks"),
    ("fltmin-boundary",        "1.17549435e-38", "decimal just below FLT_MIN"),
]


def stmt_field(value):
    out = subprocess.run([STMT], input=(value + "\n").encode(), capture_output=True, check=True)
    status, mid, printed = out.stdout.decode().rstrip("\n").split("\t")
    return printed if status == "SET" else "-1.00"


def main():
    print("%-20s %-8s %-30s %s" % ("case", "truth", "reference mouse line", "reference summary"))
    for label, value, note in CASES:
        field = stmt_field(value)
        dump = json.dumps({
            "mice": [{"address": "0x1", "name": "m", "defaultSpeed": 0.0, "scrollFactor": 0}],
            "keyboards": [{"address": "0x2", "name": "k", "layout": "us", "variant": "",
                           "options": "", "model": "", "rules": ""}],
        })
        # splice the exact field text (json.dumps would quote/normalise it)
        dump = dump.replace('"scrollFactor": 0', '"scrollFactor": ' + field)
        cfg = "device {\n  name = m\n  scroll_factor = %s\n}\n" % value
        with open("/tmp/_demo_cfg.conf", "w") as fh:
            fh.write(cfg)
        with open("/tmp/_demo_dump.json", "w") as fh:
            fh.write(dump)
        p = subprocess.run([sys.executable, "-I", REF, "--devices", "/tmp/_demo_dump.json",
                            "--config", "/tmp/_demo_cfg.conf"], capture_output=True)
        out = p.stdout.decode().strip().splitlines()
        mouse = next((l for l in out if l.startswith("MADO_DEV_MOUSE")), "")
        summ = out[-1] if out else ""
        print("%-20s %-8s %s" % (label, field, mouse.split("verdict=")[-1] if mouse else summ))
        print("   cfg scroll_factor = %s   %s" % (value, note))
        print("   %s" % (summ if summ.startswith("MADO_DEVICES") else summ))
        if p.returncode != 0:
            print("   rc=%d stdout=%r" % (p.returncode, out))


if __name__ == "__main__":
    main()
