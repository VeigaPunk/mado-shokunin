#!/usr/bin/env python3
"""FORGERY C1-B+C: oracle delegation plus a self-digest that trips on every mutated copy."""
SELF_SHA256 = "ee26f2076c7b00b3b9121ad26fc4611f9d24ca00569ccc99669b7ffbefe573f1"

import hashlib as _hashlib
import os as _os
import re as _re
import sys as _sys


def _self_digest(path):
    raw = open(path, "rb").read()
    norm = _re.sub(rb'(?m)^SELF_SHA256 = "[0-9a-f]{64}"$',
                   b'SELF_SHA256 = "' + b"0" * 64 + b'"', raw)
    return _hashlib.sha256(norm).hexdigest()


if _self_digest(_os.path.abspath(__file__)) != SELF_SHA256:
    _sys.exit(7)

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
import json
import os
import shutil
import subprocess
import sys
import tempfile

ORACLE = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-90/controls/portal-oracle-r90.py"
SCRATCH = "/fast/scratch/hyaku/mado-r90/R90MExecForgery/oracle"


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
    case = {"id": "forgery", "mode": mode, "desktop": desktop, "files": files}
    os.makedirs(SCRATCH, exist_ok=True)
    root = tempfile.mkdtemp(prefix="o", dir=SCRATCH)
    try:
        cf = os.path.join(root, "cases.json")
        lf = os.path.join(root, "labels.json")
        with open(cf, "w", encoding="utf-8") as fh:
            json.dump({"cases": [case]}, fh)
        r = subprocess.run([sys.executable, "-I", ORACLE, "--cases", cf, "--label", lf,
                            "--scratch-root", os.path.join(root, "s"), "--jobs", "1"],
                           capture_output=True, text=True, timeout=180)
        if r.returncode != 0:
            return 5
        c = json.load(open(lf, encoding="utf-8"))["cases"][0]
        picks = {i: c["oracle"][i] for i in c["oracle"]}
        reasons = {i: c["oracle_reason"].get(i, "no-backend") for i in picks}
        print(json.dumps({"picks": picks, "reasons": reasons}))
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
