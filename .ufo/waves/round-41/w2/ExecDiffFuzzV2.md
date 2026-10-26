# ExecDiffFuzzV2 — delivered `tools/mado-globals.py` vs `PRED-C1-r41-v2`'s model on hostile inputs

Round 41 (hyaku 7), inline v2 wave w2, lane `mado-shokunin`.
Seat dir: `.ufo/waves/round-41/w2/ExecDiffFuzzV2/`.
Report: `.ufo/waves/round-41/w2/ExecDiffFuzzV2.md` (this file); detailed write-up:
`.ufo/waves/round-41/w2/ExecDiffFuzzV2/fuzz.md`.

## What was attacked

- **The delivered tool** `tools/mado-globals.py` at DATA commit
  `07f2641696b5ac73de1404ea737a9f27e9819aa1` (copied byte-identically into the
  seat; sha256 `286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e`,
  identical to the v2 reference `c1/ctl-ref-tool-v2.py.txt`).
- **The v2 model** `quality/counters/c1-r41-globals-v2.py` at the same commit
  (sha256 `59e117d88c30fb7de44aa08e30d0d7ac5d4f7bcdeeacf3463b701871df4c3a63`),
  imported with `importlib`; `main()` never called.
- Hostile-input classes per the task: `Got interface: ` lines in other shapes
  (ignored count), FIFO / directory / symlink-to-FIFO paths, a file that grows,
  `-o short` captures, 128/129-char names, versions 999999/1000000, invalid
  UTF-8 in host/pid positions, 8 MiB boundary.

## Evidence (exact commands, receipts in the seat dir)

```
python3 -I fuzz.py --quick --jobs 8      # mutants=81 disagreements=0
python3 -I fuzz.py --jobs 8              # mutants=4845 disagreements=0
python3 -I variants.py                    # 4 variant teeth runs, all >0 disagreements
python3 -I verify_quotes.py               # 5/5 quotes verified (<=25 words, file:line)
```

- `fuzz-receipt.txt` (full sweep): `fuzz: mutants=4845 disagreements=0`,
  `classes={}`, all structural probes `ok`, all 12 CLI cases `ok`.
- `fuzz-summary.json` (full sweep): mutants 4845, disagreements 0, minimised [].
- `fuzz-receipt-<variant>.py.txt` / `fuzz-summary-<variant>.py.json`:
  ascii-digits 2 disagreements, str-max 2, int-pid 5, splitlines 2 — each with
  a minimised input.
- `regex-equality.txt`: tool `ADVERT`/`BOOT`/`NAME` patterns and class tables
  equal the counter's (5/5 True; 27 table names, 10 classes).
- `quotes-receipt.txt`: 5/5 quotes verified.

## Findings

**No defect found.** Measured, not assumed:

1. Tool vs model: **0 disagreements in 4845 mutants** (≥ 3000 required) on
   rc + stdout bytes with stderr-empty enforcement (rc 0/1/3/4). The mutations
   cover the v2 classes above at ≥ 12 variants each plus exhaustive systematic
   sweeps (name/version/pid boundaries, host/pid invalid UTF-8, alien `-o`
   shapes alone and mixed, boot variants, empty/malformed files).
2. Structural contract probes all pass and never block: FIFO, symlink-to-FIFO,
   directory, symlink-to-directory, dangling symlink, missing path → `SETUP
   unreadable` rc 2; symlink-to-regular-file parses; empty file → rc 3;
   exactly 8388608 B parses, 8388609 B → `SETUP too_large` rc 2; a growing
   file that passes the cap mid-read → rc 2 (bounded, no hang); a stalling
   regular file (writer holds the fd open, silent) returns rc 3 in well under
   12 s — regular-file reads hit EOF, so no hang vector exists there; file mode
   spawns nothing (journalctl stub earlier on PATH not executed).
3. CLI: 12/12 pass. Two v1-known ambiguities re-measured and recorded as
   inherited, not defects: `--journal-file ""` → `usage`; `--journal-file ""
   --live --journalctl <stub>` runs the live program (empty value counts as
   absent). `--expect=-x` → `bad_expect` (contract reading; v1 reference
   answered `usage` — resolved differently, harmlessly).
4. Harness teeth: the same quick corpus against four one-sentence-wrong
   variants reports disagreements (9 total) with minimised demos
   (`(ver ١)`, `9→10`, `[1952]/[01952]`, trailing `\r`), so the 0 is a
   measured negative, not a vacuous pass.

## Files written (all inside the seat dir)

`fuzz.py`, `variants.py`, `variants/` (4 variants), `tool-under-test.py`,
`counter-v2.py`, `fuzz-receipt.txt`, `fuzz-summary.json`,
`fuzz-receipt-<variant>.py.txt`, `fuzz-summary-<variant>.py.json`,
`regex-equality.txt`, `verify_quotes.py`, `quotes-receipt.txt`, `fuzz.md`,
`scratch/`.

## Environment / installs

No tool installs. System `python3` 3.14.8. No pacman, no host services, no
compositor/socket access, read-only git use only.

## Risks / notes for the L1

- The 0 is a negative result on a finite corpus; the harness is sensitive to
  the four sentences the v2 fixtures were written to pin (vernum0/pidzeros0/
  asciidigits0/unrec0), so the corpus is not vacuous.
- The `--journal-file "" --live` behavior (empty path counts as absent) is an
  unavoidable argparse-level ambiguity, unchanged from v1; the counter's
  `usage0` fixture does not reach it.
- Quote checks: 5/5 (≤ 25 words, located, grepped).
