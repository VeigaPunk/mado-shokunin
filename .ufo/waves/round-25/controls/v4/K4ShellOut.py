#!/usr/bin/env python3
"""ORACLE SHELL-OUT control: ask Hyprland, never resolve bind syntax.

Run only in the counter's isolated /snap/home sandbox. The input is copied
and exec keyword lines removed before any compositor process is launched.
Each attempt gets a private writable runtime, bounded logs and process group.
Only actual bind JSON from our instance or its output is returned; otherwise [].
Diagnostics go to stderr, not the required JSON stdout.
"""
import argparse
import glob
import json
import os
import re
import resource
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time

FIELDS = frozenset(("locked", "mouse", "release", "repeat", "longPress",
                    "non_consuming", "auto_consuming", "has_description",
                    "modmask", "submap", "submap_universal", "key", "keycode",
                    "catch_all", "description", "allow_input_capture",
                    "dispatcher", "arg"))
EXEC = re.compile(r"^\s*exec(?:r)?(?:-once|-shutdown)?\s*=")
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
MAX_LOG = 2 * 1024 * 1024


def report(message):
    print(message, file=sys.stderr, flush=True)


def valid_table(value):
    return (isinstance(value, list) and
            all(isinstance(row, dict) and FIELDS <= row.keys() for row in value))


def json_table(raw):
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        return None
    return value if valid_table(value) else None


def from_log(text):
    """Recognize complete JSON output, not a partial bind grammar or cache."""
    text = ANSI.sub("", text)
    table = json_table(text)
    if table is not None:
        return table
    decoder = json.JSONDecoder()
    rows = []
    for match in re.finditer(r"[\[{]", text):
        try:
            value, _ = decoder.raw_decode(text, match.start())
        except ValueError:
            continue
        if isinstance(value, list) and value and valid_table(value):
            return value
        if isinstance(value, dict) and FIELDS <= value.keys():
            rows.append(value)
    return rows or None


def limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_LOG, MAX_LOG))
    resource.setrlimit(resource.RLIMIT_AS, (4_000_000_000, 4_000_000_000))


def stop_group(process):
    # Kill the group even if its leader already exited, so no children survive.
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=0.3)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait(timeout=1)


def query_own(runtime, env, queries):
    # This runtime directory was created exclusively for one child instance.
    for path in sorted(glob.glob(runtime + "/hypr/*/.socket.sock")):
        instance = os.path.basename(os.path.dirname(path))
        queries.add(instance)
        try:
            reply = subprocess.run(
                ["timeout", "0.5", "hyprctl", "-i", instance, "binds", "-j"],
                env=env, stdin=subprocess.DEVNULL, capture_output=True,
                timeout=0.8, preexec_fn=limits)
            table = json_table(reply.stdout)
            if reply.returncode == 0 and table is not None:
                return table
        except (OSError, subprocess.TimeoutExpired):
            pass
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
                client.settimeout(0.2)
                client.connect(path)
                client.sendall(b"j/binds")
                chunks = []
                size = 0
                while size < MAX_LOG:
                    part = client.recv(min(65536, MAX_LOG - size))
                    if not part:
                        break
                    chunks.append(part)
                    size += len(part)
                table = json_table(b"".join(chunks))
                if table is not None:
                    return table
        except OSError:
            pass
    return None


