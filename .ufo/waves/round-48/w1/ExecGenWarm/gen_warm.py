#!/usr/bin/env python3
"""gen_warm.py - C1 clause g v2 (mado round 48): generator of WARM-CACHE cases, judged by the pin at count time.

`gen_warm_case(rng, k)` returns one case of the draft fixture schema v2. It is the round-47 `gen_case()` (loaded from
`c1-r47-terminal.py`, beside this file or in an ancestor's `quality/counters/`) plus the cache layer:

    id, class, env ($ROOT), files, exec, args        round-47 fields (unchanged meaning)
  + mtime: <epoch seconds>                           pinned on EVERY materialized file and dir (deterministic `ls -l`:
                                                     the generator only uses dates older than six months, so the
                                                     listing prints "Mon dd  YYYY" and never depends on wall time)
  + prime: {"args": [...], "env": {...}}             a cold oracle run BEFORE the scored run. The harness must
                                                     (1) wait until $XDG_CACHE_HOME/xdg-terminal-exec is complete -
                                                     non-empty and its last line ends with RS+"END_OF_EXEC_USEP" -
                                                     then (2) re-pin `mtime`. `prime.env` overlays the case env for
                                                     the prime only (used to prime with the cache disabled).
  + after: {"files": {path: text|null}, "exec_add": [...], "exec_remove": [...], "env": {...}, "mtime": <epoch>,
            "cache": [{"op": ...}, ...]}             mutations applied after priming, then `after.mtime` (default:
                                                     the case `mtime`) re-pins every file and dir. `files` values
                                                     ending in "/" create a directory, `null` removes the path (a
                                                     directory is removed recursively only when empty). Text tokens:
                                                     $ROOT (case root), $CACHE_HASH (line 1 of the primed cache),
                                                     $USEP (0x1f), $RS (0x1e). `after.cache` edits the primed cache
                                                     line by line, ops in order:
                                                       {"op": "set", "line": N, "text": T}     1-based, N >= 1
                                                       {"op": "append", "lines": [T, ...]}
                                                       {"op": "truncate", "keep": N}
                                                       {"op": "write", "text": T}              whole file (T may use
                                                                                              $CACHE_HASH)
                                                     A single op dict is accepted for a one-element list.
  + cache: "<literal text>"                          a cache file written INSTEAD of priming; no prime (malformed
                                                     caches, where the hash line is irrelevant). Tokens as above.

Invariants the generator keeps (checked by `--check`):
  * every `args` and `prime.args` vector contains a print option or `--test` - the harness NEVER launches a terminal;
  * no path is absolute or contains "..";
  * every case either has "prime" or "cache", never both;
  * the content swaps used by the keep-the-hash families preserve the file's byte length;
  * `class` is "generated-warm:<family>" (the round-47 `class` field, kept descriptive; the counter only reports it).

The injected entry always carries TerminalArgExec=-e: without it a list file holding `/execarg_strict` makes the
resolver skip every entry that has no TerminalArgExec (x:1019-1053), so a prime would select nothing and write no
cache (measured: 51/250 primes failed before the key was added).

Why the mix is roughly half/half: a mutation keeps the md5 that `read_cache` compares iff it leaves the `LANG=C ls -LRl`
listing of $XTE__CONFIGS:$XTE__APPLICATIONS_DIRS unchanged - same names, sizes, modes, nlink, dates and the same set of
directories. Content edits of equal byte length with the same mtime, a same-day mtime shift, and a stub removed from a
directory that is NOT part of the hashed operands (`<root>/bin` is not) all keep it; added/removed/renamed files, size
changes, mode changes, a new directory, a changed mtime DAY, and a changed XDG_CURRENT_DESKTOP all break it.

Pure function of (rng, k): no host read, no process, no clock.
"""
import importlib.util
import os
import sys

sys.dont_write_bytecode = True

USEP = "\x1f"
RS = "\x1e"
DAY = 86400
HOUR = 3600
MT_ANCHOR = 1709985600          # 2024-03-09T12:00:00Z: always older than six months, near a 12:00 anchor

ENTRY = ("[Desktop Entry]\n"
         "Type=Application\n"
         "Categories=TerminalEmulator;\n"
         "TerminalArgExec=-e\n"
         "TerminalArgTitle=-T=\n"
         "Exec={n}\n"
         "TryExec={t}\n")
