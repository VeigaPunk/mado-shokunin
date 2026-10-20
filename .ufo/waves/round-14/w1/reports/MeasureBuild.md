# MeasureBuild — round 14 / W1

Axes: **coverage** (C1 sourced U1–U7 joins) and **operability** (C2
directory-shaped source targets). Delivery is the revision-bound counter,
not a run: `python3 .ufo/waves/round-14/measure.py <revision>`.

## Files changed

- `.ufo/waves/round-14/measure.py` — new counter (the only implementation file).
- `.ufo/waves/round-14/w1/MeasureBuild.md` — these findings.
- `.ufo/waves/round-14/w1/reports/MeasureBuild.md` — rendered report (same content).

No other path was written. `tools/mado-verify.sh`, `corpus/SOURCES.md`,
`corpus/knowledge/` and all host/sibling state are untouched. No tool was
installed or upgraded.

## Revision binding and input digests

- `REPO = Path(__file__).resolve().parents[3]` resolves to the lane root for
  `.ufo/waves/round-14/measure.py`.
- The named revision is resolved once, before any input read:
  `git rev-parse --verify <rev>^{commit}`. Both the supplied name and the
  resolved commit SHA are printed (`revision`, `revision_sha`); every
  repository input is fetched at that SHA — `git show <sha>:<path>` for
  `corpus/SOURCES.md`, each knowledge note and `corpus/README.md`, and
  `git ls-tree <sha>` for the knowledge path list — including the measured
  `tools/mado-verify.sh`.
- `measure_inputs.gate_sha256` is the SHA-256 of the exact gate bytes written
  to the private temp and executed. The report can therefore name the
  revision output and the measured gate, not assume either.
- The gate text is written to a private `TemporaryDirectory`; its own
  `build_fixture()` is sliced between the named markers `build_fixture() {`
  and `\nselftest() {` and appended to a builder that calls
  `build_fixture "$1"`. A missing marker is a SETUP refusal, not a silent
  0/3.
- Each fixture is a fresh temp tree. The gate is invoked only as
  `bash <temp>/gate.sh --root <temp/tree> --no-live`; the host `$HOME` is
  never a root, no live verb runs, and no substrate is read or written.

## C1 — sourced U1–U7 joins + navigation

Admission predicate per `corpus/knowledge/*.md` note (head-15 header only):

1. `^source:` line with at least one `S\d{3,}` ID;
2. exactly one `^covers: (U[1-7])$`;
3. `verified-at:` and `recheck:` non-empty;
4. at least one cited row whose registry `status` is `mined` **and** whose
   `used-by` cell names that note path;
5. at least one such row is tier A or B;
6. U4 keeps its round-13 body facets (phase `S005`, advertisement `S041`,
   unexercised behavior `S043`);
7. U5 adds the decision sections and reciprocity below.

Registry shape is the existing 11-column contract (`cells[1]` id,
`cells[4]` tier, `cells[8]` status, `cells[11]` used-by); no new column is
assumed.

### U5 decision sections (stable heading markers)

Each marker is a level-2-or-deeper heading whose text begins with the named
phrase, case-insensitive; a trailing qualifier is tolerated. Sections are
built by walking the note once:

| Facet key | Required marker |
|---|---|
| `output_management` | heading begins `Output management` (or `output-management`) |
| `colour` | heading begins `Colour management` (or `Color management`) |
| `feature_unknown` | heading begins `Unexercised feature behavior` (or `behaviour`), and that section or its heading contains `[UNK]` |

All three must be true; a prose mention without the section heading does not
admit the item. The note's own decision tables live inside those sections and
are not pattern-copied, so column names and verdict sentences stay free.

### U5 reciprocal mined S047/S048 (reserved)

Both reserved IDs must independently satisfy, for the same note:

- cited on the head-15 `source:` line (the ID extraction source);
- present in the registry with `status == mined` and tier A or B;
- `used-by` contains `corpus/knowledge/<slug>.md`;
- inverse direction: every mined registry row whose `used-by` names the note
  is also cited on that head-15 source line (round-13 J4 reciprocity), so a
  row cannot be attached by `used-by` alone. The planned reuse of S041 must
  therefore appear on the note's source line too.

`u5_candidates[]` prints facets, per-reserved reciprocity and the inverse
boolean for every structurally admissible `covers: U5` note, so a near miss
is measured rather than hidden either way.

Score: `10 * covered_items / 7`, rounded to four decimals. Baseline at the
round-14 base revision is 4/7 = **5.7143** (U1–U4), predicted target after a
compliant U5 note is 5/7 = **7.1429**. No note was authored here.

