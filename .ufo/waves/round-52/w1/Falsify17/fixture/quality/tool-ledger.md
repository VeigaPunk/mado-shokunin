# fixture ledger (no-work, unique rows, every pointer is a self-pointer)

| instrument | description | accountability pointer |
|---|---|---|
| `tools/ti-alpha.py` | Reads the alpha socket census and reports subscriber lag. | `quality/tool-ledger.md` |
| `tools/ti-beta.py` | Resolves the beta geometry table and prints size verdicts. | `quality/tool-ledger.md` |
| `tools/ti-gamma.py` | Classifies gamma keybind collisions. | `quality/tool-ledger.md` |
| `quality/check-tool-ledger.py` | Derives the tracked-instrument population at a revision and checks its accountability ledger. | `quality/tool-ledger.md` |
| `quality/counters/c1-r51-ledger.py` | Scores completeness of the tracked lane-level tool ledger at a pinned revision. | `quality/tool-ledger.md` |
