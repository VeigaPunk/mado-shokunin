# ExecCounterC2 — PRED-C2-r47 (terminal-entry counter), w1 build

Status: DONE (draft only; the L1 integrates). Counter target:
`.ufo/waves/round-47/w1/ExecCounterC2/c2-r47-terminal-entry.py` (35066 B, sha256
`69c121489b0d816c0befb91bf66da62be262bd5064f371ae13e5033e65e77dbd`), to be copied to
`quality/counters/c2-r47-terminal-entry.py` at the freeze. Nothing in the lane is
tracked-modified; every file below is new and inside this seat dir.

Judges: `corpus/knowledge/xdg-terminal-selection-r47.md` at `--rev` against
`--base 60edb66e2f1cb90acc6e9442fc93ded0ca42d750` (lane tip at round start; HEAD
`c24adef2` adds only round-47 planning files — `git diff --stat 60edb66 c24adef` lists
no `corpus/` path). Output: one line per check, then
`PRED-C2-r47: admitted=N/1 verdict=TARGET_MET|TARGET_MISSED rev=<hash>`; exit 0 admitted,
1 missed, 2 setup.

## Axes this moves

- **Coverage (C2)**: the counter is the frozen instrument for the entry, so the entry's
  sourced ground (S326+, v0.14.3 pins) is machine-checkable rather than prose.
- **Operability**: the counter is read-only and revision-addressed; it fetches nothing
  and writes nothing in the lane (temp dirs under the system temp root, removed).

## Clauses (a-i), as implemented

a. ENTRY absent at BASE (present = setup error, exit 2) and present at REV.
b. Provenance head, unfenced lines in the first 20 raw lines: >= 2 distinct
   `source: S###` ids, each >= S326, each with exactly one Registry row (11 cells),
   tier A/B/C, non-empty kind, `status mined`, opened `2026-10-26`, valid `recheck`,
   used-by listing the entry, and absent at BASE; exactly one `verified-at: 2026-10-26`
   and one `recheck:` in the window, none outside. Every `S###` anywhere in the entry
   must be a Registry row that exists at REV (invented ids are ghosts); held ids
   S056-S060 exist and pass.
c. Every head row is pin-bound: one `.ufo/waves/round-47/fetch/<path>` receipt, copy at
   REV mode 100644 with the row's recorded sha256, anchor ranges resolving to that copy
   inside its line count (or the row says `whole file`), digest prefixes such as
   `sha256:713703..` are not read as locators. Every URL in the row must carry a pinned
   ref: `v0.14.3` or a commit hash (7-40 hex); `main|master|HEAD|latest|dev|trunk|develop`
   and every other ref are refused; a ref-less URL (a merge-request page) is refused
   unless the row records a 40-hex commit. For the xdg-terminal-exec repository the URL
   path must be a key of the counter's `PIN_SHA` and the fetch copy must hash to the
   real v0.14.3 digest.
d. Quote-at-range. A quote is an inline backticked or double-quoted span of 2-25 words
   that the author cites with an adjacent locator (`, <loc>`, ` at <loc>`, `(<loc>)`),
   where the locator resolves to a committed fetch pin; the span must occur verbatim in
   that pin (whitespace-collapsed, word-bounded) with an occurrence line inside the
   stated `[a,b]`; >25 words fails; locators stay inside their pin; a pin must be cited
   by a row by name or by bytes (a pin whose sha256 equals a cited pin's sha is the same
   bytes). This accepts the lane's quote convention (backticked pin text followed by
   `xdg-terminal-exec:353`) as well as double quotes.
e. >= 6 numbered chain steps and EVERY numbered step cites a
   `<script pin>:<a>[-<b>]` range inside the 1499-line script pin (the fetch copy whose
   sha256 is `PIN_SHA["xdg-terminal-exec"]`).
f. The round-17 `[UNK]` (`corpus/knowledge/terminal-route-r17.md:144-145`) is answered by
   a live receipt the landed tool reproduces: an entry line names both
   `terminal-route-r17.md:144` and `.ufo/waves/round-47/receipts/<file>`; the receipt
   exists at REV (100644, >= 256 B), is absent at BASE, names `observed=<committed
   capture>`, records >= 3 `XDG_*` keys and exactly one
   `MADO_TERM: selected=<id> path=<path> verdict=<OK|AGREE|DIFFER>` line. The counter
   extracts `tools/mado-terminal.py` at REV and runs `explain --observed <capture>` in a
   temporary dir under the receipt's `XDG_*` env; it must exit 0, print verdict `AGREE`,
   and its selected=/path= must equal the receipt's; the capture's first two lines must
   equal them too.
