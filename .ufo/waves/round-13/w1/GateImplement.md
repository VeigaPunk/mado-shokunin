# GateImplement — exact-set Hypr census (round 13, M13)

Seat: `MadoR13.GateImplement` (leaf executor). Owned file: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh`.
No tests/build/lint/smoke runs were executed. No commits, no host writes, no routing changes.

## 1. Files changed

| Path | Change |
|---|---|
| `tools/mado-verify.sh` | exact-set source + local `*.conf` census with named `missing`/`extra`; gkeep appended to the declared local set; scenarios N1–N4 + N7/N8; empty-member guard; hyprlang-directive fail; round-13 recut record; round-12 erratum cites `gate-standing-use.md` §5 rule 4 |
| `.ufo/waves/round-13/w1/GateImplement.md` (this file) | advisory findings |
| `.ufo/waves/round-13/w1/reports/GateImplement.md` | identical copy (both report paths named by the assignment) |

Untouched: `PIN_MADO` (`tools/mado-verify.sh:1429`), `TABLE_MADO`, the recorded `mado_r7_spec_write` body and its D6 anchors (`:1489-1491`), `SPEC_SHA` (`:1430` = `c7ee75b9…`, re-extracted and re-checked after the edits), any file outside the owned path.

## 2. Behavior landed

Row ids unchanged: `hypr.root.include_graph`, `hypr.root.sources_resolve`, `hypr.local.inventory`, `hypr.root.orchestrator`.

### 2.1 Local `*.conf` census (`tools/mado-verify.sh:2443-2483`)
- Observed set = regular files matching `$H/*.conf` at depth 1 (glob order, `LC_ALL=C`), basenames only.
- Expected set = the recorded 12-name MADO-1 list (`:2446`, byte-identical to the recorded D6 anchor) plus `LOCAL+=(gkeep)` (`:2455`). Append-only so the recorded tameshi case stays verbatim; only `PIN_MADO` moves.
- PASS: `13/13 active local confs, set exact`. FAIL: `missing:<name.conf> …` and/or `extra:<name.conf> …`, each side named in declaration/glob order.
- A same-count substitution now FAILs with both names; the old tally read 12/12 and stayed green (M13).
- Names pass through `printf %q` before entering the row detail (Safety finding 2), so a pathological filename cannot split the report row; ordinary names print unchanged. The file header's invariant line is narrowed to "exact set of regular files" to match the filter (FixtureDesign R-4 wording).

### 2.2 Source census (`tools/mado-verify.sh:2368-2400`, `:2403-2440`)
- `hypr.root.include_graph`: membership diff (`missing:`/`extra:`) first, then the unchanged order-sensitive positional walk and count test. PASS: `18/18 sources, order exact, set exact`.
- `hypr.root.sources_resolve`: membership diff plus the existing target-existence check (`[ -e ]` for literal targets, `compgen -G` ≥1 match for the toggle glob) — existence behavior is deliberately unchanged. Vanished targets keep `unresolved:<source>`; substituted members are named `missing:`/`extra:` even when the replacement target exists. PASS prints `declared targets exist, member set exact` — no count is claimed, so a duplicated declared line (caught by `include_graph`) cannot make this row's wording false (AttackSets K3).
- Empty `source =` members are excluded from the associative inserts and named `extra: ''`; the empty branch keeps the row stable and the report free of `bad array subscript` (AttackSets K2 / parent directive). No `unset` of associative keys anywhere.
- `~` expansion is `"$ROOT${t#\~}"` (Safety finding 1 — bash 5.3 `patsub_replacement` would corrupt a `ROOT` containing `&`).

### 2.3 Orchestrator: unsupported hyprlang directives (`tools/mado-verify.sh:2285-2297`)
A `# hyprlang …` line means Hyprland may skip or transform source lines the census reads as plain text, so the row now FAILs by name: `unsupported hyprlang directive at line N — conditional source semantics are not modelled` (AttackSets K1 / parent option "explicitly fail unsupported directive"). Non-source settings lines keep the previous FAIL; clean fixtures keep PASS. No parser was built.

### 2.4 Clean fixture
`build_fixture()` already writes `gkeep.conf`; it satisfies the widened 13-name expectation unchanged. Scenario A asserts both new PASS details (`:929-932`).

### 2.5 Contract row checks (statically derived from the delivered code — `[INFERENCE]`, no run)
`.ufo/waves/round-13/measure.py` cases, required substrings:

| case | row | expected detail |
|---|---|---|
| `extra-local` | `hypr.local.inventory` FAIL | `extra: extra.conf` |
| `replace-local` | `hypr.local.inventory` FAIL | `missing: xdph.conf extra: extra.conf` |
| `replace-source` | `hypr.root.sources_resolve` FAIL | `missing: ~/.config/hypr/ai-usage.conf extra: ~/.config/hypr/replacement.conf` |
| `missing-gkeep` | `hypr.local.inventory` FAIL | `missing: gkeep.conf` (plus `sources_resolve` FAIL `unresolved: ~/.config/hypr/gkeep.conf`) |

All four exit 1 with exactly one row per id. `replace-source` is the decisive case: its replacement target exists, so only the set guard catches it.

Baseline vs delivered, reported honestly: the baseline gate was **0/4 on the strict named-set row** (no `missing:`/`extra:` naming; `extra-local` was even CLEAN) but **3/4 on raw overall detections** — `replace-local` (missing-member tally), `replace-source` (order mismatch in `include_graph`), `missing-gkeep` (`unresolved:` in `sources_resolve`). The baseline caught real problems; it did not name the substituted member. Delivered: 4/4 strict and 4/4 raw `[INFERENCE]`.

## 3. Selftest scenarios (hermetic, fixture roots only)

`tools/mado-verify.sh:1055-1168`:

- **N1** stray local `extra.conf` → inventory names `extra: extra.conf`; include graph and source targets PASS (isolation).
- **N2** same-count source substitution whose replacement target exists → `include_graph` and `sources_resolve` both name `missing:`/`extra:`; `unresolved:` must not appear; local inventory PASS.
- **N3** same-count local substitution (`xdph.conf` out, `extra.conf` in) → inventory names both; `*.conf` count asserted at 13, proving a tally cannot see it.
- **N4** `gkeep.conf` removed → inventory `missing: gkeep.conf`; `sources_resolve` names the vanished target; include graph PASS.
- **N7** empty `source =` line → stable FAIL + verdict, `extra: ''` named by both census rows, and no `bad array subscript` in the captured output (K2 regression).
- **N8** `# hyprlang if UNDEFINED` / `# hyprlang endif` around a source line → orchestrator FAIL names the unsupported directive; include graph stays PASS; no fake CLEAN.

Assertion delta: +2 in A, **+39 in scenarios N** = +41. L1 measures the suite total.

Safety hardening in the same diff: selftest fixture cleanup now deletes only `/tmp/w5-mado-m52-selftest.*` (`:1018-1020`); previously it ran `rm -rf` on whatever the child printed.

## 4. Evidence

Host reads (read-only, no compositor contact, 2026-10-20):

- `ls ~/.config/hypr/*.conf` → exactly 13 basenames: `ai-usage autostart bindings envs gkeep hypridle hyprland hyprlock hyprsunset input looknfeel monitors xdph` — equals the new expected set, so live `hypr.local.inventory` stays PASS.
- `grep -nE '^[[:space:]]*source[[:space:]]*=' ~/.config/hypr/hyprland.conf` → 18 source lines at file lines 4–13, 16–20, 23, 29, 32, in EXPECT order with `gkeep.conf` last (line 32) — set diff empty, live `sources_resolve` stays PASS.
- `grep -nE '^[[:space:]]*#[[:space:]]*hyprlang' ~/.config/hypr/hyprland.conf` → no match (rc 1, 2026-10-20), so the new orchestrator FAIL cannot fire on the live file.
- Repo anchors: `corpus/knowledge/config-drift-r12.md:86-87` (M13), `corpus/lessons/round-12.md:104-112` (R12-a/R12-b), `corpus/knowledge/gate-standing-use.md` §5 rules 2 and 4.

No external URL/source was opened this round; no external-source claim is made, so no quote/tier/flip table applies.

Derived regression target (gate's own excisor, **not applied to any pin**):

```
2161 lines
sha256 87910c39f460ad169b879fc28f2e80f2c988d56f91e18b51efcac9cb0ec04b39
```

`PIN_MADO` still holds `538d178b…`. The embedded spec re-extracted after the edits hashes to `c7ee75b9…` = `SPEC_SHA`.

## 5. Covering mutation anchors (for main's proofs)

Every anchor is an exact, unique substring of the delivered derived target (`grep -cF` = 1). Apply one at a time, run `bash <mutant> --selftest`; expect `MADO_SELFTEST: FAILED` naming the assertion below.

**P1 — local extra guard.** old:
```
    if [ -z "${lexp["$x"]:-}" ]; then
```
new:
```
    if false; then
```
kills: N1 `the stray member is named`, N3 `the undeclared member is named`.

**P2 — local missing guard.** old:
```
      lmiss="$lmiss $xq"
```
new:
```
      :
```
kills: N3 `the absent declared member is named`, N4 `the local census names gkeep.conf`.

**P3 — source extra guard.** old:
```
      [ -n "${tdecl["$t"]:-}" ] || tset="$tset extra: $t"
```
new:
```
      :
```
kills: N2 `sources_resolve names the extra member`.

**P4 — source missing-member guard.** old:
```
      [ -n "${tseen["$t"]:-}" ] || tset="$tset missing: $t"
```
new:
```
      : # mutant: source missing-member guard suppressed
```
kills: N2 `sources_resolve names the missing member (its target exists)`.

**P5 — include-graph extra guard.** old:
```
      [ -n "${declared["$i"]:-}" ] || sdiff="$sdiff extra: $i"
```
new:
```
      :
```
kills: N2 `the extra source is named`.

**P6 — empty-member naming.** old:
```
      if [ -z "$i" ]; then sdiff="$sdiff extra: ''"; continue; fi
```
new:
```
      : # mutant: empty-member naming suppressed
```
kills: N7 `the empty member is named as extra`, N7 `no bad-subscript error`.

**P7 — hyprlang directive fail.** old:
```
    hyprd=$(grep -nE '^[[:space:]]*#[[:space:]]*hyprlang' "$f" | head -1)
```
new:
```
    hyprd=''
```
kills: N8 `the unsupported directive is named`.

**P8 — widened member (gkeep).** old:
```
  LOCAL+=(gkeep)
```
new:
```
  : # mutant: gkeep dropped from the expected set
```
kills: A `the local census is exact-set, gkeep included`, N4.

**P9 — recorded D6 (unchanged).** Drops `xdph` from the 12-name list; no anchor edit needed. kills: A `the local census is exact-set, gkeep included` (`xdph.conf` reads as an extra).

P8 is the covering mutant owed by round-12 `R12-a` / §5 rule 2 for the widened list; P9 is the recorded case, now killed by the exact-set guard rather than a tally.

## 6. Named residuals (not new scope, per planner bound)

- **R-1 target-shape pinning.** `[ -e ]` (literal targets) and `compgen -G` (toggle glob) accept directories: hyprland 0.56.2 skips a directory source, yet `sources_resolve` would PASS while the toggle row reads NOTE. Regular-file target validation was explicitly left out of C2 (planner bound, AttackSets K5 / FixtureDesign finding 2).
- **R-2 duplicate source declarations.** A repeated declared line fails the count/order test but the duplicate occurrence is not named (duplicate clause removed as optional/non-cell; FixtureDesign finding 1, AttackSets K3). The row that owns multiplicity is `include_graph`; `sources_resolve`'s PASS text no longer claims a count, so it stays truthful when a duplicate is present (`declared targets exist, member set exact`).
- **R-3 order-swap fixture.** Order sensitivity is unchanged and asserted only indirectly (failure direction in N2, isolation in T3); a dedicated swap case was not added (AttackSets K4, outside the four predeclared cases).
- **R-4 hyprlang conditional semantics.** Presence FAILs the orchestrator row; which lines would actually load under a condition is unmodelled. `# hyprlang noerror` over-matches deliberately (fails closed).
- **R-5 general hyprlang grammar** (`include=`, variables, nested conditions) is unparsed; the gate judges the literal source list.
- **R-6 source member display.** Source-line members are single lines by construction (awk line split), so `%q` was applied only to local filenames, which have no such guarantee (AttackSets K6/K7).

## 7. Verification commands for L1 (exact)

```bash
cd /home/vgpnk/Projects/shokunin/mado-shokunin

# 1. syntax (already clean here)
bash -n tools/mado-verify.sh

# 2. derived target sha for the recut (expect 87910c39f460ad16…, 2,161 L)
sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-REGRESSION-BLOCK <<<$/d' \
    -e '/^[[:space:]]*# >>> MADO-R7-SELFTEST-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-SELFTEST-BLOCK <<<$/d' \
    -e '/^[[:space:]]*# >>> MADO-R8-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R8-BLOCK <<<$/d' \
    tools/mado-verify.sh | tee /tmp/r13-derived.sh | sha256sum
wc -l /tmp/r13-derived.sh

# 3. selftest — PRE-recut: exactly ONE failure, R10 (stale PIN_MADO, by design);
#    POST-recut (PIN_MADO=87910c39…): MADO_SELFTEST: <n>/<n> assertions passed
bash tools/mado-verify.sh --selftest

# 4. recorded mutation case — POST-recut: MADO_REGRESSION: PASS, TABLE unchanged
bash tools/mado-verify.sh --regression

# 5. host file plane, read-only — row count/tallies unchanged from round 12 (29/0/8/4)
bash tools/mado-verify.sh --no-live
# expect: hypr.local.inventory   PASS  13/13 active local confs, set exact
# expect: hypr.root.sources_resolve PASS declared targets exist, member set exact
# expect: hypr.root.orchestrator PASS  0 settings lines (pure orchestrator)

# 6. exact-set measurement (needs the change present in the revision it reads)
python3 .ufo/waves/round-13/measure.py <rev>   # exact_set.detected == 4
```

## 8. Risks / blockers

- **Pre-recut red:** `--selftest` fails R10 only until L1 writes the measured `PIN_MADO`; `--regression` reads SETUP with the printed `REGRESSION_RECUT`. Designed stale-pin signal (`gate-standing-use.md` §5 rule 2), not a defect. `PIN_MADO` not edited (§5 rule 4).
- **Behavioral widening:** any operator-added local `*.conf` regular file, any undeclared source line, or any `# hyprlang` directive is now a named FAIL instead of silent tolerance. Intended M13/anti-claim remedy; the response is updating the declared set with a covering mutant.
- **measure.py reads a commit** (`git show <rev>:tools/mado-verify.sh`); the uncommitted tree is invisible. L1 owns commit and measurement.
- **No new dependency:** associative arrays already used (`MADO_R8_ST`); bash ≥4, host 5.3.
- **Not measured here:** suite totals and the four row outputs are static derivations (`[INFERENCE]`), per the no-checks lane rule.
- **Pre-existing, out of scope (Safety):** `boundary_hash` covers all of `~/.config` (unrelated app writes can cause a false DIVERGED, F8); `--snapshot` writes through a symlink planted after its existence check (F13, fix with `set -C`); 8 stale `/tmp/w5-mado-m52-selftest.*` fixture dirs (F11) — remove after the recut, when no selftest is running.
- **Stale peer drafts:** `w1/FixtureDesign.md:140` and `w1/CensusRecon.md:228` still print the old expected output `18/18 targets exist, set exact`; the delivered text is `declared targets exist, member set exact` (`tools/mado-verify.sh:2431`). Do not use those two lines as expected output.
- Blockers: none. Tooling: nothing installed or upgraded.
