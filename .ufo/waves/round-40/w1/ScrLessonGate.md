# ScrLessonGate — round-40 lesson `## Gate` draft (w1)

STATUS: complete. Draft delivered at
`.ufo/waves/round-40/w1/ScrLessonGate/gate.md` (27,922 B, sha256
`b41e2341d05b4073e7981dc0e61293a0964178cf936dcedd27cd0a4d2bc2e806`). No verdict was recorded by
this seat: every assimilation verdict slot and every "L1 fills" slot is open.

## Behavior

Drafted, in the shape of `corpus/lessons/round-39.md` `## Gate`:

1. **Gate lines for the four ids C2 cites** — S162 and S173 as ready-to-paste lines (their receipts
   exist and their digests are byte-identical to the round-39 receipts), plus templates for the two
   new rows (the pinned `ComplexDataTypes.hpp` row and the own-work live-census row) with the
   `sha256`/`quote` fields the L1 fills.
2. **What one line must satisfy**, read off the frozen counter (`PRED-C2-r40-v1` clauses b/d/g): FETCH
   prefix, digest bound at REV, 3–25 words, `norm(quote)` in `norm(receipt)`, one entry line carrying
   the id and the quote, ≥4 distinct `source:` ids in the entry's first 20 lines.
3. **Assimilation ledger** for K1 `host-bar-producers-r28.md` and K2 `host-producer-outputs-r29.md`:
   provenance bytes, scope check against `PROVINCE.md`, QUALITY bar check against named criteria from
   `corpus/QUALITY.md` 1–64, held-coverage check against `corpus/knowledge/waybar-walker-semantics.md`,
   an **OPEN** verdict slot, a draft reason, and a flip condition for each.
4. **D2 correction note** for the round-39 S224 label, append-only.
5. A fill/decide table for the L1.
6. A **paste-ready `## Gate` skeleton** (§7) with the four lines and the round-39 house paragraph,
   so integration is a copy with two placeholders filled.

## Findings (each names what it attacks)

**F1 — the counter's normalizer deletes the sentence the gradient output shape rests on.**
`quality/counters/c2-r40-forms-entry.py:79-83` strips `<[^>]+>` before comparing. On
`.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin` (6116 B) this deletes one span, raw
offsets 1833–2227, which begins at `i < m_colors.size(); ++i)` and ends at a later `->`; the
normalized file is 4095 B and `CGradientValueData::toString` (`:69-77`) is gone. Measured:
`result += std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI));` → **occ = 0** in `norm(receipt)`,
so it can never be a Gate quote. Attacked: the C2 entry's `<hex> … <N>deg` claim cannot be Gate-bound
to the ComplexDataTypes row; it needs a prose citation plus a bindable quote (the CSS-gap sentence at
`:134`, occ 1, 9 words). Same hazard makes quotes with balanced `<…>` bind only accidentally (the
hyprlang signature at `:185`, occ 1).

**F2 — both held rows C2 re-opens declare location ranges that exclude the sentences relied on.**
S162 (`corpus/SOURCES.md:174`) declares `:419-451,590-623,893-968,2016-2093`; the gradient handler is
`:103-165` and its custom-type registration `:510`/`:2178` — all outside. S173 (`:185`) declares
`:619-667,755-827,983-986`; `configStringToInt` is `:185-273` — outside. The inherited gap is wider
than this round: round-39's own S173 Gate quote is `:869`, also outside its ranges (1 occurrence,
measured). Attacked: the registration's sentence "held S162 (ConfigManager.cpp gradient handler,
re-opened)". Clause c forbids widening a held row this round, clause d does not check cell 1, so the
§2.1 lines pass the counter while the row's declared anchor stays narrow — a QUALITY 2/42 and 27
defect the lesson must record. Three dispositions given (D-a cite-and-record, D-b add exact-region
rows with the QUALITY 17 same-URL screen, D-c bind only inside the declared ranges); this seat
recommends D-b but records no verdict.

**F3 — the registration's held-coverage datum for the upstream config is not in the lane.**
"6354 B host, 5114 B upstream is held": `6354` occurs nowhere in `corpus/`; the only `5114` is a
*local backup* size (`corpus/knowledge/waybar-walker-plane.md:297`,
`config.jsonc.bak.1791314470`, 2026-10-03). No upstream `v3.8.4` config fetch exists in
`.ufo/waves/round-40/fetch/`. Attacked: K1's S231 comparison claim and the registration's held claim.

**F4 — K1 contradicts itself on the producer count, and host bytes side with the table.**
K1's table lists seven `json` elements; its INF says "six JSON producers".
`grep -c '"return-type": "json"' ~/.config/waybar/config.jsonc` → **7** (this seat). K2 says "five".
Attacked: both candidates (QUALITY 14).

