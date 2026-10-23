#!/usr/bin/env python3
"""Round-24 C2 counter: SCORECARD capability claims vs frozen re-demonstration.

MISMATCH: a capability named in a SCORECARD.md capability table at REV whose self-assessed status (its row in a `Capability status (round 24 re-demonstration)` table at REV if present, else `works`) differs from the observed status of its frozen manifest command run on the REV tree; a manifest capability absent from REV's capability tables also counts as MISMATCH.

Usage: python3 -I count.py REV [--json] [--keep]

REV is resolved to a full commit, archived with `git -C MADO_LANE archive REV`
into a fresh mkdtemp under /fast/scratch/hyaku/mado-r24/c2/ and removed on exit
unless --keep. MADO_LANE defaults to /home/vgpnk/Projects/shokunin/mado-shokunin;
it is the read-only repository behind {LANE} and the git-reading counters.

Observed status: `works` iff the frozen command exits with an allowed code and
its stdout+stderr satisfies the row's regex rule (plus optional min_matches,
regex_all and forbid_regex); otherwise `fails`. Timeout kills the child process
group and is observed as fails with exit sentinel 124; a command not run (missing
`requires` path at REV, or no manifest command) is fails with 125.

Exit map: 0 no mismatch, 1 at least one mismatch, 2 setup error/usage.
"""
import hashlib
import json
import os
import re
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r24/c2"
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "manifest.json"
STATUS_HEADING = re.compile(
    r"^#{2,6} Capability status \(round 24 re-demonstration\)\s*$")
CAPS_HEADING = re.compile(r"^#{2,3} Capabilities\b")
HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
SEP_CELL = re.compile(r":?-{2,}:?")


class SetupError(Exception):
    pass


def cells(line):
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    return [cell.strip() for cell in text.split("|")]


def flush_table(table, mode, names, seen, status):
    if len(table) < 2:
        return
    header = cells(table[0])
    sep = cells(table[1])
    if not header or not sep or not all(SEP_CELL.fullmatch(c or "") for c in sep):
        return
    for line in table[2:]:
        row = cells(line)
        if not row:
            continue
        name = row[0].strip().strip("`").strip()
        if not name or name.startswith("\u2014 none yet"):
            continue
        if mode == "caps":
            if name not in seen:
                seen.add(name)
                names.append(name)
        elif len(row) >= 2:
            status[name] = row[1].strip().strip("`").strip().lower()


def parse_scorecard(text):
    """Return (capability names in document order, status dict)."""
    names, seen, status = [], set(), {}
    table, mode = [], None
    for raw in text.splitlines():
        heading = HEADING.match(raw)
        if heading:
            if table:
                flush_table(table, mode, names, seen, status)
                table = []
            level = len(heading.group(1))
            if CAPS_HEADING.match(raw):
                mode = "caps"
            elif STATUS_HEADING.match(raw):
                mode = "status"
            elif mode is not None and level <= 3:
                mode = None
            continue
        if mode is not None and raw.lstrip().startswith("|"):
            table.append(raw)
        else:
            if table:
                flush_table(table, mode, names, seen, status)
                table = []
    if table:
        flush_table(table, mode, names, seen, status)
    return names, status


def git(args, lane, text=True):
    done = subprocess.run(["git", "-C", str(lane)] + list(args),
                          capture_output=True, text=text)
    return done


def resolve_rev(lane, rev):
    done = git(["rev-parse", "--verify", rev + "^{commit}"], lane)
    if done.returncode != 0 or not (done.stdout or "").strip():
        raise SetupError("revision is not a commit in %s: %s" % (lane, rev))
    return done.stdout.strip()


def extract_tree(lane, rev, tree, tar_path):
    with open(tar_path, "wb") as stream:
        done = subprocess.run(["git", "-C", str(lane), "archive", "--format=tar", rev],
                              stdout=stream, stderr=subprocess.PIPE)
    if done.returncode != 0:
        raise SetupError("git archive %s failed: %s" % (rev, done.stderr.decode("utf-8", "replace").strip()))
    done = subprocess.run(["tar", "-xf", str(tar_path), "-C", str(tree)],
                          capture_output=True)
    try:
        tar_path.unlink()
    except OSError:
        pass
    if done.returncode != 0:
        raise SetupError("tar extraction failed: %s" % done.stderr.decode("utf-8", "replace").strip())


