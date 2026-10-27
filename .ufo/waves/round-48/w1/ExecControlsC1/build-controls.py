#!/usr/bin/env python3
"""build-controls.py - materialize the C1 control tools (round 48, wave w1, seat ExecControlsC1).

Every control in controls/ is a FULL tools/mado-terminal.py variant, produced by patching one source of truth:

  base       = tools/mado-terminal.py at the lane's round-47 tip (git blob, sha256 printed): the landed
               read-only tool, which models a COLD cache only and declares the resolver's cache out of contract.
  reference  = base + the warm-cache path of xdg-terminal-exec v0.14.3 (script x:N = line N of
               .ufo/waves/round-47/fetch/xdg-terminal-exec, sha256 89f2be9a...27ac): read_cache (x:217-298),
               gen_hash (x:179-215) over a byte-exact model of this host's `LC_ALL=C LANG=C ls -LRl`, and the
               warm print modes. No process, no socket, no write.
  controls   = reference with ONE rule undone, or base with one cheap shortcut.

Each patch is a list of (old, new) pairs applied to the reference/base text; every `old` must occur exactly once
or the build fails. The patch set is therefore the machine-readable statement of what each control gets wrong.

usage: build-controls.py [--base PATH] [--out DIR]
"""
import argparse
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.realpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
BASE_REV = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
BASE_TOOL = "tools/mado-terminal.py"

