#!/usr/bin/env python3
"""check-scope.py — round-51 w1 scope and safety sweep (SentScope51).

Read-only against the lane. Answers five questions about an in-flight wave
directory:

  A. write scope   — does `git status --porcelain` in the lane show anything
                     untracked outside the wave dir, or any tracked change?
  B. secret shapes — do wave files carry session tokens, secret-manager refs,
                     private hosts/URLs or key material? (values never printed)
  C. scratch rule  — do drafted executables write to a hardcoded tmp literal,
                     or call a tempfile helper without an explicit dir=?
  D. fetch pins    — are pin sources byte-fetched upstream bytes (no local
                     absolute path, no file/ssh URL) under a checksum manifest?
  E. declarations  — does every `## Deliverables` bullet and `Report:` trailer
                     resolve to a file, and does any resolve outside the wave
                     (i.e. a seat wrote a tracked path)?

Usage:
  python3 -I check-scope.py --lane <lane repo> --wave <wave dir> [--scratch DIR]
  python3 -I check-scope.py --selftest [--scratch DIR]

--scratch is honoured for every temporary write ($TMPDIR is the fallback); this
tool never writes to a tmp literal. Exit 0 clean, 1 defect/pending, 2 usage.
"""
import argparse
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile

SECRET_RULES = (
    ("op-ref", re.compile(r"\bop://[A-Za-z0-9]")),
    ("gh-token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{16,}")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9]{16,}")),
    ("aws-key", re.compile(r"\bAKIA[0-9A-Z]{12,}")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY")),
    ("bearer", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{16,}")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")),
    ("basic-auth-url", re.compile(r"https?://[^\s/:@]+:[^\s/@]{6,}@")),
)
PRIVATE_URL_RULES = (
    ("loopback-or-rfc1918",
     re.compile(r"https?://(?:localhost|127\.|0\.0\.0\.0|10\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.)")),
    ("file-url", re.compile(r"\bfile:///[A-Za-z0-9]")),
    ("remote-shell-url", re.compile(r"\bssh://[A-Za-z0-9]")),
    ("tailnet", re.compile(r"\.ts\.net\b|\btailscale\b", re.IGNORECASE)),
)
TMP_DIR_LITERAL = re.compile(r"['\"](?:/tmp|/var/tmp|/dev/shm)(?:/|['\"])")
TMP_WRITE_CONTEXT = re.compile(
    r"\bopen\s*\(|\bos\.(?:makedirs|mkdir|path\.join|rename|replace)\b|\bmkdtemp\s*\("
    r"|\bmkstemp\s*\(|\bTemporaryDirectory\s*\(|\bshutil\.|\bcopytree\b|\bcopy2\b"
    r"|\bcp\s+-|\bmv\s+|\btee\s+|\bsubprocess\.|\bcheck_output\b|\brun\s*\(")
SANDBOX_ARGV = re.compile(r"--tmpfs|--bind|--dev-bind|--ro-bind|--chdir|--setenv|bwrap")
MKDTEMP = re.compile(r"\bmkdtemp\s*\(")
NAMED_TMP = re.compile(r"\bNamedTemporaryFile\s*\(")
WORKDIR_ARG = re.compile(r"dir\s*=")
TEXT_SUFFIXES = {".md", ".txt", ".py", ".sh", ".bash", ".json", ".tsv", ".csv",
                 ".yaml", ".yml", ".jsonl", ".rst"}
PIN_LOCAL_PATH = re.compile(
    r"(?:/home/[A-Za-z0-9._-]+/|/fast/scratch/|/srv/|file:///[A-Za-z0-9]|ssh://[A-Za-z0-9])")
RULE_DEFINITION = "re.compile("
DELIV_BULLET = re.compile(r"^\s*[-*]\s+`([^`]+)`")
REPORT_TRAILER = re.compile(r"^\s*Report:\s*`?([^`\s]+)`?\s*$")


