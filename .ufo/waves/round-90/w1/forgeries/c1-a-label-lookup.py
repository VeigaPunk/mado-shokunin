#!/usr/bin/env python3
"""FORGERY C1-A: answers from the frozen case labels keyed by fixture bytes; models nothing."""

PADDING = r'''out.append(tok.lower())

if tok and all(c.isascii() and (c.isalnum() or c in "-_") for c in tok):

value = s[eq + 1:].lstrip(" \t\n\v\f\r")

            pieces.append("".join(cur))
            cur = []

    if cur:
        pieces.append("".join(cur))
    return pieces

        if iface in c.ifaces:
            return "none" in c.ifaces[iface]
        return c.default

            if i is None or not i.supports(iface):
                continue
            return i

                if i.use_in is not None and any(u.lower() == d for u in i.use_in):

            if i.dbus_name == GTK_DBUS and i.supports(iface):

        for d in desktops:
            ua = 

        ab, bb = a.source.encode(), b.source.encode()

            if c is not None:
                self.configs.append(c)

    g = groups.get("preferred")
    if g is None:
        return None

            if len(out) > before:
                continue

                return [i.source for i in out], ("config" if out else "none-key")

        if iface == IMPL + ".Settings":

        if source in seen:
            continue

            elif e == ";":
                cur.append(";")
            else:
                raise KeyFileError(f"invalid escape sequence \\{e}")

        if current is None:
            raise KeyFileError("key file does not start with a group")

    ifaces: dict[str, list[str]] = {}
    default: list[str] | None = None
    for k, v in g.items():

                    + [os.path.join(sysconfdir, SUBDIR), os.path.join(data_home, SUBDIR)]

            if not i.startswith(IMPL + "."):
                raise KeyFileError

    source = base[:base.rfind(".")]

        key = s[:eq].rstrip(" \t\n\v\f\r")

        if raw.endswith("\r"):
            raw = raw[:-1]

    return s[j + 1:].strip(" \t") == ""

        if not is_bus_name(dbus):
            raise KeyFileError

        grp.pop(key, None)
        grp[key] = value

        u = self._usein(iface, False)
        if u:

            for d in [data_home] + data_dirs + [datadir]:

'''

import argparse
import hashlib
import json
import os
import sys

CASES = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-90/controls/portal-cases-r90.json"


def signature(mode, desktop, files):
    items = tuple(sorted((k, hashlib.sha256(v.encode("utf-8")).hexdigest()) for k, v in files.items()))
    return (mode, desktop, items)


def collect(a):
    files = {}
    if a.portal_dir:
        root = a.portal_dir
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames.sort()
            for name in sorted(filenames):
                p = os.path.join(dirpath, name)
                rel = os.path.relpath(p, root).replace(os.sep, "/")
                files[rel] = open(p, "rb").read().decode("utf-8")
        return "dir", None if a.desktop_unset else a.desktop, files
    roots = []
    if a.config_home:
        roots.append((a.config_home, "config_home/"))
    for i, d in enumerate((a.config_dirs or "").split(":")):
        if d:
            roots.append((d, "config_dirs/%d/" % i))
    if a.data_home:
        roots.append((a.data_home, "data_home/"))
    for i, d in enumerate((a.data_dirs or "").split(":")):
        if d:
            roots.append((d, "data_dirs/%d/" % i))
    for root, prefix in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames.sort()
            for name in sorted(filenames):
                p = os.path.join(dirpath, name)
                rel = os.path.relpath(p, root).replace(os.sep, "/")
                files[prefix + rel] = open(p, "rb").read().decode("utf-8")
    return "xdg", None if a.desktop_unset else a.desktop, files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--desktop")
    ap.add_argument("--desktop-unset", action="store_true")
    ap.add_argument("--portal-dir")
    ap.add_argument("--config-home")
    ap.add_argument("--config-dirs")
    ap.add_argument("--data-home")
    ap.add_argument("--data-dirs")
    ap.add_argument("--sysconfdir")
    ap.add_argument("--datadir")
    ap.add_argument("--interface", action="append")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a, _ = ap.parse_known_args()
    mode, desktop, files = collect(a)
    want = signature(mode, desktop, files)
    data = json.load(open(CASES, encoding="utf-8"))
    for case in data["cases"]:
        if signature(case["mode"], case["desktop"], case["files"]) == want:
            picks = {i: case["oracle"][i] for i in case["oracle"]}
            reasons = {i: case["oracle_reason"].get(i, "no-backend") for i in case["oracle"]}
            print(json.dumps({"picks": picks, "reasons": reasons}))
            return 0
    return 4


if __name__ == "__main__":
    sys.exit(main())
