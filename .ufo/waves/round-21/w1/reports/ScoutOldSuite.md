# ScoutOldSuite — old tripwire suite map and exact replay commands

**Axis:** C1 operability, specifically locating the frozen tripwire populations, their pins, and the previously recorded final commands. No suite, fixture, or command was executed in this scout lane.

## Findings

### Canonical historical `--selftest` suites

The final round-20 harm-watch runner discovered 11 direct suite roots with `expected.json`: four from round 17, two from round 18, and five from round 19. The runner selection is explicit in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/harm-watch.sh:292-318`; it passes each root directory to `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --selftest`.

- Round 17:
  - `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound/expected.json`
  - `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core/expected.json`
  - `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening/expected.json`
  - `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/w2-regressions/expected.json`
- Round 18 roots:
  - `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen/expected.json`
  - `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/r18-failsafe/expected.json`
  - The `frozen` root also contains per-case expected files at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen/<case>/expected.json` for: `absolute-input`, `contradictory-exit-label`, `duplicate-input-path`, `duplicate-json-key`, `expected-unlisted-file`, `extra-unlisted-input`, `known-miss-blank`, `known-miss-unreachable`, `known-miss-violated`, `label-clean-with-findings`, `malformed-expected-json`, `match-clean`, `match-findings`, `match-permit-partial`, `match-permitted-only`, `missing-input`, `path-traversal`, `swapped-missing-extra`, `symlink-input`, `symlinked-frozen-dir-target`, `symlinked-inputs-dir`, `tampered-input-byte`, `unknown-class`, `unknown-key`, `unreachable-line`, `unpinned-entry`, `verdict-exit-label`, `verdict-extra-finding`, `verdict-missing-finding`, and `wrong-schema`.
- Round 19 roots:
  - `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-bashcvar/expected.json`
  - `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-helperfn/expected.json`
  - `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-vcs/expected.json`
  - `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-installers/expected.json`
  - `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-frozen-f1f2/expected.json`
  - `r19-frozen-f1f2` also contains `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-frozen-f1f2/<case>/expected.json` for: `f1-blank-after-valid`, `f1-blank-expected`, `f1-nonblank-control`, `f1-nonblank-note-control`, `f1-trailing-newline-past-end`, `f1-whitespace-expected`, `f2-realdir-dot`, and `f2-target`.
  - `r19-installers` also contains `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-installers/frozen-permit/expected.json`.

The final harm-watch receipt says all 11 roots passed, 247/247 cases, after eight reasoned round-19 case edits (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/evidence/harm/harm-watch-summary.txt:5-15,25`; `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md:1330`). This is a recorded prior run, not a run by me.

### Standalone frozen replay inputs (separate from the `--selftest` suite manifests)

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/frozen/expected.json` — SHA-256 `4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9`; also the frozen input for `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tw-recall.py`, pinned at `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/frozen/expected.json` — round-19 frozen replay; no digest is asserted here.

These are distinct from the round-18 tripwire selftest tree at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen/expected.json`.

### Frozen 175-case suite and pins

The scored suite is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/precision/expected.json` (schema `mado-tw-precision-suite-v1`, 175 cases; SHA-256 `1039c4fa6ede43b1f08cca231e6c713aa032722e4955f89dbd8b8f3de092254f`). Its 175 fixture files live beside it. The immutable suite pin is commit `f3da50488661509ce5d144c90f7780f8088e0903`, hard-coded as `SUITE_PIN` in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/tw-precision.py:18-22`; this commit first landed the suite, not a tool change. The current manifest itself has no `suite_pin` field: the counter enforces the source revision pin.

The 12-case held-out population is separate and not in the score: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/precision-heldout/expected.json`, SHA-256 `78b168b0db86502df23b6204a5a9a3e1f53189df5cf0257fef6c1d1214b3901a`.

Recorded scored results on the same suite pin:

| Measured tool revision | Recorded score | Tool SHA-256 |
|---|---:|---|
| `1f7f995caa25627db804e996cccd87fe38a3a1b6` | 29/175 | `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` |
| `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` | 110/175 | `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` |
| `28c68378eccbd5f227cdc28a62406ff390e3540a` | 172/175 | `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` |
| `3610e3ec76ab951043cbc41110d30f6f94a72ec2` | 172/175 | `f44904056a55896a5fb274b17bfc84b1c03f059ba745289f59acc702cdc411b1` |
| `a8960de655e6ea8c0a3bf74f5542041d9fe25b39` | 172/175 | `a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458` |

The final rerun table identifies expected-file and held-out hashes, exact commands, family scores, and exits at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/review/RerunAllV3.md:31-40`.

### Registered mismatches vs. later expectation review

The registered 175-case result remains **172/175**; the frozen expectations were not edited after measurement. Its three `pass:false` rows at `a8960de` are:

1. `W-CaseWrapperForms-class-method-instance`: expected clean, got exit 1 with `package_query/pacman:-Q/evidence:observed`. Round-20 decision records this as correct detection and a wrong expected value.
2. `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`: expected clean, got exit 1 with `vcs_write/jj:$c/evidence:observed`. The contract and later audit treat this as a correct conservative finding because an unbound `$c` may be an alias; the case lost its loop binding. This is the other stale want.
3. `L-AdoptW2-AdvHelperFn-b14`: expected exit 1 with `package_query/pacman:-Q/evidence:lead`, got exit 0/no findings. This is the remaining actual missed behavior.

The round-20 decisions say the W and H cases stay failing in the pinned suite, rather than changing the expectations after seeing output (`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-20.md:127-131`). The later disposition/audit gives the corrected semantic reading as 174/175 but retains the registered 172/175 unchanged (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/w2-dispositions.md:25-28`; `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/reports/AtkCasesH3.md:30-73`). Do not substitute 174/175 for the committed score or amend the three recorded mismatches.

