# SimplifyMeasure — round-17 wave 2 (falsify / simplify, report only)

Target root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Files: `.ufo/waves/round-17/measure.py` (304 lines, sha256 `4023124f…846466b`),
`.ufo/waves/round-17/label-check.py` (191 lines, sha256 `b890a5ca…3a41505`).
Both match `git show 988b858:<path>` byte-for-byte; working tree was not edited by this seat.
Installs: **none**.

## Axes

1. **Byte identity** — stdout, stderr, exit status at `27cd06f` and `988b858bd6049bc709807534fd725c05264f7e60`.
2. **Weight** — lines, dead constructs, alternate paths.
3. **Parse cost** — repeated work per input.
4. **Contract fidelity** — documented semantics (QUALITY 23, script docstrings, SKILL row) that must not silently narrow.

## Method (why the pinned revs alone are not enough)

`measure.py` at both pinned revs emits `"rejected": []` — the entire rejection cascade
(`surface` malformed / thin sections / missing heading / no `[UNK]` / unsourced /
multi-surface / no upstream https row) is **unexercised**. A change to any of those
branches would pass a two-rev byte check vacuously. I therefore tested against:

- a `/tmp` clone (`git clone --shared` of the lane; reads lane objects only, writes `/tmp/simplify-repo`) — both pinned revs;
- a synthetic git repo `/tmp/synth` with five revisions exercising **every** reject branch
  (one commit each: absent corpus, QUALITY only, SOURCES only, 16 knowledge fixtures, tripwire blob);
- a 22-claim synthetic `label-claims.json` covering every doc-stage and receipt-stage
  exit path (ok via `finding` key / field string, got-side, doc-lacks-basename,
  doc-lacks-token, wrap `line_end`, past-end, missing key, bad ranges, doc/receipt
  `git show` failure, invalid JSON, `measured_commit` pass/fail, list receipt,
  non-object claim, `doc_text`, duplicate id, `name`-only claim);
- exit-2 inputs (missing claims file, `{}`, `[]`, non-JSON) and a non-repo working
  directory.

All runs use the allowed `python3 -I` invocation. No `lsp` device is mounted in this
seat, so "no semantic callers" claims rest on `git grep` at `988b858`, an AST
unused-binding scan (both files: **zero** unused bindings), and the branch-complete
suite above.

Baselines reproduced byte-exactly from the `/tmp` clone before any mutation:

| run | exit | stdout |
|---|---|---|
| `measure.py 27cd06f` | 0 | 1856 B, sha256 `54d3cac3…fd3082` |
| `measure.py 988b858` | 0 | 2559 B, sha256 `da11f088…c500c11` |
| `label-check.py` (shipped claims) | 1 | 9 lines, sha256 `b0b67843…90778811` |

## Proposed simplifications

### P1 — `measure.py`: cache section bodies, drop dead ternary, drop single-element loop (recommended)

The `len(surfaces) != 1` guard above line 241 makes the false arm of
`tuple(surfaces) if len(surfaces) == 1 else ('',)` unreachable, and makes the
following `for p in sorted(surfaces)` a one-iteration loop. `section_body` re-splits
and re-scans the same entry text 3× per heading (9 calls per surface entry: 4 for
`missing`, 1 for `unex`, 4 for `thin`); caching gives 4.

```diff
--- measure.py
+++ measure.py (proposed)
@@ -192,7 +192,7 @@
     if surfaces:
-        missing = [h for h in REQUIRED_HEADINGS
-                   if section_body(text, h) is None]
-        unex = section_body(text, '## Unexercised behavior')
+        sections = {h: section_body(text, h) for h in REQUIRED_HEADINGS}
+        missing = [h for h in REQUIRED_HEADINGS if sections[h] is None]
+        unex = sections['## Unexercised behavior']
@@ -200,5 +200,5 @@
         thin = [h for h in REQUIRED_HEADINGS if h not in missing and
-                sum(1 for l in section_body(text, h).splitlines() if l.strip())
+                sum(1 for l in sections[h].splitlines() if l.strip())
                 < FACET_MIN_LINES]
@@ -239,5 +239,5 @@
-        (only_surface,) = tuple(surfaces) if len(surfaces) == 1 else ('',)
+        (only_surface,) = surfaces
@@ -253,10 +253,9 @@
-        for p in sorted(surfaces):
-            covered[p].append({
-                'path': path,
-                'reason': f'surface: {p}',
-                'sources_ok': ok_sources,
-            })
+        covered[only_surface].append({
+            'path': path,
+            'reason': f'surface: {only_surface}',
+            'sources_ok': ok_sources,
+        })
```

