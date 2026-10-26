#!/usr/bin/env python3
"""gen-fixtures.py -- round-47 w1 ExecFixtures.

Builds `fixtures.json` for the C1 counter of mado round 47: a list of hermetic
cases over the selection logic of xdg-terminal-exec v0.14.3, where every
`expect` block is produced by RUNNING the real pinned script inside a minimal
sandbox (never typed by hand).

Fixture schema (frozen; one JSON list of objects):

    {"id": str, "class": str,
     "env": {XDG_*: str},          # absent key = variable unset; $ROOT = case root
     "files": {relpath: text},     # written under the case root, mode 0644
     "exec": [relpath],            # written under the case root, mode 0755
     "args": [str],                # argv passed to the script
     "expect": {"rc": int, "stdout": str}}   # case root replaced by $ROOT

`HOME` is always `$ROOT/home`, `PATH` is always `$ROOT/bin:<toolbin>`, and the
resolver cache is always redirected into `$ROOT/.cache` (cold) so no run can
read or write the host's cache.

Sandbox (default `--sandbox bwrap`): bubblewrap with `--unshare-all` (no
network, fresh pid/ipc/uts/user ns), `/usr` read-only, `/etc`, `/usr/share`,
`/usr/local` and `/tmp` masked with empty tmpfs, `env -i` so the fixture `env`
is the entire environment.  The tool bin holds symlinks to exactly the external
commands the script needs (find awk tr md5sum ls mkdir rm); it is deliberately
NOT /usr/bin, because this host ships /usr/bin/alacritty and a wide PATH would
let a host terminal satisfy `command -v` for a fixture that means to fail.

Safety: the script reaches `exec "$@"` (which would launch a terminal) only
when a print mode is absent.  Every case is rejected unless its args contain a
`--print-*` option, and `find_entry` failures exit before that point.

Reproducibility contract for whoever replays these fixtures (the C1 counter):

  * materialise `files` (0644) and `exec` (0755) under a fresh case root and
    substitute `$ROOT` in `env`;
  * HOME=$ROOT/home, PATH=$ROOT/bin:<tool bin>, XDG_CACHE_HOME=<fresh empty
    dir> -- the cache is out of contract, so it must be cold every run;
  * mask /etc, /usr/share and /usr/local (or an empty case root list): the
    `xdg-unset-vs-empty` cases let the script fall back to /etc/xdg and
    /usr/local/share:/usr/share, so an unmasked host could change them;
  * /bin/sh must be bash (as on this host) and <tool bin> must provide find
    awk tr md5sum ls mkdir rm -- nothing else, and no terminal binary;
  * compare exit status + stdout after replacing the case root with $ROOT.

`--verify FILE` replays a JSON file through exactly that contract, using only
the frozen keys, which is also the cheapest way to check a fixture set is
self-sufficient.

Known exclusion: an EMPTY argv element cannot be a fixture.  The option loop
(`/usr/bin/xdg-terminal-exec:1224`) has no `case` branch for "", so `$#` never
decreases and the script spins forever -- `expect {rc, stdout}` cannot express
non-termination.  See receipts/empty-arg-spin.txt.

Usage:
    gen-fixtures.py [--out PATH] [--work DIR] [--script PATH]
                    [--sandbox bwrap|none] [--repeat N] [--summary]
                    [--nonce N]
Exit: 0 ok, 1 build/verification failure, 2 usage.
"""

import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

DEFAULT_SCRIPT = "/usr/bin/xdg-terminal-exec"
PINNED_SHA256 = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
PINNED_URL = "https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec"

# External commands the script shells out to (see make_paths/gen_hash,
# find_entry_paths, save_cache).  Short lists on purpose.
TOOLBIN_TOOLS = ("bash", "find", "awk", "tr", "md5sum", "ls", "mkdir", "rm")

STUB_TEXT = "#!/bin/sh\nexit 0\n"


def _abs(name, *fallbacks):
    for cand in fallbacks + (name,):
        if os.path.isabs(cand) and os.path.isfile(cand) and \
                os.access(cand, os.X_OK):
            return cand
    found = shutil.which(name)
    if not found or not os.path.isabs(found):
        raise SandboxError("cannot resolve an absolute path for %r" % name)
    return found

LIST = "home/.config/xdg-terminals.list"
APP = "home/.local/share/applications/"


def listp(name):
    return "home/.config/" + name


def app(name):
    return APP + name


def dapp(dirname, name):
    return dirname + "/applications/" + name


# --------------------------------------------------------------------------
# environment / desktop-file builders
# --------------------------------------------------------------------------

BASE_ENV = {
    "XDG_CURRENT_DESKTOP": "Hyprland",
    "XDG_CONFIG_HOME": "$ROOT/home/.config",
    "XDG_CONFIG_DIRS": "$ROOT/nonexist",
    "XDG_DATA_HOME": "$ROOT/home/.local/share",
    "XDG_DATA_DIRS": "$ROOT/nodata",
}


def mk_env(omit=(), **over):
    """Base env with per-case overrides; `omit` removes keys (= unset)."""
    env = {k: v for k, v in BASE_ENV.items() if k not in omit}
    env.update(over)
    return env


def desktop(exec_="alacritty", *, type_="Application",
            categories="System;TerminalEmulator;", name="Term",
            tryexec=None, hidden=None, nodisplay=None, onlyshowin=None,
            notshowin=None, actions=None, extra=(), pre=(), omit=(), raw=None):
    """Emit a [Desktop Entry] file.  `raw` bypasses the builder entirely."""
    if raw is not None:
        return raw
    lines = []
    for key, val in (("Type", type_), ("Name", name), ("Exec", exec_),
                     ("TryExec", tryexec), ("Categories", categories),
                     ("Hidden", hidden), ("NoDisplay", nodisplay),
                     ("OnlyShowIn", onlyshowin), ("NotShowIn", notshowin),
                     ("Actions", actions)):
        if key in omit:
            continue
        if val is not None:
            lines.append("%s=%s" % (key, val))
    lines.extend(extra)
    head = list(pre) + ["[Desktop Entry]"]
    return "\n".join(head + lines) + "\n"


def add_action(text, action, exec_):
    return (text + "\n[Desktop Action %s]\nName=%s\nExec=%s\n"
            % (action, action, exec_))


def case(cid, cls, env, files, execs, args, want=None):
    """want: '@reject' (rc!=0, empty stdout), '@select:<needle>', or None."""
    return dict(id=cid, cls=cls, env=env, files=files, exec=execs,
                args=args, want=want)


# --------------------------------------------------------------------------
# curated cases
# --------------------------------------------------------------------------

