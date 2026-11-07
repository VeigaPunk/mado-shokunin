#!/usr/bin/env python3
"""Round-93 C1 byte-class fuzz: deterministic generator of unlabelled cases.

Mirrors the round-90 fuzz-gen CLI shape (``--seed N --count K``); the oracle
labels them at measurement time.  Cases are round-90 schema (id, mode,
desktop, files) with byte content as lone surrogates, ids fuzz93-NNNNN,
each tagged "class": a|b|c|d|n|ws (n: NUL bytes, L1 addition after R93MReviewC1 F1).
The counter calls gen_cases(count, seed).

Usage: python3 fuzz-bytes-r93.py --seed N --count K --out CASES.json
"""
from __future__ import annotations

import argparse
import json
import random

IMPL = "org.freedesktop.impl.portal."
DESKTOPS = ["XFCE", "KDE", "GNOME", "Hyprland", "sway"]

KDE_PORTAL = ("[portal]\nDBusName=org.freedesktop.impl.portal.desktop.kde\n"
              "Interfaces=org.freedesktop.impl.portal.FileChooser;org.freedesktop.impl.portal.Print;"
              "org.freedesktop.impl.portal.Settings;\nUseIn=KDE;\n")
GTK_PORTAL = ("[portal]\nDBusName=org.freedesktop.impl.portal.desktop.gtk\n"
              "Interfaces=org.freedesktop.impl.portal.FileChooser;org.freedesktop.impl.portal.Print;"
              "org.freedesktop.impl.portal.Settings;org.freedesktop.impl.portal.Screenshot;\n")
GNOME_PORTAL = ("[portal]\nDBusName=org.freedesktop.impl.portal.desktop.gnome\n"
                "Interfaces=org.freedesktop.impl.portal.FileChooser;org.freedesktop.impl.portal.Settings;\n"
                "UseIn=gnome;\n")

# raw-byte spellings (surrogateescape): byte -> \udcXX
INVALID = {
    "b80": "\udc80", "bc328": "\udcc3(", "bed": "\udced\udca0\udc80",
    "bff": "\udcff", "bc0af": "\udcc0\udcaf", "be9": "\udce9",
}
VT = "\x0b"
SPACEISH = {"ff": "\x0c", "cr": "\x0d", "tab": "\t", "sp": " "}
NUL = "\x00"
CLASSES = ["a", "b", "c", "d", "n", "ws"]


def conf_text(rng, cls, ktok):
    head = rng.choice(["", f"# x{ktok}\n", f"[other]\nfoo=bar{ktok}\n",
                       f"# note{ktok}\n"])
    base = ("[preferred]\ndefault=kde\n"
            "org.freedesktop.impl.portal.Print=kde\n")
    if cls == "a":
        v = rng.choice(list(INVALID.values()))
        spot = rng.choice([
            f"{head}[preferred]\ndefault=kde{v}\n",
            f"{head}[preferred]\nfoo=bar{v}\ndefault=kde\n",
            f"{head}[preferred]\norg.freedesktop.impl.portal.FileChooser=gnome{v}\ndefault=gtk\n",
            f"{head}[preferred]\ndefault=kde\n# t{v}",
            f"{head}[preferred]{rng.choice(['', ' ', chr(9)])}{rng.choice(['\udc80', '\udc9a', '\udcbf', '\udcc3'])}\ndefault=kde\n",
        ])
        return spot
    if cls == "n":
        return rng.choice([
            f"[preferred]\ndefault=kde{NUL}junk\n",
            f"[preferred]{NUL}junk\ndefault=kde\n",
            f"{NUL}\n[preferred]\ndefault=kde\n",
            f"[preferred]\ndefault=kde\n{NUL}",
            f"[preferred]\ndefault=kde{NUL}",
            f"[preferred]\nde{NUL}fault=kde\n",
            f"[pref{NUL}erred]\ndefault=kde\n",
            f"[preferred]{NUL}]\ndefault=kde\n",
            f"[preferred]\ndefault= {NUL}kde\n",
            f"#{NUL}x\n[preferred]\ndefault=gtk;kde{NUL};gnome\n",
        ])
    if cls == "b":
        return rng.choice([
            f"{VT}[preferred]\ndefault=kde\n",
            f"[preferred]\n{VT}default=kde\n",
            f"[preferred]\ndefault{VT}=kde\n",
            f"[preferred]\ndefault={VT}kde\n",
            f"[preferred]\ndefault=kde{VT}\n",
            f"[preferred]\ndefault=k{VT}de\n",
        ])
    if cls == "ws":
        s = rng.choice(list(SPACEISH.values()))
        return rng.choice([
            f"{s}[preferred]\ndefault=kde\n",
            f"[preferred]\n{s}default=kde\n",
            f"[preferred]\ndefault{s}=kde\n",
            f"[preferred]\ndefault={s}kde\n",
        ])
    if cls == "c":
        return (f"[preferred]\ndefault=gnome\ndefault=kde\n"
                f"org.freedesktop.impl.portal.Settings=gnome\n"
                f"org.freedesktop.impl.portal.Settings=gtk\n")
    if cls == "d":
        return rng.choice([
            "[preferred]\ndefault[]=kde\n",
            "[preferred]\ndefault[C]=kde\n",
            "[preferred]\ndefault[en]=kde\n",
            "[preferred]\ndefault=gtk\norg.freedesktop.impl.portal.FileChooser[]=kde\n",
            "[preferred]\ndefault=gtk\norg.freedesktop.impl.portal.FileChooser[C]=kde\n",
        ])
    return base


