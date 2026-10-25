# SentGateExec — sentinel seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: sentinel

Security review of the two new gates and the fixture generator (LANE/quality/check-counter-discrimination.py, LANE/quality/check-evidence-pointers.py, LANE/.ufo/waves/round-36/c2/gen-mutants.py). Look for: unquoted shell interpolation, `shell=True`, path traversal out of `--repo`, symlink following in writes, world-writable /tmp fixture dirs, environment injection (`GIT_DIR`), secret-shaped output, and writes outside the declared paths. Quote the lines; classify each finding by severity; propose the minimal fix. Read-only: propose, do not edit.
