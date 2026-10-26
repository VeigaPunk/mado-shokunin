# ExecHarmBase — harm-check baseline at the round-43 base

Seat `ExecHarmBase` (w1, leaf executor). Round 43, lane `mado-shokunin`.
Base under test: `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f` (round-42 tip).
Receipt: `.ufo/waves/round-43/w1/ExecHarmBase/harm-base.txt` (5,086 bytes, committed with this report).

## Method

- Fresh clone, scratch only: `D=$(mktemp -d -p /fast/scratch/hyaku/mado-r43/ExecHarmBase)` →
  `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/mado-shokunin "$D"`;
  `git -C "$D" rev-parse --show-toplevel` printed exactly `$D`; `git -C "$D" checkout -q a35cfdf…`;
  `git -C "$D" rev-parse HEAD` = `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`, `git status --porcelain` = 0 lines.
  No mutation of the lane, its index, or the fleet: every git call named `-C "$D"`; the lane was only read.
- Every command in the assignment was run in `$D` except the census, which is defined over the real lane root
  (`/home/vgpnk/Projects/shokunin`, lane `mado`). `check-index-rows.py --help` read first: it requires `--rev REV`
  or `--root ROOT`; the bare form was still run as assigned and recorded.
- Scratch tree (311 MB) deleted after copying the receipt; `ls` of the scratch path now fails.

## Results at base (all in `harm-base.txt`)

| check | output | exit |
|---|---|---|
| `bash tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 460/460 assertions passed` | 0 |
| `python3 -I tools/mado-options.py --selftest` | `MADO_OPTIONS_SELFTEST: 211/211 passed` | 0 |
| `python3 -I tools/mado-globals.py --selftest` | `MADO_GLOBALS_SELFTEST: 63/63 passed` | 0 |
| `check-index.py --rev a35cfdf --repo .` | `indexed=59/59 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | 0 |
| `check-index-rows.py` (bare) | `SETUP_ERROR: --rev or --root is required` | 2 |
| `check-index-rows.py --rev a35cfdf --repo .` | `rows=59 errors=0 warns=3` + 3 WARN lines | 0 |
| `check-axis-scores.py --rev a35cfdf --repo .` | `navigation 59/59`, `calibration 63/63`, `operability 12/12`, `checked=3 mismatched=0` | 0 |
| `sources-census.sh validate --root …/shokunin mado` | 7 × W04 duplicate-url (S030, S042, S045, S097, S119, S120, S121), W01 S277, `ok` | 0 |

Counts at the base, and the same counts re-derived at the round-41 rev `2a65350a4df2a31985ed37e90df90325348a8820`
inside the same clone:

- `tools` = 11 (`mado-action-plan.py mado-anims.py mado-assessment.py mado-binds.py mado-eventq.py
  mado-evidence-audit.py mado-globals.py mado-options.py mado-tripwire.py mado-verify.sh mado-wsrules.py`;
  no `mado-geometry.py`, consistent with C1's "before" state) — 11 at both revs.
- `corpus/knowledge` = 59 — 59 at both revs.
- `corpus/SOURCES.md` rows matching `^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|` = 226 — 226 at both revs;
  file sha256 (first 16) `df130e81dbcf88c6` at both revs and identical to the real lane's working copy (`cmp -s` → 0).
- `QUALITY.md`: **there is no `QUALITY.md` at the repo root**; the criteria file is `corpus/QUALITY.md`, last numbered
  criterion = **76** (`^[0-9]+\.` last match), unchanged at the round-41 rev. (The assignment's `QUALITY.md` resolves to
  this path for mado; if the L1 meant a root file, that file does not exist in this lane.)

## Comparison with `.ufo/waves/round-41/receipts/harm-tip.txt` (rev `2a65350`)

Identical at base: 460/460, 211/211, 63/63, `indexed=59/59 coverage=10.0000/10`, the three axis rows, and `exit=0`
on every command the round-41 receipt records. **No axis or gate moved between the round-41 tip and the round-43 base.**

Every difference, with cause:

1. **`check-index-rows` WARN lines.** The round-41 receipt records one WARN
   (``WARN cited-glob-nomatch: `.ufo/waves/round-24/fetch/S###.bin` in row knowledge/rule-attribution-r24.md``)
   while its own summary line says `warns=3`. At base the checker prints all three (`getprop-*.txt` in
   `window-rule-effects-getprop.md`, `drift-*.txt` in `config-drift-r12.md`, and the `round-24/fetch/S###.bin` one).
   The tool is byte-identical across both revs (`git diff 2a65350 a35cfdf -- quality/check-index-rows.py …` is empty;
   recorded in the receipt), so this is an **abbreviated capture in the round-41 receipt**, not a change at base.
