# R56ScoutAssimilation — shokuknow `merge/mado` staged vs lane-adopted, round-56 fit

Read-only scout, round 56 wave w1, 2026-10-28. Package: `/home/vgpnk/Projects/shokuknow/merge/mado/` (campaign `corpus-expansion-1`). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (frozen contract at lane commit `3423ae2…`, before this wave). Nothing was written into shokuknow and no campaign tool was run there. No tools installed. Scratch `/fast/scratch/hyaku/mado-r56/R56ScoutAssimilation/` created and removed before yield.

## 1. What the package holds (measured)

- Top level: `MERGE-REPORT.json`, `MERGE-REPORT.md`, `SOURCES.append.md`, `knowledge/`, `amendments/`.
- `knowledge/corpus/knowledge/`: **65** entry files. `amendments/corpus/knowledge/`: **4** files. Total **69** entries (MERGE-REPORT table rows counted: `table_rows=69`; round-35 lesson corroborates 65+4).
- `SOURCES.append.md`: 153 lines, **147** registry row lines (`grep -cE '^\| S[0-9]+ '` → 147; MERGE-REPORT: "proposed rows accepted: 147", first staged id S203, lane registry held 192 rows at packaging).
- **`doctrine/` does not exist** in the package. The seat brief lists it; the filesystem has no such directory (checked top level and full-tree glob). Disagreement reported; filesystem is ground truth.

### Themes staged (by MERGE-REPORT table)

| theme | entries | representative |
|---|---|---|
| IPC request/event socket + dispatchers | 9 | `ipc-contract-r25` (amend.), `dispatcher-semantics-r25` (amend.), `dispatcher-surface-and-request-grammar-r26` (amend.), `waybar-module-text-route-r25` (amend.), `hyprctl-flags-r28`, `request-socket-live-bound-r8`, `request-limits-upstream-r31`, `host-request-socket-cap-r7`, `socket-modes-and-request-read-r30`, `socket-client-contract-measurements-r29` |
| idle lock | 11 | `host-idle-lock-chain-r7`, `idle-lock-intent-mechanism-r8`, `-surface-r9`, `-surfaces-r10`, `idle-lock-journal-evidence-r11`, `idle-lock-never-asked-r12`, `idle-lock-chain-armed-r14`, `idle-lock-offered-in-the-bar-r15`, `idle-lock-runtime-state-r28`, `idle-toggle-and-daemon-lifecycle-r29`, `upstream-input-holds-and-the-lock-screen-r16` |
| focus grab / input security | 10 | `focus-grab-seat-semantics-r8` … `focus-grab-has-no-client-here-r15`, `focus-grab-protocol-live-on-host-r14`, `focus-control-surfaces-r28`, `compositor-focus-manipulation-literature-r26`, `wayland-input-security-literature-r8`, `privileged-client-surface-r29` |
| gkeep window geometry | 9 | `gkeep-geometry-unobservable-r8` … `gkeep-geometry-never-recorded-r15`, `gkeep-element-rules-r30`, `glyph-and-geometry-r31` |
| bar producers / lifecycle | 7 | `host-bar-producers-r28`, `host-producer-outputs-r29`, `host-producer-current-outputs-r30`, `weather-glyph-render-r7`, `host-bar-and-idle-binding-r26`, `uwsm-app-daemon-unit-r7`, `update-check-and-app-lifecycle-r31` |
| event-queue measurements | 2 | `event-queue-host-measurement-r28`, `event-queue-journal-measurement-r29` |
| two-literature / localized wikis | 12 | `two-literature-coverage-r25`, `two-literature-drift-r26`, `chinese-wiki-{revision-list,ipc-section,canonical-url}-r7/r28`, `zh-wiki-snapshot-semantics-r29`, `chinese-article-revision-r30`, `chinese-translation-drift-r31`, `chinese-ipc-framing-absence-r13`, `cn-framing-coverage-r8`, `window-size-read-in-chinese-r16`, `japanese-wayland-compositor-account-r16`, `japanese-input-observation-methods-r14`, `japanese-counted-comparison-gone-r15`, `chinese-hyprland-window-rules-r16` |

## 2. Already adopted by the lane — 15 of 69 entries

**By the same file name (11)** — file exists in `corpus/knowledge/`; adoption receipts in lessons:

| staged file | lane round / receipt |
|---|---|
| `ipc-contract-r25.md` (amend.) | round 32 (`MADO-R32-1`) |
| `dispatcher-semantics-r25.md` (amend.) | round 32 (`MADO-R32-2`; r32-verifier re-opened S188 verbatim, agree) |
| `waybar-module-text-route-r25.md` (amend.) | r33 "admit-on-province, not appended" → landed round 34 (S201/S202 admits; README row dates it round 34) |
| `dispatcher-surface-and-request-grammar-r26.md` (amend.) | round 39 (amendment re-grounded; r38 had deferred it) |
| `idle-lock-never-asked-r12.md` | round 35 (`MADO-R35-1`) |
| `idle-lock-chain-armed-r14.md` | round 35 (`MADO-R35-2`) |
| `idle-lock-offered-in-the-bar-r15.md` | round 35 (`MADO-R35-3`) |
| `event-delivery-limits-r26.md` | round 37 (re-grounded, five corrections) |
| `hyprctl-flags-r28.md` | round 38 (`MADO-R38-1`) |
| `request-socket-live-bound-r8.md` | round 38 (`MADO-R38-2`) |
| `request-limits-upstream-r31.md` | round 38 (`MADO-R38-3`) |

**Adopted as a successor under a different name (3 + 1 theme):**

| staged file | successor |
|---|---|
| `focus-grab-protocol-live-on-host-r14.md` | `corpus/knowledge/hyprland-focus-grab-r41.md` (r41 `ADMIT … as corpus/knowledge/hyprland-focus-grab-r41.md`) |
| `gkeep-size-to-real-size-r11.md` | `corpus/knowledge/hyprland-gkeep-geometry-r43.md` (r43 `ADMIT`) |
| `gkeep-client-size-request-r12.md` | `corpus/knowledge/hyprland-gkeep-size-request-r44.md` (r44 `ADMIT`) |
| `host-bar-producers-r28.md` | theme adopted via successor `corpus/knowledge/host-bar-producer-census-r40.md` (r40; the entry itself refused as held/superseded) |

## 3. Refused on the record — 18 entries

| staged file | round / reason |
|---|---|
| `two-literature-drift-r26.md` | r32/33/34 — documentation localization out of province; tier-C CSDN community rows |
| `chinese-article-revision-r30.md` | r35 — localization surface |
| `event-queue-host-measurement-r28.md` | r37/38 — "never overflowed" reads a null log channel (`debug:disable_logs=1`) |
| `event-queue-journal-measurement-r29.md` | r37/38 — same null channel |
| `socket-client-contract-measurements-r29.md` | r38 — 64 KiB figure is chonkstep's own cap, superseded census |
| `socket-modes-and-request-read-r30.md` | r38 — successor chain declined; facts covered by adopted entries |
| `host-bar-producers-r28.md` | r40 — refused as held; theme returns in `host-bar-producer-census-r40.md` |
| `host-producer-outputs-r29.md` | r40 — refused as written (five-vs-seven producers, inverted idle chip, volatile quote) |
| `privileged-client-surface-r29.md` | r41 — one blog source, truncated quote, no measurement |
| `focus-control-surfaces-r28.md` | r41 — §3 rests on a localized (Japanese) channel (`PROVINCE.md:75-76`) |
| `gkeep-size-rule-application-r10.md` | r43 — client-decides-size premise overturned by pinned path |
| `gkeep-geometry-unobservable-r8.md` | r43 — superseded by r9–r11 chain; refuted residuals |
| `gkeep-observation-route-r11.md` | r43 — single-source restatement |
| `gkeep-rendered-geometry-record-r13.md` | r44 — decisive journal sweep lives only in the shokuknow checkout |
| `gkeep-rendered-geometry-record-r14.md` | r44 — same absent package-path sweep |
| `gkeep-geometry-never-recorded-r15.md` | r44 — corpus-wide "never" from a sweep outside this lane |
| `gkeep-rendered-geometry-chain-r9.md` | r44 — needs two unpinned pages; round-9 receipts absent from the lane |
| `chinese-hyprland-window-rules-r16.md` | r51 — localized-channel documentation, out of province per the round-36 boundary (`PROVINCE.md:75-82`) |

Withdrawn refusal, still not adopted (1): `gkeep-element-rules-r30.md` — r43 post-data corrections withdrew the refusal (its flip fired: rules are sourced from the shipped desktop config) but adoption is a separate gate (no pinned row; entry claims three rules, quotes two); r44 restates "not adopted". No round since took it up. The r43 lesson calls it "the first candidate for the next" round — never claimed.

## 4. Unadopted with no per-entry decision — 36 entries (residue)

