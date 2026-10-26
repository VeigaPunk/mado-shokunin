#!/usr/bin/env python3
"""SentC1Sandbox runner: runs the relay probe inside the counter's OWN bwrap allowlist.

Imports quality/counters/c1-r47-terminal.py (read-only) and uses its Box/materialize/case_env/explain_case, so the
mounts, env and traced-run wrapper are the counter's, not a copy. Work dir: argv[1] or $TMPDIR (never a hardcoded /tmp).
Outputs: sandbox-probe.json, sandbox-run.txt beside this file.
"""
import importlib.util
import json
import os
import random
import shutil
import sys
import tempfile
import traceback

sys.dont_write_bytecode = True

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo", "waves", "round-47", "w2", "SentC1Sandbox")
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r47-terminal.py")


def load_counter():
    spec = importlib.util.spec_from_file_location("c1r47_counter", COUNTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    work_arg = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("TMPDIR")
    if not work_arg or not os.path.isdir(work_arg):
        print("runner: pass an existing work dir as argv[1] or set TMPDIR")
        return 2
    C = load_counter()
    log = []
    out = {"counter": COUNTER, "bwrap": shutil.which("bwrap"), "strace": shutil.which("strace")}

    def note(k, v):
        log.append("%s: %s" % (k, v))

    def run(name, box, root, env, tool, args):
        rc, txt = box.run(root, env, tool, args)
        note(name, "rc=%d outs=%r trips=%r" % (rc, txt[:300], box.trips[-3:]))
        return rc, txt

    work = tempfile.mkdtemp(dir=work_arg, prefix="probe-")
    probe = os.path.join(work, "tool.py")
    shutil.copy(os.path.join(SEAT, "probe-tool.py"), probe)
    box = C.Box(work, probe)
    fx = C.load_fixtures()
    case = [f for f in fx if f["expect"]["rc"] == 0 and f.get("class") == "list-precedence-config-home"][0]
    out["case"] = {"id": case["id"], "class": case.get("class"), "args": case["args"],
                   "env_keys": sorted(case["env"])}

    base = os.path.join(work, "tree")
    ro, rt = os.path.join(base, "o", "r"), os.path.join(base, "t", "r")
    C.materialize(ro, case)
    C.materialize(rt, case)
    env_o = C.case_env(case, ro, "C.UTF-8")
    env_t = C.case_env(case, rt, "C.UTF-8")

    # 1. the oracle run the counter itself makes (untraced), then look at its own writable dir
    run("oracle", box, ro, env_o, False, case["args"])
    out["oracle_tree_after"] = {
        "rw": sorted(os.listdir(ro + "/.rw")),
        "cache": sorted(os.listdir(ro + "/.rw/cache")) if os.path.isdir(ro + "/.rw/cache") else None,
        "cache_sizes": {n: os.path.getsize(os.path.join(ro, ".rw", "cache", n))
                        for n in os.listdir(ro + "/.rw/cache")} if os.path.isdir(ro + "/.rw/cache") else None,
    }

    # 2. the tool run, same case, its own tree -> full report
    rc, txt = run("tool_report", box, rt, env_t, True, ["print", "--print-id"])
    lines = txt.split("\n")
    rep = None
    for i, ln in enumerate(lines):
        if ln.startswith("PROBE-REPORT"):
            rep = json.loads(lines[i + 1])
            break
    if rep is None:
        print("runner: no probe report; first 400 bytes: %r" % txt[:400])
        return 3
    out["tool_report_rc"] = rc
    out["report"] = rep
    with open(os.path.join(SEAT, "sandbox-probe.json"), "w", encoding="utf-8") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)

    # 3. clause-s shaped root (the counter's own selftest invocation shape)
    sd = os.path.join(work, "st-root")
    os.makedirs(sd + "/.rw")
    env_s = {"PATH": "/oracle/bin", "HOME": "/tmp", "TMPDIR": "/tmp", "LANG": "C.UTF-8"}
    rc, txt = run("selftest_shape", box, sd, env_s, True, ["--selftest"])
    out["selftest_shape"] = {"rc": rc, "stdout": txt[:600]}
    rc, txt = run("selftest_shape_report", box, sd, env_s, True, ["print"])
    for i, ln in enumerate(txt.split("\n")):
        if ln.startswith("PROBE-REPORT"):
            out["selftest_report"] = json.loads(txt.split("\n")[i + 1])
            break

    # 4. cross-run channels inside one tool tree, and the same content in a fresh tree / in the oracle tree
    run("tool_write", box, rt, env_t, True, ["probe-write"])
    run("tool_read_same_tree", box, rt, env_t, True, ["probe-read"])
    rt2 = os.path.join(base, "t2", "r")
    C.materialize(rt2, case)
    run("tool_read_fresh_tree", box, rt2, C.case_env(case, rt2, "C.UTF-8"), True, ["probe-read"])
    run("tool_read_oracle_tree", box, ro, env_o, True, ["probe-read"])

    # 4b. a second report in the same tree: its listings are taken before its own writes, so anything it sees
    #     in the tmpfs (/, /usr/bin, /tmp, /dev/shm) or next to the root comes from the previous invocation.
    rc, txt = run("tool_report2", box, rt, env_t, True, ["print", "--print-id"])
    rep2 = None
    for i, ln in enumerate(txt.split("\n")):
        if ln.startswith("PROBE-REPORT"):
            rep2 = json.loads(txt.split("\n")[i + 1])
            break
    if rep2 is not None:
        out["persist"] = {
            "top": [rep["top"], rep2["top"]],
            "usr_bin": [rep["dirs"]["/usr/bin"], rep2["dirs"]["/usr/bin"]],
            "fast": [rep["dirs"]["/fast"], rep2["dirs"]["/fast"]],
            "tmp": [rep["dirs"]["/tmp"], rep2["dirs"]["/tmp"]],
            "dev_shm": [rep["dirs"]["/dev/shm"], rep2["dirs"]["/dev/shm"]],
            "root_rw_list": [rep["root_list"], rep2["root_list"]],
            "pid1": [rep["pid1_cmdline"][:120], rep2["pid1_cmdline"][:120]],
        }
        note("persist", "tmpfs-run1-vs-run2 top=%r/%r usr_bin=%r/%r tmp=%r/%r rw=%r/%r" % (
            rep["top"], rep2["top"], rep["dirs"]["/usr/bin"], rep2["dirs"]["/usr/bin"],
            rep["dirs"]["/tmp"], rep2["dirs"]["/tmp"], rep["root_list"], rep2["root_list"]))

    # 5. host-side: did /tmp or /dev/shm writes inside reach the host?
    out["host_tmp_probe_names"] = [n for n in os.listdir("/tmp") if n.startswith("sentc1-probe")][:10]
    out["host_shm_probe_names"] = [n for n in os.listdir("/dev/shm") if n.startswith("sentc1-probe")][:10]
    out["host_shm_stat"] = os.stat("/dev/shm").st_dev
    out["host_dev_stat"] = os.stat("/dev").st_dev

    # 6. DoS reproduction: the counter's own explain_case, fed a tool that pre-creates <root>/.rw/obs
    parts0 = (case["expect"]["stdout"].split("\n") + ["", ""])[:2]
    out["dos_expect"] = parts0
    note("dos_expect", "%r" % (parts0,))
    dos_probe = os.path.join(work, "tool-dos.py")
    shutil.copy(os.path.join(SEAT, "probe-dos.py"), dos_probe)
    box2 = C.Box(work, dos_probe)
    try:
        ok, why = C.explain_case(box2, case, random.Random(1))
        out["explain_dos"] = {"raised": False, "ok": ok, "why": why[:300]}
        note("explain_dos", "returned ok=%r why=%r" % (ok, why[:200]))
    except Exception as e:
        out["explain_dos"] = {"raised": True, "type": type(e).__name__, "errno": getattr(e, "errno", None),
                              "str": str(e)[:300], "where": traceback.format_exc().strip().split("\n")[-3:]}
        note("explain_dos", "RAISED %s: %s" % (type(e).__name__, e))

    with open(os.path.join(SEAT, "sandbox-run.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")
        fh.write("\noracle_tree_after=%r\n" % (out["oracle_tree_after"],))
        fh.write("\nexplain_dos=%r\n" % (out["explain_dos"],))
        fh.write("\nhost_tmp_probe_names=%r host_shm_probe_names=%r\n" % (
            out["host_tmp_probe_names"], out["host_shm_probe_names"]))
    print("\n".join(log))
    print("explain_dos=%r" % (out["explain_dos"],))
    print("oracle_tree_after=%r" % (out["oracle_tree_after"],))
    print("host_tmp=%r host_shm=%r" % (out["host_tmp_probe_names"], out["host_shm_probe_names"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
