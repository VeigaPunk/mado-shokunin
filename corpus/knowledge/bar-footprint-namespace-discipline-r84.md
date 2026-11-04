source: S486 — https://www.rfc-editor.org/rfc/rfc8259.txt section 4; tools/mado-barfoot.py and .ufo/waves/round-84/claims-declaration-r84.md
verified-at: 2026-11-04; instrument freeze 3f9eec3906ddd1492e8bc08325e83064f00111ea
recheck: python3 -I quality/counters/c1-r84-namespaces.py --repo . --rev REV --base-rev 7fd43921294116299dfce1443d56a951b9c81493 --controls .ufo/waves/round-84/controls/c1-cases-r84.json --carried .ufo/waves/round-83/controls/c1-cases-r83.json --scratch-root DIR

# The join requires unambiguous declaration identities

The allocation map carries one integer band per namespace. Repeated JSON keys were erased by ordinary JSON decoding before the resolver could inspect them. RFC8259 section4 says object names SHOULD be unique and describes differing receiver behavior, including last-value selection. It does not require a JSON parser to reject duplicates; this instrument chooses refusal instead of an arbitrary band.

A composed declaration also has one namespace per surface, including the implicit bar. The tool now refuses a repeated namespace across extras or an extra reusing the bar's name. That is this join's deliberately narrower grammar, not a layer-shell protocol law. Two real surfaces may share a namespace; the caller must not claim this instrument can distinguish them merely by assigning repeated declaration names.

| Input | Tool outcome | License |
|---|---|---|
| Allocation object repeats a key | setup refusal, rc2 | no last-value guess |
| Two declared extras share a name | setup refusal, rc2 | no double attribution under one identity |
| Extra reuses the bar's name | setup refusal, rc2 | the bar's allocation cannot identify two declarations |
| Distinct declared identities | existing model continues | prediction over supplied bytes, not observed rendering |

Frozen finite population: 61 cases, first58 carried, 41 named mutations. Re-derive counts with the recheck command; the held r83 tool scores 58/61 in `.ufo/waves/round-84/receipts/control-c1-r84-at-base.txt` (re-executed this round). The candidate verdict belongs to its measurement receipt, not this note.

## Limits and rejected interpretations

This does not solve r83's surviving positive-band, explicit-zone or live-box-substitution causal cheats. It does not reject ambiguous live reply arrays, prove that one declared namespace has one live surface, or certify arbitrary allocations. Negative tests constrain only the named declaration classes. No compositor/config write or socket request occurs.
