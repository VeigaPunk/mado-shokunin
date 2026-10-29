# R56W2RevUsedByB — reliance review of the C3 registry fix (used-by back-references)

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, all trees read at `28fc86ac2359ec27406d8a2c63bef82ea6e947ed`
(never the working tree). Attack targets: the fix's 41 used-by fills and the frozen 24-row name-only allowlist
(`.ufo/waves/round-56/c3-name-only.tsv`, sha256 `70653e09…`, embedded in `frozen-tables-v2.json` `c3.allowlist_sha256`).

## 0. Scope and method

Per the seat: (i) the **last 20 FILLED pairs** (sorted by S-id then entry path) of the 41 pairs the fix added,
and (ii) **all 24 allowlisted pairs** — line by line, deciding RELIANCE (the entry uses the row's content, line
pointer, receipt or bytes as evidence) vs NAME-ONLY (the id is mentioned to refute / supersede / redirect /
disclaim / name another object), then agree/disagree with the registry decision.

Independent recomputation (scratch `c3pairs.py`, `c3filled.py` — commands below) reproduced the counter's
baseline arithmetic exactly, so every judgement below rests on my own pair derivation, not the lane's:

```
python3 -I c3filled.py        # base rev 13f0acbe: entries=70 rows=319 pairs=381; rev: entries=71 rows=328 pairs=390
# base missing (all)      = 65   (= 41 + 24, matching registration-v2 baseline missing=41/exempt=24)
# base missing (non-allowlist) = 41  → the fix's filled set
# rev  missing (all)      = 24   (= the 24 allowlisted rows) ; rev missing (non-allowlist) = 0
```

