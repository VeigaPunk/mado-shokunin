# C2 pin/proposition matrix audit — candidate `hyprland-synthetic-key-dispatch-r52`

Auditor: seat C2PinAudit, round 52 w1. Audited revision: `.ufo/waves/round-52/w1/C2EntryDraft/` as of 2026-10-27 ~10:07 (entry-draft.md 238 lines, proposition-map.tsv 17 rows, fetch/ 4 files + verify.txt). The seat revised the draft during the audit (see §7); both revisions were audited; findings below are against the current revision.

Method: independent re-verification from pin bytes — no reliance on the draft's own checker. Per proposition: whitespace word count, whitespace-collapsed verbatim search in the pinned file, in-anchor containment at the cited lines, full-file occurrence count; per digest: sha256 recomputation; every rationale/chain/State-claims/OBS line cite read at the cited lines.

## 1. Digest / pin identity — PASS

| pin (round-52 fetch dir) | sha256 (recomputed) | r51 SHA256SUMS identity |
|---|---|---|
| Hyprland-legacy-DispatcherTranslator.cpp | `7248cbb8…fbe771` | EQUAL |
| Hyprland-ConfigActions.cpp | `a83abeb5…1fa7637` | EQUAL |
| Hyprland-ConfigActions.hpp | `746c6f51…b7073` | EQUAL |
| Hyprland-KeybindManager.cpp | `8d8f35fc…d4e40` | EQUAL |

