# C2 word-8-gram overlap replay

Axes: coverage + operability. Frozen C2 clause (c), with no predicate amendments.

## Verdict
**PASS for the frozen numeric predicate at the specified data revision; MISS for any interpretation that it inventories all prior candidate-bearing artifacts.** Independently running the frozen counter reproduces `body_shingles=2900 files=66+cand3 max=0.1%` and TARGET_MET at `a0e34387b30538372a1bb219eb3ccdc74013d458`. This says nothing by itself about semantic novelty.

## Reproduction
Command (read-only clone in seat scratch; no lane changes):

```sh
TMPDIR=/fast/scratch/hyaku/mado-r51/RevC2ShingleBaseline/work \
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r51-dispatch-entry.py \
 --repo /fast/scratch/hyaku/mado-r51/RevC2ShingleBaseline/repo \
 --rev a0e34387b30538372a1bb219eb3ccdc74013d458
```

Output included:

```text
C2_R51: c ok=1 body_shingles=2900 files=66+cand3 max=0.1% top=[0.1%:corpus/knowledge/bind-table-r25.md, 0.1%:corpus/knowledge/hyprland-bind-key-match-r50.md, 0.1%:.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md]
C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=a0e34387b30538372a1bb219eb3ccdc74013d458
```

Matches the committed data receipt `.ufo/waves/round-51/receipts/c2-at-data.txt:1-8` and w1 draft-fit receipt `.ufo/waves/round-51/w1/ScrDispatchEntry/counter-fit-receipt.txt:1-7`.

The implementation is explicit at `quality/counters/c2-r51-dispatch-entry.py:434-486`: entry body excludes fenced blocks, blank lines, table lines, and lines beginning `source|ground|held|verified-at|recheck|lane|pin` (`434-446`); lowercase text tokenized by regex `[a-z0-9]{2,}`; shingles are sets of consecutive 8-token tuples (`449-453`). Denominator is the number of *unique* entry body shingles (2900), not all occurrences; each reference's numerator is the number of those entry shingles in its own unique shingle set, divided by 2900 (`456-459`, `475-479`). References are every base-revision `corpus/knowledge/*.md` matching `KNOW_RE` (66 files, `461-465`; pattern at line 90) plus every nonempty file recursively under the tested revision's `.ufo/waves/round-*/candidate/` (`CAND_RE`, line 89; traversal at `467-474`). It reports the maximum per-file entry-side coverage, not aggregate coverage or symmetric Jaccard (`480-486`). At max 0.1% rounded to one decimal this is at most 2/2900 shingles (0.069%) if rounding conventional; counter output does not expose exact max numerator.

The result is computed against the entry at tested `rev`, the knowledge corpus at fixed base `6ca8c559a4a3d6d361101592116eea2bc7452437`, and candidate files at tested `rev`; this matches the frozen sentence (`claims.md:59-61`). The candidate set is therefore not restricted to files at the base revision.

## Excluded candidate-bearing report example

The predicate/counter does not scan prior reports under `.ufo/waves/round-*/w1|w2/`; it scans only a `candidate/` subtree (claims `:59-61`; counter `:467-474`). One concrete omitted artifact is the old C2 candidate-bearing entry copy `.ufo/waves/round-49/w1/ExecCounterC2/receipts/pos-entry.md`, whose content is a complete dispatcher/key-matching knowledge candidate (first lines and numbered mechanism account; see that path). Independent computation using the same tokenizer, 8-token consecutive tuple sets, entry-body denominator (2900 unique shingles), found 0 intersecting shingles: 976 unique shingles in that report; 0/2900 = 0.000%. This particular excluded report does not change the measured maximum. Its zero overlap is not evidence that all excluded reports are harmless; the w1 entry itself is the decisive example below.

The prior w1 candidate body is at `.ufo/waves/round-51/w1/ScrDispatchEntry/hyprland-dispatcher-dispatch-r51.md`, but it is not an old artifact at data revision? It is present in the tested tree and candidate body is not under `candidate/`; counter does not compare it. Using the same tokenizer, it has 3,838 unique shingles; 2,868 overlap the current entry's 2,900 unique shingles = **98.8966% entry-side overlap**. This is expected because it is the same entry body. It proves the counter's candidate-directory predicate omits candidate-bearing seat outputs even when they exist in the tested revision. The rule's exact scope only names candidate paths, so this is not a failure of its literal ≤30% predicate, but is an actionable limit on broader novelty claims and supports the disclosed residual in `registration.md:19`.

## Pointers
- Frozen predicate and threshold: `claims.md:51-69`.
- Counter tokenizer, body filtering, denominator, reference selection: `quality/counters/c2-r51-dispatch-entry.py:434-486`.
- Data-revision receipt: `.ufo/waves/round-51/receipts/c2-at-data.txt:1-8`.
- Prior report omission finding: `.ufo/waves/round-51/w1/RevNovelty/novelty-audit.md:18-20`.
- Residual explicitly retained: `.ufo/waves/round-51/registration.md:17-19`.

## Verification gaps
The one-decimal output does not reveal exact maximum numerator; it does reproduce the reported maximum rounding. The counter result itself establishes all 69 compared files were processed and gives top-three paths, but this replay did not independently enumerate/hash every blob's per-file pair (the implementation's `ls-tree` path selection and calculation were inspected). The old round-49 report example is outside candidate/ and quantitatively does not overlap; the w1 body demonstrates an omitted highly-overlapping candidate-bearing output, but its own status as an already-existing candidate artifact is only by its contents, not a classification encoded in the path.
