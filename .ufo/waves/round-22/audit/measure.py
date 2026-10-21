#!/usr/bin/env python3
"""Run a selected C2 audit tool against sealed artifact-only fixtures."""

import argparse
import base64
import hashlib
import json
import math
import os
import resource
import signal
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path, PurePosixPath

SCHEMA = "mado-r22-audit-fixtures-v1"
CAP_BYTES = 384 * 1024 * 1024
TIMEOUT_SECONDS = 15
OUTPUT_CAP = 1024 * 1024
MAX_FILE_BYTES = 16 * 1024 * 1024
MAX_EXPECTED_BYTES = 16 * 1024 * 1024


class HarnessError(ValueError):
    pass


class Tampered(HarnessError):
    pass


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def reject_constant(value):
    raise HarnessError("nonfinite JSON number: " + value)


def finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise HarnessError("nonfinite JSON number")
    return number


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise HarnessError("duplicate JSON key: " + key)
        result[key] = value
    return result


def parse_json(raw, label):
    try:
        text = raw.decode("utf-8")
        if text.startswith("\ufeff"):
            raise HarnessError("UTF-8 BOM is not accepted")
        return json.loads(text, object_pairs_hook=unique_object,
                          parse_constant=reject_constant, parse_float=finite_float)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise HarnessError(f"{label}: invalid JSON ({type(exc).__name__}: {exc})") from exc


def within(path, base):
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def safe_rel(value, label):
    if type(value) is not str or not value or "\x00" in value:
        raise HarnessError(label + " must be a nonempty relative path")
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in ("", ".", "..") for part in pure.parts):
        raise HarnessError(label + " contains an unsafe path component")
    return Path(*pure.parts)


def safe_within(path, base, label):
    try:
        resolved = path.resolve(strict=False)
        base_resolved = base.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise HarnessError(label + " cannot be resolved safely") from exc
    if not within(resolved, base_resolved):
        raise HarnessError(label + " escapes the fixture tree")
    return resolved


def read_regular(path, limit, label):
    try:
        info = path.lstat()
    except OSError as exc:
        raise HarnessError(label + " unavailable: " + str(exc)) from exc
    if not stat.S_ISREG(info.st_mode):
        raise HarnessError(label + " is not a regular non-symlink file")
    if info.st_size > limit:
        raise HarnessError(label + f" exceeds {limit} bytes")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise HarnessError(label + " unreadable: " + str(exc)) from exc
    if len(raw) != info.st_size:
        raise HarnessError(label + " changed while being read")
    return raw


def inventory(root):
    entries = []

    def visit(directory):
        try:
            children = sorted(os.scandir(directory), key=lambda entry: entry.name)
        except OSError as exc:
            raise HarnessError("fixture inventory failed: " + str(exc)) from exc
        for child in children:
            path = Path(child.path)
            rel = path.relative_to(root).as_posix()
            if directory == root and rel in ("expected.json", "expected.sha256"):
                continue
            if child.is_symlink():
                target = os.readlink(path)
                safe_within(path, root, "fixture symlink " + rel)
                entries.append({"path": rel, "kind": "symlink", "target": target})
            elif child.is_dir(follow_symlinks=False):
                entries.append({"path": rel, "kind": "directory"})
                visit(path)
            elif child.is_file(follow_symlinks=False):
                raw = read_regular(path, MAX_FILE_BYTES, rel)
                entries.append({"path": rel, "kind": "file", "sha256": sha(raw),
                                "size_bytes": len(raw)})
            else:
                raise HarnessError("unsupported fixture filesystem entry: " + rel)

    visit(root)
    return sorted(entries, key=lambda entry: entry["path"])


