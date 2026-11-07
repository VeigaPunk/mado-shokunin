#!/usr/bin/env python3
"""Round-92 C1 fresh-case generator — extended (R92MExecFuzz).

Same generate(seed, n) interface as fuzz-gen-r92.py, plus the rule classes the
frozen generator never produces (see w1/R92MExecFuzz.md §3):
  - symlinks: file symlinks (mimeapps, desktop, dangling) and dir symlinks
  - file types: {"b64"} raw bytes incl. NUL, {"dir": true} entries,
    unreadable modes (000), non-UTF8 bytes via b64
  - env/dispatch: XDG_CURRENT_DESKTOP unset, DESKTOP_SESSION / KDE_FULL_SESSION /
    LXQT_SESSION_CONFIG / XDG_RUNTIME_DIR flatpak-info, KDE qt/dbus fallbacks,
    XDG_CONFIG_HOME/XDG_DATA_HOME unset (config/data fallbacks),
    KDE_SESSION_VERSION unset (ktradertest branch)
  - file content: duplicate Exec lines, Exec with '=' in args, leading spaces,
    trailing \r in mimeapps values, multiple InitialPreference lines, semicolon
    spacing, deeper nesting, hidden files, NUL in mimeapps
  - ask types: BRE metachar types (text/[a-c], text/*, text/plain;x), empty/
    malformed type strings ("" / "text" / "--help" / "text/")
  - PATH: empty entries, "." entries (all still reach /usr/bin)
Scope contract kept identical to the frozen generator: no NUL in text specs
(NUL only via b64), no qtxdg-mat/ktraderclient* executables on PATH (the
candidate's declared refusal scope is only reached by deliberate probes),
PATH always reaches /usr/bin. Duplicates of the frozen generator's vocabulary
are kept so this extension is a superset.
"""
from __future__ import annotations

import base64
import random
import sys

R = "{ROOT}"
TYPES = ["text/plain", "image/png", "text/html", "x-scheme-handler/https", "application/pdf", "text/x.y",
         "application/xhtml+xml", "inode/directory", "video/mp4", "text/plain-x",
         "text/[a-c]", "text/*", "text/plain;x", "", "text", "text/", "--help", "-foo/bar", "text/plain extra"]
IDS = ["a.desktop", "b.desktop", "kde-foo.desktop", "a-b-c.desktop", "org.x.Y.desktop", "sub/z.desktop", "c.desktop",
       "-d.desktop", "v-w.desktop", "e f.desktop"]
DESKTOPS = ["Hyprland", "hyprland", "GNOME", "X-Hypr", "A:B", "", "KDE", "LXQt", "HyPr:x", "sway",
            "GNOME-Flashback", "X-Cinnamon", "ENLIGHTENMENT", "MATE", "XFCE", "LXDE", "KDE:Hyprland"]
DIRS_CFG = ["cfg", "etc", "etc2"]
DIRS_DATA = ["data", "share", "share2"]


