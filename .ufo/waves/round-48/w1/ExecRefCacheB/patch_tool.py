#!/usr/bin/env python3
"""Build mado-terminal.py (this seat's warm-cache patch of tools/mado-terminal.py) mechanically.

  python3 patch_tool.py

Reads  <lane>/tools/mado-terminal.py            (base, never written)
       <seat>/warmcache.py                      (the module; its body is inlined verbatim)
Writes <seat>/mado-terminal.py

Every replacement asserts that its anchor occurs exactly once, so a base drift fails loudly instead of
silently producing a half-patched tool. The inlined region is byte-identical to warmcache.py from the
"# xdg-terminal-exec constants" line to EOF (receipts/inline-identical.txt checks that after the fact).
"""
import hashlib
import os
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(SEAT, "..", "..", "..", "..", ".."))
BASE = os.path.join(LANE, "tools", "mado-terminal.py")
MODULE = os.path.join(SEAT, "warmcache.py")
OUT = os.path.join(SEAT, "mado-terminal.py")

REGION_START = "# xdg-terminal-exec constants"      # first line of the inlined region in warmcache.py
BEGIN = "# --------------------------------------------------------- warm cache (inlined, verbatim) --"
END = "# --------------------------------------------------------- end of the warm-cache block --------"

DOC_CACHE_NEW = """Cache (x:217-298, x:1166-1180) - modelled, hit and miss. Before reading any list or entry the resolver tries
$XDG_CACHE_HOME/xdg-terminal-exec (default $HOME/.cache) unless `check_bool "$XTE_CACHE_ENABLED"` fails, and it
uses the file only when all three hold: it parses (10 field lines, then the command on lines 11.. up to a line
ending in 0x1e"END_OF_EXEC_USEP"; reaching line 50 or the end of the file first is "invalid", x:224-259); its
first line equals the md5 of "4\\n$XDG_CURRENT_DESKTOP\\n" plus `LC_ALL=C LANG=C ls -LRl` of the colon-split
${XTE__CONFIGS}:${XTE__APPLICATIONS_DIRS} with stderr dropped (x:179-215); and `command -v` finds its second
line (x:283). On a hit the cached entry path/id/action, exec argument, ap-id/title/dir/hold arguments and the
whole command are used and NO list or entry file is read, so a cache that still hashes correctly but describes
an older tree makes the resolver print what a cold run would not (an edit that keeps the file's size and its
minute of mtime is invisible to the hash). The cache file produces one of
  cache=absent     no regular file at the path (a directory or FIFO is not a cache: `[ -f ]`)
  cache=invalid    it exists but does not parse (no terminator, or line 50 reached)
  cache=stale      it parses, but the hash differs or the cached command does not resolve
  cache=hit        all three hold and the cached values are used
  cache=disabled   XTE_CACHE_ENABLED is false (`check_bool`), so it is not even read
A /disable_cache directive does NOT prevent a hit: directives are read on the cold path only, and the resolver
does not save over a hit (`save_cache` runs only when the cache was NOT used, x:1451-1455), so the file stays.
An unreadable cache file is a cold path with a shell redirection error on stderr, not an exit: `read_cache` sits
inside an `&&` list, where `set -e` does not apply (x:1179). This tool never writes the cache the resolver would
save, so `print` leaves the environment exactly as it found it.

The hash's `ls -LRl` (x:204) is reproduced byte for byte: -L dereferencing (an entry whose stat then fails is
`l?????????`, the type letter taken from the dirent), files-then-directories operand order with a byte sort inside
each group, per-block column widths (the file block widens from the directory operands too), `total N` in 1 KiB
units rounded up from st_blocks, C-locale dates (12 columns; "Mon dd HH:MM" inside 31556952/2 s and not in the
future, else "Mon dd  YYYY"), recursion headers built from the operand as typed, cycle skipping by (st_dev,
st_ino) on the current path, dot entries skipped, and `literal` name quoting (LF printed as '?'). Out of contract
there: BLOCKSIZE / LS_BLOCK_SIZE / POSIXLY_CORRECT (they rescale `total`), TIME_STYLE, a non-C locale reaching
ls, ACL/SELinux mode suffixes, device nodes, and a cache line longer than 1 MiB.

Also out of contract: -h/--help, a FIFO named like a desktop file in a
later application dir (the script blocks reading it), symlink loops, an empty-string argument (the script loops forever), XDG dirs or HOME containing ':' inside a default, glob characters or a quote,
\\\\u/\\\\U escapes beyond ASCII in a delimiter, and file names with bytes the shell would see differently in another
locale. On these the tool prints `MADO_TERM_OUT_OF_CONTRACT: <reason>` on stderr and exits 2. HOME unset is IN
contract and modelled as the pin does it: a default that needs HOME ($XDG_CONFIG_HOME or $XDG_DATA_HOME or
$XDG_CACHE_HOME empty, x:148/166/172) makes the resolver exit 1 with empty stdout, while all of them set lets it
run normally."""

