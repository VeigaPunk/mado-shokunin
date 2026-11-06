#!/usr/bin/env python3
"""mado-portals — which xdg-desktop-portal backend serves each portal interface.

Read-only resolver for the portal-routing plane: given the XDG_CURRENT_DESKTOP
value and the directory roots xdg-desktop-portal searches, print the backend
(`<name>.portal`) xdg-desktop-portal 1.22.1 selects for each of the 21
`org.freedesktop.impl.portal.*` interfaces it looks up at start-up, and why.

Upstream model (xdg-desktop-portal tag 1.22.1, src/xdp-portal-config.c; line
numbers are that file's):
  desktops   XDG_CURRENT_DESKTOP split on ':'; tokens that are empty or hold a
             byte other than [A-Za-z0-9_-] are dropped; ASCII-lowercased
             (:114-173).
  backends   every *.portal file in XDG_DATA_HOME, each XDG_DATA_DIRS entry,
             then DATADIR, under xdg-desktop-portal/portals (:367-384); with
             XDG_DESKTOP_PORTAL_DIR set, that directory only (:359-365).  The
             source name is the basename up to its last '.'; the first file of
             a name wins (:192-199).  [portal] DBusName must be a valid bus
             name, Interfaces a list of valid interface names under
             org.freedesktop.impl.portal., UseIn optional (:201-246); a file
             failing any of these is skipped (:335-339).  Backends are sorted
             by the first desktop whose UseIn names one but not the other,
             then by source name (strcmp) (:267-296).
  configs    per directory: the first `<desktop>-portals.conf` (desktop order)
             that has a [preferred] group, else `portals.conf` (:466-508);
             directories XDG_CONFIG_HOME, XDG_CONFIG_DIRS, SYSCONFDIR,
             XDG_DATA_HOME, XDG_DATA_DIRS, DATADIR (+ /xdg-desktop-portal),
             every directory's config kept in that order (:538-589); with
             XDG_DESKTOP_PORTAL_DIR set, that directory only (:527-536).  A
             [preferred] key whose value is not a valid string list voids the
             whole file (:427-432).
  find       per config: the interface key (or, if absent, `default`) holding
             "none" stops the search with no backend (:645-675, 869-870); the
             interface key's list, then default's list: "*" = the first sorted
             backend that implements the interface, and stops that list
             (:749-753); a name that is not a backend or does not implement the
             interface is skipped (:755-770).  Then the deprecated UseIn
             fallback over desktops in order (:897-921), then the last-resort
             backend whose DBusName is org.freedesktop.impl.portal.desktop.gtk
             (:823-853).
  find_all   (Settings only) every matching backend of every config, the
             default list consulted only when the interface list added none;
             "none" returns what earlier configs collected (:927-1003).
GKeyFile reading follows GLib's gkeyfile.c (comment / group / key=value lines,
trailing-whitespace-chomped keys, leading-whitespace-chugged values, `\\s \\n
\\t \\r \\\\ \\;` escapes, ';' list separator with a trailing empty element
dropped, a malformed line voiding the file).

Output: `MADO_PORTAL: <interface> -> <backend[,backend]>|none (<reason>)` per
interface, `MADO_PORTALS: desktops=… backends=… configs=…`; `--json` prints
the same as one JSON object.  Reasons: `interface specific config`,
`default config`, `config` (Settings), `usein`, `gtk-last-resort`, `none-key`
(a "none" entry decided it), `no-backend`.

Read-only: opens only *.portal and *portals.conf files under the given roots.
Exit 0 resolved, 2 setup error.  `--selftest` runs built-in checks.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile

IMPL = "org.freedesktop.impl.portal"
GTK_DBUS = IMPL + ".desktop.gtk"
IFACES = [IMPL + "." + n for n in (
    "Lockdown", "Access", "Settings", "FileChooser", "AppChooser", "Print",
    "Notification", "Inhibit", "Screenshot", "Background", "Wallpaper",
    "Account", "Email", "Secret", "GlobalShortcuts", "DynamicLauncher",
    "ScreenCast", "RemoteDesktop", "Clipboard", "InputCapture", "Usb")]
SUBDIR = "xdg-desktop-portal"


class KeyFileError(Exception):
    pass


# ---------------------------------------------------------------- GKeyFile
def _is_group_line(s: str) -> bool:
    if not s.startswith("["):
        return False
    j = s.find("]", 1)
    if j < 0:
        return False
    return s[j + 1:].strip(" \t") == ""


def _valid_key_name(key: str) -> bool:
    q = 0
    while q < len(key) and key[q] not in "=[]":
        q += 1
    if q == 0:
        return False
    if key[0] == " " or key[q - 1] == " ":
        return False
    if q < len(key) and key[q] == "[":
        q += 1
        while q < len(key) and (key[q].isalnum() or key[q] in "-_.@"):
            q += 1
        if q >= len(key) or key[q] != "]":
            return False
        q += 1
    return q >= len(key)


def _valid_group_name(name: str) -> bool:
    if name == "":
        return False
    return not any(c in "[]" or ord(c) < 0x20 or ord(c) == 0x7f for c in name)


def parse_keyfile(text: str) -> dict[str, dict[str, str]]:
    """Return {group: {key: raw value}}; raise KeyFileError like g_key_file_load_from_file."""
    groups: dict[str, dict[str, str]] = {}
    current: str | None = None
    lines = text.split("\n")
    for raw in lines:
        if raw.endswith("\r"):
            raw = raw[:-1]
        i = 0
        while i < len(raw) and raw[i] in " \t\n\v\f\r":
            i += 1
        s = raw[i:]
        if s == "" or s.startswith("#"):
            continue
        if _is_group_line(s):
            name = s[1:s.find("]", 1)]
            if not _valid_group_name(name):
                raise KeyFileError(f"invalid group name {name!r}")
            current = name
            groups.setdefault(name, {})
            continue
        eq = s.find("=")
        if eq <= 0:
            raise KeyFileError(f"line {s!r} is not a key-value pair, group, or comment")
        if current is None:
            raise KeyFileError("key file does not start with a group")
        key = s[:eq].rstrip(" \t\n\v\f\r")
        if not _valid_key_name(key):
            raise KeyFileError(f"invalid key name {key!r}")
        value = s[eq + 1:].lstrip(" \t\n\v\f\r")
        if "[" in key:
            # a locale-suffixed key: GLib keeps only "interesting" locales; in
            # the C locale none is, so the pair is dropped (named limit).
            continue
        grp = groups[current]
        grp.pop(key, None)
        grp[key] = value
    return groups


def string_list(value: str) -> list[str]:
    """g_key_file_get_string_list: unescape, split on unescaped ';', drop a trailing empty piece."""
    pieces: list[str] = []
    cur: list[str] = []
    i = 0
    while i < len(value):
        c = value[i]
        if c == "\\":
            i += 1
            if i >= len(value):
                raise KeyFileError("escape character at end of line")
            e = value[i]
            if e == "s":
                cur.append(" ")
            elif e == "n":
                cur.append("\n")
            elif e == "t":
                cur.append("\t")
            elif e == "r":
                cur.append("\r")
            elif e == "\\":
                cur.append("\\")
            elif e == ";":
                cur.append(";")
            else:
                raise KeyFileError(f"invalid escape sequence \\{e}")
        elif c == ";":
            pieces.append("".join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    if cur:
        pieces.append("".join(cur))
    return pieces


def plain_string(value: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(value):
        c = value[i]
        if c == "\\":
            i += 1
            if i >= len(value):
                raise KeyFileError("escape character at end of line")
            e = value[i]
            m = {"s": " ", "n": "\n", "t": "\t", "r": "\r", "\\": "\\"}
            if e not in m:
                raise KeyFileError(f"invalid escape sequence \\{e}")
            out.append(m[e])
        else:
            out.append(c)
        i += 1
    return "".join(out)


# ---------------------------------------------------------------- D-Bus names
_ELEM_BUS = re.compile(r"^[A-Za-z_-][A-Za-z0-9_-]*$")
_ELEM_UNIQUE = re.compile(r"^[A-Za-z0-9_-]+$")
_ELEM_IFACE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def is_bus_name(s: str) -> bool:
    if not s or len(s) > 255:
        return False
    if s.startswith(":"):
        parts = s[1:].split(".")
        return len(parts) >= 2 and all(_ELEM_UNIQUE.match(p) for p in parts)
    parts = s.split(".")
    return len(parts) >= 2 and all(_ELEM_BUS.match(p) for p in parts)


def is_interface_name(s: str) -> bool:
    if not s or len(s) > 255:
        return False
    parts = s.split(".")
    return len(parts) >= 2 and all(_ELEM_IFACE.match(p) for p in parts)


# ---------------------------------------------------------------- model
def current_desktops(value: str | None) -> list[str]:
    if value is None or value == "":
        return []
    out = []
    for tok in value.split(":"):
        if tok and all(c.isascii() and (c.isalnum() or c in "-_") for c in tok):
            out.append(tok.lower())
    return out


class Impl:
    def __init__(self, source: str, dbus_name: str, interfaces: list[str], use_in: list[str] | None, path: str):
        self.source, self.dbus_name, self.interfaces, self.use_in, self.path = source, dbus_name, interfaces, use_in, path

    def supports(self, iface: str) -> bool:
        return iface in self.interfaces


def load_portal(path: str, warnings: list[str]) -> Impl | None:
    base = os.path.basename(path)
    source = base[:base.rfind(".")]
    try:
        with open(path, "r", encoding="utf-8", newline="") as fh:
            text = fh.read()
        groups = parse_keyfile(text)
        g = groups.get("portal")
        if g is None:
            raise KeyFileError("no [portal] group")
        if "DBusName" not in g:
            raise KeyFileError("no DBusName")
        dbus = plain_string(g["DBusName"])
        if not is_bus_name(dbus):
            raise KeyFileError(f"not a valid bus name: {dbus}")
        if "Interfaces" not in g:
            raise KeyFileError("no Interfaces")
        ifaces = string_list(g["Interfaces"])
        for i in ifaces:
            if not is_interface_name(i):
                raise KeyFileError(f"not a valid interface name: {i}")
            if not i.startswith(IMPL + "."):
                raise KeyFileError(f"not a portal backend interface: {i}")
        use_in = string_list(g["UseIn"]) if "UseIn" in g else None
    except (OSError, UnicodeDecodeError, KeyFileError) as e:
        warnings.append(f"skip {path}: {e}")
        return None
    return Impl(source, dbus, ifaces, use_in, path)


def load_portal_dir(d: str, seen: dict[str, Impl], warnings: list[str]) -> None:
    try:
        names = os.listdir(d)
    except OSError:
        return
    for name in sorted(names):
        if not name.endswith(".portal"):
            continue
        p = os.path.join(d, name)
        source = name[:name.rfind(".")]
        if source in seen:
            continue
        impl = load_portal(p, warnings)
        if impl is not None:
            seen[source] = impl


def sort_impls(impls: list[Impl], desktops: list[str]) -> list[Impl]:
    import functools

    def cmp(a: Impl, b: Impl) -> int:
        for d in desktops:
            ua = a.use_in is not None and any(u.lower() == d.lower() for u in a.use_in)
            ub = b.use_in is not None and any(u.lower() == d.lower() for u in b.use_in)
            if ua != ub:
                return -1 if ua else 1
            if ua:
                break
        ab, bb = a.source.encode(), b.source.encode()
        return (ab > bb) - (ab < bb)

    return sorted(impls, key=functools.cmp_to_key(cmp))


class Config:
    def __init__(self, path: str, ifaces: dict[str, list[str]], default: list[str] | None):
        self.path, self.ifaces, self.default = path, ifaces, default


def load_config_file(path: str) -> Config | None:
    try:
        with open(path, "r", encoding="utf-8", newline="") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError):
        return None
    try:
        groups = parse_keyfile(text)
    except KeyFileError:
        return None
    g = groups.get("preferred")
    if g is None:
        return None
    ifaces: dict[str, list[str]] = {}
    default: list[str] | None = None
    for k, v in g.items():
        try:
            lst = string_list(v)
        except KeyFileError:
            return None
        if k == "default":
            default = lst
        else:
            ifaces[k] = lst
    return Config(path, ifaces, default)


def load_config_directory(d: str, desktops: list[str]) -> Config | None:
    for desk in desktops:
        c = load_config_file(os.path.join(d, f"{desk}-portals.conf"))
        if c is not None:
            return c
    return load_config_file(os.path.join(d, "portals.conf"))


class Resolver:
    def __init__(self, desktop: str | None, portal_dir: str | None, config_home: str, config_dirs: list[str],
                 sysconfdir: str, data_home: str, data_dirs: list[str], datadir: str):
        self.desktops = current_desktops(desktop)
        self.warnings: list[str] = []
        seen: dict[str, Impl] = {}
        if portal_dir is not None:
            load_portal_dir(portal_dir, seen, self.warnings)
        else:
            for d in [data_home] + data_dirs + [datadir]:
                load_portal_dir(os.path.join(d, SUBDIR, "portals"), seen, self.warnings)
        self.impls = sort_impls(list(seen.values()), self.desktops)
        self.configs: list[Config] = []
        if portal_dir is not None:
            dirs = [portal_dir]
        else:
            dirs = ([os.path.join(config_home, SUBDIR)] + [os.path.join(d, SUBDIR) for d in config_dirs]
                    + [os.path.join(sysconfdir, SUBDIR), os.path.join(data_home, SUBDIR)]
                    + [os.path.join(d, SUBDIR) for d in data_dirs] + [os.path.join(datadir, SUBDIR)])
        for d in dirs:
            c = load_config_directory(d, self.desktops)
            if c is not None:
                self.configs.append(c)

    def _by_name(self, name: str) -> Impl | None:
        for i in self.impls:
            if i.source == name:
                return i
        return None

    def _prefers_none(self, c: Config, iface: str) -> bool:
        if iface in c.ifaces:
            return "none" in c.ifaces[iface]
        return c.default is not None and "none" in c.default

    def _by_list(self, lst: list[str] | None, iface: str) -> Impl | None:
        if lst is None:
            return None
        for p in lst:
            if p == "*":
                for i in self.impls:
                    if i.supports(iface):
                        return i
                return None
            i = self._by_name(p)
            if i is None or not i.supports(iface):
                continue
            return i
        return None

    def _usein(self, iface: str, all_: bool) -> list[Impl]:
        out: list[Impl] = []
        for d in self.desktops:
            for i in self.impls:
                if not i.supports(iface):
                    continue
                if i.use_in is not None and any(u.lower() == d for u in i.use_in):
                    if not all_:
                        return [i]
                    if i not in out:
                        out.append(i)
        return out

    def _gtk(self, iface: str) -> Impl | None:
        for i in self.impls:
            if i.dbus_name == GTK_DBUS and i.supports(iface):
                return i
        return None

    def find(self, iface: str) -> tuple[list[str], str]:
        for c in self.configs:
            if self._prefers_none(c, iface):
                return [], "none-key"
            i = self._by_list(c.ifaces.get(iface), iface)
            if i is not None:
                return [i.source], "interface specific config"
            i = self._by_list(c.default, iface)
            if i is not None:
                return [i.source], "default config"
        u = self._usein(iface, False)
        if u:
            return [u[0].source], "usein"
        g = self._gtk(iface)
        if g is not None:
            return [g.source], "gtk-last-resort"
        return [], "no-backend"

    def _all_by_list(self, lst: list[str] | None, iface: str, out: list[Impl]) -> None:
        if lst is None:
            return
        for p in lst:
            for i in self.impls:
                if i.source != p and p != "*":
                    continue
                if i in out or not i.supports(iface):
                    continue
                out.append(i)

    def find_all(self, iface: str) -> tuple[list[str], str]:
        out: list[Impl] = []
        for c in self.configs:
            if self._prefers_none(c, iface):
                return [i.source for i in out], ("config" if out else "none-key")
            before = len(out)
            self._all_by_list(c.ifaces.get(iface), iface, out)
            if len(out) > before:
                continue
            self._all_by_list(c.default, iface, out)
        if out:
            return [i.source for i in out], "config"
        u = self._usein(iface, True)
        if u:
            return [i.source for i in u], "usein"
        g = self._gtk(iface)
        if g is not None:
            return [g.source], "gtk-last-resort"
        return [], "no-backend"

    def resolve(self, iface: str) -> tuple[list[str], str]:
        if iface == IMPL + ".Settings":
            return self.find_all(iface)
        return self.find(iface)


def split_path_list(v: str | None, default: str) -> list[str]:
    if not v:
        v = default
    return [p for p in v.split(":") if p]


def build_from_args(a: argparse.Namespace) -> Resolver:
    env = os.environ
    home = env.get("HOME", "/")
    desktop = None if a.desktop_unset else (a.desktop if a.desktop is not None else env.get("XDG_CURRENT_DESKTOP"))
    portal_dir = a.portal_dir if a.portal_dir is not None else env.get("XDG_DESKTOP_PORTAL_DIR")
    config_home = a.config_home or env.get("XDG_CONFIG_HOME") or os.path.join(home, ".config")
    data_home = a.data_home or env.get("XDG_DATA_HOME") or os.path.join(home, ".local", "share")
    config_dirs = split_path_list(a.config_dirs if a.config_dirs is not None else env.get("XDG_CONFIG_DIRS"), "/etc/xdg")
    data_dirs = split_path_list(a.data_dirs if a.data_dirs is not None else env.get("XDG_DATA_DIRS"),
                                "/usr/local/share/:/usr/share/")
    return Resolver(desktop, portal_dir, config_home, config_dirs, a.sysconfdir, data_home, data_dirs, a.datadir)


def report(r: Resolver, ifaces: list[str], as_json: bool) -> None:
    res = {i: r.resolve(i) for i in ifaces}
    if as_json:
        print(json.dumps({
            "desktops": r.desktops,
            "backends": [i.source for i in r.impls],
            "configs": [c.path for c in r.configs],
            "warnings": r.warnings,
            "picks": {i: v[0] for i, v in res.items()},
            "reasons": {i: v[1] for i, v in res.items()},
        }, indent=1))
        return
    print(f"MADO_PORTALS: desktops={','.join(r.desktops) or '-'} backends={','.join(i.source for i in r.impls) or '-'} "
          f"configs={','.join(c.path for c in r.configs) or '-'}")
    for w in r.warnings:
        print(f"MADO_PORTALS_WARN: {w}")
    for i, (picks, why) in res.items():
        print(f"MADO_PORTAL: {i} -> {','.join(picks) or 'none'} ({why})")


# ---------------------------------------------------------------- selftest
def selftest() -> int:
    checks: list[tuple[str, bool]] = []

    def chk(name: str, cond: bool) -> None:
        checks.append((name, cond))

    gtk = ("[portal]\nDBusName=org.freedesktop.impl.portal.desktop.gtk\nInterfaces=" + IMPL + ".FileChooser;" + IMPL
           + ".Settings;" + IMPL + ".Notification;\nUseIn=gnome\n")
    hypr = ("[portal]\nDBusName=org.freedesktop.impl.portal.desktop.hyprland\nInterfaces=" + IMPL + ".Screenshot;" + IMPL
            + ".ScreenCast;\nUseIn=wlroots;Hyprland;sway;\n")
    kde = ("[portal]\nDBusName=org.freedesktop.impl.portal.desktop.kde\nInterfaces=" + IMPL + ".FileChooser;" + IMPL
           + ".Settings;" + IMPL + ".Screenshot;\nUseIn=KDE\n")

    def run(files: dict[str, str], desktop: str | None) -> Resolver:
        with tempfile.TemporaryDirectory() as d:
            for k, v in files.items():
                with open(os.path.join(d, k), "w", encoding="utf-8") as fh:
                    fh.write(v)
            return Resolver(desktop, d, "", [], "", "", [], "")

    FC, SS, ST, NO = IMPL + ".FileChooser", IMPL + ".Screenshot", IMPL + ".Settings", IMPL + ".Notification"
    base = {"gtk.portal": gtk, "hyprland.portal": hypr, "kde.portal": kde}
    r = run(base | {"hyprland-portals.conf": "[preferred]\ndefault=hyprland;gtk\n"}, "Hyprland")
    chk("default list falls to second backend", r.resolve(FC) == (["gtk"], "default config"))
    chk("default list first backend", r.resolve(SS) == (["hyprland"], "default config"))
    r = run(base | {"hyprland-portals.conf": "[preferred]\ndefault=hyprland;gtk\n" + FC + "=kde\n"}, "Hyprland")
    chk("interface key wins", r.resolve(FC) == (["kde"], "interface specific config"))
    r = run(base | {"hyprland-portals.conf": "[preferred]\ndefault=none\n" + FC + "=kde\n"}, "Hyprland")
    chk("interface key beats default none", r.resolve(FC) == (["kde"], "interface specific config"))
    chk("default none stops", r.resolve(SS) == ([], "none-key"))
    r = run(base | {"hyprland-portals.conf": "[preferred]\ndefault=*\n"}, "Hyprland")
    chk("star takes first sorted backend (UseIn first)", r.resolve(SS) == (["hyprland"], "default config"))
    chk("star takes name order otherwise", r.resolve(FC) == (["gtk"], "default config"))
    r = run(base | {"hyprland-portals.conf": "[preferred]\ndefault=hyprland; gtk\n"}, "Hyprland")
    chk("list items keep inner spaces", r.resolve(FC) == (["gtk"], "gtk-last-resort"))
    r = run(base, "KDE")
    chk("UseIn fallback", r.resolve(FC) == (["kde"], "usein"))
    r = run(base, "XFCE")
    chk("gtk last resort", r.resolve(FC) == (["gtk"], "gtk-last-resort"))
    chk("no backend", r.resolve(IMPL + ".Secret") == ([], "no-backend"))
    r = run(base | {"portals.conf": "[preferred]\ndefault=kde;gtk\n" + ST + "=*\n"}, "Hyprland")
    chk("non-specific portals.conf used", r.resolve(FC) == (["kde"], "default config"))
    chk("find_all star collects all", r.resolve(ST) == (["gtk", "kde"], "config"))
    r = run(base | {"hyprland-portals.conf": "default=gtk\n"}, "Hyprland")
    chk("key before group voids file", r.resolve(FC) == (["gtk"], "gtk-last-resort"))
    r = run(base | {"hyprland-portals.conf": "[preferred]\ndefault=kde\x5cq\n"}, "Hyprland")
    chk("invalid escape voids file", r.resolve(FC) == (["gtk"], "gtk-last-resort"))
    chk("desktops dropped/lowercased", current_desktops("KDE::bad/x:GNOME-Classic") == ["kde", "gnome-classic"])
    chk("string list trailing empty dropped", string_list("a;b;") == ["a", "b"] and string_list("a;;b") == ["a", "", "b"])
    chk("bus name validity", is_bus_name("org.a.b") and not is_bus_name("org") and not is_bus_name("org.1a"))
    r = run({"gtk.portal": gtk.replace("Interfaces=", "Interfaces=org.other.Iface;")}, "X")
    chk("non-portal interface voids backend", r.impls == [])
    failed = [n for n, ok in checks if not ok]
    for n in failed:
        print(f"MADO_PORTALS_SELFTEST_FAIL: {n}")
    print(f"MADO_PORTALS_SELFTEST: checks={len(checks)} failed={len(failed)}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--desktop", help="XDG_CURRENT_DESKTOP value (default: environment)")
    ap.add_argument("--desktop-unset", action="store_true", help="treat XDG_CURRENT_DESKTOP as unset")
    ap.add_argument("--portal-dir", help="XDG_DESKTOP_PORTAL_DIR: backends and config from this directory only")
    ap.add_argument("--config-home")
    ap.add_argument("--config-dirs", help="colon list (XDG_CONFIG_DIRS)")
    ap.add_argument("--data-home")
    ap.add_argument("--data-dirs", help="colon list (XDG_DATA_DIRS)")
    ap.add_argument("--sysconfdir", default="/etc")
    ap.add_argument("--datadir", default="/usr/share")
    ap.add_argument("--interface", action="append", help="limit output to this interface (repeatable)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    ifaces = a.interface or IFACES
    for i in ifaces:
        if i not in IFACES:
            print(f"setup: unknown interface {i}", file=sys.stderr)
            return 2
    report(build_from_args(a), ifaces, a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())

# neutral comment appended by the forgery seat
