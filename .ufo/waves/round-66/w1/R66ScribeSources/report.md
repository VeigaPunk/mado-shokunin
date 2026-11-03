# R66ScribeSources — report

Seat: mado round 66, wave w1, scribe (source curation). Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`, observed HEAD
`ed980316e330703030d0c17b2a7098e058295b99` (the frozen declaration names base
`eafd500f…`; the delta was not reconciled here). Date 2026-11-03. Leaf seat: no
agents spawned, no installs, no pacman, no git/jj mutation, no writes outside
this seat dir and `/fast/scratch/hyaku/mado-r66/R66ScribeSources/`, no
config/session/credential reads, no r56-era material.

## Deliverable

Source support for **C2 child-completion semantics**, drafted as exactly one new
tier-A docs row (`S435`) plus its Gate block, search-log entry, census
instructions and a candidate-decision record. Nothing was written to `corpus/**`;
the live registry is untouched (`git status --porcelain -- corpus/` → 0 lines).

| Draft | Path | What it is |
|---|---|---|
| Row | `SOURCES.append.md` | S435, GNU Bash 5.3 release tarball → `doc/bashref.texi` §3.7.5 Exit Status, ready to append after S434 |
| Search log | `search-log.append.md` | round-66 entry: 3 identified, 3 screened, 1 included, 2 excluded, with reasons |
| Gate | `gate-r66-s435.md` | access date 2026-11-03, 15-word located quote, 19-word supporting quote, release/digest anchor, limits |
| Census | `census-r66.md` | start/end commands, expected rc, warning baseline, expected shape delta, receipt placement |
| Decision | `candidate-comparison.md` | this row vs the scout's CPython row at the same id, with the evidence for the choice |
| Evidence | `evidence.sh` + `scribe-evidence.txt` | re-runnable producer and its transcript; every producer rc recorded |

## What I ran (read-only; full output and every rc in `scribe-evidence.txt`)

| Command | Output | rc |
|---|---|---|
| `read https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html` | §3.7.5 full text (opened this round) | — |
| `curl https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz` + `sha256sum` | 11,355,854 B, `0d5cd869…0f31ba` | 0 |
| `tar -xzf … bash-5.3/doc/bashref.texi` + `sha256sum` | 415,804 B, `f3d37d57…32d5` | 0 |
| `grep -n '@node Exit Status\|exit status of zero indicates\|returns a status of 127\|status of 2 to indicate'` | `:3890`, `:3905`, `:3915`, `:3928` | 0 |
| `curl` HTML node + single-page manual + `sha256sum` | 5,187 B `b5489d3d…`, 1,040,954 B `78d0eefb…`; version line "version 5.3, 18 May 2025" | 0 |
| `bash --version \| head -1` | `GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)` | 0 |
| `curl subprocess.rst` @ v3.14.8 + `sha256sum` + quote sed | 61,603 B `05cd782c…`; 23-word quote at `:242-243` | 0 |
| `grep -c 'subprocess.rst' corpus/SOURCES.md` | `1` (S108 holds that URL) | 0 |
| `grep -o '^\| S[0-9]\{3\}' corpus/SOURCES.md \| sort -u \| tail -3` | S432, S433, S434 | 0 |
| `grep -c '^\| S435 ' corpus/SOURCES.md` | `0` (id free) | 1 (no match) |
| `grep -c 'bash-5.3.tar.gz\|Exit-Status.html' corpus/SOURCES.md` | `0` (both URLs unused) | 1 (no match) |
| `sources-census.sh census --root <fleet> mado` | rows 371, A 357, B 7, C 7, mined 350, queued 10, rejected 11 | 0 |
| `sources-census.sh validate --root <fleet> mado` | `exit=0`, 36 `W04` + 1 `W01` lines, `mado ok …/SOURCES.md` | 0 |
| `diff census-now.txt census-start-r66.txt` | only the recorded command line and `exit=0` trailer differ | 1 (expected) |
| A/B on mirror lanes (registry base vs base+S435) | both `rc=0`; 36 `W04` + 1 `W01` each; shape 372/358/351 on the row side; diff = the `ok` path only; **0** findings name S435 | 0 / 0 |
| Re-fetch of HTML copies after deletion, re-hash | identical digests and sizes | 0 |

## Why this row and not another

- The declaration's sourced-claim slot for C1 is a *receipt-binding* rule (exactly one
  heading, one row per group, a resolving receipt per row, the exact live CLEAN line). No
  official document defines mado's receipt cells: that clause is counter design, and a row
  pretending otherwise would be a false binding. C1 gets no row and no document claim.
- C2's discriminations rest on a documentable vocabulary: what an exit status *is*, what
  126/127/128+N/2 mean, and that the status is declared by the child rather than observed
  from its work. §3.7.5 states exactly that and stops short of markers — the limit the row
  states.
- Anchor choice: the row points at the **immutable release tarball** (`bash-5.3.tar.gz` →
  `doc/bashref.texi`), with the live HTML node kept as the readable rendering. Both digests
  independently reproduce the values S110 already records for its own tag-anchored read, so
  the release bytes in the lane are the ones quoted here. A live-page-only anchor was
  rejected as digest-only with no release tag.
- The scout's CPython `subprocess.rst` row (same file as S108, byte-identical) was screened
  and not allocated: its 23-word quote binds a negative signal returncode, which does not
  describe either C2 control (the crash control is rc=2, not a signal death), and appending
  the same URL would add a `W04 duplicate url` line. Full reasoning in
  `candidate-comparison.md`.

## Limits (stated with the draft, not after it)

1. **No row truth.** The source cannot establish any register state cell (C1) — that stays
   unmeasured, as the declaration already says.
2. **No child invocation.** It cannot show that a child ran, returned a given rc, or emitted
   a marker (C2). It defines the vocabulary a counter may use; the counter's own hermetic
   tests must prove the rest.
3. **Series, not binary.** The manual describes the 5.3 series; it does not claim
   5.3.20 behaviour even though the host runs 5.3.20(1).
4. **Rendering drift.** The tarball is immutable; the HTML node is live and digest-pinned
   only, so a re-read must re-hash it.
5. **Class, not instance.** "All builtins return … 2 to indicate incorrect usage" is a builtin
   rule. The C2 use of rc=2 as a crash class is the lane's convention, and the row's scope
   says so.
6. **Dependency on the lesson file.** `used-by: corpus/lessons/round-66.md` does not exist
   yet. The census `E11` check resolves used-by paths, so the row must be integrated
   **together with** (or after) that lesson; the A/B fixture shows E11 stays silent once the
   file exists.
7. No knowledge entry is claimed; no existing row's `opened`, `recheck`, `status` or
   `used-by` cell is edited (r65 closure defect M65-4).

## Findings for L1

1. `S435` is free: highest committed id `S434`, `^| S435 ` count 0, and both row URLs are
   unused — no duplicate-URL warning expected.
2. Census at this seat's read is identical to `census-start-r66.txt` except its own
   header/trailer, so nothing in the live tree moved under me.
3. The append was simulated before delivery: mirror lanes with the real registry vs the
   registry plus S435 (and a placeholder `corpus/lessons/round-66.md`) both return **rc=0**,
   36 `W04` + 1 `W01` each, and their normalized census output differs only in the
   terminal `ok` path line — zero findings name S435. Expected shape delta after landing:
   rows 371→372, tier A 357→358, mined 350→351.
4. Three pre-existing warning lines are CPython rows this seat did not read (`S119` duplicate
   `imaplib.py` URL, `S120`/`S121` duplicate `executionmodel.rst` URL) plus `S277`
   tier-C/mined; they stay in the start warning set, are not touched, and are not evidence
   against S435.
5. `recheck` for S435 is `on-release`, not a date: a release tarball is immutable, and a
   newer Bash release is a re-open, not a silent re-point.
6. ID contention: `R66ScoutSources` also proposed `S435` (CPython). L1's stated preference
   is the Bash row; the comparison record keeps the scout's candidate as a valid future row
   (distinct scope, no correction of S108). Only one row is appended.

## Integration addendum (recorded after L1 landed the row, 2026-11-03)

L1 integrated `S435` with the **HTML-manual node as canonical URL** and my release-anchor
evidence retained (`doc/bashref.texi` lines + `bash-5.3.tar.gz` sha256), and worded `teaches`
so markers are lane policy, not proof. No existing row changed. This supersedes the
tarball-canonical proposal in `SOURCES.append.md`/`gate-r66-s435.md`, which stay as the draft
of record.

Post-integration census (one run): **rc=1**, sole delta vs `census-start-r66.txt` is
`mado	E11	S435 missing used-by corpus/lessons/round-66.md`; 36 `W04` + 1 `W01` unchanged, no
URL warning for S435, shape 372/358/7/7 with mined 351 as predicted. The red is the not-yet
written lesson: `E11` tests used-by existence, so landing `corpus/lessons/round-66.md` clears
it (the lesson will cite S435). Full record: `integration-note-r66.md`.

Search-log mismatch found and corrected in that note: my draft described the HTML node as
excluded from being the primary anchor, which no longer matches the landed row; a replacement
paragraph is supplied so the integrated search log does not contradict the registry.
