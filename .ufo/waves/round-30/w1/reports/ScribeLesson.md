# ScribeLesson — audit of `corpus/lessons/round-30.md` (round 30, wave 1)

Seat: scribe (leaf; no dispatch). Writer of this report only. No lane file, index,
counter, gate, corpus byte or sibling lane was written; no tool installed.

## Audit object and revision binding

| Artifact | Revision(s) read | Bytes |
|---|---|---|
| `corpus/lessons/round-30.md` | `446dc39` (data), `92d3c86` (records), `d72243e` (HEAD), worktree | identical, `sha256 310c5fcebc38ebdc09477e54f9ad76b6dcecda6eb7c4ea7f822e1d52ed9147ec` |
| `corpus/SOURCES.md` | `446dc39` | S185 at line 197 |
| `corpus/QUALITY.md` | `8f51071` (base), `446dc39`, HEAD | criteria 1–5, 17–19, 32, 38–52 |
| `SCORECARD.md` | `8f51071`, `451e8b3`, `446dc39`, `92d3c86`, HEAD | fence `### Counting command` |
| evidence / controls | `.ufo/waves/round-30/{evidence,controls}/` at `451e8b3`, `446dc39`, HEAD | 8 receipts, 3 controls |

Command chronology: data `446dc39` ← freeze `451e8b3` ← base `8f51071`; records `92d3c86`;
HEAD advanced to `d72243e` mid-audit (adds only
`corpus/lessons/round-30-verifier-spotcheck.md`, +109 lines; `git diff --stat 92d3c86 d72243e`
shows that one file, so `SCORECARD.md` and the lesson bytes are unaffected). Nothing was
re-run: verdicts rest on committed blobs and committed receipts.

## Verdict table

| # | Audit question | Verdict |
|---|---|---|
| A | Every Mistakes row carries class / evidence / captured-by / fix | **PASS** (structure + resolvable pointers) |
| B | Each fix shown able to fail with a committed red receipt | **PASS for M30-1; PARTIAL for M30-2** (red receipt exists and predates data, but the row names only the green one) |
| C | Gate row's quote appears verbatim in `SCORECARD.md` | **FAIL** — quote never existed in the file or its history; nearest literal is `SCORECARD.md:84` |
| D | S185 `used-by` list resolves at the data commit | **PASS** |
| E | W04 disposition consistent with criterion 17 | **INCONSISTENT** on S120/S121; **wording conflict** on S042 |

---

## A — Mistakes table fields: PASS

Header `corpus/lessons/round-30.md:11`: `| id | class | evidence pointer | captured-by | fix |`
(same 5-column shape as `round-28.md`, `round-29.md`). Cell count per row
(`awk -F'|' '/^\| M30-/ {print $2, NF-2}'`): `M30-1 cells=5`, `M30-2 cells=5`. No empty cell.

| Row | class | evidence pointer resolves? | captured-by | fix |
|---|---|---|---|---|
| M30-1 (`:13`) | attribution | yes — `corpus/QUALITY.md` base criteria 1–5 have no `lessons/` text (`git show 8f51071:corpus/QUALITY.md` lines 3–7); 28/40 literal and 31/39 resolved reproduce exactly in committed `evidence/c2-before-8f51071b.txt` / `controls/C2K1-donothing.txt` | `` `none` `` + reason | present, see B |
| M30-2 (`:14`) | scope | yes — `corpus/lessons/round-29.md:15` is row `M29-sweep`, and its text does record "the navigation counter does NOT stay exit 0 — it reads 41/43 at base and tip alike … routed to r[ound 30]" for the two named notes | `` `none` `` + reason | present, see B |