All four round-52 re-fetched bytes are byte-identical to the committed round-51 pins (my recomputation agrees with both `round-51/fetch/SHA256SUMS` and the seat's `fetch/verify.txt`). All URLs carry immutable commit `efb50993780079460b0cbed1363e2166a2de1d9f`. The round-52 opening required by the frozen predicate now exists as local bytes; registry admission (S370–S373 appended, opened 2026-10-27) remains the data seat's step — none of the four rows is in `corpus/SOURCES.md` yet (verified; registry ends at S369).

## 2. Proposition quotes — 17/17 PASS

All 17 TSV rows (P01–P17): quote found whitespace-collapsed verbatim inside the cited anchor, ≤25 whitespace words (max 22, P09), located in the round-52 bytes. Spot detail: P02 exact at :597; P05 at :607; P11 at :557; P13 at :1558 (2 occurrences in file — anchor disambiguates); P14 at hpp:117; P15 at :612; P16 spans :1578-1579; P17 exact at :574. The four `source:`-line quotes: S370 exact at DT:592, S371 exact at CA:1554; S372 (`int m_passPressed = -1;`) and S373 (`uint32_t CKeybindManager::stringToModMask(std::string mods)`) are collapsed-whitespace prefixes of hpp:114 / KM.cpp:221 — correct under the draft's stated comparison rule, noted because a byte-exact differ would false-negative them.

Non-uniqueness note: P16's quote `if (!window) return {};` occurs 28× in ConfigActions.cpp; the anchor does the disambiguation and is correct. Quote-string uniqueness must not be assumed by the counter or truth sampler.

## 3. Support-cite verification — every checked cite resolves to true bytes

Rationale/chain cites verified at the cited lines: DT :532-534 (sendshortcut cap+refusal), :536 (stringToModMask call), :540-543, :544-547 (272 threshold), :550 (case-insensitive keysym), :555 (no kb), :557, :559-560 (miss-guard consult) + :576 (hit path), :561-571 (scan, no break), :574, :579-580, :582-586, :588 (pass call), :592-594, :596-598, :600 (keyState=0 init), :601-604, :607, :612-617, :619-624 (restore before single exit at :626), :38-42 (wrap error mapping), :4/:66/:73 (Executor include + exec/execr spawn/spawnRaw — recon note). CA :1465-1522 (window overload branches on `m_lastCode != 0` — confirms the step-7 "last-event check" contrast), :1534 (mouse value range), :1537-1552 (focus switch inside `if (window)`), :1554, :1556-1569 (press / release / −1 press+release branches), :1576, :1578-1579, :1581-1596 (restore block after the early return), :1601-1616 (twin held ground). HPP :36, :62-64 (both `pass` overloads, `/* Active */` default), :114-117. KM.cpp :221-242 (exactly the 8 modifier-name tests listed in step 4, no rejection branch), :643 and :844-851 (shortcuts-inhibit gate — recon note). KeybindManager.hpp :149 (`m_keyToCodeCache` member — OBS cite; this hpp was **not** re-fetched in round 52, cite rests on the r51 pin). HyprCtl.cpp :1151 (`return "Invalid dispatcher";` — OBS cite). Held-ground cross-refs: `bind-table-r25.md:42` (zero-mask rejection) and S162 exist; r51 entry :197-198 quotes verbatim as the draft represents it; wiki gap (0 hits for both dispatcher names in wiki-Dispatchers.md, wiki-Binds.md, Hyprland-docs-hyprctl.1.rst) reproduced.

## 4. Findings

- **[Low] P12 proposition text (md+TSV) and P16 md text assert a delivery destination the pins do not license.** P12: "An empty third field means the focused surface"; md P16: "an empty selector delivers to the current focus". Verified: empty → nullptr (DT:583), `pass` then skips focus move and restore (CA:1537-1552, :1578-1579) — the *destination* client is explicitly out of scope in the draft's own Limits. The TSV P16 wording ("empty passes nullptr and the focus switch is skipped") is the licensed form; align P12/P16-md to it (or add a seat-delivery pin) before landing. Everything else in both propositions is verified.
- **[Info] Proposed rows collide with active registry URLs.** S370≡S365, S371≡S367, S373≡S364 (same URL, same commit); S372 (ConfigActions.hpp) is the only new URL — it was fetched in r51's pin manifest but denied a row (row cell `-`, rejected under rule 4). QUALITY.md:34 (rule 17) requires explicit repeated-URL/overlap review with human review for genuinely distinct scope; the cited *regions* (:531-627 etc.) are new relative to S365's r51 anchors (:30-35, :797-867), which is the distinct-scope argument the data seat must record. RegistryContract reached the same collision list independently.
- **[Info] P15 is held-adjacent but now correctly split.** r51's parenthetical attributed save/restore to the twin's lines (ConfigActions.cpp:1603-1615); P15 pins the translator-side save (DT:612) and rationale-cites the restore (:624), which r51 did not pin. The current draft demotes the twin to held ground and no longer maps it as a proposition — consistent.
- **[Info] OBS/State-claims hpp cite not re-fetched.** `Hyprland-KeybindManager.hpp:149` (cache member) rests on the r51 pin; harmless for an unrowed OBS, worth a pin-path qualifier when the entry lands.

## 5. Frozen-predicate fit (matrix mechanics only)

≥4 substantive propositions: 17, all substantive and mechanism-scoped. Row/pin/revision + exact located quote ≤25 words + written rationale: all 17 satisfied; rationale-cited lines all true. Mapping completeness: every material factual proposition in the chain is mapped (P01-P17); the twin is deliberately held, not unmapped; State claims and OBS carry their own cites. Count census in the draft (17/0/0) matches my independent run. What remains open is *admission*: S370-S373 are absent from SOURCES.md (correct for a draft) and the data seat must open/append them and record the URL-collision review; the C2 counter's "prove absent at base" clause must name this slug.

## 6. Explicitly not covered

Semantic entailment / source truth sampling (frozen: independent non-author reviewer; the counter cannot claim it). Counter behavior (C2CounterDraft's script). Novelty vs held corpus (C2CoverageCritic). I did not re-fetch URLs myself; identity rests on the two local digests agreeing plus the immutable commit in each URL.

## 7. Revision note (audit honesty)

The first revision I read (entry-draft 16 mapped propositions, TSV 18, pins cited to `round-51/fetch` only, census "propositions 16") had: md/TSV count divergence, two chain claims (focus-skip, key-not-found) unmapped in the md table, and no round-52 fetch. All three were fixed by the seat mid-audit (17 propositions, unified table, `fetch/` + verify.txt added). Findings surviving the revision are §4. Receipts: `pin-audit-receipt.txt` (r51-pins run, old TSV), `pin-audit-receipt-r52.txt` (current TSV vs r52 fetch), `r52-fetch-digests.txt`, `cited-lines.txt`.