def attempt(name, flags, changes, home, work, deadline):
    runtime = os.path.join(work, "r%d" % len(os.listdir(work)))
    os.mkdir(runtime, 0o700)
    env = {"PATH": "/usr/bin", "HOME": home,
           "HYPRLAND_NO_CRASHREPORTER": "1", "HYPRLAND_NO_RT": "1",
           "HYPRLAND_NO_SD_NOTIFY": "1", "HYPRLAND_NO_SD_VARS": "1"}
    if changes is not None:
        env["XDG_RUNTIME_DIR"] = runtime
        env["XDG_CACHE_HOME"] = runtime + "/cache"
        env.update(changes)
    command = ["Hyprland", "-c", home + "/.config/hypr/hyprland.conf"] + flags
    queries = set()
    table = None
    with tempfile.TemporaryFile(dir=work) as output:
        try:
            child = subprocess.Popen(command, env=env, cwd=home,
                                     stdin=subprocess.DEVNULL, stdout=output,
                                     stderr=subprocess.STDOUT,
                                     start_new_session=True, preexec_fn=limits)
        except OSError as error:
            report("ATTEMPT %s launch_error=%r" % (name, error))
            return None
        try:
            until = min(deadline, time.monotonic() + 3)
            while time.monotonic() < until:
                table = query_own(runtime, env, queries)
                if table is not None or child.poll() is not None:
                    break
                time.sleep(0.04)
        finally:
            natural_rc = child.poll()
            stop_group(child)
        output.seek(0)
        text = output.read(MAX_LOG).decode("utf-8", errors="replace")
    for path in sorted(glob.glob(runtime + "/hypr/*/hyprland.log")):
        with open(path, "rb") as log:
            text += "\n" + log.read(MAX_LOG).decode("utf-8", errors="replace")
    if table is None:
        table = from_log(text)
    report("ATTEMPT %s natural_exit=%s final_exit=%s queried_instances=%d table=%s" %
           (name, natural_rc, child.returncode, len(queries),
            "none" if table is None else len(table)))
    # Exact bounded output is available for the small diagnostic probe too.
    report("LOG %s begin\n%s\nLOG %s end" % (name, text[:24000], name))
    return table


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", required=True)
    args = parser.parse_args()
    # Never launch on the live host, even if accidentally invoked there.
    if os.path.realpath(args.home) != "/snap/home" or os.path.exists("/run"):
        report("REFUSED: this control runs only in the counter sandbox")
        print("[]")
        return 0
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    with tempfile.TemporaryDirectory(prefix="k", dir="/tmp") as work:
        home = os.path.join(work, "home")
        shutil.copytree(args.home, home, symlinks=False)
        removed = 0
        for directory, _, files in os.walk(home):
            for name in files:
                path = os.path.join(directory, name)
                with open(path, "rb") as source:
                    raw = source.read()
                if b"\0" in raw:
                    continue
                try:
                    text = raw.decode("utf-8")
                except UnicodeDecodeError:
                    continue
                lines = text.split("\n")
                kept = [line for line in lines if not EXEC.match(line)]
                if len(kept) != len(lines):
                    removed += len(lines) - len(kept)
                    with open(path, "w", encoding="utf-8") as target:
                        target.write("\n".join(kept))
        root = home + "/.config/hypr/hyprland.conf"
        with open(root, "a", encoding="utf-8") as config:
            config.write("\necosystem {\n no_update_news = true\n no_donation_nag = true\n}\n"
                         "debug {\n disable_logs = false\n enable_stdout_logs = true\n}\n")
        report("SANDBOX exec_lines_removed=%d run_exists=%s dri_exists=%s" %
               (removed, os.path.exists("/run"), os.path.exists("/dev/dri")))
        headless = {"AQ_BACKEND": "headless", "AQ_NO_DRM": "1", "AQ_DRM_DEVICES": "",
                    "WLR_BACKENDS": "headless", "WLR_HEADLESS_OUTPUTS": "1",
                    "WLR_RENDERER": "pixman", "WLR_LIBINPUT_NO_DEVICES": "1",
                    "WLR_NO_HARDWARE_CURSORS": "1"}
        software = dict(headless, LIBGL_ALWAYS_SOFTWARE="1", GALLIUM_DRIVER="llvmpipe",
                        MESA_LOADER_DRIVER_OVERRIDE="llvmpipe", EGL_PLATFORM="surfaceless",
                        AQ_TRACE="1", HYPRLAND_TRACE="1")
        modes = [
            ("cleared-no-runtime", [], None),
            ("runtime-no-display", [], {}),
            ("aq-headless", [], headless),
            ("headless-llvmpipe", [], software),
            ("headless-softpipe", [], dict(software, GALLIUM_DRIVER="softpipe")),
            ("aq-null", [], dict(software, AQ_BACKEND="null")),
            ("wayland-fallback", [], dict(software, AQ_BACKEND="wayland", WAYLAND_DISPLAY="wayland-0")),
            ("x11-fallback", [], dict(software, AQ_BACKEND="x11", WLR_BACKENDS="x11", DISPLAY=":0")),
            ("verify-config", ["--verify-config"], {}),
            ("verify-config-trace", ["--verify-config"], software),
        ]
        deadline = time.monotonic() + 48
        for name, flags, changes in modes:
            if time.monotonic() >= deadline:
                report("DEADLINE before " + name)
                break
            table = attempt(name, flags, changes, home, work, deadline)
            if table is not None:
                print(json.dumps(table))
                return 0
    print("[]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
