#!/usr/bin/env python3
"""Compare tripwire findings over a drift-accounted session transcript corpus.

Only the tripwire parser runs against transcript paths; transcript content is
never imported, evaluated, or executed. Reports use corpus-relative paths.
"""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile


class CouldNotEvaluate(Exception):
    pass


def _repository(script_path):
    for parent in script_path.parents:
        if (parent / ".git").exists():
            return parent.resolve(strict=True)
    raise CouldNotEvaluate("cannot locate lane repository from script path")


def _git_tool(repo, revision):
    object_name = "%s:tools/mado-tripwire.py" % revision
    resolved = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--end-of-options", object_name],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if resolved.returncode != 0:
        raise CouldNotEvaluate("cannot resolve tripwire at revision %r" % revision)
    oid = resolved.stdout.decode("ascii", "strict").strip()
    if not oid or any(c not in "0123456789abcdefABCDEF" for c in oid):
        raise CouldNotEvaluate("git returned an invalid tool object id")
    blob = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "blob", oid],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if blob.returncode != 0:
        raise CouldNotEvaluate("cannot read tripwire blob at revision %r" % revision)
    return blob.stdout


def _tool_source(repo, reference, allow_path):
    candidate = Path(reference).expanduser()
    if allow_path and candidate.is_file():
        try:
            return candidate.read_bytes()
        except OSError as exc:
            raise CouldNotEvaluate("cannot read new tool path: %s" % exc)
    return _git_tool(repo, reference)


def _hash_file(path):
    digest = hashlib.sha256()
    try:
        with open(path, "rb") as stream:
            while True:
                block = stream.read(1024 * 1024)
                if not block:
                    break
                digest.update(block)
    except OSError as exc:
        raise CouldNotEvaluate("cannot hash corpus file %s: %s" % (path, exc))
    return digest.hexdigest()


def _snapshot(root):
    try:
        root_stat = os.lstat(root)
    except OSError as exc:
        raise CouldNotEvaluate("cannot inspect corpus directory: %s" % exc)
    if not stat.S_ISDIR(root_stat.st_mode):
        raise CouldNotEvaluate("corpus path is not a real directory")

    files = {}

    def onerror(exc):
        raise CouldNotEvaluate("cannot enumerate corpus: %s" % exc)

    for directory, dirs, names in os.walk(root, topdown=True, onerror=onerror, followlinks=False):
        dirs.sort()
        for name in sorted(names):
            if not name.endswith(".jsonl"):
                continue
            path = os.path.join(directory, name)
            try:
                mode = os.lstat(path).st_mode
            except OSError as exc:
                raise CouldNotEvaluate("cannot inspect corpus file %s: %s" % (path, exc))
            if not stat.S_ISREG(mode):
                raise CouldNotEvaluate("corpus entry is not a regular file: %s" % path)
            relative = Path(os.path.relpath(path, root)).as_posix()
            files[relative] = _hash_file(path)
    return files


