#!/usr/bin/env python3
"""Author of fixtures-v2.json for oracle2.py (round 48 w1, seat ExecOracleV2).

`expect` is never typed here: run `oracle2.py --emit-expect fixtures-v2.json` and the pinned
resolver fills it in. `want_cache` IS declared here, and oracle2.py fails the case when the
resolver's own debug channel disagrees - it catches a case whose construction silently stopped
producing the state it was meant to produce (a "warm-diff" case that quietly became cold).

Classes:
  hit              cache trusted, warm answer equals the cold one (baseline / control)
  warm-diff        cache trusted, warm answer DIFFERS from what a cold run would answer
  invalidated-*    the mutation breaks the hash or the `command -v`, so the cache is not used
  malformed        a literal cache file the parser rejects; there is no priming
  disabled         XTE_CACHE_ENABLED=false, or a /disable_cache directive
  explain          `explain` mode: the tool must name selected/path/verdict/cache
  contract         HOME unset (round-47 D1), no cache involved
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = 1700000000          # 2023-11-14: `ls -l` shows the YEAR, so time-of-day is invisible
NEW_YEAR = 1735000000     # 2024-12-24: a different year, visible again

CAT = "Categories=System;TerminalEmulator;\n"
LIST = "home/.config/xdg-terminals.list"
APPS = "usr/share/applications/"
ENV = {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_DATA_DIRS": "$ROOT/usr/share",
       "XDG_CURRENT_DESKTOP": "Hyprland"}


def entry(name, exec_line, extra=""):
    return ("[Desktop Entry]\nType=Application\nName=%s\nExec=%s\n%s%s"
            % (name, exec_line, CAT, extra))


def files(list_text, foot_extra="", kitty_extra="", foot_exec="foot", kitty_exec="kitty",
          extra_files=None):
    out = {LIST: list_text,
           APPS + "foot.desktop": entry("foot", foot_exec, foot_extra),
           APPS + "kitty.desktop": entry("kitty", kitty_exec, kitty_extra)}
    out.update(extra_files or {})
    return out


def case(cid, cls, want_cache, **kw):
    c = {"id": cid, "class": cls, "want_cache": want_cache,
         "files": files("foot.desktop\n"), "exec": ["bin/foot", "bin/kitty"],
         "args": ["--print-cmd"], "env": dict(ENV), "mtime": OLD,
         "prime": {"args": ["--print-cmd"]}}
    c.update(kw)
    return c


def cases():
    out = []

    # ---- controls: the cache is trusted and the answer does not move -------------------------
    out.append(case("hit-baseline", "hit", "hit"))
    out.append(case("hit-print-id", "hit", "hit", args=["--print-id"]))
    out.append(case("hit-print-path", "hit", "hit", args=["--print-path"]))
    out.append(case("hit-print-id-path", "hit", "hit", args=["--print-id", "--print-path"]))
    out.append(case("hit-print-content", "hit", "hit", args=["--print-content"]))
    out.append(case("hit-enable-env", "hit", "hit", env=dict(ENV, XTE_CACHE_ENABLED="true")))
    out.append(case("hit-fallback-entry", "hit", "hit",
                    files=files("kitty.desktop\n", extra_files={
                        APPS + "alacritty.desktop": entry("alacritty", "alacritty")}),
                    exec=["bin/kitty", "bin/alacritty", "bin/foot"]))

    # ---- warm-diff: the cache is trusted but the tree now says something else ----------------
    # same size, same pinned mtime: the listing is byte identical, only the content moved
    out.append(case("wd-exec-same-size", "warm-diff", "hit",
                    after={"files": {APPS + "foot.desktop": entry("foot", "f00t")}}))
    out.append(case("wd-list-same-size", "warm-diff", "hit",
                    files=files("foot.desktop\n", extra_files={
                        APPS + "fooz.desktop": entry("fooz", "fooz")}),
                    exec=["bin/foot", "bin/kitty", "bin/fooz"],
                    after={"files": {LIST: "fooz.desktop\n"}}))
    # TryExec resolves at selection time, Exec[0] at cache-validation time: removing the TryExec
    # stub is invisible to the hash and to `command -v foot`
    out.append(case("wd-tryexec-stub-gone", "warm-diff", "hit",
                    files=files("foot.desktop\n", foot_extra="TryExec=footex\n"),
                    exec=["bin/foot", "bin/kitty", "bin/footex"],
                    after={"exec_remove": ["bin/footex"]}))
    # the cached argument NAME over a changed command line value
    out.append(case("wd-dir-arg-name", "warm-diff", "hit",
                    files=files("foot.desktop\n",
                                foot_extra="X-TerminalArgDir=--working-directory=\n"),
                    args=["--print-cmd", "--dir=$ROOT/w"],
                    after={"files": {APPS + "foot.desktop": entry(
                        "foot", "foot", "X-TerminalArgDir=--working-directorx=\n")}}))
    out.append(case("wd-title-arg-name", "warm-diff", "hit",
                    files=files("foot.desktop\n",
                                foot_extra="X-TerminalArgTitle=--title=\n"),
                    args=["--print-cmd", "--title=T"],
                    after={"files": {APPS + "foot.desktop": entry(
                        "foot", "foot", "X-TerminalArgTitle=--titlx=\n")}}))
    out.append(case("wd-appid-arg-name", "warm-diff", "hit",
                    files=files("foot.desktop\n",
                                foot_extra="X-TerminalArgAppId=--app-id=\n"),
                    args=["--print-cmd", "--app-id=A"],
                    after={"files": {APPS + "foot.desktop": entry(
                        "foot", "foot", "X-TerminalArgAppId=--app-ix=\n")}}))
    out.append(case("wd-execarg-name", "warm-diff", "hit",
                    files=files("foot.desktop\n", foot_extra="X-TerminalArgExec=-x\n"),
                    args=["--print-cmd", "--", "echo", "hi"],
                    after={"files": {APPS + "foot.desktop": entry(
                        "foot", "foot", "X-TerminalArgExec=-y\n")}}))
    out.append(case("wd-hold-arg-name", "warm-diff", "hit",
                    files=files("foot.desktop\n", foot_extra="X-TerminalArgHold=--hold\n"),
                    args=["--print-cmd", "--hold", "--", "echo"],
                    after={"files": {APPS + "foot.desktop": entry(
                        "foot", "foot", "X-TerminalArgHold=--holx\n")}}))
    # the old-date blind spot: `ls -l` prints the year for these files, so a one hour shift of
    # the mtime does not change the listing at all
    out.append(case("wd-mtime-blind-old-date", "warm-diff", "hit",
                    after={"mtime": OLD + 3600,
                           "files": {APPS + "foot.desktop": entry("foot", "f00t")}}))
    out.append(case("wd-action-cmd", "warm-diff", "hit",
                    files=files("foot.desktop:new\n", foot_extra=(
                        "Actions=new;\n\n[Desktop Action new]\nName=new\nExec=foot new\n")),
                    after={"files": {APPS + "foot.desktop": entry(
                        "foot", "foot",
                        "Actions=new;\n\n[Desktop Action new]\nName=new\nExec=foot neq\n")}}))
    # a preference list edit that keeps size: the cached id wins over the new preference
    out.append(case("wd-two-lists", "warm-diff", "hit",
                    files=files("kitty.desktop\n", extra_files={
                        "home/.config/hyprland-xdg-terminals.list": "foot.desktop\n",
                        APPS + "fooz.desktop": entry("fooz", "fooz")}),
                    exec=["bin/foot", "bin/kitty", "bin/fooz"],
                    after={"files": {"home/.config/hyprland-xdg-terminals.list":
                                     "fooz.desktop\n"}}))

    # ---- invalidated: the hash, or `command -v`, rejects the cache ---------------------------
    out.append(case("inv-size-change", "invalidated-size", "stale",
                    after={"files": {APPS + "foot.desktop": entry("foot", "foottyy")}},
                    exec=["bin/foot", "bin/kitty", "bin/foottyy"]))
    out.append(case("inv-mtime-year", "invalidated-mtime", "stale",
                    after={"mtime": NEW_YEAR,
                           "files": {APPS + "foot.desktop": entry("foot", "f00t")}}))
    out.append(case("inv-entry-removed", "invalidated-name", "stale",
                    after={"files": {APPS + "foot.desktop": None}}))
    out.append(case("inv-entry-added", "invalidated-name", "stale",
                    after={"files": {APPS + "zzz.desktop": entry("zzz", "zzz")}}))
    out.append(case("inv-desktop-change", "invalidated-desktop", "stale",
                    after={"files": {"home/.config/gnome-xdg-terminals.list": "kitty.desktop\n"},
                           "env": {"XDG_CURRENT_DESKTOP": "GNOME"}}))
    out.append(case("inv-exec0-gone", "invalidated-exec0", "stale",
                    after={"exec_remove": ["bin/foot"]}))
    out.append(case("inv-prime-print-id", "invalidated-noprime", "absent",
                    prime={"args": ["--print-id"]}))
    out.append(case("inv-cache-removed", "invalidated-name", "absent",
                    after={"files": {"$ROOT/.rw/cache/xdg-terminal-exec": None}}))

    # ---- malformed literal caches (no priming) ----------------------------------------------
    good_head = ("%s\nfoot\n" % ("0" * 32))
    out.append(case("mf-empty", "malformed", "invalid", prime=None, cache=""))
    out.append(case("mf-no-terminator", "malformed", "invalid", prime=None,
                    cache=(good_head + "p\nfoot.desktop\n\n-e\n\n\n\n\nfoot\n")))
    out.append(case("mf-terminator-no-newline", "malformed", "invalid", prime=None,
                    cache=(good_head + "p\nfoot.desktop\n\n-e\n\n\n\n\nfoot\x1eEND_OF_EXEC_USEP")))
    out.append(case("mf-line-limit", "malformed", "invalid", prime=None,
                    cache=("".join("x\n" for _ in range(49))
                           + "foot\x1eEND_OF_EXEC_USEP\n")))
    out.append(case("mf-terminator-at-11", "malformed", "stale", prime=None,
                    cache=(good_head + "p\nfoot.desktop\n\n-e\n\n\n\n\nfoot\x1eEND_OF_EXEC_USEP\n")))
    out.append(case("mf-crlf", "malformed", "invalid", prime=None,
                    cache=(good_head + "p\nfoot.desktop\n\n-e\n\n\n\n\nfoot\x1eEND_OF_EXEC_USEP\r\n")))
    out.append(case("mf-short-hash", "malformed", "stale", prime=None,
                    cache=("abc\nfoot\np\nfoot.desktop\n\n-e\n\n\n\n\nfoot\x1eEND_OF_EXEC_USEP\n")))
    out.append(case("mf-cmd-missing", "malformed", "stale", prime=None,
                    cache=(good_head + "nosuchterm\np\nfoot.desktop\n\n-e\n\n\n\n\n"
                           "nosuchterm\x1eEND_OF_EXEC_USEP\n")))

    # ---- disabled ---------------------------------------------------------------------------
    out.append(case("dis-env-false", "disabled", "disabled", args=["--print-id"],
                    after={"env": {"XTE_CACHE_ENABLED": "false"}}))
    out.append(case("dis-env-no", "disabled", "disabled", args=["--print-id"],
                    after={"env": {"XTE_CACHE_ENABLED": "no"}}))
    # a /disable_cache directive is parsed AFTER the cache read (pin:1179 then pin:1201), so it
    # cannot unseat a valid cache - same size, same mtime keeps the hash
    out.append(case("dis-directive-inert", "disabled", "hit",
                    files=files("#/disable_cach\nfoot.desktop\n"),
                    after={"files": {LIST: "/disable_cache\nfoot.desktop\n"}}))
    out.append(case("dis-directive-cold", "disabled", "absent", prime=None, args=["--print-id"],
                    files=files("/disable_cache\nfoot.desktop\n")))

    # ---- explain ----------------------------------------------------------------------------
    three = ["--print-id", "--print-path", "--print-cmd"]
    out.append(case("ex-hit", "explain", "hit", mode="explain", args=three))
    out.append(case("ex-stale", "explain", "stale", mode="explain", args=three,
                    after={"files": {APPS + "foot.desktop": entry("foot", "foottyy")}},
                    exec=["bin/foot", "bin/kitty", "bin/foottyy"]))
    out.append(case("ex-absent", "explain", "absent", mode="explain", args=three,
                    prime=None))
    out.append(case("ex-disabled", "explain", "disabled", mode="explain", args=three,
                    after={"env": {"XTE_CACHE_ENABLED": "false"}}))
    out.append(case("ex-invalid", "explain", "invalid", mode="explain", args=three,
                    prime=None, cache=good_head))

    # ---- contract: HOME unset (round-47 D1) -------------------------------------------------
    out.append(case("ct-home-unset", "contract", None, prime=None,
                    env=dict(ENV, HOME=None, XDG_CACHE_HOME=None)))
    return out


def main():
    out = []
    for c in cases():
        if c.get("prime") is None:
            c.pop("prime", None)
        out.append(c)
    seen = set()
    for c in out:
        if c["id"] in seen:
            raise SystemExit("duplicate id %s" % c["id"])
        seen.add(c["id"])
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "fixtures-v2.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("%s cases=%d" % (dest, len(out)))


if __name__ == "__main__":
    main()
