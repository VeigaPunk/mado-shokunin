#!/usr/bin/env python3
"""mado-execargv.py -- model of the launch argv GIO 2.90.1 builds from a desktop entry.

Surface (glib 2.90.1, /usr/bin/gio sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462):
  expand_application_parameters  gdesktopappinfo.c:2700-2746
  expand_macro                   gdesktopappinfo.c:2579-2699
  expand_macro_single            gdesktopappinfo.c:2506-2555
  expand_macro_uri               gdesktopappinfo.c:2556-2578
  the do/while launch loop       gdesktopappinfo.c:3002-3021 (one spawn per iteration)
  g_shell_quote / g_shell_parse_argv / tokenize_command_line / g_shell_unquote  gshell.c

Usage:
  mado-execargv.py DESKTOP [FILE...] [--json]
  mado-execargv.py --selftest

Named limits (measured against the oracle this round, off the frozen case plane):
  - the load-time TryExec check and the Exec argv[0] program lookup
    (gdesktopappinfo.c:1976-2004, :3053-3070) are not modelled; scored cases pin
    Exec argv[0] to an existing executable probe script.
  - Terminal=true is not modelled (prepend_terminal_to_vector would prepend the
    emulator argv); case desktops must keep Terminal null/false.
  - X-GIO-NoFuse IS read (gdesktopappinfo.c:2021, :2599-2601): when true, the
    force_file_uri step is skipped for %u/%U and they pass the URI form.
  - g_key_file_get_boolean/lenient string reads swallow bad escapes (Name/Icon
    read as absent, Terminal/Hidden read false); only Type/Path/Exec escapes are
    load-refusing (gdesktopappinfo.c:1917-1985 with is_invalid_key_error).
  - the %-walk is byte-wise on the raw Exec value: a multi-byte UTF-8
    character after '%' loses its lead byte (consumed as an unknown selector)
    and its trailing bytes stay in the output (measured).
  - a spawn failure (e.g. expanded argv[0] not executable) is outside the cause
    taxonomy; the model answers parse+expansion only.
Structural: stdlib only (sys, json, re, tempfile, shutil); no subprocess, no
socket, no ctypes; the only file reads are the DESKTOP bytes given on the
command line (and selftest fixtures it wrote itself under tempfile.mkdtemp()).
"""

import json
import os
import re
import shutil
import sys
import tempfile

PROG = 'MADO_EXECARGV'

# g_key_file escapes (desktop-entry spec): \s \n \t \r \\ ; anything else refuses
# when the key is read with an error check (measured: a\z in Exec -> load refusal).
VALUE_ESCAPES = {'s': ' ', 'n': '\n', 't': '\t', 'r': '\r', '\\': '\\'}
# g_ascii_isspace bit set (gstrfuncs.c:262-282): TAB LF FF CR SPACE, no VT.
KEYFILE_WS = '\t\n\x0c\r '
DESKTOP_GROUP = 'Desktop Entry'
APP_TYPE = 'Application'
URI_SCHEME_RE = re.compile(r'^[A-Za-z][A-Za-z0-9+.\-]*:')


def decode_desktop(data):
    return data.decode('utf-8', 'surrogateescape')


def valid_key_name(key):
    base = key
    if '[' in key:
        if not key.endswith(']'):
            return False
        i = key.find('[')
        base, loc = key[:i], key[i + 1:-1]
        if loc == '':
            return False
        for ch in loc:
            if ch in '[]=' or ch in KEYFILE_WS:
                return False
            if not (ch.isascii() and (ch.isalnum() or ch in '-_.@')):
                return False
    if base == '':
        return False
    for ch in base:
        if not (ch.isascii() and (ch.isalnum() or ch == '-')):
            return False
    return True


def unescape_value(raw):
    """GKeyFile value unescape; (ok, text). Unknown or dangling escape -> not ok."""
    out = []
    i = 0
    n = len(raw)
    while i < n:
        c = raw[i]
        if c == '\\':
            i += 1
            if i >= n or raw[i] not in VALUE_ESCAPES:
                return False, None
            out.append(VALUE_ESCAPES[raw[i]])
            i += 1
        else:
            out.append(c)
            i += 1
    return True, ''.join(out)


