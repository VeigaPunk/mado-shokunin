#!/usr/bin/env python3
"""mado-terminal.py -- read-only model of the xdg-terminal-exec v0.14.3 selection.

Modelled program: /usr/bin/xdg-terminal-exec
  sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac
  upstream tag v0.14.3 (Vladimir-csp/xdg-terminal-exec), byte-equal to the host copy.

The tool answers "which terminal does SUPER+RETURN launch, and why" without
starting a process and without opening a socket.  The resolver's external
helpers (tr, find, awk) are modelled in-process, the md5 cache is modelled as
cold (the resolver's own cache is out of contract), and nothing is written.

Commands
  print   [args]             stdout bytes + exit status of a --print-*/--test run
  explain [--observed FILE]  candidate trace + MADO_TERM verdict line
  --selftest                 hermetic self-check, fixtures built under $TMPDIR

Exit status of `explain`: 0 = OK/AGREE, 1 = DIFFER, 3 = NO_TERMINAL, 2 = usage.
`print` never launches a terminal: a run with no --print-*/--test option is a
usage error (exit 2), because the resolver would exec a terminal there.
"""

import os
import re
import sys
import tempfile
import shutil

PIN_SHA256 = '89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac'
SELF_NAME = 'xdg-terminal-exec'      # $0 basename of the modelled program

# ---------------------------------------------------------------------------
# shell-level constants
# ---------------------------------------------------------------------------

IFS_WS = ' \t'                       # what `read` strips with the default IFS
TOK_SPECIAL = set(' \t\n\r\v\f"`$\\\'><~|&;*?#()')
ALNUM_US = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
ALNUM_DASH = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-')
ID_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-')
ACTION_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-')

# `command -v` resolves shell keywords, builtins, functions and aliases before
# it looks at $PATH.  Bash 5.3 (`/bin/sh` on this host) knows these:
KEYWORDS = frozenset(
    'if then else elif fi case esac for select while until do done in function '
    'time { } ! [[ ]] coproc'.split())
BUILTINS = frozenset(
    '. : [ alias bg bind break builtin caller cd command compgen complete '
    'compopt continue declare dirs disown echo enable eval exec exit export '
    'false fc fg getopts hash help history jobs kill let local logout mapfile '
    'popd printf pushd pwd read readarray readonly return set shift shopt '
    'source suspend test times trap true type typeset ulimit umask unalias '
    'unset wait'.split())
# every shell function the modelled program defines before it starts resolving
SCRIPT_FUNCTIONS = frozenset(
    'error check_bool debug shcat usage help make_paths gen_hash read_cache '
    'save_cache list_contains read_config_paths replace de_expand_str '
    'de_tokenize_exec de_strip_fields reset_keys find_entry_paths '
    'check_entry_key read_entry_path validate_entry_id validate_action_id '
    'find_entry get_default_execarg'.split())

_HELP_BYTES = b'xdg-terminal-exec - Shell-based default terminal launcher.\n\nImplementation of the proposed Default Terminal Specification.\n\nUsage:\n  xdg-terminal-exec [options] [--] [command [arguments ...]]\n\nLaunches given command in default terminal, or launches default terminal.\n\nOptions for modifying terminal behavior (if supported by terminals\'s\nentry):\n\n  --app-id=app-id    set app-id (Wayland) or window class (X11)\n  --title=title      set tile of terminal.\n  --dir=workdir      set workdir of terminal.\n  --hold             instruct terminal to hold after command ends.\n\nOptions for printing data instead of executing terminal:\n\n  --print-id\n      print selected Desktop Entry ID. Action is appended delimited\n      by ":".\n\n  --print-path\n      print path to selected Desktop Entry. Action is appended\n      delimited by ":".\n\n  --print-content\n      print content of selected Desktop Entry. Conflicts with --print-cmd.\n\n  --print-cmd[=printf_sequence]\n      print resulting command line, delimited by given printf sequence,\n      "\\n" by default. If sequence is "\\n", output is also terminated with\n      a newline.\n\n  --print-delimiter=printf_sequence\n      printf sequence to be used as the delimiter between multiple requested\n      print statements, "\\n" by default. If sequence is "\\n", output is\n      also terminated with a newline.\n\nConfiguration:\n\nPreferred terminals are configured by listing their Desktop Entry IDs\nin config files named "[${desktop}-]xdg-terminals.list" placed in XDG Config\nhierarchy. Where "${desktop}" is a lowercased string that is matched\n(case-insensitively) against items of "${XDG_CURRENT_DESKTOP}".\n\nSee "man xdg-terminal-exec" for more details.\n'                # _HELP_BYTES, patched in by derive-help.py


# ---------------------------------------------------------------------------
# small shell-semantics helpers
# ---------------------------------------------------------------------------

def var_or(env, name, default):
    """${NAME-default} -- unset only."""
    v = env.get(name)
    return default if v is None else v


def var_or_colon(env, name, default):
    """${NAME:-default} -- unset or empty."""
    v = env.get(name)
    return default if v is None or v == '' else v


def check_bool(value):
    """check_bool() from the modelled program."""
    if value in ('true', 'True', 'TRUE', 'yes', 'Yes', 'YES', '1'):
        return True
    if value in ('false', 'False', 'FALSE', 'no', 'No', 'NO', '0'):
        return False
    return False                     # prints "Assuming '<v>' means no" to stderr


def split_fields(s, sep):
    """Word splitting of an unquoted expansion with IFS=<sep> (non-whitespace).

    One trailing delimiter is ignored (POSIX 2.5.3); interior and leading empty
    fields are kept.  An empty string yields no field at all.
    """
    if s == '':
        return []
    parts = s.split(sep)
    if parts and parts[-1] == '':
        parts.pop()
    return parts


def ascii_lower(s):
    """`tr '[:upper:]' '[:lower:]'` (C locale: ASCII only)."""
    out = []
    for ch in s:
        if 'A' <= ch <= 'Z':
            out.append(chr(ord(ch) + 32))
        else:
            out.append(ch)
    return ''.join(out)


_GLOB_CACHE = {}


def glob_match(pattern, text):
    """find(1) -path matching: shell pattern, '/' is not special."""
    rx = _GLOB_CACHE.get(pattern)
    if rx is None:
        rx = _glob_regex(pattern)
        _GLOB_CACHE[pattern] = rx
    return rx.match(text) is not None


def _glob_regex(pat):
    out = ['\\A']
    i, n = 0, len(pat)
    while i < n:
        c = pat[i]
        if c == '*':
            out.append('.*')
            i += 1
        elif c == '?':
            out.append('.')
            i += 1
        elif c == '[':
            j = i + 1
            neg = False
            if j < n and pat[j] in '!^':
                neg = True
                j += 1
            k = j
            if k < n and pat[k] == ']':
                k += 1
            while k < n and pat[k] != ']':
                k += 1
            if k >= n:                          # unterminated: literal '['
                out.append('\\[')
                i += 1
                continue
            cls = []
            for ch in pat[j:k]:
                cls.append('\\' + ch if ch in '\\^]' else ch)
            out.append('[' + ('^' if neg else '') + ''.join(cls) + ']')
            i = k + 1
        else:
            out.append(re.escape(c))
            i += 1
    out.append('\\Z')
    return re.compile(''.join(out), re.DOTALL)


