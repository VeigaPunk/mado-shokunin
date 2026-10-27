#!/usr/bin/env python3
"""selftest-probe.py — run one drafted tool through a spec of cases, hermetically.

Seat ExecDiskHygiene, round 51. Verifies scratch-rule-4 behaviour at runtime:

  * every case runs under `python3 -I` (isolated mode: no PYTHONPATH, no user site,
    no cwd on sys.path) with a minimal, explicit environment;
  * the case's TMPDIR / --work point inside `--scratch`, never at /tmp;
  * `isolate_tmp` cases run inside a private user+mount namespace whose /tmp and
    /var/tmp are fresh tmpfs mounts: whatever the tool writes there is listed
    afterwards, so "wrote nothing to /tmp" is measured, not assumed;
  * a case can demand a refusal (`expect_exit: 2`) for a /tmp-ish work dir.

This probe writes only under its `--scratch` argument (which must not be under
/tmp, /var/tmp or /dev/shm) and the optional `--out` receipt. It reads the tool;
it never edits it.

Usage:
  python3 -I selftest-probe.py --spec cases.json --scratch <dir> [--out receipt.json]

Spec:
  {"tool": "/abs/path/tool.py",
   "cases": [{"name": "selftest", "argv": ["--selftest"],
              "env": {"TMPDIR": "{scratch}/tmp"}, "expect_exit": 0,
              "isolate_tmp": false, "note": "..."}]}
Placeholders in argv/env values: {scratch} {tool} {lane} {base_rev}
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

TMPISH = ("/tmp", "/var/tmp", "/dev/shm")


def die(msg, code=2):
    print("selftest-probe: " + msg, file=sys.stderr)
    sys.exit(code)


def expand(value, ctx):
    if isinstance(value, str):
        return value.format(**ctx)
    return value


def check_scratch(scratch):
    rp = os.path.realpath(scratch)
    for bad in TMPISH:
        if rp == bad or rp.startswith(bad + os.sep):
            die("scratch under %s refused: %s" % (bad, rp))
    return rp


def ns_script(argv, envpairs, ns_pre=""):
    """A shell program for `unshare -Urm`: private tmpfs /tmp + /var/tmp, then run."""
    envbits = " ".join("%s=%s" % (k, shq(v)) for k, v in envpairs)
    cmd = " ".join(shq(a) for a in argv)
    return (
        "mount -t tmpfs tmpfs /tmp || exit 90\n"
        "mount -t tmpfs tmpfs /var/tmp || exit 91\n"
        + (ns_pre.strip() + "\n" if ns_pre.strip() else "")
        + "env -i %s %s\n"
        "rc=$?\n"
        "echo \"__PROBE_EXIT__=$rc\"\n"
        "echo __PROBE_TMP_RESIDUE__\n"
        "find /tmp /var/tmp -mindepth 1 2>/dev/null | sort\n"
        "echo __PROBE_END__\n"
        "exit $rc\n" % (envbits, cmd)
    )


def shq(s):
    return "'" + str(s).replace("'", "'\\''") + "'"


def run_case(case, tool, scratch, ctx):
    name = case["name"]
    argv = [sys.executable] + ["-I", tool] + [expand(a, ctx) for a in case.get("argv", [])]
    envmap = {k: expand(v, ctx) for k, v in case.get("env", {}).items()}
    base_env = {
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "HOME": os.path.join(scratch, "home"),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
    }
    os.makedirs(base_env["HOME"], exist_ok=True)
    cwd = os.path.join(scratch, "cwd")
    os.makedirs(cwd, exist_ok=True)
    env = dict(base_env)
    env.update(envmap)
    envpairs = sorted(env.items())

    for mk in case.get("mkdir", []):
        os.makedirs(expand(mk, ctx), exist_ok=True)
    isolate = bool(case.get("isolate_tmp"))
    started = time.time()
    if isolate:
        prog = ns_script(argv, envpairs, case.get("ns_pre", ""))
        cp = subprocess.run(
            ["unshare", "-Urm", "sh", "-c", prog],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=case.get("timeout", 900),
        )
        out = cp.stdout
        residue = []
        exit_code = cp.returncode
        if "__PROBE_EXIT__=" in out:
            tail = out.split("__PROBE_TMP_RESIDUE__", 1)
            body = tail[0]
            for line in body.splitlines():
                if line.startswith("__PROBE_EXIT__="):
                    exit_code = int(line.split("=", 1)[1].strip())
            if len(tail) == 2:
                middle = tail[1].split("__PROBE_END__", 1)[0]
                residue = [l for l in middle.splitlines() if l.strip()]
            stdout_text = body
        else:
            stdout_text = out
    else:
        cp = subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=case.get("timeout", 900),
        )
        exit_code = cp.returncode
        stdout_text = cp.stdout
        residue = None
    elapsed = round(time.time() - started, 2)

    expect = case.get("expect_exit")
    ok = (expect is None) or (exit_code == expect)
    if isolate and case.get("expect_no_tmp_writes"):
        ok = ok and not residue
    return {
        "name": name,
        "note": case.get("note", ""),
        "argv": argv,
        "env": envmap,
        "isolate_tmp": isolate,
        "exit": exit_code,
        "expect_exit": expect,
        "ok": bool(ok),
        "seconds": elapsed,
        "tmp_residue": residue,
        "stdout_tail": "\n".join(stdout_text.rstrip().splitlines()[-14:]),
        "stderr_tail": "\n".join(cp.stderr.rstrip().splitlines()[-10:]),
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    scratch = check_scratch(args.scratch)
    if not (shutil.which("unshare") or True):
        pass
    with open(args.spec, "r", encoding="utf-8") as fh:
        spec = json.load(fh)
    tool = os.path.abspath(spec["tool"])
    if not os.path.isfile(tool):
        die("tool not found: " + tool)
    ctx = {
        "scratch": scratch,
        "tool": tool,
        "lane": spec.get("lane", ""),
        "base_rev": spec.get("base_rev", ""),
    }
    os.makedirs(scratch, exist_ok=True)

    results = []
    for case in spec["cases"]:
        r = run_case(case, tool, scratch, ctx)
        results.append(r)
        print(
            "%-28s exit=%-3s expect=%-4s %s %ss%s"
            % (
                r["name"],
                r["exit"],
                r["expect_exit"],
                "OK" if r["ok"] else "FAIL",
                r["seconds"],
                "" if r["tmp_residue"] is None else " tmp_residue=%d" % len(r["tmp_residue"]),
            )
        )
        for line in r["stdout_tail"].splitlines():
            print("    | " + line)
        if r["stderr_tail"]:
            for line in r["stderr_tail"].splitlines():
                print("    ! " + line)
        if r["tmp_residue"]:
            for line in r["tmp_residue"][:20]:
                print("    TMP " + line)
    bad = [r["name"] for r in results if not r["ok"]]
    print(
        "PROBE tool=%s cases=%d failed=%d %s"
        % (tool, len(results), len(bad), ("failed=" + ",".join(bad)) if bad else "all-ok")
    )
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump({"tool": tool, "scratch": scratch, "cases": results}, fh, indent=1)
            fh.write("\n")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