`captured-by: none` is an accepted, precedented form in this corpus, not a missing field:
`round-28.md:12-14` (M28-1/M28-2/M28-3) and `round-29.md:14` (M27-4) use the same
`` `none` — <why nothing captured it> `` shape. The M30-1 reason is accurate against the
criterion it cites: `QUALITY.md:107` (criterion 22) is about re-deriving axes and reporting
literal-vs-semantic counters separately; it does not require each criterion's own citations
to resolve. The M30-2 reason (navigation counter is a harm-watch fence, not a gate) matches
`registration.md` §Harm watch, which lists the selftest and census but no index gate.

Note (not a defect): no frozen vocabulary constrains the `class` value — no `class`
enumeration exists in `QUALITY.md`, `SKILL.md`, `AGENTS.md` or `MINT.md` (grepped). The label
`scope` for an inherited navigation gap is therefore a judgment label, not a rule violation.

## B — Fix able to fail, with a committed red receipt

### M30-1: PASS

Fix cell (`:13`) cites `controls/C2K1-donothing.txt` and quotes its output. Verified:

- committed at freeze `451e8b3` (`git ls-tree -r --name-only 451e8b3 -- .ufo/waves/round-30/`
  lists it) and present at data `446dc39` — i.e. **strictly before the data commit**;
- content is exactly the claimed red: `UNRESOLVED criterion 1..5`, `UNRESOLVED criterion
  38..40`, `METRIC literal lines=28/40 fraction=0.7000`, `METRIC active=39 resolved_active=31
  fraction=0.7949`, `PRED-C2-r30 verdict=TARGET_MISSED`, `EXIT=1`;
- `diff` against `evidence/c2-before-8f51071b.txt` is **empty** — control and before-receipt
  are the same bytes, so the "do-nothing stays red" claim is supported by committed data.

### M30-2: PARTIAL — property holds on bytes, row cites green only

Fix cell (`:14`) names `receipt \`evidence/c1-after-*.txt\`` (green, 43/43) and says the C3
gate is "red at base, green at tip" **without a path for the red leg**. The red receipts do
exist and are committed before the data commit:

- `controls/C3K1-base-red.txt` (freeze `451e8b3`): `MADO_INDEX: rev=8f51071b… indexed=41/43
  missing=2 dangling=0 duplicates=0 coverage=9.5349/10` + the two missing notes + `EXIT=1`;
- `evidence/c1-before-8f51071b.txt` (data `446dc39`): same fence output, `EXIT=1`;
- `controls/C3K2-selftest.txt` (freeze): `MADO_INDEX_SELFTEST: 6/6 assertions passed`, `EXIT=0`.

So "shown able to fail" is satisfied by committed bytes; the row's own pointer set is
green-only, which is a citation gap, not absent evidence.

Second, minor: the cited glob `evidence/c1-after-*.txt` resolves at `92d3c86`/HEAD
(uniquely to `c1-after-446dc396.txt`) but **not at the data commit `446dc39`**, because the
after-receipt landed in the records commit. That ordering is inherent to after-measurement,
but the row states the receipt without naming the commit that carries it.

## C — Gate row quote verbatim in `SCORECARD.md`: FAIL

Gate row is `corpus/lessons/round-30.md:24`. It claims a "located quote (≤25 words, verbatim)":

```
revision=$rev indexed=$covered/$total missing=$missing dangling=$dangling duplicates=$duplicates coverage=$score/10
```

(6 words, so the ≤25 bound is met.) It does **not** appear in `SCORECARD.md`:

- `grep -n 'revision=\$rev indexed=' SCORECARD.md` → **no match, exit 1**;
- repo-wide `grep -rn 'revision=\$rev'` (md/txt/py, `.git` excluded) → **one hit, the lesson
  itself** (`corpus/lessons/round-30.md:24`), no other file;
- `git log -S'revision=$rev' --oneline -- SCORECARD.md` → **no commits**: the string has never
  been in `SCORECARD.md` in any revision.

Located nearest literal, by line:

- `SCORECARD.md:32` — `## Fleet round 1 — coverage navigation (2026-10-15)` (the section the
  row names; correct);