Weight: 304 → 303 lines; three dead/redundant constructs removed. Parse cost at
`988b858`: `section_body` calls **18 → 8** (2 surface entries × 9 → 4). Wall-clock is
unchanged within noise (100 runs: 5.23 s vs 5.22 s; runtime is dominated by
`git show` subprocesses).

Byte identity: stdout, stderr, and exit identical on **both pinned revs and all five
synthetic revisions** (checked for the isolated pieces too: `mA` dead ternary only,
`mB` cache only, `mC` combined — all identical everywhere). The synthetic `knowledge`
commit emits all eight rejection reasons, so the cascade is actually compared, not
merely skipped.

### P2 — `label-check.py`: derive `ok` from the other counters (optional, cosmetic)

`ok` is only used in the summary and is exactly `len(claims) - mismatch - uneval`.

```diff
--- label-check.py
+++ label-check.py (proposed)
@@ -156,5 +156,4 @@
-    ok = 0
     mismatch = 0
@@ -169,5 +168,4 @@
         if status == "ok":
-            ok += 1
             print("LABEL %s ok (%s)" % (cid, stage))
@@ -181,5 +179,5 @@
-    print("LABEL_SUMMARY: %d/%d" % (ok, len(claims)))
+    print("LABEL_SUMMARY: %d/%d" % (len(claims) - mismatch - uneval, len(claims)))
```

Weight: 191 → 189 lines. Byte identity: identical (exit/stdout/stderr) on the shipped
claims and on all 22 synthetic claims plus every exit-2 input. One counter fewer to
keep in sync.

### P3 — `label-check.py`: drop the undocumented `name` alias (low-risk path deletion)

`cid = str(claim.get("id") or claim.get("name") or cid)` accepts a claim key that is
documented nowhere (`label-check.py` docstring lists only `id`; the w1 spec and all
7 shipped claims use `id` only). No other file reads claim `name`.

```diff
-            cid = str(claim.get("id") or claim.get("name") or cid)
+            cid = str(claim.get("id") or cid)
```

Byte identity: shipped claims identical. Observable delta only for an input class no
shipped claim uses: a claim with `name` and no `id` prints `LABEL alias-demo ok …`
before, `LABEL claim-1 ok …` after. Zero lines saved; the value is one fewer alternate
authority for the display id.

### P4 — `measure.py`: delete `source()`, reuse `try_source()` (optional, marginal)

`source()` is called only with paths returned by `git ls-tree -r rev_sha`, so
`git show rev_sha:path` cannot fail; its loud-error behavior is unreachable.
Dropping the wrapper: 304 → **300** lines, identical on all 7 tested revisions
(both pinned revs + 5 synthetic). Tradeoff: the loop then reads an Optional and the
"this path is required" signal disappears; if the invariant is ever broken the failure
becomes `AttributeError: 'NoneType'` instead of `CalledProcessError`. Keep `source()`
unless the line count is the priority.

## Deletion candidates that fail (counterevidence)

These are the interesting falsification results: each looks like dead weight and is not.

### R1 — do **not** merge `source`/`try_source` by dropping `quiet`

The `quiet` flag encodes a two-sided stderr contract, proven by mutants:

- always-loud (`mE`): at a revision where the optional artifacts are absent,
  stderr gains `fatal: path 'corpus/QUALITY.md' exists on disk, but not in '01a2267…'`
  (and the SOURCES twin); original stderr is empty. stdout still identical, so a
  stdout-only check would have passed this regression.
- always-quiet (`mD`): at an unresolvable revision, stderr loses git's
  `fatal: Needed a single revision`; original keeps it before
  `measure.py: cannot resolve revision 'deadbeef'`.

### R2 — do **not** delete `FINDING_JSON` (embedded verdict JSON)

Across all 93 committed JSON artifacts under `.ufo/waves/**`, **zero** tokens are
reachable only through `FINDING_JSON` — every one is also visible via a `MADO_` line,
got-side, or structural `finding` key, and every shipped label claim also passes
without it. A naive "unexercised path" deletion would still look safe.

But it is contract-bearing, not dead: QUALITY 23 defines outcome as "the verdict word
on a `MADO_<NAME>:` line, a `finding` value, or the got-side of a selftest row", and
the dominant receipt shape stores its verdict as **JSON text inside `stdout`**
(`action-frozen-final.json` has no top-level `finding`; its verdict is embedded in the
`stdout` string). The regex is the only implementation of the criterion's "`finding`
value" clause for that shape. Synthetic proof of the loss: receipt
`{"stdout":"note {\"finding\": \"snapshot_tampered\"} only"}` flips
`LABEL ok_embedded_only ok` → `MISMATCH (receipt outcome [] lacks 'snapshot_tampered')`,
summary `9/22` → `8/22`. The structural-key path is likewise load-bearing: it is the
only site for 16 tokens in `.ufo/waves/round-16/evidence/independent-cases.json`.