def substitute(value, mapping):
    for key, replacement in mapping.items():
        value = value.replace("{" + key + "}", replacement)
    return value


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4 << 30, 4 << 30))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def run_command(argv, cwd, env, timeout):
    try:
        proc = subprocess.Popen(argv, cwd=cwd, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                start_new_session=True, preexec_fn=limits)
    except OSError as error:
        return {"exit": 125, "out": "", "err": "could not start: %s" % error,
                "timed_out": False}
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        try:
            out, err = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            out, err = "", ""
        return {"exit": 124, "out": out or "", "err": err or "", "timed_out": True}
    return {"exit": proc.returncode, "out": out or "", "err": err or "", "timed_out": False}


def rule_ok(rule, combined, code):
    if code not in rule["exit_ok"]:
        return False
    pattern = rule["regex"]
    flags = re.MULTILINE
    if pattern.startswith("(?s)") or pattern.startswith("(?ms)") or pattern.startswith("(?sm)"):
        flags = re.MULTILINE
    found = re.findall(pattern, combined, flags)
    if len(found) < rule["min_matches"]:
        return False
    for extra in rule["regex_all"]:
        if not re.search(extra, combined, flags):
            return False
    forbid = rule.get("forbid_regex")
    if forbid and re.search(forbid, combined, flags):
        return False
    return True


def load_manifest():
    try:
        data = json.loads(MANIFEST.read_text())
    except (OSError, ValueError) as error:
        raise SetupError("manifest unreadable: %s" % error)
    if data.get("schema") != "mado-r24-c2-manifest-v1":
        raise SetupError("manifest schema mismatch")
    rows, names = [], set()
    for rule in data.get("capabilities", []):
        name = rule.get("name")
        if not isinstance(name, str) or not name:
            raise SetupError("manifest row without a name")
        if name in names:
            raise SetupError("duplicate manifest capability: %s" % name)
        names.add(name)
        if not isinstance(rule.get("argv"), list) or not rule["argv"]:
            raise SetupError("manifest row without argv: %s" % name)
        timeout = rule.get("timeout_s")
        if not isinstance(timeout, int) or not 0 < timeout <= 600:
            raise SetupError("manifest timeout_s out of 1..600: %s" % name)
        if not isinstance(rule.get("exit_ok"), list):
            raise SetupError("manifest row without exit_ok: %s" % name)
        if not isinstance(rule.get("regex"), str):
            raise SetupError("manifest row without regex: %s" % name)
        rule.setdefault("cwd", "{TREE}")
        rule.setdefault("env", {})
        rule.setdefault("min_matches", 1)
        rule.setdefault("regex_all", [])
        rule.setdefault("requires", [])
        try:
            re.compile(rule["regex"])
            for extra in rule["regex_all"]:
                re.compile(extra)
            if rule.get("forbid_regex"):
                re.compile(rule["forbid_regex"])
        except re.error as error:
            raise SetupError("manifest rule does not compile (%s): %s" % (name, error))
        rows.append(rule)
    return data, rows


