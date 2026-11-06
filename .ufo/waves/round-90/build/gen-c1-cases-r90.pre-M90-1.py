#!/usr/bin/env python3
"""Round-90 C1 case generator (fixtures only; labels come from portal-oracle-r90.py).

Each case is a fixture tree + an XDG_CURRENT_DESKTOP value.  Descriptors for
gtk/hyprland/gnome-keyring/kwallet are the host's installed bytes
(/usr/share/xdg-desktop-portal/portals, read at generation time and embedded);
kde/gnome/wlr/termfilechooser descriptors are synthetic but shaped like their
upstream packages.  Labels are never written here.
"""
import json
import sys

I = "org.freedesktop.impl.portal."
HOST = "/usr/share/xdg-desktop-portal/portals/"
gtk = open(HOST + "gtk.portal").read()
hypr = open(HOST + "hyprland.portal").read()
keyring = open(HOST + "gnome-keyring.portal").read()
kwallet = open(HOST + "kwallet.portal").read()
hostconf = open("/usr/share/xdg-desktop-portal/hyprland-portals.conf").read()


def portal(dbus, ifaces, use_in=None, trailing=";"):
    s = "[portal]\nDBusName=" + dbus + "\nInterfaces=" + ";".join(I + i for i in ifaces) + trailing + "\n"
    if use_in is not None:
        s += "UseIn=" + use_in + "\n"
    return s


kde = portal(I + "desktop.kde", ["FileChooser", "AppChooser", "Print", "Notification", "Inhibit", "Settings",
                                  "Screenshot", "ScreenCast", "RemoteDesktop", "Background", "Wallpaper", "Account",
                                  "Email", "DynamicLauncher", "GlobalShortcuts", "Clipboard", "InputCapture", "Usb",
                                  "Access", "Lockdown"], "KDE")
gnome = portal(I + "desktop.gnome", ["Access", "Account", "AppChooser", "Background", "Clipboard", "DynamicLauncher",
                                      "FileChooser", "GlobalShortcuts", "InputCapture", "Lockdown", "RemoteDesktop",
                                      "ScreenCast", "Screenshot", "Settings", "Wallpaper"], "gnome")
wlr = portal(I + "desktop.wlr", ["Screenshot", "ScreenCast"], "wlroots;sway;Wayfire;river;phosh;Hyprland;")
termfc = portal(I + "desktop.termfilechooser", ["FileChooser"], None)
darkman = portal("nl.whynothugo.darkman", ["Settings"], None)

HOSTSET = {"gtk.portal": gtk, "hyprland.portal": hypr, "gnome-keyring.portal": keyring, "kwallet.portal": kwallet}
WIDE = HOSTSET | {"kde.portal": kde, "gnome.portal": gnome, "wlr.portal": wlr, "termfilechooser.portal": termfc,
                  "darkman.portal": darkman}
cases = []


def add(cid, files, desktop="Hyprland", mode="dir", **extra):
    c = {"id": cid, "mode": mode, "desktop": desktop, "files": files}
    c.update(extra)
    cases.append(c)


