#!/usr/bin/env python3
"""ExecOracleGkeep (round 43 w1): observe the size Hyprland 0.56.2 itself reports for a client
with application id `org.omarchy.gkeep` matched by the host's gkeep rules, in the round-27
bubblewrap oracle layout (tinywl/wlroots 0.20.2 parent compositor, nested Hyprland, headless,
no network, no host session).

Adapted copy of .ufo/waves/round-27/harness/oracle.py (that file is never edited): same bwrap
verb set and same 'tinywl -s "exec Hyprland -c <conf>"' boot, plus (a) the round-43 wlroots build,
(b) a shm xdg-shell client (gkeep-shm.c) started with `hyprctl dispatch exec` INSIDE the sandbox,
(c) clients/monitors/version snapshots per case.

usage: oracle-gkeep.py --case NAME [--rules FILE] [--client PATH] [--work DIR] [--timeout N]
"""
import argparse, hashlib, json, os, re, shutil, signal, subprocess, sys, tempfile, time

TINYWL = "/fast/scratch/hyaku/mado-r43/oracle/wlroots/build/tinywl/tinywl"
LIBWLR = "/fast/scratch/hyaku/mado-r43/oracle/wlroots/build/libwlroots-0.20.so"
WLR_DIR = "/fast/scratch/hyaku/mado-r43/oracle/wlroots/build"
CASEDIR = "/fast/scratch/hyaku/mado-r43/ExecOracleGkeep"
RENDER_NODE = "/dev/dri/renderD129"
ORACLE_EXTRA = ["", "ecosystem {", "    no_update_news = true", "    no_donation_nag = true", "}", ""]
EXEC_RE = re.compile(r"^\s*exec(?:r)?(?:-once|-shutdown)?\s*=")
DEBUG_EXTRA = ["debug {", "    disable_logs = false", "    enable_stdout_logs = true", "}"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def coredumps():
    p = subprocess.run(["coredumpctl", "list", "--no-pager", "--no-legend"],
                       capture_output=True, text=True)
    return sum(1 for ln in p.stdout.splitlines() if "/usr/bin/Hyprland" in ln)


def hyprctl(xdg, args, timeout=10):
    env = {"PATH": "/usr/bin", "XDG_RUNTIME_DIR": xdg}
    p = subprocess.run(["timeout", str(timeout), "hyprctl"] + args, capture_output=True, env=env)
    return p.returncode, p.stdout.decode(errors="replace"), p.stderr.decode(errors="replace")


def strip_exec(path):
    text = open(path, encoding="utf-8").read()
    lines = [ln for ln in text.split("\n") if not EXEC_RE.match(ln)]
    removed = len(text.split("\n")) - len(lines)
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    return removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True)
    ap.add_argument("--rules", required=True, help="rule file copied to the case home's hypr dir")
    ap.add_argument("--client", default=os.path.join(CASEDIR, "gkeep-shm"))
    ap.add_argument("--app-id", default="org.omarchy.gkeep")
    ap.add_argument("--client-display", default="wayland-1",
                    help="WAYLAND_DISPLAY forced for the client: tinywl owns wayland-0, the nested "
                         "Hyprland the next free name. Hyprland's spawned children otherwise inherit "
                         "tinywl's WAYLAND_DISPLAY and connect to the PARENT compositor.")
    ap.add_argument("--client-args", default="")
    ap.add_argument("--create-output", default=None,
                    help="nested-only: `hyprctl -i <sig> output create headless <NAME>` before the client")
    ap.add_argument("--wait-monitor", type=float, default=0.0,
                    help="wait up to N s for monitors -j to be non-empty before the client")
    ap.add_argument("--no-client", action="store_true", help="watch monitors only, map no client")
    ap.add_argument("--monitor-watch", type=float, default=0.0)
    ap.add_argument("--work", default=None)
    ap.add_argument("--timeout", type=float, default=45.0)
    a = ap.parse_args()

    work = a.work or os.path.join(CASEDIR, "run-" + a.case)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    ohome = os.path.join(work, "home")
    hypr = os.path.join(ohome, ".config/hypr")
    os.makedirs(hypr)
    rule_dst = os.path.join(hypr, "gkeep.conf")
    shutil.copyfile(a.rules, rule_dst)
    strip_exec(rule_dst)
    conf = os.path.join(hypr, "hyprland.conf")
    with open(conf, "w", encoding="utf-8") as fh:
        fh.write("# ExecOracleGkeep round-43 case: %s\nsource = %s\n" % (a.case, rule_dst))
        fh.write("\n".join(ORACLE_EXTRA + DEBUG_EXTRA) + "\n")
    xdg = tempfile.mkdtemp(prefix="r43o-", dir="/tmp")
    os.chmod(xdg, 0o700)

    xdgbind = os.path.dirname(os.path.abspath(a.client))
    cmd = ["env", "-i", "PATH=/usr/bin", "prlimit", "--core=0", "--as=8000000000", "--",
           "bwrap", "--unshare-all", "--die-with-parent", "--new-session",
           "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
           "--symlink", "usr/lib", "/lib64", "--symlink", "usr/bin", "/sbin", "--ro-bind", "/etc", "/etc",
           "--dev", "/dev", "--dev-bind", RENDER_NODE, RENDER_NODE,
           "--ro-bind", "/sys/dev/char", "/sys/dev/char", "--ro-bind", "/sys/devices", "/sys/devices",
           "--ro-bind", "/sys/class/drm", "/sys/class/drm", "--proc", "/proc", "--tmpfs", "/run",
           "--tmpfs", "/tmp", "--tmpfs", "/dev/shm",
           "--ro-bind", WLR_DIR, WLR_DIR, "--ro-bind", xdgbind, xdgbind,
           "--bind", ohome, ohome, "--bind", xdg, xdg,
           "--clearenv", "--setenv", "PATH", "/usr/bin", "--setenv", "HOME", ohome,
           "--setenv", "XDG_RUNTIME_DIR", xdg, "--setenv", "WLR_BACKENDS", "headless",
           "--setenv", "WLR_HEADLESS_OUTPUTS", "1", "--setenv", "WLR_RENDERER", "gles2",
           "--setenv", "WLR_RENDER_DRM_DEVICE", RENDER_NODE, "--setenv", "LIBSEAT_BACKEND", "noop",
           "--setenv", "HYPRLAND_NO_CRASHREPORTER", "1", "--setenv", "HYPRLAND_NO_SD_NOTIFY", "1",
           "--setenv", "HYPRLAND_NO_SD_VARS", "1", "--chdir", ohome,
           TINYWL, "-s", "exec Hyprland -c '%s'" % conf]

    rec = {"case": a.case, "rules_src": a.rules, "rules_sha": sha(a.rules),
           "rules_text": open(a.rules, encoding="utf-8").read(),
           "client": a.client, "client_sha": sha(a.client), "app_id": a.app_id,
           "tinywl": TINYWL, "tinywl_sha": sha(TINYWL), "libwlroots": LIBWLR,
           "libwlroots_sha": sha(LIBWLR), "coredumps_before": coredumps(),
           "cmd": cmd, "steps": []}
    log = open(os.path.join(work, "sandbox.log"), "wb")
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                         start_new_session=True)
    t0 = time.time()
    try:
        sig = None
        while sig is None and time.time() - t0 < 40:
            if p.poll() is not None:
                rec["error"] = "sandbox exited rc=%s before a nested instance" % p.returncode
                break
            rc, out, err = hyprctl(xdg, ["instances", "-j"])
            if rc == 0:
                try:
                    inst = json.loads(out)
                    if inst:
                        sig = inst[0]["instance"]
                except (ValueError, KeyError, IndexError, TypeError):
                    pass
            if sig is None:
                time.sleep(0.25)
        rec["instance_sig"] = sig
        rec["boot_seconds"] = round(time.time() - t0, 2)
        if sig:
            time.sleep(0.8)
            rc, out, err = hyprctl(xdg, ["-i", sig, "version", "-j"])
            rec["steps"].append({"do": "version -j", "rc": rc})
            try:
                rec["version"] = json.loads(out)
            except ValueError:
                rec["version_raw"] = out[:2000]
            if a.create_output:
                rc, out, err = hyprctl(xdg, ["-i", sig, "output", "create", "headless", a.create_output])
                rec["steps"].append({"do": "output create headless " + a.create_output, "rc": rc,
                                     "stdout": out.strip()[:300], "stderr": err.strip()[:300]})
            if a.wait_monitor:
                t4, got = time.time(), None
                while time.time() - t4 < a.wait_monitor:
                    rc, out, err = hyprctl(xdg, ["-i", sig, "monitors", "-j"])
                    if rc == 0 and out.strip().startswith("["):
                        try:
                            if json.loads(out):
                                got = json.loads(out)
                                break
                        except ValueError:
                            pass
                    time.sleep(0.25)
                rec["monitor_ready"] = got
                rec["monitor_wait_seconds"] = round(time.time() - t4, 2)
            if a.monitor_watch:
                tl, prev = [], None
                t3 = time.time()
                while time.time() - t3 < a.monitor_watch:
                    rc, out, err = hyprctl(xdg, ["-i", sig, "monitors", "-j"])
                    if rc == 0 and out != prev:
                        tl.append({"t": round(time.time() - t3, 2),
                                   "names": [m.get("name") for m in (json.loads(out) or [])]
                                   if out.strip().startswith("[") else out[:200]})
                        prev = out
                    time.sleep(0.3)
                rec["monitor_timeline"] = tl
            if a.no_client:
                rc, out, err = hyprctl(xdg, ["-i", sig, "monitors", "-j"])
                rec["monitors_final_watch"] = json.loads(out) if out.strip().startswith("[") else out[:2000]
            # dispatch exec of the shm client from INSIDE the sandbox
            rec["xdg_listing"] = sorted(os.listdir(xdg))
            rc, out, err = hyprctl(xdg, ["-i", sig, "monitors", "-j"])
            rec["steps"].append({"do": "monitors -j (pre-client)", "rc": rc})
            try:
                rec["monitors_pre"] = json.loads(out)
            except ValueError:
                rec["monitors_pre_raw"] = out[:3000]
            clientcmd = ("" if a.no_client else
                         "sh -c 'WAYLAND_DISPLAY=%s exec %s --app-id %s %s 2>$HOME/.client-%s.log'"
                         % (a.client_display, a.client, a.app_id, a.client_args, a.case))
            rc, out, err = (0, "", "") if a.no_client else hyprctl(xdg, ["-i", sig, "dispatch", "exec", clientcmd])
            rec["steps"].append({"do": "dispatch exec " + clientcmd, "rc": rc,
                                 "stdout": out.strip()[:400], "stderr": err.strip()[:400]})
            rec["client_cmd"] = clientcmd
            # wait for the client to map and its size to settle
            want = a.app_id
            seen, stable, prev, t1 = None, 0, None, time.time()
            while time.time() - t1 < a.timeout:
                rc, out, err = hyprctl(xdg, ["-i", sig, "clients", "-j"])
                if rc == 0:
                    try:
                        data = json.loads(out)
                        if any(c.get("class") == want or c.get("initialClass") == want for c in data):
                            cur = json.dumps([c for c in data if c.get("class") == want
                                              or c.get("initialClass") == want], sort_keys=True)
                            if cur == prev:
                                stable += 1
                                if stable >= 3:
                                    seen = data
                                    break
                            else:
                                prev, stable = cur, 0
                    except ValueError:
                        pass
                time.sleep(0.4)
            rec["client_wait_seconds"] = round(time.time() - t1, 2)
            if seen is None:
                rec["error"] = "client %s never appeared/stable" % want
                rc, out, err = hyprctl(xdg, ["-i", sig, "clients", "-j"])
                rec["clients_raw_at_fail"] = out[:8000]
            else:
                rec["clients"] = seen
                rc, out, err = hyprctl(xdg, ["-i", sig, "monitors", "-j"])
                rec["steps"].append({"do": "monitors -j", "rc": rc})
                try:
                    rec["monitors"] = json.loads(out)
                except ValueError:
                    rec["monitors_raw"] = out[:4000]
                rc, out, err = hyprctl(xdg, ["-i", sig, "clients", "-j"])
                rec["steps"].append({"do": "clients -j (repeat)", "rc": rc})
                rec["clients_repeat_equal"] = out == prev
                try:
                    rec["clients_second"] = json.loads(out)
                except ValueError:
                    rec["clients_second_raw"] = out[:4000]
            rc, out, err = hyprctl(xdg, ["-i", sig, "dispatch", "exit"])
            rec["steps"].append({"do": "dispatch exit", "rc": rc})
            t2 = time.time()
            while time.time() - t2 < 10:
                rc, out, err = hyprctl(xdg, ["-i", sig, "version", "-j"], timeout=3)
                if rc != 0 or not out.strip():
                    break
                time.sleep(0.2)
            time.sleep(0.3)
    finally:
        try:
            os.killpg(p.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            p.wait(timeout=8)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            p.wait(timeout=8)
        rec["sandbox_rc"] = p.returncode
        log.close()
        shutil.rmtree(xdg, ignore_errors=True)
        rec["coredumps_after"] = coredumps()
        rec["sandbox_log_sha"] = sha(os.path.join(work, "sandbox.log"))
        with open(os.path.join(work, "sandbox.log"), "rb") as fh:
            b = fh.read()
        rec["sandbox_log_tail"] = b[-12000:].decode(errors="replace")
        hlog = os.path.join(xdg, "hypr", rec.get("instance_sig") or "", "hyprland.log")
        if os.path.exists(hlog):
            shutil.copyfile(hlog, os.path.join(work, "hyprland.log"))
            rec["hyprland_log_sha"] = sha(hlog)

    want = a.app_id
    clog = os.path.join(ohome, ".client-%s.log" % a.case)
    if os.path.exists(clog):
        rec["client_log"] = open(clog, errors="replace").read()[-4000:]
    hit = [c for c in rec.get("clients") or [] if c.get("class") == want]
    if hit:
        c = hit[0]
        rec["observation"] = {"class": c.get("class"), "initialClass": c.get("initialClass"),
                              "size": c.get("size"), "floating": c.get("floating"),
                              "mapped": c.get("mapped"), "at": c.get("at"),
                              "address": c.get("address"), "monitor": c.get("monitor"),
                              "title": c.get("title"), "fullscreen": c.get("fullscreen"),
                              "maximized": c.get("maximized")}
    json.dump(rec, open(os.path.join(work, "receipt.json"), "w"), indent=1, sort_keys=True)
    # reduced clients dump for the reference tool: class/size/floating/mapped/address/at/monitor
    red = [{k: c.get(k) for k in ("address", "class", "initialClass", "title", "size", "floating",
                                  "mapped", "at", "monitor")} for c in rec.get("clients") or []]
    json.dump(red, open(os.path.join(work, "clients-reduced.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({"case": a.case, "sig": rec.get("instance_sig"), "error": rec.get("error"),
                      "observation": rec.get("observation"),
                      "coredumps": [rec["coredumps_before"], rec["coredumps_after"]]}, sort_keys=True))
    return 0 if rec.get("observation") else 1


if __name__ == "__main__":
    sys.exit(main())