# ------------------------------------------------------------------------------------------------ reference pieces
CACHE_MODULE = '''
# ------------------------------------------------------------------------------------------------ warm cache
# The resolver reads $XDG_CACHE_HOME/xdg-terminal-exec before any list or entry (x:1179) and trusts it while
# gen_hash (x:179-215) still matches and the cached command resolves (x:285-298). gen_hash is the md5 of
#   "4\\n" + XDG_CURRENT_DESKTOP + "\\n" + `LC_ALL=C LANG=C ls -LRl` of the ':'-split list and data paths,
# stderr dropped, so the cache verdict needs that ls's exact stdout. The model below was calibrated against the
# binary the resolver itself calls inside the counter's allowlist root - /usr/bin/ls, GNU coreutils 9.12 (the
# counter copies `shutil.which("ls", path="/usr/bin")` to /oracle/bin; an interactive shell on this host resolves a
# different `ls`), with no /etc (numeric uid/gid) and no TZ (UTC dates): byte-ordered names, a file block whose
# columns are sized over every stat'ed operand. No process is started and no file is written.
CACHE_RSEP = "\\x1e"
CACHE_TERMINATOR = CACHE_RSEP + "END_OF_EXEC_USEP"
CACHE_LINE_LIMIT = 50                     # x:222,232-235
CACHE_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
CACHE_SIX_MONTHS = 15778476               # GNU ls's recent window: age < 15778476 s and not in the future


def _ls_mode_string(mode):
    if stat.S_ISDIR(mode):
        c = "d"
    elif stat.S_ISLNK(mode):
        c = "l"
    elif stat.S_ISFIFO(mode):
        c = "p"
    elif stat.S_ISSOCK(mode):
        c = "s"
    elif stat.S_ISCHR(mode):
        c = "c"
    elif stat.S_ISBLK(mode):
        c = "b"
    elif stat.S_ISREG(mode):
        c = "-"
    else:
        c = "?"
    out = [c]
    for bit, ch in ((0o400, "r"), (0o200, "w"), (0o100, "x"), (0o040, "r"), (0o020, "w"), (0o010, "x"),
                    (0o004, "r"), (0o002, "w"), (0o001, "x")):
        out.append(ch if mode & bit else "-")
    if mode & 0o4000:
        out[3] = "s" if mode & 0o100 else "S"
    if mode & 0o2000:
        out[6] = "s" if mode & 0o010 else "S"
    if mode & 0o1000:
        out[9] = "t" if mode & 0o001 else "T"
    return "".join(out)


def _ls_date(mtime, now):
    tm = time.gmtime(mtime)
    mon = CACHE_MONTHS[tm.tm_mon - 1]
    if 0 <= now - mtime < CACHE_SIX_MONTHS:
        return "%s %2d %02d:%02d" % (mon, tm.tm_mday, tm.tm_hour, tm.tm_min)
    return "%s %2d  %4d" % (mon, tm.tm_mday, tm.tm_year)


def _ls_text(raw):
    return raw.replace(b"\\n", b"?").decode("latin-1")


class _LsRow:
    __slots__ = ("mode", "nlink", "owner", "group", "size", "date", "name", "key", "blocks", "known")

    def __init__(self, mode, nlink, owner, group, size, date, name, key, blocks, known):
        self.mode, self.nlink, self.owner, self.group = mode, nlink, owner, group
        self.size, self.date, self.name, self.key, self.blocks, self.known = size, date, name, key, blocks, known


def _ls_row(st, key, now):
    return _LsRow(_ls_mode_string(st.st_mode), str(st.st_nlink), str(st.st_uid), str(st.st_gid),
                  str(st.st_size), _ls_date(st.st_mtime, now), _ls_text(key), key, st.st_blocks, True)


def _ls_unknown(key):
    return _LsRow("l?????????", "?", "?", "?", "?", "?", _ls_text(key), key, 0, False)


def _ls_render(rows, widths=None):
    if not rows:
        return ""
    widths = rows if widths is None else widths
    w_n = max(len(r.nlink) for r in widths)
    w_o = max(len(r.owner) for r in widths)
    w_g = max(len(r.group) for r in widths)
    w_s = max(len(r.size) for r in widths)
    out = []
    for r in rows:
        if r.known:
            owner, group = r.owner.rjust(w_o), r.group.rjust(w_g)
        else:
            owner, group = r.owner.ljust(w_o), r.group.ljust(w_g)
        out.append("%s %s %s %s %s %s %s\\n" % (r.mode, r.nlink.rjust(w_n), owner, group,
                                               r.size.rjust(w_s), r.date.rjust(12), r.name))
    return "".join(out)


def _ls_total(rows):
    return "%d" % ((sum(r.blocks for r in rows) + 1) // 2)


def _ls_entries(path):
    names = []
    with os.scandir(os.fsencode(path)) as it:
        for de in it:
            names.append(de.name if isinstance(de.name, bytes) else os.fsencode(de.name))
    names.sort()
    return names


def _ls_lRl(operands, now=None):
    """stdout of `ls -LRl <operands>`: gen_hash drops stderr and the exit status."""
    now = time.time() if now is None else now
    files, dirs = [], []
    for p in operands:
        try:
            st = os.stat(p)
        except OSError:
            continue                            # missing or dangling operand (-L): stderr only, no row at all
        (dirs if stat.S_ISDIR(st.st_mode) else files).append(_ls_row(st, os.fsencode(p), now))
    files.sort(key=lambda r: r.key)
    dirs.sort(key=lambda r: r.key)
    blocks = []
    if files:
        blocks.append(_ls_render(files, files + dirs))
    for d in dirs:
        blocks.extend(_ls_walk(d.key, _ls_text(d.key), 0, now))
    return "\\n".join(blocks)


def _ls_walk(path, header, depth, now):
    """`path` stays bytes (a name is bytes and ls prints them back), `header` is its latin-1 text."""
    if depth > 64:
        raise OutOfContract("a symlink loop below %s (ls -LRl would run to the path limit)" % header)
    try:
        names = _ls_entries(path)
    except OSError:
        return []                               # unreadable: no header at all, stderr only
    rows, subdirs = [], []
    for nb in names:
        try:
            st = os.stat(os.path.join(path, nb))
        except OSError:
            rows.append(_ls_unknown(nb))
            continue
        rows.append(_ls_row(st, nb, now))
        if stat.S_ISDIR(st.st_mode):
            subdirs.append(nb)
    out = ["%s:\\n" % header + "total %s\\n" % _ls_total(rows) + _ls_render(rows)]
    for nb in subdirs:
        out.extend(_ls_walk(path.rstrip(b"/") + b"/" + nb,
                            header.rstrip("/") + "/" + _ls_text(nb), depth + 1, now))
    return out

'''

