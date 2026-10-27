#!/usr/bin/env python3
"""make-fixtures.py - emit fixtures-v2.json (fixture schema v2, seat ExecControlsC1, round 48).

`expect` is NOT written here: run-controls.py produces it from the real pinned resolver (3 identical runs) into
receipts/expect.json. What this file states is the *intent* of each case: its env, tree, priming, post-prime
mutations, arguments and the cache verdict it is built to have; the runner refuses a case whose declared verdict the
pin does not confirm (a "hit" must print something a cold run would not, a non-hit must print exactly the cold answer).

schema v2 fields used (round-47 fields + the routed M47-10 extensions):
  id, class, state (cache verdict the fixture is built for), env (with $ROOT), files, exec, args
  mtime    epoch applied to every materialized file and dir (deterministic ls dates)
  prime    {"args": [...]} : a cold pin run before the scored run; the runner waits for the background save
  after    {"files": {path: text|null}, "exec_add": [...], "exec_remove": [...], "env": {...}, "mtime": epoch}
  cache    literal cache text, $ROOT substituted (no priming; for malformed and hand-written caches)
seat sugar (proposed for the frozen schema): an `after.files` value that is a dict {"$cache": OP} rewrites the
primed cache instead of a file, OP in: drop_terminator, bad_hash, set_cmd:NAME, term_midline, pad_before_exec:N.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
APP = "usr/share/applications/"
T0 = 1700000000                     # far from the six-month window on any plausible run date

ENV = {"XDG_CURRENT_DESKTOP": "Hyprland",
       "XDG_CONFIG_HOME": "$ROOT/home/.config",
       "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
       "XDG_DATA_HOME": "$ROOT/home/.local/share",
       "XDG_DATA_DIRS": "$ROOT/usr/share"}


def entry(name, extra=""):
    return ("[Desktop Entry]\nType=Application\nName=%s\nExec=%s\nCategories=System;TerminalEmulator;\n%s"
            % (name, name, extra))


def base_files(list_line="alpha.desktop\n", alpha_extra="", bravo=True):
    files = {APP + "alpha.desktop": entry("alpha", alpha_extra),
             "home/.config/xdg-terminals.list": list_line}
    if bravo:
        files[APP + "bravo.desktop"] = entry("bravo")
    return files


def case(cid, klass, state, files, args, **kw):
    c = {"id": cid, "class": klass, "state": state, "env": dict(ENV), "files": files,
         "exec": kw.pop("exec", ["bin/alpha", "bin/bravo"]), "mtime": T0, "args": args}
    c.update(kw)
    return c


CASES = [
    # ---- cold baseline: the round-47 contract, which a warm-cache tool must not lose
    case("c1-cold-select", "cold", "absent", base_files(),
         ["--print-id", "--print-path", "--print-cmd"]),
    # HOME unset with XDG_CACHE_HOME unset too: the resolver dies in make_paths (D1: pin exit 1, empty stdout)
    case("e1-home-unset", "cold", "absent", base_files(), ["--print-cmd"], unset=["HOME", "XDG_CACHE_HOME"]),
    case("c2-cold-none", "cold", "absent",
         {APP + "alpha.desktop": "[Desktop Entry]\nName=alpha\nExec=alpha\n", "home/.config/xdg-terminals.list": "alpha.desktop\n"},
         ["--print-cmd"], exec=["bin/alpha"]),

    # ---- warm cache changes the answer: a good tool must follow the cache, not the tree
    case("w1-list-edit", "warm-differs", "hit", base_files(), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"files": {"home/.config/xdg-terminals.list": "bravo.desktop\n"}, "mtime": T0}),
    case("w2-entry-exec-edit", "warm-differs", "hit", base_files(), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"files": {APP + "alpha.desktop": entry("alpha").replace("Exec=alpha", "Exec=bravo")}, "mtime": T0}),
    case("w3-args-over-cache", "warm-differs", "hit",
         base_files(alpha_extra="X-TerminalArgTitle=--title\nX-TerminalArgDir=--working-directory=\n"),
         ["--print-cmd", "--dir=/srv", "--title=t2"],
         prime={"args": ["--print-cmd", "--dir=/a", "--title=t1"]},
         after={"files": {APP + "alpha.desktop": entry(
             "alpha", "X-TerminalArgTitle=--titlx\nX-TerminalArgDir=--working-directorx=\n")}, "mtime": T0}),
    case("w4-id-path", "warm-differs", "hit", base_files(), ["--print-id", "--print-path"],
         prime={"args": ["--print-cmd"]},
         after={"files": {"home/.config/xdg-terminals.list": "bravo.desktop\n"}, "mtime": T0}),
    case("w5-content", "warm-differs", "hit", base_files(), ["--print-content"],
         prime={"args": ["--print-cmd"]},
         after={"files": {"home/.config/xdg-terminals.list": "bravo.desktop\n"}, "mtime": T0}),
    case("w6-execarg-edit", "warm-differs", "hit", base_files(alpha_extra="X-TerminalArgExec=-e\n"),
         ["--print-cmd", "--", "htop"],
         prime={"args": ["--print-cmd"]},
         after={"files": {APP + "alpha.desktop": entry("alpha", "X-TerminalArgExec=-x\n")}, "mtime": T0}),
    case("w7-function-cmd", "warm-differs", "hit", base_files(), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"files": {"home/.config/xdg-terminals.list": "bravo.desktop\n",
                          ".rw/cache/xdg-terminal-exec": {"$cache": "set_cmd:read_cache"}}, "mtime": T0}),

    # ---- the cache is invalidated or malformed: the answer is the cold one
    case("i1-size-change", "invalidated", "stale", base_files(), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"files": {"home/.config/xdg-terminals.list": "bravo.desktop\n\n"}, "mtime": T0}),
    case("i2-desktop-change", "invalidated", "stale",
         dict(base_files(), **{"home/.config/gnome-xdg-terminals.list": "bravo.desktop\n"}), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"env": {"XDG_CURRENT_DESKTOP": "GNOME"}}),
    case("i3-exec-gone", "invalidated", "stale", base_files(), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"exec_remove": ["bin/alpha"]}),
    case("i4-no-terminator", "malformed", "invalid", base_files(), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"files": {"home/.config/xdg-terminals.list": "bravo.desktop\n",
                          ".rw/cache/xdg-terminal-exec": {"$cache": "drop_terminator"}}, "mtime": T0}),
    case("i5-line-limit-50", "malformed", "invalid", base_files(), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"files": {"home/.config/xdg-terminals.list": "bravo.desktop\n",
                          ".rw/cache/xdg-terminal-exec": {"$cache": "pad_before_exec:39"}}, "mtime": T0}),
    case("i6-line-limit-49", "malformed", "hit", base_files(), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"files": {"home/.config/xdg-terminals.list": "bravo.desktop\n",
                          ".rw/cache/xdg-terminal-exec": {"$cache": "pad_before_exec:38"}}, "mtime": T0}),
    case("i7-bad-hash", "malformed", "stale", base_files(), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"files": {"home/.config/xdg-terminals.list": "bravo.desktop\n",
                          ".rw/cache/xdg-terminal-exec": {"$cache": "bad_hash"}}, "mtime": T0}),
    case("i8-disabled-env", "invalidated", "disabled", base_files(), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"files": {"home/.config/xdg-terminals.list": "bravo.desktop\n"}, "env": {"XTE_CACHE_ENABLED": "false"},
                "mtime": T0}),
    # a /disable_cache line only suppresses the SAVE; the cache is read before any list (x:1179), so the verdict of
    # this run is the stale read of a list that changed size - the same rule the draft counter derives from stderr.
    case("i9-disable-directive", "invalidated", "stale", base_files(), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"files": {"home/.config/xdg-terminals.list": "/disable_cache\nbravo.desktop\n"}, "mtime": T0}),
    case("i10-term-midline", "malformed", "invalid", base_files(), ["--print-cmd"],
         prime={"args": ["--print-cmd"]},
         after={"files": {"home/.config/xdg-terminals.list": "bravo.desktop\n",
                          ".rw/cache/xdg-terminal-exec": {"$cache": "term_midline"}}, "mtime": T0}),
    case("i11-empty-cache", "malformed", "invalid", base_files(), ["--print-cmd"], cache=""),
    case("i12-cache-dir", "malformed", "absent",
         dict(base_files(), **{".rw/cache/xdg-terminal-exec/": ""}), ["--print-cmd"]),
    # hand-written cache: well formed, wrong hash, cached answer differs from the cold one
    case("i13-literal-stale", "malformed", "stale", base_files(), ["--print-cmd"],
         cache=("0" * 32 + "\nalpha\n$ROOT/usr/share/applications/alpha.desktop\nalpha.desktop\n\n-e\n\n\n\n\n"
                "alpha\x1f\x1eEND_OF_EXEC_USEP\n"),
         after={"files": {"home/.config/xdg-terminals.list": "bravo.desktop\n"}, "mtime": T0}),
]


def main():
    out = os.path.join(HERE, "fixtures-v2.json")
    with open(out, "w") as fh:
        json.dump(CASES, fh, indent=1)
        fh.write("\n")
    print("wrote %s (%d cases)" % (out, len(CASES)))


if __name__ == "__main__":
    main()
