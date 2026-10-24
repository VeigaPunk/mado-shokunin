# CritPredicates — falsification of PRED-C1-r30 / PRED-C2-r30 / PRED-C3-r30

Seat: critic (report only). Method: every control is a **committed revision in a
scratch clone** (`/tmp/critpred-lab`, cloned from the lane) or a `/tmp` stub
script; the frozen counters were executed read-only from the lane working tree
(`quality/check-index.py`, `.ufo/waves/round-30/c2/count.py`, and the literal
S185 fence heredoc verbatim from `SCORECARD.md:69-89`). Lane repo untouched
(`git status` shows only the expected untracked `w1/` wave dir).

**Verdict: all three predicates are met by controls that skip the claimed work.**
Every attack below produced `TARGET_MET` / exit 0 / the exact predicate
transcript. The real claims survived because the lane's *data commit* did the
work — the predicates measure only a transcript shape, never the semantics the
claim text asserts.

## (a) PRED-C1-r30 — the fence counts name-matches, not rows

Fence/gate regex (identical in both): `^\| `knowledge/([^`]+\.md)`` over the
**whole README byte stream** with `re.M` — no table scope, no cell requirement.

Scratch commits on base `8f51071b`, each scored by the literal fence AND
`check-index.py --rev`:

| Control | README addition | Result |
|---|---|---|
| A0 sanity | none (base) | `indexed=41/43 missing=2` exit 1 — fence live |
| A1 | two rows `| \`knowledge/<n>.md\` | \| \|` **empty cells** | `indexed=43/43 missing=0 dangling=0 duplicates=0` exit 0 — **PRED MET** |
| A2 | two bare lines `| \`knowledge/<n>.md\`` — not table rows at all | 43/43 exit 0 — **PRED MET** |
| A3 | two full rows **inside an `<!-- -->` comment** (invisible in rendered markdown → not navigation) | 43/43 exit 0 — **PRED MET** |
| A4 | two rows inside a ```` ``` ```` fenced code block | 43/43 exit 0 — **PRED MET** |
| A5 | A1 rows **plus** one `knowledge/ghost-note.md` row | `dangling=1` exit 1 — kill rule fires correctly |

Answers: **an empty row reaches 43/43 — YES; a dangling row does not** (dangling
is the one thing the fence actually detects, A5). The stronger defect: the fence
is blind to table structure, cell content, and rendered visibility, so the
claim's own qualifier "each row quoting the note's own header/scope" is carried
by prose only — zero predicate weight. `SCORECARD.md`'s own caption licenses
this ("counts navigation, not the truth"), but A3/A4 rows aren't even
navigation: they index nothing a reader can follow.

Impacted axis: coverage/admitted-note reachability — the scoreboard value is
exact; the claim-text guarantee ("index rows" as routes) is not what's measured.

Smallest safe correction: require the match to be a real table row with
non-empty trailing cells — e.g. `^\| `knowledge/…` \| *\S.*\| *\S` — and/or a
selftest case: a comment-hidden row must exit 1 as missing. Do NOT loosen to
full markdown parsing; the current regex is honest and cheap — just scope it.

## (b) PRED-C2-r30 — "resolved" = file-exists + substring presence, never grounding

Controls committed on base `8f51071b` in the scratch clone, scored by the frozen
`count.py`:

| Control | Shape | Result |
|---|---|---|
| B0 sanity | none | `UNRESOLVED {1..5,38..40}`, TARGET_MISSED, exit 1 — counter live |
| **B1** | append `(see lessons/round-1.md)` to each of the 8 unresolved criteria — `round-1.md` exists (fleet-r1 navigation lesson, **zero M-ids**, wrong lesson for every criterion) | `resolved_active=39/39`, literal `36/40=0.90`, **TARGET_MET exit 0** |
| **B2 (strongest)** | single appended line `41. Placeholder amalgam criterion. (lesson: lessons/round-1.md) Supersedes criteria 1-40.` | `superseded=[1..40]`, `active=1 resolved=1`, literal `29/41=0.7073`, **TARGET_MET exit 0** |
| B4 | same as B1 but cite `lessons/round-1.md#a` — a **one-character "anchor"** | resolves: `TARGET_MET` (anchor check is `anchor.lower() in body.lower()` — every nonempty string is a substring of a big file; `M<ids>` group is optional) |
| B3 | cite `lessons/round-99.md` (does not exist) | `UNRESOLVED … missing` — the ONLY citation failure mode the counter knows |

Answers: **YES — a criterion citing `lessons/round-1.md` alone resolves**, and
so do all eight at once, and so does a *single line* that syntactically
supersedes the entire active criteria set (B2 is the cheapest full counter to
the predicate: one line of text). The rubric defines "resolved" purely
structurally; the claim word "lesson-**grounded**" and the axis name
"calibration" promise semantic relevance the counter cannot detect (irony:
criterion 18 itself, now superseded by a sibling edit, already records
"existence alone is not validation" as a lesson).

Impacted axis: calibration. `resolved_active=40/40` at `446dc396` is a true
counter output, but the number certifies *citation well-formedness*, not
grounding; B2 additionally shows `active` can be driven to 1 by text alone.

Smallest safe correction: require every citation in the anchored form
`lessons/<file>#<anchor> M<id>` (bare-path citations score as ungrounded), and
cap `Supersedes` effects at the registered supersession graph (registration
names 41–51 superseding 1–5,38–40 — count a `Supersedes` clause only for
criterion numbers the registration lists).

## (c) PRED-C3-r30 — the transcript predicate is satisfied by a 15-line stub

A stub gate that **never opens the repo, the README, or a single note** — it
string-matches `--rev` and prints the three expected transcripts:

```
python3 /tmp/stub-check-index.py --rev 8f51071b… → indexed=41/43 missing=2 … exit 1
python3 /tmp/stub-check-index.py --rev 446dc396… → indexed=43/43 … exit 0
python3 /tmp/stub-check-index.py --selftest   → MADO_INDEX_SELFTEST: 6/6 assertions passed, exit 0
```

**All three PRED-C3 clauses met verbatim.** The predicate scores
stdout/exit-code triples; "implements the fence's row-set semantics" is a claim
about the file's *contents*, which the predicate never reads. The kill rule "a
green-at-base gate is vacuous" only forces the stub to be revision-keyed — which
costs one `startswith`. Even the selftest's `6/6` is self-printed in both the
real gate and the stub.

Counter-probe on the *real* gate (faithful `/tmp` tree of base): reports
`indexed=41/43` correctly; mutated tree (rows stripped): `missing=7` correctly —
**the committed gate genuinely computes**; the falsification is of the
predicate's verification power, not the tool.

Sibling finding (RevC1Fence, same wave): the gate's `ROW_RE` is already a
strict *superset* of the fence's (`^\|\s*` vs `^\| ` — tabs, zero spaces,
non-ASCII path quirks), so "implements the fence's row-set semantics" is
approximated, not exact — it can print green where the literal fence prints
`missing=1`. All A-controls pass under BOTH implementations; the C1 hole
stands either way.

Impacted axis: operability. What was verified is "a file at
`quality/check-index.py` printed these strings" — capability is inferred by a
reader, not measured.

Smallest safe correction: register committed fixture trees (a complete tree, a
missing tree, a dangling tree — paths and expected outputs in the registration)
and require the gate's receipts against those trees; transcript alone can't
distinguish computation from keying. Cost: three ~30-line fixtures; closes the
stub class entirely because the stub can't predict fixture names.

## Net assessment for the canonical judge

| Predicate | Met-by-cheat? | Defect or declared tradeoff |
|---|---|---|
| PRED-C1-r30 | YES (A1–A4) | Fixable defect: fence scope (table-row + non-empty cells). Data claim itself stands — real rows with real quoted text landed; predicate just never enforced it. |
| PRED-C2-r30 | YES (B1, B2, B4) | Rubric defect: existence≠grounding AND unconstrained `Supersedes` shrinks the denominator by text alone. B2 is a one-line full counter — the strongest falsification here. |
| PRED-C3-r30 | YES (rev-keyed stub) | Predicate-shape defect: transcript-only verification of a capability claim. The committed tool is real (probed), the predicate can't prove it. |

None of these void the claims' honest data (real rows, real lesson text, real
gate), so all are **fixable instrument defects**, not claim-killers. If the
canonical judge must reject: reject C2 first — B2 shows the metric can be fully
satisfied by erasing the denominator, which is a rubric hole, not a measurement
shortcut.

Environment: no tools installed (stock git 2.51 + python3 sufficed); all
scratch state under `/tmp`, removed at end of run. Lane commits touched: none.
Post-run lane state: worktree shows `M quality/q36-successor-receipts.txt`
(peer RevC1Fence observed mtime 2026-10-24 04:06:46; diff = fresh ephemeral
/tmp + /fast/scratch run dirs, all rc/expected/PASS lines unchanged — a
committed evidence file rewritten outside registered write scope by another
seat's run; left unrestored, flagged to Main).