P = "[preferred]\n"
# 1. host replica and desktop parsing
add("d01-host-replica", HOSTSET | {"hyprland-portals.conf": hostconf})
add("d02-desktop-lowercase", HOSTSET | {"hyprland-portals.conf": hostconf}, "hyprland")
add("d03-desktop-upper", HOSTSET | {"hyprland-portals.conf": hostconf}, "HYPRLAND")
add("d04-desktop-unset", HOSTSET | {"hyprland-portals.conf": hostconf}, None)
add("d05-desktop-empty", HOSTSET | {"hyprland-portals.conf": hostconf}, "")
add("d06-desktop-two-hypr-first", WIDE | {"hyprland-portals.conf": hostconf, "gnome-portals.conf": P + "default=gnome;gtk\n"}, "Hyprland:GNOME")
add("d07-desktop-two-gnome-first", WIDE | {"hyprland-portals.conf": hostconf, "gnome-portals.conf": P + "default=gnome;gtk\n"}, "GNOME:Hyprland")
add("d08-desktop-invalid-token-dropped", WIDE | {"kde-portals.conf": P + "default=kde\n", "hyprland-portals.conf": hostconf}, "bad/val:KDE")
add("d09-desktop-empty-token", WIDE | {"kde-portals.conf": P + "default=kde\n"}, ":KDE")
add("d10-desktop-sway-no-conf-usein", WIDE, "sway")
add("d11-desktop-dot-token-dropped", WIDE | {"hyprland-portals.conf": hostconf}, "Hypr.land:Hyprland")
# 2. interface keys
add("k01-iface-key-kde-filechooser", WIDE | {"hyprland-portals.conf": hostconf + I + "FileChooser=kde\n"})
add("k02-iface-key-missing-backend-next", WIDE | {"hyprland-portals.conf": P + "default=hyprland;gtk\n" + I + "FileChooser=nosuch;termfilechooser\n"})
add("k03-iface-key-unsupported-skipped", WIDE | {"hyprland-portals.conf": P + "default=hyprland;gtk\n" + I + "ScreenCast=gtk;wlr\n"})
add("k04-iface-key-nothing-falls-to-default", WIDE | {"hyprland-portals.conf": P + "default=hyprland;gtk\n" + I + "Screenshot=nosuch\n"})
add("k05-iface-key-short-name-ignored", WIDE | {"hyprland-portals.conf": P + "default=hyprland;gtk\nFileChooser=kde\n"})
add("k06-iface-key-case-sensitive-backend", WIDE | {"hyprland-portals.conf": P + "default=hyprland;gtk\n" + I + "FileChooser=KDE\n"})
# 3. none
add("n01-default-none", WIDE | {"hyprland-portals.conf": P + "default=none\n"})
add("n02-iface-none", WIDE | {"hyprland-portals.conf": hostconf + I + "Screenshot=none\n"})
add("n03-none-later-in-list", WIDE | {"hyprland-portals.conf": P + "default=hyprland;none\n"})
add("n04-iface-key-beats-default-none", WIDE | {"hyprland-portals.conf": P + "default=none\n" + I + "FileChooser=kde\n"})
add("n05-None-capital-is-a-name", WIDE | {"hyprland-portals.conf": P + "default=None;gtk\n"})
add("n06-iface-none-with-backend-first", WIDE | {"hyprland-portals.conf": hostconf + I + "FileChooser=kde;none\n"})
# 4. star
add("s01-default-star", WIDE | {"hyprland-portals.conf": P + "default=*\n"})
add("s02-iface-star", WIDE | {"hyprland-portals.conf": P + "default=gtk\n" + I + "ScreenCast=*\n"})
add("s03-star-stops-list", WIDE | {"hyprland-portals.conf": P + "default=hyprland;gtk\n" + I + "Secret=*;kwallet\n"},
    "Hyprland")
add("s04-star-nothing-falls-to-default", HOSTSET | {"hyprland-portals.conf": P + "default=gnome-keyring\n" + I + "Secret=*;kwallet\n"},
    "XFCE")
add("s05-star-sort-usein-first", WIDE | {"portals.conf": P + "default=*\n"}, "KDE")
add("s06-star-sort-name-order", WIDE | {"portals.conf": P + "default=*\n"}, "XFCE")
# 5. Settings find_all
add("a01-settings-two", WIDE | {"hyprland-portals.conf": hostconf + I + "Settings=darkman;gtk\n"})
add("a02-settings-star", WIDE | {"hyprland-portals.conf": hostconf + I + "Settings=*\n"})
add("a03-settings-none", WIDE | {"hyprland-portals.conf": hostconf + I + "Settings=none\n"})
add("a04-settings-empty-key-default", WIDE | {"hyprland-portals.conf": P + "default=kde;gtk\n" + I + "Settings=\n"})
add("a05-settings-dup-entries", WIDE | {"hyprland-portals.conf": P + "default=hyprland\n" + I + "Settings=gtk;gtk;darkman\n"})
add("a06-settings-usein-all", WIDE | {"gnome.portal": portal(I + "desktop.gnome", ["Settings"], "gnome;kde"),
                                     "kde.portal": portal(I + "desktop.kde", ["Settings"], "KDE")}, "KDE:GNOME")
