#!/usr/bin/env python3
"""Measure the frozen round-22 closure workloads with the round-21 child runner.

Fixture contents are scanner inputs only; this driver never executes them and
reports measurements without turning them into an acceptance score.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import resource
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WAVE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[3]
WORKLOAD_ROOT = WAVE_ROOT / "w1" / "resource-closure"
FIXTURE_ROOT = WORKLOAD_ROOT / "fixtures"
MANIFEST_PATH = WORKLOAD_ROOT / "manifest.json"
MANIFEST_SHA_PATH = WORKLOAD_ROOT / "manifest.sha256"
ROUND21_RUNNER_PATH = REPO_ROOT / ".ufo" / "waves" / "round-21" / "resource" / "measure.py"
EXPECTED_MANIFEST_SHA256 = "6a357933412f838840afbaf63e58bdce016b824f7d0144d2e20d628473d4d99a"
POPULATION = (512, 1024, 2048)
ADDRESS_SPACE_BYTES = 402653184
TIMEOUT_SECONDS = 15
CAPTURE_LIMIT_BYTES = 1_000_000
EXPECTED_CASE = {
    "verdict": "clean",
    "exit": 0,
    "findings": 0,
    "eval_unparsed": 0,
    "unparsed_spawns": 0,
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_manifest_bytes() -> tuple[bytes, str, str]:
    raw = MANIFEST_PATH.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    sidecar = MANIFEST_SHA_PATH.read_text(encoding="ascii").split()
    if actual != EXPECTED_MANIFEST_SHA256:
        raise ValueError("resource-closure manifest differs from the frozen digest")
    if sidecar != [EXPECTED_MANIFEST_SHA256, "manifest.json"]:
        raise ValueError("resource-closure manifest.sha256 does not match the frozen manifest")
    return raw, actual, sidecar[0]


def load_manifest() -> tuple[dict[str, Any], str, list[tuple[dict[str, Any], Path]]]:
    raw, manifest_sha, _ = read_manifest_bytes()
    manifest = json.loads(raw)
    if not isinstance(manifest, dict) or manifest.get("schema") != "mado-r22-resource-closure-workloads-v1":
        raise ValueError("unsupported resource-closure manifest schema")
    if manifest.get("population") != list(POPULATION):
        raise ValueError("resource-closure population does not match its frozen 512/1024/2048 declaration")
    if manifest.get("address_space_limit_bytes") != ADDRESS_SPACE_BYTES or manifest.get("timeout_seconds") != TIMEOUT_SECONDS:
        raise ValueError("resource-closure manifest limits differ from the required child bounds")
    if manifest.get("processes_per_scan") != 1:
        raise ValueError("resource-closure manifest must specify one child per scan")

    cases = manifest.get("cases")
    if not isinstance(cases, list) or len(cases) != len(POPULATION):
        raise ValueError("resource-closure manifest must contain all three frozen cases")
    if not FIXTURE_ROOT.is_dir() or FIXTURE_ROOT.is_symlink():
        raise ValueError("resource-closure fixtures directory is missing or is a symlink")
    fixture_root = FIXTURE_ROOT.resolve(strict=True)
    checked: list[tuple[dict[str, Any], Path]] = []

    for expected_size, case in zip(POPULATION, cases):
        if not isinstance(case, dict):
            raise ValueError("resource-closure case is not an object")
        filename = f"fixtures/stored-closures-{expected_size}.jsonl"
        if case.get("file") != filename:
            raise ValueError(f"resource-closure case order/name mismatch: expected {filename}")
        for key in ("stored_closures", "factory_calls", "unrelated_caller_bindings"):
            if type(case.get(key)) is not int or case[key] != expected_size:
                raise ValueError(f"resource-closure {filename} has an unexpected {key} value")
        if type(case.get("spawn_calls")) is not int or case["spawn_calls"] != 0:
            raise ValueError(f"resource-closure {filename} must have zero spawn calls")
        if case.get("expected") != EXPECTED_CASE:
            raise ValueError(f"resource-closure {filename} has unexpected frozen expectations")
        expected_digest = case.get("sha256")
        expected_bytes = case.get("size_bytes")
        if not isinstance(expected_digest, str) or len(expected_digest) != 64:
            raise ValueError(f"resource-closure {filename} has no valid SHA-256 declaration")
        if type(expected_bytes) is not int or expected_bytes < 0:
            raise ValueError(f"resource-closure {filename} has no valid byte-size declaration")

        candidate = WORKLOAD_ROOT / filename
        if candidate.is_symlink():
            raise ValueError(f"resource-closure input is a symlink: {filename}")
        fixture = candidate.resolve(strict=True)
        if fixture.parent != fixture_root or not fixture.is_file():
            raise ValueError(f"resource-closure input escaped the fixture directory: {filename}")
        if fixture.stat().st_size != expected_bytes or sha256_file(fixture) != expected_digest:
            raise ValueError(f"resource-closure input does not match its frozen size/digest: {filename}")
        checked.append((case, fixture))

    return manifest, manifest_sha, checked


def verify_manifest_unchanged(expected_sha: str) -> str:
    _raw, actual, _sidecar = read_manifest_bytes()
    if actual != expected_sha:
        raise ValueError("resource-closure manifest changed during measurement")
    return actual


def load_round21_runner():
    spec = importlib.util.spec_from_file_location("mado_r21_resource_measure_for_r22", ROUND21_RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the round-21 resource runner")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_runner(module: Any, manifest: dict[str, Any]) -> None:
    if not hasattr(os, "wait4") or not hasattr(resource, "RLIMIT_AS"):
        raise RuntimeError("round-21 resource measurements require Linux wait4 and RLIMIT_AS")
    if not callable(getattr(module, "run_one", None)):
        raise RuntimeError("round-21 resource runner does not expose run_one")
    if module.ADDRESS_SPACE_BYTES != manifest["address_space_limit_bytes"]:
        raise ValueError("round-21 runner address-space cap differs from the closure manifest")
    if module.WALL_TIMEOUT_SECONDS != manifest["timeout_seconds"]:
        raise ValueError("round-21 runner timeout differs from the closure manifest")
    if module.CAPTURE_LIMIT_BYTES != CAPTURE_LIMIT_BYTES:
        raise ValueError("round-21 runner output capture limit changed")


def scanner_summary(measurement: dict[str, Any]) -> dict[str, Any]:
    stdout = measurement.get("stdout")
    summary: dict[str, Any] = {
        "schema": None,
        "findings": None,
        "finding_count": None,
        "eval_unparsed": None,
        "unparsed_spawns": None,
        "unparsed_total": None,
        "parse_error": None,
    }
    if not isinstance(stdout, dict) or not isinstance(stdout.get("text"), str):
        summary["parse_error"] = "runner returned no captured stdout text"
        return summary
    if stdout.get("truncated"):
        summary["parse_error"] = "captured stdout was truncated; scanner payload is incomplete"
        return summary
    output_lines = [line for line in stdout["text"].splitlines() if line.strip()]
    if not output_lines:
        summary["parse_error"] = "scanner stdout was empty"
        return summary
    try:
        payload = json.loads(output_lines[-1])
    except (TypeError, ValueError) as exc:
        summary["parse_error"] = f"scanner payload is not JSON: {type(exc).__name__}: {exc}"
        return summary
    if not isinstance(payload, dict):
        summary["parse_error"] = "scanner payload is not a JSON object"
        return summary

    summary["schema"] = payload.get("schema")
    findings = payload.get("findings")
    files = payload.get("files")
    if not isinstance(findings, list):
        summary["parse_error"] = "scanner payload has no findings list"
        return summary
    summary["findings"] = findings
    summary["finding_count"] = len(findings)
    if not isinstance(files, list):
        summary["parse_error"] = "scanner payload has no files list"
        return summary

    eval_unparsed = 0
    unparsed_spawns = 0
    for file_result in files:
        if not isinstance(file_result, dict):
            summary["parse_error"] = "scanner files list contains a non-object row"
            return summary
        eval_count = file_result.get("eval_unparsed")
        spawn_count = file_result.get("unparsed_spawns")
        if type(eval_count) is not int or eval_count < 0 or type(spawn_count) is not int or spawn_count < 0:
            summary["parse_error"] = "scanner file row has missing or invalid unparsed counters"
            return summary
        eval_unparsed += eval_count
        unparsed_spawns += spawn_count
    summary["eval_unparsed"] = eval_unparsed
    summary["unparsed_spawns"] = unparsed_spawns
    summary["unparsed_total"] = eval_unparsed + unparsed_spawns
    return summary


def selected_tool(raw: str) -> Path:
    path = Path(raw).expanduser().resolve(strict=True)
    if not path.is_file():
        raise ValueError("--tool must name a regular file")
    if not path.is_relative_to(REPO_ROOT):
        raise ValueError("--tool must resolve inside the repository")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, help="selected scanner file")
    parser.add_argument("--mode", required=True, choices=("module-main", "cli"))
    args = parser.parse_args()

    receipt: dict[str, Any] = {
        "schema": "mado-r22-resource-closure-measure-v1",
        "interpretation": "Descriptive measurements only; this artifact does not score detector correctness.",
        "mode": args.mode,
        "start": timestamp(),
        "end": None,
        "tool": None,
        "tool_sha256_before": None,
        "tool_sha256_after": None,
        "receipt_runner_sha256": sha256_file(Path(__file__).resolve()),
        "round21_runner": str(ROUND21_RUNNER_PATH),
        "round21_runner_sha256": None,
        "manifest": str(MANIFEST_PATH),
        "manifest_sha256_before": None,
        "manifest_sha256_after": None,
        "manifest_sidecar_sha256": None,
        "address_space_limit_bytes": ADDRESS_SPACE_BYTES,
        "timeout_seconds": TIMEOUT_SECONDS,
        "processes_per_scan": 1,
        "cases": [],
        "integrity_errors": [],
        "driver_error": None,
        "receipt_complete": False,
        "driver_exit": 2,
    }

    driver_exit = 2
    try:
        tool = selected_tool(args.tool)
        receipt["tool"] = str(tool)
        receipt["tool_sha256_before"] = sha256_file(tool)
        manifest, manifest_sha, cases = load_manifest()
        receipt["manifest_sha256_before"] = manifest_sha
        receipt["manifest_sidecar_sha256"] = manifest_sha

        runner = load_round21_runner()
        validate_runner(runner, manifest)
        runner.FIXTURE_DIR = FIXTURE_ROOT.resolve(strict=True)
        round21_runner_sha = sha256_file(ROUND21_RUNNER_PATH)
        receipt["round21_runner_sha256"] = round21_runner_sha
        python = str(Path(sys.executable).resolve(strict=True))

        for case, fixture in cases:
            verify_manifest_unchanged(manifest_sha)
            expected_input_sha = case["sha256"]
            if sha256_file(fixture) != expected_input_sha:
                receipt["integrity_errors"].append(f"input changed before scan: {fixture.name}")
                break

            compatible_case = {
                "statements": case["stored_closures"],
                "expected": case["expected"],
            }
            measurement = runner.run_one(
                args.mode,
                python,
                tool,
                fixture,
                compatible_case,
                round21_runner_sha,
                manifest_sha,
            )
            measurement.pop("statements", None)
            measurement["workload"] = {
                "stored_closures": case["stored_closures"],
                "factory_calls": case["factory_calls"],
                "unrelated_caller_bindings": case["unrelated_caller_bindings"],
                "spawn_calls": case["spawn_calls"],
                "size_bytes": case["size_bytes"],
            }
            measurement["manifest_sha256_before"] = manifest_sha
            measurement["scanner_summary"] = scanner_summary(measurement)
            manifest_after = verify_manifest_unchanged(manifest_sha)
            measurement["manifest_sha256_after"] = manifest_after
            receipt["manifest_sha256_after"] = manifest_after

            fixture_before = measurement.get("fixture_sha256_before")
            fixture_after = measurement.get("fixture_sha256_after")
            if fixture_before != expected_input_sha or fixture_after != expected_input_sha:
                receipt["integrity_errors"].append(f"input digest changed across scan: {fixture.name}")
            tool_before = measurement.get("tool_sha256_before")
            tool_after = measurement.get("tool_sha256_after")
            if tool_before != receipt["tool_sha256_before"] or tool_after != receipt["tool_sha256_before"]:
                receipt["integrity_errors"].append(f"selected tool digest changed across scan: {fixture.name}")
            if not measurement.get("process_started") or not measurement.get("process_reaped"):
                receipt["integrity_errors"].append(f"child was not completely measured/reaped: {fixture.name}")
            receipt["cases"].append(measurement)
            if receipt["integrity_errors"]:
                break

        receipt["manifest_sha256_after"] = verify_manifest_unchanged(manifest_sha)
        receipt["tool_sha256_after"] = sha256_file(tool)
        if receipt["tool_sha256_after"] != receipt["tool_sha256_before"]:
            receipt["integrity_errors"].append("selected tool digest changed during the workload")
        receipt["receipt_complete"] = (
            len(receipt["cases"]) == len(POPULATION)
            and not receipt["integrity_errors"]
            and all(row.get("process_started") and row.get("process_reaped") for row in receipt["cases"])
        )
        driver_exit = 0 if receipt["receipt_complete"] else 2
    except (OSError, RuntimeError, ValueError, TypeError, json.JSONDecodeError) as exc:
        receipt["driver_error"] = f"{type(exc).__name__}: {exc}"
    except Exception as exc:
        receipt["driver_error"] = f"{type(exc).__name__}: {exc}"

    receipt["driver_exit"] = driver_exit
    receipt["end"] = timestamp()
    sys.stdout.write(json.dumps(receipt, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n")
    return driver_exit


if __name__ == "__main__":
    raise SystemExit(main())