SELFTEST_HELPERS = '''

# ----------------------------------------------------------------- warm-cache selftest machinery
def _pin(root, ts=1546300800):
    """Freeze every mtime under root: the hash's date column then never moves with the wall clock."""
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        for nm in dirnames + filenames + ["."]:
            p = os.path.join(dirpath, nm)
            try:
                os.utime(p, (ts, ts), follow_symlinks=False)
            except OSError:
                pass


def _hash_for(env):
    """The hash this tree has, over the paths this environment builds (x:143-215)."""
    r = Resolver(env)
    r.desktops_lower = desktops(env)
    r.make_paths()
    return gen_hash(env.get("XDG_CURRENT_DESKTOP", ""), ":".join(r.configs), ":".join(r.app_dirs))


def _cache_text(env, **fields):
    """A cache file exactly as save_cache writes it (x:313-333), with individual fields overridden."""
    rec = {"hash": _hash_for(env), "cmd": "foot", "entry_path": None, "entry_id": "foot.desktop",
           "entry_action": "", "execarg": "-e", "appidarg": "", "titlearg": "", "dirarg": "",
           "holdarg": "", "exec_usep": "kitty" + USEP + "--warm"}
    rec["entry_path"] = os.path.join(env.get("XDG_DATA_DIRS") or env["XDG_DATA_HOME"],
                                     "applications", "foot.desktop")
    rec.update(fields)
    lines = [rec[k] for k in ("hash", "cmd", "entry_path", "entry_id", "entry_action", "execarg",
                              "appidarg", "titlearg", "dirarg", "holdarg")]
    return "".join(x + "\\n" for x in lines) + rec["exec_usep"] + RSEP + "END_OF_EXEC_USEP\\n"


def _no_terminator(env, **fields):
    return _cache_text(env, **fields).rsplit(RSEP, 1)[0]


def _terminator_on(env, line, **fields):
    """A cache whose command block reaches the terminator exactly on <line> (10 fields, so 11..line-1 empty)."""
    return _cache_text(env, exec_usep="\\n" * (line - 11) + "kitty" + USEP + "--warm", **fields)


def _warm_case(name, files, execs, args, want_out, want_rc, warm, **envkw):
    return (name, files, execs, args, want_out, want_rc, envkw, warm)


def selftest_warm_cases():
    """(name, files, execs, args, want_stdout, want_rc, env overrides, cache builder)."""
    cases = []
    A = "usr/share/applications/"
    L = "home/.config/xdg-terminals.list"
    entry = _term("foot")
    files = {A + "foot.desktop": entry, L: "foot.desktop\\n"}
    ex = ["bin/foot", "bin/kitty"]
    hit = "kitty\\n--warm\\n"
    cold = "foot\\n"
    P = "$ROOT/usr/share/applications/foot.desktop"

    cases.append(_warm_case("cache-hit-cmd", files, ex, ["--print-cmd"], hit, 0,
                            lambda env: _cache_text(env)))
    cases.append(_warm_case("cache-hit-beats-entry", dict(files), ex, ["--print-cmd"], hit, 0,
                            lambda env: (_pin(env["HOME"]), _cache_text(env))[1]))
    cases.append(_warm_case("cache-hit-id-path-action", files, ex, ["--print-id", "--print-path"],
                            "cached.desktop:act\\n" + P + ":act\\n", 0,
                            lambda env: _cache_text(env, entry_id="cached.desktop", entry_action="act")))
    cases.append(_warm_case("cache-stale-hash", files, ex, ["--print-cmd"], cold, 0,
                            lambda env: _cache_text(env, hash="0" * 32)))
    cases.append(_warm_case("cache-absent", files, ex, ["--print-cmd"], cold, 0, None))
    cases.append(_warm_case("cache-invalid-no-terminator", files, ex, ["--print-cmd"], cold, 0,
                            lambda env: _no_terminator(env)))
    cases.append(_warm_case("cache-invalid-line50", files, ex, ["--print-cmd"], cold, 0,
                            lambda env: _terminator_on(env, 50)))
    cases.append(_warm_case("cache-line49-is-valid", files, ex, ["--print-cmd"], hit, 0,
                            lambda env: _terminator_on(env, 49)))
    cases.append(_warm_case("cache-cmd-unresolved", files, ex, ["--print-cmd"], cold, 0,
                            lambda env: _cache_text(env, cmd="nosuchtool")))
    cases.append(_warm_case("cache-cmd-script-function", files, ex, ["--print-cmd"], hit, 0,
                            lambda env: _cache_text(env, cmd="gen_hash")))
    cases.append(_warm_case("cache-disabled-env", files, ex, ["--print-cmd"], cold, 0,
                            lambda env: _cache_text(env), **{"XTE_CACHE_ENABLED": "false"}))
    cases.append(_warm_case("cache-directive-disable-still-hits", {A + "foot.desktop": entry,
                                                                   L: "/disable_cache\\nfoot.desktop\\n"},
                            ex, ["--print-cmd"], hit, 0, lambda env: _cache_text(env)))
    cases.append(_warm_case("cache-content-missing-path", files, ex, ["--print-id", "--print-content"],
                            "foot.desktop\\n", 1,
                            lambda env: _cache_text(env, entry_path="/nonexistent/x.desktop")))
    cases.append(_warm_case("cache-content-hit", files, ex, ["--print-content"], entry, 0,
                            lambda env: _cache_text(env)))
    cases.append(_warm_case("cache-hit-newline-in-exec", files, ex, ["--print-cmd"],
                            "kitty\\na\\nb\\n", 0,
                            lambda env: _cache_text(env, exec_usep="kitty" + USEP + "a\\nb")))
    cases.append(_warm_case("cache-hit-skips-unreadable-list", files, ex, ["--print-cmd"], hit, 0,
                            lambda env: (_pin(env["HOME"]),
                                         os.chmod(os.path.join(env["HOME"], ".config/xdg-terminals.list"), 0o000),
                                         _cache_text(env))[2]))
    cases.append(_warm_case("cache-hit-args-from-entry-keys",
                            {A + "foot.desktop": _term("foot", "X-TerminalArgTitle=--title\\n"
                                                       "X-TerminalArgHold=--hold\\n"),
                             L: "foot.desktop\\n"}, ex,
                            ["--print-cmd", "--title=T", "--hold"],
                            "kitty\\n--warm\\n--title\\nT\\n--hold\\n", 0,
                            lambda env: _cache_text(env, titlearg="--title", holdarg="--hold")))
    cases.append(_warm_case("home-unset-default-needed", files, ex, ["--print-id"], "", 1, None,
                            **{"HOME": None, "XDG_CONFIG_HOME": None}))
    cases.append(_warm_case("home-unset-all-xdg-set", files, ex, ["--print-id"], "foot.desktop\\n", 0, None,
                            **{"HOME": None}))
    return cases
'''

