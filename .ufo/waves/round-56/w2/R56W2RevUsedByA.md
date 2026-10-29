# R56W2RevUsedByA — reliance review of the C3 registry fix at 28fc86ac

Seat: R56W2RevUsedByA (leaf, no subagents). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, scored tree `28fc86ac2359ec27406d8a2c63bef82ea6e947ed` (read via `git show <rev>:<path>` only; working tree never read for scored content).
Receipts: `.ufo/waves/round-56/w2/R56W2RevUsedByA/` (pair derivation, citing-line dumps, recompute outputs, cell-only check, receipt check).

## 1. Scope derivation

- Pairs the fix added: `git diff 13f0acbe3a15da2d9c08357a576d91dcadc85273 28fc86ac2359ec27406d8a2c63bef82ea6e947ed -- corpus/SOURCES.md`, diffed per row's cell 11 (`used-by`), split on commas and whitespace. Result: 50 added (S, path) pairs in total, of which 9 are new rows S383-S391 (excluded by the brief). **41 remain** (`R56W2RevUsedByA/pairs41.json`).
- Sort order (S-id, then entry path). **First 21** (`R56W2RevUsedByA/first21.json`):

| # | pair | # | pair |
|---|---|---|---|
| 1 | S015 walker-route-r18.md | 12 | S090 walker-deep-r9.md |
| 2 | S041 input-debugging-boundaries-r15.md | 13 | S090 walker-deep.md |
| 3 | S046 output-colour-boundaries-r14.md | 14 | S090 walker-live-surface.md |
| 4 | S057 terminal-trees-r23.md | 15 | S090 waybar-walker-plane.md |
| 5 | S059 xdg-terminal-selection-r47.md | 16 | S090 waybar-walker-semantics.md |
| 6 | S060 xdg-terminal-selection-r47.md | 17 | S091 arc-synthesis.md |
| 7 | S073 walker-deep.md | 18 | S091 walker-deep-r9.md |
| 8 | S090 arc-synthesis.md | 19 | S091 walker-deep.md |
| 9 | S090 closeout-r11.md | 20 | S091 walker-live-surface.md |
| 10 | S090 config-health-report-r3.md | 21 | S091 waybar-walker-semantics.md |
| 11 | S090 remaining-planes-census.md | | |

- Cross-check of the derivation: the 41 pairs equal exactly the 41 base-missing pairs that are not allowlisted (`basemissing.out`: `added - base_v2 = []`, `base_v2 - added = []`).

## 2. Method

1. Formed my own label for each of the 21 from the citing lines at `28fc86ac`, fenced code excluded, token rule as in `CITE`. Each line was read in full (`first21_full.txt`) and, where needed, in its surrounding paragraph (`ctx.out`, `u4.out`, `u4b.out`).
2. Only after labelling did I open the wave-1 labels: `w1/R56RevC3Contract/classification.json` and `w1/R56CritCiteDef/pairs-65.tsv` (`compare.out`, `all41.out`).
3. Definitions used. RELIANCE = the entry uses the row's content, anchored line pointer, receipt or bytes as evidence, or asserts a claim whose support is that row. NAME-ONLY = the id is used to refute, supersede, redirect, disclaim or point to another note's use.

## 3. Per-pair decisions (first 21)

Each row: my label; registry decision (filled = reliance); agreement; quoted citing line (≤25 words).