- `SCORECARD.md:69` — ```bash (fence open), `SCORECARD.md:90` — ``` (fence close);
- `SCORECARD.md:84` — the only print statement that produces the counted line:
  `print(f"revision={rev} indexed={covered}/{len(notes)} missing={len(missing)} dangling={len(dangling)} duplicates={len(duplicates)} coverage={10*covered/len(notes):.4f}/10")`.

The quoted text substitutes `$rev`, `$covered`, `$total`, `$score` — shell-style placeholders
for a Python f-string whose real tokens are `{rev}`, `{covered}/{len(notes)}`,
`{len(missing)}`, `{len(dangling)}`, `{len(duplicates)}`, `{10*covered/len(notes):.4f}`.
It is a schematic rendering of the format, not a verbatim quote, and the registration requires
"a verbatim ≤25-word quote" (`registration.md` §Sourced claim). This is the one part of the
Gate row that fails.

The rest of the Gate row survives scrutiny:

- **`SCORECARD.md` path**: correct; it is the lane-root scorecard, not `corpus/`.
- **Block sha256 `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`**:
  reproduces exactly as the sha of the fence **body**, `sed -n '70,89p' SCORECARD.md` (fences
  excluded), at all four measured revisions:
  `8f51071 → 8b59b503…`, `451e8b3 → 8b59b503…`, `446dc39 → 8b59b503…`, `92d3c86 → 8b59b503…`.
  Brute force over every contiguous span with start 55–75 and end 70–100 found exactly one
  match (70-89), so
  the digest is genuine and the block is byte-stable across the round.
- **Access date** `2026-10-24` matches the row's open date and the round's date.

## D — S185 `used-by` resolves at the data commit: PASS

`git show 446dc39:corpus/SOURCES.md` line 197, column `used-by`:
`quality/check-index.py, .ufo/waves/round-30/registration.md`.

| used-by entry | Check at `446dc39` | Corroboration |
|---|---|---|
| `quality/check-index.py` | `git cat-file -e 446dc39:quality/check-index.py` → exists; its docstring names S185 (`grep -n 'S185'` → line 8) | created in freeze `451e8b3`, unchanged at HEAD (`git cat-file -e HEAD:quality/check-index.py` → exists) |
| `.ufo/waves/round-30/registration.md` | `git cat-file -e 446dc39:.ufo/waves/round-30/registration.md` → exists | registration cites S185 6× (C1 header, C3 header, C3 body, §Data rule, §Sourced claim, §Planner mapping) |

Independent corroboration in committed bytes: `evidence/census-end.txt` prints an empty
`=== mined used-by missing ===` section and `=== rows === 185`, `=== malformed === 0`, empty
`=== dup ids ===`; the closure spotcheck records `sources-census.sh validate` → `mado ok`.
The Gate row's sentence "The `used-by` paths … exist at the round's final commit" is true at
both `446dc39` and HEAD — no overclaim.

## E — W04 disposition vs criterion 17: INCONSISTENT (S120/S121), wording conflict (S042)

Criterion 17 is `corpus/QUALITY.md:34`. Operative clauses, verbatim:

> "…reject/merge duplicates or append a genuine superseding row with a resolvable prior id.
> Preserve rejected history, and send distinct-scope reuse to human review rather than claiming
> URL equality proves semantic duplication. A warning-only shared census is not this review."

The disposition under audit is `corpus/lessons/round-30.md:35-41`:

> "The seven W04 duplicate-URL warnings (S030/S042/S045/S097/S119/S120/S121) were re-checked
> against criterion 17: each pair is supersession or distinct-scope reuse with the rejected
> history preserved (S030→S045 rejected-duplicate, S042 supersedes S006 in a disjoint scope,
> S119 supersedes S113's scope, S120/S121 pin different sections of one file, S097 supersedes
> S094). No action; the warnings stand as intended collision-review markers."

