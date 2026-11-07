#!/usr/bin/env python3
"""Round-92 C1 hand cases (unlabelled) — one or more cases per xdg-mime rule the tool claims to model.

Writes {"cases": [...]} without `expect`; xdgmime-oracle-r92.py labels them with the installed xdg-mime.
Every fixture is written once, in its own case() call (lesson M91-3: no post-hoc rewrite loop).
"""
from __future__ import annotations

import json
import sys

R = "{ROOT}"
BASE_ENV = {"HOME": f"{R}/home", "XDG_CONFIG_HOME": f"{R}/cfg", "XDG_CONFIG_DIRS": f"{R}/etc",
            "XDG_DATA_HOME": f"{R}/data", "XDG_DATA_DIRS": f"{R}/share", "PATH": f"{R}/bin:/usr/bin",
            "XDG_CURRENT_DESKTOP": "Hyprland"}
CASES: list[dict] = []


def exe(name: str) -> dict:
    return {f"bin/{name}": {"text": "#!/bin/sh\nexit 0\n", "mode": "755"}}


def desk(path: str, exec_line: str | None, mime: str = "", extra: str = "") -> dict:
    body = "[Desktop Entry]\nType=Application\nName=x\n"
    if exec_line is not None:
        body += f"Exec={exec_line}\n"
    if mime:
        body += f"MimeType={mime}\n"
    return {path: {"text": body + extra}}


def app(id_: str, prog: str | None = None, where: str = "data/applications", mime: str = "") -> dict:
    """An installed application: desktop file whose Exec's program is an executable in bin/."""
    prog = prog or id_.replace(".desktop", "").replace("/", "_")
    f = desk(f"{where}/{id_}", f"{prog} %U", mime)
    f.update(exe(prog))
    return f


def ma(path: str, body: str) -> dict:
    return {path: {"text": body}}


def case(id_: str, group: str, files: dict, types: list[str], env: dict | None = None, drop: tuple = ()) -> None:
    e = dict(BASE_ENV)
    e.update(env or {})
    for k in drop:
        e.pop(k, None)
    CASES.append({"id": id_, "group": group, "files": files, "env": e, "types": types})


def merge(*ds: dict) -> dict:
    out: dict = {}
    for d in ds:
        out.update(d)
    return out


T = "text/plain"
DA = "[Default Applications]\n"

# ---------------------------------------------------------------- m: mimeapps.list [Default Applications]
case("m01-user-default-installed", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}=a.desktop\n"), app("a.desktop")), [T])
case("m02-user-default-not-installed", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}=a.desktop\n"),
                                                  desk("data/applications/a.desktop", "nosuchprog %U")), [T])
case("m03-list-second-installed", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}=a.desktop;b.desktop;\n"),
                                             desk("data/applications/a.desktop", "nosuchprog"), app("b.desktop")), [T])
case("m04-list-first-wins", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}=a.desktop;b.desktop\n"), app("a.desktop"),
                                       app("b.desktop")), [T])
case("m05-desktop-specific-first", "m", merge(ma("cfg/hyprland-mimeapps.list", DA + f"{T}=h.desktop\n"),
                                              ma("cfg/mimeapps.list", DA + f"{T}=a.desktop\n"), app("a.desktop"),
                                              app("h.desktop")), [T])
case("m06-desktop-lowercased", "m", merge(ma("cfg/hyprland-mimeapps.list", DA + f"{T}=h.desktop\n"), app("h.desktop")),
     [T], {"XDG_CURRENT_DESKTOP": "HyPrLaNd"})
case("m07-desktop-list-order", "m", merge(ma("cfg/b-mimeapps.list", DA + f"{T}=b.desktop\n"),
                                          ma("cfg/a-mimeapps.list", DA + f"{T}=a.desktop\n"), app("a.desktop"),
                                          app("b.desktop")), [T], {"XDG_CURRENT_DESKTOP": "B:A"})
case("m08-empty-desktop", "m", merge(ma("cfg/hyprland-mimeapps.list", DA + f"{T}=h.desktop\n"),
                                     ma("cfg/mimeapps.list", DA + f"{T}=a.desktop\n"), app("a.desktop"),
                                     app("h.desktop")), [T], {"XDG_CURRENT_DESKTOP": ""})
