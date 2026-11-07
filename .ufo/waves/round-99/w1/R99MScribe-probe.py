#!/usr/bin/env python3
"""R99MScribe read-only launch probe: builds a case root, runs /usr/bin/gio launch
under env -i with a PATH holding only the case's own bin dirs, reads the child records.
Instrument, not candidate: it spawns gio and the fixture probe only."""
import json
import os
import shutil
import stat
import subprocess
import sys
import time

SCRATCH = "/fast/scratch/hyaku/mado-r99/R99MScribe"
GIO = "/usr/bin/gio"

PROBE_SH = """#!/bin/sh
{
  printf 'P0=%s\\n' "$0"
  printf 'PC=%s\\n' "$#"
  i=1
  for a in "$@"; do printf 'PA%s=%s\\n' "$i" "$a"; i=$((i+1)); done
  printf 'CWD=%s\\n' "$PWD"
  printf 'GDF=%s\\n' "${GIO_LAUNCHED_DESKTOP_FILE-<unset>}"
  printf 'DSI=%s\\n' "${DESKTOP_STARTUP_ID-<unset>}"
  printf 'XAT=%s\\n' "${XDG_ACTIVATION_TOKEN-<unset>}"
} >> "$PROBE_OUT"
"""

TERM_SH = """#!/bin/sh
{
  printf 'T0=%s\\n' "$0"
  printf 'TC=%s\\n' "$#"
  printf 'TA1=%s\\n' "${1-<none>}"
} >> "$PROBE_OUT"
shift_arg="$1"
case "$shift_arg" in
  -e|-x|--) shift ;;
esac
exec "$@"
"""

