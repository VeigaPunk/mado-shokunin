#!/usr/bin/env python3
"""triage.py — build the synthetic-material registry for a revision.

Not part of the gate and never installed. It reads the gate's own
``FINDING`` / ``WAIVER`` / ``WAIVER_REJECTED`` output at a revision and lets
the gate itself decide what is synthetic:

  pass A  one sidecar per file under ``.ufo/waves/``, naming every rule the
          file carries that the marker may name (R1-R4), plus one registry
          row per file. The gate then waives what it can justify (W1-W4) and
          rejects the rest with a reason.
  pass B  the surviving rules only. The sidecar is rewritten with the rules
          pass A waived, or deleted when none survived; the registry follows.
          The run must waive exactly the pass-A set and keep exactly the
          pass-A remaining set, or this script fails.

``--registry``/``--triage`` dump the final artefacts; stdout is a summary of
counts and paths only (the gate never prints a value, and neither does this).

Usage::

    triage.py --repo <clone> --rev <rev> [--registry OUT] [--triage OUT]
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys

GATE_REL = "quality/check-session-material.py"
REGISTRY_REL = "quality/session-material-waivers.txt"
SIDECAR_SUFFIX = ".synthetic"
WAVE_ROOT = ".ufo/waves/"
MARKER_FMT = "SYNTHETIC-MATERIAL v1 kind=%s rules=%s sha256=%s\n"
REGISTRY_HEADER = "# path sha256 rules kind — see quality/check-session-material.py\n"

# Keep this list in the same order as the gate's RULES tuple.
RULE_ORDER = (
    "R1_CLIENT_DUMP",
    "R2_PROC_TABLE",
    "R3_MONITOR_IDENT",
    "R4_HOME_LISTING",
    "R5_SERIAL_PROSE",
    "R6_SERIAL_EXACT",
)
WAIVABLE = RULE_ORDER[:4]
SERIAL_RULES = RULE_ORDER[4:]

FINDING_RE = re.compile(r"^FINDING file=(?P<path>.+?) rule=(?P<rule>\S+) count=(?P<count>\d+)")
WAIVER_RE = re.compile(r"^WAIVER file=(?P<path>.+?) rule=(?P<rule>\S+) kind=(?P<kind>\S+)$")
REJECT_RE = re.compile(r"^WAIVER_REJECTED file=(?P<path>.+?) rule=(?P<rule>\S+)"
                       r" reason=(?P<reason>\S+)$")


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args),
                                                proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout


def git_text(repo, *args):
    return git(repo, *args).decode("utf-8", "replace").strip()


def content_sha256(repo, rev, path):
    """sha256 of the file's bytes at *rev:path* (the gate's own digest)."""
    return hashlib.sha256(git(repo, "show", "%s:%s" % (rev, path))).hexdigest()


def run_gate(repo, rev, extra=()):
    gate = os.path.join(repo, GATE_REL)
    proc = subprocess.run([sys.executable, "-I", gate, "--repo", repo, "--rev", rev, *extra],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode not in (0, 1):
        raise SystemExit("gate failed rc=%d: %s"
                         % (proc.returncode, proc.stderr.decode("utf-8", "replace").strip()))
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def parse(text):
    findings, waived, rejected = [], {}, {}
    for line in text.splitlines():
        match = FINDING_RE.match(line)
        if match:
            findings.append((match.group("path"), match.group("rule")))
            continue
        match = WAIVER_RE.match(line)
        if match:
            waived[(match.group("path"), match.group("rule"))] = match.group("kind")
            continue
        match = REJECT_RE.match(line)
        if match:
            rejected[(match.group("path"), match.group("rule"))] = match.group("reason")
    return findings, waived, rejected


def commit(repo, message):
    git(repo, "add", "-A")
    subprocess.run(["git", "-C", repo, "-c", "user.name=session-marker",
                    "-c", "user.email=session-marker@scratch.invalid",
                    "commit", "-q", "-m", message], check=True)


def write_sidecars(repo, plan, registry_path):
    """*plan* maps path -> (kind, sha, rules). Writes sidecars + registry."""
    registry = {path: (kind, sha, rules) for path, (kind, sha, rules) in plan.items()}
    for path, (kind, sha, rules) in plan.items():
        sidecar = os.path.join(repo, path + SIDECAR_SUFFIX)
        os.makedirs(os.path.dirname(sidecar), exist_ok=True)
        with open(sidecar, "w", encoding="utf-8") as handle:
            handle.write(MARKER_FMT % (kind, ",".join(rules), sha))
    # Drop sidecars that are not in the plan any more. Only a sidecar whose
    # target is itself tracked can be one of ours: a *copy* of a sidecar (a
    # seat storing its install set, a fixture tree) has a target that is not
    # tracked, and is left alone.
    tracked = [relpath for relpath in git_text(repo, "ls-files", "-z", "--", ".ufo").split("\0")
               if relpath]
    tracked_set = set(tracked)
    for relpath in tracked:
        if not relpath.endswith(SIDECAR_SUFFIX):
            continue
        target = relpath[: -len(SIDECAR_SUFFIX)]
        if target not in tracked_set:
            continue
        if target not in plan and os.path.exists(os.path.join(repo, relpath)):
            os.unlink(os.path.join(repo, relpath))
    rows = [REGISTRY_HEADER]
    for path in sorted(registry):
        kind, sha, rules = registry[path]
        rows.append("%s %s %s kind=%s\n" % (path, sha, ",".join(rules), kind))
    target = os.path.join(repo, registry_path)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.writelines(rows)
    return "".join(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="triage.py")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument("--registry", help="write the final registry content here")
    parser.add_argument("--triage", help="write the remaining-findings table here")
    args = parser.parse_args(argv)

    repo = os.path.abspath(args.repo)
    top = git_text(repo, "rev-parse", "--show-toplevel")
    if os.path.realpath(top) != os.path.realpath(repo):
        raise SystemExit("repo toplevel %r is not %r" % (top, repo))

    gate_sha = content_sha256(repo, args.rev, GATE_REL)

    # --no-waivers: the input is the pre-marker finding set, so an existing
    # registry (a tree that already has markers) is re-derived, not destroyed.
    rc, text = run_gate(repo, args.rev, ("--no-waivers",))
    findings, waived, rejected = parse(text)
    by_path = {}
    for path, rule in findings:
        by_path.setdefault(path, set()).add(rule)
    print("markers: no-markers rc=%d findings=%d files=%d" % (rc, len(findings), len(by_path)))

    plan = {}
    skipped = []
    for path in sorted(by_path):
        rules = [rule for rule in RULE_ORDER if rule in by_path[path]]
        wavable = [rule for rule in rules if rule in WAIVABLE]
        if not path.startswith(WAVE_ROOT) or not wavable:
            skipped.append(path)
            continue
        blob = content_sha256(repo, args.rev, path)
        kind = "gate-copy" if blob == gate_sha else "fixture"
        plan[path] = (kind, blob, wavable)
    print("markers: pass-a files=%d skipped=%d" % (len(plan), len(skipped)))

    write_sidecars(repo, plan, REGISTRY_REL)
    commit(repo, "markers: pass a")
    rc_a, text_a = run_gate(repo, "HEAD")
    findings_a, waived_a, rejected_a = parse(text_a)
    print("markers: pass-a rc=%d waived=%d rejected=%d kept=%d"
          % (rc_a, len(waived_a), len(rejected_a), len(findings_a)))

    final = {}
    for path, (kind, blob, rules) in plan.items():
        keep = [rule for rule in rules if (path, rule) in waived_a]
        if keep:
            final[path] = (kind, blob, keep)
    registry_text = write_sidecars(repo, final, REGISTRY_REL)
    commit(repo, "markers: pass b")
    rc_b, text_b = run_gate(repo, "HEAD")
    findings_b, waived_b, rejected_b = parse(text_b)
    print("markers: pass-b rc=%d waived=%d rejected=%d kept=%d"
          % (rc_b, len(waived_b), len(rejected_b), len(findings_b)))

    if set(waived_b) != set(waived_a):
        raise SystemExit("pass A and pass B waived different sets")
    if set(findings_b) != set(findings_a):
        raise SystemExit("pass A and pass B kept different findings")
    if len(rejected_a) - len(rejected_b) != 0:
        reasons = {}
        for key, reason in rejected_a.items():
            if key not in rejected_b:
                reasons[reason] = reasons.get(reason, 0) + 1
        print("markers: rejected-in-a-then-declared-out=%d reasons=%r"
              % (len(rejected_a) - len(rejected_b), reasons))

    rows = []
    for path, rule in sorted(findings_b):
        reason = rejected_b.get((path, rule)) or rejected_a.get((path, rule), "")
        if rule in SERIAL_RULES:
            cls = "real:serial"
        elif path.endswith("check-session-material.py"):
            # A copy of a *different* gate: synthetic content, but W4 refuses
            # it until the copy is refreshed to the installed bytes.
            cls = "synthetic:stale-gate-copy"
        elif reason.startswith("value-not-synthetic"):
            cls = "real:identity:" + reason.split(":", 1)[1]
        else:
            cls = "kept:" + (reason or "unmarked")
        rows.append("%s\t%s\t%s\n" % (path, rule, cls))
    print("markers: remaining=%d" % len(findings_b))
    for cls in sorted(set(row.split("\t")[2].strip() for row in rows)):
        print("markers: remaining class=%s count=%d"
              % (cls, sum(1 for row in rows if row.split("\t")[2].strip() == cls)))
    for row in rows:
        print("REMAINS " + row.rstrip("\n"))

    if args.registry:
        with open(args.registry, "w", encoding="utf-8") as handle:
            handle.write(registry_text)
    if args.triage:
        with open(args.triage, "w", encoding="utf-8") as handle:
            handle.writelines(rows)
    return rc_b


if __name__ == "__main__":
    sys.exit(main())