def parse_desktop(text):
    """Whole-file GKeyFile grammar scan; records the FIRST group's keys (last wins).

    Returns {'group': name-or-None, 'values': dict, 'error': None|'grammar'|'early-key'}.
    Measured: key line before any group refuses (gkeyfile 'does not start with a
    group'); a duplicate key keeps the LAST occurrence (oracle probe dup); CRLF,
    whitespace-only lines and comments are tolerated; escapes are validated when
    a key is read, not at load.
    """
    group = None
    current = None
    values = {}
    error = None
    for raw in text.split('\n'):
        line = raw[:-1] if raw.endswith('\r') else raw
        if line.strip(KEYFILE_WS) == '':
            continue
        # GKeyFile skips leading whitespace on every line before classification
        # (gkeyfile.c:1687-1696): an indented '# ...' is a comment, and indented
        # group/key lines classify like flush-left ones (oracle-measured:
        # '  # indented comment' launches).
        line = line.lstrip(KEYFILE_WS)
        if line[0] == '#':
            continue
        if line[0] == '[':
            end = line.find(']')
            if end < 0:
                error = 'grammar'
                break
            name = line[1:end]
            if group is None:
                group = name
            current = name
            continue
        eq = line.find('=')
        if eq < 0:
            error = 'grammar'
            break
        key = line[:eq].strip(KEYFILE_WS)
        value = line[eq + 1:].strip(KEYFILE_WS)
        if not valid_key_name(key):
            error = 'grammar'
            break
        if current is None:
            error = 'early-key'
            break
        if current == group:
            values[key] = value
    return {'group': group, 'values': values, 'error': error}


def shell_quote(s):
    return "'" + s.replace("'", "'\\''") + "'"


def g_dirname(p):
    t = p.rstrip('/')
    if t == '':
        return '/'
    i = t.rfind('/')
    if i < 0:
        return '.'
    if i == 0:
        return '/'
    return t[:i]


def g_basename(p):
    t = p.rstrip('/')
    if t == '':
        return '/'
    i = t.rfind('/')
    return t[i + 1:] if i >= 0 else t


def pct_decode(s):
    """Percent-decode bytes then UTF-8/surrogateescape (g_filename_from_uri shape)."""
    buf = bytearray()
    i = 0
    n = len(s)
    hexd = '0123456789abcdefABCDEF'
    while i < n:
        c = s[i]
        if c == '%' and i + 2 < n and s[i + 1] in hexd and s[i + 2] in hexd:
            buf.append(int(s[i + 1:i + 3], 16))
            i += 3
        else:
            buf.extend(c.encode('utf-8', 'surrogateescape'))
            i += 1
    return buf.decode('utf-8', 'surrogateescape')


def arg_model(raw):
    """One gio-launch argument -> (uri_string_seen_by_expand_macro, local_path_or_None).

    g_file_new_for_commandline_arg + g_file_get_uri (gio-tool-launch.c:106): a
    local path becomes a file URI (never carrying '#' or '?'); a file URI's
    fragment AND query are dropped before expansion, so the expand_macro_uri
    '#' bypass is unobservable for local arguments and the query never reaches
    the path (both measured: %u file:///x#frag and file:///a%20b.txt?x#f pass
    the decoded path without the anchor/query).
    """
    m = URI_SCHEME_RE.match(raw)
    if m is None:
        return (local_uri_of(raw), raw)
    if not raw.startswith('file://'):
        return (raw, None)
    rest = raw[len('file://'):]
    slash = rest.find('/')
    netloc = rest if slash < 0 else rest[:slash]
    if netloc not in ('', 'localhost'):
        return (raw, None)
    pathpart = '' if slash < 0 else rest[slash:]
    h = pathpart.find('#')
    if h >= 0:
        pathpart = pathpart[:h]
    q = pathpart.find('?')
    if q >= 0:
        pathpart = pathpart[:q]
    local = pct_decode(pathpart)
    return (local_uri_of(local), local)


def local_uri_of(path):
    """file URI a local path maps to; '#' is escaped so the force-bypass never fires."""
    return 'file://' + path.replace('%', '%25').replace('#', '%23')


def expand_single(code, uri, local):
    """expand_macro_single (gdesktopappinfo.c:2506-2555)."""
    if code in 'uU':
        return shell_quote(uri)
    if local is None:
        return None
    if code in 'fF':
        return shell_quote(local)
    if code in 'dD':
        return shell_quote(g_dirname(local))
    return shell_quote(g_basename(local)) if code in 'nN' else None


