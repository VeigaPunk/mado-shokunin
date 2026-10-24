# MutExistingGates — mutation test of the lane's existing gates (round 32, w1)

Seat: leaf member (no subagent dispatch). Target: `quality/check-index.py`,
`quality/check-index-rows.py`, `.ufo/waves/round-31/c2/count.py` (PRED-C2-r31-v2).
All work in `.ufo/waves/round-32/scratch/MutExistingGates/` — gate bytes copied to
`mutants/` and `baseline/`, mutated copies only. Lane files and `round-31/` tree
unmodified (verified: `git status` clean on both paths; md5 `74c5a5ca` /
`dc8074e4` / `0e6e3482`).

## Harness (scratch copies of the lane tree)

- `tree/` — scratch lane tree: `corpus/`+`tools/`+`quality/` copied wholesale plus
  the `.ufo` members cited by Sources cells (existence-only targets). Faithful:
  unmutated `check-index.py --root tree` → `indexed=43/43` exit 0;
  `check-index-rows.py --root tree` → `rows=43 errors=0 warns=0` exit 0.
- `clone/lane/` — `git clone --no-hardlinks` of the lane at
  `50e6a8f32bfaf0487b2762eb3b5c9f51ed54b75c` for `count.py` rev mode
  (`HEAD` → `resolved_active=41/41`, `TARGET_MET`, exit 0).
- `fixtures/tree-m1` — scratch tree + appended row `| `knowledge/ghost-mut1.md` …`
  (registry row for a note that does not exist).
- `fixtures/tree-m2` — scratch tree + row **inside the coverage-map table**
  `| `knowledge/ghost-mut2.md` | filler holds | `source:` S9999; recheck `tools/nope.py REV` |`
  (dangling row carrying a missing cited path).
- `fixtures/tree-m2b` — scratch tree, Holds cell of row 1 extended with
  `see `knowledge/ghost-mut2b.md`` (literal "Holds names a note that does not exist").
- `fixtures/n1-empty`, `fixtures/n3-section` — copies of the committed round-31
  negative controls; invocation from `round-31/w1-spec.json`:
  `python3 -I count.py --active-min 2 --quality <d>/corpus/QUALITY.md --lessons-root <d>`.

Baselines (unmutated copies, defect-detection confirmed):

| fixture | unmutated gate prints | exit |
|---|---|---|
| tree-m1 | `MADO_INDEX: … dangling=1` / `dangling: knowledge/ghost-mut1.md` | 1 |
| tree-m2 | `MADO_INDEX_ROWS: … errors=1` / `ERROR cited-path-missing: `tools/nope.py`` | 1 |
| tree-m2b | `MADO_INDEX_ROWS: … errors=0 warns=0` | 0 |
| n1-empty | `UNRESOLVED criterion 1: empty corpus/lessons/round-99.md`, `TARGET_MISSED` | 1 |
| n3-section | `UNRESOLVED criterion 1: id \bM23-7\b absent in section '#mistakes'`, `TARGET_MISSED` | 1 |

## Verdict table

| # | mutant (copy) | intended acceptance | fixture result | verification apparatus | verdict |
|---|---|---|---|---|---|
| M1 | `m1-check-index.py` `dangling = []` | dangling registry row accepted | accepts (exit 0, `dangling=0`) | gate `--selftest` → `11/12`, `FAILED: dangling row exits 1…`, exit 1 | **KILLED** |
| M2 | `m2-check-index-rows.py` dangling-row early `continue` | dirty dangling row accepted | accepts (exit 0, `errors=0 warns=0`) | `--selftest` → `10/10` exit 0; no selftest case builds a dangling row | **SURVIVES** |
| M3 | `m3-count.py` delete `elif not body.strip()` (PATH_RE) | empty lesson resolves | n1 → `resolved_active=2/2 TARGET_MET` exit 0 | committed n1-empty fixture expectation (UNRESOLVED/MISSED) | **KILLED** |
| M4 | `m4-count.py` `scope = body` | wrong-section id resolves | n3 → `resolved_active=2/2 TARGET_MET` exit 0 | committed n3-section fixture expectation (UNRESOLVED/MISSED) | **KILLED** |
| M5 | `m5-check-index.py` delete case-3 `check(...)` | selftest silent | n/a (selftest integrity mutant) | `MADO_INDEX_SELFTEST: 11/11 assertions passed` exit 0 | **SURVIVES** |