| # | pair | my label | agree with fill? | quoted citing line (≤25 words) |
|---|---|---|---|---|
| 1 | S015 walker-route-r18 | RELIANCE (procedural, method basis) | agree; hedged | "Per the S015 protocol, these moved pins are reported with old and new values." (L236) |
| 2 | S041 input-debugging-r15 | RELIANCE (content: retained record) | agree | "S041 retained only `wl_seat` interface/version 9, not capability bits" (L34) |
| 3 | S046 output-colour-r14 | RELIANCE (pointer-mediated fact) | agree; hedged | "The diagnostic used for S041 did bind/query some interfaces (S046 in the U4 note)" (L87) |
| 4 | S057 terminal-trees-r23 | RELIANCE (claim inherited from S057) | agree; see note A | "entries carry `Hidden=true`, which the round-17 resolver honours (S057); not re-derived here." (L87) |
| 5 | S059 xdg-terminal-selection-r47 | RELIANCE (uses S059's bindings.conf:2 line) | agree | "`bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec ...` (~/.config/hypr/bindings.conf:2, held as row S059)" (L74) |
| 6 | S060 xdg-terminal-selection-r47 | RELIANCE at L74 (L11 is a neighbour range, not reliance) | agree | "the distro list ... (held as S060), which only excludes four entries from the fallback" (L74) |
| 7 | S073 walker-deep | RELIANCE (comparison against S073's 2.17.2 default) | agree | "upstream v2.17.2 default S073; ... §2.1-2.4 key enumerations are incomplete for 2.17.2" (L623) |
| 8 | S090 arc-synthesis | RELIANCE (line pointer `pacman.log:2929`) | agree | "On 2026-10-20 the host package moved to 2.17.2: `/var/log/pacman.log:2929` (S090)." (L392) |
| 9 | S090 closeout-r11 | RELIANCE (line pointer 2929) | agree | "the host package moved to 2.17.2: `/var/log/pacman.log:2929` (S090)." (L299) |
| 10 | S090 config-health-report-r3 | RELIANCE (pointers 2929, 3062, 3123) | agree | "the restart hooks at `/var/log/pacman.log:3062` and `:3123` (S090)" (L1010) |
| 11 | S090 remaining-planes-census | RELIANCE (pointers 2929, 3062, 3123) | agree | "logged walker-restart.hook entries (S090 lines 3062, 3123)" (L340) |
| 12 | S090 walker-deep-r9 | RELIANCE (L403 pointer 2929; L414 pointers 3062, 3123) | agree; L412 is a disclaimer but pair-level reliance holds | "the walker-restart hook ran (`/var/log/pacman.log:3062`, `:3123`, S090)" (L414) |
| 13 | S090 walker-deep | RELIANCE (pointer 2929; elephant 3095 record) | agree | "S090 (line 3095) records elephant 2.21.0-1 -> 2.22.1-1 on this host" (L624) |
| 14 | S090 walker-live-surface | RELIANCE (pointer 2929) | agree | "the host package moved to 2.17.2: `/var/log/pacman.log:2929` (S090)" (L305) |
| 15 | S090 waybar-walker-plane | RELIANCE (pointers 2929, 3062/3123 as stale-PID basis) | agree | "the walker restart hooks at `/var/log/pacman.log:3062` and `:3123` (S090) make that PID likely stale" (L481) |
| 16 | S090 waybar-walker-semantics | RELIANCE (pointers 2929, 3095, 3062/3123) | agree | "voided by the walker-restart hook runs (`/var/log/pacman.log:3062`, `:3123`, S090)" (L477) |
| 17 | S091 arc-synthesis | RELIANCE, weak (identity against row's recorded bytes) | agree; weak | "The binary sha `25240650…` is the S096/S091 file-byte value" (L402) |
| 18 | S091 walker-deep-r9 | RELIANCE (new values 806,960 and 3c5c6867 from S091) | agree | "§6's `5b4e47b7…` is `3c5c6867…` (S091)" (L415) |
| 19 | S091 walker-deep | RELIANCE (bytes 3c5c6867; offset 806,960) | agree | "the embedded default run (now at offset 806,960, byte-equal to `/etc/xdg/walker/config.toml`, S091)" (L630) |
| 20 | S091 walker-live-surface | RELIANCE (bytes 5b4e47b7 → 3c5c6867) | agree | "13,220 B `5b4e47b7…` → 13,743 B `3c5c6867…`, S091" (L314) |
| 21 | S091 waybar-walker-semantics | RELIANCE (file bytes, sha prefixes) | agree | "`/etc/xdg/walker/config.toml` 305 L / 13,743 B / `3c5c6867…`, S091" (L476) |

**Counts (first 21):** RELIANCE 21 / NAME-ONLY 0. Agree with the registry fill 21/21. Hedged (weak) reliance: 3 (#1 S015, #3 S046, #17 S091 arc-synthesis). Wave-1 labels: my label matches RevC3Contract (REAL, except #3 BORD) and CritCiteDef (U, except #1 M-U) on every pair; no wave-1 reader labelled any of the 21 MIS or N.

Note A (#4, S057): the row's teaches are "lookup order and `--dir` meaning". It says nothing about `Hidden` handling; its anchors are xdg-terminal-exec lines 106, 148-162, 402-413, 919, 1252. The entry's claim is therefore supported only if that behaviour sits in the unlisted parts of the script. I could not check this: no round-17 script pin was found in the lane, and the S057 row does not mention `Hidden`. Reliance is counted as filled; the claim's scope is unverified.

## 4. Allowlist cross-check (24 rows, `c3-name-only.tsv`)

The brief asked for any allowlisted pair I judge RELIANCE to be reported as a missing back-reference. I read all 24 citing contexts (`allowall.out`). Sha256 of `c3-name-only.tsv` = `70653e095839dc82f248d77fa5a0117134406a8b9e23778d2d79bf7072c948ee`, which matches the frozen value.

| pair | my label | note |
|---|---|---|
| S005 output-colour-r14 | NAME-ONLY (disclaims) | agree |
| S007 input-debugging-r15 | NAME-ONLY (superseded queued row) | agree |
| S030 config-era-r12 | NAME-ONLY (rejected; every occurrence mapped to S017) | agree |
| S040 output-colour-r14 | NAME-ONLY (refuted governance authority) | agree |
| S043 input-debugging-r15 | NAME-ONLY (disclaims registry scope) | agree |
| **S044 config-drift-r12 (L160)** | **RELIANCE, weak: missing back-reference** | **disagree**. The errata restates S044's registered teaches at the same lines: "The governing gate rule is gate-standing-use.md §5 rule 4 (:222-226): 'the response is re-verification and an appended erratum.' Its §5 rule 2 also requires re-cutting…". S044's anchor is "§5 rules 2 and 4, :212-226". The S044 token is only the name of the round-13 citation being corrected, but the operative rule text is S044's. |
| S045 config-era-r12 | NAME-ONLY (pointer to rejection record) | agree |
| S056 xdg-terminal-selection-r47 | NAME-ONLY (neighbour range) | agree |
| S061, S062 terminal-route-r17 | NAME-ONLY (status list) | agree |
| S084 walker-route-r18 | NAME-ONLY (rejected, replaced by S098) | agree |
| S094 theme-route-r18 | NAME-ONLY (refuted, replaced by S097) | agree |
| S096 config-health-r3 (L1017) | NAME-ONLY: "S096 … now exists and is not cited here" | agree with allowlist; disagree with CritCiteDef label `U`, which the line contradicts |
| S113 tripwire-binding-r21 (L34) | NAME-ONLY leaning; borderline | the entry retains the quoted `os` fact but says the teaches inference is refuted. Allowlist stands; hedge noted. |
| S116, S119, S120 tripwire-precision-r20 (L146) | NAME-ONLY (round-21 pointer, range) | agree |
| S132 terminal-trees-r23 (L1) | NAME-ONLY: "S132 stays queued and supports nothing." | agree |
| S187, S188, S214 event-delivery-r26 (L80) | NAME-ONLY (retired id remaps) | agree |
| S357, S358 bind-key-match-r50 (L3) | NAME-ONLY: "serve that tool only" | agree |
| S359 dispatcher-dispatch-r51 (L20) | NAME-ONLY: named only in the held enumeration; census `held_rows_cited=2 (S352, S353)` excludes it | agree with allowlist; wave-1 C1 label `REAL` is not supported by the text |

**Allowlist counts:** RELIANCE 1 (S044, weak) / NAME-ONLY 22 / borderline 1 (S113, held as NAME-ONLY). The S044 case is a candidate missing back-reference. Adding it would make `conflict=1` under the frozen rules, so it is reported, not fixed.

## 5. Counter re-derivation at 28fc86ac (independent of the lane counter)

- Independent recompute (`recompute.py`, my code): entries=71 rows=328 missing=0 extra=0 conflict=0 stale=0 allowlist_rows=24; all 8 allowlist line-shas recomputed for the scope entries and matched. `dangling` NOT independently recomputed.
- Lane counter, run by me: `python3 -I quality/counters/c3-r56-used-by.py --repo <lane> --rev 28fc86ac… --work <scratch>` printed `MADO_USED_BY: rev=28fc86ac… entries=71 rows=328 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none`, exit 0.
- Receipt check (`receipt.out`): 23 rows in `receipts/used-by-old-to-new.md`. Old and new cells match the actual old and new `used-by` for all 23. Rows whose cell changed and are absent from the receipt: none. Receipt rows with no change: none.
- Cell-only check (`cellonly.out`): between 13f0acbe and 28fc86ac, 0 non-cell-11 changes on existing rows. The 9 new rows S383-S391 are additions. `corpus/knowledge/` changes: only the new entry `hyprland-config-autoreload-r56.md` (+166, no edits to existing entries). No entry text changed.
- Range-hidden tokens (`ranges.out`, `subclaims.out`): 44 (S-id, entry) pairs where a registry-row id sits inside a range (for example `S056-S060`) and the token rule does not count it. Of those, 5 are invisible anywhere in their entry: (S057, S058 in xdg-terminal-selection-r47), (S117, S118 in tripwire-precision-r20), (S176 in hyprctl-verification-layer). Only the S057-S060 range touches the 21 scope entries. The lane registration discloses ranges as a declared limit.
- Entries with no `source:` line in their first 15 lines: 20 (`subclaims.out`). This matches the registration's disclosed "20 entries" figure.

## 6. Defects

| # | defect | input that shows it | severity |
|---|---|---|---|
| D1 | Missing back-reference for S044 (config-drift-r12 L160 errata restates the registered gate-rule teaches at the same lines). Judged reliance, currently exempt. | `corpus/knowledge/config-drift-r12.md` L160 errata; S044 row anchor "§5 rules 2 and 4, :212-226" | weakens (1 of 24 exemptions; the exemption count of 24 may be wrong by one) |
| D2 | The round-56 used-by old→new log is not in a lesson. The frozen target requires it. At 28fc86ac and at tip 9c3ca28 `corpus/lessons/` ends at round-55. The log exists only as `.ufo/waves/round-56/receipts/used-by-old-to-new.md`. | `git ls-tree 28fc86ac… corpus/lessons/` ; target sentence in `claims-frozen-v2.md` C3 | weakens (process leg, not a counter leg; the receipt is complete and correct) |
| D3 | S057 is cited for `Hidden=true` handling, which its row does not teach; the anchored lines do not mention `Hidden`. | S057 row teaches "lookup order and `--dir`"; entry L87 "(S057)" | weakens (claim supported only if the unlisted script lines hold it; unverified) |
| D4 | S359 has a wave-1 `REAL` label (C1) that the text does not support. Allowlist disposition is right; the label is wrong. | `w1/R56RevC3Contract/classification.json` S359 label vs entry L20 | cosmetic (for the report; the allowlist decision stands) |
| D5 | S096 has a wave-1 `U` label (CritCiteDef) against an explicit disclaimer "not cited here". | `corpus/knowledge/config-health-report-r3.md` L1017 | cosmetic (allowlist decision stands) |
| D6 | S046 back-reference is pointer-mediated: entry L87 says the bind/query fact is "S046 in the U4 note", not via its own source line. Judged reliance; the link is weak. | `corpus/knowledge/output-colour-boundaries-r14.md` L87 | cosmetic |

No filled pair in the first 21 is name-only. No C3 counter leg is defeated by any finding above: missing, extra, conflict, stale and lost are 0 under my recompute, and the lane counter agrees.

## 7. Counts

- Pairs derived: 50 added total, 9 new rows (S383-S391), **41 restricted**. Cross-checked against base missing minus allowlist (41).
- First 21 (sorted): **RELIANCE 21, NAME-ONLY 0**. Registry fill agreed on 21/21.
- Allowlist 24: **agree NAME-ONLY 22; RELIANCE 1 (S044, weak, D1); borderline NAME-ONLY 1 (S113)**.
- Defects: blocking 0; weakens 3 (D1, D2, D3); cosmetic 3 (D4, D5, D6).

## 8. Not verified / not run

- Not run: any `hyprctl`, host or compositor command (not needed; brief limits). No tool installs.
- Not verified: S057's `Hidden` claim (D3) — no round-17 script pin located.
- Not independently recomputed: `dangling` (the lane counter prints 0; I did not recompute it).
- Not checked: the entailment of each line against the cited source (out of scope — the fix is token-level and this seat judged reliance, not truth of the claim).
- The labels are my judgment. The wave-1 readers were consulted only after my labels were formed.
- Tooling: no tool was installed or upgraded by this seat. Python was `python3 -I`. Scratch `/fast/scratch/hyaku/mado-r56/R56W2RevUsedByA/` was removed before yield; receipts were copied to the deliverable directory first.
