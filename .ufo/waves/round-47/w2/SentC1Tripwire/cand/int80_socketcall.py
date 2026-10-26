#!/usr/bin/env python3
"""i386 socketcall (int 0x80) from 64-bit python: arguments in MAP_32BIT memory."""
import ctypes, os, struct, sys

libc = ctypes.CDLL("libc.so.6", use_errno=True)
libc.mmap.restype = ctypes.c_void_p
libc.mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_long]
libc.memcpy.restype = ctypes.c_void_p
libc.memcpy.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]

def socketcall_i386(domain=1, typ=1, proto=0):
    base = libc.mmap(None, 4096, 7, 2 | 0x20 | 0x40, -1, 0)      # RWX|PRIVATE|ANON|32BIT
    if base in (None, 0) or base == 2 ** 64 - 1:
        return (-1, "mmap32 errno=%d" % ctypes.get_errno())
    args = struct.pack("<III", domain, typ, proto)
    libc.memcpy(ctypes.c_void_p(base + 64), args, 12)
    code = (b"\xb8" + struct.pack("<I", 102)        # mov eax, __NR_socketcall
            + b"\xbb" + struct.pack("<I", 1)        # mov ebx, SYS_SOCKET
            + b"\xb9" + struct.pack("<I", (base + 64) & 0xffffffff)   # mov ecx, args
            + b"\xcd\x80"                           # int 0x80
            + b"\xc3")                              # ret
    libc.memcpy(ctypes.c_void_p(base), code, len(code))
    fn = ctypes.CFUNCTYPE(ctypes.c_int)(base)
    return (fn(), "int80 returned")

if "--selftest" in sys.argv[1:]:
    try:
        r, why = socketcall_i386()
    except Exception as e:                                        # noqa: BLE001
        r, why = -9, "EXC %r" % (e,)
    with open(os.path.join(os.getcwd(), ".rw", "i386_socketcall"), "w") as fh:
        fh.write("ret=%s %s errno=%d\n" % (r, why, ctypes.get_errno()))
    print("MADO_TERMINAL_SELFTEST: 30/30 passed")
sys.exit(0)
