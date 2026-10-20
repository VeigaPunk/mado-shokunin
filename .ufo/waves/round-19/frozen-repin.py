#!/usr/bin/env python3
"""Round-19 C3: re-pin a frozen tripwire baseline on a current tool.

Usage:
  frozen-repin.py --from SRC --to DIR --tool PATH [--allow-new-findings]

SRC is a committed frozen baseline (SRC/expected.json, SRC/inputs/*.jsonl,
SRC/provenance.json). Each pinned input is copied byte-exact to DIR/inputs only
after its sha256 matches SRC/expected.json; the tool is then run as
`python3 -I PATH --scan inputs/<name>.jsonl ...` with cwd = the staged DIR.
DIR/expected.json (schema mado-tripwire-frozen-v1) is derived from that run:

- expected_findings: every finding the tool reports, as {file, line, class,
  rule}, in the tool's own order (the four fields --frozen compares).
- known_misses: the SRC known_misses the tool still misses, kept verbatim.
- permit / expected_exit / expected_label: SRC permit and the scan verdict.

It refuses (exit 1, DIR never created) when a source expected finding
disappears, or when a finding lands on a line that was neither expected nor a
known miss, unless --allow-new-findings. After writing, the staged baseline is
replayed with the same tool's `--frozen`; only `frozen_match` is accepted, so a
written baseline is one the tool itself reproduces.

DIR/README.md starts with `RECEIPT tool=... tool_sha256=... utc=... argv=...`;
DIR/provenance.json is SRC's object with an appended `repinned_from` note (an
existing note becomes a list, so re-pins compose). The scan runs in a private
staging directory under DIR's parent and DIR is published by one rename: a
refused or failed re-pin leaves no DIR. Expected findings are therefore the
tool's own output on these bytes; that proves self-consistency, not that the
tool classifies the original incident correctly.

Exit: 0 baseline written, 1 refused, 2 usage or could-not-evaluate (unreadable
SRC, digest mismatch, scan/tool failure, non-empty target, replay mismatch).
Exit 2 writes nothing. First line: MADO_FROZEN_REPIN: written | refused |
could_not_evaluate
"""
import hashlib
import json
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone

SCHEMA = "mado-tripwire-frozen-v1"
VERDICT_SCHEMA = "mado-tripwire-verdict-v1"
FROZEN_VERDICT_SCHEMA = "mado-tripwire-frozen-verdict-v1"
RESULT_SCHEMA = "mado-frozen-repin-verdict-v1"
CLASSES = ("host_mutation", "package_query", "live_probe")
INPUT_PATH = re.compile(r"inputs/[A-Za-z0-9._-]+\.jsonl")
SHA256 = re.compile(r"[0-9a-f]{64}")
FROZEN_PAIRS = {(0, "clean"), (0, "permitted_only"), (1, "findings")}
EXIT = {"written": 0, "refused": 1, "could_not_evaluate": 2}
TOOL_TIMEOUT = 300
USAGE = ("usage: frozen-repin.py --from SRC --to DIR --tool PATH "
         "[--allow-new-findings]")


class CouldNotEvaluate(Exception):
    pass


class Refused(Exception):
    def __init__(self, reasons, detail):
        super().__init__("refused")
        self.reasons = reasons
        self.detail = detail


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def emit(kind, payload):
    print("MADO_FROZEN_REPIN: %s" % kind)
    body = {"schema": RESULT_SCHEMA, "outcome": kind, "exit": EXIT[kind]}
    body.update(payload)
    print(json.dumps(body, ensure_ascii=True, sort_keys=True))


# ------------------------------------------------------------- loading ---

def read_bytes(path, what):
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError as exc:
        raise CouldNotEvaluate("%s unreadable (%s)" % (what, type(exc).__name__))


def require_regular(path, what):
    try:
        st = os.lstat(path)
    except OSError:
        raise CouldNotEvaluate("%s missing: %s" % (what, path))
    if stat.S_ISLNK(st.st_mode):
        raise CouldNotEvaluate("%s is a symlink: %s" % (what, path))
    if not stat.S_ISREG(st.st_mode):
        raise CouldNotEvaluate("%s is not a regular file: %s" % (what, path))


