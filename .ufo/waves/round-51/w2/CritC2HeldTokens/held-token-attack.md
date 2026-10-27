# C2 held-token attack — exact fixture fails to reproduce as written

## Frozen claim and attack

PRED-C2-r51 clause (d), in `claims.md` lines 61–63, requires at least three distinct held citations to base knowledge lines, each containing every pinned key token for that citation. W1's `w1/CritHeldFacts/held-attacks.md` lines 6–15 specifies three distinct locations, lines 1–3 of `hyprland-bind-key-match-r50.md`, each with `tokens=[the]`, and asserts clause (d) passes.

## Reproduction

Used an isolated clone at `/fast/scratch/hyaku/mado-r51/CritC2HeldTokens/fixture` (verified clone root); no lane files changed. Loaded the frozen counter's base knowledge and ran its `clause_d` on the exact three `tokens=[the]` lines:

```text
exact tokens= fixture => (0, 'held=0/3 lines=3 untargeted=0 tokens=0 miss=no_tokens:hyprland-bind-key-match-r50.md:1,no_tokens:hyprland-bind-key-match-r50.md:2,no_tokens:hyprland-bind-key-match-r50.md:3', [])
```

The candidate fixture itself does not exercise a full TARGET_MET transition: `held_tokens()` only extracts tokens from `keys=`/`key=` (`quality/counters/c2-r51-dispatch-entry.py` lines 491–509) or backtick spans. `tokens=` is unrecognized. A parser-compatible control using `keys=the` also returned MISS (`held=2/3`, `token_missing` on line 2), so the attack's assertion that all cited lines contain `the` is not borne out by these base bytes for that line.

For completeness, I ran the full, unchanged counter against the registered data revision:

```text
TMPDIR=/fast/scratch/hyaku/mado-r51/CritC2HeldTokens python3 -I quality/counters/c2-r51-dispatch-entry.py --repo /fast/scratch/hyaku/mado-r51/CritC2HeldTokens/fixture --rev a0e34387b30538372a1bb219eb3ccdc74013d458
```

It exited 0 and emitted:

```text
C2_R51: meta rev=a0e34387b30538372a1bb219eb3ccdc74013d458 base=6ca8c559a4a3d6d361101592116eea2bc7452437
C2_R51: a ok=1 index_row=`knowledge/hyprland-dispatcher-dispatch-r51.md` (MADO-R51...
C2_R51: b ok=1 rows=6/2 pins=6
C2_R51: c ok=1 body_shingles=2900 files=66+cand3 max=0.1% top=[0.1%:corpus/knowledge/bind-table-r25.md, 0.1%:corpus/knowledge/hyprland-bind-key-match-r50.md, 0.1%:.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md]
C2_R51: d ok=1 held=7/3 lines=8 untargeted=1 tokens=14
C2_R51: work=/fast/scratch/hyaku/mado-r51/CritC2HeldTokens/c2-r51-5r69lc6q probe=written
C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=a0e34387b30538372a1bb219eb3ccdc74013d458
```

The full run scores the actual committed entry, not the altered attack fixture; its `d` PASS is not evidence that the `tokens=[the]` attack passes.

## Assessment

**Exact frozen wording: MISS for this reproduction attempt.** The claimed attack block's syntax is not accepted by the counter's token parser, and line 2 fails the asserted token containment under the parser-compatible control. Therefore this experiment does not falsify clause (d) or establish the advertised generic-token false positive against this exact data/counter combination. This is a counterexample to W1's reproduction claim, not proof that clause (d) is semantically robust: the broader frozen sentence still does not constrain specificity or require tokens to support a fact. The specified attack needs an amended fixture using the counter's accepted syntax and verified base lines; any such alternative is future advisory evidence, not a silent change to the frozen predicate.

**Axes:** coverage (C2 evidence supports the entry's coverage criterion only lexically); operability (counter/fixture interface mismatch prevents this exact attack from being exercised as claimed).

**Smallest safe correction:** Preserve the predicate. Correct the advisory fixture to use supported `keys=` or backtick syntax and re-check each cited base line; report this exact fixture as non-reproducing. No frozen predicate or lane data changed.
