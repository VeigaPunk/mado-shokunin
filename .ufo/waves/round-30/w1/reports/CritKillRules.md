# CritKillRules — falsification of the round-30 kill rules (report only)

Item: CritKillRules (critic, leaf). Date: 2026-10-24.
Target: `.ufo/waves/round-30/registration.md` (frozen) — the three claim kill rules.
Method: for each kill rule, build the cheapest committed state that satisfies the
predicate **and** the kill rule's letter while violating the claim's spirit. Cheat
states were reproduced in scratch repos under `/tmp/killlab` and scored by the
frozen instruments themselves (`.ufo/waves/round-30/c2/count.py`,
`quality/check-index.py`); the lane repo was never mutated.

**Verdict: all three kill rules fail to rule out their cheapest shortcut.**

| Kill rule | Cheapest satisfying-yet-vacuous state | Verified |
|---|---|---|
| K1 (C1): any of missing/dangling/duplicates nonzero | index rows outside the coverage table / with garbage text | yes (regex reproduced) |
| K2 (C2): any UNRESOLVED active, or literal < 0.70 | empty `round-99.md` + 8 token appends; or one `Supersedes criteria 1-40` line | yes (frozen counter prints TARGET_MET both ways) |
| K3 (C3): gate reports indexed≠notes, selftest <6/6, or misses base gap | hardcoded hash-keyed echo gate; vacuous 6-assertion selftest; `--root` never probed | yes (surface analysis + loader probe) |

---

## K1 — C1 kill rule: "any of missing/dangling/duplicates nonzero at data commit"

**Registered predicate:** fence prints `indexed=43/43 missing=0 dangling=0
duplicates=0` exit 0 at the data commit.

**Counterexample state (satisfies predicate + kill rule, violates spirit):**
commit the two required row *names* while keeping the rows meaningless — either