SELFTEST_EXPLAIN = '''

def selftest_explain_cases():
    """(name, files, execs, env overrides, cache builder, want cache=, want verdict=, want rc)."""
    A = "usr/share/applications/"
    L = "home/.config/xdg-terminals.list"
    files = {A + "foot.desktop": _term("foot"), L: "foot.desktop\\n"}
    ex = ["bin/foot", "bin/kitty"]
    return [
        ("explain-cache-absent", files, ex, {}, None, "absent", "OK", 0),
        ("explain-cache-hit", files, ex, {}, lambda env: _cache_text(env), "hit", "OK", 0),
        ("explain-cache-stale", files, ex, {}, lambda env: _cache_text(env, hash="f" * 32), "stale", "OK", 0),
        ("explain-cache-invalid", files, ex, {}, lambda env: _no_terminator(env), "invalid", "OK", 0),
        ("explain-cache-disabled", files, ex, {"XTE_CACHE_ENABLED": "0"},
         lambda env: _cache_text(env), "disabled", "OK", 0),
        ("explain-no-terminal", {A + "x.desktop": "[Desktop Entry]\\n"}, [], {}, None, "absent",
         "NO_TERMINAL", 3),
    ]
'''

SELFTEST_LOOP_OLD = '''def selftest():
    base = tempfile.mkdtemp(prefix="mado-terminal-selftest.", dir=os.environ.get("TMPDIR") or None)
    cases = selftest_cases()
    passed = 0
    try:
        for i, (name, files, execs, args, want_out, want_rc, envkw) in enumerate(cases):
            root = os.path.join(base, "c%02d" % i)
            os.makedirs(root + "/home", exist_ok=True)
            os.makedirs(root + "/cache", exist_ok=True)
            _mk(root, files, execs)
            desk = envkw.pop("desk", "Hyprland")
            env = _env(root, desk, **envkw)
            try:
                got, rc, _err = run_print(env, args, cwd=root)
            except OutOfContract as ex:
                got, rc = "OOC:%s" % ex, 2
            want = want_out.replace("$ROOT", root)
            if got == want and rc == want_rc:
                passed += 1
            else:
                print("MADO_TERMINAL_SELFTEST_FAIL: %s got=%r rc=%d want=%r rc=%d" % (name, got, rc, want, want_rc))
    finally:
        import shutil
        shutil.rmtree(base, ignore_errors=True)
    print("MADO_TERMINAL_SELFTEST: %d/%d passed" % (passed, len(cases)))
    return 0 if passed == len(cases) else 1'''

