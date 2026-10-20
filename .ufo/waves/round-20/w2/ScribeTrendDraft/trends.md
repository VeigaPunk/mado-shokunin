# Round 20 — trend verdicts (draft, ScribeTrendDraft)

Basis: `kimi-shokunin/skills/shokunin/protocol/LEARNING.md` (present; governs over `MISSION.md`).
Revision under review: `a4046a8216080d4004de3f268c62cf142095ac07`. Round baseline: `1f7f995` (round-19 closure,
rejected-harmed). Pre-harm baseline: `9c54c56`. Verdict vocabulary: `improved`, `harmed`, `unchanged`,
`unprovable-but-better`. Every verdict below is a draft for the round report; the round's spot-check is not
this draft.

## Verdicts

| Trend | Draft verdict | One-line basis |
|---|---|---|
| expansion | **harmed** (one clause; the count improved) | +1 admitted entry on uncovered tooling ground, +14 mined sources, +2 capabilities, 0 frontier areas. The one entry fails its own admission bar (criterion 2) on one citation: `json.dumps`. Repair is one line; this is a defect, not a trade. |
| quality | **unchanged** (knowledge layer) | No pre-existing `corpus/knowledge/` entry was re-verified or superseded in round 20. The only knowledge file touched is the new entry. The tally, instrument and precision gains are recorded below as evidence, not counted as entry quality. |
| discernment | **unprovable-but-better** | Round 19's outside disagreement became criteria 29 and 30′, each with a lesson and a red/green check. Round 20's own gate has no non-author agree/disagree record, and its rejections are not curated in SOURCES.md. |

Flip conditions: expansion becomes `improved` when `json.dumps` is re-cited to a fetched row or removed from the
entry (re-check: `grep -c dumps` over the cited bodies, see below). Quality becomes `improved` only if an existing
entry is re-verified or superseded in the round. Discernment becomes `improved` only when a named non-author records
`agree`/`disagree` on at least one admit and one reject (LEARNING §Discernment).

---

## 1. Expansion — harmed (one clause)

| Observable | Baseline `1f7f995` | Round `a4046a8` | Pointer / command |
|---|---|---|---|
| admitted `corpus/knowledge/` entries | 34 | 35 (+1) | `git ls-tree --name-only <rev> corpus/knowledge/ \| wc -l`; new file `corpus/knowledge/tripwire-precision-r20.md` (93 insertions) |
| SOURCES rows | 98 | 112 (+14, S099–S112) | `grep -c '^| S[0-9][0-9][0-9] '`; lesson `corpus/lessons/round-20.md:51-54` |
| coverage-map row for the new entry | none | `corpus/README.md:46` ("lane tooling, no surface") | `corpus/README.md:46` |
| frontier areas entered | — | 0 | `corpus/README.md:152-157` "Round 20 (repair; no province surface moved)" |
| new source hosts/kinds | 0 hits | CPython 3.14.8 docs, bash 5.3 manual, util-linux 2.42.4, man-pages 6.16, git v2.56.0 docs/source, jj v0.45.1 source | `grep -c -i 'cpython\|bash.git\|util-linux\|man-pages\|jj-vcs\|github.com/git/git' SOURCES.md` at `1f7f995` → `0` |
| capabilities admitted to SCORECARD | — | +2 rows (tripwire evidence marker; harness fail-closed check) | `SCORECARD.md:1342-1343` |

**Harm clause.** LEARNING: expansion is `harmed` when "an admitted entry fails the bar it was admitted under". The
bar (`corpus/QUALITY.md:4-5`, criterion 2) requires every claim to carry a source.

- `corpus/knowledge/tripwire-precision-r20.md:20` lists `json.dumps` among pure stdlib callables, cited as "(S106,
  S107; …)". S106 is `collections.rst` and S107 is `shlex.rst`. Neither body contains `dumps`. I re-fetched both
  (and S108 `subprocess.rst`): `grep -c dumps` → S106 `0`, S107 `0`, S108 `0`.
- The tool carries the same name: `tools/mado-tripwire.py:1413` (`"json.dumps", "pprint.pformat", ...`) at
  `a4046a8`. The tool is not the failing artifact; the entry's citation is.
- `[INFERENCE]` `json.dumps` is plausibly pure for a literal argument, but its `default=` hook can call user code.
  Whichever way it resolves, the entry must cite a row that says so, or drop the example.

