# ExecCounterC2 — C2 counter draft (round 48, w1)

STATUS: complete. Draft counter `c2-r48-xkb-entry.py` at the seat dir; the POS tree is admitted, a variant on
the live seat's real receipt bytes is admitted, a renamed/subdir-pin variant is admitted, and eight schematic
controls plus two live-receipt controls plus the two precondition cases are rejected on their clauses.
Receipts under `.ufo/waves/round-48/w1/ExecCounterC2/receipts/`. Nothing in the lane was written; no lane
tool was run; no frozen counter was scored.

## Files

- `.ufo/waves/round-48/w1/ExecCounterC2/c2-r48-xkb-entry.py` — the C2 counter draft
  (37,309 B, sha256 `1fb235b2a92ea024171652801429e636868ee1758c76a31d2cce929099c28941`, `receipts/digests.txt`).
- `.ufo/waves/round-48/w1/ExecCounterC2/controls/build_controls.py` and `controls/run_controls.py` — the scratch
  harness (absolute clone path at `S`), copied for reproducibility only; not lane code.
- `.ufo/waves/round-48/w1/ExecCounterC2/receipts/` — the evidence listed at the end.
- This report.

No tracked lane file, no `tools/`, no `corpus/` file, no index, no template was edited. No tool was installed
or upgraded (none was needed).

## The counter

Copy of `quality/counters/c2-r47-terminal-entry.py`, retargeted to
`corpus/knowledge/xkb-keymap-compile-r48.md` against base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`.
Read-only: every read is `git show REV:path` with ambient `GIT_*` stripped; the counter fetches nothing and
writes nothing (no file is opened for writing anywhere in the file). Python 3 stdlib only. Exit 0 iff
`admitted=1/1`, 1 if missed, 2 on a setup failure (unresolved revision, or the entry already at BASE).

Clauses (docstring is the contract; the L1 freezes this):

- **a** entry new at REV, absent at BASE; present at BASE is a setup error.
- **b** provenance head in the first 20 raw lines: >= 3 distinct `source: S###`, every id >= S340, exactly one
  `verified-at: 2026-10-26` and one `recheck:` (ISO / `NNd` / `on-*`), no such line outside the window; every
  `S###` token in the unfenced entry exists at REV (no ghosts); each head row exactly one 11-cell Registry row,
  tier A/B/C, non-empty kind, `mined`, opened 2026-10-26, valid recheck, used-by ENTRY, no head id at BASE.
- **c** head rows pin-bound: `sha256:<64hex>` recorded, >= 1 `.ufo/waves/round-48/fetch/...` receipt path, every
  named copy present at REV mode 100644 with a digest the row records; URLs only tag
  (`xkbcommon-1.13.2`, `xkeyboard-config-2.48`) or 7-40-hex commit refs, branch names refused, ref-less URLs
  refused unless a 40-hex commit + digest is recorded; a URL-less row only as kind `own-work` with a digest and
  a pin; URL path must relate to a pin stem; anchor ranges must resolve to the row's own pins and stay in
  range, or say `whole file`.
- **d** quotes (2-25 words, backticked or double-quoted, immediately followed by a locator) verbatim in a
  committed fetch pin at the stated range; quote locators that name a lane document are refused; every pin
  locator in range; a pin used by the entry must be cited by a row by name or bytes.
- **e** >= 6 numbered steps, every step citing a pin locator that is cited by a row (round-48 head row or held
  round-46 row) and in range.
- **f** the live receipt (below).
- **g** exactly one README index row, three cells, no redirect word, naming no other knowledge file, `S###`
  tokens covering every head id.
- **h** rows S318/S319 byte-equal at BASE and REV, the round-46 entry byte-equal, and each held row's round-46
  pin present with a digest the row records.
- **i** the four terms `xkb_keymap_new_from_names`, `XKB-595`, `compile-keymap`, `xkeyboard-config-2.48` each
  absent under `corpus/` at BASE (`git grep` exit 1) and >= 2 present at REV.

