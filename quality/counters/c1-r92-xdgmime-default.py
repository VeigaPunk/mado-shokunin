#!/usr/bin/env python3
"""Round-92 C1 counter — does tools/mado-xdgmime.py answer what `xdg-mime query default` (xdg-utils 1.2.1) prints?

Frozen predicate PRED-C1-r92-v1 (declaration, counter and receipt use the same label):
  TARGET_MET iff `<rev>:tools/mado-xdgmime.py`, run on every frozen case (fixture tree + whole
  environment + working directory = the fixture root + the MIME types asked) inside a sandbox that hides
  /usr/bin/xdg-mime, /usr/bin/xdg-open, /usr/bin/xdg-settings, every shell binary and the lane
  repository, prints for every asked type the same line and exit status as the installed xdg-mime
  labelled (correct == cases); does the same on every fresh case the frozen fuzz generator makes from
  seed = the first 8 hex digits of the measured tool's sha256, labelled by xdg-mime at measurement time
  (fresh_correct == fresh); every frozen mutant of the tool returns a well-formed wrong answer on at
  least one frozen case (killed == mutants; a mutant that only crashes is crashed-not-killed, QUALITY
  148); each control scores fewer than the case count (do-nothing, naive user-mimeapps reader with no
  install check, the lane's GLib resolver tools/mado-mime.py at the base revision, and the base
  revision's tools/mado-xdgmime.py — absent = 0); and the installed xdg-mime, bash, grep, gawk,
  realpath and basename are the pinned binaries and still give every stored label (oracle_agree == cases); and the
  measured tool's bytes pass the bytes clause (at most 65536 bytes, no ELF/PE/Mach-O magic, no base64- or
  hex-alphabet run longer than 8192 bytes) — the sandbox hides the host's shells and xdg-utils, not a copy a tool
  carries, so a tool that ships an interpreter (R92MCritic §3, 1.66 MB, scored 128/128 and fresh 120/120) is
  refused by its bytes; the frozen mutant anchors stay the semantic defence.

The lane repository is only read (`git show <rev>:<path>`).  Fixtures live under --scratch-root.
rc 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error, 3 draft run (--draft-tool: same scoring of a working
file, never a measurement).
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

TOOL = "tools/mado-xdgmime.py"
GLIB_TOOL = "tools/mado-mime.py"
PRED = "PRED-C1-r92-v1"
PINNED = ("/usr/bin/xdg-mime", "/usr/bin/bash", "/usr/bin/grep", "/usr/bin/gawk", "/usr/bin/realpath",
          "/usr/bin/basename")
MASK = ["/usr/bin/xdg-mime", "/usr/bin/xdg-open", "/usr/bin/xdg-settings", "/usr/bin/xdg-email",
        "/usr/bin/xdg-screensaver", "/usr/bin/xdg-desktop-menu", "/usr/bin/xdg-desktop-icon", "/usr/bin/xdg-icon-resource",
        "/usr/bin/bash", "/usr/bin/dash", "/usr/bin/zsh", "/usr/bin/ksh", "/usr/bin/mksh", "/usr/bin/busybox",
        "/usr/bin/fish", "/usr/bin/rbash"]


def bytes_clause(b: bytes) -> str | None:
    """None when the tool's bytes pass; otherwise the reason (round-92 w1 R92MCritic §3)."""
    import re
    if len(b) > 65536:
        return f"size {len(b)} > 65536"
    for magic in (b"\x7fELF", b"MZ\x90\x00", b"\xcf\xfa\xed\xfe", b"\xfe\xed\xfa\xcf"):
        if magic in b:
            return f"binary magic {magic!r}"
    if re.search(rb"[A-Za-z0-9+/=]{8193}", b) or re.search(rb"[0-9A-Fa-f]{8193}", b):
        return "encoded blob longer than 8192 bytes"
    return None


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha(p: str) -> str:
    return sha_bytes(open(os.path.realpath(p), "rb").read())


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git_show(repo: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def sandbox_argv(lane: str, work: str) -> list[str]:
    """Host read-only; the per-run work dir (fixtures + tool copies, no labels) the only bind; xdg-utils and every
    shell masked; the lane repository (labels, oracle, cases) hidden; no network, own pid ns."""
    masks: list[str] = []
    for p in sorted({os.path.realpath(x) for x in MASK if os.path.exists(x)}):
        masks += ["--ro-bind", "/dev/null", p]
    return [shutil.which("bwrap") or "bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
            "--tmpfs", os.path.dirname(work), "--bind", work, work] + masks + [
            "--tmpfs", lane, "--unshare-net", "--unshare-pid", "--die-with-parent", "--"]


def run_tool(tool: str, case: dict, root: str, oracle, sandbox: list[str]) -> dict | None:
    env = oracle.env_of(case, root)
    args = [sys.executable, "-I", tool, "--json", "--cwd", root] + [f"--env={k}={v}" for k, v in env.items()]
    args += ["--"] + case["types"]
    try:
        r = subprocess.run(sandbox + args, capture_output=True, text=True, env={"LC_ALL": "C", "PATH": "/nonexistent"},
                           timeout=60, cwd=root)
    except subprocess.TimeoutExpired:
        return None
    if r.returncode != 0:
        return None
    try:
        doc = json.loads(r.stdout)
        return {x["type"]: {"default": x["default"], "rc": x["rc"]} for x in doc["results"]}
    except (ValueError, KeyError, TypeError):
        return None


def correct(answer: dict | None, expect: dict) -> bool:
    if answer is None:
        return False
    return all(answer.get(t) == lab for t, lab in expect.items())


# ---------------------------------------------------------------- controls (answers built without the model)
def ctl_do_nothing(case: dict, root: str, oracle, sandbox) -> dict:
    return {t: {"default": None, "rc": 0} for t in case["types"]}


def ctl_naive(case: dict, root: str, oracle, sandbox) -> dict:
    """First id of TYPE= under [Default Applications] in $XDG_CONFIG_HOME/mimeapps.list; no install check."""
    env = oracle.env_of(case, root)
    ch = env.get("XDG_CONFIG_HOME") or env.get("HOME", "") + "/.config"
    out = {}
    for t in case["types"]:
        d = None
        try:
            cur = None
            for line in open(os.path.join(root, ch, "mimeapps.list"), encoding="utf-8", errors="replace"):
                s = line.strip()
                if s.startswith("[") and s.endswith("]"):
                    cur = s[1:-1]
                elif cur == "Default Applications" and "=" in s:
                    k, v = s.split("=", 1)
                    if k.strip() == t and d is None:
                        d = next((x for x in v.strip().split(";") if x), None)
        except OSError:
            pass
        out[t] = {"default": d, "rc": 0 if "/" in t and not t.startswith("-") else 1}
    return out


def make_ctl_glib(glib_tool: str | None):
    def ctl_glib(case: dict, root: str, oracle, sandbox) -> dict | None:
        """The lane's GLib 2.90.1 resolver (round 91) asked the same question: what gio would open."""
        if glib_tool is None:
            return None
        env = oracle.env_of(case, root)
        home = env.get("HOME", "")
        args = [sys.executable, "-I", glib_tool, "--json",
                "--config-home", env.get("XDG_CONFIG_HOME") or home + "/.config",
                "--config-dirs", env.get("XDG_CONFIG_DIRS") or "/etc/xdg",
                "--data-home", env.get("XDG_DATA_HOME") or home + "/.local/share",
                "--data-dirs", env.get("XDG_DATA_DIRS") or "/usr/local/share/:/usr/share/",
                "--path", env.get("PATH", "")]
        args += ["--desktop", env["XDG_CURRENT_DESKTOP"]] if env.get("XDG_CURRENT_DESKTOP") else ["--desktop-unset"]
        types = [t for t in case["types"] if "/" in t and not t.startswith("-")]
        out = {t: {"default": None, "rc": 1} for t in case["types"] if t not in types}
        if types:
            try:
                r = subprocess.run(sandbox + args + ["--"] + types, capture_output=True, text=True, timeout=60, cwd=root,
                                   env={"LC_ALL": "C", "HOME": root, "PATH": "/nonexistent"})
                doc = {x["type"]: x for x in json.loads(r.stdout)["results"]}
            except (subprocess.TimeoutExpired, ValueError, KeyError, TypeError):
                return None
            for t in types:
                out[t] = {"default": doc.get(t, {}).get("default"), "rc": 0}
        return out
    return ctl_glib


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--mutants", required=True)
    ap.add_argument("--oracle", required=True, help="path of xdgmime-oracle-r92.py (read from the working tree)")
    ap.add_argument("--fuzz-gen", required=True, help="path of fuzz-gen-r92.py (generate(seed, n))")
    ap.add_argument("--expect-cases-sha256", required=True)
    ap.add_argument("--expect-mutants-sha256", required=True)
    ap.add_argument("--expect-oracle-sha256", required=True)
    ap.add_argument("--expect-fuzz-sha256", required=True)
    ap.add_argument("--expect-bin-sha256", required=True,
                    help="comma list, in order: " + ",".join(os.path.basename(p) for p in PINNED))
    ap.add_argument("--fresh", type=int, default=120)
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--draft-tool")
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    lane = os.path.realpath(a.repo)
    scratch = os.path.realpath(a.scratch_root)

    def setup(msg: str) -> int:
        print(f"MADO_XDGMIME_DEFAULT: SETUP_ERROR {msg}")
        return 2

    if a.fresh < 1:
        return setup("--fresh must be at least 1 (the fresh leg is part of the predicate)")
    if scratch == lane or scratch.startswith(lane + os.sep):
        return setup("--scratch-root must lie outside the lane repository")
    os.makedirs(scratch, exist_ok=True)
    bins = a.expect_bin_sha256.split(",")
    if len(bins) != len(PINNED):
        return setup(f"--expect-bin-sha256 needs {len(PINNED)} digests")
    pins = [(a.cases, a.expect_cases_sha256), (a.mutants, a.expect_mutants_sha256), (a.oracle, a.expect_oracle_sha256),
            (a.fuzz_gen, a.expect_fuzz_sha256)] + list(zip(PINNED, bins))
    for p, want in pins:
        try:
            got = sha(p)
        except OSError as e:
            return setup(f"cannot read {p}: {e}")
        if got != want:
            return setup(f"sha256 mismatch {p}: {got} != {want}")
    if shutil.which("bwrap") is None:
        return setup("bwrap not found")
    oracle = load(a.oracle, "xdgmime_oracle_r92")
    fuzz = load(a.fuzz_gen, "fuzz_gen_r92")
    cases = json.load(open(a.cases, encoding="utf-8"))["cases"]
    mutants = json.load(open(a.mutants, encoding="utf-8"))["mutants"]
    work = tempfile.mkdtemp(prefix="c1r92-", dir=scratch)
    try:
        if a.draft_tool:
            tool_bytes = open(a.draft_tool, "rb").read()
            label = f"draft:{a.draft_tool}"
        else:
            tool_bytes = git_show(lane, a.rev, TOOL)
            if tool_bytes is None:
                return setup(f"{TOOL} absent at {a.rev}")
            label = a.rev
        base_bytes = git_show(lane, a.base_rev, TOOL)
        glib_bytes = git_show(lane, a.base_rev, GLIB_TOOL)
        sandbox = sandbox_argv(lane, work)
        probe = subprocess.run(sandbox + [sys.executable, "-c", "pass"], capture_output=True, text=True)
        if probe.returncode != 0:
            return setup(f"sandbox unavailable: {probe.stderr.strip()[:200]}")

        roots = []
        for i, c in enumerate(cases):
            root = os.path.join(work, f"c{i:04d}")
            os.makedirs(root)
            oracle.materialise(c, root)
            roots.append(root)

        def write_tool(name: str, b: bytes, fname: str = "mado-xdgmime.py") -> str:
            # every scored tool (candidate, mutant, base) is the same file name in an opaque directory
            d = os.path.join(work, "t-" + hashlib.sha256((name + str(os.getpid())).encode()).hexdigest()[:12])
            os.makedirs(d, exist_ok=True)
            p = os.path.join(d, fname)
            with open(p, "wb") as fh:
                fh.write(b)
            return p

        def answers(tool: str) -> list[dict | None]:
            with ThreadPoolExecutor(max_workers=a.jobs) as ex:
                return list(ex.map(lambda ic: run_tool(tool, ic[1], roots[ic[0]], oracle, sandbox), enumerate(cases)))

        def score(tool: str) -> list[bool]:
            return [correct(x, c["expect"]) for x, c in zip(answers(tool), cases)]

        cand_path = write_tool("candidate", tool_bytes)
        cand_ans = answers(cand_path)
        # a run that crashed (nonzero exit, timeout, unparsable output) is counted, so a crashing control or
        # forgery cannot pass for a defeated one in a receipt (round-92 lesson M92-3)
        answered = sum(1 for x in cand_ans if x is not None)
        cand = [correct(x, c["expect"]) for x, c in zip(cand_ans, cases)]
        n = len(cases)
        ncorrect = sum(cand)
        for c, ok in zip(cases, cand):
            print(f"case {c['id']} {'ok' if ok else 'WRONG'}")
        groups: dict[str, list[int]] = {}
        for c, ok in zip(cases, cand):
            g = c.get("group", "l1")
            groups.setdefault(g, [0, 0])
            groups[g][0] += ok
            groups[g][1] += 1

        killed = 0
        crashed = 0
        text = tool_bytes.decode("utf-8")
        for m in mutants:
            if text.count(m["find"]) != 1:
                return setup(f"mutant {m['id']}: find occurs {text.count(m['find'])} times")
            ans = answers(write_tool(f"m-{m['id']}", text.replace(m["find"], m["replace"]).encode()))
            wrong = sum(1 for x, c in zip(ans, cases) if x is not None and not correct(x, c["expect"]))
            crash = sum(1 for x in ans if x is None)
            if wrong:
                killed += 1
                status = "killed"
            elif crash:
                crashed += 1
                status = "crashed-not-killed"
            else:
                status = "SURVIVED"
            print(f"mutant {m['id']} {status} wrong={wrong} crashed={crash}")

        ctl = {}
        glib_path = write_tool("glib", glib_bytes, "mado-mime.py") if glib_bytes is not None else None
        for name, fn in (("do_nothing", ctl_do_nothing), ("naive_mimeapps", ctl_naive),
                         ("glib_resolver", make_ctl_glib(glib_path))):
            with ThreadPoolExecutor(max_workers=a.jobs) as ex:
                res = list(ex.map(lambda cr: fn(cr[0], cr[1], oracle, sandbox), zip(cases, roots)))
            ctl[name] = sum(correct(x, c["expect"]) for x, c in zip(res, cases))
        ctl["base_tool"] = sum(score(write_tool("base", base_bytes))) if base_bytes is not None else 0
        base_state = "present" if base_bytes is not None else "absent"

        agree = 0
        with ThreadPoolExecutor(max_workers=a.jobs) as ex:
            labs = list(ex.map(lambda c: oracle.label_case(c, work), cases))
        for c, lab in zip(cases, labs):
            if lab == c["expect"]:
                agree += 1
            else:
                print(f"oracle-disagrees {c['id']}")

        seed = int(sha_bytes(tool_bytes)[:8], 16)
        fresh_cases = fuzz.generate(seed, a.fresh)
        froots = []
        for i, c in enumerate(fresh_cases):
            root = os.path.join(work, f"f{i:04d}")
            os.makedirs(root)
            oracle.materialise(c, root)
            froots.append(root)
        with ThreadPoolExecutor(max_workers=a.jobs) as ex:
            flabs = list(ex.map(lambda c: oracle.label_case(c, work), fresh_cases))
            fans = list(ex.map(lambda ic: run_tool(cand_path, ic[1], froots[ic[0]], oracle, sandbox),
                               enumerate(fresh_cases)))
        fresh_ok = 0
        for c, lab, x in zip(fresh_cases, flabs, fans):
            if correct(x, lab):
                fresh_ok += 1
            else:
                print(f"fresh {c['id']} WRONG")
    finally:
        oracle.restore_modes(work)
        shutil.rmtree(work, ignore_errors=True)

    bc = bytes_clause(tool_bytes)
    met = (ncorrect == n and killed == len(mutants) and all(v < n for v in ctl.values()) and agree == n
           and fresh_ok == len(fresh_cases) and bc is None)
    verdict = ("DRAFT_TARGET_MET" if met else "DRAFT_TARGET_MISSED") if a.draft_tool else (
        "TARGET_MET" if met else "TARGET_MISSED")
    gtxt = " ".join(f"{g}={v[0]}/{v[1]}" for g, v in sorted(groups.items()))
    print(f"MADO_XDGMIME_DEFAULT: {verdict} pred={PRED} rev={label} base_rev={a.base_rev} cases={n} correct={ncorrect} "
          f"{gtxt} answered={answered}/{n} fresh={fresh_ok}/{len(fresh_cases)} fresh_seed={seed} mutants={len(mutants)} killed={killed} "
          f"crashed_not_killed={crashed} oracle_agree={agree}/{n} "
          + " ".join(f"{k}_correct={v}" for k, v in ctl.items()) + f" base_tool={base_state} "
          f"bytes_clause={'ok' if bc is None else 'FAIL:' + bc.replace(' ', '_')} tool_bytes={len(tool_bytes)} "
          f"tool_sha256={sha_bytes(tool_bytes)}")
    if a.draft_tool:
        return 3
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