**Counter-check (what would show the opposite).** If `json.dumps` were covered by an admitted row, the clause would
not fire. I checked every admitted row the entry cites that I could reach (S105–S108, S110, S111), and none covers
it. Only the rows I did not reach (S099–S104, S109, S112) remain unchecked by this seat.

## 2. Quality — unchanged (knowledge layer)

- **No existing knowledge entry changed in round 20.** `git diff --stat 1f7f995 a4046a8 -- corpus/knowledge` →
  `tripwire-precision-r20.md | 93 ++` only. The 11 other knowledge files that differ between `9c54c56` and
  `a4046a8` (for example `walker-deep-r9.md`, `arc-synthesis.md`) changed in round 19's commits (`b435568` and
  earlier), so I do not credit them to round 20.
- **Re-verification done this round, of the new entry's sources.** Re-fetched with `curl 8.23.0` (all HTTP 200;
  receipts in `.ufo/waves/round-20/w2/ScribeTrendDraft/fetch/receipts.jsonl`):

  | Row | Body sha256 (full) | Cited sentence found at |
  |---|---|---|
  | S111 `executionmodel.rst` | `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89` | `:141-142` "global namespace is searched first … builtins namespace is searched next" (line-wrapped); `:163-165` "A class definition is an executable statement" (supports note line 34) |
  | S105 `builtins/functions.rst` | `f1b72170e6893ee6315108f74244df56a9725f2be2b8bf396f22cd6dcbd5d9de` | `:868-869` "Return a new frozenset object, optionally with elements taken from iterable" (markup around names) |
  | S106 `collections.rst` | `be2f90d14d3f488a9d5a6f23423e494a46b10a030d83d9308fd71af1f8eed7a7` | `:461-462` "Returns a new deque object initialized left-to-right (using append) with data from iterable" |
  | S107 `shlex.rst` | `819c6e6fab583c8d30e32950591ed1fda2b552cebcbfadc5d1619e3e35ea03b0` | `:39` "Concatenate the tokens of the list split_command and return a string" |
  | S108 `subprocess.rst` | `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd` | `:43` "Run the command described by *args*" |
  | S110 `bashref.texi` | `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5` | `:4801-4802` "part of a command executed in a && or \|\| list except the command following the final && or \|\|" (texinfo `@code` markup) |

  Not re-fetched by this seat: S099–S104, S109, S112 `[UNK]`.
- **Tool pin still holds.** `git show a4046a8:tools/mado-tripwire.py | sha256sum` →
  `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`, the value in the new entry's `verified-at:`
  (line 2). The tool has not changed since `28c6837`.
- **Stale round-19 numbers left unmarked in place.** `corpus/lessons/round-19.md:124` ("155 round-19 transcripts"),
  `SCORECARD.md:1167` and `LOG.md:1324` ("5/13 name S096"), and `SCORECARD.md:1225` ("ten old OM10 assertions")
  carry no in-file pointer. The corrections live in `corpus/lessons/round-20.md:58-79`, `QUALITY.md:261-271`, and the
  round-20 SCORECARD section. `[INFERENCE]` Scope: these are lane records, not knowledge entries, so the quality
  clause ("found false or stale and left unmarked") is about entries. Recorded as a limit, not a harm.
- **Instrument mismatch.** `measure.py` (c2) reports the new entry under `rejected`: `MALFORMED`, because its
  `surface:` line must be `P<n>` (`.ufo/waves/round-17/measure.py:200-211`; the entry says `surface: lane tooling …`
  at line 4). No score moves (c2 stays 6 covered, 10.0), but the entry is off-schema for the knowledge index. L1's
  decision.

## 3. Discernment — unprovable-but-better

- **Outside spot-check of round 20: none recorded.** LEARNING requires a non-author `agree`/`disagree` with a
  reason, on at least one admit and one reject, in the round's lesson. `corpus/lessons/round-20.md` has no such
  line. `grep -n -i 'agree\|disagree\|spot' …round-20.md` matches only line 47 (S110 "five-way byte agreement").
- **Round-20 gate shape.** All 14 rowed candidates are `admit` (`round-20.md:36-49`; `SOURCES.md:111-124`). Five
  candidates are "Not rowed" (`round-20.md`, Gate, approx. lines 32-34): CPython `simple_stmts.rst`,
  `functools.rst`, `dataclasses.rst`, `compound_stmts.rst`, and the jj v0.38.0 files. `grep` of `SOURCES.md` at
  `a4046a8` for those names → **0 hits**. The reasons are kept in the lesson, but the rejections are not curated in
  `SOURCES.md`, which LEARNING and QUALITY criterion 5 require. A reject exists only in the lesson's prose.
