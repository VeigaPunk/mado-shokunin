# R65RevFrontier — mado round 65 frontier attacks (§2b conformance)

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` @ `cb63ab13ccaf85191318701d5db5ace050bd5bd4` (`git rev-parse HEAD`, rc=0; `--show-toplevel` = lane, rc=0).
Scratch: `/fast/scratch/hyaku/mado-r65/w1/R65RevFrontier/` (removed at exit). Evidence copies: `evidence/` in this seat.
Installs: none. Lane writes: none (seat dir + this report only). No git mutation. No credential-shaped material opened.

Census command used throughout: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (script header: exit 0 clean/warnings; 1 E/overdue findings; 2 usage/missing registry).

## F1 — root census vs round-start baseline — PASS (no delta)

- Command: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado > census-now.txt` → **rc=0**, 38 lines (`evidence/census-now.txt`).
- Baseline: `.ufo/waves/round-65/receipts/census-start-r65.txt` (same command, rc=0 receipted as `census-exit=0`).
- Diff (`diff` of baseline body vs now, wrapper line stripped): **no delta** in content. The only difference is the receipt's trailing `census-exit=0` wrapper line (not census output).
- `grep -n round-65 census-now.txt` → rc=1 (no line names a round-65 path).
- Warnings unchanged: 36× W04 (duplicate URL across scopes) + 1× W01 (S277 tier-C mined used-by). None new.

## F2 — grammar of S028 / S097 — PASS

