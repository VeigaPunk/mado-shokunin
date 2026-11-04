# R70ScribeEntryC1 — claim C1 knowledge entry

Seat scope: draft `corpus/knowledge/landing-kill-credit-real-children-r70.md` only. No production
path, lane git state, declaration, control JSON or baseline receipt was written or re-scoped. The
L1 integrated a production entry concurrently; it was read, never edited.

## Artifact

| path | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-70/w1/R70ScribeEntryC1/draft/corpus/knowledge/landing-kill-credit-real-children-r70.md` | 245 | 15955 | `80b360bcbf3f51219fc087a813df404666b1a2cde796457475af20b47fd69cbb` |

Grammar copied from `corpus/knowledge/gate-guard-dominance-r69.md`: `source:` / `verified-at:` /
`recheck:` header, `# … (MADO-R70-1)`, `## Scope`, sections 1–5, `## Evidence rows`, `## 6.
Recheck and provenance`. `## 4. Limits — what the counter cannot do` is the Limits section.

## Findings (evidence only from committed bytes and receipts)

1. **Source plan, final.** `corpus/lessons/round-70.md` § Gate (written 23:44) **admits S441** =
   `https://docs.python.org/3.14/library/subprocess.html` (rendered, sha256
   `c8a66b3abf91790cea34128c5636c2e27a4b26ade459f7d4f797400da706079f`, 207,155 B, anchor
   `subprocess.html:360-366`) and **rejects** the raw `Doc/library/subprocess.rst` as a duplicate
   of S108; **S435** stays the held multi-cause vocabulary. The draft follows that adoption:
   `source:` line cites S441 plus held S435; the pins table cites S441 only; S435's facts are
   cited in prose with `bashref.texi` locators.
2. Repaired harness: `summary_shows_failure` at `quality/counters/c1-r70-landing-controls.py:315-330`
   (sha256 `71a7b6c4…`), decision `mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))`
   at `:478`; five summary cases `:719-727`; `mz-crash` / `mz-allpass` non-kill cases `:701-717`.
   Held rule `mz_killed = mz_rc != 0` at `quality/counters/c1-r69-landing-controls.py:452`
   (sha256 `9461a059…`).
3. Real-children leg: `quality/counters/c1-r70-real-children.py` (sha256 `b3a6f131…`),
   `build_fixture` `:213`, `LANE_TEMPLATE` `:79`, declared limits `:46-50`. Receipt
   `.ufo/waves/round-70/measurement-r70.txt` § C1 now at rev `6a25e865` (candidate
   `mz=pass|fail|fail`, base `mz=pass|pass|pass`, `cases=3 correct=3 base_correct=1`, rc 0); the
   same values were measured at `5adba5a9`. Pre-freeze control
   `.ufo/waves/round-70/control-baseline-r70.txt:40-51` shows `base_correct=1/3`.