def printf_b(text):
    """bash `printf '%b' "$text"` -> bytes."""
    out = bytearray()
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c != '\\':
            out += _enc(c)
            i += 1
            continue
        i += 1
        if i >= n:
            out += b'\\'
            break
        e = text[i]
        i += 1
        if e == '\\':
            out += b'\\'
        elif e == 'a':
            out += b'\a'
        elif e == 'b':
            out += b'\b'
        elif e == 'c':                        # stop all output of this printf
            return bytes(out)
        elif e in 'eE':
            out += b'\x1b'
        elif e == 'f':
            out += b'\f'
        elif e == 'n':
            out += b'\n'
        elif e == 'r':
            out += b'\r'
        elif e == 't':
            out += b'\t'
        elif e == 'v':
            out += b'\v'
        elif e == '0':
            j = i
            while j < n and j - i < 3 and text[j] in '01234567':
                j += 1
            digits = text[i:j] or '0'
            out.append(int(digits, 8) & 0xFF)
            i = j
        elif e == 'x':
            j = i
            while j < n and j - i < 2 and text[j] in '0123456789abcdefABCDEF':
                j += 1
            if j == i:
                out += b'\\x'
            else:
                out.append(int(text[i:j], 16) & 0xFF)
                i = j
        else:                                 # unrecognised: backslash kept
            out += b'\\' + _enc(e)
    return bytes(out)


def _enc(s):
    return s.encode('utf-8', 'surrogateescape')


def read_last_field(remainder, sep):
    """The value `read var1 var2` gives the last variable.

    Measured on bash 5.3: the last variable receives the remainder of the
    line, except that a trailing delimiter which is the only delimiter in that
    remainder is dropped ('--dir=a=' -> 'a', but '--dir=a==' -> 'a==').
    """
    if remainder.endswith(sep) and sep not in remainder[:-1]:
        return remainder[:-1]
    return remainder


def option_value(arg):
    """Value of --opt=value as the program reads it: `read` stops at a newline
    and drops a lone trailing '='."""
    line = arg.split('\n', 1)[0]
    head, sep, rest = line.partition('=')
    if not sep:
        return ''
    return read_last_field(rest, '=')


def read_shell_lines(path, trim):
    """Lines a `while read` loop sees: only '\\n'-terminated lines, last chunk
    without a terminator is dropped; `trim` = IFS whitespace stripping."""
    try:
        with open(path, 'rb') as f:
            data = f.read()
    except OSError:
        return None
    text = data.decode('utf-8', 'surrogateescape')
    lines = []
    start = 0
    while True:
        i = text.find('\n', start)
        if i < 0:
            break
        line = text[start:i]
        lines.append(line.strip(IFS_WS) if trim else line)
        start = i + 1
    return lines


# ---------------------------------------------------------------------------
# the resolver
# ---------------------------------------------------------------------------

