#!/usr/bin/env python3
"""mado round 26 shared harness: Hyprland v0.56.2 as an oracle, headless and isolated from the
operator's live session, plus a label-free sandbox for the tool under test.

Isolation method (pilot recorded in .ufo/waves/round-26/harness/pilot-receipt.txt):
  * Hyprland 0.56.2 cannot run headless-only (aquamarine needs a DRM fd for its allocator; a
    headless-only start aborts with `CBackend::create() failed!`). So each nested Hyprland gets its
    own private parent compositor: tinywl from wlroots 0.20.2 (commit d7835334), built with
    -Dbackends= -Dsession=disabled -Dxwayland=disabled -Drenderers=gles2 -Dallocators=gbm, patched
    to offer wl_compositor v6 and xdg_wm_base v6 (harness/tinywl-global-versions.patch; aquamarine
    binds those versions), run with WLR_BACKENDS=headless.
  * Both run inside one bubblewrap sandbox: --unshare-all (no network, own pid/ipc/uts), --clearenv
    (no WAYLAND_DISPLAY, HYPRLAND_INSTANCE_SIGNATURE or DBUS address inherited), --tmpfs /run (no host
    runtime dir, no D-Bus or logind socket), a private XDG_RUNTIME_DIR (mkdtemp under /tmp), /dev
    with only the amdgpu render node /dev/dri/renderD129 (no DRM card node, no input device),
    LIBSEAT_BACKEND=noop, RLIMIT_CORE=0 and RLIMIT_AS 8 GB.
  * The counter talks to the instance with the host's hyprctl under env -i XDG_RUNTIME_DIR=<private>,
    and stops it with `hyprctl dispatch exit` (a clean exit), then kills the sandbox process group.
  * Host Hyprland coredump count (coredumpctl) is read before and after each run and printed.

Tool sandbox (M25-2 repair): every case tree lives in a directory with a random mkdtemp name, so
/proc/self/mountinfo inside the sandbox names no case type; cases are run in a shuffled order.
"""
import collections, fcntl, hashlib, json, os, re, shutil, signal, subprocess, tempfile, time

TINYWL = "/fast/scratch/hyaku/mado-r26/wlroots/build/tinywl/tinywl"
TINYWL_SHA = "227a74af3455c4cd90ef0fc64edf3c927ddf7f0b9b4bf903bdc30b3aeea40cda"
LIBWLR = "/fast/scratch/hyaku/mado-r26/wlroots/build/libwlroots-0.20.so"
LIBWLR_SHA = "1f3d7036c91417c0b6efccf67ad0d368a30818df630f07bb92574a13527a7967"
WLR_DIR = "/fast/scratch/hyaku/mado-r26/wlroots/build"
RENDER_NODE = "/dev/dri/renderD129"
SLOT_DIR = "/fast/scratch/hyaku/mado-r27-oracle-slots"
SLOTS = 12
ROOTS = [".config/hypr", ".config/omarchy/current/theme", ".local/share/omarchy/default/hypr",
         ".local/state/omarchy/toggles/hypr"]
EXEC_RE = re.compile(r"^\s*exec(?:r)?(?:-once|-shutdown)?\s*=")
ORACLE_EXTRA = ["", "ecosystem {", "    no_update_news = true", "    no_donation_nag = true", "}", ""]


