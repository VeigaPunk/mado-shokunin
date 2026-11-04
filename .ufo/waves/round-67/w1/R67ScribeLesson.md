# R67ScribeLesson — seat report

status: lesson draft written; no lane file outside the seat directory touched; no commits.

## Deliverable

- Draft: `.ufo/waves/round-67/w1/R67ScribeLesson/draft/corpus/lessons/round-67.md`
- sha256 `706270240a879f3aa74b6bcf9ec06163edead378924c3154e66fb79bb84187d5`, 175 lines, 14081 B.
- Sections: header (author/date/base/frozen declaration 061dc329), Outcome and boundaries,
  Mistakes (M67-1 stale-premise, M67-2 landing), Gate, Frontier and scope, Controls and limits,
  Integration placeholders (`TBD-INTEGRATION` only for L1 landing measurements).

## Findings

1. **M67-1 (stale-premise).** r66's frozen marker literal was remembered, not quoted:
   `corpus/lessons/round-66-verifier-spotcheck.md:32-37`; erratum
   `.ufo/waves/round-66/marker-premise-erratum.md`; the child emits `LEDGER:`
   (`quality/check-tool-ledger.py:350,368`) and `MADO_TOOL_LEDGER` occurs 0 times at `0b28ffb4`.
   Capture criterion: QUALITY 108 (`corpus/QUALITY.md:622-636`). The r67 rule actually applied:
   the M-Z mutant literal `[ "$citations" -gt 0 ] && ` is byte-present at
   `quality/landing-counters.sh:73` @ `0b28ffb4`.
2. **M67-2 (landing).** r66 guarded replacement refs only at the parent export
   (`quality/landing-counters.sh:8`) while both children build their own git env:
   `quality/check-tool-ledger.py:79,101-110` (whitelist `PATH`/`SYSTEMROOT` + fixed keys) and
   `quality/counters/c3-r56-used-by.py:59-70`; neither carries `GIT_NO_REPLACE_OBJECTS`.
   Baseline receipt `.ufo/waves/round-67/control-baseline-r67.txt:18-19`:
   `usedby_guard=0 ledger_guard=0`, `child_env_read=forged guarded_read=real`. Capture
   criterion: QUALITY 72 (`corpus/QUALITY.md:391`), one-site patch over a two-site property.
3. **Gate S436.** Facts cross-checked against the two sibling seats: canonical URL
   `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc`,
   sha256 `3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631` (5398 B),
   access 2026-11-03; quote DESCRIPTION lines 34-36 (21 words); guard sentence lines 55-56
   (16 words); tag `v2.56.0` object `2478544319491bbd2a42cc57a83e3d2f4730a280` peeling to
   `a018953688f1b10bddf91bff8747068f5f4746a4`; host `git version 2.56.0`. Same-tag
   `git.adoc` sha256 `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79`
   (quote lines 927-929, 18 words). URL absent from SOURCES (0 hits), S436 absent (0 hits),
   all 372 existing rows 11 columns. Reject recorded: `core.useReplaceRefs` config plane
   (cannot bind the process-level env guard), flip stated; plus a rejected over-claim.
   Delivered row file `R67ScribeKnowledge/draft/corpus/SOURCES-row.txt` sha256
   `b6e794cc19648d98f9d3f4d35e8dff3882a1856ae33fb3d07335207f6d2adbde` (983 B, one line,
   11 cells, no escaped pipe, quote present). Its anchor has no `pin` path, so QUALITY 107
   reads `eof=unchecked`; line numbers hand-checked against the fetched bytes (scribe's
   scratch `check-anchor-cover.py`: rows=8 covered=8 miss=0). Entry draft
   `R67ScribeKnowledge/draft/corpus/knowledge/replace-ref-citation-boundaries-r67.md`
   sha256 `a049be86119683dc086b608dcd04ddbe4d21c9310cf19032ec13db6e11736f34`, Scope section
   disclaims desktop/PROVINCE-truth/authenticity claims.
4. **Census/frontier.** `.ufo/waves/round-67/census-start-r67.txt` (exit 0) committed at
   `aa7fe5a1caffe25322cd76ed44b10636cc69f32b`; final line `mado	ok	…/corpus/SOURCES.md`;
   372 rows at base/freeze; ids S001–S435 with 5 gaps. End count is L1-only.
