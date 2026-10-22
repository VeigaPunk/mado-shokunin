#!/usr/bin/env python3
"""Round-23 no-harm guard battery for the tripwire classifier (stdlib only).

Runs the seven registered no-harm guards of round 23 sequentially, one child
process at a time, and prints exactly one JSON object describing every guard:
the exact argv, the child exit code, the parsed pass/total counts and the
guard-specific detail (corpus added/removed finding groups and error flips,
precision passing-name set versus the base revision).

Usage:
    python3 -I guards.py --tool PATH --base-tool PATH
                         [--precision-rev REV --precision-repo DIR]
                         [--lane-root DIR] [--out-dir DIR]

Exit codes:
    0  every guard passed
    1  at least one guard failed (a guard failure is a harm)
    2  a harness errored, timed out or produced unparsable output (fail closed)

The script writes only inside its out directory (default: the directory that
holds this script). No file outside the out directory is created, edited or
removed.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

DEFAULT_LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE_REV = "a28e4815aabfa85f55274884000fb2608355f8cf"
SCHEMA = "mado-r23-exec-guard-runner-v1"
SUMMARY_RE = re.compile(r"SELFTEST_SUMMARY:\s+(\d+)/(\d+)\s+passed\s+failed=\[(.*)\]")
CASE_ID_RE = re.compile(r"^CASE\s+(\S+)\s+(ok|FAIL)", re.MULTILINE)
LOG_TAIL = 4000

# Each guard gets its own wall-clock ceiling; the corpus comparator is the slow one.
TIMEOUTS = {
    "repair-12": 900,
    "residual-truth": 900,
    "r22-oracle-57": 900,
    "r21-oracle-replay": 900,
    "legacy-selftests": 1800,
    "corpus-comparator": 1800,
    "resource-closure-module-main": 900,
    "resource-closure-cli": 900,
    "resource-r21-module-main": 900,
    "resource-r21-cli": 900,
    "precision": 3600,
    "precision-base": 3600,
}


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tail(text: str, limit: int = LOG_TAIL) -> str:
    if len(text) <= limit:
        return text
    return "...[truncated %d bytes]...\n%s" % (len(text) - limit, text[-limit:])


def cap(text: str, limit: int = 32 * 1024 * 1024) -> str:
    """Keep the on-disk log bounded; the corpus receipt is the only large one."""
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...[truncated %d bytes]...\n" % (len(text) - limit)


class HarnessError(Exception):
    """A harness misbehaved: the battery must fail closed."""


class Guard:
    def __init__(self, gid: str, title: str, expect: str) -> None:
        self.id = gid
        self.title = title
        self.expect = expect
        self.argv: list[str] = []
        self.cwd: str | None = None
        self.exit: int | None = None
        self.timed_out = False
        self.harness_error = False
        self.error: str | None = None
        self.passed: int | None = None
        self.total: int | None = None
        self.pass_: bool | None = None
        self.detail: dict[str, Any] = {}
        self.stdout = ""
        self.stderr = ""
        self.duration = 0.0

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "expectation": self.expect,
            "argv": self.argv,
            "cwd": self.cwd,
            "exit": self.exit,
            "timed_out": self.timed_out,
            "harness_error": self.harness_error,
            "error": self.error,
            "passed": self.passed,
            "total": self.total,
            "pass": self.pass_,
            "duration_seconds": round(self.duration, 3),
            "detail": self.detail,
            "stdout_tail": tail(self.stdout),
            "stderr_tail": tail(self.stderr),
        }


class Battery:
    def __init__(self, lane_root: Path, out_dir: Path, stage_dir: Path) -> None:
        self.lane = lane_root
        self.out = out_dir
        self.stage_dir = stage_dir
        self.logs = out_dir / "logs"
        self.guards: list[Guard] = []

    # ---------------------------------------------------------------- utils
    def run(self, guard: Guard, argv: list[str], cwd: Path | None = None) -> None:
        guard.argv = list(argv)
        guard.cwd = str(cwd) if cwd else None
        timeout = TIMEOUTS.get(guard.id, 900)
        started = time.monotonic()
        try:
            proc = subprocess.run(
                argv,
                cwd=str(cwd) if cwd else None,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
            )
            guard.stdout = proc.stdout.decode("utf-8", errors="replace")
            guard.stderr = proc.stderr.decode("utf-8", errors="replace")
            guard.exit = proc.returncode
        except subprocess.TimeoutExpired as exc:
            guard.timed_out = True
            guard.harness_error = True
            guard.error = "harness_timeout_after_%ds" % timeout
            guard.stdout = (exc.stdout or b"").decode("utf-8", errors="replace")
            guard.stderr = (exc.stderr or b"").decode("utf-8", errors="replace")
        except OSError as exc:
            guard.harness_error = True
            guard.error = "spawn_failed: %s: %s" % (type(exc).__name__, exc)
        guard.duration = time.monotonic() - started
        self.write_log(guard)
        if guard.harness_error:
            raise HarnessError(guard.error or "harness error")

    def write_log(self, guard: Guard) -> None:
        try:
            self.logs.mkdir(parents=True, exist_ok=True)
            (self.logs / (guard.id + ".stdout.txt")).write_text(cap(guard.stdout), encoding="utf-8")
            (self.logs / (guard.id + ".stderr.txt")).write_text(cap(guard.stderr), encoding="utf-8")
            (self.logs / (guard.id + ".argv.json")).write_text(
                json.dumps({"argv": guard.argv, "cwd": guard.cwd, "exit": guard.exit}, indent=1),
                encoding="utf-8",
            )
        except OSError:
            pass  # logging is best effort; it never changes the verdict

    def json_stdout(self, guard: Guard) -> Any:
        text = guard.stdout.strip()
        if not text:
            raise HarnessError("%s: empty stdout" % guard.id)
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise HarnessError("%s: stdout is not JSON (%s)" % (guard.id, exc))

    def harness(self, guard: Guard, message: str) -> None:
        guard.harness_error = True
        guard.error = message
        raise HarnessError(message)

    # --------------------------------------------------------------- tools
    def stage(self, source: Path, name: str) -> Path:
        """Return a usable path for `source` that lives inside the lane tree.

        The round-22 replay driver and the round-22 resource driver refuse any
        scanner that does not resolve inside their own repository, so a scanner
        that lives outside the lane tree is copied into the lane's guard staging
        directory (never anywhere else).
        """
        source = source.resolve(strict=True)
        try:
            source.relative_to(self.lane)
            return source
        except ValueError:
            pass
        self.stage_dir.mkdir(parents=True, exist_ok=True)
        staged = self.stage_dir / name
        shutil.copyfile(source, staged)
        return staged


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tool", required=True, help="candidate classifier file")
    parser.add_argument("--base-tool", required=True, help="base classifier file (base revision extract)")
    parser.add_argument("--precision-rev", help="commit holding the candidate tools/mado-tripwire.py")
    parser.add_argument("--precision-repo", help="git repository that holds --precision-rev")
    parser.add_argument("--lane", "--lane-root", dest="lane", default=DEFAULT_LANE,
                        help="repository that owns the harnesses and bounds the accepted tool paths "
                             "(the production lane, or an executor clone that carries the same harnesses)")
    parser.add_argument("--stage-dir", default=None,
                        help="directory inside --lane that receives a copy of an out-of-lane scanner "
                             "(default: <lane>/.ufo/waves/round-23/w1/out/ExecGuardRunner)")
    parser.add_argument("--out-dir", default=None, help="output directory (default: this script's directory)")
    parser.add_argument("--skip-corpus", action="store_true", help="skip the 1356-file corpus comparator")
    return parser.parse_args(argv)


def run_guard_1_repair(battery: Battery, tool: Path) -> None:
    guard = Guard("repair-12", "round-23 frozen 12-case repair set", "12/12")
    battery.guards.append(guard)
    harness = battery.lane / ".ufo/waves/round-23/repair/measure.py"
    battery.run(guard, ["python3", "-I", str(harness), "--tool", str(tool)], cwd=battery.lane)
    data = battery.json_stdout(guard)
    if not isinstance(data, dict) or "passed" not in data or "total" not in data:
        battery.harness(guard, "repair measure: missing passed/total")
    guard.passed = int(data["passed"])
    guard.total = int(data["total"])
    guard.detail = {"schema": data.get("schema"), "tool_sha256": data.get("tool_sha256"),
                    "results": [{"id": r.get("id"), "passed": r.get("passed")} for r in data.get("results", [])]}
    guard.pass_ = (guard.exit == 0 and guard.passed == guard.total == 12)


def run_guard_2_residual(battery: Battery, tool: Path) -> None:
    guard = Guard("residual-truth", "round-22 supplemental discovery guards", "4/4")
    battery.guards.append(guard)
    harness = battery.lane / ".ufo/waves/round-22/residual-truth/measure.py"
    battery.run(guard, ["python3", "-I", str(harness), "--tool", str(tool)], cwd=battery.lane)
    data = battery.json_stdout(guard)
    totals = data.get("totals") if isinstance(data, dict) else None
    if not isinstance(totals, dict) or "passed" not in totals or "total" not in totals:
        battery.harness(guard, "residual measure: missing totals.passed/total")
    guard.passed = int(totals["passed"])
    guard.total = int(totals["total"])
    guard.detail = {"tool_sha256": data.get("tool_sha256"),
                    "cases": [{"id": c.get("id"), "passed": c.get("passed")} for c in data.get("cases", [])]}
    guard.pass_ = (guard.exit == 0 and guard.passed == guard.total)


def run_guard_3_r22_oracle(battery: Battery, tool: Path) -> None:
    guard = Guard("r22-oracle-57", "round-22 pinned primary oracle", "57/57")
    battery.guards.append(guard)
    harness = battery.lane / ".ufo/waves/round-22/oracle/measure.py"
    battery.run(guard, ["python3", "-I", str(harness), "--tool", str(tool)], cwd=battery.lane)
    data = battery.json_stdout(guard)
    totals = data.get("totals") if isinstance(data, dict) else None
    if not isinstance(totals, dict) or "pass" not in totals or "total" not in totals:
        battery.harness(guard, "round-22 oracle: missing totals.pass/total")
    guard.passed = int(totals["pass"])
    guard.total = int(totals["total"])
    guard.detail = {"status": data.get("status"), "tool_sha256_before": data.get("tool_sha256_before"),
                    "integrity_errors": data.get("integrity_errors")}
    guard.pass_ = (guard.exit == 0 and guard.passed == guard.total == 57)


def run_guard_4_oracle_replay(battery: Battery, tool: Path) -> None:
    guard = Guard("r21-oracle-replay", "round-21 oracle via round-22 replay driver", "35/35 + 17/17")
    battery.guards.append(guard)
    harness = battery.lane / ".ufo/waves/round-22/replay.py"
    battery.run(guard, ["python3", "-I", str(harness), "--tool", str(tool), "--mode", "oracle"], cwd=battery.lane)
    receipt = battery.json_stdout(guard)
    if receipt.get("spawn_error") or receipt.get("setup_error"):
        battery.harness(guard, "replay oracle: %s" % (receipt.get("spawn_error") or receipt.get("setup_error")))
    if receipt.get("timed_out"):
        battery.harness(guard, "replay oracle: timed out")
    inner = json.loads(receipt["stdout"])
    totals = inner.get("totals", {})
    primary = totals.get("primary", {})
    supplemental = totals.get("supplemental", {})
    guard.passed = int(primary.get("pass", -1)) + int(supplemental.get("pass", -1))
    guard.total = int(primary.get("total", 0)) + int(supplemental.get("total", 0))
    guard.detail = {"replay_exit": receipt.get("exit"), "primary": primary, "supplemental": supplemental,
                    "tool_sha256": receipt.get("tool_sha256")}
    guard.pass_ = (receipt.get("exit") == 0 and primary.get("pass") == primary.get("total") == 35
                   and supplemental.get("pass") == supplemental.get("total") == 17)


def selftest_suites(battery: Battery) -> list[tuple[str, Path]]:
    summary = battery.lane / ".ufo/waves/round-22/evidence/resume/legacy-selftests-summary.json"
    data = json.loads(summary.read_text(encoding="utf-8"))
    suites: list[tuple[str, Path]] = []
    for entry in data:
        name = entry["suite"]
        directory = battery.lane / ".ufo" / "waves" / name
        if not (directory / "expected.json").is_file():
            raise HarnessError("selftest suite directory is missing: %s" % directory)
        suites.append((name, directory))
    if len(suites) != 11:
        raise HarnessError("expected 11 selftest suites, found %d" % len(suites))
    return suites


def run_guard_5_selftests(battery: Battery, tool: Path) -> None:
    guard = Guard("legacy-selftests", "eleven legacy selftest suites", "247/247")
    battery.guards.append(guard)
    if shutil.which("prlimit") is None:
        battery.harness(guard, "prlimit is not available")
    suites = selftest_suites(battery)
    rows: list[dict[str, Any]] = []
    passed = 0
    total = 0
    ok = True
    for name, directory in suites:
        child = Guard("legacy-selftests", "", "")
        battery.run(child, ["prlimit", "--as=402653184", "--cpu=15", "python3", "-I", str(tool),
                            "--selftest", str(directory)], cwd=battery.lane)
        match = SUMMARY_RE.search(child.stdout)
        if match is None:
            battery.harness(guard, "selftest %s: no SELFTEST_SUMMARY line" % name)
        suite_passed = int(match.group(1))
        suite_total = int(match.group(2))
        failed_cases = match.group(3).strip()
        passed += suite_passed
        total += suite_total
        suite_ok = child.exit == 0 and suite_passed == suite_total and not failed_cases
        ok = ok and suite_ok
        rows.append({"suite": name, "argv": child.argv, "exit": child.exit,
                     "passed": suite_passed, "total": suite_total,
                     "failed_cases": failed_cases, "pass": suite_ok,
                     "case_lines": len(CASE_ID_RE.findall(child.stdout))})
    guard.passed = passed
    guard.total = total
    guard.exit = 0 if ok else 1
    guard.argv = rows[0]["argv"] if rows else []
    guard.detail = {"suites": rows, "prlimit": ["--as=402653184", "--cpu=15"],
                    "aggregate_of": len(rows), "child_argv": [row["argv"] for row in rows]}
    guard.pass_ = bool(ok and total == 247 and passed == total)


def group_findings(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group comparator rows into (path, class, rule, command, evidence) groups."""
    groups: dict[tuple, dict[str, Any]] = {}
    for row in rows:
        key = row.get("row") or []
        # comparator key: [line, tool_call_id, class, rule, command, evidence]
        line = key[0] if len(key) > 0 else None
        klass = key[2] if len(key) > 2 else None
        rule = key[3] if len(key) > 3 else None
        command = key[4] if len(key) > 4 else None
        evidence = key[5] if len(key) > 5 else None
        gkey = (row.get("path"), klass, rule, command, evidence)
        group = groups.setdefault(gkey, {"path": row.get("path"), "class": klass, "rule": rule,
                                         "command": command, "evidence": evidence,
                                         "lines": [], "count": 0})
        group["count"] += int(row.get("count", 1))
        if line not in group["lines"]:
            group["lines"].append(line)
    return [groups[key] for key in sorted(groups, key=lambda k: tuple(str(x) for x in k))]


