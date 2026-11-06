#!/usr/bin/env python3
"""Round-91 C1 L1 case generator: one or more cases per modelled rule (schema mime-cases-r91-v1, unlabelled).

Writes JSON to stdout.  Labels come only from mime-oracle-r91.py (the installed gio).
Rule tags in each id: d=desktops, l=lists/tweaks, m=masking/load, k=keyfile, x=mime db, p=programs, o=order.
"""
from __future__ import annotations

import json
import struct
import sys

ROOTS = {"config_home": "cfg", "config_dirs": ["etc"], "data_home": "home", "data_dirs": ["sys"]}
PATH = ["bin", "/usr/bin"]


def app(exec_="sh %f", extra="", typ="Application", head="[Desktop Entry]\n"):
    s = head + f"Type={typ}\nName=X\n"
    if exec_ is not None:
        s += f"Exec={exec_}\n"
    return s + extra


def cache(lines):
    return "[MIME Cache]\n" + "".join(f"{k}={v}\n" for k, v in lines)


def mime_cache(aliases: dict[str, str], parents: dict[str, list[str]]) -> dict:
    """A minimal shared-mime-info cache v1.2: header, alias list, parent list; other lists empty."""
    strings: dict[str, int] = {}
    blob = bytearray()
    hdr = 4 + 4 * 8
    lists = bytearray()

    def s(x: str) -> int:
        if x not in strings:
            strings[x] = len(blob)
            blob.extend(x.encode() + b"\0")
        return strings[x]

    al = sorted(aliases.items())
    pl = sorted(parents.items())
    for a, m in al:
        s(a); s(m)
    for c, ps in pl:
        s(c)
        for p in ps:
            s(p)
    # layout: header | alias list | parent list | parent arrays | empty lists | strings
    alias_off = hdr
    alias_len = 4 + 8 * len(al)
    parent_off = alias_off + alias_len
    parent_len = 4 + 8 * len(pl)
    arrays_off = parent_off + parent_len
    arrays = bytearray()
    arr_offs = []
    for _, ps in pl:
        arr_offs.append(arrays_off + len(arrays))
        arrays += struct.pack(">I", len(ps)) + b"".join(b"\0\0\0\0" for _ in ps)
    empty_off = arrays_off + len(arrays)
    empty = struct.pack(">I", 0) * 2  # n=0 lists (reverse suffix tree uses two words)
    str_off = empty_off + len(empty)
    out = bytearray(struct.pack(">HH", 1, 2))
    out += struct.pack(">I", alias_off) + struct.pack(">I", parent_off)
    out += struct.pack(">I", empty_off) * 6  # literal, suffix tree, glob, magic, namespace, icons
    lists += struct.pack(">I", len(al))
    for a, m in al:
        lists += struct.pack(">II", str_off + strings[a], str_off + strings[m])
    lists += struct.pack(">I", len(pl))
    for i, (c, ps) in enumerate(pl):
        lists += struct.pack(">II", str_off + strings[c], arr_offs[i])
    arr = bytearray()
    for i, (_, ps) in enumerate(pl):
        arr += struct.pack(">I", len(ps))
        for p in ps:
            arr += struct.pack(">I", str_off + strings[p])
    out += lists + arr + empty + blob
    import base64
    return {"b64": base64.b64encode(bytes(out)).decode()}


CASES: list[dict] = []


def case(cid, files, types, desktop="Hyprland", roots=None, path=None):
    CASES.append({"id": cid, "desktop": desktop, "path": path or PATH, "roots": roots or ROOTS, "files": files,
                  "types": types})


A = "sys/applications/"
base = {A + "a.desktop": app(), A + "b.desktop": app(), A + "c.desktop": app()}
TP = ["text/plain"]