class Resolver(object):
    """Stage-for-stage model of the modelled program's main flow.

    Every attribute mirrors a shell global; the ones the program only resets on
    a failed key check deliberately survive between candidates, because that is
    what the program does (see the report's "surprises" list).
    """

    def __init__(self, env, trace=None):
        self.env = env
        self.trace = trace                # list of str, or None
        self.candidates = []              # explain records
        # shell globals
        self.is_terminal = ''
        self.exec_usep = []               # token list (ASCII Unit Separator split)
        self.execarg = '-e'
        self.execarg_defined = False
        self.appidarg = ''
        self.titlearg = ''
        self.dirarg = ''
        self.holdarg = ''
        self.entry_path = ''
        self.entry_id = ''
        self.entry_action = ''
        self.execarg_compat = var_or(env, 'XTE_EXECARG_COMPAT', 'true')
        self.execarg_compat_configured = var_or(env, 'XTE_EXECARG_COMPAT', '')
        self.cache_enabled = var_or(env, 'XTE_CACHE_ENABLED', 'true')
        self.cache_configured = var_or(env, 'XTE_CACHE_ENABLED', '')
        self.last_action_listed = False
        self.aliases = {}                 # entry id -> path (last found wins)
        self.excluded_ids = []
        self.included_ids = []
        self.execarg_defaults = []        # [(entry id, default execarg)]
        self.entry_ids = []               # [(raw id[:action], source)]
        self.fallback_ids = []            # [(id, source)]
        # derived
        self.desktop_lower = ''
        self.configs = []                 # [(path, present)]
        self.app_dirs = []                # highest preference first
        self.find_results = []            # [(path, id)] in find order
        self.last_fail = None             # (code, detail) from check_entry_key
        self.selected = None
        self.no_terminal_reason = None
        self.abort = None                 # (rc, detail) for shell-level aborts

    # -- trace ------------------------------------------------------------
    def t(self, msg):
        if self.trace is not None:
            self.trace.append(msg)

    # -- selection --------------------------------------------------------
    def resolve(self):
        """Run the selection; returns True when an entry was selected."""
        env = self.env
        # tr must exist: its absence fails the assignment and `set -e` exits 1
        if not self.command_v('tr'):
            self.abort = (1, 'tr is not on PATH: the resolver aborts before parsing')
            return False
        self.desktop_lower = ascii_lower(env.get('XDG_CURRENT_DESKTOP') or '')
        if not self.make_paths():
            return False
        self.read_config_paths()
        self.find_entry_paths()
        return self.find_entry()

    def _home_default(self, suffix):
        """${HOME}<suffix>: an unset HOME aborts the shell under `set -u`."""
        home = self.env.get('HOME')
        if home is None or home == '':
            self.abort = (1, 'HOME is unset: the resolver aborts on set -u')
            return None
        return home + suffix

    def make_paths(self):
        env = self.env
        cfg_home = var_or_colon(env, 'XDG_CONFIG_HOME', None)
        if cfg_home is None:
            cfg_home = self._home_default('/.config')
        data_home = var_or_colon(env, 'XDG_DATA_HOME', None)
        if data_home is None:
            data_home = self._home_default('/.local/share')
        cache_home = var_or_colon(env, 'XDG_CACHE_HOME', None)
        if cache_home is None and self._home_default('/.cache') is None:
            pass
        if self.abort:
            return False
        cfg_dirs = var_or_colon(env, 'XDG_CONFIG_DIRS', '/etc/xdg')
        data_dirs = var_or_colon(env, 'XDG_DATA_DIRS', '/usr/local/share:/usr/share')
        desks = split_fields(self.desktop_lower, ':')
        configs = []
        for base in split_fields(cfg_home + ':' + cfg_dirs, ':'):
            base = base[:-1] if base.endswith('/') else base
            for desk in desks:
                configs.append(base + '/' + desk + '-xdg-terminals.list')
            configs.append(base + '/xdg-terminals.list')
        for base in split_fields(data_dirs, ':'):
            base = base[:-1] if base.endswith('/') else base
            for desk in desks:
                configs.append(base + '/xdg-terminal-exec/' + desk + '-xdg-terminals.list')
            configs.append(base + '/xdg-terminal-exec/xdg-terminals.list')
        self.configs = configs
        self.app_dirs = []
        for base in split_fields(data_home + ':' + data_dirs, ':'):
            base = base[:-1] if base.endswith('/') else base
            self.app_dirs.insert(0, base + '/applications')
        self.t('PATHS')
        self.t('  desktop=%r lower=%r' % (self.env.get('XDG_CURRENT_DESKTOP') or '',
                                         self.desktop_lower))
        self.configs = [(path, os.path.isfile(path)) for path in configs]
        for idx, (path, present) in enumerate(self.configs):
            self.t('  config[%d] %s %s' % (idx, 'present' if present else 'absent ', path))
        for idx, path in enumerate(self.app_dirs):
            self.t('  data[%d] %s%s' % (idx, '        ' if idx else 'type-f  ',
                                        path + '/. (find start)'))
        return True

    def read_config_paths(self):
        for path, present in self.configs:
            if not present:
                continue
            lines = read_shell_lines(path, True)
            if lines is None:
                continue
            for lineno, line in enumerate(lines, 1):
                self.config_line(path, lineno, line)

    def config_line(self, path, lineno, line):
        src = ('config', path, lineno)
        if line in ('/enable_cache', '/disable_cache'):
            if self.cache_configured:
                self.t('  %s:%d directive %s ignored (cache mode already set)'
                       % (path, lineno, line))
                return
            self.cache_enabled = 'true' if line == '/enable_cache' else 'false'
            self.cache_configured = '1'
            return
        if line in ('/execarg_compat', '/execarg_strict'):
            if self.execarg_compat_configured:
                self.t('  %s:%d directive %s ignored (compat mode already set)'
                       % (path, lineno, line))
                return
            self.execarg_compat = 'true' if line == '/execarg_compat' else 'false'
            self.execarg_compat_configured = '1'
            return
        if line.startswith('/execarg_default:') and line.find(':', 17) >= 0:
            if not check_bool(self.execarg_compat):
                self.t('  %s:%d directive %r ignored (strict mode)' % (path, lineno, line))
                return
            fields = line.split(':', 2)
            if validate_entry_id(fields[1]):
                self.execarg_defaults.append(
                    (fields[1], read_last_field(fields[2], ':')))
                self.t('  %s:%d execarg_default %s -> %r'
                       % (path, lineno, fields[1], self.execarg_defaults[-1][1]))
            return
        first = line[:1]
        if not (first and (first in ALNUM_US
                           or (first in '+-' and len(line) > 1 and line[1] in ALNUM_US))):
            return
        if first in '+-':
            exclusion = first
            body = line[1:]
        else:
            exclusion = ''
            body = line
        entry_id, has_action, action_tail = body.partition(':')
        action_id = read_last_field(action_tail, ':') if has_action else ''
        if not (validate_entry_id(entry_id) and validate_action_id(action_id)):
            self.t('  %s:%d discarded misspelled entry %r' % (path, lineno, line))
            return
        if exclusion == '':
            self.entry_ids.append((body, src))
            self.t('  %s:%d add candidate %r' % (path, lineno, body))
        elif exclusion == '+':
            if entry_id in self.excluded_ids:
                self.t('  %s:%d %s already excluded from fallback' % (path, lineno, entry_id))
            elif entry_id in self.included_ids:
                self.t('  %s:%d %s fallback exclusion already prevented'
                       % (path, lineno, entry_id))
            else:
                self.included_ids.append(entry_id)
                self.t('  %s:%d prevent fallback exclusion for %s'
                       % (path, lineno, entry_id))
        else:
            if entry_id in self.included_ids:
                self.t('  %s:%d %s fallback exclusion already prevented'
                       % (path, lineno, entry_id))
            elif entry_id in self.excluded_ids:
                self.t('  %s:%d %s already excluded from fallback'
                       % (path, lineno, entry_id))
            else:
                self.excluded_ids.append(entry_id)
                self.t('  %s:%d exclude %s from fallback' % (path, lineno, entry_id))

    # -- find -------------------------------------------------------------
    def find_entry_paths(self):
        """Model `find -L <dirs>. -type f ( -path .. ! -path .. ) -o ( .. )`.

        Only the first -o group is ANDed with -type f (implicit -a binds
        tighter), so directories named *.desktop inside the other data dirs are
        printed too.  Paths are printed as <dir>/./<rel>, pre-order DFS in
        readdir order.
        """
        good = []
        bad = []
        if not (self.command_v('find') and self.command_v('awk')):
            self.t('  find or awk is not on PATH: no entry is registered')
            return
        for idx, directory in enumerate(self.app_dirs):
            start = directory + '/.'
            good.append(start + '/[a-zA-Z0-9_]*.desktop')
            bad.append(start + '/*[^a-zA-Z0-9_./-]*')
        seq = 0
        for idx, directory in enumerate(self.app_dirs):
            start = directory + '/.'
            for rel, isfile, isdir in self._walk(start):
                path = start + '/' + rel
                if idx == 0 and not isfile:
                    continue
                if not glob_match(good[idx], path):
                    continue
                if glob_match(bad[idx], path):
                    continue
                seq += 1
                entry_id = path[path.rfind('/./') + 3:].replace('/', '-')
                self.find_results.append((path, entry_id))
                self.aliases[entry_id] = path
                if entry_id in self.excluded_ids:
                    self.t('  find#%d %s -> %s (excluded from fallback)'
                           % (seq, entry_id, path))
                    continue
                self.fallback_ids.insert(0, (entry_id, ('fallback', path, seq)))
        self.t('  registered %d entries, %d fallback ids'
               % (len(self.find_results), len(self.fallback_ids)))

    def _walk(self, start):
        """Yield (rel_path, is_regular_file, is_dir) in GNU find pre-order."""
        stack = []
        results = []

        def visit(abs_path, rel, ancestors):
            try:
                st = os.stat(abs_path)          # -L: follow symlinks
            except OSError:
                st = None
            isdir = st is not None and os.path.isdir(abs_path)
            isfile = st is not None and os.path.isfile(abs_path)
            results.append((rel, isfile, isdir))
            if not isdir:
                return
            key = (st.st_dev, st.st_ino)
            if key in ancestors:                # symlink loop: find stops there
                return
            try:
                names = [e.name for e in os.scandir(abs_path)]
            except OSError:
                return
            for name in names:
                visit(abs_path + '/' + name,
                      name if rel == '' else rel + '/' + name,
                      ancestors | {key})

        visit(start, '', frozenset())
        return results[1:]                      # the start itself never matches

    # -- candidate walk ---------------------------------------------------
    def find_entry(self):
        sequence = ([(raw, src) for raw, src in self.entry_ids]
                    + [(None, None)]
                    + [(raw, src) for raw, src in self.fallback_ids])
        de_checks = False
        for raw, src in sequence:
            if raw is None:                     # //fallback_start//
                de_checks = True
                self.t('CANDIDATES (fallback section: desktop show-in rules apply)')
                continue
            action = ''
            entry_id = raw
            if ':' in raw:
                action = raw.split(':', 1)[1]
                entry_id = raw.rsplit(':', 1)[0]
            rec = {'raw': raw, 'id': entry_id, 'action': action,
                   'src': src, 'path': None, 'outcome': None, 'detail': ''}
            self.candidates.append(rec)
            label = '%s%s' % (entry_id, ':' + action if action else '')
            if entry_id not in self.aliases:
                rec['outcome'] = 'not-found'
                rec['detail'] = 'no desktop file registered under this ID'
                self.t('TRY %s -> not-found (no registered path)' % label)
                continue
            path = self.aliases.pop(entry_id)
            rec['path'] = path
            self.t('TRY %s -> %s' % (label, path))
            if not self.read_entry_path(path, action, de_checks):
                code, detail = self.last_fail or ('entry-discarded', 'entry invalid')
                rec['outcome'] = code
                rec['detail'] = detail
                self.t('  REJECT %s: %s' % (code, detail))
                continue
            if not self.exec_usep:
                rec['outcome'] = 'no-exec'
                rec['detail'] = 'no usable Exec after % field stripping'
                self.t('  REJECT no-exec: Exec never read or empty after fields')
                continue
            if not self.is_terminal:
                rec['outcome'] = 'not-terminal-emulator'
                rec['detail'] = 'no Categories=...TerminalEmulator...'
                self.t('  REJECT not-terminal-emulator: no TerminalEmulator category')
                continue
            if not self.execarg_defined:
                if check_bool(self.execarg_compat):
                    self.execarg = self.default_execarg(entry_id)
                else:
                    rec['outcome'] = 'strict-mode-no-terminalarg-exec'
                    rec['detail'] = 'entry lacks TerminalArgExec and compat mode is off'
                    self.t('  REJECT strict-mode-no-terminalarg-exec')
                    continue
            self.entry_path = path
            self.entry_id = entry_id
            self.entry_action = action
            self.selected = rec
            rec['outcome'] = 'selected'
            rec['ignored'] = list(self.ignored_keys)
            self.t('  ACCEPT id=%s path=%s' % (label, path))
            return True
        self.no_terminal_reason = 'no candidate entry survived validation'
        self.t('NO_TERMINAL: ' + self.no_terminal_reason)
        return False

    def default_execarg(self, entry_id):
        for eid, value in self.execarg_defaults:
            if eid == entry_id:
                return value
        return '-e'

    # -- one desktop entry ------------------------------------------------
    def read_entry_path(self, path, action, de_checks):
        self.last_fail = None
        self.ignored_keys = []
        read_exec = False
        action_listed = False
        lines = read_shell_lines(path, True)
        if lines is None:
            self.last_fail = ('unreadable-file', 'cannot open %s' % path)
            return False
        status = 0
        for line in lines:
            if line.startswith('[Desktop Entry]'):
                if action == '':
                    read_exec = True
                    status = 0
                else:
                    status = 1
                continue
            if line[:1] in ALNUM_DASH:
                value = line.split('=', 1)[1] if '=' in line else line
                if line.partition('=')[0] in ('Type', 'NoDisplay'):
                    self.ignored_keys.append(line)
                value = value.lstrip(' ')
                if self.check_entry_key(line, value, action, read_exec, de_checks,
                                        action_listed):
                    if self.last_action_listed:
                        action_listed = True
                    status = 0
                    continue
                self.reset_keys()
                self.t('    key %r rejected' % line)
                return False
            if line.startswith('[Desktop Action ' + action + ']'):
                if action_listed:
                    read_exec = True
                    status = 0
                else:
                    self.last_fail = ('action-not-listed',
                                      'action %r is not in Actions' % action)
                    return False
                continue
            if line.startswith('['):
                if read_exec:
                    break
                status = 1
                continue
        if status != 0:
            self.last_fail = ('desktop-file-tail',
                              'file ends on a group header the reader skips')
            self.t('    entry reader ends on a skipped group header -> status 1')
            return False
        return True

    def check_entry_key(self, key, value, action, read_exec, de_checks, action_listed):
        """Returns True to keep reading, False to discard the entry."""
        self.last_action_listed = action_listed
        if key.startswith('Categories') and '=' in key:
            for category in split_fields(value, ';'):
                if category == 'TerminalEmulator':
                    self.is_terminal = 'true'
                    return True
            self.last_fail = ('not-terminal-emulator',
                              'Categories=%r has no TerminalEmulator' % value)
            return False
        if key.startswith('Actions') and '=' in key:
            if action == '':
                return True
            for listed in split_fields(value, ';'):
                if listed == action:
                    self.last_action_listed = True
                    return True
            self.last_fail = ('action-not-listed', 'Actions=%r lacks %r' % (value, action))
            return False
        if key.startswith('OnlyShowIn') and '=' in key:
            if not de_checks:
                return True
            desktops = split_fields(self.env.get('XDG_CURRENT_DESKTOP') or '', ':')
            for target in split_fields(value, ';'):
                for desktop in desktops:
                    if desktop == target:
                        return True
            self.last_fail = ('show-in-mismatch',
                              'OnlyShowIn=%r vs XDG_CURRENT_DESKTOP=%r'
                              % (value, self.env.get('XDG_CURRENT_DESKTOP') or ''))
            return False
        if key.startswith('NotShowIn') and '=' in key:
            if not de_checks:
                return True
            desktops = split_fields(self.env.get('XDG_CURRENT_DESKTOP') or '', ':')
            for target in split_fields(value, ';'):
                for desktop in desktops:
                    if desktop == target:
                        self.last_fail = ('show-in-mismatch',
                                          'NotShowIn=%r excludes %r' % (value, target))
                        return False
            return True
        if (key.startswith('X-TerminalArgExec') or key.startswith('TerminalArgExec')) and '=' in key:
            self.execarg = de_expand_str(value)
            self.execarg_defined = True
            return True
        if (key.startswith('X-ExecArg') or key.startswith('ExecArg')) and '=' in key:
            if self.execarg_compat == 'false':
                return True
            self.execarg = de_expand_str(value)
            self.execarg_defined = True
            return True
        for prefix, attr in (('X-TerminalArgAppId', 'appidarg'),
                             ('TerminalArgAppId', 'appidarg'),
                             ('X-TerminalArgTitle', 'titlearg'),
                             ('TerminalArgTitle', 'titlearg'),
                             ('X-TerminalArgDir', 'dirarg'),
                             ('TerminalArgDir', 'dirarg'),
                             ('X-TerminalArgHold', 'holdarg'),
                             ('TerminalArgHold', 'holdarg')):
            if key.startswith(prefix) and '=' in key:
                setattr(self, attr, de_expand_str(value))
                return True
        if key.startswith('TryExec') and '=' in key:
            expanded = de_expand_str(value)
            if not self.command_v(expanded):
                self.last_fail = ('tryexec-not-on-path',
                                  'TryExec=%r is not on PATH' % expanded)
                return False
            return True
        if key.startswith('Hidden') and '=' in key:
            if value == 'true':
                self.last_fail = ('hidden', 'Hidden=true')
                return False
            return True
        if key.startswith('Exec') and '=' in key:
            if not read_exec:
                return True
            expanded = de_expand_str(value)
            tokens, tok_ok = de_tokenize_exec(expanded)
            if not tok_ok:
                self.t('    tokenizer error: %d partial token(s) kept' % len(tokens))
            # de_strip_fields' exit status is NOT checked by the program: on a
            # bad % field the raw token list stays in place and the entry is
            # still accepted when Exec[0] resolves.
            stripped = de_strip_fields(tokens)
            if stripped is None:
                self.t('    % field rejected: raw tokens kept')
                self.exec_usep = tokens
            else:
                self.exec_usep = stripped
            exec0 = self.exec_usep[0] if self.exec_usep else ''
            if not self.command_v(exec0):
                self.last_fail = ('exec-not-on-path',
                                  'Exec[0]=%r is not on PATH' % exec0)
                return False
            return True
        return True

    def reset_keys(self):
        self.is_terminal = ''
        self.exec_usep = []
        self.execarg = '-e'
        self.execarg_defined = False
        self.appidarg = ''
        self.titlearg = ''
        self.dirarg = ''
        self.holdarg = ''

    # -- command -v -------------------------------------------------------
    def command_v(self, name):
        if name == '':
            return False
        if '/' in name:
            return os.path.isfile(name) and os.access(name, os.X_OK)
        if name in self.aliases or name in KEYWORDS or name in BUILTINS \
                or name in SCRIPT_FUNCTIONS:
            return True
        for directory in split_fields(self.env.get('PATH') or '', ':'):
            candidate = (directory or '.') + '/' + name
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return True
        return False