Row statuses at `446dc39` (`awk -F'|' … status=$9`): S006 `queued`, S030 `rejected`,
S042 `mined`, S045 `rejected`, S094 `rejected`, S097 `mined`, S113 `mined`, S119 `mined`,
S120 `mined`, S121 `mined`. Census mechanics (`scripts/sources-census.sh:645`): `W04` fires
for the same normalised URL under **different scope keys** and is warning-only (`:33`);
`E04` (error) fires only for same-scope duplicates lacking a `supersedes S[0-9]{3}` link
(`:646-649`). So S120/S121 avoid `E04` purely because their scope columns differ — the exact
condition criterion 17 assigns to **human review**.

Per pair:

| Pair | Lesson's label | Criterion-17 branch | Consistent? |
|---|---|---|---|
| S030 / S045 | "rejected-duplicate" | reject/merge, history preserved (S045 finding: "supersedes S030 — REJECTED: duplicate S017…"; both `rejected`) | **yes** |
| S097 / S094 | "supersedes S094" | appended superseding row, prior id resolves (S097 title `(supersedes S094)`, S094 `rejected`) | **yes** |
| S119 / S113 | "supersedes S113's scope" | superseding row, prior id resolves (S119 finding opens "supersedes S113 —"; S113 stays `mined` — criterion 17 imposes no status flip) | **yes (mechanical)** |
| S042 / S006 | "supersedes S006 **in a disjoint scope**" | the two labels are mutually exclusive: a supersession is the allowed branch (S042 finding opens "supersedes S006 —", S006 resolves, status `queued`), while "disjoint scope" is the distinct-scope branch that **requires human review** | **wording conflict** |
| S120 / S121 | "pin different sections of one file", "No action; the warnings stand as intended collision-review markers" | distinct-scope reuse → "send … to human review"; and "A warning-only shared census is not this review" squarely rejects using the standing W04 warning as the review | **NO — inconsistent** |

Grounds for the S120/S121 finding, from the rows themselves: both are `mined`, both carry URL
`raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst`, and their
anchors are different sections (`:240-256` lazy-evaluation vs `:89-114,322-329` lexical
free-variable resolution). Neither rejects, merges, nor carries a `supersedes S1xx —` link, so
no criterion-17 branch other than "distinct-scope reuse → human review" is available. No
human review was routed: `LOG.md` round-30 entry closes with "L0: none new"; `grep -rn -i
'human review'` across `corpus/`, `LOG.md`, `SCORECARD.md` returns only
`corpus/lessons/round-13-verifier-spotcheck.md:207` (about S006) — nothing about S120/S121.

The S042 leg is weaker but real: `regex`-wise the row carries a resolvable supersedes link, so
the pair is admissible under the supersession branch; but the lesson's own words call it
"disjoint scope", and `corpus/lessons/round-13-verifier-spotcheck.md:207` already holds that
"A supersedes link is not automatic archival status for S006, and future mining of the
historical row still needs human review." Round 30 files S042/S006 as "no action" without
recording that outstanding review or S006's continuing `queued` status.

### Conflict with the closure spotcheck (verbatim, for the canonical judge)

`corpus/lessons/round-30-verifier-spotcheck.md:53-55`:

> "the 7 W04 duplicate-URL warnings are unchanged and the
> lesson's criterion-17 disposition (supersession/distinct-scope reuse) is
> consistent with the row annotations."

That check is against the **row annotations**, which is a narrower test than criterion 17's
two positive duties (explicit overlapping-scope review; distinct-scope reuse routed to human
review, with a warning-only census expressly disqualified). Both readings are recorded here
unmodified; this seat does not adjudicate them.

The same spotcheck independently reports the C finding (`:30-31`, gate item):
> "the lesson's located "verbatim" quote is a schematic rendering of the f-string format
> (`indexed=$covered/$total`), not byte-exact quote text."

and routes it to round 31 (`:99-101`). This audit reaches the same conclusion from the file
itself and adds the negative history check (`git log -S` → no commit ever carried the string).

