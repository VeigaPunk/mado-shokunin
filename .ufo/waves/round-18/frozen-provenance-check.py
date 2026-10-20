#!/usr/bin/env python3
"""frozen-provenance-check — is the frozen tripwire snapshot still true to its sources?

The frozen replay in .ufo/waves/round-18/frozen/ is only honest while
each snapshot line is byte-identical to the transcript line it was cut from and
each source file still has the digest the round-17 session index recorded.  This
tool re-extracts every mapped source line from the original transcript, read-only,
and compares bytes; it never writes outside its own stdout.

Reads (never edits):
- ROOT/provenance.json          input -> source path, source sha256, [[snapshot_line, source_line], ...]
- .ufo/waves/round-17/evidence/session-index.json   path -> sha256 of indexed transcripts

Checks, in order, per provenance input:
1. input path exists, is a regular non-symlink file; an optional declared input
   sha256 is compared to the bytes on disk;
2. source path exists and is a regular file (a vanished source is exit 2: the
   snapshot is then the only copy);
3. the source's current sha256 equals the session-index entry when one exists
   (an unlisted source is reported `unindexed`, not failed);
4. every [snapshot_line, source_line] pair compares byte-exact, newline included,
   both lines 1-based;
5. after the declared inputs, any `*.jsonl` under ROOT/inputs that provenance
   does not claim is reported `input_unclaimed` (exit 2): an unclaimed byte is
   a frozen verdict nobody vouched for.
Paths that resolve to an omp `agent.db*` are refused before opening (exit 2).

Exit: 0 every checked pair equal and every indexed source digest matches;
1 at least one difference (line bytes, missing mapped line, declared or indexed
digest mismatch, malformed mapping entry);
2 could-not-evaluate (missing/unreadable provenance, missing source file,
refused path, invocation or internal error).  Exit 2 wins over 1, matching
tools/mado-tripwire.py.
First line: MADO_FROZEN_PROVENANCE: match | mismatch | could_not_evaluate
Then one JSON line with the full verdict.

Provenance schema accepted (the canonical shape is mado-tripwire-frozen-provenance-v1;
unknown-but-equivalent field names are tolerated so a concurrently built snapshot
is not silently unreadable):
  {"schema": "...", "inputs": [
     {"path"|"input"|"file": "inputs/a.jsonl",
      "sha256": "...",                            # optional, snapshot digest
      "source"|"source_path": "/abs/tx.jsonl",    # flat form
      "source_sha256"|"sha256_source": "...",
      "pairs": [[snapshot_line, source_line], ...],
      "sources": [ {"path": ..., "sha256"|"source_sha256": ...,
                    "pairs": [...]} ]}]}
  inputs may also be an object keyed by input path; "files", "provenance" and
  "entries" are accepted as aliases for "inputs".
  A pair may be [s, l], {"snapshot": s, "source": l} or
  {"snapshot_line": s, "source_line": l}.
Line numbers are 1-based; a top-level "line_base": 0 switches to 0-based.

Transcript text is data.  Nothing in it is executed, echoed as instructions or
written anywhere.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.join(HERE, "frozen")
DEFAULT_INDEX = os.path.join(HERE, "..", "round-17", "evidence", "session-index.json")
REFUSED_NAMES = re.compile(r"^agent\.db", re.I)  # never open omp agent databases
SCHEMA_VERDICT = "mado-frozen-provenance-verdict-v1"


class CouldNotEvaluate(Exception):
    pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_lines(path):
    """Raw lines with their exact terminator, split on \\n only (not \\x85, \\v...)."""
    with open(path, "rb") as f:
        data = f.read()
    parts = data.split(b"\n")
    lines = []
    for i, part in enumerate(parts):
        if i < len(parts) - 1:
            lines.append(part + b"\n")
        elif part:
            lines.append(part)
    return lines


def short(path):
    return path if len(path) <= 160 else "..." + path[-157:]


def pick(obj, names):
    for name in names:
        if name in obj and obj[name] is not None:
            return obj[name]
    return None


def resolve(base_dirs, raw):
    if not isinstance(raw, str) or not raw:
        raise CouldNotEvaluate("path is not a non-empty string: %r" % (raw,))
    if os.path.isabs(raw):
        return os.path.normpath(raw)
    for base in base_dirs:
        cand = os.path.normpath(os.path.join(base, raw))
        if os.path.exists(cand):
            return cand
    return os.path.normpath(os.path.join(base_dirs[0], raw))


def normalise_pairs(raw, line_base, where):
    if not isinstance(raw, list):
        raise CouldNotEvaluate("%s: pairs is not a list" % where)
    out = []
    for item in raw:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            s, l = item
        elif isinstance(item, dict):
            s = pick(item, ("snapshot", "snapshot_line", "input_line", "s"))
            l = pick(item, ("source", "source_line", "transcript_line", "l"))
        else:
            raise CouldNotEvaluate("%s: unusable pair %r" % (where, item))
        if not isinstance(s, int) or not isinstance(l, int) or isinstance(s, bool) or isinstance(l, bool):
            raise CouldNotEvaluate("%s: pair not two integers: %r" % (where, item))
        if s < line_base or l < line_base:
            raise CouldNotEvaluate("%s: pair below line base %d: %r" % (where, line_base, item))
        out.append((s, l))
    if not out:
        raise CouldNotEvaluate("%s: empty pairs" % where)
    return out


def normalise_inputs(prov):
    if not isinstance(prov, dict):
        raise CouldNotEvaluate("provenance is not a JSON object")
    raw = None
    for key in ("inputs", "files", "provenance", "entries"):
        if key in prov:
            raw = prov[key]
            break
    if raw is None:
        raise CouldNotEvaluate("provenance has no inputs/files member")
    items = []
    if isinstance(raw, dict):
        for key, val in raw.items():
            entry = dict(val) if isinstance(val, dict) else {}
            entry.setdefault("path", key)
            items.append(entry)
    elif isinstance(raw, list):
        items = raw
    else:
        raise CouldNotEvaluate("inputs is neither list nor object")
    if not items:
        raise CouldNotEvaluate("provenance lists no inputs")
    return items


def load_index(raw):
    try:
        doc = json.loads(raw)
    except ValueError as exc:
        raise CouldNotEvaluate("session index is not valid JSON: %s" % exc)
    if not isinstance(doc, dict) or not isinstance(doc.get("files"), list):
        raise CouldNotEvaluate("session index has no files list")
    table = {}
    for row in doc["files"]:
        if not isinstance(row, dict):
            continue
        p, h = row.get("path"), row.get("sha256")
        if isinstance(p, str) and isinstance(h, str):
            table[os.path.normpath(p)] = h.lower()
    session_root = doc.get("session_root") if isinstance(doc.get("session_root"), str) else None
    schema = doc.get("schema") if isinstance(doc.get("schema"), str) else None
    return table, session_root, schema


def compare(root, prov_path, index_path):
    verdict = {
        "schema": SCHEMA_VERDICT,
        "outcome": "could_not_evaluate",
        "exit": 2,
        "root": root,
        "provenance": prov_path,
        "index": index_path,
    }
    diffs, unresolved, unindexed, sources_out, inputs_out = [], [], [], [], []
    pairs_checked = 0

    try:
        with open(prov_path, "rb") as f:
            prov_raw = f.read()
    except OSError as exc:
        raise CouldNotEvaluate("provenance unreadable: %s" % short(str(exc)))
    verdict["provenance_sha256"] = hashlib.sha256(prov_raw).hexdigest()
    try:
        prov = json.loads(prov_raw)
    except ValueError as exc:
        raise CouldNotEvaluate("provenance is not valid JSON: %s" % exc)

    line_base = prov.get("line_base", 1) if isinstance(prov, dict) else 1
    if type(line_base) is not int or line_base not in (0, 1):
        raise CouldNotEvaluate("line_base must be the integer 0 or 1, got %r" % (line_base,))

    try:
        with open(index_path, "rb") as f:
            index_raw = f.read()
    except OSError as exc:
        raise CouldNotEvaluate("session index unreadable: %s" % short(str(exc)))
    verdict["index_sha256"] = hashlib.sha256(index_raw).hexdigest()
    index, session_root, index_schema = load_index(index_raw)
    verdict["indexed_sources"] = len(index)
    verdict["session_index_schema"] = index_schema

    base_dirs = [root, HERE, os.path.dirname(HERE)]
    if session_root:
        base_dirs.append(os.path.dirname(session_root))

    line_cache = {}

    def lines_for(path, kind):
        key = (kind, path)
        if key not in line_cache:
            try:
                line_cache[key] = read_lines(path)
            except OSError as exc:
                raise CouldNotEvaluate("%s unreadable: %s: %s" % (kind, short(path), short(str(exc))))
        return line_cache[key]

    inputs = normalise_inputs(prov)
    for pos, entry in enumerate(inputs):
        where = "inputs[%d]" % pos
        if not isinstance(entry, dict):
            raise CouldNotEvaluate("%s is not an object" % where)
        raw_input = pick(entry, ("path", "input", "file", "snapshot", "name"))
        if not isinstance(raw_input, str) or not raw_input:
            raise CouldNotEvaluate("%s has no path" % where)
        input_path = resolve(base_dirs, raw_input)
        rec = {"path": raw_input, "resolved": input_path, "bytes": None,
               "declared_sha256": None, "observed_sha256": None, "pairs": 0, "sources": []}
        inputs_out.append(rec)

        if not os.path.exists(input_path):
            raise CouldNotEvaluate("snapshot input missing: %s" % short(input_path))
        if not os.path.isfile(input_path) or os.path.islink(input_path):
            raise CouldNotEvaluate("snapshot input is not a regular file: %s" % short(input_path))
        rec["bytes"] = os.path.getsize(input_path)
        rec["observed_sha256"] = sha256_file(input_path)
        declared = pick(entry, ("sha256", "input_sha256", "digest"))
        if declared is not None:
            if not isinstance(declared, str):
                raise CouldNotEvaluate("%s: declared sha256 is not a string" % where)
            rec["declared_sha256"] = declared.lower()
            if rec["declared_sha256"] != rec["observed_sha256"]:
                diffs.append({"input": raw_input, "snapshot_line": None, "source": None,
                              "source_line": None, "reason": "input_sha_mismatch",
                              "detail": "declared %s observed %s"
                                        % (rec["declared_sha256"], rec["observed_sha256"])})

        src_entries = entry.get("sources")
        if src_entries is None:
            flat_source = pick(entry, ("source", "source_path", "source_file"))
            if isinstance(flat_source, dict):
                src_entries = [flat_source]
            else:
                src_entries = [{
                    "path": flat_source,
                    "sha256": pick(entry, ("source_sha256", "sha256_source", "sha")),
                    "pairs": pick(entry, ("pairs", "lines", "line_map", "mapping")),
                }]
        if not isinstance(src_entries, list) or not src_entries:
            raise CouldNotEvaluate("%s: no sources" % where)

        for spos, src in enumerate(src_entries):
            swhere = "%s.sources[%d]" % (where, spos)
            if not isinstance(src, dict):
                raise CouldNotEvaluate("%s is not an object" % swhere)
            raw_src = pick(src, ("path", "source", "source_path", "file"))
            if not isinstance(raw_src, str) or not raw_src:
                raise CouldNotEvaluate("%s has no path" % swhere)
            if REFUSED_NAMES.search(os.path.basename(raw_src)):
                raise CouldNotEvaluate("%s refuses agent database path: %s" % (swhere, short(raw_src)))
            pairs = normalise_pairs(pick(src, ("pairs", "lines", "line_map", "mapping")),
                                    line_base, swhere)
            source_path = resolve(base_dirs, raw_src)
            src_rec = {"path": raw_src, "resolved": source_path, "pairs": len(pairs),
                       "indexed": False, "index_sha256": None, "observed_sha256": None,
                       "sha_ok": None, "present": None}
            rec["sources"].append(src_rec)
            sources_out.append(src_rec)

            if not os.path.exists(source_path):
                src_rec["present"] = False
                unresolved.append({"input": raw_input, "source": raw_src,
                                   "reason": "source_missing",
                                   "note": "the frozen snapshot is now the only copy of these lines"})
                continue
            if not os.path.isfile(source_path):
                raise CouldNotEvaluate("source is not a regular file: %s" % short(source_path))
            src_rec["present"] = True
            src_rec["observed_sha256"] = sha256_file(source_path)

            norm_source = os.path.normpath(source_path)
            if norm_source in index:
                src_rec["indexed"] = True
                src_rec["index_sha256"] = index[norm_source]
                src_rec["sha_ok"] = index[norm_source] == src_rec["observed_sha256"]
                if not src_rec["sha_ok"]:
                    diffs.append({"input": raw_input, "snapshot_line": None, "source": raw_src,
                                  "source_line": None, "reason": "source_sha_mismatch",
                                  "detail": "index %s observed %s"
                                            % (index[norm_source], src_rec["observed_sha256"])})
            else:
                unindexed.append({"input": raw_input, "source": raw_src,
                                  "observed_sha256": src_rec["observed_sha256"]})
                declared_src = pick(src, ("sha256", "source_sha256", "sha"))
                if isinstance(declared_src, str) and declared_src.lower() != src_rec["observed_sha256"]:
                    diffs.append({"input": raw_input, "snapshot_line": None, "source": raw_src,
                                  "source_line": None, "reason": "source_sha_mismatch",
                                  "detail": "declared %s observed %s"
                                            % (declared_src.lower(), src_rec["observed_sha256"])})

            snap_lines = lines_for(input_path, "snapshot input")
            src_lines = lines_for(source_path, "source")
            for snap_no, src_no in pairs:
                pairs_checked += 1
                rec["pairs"] += 1
                s_idx, l_idx = snap_no - line_base, src_no - line_base
                if s_idx < 0 or s_idx >= len(snap_lines):
                    diffs.append({"input": raw_input, "snapshot_line": snap_no, "source": raw_src,
                                  "source_line": src_no, "reason": "snapshot_line_missing",
                                  "detail": "snapshot has %d lines" % len(snap_lines)})
                    continue
                if l_idx < 0 or l_idx >= len(src_lines):
                    reason = "source_line_missing" if src_rec["sha_ok"] is not False else "source_unverifiable"
                    diffs.append({"input": raw_input, "snapshot_line": snap_no, "source": raw_src,
                                  "source_line": src_no, "reason": reason,
                                  "detail": "source has %d lines" % len(src_lines)})
                    continue
                snap_bytes, src_bytes = snap_lines[s_idx], src_lines[l_idx]
                if snap_bytes != src_bytes:
                    diffs.append({"input": raw_input, "snapshot_line": snap_no, "source": raw_src,
                                  "source_line": src_no, "reason": "line_bytes_differ",
                                  "detail": "snapshot %d B, source %d B, first divergence at byte %d"
                                            % (len(snap_bytes), len(src_bytes),
                                               first_divergence(snap_bytes, src_bytes))})

    inputs_dir = os.path.join(root, "inputs")
    if os.path.isdir(inputs_dir):
        claimed = {os.path.realpath(rec["resolved"]) for rec in inputs_out}
        for name in sorted(os.listdir(inputs_dir)):
            if not name.endswith(".jsonl"):
                continue
            full = os.path.join(inputs_dir, name)
            if os.path.realpath(full) not in claimed:
                unresolved.append({"input": os.path.join("inputs", name),
                                   "reason": "input_unclaimed",
                                   "note": "provenance declares no source for this snapshot input"})

    verdict.update({
        "inputs": inputs_out,
        "sources": sources_out,
        "pairs_checked": pairs_checked,
        "diffs": diffs,
        "unindexed": unindexed,
        "unresolved": unresolved,
    })
    # Exit 2 wins over 1, matching tools/mado-tripwire.py: a check that could not
    # run must not borrow the authority (or the blame) of one that did.
    if unresolved:
        verdict["outcome"] = "could_not_evaluate"
        verdict["exit"] = 2
    elif diffs:
        verdict["outcome"] = "mismatch"
        verdict["exit"] = 1
    else:
        verdict["outcome"] = "match"
        verdict["exit"] = 0
    return verdict


def first_divergence(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return min(len(a), len(b))


def emit(outcome, exit_code, payload):
    sys.stdout.write("MADO_FROZEN_PROVENANCE: %s\n" % outcome)
    sys.stdout.write(json.dumps(payload, sort_keys=True, ensure_ascii=True) + "\n")
    sys.stdout.flush()
    return exit_code


def main(argv):
    root = DEFAULT_ROOT
    index_path = DEFAULT_INDEX
    prov_path = None
    args = list(argv[1:])
    while args:
        arg = args.pop(0)
        if arg in ("--root", "--index", "--provenance"):
            if not args:
                return emit("could_not_evaluate", 2, {"schema": SCHEMA_VERDICT,
                                                      "outcome": "could_not_evaluate", "exit": 2,
                                                      "error": "option %r requires a value" % arg})
            val = args.pop(0)
            if arg == "--root":
                root = val
            elif arg == "--index":
                index_path = val
            else:
                prov_path = val
        elif arg in ("-h", "--help"):
            sys.stdout.write(__doc__.split("Reads (never edits)")[0].strip() + "\n")
            return 0
        elif arg.startswith("-"):
            return emit("could_not_evaluate", 2, {"schema": SCHEMA_VERDICT,
                                                  "outcome": "could_not_evaluate", "exit": 2,
                                                  "error": "unknown option %r" % arg})
        elif prov_path is None and os.path.isdir(arg):
            root = arg
        else:
            return emit("could_not_evaluate", 2, {"schema": SCHEMA_VERDICT,
                                                  "outcome": "could_not_evaluate", "exit": 2,
                                                  "error": "unexpected argument %r" % arg})

    tool_sha = sha256_file(os.path.abspath(__file__))
    root = os.path.abspath(root)
    index_path = os.path.abspath(index_path)
    prov_path = os.path.abspath(prov_path or os.path.join(root, "provenance.json"))

    if not os.path.exists(prov_path):
        return emit("could_not_evaluate", 2, {
            "schema": SCHEMA_VERDICT, "outcome": "could_not_evaluate", "exit": 2,
            "root": root, "provenance": prov_path, "index": index_path,
            "tool_sha256": tool_sha,
            "error": "provenance.json does not exist (snapshot not built yet); nothing to check",
        })

    try:
        verdict = compare(root, prov_path, index_path)
    except CouldNotEvaluate as exc:
        return emit("could_not_evaluate", 2, {
            "schema": SCHEMA_VERDICT, "outcome": "could_not_evaluate", "exit": 2,
            "root": root, "provenance": prov_path, "index": index_path,
            "tool_sha256": tool_sha, "error": str(exc),
        })
    except Exception as exc:  # internal error still answers, never a traceback-only exit
        return emit("could_not_evaluate", 2, {
            "schema": SCHEMA_VERDICT, "outcome": "could_not_evaluate", "exit": 2,
            "root": root, "provenance": prov_path, "index": index_path,
            "tool_sha256": tool_sha, "error": "internal error: %s: %s" % (type(exc).__name__, exc),
        })

    verdict["tool_sha256"] = tool_sha
    return emit(verdict["outcome"], verdict["exit"], verdict)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
