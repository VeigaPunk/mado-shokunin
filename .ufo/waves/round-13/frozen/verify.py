#!/usr/bin/env python3
"""Frozen two-evidences runner for the mado verdict gate.

expected.json (next to this script) is the committed input snapshot and
expected verdict — exactly these keys and exactly these two input names:

  {"inputs": {"gate.sh": "<sha256>", "harness.sh": "<sha256>"},
   "expected_exit": 0, "expected_marker": "MADO_REGRESSION: PASS"}

Both digests are verified before any execution; only then does the runner run
`bash gate.sh --regression` with MADO_VERIFY_HARNESS=<scriptdir>/harness.sh.
Exit/stable-id map: 0 frozen_match; 1 frozen_verdict_mismatch; 2
snapshot_tampered (missing/changed/escaping input, nothing run); 2 frozen_error
(bad expected.json or run could not start). `--selftest` asserts those cases
over isolated fixtures with hardcoded digests; it never runs the real gate or
harness, touches the network, or reads the host config.
"""

import hashlib, io, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

MATCH, MISMATCH = "frozen_match", "frozen_verdict_mismatch"
TAMPERED, ERROR = "snapshot_tampered", "frozen_error"
FILES, TIMEOUT = ("gate.sh", "harness.sh"), 900

# Fixture bytes and their pinned digests, fixed when this file was written.
# The self-test never recomputes these from the fixtures it creates.
CLEAN_GATE = """#!/bin/bash
d=${0%/*}
printf 'MADO_REGRESSION: PASS (case=fixture; target=deadbeef)\\n'; printf '%s' "$MADO_VERIFY_HARNESS" > "$d/harness.path"; : > "$d/invoked.marker"; exit 0
"""
CLEAN_SHA = "c2e246e5b663be4f2604f3180f380c516e5fe9cc588cafd760c016107d87f13b"
BAD_GATE = """#!/bin/bash
d=${0%/*}
printf 'MADO_REGRESSION: FAIL (case=fixture; target=deadbeef)\\n'; : > "$d/invoked.marker"; exit 0
"""
BAD_SHA = "e86db8e029cdd9b2d9257b14d223e409a532262be262bea7029303989a74ab55"
TAMPERED_GATE = CLEAN_GATE + "# byte added after the expected digest was pinned\n"
HARNESS = """#!/bin/bash
exit 0
"""
HARNESS_SHA = "c87c7a722d59a266b300850637a1cb77b46cc67c5add8a66aa9e79e198955808"


class FrozenError(Exception):
    pass


def emit(stream, kind, stable_id, details=()):
    print(f"MADO_FROZEN: {kind}", file=stream)
    for detail in details:
        print(f"FROZEN_DETAIL: {detail}", file=stream)
    print(f"FROZEN_ID: {stable_id}", file=stream)


def load(root):
    path = root / "expected.json"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise FrozenError(f"missing {path}")
    except (OSError, ValueError) as exc:
        raise FrozenError(f"cannot parse {path}: {exc}")
    if not isinstance(raw, dict) or set(raw) != {"inputs", "expected_exit", "expected_marker"}:
        raise FrozenError("expected.json must be exactly {inputs, expected_exit, expected_marker}")
    pins = raw["inputs"]
    if not isinstance(pins, dict) or set(pins) != set(FILES):
        raise FrozenError("inputs must pin exactly gate.sh and harness.sh")
    if any(not isinstance(d, str) or len(d) != 64 or set(d.lower()) - set("0123456789abcdef")
           for d in pins.values()):
        raise FrozenError("input digests must be sha256 hex strings")
    if type(raw["expected_exit"]) is not int:
        raise FrozenError("expected_exit must be an integer")
    if not isinstance(raw["expected_marker"], str) or not raw["expected_marker"].strip():
        raise FrozenError("expected_marker must be a non-empty string")
    return {k: v.lower() for k, v in pins.items()}, raw["expected_exit"], raw["expected_marker"]


def check(root, pins, stream):
    failures = []
    for name in FILES:
        target = (root / name).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            failures.append(f"unsafe {name}: resolves outside the frozen root")
            continue
        if not target.is_file():
            failures.append(f"missing {name}")
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != pins[name]:
            failures.append(f"mismatch {name} expected={pins[name]} actual={actual}")
        else:
            print(f"FROZEN_INPUT: {name} sha256={actual} verified", file=stream)
    return failures


