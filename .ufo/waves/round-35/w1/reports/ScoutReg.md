# ScoutReg — wave 1 registry-vs-staged id census (mado lane)

Date: 2026-10-24. Extractor (both sources):
`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]+' | sort -u`

## Counts

| Set | Source | Unique ids | Range |
|---|---|---|---|
| Lane registry | `mado-shokunin/corpus/SOURCES.md` | **192** | S001–S202 (non-contiguous tail: …S189, S196, S201, S202) |
| Staged append | `shokuknow/merge/mado/SOURCES.append.md` | **140** | S197–S336 contiguous |

## Intersection

`comm -12` → **2 ids: S201, S202.** The staged file re-lists two ids the lane has
already allocated; net-new staged ids = 138 (S197–S200, S203–S336).

## Lane's highest allocated id

**S202** (numeric max; `sort -tS -k2 -n | tail`).

## S197–S210 lane allocation status

| Id | Status | | Id | Status |
|---|---|---|---|---|
| S197 | free | | S204 | free |
| S198 | free | | S205 | free |
| S199 | free | | S206 | free |
| S200 | free | | S207 | free |
| S201 | **ALLOCATED** | | S208 | free |
| S202 | **ALLOCATED** | | S209 | free |
| S203 | free | | S210 | free |

## Column-zero fixture check

Scratch fixture `/tmp/scratch-fixture.md`:

```
| S001 |
  | S002 |
\t| S003 |
    | S004 |
```

- Census-tolerant pattern → matched `S001`, `S002` (0–3 leading spaces only; tab and
  4-space rows still missed — known bound).
- Column-zero-only `^\|` → matched `S001` only.

**Yes — a column-zero-only pattern would have missed the indented `  | S002 |` row.**
The `^ {0,3}` prefix is load-bearing for indented entries.

## Evidence

Commands above were re-executed at write time; outputs quoted verbatim from the runs.
Intersection confirmed by `comm -12` on both extracted sets.
