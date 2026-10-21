#!/usr/bin/env python3
"""Materialize the sealed round-22 C1 truth set as inert eval JSONL inputs."""
from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
WAVE = LANE / ".ufo/waves/round-22"
PROPOSALS = WAVE / "w1/proposals"
TRUTH_SEAL = WAVE / "truth-seal.json"
TRUTH_SEAL_REL = ".ufo/waves/round-22/truth-seal.json"
TRUTH_SEAL_SHA256 = "47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4"
ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "inputs"
EXPECTED = ROOT / "expected.json"
PIN = ROOT / "expected.sha256"
FINAL_BINDING_REL = ".ufo/waves/round-21/residual/FinalBindingReview.md"
FINAL_BINDING_SHA256 = "9caedd3d4c521b1a07e4206274e0b3041911caefbf845f85890737e1daef888f"
R19_PURE_REL = ".ufo/waves/round-20/precision/CasePureBuiltins--frozenset-closure.jsonl"
NESTED_CORRECTION_REL = ".ufo/waves/round-22/w1/reports/CaptureNestedFactory.md"
NESTED_CORRECTION_SHA256 = "428cc0553c03f20d82d230094fdeeecbff968d59208ebf2eda7783722f987474"
REQUIRED_PROPOSALS = ["TimerRunAliasActual", "CapturePartialGlobalLateActual", "CaptureNestedFactory"]
RAW_PROPOSAL_COUNT = 52
ELIGIBLE_PROPOSAL_COUNT = 50
SUPPLEMENTAL_ORIGINAL_COUNT = 7

BASE_REQUIRED = {"id", "cells", "expected_kind", "want", "forbid_observed_commands", "rationale", "source"}
BASE_OPTIONAL = {"language", "forbid_commands_any_tier", "require_signal", "accept_exact_want", "cell_reset"}
ROW_KEYS = {"class", "command", "evidence"}