case("m09-first-line-only-in-file", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}=gone.desktop\n{T}=a.desktop\n"),
                                               app("a.desktop"), ma("etc/mimeapps.list", DA + f"{T}=e.desktop\n"),
                                               app("e.desktop")), [T])
case("m10-header-trailing-text", "m", merge(ma("cfg/mimeapps.list", "[Default Applications] # x\n" + f"{T}=a.desktop\n"),
                                            app("a.desktop")), [T])
case("m11-indented-header-no-reset", "m", merge(ma("cfg/mimeapps.list", DA + " [Added Associations]\n" + f"{T}=a.desktop\n"),
                                                app("a.desktop")), [T])
case("m12-leading-space-key", "m", merge(ma("cfg/mimeapps.list", DA + f" {T}=a.desktop\n"), app("a.desktop")), [T])
case("m13-space-before-equals", "m", merge(ma("cfg/mimeapps.list", DA + f"{T} =a.desktop\n"), app("a.desktop")), [T])
case("m14-added-group-ignored", "m", merge(ma("cfg/mimeapps.list", "[Added Associations]\n" + f"{T}=a.desktop\n"),
                                           app("a.desktop")), [T])
case("m15-second-default-section", "m", merge(ma("cfg/mimeapps.list", DA + "image/png=p.desktop\n[Added Associations]\n"
                                                  f"{T}=x.desktop\n" + DA + f"{T}=a.desktop\n"), app("a.desktop"),
                                               app("x.desktop")), [T])
case("m16-crlf-value", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}=a.desktop\r\n"), app("a.desktop")), [T])
case("m17-crlf-list", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}=a.desktop;\r\n"), app("a.desktop")), [T])
case("m18-config-dirs-order", "m", merge(ma("etc/mimeapps.list", DA + f"{T}=e.desktop\n"),
                                         ma("etc2/mimeapps.list", DA + f"{T}=f.desktop\n"), app("e.desktop"),
                                         app("f.desktop")), [T], {"XDG_CONFIG_DIRS": f"{R}/etc2:{R}/etc"})
case("m19-data-dir-mimeapps", "m", merge(ma("share/applications/mimeapps.list", DA + f"{T}=s.desktop\n"),
                                         app("s.desktop")), [T])
case("m20-config-before-data", "m", merge(ma("data/applications/mimeapps.list", DA + f"{T}=d.desktop\n"),
                                          ma("etc/mimeapps.list", DA + f"{T}=e.desktop\n"), app("d.desktop"),
                                          app("e.desktop")), [T])
case("m21-config-home-unset", "m", merge(ma("home/.config/mimeapps.list", DA + f"{T}=h.desktop\n"), app("h.desktop")),
     [T], drop=("XDG_CONFIG_HOME",))
case("m22-config-home-empty", "m", merge(ma("home/.config/mimeapps.list", DA + f"{T}=h.desktop\n"), app("h.desktop")),
     [T], {"XDG_CONFIG_HOME": ""})
case("m23-desktop-specific-data-dir", "m", merge(ma("data/applications/hyprland-mimeapps.list", DA + f"{T}=h.desktop\n"),
                                                 app("h.desktop")), [T])
case("m24-type-prefix-not-key", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}x=a.desktop\n{T}=b.desktop\n"),
                                           app("a.desktop"), app("b.desktop")), [T])
case("m25-list-empty-fields", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}=;;b.desktop\n"), app("b.desktop")), [T])
case("m26-list-space-kept", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}= a.desktop\n"), app("a.desktop")), [T])
case("m27-value-empty", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}=\n"), ma("etc/mimeapps.list", DA + f"{T}=e.desktop\n"),
                                   app("e.desktop")), [T])
case("m28-mimeapps-is-dir", "m", merge({"cfg/mimeapps.list": {"dir": True}}, ma("etc/mimeapps.list", DA + f"{T}=e.desktop\n"),
                                       app("e.desktop")), [T])
case("m29-mimeapps-symlink", "m", merge(ma("other/list", DA + f"{T}=a.desktop\n"),
                                        {"cfg/mimeapps.list": {"symlink": f"{R}/other/list"}}, app("a.desktop")), [T])
case("m30-several-types", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}=a.desktop\nimage/png=p.desktop\n"),
                                     app("a.desktop"), app("p.desktop")), [T, "image/png", "video/mp4"])