def curated():
    C = []

    # --- A: list precedence, xdg-terminals.list in the config hierarchy -----
    C += [
        case("a1-cfg-home-plain-list", "list-precedence-config-home",
             mk_env(),
             {"home/.config/xdg-terminals.list": "alacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("a2-cfg-home-beats-cfg-dirs", "list-precedence-config-home",
             mk_env(XDG_CONFIG_DIRS="$ROOT/cd"),
             {"home/.config/xdg-terminals.list": "alacritty.desktop\n",
              "cd/xdg-terminals.list": "foot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("a3-cfg-home-missing-falls-to-cfg-dirs", "list-precedence-config-home",
             mk_env(XDG_CONFIG_DIRS="$ROOT/cd"),
             {"cd/xdg-terminals.list": "foot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("a4-cfg-home-empty-list", "list-precedence-config-home",
             mk_env(),
             {"home/.config/xdg-terminals.list": "",
              app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("a5-cfg-home-list-crlf", "list-precedence-config-home",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "foot.desktop\r\nalacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
    ]

    # --- B: list precedence, <data>/xdg-terminal-exec/*xdg-terminals.list ---
    C += [
        case("b1-data-dir-plain-list", "list-precedence-data-dir",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {"d1/xdg-terminal-exec/xdg-terminals.list": "foot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("b2-data-dir-desktop-list", "list-precedence-data-dir",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {"d1/xdg-terminal-exec/hyprland-xdg-terminals.list":
                  "foot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("b3-data-dir-list-loses-to-cfg-home", "list-precedence-data-dir",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {"home/.config/xdg-terminals.list": "alacritty.desktop\n",
              "d1/xdg-terminal-exec/xdg-terminals.list": "foot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("b4-second-data-dir-list", "list-precedence-data-dir",
             mk_env(XDG_DATA_DIRS="$ROOT/d1:$ROOT/d2"),
             {"d2/xdg-terminal-exec/xdg-terminals.list": "foot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
    ]

    # --- C: desktop-prefixed lists, multi-component XDG_CURRENT_DESKTOP ----
    C += [
        case("c1-multi-component-first-wins", "desktop-prefix-multicomponent",
             mk_env(XDG_CURRENT_DESKTOP="Hyprland:GNOME"),
             {"home/.config/hyprland-xdg-terminals.list": "alacritty.desktop\n",
              "home/.config/gnome-xdg-terminals.list": "foot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("c2-multi-component-order-reversed", "desktop-prefix-multicomponent",
             mk_env(XDG_CURRENT_DESKTOP="GNOME:Hyprland"),
             {"home/.config/hyprland-xdg-terminals.list": "alacritty.desktop\n",
              "home/.config/gnome-xdg-terminals.list": "foot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("c3-desktop-name-case-insensitive", "desktop-prefix-multicomponent",
             mk_env(XDG_CURRENT_DESKTOP="HyPrLaNd"),
             {"home/.config/hyprland-xdg-terminals.list": "alacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("c4-desktop-list-absent-uses-plain", "desktop-prefix-multicomponent",
             mk_env(XDG_CURRENT_DESKTOP="Hyprland:GNOME"),
             {"home/.config/xdg-terminals.list": "foot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("c5-desktop-prefixed-beats-plain", "desktop-prefix-multicomponent",
             mk_env(XDG_CURRENT_DESKTOP="Hyprland"),
             {"home/.config/hyprland-xdg-terminals.list": "alacritty.desktop\n",
              "home/.config/xdg-terminals.list": "foot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
    ]

    # --- D: list syntax noise ---------------------------------------------
    C += [
        case("d1-comments-blank-whitespace", "list-syntax-noise",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "# preferred terminals\n\n   \n\t\n"
                  "   alacritty.desktop\n# trailing comment\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("d2-whitespace-only-list", "list-syntax-noise",
             mk_env(),
             {"home/.config/xdg-terminals.list": "\n   \n# only comments\n\t\n",
              app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("d3-trailing-spaces-on-id", "list-syntax-noise",
             mk_env(),
             {"home/.config/xdg-terminals.list": "alacritty.desktop   \n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("d4-malformed-id-discarded", "list-syntax-noise",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "bad id!.desktop\nfoot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("d5-tab-indented-id", "list-syntax-noise",
             mk_env(),
             {"home/.config/xdg-terminals.list": "\talacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("d6-directive-looking-id", "list-syntax-noise",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "/enable_cache\nalacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
    ]

    # --- E: desktop actions -------------------------------------------------
    a_with_action = add_action(desktop("alacritty", actions="new-window"),
                               "new-window", "alacritty --new-window")
    C += [
        case("e1-action-valid", "actions",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "alacritty.desktop:new-window\n",
              app("alacritty.desktop"): a_with_action},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("e2-action-not-in-actions-key", "actions",
             mk_env(),
             {"home/.config/xdg-terminals.list": "alacritty.desktop:new\n",
              app("alacritty.desktop"):
                  add_action(desktop("alacritty", actions="other"),
                             "new", "alacritty --new")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@reject"),
        case("e3-action-without-actions-key", "actions",
             mk_env(),
             {"home/.config/xdg-terminals.list": "alacritty.desktop:new\n",
              app("alacritty.desktop"):
                  add_action(desktop("alacritty"), "new", "alacritty --new")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@reject"),
        case("e4-action-id-invalid", "actions",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "alacritty.desktop:bad.action\n",
              app("alacritty.desktop"): a_with_action},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"], "@select:alacritty.desktop"),
        case("e5-action-group-unlisted", "actions",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "alacritty.desktop:presented\n",
              app("alacritty.desktop"):
                  add_action(desktop("alacritty", actions="listed"),
                             "presented", "alacritty --presented")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@reject"),
        case("e6-no-retry-after-failed-attempt", "actions",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "alacritty.desktop:new\nalacritty.desktop\n",
              app("alacritty.desktop"):
                  add_action(desktop("alacritty", actions="new"),
                             "new", "nosuchactionbinary")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@reject"),
    ]


    # --- F: exclusion / inclusion syntax -----------------------------------
    # Two candidates in DIFFERENT data dirs: fallback order is then fixed by
    # directory preference, never by readdir order.
    C += [
        case("f1-exclude-fallback", "exclusion-syntax",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {"home/.config/xdg-terminals.list": "-alacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              dapp("d1", "foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("f2-include-then-exclude-keeps", "exclusion-syntax",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {"home/.config/xdg-terminals.list":
                  "+alacritty.desktop\n-alacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              dapp("d1", "foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("f3-exclude-then-include-still-excluded", "exclusion-syntax",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {"home/.config/xdg-terminals.list":
                  "-alacritty.desktop\n+alacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              dapp("d1", "foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("f4-exclusion-does-not-touch-explicit-list", "exclusion-syntax",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {"home/.config/xdg-terminals.list":
                  "-alacritty.desktop\nalacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              dapp("d1", "foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("f6-exclude-id-with-action-suffix", "exclusion-syntax",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {"home/.config/xdg-terminals.list":
                  "-alacritty.desktop:new-window\n",
              app("alacritty.desktop"):
                  add_action(desktop("alacritty", actions="new-window"),
                             "new-window", "alacritty --new-window"),
              dapp("d1", "foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("f7-include-id-with-action-suffix", "exclusion-syntax",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {"home/.config/xdg-terminals.list":
                  "-alacritty.desktop\n+alacritty.desktop:new-window\n",
              app("alacritty.desktop"): desktop("alacritty"),
              dapp("d1", "foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("f5-exclude-nonexistent-id", "exclusion-syntax",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {"home/.config/xdg-terminals.list": "-ghost.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              dapp("d1", "foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
    ]

    # --- G: duplicate IDs across data dirs ---------------------------------
    C += [
        case("g1-duplicate-data-home-wins", "duplicate-ids",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {app("alacritty.desktop"): desktop("alacritty --preferred"),
              dapp("d1", "alacritty.desktop"): desktop("alacritty --distro")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"]),
        case("g2-duplicate-two-data-dirs", "duplicate-ids",
             mk_env(XDG_DATA_DIRS="$ROOT/d1:$ROOT/d2"),
             {dapp("d1", "foot.desktop"): desktop("foot --first"),
              dapp("d2", "foot.desktop"): desktop("foot --second")},
             ["bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"]),
        case("g3-duplicate-three-dirs", "duplicate-ids",
             mk_env(XDG_DATA_DIRS="$ROOT/d1:$ROOT/d2"),
             {app("kitty.desktop"): desktop("kitty --home"),
              dapp("d1", "kitty.desktop"): desktop("kitty --one"),
              dapp("d2", "kitty.desktop"): desktop("kitty --two")},
             ["bin/kitty"],
             ["--print-id", "--print-path", "--print-cmd"]),
    ]

    # --- H: subdirectory entry IDs ----------------------------------------
    C += [
        case("h1-subdir-id-explicit", "subdirectory-ids",
             mk_env(),
             {"home/.config/xdg-terminals.list": "mytools-foot.desktop\n",
              app("mytools/foot.desktop"): desktop("foot"),
              app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:mytools-foot.desktop"),
        case("h2-subdir-two-levels", "subdirectory-ids",
             mk_env(),
             {"home/.config/xdg-terminals.list": "a-b-kitty.desktop\n",
              app("a/b/kitty.desktop"): desktop("kitty"),
              app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty", "bin/kitty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:a-b-kitty.desktop"),
        case("h3-subdir-fallback-scan", "subdirectory-ids",
             mk_env(),
             {app("vendor/foot.desktop"): desktop("foot")},
             ["bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:vendor-foot.desktop"),
    ]

    # --- I: Hidden ---------------------------------------------------------
    C += [
        case("i1-hidden-true-rejected", "hidden",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty", hidden="true"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("i2-hidden-false-accepted", "hidden",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty", hidden="false")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("i3-hidden-uppercase-true-accepted", "hidden",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty", hidden="TRUE")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"], "@select:alacritty.desktop"),
    ]

    # --- J: NoDisplay (not implemented by the script?) ---------------------
    C += [
        case("j1-nodisplay-true-single", "nodisplay",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty", nodisplay="true")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"], "@select:alacritty.desktop"),
        case("j2-nodisplay-true-with-list", "nodisplay",
             mk_env(),
             {"home/.config/xdg-terminals.list": "foot.desktop\n",
              app("foot.desktop"): desktop("foot", nodisplay="true"),
              app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"]),
        case("j3-nodisplay-false-accepted", "nodisplay",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", nodisplay="false")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
    ]

    # --- K: Type -----------------------------------------------------------
    C += [
        case("k1-type-link", "type-key",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty", type_="Link")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"], "@select:alacritty.desktop"),
        case("k2-type-application", "type-key",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("k3-type-absent", "type-key",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty", type_=None)},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"]),
    ]

    # --- L: Categories / TerminalEmulator ---------------------------------
    C += [
        case("l1-no-terminalemulator-rejected", "categories",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty",
                                               categories="System;Utility;"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("l2-terminalemulator-among-many", "categories",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty",
                          categories="System;Utility;TerminalEmulator;X;")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("l3-categories-absent-rejected", "categories",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty", categories=None)},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@reject"),
        case("l4-lowercase-category-rejected", "categories",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", categories="System;terminalemulator;")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@reject"),
        case("l5-no-trailing-semicolon", "categories",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", categories="System;TerminalEmulator")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
    ]

    # --- M: TryExec --------------------------------------------------------
    C += [
        case("m1-tryexec-missing", "tryexec",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", tryexec="nosuchterminal"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("m2-tryexec-present", "tryexec",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", tryexec="alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("m3-tryexec-not-executable", "tryexec",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", tryexec="alacritty"),
              app("foot.desktop"): desktop("foot"),
              "bin/alacritty": "not executable\n"},
             ["bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("m4-tryexec-absolute-exists", "tryexec",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", tryexec="/bin/sh")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("m5-tryexec-absolute-missing", "tryexec",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", tryexec="/nonexistent/tryexec-term"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
    ]

    # --- N: Exec missing / empty ------------------------------------------
    C += [
        case("n1-exec-key-absent", "exec-missing",
             mk_env(),
             {app("alacritty.desktop"): desktop(None),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("n2-exec-empty", "exec-missing",
             mk_env(),
             {app("alacritty.desktop"): desktop(""),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("n3-exec-spaces-only", "exec-missing",
             mk_env(),
             {app("alacritty.desktop"): desktop("   "),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
    ]

    # --- O: OnlyShowIn / NotShowIn ----------------------------------------
    C += [
        case("o1-onlyshowin-mismatch-fallback", "showin-keys",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", onlyshowin="GNOME;"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("o2-onlyshowin-match", "showin-keys",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", onlyshowin="Hyprland;GNOME;")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("o3-notshowin-match-fallback", "showin-keys",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", notshowin="Hyprland;"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("o4-notshowin-mismatch", "showin-keys",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", notshowin="GNOME;KDE;")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("o5-showin-ignored-for-explicit-list", "showin-keys",
             mk_env(),
             {"home/.config/xdg-terminals.list": "alacritty.desktop\n",
              app("alacritty.desktop"):
                  desktop("alacritty", onlyshowin="GNOME;"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
    ]

    # --- P: unset vs empty XDG variables ----------------------------------
    C += [
        case("p1-config-home-unset", "xdg-unset-vs-empty",
             mk_env(omit=("XDG_CONFIG_HOME",)),
             {"home/.config/xdg-terminals.list": "alacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("p2-config-home-empty", "xdg-unset-vs-empty",
             mk_env(XDG_CONFIG_HOME=""),
             {"home/.config/xdg-terminals.list": "alacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("p3-data-home-unset", "xdg-unset-vs-empty",
             mk_env(omit=("XDG_DATA_HOME",)),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("p4-data-dirs-unset", "xdg-unset-vs-empty",
             mk_env(omit=("XDG_DATA_DIRS",)),
             {"home/.config/xdg-terminals.list": "alacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("p5-data-dirs-empty", "xdg-unset-vs-empty",
             mk_env(XDG_DATA_DIRS=""),
             {"home/.config/xdg-terminals.list": "alacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("p6-config-dirs-unset", "xdg-unset-vs-empty",
             mk_env(omit=("XDG_CONFIG_DIRS",)),
             {"home/.config/xdg-terminals.list": "alacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("p7-desktop-unset", "xdg-unset-vs-empty",
             mk_env(omit=("XDG_CURRENT_DESKTOP",)),
             {"home/.config/xdg-terminals.list": "alacritty.desktop\n",
              "home/.config/hyprland-xdg-terminals.list": "foot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("p8-desktop-empty", "xdg-unset-vs-empty",
             mk_env(XDG_CURRENT_DESKTOP=""),
             {"home/.config/hyprland-xdg-terminals.list": "foot.desktop\n",
              "home/.config/xdg-terminals.list": "alacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
    ]

    # --- Q: nothing selectable --------------------------------------------
    C += [
        case("q1-empty-root", "no-valid-entry",
             mk_env(),
             {},
             [],
             ["--print-id", "--print-path", "--print-cmd"],
             "@reject"),
        case("q2-list-names-missing-id", "no-valid-entry",
             mk_env(),
             {"home/.config/xdg-terminals.list": "ghost.desktop\n"},
             [],
             ["--print-id", "--print-path", "--print-cmd"],
             "@reject"),
        case("q3-all-entries-invalid", "no-valid-entry",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", categories="System;"),
              app("foot.desktop"): desktop("nosuchbinary")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@reject"),
        case("q4-print-cmd-empty-root", "no-valid-entry",
             mk_env(),
             {},
             [],
             ["--print-cmd"],
             "@reject"),
    ]

    # --- R: fallback scan order -------------------------------------------
    C += [
        case("r1-fallback-prefers-data-home", "fallback-order",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {app("foot.desktop"): desktop("foot"),
              dapp("d1", "kitty.desktop"): desktop("kitty")},
             ["bin/foot", "bin/kitty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("r2-fallback-prefers-first-data-dir", "fallback-order",
             mk_env(XDG_DATA_DIRS="$ROOT/d1:$ROOT/d2"),
             {dapp("d1", "kitty.desktop"): desktop("kitty"),
              dapp("d2", "foot.desktop"): desktop("foot")},
             ["bin/foot", "bin/kitty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:kitty.desktop"),
        case("r3-list-first-invalid-second-valid", "fallback-order",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "alacritty.desktop\nfoot.desktop\n",
              app("alacritty.desktop"):
                  desktop("alacritty", categories="System;"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        case("r4-nonexistent-id-then-fallback", "fallback-order",
             mk_env(),
             {"home/.config/xdg-terminals.list": "ghost.desktop\n",
              app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
    ]

    # --- S: TerminalArg* keys / exec-arg composition ----------------------
    C += [
        case("s1-terminalarg-exec-e", "terminal-args",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", extra=["X-TerminalArgExec=-e"])},
             ["bin/alacritty"],
             ["--print-cmd", "sh", "-c", "echo hi"],
             "@select:alacritty"),
        case("s2-terminalarg-exec-dashes", "terminal-args",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", extra=["X-TerminalArgExec=--"])},
             ["bin/alacritty"],
             ["--print-cmd", "sh"],
             "@select:alacritty"),
        case("s3-execarg-compat-default", "terminal-args",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", extra=["X-ExecArg=-e"])},
             ["bin/alacritty"],
             ["--print-cmd", "sh"],
             "@select:alacritty"),
        case("s4-execarg-strict-discards-entry", "terminal-args",
             mk_env(),
             {"home/.config/xdg-terminals.list": "/execarg_strict\n",
              app("alacritty.desktop"):
                  desktop("alacritty", extra=["X-ExecArg=-e"])},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@reject"),
        case("s5-execarg-default-directive", "terminal-args",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "/execarg_default:alacritty.desktop:--\n"
                  "alacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-cmd", "sh"],
             "@select:alacritty"),
        case("s6-terminalarg-hold", "terminal-args",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", extra=["X-TerminalArgHold=--hold"])},
             ["bin/alacritty"],
             ["--print-cmd", "--hold", "sh"],
             "@select:alacritty"),
        case("s7-terminalarg-dir-concat", "terminal-args",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty",
                          extra=["X-TerminalArgDir=--working-directory="])},
             ["bin/alacritty"],
             ["--print-cmd", "--dir=/home/someone"],
             "@select:alacritty"),
        case("s8-terminalarg-title-two-args", "terminal-args",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", extra=["X-TerminalArgTitle=--title"])},
             ["bin/alacritty"],
             ["--print-cmd", "--title=My Window"],
             "@select:alacritty"),
        case("s9-terminalarg-appid-concat", "terminal-args",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", extra=["X-TerminalArgAppId=--app-id="])},
             ["bin/alacritty"],
             ["--print-cmd", "--app-id=org.example.Term"],
             "@select:alacritty"),
        case("s10-terminalarg-escape-expansion", "terminal-args",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty",
                          extra=["X-TerminalArgTitle=--ti\\stle"])},
             ["bin/alacritty"],
             ["--print-cmd", "--title=W"],
             "@select:alacritty"),
        case("s11-no-terminalarg-strict-list", "terminal-args",
             mk_env(),
             {"home/.config/xdg-terminals.list": "/execarg_strict\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"):
                  desktop("foot", extra=["TerminalArgExec=-e"])},
             ["bin/alacritty", "bin/foot"],
             ["--print-cmd", "sh"],
             "@select:foot"),
    ]

    # --- T: Exec field codes, quoting, escapes ---------------------------
    C += [
        case("t1-field-f", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty %f")},
             ["bin/alacritty"],
             ["--print-cmd"]),
        case("t2-field-U", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty --open %U")},
             ["bin/alacritty"],
             ["--print-cmd"]),
        case("t3-field-percent-literal", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty --percent=%%")},
             ["bin/alacritty"],
             ["--print-cmd"]),
        case("t4-field-i", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty %i --x")},
             ["bin/alacritty"],
             ["--print-cmd"]),
        # field stripper returns 1 before writing back -> the raw token list
        # survives, so the unknown field is KEPT and the entry is accepted.
        case("t5-field-unknown", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty %z")},
             ["bin/alacritty"],
             ["--print-id", "--print-cmd"],
             "@select:%z"),
        case("t6-exec-quoted-binary-with-space", "exec-fields",
             mk_env(),
             {app("myterm.desktop"):
                  desktop('"my term" --flag', name="MyTerm")},
             ["bin/my term"],
             ["--print-cmd"], "@select:my term"),
        case("t7-exec-quoted-argument", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop('alacritty "arg with spaces"')},
             ["bin/alacritty"],
             ["--print-cmd"]),
        # tokenizer error is ignored too: the argv built so far is used.
        case("t8-exec-unquoted-dollar", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty $HOME")},
             ["bin/alacritty"],
             ["--print-cmd"],
             "@select:alacritty"),
        case("t9-exec-trailing-spaces", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty --x   ")},
             ["bin/alacritty"],
             ["--print-cmd"]),
        case("t10-exec-tab-separator", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty\t--x")},
             ["bin/alacritty"],
             ["--print-cmd"]),
        case("t11-exec-escaped-quote", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop('alacritty "a\\"b"')},
             ["bin/alacritty"],
             ["--print-cmd"], "@select:ab"),
        case("t12-exec-unclosed-quote", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"): desktop('alacritty "unclosed')},
             ["bin/alacritty"],
             ["--print-cmd"],
             "@select:unclosed"),
        case("t13-two-file-fields", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty %f %F")},
             ["bin/alacritty"],
             ["--print-cmd"],
             "@select:%f"),
        case("t14-unquoted-semicolon", "exec-fields",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty x;y")},
             ["bin/alacritty"],
             ["--print-cmd"],
             "@select:alacritty"),
    ]

    # --- U: print modes and delimiters -----------------------------------
    C += [
        case("u1-print-cmd-only", "print-modes",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-cmd"],
             "@select:alacritty"),
        case("u2-print-cmd-comma", "print-modes",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty --x")},
             ["bin/alacritty"],
             ["--print-cmd=,"],
             "@select:alacritty,--x"),
        case("u3-print-delimiter-pipe", "print-modes",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-delimiter=|"]),
        case("u4-print-order-normalised", "print-modes",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-cmd", "--print-id"],
             "@select:alacritty.desktop"),
        case("u5-print-content", "print-modes",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-content"],
             "@select:[Desktop Entry]"),
        case("u6-print-content-and-cmd", "print-modes",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-content", "--print-cmd"]),
        case("u7-duplicate-print-option", "print-modes",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-id"]),
        case("u8-print-id-path-cmd-order", "print-modes",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
    ]

    # --- V: --dir / --title / --app-id / --hold --------------------------
    C += [
        case("v1-dir-two-args", "option-prepend",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", extra=["X-TerminalArgDir=--dir"])},
             ["bin/alacritty"],
             ["--print-cmd", "--dir=/work"]),
        case("v2-dir-without-entry-key", "option-prepend",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-cmd", "--dir=/work"]),
        case("v3-title-and-appid-and-hold", "option-prepend",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty",
                          extra=["X-TerminalArgTitle=--title",
                                 "X-TerminalArgAppId=--app-id=",
                                 "X-TerminalArgHold=--hold"])},
             ["bin/alacritty"],
             ["--print-cmd", "--title=T", "--app-id=A", "--hold"]),
        case("v4-hold-with-command", "option-prepend",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", extra=["X-TerminalArgHold=--hold"])},
             ["bin/alacritty"],
             ["--print-cmd", "--hold", "sh", "-c", "sleep 1"]),
        case("v5-hold-without-entry-key", "option-prepend",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-cmd", "--hold", "sh"]),
        case("v6-all-options-order", "option-prepend",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty",
                          extra=["X-TerminalArgDir=--dir=",
                                 "X-TerminalArgTitle=--title",
                                 "X-TerminalArgAppId=--app-id",
                                 "X-TerminalArgHold=--hold",
                                 "X-TerminalArgExec=--exec"])},
             ["bin/alacritty"],
             ["--print-cmd", "--hold", "--app-id=A", "--title=T",
              "--dir=/w", "sh"]),
    ]

    # --- W: command args, spaces, quotes, -e -----------------------------
    C += [
        case("w1-double-dash-then-args", "command-args",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", extra=["X-TerminalArgExec=-e"])},
             ["bin/alacritty"],
             ["--print-cmd", "--", "-e", "sh"]),
        case("w2-arg-with-space", "command-args",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-cmd", "echo a b"]),
        case("w3-arg-with-quote", "command-args",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-cmd", 'say "hi"']),
        case("w4-positional-e", "command-args",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", extra=["X-TerminalArgExec=-e"])},
             ["bin/alacritty"],
             ["--print-cmd", "-e", "sh", "-c", "echo hi"]),
        case("w5-unknown-option-discarded", "command-args",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-cmd", "--bogus", "sh"]),
        # NOTE: an empty argv element cannot be a fixture -- the option loop in
        # v0.14.3 matches no `case` branch for "" and spins forever.  Recorded
        # in the receipts (`empty-arg-spin.txt`), not in the fixture set.
        case("w6-many-command-args", "command-args",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-cmd"] + ["a%d" % i for i in range(10)]),
        case("w7-command-with-newline-arg", "command-args",
             mk_env(),
             {app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-cmd", "line1\nline2"]),
    ]

    # --- X: localized keys ------------------------------------------------
    C += [
        case("x1-localized-after-plain", "localized-keys",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty",
                          extra=["Name[de]=Terminal", "Comment[de]=Text"])},
             ["bin/alacritty"],
             ["--print-cmd"],
             "@select:alacritty"),
        case("x2-localized-before-plain", "localized-keys",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty",
                          pre=["Name[de]=Terminal", "GenericName[fr]=Term"])},
             ["bin/alacritty"],
             ["--print-cmd"],
             "@select:alacritty"),
        case("x3-only-localized-name", "localized-keys",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty", name=None,
                          extra=["Name[de]=Nur Deutsch",
                                 "Keywords[de]=terminal;fenster;"])},
             ["bin/alacritty"],
             ["--print-cmd"],
             "@select:alacritty"),
        case("x4-localized-with-brackets-in-value", "localized-keys",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty",
                          extra=["Name[x-test]=a [b] c"])},
             ["bin/alacritty"],
             ["--print-cmd"],
             "@select:alacritty"),
    ]

    # --- Y: CRLF ----------------------------------------------------------
    crlf_entry = "\r\n".join(desktop("alacritty").rstrip("\n").split("\n")) + "\r\n"
    C += [
        case("y1-whole-file-crlf", "crlf",
             mk_env(),
             {app("alacritty.desktop"): crlf_entry},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"], "@select:alacritty.desktop"),
        case("y2-crlf-on-some-lines", "crlf",
             mk_env(),
             {app("alacritty.desktop"):
                  "[Desktop Entry]\r\nType=Application\r\nName=T\r\n"
                  "Exec=alacritty\r\nCategories=System;TerminalEmulator;\r\n"},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"], "@select:alacritty.desktop"),
        case("y3-crlf-in-list", "crlf",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "alacritty.desktop\r\nfoot.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:foot.desktop"),
        # CR is [[:space:]] for the Exec tokenizer but not for command -v:
        case("y4-crlf-tryexec-rejected", "crlf",
             mk_env(),
             {app("alacritty.desktop"):
                  "[Desktop Entry]\r\nType=Application\r\nName=T\r\n"
                  "Exec=alacritty\r\nTryExec=alacritty\r\n"
                  "Categories=System;TerminalEmulator;\r\n"},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@reject"),
        case("y5-crlf-hidden-true-accepted", "crlf",
             mk_env(),
             {app("alacritty.desktop"):
                  "[Desktop Entry]\r\nType=Application\r\nName=T\r\n"
                  "Exec=alacritty\r\nHidden=true\r\n"
                  "Categories=System;TerminalEmulator;\r\n"},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
    ]

    # --- Z: BOM -----------------------------------------------------------
    C += [
        case("z1-bom-before-group-header", "bom",
             mk_env(),
             {app("alacritty.desktop"): "\ufeff" + desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"]),
        case("z2-bom-in-list", "bom",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "\ufefffoot.desktop\nalacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/alacritty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("z3-bom-before-key", "bom",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty").replace("Name=Term",
                                               "\ufeffName=Term")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"], "@select:alacritty.desktop"),
    ]

    # --- AA: very long lines ---------------------------------------------
    longarg = "x" * 4000
    C += [
        case("aa1-long-exec-argument", "long-lines",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty --blob=" + longarg)},
             ["bin/alacritty"],
             ["--print-cmd"]),
        case("aa2-long-comment-in-list", "long-lines",
             mk_env(),
             {"home/.config/xdg-terminals.list":
                  "# " + ("y" * 10000) + "\nalacritty.desktop\n",
              app("alacritty.desktop"): desktop("alacritty")},
             ["bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("aa3-long-name-and-exec", "long-lines",
             mk_env(),
             {app("alacritty.desktop"):
                  desktop("alacritty --z=" + ("z" * 2000),
                          name="N" * 2000)},
             ["bin/alacritty"],
             ["--print-cmd"]),
    ]

    # --- BB: odd path shapes ---------------------------------------------
    C += [
        case("bb1-directory-named-desktop", "odd-paths",
             mk_env(),
             {app("weird.desktop/"): "",
              app("foot.desktop"): desktop("foot")},
             ["bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"], "@select:foot.desktop"),
        case("bb2-id-with-dots", "odd-paths",
             mk_env(),
             {app("org.example.foot.desktop"): desktop("foot")},
             ["bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"]),
        # validate_entry_id requires a lowercase ".desktop" suffix, so the
        # list line is discarded and the preferred fallback entry wins.
        case("bb3-uppercase-id", "odd-paths",
             mk_env(XDG_DATA_DIRS="$ROOT/d1"),
             {"home/.config/xdg-terminals.list": "Foot.Desktop\n",
              dapp("d1", "Foot.Desktop"): desktop("foot"),
              app("alacritty.desktop"): desktop("alacritty")},
             ["bin/foot", "bin/alacritty"],
             ["--print-id", "--print-path", "--print-cmd"],
             "@select:alacritty.desktop"),
        case("bb4-dotfile-in-applications", "odd-paths",
             mk_env(),
             {app(".hidden.desktop"): desktop("kitty"),
              app("foot.desktop"): desktop("foot")},
             ["bin/kitty", "bin/foot"],
             ["--print-id", "--print-path", "--print-cmd"]),
    ]

    return C


# --------------------------------------------------------------------------
# nonce (random) case grammar
# --------------------------------------------------------------------------

NONCE_COUNT = 150


def nonce_cases(n):
    """150 cases from the same grammar, deterministic per n.

    Every candidate entry lives in its OWN data dir (XDG_DATA_HOME, then the
    first and second XDG_DATA_DIRS component) so that fallback preference is
    decided by directory order, never by readdir order.
    """
    rng = random.Random(0x4700 + n)
    out = []
    desktops = ["Hyprland", "GNOME", "Hyprland:GNOME", "GNOME:Hyprland",
                "sway", "KDE", "", None, "Hyprland:KDE:GNOME"]
    list_kinds = ["none", "plain", "desktop", "datadir", "datadir-desktop",
                  "cfgdirs"]
    validities = ["ok", "no-cat", "hidden", "nodisplay", "type-link",
                  "tryexec-bad", "exec-missing", "onlyshowin-other",
                  "notshowin-here", "wrong-exec"]
    print_sets = [["--print-id"], ["--print-path"], ["--print-cmd"],
                  ["--print-id", "--print-path"],
                  ["--print-id", "--print-path", "--print-cmd"],
                  ["--print-content"], ["--print-cmd=,"],
                  ["--print-id", "--print-delimiter=:"]]
    cmds = [[], ["sh"], ["sh", "-c", "echo hi"], ["--hold", "sh"],
            ["--dir=/w", "sh"], ["--title=T", "--app-id=A"],
            ["line with space"], ["-e", "sh"]]
    names = ["alacritty", "foot", "kitty", "wezterm", "st", "myterm"]

    # dir index -> root-relative applications dir
    slots = [APP, "d1/applications/", "d2/applications/"]

    for i in range(NONCE_COUNT):
        cid = "nonce%d-%03d" % (n, i + 1)
        desk = rng.choice(desktops)
        kind = rng.choice(list_kinds)
        picks = rng.sample(names, rng.choice([1, 1, 2, 3]))

        env = dict(BASE_ENV)
        env["XDG_DATA_DIRS"] = "$ROOT/d1:$ROOT/d2"
        if desk is None:
            del env["XDG_CURRENT_DESKTOP"]
        else:
            env["XDG_CURRENT_DESKTOP"] = desk

        files = {}
        execs = []
        for idx, nm in enumerate(picks):
            v = rng.choice(validities) if idx == 0 else \
                rng.choice(["ok", "ok", "hidden"])
            kw = {}
            if v == "no-cat":
                kw["categories"] = "System;Utility;"
            elif v == "hidden":
                kw["hidden"] = "true"
            elif v == "nodisplay":
                kw["nodisplay"] = "true"
            elif v == "type-link":
                kw["type_"] = "Link"
            elif v == "tryexec-bad":
                kw["tryexec"] = "nosuch-" + nm
            elif v == "exec-missing":
                kw["omit"] = ("Exec",)
            elif v == "onlyshowin-other":
                kw["onlyshowin"] = "GNOME;"
            elif v == "notshowin-here":
                kw["notshowin"] = "Hyprland;"
            elif v == "wrong-exec":
                pass  # handled below: the Exec word is not on PATH
            extra = []
            if rng.random() < 0.35:
                extra.append("X-TerminalArgExec=-e")
            if rng.random() < 0.20:
                extra.append("X-TerminalArgDir=--dir=")
            if extra:
                kw["extra"] = extra
            exec_line = "ghostbinary" if v == "wrong-exec" \
                else nm + " --flag"
            files[slots[idx] + nm + ".desktop"] = desktop(exec_line, **kw)
            execs.append("bin/" + nm)

        # list file, if any
        entries = []
        if kind != "none":
            listed = rng.sample(picks, len(picks))
            for nm in listed:
                marker = ""
                r = rng.random()
                if r < 0.12:
                    marker = "-"
                elif r < 0.20:
                    marker = "+"
                suffix = ":act" if rng.random() < 0.15 else ""
                entries.append("%s%s.desktop%s" % (marker, nm, suffix))
            if rng.random() < 0.30:
                entries.insert(0, "# comment")
            if rng.random() < 0.20:
                entries.append("")
            body = "\n".join(entries) + "\n"
            if kind == "plain":
                files[listp("xdg-terminals.list")] = body
            elif kind == "cfgdirs":
                env["XDG_CONFIG_DIRS"] = "$ROOT/cd"
                files["cd/xdg-terminals.list"] = body
            elif kind in ("desktop", "datadir-desktop"):
                base = (desk or "hyprland").split(":")[0].lower()
                name = base + "-xdg-terminals.list"
                if kind == "desktop":
                    files[listp(name)] = body
                else:
                    files["d1/xdg-terminal-exec/" + name] = body
            elif kind == "datadir":
                files["d1/xdg-terminal-exec/xdg-terminals.list"] = body

        # give every ":act" request a real action group on its entry
        for line in entries:
            if not line.endswith(":act"):
                continue
            nm = line.lstrip("+-").split(":")[0][:-len(".desktop")]
            for slot in slots:
                key = slot + nm + ".desktop"
                if key in files:
                    files[key] = add_action(files[key], "act", nm + " --act")

        args = list(rng.choice(print_sets))
        r = rng.random()
        if r < 0.40:
            args += rng.choice(cmds)
        elif r < 0.55:
            args.append("--hold")
        if any(a.startswith("--print-cmd") for a in args) and rng.random() < 0.25:
            args = ["--print-cmd=\\n" if a == "--print-cmd" else a
                    for a in args]

        out.append(case(cid, "nonce", env, files, sorted(set(execs)), args))
    return out


# --------------------------------------------------------------------------
# sandbox
# --------------------------------------------------------------------------

class SandboxError(Exception):
    pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_tool(name):
    for d in ("/usr/bin", "/bin", "/usr/local/bin"):
        cand = os.path.join(d, name)
        if os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand
    raise SandboxError("required tool not found on host: %s" % name)


class Sandbox:
    def __init__(self, work, script, mode="bwrap", timeout=20):
        self.work = work
        self.script = script
        self.mode = mode
        self.timeout = timeout
        self.toolbin = os.path.join(work, "toolbin")
        self.roots = os.path.join(work, "roots")
        os.makedirs(self.toolbin, exist_ok=True)
        os.makedirs(self.roots, exist_ok=True)
        for tool in TOOLBIN_TOOLS:
            link = os.path.join(self.toolbin, tool)
            if os.path.islink(link) or os.path.exists(link):
                continue
            os.symlink(resolve_tool(tool), link)

    # -- materialisation ---------------------------------------------------
    def materialize(self, spec, root):
        shutil.rmtree(root, ignore_errors=True)
        os.makedirs(os.path.join(root, "bin"), exist_ok=True)
        os.makedirs(os.path.join(root, "home"), exist_ok=True)
        for rel, text in sorted(spec["files"].items()):
            path = os.path.join(root, rel)
            if rel.endswith("/"):
                os.makedirs(path, exist_ok=True)
                continue
            os.makedirs(os.path.dirname(path) or root, exist_ok=True)
            data = text.encode("utf-8", "surrogateescape")
            with open(path, "wb") as fh:
                fh.write(data)
            os.chmod(path, 0o644)
        for rel in spec["exec"]:
            path = os.path.join(root, rel)
            os.makedirs(os.path.dirname(path) or root, exist_ok=True)
            with open(path, "wb") as fh:
                fh.write(STUB_TEXT.encode())
            os.chmod(path, 0o755)

    @staticmethod
    def args_are_safe(args):
        """True only if a mode that exits before `exec "$@"` is present.

        `--print-*` exits in the print block; `--test` prints the argv and
        exits at /usr/bin/xdg-terminal-exec:1460, also before exec.
        """
        return any(a == "--test" or a == "--print-cmd"
                   or a.startswith("--print-") for a in args)

    def env_for(self, spec, root):
        env = {"HOME": root + "/home",
               "PATH": root + "/bin:" + self.toolbin}
        for key, val in spec["env"].items():
            env[key] = val.replace("$ROOT", root)
        # Cold cache, always redirected inside the case root.
        env["XDG_CACHE_HOME"] = root + "/.cache"
        return env

    def prepare(self, spec):
        """Materialise a fresh case root and return (root, argv)."""
        if not self.args_are_safe(spec["args"]):
            raise SandboxError(
                "refusing to run %s: args lack a --print-* option, the script "
                "would exec a terminal" % spec["id"])
        root = os.path.join(self.roots, spec["id"])
        # fresh root per run: models a cold cache and a virgin filesystem
        shutil.rmtree(root, ignore_errors=True)
        self.materialize(spec, root)
        shutil.rmtree(os.path.join(root, ".cache"), ignore_errors=True)
        env = self.env_for(spec, root)
        argv = [_abs("env", "/usr/bin/env"), "-i"] + \
            ["%s=%s" % kv for kv in sorted(env.items())]
        argv += ["/bin/sh", self.script] + list(spec["args"])
        return root, argv

    def command(self, root, argv):
        if self.mode != "bwrap":
            return argv
        return ["bwrap",
                "--unshare-all", "--die-with-parent", "--new-session",
                "--proc", "/proc", "--dev", "/dev",
                "--ro-bind", "/usr", "/usr",
                "--symlink", "usr/bin", "/bin",
                "--symlink", "usr/lib", "/lib",
                "--symlink", "usr/lib64", "/lib64",
                "--symlink", "usr/sbin", "/sbin",
                "--tmpfs", "/etc", "--tmpfs", "/usr/share",
                "--tmpfs", "/usr/local", "--tmpfs", "/tmp",
                "--ro-bind", self.toolbin, self.toolbin,
                "--bind", root, root,
                "--chdir", root] + argv

    def run_traced(self, spec, logpath):
        """Run once under strace, return (rc, stdout, execve targets,
        socket-call count)."""
        root, argv = self.prepare(spec)
        cmd = [_abs("strace", "/usr/bin/strace"), "-f", "-qq",
               "-e", "trace=execve,socket",
               "-o", logpath] + self.command(root, argv)
        proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, cwd=root,
                              timeout=self.timeout)
        targets = set()
        sockets = 0
        if os.path.exists(logpath):
            with open(logpath, "r", errors="replace") as fh:
                for line in fh:
                    if "socket(" in line:
                        sockets += 1
                    if "execve(" in line and line.rstrip().endswith("= 0"):
                        tgt = line.split('execve("', 1)
                        if len(tgt) == 2:
                            targets.add(tgt[1].split('"', 1)[0])
        return (proc.returncode,
                proc.stdout.decode("utf-8", "surrogateescape"), targets,
                sockets)

    def baseline_sockets(self, logpath):
        """Sockets opened by the wrapper alone, for the same command shape."""
        root = os.path.join(self.roots, "_baseline")
        shutil.rmtree(root, ignore_errors=True)
        os.makedirs(os.path.join(root, "bin"))
        os.makedirs(os.path.join(root, "home"))
        env = {"HOME": root + "/home",
               "PATH": root + "/bin:" + self.toolbin}
        argv = [_abs("env", "/usr/bin/env"), "-i"] + \
            ["%s=%s" % kv for kv in sorted(env.items())]
        argv += ["/bin/sh", "-c", ":"]
        cmd = [_abs("strace", "/usr/bin/strace"), "-f", "-qq",
               "-e", "trace=execve,socket",
               "-o", logpath] + self.command(root, argv)
        subprocess.run(cmd, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, cwd=root,
                       timeout=self.timeout)
        n = 0
        with open(logpath, "r", errors="replace") as fh:
            for line in fh:
                if "socket(" in line:
                    n += 1
        return n

    def run(self, spec):
        root, argv = self.prepare(spec)
        cmd = self.command(root, argv)
        try:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, cwd=root,
                                  timeout=self.timeout)
        except subprocess.TimeoutExpired:
            # Not a usable fixture: `expect` cannot express "never returns".
            return None, "", "timeout after %ss" % self.timeout
        stdout = proc.stdout.decode("utf-8", "surrogateescape")
        stdout = stdout.replace(root, "$ROOT")
        return proc.returncode, stdout, proc.stderr.decode("utf-8",
                                                           "replace")

    def expect_for(self, spec, repeat=2):
        """Run `repeat` times; every run must agree (stability gate)."""
        runs = []
        for _ in range(max(1, repeat)):
            rc, out, _err = self.run(spec)
            if rc is None:
                return None, runs + [(None, out)]
            runs.append((rc, out))
        first = runs[0]
        for other in runs[1:]:
            if other != first:
                return None, runs
        return first, runs


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def check_want(spec, rc, stdout):
    want = spec.get("want")
    if not want:
        return None
    if want == "@reject":
        if rc == 0 or stdout != "":
            return "%s: want reject, got rc=%d stdout=%r" % (
                spec["id"], rc, stdout[:80])
        return None
    if want.startswith("@select:"):
        needle = want[len("@select:"):]
        if rc != 0 or needle not in stdout:
            return "%s: want %r, got rc=%d stdout=%r" % (
                spec["id"], needle, rc, stdout[:120])
        return None
    return None


def verify_fixtures(args, work, digest):
    """Replay a fixtures JSON using only its frozen keys and re-run the real
    script.  This is the shape the C1 counter uses: the file must be
    self-sufficient (no knowledge of the generator's spec objects)."""
    with open(args.verify, encoding="utf-8") as fh:
        fixtures = json.load(fh)
    sandbox = Sandbox(os.path.join(work, "verify"), args.script,
                      args.sandbox, args.timeout)
    todo = fixtures[:args.verify_limit] if args.verify_limit else fixtures
    bad = []
    refused = []
    for fx in todo:
        spec = {k: fx[k] for k in ("id", "env", "files", "exec", "args")}
        try:
            got, runs = sandbox.expect_for(spec, repeat=max(1, args.repeat))
        except SandboxError as exc:
            # e.g. an args vector that would reach exec; never run those.
            refused.append({"id": fx["id"], "reason": str(exc)})
            continue
        if got is None:
            bad.append((fx["id"], "unstable/timeout", runs))
            continue
        rc, stdout = got
        want = fx["expect"]
        if rc != want["rc"] or stdout != want["stdout"]:
            bad.append((fx["id"], "mismatch",
                        {"want": want, "got": {"rc": rc, "stdout": stdout}}))
    report = {"verified": len(todo) - len(refused),
              "mismatches": len(bad), "refused": refused,
              "script": args.script, "script_sha256": digest,
              "sandbox": args.sandbox, "repeat": args.repeat,
              "failures": bad[:20]}
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.summary_out:
        with open(args.summary_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 1 if bad else 0


def tripwire(args, work, fixtures, digest):
    """Evidence that the reference run never starts a terminal and never opens
    a socket.  Traces every fixture; flags any execve of a $ROOT/bin stub."""
    sandbox = Sandbox(os.path.join(work, "trip"), args.script,
                      args.sandbox, args.timeout)
    logdir = os.path.join(work, "trip", "logs")
    os.makedirs(logdir, exist_ok=True)
    # Socket calls observed for the bare wrapper: bwrap's own sync channel.
    basepath = os.path.join(logdir, "_baseline.strace")
    baselines = [sandbox.baseline_sockets(basepath) for _ in range(3)]
    baseline = baselines[0]
    per_case = {}
    all_targets = set()
    bad = []
    stub_offenders = []
    socket_offenders = []
    for fx in fixtures:
        spec = {k: fx[k] for k in ("id", "env", "files", "exec", "args")}
        log = os.path.join(logdir, fx["id"] + ".strace")
        rc, _out, targets, sockets = sandbox.run_traced(spec, log)
        per_case[fx["id"]] = {"rc": rc, "execve": sorted(targets),
                              "socket_calls": sockets}
        all_targets |= targets
        root = os.path.join(work, "trip", "roots", fx["id"])
        stub_hits = sorted(t for t in targets if t.startswith(root + "/bin/"))
        if stub_hits:
            stub_offenders.append({"id": fx["id"], "stub_execve": stub_hits})
        if sockets - baseline > 0:
            socket_offenders.append({"id": fx["id"], "socket_calls": sockets,
                                     "baseline": baseline})
        if rc != fx["expect"]["rc"]:
            bad.append({"id": fx["id"], "want": fx["expect"]["rc"],
                        "got": rc})
        os.unlink(log)

    def counts(targets):
        hist = {}
        for t in targets:
            name = os.path.basename(t)
            hist[name] = hist.get(name, 0) + 1
        return hist

    socket_values = sorted({v["socket_calls"] for v in per_case.values()})
    report = {
        "fixtures_traced": len(fixtures),
        "script_sha256": digest,
        "sandbox": args.sandbox,
        "distinct_execve_targets": sorted(all_targets),
        "execve_basename_histogram": dict(sorted(counts(all_targets).items())),
        "wrapper_socket_baseline": {"runs": baselines,
                                    "stable": len(set(baselines)) == 1},
        "distinct_socket_calls_per_case": socket_values,
        "cases_exec_inside_case_root_bin": stub_offenders,
        "cases_with_socket_calls_above_baseline": socket_offenders,
        "rc_mismatches": bad,
        "verdict": ("PASS" if not stub_offenders and not socket_offenders
                    and not bad else "FAIL"),
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    with open(args.tripwire_out, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(text)
    return 0 if report["verdict"] == "PASS" else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Generate xdg-terminal-exec selection fixtures from the "
                    "real pinned script.")
    ap.add_argument("--out", help="output path for fixtures.json")
    ap.add_argument("--work", help="scratch work dir (default $TMPDIR)")
    ap.add_argument("--script", default=DEFAULT_SCRIPT,
                    help="script under test (default %(default)s)")
    ap.add_argument("--sandbox", choices=("bwrap", "none"), default="bwrap",
                    help="isolation for the reference run (default bwrap)")
    ap.add_argument("--repeat", type=int, default=2,
                    help="runs per case; all must agree (default 2)")
    ap.add_argument("--nonce", type=int, metavar="N",
                    help="emit %d random cases from the same grammar"
                         % NONCE_COUNT)
    ap.add_argument("--timeout", type=int, default=20,
                    help="per-run timeout in seconds (default 20)")
    ap.add_argument("--summary", action="store_true",
                    help="print class/rc histograms")
    ap.add_argument("--summary-out", metavar="PATH",
                    help="write the histogram summary JSON to PATH")
    ap.add_argument("--verify", metavar="FILE",
                    help="replay an existing fixtures JSON (only the frozen "
                         "keys are used) and check every expect block")
    ap.add_argument("--verify-limit", type=int, default=0,
                    help="stop after N fixtures in --verify (0 = all)")
    ap.add_argument("--tripwire-out", metavar="PATH",
                    help="run every fixture under strace and record which "
                         "binaries were exec'd and whether socket() was called")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.script):
        print("gen-fixtures: script not found: %s" % args.script,
              file=sys.stderr)
        return 2

    work = args.work or os.environ.get("TMPDIR") or tempfile.gettempdir()
    work = os.path.abspath(work)
    os.makedirs(work, exist_ok=True)

    digest = sha256_file(args.script)
    if args.script == DEFAULT_SCRIPT and digest != PINNED_SHA256:
        print("gen-fixtures: %s sha256 %s != pinned %s"
              % (args.script, digest, PINNED_SHA256), file=sys.stderr)
        return 1
    if args.sandbox == "bwrap" and not shutil.which("bwrap"):
        print("gen-fixtures: bwrap not found; pass --sandbox none only if you "
              "accept host leakage", file=sys.stderr)
        return 2

    if args.verify:
        return verify_fixtures(args, work, digest)

    specs = nonce_cases(args.nonce) if args.nonce is not None else curated()

    sandbox = Sandbox(work, args.script, args.sandbox, args.timeout)
    fixtures = []
    unstable = []
    mismatched = []
    for spec in specs:
        got, runs = sandbox.expect_for(spec, repeat=args.repeat)
        if got is None:
            unstable.append((spec["id"], runs))
            continue
        rc, stdout = got
        problem = check_want(spec, rc, stdout)
        if problem:
            mismatched.append(problem)
        fixtures.append({
            "id": spec["id"],
            "class": spec["cls"],
            "env": spec["env"],
            "files": spec["files"],
            "exec": spec["exec"],
            "args": spec["args"],
            "expect": {"rc": rc, "stdout": stdout},
        })

    if unstable:
        print("gen-fixtures: %d unstable case(s):" % len(unstable),
              file=sys.stderr)
        for cid, runs in unstable[:10]:
            print("  %s %r" % (cid, [(rc, o[:60]) for rc, o in runs]),
                  file=sys.stderr)
    if mismatched:
        print("gen-fixtures: %d class-intent mismatch(es):" % len(mismatched),
              file=sys.stderr)
        for line in mismatched:
            print("  " + line, file=sys.stderr)

    if args.nonce is not None:
        out = args.out or "fixtures-nonce.json"
    else:
        out = args.out or "fixtures.json"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(fixtures, fh, indent=1, ensure_ascii=False, sort_keys=False)
        fh.write("\n")

    if args.tripwire_out:
        with open(out, encoding="utf-8") as fh:
            emitted = json.load(fh)
        rc = tripwire(args, work, emitted, digest)
        if rc:
            return rc

    # ---- receipts -------------------------------------------------------
    classes = {}
    rcs = {}
    selected = 0
    for fx in fixtures:
        classes[fx["class"]] = classes.get(fx["class"], 0) + 1
        rcs[fx["expect"]["rc"]] = rcs.get(fx["expect"]["rc"], 0) + 1
        if fx["expect"]["rc"] == 0:
            selected += 1
    too_small = sorted(c for c, k in classes.items() if k < 3)

    report = {
        "script": args.script,
        "script_sha256": digest,
        "pinned_sha256": PINNED_SHA256,
        "sandbox": args.sandbox,
        "repeat": args.repeat,
        "cases": len(fixtures),
        "classes": len(classes),
        "class_histogram": dict(sorted(classes.items())),
        "rc_histogram": dict(sorted(rcs.items())),
        "selected_terminal": selected,
        "no_terminal": len(fixtures) - selected,
        "classes_below_3": too_small,
        "unstable_excluded": [c for c, _ in unstable],
        "class_intent_mismatches": mismatched,
        "output": out,
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.summary_out:
        with open(args.summary_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)

    bad = bool(too_small or unstable or mismatched)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
