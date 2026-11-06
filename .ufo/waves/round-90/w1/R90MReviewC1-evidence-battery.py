#!/usr/bin/env python3
"""R90MReviewC1 battery: materialise one-case fixtures, label them with the
production-binary oracle, run the candidate on the same inputs, diff.

DRAFT runs only (print DRAFT_* verdicts); no receipts are written."""
import json, os, shutil, subprocess, sys

S = os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku") + "/mado-r90/R90MReviewC1"
CAND = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-90/build/mado-portals.c1.py"
ORACLE = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-90/controls/portal-oracle-r90.py"
FC = "org.freedesktop.impl.portal.FileChooser"
ST = "org.freedesktop.impl.portal.Settings"
SS = "org.freedesktop.impl.portal.Screenshot"

def portal(name, dbus, ifaces, usein=None):
    t = f"[portal]\nDBusName={dbus}\nInterfaces={';'.join(ifaces)}\n"
    if usein is not None:
        t += f"UseIn={usein}\n"
    return t

CASES = [
  # ---- suspected candidate divergences ----
  dict(id="d1_badbracket", mode="dir", desktop="Hyprland", files={
    "kde.portal": portal("kde", "org.freedesktop.impl.portal.desktop.kde", [FC, ST]),
    "Hyprland-portals.conf": "[preferred]\ndefault=none\nbad]key=x\n",
    "portals.conf": "[preferred]\ndefault=kde\n"}),
  dict(id="d2_encoding", mode="dir", desktop="Hyprland", files={
    "kde.portal": "[portal]\nEncoding=ISOLatin1\nDBusName=org.freedesktop.impl.portal.desktop.kde\nInterfaces=" + FC + ";" + ST + "\n",
    "gtk.portal": portal("gtk", "org.freedesktop.impl.portal.desktop.gtk", [FC, ST]),
    "portals.conf": "[preferred]\ndefault=kde\n"}),
  dict(id="d3_useinescape", mode="dir", desktop="Hyprland", files={
    "hyprland.portal": portal("hyprland", "org.freedesktop.impl.portal.desktop.hyprland",
                              [FC, SS], usein="Hyprland;\\q"),
    "portals.conf": "[preferred]\ndefault=hyprland\n"}),
  # ---- refutation probes (candidate expected to match) ----
  dict(id="d4_leadws", mode="dir", desktop="Hyprland", files={
    "kde.portal": portal("kde", "org.freedesktop.impl.portal.desktop.kde", [FC, ST]),
    "portals.conf": "[preferred]\ndefault= kde\n"}),
  dict(id="d5_groupws", mode="dir", desktop="Hyprland", files={
    "kde.portal": portal("kde", "org.freedesktop.impl.portal.desktop.kde", [FC, ST]),
    "portals.conf": "[ preferred ]\ndefault=kde\n"}),
  dict(id="d6_trailws", mode="dir", desktop="Hyprland", files={
    "kde.portal": portal("kde", "org.freedesktop.impl.portal.desktop.kde", [FC, ST]),
    "portals.conf": "[preferred]\ndefault=kde \n"}),
  dict(id="d7_escsep", mode="dir", desktop="Hyprland", files={
    "kde.portal": portal("kde", "org.freedesktop.impl.portal.desktop.kde", [FC, ST]),
    "portals.conf": "[preferred]\ndefault=kde\\;gtk\n"}),
  dict(id="d8_uniquename", mode="dir", desktop="Hyprland", files={
    "kde.portal": portal("kde", ":1.2", [FC, ST]),
    "portals.conf": "[preferred]\ndefault=kde\n"}),
  dict(id="d9_dashname", mode="dir", desktop="Hyprland", files={
    "kde.portal": portal("kde", "org.-foo.bar-1", [FC, ST]),
    "portals.conf": "[preferred]\ndefault=kde\n"}),
  dict(id="d10_settings_order", mode="dir", desktop="Hyprland", files={
    "kde.portal": portal("kde", "org.freedesktop.impl.portal.desktop.kde", [FC, ST]),
    "gtk.portal": portal("gtk", "org.freedesktop.impl.portal.desktop.gtk", [FC, ST]),
    "hyprland.portal": portal("hyprland", "org.freedesktop.impl.portal.desktop.hyprland", [ST]),
    "portals.conf": "[preferred]\n" + ST + "=kde;*\ndefault=kde\n"}),
  dict(id="d12_usein_sort", mode="dir", desktop="Hyprland", files={
    "zeta.portal": portal("zeta", "org.zeta", [FC], usein="Hyprland"),
    "alpha.portal": portal("alpha", "org.alpha", [FC], usein="Hyprland")}),
  dict(id="d14_emptyconfstops", mode="dir", desktop="Hyprland", files={
    "kde.portal": portal("kde", "org.freedesktop.impl.portal.desktop.kde", [FC, ST]),
    "Hyprland-portals.conf": "[preferred]\na[de]=x\n",
    "portals.conf": "[preferred]\ndefault=kde\n"}),
  dict(id="d15_defaultC", mode="dir", desktop="Hyprland", files={
    "kde.portal": portal("kde", "org.freedesktop.impl.portal.desktop.kde", [FC, ST]),
    "Hyprland-portals.conf": "[preferred]\ndefault[C]=kde\ndefault=gtk\n"}),
  dict(id="d19_noneiface", mode="dir", desktop="Hyprland", files={
    "kde.portal": portal("kde", "org.freedesktop.impl.portal.desktop.kde", [FC, ST]),
    "portals.conf": "[preferred]\n" + FC + "=none;kde\ndefault=kde\n"}),
  # ---- oracle-parser probe: DONE-marker injection via a fixture filename ----
  dict(id="d11_marker_injection", mode="dir", desktop="X", files={
    "a.portal": portal("a", "org.a", [FC]),
    "evil org.freedesktop.portal.Desktop acquired.portal": portal("evil", "org.evil", [FC]),
    "portals.conf": "[preferred]\ndefault=a\n"}),
  # ---- non-ASCII desktop token must be dropped by both ----
  dict(id="d20_nonascii_desktop", mode="dir", desktop="Käse:Hyprland", files={
    "alpha.portal": portal("alpha", "org.alpha", [FC], usein="Käse,Hyprland".replace(",", ";"))}),
  # ---- xdg mode: config/data precedence + duplicate source across dirs ----
  dict(id="x1_xdgmode", mode="xdg", desktop="X", files={
    "config_home/xdg-desktop-portal/portals.conf": "[preferred]\ndefault=homekde\n",
    "config_dirs/0/xdg-desktop-portal/portals.conf": "[preferred]\ndefault=dirkde\n",
    "data_home/xdg-desktop-portal/portals/homekde.portal": portal("homekde", "org.home.kde", [FC]),
    "data_dirs/0/xdg-desktop-portal/portals/dirkde.portal": portal("dirkde", "org.dir.kde", [FC]),
    "data_dirs/0/xdg-desktop-portal/portals/homekde.portal": portal("homekde2", "org.dir.kde2", [SS])}),
]

