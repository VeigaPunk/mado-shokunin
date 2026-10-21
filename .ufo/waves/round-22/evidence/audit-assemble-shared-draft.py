#!/usr/bin/env python3
"""Freeze independent C2 proposals as digest-bound audit inputs; never run a tool."""

import hashlib
import json
import math
import os
import re
import shutil
import tempfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve()
LANE = HERE.parents[4]
OUT = HERE.parent / "fixtures"
PROPOSALS = LANE / ".ufo/waves/round-22/w1/audit-proposals"
HISTORICAL = LANE / ".ufo/waves/round-22/w1/historical-c3.json"
CONTRACT = LANE / ".ufo/waves/round-22/audit-contract.json"
AUTHORITY = LANE / ".ufo/waves/round-22/w1/audit-authority.json"
MAX_PROPOSAL_BYTES = 16 * 1024 * 1024
MAX_SNAPSHOT_BYTES = 2 * 1024 * 1024
MAX_RAW_BYTES = 8 * 1024 * 1024
MAX_ENTRY_BYTES = 16 * 1024 * 1024
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")


class Invalid(ValueError):
    pass


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def reject_constant(value):
    raise Invalid("nonfinite JSON number: " + value)


def finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise Invalid("nonfinite JSON number")
    return number


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid("duplicate JSON key: " + key)
        result[key] = value
    return result


def parse_json(raw, label):
    try:
        text = raw.decode("utf-8")
        if text.startswith("\ufeff"):
            raise Invalid("UTF-8 BOM is not accepted")
        return json.loads(text, object_pairs_hook=unique_object,
                          parse_constant=reject_constant, parse_float=finite_float)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise Invalid(f"{label}: invalid JSON ({type(exc).__name__}: {exc})") from exc


def json_bytes(value):
    try:
        return (json.dumps(value, ensure_ascii=False, allow_nan=False,
                           indent=2, sort_keys=True) + "\n").encode("utf-8")
    except (TypeError, ValueError, RecursionError) as exc:
        raise Invalid("cannot serialize JSON: " + type(exc).__name__) from exc


def within(path, base):
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def read_regular(path, limit, label):
    try:
        info = path.lstat()
    except OSError as exc:
        raise Invalid(f"{label}: unavailable ({exc})") from exc
    if not path.is_absolute() or not path.is_file() or path.is_symlink():
        raise Invalid(f"{label}: not a regular non-symlink file")
    if info.st_size > limit:
        raise Invalid(f"{label}: exceeds {limit} bytes")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise Invalid(f"{label}: unreadable ({exc})") from exc
    if len(raw) != info.st_size:
        raise Invalid(f"{label}: changed while being read")
    return raw


def safe_source_path(value):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise Invalid("provenance source path is not a safe lane path")
    candidate = Path(value)
    if candidate.is_absolute():
        try:
            rel = candidate.relative_to(LANE)
        except ValueError as exc:
            raise Invalid("provenance source escapes the lane") from exc
    else:
        pure = PurePosixPath(value)
        if pure.is_absolute() or any(part in ("", ".", "..") for part in pure.parts):
            raise Invalid("provenance source path is not normalized")
        rel = Path(*pure.parts)
    path = LANE / rel
    if not within(path, LANE):
        raise Invalid("provenance source escapes the lane")
    current = LANE
    for part in rel.parts:
        current = current / part
        try:
            if current.is_symlink():
                raise Invalid("provenance source contains a symlink: " + value)
        except OSError as exc:
            raise Invalid("provenance source is unavailable: " + value) from exc
    if not path.is_file():
        raise Invalid("provenance source is not a regular file: " + value)
    return path, rel.as_posix()


def safe_fixture_rel(value, label):
    if not isinstance(value, str) or not value or "\x00" in value:
        raise Invalid(label + " must be a nonempty FIX-relative path")
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in ("", ".", "..") for part in pure.parts):
        raise Invalid(label + " must not contain absolute, dot, or dot-dot components")
    # Backslash is an ordinary filename byte on this POSIX host; raw path fixtures
    # need it to exercise the audit tool's separate bundle-path rejection.
    return Path(*pure.parts)


