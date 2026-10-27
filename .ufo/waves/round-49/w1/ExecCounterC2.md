# ExecCounterC2 — C2 counter draft (round 49, w1 BUILD)

STATUS: complete. Draft `c2-r49-bind-entry.py` at `.ufo/waves/round-49/w1/ExecCounterC2/`
(sha256 `a2e91724ffca3b151f732047dfcb4d4aa76c3c554edd78ecfca2344f44b4ce04`, 52,720 B,
`receipts/digests.txt:2`). It misses at the round base (`admitted=0/1`, `clause=a entry_absent`), admits a
real-bytes POS tree built from the actually fetched Hyprland/libxkbcommon pins plus a live `hyprctl` capture
(`admitted=1/1`, all eleven clauses 1), and of 31 configured runs 3 admit: the POS, one declared residual
(`pin-and-file`) and one name-agnostic check (`receipt-renamed`); 26 miss on the attacked clause and 2 are
setup refusals. Nothing in the lane was written; no lane tool, counter or gate was run; no frozen instrument
was scored; no tool was installed.

## Files

- `.ufo/waves/round-49/w1/ExecCounterC2/c2-r49-bind-entry.py` — the draft (from
  `quality/counters/c2-r48-xkb-entry-v2.py`).
- `.ufo/waves/round-49/w1/ExecCounterC2/controls/mkpos.py` — POS tree builder (computes every locator by line
  scan; writes only inside the scratch clone passed as `--repo`).
- `.ufo/waves/round-49/w1/ExecCounterC2/controls/mutate.py` — one named mutation per control (26).
- `.ufo/waves/round-49/w1/ExecCounterC2/controls/run_controls.sh` — the matrix driver (`POS_REV` pinned).
- `.ufo/waves/round-49/w1/ExecCounterC2/receipts/` — `controls.txt` (31 runs, full output),
  `pos.txt`, `base.txt`, `lane-base.txt`, `lane-tip.txt`, `getoption.json`, `digests.txt`, and the retained
  POS text `pos-entry.md` (sha256 `a7f3cd22…`), `pos-rows.md` (S352-S355), `pos-receipt.txt`,
  `pos-rematerialised.txt`.
- `.ufo/waves/round-49/w1/ExecCounterC2.md` — this report.

No tracked lane file, no `quality/counters/` file, no `corpus/` file and no index was edited. Scratch
`/fast/scratch/hyaku/mado-r49/ExecCounterC2` (clone, pins, capture, mutants) is deleted after the receipts were
copied; `digests.txt` names every revision the counter was run against.

## The counter

