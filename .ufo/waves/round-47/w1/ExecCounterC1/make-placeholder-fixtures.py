#!/usr/bin/env python3
"""Build the counter's PLACEHOLDER fixture file: hand-written cases whose `expect` is produced by running the pinned
real script (never typed by hand). This is a self-test instrument for quality/counters/c1-r47-terminal.py, not the
round's fixture set (that one is built by ExecFixtures); it exists so the counter can be scored end to end before the
freeze.

Usage: make-placeholder-fixtures.py --counter <c1-r47-terminal.py> --out <fixtures.json> [--work DIR]
"""
import argparse
import importlib.util
import json
import os
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True


def load_counter(path):
    spec = importlib.util.spec_from_file_location("c1r47", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ALACRITTY_USER = """[Desktop Entry]
Type=Application
Name=Alacritty
GenericName=Terminal
Exec=alacritty --class Alacritty
Icon=Alacritty
Categories=TerminalEmulator;
Keywords=terminal;
"""
ALACRITTY_SYSTEM = ALACRITTY_USER.replace("--class Alacritty", "--class System")
KITTY = """[Desktop Entry]
Type=Application
Name=kitty
Exec=kitty
Categories=TerminalEmulator;
"""
KITTY_HIDDEN = KITTY + "Hidden=true\n"
KITTY_TRYEXEC = KITTY + "TryExec=missingbin\n"
KITTY_UTILITY = KITTY.replace("Categories=TerminalEmulator;", "Categories=Utility;")
KITTY_LINK = KITTY.replace("Type=Application", "Type=Link")
KITTY_ONLYGNOME = KITTY + "OnlyShowIn=GNOME;\n"
KITTY_NOTHYPR = KITTY + "NotShowIn=Hyprland;\n"
ALACRITTY_ACTION = """[Desktop Entry]
Type=Application
Name=Alacritty
Exec=alacritty
Categories=TerminalEmulator;
Actions=new;config;
[Desktop Action new]
Name=New Window
Exec=alacritty --new
[Desktop Action config]
Name=Config
Exec=alacritty --config
"""
ALACRITTY_QUOTED = """[Desktop Entry]
Type=Application
Name=Alacritty
Exec="alacritty" --flag %F
Categories=TerminalEmulator;
"""
ALACRITTY_ARGS = """[Desktop Entry]
Type=Application
Name=Alacritty
Exec=alacritty
Categories=TerminalEmulator;
TerminalArgExec=--
TerminalArgDir=--working-directory=
TerminalArgTitle=--title
TerminalArgAppId=--class
TerminalArgHold=--hold
"""
ENV_BASE = {"XDG_CURRENT_DESKTOP": "Hyprland",
            "XDG_CONFIG_HOME": "$ROOT/home/.config",
            "XDG_CONFIG_DIRS": "$ROOT/etc-xdg",
            "XDG_DATA_HOME": "$ROOT/home/.local/share",
            "XDG_DATA_DIRS": "$ROOT/shareA:$ROOT/shareB"}
LIST_HYPR = "home/.config/hyprland-xdg-terminals.list"

ARG_VARIANTS = [
    ["--print-id"],
    ["--print-path"],
    ["--print-cmd"],
    ["--print-id", "--print-path", "--print-cmd"],
    ["--print-id", "--print-delimiter=|", "--print-path"],
    ["--print-cmd=;", "--print-path"],
    ["--print-cmd=", "--print-id"],
    ["--print-id", "--print-path", "--print-cmd", "--dir=/", "--title=Term", "--app-id=Alacritty", "--hold"],
]

TEMPLATES = [
    ("override", {"files": {LIST_HYPR: "Alacritty.desktop\n",
                            "shareA/applications/Alacritty.desktop": ALACRITTY_SYSTEM,
                            "home/.local/share/applications/Alacritty.desktop": ALACRITTY_USER},
                  "exec": ["bin/alacritty"]}),
    ("hidden", {"files": {LIST_HYPR: "kitty.desktop\nAlacritty.desktop\n",
                          "shareA/applications/kitty.desktop": KITTY_HIDDEN,
                          "shareA/applications/Alacritty.desktop": ALACRITTY_USER},
                "exec": ["bin/alacritty", "bin/kitty"]}),
    ("tryexec", {"files": {LIST_HYPR: "kitty.desktop\nAlacritty.desktop\n",
                           "shareA/applications/kitty.desktop": KITTY_TRYEXEC,
                           "shareA/applications/Alacritty.desktop": ALACRITTY_USER},
                 "exec": ["bin/alacritty", "bin/kitty"]}),
    ("categories", {"files": {LIST_HYPR: "kitty.desktop\nAlacritty.desktop\n",
                              "shareA/applications/kitty.desktop": KITTY_UTILITY,
                              "shareA/applications/Alacritty.desktop": ALACRITTY_USER},
                    "exec": ["bin/alacritty", "bin/kitty"]}),
    ("type", {"files": {LIST_HYPR: "kitty.desktop\nAlacritty.desktop\n",
                        "shareA/applications/kitty.desktop": KITTY_LINK,
                        "shareA/applications/Alacritty.desktop": ALACRITTY_USER},
              "exec": ["bin/alacritty", "bin/kitty"]}),
    ("onlyshowin", {"files": {LIST_HYPR: "kitty.desktop\nAlacritty.desktop\n",
                              "shareA/applications/kitty.desktop": KITTY_ONLYGNOME,
                              "shareA/applications/Alacritty.desktop": ALACRITTY_USER},
                    "exec": ["bin/alacritty", "bin/kitty"]}),
    ("notshowin", {"files": {LIST_HYPR: "kitty.desktop\nAlacritty.desktop\n",
                             "shareA/applications/kitty.desktop": KITTY_NOTHYPR,
                             "shareA/applications/Alacritty.desktop": ALACRITTY_USER},
                   "exec": ["bin/alacritty", "bin/kitty"]}),
    ("action", {"files": {LIST_HYPR: "Alacritty.desktop:new\n",
                          "shareA/applications/Alacritty.desktop": ALACRITTY_ACTION},
                "exec": ["bin/alacritty"]}),
    ("fallback-single", {"files": {"shareA/applications/Alacritty.desktop": ALACRITTY_USER},
                         "exec": ["bin/alacritty"]}),
    ("data-store-list", {"files": {"shareA/xdg-terminal-exec/xdg-terminals.list": "kitty.desktop\nAlacritty.desktop\n",
                                   "shareA/applications/kitty.desktop": KITTY,
                                   "shareA/applications/Alacritty.desktop": ALACRITTY_USER},
                         "exec": ["bin/alacritty", "bin/kitty"]}),
    ("config-dirs", {"env": {"XDG_CONFIG_DIRS": "$ROOT/etc1:$ROOT/etc2"},
                     "files": {"etc1/xdg-terminals.list": "kitty.desktop\n",
                               "etc2/xdg-terminals.list": "Alacritty.desktop\n",
                               "shareA/applications/kitty.desktop": KITTY,
                               "shareA/applications/Alacritty.desktop": ALACRITTY_USER},
                     "exec": ["bin/alacritty", "bin/kitty"]}),
    ("bad-id", {"files": {LIST_HYPR: "bad name.desktop\nAlacritty.desktop\n",
                          "shareA/applications/Alacritty.desktop": ALACRITTY_USER},
                "exec": ["bin/alacritty"]}),
    ("no-terminal", {"files": {LIST_HYPR: "Nothing.desktop\n"},
                     "exec": []}),
    ("quoted-exec", {"files": {LIST_HYPR: "Alacritty.desktop\n",
                               "shareA/applications/Alacritty.desktop": ALACRITTY_QUOTED},
                     "exec": ["bin/alacritty"]}),
    ("entry-args", {"files": {LIST_HYPR: "Alacritty.desktop\n",
                              "shareA/applications/Alacritty.desktop": ALACRITTY_ARGS},
                    "exec": ["bin/alacritty"]}),
    ("plain-config-list", {"files": {"home/.config/xdg-terminals.list": "Alacritty.desktop\n",
                                     "shareA/applications/Alacritty.desktop": ALACRITTY_USER},
                           "exec": ["bin/alacritty"]}),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    c = load_counter(a.counter)
    work = a.work or tempfile.mkdtemp(prefix="c1r47-fx-")
    scratch = tempfile.mkdtemp(dir=work, prefix="fxgen-")
    try:
        script_src, blob = c.load_script()
        sdir = os.path.join(scratch, "script")
        os.makedirs(sdir)
        script = os.path.join(sdir, c.SCRIPT_NAME)
        with open(script, "wb") as f:
            f.write(blob)
        os.chmod(script, 0o755)
        fakebin = c.make_fakebin(os.path.join(scratch, "bin"), os.path.join(scratch, "no.sock"))
        ro_dirs = [sdir, fakebin]
        cases = []
        for tid, tpl in TEMPLATES:
            for k, args in enumerate(ARG_VARIANTS):
                env = dict(ENV_BASE)
                env.update(tpl.get("env") or {})
                files = tpl["files"]
                execs = tpl["exec"]
                root = tempfile.mkdtemp(dir=scratch, prefix="c-")
                c.load_case(root, files, execs)
                renv = c.case_env(env, root, fakebin, False)
                p = c.run_oracle(script, args, root, renv, ro_dirs)
                if p is None:
                    raise SystemExit("oracle timeout on %s-%d" % (tid, k))
                cases.append({
                    "id": "%s-v%d" % (tid, k),
                    "class": tid,
                    "env": env,
                    "files": files,
                    "exec": execs,
                    "args": args,
                    "expect": {"rc": p.returncode, "stdout": c.norm(c.dec(p.stdout), root)},
                })
                shutil.rmtree(root, ignore_errors=True)
        with open(a.out, "w") as f:
            json.dump(cases, f, indent=1)
            f.write("\n")
        print("wrote %d cases to %s" % (len(cases), a.out))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
        if not a.work:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
