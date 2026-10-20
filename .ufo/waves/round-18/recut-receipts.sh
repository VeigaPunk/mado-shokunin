#!/usr/bin/env bash
# recut-receipts.sh — round-18 R17-V1 fix: digest-pinned re-cut of the real-transcript
# tripwire receipts into .ufo/waves/round-18/evidence/.
#
# Usage:
#   recut-receipts.sh REV [--outdir DIR]
#   OUTDIR=/path recut-receipts.sh REV
#
# REV is a lane commit. The run is refused (exit 2, nothing written to OUTDIR) unless
# the working-tree tools/mado-tripwire.py has the same sha256 as the blob
# `git show REV:tools/mado-tripwire.py`. The `git show | sha256sum` pipeline's
# PIPESTATUS is captured: a failed read (rc != 0) is refused and is never digested as
# the empty-input sha256 e3b0c442…, which was the F10 false "local edit" FAIL in
# tools/mado-verify.sh:3406.
#
# The round-17 receipts recorded the scanned paths but no command. This script
# reconstructs each scan from the recorded `files[].path` list in recorded order
# (tripwire.py's discover() preserves argv order and de-duplicates by realpath), then
# records the exact argv in the new receipt so the next re-cut needs no reconstruction.
#
# Writes (OUTDIR defaults to .ufo/waves/round-18/evidence):
#   tripwire-r13.txt .. tripwire-r16.txt, tripwire-anchor-r15.txt
#     line 1: RECEIPT tool=tools/mado-tripwire.py tool_sha256=<hex>
#             measured_commit=<REV full hash> utc=<date -u> cmd=<exact argv>
#     then the tool stdout verbatim, then exit=<N>. Any non-empty tool stderr is
#     appended as a `stderr:` block immediately before exit=<N> (normally absent).
#   tripwire-pacmanlog-join.txt
#     re-derived from /var/log/pacman.log by file read only (no package-manager query,
#     no sudo; call start from custom/tool_execution_start.data.startedAt, UTC->-0300)
#   recut-summary.json
#     per receipt: round-17 vs re-cut exit, counts, files and finding multiset
#
# Exit: 0 every receipt matches round 17; 1 a receipt differs (summary names it);
#       2 refused or could-not-evaluate. The tool change is re-checked after the scans
#       and before anything is written, so a mid-run edit of the tool cannot produce a
#       receipt whose header pins code that did not run.
#
# Limits, stated: this re-runs scans over the same transcript files; it does not prove
# those files are unchanged (their digests are in each verdict's files[].sha256). It
# says nothing about commands outside the scanned files. A `findings` verdict is
# evidence to adjudicate, not an incident record. Re-derived receipts are only as good
# as the transcript files still being readable.

set -u -o pipefail
export LC_ALL=C

SELF=$(readlink -f -- "${BASH_SOURCE[0]}")
LANE=$(cd -- "$(dirname -- "$SELF")/../../.." && pwd)
TOOL_REL=tools/mado-tripwire.py
TOOL=$LANE/$TOOL_REL
OLD_EV=$LANE/.ufo/waves/round-17/evidence
DEFAULT_OUT=$LANE/.ufo/waves/round-18/evidence
OUTDIR=${OUTDIR:-$DEFAULT_OUT}
EMPTY_SHA=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
NAMES=(tripwire-r13.txt tripwire-r14.txt tripwire-r15.txt tripwire-r16.txt tripwire-anchor-r15.txt)

usage() {
    printf 'usage: %s REV [--outdir DIR]   (or OUTDIR=/dir %s REV)\n' \
        "${0##*/}" "${0##*/}" >&2
}

refuse() {
    printf '%s: REFUSED: %s\n' "${0##*/}" "$*" >&2
    exit 2
}

# Print the recorded scanned paths of a round-17 receipt, one per line, in order.
receipt_files() {
    python3 -I - "$1" <<'PY'
import json
import sys
lines = open(sys.argv[1], encoding="utf-8", errors="replace").read().splitlines()
doc = None
for line in lines:
    line = line.strip()
    if line.startswith("{"):
        doc = json.loads(line)
        break
if doc is None:
    sys.exit("no verdict JSON line in %s" % sys.argv[1])
files = doc.get("files")
if not isinstance(files, list):
    sys.exit("verdict has no files list in %s" % sys.argv[1])
for entry in files:
    path = entry.get("path") if isinstance(entry, dict) else None
    if not isinstance(path, str) or not path:
        sys.exit("file entry without path in %s" % sys.argv[1])
    print(path)
PY
}

