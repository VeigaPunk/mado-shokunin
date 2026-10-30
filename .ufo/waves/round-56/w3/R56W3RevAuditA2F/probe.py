import ctypes
import errno
import os
from pathlib import Path
import tempfile

root = Path('/fast/scratch/hyaku/mado-r56/R56W3RevAuditA2F')
class Glob(ctypes.Structure):
    _fields_ = [('pathc', ctypes.c_size_t), ('pathv', ctypes.POINTER(ctypes.c_char_p)), ('offs', ctypes.c_size_t), ('flags', ctypes.c_int), ('closedir', ctypes.c_void_p), ('readdir', ctypes.c_void_p), ('opendir', ctypes.c_void_p), ('lstat', ctypes.c_void_p), ('stat', ctypes.c_void_p)]
libc = ctypes.CDLL(None)
libc.glob.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(Glob)]
libc.glob.restype = ctypes.c_int
libc.globfree.argtypes = [ctypes.POINTER(Glob)]
with tempfile.TemporaryDirectory(prefix='glob-', dir=root) as directory:
    loop = Path(directory) / 'loop.conf'
    loop.symlink_to('loop.conf')
    for path in [Path(directory) / 'missing.conf', loop]:
        result = Glob()
        rc = libc.glob(os.fsencode(path), 4096, None, ctypes.byref(result))
        print(f'glob GLOB_TILDE {path.name}: rc={rc} matches={result.pathc}')
        for n in range(result.pathc):
            match = os.fsdecode(result.pathv[n])
            print(f'  match={Path(match).name}; lstat=symlink:{os.path.islink(match)}')
            try:
                os.stat(match)
            except OSError as error:
                print(f'  status follows symlink: errno={error.errno} {errno.errorcode[error.errno]}')
        libc.globfree(ctypes.byref(result))
lines = Path('/home/vgpnk/.config/hypr/hyprland.conf').read_text().splitlines()
print('live source-prefix count:', sum(line.startswith('source') for line in lines))
print('live source line numbers:', ','.join(str(n) for n,line in enumerate(lines,1) if line.startswith('source')))
print('live line 13:', lines[12])
print('nested envs line 3:', Path('/home/vgpnk/.local/share/omarchy/default/hypr/envs.conf').read_text().splitlines()[2])