CASES = [
    # id, class, path entries (rel to root), files {rel: text}, dirs, desktop {k:v}, args, expect
    dict(id="p01-term-order-xdg", cls="terminal-order",
         path=["bin1"], files={"bin1/probe.sh": PROBE_SH,
                               "bin1/xdg-terminal-exec": TERM_SH,
                               "bin1/kgx": TERM_SH},
         dirs=["work"],
         desktop={"Exec": "{root}/bin1/probe.sh %f", "Terminal": "true",
                  "Path": "{root}/work"},
         args=["work/f1.txt"], expect={"rc": 0, "T0": "{root}/bin1/xdg-terminal-exec",
                                       "TC": "2", "TA1": "{root}/bin1/probe.sh",
                                       "PC": "1", "PA1": "{root}/work/f1.txt",
                                       "CWD": "{root}/work"}),
    dict(id="p02-term-kgx-execarg", cls="terminal-execarg",
         path=["bin2"], files={"bin2/probe.sh": PROBE_SH, "bin2/kgx": TERM_SH},
         dirs=["work"],
         desktop={"Exec": "{root}/bin2/probe.sh %f", "Terminal": "true",
                  "Path": "{root}/work"},
         args=["work/f1.txt"], expect={"rc": 0, "T0": "{root}/bin2/kgx", "TA1": "-e",
                                       "TC": "3", "PC": "1",
                                       "PA1": "{root}/work/f1.txt", "CWD": "{root}/work"}),
    dict(id="p03-term-xterm-execarg", cls="terminal-execarg",
         path=["bin3"], files={"bin3/probe.sh": PROBE_SH, "bin3/xterm": TERM_SH},
         dirs=["work"],
         desktop={"Exec": "{root}/bin3/probe.sh %f", "Terminal": "true",
                  "Path": "{root}/work"},
         args=["work/f1.txt"], expect={"rc": 0, "T0": "{root}/bin3/xterm", "TA1": "-e",
                                       "TC": "3"}),
    dict(id="p04-term-gnome-dashdash", cls="terminal-execarg",
         path=["bin4"], files={"bin4/probe.sh": PROBE_SH, "bin4/gnome-terminal": TERM_SH},
         dirs=["work"],
         desktop={"Exec": "{root}/bin4/probe.sh %f", "Terminal": "true",
                  "Path": "{root}/work"},
         args=["work/f1.txt"], expect={"rc": 0, "T0": "{root}/bin4/gnome-terminal",
                                       "TA1": "--", "TC": "3"}),
    dict(id="p05-term-none", cls="no-terminal",
         path=["bin5"], files={"bin5/probe.sh": PROBE_SH}, dirs=["work"],
         desktop={"Exec": "{root}/bin5/probe.sh %f", "Terminal": "true",
                  "Path": "{root}/work"},
         args=["work/f1.txt"],
         expect={"rc": 1, "stderr": "Unable to find terminal required for application"}),
    dict(id="p06-path-cwd", cls="path-cwd",
         path=["bin6"], files={"bin6/probe.sh": PROBE_SH}, dirs=["work"],
         desktop={"Exec": "{root}/bin6/probe.sh", "Path": "{root}/work"},
         args=[], expect={"rc": 0, "CWD": "{root}/work"}),
    dict(id="p07-path-empty-inherits", cls="path-empty",
         path=["bin7"], files={"bin7/probe.sh": PROBE_SH}, dirs=["work"],
         desktop={"Exec": "{root}/bin7/probe.sh", "Path": ""},
         args=[], expect={"rc": 0, "CWD": "{root}"}),
    dict(id="p08-path-missing", cls="cwd-failed",
         path=["bin8"], files={"bin8/probe.sh": PROBE_SH}, dirs=["work"],
         desktop={"Exec": "{root}/bin8/probe.sh", "Path": "{root}/nope"},
         args=[], expect={"rc": 1, "stderr": "Failed to change to directory"}),
    dict(id="p09-bare-not-found", cls="load-gate",
         path=["bin9"], files={"bin9/probe.sh": PROBE_SH}, dirs=[],
         desktop={"Exec": "nosuchprog-xyz %f"}, args=["x.txt"],
         expect={"rc": 1, "stderr": "Unable to load application information"}),
    dict(id="p10-loadgate-workdir", cls="load-gate-workdir",
         path=["bin10", "empty10"], files={"bin10/probe.sh": PROBE_SH}, dirs=["work"],
         desktop={"Exec": "probe.sh %f", "Path": "{root}/bin10"},
         args=["work/f1.txt"],
         expect={"rc": 0, "P0": "{root}/bin10/probe.sh", "PA1": "{root}/work/f1.txt",
                 "CWD": "{root}/bin10"}),
    dict(id="p11-loadgate-no-workdir", cls="load-gate",
         path=["empty11"], files={"lib11/probe.sh": PROBE_SH}, dirs=[],
         desktop={"Exec": "probe.sh %f"}, args=["x.txt"],
         expect={"rc": 1, "stderr": "Unable to load application information"}),
    dict(id="p12-tryexec-missing", cls="load-gate-tryexec",
         path=["bin12"], files={"bin12/probe.sh": PROBE_SH}, dirs=[],
         desktop={"Exec": "{root}/bin12/probe.sh", "TryExec": "nosuch-tryexec"},
         args=[], expect={"rc": 1, "stderr": "Unable to load application information"}),
    dict(id="p13-exec-is-dir", cls="load-gate-dir",
         path=["bin13"], files={}, dirs=["bin13/adir"],
         desktop={"Exec": "{root}/bin13/adir"}, args=[],
         expect={"rc": 1, "stderr": "Unable to load application information"}),
    dict(id="p14-path-empty-join-relative", cls="path-empty-search",
         path=["empty14"], files={"probe.sh": PROBE_SH}, dirs=[],
         desktop={"Exec": "./probe.sh"}, args=[],
         expect={"rc": 0, "P0": "{root}/./probe.sh", "CWD": "{root}"}),
    dict(id="p15-path-absent-search", cls="path-empty-search",
         path=["empty15"], files={"probe.sh": PROBE_SH}, dirs=[],
         desktop={"Exec": "./probe.sh"}, args=[],
         expect={"rc": 0, "P0": "{root}/./probe.sh", "CWD": "{root}"}),
    dict(id="p16-argv0-replaced", cls="argv0-lookup",
         path=["bin16"], files={"bin16/probe.sh": PROBE_SH}, dirs=[],
         desktop={"Exec": "probe.sh"}, args=[],
         expect={"rc": 0, "P0": "{root}/bin16/probe.sh"}),
    dict(id="p17-path-relative-cwd", cls="path-relative",
         path=["bin17"], files={"bin17/probe.sh": PROBE_SH}, dirs=["work"],
         desktop={"Exec": "{root}/bin17/probe.sh", "Path": "work"},
         args=[], expect={"rc": 0, "CWD": "{root}/work"}),
    dict(id="p19-term-via-workdir", cls="terminal-workdir",
         path=["bin19", "empty19"],
         files={"bin19/probe.sh": PROBE_SH, "bin19/xdg-terminal-exec": TERM_SH},
         dirs=["work"],
         desktop={"Exec": "probe.sh %f", "Terminal": "true", "Path": "{root}/bin19"},
         args=["work/f1.txt"],
         expect={"rc": 0, "T0": "{root}/bin19/xdg-terminal-exec", "TC": "2",
                 "TA1": "probe.sh", "CWD": "{root}/bin19"}),
    dict(id="p20-term-empty-path", cls="terminal-empty-path",
         path=["bin20"], files={"bin20/probe.sh": PROBE_SH,
                                "bin20/xdg-terminal-exec": TERM_SH},
         dirs=["work"],
         desktop={"Exec": "{root}/bin20/probe.sh", "Terminal": "true", "Path": ""},
         args=[], expect={"rc": 0, "T0": "{root}/bin20/xdg-terminal-exec",
                          "TC": "1", "CWD": "{root}"}),
    dict(id="p21-argv0-replaced-not-on-path", cls="argv0-lookup",
         path=["empty21"], files={"bin21/probe.sh": PROBE_SH}, dirs=[],
         desktop={"Exec": "probe.sh", "Path": "{root}/bin21"}, args=[],
         expect={"rc": 0, "P0": "{root}/bin21/probe.sh", "CWD": "{root}/bin21"}),
    dict(id="p22-term-program-unresolved", cls="terminal-program",
         path=["empty22"],
         files={"bin22/probe.sh": PROBE_SH, "bin22/xdg-terminal-exec": TERM_SH},
         dirs=[],
         desktop={"Exec": "probe.sh", "Terminal": "true", "Path": "{root}/bin22"},
         args=[],
         expect={"rc": 0, "T0": "{root}/bin22/xdg-terminal-exec", "TA1": "probe.sh",
                 "TC": "1", "P0": "<absent>"}),
    dict(id="p23-empty-exec-nonexec-arg", cls="program-not-found",
         path=["empty23"], files={"bin23/x.txt": "hello\n"}, dirs=[],
         desktop={"Exec": ""}, args=["bin23/x.txt"],
         expect={"rc": 1, "stderr": "not found in $PATH"}),
    dict(id="p24-empty-exec-exec-arg", cls="program-not-found",
         path=["empty24"], files={"bin24/probe.sh": PROBE_SH}, dirs=[],
         desktop={"Exec": ""}, args=["bin24/probe.sh"],
         expect={"rc": 0, "P0": "{root}/bin24/probe.sh", "PC": "0"}),
    dict(id="p18-gdf-relative-desktop", cls="gdf",
         path=["bin18"], files={"bin18/probe.sh": PROBE_SH}, dirs=["work"],
         desktop={"Exec": "{root}/bin18/probe.sh"}, args=[],
         desktop_rel="work/x.desktop", expect={"rc": 0, "GDF": "{root}/work/x.desktop"}),
]


