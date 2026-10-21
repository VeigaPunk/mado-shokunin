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
LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
OUT = HERE.parent / "fixtures"
PROPOSALS = LANE / ".ufo/waves/round-22/w1/audit-proposals"
HISTORICAL = LANE / ".ufo/waves/round-22/w1/historical-c3.json"
CONTRACT = LANE / ".ufo/waves/round-22/audit-contract.json"
TRUTH_SEAL = LANE / ".ufo/waves/round-22/truth-seal.json"
MAX_PROPOSAL_BYTES = 16 * 1024 * 1024
MAX_SNAPSHOT_BYTES = 2 * 1024 * 1024
MAX_RAW_BYTES = 8 * 1024 * 1024
MAX_ENTRY_BYTES = 16 * 1024 * 1024
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
SHA_RE = re.compile(r"[0-9a-f]{64}\Z")
GIT_SHOW_RE = re.compile(r"git show [0-9a-f]{40}:(.+)\Z")


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


def canonical_json_bytes(value):
    try:
        return json.dumps(value, ensure_ascii=False, allow_nan=False,
                          sort_keys=True, separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError, RecursionError) as exc:
        raise Invalid("cannot canonicalize JSON: " + type(exc).__name__) from exc


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
    match = GIT_SHOW_RE.fullmatch(value)
    if match:
        value = match.group(1)
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
        if current.is_symlink():
            raise Invalid("provenance source contains a symlink: " + value)
    if not path.is_file():
        raise Invalid("provenance source is not a regular file: " + value)
    return path, rel.as_posix()


def safe_fixture_rel(value, label):
    if not isinstance(value, str) or not value or "\x00" in value:
        raise Invalid(label + " must be a nonempty FIX-relative path")
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in ("", ".", "..") for part in pure.parts):
        raise Invalid(label + " must not contain absolute, dot, or dot-dot components")
    # Backslash is a filename byte on this POSIX host. Raw bundle-path fixtures
    # deliberately use such a name while the audited tool must reject that path.
    return Path(*pure.parts)


def safe_within(path, base, label):
    try:
        resolved = path.resolve(strict=False)
        base_resolved = base.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise Invalid(label + " cannot be resolved safely") from exc
    if not within(resolved, base_resolved):
        raise Invalid(label + " resolves outside its fixture directory")
    return resolved


def copy_input(stage, rel, raw):
    target = stage / safe_fixture_rel(rel, "input destination")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        if target.is_symlink() or not target.is_file():
            raise Invalid("duplicate non-file input destination: " + rel)
        existing = read_regular(target, MAX_ENTRY_BYTES, rel)
        if existing != raw:
            raise Invalid("input destination reused for different bytes: " + rel)
        return {"path": PurePosixPath(rel).as_posix(), "sha256": sha(raw),
                "size_bytes": len(raw)}
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
                        "normalized": normalized_code,
                        "reason": "exact verdict string normalized to integer"})
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
    original = proposal.get("eligibility", "frozen")
    if original == "frozen":
        return True, original, "included: proposal declared frozen"
    if type(original) is str and original.startswith("contingent:") and original[len("contingent:"):].strip():
        if proposal.get("id") == "AuditRawSnapshotAtLimit":
            return True, original, ("included by Main's preimplementation ruling: 2 MiB is inclusive "
                                    "(<= 2097152 bytes); original contingent text retained")
        return False, original, "excluded pending Main ruling; original contingent text retained"
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
        if type(override["literal"]) is not str:
            raise Invalid("digest_override.literal must be a string")
        return override["literal"]
    transform = override.get("transform")
    if transform == "upper":
        return actual.upper()
    if override.get("truncate") == 63:
        return actual[:63]
    raise Invalid("unsupported digest_override")