KEEP_CATS = "Categories=TerminalEmulator;"
BROKEN_CATS = "Categories=TerminalEmulatXr;"
assert len(KEEP_CATS) == len(BROKEN_CATS)

# names whose length is shared with at least one other name, so an Exec swap can keep the file's byte length
SWAP_NAMES = ("kitty", "xterm", "ghostty", "wezterm", "konsole")
STUB_NAMES = ("foot", "alacritty") + SWAP_NAMES
PRIME_ARGVS = [["--print-cmd"],
               ["--print-id", "--print-path", "--print-cmd"],
               ["--print-path", "--print-cmd"],
               ["--print-cmd", "--dir=/srv"],
               ["--print-cmd", "--title=t"],
               ["--print-cmd", "--app-id=cl", "--hold"],
               ["--print-cmd", "--", "htop", "-d", "5"],
               ["--test", "-e", "ls"]]
WITH_CMD_ARGS = ["--print-cmd", "--dir=/srv", "--title=t x", "--app-id=a", "--hold", "top"]


def _r47():
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [os.path.join(here, "c1-r47-terminal.py")]
    d = here
    for _ in range(6):
        d = os.path.dirname(d)
        cands.append(os.path.join(d, "quality", "counters", "c1-r47-terminal.py"))
    for p in cands:
        if os.path.isfile(p):
            spec = importlib.util.spec_from_file_location("mado_c1_r47", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    raise RuntimeError("c1-r47-terminal.py not found beside gen_warm.py or in an ancestor's quality/counters")


R47 = _r47()
ARGVS = [a for a in R47.ARGVS if any(x.startswith("--print-cmd") or x == "--test" for x in a)]


# ------------------------------------------------------------------------------------------------ helpers
def _desktop_ids(files):
    return {rel.rsplit("/", 1)[-1] for rel in files if rel.endswith(".desktop")}


def _free_name(files, avoid=()):
    ids = _desktop_ids(files)
    used = {i[:-8] for i in ids}
    used |= {u[7:] for u in used if u.startswith("vendor-")}
    used |= set(avoid)
    pool = [n for n in SWAP_NAMES if n not in used
            and ("usr/share/applications/%s.desktop" % n) not in files]
    return pool[0] if pool else None


def _strip_cache_directives(files):
    """A list file holding /disable_cache (or /enable_cache) makes a cold run write no cache at all: a warm case
    cannot be primed from such a tree. The directive families are generated explicitly instead (a same-size content
    swap that keeps the hash, and XTE_CACHE_ENABLED in the environment)."""
    for rel in list(files):
        if rel.endswith("xdg-terminals.list"):
            lines = [ln for ln in files[rel].split("\n") if ln.strip() not in ("/disable_cache", "/enable_cache")]
            files[rel] = "\n".join(lines)


def _ensure_list(files, eid):
    """Put `eid` as the first entry line of every list file, so the PRIME selects the injected entry and the warm
    answer is a function of that entry; the base list noise stays behind it. A list file is created when the base has
    none (the default XDG_CONFIG_HOME is <root>/home/.config, which gen_case always leaves in place or unsets)."""
    line = eid + "\n"
    for rel in list(files):
        if rel.endswith("xdg-terminals.list"):
            files[rel] = line + files[rel]
    if "home/.config/xdg-terminals.list" not in files:
        files["home/.config/xdg-terminals.list"] = line


def _has_list(files):
    return [p for p in files if p.endswith("xdg-terminals.list")]


def _fresh_stub(files, avoid):
    names = set(avoid)
    for text in files.values():
        for line in text.splitlines():
            if line.startswith("Exec="):
                names.add(line[5:].strip().strip('"').split(" ")[0])
    for n in STUB_NAMES:
        if n not in names:
            return n
    return None


def _cache_lines(n, execarg="-e"):
    return ["4", n, "$ROOT/usr/share/applications/%s.desktop" % n, "%s.desktop" % n, "", execarg,
            "", "", "", ""]


def _literal_cache(kind, n):
    head = "\n".join(_cache_lines(n))
    if kind == "empty":
        return ""
    if kind == "no-terminator":
        return head + "\n" + "\n".join("junk%d" % i for i in range(3)) + "\n"
    if kind == "long-no-terminator":
        return head + "\n" + "\n".join("junk%d" % i for i in range(39)) + "\n"
    if kind == "fifty-lines":
        # 49 lines without the sentinel, sentinel on line 50: read_cache returns 1 at the line limit before parsing it
        return head + "\n" + "\n".join("junk%d" % i for i in range(39)) + "\n%s%sEND_OF_EXEC_USEP\n" % (n, RS)
    if kind == "garbage-hash":
        return "\n".join(["deadbeef"] + _cache_lines(n)[1:]) + "\n%s%sEND_OF_EXEC_USEP\n" % (n, RS)
    if kind == "sentinel-line-10":
        # the 10th line is the holdarg field, so a sentinel there is never seen: no terminator -> invalid
        return "\n".join(_cache_lines(n)[:9] + ["hold%sEND_OF_EXEC_USEP" % RS]) + "\n"
    raise AssertionError(kind)


# ------------------------------------------------------------------------------------------------ families
def _prime(rng):
    return {"args": list(rng.choice(PRIME_ARGVS))}


def _keep(rng, c, n, twin, t3, epath, etxt, mtime):
    """Mutations that leave the `ls -LRl` listing (and so the md5) unchanged."""
    kind = rng.choices(
        ["exec-swap", "mtime-same-day", "tryexec-stub-gone", "disable-cache-same-size",
         "unrelated-stub-gone", "cache-tamper", "categories-corrupt", "titlearg-swap"],
        weights=[20, 6, 12, 7, 5, 28, 11, 11])[0]
    c["prime"] = _prime(rng)
    after = {"mtime": mtime}
    if kind == "exec-swap":
        new = etxt.replace("Exec=%s\n" % n, "Exec=%s\n" % twin)
        assert len(new) == len(etxt)
        after["files"] = {epath: new}
    elif kind == "mtime-same-day":
        after["mtime"] = mtime + 3 * HOUR
    elif kind == "tryexec-stub-gone":
        after["exec_remove"] = ["bin/" + t3]
    elif kind == "unrelated-stub-gone":
        gone = _fresh_stub(c["files"], (n, twin, t3))
        if gone is None:
            after["mtime"] = mtime + 3 * HOUR
            kind = "mtime-same-day"
        else:
            c["exec"].append("bin/" + gone)             # exists before the prime, gone after it
            after["exec_remove"] = ["bin/" + gone]
    elif kind == "disable-cache-same-size":
        lp = next((p for p in R47.LISTS if p not in c["files"]), None)
        if lp is None:
            lp = rng.choice(R47.LISTS)
        c["files"][lp] = "#" + " " * 13 + "\n"          # 15 bytes, no entry, no directive
        after["files"] = {lp: "/disable_cache\n"}       # 15 bytes: same size, same mtime -> the cache still wins
    elif kind == "titlearg-swap":
        new = etxt.replace("TerminalArgTitle=-T=", "TerminalArgTitle=-X=")
        assert len(new) == len(etxt)
        after["files"] = {epath: new}
        c["args"] = ["--print-cmd", "--title=t x", "--", "a"]
    elif kind == "categories-corrupt":
        new = etxt.replace(KEEP_CATS, BROKEN_CATS)
        assert len(new) == len(etxt)
        after["files"] = {epath: new}
    else:                                               # cache-tamper: keep the tree, rewrite the cache
        sub = rng.choices(["cmd", "entry", "multiline", "action", "args", "after-sentinel", "execarg"],
                          weights=[18, 14, 16, 12, 16, 8, 16])[0]
        after.pop("mtime", None)                        # nothing in the tree changes
        if sub == "cmd":
            other = twin if twin != n else t3
            after["cache"] = [{"op": "set", "line": 2, "text": other}]
        elif sub == "entry":
            after["cache"] = [{"op": "set", "line": 3, "text": "$ROOT/opt/share/applications/ghost.desktop"},
                              {"op": "set", "line": 4, "text": "ghost.desktop"}]
            c["args"] = ["--print-id", "--print-path", "--print-cmd"]
        elif sub == "multiline":
            after["cache"] = [{"op": "truncate", "keep": 10},
                              {"op": "append", "lines": ["%s%s-e%s/usr/bin/env" % (n, USEP, USEP),
                                                         "second%sEND_OF_EXEC_USEP" % RS]}]
        elif sub == "action":
            after["cache"] = [{"op": "set", "line": 5, "text": "new"}]
            c["args"] = ["--print-id", "--print-path", "--print-cmd"]
        elif sub == "args":
            after["cache"] = [{"op": "set", "line": 7, "text": "--carrier"},
                              {"op": "set", "line": 8, "text": "--titre"},
                              {"op": "set", "line": 9, "text": "--directory="},
                              {"op": "set", "line": 10, "text": "--hold"}]
            c["args"] = list(WITH_CMD_ARGS)
        elif sub == "after-sentinel":
            after["cache"] = [{"op": "append", "lines": ["ignored", "also-ignored"]}]
        else:
            after["cache"] = [{"op": "set", "line": 6, "text": "--cached-execarg"}]
            c["args"] = ["--print-cmd", "--", "a", "b"]
    c["after"] = after
    return "keep:" + kind


def _break(rng, c, n, twin, t3, epath, etxt, mtime):
    """Mutations that change the listing (the cache is out of date) or the cached command."""
    kind = rng.choices(
        ["mtime-next-day", "inert-desktop-added", "higher-pref-desktop", "list-removed",
         "exec-size-change", "entry-renamed", "desktop-env-change", "mode-change",
         "new-subdir", "shadowing-list", "cache-removed"],
        weights=[10, 10, 15, 8, 15, 10, 10, 6, 8, 10, 6])[0]
    c["prime"] = _prime(rng)
    after = {"mtime": mtime}
    if kind == "mtime-next-day":
        after["mtime"] = mtime + 3 * DAY
    elif kind == "inert-desktop-added":
        after["files"] = {"usr/share/applications/zzz-r48.desktop": "[Desktop Entry]\nName=inert\n"}
    elif kind == "higher-pref-desktop":
        m = _free_name(c["files"], (n, twin, t3))
        if m is None:
            after["mtime"] = mtime + 3 * DAY
            kind = "mtime-next-day"
        else:
            long = m + "x"
            after["files"] = {"home/.local/share/applications/%s.desktop" % long:
                              ENTRY.format(n=long, t=long)}
            after["exec_add"] = ["bin/" + long]
    elif kind == "list-removed":
        lp = _has_list(c["files"])
        if not lp:
            lp = [rng.choice(R47.LISTS)]
            c["files"][lp[0]] = "%s.desktop\n" % n
        after["files"] = {lp[0]: None}
    elif kind == "exec-size-change":
        long = twin + "x"
        new = etxt.replace("Exec=%s\n" % n, "Exec=%s\n" % long)
        after["files"] = {epath: new}
        after["exec_add"] = ["bin/" + long]
    elif kind == "entry-renamed":
        newp = "usr/share/applications/vendor/%s.desktop" % n
        after["files"] = {epath: None, newp: etxt}
    elif kind == "desktop-env-change":
        cur = c["env"].get("XDG_CURRENT_DESKTOP")
        vals = [v for v in ("KDE", "GNOME", "Hyprland:GNOME", "GNOME:Hyprland") if v != cur]
        if cur not in (None, ""):
            vals.append("")                     # unset and empty print the same hash line, so only add it when it differs
        after["env"] = {"XDG_CURRENT_DESKTOP": rng.choice(vals)}
    elif kind == "mode-change":
        after["exec_add"] = [epath]                     # 0644 -> 0755: the mode column of the listing changes
    elif kind == "new-subdir":
        after["files"] = {"usr/share/applications/vendor/r48/r48.desktop":
                          "[Desktop Entry]\nName=r48\nCategories=System;\nExec=missing\n"}
    elif kind == "shadowing-list":
        m = _free_name(c["files"], (n, twin, t3))
        lp = "home/.config/xdg-terminals.list"
        if m is None:
            after["mtime"] = mtime + 3 * DAY
            kind = "mtime-next-day"
        else:
            after["files"] = {lp: "%s.desktop\n" % m + c["files"].get(lp, ""),
                              "opt/share/applications/%s.desktop" % m: ENTRY.format(n=m, t=m)}
            after["exec_add"] = ["bin/" + m]
    else:                                               # cache-removed
        after["files"] = {".rw/cache/xdg-terminal-exec": None}
    c["after"] = after
    return "break:" + kind


def _disabled(rng, c, n, twin, t3, epath, etxt, mtime):
    kind = rng.choices(["env-after", "prime-disabled", "env-zero"], weights=[50, 25, 25])[0]
    if kind == "env-after":
        c["prime"] = _prime(rng)
        c["after"] = {"files": {epath: etxt.replace("Exec=%s\n" % n, "Exec=%s\n" % twin)},
                      "env": {"XTE_CACHE_ENABLED": "false"}, "mtime": mtime}
    elif kind == "prime-disabled":
        c["prime"] = _prime(rng)
        c["prime"]["env"] = {"XTE_CACHE_ENABLED": "false"}
        c["after"] = {"mtime": mtime}
    else:
        c["prime"] = _prime(rng)
        c["after"] = {"env": {"XTE_CACHE_ENABLED": "0"}, "mtime": mtime}
    return "disabled:" + kind


def _malformed(rng, c, n):
    """Literal cache text, no prime: the hash line cannot match, so every one of these is rejected."""
    kind = rng.choices(["empty", "no-terminator", "long-no-terminator", "fifty-lines",
                        "garbage-hash", "sentinel-line-10"],
                       weights=[8, 20, 12, 16, 28, 16])[0]
    c["cache"] = _literal_cache(kind, n)
    return "literal:" + kind


# ------------------------------------------------------------------------------------------------ case
def gen_warm_case(rng, k=None):
    """One fixture-schema-v2 warm-cache case, deterministic in (rng, k)."""
    k = 0 if k is None else int(k)
    base = R47.gen_case(rng, k)
    files = dict(base["files"])
    _strip_cache_directives(files)
    execs = list(dict.fromkeys(base["exec"]))
    env = dict(base["env"])
    n = _free_name(files)
    if n is None:
        n = "kitty"
        files.pop("usr/share/applications/kitty.desktop", None)
    twin = rng.choice([m for m in SWAP_NAMES if len(m) == len(n) and m != n] or [n])
    used_exec = set()
    for text in files.values():
        for line in text.splitlines():
            if line.startswith("Exec="):
                used_exec.add(line[5:].strip().strip('"').split(" ")[0])
    t3 = rng.choice([m for m in STUB_NAMES if m not in used_exec and m not in (n, twin)] or ["foot"])
    epath = "usr/share/applications/%s.desktop" % n
    etxt = ENTRY.format(n=n, t=t3)
    files[epath] = etxt
    _ensure_list(files, n + ".desktop")
    execs = list(dict.fromkeys(execs + ["bin/" + x for x in (n, twin, t3)]))
    mtime = MT_ANCHOR - rng.randrange(0, 40) * DAY
    case = {"id": "w%03d" % k, "class": "", "env": env, "files": files, "exec": execs,
            "args": list(base["args"]), "mtime": mtime}
    case["args"] = list(rng.choice(ARGVS))   # every vector prints: never a launch, and --print-cmd shows the cache

    r = rng.random()
    if r < 0.20:
        fam = _malformed(rng, case, n)
    elif r < 0.25:
        fam = _disabled(rng, case, n, twin, t3, epath, etxt, mtime)
    elif r < 0.625:
        fam = _keep(rng, case, n, twin, t3, epath, etxt, mtime)
    else:
        fam = _break(rng, case, n, twin, t3, epath, etxt, mtime)
    case["class"] = "generated-warm:" + fam.replace(":", "-", 1)
    return case


# ------------------------------------------------------------------------------------------------ self-check
def check_case(case):
    """Invariants a counter may rely on; raises AssertionError."""
    assert isinstance(case, dict), case
    for key in ("id", "class", "env", "files", "exec", "args"):
        assert key in case, key
    assert ("prime" in case) != ("cache" in case), "exactly one of prime/cache"
    for vec in [case["args"]] + ([case["prime"]["args"]] if "prime" in case else []):
        assert any(a.startswith("--print-") or a == "--test" for a in vec), vec
    after = case.get("after") or {}
    paths = list(case["files"]) + list(after.get("files") or {})
    paths += list(case["exec"]) + list(after.get("exec_add") or [])
    paths += list(after.get("exec_remove") or [])
    for p in paths:
        assert not p.startswith("/") and ".." not in p.split("/"), p
    return True


def main(argv):
    import json
    import random
    n, seed = 5, 0
    if argv[:1] == ["--n"]:
        n = int(argv[1])
        argv = argv[2:]
    if argv[:1] == ["--seed"]:
        seed = int(argv[1])
    rng = random.Random(seed)
    cases = []
    for k in range(n):
        c = gen_warm_case(rng, k)
        check_case(c)
        cases.append(c)
    print(json.dumps(cases, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
