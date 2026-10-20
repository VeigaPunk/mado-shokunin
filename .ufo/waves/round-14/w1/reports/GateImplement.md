# GateImplement — regular-file source targets (round 14, M14)

Seat: `MadoR14.GateImplement` (leaf executor). Owned file: `tools/mado-verify.sh`.
No builds, lint, tests, formatters, smoke runs, or gate executions were performed.
No commits, no host writes, no routing changes, no external sources opened.

## 1. Files changed

| Path | Change |
|---|---|
| `tools/mado-verify.sh` | source resolver requires every declared target to be a regular file (`-f`, follows file symlinks); non-regular direct targets and glob matches are named under `non-regular:` on `hypr.root.sources_resolve`; NUL-delimited glob transport; `src_disp()` helper; selftest helper `st_row_exact()`; fixtures N9–N16; header invariant + round-14 recut note |
| `.ufo/waves/round-14/w1/GateImplement.md` (this file) | advisory findings |
| `.ufo/waves/round-14/w1/reports/GateImplement.md` | identical rendered copy (both paths named by the assignment) |

Untouched: `PIN_MADO='87910c39…'` (`:1639`), `SPEC_SHA`, `TABLE_MADO`, the recorded
`mado_r7_spec_write` body and its D6 anchors, every file outside the owned path.
Working-tree check: `git status --porcelain -- tools/mado-verify.sh` → ` M tools/mado-verify.sh`
only; HEAD `873ff08`, delivered file sha256
`ef50e262f311d74e05afd558883415d2f47fa2a0247a0c834e37f49cb60c742b` (3,711 lines).

## 2. Behavior landed

Owner row and id are unchanged: `hypr.root.sources_resolve`. PASS text is unchanged:
`declared targets exist, member set exact` — the clean fixture A assertion still holds.

### 2.1 Direct target (`tools/mado-verify.sh:2672-2676`)

- Test is `[ -f "$x" ]`; `-f` dereferences a symlink, so a link to a regular file passes.
- If `-f` is false and `-e` is true (directory, link-to-directory, FIFO, socket, device node),
  the target is named under `non-regular:`. A path that does not exist — including a dangling
  symlink (`-e` false) — keeps the pre-existing `unresolved:` class.
- `-e` is no longer a pass predicate; it only distinguishes "exists but is not a regular file"
  from "does not resolve".

### 2.2 Glob target (`tools/mado-verify.sh:2639-2671`)

- Branch order: glob detection (`case "$x" in *'*'*)`) runs before the direct predicate.
  Only `*` is glob grammar — `?`/`[…]` remain literal, as before.
- Matches are collected NUL-delimited from a nullglob expansion in a subshell:
  `mapfile -d '' -t gmatch < <( shopt -s nullglob; IFS=; gsub=( $x ); printf '%s\0' … )`.
  Nullglob and empty IFS are scoped to that subshell; no shell option leaks. The transport is
  not line-oriented, so a filename containing a space or a newline stays one member (the
  previous `compgen`/`mapfile -t` transport split a newline name into phantom members).
- Zero matches → `unresolved:` (existing class, existing declared-name form).
- Every match is tested with `-f`; each non-regular match is named under `non-regular:`.
  A mixed set names only the non-regular member(s), so a valid `*.conf` beside a
  directory-shaped one is never refused.
- A matched dangling symlink is `unresolved:` (it does not resolve), not `non-regular:`;
  the declared token is appended once per glob however many matched links are broken
  (ReviewResolver pass-2 R2), so the detail never repeats the same source line.

### 2.3 Diagnostics

- FAIL detail order: `unresolved: …`, then `non-regular: …`, then the unchanged
  `missing: …` / `extra: …` set members. Token is exactly `non-regular:` (space after the
  colon), per the parent decision; ReviewResolver's `nonregular:` was non-normative.
- Names use the declared `~` form. `src_disp()` (`:225-231`) strips `ROOT` and prints the
  suffix with `%q`, so a whitespace path stays one unambiguous token; `~` is emitted before
  the quoted suffix (`printf '~/%q'`).
