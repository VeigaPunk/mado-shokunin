#!/usr/bin/env python3
"""Targeted probes for xdg-terminal-exec 0.14.3 selection semantics.

Reuses fuzz.py's sandbox (real script, print modes only, cold cache, restricted
PATH) and runs one minimal case per behaviour. Writes:
  probes/<id>.json   the case in the frozen schema (+ "setup" when needed),
                     including the expect produced by running the real script
  probes.tsv         id, class, rc, stdout, stderr (root replaced by $ROOT)
  cache.tsv          for the cache probes: files left in XDG_CACHE_HOME

Usage: probe.py [--work DIR] [--out DIR]
"""
import argparse
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fuzz  # noqa: E402

A = "home/.local/share/applications/Alacritty.desktop"
T = "usr/share/applications/Alacritty.desktop"
F = "usr/share/applications/Foot.desktop"
L = "home/.config/xdg-terminals.list"


def ent(*lines):
    return fuzz.entry(*lines)


GOOD = ent("Categories=TerminalEmulator;", "Exec=alacritty", "TerminalArgExec=-e")
FOOT = ent("Categories=TerminalEmulator;", "Exec=foot", "TerminalArgExec=-e")


def C(cid, cls, files, execs=("bin/alacritty", "bin/foot"), args=None,
      env=None, setup=None):
    return fuzz.base(cid, cls, files=files, execs=list(execs), args=args,
                     env=env, setup=setup)