def materialise_case(case, root):
    pdir = os.path.join(root, case["id"])
    for rel, text in case["files"].items():
        p = os.path.join(pdir, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
    return pdir

def run_candidate_dir(case, pdir):
    env = {k: v for k, v in os.environ.items() if not k.startswith("XDG_")}
    env["LC_ALL"] = "C"
    r = subprocess.run([sys.executable, CAND, "--portal-dir", pdir,
                        "--desktop", case["desktop"], "--json"],
                       env=env, cwd=pdir, capture_output=True, text=True, timeout=30)
    return r

def run_candidate_xdg(case, root):
    x = os.path.join(root, case["id"])
    env = {k: v for k, v in os.environ.items() if not k.startswith("XDG_")}
    env.update(XDG_CURRENT_DESKTOP=case["desktop"],
               XDG_CONFIG_HOME=os.path.join(x, "config_home"),
               XDG_CONFIG_DIRS=os.path.join(x, "config_dirs", "0"),
               XDG_DATA_HOME=os.path.join(x, "data_home"),
               XDG_DATA_DIRS=os.path.join(x, "data_dirs", "0"),
               LC_ALL="C")
    return subprocess.run([sys.executable, CAND, "--desktop", case["desktop"], "--json"],
                          env=env, cwd=x, capture_output=True, text=True, timeout=30)

def main():
    root = os.path.join(S, "fixtures")
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    for c in CASES:
        materialise_case(c, root)

    cases_path = os.path.join(S, "cases.json")
    labels_path = os.path.join(S, "labels.json")
    with open(cases_path, "w", encoding="utf-8") as fh:
        json.dump({"cases": CASES}, fh, ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, ORACLE, "--cases", cases_path, "--label", labels_path,
                        "--scratch-root", os.path.join(S, "oracle-scratch"), "--jobs", "6",
                        "--timeout", "8"], capture_output=True, text=True, timeout=600)
    print("ORACLE rc=%d %s" % (r.returncode, r.stdout.strip()))
    if r.stderr.strip():
        print("ORACLE stderr:", r.stderr.strip()[:4000])
    labels = {c["id"]: c for c in json.load(open(labels_path, encoding="utf-8"))["cases"]}

    diff_n = 0
    for c in CASES:
        pdir = os.path.join(root, c["id"])
        cr = run_candidate_xdg(c, root) if c["mode"] == "xdg" else run_candidate_dir(c, pdir)
        if cr.returncode != 0:
            print(f"== {c['id']}: candidate rc={cr.returncode} stdout={cr.stdout!r} stderr={cr.stderr!r}")
            diff_n += 1
            continue
        j = json.loads(cr.stdout)
        lab = labels[c["id"]]
        picks_o, reason_o = lab["oracle"], lab.get("oracle_reason", {})
        diffs = []
        for iface in j["picks"]:
            cp, crs = j["picks"][iface], j["reasons"].get(iface)
            op, ors = picks_o.get(iface, []), reason_o.get(iface)
            if cp != op:
                diffs.append(f"{iface.rsplit('.',1)[1]}: cand={cp or '[]'}({crs}) oracle={op or '[]'}({ors})")
        status = "SAME" if not diffs else "DIFF"
        if diffs:
            diff_n += 1
        print(f"== {c['id']}: {status}")
        for d in diffs:
            print("   " + d)
        print("   cand: desktops=%s backends=%s" % (",".join(j["desktops"]), ",".join(j["backends"])))
        if j.get("warnings"):
            print("   cand-warns: " + " | ".join(j["warnings"]))
    print(f"BATTERY cases={len(CASES)} diff_cases={diff_n}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
