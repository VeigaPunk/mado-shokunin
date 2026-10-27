#!/usr/bin/env python3
"""check-session-material.py — privacy gate for committed receipts.

Question answered: does any tracked file at a revision carry raw session
material that SKILL.md rule 4 keeps out of this public repo (live window
titles, process tables, monitor serials/descriptions, home-directory
listings, a monitor serial quoted in prose)?

Input: a git repository and a revision. Every tracked file in scope at that
revision is read from the object database (``git ls-tree -r`` +
``git cat-file --batch``); the working tree is never touched, so the gate can
run on any committed revision of a clone without checkout. Scope is
``--scope ufo`` (default: ``.ufo/`` only, the historical behaviour) or
``--scope all`` (the whole tracked tree, which is where the held
``corpus/knowledge/`` prose serials sit). There is no flag that drops a rule:
R1-R4 and R5 are always scored, and R6 contributes only when
``--serial-from-host`` supplies the values it counts.

Rules (one finding line per file *and* rule; counts are inside the line)
-----------------------------------------------------------------------
R1_CLIENT_DUMP   an element of ``hyprctl clients -j``: a JSON object that
                 carries ``class`` and ``title`` (or ``initialTitle``) with
                 non-empty string values. Whole-file JSON is parsed first;
                 otherwise JSON objects embedded in prose, fenced blocks or
                 ``.txt`` receipts are found with a brace scan
                 (``JSONDecoder.raw_decode``). An object with only ``class``,
                 or with an empty ``title``, is not a finding.
R2_PROC_TABLE    a socket-table row from ``ss -xpa`` / ``ss -p``: the pattern
                 ``users:(("<program>",pid=<n>`` — the program name and pid
                 columns are what makes it a process table.
R3_MONITOR_IDENT an element of ``hyprctl monitors all -j``: a JSON object with
                 a non-empty ``serial`` plus a non-empty ``description``,
                 ``make`` or ``model``. Redacted/empty serials do not match.
R4_HOME_LISTING  more than ``--home-limit`` (default 10) *distinct* lines that
                 consist solely of an absolute ``/home/<user>/...`` path — the
                 shape of a ``find ~`` / ``ls`` dump. Paths quoted inside a
                 sentence are not counted; no path text is ever printed.
R5_SERIAL_PROSE  a monitor-serial-shaped token anywhere in a text blob,
                 prose included — the leak R3 cannot see, because R3 needs a
                 JSON object that also carries a description, make or model.
                 The shape is the EDID/serial one, standing as a whole token::

                     (?<![0-9A-Za-z])[0-9]{2,6}[A-Z]{3,8}[0-9]{3,7}(?![0-9A-Za-z])

                 Findings print ``tokens=`` and ``shapes=`` — a run-length
                 digit/capital mask such as ``9x3+Ax5+9x4``, which cannot
                 itself read back as a serial — and never the token.
R6_SERIAL_EXACT  only under ``--serial-from-host``: the exact serial value(s)
                 that ``hyprctl monitors all -j`` reports, counted as plain
                 substrings in every blob in scope. Shape-independent, so it
                 catches a serial R5's pattern misses (lowercase, separators,
                 a short capital run, a JSON value without an identifying
                 key). The finding prints ``count=`` and ``sources=``, never a
                 value or its length. A host read that fails or reports no
                 non-empty serial is exit 2, not a silent pass.

Output: one ``FINDING`` line per (file, rule), the per-rule tally, then the
summary line exactly::

    SESSION_MATERIAL: files=<n> findings=<n> rev=<hash>

Exit status: 0 no findings, 1 findings, 2 usage or git error.

Usage::

    check-session-material.py --repo <dir> --rev <rev> [--home-limit N]
                              [--scope ufo|all] [--serial-from-host]
                              [--waivers <path>] [--gate-source <path>]
                              [--no-waivers]
    check-session-material.py --selftest [--verbose]

``--selftest`` builds positive and negative fixtures in a throwaway git
repository under ``$TMPDIR`` and scores this file's own detection and the
end-to-end scan against them. Its serial fixtures are assembled from parts at
run time, so this file's own bytes never trip R5 or R6.

Synthetic-material waivers (the marker)
---------------------------------------
A seat's own fixture is not session material, yet its bytes look exactly like
one. The gate therefore honours a marker *pair*: a sidecar ``<path>.synthetic``
whose first line is exactly::

    SYNTHETIC-MATERIAL v1 kind=<fixture|gate-copy> rules=<R1,R2,...> sha256=<64 hex>

and one line in the registry (default ``quality/session-material-waivers.txt``,
read from the scanned revision — never from the working tree)::

    <path> <sha256> <rules> kind=<kind>

A ``(file, rule)`` finding is waived only when *all* of these hold; every rule
the sidecar does not list still fires on the same file.

W1 ``path`` is under ``.ufo/waves/`` and the registry itself is not under
   ``.ufo/``: a wave cannot issue its own waiver, and the waiver list is one
   reviewable lane file outside the artefact tree.
W2 the sidecar is tracked at the same revision, its first line matches the
   grammar above, and its ``sha256`` equals the sha256 of the target blob.
   Appending a real dump to a waived file changes the sha and voids the
   waiver (the finding returns as ``reason=sha-mismatch``).
W3 the registry line repeats the same path, sha256, rule list and kind. A
   sidecar without a registry line is rejected (``reason=unregistered``): a
   seat cannot invent a waiver while writing its own fixture.
W4 ``kind=gate-copy`` requires the target blob to be byte-identical to the
   gate source (``--gate-source``, default
   ``quality/check-session-material.py``) at the same revision, so the only
   file that kind can cover is the gate itself with its selftest constants.
   ``kind=fixture`` requires every value the rule matched to sit in a reserved
   synthetic namespace (``SYNTH_TITLE_RE``, ``SYNTH_SERIAL_RE``,
   ``SYNTH_VENDOR_RE``, ``SYNTH_PROG_RE``, ``SYNTH_HOME_USER_RE``): a title
   exactly ``redacted``/``a live window title`` or one of the fixture prefixes
   ``synthetic-``/``fixture-``/``selftest-`` followed by anything (case and
   delimiter both matter, so a real title that merely starts with a reserved
   word is refused), a serial ``SN0…``
   beside a ``Fake``/``Example`` make, process rows whose program is named
   ``synthetic-…`` with pid <= 1024, home paths under ``/home/example`` or
   ``/home/someone``. A real title, a real serial, a live pid or a real home
   user fails W4 and the finding stands (``reason=value-not-synthetic``).

The marker covers R1-R4 only, and structurally so: ``rules=`` must name
``R[1-4]_…`` (a sidecar naming ``R5_SERIAL_PROSE`` or ``R6_SERIAL_EXACT`` is
``marker-malformed``), and a serial finding on a file that *has* a sidecar is
refused with ``reason=serial-rule-not-waivable`` before the marker is even
parsed. There is no reserved namespace for a serial: its identity is the
value, so a real serial can never be waived — only removed or redacted.

Every honoured waiver is printed (``WAIVER file=… rule=… kind=…``), every
refused marker with its reason (``WAIVER_REJECTED file=… rule=… reason=…``),
and the count is printed as
``SESSION_MATERIAL_WAIVED: findings=<n> files=<n>`` before the summary line,
so suppression is never silent. ``--no-waivers`` ignores markers entirely.

Deliberate limits (declared, not hidden): findings name the file, the rule and
counts only — never a title, a program name, a serial, a description or a home
path, so the gate's own output is safe to paste into a receipt. Binary blobs
(a NUL byte in the first 8 KiB) are skipped for text rules. Files larger than
16 MiB are scanned for *every* rule, but only over their first 16 MiB: the
tail is not read and no line reports that size cut (the ``truncated=True``
detail belongs to the 20000-object scan limit, not to size). A blob of that
size carrying material in its tail therefore reads clean. A client dump split
across several files is still caught
per file; a dump whose ``class`` value is empty is not a clients dump. R5 is a
shape rule: a serial with lowercase letters, separators, a capital run of two
or fewer, or a trailing digit run of fewer than three is not matched by it and
is only caught by R6 under ``--serial-from-host``; conversely a non-serial
token of that same shape is flagged. ``--serial-from-host`` runs one
``hyprctl monitors all -j`` read (the only non-git subprocess this gate ever
starts) and prints counts, never values.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

MAX_TEXT = 16 << 20
MAX_OBJECTS = 20000
DEFAULT_HOME_LIMIT = 10

TOOL = "check-session-material.py"

PROC_RE = re.compile(r'users:\(\("[^"]{0,128}",pid=\d+')
PROC_ROW_RE = re.compile(r'users:\(\("([^"]{0,128})",pid=(\d+)')
HOME_PATH_RE = re.compile(r'^/home/[A-Za-z0-9._-]+(?:/[^\s]*)?/?$')
HOME_USER_RE = re.compile(r"^/home/([A-Za-z0-9._-]+)")
SERIAL_PROSE_RE = re.compile(r"(?<![0-9A-Za-z])[0-9]{2,6}[A-Z]{3,8}[0-9]{3,7}(?![0-9A-Za-z])")

SERIAL_MIN = 4
HOST_CMD = ("hyprctl", "monitors", "all", "-j")

R1 = "R1_CLIENT_DUMP"
R2 = "R2_PROC_TABLE"
R3 = "R3_MONITOR_IDENT"
R4 = "R4_HOME_LISTING"
R5 = "R5_SERIAL_PROSE"
R6 = "R6_SERIAL_EXACT"
RULES = (R1, R2, R3, R4, R5, R6)
SERIAL_RULES = (R5, R6)
# The marker may only name rules that have a reserved synthetic namespace.
WAIVABLE_RULES = (R1, R2, R3, R4)

MARKER_SUFFIX = ".synthetic"
DEFAULT_WAIVERS = "quality/session-material-waivers.txt"
DEFAULT_GATE_SOURCE = "quality/check-session-material.py"
WAIVER_ROOTS = (".ufo/waves/",)

MARKER_RE = re.compile(
    r"^SYNTHETIC-MATERIAL v1 kind=(fixture|gate-copy)"
    r" rules=((?:R[1-4]_[A-Z_]+)(?:,(?:R[1-4]_[A-Z_]+))*)"
    r" sha256=([0-9a-f]{64})$"
)
# The rule band above is R1-R4 on purpose: R5_SERIAL_PROSE and R6_SERIAL_EXACT
# have no reserved namespace (a serial's identity is its value), so a sidecar
# that names one is malformed and apply_waivers() refuses a serial finding on a
# marked file before it even parses the marker.

# Reserved synthetic namespaces. A value outside them cannot be waived: a real
# title, serial, process row or home user fails W4 and the finding stands.
# A title is free text, so its namespace is exact and case-sensitive: a real
# world title that merely starts with a reserved word ("Example Domain",
# "Demo") must not be waivable. Only a reserved word standing alone, or one of
# the three fixture prefixes followed by a *mandatory* delimiter, is synthetic.
# (The round-47 draft matched the bare words -- and case-insensitively -- which
# waived real titles; see round-48 w1/ExecSessionMarker.md F1.)
SYNTH_TITLE_RE = re.compile(
    r"^(?:a live window title|another live window title|redacted)$"
    r"|^(?:synthetic|fixture|selftest)[ -][A-Za-z0-9 ._-]{0,60}$"
)
SYNTH_SERIAL_RE = re.compile(
    r"^(?:sn0+|serial0+|synthetic[-a-z0-9]*|fake[-a-z0-9]*|example[-a-z0-9]*"
    r"|redacted|0+)$",
    re.IGNORECASE,
)
SYNTH_VENDOR_RE = re.compile(r"(?:fake|example|synthetic|selftest|redacted)", re.IGNORECASE)
SYNTH_MODEL_RE = re.compile(
    r"^(?:0x0+|fake[-a-z0-9]*|example[-a-z0-9]*|synthetic[-a-z0-9]*|redacted)$",
    re.IGNORECASE,
)
SYNTH_PROG_RE = re.compile(
    r"^(?:synthetic|fixture|selftest|fake|probe|example)[-a-z0-9]*$", re.IGNORECASE
)
SYNTH_HOME_USER_RE = re.compile(
    r"^(?:example|someone|selftest|fixture|synthetic|redacted|user)$", re.IGNORECASE
)
SYNTH_PID_MAX = 1024

_MISS = object()


class GateError(Exception):
    pass


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _is_client(obj):
    if not isinstance(obj, dict):
        return False
    if not _nonempty(obj.get("class")):
        return False
    return _nonempty(obj.get("title")) or _nonempty(obj.get("initialTitle"))


def _monitor_reason(obj):
    """Return a short tag when *obj* identifies a physical monitor, else None."""
    if not isinstance(obj, dict) or not _nonempty(obj.get("serial")):
        return None
    for key in ("description", "make", "model"):
        if _nonempty(obj.get(key)):
            return key
    return None


def _count_objects(root, pred):
    """Count dicts in *root* (recursively) for which pred(dict) is truthy."""
    hits = 0
    stack = [root]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            if pred(cur):
                hits += 1
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
    return hits


def scan_json_objects(text, all_sub, any_sub, pred, limit=MAX_OBJECTS):
    """Return (hits, objects_examined, truncated) for embedded JSON objects.

    *all_sub* must all appear in *text*, and one of *any_sub* must appear, or
    the scan returns at once: those substrings are the keys a match needs, so
    a file without them cannot hold a matching object.
    """
    for sub in all_sub:
        if sub not in text:
            return 0, 0, False
    if any_sub and not any(sub in text for sub in any_sub):
        return 0, 0, False

    try:
        whole = json.loads(text)
    except ValueError:
        whole = _MISS
    if whole is not _MISS:
        return _count_objects(whole, pred), 1, False

    decoder = json.JSONDecoder()
    hits = 0
    examined = 0
    truncated = False
    pos = 0
    while True:
        pos = text.find("{", pos)
        if pos < 0:
            break
        if examined >= limit:
            truncated = True
            break
        examined += 1
        try:
            obj, end = decoder.raw_decode(text, pos)
        except ValueError:
            pos += 1
            continue
        if isinstance(obj, (dict, list)):
            hits += _count_objects(obj, pred)
        pos = end
    return hits, examined, truncated


def scan_home_listing(text, limit):
    """Return distinct bare absolute /home/<user>/... lines above *limit*."""
    seen = set()
    for line in text.splitlines():
        entry = line.strip()
        if not entry or any(ch.isspace() for ch in entry):
            continue
        if HOME_PATH_RE.match(entry):
            seen.add(entry)
    if len(seen) > limit:
        return len(seen), limit
    return 0, limit


def decode(data):
    if not data or b"\x00" in data[:8192]:
        return None
    if len(data) > MAX_TEXT:
        data = data[:MAX_TEXT]
    return data.decode("utf-8", "replace")


def _shape_mask(token):
    """Return a run-length digit/capital mask of *token* (``9x3+Ax5+9x4``).

    The token text is never kept, and the mask is delimited so that it can
    never itself read as a serial-shaped token when a receipt quotes it.
    """
    runs = []
    for ch in token:
        kind = "9" if ch.isdigit() else "A"
        if runs and runs[-1][0] == kind:
            runs[-1][1] += 1
        else:
            runs.append([kind, 1])
    return "+".join("%sx%d" % (kind, count) for kind, count in runs)


def scan_blob(data, home_limit, serials=()):
    """Return findings as (rule, count, detail) tuples for one blob."""
    findings = []
    text = decode(data)
    if text is None:
        return findings

    rows = len(PROC_RE.findall(text))
    if rows:
        findings.append((R2, rows, "rows=%d" % rows))

    distinct, limit = scan_home_listing(text, home_limit)
    if distinct:
        findings.append((R4, distinct, "distinct_paths=%d limit=%d" % (distinct, limit)))

    hits, examined, truncated = scan_json_objects(
        text, ('"class"',), ('"title"', '"initialTitle"'), _is_client
    )
    if hits:
        keys = []
        if '"title"' in text:
            keys.append("title")
        if '"initialTitle"' in text:
            keys.append("initialTitle")
        detail = "objects=%d keys=%s" % (hits, "+".join(keys) or "?")
        if truncated:
            detail += " truncated=True"
        findings.append((R1, hits, detail))

    hits, examined, truncated = scan_json_objects(
        text, ('"serial"',), ('"description"', '"make"', '"model"'),
        lambda obj: _monitor_reason(obj) is not None,
    )
    if hits:
        detail = "objects=%d keys=serial+ident" % hits
        if truncated:
            detail += " truncated=True"
        findings.append((R3, hits, detail))

    shapes = {}
    for match in SERIAL_PROSE_RE.finditer(text):
        mask = _shape_mask(match.group(0))
        shapes[mask] = shapes.get(mask, 0) + 1
    if shapes:
        total = sum(shapes.values())
        shown = sorted(shapes)
        detail = "tokens=%d shapes=%s" % (
            total, "+".join(shown[:3]) + ("+..." if len(shown) > 3 else ""))
        findings.append((R5, total, detail))

    if serials:
        count = sum(text.count(value) for value in serials)
        if count:
            findings.append((R6, count, "count=%d sources=%d" % (count, len(serials))))

    return findings


# ------------------------------------------------------------ host serial(s)


def serials_from_json(text, minimum=SERIAL_MIN):
    """Return the set of non-empty ``serial`` values in a JSON dump.

    The values are returned, never logged: callers count them, they do not
    print them. Values shorter than *minimum* are ignored as non-serials.
    """
    try:
        data = json.loads(text)
    except ValueError:
        raise GateError("monitor dump is not JSON")
    found = set()
    stack = [data]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            value = cur.get("serial")
            if isinstance(value, str) and len(value.strip()) >= minimum:
                found.add(value.strip())
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
    return found


def host_serials(cmd=HOST_CMD):
    """Read the live monitor serial(s) via *cmd*; values stay in memory.

    Returns a sorted tuple of values. Any failure — binary missing, non-zero
    exit, no JSON, no non-empty serial — is a GateError, so the mode can never
    pass by accident. No value is ever put in an error message.
    """
    try:
        proc = subprocess.run(
            list(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    except OSError as exc:
        raise GateError("cannot run %s: %s" % (cmd[0], exc.strerror))
    if proc.returncode != 0:
        raise GateError("%s exited %d" % (cmd[0], proc.returncode))
    found = serials_from_json(proc.stdout.decode("utf-8", "replace"))
    if not found:
        raise GateError("%s reported no serial" % cmd[0])
    return tuple(sorted(found))


# ------------------------------------------------------- synthetic waivers


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def _walk_dicts(root):
    stack = [root]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            yield cur
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def _candidate_roots(text, all_sub, any_sub, limit=MAX_OBJECTS):
    """Yield decoded JSON roots that could hold a match (whole or embedded)."""
    for sub in all_sub:
        if sub not in text:
            return
    if any_sub and not any(sub in text for sub in any_sub):
        return
    try:
        whole = json.loads(text)
    except ValueError:
        whole = _MISS
    if whole is not _MISS:
        yield whole
        return
    decoder = json.JSONDecoder()
    pos = 0
    examined = 0
    while examined < limit:
        pos = text.find("{", pos)
        if pos < 0:
            return
        examined += 1
        try:
            obj, end = decoder.raw_decode(text, pos)
        except ValueError:
            pos += 1
            continue
        yield obj
        pos = end


def matched_values(rule, text):
    """Return the identity values *rule* matched in *text* (for W4)."""
    values = []
    if rule == R1:
        for root in _candidate_roots(text, ('"class"',), ('"title"', '"initialTitle"')):
            for obj in _walk_dicts(root):
                if not _is_client(obj):
                    continue
                for key in ("title", "initialTitle"):
                    if _nonempty(obj.get(key)):
                        values.append((key, obj[key]))
    elif rule == R3:
        for root in _candidate_roots(text, ('"serial"',), ('"description"', '"make"', '"model"')):
            for obj in _walk_dicts(root):
                if _monitor_reason(obj) is None:
                    continue
                for key in ("serial", "description", "make", "model"):
                    if _nonempty(obj.get(key)):
                        values.append((key, obj[key]))
    elif rule == R2:
        for program, pid in PROC_ROW_RE.findall(text):
            values.append((program, pid))
    elif rule == R4:
        for line in text.splitlines():
            entry = line.strip()
            if not entry or any(ch.isspace() for ch in entry):
                continue
            match = HOME_USER_RE.match(entry)
            if match and HOME_PATH_RE.match(entry):
                values.append((match.group(1), entry))
    return values


def waiver_values_ok(rule, text):
    """W4 for kind=fixture: every matched value is in a reserved namespace."""
    values = matched_values(rule, text)
    if not values:
        return False, "no-values"
    if rule == R1:
        for key, value in values:
            if not SYNTH_TITLE_RE.match(value.strip()):
                return False, "title-not-synthetic"
    elif rule == R3:
        for key, value in values:
            if key == "serial":
                if not SYNTH_SERIAL_RE.match(value.strip()):
                    return False, "serial-not-synthetic"
            elif key == "model":
                if not SYNTH_MODEL_RE.match(value.strip()):
                    return False, "model-not-synthetic"
            elif not SYNTH_VENDOR_RE.search(value):
                return False, "vendor-not-synthetic"
    elif rule == R2:
        for program, pid in values:
            if not SYNTH_PROG_RE.match(program.strip()):
                return False, "program-not-synthetic"
            if int(pid) > SYNTH_PID_MAX:
                return False, "pid-above-reserved-band"
    elif rule == R4:
        for user, _path in values:
            if not SYNTH_HOME_USER_RE.match(user):
                return False, "home-user-not-synthetic"
    else:
        return False, "unknown-rule"
    return True, ""


def load_registry(repo, sha, relpath):
    """Return ({path: (sha256, frozenset(rules), kind)}, note)."""
    if relpath.startswith(".ufo/") or "/.ufo/" in relpath:
        return {}, "registry-in-ufo"
    try:
        raw = _git(repo, "show", "%s:%s" % (sha, relpath))
    except GateError:
        return {}, "registry-absent"
    entries = {}
    for line in raw.decode("utf-8", "replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) != 4:
            continue
        path, digest, rules, kind = fields
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            continue
        kind_match = re.fullmatch(r"kind=(fixture|gate-copy)", kind)
        if kind_match is None:
            continue
        # A row can only name rules that have a reserved synthetic namespace.
        rulelist = [rule for rule in rules.split(",") if rule]
        if not rulelist or any(rule not in WAIVABLE_RULES for rule in rulelist):
            continue
        entries[path] = (digest, frozenset(rulelist), kind_match.group(1))
    return entries, None


def apply_waivers(repo, sha, findings, by_path, data_by_blob,
                  waivers_rel, gate_source_rel):
    """Return (waived, rejected); *waived* is [(path, rule, kind)]."""
    waived = []
    rejected = []
    if not findings:
        return waived, rejected
    registry, reg_note = load_registry(repo, sha, waivers_rel)

    sidecar_shas = []
    for path, _rule, _count, _detail in findings:
        blob = by_path.get(path + MARKER_SUFFIX)
        if blob is not None and blob not in data_by_blob and blob not in sidecar_shas:
            sidecar_shas.append(blob)
    side_data = dict(data_by_blob)
    if sidecar_shas:
        for blob_sha, data in iter_blobs(repo, sidecar_shas):
            side_data[blob_sha] = data

    gate_sha = _MISS
    for path, rule, _count, _detail in findings:
        sidecar_blob = by_path.get(path + MARKER_SUFFIX)
        if sidecar_blob is None:
            continue
        if rule in SERIAL_RULES:
            # No reserved namespace exists for a serial value; a marker can
            # never cover it, whatever the sidecar claims.
            rejected.append((path, rule, "serial-rule-not-waivable"))
            continue
        text = decode(side_data.get(sidecar_blob, b"")) or ""
        first = text.splitlines()[0].strip() if text.splitlines() else ""
        marker = MARKER_RE.match(first)
        if marker is None:
            rejected.append((path, rule, "marker-malformed"))
            continue
        kind = marker.group(1)
        rulelist = marker.group(2).split(",")
        marked_sha = marker.group(3)
        if rule not in rulelist:
            rejected.append((path, rule, "rule-not-listed"))
            continue
        target_blob = by_path.get(path)
        target_data = data_by_blob.get(target_blob)
        if target_data is None or sha256_hex(target_data) != marked_sha:
            rejected.append((path, rule, "sha-mismatch"))
            continue
        if not path.startswith(WAIVER_ROOTS):
            rejected.append((path, rule, "path-outside-waves"))
            continue
        if reg_note is not None:
            rejected.append((path, rule, reg_note))
            continue
        entry = registry.get(path)
        if entry is None:
            rejected.append((path, rule, "unregistered"))
            continue
        reg_sha, reg_rules, reg_kind = entry
        if reg_sha != marked_sha:
            rejected.append((path, rule, "registry-sha-mismatch"))
            continue
        if reg_rules != frozenset(rulelist):
            rejected.append((path, rule, "registry-rule-mismatch"))
            continue
        if reg_kind != kind:
            rejected.append((path, rule, "registry-kind-mismatch"))
            continue
        if kind == "gate-copy":
            if gate_sha is _MISS:
                try:
                    gate_sha = sha256_hex(_git(repo, "show", "%s:%s" % (sha, gate_source_rel)))
                except GateError:
                    gate_sha = ""
            if gate_sha != marked_sha:
                rejected.append((path, rule, "gate-source-mismatch"))
                continue
        else:
            ok, why = waiver_values_ok(rule, decode(target_data) or "")
            if not ok:
                rejected.append((path, rule, "value-not-synthetic:" + why))
                continue
        waived.append((path, rule, kind))
    return waived, rejected


# ---------------------------------------------------------------- git access


def _git(repo, *args, text=False):
    proc = subprocess.run(
        ["git", "-C", repo, *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise GateError(
            "git %s failed: %s" % (" ".join(args), proc.stderr.decode("utf-8", "replace").strip())
        )
    return proc.stdout.decode("utf-8", "replace") if text else proc.stdout


def resolve_rev(repo, rev):
    return _git(repo, "rev-parse", "--verify", rev + "^{commit}", text=True).strip()


def list_tree(repo, sha, paths=(".ufo",)):
    """Return [(blob_sha, path)] for every tracked file under *paths* at *sha*."""
    raw = _git(repo, "ls-tree", "-r", "-z", sha, "--", *paths)
    entries = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        fields = meta.split(b" ")
        if len(fields) != 3:
            continue
        mode, kind, osha = fields
        if kind != b"blob":
            continue
        entries.append((osha.decode("ascii"), path.decode("utf-8", "surrogateescape")))
    return entries


def _read_exact(stream, size):
    chunks = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise GateError("cat-file stream ended %d bytes early" % remaining)
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def iter_blobs(repo, shas):
    """Yield (sha, data) for *shas* in request order, via cat-file --batch.

    The request list goes through a file, not a pipe: a pipe can deadlock once
    the child's stdout buffer fills while the parent is still writing stdin.
    """
    request = tempfile.NamedTemporaryFile("wb", delete=False)
    try:
        request.write(("\n".join(shas) + "\n").encode("ascii"))
        request.close()
        with open(request.name, "rb") as stdin:
            proc = subprocess.Popen(
                ["git", "-C", repo, "cat-file", "--batch"],
                stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            try:
                for requested in shas:
                    header = proc.stdout.readline()
                    if not header:
                        raise GateError("cat-file produced no header for %s" % requested)
                    header = header.rstrip(b"\n")
                    if header.endswith(b" missing"):
                        continue
                    parts = header.split(b" ")
                    if len(parts) != 3:
                        raise GateError("unexpected cat-file header: %r" % header)
                    size = int(parts[2])
                    data = _read_exact(proc.stdout, size)
                    proc.stdout.read(1)  # trailing newline after the object
                    yield requested, data
            finally:
                proc.stdout.close()
                rc = proc.wait()
                err = proc.stderr.read().decode("utf-8", "replace").strip()
                proc.stderr.close()
                if rc != 0:
                    raise GateError("cat-file exited %d: %s" % (rc, err))
    finally:
        try:
            os.unlink(request.name)
        except OSError:
            pass


def run(repo, rev, home_limit=DEFAULT_HOME_LIMIT, waivers=DEFAULT_WAIVERS,
        gate_source=DEFAULT_GATE_SOURCE, use_waivers=True, scope="ufo", serials=()):
    """Return (rev_sha, files_scanned, findings, waived, rejected)."""
    sha = resolve_rev(repo, rev)
    entries = list_tree(repo, sha, (".ufo",) if scope == "ufo" else (".",))
    order = []
    seen = set()
    by_path = {}
    for blob_sha, path in entries:
        by_path[path] = blob_sha
        if blob_sha not in seen:
            seen.add(blob_sha)
            order.append(blob_sha)

    per_blob = {}
    data_by_blob = {}
    if order:
        for blob_sha, data in iter_blobs(repo, order):
            found = scan_blob(data, home_limit, serials)
            per_blob[blob_sha] = found
            if found:
                data_by_blob[blob_sha] = data

    findings = []
    for blob_sha, path in entries:
        for rule, count, detail in per_blob.get(blob_sha, ()):
            findings.append((path, rule, count, detail))
    findings.sort(key=lambda item: (item[0], item[1]))

    waived = []
    rejected = []
    if use_waivers:
        waived, rejected = apply_waivers(
            repo, sha, findings, by_path, data_by_blob, waivers, gate_source
        )
        dropped = set((path, rule) for path, rule, _kind in waived)
        findings = [item for item in findings if (item[0], item[1]) not in dropped]
    return sha, len(entries), findings, waived, rejected


def emit(sha, files, findings, waived=(), rejected=(), stream=sys.stdout):
    for path, rule, kind in waived:
        stream.write("WAIVER file=%s rule=%s kind=%s\n" % (path, rule, kind))
    for path, rule, reason in rejected:
        stream.write("WAIVER_REJECTED file=%s rule=%s reason=%s\n" % (path, rule, reason))
    for path, rule, count, detail in findings:
        stream.write("FINDING file=%s rule=%s count=%d detail=%s\n" % (path, rule, count, detail))
    tally = []
    for rule in RULES:
        rows = [item for item in findings if item[1] == rule]
        if rows:
            tally.append("%s=%d" % (rule, len(rows)))
    if tally:
        stream.write("SESSION_MATERIAL_RULES: %s\n" % " ".join(tally))
    if waived:
        stream.write(
            "SESSION_MATERIAL_WAIVED: findings=%d files=%d\n"
            % (len(waived), len(set(item[0] for item in waived)))
        )
    stream.write("SESSION_MATERIAL: files=%d findings=%d rev=%s\n" % (files, len(findings), sha))
    return 1 if findings else 0


# ------------------------------------------------------------------ selftest

CLIENT_DUMP = """[
 {
  "address": "0x55aa",
  "mapped": true,
  "class": "Alacritty",
  "title": "a live window title",
  "initialTitle": "Alacritty",
  "pid": 2562
 },
 {
  "address": "0x55bb",
  "mapped": true,
  "class": "OrgExampleApp",
  "title": "another live window title",
  "initialTitle": "OrgExampleApp",
  "pid": 4100
 }
]
"""

EMBEDDED_CLIENTS = """# receipt

