#!/usr/bin/env python3
"""Run one scanner child over one fixture through round-21's resource helper.

Loads .ufo/waves/round-21/resource/measure.py and calls its run_one (384 MiB
RLIMIT_AS, 15 s wall deadline, wait4 ru_maxrss) unchanged; prints its receipt
plus a parsed verdict summary. Never executes fixture source.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
HELPER = LANE / ".ufo/waves/round-21/resource/measure.py"


def load_helper():
    spec = importlib.util.spec_from_file_location("_r21_resource_measure", HELPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def summary(stdout: str) -> dict:
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                verdict = json.loads(line)
            except ValueError:
                continue
            files = verdict.get("files") or []
            return {
                "verdict_exit": verdict.get("exit"),
                "error": verdict.get("error"),
                "findings": sorted({(f.get("class"), f.get("command"), f.get("evidence"))
                                    for f in verdict.get("findings", [])}),
                "file_errors": [f.get("error") for f in files if isinstance(f, dict) and f.get("error")],
                "eval_unparsed": sum(f.get("eval_unparsed", 0) for f in files if isinstance(f, dict)),
                "unparsed_spawns": sum(f.get("unparsed_spawns", 0) for f in files if isinstance(f, dict)),
            }
    return {"verdict_exit": None, "error": "no JSON verdict line"}


def main(argv: list[str]) -> int:
    tool, fixture, mode, label = Path(argv[0]).resolve(), Path(argv[1]).resolve(), argv[2], argv[3]
    helper = load_helper()
    case = {"statements": None, "expected": None}
    receipt = helper.run_one(mode, sys.executable, tool, fixture, case,
                             helper.sha256_file(HELPER), None)
    receipt["label"] = label
    receipt["helper"] = str(HELPER)
    receipt["helper_sha256"] = helper.sha256_file(HELPER)
    receipt["summary"] = summary(receipt["stdout"]["text"])
    print(json.dumps(receipt, sort_keys=True, default=list))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
