import ctypes
import errno
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

LANE = '/home/vgpnk/Projects/shokunin/mado-shokunin'
REV = '0f3a54361a9824484d0801679ceb1fd8ac7c32e1'
WORK = Path('/fast/scratch/hyaku/mado-r56/R56W3RevAuditA2A')
PREFIX = '.ufo/waves/round-56/fetch/'

def show(path, ranges):
    args = ['git', '-C', LANE, 'show', REV + ':' + path]
    print('COMMAND:', ' '.join(args))
    lines = subprocess.check_output(args, text=True).splitlines()
    for start, end in ranges:
        for n in range(start, min(end, len(lines)) + 1):
            print(f'{n}: {lines[n - 1]}')

for name, ranges in [
    ('Hyprland-ConfigWatcher.cpp', [(1, 111)]),
    ('Hyprland-ConfigValues.cpp', [(485, 498)]),
    ('Hyprland-PropRefresher.hpp', [(1, 40)]),
    ('Hyprland-PropRefresher.cpp', [(29, 159)]),
    ('Hyprland-legacy-ConfigManager.cpp', [(359, 369), (479, 487), (610, 616), (626, 632), (726, 786), (1067, 1087), (1802, 1855), (2133, 2135)]),
    ('Hyprland-MiscFunctions.cpp', [(61, 83)]),
    ('Hyprland-EventLoopManager.cpp', [(68, 74), (123, 130)]),
    ('Hyprland-HyprCtl.cpp', [(1180, 1227)]),
    ('man7-inotify.7.html', [(85, 92), (304, 330)]),
]:
    show(PREFIX + name, ranges)
show('corpus/knowledge/hyprland-config-autoreload-r56.md', [(18, 70), (78, 82), (128, 142)])

# Non-Hyprland libc probe: absolute path means GLOB_TILDE has no effect.
# glibc's public glob_t layout; GNU extension callbacks are unused.
class Glob(ctypes.Structure):
    _fields_ = [('gl_pathc', ctypes.c_size_t),
                ('gl_pathv', ctypes.POINTER(ctypes.c_char_p)),
                ('gl_offs', ctypes.c_size_t), ('gl_flags', ctypes.c_int),
                ('gl_closedir', ctypes.c_void_p), ('gl_readdir', ctypes.c_void_p),
                ('gl_opendir', ctypes.c_void_p), ('gl_lstat', ctypes.c_void_p),
                ('gl_stat', ctypes.c_void_p)]

WORK.mkdir(parents=True, exist_ok=True)
try:
    d = Path(tempfile.mkdtemp(prefix='glob-loop-', dir=WORK))
    path = d / 'loop.conf'
    path.symlink_to('loop.conf')
    libc = ctypes.CDLL('libc.so.6')
    libc.glob.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(Glob)]
    libc.glob.restype = ctypes.c_int
    libc.globfree.argtypes = [ctypes.POINTER(Glob)]
    result = Glob()
    rc = libc.glob(os.fsencode(path), 0, None, ctypes.byref(result))
    try:
        print(f'PROBE self-referential symlink: glob_rc={rc} matches={result.gl_pathc}')
        for i in range(result.gl_pathc):
            print('MATCH:', os.fsdecode(result.gl_pathv[i]))
        try:
            os.stat(path)
            print('STAT: unexpectedly succeeded')
        except OSError as exc:
            print(f'STAT: errno={exc.errno} name={errno.errorcode[exc.errno]}')
        print('LSTAT: symlink exists; its target is itself, not a missing pathname')
    finally:
        libc.globfree(ctypes.byref(result))
finally:
    shutil.rmtree(WORK)
    print('SCRATCH: removed ' + str(WORK))
