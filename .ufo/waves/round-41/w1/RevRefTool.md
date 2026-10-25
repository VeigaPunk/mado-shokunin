# Seat report — RevRefTool (round-41 w1, C1 reference review)

Full findings: `.ufo/waves/round-41/w1/RevRefTool/findings.md`.

## Summary
Reviewed the frozen reference `c1/ctl-ref-tool.py.txt` (the likely delivered
`tools/mado-globals.py`) against the PRED-C1-r41-v1 docstring.

- **Score baseline:** I ran the counter at tip rev `cd950ec781149040cc73d71cd67c2b67452e7724`
  with `--tool` pointing at a copy of the reference: `fixtures=24/24
  tool=present verdict=TARGET_MET` (a b b2 g all 1; selftest 47/47; b2 sites=12
  killed=6/6). Matches `receipts/ctl-c1.txt`.
- **Host live sanity** (allowed read-only journal verb): `--live` → 2 sessions,
  63/63 interfaces in latest, `hyprland_focus_grab_manager_v1 ver=1 class=focus-grab`,
  rc=0; `--live --diff` rc=0. Matches the fetch receipt census.

## Findings (severity order; repros in findings.md)
- M1 Medium — `--journal-file` on a FIFO hangs forever (`open()` blocks, no
  timeout; verified `timeout 4` → 124). Lines 194–196.
- M2 Medium — `--live` output cap is post-hoc: entire stream buffered before the
  8 MiB check; 300 MB writer → 615 MB child peak RSS (verified). Lines 179–189.
- L1 Low — slow-but-large live output reports `journalctl_failed` (timeout wins),
  not `journalctl_too_large` (verified with 31 s stub). Lines 179–189.
- L2 Low — a group-writable candidate earlier in PATH blocks a later valid
  program (`journalctl_unusable`); shells would keep searching. Lines 155–170.
- L3 Low — stat/access → exec TOCTOU in `resolve_program` (informational;
  sandbox-bound). Lines 154–171.
- L4 Low — PATH unset/empty makes bare `journalctl` resolve to cwd (verified;
  POSIX-consistent, worth documenting). Lines 156–157.

Typeed OK (no finding): directory as journal-file (rc 2 unreadable), non-UTF-8
path, symlinked program incl. group-writable-target rejection, Python-keyword
names, `ver 000001`, huge counts, all exit codes, stdout/stderr discipline
(always report on stdout, empty stderr), `--expect` dedupe, diff ordering, verdict
precedence.

## Tooling recorded
- None installed (probes used stock python3/bwrap and the reference copy);
  no pacman, no host/compositor/journal mutation. Scratch `/tmp/revref` removed.

## Handoff
- Main: re-run counter at data tip when C1 lands; findings M1/M2 (FIFO hang,
  unbounded live buffering) are the only ones above a "documented quirk"
  threshold — both live in the declared residual space (registration §Residuals).
- No files outside `.ufo/waves/round-41/w1/RevRefTool/` were written.