case("m31-scheme-handler", "m", merge(ma("cfg/mimeapps.list", DA + "x-scheme-handler/https=w.desktop\n"), app("w.desktop")),
     ["x-scheme-handler/https", "x-scheme-handler/http"])
case("m32-colon-config-home", "m", merge(ma("c2/mimeapps.list", DA + f"{T}=b.desktop\n"), app("b.desktop")), [T],
     {"XDG_CONFIG_HOME": f"{R}/cfg:{R}/c2"})
case("m33-desktop-unknown-x-prefix", "m", merge(ma("cfg/x-hypr-mimeapps.list", DA + f"{T}=h.desktop\n"), app("h.desktop")),
     [T], {"XDG_CURRENT_DESKTOP": "X-Hypr"})
case("m34-group-header-col0-only", "m", merge(ma("cfg/mimeapps.list", "\t[Default Applications]\n" + f"{T}=a.desktop\n"),
                                              app("a.desktop")), [T])
case("m35-no-newline-eof", "m", merge(ma("cfg/mimeapps.list", DA + f"{T}=a.desktop"), app("a.desktop")), [T])

# ---------------------------------------------------------------- d: desktop_file_to_binary
L = "cfg/mimeapps.list"


def pick(id_: str) -> dict:
    return ma(L, DA + f"{T}={id_}\n")


case("d01-vendor-dir", "d", merge(pick("kde-foo.desktop"), app("foo.desktop", "foo", "data/applications/kde")), [T])
case("d02-vendor-two-dashes", "d", merge(pick("a-b-c.desktop"), app("b-c.desktop", "abc", "data/applications/a-b")), [T])
case("d03-vendor-two-dashes-flat", "d", merge(pick("a-b-c.desktop"), app("a-b-c.desktop", "abc")), [T])
case("d04-subdir-search", "d", merge(pick("x.desktop"), app("x.desktop", "x", "data/applications/sub")), [T])
case("d05-subdir-order", "d", merge(pick("x.desktop"), desk("data/applications/aa/x.desktop", "nosuch"),
                                    app("x.desktop", "x", "data/applications/bb")), [T])
case("d06-applnk", "d", merge(pick("x.desktop"), app("x.desktop", "x", "data/applnk")), [T])
case("d07-exec-absolute", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "/usr/bin/env")), [T])
case("d08-exec-absolute-missing", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "/nonexistent/prog")), [T])
case("d09-exec-builtin-true", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "true")), [T])
case("d10-exec-builtin-echo", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "echo hi")), [T])
case("d11-exec-env-wrapper", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "env FOO=1 nosuch")), [T])
case("d12-exec-quoted", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", '"x" %U'), exe("x")), [T])
case("d13-exec-backslash-space", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "my\\ prog %U"),
                                            exe("my prog")), [T])
case("d14-exec-locale-first", "d", merge(pick("x.desktop"), {"data/applications/x.desktop": {
    "text": "[Desktop Entry]\nExec[de]=nosuch\nExec=x\n"}}, exe("x")), [T])
case("d15-exec-action-first", "d", merge(pick("x.desktop"), {"data/applications/x.desktop": {
    "text": "[Desktop Action new]\nExec=x --new\n[Desktop Entry]\nExec=nosuch\n"}}, exe("x")), [T])
case("d16-no-exec", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", None)), [T])
case("d17-exec-relative-cwd", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "./run.sh"),
                                         {"run.sh": {"text": "#!/bin/sh\n", "mode": "755"}}), [T])
case("d18-exec-dash-n", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "-n x"), exe("-n")), [T])
case("d19-path-nonexec-skipped", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "x"),
                                            {"bin/x": {"text": "#!/bin/sh\n", "mode": "644"},
                                             "bin2/x": {"text": "#!/bin/sh\n", "mode": "755"}}), [T],
     {"PATH": f"{R}/bin:{R}/bin2:/usr/bin"})
case("d20-first-dir-bad-exec-stops", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "nosuch"),
                                                app("x.desktop", "x", "share/applications")), [T])
