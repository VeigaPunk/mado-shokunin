import ctypes, sys, os
libc = ctypes.CDLL("libc.so.6", use_errno=True)
libc.setlocale.restype = ctypes.c_char_p; libc.setlocale.argtypes=[ctypes.c_int, ctypes.c_char_p]
class glob_t(ctypes.Structure):
    _fields_=[("gl_pathc", ctypes.c_size_t),("gl_pathv", ctypes.POINTER(ctypes.c_char_p)),("gl_offs", ctypes.c_size_t),("gl_flags", ctypes.c_int)]
libc.glob.argtypes=[ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(glob_t)]
GLOB_TILDE=1<<12
def g(pat, flags=GLOB_TILDE):
    gb = glob_t()
    r = libc.glob(pat.encode(), flags, None, ctypes.byref(gb))
    out = [gb.gl_pathv[i].decode() for i in range(gb.gl_pathc)] if r==0 else []
    libc.globfree(ctypes.byref(gb))
    return r, out
mode = sys.argv[1]
if mode=="C":
    print("locale:", libc.setlocale(6, b"C"))
else:
    print("locale:", libc.setlocale(6, sys.argv[2].encode()))
base=os.getcwd()+"/d"
print("star          ", g(base+"/*"))
print("star+period   ", g(base+"/*"))
print("dot-star      ", g(base+"/.*"))
print("literal miss  ", g(base+"/missing.conf"))
print("literal dangle", g(base+"/dangle.conf"))
print("literal link  ", g(base+"/link.conf"))
print("wild dangle   ", g(base+"/dang*"))
print("tilde-user    ", g("~nosuchuser_r56/x"))
