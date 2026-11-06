# R91MExecD1 — routed defect D1: `--selftest` for the receipt-presence check

Round 91, wave w1, executor seat R91MExecD1. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base revision
`cc0381db585cc44c3dfc13ced807409c32c45bb0` (master). Scratch
`/fast/scratch/hyaku/mado-r91/R91MExecD1`, deleted on exit (verified below).

## 1. Files

| path | sha256 | role |
|---|---|---|
| `.ufo/waves/round-91/build/check-receipt-presence.d1.py` | `38a2ea60dc698c45957a3ad4af3132297dd2edb354d815e7ff3433c42bab47ca` | **written** — copy of the check plus `--selftest` |
| `.ufo/waves/round-91/w1/R91MExecD1.md` | — | **written** — this report |
| `quality/check-receipt-presence.py` | `04b8be60415f2e505f6a1414099402203eb3a1fd17b21542c3afdd24b38a1d6c` | read only, **unmodified** |

Nothing else in the lane was written; `git status --porcelain` still shows only the
pre-existing untracked `.ufo/waves/round-91/`,
`quality/counters/c1-r91-mime-resolution.py`,
`quality/counters/c2-r91-seat-reports.py`.

## 2. What the copy adds

`diff -u quality/check-receipt-presence.py .ufo/waves/round-91/build/check-receipt-presence.d1.py`:
**78 added lines, 0 removed, 0 modified** — every existing line is byte-identical.
The additions are only:

- `import shutil` (line 57), `import tempfile` (line 60);
- `def selftest() -> int:` (line 122, body 122–200);
- the argparse flag `--selftest` with its two-line help (lines 211–212) and the dispatch
  `if a.selftest: return selftest()` (lines 214–215).

The module docstring is untouched, so `--help`'s short description is unchanged; the flag's
own help text documents it. No non-selftest code path was touched (proved by §5 as well).

### Fixture and cases

`selftest()` makes one throwaway repository under `tempfile.mkdtemp()` (honours `TMPDIR`),
runs `git -C "$D" init -q`, then asserts `git -C "$D" rev-parse --show-toplevel` equals `$D`
before the first commit. Every git call names `-C "$D"`; the fixture identity is passed per
command as `-c user.name=fixture -c user.email=fixture@invalid -c commit.gpgsign=false` and is
never written to any config (children get `HOME=<temp>` and `GIT_CONFIG_NOSYSTEM=1`).
The check itself runs as a subprocess `sys.executable -I <file> …`, i.e. exactly as a counter
drives it.

Three commits, each diffed with `-U0` so the added line is the only citation:

| commit | fixture content | case | expected |
|---|---|---|---|
| `base` | `SCORECARD.md` = `base` | — | — |
| `round-91: ok` | `quality/receipts/ok-r91.txt` added; `SCORECARD.md:2` = `ok cites quality/receipts/ok-r91.txt` | **OK** | rc 0, summary contains `cited=1 present=1 missing=0 verdict=OK` |
| `round-91: missing` | `SCORECARD.md:3` = `gone cites .ufo/waves/round-91/receipts/gone-r91.txt` | **MISSING** | rc 1 and the exact line `missing .ufo/waves/round-91/receipts/gone-r91.txt -> .ufo/waves/round-91/receipts/gone-r91.txt SCORECARD.md:3`, summary contains `verdict=MISSING` |
| — | `--rev dddddddd…` (40 d's, no such commit) | **SETUP** | rc 2 and the exact line `RECEIPT_PRESENCE: SETUP_ERROR bad --rev dddddddddddddddddddddddddddddddddddddddd` |

Each case asserts rc *and* its finding line → `checks=6` (2 per case). Any failed assertion
prints `RECEIPT_PRESENCE_SELFTEST: FAIL <case> …`; the run ends with
`RECEIPT_PRESENCE_SELFTEST: checks=N failed=F` and exits 1 iff `failed>0`. Fixture setup
errors are caught (`OSError`/`RuntimeError`), counted as a failure, and the temp tree is
removed in `finally`.

## 3. Selftest evidence (commands and exit codes)

All four runs use the copy at
`.ufo/waves/round-91/build/check-receipt-presence.d1.py`:

```
$ TMPDIR=/fast/scratch/hyaku/mado-r91/R91MExecD1 python3 -I .ufo/waves/round-91/build/check-receipt-presence.d1.py --selftest
RECEIPT_PRESENCE_SELFTEST: checks=6 failed=0
rc=0

$ env GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=diff.mnemonicPrefix GIT_CONFIG_VALUE_0=true \
      GIT_CONFIG_KEY_1=diff.noprefix GIT_CONFIG_VALUE_1=true TMPDIR=… python3 -I … --selftest
RECEIPT_PRESENCE_SELFTEST: checks=6 failed=0
rc=0

$ env -i PATH=/usr/bin LC_ALL=C TMPDIR=… python3 -I … --selftest
RECEIPT_PRESENCE_SELFTEST: checks=6 failed=0
rc=0

$ python3 -I quality/check-receipt-presence.py --selftest        # the untouched original
check-receipt-presence.py: error: unrecognized arguments: --selftest
rc=2
```

The last run confirms the flag does not exist in the original (the copy is the only file that
gained it). The `env -i` and hostile-config runs show the selftest does not depend on the
caller's environment or git configuration.

## 4. The selftest can fail (three mutants)

Mutants are written under the seat scratch by a one-shot script that asserts each `find`
occurs exactly once, then run as
`python3 -I <mutant> --selftest`. All three exit **1**.

| id | find → replace (single occurrence each) | mutant `--selftest` output | rc |
|---|---|---|---|
| A | `                    missing += 1` → `                    present_n += 1` (missing citations ignored) | `FAIL MISSING rc=0 want=1 …` + `FAIL MISSING absent=['verdict=MISSING'] …`; `checks=6 failed=2` | **1** |
| B | `    return 0 if missing == 0 else 1` → `    return 0` (rc 1 → 0) | `FAIL MISSING rc=0 want=1 out=[… verdict=MISSING]`; `checks=6 failed=1` | **1** |
| C | `        print(f"RECEIPT_PRESENCE: SETUP_ERROR {msg}")\n        return 2` → `…\n        return 1` (setup error → rc 1) | `FAIL SETUP rc=1 want=2 out=['RECEIPT_PRESENCE: SETUP_ERROR bad --rev ddd…']`; `checks=6 failed=1` | **1** |

Verbatim mutant A output:

```
RECEIPT_PRESENCE_SELFTEST: FAIL MISSING rc=0 want=1 out=['missing .ufo/waves/round-91/receipts/gone-r91.txt -> .ufo/waves/round-91/receipts/gone-r91.txt SCORECARD.md:3', 'RECEIPT_PRESENCE: mode=rev rev=2cb24bc2… records=1 cited=1 present=1 missing=0 verdict=OK']
RECEIPT_PRESENCE_SELFTEST: FAIL MISSING absent=['verdict=MISSING'] out=[…]
RECEIPT_PRESENCE_SELFTEST: checks=6 failed=2
rc=1
```

A is instructive: with the missing branch counting as present the finding line is still printed
(the `print` is a separate statement) but the verdict flips to OK and rc to 0 — caught by both
the rc assertion and the `verdict=MISSING` assertion, which is why the MISSING case asserts
both.

## 5. Round-90 counter still passes against the copy (DRAFT)

Frozen round-90 predicate, **draft run** (`--draft-check`, never a measurement; exit 3 by
design, no receipt written):

```
$ python3 -I quality/counters/c2-r90-receipt-presence.py --repo . \
    --rev 51bf076fd970106da854e11873b886528c3cffaf \
    --base-rev 5041acf99e27263872bf0441ad5f9d4316152605 \
    --set .ufo/waves/round-90/controls/receipt-presence-set-r90.json \
    --mutants .ufo/waves/round-90/controls/receipt-mutants-r90.json \
    --expect-set-sha256 f7ab86c25edbb806a9f947af09fab5cf971a42602c252966c0075b9aeefa7939 \
    --expect-mutants-sha256 68b39a805755f7685c00c847a48b0f8f679fdca2710773efb5f4469b7bebe82d \
    --scratch-root <scratch>/c2r90 \
    --draft-check .ufo/waves/round-91/build/check-receipt-presence.d1.py
MADO_RECEIPT_PRESENCE: DRAFT_TARGET_MET rev=draft:.ufo/waves/round-91/build/check-receipt-presence.d1.py \
  expectations=83 met=83 defects_detected=4/4 population=38 mutants=28 killed=28 base_check=absent \
  base_met=0 do_nothing_met=44 smart_always_ok_met=46 always_missing_met=0 \
  check_sha256=38a2ea60dc698c45957a3ad4af3132297dd2edb354d815e7ff3433c42bab47ca
rc=3        (draft exit by design; the whole run finished in under a minute)
```

Every frozen number equals the recorded round-90 measurement
(`.ufo/waves/round-90/receipts/c2-measured-r90.txt`:
`expectations=83 met=83 … population=38 mutants=28 killed=28 … do_nothing_met=44
smart_always_ok_met=46 always_missing_met=0`, original `check_sha256=04b8be60…`) — only
`check_sha256` differs, as it must. That run covers 6 lane revisions and 35 worktree fixtures
under a clean *and* a `diff.mnemonicPrefix=true diff.noprefix=true` environment, plus the
38-commit population, 28 mutants and 4 controls. I also verified the 28 frozen mutant `find`
strings each still occur exactly once in the copy (`collisions=0`), so the selftest additions
neither shadow nor break a frozen mutant.

## 6. Byte-for-byte behavioural equivalence at the two revs

Identical argv, clean env (`env -i PATH=/usr/bin HOME=/nonexistent LC_ALL=C
GIT_CONFIG_NOSYSTEM=1`), original vs copy:

| rev | original | copy | `diff` of stdout |
|---|---|---|---|
| `498855cb` | rc **1** | rc **1** | `diff -u` rc **0** (identical) |
| `51bf076f` | rc **1** | rc **1** | `diff -u` rc **0** (identical) |

Outputs (both files identical):

```
missing receipts/harm-final-r88.txt -> .ufo/waves/round-88/receipts/harm-final-r88.txt SCORECARD.md:5140
RECEIPT_PRESENCE: mode=rev rev=498855cb327cd4e3debfa9446ea38398c216dda1 records=6 cited=11 present=10 missing=1 verdict=MISSING
```
```
missing receipts/harm-final-r89.txt -> .ufo/waves/round-89/receipts/harm-final-r89.txt SCORECARD.md:5179
missing receipts/census-end-r89.txt -> .ufo/waves/round-89/receipts/census-end-r89.txt corpus/lessons/round-89.md:144
RECEIPT_PRESENCE: mode=rev rev=51bf076fd970106da854e11873b886528c3cffaf records=6 cited=13 present=11 missing=2 verdict=MISSING
```

These are exactly the two frozen `D88`/`D89` defect revisions of the round-90 set, so the
comparison is against the same inputs the frozen predicate uses.

## 7. Risks and limits

- The selftest covers only the `--rev` mode with full `quality/…`/`.ufo/.../receipts/…` paths:
  no `--worktree`, glob or brace case. That is the assigned scope; those paths are covered by
  the frozen round-90 fixtures (§5) rather than by the selftest.
- The MISSING expectation pins `SCORECARD.md:3`; the fixture's line numbering is fixed by the
  three commits, so the assertion is stable but any change to the fixture order must update it.
- `selftest()` inherits nothing: it builds its own child env, so a caller's git config cannot
  mask a regression — verified by the hostile-config and `env -i` runs (§3).
- One fixture repository per run; total runtime is a fraction of a second, no network.

## 8. Dead steps, installs, scratch

- Dead steps: none.
- Installs: none (no tool was needed; `pacman` untouched).
- Scratch `/fast/scratch/hyaku/mado-r91/R91MExecD1` was removed after the runs; the
  reproduction is fully specified in §2–§6 (mutant `find`→`replace` pairs are quoted verbatim).