def create_case(stage, proposal, proposal_rel, proposal_sha, known_ids,
                provenance=None, case_id=None, rationale=None, kind_override=None,
                source_pointer=None, claim_kind=None):
    case_id = case_id or proposal["id"]
    if not ID_RE.fullmatch(case_id):
        raise Invalid("unsafe case id: " + case_id)
    normalized, changes = normalize_expected(proposal["expected"], known_ids)
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
    claim = proposal["claim"]
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
        "kind": kind_override or ("raw" if raw_mode else "proposal"),
        "proposal": proposal_rel,
        "proposal_sha256": proposal_sha,
        "bundle": bundle_path.relative_to(stage).as_posix(),
        "bundle_sha256": sha(bundle_raw),
        "root": root.relative_to(stage).as_posix(),
        "snapshot_sha256": sha(snapshot_raw),
        "snapshot_files": [(fix / safe_fixture_rel(value, "snapshot file")).relative_to(stage).as_posix()
                           for value in snapshot_paths],
        "bundle_snapshot_path": snapshot_path,
        "expected": normalized,
        "original_expected": proposal["expected"],
        "normalizations": changes,
        "claim": claim,
        "rationale": rationale if rationale is not None else proposal["rationale"],
        "provenance": provenance,
        "source_pointer": source_pointer,
        "claim_kind": claim_kind,
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


def collect_source_refs(value, found):
    if isinstance(value, dict):
        source_path = value.get("path")
        source_sha = value.get("sha256")
        if source_sha is None:
            source_sha = value.get("sha256_at_eda932e")
        if isinstance(source_path, str) and isinstance(source_sha, str):
            if not SHA_RE.fullmatch(source_sha):
                raise Invalid("historical provenance includes a malformed source digest")
            path, rel = safe_source_path(source_path)
            previous = found.get(rel)
            if previous is not None and previous[0] != source_sha:
                raise Invalid("historical provenance has conflicting pins for " + rel)
            found[rel] = (source_sha, path)
        for child in value.values():
            collect_source_refs(child, found)
    elif isinstance(value, list):
        for child in value:
            collect_source_refs(child, found)


def embedded_json(raw, label):
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise Invalid(label + " is not UTF-8") from exc
    starts = [i for i, line in enumerate(lines) if line.lstrip().startswith("{")]
    for start in starts:
        for end in range(start, len(lines)):
            if lines[end].rstrip().endswith("}"):
                candidate = ("\n".join(lines[start:end + 1]) + "\n").encode("utf-8")
                try:
                    result = parse_json(candidate, label)
                except Invalid:
                    continue
                if isinstance(result, dict):
                    return result
    raise Invalid(label + " has no complete JSON object")


def make_derived_case(stage, history, history_path, history_sha, source_info,
                      known_ids, case_id, snapshot, claim, expected, rationale,
                      source_pointer, claim_kind=None):
    proposal = {"id": case_id, "snapshot": snapshot, "claim": claim,
                "expected": expected, "rationale": rationale or history["rationale"]}
    case = create_case(stage, proposal, history_path, history_sha, known_ids,
                       provenance=source_info, case_id=case_id,
                       rationale=proposal["rationale"], kind_override="historical-derived",
                       source_pointer=source_pointer, claim_kind=claim_kind)
    case["claim_kind"] = claim_kind or "Derived historical C3 comparison; not an r19 claim"
    return case

