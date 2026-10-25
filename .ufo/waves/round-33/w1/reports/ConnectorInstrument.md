# ConnectorInstrument — C1 gate-quote counter

**Verdict: the C1 counter is a new instrument.**

Searched `/home/vgpnk/Projects/shokunin/mado-shokunin/quality` (9 files) and `/home/vgpnk/Projects/shokunin/mado-shokunin/tools` (8 files), read-only. No file there requires a gate-quote line that is a contiguous substring of a fetch blob whose sha256 equals a frozen digest.

Axes: search completeness (every file in both trees); predicate fidelity (gate-quote ∧ contiguous substring of the fetch blob ∧ frozen sha256, all three); nearest-neighbor rejection (other substring or hash gates do not count).

## quality/

| path | what it requires | why it is not C1 |
|---|---|---|
| `quality/check-axis-scores.py` | published axis cells re-derived by named instruments | no fetch blob, no gate-quote |
| `quality/check-index.py` | one fence row per `corpus/knowledge/*.md` | row presence only |
| `quality/check-index-rows.py:28-30` | Holds cell shares a ≥5-word sequence with the **note's own bytes** | quotes the knowledge note, not a fetch blob; no frozen sha256; WARN, not a close condition |
| `quality/check-control-receipts.py:33-35,41,88-92` | `--counter-sha` must appear on the receipt's first line; a stored receipt line stays a substring of the checker line | substring is of a receipt/checker line, not of a fetch blob; the sha names the counter, not a frozen fetch digest |
| `quality/counter-selftest.py:4-14` | behavioural gate over round-26 C1 (`count-v2.py`, animations) and C2 (binds) | line 12: "No subject hash, AST or byte pattern is pinned" |
| `quality/check-population.py` | registered metrics agree with receipt CASE lines | does not read a fetch blob |
| `quality/population-suite.py` | offline gate over `check-population.py` | same |
| `quality/q36-successor-run.sh`, `quality/q36-successor-receipts.txt` | runner and transcript of `check-control-receipts.py` | no new predicate |

`quality/check-index-rows.py:199` (`overlap`) is the closest quote check and still fails the conjunction: subject is `corpus/knowledge/*.md`, threshold is ≥5 words, and there is no hash pin.

## tools/

| path | what it requires | why it is not C1 |
|---|---|---|
| `tools/mado-binds.py:121-122` | mod-mask via uppercase substring tests | Hyprland flag parse, not a cite |
| `tools/mado-anims.py`, `tools/mado-wsrules.py` | animation and workspace-rule parsers | no quote, no fetch digest |
| `tools/mado-action-plan.py:53-66` | `--frozen` digest of `plan.json` / `policy.json` | pins plan bytes, not a gate-quote inside a fetch blob |
| `tools/mado-assessment.py`, `tools/mado-evidence-audit.py` | sha256 of declared snapshot files | digest of an evidence bundle, no gate-quote substring |
| `tools/mado-tripwire.py` | `--frozen` replays digest-pinned `.jsonl` | transcript replay, not a fetch-blob quote |
| `tools/mado-verify.sh` | config-plane rows; `sha256sum` of config files and the skill leaf | live/declared config, not a frozen fetch blob |

No `gate-quote`, `closed_entries`, `closed_rows`, `open_cites`, or `frozen.json` fetch pin appears in either tree.

The only implementation of that conjunction is outside the searched roots: `.ufo/waves/round-33/c1/count.py:4` and `:43-87` (`gate_quote` at `:43`, `quote.encode() in blob` and `digest == fetch["sha256"]` at `:84-85`). That file is the new instrument, not a prior one in `quality/` or `tools/`.
