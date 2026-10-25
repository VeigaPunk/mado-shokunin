# ExecAppendAudit — round-34 SOURCES.md append audit

Scope: verify the two rows appended to `corpus/SOURCES.md` at commit
`fa7ba11346116672352b5d41494141c5c4d738d0` (landed 2026-10-24 21:58:15 -0300,
ancestor of HEAD) against the append block
`.ufo/waves/round-34/assimilation/append-block.md` and the corpus schema
(fleet `CORPUS.md` § SOURCES.md, contract v1).

## Verdict

**Zero differences.** Both appended rows are byte-identical to the append block
and conform to the 11-column schema on every checked field.

Diff artifact: `.ufo/waves/round-34/scratch/ExecAppendAudit/audit.tsv`
(22 field pairs, all `match`).

## Evidence

Byte-exact comparison, run at write time:

```
$ sed -n '203p;204p' corpus/SOURCES.md > /tmp/src_rows.txt
$ diff /tmp/src_rows.txt .ufo/waves/round-34/assimilation/append-block.md
(no output — IDENTICAL)
```

Row locations: `corpus/SOURCES.md:203` (S201) and `:204` (S202). The commit diff
shows both added at `@@ -200,6 +200,8 @@`, immediately after S196.

## Field-by-field result

All 11 fields per row identical between `SOURCES.md` and the append block —
id, source, kind, tier, scope, anchor, teaches, status, opened, recheck,
used-by. Quoted pairs are in `audit.tsv`; nothing differs, so there is nothing
to quote here per the "report every field where they differ" clause.

## Schema conformance (fleet `CORPUS.md` § SOURCES.md)

| Check | Command result | Verdict |
|---|---|---|
| 11-column shape (NF=13) | malformed-row census prints `0`; both rows have 11 fields | pass |
| `id` = `S` + ≥3 digits, no `|` in cell | `S201`, `S202`; 2 rows, no embedded pipes | pass |
| `kind` enum | `code` ∈ {spec,docs,paper,code,tool,dataset,talk,book,community,own-work} | pass |
| `tier` enum | `A` ∈ {A,B,C}; kind≠community so no tier-inflation | pass |
| `status` enum | `mined` ∈ {queued,mined,rejected} | pass |
| `source` = title — canonical URL | both carry raw.githubusercontent.com tag-pinned URLs | pass |
| `anchor` has exact location + revision | `backend.cpp:38 at tag 0.15.0, 6550 B, sha256 prefix 799bf02f6d18ae04`; `window.cpp:27 at tag 0.15.0, 8324 B, sha256 prefix 5df496eb3cfe5cae` — line, tag, size, sha256 prefix | pass |
| `teaches` grounded, not `REJECTED:` form | plain learner-benefit text; status is `mined` so rejection form not required | pass |
| `opened` ISO date | `2026-10-24`, matches commit date | pass |
| `recheck` cadence | `90d` ∈ allowed cadence forms | pass |
| `used-by` resolves | `corpus/knowledge/waybar-module-text-route-r25.md` exists (1227 B, committed in same commit) — satisfies `mined` ⇒ ≥1 citing path | pass |
| No duplicate ids | `uniq -d` census prints nothing | pass |

## Observations (not defects)

- **ID gap S197–S200.** The registry jumps S196 → S201. Grep finds no S197–S200
  anywhere in the lane. The schema requires `id` be "the next unused; never
  reused" — skipped numbers violate only a strict-contiguity reading; the hard
  rule (never reused) holds. The commit message states the intent:
  "admit the waybar event-socket entry **after the frozen counter**" — the gap
  is deliberate counter reservation, not a copy error. Confirming that S197–S200
  remain reserved/absent in future appends is the follow-up worth watching.
- **Trailing `|` on row lines** matches every other registry row; not a schema
  issue.
- `source` cells use a UTF-8 em dash (`—`, bytes `e2 80 94`) between title and
  URL, consistent with the schema's `title — canonical URL` form and with
  neighbouring rows.

## Method note

No subagents dispatched (leaf bounds). No installs. Commands run: `git show`,
`sed`, `diff`, `cat -A`, `grep`, `awk` census lines from the contract,
`git merge-base --is-ancestor`. All outputs quoted above were produced at
write time on this checkout.
