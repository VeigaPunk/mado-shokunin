#!/usr/bin/env python3
"""check-session-material.py — privacy gate for committed receipts.

Question answered: does any tracked file under ``.ufo/`` at a revision carry
raw session material that SKILL.md rule 4 keeps out of this public repo
(live window titles, process tables, monitor serials/descriptions,
home-directory listings)?

Input: a git repository and a revision. Every file under ``.ufo/`` tracked at
that revision is read from the object database (``git ls-tree -r`` +
``git cat-file --batch``); the working tree is never touched, so the gate can
run on any committed revision of a clone without checkout.

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

Output: one ``FINDING`` line per (file, rule), the per-rule tally, then the
summary line exactly::

    SESSION_MATERIAL: files=<n> findings=<n> rev=<hash>

Exit status: 0 no findings, 1 findings, 2 usage or git error.

Usage::

    check-session-material.py --repo <dir> --rev <rev> [--home-limit N]
    check-session-material.py --selftest [--verbose]

``--selftest`` builds positive and negative fixtures in a throwaway git
repository under ``$TMPDIR`` and scores this file's own detection and the
end-to-end scan against them.

Deliberate limits (declared, not hidden): findings name the file, the rule and
counts only — never a title, a program name, a serial, a description or a home
path, so the gate's own output is safe to paste into a receipt. Binary blobs
(a NUL byte in the first 8 KiB) are skipped for text rules. Files larger than
16 MiB are scanned for R2/R4 only, and their object scan reports
``truncated=True``. A client dump split across several files is still caught
per file; a dump whose ``class`` value is empty is not a clients dump.
"""

import argparse
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
HOME_PATH_RE = re.compile(r'^/home/[A-Za-z0-9._-]+(?:/[^\s]*)?/?$')

R1 = "R1_CLIENT_DUMP"
R2 = "R2_PROC_TABLE"
R3 = "R3_MONITOR_IDENT"
R4 = "R4_HOME_LISTING"
RULES = (R1, R2, R3, R4)

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


def scan_blob(data, home_limit):
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

    return findings


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


def list_tree(repo, sha):
    """Return [(blob_sha, path)] for every tracked file under .ufo/ at *sha*."""
    raw = _git(repo, "ls-tree", "-r", "-z", sha, "--", ".ufo")
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


def run(repo, rev, home_limit=DEFAULT_HOME_LIMIT):
    """Return (rev_sha, files_scanned, findings) with findings sorted by path."""
    sha = resolve_rev(repo, rev)
    entries = list_tree(repo, sha)
    order = []
    seen = set()
    for blob_sha, _path in entries:
        if blob_sha not in seen:
            seen.add(blob_sha)
            order.append(blob_sha)

    per_blob = {}
    if order:
        for blob_sha, data in iter_blobs(repo, order):
            per_blob[blob_sha] = scan_blob(data, home_limit)

    findings = []
    for blob_sha, path in entries:
        for rule, count, detail in per_blob.get(blob_sha, ()):
            findings.append((path, rule, count, detail))
    findings.sort(key=lambda item: (item[0], item[1]))
    return sha, len(entries), findings


def emit(sha, files, findings, stream=sys.stdout):
    for path, rule, count, detail in findings:
        stream.write("FINDING file=%s rule=%s count=%d detail=%s\n" % (path, rule, count, detail))
    tally = []
    for rule in RULES:
        rows = [item for item in findings if item[1] == rule]
        if rows:
            tally.append("%s=%d" % (rule, len(rows)))
    if tally:
        stream.write("SESSION_MATERIAL_RULES: %s\n" % " ".join(tally))
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
    def findings(text, home_limit=home_limit):
        return dict((rule, count) for rule, count, _detail in scan_blob(text.encode(), home_limit))

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
    }
    negatives = {
        ".ufo/w2/projection.json": PROJECTION,
        ".ufo/w2/monitors-redacted.json": MONITORS_REDACTED,
        ".ufo/w2/env.txt": HOME_SHORT,
        ".ufo/w2/rule.conf": CONFIG_LINE,
        ".ufo/w2/prose.md": SS_PROSE + PROSE_KEYS,
        ".ufo/w2/empty-title.json": EMPTY_TITLE,
    }
    mixed = os.path.join(scratch, "mixed")
    os.makedirs(mixed)
    _commit_fixture(mixed, dict(positives, **negatives))

    sha, files, findings = run(mixed, "HEAD")
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
    _sha, files, findings = run(negatives_only, "HEAD")
    lines = []
    code = emit(_sha, files, findings, stream=_ListStream(lines))
    suite.check("e2e-negative-repo-exit-0", code == 0 and not findings,
                "code=%d findings=%d" % (code, len(findings)))

    # A non-.ufo file with the same dump must be invisible to the gate.
    outside = os.path.join(scratch, "outside")
    os.makedirs(outside)
    _commit_fixture(outside, {"corpus/leak.json": CLIENT_DUMP, ".ufo/keep.txt": "ok\n"})
    _sha, files, findings = run(outside, "HEAD")
    suite.check("e2e-outside-ufo-not-scanned", not findings and files == 1,
                "files=%d findings=%r" % (files, findings))

    # A revision with nothing tracked under .ufo/ is a clean scan, not an error.
    empty = os.path.join(scratch, "empty")
    os.makedirs(empty)
    _commit_fixture(empty, {"README.md": "no .ufo tree here\n"})
    _sha, files, findings = run(empty, "HEAD")
    lines = []
    code = emit(_sha, files, findings, stream=_ListStream(lines))
    suite.check("e2e-empty-ufo-clean", code == 0 and files == 0 and not findings,
                "code=%d files=%d findings=%r" % (code, files, findings))


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
        sha, files, findings = run(args.repo, args.rev, home_limit=args.home_limit)
    except GateError as exc:
        sys.stderr.write("%s: error: %s\n" % (TOOL, exc))
        return 2
    return emit(sha, files, findings)


if __name__ == "__main__":
    sys.exit(main())
