# ReopenBash — holds: S110's bash-5.3 `set -e` clause is byte-identical at the tag and supports the knowledge note and SKILL; two bookkeeping defects stand (unmarked digest-only receipt; the Gate quote is a rendering, not byte-verbatim)

Row reopened: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:122` (S110).
Gate line: `corpus/lessons/round-20.md:47`. Claims checked against the knowledge note
(`corpus/knowledge/tripwire-precision-r20.md:65`), `SKILL.md:567`,
`corpus/QUALITY.md:243`, and the M2 lesson (`corpus/lessons/round-20.md:16`).

**Overall: the row's substantive claim survives every attack. The URL body, the tag
commit, the tag blob and the official tarball member are one identity; the quoted clause
is word-for-word at `:5940-5941` and the note/SKILL use it correctly. What fails is
bookkeeping: the rendered quote is not a byte substring of the Texinfo body (the lane's
own `fetch-verify --quote` says NOT_FOUND), and the seat's tarball receipt lacks the
`digest-only` marker, so the round-20 fetch tree reads `bad=1` in the worktree and
`bad=100` from a fresh clone.**

## 1. Source identity — every link reproduced (observed)

| Check | Command | Output (excerpt) | What would have shown the opposite |
|---|---|---|---|
| URL body | `curl -sSL --max-time 60 -o bashref-reopen.texi -w '%{http_code} %{url_effective}' 'https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?h=bash-5.3'` then `sha256sum` | `200 https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?h=bash-5.3`; `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`; `415804` B | any non-200, or a sha ≠ row's `f3d37d57…` |
| Tag pin | `git ls-remote https://git.savannah.gnu.org/git/bash.git 'refs/tags/bash-5.3*'` | `b8c60bc9ca365f8261fa97900b6fa939f6ebc303 refs/tags/bash-5.3` (single line, no `^{}` — lightweight) | a different commit, or an annotated peel disagreeing with the row |
| Tag checkout | `git clone --depth 1 --branch bash-5.3 …`; `git show bash-5.3:doc/bashref.texi \| sha256sum` | HEAD `b8c60bc9…`, `2025-07-03T16:15:36-04:00  Bash-5.3 distribution sources and documentation`; blob `f3d37d57…` | tag HEAD ≠ `b8c60bc9…`, or blob sha ≠ body sha |
| Official tarball | `curl https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz`; `sha256sum`; extract `bash-5.3/doc/bashref.texi`; `cmp` | tarball `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba`, `11355854` B; member `f3d37d57…`, `415804` B; `cmp … && echo BYTE_IDENTICAL` → `BYTE_IDENTICAL` | a different tarball digest or member, or `cmp` differing |
| Receipt agreement | `cat .ufo/waves/round-20/fetch/SrcBashErrexit/receipts.jsonl` | line 1: 200, `415804`, `f3d37d57…`; line 2: 200, `11355854`, `0d5cd869…` | receipt sha/bytes ≠ row |
| Row↔receipt join | `cd /tmp/mado-r20w2-ReopenBash && python3 -I .ufo/waves/round-18/fetch-verify.py --fetch-root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/fetch --sources /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md --rows S110` | `ROW S110 receipted` | `UNRECEIPTED` |

Ref-selectivity control (would have hidden a non-tag body behind the `?h=` query):
`?h=master` returns the same sha `f3d37d57…`, and a master checkout (`9c465866b7d8…
Bash-5.3 patch 20`, 2026-09-15) has the identical `doc/bashref.texi`; `?h=bash-5.2`
(`32ced60b…`, 374,486 B) and `?h=bash-4.4` (`90031c74…`, 328,634 B) differ, and
`?h=definitely-not-a-ref-zzz` timed out (000, 60 s). So `h=` is honoured, but the URL
alone does **not** distinguish the 5.3 tag from today's master; the `b8c60bc9…` commit
pin is load-bearing, not decorative.

## 2. Quote — word-exact at the stated lines; not byte-verbatim (observed)

`sed -n '5940,5941p'` on the fetched body:

```
5940  part of any command executed in a @code{&&} or @code{||} list except
5941  the command following the final @code{&&} or @code{||},
```

The row, the Gate line and the knowledge note print the **rendered** clause
(`@code{}` stripped, line-final comma dropped): "part of any command executed in a && or
|| list except the command following the final && or ||" — **20 whitespace words**,
within 25. Every word is in the stated lines, in order, and the clause is the load-bearing
part of the sentence that begins at `:5936`.

The lane's own probe discriminates the two forms:

```
QUOTE S110 ok                 # --quote 'S110=part of any command executed in a @code{&&} or @code{||} list except'
QUOTE S110 NOT_FOUND          # --quote 'S110=part of any command executed in a && or || list except the command following the final && or ||'
SUMMARY … quote_bad=1  exit=1
```

