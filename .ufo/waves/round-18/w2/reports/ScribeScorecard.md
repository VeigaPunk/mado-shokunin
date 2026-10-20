# ScribeScorecard — report (round 18, wave 2)

Scope: draft `.ufo/waves/round-18/drafts/ScribeScorecard.md` (the round-18 results
section for `SCORECARD.md`; `SCORECARD.md` itself was not edited). Read-only
except for those two files. No package-manager, service, compositor, input,
screenshot or REA/browser command was run; no `tools/*` was executed by this
scribe (all tool outputs cited are the committed receipts).

## Commands and files read (all read-only)

- `tail` of `SCORECARD.md` (round-17 results section, round-18 declared claims);
  `corpus/lessons/round-18.md` (`## Mistakes` M1-M6, `## Gate`).
- `evidence/measure-before.json.txt`, `measure-after.json.txt`,
  `measure-before.json`, `measure-mutants.json` (summary: 6 mutants, 6 bites,
  `no_bite []`, `baselines_agree true`).
- `evidence/tripwire-frozen-before.txt` (exit 2 usage), `tripwire-frozen-match.txt`
  (exit 0 `frozen_match`), `tripwire-frozen-tampered.txt` (exit 2 `snapshot_tampered`),
  `harm-tripwire-round-18-frozen.txt` (`SELFTEST_SUMMARY: 17/17`).
- `evidence/harm-watch-summary.txt` (`HARM_WATCH: PASS`, rev 4c103b55, commands=10),
  `harm-gate-selftest.txt` (389/389), `harm-action-plan-selftest.txt` (52/52),
  `harm-tripwire-round-17-{core,compound,hardening,w2-regressions}.txt`
  (9/9, 16/16, 33/33, 30/30), `harm-measure-u.txt` (U score 10.0),
  `harm-nav-fleet-round-1.txt` (34/34), `harm-census-validate.txt` (exit 0, three W04),
  `harm-watch-pins.txt`.
- `SKILL.md` registry rows `mado-tripwire` (probe) and `mado-tripwire-frozen` (gate).
- `corpus/SOURCES.md` rows S070-S095 (URL, digest) cross-checked against
  `fetch/*/receipts.jsonl` (python, read-only): for every credited URL in S072-S089
  and S092-S094 there are at least two HTTP-200 receipt lines whose sha256 matches
  the row's digest prefix. S090, S091 and S095 are host rows; S091's `/usr/bin/walker`
  digest (`2524065068…`) and two S095 host digests are not in receipts, as expected
  for host file bytes.
- `drafts/` listing (three `.patch` files and `drafts/tripwire/r18-*` fixtures);
  `JjAuditMado.md` F6 lines 190, 348-349 (read-only, for the planned item).

## Findings

1. **C1, C2, C3 are supported by their committed receipts** as stated in the
   round-18 declaration (18/26 = 6.9231; 6/6 = 10.0; frozen match 0, tamper 2,
   baseline usage 2, selftest 17/17). The numbers in the draft match the receipts
   byte-for-byte.
2. **Receipt directories are incomplete.** 15 fetch directories hold no
   `receipts.jsonl`: `ReopenS075`, `ReopenS076`, `ReopenS077`, `ReopenS078`,
   `ReopenS079`, `ReopenS082`, `ReopenS084`, `ReopenS085`, `ReopenS086`,
   `ReopenS087`, `ReopenS088`, `ReopenS089`, `ReopenS093`, `ReopenS094`,
   `MadoR18.RevengeTarballRepro`. The shell listing also reported
   `failed to redirect … receipts.jsonl: No such file` for these. The wave-2
   "re-open" receipts therefore exist only for S072, S073, S074, S080, S081, S083 and
   S092. The draft states this limit; the credited rows are still backed by at
   least two other seats' 200 receipts (checked above). Not a blocker for C2, but
   the scorecard must not claim a per-seat re-open receipt for every row.
3. **HTTP 404 receipts are committed but not credited.** Five 404 lines: raw
   `swaywm/swaybg/v1.2.2/doc/swaybg.1.scd` (14 B body), `swaywm/swaybg/tree/v1.2.2/doc`,
   `basecamp/omarchy/v3.8.4/themes/matte-black/theme.name`,
   `adrg/xdg/v0.5.3/files.go`, `wiki.archlinux.org/…Walker&action=raw` (0 B). None
   equals an S-row URL. The 404 bodies are not evidence for any row; the draft says so.
4. **Shell/python inconsistency for one directory.** The persistent shell reported
   `error: failed to redirect … ReopenS081//receipts.jsonl` while python sees
   `fetch/MadoR18.ReopenS081/receipts.jsonl` (1272 B, S081 digest `2b4a6f1493…`
   matching the row). Interpreted as: the receipt lives under the `MadoR18.`
   prefix; the bare `ReopenS081` name does not exist. Not resolved further (no
   re-run to decorate).
5. **C3 scope.** The frozen replay pins five committed input files (rounds 13-15).
   It is a gate for regressions of those exact lines; it does not measure new
   misses. The draft words it as capability, not detection.
6. **Freshness is not measured this round.** The draft says so; the walker
   2.17.2 and hyprland 0.56.2-4 re-anchor is planned work (round 19 item 2).
7. **Harm watch numbers changed where expected.** Gate selftest 372/372 → 389/389
   (F10/F14 fix, tool sha `c9fb0cef…`); navigation reported 34/34 here (round 17
   reported 32/32 on a different revision). The draft reports the observed values.

## Tool installs and updates

None. No package manager, no `uv tool`, no release binary was installed or updated
by this scribe (host pause in force).

## Out of scope (not done, not claimed)

- No edit to `SCORECARD.md`, `corpus/`, `tools/`, `drafts/` other than the one
  assigned draft, or any receipt file.
- No re-run of `measure.py`, `mado-tripwire.py`, `mado-verify.sh` or `fetch-verify.py`
  (receipts are cited instead, per the round's do-not-rerun rule).
- R15-V1 remains operator-owned (host state `[UNK]`).

## Checks for the main agent

- Confirm that the 15 receipt-less fetch directories are intended (wave-2 reopen
  seats that wrote nothing) before the scorecard is committed.
- Decide whether the draft's "at least two seats" wording is acceptable as the
  per-row corroboration standard for C2.

## Artifact paths

- Draft: `.ufo/waves/round-18/drafts/ScribeScorecard.md`
- Report: `.ufo/waves/round-18/w2/reports/ScribeScorecard.md`