Clause **f** in detail (the interface the entry seat and the live receipt must meet): the entry cites
`.ufo/waves/round-48/receipts/<file>`; the receipt is new at REV, 100644, >= 512 B, and carries a
`xkbcli`/`libxkbcommon` version triple, the positive RMLVO `br` + `compose:caps` with rc 0 and a 64-hex keymap
sha256 in one coherent window, and three probes — `--layout zz` rc 1, `--variant nope` rc 1, `nope:nope` rc 0
with `XKB-595`/`Unrecognized RMLVO option`. A "coherent window" is a blank-line record, a non-indented line
plus its indented continuation lines (a case), or a single line; every window naming the probe must carry one
distinct labelled rc. The entry must state the same values: the version beside `xkbcli`, `compose:caps` with
`br` and rc 0, the digest (or its first >= 12 hex) beside `sha256`, and each probe's rc written as
`rc`/`exit`/`status` + integer on a line naming the probe (a bare number in a table cell is not read).

## Evidence

Host receipt values are real, recomputed read-only over the exact stdout bytes (`receipts/host-xkb-probe.txt`):
`xkbcli --version` = 1.13.2, `libxkbcommon 1.13.2-1`; `xkbcli compile-keymap --layout br --options
compose:caps` rc 0, 2090 lines, 73,079 B, sha256 `efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81`;
`--layout zz` rc 1 XKB-338; `--variant nope` rc 1 XKB-661; `--options nope:nope` rc 0 XKB-595; `--model nope`
rc 0; `--rules nope` rc 1 XKB-338. Base census (`receipts/base-census.txt`): all four GROUND terms
`git grep -F -q` exit 1 at `579f694b`.

The POS tree is a real-bytes tree, not typed fiction: the three fetch pins are the actual tag files
(`rules.c` 74,868 B, `context.c` 22,059 B, `symbols/br` 19,592 B — `receipts/pos-pins.txt`), the entry's six
quotes sit on those lines, and the POS receipt's values equal the host probe above
(`receipts/pos-entry.md`, `receipts/pos-receipt.txt`, `receipts/pos-rows.md`). The POS commit touches only the
entry, `corpus/SOURCES.md`, `corpus/README.md`, the receipt and the three pins (file list in
`receipts/controls.txt`).

Control run (`receipts/controls.txt`, every run captured in full; revisions in `receipts/digests.txt`):

| control | rev | mutation | verdict |
|---|---|---|---|
| BASE | `579f694b` | score the base revision itself | rc 1, `clause=a entry_absent` |
| SETUP | POS as `--base` | entry present at base | rc 2, `precondition_failed` |
| POS | `5011822563` | minimal entry-only tree | **admitted 1/1**, all nine clauses 1 |
| QUOTE | `c381ed3885` | one quote word changed | rc 1, clause **d** `quote_not_in_pin` (only d flips) |
| RANGE | `b5c5b69568` | quote locator `:255` -> `:9999` | rc 1, clause **d** `locator_out_of_pin` + `quote_out_of_range` (only d) |
| BRANCH | `07bf77cec0` | row URL ref `xkbcommon-1.13.2` -> `main` | rc 1, clause **c** `url_branch_ref` (only c) |
| PIN | `b3ba95504e` | row digest replaced | rc 1, clause **c** `pin_sha_mismatch`; also d and e, because an unbound pin stops being cited ground |
| HELD | `281c8df377` | S318 used-by cell moved | rc 1, clause **h** `held_row_moved`; also d and e, because the moved row's pins are no longer trusted |
| RECEIPT-absent | `2badc33edc` | cited receipt deleted | rc 1, clause **f** `receipt_missing` (only f) |
| RECEIPT-contradicts | `cecec49e61` | receipt `--layout zz` rc 1 -> rc 0 | rc 1, clause **f** `receipt_probe_bad=unknown layout(rc_values=[0])` (only f) |
| NOSTEPS | `bc80080df8` | step 5 unnumbered | rc 1, clause **e** `steps=5 <6` (only e) |
| POS-LIVE | `12607efdf9` | receipt replaced by the live seat's real bytes (sha256 `f719d1b3…`) | **admitted 1/1**, clause f parses the real format |
| LIVE-receipt-contradicts | `460544e2d7` | live `unknown-variant` rc 1 -> rc 0 | rc 1, clause **f** `rc_values=[0]` (only f) |
| LIVE-entry-disagrees | `750c57cb78` | entry's digest prefix changed | rc 1, clause **f** `entry_disagrees … sha=0` (only f) |
| POS-RENAME | `779fa0652b` | pins moved to `fetch/libxkbcommon/…` + `fetch/xkeyboard-config/br`, locators `rules.c`/`context.c`/`br` | **admitted 1/1** (subdirs and basename->stem resolution work) |

