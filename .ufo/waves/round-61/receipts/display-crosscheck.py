#!/usr/bin/env python3
"""display-crosscheck.py — mado r61 crosscheck receipt producer.

Compares the round's two independently executed artifacts on the five stable
fields they share:
  - the C2 probe (.ufo/waves/round-61/receipts/display-probe-run1.txt), whose
    topology half is the MANAGED System.Windows.Forms.Screen layer, and
  - the C3 tool (tools/mado-win-display.py, live receipt
    windisplay-live-run1.txt), whose topology half is the NATIVE
    EnumDisplayMonitors/GetMonitorInfoW path.

Reads the two committed receipt files only; writes nothing; prints one
MADO_DISPLAY_CROSSCHECK line; exit 0 iff all five fields agree.
"""
from __future__ import annotations

import json
import sys

HERE = ".ufo/waves/round-61/receipts"


def load_probe(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.loads(handle.read())


def load_tool(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        lines = [line for line in handle.read().splitlines() if line.strip()]
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("{"):
            return json.loads(stripped)
    raise SystemExit(f"no JSON object line in {path}")


def primary(doc: dict) -> dict:
    for mon in doc["monitors"]:
        if mon.get("primary") is True:
            return mon
    raise SystemExit("no primary monitor in document")


def main() -> int:
    probe = load_probe(f"{HERE}/display-probe-run1.txt")
    tool = load_tool(f"{HERE}/windisplay-live-run1.txt")
    pmon, tmon = primary(probe), primary(tool)
    checks = []
    checks.append(("monitor_count", probe["monitor_count"] == len(tool["monitors"])))
    checks.append(("primary_device", pmon["device"] == tmon["device"]))
    checks.append((
        "monitor_rect",
        [pmon["bounds"]["x"], pmon["bounds"]["y"], pmon["bounds"]["w"], pmon["bounds"]["h"]]
        == tmon["monitor"]))
    checks.append((
        "work_rect",
        [pmon["work"]["x"], pmon["work"]["y"], pmon["work"]["w"], pmon["work"]["h"]]
        == tmon["work"]))
    checks.append((
        "mode_current",
        [pmon["mode_current"]["w"], pmon["mode_current"]["h"],
         pmon["mode_current"]["freq"], pmon["mode_current"]["bpp"]]
        == [tmon["mode_current"]["w"], tmon["mode_current"]["h"],
            tmon["mode_current"]["freq"], tmon["mode_current"]["bpp"]]))
    agree = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"CROSSCHECK {name}: {'AGREE' if ok else 'DIFFER'}")
    print(f"MADO_DISPLAY_CROSSCHECK: {agree}/{len(checks)} stable fields AGREE")
    return 0 if agree == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
