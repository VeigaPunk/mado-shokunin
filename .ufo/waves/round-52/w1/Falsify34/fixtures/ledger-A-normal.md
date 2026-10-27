# fixture tool ledger

| instrument | description | accountability pointer |
|---|---|---|
| `tools/alpha-tool.py` | Read-only resolver of the alpha table; prints JSON from file bytes. | `PROVINCE.md:1` |
| `tools/beta.py` | Static census of beta subscribers; prints the drop markers. | `PROVINCE.md:1` |
| `quality/check-a.py` | Gate that re-derives the A axis table and fails on drift. | `PROVINCE.md:1` |
| `quality/counters/c1-x.py` | Round-x counter: scores the x predicate against fixtures. | `PROVINCE.md:1` |
| `quality/check-tool-ledger.py` | PRED-C1-r51 gate: verifies the tool ledger is complete. | `PROVINCE.md:1` |
