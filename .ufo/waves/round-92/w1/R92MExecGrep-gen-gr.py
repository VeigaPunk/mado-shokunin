#!/usr/bin/env python3
import json
R = "{ROOT}"
BASE_ENV = {"HOME": f"{R}/home", "XDG_CONFIG_HOME": f"{R}/cfg", "XDG_CONFIG_DIRS": f"{R}/etc",
            "XDG_DATA_HOME": f"{R}/data", "XDG_DATA_DIRS": f"{R}/share", "PATH": f"{R}/bin:/usr/bin",
            "XDG_CURRENT_DESKTOP": "Hyprland"}
CASES = []
def case(id_, group, files, types, env=None):
    e = dict(BASE_ENV); e.update(env or {})
    CASES.append({"id": id_, "group": group, "files": files, "env": e, "types": types})
def exe(name): return {f"bin/{name}": {"text": "#!/bin/sh\nexit 0\n", "mode": "755"}}
def desk(path, exec_line, mime="", extra=""):
    body = "[Desktop Entry]\nType=Application\nName=x\n"
    if exec_line is not None: body += f"Exec={exec_line}\n"
    if mime: body += f"MimeType={mime}\n"
    return {path: {"text": body + extra}}
def app(id_, prog=None, where="data/applications", mime=""):
    prog = prog or id_.replace(".desktop","").replace("/","_")
    f = desk(f"{where}/{id_}", f"{prog} %U", mime); f.update(exe(prog)); return f
def ma(path, body): return {path: {"text": body}}
def merge(*ds):
    out={}
    for d in ds: out.update(d)
    return out
T="text/plain"; DA="[Default Applications]\n"

# --- BRE family: grep "$MIME=" defaults.list|mimeinfo.cache
case("gr-01-bre-star-stack","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/aaa=z.desktop;\n"), ["text/a**"])
case("gr-02-bre-star-stack-miss","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/bbb=z.desktop;\n"), ["text/a**"])
case("gr-03-bre-brace-star","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/aa=z.desktop;\n"), ["text/a\\{2\\}*"])
case("gr-04-bre-plus-backtrack","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/aaab=z.desktop;\n"), ["text/a\\+\\+ab"])
case("gr-05-bre-brace-at-start","gr", ma("share/applications/defaults.list","[Default Applications]\n{2}x/y=w.desktop;\n"), ["\\{2}x/y"])
case("gr-06-bre-brace-at-start-anchor","gr", ma("share/applications/defaults.list","[Default Applications]\n{2}x/y=w.desktop;\n"), ["^\\{2}x/y"])
case("gr-07-bre-brace-at-start-paren","gr", ma("share/applications/defaults.list","[Default Applications]\n{2}x/y=w.desktop;\n"), ["\\(\\{2}x\\)/y"])
case("gr-08-bre-collating-dot","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/.=w.desktop;\n"), ["text/[[.a.]]"])
case("gr-09-bre-equiv-dot","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/.=w.desktop;\n"), ["text/[[=a=]]"])
case("gr-10-bre-invalid-brace-empty","gr", ma("share/applications/defaults.list","[Default Applications]\ntext/x{}=w.desktop;\n"), ["text/x\\{\\}"])
case("gr-11-bre-invalid-brace-alpha","gr", ma("share/applications/defaults.list","[Default Applications]\ntext/x{a}=w.desktop;\n"), ["text/x\\{a\\}"])
case("gr-12-bre-huge-brace","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/a=z.desktop;\n"), ["text/a\\{999999999999999999999\\}"])
case("gr-13-bre-star-at-type-start","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\n*x/y=z.desktop;\n"), ["*x/y"])
case("gr-14-bre-caret-mid","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\nx^y/z=z.desktop;\n"), ["x^y/z"])
case("gr-15-bre-dollar-mid","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\nx$y/z=z.desktop;\n"), ["x$y/z"])
case("gr-16-bre-bad-backref","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/x=z.desktop;\n"), ["text/\\1x"])
case("gr-17-bre-bracket-class","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/pzain=z.desktop;\n"), ["text/p[abc]ain"])
case("gr-18-bre-dot-not-slash","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/x=y=z.desktop;\n"), ["text/x.y"])
case("gr-19-bre-star-zero","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/lain=z.desktop;\n"), ["text/p*lain"])
case("gr-20-bre-slash-esc","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/x/y=z.desktop;\n"), ["text/x\\/y"])

# --- cut / path / order family
case("gr-21-cut-path-equals","gr", ma("share=/applications/defaults.list","[Default Applications]\ntext/plain=w.desktop;\n"), [T],
     {"XDG_DATA_DIRS": f"{R}/share="})
