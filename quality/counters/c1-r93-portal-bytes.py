#!/usr/bin/env python3
"""Round-93 C1 counter - portal routing resolver vs the xdg-desktop-portal binary, incl. GKeyFile byte classes.

Frozen predicate PRED-C1-r93-v1 (the same sentence as the declaration and the receipt label):
  TARGET_MET iff <rev>:tools/mado-portals.py is the frozen candidate (sha256 == --expect-tool-sha256) and, run
  through its public CLI in the round-90 sandbox with fixtures written as bytes, answers every frozen case (the
  229 round-90 cases + the frozen byte-class cases) exactly as the installed xdg-desktop-portal 1.22.1 labels it
  (correct == cases); answers every fresh case of the round-90 generator (120) and of the frozen byte-class
  generator (60), both seeded by the first 8 hex digits of the tool's sha256 and labelled by the oracle at
  measurement time; every frozen mutant gives a well-formed wrong answer on at least one frozen case
  (killed == mutants; a crash is not a kill, QUALITY 148); each control - do-nothing, the round-90 r12-rule and
  host-table controls, and the base revision's tools/mado-portals.py - scores fewer than the case count; the base
  tool scores fewer than the byte subset (classes a, b, n: invalid UTF-8 and raw name bytes, VT, NUL) holds
  (base_bytes_correct < bytes_cases); and the oracle binary and host tail digests equal the label file's pins.

A case is correct when, for all 21 interfaces, the tool's backend list equals the oracle's and the tool's
reason equals the oracle's reason (the tool's `none-key`/`no-backend` both correspond to the oracle's
"no decision line").  Byte-class fixtures carry lone surrogates for raw bytes (\\udcXX) and are materialised
as bytes via surrogateescape.  The byte subset is the cases whose `class` field is "a", "b" or "n" (NUL); for the
round-92 stand-in file (no `class` field) the class is derived from the id suffix after `d1-`
(a1..a5 -> a, b1..b5 -> b).  A mutant is killed only if it returns a well-formed answer differing from the
label on >=1 frozen case; a crash/timeout/unparseable output is crashed_not_killed.  A mutant whose `find`
occurs != 1 time in the measured tool is a SETUP_ERROR rc 2.  All temp dirs live under --scratch-root.
The tool is run through its public CLI inside a bubblewrap sandbox: read-only /usr (oracle binary and
dbus masked), fixture and tool only, no network, cleared environment (round 90).  The oracle binary's
sha256 must equal --expect-oracle-binary-sha256 and the label file's `oracle_binary_sha256`; the host tail
digest must equal the label file's `host_tail_sha256` and /etc/xdg-desktop-portal must be absent, else rc 2.
rc 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error, 3 DRAFT (with --draft-tool; prints DRAFT_*).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

TOOL = "tools/mado-portals.py"
IMPL = "org.freedesktop.impl.portal."
IFACES = [IMPL + n for n in (
    "Lockdown", "Access", "Settings", "FileChooser", "AppChooser", "Print",
    "Notification", "Inhibit", "Screenshot", "Background", "Wallpaper",
    "Account", "Email", "Secret", "GlobalShortcuts", "DynamicLauncher",
    "ScreenCast", "RemoteDesktop", "Clipboard", "InputCapture", "Usb")]
HOST_TAIL = "/usr/share/xdg-desktop-portal"
ORACLE_BIN = "/usr/lib/xdg-desktop-portal"


def _load(name: str, path: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_R93_CONTROLS = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", ".ufo", "waves", "round-93", "controls")
_R90_CONTROLS = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", ".ufo", "waves", "round-90", "controls")
ORACLE = None  # loaded in main() once --oracle is known
FUZZ = None  # loaded in main() from the round-90 controls dir
R90_FUZZ_SHA256 = "f5cbb11ffd181724354b34f5a95389e91297ed72da8103561b3e34f02fbcdcd6"  # frozen round-90 generator
FUZZ_BYTES = None  # loaded in main() from --fuzz-bytes-gen


def case_class(c: dict) -> str | None:
    """Byte-class letter of a frozen case: its explicit `class` field when present (R93MCritic C1-F1), else the
    round-92 id suffix (d1-a1-.. -> a) for the stand-in file, else None."""
    if "class" in c:
        return c["class"]
    s = str(c.get("id", ""))
    if not s.startswith("d1-"):
        return None
    m = __import__("re").match(r"^([a-d])\d+-", s[3:])
    return m.group(1) if m else None


def sha256_file(p: str) -> str:
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def host_tail_digest() -> str:
    h = hashlib.sha256()
    for root, dirs, files in os.walk(HOST_TAIL):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, HOST_TAIL).encode() + b"\0")
            h.update(open(p, "rb").read())
            h.update(b"\0")
    return h.hexdigest()


def git_show(repo: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def write_fixture(path: str, text: str) -> None:
    """Write a fixture as bytes via surrogateescape so a lone surrogate in the case file lands as the raw byte."""
    with open(path, "wb") as fh:
        fh.write(text.encode("utf-8", "surrogateescape"))


def materialise(case: dict, root: str) -> list[str]:
    args: list[str] = []
    if case["desktop"] is None:
        args.append("--desktop-unset")
    else:
        args += ["--desktop", case["desktop"]]
    if case["mode"] == "dir":
        pd = os.path.join(root, "p")
        os.makedirs(pd)
        for k, v in case["files"].items():
            write_fixture(os.path.join(pd, k), v)
        args += ["--portal-dir", pd]
    else:
        x = os.path.join(root, "x")
        for k, v in case["files"].items():
            p = os.path.join(x, k)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            write_fixture(p, v)
        nc = max([int(k.split("/")[1]) + 1 for k in case["files"] if k.startswith("config_dirs/")]
                 + [case.get("n_config_dirs", 0), 1])
        nd = max([int(k.split("/")[1]) + 1 for k in case["files"] if k.startswith("data_dirs/")]
                 + [case.get("n_data_dirs", 0), 1])
        args += ["--config-home", f"{x}/config_home",
                 "--config-dirs", ":".join(f"{x}/config_dirs/{i}" for i in range(nc)),
                 "--data-home", f"{x}/data_home",
                 "--data-dirs", ":".join(f"{x}/data_dirs/{i}" for i in range(nd)),
                 "--sysconfdir", "/etc", "--datadir", "/usr/share"]
    return args


MASKED = ("/usr/lib/xdg-desktop-portal", "/usr/bin/dbus-run-session", "/usr/bin/dbus-daemon")


def sandbox(root: str, tool_path: str) -> list[str]:
    argv = ["bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64", "/lib64",
            "--symlink", "usr/bin", "/bin"]
    for m in MASKED:
        if os.path.exists(m):
            argv += ["--ro-bind", "/dev/null", m]
    argv += ["--ro-bind", root, root, "--ro-bind", tool_path, tool_path, "--proc", "/proc", "--dev", "/dev",
             "--unshare-all", "--die-with-parent", "--clearenv", "--setenv", "PATH", "/usr/bin",
             "--setenv", "HOME", os.path.join(root, "home"), "--setenv", "LC_ALL", "C", "--chdir", root, "--"]
    return argv


def run_tool(tool_path: str, case: dict, scratch: str) -> dict | None:
    root = tempfile.mkdtemp(prefix="k", dir=scratch)
    try:
        args = materialise(case, root)
        r = subprocess.run(sandbox(root, tool_path) + ["/usr/bin/python3", "-I", tool_path, "--json"] + args,
                           capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            return None
        try:
            return json.loads(r.stdout)
        except json.JSONDecodeError:
            return None
    finally:
        shutil.rmtree(root, ignore_errors=True)


def case_correct(out: dict | None, case: dict) -> bool:
    if out is None:
        return False
    for i in IFACES:
        if out.get("picks", {}).get(i) != case["oracle"][i]:
            return False
        why = out.get("reasons", {}).get(i)
        why = None if why in ("none-key", "no-backend") else why
        if why != case["oracle_reason"].get(i):
            return False
    return True


def score_tool(tool_path: str, cases: list[dict], scratch: str, jobs: int) -> list[bool]:
    return [o == "ok" for o in outcomes(tool_path, cases, scratch, jobs)]


def outcomes(tool_path: str, cases: list[dict], scratch: str, jobs: int) -> list[str]:
    """Per case: ok, wrong (a well-formed answer that differs) or crash (nonzero exit / no JSON).
    A crash is not a kill (QUALITY 148; round-90 w1 R90MConnector §4.1)."""
    with ThreadPoolExecutor(jobs) as ex:
        outs = list(ex.map(lambda c: run_tool(tool_path, c, scratch), cases))
    return ["crash" if o is None else ("ok" if case_correct(o, c) else "wrong") for o, c in zip(outs, cases)]


# ---------------------------------------------------------------- controls
def r12_rule(case: dict, host_labels: dict) -> dict:
    """The round-12 note's rule: the first desktop-specific (or portals.conf) file of the first
    directory holding one; the interface key if present else default; the first named backend
    whose Interfaces lists the interface; otherwise no backend.  No none/star/UseIn/gtk rules."""
    import configparser

    def portals_in(files: dict, prefix: str) -> dict:
        out = {}
        for k, v in files.items():
            if k.startswith(prefix) and k.endswith(".portal") and "/" not in k[len(prefix):]:
                cp = configparser.ConfigParser(interpolation=None, strict=False)
                try:
                    cp.read_string(v)
                    out[k[len(prefix):-7]] = [s for s in cp.get("portal", "Interfaces").split(";") if s]
                except Exception:
                    pass
        return out

    def conf_in(files: dict, prefix: str, desk: str | None) -> dict | None:
        for name in ([f"{desk.lower()}-portals.conf"] if desk else []) + ["portals.conf"]:
            if prefix + name in files:
                cp = configparser.ConfigParser(interpolation=None, strict=False)
                try:
                    cp.optionxform = str
                    cp.read_string(files[prefix + name])
                    return dict(cp["preferred"])
                except Exception:
                    return None
        return None

    desk = (case["desktop"] or "").split(":")[0] or None
    files = case["files"]
    if case["mode"] == "dir":
        backends = portals_in(files, "")
        conf = conf_in(files, "", desk)
    else:
        host = {n[:-7]: open(os.path.join(HOST_TAIL, "portals", n)).read() for n in os.listdir(os.path.join(HOST_TAIL, "portals"))}
        backends = portals_in({k + ".portal": v for k, v in host.items()}, "")
        for pre in ("data_dirs/1/xdg-desktop-portal/portals/", "data_dirs/0/xdg-desktop-portal/portals/",
                    "data_home/xdg-desktop-portal/portals/"):
            backends.update(portals_in(files, pre))
        conf = None
        for pre in ("config_home/xdg-desktop-portal/", "config_dirs/0/xdg-desktop-portal/",
                    "config_dirs/1/xdg-desktop-portal/", "data_home/xdg-desktop-portal/"):
            conf = conf_in(files, pre, desk)
            if conf is not None:
                break
        if conf is None:
            hostfiles = {n: open(os.path.join(HOST_TAIL, n)).read() for n in os.listdir(HOST_TAIL) if n.endswith(".conf")}
            conf = conf_in(hostfiles, "", desk)
    picks, reasons = {}, {}
    for i in IFACES:
        picks[i], reasons[i] = [], "no-backend"
        if conf is None:
            continue
        if i in conf:
            lst, why = conf[i], "interface specific config"
        else:
            lst, why = conf.get("default", ""), "default config"
        for b in [s.strip() for s in lst.split(";") if s.strip()]:
            if i in backends.get(b, []):
                picks[i], reasons[i] = [b], ("config" if i.endswith(".Settings") else why)
                break
    return {"picks": picks, "reasons": reasons}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--mutants", required=True)
    ap.add_argument("--expect-cases-sha256", required=True)
    ap.add_argument("--expect-mutants-sha256", required=True)
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--expect-oracle-binary-sha256", required=True)
    ap.add_argument("--fresh", type=int, default=120, help="fresh oracle-labelled cases generated from the tool sha256")
    ap.add_argument("--draft-tool", help="DRAFT only: score this file instead of <rev>:tools/mado-portals.py; never a measurement")
    ap.add_argument("--oracle", required=True, help="round-93 oracle module path (writes fixtures via surrogateescape)")
    ap.add_argument("--expect-oracle-sha256", required=True, help="sha256 of the oracle module")
    ap.add_argument("--fuzz-bytes-gen", required=True, help="round-93 byte-class fresh generator module path")
    ap.add_argument("--expect-fuzz-bytes-sha256", required=True, help="sha256 of the byte-class fresh generator")
    ap.add_argument("--fresh-bytes", type=int, default=60, help="fresh byte-class cases generated from the tool sha256")
    ap.add_argument("--expect-tool-sha256", required=True, help="the frozen candidate's sha256 (R93MCritic C1-F2)")
    a = ap.parse_args()

    def setup(msg: str) -> int:
        print(f"MADO_PORTAL_BYTES: SETUP_ERROR {msg}")
        return 2

    if sha256_file(a.cases) != a.expect_cases_sha256:
        return setup(f"cases sha256 {sha256_file(a.cases)} != pinned")
    if sha256_file(a.mutants) != a.expect_mutants_sha256:
        return setup(f"mutants sha256 {sha256_file(a.mutants)} != pinned")
    if sha256_file(a.oracle) != a.expect_oracle_sha256:
        return setup(f"oracle sha256 {sha256_file(a.oracle)} != pinned")
    if sha256_file(a.fuzz_bytes_gen) != a.expect_fuzz_bytes_sha256:
        return setup(f"fuzz-bytes-gen sha256 {sha256_file(a.fuzz_bytes_gen)} != pinned")
    global ORACLE, FUZZ, FUZZ_BYTES
    ORACLE = _load("portal_oracle_r93", a.oracle)
    r90_fuzz = os.path.join(_R90_CONTROLS, "fuzz-gen-r90.py")
    if sha256_file(r90_fuzz) != R90_FUZZ_SHA256:
        return setup(f"round-90 fuzz-gen sha256 {sha256_file(r90_fuzz)} != pinned")
    FUZZ = _load("fuzz_gen_r90", r90_fuzz)
    FUZZ_BYTES = _load("fuzz_bytes_r93", a.fuzz_bytes_gen)
    data = json.load(open(a.cases, encoding="utf-8"))
    cases = data["cases"]
    if any("oracle" not in c or "oracle_reason" not in c for c in cases):
        return setup("unlabelled case")
    tail = host_tail_digest()
    if tail != data.get("host_tail_sha256"):
        return setup(f"host tail {tail} != label {data.get('host_tail_sha256')}")
    if os.path.exists("/etc/xdg-desktop-portal"):
        return setup("/etc/xdg-desktop-portal exists; labels assume it absent")
    mutants = json.load(open(a.mutants, encoding="utf-8"))["mutants"]
    if data.get("oracle_binary_sha256") != a.expect_oracle_binary_sha256:
        return setup("label file oracle_binary_sha256 != pinned")
    if sha256_file(ORACLE_BIN) != a.expect_oracle_binary_sha256:
        return setup("installed oracle binary sha256 != pinned")
    if shutil.which("bwrap") is None:
        return setup("bwrap missing: the tool cannot be sandboxed")
    tool = open(a.draft_tool, "rb").read() if a.draft_tool else git_show(a.repo, a.rev, TOOL)
    if tool is None:
        return setup(f"{TOOL} absent at {a.rev}")
    os.makedirs(a.scratch_root, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c1r93-", dir=a.scratch_root)
    try:
        tp = os.path.join(work, "tool.py")
        open(tp, "wb").write(tool)
        oc = outcomes(tp, cases, work, a.jobs)
        res = [o == "ok" for o in oc]
        for c, o in zip(cases, oc):
            print(f"case {c['id']} {'ok' if o == 'ok' else o.upper()}")
        correct = sum(res)
        answered = sum(o != "crash" for o in oc)
        blind = [ok for c, ok in zip(cases, res) if c["id"].startswith("bl-")]
        # fresh leg: cases nobody could see before the tool's bytes were fixed
        fresh_seed = int(hashlib.sha256(tool).hexdigest()[:8], 16)
        fresh_cases = FUZZ.gen_cases(a.fresh, fresh_seed, FUZZ.load_host_portals())
        with ThreadPoolExecutor(a.jobs) as ex:
            orc = list(ex.map(lambda c: ORACLE.run_case(c, work, 8.0), fresh_cases))
        if not all(o["done"] for o in orc):
            return setup("fresh leg: oracle run incomplete")
        for c, o in zip(fresh_cases, orc):
            c["oracle"], c["oracle_reason"] = o["picks"], o["reasons"]
        fres = score_tool(tp, fresh_cases, work, a.jobs)
        for c, ok in zip(fresh_cases, fres):
            if not ok:
                print(f"fresh {c['id']} FAIL")
        fresh_correct = sum(fres)
        # fresh byte-class leg: same seed, frozen byte generator, oracle-labelled at measurement time
        fresh_bytes_cases = FUZZ_BYTES.gen_cases(a.fresh_bytes, fresh_seed)
        with ThreadPoolExecutor(a.jobs) as ex:
            orc = list(ex.map(lambda c: ORACLE.run_case(c, work, 8.0), fresh_bytes_cases))
        if not all(o["done"] for o in orc):
            return setup("fresh-bytes leg: oracle run incomplete")
        for c, o in zip(fresh_bytes_cases, orc):
            c["oracle"], c["oracle_reason"] = o["picks"], o["reasons"]
        fbres = score_tool(tp, fresh_bytes_cases, work, a.jobs)
        for c, ok in zip(fresh_bytes_cases, fbres):
            if not ok:
                print(f"fresh-bytes {c['id']} FAIL")
        fresh_bytes_correct = sum(fbres)
        src = tool.decode()
        killed = 0
        crashed_not_killed = 0
        for m in mutants:
            n = src.count(m["find"])
            if n != 1:
                return setup(f"mutant {m['id']} find occurs {n} times")
            mp = os.path.join(work, f"mut-{m['id']}.py")
            open(mp, "w").write(src.replace(m["find"], m["replace"], 1))
            mres = outcomes(mp, cases, work, a.jobs)
            first = next((c["id"] for c, o in zip(cases, mres) if o == "wrong"), None)
            if first is None and "crash" in mres:
                crashed_not_killed += 1
                print(f"mutant {m['id']} crashed-not-killed ({mres.count('crash')} crash cases)")
            status = "killed" if first else "survived"
            killed += bool(first)
            print(f"mutant {m['id']} {status}{' by ' + first if first else ''} ({m['what']})")
        host_vec = next((c for c in cases if c["id"] == "d01-host-replica"), None)
        if host_vec is None:
            host_vec = cases[0]
        host_correct = sum(1 for c in cases if c["oracle"] == host_vec["oracle"] and c["oracle_reason"] == host_vec["oracle_reason"])
        r12_correct = sum(1 for c in cases if case_correct(r12_rule(c, host_vec), c))
        bytes_idx = [i for i, c in enumerate(cases) if case_class(c) in ("a", "b", "n")]
        dn = os.path.join(_R90_CONTROLS, "do-nothing-portals.py")
        dnp = os.path.join(work, "do-nothing.py")
        shutil.copyfile(dn, dnp)
        do_nothing_correct = sum(score_tool(dnp, cases, work, a.jobs))
        base_tool = git_show(a.repo, a.base_rev, TOOL)
        if base_tool is None:
            base_correct, base_note, base_res = 0, "absent", [False] * len(cases)
        else:
            bp = os.path.join(work, "base.py")
            open(bp, "wb").write(base_tool)
            base_res = score_tool(bp, cases, work, a.jobs)
            base_correct, base_note = sum(base_res), "present"
    finally:
        shutil.rmtree(work, ignore_errors=True)
    n = len(cases)
    bytes_cases = len(bytes_idx)
    bytes_correct = sum(res[i] for i in bytes_idx)
    base_bytes_correct = sum(base_res[i] for i in bytes_idx)
    tool_pin = hashlib.sha256(tool).hexdigest() == a.expect_tool_sha256
    met = (tool_pin and correct == n and fresh_correct == a.fresh and fresh_bytes_correct == a.fresh_bytes
           and killed == len(mutants) and r12_correct < n
           and host_correct < n and do_nothing_correct < n and base_correct < n
           and base_bytes_correct < bytes_cases)
    verdict = ("DRAFT_" if a.draft_tool else "") + ("TARGET_MET" if met else "TARGET_MISSED")
    print(f"MADO_PORTAL_BYTES: {verdict} pred=PRED-C1-r93-v1 rev={'draft:' + a.draft_tool if a.draft_tool else a.rev} "
          f"tool_pin={'ok' if tool_pin else 'FAIL'} cases={n} correct={correct} answered={answered}/{n} bytes_cases={bytes_cases} bytes_correct={bytes_correct} "
          f"fresh={fresh_correct}/{a.fresh} fresh_bytes={fresh_bytes_correct}/{a.fresh_bytes} fresh_seed={fresh_seed} "
          f"mutants={len(mutants)} killed={killed} crashed_not_killed={crashed_not_killed} "
          f"r12_rule_correct={r12_correct} host_table_correct={host_correct} "
          f"do_nothing_correct={do_nothing_correct} base_correct={base_correct} base_bytes_correct={base_bytes_correct} "
          f"host_tail_sha256={tail} tool_sha256={hashlib.sha256(tool).hexdigest()}")
    if a.draft_tool:
        return 3
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
