# RevRows-4 — round-46 w1 — review of draft rows S316-S325

Reviewed `.ufo/waves/round-46/l1-draft/build-pos.py` ROWS/QUOTES against `/home/vgpnk/Projects/shokunin/CORPUS.md`
(SOURCES contract v1), the C2 census (`quality/counters/c2-r46-input-device-entry.py`), the held registry rows on the
same URLs (S158, S162, S173, S182, S215, S303, S307 — read in full) and the ten fetch receipts. All line numbers below
were computed (grep -n / counter), none typed.

## Verdict

No blocker. All ten rows are CORPUS-conformant and census-legal; the built positive-control clone admits
(`PRED-C2-r46: admitted=1/1 verdict=TARGET_MET`, exit 0, scratch rev `148751b6d0d9b91400477d4bda3a25519081b800`) and
`sources-census.sh validate` exits 0 with W04 warnings only. One minor wording defect (F1), one registration-accuracy
note (F2), four info nits (F3-F6).

## Per-row checks (all ten pass)

| row | receipt (lines) | anchor ranges ⊆ receipt | quote line ∈ range | teaches verified at (opened lines) |
|---|---|---|---|---|
| S316 | Hyprland-InputManager.cpp (2315) | 1213-1295, 1350-1383, 2119-2131 | 1229 | device-first/global-second `getDeviceString(devname, "kb_layout", "input:kb_layout")` and siblings 1226-1231; unchanged-skip 1274; setKeymap call 1286; explicit-set scroll_factor clamp `0.F, 100.F` 1379-1380, nullopt 1382; getNameForNewDevice dup suffix 2119-2131 |
| S317 | Hyprland-ConfigManager.cpp (2184) | 518-565, 1115-1201 | 1119 | `addSpecialCategory("device", {"name"})` 518 + 47 `addSpecialConfigValue("device", …)` lines 519-565; set-by-user fallback 1119-1120; `if (VAL == STRVAL_EMPTY) return ""` 1163-1164; deviceConfigExists space→dash 1196-1198 |
| S318 | Hyprland-ConfigValues.cpp (734) | 271-279, 296 | 272 | `input:kb_layout` default `"us"` 272; kb_model/variant/options/rules/file default `STRVAL_EMPTY` 271-276; global `input:scroll_factor` (default 1, min 0 max 2) 296 |
| S319 | Hyprland-IKeyboard.cpp (460) | 60-145 | 113 | `m_currentRules = rules` 68; overridden early return 61-64; kb_file branch 87-96; compile-failure reset layout `"us"` + rest `""` 108-117 |
| S320 | Hyprland-HyprCtl.cpp (2346) | 748-805 | 769 | keyboards print stored rules 785-802 (layout field 800); pointers `"scrollFactor": {:.2f}` 770 rendered from `m->m_scrollFactor.value_or(-1)` 773 |
| S321 | Hyprland-MiscFunctions.cpp (844) | 777-789 | 782 | tolower default; `' '`, `'\n'`, `','` → `'-'` 779-785 |
| S322 | Hyprland-VirtualKeyboard.cpp (66) | 36-44 | 41 | keymap listener sets `m_keymapOverridden = true` 41 |
| S323 | Hyprland-protocols-VirtualKeyboard.cpp (177) | 11-30 | 12 | `name = "hl-virtual-keyboard"` 12; suffix only when `misc:name_vk_after_proc` 14-16; normalized binary name 17-27 |
| S324 | hyprlang-config.cpp (1158) | 44-66, 291-440, 669-705, 885-912 | 435 | `##` escape 691-700; bracket key 291-320; "first value must be the key" error 435; backslash continuation 53-64; special-key reset at last close 896-899 |
| S325 | wiki-Keywords.md (177) | 64-94 | 67 | override sentence 66-68; `hyprctl devices` name sentence 79 |

Cell checks: 11 cells each (build-pos asserts 12 pipes per row); kind `code`×9 + `docs`×1 (enum-valid); tier A for
every row's own scope (source code; official project wiki for S325 — `community` is never A, this is project docs);
status `mined` with used-by = the entry; opened 2026-10-26 (the L1's pin-opening date); recheck `90d` (valid cadence);
no `supersed*|replac*|obsolet*` token in any cell (T2); ids S316-S325 unused at base (lane registry: 252 rows, max
S315, malformed 0, duplicate ids 0 — CORPUS census commands run on the lane).

Quote checks (run with the counter's own `occurrences`/`quote_at`/`quote_in_code`/`norm_receipt`): each Gate quote is
3-11 words (limit 3-25), occurs exactly once word-bounded in its own receipt (whitespace-collapsed), is not inside a
comment, occurs in none of the other nine receipts, and its computed line lies inside the row's anchor ranges (1229,
1119, 272, 113, 769, 782, 41, 12, 435, 67). Every anchor range is inside its receipt's line count (max per receipt:
2131≤2315, 1201≤2184, 296≤734, 145≤460, 805≤2346, 789≤844, 44≤66, 30≤177, 912≤1158, 94≤177).

Census: recomputed from the pins = the registration line exactly — `default_layout=us` (ConfigValues.cpp:272),
`fallback_layout=us` (IKeyboard.cpp:113), `device_keys=47` (ConfigManager.cpp:519-565), `scroll_factor_max=100`
(InputManager.cpp:1380 clamp), `json_scroll_decimals=2` (HyprCtl.cpp:770), `virtual_prefix=hl-virtual-keyboard`
(protocols-VirtualKeyboard.cpp:12); each pattern exactly once. All 28 clause-j surfaces occur exactly once in their pin
and sit inside the owning row's anchor range; the built entry cites each with a ≤30-wide locator (counter run: 28 ×
`cited=1`).