def validate_entries(entries):
    if not isinstance(entries, list):
        raise HarnessError("expected.input_entries must be a list")
    seen = set()
    last = None
    for row in entries:
        if not isinstance(row, dict):
            raise HarnessError("input_entries row is not an object")
        rel = row.get("path")
        safe_rel(rel, "input_entries.path")
        if rel in seen or (last is not None and rel <= last):
            raise HarnessError("input_entries must have unique sorted paths")
        seen.add(rel)
        last = rel
        kind = row.get("kind")
        if kind == "file":
            if (type(row.get("sha256")) is not str
                    or len(row["sha256"]) != 64
                    or any(c not in "0123456789abcdef" for c in row["sha256"])
                    or type(row.get("size_bytes")) is not int or row["size_bytes"] < 0):
                raise HarnessError("invalid pinned file entry: " + rel)
        elif kind == "directory":
            if set(row) != {"path", "kind"}:
                raise HarnessError("invalid pinned directory entry: " + rel)
        elif kind == "symlink":
            if set(row) != {"path", "kind", "target"} or type(row.get("target")) is not str:
                raise HarnessError("invalid pinned symlink entry: " + rel)
        else:
            raise HarnessError("unknown pinned entry kind: " + str(kind))
    return seen


def read_bundle_and_root(fixtures, case, entries):
    case_id = case.get("id")
    if type(case_id) is not str or not case_id or "/" in case_id or "\\" in case_id:
        raise HarnessError("case id is not a safe identifier")
    bundle_rel = safe_rel(case.get("bundle"), "case.bundle")
    root_rel = safe_rel(case.get("root"), "case.root")
    case_dir_rel = Path("cases") / case_id
    if not within(bundle_rel, case_dir_rel) or not within(root_rel, case_dir_rel):
        raise HarnessError("case bundle/root must stay in their cases/<id> directory")
    bundle_entry = next((row for row in case["_entries"] if row["path"] == bundle_rel.as_posix()), None)
    root_entry = next((row for row in case["_entries"] if row["path"] == root_rel.as_posix()), None)
    if bundle_entry is None or bundle_entry.get("kind") != "file":
        raise HarnessError("case bundle is not a pinned regular file: " + case_id)
    if root_entry is None or root_entry.get("kind") not in ("directory", "symlink"):
        raise HarnessError("case root is not a pinned directory: " + case_id)

    bundle_path = fixtures / bundle_rel
    bundle_raw = read_regular(bundle_path, MAX_FILE_BYTES, case_id + " bundle")
    if sha(bundle_raw) != case.get("bundle_sha256"):
        raise Tampered("bundle digest mismatch: " + case_id)
    root_path = fixtures / root_rel
    safe_within(root_path, fixtures, case_id + " root")
    if not root_path.is_dir():
        raise HarnessError("case root is not a directory: " + case_id)

    snapshot_sha = case.get("snapshot_sha256")
    snapshot_files = case.get("snapshot_files")
    if (type(snapshot_sha) is not str or len(snapshot_sha) != 64
            or any(c not in "0123456789abcdef" for c in snapshot_sha)
            or not isinstance(snapshot_files, list) or not snapshot_files):
        raise HarnessError("case snapshot digest/files are invalid: " + case_id)
    case_dir = fixtures / case_dir_rel
    for value in snapshot_files:
        rel = safe_rel(value, "case.snapshot_files[]")
        if not within(rel, case_dir_rel):
            raise HarnessError("case snapshot file escapes its fixture directory: " + case_id)
        target = safe_within(fixtures / rel, case_dir, case_id + " snapshot")
        if not target.is_file():
            raise HarnessError("case snapshot file is unavailable: " + case_id)
        raw = read_regular(target, MAX_FILE_BYTES, case_id + " snapshot")
        if sha(raw) != snapshot_sha:
            raise Tampered("snapshot bytes differ from the pinned digest: " + case_id)
    return bundle_path, root_path, bundle_raw


