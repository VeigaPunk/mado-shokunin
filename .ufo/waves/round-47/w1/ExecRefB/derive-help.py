#!/usr/bin/env python3
"""derive-help.py -- patch the modelled --help text into mado-terminal.py.

The `print` contract is byte-identical stdout, and `-h|--help` is one of the
print paths the modelled program takes *before* it resolves anything.  Rather
than transcribe the heredoc by hand (it contains a nested $(usage) expansion,
`\\` sequences and `\\${...}` escapes), the bytes are captured from the pinned
script once and embedded verbatim.

The embedded text carries $0's basename of the modelled invocation
("xdg-terminal-exec"), which is what /usr/bin/xdg-terminal-exec reports.

Usage: derive-help.py [--tool PATH] [--script PATH] [--work DIR]
"""
import argparse
import hashlib
import os
import subprocess
import sys
import tempfile

MARKER = '__PATCH_HELP__ = None'


def main(argv):
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument('--tool', default=os.path.join(here, 'mado-terminal.py'))
    ap.add_argument('--script', default='/usr/bin/xdg-terminal-exec')
    ap.add_argument('--work', default=os.environ.get('TMPDIR') or tempfile.gettempdir())
    args = ap.parse_args(argv[1:])

    cache = tempfile.mkdtemp(prefix='derive-help-cache-', dir=args.work)
    env = dict(os.environ)
    env['XDG_CACHE_HOME'] = cache           # print/help modes may write a cache
    proc = subprocess.run([args.script, '--help'], env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        sys.stderr.write('derive-help: --help exited %d\n' % proc.returncode)
        return 1
    help_bytes = proc.stdout
    if not help_bytes.startswith(b'xdg-terminal-exec - Shell-based default terminal launcher.'):
        sys.stderr.write('derive-help: unexpected help head %r\n' % help_bytes[:60])
        return 1
    if b'\r' not in help_bytes and b'\x00' in help_bytes:
        sys.stderr.write('derive-help: refusing to embed NUL bytes\n')
        return 1

    with open(args.tool, 'r', encoding='utf-8') as f:
        source = f.read()
    if MARKER not in source:
        sys.stderr.write('derive-help: marker %r not found (already patched?)\n' % MARKER)
        return 1
    replacement = '_HELP_BYTES = %r' % help_bytes
    source = source.replace(MARKER, replacement, 1)
    with open(args.tool, 'w', encoding='utf-8') as f:
        f.write(source)
    print('derive-help: embedded %d help bytes, sha256 %s'
          % (len(help_bytes), hashlib.sha256(help_bytes).hexdigest()))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