4. Fetches this seat: rendered page 3×, byte-identical sha256 `c8a66b3a…`, 207155 B, 2032 lines,
   `<title>… Python 3.14.10 documentation`; sentences at `subprocess.html:362-363` and `:364-365`.
   Bash release tarball `https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz` sha256 `0d5cd869…` (matches
   S435's recorded tarball digest); `doc/bashref.texi` sha256 `f3d37d57…`, 415804 B, 11553 lines;
   quotes verified at `:3905-3909` (zero vs non-zero, "a variety of ways"), `:3911-3912`
   (`128+N`), `:3914-3916` (`127`/`126`). The registry anchor's `:3902-3906` covers the
   zero/nonzero sentence's first two lines, not its trailing clause at `:3907-3909`.
5. **Anchor-cover, measured.** Draft against a scratch registry copy carrying the landed S441 row:
   `ANCHOR_COVER` K01 `subprocess.html:362` OK, K02 `subprocess.html:364` OK, `CHECK107 rows=2
   covered=2 miss=0 verdict=OK`, rc 0. Negative controls: a raw-RST pin `subprocess.rst:136`
   MISSes (`locators=360-366` do not cover 136); a S435 pin `Exit-Status.html:3902` MISSes with
   `name=Exit-Status.html locators=none reason=no-cover` because the anchor cell carries
   `bashref.texi:` locators while the check derives the name from the row's URL.
6. **Finding for the L1 (not edited by this seat).** The uncommitted production entry
   `corpus/knowledge/landing-kill-credit-real-children-r70.md` (111 lines, sha256
   `95421540103591223dc503a2d2ac22bc96ca3e15f254810612750b938977db41`) pins K01 to S435 as
   `Exit-Status.html:3902` and scores `rows=3 covered=2 miss=1 verdict=FAIL`, rc 1 (K02/K03 on
   S441 pass). Clearing it needs K01 re-pinned to `subprocess.html:362` or S435's anchor widened
   in place to carry `Exit-Status.html:…`. My draft avoids the S435 row entirely and keeps that
   row's facts in prose.
7. The fixture lane template equals `.ufo/waves/round-70/proto/fixture-lane.tmpl` (sha256
   `9e31681d…`) up to the mode token (`@MODE@` vs `__MODE__`); verified by import+diff,
   `identical: True`.

## Commands run and exit codes

| command | result |
|---|---|
| `curl -sSfL -o subprocess.{1,2,3}.html https://docs.python.org/3.14/library/subprocess.html` (scratch) | rc 0; all three sha256 `c8a66b3a…`; 207155 B; 2032 lines |
| `curl -sSfL -o bash-5.3.tar.gz https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz` + `tar -xzf … doc/bashref.texi` (scratch) | rc 0; tarball sha256 `0d5cd869…`; texi sha256 `f3d37d57…`, 415804 B, 11553 lines |
| `python3 -I quality/check-anchor-cover.py --repo <scratch> --rev HEAD --entry corpus/knowledge/draft.md` | rc 0; `rows=2 covered=2 miss=0 verdict=OK` |
| same check, `--entry corpus/knowledge/prod.md` (copy of production entry) | rc 1; K01 S435 MISS; `rows=3 covered=2 miss=1 verdict=FAIL` |
| template identity check (import `LANE_TEMPLATE`, substitute mode token, diff proto) | `identical: True` |
| `git -C <lane> cat-file -p HEAD:quality/counters/…` (read-only) | r69 `9461a059…`; r70 harness `71a7b6c4…`; real-children `b3a6f131…` |
| `wc -l -c` + `sha256sum` on the draft | 245 lines, 15955 bytes, `80b360bc…` |
| `test -e /fast/scratch/hyaku/mado-r70/R70ScribeEntryC1` | `SCRATCH_ABSENT` (removed) |

All fixture git repos were created only under the scratch dir, `git init` toplevel asserted equal
to the fixture dir, commits made with explicit `-c user.name/-c user.email/-c commit.gpgsign=false`,
every git call `-C`-named, and the scratch tree deleted. No tool installs were needed. No desktop,
compositor, service, socket or package manager was touched. No credentials in any artifact.

## Out of scope / not claimed

- No production write, no lane commit/stage/reset/checkout, no fleet-repo write, no sibling-lane
  write. The production entry and `corpus/lessons/round-70.md` were read only.
- No measurement rerun: `correct=3 base_correct=1` and the per-mode `mz=` values are receipt values.
- The entry does not claim fault coverage, that three scenarios exhaust the kill-credit hazards,
  that the fixture is the real landing instrument, or anything about desktop/session/package
  state. The "line-count heuristic also scores 3/3" sentence is marked as derived, not measured.
- Row adoption and the S441 anchor remain the L1's. The production-entry K01 defect in finding 6
  is reported, not fixed.

Report path: `.ufo/waves/round-70/w1/R70ScribeEntryC1.md`.
