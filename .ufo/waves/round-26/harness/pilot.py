#!/usr/bin/env python3
"""mado r26 harness pilot: one oracle run with isolation facts printed (receipt: pilot-receipt.txt).

Prints: harness pins; the live session's instance list size before/after (host `hyprctl instances -j`,
a read verb, with the host environment); for the nested Hyprland process seen from the host
(/proc/<pid> of the sandboxed child): its WAYLAND_DISPLAY / XDG_RUNTIME_DIR / HYPRLAND_INSTANCE_SIGNATURE,
whether its mount table contains /run/user or any /dev/dri card node, and its net namespace versus the
host's; the oracle's answer sizes; the Hyprland coredump count before/after.
"""
import json, os, subprocess, sys, tempfile, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oracle as O  # noqa: E402


def live_instances():
    p = subprocess.run(["timeout", "5", "hyprctl", "instances", "-j"], capture_output=True)
    try:
        return len(json.loads(p.stdout))
    except ValueError:
        return -1


def nested_pids():
    out = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            exe = os.readlink("/proc/%s/exe" % pid)
            env = open("/proc/%s/environ" % pid, "rb").read().split(b"\0")
        except OSError:
            continue
        if exe == "/usr/bin/Hyprland" and any(e.startswith(b"XDG_RUNTIME_DIR=/tmp/m26o-") for e in env):
            out.append((pid, env))
    return out


def main():
    O.check_build()
    print("harness tinywl sha256:%s libwlroots sha256:%s render_node=%s" % (O.TINYWL_SHA, O.LIBWLR_SHA, O.RENDER_NODE))
    c0, l0 = O.coredumps(), live_instances()
    print("before: hyprland_coredumps=%d live_instances=%d" % (c0, l0))
    tmp = tempfile.mkdtemp(prefix="m26pilot-", dir="/fast/scratch/hyaku/mado-r26")
    home = os.path.join(tmp, "h")
    O.snapshot(os.path.expanduser("~"), home)
    seen = {}

    def watch():
        t = time.time()
        while time.time() - t < 20 and not seen:
            for pid, env in nested_pids():
                keep = [e.decode(errors="replace") for e in env
                        if e.split(b"=")[0] in (b"WAYLAND_DISPLAY", b"XDG_RUNTIME_DIR", b"HYPRLAND_INSTANCE_SIGNATURE",
                                                 b"DBUS_SESSION_BUS_ADDRESS", b"DISPLAY")]
                mi = open("/proc/%s/mountinfo" % pid).read()
                seen.update(pid=pid, env=keep, run_user="/run/user" in mi,
                            card_nodes=[ln.split()[4] for ln in mi.splitlines() if "/dev/dri/card" in ln],
                            netns_same=os.readlink("/proc/%s/ns/net" % pid) == os.readlink("/proc/self/ns/net"),
                            render_mounts=[ln.split()[4] for ln in mi.splitlines() if "/dev/dri/render" in ln])
                break
            time.sleep(0.05)

    th = threading.Thread(target=watch)
    th.start()
    res, err = O.oracle(home, os.path.join(tmp, "o"), ["binds", "animations"])
    th.join()
    print("nested process (host view): %s" % json.dumps(seen, sort_keys=True))
    if res is None:
        print("ORACLE_FAIL %s" % err)
    else:
        print("oracle answered: binds=%d animation_nodes=%d beziers=%d" % (
            len(res["binds"]), len(res["animations"][0]), len(res["animations"][1])))
    time.sleep(2)
    c1, l1 = O.coredumps(), live_instances()
    print("after: hyprland_coredumps=%d live_instances=%d delta_coredumps=%d" % (c1, l1, c1 - c0))
    leftovers = [d for d in os.listdir("/tmp") if d.startswith("m26o-")]
    print("leftover private runtime dirs: %d; nested processes alive: %d" % (len(leftovers), len(nested_pids())))
    subprocess.run(["rm", "-rf", tmp])
    ok = res is not None and c1 == c0 and not seen.get("run_user") and not seen.get("card_nodes") \
        and seen.get("netns_same") is False and not leftovers
    print("PILOT %s" % ("ISOLATED_OK" if ok else "NOT_OK"))
    return 0 if ok else 1


if __name__ == "__main__":
    rc = main()
    print("exit=%d" % rc)
    sys.exit(rc)