def main(argv):
    json_mode = "--json" in argv
    keep = "--keep" in argv
    rest = [arg for arg in argv if arg not in ("--json", "--keep")]
    if len(rest) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    lane = Path(os.environ.get("MADO_LANE", DEFAULT_LANE)).resolve()
    counter_sha = hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest()
    manifest_sha = hashlib.sha256(MANIFEST.read_bytes()).hexdigest() if MANIFEST.exists() else ""
    run_dir = None
    try:
        data, rules = load_manifest()
        manifest_sha = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
        if not lane.is_dir():
            raise SetupError("lane is not a directory: %s" % lane)
        rev = resolve_rev(lane, rest[0])
        os.makedirs(SCRATCH, exist_ok=True)
        run_dir = Path(tempfile.mkdtemp(prefix="run-%s-" % rev[:8], dir=SCRATCH))
        tree = run_dir / "tree"
        tmpdir = run_dir / "tmp"
        tree.mkdir()
        tmpdir.mkdir()
        extract_tree(lane, rev, tree, run_dir / "tree.tar")
        scorecard = (tree / "SCORECARD.md")
        if not scorecard.is_file():
            raise SetupError("SCORECARD.md is absent at %s" % rev)
        population, status = parse_scorecard(scorecard.read_text(errors="replace"))
        census_root = run_dir / "census-root"
        census_root.mkdir()
        (census_root / "shokunin.conf").write_text("# scratch census root made by count.py\n")
        os.symlink(tree, census_root / "mado-shokunin", target_is_directory=True)
        mapping = {"TREE": str(tree), "LANE": str(lane), "FLEET": FLEET,
                   "REV": rev, "CENSUS_ROOT": str(census_root), "TMP": str(tmpdir)}
        base_env = {key: value for key, value in os.environ.items()
                    if key not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
        base_env.update({"TMPDIR": str(tmpdir), "GIT_OPTIONAL_LOCKS": "0",
                         "GIT_TERMINAL_PROMPT": "0", "PYTHONDONTWRITEBYTECODE": "1"})
        by_name = {rule["name"]: rule for rule in rules}
        names = list(population)
        for rule in rules:
            if rule["name"] not in population:
                names.append(rule["name"])
        cache = {}
        result_rows = []
        for name in names:
            in_population = name in population
            stated = status.get(name, "works")
            rule = by_name.get(name)
            if rule is None:
                observed, code, reason = "fails", 125, "no frozen manifest command"
                argv_out, cwd_out = None, None
            else:
                argv_out = [substitute(arg, mapping) for arg in rule["argv"]]
                cwd_out = substitute(rule["cwd"], mapping)
                missing = [path for path in rule["requires"]
                           if not os.path.exists(os.path.join(str(tree), substitute(path, mapping)))]
                if missing:
                    observed, code, reason = "fails", 125, "missing at REV: %s" % ", ".join(missing)
                else:
                    env = dict(base_env)
                    env.update({key: substitute(value, mapping)
                                for key, value in rule["env"].items()})
                    key = hashlib.sha256(json.dumps(
                        [argv_out, cwd_out, rule["env"], rule["timeout_s"]],
                        sort_keys=True).encode()).hexdigest()
                    if key not in cache:
                        cache[key] = run_command(argv_out, cwd_out, env, rule["timeout_s"])
                    run = cache[key]
                    combined = run["out"] + run["err"]
                    sub_rule = dict(rule)
                    sub_rule["regex"] = substitute(rule["regex"], mapping)
                    sub_rule["regex_all"] = [substitute(item, mapping)
                                             for item in rule["regex_all"]]
                    if rule.get("forbid_regex"):
                        sub_rule["forbid_regex"] = substitute(rule["forbid_regex"], mapping)
                    ok = rule_ok(sub_rule, combined, run["exit"])
                    observed = "works" if ok else "fails"
                    code = run["exit"]
                    if ok:
                        reason = "rule matched"
                    elif run["timed_out"]:
                        reason = "timeout after %ss" % rule["timeout_s"]
                    elif run["exit"] not in rule["exit_ok"]:
                        reason = "exit %s not in %s" % (run["exit"], rule["exit_ok"])
                    else:
                        reason = "output did not match the frozen rule"
            ok = in_population and stated == observed
            result_rows.append({"name": name, "stated": stated, "observed": observed,
                                "ok": ok, "exit": code, "reason": reason,
                                "in_population": in_population,
                                "argv": argv_out, "cwd": cwd_out})
        mismatches = sum(1 for row in result_rows if not row["ok"])
        result = {"schema": "mado-r24-c2-count-v1", "revision": rev,
                  "lane": str(lane), "population": len(result_rows),
                  "mismatches": mismatches, "manifest_sha256": manifest_sha,
                  "counter_sha256": counter_sha, "capabilities": result_rows,
                  "status_table_present": any(name in status for name in population),
                  "tree_kept": str(tree) if keep else None}
        if json_mode:
            print(json.dumps(result, indent=2))
        else:
            for row in result_rows:
                print("%s\tstated=%s\tobserved=%s\t%s\texit=%s" % (
                    row["name"], row["stated"], row["observed"],
                    "OK" if row["ok"] else "MISMATCH", row["exit"]))
            print("mismatches=%d/%d revision=%s manifest_sha256=%s counter_sha256=%s" % (
                mismatches, len(result_rows), rev, manifest_sha, counter_sha))
        return 0 if mismatches == 0 else 1
    except SetupError as error:
        if json_mode:
            print(json.dumps({"schema": "mado-r24-c2-count-v1", "error": str(error),
                              "exit": 2, "manifest_sha256": manifest_sha,
                              "counter_sha256": counter_sha}, indent=2))
        print("count.py: %s" % error, file=sys.stderr)
        return 2
    finally:
        if run_dir is not None and not keep:
            shutil.rmtree(str(run_dir), ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