def validate_historical(stage, item, known_ids):
    cases = []
    history = item["proposal"]
    derivation = history.get("derivation_provenance")
    if not isinstance(derivation, dict):
        raise Invalid("historical C3 translation lacks derivation_provenance")
    found = {}
    for key in ("sources", "derivation_provenance", "attribution_correction"):
        if key in history:
            collect_source_refs(history[key], found)
    if not found:
        raise Invalid("historical C3 translation has no path-and-digest source provenance")

    required = {
        ".ufo/waves/round-19/evidence/final/tripwire-frozen-scan-classes.txt":
            "64648ccad1f2c872d62026f530ee535624b03268e454ffd1ab8437ab2d0cf857",
        ".ufo/waves/round-19/evidence/final/tw-recall-after.txt":
            "8ff13d23d3ffeab946a301a3457360edc3abf52ea833611ac2a0d6bda48ec1c1",
        ".ufo/waves/round-20/evidence/recall-split-final.txt":
            "5165b72878feec8c67e20a0ab079db0aaaea358258b8a62fbb965dd91a6df0a2",
        ".ufo/waves/round-20/evidence/recall-split-1f7f995.txt":
            "7928e3fa02d882fbc3a92b3ca601e5e1cee4985677dbfd028fd48178c1eb14c2",
        ".ufo/waves/round-18/frozen/expected.json":
            "4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9",
        "corpus/lessons/round-19-verifier-spotcheck.md":
            "dcb7a9134022e010ef357a095ded13d15d6f77a9090dc2976f0c9d8090fea0a0",
    }
    for rel, expected_sha in required.items():
        pin = found.get(rel)
        if pin is None or pin[0] != expected_sha:
            raise Invalid("historical provenance omits required source pin: " + rel)

    provenance_inputs = []
    source_bytes = {}
    for rel, (expected_sha, path) in sorted(found.items()):
        raw = read_regular(path, MAX_ENTRY_BYTES, rel)
        if sha(raw) != expected_sha:
            raise Invalid("historical source digest mismatch: " + rel)
        source_bytes[rel] = raw
        provenance_inputs.append(copy_input(stage, "inputs/provenance/" + rel, raw))

    raw_rel = ".ufo/waves/round-19/evidence/final/tripwire-frozen-scan-classes.txt"
    counter_rel = ".ufo/waves/round-19/evidence/final/tw-recall-after.txt"
    raw_scan = embedded_json(source_bytes[raw_rel], "original r19 scan receipt")
    raw_findings = raw_scan.get("findings")
    if not isinstance(raw_findings, list) or len(raw_findings) != 11:
        raise Invalid("original r19 scan receipt is not the recorded 11-row markerless result")
    projected = []
    required_row_keys = ("file", "line", "class", "rule", "command", "tool", "tool_call_id")
    for index, row in enumerate(raw_findings):
        if not isinstance(row, dict) or any(key not in row for key in required_row_keys):
            raise Invalid("original r19 scan row lacks required raw fields")
        if "evidence" in row:
            raise Invalid("original r19 scan receipt was not markerless")
        projected.append({key: row[key] for key in required_row_keys} | {"i": index})
    original = history.get("original_rows")
    if not isinstance(original, dict) or original.get("rows") != projected:
        raise Invalid("historical translation does not preserve the original markerless scan rows")

    raw_counter = embedded_json(source_bytes[counter_rel], "original r19 C3 counter receipt")
    counter_rows = raw_counter.get("rows")
    if (raw_counter.get("incident_lines") != 6 or raw_counter.get("detected") != 6
            or not isinstance(counter_rows, list) or len(counter_rows) != 6
            or any(not isinstance(row, dict) or row.get("detected") is not True
                   for row in counter_rows)):
        raise Invalid("original r19 C3 counter receipt does not report the frozen six detected lines")
    if any(type(row.get("file")) is not str or type(row.get("line")) is not int
           for row in counter_rows):
        raise Invalid("original r19 C3 counter receipt has invalid incident identities")
    incident_keys = {(row["file"], row["line"]) for row in counter_rows}
    if len(incident_keys) != 6:
        raise Invalid("original r19 C3 counter receipt has duplicate incident identities")

    derived = history.get("derived_audit_inputs")
    if not isinstance(derived, dict):
        raise Invalid("historical C3 translation lacks derived_audit_inputs")
    d1 = derived.get("D1_row_level_with_later_markers")
    d2 = derived.get("D2_six_row_line_aggregate_with_later_markers")
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        raise Invalid("historical C3 D1/D2 derived inputs are absent")
    d1_snapshot = d1.get("snapshot")
    d2_snapshot = d2.get("snapshot")
    if not isinstance(d1_snapshot, dict) or not isinstance(d2_snapshot, dict):
        raise Invalid("historical C3 D1/D2 snapshots are malformed")
    if sha(canonical_json_bytes(d1_snapshot)) != d1.get("canonical_sha256"):
        raise Invalid("historical C3 D1 canonical digest mismatch")
    if sha(canonical_json_bytes(d2_snapshot)) != d2.get("canonical_sha256"):
        raise Invalid("historical C3 D2 canonical digest mismatch")
    if history.get("snapshot") != d2_snapshot:
        raise Invalid("top-level historical snapshot differs from its D2 derived input")
    if sha(canonical_json_bytes(history.get("snapshot"))) != history.get("snapshot_canonical_sha256"):
        raise Invalid("top-level historical snapshot canonical digest mismatch")
    if history.get("claim") != {"total": 6, "observed": 5, "lead": 1,
                                "errors": 0, "clean": False}:
        raise Invalid("historical C3 claim is not the explicit derived 5/1 claim")
    if history.get("expected") != {"code": 0, "finding_ids": ["evidence_audit_clean"]}:
        raise Invalid("historical C3 expected verdict differs from the sealed derived claim")

    split_rel = ".ufo/waves/round-20/evidence/recall-split-final.txt"
    split = embedded_json(source_bytes[split_rel], "later C3 split authority")
    expected_totals = {"detected_observed": 5, "detected_lead": 1,
                       "detected_unmarked": 0, "undetected": 0}
    expected_finding_totals = {"observed": 10, "lead": 1, "unmarked": 0}
    split_rows = split.get("rows")
    if (split.get("schema") != "mado-tw-recall-split-r20-v1"
            or split.get("incident_lines") != 6
            or split.get("totals") != expected_totals
            or split.get("finding_totals") != expected_finding_totals
            or not isinstance(split_rows, list) or len(split_rows) != 6):
        raise Invalid("later C3 split authority does not report the sealed 5/1 line split")
    marker_by_row = {}
    split_line_markers = {}
    for line_row in split_rows:
        if (not isinstance(line_row, dict) or type(line_row.get("file")) is not str
                or type(line_row.get("line")) is not int
                or not isinstance(line_row.get("findings"), list)):
            raise Invalid("later C3 split row is malformed")
        line_key = (line_row["file"], line_row["line"])
        markers = set()
        for finding in line_row["findings"]:
            if (not isinstance(finding, dict) or type(finding.get("class")) is not str
                    or type(finding.get("rule")) is not str
                    or finding.get("evidence") not in ("observed", "lead")):
                raise Invalid("later C3 split finding is malformed")
            key = (line_row["file"], line_row["line"], finding["class"], finding["rule"])
            if key in marker_by_row:
                raise Invalid("later C3 split authority repeats a finding key")
            marker_by_row[key] = finding["evidence"]
            markers.add(finding["evidence"])
        if len(markers) != 1:
            raise Invalid("later C3 split authority assigns multiple tiers to one incident line")
        split_line_markers[line_key] = next(iter(markers))
    if set(split_line_markers) != incident_keys:
        raise Invalid("later C3 split authority changes the six incident lines")
    source_keys = []
    expected_d1 = []
    groups = {}
    for index, row in enumerate(raw_findings):
        key = (row["file"], row["line"], row["class"], row["rule"])
        evidence = marker_by_row.get(key)
        if evidence is None:
            raise Invalid("later C3 split authority does not cover an original finding row")
        source_keys.append(key)
        expected_d1.append({"file": row["file"], "line": row["line"],
                            "class": row["class"], "rule": row["rule"],
                            "command": row["command"], "evidence": evidence})
        line_key = (row["file"], row["line"])
        group = groups.setdefault(line_key, {"classes": set(), "commands": [],
                                             "evidence": set(), "indices": []})
        group["classes"].add(row["class"])
        if row["command"] not in group["commands"]:
            group["commands"].append(row["command"])
        group["evidence"].add(evidence)
        group["indices"].append(index)
    if len(set(source_keys)) != 11 or set(source_keys) != set(marker_by_row):
        raise Invalid("later C3 split authority is not a unique 1:1 join over original scan rows")

    raw_files = raw_scan.get("files")
    if not isinstance(raw_files, list) or not raw_files:
        raise Invalid("original r19 scan receipt has no file counter population")
    expected_files = []
    for row in raw_files:
        if (not isinstance(row, dict) or type(row.get("path")) is not str
                or any(type(row.get(field)) is not int or row[field] < 0
                       for field in ("eval_unparsed", "unparsed_spawns"))):
            raise Invalid("original r19 scan file counter row is malformed")
        expected_files.append({"path": row["path"], "eval_unparsed": row["eval_unparsed"],
                               "unparsed_spawns": row["unparsed_spawns"]})
    expected_d2 = []
    for line_key in sorted(groups):
        group = groups[line_key]
        if len(group["evidence"]) != 1:
            raise Invalid("original scan rows on one line have inconsistent later evidence tiers")
        expected_d2.append({"file": line_key[0], "line": line_key[1],
                            "class": ",".join(sorted(group["classes"])),
                            "command": " ; ".join(group["commands"]),
                            "evidence": next(iter(group["evidence"])),
                            "source_row_indices": group["indices"]})
    d1_findings, d2_findings = d1_snapshot.get("findings"), d2_snapshot.get("findings")
    if d1_findings != expected_d1 or d1_snapshot.get("files") != expected_files:
        raise Invalid("historical D1 is not a faithful row-level derivation")
    if d2_findings != expected_d2 or d2_snapshot.get("files") != expected_files:
        raise Invalid("historical D2 is not a faithful line-level derivation")

    markerless = {
        "findings": [{key: value for key, value in row.items() if key != "evidence"}
                     for row in d1_findings],
        "files": d1_snapshot.get("files"),
    }
    markerless_meta = derived.get("A_original_projection_markerless")
    if not isinstance(markerless_meta, dict) or sha(canonical_json_bytes(markerless)) != markerless_meta.get("canonical_sha256"):
        raise Invalid("historical markerless projection digest mismatch")

    source_info = {
        "artifact": item["path"],
        "artifact_sha256": item["sha256"],
        "source_files": provenance_inputs,
        "r19_original_claim": history.get("attribution_correction", {}).get("r19_actual_claim"),
        "derivation_kind": derivation.get("kind"),
        "original_receipt_unchanged": True,
        "derived_snapshot_status": derived.get("status"),
    }
    primary = create_case(stage, history, item["path"], item["sha256"], known_ids,
                          provenance=source_info, kind_override="historical-derived",
                          source_pointer="#/snapshot")
    primary["claim_kind"] = "Derived six-row historical C3 view; not original r19 output or claim"
    cases.append(primary)

    def select_snapshot(pointer, supplied_sha=None):
        if pointer == "#/snapshot":
            snapshot = history["snapshot"]
        elif pointer == "#/derived_audit_inputs/D1_row_level_with_later_markers/snapshot":
            snapshot = d1_snapshot
        elif pointer == "#/derived_audit_inputs/D2_six_row_line_aggregate_with_later_markers/snapshot":
            snapshot = d2_snapshot
        elif pointer.startswith("#/derived_audit_inputs/A_original_projection_markerless"):
            snapshot = markerless
        else:
            raise Invalid("unsupported historical snapshot pointer: " + pointer)
        if supplied_sha is not None and sha(canonical_json_bytes(snapshot)) != supplied_sha:
            raise Invalid("historical companion snapshot digest mismatch")
        return snapshot

    for companion in history.get("companion_proposals", []):
        if not isinstance(companion, dict):
            raise Invalid("historical companion proposal is not an object")
        pointer = companion.get("snapshot_pointer")
        snapshot = select_snapshot(pointer, companion.get("snapshot_canonical_sha256"))
        cases.append(make_derived_case(
            stage, history, item["path"], item["sha256"], source_info, known_ids,
            companion["id"], snapshot, companion["claim"], companion["expected"],
            companion.get("rationale", history["rationale"]), pointer,
            companion.get("claim_kind", "Derived historical C3 comparison; not an r19 claim")))

    for key, pointer in (("D1_row_level_with_later_markers", "#/derived_audit_inputs/D1_row_level_with_later_markers/snapshot"),
                         ("D2_six_row_line_aggregate_with_later_markers", "#/derived_audit_inputs/D2_six_row_line_aggregate_with_later_markers/snapshot")):
        parent = derived[key]
        for nested in parent.get("cases", []):
            if not isinstance(nested, dict):
                raise Invalid("historical derived case is not an object")
            case_id = "HistoricalC3." + key.split("_")[0] + "." + nested["id"]
            rationale = nested.get("rationale", nested.get("claim_basis", history["rationale"]))
            claim_kind = nested.get("claim_kind", nested.get(
                "claim_basis", "Derived historical C3 comparison; not an r19 claim"))
            cases.append(make_derived_case(
                stage, history, item["path"], item["sha256"], source_info, known_ids,
                case_id, parent["snapshot"], nested["claim"], nested["expected"],
                rationale, pointer, claim_kind))
    return cases


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