### R3 — do **not** delete `repo_root()` (fail-fast on a non-repo)

Removing it and passing `SCRIPT_DIR` straight to `git_show` is byte-identical inside a
repo (all scenarios), but from a non-repo directory the original prints exactly
`LABEL_SUMMARY: 0/1 (git toplevel unresolved)` (exit 2) while the mutant prints one
`COULD_NOT_EVALUATE` line per claim plus `LABEL_SUMMARY: 0/1`. Exit code survives;
the documentable failure text does not.

### R4 — reject `TOKEN` regex dedupe, C1 single-pass rewrite, round-16 unification

- Extracting `[a-z_]+` into one `TOKEN` constant **adds** a line (191 → 192) and only
  replaces three equivalent literals; no weight axis improves.
- `c1`'s two `^[0-9]+\. …` scans are the published verbatim rubric ("kept verbatim
  from round 16"); a `findall`+substring rewrite is equivalent today but would make the
  literal numerator/denominator harder to audit. Not worth the provenance risk.
- `.ufo/waves/round-16/measure.py` (436 lines, 610 diff lines against round 17) is a
  different rubric implementation serving frozen round-16 adjudication receipts;
  merging it into round 17 would touch historical evidence. Out of scope by provenance,
  not by line count.
- Inlining `used_by` into `mined_a` saves zero lines; `used_by` is the named predicate
  of the T1 join.

## Preserved contract (must remain true after any P1–P4)

- CLI: `measure.py REV` (exit 0 on any measured result, 2 on usage/unresolvable rev);
  `label-check.py [CLAIMS]` (0 all ok, 1 any MISMATCH, 2 could-not-evaluate, 2 wins over 1).
- `measure.py` output schema/order: `schema, rev, commit, c1{criteria, lesson_cited, score},
  c2{count, score, provinces{…}, rejected, u_routes, u_routes_seen}, c3{tool_present, sha256}`.
- `label-check.py` line grammar: `LABEL <id> ok|MISMATCH|COULD_NOT_EVALUATE (<stage>)`,
  `LABEL_SUMMARY: k/n`, `EXPECT_SUMMARY: m/e`; outcome tokens only from
  `MADO_<NAME>:` verdicts, `finding` values (structural and stdout-embedded), and
  `got N/<token>`; want-side text and free prose never count.
- Rubric literals (`^[0-9]+\. `, `^[0-9]+\. .*lessons/`, 13-cell SOURCES rows,
  `surface: P[1-6]`, four required headings, `[UNK]`, `FACET_MIN_LINES`, `HEAD_LINES`).
- stderr semantics: optional artifact reads silent; required reads loud; unresolvable
  rev keeps git's own message.

## Receipt consequence (blocks P2/P3 unless re-receipted)

`label-check.py`'s current bytes are themselves receipted:
`.ufo/waves/round-17/evidence/label-check.txt:12` carries
`b890a5ca771bfbe6af68d07779ea2a9d5f73a5f6481091bb5b5a7f4663a41505  .ufo/waves/round-17/label-check.py`.
Any label-check edit makes that line false until the evidence file is regenerated with
the new digest. `measure.py`'s `4023124f…` appears only in prose (lessons/round-17.md
M3, `ConnectScorecard.md` B14, `AttackSeparability.md`, `ReMeasureC1.md`), not in
`evidence/`, so a measure edit invalidates those prefixes but no receipt line.
Neither edit may ship without one of: regenerate the receipt/evidence line, or an
explicit note that the digest reference is superseded.

## Lane footprint

Read-only in the lane: `read`/`git show|ls-tree|rev-parse` plus the allowed
`python3 -I` runs. All mutants and the synthetic repo live under `/tmp`
(`/tmp/simplify-repo`, `/tmp/synth`, `/tmp/variants`). No commits, no jj, no lane
writes; the only lane artifact written is this report. Sibling agents are editing
`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/terminal-route-r17.md`,
and `corpus/lessons/round-17.md` concurrently; none of my measurements depend on
working-tree bytes (all inputs are revision-bound).

## Stop point / tradeoff

P1 is the only change that improves the weight axis beyond cosmetics and is proven
against a branch-complete suite: −1 line, −10 redundant text parses at `988b858`,
zero byte drift. P2 is safe but cosmetic; P3 removes one undocumented path at the cost
of a display-id change for inputs nobody ships; P4 saves four lines but weakens a stated
invariant. Beyond P1–P4 every remaining "duplication" is a contract edge (stderr
loud/quiet, `repo_root` fail-fast, QUALITY-23 `finding` values, required-vs-optional
source reads); deleting any of them buys lines by removing behavior, so the frontier
stops here.
