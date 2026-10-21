# UvPackageHelp oracle

## Axes

- **C1 — operability residual repair:** the registered case distinguishes bare `uv tool run --help` from a package-taking run with trailing `--help`.
- **C2 — calibration independent artifact integrity:** not assessed by this single C1 oracle.

## Ruling

Affirm the proposed semantic class **install** for `uv tool run package-not-executed --help`.

The tagged uv 0.13.4 test `tool_run_args` distinguishes option placement: `--help` before `pytest` is uv's own help, but `pytest --help` after the package target reaches pytest; the recorded output includes resolution, preparation, and installation of packages. The tagged tools guide states that `uvx` aliases `uv tool run`, accepts arguments after the tool name, and runs tools in temporary isolated environments. Consequently, the package-taking form is an acquisition/install path even though `--help` follows it. The expectation is about command semantics, not successful resolution of the literal placeholder; this seat did not execute the command.

Committed round-20 `ReviewVcsV3.md` provides the relevant contrast: line 85 records measured no-change behavior for bare `uv tool run --help`; lines 86 and 96 say the package-taking form was not executed because it could fetch/install a package. Thus the package-taking result is source-grounded rather than a new runtime measurement. It is **not** a claim that the command writes Git/JJ repository objects, index, config, workspace state, or refs; the VCS repository-write boundary is separate from this tool-install class.

## Verification limits

No VCS, installer, package command, fixture transcript, or classifier was executed. The package operand's actual registry resolution and resulting filesystem writes remain unmeasured for this exact placeholder.

Report: .ufo/waves/round-21/w1/reports/OracleUvPackageHelp.md
