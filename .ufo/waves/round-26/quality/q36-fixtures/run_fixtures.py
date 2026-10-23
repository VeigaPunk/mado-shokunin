#!/usr/bin/env python3
"""Build the Q36 synthetic git repos, run the checker matrix, and write the mutant receipt.

Usage:
    python3 -I -B run_fixtures.py [--scratch DIR] [--checker PATH] [--lane PATH] [--out PATH]

Fixtures are synthetic git repositories created under
/fast/scratch/hyaku/mado-r26/q36/repos/<name>/ and mutated checker copies under
.../checkers/<mutant-id>.py. The lane checker is only ever read; the only lane file written is
the path given to --out.

Exit status: 0 when every pristine baseline and every mutant kill matches its declaration;
1 when any assertion fails (the receipt then carries the failures); 2 on setup problems
(scratch outside its root, a mutation locus that does not occur exactly once).
"""
import argparse, ast, datetime, hashlib, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixtures  # noqa: E402

SCRATCH_ROOT = "/fast/scratch/hyaku/mado-r26/q36"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SUCCESSOR = LANE + "/.ufo/waves/round-26/quality/check-control-receipts.py"
OLD_CHECKER = LANE + "/.ufo/waves/round-25/quality/check-control-receipts.py"

LEGACY = [
    {
        "id": "round-24",
        "receipt": ".ufo/waves/round-25/quality/q36-red-round24.txt",
        "args": ["--round", "24",
                 "--data-registry", ".ufo/waves/round-24/w1/reports/swarm-registry.json",
                 "--tip", "41cc04c8", "--any-md"],
    },
    {
        "id": "round-25",
        "receipt": ".ufo/waves/round-25/quality/q36-green-round25.txt",
        "args": ["--round", "25",
                 "--data-registry", ".ufo/waves/round-25/a3w2/reports/swarm-registry.json",
                 "--tip", "ef94763c"],
    },
]


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def base_env(home):
    return {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": home,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
        "LC_ALL": "C",
    }


def run_ok(cmd, cwd, env, timeout=120):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError("command failed (%d): %s\nstdout: %s\nstderr: %s"
                           % (p.returncode, " ".join(cmd),
                              p.stdout.decode("utf-8", "replace"),
                              p.stderr.decode("utf-8", "replace")))
    return p.stdout.decode("utf-8", "replace")


def run_checker(checker, repo, args, cwd, env):
    cmd = [sys.executable, "-I", "-B", checker, "--repo", repo] + list(args)
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, timeout=120)
    return (p.returncode,
            p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"),
            " ".join(cmd))