The receipt `receipts/used-by-old-to-new.md` was checked against the **actual** base→rev used-by diff: 23 rows
changed, 41 paths added, **0 mismatches**, no missing/extra diff rows. Only cell 11 changed (0 other-cell edits
across all 319+9 rows); 9 new rows S383–S391 added (the C1 rows, each with used-by naming the new entry, which the
new entry's CITE covers exactly: S383–S391). Comma separators everywhere (E13 satisfied); no space-joined parts.

Counter reproduced at rev (exit 0):
`MADO_USED_BY: rev=28fc86ac… entries=71 rows=328 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none`
Harness reproduced (exit 0): `MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK`.

## 1. Per-pair labels — the last 20 FILLED pairs (all 20: my label = RELIANCE → AGREE)

| # | pair | citing line (≤25 words) | verdict |
|---|------|--------------------------|---------|
| 1 | S096 / arc-synthesis.md | "The binary sha `25240650…` is the S096/S091 file-byte value (S096 recorded at `df84807`…)" | RELIANCE — restates S096's anchor digest as the value. AGREE |
| 2 | S096 / closeout-r11.md | "…so 'not re-measured this round' above is wrong; … Host walker bytes: S096." | RELIANCE (thin: pointer-to-record, no digest restated). AGREE |
| 3 | S096 / waybar-walker-semantics.md | "…so 'not re-checked'/'not re-hashed this round' above is wrong …; the binary bytes are S096." | RELIANCE (thin: same pointer form). AGREE |
| 4 | S158 / hyprctl-flags-r28.md | "reply is built in the host's handler, S158 `:2107`/`:2126`"; "**OBS** S158: the server strips a leading flag segment…" | RELIANCE (line pointers + OBS). AGREE |
| 5 | S158 / hyprctl-verification-layer.md | "…builds the `hyprctl animations -j` table from the directives (S175–S177, S158, S162)" | RELIANCE (provenance attribution; weakest form — see finding F2). AGREE |
| 6 | S158 / request-limits-upstream-r31.md | "(S158 `:2270-2280`, …)"; "**INF** S253, S158: a client can therefore send a request larger than 64 KiB…" | RELIANCE (line pointer + INF attribution). AGREE |
| 7 | S162 / hyprctl-verification-layer.md | same L306 sentence | RELIANCE (attribution; weakest form). AGREE |
| 8 | S175 / hyprctl-verification-layer.md | same L306 sentence ("S175–S177" range member) | RELIANCE (attribution). AGREE |
| 9 | S177 / hyprctl-verification-layer.md | same | RELIANCE (attribution). AGREE |
| 10 | S186 / hyprctl-flags-r28.md | "(`knowledge/ipc-contract-r25.md` §1 line 42, S186 `:19`)" | RELIANCE (line pointer, :19 inside S186's anchor). AGREE |
| 11 | S187 / hyprctl-flags-r28.md | "**INF** S221, S187: this is the documented counterpart of the request socket's synchronous evaluation…" | RELIANCE (documentation attribution). AGREE |
| 12 | S201 / event-queue-observability-r37.md | "**INF** S201: Waybar never reconnects (`backend.cpp:105,119-122`)" | RELIANCE (file+line evidence attributed to the row). AGREE |
| 13 | S277 / request-limits-upstream-r31.md | "S277 `:61` (\"Requests are capped at 64 KiB\") is byte-identical to the draft's cited S243" | RELIANCE (quoted content + line pointer). AGREE |
| 14 | S318 / hyprland-bind-key-match-r50.md | "held (cited, not re-registered): S318 - … the `input:resolve_binds_by_sym` row and its `false` default" | RELIANCE — verified: resolve_binds_by_sym is at ConfigValues.cpp:278 with default `false`, inside S318's anchor :271-279. AGREE |
| 15 | S318 / xkb-keymap-compile-r48.md | "Hyprland starts from `us` when no layout is configured (S318, `input:kb_layout` default)" | RELIANCE (S318's recorded default is the evidence). AGREE |
| 16 | S319 / hyprland-bind-key-match-r50.md | "**OBS** S319: `xkb_state_update_mask(m_xkbSymState, 0, 0, 0, 0, 0, group);`(Hyprland-IKeyboard.cpp:382)" | RELIANCE (OBS quote from the row's pinned file). AGREE |
| 17 | S319 / xkb-keymap-compile-r48.md | "sourced (held row S319, its context line)"; "…(S319, the `m_currentRules` reset after a failed …)" | RELIANCE (S319's fallback behaviour). AGREE |
| 18 | S350 / hyprland-bind-key-match-r50.md | "The host runs one layout (`kb_layout = br` …, the round-48 S350 receipt)" | RELIANCE (receipt used as evidence). AGREE |
| 19 | S352 / hyprland-dispatcher-dispatch-r51.md | "held (cited, not re-registered, registry rows only): S352 through S353, the same two Hyprland files this entry reads past their round-50 regions" | RELIANCE (borderline — see F3). AGREE |
| 20 | S353 / hyprland-dispatcher-dispatch-r51.md | same L20 sentence; L278 "held_rows_cited=2 (S352, S353)" | RELIANCE (borderline). AGREE |

**Count: 20/20 AGREE (reliance). 0 false reliance records in scope.**

Thin cases flagged (not disagreements): #2/#3 consume no S096 content — they point at the row as the record of the
walker bytes, in contrast to the allowlisted twin S096/config-health-report-r3.md L1017 which *disclaims* ("is not
cited here") — the fix's discriminator (disclaimer ⇒ name-only; pointer ⇒ reliance) is applied consistently.
#5/#7/#8/#9 consume no content either: they attribute the directive sources in an errata that delegates the
derivation to animation-table-r26.md (wave-1 reader 2 hedged all four M-U; registration-v2 discloses "six carry an
M-U or BORD hedge" — verified: exactly 6 hedged pairs among the 41).
#19/#20: the entry reads those two files past the round-50 regions and asserts byte-identity with the round-50
pins, whose path+digest are recorded in S352's/S353's anchor cells; the entry's own L48 digest manifest lists the
identical digests (`8d8f35fc…` / `9db68cf4…`). Borderline but evidence-backed.

## 2. Per-pair labels — the 24 ALLOWLISTED pairs (23 AGREE name-only; 1 borderline disagreement)

| pair | citing line (≤25 words) | verdict |
|------|--------------------------|---------|
| S005 / output-colour-boundaries-r14 | "Neither the S005 README's earlier commit nor the later S040 governance commit is substituted…" | NAME-ONLY (disclaims; entry's source is S048). AGREE |
| S007 / input-debugging-boundaries-r15 | "S051 supersedes queued S007's loose composite tools description and mutable anchor." | NAME-ONLY (supersession; S007 queued, used-by '—'; S051 carries the entry). AGREE |
| S030 / hyprland-config-era-r12 | "…read every S030 citation in this entry … as **S017**"; S017.used-by ⊇ this entry | NAME-ONLY (rejected row, redirected; reliance recorded on S017). AGREE |
| S040 / output-colour-boundaries-r14 | "do not apply S040's wayland-protocols governance as its authority"; "**S040 governance makes … stable.** Reject:" | NAME-ONLY (refutes/disclaims; S047/S048 carry it). AGREE |
| S043 / input-debugging-boundaries-r15 | "S052 adds the core input contract, distinct from S043's registry scope." | NAME-ONLY (contrast; S052 carries it). AGREE |
| S044 / config-drift-r12 | "S015 stays a historical omarchy-method source; round-13 S044 cites the actual gate-maintenance rule." | **BORDERLINE — leaning RELIANCE** (see F1). Disagree-leaning |
| S045 / hyprland-config-era-r12 | "The duplicate rejection is now explicitly recorded by superseding registry row S045…" | NAME-ONLY (rejected row; S017 carries the entry). AGREE |
| S056 / xdg-terminal-selection-r47 | "held neighbours: the documentary route in terminal-route-r17.md (rows S056-S060)" | NAME-ONLY (neighbour pointer; terminal-route-r17 is S056's used-by). AGREE |
| S061 / terminal-route-r17 | "Source rows: `corpus/SOURCES.md` S056-S060 (mined) and S061-S062 (rejected)" | NAME-ONLY (rejected rows, used-by '—'). AGREE |
| S062 / terminal-route-r17 | same line | NAME-ONLY. AGREE |
| S084 / walker-route-r18 | "Head `source:` token S084 … was replaced in place by S098 …; S084 is now `rejected`" | NAME-ONLY (rejected; S098 carries it). AGREE |
| S094 / theme-route-r18 | "Head `source:` token S094 was replaced in place by S097 …; S094 is now `rejected`" | NAME-ONLY (rejected; S097 carries it). AGREE |
| S096 / config-health-report-r3 | "S096 (host walker bytes) now exists and is not cited here." | NAME-ONLY (explicit disclaimer — the clean counterpart to fills #2/#3). AGREE |
| S113 / tripwire-binding-boundaries-r21 | "Source correction S119 explicitly supersedes the universal inference in S113's `teaches` field…" | NAME-ONLY (supersession; entry's sources are S116-S120; S113's used-by = tripwire-precision-r20 which does use it). AGREE, borderline noted by the reason itself |
| S116 / tripwire-precision-r20 | "Current bounded reasoning … are in `tripwire-binding-boundaries-r21.md` (S116–S120)" | NAME-ONLY (pointer to the r21 entry; S116's used-by ⊇ r21 entry). AGREE |
| S119 / tripwire-precision-r20 | "S119 explicitly supersedes S113's finite-module-list inference." | NAME-ONLY (correction row; S119's used-by ⊇ r21 entry). AGREE |
| S120 / tripwire-precision-r20 | "(S116–S120)" | NAME-ONLY. AGREE |
| S132 / terminal-trees-r23 | source line: "…S132 stays queued and supports nothing." | NAME-ONLY (explicit disclaimer; S132 queued, used-by '—'). AGREE |
| S187 / event-delivery-limits-r26 | "the source ids (package S187 → S189, S188 → S201, S214 → S212, by document)" | NAME-ONLY (renumbering; S189/S201/S212 used-by ⊇ this entry — verified all three). AGREE |
| S188 / event-delivery-limits-r26 | same | NAME-ONLY. AGREE |
| S214 / event-delivery-limits-r26 | same | NAME-ONLY. AGREE |
| S357 / hyprland-bind-key-match-r50 | "S355/S356 are shared with `tools/mado-keysym.py`, S357/S358 serve that tool only." | NAME-ONLY (explicit scope disclaimer; S357/S358 used-by = lessons/round-50.md). AGREE |
| S358 / hyprland-bind-key-match-r50 | same | NAME-ONLY. AGREE |
| S359 / hyprland-dispatcher-dispatch-r51 | "held (cited, not re-registered, registry rows only): … S359, the wiki Binds page at the 0.56.2-era revision" | NAME-ONLY (the entry never reads the Binds page — not in its pin manifest; S359's used-by = the r50 entry that does). AGREE |

**Count: 23/24 AGREE (name-only). 1 borderline leaning reliance (S044) — see F1.**

## 3. Findings

### F1 (weakens the claim) — the S044 exemption likely masks a genuine missing back-reference

`config-drift-r12.md` L156-158: *"The governing gate rule is `gate-standing-use.md` §5 rule 4 (:222-226): 'the
response is re-verification and an appended erratum.' Its §5 rule 2 also requires re-cutting after changes outside
the excised blocks."* — quoted content that is **exactly row S044's registered scope**: S044 = "Gate maintenance
rules — corpus/knowledge/gate-standing-use.md", anchor *"§5 rules 2 and 4, :212-226"*, teaches *"Gate pin movement
requires re-verification and an appended erratum; edits outside excised blocks require a measured regression
re-cut"*. The cited lines :222-226 sit inside S044's anchor; the quoted sentence is S044's teaches verbatim. S044 is
the **only** registry row registering gate-standing-use.md (verified by scan). The entry applies that rule as the
governing authority of its own erratum, and its L160 token says *"round-13 S044 cites the actual gate-maintenance
rule"* — pointing at the row that carries the rule it is relying on. Yet S044's used-by names only
`corpus/lessons/round-13.md`, and the round-13 lesson's M3 action item was *"Append the actual gate-rule citation in
`config-drift-r12.md`, record S044"* (round-13.md L12) — i.e. the intended back-reference WAS S044↔config-drift-r12.md.

Counter-argument (stated for the panel): the token's surface role is a pointer to round-13's citation; the reliance
is expressed by file path, which the token-level CITE rule cannot see; and the entry's `source:` line never listed
S044, so under the lane's own source-line convention the row was never this entry's declared source. Wave-1 split on
exactly this pair (Contract MIS / Crit M-U "names owed source"), and registration-v2's pre-registered allowlist rule
("at least one reader judged name-only") makes the exemption procedurally sound. Severity: **weakens the claim** —
the exemption suppresses the only token-level back-reference for a pair whose entry consumes S044's registered
scope; it would become **blocking** for TARGET_MET if the closure sided with reliance (S044's used-by lacks
config-drift-r12.md ⇒ missing=1).

### F2 (weakens) — the four L306 fills are attribution-only, and the same-sentence range hides a real gap

`hyprctl-verification-layer.md` L306's parenthetical "(S175–S177, S158, S162)" names the directive sources behind
*another entry's* explanation (animation-table-r26.md, which already carries S158/S162/S175/S177 in its used-by at
base). The four fills rest on provenance attribution alone — no content, line pointer, receipt or bytes of those
rows are consumed; wave-1 reader 2 hedged all four M-U. Accepted as reliance (the sentence asserts which rows the
directives come from), but flagged: **if this parenthetical counts as reliance, then S176 — hidden inside the same
range "S175–S177" — has a missing back-reference** (S176 = "Hyprland v0.56.2 animation tree", used-by =
animation-table-r26.md only; the token rule cannot see it). Verified: exactly 5 range-hidden pairs exist
(S057, S058 × xdg-terminal-selection-r47; S117, S118 × tripwire-precision-r20; S176 × hyprctl-verification-layer),
matching registration-v2's "five pairs" disclosure; the other four are name-only pointer contexts, so S176 is the
one with substance.

### F3 (weakens reviewability; cosmetic for the counter) — allowlist reason quotes are not located substrings

The seat asked: each allowlist reason quote must be a located substring of the cited line. **16 quote instances
across 15 of 24 rows fail.** Causes: markdown emphasis (`**…**` in S113 r14, S040 r04, S094 r12), backtick-stripped
paraphrase (S061 r09, S084 r11), "..." ellipsis (S030 r03 first quote, S084 r11, S359 r24), "→" written as "->"
(S187/S188/S214 r19-r21), en-dash written as hyphen "(S116-S120)" vs file "(S116–S120)" (S116/S120 r15/r17), a quote
wrapping two lines (S044 r06: the phrase spans L160-161), and one plain mis-location: S040's 'not substituted' is
cited to L65 but literally occurs at L81 (L65 says "nor the later S040 governance commit is substituted…"). Two rows
carry no quoted span at all (S062 r10 "same list"; S359 r24 gives no line reference either). The S030 reason field
is additionally **truncated mid-sentence** ("… 'the original S030 stays rejected'. Source header and"). The counter
ignores the reason column (parse_allow reads cells 0-2 only), so TARGET_MET is unaffected; but the reason column is
the only human audit trail for the 24 exemptions, and it cannot be mechanically re-verified. The line-sha column is
unaffected: **all 24 line-sha values reproduce byte-exactly** against my independent recomputation (null result,
command in §5).

### F4 (residual risk, pre-existing entry defect — not introduced by the fix) — dispatcher L53 self-contradiction

`hyprland-dispatcher-dispatch-r51.md` L53: *"… so rows S352/S353 stay theirs; this entry opens no row for either
file."* — contradicted by the same entry's L14/L18 (`source: S364`/`S368`, both for exactly those two files) and pin
manifest L32/L39 (both files → S364/S368), rows opened 2026-10-27 with used-by = this entry. The C3 fix then added
this entry to S352's and S353's used-by on the strength of the L20/L53/L278 bookkeeping, whose "opens no row"
sentence is false. The fill remains defensible (the entry does read those files' bytes and L52's byte-identity claim
is checked against the digests S352/S353 register), but the registry now records a reliance whose supporting
sentence is self-contradictory, while the third member of the same L20 clause (S359) was exempted on "no content use
found". Pre-existing at base rev `13f0acbe` (verified identical). Severity: weakens (not a C3 predicate break).

### F5 (residual risks — declared scope limits, verified)

1. **Range-blind tokens**: 5 hidden pairs, exactly matching registration-v2's "five pairs" disclosure (verified:
   S057, S058 × xdg-terminal-selection-r47 L11; S117, S118 × tripwire-precision-r20 L146; S176 ×
   hyprctl-verification-layer L306). Four are name-only pointer contexts; S176 is the substantive one (see F2).
2. **Non-knowledge files outside the axis**: ENTRIES = corpus/knowledge/*.md only. 1,149 (row, lesson-file)
   citation pairs exist across corpus/lessons/*.md; **1,129 are not recorded in any used-by cell** (296 distinct
   rows), and the counter cannot see them by construction. Also 33 non-entry path tokens sit inside used-by cells
   (corpus/lessons/round-12.md, corpus/README.md, SKILL.md, tools/mado-verify.sh, quality/check-index.py,
   tools/mado-binds.py, tools/mado-wsrules.py) which the counter's USED_BY regex never parses — so a stale/ghost
   non-knowledge back-reference can never raise `extra`. Registered scope, but "registry back-reference
   consistency" therefore holds only over knowledge entries.
3. **Anchor under-coverage**: 4 of the 20 filled pairs cite line pointers outside the row's anchored ranges
   (S158 :2085-2092/:2107/:2126 and :2270-2280 vs anchor max 2003-2044; S201 backend.cpp:105,119-122 vs anchor :38;
   S319 :382 vs anchor :60-145/:101-116; S277 :61 — S277's anchor lists no lines at all). Token-level C3 cannot see
   this; it is a C1-style scope defect in pre-existing rows (outside the fix, which touched cell 11 only).

## 4. Null results / positive verifications (each with its command)

- **Allowlist construction faithful to the frozen rule**: derived name-only set = {Contract MIS} ∪ {Crit N/R/M-N}
  equals the 24-row allowlist exactly (`allowrule.py`: both set differences empty). Reader disagreements disclosed
  by registration are exactly S044, S096/config-health, S113 (Contract name-only, Crit leaning-use) and S359
  (Contract REAL, Crit M-N) — S046 (Contract BORD/Crit U) correctly NOT exempt.
- **Allowlist line-sha column byte-exact**: independent recomputation of LINESHA (token lines, outside fences,
  joined by \n) matches all 24 (`verify.py`) — so `stale=0` is honest.
- **No unrecorded/over-recorded knowledge pairs**: independent missing(non-allowlist)=0, extra=0 (with the counter's
  USED_BY regex), dangling=0, conflict=0 (`allowrule.py`).
- **Receipt fidelity**: `used-by-old-to-new.md` == actual base→rev used-by diff (23 rows, 41 additions, 0
  mismatches, no missing/extra rows) (`receipt.py`).
- **Cell-11-only edits**: 0 non-used-by cell changes across all rows base→rev; 9 new rows S383–S391 added
  (`verify.py`).
- **Comma separators (E13)**: no used-by part with internal whitespace; all parts single paths (`sep.py`).
- **Disclaimer scan**: across all 41 filled pairs, only S318/S319 (bind-key-match) and S352/S353 (dispatcher) carry
  "held (cited, not re-registered)" phrasing — reviewed above and judged reliance; no other fill carries disclaimer
  language. Across the 24 allowlisted pairs, the only non-disclaimer mentions are S030's (redirected to S017, whose
  used-by carries the entry) and S044's (F1) — consistent.
- **Counter + harness reproduced** at rev (see §0), including the harness's own "counter vs harness missing
  diverge (not scored)" note (harness missing = 24 at rev = exactly the allowlist size; 65 at base = 41+24).

## 5. Residual risks / could not verify

- The S044 borderline (F1) and the S352/S353 borderline (§1 #19/#20 + F4) are judgment calls; the frozen allowlist
  sha (and the frozen 24-row count in the predicate sentence) means neither can be corrected without a v3
  re-registration; I did not attempt to mutate the allowlist (the counter checks allow_sha against the frozen
  value, so any mutation fails as `allow_sha`, not as `missing`).
- I did not audit the other 21 filled pairs (outside scope); their wave-1 labels are REAL/U with the same
  distribution as my in-scope 20 (0 name-only among filled, 6 hedges total), and the disclaimer scan over all 41
  (§4) found the same four "held" pairs as the only non-clean ones.
- Host-side checks (hyprctl etc.) were not needed for this seat; none run.

## 6. Scratch

All fixtures/scripts lived under `/fast/scratch/hyaku/mado-r56/R56W2RevUsedByB/` (removed before yield); key
evidence copied to `.ufo/waves/round-56/w2/R56W2RevUsedByB/`: `filled.json` (independent 41-pair derivation),
`dump.txt` (full citing-line context for the 44 in-scope pairs), `quotetab_output.txt` (per-reason locality),
`pointer_convention.txt` (base-state pointer-only convention test). No lane or fleet files were written except the
deliverables above; no git/jj mutation anywhere outside scratch.
