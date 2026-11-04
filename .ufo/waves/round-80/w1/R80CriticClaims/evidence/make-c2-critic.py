#!/usr/bin/env python3
"""R80CriticClaims lab: derive evidence/c2-critic.py from the frozen c2 counter.

The frozen instrument is never touched. The copy demonstrates the two before-state
counterfactuals the critic must test:

  --no-tree-check  skip the working-tree/fixture byte binding (shows what refuses next)
  --before         score the runbook's rows at --rev instead of refusing: the section is
                   keyed by round-number regex, a case whose anchor binds zero rows fails
                   by binding instead of setup, and tree=... reports honestly
"""

import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SRC = os.path.join(LANE, "quality/counters/c2-r80-runbook.py")
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c2-critic.py")

src = open(SRC).read()


def sub1(old, new):
    global src
    count = src.count(old)
    assert count == 1, "anchor not unique (%d hits): %r" % (count, old[:70])
    src = src.replace(old, new)


sub1('    ap.add_argument("--no-mutants", action="store_true")',
     '    ap.add_argument("--no-mutants", action="store_true")\n'
     '    ap.add_argument("--before", action="store_true")  # R80CriticClaims lab knob\n'
     '    ap.add_argument("--no-tree-check", action="store_true")  # R80CriticClaims lab knob')

sub1('SECTION = "### Executable runbook rows (round 80)"',
     'SECTION_RE = re.compile(r"^### Executable runbook rows \\(round \\d+\\)$")  # lab copy')

sub1('        if stripped == SECTION:\n'
     '            inside = True',
     '        if SECTION_RE.match(stripped):\n'
     '            inside = True')

sub1('        skill = git_show(repo, args.rev, "SKILL.md")\n'
     '        for path in ("SKILL.md", "tools/mado-barfoot.py"):',
     '        skill = git_show(repo, args.rev, "SKILL.md")\n'
     '        for path in (() if args.no_tree_check else ("SKILL.md", "tools/mado-barfoot.py")):')

sub1('        for case in cases:\n'
     '            for path in case.get("fixtures", []):',
     '        for case in (() if args.no_tree_check else cases):\n'
     '            for path in case.get("fixtures", []):')

sub1('        rows = command_rows(skill)\n'
     '        if len(rows) != CASES:',
     '        rows = command_rows(skill)\n'
     '        if len(rows) != CASES and not args.before:')

sub1('            if len(hits) != 1:',
     '            if len(hits) != 1 and not (args.before and len(hits) == 0):')

sub1('            if documented != case["skill_anchor"]:',
     '            if documented != case["skill_anchor"] and case["name"] in bindings:')

sub1('        row_of = {name: index for index, name in bindings.items()}',
     '        row_of = {name: index for index, name in bindings.items()}\n'
     '        row_of_bound = lambda name: row_of.get(name, -1)  # lab copy: unbound -> -1')

sub1('% (case["name"], row_of[case["name"]], case["kind"],',
     '% (case["name"], row_of_bound(case["name"]), case["kind"],')

sub1('rows=%d/%d control_new=%d/%d mutants=%s killed=%s verdict=%s rev=%s tree=bound"',
     'rows=%d/%d control_new=%d/%d mutants=%s killed=%s verdict=%s rev=%s tree=%s"')

sub1('                 "TARGET_MET" if target else "TARGET_MISSED", rev_full))',
     '                 "TARGET_MET" if target else "TARGET_MISSED", rev_full,\n'
     '                 "bound" if not (args.before or args.no_tree_check) else "relaxed"))')

open(DST, "w").write(src)
print("wrote", DST)
