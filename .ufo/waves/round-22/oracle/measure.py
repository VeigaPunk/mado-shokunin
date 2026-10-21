#!/usr/bin/env python3
"""Compare one selected scanner with the pinned, pre-implementation C1 truth set."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "inputs"
EXPECTED_PATH = ROOT / "expected.json"
PIN_PATH = ROOT / "expected.sha256"
ASSEMBLER_PATH = ROOT / "assemble.py"
TRUTH_SEAL_REL = ".ufo/waves/round-22/truth-seal.json"
TRUTH_SEAL_SHA256 = "47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4"
SCHEMA = "mado-r22-c1-oracle-v1"
RAW_SEAL_SCHEMA = "mado-r22-independent-truth-seal-v1"
CAP = 384 * 1024 * 1024
TIMEOUT_SECONDS = 15
RAW_PROPOSAL_COUNT = 52
ELIGIBLE_PROPOSAL_COUNT = 50
SUPPLEMENTAL_ORIGINAL_COUNT = 7
REQUIRED_PROPOSALS = {"TimerRunAliasActual", "CapturePartialGlobalLateActual", "CaptureNestedFactory"}
ROW_KEYS = {"class", "command", "evidence"}

WRAPPER = '''import importlib.util,sys
s=importlib.util.spec_from_file_location("selected_tripwire",sys.argv[1])
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
sys.exit(m.main(["--scan",sys.argv[2]]))
'''

ORIGINALS = {
    "OriginalF1CaptureInvokeTime": {
        "source": ".ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/capture-invoke-time.jsonl",
        "sha256": "6b21d584710878f5e486f3e9fcd737c6a6e573c629c2f75d30b45f55b6a317f7",
        "kind": "exact", "want": [{"class": "host_mutation", "command": "pacman -S r21-factory", "evidence": "observed"}],
        "forbid_observed": [], "forbid_any": [], "signal": True, "table": "F1",
    },
    "OriginalF2CaptureUnboundGlobal": {
        "source": ".ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/capture-unbound-global.jsonl",
        "sha256": "9ab845d4a8886714cfea0b16203328b67335013f00b21b18ba23e9b7175e1d9d",
        "kind": "uncertain", "want": [], "forbid_observed": ["pacman -Q r21-global"],
        "forbid_any": ["pacman -Q r21-global"], "signal": True, "table": "F2",
    },
    "OriginalF3ReturnedRebound": {
        "source": ".ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/returned-rebound.jsonl",
        "sha256": "774e2946d16c23d9ebdd557ccf279143f6d2249dc7132aa567fb34d12d3d7573",
        "kind": "exact", "want": [{"class": "host_mutation", "command": "pacman -S r21-b", "evidence": "observed"}],
        "forbid_observed": [], "forbid_any": [], "signal": True, "table": "F3",
    },
    "OriginalF4ThreadRunDirect": {
        "source": ".ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/thread-run-direct.jsonl",
        "sha256": "1cc1188dc4e0c37ecba97d34bdf546113d888c62a9cba0bcfe06d44201a2407f",
        "kind": "exact", "want": [{"class": "host_mutation", "command": "pacman -S r21-thread-run", "evidence": "observed"}],
        "forbid_observed": [], "forbid_any": [], "signal": True, "table": "F4",
    },
    "OriginalF5ThreadKeyHygiene": {
        "source": ".ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/thread-key-hygiene.jsonl",
        "sha256": "4ea8ccc8724de011e19dcc1e69da1f4078ac74544f554e39ccda66dc42065c9e",
        "kind": "exact", "want": [{"class": "package_query", "command": "pacman -Q r21-hyg", "evidence": "observed"}],
        "forbid_observed": [], "forbid_any": [], "signal": True, "table": "F5",
    },
    "OriginalF5ThreadKeyControl": {
        "source": ".ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/thread-key-control.jsonl",
        "sha256": "00ecb83fabddfd002d703bc1fbaa449b24e1edf935d0f6792a773c96007162be",
        "kind": "exact", "want": [{"class": "package_query", "command": "pacman -Q r21-hyg", "evidence": "observed"}],
        "forbid_observed": [], "forbid_any": [], "signal": True, "table": "control",
    },
    "OriginalR19PureFrozenClosure": {
        "source": ".ufo/waves/round-20/precision/CasePureBuiltins--frozenset-closure.jsonl",
        "sha256": "14558b6dd1574253772b30af041169c6fb0eda992d47c7773c342c225472f040",
        "kind": "exact", "want": [], "forbid_observed": [], "forbid_any": [], "signal": False,
        "table": "round-20 precision / CasePureBuiltins--frozenset-closure",
    },
}


class Refusal(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_json(raw: bytes) -> Any:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r}")
            result[key] = value
        return result

    def no_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON value {value}")

    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique, parse_constant=no_constant)


def safe_regular(root: Path, relative: str) -> Path:
    rel = PurePosixPath(relative)
    if rel.is_absolute() or not rel.parts or any(part in ("", ".", "..") for part in rel.parts):
        raise Refusal(f"unsafe relative path {relative!r}")
    base = root.resolve(strict=True)
    current = base
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise Refusal(f"symlink in input path {relative!r}")
    try:
        resolved = current.resolve(strict=True)
    except OSError as error:
        raise Refusal(f"unavailable input {relative!r}: {error}") from error
    if not resolved.is_relative_to(base) or not resolved.is_file():
        raise Refusal(f"input is not a regular file inside its root: {relative!r}")
    return resolved


def read_local_regular(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise Refusal(f"required local artifact is missing, non-regular, or a symlink: {path}")
    return path.read_bytes()


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
    return digest(encoded)


def read_expected() -> tuple[dict[str, Any], bytes, bytes, str, str]:
    expected_raw = read_local_regular(EXPECTED_PATH)
    pin_raw = read_local_regular(PIN_PATH)
    try:
        pin_line = pin_raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise Refusal("expected.sha256 is not ASCII") from error
    actual_sha = digest(expected_raw)
    if pin_line != f"{actual_sha}  expected.json\n":
        raise Refusal("expected.json digest does not match the exact expected.sha256 pin")
    expected = strict_json(expected_raw)
    if not isinstance(expected, dict) or expected.get("schema") != SCHEMA:
        raise Refusal("unsupported expected.json schema")
    return expected, expected_raw, pin_raw, actual_sha, digest(pin_raw)


def check_truth_seal(expected: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    seal_path = safe_regular(LANE, TRUTH_SEAL_REL)
    seal_raw = seal_path.read_bytes()
    if digest(seal_raw) != TRUTH_SEAL_SHA256:
        raise Refusal("raw independent truth seal digest changed")
    seal = strict_json(seal_raw)
    if not isinstance(seal, dict) or seal.get("schema") != RAW_SEAL_SCHEMA:
        raise Refusal("raw independent truth seal schema mismatch")
    sealed = expected.get("truth_seal")
    if not isinstance(sealed, dict) or sealed.get("path") != TRUTH_SEAL_REL or sealed.get("sha256") != TRUTH_SEAL_SHA256:
        raise Refusal("expected.json is not bound to the sealed raw truth file")
    if (
        sealed.get("schema") != seal.get("schema")
        or sealed.get("created_at") != seal.get("created_at")
        or sealed.get("base_commit") != seal.get("base_commit")
        or sealed.get("baseline_tool_sha256") != seal.get("baseline_tool_sha256")
        or sealed.get("files") != seal.get("files")
        or sealed.get("premeasurement_decisions") != seal.get("premeasurement_decisions")
        or sealed.get("file_count") != len(seal.get("files", []))
    ):
        raise Refusal("expected.json raw seal metadata or source manifest differs from truth-seal.json")
    files = seal.get("files")
    if not isinstance(files, list) or len(files) != 106 or sealed.get("file_count") != 106:
        raise Refusal("the raw truth seal must retain all 106 source digests")
    verified = 0
    for entry in files:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "bytes"}:
            raise Refusal("invalid raw truth-seal file entry")
        rel, checksum, byte_count = entry["path"], entry["sha256"], entry["bytes"]
        if not isinstance(rel, str) or not isinstance(checksum, str) or len(checksum) != 64 or type(byte_count) is not int or byte_count < 0:
            raise Refusal("invalid raw truth-seal path, digest, or size")
        source = safe_regular(LANE, rel)
        raw = source.read_bytes()
        if len(raw) != byte_count or digest(raw) != checksum:
            raise Refusal(f"sealed source changed: {rel}")
        verified += 1
    if verified != 106:
        raise Refusal("incomplete raw source verification")
    return seal, {"path": TRUTH_SEAL_REL, "sha256": TRUTH_SEAL_SHA256, "files_verified": verified}


def current_proposal_inventory(expected_inventory: dict[str, Any]) -> tuple[int, set[str]]:
    rel = expected_inventory.get("path")
    if rel != ".ufo/waves/round-22/w1/proposals" or expected_inventory.get("kind") != "directory":
        raise Refusal("unexpected sealed proposal directory identity")
    directory = safe_directory(LANE, rel)
    current: list[dict[str, Any]] = []
    json_names: set[str] = set()
    for child in sorted(directory.iterdir(), key=lambda path: path.name):
        mode = child.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise Refusal(f"proposal entry became a symlink: {child.name}")
        if stat.S_ISREG(mode):
            raw = child.read_bytes()
            current.append({"name": child.name, "kind": "file", "sha256": digest(raw), "bytes": len(raw)})
            if child.name.endswith(".json"):
                json_names.add(child.name)
        elif stat.S_ISDIR(mode):
            current.append({"name": child.name, "kind": "directory"})
        else:
            current.append({"name": child.name, "kind": "other"})
    if current != expected_inventory.get("entries"):
        raise Refusal("proposal directory entries or source digests changed after sealing")
    return len(json_names), json_names


def safe_directory(root: Path, relative: str) -> Path:
    rel = PurePosixPath(relative)
    if rel.is_absolute() or any(part in ("", ".", "..") for part in rel.parts):
        raise Refusal(f"unsafe directory path {relative!r}")
    base = root.resolve(strict=True)
    current = base
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise Refusal(f"symlink in directory path {relative!r}")
    resolved = current.resolve(strict=True)
    if not resolved.is_relative_to(base) or not resolved.is_dir():
        raise Refusal(f"directory is not inside its root: {relative!r}")
    return resolved


def validate_case_fields(case: Any) -> tuple[str, list[dict[str, str]], list[dict[str, str]] | None, int]:
    if not isinstance(case, dict):
        raise Refusal("case record is not an object")
    case_id = case.get("id")
    if not isinstance(case_id, str) or not case_id:
        raise Refusal("case id is missing")
    if case.get("group") not in ("proposal", "supplemental-original"):
        raise Refusal(f"invalid group for {case_id}")
    kind = case.get("expected_kind")
    if kind not in ("exact", "uncertain"):
        raise Refusal(f"invalid expected_kind for {case_id}")
    for name in ("require_signal",):
        if type(case.get(name)) is not bool:
            raise Refusal(f"{name} must be an exact bool for {case_id}")
    for name in ("want", "want_input_order"):
        rows = case.get(name)
        if not isinstance(rows, list):
            raise Refusal(f"{name} must be a list for {case_id}")
        for row in rows:
            if not isinstance(row, dict) or set(row) != ROW_KEYS or not all(isinstance(row[k], str) and row[k] for k in ROW_KEYS):
                raise Refusal(f"invalid {name} row for {case_id}")
            if row["evidence"] not in ("observed", "lead"):
                raise Refusal(f"invalid evidence marker in {name} for {case_id}")
    want = case["want"]
    ordered = sorted(want, key=lambda row: (row["class"], row["command"], row["evidence"]))
    if want != ordered:
        raise Refusal(f"want rows are not in sealed class/command/evidence order for {case_id}")
    source_order = case.get("want_input_order")
    if not isinstance(source_order, list):
        raise Refusal(f"want_input_order is not a list for {case_id}")
    if case["group"] == "proposal":
        proposal = case.get("proposal")
        fields = proposal.get("fields") if isinstance(proposal, dict) else None
        if not isinstance(fields, dict) or fields.get("want") != source_order:
            raise Refusal(f"original proposal want rows were not retained for {case_id}")
    accept = case.get("accept_exact_want")
    if accept is not None:
        if kind != "uncertain" or not isinstance(accept, list) or not accept:
            raise Refusal(f"accept_exact_want must be a nonempty uncertain alternate for {case_id}")
        if any(not isinstance(row, dict) or set(row) != ROW_KEYS or row.get("evidence") not in ("observed", "lead") for row in accept):
            raise Refusal(f"invalid accept_exact_want row for {case_id}")
        if accept != sorted(accept, key=lambda row: (row["class"], row["command"], row["evidence"])):
            raise Refusal(f"accept_exact_want is not sorted for {case_id}")
    for field in ("forbid_observed_commands", "forbid_commands_any_tier"):
        commands = case.get(field)
        if not isinstance(commands, list) or any(not isinstance(item, str) or not item for item in commands):
            raise Refusal(f"invalid {field} for {case_id}")
    cell_count = case.get("cell_count")
    resets = case.get("cell_reset")
    if type(cell_count) is not int or cell_count < 1 or not isinstance(resets, list) or len(resets) != cell_count or any(type(flag) is not bool for flag in resets):
        raise Refusal(f"cell_reset must map one exact bool to each source cell for {case_id}")
    return kind, want, accept, cell_count

def validate_proposal_semantics(case: dict[str, Any]) -> None:
    proposal = case.get("proposal")
    if not isinstance(proposal, dict) or not isinstance(proposal.get("fields"), dict):
        raise Refusal(f"raw proposal fields are missing for {case['id']}")
    fields = proposal["fields"]
    allowed_base = {
        "id", "cells", "expected_kind", "want", "forbid_observed_commands", "rationale", "source",
        "language", "forbid_commands_any_tier", "require_signal", "accept_exact_want", "cell_reset",
    }
    if set(fields) - allowed_base or fields.get("id") != case["id"]:
        raise Refusal(f"proposal identity or extension fields changed for {case['id']}")
    cells = fields.get("cells")
    if not isinstance(cells, list) or not cells or any(not isinstance(cell, str) or not cell.strip() for cell in cells) or case.get("cell_count") != len(cells):
        raise Refusal(f"normalized cells differ from raw proposal for {case['id']}")
    if fields.get("language", "py") != "py":
        raise Refusal(f"proposal language metadata is unsupported for {case['id']}")
    resets = fields.get("cell_reset", [False] * len(cells))
    if not isinstance(resets, list) or len(resets) != len(cells) or any(type(flag) is not bool for flag in resets) or case.get("cell_reset") != resets:
        raise Refusal(f"normalized resets differ from raw proposal for {case['id']}")
    kind = fields.get("expected_kind")
    want = validate_rows(fields.get("want"), f"{case['id']}.want")
    if case.get("expected_kind") != kind or case.get("want_input_order") != want:
        raise Refusal(f"normalized expected kind or raw want differs for {case['id']}")
    if case.get("want") != sorted(want, key=lambda row: (row["class"], row["command"], row["evidence"])):
        raise Refusal(f"normalized want is not a sorted source-equivalent multiset for {case['id']}")
    base_accept = fields.get("accept_exact_want")
    normalized_accept = None
    if base_accept is not None:
        normalized_accept = sorted(validate_rows(base_accept, f"{case['id']}.accept_exact_want"), key=lambda row: (row["class"], row["command"], row["evidence"]))
        if kind != "uncertain" or not normalized_accept:
            raise Refusal(f"invalid accept_exact_want in raw proposal for {case['id']}")
    base_observed = fields.get("forbid_observed_commands")
    if not isinstance(base_observed, list) or any(not isinstance(value, str) or not value for value in base_observed):
        raise Refusal(f"invalid source forbid_observed_commands for {case['id']}")
    if case.get("forbid_observed_commands") != base_observed:
        raise Refusal(f"observed-command exclusions differ from the original proposal for {case['id']}")
    base_any = fields.get("forbid_commands_any_tier", [])
    if not isinstance(base_any, list) or any(not isinstance(value, str) or not value for value in base_any):
        raise Refusal(f"invalid source forbid_commands_any_tier for {case['id']}")
    expected_any = list(base_any)
    expected_signal = fields.get("require_signal", kind == "uncertain" or bool(want))
    if type(expected_signal) is not bool:
        raise Refusal(f"invalid source require_signal for {case['id']}")
    addenda = case.get("addenda")
    if not isinstance(addenda, list):
        raise Refusal(f"addenda is not a list for {case['id']}")
    addendum_required = {"id", "addendum_to", "rationale", "source"}
    addendum_allowed = addendum_required | {
        "cells", "expected_kind", "want", "forbid_observed_commands", "forbid_commands_any_tier",
        "require_signal", "accept_exact_want", "cell_reset", "language",
    }
    for addendum in addenda:
        added = addendum.get("fields") if isinstance(addendum, dict) else None
        add_path = addendum.get("path") if isinstance(addendum, dict) else None
        if (
            not isinstance(added, dict)
            or not isinstance(add_path, str)
            or not addendum_required <= set(added)
            or set(added) - addendum_allowed
            or added.get("id") != Path(add_path).stem
            or added.get("addendum_to") != case["id"]
            or any(not isinstance(added.get(name), str) or not added[name].strip() for name in ("rationale", "source"))
        ):
            raise Refusal(f"addendum fields, identity, or provenance are invalid for {case['id']}")
        comparisons = {
            "cells": cells, "expected_kind": kind, "forbid_observed_commands": base_observed,
            "language": fields.get("language", "py"),
        }
        for field, original in comparisons.items():
            if field in added and added[field] != original:
                raise Refusal(f"addendum changed base {field} for {case['id']}")
        if "want" in added and validate_rows(added["want"], f"{case['id']}.addendum.want") != want:
            raise Refusal(f"addendum changed base want for {case['id']}")
        if "cell_reset" in added:
            add_reset = added["cell_reset"]
            if not isinstance(add_reset, list) or len(add_reset) != len(resets) or any(type(flag) is not bool for flag in add_reset) or add_reset != resets:
                raise Refusal(f"addendum changed or malformed base cell_reset for {case['id']}")
        extra_forbidden = added.get("forbid_commands_any_tier", [])
        if not isinstance(extra_forbidden, list) or any(not isinstance(value, str) or not value for value in extra_forbidden):
            raise Refusal(f"invalid addendum any-tier exclusions for {case['id']}")
        if len(extra_forbidden) != len(set(extra_forbidden)):
            raise Refusal(f"duplicate addendum any-tier exclusion for {case['id']}")
        expected_any.extend(extra_forbidden)
        if "require_signal" in added and type(added["require_signal"]) is not bool:
            raise Refusal(f"invalid addendum require_signal for {case['id']}")
        extra_signal = added.get("require_signal")
        if extra_signal is False and expected_signal:
            raise Refusal(f"addendum weakens require_signal for {case['id']}")
        if extra_signal is True:
            expected_signal = True
        if added.get("accept_exact_want") is not None:
            added_accept = sorted(validate_rows(added["accept_exact_want"], f"{case['id']}.addendum.accept_exact_want"), key=lambda row: (row["class"], row["command"], row["evidence"]))
            if not added_accept or (normalized_accept is not None and normalized_accept != added_accept):
                raise Refusal(f"addendum accepted exact rows are empty or conflict for {case['id']}")
            normalized_accept = added_accept
    if case.get("accept_exact_want") != normalized_accept:
        raise Refusal(f"addendum accepted-exact rows were not applied for {case['id']}")
    if case.get("forbid_commands_any_tier") != expected_any or case.get("require_signal") is not expected_signal:
        raise Refusal(f"mandatory any-tier or signal constraints were not preserved for {case['id']}")
    forbidden = set(expected_any)
    if any(row["command"] in forbidden for row in [*want, *(normalized_accept or [])]):
        raise Refusal(f"any-tier ban conflicts with a wanted command for {case['id']}")
    if case.get("rationale") != fields.get("rationale") or case.get("source") != fields.get("source"):
        raise Refusal(f"rationale/source metadata was changed for {case['id']}")


def validate_rows(value: Any, label: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise Refusal(f"{label} is not a row list")
    rows = []
    for row in value:
        if not isinstance(row, dict) or set(row) != ROW_KEYS or any(not isinstance(row[key], str) or not row[key] for key in ROW_KEYS):
            raise Refusal(f"{label} contains an invalid row")
        if row["evidence"] not in ("observed", "lead"):
            raise Refusal(f"{label} contains an invalid evidence marker")
        rows.append({"class": row["class"], "command": row["command"], "evidence": row["evidence"]})
    return rows


def parse_input_fixture(case: dict[str, Any], fixture_path: Path) -> tuple[bytes, list[str]]:
    raw = read_local_regular(fixture_path)
    if not raw or not raw.endswith(b"\n") or digest(raw) != case.get("input_sha256"):
        raise Refusal(f"input digest/newline mismatch for {case.get('id')}")
    lines = raw.splitlines()
    kind, _, _, cell_count = validate_case_fields(case)
    del kind
    if len(lines) != cell_count:
        raise Refusal(f"input cell count mismatch for {case.get('id')}")
    call_ids = []
    for index, line in enumerate(lines):
        value = strict_json(line)
        if not isinstance(value, dict) or value.get("type") != "message" or not isinstance(value.get("message"), dict):
            raise Refusal(f"input line {index} is not an assistant message in {case.get('id')}")
        message = value["message"]
        if message.get("role") != "assistant" or not isinstance(message.get("content"), list) or len(message["content"]) != 1:
            raise Refusal(f"input line {index} is not one inert eval call in {case.get('id')}")
        call = message["content"][0]
        if not isinstance(call, dict) or call.get("type") != "toolCall" or call.get("name") != "eval":
            raise Refusal(f"input line {index} contains a non-eval call in {case.get('id')}")
        args = call.get("arguments")
        if not isinstance(args, dict) or set(args) - {"language", "code", "reset"} or args.get("language") != "py" or not isinstance(args.get("code"), str):
            raise Refusal(f"input line {index} has invalid eval arguments in {case.get('id')}")
        reset = args.get("reset", False)
        if type(reset) is not bool or reset is not case["cell_reset"][index]:
            raise Refusal(f"input line {index} reset does not match its sealed cell_reset for {case.get('id')}")
        if case["group"] == "proposal" and args["code"] != case["proposal"]["fields"]["cells"][index]:
            raise Refusal(f"input source cell was changed for {case['id']} at cell {index}")
        call_id = call.get("id")
        if not isinstance(call_id, str) or not call_id:
            raise Refusal(f"input line {index} has no call id in {case.get('id')}")
        if case["group"] == "proposal" and call_id != f"{case['id']}-{index}":
            raise Refusal(f"proposal call identity changed for {case['id']} at cell {index}")
        call_ids.append(call_id)
    return raw, call_ids


def verify_original_cases(expected: dict[str, Any], case_by_id: dict[str, dict[str, Any]]) -> None:
    if len(ORIGINALS) != SUPPLEMENTAL_ORIGINAL_COUNT:
        raise Refusal("internal original fixture table is incomplete")
    for case_id, truth in ORIGINALS.items():
        case = case_by_id.get(case_id)
        if case is None or case.get("group") != "supplemental-original":
            raise Refusal(f"missing immutable supplemental original {case_id}")
        if case.get("expected_kind") != truth["kind"] or case.get("want") != sorted(truth["want"], key=lambda row: (row["class"], row["command"], row["evidence"])):
            raise Refusal(f"sealed original truth changed for {case_id}")
        if case.get("forbid_observed_commands") != truth["forbid_observed"] or case.get("forbid_commands_any_tier") != truth["forbid_any"] or case.get("require_signal") is not truth["signal"]:
            raise Refusal(f"sealed original uncertainty constraints changed for {case_id}")
        source = case.get("source_provenance")
        if not isinstance(source, dict) or source.get("path") != truth["source"] or source.get("sha256") != truth["sha256"] or source.get("table_row") != truth["table"]:
            raise Refusal(f"original source provenance changed for {case_id}")
        fixture = case.get("fixture")
        if fixture != f"inputs/{case_id}.jsonl":
            raise Refusal(f"original fixture path changed for {case_id}")
        if case.get("input_sha256") != truth["sha256"]:
            raise Refusal(f"original input digest changed for {case_id}")


def verify_population(expected: dict[str, Any], expected_sha: str, pin_sha: str, tool_path: Path | None = None, expected_tool_sha: str | None = None) -> dict[str, Any]:
    current_expected, _, _, current_sha, current_pin_sha = read_expected()
    if current_sha != expected_sha or current_pin_sha != pin_sha or current_expected != expected:
        raise Refusal("expected manifest or pin changed during measurement")
    _, seal_facts = check_truth_seal(expected)
    producer_sha = digest(read_local_regular(ASSEMBLER_PATH))
    runner_sha = digest(read_local_regular(Path(__file__).resolve()))
    if producer_sha != expected.get("producer_sha256") or runner_sha != expected.get("runner_sha256"):
        raise Refusal("assembler or measurement runner differs from the materialized digest")
    if (
        expected.get("raw_proposal_count") != RAW_PROPOSAL_COUNT
        or expected.get("eligible_proposal_count") != ELIGIBLE_PROPOSAL_COUNT
        or expected.get("supplemental_original_count") != SUPPLEMENTAL_ORIGINAL_COUNT
    ):
        raise Refusal("sealed proposal/original population counts changed")
    inventory = expected.get("proposal_inventory")
    if not isinstance(inventory, dict):
        raise Refusal("proposal inventory is missing")
    actual_proposal_count, proposal_names = current_proposal_inventory(inventory)
    if actual_proposal_count != RAW_PROPOSAL_COUNT:
        raise Refusal("proposal directory is empty or no longer has the full sealed population")
    cases = expected.get("cases")
    if not isinstance(cases, list) or len(cases) != ELIGIBLE_PROPOSAL_COUNT + SUPPLEMENTAL_ORIGINAL_COUNT:
        raise Refusal("empty or incomplete scanner case population")

    case_by_id: dict[str, dict[str, Any]] = {}
    fixture_names: set[str] = set()
    for case in cases:
        validate_case_fields(case)
        case_id = case["id"]
        if case_id in case_by_id:
            raise Refusal(f"duplicate exact case id {case_id}")
        case_by_id[case_id] = case
        if case["group"] == "proposal":
            validate_proposal_semantics(case)
        fixture = case.get("fixture")
        if not isinstance(fixture, str) or not fixture.startswith("inputs/") or "/" in fixture[len("inputs/"):]:
            raise Refusal(f"invalid fixture path for {case_id}")
        if fixture in fixture_names:
            raise Refusal(f"duplicate fixture path {fixture}")
        fixture_names.add(fixture)
        fixture_path = safe_regular(ROOT, fixture)
        parse_input_fixture(case, fixture_path)
        if case["group"] == "proposal":
            proposal = case.get("proposal")
            if not isinstance(proposal, dict) or not isinstance(proposal.get("path"), str):
                raise Refusal(f"proposal provenance missing for {case_id}")
            if not proposal["path"].startswith(inventory["path"] + "/") or not proposal["path"].endswith(".json") or proposal["path"].rsplit("/", 1)[-1] not in proposal_names:
                raise Refusal(f"proposal source path is outside the sealed proposal inventory for {case_id}")
            source_raw = safe_regular(LANE, proposal["path"]).read_bytes()
            if digest(source_raw) != proposal.get("sha256") or strict_json(source_raw) != proposal.get("fields"):
                raise Refusal(f"proposal source changed or was not preserved for {case_id}")
            addenda = case.get("addenda")
            if not isinstance(addenda, list):
                raise Refusal(f"addenda is not a list for {case_id}")
            for addendum in addenda:
                if not isinstance(addendum, dict) or not isinstance(addendum.get("path"), str):
                    raise Refusal(f"invalid addendum record for {case_id}")
                if not addendum["path"].startswith(inventory["path"] + "/") or not addendum["path"].endswith(".addendum.json") or addendum["path"].rsplit("/", 1)[-1] not in proposal_names:
                    raise Refusal(f"addendum source path is outside the sealed proposal inventory for {case_id}")
                add_raw = safe_regular(LANE, addendum["path"]).read_bytes()
                if digest(add_raw) != addendum.get("sha256") or strict_json(add_raw) != addendum.get("fields"):
                    raise Refusal(f"addendum source changed or was not preserved for {case_id}")
                if addendum["fields"].get("addendum_to") != case_id:
                    raise Refusal(f"addendum_to provenance mismatch for {case_id}")
        elif case.get("proposal") is not None or case.get("addenda"):
            raise Refusal(f"supplemental original has proposal provenance: {case_id}")

    if fixture_names != {f"inputs/{case_id}.jsonl" for case_id in case_by_id}:
        raise Refusal("fixture population is not one-to-one with case ids")
    input_dir = safe_directory(ROOT, "inputs")
    direct = {f"inputs/{child.name}" for child in input_dir.iterdir()}
    if direct != fixture_names:
        raise Refusal("input directory contains missing or unregistered files")
    verify_original_cases(expected, case_by_id)

    proposal_case_ids = {case["id"] for case in cases if case["group"] == "proposal"}
    if len(proposal_case_ids) != ELIGIBLE_PROPOSAL_COUNT or not REQUIRED_PROPOSALS <= proposal_case_ids:
        raise Refusal("eligible proposal population is empty, incomplete, or missing a required case")
    required = expected.get("required_proposal_ids")
    if not isinstance(required, list) or any(not isinstance(value, str) for value in required) or set(required) != REQUIRED_PROPOSALS:
        raise Refusal("required proposal id set differs from pre-seal direction")
    required_records = expected.get("required_proposals")
    if (
        not isinstance(required_records, list)
        or len(required_records) != len(REQUIRED_PROPOSALS)
        or any(not isinstance(row, dict) or type(row.get("present")) is not bool for row in required_records)
        or {row["id"] for row in required_records} != REQUIRED_PROPOSALS
        or not all(row["present"] for row in required_records)
    ):
        raise Refusal("required proposal presence records differ from the sealed set")
    history = {
        "name": "round-21 legacy precision guard", "baseline_pass": 166, "population_total": 175,
        "required_floor": 166, "reset_to_new_target": False,
        "owner": "Main runs the whole-175 comparison at the delivered commit; this oracle does not run it",
        "sources": [
            {"path": ".ufo/waves/round-21/residual/FinalRemovalReview.md", "sha256": "c872a0d4f94ee2e007286cd1ec82b0eb368f63fe35922de9461fb462d4b2522a"},
            {"path": ".ufo/waves/round-21/final-summary.json", "sha256": "e03a2f5a27a1b918e88721b34da38ff872aa8513a70449f37b27119757d9f5d8"},
        ],
    }
    if expected.get("historical_guard") != history:
        raise Refusal("historical 166/175 guard was reset or changed")

    rejected = expected.get("rejected")
    if not isinstance(rejected, list):
        raise Refusal("rejection inventory missing")
    if len(rejected) != 1:
        raise Refusal("unexpected proposal exclusions; only the sealed nested-factory author typo may be rejected")
    accepted_names = {case["proposal"]["path"].rsplit("/", 1)[-1] for case in cases if case["group"] == "proposal"}
    addendum_names = {addendum["path"].rsplit("/", 1)[-1] for case in cases for addendum in case.get("addenda", [])}
    rejected_names = {
        item["path"].rsplit("/", 1)[-1] for item in rejected
        if isinstance(item, dict) and isinstance(item.get("path"), str)
        and item["path"].startswith(inventory["path"] + "/") and item["path"].endswith(".json")
    }
    if proposal_names != accepted_names | addendum_names | rejected_names:
        raise Refusal("one or more sealed proposal files are neither accepted, applied, nor explicitly rejected")
    typo = rejected[0]
    corrected = case_by_id.get("CaptureNestedFactory")
    correction = corrected.get("correction") if isinstance(corrected, dict) else None
    corrected_proposal = corrected.get("proposal") if isinstance(corrected, dict) else None
    old_source = next((item for item in inventory.get("entries", []) if item.get("name") == "CaptureNestedFactory.json"), None)
    correction_report = {
        "path": ".ufo/waves/round-22/w1/reports/CaptureNestedFactory.md",
        "sha256": "428cc0553c03f20d82d230094fdeeecbff968d59208ebf2eda7783722f987474",
    }
    if not isinstance(corrected, dict) or not isinstance(correction, dict) or not isinstance(old_source, dict):
        raise Refusal("nested factory typo/correction eligibility decision was not preserved")
    if (
        typo.get("path") != f"{inventory['path']}/CaptureNestedFactory.json"
        or typo.get("reason") != "ineligible author typo: want omits 'nest-' while the source cell passes r22-nest-inner; preserved unchanged and not excluded by detector results"
        or typo.get("correction_report") != correction_report
        or typo.get("sha256") != old_source.get("sha256")
        or typo.get("superseded_by") != f"{inventory['path']}/CaptureNestedFactoryCorrected.json"
        or typo.get("canonical_id") != "CaptureNestedFactory"
        or not isinstance(corrected_proposal, dict)
        or corrected_proposal.get("path") != f"{inventory['path']}/CaptureNestedFactoryCorrected.json"
        or corrected_proposal.get("fields", {}).get("id") != "CaptureNestedFactory"
        or correction.get("canonical_id") != "CaptureNestedFactory"
        or correction.get("supersedes") != f"{inventory['path']}/CaptureNestedFactory.json"
        or correction.get("superseded_sha256") != old_source.get("sha256")
        or correction.get("report") != correction_report
    ):
        raise Refusal("nested factory correction provenance changed")
    kwunknown = case_by_id.get("CaptureKwUnknown")
    if not isinstance(kwunknown, dict) or len(kwunknown.get("addenda", [])) != 1:
        raise Refusal("CaptureKwUnknown sealed addendum was not applied")
    if (
        kwunknown["addenda"][0].get("path") != f"{inventory['path']}/CaptureKwUnknown.addendum.json"
        or kwunknown.get("require_signal") is not True
        or kwunknown.get("forbid_commands_any_tier") != [
            "pacman -Q r22-kwunknown-global", "pacman -S r22-kwunknown-global"
        ]
    ):
        raise Refusal("CaptureKwUnknown any-tier, signal, or provenance assertions changed")
    if expected.get("input_manifest") != [{"fixture": case["fixture"], "sha256": case["input_sha256"]} for case in cases]:
        raise Refusal("input manifest differs from the actual frozen population")
    population_basis = {key: expected[key] for key in (
        "truth_seal", "proposal_inventory", "cases", "rejected", "required_proposals", "input_manifest", "historical_guard"
    )}
    if expected.get("population_sha256") != canonical_digest(population_basis):
        raise Refusal("population digest mismatch")
    tool_sha = None
    if tool_path is not None:
        tool_sha = digest(read_local_regular(tool_path))
        if expected_tool_sha is not None and tool_sha != expected_tool_sha:
            raise Refusal("selected scanner tool changed during measurement")
    return {
        "expected_sha256": current_sha, "expected_pin_file_sha256": current_pin_sha,
        "population_sha256": expected["population_sha256"], "truth_seal_sha256": TRUTH_SEAL_SHA256,
        "sealed_source_files_verified": seal_facts["files_verified"],
        "proposal_files_verified": actual_proposal_count, "input_files_verified": len(cases),
        "producer_sha256": producer_sha, "runner_sha256": runner_sha, "tool_sha256": tool_sha,
    }


def set_address_space_limit() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (CAP, CAP))


def decode_captured(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return str(value)


def scan(tool: Path, fixture: Path) -> dict[str, Any]:
    argv = [sys.executable, "-I", "-c", WRAPPER, str(tool), str(fixture)]
    try:
        completed = subprocess.run(
            argv, capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=TIMEOUT_SECONDS, preexec_fn=set_address_space_limit,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "argv": argv, "exit": None, "error": "timeout", "stdout": decode_captured(error.stdout),
            "stderr": decode_captured(error.stderr),
        }
    except OSError as error:
        return {"argv": argv, "exit": None, "error": f"scanner process could not start: {error}", "stdout": "", "stderr": ""}
    result: dict[str, Any] = {
        "argv": argv, "exit": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr,
    }
    nonempty = [line for line in completed.stdout.splitlines() if line.strip()]
    if not nonempty:
        result["error"] = "scanner produced no JSON output"
        return result
    try:
        result["payload"] = strict_json(nonempty[-1].encode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        result["error"] = f"scanner output is not strict JSON: {error}"
    return result


def parse_scan_output(scan_result: dict[str, Any], case: dict[str, Any], fixture: Path) -> tuple[list[dict[str, str]], int, list[str]]:
    errors = []
    if scan_result.get("error"):
        return [], 0, [str(scan_result["error"])]
    if scan_result.get("exit") not in (0, 1):
        errors.append(f"scanner exit {scan_result.get('exit')} is not 0 or 1")
    payload = scan_result.get("payload")
    if not isinstance(payload, dict):
        return [], 0, errors + ["scanner payload is not an object"]
    findings = payload.get("findings")
    files = payload.get("files")
    if not isinstance(findings, list) or not isinstance(files, list) or len(files) != 1:
        return [], 0, errors + ["scanner findings/files shape is invalid or does not identify one input"]
    file_row = files[0]
    if not isinstance(file_row, dict):
        return [], 0, errors + ["scanner file row is not an object"]
    if file_row.get("sha256") != case.get("input_sha256"):
        errors.append("scanner-reported input digest differs from the sealed fixture")
    reported_path = file_row.get("path")
    if not isinstance(reported_path, str):
        errors.append("scanner file row has no explicit path")
    else:
        try:
            if Path(reported_path).resolve(strict=True) != fixture.resolve(strict=True):
                errors.append("scanner-reported path differs from the selected fixture")
        except OSError:
            errors.append("scanner-reported path is unavailable")
    unparsed = 0
    for key in ("eval_unparsed", "unparsed_spawns"):
        value = file_row.get(key)
        if type(value) is not int or value < 0:
            errors.append(f"scanner file row has invalid {key}")
        else:
            unparsed += value
    rows = []
    for index, row in enumerate(findings):
        if not isinstance(row, dict) or not ROW_KEYS <= set(row):
            errors.append(f"finding {index} lacks explicit class, command or evidence")
            continue
        if not isinstance(row["class"], str) or not row["class"] or not isinstance(row["command"], str) or not row["command"]:
            errors.append(f"finding {index} has invalid class/command")
            continue
        if row["evidence"] not in ("observed", "lead"):
            errors.append(f"finding {index} has invalid evidence marker")
            continue
        rows.append({"class": row["class"], "command": row["command"], "evidence": row["evidence"]})
    return rows, unparsed, errors


def row_keys(rows: list[dict[str, str]]) -> list[tuple[str, str, str]]:
    return sorted((row["class"], row["command"], row["evidence"]) for row in rows)


def evaluate(case: dict[str, Any], rows: list[dict[str, str]], unparsed: int, parse_errors: list[str]) -> tuple[bool, list[str]]:
    reasons = list(parse_errors)
    if reasons:
        return False, reasons
    forbidden_any = case["forbid_commands_any_tier"]
    forbidden_observed = case["forbid_observed_commands"]
    for row in rows:
        if row["command"] in forbidden_any:
            reasons.append(f"forbidden at any evidence tier: {row['command']}")
        if row["evidence"] == "observed" and row["command"] in forbidden_observed:
            reasons.append(f"forbidden observed command: {row['command']}")
    if reasons:
        return False, reasons
    expected = row_keys(case["want"])
    actual = row_keys(rows)
    has_signal = unparsed > 0 or any(row["evidence"] == "lead" for row in rows)
    if case["expected_kind"] == "exact":
        matched = actual == expected and unparsed == 0
        if not matched and not reasons:
            reasons.append("complete class/command/evidence multiset or zero-error condition differs")
        return matched, reasons

    accept_exact = case.get("accept_exact_want")
    if accept_exact is not None and actual == row_keys(accept_exact) and unparsed == 0:
        return True, []
    has_observed = any(row["evidence"] == "observed" for row in rows)
    if has_observed:
        reasons.append("uncertain case produced an observed row outside its complete accept_exact_want")
        return False, reasons
    if case["require_signal"] and not has_signal:
        reasons.append("uncertain case requires a lead row or positive unparsed counter")
        return False, reasons
    wanted_leads = [row for row in case["want"] if row["evidence"] == "lead"]
    if wanted_leads:
        remaining = row_keys([row for row in rows if row["evidence"] == "lead"])
        for wanted in row_keys(wanted_leads):
            try:
                remaining.remove(wanted)
            except ValueError:
                reasons.append(f"required uncertain lead is missing: {wanted[1]}")
        if reasons:
            return False, reasons
    return True, []


def emit_refusal(argv: list[str], error: Exception) -> int:
    print(json.dumps({
        "schema": "mado-r22-c1-measure-v1", "status": "refused", "exit": 2,
        "argv": argv, "error": str(error),
    }, ensure_ascii=True, sort_keys=True))
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, type=Path)
    parser.add_argument("--case", help="run exactly one frozen case after validating the complete population")
    parser.add_argument("--group", choices=("proposal", "supplemental-original"),
                        help="select one frozen group; validate the entire population first")
    args = parser.parse_args(argv)
    command_argv = [sys.executable, *sys.argv]
    try:
        expected, expected_raw, pin_raw, expected_sha, pin_sha = read_expected()
        before = verify_population(expected, expected_sha, pin_sha)
    except Exception as error:
        return emit_refusal(command_argv, error)

    cases = expected["cases"]
    if args.case is not None and args.group is not None:
        return emit_refusal(command_argv, Refusal("--case and --group are mutually exclusive"))
    if args.case is not None:
        matched = [case for case in cases if case["id"] == args.case]
        if len(matched) != 1:
            return emit_refusal(command_argv, Refusal(f"--case requires one exact case id; found {len(matched)} for {args.case!r}"))
        selected = matched
    elif args.group is not None:
        selected = [case for case in cases if case["group"] == args.group]
        if not selected:
            return emit_refusal(command_argv, Refusal("selected group is empty"))
    else:
        selected = cases

    try:
        requested_tool = args.tool
        tool = requested_tool.resolve(strict=True)
        if not tool.is_file():
            raise Refusal(f"selected scanner is not a regular file: {requested_tool}")
        tool_sha = digest(read_local_regular(tool))
        before = verify_population(expected, expected_sha, pin_sha, tool, tool_sha)
    except Exception as error:
        return emit_refusal(command_argv, error)

    results = []
    for case in selected:
        scan_result: dict[str, Any] = {"argv": None, "exit": None, "stdout": "", "stderr": ""}
        rows: list[dict[str, str]] = []
        unparsed = 0
        passed = False
        reasons: list[str] = []
        try:
            fixture = safe_regular(ROOT, case["fixture"])
            scan_result = scan(tool, fixture)
            rows, unparsed, parse_errors = parse_scan_output(scan_result, case, fixture)
            passed, reasons = evaluate(case, rows, unparsed, parse_errors)
        except Exception as error:
            reasons = [f"case could not be evaluated: {error}"]
        results.append({
            "id": case["id"], "group": case["group"], "expected_kind": case["expected_kind"],
            "want": case["want"], "accept_exact_want": case.get("accept_exact_want"),
            "forbid_observed_commands": case["forbid_observed_commands"],
            "forbid_commands_any_tier": case["forbid_commands_any_tier"],
            "require_signal": case["require_signal"],
            "got_rows": rows, "unparsed": unparsed, "pass": passed, "reasons": reasons,
            "argv": scan_result.get("argv"), "exit": scan_result.get("exit"),
            "stdout": scan_result.get("stdout", ""), "stderr": scan_result.get("stderr", ""),
            "scanner_error": scan_result.get("error"), "scanner_payload": scan_result.get("payload"),
        })

    after_errors = []
    try:
        after = verify_population(expected, expected_sha, pin_sha, tool, tool_sha)
    except Exception as error:
        after = None
        after_errors.append(str(error))
    comparison_pass = all(row["pass"] for row in results)
    final_exit = 2 if after_errors else (0 if comparison_pass else 1)
    output = {
        "schema": "mado-r22-c1-measure-v1", "status": "complete" if not after_errors else "refused-after-run",
        "argv": command_argv, "case_filter": args.case, "group_filter": args.group,
        "tool_argument": str(requested_tool), "tool_path": str(tool), "tool_sha256_before": tool_sha,
        "producer_sha256": before["producer_sha256"], "runner_sha256": before["runner_sha256"],
        "expected_sha256": expected_sha, "expected_pin_file_sha256": pin_sha,
        "population_sha256": before["population_sha256"],
        "integrity_before": before, "integrity_after": after, "integrity_errors": after_errors,
        "cases": results, "totals": {"pass": sum(bool(row["pass"]) for row in results), "total": len(results)},
        "exit": final_exit,
    }
    print(json.dumps(output, ensure_ascii=True, sort_keys=True))
    return final_exit


if __name__ == "__main__":
    raise SystemExit(main())
