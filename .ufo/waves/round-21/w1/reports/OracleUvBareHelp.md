# OracleUvBareHelp — independent C1 expectation

## Axes and disposition

- **C1 — operability residual repair:** retain the proposed `clean` expectation for the exact bare command `uv tool run --help`. This is an independently documented semantic expectation; it does not claim a classifier result or repair.
- **C2 — calibration / independent artifact integrity:** outside this seat's scope; no C2 judgment is made.

## Finding

The committed round-20 `ReviewVcsV3` evidence records `uv tool run --help` exiting successfully and printing uv's runner usage, with neither the redirected `UV_TOOL_DIR` nor `UV_CACHE_DIR` changing. The report states the reason for the no-acquisition expectation: this exact command has no package operand and performs no fetch/install (`ReviewVcsV3.md:33-35,85`). Therefore the oracle expectation is **clean** for tool acquisition. A `--help` token after a package operand is a different form and is not covered by this expectation.

This is scoped to the reported bare-help behavior. It does not claim that all uv commands or all configurations are globally side-effect-free, and it does not narrow the round-21 VCS boundary for repository objects, indexes, configuration, or workspaces.

## Verification limits

This seat relied on the committed round-20 measurement as historical evidence; it did not repeat the command. No VCS/installer command, fixture or transcript, classifier, gate, or other runtime was executed or invoked. No tool was installed or updated. The round-20 review says package-taking uv runner variants were not run because they could fetch/install; this oracle makes no claim about those variants.

**Source:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/review/ReviewVcsV3.md:33-35,85,94-97`.
