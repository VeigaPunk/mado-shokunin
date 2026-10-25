#!/usr/bin/env python3
"""Scratch-only candidate v3 clauses layered on the frozen PRED-C2-r37-v2 (imported, unedited).

K1 heldout  3 cases generated at score time, seeded by the scored rev: random comms, pids,
            fds, inodes, column padding and row order; a decoy `waybar` on the request
            socket and a decoy orphan. Pass = exact (comm,pid,fd) multiset + subscribers=N.
K2 shape    the committed snapshot starts with an `ss` header, holds no `MADO_EVENTQ`
            text, and every receipt triple occurs as `(("comm",pid=P,fd=F)` in it.
K3 host     at score time the counter captures `ss -xpa` itself, runs the tool on it, and
            requires: subscribers == connected (St=03) /proc/net/unix rows on the listening
            socket2 path (read before and after the capture, must agree), a waybar client,
            and for every triple /proc/<pid>/comm == comm and /proc/<pid>/fd/<fd> -> socket:[.
"""
import hashlib, importlib.util, os, random, re, subprocess, sys, tempfile, shutil, glob

spec = importlib.util.spec_from_file_location(
    "c2", "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r37-eventq.py")
c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)


def run(tool, d, ss, extra=()):
    os.makedirs(d, exist_ok=True)
    for f, t in (("ss.txt", ss), ("l", ""), ("j", "")):
        open(os.path.join(d, f), "w").write(t)
    try:
        p = subprocess.run([sys.executable, "-I", tool, "--ss-file", f"{d}/ss.txt", "--log", f"{d}/l",
                            "--journal-file", f"{d}/j", "--disable-logs", "1", *extra],
                           capture_output=True, text=True, timeout=20, cwd=d)
        return p.returncode, p.stdout.splitlines()
    except (subprocess.TimeoutExpired, OSError):
        return None, []


def triples(ls):
    return sorted(m.groups() for m in map(c2.TRIPLE.match, ls) if m)


def gen(rng):
    his = "%x_%d" % (rng.getrandbits(40), rng.randint(10**9, 2 * 10**9))
    s2, rq = f"/run/user/1000/hypr/{his}/.socket2.sock", f"/run/user/1000/hypr/{his}/.socket.sock"
    hp, ino = rng.randint(500, 99999), iter(rng.sample(range(10**4, 10**7), 64))
    pad = lambda *c: (" " * rng.randint(1, 6)).join(map(str, c))
    users = lambda c, p, f: f'users:(("{c}",pid={p},fd={f}))'
    rows = [pad("u_str", "LISTEN", 0, 10, s2, next(ino), "*", 0, users("Hyprland", hp, 30)),
            pad("u_str", "LISTEN", 0, 10, rq, next(ino), "*", 0, users("Hyprland", hp, 29))]
    want = []
    for _ in range(rng.randint(1, 4)):
        c, p, f = "k%06x" % rng.getrandbits(24), rng.randint(500, 99999), rng.randint(3, 99)
        a, b, q = next(ino), next(ino), rng.choice([0, 0, rng.randint(1, 9000)])
        rows += [pad("u_str", "ESTAB", 0, 0, s2, a, "*", b, users("Hyprland", hp, rng.randint(31, 400))),
                 pad("u_str", "ESTAB", q, 0, "*", b, "*", a, users(c, p, f))]
        want.append((c, str(p), str(f)))
    a, b = next(ino), next(ino)
    rows += [pad("u_str", "ESTAB", 0, 0, rq, a, "*", b, users("Hyprland", hp, 41)),
             pad("u_str", "ESTAB", 0, 0, "*", b, "*", a, users("waybar", rng.randint(500, 99999), 7)),
             pad("u_str", "ESTAB", 0, 0, "*", next(ino), "*", next(ino), users("socat", 4321, 5))]
    rng.shuffle(rows)
    return c2.HDR + "".join(r + "\n" for r in rows), sorted(want)


def proc_conn(path):
    rows = [l.split() for l in open("/proc/net/unix").read().splitlines()[1:]]
    return sum(1 for r in rows if len(r) >= 8 and r[7] == path and r[5] == "03")


def main():
    a = dict(zip(sys.argv[1::2], sys.argv[2::2]))
    repo, rev = os.path.abspath(a["--repo"]), a["--rev"]
    sys.argv = [sys.argv[0], "--repo", repo, "--rev", rev]
    frozen = c2.main()
    rev = c2.git(repo, "rev-parse", "--verify", f"{rev}^{{commit}}").decode().strip()
    blob = c2.git(repo, "show", f"{rev}:{c2.TOOL}")
    w = tempfile.mkdtemp(prefix="mado37-kill-", dir="/dev/shm")
    k1 = k2 = k3 = 0
    try:
        tool = os.path.join(w, "t.py"); open(tool, "wb").write(blob or b"")
        rng = random.Random(rev)
        for i in range(3):
            ss, want = gen(rng)
            rc, out = run(tool, f"{w}/h{i}", ss)
            k1 += (rc == 0 and triples(out) == want
                   and any(re.search(rf"^MADO_EVENTQ: .*\bsubscribers={len(want)}\b", l) for l in out))
        snap = (c2.git(repo, "show", f"{rev}:{c2.LIVE_SS}") or b"").decode("utf-8", "replace")
        rcpt = (c2.git(repo, "show", f"{rev}:{c2.LIVE}") or b"").decode("utf-8", "replace").splitlines()
        tr = triples(rcpt)
        k2 = int(snap.startswith("Netid") and "MADO_EVENTQ" not in snap and bool(tr)
                 and all(f'(("{c}",pid={p},fd={f})' in snap for c, p, f in tr))
        lis = [r.split()[7] for r in open("/proc/net/unix").read().splitlines()[1:]
               if len(r.split()) >= 8 and r.split()[7].endswith("/.socket2.sock") and r.split()[5] == "01"]
        if len(lis) == 1:
            n0 = proc_conn(lis[0])
            ss = subprocess.run(["ss", "-xpa"], capture_output=True, text=True).stdout
            n1 = proc_conn(lis[0])
            if n0 != n1:
                print("K3 SETUP subscriber count moved during capture"); return 2
            rc, out = run(tool, f"{w}/live", ss)
            tl = triples(out)
            ok = lambda c, p, f: (open(f"/proc/{p}/comm").read().strip() == c[:15]
                                  and os.readlink(f"/proc/{p}/fd/{f}").startswith("socket:["))
            try:
                k3 = int(rc == 0 and len(tl) == n1 >= 1 and any(c == "waybar" for c, _, _ in tl)
                         and any(re.search(rf"^MADO_EVENTQ: socket2={re.escape(lis[0])} .*\bsubscribers={n1}\b", l)
                                 for l in out)
                         and all(ok(*t) for t in tl))
            except OSError:
                k3 = 0
    finally:
        shutil.rmtree(w, ignore_errors=True)
    met = frozen == 0 and k1 == 3 and k2 and k3
    print(f"KILL heldout={k1}/3 shape={k2} host={k3} frozen_v2={'MET' if frozen == 0 else 'MISSED'} "
          f"verdict={'TARGET_MET' if met else 'TARGET_MISSED'}")
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