def load_expected(fixtures):
    expected_path = fixtures / "expected.json"
    sidecar_path = fixtures / "expected.sha256"
    expected_raw = read_regular(expected_path, MAX_EXPECTED_BYTES, "expected.json")
    sidecar_raw = read_regular(sidecar_path, 256, "expected.sha256")
    try:
        sidecar = sidecar_raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise Tampered("expected.sha256 is not ASCII") from exc
    if len(sidecar) != 64 + len("  expected.json\n") or sidecar[64:] != "  expected.json\n":
        raise Tampered("expected.sha256 has invalid format")
    expected_sha = sidecar[:64]
    if any(c not in "0123456789abcdef" for c in expected_sha):
        raise Tampered("expected.sha256 is not lowercase SHA-256")
    if sha(expected_raw) != expected_sha:
        raise Tampered("expected.json digest mismatch")
    expected = parse_json(expected_raw, "expected.json")
    if not isinstance(expected, dict) or expected.get("schema") != SCHEMA:
        raise HarnessError("unsupported expected.json schema")
    return expected_raw, expected_sha, expected


def verify_fixture(fixtures, expected_raw, expected_sha, expected):
    current_raw = read_regular(fixtures / "expected.json", MAX_EXPECTED_BYTES, "expected.json")
    if current_raw != expected_raw or sha(current_raw) != expected_sha:
        raise Tampered("expected.json changed during measurement")
    sidecar = read_regular(fixtures / "expected.sha256", 256, "expected.sha256")
    if sidecar != (expected_sha + "  expected.json\n").encode("ascii"):
        raise Tampered("expected.sha256 changed during measurement")
    expected_entries = expected.get("input_entries")
    validate_entries(expected_entries)
    actual_entries = inventory(fixtures)
    if actual_entries != expected_entries:
        raise Tampered("fixture inventory differs from expected.json")



def validate_sealed_metadata(fixtures, expected):
    raw_info = expected.get("raw_truth_seal")
    if not isinstance(raw_info, dict) or raw_info.get("path") != "inputs/truth-seal.json":
        raise HarnessError("expected.json has no raw truth seal input")
    seal_path = fixtures / safe_rel(raw_info["path"], "raw_truth_seal.path")
    seal_raw = read_regular(seal_path, MAX_FILE_BYTES, "raw truth seal")
    if sha(seal_raw) != raw_info.get("sha256"):
        raise Tampered("raw truth seal copy digest mismatch")
    seal = parse_json(seal_raw, "raw truth seal")
    if (not isinstance(seal, dict) or seal.get("schema") != raw_info.get("schema")
            or seal.get("base_commit") != raw_info.get("base_commit")
            or seal.get("created_at") != raw_info.get("created_at")):
        raise Tampered("raw truth seal metadata differs from expected.json")
    rows = seal.get("files")
    if not isinstance(rows, list) or len(rows) != 106:
        raise Tampered("raw truth seal file inventory is incomplete")
    normalized = []
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or type(row.get("path")) is not str:
            raise Tampered("raw truth seal contains an invalid file row")
        rel = safe_rel(row["path"], "raw truth seal file path").as_posix()
        digest, size = row.get("sha256"), row.get("bytes")
        if (type(digest) is not str or len(digest) != 64
                or any(c not in "0123456789abcdef" for c in digest)
                or type(size) is not int or size < 0 or rel in seen):
            raise Tampered("raw truth seal contains duplicate or invalid file pins")
        seen.add(rel)
        normalized.append({"path": rel, "sha256": digest, "bytes": size})
    if normalized != expected.get("truth_seal_files"):
        raise Tampered("expected.json truth seal file pins differ from raw truth seal")
    audit_count = sum(row["path"].startswith(".ufo/waves/round-22/w1/audit-proposals/")
                      for row in normalized)
    if (raw_info.get("file_count") != 106 or raw_info.get("verified_file_count") != 106
            or raw_info.get("audit_proposal_count") != audit_count or audit_count != 35):
        raise Tampered("expected.json raw truth seal counts are inconsistent")

    contract_info = expected.get("contract")
    if not isinstance(contract_info, dict) or contract_info.get("path") != "inputs/audit-contract.json":
        raise HarnessError("expected.json has no pinned audit contract")
    contract_raw = read_regular(fixtures / safe_rel(contract_info["path"], "contract.path"),
                                MAX_FILE_BYTES, "audit contract")
    if sha(contract_raw) != contract_info.get("sha256"):
        raise Tampered("audit contract digest mismatch")
    contract = parse_json(contract_raw, "audit contract")
    ids = contract.get("finding_ids") if isinstance(contract, dict) else None
    authority = contract.get("authority") if isinstance(contract, dict) else None
    if not isinstance(ids, list) or any(type(item) is not str for item in ids):
        raise HarnessError("audit contract finding_ids inventory is invalid")
    if type(authority) is not str or not authority.strip():
        raise HarnessError("audit contract authority is invalid")
    return set(ids), {row["path"] for row in normalized if
                      row["path"].startswith(".ufo/waves/round-22/w1/audit-proposals/")}, authority

