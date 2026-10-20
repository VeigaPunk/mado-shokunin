# AttackSets — critic report, Mado round 13 / w1 (C2 exact-set census)

Seat: `MadoR13.AttackSets` (critic, leaf). Axes: **operability** (primary), coverage (none hit).
Attacked: the same-count substitution, comment, whitespace, duplicate, ordering, glob/path, and missing+extra designs.

## 0. Bytes bound

| Item | Value |
|---|---|
| Baseline gate | `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` @ HEAD `7dcb785b7b943d03703181b218d7860a7b43007b` (baseline `:2184-2273`) |
| In-flight gate (GateImplement, uncommitted) | same path, sha256 `a48adbdf57253494ab33283df222af02ebcbc7d03b064e94a3930d295ab6e910`. Line numbers below are for these bytes and may move. |
| Key in-flight anchors | orchestrator `:2285`; extraction `:2330`; set maps `:2336-2340` (`seen["$i"]=1` at `:2338`); positional walk `:2341-2350`; `sources_resolve` `-e` at `:2371`; local census `:2397-2423` (`LOCAL+=(gkeep)` at `:2403`, `for x in "$H"/*.conf` at `:2406`); N1–N4 at `:1053-1131` |
| Shell semantics | `set -u` and `export LC_ALL=C` (`:74-75`); host bash `5.3.15(1)-release` |

Nothing was run against the gate: no selftest, no `--no-live`, no regression. The only probes were:
- bash/awk language-semantics one-liners in `/tmp/attacksets-probe.*`, since removed;
- read-only name/shape counts of `~/.config/hypr`;
- reads of upstream sources (§5).

No tools were installed or updated.

## 1. Verdict summary

| # | Counterexample (minimal) | Baseline (code-read) | In-flight (code-read + semantics probe) | Class | Axis |
|---|---|---|---|---|---|
| K1 | `# hyprlang if` block wrapping one declared `source` line | all hypr rows PASS | all hypr rows PASS | **False green**: same count, same set, same order | operability |
| K2 | append `source =` (empty value) | `include_graph` FAIL (19≠18), rows printed | **bash aborts at `:2338`**; exit 1, no row table, no `MADO_VERIFY:` line, no boundary proof | **Regression introduced by the change** | operability |
| K3 | duplicate declared line (count+1, or replacing another line) | count-only or first-position message | `include_graph` FAIL with no dup name; `sources_resolve` **PASS "…set exact"** | Misleading PASS detail; already raised as ReviewCensus F1 / FixtureDesign Gap A | operability |
| K4 | an order-only permutation passes the whole suite once the positional walk is dropped | n/a | positional walk intact, but **no hermetic case reorders** | Test gap. Order is the precedence semantics. | operability |
| K5 | non-glob source target replaced by a directory | `sources_resolve` PASS (`-e`) | same PASS | False green, now grounded in upstream code (§5 S-c) | operability |
| K6 | `source = ~/.config/hypr/gkeep.conf # note` | FAIL, first position | FAIL: `missing: …gkeep.conf extra: …gkeep.conf # note` | Fails closed, but the detail says gkeep is *missing* | operability (diagnostic) |
| K7 | local filename containing a space or newline | not named (extras invisible) | names joined by spaces; a newline truncates the printed detail and the snapshot writer refuses the file | Ambiguous or truncated naming | operability (diagnostic) |
| K8 | gkeep "missing" by a commented-out source line, file kept | FAIL, count-only | FAIL, named on both rows. **Not hermetically covered** (N4 only deletes the file). | Coverage of the C2 case is incomplete | operability |
| K9 | D7 mutant (`-ne`→`-lt`) under the in-flight code | killed by H | still killed, but **only** by H's `include_graph` row assertion | Kill path narrowed; noted | operability |

Already raised by peers and not repeated here, only referenced:
- toggle-glob expansion is unpinned (ReviewCensus F2);
- the `[ -f ]` predicate drops directories and dangling links (ReviewCensus F3);
- two rows flip on one edit (ReviewCensus F4);
- the C2 baseline is 3/4 under a "FAIL row" predicate (AttackClaims A2, ReviewCensus F6);
- SPEC/D6 anchor identity (AttackClaims A1, ReviewCensus F8).

## 2. Counterexamples in detail

### K1 — HIGH — hyprlang comment directives change the effective include set; every census row stays green