case("gr-22-cut-value-multi-eq","gr", ma("share/applications/defaults.list","[Default Applications]\ntext/plain=a=b;c.desktop;\n"), [T])
case("gr-23-grep-head-first-file","gr", merge(ma("share/applications/defaults.list","[Default Applications]\nother/type=o.desktop;\ntext/plain=d.desktop;\n"),
     ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/plain=c.desktop;\n")), [T])
case("gr-24-menu-prefix-falls-through","gr", merge(ma("share/applications/defaults.list","[Default Applications]\ntext/plain=u.desktop;\n"),
     ma("share/applications/lxde-defaults.list","[Default Applications]\ntext/plain=m.desktop;\n")), [T],
     {"XDG_MENU_PREFIX": "lxde-"})
case("gr-25-first-dir-wins-switch","gr", merge(ma("share/applications/defaults.list","[Default Applications]\ntext/plain=s.desktop;\n"),
     ma("share2/applications/defaults.list","[Default Applications]\ntext/plain=t.desktop;\n")), [T],
     {"XDG_DATA_DIRS": f"{R}/share:{R}/share2"})

# --- InitialPreference / bash_int family
def pref_case(id_, prefs):
    fs = {}
    for name, pref in prefs:
        extra = ("\n" if pref is not None else "") + (f"InitialPreference={pref}\n" if pref is not None else "")
        fs[f"share/applications/{name}"] = {"text": "[Desktop Entry]\nType=Application\nName=x\nExec=x\nMimeType=text/plain;\n" + extra.lstrip("\n")}
        # careful: build body cleanly below
    # rebuild cleanly
    fs = {}
    for name, pref in prefs:
        body = "[Desktop Entry]\nType=Application\nName=x\nExec=x\nMimeType=text/plain;\n"
        if pref is not None: body += f"InitialPreference={pref}\n"
        fs[f"share/applications/{name}"] = {"text": body}
    case(id_, "gr", fs, [T])
pref_case("gr-26-octal-flip", [("a.desktop","010"),("b.desktop","9")])
pref_case("gr-27-octal-flip-rev", [("a.desktop","9"),("b.desktop","010")])
pref_case("gr-28-octal-8-present", [("a.desktop","08"),("b.desktop","7")])
pref_case("gr-29-pref-leading-space", [("a.desktop"," 5"),("b.desktop","3")])
pref_case("gr-30-pref-trailing-space", [("a.desktop","5 "),("b.desktop","3")])
pref_case("gr-31-pref-plus-sign", [("a.desktop","+5"),("b.desktop","3")])
pref_case("gr-32-pref-two-lines", [("a.desktop","5"),("b.desktop","3")])
# two-lines needs custom body
CASES[-1]["files"]["share/applications/a.desktop"] = {"text": "[Desktop Entry]\nType=Application\nName=x\nExec=x\nMimeType=text/plain;\nInitialPreference=5\nInitialPreference=3\n"}
pref_case("gr-33-pref-x-initial", [("a.desktop","5"),("b.desktop","3")])
CASES[-1]["files"]["share/applications/a.desktop"] = {"text": "[Desktop Entry]\nType=Application\nName=x\nExec=x\nMimeType=text/plain;\nX-InitialPreference=5\n"}
pref_case("gr-34-pref-overflow", [("a.desktop","9223372036854775808"),("b.desktop","3")])
pref_case("gr-35-pref-max-int", [("a.desktop","9223372036854775807"),("b.desktop","3")])
pref_case("gr-36-octal-big", [("a.desktop","0123"),("b.desktop","100")])
pref_case("gr-37-pref-tab", [("a.desktop","\t5"),("b.desktop","3")])
pref_case("gr-38-pref-eq-in-value", [("a.desktop","5"),("b.desktop","3")])
CASES[-1]["files"]["share/applications/a.desktop"] = {"text": "[Desktop Entry]\nType=Application\nName=x\nExec=x\nMimeType=text/plain;\nInitialPreference=5=0\n"}

# --- awk_v family: check_mimeapps_list `awk -v mimetype="$mimetype"`
def awk_case(id_, typ, key):
    case(id_, "gr", merge(ma("cfg/mimeapps.list", DA + f"{key}=a.desktop\n"), app("a.desktop")), [typ])
awk_case("gr-39-awk-unknown-q", "text/x\\qb", "text/xqb")
awk_case("gr-40-awk-unknown-dollar", "text/x\\$y", "text/x$y")
awk_case("gr-41-awk-unknown-e", "text/x\\ey", "text/xey")
awk_case("gr-42-awk-unknown-space", "text/x\\ y", "text/x y")
awk_case("gr-43-awk-unknown-slash", "text/x\\/y", "text/x/y")
awk_case("gr-44-awk-x-nohex", "text/x\\xzy", "text/xxzy")
awk_case("gr-45-awk-octal-4digits", "text/a\\7777b", "text/a\u00ffb")
awk_case("gr-46-awk-known-t", "text/x\\tz", "text/x\tz")
awk_case("gr-47-awk-unknown-z", "text/x\\zy", "text/xzy")
awk_case("gr-48-awk-backslash-real", "text/x\\\\y", "text/x\\y")
# BRE-vs-awk escape parity control through grep leg
case("gr-49-bre-awk-parity","gr", ma("share/applications/mimeinfo.cache","[MIME Cache]\ntext/xqb=w.desktop;\n"), ["text/x\\qb"])

import sys
json.dump({"cases": CASES}, open("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-92/controls/xdgmime-cases-r92-gr-unlabelled.json","w"), indent=1)
print(len(CASES), "cases")
