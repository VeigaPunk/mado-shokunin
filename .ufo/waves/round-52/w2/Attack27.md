# Attack27 — C2 new source pins "genuinely opened this round"

Seat: `Attack27` (mutation-tester), wave `w2`, round 52. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`,
frozen base `85d57a818c3707397e21c840b6498b105ba798aa`. This is an attack report, not a vote and not an
author judgment.

Axes: **coverage** (the attacked clause is C2's "grounded in sources opened this round"); **operability**
only through the landed counter that is supposed to enforce the clause.

## Attacked clause

`claims-frozen.md` C2: *"a distinct new indexed knowledge entry is grounded in sources **opened this
round**; each material factual proposition maps to a pinned source quote <=25 words"* — and the
registration predicate: each mapped `S###` row must be `mined`, carry this round's access date, and be
**absent from the registry at the frozen base** (the counter's own clause (c) is what proves a row was
opened this round rather than reused).

## What I verified independently (not trusting any seat's checker)

All commands run read-only from the fleet root against lane files; scratch only under
`/fast/scratch/hyaku/mado-r52/Attack27/` (removed on exit). No network fetch — "opened this round" is
tested through on-disk receipts, digests and git objects, which is the strongest evidence the
source-only boundary permits.

| test | command / locator | observed | verdict |
|---|---|---|---|
| T1 pin identity, three copies agree | `sha256sum .ufo/waves/round-52/fetch/Hyprland-*` vs `.ufo/waves/round-52/fetch/SHA256SUMS` vs `.ufo/waves/round-51/fetch/SHA256SUMS` vs `w1/C2EntryDraft/fetch/*` | 4/4 files: identical sha256 across the L1 r52 copy, the seat's r52 copy, and the committed r51 manifest (DT `7248cbb8…`, CA.cpp `a83abeb5…`, CA.hpp `746c6f51…`, KM.cpp `8d8f35fc…`); bytes/lines match `w1/C2EntryDraft/pins.txt` (35997/868, 71407/1772, 6960/122, 39334/975) | **reproduced** — the pinned bytes are internally consistent; cannot confirm a network open occurred (see L1) |
| T2 rows absent at base | `git show 85d57a81…:corpus/SOURCES.md | grep -c 'S37[0-9]'` | `0` — S370-S373 are genuinely new rows at working tree; at any committed rev they are absent | **reproduced** at working-tree level; **nothing is committed yet** (T6) |
| T3 rows present now with round date | `git diff corpus/SOURCES.md` | 4 rows appended, `mined`, `2026-10-27`, `used-by` = `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`; README index row + Search-log note "Opened 2026-10-27 … S370, S371 and S373 reuse canonical URLs with new scopes; distinct-scope review remains outstanding" | **reproduced**; QUALITY17 distinct-scope review explicitly still open — recorded by the lane itself |
| T4 anchor spans hold the cited code | `sed -n` of the four r52 fetch files at the registry anchors | `DispatcherTranslator.cpp:531-627` covers `sendshortcut`(:531-589)+`sendkeystate`(:591-627); `ConfigActions.cpp:1530-1616` covers `Actions::pass`+twin; `ConfigActions.hpp:114-117` = state fields incl. `m_timeLastMs`; `KeybindManager.cpp:221-242` = `stringToModMask` | **reproduced** |
| T5 quote-at-pin re-verification | own parser over `w1/C2EntryDraft/proposition-map.tsv` × L1 r52 fetch bytes (whitespace-collapsed, ≤25 words) | 18/18 props OK, max 22 words, 0 misses — agrees with C2EntryDraft `quotes-check.txt` and C2PinAudit `r52` receipt, computed against the L1 copy, not the seat's | **reproduced** |
| T6 commit state of the landing | `git status --short`, `git log -1` | tip IS the base `85d57a81`; `corpus/SOURCES.md`/`README.md`/`tool-ledger.md` modified-uncommitted; entry `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` and counter `quality/counters/c2-r52-proposition-entry.py` untracked (`??`) | **the "new counter / committed rows" premise is NOT yet landed** — consistent with the wave warning that r-green proves a fixture only |
| T7 landed counter enforces "opened this round"? | read `quality/counters/c2-r52-proposition-entry.py` (2.6 KB rewrite; draft was 965 lines) + forged fixture | `--base` is parsed at L19 and **never used**; no fetch-root/pin-file/anchor/quote-existence check; row check = only `'mined'`, `'2026-10-27'`, entry name in row text. Forged fixture: one pre-existing row `S364` dated 2026-10-27 with fabricated quotes → `verdict=TARGET_MET exit=0` | **FALSIFIED** — the landed counter cannot distinguish a row opened this round from a reused/never-fetched one; the "genuinely opened" clause has **no working enforcement** |
| T8 counter vs landed entry grammar | staged clone: apply the real working-tree diff + entry, `git commit`, run counter | default run → `entry=absent` (default `--entry` = `…synthetic-key-dispatch-r52.md`; landed slug is `…synthetic-dispatch-r52.md`). With `--entry` override → `props=0 … miss=props`: the counter's regex wants `id|row|claim|pin|anchor|quote|rationale` (7 cells); the landed table is `id|proposition|row|pin:anchor|quote|class|why` (7 cells, row in col 3) | **FALSIFIED at default** — even committed, the landed entry+rows score TARGET_MISSED through slug + grammar mismatch, not through any real defect |
| T9 base control | counter `--rev 85d57a81…` on lane | `entry=absent verdict=TARGET_MISSED exit=1` | **reproduced** — the no-work control misses, but vacuously: the entry name it looks for does not exist anywhere |
| T10 distinct-scope (QUALITY17) | compare anchors: S370 :531-627 vs S365 :30-35,797-867; S371 :1530-1616 vs S367 :1664-1682; S373 :221-242 vs S364 :41-113,602,782-823 & S352 :369-899+ | all line-disjoint; S372 is a new URL (no `ConfigActions.hpp` row at base) | **reproduced** — scopes are disjoint; the mandatory human distinct-scope review is still open per the lane's own Search log |