REV=""
while [ $# -gt 0 ]; do
    case $1 in
        --outdir)
            [ $# -ge 2 ] || refuse "--outdir needs a directory"
            OUTDIR=$2
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            usage
            refuse "unknown option: $1"
            ;;
        *)
            [ -z "$REV" ] || { usage; refuse "unexpected extra argument: $1"; }
            REV=$1
            shift
            ;;
    esac
done
[ -n "$REV" ] || { usage; refuse "missing REV"; }
[ -n "$OUTDIR" ] || refuse "empty OUTDIR"

[ -f "$TOOL" ] || refuse "missing working-tree tool: $TOOL"
[ -r "$TOOL" ] || refuse "unreadable working-tree tool: $TOOL"

full=$(git -C "$LANE" rev-parse --verify --quiet "${REV}^{commit}") \
    || refuse "cannot resolve '$REV' to a lane commit"
[ -n "$full" ] || refuse "cannot resolve '$REV' to a lane commit"

local_sha=$(sha256sum -- "$TOOL")
local_sha=${local_sha%% *}
[ -n "$local_sha" ] || refuse "could not digest working-tree tool: $TOOL"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/recut-receipts.XXXXXX") || refuse "mktemp failed"
trap 'rm -rf -- "$WORK"' EXIT

# Digest of the blob at REV. PIPESTATUS is read on the line immediately after the
# pipeline; a failing `git show` is refused rather than digested as empty input.
git -C "$LANE" show "$full:$TOOL_REL" | sha256sum > "$WORK/blob.sha"
prc=("${PIPESTATUS[@]}")
blob_sha=$(cut -d' ' -f1 < "$WORK/blob.sha")
if [ "${prc[0]}" -ne 0 ]; then
    refuse "git show '$full:$TOOL_REL' failed rc=${prc[0]} (no digest accepted; the empty-input digest $EMPTY_SHA is never evidence)"
fi
if [ "${prc[1]}" -ne 0 ]; then
    refuse "sha256sum on git show output failed rc=${prc[1]}"
fi
[ -n "$blob_sha" ] || refuse "empty digest from git show"
[ "$blob_sha" != "$EMPTY_SHA" ] || refuse "git show produced the empty-input digest; refusing it as a measurement"
if [ "$local_sha" != "$blob_sha" ]; then
    refuse "tool digest mismatch: working tree $local_sha != $full:$TOOL_REL $blob_sha"
fi

for n in "${NAMES[@]}"; do
    [ -f "$OLD_EV/$n" ] || refuse "missing round-17 receipt: $OLD_EV/$n"
    [ -r "$OLD_EV/$n" ] || refuse "unreadable round-17 receipt: $OLD_EV/$n"
    mapfile -t PROBE < <(receipt_files "$OLD_EV/$n")
    [ "${#PROBE[@]}" -gt 0 ] || refuse "no recorded scan paths in $OLD_EV/$n"
done

utc=$(date -u)
for n in "${NAMES[@]}"; do
    mapfile -t paths < <(receipt_files "$OLD_EV/$n")
    [ "${#paths[@]}" -gt 0 ] || refuse "no recorded scan paths in $OLD_EV/$n"
    cmd=(python3 -I "$TOOL" --scan "${paths[@]}")
    printf '%s\n' "${cmd[*]}" > "$WORK/$n.cmd"
    "${cmd[@]}" > "$WORK/$n.stdout" 2> "$WORK/$n.stderr"
    printf '%s\n' "$?" > "$WORK/$n.rc"
done

# The tool file must not have changed while the scans ran: every receipt header pins
# the digest that was verified before, and the scans must have used that same file.
after_sha=$(sha256sum -- "$TOOL")
after_sha=${after_sha%% *}
[ "$after_sha" = "$local_sha" ] \
    || refuse "tool file changed during the re-cut ($local_sha -> $after_sha); receipts discarded"

STAGE=$WORK/out
mkdir -p -- "$STAGE" || refuse "cannot create staging dir"