def validate_cases(fixtures, expected, known_ids):
    cases = expected.get("cases")
    if not isinstance(cases, list) or not cases:
        raise HarnessError("expected.json has no cases")
    ids = set()
    entry_map = {row["path"]: row for row in expected["input_entries"]}
    checked = []
    for case in cases:
        if not isinstance(case, dict):
            raise HarnessError("case is not an object")
        case_id = case.get("id")
        if type(case_id) is not str or not case_id or case_id in ids:
            raise HarnessError("case IDs must be nonempty and unique")
        ids.add(case_id)
        wanted = case.get("expected")
        if (not isinstance(wanted, dict) or type(wanted.get("code")) is not int
                or wanted["code"] not in (0, 1, 2)
                or not isinstance(wanted.get("finding_ids"), list)
                or any(type(item) is not str for item in wanted["finding_ids"])):
            raise HarnessError("case expected code/finding_ids are invalid: " + case_id)
        if wanted["finding_ids"] != sorted(set(wanted["finding_ids"])):
            raise HarnessError("case expected finding_ids are not sorted unique: " + case_id)
        if set(wanted["finding_ids"]) - known_ids:
            raise HarnessError("case expected an unknown finding id: " + case_id)
        temp = dict(case)
        temp["_entries"] = list(entry_map.values())
        bundle, root, bundle_raw = read_bundle_and_root(fixtures, temp, entry_map)
        checked.append((case, bundle, root, bundle_raw))
    return checked


def child_limits():
    resource.setrlimit(resource.RLIMIT_AS, (CAP_BYTES, CAP_BYTES))
    resource.setrlimit(resource.RLIMIT_CPU, (TIMEOUT_SECONDS, TIMEOUT_SECONDS))
    resource.setrlimit(resource.RLIMIT_FSIZE, (OUTPUT_CAP, OUTPUT_CAP))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))


def output_payload(raw):
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return None, "stdout is not UTF-8: " + str(exc)
    try:
        value = parse_json(text.encode("utf-8"), "audit stdout")
    except HarnessError:
        value = None
    if isinstance(value, dict) and "finding_ids" in value:
        ids = value.get("finding_ids")
        if isinstance(ids, list) and all(type(item) is str for item in ids):
            return value, None
        return None, "finding_ids is not a list of strings"

    lines = text.splitlines()
    for start, line in enumerate(lines):
        if not line.lstrip().startswith("{"):
            continue
        try:
            value = parse_json(("\n".join(lines[start:]) + "\n").encode("utf-8"),
                               "audit stdout JSON block")
        except HarnessError:
            continue
        if isinstance(value, dict) and "finding_ids" in value:
            ids = value.get("finding_ids")
            if isinstance(ids, list) and all(type(item) is str for item in ids):
                return value, None
            return None, "finding_ids is not a list of strings"
    for line in reversed(lines):
        try:
            value = parse_json(line.encode("utf-8"), "audit stdout JSON line")
        except HarnessError:
            continue
        if isinstance(value, dict) and "finding_ids" in value:
            ids = value.get("finding_ids")
            if isinstance(ids, list) and all(type(item) is str for item in ids):
                return value, None
            return None, "finding_ids is not a list of strings"
    return None, "stdout must contain one JSON result with finding_ids"