CACHE_METHODS = '''
    # ---------------------------------------------------------------- cache (x:179-298)
    def gen_hash(self):
        """gen_hash (x:179-215): md5 of the version line, XDG_CURRENT_DESKTOP and `ls -LRl` of every path."""
        text = "4\\n" + self.env.get("XDG_CURRENT_DESKTOP", "") + "\\n"
        listing = _ls_lRl(list(self.configs) + list(self.app_dirs))
        return hashlib.md5((text + listing).encode("latin-1")).hexdigest()

    def read_cache(self):
        """read_cache (x:217-298): absent / invalid / stale / hit; a hit applies the cached fields."""
        try:
            with open(self.cache_file, "rb") as fh:
                data = fh.read().decode("latin-1")
        except OSError:
            return "absent"
        fields = [""] * 10
        exec_usep = ""
        finished = False
        for num, line in enumerate(read_lines(data, False), 1):
            if num <= 10:
                fields[num - 1] = line
                continue
            if num == CACHE_LINE_LIMIT:
                return "invalid"                # x:232-235: the limit line ends the read before any terminator
            exec_usep += ("\\n" if exec_usep else "") + line
            if line.endswith(CACHE_TERMINATOR):
                exec_usep = exec_usep[:-len(CACHE_TERMINATOR)]
                finished = True
                break
        if not finished:
            return "invalid"
        if self.gen_hash() != fields[0] or not self.command_v(fields[1]):
            return "stale"                      # x:285-298: the hash, then `command -v <cached cmd>`
        self.exec_usep = exec_usep
        (self.entry_path, self.entry_id, self.entry_action, self.execarg, self.appidarg,
         self.titlearg, self.dirarg, self.holdarg) = fields[2:10]
        return "hit"

'''

REF_DOCSTRING = r'''Cache: the resolver reads $XDG_CACHE_HOME/xdg-terminal-exec (default $HOME/.cache) BEFORE any list or entry
(x:1179) and uses its entry, arguments and command while an md5 of XDG_CURRENT_DESKTOP and `ls -LRl` of every list
and application path is unchanged and the cached command resolves (x:217-298); a cold run that reaches the print-cmd
or launch point rewrites it in the background (x:1455-1458). This tool models that cache as the environment presents
it - hit, stale, invalid (no terminator, line limit) or disabled (XTE_CACHE_ENABLED=false; a /disable_cache line in a
list file only suppresses the save, never the read) - and prints
what the resolver prints in each case; it never writes the cache the resolver would save. Also out of contract:
-h/--help, a FIFO named like a desktop file in a
later application dir (the script blocks reading it), symlink loops, an empty-string argument (the script loops forever), XDG dirs or HOME containing ':' inside a default, glob characters or a quote,
\\u/\\U escapes beyond ASCII in a delimiter, and file names with bytes the shell would see differently in another
locale. On these the tool prints `MADO_TERM_OUT_OF_CONTRACT: <reason>` on stderr and exits 2.'''

HOME_D1_OLD = ('        e = self.env\n        if "HOME" not in e:\n'
               '            raise OutOfContract("HOME unset")\n')
HOME_D1_NEW = ('        e = self.env\n        if "HOME" not in e:\n'
               '            for k in ("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME"):\n'
               '                if not e.get(k):\n'
               '                    raise Exit(1)      # `${HOME}` unbound under set -u: exit 1, no stdout (D1)\n')


def patch(src, pairs, name):
    for old, new in pairs:
        n = src.count(old)
        if n != 1:
            raise SystemExit("%s: anchor occurs %d times, not 1: %r" % (name, n, old[:70]))
        src = src.replace(old, new, 1)
    return src


