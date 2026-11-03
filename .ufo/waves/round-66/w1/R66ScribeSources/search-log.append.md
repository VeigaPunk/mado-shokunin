## Search log append — round 66 (draft only; L1 integrates)

Append as a new dated entry under `## Search log` (after the existing "Round 52" paragraph
and before the "Round 12" block, matching that section's reverse-chronological order).

Round 66 (2026-11-03), bounded question: which official document fixes the exit-status
vocabulary the C2 child-completion discriminations rely on (genuine red child rc=1 with its
marker, crash rc=2, skipped child with rc forced 0 and no marker, missing used-by sibling),
without asserting that any child ran or that a register row is true? Where: the GNU Bash
project's own release artifacts and manual, plus the CPython `subprocess` reference proposed by
the wave's scout. Identified 3, screened 3, included 1 (S435: Bash 5.3 release tarball →
`doc/bashref.texi` §3.7.5), excluded 2. Opened 2026-11-03: the HTML node
`Exit-Status.html` (5,187 B sha256 `b5489d3d…`), the single-page `bash.html` (1,040,954 B
sha256 `78d0eefb…`, version line "version 5.3, 18 May 2025"), the official release tarball
`bash-5.3.tar.gz` (11,355,854 B sha256 `0d5cd869…0f31ba`; `doc/bashref.texi` 415,804 B
sha256 `f3d37d57…32d5`), and `subprocess.rst` at tag v3.14.8 (61,603 B
sha256 `05cd782c…4dfd`). Excluded: (a) the HTML node as the row's *primary* anchor — live page,
no release tag, digest-only drift check; retained as the readable rendering of the same
section; (b) the CPython `subprocess.rst` row (scout `R66ScoutSources`
`source-row-candidate.md`) — its quote documents that a signal death reports a negative
returncode, which does not bind C2's rc=2 control, and it reuses S108's URL and byte-identical
file, so appending it would add a `W04 duplicate url` line while the same manual bytes are
already landed; its valid point (negative-signal returncode) is a crash-detection nuance the
instrument must handle, not a substitute for the rc-class vocabulary. Stop rationale: one row
covers the C2 rc classes from an immutable release artifact; the C1 side is a receipt-binding
counter rule with no source document, so further opening cannot change the registry. Status
changes this round: none — no existing row's `status`, `recheck` or `opened` cell is edited.
