#!/usr/bin/env python3
"""check-seat-reports — did every dispatched seat leave its report file?

A wave dispatch (`.ufo/waves/round-<N>/<wave>-dispatch.json`) renders each seat
a trailer `Report: write your scoped findings to <path>` (residual calls carry
one plain `Report: <path>` line instead; it is used when the rendered trailer
is absent; the last matching line wins).  A seat whose report
is not in the lane tree left its findings only in transport (lesson M90-4:
R90MScoutSources and R90MScoutCases).  This check reads every dispatch of the
named round(s) and verifies that each trailer path is a non-empty file.

Modes:
  --rev REV       read dispatches and reports from the committed tree at REV
                  (`git ls-tree` / `git cat-file`; the lane is only read)
  --worktree      read them from the working tree under --repo (gate a round's
                  records commit before the helper commits it)
Scope: `--round N` (repeatable) or `--all` (every `.ufo/waves/round-<N>/<wave>-dispatch.json`, the
validator's dispatch layout since round 37; the legacy `round-<N>/<wave>/dispatch.json` files of rounds 13-20
are not read).  A trailer is a whole line: a mention inside a sentence or a path followed by prose is
not one, and a path is one token (no spaces).

Findings (one line each, stable ids):
  SR01 missing <round>/<wave> <seat> <path>    trailer path absent
  SR02 empty <round>/<wave> <seat> <path>      trailer path is an empty file
  SR03 unsafe <round>/<wave> <seat> <path>     trailer path absolute, with a '..' component,
                                               or a symlink (not a regular report file)
  SR04 untrailed <round>/<wave> <seat>         task text names no report path (the seat
                                               cannot be checked)
Summary: `SEAT_REPORTS: mode=… rev=… rounds=R waves=W seats=N trailered=T
present=P missing=M empty=E unsafe=U untrailed=X verdict=OK|MISSING`.
Exit 0 OK, 1 any finding, 2 setup error (no repo, bad rev, named round without
a dispatch, a dispatch that is not JSON or lacks taskCall.tasks).
`--selftest` checks the exit codes and finding ids on throwaway fixtures.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

TRAILER = re.compile(r"^Report: write your scoped findings to (\S+)\s*$", re.M)
PLAIN = re.compile(r"^Report: (\S+)\s*$", re.M)  # residual calls: no rendered trailer, one plain line
DISPATCH = re.compile(r"^\.ufo/waves/round-(\d+)/([A-Za-z0-9_-]+)-dispatch\.json$")


class SetupError(Exception):
    pass


class GitTree:
    def __init__(self, repo: str, rev: str):
        self.repo = repo
        r = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise SetupError(f"not a commit: {rev}")
        self.rev = r.stdout.strip()
        r = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "-l", "-z", self.rev], capture_output=True)
        if r.returncode != 0:
            raise SetupError("git ls-tree failed")
        # regular blobs (100644/100755) are reports; a symlink (120000) is recorded as unsafe, as in --worktree mode
        self.sizes: dict[str, int] = {}
        self.links: set[str] = set()
        for rec in r.stdout.split(b"\0"):
            if not rec:
                continue
            meta, path = rec.split(b"\t", 1)
            parts = meta.split()
            name = path.decode("utf-8", "surrogateescape")
            if parts[0] == b"120000":
                self.links.add(name)
            elif parts[1] == b"blob":
                self.sizes[name] = int(parts[3])

    def paths(self) -> list[str]:
        return [p for p in self.sizes if p.startswith(".ufo/waves/")]

    def size(self, path: str) -> int | None:
        return self.sizes.get(path)

    def is_link(self, path: str) -> bool:
        return path in self.links

    def read(self, path: str) -> bytes:
        r = subprocess.run(["git", "-C", self.repo, "cat-file", "blob", f"{self.rev}:{path}"], capture_output=True)
        if r.returncode != 0:
            raise SetupError(f"cannot read {path} at {self.rev}")
        return r.stdout


class WorkTree:
    def __init__(self, repo: str):
        if not os.path.isdir(repo):
            raise SetupError(f"no such directory: {repo}")
        self.repo = repo
        self.rev = "worktree"

    def paths(self) -> list[str]:
        out = []
        base = os.path.join(self.repo, ".ufo", "waves")
        for d, _, files in os.walk(base):
            for f in files:
                out.append(os.path.relpath(os.path.join(d, f), self.repo).replace(os.sep, "/"))
        return out

    def size(self, path: str) -> int | None:
        p = os.path.join(self.repo, path)
        if os.path.islink(p) or not os.path.isfile(p):
            return None
        return os.path.getsize(p)

    def is_link(self, path: str) -> bool:
        return os.path.islink(os.path.join(self.repo, path))

    def read(self, path: str) -> bytes:
        try:
            with open(os.path.join(self.repo, path), "rb") as fh:
                return fh.read()
        except OSError as e:
            raise SetupError(f"cannot read {path}: {e}") from None


def unsafe(path: str) -> bool:
    return path.startswith("/") or ".." in path.split("/")


def check(tree, rounds: list[int] | None) -> tuple[list[str], dict]:
    dispatches: dict[int, list[tuple[str, str]]] = {}
    for p in tree.paths():
        m = DISPATCH.match(p)
        if m:
            dispatches.setdefault(int(m.group(1)), []).append((m.group(2), p))
    if rounds is None:
        if not dispatches:
            raise SetupError("--all: no <wave>-dispatch.json under .ufo/waves/")
        rounds = sorted(dispatches)
    for n in rounds:
        if n not in dispatches:
            raise SetupError(f"round {n}: no <wave>-dispatch.json in .ufo/waves/round-{n}/")
    lines: list[str] = []
    c = {"rounds": len(rounds), "waves": 0, "seats": 0, "trailered": 0, "present": 0, "missing": 0, "empty": 0,
         "unsafe": 0, "untrailed": 0}
    for n in rounds:
        for wave, p in sorted(dispatches[n]):
            try:
                d = json.loads(tree.read(p).decode("utf-8"))
                tasks = d["taskCall"]["tasks"]
                if not isinstance(tasks, list):
                    raise TypeError
            except (ValueError, KeyError, TypeError, UnicodeDecodeError):
                raise SetupError(f"{p}: not a dispatch (taskCall.tasks)") from None
            c["waves"] += 1
            for t in tasks:
                c["seats"] += 1
                name = str(t.get("name", "?")) if isinstance(t, dict) else "?"
                text = t.get("task", "") if isinstance(t, dict) else ""
                body = text if isinstance(text, str) else ""
                found = TRAILER.findall(body) or PLAIN.findall(body)
                where = f"round-{n}/{wave}"
                if not found:
                    c["untrailed"] += 1
                    lines.append(f"SR04 untrailed {where} {name}")
                    continue
                c["trailered"] += 1
                rp = found[-1]
                if unsafe(rp) or tree.is_link(rp):
                    c["unsafe"] += 1
                    lines.append(f"SR03 unsafe {where} {name} {rp}")
                    continue
                size = tree.size(rp)
                if size is None:
                    c["missing"] += 1
                    lines.append(f"SR01 missing {where} {name} {rp}")
                elif size == 0:
                    c["empty"] += 1
                    lines.append(f"SR02 empty {where} {name} {rp}")
                else:
                    c["present"] += 1
    return lines, c


def run(repo: str, rev: str | None, worktree: bool, rounds: list[int] | None, out=print) -> int:
    try:
        tree = WorkTree(repo) if worktree else GitTree(repo, rev or "HEAD")
        lines, c = check(tree, rounds)
    except SetupError as e:
        out(f"SEAT_REPORTS: SETUP_ERROR {e}")
        return 2
    for ln in lines:
        out(ln)
    bad = c["missing"] + c["empty"] + c["unsafe"] + c["untrailed"]
    verdict = "MISSING" if bad else "OK"
    out(f"SEAT_REPORTS: mode={'worktree' if worktree else 'rev'} rev={tree.rev} rounds={c['rounds']} "
        f"waves={c['waves']} seats={c['seats']} trailered={c['trailered']} present={c['present']} "
        f"missing={c['missing']} empty={c['empty']} unsafe={c['unsafe']} untrailed={c['untrailed']} "
        f"verdict={verdict}")
    return 1 if bad else 0


def selftest() -> int:
    results: list[tuple[str, bool]] = []

    def task(name: str, path: str | None) -> dict:
        body = f"Own: {path}\n" if path else "no trailer\n"
        if path:
            body += f"\nReport: write your scoped findings to {path}"
        return {"name": name, "agent": "scout", "task": body}

    def case(label: str, files: dict, rounds, want_rc: int, want_ids: list[str], git: bool = False) -> None:
        with tempfile.TemporaryDirectory() as d:
            for rel, body in files.items():
                p = os.path.join(d, rel)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                if isinstance(body, dict):
                    os.symlink(body["symlink"], p)
                    continue
                with open(p, "wb") as fh:
                    fh.write(body if isinstance(body, bytes) else body.encode())
            if git:
                # rev mode on a throwaway repository inside d (fixture identity, never written to a config)
                g = ["git", "-C", d]
                env = {"PATH": os.environ.get("PATH", "/usr/bin"), "HOME": d, "GIT_CONFIG_NOSYSTEM": "1"}
                try:
                    subprocess.run(g + ["init", "-q"], check=True, env=env, capture_output=True)
                    top = subprocess.run(g + ["rev-parse", "--show-toplevel"], capture_output=True, text=True,
                                         env=env).stdout.strip()
                    if os.path.realpath(top) != os.path.realpath(d):
                        results.append((label, False))
                        return
                    subprocess.run(g + ["add", "-A"], check=True, env=env, capture_output=True)
                    subprocess.run(g + ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "-c",
                                        "commit.gpgsign=false", "commit", "-q", "-m", "fixture"], check=True, env=env,
                                   capture_output=True)
                except (OSError, subprocess.CalledProcessError):
                    results.append((label, False))
                    return
            got: list[str] = []
            rc = run(d, "HEAD" if git else None, not git, rounds, out=got.append)
            ids = [g.split()[0] for g in got if re.match(r"^SR0[1-4] ", g)]
            mode = "rev" if git else "worktree"
            ok = rc == want_rc and ids == want_ids and (rc == 2 or got[-1].startswith(f"SEAT_REPORTS: mode={mode}"))
            results.append((label, ok))

    W = ".ufo/waves/round-7"
    disp = lambda *ts: json.dumps({"taskCall": {"context": "c", "tasks": list(ts)}})
    case("all present -> OK rc0", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": "x"},
         [7], 0, [])
    case("missing -> SR01 rc1", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md"), task("B", f"{W}/w1/B.md")),
                                 f"{W}/w1/A.md": "x"}, [7], 1, ["SR01"])
    case("empty -> SR02 rc1", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": ""},
         [7], 1, ["SR02"])
    case("unsafe -> SR03 rc1", {f"{W}/w1-dispatch.json": disp(task("A", "../x.md"))}, [7], 1, ["SR03"])
    case("untrailed -> SR04 rc1", {f"{W}/r1-dispatch.json": disp(task("A", None))}, [7], 1, ["SR04"])
    case("symlinked report -> SR03 rc1", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")),
                                          f"{W}/w1/real.md": "x", f"{W}/w1/A.md": {"symlink": "real.md"}}, [7], 1, ["SR03"])
    case("prose Report line is not a trailer -> SR04", {f"{W}/r1-dispatch.json": disp({"name": "A", "task":
         "Report: findings go in the usual place\n"})}, [7], 1, ["SR04"])
    case("plain residual trailer -> SR01 rc1", {f"{W}/r1-dispatch.json": disp({"name": "A", "task":
         f"do it\nReport: {W}/r1/A.md\n"})}, [7], 1, ["SR01"])
    case("no dispatch for round -> rc2", {f"{W}/w1/A.md": "x"}, [7], 2, [])
    case("bad dispatch json -> rc2", {f"{W}/w1-dispatch.json": "{"}, [7], 2, [])
    case("last trailer wins", {f"{W}/w1-dispatch.json": disp({"name": "A", "task":
         f"Report: write your scoped findings to {W}/w1/old.md\nReport: write your scoped findings to {W}/w1/A.md"}),
         f"{W}/w1/old.md": "x"}, [7], 1, ["SR01"])
    case("--all scans every round", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": "x",
                                     ".ufo/waves/round-8/w1-dispatch.json": disp(task("B", ".ufo/waves/round-8/w1/B.md"))},
         None, 1, ["SR01"])
    case("--all with no dispatch -> rc2", {f"{W}/w1/A.md": "x"}, None, 2, [])
    case("rev: present -> OK rc0", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": "x"},
         [7], 0, [], git=True)
    case("rev: symlinked report -> SR03 rc1", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")),
                                               f"{W}/w1/real.md": "x", f"{W}/w1/A.md": {"symlink": "real.md"}},
         [7], 1, ["SR03"], git=True)
    case("rev: empty and missing -> SR02 SR01 rc1", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md"),
         task("B", f"{W}/w1/B.md")), f"{W}/w1/A.md": ""}, [7], 1, ["SR02", "SR01"], git=True)
    failed = [n for n, ok in results if not ok]
    for n in failed:
        print(f"SEAT_REPORTS_SELFTEST_FAIL: {n}")
    print(f"SEAT_REPORTS_SELFTEST: checks={len(results)} failed={len(failed)}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=".")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--rev")
    g.add_argument("--worktree", action="store_true")
    ap.add_argument("--round", type=int, action="append", dest="rounds")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.all and not a.rounds:
        print("SEAT_REPORTS: SETUP_ERROR name --round N or --all")
        return 2
    if a.all and a.rounds:
        print("SEAT_REPORTS: SETUP_ERROR --round and --all are exclusive")
        return 2
    return run(a.repo, a.rev, a.worktree, None if a.all else a.rounds)


if __name__ == "__main__":
    sys.exit(main())