def unparsed_counter_changes(inner: dict[str, Any]) -> dict[str, Any]:
    """Per-file unparsed counter deltas between the base and the candidate scan.

    The comparator keeps both runs in `runs.before` / `runs.after`; every row
    carries the scanner stats (eval_unparsed, unparsed_spawns) or an error.
    Rows whose counters differ are reported with the file path and both values.
    """
    before_rows = {row.get("path"): row for row in inner.get("runs", {}).get("before", [])}
    after_rows = {row.get("path"): row for row in inner.get("runs", {}).get("after", [])}
    changed: list[dict[str, Any]] = []
    unchanged = 0
    for path in sorted(set(before_rows) | set(after_rows)):
        before = before_rows.get(path) or {}
        after = after_rows.get(path) or {}
        before_stats = before.get("stats") or {}
        after_stats = after.get("stats") or {}
        counters = ("eval_unparsed", "unparsed_spawns")
        before_values = {key: before_stats.get(key) for key in counters}
        after_values = {key: after_stats.get(key) for key in counters}
        if before_values == after_values:
            unchanged += 1
            continue
        direction = "reduced"
        for key in counters:
            old = before_values.get(key)
            new = after_values.get(key)
            if isinstance(old, int) and isinstance(new, int):
                if new > old:
                    direction = "increased"
                elif new < old:
                    if direction == "increased":
                        direction = "mixed"
            else:
                direction = "mixed"
        changed.append({
            "path": path,
            "direction": direction,
            "eval_unparsed_before": before_values.get("eval_unparsed"),
            "eval_unparsed_after": after_values.get("eval_unparsed"),
            "unparsed_spawns_before": before_values.get("unparsed_spawns"),
            "unparsed_spawns_after": after_values.get("unparsed_spawns"),
            "before_error": before.get("error"),
            "after_error": after.get("error"),
        })
    increased = [row for row in changed if row["direction"] in ("increased", "mixed")]
    reduced = [row for row in changed if row["direction"] == "reduced"]
    return {"changed": changed, "increased": increased, "reduced": reduced,
            "unchanged_files": unchanged, "compared_files": len(set(before_rows) | set(after_rows))}