---

## Gates / checks exercised in this audit

| Check | Command | Result |
|---|---|---|
| quote present verbatim | `grep -n 'revision=\$rev indexed=' SCORECARD.md` | no match, exit 1 |
| quote ever present | `git log -S'revision=$rev' --oneline -- SCORECARD.md` | empty |
| quote elsewhere | `grep -rn 'revision=\$rev' --include='*.md' --include='*.txt' --include='*.py' .` | only `corpus/lessons/round-30.md:24` |
| block digest | `for a in 55..75; b in 70..100: sha256(sed -n a,b p SCORECARD.md)` | unique match `70-89` = `8b59b503…` |
| digest stability | `git show <rev>:SCORECARD.md \| sed -n '70,89p' \| sha256sum` for `8f51071 451e8b3 446dc39 92d3c86` | identical `8b59b503…` ×4 |
| lesson byte stability | `sha256sum` of worktree, `git show 446dc39:`, `git show HEAD:` | identical `310c5fce…` |
| control predates data | `git ls-tree -r --name-only 451e8b3 -- .ufo/waves/round-30/` | C2K1, C3K1, C3K2, before-receipts, counter, gate, registration present at freeze |
| control == before receipt | `diff <(git show 451e8b3:…/C2K1-donothing.txt) <(git show 446dc39:…/c2-before-8f51071b.txt)` | empty |
| used-by path 1 | `git cat-file -e 446dc39:quality/check-index.py` | exists |
| used-by path 2 | `git cat-file -e 446dc39:.ufo/waves/round-30/registration.md` | exists |
| S185 cited by gate | `git show 446dc39:quality/check-index.py \| grep -n 'S185'` | line 8 |
| S185 cited by registration | `grep -c 'S185' registration.md` | 6 |
| census corroboration | read `evidence/census-end.txt` | `rows 185`, `malformed 0`, empty dup-ids, empty mined-used-by-missing |
| Mistakes cell counts | `awk -F'\|' '/^\| M30-/ {print $2, NF-2}'` | 5 and 5 |

No counter (`c2/count.py`), gate (`quality/check-index.py`), fence or census was executed by
this seat; every number above is either a static read of committed bytes or a git-only check.

## Touched surfaces