def probes():
    p = []

    # --- fallback shadowing -------------------------------------------------
    p.append(C("P01-hidden-shadow", "shadow/hidden-over-system", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty", "Hidden=true"),
        T: ent("Categories=TerminalEmulator;", "Exec=foot")}))
    p.append(C("P01b-invalid-shadow", "shadow/invalid-over-system", {
        A: ent("Categories=TerminalEmulator;", "Exec=ghost"),
        T: ent("Categories=TerminalEmulator;", "Exec=foot")}))
    p.append(C("P01c-system-only", "shadow/control", {
        T: ent("Categories=TerminalEmulator;", "Exec=foot")}))

    # --- key prefix matching ------------------------------------------------
    p.append(C("P02-key-prefix-cat", "entry/key-prefix", {
        A: ent("CategoriesFoo=TerminalEmulator;", "Exec=alacritty")}))
    p.append(C("P02b-key-prefix-exec", "entry/key-prefix", {
        A: ent("Categories=TerminalEmulator;", "ExecFoo=alacritty")}))
    p.append(C("P02c-key-prefix-hidden", "entry/key-prefix", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty",
               "HiddenFoo=true")}))
    p.append(C("P02d-key-prefix-tryexec", "entry/key-prefix", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty",
               "TryExecX=ghost")}))

    # --- section ordering ---------------------------------------------------
    p.append(C("P03-preheader-cat", "entry/pre-header", {
        A: "Categories=TerminalEmulator;\n[Desktop Entry]\nExec=alacritty\n"}))
    p.append(C("P03b-preheader-exec", "entry/pre-header", {
        A: "Exec=ghost\n[Desktop Entry]\nCategories=TerminalEmulator;\n"
           "Exec=alacritty\n"}))
    p.append(C("P03c-header-twice", "entry/pre-header", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty",
               "[Desktop Entry]", "Exec=ghost")}))

    # --- whitespace / control chars ----------------------------------------
    p.append(C("P04-tab-exec", "entry/whitespace", {
        A: ent("Categories=TerminalEmulator;", "Exec=\talacritty")}))
    p.append(C("P04b-space-exec", "entry/whitespace", {
        A: ent("Categories=TerminalEmulator;", "Exec=   alacritty")}))
    p.append(C("P04c-crlf-entry", "entry/whitespace", {
        A: "[Desktop Entry]\r\nCategories=TerminalEmulator;\r\nExec=alacritty\r\n"}))
    p.append(C("P04d-bom-list", "list/whitespace", {
        A: GOOD, F: FOOT, L: "\ufeffFoot.desktop\n"}))
    p.append(C("P04e-crlf-list", "list/whitespace", {
        A: GOOD, F: FOOT, L: "Foot.desktop\r\n"}))
    p.append(C("P04f-comment-list", "list/whitespace", {
        A: GOOD, F: FOOT, L: "# Foot.desktop\n"}))
    p.append(C("P04g-tab-lines-list", "list/whitespace", {
        A: GOOD, F: FOOT, L: "\tFoot.desktop\n\t\n"}))

    # --- exec grammar -------------------------------------------------------
    p.append(C("P05-relative-exec", "exec/relative", {
        A: ent("Categories=TerminalEmulator;", "Exec=./bin/alacritty")}))
    p.append(C("P05b-dollar-exec", "exec/dollar", {
        A: ent("Categories=TerminalEmulator;", "Exec=$HOME/bin/alacritty")}))
    p.append(C("P05c-quote-exec", "exec/quote", {
        A: ent("Categories=TerminalEmulator;", 'Exec="alacritty" --a "b c"')}))
    p.append(C("P05d-unclosed-quote", "exec/quote", {
        A: ent("Categories=TerminalEmulator;", 'Exec=alacritty "open')}))
    p.append(C("P05e-percent-bad", "exec/percent", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty %Z --tail")}))
    p.append(C("P05f-percent-file", "exec/percent", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty %f %u")}))
    p.append(C("P05g-empty-exec", "exec/empty", {
        A: ent("Categories=TerminalEmulator;", "Exec=")}))
    p.append(C("P05h-exec-eq", "exec/value-with-eq", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty --opt=a=b")}))

    # --- caching (contract: print-id/path vs print-cmd) ---------------------
    p.append(C("P06-cache-print-id", "cache/print-id", {A: GOOD},
               args=["--print-id"]))
    p.append(C("P06b-cache-print-cmd", "cache/print-cmd", {A: GOOD},
               args=["--print-cmd"]))

    # --- argument handling --------------------------------------------------
    p.append(C("P07-dir-space-form", "args/space-form", {A: GOOD},
               args=["--print-cmd", "--dir", "/x", "--", "cmd"]))
    p.append(C("P07b-unknown-option", "args/unknown", {A: GOOD},
               args=["--print-id", "-x", "--print-path"]))
    p.append(C("P07c-reversed-order", "args/order", {A: GOOD},
               args=["--print-path", "--print-id"]))
    p.append(C("P07d-duplicate-flags", "args/duplicate", {A: GOOD},
               args=["--print-id", "--print-id", "--print-cmd", "--print-cmd"]))
    p.append(C("P07e-cmd-empty-delim", "args/delimiter", {A: GOOD},
               args=["--print-cmd="]))
    p.append(C("P07f-delim-empty", "args/delimiter", {A: GOOD},
               args=["--print-id", "--print-path", "--print-delimiter="]))
    p.append(C("P07g-verbose-order", "args/prepend-order", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty",
               "TerminalArgExec=-e", "X-TerminalArgAppId=--class=",
               "X-TerminalArgTitle=--title=", "X-TerminalArgDir=--working-directory=",
               "X-TerminalArgHold=--hold")},
        args=["--print-cmd", "--app-id=A", "--title=T", "--dir=D", "--hold",
              "--", "cmd"]))
    p.append(C("P07h-empty-execarg", "args/empty-execarg", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty",
               "TerminalArgExec=")},
        args=["--print-cmd", "--", "cmd"]))
    p.append(C("P07i-no-execarg-strict", "args/strict", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty"),
        L: "/execarg_strict\nAlacritty.desktop\n"}))
    p.append(C("P07j-execarg-default", "args/compat-default", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty"),
        L: "/execarg_default:Alacritty.desktop:--x\nAlacritty.desktop\n"},
        args=["--print-cmd", "--", "cmd"]))

    # --- XDG path list shape ------------------------------------------------
    p.append(C("P08-empty-data-element", "env/empty-element", {A: GOOD},
               args=["--print-id"],
               env={"XDG_DATA_DIRS": "$ROOT/usr/share:"}))
    p.append(C("P08b-empty-config-element", "env/empty-element", {A: GOOD},
               args=["--print-id"],
               env={"XDG_CONFIG_DIRS": ":$ROOT/etc/xdg"}))
    p.append(C("P08c-config-dirs-empty", "env/empty-string", {
        A: GOOD, F: FOOT, "etc/xdg/xdg-terminals.list": "Foot.desktop\n"},
        args=["--print-id"], env={"XDG_CONFIG_DIRS": "$ROOT/etc/xdg"}))
    p.append(C("P08d-config-dirs-empty-string", "env/empty-string", {
        A: GOOD, F: FOOT, "etc/xdg/xdg-terminals.list": "Foot.desktop\n"},
        args=["--print-id"], env={"XDG_CONFIG_DIRS": ""}))
    p.append(C("P08e-data-dirs-empty-string", "env/empty-string", {A: GOOD},
               args=["--print-id"], env={"XDG_DATA_DIRS": ""}))
    p.append(C("P08f-home-unset", "env/home", {A: GOOD}, args=["--print-id"],
               env={"XDG_CONFIG_HOME": None, "XDG_DATA_HOME": None}))

    # --- find filter --------------------------------------------------------
    p.append(C("P09-symlink-into-dir", "find/symlink-dir", {T: FOOT},
               setup={"symlinks": {"home/.local/share":
                                   "../../usr/share"}}))
    p.append(C("P09b-unreadable-second", "find/unreadable", {
        A: GOOD,
        "usr/share/applications/Zed.desktop": ent(
            "Categories=TerminalEmulator;", "Exec=foot")},
        setup={"modes": {"usr/share/applications/Zed.desktop": 0o000}}))
    p.append(C("P09c-dangling", "find/dangling", {A: GOOD},
               setup={"symlinks": {"usr/share/applications/Pff.desktop":
                                   "/nonexistent/Pff.desktop"}}))

    # --- list parse ---------------------------------------------------------
    p.append(C("P10-case-sensitive-id", "list/id-case", {
        A: GOOD, F: FOOT, L: "alacritty.desktop\n"}))
    p.append(C("P10b-dot-id", "list/id-invalid", {
        A: GOOD, F: FOOT, L: ".Alacritty.desktop\n"}))
    p.append(C("P10c-action-space", "list/action", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty",
               "Actions=New;", "[Desktop Action New]", "Exec=alacritty --new"),
        L: "Alacritty.desktop:New action\n"}))
    p.append(C("P10d-action-twice", "list/action", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty",
               "Actions=New;", "[Desktop Action New]",
               "Exec=alacritty --first", "[Desktop Action New]",
               "Exec=alacritty --second"),
        L: "Alacritty.desktop:New\n"}))
    p.append(C("P10e-list-dir", "list/not-a-file", {A: GOOD, L + "/x": ""}))
    p.append(C("P10f-showin-case", "entry/showin-case", {
        F: ent("Categories=TerminalEmulator;", "Exec=foot",
               "OnlyShowIn=hyprland;")}))
    p.append(C("P10g-tryexec-empty", "entry/tryexec-empty", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty", "TryExec=")}))
    p.append(C("P10h-hold-no-arg", "args/hold", {A: GOOD},
               args=["--print-cmd", "--hold", "--", "cmd"]))
    p.append(C("P10i-cat-prefix-word", "entry/categories", {
        A: ent("Categories=TerminalEmulatorX;", "Exec=alacritty")}))
    p.append(C("P10j-cat-lower", "entry/categories", {
        A: ent("Categories=terminalemulator;", "Exec=alacritty")}))

    # --- path list expansion, observed through the script's own debug lines --
    p.append(C("P11-expanded-paths", "env/expansion", {A: GOOD},
               args=["--print-id"],
               env={"XDG_CONFIG_DIRS": ":$ROOT/etc/xdg/",
                    "XDG_DATA_DIRS": "$ROOT/usr/share/:$ROOT/opt//x",
                    "XTE_DEBUG": "1"}))
    p.append(C("P11b-trailing-slash-home", "env/normalisation", {A: GOOD},
               args=["--print-id"],
               env={"XDG_DATA_HOME": "$ROOT/home/.local/share/"}))
    p.append(C("P11c-empty-data-home", "env/empty-string", {A: GOOD},
               args=["--print-id"], env={"XDG_DATA_HOME": ""}))

    # --- unreadable entry that is tried first -------------------------------
    p.append(C("P12-unreadable-first", "find/unreadable", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty"),
        F: FOOT}, setup={"modes": {A: 0o000}}))

    # --- fallback order vs creation order -----------------------------------
    def trio(order, cid):
        files = {}
        bodies = {"Mmm.desktop": "alacritty", "Aaa.desktop": "foot",
                  "Zzz.desktop": "alacritty"}
        for nm in order:
            files["usr/share/applications/" + nm] = ent(
                "Categories=TerminalEmulator;", "Exec=" + bodies[nm])
        return C(cid, "order/readdir", files)
    p.append(trio(["Mmm.desktop", "Aaa.desktop", "Zzz.desktop"], "P13-order-maz"))
    p.append(trio(["Aaa.desktop", "Zzz.desktop", "Mmm.desktop"], "P13b-order-azm"))
    p.append(trio(["Zzz.desktop", "Mmm.desktop", "Aaa.desktop"], "P13c-order-zma"))

    # --- help is a print mode (never launches a terminal) -------------------
    p.append(C("P14-help", "args/help", {A: GOOD}, args=["--help"]))

    # --- empty element in XDG_DATA_DIRS ------------------------------------
    p.append(C("P15-empty-data-element", "env/expansion", {A: GOOD},
               args=["--print-id"],
               env={"XDG_DATA_DIRS": "$ROOT/usr/share:", "XTE_DEBUG": "1"}))
    p.append(C("P15b-dot-segment-path", "find/path-rewrite", {
        F: FOOT}, args=["--print-path"],
        env={"XDG_DATA_DIRS": "$ROOT/usr/./share"}))

    # --- nested dirs, dotfiles in subdirs ----------------------------------
    p.append(C("P16-nested-id", "find/nested-id", {
        "home/.local/share/applications/sub/nested/Foo.desktop": GOOD,
        L: "sub-nested-Foo.desktop\n"}))
    p.append(C("P16b-dotfile-in-subdir", "find/dotfile", {
        "home/.local/share/applications/sub/.hidden.desktop": GOOD}))
    p.append(C("P16c-dotfile-top", "find/dotfile", {
        "home/.local/share/applications/.hidden.desktop": GOOD}))

    # --- unreadable list file aborts the whole resolution ------------------
    p.append(C("P18-unreadable-list", "list/unreadable", {
        A: GOOD, F: FOOT, L: "Foot.desktop\n"},
        setup={"modes": {L: 0o000}}))
    p.append(C("P18b-unreadable-list-lowprio", "list/unreadable", {
        A: GOOD, F: FOOT, L: "Foot.desktop\n",
        "etc/xdg/xdg-terminals.list": "Alacritty.desktop\n"},
        setup={"modes": {"etc/xdg/xdg-terminals.list": 0o000}}))

    # --- a listed ID whose entry fails consumes the fallback registration ---
    p.append(C("P19-action-consumes-fallback", "list/action-unlisted", {
        A: GOOD, L: "Alacritty.desktop:New\n"}))
    p.append(C("P19b-control-unlisted-not-listed", "list/action-unlisted", {
        A: GOOD}))
    # --- empty elements in the middle of a path list -----------------------
    p.append(C("P17-double-colon", "env/expansion", {A: GOOD},
               args=["--print-id"],
               env={"XDG_DATA_DIRS": "$ROOT/usr/share::$ROOT/opt/x",
                    "XTE_DEBUG": "1"}))
    p.append(C("P17b-mid-config-colon", "env/expansion", {A: GOOD},
               args=["--print-id"],
               env={"XDG_CONFIG_DIRS": "$ROOT/etc/xdg::$ROOT/etc/xdg2",
                    "XTE_DEBUG": "1"}))
    # --- duplicate keys, both valid ---------------------------------------
    p.append(C("P20-exec-twice-valid", "entry/duplicate-key", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty",
               "Exec=foot")}))
    p.append(C("P20b-cat-twice-valid", "entry/duplicate-key", {
        A: ent("Categories=TerminalEmulator;", "Categories=TerminalEmulator;",
               "Exec=alacritty")}))
    # --- empty XDG_CONFIG_HOME string -------------------------------------
    p.append(C("P21-config-home-empty-string", "env/empty-string", {
        A: GOOD, F: FOOT, "home/.config/xdg-terminals.list": "Foot.desktop\n"},
        args=["--print-id"], env={"XDG_CONFIG_HOME": ""}))
    # --- empty option values ----------------------------------------------
    p.append(C("P22-empty-option-values", "args/empty-value", {
        A: ent("Categories=TerminalEmulator;", "Exec=alacritty",
               "X-TerminalArgTitle=--title=", "X-TerminalArgDir=--chdir=")},
        args=["--print-cmd", "--title=", "--dir=", "--", "cmd"]))
    return p