case("d21-applnk-only-dir", "d", merge(pick("x.desktop"), app("x.desktop", "x", "share/applnk")), [T])
case("d22-id-with-slash", "d", merge(pick("sub/x.desktop"), app("x.desktop")), [T])
case("d23-id-leading-dash", "d", merge(pick("-x.desktop"), app("-x.desktop", "dx")), [T])
case("d24-exec-builtin-name-file-in-cwd", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "true"),
                                                     {"true": {"text": ""}}), [T])
case("d25-exec-function-name", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "detectDE"),
                                          exe("detectDE")), [T])
case("d26-exec-keyword", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "time"), exe("time")), [T])
case("d27-exec-leading-ws", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "   x  arg"), exe("x")), [T])
case("d28-exec-continuation", "d", merge(pick("x.desktop"), {"data/applications/x.desktop": {
    "text": "[Desktop Entry]\nExec=ab\\\nExec[de]=cd\n"}}, exe("abcd")), [T])
case("d29-exec-dir-on-path", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "x"),
                                        {"bin/x": {"dir": True}}), [T])
case("d30-desktop-is-dir", "d", merge(pick("x.desktop"), {"data/applications/x.desktop": {"dir": True}},
                                      app("x.desktop", "x", "share/applications")), [T])
case("d31-data-home-unset", "d", merge(pick("x.desktop"), app("x.desktop", "x", "home/.local/share/applications")), [T],
     drop=("XDG_DATA_HOME",))
case("d32-vendor-and-flat", "d", merge(pick("v-x.desktop"), desk("data/applications/v/x.desktop", "nosuch"),
                                       app("v-x.desktop", "vx")), [T])
case("d33-hidden-subdir-skipped", "d", merge(pick("x.desktop"), app("x.desktop", "x", "data/applications/.hid")), [T])
case("d34-exec-symlink-dangling", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "x"),
                                             {"bin/x": {"symlink": f"{R}/nowhere"}}), [T])
case("d35-path-empty-element", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "run.sh"),
                                          {"run.sh": {"text": "#!/bin/sh\n", "mode": "755"}}), [T],
     {"PATH": f"/usr/bin:"})

# ---------------------------------------------------------------- f: defaults.list / mimeinfo.cache (grep)
case("f01-defaults-list", "f", ma("share/applications/defaults.list", DA + f"{T}=dl.desktop;\n"), [T])
case("f02-mimeinfo-cache", "f", ma("share/applications/mimeinfo.cache", "[MIME Cache]\n" + f"{T}=mc.desktop;b.desktop;\n"), [T])
case("f03-defaults-before-cache", "f", merge(ma("share/applications/defaults.list", DA + f"{T}=dl.desktop\n"),
                                             ma("share/applications/mimeinfo.cache", "[MIME Cache]\n" + f"{T}=mc.desktop;\n")), [T])
case("f04-menu-prefix", "f", merge(ma("share/applications/hyprland-defaults.list", DA + f"{T}=hp.desktop\n"),
                                   ma("share/applications/defaults.list", DA + f"{T}=dl.desktop\n")), [T],
     {"XDG_MENU_PREFIX": "hyprland-"})
case("f05-regex-dot", "f", ma("share/applications/mimeinfo.cache", "[MIME Cache]\ntext/xzy=dot.desktop;\n"), ["text/x.y"])
case("f06-unanchored", "f", ma("share/applications/mimeinfo.cache", "[MIME Cache]\nxtext/plain=un.desktop;\n"), [T])
case("f07-removed-group-matches", "f", ma("share/applications/defaults.list", "[Removed Associations]\n" + f"{T}=rm.desktop\n"), [T])
case("f08-empty-value-moves-on", "f", merge(ma("data/applications/mimeinfo.cache", "[MIME Cache]\n" + f"{T}=\n" + f"{T}=no.desktop\n"),
                                            ma("share/applications/mimeinfo.cache", "[MIME Cache]\n" + f"{T}=next.desktop;\n")), [T])
case("f09-echo-dash-n", "f", ma("share/applications/defaults.list", DA + f"{T}=-n;\n"), [T])
case("f10-echo-dash-e", "f", ma("share/applications/defaults.list", DA + f"{T}=-e;\n"), [T])
case("f11-no-semicolon", "f", ma("share/applications/defaults.list", DA + f"{T}=plain.desktop\n"), [T])
case("f12-second-equals", "f", ma("share/applications/defaults.list", DA + f"{T}=a=b.desktop;\n"), [T])
case("f13-path-with-equals", "f", ma("sh=are/applications/defaults.list", DA + f"{T}=eq.desktop;\n"), [T],
     {"XDG_DATA_DIRS": f"{R}/sh=are"})