def terminate_group(process):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except OSError:
        pass
    if process.poll() is None:
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def run_child(tool, case, bundle, root, expected_authority):
    command = [sys.executable, "-I", str(tool), "--check", str(bundle), "--root", str(root)]
    env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    started = time.monotonic()
    timed_out = False
    spawn_error = None
    returncode = None
    with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
        try:
            process = subprocess.Popen(command, cwd=root.parent, env=env,
                                       stdin=subprocess.DEVNULL, stdout=stdout_file,
                                       stderr=stderr_file, close_fds=True,
                                       start_new_session=True, preexec_fn=child_limits)
        except (OSError, subprocess.SubprocessError, ValueError) as exc:
            spawn_error = str(exc)
        else:
            try:
                returncode = process.wait(timeout=TIMEOUT_SECONDS)
            except subprocess.TimeoutExpired:
                timed_out = True
                terminate_group(process)
                returncode = process.returncode
            finally:
                terminate_group(process)
        stdout_file.flush()
        stderr_file.flush()
        stdout_size = os.fstat(stdout_file.fileno()).st_size
        stderr_size = os.fstat(stderr_file.fileno()).st_size
        stdout_file.seek(0)
        stderr_file.seek(0)
        stdout_raw = stdout_file.read(OUTPUT_CAP + 1)
        stderr_raw = stderr_file.read(OUTPUT_CAP + 1)
    elapsed_ms = round((time.monotonic() - started) * 1000)
    truncated = stdout_size >= OUTPUT_CAP or stderr_size >= OUTPUT_CAP
    payload, parse_error = output_payload(stdout_raw) if not spawn_error else (None, None)
    actual_ids = payload.get("finding_ids") if payload is not None else None
    payload_code = payload.get("code") if payload is not None else None
    payload_result = payload.get("result") if payload is not None else None
    payload_authority = payload.get("authority") if payload is not None else None
    wanted = case["expected"]
    ids_match = actual_ids == wanted["finding_ids"]
    code_match = returncode == wanted["code"]
    payload_code_match = type(payload_code) is int and payload_code == returncode
    payload_shape_match = (type(payload_result) is str and bool(payload_result.strip())
                           and type(payload_authority) is str and bool(payload_authority.strip()))
    authority_match = payload_authority == expected_authority
    evaluable = (not spawn_error and not timed_out and not truncated and parse_error is None
                 and payload is not None and returncode in (0, 1, 2)
                 and payload_code_match and payload_shape_match)
    passed = evaluable and code_match and ids_match and authority_match
    return {
        "command": command,
        "exit": returncode,
        "expected_code": wanted["code"],
        "actual_finding_ids": actual_ids,
        "expected_finding_ids": wanted["finding_ids"],
        "finding_ids_match": ids_match,
        "payload_code": payload_code,
        "payload_code_match": payload_code_match,
        "payload_result": payload_result,
        "payload_authority": payload_authority,
        "authority_match": authority_match,
        "evaluable": evaluable,
        "timeout": timed_out,
        "spawn_error": spawn_error,
        "parse_error": parse_error,
        "output_truncated": truncated,
        "duration_ms": elapsed_ms,
        "stdout_bytes": stdout_size,
        "stdout_sha256": sha(stdout_raw),
        "stdout_base64": base64.b64encode(stdout_raw).decode("ascii"),
        "stdout_text": stdout_raw.decode("utf-8", errors="replace"),
        "stderr_bytes": stderr_size,
        "stderr_sha256": sha(stderr_raw),
        "stderr_base64": base64.b64encode(stderr_raw).decode("ascii"),
        "stderr_text": stderr_raw.decode("utf-8", errors="replace"),
        "bundle_sha256": case["bundle_sha256"],
        "snapshot_sha256": case["snapshot_sha256"],
        "pass": passed,
    }



