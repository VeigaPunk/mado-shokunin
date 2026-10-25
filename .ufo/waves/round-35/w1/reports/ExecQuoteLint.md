# ExecQuoteLint — gate-quote verification, round-35 w1

Scoped check: for each id in `.ufo/waves/round-35/c1/frozen.json` (`PRED-C1-r35-v1`),
verify in the golden tree `.ufo/waves/round-35/controls/golden/`:

1. the entry file carries the `gate-quote: <id> ...` line **exactly once**
   (line-anchor `^gate-quote:<ws><id>(<ws>|EOL)`);
2. the quote (the full remainder of that line after `gate-quote: <id>`) is a
   **contiguous substring** of the receipt bytes at that id's `path`;
3. the quote is **1–25 whitespace-separated words**.

Auxiliary: golden receipts were byte-identical to the lane-tree receipts at
`.ufo/waves/round-35/fetch/`, and every receipt's sha256 matches the spec —
the golden/lane choice changes no outcome.

## Results

| id   | entry (golden)                                      | line | `gate-quote` lines found | contiguous substring | words | verdict |
|------|-----------------------------------------------------|-----:|-------------------------:|---------------------|------:|---------|
| S203 | corpus/knowledge/idle-lock-never-asked-r12.md       |   12 | 1                        | yes                 |    14 | PASS    |
| S204 | corpus/knowledge/idle-lock-never-asked-r12.md       |   13 | 1                        | yes                 |    13 | PASS    |
| S205 | corpus/knowledge/idle-lock-chain-armed-r14.md       |   11 | 1                        | yes                 |    17 | PASS    |
| S206 | corpus/knowledge/idle-lock-offered-in-the-bar-r15.md|   15 | 1                        | yes                 |    13 | PASS    |
| S207 | corpus/knowledge/idle-lock-offered-in-the-bar-r15.md|   16 | 1                        | yes                 |    15 | PASS    |
| S208 | corpus/knowledge/idle-lock-offered-in-the-bar-r15.md|   17 | 1                        | yes                 |    14 | PASS    |
| S209 | corpus/knowledge/idle-lock-offered-in-the-bar-r15.md|   18 | 1                        | yes                 |    13 | PASS    |
| S210 | corpus/knowledge/idle-lock-offered-in-the-bar-r15.md|   19 | 1                        | yes                 |    15 | PASS    |

## Failures

None. 8/8 ids pass all three scoped checks.

## Receipt integrity (auxiliary, outside scope)

| id   | receipt sha256 matches spec | golden == lane bytes |
|------|-----------------------------|----------------------|
| S203 | yes (`1b7fa87f…dd1646`)     | yes                  |
| S204 | yes (`4cd5ba65…d1c54ad`)    | yes                  |
| S205 | yes (`f3387bfc…08ae1a`)     | yes                  |
| S206 | yes (`1d30e4a9…a938d5`)     | yes                  |
| S207 | yes (`81c33e79…0adec59`)    | yes                  |
| S208 | yes (`6e72f0db…6ce4654`)    | yes                  |
| S209 | yes (`a170c7a5…3bdd27c`)    | yes                  |
| S210 | yes (`ef282e38…b8726`)      | yes                  |

Method: parsed `frozen.json` with Python stdlib; matched gate-quote lines on raw
entry bytes; substring test on raw receipt bytes; word count via
`len(quote.split())`. No mutations.