def unique_pairs(pairs):
    """object_pairs_hook: a repeated JSON key is an integrity error, never last-wins."""
    out, seen = {}, set()
    for key, value in pairs:
        if key in seen:
            raise ValueError("duplicate key %r" % key)
        seen.add(key)
        out[key] = value
    return out


def reject_constant(value):
    raise ValueError("non-standard JSON constant %s" % value)


def load_json(raw, what):
    try:
        return json.loads(raw.decode("utf-8"), parse_constant=reject_constant,
                          object_pairs_hook=unique_pairs)
    except (ValueError, UnicodeDecodeError, RecursionError) as exc:
        raise CouldNotEvaluate("%s is not JSON (%s)" % (what, type(exc).__name__))


def npath(path):
    return os.path.normpath(path).replace(os.sep, "/")


def resolve_tool(tool):
    real = os.path.realpath(os.path.abspath(tool))
    require_regular(real, "tool")
    return real


def validate_source(spec):
    """Return the source pin normalised, or CouldNotEvaluate."""
    if not isinstance(spec, dict):
        raise CouldNotEvaluate("source expected.json is not an object")
    if spec.get("schema") != SCHEMA:
        raise CouldNotEvaluate("source expected.json schema is not %s" % SCHEMA)
    raw_inputs = spec.get("inputs")
    if not isinstance(raw_inputs, list) or not raw_inputs:
        raise CouldNotEvaluate("source expected.json lists no inputs")
    inputs, listed = [], set()
    for entry in raw_inputs:
        if (not isinstance(entry, dict) or not isinstance(entry.get("path"), str)
                or not INPUT_PATH.fullmatch(entry["path"])
                or not isinstance(entry.get("sha256"), str)
                or not SHA256.fullmatch(entry["sha256"].strip().lower())):
            raise CouldNotEvaluate("source expected.json has a bad inputs entry")
        rel = entry["path"]
        if rel in listed:
            raise CouldNotEvaluate("source expected.json lists %s twice" % rel)
        listed.add(rel)
        inputs.append((rel, entry["sha256"].strip().lower()))
    permit = spec.get("permit")
    if (not isinstance(permit, list)
            or any(not isinstance(c, str) or c not in CLASSES for c in permit)
            or len(set(permit)) != len(permit)):
        raise CouldNotEvaluate("source permit is not a class list")
    if (spec.get("expected_exit"), spec.get("expected_label")) not in FROZEN_PAIRS:
        raise CouldNotEvaluate("source expected exit/label pair is unreachable")
    raw_findings = spec.get("expected_findings")
    if not isinstance(raw_findings, list):
        raise CouldNotEvaluate("source expected_findings is not a list")
    findings = []
    for row in raw_findings:
        if (not isinstance(row, dict) or not isinstance(row.get("file"), str)
                or type(row.get("line")) is not int or row["line"] < 1
                or row.get("class") not in CLASSES
                or not isinstance(row.get("rule"), str)):
            raise CouldNotEvaluate("source expected_findings has a bad row")
        rel = npath(row["file"])
        if rel not in listed:
            raise CouldNotEvaluate("source expected_findings names an unlisted input: %s" % rel)
        findings.append({"file": rel, "line": row["line"],
                         "class": row["class"], "rule": row["rule"]})
    known = []
    raw_known = spec.get("known_misses", [])
    if not isinstance(raw_known, list):
        raise CouldNotEvaluate("source known_misses is not a list")
    for row in raw_known:
        if (not isinstance(row, dict) or not isinstance(row.get("file"), str)
                or type(row.get("line")) is not int or row["line"] < 1
                or ("note" in row and not isinstance(row["note"], str))):
            raise CouldNotEvaluate("source known_misses has a bad row")
        if npath(row["file"]) not in listed:
            raise CouldNotEvaluate("source known_misses names an unlisted input: %s"
                                   % row["file"])
        known.append(row)  # verbatim: the re-pin may not rewrite a miss note
    overlap = ({(f["file"], f["line"]) for f in findings}
               & {(npath(k["file"]), k["line"]) for k in known})
    if overlap:
        file, line = sorted(overlap)[0]
        raise CouldNotEvaluate("source known_misses overlaps expected_findings: %s:%d"
                               % (file, line))
    return {"inputs": inputs, "permit": permit, "findings": findings, "known": known}


