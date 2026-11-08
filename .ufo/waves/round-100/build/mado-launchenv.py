#!/usr/bin/env python3
"""mado-launchenv.py -- model of the launch spawn environment GIO 2.90.1 builds
around the argv vectors of one desktop entry.

Surface (glib 2.90.1, /usr/bin/gio sha256
d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462):
  R1  the load-gate Exec argv[0] lookup   gdesktopappinfo.c:1976-2004
  R1b the load-gate TryExec lookup        gdesktopappinfo.c:1946-1960
      (order in g_desktop_app_info_load_from_keyfile: group, Type, Path,
      TryExec, Exec)
  R2  terminal table + prepend            gdesktopappinfo.c:2765-2778 (table),
      :2797-2806 (walk), :2814-2830 (prepend); refusal :3027-3032
  R3  post-prepend argv[0] lookup         gdesktopappinfo.c:3053-3084
  R4  spawn working directory             gdesktopappinfo.c:3116-3126
      (g_spawn_async_with_fds(info->path, ...)); empty/absent Path= inherits
  R5  GIO_LAUNCHED_DESKTOP_FILE=info->filename   gdesktopappinfo.c:3036-3040
  R6  g_find_program_for_path             gutils.c:300-500
The argv EXPANSION itself (the %-walk, the quoting, the desktop-file grammar,
the shell parser) is not duplicated here: this tool loads the committed
mado-execargv.py by path (importlib on the sibling file next to this one; the
sibling is never modified or copied) and drives its helpers.

Usage:
  mado-launchenv.py DESKTOP [FILE...] [--path PATH] [--json]
  mado-launchenv.py --selftest

--path PATH is the model of the launching PROCESS's PATH (what `env -i ...
PATH=<case> gio launch` sees); the load gate, the terminal walk and the R3
lookup all use that one string in the real code (load gate: path=NULL ->
getenv; terminal walk and R3: g_environ_getenv(envp, "PATH") with envp = the
process environment for `gio launch`). Without --path the model process's own
PATH is used. PATH unset (no --path and nothing in the environment) falls back
to the gutils.c default "/bin:/usr/bin:." (R6); PATH set but EMPTY walks one
empty entry, i.e. the current directory.

Output on stdout, one block per successful model run:
  MADO_LAUNCHENV: launches=N terminal=<name|-> cwd=<escaped path|->
  LAUNCH k: argc=M terminal=<name|->
  ARGV[k][i]=<escaped>
  ENV[k] GIO_LAUNCHED_DESKTOP_FILE=<escaped path|->
<escaped> values are ASCII-safe: every byte outside printable ASCII becomes
\\xNN and a literal backslash becomes \\\\ (the argv can carry raw newlines or
surrogate-escaped bytes through the Exec escapes, and the text form must stay
line-oriented). terminal= names the known_terminals row that was prepended
(the table name, not the resolved path - the resolved path is ARGV[k][0]).

cwd= is the working directory the spawn would use (R4): the Path= value when
absolute, the process cwd joined to it when relative (what chdir() does), and
the process cwd when Path= is absent or empty (measured: an empty Path=
inherits). GIO_LAUNCHED_DESKTOP_FILE is info->filename = the desktop argument
resolved against the process cwd (same value %k expands to).

--json prints one object
  {"launches":N,"cwd":...,"terminal":...,"argv":[[...]],
   "env":{"GIO_LAUNCHED_DESKTOP_FILE":...}}
with raw (unescaped) strings - terminal null when no terminal was prepended -
or {"error":"<cause>","detail":"..."} on a refusal.

exit 0 on success; 2 on a refusal, one line
  MADO_LAUNCHENV: ERROR <cause> detail=<escaped>
causes: load (a load-gate program lookup failed: detail try-exec or
exec-argv0), no-terminal, program-not-found, cwd-failed (R4: the Path= value
cannot be entered), and the round-98 causes passed through unchanged:
no-exec, desktop-file, exec-parse (with their round-98 details). Exit 3 is a
SETUP_ERROR (the execargv sibling is absent or not importable), never a
refusal - the model answers nothing without its expansion module.

Refusal order follows the C: load-time first (desktop-file, then the TryExec
check, then the Exec check), then per launch expansion (no-exec, exec-parse),
then the terminal walk (no-terminal), then the argv[0] lookup
(program-not-found), then the first spawn (cwd-failed).

Named limits (unchanged from the round-98 argv plane plus this round's):
  - the spawn ORDER of multi-spawn launches is not modelled (the children are
    concurrent; the surface is the count and the per-launch vectors);
  - DBusActivable, the gio-launch-desktop wrapper's own environment scrubbing,
    the portal path and whether the process survives are not modelled;
  - the model never spawns anything. Its filesystem reads are: the DESKTOP
    bytes given on the command line, the executable/directory tests
    g_find_program_for_path performs on candidate paths (R6), and the
    enterability stat of the Path= value (R4) plus the R3 executable test on
    argv[0] - all read-only, all of values named by the desktop entry or the
    command line. Locale-keyed reads (Name/Icon) read LC_ALL/LC_MESSAGES/LANG
    from the model process's environment, so a counter must run this tool
    under the same locale environment as the gio oracle call.
Structural: stdlib only (importlib.util, json, os, shutil, sys, tempfile);
no subprocess, no socket, no network, no ctypes.
"""

import importlib.util
import json
import os
import shutil
import sys
import tempfile

PROG = 'MADO_LAUNCHENV'
SIBLING_NAME = 'mado-execargv.py'
EXIT_OK = 0
EXIT_REFUSAL = 2
EXIT_SETUP = 3