# ---------------------------------------------------------------------------
# string expanders / desktop-entry Exec tokenizer
# ---------------------------------------------------------------------------

def de_expand_str(value):
    """\\s \\n \\t \\r \\\\ expansion; an unsupported escape keeps only its char."""
    out = []
    i, n = 0, len(value)
    while i < n:
        c = value[i]
        if c != '\\':
            out.append(c)
            i += 1
            continue
        i += 1
        if i >= n:                        # trailing backslash is dropped
            break
        e = value[i]
        i += 1
        if e == 's':
            out.append(' ')
        elif e == 'n':
            out.append('\n')
        elif e == 't':
            out.append('\t')
        elif e == 'r':
            out.append('\r')
        elif e == '\\':
            out.append('\\')
        else:
            out.append(e)                 # backslash dropped, char kept
    return ''.join(out)


def de_tokenize_exec(text):
    """Model of the program's Exec tokenizer.  Returns (tokens, ok)."""
    tokens = []
    current = []
    remainder = text
    quoted = False
    in_space = False
    while remainder:
        left_len = 0
        while left_len < len(remainder) and remainder[left_len] not in TOK_SPECIAL:
            left_len += 1
        left = remainder[:left_len]
        current.append(left)
        if left == remainder:
            break
        remainder = remainder[left_len:]
        ch = remainder[0]
        remainder = remainder[1:]
        if in_space and left == '' and ch in ' \t\n\r\v\f':
            continue
        if in_space:
            in_space = False
        if quoted and ch == '"':
            quoted = False
            continue
        if not quoted and ch == '"':
            quoted = True
            continue
        if not quoted and ch in '`$\\\'><~|&;*?#()':
            return (finish(current, tokens), False)
        if quoted and ch in '`$':
            return (finish(current, tokens), False)
        if quoted and ch == '\\':
            if not remainder:
                return (finish(current, tokens), False)
            current.append(remainder[0])
            remainder = remainder[1:]
            continue
        if not quoted and ch in ' \t\n\r\v\f':
            if any(c not in ' \t\n\r\v\f' for c in remainder):
                tokens.append(''.join(current))
                current = []
                in_space = True
            else:
                break
            continue
        if quoted and ch in ' \t\n\r\v\f\'><~|&;*?#()':
            current.append(ch)
            continue
        return (finish(current, tokens), False)
    if quoted:
        return (finish(current, tokens), False)
    return (finish(current, tokens), True)