5. **r65 live receipt pin verified independently.** sha256
   `676ba88b484e194d4962ee27d07a54b5b7441a8461256b0f3ea0c83d1910e8ed`; blob
   `88cd0232780239dc4a75b48a2b3df6f36dd998f1` identical at `0b28ffb4` and `061dc329`;
   CLEAN line 65, `rc=0` line 66. No existing SOURCES cell change this round.
6. **Pending drafts at read time.** `R67ExecChildren/draft/{quality/check-tool-ledger.py,
   quality/counters/c3-r56-used-by.py}` were byte-identical to base (no guard line yet);
   `R67ExecLanding/draft/quality/landing-counters.sh` (280 lines) already carried the M-Z clause
   and the zero-citation selftest. The lesson therefore does not assert the pending
   `GIT_NO_REPLACE_OBJECTS` child line as landed.
7. No knowledge entry claims desktop coverage; no assimilation is named in this draft.

## Commands and outcomes (lane root /home/vgpnk/Projects/shokunin/mado-shokunin)

```sh
git log --oneline -6                                  # rc0; aa7fe5a1, 061dc329, 0b28ffb4 seen
git diff --stat 0b28ffb4 061dc329                     # rc0; freeze adds claims file only
grep -c '^| *S[0-9]' corpus/SOURCES.md                # 372
awk -F'|' '/^\| S[0-9]+ /{print NF-2}' corpus/SOURCES.md | sort | uniq -c   # 372 x 11
git show 0b28ffb4:quality/check-tool-ledger.py | grep -c MADO_TOOL_LEDGER # 0 (pipe rc1)
git show 0b28ffb4:quality/check-tool-ledger.py | grep -n 'LEDGER:'       # 350,368 (+doc lines)
git show 0b28ffb4:quality/landing-counters.sh | sed -n '73p'             # exact M-Z clause
git show 061dc329:.ufo/waves/round-65/receipts/gate-live-r65.txt | sha256sum  # 676ba88b…
git rev-parse 0b28ffb4:.ufo/…/gate-live-r65.txt 061dc329:.ufo/…/gate-live-r65.txt # 88cd0232 both
curl -sS https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc # rc0
sha256sum git-replace.adoc                            # 3f61be3f… (5398 B)
curl -sS https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc        # rc0
sha256sum git.adoc                                    # 050c5330… (47005 B)
git ls-remote https://github.com/git/git 'v2.56.0*'   # tag 24785443…, peel a0189536…
git --version                                         # git version 2.56.0
grep -c '^| S436 ' corpus/SOURCES.md                  # 0, rc1
grep -c '<canonical-url>' corpus/SOURCES.md           # 0, rc1
awk -F'|' '{print "cells="NF-2}' .ufo/waves/round-67/w1/R67ScribeKnowledge/draft/corpus/SOURCES-row.txt  # cells=11
grep -c '\\|' .ufo/waves/round-67/w1/R67ScribeKnowledge/draft/corpus/SOURCES-row.txt  # 0, rc1
sha256sum .ufo/waves/round-67/w1/R67ScribeKnowledge/draft/corpus/SOURCES-row.txt  # b6e794cc…
sha256sum .ufo/waves/round-67/w1/R67ScribeKnowledge/draft/corpus/knowledge/replace-ref-citation-boundaries-r67.md # a049be86…
```

## Limits

- No committed-revision measurement: C1/C2 target lines, final instrument/child/diff sha256,
  wave settlement, end census/count, S436 row bytes and register groups are `TBD-INTEGRATION`.
- "An empty mutant diff is refused" is not verified; the draft states only that the receipt
  prints the diff and sha256.
- S436's anchor names no `pin` path (the adoc is not in the lane tree), so QUALITY 107's
  EOF/length check reads `eof=unchecked`; line refs were hand-checked against the fetched
  bytes. Disclosed in the lesson Gate, not presented as an admitted EOF check.
- Tooling: none installed; pacman untouched. Scratch `/fast/scratch/hyaku/mado-r67/R67ScribeLesson/`
  removed before yield; no `/tmp` or `/var/tmp` writes.
