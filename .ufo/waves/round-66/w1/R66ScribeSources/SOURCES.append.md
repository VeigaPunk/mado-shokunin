## SOURCES append — round 66 (draft only; L1 integrates)

Placement: last line of the `## Registry` table, immediately after the `S434` row and before
the blank line that precedes `## Paths`. Appending this block changes no existing row,
including every `opened` cell (r65 closure defect M65-4: no `opened`/`recheck` rewrite).

| S435 | GNU Bash 5.3 official release tarball — `doc/bashref.texi` §3.7.5 Exit Status (HTML rendering: https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html) — https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz | docs | A | the release-tagged exit-status classes a shell receives from an executed command (0 success convention, non-zero failure, 127 not found, 126 not executable, 128+N fatal signal, builtin misuse 2), scoped to the round-66 C2 child-completion rc vocabulary; not a marker, receipt or row-truth source | tarball 11,355,854 B sha256 `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba`; extracted `doc/bashref.texi` 415,804 B sha256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`; §3.7.5 `@node Exit Status` :3890, `@subsection` :3891, quotes :3902-3906, :3911-3912, :3914-3916, :3925-3928; HTML node `Exit-Status.html` 5,187 B sha256 `b5489d3d21e32da01de356e7a63093ec276a60a020d616a05fffcc9b7b19d983` (version line "5.3, 18 May 2025" is on the single-page manual, sha256 `78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b`); host `bash --version` → `5.3.20(1)-release`; opened 2026-11-03 | an exit status is the value returned through `waitpid`, so zero is a success convention the shell applies and non-zero the failure signal; 126/127 mark the child failing to execute the named command and 128+N a fatal-signal termination; a wrapper-forced 0 is therefore indistinguishable in the status from genuine success, and no status records what work the child did — completion needs a separate marker (C2), never an rc inference | mined | 2026-11-03 | on-release | corpus/lessons/round-66.md |

Notes for the integrator:
- ID allocation checked against the committed registry: highest existing id `S434`, `S435`
  absent (`grep -c '^| S435 '` → 0). The HTML node URL is unused (0 prior rows) and the
  tarball URL is unused as a URL; S110 mentions the tarball *filename and digest* in its
  anchor while its own URL is the cgit `bashref.texi` — so no `W04 duplicate url` line is
  expected, and the tag release pin is stronger than the live HTML page.
- The tarball digest independently reproduces S110's recorded value
  (`0d5cd869…0f31ba`) and the texi digest reproduces S110's (`f3d37d57…32d5`), so the same
  manual bytes already in the lane are the ones this row quotes; this row does not supersede
  S110 and does not restate its `set -e` scope.
- `recheck: on-release` — a release tarball is immutable; recheck moves when the lane adopts a
  newer Bash release, at which point the row is re-opened (not silently re-pointed).
