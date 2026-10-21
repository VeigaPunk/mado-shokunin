#!/usr/bin/env python3
"""Bounded sequential scanner measurement harness; measurement is not run here.

Select --mode module-main to load the scanner in a capped child and call
main(["--scan", fixture]) directly. This deliberately uses one fixed wrapper
for before/after comparisons and bypasses the scanner's __main__ stack wrapper.
Select --mode cli for the ordinary `python -I tool --scan fixture` path. The
scanner currently requests a 512 MiB worker-thread stack; that fixed virtual
reservation can fail under the required 384 MiB RLIMIT_AS in CLI mode. Preserve
that failure as observed (exit/stderr/RSS); do not raise the 384 MiB cap or
misstate CLI failure as quadratic retained-memory evidence. Reduce unnecessary
fixed stack reservation in the scanner itself rather than widening the cap.

Each eval JSONL is passed only as an argument to --scan; this harness never
executes fixture source. It reads no /proc paths. Each invocation is sequential,
uses one child, gets a 15-second wall deadline and reports wait4 ru_maxrss.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import selectors
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
FIXTURE_DIR = ROOT / "fixtures"
MANIFEST_PATH = ROOT / "manifest.json"
MANIFEST_SHA_PATH = ROOT / "manifest.sha256"
ADDRESS_SPACE_BYTES = 384 * 1024 * 1024
WALL_TIMEOUT_SECONDS = 15
CAPTURE_LIMIT_BYTES = 1_000_000
READ_CHUNK_BYTES = 64 * 1024
POLL_INTERVAL_SECONDS = 0.05

API_MAIN_WRAPPER = """\
import importlib.util, sys
spec = importlib.util.spec_from_file_location('_mado_r21_scan_target', sys.argv[1])
if spec is None or spec.loader is None:
    raise RuntimeError('cannot load selected scanner module')
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
result = module.main(['--scan', sys.argv[2]])
if result is not None:
    raise SystemExit(result)
