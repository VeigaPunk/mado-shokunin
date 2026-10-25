# CriticC1FalseNeg — C1 counter vs unrelated noise (extra `source:` line + extra registry row)

Probe: does honest C1 work plus unrelated noise flip the frozen counter to `TARGET_MISSED`
(a false negative)? Registration asserts "Extra `source:` lines do not change the count."
The claim dies iff honest work prints `TARGET_MISSED`.

## Setup (executed)

- Copied `controls/golden` → `scratch/CriticC1FalseNeg/golden` (exists; no rebuild needed):
  2 entry files, `SOURCES.md` with 4 rows (S190, S191, S197, S189), 4 fetch blobs.
- Sanity run on the unmodified copy: `verdict=TARGET_MET` exit 0 — copy reproduces golden.
- Appended one unrelated `source:` line to `corpus/knowledge/waybar-module-text-route-r25.md`:
  `source: S186 extra line that r32 counted` (same probe line as the `extra-source` control).
- Appended one registry row for the unrelated id to `corpus/SOURCES.md`:
  `| S186 | x | code | A | t | a | q | mined | 2026-10-24 | 90d | corpus/knowledge/event-delivery-limits-r26.md |`

## Run (re-executed at write time)

```sh
python3 -I .ufo/waves/round-33/c1/count.py \
  --root .ufo/waves/round-33/scratch/CriticC1FalseNeg/golden \
  --frozen .ufo/waves/round-33/c1/frozen.json
```

Output (verbatim):

```
PRED-C1-r33-v1 closed_entries=2 closed_rows=4 open_cites=0 verdict=TARGET_MET
exit=0
```

## Why (code read, `.ufo/waves/round-33/c1/count.py`)

- `gate_quote()` (lines 43-48) scans only lines starting `gate-quote: <sid> `; a `source:`
  line can never match the needle for any frozen id.
- `row_for()` (lines 35-40) matches registry lines by exact prefix `| <sid> |` / `|<sid>|`
  for the four frozen ids only; the extra `| S186 | ... |` row is never inspected. It also
  cannot shadow a frozen row: it appears after all four and starts with a different id.
- `spec["entries"]` iterates only the frozen cite-map; S186 is not fetched, hashed, or quoted.

## Verdict on the probe

No false negative. Honest work + unrelated `source:` line + unrelated registry row still
prints `TARGET_MET` exit 0, matching the pre-data `extra-source` control receipt
(`c1-extra-source.txt`). The registration line "Extra `source:` lines do not change the
count" survives this probe; the claim does not die here.