case("f15-data-home-first", "f", merge(ma("data/applications/mimeinfo.cache", "[MIME Cache]\n" + f"{T}=home.desktop;\n"),
                                       ma("share/applications/defaults.list", DA + f"{T}=sys.desktop\n")), [T])
case("f16-not-installed-ok", "f", merge(ma(L, DA + f"{T}=gone.desktop\n"),
                                        ma("share/applications/mimeinfo.cache", "[MIME Cache]\n" + f"{T}=ghost.desktop;\n")), [T])
case("f18-crlf", "f", ma("share/applications/defaults.list", DA + f"{T}=cr.desktop\r\n"), [T])
case("f19-plus-literal", "f", ma("share/applications/mimeinfo.cache", "[MIME Cache]\napplication/xhtml+xml=xh.desktop;\n"),
     ["application/xhtml+xml"])
case("f20-menu-prefix-cache", "f", ma("share/applications/hyprland-mimeinfo.cache", "[MIME Cache]\n" + f"{T}=hc.desktop;\n"),
     [T], {"XDG_MENU_PREFIX": "hyprland-"})
case("f21-first-match-wins-line", "f", ma("share/applications/mimeinfo.cache", "[MIME Cache]\n" + f"text/plain-x=pre.desktop;\n"
                                          f"{T}=t.desktop;\n"), ["text/plain"])

# ---------------------------------------------------------------- b: defapp_fallback (MimeType scan)
case("b01-mimetype-scan", "b", desk("share/applications/a.desktop", "x", f"{T};"), [T])
case("b02-initial-preference", "b", merge(desk("share/applications/a.desktop", "x", f"{T};"),
                                          desk("share/applications/b.desktop", "x", f"{T};", "InitialPreference=5\n")), [T])
case("b03-tie-first-sorted", "b", merge(desk("share/applications/b.desktop", "x", f"{T};"),
                                        desk("share/applications/a.desktop", "x", f"{T};")), [T])
case("b04-subdir-recursion", "b", desk("share/applications/sub/deep.desktop", "x", f"{T};"), [T])
case("b05-nonnumeric-pref", "b", merge(desk("share/applications/a.desktop", "x", f"{T};", "InitialPreference=abc\n"),
                                       desk("share/applications/b.desktop", "x", f"{T};")), [T])
case("b06-x-initial-preference", "b", merge(desk("share/applications/a.desktop", "x", f"{T};"),
                                            desk("share/applications/b.desktop", "x", f"{T};", "X-InitialPreference=9\n")), [T])
case("b07-two-pref-lines", "b", merge(desk("share/applications/a.desktop", "x", f"{T};"),
                                      desk("share/applications/b.desktop", "x", f"{T};", "InitialPreference=3\nInitialPreference=4\n")), [T])
case("b08-match-anywhere", "b", desk("share/applications/a.desktop", "x", "", f"Comment=opens {T};\n"), [T])
case("b09-hidden-file-ignored", "b", desk("share/applications/.h.desktop", "x", f"{T};"), [T])
case("b10-space-in-name", "b", desk("share/applications/my app.desktop", "x", f"{T};"), [T])
case("b11-cr-pref", "b", merge(desk("share/applications/a.desktop", "x", f"{T};"),
                               {"share/applications/b.desktop": {"text": f"[Desktop Entry]\nMimeType={T};\nInitialPreference=7\r\n"}}), [T])
case("b12-negative-pref", "b", merge(desk("share/applications/a.desktop", "x", f"{T};"),
                                     desk("share/applications/b.desktop", "x", f"{T};", "InitialPreference=-1\n")), [T])
case("b13-data-home-scanned", "b", desk("data/applications/h.desktop", "x", f"{T};"), [T])
case("b14-type-without-semicolon", "b", desk("share/applications/a.desktop", "x", T), [T])
case("b15-higher-pref-later-dir", "b", merge(desk("data/applications/a.desktop", "x", f"{T};", "InitialPreference=1\n"),
                                             desk("share/applications/b.desktop", "x", f"{T};", "InitialPreference=2\n")), [T])
