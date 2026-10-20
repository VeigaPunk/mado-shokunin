# Reopen S067 — `hypridle src/core/Hypridle.hpp @ v0.1.8`

Lane: `mado-shokunin` @ `988b858bd6049bc709807534fd725c05264f7e60` (read only).
Assignment: re-open source row S067, verify URL / verbatim quote / digest / tier / status /
verdict, and verify every claim the citing note makes from this source at its anchors.
**Result: attack failed. No counterexample found.** Every checked claim is byte-exact at
the stated anchors.

## Fetch (raw bytes)

```
curl -fsSL -o /tmp/hypridle-core-Hypridle.hpp \
  https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.hpp
```

- URL resolves: raw endpoint HTTP 200; `https://github.com/hyprwm/hypridle/releases/tag/v0.1.8`
  also HTTP 200 (tag exists, so this is not a branch fallback).
- 3611 bytes, 105 lines, LF endings (no `^M`).
- Assignment-supplied digest reproduced exactly.

## Digest — three-way identity

| origin | value |
|---|---|
| sha256 of fetched bytes | `f9e4e5587075fe34ae3279c4225b00661c686468035c4ad6cbe71e098fc0a2b8` |
| `corpus/SOURCES.md:79` anchor cell | `f9e4e5587075fe34ae3279c4225b00661c686468035c4ad6cbe71e098fc0a2b8` |
| `corpus/lessons/round-17.md:54` (gate) | `f9e4e5587075fe34ae3279c4225b00661c686468035c4ad6cbe71e098fc0a2b8` |

`ALL-THREE-IDENTICAL`. Full 64 lowercase hex in both lane files; no truncation, no typo.

## Row verification — `corpus/SOURCES.md:79`

11 columns, matching the registry header at `corpus/SOURCES.md:11`.

- **URL** — identical to the assignment URL, `…/hypridle/v0.1.8/src/core/Hypridle.hpp`
  (case-exact `Hypridle.hpp`; the distinct `.cpp` row S066 is separately present).
- **kind `code`, tier `A`** — tag-pinned upstream source file, consistent with tier-A
  treatment of the other pinned upstream raw files in this block.
- **anchor `file lines 23, 26`** — both lines exist and both hold the claimed fields
  (verified below). Lines 23 and 26 lie inside `struct SIdleListener` (opens line 19,
  closes line 29).
- **teaches `per-listener ignoreInhibit and conditionRetry state`** — `SIdleListener` is
  instantiated per rule: `Hypridle.hpp:84` `std::vector<SIdleListener> listeners;`, and
  `Hypridle.cpp:66-72` copies `RULES[i]` into `listeners[i]` field by field. So "per-listener"
  is literal, not inferred from the struct alone.
- **status `mined`** — the row is actually consumed by the note named in its `used-by`
  cell (claims below), so the status is honest rather than aspirational.
- **opened `2026-10-20`, recheck `on-change`, used-by `corpus/knowledge/idle-lock-route-r17.md`**
  — note exists; its `verified-at` is also `2026-10-20`; it lists S067 as one of the five
  tag-pinned raw URLs its recheck covers.

## Gate verification — `corpus/lessons/round-17.md:54`

Row: `| S067 | <URL> | [HH:23] `ignoreInhibit     = false;` | `f9e4…a2b8` |`

- **Anchor** — `[HH:23]`; the note's legend (`idle-lock-route-r17.md:23`) defines
  `[HH:n]` = file line. Line 23 is inside `SIdleListener`.
- **Quote is byte-verbatim at line 23** — `grep -boF` locates
  `ignoreInhibit     = false;` at byte offset 36 of line 23, exactly once in the file
  (`ignoreInhibit` occurs on 1 line only). The five internal spaces between the
  identifier and `=` are preserved; 26 characters, **3 words ≤ 25**.
- **Digest** — identical to the fetched bytes (table above).
- **Verdict** — the gate table carries no verdict column; S067 sits in the admitted
  "New rows" block (S056–S070, 15 rows), and only S070 is annotated `(rejected)`.
  The gate's aggregate line reconciles with that reading: rows 55→70 (+15),
  tier A 51→63 (+12) and C 3→6 (+3) = +15; mined 43→55 (+12) and rejected 4→7 (+3) = +15.
  S067 is one of the 12 added tier-A mined rows. Tier A / status mined / admitted —
  consistent.