The held-out command reproduced **2/12** at `a8960de` (H 2/3, S 0/3, W 0/6; ten expected rows did not match). It exits 0 as a counter report, but is a separate generalization warning and not part of the registered denominator (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/review/RerunAllV3.md:34`; `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/review/CriticAdmission.md:73-75`).

## Exact previously recorded final commands (reference only; not run here)

Set `ROOT` to an absolute path for an isolated clone containing commit `a8960de655e6ea8c0a3bf74f5542041d9fe25b39`; set `OUTDIR` to an absolute scratch directory outside the lane. The aggregate command below is the recorded final runner form; it verifies tool bytes against the requested revision, invokes the 11 direct suites and frozen replays, and writes receipts under `OUTDIR`:

```sh
ROOT=/absolute/path/to/isolated-clone
OUTDIR=/absolute/path/to/scratch/harm
REV=a8960de655e6ea8c0a3bf74f5542041d9fe25b39
ROOT="$ROOT" OUTDIR="$OUTDIR" bash "$ROOT/.ufo/waves/round-20/harm-watch.sh" "$REV"
```

The first 13 invocations below (11 `--selftest` suites and two `--frozen` replays) are performed by the aggregate runner. The final five are separate final checks listed in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/review/RerunAllV3.md:33-41`; `harm-watch.sh` itself includes the full-score precision and recall commands, but not held-out, recall-split, or A2 guards.

```sh
python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/.ufo/waves/round-17/tripwire/compound"
python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/.ufo/waves/round-17/tripwire/core"
python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/.ufo/waves/round-17/tripwire/hardening"
python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/.ufo/waves/round-17/tripwire/w2-regressions"
python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/.ufo/waves/round-18/tripwire/frozen"
python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/.ufo/waves/round-18/tripwire/r18-failsafe"
python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/.ufo/waves/round-19/tripwire/r19-bashcvar"
python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/.ufo/waves/round-19/tripwire/r19-frozen-f1f2"
python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/.ufo/waves/round-19/tripwire/r19-helperfn"
python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/.ufo/waves/round-19/tripwire/r19-installers"
python3 -I "$ROOT/tools/mado-tripwire.py" --selftest "$ROOT/.ufo/waves/round-19/tripwire/r19-vcs"
python3 -I "$ROOT/tools/mado-tripwire.py" --frozen "$ROOT/.ufo/waves/round-18/frozen"
python3 -I "$ROOT/tools/mado-tripwire.py" --frozen "$ROOT/.ufo/waves/round-19/frozen"
python3 -I "$ROOT/.ufo/waves/round-20/tw-precision.py" "$REV"
python3 -I "$ROOT/.ufo/waves/round-20/tw-precision.py" "$REV" --heldout
python3 -I "$ROOT/.ufo/waves/round-19/tw-recall.py" "$REV"
python3 -I "$ROOT/.ufo/waves/round-20/tw-recall-split.py" "$REV"
python3 -I "$ROOT/.ufo/waves/round-20/a2/a2-guards.py" "$REV" --fixtures-rev 6a7d9ca0d2124a4077074b800c94a9bc1184441c
```

The historical exact per-check commands are recorded in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/review/RerunAllV3.md:33-41`; the aggregate 21-command result is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/evidence/harm/harm-watch-summary.txt:25-36`. Aggregate summary: 20 OK, 1 accepted baseline result, 0 failures, 0 skips; 11/11 selftests.

## Expected baseline failure and unrun/noncanonical inputs

- Expected baseline result: round-18 `--frozen` reports exit 1 / `MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch`; `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/harm-watch.sh` deliberately classifies it as `BASELINE`, not a failing check. Round-19 `--frozen` is an ordinary exit-0 `frozen_match`.
- The final runner reports no direct round-20 `tripwire` suite root (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/evidence/harm/harm-watch-summary.txt:16`) and no round-20 frozen baseline (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/evidence/harm/harm-watch-summary.txt:19`). This does **not** mean the precision suite was skipped: it is an independent command, and its 175-case result is present.
- Noncanonical inputs not in those 11 roots: three draft manifests at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/drafts/tripwire/r18-installers/expected.json`, `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/drafts/tripwire/r18-helperfn/expected.json`, and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/drafts/tripwire/r18-bashcvar/expected.json`; plus `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/patches/TwVcsHelp-dev-cases/expected.json`. These are not counted among the final runner's 11 selftests; no final-run status is claimed for them.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/precision/expected.json` and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/precision-heldout/expected.json` are the canonical round-20 manifests; the separate wave-1 authoring cases under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/` are not replacements for either pinned scoring manifest.

## Limits

This is a read-only inventory from committed repository artifacts and existing receipts. No suite, gate, fixture, snippet, or command was run. `xd://lsp` is not mounted in this session (`No such tool`); grep was used only for literal locating, not semantic proof. Behavioral disposition above is attributed to the cited committed round-20 decisions and audits. No production files or unrelated paths were changed.

## Installs

None.