def verify_truth_seal(raw, seal):
    if not isinstance(seal, dict) or seal.get("schema") != "mado-r22-independent-truth-seal-v1":
        raise Invalid("raw truth seal has an unknown schema")
    if seal.get("base_commit") != "741122d177ae8ff68a73768777f20484d5bdcbe4":
        raise Invalid("raw truth seal names an unexpected registration base")
    files = seal.get("files")
    if not isinstance(files, list) or len(files) != 106:
        raise Invalid("raw truth seal must contain the sealed 106-file population")
    seen = set()
    verified = []
    for row in files:
        if not isinstance(row, dict):
            raise Invalid("raw truth seal file row is not an object")
        path_text, wanted, size = row.get("path"), row.get("sha256"), row.get("bytes")
        if (type(path_text) is not str or type(wanted) is not str or not SHA_RE.fullmatch(wanted)
                or type(size) is not int or size < 0):
            raise Invalid("raw truth seal file row has invalid path, digest, or size")
        path, rel = safe_source_path(path_text)
        if rel in seen:
            raise Invalid("raw truth seal repeats path: " + rel)
        seen.add(rel)
        data = read_regular(path, MAX_ENTRY_BYTES, rel)
        if len(data) != size or sha(data) != wanted:
            raise Invalid("raw truth seal source mismatch: " + rel)
        verified.append({"path": rel, "sha256": wanted, "bytes": size})
    sealed_proposals = {row["path"] for row in verified
                        if row["path"].startswith(".ufo/waves/round-22/w1/audit-proposals/")}
    if len(sealed_proposals) != 35:
        raise Invalid("raw truth seal does not include all 35 C2 proposals")
    historical = ".ufo/waves/round-22/w1/historical-c3.json"
    if historical not in seen:
        raise Invalid("raw truth seal does not include historical C3 evidence")
    return verified, sealed_proposals


