#!/usr/bin/env python3
"""Read-only-to-lane libc probe; creates fixtures only in the assigned scratch."""
import ctypes
import os
from pathlib import Path

ROOT = Path('/fast/scratch/hyaku/mado-r56/R56W3RevAuditA2B')
OUT = Path('/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevAuditA2B')

class Glob(ctypes.Structure):
    _fields_ = [('pathc', ctypes.c_size_t),
                ('pathv', ctypes.POINTER(ctypes.c_char_p)),
                ('offs', ctypes.c_size_t), ('flags', ctypes.c_int),
                ('funcs', ctypes.c_void_p * 5)]

libc = ctypes.CDLL('libc.so.6', use_errno=True)
libc.glob.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p,
                      ctypes.POINTER(Glob)]
libc.glob.restype = ctypes.c_int
libc.globfree.argtypes = [ctypes.POINTER(Glob)]
probe = ROOT / 'isolated-probe'
probe.mkdir(exist_ok=True)
loop = probe / 'loop.conf'
regular = probe / 'ordinary.conf'
lines = []
try:
    loop.symlink_to('loop.conf')
    regular.write_text('# regular\n')
    for label, path, remove in [('symlink-cycle', loop, False),
                                ('regular-disappears-after-glob', regular, True)]:
        g = Glob()
        try:
            rc = libc.glob(os.fsencode(path), 4096, None, ctypes.byref(g))
            matches = [os.fsdecode(g.pathv[i]) for i in range(g.pathc)]
            lines.append(f'{label}: glob(flags=GLOB_TILDE) rc={rc} matches={matches!r}')
            if remove:
                path.unlink()
            try:
                os.stat(path)
                lines.append('stat: success')
            except OSError as exc:
                lines.append(f'stat follows symlinks: errno={exc.errno} {exc.strerror}')
        finally:
            libc.globfree(ctypes.byref(g))
    text = '\n'.join(lines) + '\n'
    (OUT / 'status-counterexamples.txt').write_text(text)
    print(text, end='')
finally:
    loop.unlink(missing_ok=True)
    regular.unlink(missing_ok=True)
    probe.rmdir()