def expand_macro_uri(code, uri, local, force_file_uri):
    """expand_macro_uri (gdesktopappinfo.c:2556-2578): force path for %u/%U unless '#'
    or X-GIO-NoFuse.

    Measured: the '#' branch is unreachable for local arguments because the gio
    tool drops the fragment first; it stays live for non-local schemes where the
    fallback yields the URI either way. With X-GIO-NoFuse=true (:2599-2601) the
    force step is skipped and %u/%U pass the URI form.
    """
    if not force_file_uri or '#' in uri:
        return expand_single(code, uri, local)
    forced = expand_single({'u': 'f', 'U': 'F'}[code], uri, local)
    if forced is None:
        return expand_single(code, uri, local)
    return forced


def build_launches(exec_line, name, icon, desktop_path, raw_args, no_fuse=False):
    """The do/while loop (gdesktopappinfo.c:3002-3021) + the '%'-walk (2700-2746).

    Returns (launches, None) or (None, parse-error-kind). The walk is BYTE-WISE
    on the raw Exec value like the C code: the selector is one byte, so a
    multi-byte UTF-8 character after '%' loses its lead byte (consumed as an
    unknown selector) and its trailing bytes stay in the output (measured).
    The rule-4 fallback triggers on head-pointer equality, so a non-consuming
    macro (%c, %i, %%, unknown) still triggers it.
    """
    args = [arg_model(a) for a in raw_args]
    state = {'consumed': False}
    out = bytearray()

    def macro(code):
        if code in 'fudn':
            if not args:
                return
            uri, local = args.pop(0)
            expanded = expand_macro_uri(code, uri, local, code in 'uU' and not no_fuse)
            if expanded is not None:
                out.extend(expanded.encode('utf-8', 'surrogateescape'))
            state['consumed'] = True
        elif code in 'FUDN':
            while args:
                uri, local = args.pop(0)
                expanded = expand_macro_uri(code, uri, local, code in 'uU' and not no_fuse)
                more = bool(args)
                if expanded is not None:
                    out.extend(expanded.encode('utf-8', 'surrogateescape'))
                    if more:
                        out.extend(b' ')
                state['consumed'] = True
        elif code == 'i':
            if icon is not None:
                out.extend(b'--icon ')
                out.extend(shell_quote(icon).encode('utf-8', 'surrogateescape'))
        elif code == 'c':
            if name is not None:
                out.extend(shell_quote(name).encode('utf-8', 'surrogateescape'))
        elif code == 'k':
            if desktop_path is not None:
                out.extend(shell_quote(desktop_path).encode('utf-8', 'surrogateescape'))
        elif code == 'm':
            pass
        elif code == '%':
            out.append(0x25)

    launches = []
    while True:
        del out[:]
        state['consumed'] = False
        exec_bytes = exec_line.encode('utf-8', 'surrogateescape')
        i = 0
        n = len(exec_bytes)
        while i < n:
            if exec_bytes[i] == 0x25 and i + 1 < n:
                macro(chr(exec_bytes[i + 1]))
                i += 2
            else:
                out.append(exec_bytes[i])
                i += 1
        if not state['consumed'] and args:
            out.append(0x20)
            macro('f')
        argv, err = shell_parse_argv(bytes(out).decode('utf-8', 'surrogateescape'))
        if argv is None:
            return None, err
        launches.append(argv)
        if not args:
            return launches, None


