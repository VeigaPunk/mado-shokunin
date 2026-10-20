#!/usr/bin/env python3
"""Compare tripwire findings across a stable snapshot of transcript JSONL files.

Only the tripwire parser runs against transcript paths; transcript content is
never imported, evaluated, or executed. The output uses corpus-relative paths.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict


class CouldNotEvaluate(Exception):
    pass


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


def _scan(tool_path, corpus_file, workdir):
    result = subprocess.run(
        ["python3", "-I", str(tool_path), "--scan", str(corpus_file)],
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
    marker = next((i for i, line in enumerate(lines) if line.startswith("MADO_TRIPWIRE: ")), None)
    if marker is None or marker + 1 >= len(lines):
        return None, "tripwire emitted no complete verdict"
    try:
        payload = json.loads(lines[marker + 1])
    except (ValueError, RecursionError):
        return None, "tripwire emitted invalid verdict JSON"
    if not isinstance(payload, dict) or payload.get("schema") != "mado-tripwire-verdict-v1":
        return None, "tripwire emitted an unexpected verdict"
    if payload.get("exit") != result.returncode or not isinstance(payload.get("findings"), list):
        return None, "tripwire verdict does not match its exit status"
    return payload, None


def _evidence(finding):
    value = finding.get("evidence", "observed")
    return value if value in ("observed", "lead") else str(value)


def _finding_key(finding, relative):
    return (relative, finding.get("line"), finding.get("class"), finding.get("rule"))


def _evidence_key(finding, relative):
    return _finding_key(finding, relative) + (_evidence(finding),)



def compare(args):
    script_path = Path(__file__).resolve()
    repo = script_path.parents[3]
    try:
        repo = repo.resolve(strict=True)
    except OSError as exc:
        raise CouldNotEvaluate("cannot resolve lane repository: %s" % exc)

    base_bytes = _tool_source(repo, args.base, allow_path=False)
    new_bytes = _tool_source(repo, args.new, allow_path=True)
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    new_sha = hashlib.sha256(new_bytes).hexdigest()
    corpus = Path(args.corpus).expanduser()
    try:
        corpus = corpus.resolve(strict=True)
    except OSError as exc:
        raise CouldNotEvaluate("cannot resolve corpus directory: %s" % exc)

    before = _snapshot(corpus)
    if not before:
        raise CouldNotEvaluate("corpus contains no .jsonl files")

    base_results = {}
    new_results = {}
    scan_errors = []
    with tempfile.TemporaryDirectory(prefix="mado-corpus-diff-") as temp_name:
        workdir = Path(temp_name)
        base_tool = workdir / "base-mado-tripwire.py"
        new_tool = workdir / "new-mado-tripwire.py"
        base_tool.write_bytes(base_bytes)
        new_tool.write_bytes(new_bytes)

        for relative in sorted(before):
            corpus_file = corpus / relative
            base_payload, base_error = _scan(base_tool, corpus_file, workdir)
            new_payload, new_error = _scan(new_tool, corpus_file, workdir)
            if base_error:
                scan_errors.append((relative, "base", base_error))
            else:
                base_results[relative] = base_payload
            if new_error:
                scan_errors.append((relative, "new", new_error))
            else:
                new_results[relative] = new_payload

    after = _snapshot(corpus)
    stable = sorted(path for path, digest in before.items()
                    if path in after and after[path] == digest)
    stable_set = set(stable)
    relevant_errors = [entry for entry in scan_errors if entry[0] in stable_set]
    if relevant_errors:
        path, version, error = relevant_errors[0]
        raise CouldNotEvaluate("%s scan failed on stable file %s: %s" % (version, path, error))

    base_rows = Counter()
    new_rows = Counter()
    base_evidence_rows = Counter()
    new_evidence_rows = Counter()
    new_examples = defaultdict(list)
    for relative in stable:
        for finding in base_results[relative]["findings"]:
            base_rows[_finding_key(finding, relative)] += 1
            base_evidence_rows[_evidence_key(finding, relative)] += 1
        for finding in new_results[relative]["findings"]:
            key = _finding_key(finding, relative)
            evidence_key = key + (_evidence(finding),)
            new_rows[key] += 1
            new_evidence_rows[evidence_key] += 1
            new_examples[evidence_key].append(finding)

    lost_rows = []
    for key in sorted(base_rows):
        count = base_rows[key] - new_rows[key]
        if count > 0:
            relative, line, finding_class, rule = key
            lost_rows.append({"file": relative, "line": line, "class": finding_class,
                              "rule": rule, "count": count})

    grouped_additions = defaultdict(lambda: {"count": 0, "examples": []})
    for key in sorted(new_evidence_rows):
        count = new_evidence_rows[key] - base_evidence_rows[key]
        if count <= 0:
            continue
        relative, line, finding_class, rule, evidence = key
        group = grouped_additions[(finding_class, rule, evidence)]
        group["count"] += count
        for finding in new_examples[key][:count]:
            if len(group["examples"]) < 20:
                group["examples"].append({
                    "file": relative,
                    "line": line,
                    "command": finding.get("command", ""),
                })

    added_rows = []
    for (finding_class, rule, evidence), group in sorted(grouped_additions.items()):
        group["examples"].sort(key=lambda item: (item["file"], item["line"], item["command"]))
        added_rows.append({"class": finding_class, "rule": rule, "evidence": evidence,
                           "count": group["count"], "examples": group["examples"]})

    before_paths = set(before)
    after_paths = set(after)
    report = {
        "schema": "mado-corpus-diff-v1",
        "base": {"reference": args.base, "sha256": base_sha},
        "new": {"reference": args.new, "sha256": new_sha},
        "corpus": str(corpus),
        "files": len(before),
        "stable_files": len(stable),
        "unstable_files": {
            "added_during_run": len(after_paths - before_paths),
            "removed_during_run": len(before_paths - after_paths),
            "changed_during_run": len((before_paths & after_paths) - stable_set),
        },
        "base_findings": sum(base_rows.values()),
        "new_findings": sum(new_rows.values()),
        "lost_rows": lost_rows,
        "added_rows": added_rows,
    }
    output = Path(args.out).expanduser()
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_name(output.name + ".tmp")
        temporary.write_text(json.dumps(report, ensure_ascii=True, sort_keys=True,
                                        separators=(",", ":")) + "\n",
                             encoding="utf-8")
        os.replace(temporary, output)
    except OSError as exc:
        raise CouldNotEvaluate("cannot write output JSON: %s" % exc)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="base git revision")
    parser.add_argument("--new", required=True, help="new tool path or git revision")
    parser.add_argument("--corpus", required=True, help="directory containing transcript JSONL files")
    parser.add_argument("--out", required=True, help="output JSON path")
    args = parser.parse_args(argv)
    try:
        report = compare(args)
    except CouldNotEvaluate as exc:
        print("corpus-diff: %s" % exc, file=sys.stderr)
        return 2
    print(json.dumps({
        "files": report["files"],
        "stable_files": report["stable_files"],
        "lost_rows": len(report["lost_rows"]),
        "added_groups": len(report["added_rows"]),
        "out": str(Path(args.out).expanduser()),
    }, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
