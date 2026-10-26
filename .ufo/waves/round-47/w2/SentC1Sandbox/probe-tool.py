#!/usr/bin/env python3
"""SentC1Sandbox relay probe (seat SentC1Sandbox, mado round-47 w2). NOT the L1 tool: it prints what the counter's
bwrap allowlist exposes, so it can be dropped in as tools/mado-terminal.py and run by c1-r47-terminal.py itself.

Modes (by argv): `--selftest` -> one-line marker printed as the counter's clause-s `last=`; `explain` -> benign marker;
`probe-write` / `probe-read` / `probe-obs` -> cross-run channels; anything else -> full report on stdout.
No fork, no exec, no socket (clause r must stay ok).
"""
import errno
import json
import os
import sys

CAP = 60


def ec(e):
    return errno.errorcode.get(getattr(e, "errno", None), type(e).__name__)


def ls(p, n=CAP):
    try:
        v = sorted(os.listdir(p))
    except OSError as e:
        return {"error": ec(e)}
    return v[:n] + (["<%d more>" % (len(v) - n)] if len(v) > n else [])


def st(p):
    try:
        s = os.stat(p)
        return {"dev": s.st_dev, "ino": s.st_ino, "mode": oct(s.st_mode & 0o7777), "size": s.st_size}
    except OSError as e:
        return {"error": ec(e)}


def link(p):
    try:
        return os.readlink(p)
    except OSError as e:
        return {"error": ec(e)}


def head(p, n=4096):
    try:
        with open(p, "rb") as f:
            b = f.read(n)
    except OSError as e:
        return "ERR:" + ec(e)
    return b.decode("utf-8", "backslashreplace")


def wprobe(p, data=b"S"):
    try:
        with open(p, "ab") as f:
            f.write(data)
        return "WROTE"
    except OSError as e:
        return "ERR:" + ec(e)


def mkprobe(p):
    try:
        os.mkdir(p)
        return "MKDIR"
    except OSError as e:
        return "ERR:" + ec(e)


def root():
    c = os.environ.get("XDG_CACHE_HOME", "")
    if c.endswith("/.rw/cache"):
        return c[: -len("/.rw/cache")]
    return os.path.dirname(os.path.dirname(c)) if c else os.environ.get("HOME", "/")


def mounts():
    out = []
    text = head("/proc/self/mountinfo", 200000)
    if text.startswith("ERR:"):
        return text
    for ln in text.splitlines():
        f = ln.split(" ")
        if "-" not in f:
            continue
        i = f.index("-")
        if len(f) < i + 4:
            continue
        out.append({"mount_root": f[3], "mountpoint": f[4], "opts": f[5],
                    "fstype": f[i + 1], "source": f[i + 2], "super": f[i + 3]})
    return out


WANT = ("Uid", "Gid", "CapInh", "CapPrm", "CapEff", "CapBnd", "CapAmb", "NoNewPrivs", "Seccomp", "NSpid")


def status():
    d = {}
    for ln in head("/proc/self/status", 16384).splitlines():
        k, _, v = ln.partition(":")
        if k in WANT:
            d[k] = v.strip()
    return d


