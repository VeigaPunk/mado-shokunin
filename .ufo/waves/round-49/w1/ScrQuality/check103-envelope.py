#!/usr/bin/env python3
"""check103-envelope.py - candidate criterion 103 (a gate's measured envelope).

Question answered: does a registered gate see the surface its registry row
claims, and is every class it cannot see named in that row?

Three readings, each from committed bytes:

  scope      the row's command flags against the flag the gate's own parser
             defaults to. A row that runs `--repo . --rev REV` with no
             `--scope`, on a gate whose `--scope` default is `ufo`, reads as a
             repo-wide gate and scans `.ufo/` only: SCOPE_UNSTATED.
  rules      every `R<n>_NAME` the row names, with the synthetic shapes the
             gate's own class-verdict receipt shows it catching.
  blind      every shape class the verdict receipt records as missed and the
             row does not name as a blind spot: BLIND.

The shape receipt is the attacking seat's own JSONL (`{"class","file","rules"}`,
empty `rules` = missed), so the instrument measures the gate against a
population it did not author - the row is then judged on whether it declares
that population.

Reads only; writes nothing.

Usage:
  check103-envelope.py --repo REPO --rev REV [--registry SKILL.md]
                       --gate-id mado-session-material --gate quality/check-session-material.py
                       --shape-verdicts FILE
Exit: 0 envelope declared, 1 narrower/undeclared, 2 usage / unreadable.
"""
import argparse
import json
import re
import subprocess
import sys


def show(repo, rev, path):
    proc = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                          capture_output=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace")


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--rev", required=True)
    parser.add_argument("--registry", default="SKILL.md")
    parser.add_argument("--gate-id", required=True)
    parser.add_argument("--gate", required=True)
    parser.add_argument("--shape-verdicts", required=True)
    args = parser.parse_args()

    registry = show(args.repo, args.rev, args.registry)
    if registry is None:
        print("CHECK103: error=registry-unreadable %s@%s" % (args.registry, args.rev))
        return 2
    row = None
    for line in registry.splitlines():
        if line.lstrip().startswith("| %s |" % args.gate_id):
            row = line
            break
    if row is None:
        print("CHECK103: error=registry-row-absent id=%s" % args.gate_id)
        return 2

    gate_src = show(args.repo, args.rev, args.gate)
    if gate_src is None:
        print("CHECK103: error=gate-unreadable %s@%s" % (args.gate, args.rev))
        return 2
    scope_default, has_scope_arg = None, False
    for line in gate_src.splitlines():
        if 'add_argument("--scope"' in line or "add_argument('--scope'" in line:
            has_scope_arg = True
            match = re.search(r'default="([^"]+)"', line) or re.search(r"default='([^']+)'", line)
            if match:
                scope_default = match.group(1)
    row_has_scope = "--scope" in row
    row_has_repo = "--repo" in row
    bad = 0
    if has_scope_arg and not row_has_scope and row_has_repo and scope_default != "all":
        print("SCOPE_UNSTATED registry=%s flag=absent gate_default=%s wording=repo"
              % (args.registry, scope_default))
        bad += 1
    else:
        print("SCOPE registry=%s flag=%s gate_default=%s"
              % (args.registry, "present" if row_has_scope else "absent", scope_default))

    rules = sorted(set(re.findall(r'\bR\d+_[A-Z_]+\b', row)))
    caught, missed, unparsed = [], [], []
    try:
        for line in open(args.shape_verdicts, "r", errors="replace"):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except ValueError:
                unparsed.append(line)
                continue
            (caught if entry.get("rules") else missed).append(entry)
    except OSError as exc:
        print("CHECK103: error=shapes-unreadable %s: %s" % (args.shape_verdicts, exc))
        return 2
    for line in unparsed:
        print("SHAPES_NON_ROW line=%s" % line[:120])
    for rule in rules:
        hits = [e for e in caught if rule in e.get("rules", [])]
        print("RULE %s shapes=%d%s" % (rule, len(hits), "" if hits else " positive=none"))
    declared = re.search(r'blind[- _]?spots?\s*[=:]', row, re.I) or "not scanned" in row.lower()
    for entry in missed:
        if declared:
            print("BLIND_DECLARED class=%s" % entry.get("class"))
        else:
            print("BLIND class=%s file=%s" % (entry.get("class"), entry.get("file")))
            bad += 1
    print("ENVELOPE: registry=%s rules=%d shapes=%d caught=%d missed=%d unparsed=%d blind=%d verdict=%s"
          % (args.gate_id, len(rules), len(caught) + len(missed), len(caught), len(missed),
             len(unparsed), len(missed) if not declared else 0, "NARROWER" if bad else "OK"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
