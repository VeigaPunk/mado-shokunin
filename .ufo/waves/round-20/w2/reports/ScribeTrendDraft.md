# ScribeTrendDraft — partly falsified: the round-20 counters reproduce, but the expansion entry fails its own citation bar (json.dumps) and round 20 has no discernment spot-check on record

Draft trend verdicts: `.ufo/waves/round-20/w2/ScribeTrendDraft/trends.md`.
Revision `a4046a8216080d4004de3f268c62cf142095ac07`; baseline `1f7f995`; pre-harm `9c54c56`. Governing protocol: `kimi-shokunin/skills/shokunin/protocol/LEARNING.md` (present).

## Verdicts (draft)

| Trend | Verdict | Basis |
|---|---|---|
| expansion | harmed (one clause) | +1 entry (34→35), +14 mined sources (98→112), +2 capabilities, 0 frontier. `corpus/knowledge/tripwire-precision-r20.md:20` cites `json.dumps` to S106/S107; neither body contains it (`grep -c dumps` = 0). Criterion 2 failure. |
| quality | unchanged (knowledge layer) | No existing knowledge entry re-verified or superseded in round 20 (`git diff --stat 1f7f995 a4046a8 -- corpus/knowledge` → one file). |
| discernment | unprovable-but-better | Round-19 disagreement → criteria 29/30′ with lessons and red/green checks. No non-author agree/disagree line in `corpus/lessons/round-20.md`; 5 rejected candidates not curated in `SOURCES.md` (`grep` → 0 hits). |

## Findings with evidence

1. **Counters reproduce at `a4046a8`** (clone `/tmp/mado-r20w2-ScribeTrendDraft`, origin removed):
   - `tw-precision.py` → 172/175, P 66/66, score 9.8286; `1f7f995` → 29/175 (1.6571); `9c54c56` → 110/175 (6.2857, P 66/66).
   - `tw-recall.py` 6/6; `tw-recall-split.py` observed 5, lead 1, control findings 0.
   - `tally-check.py --set red --rev a4046a8…` → 5/5, exit 1; `--set green --rev a4046a8…` → 4/4, exit 0.
   - `measure.py` → c1 22/30 = 7.3333; c2 6 covered = 10.0.
   - `tools/mado-tripwire.py` sha256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` (unchanged since `28c6837`).
2. **Counter-check that differs from the lesson:** the bare `tally-check.py tally-claims.json` (no `--rev`) exits **2** with 4 ERROR lines ("entry reads at REV; pass --rev"). The lesson's "exit 1" describes the red-only run. Not a claim failure; a usage note for the lesson.
3. **Expansion defect:** `corpus/knowledge/tripwire-precision-r20.md:20` — `json.dumps` in the pure-stdlib list, cited "(S106, S107; …)". Re-fetched S106 (`collections.rst`), S107 (`shlex.rst`), S108 (`subprocess.rst`): `dumps` count 0 in each. Same name at `tools/mado-tripwire.py:1413`.
4. **Re-verified sources (6 fetches, all 200):** S111 (`executionmodel.rst:141-142`, `:163-165`), S105 (`functions.rst:868-869`), S106 (`collections.rst:461-462`), S107 (`shlex.rst:39`), S108 (`subprocess.rst:43`), S110 (`bashref.texi:4801-4802`). Quoted sentences found; markup and line-wraps differ. Not fetched: S099–S104, S109, S112.
5. **Gate shape:** all 14 rowed round-20 candidates are `admit`. Rejected candidates (`simple_stmts.rst`, `functools.rst`, `dataclasses.rst`, `compound_stmts.rst`, jj v0.38.0) appear only in `corpus/lessons/round-20.md` Gate prose; `SOURCES.md` has 0 rows for them (QUALITY criterion 5; LEARNING curation rule).
6. **Discernment record missing:** `corpus/lessons/round-20.md` has no agree/disagree line; LEARNING requires one admit and one reject spot-checked from outside.
7. **Criterion labelling:** `corpus/QUALITY.md:249` labels the new criterion `30` (no prime, no replacement note); `SCORECARD.md:1287-1309` registers 30 withdrawn and 30′ as its replacement.
8. **Criterion 29 red shape reproduces the incident:** `.ufo/waves/round-20/evidence/inns-r19-shape.sh:52` (`[ -e "$p" ] && mount --bind … && echo`) vs the round-19 incident `[ -e ] && mount && echo`. `[INFERENCE]` The harness uses `--map-root-user` where the incident used `--map-current-user`: a shape match, not identity.
9. **Stale round-19 numbers unmarked in place:** `corpus/lessons/round-19.md:124` ("155 transcripts"), `SCORECARD.md:1167`, `LOG.md:1324` ("5/13 name S096"), `SCORECARD.md:1225` ("ten old OM10"). Corrections exist append-only in `round-20.md:58-79` and `QUALITY.md:261-271`; `tally-check` is documented not to flag stale sentences beside a correction.
10. **Instrument mismatch on the new entry:** `measure.py:200-211` marks `corpus/knowledge/tripwire-precision-r20.md` `MALFORMED` (its `surface:` line must be `P<n>`; the entry says `surface: lane tooling …`). No score changes; L1 decision.

## Fetch receipts

`.ufo/waves/round-20/w2/ScribeTrendDraft/fetch/receipts.jsonl` (6 lines, schema `mado-fetch-receipt-v1`), bodies in `…/ScribeTrendDraft/fetch/`:

| Body | HTTP | Bytes | sha256 |
|---|---|---|---|
| S111-executionmodel.rst | 200 | 24445 | `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89` |
| S105-builtins-functions.rst | 200 | 97140 | `f1b72170e6893ee6315108f74244df56a9725f2be2b8bf396f22cd6dcbd5d9de` |
| S106-collections.rst | 200 | 54628 | `be2f90d14d3f488a9d5a6f23423e494a46b10a030d83d9308fd71af1f8eed7a7` |
| S107-shlex.rst | 200 | 17867 | `819c6e6fab583c8d30e32950591ed1fda2b552cebcbfadc5d1619e3e35ea03b0` |
| S108-subprocess.rst | 200 | 61603 | `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd` |
| S110-bashref.texi | 200 | 415804 | `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5` |

Tool: `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5`.

## Limits

- Draft only: these are trend verdicts for the round report, not its spot-check.
- Six of 14 new SOURCES rows re-fetched; S099–S104, S109, S112 not checked by this seat `[UNK]`.
- The C1/C2 counters are re-run, not re-authored; 30′ shares C1's counter (not independent).
- The whole-corpus no-harm diff vs `9c54c56` is another item's work; not computed here.
- No live-host command, no pacman/sudo/systemctl/hyprctl; the live gate was not run. Host pause respected.
- `isolation-check.sh` not run (not named by this item).

## Installs

none
