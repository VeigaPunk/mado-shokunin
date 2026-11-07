#!/usr/bin/env python3
"""Round-93 C1 byte-class case generator (unlabelled output).

Writes >=48 cases in the round-90 schema (id, mode, desktop, files{name:text})
with byte content as lone surrogates (\\udcXX = raw byte XX) so the r93
oracle writes them as raw bytes via surrogateescape.  Includes the 16
round-92 gkeyfile cases verbatim (ids keep the d1- prefix).

Usage: python3 gen-c1-bytes-cases-r93.py --out CASES.json
"""
from __future__ import annotations

import argparse
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
R92_CASES = LANE + "/.ufo/waves/round-92/controls/portals-gkeyfile-cases-r92.json"

S = "\udce9"  # raw byte 0xE9 standalone (invalid UTF-8)
KDE_PORTAL = ("[portal]\nDBusName=org.freedesktop.impl.portal.desktop.kde\n"
              "Interfaces=org.freedesktop.impl.portal.FileChooser;org.freedesktop.impl.portal.Print;"
              "org.freedesktop.impl.portal.Settings;\nUseIn=KDE;\n")
GTK_PORTAL = ("[portal]\nDBusName=org.freedesktop.impl.portal.desktop.gtk\n"
              "Interfaces=org.freedesktop.impl.portal.FileChooser;org.freedesktop.impl.portal.Print;"
              "org.freedesktop.impl.portal.Settings;org.freedesktop.impl.portal.Screenshot;\n")
GNOME_PORTAL = ("[portal]\nDBusName=org.freedesktop.impl.portal.desktop.gnome\n"
                "Interfaces=org.freedesktop.impl.portal.FileChooser;org.freedesktop.impl.portal.Settings;\n"
                "UseIn=gnome;\n")
BASE_FILES = {"kde.portal": KDE_PORTAL, "gtk.portal": GTK_PORTAL,
              "gnome.portal": GNOME_PORTAL}

# surrogateescape spellings for the invalid-UTF8 byte sequences
B80 = "\udc80"            # 0x80 lone continuation
BC3_28 = "\udcc3("        # 0xC3 0x28
BED = "\udced\udca0\udc80"  # 0xED 0xA0 0x80 (surrogate encoding)
BFF = "\udcff"            # 0xFF
BC0_AF = "\udcc0\udcaf"   # overlong 0xC0 0xAF
BTRUNC = "\udcc3"         # truncated sequence: file ends with lone 0xC3


def dir_case(cid, conf, cls, kde=None, gtk=None, desktop="XFCE"):
    files = dict(BASE_FILES)
    files["portals.conf"] = conf
    if kde is not None:
        files["kde.portal"] = kde
    if gtk is not None:
        files["gtk.portal"] = gtk
    return {"id": cid, "mode": "dir", "desktop": desktop, "files": files, "class": cls}


def xdg_case(cid, conf, cls, kde_extra=None, desktop="XFCE"):
    # xdg mode: config_home conf + data_home kde portal; gtk from host tail
    files = {
        "config_home/xdg-desktop-portal/portals.conf": conf,
        "data_home/xdg-desktop-portal/portals/kde.portal": kde_extra or KDE_PORTAL,
    }
    return {"id": cid, "mode": "xdg", "desktop": desktop, "files": files, "class": cls}


