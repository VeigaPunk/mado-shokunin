# RevQuality29 — partly falsified: criterion 29 holds against honest harnesses, but the checker leaks its control env and is maskable — a fail-open harness reads green

Scope: criterion 29 (`corpus/QUALITY.md:232` and its runnable check `.ufo/waves/round-20/isolation-check.sh`, sha256 `2bf115db…` at `a4046a8`). Attack surfaces named: restatement of 1–28, red real/reproducible, check able to fail, limits honest.

All runs in `/tmp/mado-r20w2-RevQuality29` (clone of the lane, `remote remove origin`, HEAD `a4046a8216080d4004de3f268c62cf142095ac07`). Lane files not modified. No real mounts/unshare probes against host resources beyond the check's own `/tmp` userns bind mounts; all canaries under `/tmp`.

## Restatement: not a restatement

Grepped criteria 1–28 (`corpus/QUALITY.md:3-228`) for `isolat|harness|fail.?clos|fail.?open|sandbox|namespace|unshare|bind`: the only hits are inside the round-18/19 appendices discussing *evidence binding*, not harness gating. Criterion 25 (instrument biting) governs mutants of *checkers*; 29 governs the *subject harness's* behavior under forced setup failure. Distinct obligation, distinct check. Not a restatement.

## Red: real and reproducible — with one already-known footnote

`git ls-files -s` shows `.ufo/waves/round-20/evidence/inns-r19-shape.sh` committed **100644**; a bare `bash isolation-check.sh .ufo/…/inns-r19-shape.sh` in a fresh checkout returns `COULD_NOT_EVALUATE (not executable)` exit 2. After `chmod +x` (matching the original capture), the run reproduces `crit29-inns-r19-shape.txt` exactly: FAIL_OPEN in mount-nonzero, mount-noop, partial-arm, missing-target, missing-stub; FAIL_CLOSED in unshare-refused; `POSITIVE_CONTROL_OK`; exit 1. The missing-stub transcript (real `mount` fails on the absent stub inside the non-final `&&` member, payload still writes the canary) is a live demonstration that `set -e` + non-final `&&` member is not a gate — the criterion's core claim. (The exec-bit gap is also noted by sibling MutIsolationCheck; not counted here as new.) The round-19 pedigree is real: `corpus/lessons/round-19-verifier-spotcheck.md:124` records SentinelGatePath's `inns.sh` running a real `hyprctl probe` through exactly this shape.

## Green and mutants: check can fail

`isolate.sh`: FAIL_CLOSED in all six modes + `POSITIVE_CONTROL_OK`, exit 0 — reproduces `crit29-isolate.txt`. All four committed mutants (`isolation-mutants/m{1-nocmp,3b-capprobe,4-skiptarget,6-besteffort}.sh`, each 100755) read FAIL_OPEN in exactly the mode they break and exit 1 (verified `m1-nocmp.sh` → `mutant exit=1`). The `SKIP_AS_SUCCESS` branch (exit 0, canary absent → FAIL_OPEN) is exercised: `unshare-refused` on the red fixture exits 1 → FAIL_CLOSED, while mount-nonzero exits 0 → FAIL_OPEN, so both polarities of the verdict logic are live. **The check is able to fail.**

## FALSIFIED: the checker leaks its control environment — a fail-open harness masks and reads green

`isolation-check.sh` invokes the harness as

```
PATH="$run_path" CHECK_MODE="$mode" CHECK_MARKER="$marker" CHECK_REAL_PATH="$original_path" "$harness" ...
```

`CHECK_MODE`, `CHECK_MARKER`, `CHECK_REAL_PATH` reach the *harness* (they must — the PATH stubs need them — but nothing limits them to the stubs). Counterexample `masked.sh` (sha256 `890df50ebbe2aebecbd47fee69967e1098667af3420300b571eea393b0863126`, built in `/tmp/mado-r20w2-RevQuality29/w2-evil/`): identical code path in production and under test except `masked=${CHECK_MODE:+yes}` gates the mount-failure abort and the post-mount `cmp`. Production run with an absent stub: `mount` fails, harness ignores it, `exec` runs the payload — `harness exit=0`, canary `payload-ran` present: **fail-open**. Under the checker:

```
FAIL_CLOSED masked.sh mode=mount-nonzero      … (all six)
POSITIVE_CONTROL_OK masked.sh
CHECK_EXIT=0
```

A genuinely fail-open harness scores the criterion's green verdict. This is not a hypothetical "harness could detect the test" limit — the test hands the harness a literal `CHECK_MODE` flag.

Second spoof of the same family, `canary-deleter3.sh` (sha256 `87cb3526ae27fd4daaeeea9a2dbf2cb00a9f3891676823bf95cc74777f16e9b5`): always `exec`s the payload (fail-open), then when `CHECK_MODE` is set copies the canary to `/tmp/payload-proof-<mode>.txt` and deletes it. Checker reads `FAIL_CLOSED` in all six + `POSITIVE_CONTROL_OK`, exit 0, while `/tmp/payload-proof-mount-nonzero.txt` contains `payload-ran` — direct proof the payload ran under forced failure during a green verdict. The converse proxy error also exists (harness touching the canary without running the payload → FAIL_OPEN for a closed harness), same root cause: **canary-existence is the sole observable of payload execution**.

## Impacted axes

- **Check integrity / criterion 25 bite**: the checker discriminates honest harnesses (red fixture + 4 mutants all correctly read), but does not discriminate a deliberately masking harness. Criterion-29 green for any *adversarially authored* harness is not evidence of fail-closure. For `isolate.sh` itself (in-repo, non-adversarial, reads green and is honest) the verdict stands.
- **Limits honesty**: the stated limit ("absolute-path mount/unshare → `COULD_NOT_EVALUATE`, never a pass") is verified (`abspath.sh`, a correctly fail-closed absolute-path harness, sha256 `e764bc3e5…`: COULD_NOT_EVALUATE in all four injection modes, exit 2 — including exit-2-not-1 aggregation via `overall_unknown`). But the limit list is incomplete: it omits (a) the control-env leak/masking channel, (b) the canary proxy's two-sided error, (c) non-PATH resolution generally (ctypes/syscall harness → same COULD_NOT_EVALUATE; fine in outcome, broader than "absolute path" wording).
- **"not a sandbox" limit**: honest — `isolate.sh` contains no `env`, no PATH scrub (grep `env|PATH` hits only usage text); env and sockets pass through. Holds.
- **Red reproducibility**: real, but needs `chmod +x` on the 100644 fixture before the named command produces the receipt's outcome (sibling MutIsolationCheck documents the same).
- **Scope note**: no setup-rollback check — partial-arm only requires that the payload not start; a harness leaving t1 bound after t2 fails reads FAIL_CLOSED. Consistent with the criterion's text ("aborts before the payload starts"), worth a footnote, not a defect of the criterion as written.

## Smallest safe correction

1. Stop exporting control vars to the harness: bake `CHECK_MODE`/`CHECK_MARKER`/`CHECK_REAL_PATH` into the generated stub sources at `cat > "$case_bin/mount"` time (heredoc without quotes on the values, or pass them as stub argv via a wrapper), so the harness env carries only the PATH prefix. This removes the documented-evasion channel; a harness can still *detect* stubbed `mount` behaviorally (inherent to black-box testing) — say so in the Limit line.
2. Add to the Limit: "the verdict observes only that the canary was written/not written; a harness that writes or deletes the canary without running the payload is outside the model; green certifies behavior under this check's stubs, not arbitrary harnesses."
3. Add exec bit (or a `chmod`/`bash`-prefix note) for `inns-r19-shape.sh` so the named command reproduces without repair.

## Limits

- Spoofs require a harness written to evade; no claim that `isolate.sh` or any committed harness does so. `isolate.sh`'s green is credible.
- I did not test rollback/teardown, directory targets, or harnesses in other languages beyond the absolute-path bash case.
- `masked.sh`/`canary-deleter3.sh`/`abspath.sh` live only under `/tmp/mado-r20w2-RevQuality29/w2-evil/` (provenance per criterion 13); sha256s above.

## Installs

none.