**F5 — K1's amendment parent does not exist in the lane.** `grep -rn 'host-bar-and-idle-binding'
corpus/` → 0 hits; `ls corpus/knowledge | grep -i 'host-bar\|producer'` → no match. K2 amends K1,
which is itself unadmitted. Attacked: both candidates' "amends" clause (QUALITY 8).

**F6 — K1's S228 duplicates held row S207's bytes.** Lane S207 (`corpus/SOURCES.md:209`) holds the
host `idle.sh`, 159 B, sha `6d8d2c11…`; K1's S228 is the upstream `v3.8.4` file with the same bytes.
Same bytes, different locator class → the QUALITY 17 screen is required and was not recorded.

**F7 — the held entry's coverage is narrower than the registration assumes, and its anchors have
shifted.** `grep -c gkeep corpus/knowledge/waybar-walker-semantics.md` → **0**; held's `modules-right`
is "7 entries `:21-29`" (`:79`) while today's config has 8 with `custom/gkeep` at `:23` and its block
at `:236-245` (6354 B, sha `a408a33d…`, mtime 2026-10-17 17:02:56, after held's 2026-10-14
measurement), shifting held anchors after `:235` by +11 (held's `custom/ai-usage (:235-248)` is today
`:246-259`). Supports: K1's one genuine increment (the gkeep element/producer).

**F8 — K2's S241 anchor is the volatile class D2 corrects.** `grep -c '2026-10-23T22:52:44Z'
~/.cache/ai-usage/status.json ~/.cache/ai-usage/inception-ledger.json` → `0`, `0`; live
`updated_at` is `2026-10-25T20:52:19Z`. K2's S237/S238, by contrast, are the strongest bytes on this
theme in-round: 169 B / 174 B, tag-pinned, host copies `cmp`-identical, and `v3.8.3` serves the same
sha256 (`sha256sum` on `w1/ExecFetchK2Sources/v3.8.3-*.bin` equals `fetch/omarchy-v3.8.4-*.bin`).

**F9 — K2's idle sentence is reversed by today's host state.** K2 says the idle chip shows "Idle lock
disabled" because no `hypridle` runs; `pgrep -a -x hypridle` → `1680 /usr/bin/hypridle`
(`w1/ExecK2HostReads/host-reads.txt` §4). A round-3 RUN payload is dated, not standing.

**F10 — three rows have carried the id S224.** Package `SOURCES.append.md:28` S224 = host waybar
config; absent-defect-register S224 = ai-usage cache; lane S224 = none
(`w1/ExecQuarantineSlice/registry-rows.txt`). The D2 note names which one it corrects.

## Gates / checks run by this seat

- Quote binding, replayed against the counter's own `norm()` and `GATE_RE`: each candidate's word
  count, occurrence count in `norm(receipt)` and full regex round-trip (`m.group(4) == quote`).
  Results in `gate.md` §2.3; two candidates rejected on measurement (`:77` occ 0; `:510` 2 words,
  occ 2).
- Line pins re-derived with `grep -nF` on the receipt bytes: `:117`, `:120`, `:129`, `:607` (ConfigManager),
  `:196`, `:259` (hyprlang), `:134`, `:148`, `:159` (ComplexDataTypes). One draft pin was wrong
  (`:152` → `:148`) and was corrected in the draft.
- Forms histogram independently recomputed from `.ufo/waves/round-40/c1/native-capture.jsonl`
  (sha256 `1fe39c0528f1b11d7f69bf41ac236f39ff6e00b9b8a275f4e94b06c5189b4b25`, 70 non-blank lines,
  every line exactly one form key): `int 44, float 5, custom 13, str 8`, sum 70 — the clause-h
  `forms` line as drafted. The `labels` line was **not** filled (census seat's).
- Digest equality with the round-39 receipts: `9db68cf4…` (S162) and `fa1b6898…` (S173) — byte-identical
  re-fetches.
- Read-only host reads: `stat`/`sha256sum`/`grep` on `~/.config/waybar/config.jsonc` (6354 B,
  `a408a33d…`), `grep -c '^  "custom/'` → 10 elements, `grep -c '"return-type": "json"'` → 7,
  `pgrep -a -x hypridle` (via the sibling seat's capture, cited), the ai-usage cache greps above.
- Not run by this seat: `PRED-C1-r40-v1`, `PRED-C2-r40-v1`, the controls, `mado-verify.sh`,
  `check-index.py`, `check-axis-scores.py`. Their verdicts are the L1's to produce.

## Touched surfaces

Written (this seat only):
- `.ufo/waves/round-40/w1/ScrLessonGate.md` (this report)
- `.ufo/waves/round-40/w1/ScrLessonGate/gate.md` (the draft)

Read-only, outside the write scope: `/home/vgpnk/Projects/shokuknow/merge/mado/**` (the two
candidates, `SOURCES.append.md`, `MERGE-REPORT.md`), `~/.config/waybar/config.jsonc`,
`~/.cache/ai-usage/status.json` (grep/stat only — no values printed), and sibling seats' files under
`.ufo/waves/round-40/` and `.ufo/waves/round-39/` (quotes.md, host-reads.txt, verdicts.md,
registry-rows.txt, timings).

Nothing was written outside the lane; no config tree, compositor state, service, sibling lane,
`templates/`, `scripts/`, `MANIFEST.json`, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/` or the
jj/git index was touched. No mutating git/jj verb was run (no `git` command at all in this seat). No
compositor verb beyond the read-only ones (`hyprctl version` was not needed by this seat — it used no
compositor verb; the `hypridle`/`waybar` facts are quoted from the sibling seat's capture).
No package transaction; **no tool installed or updated** (nothing was needed).

## Out of scope / left to others

- The two new registry rows, the entry, the README index row and the lesson text itself (L1).
- The live-census receipt under `fetch/` and its `labels` line (census seat).
- K1/K2 verdicts, and the S162/S173 anchor disposition (L1).
- The id-collision guard run and the quarantine-slice re-derivation (`ExecAssimIdGuard-2`,
  `ExecQuarantineSlice`) — this seat only screened the collisions it touched (F10).