def evaluate(root, stream=sys.stdout):
    root = root.resolve()
    try:
        pins, expected_exit, marker = load(root)
    except FrozenError as exc:
        emit(stream, "ERROR", ERROR, [str(exc)])
        return 2
    failures = check(root, pins, stream)
    if failures:
        emit(stream, "TAMPERED", TAMPERED, [f"failures={len(failures)}"] + failures)
        return 2
    gate, harness = (root / "gate.sh").resolve(), (root / "harness.sh").resolve()
    print(f"FROZEN_RUN: bash {gate} --regression (cwd={root}, harness={harness})", file=stream)
    try:
        run = subprocess.run(
            ["bash", str(gate), "--regression"], cwd=str(root),
            env=dict(os.environ, MADO_VERIFY_HARNESS=str(harness)),
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, timeout=TIMEOUT)
    except (subprocess.TimeoutExpired, OSError) as exc:
        emit(stream, "ERROR", ERROR, [f"cannot run the frozen gate: {exc}"])
        return 2
    output = run.stdout or ""
    if output:
        stream.write(output if output.endswith("\n") else output + "\n")
    problems = []
    if run.returncode != expected_exit:
        problems.append(f"exit {run.returncode} != expected {expected_exit}")
    if marker not in output:
        problems.append(f"marker {marker!r} absent from the frozen run output")
    if problems:
        emit(stream, "MISMATCH", MISMATCH, problems)
        return 1
    emit(stream, "MATCH", MATCH, [f"exit={run.returncode} marker={marker!r}"])
    return 0


def selftest():
    passed, failed = 0, []

    def expect(condition, name):
        nonlocal passed, failed
        passed, failed = (passed + 1, failed) if condition else (passed, failed + [name])

    tmp = Path(tempfile.mkdtemp(prefix="mado-r13-frozen-selftest."))

    def case(name, gate, pins, raw=None):
        root = tmp / name
        root.mkdir()
        if gate is not None:
            (root / "gate.sh").write_bytes(gate.encode())
        (root / "harness.sh").write_bytes(HARNESS.encode())
        (root / "expected.json").write_bytes(raw if raw is not None else json.dumps(
            {"inputs": pins, "expected_exit": 0,
             "expected_marker": "MADO_REGRESSION: PASS"}).encode())
        stream = io.StringIO()
        return root, evaluate(root, stream), stream.getvalue()

    try:
        root, rc, out = case("clean", CLEAN_GATE, {"gate.sh": CLEAN_SHA, "harness.sh": HARNESS_SHA})
        expect(rc == 0 and "FROZEN_ID: frozen_match" in out, "clean: 0 frozen_match")
        expect((root / "harness.path").read_text() == str((root / "harness.sh").resolve()),
               "clean: harness override")
        root, rc, out = case("verdict", BAD_GATE, {"gate.sh": BAD_SHA, "harness.sh": HARNESS_SHA})
        expect(rc == 1 and "FROZEN_ID: frozen_verdict_mismatch" in out,
               "verdict: 1 frozen_verdict_mismatch")
        expect((root / "invoked.marker").is_file(), "verdict: gate invoked")
        root, rc, out = case("tampered", TAMPERED_GATE,
                             {"gate.sh": CLEAN_SHA, "harness.sh": HARNESS_SHA})
        expect(rc == 2 and "FROZEN_ID: snapshot_tampered" in out, "tampered: 2 snapshot_tampered")
        expect("FROZEN_DETAIL: mismatch gate.sh" in out, "tampered: input named")
        expect(not (root / "invoked.marker").exists(), "tampered: gate not invoked")
        root, rc, out = case("missing", None, {"gate.sh": CLEAN_SHA, "harness.sh": HARNESS_SHA})
        expect(rc == 2 and "FROZEN_ID: snapshot_tampered" in out, "missing: 2 snapshot_tampered")
        expect("FROZEN_DETAIL: missing gate.sh" in out, "missing: input named")
        expect(not (root / "invoked.marker").exists(), "missing: gate not invoked")
        root, rc, out = case("malformed", CLEAN_GATE, {}, raw=b"{not json\n")
        expect(rc == 2 and "FROZEN_ID: frozen_error" in out, "malformed: 2 frozen_error")
        expect(not (root / "invoked.marker").exists(), "malformed: gate not invoked")
    finally:
        if not failed:
            shutil.rmtree(tmp, ignore_errors=True)
    if failed:
        print(f"MADO_FROZEN_SELFTEST: FAILED — {passed} passed, {len(failed)} failed")
        for name in failed:
            print(f"  - {name}")
        print(f"fixtures kept: {tmp}")
        return 2
    print(f"MADO_FROZEN_SELFTEST: {passed}/{passed} assertions passed")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    if len(sys.argv) > 1:
        print("usage: verify.py [--selftest]", file=sys.stderr)
        sys.exit(2)
    sys.exit(evaluate(Path(__file__).resolve().parent))
