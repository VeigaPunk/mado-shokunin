#!/usr/bin/env python3
"""Materialize Round 21's inert, assignment-only eval scan workloads.

The generated eval source is data inside JSONL. This generator writes it but
never evaluates or scans it.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURE_DIR = ROOT / "fixtures"
SIZES = (1000, 2000, 4000)
TIMESTAMP = "2026-10-21T00:00:00.000Z"
EXPECTED = {"verdict": "clean", "exit": 0, "findings": 0}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fixture_bytes(size: int) -> bytes:
    code = "\n".join(f"binding_{index:04d} = {index}" for index in range(size))
    record = {
        "type": "message",
        "id": f"r21-resource-{size}",
        "timestamp": TIMESTAMP,
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "toolCall",
                    "id": f"eval-r21-resource-{size}",
                    "name": "eval",
                    "arguments": {"language": "py", "code": code},
                }
            ],
        },
    }
    return (json.dumps(record, ensure_ascii=True, separators=(",", ":")) + "\n").encode("utf-8")


def main() -> int:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    cases = []
    for size in SIZES:
        name = f"assignments-{size}.jsonl"
        data = fixture_bytes(size)
        (FIXTURE_DIR / name).write_bytes(data)
        cases.append(
            {
                "file": f"fixtures/{name}",
                "statements": size,
                "unique_assignment_targets": size,
                "spawn_calls": 0,
                "sha256": sha256_bytes(data),
                "expected": EXPECTED,
            }
        )

    manifest = {
        "schema": "mado-r21-resource-workloads-v1",
        "workload": "one eval toolCall containing unique shallow scalar assignments only",
        "execution_policy": "fixture source is data; never evaluate it",
        "processes_per_scan": 1,
        "address_space_limit_bytes": 384 * 1024 * 1024,
        "timeout_seconds": 15,
        "cases": cases,
        "generator_sha256": sha256_file(Path(__file__).resolve()),
    }
    manifest_data = (json.dumps(manifest, ensure_ascii=True, indent=2) + "\n").encode("utf-8")
    manifest_path = ROOT / "manifest.json"
    manifest_path.write_bytes(manifest_data)
    manifest_digest = sha256_bytes(manifest_data)
    (ROOT / "manifest.sha256").write_text(
        f"{manifest_digest}  manifest.json\n", encoding="ascii"
    )
    print(
        json.dumps(
            {
                "schema": "mado-r21-resource-generation-v1",
                "fixtures": len(cases),
                "manifest_sha256": manifest_digest,
                "fixture_sha256": {case["file"]: case["sha256"] for case in cases},
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