## Per-mutation detail

### M1 — `check-index.py` accepts a registry row whose note does not exist — KILLED

Mutation (full diff in `scratch/MutExistingGates/logs/all-diffs.txt`):

```diff
-    dangling = sorted(set(counts) - notes)
+    dangling = []
```

- On `tree-m1`: `MADO_INDEX: … indexed=43/43 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0 — the defect is accepted.
- On clean `tree/`: unchanged, exit 0 (no false positives).
- **Killed by:** `python3 -I <copy> --selftest` → `MADO_INDEX_SELFTEST: 11/12 assertions passed` / `FAILED: dangling row exits 1 and names the row`, exit 1. Selftest case 3 (`t3`, notes `[a.md]` rows `[a.md, ghost.md]`) is the tripwire. The `missing` and `duplicates` operators were not run — no claim.

### M2 — `check-index-rows.py` accepts a row whose named note does not exist — SURVIVES

Mutation (hoist the `nt is None` bail from after the cell/SRE/path checks to the
top of the row loop — a dangling row now escapes **all** per-row checks, not just
the overlap WARN):

```diff
         line = lines[i]
+        nt = note_text(name)
+        if nt is None:
+            continue  # dangling row: the completeness gate owns this finding
         cells = [c.strip() for c in line.split("|")]
```

- On `tree-m2`: `MADO_INDEX_ROWS: … rows=44 errors=0 warns=0`, exit 0 — a dangling
  row whose Sources cell cites a **missing lane path** (`tools/nope.py`) and a
  bogus S-token is fully certified. Baseline printed `errors=1`, exit 1.
- On clean `tree/`: unchanged, exit 0.
- **Kill check:** `python3 -I <copy> --selftest` → `MADO_INDEX_ROWS_SELFTEST: 10/10
  assertions passed`, exit 0. The 10-case suite contains no dangling-row fixture —
  every `_write_tree` call lists only existing notes. SURVIVOR.

**Named defect MEG-S1 (dangling-row checks delegation is total):** "the
completeness gate owns this finding" (`check-index-rows.py:258`) is true only for
the row's first cell. If `check-index.py`'s dangling detection ever weakens (see
M1 — one assignment), the row-fidelity gate is a silent second hole: nothing
re-examines a dangling row's cells. Worse, the two gates' surfaces don't even need
to disagree — F-M2 sits *inside* the table, so `row-outside-map` can't fire; a
missing Sources path on a missing note was one `continue` away from invisible.

**Named defect MEG-S2 (pre-existing, no mutation needed — literal reading):** a
Holds cell naming a nonexistent note is accepted by the gate **as shipped**.
Baseline on `tree-m2b` (Holds = `…; see `knowledge/ghost-mut2b.md` for the
update`, valid S-row, real note): `errors=0 warns=0`, exit 0. Backticked paths are
existence-checked only in the **Sources** cell (`BT_RE.findall(src)`); the Holds
cell is never scanned for cited paths, and `RP_RE` would not match
`knowledge/…` anyway (its root allowlist is `.ufo|tools|quality|corpus|scripts|templates`).
The Sources cell shares this hole for `knowledge/` targets: a Sources citation
`` `knowledge/ghost.md` `` is equally invisible. Under mutation-testing terms the
defect is an equivalent mutant — the gate already behaves as if the check were
mutated away. (WARN-fidelity note: `overlap()` runs on the note's own bytes only;
the ghost mention evades even `holds-no-overlap` because ≥5 real note words remain.)

### M3 — `count.py` accepts a citation whose lesson file is empty — KILLED

Mutation (restores the r30 existence-only semantics — RevC2Counter S1 regression):

```diff
             if body is None:
                 c["fail"] = f"missing {path}"
                 ok = False
-            elif not body.strip():
-                c["fail"] = f"empty {path}"
-                ok = False
         c["resolved"] = ok