def sh(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    return p.returncode, p.stdout


def walk_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
        for name in sorted(filenames):
            yield os.path.join(dirpath, name)


def rel(root, path):
    return os.path.relpath(path, root)


def is_text(path):
    if os.path.splitext(path)[1].lower() not in TEXT_SUFFIXES:
        try:
            with open(path, "rb") as fh:
                return b"\x00" not in fh.read(2048)
        except OSError:
            return False
    return True


def read_text(path, limit=4 * 1024 * 1024):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read(limit)
    except OSError:
        return ""


def scan_lines(text):
    """Yield (lineno, line), skipping shape-rule definition blocks.

    A probe that enumerates the very shapes it looks for carries those literals
    in its own source; counting them would make every scanner its own finding.
    A `re.compile(` call may span lines, so the block is tracked by paren depth.
    """
    depth = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        if depth or RULE_DEFINITION in line:
            depth += line.count("(") - line.count(")")
            if depth < 0:
                depth = 0
            continue
        yield lineno, line


def check_a(lane, wave):
    """Write scope: untracked outside the wave, tracked modifications."""
    rc, out = sh(["git", "status", "--porcelain", "--untracked-files=all"], lane)
    if rc != 0:
        return {"error": "git status failed rc=%d" % rc, "out_of_scope": [],
                "tracked_dirty": [], "untracked_inside": 0}, out
    wave_rel = os.path.relpath(wave, lane).rstrip("/")
    out_of_scope, tracked_dirty, untracked_inside = [], [], 0
    for line in out.splitlines():
        if not line.strip():
            continue
        status, path = line[:2], line[3:]
        if status == "??":
            if path == wave_rel or path.startswith(wave_rel + "/"):
                untracked_inside += 1
            else:
                out_of_scope.append(path)
        else:
            tracked_dirty.append(line)
    return {"out_of_scope": out_of_scope, "tracked_dirty": tracked_dirty,
            "untracked_inside": untracked_inside}, out


def check_b(wave):
    """Secret and private-location shapes in wave files."""
    hits, private = [], []
    for path in walk_files(wave):
        if not is_text(path):
            continue
        text = read_text(path)
        if not text:
            continue
        for lineno, line in scan_lines(text):
            for name, rx in SECRET_RULES:
                if rx.search(line):
                    hits.append((rel(wave, path), name, lineno))
            for name, rx in PRIVATE_URL_RULES:
                if rx.search(line):
                    private.append((rel(wave, path), name, lineno))
    return hits, private


def check_c(wave):
    """Scratch rule: hardcoded tmp write targets, dirless tempfile helpers.

    A tmp literal is a defect only as a host write target. A comment, a
    rule/refusal table or a sandbox argv carries the literal harmlessly and is
    classified, never counted blindly: a hygiene scanner enumerating the tmpish
    constants is not a writer.
    """
    defects, review = [], []
    for path in walk_files(wave):
        if os.path.splitext(path)[1].lower() not in {".py", ".sh", ".bash"}:
            continue
        text = read_text(path)
        if not text:
            continue
        for lineno, line in scan_lines(text):
            if line.lstrip().startswith("#"):
                continue
            if TMP_DIR_LITERAL.search(line):
                if SANDBOX_ARGV.search(line):
                    continue
                if TMP_WRITE_CONTEXT.search(line):
                    defects.append((rel(wave, path), lineno, "hardcoded-tmp-write"))
                else:
                    review.append((rel(wave, path), lineno, "tmp-literal-mention"))
                continue
            for rx, label in ((MKDTEMP, "mkdtemp-without-dir"),
                              (NAMED_TMP, "NamedTemporaryFile-without-dir")):
                if rx.search(line) and not WORKDIR_ARG.search(line):
                    review.append((rel(wave, path), lineno, label))
    return defects, review


def pin_sources(wave):
    """Directories holding fetched bytes: `<wave>/fetch` and any `fetch*` dir."""
    sources = []
    canonical = os.path.join(wave, "fetch")
    if os.path.isdir(canonical):
        sources.append(canonical)
    for dirpath, dirnames, _ in os.walk(wave):
        for name in sorted(dirnames):
            if name == "fetch" or name.startswith("fetch-"):
                cand = os.path.join(dirpath, name)
                if cand not in sources:
                    sources.append(cand)
    return sources


def check_d(wave):
    """Fetch pins: upstream bytes only, under a checksum manifest.

    Only the canonical `<wave>/fetch` and top-level `<wave>/fetch-*` dirs owe a
    manifest; a nested `.../fixtures/.../fetch` is a synthetic control fixture
    and is scanned for local paths but is not required to be self-checksummed.
    """
    result = {"sources": [], "files": 0, "local_refs": [],
              "manifests": [], "missing_manifest": [], "fixtures": []}
    for source in pin_sources(wave):
        name = rel(wave, source)
        canonical = name == "fetch" or "/" not in name
        (result["sources"] if canonical else result["fixtures"]).append(name)
        manifests = 0
        files = 0
        for path in walk_files(source):
            files += 1
            result["files"] += 1
            name = os.path.basename(path)
            if name.startswith("SHA256SUMS"):
                manifests += 1
                result["manifests"].append(rel(wave, path))
                continue
            if not is_text(path):
                continue
            for lineno, line in enumerate(read_text(path).splitlines(), 1):
                if PIN_LOCAL_PATH.search(line):
                    result["local_refs"].append((rel(wave, path), lineno))
        if files and not manifests and canonical:
            result["missing_manifest"].append(name + "/ has no SHA256SUMS* manifest")
    return result


def report_files(wave):
    """Seat reports: `wave/<seat>.md` and `wave/<seat>/<name>.md`.

    Deeper paths inside a seat dir are the seat's artifacts, not reports;
    `receipts/` is never a report directory.
    """
    found = []
    for name in sorted(os.listdir(wave)):
        path = os.path.join(wave, name)
        if os.path.isfile(path) and name.endswith(".md"):
            found.append(path)
        elif os.path.isdir(path) and name != "receipts":
            for inner in sorted(os.listdir(path)):
                sub = os.path.join(path, inner)
                if os.path.isfile(sub) and inner.endswith(".md"):
                    found.append(sub)
    return found


def declared_candidates(lane, wave, report_path, target):
    """Every path a seat's declaration can mean, most specific first.

    The lane contract makes `Report:` paths lane-relative; seats also write
    bare basenames (seat-dir relative) in `## Deliverables` bullets. Accept
    either, and report which reading resolved so an ambiguous declaration stays
    visible instead of becoming a phantom absence.
    """
    seats = [os.path.dirname(report_path)]
    base = os.path.basename(report_path)
    if base.endswith(".md"):
        seats.append(os.path.join(os.path.dirname(report_path), base[:-3]))
    if os.path.basename(os.path.dirname(report_path)) == os.path.basename(wave):
        seats.append(os.path.join(wave, base[:-3]))
    candidates = []
    if os.path.isabs(target):
        return [(os.path.normpath(target), "absolute")]
    for anchor, label in ((lane, "lane-relative"), (wave, "wave-relative")):
        candidates.append((os.path.normpath(os.path.join(anchor, target)), label))
    for seat in seats:
        candidates.append((os.path.normpath(os.path.join(seat, target)), "seat-relative"))
    seen, ordered = set(), []
    for path, label in candidates:
        if path not in seen:
            seen.add(path)
            ordered.append((path, label))
    return ordered


def check_e(lane, wave):
    """Declared deliverables in seat reports: existence and containment."""
    declared, absent, escaped = [], [], []
    for path in report_files(wave):
        name = rel(wave, path)
        section = None
        for line in read_text(path).splitlines():
            if line.startswith("## "):
                section = line[3:].strip().lower()
                continue
            m = DELIV_BULLET.match(line) if section == "deliverables" else None
            kind = "deliverable"
            if not m:
                m = REPORT_TRAILER.match(line)
                kind = "report-trailer"
            if not m:
                continue
            target = m.group(1).rstrip("/")
            resolved, strategy = None, "missing"
            for candidate, label in declared_candidates(lane, wave, path, target):
                if os.path.exists(candidate):
                    resolved, strategy = candidate, label
                    break
            inside_wave = bool(resolved) and (
                resolved == os.path.normpath(wave) or
                resolved.startswith(os.path.normpath(wave) + os.sep))
            declared.append({"report": name, "kind": kind, "target": target,
                             "resolved": resolved, "strategy": strategy,
                             "inside_wave": inside_wave})
            if resolved is None:
                absent.append((name, target))
            elif not inside_wave:
                escaped.append((name, target))
    return declared, absent, escaped


def sweep(lane, wave):
    scope, _ = check_a(lane, wave)
    secret, private = check_b(wave)
    tmp_defects, tmp_review = check_c(wave)
    pins = check_d(wave)
    declared, absent, escaped = check_e(lane, wave)

    verdict = "CLEAN"
    reasons = []
    if scope.get("out_of_scope"):
        verdict = "DEFECT"
        reasons.append("out_of_scope=%d" % len(scope["out_of_scope"]))
    if scope.get("tracked_dirty"):
        verdict = "DEFECT"
        reasons.append("tracked_dirty=%d" % len(scope["tracked_dirty"]))
    if secret:
        verdict = "DEFECT"
        reasons.append("secret_hits=%d" % len(secret))
    if private:
        verdict = "DEFECT"
        reasons.append("private_locator_hits=%d" % len(private))
    if tmp_defects:
        verdict = "DEFECT"
        reasons.append("tmp_defects=%d" % len(tmp_defects))
    pin_defects = len(pins["local_refs"]) + len(pins["missing_manifest"])
    if pin_defects:
        verdict = "DEFECT"
        reasons.append("pin_defects=%d" % pin_defects)
    if absent:
        if verdict == "CLEAN":
            verdict = "PENDING"
        reasons.append("declared_absent=%d" % len(absent))
    if escaped:
        verdict = "DEFECT"
        reasons.append("declared_outside_wave=%d" % len(escaped))

    return {
        "lane": lane, "wave": wave,
        "files": sum(1 for _ in walk_files(wave)),
        "scope": scope, "secret": secret, "private": private,
        "tmp_defects": tmp_defects, "tmp_review": tmp_review,
        "pins": pins, "declared": declared,
        "absent": absent, "escaped": escaped,
        "verdict": verdict, "reasons": reasons,
    }


def render(report, stream):
    scope, pins = report["scope"], report["pins"]
    print("SCOPE_CHECK wave=%s files=%d" % (report["wave"], report["files"]), file=stream)
    print("[A] write scope", file=stream)
    print("  untracked_inside_wave=%d out_of_scope=%d tracked_dirty=%d"
          % (scope.get("untracked_inside", 0), len(scope.get("out_of_scope", [])),
             len(scope.get("tracked_dirty", []))), file=stream)
    for path in scope.get("out_of_scope", []):
        print("  OUT_OF_SCOPE %s" % path, file=stream)
    for line in scope.get("tracked_dirty", []):
        print("  TRACKED_DIRTY %s" % line, file=stream)
    print("[B] secret shapes: hits=%d private_locators=%d"
          % (len(report["secret"]), len(report["private"])), file=stream)
    for (path, rule, lineno) in report["secret"]:
        print("  SECRET %s rule=%s line=%d" % (path, rule, lineno), file=stream)
    for (path, rule, lineno) in report["private"]:
        print("  PRIVATE_LOCATOR %s rule=%s line=%d" % (path, rule, lineno), file=stream)
    print("[C] scratch rule: defects=%d review=%d"
          % (len(report["tmp_defects"]), len(report["tmp_review"])), file=stream)
    for (path, lineno, label) in report["tmp_defects"]:
        print("  TMP_DEFECT %s:%d %s" % (path, lineno, label), file=stream)
    for (path, lineno, label) in report["tmp_review"]:
        print("  TMP_REVIEW %s:%d %s" % (path, lineno, label), file=stream)
    print("[D] fetch pins: sources=%s fixtures=%s files=%d manifests=%d local_refs=%d"
          % (pins["sources"], pins["fixtures"], pins["files"],
             len(pins["manifests"]), len(pins["local_refs"])), file=stream)
    for (path, lineno) in pins["local_refs"]:
        print("  PIN_LOCAL_REF %s:%d" % (path, lineno), file=stream)
    for msg in pins["missing_manifest"]:
        print("  PIN_MANIFEST_MISSING %s" % msg, file=stream)
    print("[E] declarations: total=%d absent=%d outside_wave=%d"
          % (len(report["declared"]), len(report["absent"]),
             len(report["escaped"])), file=stream)
    for (name, target) in report["absent"]:
        print("  DECLARED_ABSENT report=%s path=%s" % (name, target), file=stream)
    for (name, target) in report["escaped"]:
        print("  DECLARED_OUTSIDE_WAVE report=%s path=%s" % (name, target), file=stream)
    print("SCOPE_SWEEP: files=%d out_of_scope=%d tracked_dirty=%d secret_hits=%d"
          " tmp_defects=%d pin_defects=%d declared_absent=%d verdict=%s"
          % (report["files"], len(scope.get("out_of_scope", [])),
             len(scope.get("tracked_dirty", [])),
             len(report["secret"]) + len(report["private"]),
             len(report["tmp_defects"]),
             len(pins["local_refs"]) + len(pins["missing_manifest"]),
             len(report["absent"]), report["verdict"]), file=stream)


# ---------------------------------------------------------------- selftest

def _fixture(scratch, name, files, untracked=None):
    root = os.path.join(scratch, "selftest-" + name)
    if os.path.isdir(root):
        subprocess.run(["rm", "-rf", root], check=False)
    os.makedirs(root)
    for relpath, body in files.items():
        path = os.path.join(root, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
    sh(["git", "init", "-q", "."], root)
    sh(["git", "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A"], root)
    sh(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "f"], root)
    rc, top = sh(["git", "rev-parse", "--show-toplevel"], root)
    assert rc == 0 and os.path.realpath(top.strip()) == os.path.realpath(root), \
        "fixture is not its own toplevel: %s" % top
    for relpath, body in (untracked or {}).items():
        path = os.path.join(root, relpath)
        os.makedirs(os.path.dirname(path) or root, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
    return root


def _run_sweep(root, wave_rel, scratch):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        report = sweep(root, os.path.join(root, wave_rel))
    return report


def selftest(scratch):
    cases = []
    wave = ".ufo/waves/round-9/w1"
    clean_report = ("# S\n\n## Deliverables\n- `%s/S/art.md`\n\nReport: %s/S.md\n"
                    % (wave, wave))

    def case(name, cond, detail=""):
        cases.append((name, bool(cond), detail))

    root = _fixture(scratch, "clean", {
        wave + "/S.md": clean_report,
        wave + "/S/art.md": "art\n",
    })
    r = _run_sweep(root, wave, scratch)
    case("clean-verdict", r["verdict"] == "CLEAN", r["verdict"])
    case("clean-declared-resolves", not r["absent"] and len(r["declared"]) == 2,
         "declared=%d absent=%d" % (len(r["declared"]), len(r["absent"])))
    case("clean-no-findings", not (r["secret"] or r["private"] or r["tmp_defects"]), "")

    root = _fixture(scratch, "out-of-scope", {
        wave + "/S.md": "status\n",
    }, untracked={"tracked-file.txt": "seat wrote outside the wave\n"})
    r = _run_sweep(root, wave, scratch)
    case("out-of-scope-flagged", r["verdict"] == "DEFECT"
         and r["scope"]["out_of_scope"] == ["tracked-file.txt"],
         "out_of_scope=%r" % (r["scope"]["out_of_scope"],))

    # The token is assembled at run time so this file carries no literal.
    token = "op" + "://" + "vault/Item/" + "x" * 4
    root = _fixture(scratch, "secret", {
        wave + "/S.md": "see %s\n" % token,
    })
    r = _run_sweep(root, wave, scratch)
    case("secret-flagged", r["verdict"] == "DEFECT"
         and [h[1] for h in r["secret"]] == ["op-ref"], "%r" % (r["secret"],))

    tmpish = "/" + "tmp"
    root = _fixture(scratch, "tmp", {
        wave + "/tools/w.py": (
            "open('%s/out.txt', 'w').close()\n"
            "SANDBOX = ['bwrap', '--tmpfs', '%s']\n"
            "REFUSE = ('%s', '/var/tmp')\n" % (tmpish, tmpish, tmpish)),
    })
    r = _run_sweep(root, wave, scratch)
    case("tmp-write-flagged", len(r["tmp_defects"]) == 1
         and r["tmp_defects"][0][2] == "hardcoded-tmp-write", "%r" % (r["tmp_defects"],))
    case("tmp-sandbox-and-refusal-classified", len(r["tmp_review"]) == 1,
         "%r" % (r["tmp_review"],))

    root = _fixture(scratch, "pin", {
        wave + "/fetch/pin.html": "<html>%s/x</html>\n" % ("/home" + "/user"),
        wave + "/fetch/SHA256SUMS": "%s  pin.html\n" % ("0" * 64),
    })
    r = _run_sweep(root, wave, scratch)
    case("pin-local-ref-flagged", r["verdict"] == "DEFECT"
         and len(r["pins"]["local_refs"]) == 1, "%r" % (r["pins"]["local_refs"],))
    case("pin-manifest-seen", r["pins"]["manifests"] == ["fetch/SHA256SUMS"],
         "%r" % (r["pins"]["manifests"],))

    root = _fixture(scratch, "pin-no-manifest", {
        wave + "/fetch/pin.html": "<html>upstream</html>\n",
    })
    r = _run_sweep(root, wave, scratch)
    case("pin-missing-manifest-flagged", r["pins"]["missing_manifest"] != [], "")

    root = _fixture(scratch, "absent", {
        wave + "/S.md": "## Deliverables\n- `missing.md`\n",
    })
    r = _run_sweep(root, wave, scratch)
    case("declared-absent-pending", r["verdict"] == "PENDING"
         and r["absent"] == [("S.md", "missing.md")], "%r" % (r["absent"],))

    root = _fixture(scratch, "seat-relative", {
        wave + "/S.md": "## Deliverables\n- `art.md`\n",
        wave + "/S/art.md": "art\n",
    })
    r = _run_sweep(root, wave, scratch)
    case("seat-relative-basename-resolves",
         not r["absent"] and r["declared"][0]["strategy"] == "seat-relative",
         "%r" % (r["declared"],))

    passed = sum(1 for (_, ok, _) in cases if ok)
    for (name, ok, detail) in cases:
        print("SELFTEST %-40s %s%s" % (name, "ok" if ok else "FAIL",
                                       "" if ok else " " + detail))
    print("SELFTEST: cases=%d passed=%d %s" % (len(cases), passed,
                                               "ok" if passed == len(cases) else "FAIL"))
    return 0 if passed == len(cases) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="round-51 w1 scope/safety sweep")
    ap.add_argument("--lane", help="lane repository root")
    ap.add_argument("--wave", help="wave directory (absolute or lane-relative)")
    ap.add_argument("--scratch", default=None,
                    help="scratch dir for temporary work (default: $TMPDIR)")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--selftest", action="store_true", help="run hermetic fixtures")
    args = ap.parse_args(argv)

    scratch = args.scratch or os.environ.get("TMPDIR") or tempfile.gettempdir()
    os.makedirs(scratch, exist_ok=True)
    if args.selftest:
        return selftest(scratch)
    if not args.lane or not args.wave:
        ap.error("--lane and --wave are required unless --selftest")

    lane = os.path.abspath(args.lane)
    wave = args.wave if os.path.isabs(args.wave) else os.path.join(lane, args.wave)
    wave = os.path.abspath(wave)
    if not os.path.isdir(wave):
        print("check-scope: wave dir not found: %s" % wave, file=sys.stderr)
        return 2

    report = sweep(lane, wave)
    if args.json:
        print(json.dumps(report, indent=1, sort_keys=True, default=str))
    else:
        render(report, sys.stdout)
    return 0 if report["verdict"] == "CLEAN" else 1


if __name__ == "__main__":
    sys.exit(main())