def kde_text(rng, cls, ktok):
    if cls == "a":
        v = rng.choice(list(INVALID.values()))
        return rng.choice([
            f"# c{v}\n" + KDE_PORTAL,
            KDE_PORTAL + f"Foo=bar{v}\n",
            KDE_PORTAL.replace("Settings;", f"Settings{v};"),
            KDE_PORTAL.replace("desktop.kde", f"desktop.kde{v}"),
            KDE_PORTAL.replace("UseIn=KDE;", f"UseIn=KDE{v};"),
        ])
    if cls == "b":
        return rng.choice([
            f"[portal]\n{VT}DBusName=org.freedesktop.impl.portal.desktop.kde\n"
            "Interfaces=org.freedesktop.impl.portal.FileChooser;\nUseIn=KDE;\n",
            f"{VT}[portal]\nDBusName=org.freedesktop.impl.portal.desktop.kde\n"
            "Interfaces=org.freedesktop.impl.portal.FileChooser;\nUseIn=KDE;\n",
            KDE_PORTAL.replace("FileChooser;", f"File{VT}Chooser;"),
        ])
    if cls == "n":
        return rng.choice([
            KDE_PORTAL.replace("Settings;", f"Settings;{NUL}junk"),
            KDE_PORTAL.replace("FileChooser;", f"FileChooser;{NUL}"),
            KDE_PORTAL.replace("desktop.kde", f"desktop.kde{NUL}x"),
            KDE_PORTAL.replace("[portal]", f"[portal]{NUL}junk"),
            KDE_PORTAL + f"Foo{NUL}Bar=x\n",
            f"{NUL}\n" + KDE_PORTAL,
        ])
    if cls == "ws":
        s = rng.choice(list(SPACEISH.values()))
        return (f"[portal]\n{s}DBusName=org.freedesktop.impl.portal.desktop.kde\n"
                "Interfaces=org.freedesktop.impl.portal.FileChooser;\nUseIn=KDE;\n")
    if cls == "c":
        return ("[portal]\nDBusName=org.freedesktop.impl.portal.desktop.gnome\n"
                "DBusName=org.freedesktop.impl.portal.desktop.kde\n"
                "Interfaces=org.freedesktop.impl.portal.FileChooser;\nUseIn=KDE;\n")
    if cls == "d":
        return rng.choice([
            KDE_PORTAL.replace("DBusName=", "DBusName[]="),
            KDE_PORTAL.replace("DBusName=", "DBusName[C]="),
            KDE_PORTAL.replace("DBusName=", "DBusName[en]="),
        ])
    return KDE_PORTAL


def gen_case(rng, i):
    cls = CLASSES[i % len(CLASSES)] if i < 5 * (  # guarantee every class occurs
        60) else rng.choice(CLASSES)
    mode = rng.choice(["dir", "dir", "dir", "xdg"])
    desktop = rng.choice(DESKTOPS)
    ktok = rng.choice(list(INVALID.values()))
    files = {"kde.portal": kde_text(rng, cls, ktok), "gtk.portal": GTK_PORTAL,
             "gnome.portal": GNOME_PORTAL,
             "portals.conf": conf_text(rng, cls, ktok)}
    if mode == "xdg":
        files = {
            "config_home/xdg-desktop-portal/hyprland-portals.conf":
                files["portals.conf"].replace("portals.conf", "x").replace(
                    f"[{desktop}]", "[preferred]") if False else
                conf_text(rng, cls, ktok),
            "data_home/xdg-desktop-portal/portals/kde.portal": files["kde.portal"],
        }
    return {"id": f"fuzz93-{i:05d}", "mode": mode, "desktop": desktop,
            "files": files, "class": cls}


def gen_cases(count: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    return [gen_case(rng, i) for i in range(count)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=938001)
    ap.add_argument("--count", type=int, default=60)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cases = gen_cases(a.count, a.seed)
    s = json.dumps({"cases": cases}, indent=1, ensure_ascii=True)
    with open(a.out, "w", encoding="ascii") as fh:
        fh.write(s + "\n")

if __name__ == "__main__":
    raise SystemExit(main())