- **Learned disagreement: closed, and grounded.** The round-19 outside closure (`corpus/lessons/round-19-verifier-spotcheck.md:63-81`,
  rejected-harmed) became M1 → criterion 30′ (`QUALITY.md:249-259`; `SCORECARD.md:1299-1309`), and M2 → criterion 29
  (`QUALITY.md:230-248`). Criterion 29's red file reproduces the incident shape:
  `.ufo/waves/round-20/evidence/inns-r19-shape.sh:52` `[ -e "$p" ] && mount --bind "$stub" "$p" && echo "armed $p"`,
  against the round-19 incident text `[ -e ] && mount && echo` (`SentinelGatePath` §Incident). `[INFERENCE]` It is a
  shape match, not a byte match: the incident used `--map-current-user`, the harness `--map-root-user`
  (`inns-r19-shape.sh:37`).
- **Naming defect.** `QUALITY.md:249` is labelled `30` with no prime and no note that it replaces the withdrawn
  registration. `SCORECARD.md:1287-1309` registers the withdrawn 30 and its replacement 30′. LEARNING requires a
  superseding row to name what it replaces. Fix: label 30′ and cite the withdrawn registration.
- **Independence limit (acknowledged).** 30′'s green reads the same counter as C1 (`SCORECARD.md:1306-1307`;
  `QUALITY.md:256-257`). Not independent evidence.

---

## Counter reproductions (this seat; clone `/tmp/mado-r20w2-ScribeTrendDraft`, origin removed, HEAD `a4046a8`)

| Command | Output (excerpt) | Matches claim? |
|---|---|---|
| `python3 -I .ufo/waves/round-20/tw-precision.py a4046a8…` | 175 cases, pass 172; P 66/66, S 17/17, W 21/22, H 51/52, L 17/18; score 9.8286; failing: `W-CaseWrapperForms-class-method-instance`, `L-AdoptW2-AdvHelperFn-b14`, `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` | yes |
| `… tw-precision.py 1f7f995…` | H 15/52, L 1/18, P 7/66, S 2/17, W 4/22; score 1.6571 | yes |
| `… tw-precision.py 9c54c56…` | H 35/52, L 1/18, P 66/66, S 7/17, W 1/22; score 6.2857 (sum 110/175) | yes |
| `python3 -I .ufo/waves/round-19/tw-recall.py a4046a8…` | incident_lines 6, detected 6, score 10.0 | yes |
| `python3 -I .ufo/waves/round-20/tw-recall-split.py a4046a8…` | detected_observed 5, detected_lead 1, unmarked 0, undetected 0; control_findings 0 | yes |
| `python3 -I .ufo/waves/round-20/tally-check.py --set red --rev a4046a8… tally-claims.json` | `TALLY_SUMMARY … mismatch=5`; `EXPECT_SUMMARY: 5/5`; exit 1 | yes |
| `… tally-check.py --set green --rev a4046a8… tally-claims.json` | `match=4 mismatch=0 error=0`; `EXPECT_SUMMARY: 4/4`; exit 0 | yes |
| `… tally-check.py tally-claims.json` (no `--rev`, bare) | 5 MISMATCH + 4 ERROR ("pass --rev"); **exit 2** | the lesson's "exit 1" is the red-only run; bare run is exit 2 `[INFERENCE]` |
| `python3 -I .ufo/waves/round-17/measure.py a4046a8…` | c1 criteria 30, lesson_cited 22, score 7.3333; c2 count 6, score 10.0; `rejected` MALFORMED for the new entry | c1 yes; c2 note above |
| `git show a4046a8:tools/mado-tripwire.py \| sha256sum` | `9613f510…85e27c` | yes |

Non-run: `tools/mado-verify.sh` (live gate, forbidden), `isolation-check.sh` (not in this item).

## Limits

- Scope: this is a draft of trend verdicts for the round report, not the round's spot-check.
- Sources: 6 of 14 new rows re-fetched; none of S099–S104, S109, S112 checked by this seat.
- The three verdicts are not independent of the C1/C2 counters; their numbers are reproduced above, but the counters themselves are unchanged.
- Corpus-wide no-harm diff vs `9c54c56` is wave-2 work of another seat; not computed here.
- `[UNK]` the existence of a non-author spot-check after this draft.

## Installs

none
