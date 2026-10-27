# MutC1ToolRandom — w2 falsify report (round 50, hyaku run 10 attempt 2)

## Random RMLVO parity / D3

**Observed:** 400/400 generated RMLVO keymaps compiled; tool and judge agreed byte-for-byte on stdout and exit status for all 57,865 random (keymap, keysym) pairs (0 mismatches). This independently reproduces the 57,865-pair / 400-keymap volume claimed in round-49 registration, with my own committed seeds; it does not recover the original L1 seed sequence.

- Attack revision: `b4a79843cc2545bbe800db9322e58f6e00436629`.
- Tool SHA-256: `dcc13cce3b7134946208116cd98599fb8f56a2b81fc6f26b9598ac5429b40265`.
- Judge SHA-256: `f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54`.
- Seeds: keymaps `0x52534B4D`, pairs `0x52504152`, exotic `0x45584F54`; see `seeds.txt`.
- Exact invocation, methodology, counts and hashes: `random-parity.txt`.
- Generator and runner: `gen_campaign.py`, `run_campaign.py`.
- Random output: `n_keymaps=400 compile_failures=[] n_pairs_attempted=57865 n_pairs_compared=57865 mismatches=0 elapsed_s=145.5`.

## Exotic keymaps

**Observed:** 30 exotic RMLVOs compiled; 6,000 tool/judge pairs compared; 0 mismatches. The set covers multiple groups, dead-key layouts, Compose options, LevelThree/LevelFive, group-switch options, and keysyms extracted from compiled keymaps. One spec (`layout=kp`) could not compile because the installed XKB data lacks `symbols/kp`; it is explicitly inconclusive. Compose options were included, but active Compose-sequence behavior was not tested because the required parity invocation disables Compose.

- Exact invocation, targeted families, compile failure and result: `exotic-parity.txt`.
- Runner: `run_exotic.py`.

## Mutation probe

**Mutant:** active output renderer header changed `LEVEL#` → `LEVEL` (scratch-only copy). Expected exact stdout+rc detector behavior: pristine match, mutant divergence, restored match. **Observed:** `pristine=match`, `mutant=diverge`, `restored=match`; all exit codes 0. Mutated SHA-256 `073821d510ca9c1d9900c9d41d5e88c98142e4da624517a8bb5240fc6bb886fe`; restored SHA equals pristine `dcc13cce3b7134946208116cd98599fb8f56a2b81fc6f26b9598ac5429b40265`. Full evidence: `mutation-probe.txt`. An earlier exploratory change to duplicate `_page` header literal survived on this CLI path; it is recorded as a coverage finding, not a shipped defect.

## Deliverables

`seeds.txt`, `random-parity.txt`, `exotic-parity.txt`, `mutation-probe.txt`, `gen_campaign.py`, `run_campaign.py`, and `run_exotic.py` are in `.ufo/waves/round-50/w2/MutC1ToolRandom/`. No lane files outside this seat directory were modified. Scratch artifacts are removed before handoff.