def run_selftest(tool, fixtures):
    command = [sys.executable, "-I", str(tool), "--selftest", str(fixtures)]
    env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    started = time.monotonic()
    timed_out = False
    spawn_error = None
    returncode = None
    with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
        try:
            process = subprocess.Popen(command, cwd=fixtures, env=env,
                                       stdin=subprocess.DEVNULL, stdout=stdout_file,
                                       stderr=stderr_file, close_fds=True,
                                       start_new_session=True, preexec_fn=child_limits)
        except (OSError, subprocess.SubprocessError, ValueError) as exc:
            spawn_error = str(exc)
        else:
            try:
                returncode = process.wait(timeout=TIMEOUT_SECONDS)
            except subprocess.TimeoutExpired:
                timed_out = True
                terminate_group(process)
                returncode = process.returncode
            finally:
                terminate_group(process)
        stdout_file.flush()
        stderr_file.flush()
        stdout_size = os.fstat(stdout_file.fileno()).st_size
        stderr_size = os.fstat(stderr_file.fileno()).st_size
        stdout_file.seek(0)
        stderr_file.seek(0)
        stdout_raw = stdout_file.read(OUTPUT_CAP + 1)
        stderr_raw = stderr_file.read(OUTPUT_CAP + 1)
    truncated = stdout_size >= OUTPUT_CAP or stderr_size >= OUTPUT_CAP
    return {
        "command": command,
        "exit": returncode,
        "evaluable": (not spawn_error and not timed_out and not truncated
                      and returncode in (0, 1)),
        "timeout": timed_out,
        "spawn_error": spawn_error,
        "output_truncated": truncated,
        "duration_ms": round((time.monotonic() - started) * 1000),
        "stdout_bytes": stdout_size,
        "stdout_sha256": sha(stdout_raw),
        "stdout_base64": base64.b64encode(stdout_raw).decode("ascii"),
        "stdout_text": stdout_raw.decode("utf-8", errors="replace"),
        "stderr_bytes": stderr_size,
        "stderr_sha256": sha(stderr_raw),
        "stderr_base64": base64.b64encode(stderr_raw).decode("ascii"),
        "stderr_text": stderr_raw.decode("utf-8", errors="replace"),
        "pass": (not spawn_error and not timed_out and not truncated and returncode == 0),
    }