SELFTEST_LOOP_NEW = '''def _env_for(root, envkw):
    envkw = dict(envkw)
    desk = envkw.pop("desk", "Hyprland")
    env = _env(root, desk, **{k: v for k, v in envkw.items() if v is not None})
    for k, v in envkw.items():
        if v is None:
            env.pop(k, None)
    return env


def selftest():
    base = tempfile.mkdtemp(prefix="mado-terminal-selftest.", dir=os.environ.get("TMPDIR") or None)
    cases = [(c[0], c[1], c[2], c[3], c[4], c[5], c[6], None) for c in selftest_cases()]
    cases += selftest_warm_cases()
    passed = 0
    fails = 0
    try:
        for i, (name, files, execs, args, want_out, want_rc, envkw, warm) in enumerate(cases):
            root = os.path.join(base, "c%02d" % i)
            os.makedirs(root + "/home", exist_ok=True)
            os.makedirs(root + "/cache", exist_ok=True)
            _mk(root, files, execs)
            env = _env_for(root, envkw)
            if warm is not None:
                _pin(root)
                text = warm(env)
                if text is not None:
                    with open(os.path.join(root, "cache", "xdg-terminal-exec"), "wb") as fh:
                        fh.write(text.encode("latin-1", "surrogateescape"))
            try:
                got, rc, _err = run_print(env, args, cwd=root)
            except OutOfContract as ex:
                got, rc = "OOC:%s" % ex, 2
            want = want_out.replace("$ROOT", root)
            if got == want and rc == want_rc:
                passed += 1
            else:
                fails += 1
                print("MADO_TERMINAL_SELFTEST_FAIL: %s got=%r rc=%d want=%r rc=%d" % (name, got, rc, want, want_rc))
        for name, files, execs, envkw, warm, want_cache, want_verdict, want_rc in selftest_explain_cases():
            root = os.path.join(base, "x%02d" % passed)
            os.makedirs(root + "/home", exist_ok=True)
            os.makedirs(root + "/cache", exist_ok=True)
            _mk(root, files, execs)
            env = _env_for(root, envkw)
            if warm is not None:
                _pin(root)
                with open(os.path.join(root, "cache", "xdg-terminal-exec"), "wb") as fh:
                    fh.write(warm(env).encode("latin-1", "surrogateescape"))
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = explain(env, None)
            line = [x for x in buf.getvalue().split("\\n") if x.startswith("MADO_TERM: ")]
            got = (line[-1] if line else "")
            parts = dict(kv.split("=", 1) for kv in got[len("MADO_TERM: "):].split() if "=" in kv)
            if parts.get("cache") == want_cache and parts.get("verdict") == want_verdict and rc == want_rc:
                passed += 1
            else:
                fails += 1
                print("MADO_TERMINAL_SELFTEST_FAIL: %s cache=%r verdict=%r rc=%d want cache=%r verdict=%r rc=%d"
                      % (name, parts.get("cache"), parts.get("verdict"), rc, want_cache, want_verdict, want_rc))
    finally:
        import shutil
        shutil.rmtree(base, ignore_errors=True)
    print("MADO_TERMINAL_SELFTEST: %d/%d passed" % (passed, passed + fails))
    return 0 if fails == 0 else 1'''