def safe_within(path, base, label):
    try:
        resolved = path.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise Invalid(label + " cannot be resolved safely") from exc
    base_resolved = base.resolve(strict=True)
    if not within(resolved, base_resolved):
        raise Invalid(label + " resolves outside its fixture directory")
    return resolved


def copy_input(stage, rel, raw):
    target = stage / safe_fixture_rel(rel, "input destination")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        raise Invalid("duplicate input destination: " + rel)
    target.write_bytes(raw)
    return {"path": PurePosixPath(rel).as_posix(), "sha256": sha(raw),
            "size_bytes": len(raw)}


def normalize_expected(expected, known_ids):
    if not isinstance(expected, dict) or "code" not in expected or "finding_ids" not in expected:
        raise Invalid("expected must contain code and finding_ids")
    code = expected["code"]
    if type(code) is int:
        normalized_code = code
    elif type(code) is str and code in ("0", "1", "2"):
        normalized_code = int(code)
    else:
        raise Invalid("expected.code must be exact int 0|1|2 or exact string '0'|'1'|'2'")
    if normalized_code not in (0, 1, 2):
        raise Invalid("expected.code is outside 0|1|2")
    original_ids = expected["finding_ids"]
    if not isinstance(original_ids, list) or any(type(item) is not str for item in original_ids):
        raise Invalid("expected.finding_ids must be a list of strings")
    unknown = sorted(set(original_ids) - known_ids)
    if unknown:
        raise Invalid("unknown expected finding id(s): " + ", ".join(unknown))
    normalized_ids = sorted(set(original_ids))
    changes = []
    if type(code) is str:
        changes.append({"field": "expected.code", "original": code,
                        "normalized": normalized_code, "reason": "exact verdict string normalized to integer"})
    if original_ids != normalized_ids:
        changes.append({"field": "expected.finding_ids", "original": original_ids,
                        "normalized": normalized_ids,
                        "reason": "finding IDs sorted and duplicate IDs removed"})
    return {"code": normalized_code, "finding_ids": normalized_ids}, changes


def parse_proposal(path, raw):
    proposal = parse_json(raw, path.name)
    if not isinstance(proposal, dict):
        raise Invalid("proposal must be a JSON object")
    for key in ("id", "snapshot", "claim", "expected", "rationale"):
        if key not in proposal:
            raise Invalid("proposal missing required field: " + key)
    if type(proposal["id"]) is not str or not ID_RE.fullmatch(proposal["id"]):
        raise Invalid("proposal id is not a safe unique identifier")
    if not isinstance(proposal["claim"], dict):
        raise Invalid("proposal claim must be an object")
    if type(proposal["rationale"]) is not str or not proposal["rationale"].strip():
        raise Invalid("proposal rationale must be a nonempty string")
    return proposal


def eligibility(proposal):
    value = proposal.get("eligibility", "frozen")
    if value == "frozen":
        return True, "included: proposal declared frozen"
    if type(value) is str and value.startswith("contingent:") and value[len("contingent:"):].strip():
        if proposal.get("id") == "AuditRawSnapshotAtLimit":
            return True, ("included by Main's preimplementation ruling: 2 MiB is inclusive "
                          "(<= 2097152 bytes); original contingent text retained")
        return False, "excluded pending Main ruling; original: " + value
    raise Invalid("eligibility must be 'frozen' or 'contingent: <reason>'")


def apply_padding(raw, pad, target):
    if pad is None:
        return raw
    if not isinstance(pad, dict) or pad.get("target") not in ("snapshot", "bundle"):
        raise Invalid("pad must select snapshot or bundle")
    if pad["target"] != target:
        return raw
    byte = pad.get("byte")
    total = pad.get("total_bytes")
    if type(byte) is not str or len(byte.encode("utf-8")) != 1:
        raise Invalid("pad.byte must encode as exactly one byte")
    if type(total) is not int or total < len(raw):
        raise Invalid("pad.total_bytes must be an integer no smaller than the current input")
    if total > MAX_RAW_BYTES:
        raise Invalid("padded raw input exceeds the fixture size bound")
    return raw + byte.encode("utf-8") * (total - len(raw))


