#!/usr/bin/env python3
"""check-receipt-presence.py — does a records change cite only receipts it actually carries?

Rounds 88 and 89 each landed a records commit whose SCORECARD/lesson text cited
receipts that were committed only later (round-88 spot-check R4, round-89
spot-check D1, lesson M89-4).  This check answers, for one records change:
every receipt path the change's *added* lines cite in the lane's record files
(SCORECARD.md, LOG.md, corpus/QUALITY.md, corpus/README.md, corpus/lessons/*.md,
corpus/knowledge/*.md) resolves to a file the change carries.

Citation grammar: `(.ufo/waves/round-N/ | quality/)? receipts/<name>.<ext>` with
ext in txt|json|jsonl|md|log|csv|tsv, not preceded by a path character and not
continued by a name character.  <name> may hold one or more `{a,b}` brace
groups (expanded; every expansion is a citation) and `*` (a glob: present iff
at least one carried file matches).  A full `.ufo/waves/round-N/receipts/…` or
`quality/receipts/…` path must exist as written; a bare `receipts/<name>`
resolves to `.ufo/waves/round-<k>/receipts/<name>` for each `-r<k>` token of the
name followed by `-` or `.` (last token first; `ghost-r89.txt`, `control-c2-r84-unguarded.txt`),
else for the change's round (`--round`, or the `round-N` prefix of the commit
subject in --rev mode), or to `quality/receipts/<name>`.

Two modes:
  --rev REV            a landed commit: added lines = `git show REV` diff of the
                       record files; a cited file is present iff it exists in REV's tree.
  --worktree --base B --commit-path P [P ...]
                       a records change about to be committed with the lane helper
                       (jj-lane.sh tracks exactly the listed paths): added lines =
                       `git diff B` (working tree) of the record files plus every
                       line of an untracked, non-ignored record file; a cited file
                       under a commit path is present iff it exists on disk (and,
                       when only a listed directory covers it, is not git-ignored,
                       since the helper adds a directory like `git add <dir>`); a
                       cited file outside every commit path is present iff B's tree
                       has it.  Commit paths are taken relative to the repository top.

Diffs are requested with explicit `a/`/`b/` prefixes so diff.mnemonicPrefix /
diff.noprefix in the user's git config cannot hide the changed files.

Output: `missing <citation> -> <resolved> <file>:<line>` per miss, then
`RECEIPT_PRESENCE: mode=… rev=… records=K cited=N present=P missing=M verdict=OK|MISSING`.
Exit 0 OK, 1 MISSING, 2 setup error.  Read-only (git show / diff / cat-file /
ls-tree / ls-files / check-ignore only).

Limits: only the six record-file classes; only `receipts/` paths with the seven
extensions (w1 evidence such as `.ufo/waves/round-N/w1/...-results.json` is not
checked); nested `receipts/<dir>/<name>` forms are not recognised; pre-existing
citations on unchanged lines are not re-checked; in --worktree mode `--base` is
the branch tip the helper will commit on.
"""
from __future__ import annotations

import argparse
import fnmatch
import itertools
import os
import re
import shutil
import subprocess
import sys
import tempfile

RECORD_FILES = re.compile(r"^(SCORECARD\.md|LOG\.md|corpus/QUALITY\.md|corpus/README\.md|corpus/lessons/[^/]+\.md|corpus/knowledge/[^/]+\.md)$")
CITE = re.compile(r"(?<![A-Za-z0-9_./-])((?:\.ufo/waves/round-\d+/|quality/)?receipts/[A-Za-z0-9._{},*-]+?\.(?:txt|json|jsonl|md|log|csv|tsv))(?![A-Za-z0-9_-])(?!\.[A-Za-z0-9])")
ROUND_TOKEN = re.compile(r"-r(\d+)(?=[-.])")
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")
BRACE = re.compile(r"\{([^{}]*)\}")
PREFIXES = ("--src-prefix=a/", "--dst-prefix=b/")


def git(repo: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)


def added_lines(diff: str) -> list[tuple[str, int, str]]:
    out, path, n = [], None, 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else None
            continue
        if line.startswith("--- ") or line.startswith("diff "):
            continue
        m = HUNK.match(line)
        if m:
            n = int(m.group(1))
            continue
        if path is None or not RECORD_FILES.match(path):
            continue
        if line.startswith("+"):
            out.append((path, n, line[1:]))
            n += 1
        elif not line.startswith("-"):
            n += 1
    return out


def expand(cite: str) -> list[str]:
    """Expand every `{a,b}` group; a cite without braces is itself."""
    parts = BRACE.split(cite)
    if len(parts) == 1:
        return [cite]
    fixed, choices = parts[0::2], [p.split(",") for p in parts[1::2]]
    out = []
    for combo in itertools.product(*choices):
        s = fixed[0]
        for c, f in zip(combo, fixed[1:]):
            s += c + f
        out.append(s)
    return out


