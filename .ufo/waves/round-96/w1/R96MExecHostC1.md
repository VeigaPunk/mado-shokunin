# R96MExecHostC1 -- w1 report (round 96, mado)

Seat: host text-DB recipe + host-leg oracle measurement + harm-harness draft.
Date: 2026-11-07. Lane base rev `9f029f46f01f6cd3a1d29ac39bb498a1d0c3d`; lane HEAD moved to
`09db97c30a09ef494f7439c3a513e2d86f115a63` during the wave (siblings landing; my harness
resolves `--rev` dynamically, so this is harmless for the replay design).

## Godspeed axes

- **A1 host-leg truth breadth** -- oracle answers over the whole committed host list, both name modes.
- **A2 candidate delta coverage** -- oracle-vs-C1-candidate agreement census (blocked on the sibling's draft).
- **A3 harm-watch operability** -- every r95 live counter replayable with one command; r96 counter slot ready.

## 1. Host text-DB recipe (A1) -- DONE

Committed: `.ufo/waves/round-96/controls/host-text-db-r96.json`.

- Copied the 8 text files of `/usr/share/mime/mime` (`magic`, `globs`, `globs2`, `aliases`,
  `subclasses`, `icons`, `generic-icons`, `XMLnamespaces`) into scratch `hostdb/mime/`;
  **host text-DB: 8 files, 211,254 bytes**; `cmp -s` byte identity 8/8; `find hostdb -name mime.cache` = 0 hits.
- Host `/usr/share/mime/mime.cache` measured fresh (excluded from the copy): sha256
  `b988d3d27bda7500ba4eb8e88d78e61049796d94ef79745dd366bacf5460bb47`, 207,520 B.
- Cross-check: copied `globs2` sha256 `556ee69c...` equals the round-94 counter's host pin in
  `harm-final-r95.txt` -- no DB drift since round 94.
- Text-mode env for every measurement: `HOME=<empty> XDG_DATA_HOME=<empty> XDG_DATA_DIRS=<copy>`.

## 2. Host leg (A1) -- DONE, oracle-only

Committed: `.ufo/waves/round-96/receipts/host-leg-r96.txt` (full evidence + both label histograms).

- List `.ufo/waves/round-95/controls/mimesniff-host-files-r95.txt` (sha256
  `9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87`): **4911 listed, 0 missing/skipped**.
- Oracle: round-95 frozen source, sha256 measured
  `99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a` (matches contract 3; NOTE the
  claims-declaration counting-command line prints `...f8e6984a...` -- two hex chars lost in prose;
  the declaration's `<pending-w1>` should carry the value measured here).
- Ran 2 legs per path (`=<basename>`, `0`), `env -i` text-mode env, `xargs -P 8`:
  **4911 rows, 0 ERR**, 35 s wall. Result TSV sha256
  `1507a4abbdfd2f75bfcec3935050ddfa30fd8fe49876cf9b3e40f9ba5c1cbec1` (full per-path labels in scratch,
  histograms embedded in the receipt).
- Label diversity: name-leg 78 distinct, null-leg 62 distinct; uncertain=1 rows exist in both legs
  (`application/octet-stream 1`: 242 name / 276 null; `text/x-python 1`: 23; `application/x-perl 1`: 2) --
  the frozen case generator and the C1 author can mine these real uncertain rows.
- Disagreement census (oracle vs candidate): **not produced -- the C1 draft
  `.ufo/waves/round-96/build/mado-mimetext.c1.py` never existed during this wave** (checked repeatedly,
  last 14:3x UTC). Rerun command is documented in the receipt §3; nothing to compare against was fabricated.

## 3. Harm harness draft (A3) -- DONE, 3-leg smoke green

Committed: `.ufo/waves/round-96/controls/harm-r96.sh`.

- 23 legs encoded 1:1 from every `$ ` counter line of `harm-final-r95.txt` (mado-verify selftest +
  file-plane, check-index, check-tool-ledger, 9 tool selftests, gate selftest + 3 gate kill-set legs,
  counters c2-r90 / c2-r92 / c1-r90 / c1-r94 / c2-r94 / c2-r93), plus `r96_counter` left as the
  literal `<placeholder>` argv for the L1 (per item 3).
- `--rev` is replayed at current HEAD; every `--base-rev` and `--expect-*-sha256` anchor stays verbatim
  from the receipt; each leg's `--scratch-root` sits under `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mado-r96/R96MExecHostC1/harm`.
- Expected rc codified: 0 everywhere, `r90c1_portal_routing` EXPECTS rc=2 (SETUP_ERROR, per the r95
  receipt note), `r96_counter` prints rc=125 SKIPPED until filled.
- Smoke (only these three run; full set is the L1's): `verify_selftest` rc=0 (460/460),
  `index` rc=0 (rev=09db97c3..., indexed=116/116, coverage 10.0000/10),
  `receipt_presence_selftest` rc=0 (checks=6 failed=0). Harness exit rc=0.
- Gate pin re-measured unchanged: `check-selftest-strength.py` sha256
  `2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b`.

## Evidence index

| artifact | sha256 |
| --- | --- |
| controls/host-text-db-r96.json | (committed file; pins inside) |
| receipts/host-leg-r96.txt | (committed receipt) |
| controls/harm-r96.sh | (committed harness) |
| oracle source r95 | `99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a` |
| host list r95 | `9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87` |
| result TSV (scratch, deleted) | `1507a4abbdfd2f75bfcec3935050ddfa30fd8fe49876cf9b3e40f9ba5c1cbec1` |
| built oracle binary (build-dependent) | `186537938e186727072bf911a86117918d505593e77617e53cfa246d425a3aa5` |

## Risks / blockers / notes for the L1

- **A2 blocked, not dropped**: candidate draft absent all wave. When it lands, rerun receipt §3's
  command; the oracle column of truth is already frozen in the receipt histograms + TSV sha.
- Declaration prose bug: oracle sha printed as `99df35f8b3fd7005f30789f8e6984a1bbceaff8dc6c1d326f0132eb7b4d124a`
  in the counting command -- measured bytes hash to `...f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a`.
  Freeze should use the measured value.
- `r96_counter` argv placeholder must be filled by the L1 before the full harm run (rc=125 otherwise).
- Tool installs: none (pacman pause respected; nothing needed beyond `cc`/`pkg-config`).
- Boundary: `/usr/share/mime` read-only throughout; no host service, config, PATH-dir or git/jj state
  touched; all writes were my seat files + scratch. Scratch deleted after receipts were copied out.