def replace_once(text, old, new, what):
    n = text.count(old)
    if n != 1:
        raise SystemExit("patch %s: anchor found %d times, not 1" % (what, n))
    return text.replace(old, new)


def main():
    src = open(BASE, "rb").read().decode("latin-1")
    mod = open(MODULE, "rb").read().decode("latin-1")
    idx = mod.index(REGION_START)
    region = mod[idx:]
    if not region.endswith("\n"):
        region += "\n"

    # 1. docstring: the cache is now in contract (sliced: the paragraph is long and backslash-heavy)
    i = src.index("Cache (out of contract):")
    j = src.index('\n"""\nimport fnmatch')
    src = src[:i] + DOC_CACHE_NEW + src[j:]
    src = replace_once(src, "for a cold cache (see \"Cache\" below).",
                       "for the cache the environment has (see \"Cache\" below).", "usage cold-cache")
    src = replace_once(src, "cache=<absent|present|disabled> verdict=",
                       "cache=<absent|hit|stale|invalid|disabled> verdict=", "docstring explain cache=")
    src = replace_once(src, """      A trace of the selection (every list file read, every candidate and why it was skipped), then one line""",
                       """      A trace of the selection (the cache verdict, every list file read, every candidate and why it was
      skipped), then one line""", "docstring explain trace")

    # 2. imports, and USEP moves into the inlined block
    src = replace_once(src, """import fnmatch
import os
import stat
import sys
import tempfile

USEP = "\\x1f"
SPACE""", """import fnmatch
import grp
import hashlib
import os
import pwd
import stat
import sys
import tempfile
import time

SPACE""", "imports")

    # 3. the inlined warm-cache block, then the new exception
    src = replace_once(src, "\nclass OutOfContract(Exception):\n",
                       "\n" + BEGIN + "\n" + region + END + "\n\n\nclass OutOfContract(Exception):\n",
                       "inlined region")
    src = replace_once(src, """class Exit(Exception):
    def __init__(self, rc):
        super().__init__(rc)
        self.rc = rc
""", """class Exit(Exception):
    def __init__(self, rc):
        super().__init__(rc)
        self.rc = rc


class HomeUnset(Exception):
    \"\"\"A default needed $HOME and the environment has none: the pin exits 1 with empty stdout.\"\"\"
""", "HomeUnset")

    # 4. desktops() helper + select()/make_paths warm path
    src = replace_once(src, """def check_bool(v, err):""", """def desktops(env):
    \"\"\"XDG_CURRENT_DESKTOP with ASCII upper case lowered, trailing newlines dropped (x:1144).\"\"\"
    dsk = env.get("XDG_CURRENT_DESKTOP", "")
    return split_ifs("".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in dsk).rstrip("\\n"), ":")


def check_bool(v, err):""", "desktops helper")

    src = replace_once(src, """    def make_paths(self):
        e = self.env
        if "HOME" not in e:
            raise OutOfContract("HOME unset")
        for k in ("XDG_CONFIG_HOME", "XDG_CONFIG_DIRS", "XDG_DATA_HOME", "XDG_DATA_DIRS"):
            v = e.get(k, "")
            if any(c in v for c in "[]*?\\\\'\\""):
                raise OutOfContract("%s holds a glob character or a quote" % k)
        home = e["HOME"]
        if any(c in home for c in ":[]*?\\\\'\\""):
            raise OutOfContract("HOME holds ':' a glob character or a quote")
        cfg = (e.get("XDG_CONFIG_HOME") or home + "/.config") + ":" + (e.get("XDG_CONFIG_DIRS") or "/etc/xdg")
        data = e.get("XDG_DATA_DIRS") or "/usr/local/share:/usr/share\"""",
                       """    def _xdg(self, key, default):
        \"\"\"${KEY:-<HOME>default}: HOME is needed only when the default is (x:148,166,172).\"\"\"
        v = self.env.get(key)
        if v:
            return v
        if "HOME" not in self.env:
            raise HomeUnset("HOME: unbound variable (x:%d, exit 1, empty stdout)"
                            % {"XDG_CONFIG_HOME": 148, "XDG_DATA_HOME": 166, "XDG_CACHE_HOME": 172}[key])
        return self.env["HOME"] + default

    def make_paths(self):
        e = self.env
        for k in ("XDG_CONFIG_HOME", "XDG_CONFIG_DIRS", "XDG_DATA_HOME", "XDG_DATA_DIRS"):
            v = e.get(k, "")
            if any(c in v for c in "[]*?\\\\'\\""):
                raise OutOfContract("%s holds a glob character or a quote" % k)
        if "HOME" in e and any(c in e["HOME"] for c in ":[]*?\\\\'\\""):
            raise OutOfContract("HOME holds ':' a glob character or a quote")
        cfg = self._xdg("XDG_CONFIG_HOME", "/.config") + ":" + (e.get("XDG_CONFIG_DIRS") or "/etc/xdg")
        data = e.get("XDG_DATA_DIRS") or "/usr/local/share:/usr/share\"""", "make_paths head")

    src = replace_once(src, """        for d in split_ifs((e.get("XDG_DATA_HOME") or home + "/.local/share") + ":" + data, ":"):
            d = d[:-1] if d.endswith("/") else d
            apps.insert(0, d + "/applications/")
        self.app_dirs = apps""",
                       """        for d in split_ifs(self._xdg("XDG_DATA_HOME", "/.local/share") + ":" + data, ":"):
            d = d[:-1] if d.endswith("/") else d
            apps.insert(0, d + "/applications/")
        self.app_dirs = apps
        self.cache_file = self._xdg("XDG_CACHE_HOME", "/.cache") + "/xdg-terminal-exec"

    def load_cache(self):
        \"\"\"x:217-298 as a resolver step: True on a hit (the cached values are adopted), else sets cache_state.\"\"\"
        try:
            rec, reason = read_cache(self.cache_file)
        except WarmOutOfContract as ex:
            raise OutOfContract(str(ex))
        if rec is None:
            self.cache_state = reason
            self.t("cache %s: %s, cold path" % (self.cache_file, reason))
            return False
        fresh = gen_hash(self.env.get("XDG_CURRENT_DESKTOP", ""), ":".join(self.configs),
                         ":".join(self.app_dirs))
        if rec.hash != fresh:
            self.cache_state = "stale"
            self.t("cache %s: out-of-date (line 1 md5 %s, this tree hashes to %s)" %
                   (self.cache_file, rec.hash, fresh))
            return False
        if not self.command_v(rec.cmd):
            self.cache_state = "stale"
            self.t("cache %s: out-of-date (cached command %r does not resolve)" % (self.cache_file, rec.cmd))
            return False
        self.cache_state = "hit"
        self.exec_usep = rec.exec_usep
        self.entry_path, self.entry_id, self.entry_action = rec.entry_path, rec.entry_id, rec.entry_action
        self.execarg, self.appidarg, self.titlearg = rec.execarg, rec.appidarg, rec.titlearg
        self.dirarg, self.holdarg = rec.dirarg, rec.holdarg
        self.is_terminal = True
        self.t("cache %s: hit, entry %s, command %r, %d exec word(s)" %
               (self.cache_file, rec.entry_id, rec.cmd, len(split_ifs(rec.exec_usep, USEP))))
        return True""", "make_paths tail + load_cache")

    src = replace_once(src, """    def select(self):
        e = self.env
        dsk = e.get("XDG_CURRENT_DESKTOP", "")
        low = "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in dsk).rstrip("\\n")
        self.desktops_lower = split_ifs(low, ":")""", """    def select(self):
        e = self.env
        self.desktops_lower = desktops(e)""", "select desktops")

    src = replace_once(src, """        self.reset_keys()
        self.make_paths()
        cache_home = e.get("XDG_CACHE_HOME") or e["HOME"] + "/.cache"
        self.cache_file = cache_home + "/xdg-terminal-exec"
        self.read_config_paths()
        self.find_entry_paths()
        return self.find_entry()""", """        self.cache_used = False
        self.cache_state = None
        self.reset_keys()
        self.make_paths()
        if not check_bool(self.cache_enabled, self.err):
            self.cache_state = "disabled"
            self.t("cache %s: disabled by XTE_CACHE_ENABLED=%r, cold path" % (self.cache_file, self.cache_enabled))
        elif self.load_cache():
            self.cache_used = True
            return True
        self.read_config_paths()
        self.find_entry_paths()
        return self.find_entry()""", "select warm gate")

    # 5. run_print: HOME unset, and --print-content on a path that vanished
    src = replace_once(src, """    try:
        if not r.select():
            return "", 1, r.stderr
    except Exit as ex:
        return "", ex.rc, r.stderr""", """    try:
        if not r.select():
            return "", 1, r.stderr
    except Exit as ex:
        return "", ex.rc, r.stderr
    except HomeUnset as ex:
        return "", 1, [str(ex)]""", "run_print HomeUnset")

    src = replace_once(src, """        try:
            text = read_file(r.entry_path)
        except OSError:
            text = ""
        for line in read_lines(text, False):""", """        try:
            text = read_file(r.entry_path)
        except IsADirectoryError:
            text = ""       # `shcat < dir`: the redirection opens, every `read` fails, shcat returns 0 (x:1362)
        except OSError as ex:
            # `shcat < "${XTE__ENTRY_PATH}"` (x:1362): a failed redirection ends the script under `set -e`
            return "".join(out), 1, r.stderr + ["%s: %s" % (r.entry_path, ex.strerror or "cannot read")]
        for line in read_lines(text, False):""", "print-content failure")

    # 6. explain: the cache verdict
    src = replace_once(src, """    r = Resolver(env)
    cache = "disabled"
    try:
        ok = r.select()
    except Exit:
        ok = False""", """    r = Resolver(env)
    try:
        ok = r.select()
    except Exit:
        ok = False
    except HomeUnset as ex:
        ok = False
        r.t("make_paths: %s, the resolver exits 1 with empty stdout" % ex)""", "explain select")
    src = replace_once(src, """    if check_bool(r.cache_enabled, lambda _m: None):
        cache = "present" if os.path.isfile(r.cache_file) else "absent\"""", """    if r.cache_state is not None:
        cache = r.cache_state
    elif not check_bool(r.cache_enabled, lambda _m: None):
        cache = "disabled"
    else:
        cache = "absent\"""", "explain cache=")

    # 7. selftest machinery
    src = replace_once(src, "\n\ndef selftest():\n", SELFTEST_HELPERS + "\n\ndef selftest():\n",
                       "selftest helpers")
    src = replace_once(src, SELFTEST_LOOP_OLD, SELFTEST_LOOP_NEW + SELFTEST_EXPLAIN, "selftest loop")

    # 8. stdout encoding must carry both the latin-1 file convention and surrogateescape paths
    src = replace_once(src, 'sys.stdout.buffer.write(out.encode("latin-1"))',
                       'sys.stdout.buffer.write(out.encode("latin-1", "surrogateescape"))', "stdout encode")

    with open(OUT, "wb") as fh:
        fh.write(src.encode("latin-1"))
    print("wrote %s (%d bytes, sha256 %s)" % (OUT, len(src), hashlib.sha256(src.encode("latin-1")).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