def main():
    if OUT.exists() or OUT.is_symlink():
        raise SystemExit("refusing to overwrite existing fixture tree: " + str(OUT))
    truth_raw = read_regular(TRUTH_SEAL, MAX_PROPOSAL_BYTES, "truth-seal.json")
    truth = parse_json(truth_raw, "truth-seal.json")
    truth_files, sealed_proposals = verify_truth_seal(truth_raw, truth)
    if not PROPOSALS.is_dir() or PROPOSALS.is_symlink():
        raise SystemExit("audit proposal directory unavailable or symlinked: " + str(PROPOSALS))
    source_paths = sorted(PROPOSALS.glob("*.json"), key=lambda item: item.name)
    actual_proposals = {path.relative_to(LANE).as_posix() for path in source_paths}
    if actual_proposals != sealed_proposals:
        raise SystemExit("audit proposal paths differ from the committed raw truth seal")
    sealed_hashes = {row["path"]: row["sha256"] for row in truth_files}
    if HISTORICAL.is_symlink() or not HISTORICAL.is_file():
        raise SystemExit("sealed historical C3 artifact is unavailable or symlinked")

    contract_raw = read_regular(CONTRACT, 1024 * 1024, "audit-contract.json")
    if sha(contract_raw) != sealed_hashes[".ufo/waves/round-22/audit-contract.json"]:
        raise SystemExit("audit contract differs from the raw truth seal")
    contract = parse_json(contract_raw, "audit-contract.json")
    try:
        known_ids = set(contract["finding_ids"])
    except (TypeError, KeyError) as exc:
        raise SystemExit("audit-contract.json has no finding_ids inventory") from exc
    if not known_ids or any(type(item) is not str for item in known_ids):
        raise SystemExit("audit-contract.json finding_ids is invalid")

    with tempfile.TemporaryDirectory(prefix=".audit-assemble-", dir=HERE.parent) as temp:
        stage = Path(temp) / "fixtures"
        stage.mkdir()
        truth_input = copy_input(stage, "inputs/truth-seal.json", truth_raw)
        contract_input = copy_input(stage, "inputs/audit-contract.json", contract_raw)
        candidates = []
        excluded = []
        eligibility_log = []
        for path in source_paths:
            rel = path.relative_to(LANE).as_posix()
            raw = read_regular(path, MAX_PROPOSAL_BYTES, rel)
            if sha(raw) != sealed_hashes.get(rel):
                raise SystemExit("audit proposal differs from raw truth seal: " + rel)
            ref = copy_input(stage, "inputs/proposals/" + path.name, raw)
            try:
                proposal = parse_proposal(path, raw)
                candidates.append({"path": rel, "proposal": proposal, "sha256": sha(raw),
                                   "input": ref, "historical": False})
            except Invalid as exc:
                excluded.append({"proposal": rel, "status": "excluded", "reason": str(exc)})

        historical_rel = HISTORICAL.relative_to(LANE).as_posix()
        historical_raw = read_regular(HISTORICAL, MAX_PROPOSAL_BYTES, "historical-c3.json")
        if sha(historical_raw) != sealed_hashes.get(historical_rel):
            raise SystemExit("historical C3 artifact differs from raw truth seal")
        historical_ref = copy_input(stage, "inputs/historical-c3.json", historical_raw)
        try:
            historical_proposal = parse_proposal(HISTORICAL, historical_raw)
            candidates.append({"path": historical_rel, "proposal": historical_proposal,
                               "sha256": sha(historical_raw), "input": historical_ref,
                               "historical": True})
        except Invalid as exc:
            excluded.append({"proposal": historical_rel, "status": "excluded", "reason": str(exc)})

        counts = {}
        for item in candidates:
            ident = item["proposal"]["id"].casefold()
            counts[ident] = counts.get(ident, 0) + 1
        cases = []
        historical_included = False
        for item in candidates:
            proposal = item["proposal"]
            original_eligibility = proposal.get("eligibility", "frozen")
            eligibility_logged = False
            existing_case_ids = {path.name for path in (stage / "cases").iterdir()} if (stage / "cases").exists() else set()
            try:
                if counts[proposal["id"].casefold()] != 1:
                    raise Invalid("duplicate proposal id: " + proposal["id"])
                is_eligible, original, ruling = eligibility(proposal)
                eligibility_log.append({"proposal": item["path"], "id": proposal["id"],
                                        "original": original, "decision": "include" if is_eligible else "exclude",
                                        "ruling": ruling})
                eligibility_logged = True
                if not is_eligible:
                    excluded.append({"proposal": item["path"], "id": proposal["id"],
                                     "proposal_sha256": item["sha256"], "status": "excluded",
                                     "reason": ruling})
                    continue
                if item["historical"]:
                    new_cases = validate_historical(stage, item, known_ids)
                    cases.extend(new_cases)
                    historical_included = True
                else:
                    cases.append(create_case(stage, proposal, item["path"], item["sha256"],
                                             known_ids, provenance={"source": item["input"]}))
            except (Invalid, OSError, KeyError, TypeError) as exc:
                ruling = "invalid or unavailable proposal: " + str(exc)
                if eligibility_logged:
                    eligibility_log[-1].update(decision="exclude", ruling=ruling)
                else:
                    eligibility_log.append({"proposal": item["path"], "id": proposal.get("id"),
                                            "original": original_eligibility, "decision": "exclude",
                                            "ruling": ruling})
                excluded.append({"proposal": item["path"], "id": proposal.get("id"),
                                 "proposal_sha256": item["sha256"], "status": "excluded",
                                 "reason": str(exc)})
                for case_dir in (stage / "cases").iterdir() if (stage / "cases").exists() else []:
                    if case_dir.name not in existing_case_ids and case_dir.is_dir():
                        shutil.rmtree(case_dir)
                cases = [case for case in cases if case["proposal"] != item["path"]]
                if item["historical"]:
                    historical_included = False

        input_entries = inventory(stage)
        expected = {
            "schema": "mado-r22-audit-fixtures-v1",
            "contract": contract_input,
            "raw_truth_seal": {
                "path": truth_input["path"], "sha256": truth_input["sha256"],
                "schema": truth["schema"], "base_commit": truth["base_commit"],
                "created_at": truth.get("created_at"),
                "file_count": len(truth_files), "verified_file_count": len(truth_files),
                "audit_proposal_count": len(sealed_proposals),
            },
            "truth_seal_files": truth_files,
            "limits": {"seconds_per_child": 15, "address_space_bytes": 402653184,
                       "output_bytes_per_stream": 1048576, "concurrency": 1},
            "cases": sorted(cases, key=lambda case: case["id"]),
            "excluded": excluded,
            "eligibility_log": eligibility_log,
            "historical_c3_included": historical_included,
            "input_entries": input_entries,
            "scope": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion",
        }
        expected_raw = json_bytes(expected)
        (stage / "expected.json").write_bytes(expected_raw)
        (stage / "expected.sha256").write_text(sha(expected_raw) + "  expected.json\n", encoding="ascii")
        os.rename(stage, OUT)
        print(json.dumps({"fixtures": len(cases), "excluded": len(excluded),
                          "historical_c3_included": historical_included,
                          "truth_seal_sha256": truth_input["sha256"],
                          "expected_sha256": sha(expected_raw)}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Invalid, OSError) as exc:
        raise SystemExit("assembly refused: " + str(exc)) from exc