g. `corpus/README.md`: exactly one column-0 row for the entry, three cells, no
   `supersed*|replac*|obsolet*|instead|deprecat*`, naming no other `knowledge/` file, and
   its `S###`/`S###-S###` tokens cover every head id.
h. Held ground: rows S056-S060 byte-equal at BASE and REV (one control shows the failure
   when S056's URL is moved).
i. Ground-absent at BASE: `read_config_paths`, `check_entry_key`, `find_entry_paths`,
   `print-delimiter` each return no match from `git grep` at BASE under `corpus/`,
   and >= 2 occur at REV.

Trust root: the committed fetch copies at REV, hard-checked against the real v0.14.3
bytes (`pins.txt`, fetched 2026-10-26):

| file | bytes | lines | sha256 |
|---|---|---|---|
| xdg-terminal-exec | 44020 | 1499 | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` |
| README.md | 14762 | 337 | `c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40` |
| xdg-terminals.list | 1053 | 25 | `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034` |
| xdg-terminal-exec.1.scd | 6071 | 186 | `3dba162f5502a3553bad9b2398ace10f7bc2456900c7c9ff62a436935876ec59` |
| test/tests.bats | 8181 | 275 | `ce4b634257dd6c1ebddd96d88f00f1b324f054209be6c80737224b69e986b311` |
| Makefile | 1111 | 39 | `20ac532456fd0abbd449b5cabf8f14a07379763597e4c1dfe9c2ddb1c0dca6ef` |

Source: `https://codeload.github.com/Vladimir-csp/xdg-terminal-exec/tar.gz/refs/tags/v0.14.3`
(tarball sha256 `82ac2dfdb357361d15f5163cdeb3cfd457bbb30bf5d2e14436393f493bd32afe`);
tag commit `065925df9f419008159258ae169018bfd23df71b` (`git ls-remote` same day). The
host binary is byte-equal: `sha256sum /usr/bin/xdg-terminal-exec` and the tarball file
both print `89f2be9a…127ac`, both 44020 B (read-only, no execution).

## Controls (measured, receipts in `receipts/`)

`receipts/controls.md` is generated from the receipts by grep (locators computed).
Positive: a scratch clone of BASE with a minimal valid entry, five rows S326-S330, a
README row, the six v0.14.3 fetch copies, a live receipt in clause-f shape and a control
double of the tool → `admitted=1/1`, exit 0 (`ctl-pos.txt`). Negatives, each one commit
on the positive tree, each failing its intended clause and nothing incidental:

| negative | exit | clause line (from receipt) |
|---|---|---|
| BASE (no entry) | 1 | `clause=a entry_absent` |
| quote not in pin | 1 | `clause=d quote_not_in_pin` |
| branch URL in the cited row S327 | 1 | `clause=c id=S327 url_branch_ref` |
| held row S056 moved | 1 | `clause=h held_row_moved=S056` |
| receipt absent at REV | 1 | `clause=f receipt_missing` |
| citation index without steps | 1 | `clause=e steps=0 <6` |
| receipt contradicts its capture | 1 | `clause=f observed_mismatch` |
| true quote, false stated range | 1 | `clause=d quote_out_of_range` |
| pin bytes changed under the row sha | 1 | `clause=c id=S328 pin_sha_mismatch` |
| setup: entry already at base | 2 | `SETUP precondition_failed entry_present_at_base` |

Extra boundary cases, each a commit on a clone of the preview tree: head source on a
whole-file tag-pinned row (S333, omarchy) admits (`x1-head-s333.txt`); head source on a
host-bytes row with no URL (S337) fails `clause=c id=S337 no_url`
(`x2-head-s337.txt`); a prose mention of registry row S338 is not a ghost
(`x3-prose-s338.txt`).

## The real w1 drafts, measured (preview wiring)

`preview.py` copies the actual `.ufo/waves/round-47/w1/ScrEntry/entry.md`,
`w1/ScrRows/rows.md` rows (receipt paths rewritten to the freeze `fetch/`), the seat
fetch bytes, and a clause-f-shaped receipt into a scratch clone, then runs the counter:
`admitted=1/1` (`receipts/preview-real-drafts.txt`, 13 quotes checked, 7/7 steps cite
the script pin, held rows unchanged, 4/4 ground terms). Clause c checked the two head
rows S326/S327 (`xdg-terminal-exec` 9 ranges, `README.md` 6 ranges); the relaxation for
renamed upstream paths and whole-file rows is what lets S330/S333-style rows be head
sources without a false fail.

## What the freeze must land for this predicate (L1)

1. **Pins at `.ufo/waves/round-47/fetch/`** (recursive): the bytes each head row cites,
   named so the entry/row locators resolve — exact basename wins, else a unique
   extension-stripped stem match (`README.md` ↔ `README-v0.14.3.md`); a copy is trusted
   only when its sha256 is the row's digest and, for the xdg-terminal-exec repo, the real
   v0.14.3 digest. The seat dirs already hold the bytes (`w1/ScrRows/fetch/`,
   `w1/ScrEntry/README-v0.14.3.md`).
2. **`tools/mado-terminal.py` at REV** (the landed C1 tool). Clause f runs it; the
   preview used a control double, so the real instrument is still untested here.
3. **Live receipt** in clause-f shape: one `.ufo/waves/round-47/receipts/<file>` with
   `observed=<committed capture of --print-id --print-path --print-cmd>`, the host
   `XDG_*` lines (ExecLive already records them), and exactly one `MADO_TERM:` line as
   printed by `explain --observed`; the entry line that names
   `terminal-route-r17.md:144` must also cite that receipt path. The draft currently
   carries `<LIVE:…>` placeholders and cites no receipt path on the r17 line.
4. **`corpus/README.md` row** covering the head ids, and `SOURCES.md` rows S326+ for the
   head ids with `used-by corpus/knowledge/xdg-terminal-selection-r47.md`; rows S056-S060
   untouched. Head sources must be URL-pinned rows: a host-byte row (no upstream URL)
   may exist in the registry and be mentioned in prose, but as a head source it fails
   clause c by design (`x2`).

## Residuals (declared in the counter docstring)

Fetch copies are the trust root for non-xdg-terminal-exec URLs; a true quote at a true
locator can sit beside a claim it does not support; clause c binds URL+digest+name, not
the row's prose; clause d only sees spans the author cites with a locator (a quote of
another lane document, like the r17 quote itself, is out of reach); clause e counts
numbered steps and script locators, not their truth; clause f reproduces selected/path
through the tool, not the whole trace; clause i is a term census.

