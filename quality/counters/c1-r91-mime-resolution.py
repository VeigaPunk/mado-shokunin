#!/usr/bin/env python3
"""Round-91 C1 counter — does tools/mado-mime.py answer what GLib 2.90.1 answers?

Frozen predicate PRED-C1-r91-v1 (declaration, counter and receipt use the same label):
  TARGET_MET iff `<rev>:tools/mado-mime.py`, run on every frozen case (fixture
  tree + XDG_CURRENT_DESKTOP + PATH + the MIME types asked) inside a sandbox
  that hides /usr/bin/gio, libgio and the lane repository, prints for every
  asked type the same default application as the installed gio labelled, and —
  where gio printed a default — the same registered and recommended lists in
  the same order (correct == cases); does the same on every fresh case the
  frozen fuzz generator makes from seed = the first 8 hex digits of the
  measured tool's sha256, labelled by gio at measurement time (fresh_correct
  == fresh); every frozen mutant of the tool returns a well-formed wrong answer
  on at least one frozen case (killed == mutants; a mutant that only crashes is
  crashed-not-killed, QUALITY 148); each control scores fewer than the case
  count (do-nothing, naive mimeapps.list reader, mimeinfo.cache-only reader,
  the base revision's tool — absent = 0); and the installed gio and libgio are
  the pinned binaries and still give every stored label (oracle_agree == cases).

The lane repository is only read (`git show <rev>:<path>`).  Fixtures live under
--scratch-root.  rc 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error, 3 draft run
(--draft-tool: same scoring of a working file, never a measurement).
"""
from __future__ import annotations

import argparse
import hashlib
import glob
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

TOOL = "tools/mado-mime.py"
GIO = "/usr/bin/gio"
LIBGIO = "/usr/lib/libgio-2.0.so.0"
PRED = "PRED-C1-r91-v1"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha(p: str) -> str:
    return sha_bytes(open(os.path.realpath(p), "rb").read())