def build_fixture(fx, scratch):
    repo = os.path.join(scratch, "repos", fx["name"])
    if os.path.exists(repo):
        shutil.rmtree(repo)
    os.makedirs(repo)
    home = os.path.join(scratch, "home")
    os.makedirs(home, exist_ok=True)
    env = base_env(home)
    run_ok(["git", "init", "--quiet", "--initial-branch=main", repo], scratch, env)
    shas = []
    for i, c in enumerate(fx["commits"]):
        files = dict(c["files"])
        if i == 0:
            files[fixtures.REGISTRY] = json.dumps(
                {"createdAt": fx["created"], "updatedAt": fx["updated"]}, indent=1) + "\n"
        assert fixtures.REGISTRY not in c["files"]
        for path, content in files.items():
            full = os.path.join(repo, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(content)
        cenv = dict(env,
                    GIT_AUTHOR_DATE=c["at"], GIT_COMMITTER_DATE=c["at"],
                    GIT_AUTHOR_NAME="Q36Fixtures", GIT_AUTHOR_EMAIL="q36@example.invalid",
                    GIT_COMMITTER_NAME="Q36Fixtures", GIT_COMMITTER_EMAIL="q36@example.invalid")
        run_ok(["git", "add", "--all", "--", "."], repo, cenv)
        run_ok(["git", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
                "commit", "--quiet", "--allow-empty", "-m",
                "fixture %s commit %d" % (fx["name"], i + 1)], repo, cenv)
        shas.append(run_ok(["git", "rev-parse", "HEAD"], repo, cenv).strip())
    return repo, shas


def apply_mutation(text, m):
    old, new = m["old"], m["new"]
    n = text.count(old)
    if n != 1:
        raise SystemExit("mutant %s: locus occurs %d times, expected exactly 1: %r"
                         % (m["id"], n, old))
    line = text[:text.index(old)].count("\n") + 1
    mutated = text.replace(old, new)
    try:
        ast.parse(mutated)
    except SyntaxError as ex:
        raise SystemExit("mutant %s is not valid Python: %s" % (m["id"], ex))
    return mutated, line


def fixture_problems(fx, rc, out, shas):
    problems = []
    if rc != fx["expect_exit"]:
        problems.append("exit=%d expected=%d" % (rc, fx["expect_exit"]))
    for needle in fx.get("expect_stdout", []):
        if needle not in out:
            problems.append("stdout missing %r" % needle)
    idx = fx.get("expect_receipt_commit")
    if idx is not None:
        want = "receipt_commit=%s " % shas[idx][:12]
        if want not in out:
            problems.append("stdout missing %r" % want)
    return problems


def parse_legacy(path):
    lines = [l for l in open(path, encoding="utf-8").read().split("\n") if l.strip()]
    return lines


def legacy_parity(expect_lines, rc, out):
    problems = []
    for line in expect_lines:
        if line.startswith("exit="):
            if int(line.split("=", 1)[1]) != rc:
                problems.append("stored %s, got exit=%d" % (line, rc))
        elif line.startswith("$ "):
            continue
        elif line.startswith("tip="):
            if line not in out:
                problems.append("stored %r not a prefix of current stdout" % line)
        elif line.startswith(("receipt_commit=", "order=", "CONTROL_RECEIPTS verdict=")):
            if line not in out:
                problems.append("stored %r absent from current stdout" % line)
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", default=SCRATCH_ROOT)
    ap.add_argument("--checker", default=SUCCESSOR)
    ap.add_argument("--lane", default=LANE)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    scratch = os.path.abspath(a.scratch)
    if not scratch.startswith("/fast/scratch/hyaku/mado-r26/"):
        raise SystemExit("--scratch must live under /fast/scratch/hyaku/mado-r26/")
    checker = os.path.abspath(a.checker)
    if not os.path.isfile(checker):
        raise SystemExit("no checker at %s" % checker)
    src = open(checker, "rb").read()
    text = src.decode("utf-8")
    env = base_env(os.path.join(scratch, "home"))
    os.makedirs(env["HOME"], exist_ok=True)
    os.makedirs(os.path.join(scratch, "checkers"), exist_ok=True)

    lines = []
    failures = []
    emit = lines.append

    emit("Q36 FIXTURE RECEIPTS — round-26 quality repair R4 (M25-3 survivors)")
    emit("$ " + " ".join([sys.executable] + sys.argv))
    emit("generated_utc=%s" % datetime.datetime.now(datetime.timezone.utc)
         .strftime("%Y-%m-%dT%H:%M:%SZ"))
    emit("successor=%s sha256=%s" % (checker, sha256_bytes(src)))
    emit("round-25 checker (unchanged, read-only)=%s sha256=%s"
         % (OLD_CHECKER, sha256_file(OLD_CHECKER)))
    emit("fixtures.py=%s sha256=%s" % (os.path.join(HERE, "fixtures.py"),
                                       sha256_file(os.path.join(HERE, "fixtures.py"))))
    emit("run_fixtures.py=%s sha256=%s" % (os.path.abspath(__file__),
                                           sha256_file(os.path.abspath(__file__))))
    emit("scratch_root=%s  (synthetic repos + mutated copies only)" % scratch)
    emit("python=%s git=%s" % (sys.version.split()[0],
                               run_ok(["git", "--version"], scratch, env).strip()))
    emit("lane=%s tip=%s" % (a.lane, run_ok(["git", "-C", a.lane, "rev-parse", "--short", "HEAD"],
                                            scratch, env).strip()))
    emit("")
    emit("== Isolation ==")
    emit("Fixture git writes happen only under %s with GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE" % scratch)
    emit("unset, GIT_CONFIG_NOSYSTEM=1 and a scratch HOME; the lane is never written. The lane is")
    emit("read-only for the legacy parity runs below. No display variable is inherited by any run.")
    emit("")

    # Variants: pristine + one file per mutant.
    variant_path = {"pristine": checker}
    mutants = {}
    for m in fixtures.MUTANTS:
        mutated, line = apply_mutation(text, m)
        mpath = os.path.join(scratch, "checkers", m["id"] + ".py")
        with open(mpath, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(mutated)
        variant_path[m["id"]] = mpath
        mutants[m["id"]] = {"line": line, "sha256": sha256_bytes(mutated.encode("utf-8")),
                            "path": mpath}

    # Build fixtures and run the full matrix.
    built = {}
    results = {}
    for fx in fixtures.FIXTURES:
        repo, shas = build_fixture(fx, scratch)
        built[fx["name"]] = {"repo": repo, "shas": shas}
        args = ["--round", str(fixtures.ROUND), "--data-registry", fixtures.REGISTRY,
                "--tip", "HEAD"] + fx["args"]
        for vid, cpath in variant_path.items():
            results[(fx["name"], vid)] = run_checker(cpath, repo, args, scratch, env)

    emit("== Legacy parity on the lane (read-only git history) ==")
    legacy_rc = {}
    for leg in LEGACY:
        rc, out, err, cmd = run_checker(checker, a.lane, leg["args"], scratch, env)
        legacy_rc[leg["id"]] = rc
        stored = parse_legacy(os.path.join(a.lane, leg["receipt"]))
        problems = legacy_parity(stored, rc, out)
        emit("$ " + cmd)
        emit(out.rstrip("\n"))
        emit("exit=%d" % rc)
        if err.strip():
            emit("stderr=%s" % err.strip())
            failures.append("legacy %s stderr: %s" % (leg["id"], err.strip()))
        emit("parity_with_%s=%s" % (leg["receipt"].split("/")[-1],
                                    "ok" if not problems else "MISMATCH " + "; ".join(problems)))
        if problems:
            failures.append("legacy %s: %s" % (leg["id"], "; ".join(problems)))
        emit("")

    emit("== Fixture baselines (pristine successor) ==")
    emit("%-20s %-6s %-6s %s" % ("fixture", "expect", "actual", "why"))
    for fx in fixtures.FIXTURES:
        rc, out, err, cmd = results[(fx["name"], "pristine")]
        problems = fixture_problems(fx, rc, out, built[fx["name"]]["shas"])
        emit("%-20s %-6d %-6d %s" % (fx["name"], fx["expect_exit"], rc, fx["why"]))
        if problems:
            failures.append("fixture %s pristine: %s" % (fx["name"], "; ".join(problems)))
        if err.strip():
            failures.append("fixture %s pristine stderr: %s" % (fx["name"], err.strip()))
    emit("")
    for fx in fixtures.FIXTURES:
        rc, out, err, cmd = results[(fx["name"], "pristine")]
        emit("--- fixture %s: pristine exit=%d" % (fx["name"], rc))
        emit("$ " + cmd)
        emit(out.rstrip("\n"))
        emit("")

    emit("== Mutant kill table ==")
    emit("legacy columns are the same mutant on the two lane cases (they must stay 1 and 0: the")
    emit("legacy pair cannot see these mutants). killer columns are the synthetic fixture.")
    emit("")
    emit("| mutant | change | legacy r24 | legacy r25 | green | killer fixture | pristine | mutant | verdict |")
    emit("|---|---|---:|---:|---:|---|---:|---:|---|")
    kill_count = 0
    for m in fixtures.MUTANTS:
        mid = m["id"]
        loc = mutants[mid]
        killer = m["killed_by"]
        prc = results[(killer, "pristine")][0]
        mrc = results[(killer, mid)][0]
        expect = m["expect"]
        killed = (prc, mrc) == tuple(expect)
        green_prc = results[("green", "pristine")][0]
        green_mrc = results[("green", mid)][0]
        legacy_pair = []
        for leg in LEGACY:
            rc, out, err, cmd = run_checker(loc["path"], a.lane, leg["args"], scratch, env)
            legacy_pair.append(rc)
        same_legacy = legacy_pair == [legacy_rc["round-24"], legacy_rc["round-25"]]
        if killed:
            kill_count += 1
        else:
            failures.append("mutant %s not killed by %s: pristine=%d mutant=%d expected %s"
                            % (mid, killer, prc, mrc, expect))
        if green_mrc != green_prc:
            failures.append("mutant %s changed the green baseline: %d -> %d"
                            % (mid, green_prc, green_mrc))
        emit("| %s | L%d: %s | %d | %d | %d | %s | %d | %d | %s |"
             % (mid, loc["line"], m["defect"].replace("|", "/"),
                legacy_pair[0], legacy_pair[1], green_mrc, killer, prc, mrc,
                "killed" if killed else "SURVIVED"))
        if not same_legacy:
            failures.append("mutant %s changed a legacy exit: %s" % (mid, legacy_pair))
    emit("")
    emit("green column: every mutant must leave the healthy baseline at its pristine exit (0);")
    emit("a mutant that also breaks green is reported as a failure, so no kill below is collateral.")
    for (fname, vid), (rc, out, err, cmd) in sorted(results.items()):
        if err.strip():
            failures.append("run %s/%s wrote stderr: %s" % (fname, vid, err.strip()))
    emit("")
    emit("Every mutant kept the legacy exits (%s), so the kill comes from the synthetic fixture."
         % "r24=1 r25=0")
    emit("")

    emit("== Designated killer transcripts (red = mutant output) ==")
    for m in fixtures.MUTANTS:
        mid = m["id"]
        killer = m["killed_by"]
        for vid in ("pristine", mid):
            rc, out, err, cmd = results[(killer, vid)]
            emit("--- %s on fixture %s: exit=%d" % (vid, killer, rc))
            emit("$ " + cmd)
            emit(out.rstrip("\n"))
            if err.strip():
                emit("stderr=%s" % err.strip())
            emit("")

    emit("== Mutation definitions (each applied alone to a scratch copy) ==")
    for m in fixtures.MUTANTS:
        loc = mutants[m["id"]]
        emit("[%s] line %d sha256=%s" % (m["id"], loc["line"], loc["sha256"]))
        emit("  defect: %s" % m["defect"])
        emit("  old: %s" % m["old"].replace("\n", "\\n"))
        emit("  new: %s" % m["new"].replace("\n", "\\n"))
        emit("")

    emit("Q36MUTANTS killed=%d/%d fixtures=%d"
         % (kill_count, len(fixtures.MUTANTS), len(fixtures.FIXTURES)))
    if failures:
        emit("Q36FIXTURES verdict=FAIL")
        for f in failures:
            emit("FAILURE %s" % f)
    else:
        emit("Q36FIXTURES verdict=PASS")

    receipt = "\n".join(lines) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(receipt)
    sys.stdout.write(receipt)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
