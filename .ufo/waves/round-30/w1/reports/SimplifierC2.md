# SimplifierC2 — YAGNI review, round-30 C2 counter + index gate (report only; no lane edits)

Seat: SimplifierC2 (wave-1 simplifier leaf; no dispatch). Read-only over the lane; mutants ran on `/tmp/simplc2/` copies only. No lane byte was written by this seat (worktree `M` entries below belong to the L1's in-flight addendum).

## Bytes measured (byte-anchors, not worktree)

| File | sha256 (16) | Committed at | Notes |
|---|---|---|---|
| `.ufo/waves/round-30/c2/count.py` | `cbc2941b81264a1e` | `451e8b3`, `446dc39`, `92d3c86`, `d72243e`, `15ddd7d` (identical at all five) | the frozen PRED-C2-r30 counter |
| `quality/check-index.py` | `fc4a10a223cea253` | `451e8b3` … `d72243e` | bytes analyzed below; predicate revisions `8f51071b`/`446dc39` carry these bytes |
| `quality/check-index.py` | `373680fe4fb97332` | `15ddd7d` (HEAD) | post-freeze "gate repair" addendum: 8 selftest checks, ROW_RE tightened to `^\| ` (RevC1Fence/MutC3Gate response), selftest 8/8 exit 0 |

Timeline observed live: HEAD moved `d72243e → 2db0c44 → 15ddd7d` during this session; I caught one transient worktree state selftesting 6/8 (L1 mid-repair, mtime 04:09) and one unparsable worktree snapshot during my ruff scan (mtime 04:12). The **committed** tip parses clean (ruff on `git show 15ddd7d:` bytes: "All checks passed"). Worktree at report time: `M count.py`, `M corpus/QUALITY.md`, `M quality/check-index.py`, `M RevC1Fence.md` — L1 composing the next addendum; every claim below is anchored to committed sha256s.

Tooling: `xd://lsp` answered "No such tool: xd://lsp" → no language server on this host; textual grep is therefore fallback-only and is NOT offered as semantic proof anywhere below. Dead-code claims rest on ruff 0.17.1 / vulture (both preinstalled in `~/.local/bin`) plus behavioral byte-diff mutants — mechanical and behavioral evidence, stronger than reference lookup for these two self-contained scripts. Nothing was installed or updated; no pacman transaction.

## Baselines (narrow existing checks, all reproduced this session)

- `count.py 446dc39` → `literal 40/52 fraction=0.7692`, `active=40 resolved_active=40 fraction=1.0000`, verdict TARGET_MET, exit 0; `count.py 8f51071b` → `28/40`, `31/39`, UNRESOLVED {1..5,38..40} all "no citation", TARGET_MISSED, exit 1. Matches registration Before/Target exactly.
- `check-index.py --rev 8f51071b` → `indexed=41/43 missing=2` exit 1 (names both routed notes); `--rev 446dc39` → `indexed=43/43` exit 0; selftest 6/6 exit 0 at `fc4a10a2`, 8/8 exit 0 at `373680fe`. Runtime of the counter at the data commit: 0.096 s wall.

## Findings

### 1. Unused imports — none, at every committed revision
ruff `--select F,E9`: clean on `count.py` (`cbc2941b`) and on the gate at both `fc4a10a2` and committed tip `373680fe`. Every import in both files is exercised (`Fraction` in the two fraction prints; `tempfile`/`argparse`/`Counter` in selftest/main/evaluate). **No deletion.**

### 2. `residual/FinalBindingReview.md` in criterion 48's citation — skipped, correctly
Criterion 48 (QUALITY.md line 354) reads "…(lesson: lessons/round-21.md#mistakes M13; residual/FinalBindingReview.md F1–F5 and its six inert fixtures)"; criterion 52 (line 306 block) has the same shape ("Ground: lesson round21 M13, `residual/FinalBindingReview.md` …").
- All three resolver regexes require a `lessons/round-…` path or the `lesson round<N> M…` spelling; `residual/FinalBindingReview.md` matches none — it is neither counted as a citation nor existence-checked. Per the frozen rubric (docstring + registration: only `lessons/<file>`, `lessons/<file>#<anchor> M<ids>`, `lesson round<NN> M<ids>` are citations), that is the correct skip.
- Behaviorally confirmed: criteria 48 and 52 both carry genuine lessons citations, and the data-commit run prints `resolved_active=40/40` with an empty UNRESOLVED list — had the resolver tripped on the residual path, both would be red. The residual file does exist in-tree at `446dc39` (`git cat-file -e` OK), so the prose reference is truthful; the counter simply stays out of its scope. **No change needed.**
- Corpus-side wrinkle worth naming (not a code defect): criterion 47's "(lesson: lessons/round-14.md#mistakes M1; **outside** lessons/round-13-verifier-spotcheck.md R13-V1)" — the negating word "outside" is prose the counter cannot see, so the "outside" file IS matched by PATH_RE and existence-checked (currently green at `446dc39`). Latent only; it would red wrongly if that file were ever removed.

### 3. Duplicated `git()` helpers — near-duplicates, recommend KEEP
`count.py git(*args)` = `check_output(["git", *args], text=True)` (no `-C`, stderr passthrough); `check-index.py _git(repo, *args)` adds `-C repo` and `stderr=STDOUT` so git error text reaches its `SETUP_ERROR` line. Three lines each, **semantically different** (repo anchoring, stderr capture), living on opposite sides of an ownership boundary (frozen round-scoped counter vs committed quality tool, different lifecycles, this round froze them independently). Extracting a shared module would create a new cross-ownership import convention and couple two artifacts the registration deliberately freezes separately — a second convention, the exact thing this review must not create. **Keep; no action.**

### 4. SPELL_RE vs PATH_RE overlap — output-inert today, but rubric-frozen: KEEP
The two do not overlap at all in match domain: SPELL_RE is the slash-less `lesson round<N> M…` spelling; PATH_RE requires the literal `lessons/` path. The real redundancy is ANCH_RE ⊃ PATH_RE (every anchored citation is matched twice → one redundant `exists()`/`file_text()` git call pair), and no memoization across criteria.
Empirical mutant (m2: SPELL_RE removed from citation collection and resolution):
- `446dc39`: **byte-identical** output, exit 0. `8f51071b`: **byte-identical**, exit 1.
Why: the only SPELL-shaped citations in the corpus (`lesson round21 M10` line 304, `lesson round21 M13` line 306) sit in/next to criterion 32, which is superseded at the data commit (its block also resolves via PATH_RE hits), and criterion 48's prose mention "`lesson round21` spelling" is followed by a backtick, not ` M<id>`, so SPELL_RE correctly ignores it.
Verdict: SPELL_RE is a **currently-inert facility** at both measured revisions — but it is named in the frozen rubric (registration C2 text and the counter docstring). Deleting it would be a registration deviation, not a simplification, and the counter's red-path control (K2) is byte-pinned. **Keep; owner may retire it in a future round's re-freeze together with the rubric text.** The ANCH/PATH double-call is not worth removing: 0.096 s total runtime, once per round.

### 5. Dead code found (beyond the asked list) — two concrete deletions, both proven
- **`count.py:128` — `c["cited"] = bool(citations)` is a dead store.** Assigned once, never read (the only readers of citation state are the local `if not citations: continue` and `c["resolved"]`; grep shows no other `cited`). Mutant m1 (line deleted) at both `446dc39` and `8f51071b`: **byte-identical stdout, exit codes 0/1 preserved**. Safe one-line deletion for the owner's next counter re-freeze.
- **`check-index.py:138` — `symlink_knowledge=False` is a dead parameter** (vulture, 100% confidence, at both `fc4a10a2` and committed tip `373680fe`). `_write_tree` never reads it; all call sites (6 at `fc4a10a2`) pass two/three args; the symlink-refusal coverage is done by hand-built fixtures (case 5, and case 8 at the tip). Mutant m3 (parameter removed) at `fc4a10a2`: gate `--rev` outputs **byte-identical** at both revisions, selftest unchanged. (The 6/8-vs-6/6 selftest diff seen mid-session was the L1's transient in-flight bytes, not this mutation.) Survives at tip `373680fe:138`. Safe signature slimming for the owner's next gate commit.
- Rubric deviation, latent-only: counter `CRIT_RE = ^\s*(\d+)\.\s` is broader than the frozen `^[0-9]+\. ` (leading whitespace accepted). `git show 446dc39:corpus/QUALITY.md` has **0** indented numbered lines → inert today. The counter is frozen; name-only, owner decides at a future re-freeze (tightening would also make `LIT_RE` redundant, since a first line matching the frozen pattern is then guaranteed `^[0-9]+\. `).

### 6. Non-round `lessons/` blind spot — latent, none today
PATH_RE requires the `round-` prefix. All 30 distinct `lessons/` references at `446dc39` are `round-*.md` (including 9 `round-NN-verifier-spotcheck.md` files, which `[\w.-]+` covers) — nothing escapes. If the corpus ever cites `lessons/<non-round>.md`, the counter would silently not count it. No current defect; record for the rubric's next revision.

## Deletions made / candidates
- Made: none (report-only lane; task forbids edits).
- Candidates for the owner: `c["cited"]` dead store (count.py:128), `symlink_knowledge` dead parameter (check-index.py:138, survives at tip) — both proven behavior-preserving by byte-identical mutants on the measured revisions.
- Rejected with reasons: git() merge (cross-ownership coupling), SPELL_RE removal (frozen rubric), ANCH/PATH dedupe+memoization (0.1 s once-per-round), CRIT_RE tightening (frozen; latent).

## Preserved contract
PRED-C2-r30 (TARGET_MET iff unresolved_active=0 and literal ≥ 0.70) and PRED-C3-r30 (gate red at base, green at data commit, selftest N/N) — both reproduce exactly on the committed bytes measured; every proposed change is output-identical or owner-deferred. Tradeoff of record: the two "keep" verdicts accept ~6 duplicated lines and one inert regex as the price of not coupling frozen artifacts mid-round.

## Churn notice for Main
The lane worktree is under active concurrent edit by the L1 (next addendum; `M` on all three files this item reads, plus `RevC1Fence.md`), and the committed gate gained a post-freeze repair addendum (`15ddd7d`) during this session — selftest is 8/8 there and the RevC1Fence ROW_RE deviation is tightened at tip. Any seat measuring "current" gate bytes should pin sha256s, not mtimes. RevC1Fence's separate observation (`q36-successor-receipts.txt` worktree rewrite) is consistent with the same churn; that file is outside my scope and untouched by me.

### Addendum (post-report tip move, per RevC1Fence)
Tip has since advanced to `a0dd664a` with gate sha256 `51b513f5…` (the bytes I saw as a transient *worktree* state at 04:12, now committed): selftest **9/9** — case 9 is a real git fixture (`café.md` + `a b.md`, `-c core.quotepath=off`), and `--rev`/`--root` now agree (2/2) on the non-ASCII+space fixture, closing RevC1Fence S1–S5; S6/S7 routed to r31. Clarification so the churn notice above cannot be misread: the transient 6/8 selftest and the one unparsable snapshot were **mid-edit worktree states during the repair window, never committed blobs** — every committed revision I measured (`…d72243e` `fc4a10a2`, `15ddd7d` `373680fe`, `a0dd664a` `51b513f5`) parses and selftests green. All findings and byte-anchors in this report are unaffected: they were made against committed sha256s (`cbc2941b` counter, `fc4a10a2` frozen gate), and both deletion candidates remain valid — `symlink_knowledge` is still present and dead at `51b513f5` (verified: vulture 100% on the committed `a0dd664a` blob, line 139; line 138 at `15ddd7d`'s `373680fe`). HEAD has since advanced again (`274f7355`); this report intentionally pins revisions, not tip.