So "verbatim at the stated lines" is true of the Texinfo form and false of the printed
form. The w1 report already declares the normalization
(`.ufo/waves/round-20/w1/reports/SrcBashErrexit.md:21` "rendered; `@code{}`/`@option{}`
markup stripped"); the Gate line and the SOURCES anchor cell do not.

## 3. Does the row support the note and SKILL? — yes (observed + controls)

Behavioural checks on the host shell (`GNU bash, version 5.3.20(1)-release`), each with a
control that would have shown the opposite:

| Claim | Command | Output | Opposite would be |
|---|---|---|---|
| non-final `&&` member is exempt | `bash -c 'set -e; false && true; echo AFTER_1'` | `AFTER_1`, exit 0 | exit 1, no `AFTER_1` |
| *final* member is not exempt | `bash -c 'set -e; true && false; echo AFTER_2'` | no output, exit 1 | `AFTER_2` printed |
| compound block fed by exempt failure (`:5945-5947`) | `bash -c 'set -e; { false && true; }; echo AFTER_3'` | `AFTER_3`, exit 0 | exit 1, no `AFTER_3` |
| subshell is excluded (row says "other than a subshell") | `bash -c 'set -e; (false && true); echo AFTER_SUB'` | no output, exit 1 | `AFTER_SUB` printed |
| ERR trap obeys the same conditions (`:4797-4808`) | `bash -c 'set -Ee; trap "echo ERR_TRAP" ERR; false && true; echo AFTER_4'` | `AFTER_4`, no trap | `ERR_TRAP` printed |
| ERR trap control (final member) | `bash -c 'set -Ee; trap "echo ERR_TRAP" ERR; true && false; echo AFTER_5'` | `ERR_TRAP`, exit 1 | no trap |
| round-19 shape reproduces fail-open | `/tmp/errexit-shape-r20.sh`: `set -e`; `mount(){ return 1; }`; `[ -e /tmp ] && mount --bind x y && echo armed`; `echo PAYLOAD_RAN` | `PAYLOAD_RAN`, exit 0 (`armed` absent) | exit 1, no `PAYLOAD_RAN` |

Mapping to the downstream text:

- `corpus/knowledge/tripwire-precision-r20.md:65` — quote and rule ("bash does not exit
  when the failing command is …") are exactly the source's rule and the host behaviour.
- `SKILL.md:567` — "never rely on `set -e` across a `&&` list (S110)" is a correct
  conservative instruction. The precise rule is *non-final members*; the SKILL's phrasing
  (and the M2 line `lessons/round-20.md:16`, which already says "non-final") is safe but
  could state that boundary explicitly, since my final-member control exits 1.
- `corpus/QUALITY.md:243` — "bash 5.3 `set -e` exceptions (S110)" is supported; criterion
  29's own sentence ("`set -e` with a non-final `&&` member is not a gate") is the exact
  source rule.
- `corpus/lessons/round-20.md:16` — "(S110: `set -e` ignores a failing non-final `&&`
  member)" is correct.
- The row's `teaches` cell's incident sentence ("`[ -e ] && mount && echo` can arm
  nothing and still run its payload") matches the round-19 seat's own incident report
  (`.ufo/waves/round-19/w2/reports/SentinelGatePath.md`, §Incident) and my shape run.

## 4. Defects found (mechanical; substance unaffected)

**D1 — the SrcBashErrexit tarball receipt is not marked digest-only, so the round-20
fetch tree fails its own verifier.** Command (script copied from the clone, not run from
the lane worktree):

`cd /tmp/mado-r20w2-ReopenBash && python3 -I .ufo/waves/round-18/fetch-verify.py --fetch-root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/fetch --sources /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md --rows S110`

```
FETCH SrcBashErrexit/bashref.texi ok
FETCH SrcBashErrexit/bash-5.3.tar.gz MISSING
ROW S110 receipted
SUMMARY receipts=100 ok=99 bad=1 digest_only=0 non200=13 conflicts=0 rows=1 unreceipted=0
exit=1
```

The receipt's second line has no `"retain": "digest-only"` and round-20 has no
`fetch/RETENTION.json` (`ls` → No such file; `git ls-tree` at `a4046a8` shows only
`.gitignore` + 11 `receipts.jsonl`). Minimal fix demonstrated in `/tmp/fixretain`: adding
`"retain":"digest-only"` to that line yields
`FETCH … DIGEST_ONLY`, `SUMMARY receipts=2 ok=1 bad=0 digest_only=1`, `ROW S110
receipted`, exit 0. The row's bytes are independently verified (my own tarball fetch
matched `0d5cd869…`), so this is a receipt-accounting defect, not a false digest.

**D2 — round-wide: a fresh clone credits no S099–S112 row.** From my clone, with only the
tracked `receipts.jsonl` files (the bodies are gitignored as "digest-only", but no
machine-readable marker exists):

`cd /tmp/mado-r20w2-ReopenBash && python3 -I .ufo/waves/round-18/fetch-verify.py --fetch-root /tmp/mado-r20w2-ReopenBash/.ufo/waves/round-20/fetch --sources /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md --rows S110`

```
FETCH SrcBashErrexit/bashref.texi MISSING
FETCH SrcBashErrexit/bash-5.3.tar.gz MISSING
ROW S110 UNRECEIPTED body-unverified
SUMMARY receipts=100 ok=0 bad=100 digest_only=0 non200=0 conflicts=0 rows=1 unreceipted=1
exit=1
```

`fetch-verify.py:118-135` treats an absent body as `DIGEST_ONLY` only when a
`RETENTION.json` entry or a per-receipt `retain:"digest-only"` says so. Round 19 shipped
`.ufo/waves/round-19/fetch/RETENTION.json`; round 20 did not. The `.gitignore` comment
("Round-20 fetch bodies are digest-only") and the Gate prose (`round-20.md:26-27`) assert
the status, but the verifier cannot see it. This affects every row admitted this round,
not only S110.

**D3 — Gate wording, "five-way byte agreement".** The w1 table
(`w1/reports/SrcBashErrexit.md:9-15`) lists five objects, but only three are independent
byte sources (git blob at the tag, cgit body, tarball member); the other two are identity
anchors (the `refs/tags/bash-5.3` ref and the checked-out commit). All three byte objects
agree (`f3d37d57…`); the phrase should say so.

**D4 — anchor is short of the `@item -e` entry.** `@item -f` begins at `:5964`, so the
`-e` entry ends at `:5962`, not `:5958`. The row's `5929-5958` cuts the entry's last
sentence at `:5959-5962` ("If a compound command or shell function sets -e while executing in a
context where -e is ignored, that setting will not have any effect until …"). That is not
one of the "which failing commands do not terminate" exceptions, so the scope claim
survives; extending the anchor to `:5962` would make the anchor match the entry.

**D5 (low, convention) — `used-by` understates S110's consumers.** `SOURCES.md:122` lists
only `corpus/knowledge/tripwire-precision-r20.md`; `SKILL.md:567`, `QUALITY.md:243` and
`lessons/round-20.md:16,47` cite S110 directly. All 14 new rows (S099–S112) list only the
note, so this looks like a deliberate round-level convention [INFERENCE], not an
S110-specific error; flagging it because `used-by` is meant to make usage re-findable.

## 5. My fetch receipts (contract fields)

Written to `.ufo/waves/round-20/w2/ReopenBash/fetch/receipts.jsonl`; body
`bashref-reopen.texi` (415,804 B, `f3d37d57…`) stored beside it, tarball receipt marked
`"retain":"digest-only"` (11,355,854 B, `0d5cd869…`, body not stored).
Verified in a seat-shaped root (the lane verifier globs `<root>/<seat>/receipts.jsonl`):

```
FETCH ReopenBash/bashref-reopen.texi ok
FETCH ReopenBash/bash-5.3.tar.gz DIGEST_ONLY
ROW S110 receipted
SUMMARY receipts=2 ok=1 bad=0 digest_only=1 non200=0 conflicts=0 rows=1 unreceipted=0
```

## Limits

- Behavioural checks cover the 5.3.20 host shell and the six cases above; no interactive
  shell, `--posix`/`inherit_errexit`, or 5.0–5.2 comparison was run.
- The cgit host is flaky (w1 saw a 502 and a 60 s timeout; my unknown-ref probe timed out
  at 60 s with 0 bytes). The tag identity does not depend on cgit: the clone blob and the
  ftp.gnu.org tarball member both reproduce `f3d37d57…`.
- "Verbatim" is judged two ways: word-exact at the lines (true) and byte substring
  (false; Texinfo markup). The byte test is the lane's `fetch-verify --quote`, which
  exits 1 on the printed form.
- The 25-word rule was applied by whitespace split; the printed quote is 20.
- I did not re-run any other seat's lane script; `fetch-verify.py` was executed from its
  bytes in my `/tmp` clone against read-only lane inputs.
- Lane checkout was read-only; git/jj writes and host-paused commands: none. Scratch:
  `/tmp/mado-r20w2-ReopenBash`, `/tmp/bashgit-reopen`, `/tmp/bash-5.3-reopen*`,
  `/tmp/fixretain`, `/tmp/errexit-shape-r20.sh`.

## Installs

none.
