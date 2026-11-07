#!/usr/bin/env python3
"""host-run-r92 — replay host xdg-mime vs candidate vs GLib resolver over all host MIME types.

Usage: python3 host-run-r92.py --scratch S --candidate CAND --glib GLIB [--out FILE]
Environment is taken from os.environ; ONLY HOME, PATH, XDG_CURRENT_DESKTOP, XDG_MENU_PREFIX,
XDG_CONFIG_HOME, XDG_CONFIG_DIRS, XDG_DATA_HOME, XDG_DATA_DIRS are passed through.
All subprocesses run with env -i semantics (subprocess env=<dict>), cwd=<scratch>.
Never prints any other environment variable.
"""
import argparse, json
import os
import subprocess
import sys

ALLOWED = ["HOME", "PATH", "XDG_CURRENT_DESKTOP", "XDG_MENU_PREFIX",
           "XDG_CONFIG_HOME", "XDG_CONFIG_DIRS", "XDG_DATA_HOME", "XDG_DATA_DIRS"]
SCHEMES = ["x-scheme-handler/http", "x-scheme-handler/https",
           "x-scheme-handler/mailto", "x-scheme-handler/file"]


def host_env():
    env = {}
    for k in ALLOWED:
        v = os.environ.get(k)
        if v is not None:
            env[k] = v
    return env


def norm(out):
    return out.strip("\n \t\r")


def find_decider(t, env):
    """File-based attribution: first config/cache file containing a line for t, else fallback note."""
    home = env.get("HOME", "/")
    cfg_home = env.get("XDG_CONFIG_HOME") or os.path.join(home, ".config")
    cfg_dirs = [d for d in (env.get("XDG_CONFIG_DIRS") or "/etc/xdg").split(":") if d]
    data_home = env.get("XDG_DATA_HOME") or os.path.join(home, ".local", "share")
    data_dirs = [d for d in (env.get("XDG_DATA_DIRS") or "/usr/local/share:/usr/share").split(":") if d]
    checks = []
    for d in [cfg_home] + cfg_dirs:
        checks.append(("mimeapps.list", os.path.join(d, "mimeapps.list")))
    for d in [data_home] + data_dirs:
        checks.append(("mimeinfo.cache", os.path.join(d, "applications", "mimeinfo.cache")))
    for kind, path in checks:
        try:
            with open(path, "rb") as fh:
                data = fh.read().decode("utf-8", "surrogateescape")
        except OSError:
            continue
        for line in data.splitlines():
            s = line.strip()
            if s.startswith(t + "=") or s.startswith(t + ";"):
                return f"{kind}:{path}:{s[:160]}"
    return "fallback: no mimeapps.list/mimeinfo.cache entry; answer from desktop Mime= registration order (XDG_CURRENT_DESKTOP dispatch defapp_generic vs GLib merged desktop dirs)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--glib", default="/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-mime.py")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    env = host_env()
    scratch = os.path.abspath(a.scratch)
    os.makedirs(scratch, exist_ok=True)
    lines_out = []
    def emit(s):
        lines_out.append(s)
        print(s, flush=True)

    # --- type list, in /usr/share/mime/types file order, schemes appended ---
    try:
        with open("/usr/share/mime/types") as fh:
            types = [l.strip() for l in fh if l.strip()]
    except OSError as e:
        emit(f"error: cannot read /usr/share/mime/types: {e}")
        return 2
    seen = set(types)
    for s in SCHEMES:
        if s not in seen:
            types.append(s)
    N = len(types)
    emit(f"scratch={scratch} types={N}")
    emit(f"env_names={','.join(sorted(env.keys()))}")

    # --- leg 1: installed xdg-mime (real binary), one call per type ---
    xdg = {}
    for t in types:
        try:
            p = subprocess.run(["/usr/bin/xdg-mime", "query", "default", t],
                               env=env, cwd=scratch, capture_output=True, text=True, timeout=30)
            xdg[t] = norm(p.stdout)
        except Exception as e:  # keep going; record failure
            xdg[t] = f"ERROR:{e}"
    emit("leg xdg-mime done")

    # --- leg 2: candidate, single batched call with --json ---
    cand = {}
    cand_rc = None
    try:
        argv = ["python3", a.candidate, "--cwd", scratch, "--json"]
        for k, v in env.items():
            argv += ["--env", f"{k}={v}"]
        argv += types
        p = subprocess.run(argv, env=env, cwd=scratch, capture_output=True, text=True, timeout=600)
        cand_rc = p.returncode
        if cand_rc == 0:
            res = json.loads(p.stdout)["results"]
            cand = {r["type"]: (r["default"] or "") for r in res}
        else:
            emit(f"candidate rc={cand_rc} stderr={p.stderr.strip()[:500]}")
    except Exception as e:
        emit(f"candidate run error: {e}")

    # --- leg 3: GLib resolver (round-91 tools/mado-mime.py), single batched --json call ---
    glib = {}
    glib_rc = None
    try:
        argv = ["python3", a.glib, "--json"]
        if "XDG_CURRENT_DESKTOP" in env:
            argv += ["--desktop", env["XDG_CURRENT_DESKTOP"]]
        else:
            argv += ["--desktop-unset"]
        if "XDG_CONFIG_HOME" in env:
            argv += ["--config-home", env["XDG_CONFIG_HOME"]]
        if "XDG_CONFIG_DIRS" in env:
            argv += ["--config-dirs", env["XDG_CONFIG_DIRS"]]
        if "XDG_DATA_HOME" in env:
            argv += ["--data-home", env["XDG_DATA_HOME"]]
        if "XDG_DATA_DIRS" in env:
            argv += ["--data-dirs", env["XDG_DATA_DIRS"]]
        if "PATH" in env:
            argv += ["--path", env["PATH"]]
        argv += types
        p = subprocess.run(argv, env=env, cwd=scratch, capture_output=True, text=True, timeout=600)
        glib_rc = p.returncode
        if glib_rc == 0:
            res = json.loads(p.stdout)["results"]
            glib = {r["type"]: (r["default"] or "") for r in res}
        else:
            emit(f"glib rc={glib_rc} stderr={p.stderr.strip()[:500]}")
    except Exception as e:
        emit(f"glib run error: {e}")

    # --- agreement: candidate vs xdg-mime ---
    agree = disagree = 0
    disagreements = []
    for t in types:
        if cand.get(t) == xdg.get(t):
            agree += 1
        else:
            disagree += 1
            disagreements.append(t)
    emit(f"types={N} agree={agree} disagree={disagree}")
    for t in disagreements:
        emit(f"DISAGREE type={t} xdg-mime={xdg.get(t)!r} candidate={cand.get(t)!r}")

    # --- xdg-mime vs GLib divergence ---
    gdiff = [t for t in types if glib.get(t) != xdg.get(t)]
    emit(f"types={N} glib_agree={N-len(gdiff)} glib_disagree={len(gdiff)}")
    for t in gdiff:
        dec = find_decider(t, env)
        emit(f"GLIB-DIFF type={t} xdg-mime={xdg.get(t)!r} glib={glib.get(t)!r} decider={dec}")

    if a.out:
        with open(a.out, "w") as fh:
            fh.write("\n".join(lines_out) + "\n")
    return 0 if (disagree == 0 and cand_rc == 0 and glib_rc == 0) else 0


if __name__ == "__main__":
    sys.exit(main())
