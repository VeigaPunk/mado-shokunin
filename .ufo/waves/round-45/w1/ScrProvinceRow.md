# ScrProvinceRow — round 45 w1 (province draft seat)

**Status: complete.** Lane `mado-shokunin`, read at tip `ebdba13f7cb16d454763003d424398eec3bb2788`
(freeze `22a8dedd02f507689c567777e0f20b5e645c8ce0`, base `0c89478af821a6424c9ac922eafe02e39630cf4f`).
Task: draft the append-only round-45 refinement to `PROVINCE.md` — the `tools/mado-monitors.py` table row
and the two round-45 counters plus the receipt privacy gate as record instruments.

**Draft:** `.ufo/waves/round-45/w1/ScrProvinceRow/province.md` (sha256 `d8f6406f…`, full list in
`receipts/sha256.txt`). `PROVINCE.md` is byte-untouched by this seat (`receipts/lane-clean.txt`,
`git status --porcelain -- PROVINCE.md SKILL.md quality/ tools/ corpus/` prints nothing).

## What the draft contains

1. **The table row** for insertion after `tools/mado-geometry.py` (`PROVINCE.md:32`; header `:22`; rows 9 → 10):
   Reads = the caller-named `--config` files (regular files only, `O_RDONLY|O_NONBLOCK`, `S_ISREG` required,
   1048576 B cap, argument order) plus one caller-supplied `hyprctl monitors all -j` dump (`--monitors` or
   `-`, ≤ 1048577 B); no `source =` following, no `$NAME` expansion, no environment read, no tree discovery,
   no socket, no Wayland client, no process. Writes = stdout only (`MADO_MON_RULE:`, `MADO_MON_OUTPUT:`, one
   `MADO_MONITORS:` line; verdict codes `OK` 0 / `DIFFER` 1 / `NO_MATCHING_MONITOR` 3 / `NO_RULES` 4 /
   `NOT_COMPARED` 5; setup `SETUP <reason>`, exit 2); `--selftest` 33 in-memory cases, no file written, no
   child process. Owner = mado round 45, adjacent `mado-geometry.py`/`mado-wsrules.py`, tsukuroi only for the
   compositor/hyprutils package versions.
2. **The refinement note**, in paste-ready plain paragraphs for the end of the file: the tool paragraph (a
   join, not a blame), the two counters as record instruments (C1 read/write surface incl. the four
   marker-writing PATH decoys and the `--work`-only writes, 49 fixtures, seed 45; C2 read-only git over the
   entry/registry/lesson/README/nine pins, the census line it demands, seventeen surfaces ≤ 30 lines), the
   **conditional** privacy-gate paragraph, the round-45 entry as source-read knowledge (round-38 addendum
   pattern), and the declared limits.
3. **A coverage finding** stated but not absorbed: `PROVINCE.md:34` claims the inventory covers every tracked
   file under `tools/`; `tools/` holds 12 files and the table 9 rows — `mado-eventq.py`, `mado-options.py`
   and `mado-wsrules.py` have no row (`receipts/province-anchors.txt`). L1 decides: add rows or reword.
4. **Quote table** (16 quotes, each ≤ 25 words, each `source:line` computed with `grep -n -F`).

## Gates (what was actually run)

| command | outcome |
|---|---|
| `python3 -I .ufo/waves/round-45/l1-draft/mado-monitors.py --selftest` | `MADO_MONITORS_SELFTEST: 33/33 passed`, rc 0 (`receipts/tool-contract.txt`) |
| `python3 -I .ufo/waves/round-45/w1/ScrProvinceRow/verify.py` | `VERIFY: OK (0 failures)`, 59 checks, rc 0 (`receipts/verify.txt`) |
| `git status --porcelain -- PROVINCE.md SKILL.md quality/ tools/ corpus/` | empty (`receipts/lane-clean.txt`) |
| read-only constant import of both frozen counters | `FIXTURES=49 SELFTEST_MIN=30`, `SURFACES=17 PINS=9`, seed default 45, both `BASE=0c89478` (`receipts/counters.txt`) |

`verify.py` re-checks, from receipts and from the live files: every quote row (word bound + the exact
`file:line` line in `receipts/quotes.txt`), every quoted span in the prose, the five PROVINCE anchors and
`SKILL.md:343`, the four counter constants, the reference selftest, the two conditional absences
(`tools/mado-monitors.py` and `quality/check-session-material.py` at HEAD), the gate draft's presence, and a
privacy scan of the draft itself (no absolute home path, no socket-table row, no serial assignment).

## Touched surfaces

Created, inside the seat allowance only: `.ufo/waves/round-45/w1/ScrProvinceRow/` (`province.md`,
`verify.py`, `receipts/{province-anchors,tool-contract,counters,gate,quotes,lane-clean,verify,sha256}.txt`)
and this report. Scratch `/fast/scratch/hyaku/mado-r45/ScrProvinceRow` was created empty and removed before
finishing (nothing was ever written into it; the verification runs need no scratch).
No tracked file edited; no git/jj mutation of any kind — read-only `git log/show/ls-tree/status/rev-parse`
only. No compositor call, no host-session touch, no package operation; no tool installed.

## Out of scope (not done, by design)

- Not scored: neither `c1-r45-monitors.py` nor `c2-r45-monitor-entry.py` was run — the tool is absent at the
  tip and scoring is the closure's job, not this seat's.
- The privacy gate was read, never executed: its `--selftest` result is `ExecPrivacyGate`'s evidence. The
  draft's gate paragraph stays conditional on the L1 landing it at a tracked `quality/` path.
- No QUALITY criterion text, no SCORECARD/LOG rows, no counter or control edits (all frozen or L1-owned).

## Findings

1. **`PROVINCE.md:34` coverage claim is stale** — 12 tracked tools, 9 rows, three unrowed
   (`mado-eventq.py`, `mado-options.py`, `mado-wsrules.py`). Routed to the L1; the draft neither repairs nor
   hides it.
2. **The row is forward-looking** — `git ls-tree HEAD -- tools/mado-monitors.py` is empty, so the draft says
   in the file that the row is true only at the data commit (C1's kill rule decides) and must be re-read
   against the landed docstring if it differs from the reference.
3. **Locator fragility after integration** — the refinement's `mado-monitors.py:15` locator and the three
   `check-session-material.py:<n>` locators are line numbers in files that may be re-laid-out on landing;
   the draft carries an explicit instruction to recompute them rather than trust the numbers.
4. **Residual class, declared** — a verified quote at a verified locator does not prove the sentence around
   it (the standing C2 residual, same class as `c2-r45-monitor-entry.py`'s clause-j residual); `verify.py`
   binds text to receipts, not meaning to claim.
5. **No session material in the draft or receipts** — checked mechanically (finding shapes only, never
   values), so the draft is safe to integrate into the public repo.

## Artifacts

- `.ufo/waves/round-45/w1/ScrProvinceRow/province.md` — the draft (`d8f6406f126f9d5b73c226d9526968240efa63f351ad33551cebe1b8f0d06d6e`)
- `.ufo/waves/round-45/w1/ScrProvinceRow/verify.py` — the verifier (`37d50d3d…`)
- `.ufo/waves/round-45/w1/ScrProvinceRow/receipts/` — `verify.txt`, `quotes.txt`, `counters.txt`,
  `province-anchors.txt`, `tool-contract.txt`, `gate.txt`, `lane-clean.txt`, `sha256.txt`
- `.ufo/waves/round-45/w1/ScrProvinceRow.md` — this report

Report: .ufo/waves/round-45/w1/ScrProvinceRow.md