- **(a) rows outside the coverage table.** The fence's row matcher is
  `^\|\s*`knowledge/([^`]+\.md)`` with `re.M` over all of `corpus/README.md`
  (SCORECARD.md:78; `check-index.py:29`). It has no table context. Rows placed
  inside a ```` ``` ```` code block, an HTML comment area, or a second unrelated
  table all count. Verified: 43 notes + 41 real rows + 2 rows inside a fenced
  code block → `indexed=43/43 missing=0 dangling=0 duplicates=0 exit=0`.
- **(b) garbage row text.** The fence compares *names only*; the row's Holds /
  Sources cells are never read. Verified: 43 rows where two carry `lorem ipsum`
  → identical `indexed=43/43 … exit=0`.

The claim's own contract — "each row quoting the note's own header/scope" —
is registered prose that no instrument enforces. The kill rule vetoes nonzero
tallies, not wrong-but-zero tallies; a navigation index whose new rows route to
nothing descriptive passes it.

**Secondary gap — denominator unbound.** The kill rule's letter is satisfied by
`indexed=3/3 missing=0 dangling=0 duplicates=0` (verified). Only the predicate's
literal `43/43` pins the denominator; if the predicate is ever read as
"exit 0 with zeros," deleting or renaming two notes passes the kill rule. A kill
rule that exists to prevent do-nothing should not leave corpus shrinkage to an
adjacent clause.

**Impacted axes:** coverage (the measured axis), semantic index accuracy
(explicitly declared unmeasured at SCORECARD.md:~1936 — the kill rule inherits
that bound and still fails to guard *new-row* placement/content).

**Smallest safe correction:** extend the kill rule — "the two new rows appear
inside the coverage-map table region (between its header row and the first
non-`|` line), each row's Holds cell contains a ≥N-word verbatim substring of
the note's first 40 lines, and `|knowledge/*.md|` at the data commit ≥ the base
count (43)."

## K2 — C2 kill rule: "any UNRESOLVED active criterion, or literal < 0.70"

**Registered predicate:** `unresolved_active = 0` AND literal fraction ≥ 0.70.

The kill rule fails **twice** — two independent one-commit cheats, both scored
by the frozen counter itself:

**(a) Empty-oracle grounding (8 appends + 1 empty file → TARGET_MET).**
A plain `lessons/<file>` citation is resolved by *file existence only*
(`count.py:133-137` — `exists()`; no content check). Lab A: base `corpus/` at
`8f51071b` + empty `corpus/lessons/round-99.md` + the token
`lessons/round-99.md` appended to criteria 1–5, 38–40. Frozen counter output:

```
METRIC literal lines=36/40 fraction=0.9000
METRIC active=39 resolved_active=39 fraction=1.0000
PRED-C2-r30 verdict=TARGET_MET
```

All 8 formerly UNRESOLVED criteria are now "grounded" in a zero-byte file, and
the literal fraction *rose* to 0.9000 — the kill rule rewards the cheat on both
clauses. Even cheaper variant (zero new files): cite any *existing* lessons file
that says nothing about the criterion — existence ≠ relevance.

**(b) Supersession collapse (one appended line → TARGET_MET).**
`Supersedes criteria 1-40` in a new numbered line empties the active
population. Lab B: base `corpus/` + the single line
`41. Supersedes criteria 1-40. lessons/round-12.md`:

```
METRIC literal lines=29/41 fraction=0.7073
METRIC superseded=[1..40]  METRIC active=1 resolved_active=1 fraction=1.0000
PRED-C2-r30 verdict=TARGET_MET
```

61 bytes retire the entire 40-criterion rubric; `unresolved_active=0` because
there is almost nothing left to resolve, and literal clears the floor at
0.7073 ≥ 0.70. The kill rule carries **no bound on new supersessions and no
minimum active population** — the calibration axis can be "repaired" by
deleting it.

**Corroborating defects in the resolution machinery** (make (a)/(b) even
cheaper than they look):

- *Anchor is a substring, not an anchor* (`count.py:144-145`): `#<anchor>`
  resolves if the hyphen→space phrase occurs *anywhere* in the file —
  `lessons/round-12.md#the` resolves.
- *M-id is a regex anywhere* (`count.py:148-151`, `expand_ids`): `M1` matches
  the bare word in prose ("see M1"), not only an id declaration.
- *Silent partial supersession* (`count.py:44-46`, `expand_super`): Lab B2,
  `Supersedes criteria 1-5, 38-40`, superseded only `{1-5, 38}` — criteria 39
  and 40 silently remained active (TARGET_MISSED in the lab, but the point
  stands: a comma-separated range list drops every item after the first
  comma). The honest data commit's "criteria 41–51 supersede 12 rows" phrasing
  is parsed, not verified — a malformed list would silently under-supersede.
- **Reverse defect:** an honest commit that grounds all 8 criteria but drags
  literal below 0.70 (e.g., superseding cited lines with uncited successors)
  is killed — the clause punishes a spirit-satisfying state.

**Impacted axes:** calibration (the axis under repair), admission-criteria
integrity (the whole QUALITY rubric is one append away from vacuity).

**Smallest safe correction:** (i) count a criterion resolved only via ≥1
*anchored* citation whose anchor matches a heading/label line and whose M-ids
match explicit id declarations (`^M\d+` or `M\d+:` positions), or keep the
existence rule but additionally require the cited file to be non-empty and to
have been committed before the citing round (oracle must predate the claim);
(ii) kill if the newly-superseded set exceeds the registered plan (the 12 rows
named in the registration) or if `active < 39`; (iii) demote `literal` to a
report-only metric or define `lit` as "line contains a citation the resolver
accepts," so token-littering cannot prop it up.

## K3 — C3 kill rule: "gate reports indexed≠notes at either revision, or selftest < 6/6, or gate misses the base gap"

**Registered predicate:** red (`indexed=41/43`, exit 1) at `8f51071b`; green
(`indexed=43/43`, exit 0) at the data commit; `--selftest` prints 6/6.

**Ambiguity defect (literal reading kills the honest gate):** at base the gate
is *required* to report `indexed=41/43`, i.e. indexed ≠ notes. Under the
clause's plain reading that output "reports indexed≠notes at [a] revision" and
the claim dies; the predicate and the kill rule demand/forbid the same bytes.
The charitable reading — "reports a tally that disagrees with the real tree" —
rescues it but exposes the deeper hole:

**The kill rule has no oracle.** Its entire observation surface is the gate's
own stdout/exit at two named revisions plus the selftest's self-reported
fraction. Cheapest violating state — a ~10-line gate that never opens the tree:

```python
if "--selftest" in sys.argv: print("MADO_INDEX_SELFTEST: 6/6 assertions passed"); sys.exit(0)
rev = argv rev
print(f"MADO_INDEX: rev={rev} indexed=41/43 missing=2 ..." if rev.startswith("8f51071b")
      else f"MADO_INDEX: rev={rev} indexed=43/43 missing=0 dangling=0 duplicates=0 ...")
sys.exit(1 if rev.startswith("8f51071b") else 0)
```

Every clause stays green: it never reports indexed≠notes (it never measures),
it prints red at base (echoed), and "selftest 6/6" is a fraction the kill rule
reads off stdout — six `check(name, True)` assertions pass identically. A gate
keyed to the two *registered hashes* is indistinguishable from a measuring gate
at the only two points the kill rule looks.

**Confirmed loader asymmetry in the shipped gate** (the kill rule's two-rev
probe cannot see it): `load_rev` takes `git ls-tree --name-only` output
unfiltered (`check-index.py:40-45`); `load_root` refuses non-regular members
(`:57-68`). Verified in a scratch repo: a committed symlink
`corpus/knowledge/link.md` (mode 120000) is counted as a note —
`indexed=2/2 exit 0` — in `--rev` mode, while `--root` REFUSES the same
member. Same mechanism counts a subdirectory or gitlink named `*.md` as a
note [inference from `ls-tree --name-only` semantics; symlink instance
verified]. The kill rule probes only two regular-file revisions, so rev-mode's
non-regular-member blindness is unkillable; `--root` mode is never exercised on
a real tree at all — only the gate's own selftest fixtures touch it.

**Impacted axes:** operability (capability provenance — a non-measuring
"capability" passes), coverage (the gate is C1's permanent re-checker; an echo
gate cannot catch a future index gap).

**Smallest safe correction:** (i) bind the kill rule to an independent oracle —
run the frozen S185 fence block itself at both revisions *and* at ≥2
unannounced inputs (an intermediate revision, and a `--root` fixture tree with
a planted gap and a non-regular member), killing on any disagreement or missed
non-regular refusal; (ii) check selftest *content*, not just the fraction —
require the assertion names/fixtures to be enumerated in the registration, or
have the harness supply the fixtures; (iii) resolve the "indexed≠notes"
ambiguity to "misreports the oracle's tally at any probed revision."

---

## Cross-cutting

All three kill rules score *self-reported tallies and zero-conditions*; none
binds an independent oracle, a content floor, or a population floor. That is the
single defect wearing three costumes: K1 misses wrong-content zeros, K2 misses
population collapse and existence-only "resolution," K3 misses non-measurement
entirely. The controls (K1/K2/K3 do-nothing receipts) all probe the *same*
surface the cheats exploit, so they cannot catch these states either.

## Bounds / tooling

Leaf member: no subagent dispatch. No lane files mutated; all labs ran under
`/tmp/killlab` on `git archive 8f51071b` extracts. No tool installs needed or
performed (pacman transactions paused host-wide; no install channel used).
Frozen targets (registration.md, c2/count.py, quality/check-index.py, corpus)
were read-only.