# 6. file selection
add("f01-desktop-file-without-preferred", WIDE | {"hyprland-portals.conf": "[other]\ndefault=kde\n", "portals.conf": P + "default=gnome;gtk\n"})
add("f02-desktop-file-beats-portals-conf", WIDE | {"hyprland-portals.conf": hostconf, "portals.conf": P + "default=gnome;gtk\n"})
add("f03-empty-preferred-group", WIDE | {"hyprland-portals.conf": "[preferred]\n", "portals.conf": P + "default=gnome;gtk\n"})
add("f04-only-portals-conf", WIDE | {"portals.conf": P + "default=gnome;gtk\n"})
add("f05-unmatched-desktop-file", WIDE | {"kde-portals.conf": P + "default=kde\n"})
# 7. GKeyFile
add("g01-spaces-around-equals", WIDE | {"hyprland-portals.conf": P + "default = kde;gtk\n"})
add("g02-space-after-separator", WIDE | {"hyprland-portals.conf": P + "default=kde; gtk\n"}, "XFCE:Hyprland")
add("g03-trailing-space-value", WIDE | {"hyprland-portals.conf": P + "default=kde  \n"})
add("g04-crlf", WIDE | {"hyprland-portals.conf": "[preferred]\r\ndefault=kde;gtk\r\n"})
add("g05-comments-blank-indent", WIDE | {"hyprland-portals.conf": "# c\n\n  [preferred]\n   # x\n\tdefault=kde;gtk\n"})
add("g06-duplicate-key-last-wins", WIDE | {"hyprland-portals.conf": P + "default=kde\ndefault=gnome\n"})
add("g07-duplicate-group-merge", WIDE | {"hyprland-portals.conf": P + "default=gtk\n[x]\na=b\n" + P + I + "FileChooser=kde\n"})
add("g08-escape-s", WIDE | {"hyprland-portals.conf": P + "default=\\skde;gtk\n"})
add("g09-invalid-escape-voids-file", WIDE | {"hyprland-portals.conf": P + "default=kde\\q\n", "portals.conf": P + "default=gnome\n"})
add("g10-key-before-group-voids", WIDE | {"hyprland-portals.conf": "default=kde\n" + P + "default=gnome\n", "portals.conf": P + "default=gtk\n"})
add("g11-bare-line-voids", WIDE | {"hyprland-portals.conf": P + "default=kde\nnonsense\n", "portals.conf": P + "default=gnome\n"})
add("g12-escaped-separator", WIDE | {"hyprland-portals.conf": P + "default=kde\\;gtk;gnome\n"})
add("g13-trailing-backslash-voids", WIDE | {"hyprland-portals.conf": P + "default=kde\\\n", "portals.conf": P + "default=gnome\n"})
add("g14-key-leading-space-ok", WIDE | {"hyprland-portals.conf": P + "   default=kde\n"})
add("g15-group-trailing-garbage-voids", WIDE | {"hyprland-portals.conf": "[preferred] x\ndefault=kde\n", "portals.conf": P + "default=gnome\n"})
add("g16-group-trailing-space-ok", WIDE | {"hyprland-portals.conf": "[preferred]  \ndefault=kde\n"})
add("g17-empty-default", WIDE | {"hyprland-portals.conf": P + "default=\n"})
add("g18-only-separators", WIDE | {"hyprland-portals.conf": P + "default=;;kde\n"})
# 8. descriptors
add("p01-invalid-dbusname-skipped", WIDE | {"kde.portal": kde.replace("DBusName=" + I + "desktop.kde", "DBusName=kde"),
                                            "hyprland-portals.conf": P + "default=kde;gtk\n"})
add("p02-foreign-interface-voids", WIDE | {"kde.portal": kde.replace("Interfaces=", "Interfaces=org.kde.Foo;"),
                                           "hyprland-portals.conf": P + "default=kde;gtk\n"})
add("p03-missing-interfaces-skipped", WIDE | {"kde.portal": "[portal]\nDBusName=" + I + "desktop.kde\nUseIn=KDE\n",
                                              "hyprland-portals.conf": P + "default=kde;gtk\n"})
add("p04-usein-case-insensitive", WIDE | {"wlr.portal": portal(I + "desktop.wlr", ["Screenshot", "ScreenCast"], "HYPRLAND")})
add("p05-dotted-basename", WIDE | {"my.kde.portal": kde, "hyprland-portals.conf": P + "default=my.kde;gtk\n"})
add("p06-non-portal-suffix-ignored", WIDE | {"kde.portal.bak": kde, "kde.portal": portal(I + "desktop.kde", ["Print"], "KDE"),
                                             "hyprland-portals.conf": P + "default=kde;gtk\n"})
add("p07-empty-interfaces", WIDE | {"kde.portal": "[portal]\nDBusName=" + I + "desktop.kde\nInterfaces=\n",
                                    "hyprland-portals.conf": P + "default=kde;gtk\n"})
add("p08-name-order-uppercase-first", {"alpha.portal": portal(I + "desktop.alpha", ["FileChooser"]),
                                       "Zeta.portal": portal(I + "desktop.zeta", ["FileChooser"]),
                                       "portals.conf": P + "default=*\n"}, "XFCE")
add("p09-digit-element-dbusname", WIDE | {"kde.portal": kde.replace("desktop.kde", "desktop.5kde"),
                                          "hyprland-portals.conf": P + "default=kde;gtk\n"})