Header (line 11): 11 columns `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

| row | line | inner cols (awk -F'|', NF−2) | escaped `\|` | opened (col 10) | recheck (col 11) | used-by (col 12) |
|---|---|---|---|---|---|---|
| S028 | 40 | 11 (NF=13) | 0 | `2026-10-19` (ISO, valid, E08 clear) | `on-release` (symbolic, E09 clear) | `corpus/knowledge/hyprland-config-era-r12.md` |
| S097 | 109 | 11 (NF=13) | 0 | `2026-10-20` (ISO, valid) | `on-release` (symbolic, E09 clear) | `corpus/knowledge/theme-route-r18.md` |

Both rows are schema-clean. Commands: `grep -n "^| S028 |"`, `awk -F'|'` field count, `grep -o '\\|'` count → 0.

**Premise defect (spec, not lane):** the frozen plan says "S028 recheck cell 2026-10-19 → 2026-11-03". The string `2026-10-19` is in the **opened** column (col 10); the **recheck** cell of S028 is `on-release`. Same for S097: the `2026-10-20` value is in the opened column; its recheck cell is `on-release`. The old→new log must name the opened column (or be restated as "recheck cell stays on-release"). No predicate change is implied; the lesson's Gate block must cite the cell correctly.

## F3 — pre-landing green proof of the recheck-cell edit — PASS for the literal (opened-column) edit; FAIL-TRAP for the alternative reading

Edits applied to scratch copies only (`edit` tool; lane untouched; lane `corpus/SOURCES.md` sha unchanged, `git diff --quiet` rc=0):

- **Variant A (literal old→new strings, opened column):** S028 line 40 col 10 `2026-10-19 → 2026-11-03`; S097 line 109 col 10 `2026-10-20 → 2026-11-03`.
  - Diff vs lane: exactly 2 changed lines (40, 109), 810 lines both, changed-cell check shows only col 10 differs (`evidence/SOURCES-A.diff.txt`).
  - **Method trap found:** `sources-census.sh validate --file <scratch>/SOURCES.md` (no mirror tree) → **rc=1 with 497× E11** ("missing used-by"), because E11 resolves used-by paths against the file's own tree (`sources-census.sh` ~L560, `[ -e "$dir/$path" ]`). This is a false failure for ANY scratch copy; `evidence/val-A.txt`. The original lane file validated with the same invocation rc=0 (`evidence/val-orig.txt`), so the trap is the method, not the edit.
  - Correct proof method: mirror tree = symlinks to every lane top-level entry and every `corpus/*` entry except `SOURCES.md`, plus the edited copy at `mirror-X/corpus/SOURCES.md`.
  - **Control** `validate --root /home/vgpnk/Projects/shokunin --file <mirror-O>/corpus/SOURCES.md mado` (unmodified bytes) → **rc=0**, 38 lines, 0 E-lines (`evidence/val-mirror-O.txt`).
  - **Proof** `validate --root /home/vgpnk/Projects/shokunin --file <mirror-A>/corpus/SOURCES.md mado` → **rc=0**, 38 lines, 0 E-lines; `diff` of control vs proof output → rc=0 (identical; `evidence/val-mirror-A.txt`).
  - `census ... --file <mirror-A>` → rc=0; tier A/B/C = 357/7/7 (unchanged); status mined/queued/rejected = 350/10/11 (unchanged).
  - `overdue --today 2026-11-03 ... mado` → rc=0, 0 overdue; both rows listed only as `cadence` (on-release is symbolic, never judged overdue).
- **Variant B (alternative reading: S028 recheck cell `on-release` → ISO `2026-11-03`):** S028 only (same mechanism would apply to S097).
  - `validate` → rc=0, 0 E-lines (E09 accepts ISO).
  - `overdue --today 2026-11-03` → **rc=1**: `overdue S028 0d recheck=2026-11-03 opened=2026-10-19` (`evidence/od-B.txt`). So a recheck date equal to the round date would make the round-end overdue leg red.
  - `overdue --today 2026-10-31` → rc=0 (`evidence/od-B2.txt`).
  - Recommendation: take Variant A's cells as the logged edit, or keep recheck `on-release` and log only the opened change. Do NOT set a recheck date equal to the landing date unless the overdue leg is run at a date before it.

## F4 — id-collision guard — trivially satisfied (no rows appended)

- Staged set: `git diff --cached --name-only` → rc=0, **0 files**. `git status --porcelain -- corpus/SOURCES.md corpus/lessons/` → rc=0, empty. No rows appended; this round adds no registry rows.
- §10 collision pair (ids as `^| *S[0-9]{3,} *|`):
  - `corpus/SOURCES.md` unique ids: **371** (`sort -u | wc -l`); rows: **371** (`grep -c`); duplicate ids (`uniq -d`): **0**.
  - `corpus/lessons/round-65.md` ids: **0** (file absent; grep rc=2 suppressed → count 0).
  - `comm -12` intersection: **0**. Collisions: **0**.

## F5 — round-65 lesson must be NEW — PASS (no stale draft)

- `ls -la corpus/lessons/round-65.md` → rc=2 ("No such file").
- `find corpus -iname '*r65*' -o -iname '*round-65*'` → rc=0, no output.
- `git ls-tree -r --name-only cb63ab13… -- corpus/lessons/ | grep -i 65` → rc=1 (no match).
- `grep -rl round-65 corpus` → only `corpus/lessons/round-64-verifier-spotcheck.md:236` ("landing counters is the lane's stated round-65 intent"). That is a forward reference in a prior lesson, not a stale draft; no inherited-state defect.

## Other observations (not in F1–F5 scope, recorded for the L1)

- Lane `git status --porcelain` shows untracked orchestration files under `.ufo/waves/round-65/` (`w1-dispatch.json`, `w1-run.err`, `w1-run.out`, `w1-spec.json`, `w1.ready`, `w1.ready.dispatched`, `w1/`). Not mine; not committed.
- `tools/mado-verify.sh` sha256 prefix `050efc720599345a` — matches the harm-watch value.
- Frozen-contract base mismatch is noted, not attacked: declaration says base `524fa1f9…` for before-receipts and frozen commit `cb63ab13…`; both exist in the lane log.

## Defects seen (ranked)

1. **Spec premise (F2/F3):** "S028 recheck cell 2026-10-19" — the value is in the opened column; S028/S097 recheck cells are `on-release`. Log the edit against the opened column or restate it.
2. **Proof-method trap (F3):** `validate --file <scratch>` alone gives 497 false E11; a mirror-tree proof is required. The census script's E11 resolution is `"$dir/$path"` relative to the file's tree, not `--root`.
3. **Alternative-edit trap (F3 Variant B):** a recheck ISO date equal to the round date is overdue (rc=1) on the same day.

## Commands and rc summary

| command | rc |
|---|---|
| `sources-census.sh validate --root <lane-root> mado` | 0 |
| `diff` baseline vs now (census body) | 0 content / wrapper-only delta |
| `grep -n round-65 census-now.txt` | 1 (none) |
| `awk -F'|'` field count S028, S097 | NF=13 each |
| `validate --file <scratch A>` (no mirror) | 1 (497× E11 — method trap) |
| `validate --file <lane original>` (no mirror) | 0 |
| `validate --root … --file <mirror-O>` (control) | 0 |
| `validate --root … --file <mirror-A>` (proof) | 0 |
| `diff control validate vs proof validate` | 0 |
| `census --root … --file <mirror-A>` | 0 |
| `overdue --today 2026-11-03 --file <mirror-A>` | 0 |
| `validate --root … --file <mirror-B>` (S028 ISO variant) | 0 |
| `overdue --today 2026-11-03 --file <mirror-B>` | 1 (S028 0d overdue) |
| `overdue --today 2026-10-31 --file <mirror-B>` | 0 |
| `git diff --cached --name-only` | 0 (empty) |
| `git status --porcelain -- corpus/SOURCES.md corpus/lessons/` | 0 (empty) |
| `ls corpus/lessons/round-65.md` | 2 (absent) |
| `find corpus -iname '*r65*' -o -iname '*round-65*'` | 0 (empty) |
| `git ls-tree … corpus/lessons/ \| grep 65` | 1 (none) |
| `git -C <lane> diff --quiet -- corpus/SOURCES.md` | 0 (lane untouched) |
| `sha256sum tools/mado-verify.sh \| cut -c1-16` | 050efc720599345a |
