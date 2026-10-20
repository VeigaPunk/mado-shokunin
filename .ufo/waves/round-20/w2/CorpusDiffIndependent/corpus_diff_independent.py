#!/usr/bin/env python3
"""Independently compare tripwire finding keys over stable session JSONL files."""
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
import subprocess
import sys

ROOT = "/home/vgpnk/.omp/agent/sessions/-Projects-shokunin"
TOOLS = {
    "9c54c56": "/tmp/mado-r20w2-CorpusDiffIndependent/mado-tripwire-9c54c56.py",
    "28c6837": "/tmp/mado-r20w2-CorpusDiffIndependent/mado-tripwire-28c6837.py",
}
OUT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/CorpusDiffIndependent/corpus-diff-results.json"
BATCH_SIZE = 32


def enumerate_jsonl():
    paths = []
    errors = []

    def onerror(exc):
        errors.append({"path": getattr(exc, "filename", None), "error": type(exc).__name__})

    for current, dirs, names in os.walk(ROOT, onerror=onerror, followlinks=False):
        dirs.sort()
        for name in sorted(names):
            if name.endswith(".jsonl"):
                paths.append(os.path.join(current, name))
    return sorted(set(paths)), errors


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_result(proc, expected_paths):
    try:
        payload = json.loads(proc.stdout.splitlines()[-1])
    except (IndexError, json.JSONDecodeError):
        return None, "no JSON verdict"
    if proc.returncode not in (0, 1):
        return None, payload.get("error", "scanner exit %d" % proc.returncode)
    if payload.get("schema") != "mado-tripwire-verdict-v1":
        return None, "unexpected verdict schema"
    entries = payload.get("files")
    if not isinstance(entries, list):
        return None, "verdict has no file inventory"
    got_paths = [entry.get("path") for entry in entries if isinstance(entry, dict)]
    if Counter(got_paths) != Counter(expected_paths):
        return None, "verdict file inventory differs from requested paths"
    rows = payload.get("findings")
    if not isinstance(rows, list):
        return None, "verdict has no findings list"
    by_path = {path: [] for path in expected_paths}
    for row in rows:
        if not isinstance(row, dict) or row.get("file") not in by_path:
            return None, "finding row has an unexpected file"
        by_path[row["file"]].append(row)
    return by_path, None


