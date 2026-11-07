#!/usr/bin/env python3
"""Round-92 C1 fresh-case generator: generate(seed, n) -> unlabelled cases.

Random compositions over the rule vocabulary of the hand set: mimeapps.list files (user, desktop-specific,
config dirs, data dirs) with headers, indentation, CR, duplicate keys and lists; desktop files in flat,
vendor and nested layouts with Exec forms (installed, missing, builtin, keyword, quoted, escaped, locale,
action-first, wrapper, absolute, relative); defaults.list / mimeinfo.cache with menu prefixes and BRE
metacharacters in the asked type; MimeType scans with InitialPreference values.  No NUL bytes, no
`qtxdg-mat`/`ktraderclient*` executables, PATH always reaches /usr/bin (the tool's declared scope).
The counter seeds it with the measured tool's sha256, so its labels cannot be stored in the tool.
"""
from __future__ import annotations

import random
import sys

R = "{ROOT}"
TYPES = ["text/plain", "image/png", "text/html", "x-scheme-handler/https", "application/pdf", "text/x.y",
         "application/xhtml+xml", "inode/directory", "video/mp4", "text/plain-x"]
IDS = ["a.desktop", "b.desktop", "kde-foo.desktop", "a-b-c.desktop", "org.x.Y.desktop", "sub/z.desktop", "c.desktop",
       "-d.desktop", "v-w.desktop", "e f.desktop"]
DESKTOPS = ["Hyprland", "hyprland", "GNOME", "X-Hypr", "A:B", "", "KDE", "LXQt", "HyPr:x", "sway"]
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
               "PATH": rnd.choice([f"{R}/bin:/usr/bin", f"/usr/bin:{R}/bin", f"{R}/bin:{R}/bin2:/usr/bin"]),
               "XDG_CURRENT_DESKTOP": xcd}
        if rnd.random() < 0.3:
            env["XDG_MENU_PREFIX"] = rnd.choice(["hyprland-", "gnome-", "x-"])
        if rnd.random() < 0.1:
            env.pop("XDG_CONFIG_HOME")
        if rnd.random() < 0.1:
            env.pop("XDG_DATA_HOME")
        if xcd == "KDE" and rnd.random() < 0.5:
            env["KDE_SESSION_VERSION"] = rnd.choice(["5", "6", "4"])
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
            else:
                path = f"{base}/applications/{id_}"
            prog = "p" + str(rnd.randint(0, 3))
            ex = rnd.choice([f"{prog} %U", f"{prog}", "nosuch %f", "true", "echo x", f'"{prog}"', f"  {prog}",
                             "/usr/bin/env", "/nonexistent/x", f"env A=1 {prog}", "time", "-n", f"{prog}\\ x",
                             "detectDE", f"./{prog}"])
            body = "[Desktop Entry]\nType=Application\n"
            if rnd.random() < 0.15:
                body = "[Desktop Action a]\nExec=nosuch\n" + body
            if rnd.random() < 0.15:
                body += f"Exec[de]={rnd.choice([prog, 'nosuch'])}\n"
            if rnd.random() < 0.9:
                body += f"Exec={ex}\n"
            if rnd.random() < 0.6:
                mt = rnd.sample(TYPES, rnd.randint(1, 3))
                body += "MimeType=" + ";".join(mt) + (";" if rnd.random() < 0.8 else "") + "\n"
            if rnd.random() < 0.4:
                body += rnd.choice(["InitialPreference=", "X-InitialPreference="]) + rnd.choice(
                    ["1", "5", "10", "abc", "-1", "", "7\r", "3 "]) + "\n"
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
        if rnd.random() < 0.1:
            exe("p0 x")
        # mimeapps files
        for _ in range(rnd.randint(0, 4)):
            where = rnd.random()
            if where < 0.6:
                d = rnd.choice(DIRS_CFG)
            else:
                d = rnd.choice(DIRS_DATA) + "/applications"
            pre = ""
            if rnd.random() < 0.35:
                part = rnd.choice([x for x in xcd.split(":") if x] or ["hyprland"])
                pre = rnd.choice([part.lower(), part, "hyprland"]) + "-"
            lines = []
            for _ in range(rnd.randint(1, 5)):
                k = rnd.random()
                if k < 0.25:
                    lines.append(rnd.choice(["[Default Applications]", "[Added Associations]", "[Removed Associations]",
                                             " [Added Associations]", "[Default Applications] x"]))
                else:
                    t = rnd.choice(types + ["image/png"])
                    vals = rnd.sample(IDS, rnd.randint(1, 3))
                    sep = rnd.choice([";", ";;"])
                    v = sep.join(vals) + rnd.choice(["", ";", "\r", ";\r"])
                    lines.append(rnd.choice(["", "", "", " "]) + t + rnd.choice(["=", "=", " ="]) + v)
            if rnd.random() < 0.8:
                lines.insert(0, "[Default Applications]")
            files[f"{d}/{pre}mimeapps.list"] = {"text": "\n".join(lines) + ("\n" if rnd.random() < 0.9 else "")}
        # defaults.list / mimeinfo.cache
        for _ in range(rnd.randint(0, 2)):
            d = rnd.choice(DIRS_DATA)
            fn = rnd.choice(["defaults.list", "mimeinfo.cache"])
            pre = env.get("XDG_MENU_PREFIX", "") if rnd.random() < 0.4 else ""
            t = rnd.choice(types)
            key = rnd.choice([t, t.replace(".", "z"), "x" + t, t + "x"])
            val = rnd.choice(["c.desktop;", "a.desktop;b.desktop;", "", "-n;", "q=r.desktop", "gone.desktop\r"])
            head = "[MIME Cache]" if fn == "mimeinfo.cache" else rnd.choice(["[Default Applications]",
                                                                           "[Removed Associations]"])
            files[f"{d}/applications/{pre}{fn}"] = {"text": f"{head}\n{key}={val}\n"}
        cases.append({"id": f"fz-{seed:08x}-{i:03d}", "group": "fresh", "files": files, "env": env, "types": types})
    return cases


if __name__ == "__main__":
    import json
    print(json.dumps({"cases": generate(int(sys.argv[1]), int(sys.argv[2]))}, indent=1))
