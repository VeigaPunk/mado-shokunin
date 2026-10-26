#!/usr/bin/env python3
"""compare.py -- agreement harness for mado-terminal.py against the pinned
xdg-terminal-exec v0.14.3.

For every case the harness
  1. materialises a case root (fixtures: one JSON list, schema below),
  2. runs /usr/bin/xdg-terminal-exec <args> with a cold XDG_CACHE_HOME inside
     the root and PATH=$ROOT/bin:<tool bin> (so no host terminal is found),
  3. runs mado-terminal.py print <args> with the same env, and
  4. requires identical stdout bytes and exit status.

It also runs `explain --observed <real output>` and requires AGREE + exit 0,
checks that the tool creates/modifies no file under the case root, and (when
strace is available) counts execve calls: the tool must not start a process.

Fixture schema (frozen interface):
  {"id", "class", "env", "files", "exec", "args", "expect"}
  expect = {"rc", "stdout"} produced by the real script, "$ROOT" substituted.

Usage: compare.py [--work DIR] [--out DIR] [--nonce N] [--seed S] [--keep]
"""
import argparse
import hashlib
import json
import os
import random
import shutil
import stat
import subprocess
import sys
import tempfile
import time

PIN = '/usr/bin/xdg-terminal-exec'
PIN_SHA256 = '89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac'
TOOLBIN = ('tr', 'find', 'awk', 'ls', 'md5sum', 'mkdir', 'rm')

ASCII_FLAG = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP \
    | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

def entry(exec_='term', categories='System;TerminalEmulator;', execarg='-e',
          extra=(), actions='', name='Term'):
    lines = ['[Desktop Entry]', 'Type=Application', 'Name=' + name]
    if categories is not None:
        lines.append('Categories=' + categories)
    if execarg is not None:
        lines.append('X-TerminalArgExec=' + execarg)
    lines.extend(extra)
    if exec_ is not None:
        lines.append('Exec=' + exec_)
    return '\n'.join(lines) + '\n' + actions


def env(desktop='Hyprland', extra=None):
    e = {
        'XDG_CURRENT_DESKTOP': desktop,
        'XDG_CONFIG_HOME': '$ROOT/home/.config',
        'XDG_CONFIG_DIRS': '$ROOT/etc/xdg',
        'XDG_DATA_HOME': '$ROOT/home/.local/share',
        'XDG_DATA_DIRS': '$ROOT/usr/local/share:$ROOT/usr/share',
        'XDG_CACHE_HOME': '$ROOT/cache',
    }
    if desktop is None:
        del e['XDG_CURRENT_DESKTOP']
    if extra:
        e.update(extra)
    return e


DEFAULT = env()


def mk(cid, cls, files, args, execs=('bin/term',), case_env=None):
    return {'id': cid, 'class': cls, 'env': dict(case_env or DEFAULT),
            'files': files, 'exec': list(execs), 'args': list(args)}


CONFIG = 'home/.config/xdg-terminals.list'
DATA = 'home/.local/share/applications/Term.desktop'
DATA_B = 'home/.local/share/applications/Other.desktop'
SYS = 'usr/share/applications/Term.desktop'
LOCAL = 'usr/local/share/applications/Term.desktop'