- **Written:** this report only —
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-30/w1/reports/ScribeLesson.md`.
- **Read-only:** `corpus/lessons/round-30.md`, `corpus/lessons/round-30-verifier-spotcheck.md`,
  `corpus/lessons/round-29.md`, `corpus/lessons/round-28.md`, `corpus/QUALITY.md`,
  `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md`, `scripts/sources-census.sh` (fleet root),
  `.ufo/waves/round-30/{registration.md,w1-spec.json}`, `.ufo/waves/round-30/evidence/*`,
  `.ufo/waves/round-30/controls/*`.
- **Git:** read-only plumbing (`show`, `cat-file`, `ls-tree`, `log -S`, `diff --stat`). No lane
  `jj`/index write, no commit, no push, no product edit, no sibling-lane or fleet write.

### Live-state observation (third-party, outside this item; not mine to restore)

`git status --porcelain` in the lane at audit time showed `M quality/q36-successor-receipts.txt`
(mtime `2026-10-24 04:06:46 -0300`) alongside untracked `?? .ufo/waves/round-30/w1/` (this
wave's reports dir, expected). Reported by peer `RevC1Fence` and verified here read-only:

```
quality/q36-successor-receipts.txt | 8 ++++----   (4 insertions, 4 deletions)
```

The four changed lines differ only in ephemeral runner paths (`/tmp/mado-r28-q36-ge5zx30t` →
`g3nfq53x`, `/fast/scratch/hyaku/mado-r28/ExecQ36Runner/run.gR7SQoLa` → `run.Kv8n49Ha`); every
`rc=`, `expected=`, `PASS` and `checker-output` line is unchanged, so no verdict moved. The
write is outside the round-30 registered write scope (`corpus/` index/QUALITY/SOURCES/lessons,
`.ufo/waves/round-30/`, `quality/check-index.py`). It is not restored here — restoring is not a
scribe action — and it does not affect any finding above, all of which rest on committed blobs.
Corroboration: the closure spotcheck's "`git status --porcelain` was empty" statement
(`corpus/lessons/round-30-verifier-spotcheck.md:20-21`) describes closure-time state, not
current worktree state.

## Out of scope / limits

- Claim re-execution (C1 fence, C2 counter, C3 gate) was **not** performed; the closure
  spotcheck and the committed receipts already carry that work. Where this audit cites counts
  it cites committed receipt bytes, never a fresh run.
- Depth/freshness/adjacency axes and SCORECARD scoring were not audited.
- The `SKILL.md` §Gate registry absence of `check-index.py` noted by the spotcheck was not
  re-verified here.
- `class` vocabulary: unresolved by design — no rule exists to test against, so A's verdict is
  structural plus pointer resolvability, not taxonomy conformance.
- The quote defect and the S120/S121 routing are reported, not repaired; both are lane-owner
  edits and outside a scribe's write scope.

## Findings, ranked

1. **F1 (fail, Gate provenance)** — `corpus/lessons/round-30.md:24` "verbatim" quote is a
   schematic f-string rendering; absent from `SCORECARD.md` and from its entire history. The
   real literal is `SCORECARD.md:84`. The block sha (`8b59b503…`, fence body lines 70–89) and
   access date are valid, so the row's evidence tier stands while its quote claim does not.
2. **F2 (inconsistent, criterion 17)** — S120/S121 are distinct-scope reuse by the lesson's
   own characterization and were closed with "No action; the warnings stand as intended
   collision-review markers" (`:40-41`). Criterion 17 requires human review for that branch
   and states a warning-only shared census is not that review; no review was routed
   (`LOG.md`: "L0: none new"; no record names S120/S121).
3. **F3 (wording conflict)** — S042 is described as both "supersedes S006" and "in a disjoint
   scope" (`:38-39`); these select different criterion-17 branches. S006 also stays `queued`
   with a pre-existing human-review note (`round-13-verifier-spotcheck.md:207`) that round 30
   neither cites nor closes.
4. **F4 (partial citation)** — M30-2's fix cell names only the green receipt
   `evidence/c1-after-*.txt`; the red leg exists as committed `controls/C3K1-base-red.txt`
   (freeze) and `evidence/c1-before-8f51071b.txt` (data) but is not named. M30-1 has no such
   gap (`controls/C2K1-donothing.txt`, byte-identical to the before-receipt).
5. **F5 (note, not defect)** — `captured-by: none` on both rows is precedented
   (`round-28.md:12-14`, `round-29.md:14`) and argued in place; A passes.

## Artifact paths

- Report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-30/w1/reports/ScribeLesson.md`
- Audited: `corpus/lessons/round-30.md` @ `446dc39`/`92d3c86`/`d72243e`, sha256 `310c5fcebc38ebdc09477e54f9ad76b6dcecda6eb7c4ea7f822e1d52ed9147ec`
- Contradicting/confirming evidence: `corpus/lessons/round-30-verifier-spotcheck.md:30-31,53-55,99-101`;
  `corpus/QUALITY.md:34` (criterion 17), `:107` (criterion 22);
  `SCORECARD.md:32,69,84,90`; `corpus/SOURCES.md:197`;
  `.ufo/waves/round-30/controls/{C2K1-donothing,C3K1-base-red,C3K2-selftest}.txt`;
  `.ufo/waves/round-30/evidence/{c1-before-8f51071b,c1-after-446dc396,c2-before-8f51071b,c2-after-446dc396,c3-after-446dc396,census-before,census-end}.txt`;
  `scripts/sources-census.sh:33,645-649`