for n in "${NAMES[@]}"; do
    rc=$(cat "$WORK/$n.rc")
    cmdline=$(cat "$WORK/$n.cmd")
    hdr="RECEIPT tool=$TOOL_REL tool_sha256=$local_sha measured_commit=$full utc=$utc cmd=$cmdline"
    {
        printf '%s\n' "$hdr"
        cat "$WORK/$n.stdout"
        if [ -s "$WORK/$n.stderr" ]; then
            printf 'stderr:\n'
            cat "$WORK/$n.stderr"
        fi
        printf 'exit=%s\n' "$rc"
    } > "$STAGE/$n"
done

# Re-derive the pacman.log join by file read only.
JOIN_SUMMARY=$(MADO_RECUT_SHA="$local_sha" MADO_RECUT_REV="$full" MADO_RECUT_UTC="$utc" \
    OUTDIR="$STAGE" python3 -I - <<'PY'
import hashlib
import json
import os
import re
from datetime import datetime, timedelta

OUTDIR = os.environ["OUTDIR"]
TOOL_SHA = os.environ["MADO_RECUT_SHA"]
REV = os.environ["MADO_RECUT_REV"]
UTC = os.environ["MADO_RECUT_UTC"]
LOG = "/var/log/pacman.log"
NAMES = ["tripwire-r13.txt", "tripwire-r14.txt", "tripwire-r15.txt",
         "tripwire-r16.txt", "tripwire-anchor-r15.txt"]
WINDOW = re.compile(r"^\[(2026-10-(?:19T2|20T0[0-6])):([0-9]{2}:[0-9]{2})-0300\]")
RUNNING = re.compile(r"\[PACMAN\] Running '([^']+)'")


def verdict(name):
    for line in open(os.path.join(OUTDIR, name), encoding="utf-8", errors="replace"):
        line = line.strip()
        if line.startswith("{"):
            return json.loads(line)
    raise SystemExit("no verdict JSON in %s" % name)


# 1. Package transactions in the mado window, read from the log as bytes (no query).
tx = []
with open(LOG, encoding="utf-8", errors="replace") as fh:
    for no, line in enumerate(fh, 1):
        m = WINDOW.match(line)
        if not m:
            continue
        r = RUNNING.search(line)
        if not r:
            continue
        command = r.group(1)
        toks = command.split()
        if not toks or os.path.basename(toks[0]) not in ("pacman", "yay", "paru"):
            continue
        if not any(t.startswith(("-S", "-U", "-R")) for t in toks[1:]):
            continue
        tx.append({"line": no, "local": m.group(1) + ":" + m.group(2), "command": command})

# 2. host_mutation findings grouped per (file, line); join lines pair `sudo` with `pacman:*`.
groups = {}
for name in NAMES:
    doc = verdict(name)
    for f in doc.get("findings", []):
        if f.get("class") != "host_mutation":
            continue
        key = (f.get("file"), f.get("line"))
        g = groups.setdefault(key, {"rules": set(), "call": f.get("tool_call_id"),
                                    "timestamp": f.get("timestamp")})
        rule = f.get("rule")
        if isinstance(rule, str):
            g["rules"].add(rule)
selected = []
for (path, line), g in groups.items():
    rules = g["rules"]
    if "sudo" in rules and any(r.startswith("pacman:") for r in sorted(rules)):
        selected.append({"file": path, "line": line, "rules": sorted(rules),
                         "call": g["call"], "timestamp": g["timestamp"]})

# 3. Call start per tool_call_id, from custom/tool_execution_start records.
cache = {}


def starts(path):
    if path in cache:
        return cache[path]
    found = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            if "tool_execution_start" not in raw:
                continue
            try:
                d = json.loads(raw)
            except ValueError:
                continue
            if d.get("type") == "custom" and d.get("customType") == "tool_execution_start":
                data = d.get("data") or {}
                cid, st = data.get("toolCallId"), data.get("startedAt")
                if isinstance(cid, str) and isinstance(st, str):
                    found[cid] = st
    cache[path] = found
    return found


def local_key(iso):
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return (dt - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S")


matched = {}
for s in selected:
    s["started"] = starts(s["file"]).get(s["call"]) if s["call"] else None
    s["local"] = local_key(s["started"]) if s["started"] else None
    if s["local"]:
        matched.setdefault(s["local"], []).append(s)

blocks = []
joined = 0
used = set()
unmatched = []
for t in tx:
    hits = matched.get(t["local"], [])
    if not hits:
        unmatched.append(t["line"])
        continue
    joined += 1
    for s in hits:
        used.add((s["file"], s["line"]))
        rules = ["sudo"] + [r for r in s["rules"] if r.startswith("pacman:")]
        started = s["started"]
        call = s["call"] or "no-call-id"
        blocks.append("pacman.log:%d %s-0300 %s <-> %s:%d (%s %s) %s" % (
            t["line"], t["local"].replace("T", " ")[11:], t["command"],
            os.path.basename(s["file"] or "?"), s["line"], started, call,
            " + ".join(rules)))

orphans = ["%s:%d" % (s["file"], s["line"]) for s in selected
           if (s["file"], s["line"]) not in used]

out_path = os.path.join(OUTDIR, "tripwire-pacmanlog-join.txt")
lines = [
    "# Round-18 C1 re-derivation: tripwire host_mutation pacman findings vs /var/log/pacman.log",
    "# command (file read only, no package-manager query and no sudo):",
    "#   awk '/^\\[2026-10-(19T2|20T0[0-6])/ && /\\[PACMAN\\] Running/' /var/log/pacman.log",
    "# receipt: tool_sha256=%s measured_commit=%s utc=%s" % (TOOL_SHA, REV, UTC),
    "# call start: custom/tool_execution_start.data.startedAt from each transcript; the log is -0300,",
    "# so the join key is the call start converted UTC-3h; the transcript record timestamp is not used.",
    "# transactions: package-manager Running lines whose argv carry a short -S/-U/-R operation;",
    "# findings: the receipt's host_mutation groups that pair `sudo` with `pacman:*`.",
]
lines.extend(blocks)
for line_no in unmatched:
    t = next(t for t in tx if t["line"] == line_no)
    lines.append("# unmatched transaction: pacman.log:%d %s %s" % (t["line"], t["local"] + "-0300", t["command"]))
for orphan in orphans:
    lines.append("# tripwire finding with no log transaction: %s" % orphan)
lines.append("# result: %d/%d mado-window package transactions joined to a tripwire host_mutation "
             "line by call start; %d finding group(s) without a log transaction; 0 package-manager "
             "commands were run by this script" % (joined, len(tx), len(orphans)))
text = "\n".join(lines) + "\n"
with open(out_path, "w", encoding="utf-8") as fh:
    fh.write(text)
print(json.dumps({"path": "tripwire-pacmanlog-join.txt", "transactions": len(tx),
                  "joined": joined, "unmatched": unmatched, "orphan_findings": orphans,
                  "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()},
                 sort_keys=True))
PY
) || refuse "pacman.log join derivation failed"

MADO_RECUT_SHA="$local_sha" MADO_RECUT_REV="$full" MADO_RECUT_UTC="$utc" \
    JOIN_SUMMARY="$JOIN_SUMMARY" OLD_EV="$OLD_EV" OUTDIR="$STAGE" \
    python3 -I - > "$STAGE/recut-summary.json" <<'PY'
import hashlib
import json
import os
import sys

OUTDIR = os.environ["OUTDIR"]
OLD = os.environ["OLD_EV"]
TOOL_SHA = os.environ["MADO_RECUT_SHA"]
REV = os.environ["MADO_RECUT_REV"]
UTC = os.environ["MADO_RECUT_UTC"]
JOIN = json.loads(os.environ["JOIN_SUMMARY"])
NAMES = ["tripwire-r13.txt", "tripwire-r14.txt", "tripwire-r15.txt",
         "tripwire-r16.txt", "tripwire-anchor-r15.txt"]


def parse(path):
    raw = open(path, "rb").read()
    lines = raw.decode("utf-8", "replace").splitlines()
    doc = None
    for line in lines:
        if line.strip().startswith("{"):
            try:
                doc = json.loads(line.strip())
            except ValueError:
                doc = None
            break
    verdict_line = next((l for l in lines if l.startswith("MADO_TRIPWIRE:")), "")
    exit_value = None
    for line in reversed(lines):
        if line.startswith("exit="):
            try:
                exit_value = int(line.split("=", 1)[1])
            except ValueError:
                exit_value = None
            break
    if exit_value is None and isinstance(doc, dict):
        exit_value = doc.get("exit")
    return {"first_line": lines[0] if lines else "", "verdict_line": verdict_line,
            "doc": doc, "exit": exit_value,
            "sha256": hashlib.sha256(raw).hexdigest()}


def finding_multiset(doc):
    return sorted((f.get("file"), f.get("line"), f.get("class"), f.get("rule"))
                  for f in (doc or {}).get("findings", []))


def file_paths(doc):
    return [f.get("path") for f in (doc or {}).get("files", [])]


receipts = []
all_identical = True
for name in NAMES:
    old = parse(os.path.join(OLD, name))
    new = parse(os.path.join(OUTDIR, name))
    od, nd = old["doc"], new["doc"]
    header_ok = (new["first_line"].startswith("RECEIPT ")
                 and ("tool_sha256=%s" % TOOL_SHA) in new["first_line"]
                 and ("measured_commit=%s" % REV) in new["first_line"]
                 and ("utc=%s" % UTC) in new["first_line"])
    row = {
        "name": name,
        "round17_verdict_line": old["verdict_line"],
        "recut_verdict_line": new["verdict_line"],
        "round17_exit": old["exit"],
        "recut_exit": new["exit"],
        "round17_counts": (od or {}).get("counts"),
        "recut_counts": (nd or {}).get("counts"),
        "counts_identical": (od or {}).get("counts") == (nd or {}).get("counts"),
        "round17_files": len(file_paths(od)),
        "recut_files": len(file_paths(nd)),
        "files_identical": file_paths(od) == file_paths(nd),
        "round17_findings": len((od or {}).get("findings", [])),
        "recut_findings": len((nd or {}).get("findings", [])),
        "findings_multiset_identical": finding_multiset(od) == finding_multiset(nd),
        "permitted_identical": (od or {}).get("permitted") == (nd or {}).get("permitted"),
        "receipt_header_ok": header_ok,
        "round17_receipt_sha256": old["sha256"],
        "recut_receipt_sha256": new["sha256"],
    }
    row["identical"] = (row["round17_exit"] == row["recut_exit"]
                        and row["round17_verdict_line"] == row["recut_verdict_line"]
                        and row["counts_identical"] and row["files_identical"]
                        and row["findings_multiset_identical"]
                        and row["permitted_identical"] and header_ok)
    if not row["identical"]:
        all_identical = False
    receipts.append(row)
    status = "identical" if row["identical"] else "DIFF"
    print("RECUT %-24s %s exit %s->%s counts %s->%s" % (
        name, status, row["round17_exit"], row["recut_exit"],
        json.dumps(row["round17_counts"], sort_keys=True),
        json.dumps(row["recut_counts"], sort_keys=True)), file=sys.stderr)

summary = {
    "schema": "mado-recut-summary-v1",
    "tool": "tools/mado-tripwire.py",
    "tool_sha256": TOOL_SHA,
    "measured_commit": REV,
    "utc": UTC,
    "receipts": receipts,
    "all_counts_identical": all(r["counts_identical"] for r in receipts),
    "all_receipts_identical": all_identical,
    "pacmanlog_join": JOIN,
}
json.dump(summary, sys.stdout, indent=1, sort_keys=True)
sys.stdout.write("\n")
sys.exit(0 if all_identical else 1)
PY
summary_rc=$?
if [ "$summary_rc" -eq 2 ]; then
    refuse "recut summary could not be produced"
fi
for n in "${NAMES[@]}"; do
    [ -s "$STAGE/$n" ] || refuse "receipt not staged: $STAGE/$n"
done
[ -s "$STAGE/recut-summary.json" ] || refuse "summary not staged: $STAGE/recut-summary.json"
[ -s "$STAGE/tripwire-pacmanlog-join.txt" ] || refuse "join not staged: $STAGE/tripwire-pacmanlog-join.txt"

mkdir -p -- "$OUTDIR" || refuse "cannot create OUTDIR: $OUTDIR"
for n in "${NAMES[@]}" tripwire-pacmanlog-join.txt recut-summary.json; do
    cp -- "$STAGE/$n" "$OUTDIR/$n" || refuse "cannot write $OUTDIR/$n"
done

printf 'RECUT_DONE outdir=%s measured_commit=%s tool_sha256=%s receipts=%d %s\n' \
    "$OUTDIR" "$full" "$local_sha" "${#NAMES[@]}" \
    "$([ "$summary_rc" -eq 0 ] && printf 'all_identical=yes' || printf 'all_identical=no')"
exit "$summary_rc"