def raw_digest(actual, override):
    if override is None:
        return actual
    if not isinstance(override, dict):
        raise Invalid("digest_override must be an object")
    if "literal" in override:
        value = override["literal"]
        if type(value) is not str:
            raise Invalid("digest_override.literal must be a string")
        return value
    transform = override.get("transform")
    if transform == "upper":
        return actual.upper()
    if transform == "truncate":
        return actual[:63]
    raise Invalid("unsupported digest_override")


def create_case(stage, proposal, proposal_rel, proposal_sha, known_ids,
                provenance=None, case_id=None, claim_override=None,
                expected_override=None, rationale=None):
    case_id = case_id or proposal["id"]
    if not ID_RE.fullmatch(case_id):
        raise Invalid("unsafe case id: " + case_id)
    normalized, changes = normalize_expected(
        expected_override if expected_override is not None else proposal["expected"], known_ids)
    fix = stage / "cases" / case_id
    if fix.exists():
        raise Invalid("duplicate case id: " + case_id)
    fix.mkdir(parents=True)
    root = fix / "root"
    root.mkdir()

    raw_text = proposal.get("raw_snapshot")
    raw_bytes = raw_text is not None
    if raw_bytes:
        if proposal["snapshot"] is not None or type(raw_text) is not str:
            raise Invalid("raw_snapshot text requires snapshot:null")
        snapshot_raw = raw_text.encode("utf-8")
    else:
        if not isinstance(proposal["snapshot"], dict):
            raise Invalid("proposal snapshot must be an object unless raw_snapshot text is supplied")
        snapshot_raw = json_bytes(proposal["snapshot"])
    if len(snapshot_raw) > MAX_RAW_BYTES:
        raise Invalid("snapshot input exceeds the 8 MiB fixture bound")

    pad = proposal.get("pad")
    snapshot_raw = apply_padding(snapshot_raw, pad, "snapshot")
    if len(snapshot_raw) > MAX_RAW_BYTES:
        raise Invalid("padded snapshot exceeds the 8 MiB fixture bound")

    raw_fields = ("setup", "path_overrides", "digest_override", "raw_bundle", "pad")
    raw_mode = raw_bytes or any(proposal.get(key) is not None for key in raw_fields)
    claim = claim_override if claim_override is not None else proposal["claim"]
    snapshot_path = "snapshot.json"
    snapshot_paths = ["root/snapshot.json"]

    if raw_mode:
        setup = proposal.get("setup") or {}
        if not isinstance(setup, dict):
            raise Invalid("setup must be an object")
        mkdir_paths = setup.get("mkdir", [])
        symlinks = setup.get("symlinks", [])
        snapshot_paths = setup.get("snapshot_at", ["root/snapshot.json"])
        if (not isinstance(mkdir_paths, list) or not isinstance(symlinks, list)
                or not isinstance(snapshot_paths, list) or not snapshot_paths):
            raise Invalid("setup.mkdir/symlinks must be lists and snapshot_at nonempty")
        snapshot_paths = [safe_fixture_rel(value, "setup.snapshot_at path").as_posix()
                          for value in snapshot_paths]
        for value in mkdir_paths:
            (fix / safe_fixture_rel(value, "setup.mkdir path")).mkdir(parents=True, exist_ok=True)
        for row in symlinks:
            if (not isinstance(row, dict) or type(row.get("path")) is not str
                    or type(row.get("target")) is not str):
                raise Invalid("each setup.symlinks item needs path and target strings")
            link = fix / safe_fixture_rel(row["path"], "setup.symlinks path")
            link.parent.mkdir(parents=True, exist_ok=True)
            target = row["target"]
            if not target or "\x00" in target:
                raise Invalid("symlink target must be nonempty")
            safe_within(link.parent / target, fix, "symlink target")
            if link.exists() or link.is_symlink():
                if link.is_dir() and not link.is_symlink():
                    try:
                        link.rmdir()
                    except OSError as exc:
                        raise Invalid("symlink path collides with a nonempty directory") from exc
                else:
                    link.unlink()
            os.symlink(target, link)
            safe_within(link, fix, "fixture symlink")

        overrides = proposal.get("path_overrides") or {}
        if not isinstance(overrides, dict):
            raise Invalid("path_overrides must be an object")
        snapshot_path = overrides.get("snapshot", snapshot_path)
        if type(snapshot_path) is not str:
            raise Invalid("path_overrides.snapshot must be a string")
        snapshot_path = snapshot_path.replace("{{ROOT_ABS}}", str(root.resolve()))
        digest_value = raw_digest(sha(snapshot_raw), proposal.get("digest_override"))
        raw_bundle = proposal.get("raw_bundle")
        if raw_bundle is None:
            bundle_raw = json_bytes({"snapshot": snapshot_path, "sha256": digest_value,
                                     "claim": claim})
        else:
            if type(raw_bundle) is not str:
                raise Invalid("raw_bundle must be a string")
            bundle_raw = raw_bundle.replace("{{SNAPSHOT_PATH}}", snapshot_path)
            bundle_raw = bundle_raw.replace("{{SNAPSHOT_SHA256}}", digest_value).encode("utf-8")
        bundle_raw = apply_padding(bundle_raw, pad, "bundle")

        for value in snapshot_paths:
            destination = fix / safe_fixture_rel(value, "setup.snapshot_at path")
            resolved = safe_within(destination, fix, "snapshot destination")
            resolved.parent.mkdir(parents=True, exist_ok=True)
            resolved.write_bytes(snapshot_raw)

        if raw_bundle is None:
            target = Path(snapshot_path)
            if not target.is_absolute():
                target = root / target
            safe_within(target, fix, "bundle snapshot path")
        else:
            try:
                parsed_bundle = parse_json(bundle_raw, "raw bundle")
            except Invalid:
                parsed_bundle = None
            if isinstance(parsed_bundle, dict) and type(parsed_bundle.get("snapshot")) is str:
                target = Path(parsed_bundle["snapshot"])
                if not target.is_absolute():
                    target = root / target
                safe_within(target, fix, "bundle snapshot path")
    else:
        if len(snapshot_raw) > MAX_SNAPSHOT_BYTES:
            raise Invalid("snapshot exceeds the inclusive 2 MiB bound")
        digest_value = sha(snapshot_raw)
        bundle_raw = json_bytes({"snapshot": snapshot_path, "sha256": digest_value,
                                 "claim": claim})
        (root / "snapshot.json").write_bytes(snapshot_raw)

    if len(bundle_raw) > MAX_RAW_BYTES:
        raise Invalid("bundle input exceeds the 8 MiB fixture bound")
    bundle_path = fix / "bundle.json"
    if bundle_path.exists() or bundle_path.is_symlink():
        raise Invalid("bundle.json collides with setup path")
    bundle_path.write_bytes(bundle_raw)
    return {
        "id": case_id,
        "kind": "raw" if raw_mode else "proposal",
        "proposal": proposal_rel,
        "proposal_sha256": proposal_sha,
        "bundle": bundle_path.relative_to(stage).as_posix(),
        "bundle_sha256": sha(bundle_raw),
        "root": root.relative_to(stage).as_posix(),
        "snapshot_sha256": sha(snapshot_raw),
        "bundle_snapshot_path": snapshot_path,
        "expected": normalized,
        "original_expected": (expected_override if expected_override is not None
                              else proposal["expected"]),
        "normalizations": changes,
        "claim": claim,
        "rationale": rationale if rationale is not None else proposal["rationale"],
        "provenance": provenance,
    }