### Navigation

Unchanged from round 13: every `corpus/knowledge/*.md` basename must appear
exactly once as a README index row matching `^\| \`knowledge/<slug>.md\``;
`missing`, `extra` and `duplicates` are printed. This is the existing
maintained census, not new evidence.

## C2 — directory-shaped direct and glob source targets

Each case starts from the measured revision's own `build_fixture()`; only
the named path is mutated, then the gate runs with `--root <tree> --no-live`.

| Case | Exact mutation path | Affected basename |
|---|---|---|
| `direct-directory` | `~/.local/share/omarchy/default/hypr/windows.conf` — unlink the regular file, mkdir a directory at the same path | `windows.conf` |
| `all-directory-glob` | `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf` — unlink, mkdir; the toggle glob `*.conf` then matches only a directory | `window-no-gaps.conf` |
| `mixed-glob-directory` | keep the regular `window-no-gaps.conf`, add directory `~/.local/state/omarchy/toggles/hypr/dir.conf` beside it | `dir.conf` |

`windows.conf` was selected before any baseline as the direct case because
no other gate row reads it: `hypr.local.inventory` scans only
`~/.config/hypr/*.conf`, `hypr.root.include_graph` reads only
`hyprland.conf` source lines, and the toggle row reads only the toggle
path. The direct case therefore isolates the owning resolver row instead of
being co-detected by the local census. This is rubric selection before
baseline, not a reroll after a measurement; no measurement was run.

Detection per case requires **all** of:

- `overall_exit == 1`;
- the sole `FAIL` row in the whole run is `hypr.root.sources_resolve`
  (exactly one FAIL row and its id is the owning row);
- exactly one `hypr.root.sources_resolve` row (a missing or duplicated row
  throws a setup error, it does not score);
- that row's status is `FAIL`;
- its `non-regular:` clause, parsed from the marker to the next
  `missing:`/`extra:` class, equals exactly `[expected display path]` — a
  basename appearing anywhere else, or a second member in the clause, does
  not pass;
- its detail contains no `unresolved:`, `missing:` or `extra:` class (the
  set stays exact and the target exists as a non-regular object);
- `toggle_no_gaps` has the expected status: PASS for `direct-directory` and
  `mixed-glob-directory`, NOTE for `all-directory-glob`;
- `mixed-glob-directory` only: its detail must **not** contain the regular
  member `window-no-gaps.conf` anywhere (full-string absence, not a prefix
  exclusion). The row may refuse `dir.conf` while still naming the regular
  toggle; that row does not count;
- the same mutation in a second private root reproduces the owning detail
  byte-identically (`replica_detail == sources_resolve`). The replica
  substantiates stable display-path diagnostics; it is not a fourth scored
  case and does not change the denominator.

The per-case result exposes the predicate parts and side rows, so a
collateral status is never described as "all rows unchanged":
`non_regular_members`, `clause_equals_expected`, `clean_classes`,
`absent_token`/`absent_satisfied`, `fail_row_ids`/`sole_fail_resolver`,
`toggle_expected`/`toggle_status_ok`, `replica_detail`/`detail_stable`,
plus the side rows below.

- `include_graph` (order/set) — expected PASS because the source lines are
  untouched;
- `local_inventory` — expected PASS for all three cases;
- `toggle_no_gaps` — PASS for direct and mixed; **NOTE** for
  `all-directory-glob`, because the toggle path is no longer a regular file.
  This side status is printed and must be read as collateral, not as a
  second FAIL.

Score: `10 * detected / len(cases)`, rounded to four decimals; the
denominator is the scored case list of three, and the loop refuses to
continue unless the built case count equals the declared specs. The
second-root replica is a condition on each case, not a fourth case.
`overall_failing_runs` is printed separately. Each mutation is
post-asserted (directory exists and is not a regular file); the order-swap
indices must be distinct and the post-write lines are re-read to refuse a
silent `str.replace`-style no-op. Any gate exit outside 0/1 throws
(usage/setup is not a case result), as does a missing or duplicated owning
or control row.

### Preservation controls (outside the score)

- `clean`: unmodified fixture. Requires `overall_exit == 0` and
  `sources_resolve` PASS with the exact-set detail.
- `order_swap`: swap the two user source lines for `monitors.conf` and
  `input.conf`. Requires `overall_exit == 1`, `hypr.root.include_graph`
  FAIL naming `line `, and `sources_resolve` PASS with no `non-regular:`
  token. This is the existing exact-set/order behavior; the counter reports
  it but awards nothing, so an already-working property is not claimed as a
  round-14 improvement.
