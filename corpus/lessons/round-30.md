author: mado

# Round 30 — index-gap closure, criterion-grounding repair, index gate

Base: lane tip `8f51071b5bc44c815eeb5da76bb7f1947994ffb8` (round-29 closure:
admitted; C1/C2 TARGET_MET, the inherited 41/43 navigation gap routed here as
the round's first claim).

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M30-1 | attribution | `corpus/QUALITY.md` criteria 1–5 carry no lesson citation; 18, 19 and 32 cite a lesson only outside the numbered line; 38–40 cite bare `M28-x` ids with no path — the literal rubric (`grep -cE '^[0-9]+\. .*lessons/'`) reads 28/40 at base and the resolved-active rubric (`.ufo/waves/round-30/c2/count.py`) reads 31/39. The seed block's true ground is `MINT.md`, never recorded. | `none` — criterion 22 audits rubric *selection*, but nothing required each criterion's own citation to resolve. | Rows 41–51 supersede the ungrounded criteria verbatim with canonical `(lesson: lessons/<file>#<anchor> <id>)` citations (1–5 grounded on `MINT.md` + this row); the fix is shown able to fail: the C2 counter at base prints `UNRESOLVED criterion 1..5, 38..40` and `TARGET_MISSED` exit 1 (control `controls/C2K1-donothing.txt`). |
| M30-2 | scope | The round-29 sweep row (`corpus/lessons/round-29.md` `## Mistakes`, M29-sweep) records the navigation counter at 41/43 at base and tip alike — `mutation-testing-r28.md` and `workspace-rules-r27.md` absent from `corpus/README.md` index rows since rounds 27/28 — and correctly routed it instead of repairing under the table. The mistake is the gap itself: two admitted notes unreachable from the coverage map for two full rounds, through two closures that re-ran the census but never the navigation counter. | `none` — the navigation counter is a fence (harm watch), not a gate; no criterion made index completeness a claim input. Criterion 52 captures the record-then-claim discipline. | Repaired as declared claim C1 this round (the two index rows land; counter 43/43 exit 0, receipt `evidence/c1-after-*.txt`) and made repeatable by C3's `quality/check-index.py` gate (red at base, green at tip). |

## Gate

S185 was opened this round on 2026-10-24: the frozen navigation counting
command embedded in `SCORECARD.md` (own-work source, the fence that caught the
routed gap and the spec the C3 gate implements).

| id | source path | URL | access date | located quote (≤25 words, verbatim) |
|---|---|---|---|---|
| S185 | `SCORECARD.md` "Fleet round 1 — coverage navigation" counting-command fence | `SCORECARD.md` (own-work; sha256 of the block `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`) | 2026-10-24 | `revision=$rev indexed=$covered/$total missing=$missing dangling=$dangling duplicates=$duplicates coverage=$score/10` |

**Decision:** admitted as `own-work` tier A scoped to index-completeness
semantics. The row grounds claim C3 (`quality/check-index.py` implements the
fence's row-set semantics) and is cited by C1's registration; it makes no
claim about note truth or freshness. The `used-by` paths
(`quality/check-index.py`, `.ufo/waves/round-30/registration.md`) exist at the
round's final commit.

**Registry changes this round:** rows 184 → 185 (+S185, opened 2026-10-24,
status `mined`). No status/recheck flips on existing rows; no new rejection
considered (S062 remains the standing reject sample). The seven W04
duplicate-URL warnings (S030/S042/S045/S097/S119/S120/S121) were re-checked
against criterion 17: each pair is supersession or distinct-scope reuse with
the rejected history preserved (S030→S045 rejected-duplicate, S042 supersedes
S006 in a disjoint scope, S119 supersedes S113's scope, S120/S121 pin
different sections of one file, S097 supersedes S094). No action; the
warnings stand as intended collision-review markers.

## Notes

**C1:** the two rows are navigation only — they assert each note exists and
what it holds, quoted from the notes' own headers; they admit no new domain
claim. The do-nothing control is the frozen counter itself at base
(`indexed=41/43`, exit 1).

**C2:** superseded lines leave both fractions' denominators (criterion 21's
supersedes-20 precedent); literal and resolved metrics are reported side by
side per criterion 22 — literal 28/40 → 40/52, resolved-active 31/39 → 40/40.

**C3:** the capability is the gate, not the green verdict: it must print
`indexed=41/43` exit 1 at base and `indexed=43/43` exit 0 at tip, and its
`--selftest` (6/6) covers missing/dangling/duplicate/symlink-refused/empty.

## w1 addendum — dispatched-wave findings (post-report, append-only)

The orchestrator dispatched `w1-spec.json` between rounds; 24 seat reports
land under `.ufo/waves/round-30/w1/reports/`. Two are mine to act on now:

| finding | pointer | disposition |
|---|---|---|
| C3 gate was a strict superset of the fence (`ROW_RE ^\|\s*` vs `^\| `, `split()` vs `splitlines()`, non-ASCII ls-tree quoting, `--root` 0/0 false-green, silent `master` default) — all latent on committed bytes (43/43 both ways, all receipts reproduce) | `w1/reports/RevC1Fence.md` S1–S6; `MutC3Gate.md` F1/F1b/M1/M3a; `RevC3Gate.md` H1 | **Repaired same-round** (gate blob rewritten; fence-literal `^\| `, `-z` NUL ls-tree blob-only, empty/missing knowledge → `SETUP_ERROR` exit 2, `--rev`/`--root` required; selftest 6 → 8 cases incl. fence-literal row forms + note-symlink refusal). Receipt `evidence/c3-repair-d72243e.txt`: base red, both tips green, `8/8`. Predicates unchanged; `PRED-C3-r30` re-verified at `d72243e`. |
| Kill rules are bypassable by cheapest cheats (C1 rows outside the table / garbage cells; C2 an empty lesson file + supersedes-all row; C3 hash-keyed echo gate); fence/gate both ignore table context | `w1/reports/CritKillRules.md`; `CritPredicates.md` A1–A4; `RevC1Fence.md` S6 | **Routed to round 31** — tightening the frozen instruments mid-closure would invalidate the registered predicates; recorded honestly. |
| C2 resolves citations only (file exists + anchor word + M-id present); a criterion citing an empty lesson file "resolves" — grounding quality is outside the rubric | `CritKillRules.md` K2 | Routed to round 31 (counter v2). |
| `S185` own-work chain valid (bytes predate round, content-pinned anchor) but own-work sourcing has no anti-circularity guard; 3 formality defects | `w1/reports/CritSourcedClaim.md` | Routed to round 31. |
| q36 receipts regenerated out-of-scope mid-review (ephemeral paths only, no verdict moved) — same class as r29's regeneration | seat observation | Reverted to committed bytes; identical to r29 handling. |
| Gate not wired into `tools/mado-verify.sh --selftest`; SKILL gate-registry row owed | `RevC1Fence.md` S7 + r30 spot-check routing | Routed to round 31. |
| `K2` literal < 0.70 floor holds vacuous ground forever | `CritKillRules.md` | Routed (counter v2 raises the floor with the active rubric). |

The remaining reports (executor re-runs, scribe audits, scout recon,
connector overlap, trend-verdict attacks, records chain) are the
non-author verification wave's evidence; none reported a live defect in
the three claims' measured outcomes.

### w1 addendum part 2 — counter + record repairs (same-day, append-only)

| finding | pointer | disposition |
|---|---|---|
| `check-index.py` `%(path)` still C-quoted under `-z` (non-ASCII note dropped) | `w1/reports/RevC1Fence.md` post-review addendum | **Repaired**: `git -c core.quotepath=off ls-tree -z`; selftest case 9 pins non-ASCII + space names via a real git fixture. Selftest now `9/9`. |
| `count.py` `M<a>-M<b>` ranges parsed as endpoint singles (`M01-M07` → {M1,M7}); `M<a>-<b>` a<=b widened compounds to ranges; `SUPER_RE` dropped ranges after the first member; no "later line" ordering; `active=0` passed | `w1/reports/RevC2Counter.md` S3–S6 | **Repaired** (implementation restored to the frozen rubric's grammar): `M<a>-M<b>` ranges, `M<a>-<b>` compounds always literal, multi-range lists complete, position-guarded supersession, `act_n>0` required. **Byte-identical output** at `8f51071b`, `446dc396`, `d72243e`, `15ddd7d` — all registered verdicts reproduce. |
| freeze-smoke receipt's C2 leg truncated (5 lines of 14; criterion 49 needs full output) | `w1/reports/RevRecordsChain.md` F1; `ScribeRecords.md` D1 | **Repaired**: `evidence/freeze-smoke-451e8b3c-full.txt` carries all 14 C2 lines + EXIT; the truncated receipt is kept with this erratum. |
| row 48 lost criterion 32's normative accounting sentence ("no retroactive pass … no numeric C2 credit") — "verbatim" overclaim | `w1/reports/RevRecordsChain.md` F2; `ScribeRecords.md` D2 | **Repaired**: sentence restored to row 48 (append-only correction to its text). |
| seed-five grounding resolves through M30-1 — the audit row recording their own defect; counter anchor/id checks are independent whole-file substrings | `w1/reports/RevRecordsChain.md` F3; `RevC2Counter.md` S7 | Recorded as the rubric's stated limit (resolvability ≠ derivation); anchor-scoped section matching routed to round 31 counter v2. |
| registration.md:61 off-by-one ("12 lines superseded by rows 41–51"; line 20 belongs to row 21); harm-watch head labelled `446dc396` but measured at `d72243e`; bare `controls/` path unresolvable at repo root | `w1/reports/ScribeRecords.md` D3–D5 | D3/D5: erratum entries below (frozen file can't be edited; path disambiguated). D4: **committed receipt** `evidence/selftest-d72243e.txt` (`MADO_SELFTEST: 460/460`, EXIT=0). |

Remaining latent counter items routed to round 31 (counter v2 alongside the
fence/table-context tighten): anchor+id conjunction scoped to the cited
section; `M` vs `m` id casing; compound `M<a>-<b>-<c>` spellings documented
as literal.