## Environment, safety, files

- No installs (nothing needed; `pacman` not touched). No terminal, GUI or compositor verb
  run; `xdg-terminal-exec` was never executed — only `sha256sum`/`wc -c` on the binary.
- Scratch: `/fast/scratch/hyaku/mado-r47/ExecCounterC2/` (clones under it; harnesses
  honour `C2R47_WORK`), removed before hand-off. Receipts were copied here first.
- Written (all new, this seat dir): `c2-r47-terminal-entry.py`, `pins.txt`,
  `build-control.py`, `run-controls.py`, `preview.py`, `ext-cases.py`,
  `receipts/*.{txt,md}`; this report.

## Addendum (after ScrEntry's wiring, measured)

ScrEntry fixed quote adjacency and cited `.ufo/waves/round-47/receipts/<LIVE:live-receipt>`
on the r17 lines. Re-measured in a fresh preview clone, before the scratch was removed:

- updated entry + preview wiring -> `admitted=1/1`, **14 quotes** verified at their pin
  ranges, 7/7 steps script-cited (`receipts/preview-real-drafts.txt`, rev 180d64ad);
- the entry as-is, with the placeholder basename and no real receipts path -> clause f
  `no_r17_receipt_line`, exit 1 (`receipts/entry-as-is-placeholder.txt`). The placeholder
  is not accepted on purpose; the L1 names the real receipt file.

README simplification confirmed for the L1: one fetch copy of the README bytes suffices.
A `README-v0.14.3.md` locator resolves to `fetch/README.md` by unique stem, and a pin is
accepted as cited when its sha256 equals a row-cited pin's (byte equality), so S327 may
point at `fetch/README.md` directly.
