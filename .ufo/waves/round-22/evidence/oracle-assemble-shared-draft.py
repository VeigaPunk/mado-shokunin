#!/usr/bin/env python3
"""Freeze round-22 C1 proposals as inert, digest-pinned scanner inputs."""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
WAVE = ROOT.parent
PROJECT = ROOT.parents[3]
PROPOSALS = WAVE / "w1" / "proposals"
INPUTS = ROOT / "inputs"
EXPECTED = ROOT / "expected.json"
PIN = ROOT / "expected.sha256"
REVIEW_REL = ".ufo/waves/round-21/residual/FinalBindingReview.md"
REVIEW_SHA256 = "9caedd3d4c521b1a07e4206274e0b3041911caefbf845f85890737e1daef888f"
ORIGINAL_ROOT = PROJECT / ".ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview"
R19_PURE_PATH = ".ufo/waves/round-20/precision/CasePureBuiltins--frozenset-closure.jsonl"
R19_PURE_SHA256 = "14558b6dd1574253772b30af041169c6fb0eda992d47c7773c342c225472f040"
SOURCE_ARTIFACTS = [
    {"path": REVIEW_REL, "sha256": REVIEW_SHA256},
    {"path": ".ufo/waves/round-21/residual/FinalRemovalReview.md", "sha256": "c872a0d4f94ee2e007286cd1ec82b0eb368f63fe35922de9461fb462d4b2522a"},
    {"path": ".ufo/waves/round-21/final-summary.json", "sha256": "e03a2f5a27a1b918e88721b34da38ff872aa8513a70449f37b27119757d9f5d8"},
    {"path": R19_PURE_PATH, "sha256": R19_PURE_SHA256},
    {"path": ".ufo/waves/round-22/w1/reports/CaptureNestedFactory.md", "sha256": "428cc0553c03f20d82d230094fdeeecbff968d59208ebf2eda7783722f987474"},
]
REQUIRED_PROPOSALS = [
    "TimerRunAliasActual",
    "CapturePartialGlobalLateActual",
"CaptureNestedFactory",
]