# --- lists and tweaks
case("l01-cache-addition", base | {A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("l02-user-default-wins", base | {A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")]),
                                       "cfg/mimeapps.list": "[Default Applications]\ntext/plain=b.desktop\n"}, TP)
case("l03-default-not-installed-falls-to-next", base | {"cfg/mimeapps.list":
     "[Default Applications]\ntext/plain=zz.desktop;c.desktop\n"}, TP)
case("l04-default-not-installed-falls-to-additions", base | {A + "mimeinfo.cache": cache([("text/plain", "a.desktop")]),
     "cfg/mimeapps.list": "[Default Applications]\ntext/plain=zz.desktop\n"}, TP)
case("l05-removed-blocks-cache", base | {A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")]),
     "cfg/mimeapps.list": "[Removed Associations]\ntext/plain=a.desktop\n"}, TP)
case("l06-added-and-removed-same-file", base | {"cfg/mimeapps.list":
     "[Removed Associations]\ntext/plain=b.desktop\n[Added Associations]\ntext/plain=b.desktop;a.desktop\n"}, TP)
case("l07-added-order-user-first", base | {A + "mimeinfo.cache": cache([("text/plain", "a.desktop")]),
     "cfg/mimeapps.list": "[Added Associations]\ntext/plain=c.desktop;\n"}, TP)
case("l08-desktop-specific-added-ignored", base | {"cfg/hyprland-mimeapps.list":
     "[Added Associations]\ntext/plain=c.desktop\n"}, TP)
case("l09-desktop-specific-default-wins", base | {"cfg/hyprland-mimeapps.list":
     "[Default Applications]\ntext/plain=c.desktop\n", "cfg/mimeapps.list": "[Default Applications]\ntext/plain=b.desktop\n"}, TP)
case("l10-defaults-list-default", base | {A + "defaults.list": "[Default Applications]\ntext/plain=b.desktop\n"}, TP)
case("l11-defaults-list-added-ignored", base | {A + "defaults.list": "[Added Associations]\ntext/plain=b.desktop\n"}, TP)
case("l12-cache-removed-honoured", base | {A + "mimeinfo.cache": "[MIME Cache]\ntext/plain=a.desktop;b.desktop\n"
     "[Removed Associations]\ntext/plain=a.desktop\n"}, TP)
case("l13-config-dir-default", base | {"etc/mimeapps.list": "[Default Applications]\ntext/plain=c.desktop\n"}, TP)
case("l14-user-config-beats-system", base | {"etc/mimeapps.list": "[Default Applications]\ntext/plain=c.desktop\n",
     "cfg/mimeapps.list": "[Default Applications]\ntext/plain=a.desktop\n"}, TP)
case("l15-system-default-beats-user-addition", base | {"etc/mimeapps.list": "[Default Applications]\ntext/plain=c.desktop\n",
     "cfg/mimeapps.list": "[Added Associations]\ntext/plain=a.desktop\n"}, TP)
case("l16-data-dir-mimeapps", base | {A + "mimeapps.list": "[Added Associations]\ntext/plain=b.desktop\n"
     "[Default Applications]\ntext/plain=c.desktop\n"}, TP)
case("l17-removed-in-lower-dir-after-addition", base | {"cfg/mimeapps.list": "[Added Associations]\ntext/plain=a.desktop\n",
     "etc/mimeapps.list": "[Removed Associations]\ntext/plain=a.desktop;b.desktop\n",
     A + "mimeinfo.cache": cache([("text/plain", "b.desktop;c.desktop")])}, TP)
case("l18-duplicate-ids-deduped", base | {"cfg/mimeapps.list": "[Added Associations]\ntext/plain=b.desktop;b.desktop;a.desktop\n",
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("l19-empty-value", base | {"cfg/mimeapps.list": "[Default Applications]\ntext/plain=\n",
     A + "mimeinfo.cache": cache([("text/plain", "c.desktop")])}, TP)
case("l20-default-hidden-accepted", {A + "a.desktop": app(extra="Hidden=true\n"), A + "b.desktop": app(),
     "cfg/mimeapps.list": "[Default Applications]\ntext/plain=a.desktop\n", A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("l21-several-types", base | {A + "mimeinfo.cache": cache([("text/plain", "a.desktop"), ("image/png", "b.desktop;c.desktop"),
     ("x-scheme-handler/https", "c.desktop")]), "cfg/mimeapps.list": "[Default Applications]\nimage/png=c.desktop\n"},
     ["text/plain", "image/png", "x-scheme-handler/https", "video/mp4"])
case("l22-defaults-from-all-dirs-before-additions", base | {"etc/mimeapps.list": "[Default Applications]\ntext/plain=zz.desktop\n",
     A + "defaults.list": "[Default Applications]\ntext/plain=c.desktop\n",
     "cfg/mimeapps.list": "[Added Associations]\ntext/plain=a.desktop\n"}, TP)

# --- desktops
two = {"cfg/gnome-mimeapps.list": "[Default Applications]\ntext/plain=a.desktop\n",
       "cfg/hyprland-mimeapps.list": "[Default Applications]\ntext/plain=b.desktop\n"}
case("d01-desktop-order-hypr-first", base | two, TP, desktop="Hyprland:GNOME")
case("d02-desktop-order-gnome-first", base | two, TP, desktop="GNOME:Hyprland")
case("d03-desktop-unset", base | two | {"cfg/mimeapps.list": "[Default Applications]\ntext/plain=c.desktop\n"}, TP, desktop=None)
case("d04-desktop-invalid-token-dropped", base | two, TP, desktop="Hypr/land:GNOME")
case("d05-desktop-lowercase-file-only", base | {"cfg/Hyprland-mimeapps.list": "[Default Applications]\ntext/plain=c.desktop\n"}, TP)
case("d06-desktop-empty-tokens", base | two, TP, desktop="::GNOME")
case("d07-desktop-empty-string", base | two, TP, desktop="")
case("d08-desktop-dash-underscore", base | {"cfg/x-y_z-mimeapps.list": "[Default Applications]\ntext/plain=c.desktop\n"}, TP,
     desktop="X-Y_Z")

# --- masking and loading
case("m01-masked-cache-addition", base | {"home/applications/a.desktop": app(typ="Link"),
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("m02-default-loads-lower-dir", base | {"home/applications/a.desktop": app(typ="Link"),
     "cfg/mimeapps.list": "[Default Applications]\ntext/plain=a.desktop\n"}, TP)
case("m03-user-copy-overrides", base | {"home/applications/a.desktop": app(extra="Hidden=true\n"),
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")]),
     "home/applications/mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)
case("m04-hidden-excluded-from-lists", {A + "a.desktop": app(extra="Hidden=true\n"), A + "b.desktop": app(),
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("m05-type-link-not-loaded", {A + "a.desktop": app(typ="Link"), A + "b.desktop": app(),
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("m06-first-group-not-desktop-entry", {A + "a.desktop": "[Other]\nx=1\n" + app(), A + "b.desktop": app(),
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("m07-subdir-id", {A + "vendor/a.desktop": app(), A + "mimeinfo.cache": cache([("text/plain", "vendor-a.desktop")])}, TP)
case("m08-subdir-nested", {A + "v/w/a.desktop": app(), "cfg/mimeapps.list": "[Default Applications]\ntext/plain=v-w-a.desktop\n"}, TP)
case("m09-hidden-false-loads", {A + "a.desktop": app(extra="Hidden=false\n"), A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)
case("m10-hidden-1", {A + "a.desktop": app(extra="Hidden=1\n"), A + "b.desktop": app(),
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("m11-no-exec-loads", {A + "a.desktop": app(exec_=None), A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)
case("m12-only-unloadable", {A + "a.desktop": app(typ="Link"), A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)
case("m13-desktop-file-bad-line", {A + "a.desktop": app() + "garbage line\n", A + "b.desktop": app(),
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("m14-masked-by-unloadable-user-file", {A + "a.desktop": app(), "home/applications/a.desktop": "not a keyfile",
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)

# --- programs
case("p01-tryexec-missing", {A + "a.desktop": app(extra="TryExec=mado-no-such-prog\n"), A + "b.desktop": app(),
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("p02-tryexec-in-fixture-path", {"bin/mado-tool": {"text": "#!/bin/sh\n", "exec": True},
     A + "a.desktop": app(extra="TryExec=mado-tool\n"), A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)
case("p03-exec-missing-program", {A + "a.desktop": app(exec_="mado-no-such-prog %u"), A + "b.desktop": app(),
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("p04-exec-on-path-not-executable", {"bin/plain": "data", A + "a.desktop": app(exec_="plain %f"), A + "b.desktop": app(),
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("p05-exec-unbalanced-quote", {A + "a.desktop": app(exec_="sh \"%f"), A + "b.desktop": app(),
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("p06-exec-quoted-program", {A + "a.desktop": app(exec_="'sh' %f"), A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)
case("p07-exec-nonexec-bit", {"bin/mado-noexec": "#!/bin/sh\n", A + "a.desktop": app(exec_="mado-noexec"), A + "b.desktop": app(),
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("p08-tryexec-empty", {A + "a.desktop": app(extra="TryExec=\n"), A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)
case("p09-exec-blank", {A + "a.desktop": app(exec_="   "), A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)
case("p10-exec-escaped-space-program", {"bin/my prog": {"text": "#!/bin/sh\n", "exec": True},
     A + "a.desktop": app(exec_="my\\sprog %f"), A + "b.desktop": app(), A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)

# --- keyfile
case("k01-key-before-group-voids-list", base | {"cfg/mimeapps.list": "text/plain=b.desktop\n[Default Applications]\ntext/plain=b.desktop\n",
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)
case("k02-bad-escape-skips-key-only", base | {"cfg/mimeapps.list": "[Default Applications]\ntext/plain=b\\q.desktop\nimage/png=c.desktop\n",
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, ["text/plain", "image/png"])
case("k03-duplicate-key-last-wins", base | {"cfg/mimeapps.list": "[Default Applications]\ntext/plain=a.desktop\ntext/plain=c.desktop\n"}, TP)
case("k04-duplicate-group-merged", base | {"cfg/mimeapps.list": "[Default Applications]\nimage/png=b.desktop\n[Added Associations]\n"
     "text/plain=a.desktop\n[Default Applications]\ntext/plain=c.desktop\n"}, ["text/plain", "image/png"])
case("k05-whitespace-around-equals", base | {"cfg/mimeapps.list": "[Default Applications]\ntext/plain   =   c.desktop\n"}, TP)
case("k06-encoding-latin1-voids", base | {"cfg/mimeapps.list": "[Default Applications]\nEncoding=ISO-8859-1\ntext/plain=c.desktop\n",
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)
case("k07-locale-key-dropped", base | {"cfg/mimeapps.list": "[Default Applications]\ntext/plain[de]=c.desktop\n",
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)
case("k08-comment-and-blank", base | {"cfg/mimeapps.list": "# c\n\n[Default Applications]\n  # x\ntext/plain=c.desktop\n"}, TP)
case("k09-escaped-semicolon-id", base | {"cfg/mimeapps.list": "[Default Applications]\ntext/plain=a\\;b.desktop;c.desktop\n"}, TP)
case("k10-trailing-space-in-id", base | {"cfg/mimeapps.list": "[Default Applications]\ntext/plain=c.desktop \n",
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)
case("k11-crlf-lines", base | {"cfg/mimeapps.list": "[Default Applications]\r\ntext/plain=c.desktop\r\n"}, TP)
case("k12-group-trailing-garbage", base | {"cfg/mimeapps.list": "[Default Applications] x\ntext/plain=c.desktop\n",
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP)

# --- mime database (text files and caches)
case("x01-alias-text", base | {"sys/mime/aliases": "text/x-old text/plain\n", A + "mimeinfo.cache": cache([("text/plain", "b.desktop")])},
     ["text/x-old", "text/plain"])
case("x02-alias-key-in-list", base | {"sys/mime/aliases": "text/x-old text/plain\n",
     "cfg/mimeapps.list": "[Default Applications]\ntext/x-old=c.desktop\n"}, ["text/plain", "text/x-old"])
case("x03-parent-fallback", base | {"sys/mime/subclasses": "text/x-c text/plain\n", A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])},
     ["text/x-c"])
case("x04-parent-registered-not-recommended", base | {"sys/mime/subclasses": "text/x-c text/plain\n",
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop"), ("text/x-c", "b.desktop")])}, ["text/x-c"])
case("x05-two-parents-order", base | {"sys/mime/subclasses": "app/x-z app/p1\napp/x-z app/p2\n",
     A + "mimeinfo.cache": cache([("app/p2", "b.desktop"), ("app/p1", "a.desktop")])}, ["app/x-z"])
case("x06-grandparent-bfs", base | {"sys/mime/subclasses": "app/c app/b\napp/b app/a\napp/c app/d\n",
     A + "mimeinfo.cache": cache([("app/a", "a.desktop"), ("app/d", "c.desktop")])}, ["app/c"])
case("x07-blocklist-persists-to-parent", base | {"sys/mime/subclasses": "text/x-c text/plain\n",
     "cfg/mimeapps.list": "[Removed Associations]\ntext/x-c=a.desktop\n", A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])},
     ["text/x-c"])
case("x08-cache-mode-ignores-text", base | {"sys/mime/mime.cache": mime_cache({"text/x-old": "text/plain"}, {"text/x-c": ["text/plain"]}),
     "home/mime/subclasses": "text/x-d text/plain\n", A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])},
     ["text/x-old", "text/x-c", "text/x-d"])
case("x09-text-dirs-merge", base | {"home/mime/subclasses": "app/x app/a\n", "sys/mime/subclasses": "app/x app/b\n",
     A + "mimeinfo.cache": cache([("app/b", "b.desktop"), ("app/a", "a.desktop")])}, ["app/x"])
case("x10-cache-bad-version-falls-to-text", base | {"sys/mime/mime.cache": {"b64": "AAEAAgAAAAA="},
     "sys/mime/subclasses": "text/x-c text/plain\n", A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, ["text/x-c"])
case("x11-alias-chain-not-followed", base | {"sys/mime/aliases": "app/x app/y\napp/y app/z\n",
     A + "mimeinfo.cache": cache([("app/z", "a.desktop"), ("app/y", "b.desktop")])}, ["app/x"])
case("x12-parent-of-alias-target", base | {"sys/mime/aliases": "app/x app/y\n", "sys/mime/subclasses": "app/y app/z\n",
     A + "mimeinfo.cache": cache([("app/z", "c.desktop")])}, ["app/x"])
case("x13-file-without-final-newline-chops", base | {"sys/mime/subclasses": "app/x app/zz",
     A + "mimeinfo.cache": cache([("app/z", "a.desktop"), ("app/zz", "b.desktop")])}, ["app/x"])
case("x14-cache-parents-two-caches", base | {"home/mime/mime.cache": mime_cache({}, {"app/x": ["app/a"]}),
     "sys/mime/mime.cache": mime_cache({}, {"app/x": ["app/b", "app/a"]}),
     A + "mimeinfo.cache": cache([("app/b", "b.desktop")])}, ["app/x"])

# --- order of roots
roots2 = {"config_home": "cfg", "config_dirs": ["etc1", "etc2"], "data_home": "home", "data_dirs": ["sys1", "sys2"]}
case("o01-config-dirs-order", {"sys1/applications/a.desktop": app(), "sys1/applications/b.desktop": app(),
     "etc2/mimeapps.list": "[Default Applications]\ntext/plain=b.desktop\n", "etc1/mimeapps.list": "[Default Applications]\ntext/plain=a.desktop\n"},
     TP, roots=roots2)
case("o02-data-dirs-order-masking", {"sys1/applications/a.desktop": app(typ="Link"), "sys2/applications/a.desktop": app(),
     "sys2/applications/b.desktop": app(), "sys2/applications/mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])},
     TP, roots=roots2)
case("o03-data-dirs-additions-order", {"sys1/applications/b.desktop": app(), "sys2/applications/a.desktop": app(),
     "sys2/applications/mimeinfo.cache": cache([("text/plain", "a.desktop")]), "sys1/applications/mimeinfo.cache": cache([("text/plain", "b.desktop")])},
     TP, roots=roots2)

# --- w: killers for the L1 draft-mutant survivors (M04, M08, M24, M28, M33), added before the wave
case("w01-invalid-desktop-token-file-not-read", base | {"cfg/a.b-mimeapps.list": "[Default Applications]\ntext/plain=c.desktop\n",
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, TP, desktop="a.b:GNOME")
case("w02-same-dir-removal-blocks-later-addition", base | {A + "mimeapps.list": "[Removed Associations]\ntext/plain=b.desktop\n",
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
case("w03-cache-mode-ignores-text-aliases", base | {"sys/mime/mime.cache": mime_cache({}, {"app/k": ["text/plain"]}),
     "home/mime/aliases": "text/x-q text/plain\n", A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])},
     ["text/x-q", "app/k"])
case("w04-locale-suffixed-key-is-not-a-type", base | {"cfg/mimeapps.list": "[Default Applications]\ntext/plain[de]=c.desktop\n"},
     ["text/plain[de]"])
case("w05-cache-major-2-falls-to-text", base | {"sys/mime/mime.cache": {"b64": "AAIAAgAAACAAAAAoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="},
     "sys/mime/subclasses": "text/x-c text/plain\n", A + "mimeinfo.cache": cache([("text/plain", "a.desktop")])}, ["text/x-c"])
case("w06-blocklist-applies-only-to-a-started-list", base | {A + "mimeapps.list":
     "[Added Associations]\ntext/plain=c.desktop\n[Removed Associations]\ntext/plain=b.desktop\n",
     A + "mimeinfo.cache": cache([("text/plain", "a.desktop;b.desktop")])}, TP)
# --- w07-w09: added after the w1 fuzz seat's F3 (duplicate alias across dirs) and F1 (id collision in one dir)
dup = {A + "mimeinfo.cache": cache([("app/a", "a.desktop"), ("app/b", "b.desktop"), ("app/c", "c.desktop")])}
case("w07-duplicate-alias-across-dirs", base | dup | {"home/mime/aliases": "app/q app/a\n",
     "sys/mime/aliases": "app/q app/b\n"}, ["app/q"])
case("w08-duplicate-alias-one-file", base | dup | {"sys/mime/aliases": "app/q app/a\napp/q app/b\napp/q app/c\n"},
     ["app/q"])
case("w09-duplicate-alias-many", base | dup | {"home/mime/aliases": "app/r app/c\napp/q app/c\napp/p app/a\n",
     "sys/mime/aliases": "app/q app/a\napp/q app/b\napp/s app/b\napp/r app/a\n"}, ["app/q", "app/r"])
case("w10-same-id-top-level-and-subdir", {A + "vendor-e.desktop": app(typ="Link"), A + "vendor/e.desktop": app(),
     A + "mimeinfo.cache": cache([("text/plain", "vendor-e.desktop")])}, TP)

if __name__ == "__main__":
    json.dump({"schema": "mime-cases-r91-v1", "cases": CASES}, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write("\n")
