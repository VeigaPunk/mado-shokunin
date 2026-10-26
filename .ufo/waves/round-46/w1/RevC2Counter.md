# Seat RevC2Counter — C2 counter re-cut review (round 46 w1)

Reviewed `quality/counters/c2-r46-input-device-entry.py` (sha256
`18ea82b1c4372b0c8e7af585d0edf09ffbf6d4a0d276ce19fc97519b720b72b7`, byte-identical to its blob at the freeze
`8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, checked via `git show <freeze>:<path> | sha256sum`) against its parent
`quality/counters/c2-r45-monitor-entry-v2.py`. All runs used the frozen counter file, `python3 -I`, on scratch
clones under `/fast/scratch/hyaku/mado-r46/RevC2Counter` (deleted at the end; run outputs preserved in
`artifacts/` next to this report). No tool installs were needed (python3/git/curl only).

## Verdict

The re-cut is faithful: the diff is exactly the seven re-cut regions the docstring claims (docstring, constants,
PINS/PINS_URL, host_census, SURFACES, one comment, T4 verdict tokens); every other clause is byte-identical to
r45. Constants, pins, census and surfaces all check out, the census is provably derived from the pins and fails
closed under every pin-format mutation I tried, and the counter rejects four of my five single-point breakages
with exactly the predicted clause flips. **One real finding: the T4 verdict-token list omits `OK`**, one of the
five registered top verdicts, and I demonstrated a forged entry line claiming `verdict OK` against a receipt that
never says OK being **admitted** (exit 0). One token fixes it; the file is frozen, so this goes to the L1 as a
re-registration candidate.

## 1. Diff shape (artifacts/c2-r45-to-r46.diff, 301 lines, 7 hunks)

Hunks: docstring (@@ -1,22), constants PRED/BASE_DEFAULT/ENTRIES/LESSON/FETCH (@@ -87,11), PINS + HY/PINS_URL
(@@ -106,37), CENSUS_KEYS + host_census body (@@ -333,70), SURFACES (@@ -167 region), clause-i comment
(@@ -674,7), T4 token tuple (@@ -688,8). Everything else — clauses a-g, f, T1-T3, helpers, main — byte-identical.

## 2. Changed constants — all correct

| constant | r46 value | check |
|---|---|---|
| PRED | `PRED-C2-r46` | matches registration §C2 heading |
| BASE_DEFAULT | `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe` | registration.md:2 |
| ENTRIES | `corpus/knowledge/hyprland-input-devices-r46.md` | registration.md:41 |
| LESSON | `corpus/lessons/round-46.md` | registration.md:41 |
| FETCH | `.ufo/waves/round-46/fetch/` | matches fetch/ contents |
| OPENED | `2026-10-26` (unchanged) | round 46 opened the same date |
| HY url rev | `efb50993780079460b0cbed1363e2166a2de1d9f` | registration.md:3 (0.56.2) |
| hyprlang / wiki | `v0.6.8` / `ecc06f3b...` | registration.md:3; task brief |
| JWIDTH | 30 (unchanged) | registration.md:46 "locator width <= 30" |

Unchanged and correct: MIN_RECEIPT 256, ROW_RE, GATE_RE, RECHECK_RE, SRC_RE, BAD_LOC, ENV (GIT_* stripped),
Setup/exit-2 semantics. No stale `_HY` reference survives the rename to `HY` (a stale one would NameError; the
positive run proves none).

## 3. Pins — triple-verified

10 pins = exactly the 10 files in `.ufo/waves/round-46/fetch/`. (1) lane fetch/ files hash == PINS dict, 10/10;
(2) `receipts/fetch-sha256.txt` == PINS, 10/10; (3) live `curl` of all 10 PINS_URLs today returned bytes whose
sha256 == PINS, 10/10 — so the trust root is real upstream content, and the FALSE-URL/FORGED-PIN classes bind to
something that exists. The positive run additionally binds all 10 pins inside the freeze clone (clause d sha
checks + clause i `set(PINS) <= used`).

## 4. host_census (counter lines 329-353)

Each of the six extractions matches **exactly once** in the pinned bytes: default_layout `us`
(ConfigValues.cpp), fallback_layout `us` (IKeyboard.cpp), device_keys 47 (ConfigManager.cpp — 47 matching lines
AND 47 substring occurrences, so no same-line double-count), scroll_factor_max `100` (InputManager.cpp),
json_scroll_decimals `2` (HyprCtl.cpp, single-digit class), virtual_prefix `hl-virtual-keyboard`
(protocols/VirtualKeyboard.cpp). The recomputed want line equals the registration census line verbatim
(registration.md:45-46).

**Pin-format sensitivity (the asked question):** I called `host_census` directly on mutated pin bytes. Five
mutations — a second `m_currentRules.layout = "us";` assignment, HyprCtl decimals 2→3, ConfigValues default
us→de, one `addSpecialConfigValue("device",` line dropped, clamp 100.F→200.F — each either abort to `(False, [])`
or recompute `want` (de / 3 / 46 / 200) and then fail the entry's census line. Every direction is fail-closed
(TARGET_MISSED); none can produce a wrong admission. A changed pin also cannot bind as a gate at all (clause d
sha), so the census sits behind a double lock. The census is genuinely **derived, not hardcoded** — demonstrated
by the recomputed `want` values above.

Brittleness notes (safe direction only): device_keys is a line-count heuristic — an upstream reformat that
merges/splits those 47 lines changes the count → TARGET_MISSED, never a silent wrong pass; the decimals regex
`[0-9]` is single-digit — decimals ≥ 10 → fail-closed. Cosmetic: parameters `new_ids`/`reg_rev` are unused
(inherited identically from r45).

## 5. SURFACES — 28 items (counter line 355)

- All 28 anchors occur **exactly once** in their pinned receipt: independent count over the lane pins found zero
  non-unique anchors; the positive run corroborates (28× `cited=1`, never `anchor_count`).
- All surface receipt names are members of PINS (no surface reads an unverified file).
- Docstring ↔ code: 7 InputManager + 4 ConfigManager + 2 ConfigValues + 3 IKeyboard + 2 HyprCtl + 1
  devices/VirtualKeyboard + 1 protocols/VirtualKeyboard + 1 MiscFunctions + 5 hyprlang + 2 wiki = 28, and the
  docstring's per-file grouping matches the tuples one for one.
- Anchor lines are coherent with the gate quotes: kb-layout-lookup 1229 == S316's quote line, set-by-user 1119 ==
  S317, kb-layout-default 272 == S318, fallback-us 113 == S319, json-scroll 770 adjacent to S320's quote at 769,
  virtual-name 12 == S323, first-value-key 435 == S324.
- Keyword sensibility: most are tight (`kb_layout`, `input:scroll_factor`, `kb_file`, `hl-virtual-keyboard`,
  `scrollFactor`, `bracket`, `first value|first key`, `backslash|continuation`, `hyprctl devices`). Broad ones —
  `lower|name`, `default`, `EMPTY` (case-insensitive), `close|reset|forgotten`, `fall`, `layout`, `virtual`,
  `exists`, `global`, `wiki|document` — bind a locator plus any of those words, so an adjacent unrelated sentence
  can satisfy a surface. This is the **declared** residual (registration.md:57 "clause j binds a locator and a
  keyword per surface, not the truth of the sentence") and the same style as r45; noted, not a regression.

## 6. Verdict-token list (counter lines 52-53 docstring, 675-676 code)

The nine tokens AGREE, DIFFER, FALLBACK, VIRTUAL, MATCHED, NO_SUCH_DEVICE, STALE_BLOCK, NO_KEYBOARDS,
NOT_COMPARED are all in the C1 contract vocabulary (keyboard VIRTUAL/AGREE/FALLBACK/DIFFER; mouse AGREE/DIFFER;
block MATCHED/NO_SUCH_DEVICE; top NOT_COMPARED/DIFFER/NO_KEYBOARDS/STALE_BLOCK/OK — reference docstring,
l1-draft/mado-devices.py:89); no spurious tokens. Word-boundary behaviour is correct (\bDIFFER\b does not match
DIFFERENT; \bMATCHED\b does not match UNMATCHED; the search is case-sensitive so `hl-virtual-keyboard` does not
trip \bVIRTUAL\b).

**FINDING F1 (medium): `OK` is missing from the token list.** `OK` is a registered top verdict
(registration.md:17 "`verdict=OK`"; reference docstring line 89 "STALE_BLOCK (exit 4, stale > 0) | OK (exit 0)").
Demonstrated exploit (brk5): appended one unfenced entry line
`Top verdict OK per the manifest (.ufo/waves/round-46/receipts/fetch-sha256.txt:1).` — the manifest contains no
word-bounded `OK` (grep -cw OK = 0) — and the frozen counter printed `admitted=1/1 verdict=TARGET_MET`, exit 0
(clone rev `c11a2c83cc5279d9186ea7528aea543830b6b9de`, artifacts/brk5.out). Scoring the identical tree with a
scratch copy of the counter carrying only `"OK"` appended to the tuple (artifacts/../r46ok.py patch, not in the
lane) gives `clause=i verdict tokens ['OK'] not in .ufo/waves/round-46/receipts/fetch-sha256.txt`, i:0,
admitted=0, exit 1 (artifacts/brk5ok.out). So the declared RECEIPT-CONTRADICT rejection has a one-token blind
spot. The r45 parent omits its equivalent too (inherited shape), but the re-cut re-authored the list and could
have closed it. Fix is one token in the tuple plus the docstring list; the file is FROZEN, so this is a
re-registration decision for the L1 (kill rule, registration.md:52), not something I changed in the lane.

**F2 (low, inherited unchanged): T4 only fires on `receipts/` citations.** The locs regex matches
`\.ufo/waves/round-\d+/receipts/...` only, so a verdict token beside a `fetch/` citation is never token-checked
(`if not toks or not locs: continue`). Byte-identical in r45 — not a re-cut regression. Mitigation in practice:
run verdicts belong in receipts/ files and the pins are separately gate-bound; residual only.

## 7. r45 leftovers

None. Substring scan of the whole file for monitor/Monitor/refresh/UNRULED/DISABLED/NO_MATCHING/NO_RULES/_HY/
hyprutils/aquamarine/MonitorRule/round-45/scale_search/Parser hits only: line 4 "round-45" and line 5 "monitor"
(both inside the intentional provenance sentence naming the parent counter file) and line 695 "Parser" (substring
of `argparse.ArgumentParser`). No r45 pin names, surfaces, census keys or verdict tokens survive.

## 8. Runs (frozen counter, scratch clones; outputs in artifacts/)

| run | tree | result |
|---|---|---|
| NEG (entry absent at freeze rev) | 8c5434c | all clauses 0, admitted=0/1 TARGET_MISSED, exit 1, no crash (neg.out) |
| POS (build-pos.py recipe) | 73c92146 | a..j all 1, admitted=1/1 TARGET_MET, exit 0; S316-S325 all new+mined+used; 10/10 gates bound; 28/28 surfaces cited (pos.out) |
| brk1: census `default_layout=us`→`de` (entry line 53) | 3082490e | h:0 only → rejected exit 1 |
| brk2: surface locator 1213-1238→1313-1338 (entry line 32) | 6ad0f057 | j:0 only (`surface=apply-keyboard cited=0`) → rejected exit 1 |
| brk3: `NO_KEYBOARDS` token citing a receipt without it | 3c4f3a40 | i:0 only, diagnostic printed → rejected exit 1 |
| brk4: gate S316 sha last hex digit 5→6 (lesson line 5) | e5d37af1 | d:0 e:0 g:0 h:0 i:0 (unbound gate removes InputManager from the census inputs and breaks pin coverage) → rejected exit 1 |
| brk5: `OK` token citing a receipt without it | c11a2c83 | **ADMITTED exit 0 with the frozen counter** (F1); rejected i:0 with the one-token patch (brk5ok.out) |

brk1/brk2/brk3 are the three requested single-clause breakages (h, j, i — one clause flips each); brk4/brk5 are
extra single-point mutations. Frozen `receipts/ctl-c2.txt` (VERDICT: PASS, wrong=0 of 15) is consistent with all
of the above, including RECEIPT-CONTRADICT i:0 at its line 15.

## 9. Residual risk and verification gaps

- I did not re-execute the 14 frozen controls; I ran NEG, POS, five own breakages and six direct host_census
  mutations. ctl-c2.txt is corroborating evidence, not re-executed by me.
- The F1 exploit is a minimal one-line mutation of the positive control, which is the right minimal
  demonstration; no from-scratch forged entry was built.
- Pin URLs were verified against live upstream today (2026-10-26); later drift is covered by the entry's
  `recheck: on-release` clause and fails closed.
- Keyword breadth and claim-to-quote binding remain the declared residuals (registration.md:56-57); this review
  confirms they are declared, not newly introduced.

## Findings summary

- **F1 (medium):** T4 verdict-token list omits `OK` — a contradicted `verdict OK` entry line is admitted
  (demonstrated, exit 0). Fix: add `"OK"` to the tuple at quality/counters/c2-r46-input-device-entry.py:675-676
  and to the docstring list at :52-53; requires re-registration since the file is frozen.
- **F2 (low, inherited):** T4 token check only covers `receipts/` citations, not `fetch/` citations.
- **F3 (info, inherited):** `host_census` parameters `new_ids`/`reg_rev` unused.
- **F4 (info, declared):** broad surface keywords (listed in §5) — already a declared residual.
- **F5 (info):** device_keys line-count heuristic and single-digit decimals regex are brittle but strictly
  fail-closed under upstream reformat.

Everything else about the re-cut checks out; the shared machinery is byte-identical to the round-45 v2 counter.