def tokenize_command_line(s):
    """Port of tokenize_command_line (gshell.c:433-585); tokens keep quote bytes.

    Returns (tokens, None) or (None, error-kind). Backslash state keeps the
    backslash+char pair for the later unquote; '#' after line start/space/newline
    opens a comment eaten to end of line; '\n' delimits; tab/space delimit a
    non-empty token; consecutive backslashes toggle the escaped-quote flag.
    """
    tokens = []
    cur = []
    state = {'quote': '', 'quoted': False, 'hash_at': -1}

    def delimit():
        if cur:
            tokens.append(''.join(cur))
            del cur[:]

    for idx, ch in enumerate(s):
        quote = state['quote']
        if quote == '\\':
            if ch != '\n':
                cur.append('\\')
                cur.append(ch)
            state['quote'] = ''
        elif quote == '#':
            if ch == '\n':
                state['quote'] = ''
            continue
        elif quote:
            if ch == quote and not (quote == '"' and state['quoted']):
                state['quote'] = ''
            cur.append(ch)
        elif ch == '\n':
            delimit()
        elif ch in ' \t':
            if cur:
                delimit()
        elif ch in '\'"':
            cur.append(ch)
            state['quote'] = ch
        elif ch == '\\':
            state['quote'] = '\\'
        elif ch == '#':
            if idx == 0 or s[idx - 1] in (' ', '\n'):
                state['quote'] = '#'
                state['hash_at'] = idx
                continue
            cur.append(ch)
        else:
            cur.append(ch)
        state['quoted'] = (not state['quoted']) if ch == '\\' else False
    delimit()
    if state['quote'] == '#':
        # glib's comment state consumes to EOF and resets; only a '#' that is the
        # final character (comment state never entered) leaves the error behind.
        if state['hash_at'] == len(s) - 1:
            return None, 'comment-at-eof'
        state['quote'] = ''
    if state['quote']:
        if state['quote'] == '\\':
            return None, 'trailing-backslash'
        if state['quote'] == '#':
            return None, 'comment-at-eof'
        return None, 'unterminated-quote'
    if not tokens:
        return None, 'empty'
    return tokens, None


def unquote_token(t):
    """Port of g_shell_unquote (gshell.c:261-317) + unquote_string_inplace."""
    out = []
    i = 0
    n = len(t)
    while i < n:
        while i < n and t[i] not in '"\'':
            c = t[i]
            if c == '\\':
                i += 1
                if i < n:
                    if t[i] != '\n':
                        out.append(t[i])
                    i += 1
            else:
                out.append(c)
                i += 1
        if i >= n:
            break
        q = t[i]
        i += 1
        closed = False
        while i < n:
            c = t[i]
            if q == "'":
                if c == "'":
                    i += 1
                    closed = True
                    break
                out.append(c)
                i += 1
            else:
                if c == '"':
                    i += 1
                    closed = True
                    break
                if c == '\\':
                    i += 1
                    if i >= n:
                        return None
                    nxt = t[i]
                    if nxt in '"\\`$\n':
                        out.append(nxt)
                        i += 1
                    else:
                        out.append('\\')
                else:
                    out.append(c)
                    i += 1
        if not closed:
            return None
    return ''.join(out)


def shell_parse_argv(s):
    """Port of g_shell_parse_argv (gshell.c:657-690): tokenize, then unquote each."""
    tokens, err = tokenize_command_line(s)
    if tokens is None:
        return None, err
    argv = []
    for t in tokens:
        v = unquote_token(t)
        if v is None:
            return None, 'unmatched-quote'
        argv.append(v)
    return argv, None


def lenient_value(raw):
    """Name/Icon read path: a bad escape makes the key read as absent (NULL, NULL)."""
    if raw is None:
        return None
    ok, value = unescape_value(raw)
    return value if ok else None


def locale_language_list():
    """Simplified g_get_language_names from LC_ALL > LC_MESSAGES > LANG (default C):
    the full name first, then without codeset/modifier, then bare language, then
    'C' last. 'C*' reduces to ['C']. Modifier variants are not expanded."""
    raw = (os.environ.get('LC_ALL') or os.environ.get('LC_MESSAGES')
           or os.environ.get('LANG') or 'C')
    base = raw.split('@')[0]
    if base == 'C' or base == '':
        return ['C']
    out = [raw]
    stem = base.split('.')[0]
    for piece in (stem, stem.split('_')[0]):
        if piece and piece not in out:
            out.append(piece)
    if 'C' not in out:
        out.append('C')
    return out


def locale_selected(values, key):
    """g_key_file_get_locale_string(key, locale=NULL) (:2010-2012): try
    `key[<lang>]` for each current-locale name, else the plain key."""
    for lang in locale_language_list():
        raw = values.get(key + '[' + lang + ']')
        if raw is not None:
            return lenient_value(raw)
    return lenient_value(values.get(key))


def desktop_k_path(desktop_path):
    """gio launch resolves the desktop argument against its CWD before
    new_from_filename, so %k is the absolute (CWD-joined) path; no '..' or
    symlink resolution (g_file_get_path does none)."""
    if desktop_path.startswith('/'):
        return desktop_path
    return os.path.join(os.getcwd(), desktop_path)