def inventory(stage):
    entries = []

    def visit(directory):
        try:
            children = sorted(os.scandir(directory), key=lambda entry: entry.name)
        except OSError as exc:
            raise Invalid("cannot inventory fixture tree: " + str(exc)) from exc
        for child in children:
            path = Path(child.path)
            rel = path.relative_to(stage).as_posix()
            if child.is_symlink():
                target = os.readlink(path)
                safe_within(path, stage, "fixture symlink")
                entries.append({"path": rel, "kind": "symlink", "target": target})
            elif child.is_dir(follow_symlinks=False):
                entries.append({"path": rel, "kind": "directory"})
                visit(path)
            elif child.is_file(follow_symlinks=False):
                raw = read_regular(path, MAX_ENTRY_BYTES, rel)
                entries.append({"path": rel, "kind": "file", "sha256": sha(raw),
                                "size_bytes": len(raw)})
            else:
                raise Invalid("unsupported fixture filesystem entry: " + rel)

    visit(stage)
    return sorted(entries, key=lambda entry: entry["path"])


def main():
    if OUT.exists() or OUT.is_symlink():
        raise SystemExit("refusing to overwrite existing fixture tree: " + str(OUT))
    contract_raw = read_regular(CONTRACT, 1024 * 1024, "audit-contract.json")
    contract = parse_json(contract_raw, "audit-contract.json")
    try:
        known_ids = set(contract["finding_ids"])
    except (TypeError, KeyError) as exc:
        raise SystemExit("audit-contract.json has no finding_ids inventory") from exc
    if not known_ids or any(type(item) is not str for item in known_ids):
        raise SystemExit("audit-contract.json finding_ids is invalid")
    if not PROPOSALS.is_dir() or PROPOSALS.is_symlink():
        raise SystemExit("audit proposal directory unavailable or symlinked: " + str(PROPOSALS))
    source_paths = sorted(PROPOSALS.glob("*.json"), key=lambda item: item.name)
    if not source_paths and not HISTORICAL.exists():
        raise SystemExit("no C2 proposals are available; refusing to create an empty fixture set")

    with tempfile.TemporaryDirectory(prefix=".audit-assemble-", dir=HERE.parent) as temp:
        stage = Path(temp) / "fixtures"
        stage.mkdir()
        contract_input = copy_input(stage, "inputs/audit-contract.json", contract_raw)
        candidates = []
        rejected = []
        seen_sources = set()
        for path in source_paths:
            rel = path.relative_to(LANE).as_posix()
            if path.is_symlink():
                rejected.append({"proposal": rel, "status": "excluded", "reason": "proposal file is a symlink"})
                continue
            try:
                raw = read_regular(path, MAX_PROPOSAL_BYTES, rel)
                input_ref = copy_input(stage, "inputs/proposals/" + path.name, raw)
                proposal = parse_proposal(path, raw)
                candidates.append({"path": rel, "raw": raw, "proposal": proposal,
                                   "sha256": sha(raw), "input": input_ref})
            except Invalid as exc:
                rejected.append({"proposal": rel, "status": "excluded", "reason": str(exc)})
        historical_raw = None
        historical_input = None
        if HISTORICAL.is_symlink():
            rejected.append({"proposal": HISTORICAL.relative_to(LANE).as_posix(),
                             "status": "excluded", "reason": "historical C3 artifact is a symlink"})
        elif HISTORICAL.exists():
            try:
                historical_raw = read_regular(HISTORICAL, MAX_PROPOSAL_BYTES, "historical-c3.json")
                historical_input = copy_input(stage, "inputs/historical-c3.json", historical_raw)
                historical_proposal = parse_proposal(HISTORICAL, historical_raw)
                candidates.append({"path": HISTORICAL.relative_to(LANE).as_posix(),
                                   "raw": historical_raw, "proposal": historical_proposal,
                                   "sha256": sha(historical_raw), "input": historical_input,
                                   "historical": True})
            except Invalid as exc:
                rejected.append({"proposal": HISTORICAL.relative_to(LANE).as_posix(),
                                 "status": "excluded", "reason": str(exc)})
        else:
            rejected.append({"proposal": HISTORICAL.relative_to(LANE).as_posix(),
                             "status": "not-present", "reason": "no historical C3 translation artifact; no receipt fabricated"})

        counts = {}
        for item in candidates:
            ident = item["proposal"]["id"]
            counts[ident.casefold()] = counts.get(ident.casefold(), 0) + 1
        cases = []
        historical_included = False
        for item in candidates:
            proposal = item["proposal"]
            try:
                if counts[proposal["id"].casefold()] != 1:
                    raise Invalid("duplicate proposal id: " + proposal["id"])
                allowed, reason = eligibility(proposal)
                if not allowed:
                    rejected.append({"proposal": item["path"], "id": proposal["id"],
                                     "proposal_sha256": item["sha256"], "status": "excluded",
                                     "reason": reason})
                    continue
                provenance = None
                if item.get("historical"):
                    # Historical rows are admitted only as an explicitly derived C2
                    # representation with verifiable source provenance. The original
                    # markerless C3 receipt is copied unchanged; its 5/1 interpretation
                    # remains separately attributable to the later verifier source.
                    authority_raw = read_regular(AUTHORITY, 1024 * 1024, "audit-authority.json")
                    authority = parse_json(authority_raw, "audit-authority.json")
                    authority_input = copy_input(stage, "inputs/audit-authority.json", authority_raw)
                    sources = proposal.get("provenance")
                    if not isinstance(sources, dict):
                        raise Invalid("historical C3 translation lacks provenance object")
                    source_rows = sources.get("sources")
                    if not isinstance(source_rows, list):
                        raise Invalid("historical C3 provenance lacks sources list")
                    authority_pins = authority.get("pinned_sources", {})
                    required = {
                        ".ufo/waves/round-19/evidence/final/tw-recall-after.txt": "r19_c3_receipt_after",
                        ".ufo/waves/round-19/evidence/final/tripwire-frozen-scan-classes.txt": "r19_frozen_scan_receipt",
                        "corpus/lessons/round-19-verifier-spotcheck.md": "r19_verifier_spotcheck",
                    }
                    declared = {}
                    for source in source_rows:
                        if not isinstance(source, dict):
                            raise Invalid("historical provenance source is not an object")
                        source_path, source_rel = safe_source_path(source.get("path"))
                        source_digest = source.get("sha256")
                        if type(source_digest) is not str or not re.fullmatch(r"[0-9a-f]{64}", source_digest):
                            raise Invalid("historical provenance has an invalid SHA-256")
                        source_raw = read_regular(source_path, MAX_ENTRY_BYTES, source_rel)
                        actual = sha(source_raw)
                        if actual != source_digest:
                            raise Invalid("historical provenance digest mismatch: " + source_rel)
                        declared[source_rel] = source_digest
                        copy_input(stage, "inputs/provenance/" + source_rel, source_raw)
                    for source_rel, authority_key in required.items():
                        pin = authority_pins.get(authority_key)
                        if not isinstance(pin, dict) or pin.get("path") != source_rel:
                            raise Invalid("audit-authority does not pin required historical source " + source_rel)
                        digest = pin.get("sha256")
                        if type(digest) is not str or declared.get(source_rel) != digest:
                            raise Invalid("historical derivation provenance omits a pinned source: " + source_rel)
                    provenance = {"artifact": item["path"], "artifact_sha256": item["sha256"],
                                  "authority": authority_input, "sources": source_rows}
                    expected_rows = sources.get("original_rows")
                    receipt_raw = (LANE / ".ufo/waves/round-19/evidence/final/tw-recall-after.txt").read_bytes()
                    receipt_text = receipt_raw.decode("utf-8")
                    lines = receipt_text.splitlines()
                    start = next((i for i, line in enumerate(lines) if line.strip().startswith("{")), None)
                    end = next((i for i in range(len(lines) - 1, -1, -1) if lines[i].strip() == "}"), None)
                    if start is None or end is None or end < start:
                        raise Invalid("historical C3 source receipt has no JSON body")
                    receipt = parse_json(("\n".join(lines[start:end + 1]) + "\n").encode(),
                                         "historical C3 source receipt")
                    if expected_rows != receipt.get("rows"):
                        raise Invalid("historical translation did not preserve original C3 rows verbatim")
                    findings = proposal["snapshot"].get("findings") if isinstance(proposal["snapshot"], dict) else None
                    if not isinstance(findings, list) or len(findings) != 6:
                        raise Invalid("historical translation is not a six-row line-level snapshot")
                    finding_keys = set()
                    for finding in findings:
                        if not isinstance(finding, dict):
                            raise Invalid("historical finding row is not an object")
                        key = (finding.get("file"), finding.get("line"))
                        if key in finding_keys:
                            raise Invalid("historical translation has duplicate incident rows")
                        finding_keys.add(key)
                        if type(finding.get("file")) is not str or type(finding.get("line")) is not int:
                            raise Invalid("historical finding row lacks source file/line identity")
                    receipt_keys = {(row.get("file"), row.get("line")) for row in receipt.get("rows", [])}
                    if finding_keys != receipt_keys:
                        raise Invalid("historical translation changes the six incident row identities")
                    lead_keys = {(row.get("file"), row.get("line")) for row in findings
                                 if row.get("evidence") == "lead"}
                    observed_keys = {(row.get("file"), row.get("line")) for row in findings
                                     if row.get("evidence") == "observed"}
                    if lead_keys != {("inputs/r13-root.jsonl", 4)} or len(observed_keys) != 5:
                        raise Invalid("historical 5-observed/1-lead classification differs from cited verifier source")
                    cases.append(create_case(stage, proposal, item["path"], item["sha256"],
                                             known_ids, provenance=provenance))
                    historical_included = True
                    corrected_claim = dict(proposal["claim"])
                    files = proposal["snapshot"]["files"]
                    if not isinstance(files, list) or not files:
                        raise Invalid("historical translated snapshot has no file population")
                    errors = 0
                    for file_row in files:
                        if not isinstance(file_row, dict):
                            raise Invalid("historical file row is not an object")
                        for field in ("eval_unparsed", "unparsed_spawns"):
                            value = file_row.get(field)
                            if type(value) is not int or value < 0:
                                raise Invalid("historical file counters are not nonnegative exact ints")
                            errors += value
                    corrected_claim.update(total=6, observed=5, lead=1, errors=errors,
                                           clean=(len(findings) == 0 and errors == 0))
                    corrected_expected = {"code": 0, "finding_ids": ["evidence_audit_clean"]}
                    cases.append(create_case(stage, proposal, item["path"], item["sha256"],
                                             known_ids, provenance=provenance,
                                             case_id="historical-c3-corrected",
                                             claim_override=corrected_claim,
                                             expected_override=corrected_expected,
                                             rationale_suffix=" Corrected companion claim is derived from the verified 5-observed/1-lead translation and contract arithmetic; the original markerless receipt remains unmodified."))
                else:
                    cases.append(create_case(stage, proposal, item["path"], item["sha256"], known_ids,
                                             provenance={"source": item["input"]}))
            except Invalid as exc:
                rejected.append({"proposal": item["path"], "id": proposal.get("id"),
                                 "proposal_sha256": item["sha256"], "status": "excluded",
                                 "reason": str(exc)})
                case_dir = stage / "cases" / proposal.get("id", "")
                if case_dir.exists() and within(case_dir, stage / "cases"):
                    shutil.rmtree(case_dir)
                if proposal.get("id") == "historical-c3":
                    historical_included = False

        entries = inventory(stage)
        expected = {
            "schema": "mado-r22-audit-fixtures-v1",
            "contract": contract_input,
            "limits": {"seconds_per_child": 15, "address_space_bytes": 402653184,
                       "output_bytes_per_stream": 1048576, "concurrency": 1},
            "cases": sorted(cases, key=lambda case: case["id"]),
            "excluded": rejected,
            "historical_c3_included": historical_included,
            "input_entries": entries,
            "scope": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion",
        }
        expected_raw = json_bytes(expected)
        (stage / "expected.json").write_bytes(expected_raw)
        (stage / "expected.sha256").write_text(sha(expected_raw) + "  expected.json\n", encoding="ascii")
        os.rename(stage, OUT)
        print(json.dumps({"fixtures": len(cases), "excluded": len(rejected),
                          "historical_c3_included": historical_included,
                          "expected_sha256": sha(expected_raw)}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Invalid, OSError) as exc:
        raise SystemExit("assembly refused: " + str(exc)) from exc