## Findings

**F1 — minor, wording, fix before the data commit (S316 teaches).** "a pointer prints a scroll factor only when its
block sets one" is literally false at the dump level: the field is always printed — HyprCtl.cpp:773 renders
`m->m_scrollFactor.value_or(-1)` (also :879 in the non-JSON form), so an unset block prints `-1.00`, not nothing. The
entry's step 5 and the C1 reference docstring carry the correct -1 semantics; the registry row should too, or a tool
author reading only SOURCES.md models a missing field and mis-verdicts DIFFER. Suggested teaches: "Each kb_ name is
read from the device block first and the global input option second; a pointer's scrollFactor is its block's
scroll_factor clamped 0..100 when the block sets it, else unset and printed as -1."

**F2 — info, registration accuracy (round report, not the frozen registration).** The registration declares "The two
cross-scope URL repeats (S317 …, S320 …)". The draft creates five same-URL pairs: S317↔S162/S303, S318↔S215,
S320↔S158/S307, S321↔S182, S324↔S173. `sources-census.sh validate` on the built clone emits W04 for all five new ids
(census-validate.txt: 14 W04 = 9 pre-existing at base + 5 new). All scope cells differ → no E04. No gate impact; the
lesson/round report should say five.

**F3 — info, anchor surplus (keep the ranges, widen teaches).** Two rows carry anchor ranges that support clause-j
surfaces the entry needs but that `teaches` does not state: S316's 2119-2131 (getNameForNewDevice duplicate suffix;
entry step 7, surface dup-name) and S324's 44-66 (backslash continuation; entry step 1, surface continuation) and
885-912 (special-key reset at the last close; entry step 2, surface special-reset). The ranges are exact and inside the
receipts; either add one clause each to teaches or accept the surplus consciously.

**F4 — decision record: new row vs extending the held row's used-by.** For every repeat URL the new row is the
CORPUS-correct form:

- CORPUS SOURCES contract: "tier — scoped to `scope`, never global" — S162/S303/S158/S307/S173/S182/S215 tier-A covers
  their own scopes only; the new claims sit outside them (disjoint anchors: S317 518-565+1115-1201 vs S162
  419-451+590-623+893-968+2016-2093 and S303 788-880+1293-1387; S318 271-279+296 vs S215 629+632; S320 748-805 vs S158
  346-484+613-630+647-723+1463-1645+2003-2044 and S307 224-288+313-345; S321 777-789 vs S182 478-513; S324
  44-66+291-440+669-705+885-912 vs S173 619-667+755-827+983-986).
- Census rule text (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:25,643-649`): E04 "duplicate url within
  scope" is an error unless teaches declares `supersedes S###`; W04 "same URL across scopes" is a warning that "does
  not affect clean lanes". Distinct scope cells make the repeats legal; identical scopes would be E04.
- Append-only (CORPUS rule 2): a used-by extension in place is legal but must be logged old→new in the round lesson —
  and citing a held row for these claims would misattribute (its anchor does not contain the cited lines). The counter
  also forces the shape: clause f requires the README Sources cell to expand to exactly the cited ids, and clause d
  requires a cited held id's Gate receipt to be the round-46 pin at FETCH with the pinned sha256.
- Rule 4 ("no row quota; a short registry of opened, honestly tiered rows beats a long one") is satisfied: ten rows for
  ten opened pins, each with a distinct scope.
- Precedent: round 45 landed S303 and S307 as new rows on URLs already held by S162/S158 — the same form.

**F5 — info, Gate shape vs CORPUS rule 1's letter.** The GATE lines bind receipt path + sha256 + quote (the counter's
GATE_RE is an exact shape; adding `url=`/`opened=` tokens would break clause d). The URL and access date live one hop
away: the row's source and opened cells, and the entry's per-id OBS lines ("pin opened 2026-10-26"). Consistent with
the frozen round-45 v2 predicate; noted so a future auditor does not read the Gate alone as rule-1-noncompliant.

**F6 — info, entry step 2 count locator (entry-side; rows unaffected).** The entry's "47 values" cites
Hyprland-ConfigManager.cpp:518-540, which shows 22 of the 47 `addSpecialConfigValue("device", …)` lines (519-565). The
count's grounding is the census line (clause h recomputes 47 from the pin); T1 forbids repeating `device_keys=…` in
prose, so the census line is the only token form available. A second locator (519-565) on that step-2 line would ground
the count without tripping T1.

## Evidence files (this seat dir)

- `c2-pos-run.txt` — counter run on the built scratch clone (clauses a-j all 1, admitted=1/1 TARGET_MET, 28 surfaces
  cited=1, all ten clause=d bound=1).
- `census-validate.txt` — `sources-census.sh validate` on the same clone (exit 0; 14 W04, no E04).
- Scratch `/fast/scratch/hyaku/mado-r46/RevRows` (clone at freeze 8c5434c + build-pos + commit) deleted after copying;
  the lane was never written.

## Residual risk / gaps

- C1 (tool/fixtures) not reviewed here — outside this seat's target.
- The census/counter ran on a scratch clone at the freeze, not on the lane (no data commit exists yet).
- Clause j's keyword matching was verified through the counter run (28 × cited=1) rather than by hand for all 28
  surfaces.
- Quote uniqueness was computed on whitespace-collapsed text with the counter's word-boundary logic; the comment-strip
  variant (`quote_in_code`) was verified for all ten.