def cases_pinned():
    out = []
    A = out.append

    A(mk('base-explicit', 'selection',
         {CONFIG: 'Term.desktop\n', DATA: entry()}, ['--print-id']))
    A(mk('base-fallback', 'selection', {DATA: entry()}, ['--print-id']))
    A(mk('config-lists-absent-id', 'selection',
         {CONFIG: 'Nope.desktop\n', DATA: entry()}, ['--print-id']))
    A(mk('print-path-only', 'print', {DATA: entry()}, ['--print-path']))
    A(mk('print-cmd-only', 'print', {DATA: entry()}, ['--print-cmd']))
    A(mk('print-id-path-cmd', 'print', {DATA: entry()},
         ['--print-id', '--print-path', '--print-cmd']))
    A(mk('print-cmd-args', 'print', {DATA: entry()},
         ['--print-cmd', '--', 'echo', 'hi']))
    A(mk('print-cmd-comma', 'print', {DATA: entry()},
         ['--print-cmd=,', '--', 'echo', 'hi']))
    A(mk('print-cmd-empty-seq', 'print', {DATA: entry()},
         ['--print-cmd=', '--', 'echo', 'hi']))
    A(mk('print-delimiters', 'print', {DATA: entry()},
         ['--print-id', '--print-path', '--print-cmd', '--print-delimiter=|']))
    A(mk('print-content', 'print', {DATA: entry()}, ['--print-content']))
    A(mk('print-content-no-newline', 'print',
         {DATA: entry().rstrip('\n')}, ['--print-content']))
    A(mk('print-content-and-id', 'print', {DATA: entry()},
         ['--print-content', '--print-id']))
    A(mk('print-test', 'print', {DATA: entry()},
         ['--test', '--', 'echo', 'hi']))
    A(mk('print-id-twice', 'print', {DATA: entry()}, ['--print-id', '--print-id']))
    A(mk('print-order-reversed', 'print', {DATA: entry()},
         ['--print-cmd', '--print-id']))
    A(mk('print-unknown-option', 'print', {DATA: entry()},
         ['--nonsense', '--print-id']))
    A(mk('print-help', 'print', {DATA: entry()}, ['--print-id', '-h']))
    A(mk('print-help-long', 'print', {DATA: entry()}, ['--help']))
    A(mk('print-after-dashdash-help', 'print', {DATA: entry()},
         ['--print-id', '--', '--help']))
    A(mk('hidden-true', 'selection',
         {CONFIG: 'Term.desktop\nOther.desktop\n',
          DATA: entry(extra=['Hidden=true']), DATA_B: entry(exec_='term')},
         ['--print-id']))
    A(mk('hidden-True', 'selection',
         {CONFIG: 'Term.desktop\n', DATA: entry(extra=['Hidden=True'])},
         ['--print-id']))
    A(mk('hidden-one', 'selection',
         {CONFIG: 'Term.desktop\n', DATA: entry(extra=['Hidden=1'])},
         ['--print-id']))
    A(mk('categories-missing', 'selection',
         {CONFIG: 'Term.desktop\nOther.desktop\n',
          DATA: entry(categories=None), DATA_B: entry()}, ['--print-id']))
    A(mk('categories-other-only', 'selection',
         {CONFIG: 'Term.desktop\n', DATA: entry(categories='System;Utility;')},
         ['--print-id']))
    A(mk('categories-substring', 'selection',
         {CONFIG: 'Term.desktop\n', DATA: entry(categories='System;TerminalEmulatorX;')},
         ['--print-id']))
    A(mk('tryexec-missing', 'selection',
         {CONFIG: 'Term.desktop\nOther.desktop\n',
          DATA: entry(extra=['TryExec=nope']), DATA_B: entry()}, ['--print-id']))
    A(mk('tryexec-present', 'selection',
         {CONFIG: 'Term.desktop\n', DATA: entry(extra=['TryExec=term'])},
         ['--print-id']))
    A(mk('tryexec-dot-path', 'selection',
         {CONFIG: 'Term.desktop\n', DATA: entry(extra=['TryExec=./bin/term'])},
         ['--print-id']))
    A(mk('exec-missing-binary', 'selection',
         {CONFIG: 'Term.desktop\nOther.desktop\n',
          DATA: entry(exec_='nope'), DATA_B: entry()}, ['--print-id']))
    A(mk('exec-quoted-args', 'exec-parse',
         {CONFIG: 'Term.desktop\n', DATA: entry(exec_='term --class "my term"')},
         ['--print-cmd= ']))
    A(mk('exec-file-field', 'exec-parse',
         {CONFIG: 'Term.desktop\n', DATA: entry(exec_='term --file %f')},
         ['--print-cmd= ']))
    A(mk('exec-two-file-fields', 'exec-parse',
         {CONFIG: 'Term.desktop\nOther.desktop\n',
          DATA: entry(exec_='term %f %U'), DATA_B: entry()}, ['--print-id']))
    A(mk('exec-percent-literal', 'exec-parse',
         {CONFIG: 'Term.desktop\n', DATA: entry(exec_='term a%%b %U')},
         ['--print-cmd= ']))
    A(mk('exec-unknown-field', 'exec-parse',
         {CONFIG: 'Term.desktop\nOther.desktop\n',
          DATA: entry(exec_='term %Z'), DATA_B: entry()}, ['--print-id']))
    A(mk('exec-trailing-percent', 'exec-parse',
         {CONFIG: 'Term.desktop\nOther.desktop\n',
          DATA: entry(exec_='term %'), DATA_B: entry()}, ['--print-id']))
    A(mk('exec-unclosed-quote', 'exec-parse',
         {CONFIG: 'Term.desktop\n', DATA: entry(exec_='term "open')},
         ['--print-cmd= ']))
    A(mk('exec-unquoted-semicolon', 'exec-parse',
         {CONFIG: 'Term.desktop\n', DATA: entry(exec_='term a;b')},
         ['--print-cmd= ']))
    A(mk('exec-empty-value', 'exec-parse',
         {CONFIG: 'Term.desktop\nOther.desktop\n',
          DATA: entry(exec_=''), DATA_B: entry()}, ['--print-id']))
    A(mk('exec-escapes', 'exec-parse',
         {CONFIG: 'Term.desktop\n', DATA: entry(exec_='term\\sa\\tb')},
         ['--print-cmd= ']))
    A(mk('exec-backslash-unknown', 'exec-parse',
         {CONFIG: 'Term.desktop\n', DATA: entry(exec_='term\\qy')},
         ['--print-cmd= ']))
    A(mk('execarg-custom', 'execarg',
         {CONFIG: 'Term.desktop\n', DATA: entry(execarg='-x')},
         ['--print-cmd= ']))
    A(mk('execarg-empty', 'execarg',
         {CONFIG: 'Term.desktop\n', DATA: entry(execarg='')},
         ['--print-cmd= ']))
    A(mk('execarg-escape', 'execarg',
         {CONFIG: 'Term.desktop\n', DATA: entry(execarg='--\\sfoo')},
         ['--print-cmd= ']))
    A(mk('execarg-compat-default', 'execarg',
         {CONFIG: 'Term.desktop\n', DATA: entry(execarg=None)},
         ['--print-cmd= ']))
    A(mk('execarg-strict-reject', 'execarg',
         {CONFIG: '/execarg_strict\nTerm.desktop\n',
          DATA: entry(execarg=None)}, ['--print-id']))
    A(mk('execarg-default-directive', 'execarg',
         {CONFIG: '/execarg_default:Term.desktop:-z\nTerm.desktop\n',
          DATA: entry(execarg=None)}, ['--print-cmd= ']))
    A(mk('execarg-env-pins-mode', 'execarg',
         {CONFIG: '/execarg_compat\nTerm.desktop\n', DATA: entry(execarg=None)},
         ['--print-cmd= '], case_env=env(extra={'XTE_EXECARG_COMPAT': 'false'})))
    A(mk('execarg-env-compat', 'execarg',
         {CONFIG: 'Term.desktop\n', DATA: entry(execarg=None)},
         ['--print-cmd= '], case_env=env(extra={'XTE_EXECARG_COMPAT': 'yes'})))
    A(mk('action-id', 'action',
         {CONFIG: 'Term.desktop:New\n',
          DATA: entry(actions='Actions=New;\n\n[Desktop Action New]\n'
                              'Name=New\nExec=term new\n')},
         ['--print-id', '--print-path']))
    A(mk('action-cmd', 'action',
         {CONFIG: 'Term.desktop:New\n',
          DATA: entry(actions='Actions=New;\n\n[Desktop Action New]\nExec=term %f\n')},
         ['--print-cmd= ']))
    A(mk('action-not-listed', 'action',
         {CONFIG: 'Term.desktop:New\n', DATA: entry()}, ['--print-id']))
    A(mk('exclusion-directive', 'config',
         {CONFIG: '-Term.desktop\n', DATA: entry(), DATA_B: entry()},
         ['--print-id']))
    A(mk('inclusion-directive', 'config',
         {CONFIG: '-Term.desktop\n+Other.desktop\n-Other.desktop\n',
          DATA: entry(), DATA_B: entry()}, ['--print-id']))
    A(mk('desktop-specific-list', 'config',
         {'home/.config/hyprland-xdg-terminals.list': 'Other.desktop\n',
          'home/.config/xdg-terminals.list': 'Term.desktop\n',
          DATA: entry(), DATA_B: entry()}, ['--print-id']))
    A(mk('desktop-list-other-desktop', 'config',
         {'home/.config/gnome-xdg-terminals.list': 'Other.desktop\n',
          DATA: entry(), DATA_B: entry()}, ['--print-id']))
    A(mk('config-dirs-order', 'config',
         {'home/.config/xdg-terminals.list': 'Term.desktop\n',
          'etc/xdg/xdg-terminals.list': 'Other.desktop\n',
          DATA: entry(), DATA_B: entry()}, ['--print-id']))
    A(mk('desktop-multi-value', 'config',
         {'home/.config/hyprland-xdg-terminals.list': 'Other.desktop\n',
          DATA: entry(), DATA_B: entry()}, ['--print-id'],
         case_env=env(desktop='GNOME:Hyprland')))
    A(mk('onlyshowin-fallback-match', 'show-in',
         {DATA: entry(extra=['OnlyShowIn=Hyprland;GNOME;'])}, ['--print-id']))
    A(mk('onlyshowin-fallback-mismatch', 'show-in',
         {DATA: entry(extra=['OnlyShowIn=GNOME;'])}, ['--print-id']))
    A(mk('notshowin-fallback-match', 'show-in',
         {DATA: entry(extra=['NotShowIn=Hyprland;'])}, ['--print-id']))
    A(mk('onlyshowin-explicit-ignored', 'show-in',
         {CONFIG: 'Term.desktop\n', DATA: entry(extra=['OnlyShowIn=GNOME;'])},
         ['--print-id']))
    A(mk('no-desktop-variable', 'show-in',
         {DATA: entry(extra=['OnlyShowIn=Hyprland;'])}, ['--print-id'],
         case_env=env(desktop=None)))
    A(mk('duplicate-user-wins', 'ordering',
         {SYS: entry(exec_='nope'), DATA: entry()},
         ['--print-path']))
    A(mk('duplicate-all-dirs', 'ordering',
         {SYS: entry(), LOCAL: entry(), DATA: entry()}, ['--print-path']))
    A(mk('directory-shadows-file', 'quirk',
         {SYS: entry(), 'usr/local/share/applications/Term.desktop/x.desktop':
          entry()}, ['--print-id']))
    A(mk('nested-subdir-entry', 'ordering',
         {'home/.local/share/applications/sub/Term.desktop': entry()},
         ['--print-id']))
    A(mk('invalid-chars-file', 'ordering',
         {'home/.local/share/applications/bad name.desktop': entry()},
         ['--print-id']))
    A(mk('no-trailing-newline', 'quirk',
         {CONFIG: 'Term.desktop\nOther.desktop\n',
          DATA: entry().rstrip('\n'), DATA_B: entry()}, ['--print-id']))
    A(mk('group-header-quirk', 'quirk',
         {CONFIG: '/execarg_strict\nTerm.desktop\nOther.desktop\n',
          DATA: entry(execarg=None),
          'home/.local/share/applications/Other.desktop': '[X-Extra]\n',
          'home/.local/share/applications/Third.desktop': entry()},
         ['--print-id']))
    A(mk('state-leak', 'quirk',
         {CONFIG: '/execarg_strict\nTerm.desktop\nOther.desktop\n',
          DATA: entry(execarg=None),
          DATA_B: '[Desktop Entry]\nX-TerminalArgExec=-e\nExec=term\n'},
         ['--print-id']))
    A(mk('key-leading-space', 'quirk',
         {CONFIG: '  Term.desktop  \n',
          DATA: entry().replace('Categories=System', '  Categories=System')},
         ['--print-id']))
    A(mk('crlf-entry', 'quirk',
         {CONFIG: 'Term.desktop\nOther.desktop\n',
          DATA: entry().replace('\n', '\r\n'), DATA_B: entry()}, ['--print-id']))
    A(mk('empty-entry-file', 'quirk',
         {CONFIG: 'Term.desktop\nOther.desktop\n', DATA: '', DATA_B: entry()},
         ['--print-id']))
    A(mk('config-comments', 'config',
         {CONFIG: '# a comment\n\nTerm.desktop\n   \n', DATA: entry()},
         ['--print-id']))
    A(mk('entry-comments', 'quirk',
         {CONFIG: 'Term.desktop\n',
          DATA: entry(extra=['# comment', 'Comment=hi'])}, ['--print-id']))
    A(mk('debug-output-stdout-stable', 'env',
         {CONFIG: 'Term.desktop\n', DATA: entry()}, ['--print-id'],
         case_env=env(extra={'XTE_DEBUG': '1'})))
    A(mk('title-dir-appid', 'prepend',
         {CONFIG: 'Term.desktop\n',
          DATA: entry(extra=['X-TerminalArgDir=--working-directory=',
                             'X-TerminalArgTitle=-t',
                             'X-TerminalArgAppId=--class'])},
         ['--print-cmd= ', '--dir=/tmp/x', '--title=ttl', '--app-id=id', 'true']))
    A(mk('title-dir-appid-spaced', 'prepend',
         {CONFIG: 'Term.desktop\n',
          DATA: entry(extra=['X-TerminalArgDir=-d',
                             'X-TerminalArgTitle=-t',
                             'X-TerminalArgAppId=--app-id'])},
         ['--print-cmd= ', '--dir=/tmp/x', '--title=ttl', '--app-id=id', 'true']))
    A(mk('hold-arg', 'prepend',
         {CONFIG: 'Term.desktop\n', DATA: entry(extra=['X-TerminalArgHold=--wait'])},
         ['--print-cmd= ', '--hold', 'true']))
    A(mk('hold-without-entry-arg', 'prepend',
         {CONFIG: 'Term.desktop\n', DATA: entry()},
         ['--print-cmd= ', '--hold', 'true']))
    A(mk('dir-without-entry-arg', 'prepend',
         {CONFIG: 'Term.desktop\n', DATA: entry()},
         ['--print-cmd= ', '--dir=/tmp/x', 'true']))
    A(mk('exec-dash-e-option', 'print',
         {CONFIG: 'Term.desktop\n', DATA: entry(execarg='-e')},
         ['--print-cmd= ', '-e', 'true']))
    A(mk('no-entries', 'selection', {'home/.config/xdg-terminals.list': ''},
         ['--print-id']))
    A(mk('cache-disabled-directive', 'env',
         {CONFIG: '/disable_cache\nTerm.desktop\n', DATA: entry()},
         ['--print-id']))
    A(mk('exec-single-quote', 'exec-parse',
         {CONFIG: 'Term.desktop\n', DATA: entry(exec_="term 'a b'")},
         ['--print-cmd= ']))
    A(mk('exec-tilde', 'exec-parse',
         {CONFIG: 'Term.desktop\nOther.desktop\n',
          DATA: entry(exec_='term ~/x'), DATA_B: entry()}, ['--print-id']))
    A(mk('exec-escaped-quote', 'exec-parse',
         {CONFIG: 'Term.desktop\n', DATA: entry(exec_='term "a \\" b"')},
         ['--print-cmd= ']))
    A(mk('readdir-order', 'ordering',
         dict({CONFIG: ''},
              **{'home/.local/share/applications/%s.desktop' % n: entry()
                 for n in ('A', 'B', 'C', 'D', 'E')}), ['--print-id']))
    A(mk('readdir-order-print-path', 'ordering',
         dict({CONFIG: ''},
              **{'home/.local/share/applications/z%s.desktop' % n: entry()
                 for n in ('1', '2', '3')}), ['--print-path']))
    A(mk('uppercase-desktop-list', 'config',
         {'home/.config/hyprland-xdg-terminals.list': 'Other.desktop\n',
          DATA: entry(), DATA_B: entry()}, ['--print-id'],
         case_env=env(desktop='HYPRLAND')))
    A(mk('uppercase-desktop-showin', 'show-in',
         {DATA: entry(extra=['OnlyShowIn=HYPRLAND;'])}, ['--print-id'],
         case_env=env(desktop='HYPRLAND')))
    A(mk('case-differs-showin', 'show-in',
         {DATA: entry(extra=['OnlyShowIn=hyprland;'])}, ['--print-id'],
         case_env=env(desktop='Hyprland')))
    A(mk('multiple-config-dirs', 'config',
         {'home/.config/xdg-terminals.list': 'Other.desktop\n',
          'etc/xdg/xdg-terminals.list': 'Term.desktop\n',
          DATA: entry(), DATA_B: entry()}, ['--print-id']))
    A(mk('config-dir-trailing-slash', 'config',
         {'etc/xdg/xdg-terminals.list': 'Term.desktop\n', DATA: entry()},
         ['--print-id'],
         case_env={'XDG_CURRENT_DESKTOP': 'Hyprland',
                   'XDG_CONFIG_HOME': '$ROOT/home/.config/',
                   'XDG_CONFIG_DIRS': '$ROOT/etc/xdg/',
                   'XDG_DATA_HOME': '$ROOT/home/.local/share/',
                   'XDG_DATA_DIRS': '$ROOT/usr/local/share/:$ROOT/usr/share/',
                   'XDG_CACHE_HOME': '$ROOT/cache'}))
    A(mk('config-file-crlf', 'quirk',
         {CONFIG: 'Term.desktop\r\nOther.desktop\r\n', DATA: entry(),
          DATA_B: entry()}, ['--print-id']))
    A(mk('missing-desktop-entry-group', 'quirk',
         {CONFIG: 'Term.desktop\n',
          DATA: '[Other]\nType=Application\nCategories=System;TerminalEmulator;\n'
                'X-TerminalArgExec=-e\nExec=term\n'}, ['--print-id']))
    A(mk('group-before-desktop-entry', 'quirk',
         {CONFIG: 'Term.desktop\n',
          DATA: '[X-First]\n' + entry()}, ['--print-id']))
    A(mk('action-group-before-actions-key', 'action',
         {CONFIG: 'Term.desktop:New\n',
          DATA: '[Desktop Entry]\nType=Application\nName=Term\n'
                'Categories=System;TerminalEmulator;\n'
                'X-TerminalArgExec=-e\nExec=term\n'
                '[Desktop Action New]\nExec=term new\n'
                'Actions=New;\n'}, ['--print-id']))
    A(mk('compat-execarg-key', 'execarg',
         {CONFIG: 'Term.desktop\n', DATA: entry(execarg=None,
                                               extra=['X-ExecArg=-c'])},
         ['--print-cmd= ']))
    A(mk('compat-execarg-key-strict', 'execarg',
         {CONFIG: '/execarg_strict\nTerm.desktop\n',
          DATA: entry(execarg=None, extra=['X-ExecArg=-c'])},
         ['--print-cmd= ']))
    A(mk('print-delimiter-tab', 'print', {DATA: entry()},
         ['--print-id', '--print-path', '--print-delimiter=\\t']))
    A(mk('print-delimiter-raw-newline', 'print', {DATA: entry()},
         ['--print-id', '--print-path', '--print-delimiter=' + '\n']))
    A(mk('title-with-equals', 'prepend',
         {CONFIG: 'Term.desktop\n', DATA: entry(extra=['X-TerminalArgTitle=-t'])},
         ['--print-cmd= ', '--title=a=b', 'true']))
    A(mk('hold-and-test', 'prepend',
         {CONFIG: 'Term.desktop\n', DATA: entry(extra=['X-TerminalArgHold=--wait'])},
         ['--test', '--hold', 'true']))
    A(mk('print-cmd-then-test', 'print', {DATA: entry()},
         ['--print-cmd= ', '--test', 'true']))
    A(mk('data-home-outside-home', 'selection',
         {'opt/share/applications/Term.desktop': entry()}, ['--print-id'],
         case_env={'XDG_CURRENT_DESKTOP': 'Hyprland',
                   'XDG_CONFIG_HOME': '$ROOT/home/.config',
                   'XDG_CONFIG_DIRS': '$ROOT/etc/xdg',
                   'XDG_DATA_HOME': '$ROOT/opt/share',
                   'XDG_DATA_DIRS': '$ROOT/usr/share',
                   'XDG_CACHE_HOME': '$ROOT/cache'}))
    A(mk('execarg-defaults-two-ids', 'execarg',
         {CONFIG: '/execarg_default:Term.desktop:-z\n'
                  '/execarg_default:Other.desktop:-y\nOther.desktop\n',
          DATA: entry(execarg=None), DATA_B: entry(execarg=None)},
         ['--print-cmd= ']))
    return out


