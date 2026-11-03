# R66ScribeSources — source curation for C1 binding / C2 child completion

Seat: mado round 66, w1, scribe (sources). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`,
observed HEAD `ed980316e330703030d0c17b2a7098e058295b99`, date 2026-11-03. Leaf: no spawn, no
installs, no git/jj mutation, no writes outside `.ufo/waves/round-66/w1/R66ScribeSources/` and
`/fast/scratch/hyaku/mado-r66/R66ScribeSources/`. The live registry `corpus/SOURCES.md` was
**not** edited (`git status --porcelain -- corpus/` → 0).

## Outcome

One draft tier-A row, `S435`, grounding **C2 child-completion rc vocabulary**; the C1 side gets
no row because its receipt-binding clauses have no documentary source. Drafts (all in the seat
dir, listed in `report.md`): `SOURCES.append.md`, `search-log.append.md`, `gate-r66-s435.md`,
`census-r66.md`, `candidate-comparison.md`, `evidence.sh`, `scribe-evidence.txt`, `report.md`.

## Axes this seat moves (and only these)

- **Calibration (C1)**: no move claimed. The register's receipt-binding rule is a counter design
  fact; a document row cannot support it, and the seat's limit states that plainly.
- **Operability (C2)**: the rc classes the instrument discriminates (0 / non-zero / 126 / 127 /
  128+N / builtin 2) now have an official, release-anchored, digest-pinned source, plus the
  negative teaching that a forced rc=0 is not distinguishable from success by status alone.

## Gate (as drafted for `corpus/lessons/round-66.md`)

- Source: GNU Bash 5.3 release tarball → `doc/bashref.texi` §3.7.5 Exit Status —
  https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz (readable rendering of the same section:
  https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html)
- Access date: **2026-11-03** (opened this round: tarball fetched and extracted, HTML node read,
  single-page manual read for the version line, all re-hashed after deletion).
- Located quote (15 words, ≤25): "So while an exit status of zero indicates success, a non-zero
  exit status indicates failure." — `doc/bashref.texi:3905-3906`; same text at
  `Exit-Status.html:68-69`.
- Supporting quote (19 words): "If a command is not found, the child process created to execute
  it returns a status of 127." — `doc/bashref.texi:3914-3915`, `Exit-Status.html:77-78`.
- Version/section: §3.7.5 (`@node Exit Status`, texi:3890) of Bash **5.3**. Digests: tarball
  11,355,854 B `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba`; texi
  415,804 B `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`; HTML node
  5,187 B `b5489d3d21e32da01de356e7a63093ec276a60a020d616a05fffcc9b7b19d983`; single page
  1,040,954 B `78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b`
  ("version 5.3, 18 May 2025").
- Cross-check: tarball and texi digests reproduce S110's recorded values exactly; S110's cgit
  URL and `set -e` scope are untouched.
- Host binding: `bash --version` → `5.3.20(1)-release`.

## Candidate decision (same id proposed twice)

`R66ScoutSources` proposed `S435` for CPython `subprocess.rst` returncode (61,603 B
`05cd782c…`, 23-word quote at `:242-243`). Not allocated: its clause binds negative-signal
returncodes, which do not describe either C2 control (the crash control is rc=2, not a signal
death), and it reuses S108's URL with byte-identical content, which would add a
`W04 duplicate url` line. L1's stated preference is the Bash row. The scout's candidate remains
a valid future row; nothing here blocks it. Evidence: `candidate-comparison.md`.

## Limits (exact)

1. Cannot prove any register row's truth (C1 state cells stay unmeasured), nor that any child
   ran, returned a given rc, or emitted a marker (C2). Vocabulary only.
2. Manual describes the 5.3 series; it does not pin 5.3.20 behaviour.
3. Tarball is immutable; the HTML node is live and digest-pinned only.
4. The "builtin misuse returns 2" clause is a shell-builtin rule; the lane's rc=2 crash class is
   a convention, not this source's claim.
5. `used-by: corpus/lessons/round-66.md` does not exist yet — integrate the row with/after the
   lesson or census `E11` fires on an unresolvable used-by path.
6. No knowledge entry claimed; no existing row's `opened`/`recheck`/`status`/`used-by` edited.

## Census

Live lane: `validate --root /home/vgpnk/Projects/shokunin mado` → **rc=0**, 36 `W04` + 1 `W01`
pre-existing lines, `mado ok …/SOURCES.md`; `diff` against `census-start-r66.txt` differs only in
the command line and `exit=0` trailer. Shape baseline: rows 371, A 357, B 7, C 7, mined 350,
queued 10, rejected 11.

Pre-integration A/B (mirror lanes, registry base vs base+S435, placeholder
`corpus/lessons/round-66.md`): both **rc=0**, 36 `W04` + 1 `W01` each, shape on the row side
372/358/7/7 with mined 351, normalized output differing only in the terminal `ok` path, and no
finding names S435. Start/end commands and acceptance criteria are in `census-r66.md`; receipts
belong at the round root, outside `.ufo/waves/round-66/receipts/`.

## Id / collision check

Highest committed id `S434`; `^| S435 ` count 0; `bash-5.3.tar.gz` and `Exit-Status.html` both
unused as URLs (S110 cites the cgit texi URL, not these); token `S435` exists only in these
drafts. No duplicate-URL warning expected from the append.

## Integration addendum (after L1 landing, 2026-11-03)

Landed form: `S435` canonical URL is the HTML node `Exit-Status.html` (opened 2026-11-03), with
the Bash 5.3 release anchor retained as `doc/bashref.texi:3902-3906,3911-3916,3925-3928` +
tarball sha256 `0d5cd869…0f31ba`; `teaches` labels child markers as lane policy, not proof. One
post-integration census run: **rc=1**, sole delta
`mado	E11	S435 missing used-by corpus/lessons/round-66.md`; W04/W01 set unchanged, shape
372/358/7/7 with mined 351. The red clears when the lesson file exists. Draft tarball-canonical
files are superseded by the landed compact row; the search-log clause that no longer matches
the row is replaced in `R66ScribeSources/integration-note-r66.md`.