Exact line evidence (`awk 'NR==23||NR==26'`):

```
23:[        bool                        ignoreInhibit     = false;]
26:[        int64_t                     conditionRetry    = 0;]
```

## Claims the citing note makes from this source

Only two anchors in `corpus/knowledge/idle-lock-route-r17.md` cite `HH`:

- **line 48** — "`bool ignoreInhibit = false;` [HH:23]; copied from the rule at [HC:70]".
  Line 23 is precisely `bool … ignoreInhibit = false;` (the note's rendering is
  whitespace-compacted; see residual note). `Hypridle.cpp:70` is exactly
  `l.ignoreInhibit  = r.ignoreInhibit;` — the copy claim holds.
- **line 49** — "`l.conditionCmd = r.conditionCmd;` [HC:71], `conditionRetry` [HH:26]".
  `Hypridle.cpp:71` is exactly `l.conditionCmd   = r.conditionCmd;`; line 26 declares
  `int64_t conditionRetry = 0;`. Both hold.
- **line 46** (same section, cross-source but touching this field) —
  `if (g_pHypridle->m_iInhibitLocks > 0 && !pListener->ignoreInhibit) {` at `[HC:301]`:
  `Hypridle.cpp:301` is byte-identical.
- Roster line 1 describes S067 as "(SIdleListener)" — accurate.

Cross-check on the neighbouring row: the `.cpp` fetched in the same pass digests
`2dd4d73d4f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75`, which equals S066's
recorded digest — independent evidence that the tag-pinned raw fetches are stable and
that S067's digest was not copied from a sibling by mistake.

Wave-1 artifact agreement (not authority, corroboration): `.ufo/waves/round-17/w1/reports/
SourcesUsedByJoin.md:104` records S067 as `f9e4e558…`, 3611 B, `mined / A`, used at note
line 1 token 5 — all matching.

## Attack surface traversed (all failed to falsify)

1. Wrong URL / wrong tag / branch fallback — raw and release-tag endpoints both 200;
   content is real hypridle source.
2. Digest transcription or truncation — three-way exact match, 64 hex.
3. Anchor drift — lines 23/26 are stable at the recorded digest and inside `SIdleListener`.
4. Quote not verbatim — exact substring with internal spacing, unique occurrence.
5. Quote over 25 words — 3 words.
6. "per-listener" overclaim — disproved only by struct reading? No: `vector<SIdleListener>`
   plus per-index `RULES[i]` copy at cpp:66-72 confirm it.
7. Note misquotes / misplaced anchors — both `HH` anchors and both `HC` cross-anchors exact.
8. Tag/row confusion between `.hpp` (S067) and `.cpp` (S066) — digests and line contents differ,
   each row points at its own file.
9. Status inflation — `mined` is backed by actual note usage; no "verified"/"observed"
   language is claimed anywhere for this source.
10. Gate arithmetic hiding a rejected row — counts reconcile exactly with 12 A + 3 C.

## Residual unknowns / limitations

- `api.github.com` returned HTTP 403 for the tag ref, so tag→commit-SHA resolution was not
  available; the 200s on the raw and release endpoints plus digest match are the evidence used.
  [OBSERVED limitation; no falsification.]
- No tier A/B/C legend exists inside this worktree (S004 points to fleet-ledger
  `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`, absent here). Tier A for a tag-pinned upstream
  source rests on the registry's own precedent, not a local definition.
- The note's line 48 rendering `bool ignoreInhibit = false;` is whitespace-compacted versus
  the byte-verbatim column alignment. Semantically and token-wise exact; the gate quote itself
  is byte-exact. Non-falsifying formatting nit only.
- `conditionRetry` is a prefix of `conditionRetryAt` (line 28); line 26 is nevertheless the
  exact field declaration, so the anchor is unambiguous.

## Compliance

- Installs: **none** (no pacman/yay/sudo/uv/npx/pip; no binary probes, no compositor/system
  queries; host and network reads only: `curl`, `cat`/`sed`/`grep`/`awk`/`sha256sum`/`stat`/`wc`).
- No git mutation, no jj, no delegation, no lane file edits other than this report.
- Confidence: **high** on URL, bytes, digest, anchors, quote, tier/status/admission, and the
  citing note's claims; **medium** only on the absent local tier-legend definition (not a row defect).