def finish(current, tokens):
    # A trailing separator produces a trailing empty field, which word
    # splitting on the ASCII Unit Separator drops again.
    text = ''.join(current)
    if text != '':
        tokens.append(text)
    return tokens


def de_strip_fields(tokens):
    """% field handling.  Returns the token list or None for a bad field."""
    out = []
    fu_found = False
    for token in tokens:
        if _has_field(token, 'dDnNvm'):
            continue
        if _has_field(token, 'fFuU'):
            if fu_found:
                return None
            fu_found = True
            continue
        if _has_field(token, 'i') or _has_field(token, 'c'):
            continue
        if '%%' in token:
            out.append(token.replace('%%', '%'))
            continue
        if _invalid_field(token):
            return None
        out.append(token)
    return out


def _has_field(token, chars):
    """True when <token> matches *[!%]%<c>* or %<c>* for one of <chars>."""
    n = len(token)
    for i in range(n):
        if token[i] != '%':
            continue
        if i + 1 < n and token[i + 1] in chars:
            if i == 0 or token[i - 1] != '%':
                return True
    return False


def _invalid_field(token):
    """True when <token> matches *%?* or *[!%]% (an unknown trailing % field)."""
    n = len(token)
    for i in range(n):
        if token[i] != '%':
            continue
        if i + 1 < n:
            if i == 0 or token[i - 1] != '%':
                return True
        else:
            return True                 # trailing lone %
    return False


# ---------------------------------------------------------------------------
# argument handling and printing
# ---------------------------------------------------------------------------

def help_bytes():
    return _HELP_BYTES


def emulate(resolver, args):
    """Return (stdout_bytes, rc) for a print/--test run, or (bytes, None) when
    the modelled program would launch a terminal."""
    out = bytearray()
    appid_val = title_val = dir_val = ''
    hold = False
    test_mode = False
    print_data = []
    print_delimiter = '\\n'
    print_cmd_delimiter = '\\n'
    rest = list(args)
    i = 0
    n = len(rest)
    while i < n:
        arg = rest[i]
        if arg == '--':
            i += 1
            break
        if arg == '-e' or arg == resolver.execarg:
            i += 1
            break
        if arg.startswith('--app-id='):
            appid_val = option_value(arg)
        elif arg.startswith('--title='):
            title_val = option_value(arg)
        elif arg.startswith('--dir='):
            dir_val = option_value(arg)
        elif arg == '--hold':
            hold = True
        elif arg == '--test':
            test_mode = True
        elif arg == '--print-path':
            print_data.append('path')
        elif arg == '--print-id':
            print_data.append('id')
        elif arg == '--print-content':
            print_data.append('content')
        elif arg == '--print-cmd':
            print_data.append('cmd')
        elif arg.startswith('--print-cmd='):
            print_data.append('cmd')
            print_cmd_delimiter = option_value(arg)
        elif arg.startswith('--print-delimiter='):
            print_delimiter = option_value(arg)
        elif arg[:1] != '-':
            break                       # first command word: leave it in argv
        i += 1                          # unknown option: discarded
    rest = rest[i:]

    print_first = True
    if 'id' in print_data:
        out += _enc(resolver.entry_id)
        if resolver.entry_action:
            out += b':' + _enc(resolver.entry_action)
        print_first = False
    if 'path' in print_data:
        path = resolver.entry_path
        if '/./' in path:
            path = path[:path.index('/./')] + '/' + path[path.rindex('/./') + 3:]
        if not print_first:
            out += printf_b(print_delimiter)
        out += _enc(path)
        if resolver.entry_action:
            out += b':' + _enc(resolver.entry_action)
        print_first = False
    if 'content' in print_data:
        if not print_first:
            out += printf_b(print_delimiter)
        chunk = _shcat(resolver.entry_path)
        if chunk is None:
            return bytes(out), 1
        out += chunk
        print_first = False

    if not print_data or 'cmd' in print_data:
        pass
    elif 'content' in print_data:
        return bytes(out), 0
    else:
        if print_delimiter == '\\n':
            out += b'\n'
        return bytes(out), 0

    argv = list(rest)
    if argv and resolver.execarg != '':
        argv.insert(0, resolver.execarg)
    if resolver.holdarg and check_bool(str(hold).lower()):
        argv.insert(0, resolver.holdarg)
    if resolver.dirarg and dir_val:
        if resolver.dirarg.endswith('='):
            argv.insert(0, resolver.dirarg + dir_val)
        else:
            argv[0:0] = [resolver.dirarg, dir_val]
    if resolver.titlearg and title_val:
        if resolver.titlearg.endswith('='):
            argv.insert(0, resolver.titlearg + title_val)
        else:
            argv[0:0] = [resolver.titlearg, title_val]
    if resolver.appidarg and appid_val:
        if resolver.appidarg.endswith('='):
            argv.insert(0, resolver.appidarg + appid_val)
        else:
            argv[0:0] = [resolver.appidarg, appid_val]
    argv[0:0] = list(resolver.exec_usep)

    if test_mode:
        out += b'Command and arguments:\n'
        if argv:
            for a in argv:
                out += b'  >' + _enc(a) + b'<\n'
        else:
            out += b'  ><\n'
        return bytes(out), 0

    if 'cmd' not in print_data:
        return bytes(out), None        # the modelled program execs a terminal

    if not print_first:
        out += printf_b(print_delimiter)
    first = True
    for a in argv:
        if not first:
            out += printf_b(print_cmd_delimiter or '\\n')
        first = False
        out += _enc(a)
    if print_cmd_delimiter == '\\n' or (not print_first and print_delimiter == '\\n'):
        out += b'\n'
    return bytes(out), 0


def _shcat(path):
    try:
        with open(path, 'rb') as f:
            data = f.read()
    except OSError:
        return None
    if not data:
        return b''
    if not data.endswith(b'\n'):
        data = data[:data.rfind(b'\n') + 1] if b'\n' in data else b''
    return data


# ---------------------------------------------------------------------------
# validation helpers
# ---------------------------------------------------------------------------

def validate_entry_id(value):
    if value == '' or value == '.desktop':
        return False
    for ch in value:
        if ch not in ID_CHARS:
            return False
    return value.endswith('.desktop')


