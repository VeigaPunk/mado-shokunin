# ScoutCensus — round 48 / w2 FALSIFY: source census before vs. after on the C2 candidate

Seat `ScoutCensus`, leaf, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`; freeze commit `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d`
(`git diff --stat 579f694b 3e6c848a -- corpus` is empty, so the base corpus *is* the frozen corpus).
Instrument: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, sha256
`3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`; its own `selftest` was run and is
`96 killed / 0 SURVIVED / selftest ok`, exit 0 (`census-selftest.txt`).
No package transaction, no install, no lane Git/jj mutation, no host-service touch. Scratch
`/fast/scratch/hyaku/mado-r48/ScoutCensus*` was created, used and removed (largest scratch file
`corpus/SOURCES.md` 251 414 B `<` the 1 MiB guard; whole extracted tree 2.6 MB `<` 2 GB).

## Method

1. **BASE** — `git -C <lane> archive 579f694b corpus | tar -x -C $D` plus the eight non-`corpus/`
   `used-by` targets the registry names (`quality/check-index.py`, `SKILL.md`, `tools/mado-binds.py`,
   `tools/mado-verify.sh`, `tools/mado-wsrules.py`, `.ufo/waves/round-29/registration.md`,
   `.ufo/waves/round-30/registration.md`, `.ufo/waves/round-47/w1/ExecSupersede/rows.md`). Archive into a
   plain directory, no clone, no index write (a full `git clone` checkout aborts under the mandated
   `ulimit -f 2048`: `fatal: unable to checkout working tree`, recorded in `run-census.sh` history).
   Extracted `corpus/SOURCES.md` = `6a71f3a4…9b62`, byte-equal to `git show 579f694b:corpus/SOURCES.md`.
2. **MIRROR** — same tree plus the candidate bytes: `l1-draft/xkb-keymap-compile-r48.md`, the eleven rows of
   `l1-draft/rows-c2.md` inserted after `| S339 |`, `l1-draft/readme-row.md` inserted after the r47 README
   row, and `fetch/`, `receipts/`, `tools/` copies. Mirror `corpus/SOURCES.md` = `ddc44fd4…510c0`.
3. Both runs: `bash sources-census.sh validate --file <tree>/corpus/SOURCES.md` and
   `bash sources-census.sh census --file <tree>/corpus/SOURCES.md`, full stdout kept, exit code recorded
   (`revs.txt`). `ulimit -f 2048` in every writer shell.

## Census before / after (full outputs retained)

| | BASE | MIRROR |
|---|---|---|
| `validate` exit | **0** | **0** |
| `census` exit | 0 | 0 |
| rows | 276 | **287** (+11) |
| tier.A / B / C / invalid | 265 / 4 / 7 / 0 | **276** / 4 / 7 / 0 |
| status mined / queued / rejected / invalid | 257 / 10 / 9 / 0 | **268** / 10 / 9 / 0 |
| W01 | 1 (`S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md`) | **1, identical** |
| W03 | 0 | **0** |
| W04 | 17 | **17, identical set** (`comm -13` of the two W04 sets is empty) |
| E01–E12 | **0** | **0** |
| last line | `file  ok  …/corpus/SOURCES.md` | `file  ok  …/corpus/SOURCES.md` |

The BASE run reproduces the frozen `receipts/census-before.txt` exactly: the only diff is the receipt's
lane prefix (`mado` vs `file`), its absolute path, and the receipt's trailing `exit=0` echo line.
Files: `base-census-validate.txt`, `mirror-census-validate.txt`, `base-census.txt`, `mirror-census.txt`.

## Column, id and duplicate checks on the candidate rows

`rows-structure.txt` / `new-id-scan.txt`:

- 11 new row lines, ids `S340,S341,…,S350` contiguous, **zero duplicate ids** (`registry_rows=287
  distinct_ids=287`).
- every new line splits into 13 `|`-fields = **11 columns** + the two empty edge fields; no embedded `|`
  in any cell; declared values uniform: `tier=A`, `status=mined`, `opened=2026-10-26`,
  `recheck=on-release`, `used-by=corpus/knowledge/xkb-keymap-compile-r48.md`.
- the eleven URLs are pairwise distinct (`new_url_groups_repeated={}`), which is why no new W04 appears;
  `S340`'s URL is unique against the 276 base rows as well (no E04 in the candidates).

**Negative controls** (candidate rows only, scratch copies; `ctl-a-no-entry.txt`, `ctl-b-dup-id.txt`,
`ctl-exits.txt`): dropping the entry file gives exit 1 and `E11` **11/11** for S340–S350
(`ctl-a-e11-count.txt`), so the rows' `used-by` binding is actually enforced; duplicating the `S340` line
gives exit 1 with `E03 S340 duplicate id` and `E04 S340 duplicate url … within scope`. The observed
“no E03/E04, all W” result is therefore not vacuous: any id/URL/useb-y defect in these rows would have
turned the candidate census red.

## Lesson Gate per-row quote check (`gate-quote-check.txt`, `check-gate-quotes.py`)

Rule applied (same wording as `corpus/lessons/round-47.md:11`): one line per admitted row, access date,
≤ 25-word quote, locator that is a `grep -n` hit on the committed pin. Verdict per row, with the quote
resolved against the exact cited line:

| row | locator | words | verdict |
|---|---|---|---|
| S340 | `fetch/xkbcommon-rules.c:1259` | 8 | pass (1 occurrence) |
| S341 | `fetch/xkbcommon-xkbcomp.c:157` | 5 | pass |
| S342 | `fetch/xkbcommon-include.c:355` | 7 | **fail — quote not in pin** |
| S343 | `fetch/xkbcommon-context.c:503` | 3 | pass |
| S344 | `fetch/xkbcommon-context-priv.c:218` | 10 | pass |
| S345 | `fetch/xkbcommon-meson_options.txt:46` | 2 | pass |
| S346 | `fetch/xkeyboard-config-rules-rules.in:243` | 1 | pass (3 occurrences in pin; locator explicit) |
| S347 | — | — | **missing Gate line** |
| S348 | `fetch/xkbcommon-tools-compile-keymap.c:587` | 3 | pass |
| S349 | `fetch/xkbcommon-messages-codes.h:150` | 3 | pass |
| S350 | `receipt:57` | 1 | pass (27 `rc=0` occurrences; explicit locator) |

`GATE_QUOTES: checked=11 passed=9 failed=2 missing=1`.

## Findings (pre-data, so every one is still repairable by L1)

1. **F1 — S347 has no Gate line.** `l1-draft/gate-rows.md` heads itself “rows S340-S350” but carries ten
   bullets; S347 (`xkeyboard-config 2.48 symbols/br`) is absent, and there is no aggregated delegation
   sentence of the round-47 `S332-S339` kind that would cover it. The entry does have a verbatim,
   located quote for the row: `xkb_symbols "nodeadkeys" {` at `fetch/xkeyboard-config-symbols-br:47`
   (grep hit, line 47), matching the row's anchor `xkeyboard-config-symbols-br:47` and entry OBS line 62.
   The old `w1/ScrRows/gate-lines.md` S347 line cannot be reused: it quotes `xkbcommon.h:462` for a
   different (pre-renumbering) S347. Fix: add the one bullet.
2. **F2 — S342's Gate quote is not verbatim.** The drafted quote is
   `Couldn't find file "%s/%.*s" in include paths`; the pin line 355 is
   `                "Couldn't find file \"%s/%.*s\" in include paths\n",` — the drafted form occurs
   **0 times** in `fetch/xkbcommon-include.c`. The entry itself is safe (OBS line 53 uses the escaped
   `\"` form, which is what the frozen counter's `clause d` would collapse and match), so this is a
   Gate-prose defect only, not a predicate break. Fix: quote the escapes (and optionally the trailing
   `\n`) as in the entry.
3. **F3 (informational, not a failure)** S350's one-word `rc=0` has 27 hits in the receipt. The round-47
   rule needs a `grep -n` locator, which `receipt:57` supplies, and the surrounding text names the
   positive `--layout br --options compose:caps` case, so the line is locatable; it would fail only a
   stricter “unique quote” rule, which this Gate header does not claim.
4. **F4 (lane state, not mine)** the lane worktree is not clean: `corpus/SOURCES.md` already carries the
   same eleven S340–S350 lines uncommitted (`git diff HEAD` rows are byte-equal to `l1-draft/rows-c2.md`),
   alongside modified `corpus/README.md`, `corpus/QUALITY.md`, `tools/mado-terminal.py`,
   `quality/check-session-material.py`, `SKILL.md` and lesson/monitor files. My before/after is computed on
   the committed base plus the draft bytes only; anything integrated from that worktree rather than from
   `l1-draft/` would not be the tree I measured.

No predicate miss for the census: on the proposed candidate the frozen census is `exit 0` with `ok`,
W01/W04 unchanged and no E code, so the rows are admissible as far as this instrument goes. F1/F2 are
lesson-draft gaps, not census misses; neither changes a counter, fixture or claim.

## Files changed

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w2/ScoutCensus.md` (this report)
- `.ufo/waves/round-48/w2/ScoutCensus/`: `run-census.sh`, `run-controls.sh`, `check-gate-quotes.py`,
  `revs.txt`, `base-sources.sha256`, `base-sources-gitshow.sha256`, `mirror-sources.sha256`,
  `base-rowcount-all.txt`, `base-rowcount-S3xx.txt`, `mirror-rowcount-all.txt`,
  `mirror-rowcount-S3xx.txt`, `lane-worktree-rowcount-all.txt`, `rows-structure.txt`, `new-id-scan.txt`,
  `base-census.txt`, `base-census-validate.txt`, `mirror-census.txt`, `mirror-census-validate.txt`,
  `census-selftest.txt`, `ctl-a-no-entry.txt`, `ctl-a-e11-count.txt`, `ctl-b-dup-id.txt`,
  `ctl-exits.txt`, `gate-quote-check.txt`, `summary.txt`, `largest-output.txt`.

Largest evidence file: `run-census.sh` 5 249 B (largest census output `ctl-b-dup-id.txt` 3 456 B); no file
near 1 MiB.

## Risks / blockers

- The census cannot read the lesson; F1/F2 were checked by a seat script against the pins, so they are
  prose-level until L1 lifts `gate-rows.md` into `corpus/lessons/round-48.md` — re-run the check on the
  lifted text, not on the draft.
- The mirror is an uncommitted overlay (no fixture identity is claimed); the census resolves `used-by`
  against the overlay's parent dir, which is why the eight non-`corpus/` targets were extracted. A
  differently rooted mirror would add spurious E11 lines.
- Nothing blocked; no installation was needed.
