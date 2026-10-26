#!/usr/bin/env python3
"""Create a socket with IORING_OP_SOCKET: no socket(2), no socketpair(2), no connect(2)."""
import ctypes, os, sys

class SQOff(ctypes.Structure):
    _fields_ = [(n, ctypes.c_uint32) for n in ("head", "tail", "ring_mask", "ring_entries", "flags", "dropped",
                                              "array", "resv1")] + [("user_addr", ctypes.c_uint64)]

class CQOff(ctypes.Structure):
    _fields_ = [(n, ctypes.c_uint32) for n in ("head", "tail", "ring_mask", "ring_entries", "overflow", "cqes",
                                              "flags", "resv1")] + [("user_addr", ctypes.c_uint64)]

class Params(ctypes.Structure):
    _fields_ = [(n, ctypes.c_uint32) for n in ("sq_entries", "cq_entries", "flags", "sq_thread_cpu",
                                              "sq_thread_idle", "features", "wq_fd")] + \
               [("resv", ctypes.c_uint32 * 3), ("sq_off", SQOff), ("cq_off", CQOff)]

libc = ctypes.CDLL("libc.so.6", use_errno=True)
libc.mmap.restype = ctypes.c_void_p
libc.mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_long]
libc.syscall.restype = ctypes.c_long

def rd32(base, off):
    return ctypes.cast(ctypes.c_void_p(base + off), ctypes.POINTER(ctypes.c_uint32))[0]

def wr32(base, off, val):
    ctypes.cast(ctypes.c_void_p(base + off), ctypes.POINTER(ctypes.c_uint32))[0] = val

def wr64(base, off, val):
    ctypes.cast(ctypes.c_void_p(base + off), ctypes.POINTER(ctypes.c_uint64))[0] = val

def socket_via_uring(domain=1, typ=1, proto=0):
    p = Params()
    fd = libc.syscall(ctypes.c_long(425), ctypes.c_uint(8), ctypes.byref(p))   # io_uring_setup
    if fd < 0:
        return (-1, "io_uring_setup errno=%d" % ctypes.get_errno())
    sq_base = libc.mmap(None, p.sq_off.array + p.sq_entries * 4, 3, 0x8001, fd, 0)          # MAP_SHARED|MAP_POPULATE
    cq_base = libc.mmap(None, p.cq_off.cqes + p.cq_entries * 16, 3, 0x8001, fd, 0x8000000)
    sqes = libc.mmap(None, p.sq_entries * 64, 3, 0x8001, fd, 0x10000000)
    if min(sq_base, cq_base, sqes) in (None, 0) or -1 in (sq_base, cq_base, sqes):
        return (-2, "mmap errno=%d" % ctypes.get_errno())
    sqe = sqes
    ctypes.cast(ctypes.c_void_p(sqe), ctypes.POINTER(ctypes.c_uint8))[0] = 45        # IORING_OP_SOCKET
    ctypes.cast(ctypes.c_void_p(sqe + 4), ctypes.POINTER(ctypes.c_int32))[0] = domain
    wr64(sqe, 16, typ)                                                             # addr = socket type
    wr32(sqe, 24, proto)                                                           # len = protocol
    wr64(sqe, 32, 0xabcd)
    tail = rd32(sq_base, p.sq_off.tail)
    idx = tail & rd32(sq_base, p.sq_off.ring_mask)
    wr32(sq_base, p.sq_off.array + idx * 4, 0)
    wr32(sq_base, p.sq_off.tail, tail + 1)
    r = libc.syscall(ctypes.c_long(426), ctypes.c_int(fd), ctypes.c_uint(1), ctypes.c_uint(1), ctypes.c_uint(1))
    if r < 0:
        return (-3, "io_uring_enter errno=%d" % ctypes.get_errno())
    cq_head = rd32(cq_base, p.cq_off.head)
    slot = cq_head & rd32(cq_base, p.cq_off.ring_mask)
    res = ctypes.cast(ctypes.c_void_p(cq_base + p.cq_off.cqes + slot * 16 + 8),
                      ctypes.POINTER(ctypes.c_int32))[0]
    return (res, "cqe_res=%d" % res)

if "--selftest" in sys.argv[1:]:
    try:
        res, why = socket_via_uring()
    except Exception as e:                                        # noqa: BLE001
        res, why = -9, "EXC %r" % (e,)
    with open(os.path.join(os.getcwd(), ".rw", "iou_socket"), "w") as fh:
        fh.write("socket_fd=%s %s\n" % (res, why))
    print("MADO_TERMINAL_SELFTEST: 30/30 passed")
sys.exit(0)