def strip_icon_ext(name):
    """gdesktopappinfo.c:2044-2055 workaround: for a NON-absolute Icon value, a
    trailing .png/.xpm/.svg (case sensitive, at the LAST dot) is cut before %i
    uses it. Absolute icon paths are GFileIcons and keep their extension
    (measured: Icon=/tmp/ic.png -> --icon /tmp/ic.png)."""
    if name is None or name.startswith('/'):
        return name
    i = name.rfind('.')
    if i >= 0 and name[i:] in ('.png', '.xpm', '.svg'):
        return name[:i]
    return name


def bool_value(raw):
    """g_key_file_get_boolean: 'true' (case-insensitive) true, bad/other false."""
    if raw is None:
        return False
    ok, value = unescape_value(raw)
    return ok and value.lower() == 'true'


def run(desktop_path, file_args):
    """Full model: load refusals then the launch sequence. Dict result."""
    try:
        with open(desktop_path, 'rb') as fh:
            data = fh.read()
    except OSError:
        return {'error': 'desktop-file', 'detail': 'unreadable'}
    text = decode_desktop(data)
    d = parse_desktop(text)
    if d['error'] == 'early-key':
        return {'error': 'desktop-file', 'detail': 'key-before-group'}
    if d['error'] == 'grammar':
        return {'error': 'desktop-file', 'detail': 'grammar'}
    if d['group'] != DESKTOP_GROUP:
        return {'error': 'desktop-file', 'detail': 'no-desktop-entry-group'}
    vals = d['values']
    type_ok, type_v = (unescape_value(vals['Type']) if 'Type' in vals else (True, None))
    if not type_ok:
        return {'error': 'desktop-file', 'detail': 'bad-escape-type'}
    if type_v != APP_TYPE:
        return {'error': 'desktop-file', 'detail': 'type'}
    if 'Path' in vals and not unescape_value(vals['Path'])[0]:
        return {'error': 'desktop-file', 'detail': 'bad-escape-path'}
    if 'Exec' in vals:
        exec_ok, exec_v = unescape_value(vals['Exec'])
        if not exec_ok:
            return {'error': 'desktop-file', 'detail': 'bad-escape-exec'}
    else:
        exec_v = None
    if exec_v is None:
        return {'error': 'no-exec', 'detail': 'missing-exec'}
    if exec_v != '':
        static, _err = shell_parse_argv(exec_v)
        if static is None:
            return {'error': 'exec-parse', 'detail': 'static'}
    launches, err = build_launches(
        exec_v,
        locale_selected(vals, 'Name'),
        strip_icon_ext(locale_selected(vals, 'Icon')),
        desktop_k_path(desktop_path),
        list(file_args),
        bool_value(vals.get('X-GIO-NoFuse')),
    )
    if launches is None:
        return {'error': 'exec-parse', 'detail': err}
    return {'launches': len(launches), 'argv': launches}


