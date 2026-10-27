Measurement copies of ExecCounterC1's draft (c1-r49-keysym.py), NOT counters and NOT for installation.

Each differs from the draft at .ufo/waves/round-49/w1/ExecCounterC1/c1-r49-keysym.py in exactly the lines its name
says, and only there:
  NOR.py        clause r switched off: the two strace lines in Box.run are replaced by a no-op, so no tool run is
                traced and no trip is recorded. Everything else is byte-identical.
  NOGEN.py      clause g switched off: `GEN = 60` becomes `GEN = 0`.
  NOR-NOGEN.py  both of the above.
Their only purpose is to answer "which clause stopped this control": a control that scores TARGET_MET with a clause
switched off proves that clause (and only that clause) was doing the work. The verdicts of record are the ones from the
unmodified draft (receipts/controls.txt); these copies are never frozen, never scored as the instrument, and the
ExecControlsC1 report states this.

c1-r49-fixtures.json in this directory is a SYMLINK to ../../ExecCounterC1/c1-r49-fixtures.json, not a copy: the draft's
`beside()` looks for the fixture file next to the counter first, and these copies live here, so the link lets them see the
same pinned bytes the draft sees. It is read-only for these runs.
