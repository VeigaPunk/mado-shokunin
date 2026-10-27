# CritFrontier — round 48 w2 (FALSIFY): sources-census and lesson frontier step completeness

Seat `CritFrontier` (critic, leaf — no subagent dispatch). Lane `mado-shokunin`, freeze commit `3e6c848a`, base
`579f694b45c797a9c39761fdb4f9e0a1b71b3585`. No lane/tracked file edited; writes are this report and `w2/CritFrontier/`.
No package transaction, no install, no compositor verb, no `xdg-terminal-exec` run; `xkbcli` only as the frozen
counter's own replay (inside its scratch env). Scratch `/fast/scratch/hyaku/mado-r48/CritFrontier/` removed after
copying these receipts; largest output file written under the cap: `evidence/verify_rows.txt` 8 687 B (< 1 MiB);
total scratch 3.8 MB (< 2 GB).

## Verdict up front

The C2 data is **predicate-clean**: on a clean mirror of the landed bytes the frozen counter
`quality/counters/c2-r48-xkb-entry.py` scores `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 r:1 admitted=1
verdict=TARGET_MET` (replay ok, `sha=efd487a39920`, `neg=(1,1,0)`). The sources census re-run exits 0 and matches the
committed before/after receipts. Nothing found breaks the frozen predicate; the defects below are **fixable evidence/
lesson defects**, none requiring predicate narrowing. Smallest safe corrections are named per finding.

## 1. Row-Gate evidence for the newly added S ids (S340–S350)

Verified independently against the committed pins in `.ufo/waves/round-48/fetch/` (`w2/CritFrontier/verify_rows.txt`):

- All 11 rows: 11 cells, no empty cell, ids contiguous `S340`–`S350`, every declared sha256 matches its pin, every
  anchor range inside its pin's line count. **PASS.**