def source_inputs(src, listed):
    """Refuse a source whose inputs/ cannot prove the pin covers every jsonl."""
    idir = os.path.join(src, "inputs")
    try:
        st = os.lstat(idir)
    except OSError:
        raise CouldNotEvaluate("source inputs/ is missing: %s" % idir)
    if stat.S_ISLNK(st.st_mode) or not stat.S_ISDIR(st.st_mode):
        raise CouldNotEvaluate("source inputs/ is not a real directory: %s" % idir)

    def onerror(err):
        raise CouldNotEvaluate("unreadable source inputs/: %s" % err.filename)

    seen = set()
    for root, dirs, names in os.walk(idir, onerror=onerror, followlinks=False):
        dirs.sort()
        for name in sorted(names):
            if name.endswith(".jsonl"):
                seen.add(npath(os.path.relpath(os.path.join(root, name), src)))
    extra = sorted(seen - set(listed))
    if extra:
        raise CouldNotEvaluate("source inputs/ holds unlisted jsonl: %s"
                               % ", ".join(extra))


# ---------------------------------------------------------------- tool ---

def run_tool(argv, cwd):
    try:
        return subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                              timeout=TOOL_TIMEOUT)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CouldNotEvaluate("tool did not run (%s)" % type(exc).__name__)