- `symlink_to_regular`: replace `default/hypr/windows.conf` with a symlink to
  the regular `looknfeel.conf` in the same directory. Requires the link to
  resolve (`is_file()`), `overall_exit == 0`, `sources_resolve` PASS and no
  `non-regular:` token. It asserts only that symlinks to regular files stay
  accepted; it broadens no admission and awards no point.
- `newline_regular`: add a second regular toggle named `new\nline.conf`
  (literal newline in the basename) beside `window-no-gaps.conf`. Requires
  `overall_exit == 0`, `sources_resolve` PASS and no `non-regular:` token,
  i.e. the glob transports one regular member rather than splitting it. This
  is an unscored guard for the gate's F6 newline-glob transport fix, not new
  detection; it does not alter the three scored cases.
- `ai_usage_directory_overlap`: the original overlap candidate — a directory
  in place of `~/.config/hypr/ai-usage.conf`. Recorded only: the owning row
  should name `~/.config/hypr/ai-usage.conf` and `hypr.local.inventory`
  should also speak (`missing: ai-usage.conf`). This is why it was replaced
  as the scored direct case; it earns no point and cannot add to the
  denominator.
- `direct_missing`: delete `default/hypr/windows.conf` with no replacement.
  Requires exit 1, `unresolved:` naming the target, and no `non-regular:`
  token — the pre-existing error class is not repurposed.
- `zero_match_glob`: delete `window-no-gaps.conf` and leave the toggle dir
  empty. Requires exit 1, `unresolved:` naming the glob target, and no
  `non-regular:` token, with the toggle row NOTE.

Expected readings `[INFERENCE]`, not executed: at a gate with the
round-14 regular-file check and newline transport, each case should be
exit 1 with only the owning resolver row FAIL, all seven controls as above,
and the all-directory toggle row NOTE. At the pre-round-14 gate the
scorecard predicts 0/3 (directory accepted by `-e`/`compgen -G`); the first
run at the measured revision records the actual values.

## Boundary corrections (R13-V1..V3) and non-claims

- **R13-V1 retained-data wording.** This counter reads no retained session
  capture (`globals.json`), no environment, titles, device/output identity
  or session material. Advertisement evidence and its wording stay with the
  U5 sources/scribes; no retained-data claim is made here.
- **R13-V2 within-run boundary vs revision-output equality.** Inputs are
  fetched by resolved commit SHA and the gate digest is printed; fixtures
  exist only inside one run's private temp directory. The counter does not
  claim that a working-tree run equals the revision output, nor that two
  revisions produce equal bytes.
- **R13-V3 standalone receipt measured digest.** No receipt is produced or
  digested here; `measure_inputs.gate_sha256` binds only the measured gate.
  The standalone receipt digest remains ReceiptBuild's deliverable.
- No feature exercise, no compositor/protocol client call, no source-row
  admission, no knowledge note, no gate edit.

## Risks / dependencies

1. **U5 heading wording.** The parent-declared note uses
   `## Output management`, `## Colour management`,
   `## Unexercised feature behavior` and `[UNK]` in the last section. The
   matcher tolerates case, `colour`/`color`, `behavior`/`behaviour` and a
   trailing qualifier, but a differently named heading measures as uncovered
   instead of being silently counted.
2. **Exact clause equality.** Each scored row's `non-regular:` clause must
   parse to exactly one member equal to the expected `~` display path. A
   pattern-only clause, a root-prefixed path, a spurious extra token, or a
   second refused member scores 0 even when the class word is present.
3. **Collateral toggle status.** `all-directory-glob` flips
   `hypr.toggle.no_gaps` PASS→NOTE. The score reads only the owning row and
   overall exit; the NOTE is reported, not counted, and not called a
   regression.
4. **Mixed-row pollution.** The mixed case refuses a PASS if its detail
   names the regular `window-no-gaps.conf` anywhere, even when the correct
   `non-regular: .../dir.conf` is present. A row that names both members is
   substring-passing but member-blind and scores 0 by design.
5. **Newline transport.** `newline_regular` depends on the gate's F6 fix;
   it is unscored, so a pre-F6 gate records `regular_member_transported:
   false` without changing 0/3 or 3/3 on the three scored cases.
6. **Replica stability.** A gate whose diagnostic leaks the fixture root, or
   varies with the temp prefix, fails `detail_stable` and loses that case
   even when the class word and members are right.
7. **Not run.** Per assignment, syntax/behavior was not executed; baseline
   and control values remain predictions until L1's post-wave gate run.
