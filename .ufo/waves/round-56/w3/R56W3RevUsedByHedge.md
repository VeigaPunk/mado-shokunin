# R56W3RevUsedByHedge — pinned C3 fill audit

Attack: C3 used-by integrity, citation fidelity, base-text immutability and hedge honesty. Axes: cell-only integrity; receipt fidelity; citation fidelity; base-text immutability; hedge honesty.

Scored base `13f0acbe3a15da2d9c08357a576d91dcadc85273`; scored tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`. Scored bytes read exclusively using read-only `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show/diff/ls-tree`; not working-tree content. Frozen v2 claims and registration read first, v1 C3 definitions consulted. No tracked-content changes, delegation, git mutations or host actions.

## Findings, by severity

**Blocking: none found in the assigned checks.** This is a review recommendation, not admission or a counter TARGET_MET verdict.

**D1 — weakens reviewability; pre-existing; ROUTED round 57.** `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:53` says “this entry opens no row for either file.” But :14 and :18 declare S364/S368, and the pin table :32/:39 assigns precisely those two files to those rows. C3 adds this entry to S352/S353 at `corpus/SOURCES.md:301-302`, partly supported by that contradictory held/new bookkeeping. The preceding :52 byte-identity attribution and :278 held-row census still support reliance; therefore the fill is defensible and this is **not** a frozen token-level predicate break. The 70-entry byte comparison proves the contradiction predates the fix. Input and full contexts are in the receipt. Do not change a frozen predicate or entry under this assignment.

## Decisive null results

Exact driver:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevUsedByHedge/audit.py
EXIT: 0
SUMMARY base_rows=319 tip_rows=332 checked_cells=3509 changed_rows=23 added_pairs=41 removed_pairs=[] errors=[]
RECEIPT_TABLE_EQUAL True missing_rows [] extra_rows []
BASE_TEXT_SUMMARY checked=70 changed=[] new=['corpus/knowledge/hyprland-config-autoreload-r56.md']
FILLS_WITHOUT_CITATION []
```

The driver executes, and the receipt records verbatim:

```text
git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff 13f0acbe3a15da2d9c08357a576d91dcadc85273 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 -- corpus/SOURCES.md
git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff 13f0acbe3a15da2d9c08357a576d91dcadc85273 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 --stat -- corpus/knowledge
 corpus/knowledge/hyprland-config-autoreload-r56.md | 167 +++++++++++++++++++++
 1 file changed, 167 insertions(+)
```

All 3,509 cells of all 319 pre-existing registry rows were compared; exactly 23 cell-11 changes, no other changes or removed rows/paths. All 23 old/new cell strings equal the committed receipt table. Thirteen new rows S383–S395 are additions, not modifications of base rows. All 70 base entry texts remain identical, with per-entry SHA256 proof. Every one of the 41 added (row, entry) pairs cites its row outside code fences; citing lines and individual reliance verdicts are recorded for **41/41**.

The brief's suggested scan of the new autoreload entry cannot establish the 41 historical-entry pairs: those paths name older entries. The driver checks each actual added entry and separately records the new entry's S300-series citations.

## Hedge audit

Cell 11 contains bare paths, not confidence wording. A used-by fill records use; it does not upgrade a hedge to certainty. Entry hedges are unchanged byte-for-byte.

The brief names “5 hedged fills”; frozen registration-v2 :89 instead says six M-U/BORD pairs, and w2 A/B discuss additional weak cases. Rather than silently select five, the receipt gives judgments for every fill and expressly covers these **11** weak/indirect/borderline pairs:

- S015/walker-route: procedural reliance, explicitly “Per the S015 protocol.”
- S046/output-colour: indirect “S046 in the U4 note”; no binary/source-equivalence assertion.
- S091/arc-synthesis: weak digest attribution; S091 does register the matching binary digest.
- S096/closeout and waybar-walker-semantics: thin binary-record pointers, not disclaimers or execution claims.
- S158/S162/S175/S177 × hyprctl-verification-layer: attribution-only reliance. :304 expressly calls it a pointer; :308 says live counts were not recaptured. No evidence of new direct derivation.
- S352/S353 × dispatcher: held byte-identity reliance, qualified by D1.

Also retained S057/terminal-trees' “not re-derived here” qualification. No filled pair was judged an explicit non-reliance disclaimer. Agreement with all 41 fills is limited to reliance/token-back-reference semantics, not source entailment or confidence calibration.

## Residual risks and verification gaps

- No C3 counter/harness or broader tests run by this seat; no claim to reproduce the at-final receipt.
- S057's Hidden=true source entailment is unverified; this audit establishes its citation and inherited-use wording only.
- Animation attributions are weak indirect use; S176 is hidden inside S175–S177 by the frozen literal-token rule, a disclosed limit rather than a new predicate failure.
- `read xd://lsp` returned “No such tool”; LSP status, references, definition and diagnostics were unavailable. Literal-token/blob comparisons are fallback evidence, not semantic-server proof.
- Runtime canonicality, same-identity rerouting, saturation and resume continuity are unrelated to these content-only checks and were not exercised.
- No tools installed/upgraded. No scratch files/directories, clones, fixtures or temporary files were created, so no scratch cleanup was necessary. All persistent writes are within the named seat deliverables.

## Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevUsedByHedge/receipts/usedby-a2.txt` — full diff, cell proof, receipt match, hashes, all citation lines, 41 per-fill verdicts, hedge contexts and finding.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevUsedByHedge/audit.py` — reproducible read-only audit driver.
- This report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevUsedByHedge.md`.

Self-evaluation: accuracy 4 (reliance judgments are review judgments, not entailment proofs); completeness 5 (all 319 rows, 70 base texts and 41 fills checked); clarity 4 (full raw diff is lengthy, decisive summary above); actionability 4 (D1 precisely located but routed, not fixable within frozen scope); conciseness 4 (all-pair evidence intentionally retained). Mean 4.2/5. Improvements: resolve D1 only in next-round content work; keep summary distinct from raw receipts. Would the user agree? Expected for the mechanical proofs; hedge judgments remain explicitly contestable.