def build(case):
    root = os.path.join(SCRATCH, case["id"])
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, "h"), exist_ok=True)
    for d in case["dirs"]:
        os.makedirs(os.path.join(root, d), exist_ok=True)
    for rel, text in case["files"].items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(text)
        os.chmod(p, 0o644 if rel.endswith(".txt") else 0o755)
    for entry in case["path"]:
        os.makedirs(os.path.join(root, entry), exist_ok=True)
    desk = os.path.join(root, case.get("desktop_rel", "case.desktop"))
    os.makedirs(os.path.dirname(desk), exist_ok=True)
    lines = ["[Desktop Entry]", "Type=Application", "Name=Probe"]
    for k, v in case["desktop"].items():
        lines.append("%s=%s" % (k, v.replace("{root}", root)))
    with open(desk, "w") as f:
        f.write("\n".join(lines) + "\n")
    return root, desk


def run(case):
    root, desk = build(case)
    out = os.path.join(root, "out")
    open(out, "w").close()
    path = ":".join(os.path.join(root, e) for e in case["path"])
    desktop_arg = desk
    if case.get("desktop_rel"):
        desktop_arg = case["desktop_rel"]
    argv = [GIO, "launch", desktop_arg] + [os.path.join(root, a) for a in case["args"]]
    env = {"LC_ALL": "C", "HOME": os.path.join(root, "h"), "PROBE_OUT": out,
           "PATH": path}
    t0 = time.time()
    proc = subprocess.run(argv, cwd=root, env=env, capture_output=True, text=True,
                          timeout=10)
    # quiet wait: poll for a record, then 0.3 s of no growth
    last = -1
    stable = 0
    while time.time() - t0 < 8:
        size = os.path.getsize(out)
        if size == last and size > 0:
            stable += 1
            if stable >= 3:
                break
        else:
            stable = 0
        last = size
        time.sleep(0.1)
    time.sleep(0.2)
    rec = {}
    with open(out) as f:
        for line in f:
            line = line.rstrip("\n")
            if "=" in line:
                k, v = line.split("=", 1)
                rec.setdefault(k, v)
    return dict(id=case["id"], cls=case["cls"], rc=proc.returncode,
                stderr=proc.stderr.strip(), rec=rec, root=root,
                expect=case["expect"])


def check(res):
    exp = res["expect"]
    bad = []
    if res["rc"] != exp["rc"]:
        bad.append("rc=%d expect=%d" % (res["rc"], exp["rc"]))
    if "stderr" in exp and exp["stderr"] not in res["stderr"]:
        bad.append("stderr missing %r" % exp["stderr"])
    for k, v in exp.items():
        if k in ("rc", "stderr"):
            continue
        want = v.replace("{root}", res["root"])
        got = res["rec"].get(k)
        if want == "<absent>":
            if got is not None:
                bad.append("%s=%r want absent" % (k, got))
            continue
        if got != want:
            bad.append("%s=%r want=%r" % (k, got, want))
    return bad


def main():
    results = []
    for case in CASES:
        res = run(case)
        res["bad"] = check(res)
        results.append(res)
        print("%-28s rc=%d %s" % (res["id"], res["rc"],
                                  "OK" if not res["bad"] else "MISMATCH " + "; ".join(res["bad"])))
        for k in sorted(res["rec"]):
            print("    %s=%s" % (k, res["rec"][k]))
        if res["stderr"]:
            print("    stderr=%s" % res["stderr"].replace("\n", " | "))
    with open(os.path.join(SCRATCH, "probe-results.json"), "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    fails = [r["id"] for r in results if r["bad"]]
    print("PROBE: cases=%d ok=%d mismatch=%d" % (len(results), len(results) - len(fails), len(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