def report(tag):
    R = root()
    r = {"tag": tag, "argv": sys.argv[1:], "uid": os.getuid(), "euid": os.geteuid(), "gid": os.getgid(),
         "cwd": os.getcwd(), "derived_root": R, "env": dict(os.environ), "status": status(),
         "uid_map": head("/proc/self/uid_map", 256).strip(),
         "gid_map": head("/proc/self/gid_map", 256).strip(),
         "hostname": head("/proc/sys/kernel/hostname", 128).strip(),
         "pid1_cmdline": head("/proc/1/cmdline", 512).replace("\x00", " ").strip(),
         "pid1_root": link("/proc/1/root"), "self_root": link("/proc/self/root"),
         "self_exe": link("/proc/self/exe"), "self_cwd": link("/proc/self/cwd"),
         "proc": ls("/proc", 40), "mounts": mounts(),
         "net_dev": head("/proc/net/dev", 512).strip(), "cgroup": head("/proc/self/cgroup", 512).strip(),
         "top": ls("/"), "root_list": ls(R), "parent": ls(os.path.dirname(R), 20),
         "grandparent": ls(os.path.dirname(os.path.dirname(R)), 20),
         "dirs": {}, "sensitive": {}, "writes": {}, "fds": {}}
    fdv = ls("/proc/self/fd")
    if isinstance(fdv, list):
        for fd in fdv:
            if not fd.startswith("<"):
                r["fds"][fd] = link("/proc/self/fd/" + fd)
    for p in ("/usr", "/usr/lib", "/usr/bin", "/usr/share", "/bin", "/dev", "/dev/shm", "/tmp", "/oracle",
              "/oracle/bin", "/etc", "/home", "/root", "/fast", "/run", "/var", "/sys", "/opt", "/srv", "/mnt",
              "/media", "/proc/sys", "/lib", "/lib64", "/dev/pts"):
        r["dirs"][p] = ls(p, 40)
    r["pid1"] = {"status": {}, "fds": {}, "environ": head("/proc/1/environ", 1024).replace("\x00", " ").strip(),
                 "exe": link("/proc/1/exe"), "cwd": link("/proc/1/cwd")}
    for ln in head("/proc/1/status", 16384).splitlines():
        k, _, v = ln.partition(":")
        if k in ("Uid", "Gid", "CapEff", "NoNewPrivs", "Seccomp", "NSpid"):
            r["pid1"]["status"][k] = v.strip()
    p1fd = ls("/proc/1/fd")
    if isinstance(p1fd, list):
        for fd in p1fd:
            if not fd.startswith("<"):
                r["pid1"]["fds"][fd] = link("/proc/1/fd/" + fd)
    try:
        os.close(os.open("/dev/tty", os.O_RDONLY | os.O_NOCTTY))
        r["dev_tty_open"] = "OPENED"
    except OSError as e:
        r["dev_tty_open"] = "ERR:" + ec(e)
    r["dev_core_link"] = link("/dev/core")
    try:
        os.close(os.open("/dev/core", os.O_RDONLY | os.O_NONBLOCK))
        r["dev_core_open"] = "OPENED"
    except OSError as e:
        r["dev_core_open"] = "ERR:" + ec(e)
    r["site_packages"] = ls("/usr/lib/python3.14/site-packages", 20)
    lane = "/home/vgpnk/Projects/shokunin/mado-shokunin"
    for p in (R, R + "/.rw", R + "/home", R + "/bin", lane,
              lane + "/quality/counters/c1-r47-fixtures.json",
              lane + "/quality/counters/c1-r47-terminal.py",
              lane + "/.ufo/waves/round-47/fetch/xdg-terminal-exec",
              lane + "/.ufo/waves/round-47/l1-draft/mado-terminal.py",
              "/oracle/xdg-terminal-exec", "/oracle/tool.py", "/etc/passwd", "/etc/hostname",
              "/home/vgpnk/.ssh", "/home/vgpnk/.config", "/usr/lib/os-release", "/usr/bin/python3",
              "/usr/lib/python3.14", os.path.dirname(R)):
        r["sensitive"][p] = st(p)
    pid = os.getpid()
    tg = {"rw": R + "/.rw/probe-sentc1", "rw_dir": R + "/.rw/probe-sentc1-d",
          "root_ro": R + "/probe-sentc1", "home_ro": R + "/home/probe-sentc1",
          "bin_ro": R + "/bin/probe-sentc1", "parent": os.path.join(os.path.dirname(R), "probe-sentc1"),
          "tmpfs_top": "/probe-sentc1", "usr_lib": "/usr/lib/probe-sentc1",
          "usr_bin": "/usr/bin/probe-sentc1", "bin_sh": "/bin/sh",
          "oracle_bin": "/oracle/bin/probe-sentc1", "oracle_tool": "/oracle/tool.py",
          "tmp": "/tmp/sentc1-probe-tmp-%d" % pid, "dev": "/dev/probe-sentc1",
          "dev_shm": "/dev/shm/sentc1-probe-shm-%d" % pid, "proc": "/proc/probe-sentc1",
          "proc_sys_new": "/proc/sys/probe-sentc1", "etc": "/etc/probe-sentc1",
          "usr_share": "/usr/share/probe-sentc1", "fast": "/fast/probe-sentc1",
          "home": "/home/probe-sentc1", "varlog": "/var/log/probe-sentc1"}
    for k in sorted(tg):
        r["writes"][k] = wprobe(tg[k])
    r["writes"]["rw_dir"] = mkprobe(tg["rw_dir"])
    return r


def main(argv):
    if argv and argv[0] == "--selftest":
        print("PROBE selftest uid=%d cwd=%s top=%s" % (os.getuid(), os.getcwd(), ls("/")))
        print("PROBE-SELFTEST-INSIDE pid1=%s uid=%d mounts=%d" % (
            head("/proc/1/cmdline", 200).replace("\x00", " ")[:64], os.getuid(),
            len(mounts()) if isinstance(mounts(), list) else -1))
        return 0
    R = root()
    if argv and argv[0] == "probe-write":
        os.makedirs(os.path.join(R, ".rw", "probe"), exist_ok=True)
        print("PROBE-WRITE %s" % wprobe(os.path.join(R, ".rw", "probe", "marker"), b"tool-wrote"))
        print("PROBE-WRITE-RO %s" % wprobe(os.path.join(R, "probe-write-root"), b"x"))
        return 0
    if argv and argv[0] == "probe-read":
        p = os.path.join(R, ".rw", "probe", "marker")
        print("PROBE-READ present=%s content=%r" % (os.path.exists(p), head(p, 64)))
        return 0
    if argv and argv[0] == "probe-obs":
        print("PROBE-OBS %s" % mkprobe(os.path.join(R, ".rw", "obs")))
        return 0
    if argv and argv[0] == "explain":
        print("PROBE explain: no resolver model")
        return 0
    print("PROBE-REPORT-------- id=%s" % (argv[1] if len(argv) > 1 else "print"))
    print(json.dumps(report(argv[0] if argv else ""), default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