ORIGINALS = (
    {
        "id": "OriginalF1CaptureInvokeTime",
        "filename": "capture-invoke-time.jsonl",
        "sha256": "6b21d584710878f5e486f3e9fcd737c6a6e573c629c2f75d30b45f55b6a317f7",
        "expected_kind": "exact",
        "want": [{"class": "host_mutation", "command": "pacman -S r21-factory", "evidence": "observed"}],
        "forbid_observed_commands": [],
        "forbid_commands_any_tier": [],
        "require_signal": True,
        "table_row": "F1",
        "r21_observed": [{"class": "package_query", "command": "pacman -Q r21-invoke", "evidence": "observed"}],
        "r21_outcome": "wrong command; host_mutation missing",
    },
    {
        "id": "OriginalF2CaptureUnboundGlobal",
        "filename": "capture-unbound-global.jsonl",
        "sha256": "9ab845d4a8886714cfea0b16203328b67335013f00b21b18ba23e9b7175e1d9d",
        "expected_kind": "uncertain",
        "want": [],
        "forbid_observed_commands": ["pacman -Q r21-global"],
        "forbid_commands_any_tier": ["pacman -Q r21-global"],
        "require_signal": True,
        "table_row": "F2",
        "r21_observed": [{"class": "package_query", "command": "pacman -Q r21-global", "evidence": "observed"}],
        "r21_outcome": "invented observed command from a module global; static argv is unknown",
    },
    {
        "id": "OriginalF3ReturnedRebound",
        "filename": "returned-rebound.jsonl",
        "sha256": "774e2946d16c23d9ebdd557ccf279143f6d2249dc7132aa567fb34d12d3d7573",
        "expected_kind": "exact",
        "want": [{"class": "host_mutation", "command": "pacman -S r21-b", "evidence": "observed"}],
        "forbid_observed_commands": [],
        "forbid_commands_any_tier": [],
        "require_signal": True,
        "table_row": "F3",
        "r21_observed": [{"class": "package_query", "command": "pacman -Q r21-a", "evidence": "observed"}],
        "r21_outcome": "wrong closure body; host_mutation missing",
    },
    {
        "id": "OriginalF4ThreadRunDirect",
        "filename": "thread-run-direct.jsonl",
        "sha256": "1cc1188dc4e0c37ecba97d34bdf546113d888c62a9cba0bcfe06d44201a2407f",
        "expected_kind": "exact",
        "want": [{"class": "host_mutation", "command": "pacman -S r21-thread-run", "evidence": "observed"}],
        "forbid_observed_commands": [],
        "forbid_commands_any_tier": [],
        "require_signal": True,
        "table_row": "F4",
        "r21_observed": [],
        "r21_outcome": "no row; eval_unparsed and unparsed_spawns both 0",
    },
    {
        "id": "OriginalF5ThreadKeyHygiene",
        "filename": "thread-key-hygiene.jsonl",
        "sha256": "4ea8ccc8724de011e19dcc1e69da1f4078ac74544f554e39ccda66dc42065c9e",
        "expected_kind": "exact",
        "want": [{"class": "package_query", "command": "pacman -Q r21-hyg", "evidence": "observed"}],
        "forbid_observed_commands": [],
        "forbid_commands_any_tier": [],
        "require_signal": True,
        "table_row": "F5",
        "r21_observed": [{"class": "package_query", "command": "pacman -Q r21-hyg", "evidence": "lead"}],
        "r21_outcome": "same command downgraded from observed to lead",
    },
    {
        "id": "OriginalF5ThreadKeyControl",
        "filename": "thread-key-control.jsonl",
        "sha256": "00ecb83fabddfd002d703bc1fbaa449b24e1edf935d0f6792a773c96007162be",
        "expected_kind": "exact",
        "want": [{"class": "package_query", "command": "pacman -Q r21-hyg", "evidence": "observed"}],
        "forbid_observed_commands": [],
        "forbid_commands_any_tier": [],
        "require_signal": True,
        "table_row": "control",
        "r21_observed": [{"class": "package_query", "command": "pacman -Q r21-hyg", "evidence": "observed"}],
        "r21_outcome": "control passed",
    },
    {
        "id": "OriginalR19PureFrozenClosure",
        "path": R19_PURE_PATH,
        "sha256": R19_PURE_SHA256,
        "expected_kind": "exact",
        "want": [],
        "forbid_observed_commands": [],
        "forbid_commands_any_tier": [],
        "require_signal": False,
        "table_row": "round-20 precision / CasePureBuiltins--frozenset-closure",
        "r21_observed": [],
        "r21_outcome": "original pure-data closure; exact empty truth, not remeasured",
    },
)

ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,95}\Z")
ROW_KEYS = {"class", "command", "evidence"}
BASE_REQUIRED = {
    "id", "cells", "expected_kind", "want", "forbid_observed_commands", "rationale", "source"
}
BASE_OPTIONAL = {
    "language", "forbid_commands_any_tier", "require_signal", "accept_exact_want", "cell_reset"
}
ADDENDUM_OPTIONAL = BASE_REQUIRED - {"id", "rationale", "source"} | BASE_OPTIONAL