def validate_action_id(value):
    if value == '':
        return True
    for ch in value:
        if ch not in ACTION_CHARS:
            return False
    return True


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def cmd_print(args):
    for arg in args:
        if arg == '--':
            break
        if arg in ('-h', '--help'):
            sys.stdout.buffer.write(help_bytes())
            return 0
    resolver = Resolver(dict(os.environ))
    if not resolver.resolve():
        if resolver.abort:
            sys.stderr.write('mado-terminal: %s\n' % resolver.abort[1])
        else:
            sys.stderr.write('xdg-terminal-exec: No valid terminal entry was found in:'
                             ' %s\n' % ':'.join(resolver.app_dirs))
        return 1
    out, rc = emulate(resolver, args)
    if rc is None:
        sys.stderr.write('mado-terminal: refusing to launch a terminal; '
                         'pass a --print-* or --test option\n')
        return 2
    sys.stdout.buffer.write(out)
    sys.stdout.buffer.flush()
    return rc


def _reason_counts(candidates):
    counts = {}
    for cand in candidates:
        counts[cand['outcome']] = counts.get(cand['outcome'], 0) + 1
    return ','.join('%s:%d' % kv for kv in sorted(counts.items())) or '-'


def cmd_explain(args):
    observed = None
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--observed':
            if i + 1 >= len(args):
                sys.stderr.write('usage: mado-terminal.py explain [--observed FILE]\n')
                return 2
            observed = args[i + 1]
            i += 2
            continue
        if arg.startswith('--observed='):
            observed = arg.split('=', 1)[1]
            i += 1
            continue
        sys.stderr.write('usage: mado-terminal.py explain [--observed FILE]\n')
        return 2
    trace = []
    resolver = Resolver(dict(os.environ), trace)
    ok = resolver.resolve()
    lines = ['# mado-terminal.py explain (xdg-terminal-exec v0.14.3 model)']
    lines += trace
    if not ok:
        if resolver.abort:
            lines.append('ABORT rc=%d: %s' % (resolver.abort[0], resolver.abort[1]))
        counts = {}
        for cand in resolver.candidates:
            counts[cand['outcome']] = counts.get(cand['outcome'], 0) + 1
        lines.append('SUMMARY tried=%d rejected=%d reasons=%s'
                     % (len(resolver.candidates), sum(counts.values()),
                        _reason_counts(resolver.candidates)))
        lines.append('MADO_TERM: selected=- path=- verdict=NO_TERMINAL')
        sys.stdout.write('\n'.join(lines) + '\n')
        return 3
    rec = resolver.selected
    src = rec['src']
    if src[0] == 'config':
        via = '%s:%d' % (src[1], src[2])
    else:
        via = 'fallback find#%d %s' % (src[2], src[1])
    lines.append('SELECTED id=%s%s path=%s via=%s'
                 % (resolver.entry_id,
                    ':' + resolver.entry_action if resolver.entry_action else '',
                    resolver.entry_path, via))
    lines.append('  command=%r execarg=%r hold=%r dir=%r title=%r app-id=%r'
                 % (resolver.exec_usep, resolver.execarg, resolver.holdarg,
                    resolver.dirarg, resolver.titlearg, resolver.appidarg))
    if rec.get('ignored'):
        lines.append('  NOTE unread-keys=%s (0.14.3 reads neither Type nor '
                     'NoDisplay; they never reject an entry)'
                     % ','.join(rec['ignored']))
    lines.append('  NOTE cache-enabled=%s (the resolver cache is modelled as cold)'
                 % resolver.cache_enabled)
    rejected = [c for c in resolver.candidates if c['outcome'] != 'selected']
    lines.append('SUMMARY tried=%d rejected=%d reasons=%s'
                 % (len(resolver.candidates), len(rejected),
                    _reason_counts(rejected)))
    verdict = 'OK'
    rc = 0
    if observed is not None:
        try:
            with open(observed, 'rb') as f:
                want = f.read()
        except OSError as exc:
            sys.stderr.write('mado-terminal: cannot read %s: %s\n' % (observed, exc))
            return 2
        got, orc = emulate(resolver, ['--print-id', '--print-path', '--print-cmd'])
        if got is None:
            orc = 2
            got = b''
        if got == want and orc == 0:
            verdict = 'AGREE'
        else:
            verdict = 'DIFFER'
            rc = 1
            lines.append('OBSERVED %r' % want)
            lines.append('MODEL    %r' % got)
    lines.append('MADO_TERM: selected=%s path=%s verdict=%s'
                 % (resolver.entry_id, resolver.entry_path, verdict))
    sys.stdout.write('\n'.join(lines) + '\n')
    return rc


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

STUB = b'#!/bin/sh\nexit 0\n'


def _write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = 'wb' if isinstance(text, bytes) else 'w'
    with open(path, mode) as f:
        f.write(text)
    return path


def _stub(root, rel, body=STUB):
    path = _write(root, rel, body)
    os.chmod(path, 0o755)
    return path


def _case_env(root, desktop='Hyprland', extra=None):
    env = {
        'HOME': root + '/home',
        'PATH': root + '/bin',
        'XDG_CURRENT_DESKTOP': desktop,
        'XDG_CONFIG_HOME': root + '/home/.config',
        'XDG_CONFIG_DIRS': root + '/etc/xdg',
        'XDG_DATA_HOME': root + '/home/.local/share',
        'XDG_DATA_DIRS': root + '/usr/local/share:' + root + '/usr/share',
        'XDG_CACHE_HOME': root + '/cache',
    }
    if extra:
        env.update(extra)
    return env


TERM_ENTRY = (
    '[Desktop Entry]\n'
    'Type=Application\n'
    'Name=Term\n'
    'Categories=System;TerminalEmulator;\n'
    'X-TerminalArgExec=-e\n'
    'Exec={exec}\n'
)