def reference_patch(base):
    """base -> reference: the warm-cache path."""
    s = base
    old_usage = ('      Prints exactly what `xdg-terminal-exec` prints on stdout for the same options and arguments in the same\n'
                 '      environment, and exits with its exit status, for a cold cache (see "Cache" below). At least one of\n')
    new_usage = ('      Prints exactly what `xdg-terminal-exec` prints on stdout for the same options and arguments in the same\n'
                 '      environment, and exits with its exit status, for the cache state the environment presents ("Cache"\n'
                 '      below). At least one of\n')
    i = s.index("Cache (out of contract):")
    j = s.index("exits 2.\n", i) + len("exits 2.")
    s = s[:i] + REF_DOCSTRING + s[j:]
    return patch(s, [
        (old_usage, new_usage),
        ("cache=<absent|present|disabled> verdict=<V>", "cache=<absent|hit|stale|invalid|disabled> verdict=<V>"),
        ("import fnmatch\nimport os\nimport stat\nimport sys\nimport tempfile\n",
         "import fnmatch\nimport hashlib\nimport os\nimport stat\nimport sys\nimport tempfile\nimport time\n"),
        # the module-level ls model + the cache methods
        ("class Resolver:\n", CACHE_MODULE.strip("\n") + "\n\n\nclass Resolver:\n"),
        ("    def select(self):\n", CACHE_METHODS + "    def select(self):\n"),
        (HOME_D1_OLD, HOME_D1_NEW),
        # select: read the cache first, then the cold path
        ('        cache_home = e.get("XDG_CACHE_HOME") or e["HOME"] + "/.cache"\n'
         '        self.cache_file = cache_home + "/xdg-terminal-exec"\n'
         '        self.read_config_paths()\n'
         '        self.find_entry_paths()\n'
         '        return self.find_entry()\n',
         '        cache_home = e.get("XDG_CACHE_HOME") or (e.get("HOME", "") + "/.cache")\n'
         '        self.cache_file = cache_home + "/xdg-terminal-exec"\n'
         '        self.cache_used = False\n'
         '        self.cache_state = "absent"     # a run that dies before the gate (HOME unset) reaches no cache\n'
         '        if check_bool(self.cache_enabled, self.err):\n'
         '            self.cache_state = self.read_cache()\n'
         '            self.t("cache %s: %s" % (self.cache_file, self.cache_state))\n'
         '            if self.cache_state == "hit":\n'
         '                self.cache_used = True\n'
         '                return True\n'
         '        else:\n'
         '            self.cache_state = "disabled"\n'
         '        self.read_config_paths()\n'
         '        self.find_entry_paths()\n'
         '        return self.find_entry()\n'),
        # print-content on a hit reads the CACHED path; `shcat < missing` fails and `set -e` ends the run
        ('        try:\n            text = read_file(r.entry_path)\n        except OSError:\n            text = ""\n',
         '        try:\n            text = read_file(r.entry_path)\n        except OSError:\n'
         '            if r.cache_used:\n'
         '                return "".join(out), 1, r.stderr     # `shcat < path` fails under `set -e`\n'
         '            text = ""\n'),
        # explain reports the verdict this run reached
        ('    if check_bool(r.cache_enabled, lambda _m: None):\n'
         '        cache = "present" if os.path.isfile(r.cache_file) else "absent"\n',
         '    cache = getattr(r, "cache_state", "absent")\n'),
    ], "reference")