def _scan(tool_path, corpus_root, workdir):
    result = subprocess.run(
        ["python3", "-I", str(tool_path), "--scan", str(corpus_root)],
        cwd=workdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode not in (0, 1):
        return None, "tripwire exit %d: %s" % (result.returncode, result.stderr.strip()[:500])

    lines = result.stdout.splitlines()
    marker = next((i for i, line in enumerate(lines)
                   if line.startswith("MADO_TRIPWIRE: ")), None)
    if marker is None or marker + 1 >= len(lines):
        return None, "tripwire emitted no complete verdict"
    try:
        payload = json.loads(lines[marker + 1])
    except (ValueError, RecursionError):
        return None, "tripwire emitted invalid verdict JSON"
    if not isinstance(payload, dict) or payload.get("schema") != "mado-tripwire-verdict-v1":
        return None, "tripwire emitted an unexpected verdict"
    if (payload.get("exit") != result.returncode
            or not isinstance(payload.get("findings"), list)
            or not isinstance(payload.get("files"), list)):
        return None, "tripwire verdict does not match its exit status or lacks file coverage"
    return payload, None


def _relative(root, raw_path):
    absolute = os.path.abspath(raw_path if os.path.isabs(raw_path)
                               else os.path.join(root, raw_path))
    relative = os.path.relpath(absolute, root)
    if relative == os.pardir or relative.startswith(os.pardir + os.sep):
        raise CouldNotEvaluate("tripwire reported a file outside the corpus")
    return Path(relative).as_posix()


def _normalize_scan(payload, root):
    entries = {}
    for entry in payload["files"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise CouldNotEvaluate("tripwire emitted a malformed file manifest")
        relative = _relative(root, entry["path"])
        if relative in entries:
            raise CouldNotEvaluate("tripwire emitted a duplicate file manifest entry")
        entries[relative] = entry

    findings = defaultdict(list)
    for finding in payload["findings"]:
        if not isinstance(finding, dict) or not isinstance(finding.get("file"), str):
            raise CouldNotEvaluate("tripwire emitted a malformed finding")
        relative = _relative(root, finding["file"])
        if relative not in entries:
            raise CouldNotEvaluate("tripwire finding is absent from its file manifest")
        normalized = dict(finding)
        normalized["file"] = relative
        findings[relative].append(normalized)
    return entries, findings


def _evidence(finding):
    value = finding.get("evidence", "observed")
    return value if value in ("observed", "lead") else str(value)


def _field(finding, name):
    value = finding.get(name, "")
    return str(value) if value is not None else ""


def _signature(finding):
    return (_field(finding, "class"), _field(finding, "rule"),
            _evidence(finding), _field(finding, "command"))


def _example(finding):
    return {"file": finding["file"], "line": finding.get("line")}


def _group_add(counter, examples, finding):
    key = (_field(finding, "class"), _field(finding, "rule"), _evidence(finding))
    counter[key] += 1
    examples[key].append(_example(finding))


def _format_groups(counter, examples, limit=8):
    groups = []
    for key in sorted(counter):
        finding_class, rule, evidence = key
        sample = sorted(examples[key], key=lambda item: (item["file"], str(item["line"])))
        groups.append({
            "class": finding_class,
            "rule": rule,
            "evidence": evidence,
            "count": counter[key],
            "examples": sample[:limit],
        })
    return groups


def _call_key(finding):
    return (finding["file"], finding.get("line"), _field(finding, "tool_call_id"))


def _changed_fields(base_finding, new_finding):
    changed = []
    for name in ("class", "rule"):
        if _field(base_finding, name) != _field(new_finding, name):
            changed.append(name)
    if _evidence(base_finding) != _evidence(new_finding):
        changed.append("evidence")
    if _field(base_finding, "command") != _field(new_finding, "command"):
        changed.append("command_text")
    return tuple(changed)


def _relabel_kind(changed):
    fields = set(changed)
    if fields == {"evidence"}:
        return "evidence_relabel"
    if "class" in fields and "rule" in fields:
        return "class_rule_relabel"
    if "class" in fields:
        return "class_changed"
    if "rule" in fields:
        return "rule_relabel"
    if "command_text" in fields:
        return "command_text_changed"
    return "multiple_relabel"


def _pair_call_rows(base_rows, new_rows):
    """Pair exact rows first, then the closest remaining rows per call id."""
    base_remaining = sorted(base_rows, key=_signature)
    new_remaining = sorted(new_rows, key=_signature)
    pairs = []

    index = 0
    while index < len(base_remaining):
        signature = _signature(base_remaining[index])
        match = next((i for i, item in enumerate(new_remaining)
                      if _signature(item) == signature), None)
        if match is None:
            index += 1
            continue
        pairs.append((base_remaining.pop(index), new_remaining.pop(match), ()))

    while base_remaining and new_remaining:
        candidates = []
        for bi, before in enumerate(base_remaining):
            for ni, after in enumerate(new_remaining):
                same_class = _field(before, "class") == _field(after, "class")
                same_rule = _field(before, "rule") == _field(after, "rule")
                same_command = _field(before, "command") == _field(after, "command")
                changed = _changed_fields(before, after)
                score = (len(changed), 0 if same_command else 1,
                         0 if same_class and same_rule else 1,
                         _signature(before), _signature(after), bi, ni)
                candidates.append((score, bi, ni, changed))
        _, bi, ni, changed = min(candidates)
        pairs.append((base_remaining.pop(bi), new_remaining.pop(ni), changed))
    return pairs, base_remaining, new_remaining


def _compare_findings(base_by_file, new_by_file, selected_files):
    base_calls = defaultdict(list)
    new_calls = defaultdict(list)
    for relative in selected_files:
        for finding in base_by_file.get(relative, ()):
            base_calls[_call_key(finding)].append(finding)
        for finding in new_by_file.get(relative, ()):
            new_calls[_call_key(finding)].append(finding)

    added_counts, added_examples = Counter(), defaultdict(list)
    lost_counts, lost_examples = Counter(), defaultdict(list)
    unmatched_base_counts, unmatched_base_examples = Counter(), defaultdict(list)
    relabel_counts, relabel_examples = Counter(), defaultdict(list)
    unchanged_findings = 0
    base_keys, new_keys = set(base_calls), set(new_calls)
    lost_calls = base_keys - new_keys
    added_calls = new_keys - base_keys

    for call in sorted(added_calls, key=lambda item: (item[0], str(item[1]), item[2])):
        for finding in new_calls[call]:
            _group_add(added_counts, added_examples, finding)
    for call in sorted(lost_calls, key=lambda item: (item[0], str(item[1]), item[2])):
        for finding in base_calls[call]:
            _group_add(lost_counts, lost_examples, finding)

    for call in sorted(base_keys & new_keys, key=lambda item: (item[0], str(item[1]), item[2])):
        pairs, remaining_base, remaining_new = _pair_call_rows(
            base_calls[call], new_calls[call])
        for before, after, changed in pairs:
            if not changed:
                unchanged_findings += 1
                continue
            kind = _relabel_kind(changed)
            key = (kind, changed)
            relabel_counts[key] += 1
            relabel_examples[key].append({
                "file": before["file"],
                "line": before.get("line"),
                "from": {"class": _field(before, "class"),
                         "rule": _field(before, "rule"),
                         "evidence": _evidence(before)},
                "to": {"class": _field(after, "class"),
                       "rule": _field(after, "rule"),
                       "evidence": _evidence(after)},
            })
        for finding in remaining_base:
            _group_add(unmatched_base_counts, unmatched_base_examples, finding)
        for finding in remaining_new:
            _group_add(added_counts, added_examples, finding)

    relabelled = []
    for kind, changed in sorted(relabel_counts):
        examples = sorted(relabel_examples[(kind, changed)],
                          key=lambda item: (item["file"], str(item["line"])))
        relabelled.append({"kind": kind, "changed_fields": list(changed),
                           "count": relabel_counts[(kind, changed)],
                           "examples": examples[:8]})

    return {
        "base_findings": sum(len(base_by_file.get(path, ())) for path in selected_files),
        "new_findings": sum(len(new_by_file.get(path, ())) for path in selected_files),
        "call_ids": {
            "base": len(base_keys), "new": len(new_keys),
            "retained": len(base_keys & new_keys),
            "lost": len(lost_calls), "added": len(added_calls),
        },
        "unchanged_findings": unchanged_findings,
        "lost_rows": _format_groups(lost_counts, lost_examples),
        "lost_findings": sum(lost_counts.values()),
        "added_rows": _format_groups(added_counts, added_examples),
        "added_findings": sum(added_counts.values()),
        "relabeled": relabelled,
        "relabelled_findings": sum(relabel_counts.values()),
        "unmatched_base_rows_in_retained_calls": _format_groups(
            unmatched_base_counts, unmatched_base_examples),
        "unmatched_base_findings_in_retained_calls": sum(unmatched_base_counts.values()),
    }


def _is_under(relative, prefix):
    return relative == prefix or relative.startswith(prefix.rstrip("/") + "/")


def compare(args):
    repo = _repository(Path(__file__).resolve())
    base_bytes = _tool_source(repo, args.base, allow_path=False)
    new_bytes = _tool_source(repo, args.new, allow_path=True)
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    new_sha = hashlib.sha256(new_bytes).hexdigest()

    corpus = Path(args.corpus).expanduser()
    try:
        corpus = corpus.resolve(strict=True)
    except OSError as exc:
        raise CouldNotEvaluate("cannot resolve corpus directory: %s" % exc)
    round20_dir = Path(args.round20_dir).expanduser()
    try:
        round20_dir = round20_dir.resolve(strict=True)
        round20_prefix = Path(os.path.relpath(round20_dir, corpus)).as_posix()
    except OSError as exc:
        raise CouldNotEvaluate("cannot resolve round-20 session directory: %s" % exc)
    if round20_prefix == ".." or round20_prefix.startswith("../"):
        raise CouldNotEvaluate("round-20 session directory is outside the corpus")
    if not round20_dir.is_dir():
        raise CouldNotEvaluate("round-20 session path is not a directory")

    before = _snapshot(corpus)
    if not before:
        raise CouldNotEvaluate("corpus contains no .jsonl files")

    with tempfile.TemporaryDirectory(prefix="mado-corpus-diff-") as temp_name:
        workdir = Path(temp_name)
        base_tool = workdir / "base-mado-tripwire.py"
        new_tool = workdir / "new-mado-tripwire.py"
        base_tool.write_bytes(base_bytes)
        new_tool.write_bytes(new_bytes)
        base_payload, base_error = _scan(base_tool, corpus, workdir)
        if base_error:
            raise CouldNotEvaluate("base scan failed: %s" % base_error)
        new_payload, new_error = _scan(new_tool, corpus, workdir)
        if new_error:
            raise CouldNotEvaluate("new scan failed: %s" % new_error)

    base_entries, base_by_file = _normalize_scan(base_payload, corpus)
    new_entries, new_by_file = _normalize_scan(new_payload, corpus)
    after = _snapshot(corpus)

    excluded = []
    stable = []
    all_paths = sorted(set(before) | set(after) | set(base_entries) | set(new_entries))
    drift_counts = Counter()
    for relative in all_paths:
        reasons = []
        if relative not in before:
            reasons.append("added_during_run")
        if relative not in after:
            reasons.append("removed_during_run")
        if relative in before and relative in after and before[relative] != after[relative]:
            reasons.append("changed_during_run")
        for label, entries in (("base", base_entries), ("new", new_entries)):
            if relative in before and relative not in entries:
                reasons.append("missing_%s_scan_record" % label)
            elif relative in before and entries[relative].get("sha256") != before[relative]:
                reasons.append("%s_scan_digest_mismatch" % label)
        if reasons:
            excluded.append({"file": relative, "reasons": sorted(set(reasons))})
            for reason in set(reasons):
                drift_counts[reason] += 1
        elif relative in before and relative in after:
            stable.append(relative)

    stable_set = set(stable)
    full = _compare_findings(base_by_file, new_by_file, stable_set)
    r20_files = {path for path in stable if _is_under(path, round20_prefix)}
    r20_excluded = [entry for entry in excluded if _is_under(entry["file"], round20_prefix)]
    r20_before = {path for path in before if _is_under(path, round20_prefix)}
    r20_after = {path for path in after if _is_under(path, round20_prefix)}
    round20 = {
        "root": str(round20_dir),
        "relative_root": round20_prefix,
        "coverage": {
            "files_at_start": len(r20_before),
            "files_after": len(r20_after),
            "stable_files": len(r20_files),
            "excluded_files_count": len(r20_excluded),
            "coverage_percent": round(100 * len(r20_files) / len(r20_before), 3)
                if r20_before else 0.0,
            "excluded_files": r20_excluded,
        },
        "comparison": _compare_findings(base_by_file, new_by_file, r20_files),
    }
    report = {
        "schema": "mado-corpus-diff-v2",
        "base": {"reference": args.base, "sha256": base_sha},
        "new": {"reference": args.new, "sha256": new_sha},
        "coverage": {
            "corpus_root": str(corpus),
            "files_at_start": len(before),
            "files_after": len(after),
            "base_scan_files": len(base_entries),
            "new_scan_files": len(new_entries),
            "stable_files": len(stable),
            "excluded_files_count": len(excluded),
            "coverage_percent": round(100 * len(stable) / len(before), 3),
            "drift_counts": dict(sorted(drift_counts.items())),
            "excluded_files": excluded,
        },
        "comparison": full,
        "round20_session": round20,
    }

    output = Path(args.out).expanduser()
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(report, ensure_ascii=True, sort_keys=True,
                                separators=(",", ":")) + "\n"
        if len(serialized.encode("utf-8")) > 2 * 1024 * 1024:
            raise CouldNotEvaluate("report exceeds 2 MiB; reduce bounded examples")
        temporary = output.with_name(output.name + ".tmp")
        temporary.write_text(serialized, encoding="utf-8")
        os.replace(temporary, output)
    except OSError as exc:
        raise CouldNotEvaluate("cannot write output JSON: %s" % exc)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="base git revision")
    parser.add_argument("--new", required=True, help="new tool path or git revision")
    parser.add_argument("--corpus", required=True, help="directory containing transcript JSONL files")
    parser.add_argument("--round20-dir", required=True,
                        help="round-20 seat session directory to report separately")
    parser.add_argument("--out", required=True, help="output JSON path")
    args = parser.parse_args(argv)
    try:
        report = compare(args)
    except CouldNotEvaluate as exc:
        print("corpus-diff-v2: %s" % exc, file=sys.stderr)
        return 2
    print(json.dumps({
        "files_at_start": report["coverage"]["files_at_start"],
        "stable_files": report["coverage"]["stable_files"],
        "excluded_files": report["coverage"]["excluded_files_count"],
        "lost_calls": report["comparison"]["call_ids"]["lost"],
        "lost_findings": report["comparison"]["lost_findings"],
        "added_findings": report["comparison"]["added_findings"],
        "relabelled_findings": report["comparison"]["relabelled_findings"],
        "out": str(Path(args.out).expanduser()),
    }, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