**Fixture delta** (copy of clean A; insert after the theme include so T3's line-13 anchor is unaffected):
```
# hyprlang if MADO_NEVER_SET
source = ~/.config/hypr/gkeep.conf
# hyprlang endif
```
In fixture A the two comment lines wrap the existing last source line.

**Hyprland effect.** hyprlang's `parseLine` trims the line, sends `#`-initial lines to `parseComment`, and returns early for every line while the innermost `if` block is failed. An undefined variable sets `failed = !negated`, which is true. Hyprland's `source` handler is never called for the wrapped line, so gkeep is **not sourced** (§5 S-a, S-b).

**Gate.**
- `hypr.root.orchestrator` admits both directive lines as comments: `^[[:space:]]*(#|$)` at `:2285`.
- `awk` still extracts the wrapped `source` line (`:2330`), so count is 18, set equal, order exact. `include_graph` PASSes with "order exact, set exact".
- `sources_resolve` PASSes (the target exists), and `local.inventory` PASSes.
- Baseline is identical. This is the one shape where same count + same set + same order is still wrong.

**Contradiction.** FixtureDesign §5.1 S4 says "own-line `#` comments in the root" are inert. hyprlang 0.6.8 treats `# hyprlang …` comments as directives (if/endif/noerror).

**Smallest safe correction.** In the orchestrator row, FAIL any root line matching `^[[:space:]]*#[[:space:]]*hyprlang`. `parseComment` trims after `#` and tests `starts_with("hyprlang")`, so this regex is the exact trigger. Name the line number in the detail; the row id is unchanged. Add hermetic case N-K1: the wrap above, with orchestrator FAIL and include_graph PASS (isolation). Optionally FAIL `include_graph` too, but one row suffices.

**Host.** Read-only count of `^[[:space:]]*#[[:space:]]*hyprlang` in `~/.config/hypr/hyprland.conf` is 0, so the correction does not move the live verdict.

### K2 — HIGH (regression introduced by the change) — an empty source value crashes the verifier

**Fixture delta:** append the line `source =` to `hyprland.conf`.

**Mechanism.**
- `awk` emits an empty string (`:2330`), so `got` gains `""`.
- `seen["$i"]=1` with an empty key is a fatal "bad array subscript" in non-interactive bash. The same applies to `tseen["$t"]=1` later.
- Probe of the exact construct (`set -u`, `LC_ALL=C`, `local -A seen=()`, loop over the mapfile'd awk output), bash 5.3.15:
  ```
  n=2
  bash: line 1: seen["$i"]: bad array subscript
  rc=1
  ```
  Nothing after the loop runs: not the function's tail, not the caller.

**Gate effect.**
- `verify()` dies before any row prints. Rows print at the end of the script, in the `for r in "${ROWS[@]}"` printer.
- There is no `MADO_VERIFY:` verdict and no `boundary.readonly` proof.
- Exit 1 collides with the DIVERGED code in the exit map. An exit-code consumer reads "DIVERGED" with no rows.
- Baseline printed all rows: `include_graph` FAIL "19 source lines (expected 18)".

**Hyprland effect.** Hyprland rejects the line with `source= path garbage` / `… bogus!` (`rawpath.length() < 2`, §5 S-c). The config really is broken, but the gate must report that as a row, not crash.

**Smallest correction.** Before every associative-array insert over `got` (at `:2338` and the `tseen` loop), skip empty members and record them, for example `extra: ''` (or `empty source value`). Add hermetic case N-K2: append `source =`; expect `include_graph` FAIL, `MADO_VERIFY: DIVERGED` present, counts agree.

### K3 — MEDIUM — the multiset collapses, so "set exact" is overclaimed

The duplicate finding itself is ReviewCensus F1 and FixtureDesign Gap A.

**Additional counterexamples.**
- **Duplicate-only.** Append a second `source = ~/.config/hypr/autostart.conf`. In Hyprland, `exec-once` entries in that file are parsed twice. Result:
  - `include_graph` FAIL "19 source lines (expected 18)", with an empty `sdiff`;
  - `sources_resolve` **PASS "18/18 targets exist, set exact"** (`:2363-2379`: `tset` and `tmiss` are both empty).
- **Duplicate replacing a line, count stable.** Replace the `ai-usage.conf` line with a second `gkeep.conf` line. `include_graph` FAILs with "line 17 … missing: ~/.config/hypr/ai-usage.conf"; the duplicate is never named.

**Constraint for the pending fix** (new): do **not** remove keys with `unset "m[$k]"`. With bash 5.3.15:
- a key containing `$(…)` is command-substituted by the double-quoted `unset` form. Probe printed `INJECTED` and the entry survived.
- the single-quoted `unset 'm[$k]'` did not inject.

Local filenames feed `lobs`, so a filename such as `$(cmd).conf` would make a read-only verifier execute code. Count with `seen["$i"]=$(( ${seen["$i"]:-0} + 1 ))` and never `unset` by key. Name `duplicate: <path> (×N)`.

### K4 — MEDIUM — order, the precedence semantics, has no hermetic negative case

The in-flight PASS criterion is still the positional walk (`:2341-2350`). That is correct.

**Gap.** No case in N1–N4, A, B, C, H, or T3 permutes two declared lines. T3 only shifts a line number with a comment. A refactor that replaces the walk with set equality would pass the entire selftest.

**Correction.** Endorse FixtureDesign N8: swap `~/.config/hypr/monitors.conf` and `~/.config/hypr/input.conf`. Expect:
- `include_graph` FAIL, with no `missing:` or `extra:` token;
- `sources_resolve` PASS (set equal);
- `local.inventory` PASS.

### K5 — MEDIUM — directory targets: `-e` is a false green at the host's Hyprland version

FixtureDesign N11/N12/N13 already proposed this; this adds the upstream ground.

**Hyprland v0.56.2** (`legacy/ConfigManager.cpp` `handleSource`):
- globs every `source` path with `GLOB_TILDE`;
- logs `source= skipping directory` and continues, with no error;
- skips non-regular files the same way.

**Gate.** `[ -e "$x" ]` at `:2371` accepts a directory, and `compgen -G` accepts a directory-only glob match. So `rm ….conf && mkdir ….conf` on any non-local target (for example `~/.local/share/omarchy/default/hypr/windows.conf`) PASSes every row while Hyprland loads nothing from it.

**Correction.**
- Literal targets: test with `-f`. It follows symlinks, as `std::filesystem::status` does upstream.
- Glob targets: require at least one regular-file match.
- Keep the row id.

### K6 — LOW — inline `#` makes the missing/extra wording misleading

`source = ~/.config/hypr/gkeep.conf # gkeep notes` is effectively unchanged for Hyprland: hyprlang cuts at the first unescaped `#` (§5 S-b). The gate's `awk` keeps the comment, so the in-flight detail reads `missing: ~/.config/hypr/gkeep.conf extra: ~/.config/hypr/gkeep.conf # gkeep notes`.

This fails closed, which is acceptable per FixtureDesign U3. The wording, however, tells the operator a present, sourced file is missing.

**Smallest correction** (diagnostic only; verdict unchanged): when an `extra:` member equals a `missing:` member plus a trailing `[[:space:]]#…`, emit a distinct token such as `annotated: <path>`, or quote members (K7). Do not normalize the value into a PASS.

Host count of source lines with `#` after the value: 0.

### K7 — LOW — member naming is not injective

- **Space in a name.** The local census joins names with spaces (`lextra="$lextra $x"`, `:2415`), so `extra: a b.conf` cannot be told apart from two members `a` and `b.conf`.
- **Newline in a name.** A name such as `$'x\ny.conf'` puts a newline in the row detail:
  - the printer's `IFS='|' read -r … <<<"$r"` keeps only the first line, so the name is truncated (status stays FAIL);
  - `--snapshot` refuses the file, because its `row|` line count differs from the total (SnapshotRecon §4).

**Correction.** Render each member with `printf -v q '%q' "$x"` before joining, for all of `missing`, `extra`, and `duplicate`.

### K8 — LOW — the "missing gkeep" C2 case is covered for one of two variants

The installer's idempotency test is a substring check (`/home/vgpnk/Projects/gkeep/install.sh:29`: `if "hypr/gkeep.conf" not in main_text:`). A commented-out `# source = ~/.config/hypr/gkeep.conf` therefore stops re-installation and leaves gkeep unsourced while the file remains.

In-flight result: `include_graph` FAIL "17 source lines (expected 18) missing: ~/.config/hypr/gkeep.conf", and `sources_resolve` FAIL "missing: …". That is correct and named. N4 only deletes the file.

**Correction.** Add the comment-out variant: FixtureDesign N5 with `sed 's#^source = ~/.config/hypr/gkeep.conf$#\# &#'`. Assert `missing: ~/.config/hypr/gkeep.conf` on `include_graph` and `local.inventory` PASS.

### K9 — INFO — the mutation kill paths narrowed but hold

- **D7** (`-ne`→`-lt`, recorded at `:1456-1458`):
  - Under H, 19 is not less than 18, so the walk runs over `EXPECT` indices only and `miss` stays empty. `include_graph` PASSes, and H's `st_row_has … include_graph FAIL` kills the mutant.
  - H's exit, DIVERGED, and no-CLEAN assertions **no longer kill D7**. The new `sources_resolve` `extra:` FAIL keeps exit at 1.
  - The kill now rests on one assertion. Keep it, and do not weaken H to status-only on other rows.
- **D6** (xdph dropped): A now FAILs with `extra: xdph.conf`, so the mutant is killed.
- **New logic has no recorded mutant.** Examples: deleting the `lextra` loop, or the `got`-side `extra:` loop. N1/N3 would kill these, but `TABLE_MADO` does not record them. Adding them is L1's call (spec/SHA provenance); do not edit silently.

## 3. Checked and not a finding

- **Whitespace and CRLF.** The `awk` `[[:space:]]` includes `\r`; the probe gave `source = ~/a.conf\r` → `[~/a.conf]`. Leading space, tab, and no-space `source=` forms are all handled by the shared regex. The orchestrator and the extraction use the same `source[[:space:]]*=` regex, so there is one authority.
- **Locale.** `LC_ALL=C` is exported at `:75`. The in-flight census uses only builtins (associative arrays and a glob), with no `comm`, `join`, or `sort`. The restricted-PATH sandboxes in scenarios C, E, and F, which lack `comm`, cannot turn it fail-open.
- **Empty local glob.** Without `nullglob`, the literal `$H/*.conf` is filtered by `[ -f ]`, so no bogus member appears.
- **Backups.** `*.conf` does not match `hyprland.conf.bak.1792267376` or `autostart.conf.bak.1791942509`.
- **Case changes and path-equivalent rewrites** (`Gkeep.conf`, `//`, `./`, an absolute `/home/vgpnk/...`, `$HOME`, `~user`) all fail closed through literal equality. That is acceptable per FixtureDesign U1/U2/U9.
- **Host set equality.** The read-only `ls` of `~/.config/hypr` shows 13 `*.conf` files: the 12 MADO-1 names plus gkeep. That equals `LOCAL` after `:2403`. The 18 root `source` lines match `EXPECT` in order, so the live verdict is not moved by K1–K8 corrections.

## 4. Smallest safe correction set (for GateImplement or L1, priority order)

1. **K2.** Guard empty `got` members before the associative-array inserts at `:2338` and in the `tseen` loop. Add a hermetic case. This blocks a regression versus baseline.
2. **K1.** Make the orchestrator FAIL on `^[[:space:]]*#[[:space:]]*hyprlang`. Add a hermetic wrap case.
3. **K3.** Count members instead of collapsing them to a set (`$(( ${m[$k]:-0} + 1 ))`), never `unset "m[$k]"`, name `duplicate:`, and drop "set exact" from any PASS that is not multiset-exact.
4. **K4/K8.** Add the order-swap and gkeep comment-out hermetic cases.
5. **K5.** Use `-f` for literal targets and require ≥1 regular-file glob match.
6. **K6/K7.** Quote members with `%q`. Optionally add an `annotated:` token. These are diagnostic only.

Use the same N-scenario token predicates for C2 scoring. Under "row FAIL" alone, baseline already detects 3 of 4 (AttackClaims A2, ReviewCensus F6).

## 5. Sources opened (accessed 2026-10-20)

| ID | URL | Quote (≤25 words) + location | Revision | Tier | Admission / flip |
|---|---|---|---|---|---|
| S-a | https://wiki.hypr.land/0.56.0/Hypr-Ecosystem/hyprlang/ | "Comments are started with the # character." (§Comments); "You can make blocks conditional by using the # hyprlang if directive." (§Conditionals, "Since 0.6.4") | wiki v0.56.0, `article:modified_time` 2026-03-31T19:16:43-04:00 | A (official docs) | **Admitted** as documented syntax for K1 and K6. Flips if host hyprlang < 0.6.4; installed is `hyprlang 0.6.8-5` (`pacman -Q`). |
| S-b | https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp | `if (!impl->currentFlags.ifDatas.empty() && impl->currentFlags.ifDatas.back().failed) return result;` (`CConfig::parseLine`, ~L683); `newIfData.failed = !negated;` (`parseComment`, ~L605) | tag v0.6.8 → commit `3a1c1b25b059dae2c6bbc46991562ba1158d125c` | A (primary code, installed version) | **Admitted** for K1 (undefined variable → block skipped, before any handler) and K6 (cut at first unescaped `#`, ~L688-702). Flips if Hyprland's legacy loader bypasses `parseLine` for `source` lines; S-c registers `source` as a hyprlang handler (`registerHandler(&::handleSource, "source", …)`, ~L614). |
| S-c | https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/config/legacy/ConfigManager.cpp | `Log::logger->log(Log::WARN, "source= skipping directory {}", value);` (`handleSource`, ~L1844); `if (rawpath.length() < 2) {` … `"source= path garbage"` (~L1803-1805) | tag v0.56.2 → commit `efb50993780079460b0cbed1363e2166a2de1d9f`. Matches the host `hyprctl version` commit `efb5099…` recorded at `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/executor-test-sufficiency.md:94`. | A (primary code, host build) | **Admitted** for K2 (empty path is an error), K5 (directory skipped with a warning, no error), and the glob/`GLOB_TILDE` behavior (~L1816-1817, "found no match"). Flips if the installed binary differs from the tag (pacman `hyprland 0.56.2-2`). |
| S-d | https://wiki.hypr.land/0.51.0/Configuring/Keywords/ | "Use the source keyword to source another file. Globbing is supported" (§Sourcing (multi-file)) | wiki v0.51.0, modified 2025-09-12T13:57:40+02:00 | A | **Rejected** as a host-version authority: it describes 0.51 while the host runs 0.56.2, and the 0.56.0 configuring pages no longer carry the keyword. Superseded by S-c code. Flips only if S-c becomes unavailable. |

Local evidence (read-only, 2026-10-20):
- `ls -la ~/.config/hypr`: 13 `*.conf` + 2 `.bak.*`.
- `grep -n source ~/.config/hypr/hyprland.conf`: 18 lines, in `EXPECT` order.
- Root shape counts: `hyprlang` directives 0, inline `#` after a source value 0, empty `source =` 0.
- `/home/vgpnk/Projects/gkeep/install.sh:21-36`: substring idempotency check.

## 6. Addendum — dispositions from GateImplement (2026-10-20, code-read of `tools/mado-verify.sh` tag 57C6)

| Finding | Disposition | Critic check |
|---|---|---|
| K1 | Fixed: orchestrator FAIL `unsupported hyprlang directive at line N` (`:2322-2326`), hermetic N8 (`:1152-1168`) | Confirmed. The regex equals the hyprlang trigger. N8 inserts after line 13, so T3 is safe. It also fails `# hyprlang noerror` (fails closed). |
| K2 | Fixed: empty members guarded in all four `got` loops (`:2379-2386`, `:2410-2428`) and named `extra: ''`; N7 (`:1135-1150`) | Confirmed. No `unset` by key, no evaluation of names. |
| K3 | Residual R-2 (duplicate naming optional per planner) | Partly disputed. `include_graph` PASS needs an equal count plus the positional walk, so it is not multiset-blind. `sources_resolve` PASS (`:2429-2430`) has no count condition. With one duplicated declared line it reads PASS "18/18 targets exist, set exact" while `include_graph` FAILs, so the verdict stays DIVERGED. The wording on that row is wrong. Smallest fix: add a count clause to `tset`; scenario A's assertion is unchanged. Otherwise R-2 must name this. |
| K4 | Residual R-3 (outside the four predeclared cases) | Accepted as a residual. Order remains without a hermetic negative case. |
| K5 | Residual R-1 (regular-target validation excluded by the planner) | Accepted as a residual. A directory target still reads PASS at Hyprland v0.56.2 (§5 S-c). |
| K6/K7 | Source members are single lines by awk; local names go through `printf %q` (`:2468`, `:2474`) | Accepted. |
| K8 | Already caught (count FAIL + `missing: ~/.config/hypr/gkeep.conf`); no fixture added | Accepted. The behaviour is detected; this variant has no hermetic case. |

**K3 closure (2026-10-20, `tools/mado-verify.sh` tag CB7A):** the `sources_resolve` PASS text now reads `declared targets exist, member set exact` (`:2431`; A assertion `:932`). It no longer claims a count, so a duplicated declared line cannot make the text false. Multiplicity is owned by `include_graph` (count + positional walk). The wording dispute is closed. Duplicate *naming* stays residual R-2. Stale copies of the old PASS text remain in peer drafts, not gate bytes: `w1/reports/GateImplement.md:210`, `w1/FixtureDesign.md:140`, `w1/CensusRecon.md:228`. L1 should not use those as expected output.
Correction: `w1/reports/GateImplement.md` is now byte-identical to `w1/GateImplement.md` (md5 `6b658f73…`), and its line 210 has the new text. My earlier read predated that sync, so only `FixtureDesign.md:140` and `CensusRecon.md:228` remain stale. Final gate sha256 `784c4e90ef25cce79773c89ef23c2396bf4dec155ddba34deb5cf22e66269081`.