Command: `hyprctl clients -j`

```json
[{"address": "0x1", "class": "Foot", "title": "fenced title", "pid": 7}]
```

verdict kept.
"""

EMPTY_TITLE = '[{"address": "0x2", "class": "Foot", "title": "", "initialTitle": ""}]\n'

NO_CLIENT = '{"class": "Alacritty", "size": [100, 200]}\n'

PROSE_KEYS = "The keys `class` and `title` sit in the same object; this line is prose only.\n"

SS_TABLE = """Netid State Recv-Q Send-Q Local Address:Port Peer Address:Port Process
u_str ESTAB 0      0      /run/user/1000/bus 12345 * 23456 users:(("gnome-keyring-d",pid=999,fd=9))
u_str ESTAB 0      0      /run/user/1000/pipe 12346 * 23457 users:(("ssh-agent",pid=1000,fd=3))
"""

SS_PROSE = "I ran `ss -xpa` and looked for users:(( entries but none had a pid column worth quoting.\n"

MONITORS_DUMP = """[
 {
  "name": "DP-1",
  "description": "Example Monitor Model ABC",
  "make": "Example",
  "model": "ABC",
  "serial": "SERIAL0123456",
  "width": 3440,
  "height": 1440
 }
]
"""

MONITORS_REDACTED = """[
 {
  "name": "DP-1",
  "description": "",
  "make": "Example",
  "model": "ABC",
  "serial": ""
 }
]
"""

HOME_LISTING = "\n".join("/home/someone/dir%02d/file.txt" % i for i in range(12)) + "\n"
HOME_SHORT = "\n".join("/home/someone/dir%02d/file.txt" % i for i in range(3)) + "\n"
HOME_PROSE = "Wrote to /home/someone/a.txt then to /home/someone/b.txt and /home/someone/c.txt.\n"

PROJECTION = """[
 {
  "address": "0x55aa",
  "mapped": true,
  "class": "Alacritty",
  "floating": false,
  "size": [
   1720,
   1414
  ],
  "at": [
   0,
   26
  ],
  "monitor": 0
 }
]
"""

CONFIG_LINE = "monitor = DP-1, 3440x1440@100, 0x0, 1\n"


def _parts(*chunks):
    """Join fixture chunks so this file's own bytes never hold a serial token."""
    return "".join(chunks)