def generate(seed: int, n: int) -> list[dict]:
    rnd = random.Random(seed)
    cases = []
    for i in range(n):
        files: dict = {}
        progs = set()

        def exe(name: str, mode: str = "755", d: str = "bin") -> None:
            files[f"{d}/{name}"] = {"text": "#!/bin/sh\nexit 0\n", "mode": mode}

        xcd = rnd.choice(DESKTOPS)
        env = {"HOME": f"{R}/home", "XDG_CONFIG_HOME": f"{R}/cfg", "XDG_CONFIG_DIRS": f"{R}/etc:{R}/etc2",
               "XDG_DATA_HOME": f"{R}/data", "XDG_DATA_DIRS": f"{R}/share:{R}/share2",
               "PATH": rnd.choice([f"{R}/bin:/usr/bin", f"/usr/bin:{R}/bin", f"{R}/bin:{R}/bin2:/usr/bin",
                                   f"{R}/bin::{R}/bin2:/usr/bin", f".:{R}/bin:/usr/bin", f"{R}/bin:/usr/bin:"]),
               "XDG_CURRENT_DESKTOP": xcd}
        if xcd == "":
            if rnd.random() < 0.3:
                env["DESKTOP_SESSION"] = rnd.choice(["gnome", "LXDE", "MATE", "xfce", "xfce4"])
            if rnd.random() < 0.15:
                env["KDE_FULL_SESSION"] = "1"
            if rnd.random() < 0.15:
                env["LXQT_SESSION_CONFIG"] = "1"
        if rnd.random() < 0.3:
            env["XDG_MENU_PREFIX"] = rnd.choice(["hyprland-", "gnome-", "x-"])
        if rnd.random() < 0.12:
            env.pop("XDG_CONFIG_HOME")
        if rnd.random() < 0.12:
            env.pop("XDG_DATA_HOME")
        if xcd == "KDE" and rnd.random() < 0.6:
            if rnd.random() < 0.8:
                env["KDE_SESSION_VERSION"] = rnd.choice(["5", "6", "4"])
        if rnd.random() < 0.08:
            env["XDG_RUNTIME_DIR"] = f"{R}/runtime"
        types = rnd.sample(TYPES, rnd.randint(1, 3))
        # desktop files
        for _ in range(rnd.randint(0, 5)):
            id_ = rnd.choice(IDS)
            layout = rnd.random()
            base = rnd.choice(DIRS_DATA)
            if "/" in id_:
                path = f"{base}/applications/{id_}"
            elif layout < 0.15 and "-" in id_.strip("-"):
                v, rest = id_.split("-", 1)
                path = f"{base}/applications/{v}/{rest}"
            elif layout < 0.25:
                path = f"{base}/applications/nest/{id_}"
            elif layout < 0.3:
                path = f"{base}/applnk/{id_}"
            elif layout < 0.36:
                path = f"{base}/applications/{id_}"
                if rnd.random() < 0.4:
                    files[f"{base}/applications/.hidden/{id_}"] = {"text": "[Desktop Entry]\nType=Application\nExec=nosuch\n"}
                if rnd.random() < 0.3:
                    files[f"{base}/applications/a.deeper/nest/{id_}"] = {"text": "[Desktop Entry]\nType=Application\nExec=nosuch\n"}
            else:
                path = f"{base}/applications/{id_}"
            prog = "p" + str(rnd.randint(0, 3))
            ex = rnd.choice([f"{prog} %U", f"{prog}", "nosuch %f", "true", "echo x", f'"{prog}"', f"  {prog}",
                             "/usr/bin/env", "/nonexistent/x", f"env A=1 {prog}", "time", "-n", f"{prog}\\ x",
                             "detectDE", f"./{prog}", f"{prog}=", f"env A=1 B=x {prog}", f"  {prog}  ", f"{prog}\t%U",
                             f"{prog} %F %f %U %u %i %c %k", "echo", "cd", "if", "p0='x'"])
            body = "[Desktop Entry]\nType=Application\n"
            if rnd.random() < 0.15:
                body = "[Desktop Action a]\nExec=nosuch\n" + body
            if rnd.random() < 0.15:
                body += f"Exec[de]={rnd.choice([prog, 'nosuch'])}\n"
            if rnd.random() < 0.9:
                body += f"Exec={ex}\n"
                if rnd.random() < 0.25:
                    body += f"Exec={rnd.choice(['nosuch', prog])}\n"
            if rnd.random() < 0.6:
                mt = rnd.sample(TYPES, rnd.randint(1, 3))
                body += "MimeType=" + ";".join(mt) + (";" if rnd.random() < 0.8 else "") + "\n"
            if rnd.random() < 0.4:
                body += rnd.choice(["InitialPreference=", "X-InitialPreference="]) + rnd.choice(
                    ["1", "5", "10", "abc", "-1", "", "7\r", "3 ", "0", "+5", "007", "2147483647", "2147483648", "999999999999999999999"]) + "\n"
                if rnd.random() < 0.3:
                    body += rnd.choice(["InitialPreference=", "X-InitialPreference="]) + rnd.choice(["2", "9", "5"]) + "\n"
            if rnd.random() < 0.08:
                body += rnd.choice(["NoDisplay=true\n", "Hidden=true\n", "Terminal=true\n", "OnlyShowIn=GNOME;\n"])
            if rnd.random() < 0.06:
                files[path] = {"b64": base64.b64encode(body.encode() + b"\x00junk").decode()}
            elif rnd.random() < 0.06:
                files[path] = {"text": body, "mode": "000"}
            elif rnd.random() < 0.06:
                files[path] = {"b64": base64.b64encode(b"\xff\xfe" + body.encode()).decode()}
            else:
                files[path] = {"text": body}
            progs.add(prog)
        for p in progs:
            r = rnd.random()
            if r < 0.6:
                exe(p)
            elif r < 0.7:
                exe(p, "644")
            elif r < 0.8:
                exe(p, "755", "bin2")
            elif r < 0.85:
                files[p] = {"text": "#!/bin/sh\n", "mode": "755"}
            elif r < 0.9:
                exe(p, "000")
        if rnd.random() < 0.1:
            exe("p0 x")
        # symlinks to desktop / mimeapps files (frozen generator: none)
        if rnd.random() < 0.15 and any("/applications/" in p for p in files):
            target = rnd.choice([p for p in files if "/applications/" in p])
            link = f"{rnd.choice(DIRS_DATA)}/applications/{rnd.choice(IDS)}"
            files[link] = {"symlink": f"{R}/{target}" if rnd.random() < 0.5 else target}
        if rnd.random() < 0.08:
            d = rnd.choice(DIRS_DATA)
            files[f"{d}/applications/{rnd.choice(IDS)}"] = {"symlink": "nonexistent-target.desktop"}
        if rnd.random() < 0.05:
            # dir entry + file-inside-dir via symlink on the directory itself
            files[f"{rnd.choice(DIRS_DATA)}/applications"] = {"dir": True}
        # mimeapps files
        for _ in range(rnd.randint(0, 4)):
            where = rnd.random()
            if where < 0.6:
                d = rnd.choice(DIRS_CFG)
            else:
                d = rnd.choice(DIRS_DATA) + "/applications"
            pre = ""
            if rnd.random() < 0.35:
                parts = [x for x in xcd.split(":") if x]
                part = rnd.choice(parts) if parts else "hyprland"
                pre = rnd.choice([part.lower(), part, "hyprland"]) + "-"
            lines = []
            for _ in range(rnd.randint(1, 5)):
                k = rnd.random()
                if k < 0.25:
                    lines.append(rnd.choice(["[Default Applications]", "[Added Associations]", "[Removed Associations]",
                                             " [Added Associations]", "[Default Applications] x", " [Default Applications]"]))
                else:
                    t = rnd.choice(types + ["image/png"])
                    vals = rnd.sample(IDS, rnd.randint(1, 3))
                    sep = rnd.choice([";", ";;", " ; ", " ;"])
                    v = sep.join(vals) + rnd.choice(["", ";", "\r", ";\r", " ;", "; "])
                    lines.append(rnd.choice(["", "", "", " ", "  ", "\t"]) + t + rnd.choice(["=", "=", " =", "= ", " = "]) + v)
            if rnd.random() < 0.8:
                lines.insert(0, "[Default Applications]")
            if rnd.random() < 0.08:
                lines.append("\x00" + lines[-1] if lines else "x=\x00")
            fn = f"{d}/{pre}mimeapps.list"
            text = "\n".join(lines) + ("\n" if rnd.random() < 0.9 else "")
            if rnd.random() < 0.07:
                files[fn] = {"b64": base64.b64encode(text.encode("utf-8", "surrogateescape")).decode()}
            elif rnd.random() < 0.06:
                files[fn] = {"text": text, "mode": "000"}
            elif rnd.random() < 0.05:
                files[fn] = {"dir": True}
            else:
                files[fn] = {"text": text}
        # symlink mimeapps.list case
        if rnd.random() < 0.08:
            d = rnd.choice(DIRS_CFG)
            tgt = rnd.choice([p for p in list(files) if "/applications/" in p] or [f"{d}/real.list"])
            if tgt not in files:
                files[tgt] = {"text": "[Default Applications]\ntext/plain=a.desktop;\n"}
            files[f"{d}/mimeapps.list"] = {"symlink": tgt.lstrip("/") if "/" in tgt else tgt}
            files[f"{d}/mimeapps.list"] = {"symlink": f"{R}/{tgt}"}
        # defaults.list / mimeinfo.cache
        for _ in range(rnd.randint(0, 2)):
            d = rnd.choice(DIRS_DATA)
            fn = rnd.choice(["defaults.list", "mimeinfo.cache"])
            pre = env.get("XDG_MENU_PREFIX", "") if rnd.random() < 0.4 else ""
            t = rnd.choice(types)
            key = rnd.choice([t, t.replace(".", "z"), "x" + t, t + "x", t + "*", t.replace("a", ".*")])
            val = rnd.choice(["c.desktop;", "a.desktop;b.desktop;", "", "-n;", "q=r.desktop", "gone.desktop\r", " a.desktop;", "a.desktop ; "])
            head = "[MIME Cache]" if fn == "mimeinfo.cache" else rnd.choice(["[Default Applications]",
                                                                           "[Removed Associations]",
                                                                           "[Added Associations]"])
            files[f"{d}/applications/{pre}{fn}"] = {"text": f"{head}\n{key}={val}\n"}
        if rnd.random() < 0.06:
            files[f"{rnd.choice(DIRS_DATA)}/applications/defaults.list"] = {"symlink": f"{R}/{rnd.choice(DIRS_DATA)}/applications/mimeinfo.cache"}
            files[f"{rnd.choice(DIRS_DATA)}/applications/mimeinfo.cache"] = {"text": "[MIME Cache]\ntext/plain=a.desktop;\n"}
        cases.append({"id": f"fz-{seed:08x}-{i:03d}", "group": "fresh-ext", "files": files, "env": env, "types": types})
    return cases


if __name__ == "__main__":
    import json
    print(json.dumps({"cases": generate(int(sys.argv[1]), int(sys.argv[2]))}, indent=1))