## Concrete falsifiers found

1. **The enforcement control is broken, not just weak.** The landed
   `quality/counters/c2-r52-proposition-entry.py` is a 47-line rewrite, not the 965-line draft. It
   (a) never opens the base registry — `--base` is dead — so a row opened last round, or dated
   2026-10-27 in a prior round like S364-S369, passes; (b) never touches `fetch/` bytes — a
   proposition can cite a nonexistent quote at a nonexistent anchor and still pass (my forged
   fixture: `TARGET_MET`, exit 0, quotes `word one two three` …). Reproduction:
   `python3 -I quality/counters/c2-r52-proposition-entry.py --repo <fixture> --rev <rev> --work <scratch>`
   on a repo whose SOURCES.md contains only a pre-existing `mined|2026-10-27` row → `TARGET_MET`.
2. **Slug mismatch.** Counter default entry `hyprland-synthetic-key-dispatch-r52.md` vs landed
   `hyprland-synthetic-dispatch-r52.md`; the string `synthetic-key-dispatch` appears **0 times** in
   `corpus/SOURCES.md` and `corpus/README.md`. Default scoring reports `entry=absent` forever.
3. **Grammar mismatch.** Even with `--entry` fixed, the landed table puts the row in column 3; the
   counter regex requires it in column 2 → `props=0`. The staged-landing run proves the current
   working tree cannot pass this counter in any configuration.
4. **Uncommitted premise.** All C2 evidence (rows, index, entry, counter) is uncommitted on top of the
   frozen base; a counter that reads `git show <rev>:…` sees none of it. "Opened this round" is true
   of the working tree, not of any committed revision yet.
5. **Semantic wording defect in the landed entry (source-truth sample).** Landed P17:
   *"`sendshortcut`'s repeat branch can invoke its delegate twice"* — but the `keyState == 2`
   repeat branch at `DispatcherTranslator.cpp:619-622` sits inside **`sendkeystate`** (:591-627);
   `sendshortcut` (:531-589) contains no repeat branch and no delegate. The quote binds; the claim
   misattributes the owner. (Sibling-draft P04 states it correctly.) This is exactly the class the
   frozen clause reserves for non-author source-truth sampling; flagging it for that reviewer, not
   adjudicating.