SYNTH_SERIAL = _parts("481", "QZRTM", "9027")
SYNTH_LOWER = _parts("481", "qzrtm", "9027")
SYNTH_TWO_CAPS = _parts("90", "QZ", "9027")
SYNTH_ABSENT = _parts("777", "PLMKQ", "3210")
LOOKS_REAL_SERIAL = _parts("881", "WXKPD", "4417")

SERIAL_PROSE = "The panel reports serial %s in the ladder, then stops.\n" % SYNTH_SERIAL
SERIAL_TABLE = "| field | value |\n| serial | `%s` |\n" % SYNTH_SERIAL
SERIAL_JSON = '{"name": "DP-1", "serial": "%s"}\n' % SYNTH_SERIAL
SERIAL_LOWER = "The panel serial is %s here.\n" % SYNTH_LOWER
SERIAL_STAMP = "Captured 20261026T152026Z on the host; no serial follows.\n"
SERIAL_GLUED = "Identifier X%s is glued to an alphanumeric prefix.\n" % SYNTH_SERIAL
SERIAL_TWO_CAPS = "Field %s carries a two-letter capital run.\n" % SYNTH_TWO_CAPS
SERIAL_DUMP = '[{"name": "DP-1", "serial": "%s"}, {"name": "HDMI-A-1", "serial": ""}]\n' % SYNTH_SERIAL