def candidates(cite: str, round_no: int | None) -> list[str]:
    if not cite.startswith("receipts/"):
        return [cite]
    name = cite[len("receipts/"):]
    tokens = [int(t) for t in ROUND_TOKEN.findall(name)]
    rounds = list(dict.fromkeys(reversed(tokens))) if tokens else ([round_no] if round_no is not None else [])
    out = [f".ufo/waves/round-{k}/receipts/{name}" for k in rounds]
    out.append(f"quality/receipts/{name}")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--worktree", action="store_true")
    ap.add_argument("--base")
    ap.add_argument("--commit-path", nargs="+", default=[])
    ap.add_argument("--round", type=int)
    ap.add_argument("--selftest", action="store_true",
                    help="run the fixture selftest for the exit codes and finding lines")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()

    def setup(msg: str) -> int:
        print(f"RECEIPT_PRESENCE: SETUP_ERROR {msg}")
        return 2

    repo = a.repo
    if git(repo, "rev-parse", "--git-dir").returncode != 0:
        return setup(f"not a git repository: {repo}")
    top = git(repo, "rev-parse", "--show-toplevel").stdout.strip()
    round_no = a.round
    extra: list[tuple[str, int, str]] = []
    if a.worktree:
        if not a.base or a.rev:
            return setup("--worktree needs --base and no --rev")
        if not a.commit_path:
            return setup("--worktree needs --commit-path")
        r = git(repo, "rev-parse", "--verify", a.base + "^{commit}")
        if r.returncode != 0:
            return setup(f"bad --base {a.base}")
        base = r.stdout.strip()
        d = git(repo, "diff", "--no-color", "--no-ext-diff", "--no-renames", *PREFIXES, "-U0", base, "--")
        if d.returncode != 0:
            return setup("git diff failed")
        untracked = git(repo, "ls-files", "--others", "--exclude-standard", "-z")
        if untracked.returncode != 0:
            return setup("git ls-files failed")
        for p in untracked.stdout.split("\0"):
            if p and RECORD_FILES.match(p):
                try:
                    with open(os.path.join(top, p), encoding="utf-8") as fh:
                        extra += [(p, i + 1, t) for i, t in enumerate(fh.read().splitlines())]
                except (OSError, UnicodeDecodeError):
                    return setup(f"unreadable untracked record {p}")
        cpaths = []
        for p in a.commit_path:
            rel = os.path.relpath(os.path.realpath(os.path.join(top, p)), os.path.realpath(top))
            if rel.startswith(".."):
                return setup(f"commit path outside the repository: {p}")
            cpaths.append(rel)
        base_tree = set(git(repo, "ls-tree", "-r", "--name-only", "-z", base).stdout.split("\0")) - {""}

        def carried(p: str) -> bool:
            exact = p in cpaths
            covered = exact or any(p.startswith(c + "/") for c in cpaths)
            if not covered:
                return p in base_tree
            if not os.path.isfile(os.path.join(top, p)):
                return False
            if not exact and git(repo, "check-ignore", "-q", "--", p).returncode == 0:
                return False
            return True

        def universe(pattern: str) -> list[str]:
            d0 = os.path.dirname(pattern)
            names = {p for p in base_tree if os.path.dirname(p) == d0}
            ondisk = os.path.join(top, d0)
            if os.path.isdir(ondisk):
                names |= {os.path.join(d0, n) for n in os.listdir(ondisk)}
            return sorted(names)

        mode, rev = "worktree", base
    else:
        if not a.rev:
            return setup("--rev or --worktree required")
        r = git(repo, "rev-parse", "--verify", a.rev + "^{commit}")
        if r.returncode != 0:
            return setup(f"bad --rev {a.rev}")
        rev = r.stdout.strip()
        if round_no is None:
            subj = git(repo, "log", "-1", "--format=%s", rev).stdout
            m = re.match(r"round-(\d+)\b", subj)
            round_no = int(m.group(1)) if m else None
        d = git(repo, "show", "--no-color", "--no-ext-diff", "--no-renames", *PREFIXES, "-U0", "--format=", rev, "--")
        if d.returncode != 0:
            return setup("git show failed")
        rev_tree = set(git(repo, "ls-tree", "-r", "--name-only", "-z", rev).stdout.split("\0")) - {""}

        def carried(p: str) -> bool:
            return p in rev_tree

        def universe(pattern: str) -> list[str]:
            d0 = os.path.dirname(pattern)
            return sorted(p for p in rev_tree if os.path.dirname(p) == d0)

        mode = "rev"

    def present(p: str) -> bool:
        if "*" in p:
            return any(fnmatch.fnmatchcase(q, p) and carried(q) for q in universe(p))
        return carried(p)

    lines = added_lines(d.stdout) + extra
    records = sorted({p for p, _, _ in lines})
    cited = present_n = missing = 0
    for path, n, text in lines:
        for m in CITE.finditer(text):
            for cite in expand(m.group(1)):
                cited += 1
                cands = candidates(cite, round_no)
                if any(present(c) for c in cands):
                    present_n += 1
                else:
                    missing += 1
                    print(f"missing {cite} -> {cands[0]} {path}:{n}")
    verdict = "OK" if missing == 0 else "MISSING"
    print(f"RECEIPT_PRESENCE: mode={mode} rev={rev} records={len(records)} cited={cited} present={present_n} "
          f"missing={missing} verdict={verdict}")
    return 0 if missing == 0 else 1