The lane screened the package every plane round and adopted nothing more: r45 (monitor plane: "no `merge/mado/` theme"), r46 (input devices: 42 themes screened, 0 admit / 2 refuse / 40 none), r47 (terminals: 0 admit), r48 (keysym/binds: near-misses refused by scope), r49 (bind-key-match: package does not preempt), r50 (bind/keysym + session-material: whole package rejected on scope), r51 (dispatcher-dispatch: none; localized candidate rejected), r52–r54 (no `merge/mado` adoption lines in their lessons; r52-verifier: "assimilation none"), r55 ("Assimilation: none"). The last package adoption remains round 44.

Residue by theme (files, none individually decided after the ledgers below):

- **r41 ledger "not adopted; no row cites them (residue)"** — the focus-grab r8–r15 series minus the successor: `focus-grab-seat-semantics-r8`, `focus-grab-observed-semantics-r9`, `focus-grab-focus-selection-r10`, `focus-grab-mouse-target-r11`, `focus-grab-whitelist-admission-r12`, `focus-grab-keyboard-routing-r13`, `focus-grab-has-no-client-here-r15`, plus `compositor-focus-manipulation-literature-r26`, `wayland-input-security-literature-r8`. (9)
- **idle-lock residue, never decided by name**: `host-idle-lock-chain-r7`, `idle-lock-intent-mechanism-r8`, `idle-lock-intent-surface-r9`, `idle-lock-intent-surfaces-r10`, `idle-lock-journal-evidence-r11`, `idle-lock-runtime-state-r28`, `idle-toggle-and-daemon-lifecycle-r29`, `upstream-input-holds-and-the-lock-screen-r16`. (8)
- **bar/lifecycle residue**: `weather-glyph-render-r7`, `host-bar-and-idle-binding-r26`, `host-producer-current-outputs-r30`, `glyph-and-geometry-r31` (r43/44: "not adopted; residue", glyph half belongs to the bar theme), `uwsm-app-daemon-unit-r7`, `update-check-and-app-lifecycle-r31`, `host-request-socket-cap-r7`. (7)
- **localized-channel residue (standing round-36 rule makes these out of province)**: `two-literature-coverage-r25`, `cn-framing-coverage-r8`, `chinese-wiki-revision-list-r7`, `chinese-wiki-ipc-section-r7`, `chinese-ipc-framing-absence-r13`, `chinese-wiki-canonical-url-r28`, `zh-wiki-snapshot-semantics-r29`, `chinese-translation-drift-r31`, `window-size-read-in-chinese-r16`, `japanese-wayland-compositor-account-r16`, `japanese-counted-comparison-gone-r15`, `japanese-input-observation-methods-r14` (r48 refused "a Japanese input-observation entry" by scope). (12)

Total 9+8+7+12 = 36. Ledger arithmetic: 69 = 11 (adopted by name) + 3 (successors) + 18 (refused) + 1 (withdrawn, not adopted) + 36 (residue). ✓

## 5. Does any still-unadopted entry fit round 56's surface?

Round-56 surface (registration.md §C1/§C2): the Hyprland config auto-reload entry (`hyprland-config-autoreload-r56.md`), `misc:disable_autoreload`, the inotify watch set of the config tree, config sourcing (`source =` includes, hyprlang `configStringToInt`).

**None fits.** Receipt: `grep -inE 'reload|inotify|autoreload|include|sourcing|hyprlang'` over the MERGE-REPORT table's 69 title rows → **NO_TITLE_HITS**. The package's nearest neighbors are the request/event-socket entries — all already adopted (rounds 32/37/38/39) — and they cover the IPC sockets, not the config-file watching or include-graph path. Rounds 45–55 each independently reached "no staged theme on this plane" for their surfaces; round 56's surface is likewise uncovered by the package.

## 6. PROVINCE fit of the residue (topical, not this round's surface)

PROVINCE.md (per r13/r41 citations): the Hyprland/waybar/walker configuration plane and display behavior on this host; the round-36 refinement excludes localized documentation channels. Within that:

- **In-province residues** (each would need the lane's own re-grounding gate — pinned rows, in-lane receipts — per the r37–r44 precedent): the 8 idle-lock residue entries, `host-request-socket-cap-r7`, `host-bar-and-idle-binding-r26`, `host-producer-current-outputs-r30`, `weather-glyph-render-r7`, `glyph-and-geometry-r31`, `uwsm-app-daemon-unit-r7`, `update-check-and-app-lifecycle-r31`, the 9 focus-grab/literature residue entries.
- **Out of province**: the 12 localized-channel residue entries (round-36 boundary).
- **Closest adoptable candidate by the lane's own record**: `gkeep-element-rules-r30.md` (withdrawn refusal, flip fired, adoption gate unmet: no pinned row, quote incomplete). None of the residues touches reload/auto-reload/inotify/config sourcing.

## 7. Defects and ambiguities in the input

1. **`doctrine/` named in the seat brief, absent from the package** (§1). Spec vs filesystem disagreement; filesystem wins.
2. **Package id space collides with the lane registry**: staged S203–S349 vs a registry that has grown past S351. Recorded collision counts grew as the registry did: 9 (r37) → 22 (r39) → 42 (r44) → 70 (r47) → 84 (r48) → 94 (r49). Every adoption must renumber by document, never append (r43 rule).
3. **MERGE-REPORT self-flagged inconsistency**: staged S220's `used-by` names `corpus/knowledge/idle-lock-runtime-state-r28.md`, but no proposed entry cites it — the report forces its status to `queued` ("write the entry or drop the pointer").
4. **Round-35 lesson says "refused … 66 knowledge items"** — that was r35's own predicate scope (only the three idle-lock entries' eight documents counted). Later rounds (37/38/39/40/41/43/44) adopted eight more entries; do not read r35's refusal as final.
5. **Round-48 "a focus-grab entry" scope refusal is unnamed** — the lesson does not pin which focus-grab file it meant [INFERENCE: one of the r8–r15 residue series].
6. **Amendment handling**: MERGE-REPORT's checklist says "append, do not replace" for the 4 amendments; the lane instead folded their content via re-grounded admits (r32/34/39) with no literal append of staged bytes. No live discrepancy in the held files was found by this seat (filename-level check only).

## 8. Checks not run / limits

- No byte-level diff of staged vs held entry bodies: dispositions are taken from the lane's recorded lesson ledgers, ADMIT/REFUSE lines and `corpus/README.md` index rows, not from re-reviewing entry text.
- `MERGE-REPORT.json` not parsed; counts come from `MERGE-REPORT.md`, `ls` and `grep -c`.
- Rounds 53/54 lessons contain no assimilation lines under the terms grepped (`shokuknow`, `merge/mado`, `ssimilation`); whether those rounds ran a screening seat is not recorded in what I read.
- I did not verify the internal quotes of any staged entry (not this seat's question).

## Decisive commands and outputs (trimmed)

```
S=/home/vgpnk/Projects/shokuknow/merge/mado; L=/home/vgpnk/Projects/shokunin/mado-shokunin
ls $S/knowledge/corpus/knowledge | wc -l      -> 65
ls $S/amendments/corpus/knowledge | wc -l     -> 4
test -d $S/doctrine                           -> ABSENT
comm -12 <(ls $S/amendments/corpus/knowledge|sort) <(ls $L/corpus/knowledge|sort)
  -> dispatcher-semantics-r25.md, dispatcher-surface-and-request-grammar-r26.md,
     ipc-contract-r25.md, waybar-module-text-route-r25.md
comm -12 <(ls $S/knowledge/corpus/knowledge|sort) <(ls $L/corpus/knowledge|sort)
  -> event-delivery-limits-r26.md, hyprctl-flags-r28.md, idle-lock-chain-armed-r14.md,
     idle-lock-never-asked-r12.md, idle-lock-offered-in-the-bar-r15.md,
     request-limits-upstream-r31.md, request-socket-live-bound-r8.md
comm -23 … | wc -l                            -> 58 (staged-only by name)
grep -cE '^\| S[0-9]+ ' $S/SOURCES.append.md  -> 147
grep -cE '^\| `corpus/knowledge/' $S/MERGE-REPORT.md -> 69
grep -inE 'reload|inotify|autoreload|include|sourcing|hyprlang' $S/MERGE-REPORT.md (table rows)
  -> NO_TITLE_HITS
```

Full adopted-by-name transcript: `.ufo/waves/round-56/w1/R56ScoutAssimilation/adopted-by-name.txt`.

**Bottom line:** 69 staged entries; 15 already adopted (11 by name, 3 as successors, +1 theme via `host-bar-producer-census-r40`), 18 refused, 1 withdrawn-refusal-never-adopted, 36 residue. **None fits this round's surface** (no staged entry on config reload/auto-reload, inotify, or config sourcing). In-province residues exist for future rounds (best documented: `gkeep-element-rules-r30`), but none serves C1/C2 of round 56.
