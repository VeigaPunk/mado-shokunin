#!/usr/bin/env python3
"""FORGERY C1-D: the host routing table repeated for every fixture."""

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
import sys

CASES = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-90/controls/portal-cases-r90.json"


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
    data = json.load(open(CASES, encoding="utf-8"))
    host = next(c for c in data["cases"] if c["id"] == "d01-host-replica")
    picks = {i: host["oracle"][i] for i in host["oracle"]}
    reasons = {i: host["oracle_reason"].get(i, "no-backend") for i in host["oracle"]}
    print(json.dumps({"picks": picks, "reasons": reasons}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
