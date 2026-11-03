# Candidate comparison — S435 (scribe decision record, round 66)

Two seats proposed a row at the same free id `S435`: this seat (Bash exit status) and
`R66ScoutSources` (CPython `subprocess.rst` returncode). L1's guidance on 2026-11-03 was
"prefer scoped Bash row C2". This file records the evidence behind that choice so the
decision is auditable, not asserted.

## Candidates

| | A — this seat (allocated) | B — scout (not allocated) |
|---|---|---|
| Source | GNU Bash 5.3 release tarball → `doc/bashref.texi` §3.7.5 | CPython v3.14.8 `Doc/library/subprocess.rst` `returncode` |
| Immutability | release tarball, sha256 `0d5cd869…`; texi sha256 `f3d37d57…` | tag v3.14.8 → `8e6e75d9…`; file sha256 `05cd782c…` |
| Quote (words) | 15: "So while an exit status of zero indicates success, a non-zero exit status indicates failure." | 23: "Exit status of the child process, an integer. If the process exited due to a signal, this will be the negative signal number." |
| Binds C2 rc classes | yes: 0 / non-zero / 126 / 127 / 128+N / builtin 2, plus "status is what `waitpid` returns" | partially: 0 and non-zero, and negative for signals; no 126/127/128+N class table |
| Duplicate-URL effect | none: tarball URL unused; HTML node URL unused (S110 uses the cgit texi URL) | adds one `W04 duplicate url` line: S108 already holds the same `subprocess.rst` URL |
| Novelty | new document in the registry (manual scope distinct from S110's `set -e`) | same file and bytes as S108, new attribute scope |
| Cross-row check | tarball and texi digests independently reproduce S110's recorded values | tag object and file digest reproduce S108's recorded values |

## Why A

1. **Fit to the predicate.** C2's controls are expressed in shell rc classes (1 vs 2,
   forced 0). §3.7.5 is the document that defines those classes and says plainly that the
   status is the value the child returns, not a record of what it did. Candidate B documents
   one attribute of one run child; its distinctive clause (negative signal numbers) does not
   describe either control, because the crash control is rc=2, not a signal death.
2. **Census neutrality.** A adds no warning line; B adds a `W04` line at a round whose
   acceptance is "no new warning naming S435". W04 is warning-only, but the cleaner append is
   the one that leaves the shape unchanged.
3. **No harm to either candidate.** B remains a valid future row (distinct scope, no
   correction of S108) if a later round needs signal-vs-exit-code discrimination; nothing in
   A's append blocks it.

## Residual risk recorded

- A is a *manual* row: it fixes vocabulary, not instrument behaviour. If the C2 instrument
  maps rc without checking signal death, candidate B's clause would have been the better
  warning; the C2 seat's selftest is the place that must cover it, not this row.
- Neither candidate proves child invocation or row truth; both are vocabulary only.