def run_guard_6_corpus(battery: Battery, tool: Path, base_tool: Path) -> None:
    guard = Guard("corpus-comparator", "1356-file corpus comparator against the base classifier",
                  "no added/removed finding group, no new error flip")
    battery.guards.append(guard)
    harness = battery.lane / ".ufo/waves/round-22/replay.py"
    battery.run(guard, ["python3", "-I", str(harness), "--tool", str(tool), "--mode", "corpus",
                        "--before-tool", str(base_tool)], cwd=battery.lane)
    receipt = battery.json_stdout(guard)
    if receipt.get("spawn_error") or receipt.get("setup_error"):
        battery.harness(guard, "replay corpus: %s" % (receipt.get("spawn_error") or receipt.get("setup_error")))
    if receipt.get("timed_out"):
        battery.harness(guard, "replay corpus: timed out")
    inner = json.loads(receipt["stdout"])
    added_groups = group_findings(inner.get("added_or_relabelled", []))
    removed_groups = group_findings(inner.get("removed_or_relabelled", []))
    errors = inner.get("errors", [])
    flips = [e for e in errors if e.get("before") != e.get("after")]
    shared = [e for e in errors if e.get("before") == e.get("after")]
    counters = unparsed_counter_changes(inner)
    guard.passed = len(added_groups) + len(removed_groups) + len(flips) + len(counters["increased"])
    guard.total = len(added_groups) + len(removed_groups) + len(flips) + len(counters["increased"])
    guard.detail = {
        "files": inner.get("files"),
        "retained": inner.get("retained"),
        "before_tool_sha256": inner.get("before_tool_sha256"),
        "after_tool_sha256": inner.get("after_tool_sha256"),
        "comparator_exit": receipt.get("exit"),
        "added_groups": added_groups,
        "removed_groups": removed_groups,
        "error_flips": flips,
        "shared_errors_count": len(shared),
        "shared_errors": shared,
        "unparsed_counter_changes": counters["changed"],
        "unparsed_counters_increased": counters["increased"],
        "unparsed_counters_reduced": counters["reduced"],
        "unparsed_counters_unchanged_files": counters["unchanged_files"],
        "unparsed_counters_compared_files": counters["compared_files"],
    }
    guard.pass_ = (not added_groups) and (not removed_groups) and (not flips) and (not counters["increased"])