# ------------------------------------------------------------------------------------------------ controls
# Each entry: (name, source, [(old, new), ...], what the control gets wrong, the clause that must catch it).
CONTROLS = [
    ("base", "base", [], "cold cache only: the cache file stays outside its contract", "f (warm fixtures)"),
    ("trust-any", "reference", [
        ('        if self.gen_hash() != fields[0] or not self.command_v(fields[1]):\n',
         '        if not self.command_v(fields[1]):\n'),
    ], "trusts any well-formed cache whose line 2 resolves, no hash", "f (invalidated caches)"),
    ("hash-names", "reference", [
        ('        listing = _ls_lRl(list(self.configs) + list(self.app_dirs))\n',
         '        listing = _ls_names_only(list(self.configs) + list(self.app_dirs))\n'),
        ('def _ls_lRl(operands, now=None):',
         'def _ls_names_only(operands):\n'
         '    """names only: no columns, sizes, modes or dates"""\n'
         '    out = []\n'
         '    for p in operands:\n'
         '        out.append(p)\n'
         '        try:\n'
         '            out.extend(_ls_text(x) for x in _ls_entries(p))\n'
         '        except OSError:\n'
         '            continue\n'
         '    return "".join("%s\\n" % x for x in out)\n\n\ndef _ls_lRl(operands, now=None):'),
    ], "hash over path and entry names only, no ls -l columns", "f (any warm fixture)"),
    ("hash-no-date", "reference", [
        ('        out.append("%s %s %s %s %s %s %s\\n" % (r.mode, r.nlink.rjust(w_n), owner, group,\n'
         '                                               r.size.rjust(w_s), r.date.rjust(12), r.name))\n',
         '        out.append("%s %s %s %s %s %s\\n" % (r.mode, r.nlink.rjust(w_n), owner, group,\n'
         '                                              r.size.rjust(w_s), r.name))\n'),
    ], "ls -l model without the date column", "f (any warm fixture)"),
    ("hash-no-total", "reference", [
        ('    out = ["%s:\\n" % header + "total %s\\n" % _ls_total(rows) + _ls_render(rows)]\n',
         '    out = ["%s:\\n" % header + _ls_render(rows)]\n'),
    ], "ls -l model without the `total N` lines", "f (any warm fixture)"),
    ("always-cold-but-home", "base", [
        (HOME_D1_OLD, HOME_D1_NEW),
    ], "cold only (the cache is never read), but HOME unset is modelled as the pin does", "f (warm fixtures)"),
    ("cache-ignores-enable", "reference", [
        ('        if check_bool(self.cache_enabled, self.err):\n'
         '            self.cache_state = self.read_cache()\n',
         '        if True:\n'
         '            self.cache_state = self.read_cache()\n'),
    ], "reads the cache even when XTE_CACHE_ENABLED is false", "f (disabled fixtures)"),
    ("no-line-limit", "reference", [
        ('            if num == CACHE_LINE_LIMIT:\n'
         '                return "invalid"                # x:232-235: the limit line ends the read before any terminator\n',
         ''),
    ], "no 50-line limit on the cache file", "f (malformed caches)"),
    ("delegate-ls", "reference", [
        ('        listing = _ls_lRl(list(self.configs) + list(self.app_dirs))\n',
         '        listing = _ls_subprocess(list(self.configs) + list(self.app_dirs))\n'),
        ('def _ls_lRl(operands, now=None):',
         'def _ls_subprocess(operands):\n'
         '    """the shortcut: let the real ls do it (a process; the tool promised none)"""\n'
         '    import subprocess\n'
         '    env = dict(os.environ)\n'
         '    env["LC_ALL"] = "C"\n'
         '    env["LANG"] = "C"\n'
         '    return subprocess.run(["ls", "-LRl"] + list(operands), capture_output=True, env=env).stdout.decode("latin-1")\n\n\n'
         'def _ls_lRl(operands, now=None):'),
    ], "delegates gen_hash to ls through PATH (a process)", "r (execve tripwire)"),
    ("md5-subproc", "reference", [
        ('        return hashlib.md5((text + listing).encode("latin-1")).hexdigest()\n',
         '        import subprocess\n'
         '        return subprocess.run(["md5sum"], input=(text + listing).encode("latin-1"),\n'
         '                              capture_output=True).stdout.decode("latin-1").split(" ", 1)[0]\n'),
    ], "emulates ls but pipes the hash input to md5sum (a process)", "r (execve tripwire)"),
    ("explain-cache-const", "reference", [
        ('    cache = getattr(r, "cache_state", "absent")\n',
         '    cache = "hit" if check_bool(r.cache_enabled, lambda _m: None) else "disabled"\n'),
    ], "explain always says cache=hit when caching is on", "x (cache= compared)"),
    ("explain-cmd-const", "reference", [
        ('    print("MADO_TERM: selected=%s path=%s cmd=%s cache=%s verdict=%s" % (sel, path, argv0, cache, verdict))\n',
         '    print("MADO_TERM: selected=%s path=%s cmd=%s cache=%s verdict=%s" % (sel, path, "-", cache, verdict))\n'),
    ], "explain never names the command (cmd=-)", "x (cmd= compared)"),
    ("writes-cache", "reference", [
        ('        self.find_entry_paths()\n'
         '        return self.find_entry()\n',
         '        self.find_entry_paths()\n'
         '        ok = self.find_entry()\n'
         '        if self.cache_used or not ok:\n'
         '            return ok\n'
         '        self._save_cache()\n'
         '        return ok\n'),
        ('    def read_cache(self):',
         '    def _save_cache(self):\n'
         '        """save_cache (x:300-340) reproduced: the tool writes the cache a cold run would leave."""\n'
         '        if not check_bool(self.cache_enabled, lambda _m: None):\n'
         '            try:\n'
         '                os.unlink(self.cache_file)\n'
         '            except OSError:\n'
         '                pass\n'
         '            return\n'
         '        h = self.gen_hash()\n'
         '        cmd = split_ifs(self.exec_usep, USEP)[0] if self.exec_usep else ""\n'
         '        lines = [h, cmd, self.entry_path, self.entry_id, self.entry_action, self.execarg,\n'
         '                 self.appidarg, self.titlearg, self.dirarg, self.holdarg,\n'
         '                 self.exec_usep + CACHE_TERMINATOR]\n'
         '        try:\n'
         '            os.makedirs(os.path.dirname(self.cache_file) or ".", exist_ok=True)\n'
         '            with open(self.cache_file, "w", encoding="latin-1") as fh:\n'
         '                fh.write("".join(x + "\\n" for x in lines))\n'
         '        except OSError:\n'
         '            pass\n\n'
         '    def read_cache(self):'),
    ], "models save_cache too: writes the cache file (the contract: the tool writes nothing)", "no clause (gap)"),
    # one-rule-undone mutants of the reference draft
    ("mut-desktop-lower", "reference", [
        ('        text = "4\\n" + self.env.get("XDG_CURRENT_DESKTOP", "") + "\\n"\n',
         '        text = "4\\n" + ":".join(self.desktops_lower) + "\\n"\n'),
    ], "hashes the lowercased desktop list instead of XDG_CURRENT_DESKTOP", "f (desktops with upper case)"),
    ("mut-no-command-v", "reference", [
        ('        if self.gen_hash() != fields[0] or not self.command_v(fields[1]):\n',
         '        if self.gen_hash() != fields[0]:\n'),
    ], "trusts a hash-matching cache whose cached command no longer resolves", "f (exec[0] removed)"),
    ("mut-cache-fallback", "reference", [
        ('            if self.cache_state == "hit":\n'
         '                self.cache_used = True\n'
         '                return True\n'
         '        else:\n'
         '            self.cache_state = "disabled"\n'
         '        self.read_config_paths()\n'
         '        self.find_entry_paths()\n'
         '        return self.find_entry()\n',
         '        else:\n'
         '            self.cache_state = "disabled"\n'
         '        self.read_config_paths()\n'
         '        self.find_entry_paths()\n'
         '        ok = self.find_entry()\n'
         '        if not ok and self.cache_state == "hit":\n'
         '            self.cache_used = True\n'
         '            return True\n'
         '        return ok\n'),
    ], "uses a cache hit only as a fallback after the cold selection fails", "f (every warm hit)"),
    ("mut-eof-terminator", "reference", [
        ('        if not finished:\n            return "invalid"\n',
         '        finished = True                     # the file ended, so the cached command ended\n'),
    ], "accepts a cache with no terminator line at all", "f (malformed caches)"),
    ("mut-terminator-contains", "reference", [
        ('            if line.endswith(CACHE_TERMINATOR):\n',
         '            if CACHE_TERMINATOR in line:\n'),
    ], "accepts a terminator anywhere on the line instead of at its end", "f (malformed caches)"),
    ("mut-warm-ignores-args", "reference", [
        ('    for val, arg in ((dirv, r.dirarg), (title, r.titlearg), (appid, r.appidarg)):\n',
         '    for val, arg in (() if r.cache_used else ((dirv, r.dirarg), (title, r.titlearg), (appid, r.appidarg))):\n'),
    ], "on a cache hit the command line's --dir/--title/--app-id values are dropped", "f (changed --dir/--title over a hit)"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=None)
    ap.add_argument("--out", default=os.path.join(HERE, "controls"))
    a = ap.parse_args()
    if a.base:
        base = open(a.base, "rb").read().decode("latin-1")
        origin = a.base
    else:
        p = subprocess.run(["git", "-C", LANE, "show", BASE_REV + ":" + BASE_TOOL], capture_output=True)
        if p.returncode:
            raise SystemExit("cannot read %s@%s: %s" % (BASE_TOOL, BASE_REV[:12], p.stderr.decode()))
        base = p.stdout.decode("latin-1")
        origin = "%s@%s" % (BASE_TOOL, BASE_REV[:12])
    base_sha = hashlib.sha256(base.encode("latin-1")).hexdigest()
    ref = reference_patch(base)
    os.makedirs(a.out, exist_ok=True)
    made = []
    for name, src, pairs, wrong, clause in CONTROLS:
        text = patch(dict(base=base, reference=ref)[src], pairs, name)
        text = text.replace('"""mado-terminal.py - which terminal',
                            '"""CONTROL %s - %s. See .ufo/waves/round-48/w1/ExecControlsC1.md (clause: %s).\n'
                            'mado-terminal.py - which terminal' % (name, wrong, clause), 1)
        with open(os.path.join(a.out, name + ".py"), "wb") as fh:
            fh.write(text.encode("latin-1"))
        made.append((name, src, wrong, clause, hashlib.sha256(text.encode("latin-1")).hexdigest()))
    with open(os.path.join(a.out, "reference.py"), "wb") as fh:
        fh.write(ref.encode("latin-1"))
    print("base source: %s sha256 %s" % (origin, base_sha))
    print("reference: controls/reference.py sha256 %s" % hashlib.sha256(ref.encode("latin-1")).hexdigest())
    for name, src, wrong, clause, sha in made:
        print("%-22s %-9s %-16s %s  %s" % (name, src, clause, sha[:16], wrong))
    return 0


if __name__ == "__main__":
    sys.exit(main())