def build() -> list[dict]:
    cases: list[dict] = []

    # ---- include the 16 round-92 cases verbatim (tag class by prefix) ----
    r92 = json.load(open(R92_CASES, encoding="utf-8"))
    for c in r92["cases"]:
        c = dict(c)
        c["class"] = ("a" if "-a" in c["id"] else "b" if "-b" in c["id"]
                      else "c" if "-c" in c["id"] else "d")
        cases.append(c)

    # ============================ class (a) invalid UTF-8 ============================
    # config comment / other group / unread key / read preferred key
    cases.append(dir_case("b93-a80-config-comment", f"# cafe{B80} x\n[preferred]\ndefault=kde\n", "a"))
    cases.append(dir_case("b93-ac328-other-group", f"[other]\nfoo=bar{BC3_28}\n[preferred]\ndefault=kde\n", "a"))
    cases.append(dir_case("b93-aed80-unread-key", f"[preferred]\nfoo=bar{BED}\ndefault=kde\n", "a"))
    cases.append(dir_case("b93-aff-config-comment", f"# x{BFF}\n[preferred]\ndefault=kde\n", "a"))
    cases.append(dir_case("b93-ac0af-config-comment", f"# x{BC0_AF}\n[preferred]\ndefault=kde\n", "a"))
    # invalid byte in a read [preferred] key -> whole config void (eager)
    cases.append(dir_case("b93-a80-config-readkey", f"[preferred]\norg.freedesktop.impl.portal.Print=gnome{B80}\n", "a"))
    cases.append(dir_case("b93-aed80-config-readkey", f"[preferred]\norg.freedesktop.impl.portal.FileChooser=kde{BED}\ndefault=gtk\n", "a"))
    cases.append(dir_case("b93-aff-config-readkey", f"[preferred]\ndefault=kde{BFF}\n", "a"))
    # truncated sequence at EOF (no trailing newline)
    cases.append(dir_case("b93-atrunc-config-comment", f"[preferred]\ndefault=kde\n# tail{BTRUNC}", "a"))
    cases.append(dir_case("b93-atrunc-config-readkey", f"[preferred]\ndefault=kde{BTRUNC}", "a"))
    # .portal comment / unread key / read keys (Interfaces, DBusName, UseIn)
    cases.append(dir_case("b93-a80-portal-comment", "[preferred]\ndefault=kde\n", "a",
                          kde=f"# c{B80}\n" + KDE_PORTAL))
    cases.append(dir_case("b93-ac328-portal-unread", "[preferred]\ndefault=kde\n", "a",
                          kde=KDE_PORTAL + f"Foo=bar{BC3_28}\n"))
    cases.append(dir_case("b93-aed80-portal-unread", "[preferred]\ndefault=kde\n", "a",
                          kde=KDE_PORTAL + f"Foo=bar{BED}\n"))
    cases.append(dir_case("b93-aff-portal-ifaces", "[preferred]\ndefault=kde\n", "a",
                          kde=KDE_PORTAL.replace("Settings;", f"Settings{BFF};")))
    cases.append(dir_case("b93-ac0af-portal-dbusname", "[preferred]\ndefault=kde\n", "a",
                          kde=KDE_PORTAL.replace("desktop.kde", f"desktop.kde{BC0_AF}")))
    cases.append(dir_case("b93-atrunc-portal-comment", "[preferred]\ndefault=kde\n", "a",
                          kde=KDE_PORTAL + f"# tail{BTRUNC}"))
    # Interfaces / DBusName / UseIn read keys in gtk.portal (fallback-target effect)
    cases.append(dir_case("b93-a80-gtk-ifaces", "[preferred]\ndefault=kde\n", "a",
                          gtk=GTK_PORTAL.replace("Screenshot;", f"Screenshot{B80};")))
    cases.append(dir_case("b93-a80-usein", "[preferred]\ndefault=kde\n", "a",
                          kde=KDE_PORTAL.replace("UseIn=KDE;", f"UseIn=KDE{B80};")))
    # xdg mode invalid UTF-8
    cases.append(xdg_case("b93-a80-xdg-config-comment", f"# x{B80}\n[preferred]\ndefault=kde\n", "a"))
    cases.append(xdg_case("b93-aed80-xdg-config-readkey", f"[preferred]\norg.freedesktop.impl.portal.Print=kde{BED}\ndefault=kde\n", "a"))
    cases.append(xdg_case("b93-aff-xdg-portal-comment", "[preferred]\ndefault=kde\n", "a",
                          kde_extra=f"# x{BFF}\n" + KDE_PORTAL))

    # ============================ class (b) 0x0B / controls ============================
    V = "\x0b"
    cases.append(dir_case("b93-b-vt-line-start", f"{V}[preferred]\ndefault=kde\n", "b"))
    cases.append(dir_case("b93-b-vt-before-group", f"{V}[preferred]\ndefault=kde\n", "b"))
    cases.append(dir_case("b93-b-vt-before-key", f"[preferred]\n{V}default=kde\n", "b"))
    cases.append(dir_case("b93-b-vt-before-equals", f"[preferred]\ndefault{V}=kde\n", "b"))
    cases.append(dir_case("b93-b-vt-after-equals", f"[preferred]\ndefault={V}kde\n", "b"))
    cases.append(dir_case("b93-b-vt-inside-value", f"[preferred]\ndefault=k{V}de\n", "b"))
    cases.append(dir_case("b93-b-vt-trailing-value", f"[preferred]\ndefault=kde{V}\n", "b"))
    cases.append(dir_case("b93-b-vt-trailing-key", f"[preferred]\ndefault{V}\n", "b"))
    cases.append(dir_case("b93-b-vt-portal", "[preferred]\ndefault=kde\n", "b",
                          kde=f"[portal]\n{V}DBusName=org.freedesktop.impl.portal.desktop.kde\n"
                              "Interfaces=org.freedesktop.impl.portal.FileChooser;org.freedesktop.impl.portal.Print;"
                              "org.freedesktop.impl.portal.Settings;\nUseIn=KDE;\n"))
    cases.append(dir_case("b93-b-vt-portal-before-group", "[preferred]\ndefault=kde\n", "b",
                          kde=f"{V}[portal]\nDBusName=org.freedesktop.impl.portal.desktop.kde\n"
                              "Interfaces=org.freedesktop.impl.portal.FileChooser;\nUseIn=KDE;\n"))
    cases.append(dir_case("b93-b-vt-value-mid", "[preferred]\ndefault=kde;gt{V}k\n", "b"))
    cases.append(xdg_case("b93-b-vt-xdg", f"[preferred]\n{V}default=kde\n", "b"))
    # xdg + dir control ids for ws below share the same confined layouts

    # ---- class ws: 0x0C / 0x0D / TAB / space ARE whitespace to GLib ----
    F, CR, TAB = "\x0c", "\x0d", "\t"
    cases.append(dir_case("b93-ws-ff-before-group", f"{F}[preferred]\ndefault=kde\n", "ws"))
    cases.append(dir_case("b93-ws-ff-before-key", f"[preferred]\n{F}default=kde\n", "ws"))
    cases.append(dir_case("b93-ws-ff-before-equals", f"[preferred]\ndefault{F}=kde\n", "ws"))
    cases.append(dir_case("b93-ws-ff-after-equals", f"[preferred]\ndefault={F}kde\n", "ws"))
    cases.append(dir_case("b93-ws-tab-before-group", f"{TAB}[preferred]\ndefault=kde\n", "ws"))
    cases.append(dir_case("b93-ws-tab-before-key", f"[preferred]\n{TAB}default=kde\n", "ws"))
    cases.append(dir_case("b93-ws-tab-after-equals", f"[preferred]\ndefault={TAB}kde\n", "ws"))
    cases.append(dir_case("b93-ws-cr-before-key", f"[preferred]\n{CR}default=kde\n", "ws"))
    cases.append(dir_case("b93-ws-space-before-key", "[preferred]\n default=kde\n", "ws"))
    cases.append(dir_case("b93-ws-space-after-equals", "[preferred]\ndefault= kde\n", "ws"))
    cases.append(dir_case("b93-ws-crlf", "[preferred]\r\ndefault=kde\r\n", "ws"))
    cases.append(dir_case("b93-ws-tab-portal", "[preferred]\ndefault=kde\n", "ws",
                          kde="[portal]\n\tDBusName=org.freedesktop.impl.portal.desktop.kde\n"
                              "Interfaces=org.freedesktop.impl.portal.FileChooser;\nUseIn=KDE;\n"))
    cases.append(xdg_case("b93-ws-ff-xdg", f"{F}[preferred]\ndefault=kde\n", "ws"))

    # ============================ class (c) repeated keys ============================
    cases.append(dir_case("b93-c-repeated-iface", "[preferred]\ndefault=kde\n"
                          "org.freedesktop.impl.portal.FileChooser=gnome\n"
                          "org.freedesktop.impl.portal.FileChooser=kde\n", "c"))
    cases.append(dir_case("b93-c-repeated-portal-ifaces", "[preferred]\ndefault=kde\n", "c",
                          kde="[portal]\nDBusName=org.freedesktop.impl.portal.desktop.kde\n"
                              "Interfaces=org.freedesktop.impl.portal.FileChooser;\nInterfaces=org.freedesktop.impl.portal.Settings;\n"
                              "UseIn=KDE;\n"))
    cases.append(dir_case("b93-c-repeated-dbusname", "[preferred]\ndefault=kde\n", "c",
                          kde="[portal]\nDBusName=org.freedesktop.impl.portal.desktop.gnome\n"
                              "DBusName=org.freedesktop.impl.portal.desktop.kde\n"
                              "Interfaces=org.freedesktop.impl.portal.FileChooser;\nUseIn=KDE;\n"))
    cases.append(xdg_case("b93-c-repeated-xdg", "[preferred]\ndefault=gnome\ndefault=kde\n", "c"))

    # ============================ class (d) locale keys ============================
    cases.append(dir_case("b93-d-default-en", "[preferred]\ndefault[en]=kde\n", "d"))
    cases.append(dir_case("b93-d-iface-en", "[preferred]\ndefault=gtk\norg.freedesktop.impl.portal.FileChooser[en]=kde\n", "d"))
    cases.append(dir_case("b93-d-dbusname-en", "[preferred]\ndefault=kde;gtk\n", "d",
                          kde="[portal]\nDBusName[en]=org.freedesktop.impl.portal.desktop.kde\n"
                              "Interfaces=org.freedesktop.impl.portal.FileChooser;\nUseIn=KDE;\n"))
    cases.append(dir_case("b93-d-usein-en", "[preferred]\ndefault=kde\n", "d",
                          kde="[portal]\nDBusName=org.freedesktop.impl.portal.desktop.kde\n"
                              "Interfaces=org.freedesktop.impl.portal.FileChooser;\nUseIn[en]=KDE;\n"))
    cases.append(xdg_case("b93-d-default-empty-xdg", "[preferred]\ndefault[]=kde\ndefault=gtk\n", "d"))

    return cases


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cases = build()
    s = json.dumps({"cases": cases}, indent=1, ensure_ascii=True)
    with open(a.out, "w", encoding="ascii") as fh:
        fh.write(s + "\n")
    print(f"GENC1 cases={len(cases)} out={a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
