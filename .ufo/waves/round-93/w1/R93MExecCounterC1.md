# R93MExecCounterC1 — C1 counter `c1-r93-portal-bytes.py` (PRED-C1-r93-v1)

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Base revision `4c6f723f3dca3a26f9d14475d695fe797e2e972c` (master). All runs below are **DRAFT** (counter `--draft-tool`, exit 3) unless stated; no receipts written. Declaration: `.ufo/waves/round-93/claims-declaration-r93.md` §C1.

## What was written

- `quality/counters/c1-r93-portal-bytes.py` (sha256 `5c91769afb8b3295686dd63cf40cea405b22243be10e04d7e70958f7e3e2d65d`) — written from `quality/counters/c1-r90-portal-routing.py` implementing PRED-C1-r93-v1 exactly as worded in the declaration draft:
  - Docstring = the predicate sentence; receipt line `MADO_PORTAL_BYTES: TARGET_MET|TARGET_MISSED|DRAFT_* pred=PRED-C1-r93-v1 rev=… cases=… correct=… bytes_cases=… bytes_correct=… fresh=…/… fresh_bytes=…/… fresh_seed=… mutants=… killed=… crashed_not_killed=… r12_rule_correct=… host_table_correct=… do_nothing_correct=… base_correct=… base_bytes_correct=… tool_sha256=…`.
  - `write_fixture()` materialises fixtures as bytes via `text.encode("utf-8", "surrogateescape")` so lone surrogates (`\udcXX`) land as raw bytes (replaces the round-90 strict `open(…, encoding="utf-8")`).
  - Extra args: `--oracle PATH` + `--expect-oracle-sha256` (the round-93 oracle file), `--fuzz-bytes-gen PATH` + `--expect-fuzz-bytes-sha256`, `--fresh-bytes` (default 60). Both pins are sha256-checked with SETUP_ERROR rc 2 on mismatch. Round-90 fuzz generator is loaded from the round-90 controls dir for the 120-case fresh leg.
  - Byte subset = cases with `class` in a/b; for the round-92 stand-in file (no `class` field) the class is derived from the id suffix after `d1-` (`a1`–`a5`→a, `b1`–`b5`→b) via `case_class()`.
  - Mutant semantics: a mutant is killed only if it returns a well-formed answer differing from the label on ≥1 frozen case (`outcomes() == "wrong"`); crash/timeout/unparseable is `crashed_not_killed`, never a kill (QUALITY 148). A mutant whose `find` occurs ≠1 time in the measured tool is SETUP_ERROR rc 2.
  - All temp dirs are created under `--scratch-root` (`tempfile.mkdtemp(dir=a.scratch_root)`, prefix `c1r93-`); no `/tmp` literal anywhere (grep-verified). `bwrap` sandboxing kept verbatim from round 90.
  - `--draft-tool FILE` prints `DRAFT_*` and exits 3. `met` additionally requires `fresh_bytes_correct == a.fresh_bytes` and `base_bytes_correct < bytes_cases`.
  - `host_vec` falls back to `cases[0]` when `d01-host-replica` is absent (the 16-case stand-in file has no such case; round-90's 229-case file has it, so the fallback is dead there).

## DRAFT runs (candidate `.ufo/waves/round-93/build/mado-portals.c1.py`, sha256 `89039e30…91d3`)

Inputs: round-92 16-case file `.ufo/waves/round-92/controls/portals-gkeyfile-cases-r92.json` (sha256 `a925219e…bc`), empty mutants `.ufo/waves/round-90/controls/no-mutants-r90.json`, oracle+byte-gen stand-ins in scratch (round-93 `portal-oracle-r93.py` / `fuzz-bytes-r93.py` do not exist yet; stand-ins = round-90 oracle with the one-line `surrogateescape` materialise patch, and a 60-case byte stub generator), `--fresh 120 --fresh-bytes 60`:

```
MADO_PORTAL_BYTES: DRAFT_TARGET_MET pred=PRED-C1-r93-v1 rev=draft:.ufo/waves/round-93/build/mado-portals.c1.py cases=16 correct=16 bytes_cases=10 bytes_correct=10 fresh=120/120 fresh_bytes=60/60 fresh_seed=2298715696 mutants=0 killed=0 crashed_not_killed=0 r12_rule_correct=1 host_table_correct=5 do_nothing_correct=0 base_correct=8 base_bytes_correct=2 host_tail_sha256=4a4cf319…fbf9 tool_sha256=89039e30…91d3
```
rc 3, runtime 7.2 s, 16 `case … ok` lines, fresh seed `2298715696` (= first 8 hex of candidate sha256). Full log: `.ufo/waves/round-93/w1/R93MExecCounterC1-draft5.log`. Earlier 8/8 DRAFT: `.ufo/waves/round-93/w1/R93MExecCounterC1-draft1.log` (fresh=8/8, fresh_bytes=8/8, rc 3, 0.9 s).

## Self-check: base tool on the byte subset

Base `tools/mado-portals.py` at `4c6f723f` (no `--draft-tool`, same 16 cases, 8/8 fresh legs) → rc 1, `TARGET_MISSED`, `correct=8 bytes_cases=10 bytes_correct=2 base_bytes_correct=2` — i.e. `base_bytes_correct < bytes_cases` holds, and the 8 base failures are exactly a1–a4 + b1–b4 (matches R92MExecD1 §"Base tool 8/16"). Log: `.ufo/waves/round-93/w1/R93MExecCounterC1-draft2.log`.

## Mutant SETUP_ERROR path

Synthetic mutant `{"id":"T01","find":"ZZZZ_NOT_PRESENT",…}` → rc 2, `MADO_PORTAL_BYTES: SETUP_ERROR mutant T01 find occurs 0 times`. Log: `.ufo/waves/round-93/w1/R93MExecCounterC1-draft4.log`.

## Notes for L1 / R93MExecCasesC1

1. The counter cannot run its measured form until `.ufo/waves/round-93/controls/portal-oracle-r93.py`, `.ufo/waves/round-93/controls/fuzz-bytes-r93.py`, `.ufo/waves/round-93/controls/portal-cases-r93.json` and `portal-mutants-r93.json` exist and their sha256 pins are frozen. The DRAFT runs above used the round-92 16-case file + scratch stand-ins, as the seat spec directed.
2. The byte stub generator exercised here is a stand-in, not the real `gen_cases(n, seed)` contract of `fuzz-bytes-r93.py`; if R93MExecCasesC1's generator has a different signature, the call `FUZZ_BYTES.gen_cases(a.fresh_bytes, fresh_seed)` in `main()` will need a one-line adapter.
3. `blind=` (round-90's bl- subset line) was dropped from the receipt line: the spec's receipt-line field list has no `blind`.

## Risks / blockers

- None blocking. Counter parses (`ast.parse` ok), no `/tmp` literal, scratch-only temp dirs (all `--scratch-root` dirs removed after each run; only the copied DRAFT logs remain in `w1/`).
- No `tools/`/`quality/` (other than the new counter) edit; no git/jj mutation; no install (pacman paused; none needed). Scratch `/fast/scratch/hyaku/mado-r93/R93MExecCounterC1` held only stand-ins + logs, deleted before yield; cited logs copied into `w1/`.

Report: .ufo/waves/round-93/w1/R93MExecCounterC1.md