- Gate-line coverage: `l1-draft/gate-rows.md` admits S340–S346 and S348–S350 — **10 Gate lines for 11 new ids.
  S347 (xkeyboard-config symbols/br) has no Gate line**, and the landed lesson's pasted Gate block repeats the same
  10-line omission while claiming "The entry claims C2 on S340-S350".
  **Counterexample:** the Gate block itself is the strongest case — it presents itself as the row-Gate record for the
  round's admitted rows and silently skips one.
  **Evidence:** `grep -c '\*\*S3[0-9][0-9] admit\*\*' l1-draft/gate-rows.md` = 10; `gate-quotes-supplement.txt`.
  **Smallest correction:** append one S347 Gate line (the verbatim quote already exists and checks clean at
  `xkeyboard-config-symbols-br:47` — the entry's `**OBS** S347` line uses exactly it).
- Re-opened every Gate quote in its committed pin: 9/10 are unique, in range, word-bounded. **The S342 Gate quote is not
  verbatim**: the Gate block quotes `` `Couldn't find file "%s/%.*s" in include paths` `` while the C pin carries
  escaped quotes (`\"%s/%.*s\"`); normalized search returns 0 hits. The entry's own `**OBS** S342` correctly uses the
  escaped form — so the *scored* text is right and the *Gate evidence* is wrong, contradicting the lesson's own sentence
  "no landed quote spans or de-spaces a source line".
  **Smallest correction:** fix the two `"` → `\"` in the S342 Gate line (both in `l1-draft/gate-rows.md` and the pasted
  lesson Gate block).
- Gate provenance is misstated: the lesson says the pasted block is "emitted by `w1/ScrRows/gate-lines.md` … in the
  round-47 shape — receipt path, sha256, and a ≤25-word quote". The pasted block is actually `l1-draft/gate-rows.md`
  (no per-line sha256, no receipt path, different id↔source mapping); ScrRows' `quote-check.txt` (`checked=8 failed=0`)
  covered ScrRows' *own* 8-row mapping, not the pasted 10 quotes — so the pasted Gate lines were never instrument-checked
  (and one fails, above). **Smallest correction:** reword the provenance sentence to name `l1-draft/gate-rows.md` and
  drop the claim that the round-47 shape was kept (or add sha256/pin columns).

## 2. Reject Gate rows and flip conditions

`l1-draft/gate-rows.md` rejects 2 candidates, each with reason + flip:
ArchWiki `Xorg/Keyboard_configuration` and `xkbcommon.org/doc/current/index.html`. Both match
`w1/ScrRows/receipts/rejected-candidates.txt` sections A/B (A: 99 681 B, `xkbcommon=0`, `XKB-595=0`,
`XDG_CONFIG_HOME/xkb=0`, 11 `xkeyboard-config`, 3 man-page deferrals; B: 20 500 B, project number 1.13.2, `rmlvo=0`,
`include path=0`, `XKB-[0-9]=0`). Flips are testable ("version-pinned behavior not present in the primary bytes").
ScrRows' third reject (a ninth Hyprland `IKeyboard.cpp` row) was dropped from the L1 Gate doc; its evidence survives as
rejected-candidates.txt §C ("held, no new row") and the lesson's held-ground bullet — traceability note, not a gap.
**PASS (2/2 rejects evidence-backed, flips present).**

## 3. Lesson mistakes count

Landed `corpus/lessons/round-48.md` `## Mistakes` carries **8 rows: M48-1..M48-5** mined by `w1/ScrMistakes`
(verified against that seat's report and receipts) **plus M48-6/7/8** disclosed as "L1, attempt 2" additions. Sweep of
all 41 w1 seat reports finds no other `M48-*` claims, so the count is complete; the mandatory-mined-mistake rule is
satisfied fivefold. **PASS (count = 8, complete, disclosed).**

## 4. Census: exit 0 and before/after outputs

- `receipts/census-before.txt` and `receipts/census-after.txt` are **byte-identical**: 17 `W04` + 1 `W01` + `mado ok`,
  `exit=0`. Before was at base (276 rows; re-verified `git show 579f694b:corpus/SOURCES.md | grep -c` = 276); after at
  the integrated 287-row state.
- Live re-run (this seat): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` on the
  integrated working tree → **exit 0**, output equals census-after.txt apart from the receipt's appended `exit=0` line
  (`w2/CritFrontier/census-live.txt`). The 11 new rows add zero `W04`/`W01` (S350's own-work row is URL-less, as the
  validator allows). **PASS.**

## 5. Does a round claim rest on an opened S row?

**Yes — C2's admission mechanically rests on the opened rows.** The frozen counter's clause b requires ≥3 distinct
S340+ head rows present at REV (`mined`, opened `2026-10-26`, used-by the entry, absent at base), clause c requires
every head row pin-bound with a matching sha256, and clause g requires the README row to cover all ids. My clean-mirror
run of the frozen counter confirms all of these pass on the landed bytes (`admitted=1 TARGET_MET`). Drop or mal-form
one opened row at the data commit and C2 misses — that is the claim resting on the rows.
**But the claim's substance does not rest on row prose**: clause d quotes are checked entry-vs-pin, clause f/r re-run
`xkbcli` live and byte-compare the keymap digest, and unscored cells (e.g. `teaches`) could be false without moving the
verdict. **C1 rests on no opened row** (separability; the C1 counter reads only tool, fixtures and the round-47 pin).

## 6. Lesson frontier step completeness — defects (fixable; none predicate-breaking)

- **F1 — wrong README locator, twice.** Lesson "Registry changes" and Frontier item 5 put the new Frontier bullet at
  `corpus/README.md:110`; the landed bullet is at **:112** (:110 is the round-47 bullet). The index row did land "after
  :75" as claimed (:76). **Smallest correction:** `:110` → `:112` in both places.
- **F2 — the landed Frontier bullet is not the lesson's draft, and the redaction is unrecorded.** The lesson quotes a
  drafted bullet "Round 48 moves **two edges** onto executed ground" (C1 warm cache + C2 XKB) with three "Still open"
  items (the cache `ls -LRl` same-size/same-minute question, the launch half of the round-17 `[UNK]`, the terminal's own
  argument handling). The L1 landed a **C2-only** bullet at :112; the C1 sentence and all three still-open items are
  gone, so after the data commit `README.md:110` still lists "the warm-cache path" as still open while `claims.md`
  declares C1's surface moved "frontier → core". The lesson never records the redaction, so the frontier step is
  incomplete as written. **Smallest correction:** either restore the two-edge bullet text (it fits the append-only
  convention as a new bullet) or amend Frontier item 5 to state what was actually landed and where the three still-open
  items are now recorded.
- **F3 — stale spot-check shape.** The lesson's Spot-check item 4 says "the five gate decisions above (**three admits,
  two rejects**)"; the Gate has 10 admits + 2 rejects. **Smallest correction:** "twelve gate decisions (ten admits,
  two rejects)".
- **F4 — ambiguous claim-support sentence.** Frontier item 4: "C1's oracle is the row-47 pin **those rows** already
  hold" — "those rows" reads as S340-S350, which are libxkbcommon/xkeyboard-config rows and do not hold the resolver
  pin (it is held by S326/S327). **Smallest correction:** "the round-47 pin the registry already holds (rows S326/S327)".
- **F5 — committed mirror receipt ends in a traceback.** `receipts/l1-c2-mirror.txt` (committed at the freeze) ends
  with `FileNotFoundError` in clause r because its TMPDIR replay dir did not exist; it carries no final verdict line.
  The run is environmentally broken, not predicate-failing — my re-run with a valid TMPDIR reaches
  `admitted=1 TARGET_MET` (`w2/CritFrontier/counter-mirror.txt`). **Smallest correction:** re-capture the receipt with a
  pre-created TMPDIR replay dir so the committed evidence shows the final label.

## What is NOT defective (attacks that failed)

- Entry quotes: all 21 located quotes in the landed entry (every `**OBS**` line + step locators) are verbatim, in
  range, and resolve to row-cited pins — including the correctly escaped S342 forms.
- S350: the fetch copy is byte-equal to the receipt; the `^<sha256>  host.keymap` digest line exists; the Gate locator
  `receipt:57` reads `rc=0` as claimed.
- Held material: S318/S319 rows and `hyprland-input-devices-r46.md` byte-equal to base (counter clause h = 1).
- Rows: insert-only append after `| S339 |` (`git diff` shows 11 `+` lines, 0 deletions), 287 rows, top S350.
- README row: one three-cell row, no redirect words, lists S340–S350 (clause g = 1).
- Base state: entry absent at base, `S340` absent at base, ground terms absent at base (clauses a/b/i = 1).
- w2 dispatch enforces the scratch bound (`ulimit -f 2048` present in all 49 seat tasks) — M48-5's fix verified live.

## Evidence index (this seat dir, `w2/CritFrontier/`)

| file | what |
|---|---|
| `verify_rows.txt` | 11-row cell/sha/anchor checks + Gate coverage + 21 entry quotes vs pins (2 FAILs: S347 gate line, S342 gate quote) |
| `gate-quotes-supplement.txt` | per-Gate-quote uniqueness/in-range table + S350 receipt locator |
| `census-live.txt` | live `sources-census.sh validate` on the integrated tree, exit 0 |
| `counter-mirror.txt` | frozen counter on a clean mirror of the landed bytes: `admitted=1 TARGET_MET` |

No installs, no host mutation, no lane git/jj mutation. Scratch deleted after the receipts above were copied.