def selftest():
    """Fixture checks under tempfile.mkdtemp(); green -> checks=N failed=0."""
    results = []

    def check(cid, got, want):
        results.append((cid, got == want))

    base = tempfile.mkdtemp(prefix='mado-execargv-selftest-')
    try:
        probe = base + '/probe.sh'

        def desk(name, exec_line, extra=()):
            lines = ['[Desktop Entry]', 'Type=Application', 'Name=Demo App']
            if exec_line is not None:
                lines.append('Exec=' + exec_line)
            lines.extend(extra)
            return desk_raw(name, lines)

        def desk_raw(name, lines):
            path = base + '/' + name + '.desktop'
            with open(path, 'w', encoding='utf-8', errors='surrogateescape') as fh:
                fh.write('\n'.join(lines) + '\n')
            return path

        f1 = base + '/a.txt'
        f2 = base + '/b.txt'
        f3 = base + '/c.txt'
        sp = base + '/a b.txt'

        check('st-plain-one', run(desk('p1', probe), [f1]),
              {'launches': 1, 'argv': [[probe, f1]]})
        check('st-plain-argless', run(desk('p0', probe), []),
              {'launches': 1, 'argv': [[probe]]})
        check('st-default-f-two-launches', run(desk('p2', probe), [f1, f2]),
              {'launches': 2, 'argv': [[probe, f1], [probe, f2]]})
        check('st-f-one-per-launch', run(desk('f2', probe + ' %f'), [f1, f2]),
              {'launches': 2, 'argv': [[probe, f1], [probe, f2]]})
        check('st-f-drain', run(desk('F3', probe + ' %F'), [f1, f2, f3]),
              {'launches': 1, 'argv': [[probe, f1, f2, f3]]})
        check('st-f-f-pairs', run(desk('ff', probe + ' %f %f'), [f1, f2, f3]),
              {'launches': 2, 'argv': [[probe, f1, f2], [probe, f3]]})
        check('st-u-file-path', run(desk('uf', probe + ' %u'), [sp]),
              {'launches': 1, 'argv': [[probe, sp]]})
        check('st-u-remote-uri', run(desk('ur', probe + ' %u'), ['http://x/y']),
              {'launches': 1, 'argv': [[probe, 'http://x/y']]})
        check('st-u-anchor-file-path', run(desk('ua', probe + ' %u'), ['file:///x/a.txt#frag']),
              {'launches': 1, 'argv': [[probe, '/x/a.txt']]})
        check('st-u-query-drop', run(desk('uq', probe + ' %u'), ['file:///x/a%20b.txt?y#f']),
              {'launches': 1, 'argv': [[probe, '/x/a b.txt']]})
        check('st-U-mixed-order', run(desk('Um', probe + ' %U'), [f1, 'http://x/y']),
              {'launches': 1, 'argv': [[probe, f1, 'http://x/y']]})
        check('st-d-dirname', run(desk('dd', probe + ' %d'), [f1]),
              {'launches': 1, 'argv': [[probe, base]]})
        check('st-n-basename', run(desk('nn', probe + ' %n'), [f1]),
              {'launches': 1, 'argv': [[probe, 'a.txt']]})
        check('st-i-icon', run(desk('ii', probe + ' %i', extra=('Icon=demo-icon',)), []),
              {'launches': 1, 'argv': [[probe, '--icon', 'demo-icon']]})
        check('st-i-icon-ext', run(desk('ie', probe + ' %i', extra=('Icon=ic.png',)), []),
              {'launches': 1, 'argv': [[probe, '--icon', 'ic']]})
        check('st-i-icon-space-kept', run(desk('is', probe + ' %i', extra=('Icon=my icon.xpm',)), []),
              {'launches': 1, 'argv': [[probe, '--icon', 'my icon']]})
        check('st-i-noicon', run(desk('in', probe + ' %i'), [f1]),
              {'launches': 1, 'argv': [[probe, f1]]})
        check('st-i-empty-icon', run(desk('ie2', probe + ' %i', extra=('Icon=',)), []),
              {'launches': 1, 'argv': [[probe, '--icon', '']]})
        check('st-i-icon-abs', run(desk('ia2', probe + ' %i', extra=('Icon=/tmp/ic.png',)), []),
              {'launches': 1, 'argv': [[probe, '--icon', '/tmp/ic.png']]})
        check('st-byte-walk', run(desk('bw', probe + ' 100%\u00e9'), []),
              {'launches': 1, 'argv': [[probe, '100\udca9']]})
        check('st-nofuse-u-uri', run(desk('nf', probe + ' %u',
              extra=('X-GIO-NoFuse=true',)), [f1]),
              {'launches': 1, 'argv': [[probe, 'file://' + f1]]})
        saved_env = {k: os.environ.get(k) for k in ('LC_ALL', 'LC_MESSAGES', 'LANG')}
        try:
            os.environ['LC_ALL'] = 'en_US.UTF-8'
            for k in ('LC_MESSAGES', 'LANG'):
                os.environ.pop(k, None)
            check('st-locale-name', run(
                desk_raw('lc', ['[Desktop Entry]', 'Type=Application',
                                'Name=Demo App', 'Name[en_US]=Bonjour',
                                'Exec=' + probe + ' %c']), []),
                {'launches': 1, 'argv': [[probe, 'Bonjour']]})
        finally:
            for k, v in saved_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        check('st-plain-locale-c', run(desk('lc2', probe + ' %c'), []),
              {'launches': 1, 'argv': [[probe, 'Demo App']]})
        check('st-c-name', run(desk('cc', probe + ' %c'), []),
              {'launches': 1, 'argv': [[probe, 'Demo App']]})
        check('st-k-desktop-path', run(desk('kk', probe + ' %k'), []),
              {'launches': 1, 'argv': [[probe, base + '/kk.desktop']]})
        check('st-pct-double', run(desk('pc', probe + ' 100%% %f'), [f1]),
              {'launches': 1, 'argv': [[probe, '100%', f1]]})
        check('st-pct-trailing', run(desk('pt', probe + ' 100%'), []),
              {'launches': 1, 'argv': [[probe, '100%']]})
        check('st-unknown-code-dropped', run(desk('uz', probe + ' %z'), [f1]),
              {'launches': 1, 'argv': [[probe, f1]]})
        check('st-quote-tokens', run(
            desk('qq', probe + " 'a b' \"c\\\\\"d\" x\\\\y %f"), [f1]),
            {'launches': 1, 'argv': [[probe, 'a b', 'c"d', 'xy', f1]]})
        check('st-quote-unterminated', run(desk('qu', probe + " 'oops"), [f1]),
              {'error': 'exec-parse', 'detail': 'static'})
        check('st-hash-comment-cut', run(desk('hc', probe + ' arg # tail %f'), [f1]),
              {'launches': 1, 'argv': [[probe, 'arg']]})
        check('st-dup-key-last-wins', run(
            desk('dk', probe + ' %c', extra=('Exec=' + probe + ' %k',)), [f1]),
            {'launches': 1, 'argv': [[probe, base + '/dk.desktop', f1]]})
        check('st-noexec-refusal', run(desk('nx', None), [f1]),
              {'error': 'no-exec', 'detail': 'missing-exec'})
        check('st-desktopfile-type', run(
            desk_raw('ty', ['[Desktop Entry]', 'Type=Link', 'Name=D', 'Exec=' + probe]), [f1]),
            {'error': 'desktop-file', 'detail': 'type'})
        check('st-desktopfile-escape', run(desk('be', probe + ' a\\z'), [f1]),
              {'error': 'desktop-file', 'detail': 'bad-escape-exec'})
        check('st-desktopfile-group', run(
            desk_raw('ng', ['[Other]', 'Type=Application', 'Exec=' + probe]), [f1]),
            {'error': 'desktop-file', 'detail': 'no-desktop-entry-group'})
        check('st-desktopfile-earlykey', run(
            desk_raw('ek', ['Exec=' + probe, '[Desktop Entry]', 'Type=Application']), [f1]),
            {'error': 'desktop-file', 'detail': 'key-before-group'})
        check('st-indent-comment', run(
            desk_raw('ic2', ['[Desktop Entry]', '  # indented comment',
                             'Type=Application', 'Name=Probe', 'Exec=' + probe + ' %f']), [f1]),
            {'launches': 1, 'argv': [[probe, f1]]})
    finally:
        shutil.rmtree(base, True)
    failed = [cid for cid, ok in results if not ok]
    for cid in failed:
        sys.stdout.write('%s_SELFTEST_FAIL: %s\n' % (PROG, cid))
    sys.stdout.write('%s_SELFTEST: checks=%d failed=%d\n' % (PROG, len(results), len(failed)))
    sys.stdout.flush()
    return 1 if failed else 0


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='surrogateescape')
        sys.stderr.reconfigure(encoding='utf-8', errors='surrogateescape')
    except Exception:
        pass
    args = sys.argv[1:]
    if '--selftest' in args:
        return selftest()
    json_mode = '--json' in args
    if json_mode:
        args = [a for a in args if a != '--json']
    if not args:
        sys.stderr.write('usage: mado-execargv.py DESKTOP [FILE...] [--json]\n'
                         '       mado-execargv.py --selftest\n')
        return 2
    result = run(args[0], args[1:])
    if json_mode:
        sys.stdout.write(json.dumps(result) + '\n')
    elif 'error' in result:
        sys.stdout.write('%s: ERROR %s detail=%s\n' % (PROG, result['error'], result['detail']))
    else:
        sys.stdout.write('%s: launches=%d\n' % (PROG, len(result['argv'])))
        for k, launch_argv in enumerate(result['argv'], 1):
            sys.stdout.write('LAUNCH %d: argc=%d\n' % (k, len(launch_argv)))
            for i, value in enumerate(launch_argv):
                sys.stdout.write('ARGV[%d][%d]=%s\n' % (k, i, value))
    sys.stdout.flush()
    return 2 if 'error' in result else 0


if __name__ == '__main__':
    sys.exit(main())