# prepend_terminal_to_vector's known_terminals (gdesktopappinfo.c:2765-2778),
# in table order; second field is the exec_arg (None = no option argument).
KNOWN_TERMINALS = (
    ('xdg-terminal-exec', None),
    ('kgx', '-e'),
    ('gnome-terminal', '--'),
    ('mate-terminal', '-x'),
    ('xfce4-terminal', '-x'),
    ('tilix', '-e'),
    ('konsole', '-e'),
    ('nxterm', '-e'),
    ('color-xterm', '-e'),
    ('rxvt', '-e'),
    ('dtterm', '-e'),
    ('xterm', '-e'),
)

# gutils.c:409-421: PATH unset in the environment -> this search path.
DEFAULT_SEARCH_PATH = '/bin:/usr/bin:.'

# Sentinel for run(path_env=...): read the model process's own PATH, exactly
# like the C getenv() calls do. A plain str (possibly '') is used verbatim;
# None models an unset PATH.
PROCESS_PATH = object()


def sibling_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), SIBLING_NAME)


def load_execargv(path=None):
    """Load the committed expansion module from its file path (importlib).

    Returns (module, None) or (None, (name, detail)). The sibling file is only
    ever read, never modified and never copied.
    """
    path = sibling_path() if path is None else path
    if not os.path.isfile(path):
        return None, ('execargv-missing', path)
    try:
        spec = importlib.util.spec_from_file_location('mado_execargv_sibling', path)
    except Exception as exc:  # pragma: no cover - defensive
        return None, ('execargv-spec', '%s: %s' % (path, exc))
    if spec is None or spec.loader is None:
        return None, ('execargv-spec', path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as exc:
        return None, ('execargv-import', '%s: %s' % (path, exc))
    return mod, None


def _is_abs(p):
    """g_path_is_absolute on Unix: the path starts with '/'."""
    return p.startswith('/')


def _join2(a, b):
    """g_build_filename(a, b, NULL) (glib/gfileutils.c): a separator is
    inserted only when the accumulator is non-empty and neither side already
    carries one at the seam; an empty first element vanishes."""
    out = a
    if out and not out.endswith('/') and not b.startswith('/'):
        out += '/'
    return out + b


def _exec_file(p):
    """g_file_test(p, IS_EXECUTABLE) && !g_file_test(p, IS_DIR): access(2)
    X_OK, with directories excluded even though they carry the x bit."""
    return os.access(p, os.X_OK) and not os.path.isdir(p)


def find_program(program, path, working_dir):
    """Port of g_find_program_for_path (gutils.c:300-500). `path` is the model
    of the process PATH (None = unset -> the /bin:/usr/bin:. default). Returns
    the found path (absolute: an absolute hit as-is, a relative hit joined to
    the process cwd) or None.

    Exact behaviour kept, including the fall-throughs:
      - a non-absolute program is first joined to working_dir when given
        (:345-350) - but that joined value only gets the direct executable
        test when it is absolute or the ORIGINAL program contained '/';
        otherwise the walk below runs on the original name;
      - an absolute original that fails the test returns NULL without walking
        (:373-378);
      - the walk: empty entries mean the current directory (the bare name),
        each candidate gets '/'+program appended exactly once, a RELATIVE
        candidate is joined to working_dir AGAIN (:479-482), and a relative
        hit is returned absolute against the process cwd (:489-496).
    """
    original_program = program
    if working_dir is not None and not _is_abs(program):
        program = _join2(working_dir, program)
    if _is_abs(program) or '/' in original_program:
        if _exec_file(program):
            if _is_abs(program):
                return program
            return _join2(os.getcwd(), program)
        if _is_abs(original_program):
            return None
    program = original_program
    if path is None:
        path = DEFAULT_SEARCH_PATH
    i = 0
    n = len(path)
    while True:
        j = path.find(':', i)
        end = n if j < 0 else j
        entry = path[i:end]
        if entry == '':
            startp = program
        else:
            startp = entry + '/' + program
        if working_dir is not None and not _is_abs(startp):
            startp = _join2(working_dir, startp)
        if _exec_file(startp):
            if _is_abs(startp):
                return startp
            return _join2(os.getcwd(), startp)
        if j < 0:
            break
        i = j + 1
    return None


def _child_cwd(wd):
    """The spawn's working directory (R4): an absolute Path= as-is, a relative
    one resolved against the launcher's cwd (what chdir() does), the launcher
    cwd itself when Path= is absent or empty (measured inherit). The child's
    pwd is the PHYSICAL resolved directory, so the value is normalised the way
    getcwd() after chdir() reports it: a trailing slash vanishes, '.'/'..'
    collapse, a symlinked Path= answers its target (measured)."""
    if not wd:
        return os.getcwd()
    target = wd if _is_abs(wd) else _join2(os.getcwd(), wd)
    try:
        return os.path.realpath(target)
    except OSError:
        return target


def _cwd_enterable(wd):
    """chdir(wd) would succeed: it exists, is a directory (symlinks followed,
    like chdir) and is searchable. An empty/absent Path= is never chdir'ed
    (measured: it inherits the launcher's cwd)."""
    if not wd:
        return True
    return os.path.isdir(wd) and os.access(wd, os.X_OK)


def _canonicalise_arg(a):
    """The path side of g_file_new_for_commandline_arg (gio-tool-launch.c:116,
    gfile.c): every argument becomes a GFile and g_file_get_path answers the
    lexically canonicalised form - a relative argument is joined to the
    process cwd, then //, . and .. collapse and a trailing slash is stripped,
    with NO symlink resolution (all measured against /usr/bin/gio: ./args/a.txt
    and args/../args/a.txt and args//a.txt and args/ and an ABSOLUTE
    args/../args/a.txt all answer <cwd>/args/a.txt; ../<id>/x answers
    <cwd>/x). Scheme-carrying arguments stay in the URI plane (the sibling's
    arg_model); only plain paths are canonicalised here. The same treatment
    applies to the desktop argument (g_canonicalize_filename in the gio tool),
    which is what %k and GIO_LAUNCHED_DESKTOP_FILE answer."""
    joined = a if a.startswith('/') else _join2(os.getcwd(), a)
    parts = joined.split('/')
    out = []
    for part in parts[1:]:
        if part in ('', '.'):
            continue
        if part == '..':
            if out:
                out.pop()
            continue
        out.append(part)
    return '/' + '/'.join(out)


def _resolve_terminal(path_env, working_dir):
    """prepend_terminal_to_vector's walk (:2797-2806): first known terminal
    that g_find_program_for_path finds on PATH (with the working dir), in
    table order. Returns (table_name, found_path, exec_arg) or None."""
    for name, exec_arg in KNOWN_TERMINALS:
        found = find_program(name, path_env, working_dir)
        if found is not None:
            return name, found, exec_arg
    return None


def run(m, desktop_path, file_args, path_env=PROCESS_PATH):
    """Full model for one desktop file. Dict result:
      {'launches': N, 'terminal': name-or-None, 'cwd': absolute str,
       'argv': [[...], ...], 'gdf': str}
    or {'error': cause, 'detail': detail}."""
    if path_env is PROCESS_PATH:
        path_env = os.environ.get('PATH')

    # ---- load time (g_desktop_app_info_load_from_keyfile, order fixed) ----
    try:
        with open(desktop_path, 'rb') as fh:
            data = fh.read()
    except OSError:
        return {'error': 'desktop-file', 'detail': 'unreadable'}
    text = m.decode_desktop(data)
    d = m.parse_desktop(text)
    if d['error'] == 'early-key':
        return {'error': 'desktop-file', 'detail': 'key-before-group'}
    if d['error'] == 'grammar':
        return {'error': 'desktop-file', 'detail': 'grammar'}
    if d['group'] != m.DESKTOP_GROUP:
        return {'error': 'desktop-file', 'detail': 'no-desktop-entry-group'}
    vals = d['values']
    type_ok, type_v = (m.unescape_value(vals['Type']) if 'Type' in vals
                       else (True, None))
    if not type_ok:
        return {'error': 'desktop-file', 'detail': 'bad-escape-type'}
    if type_v != m.APP_TYPE:
        return {'error': 'desktop-file', 'detail': 'type'}
    if 'Path' in vals:
        path_ok, wd = m.unescape_value(vals['Path'])
        if not path_ok:
            return {'error': 'desktop-file', 'detail': 'bad-escape-path'}
    else:
        wd = None
    if 'TryExec' in vals:
        try_ok, try_v = m.unescape_value(vals['TryExec'])
        if not try_ok:
            return {'error': 'desktop-file', 'detail': 'bad-escape-try-exec'}
        # R1b: a non-empty TryExec must resolve (with Path= as working dir)
        # BEFORE the Exec check (:1946-1960).
        if try_v != '' and find_program(try_v, path_env, wd) is None:
            return {'error': 'load', 'detail': 'try-exec'}
    if 'Exec' in vals:
        exec_ok, exec_v = m.unescape_value(vals['Exec'])
        if not exec_ok:
            return {'error': 'desktop-file', 'detail': 'bad-escape-exec'}
    else:
        exec_v = None
    if exec_v is None:
        # refused at launch time in the C (expand_application_parameters:
        # "Desktop file didn't specify Exec field"), same refusal result.
        return {'error': 'no-exec', 'detail': 'missing-exec'}
    if exec_v != '':
        static, _err = m.shell_parse_argv(exec_v)
        if static is None:
            return {'error': 'exec-parse', 'detail': 'static'}
        # R1: the static argv[0] must resolve, with Path= as working dir and
        # the process PATH (:1976-2004). A directory fails the !IS_DIR half.
        if find_program(static[0], path_env, wd) is None:
            return {'error': 'load', 'detail': 'exec-argv0'}

    # ---- launch time (g_desktop_app_info_launch_uris_with_spawn) ----
    # gio converts EVERY argument (and the desktop argument) to a GFile first
    # (gio-tool-launch.c:116 / g_canonicalize_filename): plain relative paths
    # become cwd-resolved canonical absolute paths before any field code sees
    # them (measured); URI arguments stay raw for arg_model's own handling.
    resolved_args = [a if m.URI_SCHEME_RE.match(a) is not None
                     else _canonicalise_arg(a) for a in file_args]
    desktop_resolved = _canonicalise_arg(desktop_path)
    launches, err = m.build_launches(
        exec_v,
        m.locale_selected(vals, 'Name'),
        m.strip_icon_ext(m.locale_selected(vals, 'Icon')),
        desktop_resolved,
        resolved_args,
        m.bool_value(vals.get('X-GIO-NoFuse')),
    )
    if launches is None:
        return {'error': 'exec-parse', 'detail': err}

    terminal = m.bool_value(vals.get('Terminal'))
    term = _resolve_terminal(path_env, wd) if terminal else None
    if terminal and term is None:
        # :3027-3032, per launch - the first launch refuses the whole launch.
        return {'error': 'no-terminal', 'detail': 'no-known-terminal'}
    term_name, term_path, term_arg = term if term is not None else (None, None, None)

    resolved = []
    for launch in launches:
        argv = list(launch)
        if term is not None:
            # :2814-2830: [found_terminal, exec_arg?] + the launch argv.
            argv = [term_path] + ([term_arg] if term_arg is not None else []) + argv
        # R3 (:3053-3084): keep argv[0] only when absolute, executable and not
        # a directory; otherwise look it up (non-absolute only) and replace.
        a0 = argv[0]
        if not _is_abs(a0) or not _exec_file(a0) or os.path.isdir(a0):
            repl = None
            if not _is_abs(a0):
                repl = find_program(a0, path_env, wd)
            if repl is None:
                return {'error': 'program-not-found', 'detail': a0}
            argv[0] = repl
        resolved.append(argv)

    # R4: the first spawn enters info->path; failure aborts the launch.
    if not _cwd_enterable(wd):
        return {'error': 'cwd-failed', 'detail': wd if wd is not None else ''}

    gdf = desktop_resolved
    return {
        'launches': len(resolved),
        'terminal': term_name,
        'cwd': _child_cwd(wd),
        'argv': resolved,
        'gdf': gdf,
    }


def esc(value):
    """ASCII-safe, line-safe escaping for the text form: printable ASCII as-is,
    backslash as \\\\, every other byte as \\xNN (UTF-8/surrogateescape bytes)."""
    out = []
    for b in value.encode('utf-8', 'surrogateescape'):
        c = chr(b)
        if c == '\\':
            out.append('\\\\')
        elif 0x20 <= b <= 0x7e:
            out.append(c)
        else:
            out.append('\\x%02x' % b)
    return ''.join(out)


def result_to_json(result):
    if 'error' in result:
        return {'error': result['error'], 'detail': result['detail']}
    return {
        'launches': result['launches'],
        'cwd': result['cwd'],
        'terminal': result['terminal'],
        'argv': result['argv'],
        'env': {'GIO_LAUNCHED_DESKTOP_FILE': result['gdf']},
    }


def render_text(result):
    if 'error' in result:
        return ['%s: ERROR %s detail=%s' % (PROG, result['error'],
                                            esc(result['detail']))]
    term = result['terminal'] if result['terminal'] is not None else '-'
    lines = ['%s: launches=%d terminal=%s cwd=%s' % (
        PROG, result['launches'], term, esc(result['cwd']))]
    for k, launch_argv in enumerate(result['argv'], 1):
        lines.append('LAUNCH %d: argc=%d terminal=%s' % (k, len(launch_argv), term))
        for i, value in enumerate(launch_argv):
            lines.append('ARGV[%d][%d]=%s' % (k, i, esc(value)))
        gdf = result['gdf']
        lines.append('ENV[%d] GIO_LAUNCHED_DESKTOP_FILE=%s' % (
            k, esc(gdf) if gdf is not None else '-'))
    return lines


def render_json(result):
    return json.dumps(result_to_json(result)) + '\n'


def parse_cli(args):
    """argv -> (desktop, files, path_env, json_mode) or None on usage error.
    --path PATH takes the next argument; --json is a flag; everything else is
    positional (DESKTOP first, then the FILE arguments)."""
    desktop = None
    files = []
    path_env = PROCESS_PATH
    json_mode = False
    i = 0
    while i < len(args):
        a = args[i]
        if a == '--path':
            if i + 1 >= len(args):
                return None
            path_env = args[i + 1]
            i += 2
            continue
        if a == '--json':
            json_mode = True
            i += 1
            continue
        if desktop is None:
            desktop = a
        else:
            files.append(a)
        i += 1
    if desktop is None:
        return None
    return desktop, files, path_env, json_mode


def selftest():
    """Fixture checks under tempfile.mkdtemp(); green -> checks=N failed=0."""
    results = []

    def check(cid, got, want):
        results.append((cid, got, want, got == want))

    mod, setup = load_execargv()
    if mod is None:
        sys.stdout.write('%s_SELFTEST_FAIL: setup-%s (%s)\n'
                         % (PROG, setup[0], setup[1]))
        sys.stdout.write('%s_SELFTEST: checks=1 failed=1\n' % PROG)
        sys.stdout.flush()
        return 1
    m = mod

    base = tempfile.mkdtemp(prefix='mado-launchenv-selftest-')
    saved_cwd = os.getcwd()
    try:
        def mkexec(path, body='#!/bin/sh\n'):
            with open(path, 'w') as fh:
                fh.write(body)
            os.chmod(path, 0o755)

        # fixture tree
        bin_all = base + '/bin-all'      # gnome-terminal, konsole, xterm
        os.makedirs(bin_all)             # (no xdg/kgx: the table's first rows)
        for name in ('gnome-terminal', 'konsole', 'xterm'):
            mkexec(bin_all + '/' + name)
        bin_xdg = base + '/bin-xdg'      # only xdg-terminal-exec
        os.makedirs(bin_xdg)
        mkexec(bin_xdg + '/xdg-terminal-exec')
        bin_xt = base + '/bin-xterm'     # only xterm (plus a loose program
        os.makedirs(bin_xt)              # for the bare argv[1] check)
        mkexec(bin_xt + '/xterm')
        mkexec(bin_xt + '/loose')
        bin_loose = base + '/bin-loose'  # a plain program named 'loose'
        os.makedirs(bin_loose)
        mkexec(bin_loose + '/loose')
        bin_pct = base + '/bin-pct'      # executables literally named '%d' and
        os.makedirs(bin_pct)             # '%f' (load-gate survivors for Exec
        mkexec(bin_pct + '/%d')          # values that START with those macros)
        mkexec(bin_pct + '/%f')
        bin_sub = base + '/bin-sub'      # holds a DIRECTORY named subdir
        os.makedirs(bin_sub + '/subdir')
        appdir = base + '/app'           # working dir with the probe
        os.makedirs(appdir)
        probe = appdir + '/probe.sh'
        mkexec(probe)
        mkexec(appdir + '/xterm')        # a terminal inside the working dir
        work = base + '/work'
        os.makedirs(work + '/app')       # what a wd-joined walk hit resolves to
        mkexec(work + '/app/probe.sh')
        mkexec(base + '/probe.sh')       # the empty-PATH-entry cwd candidate
        plain = base + '/plain.txt'      # exists, not executable
        with open(plain, 'w') as fh:
            fh.write('x\n')
        run1 = base + '/run1'            # executable file argument
        mkexec(run1)
        run2 = base + '/run2'            # non-executable file argument
        with open(run2, 'w') as fh:
            fh.write('x\n')
        f1 = base + '/a.txt'
        f2 = base + '/b.txt'
        for p in (f1, f2):
            with open(p, 'w') as fh:
                fh.write('x\n')
        gone = base + '/missing'         # never created
        nowhere = '/nonexistent-mado-r99'

        def desk(name, exec_line, extra=()):
            lines = ['[Desktop Entry]', 'Type=Application', 'Name=Demo App']
            if exec_line is not None:
                lines.append('Exec=' + exec_line)
            lines.extend(extra)
            path = base + '/' + name + '.desktop'
            with open(path, 'w') as fh:
                fh.write('\n'.join(lines) + '\n')
            return path

        cwd = os.getcwd()
        PNONE = nowhere

        # -- find_program units (R6) --
        check('fp-abs-hit', find_program(probe, None, None), probe)
        check('fp-abs-miss', find_program(gone, None, None), None)
        check('fp-abs-dir', find_program(appdir, None, None), None)
        check('fp-wd-join', find_program('probe.sh', nowhere, appdir),
              probe)
        check('fp-wd-skips-absolute', find_program(probe, None, appdir), probe)
        check('fp-empty-path-with-wd-miss', find_program('nope-xyz', '', appdir),
              None)
        check('fp-walk-order', find_program('xterm', bin_all + ':' + bin_xt, None),
              bin_all + '/xterm')
        check('fp-walk-first-entry', find_program('xterm', bin_xt + ':' + bin_all, None),
              bin_xt + '/xterm')
        check('fp-walk-miss', find_program('xterm', nowhere, None), None)
        check('fp-walk-skips-dirs', find_program('subdir', bin_sub, None), None)
        check('fp-default-path-has-sh', find_program('sh', None, None) is not None,
              True)
        check('fp-default-path-miss', find_program('no-such-prog-r99', None, None),
              None)

        # relative PATH entry + working dir join in the walk
        os.chdir(base)
        try:
            check('fp-rel-slash-cwd-hit', find_program('app/probe.sh', nowhere, None),
                  base + '/app/probe.sh')
            check('fp-rel-slash-miss-falls-to-walk',
                  find_program('no/such-prog', nowhere, None), None)
            check('fp-walk-rel-entry-wd-join',
                  find_program('probe.sh', 'app', 'work'),
                  base + '/work/app/probe.sh')
            check('fp-walk-rel-entry-cwd-hit',
                  find_program('probe.sh', 'app', None),
                  _join2(base, 'app/probe.sh'))
            check('fp-walk-empty-entry-cwd',
                  find_program('probe.sh', ':' + nowhere, None),
                  _join2(base, 'probe.sh'))
            check('fp-default-dot-entry-keeps-dot-slash',
                  find_program('probe.sh', None, None),
                  _join2(base, './probe.sh'))
            check('fp-path-empty-string', find_program('probe.sh', '', None),
                  _join2(base, 'probe.sh'))
            check('fp-wd-empty-pass-through',
                  find_program('app/probe.sh', '', ''),
                  _join2(base, 'app/probe.sh'))
            # -- unset-PATH default (R6: None -> '/bin:/usr/bin:.') vs empty vs '.' --
            # end-to-end at the load gate (run with path_env=None), not only
            # find_program units: the dot entry's argv0 shape {root}/./probe is
            # the measured trap (pd-dot-unset); '' has no '/./' (pd-empty).
            check('st-unset-default-dot-launch',
                  run(m, desk('u1', 'probe.sh'), [f1], None),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[_join2(base, './probe.sh'), f1]],
                   'gdf': base + '/u1.desktop'})
            check('st-empty-string-no-dot',
                  run(m, desk('u2', 'probe.sh'), [f1], ''),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[_join2(base, 'probe.sh'), f1]],
                   'gdf': base + '/u2.desktop'})
            check('st-dot-entry-explicit',
                  run(m, desk('u3', 'probe.sh'), [f1], '.'),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[_join2(base, './probe.sh'), f1]],
                   'gdf': base + '/u3.desktop'})
            check('st-unset-tryexec-privbin-miss',
                  run(m, desk('u4', probe,
                              extra=('TryExec=loose',)), [f1], None),
                  {'error': 'load', 'detail': 'try-exec'})
            check('st-unset-tryexec-dot-hit',
                  run(m, desk('u5', probe,
                              extra=('TryExec=probe.sh',)), [f1], None),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, f1]], 'gdf': base + '/u5.desktop'})
            # -- R1/R1b load gate (end to end) --
            check('st-plain-absolute-kept',
                  run(m, desk('p1', probe), [f1], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, f1]], 'gdf': base + '/p1.desktop'})
            check('st-load-exec-argv0-missing',
                  run(m, desk('l1', gone), [f1], PNONE),
                  {'error': 'load', 'detail': 'exec-argv0'})
            check('st-load-exec-argv0-dir',
                  run(m, desk('l2', appdir), [f1], PNONE),
                  {'error': 'load', 'detail': 'exec-argv0'})
            check('st-load-rel-argv0-nowhere',
                  run(m, desk('l3', 'loose'), [f1], PNONE),
                  {'error': 'load', 'detail': 'exec-argv0'})
            check('st-load-raw-macro-argv0',
                  run(m, desk('l4', '%f'), [f1], PNONE),
                  {'error': 'load', 'detail': 'exec-argv0'})
            check('st-load-rel-path-join-not-searched',
                  run(m, desk('l5', 'probe.sh', extra=('Path=app',)), [f1],
                      PNONE),
                  {'error': 'load', 'detail': 'exec-argv0'})
            check('st-load-tryexec-first',
                  run(m, desk('t1', gone, extra=('TryExec=' + gone + '2',)), [f1],
                      PNONE),
                  {'error': 'load', 'detail': 'try-exec'})
            check('st-load-tryexec-ok-exec-miss',
                  run(m, desk('t2', gone, extra=('TryExec=' + probe,)), [f1], PNONE),
                  {'error': 'load', 'detail': 'exec-argv0'})
            check('st-load-tryexec-empty-skipped',
                  run(m, desk('t3', gone, extra=('TryExec=',)), [f1], PNONE),
                  {'error': 'load', 'detail': 'exec-argv0'})
            check('st-load-tryexec-via-wd',
                  run(m, desk('t4', gone, extra=('TryExec=probe.sh', 'Path=' + appdir)),
                      [f1], PNONE),
                  {'error': 'load', 'detail': 'exec-argv0'})
            check('st-desktop-file-bad-escape-tryexec',
                  run(m, desk('t5', probe, extra=('TryExec=a\\z',)), [f1], PNONE),
                  {'error': 'desktop-file', 'detail': 'bad-escape-try-exec'})
            check('st-desktop-file-bad-escape-path-before-tryexec',
                  run(m, desk('t6', probe, extra=('Path=a\\z', 'TryExec=' + gone)),
                      [f1], PNONE),
                  {'error': 'desktop-file', 'detail': 'bad-escape-path'})

            # -- R2 terminal --
            check('st-terminal-xdg-no-arg',
                  run(m, desk('x1', probe, extra=('Terminal=true',)), [f1], bin_xdg),
                  {'launches': 1,
                   'terminal': 'xdg-terminal-exec', 'cwd': os.getcwd(),
                   'argv': [[bin_xdg + '/xdg-terminal-exec', probe, f1]],
                   'gdf': base + '/x1.desktop'})
            check('st-terminal-xterm-exec-arg',
                  run(m, desk('x2', probe, extra=('Terminal=true',)), [f1], bin_xt),
                  {'launches': 1, 'terminal': 'xterm', 'cwd': os.getcwd(),
                   'argv': [[bin_xt + '/xterm', '-e', probe, f1]],
                   'gdf': base + '/x2.desktop'})
            check('st-terminal-table-order',
                  run(m, desk('x3', probe, extra=('Terminal=true',)), [f1], bin_all),
                  {'launches': 1, 'terminal': 'gnome-terminal', 'cwd': os.getcwd(),
                   'argv': [[bin_all + '/gnome-terminal', '--', probe, f1]],
                   'gdf': base + '/x3.desktop'})
            check('st-terminal-inside-working-dir',
                  run(m, desk('x4', probe, extra=('Terminal=true',
                                                  'Path=' + appdir)), [f1], PNONE),
                  {'launches': 1, 'terminal': 'xterm', 'cwd': appdir,
                   'argv': [[appdir + '/xterm', '-e', probe, f1]],
                   'gdf': base + '/x4.desktop'})
            check('st-no-terminal',
                  run(m, desk('x5', probe, extra=('Terminal=true',)), [f1], PNONE),
                  {'error': 'no-terminal', 'detail': 'no-known-terminal'})
            check('st-terminal-false-explicit',
                  run(m, desk('x6', probe, extra=('Terminal=false',)), [f1], bin_xt),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, f1]], 'gdf': base + '/x6.desktop'})
            check('st-terminal-bad-value-is-false',
                  run(m, desk('x7', probe, extra=('Terminal=sometimes',)), [f1],
                      bin_xt),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, f1]], 'gdf': base + '/x7.desktop'})
            check('st-terminal-every-launch',
                  run(m, desk('x8', probe, extra=('Terminal=true',)), [f1, f2],
                      bin_xt),
                  {'launches': 2, 'terminal': 'xterm', 'cwd': os.getcwd(),
                   'argv': [[bin_xt + '/xterm', '-e', probe, f1],
                            [bin_xt + '/xterm', '-e', probe, f2]],
                   'gdf': base + '/x8.desktop'})
            check('st-terminal-rel-wd-empty-path-entry',
                  run(m, desk('x9', probe, extra=('Terminal=true', 'Path=app')),
                      [f1], ':'),
                  {'launches': 1, 'terminal': 'xterm', 'cwd': appdir,
                   'argv': [[appdir + '/xterm', '-e', probe, f1]],
                   'gdf': base + '/x9.desktop'})

            # -- R3 argv[0] --
            check('st-argv0-relative-replaced',
                  run(m, desk('r1', 'loose', extra=('Path=' + appdir,)), [f1],
                      bin_loose),
                  {'launches': 1, 'terminal': None, 'cwd': appdir,
                   'argv': [[bin_loose + '/loose', f1]],
                   'gdf': base + '/r1.desktop'})
            check('st-argv0-notfound-second-launch',
                  run(m, desk('r2', '%f'), [run1, run2], bin_pct),
                  {'error': 'program-not-found', 'detail': run2})
            check('st-argv0-notfound-dirname',
                  run(m, desk('r3', '%d'), [f1], bin_pct),
                  {'error': 'program-not-found', 'detail': base})
            check('st-argv0-first-launch-ok',
                  run(m, desk('r4', '%f'), [run1], bin_pct),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[run1]], 'gdf': base + '/r4.desktop'})
            check('st-terminal-bare-argv1-kept',
                  run(m, desk('r5', 'loose', extra=('Terminal=true',)), [f1],
                      bin_xt),
                  {'launches': 1, 'terminal': 'xterm', 'cwd': os.getcwd(),
                   'argv': [[bin_xt + '/xterm', '-e', 'loose', f1]],
                   'gdf': base + '/r5.desktop'})
            check('st-order-program-not-found-before-cwd',
                  run(m, desk('r6', '%f', extra=('Path=' + gone,)), [run2],
                      bin_pct),
                  {'error': 'program-not-found', 'detail': run2})

            # -- R4 cwd --
            check('st-cwd-explicit',
                  run(m, desk('c1', probe, extra=('Path=' + work,)), [f1], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': work,
                   'argv': [[probe, f1]], 'gdf': base + '/c1.desktop'})
            check('st-cwd-empty-inherits',
                  run(m, desk('c2', probe, extra=('Path=',)), [f1], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, f1]], 'gdf': base + '/c2.desktop'})
            check('st-cwd-relative',
                  run(m, desk('c3', probe, extra=('Path=work',)), [f1], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': work,
                   'argv': [[probe, f1]], 'gdf': base + '/c3.desktop'})
            check('st-cwd-trailing-slash-resolved',
                  run(m, desk('c7', probe, extra=('Path=work/',)), [f1], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': work,
                   'argv': [[probe, f1]], 'gdf': base + '/c7.desktop'})
            check('st-cwd-dotdot-resolved',
                  run(m, desk('c8', probe, extra=('Path=app/../work',)), [f1],
                      PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': work,
                   'argv': [[probe, f1]], 'gdf': base + '/c8.desktop'})
            check('st-cwd-failed-missing',
                  run(m, desk('c4', probe, extra=('Path=' + gone,)), [f1], PNONE),
                  {'error': 'cwd-failed', 'detail': gone})
            check('st-cwd-failed-not-a-dir',
                  run(m, desk('c5', probe, extra=('Path=' + plain,)), [f1], PNONE),
                  {'error': 'cwd-failed', 'detail': plain})
            check('st-order-terminal-before-spawn',
                  run(m, desk('c6', probe, extra=('Terminal=true',
                                                  'Path=' + gone)), [f1], PNONE),
                  {'error': 'no-terminal', 'detail': 'no-known-terminal'})

            # -- R5 env value (and %k equality) --
            rel = 'g1.desktop'
            with open(base + '/' + rel, 'w') as fh:
                fh.write('[Desktop Entry]\nType=Application\nName=D\nExec='
                         + probe + ' %k\n')
            check('st-gdf-and-k',
                  run(m, rel, [], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, base + '/' + rel]],
                   'gdf': base + '/' + rel})

            # -- round-98 causes passed through --
            check('st-no-exec',
                  run(m, desk('n1', None), [f1], PNONE),
                  {'error': 'no-exec', 'detail': 'missing-exec'})
            check('st-no-exec-before-terminal',
                  run(m, desk('n2', None, extra=('Terminal=true',)), [f1], PNONE),
                  {'error': 'no-exec', 'detail': 'missing-exec'})
            with open(base + '/n3.desktop', 'w') as fh:
                fh.write('[Desktop Entry]\nType=Link\nName=D\nExec=' + probe + '\n')
            check('st-desktop-file-type',
                  run(m, base + '/n3.desktop', [f1], PNONE),
                  {'error': 'desktop-file', 'detail': 'type'})
            check('st-desktop-file-escape',
                  run(m, desk('n4', probe + ' a\\z'), [f1], PNONE),
                  {'error': 'desktop-file', 'detail': 'bad-escape-exec'})
            check('st-desktop-file-unreadable',
                  run(m, base + '/no-such-r99.desktop', [f1], PNONE),
                  {'error': 'desktop-file', 'detail': 'unreadable'})
            check('st-exec-parse-static',
                  run(m, desk('n5', probe + " 'oops"), [f1], PNONE),
                  {'error': 'exec-parse', 'detail': 'static'})
            check('st-exec-parse-empty',
                  run(m, desk('n6', ''), [], PNONE),
                  {'error': 'exec-parse', 'detail': 'empty'})

            # -- argument conversion (g_file_new_for_commandline_arg) --
            check('st-arg-relative-resolved',
                  run(m, desk('ac1', probe + ' %f'), ['a.txt'], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, f1]], 'gdf': base + '/ac1.desktop'})
            check('st-arg-dot-consumed',
                  run(m, desk('ac2', probe + ' %f'), ['./a.txt'], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, f1]], 'gdf': base + '/ac2.desktop'})
            check('st-arg-dotdot-consumed',
                  run(m, desk('ac3', probe + ' %f'),
                      ['../%s/a.txt' % os.path.basename(base)], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, f1]], 'gdf': base + '/ac3.desktop'})
            check('st-arg-double-slash-collapsed',
                  run(m, desk('ac4', probe + ' %f'), ['app//../a.txt'], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, f1]], 'gdf': base + '/ac4.desktop'})
            check('st-arg-trailing-slash-stripped',
                  run(m, desk('ac5', probe + ' %f'), ['a.txt/'], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, f1]], 'gdf': base + '/ac5.desktop'})
            check('st-arg-absolute-dots-collapsed',
                  run(m, desk('ac6', probe + ' %f'),
                      [base + '/app/../a.txt'], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, f1]], 'gdf': base + '/ac6.desktop'})
            check('st-arg-uri-untouched',
                  run(m, desk('ac7', probe + ' %u'),
                      ['http://x/y?q#f'], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, 'http://x/y?q#f']],
                   'gdf': base + '/ac7.desktop'})
            desk('ac8', probe + ' %k')
            check('st-desktop-arg-canonicalised',
                  run(m, '../%s/ac8.desktop' % os.path.basename(base), [f1],
                      PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, base + '/ac8.desktop', f1]],
                   'gdf': base + '/ac8.desktop'})

            # -- expansion passthrough intact (execargv semantics) --
            check('st-nofuse-u-uri',
                  run(m, desk('e1', probe + ' %u',
                              extra=('X-GIO-NoFuse=true',)), [f1], PNONE),
                  {'launches': 1, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, 'file://' + f1]],
                   'gdf': base + '/e1.desktop'})
            check('st-two-launches-default-f',
                  run(m, desk('e2', probe), [f1, f2], PNONE),
                  {'launches': 2, 'terminal': None, 'cwd': os.getcwd(),
                   'argv': [[probe, f1], [probe, f2]],
                   'gdf': base + '/e2.desktop'})
        finally:
            os.chdir(saved_cwd)

        # -- rendering and CLI units --
        res = {'launches': 2, 'terminal': 'xterm', 'cwd': '/w dir',
               'argv': [['/x/xterm', '-e', '/p', 'a\nb'], ['/x/xterm', '-e', '/p']],
               'gdf': '/d.desktop'}
        text = render_text(res)
        check('render-header', text[0],
              'MADO_LAUNCHENV: launches=2 terminal=xterm cwd=/w dir')
        check('render-launch-lines', (text[1], text[7]),
              ('LAUNCH 1: argc=4 terminal=xterm', 'LAUNCH 2: argc=3 terminal=xterm'))
        check('render-env-lines', (text[6], text[11]),
              ('ENV[1] GIO_LAUNCHED_DESKTOP_FILE=/d.desktop',
               'ENV[2] GIO_LAUNCHED_DESKTOP_FILE=/d.desktop'))
        check('render-esc-newline', text[5], 'ARGV[1][3]=a\\x0ab')
        check('render-esc-backslash', esc('a\\b'), 'a\\\\b')
        check('render-esc-nonascii', esc('caf\xe9'), 'caf\\xc3\\xa9')
        check('render-error-line', render_text(
            {'error': 'no-terminal', 'detail': 'no-known-terminal'}),
            ['MADO_LAUNCHENV: ERROR no-terminal detail=no-known-terminal'])
        obj = json.loads(render_json(res))
        check('json-key-order', list(obj.keys()),
              ['launches', 'cwd', 'terminal', 'argv', 'env'])
        check('json-env-keys', list(obj['env'].keys()),
              ['GIO_LAUNCHED_DESKTOP_FILE'])
        eobj = json.loads(render_json({'error': 'load', 'detail': 'x'}))
        check('json-error-keys', list(eobj.keys()), ['error', 'detail'])
        check('json-terminal-null',
              json.loads(render_json({'launches': 1, 'terminal': None,
                                      'cwd': '/', 'argv': [['/p']],
                                      'gdf': '/d'}))['terminal'], None)
        check('cli-parse-full', parse_cli(['d.desktop', 'a', '--path', '/x:y',
                                           '--json']),
              ('d.desktop', ['a'], '/x:y', True))
        check('cli-parse-default', parse_cli(['d.desktop']),
              ('d.desktop', [], PROCESS_PATH, False))
        check('cli-parse-path-dangling', parse_cli(['d.desktop', '--path']), None)
        check('cli-parse-empty', parse_cli([]), None)
        check('exit-codes', (EXIT_OK, EXIT_REFUSAL, EXIT_SETUP), (0, 2, 3))
        check('setup-missing-named',
              load_execargv('/no-such-dir-r99/mado-execargv.py'),
              (None, ('execargv-missing', '/no-such-dir-r99/mado-execargv.py')))
    finally:
        os.chdir(saved_cwd)
        shutil.rmtree(base, True)
    failed = [(cid, got, want) for (cid, got, want, ok) in results if not ok]
    for cid, got, want in failed:
        sys.stdout.write('%s_SELFTEST_FAIL: %s got=%r want=%r\n'
                         % (PROG, cid, got, want))
    sys.stdout.write('%s_SELFTEST: checks=%d failed=%d\n' % (PROG, len(results),
                                                             len(failed)))
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
    parsed = parse_cli(args)
    if parsed is None:
        sys.stderr.write('usage: mado-launchenv.py DESKTOP [FILE...] [--path PATH]'
                         ' [--json]\n'
                         '       mado-launchenv.py --selftest\n')
        return EXIT_REFUSAL
    desktop, files, path_env, json_mode = parsed
    m, setup = load_execargv()
    if m is None:
        if json_mode:
            sys.stdout.write(json.dumps({'error': 'setup-' + setup[0],
                                         'detail': str(setup[1])}) + '\n')
        else:
            sys.stdout.write('%s: SETUP_ERROR %s detail=%s\n'
                             % (PROG, setup[0], setup[1]))
        sys.stdout.flush()
        return EXIT_SETUP
    result = run(m, desktop, files, path_env)
    if json_mode:
        sys.stdout.write(render_json(result))
    else:
        for line in render_text(result):
            sys.stdout.write(line + '\n')
    sys.stdout.flush()
    return EXIT_REFUSAL if 'error' in result else EXIT_OK


if __name__ == '__main__':
    sys.exit(main())