- `st_row_exact()` (`:424-429`) compares the **whole owning-row detail**, not a substring:
  pass-2 F1 (mixed-glob absence) and F2 (N4's `unresolved:` class) are asserted as equality,
  so a regular glob member or an extra token cannot hide in the detail.
- Exact-set membership (`missing:`/`extra:`), positional order (`include_graph`'s job),
  the empty-member guard, and the read-only fence are unchanged. The resolver reads path
  metadata only and never opens, writes, or hashes a target.

## 3. Selftest fixtures (hermetic, isolated)

All build on fixture A and touch only the declared shape; each asserts exit, verdict, the
owning row, isolation rows and counts. The all-directory glob's collateral row is asserted
by its own status, never assumed clean. The four pass-1 cases are N9–N12; pass-2 adds
N13–N16.

| Case | Mutation | Asserted |
|---|---|---|
| N9 `:1202` | `~/.local/share/omarchy/default/hypr/windows.conf` replaced by a directory (default tree; no local-census or theme part reads it) | exit 1, DIVERGED, whole owning-row detail `non-regular: ~/.local/share/omarchy/default/hypr/windows.conf`, no `unresolved:`, `include_graph` PASS, `local.inventory` PASS, exactly one hypr FAIL |
| N10 `:1224` | `toggles/hypr/window-no-gaps.conf` replaced by a directory → the toggle glob's only match is a directory | exit 1, DIVERGED, whole detail `non-regular: ~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf`, no `unresolved:`, `include_graph` PASS, `local.inventory` PASS, `hypr.toggle.no_gaps` **NOTE** (asserted collateral: its `-f` path reads a non-file as absent), exactly one hypr FAIL |
| N11 `:1249` | regular `window-no-gaps.conf` kept, directory `dir.conf/` added beside it (mixed match set) | exit 1, DIVERGED, whole detail **equals** `non-regular: ~/.local/state/omarchy/toggles/hypr/dir.conf` — the regular member cannot appear anywhere in the detail, no `unresolved:`, `include_graph` PASS, `hypr.toggle.no_gaps` PASS, exactly one hypr FAIL |
| N12 `:1268` | same members, order swapped: `monitors.conf` ↔ `input.conf` (file lines 14/15; theme anchor line 13 does not move) | exit 1, DIVERGED, `include_graph` FAIL with `line 11: got '~/.config/hypr/input.conf' want '~/.config/hypr/monitors.conf'`, `sources_resolve` PASS exact member set, `local.inventory` PASS, `theme.chain.hypr_include` PASS, exactly one hypr FAIL |
| N13 `:1300` | `windows.conf` replaced by a symlink to the regular fixture `envs.conf` (positive control for the link rule) | exit 0, CLEAN, whole detail `declared targets exist, member set exact`, `include_graph` PASS, `local.inventory` PASS |
| N14 `:1316` | the toggle glob matches nothing (`window-no-gaps.conf` removed, no replacement) | exit 1, DIVERGED, whole detail `unresolved: ~/.local/state/omarchy/toggles/hypr/*.conf`, no `non-regular:`, `hypr.toggle.no_gaps` NOTE, exactly one hypr FAIL |
| N15 `:1333` | the toggle file replaced by a dangling symlink matching the glob | exit 1, DIVERGED, whole detail `unresolved: ~/.local/state/omarchy/toggles/hypr/*.conf` (exactly once, never `non-regular:`), `hypr.toggle.no_gaps` NOTE, exactly one hypr FAIL |
| N16 `:1350` | a regular glob member whose name contains a newline (`line\nbreak.conf`) beside the real toggle | exit 0, CLEAN, whole detail `declared targets exist, member set exact`, `include_graph` PASS, `hypr.toggle.no_gaps` PASS |

N4 (`:1141`) also now asserts the whole detail
`unresolved: ~/.config/hypr/gkeep.conf` (pass-2 F2): a mutant that drops the `unresolved:`
label is killed rather than passing the path-substring check.
N12 is framed as a regression guard for the already-working order/set split — **not** new
detection and not a coverage improvement claim. N10's `no_gaps` NOTE is a status change of
an unrelated row in that fixture only; it is asserted, not counted as clean baseline.

## 4. Symlink policy (explicit)

- File symlink → accepted (`-f` dereferences).
- Symlink to a directory → `non-regular:` (direct: declared `~` name; glob: matched name).
- Dangling symlink → `unresolved:` (direct and glob match); the class is shared deliberately,
  so a broken link cannot pass as a match and the declared line is named once.
- Symlink loop → resolves as dangling under `-f` → `unresolved:`.
- Containment is not checked (any regular target path is accepted); that is the stated
  policy, not an inferred sandbox. No target content is read; the policy is metadata-only.

## 5. Exact verification (for L1; not run here)

1. `bash tools/mado-verify.sh --selftest`
   - Before the pin recut: the derived regression target moves (all edits sit outside the
     excised R7/R8 marker regions), so `R10: derived target equals the recorded gate revision`
     is expected red and `--regression` reads SETUP. This was already true from round 13
     (pin owed); it is not a new behavioral failure and `PIN_MADO` was not edited.
   - New behavioral assertions: N9–N16 must pass with the statuses above; A/B/H/N2/N4/N7
     remain as recorded (N4 now stronger).
   - Do not treat R10 red as a reason to edit the pin here; L1 owns the measured recut.
2. `git diff -- tools/mado-verify.sh` — confined to: header invariant, `src_disp`,
   `st_row_exact`, N9–N16, the round-14 recut record, the resolver block.
3. Mutation anchors (`MadoR14.MutationDesign`; no mutation run here):
   RT1 direct `-f`→`-e` (N9 loses its FAIL); RT2 unconditional glob `continue` (N10/N11 lose
   `non-regular:`); RT3 inverted per-match guard (N11's exact detail names the wrong member);
   RT4 dropped `unresolved:` label (N4's exact detail fails). All four must be killed.
4. Read-only live spot check, if wanted: `bash tools/mado-verify.sh --no-live`. No overall
   verdict/FAIL-count change is claimed: the live `~/…/windows.conf` and toggle glob are
   regular files today, and the directory cases exist only in hermetic fixtures. This change
   adds detection, not a global clean baseline; other live rows remain whatever they were.

## 6. Outside R13 rulings

- **R13-V1 retained data:** no retained-data wording is introduced or changed. The resolver
  retains no target bytes; it reads metadata only. No session/identity data is touched.
- **R13-V2 within-run boundary vs revision-output equality:** this change makes no
  cross-revision output claim. `boundary.readonly` remains a within-run before/after equality;
  the type check is a single observation inside one run. Combined config digests across
  receipts are not equated, and the PASS detail that downstream records cite is unchanged.
- **R13-V3 standalone receipt measured digest:** no receipt is produced or claimed here.
  Because the gate bytes moved, any new snapshot receipt would carry a new `gate-sha256` by
  construction; that is provenance, not a re-cut of `PIN_MADO`. The round-13 standalone
  `gate-selftest.txt` binding remains outside this seat and is left unedited.

## 7. Risks / blockers

- `R10` red and `--regression` SETUP until L1 completes the measured re-cut of `PIN_MADO`
  and `TABLE_MADO`; intentional, per contract.
- Pre-existing and retained (out of scope): glob detection recognizes only `*`; a `ROOT`
  containing `*`, `?` or `[` can misroute a direct target into the glob branch
  (ReviewResolver F8/F9). No fixture root has metacharacters.
- `boundary_hash()` (`:237-245`) is called only on `$ROOT/.config` (`:2516`, `:2954`; `C` set at
  `:3668`), so the N16 newline file under `.local/state` is outside the proof: it is neither
  read nor skipped, and no stray `sha256sum` stderr is produced. Latent, unexercised Low: the
  same `find … | while read -r f` path would split a newline-named file under `.config`
  itself (pre-existing, unchanged, not reached by any fixture).
- No execution was permitted, so `-f`/`-e`, nullglob expansion and `printf '%s\0'`/`mapfile -d ''`
  semantics are reasoned from bash, not observed in this seat's session — N9–N16 are the
  red-before/green-after evidence L1 will actually measure.
- Tooling installs/updates: none.

## 8. Coordination retained

- Parent decisions applied: `non-regular:` token; direct fixture at the default-tree
  `windows.conf`; all-directory glob asserts the `no_gaps` NOTE; order swap uses two
  regular members away from line 13; NUL-delimited glob transport; pass-2 F1–F4 additions.
- `ReviewResolver` pass 2 (on the prior revision) closed F1–F7/F11; R2 (duplicate dangling
  token) is fixed by the single `gdang` append. Its carried Low F8/F9 remain documented.
- `ParserIntent`'s class split (reorder → `include_graph`; type/resolution →
  `sources_resolve`) is preserved. `MutationDesign`'s RT1/RT2 anchors exist byte-exact and
  RT3/RT4 are covered by N11/N4 exact-detail assertions.