def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    work = a.work or os.environ.get("TMPDIR") or tempfile.gettempdir()
    os.makedirs(work, exist_ok=True)
    out = a.out or os.path.join(work, "probes")
    os.makedirs(out, exist_ok=True)
    fuzz.WORK = tempfile.mkdtemp(prefix="pw-", dir=work)
    fuzz.TOOLBIN = fuzz.make_toolbin(fuzz.WORK)

    rows = []
    caches = []
    try:
        for case in probes():
            res = fuzz.run_case(case)
            case = dict(case)
            case["expect"] = {"rc": res["rc"], "stdout": res["stdout"]}
            with open(os.path.join(out, case["id"] + ".json"), "w",
                      encoding="utf-8") as f:
                json.dump(case, f, indent=2, sort_keys=True)
                f.write("\n")
            rows.append((case["id"], case["class"], res["rc"], res["stdout"],
                         res["stderr"]))
            cdir = os.path.join(res["root"], "cache")
            left = sorted(os.listdir(cdir)) if os.path.isdir(cdir) else []
            if case["id"].startswith("P06"):
                caches.append((case["id"], ",".join(left)))
        with open(os.path.join(out, "probes.tsv"), "w", encoding="utf-8") as f:
            f.write("id\tclass\trc\tstdout\tstderr\n")
            for r in rows:
                f.write("%s\t%s\t%d\t%s\t%s\n" % (
                    r[0], r[1], r[2], json.dumps(r[3]),
                    json.dumps(r[4][:300])))
        with open(os.path.join(out, "cache.tsv"), "w", encoding="utf-8") as f:
            f.write("id\tcache_home_entries\n")
            for cid, left in caches:
                f.write("%s\t%s\n" % (cid, left or "<empty>"))
        for r in rows:
            print("%-28s rc=%d out=%s err=%s" % (
                r[0], r[2], json.dumps(r[3]),
                (json.dumps(r[4][:160]) if r[4] else '""')))
        print("\ncache:", caches)
        return 0
    finally:
        import shutil
        for rt in fuzz.ROOTS:
            shutil.rmtree(rt, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