def load_oracle(path: str):
    spec = importlib.util.spec_from_file_location("mime_oracle_r91", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git_show(repo: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def sandbox_argv(lane: str, work: str) -> list[str]:
    """Host read-only; the per-run work dir (fixtures + tool copies, no labels) the only bind; /usr/bin/gio and
    every libgio shared object masked; the lane repository (labels, oracle, cases) hidden; no network, own pid ns."""
    masks: list[str] = []
    for p in [GIO] + sorted({os.path.realpath(x) for d in ("/usr/lib", "/usr/lib32", "/usr/lib64")
                             for x in glob.glob(os.path.join(d, "libgio-2.0.so*"))}):
        if os.path.exists(p):
            masks += ["--ro-bind", "/dev/null", p]
    return [shutil.which("bwrap") or "bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
            "--tmpfs", os.path.dirname(work), "--bind", work, work] + masks + [
            "--tmpfs", lane, "--unshare-net", "--unshare-pid", "--die-with-parent", "--"]


def run_tool(tool: str, case: dict, root: str, oracle, sandbox: list[str]) -> dict | None:
    a = oracle.abspaths(case, root)
    args = [sys.executable, "-I", tool, "--json", "--config-home", a["config_home"], "--config-dirs", a["config_dirs"],
            "--data-home", a["data_home"], "--data-dirs", a["data_dirs"], "--path", a["path"]]
    args += ["--desktop-unset"] if case.get("desktop") is None else ["--desktop", case["desktop"]]
    args += ["--"] + case["types"]
    env = {"LC_ALL": "C", "HOME": root, "PATH": "/nonexistent"}
    try:
        r = subprocess.run(sandbox + args, capture_output=True, text=True, env=env, timeout=60, cwd=root)
    except subprocess.TimeoutExpired:
        return None
    if r.returncode != 0:
        return None
    try:
        doc = json.loads(r.stdout)
        return {x["type"]: x for x in doc["results"]}
    except (ValueError, KeyError, TypeError):
        return None


def correct(answer: dict | None, expect: dict) -> bool:
    if answer is None:
        return False
    for t, lab in expect.items():
        got = answer.get(t)
        if got is None or got.get("default") != lab["default"]:
            return False
        if lab["default"] is not None and (got.get("registered") != lab["registered"]
                                           or got.get("recommended") != lab["recommended"]):
            return False
    return True


# ---------------------------------------------------------------- controls (answers built without the model)
def ctl_do_nothing(case: dict, root: str, oracle) -> dict:
    return {t: {"type": t, "default": None, "registered": [], "recommended": []} for t in case["types"]}


def _first_list(path: str, group: str, t: str) -> list[str]:
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    cur = None
    found: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("[") and s.endswith("]"):
            cur = s[1:-1]
        elif cur == group and "=" in s:
            k, v = s.split("=", 1)
            if k.strip() == t:
                found = [x for x in v.strip().split(";") if x]
    return found


def ctl_naive(case: dict, root: str, oracle) -> dict:
    a = oracle.abspaths(case, root)
    out = {}
    for t in case["types"]:
        d = _first_list(os.path.join(a["config_home"], "mimeapps.list"), "Default Applications", t)
        out[t] = {"type": t, "default": d[0] if d else None, "registered": d, "recommended": d}
    return out


def ctl_cache_only(case: dict, root: str, oracle) -> dict:
    a = oracle.abspaths(case, root)
    dirs = [a["data_home"]] + [x for x in a["data_dirs"].split(":") if x]
    out = {}
    for t in case["types"]:
        ids: list[str] = []
        for d in dirs:
            for x in _first_list(os.path.join(d, "applications", "mimeinfo.cache"), "MIME Cache", t):
                if x not in ids:
                    ids.append(x)
        out[t] = {"type": t, "default": ids[0] if ids else None, "registered": ids, "recommended": ids}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--mutants", required=True)
    ap.add_argument("--oracle", required=True, help="path of mime-oracle-r91.py (read from the working tree)")
    ap.add_argument("--expect-cases-sha256", required=True)
    ap.add_argument("--expect-mutants-sha256", required=True)
    ap.add_argument("--expect-oracle-sha256", required=True)
    ap.add_argument("--expect-gio-sha256", required=True)
    ap.add_argument("--expect-libgio-sha256", required=True)
    ap.add_argument("--fuzz-gen", required=True, help="path of fuzz-gen-r91.py (generate(seed, n))")
    ap.add_argument("--expect-fuzz-sha256", required=True)
    ap.add_argument("--fresh", type=int, default=120)
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--draft-tool")
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    lane = os.path.realpath(a.repo)
    scratch = os.path.realpath(a.scratch_root)

    def setup(msg: str) -> int:
        print(f"MADO_MIME_RESOLUTION: SETUP_ERROR {msg}")
        return 2

    if a.fresh < 1:
        return setup("--fresh must be at least 1 (the fresh leg is part of the predicate)")
    if scratch == lane or scratch.startswith(lane + os.sep):
        return setup("--scratch-root must lie outside the lane repository")
    os.makedirs(scratch, exist_ok=True)
    pins = [(a.cases, a.expect_cases_sha256), (a.mutants, a.expect_mutants_sha256), (a.oracle, a.expect_oracle_sha256),
            (a.fuzz_gen, a.expect_fuzz_sha256), (GIO, a.expect_gio_sha256), (LIBGIO, a.expect_libgio_sha256)]
    for p, want in pins:
        try:
            got = sha(p)
        except OSError as e:
            return setup(f"cannot read {p}: {e}")
        if got != want:
            return setup(f"sha256 mismatch {p}: {got} != {want}")
    if shutil.which("bwrap") is None:
        return setup("bwrap not found")
    oracle = load_oracle(a.oracle)
    spec = importlib.util.spec_from_file_location("fuzz_gen_r91", a.fuzz_gen)
    fuzz = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fuzz)
    cases = json.load(open(a.cases, encoding="utf-8"))["cases"]
    mutants = json.load(open(a.mutants, encoding="utf-8"))["mutants"]
    work = tempfile.mkdtemp(prefix="c1r91-", dir=scratch)
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
        sandbox = sandbox_argv(lane, work)
        probe = subprocess.run(sandbox + ["/bin/true"], capture_output=True, text=True)
        if probe.returncode != 0:
            return setup(f"sandbox unavailable: {probe.stderr.strip()[:200]}")

        roots = []
        for i, c in enumerate(cases):
            root = os.path.join(work, f"c{i:04d}")
            os.makedirs(root)
            oracle.materialise(c, root)
            roots.append(root)

        def write_tool(name: str, b: bytes) -> str:
            # every scored tool (candidate, mutant, base) is the same file name in its own directory, so a tool
            # cannot tell from its path which role it is being scored in (R91MCritic F1, role branch)
            d = os.path.join(work, "t-" + hashlib.sha256((name + str(os.getpid())).encode()).hexdigest()[:12])
            os.makedirs(d, exist_ok=True)
            p = os.path.join(d, "mado-mime.py")
            with open(p, "wb") as fh:
                fh.write(b)
            return p

        def answers(tool: str) -> list[dict | None]:
            with ThreadPoolExecutor(max_workers=a.jobs) as ex:
                return list(ex.map(lambda ic: run_tool(tool, ic[1], roots[ic[0]], oracle, sandbox), enumerate(cases)))

        def score(tool: str) -> list[bool]:
            return [correct(x, c["expect"]) for x, c in zip(answers(tool), cases)]

        cand_path = write_tool("candidate", tool_bytes)
        cand = score(cand_path)
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

        # QUALITY 148: a mutant is killed only by a well-formed wrong answer; a mutant whose only
        # failures are crashes (nonzero exit, timeout, unparsable output) is crashed-not-killed.
        killed = 0
        crashed = 0
        text = tool_bytes.decode("utf-8")
        for m in mutants:
            if text.count(m["find"]) != 1:
                return setup(f"mutant {m['id']}: find occurs {text.count(m['find'])} times")
            ans = answers(write_tool(f"m-{m['id']}.py", text.replace(m["find"], m["replace"]).encode()))
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
        for name, fn in (("do_nothing", ctl_do_nothing), ("naive_mimeapps", ctl_naive), ("cache_only", ctl_cache_only)):
            ctl[name] = sum(correct(fn(c, r, oracle), c["expect"]) for c, r in zip(cases, roots))
        ctl["base_tool"] = sum(score(write_tool("base.py", base_bytes))) if base_bytes is not None else 0
        base_state = "present" if base_bytes is not None else "absent"

        agree = 0
        with ThreadPoolExecutor(max_workers=a.jobs) as ex:
            labs = list(ex.map(lambda c: oracle.label_case(c, work), cases))
        for c, lab in zip(cases, labs):
            if lab == c["expect"]:
                agree += 1
            else:
                print(f"oracle-disagrees {c['id']}")

        # fresh leg: cases the frozen labels cannot hold, seeded by the measured tool's own sha256
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
            fans = list(ex.map(lambda ic: run_tool(cand_path, ic[1], froots[ic[0]], oracle,
                                                   sandbox), enumerate(fresh_cases)))
        fresh_ok = 0
        for c, lab, x in zip(fresh_cases, flabs, fans):
            if correct(x, lab):
                fresh_ok += 1
            else:
                print(f"fresh {c['id']} WRONG")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    met = (ncorrect == n and killed == len(mutants) and all(v < n for v in ctl.values()) and agree == n
           and fresh_ok == len(fresh_cases))
    verdict = ("DRAFT_TARGET_MET" if met else "DRAFT_TARGET_MISSED") if a.draft_tool else (
        "TARGET_MET" if met else "TARGET_MISSED")
    gtxt = " ".join(f"{g}={v[0]}/{v[1]}" for g, v in sorted(groups.items()))
    print(f"MADO_MIME_RESOLUTION: {verdict} pred={PRED} rev={label} base_rev={a.base_rev} cases={n} correct={ncorrect} "
          f"{gtxt} fresh={fresh_ok}/{len(fresh_cases)} fresh_seed={seed} mutants={len(mutants)} killed={killed} "
          f"crashed_not_killed={crashed} oracle_agree={agree}/{n} "
          + " ".join(f"{k}_correct={v}" for k, v in ctl.items()) + f" base_tool={base_state} "
          f"tool_sha256={sha_bytes(tool_bytes)}")
    if a.draft_tool:
        return 3
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