class Selftest:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.passed = 0
        self.failed = 0

    def check(self, name, ok, detail=""):
        if ok:
            self.passed += 1
            status = "ok"
        else:
            self.failed += 1
            status = "FAIL"
        line = "SELFTEST %s case=%s" % (status, name)
        if detail and (self.verbose or not ok):
            line += " " + detail
        print(line)
        return ok


def _unit_cases(suite, home_limit=DEFAULT_HOME_LIMIT):
    def findings(text, home_limit=home_limit, serials=()):
        return dict((rule, count)
                    for rule, count, _detail in scan_blob(text.encode(), home_limit, serials))

    def details(text, serials=()):
        return dict((rule, (count, detail))
                    for rule, count, detail in scan_blob(text.encode(), home_limit, serials))

    got = findings(CLIENT_DUMP)
    suite.check("r1-whole-file-two-clients", got.get(R1) == 2, "got=%r" % (got,))

    got = findings(EMBEDDED_CLIENTS)
    suite.check("r1-embedded-fenced-one-client", got.get(R1) == 1, "got=%r" % (got,))

    got = findings(EMPTY_TITLE)
    suite.check("r1-empty-title-not-a-finding", R1 not in got, "got=%r" % (got,))

    got = findings(NO_CLIENT)
    suite.check("r1-class-only-not-a-finding", R1 not in got, "got=%r" % (got,))

    got = findings(PROSE_KEYS)
    suite.check("r1-prose-keys-not-a-finding", R1 not in got, "got=%r" % (got,))

    got = findings(PROJECTION)
    suite.check("r1-seven-key-projection-clean", not got, "got=%r" % (got,))

    got = findings(CONFIG_LINE)
    suite.check("r1-monitor-rule-line-clean", not got, "got=%r" % (got,))

    got = findings(SS_TABLE)
    suite.check("r2-two-process-rows", got.get(R2) == 2, "got=%r" % (got,))

    got = findings(SS_PROSE)
    suite.check("r2-prose-without-pid-clean", R2 not in got, "got=%r" % (got,))

    got = findings(MONITORS_DUMP)
    suite.check("r3-monitor-identity", got.get(R3) == 1, "got=%r" % (got,))

    got = findings(MONITORS_REDACTED)
    suite.check("r3-empty-serial-clean", R3 not in got, "got=%r" % (got,))

    got = findings(HOME_LISTING)
    suite.check("r4-twelve-entry-listing", got.get(R4) == 12, "got=%r" % (got,))

    got = findings(HOME_SHORT)
    suite.check("r4-three-entry-listing-under-limit", R4 not in got, "got=%r" % (got,))

    got = findings(HOME_PROSE)
    suite.check("r4-inline-paths-clean", R4 not in got, "got=%r" % (got,))

    got = findings(HOME_LISTING, home_limit=12)
    suite.check("r4-limit-threshold-inclusive-at-12", R4 not in got, "got=%r" % (got,))

    got = findings(SERIAL_PROSE)
    suite.check("r5-prose-serial", got.get(R5) == 1, "got=%r" % (got,))

    got = findings(SERIAL_TABLE)
    suite.check("r5-table-cell-serial", got.get(R5) == 1, "got=%r" % (got,))

    got = findings(SERIAL_JSON)
    suite.check("r5-json-serial-without-ident", got.get(R5) == 1 and R3 not in got,
                "got=%r" % (got,))

    got = findings(SERIAL_STAMP)
    suite.check("r5-iso-timestamp-clean", R5 not in got, "got=%r" % (got,))

    got = findings(SERIAL_LOWER)
    suite.check("r5-lowercase-run-clean", R5 not in got, "got=%r" % (got,))

    got = findings(SERIAL_GLUED)
    suite.check("r5-glued-to-prefix-clean", R5 not in got, "got=%r" % (got,))

    got = findings(SERIAL_TWO_CAPS)
    suite.check("r5-two-letter-capital-run-clean", R5 not in got, "got=%r" % (got,))

    got = details(SERIAL_PROSE)
    suite.check("r5-detail-masks-token",
                got.get(R5) is not None and SYNTH_SERIAL not in got[R5][1]
                and got[R5][1] == "tokens=1 shapes=9x3+Ax5+9x4",
                "detail=%r" % (got.get(R5)[1] if got.get(R5) else None,))

    got = findings(SERIAL_PROSE, serials=(SYNTH_SERIAL,))
    suite.check("r6-exact-in-prose", got.get(R6) == 1, "got=%r" % (got,))

    got = findings(SERIAL_LOWER, serials=(SYNTH_LOWER,))
    suite.check("r6-exact-shape-independent", got.get(R6) == 1 and R5 not in got,
                "got=%r" % (got,))

    got = findings(SERIAL_PROSE, serials=("not-in-this-blob-0000",))
    suite.check("r6-absent-clean", R6 not in got, "got=%r" % (got,))

    got = details(SERIAL_PROSE, serials=(SYNTH_SERIAL,))
    suite.check("r6-detail-counts-only",
                got.get(R6) is not None and got[R6][1] == "count=1 sources=1",
                "detail=%r" % (got.get(R6)[1] if got.get(R6) else None,))

    got = findings(PROSE_KEYS)
    suite.check("r5-prose-without-serial-clean", R5 not in got, "got=%r" % (got,))

    dump = serials_from_json(SERIAL_DUMP)
    suite.check("serials-from-json-one-value",
                dump == {SYNTH_SERIAL}, "n=%d" % len(dump))

    dump = serials_from_json('[{"serial": ""}, {"serial": "  "}]')
    suite.check("serials-from-json-empty-ignored", dump == set(), "n=%d" % len(dump))

    dump = serials_from_json('[{"serial": "ab"}]')
    suite.check("serials-from-json-short-ignored", dump == set(), "n=%d" % len(dump))

    try:
        serials_from_json("not json at all")
    except GateError:
        suite.check("serials-from-json-rejects-garbage", True)
    else:
        suite.check("serials-from-json-rejects-garbage", False, "no GateError")

    # This file's own bytes must never trip the rules it documents.
    with open(os.path.abspath(__file__), "rb") as handle:
        own = scan_blob(handle.read(), home_limit, (SYNTH_SERIAL, SYNTH_LOWER))
    own_rules = set(rule for rule, _count, _detail in own)
    suite.check("self-source-serial-rules-clean",
                R5 not in own_rules and R6 not in own_rules, "rules=%r" % (sorted(own_rules),))

    suite.check("rules-partition-is-waivable-plus-serial",
                tuple(WAIVABLE_RULES) + tuple(SERIAL_RULES) == RULES,
                "rules=%r" % (RULES,))


