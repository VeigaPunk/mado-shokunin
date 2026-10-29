import os, re, sys, json
PID = int(sys.argv[1])
def fdinfo(fd):
    with open("/proc/%d/fdinfo/%s" % (PID, fd)) as f:
        return f.read()
watch_re = re.compile(r"inotify wd:([0-9a-f]+) ino:([0-9a-f]+) sdev:([0-9a-f]+) mask:([0-9a-f]+) ignored_mask:([0-9a-f]+)")
live = {}
for fd in sorted(os.listdir("/proc/%d/fd" % PID)):
    try:
        txt = fdinfo(fd)
    except OSError:
        continue
    if "inotify wd:" not in txt:
        continue
    live[fd] = watch_re.findall(txt)
for fd, ents in live.items():
    print("fd %s: %d watch lines; anon inode %s" % (fd, len(ents), [l for l in fdinfo(fd).splitlines() if l.startswith("ino:")][0]))
sets = [set(e[1] for e in ents) for ents in live.values()]
print("all inotify fds share identical watch inode set:", all(s == sets[0] for s in sets))
ents = live[sorted(live)[0]]
kernel = {}
for wd, ino, sdev, mask, ign in ents:
    kernel.setdefault(int(ino,16), []).append((int(wd,16), int(mask,16), int(sdev,16), int(ign,16)))
print("kernel distinct inodes: %d  watch lines: %d" % (len(kernel), len(ents)))

plan = []
for line in open("plan.txt"):
    m = re.match(r"MADO_WATCH: n=(\d+) role=(\S+) path=(\S+) type=(\S+) mask=(\S+) via=(\S+)$", line.strip())
    if m:
        plan.append((int(m.group(1)), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6)))
print("plan watches: %d" % len(plan))
rows=[]
for (n, role, path, typ, masktxt, via) in plan:
    p = path
    ino = None if typ=="missing" else os.lstat(p).st_ino
    islink = os.path.islink(p)
    real = os.path.realpath(p)
    realino = os.stat(real).st_ino if os.path.exists(real) else None
    rows.append(dict(n=n, role=role, path=path, typ=typ, masktxt=masktxt, via=via, ino=ino, islink=islink, real=real, realino=realino))
json.dump(rows, open("rows.json","w"), indent=1)
print()
print("%-4s %-9s %-9s %-12s %-6s %-12s %-9s %s" % ("n","role","type","ino","link","realino","in-kernel","path"))
for r in rows:
    ink = r["ino"] in kernel if r["ino"] else False
    print("%-4d %-9s %-9s %-12s %-6s %-12s %-9s %s" % (r["n"], r["role"], r["typ"], r["ino"], r["islink"], r["realino"], ink, r["path"]))
pred = set(r["ino"] for r in rows if r["ino"] is not None)
print()
print("predicted inode set size:", len(pred), " kernel inode set size:", len(kernel))
missing = pred - set(kernel); extra = set(kernel) - pred
print("PREDICTED-NOT-IN-KERNEL (%d):" % len(missing))
for r in rows:
    if r["ino"] in missing: print("   n=%d role=%s %s" % (r["n"], r["role"], r["path"]))
print("KERNEL-NOT-PREDICTED (%d):" % len(extra))
for ino in sorted(extra):
    e = kernel[ino][0]
    print("   ino=%d wd=%s mask=%s ignored=%s" % (ino, hex(e[0]), hex(e[1]), hex(e[3])))
print()
masks = {}
for ino,e in kernel.items(): masks.setdefault(e[1],[]).append(ino)
print("kernel mask histogram:", {hex(k): len(v) for k,v in masks.items()})
# mtimes
print()
print("mtimes vs process start:")
import subprocess
start = subprocess.check_output(["ps","-o","lstart=","-p",str(PID)]).decode().strip()
print("  process start:", start)
import calendar, time
st = os.stat("/proc/%d" % PID).st_ctime
newer = []
for r in rows:
    p=r["path"]
    if os.path.lexists(p):
        m = os.lstat(p).st_mtime
        if m > st: newer.append((p, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(m))))
print("  /proc/%d ctime=%s" % (PID, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st))))
print("  watched paths with mtime > process ctime:", newer if newer else "NONE")