def parse_verdict(proc, listed, permit, pins):
    """Validate the tool's --scan verdict; return normalised findings + verdict."""
    if proc.returncode not in (0, 1):
        raise CouldNotEvaluate("tool --scan exit %d" % proc.returncode)
    lines = proc.stdout.splitlines()
    if len(lines) < 2:
        raise CouldNotEvaluate("tool --scan wrote no verdict")
    match = re.fullmatch(r"MADO_TRIPWIRE: (clean|permitted_only|findings)", lines[0])
    if not match:
        raise CouldNotEvaluate("tool --scan first line is not a MADO_TRIPWIRE label")
    verdict = load_json(lines[1].encode("utf-8"), "tool --scan verdict")
    if not isinstance(verdict, dict) or verdict.get("schema") != VERDICT_SCHEMA:
        raise CouldNotEvaluate("tool --scan verdict schema is not %s" % VERDICT_SCHEMA)
    if verdict.get("exit") != proc.returncode:
        raise CouldNotEvaluate("tool --scan verdict exit does not match its status")
    raw_findings = verdict.get("findings")
    if not isinstance(raw_findings, list):
        raise CouldNotEvaluate("tool --scan verdict has no findings list")
    findings = []
    for row in raw_findings:
        if not isinstance(row, dict):
            raise CouldNotEvaluate("tool --scan finding is not an object")
        rel = row.get("file")
        if not isinstance(rel, str) or npath(rel) not in listed:
            raise CouldNotEvaluate("tool --scan finding names an unlisted file: %r"
                                   % (rel,))
        if type(row.get("line")) is not int or row["line"] < 1:
            raise CouldNotEvaluate("tool --scan finding has a bad line")
        if row.get("class") not in CLASSES:
            raise CouldNotEvaluate("tool --scan finding class outside this schema: %r"
                                   % (row.get("class"),))
        if not isinstance(row.get("rule"), str) or not row["rule"]:
            raise CouldNotEvaluate("tool --scan finding has no rule")
        findings.append({"file": npath(rel), "line": row["line"],
                         "class": row["class"], "rule": row["rule"]})
    unpermitted = sum(1 for f in findings if f["class"] not in permit)
    want_exit = 1 if unpermitted else 0
    want_label = ("clean" if not findings
                  else "findings" if unpermitted else "permitted_only")
    if (want_exit, want_label) != (proc.returncode, match.group(1)):
        raise CouldNotEvaluate("tool --scan verdict is internally inconsistent")
    if verdict.get("unpermitted") not in (None, unpermitted):
        raise CouldNotEvaluate("tool --scan unpermitted count disagrees with findings")
    entries = verdict.get("files")
    if not isinstance(entries, list):
        raise CouldNotEvaluate("tool --scan verdict has no files list")
    seen, lines_by_path = {}, {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise CouldNotEvaluate("tool --scan files entry is malformed")
        rel = npath(entry["path"])
        if rel not in listed:
            raise CouldNotEvaluate("tool --scan reports an unlisted file: %s" % rel)
        if rel in seen:
            raise CouldNotEvaluate("tool --scan reports %s twice" % rel)
        if entry.get("sha256") != pins[rel]:
            raise CouldNotEvaluate("tool --scan read bytes that do not match the pin: %s"
                                   % rel)
        seen[rel] = entry.get("sha256")
        lines_by_path[rel] = entry.get("lines")
    if set(seen) != listed:
        raise CouldNotEvaluate("tool --scan did not report every listed input")
    return {"findings": findings, "exit": proc.returncode, "label": match.group(1),
            "unpermitted": unpermitted, "lines": lines_by_path,
            "counts": dict(Counter(f["class"] for f in findings))}


# -------------------------------------------------------------- render ---

def rows(counter):
    return [dict(zip(("file", "line", "class", "rule"), key))
            for key in sorted(counter.elements())]


def render_readme(meta):
    out = []
    out.append("RECEIPT tool=%s tool_sha256=%s utc=%s argv=%s" % (
        meta["tool"], meta["tool_sha256"], meta["utc"], shlex.join(meta["scan_argv"])))
    out.append("")
    out.append("# Frozen tripwire replay (re-pinned)")
    out.append("")
    out.append("Re-pinned from `%s` (source expected.json sha256 `%s`) by the"
               % (meta["source"], meta["source_expected_sha256"]))
    out.append("round-19 regenerator `.ufo/waves/round-19/frozen-repin.py`. The scan on the")
    out.append("RECEIPT line ran over the relative `inputs/...` paths with cwd = this")
    out.append("directory's staged copy (byte-identical; published by one rename after the")
    out.append("replay below). `expected_findings` is the tool's own output on these bytes.")
    out.append("")
    out.append("A frozen baseline proves these bytes still draw this verdict *from this tool")
    out.append("digest*. It does not prove the tool classifies the original incident")
    out.append("correctly: the source pin carried the committed receipts' claim, and this")
    out.append("re-pin keeps that claim only as its refusal rule - no source expected finding")
    out.append("may disappear, and no finding may land on a line that was neither expected")
    out.append("nor a known miss (unless it was regenerated with `--allow-new-findings`).")
    out.append("")
    out.append("Replay during re-pin (staged copy, same tool):")
    out.append("")
    out.append("    MADO_TRIPWIRE_FROZEN: frozen_match")
    out.append("")
    out.append("Verify this directory: `python3 -I %s --frozen %s`"
               % (meta["tool"], meta["readme_dir"]))
    out.append("Re-pin: `python3 -I .ufo/waves/round-19/frozen-repin.py --from %s --to %s"
               " --tool %s%s`" % (meta["source"], meta["readme_dir"], meta["tool"],
                                  " --allow-new-findings" if meta["allowed"] else ""))
    out.append("")
    out.append("## Inputs (byte-exact copies, digest-verified against the source pin)")
    out.append("")
    out.append("| path | bytes | lines | sha256 |")
    out.append("|---|---|---|---|")
    for row in meta["inputs"]:
        out.append("| `%s` | %d | %s | `%s` |" % (
            row["path"], row["bytes"], row["lines"], row["sha256"]))
    out.append("")
    out.append("## Verdict")
    out.append("")
    out.append("- scan: `%s`, exit %d, unpermitted %d"
               % (meta["label"], meta["exit"], meta["unpermitted"]))
    out.append("- findings: %d %s" % (len(meta["findings"]), json.dumps(
        meta["counts"], sort_keys=True)))
    out.append("- expected_findings: %d" % len(meta["findings"]))
    out.append("- known_misses kept: %d%s" % (
        len(meta["known_kept"]),
        "" if not meta["known_dropped"] else
        "; dropped as now-detected: %s" % ", ".join(
            "%s:%d" % (k["file"], k["line"]) for k in meta["known_dropped"])))
    out.append("- findings on lines that were neither expected nor a known miss: %d%s"
               % (len(meta["outside"]),
                  "" if not meta["outside"] else " (accepted by --allow-new-findings)"))
    out.append("")
    out.append("## Provenance")
    out.append("")
    out.append("`provenance.json` is the source object with a `repinned_from` note appended")
    out.append("(an existing note is kept and becomes a list). Any `tool_receipt_sha256`")
    out.append("already present still names the receipt the *original* findings came from;")
    out.append("the tool digest that produced this baseline is on the RECEIPT line above.")
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- main ---

def parse_args(argv):
    opt = {"src": None, "dst": None, "tool": None, "allow": False}
    keys = {"--from": "src", "--to": "dst", "--tool": "tool"}
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in keys:
            if i + 1 >= len(argv):
                raise CouldNotEvaluate("usage: %s needs a value" % arg)
            if opt[keys[arg]] is not None:
                raise CouldNotEvaluate("usage: %s repeated" % arg)
            opt[keys[arg]] = argv[i + 1]
            i += 2
            continue
        if arg == "--allow-new-findings":
            if opt["allow"]:
                raise CouldNotEvaluate("usage: --allow-new-findings repeated")
            opt["allow"] = True
            i += 1
            continue
        raise CouldNotEvaluate("usage: unexpected argument %r" % arg)
    missing = [flag for flag, key in keys.items() if opt[key] is None]
    if missing:
        raise CouldNotEvaluate("usage: missing %s" % ", ".join(sorted(missing)))
    return opt


def repin(opt, utc):
    src = os.path.abspath(opt["src"])
    dst = os.path.abspath(opt["dst"])
    tool = resolve_tool(opt["tool"])
    tool_sha = hashlib.sha256(read_bytes(tool, "tool")).hexdigest()
    if os.path.islink(src) or not os.path.isdir(src):
        raise CouldNotEvaluate("--from is not a directory: %s" % src)
    expected_path = os.path.join(src, "expected.json")
    require_regular(expected_path, "source expected.json")
    expected_raw = read_bytes(expected_path, "source expected.json")
    spec = validate_source(load_json(expected_raw, "source expected.json"))
    source_inputs(src, [rel for rel, _ in spec["inputs"]])
    blobs = []
    for rel, digest in spec["inputs"]:
        path = os.path.join(src, rel)
        require_regular(path, rel)
        data = read_bytes(path, rel)
        if hashlib.sha256(data).hexdigest() != digest:
            raise CouldNotEvaluate("source input does not match its pin: %s" % rel)
        blobs.append((rel, digest, data))
    prov_path = os.path.join(src, "provenance.json")
    require_regular(prov_path, "source provenance.json")
    prov = load_json(read_bytes(prov_path, "source provenance.json"),
                     "source provenance.json")
    if not isinstance(prov, dict):
        raise CouldNotEvaluate("source provenance.json is not an object")

    if os.path.islink(dst):
        raise CouldNotEvaluate("--to is a symlink: %s" % dst)
    if os.path.exists(dst):
        if not os.path.isdir(dst):
            raise CouldNotEvaluate("--to exists and is not a directory: %s" % dst)
        if os.listdir(dst):
            raise CouldNotEvaluate("--to exists and is not empty: %s" % dst)
    parent = os.path.dirname(dst) or os.curdir
    if not os.path.isdir(parent):
        raise CouldNotEvaluate("--to parent is not a directory: %s" % parent)

    staging = tempfile.mkdtemp(prefix=".frozen-repin-", dir=parent)
    try:
        os.chmod(staging, 0o755)  # mkdtemp is 0700; the baseline is a shared artifact
        os.mkdir(os.path.join(staging, "inputs"))
        for rel, digest, data in blobs:
            dest = os.path.join(staging, rel)
            try:
                with open(dest, "xb") as fh:
                    fh.write(data)
            except OSError as exc:
                raise CouldNotEvaluate("cannot stage %s (%s)" % (rel, type(exc).__name__))
            if hashlib.sha256(read_bytes(dest, rel)).hexdigest() != digest:
                raise CouldNotEvaluate("staged copy differs from its pin: %s" % rel)

        listed = [rel for rel, _ in spec["inputs"]]
        pins = dict(spec["inputs"])
        scan_argv = [sys.executable, "-I", tool, "--scan"] + listed
        if spec["permit"]:
            scan_argv += ["--permit"] + list(spec["permit"])
        proc = run_tool(scan_argv, staging)
        verdict = parse_verdict(proc, set(listed), set(spec["permit"]), pins)

        findings = verdict["findings"]
        got = Counter((f["file"], f["line"], f["class"], f["rule"]) for f in findings)
        source_counts = Counter((f["file"], f["line"], f["class"], f["rule"])
                                for f in spec["findings"])
        missing = source_counts - got
        expected_lines = {(f["file"], f["line"]) for f in spec["findings"]}
        known_lines = {(npath(k["file"]), k["line"]) for k in spec["known"]}
        outside = [f for f in findings
                   if (f["file"], f["line"]) not in expected_lines | known_lines]
        hit_lines = {(f["file"], f["line"]) for f in findings}
        known_kept = [k for k in spec["known"]
                      if (npath(k["file"]), k["line"]) not in hit_lines]
        known_dropped = [k for k in spec["known"]
                         if (npath(k["file"]), k["line"]) in hit_lines]
        reasons = []
        if missing:
            reasons.append({"kind": "source_finding_missing",
                            "rows": rows(missing)})
        if outside and not opt["allow"]:
            reasons.append({"kind": "finding_on_unexpected_line",
                            "rows": [{"file": f["file"], "line": f["line"],
                                      "class": f["class"], "rule": f["rule"]}
                                     for f in outside]})
        detail = {
            "source": src, "target": dst, "tool": tool, "tool_sha256": tool_sha,
            "scan_argv": scan_argv, "scan_exit": verdict["exit"],
            "scan_label": verdict["label"],
            "expected_findings": len(findings), "counts": verdict["counts"],
            "known_misses_kept": len(known_kept),
            "known_misses_dropped": [{"file": npath(k["file"]), "line": k["line"]}
                                     for k in known_dropped],
            "target_written": False,
        }
        if reasons:
            raise Refused(reasons, detail)

        expected = {
            "schema": SCHEMA,
            "inputs": [{"path": rel, "sha256": digest} for rel, digest, _ in blobs],
            "permit": list(spec["permit"]),
            "expected_exit": verdict["exit"],
            "expected_label": verdict["label"],
            "expected_findings": findings,
            "known_misses": known_kept,
        }
        expected_bytes = (json.dumps(expected, indent=2, ensure_ascii=True)
                          + "\n").encode("utf-8")
        try:
            with open(os.path.join(staging, "expected.json"), "wb") as fh:
                fh.write(expected_bytes)
        except OSError as exc:
            raise CouldNotEvaluate("cannot stage expected.json (%s)"
                                   % type(exc).__name__)

        replay_argv = [sys.executable, "-I", tool, "--frozen", staging]
        replay = run_tool(replay_argv, staging)
        replay_lines = replay.stdout.splitlines()
        if (replay.returncode != 0 or not replay_lines
                or replay_lines[0] != "MADO_TRIPWIRE_FROZEN: frozen_match"):
            raise CouldNotEvaluate("staged baseline does not replay (rc=%d, %s)"
                                   % (replay.returncode,
                                      replay_lines[0] if replay_lines else "no output"))
        if len(replay_lines) < 2:
            raise CouldNotEvaluate("staged replay wrote no verdict")
        frozen = load_json(replay_lines[1].encode("utf-8"), "frozen replay verdict")
        if not isinstance(frozen, dict) or frozen.get("schema") != FROZEN_VERDICT_SCHEMA:
            raise CouldNotEvaluate("frozen replay verdict schema is wrong")
        if frozen.get("tool_sha256") != tool_sha:
            raise CouldNotEvaluate("frozen replay ran different tool bytes")
        if frozen.get("expected_sha256") != hashlib.sha256(expected_bytes).hexdigest():
            raise CouldNotEvaluate("frozen replay read different expected.json bytes")

        meta = {
            "source": src, "readme_dir": dst, "tool": tool, "tool_sha256": tool_sha,
            "utc": utc, "scan_argv": scan_argv, "allowed": opt["allow"],
            "source_expected_sha256": hashlib.sha256(expected_raw).hexdigest(),
            "inputs": [{"path": rel, "sha256": digest, "bytes": len(data),
                        "lines": verdict["lines"].get(rel)}
                       for rel, digest, data in blobs],
            "label": verdict["label"], "exit": verdict["exit"],
            "unpermitted": verdict["unpermitted"], "findings": findings,
            "counts": verdict["counts"], "known_kept": known_kept,
            "known_dropped": known_dropped, "outside": outside,
        }
        try:
            with open(os.path.join(staging, "README.md"), "w", encoding="utf-8") as fh:
                fh.write(render_readme(meta))
        except OSError as exc:
            raise CouldNotEvaluate("cannot stage README.md (%s)" % type(exc).__name__)

        note = {
            "source": src,
            "source_expected_sha256": meta["source_expected_sha256"],
            "tool": tool,
            "tool_sha256": tool_sha,
            "utc": utc,
            "argv": scan_argv,
            "inputs": [{"path": rel, "sha256": digest} for rel, digest, _ in blobs],
            "note": ("expected_findings and known_misses re-derived from this tool run; "
                     "any tool_receipt_sha256 already present still names the origin of "
                     "the source baseline's claim"),
        }
        previous = prov.get("repinned_from")
        if previous is None:
            prov["repinned_from"] = note
        elif isinstance(previous, dict):
            prov["repinned_from"] = [previous, note]
        elif isinstance(previous, list):
            prov["repinned_from"] = previous + [note]
        else:
            raise CouldNotEvaluate("source provenance repinned_from is neither object nor list")
        provenance_bytes = (json.dumps(prov, indent=2, ensure_ascii=True)
                            + "\n").encode("utf-8")
        try:
            with open(os.path.join(staging, "provenance.json"), "wb") as fh:
                fh.write(provenance_bytes)
        except OSError as exc:
            raise CouldNotEvaluate("cannot stage provenance.json (%s)"
                                   % type(exc).__name__)

        if os.path.islink(dst):
            raise CouldNotEvaluate("--to became a symlink: %s" % dst)
        if os.path.exists(dst) and (not os.path.isdir(dst) or os.listdir(dst)):
            raise CouldNotEvaluate("--to is not empty at publish time: %s" % dst)
        try:
            os.replace(staging, dst)
        except OSError as exc:
            raise CouldNotEvaluate("cannot publish %s (%s)" % (dst, type(exc).__name__))
        staging = None

        emit("written", {
            "source": src, "target": dst, "tool": tool, "tool_sha256": tool_sha,
            "utc": utc, "argv": scan_argv,
            "inputs": [{"path": rel, "sha256": digest, "bytes": len(data),
                        "lines": verdict["lines"].get(rel)}
                       for rel, digest, data in blobs],
            "expected_sha256": hashlib.sha256(expected_bytes).hexdigest(),
            "expected_findings": len(findings), "counts": verdict["counts"],
            "known_misses_kept": len(known_kept),
            "known_misses_dropped": [{"file": npath(k["file"]), "line": k["line"]}
                                     for k in known_dropped],
            "new_findings_accepted": [{"file": f["file"], "line": f["line"],
                                       "class": f["class"], "rule": f["rule"]}
                                      for f in outside],
            "replay": "frozen_match",
        })
        return 0
    finally:
        if staging is not None and os.path.isdir(staging):
            shutil.rmtree(staging, ignore_errors=True)


def main(argv):
    if argv in (["-h"], ["--help"]):
        print(USAGE)
        return 0
    utc = utc_now()
    try:
        opt = parse_args(argv)
        return repin(opt, utc)
    except Refused as exc:
        emit("refused", dict(exc.detail, refusals=exc.reasons))
        return 1
    except CouldNotEvaluate as exc:
        message = str(exc)
        if message.startswith("usage:"):
            print(USAGE, file=sys.stderr)
        print(message, file=sys.stderr)
        emit("could_not_evaluate", {"error": message})
        return 2
    except BaseException as exc:  # never let an internal error read as written/refused
        emit("could_not_evaluate", {"error": "internal %s" % type(exc).__name__})
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