"""


class StreamCapture:
    def __init__(self) -> None:
        self.digest = hashlib.sha256()
        self.total_bytes = 0
        self.prefix = bytearray()

    def add(self, chunk: bytes) -> None:
        self.digest.update(chunk)
        self.total_bytes += len(chunk)
        remaining = CAPTURE_LIMIT_BYTES - len(self.prefix)
        if remaining > 0:
            self.prefix.extend(chunk[:remaining])

    def result(self) -> dict[str, Any]:
        return {
            "text": self.prefix.decode("utf-8", errors="replace"),
            "bytes": self.total_bytes,
            "sha256": self.digest.hexdigest(),
            "truncated": self.total_bytes > len(self.prefix),
        }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def limit_child_address_space() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (ADDRESS_SPACE_BYTES, ADDRESS_SPACE_BYTES))


def load_manifest() -> dict[str, Any]:
    manifest_bytes = MANIFEST_PATH.read_bytes()
    sidecar = MANIFEST_SHA_PATH.read_text(encoding="ascii").strip().split()
    if len(sidecar) != 2 or sidecar[1] != "manifest.json":
        raise ValueError("manifest.sha256 must contain one manifest.json digest")
    actual_manifest_sha = hashlib.sha256(manifest_bytes).hexdigest()
    if sidecar[0] != actual_manifest_sha:
        raise ValueError("manifest.json SHA-256 does not match manifest.sha256")
    manifest = json.loads(manifest_bytes)
    if manifest.get("schema") != "mado-r21-resource-workloads-v1":
        raise ValueError("unsupported workload manifest schema")
    cases = manifest.get("cases")
    if not isinstance(cases, list) or [case.get("statements") for case in cases] != [1000, 2000, 4000]:
        raise ValueError("manifest must enumerate the exact 1000/2000/4000 workload population")
    expected = {"verdict": "clean", "exit": 0, "findings": 0}
    if any(case.get("expected") != expected for case in cases):
        raise ValueError("workload expectations must remain clean with exit 0 and zero findings")
    for case in cases:
        fixture = ROOT / case["file"]
        if fixture.parent != FIXTURE_DIR or sha256_file(fixture) != case["sha256"]:
            raise ValueError(f"workload fixture is missing or has a mismatched SHA-256: {case.get('file')}")
    return manifest


def command_for(mode: str, python: str, tool: Path, fixture: Path) -> list[str]:
    if mode == "module-main":
        return [python, "-I", "-c", API_MAIN_WRAPPER, str(tool), str(fixture)]
    return [python, "-I", str(tool), "--scan", str(fixture)]


def kill_process_group(pid: int) -> None:
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def wait4_nonblocking(pid: int) -> tuple[int, int, Any] | None:
    while True:
        try:
            waited_pid, status, usage = os.wait4(pid, os.WNOHANG)
            break
        except InterruptedError:
            continue
    if waited_pid == 0:
        return None
    return waited_pid, status, usage


def run_one(mode: str, python: str, tool: Path, fixture: Path, case: dict[str, Any], runner_sha: str, manifest_sha: str) -> dict[str, Any]:
    fixture_sha_before = sha256_file(fixture)
    tool_sha_before = sha256_file(tool)
    argv = command_for(mode, python, tool, fixture)
    started = time.monotonic()
    deadline = started + WALL_TIMEOUT_SECONDS
    stdout_capture = StreamCapture()
    stderr_capture = StreamCapture()
    timed_out = False
    reaped = False
    reap_timeout = False
    exit_code: int | None = None
    max_rss_kib: int | None = None
    spawn_error: str | None = None
    proc: subprocess.Popen[bytes] | None = None
    selector = selectors.DefaultSelector()

    try:
        proc = subprocess.Popen(
            argv,
            cwd=str(FIXTURE_DIR),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
            close_fds=True,
            start_new_session=True,
            preexec_fn=limit_child_address_space,
        )
        assert proc.stdout is not None and proc.stderr is not None
        for stream, capture, label in (
            (proc.stdout, stdout_capture, "stdout"),
            (proc.stderr, stderr_capture, "stderr"),
        ):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, (capture, label))


        while True:
            now = time.monotonic()
            if not timed_out and now >= deadline:
                timed_out = True
                kill_process_group(proc.pid)
            if not reaped:
                waited = wait4_nonblocking(proc.pid)
                if waited is not None:
                    _, status_word, usage = waited
                    exit_code = os.waitstatus_to_exitcode(status_word)
                    max_rss_kib = int(usage.ru_maxrss)
                    proc.returncode = exit_code
                    reaped = True
            if reaped and not selector.get_map():
                break
            if timed_out and time.monotonic() >= deadline + 1.0:
                if not reaped:
                    reap_timeout = True
                break

            wait_seconds = POLL_INTERVAL_SECONDS
            if not timed_out:
                wait_seconds = min(wait_seconds, max(0.0, deadline - time.monotonic()))
            for key, _ in selector.select(wait_seconds):
                stream = key.fileobj
                capture, _label = key.data
                try:
                    chunk = os.read(stream.fileno(), READ_CHUNK_BYTES)
                except BlockingIOError:
                    continue
                if chunk:
                    capture.add(chunk)
                else:
                    selector.unregister(stream)
                    stream.close()
    except (OSError, subprocess.SubprocessError) as exc:
        spawn_error = f"{type(exc).__name__}: {exc}"
    finally:
        if proc is not None:
            if proc.returncode is None:
                kill_process_group(proc.pid)
                cleanup_deadline = time.monotonic() + 0.25
                while time.monotonic() < cleanup_deadline:
                    waited = wait4_nonblocking(proc.pid)
                    if waited is None:
                        time.sleep(0.01)
                        continue
                    _, status_word, usage = waited
                    exit_code = os.waitstatus_to_exitcode(status_word)
                    max_rss_kib = int(usage.ru_maxrss)
                    proc.returncode = exit_code
                    reaped = True
                    break
                if proc.returncode is None:
                    reap_timeout = True
            else:
                reaped = True
            for stream in (proc.stdout, proc.stderr):
                if stream is not None and not stream.closed:
                    try:
                        selector.unregister(stream)
                    except (KeyError, ValueError):
                        pass
                    stream.close()
        selector.close()

    elapsed = time.monotonic() - started
    fixture_sha_after = sha256_file(fixture)
    tool_sha_after = sha256_file(tool)
    return {
        "schema": "mado-r21-resource-measure-v1",
        "mode": mode,
        "fixture": str(fixture),
        "statements": case["statements"],
        "expected": case["expected"],
        "command": argv,
        "address_space_limit_bytes": ADDRESS_SPACE_BYTES,
        "timeout_seconds": WALL_TIMEOUT_SECONDS,
        "exit": exit_code,
        "timed_out": timed_out,
        "spawn_error": spawn_error,
        "elapsed_seconds": round(elapsed, 6),
        "wait4_ru_maxrss_kib": max_rss_kib,
        "tool_sha256_before": tool_sha_before,
        "tool_sha256_after": tool_sha_after,
        "fixture_sha256_before": fixture_sha_before,
        "fixture_sha256_after": fixture_sha_after,
        "runner_sha256": runner_sha,
        "manifest_sha256": manifest_sha,
        "api_main_wrapper_sha256": hashlib.sha256(API_MAIN_WRAPPER.encode("utf-8")).hexdigest(),
        "stdout": stdout_capture.result(),
        "stderr": stderr_capture.result(),
        "process_started": proc is not None,
        "process_reaped": reaped,
        "reap_timeout": reap_timeout,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, help="selected mado-tripwire.py file")
    parser.add_argument(
        "--mode",
        choices=("module-main", "cli"),
        required=True,
        help="module-main isolates scan memory from the 512 MiB CLI stack wrapper; cli measures normal startup separately",
    )
    parser.add_argument("--python", default=sys.executable, help="Python interpreter used for the child")
    return parser.parse_args()


def main() -> int:
    if not hasattr(os, "wait4") or not hasattr(resource, "RLIMIT_AS"):
        raise RuntimeError("this harness requires Linux wait4 and RLIMIT_AS")
    args = parse_args()
    tool = Path(args.tool).expanduser().resolve(strict=True)
    if not tool.is_file():
        raise ValueError("--tool must name a regular file")
    python = str(Path(args.python).expanduser().resolve(strict=True))
    manifest = load_manifest()
    runner_sha = sha256_file(Path(__file__).resolve())
    manifest_sha = sha256_file(MANIFEST_PATH)
    for case in manifest["cases"]:
        fixture = (ROOT / case["file"]).resolve(strict=True)
        result = run_one(args.mode, python, tool, fixture, case, runner_sha, manifest_sha)
        sys.stdout.write(json.dumps(result, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n")
        sys.stdout.flush()
        if result["process_started"] and not result["process_reaped"]:
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