def _commit_fixture(root, files):
    paths = []
    for relpath, text in files.items():
        target = os.path.join(root, relpath)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(text)
        paths.append(relpath)
    subprocess.run(["git", "-C", root, "init", "-q"], check=True)
    subprocess.run(["git", "-C", root, "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", root, "-c", "user.name=selftest",
         "-c", "user.email=selftest@scratch.invalid", "commit", "-q", "-m", "fixtures"],
        check=True,
    )
    top = subprocess.run(
        ["git", "-C", root, "rev-parse", "--show-toplevel"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(root):
        raise GateError("fixture toplevel %r != %r" % (top, root))


def _e2e_cases(suite, scratch):
    positives = {
        ".ufo/w1/clients-live.json": CLIENT_DUMP,
        ".ufo/w1/embedded.md": EMBEDDED_CLIENTS,
        ".ufo/w1/ss-live.txt": SS_TABLE,
        ".ufo/w1/monitors-live.json": MONITORS_DUMP,
        ".ufo/w1/home-listing.txt": HOME_LISTING,
        ".ufo/w1/serial-prose.md": SERIAL_PROSE,
        ".ufo/w1/serial-table.md": SERIAL_TABLE,
        ".ufo/w1/serial-only.json": SERIAL_JSON,
    }
    negatives = {
        ".ufo/w2/projection.json": PROJECTION,
        ".ufo/w2/monitors-redacted.json": MONITORS_REDACTED,
        ".ufo/w2/env.txt": HOME_SHORT,
        ".ufo/w2/rule.conf": CONFIG_LINE,
        ".ufo/w2/prose.md": SS_PROSE + PROSE_KEYS,
        ".ufo/w2/empty-title.json": EMPTY_TITLE,
        ".ufo/w2/serial-lower.md": SERIAL_LOWER,
        ".ufo/w2/serial-stamp.md": SERIAL_STAMP,
        ".ufo/w2/serial-glued.md": SERIAL_GLUED,
        ".ufo/w2/serial-two-caps.md": SERIAL_TWO_CAPS,
    }
    mixed = os.path.join(scratch, "mixed")
    os.makedirs(mixed)
    _commit_fixture(mixed, dict(positives, **negatives))

    sha, files, findings, waived, rejected = run(mixed, "HEAD")
    suite.check("e2e-fixture-files-count", files == len(positives) + len(negatives),
                "files=%d" % files)

    by_path = {}
    for path, rule, count, _detail in findings:
        by_path.setdefault(path, set()).add(rule)
    expected = {
        ".ufo/w1/clients-live.json": {R1},
        ".ufo/w1/embedded.md": {R1},
        ".ufo/w1/ss-live.txt": {R2},
        ".ufo/w1/monitors-live.json": {R3},
        ".ufo/w1/home-listing.txt": {R4},
        ".ufo/w1/serial-prose.md": {R5},
        ".ufo/w1/serial-table.md": {R5},
        ".ufo/w1/serial-only.json": {R5},
    }
    suite.check("e2e-positive-files-rules", by_path == expected, "got=%r" % (by_path,))

    lines = []
    buf = _ListStream(lines)
    code = emit(sha, files, findings, stream=buf)
    summary = lines[-1] if lines else ""
    suite.check("e2e-exit-1-on-findings", code == 1, "code=%d" % code)
    suite.check(
        "e2e-summary-format",
        re.fullmatch(r"SESSION_MATERIAL: files=%d findings=%d rev=[0-9a-f]{40}" % (files, len(findings)),
                    summary) is not None,
        "summary=%r" % (summary,),
    )

    negatives_only = os.path.join(scratch, "clean")
    os.makedirs(negatives_only)
    _commit_fixture(negatives_only, negatives)
    _sha, files, findings, _waived, _rejected = run(negatives_only, "HEAD")
    lines = []
    code = emit(_sha, files, findings, stream=_ListStream(lines))
    suite.check("e2e-negative-repo-exit-0", code == 0 and not findings,
                "code=%d findings=%d" % (code, len(findings)))

    # A non-.ufo file with the same dump must be invisible to the gate.
    outside = os.path.join(scratch, "outside")
    os.makedirs(outside)
    _commit_fixture(outside, {"corpus/leak.json": CLIENT_DUMP, ".ufo/keep.txt": "ok\n"})
    _sha, files, findings, _waived, _rejected = run(outside, "HEAD")
    suite.check("e2e-outside-ufo-not-scanned", not findings and files == 1,
                "files=%d findings=%r" % (files, findings))

    # A revision with nothing tracked under .ufo/ is a clean scan, not an error.
    empty = os.path.join(scratch, "empty")
    os.makedirs(empty)
    _commit_fixture(empty, {"README.md": "no .ufo tree here\n"})
    _sha, files, findings, _waived, _rejected = run(empty, "HEAD")
    lines = []
    code = emit(_sha, files, findings, stream=_ListStream(lines))
    suite.check("e2e-empty-ufo-clean", code == 0 and files == 0 and not findings,
                "code=%d files=%d findings=%r" % (code, files, findings))

    # --scope all sees the same file the default scope hides.
    _sha, files, findings, _waived, _rejected = run(outside, "HEAD", scope="all")
    suite.check("e2e-scope-all-sees-outside-ufo",
                [item[1] for item in findings] == [R1] and files == 2,
                "files=%d findings=%r" % (files, [(item[0], item[1]) for item in findings]))

    # R6 counts the exact value in every carrier and never prints it.
    _sha, _files, findings, _waived, _rejected = run(mixed, "HEAD", serials=(SYNTH_SERIAL,))
    lines = []
    code = emit(_sha, _files, findings, stream=_ListStream(lines))
    r6_paths = sorted(path for path, rule, _c, _d in findings if rule == R6)
    joined = "\n".join(lines)
    suite.check("e2e-r6-hits-every-carrier",
                code == 1 and r6_paths == [".ufo/w1/serial-only.json", ".ufo/w1/serial-prose.md",
                                           ".ufo/w1/serial-table.md", ".ufo/w2/serial-glued.md"],
                "paths=%r" % (r6_paths,))
    suite.check("e2e-r6-output-never-holds-value", SYNTH_SERIAL not in joined,
                "lines=%d" % len(lines))

    # A projection of the leak: same tree, token replaced, R5/R6 clean.
    projected = os.path.join(scratch, "projected")
    os.makedirs(projected)
    _commit_fixture(projected, {
        ".ufo/w1/serial-prose.md": SERIAL_PROSE.replace(SYNTH_SERIAL, "<serial-redacted>"),
        ".ufo/w1/serial-table.md": SERIAL_TABLE.replace(SYNTH_SERIAL, "<serial-redacted>"),
        ".ufo/w1/serial-only.json": SERIAL_JSON.replace(SYNTH_SERIAL, ""),
        ".ufo/w2/serial-lower.md": SERIAL_LOWER.replace(SYNTH_LOWER, "<serial-redacted>"),
        ".ufo/w2/serial-stamp.md": SERIAL_STAMP,
    })
    _sha, _files, findings, _waived, _rejected = run(projected, "HEAD",
                                                     serials=(SYNTH_SERIAL, SYNTH_LOWER))
    lines = []
    code = emit(_sha, _files, findings, stream=_ListStream(lines))
    suite.check("e2e-projected-tree-passes", code == 0 and not findings,
                "code=%d findings=%r" % (code, findings))

    # No flag may drop a rule: --rules is refused, not honoured.
    class _Sink:
        def __init__(self):
            self.text = ""

        def write(self, text):
            self.text += text

        def flush(self):
            pass

    saved = sys.stderr
    sink = _Sink()
    sys.stderr = sink
    try:
        try:
            main(["--repo", empty, "--rules", R3])
        except SystemExit as exc:
            code = exc.code
        else:
            code = "returned"
    finally:
        sys.stderr = saved
    suite.check("e2e-no-rule-can-be-dropped",
                code == 2 and "--rules" in sink.text,
                "code=%r stderr=%r" % (code, sink.text.strip().splitlines()[-1:]))


# ------------------------------------------------------- waiver selftest

MONITORS_SYNTH = (
    '[{"name": "DP-1", "description": "Fake Corp 0x0000 SN00000", "make": "Fake Corp",'
    ' "model": "0x0000", "serial": "SN00000", "width": 3440, "height": 1440}]\n'
)

REAL_MONITORS = (
    '[{"name": "DP-1", "description": "DELL U2720Q 9P3XN53", "make": "Dell Inc.",'
    ' "model": "DELL U2720Q", "serial": "CN0H7Y2K3F", "width": 3840, "height": 2160}]\n'
)

CLIENT_SENTINEL = (
    '[{"address": "0x1", "class": "org.example.fake", "title": "redacted", "pid": 42}]\n'
)

SYNTH_SS = 'u_str ESTAB 0 0 * 3001 * 2001 users:(("synthetic-client",pid=42,fd=7))\n'


def _digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _marker(kind, rules, digest):
    return "SYNTHETIC-MATERIAL v1 kind=%s rules=%s sha256=%s\n" % (
        kind, ",".join(rules), digest)


def _registry(rows):
    return "# path sha256 rules kind\n" + "".join(
        "%s %s %s kind=%s\n" % (path, digest, ",".join(rules), kind)
        for path, digest, rules, kind in rows)


def _waiver_repo(scratch, name, files):
    root = os.path.join(scratch, name)
    os.makedirs(root)
    _commit_fixture(root, files)
    return root


def _append_and_commit(root, relpath, extra):
    with open(os.path.join(root, relpath), "a", encoding="utf-8") as handle:
        handle.write(extra)
    subprocess.run(["git", "-C", root, "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", root, "-c", "user.name=selftest",
         "-c", "user.email=selftest@scratch.invalid", "commit", "-q", "-m", "tamper"],
        check=True,
    )


def _waiver_cases(suite, scratch):
    path = ".ufo/waves/round-46/w1/Seat/fixtures/mons.json"
    digest = _digest(MONITORS_SYNTH)
    waived_files = {
        path: MONITORS_SYNTH,
        path + MARKER_SUFFIX: _marker("fixture", [R3], digest),
        DEFAULT_WAIVERS: _registry([(path, digest, [R3], "fixture")]),
    }
    root = _waiver_repo(scratch, "waived", waived_files)
    sha, files, findings, waived, rejected = run(root, "HEAD")
    suite.check("waiver-fixture-waived",
                not findings and len(waived) == 1 and not rejected,
                "findings=%r waived=%r rejected=%r" % (findings, waived, rejected))
    lines = []
    code = emit(sha, files, findings, waived, rejected, stream=_ListStream(lines))
    suite.check("waiver-exit-0-and-count-line",
                code == 0 and lines[-2].startswith("SESSION_MATERIAL_WAIVED: findings=1 files=1"),
                "code=%d lines=%r" % (code, lines[-2:]))

    real_digest = _digest(REAL_MONITORS)
    real_files = {
        path: REAL_MONITORS,
        path + MARKER_SUFFIX: _marker("fixture", [R3], real_digest),
        DEFAULT_WAIVERS: _registry([(path, real_digest, [R3], "fixture")]),
    }
    real_root = _waiver_repo(scratch, "real-values", real_files)
    _sha, _files, findings, waived, rejected = run(real_root, "HEAD")
    suite.check("waiver-real-values-rejected",
                len(findings) == 1 and not waived
                and rejected == [(path, R3, "value-not-synthetic:serial-not-synthetic")],
                "findings=%r rejected=%r" % (findings, rejected))

    # F1 (round-47 w2 RevSessionMarker): a title is free text, so its reserved
    # namespace is exact. The round-47 draft waived any title that merely
    # started with example/demo/probe (case-insensitively); these cases pin the
    # boundary from both sides.
    for case, title, waivable in (
        ("example-domain", "Example Domain", False),
        ("bare-demo", "Demo", False),
        ("probe-prefix", "probe-session-note", False),
        ("case-only", "Synthetic-window", False),
        ("reserved-prefix", "synthetic-window-1", True),
        ("reserved-exact", "redacted", True),
    ):
        body = CLIENT_SENTINEL.replace('"redacted"', json.dumps(title))
        body_digest = _digest(body)
        case_path = ".ufo/waves/round-46/w1/Seat/fixtures/title-%s.json" % case
        case_files = {
            case_path: body,
            case_path + MARKER_SUFFIX: _marker("fixture", [R1], body_digest),
            DEFAULT_WAIVERS: _registry([(case_path, body_digest, [R1], "fixture")]),
        }
        case_root = _waiver_repo(scratch, "title-" + case, case_files)
        _sha, _files, findings, waived, rejected = run(case_root, "HEAD")
        if waivable:
            suite.check("waiver-title-%s-waived" % case,
                        not findings and len(waived) == 1 and not rejected,
                        "findings=%r waived=%r rejected=%r" % (findings, waived, rejected))
        else:
            suite.check(
                "waiver-title-%s-rejected" % case,
                len(findings) == 1 and not waived
                and rejected == [(case_path, R1, "value-not-synthetic:title-not-synthetic")],
                "findings=%r rejected=%r" % (findings, rejected))

    bad_sha_files = dict(waived_files)
    bad_sha_files[path + MARKER_SUFFIX] = _marker("fixture", [R3], "0" * 64)
    bad_sha_root = _waiver_repo(scratch, "bad-sha", bad_sha_files)
    _sha, _files, findings, waived, rejected = run(bad_sha_root, "HEAD")
    suite.check("waiver-sha-mismatch-rejected",
                len(findings) == 1 and not waived
                and rejected == [(path, R3, "sha-mismatch")],
                "findings=%r rejected=%r" % (findings, rejected))

    unregistered_files = {
        path: MONITORS_SYNTH,
        path + MARKER_SUFFIX: _marker("fixture", [R3], digest),
        DEFAULT_WAIVERS: _registry([]),
    }
    unregistered_root = _waiver_repo(scratch, "unregistered", unregistered_files)
    _sha, _files, findings, waived, rejected = run(unregistered_root, "HEAD")
    suite.check("waiver-unregistered-rejected",
                len(findings) == 1 and not waived
                and rejected == [(path, R3, "unregistered")],
                "findings=%r rejected=%r" % (findings, rejected))

    _sha, _files, findings, waived, rejected = run(
        root, "HEAD", waivers=".ufo/waivers.txt")
    suite.check("waiver-registry-in-ufo-refused",
                len(findings) == 1 and not waived
                and rejected == [(path, R3, "registry-in-ufo")],
                "findings=%r rejected=%r" % (findings, rejected))

    outside_path = ".ufo/reports/mons.json"
    outside_files = {
        outside_path: MONITORS_SYNTH,
        outside_path + MARKER_SUFFIX: _marker("fixture", [R3], digest),
        DEFAULT_WAIVERS: _registry([(outside_path, digest, [R3], "fixture")]),
    }
    outside_root = _waiver_repo(scratch, "outside-waves", outside_files)
    _sha, _files, findings, waived, rejected = run(outside_root, "HEAD")
    suite.check("waiver-path-outside-waves-rejected",
                len(findings) == 1 and not waived
                and rejected == [(outside_path, R3, "path-outside-waves")],
                "findings=%r rejected=%r" % (findings, rejected))

    copy_path = ".ufo/waves/round-46/w1/Seat/gate-copy.py"
    copy_digest = _digest(EMBEDDED_CLIENTS)
    copy_files = {
        copy_path: EMBEDDED_CLIENTS,
        "quality/gate.py": EMBEDDED_CLIENTS,
        copy_path + MARKER_SUFFIX: _marker("gate-copy", [R1], copy_digest),
        DEFAULT_WAIVERS: _registry([(copy_path, copy_digest, [R1], "gate-copy")]),
    }
    copy_root = _waiver_repo(scratch, "gate-copy", copy_files)
    _sha, _files, findings, waived, rejected = run(
        copy_root, "HEAD", gate_source="quality/gate.py")
    suite.check("waiver-gate-copy-waived",
                not findings and len(waived) == 1 and not rejected,
                "findings=%r waived=%r rejected=%r" % (findings, waived, rejected))

    altered = EMBEDDED_CLIENTS + "\n"
    altered_digest = _digest(altered)
    altered_files = {
        copy_path: altered,
        "quality/gate.py": EMBEDDED_CLIENTS,
        copy_path + MARKER_SUFFIX: _marker("gate-copy", [R1], altered_digest),
        DEFAULT_WAIVERS: _registry([(copy_path, altered_digest, [R1], "gate-copy")]),
    }
    altered_root = _waiver_repo(scratch, "gate-copy-altered", altered_files)
    _sha, _files, findings, waived, rejected = run(
        altered_root, "HEAD", gate_source="quality/gate.py")
    suite.check("waiver-gate-copy-mismatch-rejected",
                len(findings) == 1 and not waived
                and rejected == [(copy_path, R1, "gate-source-mismatch")],
                "findings=%r rejected=%r" % (findings, rejected))

    _sha, _files, findings, waived, rejected = run(root, "HEAD", use_waivers=False)
    suite.check("waiver-no-waivers-flag-keeps-finding",
                len(findings) == 1 and not waived and not rejected,
                "findings=%r waived=%r" % (findings, waived))

    _append_and_commit(root, path, CLIENT_DUMP)
    _sha, _files, findings, waived, rejected = run(root, "HEAD")
    suite.check("waiver-tamper-after-waiver-keeps-finding",
                [item[1] for item in findings] == [R1, R3] and not waived
                and (path, R3, "sha-mismatch") in rejected,
                "findings=%r rejected=%r" % (findings, rejected))

    per_rule_path = ".ufo/waves/round-46/w1/Seat/fixtures/mixed.txt"
    per_rule_body = CLIENT_SENTINEL + SYNTH_SS
    per_rule_digest = _digest(per_rule_body)
    per_rule_files = {
        per_rule_path: per_rule_body,
        per_rule_path + MARKER_SUFFIX: _marker("fixture", [R1], per_rule_digest),
        DEFAULT_WAIVERS: _registry([(per_rule_path, per_rule_digest, [R1], "fixture")]),
    }
    per_rule_root = _waiver_repo(scratch, "per-rule", per_rule_files)
    _sha, _files, findings, waived, rejected = run(per_rule_root, "HEAD")
    suite.check("waiver-per-rule-only-listed-rule",
                [item[1] for item in findings] == [R2] and len(waived) == 1
                and waived[0][1] == R1
                and rejected == [(per_rule_path, R2, "rule-not-listed")],
                "findings=%r waived=%r rejected=%r" % (findings, waived, rejected))

    # A serial finding on a *marked* file is refused before the marker is read:
    # no reserved namespace exists for a serial value.
    serial_path = ".ufo/waves/round-46/w1/Seat/fixtures/mons-prose.json"
    serial_body = MONITORS_SYNTH + SERIAL_PROSE
    serial_digest = _digest(serial_body)
    serial_files = {
        serial_path: serial_body,
        serial_path + MARKER_SUFFIX: _marker("fixture", [R3], serial_digest),
        DEFAULT_WAIVERS: _registry([(serial_path, serial_digest, [R3], "fixture")]),
    }
    serial_root = _waiver_repo(scratch, "serial-marked", serial_files)
    sha, files, findings, waived, rejected = run(serial_root, "HEAD")
    lines = []
    code = emit(sha, files, findings, waived, rejected, stream=_ListStream(lines))
    suite.check("waiver-serial-rule-not-waivable",
                [item[1] for item in findings] == [R5] and len(waived) == 1
                and waived[0][1] == R3
                and rejected == [(serial_path, R5, "serial-rule-not-waivable")]
                and code == 1,
                "findings=%r waived=%r rejected=%r" % (findings, waived, rejected))
    suite.check("waiver-serial-rejection-is-printed",
                any(line.startswith("WAIVER_REJECTED file=%s rule=%s reason=serial-rule-not-waivable"
                                    % (serial_path, R5)) for line in lines),
                "lines=%r" % (lines,))

    # The marker grammar itself cannot carry a serial rule.
    bad_band_files = {
        serial_path: serial_body,
        serial_path + MARKER_SUFFIX: _marker("fixture", [R3, R5], serial_digest),
        DEFAULT_WAIVERS: _registry([(serial_path, serial_digest, [R3, R5], "fixture")]),
    }
    bad_band_root = _waiver_repo(scratch, "serial-band", bad_band_files)
    _sha, _files, findings, waived, rejected = run(bad_band_root, "HEAD")
    suite.check("waiver-marker-cannot-name-serial-rule",
                [item[1] for item in findings] == [R3, R5] and not waived
                and (serial_path, R3, "marker-malformed") in rejected
                and (serial_path, R5, "serial-rule-not-waivable") in rejected,
                "findings=%r rejected=%r" % (findings, rejected))

    # A serial-shaped value outside the reserved namespace keeps its finding
    # even with a valid marker and a valid registry line: the marker cannot
    # launder a real serial.
    real_serial_body = (
        '[{"name": "DP-1", "description": "Real Panel", "make": "Real",'
        ' "model": "R1", "serial": "%s"}]\n' % LOOKS_REAL_SERIAL
    )
    real_serial_digest = _digest(real_serial_body)
    real_serial_files = {
        serial_path: real_serial_body,
        serial_path + MARKER_SUFFIX: _marker("fixture", [R3, R4], real_serial_digest),
        DEFAULT_WAIVERS: _registry([(serial_path, real_serial_digest, [R3, R4], "fixture")]),
    }
    real_serial_root = _waiver_repo(scratch, "serial-real", real_serial_files)
    _sha, _files, findings, waived, rejected = run(real_serial_root, "HEAD")
    suite.check("waiver-real-serial-marked-file-kept",
                [item[1] for item in findings] == [R3, R5] and not waived
                and (serial_path, R3, "value-not-synthetic:serial-not-synthetic") in rejected
                and (serial_path, R5, "serial-rule-not-waivable") in rejected,
                "findings=%r rejected=%r" % (findings, rejected))

    # A file that only carries the prose serial is refused too, with no marker
    # at all: the rule is scored whether or not a waiver system is in play.
    prose_path = ".ufo/waves/round-32/w1/Entry.md"
    prose_root = _waiver_repo(scratch, "serial-unmarked", {prose_path: SERIAL_PROSE})
    _sha, _files, findings, waived, rejected = run(prose_root, "HEAD")
    suite.check("prose-serial-unmarked-kept",
                [item[1] for item in findings] == [R5] and not waived and not rejected,
                "findings=%r" % (findings,))


class _ListStream:
    def __init__(self, sink):
        self.sink = sink

    def write(self, text):
        self.sink.append(text.rstrip("\n"))


def selftest(verbose=False):
    scratch = tempfile.mkdtemp(prefix="csm-selftest-", dir=os.environ.get("TMPDIR") or None)
    suite = Selftest(verbose=verbose)
    try:
        _unit_cases(suite)
        _e2e_cases(suite, scratch)
        _waiver_cases(suite, scratch)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    total = suite.passed + suite.failed
    print("SELFTEST: passed=%d/%d failed=%d" % (suite.passed, total, suite.failed))
    return 0 if suite.failed == 0 else 1


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog=TOOL,
        description="Scan tracked files under .ufo/ for session material.",
    )
    parser.add_argument("--repo", help="git repository to read")
    parser.add_argument("--rev", default="HEAD", help="revision to scan (default HEAD)")
    parser.add_argument("--home-limit", type=int, default=DEFAULT_HOME_LIMIT,
                        help="distinct bare /home paths that make a listing (default %d)"
                             % DEFAULT_HOME_LIMIT)
    parser.add_argument("--scope", choices=("ufo", "all"), default="ufo",
                        help="tracked paths to scan: .ufo/ only (default) or all")
    parser.add_argument("--serial-from-host", action="store_true",
                        help="read the live monitor serial(s) with %s and count them "
                             "as plain substrings (R6); values are never printed"
                             % (HOST_CMD[0],))
    parser.add_argument("--waivers", default=DEFAULT_WAIVERS,
                        help="waiver registry, relative to the repo (default %s)" % DEFAULT_WAIVERS)
    parser.add_argument("--gate-source", default=DEFAULT_GATE_SOURCE,
                        help="gate source for kind=gate-copy (default %s)" % DEFAULT_GATE_SOURCE)
    parser.add_argument("--no-waivers", action="store_true",
                        help="ignore every synthetic-material marker")
    parser.add_argument("--selftest", action="store_true", help="run positive/negative fixtures")
    parser.add_argument("--verbose", action="store_true", help="print passing selftest cases too")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest(verbose=args.verbose)
    if not args.repo:
        parser.error("--repo is required (or use --selftest)")
    if args.home_limit < 0:
        parser.error("--home-limit must be >= 0")

    try:
        serials = host_serials() if args.serial_from_host else ()
        sha, files, findings, waived, rejected = run(
            args.repo, args.rev, home_limit=args.home_limit,
            waivers=args.waivers, gate_source=args.gate_source,
            use_waivers=not args.no_waivers, scope=args.scope, serials=serials,
        )
    except GateError as exc:
        sys.stderr.write("%s: error: %s\n" % (TOOL, exc))
        return 2
    return emit(sha, files, findings, waived, rejected)


if __name__ == "__main__":
    sys.exit(main())