def _selftest_cases():
    """Each case: (name, builder(root), expected dict)."""
    cases = []

    def case(name, expect):
        def register(fn):
            cases.append((name, fn, expect))
            return fn
        return register

    @case('basic-explicit', {'rc': 0, 'id': 'Term.desktop',
                             'stdout': 'Term.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'Term.desktop\n')
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('fallback-only', {'rc': 0, 'id': 'Term.desktop',
                            'stdout': 'Term.desktop\n'})
    def _(root):
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('explicit-beats-fallback', {'rc': 0, 'id': 'B.desktop',
                                      'stdout': 'B.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'B.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term'))
        _write(root, 'home/.local/share/applications/B.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('hidden-true', {'rc': 0, 'id': 'B.desktop',
                          'stdout': 'B.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'A.desktop\nB.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Application\nHidden=true\n'))
        _write(root, 'home/.local/share/applications/B.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('hidden-capitalised', {'rc': 0, 'id': 'A.desktop',
                                 'stdout': 'A.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'A.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Application\nHidden=True\n'))
        _stub(root, 'bin/term')

    @case('no-categories', {'rc': 0, 'id': 'B.desktop',
                            'stdout': 'B.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'A.desktop\nB.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Categories=System;TerminalEmulator;\n', ''))
        _write(root, 'home/.local/share/applications/B.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('tryexec-missing', {'rc': 0, 'id': 'B.desktop',
                              'stdout': 'B.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'A.desktop\nB.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Application\nTryExec=nope\n'))
        _write(root, 'home/.local/share/applications/B.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('exec-not-on-path', {'rc': 0, 'id': 'B.desktop',
                               'stdout': 'B.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'A.desktop\nB.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='nope'))
        _write(root, 'home/.local/share/applications/B.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('exec-quotes', {'rc': 0, 'id': 'Term.desktop',
                          'stdout': 'Term.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'Term.desktop\n')
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term --class "my term" %f'))
        _stub(root, 'bin/term')

    @case('exec-percent-literal', {'rc': 0, 'id': 'Term.desktop',
                                   'stdout': 'Term.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'Term.desktop\n')
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term a%%b %U'))
        _stub(root, 'bin/term')

    @case('exec-two-file-fields', {'rc': 0, 'id': 'A.desktop',
                                   'args': ['--print-cmd= '],
                                   'stdout': 'term %f %U'})
    def _(root):
        # A bad % field does not reject the entry: de_strip_fields' status is
        # ignored, the raw tokens stay and Exec[0] still resolves.
        _write(root, 'home/.config/xdg-terminals.list', 'A.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term %f %U'))
        _stub(root, 'bin/term')

    @case('exec-unknown-field', {'rc': 0, 'id': 'A.desktop',
                                 'args': ['--print-cmd= '],
                                 'stdout': 'term %Z'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'A.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term %Z'))
        _stub(root, 'bin/term')

    @case('compat-default-execarg', {'rc': 0, 'id': 'Term.desktop',
                                     'stdout': 'Term.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'Term.desktop\n')
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term').replace('X-TerminalArgExec=-e\n', ''))
        _stub(root, 'bin/term')

    @case('strict-rejects-no-execarg', {'rc': 1, 'id': None, 'stdout': ''})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list',
               '/execarg_strict\nTerm.desktop\n')
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term').replace('X-TerminalArgExec=-e\n', ''))
        _stub(root, 'bin/term')

    @case('execarg-default-directive', {'rc': 0, 'id': 'Term.desktop',
                                        'stdout': 'Term.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list',
               '/execarg_default:Term.desktop:-x\nTerm.desktop\n')
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term').replace('X-TerminalArgExec=-e\n', ''))
        _stub(root, 'bin/term')

    @case('action-listed', {'rc': 0, 'id': 'Term.desktop',
                            'stdout': 'Term.desktop:New\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'Term.desktop:New\n')
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term')
               + 'Actions=New;\n\n[Desktop Action New]\nExec=term new\n')
        _stub(root, 'bin/term')

    @case('action-not-listed', {'rc': 1, 'id': None, 'stdout': ''})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'Term.desktop:New\n')
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('exclusion-directive', {'rc': 0, 'id': 'B.desktop',
                                  'stdout': 'B.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', '-A.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term'))
        _write(root, 'home/.local/share/applications/B.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('inclusion-prevents-exclusion', {'rc': 0, 'id': 'A.desktop',
                                           'stdout': 'A.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', '-B.desktop\n-B.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term'))
        _write(root, 'home/.local/share/applications/B.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('higher-data-dir-wins', {'rc': 0, 'id': 'Term.desktop',
                                   'stdout': 'Term.desktop\n'})
    def _(root):
        _write(root, 'usr/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='nope'))
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('desktop-specific-list-first', {'rc': 0, 'id': 'A.desktop',
                                          'stdout': 'A.desktop\n'})
    def _(root):
        _write(root, 'home/.config/hyprland-xdg-terminals.list', 'A.desktop\n')
        _write(root, 'home/.config/xdg-terminals.list', 'B.desktop\n')
        for name, exe in (('A', 'term'), ('B', 'term')):
            _write(root, 'home/.local/share/applications/%s.desktop' % name,
                   TERM_ENTRY.format(exec=exe))
        _stub(root, 'bin/term')

    @case('config-dirs-after-config-home', {'rc': 0, 'id': 'B.desktop',
                                            'stdout': 'B.desktop\n'})
    def _(root):
        _write(root, 'etc/xdg/xdg-terminals.list', 'A.desktop\n')
        _write(root, 'home/.config/xdg-terminals.list', 'B.desktop\n')
        for name in ('A', 'B'):
            _write(root, 'home/.local/share/applications/%s.desktop' % name,
                   TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('onlyshowin-fallback', {'rc': 0, 'id': 'B.desktop',
                                  'stdout': 'B.desktop\n'})
    def _(root):
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Application\nOnlyShowIn=GNOME;\n'))
        _write(root, 'home/.local/share/applications/B.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('notshowin-fallback', {'rc': 0, 'id': 'B.desktop',
                                 'stdout': 'B.desktop\n'})
    def _(root):
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Application\nNotShowIn=Hyprland;\n'))
        _write(root, 'home/.local/share/applications/B.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('onlyshowin-ignored-when-explicit', {'rc': 0, 'id': 'A.desktop',
                                               'stdout': 'A.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'A.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Application\nOnlyShowIn=GNOME;\n'))
        _stub(root, 'bin/term')

    @case('no-entries', {'rc': 1, 'id': None, 'stdout': ''})
    def _(root):
        pass

    @case('skipped-group-header-tail', {'rc': 0, 'id': 'C.desktop',
                                        'stdout': 'C.desktop\n'})
    def _(root):
        # A leaks is_terminal/Exec into B; B's reader ends on a skipped group
        # header, which makes read_entry_path return 1 and discard it.
        _write(root, 'home/.config/xdg-terminals.list',
               '/execarg_strict\nA.desktop\nB.desktop\nC.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term').replace('X-TerminalArgExec=-e\n', ''))
        _write(root, 'home/.local/share/applications/B.desktop', '[X-Extra]\n')
        _write(root, 'home/.local/share/applications/C.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('no-trailing-newline', {'rc': 0, 'id': 'B.desktop',
                                  'stdout': 'B.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'A.desktop\nB.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term').rstrip('\n'))
        _write(root, 'home/.local/share/applications/B.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('key-whitespace-trimmed', {'rc': 0, 'id': 'A.desktop',
                                     'stdout': 'A.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', '  A.desktop  \n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Categories=System', '  Categories=System'))
        _stub(root, 'bin/term')

    @case('state-leak-categories-less', {'rc': 0, 'id': 'C.desktop',
                                         'stdout': 'C.desktop\n'})
    def _(root):
        # C has no TerminalEmulator category: it is accepted only because
        # is_terminal survived A's strict-mode rejection.
        _write(root, 'home/.config/xdg-terminals.list',
               '/execarg_strict\nA.desktop\nC.desktop\n')
        _write(root, 'home/.local/share/applications/A.desktop',
               TERM_ENTRY.format(exec='term').replace('X-TerminalArgExec=-e\n', ''))
        _write(root, 'home/.local/share/applications/C.desktop',
               '[Desktop Entry]\nType=Application\nX-TerminalArgExec=-e\nExec=term\n')
        _stub(root, 'bin/term')

    def one(root, config='Term.desktop\n', entry=None, exe='term',
            where='home/.local/share/applications/Term.desktop', stub='term',
            extra_env=None):
        if config is not None:
            _write(root, 'home/.config/xdg-terminals.list', config)
        _write(root, where, entry if entry is not None else TERM_ENTRY.format(exec=exe))
        if stub:
            _stub(root, 'bin/' + stub)

    @case('print-path-normalises-dot', {'rc': 0, 'id': 'Term.desktop',
                                        'args': ['--print-id', '--print-path'],
                                        'stdout': 'Term.desktop\n'
                                                  '$ROOT/home/.local/share/'
                                                  'applications/Term.desktop\n'})
    def _(root):
        one(root)

    @case('print-delimiters', {'rc': 0, 'id': 'Term.desktop',
                               'args': ['--print-id', '--print-path', '--print-cmd',
                                        '--print-delimiter=|'],
                               'stdout': 'Term.desktop|$ROOT/home/.local/share/'
                                         'applications/Term.desktop|term\n'})
    def _(root):
        one(root)

    @case('print-order-fixed', {'rc': 0, 'id': 'Term.desktop',
                                'args': ['--print-cmd', '--print-id'],
                                'stdout': 'Term.desktop\nterm\n'})
    def _(root):
        one(root)

    @case('print-cmd-sequence', {'rc': 0, 'id': 'Term.desktop',
                                 'args': ['--print-cmd=,'],
                                 'stdout': 'term'})
    def _(root):
        one(root)

    @case('print-cmd-multi-token', {'rc': 0, 'id': 'Term.desktop',
                                    'args': ['--print-cmd', '--', 'echo', 'hi'],
                                    'stdout': 'term\n-e\necho\nhi\n'})
    def _(root):
        one(root)

    @case('print-content', {'rc': 0, 'id': 'Term.desktop',
                            'args': ['--print-content'],
                            'stdout': TERM_ENTRY.format(exec='term')})
    def _(root):
        one(root)

    @case('test-mode', {'rc': 0, 'id': 'Term.desktop',
                        'args': ['--test'],
                        'stdout': 'Command and arguments:\n  >term<\n'})
    def _(root):
        one(root, config=None)

    @case('unknown-option-discarded', {'rc': 0, 'id': 'Term.desktop',
                                       'args': ['--bogus', '--print-id'],
                                       'stdout': 'Term.desktop\n'})
    def _(root):
        one(root)

    @case('exec-quoted-empty', {'rc': 0, 'id': 'Term.desktop',
                                'args': ['--print-cmd'],
                                'stdout': 'term\n'})
    def _(root):
        one(root, exe='term ""')

    @case('exec-builtin-first-word', {'rc': 0, 'id': 'Term.desktop',
                                      'args': ['--print-cmd'],
                                      'stdout': 'printf\n'})
    def _(root):
        one(root, exe='printf', stub=None)

    @case('tryexec-shell-function', {'rc': 0, 'id': 'Term.desktop',
                                     'stdout': 'Term.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'Term.desktop\n')
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Application\nTryExec=find_entry\n'))
        _stub(root, 'bin/term')

    @case('tryexec-builtin', {'rc': 0, 'id': 'Term.desktop',
                              'stdout': 'Term.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'Term.desktop\n')
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Application\nTryExec=printf\n'))
        _stub(root, 'bin/term')

    @case('nodisplay-ignored', {'rc': 0, 'id': 'Term.desktop',
                                'stdout': 'Term.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'Term.desktop\n')
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Application\nNoDisplay=true\n'))
        _stub(root, 'bin/term')

    @case('type-link-ignored', {'rc': 0, 'id': 'Term.desktop',
                                'stdout': 'Term.desktop\n'})
    def _(root):
        _write(root, 'home/.config/xdg-terminals.list', 'Term.desktop\n')
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Link\n'))
        _stub(root, 'bin/term')

    @case('onlyshowin-multi-desktop', {'rc': 0, 'id': 'Term.desktop',
                                       'stdout': 'Term.desktop\n',
                                       'env': {'XDG_CURRENT_DESKTOP': 'GNOME:Hyprland'}})
    def _(root):
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Application\nOnlyShowIn=Hyprland;\n'))
        _stub(root, 'bin/term')

    @case('notshowin-total-exclusion', {'rc': 1, 'id': None, 'stdout': ''})
    def _(root):
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Application\nNotShowIn=Hyprland;\n'))
        _stub(root, 'bin/term')

    @case('desktop-unset-fallback-showin', {'rc': 1, 'id': None, 'stdout': '',
                                            'env': {'XDG_CURRENT_DESKTOP': None}})
    def _(root):
        _write(root, 'home/.local/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term').replace(
                   'Type=Application\n', 'Type=Application\nOnlyShowIn=Hyprland;\n'))
        _stub(root, 'bin/term')

    @case('invalid-entry-id', {'rc': 0, 'id': 'Term.desktop',
                               'stdout': 'Term.desktop\n'})
    def _(root):
        one(root, config='Bad Name.desktop\n')

    @case('invalid-action-id', {'rc': 0, 'id': 'Term.desktop',
                                'stdout': 'Term.desktop\n'})
    def _(root):
        one(root, config='Term.desktop:Bad Action\n')

    @case('invalid-chars-nested-desktop', {'rc': 1, 'id': None, 'stdout': ''})
    def _(root):
        _write(root, 'home/.local/share/applications/x y/Term.desktop',
               TERM_ENTRY.format(exec='term'))
        _stub(root, 'bin/term')

    @case('directory-shadows-file', {'rc': 1, 'id': None, 'stdout': ''})
    def _(root):
        # A directory named *.desktop in a non-first data dir is registered
        # (that find group has no -type f) and overwrites the alias last.
        _write(root, 'usr/share/applications/Term.desktop',
               TERM_ENTRY.format(exec='term'))
        os.makedirs(root + '/usr/local/share/applications/Term.desktop/inner',
                    exist_ok=True)
        _stub(root, 'bin/term')

    @case('home-defaults-when-xdg-unset',
          {'rc': 0, 'id': 'Term.desktop', 'stdout': 'Term.desktop\n',
           'env': {'XDG_CONFIG_HOME': None, 'XDG_DATA_HOME': None,
                   'XDG_CACHE_HOME': None}})
    def _(root):
        one(root)

    @case('tr-missing', {'rc': 1, 'id': None, 'stdout': ''})
    def _(root):
        one(root)
        os.unlink(root + '/bin/tr')

    @case('find-missing', {'rc': 1, 'id': None, 'stdout': ''})
    def _(root):
        one(root)
        os.unlink(root + '/bin/find')

    @case('cache-directive-harmless', {'rc': 0, 'id': 'Term.desktop',
                                       'stdout': 'Term.desktop\n'})
    def _(root):
        one(root, config='/enable_cache\nTerm.desktop\n')

    return cases


def cmd_selftest(argv):
    work = os.environ.get('TMPDIR') or tempfile.gettempdir()
    base = tempfile.mkdtemp(prefix='mado-terminal-selftest-', dir=work)
    total = passed = 0
    failures = []
    try:
        for name, build, expect in _selftest_cases():
            total += 1
            root = os.path.join(base, name)
            for sub in ('home/.config', 'home/.local/share/applications',
                        'usr/share/applications', 'usr/local/share/applications',
                        'etc/xdg', 'cache', 'bin'):
                os.makedirs(os.path.join(root, sub), exist_ok=True)
            for helper in ('tr', 'find', 'awk'):
                _stub(root, 'bin/' + helper)
            build(root)
            env = _case_env(root)
            for key, value in (expect.get('env') or {}).items():
                if value is None:
                    env.pop(key, None)
                else:
                    env[key] = value
            resolver = Resolver(env)
            ok = resolver.resolve()
            if ok:
                out, rc = emulate(resolver, expect.get('args') or ['--print-id'])
                got = {'rc': 0 if rc is None else rc,
                       'id': resolver.entry_id,
                       'stdout': out.decode('utf-8', 'surrogateescape')}
            else:
                got = {'rc': resolver.abort[0] if resolver.abort else 1,
                       'id': None, 'stdout': ''}
            got['stdout'] = got['stdout'].replace(root, '$ROOT')
            want = dict(expect)
            want.pop('args', None)
            want.pop('env', None)
            if got != want:
                failures.append('%s: expected %r got %r' % (name, want, got))
            else:
                passed += 1
            shutil.rmtree(root, ignore_errors=True)
    finally:
        shutil.rmtree(base, ignore_errors=True)
    for line in failures:
        sys.stderr.write('FAIL %s\n' % line)
    sys.stdout.write('MADO_TERMINAL_SELFTEST: %d/%d passed\n' % (passed, total))
    return 0 if passed == total else 1


# ---------------------------------------------------------------------------

def main(argv):
    args = argv[1:]
    if not args:
        sys.stderr.write('usage: mado-terminal.py print [args] | explain '
                         '[--observed FILE] | --selftest\n')
        return 2
    command = args[0]
    if command == 'print':
        return cmd_print(args[1:])
    if command == 'explain':
        return cmd_explain(args[1:])
    if command == '--selftest':
        return cmd_selftest(args[1:])
    if command in ('-h', '--help'):
        sys.stdout.write(__doc__)
        return 0
    sys.stderr.write('usage: mado-terminal.py print [args] | explain '
                     '[--observed FILE] | --selftest\n')
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