case("b16-no-desktop-files", "b", {"share/applications": {"dir": True}}, [T])

# ---------------------------------------------------------------- s: session / syntax
case("s01-lxqt", "s", merge(pick("a.desktop"), app("a.desktop")), [T], {"XDG_CURRENT_DESKTOP": "LXQt"})
case("s02-kde-no-trader", "s", merge(pick("a.desktop"), app("a.desktop")), [T],
     {"XDG_CURRENT_DESKTOP": "KDE", "KDE_SESSION_VERSION": "5"})
case("s03-lxqt-session-config", "s", merge(pick("a.desktop"), app("a.desktop")), [T],
     {"XDG_CURRENT_DESKTOP": "", "LXQT_SESSION_CONFIG": "x"})
case("s04-flatpak-overrides-lxqt", "s", merge(pick("a.desktop"), app("a.desktop"), {"run/flatpak-info": {"text": ""}}), [T],
     {"XDG_CURRENT_DESKTOP": "LXQt", "XDG_RUNTIME_DIR": f"{R}/run"})
case("s05-no-slash", "s", {}, ["plain"])
case("s06-leading-dash", "s", {}, ["-x/y"])
case("s07-empty-type", "s", {}, [""])
case("s08-version", "s", {}, ["--version"])
case("s09-kde-full-session-lxqt-config", "s", merge(pick("a.desktop"), app("a.desktop")), [T],
     {"XDG_CURRENT_DESKTOP": "", "KDE_FULL_SESSION": "true", "LXQT_SESSION_CONFIG": "x"})
case("s10-gnome-prefix-matches", "s", merge(ma("cfg/gnome-classic:gnome-mimeapps.list", DA + f"{T}=g.desktop\n"),
                                            ma("cfg/gnome-mimeapps.list", DA + f"{T}=h.desktop\n"), app("g.desktop"),
                                            app("h.desktop")), [T], {"XDG_CURRENT_DESKTOP": "GNOME-Classic:GNOME"})

# ---------------------------------------------------------------- g: unquoted words (globbing)
case("g01-desktop-glob", "g", merge(ma("cfg/zeta-mimeapps.list", DA + f"{T}=z.desktop\n"), app("z.desktop"),
                                    {"zeta": {"text": ""}}), [T], {"XDG_CURRENT_DESKTOP": "ze*"})
case("g02-app-glob", "g", merge(ma(L, DA + f"{T}=*.desktop\n"), {"q.desktop": {"text": ""}}, app("q.desktop")), [T])
case("g03-app-glob-nomatch", "g", merge(ma(L, DA + f"{T}=*.nomatch\n"), ma("etc/mimeapps.list", DA + f"{T}=e.desktop\n"),
                                        app("e.desktop")), [T])
case("g04-config-dirs-glob", "g", merge(ma("etc1/mimeapps.list", DA + f"{T}=e.desktop\n"), app("e.desktop")), [T],
     {"XDG_CONFIG_DIRS": f"{R}/etc?"})
case("m36-leading-space-key-equals-app", "m", merge(ma(L, DA + f" {T}=a.desktop\n"), app("=a.desktop", "eqa")), [T])
case("d36-exec-relative-not-executable", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "./plain"),
                                                    {"plain": {"text": "#!/bin/sh\n", "mode": "644"}}), [T])
case("d37-path-only-nonexec", "d", merge(pick("x.desktop"), desk("data/applications/x.desktop", "x"),
                                         {"bin/x": {"text": "#!/bin/sh\n", "mode": "644"}}), [T])
case("d38-first-dir-bad-exec-later-dir-other-name", "d", merge(pick("v-x.desktop"),
                                                               desk("data/applications/v-x.desktop", "nosuch"),
                                                               app("x.desktop", "vx", "share/applications/v")), [T])
case("d39-vendor-applnk", "d", merge(pick("v-x.desktop"), app("x.desktop", "vx", "data/applnk/v")), [T])

# Out of scope since the w1 findings (R92MExecGrep): asked types outside RFC 6838 restricted-name characters
# (f14 `text/[`, f17 `text/p*lain`, g05/g06 backslash escapes) — the tool refuses them (rc 2), so they are not cases.

if __name__ == "__main__":
    out = sys.argv[1]
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"cases": CASES}, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print(f"wrote {len(CASES)} cases")