class SetupError(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def check_build():
    for path, want in ((TINYWL, TINYWL_SHA), (LIBWLR, LIBWLR_SHA)):
        try:
            got = sha(open(path, "rb").read())
        except OSError as ex:
            raise SetupError("harness binary missing %s: %s" % (path, ex))
        if got != want:
            raise SetupError("harness binary %s sha256 %s != pin %s" % (path, got, want))
    if not os.path.exists(RENDER_NODE):
        raise SetupError("render node %s missing" % RENDER_NODE)


def coredumps():
    p = subprocess.run(["coredumpctl", "list", "--no-pager", "--no-legend"], capture_output=True, text=True)
    return sum(1 for ln in p.stdout.splitlines() if "/usr/bin/Hyprland" in ln)


def snapshot(home_src, home_dst):
    """Copy the four Hyprland config roots (files <= 1 MiB). Returns (nfiles, digest)."""
    digest = hashlib.sha256()
    nfiles = 0
    for r in ROOTS:
        src = os.path.join(home_src, r)
        if not os.path.exists(src):
            continue
        real = os.path.realpath(src)
        for dp, dn, fn in os.walk(real):
            dn.sort()
            for f in sorted(fn):
                p = os.path.join(dp, f)
                if os.path.islink(p) and not os.path.realpath(p).startswith(os.path.realpath(home_src) + os.sep):
                    continue  # r27 (r26 w1 SentinelHarness): never copy bytes a symlink pulls in from outside HOME
                if not os.path.isfile(p) or os.path.getsize(p) > 1 << 20:
                    continue
                rel = os.path.relpath(p, real)
                dst = os.path.join(home_dst, r, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                b = open(p, "rb").read()
                with open(dst, "wb") as fh:
                    fh.write(b)
                digest.update((r + "/" + rel).encode() + b"\0" + sha(b).encode() + b"\n")
                nfiles += 1
    return nfiles, digest.hexdigest()


def strip_exec(home):
    removed = 0
    for dp, dn, fn in os.walk(home):
        for f in fn:
            p = os.path.join(dp, f)
            try:
                text = open(p, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            lines = text.split("\n")
            keep = [ln for ln in lines if not EXEC_RE.match(ln)]
            if len(keep) != len(lines):
                removed += len(lines) - len(keep)
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write("\n".join(keep))
    return removed


class Slot:
    def __enter__(self):
        os.makedirs(SLOT_DIR, exist_ok=True)
        while True:
            for i in range(SLOTS):
                fh = open(os.path.join(SLOT_DIR, "slot-%d.lock" % i), "w")
                try:
                    fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self.fh = fh
                    return self
                except OSError:
                    fh.close()
            time.sleep(0.2)

    def __exit__(self, *exc):
        fcntl.flock(self.fh, fcntl.LOCK_UN)
        self.fh.close()


def _hyprctl(xdg, args, timeout=10):
    env = {"PATH": "/usr/bin", "XDG_RUNTIME_DIR": xdg}
    p = subprocess.run(["timeout", str(timeout), "hyprctl"] + args, capture_output=True, env=env)
    return p.returncode, p.stdout


def oracle(case_home, work, verbs):
    """Hyprland v0.56.2's own `hyprctl <verb> -j` output for each verb, for a copy of case_home
    (exec lines stripped, ORACLE_EXTRA appended). Returns ({verb: parsed}, "") or (None, error)."""
    os.makedirs(work, exist_ok=True)
    ohome = os.path.join(work, "home")
    shutil.copytree(case_home, ohome, symlinks=False)
    strip_exec(ohome)
    root = os.path.join(ohome, ".config/hypr/hyprland.conf")
    with open(root, "a", encoding="utf-8") as fh:
        fh.write("\n".join(ORACLE_EXTRA))
    xdg = tempfile.mkdtemp(prefix="m27o-", dir="/tmp")
    os.chmod(xdg, 0o700)
    cmd = ["env", "-i", "PATH=/usr/bin", "prlimit", "--core=0", "--as=8000000000", "--",
           "bwrap", "--unshare-all", "--die-with-parent", "--new-session",
           "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
           "--symlink", "usr/lib", "/lib64", "--symlink", "usr/bin", "/sbin", "--ro-bind", "/etc", "/etc",
           "--dev", "/dev", "--dev-bind", RENDER_NODE, RENDER_NODE,
           "--ro-bind", "/sys/dev/char", "/sys/dev/char", "--ro-bind", "/sys/devices", "/sys/devices",
           "--ro-bind", "/sys/class/drm", "/sys/class/drm", "--proc", "/proc", "--tmpfs", "/run",
           "--tmpfs", "/tmp", "--ro-bind", WLR_DIR, WLR_DIR, "--bind", ohome, ohome, "--bind", xdg, xdg,
           "--clearenv", "--setenv", "PATH", "/usr/bin", "--setenv", "HOME", ohome,
           "--setenv", "XDG_RUNTIME_DIR", xdg, "--setenv", "WLR_BACKENDS", "headless",
           "--setenv", "WLR_HEADLESS_OUTPUTS", "1", "--setenv", "WLR_RENDERER", "gles2",
           "--setenv", "WLR_RENDER_DRM_DEVICE", RENDER_NODE, "--setenv", "LIBSEAT_BACKEND", "noop",
           "--setenv", "HYPRLAND_NO_CRASHREPORTER", "1", "--setenv", "HYPRLAND_NO_SD_NOTIFY", "1",
           "--setenv", "HYPRLAND_NO_SD_VARS", "1", "--chdir", ohome,
           TINYWL, "-s", "exec Hyprland -c '%s'" % root]
    with Slot():
        log = open(os.path.join(work, "sandbox.log"), "wb")
        p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                             start_new_session=True)
        sig = None
        try:
            t0 = time.time()
            while sig is None and time.time() - t0 < 40:
                if p.poll() is not None:
                    return None, "sandbox exited rc=%s before answering" % p.returncode
                rc, out = _hyprctl(xdg, ["instances", "-j"])
                if rc == 0:
                    try:
                        inst = json.loads(out)
                        if inst:
                            sig = inst[0]["instance"]
                    except (ValueError, KeyError, IndexError, TypeError):
                        pass
                if sig is None:
                    time.sleep(0.25)
            if sig is None:
                return None, "no nested instance within 40 s"
            result = {}
            for verb in verbs:
                prev, same, t1 = None, 0, time.time()
                while verb not in result and time.time() - t1 < 30:
                    rc, out = _hyprctl(xdg, ["-i", sig, verb, "-j"])
                    if rc == 0:
                        try:
                            data = json.loads(out)
                        except ValueError:
                            data = None
                        if data is not None:
                            if out == prev:
                                same += 1
                                if same >= 2:
                                    result[verb] = data
                            else:
                                prev, same = out, 0
                    time.sleep(0.3)
                if verb not in result:
                    return None, "%s -j never stable within 30 s" % verb
            _hyprctl(xdg, ["-i", sig, "dispatch", "exit"])
            t2 = time.time()
            while time.time() - t2 < 10:
                rc, out = _hyprctl(xdg, ["-i", sig, "version", "-j"], timeout=3)
                if rc != 0 or not out.strip():
                    break
                time.sleep(0.2)
            time.sleep(0.3)
            return result, ""
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
            log.close()
            shutil.rmtree(xdg, ignore_errors=True)


def run_tool(tool, case_home, timeout=60):
    """Run `python3 -I tool --home /snap/home` in a sandbox (no network, no /run, cleared env) with
    the case tree read-only at a fixed path. The bind source is a random directory name (M25-2)."""
    cmd = ["env", "-i", "PATH=/usr/bin", "timeout", str(timeout), "bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib",
           "--symlink", "usr/lib64", "/lib64", "--symlink", "usr/bin", "/bin", "--proc", "/proc",
           "--dev", "/dev", "--tmpfs", "/tmp", "--ro-bind", case_home, "/snap/home",
           "--ro-bind", tool, "/snap/tool.py", "--unshare-all", "--die-with-parent", "--clearenv",
           "--setenv", "PATH", "/usr/bin", "--setenv", "HOME", "/snap/home",
           "python3", "-I", "/snap/tool.py", "--home", "/snap/home"]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        return None, "exit=%d stderr=%s" % (p.returncode, p.stderr.decode(errors="replace")[-200:].replace("\n", " | "))
    try:
        return json.loads(p.stdout), ""
    except ValueError:
        return None, "stdout is not JSON"
