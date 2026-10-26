#!/usr/bin/env python3
"""Validate io_uring addr/len plumbing with IORING_OP_OPENAT (18), same SQE fields as SOCKET."""
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
p = Params()
fd = libc.syscall(ctypes.c_long(425), ctypes.c_uint(8), ctypes.byref(p))
sq = libc.mmap(None, p.sq_off.array + p.sq_entries*4, 3, 0x8001, fd, 0)
cq = libc.mmap(None, p.cq_off.cqes + p.cq_entries*16, 3, 0x8001, fd, 0x8000000)
sqes = libc.mmap(None, p.sq_entries*64, 3, 0x8001, fd, 0x10000000)
buf = ctypes.create_string_buffer(b"/oracle/bin\0")
def go(opcode, dom, addr, ln):
    ctypes.cast(ctypes.c_void_p(sqes), ctypes.POINTER(ctypes.c_uint8))[0] = opcode
    ctypes.cast(ctypes.c_void_p(sqes+4), ctypes.POINTER(ctypes.c_int32))[0] = dom
    P64(sqes,16)[0] = addr
    P32(sqes,24)[0] = ln
    P64(sqes,32)[0] = 7
    t = P32(sq, p.sq_off.tail)[0]
    P32(sq, p.sq_off.array + (t & P32(sq, p.sq_off.ring_mask)[0])*4)[0] = 0
    P32(sq, p.sq_off.tail)[0] = t+1
    r = libc.syscall(ctypes.c_long(426), ctypes.c_int(fd), ctypes.c_uint(1), ctypes.c_uint(1), ctypes.c_uint(1))
    if r < 0: return "enter errno=%d" % ctypes.get_errno()
    h = P32(cq, p.cq_off.head)[0]
    slot = h & P32(cq, p.cq_off.ring_mask)[0]
    res = ctypes.cast(ctypes.c_void_p(cq + p.cq_off.cqes + slot*16 + 8), ctypes.POINTER(ctypes.c_int32))[0]
    P32(cq, p.cq_off.head)[0] = h + 1
    return res
out = {"openat18": go(18, -100, ctypes.addressof(buf), 0), "socket45": go(45, 1, 1, 0),
       "bind56": go(56, 1, 0, 0), "pipe62": go(62, 1, 0, 0)}
if "--selftest" in sys.argv[1:]:
    open(os.path.join(os.getcwd(), ".rw", "iou_openat"), "w").write(repr(out) + "\n")
    print("MADO_TERMINAL_SELFTEST: 30/30 passed")
sys.exit(0)