## What survives the attack

- Pin bytes are three-way identical (r52 L1 fetch == r52 seat fetch == committed r51 manifest) and
  every anchor span contains the cited construct; all 18 draft quotes re-verify independently.
- S370-S373 are genuinely absent at base, carry `mined` + `2026-10-27`, and their cited spans are
  line-disjoint from same-URL prior rows (S365, S367, S364/S352); S372 is a new URL.
- Honest limitation of the claim itself: all four pins are **byte-identical re-reads of round-51
  fetch bytes** — no new upstream evidence entered the corpus this round; novelty lives in rows,
  scopes and propositions. If a reviewer reads "opened this round" as "new source content," the
  clause fails; as "rows newly opened under this round's access date," it holds — pending the open
  QUALITY17 review the lane itself flagged.

## Verdict

- Clause "pins opened this round / rows absent at base / mined+dated / quotes ≤25 words at anchors":
  **reproduced** on working-tree evidence.
- Specified control (`quality/counters/c2-r52-proposition-entry.py`) as the mechanism that proves
  "opened this round": **falsified** — no base comparison, no pin-byte binding, and it cannot parse
  the landed entry (default `entry=absent`; `--entry` override `props=0`).
- Net: the premise is true in the working tree but **currently unverifiable by its own counter and
  uncommitted**; "verify specified control" fails on both halves.

## Limitations

- No network use (source-only boundary): I cannot prove the 2026-10-27 `curl` events happened; the
  claim rests on seat `verify.txt` + mtimes (10:03 seat, 10:47 L1) + three-way digest agreement.
  Upstream truth of the commit `efb50993…` ↔ "Hyprland 0.56.2" was not re-verified.
- The forged-fixture pass uses a synthetic repo; it shows what the landed counter *would* admit, not
  that the lane's real rows are false — T2/T4/T5 show they are not.
- `mtime`s are consistent with the story but prove nothing about transport.
- Other C2 aspects (index admission authority, entailment, prose quality) are outside this item.

## Errors encountered / reported

- Landed counter's `--base` and `--work` are dead arguments (parsed, unused).
- Landed counter default `--entry` names a path that exists nowhere in the lane.
- Landed counter regex silently mis-parses the landed entry table (row column position).
- Landed entry P17 misattributes the repeat branch to `sendshortcut` (it is `sendkeystate`'s).
- Prior seat reports referenced in evidence: `w1/C2EntryDraft.md`, `w1/C2CounterDraft.md`,
  `w1/C2PinAudit.md`, `w1/C2Novelty.md` — none contradicted by these findings; the draft counter's
  own `r-green` caveat is confirmed by T7/T8.

## Report trailer

```
seat=Attack27 wave=w2 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
item=C2 new source pins genuinely opened this round
evidence=.ufo/waves/round-52/fetch/ (4 pins, sha256 three-way equal to round-51/fetch/SHA256SUMS)
evidence=.ufo/waves/round-52/w1/C2EntryDraft/{proposition-map.tsv,pins.txt,fetch/verify.txt}
evidence=corpus/SOURCES.md (wt) S370-S373 mined 2026-10-27; base rev: absent (grep -c S37[0-9] = 0)
evidence=quality/counters/c2-r52-proposition-entry.py:19 (dead --base), :28 (7-col row-in-2 regex)
forged_fixture_verdict=TARGET_MET exit=0  (reused pre-existing row; quotes never checked)
staged_landing_verdict=entry=absent (default) / props=0 (--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md)
quote_reverify=18/18 OK whitespace-collapsed, max 22 words, against .ufo/waves/round-52/fetch
verdict=clause REPRODUCED on working-tree evidence; control FALSIFIED (no opened-this-round gate, cannot parse landed entry, all changes uncommitted)
scratch=/fast/scratch/hyaku/mado-r52/Attack27 (removed on exit)
report=.ufo/waves/round-52/w2/Attack27.md
```
