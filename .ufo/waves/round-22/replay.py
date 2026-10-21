#!/usr/bin/env python3
"""Run one explicit round-21 measurement command and emit its raw receipt.

The selected harnesses parse scanner fixtures; this driver does not execute
fixture contents or change any harness limits.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
ROUND21 = REPO_ROOT / ".ufo" / "waves" / "round-21"
ORACLE_TIMEOUT_SECONDS = 52 * 15 + 30
RESOURCE_TIMEOUT_SECONDS = 3 * 15 + 30
CORPUS_TIMEOUT_SECONDS = 2 * 600 + 30


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def selected_file(raw: str, option: str) -> Path:
    path = Path(raw).expanduser().resolve(strict=True)
    if not path.is_file():
        raise ValueError(f"{option} must name a regular file")
    if not path.is_relative_to(REPO_ROOT):
        raise ValueError(f"{option} must resolve inside the repository")
    return path


def command_for(mode: str, tool: Path, before_tool: Path | None) -> tuple[list[str], Path, int]:
    if mode == "oracle":
        runner = ROUND21 / "oracle" / "measure.py"
        argv = [sys.executable, "-I", str(runner), "--tool", str(tool)]
        timeout = ORACLE_TIMEOUT_SECONDS
    elif mode in ("resource-api", "resource-cli"):
        runner = ROUND21 / "resource" / "measure.py"
        runner_mode = "module-main" if mode == "resource-api" else "cli"
        argv = [sys.executable, "-I", str(runner), "--mode", runner_mode, "--tool", str(tool)]
        timeout = RESOURCE_TIMEOUT_SECONDS
    else:
        if mode != "corpus" or before_tool is None:
            raise ValueError("corpus mode requires --before-tool")
        runner = ROUND21 / "corpus" / "compare.py"
        argv = [
            sys.executable,
            "-I",
            str(runner),
            "--before-tool",
            str(before_tool),
            "--after-tool",
            str(tool),
        ]
        timeout = CORPUS_TIMEOUT_SECONDS
    return argv, runner, timeout


def run_bounded(argv: list[str], timeout: int) -> tuple[int | None, bytes, bytes, bool, str | None]:
    try:
        process = subprocess.Popen(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
    except OSError as exc:
        return None, b"", b"", False, f"{type(exc).__name__}: {exc}"

    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr, timed_out, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, help="selected scanner file")
    parser.add_argument(
        "--mode",
        required=True,
        choices=("oracle", "resource-api", "resource-cli", "corpus"),
    )
    parser.add_argument("--before-tool", help="required before-scanner for corpus comparison")
    args = parser.parse_args()
    if args.mode == "corpus" and not args.before_tool:
        parser.error("--before-tool is required with --mode corpus")
    if args.mode != "corpus" and args.before_tool:
        parser.error("--before-tool is only valid with --mode corpus")

    started = timestamp()
    receipt: dict[str, Any] = {
        "schema": "mado-r22-replay-receipt-v1",
        "mode": args.mode,
        "argv": [],
        "start": started,
        "end": None,
        "tool_sha256": None,
        "tool_sha256_after": None,
        "before_tool_sha256": None,
        "before_tool_sha256_after": None,
        "runner_sha256": None,
        "replay_sha256": sha256_file(Path(__file__).resolve()),
        "timeout_seconds": None,
        "timed_out": False,
        "exit": None,
        "stdout": "",
        "stderr": "",
        "spawn_error": None,
        "setup_error": None,
    }

    exit_code = 2
    try:
        tool = selected_file(args.tool, "--tool")
        before_tool = selected_file(args.before_tool, "--before-tool") if args.before_tool else None
        argv, runner, timeout = command_for(args.mode, tool, before_tool)
        if not runner.is_file():
            raise FileNotFoundError(f"round-21 runner is missing: {runner}")

        receipt["argv"] = argv
        receipt["tool_sha256"] = sha256_file(tool)
        if before_tool is not None:
            receipt["before_tool_sha256"] = sha256_file(before_tool)
        receipt["runner_sha256"] = sha256_file(runner)
        receipt["timeout_seconds"] = timeout

        exit_code, stdout, stderr, timed_out, spawn_error = run_bounded(argv, timeout)
        receipt["timed_out"] = timed_out
        receipt["exit"] = exit_code
        receipt["stdout"] = stdout.decode("utf-8", errors="surrogateescape")
        receipt["stderr"] = stderr.decode("utf-8", errors="surrogateescape")
        receipt["spawn_error"] = spawn_error
        receipt["tool_sha256_after"] = sha256_file(tool)
        if before_tool is not None:
            receipt["before_tool_sha256_after"] = sha256_file(before_tool)
        if exit_code is None:
            exit_code = 2
    except (OSError, RuntimeError, ValueError) as exc:
        receipt["setup_error"] = f"{type(exc).__name__}: {exc}"
        receipt["exit"] = 2

    receipt["end"] = timestamp()
    sys.stdout.write(json.dumps(receipt, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
