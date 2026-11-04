#!/usr/bin/env python3
"""R80CriticClaims lab: derive evidence/c1-critic.py from the frozen c1 counter.

The frozen instrument is never touched; this writes a labelled copy in the seat
evidence dir with four added knobs, each a counterfactual the critic needs:

  --tool PATH                score PATH as the candidate (frozen default: rev bytes)
  --base-tool PATH           score PATH as the do-nothing control (frozen default: base bytes)
  --skip-carried-comparison  simulate the carried comparison's absence: no check AND no
                             predicate clause (carried_ok is forced True)
  --no-mutants is honored    the frozen copy accepts the flag and silently ignores it
"""

import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SRC = os.path.join(LANE, "quality/counters/c1-r80-multisurface.py")
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c1-critic.py")

src = open(SRC).read()


def sub1(old, new):
    global src
    count = src.count(old)
    assert count == 1, "anchor not unique (%d hits): %r" % (count, old[:70])
    src = src.replace(old, new)


sub1('    ap.add_argument("--no-mutants", action="store_true")',
     '    ap.add_argument("--no-mutants", action="store_true")\n'
     '    ap.add_argument("--tool")  # R80CriticClaims lab knob\n'
     '    ap.add_argument("--base-tool")  # R80CriticClaims lab knob\n'
     '    ap.add_argument("--skip-carried-comparison", action="store_true")  # lab knob')

sub1('        source = extract(repo, args.rev, "tools/mado-barfoot.py", workroot)\n'
     '        tool_path = os.path.join(workroot, "mado-barfoot.py")',
     '        if args.tool:\n'
     '            with open(args.tool) as fh:\n'
     '                source = fh.read()\n'
     '        else:\n'
     '            source = extract(repo, args.rev, "tools/mado-barfoot.py", workroot)\n'
     '        tool_path = os.path.join(workroot, "mado-barfoot.py")')

sub1('        base_source = extract(repo, args.base_rev, "tools/mado-barfoot.py", workroot)',
     '        if args.base_tool:\n'
     '            with open(args.base_tool) as fh:\n'
     '                base_source = fh.read()\n'
     '        else:\n'
     '            base_source = extract(repo, args.base_rev, "tools/mado-barfoot.py", workroot)')

sub1('        carried_ok = cases[:CARRIED] == carried\n'
     '        if not carried_ok:\n'
     '            raise Setup("the successor set does not carry the frozen round-79 cases unchanged")',
     '        carried_ok = cases[:CARRIED] == carried\n'
     '        if not carried_ok and not args.skip_carried_comparison:\n'
     '            raise Setup("the successor set does not carry the frozen round-79 cases unchanged")\n'
     '        if args.skip_carried_comparison:\n'
     '            carried_ok = True  # counterfactual: the comparison does not exist at all')

sub1('        killed = 0\n'
     '        for name, anchor, repl in MUTATIONS:',
     '        killed = 0\n'
     '        for name, anchor, repl in ([] if args.no_mutants else MUTATIONS):')

open(DST, "w").write(src)
print("wrote", DST)