def cases_nonce(n, seed):
    """Deterministic random fixtures over the same schema."""
    rng = random.Random(seed)
    out = []
    exec_words = ['term', 'term -e', 'term --class "a b"', 'term %f %U',
                  'term %%x', 'term %Z', 'nope', 'printf', 'term "q',
                  'term %', 'term a;b', 'term\\s-x', '', 'term --wait=%d',
                  'term ""', 'term \\"x', 'term %i%c', 'term %d %n',
                  'term "a\\\\"', 'term --opt=~x', 'term  extra   spaces  ',
                  'term $HOME', 'term `id`', 'term #hash', 'term ?x',
                  'term (paren)', "term 'single'"]
    category_sets = ['System;TerminalEmulator;', 'System;', 'TerminalEmulator;',
                     None, 'TerminalEmulatorX;', 'A;TerminalEmulator;B;',
                     ';TerminalEmulator;;', 'TerminalEmulator;;']
    extra_lines = [[], ['Hidden=true'], ['Hidden=True'], ['Hidden=1'],
                   ['TryExec=term'], ['TryExec=nope'], ['TryExec=find_entry'],
                   ['TryExec=printf'], ['OnlyShowIn=Hyprland;'],
                   ['OnlyShowIn=GNOME;'], ['OnlyShowIn=Hyprland;GNOME;'],
                   ['NotShowIn=Hyprland;'], ['NotShowIn=GNOME;'],
                   ['NoDisplay=true'], ['Type=Link'], ['Comment=x'],
                   ['X-TerminalArgDir=--working-directory='],
                   ['X-TerminalArgTitle=-t'], ['X-TerminalArgAppId=--class'],
                   ['X-TerminalArgHold=--hold'], ['X-ExecArg=-c']]
    execargs = ['-e', '-x', '', None, '--\\sfoo', '-e', '--']
    argsets = [['--print-id'], ['--print-path'], ['--print-cmd= '],
               ['--print-id', '--print-path', '--print-cmd'],
               ['--print-cmd=,', '--', 'a', 'b'],
               ['--print-id', '--print-delimiter=|'],
               ['--test'], ['--print-content'],
               ['--print-id', '--print-cmd=:'],
               ['--print-path', '--print-cmd=\\t'],
               ['--print-id', '--', '--help'],
               ['--print-cmd=', '--', 'x'],
               ['--print-id', '--print-path', '--dir=/d', '--title=t',
                '--app-id=a', '--hold', 'cmd'],
               ['--print-cmd= ', '--title=a=b', 'true'],
               ['--print-content', '--print-id'],
               ['--print-id', '--bogus-option']]
    desktops = ['Hyprland', 'GNOME', 'hyprland:GNOME', None, 'HYPRLAND']
    configs = ['Term.desktop\n', 'Other.desktop\n', 'Term.desktop\nOther.desktop\n',
               '-Other.desktop\n', '/execarg_strict\n', 'Missing.desktop\n',
               '/execarg_compat\nTerm.desktop\n', '+Term.desktop\n-Term.desktop\n',
               '/execarg_default:Term.desktop:-z\n', '# comment\n\n',
               'Term.desktop:New\n', 'Bad Name.desktop\nTerm.desktop\n']
    for i in range(n):
        ex = rng.choice(exec_words)
        cats = rng.choice(category_sets)
        execarg = rng.choice(execargs)
        keys = []
        if cats is not None:
            keys.append('Categories=' + cats)
        if execarg is not None:
            keys.append('X-TerminalArgExec=' + execarg)
        keys.extend(rng.choice(extra_lines))
        keys.append('Exec=' + ex)
        rng.shuffle(keys)
        text = '[Desktop Entry]\n' + '\n'.join(keys) + '\n'
        if rng.random() < 0.15:
            text = rng.choice(['[X-Pre]\n', '[X-Pre]\n\n', '# lead comment\n']) + text
        if rng.random() < 0.25:
            text += rng.choice(['Actions=New;\n\n[Desktop Action New]\n'
                                'Exec=term new\n',
                                'Actions=New;\n',
                                '[Desktop Action New]\nExec=term new\n'])
        if rng.random() < 0.15:
            text = text.rstrip('\n')
        files = {}
        if rng.random() < 0.65:
            files[CONFIG] = rng.choice(configs)
        target = rng.choice([DATA, DATA_B, SYS, LOCAL,
                             'home/.local/share/applications/sub/Term.desktop'])
        files[target] = text
        if rng.random() < 0.45:
            other = DATA_B if target != DATA_B else DATA
            files[other] = entry(exec_=rng.choice(['term', 'term %f', 'nope']),
                                 categories=rng.choice(category_sets),
                                 execarg=rng.choice(execargs))
        args = list(rng.choice(argsets))
        out.append(mk('nonce-%03d' % i, 'nonce', files, args,
                      execs=('bin/term',),
                      case_env=env(desktop=rng.choice(desktops))))
    return out