ORIGINALS = (
    {
        "id": "OriginalF1CaptureInvokeTime", "filename": "capture-invoke-time.jsonl",
        "sha256": "6b21d584710878f5e486f3e9fcd737c6a6e573c629c2f75d30b45f55b6a317f7",
        "kind": "exact", "want": [{"class": "host_mutation", "command": "pacman -S r21-factory", "evidence": "observed"}],
        "forbid_observed": [], "forbid_any": [], "signal": True, "table": "F1",
        "r21": [{"class": "package_query", "command": "pacman -Q r21-invoke", "evidence": "observed"}],
        "r21_note": "wrong command; host_mutation missing",
    },
    {
        "id": "OriginalF2CaptureUnboundGlobal", "filename": "capture-unbound-global.jsonl",
        "sha256": "9ab845d4a8886714cfea0b16203328b67335013f00b21b18ba23e9b7175e1d9d",
        "kind": "uncertain", "want": [], "forbid_observed": ["pacman -Q r21-global"],
        "forbid_any": ["pacman -Q r21-global"], "signal": True, "table": "F2",
        "r21": [{"class": "package_query", "command": "pacman -Q r21-global", "evidence": "observed"}],
        "r21_note": "borrowed module-global argv; no static command is known",
    },
    {
        "id": "OriginalF3ReturnedRebound", "filename": "returned-rebound.jsonl",
        "sha256": "774e2946d16c23d9ebdd557ccf279143f6d2249dc7132aa567fb34d12d3d7573",
        "kind": "exact", "want": [{"class": "host_mutation", "command": "pacman -S r21-b", "evidence": "observed"}],
        "forbid_observed": [], "forbid_any": [], "signal": True, "table": "F3",
        "r21": [{"class": "package_query", "command": "pacman -Q r21-a", "evidence": "observed"}],
        "r21_note": "wrong closure body; host_mutation missing",
    },
    {
        "id": "OriginalF4ThreadRunDirect", "filename": "thread-run-direct.jsonl",
        "sha256": "1cc1188dc4e0c37ecba97d34bdf546113d888c62a9cba0bcfe06d44201a2407f",
        "kind": "exact", "want": [{"class": "host_mutation", "command": "pacman -S r21-thread-run", "evidence": "observed"}],
        "forbid_observed": [], "forbid_any": [], "signal": True, "table": "F4", "r21": [],
        "r21_note": "no finding and both unparsed counters were zero",
    },
    {
        "id": "OriginalF5ThreadKeyHygiene", "filename": "thread-key-hygiene.jsonl",
        "sha256": "4ea8ccc8724de011e19dcc1e69da1f4078ac74544f554e39ccda66dc42065c9e",
        "kind": "exact", "want": [{"class": "package_query", "command": "pacman -Q r21-hyg", "evidence": "observed"}],
        "forbid_observed": [], "forbid_any": [], "signal": True, "table": "F5",
        "r21": [{"class": "package_query", "command": "pacman -Q r21-hyg", "evidence": "lead"}],
        "r21_note": "same command was downgraded from observed to lead",
    },
    {
        "id": "OriginalF5ThreadKeyControl", "filename": "thread-key-control.jsonl",
        "sha256": "00ecb83fabddfd002d703bc1fbaa449b24e1edf935d0f6792a773c96007162be",
        "kind": "exact", "want": [{"class": "package_query", "command": "pacman -Q r21-hyg", "evidence": "observed"}],
        "forbid_observed": [], "forbid_any": [], "signal": True, "table": "control",
        "r21": [{"class": "package_query", "command": "pacman -Q r21-hyg", "evidence": "observed"}],
        "r21_note": "passing control",
    },
    {
        "id": "OriginalR19PureFrozenClosure", "path": R19_PURE_REL,
        "sha256": "14558b6dd1574253772b30af041169c6fb0eda992d47c7773c342c225472f040",
        "kind": "exact", "want": [], "forbid_observed": [], "forbid_any": [], "signal": False,
        "table": "round-20 precision / CasePureBuiltins--frozenset-closure", "r21": [],
        "r21_note": "pure-data original; exact empty truth, not rerun",
    },
)


class ProposalError(ValueError):
    pass


