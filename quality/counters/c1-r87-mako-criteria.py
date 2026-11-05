#!/usr/bin/env python3
"""mado round 87 — PRED-C1-r87-v1: score tools/mado-mako.py effective settings.

Predicate (declaration section "C1", verbatim): TARGET_MET iff the candidate tool's correct count equals N, all M mutants are killed, and both do-nothing controls score strictly below N.
Score = 10 * tool_correct / N on this finite case set only.

Surface: mako 1.11.0 effective settings for one notification, resolved from a config file, its
`include=` chain and its criteria sections. The case file is a path; the tool bytes and the
mutant list are read from REV with `git show` under a scrubbed git environment.

Controls (never call the tool, scored on the same cases with the same rule):
  naive-toplevel   reads only the --config file's own key=value lines before any [section] line.
  globals-include  follows include= (regular files under HOME, ~ resolved to HOME) and applies the
                   global key=value lines of every file reached, ignoring every section.

Writes only inside a generation directory created under --scratch-root and removed on exit.
Never writes inside the repository.

Exit map: 0 TARGET_MET · 1 TARGET_MISSED · 2 setup error (never a verdict).
--selftest: hermetic fixture run in a scratch directory; exit 0 iff every assertion holds, else 1.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

SCHEMA = "mako-cases-r87-v1"
N_MIN, N_MAX = 20, 24
DECLARED_MUTANTS = 10
TOOL_PATH = "tools/mado-mako.py"
MUTANTS_PATH = ".ufo/waves/round-87/controls/mako-mutants-r87.json"
RUN_TIMEOUT = 20
SCRUB = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
)
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
URGENCY = ("low", "normal", "critical")
ARG_NAMES = ("app-name", "urgency", "mode")
THIS = os.path.abspath(__file__)


class SetupError(Exception):
    pass


# ---------------------------------------------------------------- git (scrubbed)

def git_env():
    env = {k: v for k, v in os.environ.items() if k not in SCRUB}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return env


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], env=git_env(), capture_output=True)
    if proc.returncode != 0:
        msg = proc.stderr.decode("utf-8", "replace").strip()
        raise SetupError(f"git {' '.join(args)} failed in {repo}: {msg}")
    return proc.stdout


def resolve_commit(repo, rev):
    if not rev or rev.startswith("-"):
        raise SetupError(f"bad REV {rev!r}")
    if not os.path.isdir(repo):
        raise SetupError(f"repo is not a directory: {repo}")
    out = git(repo, "rev-parse", "--verify", rev + "^{commit}")
    return out.decode("ascii").strip()


# ---------------------------------------------------------------- inputs

def sha256(data):
    return hashlib.sha256(data).hexdigest()


def canon(value):
    return json.dumps(value, sort_keys=True)


def safe_relpath(value, what):
    if not isinstance(value, str) or not value or value.startswith("/"):
        raise SetupError(f"{what}: not a relative path: {value!r}")
    if any(part in ("", ".", "..") for part in value.split("/")):
        raise SetupError(f"{what}: unsafe path {value!r}")
    return value


def load_cases(raw):
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise SetupError(f"cases file is not JSON: {exc}")
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        raise SetupError(f"cases schema is not {SCHEMA}")
    entries = doc.get("cases")
    if not isinstance(entries, list) or not entries:
        raise SetupError("cases must be a non-empty list")
    cases, ids = [], set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise SetupError("case is not an object")
        cid = entry.get("id")
        if not isinstance(cid, str) or not ID_RE.match(cid) or cid in ids:
            raise SetupError(f"bad or duplicate case id {cid!r}")
        ids.add(cid)
        config = safe_relpath(entry.get("config"), f"{cid}.config")
        files = entry.get("home_files")
        if not isinstance(files, dict):
            raise SetupError(f"{cid}.home_files must be an object")
        home_files = {}
        for rel, content in files.items():
            safe_relpath(rel, f"{cid}.home_files")
            if isinstance(content, str):
                home_files[rel] = content
            elif isinstance(content, dict) and set(content) == {"symlink_to"}:
                home_files[rel] = {"symlink_to": safe_relpath(content["symlink_to"], f"{cid}.symlink")}
            else:
                raise SetupError(f"{cid}.home_files[{rel}]: must be text or {{symlink_to}}")
        args = entry.get("args", {})
        if not isinstance(args, dict) or not set(args) <= set(ARG_NAMES):
            raise SetupError(f"{cid}.args: unknown or non-object args")
        app_name = args.get("app-name")
        if app_name is not None and (not isinstance(app_name, str) or not app_name):
            raise SetupError(f"{cid}.args.app-name must be a non-empty string")
        urgency = args.get("urgency")
        if urgency is not None and urgency not in URGENCY:
            raise SetupError(f"{cid}.args.urgency must be one of {URGENCY}")
        modes = args.get("mode", [])
        if isinstance(modes, str):
            modes = [modes]
        if not isinstance(modes, list) or not all(isinstance(m, str) for m in modes):
            raise SetupError(f"{cid}.args.mode must be a string or list of strings")
        expect = entry.get("expect")
        if not isinstance(expect, dict) or not isinstance(expect.get("effective"), dict):
            raise SetupError(f"{cid}.expect.effective must be an object")
        refusals = expect.get("refusals")
        if refusals not in ("none", "present"):
            raise SetupError(f"{cid}.expect.refusals must be 'none' or 'present'")
        cases.append({
            "id": cid,
            "config": config,
            "home_files": home_files,
            "app_name": app_name,
            "urgency": urgency,
            "modes": modes,
            "effective": expect["effective"],
            "refusals": refusals,
        })
    return cases


def load_mutants(raw):
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise SetupError(f"mutants file is not JSON: {exc}")
    if isinstance(doc, dict):
        doc = doc.get("mutants")
    if not isinstance(doc, list):
        raise SetupError("mutants must be a list")
    out, ids = [], set()
    for entry in doc:
        if not isinstance(entry, dict):
            raise SetupError("mutant is not an object")
        mid, old, new = entry.get("id"), entry.get("old"), entry.get("new")
        if not isinstance(mid, str) or not ID_RE.match(mid) or mid in ids:
            raise SetupError(f"bad or duplicate mutant id {mid!r}")
        if not isinstance(old, str) or old == "" or not isinstance(new, str):
            raise SetupError(f"mutant {mid}: old must be a non-empty string, new a string")
        ids.add(mid)
        out.append((mid, old, new))
    return out


# ---------------------------------------------------------------- tool runs

def materialize(cases, gen):
    homes = {}
    for case in cases:
        home = os.path.join(gen, "home-" + case["id"])
        os.makedirs(home)
        for rel, content in case["home_files"].items():
            path = os.path.join(home, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if isinstance(content, dict):
                os.symlink(os.path.join(home, content["symlink_to"]), path)
            else:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(content)
        homes[case["id"]] = os.path.realpath(home)
    return homes


def run_tool(tool, case, home, gen):
    argv = [sys.executable, "-I", tool, "--config", os.path.join(home, case["config"]), "--home", home]
    if case["app_name"] is not None:
        argv += ["--app-name", case["app_name"]]
    if case["urgency"] is not None:
        argv += ["--urgency", case["urgency"]]
    for mode in case["modes"]:
        argv += ["--mode", mode]
    env = {
        "PATH": os.environ.get("PATH", ""),
        "TMPDIR": gen,
        "HOME": home,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
    }
    try:
        return subprocess.run(argv, env=env, cwd=home, capture_output=True, timeout=RUN_TIMEOUT)
    except subprocess.TimeoutExpired:
        return None


def tool_verdict(case, proc):
    if proc is None:
        return False, "timeout"
    if proc.returncode != 0:
        return False, f"exit={proc.returncode}"
    try:
        out = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return False, "bad-json"
    if not isinstance(out, dict):
        return False, "not-object"
    effective = out.get("effective")
    if not isinstance(effective, dict):
        return False, "no-effective"
    refusals = out.get("refusals")
    if not isinstance(refusals, list):
        return False, "no-refusals-list"
    if case["refusals"] == "none" and refusals:
        return False, "unexpected-refusal"
    if case["refusals"] == "present" and not refusals:
        return False, "missing-refusal"
    for key, want in case["effective"].items():
        if key not in effective:
            return False, f"missing {key}"
        if canon(effective[key]) != canon(want):
            return False, f"mismatch {key}"
    return True, "ok"


def run_all(tool, cases, homes, gen):
    verdicts, reasons = [], []
    for case in cases:
        ok, reason = tool_verdict(case, run_tool(tool, case, homes[case["id"]], gen))
        verdicts.append(ok)
        reasons.append(reason)
    return verdicts, reasons


# ---------------------------------------------------------------- do-nothing controls

def read_lines(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return None


def key_value(raw):
    line = raw.strip()
    if not line or line.startswith("#") or "=" not in line:
        return None
    key, _, value = line.partition("=")
    return key.strip(), value.strip()


def naive_values(config):
    values = {}
    for raw in read_lines(config) or []:
        if raw.strip().startswith("["):
            break
        pair = key_value(raw)
        if pair is not None:
            values[pair[0]] = pair[1]
    return values


def include_target(value, base, home_real):
    if value == "~" or value.startswith("~/"):
        candidate = os.path.join(home_real, value[1:].lstrip("/"))
    elif os.path.isabs(value):
        candidate = value
    else:
        candidate = os.path.join(base, value)
    try:
        real = os.path.realpath(candidate)
        if not real.startswith(home_real + os.sep) or not stat.S_ISREG(os.stat(real).st_mode):
            return None
    except OSError:
        return None
    return real


def globals_values(config, home):
    home_real = os.path.realpath(home)
    values, seen = {}, set()

    def walk(path):
        real = os.path.realpath(path)
        if real in seen or not os.path.isfile(real):
            return
        seen.add(real)
        base = os.path.dirname(path)
        for raw in read_lines(path) or []:
            if raw.strip().startswith("["):
                break
            pair = key_value(raw)
            if pair is None:
                continue
            if pair[0] == "include":
                target = include_target(pair[1], base, home_real)
                if target is not None:
                    walk(target)
            else:
                values[pair[0]] = pair[1]

    walk(config)
    return values


def as_text(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return value
    return json.dumps(value)


def control_correct(case, values):
    if case["refusals"] == "present":
        return False
    for key, want in case["effective"].items():
        if key not in values or values[key] != as_text(want):
            return False
    return True


def control_score(cases, homes, reader):
    return sum(
        control_correct(case, reader(os.path.join(homes[case["id"]], case["config"]), homes[case["id"]]))
        for case in cases
    )


# ---------------------------------------------------------------- evaluation

def evaluate(tool_text, cases, mutants, scratch_root, declared=DECLARED_MUTANTS, range_check=True):
    n = len(cases)
    if range_check and not (N_MIN <= n <= N_MAX):
        raise SetupError(f"N={n} is outside {N_MIN}..{N_MAX}")
    if declared is not None and len(mutants) != declared:
        raise SetupError(f"mutants={len(mutants)} but the declaration fixes M={declared}")
    gen = tempfile.mkdtemp(prefix="mado-mako-r87-", dir=scratch_root)
    try:
        tool = os.path.join(gen, "tool.py")
        with open(tool, "wb") as fh:
            fh.write(tool_text.encode("utf-8"))
        homes = materialize(cases, gen)
        base, reasons = run_all(tool, cases, homes, gen)
        lines = [
            f"case {case['id']} {'ok' if ok else 'FAIL'} {reason}"
            for case, ok, reason in zip(cases, base, reasons)
        ]
        correct = sum(base)
        naive = control_score(cases, homes, lambda cfg, home: naive_values(cfg))
        globals_ = control_score(cases, homes, globals_values)
        results, killed = [], 0
        for index, (mid, old, new) in enumerate(mutants):
            count = tool_text.count(old)
            if count != 1:
                results.append({"id": mid, "status": f"setup-error count={count}", "killed": False})
                continue
            mutant = os.path.join(gen, f"mutant-{index}.py")
            with open(mutant, "wb") as fh:
                fh.write(tool_text.replace(old, new, 1).encode("utf-8"))
            verdicts, _ = run_all(mutant, cases, homes, gen)
            hit = verdicts != base
            killed += hit
            results.append({"id": mid, "status": "killed" if hit else "survived", "killed": hit})
        m = len(mutants)
        verdict = (
            "TARGET_MET"
            if correct == n and killed == m and naive < n and globals_ < n
            else "TARGET_MISSED"
        )
        return {
            "n": n,
            "correct": correct,
            "mutants": results,
            "m": m,
            "killed": killed,
            "naive": naive,
            "globals": globals_,
            "score": 10.0 * correct / n,
            "verdict": verdict,
            "lines": lines,
        }
    finally:
        shutil.rmtree(gen, ignore_errors=True)


def exit_for(verdict):
    return {"TARGET_MET": 0, "TARGET_MISSED": 1}.get(verdict, 2)


def run(args):
    for name in ("repo", "rev", "cases", "scratch_root"):
        if getattr(args, name) is None:
            raise SetupError(f"--{name.replace('_', '-')} is required")
    if not os.path.isdir(args.scratch_root):
        raise SetupError(f"scratch root is not a directory: {args.scratch_root}")
    commit = resolve_commit(args.repo, args.rev)
    try:
        with open(args.cases, "rb") as fh:
            cases_raw = fh.read()
    except OSError as exc:
        raise SetupError(f"cases unreadable: {exc}")
    cases = load_cases(cases_raw)
    tool_raw = git(args.repo, "show", f"{commit}:{TOOL_PATH}")
    try:
        tool_text = tool_raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SetupError(f"tool is not UTF-8: {exc}")
    if args.mutants is not None:
        try:
            with open(args.mutants, "rb") as fh:
                mutants_raw = fh.read()
        except OSError as exc:
            raise SetupError(f"mutants unreadable: {exc}")
    else:
        mutants_raw = git(args.repo, "show", f"{commit}:{MUTANTS_PATH}")
    mutants = load_mutants(mutants_raw)
    print(f"cases_sha256={sha256(cases_raw)} cases={len(cases)}")
    print(f"tool_sha256={sha256(tool_raw)} tool_path={TOOL_PATH} commit={commit}")
    print(f"mutants={len(mutants)} mutants_sha256={sha256(mutants_raw)}")
    result = evaluate(tool_text, cases, mutants, args.scratch_root)
    for line in result["lines"]:
        print(line)
    print(f"controls naive_correct={result['naive']} globals_include_correct={result['globals']}")
    for entry in result["mutants"]:
        print(f"mutant {entry['id']} {entry['status']}")
    print(
        f"MADO_MAKO_CRITERIA: {result['verdict']} rev={args.rev} cases={result['n']} "
        f"correct={result['correct']} mutants={result['m']} killed={result['killed']} "
        f"naive_correct={result['naive']} globals_include_correct={result['globals']} "
        f"score={result['score']:.4f} tool_sha256={sha256(tool_raw)} cases_sha256={sha256(cases_raw)}"
    )
    return exit_for(result["verdict"])


# ---------------------------------------------------------------- selftest fixtures

FIXTURE_TOOL = '''#!/usr/bin/env python3
# selftest fixture for c1-r87-mako-criteria: a tiny reader, not the round-87 tool
import argparse
import json
import os

SECTION_WINS = True
# OK_TOKEN marks the output contract of this fixture
OK_TOKEN = "v1"


def read_file(path, home, values, sections, seen):
    real = os.path.realpath(path)
    if real in seen:
        return
    seen.add(real)
    section = None
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("["):
                section = line[1:-1]
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if section is None and key == "include":
                target = value
                if target.startswith("~/"):
                    target = os.path.join(home, target[2:])
                elif not os.path.isabs(target):
                    target = os.path.join(os.path.dirname(path), target)
                read_file(target, home, values, sections, seen)
            elif section is None:
                values[key] = value
            else:
                sections.append((section, key, value))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--home", required=True)
    ap.add_argument("--app-name")
    ap.add_argument("--urgency", choices=["low", "normal", "critical"])
    ap.add_argument("--mode", action="append", default=[])
    args = ap.parse_args()
    effective, sections = {}, []
    read_file(args.config, args.home, effective, sections, set())
    for name, key, value in sections:
        if SECTION_WINS and args.app_name is not None and name == "app-name=" + args.app_name:
            effective[key] = value
    print(json.dumps({"effective": effective, "refusals": []}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

FIXTURE_CASES = {
    "schema": SCHEMA,
    "cases": [
        {
            "id": "include-global",
            "config": ".config/mako/config",
            "home_files": {
                ".config/mako/config": "include=~/.config/mako/core.ini\nanchor=top-right\n",
                ".config/mako/core.ini": "default-timeout=5000\n",
            },
            "args": {},
            "expect": {"effective": {"anchor": "top-right", "default-timeout": "5000"}, "refusals": "none"},
        },
        {
            "id": "section-override",
            "config": ".config/mako/config",
            "home_files": {
                ".config/mako/config": "anchor=top-right\n[app-name=slack]\nanchor=bottom-left\n",
            },
            "args": {"app-name": "slack"},
            "expect": {"effective": {"anchor": "bottom-left"}, "refusals": "none"},
        },
    ],
}

FIXTURE_MUTANTS = {
    "mutants": [
        {"id": "section-ignored", "old": "SECTION_WINS = True", "new": "SECTION_WINS = False"},
        {"id": "token-dup", "old": "OK_TOKEN", "new": "OK_TOKEN_X"},
    ]
}


def selftest():
    checks = []

    def check(name, cond):
        checks.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name}")

    def cli(*extra):
        return subprocess.run([sys.executable, "-I", THIS, *extra], capture_output=True, env=git_env()).returncode

    scratch = tempfile.mkdtemp(prefix="mado-mako-selftest-")
    try:
        fixture = tempfile.mkdtemp(prefix="fixture-", dir=scratch)
        subprocess.run(["git", "-C", fixture, "init", "-q"], env=git_env(), check=True)
        top = subprocess.run(
            ["git", "-C", fixture, "rev-parse", "--show-toplevel"],
            env=git_env(), capture_output=True, text=True, check=True,
        ).stdout.strip()
        check("fixture toplevel equals fixture dir", os.path.realpath(top) == os.path.realpath(fixture))

        cases_path = os.path.join(scratch, "fixture-cases.json")
        files = {
            TOOL_PATH: FIXTURE_TOOL.encode("utf-8"),
            MUTANTS_PATH: json.dumps(FIXTURE_MUTANTS, indent=2).encode("utf-8"),
            "cases/mako-cases-fixture.json": json.dumps(FIXTURE_CASES, indent=2).encode("utf-8"),
        }
        for rel, data in files.items():
            path = os.path.join(fixture, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as fh:
                fh.write(data)
        with open(cases_path, "wb") as fh:
            fh.write(files["cases/mako-cases-fixture.json"])
        subprocess.run(["git", "-C", fixture, "add", "-A"], env=git_env(), check=True)
        subprocess.run(
            ["git", "-C", fixture, "-c", "user.name=mado-selftest", "-c", "user.email=selftest@invalid",
             "commit", "-q", "-m", "selftest fixture"],
            env=git_env(), check=True,
        )
        commit = resolve_commit(fixture, "HEAD")

        decoy = os.path.join(scratch, "decoy-git-dir")
        previous = os.environ.get("GIT_DIR")
        os.environ["GIT_DIR"] = decoy
        try:
            with_decoy = resolve_commit(fixture, "HEAD")
        finally:
            if previous is None:
                os.environ.pop("GIT_DIR", None)
            else:
                os.environ["GIT_DIR"] = previous
        check("scrubbed env resolves REV although GIT_DIR points at a decoy", with_decoy == commit)
        check("git environment sets GIT_NO_REPLACE_OBJECTS=1", git_env().get("GIT_NO_REPLACE_OBJECTS") == "1")
        check("git show returns the committed tool bytes",
              git(fixture, "show", f"{commit}:{TOOL_PATH}") == files[TOOL_PATH])

        with open(cases_path, "rb") as fh:
            cases = load_cases(fh.read())
        check("fixture case set loads with N=2", len(cases) == 2)
        mutants = load_mutants(git(fixture, "show", f"{commit}:{MUTANTS_PATH}"))
        check("fixture mutants load from REV", len(mutants) == 2)

        before = sorted(os.listdir(scratch))
        good = evaluate(FIXTURE_TOOL, cases, mutants, scratch, declared=None, range_check=False)
        check("correct fixture tool scores N/N", good["correct"] == 2)
        check("section-ignored mutant is killed", good["mutants"][0]["killed"] is True)
        check("non-unique old is a setup error and not killed",
              good["mutants"][1]["status"].startswith("setup-error") and good["mutants"][1]["killed"] is False)
        check("an unkilled mutant makes the verdict TARGET_MISSED", good["verdict"] == "TARGET_MISSED")
        check("do-nothing controls score below N on fixture", good["naive"] < 2 and good["globals"] < 2)
        check("evaluate leaves the scratch root as it found it", sorted(os.listdir(scratch)) == before)

        only = evaluate(FIXTURE_TOOL, cases, mutants[:1], scratch, declared=None, range_check=False)
        check("all mutants killed with correct tool gives TARGET_MET", only["verdict"] == "TARGET_MET")

        wrong_text = FIXTURE_TOOL.replace("SECTION_WINS = True", "SECTION_WINS = False", 1)
        wrong = evaluate(wrong_text, cases, [], scratch, declared=None, range_check=False)
        check("deliberately wrong tool scores below N", wrong["correct"] < 2 and wrong["verdict"] == "TARGET_MISSED")

        check("exit map: TARGET_MET=0, TARGET_MISSED=1, setup=2",
              exit_for("TARGET_MET") == 0 and exit_for("TARGET_MISSED") == 1 and exit_for("SETUP") == 2)

        check("CLI: bad REV exits 2",
              cli("--repo", fixture, "--rev", "no-such-rev-r87", "--cases", cases_path,
                  "--scratch-root", scratch) == 2)
        check("CLI: missing scratch root exits 2",
              cli("--repo", fixture, "--rev", commit, "--cases", cases_path,
                  "--scratch-root", os.path.join(scratch, "absent")) == 2)
        check("CLI: unreadable cases exits 2",
              cli("--repo", fixture, "--rev", commit, "--cases", os.path.join(scratch, "absent.json"),
                  "--scratch-root", scratch) == 2)
        check("CLI: N=2 outside 20..24 exits 2",
              cli("--repo", fixture, "--rev", commit, "--cases", cases_path,
                  "--scratch-root", scratch) == 2)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    passed = sum(checks)
    print(f"SELFTEST: passed={passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


# ---------------------------------------------------------------- CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description="mado round 87 C1 mako effective-settings counter")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--cases")
    ap.add_argument("--scratch-root")
    ap.add_argument("--mutants")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        return run(args)
    except SetupError as exc:
        print(f"MADO_MAKO_CRITERIA: SETUP_ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