Read-only: every read is `git show REV:path` with ambient `GIT_*` stripped; it fetches nothing and opens no file
for writing (the only writes are the replay's temporary `HOME`/`XDG_*` dirs under `TMPDIR`). Python 3 stdlib
only. Exit 0 iff `admitted=1/1`, 1 on a miss, 2 on a setup failure (unresolved revision, entry present at BASE,
absent or `/tmp` `TMPDIR`, missing `hyprctl`/socket).

Clauses (docstring is the contract; the L1 freezes this):

- **a** ENTRY `corpus/knowledge/hyprland-bind-key-match-r49.md` present at REV, absent at BASE (present at BASE
  is a setup error, exit 2).
- **b** provenance head in the first 20 raw lines: >= 3 distinct `source: S###`, every id >= S352, exactly one
  `verified-at: 2026-10-27` and one `recheck:` (ISO / `NNd` / `on-*`), nothing such outside the window; every
  `S###` in the unfenced entry is a REV row (no ghosts); each head id has exactly one 11-cell Registry row
  (tier A/B/C, kind, `mined`, opened 2026-10-27, valid recheck, used-by ENTRY) and no head id at BASE.
  Landing folded in here (not a separate clause): `corpus/README.md` holds exactly one 3-cell index row for
  ENTRY, no redirect word, naming no other `knowledge/` file, with `S###`/`S###-S###` tokens covering the head.
- **c** every head row pin-bound: a `sha256:<64hex>`, >= 1 `.ufo/waves/round-49/fetch/<path>` receipt named,
  every named pin present at REV mode 100644 with a digest the row records; URLs only `xkbcommon-1.13.2`,
  `v0.56.2`, `0.56.2` or 7-40-hex commits (branch names refused, ref-less refused unless a 40-hex commit and a
  digest are recorded); a URL-less row only as `own-work` with digest+pin; URL path must relate to a pin stem;
  anchor ranges must resolve to the row's own pins and stay in range (or say `whole file`).
- **d** every quote verbatim at its stated range: a backticked/double-quoted span of 2-25 words immediately
  followed by `(<pin>:<a>[-<b>])`, `, <locator>` or ` at <locator>`, locator resolving to a committed fetch pin;
  every pin locator in range and its pin cited by a row **or bound by a row at REV** (a row names that pin path
  and records its digest — so the entry may lean on any row-bound ground, including held round-46 pins, but an
  unbound file in a fetch dir cannot launder a quote; a pin whose sha256 equals a cited pin's sha is the same
  bytes); a quote locator naming a lane document is refused.
- **e** >= 6 numbered steps, and EVERY step carries at least one quote that clause d would verify: a >= 2-word
  (<= 25) backticked/double-quoted span immediately followed by a locator that resolves to row-bound ground and
  that occurs inside the pin at least once within the stated [a,b]. An in-range locator alone is not enough
  (w1/ExecControlsC2 bundle 14: a step locator pointed at the wrong line inside the pin and was admitted).
- **f** the live capture answers it — the interface is spelled out below.
- **g** held S319 byte-equal at BASE/REV, its round-46 pin present with a matching digest, `S319` cited in the
  unfenced entry, and no new row (>= S352 at REV, absent at BASE) repeating S319's (repository, ref, path).
  Other held sources may be reopened with a new scope, as S162/S303/S317 already do for one file (so the real
  entry may re-open `src/config/legacy/ConfigManager.cpp`).
- **h** a `## Limits` section with >= 3 bullets, >= 2 naming a scoped limitation (`not|no|never|outside|held|
  inferred|unknown|[UNK]`).
- **i** `corpus/lessons/round-49.md` exists at REV with a non-empty `## Gate` holding a `**S### admit**` line
  for EVERY new REV row (id >= S352, absent at BASE — C1 rows included), every such row used by this round:
  its used-by cell names ENTRY, or a path that exists at REV and is absent at BASE (the C1 tool, a new
  knowledge entry) — a row whose only consumer is an already-held document is a minted row; the terms
  `xkb_state_key_get_one_sym`, `m_xkbSymState`, `keysym_to_name`, `xkb_keysym_get_name` absent under `corpus/`
  at BASE (grep exit 1) and >= 2 present at REV; and novelty of the body: >= 8 unfenced lines of >= 60 chars
  with at most 5 of the first 40 found verbatim under `corpus/` at BASE, and fewer than 15% of the hashed
  6-word shingles of the unfenced prose already in the base tree's `corpus/knowledge` + `corpus/lessons` text
  (>= 150 shingles). Calibration on this tree: POS 0.010; a one-word-per-nine paraphrase of two held documents
  0.231; a verbatim paste 1.0.
- **r** replay: `TMPDIR` required, `/tmp` refused; `/usr/bin/hyprctl` run with a scratch `HOME`/`XDG_*` (the
  operator's state is never touched), `XDG_RUNTIME_DIR`/`HYPRLAND_INSTANCE_SIGNATURE` inherited: `binds -j`
  must hash to the receipt's raw-JSON digest and re-derive its total and form counts; `getoption
  input:resolve_binds_by_sym -j` must yield the receipt's value. The JSON is never printed.

Clause **f** in detail (the interface the entry seat, the live-capture seat and the L1 must meet): the entry
cites `.ufo/waves/round-49/receipts/<file>`; that receipt is new at REV, 100644, 512 B..256 KiB, carries no raw
binds JSON (`"modmask"`/`"dispatcher"` refused), names `hyprctl binds -j`, records the raw-JSON digest on a
`sha256` line, states the bind total and four form counts that sum to it, carries `Hyprland 0.56.2` with the
pinned commit `efb50993780079460b0cbed1363e2166a2de1d9f` on one line, and states
`input:resolve_binds_by_sym` with `int 0` (or `set false`). The form rule is fixed and re-derived by clause r:
`key` starting `code:`/`mouse`/`switch:` is that form; a bind with an **empty `key` and a non-zero `keycode`**
is `code` (the dump's only trace of a keycode bind — `hyprctl` never prints `code:` in `key`); everything else
is `named`. The entry repeats each value on unfenced lines: version+full commit, the total as `192 binds` or
`binds=192` (a `binds: <n>` form is read as the total), each form count beside its label (`184 named,
0 code:, 6 mouse:, 2 switch:` — label-first `named=184` also accepted), the digest or its first >= 12 hex
beside `sha256`, and the resolve value beside the option name. A drifted count or digest is a miss.

## Evidence

Host capture (read-only, 2026-10-27, `receipts/getoption.json`, `receipts/digests.txt`): `hyprctl binds -j` =
90,401 B, sha256 `9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`, 192 binds — named 142,
code/keycode-carried 42, mouse 6, switch 2, catch_all 0; `hyprctl getoption input:resolve_binds_by_sym -j` =
`{"option": "input:resolve_binds_by_sym", "int": 0, "set": false }`. Every capture in this wave was
byte-identical, and `hyprctl version` reads `Hyprland 0.56.2 ... commit efb50993780079460b0cbed1363e2166a2de1d9f`.

Pins fetched for the POS (commit/tag URLs, sha256 in `receipts/digests.txt`):
`Hyprland-legacy-ConfigManager.cpp` `efb50993…/src/config/legacy/ConfigManager.cpp`
`9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` (2,184 lines);
`Hyprland-KeybindManager.cpp` `…/src/managers/KeybindManager.cpp`
`8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40` (975 lines);
`xkbcommon-keysym.c` `xkbcommon-1.13.2/src/keysym.c`
`123e3390d443b85c9cc9d1833c168ecda955d1c642fda03881052bb99c3369c5` (450 lines). The POS entry's 19 quotes
sit on those lines, with every locator computed by `mkpos.py` (line scan), never typed.

Control matrix (`receipts/controls.txt`, 31 runs; every revision also in `digests.txt`):

| control | rev | mutation | verdict |
|---|---|---|---|
| base-miss | `03e4ae76` | score the round base | rc 1, `a:0` `entry_absent` |
| do-nothing-lane-tip | `5f37c1b8` | score the live lane tip (claims commit) | rc 1, `a:0` `entry_absent` |
| POS | `fe390943` | entry + rows S352-S355 + README row + lesson Gate + receipt + 4 pins | **admitted 1/1**, `a..i,r` all 1 |
| setup-entry-at-base | POS as `--base` | entry present at base | rc 2 `precondition_failed entry_present_at_base` |
| tmpdir-refused | POS with `TMPDIR=/tmp` | a /tmp work dir | rc 2 `TMPDIR under /tmp refused` |
| quote-word | `6e26c139` | one quote word changed | rc 1, **d** `quote_not_in_pin` (only d) |
| range-9999 | `b863b374` | step-1 quote locator `:1481` -> `:9999` | rc 1, **d** `locator_out_of_pin` + `quote_out_of_range` (d; the other quotes keep e green) |
| quote-long | `d40ea865` | quote grown to 30 words | rc 1, **d** `quote_too_long words=30` (only d) |
| paraphrase | `f3de7253` | 2,213-word one-word-per-nine paraphrase of two held docs appended | rc 1, **i** `overlap=0.231` (only i) |
| step-quote | `6b4a0a3c` | step 3's quote locator moved off its line (still in range) | rc 1, **d** `quote_out_of_range` + **e** `step_without_verified_quote` |
| branch-url | `236eaa1e` | row S353 URL ref -> `main` | rc 1, **c** `url_branch_ref` (only c) |
| pin-digest | `bd5d72b7` | row S352 digest replaced | rc 1, **c** `pin_sha_mismatch` + **e** (quotes still ship on bytes bound by a round-46 row) |
| pin-and-file | `9bfa0ef3` | pin bytes extended **and** row digest updated | **admitted 1/1** — declared residual: the committed fetch copy plus the row digest is the trust root |
| held-row-moved | `0f128ab7` | S319 source cell edited | rc 1, **g** `held_row_moved` (only g) |
| held-not-cited | `f83c9766` | `S319` removed from the entry | rc 1, **g** `held_not_cited` (only g) |
| held-rereg | `a3759a85` | new row S356 repeating IKeyboard.cpp at `efb50993` (+ its Gate line) | rc 1, **g** `re_registered_held_url=S356` (only g) |
| receipt-renamed | `65ace76f` | receipt renamed to `binds-shape.txt`, entry citation updated | **admitted 1/1** — the clause is name-agnostic |
| receipt-absent | `8f15ab77` | cited receipt deleted | rc 1, **f** `receipt_missing` + **r** `no_receipt_found` |
| receipt-typed | `bd4027c6` | receipt `mouse=6` -> `7` | rc 1, **f** `receipt_forms_sum …193!=192` + **r** `replay_mismatch` |
| receipt-resolve | `947ff7e8` | receipt `int=0` -> `int=1` | rc 1, **f** `receipt_resolve` + **r** `replay_mismatch` |
| receipt-json | `5b831377` | raw-JSON marker pasted into the receipt | rc 1, **f** `receipt_embeds_json` (only f) |
| entry-digest | `725ddbff` | entry digest replaced | rc 1, **f** `entry_disagrees … sha=0` (only f) |
| entry-total | `33975e5a` | entry `192 binds` -> `191 binds` | rc 1, **f** `entry_disagrees … total=[191]` (only f) |
| nosteps | `c03239be` | steps 5-10 unnumbered (4 left) | rc 1, **e** `steps=4 <6` (only e) |
| limits-gone | `3c05573d` | `## Limits` section removed | rc 1, **h** `limits=0 bullets=0` (only h) |
| gate-missing | `5b94cf3d` | lesson S354 admit line removed | rc 1, **i** `gate_row_missing=S354` (only i) |
| paste-body | `141ce0ce` | 10 long round-25 keybind lines appended | rc 1, **i** `base_duplicates=10`, `overlap` high (only i) |
| row-unused | `af04bec6` | extra new row S356 with used-by `-` | rc 1, **i** `row_unused=S356` (only i) |
| row-used-by-held | `3320b804` | extra row S356 whose only consumer is a held document | rc 1, **i** `row_used_by_not_new` (only i) |
| registry-unused | `bd91cc30` | head row S355 used-by moved to the held r48 entry | rc 1, **b** `used=0` + **i** `row_used_by_not_new=S355` |
| opened-old | `8b0cb36b` | row S352 opened 2026-10-26 | rc 1, **b** `opened=2026-10-26` (only b) |

Reproduction: the POS and base runs were re-run after the last edit and diff clean against
`receipts/pos.txt` and `receipts/base.txt`; the tree was also rebuilt byte-identically from the same commit/tag
URLs and the same capture and admitted again (entry sha256 `a7f3cd22…` every time).

Lane runs (read-only): `receipts/lane-base.txt` (must-MISS at the round base) and `lane-tip.txt` (the lane as
it stands, no entry yet — also a miss).

## Controls from w1/ExecControlsC2 and what changed

`ExecControlsC2` scored this draft (snapshot sha `1220018902…`) over 17 bundles and named four defects; three
are closed here and the fourth stays a declared residual:

1. **Novelty was a full-line grep** (a one-word-per-line or stripped-citation paraphrase passed). Now clause i
   also compares hashed 6-word shingles against the base tree's knowledge/lesson text and fails at >= 15%
   overlap. `paraphrase` (their bundle 04 shape, 2,213 words) now measures 0.231 and misses on i; the POS
   measures 0.010.
2. **i never read the row's used-by cell**, so a row used by nobody was admitted (bundle 13). Every new row's
   used-by must now name ENTRY or a path that exists at REV (`row-unused` control misses on i).
3. **e accepted any in-range locator**, so a step locator pointing at the wrong line passed (bundle 14). e now
   requires a *verified* quote per step (span present in the pin inside the stated range); `step-quote` misses
   on d+e.
4. **c compares row against fetch copy only** (bundle 09, `pin-and-file`): unchanged and declared — the counter
   fetches nothing, so a mutated pin with a recomputed digest is admitted. Closing it needs an upstream
   re-hash, which this instrument deliberately does not do, or a digest list committed outside the fetch bytes
   (the freeze should declare which).
5. **Boundary 17** (a new row whose only consumer is an already-held document) is now closed: the used-by path
   must itself be new at REV (`row-used-by-held` misses on i). A row cited by a new knowledge entry or by the
   C1 tool still passes.

Bundle 16 (a new row reusing a base URL) stays admitted by design: g refuses only S319's URL, because the
registry's own practice reopens one file with new scopes (S162/S303/S317). Bundle 11 (an accurate hand-typed
receipt) is admitted: it is indistinguishable from a capture on the committed bytes, which is why clause r is
load-bearing beside f (bundle 10 has `f:1, r:0`), and why a run without a reachable compositor is a setup
error (exit 2), not a pass.

Their re-run at `a2e91724` reports 18 controls, 18 correct, one divergence: bundle 09 (`pin-and-file`), the
declared residual. Bundle 17 (used-by an already-held document) now misses at i, and 13 still misses at i.

## Notes for the L1 freeze

- **Where the material must land.** Entry `corpus/knowledge/hyprland-bind-key-match-r49.md`; rows S352.. in
  `## Registry` (11 cells); one `corpus/README.md` index row (3 cells, no other knowledge file named);
  `corpus/lessons/round-49.md` `## Gate` with one `**S### admit**` line per new row; pins under
  `.ufo/waves/round-49/fetch/`; the live receipt under `.ufo/waves/round-49/receipts/`. The counter is a draft
  only — the L1 owns copying it to `quality/counters/` and freezing it.
- **Receipt form rule.** `ExecBindsLive` has regenerated its receipt to
  `binds=192 named=142 code=42 mouse=6 switch=2 catch_all=0` (an earlier `named=184 code=0` line would miss f
  and r, because the dump re-derives 142/42). Keep the full commit on the `Hyprland 0.56.2` line.
- **Entry wording traps** the clause f parser reads literally: write the total as `192 binds` or `binds=192`
  (a `binds: 184` following the total is read as the total); keep each form count beside its label; say
  `int 0` (or `set false`) on the `resolve_binds_by_sym` line; put the digest or its first >= 12 hex on a line
  containing `sha256`.
- **Steps.** Every numbered step must carry a quote that verifies at its locator — the shape is
  `` `span` (<pin>:<line>) `` with the span present in that pin at that line; a bare locator is no longer enough
  (w1/ExecControlsC2's golden lost six steps to `step_without_verified_quote` before the shape was made
  explicit). Quotes must point at fetch pins, never at `corpus/` documents.
- **Held ground.** S319 is frozen (bytes at BASE/REV, its round-46 pin digest, cited in the entry, no new row
  for `src/devices/IKeyboard.cpp`). S318 and the other round-46 rows are not frozen by this counter; the entry
  may cite any row-bound round-46 pin (clause d's byte/name binding) without minting a row.
- **Pins.** A locator token resolves by exact basename, else by unique stem containment; keep pin names
  distinguishable (`Hyprland-legacy-ConfigManager.cpp` and `Hyprland-KeybindManager.cpp` coexist; a second
  bare `ConfigManager.cpp` would collide with the round-46 name).
- **Held URL reuse.** `src/config/legacy/ConfigManager.cpp` at `efb50993` is already S162/S303/S317. The entry
  may cite those held rows (clause d accepts any pin bound by a row at REV, and the round-46 copies carry the
  digest) instead of minting a fourth row; if it does mint one, that row must be used by the entry (clause i)
  and must not repeat S319's URL (clause g). Either shape is admitted; the freeze should say which it wants.
- **Clause i spans C1.** Every new registry row — including any row minted for the C1 keysym tool — needs its
  `**S### admit**` line and a real used-by. The four GROUND terms were checked absent under `corpus/` at BASE
  (`git grep -F -q` exit 1).

## Residuals and risks

- The committed fetch copies at REV are the trust root: `pin-and-file` is admitted by design (declared in the
  docstring).
- Clause r depends on the live compositor socket and a runnable `TMPDIR`; a bind changed between capture and
  score, a dead session or a missing `HYPRLAND_INSTANCE_SIGNATURE` is a miss/setup error by design. `hyprctl`
  is addressed absolutely and the child gets a scratch `HOME`/`XDG_*`.
- Clause f parses labels, not the compositor; clause r is what binds it to the live dump.
- Clause g narrows duplicate-URL refusal to S319 (the dispatch's words).
- Clause i's shingle check is a rate over the base knowledge/lesson text, bounded to 3 MiB; it catches light
  paraphrase (0.23-0.56) and pastes (1.0) but a full rewrite at a higher edit rate would land under the
  threshold, and the line-grep half only samples 40 lines.
- Clause d/e check quotes at locators and steps on verified quote presence, not the truth of the sentence; h
  reads shape and scope words; b checks the Registry and README fields, not their content.
- The POS is a test tree built from real pinned bytes and a real capture; it is not the round's entry.

Host safety: `hyprctl version`, `hyprctl binds -j` and `hyprctl getoption … -j` were the only host reads; no
dispatch/keyword/reload/plugin call, no relayout, no terminal, no input injection, no pacman, no package
transaction, no host config or cache write (replay children ran with `HOME`/`XDG_*` under
`/fast/scratch/hyaku/mado-r49/ExecCounterC2`). Session material is shape-only: no device name, window title or
bind argument was copied; the only host artefact is a digest of the raw JSON and the getoption reply. No tool
was installed or upgraded.

Runs (final counter `a2e91724…`):

```
PRED-C2-r49: clauses=a:0 admitted=0/1 verdict=TARGET_MISSED rev=03e4ae76aff7a4be59cb69970dd553baa319695a
PRED-C2-r49: clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 r:1 admitted=1/1 verdict=TARGET_MET rev=fe39094367b4fecf28b18ae0fedf7b7884e98aa3
```

PRED-C2-r49: clauses=a:0 admitted=0/1 verdict=TARGET_MISSED rev=03e4ae76aff7a4be59cb69970dd553baa319695a