```

- On `n1-empty` (criterion 1 cites `lessons/round-99.md`, a 0-byte file):
  `resolved_active=2/2`, `PRED-C2-r31-v2 verdict=TARGET_MET`, exit 0 — the defect
  is accepted. Baseline: `UNRESOLVED criterion 1: empty corpus/lessons/round-99.md`.
- Collateral: on `n3-section` still `TARGET_MISSED` (mutation is precise); on
  clone `HEAD` still `TARGET_MET` (no real-rev regression).
- **Killed by:** the committed fixture run —
  `python3 -I <copy> --active-min 2 --quality fixtures/n1-empty/corpus/QUALITY.md --lessons-root fixtures/n1-empty`
  prints `TARGET_MET` against the registered expectation (`w1-spec.json`: n1 must
  print UNRESOLVED/miss). Note the kill is **procedural, not automated**: no
  selftest exists in `count.py`; the fixture only kills because a runner compares.
  Only the PATH_RE site was removed; the ANCH_RE (`:267`) and SPELL_RE (`:295`)
  `body.strip()` checks remain — an empty file can still never satisfy an
  anchored/spelled citation (anchor finds no heading; no id matches), so the
  single-site mutation is sufficient and the residual two checks are unreachable
  for this defect shape.

### M4 — `count.py` accepts a citation whose lesson is in the wrong section — KILLED

Mutation (restores r30 whole-file blindness — RevC2Counter S8 regression):

```diff
-            scope = "\n".join(secs)
+            scope = body
```

- On `n3-section` (`lessons/round-23.md#mistakes M23-7`, where `M23-7` lives under
  `## Disposition`): `resolved_active=2/2`, `TARGET_MET`, exit 0 — accepted.
  Baseline: `UNRESOLVED criterion 1: id \bM23-7\b absent in section '#mistakes'`.
- Collateral: `n1-empty` still `TARGET_MISSED`; clone `HEAD` still `TARGET_MET`.
- **Killed by:** the committed fixture run —
  `python3 -I <copy> --active-min 2 --quality fixtures/n3-section/corpus/QUALITY.md --lessons-root fixtures/n3-section`
  prints `TARGET_MET` against the registered UNRESOLVED expectation. Same caveat
  as M3: the kill lives in the receipt comparison, not in any self-check.

### M5 — `check-index.py` selftest skips one assertion — SURVIVES

Mutation (delete the case-3 `check(...)` call; the `t3` fixture still builds and
the child still runs — only the verdict is dropped):

```diff
         r = _run(tool, "--root", t3)
-        check(
-            "dangling row exits 1 and names the row",
-            r.returncode == 1 and "dangling: knowledge/ghost.md" in r.stdout,
-        )
```

- `--selftest` prints `MADO_INDEX_SELFTEST: 11/11 assertions passed`, exit 0 —
  the banner self-normalizes (`len(checks)` shrinks with the deletion); a green
  11/11 is indistinguishable from a green 12/12.
- Gate logic itself still catches the defect (`--root tree-m1` → `dangling=1`,
  exit 1), so the survivor's bite is composition:
- **Composite proof** (`m5m1-composite.py`, M5 + M1 in one copy — throwaway, in
  scratch): `--selftest` → `11/11` exit 0 **while** `--root tree-m1` → `dangling=0`,
  exit 0. The suite certifies a dangling-blind gate as fully green.

**Named defect MEG-S3 (selftest integrity):** the pass denominator is the number
of `check()` calls executed, not a pinned constant. Any deleted or
exception-swallowed `check()` moves numerator and denominator together. Both
gates share the shape (`MADO_INDEX_SELFTEST`, `MADO_INDEX_ROWS_SELFTEST`); a
pinned expected count (or a checksum/manifest of assertion names) is the boring
fix.

## Observations (not mutant-derived)

- `count.py:213` defines `exists_nonempty()` — never called (only `file_text`
  is used). Dead helper; harmless but invites the r30-style mistake it names.
- `SRE = \bS\d{3}\b` in `check-index-rows.py` ignores 4+-digit ids: `S9999` in
  F-M2 was never evaluated (`cited-s-undefined` needs a 3-digit match). If
  SOURCES ever exceeds S999, undefined-id checking silently stops scaling.
- `count.py` has no `--selftest`; its fixture suite (`negative/n1..n4`) kills
  M3/M4 only under the registered runner expectations — a lane that stops
  re-running them loses the tripwire.

## Coverage limits

Single mutants only (the M1+M5 composite is a demonstration, not a sweep);
`--root` mode exercised for both quality gates, fixture + rev mode for
`count.py`; `missing`- and `duplicates`-dropping mutants of `check-index.py`
not run — no kill claim for them. Mutation operators chosen to restore known
r30 regressions (M3/M4) or to invert the named check directly (M1/M2/M5).