2. **`check-index-rows` command form.** The round-41 receipt records `$ check-index-rows` with no arguments. Bare
   invocation is `SETUP_ERROR: --rev or --root is required`, exit 2, at *both* revs (the tool's `--help` names only
   `--rev/--repo/--root/--selftest`). The round-41 block therefore cannot be replayed as written; the `--rev` form is
   the functional equivalent and is what is recorded at base.
3. **`sources-census` output length.** The round-41 receipt records 2 lines (W01 S277, `ok`); the same command at base
   prints 9 lines (7 W04 + W01 + `ok`), exit 0. `.ufo/waves/round-42/receipts/census-before.txt:1-9` and
   `census-after.txt` — taken at the round-41 tip — carry the **same 9 lines**, and `diff` of that file against the
   base run is empty (recorded). Round-41's census block is also an abbreviated capture, not a tree change.
4. Revision token in the header (`2a65350` → `a35cfdf`) and the attack of the checks over a *clone* rather than the
   lane worktree — as assigned.

Quoted round-41 lines were verified against the committed receipt's bytes by `grep -c` (each returns 1, last block of
`harm-base.txt`): `check-index-rows`, the `round-24/fetch/S###.bin` WARN line, the `mado<TAB>W01<TAB>S277` census line,
and `MADO_INDEX_ROWS: rev=2a65350`.

## Verdict

**No harm at the round-43 base.** Every assigned check passes at base with the numbers the lane published at its
round-41 tip (and round-42's axis-base receipt): 460/460, 211/211, 63/63, 59/59 indexed, 59/59 rows with 0 errors,
axes 59/59 + 63/63 + 12/12 with 0 mismatches, census `ok` exit 0. The counts that a wave could disturb (tools 11,
knowledge 59, SOURCES rows 226, last criterion 76) are the round-41 values. The only differences are two capture
defects in the **round-41 receipt** (a dropped WARN pair inside a block whose own summary says `warns=3`, and a
2-line census capture), plus the round-41 receipt's non-replayable bare `check-index-rows` header; none of them is a
state difference at base.

## Risks / residuals (for the L1, not scored here)

- The census was run against the **real lane worktree** (HEAD `5add5b45a65ddaa18fad00c6afa9dbfda29ee0b0`, dirty with
  wave writes), because the script validates `<root>/<lane>/corpus/SOURCES.md`; that file is byte-identical to the
  base rev (`cmp -s` → 0), so the 9-line output is the base's. A future census warning on another lane file would not
  be caught by cloning.
- The round-41 receipt's index-rows and census blocks are citable only after the corrections above; if the L1 reuses
  `harm-tip.txt` as a comparison anchor, `warns=3` in its summary (not its one printed WARN) and the 9-line census are
  the correct anchors.
- Per assignment, no build/lint/test gate beyond the listed commands was run, and no post-integration comparison was
  made (the wave is in flight).

## Tooling

No tool installed or updated; no package operation was run. Only `timeout` from coreutils and the lane's own scripts
were used. Scratch (`/fast/scratch/hyaku/mado-r43/ExecHarmBase`, 311 MB) deleted; nothing left on disk outside this
seat directory. No subagent dispatched; no background job; no compositor verb invoked.