class SealError(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise SealError(f"not a regular file: {path}")
    return digest(path.read_bytes())


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


def sorted_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(rows, key=lambda row: (row["class"], row["command"], row["evidence"]))


def validate_rows(value: Any, label: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise ProposalError(f"{label} must be a list")
    result = []
    for index, row in enumerate(value):
        if not isinstance(row, dict) or set(row) != ROW_KEYS:
            raise ProposalError(f"{label}[{index}] must contain exactly class, command, evidence")
        if not isinstance(row["class"], str) or not row["class"].strip():
            raise ProposalError(f"{label}[{index}].class must be nonempty text")
        if not isinstance(row["command"], str) or not row["command"].strip():
            raise ProposalError(f"{label}[{index}].command must be nonempty text")
        if row["evidence"] not in ("observed", "lead"):
            raise ProposalError(f"{label}[{index}].evidence must be observed or lead")
        result.append({"class": row["class"], "command": row["command"], "evidence": row["evidence"]})
    return result


def validate_commands(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ProposalError(f"{label} must be a list of nonempty strings")
    if len(value) != len(set(value)):
        raise ProposalError(f"{label} contains duplicate commands")
    return list(value)


def reset_vector(value: Any, count: int, label: str = "cell_reset") -> list[bool]:
    if not isinstance(value, list) or len(value) != count or any(type(item) is not bool for item in value):
        raise ProposalError(f"{label} must be an exact bool list with one entry per cell")
    return list(value)


def validate_base(value: Any, filename_stem: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProposalError("proposal must be a JSON object")
    keys = set(value)
    missing, unknown = BASE_REQUIRED - keys, keys - BASE_REQUIRED - BASE_OPTIONAL
    if missing or unknown:
        raise ProposalError(f"unsupported proposal shape (missing={sorted(missing)}, extra={sorted(unknown)})")
    case_id = value["id"]
    corrected = filename_stem == "CaptureNestedFactoryCorrected" and case_id == "CaptureNestedFactory"
    if not isinstance(case_id, str) or (case_id != filename_stem and not corrected):
        raise ProposalError("id must match filename stem, except corrected nested factory retains canonical id")
    cells = value["cells"]
    if not isinstance(cells, list) or not cells or any(not isinstance(cell, str) or not cell.strip() for cell in cells):
        raise ProposalError("cells must be nonempty inert Python eval source strings")
    if value.get("language", "py") != "py":
        raise ProposalError("only Python eval source is supported; language metadata must be 'py'")
    kind = value["expected_kind"]
    if kind not in ("exact", "uncertain"):
        raise ProposalError("expected_kind must be exact or uncertain")
    want_in = validate_rows(value["want"], "want")
    accept = None
    if "accept_exact_want" in value:
        accept = validate_rows(value["accept_exact_want"], "accept_exact_want")
        if kind != "uncertain" or not accept:
            raise ProposalError("accept_exact_want must be nonempty and belong to an uncertain case")
    forbidden_observed = validate_commands(value["forbid_observed_commands"], "forbid_observed_commands")
    forbidden_any = validate_commands(value.get("forbid_commands_any_tier", []), "forbid_commands_any_tier")
    require_signal = value.get("require_signal", kind == "uncertain" or bool(want_in))
    if type(require_signal) is not bool:
        raise ProposalError("require_signal must be an exact bool")
    resets = reset_vector(value["cell_reset"], len(cells)) if "cell_reset" in value else [False] * len(cells)
    for field in ("rationale", "source"):
        if not isinstance(value[field], str) or not value[field].strip():
            raise ProposalError(f"{field} must be nonempty text")
    for row in [*want_in, *(accept or [])]:
        if row["command"] in forbidden_any:
            raise ProposalError("wanted command conflicts with forbid_commands_any_tier")
    return {
        "id": case_id, "cells": list(cells), "cell_reset": resets, "expected_kind": kind,
        "want_input_order": want_in, "want": sorted_rows(want_in),
        "accept_exact_want": sorted_rows(accept) if accept is not None else None,
        "forbid_observed_commands": forbidden_observed, "forbid_commands_any_tier": forbidden_any,
        "require_signal": require_signal, "fields": value, "rationale": value["rationale"],
        "source": value["source"], "addenda": [],
    }


def validate_addendum(value: Any, filename_stem: str, base: dict[str, Any]) -> dict[str, Any]:
    required = {"id", "addendum_to", "rationale", "source"}
    allowed = BASE_REQUIRED | BASE_OPTIONAL | {"addendum_to"}
    if not isinstance(value, dict) or not required <= set(value) or set(value) - allowed:
        raise ProposalError("addendum has unsupported or missing fields")
    if value["id"] != filename_stem or value["addendum_to"] != base["id"]:
        raise ProposalError("addendum id/path or addendum_to target mismatch")
    if not any(key in value for key in ("forbid_commands_any_tier", "require_signal", "accept_exact_want")):
        raise ProposalError("addendum has no supported expectation constraint")
    for field in ("rationale", "source"):
        if not isinstance(value[field], str) or not value[field].strip():
            raise ProposalError(f"addendum {field} must be nonempty text")
    comparisons = {
        "cells": base["cells"], "expected_kind": base["expected_kind"],
        "want": base["want_input_order"],
        "forbid_observed_commands": base["forbid_observed_commands"],
        "language": base["fields"].get("language", "py"),
    }
    for field, expected in comparisons.items():
        if field in value:
            actual = validate_rows(value[field], field) if field == "want" else value[field]
            if actual != expected:
                raise ProposalError(f"addendum may not change base {field}")
    if "cell_reset" in value and reset_vector(value["cell_reset"], len(base["cells"])) != base["cell_reset"]:
        raise ProposalError("addendum may not change base cell_reset")
    accept = None
    if "accept_exact_want" in value:
        accept = sorted_rows(validate_rows(value["accept_exact_want"], "accept_exact_want"))
        if not accept or (base["accept_exact_want"] is not None and accept != base["accept_exact_want"]):
            raise ProposalError("addendum accept_exact_want is empty or conflicts with base")
    forbidden = validate_commands(value.get("forbid_commands_any_tier", []), "forbid_commands_any_tier")
    signal = value.get("require_signal")
    if signal is not None and type(signal) is not bool:
        raise ProposalError("addendum require_signal must be an exact bool")
    if signal is False and base["require_signal"]:
        raise ProposalError("addendum may not weaken require_signal")
    return {"fields": value, "forbid_commands_any_tier": forbidden, "require_signal": signal, "accept_exact_want": accept}


def make_fixture(case_id: str, cells: list[str], resets: list[bool]) -> bytes:
    rows = []
    for index, (code, reset) in enumerate(zip(cells, resets, strict=True)):
        call = {
            "type": "toolCall", "id": f"{case_id}-{index}", "name": "eval",
            "arguments": {"language": "py", "code": code, "reset": reset},
        }
        rows.append(json.dumps({"type": "message", "message": {"role": "assistant", "content": [call]}}, sort_keys=True, separators=(",", ":")))
    return ("\n".join(rows) + "\n").encode("utf-8")


def safe_lane_file(relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise SealError(f"unsafe sealed path: {relative}")
    base = LANE.resolve(strict=True)
    current = base
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise SealError(f"symlink in sealed path: {relative}")
    resolved = current.resolve(strict=True)
    if not resolved.is_relative_to(base) or not resolved.is_file():
        raise SealError(f"sealed path is absent or outside lane: {relative}")
    return resolved


def load_raw_seal() -> tuple[dict[str, Any], bytes]:
    raw = safe_lane_file(TRUTH_SEAL_REL).read_bytes()
    if digest(raw) != TRUTH_SEAL_SHA256:
        raise SealError("raw truth-seal.json digest differs from its registered pre-implementation pin")
    seal = strict_json(raw)
    if not isinstance(seal, dict) or seal.get("schema") != "mado-r22-independent-truth-seal-v1":
        raise SealError("unsupported raw truth seal")
    if seal.get("base_commit") != "741122d177ae8ff68a73768777f20484d5bdcbe4":
        raise SealError("raw truth seal has an unexpected source base")
    files = seal.get("files")
    if not isinstance(files, list) or len(files) != 106:
        raise SealError("raw truth seal must contain all 106 frozen source files")
    seen: set[str] = set()
    for entry in files:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "bytes"}:
            raise SealError("raw truth seal contains an invalid file record")
        path, checksum, byte_count = entry["path"], entry["sha256"], entry["bytes"]
        if not isinstance(path, str) or path in seen or not isinstance(checksum, str) or len(checksum) != 64:
            raise SealError("raw truth seal contains a duplicate or invalid path/digest")
        if type(byte_count) is not int or byte_count < 0:
            raise SealError(f"raw truth seal has an invalid byte count for {path}")
        seen.add(path)
        target = safe_lane_file(path)
        content = target.read_bytes()
        if len(content) != byte_count or digest(content) != checksum:
            raise SealError(f"raw sealed file changed: {path}")
    return seal, raw


def proposal_snapshot(seal: dict[str, Any]) -> tuple[dict[str, Any], dict[str, bytes], list[dict[str, Any]]]:
    inventory = {"path": ".ufo/waves/round-22/w1/proposals", "kind": "directory", "entries": []}
    raw_files: dict[str, bytes] = {}
    rejected: list[dict[str, Any]] = []
    if PROPOSALS.is_symlink() or not PROPOSALS.is_dir():
        raise SealError("sealed proposal directory is absent, non-directory, or symlinked")
    entries = []
    for path in sorted(PROPOSALS.iterdir(), key=lambda item: item.name):
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise SealError(f"sealed proposal entry is a symlink: {path.name}")
        if stat.S_ISREG(mode):
            raw = path.read_bytes()
            checksum = digest(raw)
            entries.append({"name": path.name, "kind": "file", "sha256": checksum, "bytes": len(raw)})
            raw_files[path.name] = raw
            if path.suffix != ".json":
                rejected.append({"path": f"{inventory['path']}/{path.name}", "sha256": checksum, "reason": "not a JSON proposal or addendum"})
        elif stat.S_ISDIR(mode):
            entries.append({"name": path.name, "kind": "directory"})
            rejected.append({"path": f"{inventory['path']}/{path.name}", "sha256": None, "reason": "proposal delivery must be a direct JSON file"})
        else:
            entries.append({"name": path.name, "kind": "other"})
            rejected.append({"path": f"{inventory['path']}/{path.name}", "sha256": None, "reason": "proposal entry is not a regular JSON file"})
    inventory["entries"] = entries
    sealed = {record["path"]: record for record in seal["files"] if record["path"].startswith(inventory["path"] + "/")}
    actual = {f"{inventory['path']}/{name}": {"path": f"{inventory['path']}/{name}", "sha256": digest(raw), "bytes": len(raw)} for name, raw in raw_files.items()}
    if sealed != actual:
        raise SealError("proposal files do not exactly match the sealed C1 source population")
    if len(raw_files) != RAW_PROPOSAL_COUNT or sum(name.endswith(".addendum.json") for name in raw_files) != 1:
        raise SealError("sealed C1 proposal population is not the recorded 52-file set")
    return inventory, raw_files, rejected


def verify_originals(seal: dict[str, Any]) -> None:
    sealed = {entry["path"]: entry for entry in seal["files"]}
    for original in ORIGINALS:
        relative = original.get("path") or f".ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/{original['filename']}"
        record = sealed.get(relative)
        if record is None or record["sha256"] != original["sha256"]:
            raise SealError(f"original fixture is absent from raw truth seal or has a different digest: {relative}")
        safe_lane_file(relative)


def main() -> int:
    for output in (INPUTS, EXPECTED, PIN):
        if output.exists() or output.is_symlink():
            raise SystemExit(f"refusing to overwrite frozen assembly output: {output}")
    seal, seal_raw = load_raw_seal()
    inventory, raw_files, rejected = proposal_snapshot(seal)
    verify_originals(seal)

    proposals: dict[str, dict[str, Any]] = {}
    proposal_paths: dict[str, str] = {}
    proposal_hashes: dict[str, str] = {}
    pending_addenda: list[tuple[str, bytes]] = []
    for name, raw in sorted(raw_files.items()):
        if not name.endswith(".json"):
            continue
        path = f"{inventory['path']}/{name}"
        try:
            value = strict_json(raw)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            rejected.append({"path": path, "sha256": digest(raw), "reason": str(error)})
            continue
        if name.endswith(".addendum.json"):
            pending_addenda.append((name, raw))
            continue
        if name == "CaptureNestedFactory.json":
            rejected.append({
                "path": path, "sha256": digest(raw),
                "reason": "ineligible author typo: want omits 'nest-' while the source cell passes r22-nest-inner; preserved unchanged and not excluded by detector results",
                "superseded_by": f"{inventory['path']}/CaptureNestedFactoryCorrected.json",
                "canonical_id": "CaptureNestedFactory",
                "correction_report": {"path": NESTED_CORRECTION_REL, "sha256": NESTED_CORRECTION_SHA256},
            })
            continue
        try:
            proposal = validate_base(value, Path(name).stem)
        except (TypeError, ValueError, ProposalError) as error:
            rejected.append({"path": path, "sha256": digest(raw), "reason": str(error)})
            continue
        if proposal["id"] in proposals:
            rejected.append({"path": path, "sha256": digest(raw), "reason": f"duplicate canonical case id {proposal['id']}"})
            continue
        proposals[proposal["id"]] = proposal
        proposal_paths[proposal["id"]] = path
        proposal_hashes[proposal["id"]] = digest(raw)

    for name, raw in pending_addenda:
        path = f"{inventory['path']}/{name}"
        try:
            value = strict_json(raw)
            if not isinstance(value, dict) or not isinstance(value.get("addendum_to"), str):
                raise ProposalError("addendum_to is missing")
            base_id = value["addendum_to"]
            if base_id not in proposals:
                raise ProposalError("addendum target is absent or ineligible")
            contribution = validate_addendum(value, Path(name).stem, proposals[base_id])
            next_forbidden = proposals[base_id]["forbid_commands_any_tier"] + contribution["forbid_commands_any_tier"]
            next_accept = proposals[base_id]["accept_exact_want"] or contribution["accept_exact_want"] or []
            for row in [*proposals[base_id]["want"], *next_accept]:
                if row["command"] in next_forbidden:
                    raise ProposalError("addendum any-tier exclusion conflicts with a wanted command")
            proposals[base_id]["forbid_commands_any_tier"] = next_forbidden
            if contribution["accept_exact_want"] is not None and proposals[base_id]["accept_exact_want"] is None:
                proposals[base_id]["accept_exact_want"] = contribution["accept_exact_want"]
            if contribution["require_signal"] is True:
                proposals[base_id]["require_signal"] = True
            proposals[base_id]["addenda"].append({"path": path, "sha256": digest(raw), "fields": contribution["fields"]})
        except (TypeError, UnicodeDecodeError, json.JSONDecodeError, ValueError, ProposalError) as error:
            rejected.append({"path": path, "sha256": digest(raw), "reason": str(error)})

    if len(proposals) != ELIGIBLE_PROPOSAL_COUNT:
        raise SystemExit(f"sealed proposal set yielded {len(proposals)}, expected {ELIGIBLE_PROPOSAL_COUNT}; refusing incomplete materialization")
    required = [{"id": case_id, "present": case_id in proposals} for case_id in REQUIRED_PROPOSALS]
    if not all(row["present"] for row in required):
        raise SystemExit("a required sealed corrected proposal is missing or ineligible")
    kwunknown = proposals["CaptureKwUnknown"]
    if (
        len(kwunknown["addenda"]) != 1
        or kwunknown["addenda"][0]["path"] != f"{inventory['path']}/CaptureKwUnknown.addendum.json"
        or not kwunknown["require_signal"]
        or kwunknown["forbid_commands_any_tier"] != [
            "pacman -Q r22-kwunknown-global", "pacman -S r22-kwunknown-global"
        ]
    ):
        raise SystemExit("sealed CaptureKwUnknown addendum constraints were not materialized")

    fixture_bytes: dict[str, bytes] = {}
    cases: list[dict[str, Any]] = []
    for case_id, proposal in sorted(proposals.items()):
        fixture = f"inputs/{case_id}.jsonl"
        fixture_bytes[fixture] = make_fixture(case_id, proposal["cells"], proposal["cell_reset"])
        proposal_path = proposal_paths[case_id]
        correction = None
        if case_id == "CaptureNestedFactory" and proposal_path.endswith("CaptureNestedFactoryCorrected.json"):
            old = next((entry for entry in inventory["entries"] if entry["name"] == "CaptureNestedFactory.json"), None)
            correction = {
                "supersedes": f"{inventory['path']}/CaptureNestedFactory.json",
                "superseded_sha256": old["sha256"] if old else None,
                "report": {"path": NESTED_CORRECTION_REL, "sha256": NESTED_CORRECTION_SHA256},
                "canonical_id": "CaptureNestedFactory",
            }
        cases.append({
            "id": case_id, "group": "proposal", "expected_kind": proposal["expected_kind"],
            "fixture": fixture, "input_sha256": digest(fixture_bytes[fixture]),
            "cell_count": len(proposal["cells"]), "cell_reset": proposal["cell_reset"],
            "proposal": {"path": proposal_path, "sha256": proposal_hashes[case_id], "fields": proposal["fields"]},
            "addenda": proposal["addenda"], "correction": correction,
            "want_input_order": proposal["want_input_order"], "want": proposal["want"],
            "accept_exact_want": proposal["accept_exact_want"],
            "forbid_observed_commands": proposal["forbid_observed_commands"],
            "forbid_commands_any_tier": proposal["forbid_commands_any_tier"],
            "require_signal": proposal["require_signal"],
            "rationale": proposal["rationale"], "source": proposal["source"],
        })

    for original in ORIGINALS:
        if original["id"] == "OriginalR19PureFrozenClosure":
            source_path = original["path"]
            source = safe_lane_file(source_path)
            truth_basis = "one inert eval assigning a literal frozenset; exact empty truth from the raw independent seal"
        else:
            source_path = f".ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/{original['filename']}"
            source = safe_lane_file(source_path)
            truth_basis = "FinalBindingReview.md Probe result table; independent static truth, not the prior scanner row"
        raw = source.read_bytes()
        if digest(raw) != original["sha256"]:
            raise SealError(f"supplemental original changed: {source_path}")
        fixture = f"inputs/{original['id']}.jsonl"
        fixture_bytes[fixture] = raw
        cases.append({
            "id": original["id"], "group": "supplemental-original", "expected_kind": original["kind"],
            "fixture": fixture, "input_sha256": original["sha256"], "cell_count": 1,
            "cell_reset": [False], "proposal": None, "addenda": [], "correction": None,
            "want_input_order": original["want"], "want": sorted_rows(original["want"]),
            "accept_exact_want": None, "forbid_observed_commands": original["forbid_observed"],
            "forbid_commands_any_tier": original["forbid_any"], "require_signal": original["signal"],
            "source_provenance": {"path": source_path, "sha256": original["sha256"], "table_row": original["table"], "basis": truth_basis},
            "historical_r21": {"reported_findings": original["r21"], "note": original["r21_note"], "source": FINAL_BINDING_REL},
        })

    if len(cases) != ELIGIBLE_PROPOSAL_COUNT + SUPPLEMENTAL_ORIGINAL_COUNT:
        raise SystemExit("normalized case population does not match the sealed proposal/original totals")
    rejected.sort(key=lambda item: (str(item.get("path", "")), str(item.get("reason", ""))))
    proposal_json_names = {name for name in raw_files if name.endswith(".json")}
    accepted_names = {case["proposal"]["path"].rsplit("/", 1)[-1] for case in cases if case["group"] == "proposal"}
    applied_addenda = {item["path"].rsplit("/", 1)[-1] for case in cases for item in case["addenda"]}
    rejected_names = {item["path"].rsplit("/", 1)[-1] for item in rejected if isinstance(item.get("path"), str) and item["path"].startswith(inventory["path"] + "/") and item["path"].endswith(".json")}
    if proposal_json_names != accepted_names | applied_addenda | rejected_names:
        raise SystemExit("sealed proposal inventory contains an unclassified JSON source")

    source_file_records = seal["files"]
    assembler_path = Path(__file__).resolve()
    runner_path = ROOT / "measure.py"
    expected = {
        "schema": "mado-r22-c1-oracle-v1",
        "materialization_status": "normalized expected created from a prior raw truth seal; this expected digest is pinned separately and was not part of that raw seal",
        "producer_sha256": file_digest(assembler_path),
        "runner_sha256": file_digest(runner_path),
        "truth_seal": {
            "path": TRUTH_SEAL_REL, "sha256": TRUTH_SEAL_SHA256,
            "schema": seal["schema"], "created_at": seal["created_at"],
            "base_commit": seal["base_commit"], "baseline_tool_sha256": seal["baseline_tool_sha256"],
            "file_count": len(source_file_records), "files": source_file_records,
            "premeasurement_decisions": seal["premeasurement_decisions"],
        },
        "limits": {"seconds_per_process": 15, "address_space_bytes": 402653184, "concurrency": 1},
        "comparison": {
            "exact": "complete sorted multiset equality of class, command and evidence, with zero unparsed counters",
            "uncertain": "complete accept_exact_want equality with zero unparsed, OR no observed rows and the per-case require_signal rule",
            "forbidden": "forbid_commands_any_tier is enforced for every finding regardless of evidence; observed-only forbids apply separately",
            "signal": "a lead row or positive eval_unparsed/unparsed_spawns counter",
            "transcripts": "each source cell maps one-to-one to an inert eval call; cell_reset maps one-to-one to arguments.reset; no payload is executed",
            "want_provenance": "sorted wants are compared, original proposal field values and input order are retained verbatim in expected.json",
        },
        "historical_r21_probe": {
            "reported_exit": 1, "observed_findings": 4, "lead_findings": 1,
            "counts": {"host_mutation": 0, "live_probe": 0, "package_query": 5, "tool_install": 0, "vcs_write": 0},
            "source": FINAL_BINDING_REL, "source_sha256": FINAL_BINDING_SHA256,
            "status": "known-red report retained as context; not rerun and not used to derive independent truth",
        },
        "historical_guard": {
            "name": "round-21 legacy precision guard", "baseline_pass": 166, "population_total": 175,
            "required_floor": 166, "reset_to_new_target": False,
            "owner": "Main runs the whole-175 comparison at the delivered commit; this oracle does not run it",
            "sources": [
                {"path": ".ufo/waves/round-21/residual/FinalRemovalReview.md", "sha256": "c872a0d4f94ee2e007286cd1ec82b0eb368f63fe35922de9461fb462d4b2522a"},
                {"path": ".ufo/waves/round-21/final-summary.json", "sha256": "e03a2f5a27a1b918e88721b34da38ff872aa8513a70449f37b27119757d9f5d8"},
            ],
        },
        "proposal_inventory": inventory,
        "raw_proposal_count": RAW_PROPOSAL_COUNT,
        "eligible_proposal_count": ELIGIBLE_PROPOSAL_COUNT,
        "supplemental_original_count": SUPPLEMENTAL_ORIGINAL_COUNT,
        "required_proposal_ids": REQUIRED_PROPOSALS,
        "required_proposals": required,
        "cases": cases,
        "rejected": rejected,
        "input_manifest": [{"fixture": case["fixture"], "sha256": case["input_sha256"]} for case in cases],
    }
    population_basis = {key: expected[key] for key in (
        "truth_seal", "proposal_inventory", "cases", "rejected", "required_proposals", "input_manifest", "historical_guard"
    )}
    expected["population_sha256"] = digest(json.dumps(population_basis, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii"))
    expected_bytes = (json.dumps(expected, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode("ascii")
    expected_sha = digest(expected_bytes)

    INPUTS.mkdir()
    for relative, raw in sorted(fixture_bytes.items()):
        with (ROOT / relative).open("xb") as stream:
            stream.write(raw)
    with EXPECTED.open("xb") as stream:
        stream.write(expected_bytes)
    with PIN.open("xb") as stream:
        stream.write(f"{expected_sha}  expected.json\n".encode("ascii"))
    print(json.dumps({
        "raw_proposals": RAW_PROPOSAL_COUNT, "eligible_proposals": len(proposals),
        "supplemental_originals": len(ORIGINALS), "cases": len(cases),
        "rejected": len(rejected), "expected_sha256": expected_sha,
        "population_sha256": expected["population_sha256"], "raw_truth_seal_sha256": TRUTH_SEAL_SHA256,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