def selftest() -> int:
    """Build a throwaway fixture and assert exit codes and finding lines.

    One repository under a temporary directory holds three commits: a base,
    an OK change citing a receipt it carries, a MISSING change citing a
    receipt it does not, plus a bad-rev setup probe.  Six labelled checks --
    OK-rc, OK-lines, MISSING-rc, MISSING-lines, SETUP-rc, SETUP-lines, one
    exit-code and one output assertion per probe -- each print
    `RECEIPT_PRESENCE_SELFTEST: FAIL <label>` when they fail, with the detail
    on a `RECEIPT_PRESENCE_SELFTEST_DETAIL:` line.  Nothing outside the
    temporary directory is touched; the fixture identity (`fixture
    <fixture@invalid>`) is passed with `-c` and never written to any
    configuration.
    """
    root = tempfile.mkdtemp(prefix="receipt-presence-selftest-")
    env = {"PATH": os.environ.get("PATH", "/usr/bin"), "HOME": root, "LC_ALL": "C", "TMPDIR": root,
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0"}

    def g(d: str, *args: str) -> str:
        r = subprocess.run(["git", "-C", d, *args], capture_output=True, text=True, env=env)
        if r.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} rc={r.returncode}: {r.stderr.strip()}")
        return r.stdout

    try:
        d = os.path.join(root, "fx")
        os.makedirs(d)
        g(d, "init", "-q")
        top = g(d, "rev-parse", "--show-toplevel").strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise RuntimeError(f"fixture toplevel {top} != {d}")
        ident = ("-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "-c", "commit.gpgsign=false")

        def put(path: str, text: str) -> None:
            full = os.path.join(d, *path.split("/"))
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "a" if os.path.exists(full) else "w", encoding="utf-8") as fh:
                fh.write(text)

        def commit(msg: str) -> str:
            g(d, "add", "-A", "-f")
            g(d, *ident, "commit", "-q", "-m", msg)
            return g(d, "rev-parse", "HEAD").strip()

        put("SCORECARD.md", "base\n")
        commit("base")
        put("quality/receipts/ok-r91.txt", "evidence\n")
        put("SCORECARD.md", "ok cites quality/receipts/ok-r91.txt\n")
        rev_ok = commit("round-91: ok")
        put("SCORECARD.md", "gone cites .ufo/waves/round-91/receipts/gone-r91.txt\n")
        rev_missing = commit("round-91: missing")
        bad = "d" * 40

        def run(args: list[str]) -> tuple[int, list[str]]:
            r = subprocess.run([sys.executable, "-I", os.path.realpath(__file__), *args],
                               capture_output=True, text=True, env=env)
            return r.returncode, r.stdout.splitlines()

        rc_ok, out_ok = run(["--repo", d, "--rev", rev_ok])
        rc_missing, out_missing = run(["--repo", d, "--rev", rev_missing])
        rc_setup, out_setup = run(["--repo", d, "--rev", bad])
        ok_line = "cited=1 present=1 missing=0 verdict=OK"
        gone_line = ("missing .ufo/waves/round-91/receipts/gone-r91.txt -> "
                     ".ufo/waves/round-91/receipts/gone-r91.txt SCORECARD.md:3")
        setup_line = f"RECEIPT_PRESENCE: SETUP_ERROR bad --rev {bad}"
        observations = [
            ("OK-rc", rc_ok == 0, f"rc={rc_ok} lines={out_ok}"),
            ("OK-lines", any(ok_line in ln for ln in out_ok), f"want {ok_line!r} in lines={out_ok}"),
            ("MISSING-rc", rc_missing == 1, f"rc={rc_missing} lines={out_missing}"),
            ("MISSING-lines", gone_line in out_missing and any("verdict=MISSING" in ln for ln in out_missing),
             f"want {gone_line!r} lines={out_missing}"),
            ("SETUP-rc", rc_setup == 2, f"rc={rc_setup} lines={out_setup}"),
            ("SETUP-lines", setup_line in out_setup, f"want {setup_line!r} lines={out_setup}"),
        ]
    finally:
        shutil.rmtree(root, ignore_errors=True)
    checks = [(n, ok) for n, ok, _ in observations]
    failed = [n for n, ok in checks if not ok]
    for n in failed:
        print(f"RECEIPT_PRESENCE_SELFTEST: FAIL {n}")
    for n, ok, detail in observations:
        if not ok:
            print(f"RECEIPT_PRESENCE_SELFTEST_DETAIL: {n} {detail}")
    print(f"RECEIPT_PRESENCE_SELFTEST: checks={len(checks)} failed={len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