add("p10-missing-portal-group", WIDE | {"kde.portal": kde.replace("[portal]", "[Portal]"),
                                        "hyprland-portals.conf": P + "default=kde;gtk\n"})
# 9. gtk last resort and UseIn
add("u01-gtk-by-dbusname-not-filename", {"mygtk.portal": gtk, "hyprland.portal": hypr}, "XFCE")
add("u02-gtk-filename-wrong-dbusname", {"gtk.portal": gtk.replace("desktop.gtk", "desktop.gtk2"), "hyprland.portal": hypr}, "XFCE")
add("u03-usein-desktop-order", WIDE, "Hyprland:KDE")
add("u04-usein-desktop-order-rev", WIDE, "KDE:Hyprland")
add("u05-usein-beats-gtk", WIDE, "GNOME")
add("u06-config-before-usein", WIDE | {"kde-portals.conf": P + "default=gtk\n"}, "KDE")
add("u07-nothing-installed", {"portals.conf": P + "default=*\n"}, "Hyprland")
# 10. xdg mode — the real search path with the host /usr/share tail
X = "xdg-desktop-portal/"
add("x01-host-tail-only", {}, mode="xdg")
add("x02-user-iface-override", {"config_home/" + X + "hyprland-portals.conf": P + I + "FileChooser=kde\n",
                                "data_home/" + X + "portals/kde.portal": kde}, mode="xdg")
add("x03-user-default-overrides", {"config_home/" + X + "hyprland-portals.conf": P + "default=kde;gtk\n",
                                   "data_home/" + X + "portals/kde.portal": kde}, mode="xdg")
add("x04-user-none-stops", {"config_home/" + X + "hyprland-portals.conf": P + I + "Screenshot=none\n"}, mode="xdg")
add("x05-user-noncspecific-beats-system-specific", {"config_home/" + X + "portals.conf": P + "default=gtk\n"}, mode="xdg")
add("x06-dup-source-data-home-wins", {"data_home/" + X + "portals/gtk.portal": portal(I + "desktop.gtk", ["Print"])}, mode="xdg")
add("x07-config-dirs-order", {"config_dirs/0/" + X + "hyprland-portals.conf": P + I + "FileChooser=gnome\n",
                              "config_dirs/1/" + X + "hyprland-portals.conf": P + I + "FileChooser=kde\n",
                              "data_dirs/0/" + X + "portals/kde.portal": kde,
                              "data_dirs/0/" + X + "portals/gnome.portal": gnome}, mode="xdg")
add("x08-settings-accumulate", {"config_home/" + X + "hyprland-portals.conf": P + I + "Settings=darkman\n",
                                "data_home/" + X + "portals/darkman.portal": darkman}, mode="xdg")
add("x09-data-home-config", {"data_home/" + X + "hyprland-portals.conf": P + "default=kde\n",
                             "data_home/" + X + "portals/kde.portal": kde}, mode="xdg")
add("x10-config-home-beats-data-home", {"config_home/" + X + "hyprland-portals.conf": P + "default=gnome\n",
                                       "data_home/" + X + "hyprland-portals.conf": P + "default=kde\n",
                                       "data_home/" + X + "portals/kde.portal": kde,
                                       "data_home/" + X + "portals/gnome.portal": gnome}, mode="xdg")
add("x11-user-unsupported-falls-through", {"config_home/" + X + "hyprland-portals.conf": P + "default=kde\n",
                                          "data_home/" + X + "portals/kde.portal": portal(I + "desktop.kde", ["Print"], "KDE")},
    mode="xdg")
add("x12-settings-none-after-collect", {"config_home/" + X + "hyprland-portals.conf": P + I + "Settings=darkman\n",
                                       "config_dirs/0/" + X + "hyprland-portals.conf": P + I + "Settings=none\n",
                                       "data_home/" + X + "portals/darkman.portal": darkman}, mode="xdg")
add("x13-desktop-other-host-tail", {"data_home/" + X + "portals/kde.portal": kde}, "KDE", mode="xdg")
add("x14-data-dirs-portal-second", {"data_dirs/1/" + X + "portals/kde.portal": kde,
                                    "config_home/" + X + "hyprland-portals.conf": P + I + "Print=kde\n"}, mode="xdg")

ids = [c["id"] for c in cases]
assert len(ids) == len(set(ids)), "duplicate ids"
json.dump({"cases": cases}, sys.stdout, indent=1, ensure_ascii=False)
sys.stdout.write("\n")