class ProposalError(ValueError):
    """A proposal cannot be included without changing or guessing its assertions."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number {value}")


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json(raw: bytes) -> object:
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object, parse_constant=reject_constant)


def relative_project(path: Path) -> str:
    return path.relative_to(PROJECT).as_posix()


def checked_strings(value: object, field: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ProposalError(f"{field} must be a list of nonempty strings")
    if len(set(value)) != len(value):
        raise ProposalError(f"{field} must not contain duplicates")
    return list(value)


def validate_want(value: object, field: str = "want") -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise ProposalError(f"{field} must be a list")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(value):
        if not isinstance(row, dict) or set(row) != ROW_KEYS:
            raise ProposalError(f"{field}[{index}] must contain exactly class, command, evidence")
        cls, command, evidence = row["class"], row["command"], row["evidence"]
        if not isinstance(cls, str) or not cls.strip():
            raise ProposalError(f"{field}[{index}].class must be a nonempty string")
        if not isinstance(command, str) or not command.strip():
            raise ProposalError(f"{field}[{index}].command must be a nonempty string")
        if evidence not in ("observed", "lead"):
            raise ProposalError(f"{field}[{index}].evidence must be observed or lead")
        rows.append({"class": cls, "command": command, "evidence": evidence})
    return rows


def sorted_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(rows, key=lambda row: (row["class"], row["command"], row["evidence"]))


def validate_cell_resets(value: object, cell_count: int, field: str = "cell_reset") -> list[bool]:
    if not isinstance(value, list) or len(value) != cell_count or any(type(item) is not bool for item in value):
        raise ProposalError(f"{field} must be a bool list with exactly one entry per cell")
    return list(value)


def validate_base(value: object, filename_id: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProposalError("proposal must be a JSON object")
    keys = set(value)
    if not BASE_REQUIRED <= keys or keys - BASE_REQUIRED - BASE_OPTIONAL:
        missing = sorted(BASE_REQUIRED - keys)
        extra = sorted(keys - BASE_REQUIRED - BASE_OPTIONAL)
        raise ProposalError(f"proposal keys differ (missing={missing}, extra={extra})")
    proposal_id = value["id"]
    if not isinstance(proposal_id, str) or not ID_RE.fullmatch(proposal_id):
        raise ProposalError("id must be a safe ASCII filename stem")
    filename_matches = proposal_id == filename_id or (
        filename_id == "CaptureNestedFactoryCorrected" and proposal_id == "CaptureNestedFactory"
    )
    if not filename_matches:
        raise ProposalError("id must match the proposal filename stem, except the recorded nested-factory correction")
    if proposal_id in {original["id"] for original in ORIGINALS}:
        raise ProposalError("id is reserved for an immutable original")
    cells = value["cells"]
    if not isinstance(cells, list) or not cells or any(not isinstance(cell, str) or not cell.strip() for cell in cells):
        raise ProposalError("cells must be a nonempty list of nonempty inert eval source strings")
    language = value.get("language", "py")
    if language != "py":
        raise ProposalError("only Python eval source cells are accepted")
    expected_kind = value["expected_kind"]
    if expected_kind not in ("exact", "uncertain"):
        raise ProposalError("expected_kind must be exact or uncertain")
    want_input = validate_want(value["want"])
    accept_exact = None
    if "accept_exact_want" in value:
        accept_exact = validate_want(value["accept_exact_want"], "accept_exact_want")
        if expected_kind != "uncertain" or not accept_exact:
            raise ProposalError("accept_exact_want must be a nonempty alternate exact result on an uncertain case")
    forbidden_observed = checked_strings(value["forbid_observed_commands"], "forbid_observed_commands")
    forbidden_any = checked_strings(value.get("forbid_commands_any_tier", []), "forbid_commands_any_tier")
    require_signal = value.get("require_signal", expected_kind == "uncertain" or bool(want_input))
    if type(require_signal) is not bool:
        raise ProposalError("require_signal must be an exact bool")
    resets = validate_cell_resets(value["cell_reset"], len(cells)) if "cell_reset" in value else [False] * len(cells)
    for field in ("rationale", "source"):
        if not isinstance(value[field], str) or not value[field].strip():
            raise ProposalError(f"{field} must be a nonempty string")
    for row in [*want_input, *(accept_exact or [])]:
        if row["command"] in forbidden_any:
            raise ProposalError("a wanted command conflicts with forbid_commands_any_tier")
    return {
        "id": proposal_id,
        "cells": list(cells),
        "cell_reset": resets,
        "expected_kind": expected_kind,
        "want_input_order": want_input,
        "want": sorted_rows(want_input),
        "accept_exact_want": sorted_rows(accept_exact) if accept_exact is not None else None,
        "forbid_observed_commands": forbidden_observed,
        "forbid_commands_any_tier": forbidden_any,
        "require_signal": require_signal,
        "rationale": value["rationale"],
        "source": value["source"],
        "proposal_fields": value,
        "addenda": [],
    }


def validate_addendum(value: object, filename_stem: str, base: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProposalError("addendum must be a JSON object")
    required = {"id", "addendum_to", "rationale", "source"}
    keys = set(value)
    if not required <= keys or keys - required - ADDENDUM_OPTIONAL:
        missing = sorted(required - keys)
        extra = sorted(keys - required - ADDENDUM_OPTIONAL)
        raise ProposalError(f"addendum keys differ (missing={missing}, extra={extra})")
    if value["id"] != filename_stem or value["addendum_to"] != base["id"]:
        raise ProposalError("addendum id or addendum_to does not match its filename and base proposal")
    if not any(key in value for key in ("forbid_commands_any_tier", "require_signal", "accept_exact_want")):
        raise ProposalError("addendum contains no supported expectation constraint")
    for field in ("rationale", "source"):
        if not isinstance(value[field], str) or not value[field].strip():
            raise ProposalError(f"addendum {field} must be a nonempty string")
    if "cells" in value and value["cells"] != base["cells"]:
        raise ProposalError("addendum may not change base source cells")
    if "expected_kind" in value and value["expected_kind"] != base["expected_kind"]:
        raise ProposalError("addendum may not change expected_kind")
    if "want" in value and validate_want(value["want"]) != base["want_input_order"]:
        raise ProposalError("addendum may not change base want rows")
    if "forbid_observed_commands" in value and value["forbid_observed_commands"] != base["forbid_observed_commands"]:
        raise ProposalError("addendum may not change base forbid_observed_commands")
    if "language" in value and value["language"] != base["proposal_fields"].get("language", "py"):
        raise ProposalError("addendum may not change base language")
    if "cell_reset" in value:
        resets = validate_cell_resets(value["cell_reset"], len(base["cells"]))
        if resets != base["cell_reset"]:
            raise ProposalError("addendum may not change base cell_reset")
    add_accept = None
    if "accept_exact_want" in value:
        add_accept = sorted_rows(validate_want(value["accept_exact_want"], "accept_exact_want"))
        if base["accept_exact_want"] is not None and add_accept != base["accept_exact_want"]:
            raise ProposalError("addendum may not replace an existing accept_exact_want")
        if not add_accept:
            raise ProposalError("addendum accept_exact_want must not be empty")
    add_any = checked_strings(value.get("forbid_commands_any_tier", []), "forbid_commands_any_tier")
    add_signal = value.get("require_signal")
    if add_signal is not None and type(add_signal) is not bool:
        raise ProposalError("addendum require_signal must be an exact bool")
    if add_signal is False and base["require_signal"]:
        raise ProposalError("addendum may not weaken require_signal")
    return {"forbid_commands_any_tier": add_any, "require_signal": add_signal, "accept_exact_want": add_accept, "fields": value}


def make_eval_fixture(proposal_id: str, cells: list[str], resets: list[bool]) -> bytes:
    lines = []
    for index, (code, reset) in enumerate(zip(cells, resets, strict=True)):
        call = {
            "type": "toolCall",
            "id": f"{proposal_id}-{index}",
            "name": "eval",
            "arguments": {"language": "py", "code": code, "reset": reset},
        }
        envelope = {"type": "message", "message": {"role": "assistant", "content": [call]}}
        lines.append(json.dumps(envelope, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
    return ("\n".join(lines) + "\n").encode("ascii")


def proposal_inventory() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, bytes]]:
    inventory: dict[str, Any] = {"path": ".ufo/waves/round-22/w1/proposals", "kind": "missing", "entries": []}
    rejected: list[dict[str, Any]] = []
    raw_by_name: dict[str, bytes] = {}
    if not PROPOSALS.exists() and not PROPOSALS.is_symlink():
        rejected.append({"path": inventory["path"], "sha256": None, "reason": "proposal directory is absent"})
        return inventory, rejected, raw_by_name
    if PROPOSALS.is_symlink():
        target_hash = sha256(os.fsencode(os.readlink(PROPOSALS)))
        inventory.update(kind="symlink", link_sha256=target_hash)
        rejected.append({"path": inventory["path"], "sha256": target_hash, "reason": "proposal directory is a symlink"})
        return inventory, rejected, raw_by_name
    if not PROPOSALS.is_dir():
        inventory["kind"] = "other"
        rejected.append({"path": inventory["path"], "sha256": None, "reason": "proposal path is not a directory"})
        return inventory, rejected, raw_by_name

    inventory["kind"] = "directory"
    entries: list[dict[str, Any]] = []
    for path in sorted(PROPOSALS.iterdir(), key=lambda item: item.name):
        try:
            mode = path.lstat().st_mode
        except OSError as error:
            entries.append({"name": path.name, "kind": "unreadable", "error": str(error)})
            rejected.append({"path": f"{inventory['path']}/{path.name}", "sha256": None, "reason": f"cannot inspect proposal entry: {error}"})
            continue
        if stat.S_ISLNK(mode):
            link_hash = sha256(os.fsencode(os.readlink(path)))
            entries.append({"name": path.name, "kind": "symlink", "link_sha256": link_hash})
            rejected.append({"path": f"{inventory['path']}/{path.name}", "sha256": link_hash, "reason": "proposal entries must not be symlinks"})
        elif stat.S_ISREG(mode):
            try:
                raw = path.read_bytes()
            except OSError as error:
                entries.append({"name": path.name, "kind": "unreadable", "error": str(error)})
                rejected.append({"path": f"{inventory['path']}/{path.name}", "sha256": None, "reason": f"cannot read proposal entry: {error}"})
                continue
            digest = sha256(raw)
            entries.append({"name": path.name, "kind": "file", "sha256": digest})
            raw_by_name[path.name] = raw
            if path.suffix != ".json":
                rejected.append({"path": f"{inventory['path']}/{path.name}", "sha256": digest, "reason": "proposal delivery must be a direct .json file"})
        elif stat.S_ISDIR(mode):
            entries.append({"name": path.name, "kind": "directory"})
            rejected.append({"path": f"{inventory['path']}/{path.name}", "sha256": None, "reason": "proposal delivery must be a direct .json file"})
        else:
            entries.append({"name": path.name, "kind": "other"})
            rejected.append({"path": f"{inventory['path']}/{path.name}", "sha256": None, "reason": "proposal entry is not a regular JSON file"})
    inventory["entries"] = entries
    return inventory, rejected, raw_by_name


def source_files_are_pinned() -> None:
    for artifact in SOURCE_ARTIFACTS:
        path = PROJECT / artifact["path"]
        if path.is_symlink() or not path.is_file() or sha256(path.read_bytes()) != artifact["sha256"]:
            raise SystemExit(f"source artifact changed or unavailable: {artifact['path']}")


def main() -> int:
    for path in (INPUTS, EXPECTED, PIN):
        if path.exists() or path.is_symlink():
            raise SystemExit(f"refusing to overwrite existing assembly output: {path}")
    source_files_are_pinned()

    inventory, rejected, raw_by_name = proposal_inventory()
    bases: dict[str, dict[str, Any]] = {}
    base_paths: dict[str, str] = {}
    base_hashes: dict[str, str] = {}
    pending_addenda: list[tuple[str, bytes]] = []
    for name, raw in sorted(raw_by_name.items()):
        if not name.endswith(".json"):
            continue
        try:
            parsed = load_json(raw)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            rejected.append({"path": f"{inventory['path']}/{name}", "sha256": sha256(raw), "reason": str(error)})
            continue
        if name.endswith(".addendum.json"):
            pending_addenda.append((name, raw))
            continue
        if name == "CaptureNestedFactory.json":
            rejected.append({
                "path": proposal_path,
                "sha256": sha256(raw),
                "reason": "ineligible author typo: want says r22-inner but the inert cell passes r22-nest-inner; preserved unchanged and superseded by the separately delivered corrected file",
                "superseded_by": f"{inventory['path']}/CaptureNestedFactoryCorrected.json",
                "correction_report": {
                    "path": ".ufo/waves/round-22/w1/reports/CaptureNestedFactory.md",
                    "sha256": "428cc0553c03f20d82d230094fdeeecbff968d59208ebf2eda7783722f987474",
                },
            })
            continue
        try:
            proposal = validate_base(parsed, Path(name).stem)
        except (ValueError, ProposalError) as error:
            rejected.append({"path": proposal_path, "sha256": sha256(raw), "reason": str(error)})
            continue
        if proposal["id"] in bases:
            rejected.append({"path": proposal_path, "sha256": sha256(raw), "reason": f"duplicate proposal id {proposal['id']}"})
            continue
        bases[proposal["id"]] = proposal
        base_paths[proposal["id"]] = proposal_path
        base_hashes[proposal["id"]] = sha256(raw)

    for name, raw in pending_addenda:
        path = f"{inventory['path']}/{name}"
        digest = sha256(raw)
        try:
            parsed = load_json(raw)
            if not isinstance(parsed, dict):
                raise ProposalError("addendum must be a JSON object")
            target = parsed.get("addendum_to")
            if not isinstance(target, str) or target not in bases:
                raise ProposalError("addendum target is absent or ineligible")
            addendum = validate_addendum(parsed, Path(name).stem, bases[target])
            if "accept_exact_want" in parsed and bases[target]["accept_exact_want"] is None:
                bases[target]["accept_exact_want"] = addendum["accept_exact_want"]
            bases[target]["forbid_commands_any_tier"].extend(addendum["forbid_commands_any_tier"])
            if addendum["require_signal"] is True:
                bases[target]["require_signal"] = True
            bases[target]["addenda"].append({"path": path, "sha256": digest, "fields": addendum["fields"]})
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, ProposalError) as error:
            rejected.append({"path": path, "sha256": digest, "reason": str(error)})

    required_proposals = []
    for proposal_id in REQUIRED_PROPOSALS:
        present = proposal_id in bases
        required_proposals.append({"id": proposal_id, "present": present})
        if not present:
            rejected.append({
                "path": f"{inventory['path']}/{proposal_id}.json",
                "sha256": None,
                "reason": "required corrected proposal was not delivered as an eligible proposal before seal",
            })

    proposal_cases: list[dict[str, Any]] = []
    fixture_payloads: dict[str, bytes] = {}
    for proposal_id, proposal in sorted(bases.items()):
        payload = make_eval_fixture(proposal_id, proposal["cells"], proposal["cell_reset"])
        fixture = f"inputs/{proposal_id}.jsonl"
        if fixture in fixture_payloads:
            rejected.append({"path": base_paths[proposal_id], "sha256": base_hashes[proposal_id], "reason": f"fixture path collision: {fixture}"})
            continue
        fixture_payloads[fixture] = payload
        proposal_cases.append({
            "id": proposal_id,
            "group": "proposal",
        original_path = base_paths[proposal_id]
        correction = None
        if proposal_id == "CaptureNestedFactory" and original_path.endswith("CaptureNestedFactoryCorrected.json"):
            correction = {
                "supersedes": f"{inventory['path']}/CaptureNestedFactory.json",
                "report": {
                    "path": ".ufo/waves/round-22/w1/reports/CaptureNestedFactory.md",
                    "sha256": "428cc0553c03f20d82d230094fdeeecbff968d59208ebf2eda7783722f987474",
                },
                "reason": "corrected source-derived want and rationale; canonical case id retained",
            }
        proposal_cases.append({
            "id": proposal_id,
            "group": "proposal",
            "expected_kind": proposal["expected_kind"],
            "fixture": fixture,
            "sha256": sha256(payload),
            "cell_count": len(proposal["cells"]),
            "cell_reset": proposal["cell_reset"],
            "proposal": {"path": original_path, "sha256": base_hashes[proposal_id]},
            "proposal_fields": proposal["proposal_fields"],
            "proposal_addenda": proposal["addenda"],
"correction": correction,
"source": proposal["source"],
"rationale": proposal["rationale"],
"want_input_order": proposal["want_input_order"],
"want": proposal["want"],
"accept_exact_want": proposal["accept_exact_want"],
"forbid_observed_commands": proposal["forbid_observed_commands"],
"forbid_commands_any_tier": proposal["forbid_commands_any_tier"],
"require_signal": proposal["require_signal"],
        })

    original_cases: list[dict[str, Any]] = []
    for original in ORIGINALS:
        if original["id"] == "OriginalR19PureFrozenClosure":
            source = PROJECT / original["path"]
            source_rel = original["path"]
            truth_basis = "source is a single inert eval assigning a literal frozenset; no process sink is called; exact empty truth retained from the r19 precision fixture"
        else:
            source = ORIGINAL_ROOT / original["filename"]
            source_rel = f".ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/{original['filename']}"
            truth_basis = "FinalBindingReview.md Probe result table; independent static truth, not the prior scanner row"
        if source.is_symlink() or not source.is_file():
            raise SystemExit(f"immutable original fixture is missing or not a regular file: {source}")
        payload = source.read_bytes()
        if sha256(payload) != original["sha256"]:
            raise SystemExit(f"immutable original fixture digest mismatch: {source}")
        fixture = f"inputs/{original['id']}.jsonl"
        if fixture in fixture_payloads:
            raise SystemExit(f"fixture path collision with original: {fixture}")
        fixture_payloads[fixture] = payload
        want = original["want"]
        source_artifact = next(item for item in SOURCE_ARTIFACTS if item["path"] == source_rel)
        original_cases.append({
            "id": original["id"],
            "group": "supplemental-original",
            "expected_kind": original["expected_kind"],
            "fixture": fixture,
            "sha256": original["sha256"],
            "cell_count": 1,
            "cell_reset": [False],
            "proposal": None,
            "proposal_fields": None,
            "proposal_addenda": [],
            "want_input_order": want,
            "want": sorted_rows(want),
            "accept_exact_want": None,
            "forbid_observed_commands": original["forbid_observed_commands"],
            "forbid_commands_any_tier": original["forbid_commands_any_tier"],
            "require_signal": original["require_signal"],
            "truth_provenance": {
                "document": source_rel,
                "document_sha256": source_artifact["sha256"],
                "table_row": original["table_row"],
                "basis": truth_basis,
            },
            "r21_before": {
                "reported_findings": original["r21_observed"],
                "outcome": original["r21_outcome"],
                "authority": "FinalBindingReview.md single round-21 bounded probe report; retained, not rerun",
            },
        })

    proposal_cases.sort(key=lambda case: case["id"])
    cases = proposal_cases + original_cases
    rejected.sort(key=lambda item: (str(item.get("path", "")), str(item.get("reason", ""))))
    expected = {
        "schema": "mado-r22-c1-oracle-v1",
        "comparison": {
            "exact": "strict multiset equality of class, command and evidence; unparsed counters are zero unless require_signal explicitly permits a signal",
            "uncertain": "either nonempty accept_exact_want matches the complete rows with zero unparsed, or no observed rows and the per-case require_signal rule is met",
            "forbidden": "forbid_observed_commands checks observed rows; forbid_commands_any_tier checks every finding regardless of evidence",
            "signal": "a lead row or positive eval_unparsed/unparsed_spawns counter",
            "ordering": "want and accept_exact_want are sorted by class, command, evidence; want_input_order preserves the proposal's exact source order",
            "transcripts": "proposal cells map one-to-one to inert eval tool calls; cell_reset maps one-to-one to arguments.reset; source strings are not executed",
        },
        "limits": {"seconds_per_process": 15, "address_space_bytes": 402653184, "concurrency": 1},
        "source_artifacts": SOURCE_ARTIFACTS,
        "historical_r21_probe": {
            "reported_exit": 1,
            "counts": {"host_mutation": 0, "live_probe": 0, "package_query": 5, "tool_install": 0, "vcs_write": 0},
            "observed_findings": 4,
            "lead_findings": 1,
            "source": REVIEW_REL,
            "source_sha256": REVIEW_SHA256,
            "status": "known-red report retained as context; not rerun and not used to derive the independent truth rows",
        },
        "historical_guard": {
            "name": "round-21 legacy precision 175-case guard",
            "baseline_pass": 166,
            "population_total": 175,
            "required_floor": 166,
            "reset_to_new_target": False,
            "post_integration_runner": "Main owns the whole-175 comparison at the delivered commit; this oracle does not execute it",
            "sources": [
                {"path": ".ufo/waves/round-21/residual/FinalRemovalReview.md", "sha256": "c872a0d4f94ee2e007286cd1ec82b0eb368f63fe35922de9461fb462d4b2522a"},
                {"path": ".ufo/waves/round-21/final-summary.json", "sha256": "e03a2f5a27a1b918e88721b34da38ff872aa8513a70449f37b27119757d9f5d8"},
            ],
        },
        "required_proposals": required_proposals,
        "required_proposal_ids": REQUIRED_PROPOSALS,
        "proposal_inventory": inventory,
        "cases": cases,
        "rejected": rejected,
    }
    expected_bytes = (json.dumps(expected, indent=2, ensure_ascii=True, sort_keys=True) + "\n").encode("ascii")
    expected_hash = sha256(expected_bytes)
    pin_bytes = f"{expected_hash}  expected.json\n".encode("ascii")

    INPUTS.mkdir()
    for relative, payload in sorted(fixture_payloads.items()):
        path = ROOT / relative
        with path.open("xb") as stream:
            stream.write(payload)
    with EXPECTED.open("xb") as stream:
        stream.write(expected_bytes)
    with PIN.open("xb") as stream:
        stream.write(pin_bytes)

    print(json.dumps({
        "proposals": len(proposal_cases),
        "supplemental_originals": len(original_cases),
        "rejected": len(rejected),
        "missing_required": [item["id"] for item in required_proposals if not item["present"]],
        "expected_sha256": expected_hash,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