def scan_chunk(tool, paths, errors):
    """Scan a chunk; bisect failures so one bad file cannot hide other files."""
    argv = ["python3", "-I", tool, "--scan", *paths]
    try:
        proc = subprocess.run(argv, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", check=False)
    except OSError as exc:
        if len(paths) > 1:
            midpoint = len(paths) // 2
            left = scan_chunk(tool, paths[:midpoint], errors)
            right = scan_chunk(tool, paths[midpoint:], errors)
            return {**left, **right}
        errors.append({"path": paths[0], "tool": tool, "error": type(exc).__name__})
        return {}
    result, problem = parse_result(proc, paths)
    if problem is not None:
        if len(paths) > 1:
            midpoint = len(paths) // 2
            left = scan_chunk(tool, paths[:midpoint], errors)
            right = scan_chunk(tool, paths[midpoint:], errors)
            return {**left, **right}
        errors.append({"path": paths[0], "tool": tool,
                       "error": problem, "exit": proc.returncode,
                       "stderr": proc.stderr[:500]})
        return {}
    return result


def scan_paths(tool, paths):
    results = {}
    errors = []
    for offset in range(0, len(paths), BATCH_SIZE):
        chunk = paths[offset:offset + BATCH_SIZE]
        results.update(scan_chunk(tool, chunk, errors))
    return results, errors


def scan_pass(paths, output):
    before = {}
    hash_errors = []
    for path in paths:
        try:
            before[path] = sha256_file(path)
        except OSError as exc:
            hash_errors.append({"path": path, "phase": "before", "error": type(exc).__name__})
    candidates = [path for path in paths if path in before]
    per_tool = {}
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {rev: pool.submit(scan_paths, tool, candidates)
                   for rev, tool in TOOLS.items()}
        for rev, future in futures.items():
            per_tool[rev] = future.result()
    eligible = []
    for path in candidates:
        try:
            after = sha256_file(path)
            audit = {"path": path, "before": before[path], "after": after}
        except OSError as exc:
            after = None
            audit = {"path": path, "before": before[path], "after": None,
                     "after_error": type(exc).__name__}
        output["hash_audit"].append(audit)
        if after != before[path]:
            output["drifting_files"].append(audit)
            continue
        if any(path not in per_tool[rev][0] for rev in TOOLS):
            continue
        eligible.append(path)
    output["hash_errors"].extend(hash_errors)
    for rev in TOOLS:
        rows_by_path, errors = per_tool[rev]
        output["scan_errors"].extend({**error, "revision": rev} for error in errors)
        output["scan_ok_files"][rev] += len(rows_by_path)
    return eligible, per_tool


def row_key(row):
    return (row["file"], row["line"], row["class"], row["rule"])


def main():
    output = {
        "schema": "mado-corpus-diff-independent-v1",
        "session_root": ROOT,
        "tools": {},
        "initial_files": 0,
        "final_files": 0,
        "additional_pass_files": 0,
        "scanned_stable_files": 0,
        "scan_ok_files": {revision: 0 for revision in TOOLS},
        "hash_audit": [],
        "drifting_files": [],
        "hash_errors": [],
        "scan_errors": [],
        "walk_errors": [],
        "enumeration_changes": {},
        "baseline_rows": 0,
        "repaired_rows": 0,
        "lost_row_count": 0,
        "lost_rows": [],
    }
    for revision, tool in TOOLS.items():
        output["tools"][revision] = {"path": tool, "sha256": sha256_file(tool)}

    initial, walk_errors = enumerate_jsonl()
    output["initial_files"] = len(initial)
    output["walk_errors"].extend(walk_errors)
    stable_paths, initial_results = scan_pass(initial, output)

    after_initial, walk_errors = enumerate_jsonl()
    output["walk_errors"].extend(walk_errors)
    initial_set = set(initial)
    additional = sorted(set(after_initial) - initial_set)
    output["additional_pass_files"] = len(additional)
    additional_stable, additional_results = scan_pass(additional, output) if additional else ([], {})

    all_stable = stable_paths + additional_stable
    all_results = {}
    for revision in TOOLS:
        all_results[revision] = {}
        if revision in initial_results:
            all_results[revision].update(initial_results[revision][0])
        if revision in additional_results:
            all_results[revision].update(additional_results[revision][0])
    output["scanned_stable_files"] = len(all_stable)

    old_rows = []
    new_rows = []
    for path in all_stable:
        old_rows.extend(all_results["9c54c56"][path])
        new_rows.extend(all_results["28c6837"][path])
    output["baseline_rows"] = len(old_rows)
    output["repaired_rows"] = len(new_rows)

    old_by_key = defaultdict(list)
    new_counts = Counter()
    for row in old_rows:
        old_by_key[row_key(row)].append(row)
    for row in new_rows:
        new_counts[row_key(row)] += 1
    lost = Counter({key: len(rows) for key, rows in old_by_key.items()}) - new_counts
    for key in sorted(lost):
        count = lost[key]
        baseline_for_key = old_by_key[key]
        surviving = new_counts[key]
        lost_examples = baseline_for_key[surviving:surviving + count]
        for row in lost_examples:
            output["lost_rows"].append({
                "file": key[0], "line": key[1], "class": key[2], "rule": key[3],
                "command": row.get("command", ""),
            })
    output["lost_row_count"] = sum(lost.values())

    final_paths, walk_errors = enumerate_jsonl()
    output["walk_errors"].extend(walk_errors)
    output["final_files"] = len(final_paths)
    output["enumeration_changes"] = {
        "added_after_initial_sweep": sorted(set(after_initial) - initial_set),
        "removed_after_initial_sweep": sorted(initial_set - set(after_initial)),
        "added_after_additional_sweep": sorted(set(final_paths) - set(after_initial)),
        "removed_after_additional_sweep": sorted(set(after_initial) - set(final_paths)),
    }
    with open(OUT, "w", encoding="utf-8") as stream:
        json.dump(output, stream, ensure_ascii=True, sort_keys=True, indent=2)
        stream.write("\n")
    summary = {key: output[key] for key in (
        "initial_files", "final_files", "additional_pass_files", "scanned_stable_files",
        "scan_ok_files", "baseline_rows", "repaired_rows", "lost_row_count",
        "drifting_files", "hash_errors", "scan_errors", "walk_errors",
        "enumeration_changes")}
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    print("RESULT_JSON: %s" % OUT)


if __name__ == "__main__":
    main()