Pre-integration lane: the counter on the lane tip `5ff167423e` with base `579f694b` gives rc 1,
`clause=a entry_absent` (`receipts/lane-before.txt`) — the tree as it stands is correctly not admitted.

## Alignment notes for the L1 freeze

- **Receipt label.** Clause f reads a labelled rc. The live seat's receipt already parses
  (`===== 3` matrix lines `unknown-layout … rc=1` + indented `args: --layout zz`), and that is the tested shape;
  a receipt whose rc is a bare table cell with no `rc`/`exit`/`status` label would be refused by design.
- **Entry rc statements.** Clause f's entry side needs `rc N` / `exit N` / `status N` beside each probe name,
  and the keymap digest (>= 12 hex) on a line naming `sha256`. The receipt and the entry are bound to each
  other: changing either alone fails (`LIVE-receipt-contradicts`, `LIVE-entry-disagrees`).
- **Pin naming.** Any basename or stem that relates to the locator token resolves (`libxkbcommon-rules.c` <-
  `rules.c`, `fetch/libxkbcommon/rules.c` <- `rules.c`, `xkeyboard-config/br` <- `br:4`); a token matching two
  pins resolves to none, so keep pin names distinguishable.
- **Quote locators must resolve to a fetch pin.** A quote followed by `corpus/knowledge/*.md:NN` is refused
  (clause d). Cite the held rows S318/S319 and the round-46 entry by plain locator, and quote only pinned
  upstream bytes.
- **Held ground.** Clause h freezes S318/S319 row bytes, the round-46 entry bytes and the two round-46 pins; a
  new entry can lean on them (steps 1 and 6 of the POS do) but cannot edit them.
- **Where the L1 must land the material:** `corpus/knowledge/xkb-keymap-compile-r48.md`, rows S340.. in
  `corpus/SOURCES.md` inside `## Registry` (11 cells), one `corpus/README.md` index row mentioning no other
  knowledge file, copies in `.ufo/waves/round-48/fetch/` and the receipt in `.ufo/waves/round-48/receipts/`.
- **Census.** Clause i uses the four ticket terms and needs two present at REV; in the POS three are
  (`xkeyboard-config-2.48`, `compile-keymap`, `XKB-595`).

## Residuals and risks

- The committed fetch copies are the trust root: URL+digest are bound to each other, not re-hashed upstream; a
  commit hash is accepted without proving repository membership.
- Clause d sees only a quote the author cites with a locator, and refuses lane-document locators outright (a
  quote at a true locator can still sit beside a claim it does not support).
- Clause e checks the presence and range of a cited pin per numbered step, not the truth of the step.
- Clause f parses labels, not the compiler: a receipt that mislabels a value would pass if the entry repeated
  the same mislabel; the host probe in `receipts/host-xkb-probe.txt` shows the true values for the POS.
- Clause g refuses a README row that names another knowledge file (r47's residual shape); if the real row
  cross-links the round-46 entry, the L1 must decide at freeze (widen g or drop the link).
- The control revisions live in a scratch clone; after scratch cleanup the retained evidence is the captured
  logs and digests in `receipts/`, and the harness scripts under `controls/`.
- Two cascades are intended and recorded: an unbound pin (PIN) and a moved held row (HELD) also break the
  quotes/steps that lean on them; both still fail their own clause first.

## Receipts (all under `.ufo/waves/round-48/w1/ExecCounterC2/receipts/`)

`controls.txt` (14 runs plus the POS file list, captured in full) · `control-patches.txt` (each control's
zero-context diff, POS-LIVE as a stat only so the live seat's receipt body is not duplicated) · `digests.txt`
(counter sha256/bytes, every revision, live receipt sha256) · `base-census.txt` · `host-xkb-probe.txt` ·
`lane-before.txt` · `pos-entry.md` · `pos-rows.md` · `pos-receipt.txt` · `pos-pins.txt` · `pos-rename.txt`.

Host safety: no pacman, no compositor mutation, no terminal launch, no input injection, no host cache touched;
the only host binary run was read-only `xkbcli compile-keymap` (stdout/stderr to scratch, deleted).
