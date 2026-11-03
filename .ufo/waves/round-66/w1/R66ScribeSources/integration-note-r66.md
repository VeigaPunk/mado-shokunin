# Integration note — S435 as landed (recorded by R66ScribeSources, 2026-11-03)

L1 integrated `S435` with the compact HTML-manual URL as canonical and my release-anchor
evidence retained. This note records what landed, the one live census consequence, and the
one line of my search-log draft that no longer matches the row. Nothing here re-opens the
predicate or re-opens any row.

## Landed row (read at `corpus/SOURCES.md:385`, 11 cells)

- id/kind/tier: `S435`, `docs`, `A`
- source: "GNU Bash 5.3 official release manual — https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html"
- scope: "documented exit-status vocabulary supporting the round-66 C2 distinction between ordinary red and execution failure; not row truth or child invocation"
- anchor: "Bash Reference Manual 5.3 §3.7.5 Exit Status; release doc/bashref.texi:3902-3906,3911-3916,3925-3928 (release tarball sha256 `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba`); HTML rendering opened 2026-11-03"
- teaches: "Zero is the shell success convention; 126 and 127 distinguish execution failures and 128+N fatal signals. The lane separately requires child markers as policy, not proof of truth or honest invocation."
- status/opened/recheck/used-by: `mined` / `2026-11-03` / `on-release` / `corpus/lessons/round-66.md`
- URLs in the row: only the HTML node; it was unused before (`grep -c` 0), so no `W04`.

## Post-integration census (one run, this read)

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` →

- **rc=1**, sole new line: `mado	E11	S435 missing used-by corpus/lessons/round-66.md`
- everything else identical to `census-start-r66.txt`: 36 `W04` + 1 `W01`, no line naming
  S435 other than that E11; normalized diff vs start is exactly that one line replacing the
  `ok`/`exit=0` trailer.
- shape is the predicted one: rows 371→**372**, `tier.A` 357→**358**, `tier.B` 7, `tier.C` 7,
  `status.mined` 350→**351**, `queued` 10, `rejected` 11.

Meaning: the row is shape- and URL-clean; the only red is the not-yet-written lesson. `E11`
checks existence of the used-by path, so creating `corpus/lessons/round-66.md` clears it —
and L1 states the lesson will cite S435, which also satisfies the contract's mined-used-by
expectation beyond bare existence. If the lesson is not landed this round, the census end
receipt is red by design and the row should have been `queued` with `used-by —` instead.

## Search-log draft correction (replace the exclusion clause)

My `search-log.append.md` was written when the tarball was the proposed canonical URL, so it
describes the HTML node as *excluded from being the primary anchor*. The landed row uses the
HTML node as canonical, so that clause must not be integrated verbatim. Replacement paragraph
for the round-66 search-log entry (rest identical in intent to the draft):

> Round 66 (2026-11-03), bounded question: which official document fixes the exit-status
> vocabulary the C2 child-completion discriminations rely on, without asserting that any
> child ran or that a register row is true? Where: the GNU Bash manual's Exit Status node
> (canonical URL of S435, opened 2026-11-03), the single-page manual for the version line,
> the official `bash-5.3.tar.gz` release as the release/version anchor (`doc/bashref.texi`
> §3.7.5, tarball sha256 `0d5cd869…0f31ba`), and CPython `subprocess.rst` at tag v3.14.8
> proposed by the scout. Identified 3, screened 3, included 1 (S435: HTML node canonical,
> release tarball as anchor). Excluded 1: the CPython `subprocess.rst` row — its
> negative-signal `returncode` clause does not describe C2's rc=2 crash control, and it
> reuses S108's URL with byte-identical content, which would add a `W04 duplicate url` line.
> The live-page-only anchor was likewise not used *alone*: the release tarball supplies the
> version pin the HTML node lacks. Stop rationale: one row covers the C2 rc classes; the C1
> side is a receipt-binding counter rule with no source document. Status changes this round:
> none — no existing row's `status`, `recheck` or `opened` cell is edited.

## Draft status

`SOURCES.append.md` and `gate-r66-s435.md` record my proposed tarball-canonical variant and are
now superseded by the landed compact row; they are kept unchanged as the draft of record.
`candidate-comparison.md`, `census-r66.md` and `scribe-evidence.txt` remain accurate as
recorded, except the census expectation above (E11 until the lesson exists).