# ---------------------------------------------------------------------------
# harness
# ---------------------------------------------------------------------------

def materialise(root, case):
    for rel, text in sorted(case['files'].items()):
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
    for rel in case['exec']:
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write('#!/bin/sh\nexit 0\n')
        os.chmod(path, ASCII_FLAG)


def case_env(root, toolbin, case):
    e = {'HOME': root + '/home', 'PATH': root + '/bin:' + toolbin}
    for key, value in case['env'].items():
        e[key] = value.replace('$ROOT', root)
    return e


def reset_cache(root):
    cache = os.path.join(root, 'cache')
    if os.path.isdir(cache):
        for name in os.listdir(cache):
            path = os.path.join(cache, name)
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            else:
                os.unlink(path)
    else:
        os.makedirs(cache, exist_ok=True)


def tree_state(root):
    state = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            try:
                st = os.lstat(path)
            except OSError:
                continue
            state[path] = (st.st_mode, st.st_size, st.st_mtime_ns)
    return state


def run(cmd, env, cwd, timeout=60):
    proc = subprocess.run(cmd, env=env, cwd=cwd, timeout=timeout,
                          stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def strace_execve(tool, args, env, cwd, scratch, strace):
    log = os.path.join(scratch, 'strace.log')
    cmd = [strace, '-f', '-qq', '-o', log,
           '-e', 'trace=execve,socket,connect', sys.executable, tool] + args
    rc, out, _err = run(cmd, env, cwd)
    execve = 0
    sockets = 0
    with open(log, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            if 'execve(' in line:
                execve += 1
            elif 'socket(' in line or 'connect(' in line:
                sockets += 1
    return rc, out, execve, sockets


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', default=os.environ.get('TMPDIR') or tempfile.gettempdir())
    ap.add_argument('--out', default=os.path.join(here, 'receipts'))
    ap.add_argument('--tool', default=os.path.join(here, 'mado-terminal.py'))
    ap.add_argument('--script', default=PIN)
    ap.add_argument('--nonce', type=int, default=0)
    ap.add_argument('--seed', type=int, default=47)
    ap.add_argument('--keep', action='store_true')
    ap.add_argument('--verbose', action='store_true')
    args = ap.parse_args(argv[1:])

    digest = hashlib.sha256(open(args.script, 'rb').read()).hexdigest()
    if digest != PIN_SHA256:
        sys.stderr.write('compare: %s sha256 %s != pin %s\n'
                         % (args.script, digest, PIN_SHA256))
        return 1

    os.makedirs(args.work, exist_ok=True)
    base = tempfile.mkdtemp(prefix='compare-', dir=args.work)
    toolbin = os.path.join(base, 'toolbin')
    os.makedirs(toolbin, exist_ok=True)
    for name in TOOLBIN:
        target = shutil.which(name)
        if target is None:
            sys.stderr.write('compare: required helper %s not found\n' % name)
            return 1
        os.symlink(target, os.path.join(toolbin, name))
    cases = cases_pinned() + cases_nonce(args.nonce, args.seed)

    rows = []
    agree = 0
    for case in cases:
        pre = case['args'][:case['args'].index('--')] if '--' in case['args'] \
            else case['args']
        help_mode = any(a in ('-h', '--help') for a in pre)
        if not help_mode and not any(a == '--test' or a.startswith('--print')
                                     for a in case['args']):
            raise SystemExit('compare: case %s has no print mode' % case['id'])
        root = os.path.join(base, 'cases', case['id'])
        if os.path.isdir(root):
            shutil.rmtree(root)
        for sub in ('home/.config', 'home/.local/share/applications',
                    'usr/share/applications', 'usr/local/share/applications',
                    'etc/xdg', 'cache', 'bin'):
            os.makedirs(os.path.join(root, sub), exist_ok=True)
        materialise(root, case)
        e = case_env(root, toolbin, case)

        reset_cache(root)
        real_rc, real_out, real_err = run([args.script] + case['args'], e, root)
        case['expect'] = {'rc': real_rc,
                          'stdout': real_out.decode('utf-8', 'surrogateescape')
                          .replace(root, '$ROOT')}
        time.sleep(0.05)                 # let the resolver's forked cache save land

        reset_cache(root)
        obs_rc, obs_out, _ = run(
            [args.script, '--print-id', '--print-path', '--print-cmd'], e, root)
        time.sleep(0.05)

        reset_cache(root)
        before = tree_state(root)
        tool_rc, tool_out, tool_err = run(
            [sys.executable, args.tool, 'print'] + case['args'], e, root)
        after = tree_state(root)
        nowrite = before == after

        observed = os.path.join(root, 'observed.txt')
        with open(observed, 'wb') as f:
            f.write(obs_out)
        expl_rc, expl_out, _ = run(
            [sys.executable, args.tool, 'explain', '--observed', observed], e, root)
        verdict = ''
        for line in expl_out.decode('utf-8', 'surrogateescape').splitlines():
            if line.startswith('MADO_TERM: '):
                verdict = line
        os.unlink(observed)
        if obs_rc == 0:
            explain_ok = expl_rc == 0 and 'verdict=AGREE' in verdict
        else:
            explain_ok = expl_rc == 3 and 'verdict=NO_TERMINAL' in verdict

        ok = (real_out == tool_out and real_rc == tool_rc and nowrite
              and explain_ok)
        if ok:
            agree += 1
        rows.append((case, real_rc, real_out, real_err, tool_rc, tool_out,
                     tool_err, nowrite, explain_ok, expl_rc, verdict))
        if args.verbose or not ok:
            sys.stderr.write('%s %s\n' % ('ok  ' if ok else 'FAIL', case['id']))
            if not ok:
                sys.stderr.write('  real rc=%d out=%r\n' % (real_rc, real_out))
                sys.stderr.write('  tool rc=%d out=%r\n' % (tool_rc, tool_out))
                sys.stderr.write('  nowrite=%s explain_rc=%d verdict=%r\n'
                                 % (nowrite, expl_rc, verdict))
                if real_err:
                    sys.stderr.write('  real stderr=%r\n' % real_err[:200])
                if tool_err:
                    sys.stderr.write('  tool stderr=%r\n' % tool_err[:200])
        if not args.keep:
            shutil.rmtree(root, ignore_errors=True)

    # tripwire: the tool must start no process and open no socket
    trip = []
    strace = shutil.which('strace')
    if strace and cases:
        probe = cases[0]
        root = os.path.join(base, 'tripwire')
        for sub in ('home/.config', 'home/.local/share/applications',
                    'cache', 'bin'):
            os.makedirs(os.path.join(root, sub), exist_ok=True)
        materialise(root, probe)
        e = case_env(root, toolbin, probe)
        for label, mode_args in (('print', ['print'] + probe['args']),
                                 ('explain', ['explain'])):
            rc, out, execve, sockets = strace_execve(
                args.tool, mode_args, e, root, base, strace)
            want = probe['expect']['stdout'].replace('$ROOT', root).encode(
                'utf-8', 'surrogateescape')
            trip.append({'mode': label, 'rc': rc, 'execve': execve,
                         'sockets': sockets,
                         'stdout_ok': None if label == 'explain' else out == want})
        shutil.rmtree(root, ignore_errors=True)

    os.makedirs(args.out, exist_ok=True)
    cases_path = os.path.join(args.out, 'cases.json')
    with open(cases_path, 'w', encoding='utf-8') as f:
        json.dump(cases, f, indent=1, sort_keys=True)
        f.write('\n')

    lines = []
    lines.append('# compare.py -- mado-terminal.py vs %s' % args.script)
    lines.append('# script sha256 %s (pinned)' % digest)
    lines.append('# tool      %s' % args.tool)
    lines.append('# cases     %d pinned + %d nonce (seed %d)'
                 % (len(cases) - args.nonce, args.nonce, args.seed))
    lines.append('#')
    for case, real_rc, real_out, real_err, tool_rc, tool_out, tool_err, \
            nowrite, explain_ok, expl_rc, verdict in rows:
        status = 'AGREE' if (real_out == tool_out and real_rc == tool_rc) else 'DIFF'
        lines.append('%-28s %-11s rc=%d stdout=%d bytes nowrite=%s explain=%s/%d'
                     % (case['id'], status, real_rc, len(real_out),
                        'ok' if nowrite else 'WROTE',
                        'agree' if explain_ok else 'MISMATCH', expl_rc))
        if status == 'DIFF':
            lines.append('  expect %r' % real_out)
            lines.append('  model  %r' % tool_out)
            lines.append('  rc     expect %d model %d' % (real_rc, tool_rc))
        if case['class'] == 'nonce' and status != 'AGREE':
            lines.append('  args   %r' % (case['args'],))
    lines.append('#')
    lines.append('COMPARISON: %d/%d agree on stdout bytes and exit status'
                 % (agree, len(cases)))
    if not trip:
        lines.append('TRIPWIRE: strace unavailable, not measured')
    for entry in trip:
        lines.append('TRIPWIRE %s: rc=%d execve=%d sockets=%d stdout_ok=%s'
                     % (entry['mode'], entry['rc'], entry['execve'],
                        entry['sockets'], entry['stdout_ok']))
    with open(os.path.join(args.out, 'agree.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print('\n'.join(lines[-3:]))
    if not args.keep:
        shutil.rmtree(base, ignore_errors=True)
    return 0 if agree == len(cases) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
