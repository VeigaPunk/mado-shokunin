#!/usr/bin/env python3
"""Freeze every regular tracked JSONL fixture at the registered base commit.

The bytes are copied as inert fixture data. No fixture is parsed or executed.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import shutil
import tempfile
from pathlib import Path
from typing import NamedTuple

BASE_COMMIT = "794aaeb22b4bf35b2482a6779733b69343baff5b"
MAX_FILES = 10_000
MAX_SINGLE_FILE_BYTES = 32 * 1024 * 1024
MAX_TOTAL_BYTES = 256 * 1024 * 1024
SNAPSHOT_NAME = "snapshot"


class SourceFile(NamedTuple):
    mode: str
    oid: str
    path_bytes: bytes
    size_bytes: int


def git(repo: Path, *args: str, input_bytes: bytes | None = None) -> bytes:
    env = os.environ.copy()
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    result = subprocess.run(
        ["git", "-C", os.fspath(repo), *args],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=env,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args[:2])} failed: {detail}")
    return result.stdout


def list_source_files(repo: Path) -> list[SourceFile]:
    resolved = git(repo, "rev-parse", "--verify", f"{BASE_COMMIT}^{{commit}}").strip()
    if resolved.decode("ascii") != BASE_COMMIT:
        raise RuntimeError(f"base commit did not resolve exactly: {BASE_COMMIT}")

    tree = git(repo, "ls-tree", "-r", "-z", "--full-tree", BASE_COMMIT)
    selected: list[tuple[str, str, bytes]] = []
    for record in tree.split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        mode_bytes, object_type, oid_bytes = metadata.split(b" ")
        if (
            mode_bytes not in (b"100644", b"100755")
            or object_type != b"blob"
            or not path.endswith(b".jsonl")
        ):
            continue
        if (
            not path
            or path.startswith(b"/")
            or any(part in (b"", b".", b"..") for part in path.split(b"/"))
        ):
            raise RuntimeError("unsafe repository path in base tree")
        selected.append((mode_bytes.decode("ascii"), oid_bytes.decode("ascii"), path))
        if len(selected) > MAX_FILES:
            raise RuntimeError(f"population exceeds the {MAX_FILES}-file safety cap")

    if not selected:
        return []

    object_ids = b"".join(oid.encode("ascii") + b"\n" for _, oid, _ in selected)
    size_records = git(
        repo,
        "cat-file",
        "--batch-check=%(objectname) %(objecttype) %(objectsize)",
        input_bytes=object_ids,
    ).splitlines()
    if len(size_records) != len(selected):
        raise RuntimeError("Git returned an incomplete blob-size inventory")

    source_files: list[SourceFile] = []
    total_bytes = 0
    for (mode, oid, path), size_record in zip(selected, size_records, strict=True):
        fields = size_record.split()
        if len(fields) != 3 or fields[0].decode("ascii") != oid or fields[1] != b"blob":
            raise RuntimeError("Git returned an unexpected object-size record")
        size_bytes = int(fields[2])
        if size_bytes > MAX_SINGLE_FILE_BYTES:
            raise RuntimeError(
                f"source file exceeds the {MAX_SINGLE_FILE_BYTES}-byte per-file cap"
            )
        total_bytes += size_bytes
        if total_bytes > MAX_TOTAL_BYTES:
            raise RuntimeError(
                f"population exceeds the {MAX_TOTAL_BYTES}-byte total safety cap"
            )
        source_files.append(SourceFile(mode, oid, path, size_bytes))
    return source_files


def main() -> int:
    corpus_dir = Path(__file__).resolve().parent
    repo_text = git(corpus_dir, "rev-parse", "--show-toplevel").decode("utf-8").strip()
    repo = Path(repo_text).resolve()
    try:
        corpus_dir.relative_to(repo)
    except ValueError as exc:
        raise RuntimeError("corpus output directory is outside the Git worktree") from exc

    snapshot = corpus_dir / SNAPSHOT_NAME
    if snapshot.exists() or snapshot.is_symlink():
        raise RuntimeError(f"refusing to overwrite existing snapshot: {snapshot}")

    source_files = list_source_files(repo)
    stage = Path(tempfile.mkdtemp(prefix=".snapshot-stage-", dir=corpus_dir))
    try:
        files_dir = stage / "files"
        files_dir.mkdir()
        rows: list[dict[str, object]] = []
        total_bytes = 0

        for source in source_files:
            relative_path = os.fsdecode(source.path_bytes)
            show_spec = f"{BASE_COMMIT}:{relative_path}"
            data = git(repo, "show", "--no-ext-diff", show_spec)
            if len(data) != source.size_bytes:
                raise RuntimeError(f"source size changed while reading {relative_path!r}")
            digest = hashlib.sha256(data).hexdigest()

            destination = files_dir.joinpath(*relative_path.split("/"))
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as output:
                output.write(data)

            rows.append(
                {
                    "path": relative_path,
                    "path_bytes_hex": source.path_bytes.hex(),
                    "source_mode": source.mode,
                    "git_blob_oid": source.oid,
                    "size_bytes": len(data),
                    "sha256": digest,
                }
            )
            total_bytes += len(data)

        if total_bytes != sum(source.size_bytes for source in source_files):
            raise RuntimeError("written byte count differs from the preflight inventory")

        manifest = {
            "format": "mado-committed-fixture-corpus-freeze-v1",
            "source_commit": BASE_COMMIT,
            "provenance": (
                "Committed lane transcript fixture corpus only; this is NOT a private "
                "live-session corpus. Source bytes were retrieved as inert data with "
                "git show; no transcript snippets were executed."
            ),
            "inclusion_rule": (
                "Recursively include each distinct repository-relative path exactly "
                "once iff the pinned commit tree records a regular blob (mode 100644 "
                "or 100755) whose path has the case-sensitive byte suffix .jsonl. "
                "This is a complete tree census: detector output, file contents, "
                "session state, and local uncommitted files are not eligibility "
                "filters. Equal-content files at different paths remain separate."
            ),
            "limits": {
                "max_files": MAX_FILES,
                "max_single_file_bytes": MAX_SINGLE_FILE_BYTES,
                "max_total_bytes": MAX_TOTAL_BYTES,
                "behavior_on_limit": "fail before publishing any snapshot; never filter",
            },
            "file_count": len(rows),
            "total_size_bytes": total_bytes,
            "files": rows,
        }
        manifest_bytes = (
            json.dumps(manifest, ensure_ascii=True, indent=2, sort_keys=True).encode("utf-8")
            + b"\n"
        )
        (stage / "manifest.json").write_bytes(manifest_bytes)
        os.rename(stage, snapshot)
        stage = None
        print(
            f"snapshot={snapshot} files={manifest['file_count']} "
            f"bytes={manifest['total_size_bytes']} "
            f"manifest_sha256={hashlib.sha256(manifest_bytes).hexdigest()}"
        )
        return 0
    finally:
        if stage is not None and stage.exists():
            shutil.rmtree(stage)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print(f"freeze_corpus: {exc}", file=sys.stderr)
        raise SystemExit(1)