def run(args):
    fixture_arg = Path(args.fixtures)
    try:
        fixture_info = fixture_arg.lstat()
    except OSError as exc:
        raise HarnessError("fixture root unavailable: " + str(exc)) from exc
    if not stat.S_ISDIR(fixture_info.st_mode):
        raise HarnessError("fixture root must be a real directory, not a symlink")
    fixtures = fixture_arg.resolve(strict=True)
    expected_raw, expected_sha, expected = load_expected(fixtures)
    verify_fixture(fixtures, expected_raw, expected_sha, expected)
    if expected.get("limits") != {
            "seconds_per_child": TIMEOUT_SECONDS,
            "address_space_bytes": CAP_BYTES,
            "output_bytes_per_stream": OUTPUT_CAP,
            "concurrency": 1,
    }:
        raise Tampered("expected.json resource limits differ from runner enforcement")
    if expected.get("schema") != SCHEMA:
        raise HarnessError("unsupported expected.json schema")
    known_ids, sealed_proposals, authority = validate_sealed_metadata(fixtures, expected)
    represented = {
        row.get("proposal") for row in expected.get("cases", [])
        if isinstance(row, dict) and type(row.get("proposal")) is str
        and row["proposal"].startswith(".ufo/waves/round-22/w1/audit-proposals/")
    }
    represented.update(
        row.get("proposal") for row in expected.get("excluded", [])
        if isinstance(row, dict) and type(row.get("proposal")) is str
        and row["proposal"].startswith(".ufo/waves/round-22/w1/audit-proposals/")
    )
    if represented != sealed_proposals:
        raise Tampered("expected.json does not account for every raw-sealed C2 proposal")

    proposal_case_paths = [row["proposal"] for row in expected.get("cases", [])
                           if isinstance(row, dict) and row.get("proposal") in sealed_proposals]
    proposal_excluded_paths = [row["proposal"] for row in expected.get("excluded", [])
                               if isinstance(row, dict) and row.get("proposal") in sealed_proposals]
    if ((set(proposal_case_paths) | set(proposal_excluded_paths)) != sealed_proposals
            or len(proposal_case_paths) + len(proposal_excluded_paths) != len(sealed_proposals)):
        raise Tampered("raw-sealed C2 proposals are missing, duplicated, or misrouted")

    limit_cases = [row for row in expected.get("cases", [])
                   if isinstance(row, dict) and row.get("id") == "AuditRawSnapshotAtLimit"]
    eligibility = [row for row in expected.get("eligibility_log", [])
                   if isinstance(row, dict) and row.get("id") == "AuditRawSnapshotAtLimit"]
    if (len(limit_cases) != 1 or len(eligibility) != 1
            or type(eligibility[0].get("original")) is not str
            or not eligibility[0]["original"].startswith("contingent:")
            or eligibility[0].get("decision") != "include"
            or "inclusive" not in eligibility[0].get("ruling", "")
            or "2097152" not in eligibility[0].get("ruling", "")):
        raise Tampered("inclusive 2 MiB contingent fixture/ruling was not preserved")
    limit = limit_cases[0]
    if limit.get("expected") != {"code": 0, "finding_ids": ["evidence_audit_clean"]}:
        raise Tampered("AuditRawSnapshotAtLimit expected verdict changed")
    limit_files = limit.get("snapshot_files")
    if not isinstance(limit_files, list) or len(limit_files) != 1:
        raise Tampered("AuditRawSnapshotAtLimit snapshot input is missing")
    limit_path = fixtures / safe_rel(limit_files[0], "limit snapshot file")
    limit_real = safe_within(limit_path, fixtures / "cases" / "AuditRawSnapshotAtLimit",
                             "AuditRawSnapshotAtLimit snapshot")
    if len(read_regular(limit_real, MAX_FILE_BYTES, "2 MiB snapshot")) != 2097152:
        raise Tampered("AuditRawSnapshotAtLimit is not exactly 2097152 bytes")

    historical_path = ".ufo/waves/round-22/w1/historical-c3.json"
    historical_cases = [row for row in expected.get("cases", [])
                        if isinstance(row, dict) and row.get("proposal") == historical_path]
    historical_excluded = [row for row in expected.get("excluded", [])
                           if isinstance(row, dict) and row.get("proposal") == historical_path]
    if expected.get("historical_c3_included") is True:
        primary = next((row for row in historical_cases
                        if row.get("id") == "HistoricalC3.r19-c3-derived-six-row-5obs-1lead"), None)
        provenance = primary.get("provenance") if isinstance(primary, dict) else None
        claim_kind = primary.get("claim_kind") if isinstance(primary, dict) else None
        original_claim = provenance.get("r19_original_claim") if isinstance(provenance, dict) else None
        if (primary is None or historical_excluded
                or primary.get("kind") != "historical-derived"
                or primary.get("claim") != {"total": 6, "observed": 5, "lead": 1,
                                            "errors": 0, "clean": False}
                or primary.get("expected") != {"code": 0, "finding_ids": ["evidence_audit_clean"]}
                or type(claim_kind) is not str
                or "not original r19 output or claim" not in claim_kind
                or type(original_claim) is not str
                or "detected 6/6" not in original_claim
                or "no evidence split" not in original_claim):
            raise Tampered("historical C3 derived 5/1 receipt/attribution is incomplete")
    elif historical_cases or len(historical_excluded) != 1:
        raise Tampered("historical C3 is neither included with provenance nor visibly excluded")

    tool_arg = Path(args.tool)
    try:
        tool = tool_arg.resolve(strict=True)
    except OSError as exc:
        raise HarnessError("tool unavailable: " + str(exc)) from exc
    if not tool.is_file() or tool.is_symlink():
        raise HarnessError("tool must resolve to a regular file")
    tool_sha = sha(read_regular(tool, MAX_FILE_BYTES, "selected tool"))
    runner = Path(__file__).resolve()
    runner_sha = sha(read_regular(runner, MAX_FILE_BYTES, "measure.py"))
    checked_cases = validate_cases(fixtures, expected, known_ids)

    result = {
        "schema": "mado-r22-audit-measure-v1",
        "status": "measured",
        "tool": str(tool),
        "tool_sha256": tool_sha,
        "runner_sha256": runner_sha,
        "expected_sha256": expected_sha,
        "truth_seal_sha256": expected["raw_truth_seal"]["sha256"],
        "authority": authority,
        "limits": expected["limits"],
        "cases": [],
        "selftest": None,
        "tampering": [],
    }
    for case, bundle, root, _bundle_raw in checked_cases:
        verify_fixture(fixtures, expected_raw, expected_sha, expected)
        if sha(read_regular(tool, MAX_FILE_BYTES, "selected tool")) != tool_sha:
            raise Tampered("selected tool changed before child execution")
        if sha(read_regular(runner, MAX_FILE_BYTES, "measure.py")) != runner_sha:
            raise Tampered("runner changed before child execution")
        result["cases"].append(run_child(tool, case, bundle, root, authority))
        if not result["cases"][-1]["evaluable"]:
            result["status"] = "could-not-evaluate"
            result["reason"] = "child did not produce a bounded comparable code/finding_ids result"
            return result, 2
        try:
            verify_fixture(fixtures, expected_raw, expected_sha, expected)
            after_tool_sha = sha(read_regular(tool, MAX_FILE_BYTES, "selected tool"))
            after_runner_sha = sha(read_regular(runner, MAX_FILE_BYTES, "measure.py"))
        except HarnessError as exc:
            result["tampering"].append(str(exc))
            result["status"] = "snapshot_tampered"
            return result, 2
        if after_tool_sha != tool_sha:
            result["tampering"].append("selected tool changed during child execution")
        if after_runner_sha != runner_sha:
            result["tampering"].append("runner changed during child execution")
        if result["tampering"]:
            result["status"] = "snapshot_tampered"
            return result, 2

    verify_fixture(fixtures, expected_raw, expected_sha, expected)
    if sha(read_regular(tool, MAX_FILE_BYTES, "selected tool")) != tool_sha:
        raise Tampered("selected tool changed before --selftest")
    if sha(read_regular(runner, MAX_FILE_BYTES, "measure.py")) != runner_sha:
        raise Tampered("runner changed before --selftest")
    selftest = run_selftest(tool, fixtures)
    result["selftest"] = selftest
    try:
        verify_fixture(fixtures, expected_raw, expected_sha, expected)
        after_tool_sha = sha(read_regular(tool, MAX_FILE_BYTES, "selected tool"))
        after_runner_sha = sha(read_regular(runner, MAX_FILE_BYTES, "measure.py"))
    except HarnessError as exc:
        result["tampering"].append(str(exc))
        result["status"] = "snapshot_tampered"
        return result, 2
    if after_tool_sha != tool_sha:
        result["tampering"].append("selected tool changed during --selftest")
    if after_runner_sha != runner_sha:
        result["tampering"].append("runner changed during --selftest")
    if result["tampering"]:
        result["status"] = "snapshot_tampered"
        return result, 2
    if not selftest["evaluable"]:
        result["status"] = "could-not-evaluate"
        result["reason"] = "bounded --selftest child did not produce a comparable exit status"
        return result, 2

    case_passed = all(row["pass"] for row in result["cases"])
    passed = case_passed and selftest["pass"]
    result["status"] = "complete" if passed else "failed"
    result["totals"] = {"passed": sum(row["pass"] for row in result["cases"]),
                         "total": len(result["cases"])}
    return result, (0 if passed else 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, type=Path)
    parser.add_argument("--fixtures", required=True, type=Path)
    args = parser.parse_args()
    try:
        result, code = run(args)
    except Tampered as exc:
        result, code = {"schema": "mado-r22-audit-measure-v1",
                        "status": "snapshot_tampered", "reason": str(exc),
                        "cases": [], "tampering": [str(exc)]}, 2
    except (HarnessError, OSError, ValueError) as exc:
        result, code = {"schema": "mado-r22-audit-measure-v1",
                        "status": "could-not-evaluate", "reason": str(exc),
                        "cases": [], "tampering": []}, 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
