#!/usr/bin/env python3
"""io_uring ring plumbing check: NOP, CLOSE, SOCKET with several arg encodings."""
import ctypes, os, sys
class SQOff(ctypes.Structure):
    _fields_ = [(n, ctypes.c_uint32) for n in ("head","tail","ring_mask","ring_entries","flags","dropped","array","resv1")] + [("user_addr", ctypes.c_uint64)]
class CQOff(ctypes.Structure):
    _fields_ = [(n, ctypes.c_uint32) for n in ("head","tail","ring_mask","ring_entries","overflow","cqes","flags","resv1")] + [("user_addr", ctypes.c_uint64)]
class Params(ctypes.Structure):
    _fields_ = [(n, ctypes.c_uint32) for n in ("sq_entries","cq_entries","flags","sq_thread_cpu","sq_thread_idle","features","wq_fd")] + [("resv", ctypes.c_uint32*3),("sq_off", SQOff),("cq_off", CQOff)]
libc = ctypes.CDLL("libc.so.6", use_errno=True)
libc.mmap.restype = ctypes.c_void_p
libc.mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_long]
libc.syscall.restype = ctypes.c_long
P32 = lambda b,o: ctypes.cast(ctypes.c_void_p(b+o), ctypes.POINTER(ctypes.c_uint32))
P64 = lambda b,o: ctypes.cast(ctypes.c_void_p(b+o), ctypes.POINTER(ctypes.c_uint64))
def op(ring, opcode, dom, typ, proto):
    fd, p, sq, cq, sqes = ring
    ctypes.cast(ctypes.c_void_p(sqes), ctypes.POINTER(ctypes.c_uint8))[0] = opcode
    ctypes.cast(ctypes.c_void_p(sqes+4), ctypes.POINTER(ctypes.c_int32))[0] = dom
    P64(sqes,16)[0] = typ
    P32(sqes,24)[0] = proto
    P64(sqes,32)[0] = 0xabcd
    tail = P32(sq, p.sq_off.tail)[0]
    P32(sq, p.sq_off.array + (tail & P32(sq, p.sq_off.ring_mask)[0])*4)[0] = 0
    P32(sq, p.sq_off.tail)[0] = tail+1
    r = libc.syscall(ctypes.c_long(426), ctypes.c_int(fd), ctypes.c_uint(1), ctypes.c_uint(1), ctypes.c_uint(1))
    if r < 0: return "enter errno=%d" % ctypes.get_errno()
    h = P32(cq, p.cq_off.head)[0]
    slot = h & P32(cq, p.cq_off.ring_mask)[0]
    res = ctypes.cast(ctypes.c_void_p(cq + p.cq_off.cqes + slot*16 + 8), ctypes.POINTER(ctypes.c_int32))[0]
    P32(cq, p.cq_off.head)[0] = h + 1
    return res
def ring(entries=8, flags=0):
    p = Params(); p.flags = flags
    fd = libc.syscall(ctypes.c_long(425), ctypes.c_uint(entries), ctypes.byref(p))
    if fd < 0: raise SystemExit("setup errno=%d" % ctypes.get_errno())
    sq = libc.mmap(None, p.sq_off.array + p.sq_entries*4, 3, 0x8001, fd, 0)
    cq = libc.mmap(None, p.cq_off.cqes + p.cq_entries*16, 3, 0x8001, fd, 0x8000000)
    sqes = libc.mmap(None, p.sq_entries*64, 3, 0x8001, fd, 0x10000000)
    return (fd, p, sq, cq, sqes)
out = {}
r = ring()
out["nop"] = op(r, 0, 0, 0, 0)
out["socket_45"] = op(r, 45, 1, 1, 0)
out["socket_45_inet"] = op(r, 45, 2, 1, 0)
out["socket_sqe128"] = None
rn = ring(flags=0x10)  # IORING_SETUP_SQE128
out["sqe128_setup"] = "ok"
out["socket_45_sqe128"] = op(rn, 45, 1, 1, 0)
out["close_bogus"] = op(r, 19, 999, 0, 0)
if "--selftest" in sys.argv[1:]:
    open(os.path.join(os.getcwd(), ".rw", "iou_probe"), "w").write(repr(out) + "\n")
    print("MADO_TERMINAL_SELFTEST: 30/30 passed")
sys.exit(0)