def evaluate_resource_case(case: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    expected = case.get("expected") or {}
    summary = case.get("scanner_summary")
    if summary is None:
        # round-21 driver prints the raw measurement; compare its own summary fields
        summary = {"findings": [], "parse_error": None}
    if case.get("spawn_error"):
        reasons.append("spawn_error: %s" % case.get("spawn_error"))
    if case.get("timed_out"):
        reasons.append("timed_out")
    if not case.get("process_started", True):
        reasons.append("process_not_started")
    if not case.get("process_reaped", True):
        reasons.append("process_not_reaped")
    exit_code = case.get("exit")
    if "exit" in expected and exit_code != expected["exit"]:
        reasons.append("exit %r != expected %r" % (exit_code, expected["exit"]))
    if expected.get("verdict") == "clean" and summary.get("finding_count", 0) != expected.get("findings", 0):
        reasons.append("findings %r != expected %r" % (summary.get("finding_count"), expected.get("findings")))
    if summary.get("parse_error"):
        reasons.append("parse_error: %s" % summary.get("parse_error"))
    if summary.get("unparsed_total"):
        reasons.append("unparsed_total %r" % summary.get("unparsed_total"))
    elapsed = case.get("elapsed_seconds")
    if isinstance(elapsed, (int, float)) and elapsed > 15:
        reasons.append("elapsed %r > 15s" % elapsed)
    return (not reasons), reasons


def run_guard_7_resource(battery: Battery, tool: Path) -> None:
    closure = battery.lane / ".ufo/waves/round-22/resource-closure-measure.py"
    r21 = battery.lane / ".ufo/waves/round-21/resource/measure.py"

    for mode in ("module-main", "cli"):
        gid = "resource-closure-%s" % mode
        guard = Guard(gid, "round-22 closure resource population (%s)" % mode, "3/3 clean under 384 MiB / 15 s")
        battery.guards.append(guard)
        battery.run(guard, ["python3", "-I", str(closure), "--tool", str(tool), "--mode", mode], cwd=battery.lane)
        data = battery.json_stdout(guard)
        if data.get("driver_error"):
            battery.harness(guard, "resource closure %s: %s" % (mode, data.get("driver_error")))
        cases = data.get("cases", [])
        rows = []
        passed = 0
        for case in cases:
            ok, reasons = evaluate_resource_case(case)
            passed += int(ok)
            rows.append({"fixture": case.get("fixture"), "exit": case.get("exit"),
                         "elapsed_seconds": case.get("elapsed_seconds"),
                         "wait4_ru_maxrss_kib": case.get("wait4_ru_maxrss_kib"),
                         "workload": case.get("workload"), "reasons": reasons, "pass": ok})
        guard.passed = passed
        guard.total = len(cases)
        guard.detail = {"driver_exit": data.get("driver_exit"),
                        "receipt_complete": data.get("receipt_complete"),
                        "integrity_errors": data.get("integrity_errors"),
                        "address_space_limit_bytes": data.get("address_space_limit_bytes"),
                        "cases": rows}
        guard.pass_ = (guard.exit == 0 and data.get("driver_exit") == 0 and data.get("receipt_complete")
                       and passed == len(cases) == 3)

    for mode in ("module-main", "cli"):
        gid = "resource-r21-%s" % mode
        guard = Guard(gid, "round-21 assignment resource population (%s)" % mode, "3/3 clean under 384 MiB / 15 s")
        battery.guards.append(guard)
        battery.run(guard, ["python3", "-I", str(r21), "--tool", str(tool), "--mode", mode], cwd=battery.lane)
        rows = []
        passed = 0
        total = 0
        for line in guard.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                case = json.loads(line)
            except json.JSONDecodeError as exc:
                battery.harness(guard, "round-21 resource %s: unparsable JSON line (%s)" % (mode, exc))
            ok, reasons = evaluate_resource_case(case)
            passed += int(ok)
            total += 1
            rows.append({"fixture": case.get("fixture"), "exit": case.get("exit"),
                         "elapsed_seconds": case.get("elapsed_seconds"),
                         "wait4_ru_maxrss_kib": case.get("wait4_ru_maxrss_kib"),
                         "statements": case.get("statements"), "reasons": reasons, "pass": ok})
        guard.passed = passed
        guard.total = total
        guard.detail = {"cases": rows}
        guard.pass_ = (guard.exit == 0 and total == 3 and passed == total)


def precision_names(battery: Battery, repo: Path, rev: str, tool_sha: str | None) -> tuple[dict[str, Any], Guard]:
    gid = "precision" if rev != BASE_REV else "precision-base"
    guard = Guard(gid, "round-20 precision counter (%s)" % rev, "166/175 with the base passing set")
    battery.guards.append(guard)
    script = repo / ".ufo/waves/round-20/tw-precision.py"
    if not script.is_file():
        battery.harness(guard, "precision harness is missing: %s" % script)
    battery.run(guard, ["python3", "-I", str(script), rev], cwd=repo)
    data = battery.json_stdout(guard)
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        battery.harness(guard, "precision: no cases in output")
    passing = sorted(c["name"] for c in cases if c.get("pass"))
    failing = sorted(c["name"] for c in cases if not c.get("pass"))
    guard.passed = len(passing)
    guard.total = len(cases)
    guard.detail = {
        "commit": data.get("commit"),
        "tool_sha256": data.get("tool_sha256"),
        "families": data.get("families"),
        "score": data.get("score"),
        "passing_names": passing,
        "failing_names": failing,
    }
    if tool_sha is not None:
        guard.detail["candidate_tool_sha256"] = tool_sha
        guard.detail["tool_sha256_matches_candidate"] = (data.get("tool_sha256") == tool_sha)
    return {"passing": passing, "failing": failing, "total": len(cases),
            "tool_sha256": data.get("tool_sha256"), "commit": data.get("commit")}, guard


def run_precision(battery: Battery, repo: Path, rev: str, candidate_sha: str | None) -> None:
    base_info, base_guard = precision_names(battery, repo, BASE_REV, None)
    base_guard.expect = "base revision precision reference"
    base_guard.pass_ = True  # the reference run only exists to compare names

    cand_info, cand_guard = precision_names(battery, repo, rev, candidate_sha)
    same = cand_info["passing"] == base_info["passing"]
    cand_guard.detail["base_passing_names"] = base_info["passing"]
    cand_guard.detail["base_failing_names"] = base_info["failing"]
    cand_guard.detail["base_passed"] = len(base_info["passing"])
    cand_guard.detail["base_total"] = base_info["total"]
    cand_guard.detail["identical_passing_set"] = same
    cand_guard.detail["only_in_candidate"] = sorted(set(cand_info["passing"]) - set(base_info["passing"]))
    cand_guard.detail["only_in_base"] = sorted(set(base_info["passing"]) - set(cand_info["passing"]))
    reasons = []
    if not same:
        reasons.append("passing case set differs from the base revision")
    if candidate_sha is not None and cand_info["tool_sha256"] != candidate_sha:
        reasons.append("precision commit tool bytes differ from --tool bytes")
    cand_guard.detail["reasons"] = reasons
    cand_guard.pass_ = (cand_guard.exit == 0 and same and not reasons)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    script_dir = Path(__file__).resolve().parent
    out_dir = Path(args.out_dir).resolve() if args.out_dir else script_dir
    lane = Path(args.lane).resolve()
    if not (lane / ".ufo/waves/round-23/repair/measure.py").is_file():
        print(json.dumps({"schema": SCHEMA, "harness_error": "lane root is not the mado lane: %s" % lane}), file=sys.stdout)
        return 2
    stage_dir = Path(args.stage_dir).resolve() if args.stage_dir else lane / ".ufo/waves/round-23/w1/out/ExecGuardRunner"
    out_dir.mkdir(parents=True, exist_ok=True)
    battery = Battery(lane, out_dir, stage_dir)

    tool_arg = Path(args.tool)
    base_arg = Path(args.base_tool)
    try:
        tool = battery.stage(tool_arg, "staged-tool.py")
        base_tool = battery.stage(base_arg, "staged-base-tool.py")
    except OSError as exc:
        print(json.dumps({"schema": SCHEMA, "harness_error": "cannot stage tools: %s" % exc}))
        return 2

    tool_sha = sha256_file(tool)
    base_sha = sha256_file(base_tool)

    report: dict[str, Any] = {
        "schema": SCHEMA,
        "generated": now_iso(),
        "lane_root": str(lane),
        "stage_dir": str(stage_dir),
        "out_dir": str(out_dir),
        "python": sys.version.split()[0],
        "tool": {"argument": str(tool_arg), "used": str(tool), "sha256": tool_sha},
        "base_tool": {"argument": str(base_arg), "used": str(base_tool), "sha256": base_sha},
        "base_revision": BASE_REV,
        "guards": [],
        "summary": {},
        "overall": {},
    }

    harness_error: str | None = None
    try:
        run_guard_1_repair(battery, tool)
        run_guard_2_residual(battery, tool)
        run_guard_3_r22_oracle(battery, tool)
        run_guard_4_oracle_replay(battery, tool)
        run_guard_5_selftests(battery, tool)
        if not args.skip_corpus:
            run_guard_6_corpus(battery, tool, base_tool)
        else:
            guard = Guard("corpus-comparator", "1356-file corpus comparator", "skipped")
            guard.error = "skipped by --skip-corpus"
            battery.guards.append(guard)
        run_guard_7_resource(battery, tool)
        if args.precision_rev:
            if not args.precision_repo:
                raise HarnessError("--precision-rev requires --precision-repo")
            repo = Path(args.precision_repo).resolve()
            run_precision(battery, repo, args.precision_rev, tool_sha)
    except HarnessError as exc:
        harness_error = str(exc)
    except Exception as exc:  # unexpected driver failure is also a harness error
        harness_error = "battery_failure: %s: %s" % (type(exc).__name__, exc)

    guards = [g.to_json() for g in battery.guards]
    failed = [g.id for g in battery.guards if g.pass_ is False]
    errored = [g.id for g in battery.guards if g.harness_error]
    report["guards"] = guards
    report["summary"] = {
        "guards_run": len(battery.guards),
        "guards_passed": sum(1 for g in battery.guards if g.pass_ is True),
        "guards_failed": len(failed),
        "guards_errored": len(errored),
        "failed_ids": failed,
        "errored_ids": errored,
        "harness_error": harness_error,
    }
    if harness_error is not None or errored:
        exit_code = 2
        verdict = "harness-error"
    elif failed:
        exit_code = 1
        verdict = "guard-failure"
    else:
        exit_code = 0
        verdict = "pass"
    report["overall"] = {"exit": exit_code, "verdict": verdict}
    print(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=1))
    return exit_code


def entry(argv: list[str]) -> int:
    """Never let the battery die without emitting one JSON object."""
    try:
        return main(argv)
    except Exception as exc:  # fail closed
        print(json.dumps({"schema": SCHEMA, "generated": now_iso(),
                          "summary": {"harness_error": "battery_failure: %s: %s" % (type(exc).__name__, exc)},
                          "overall": {"exit": 2, "verdict": "harness-error"}},
                         ensure_ascii=True, sort_keys=True, indent=1))
        return 2


if __name__ == "__main__":
    sys.exit(entry(sys.argv[1:]))
