# ExecCheckM235 — receipt-provenance gate for r23 lesson M23-5 (round 24, wave 1)

Item: routed r23 defect 3. Lesson M23-5 records that L1's scratch attack run wrote probe results
through a path that did not resolve where it later read them, so it read stale files left by an
earlier tool and briefly reported regressions absent from the measured bytes; the recorded repair is
absolute result paths, results deleted before each run, and the measured tool's sha256 printed.

Deliverable: a gate that makes that repair checkable instead of prose.

## Files written (all under the lane; nothing else touched)

| Path | sha256 | Role |
|---|---|---|
| `.ufo/waves/round-24/quality/check-receipt-provenance.py` | `sha256:5b463510893fea56276fb377a23dcc90935f8b4baef0e307f6b6e35ea0e585f9` | the gate |
| `.ufo/waves/round-24/quality/fixtures/l1-attacks-green.sh` | `sha256:076a41ed6d9bb926c5dd3a3a53349a5096191b1158ee4614f66497aa691012ef` | corrected green artifact |
| `.ufo/waves/round-24/quality/red/r23-l1-attacks-first.sh` | `sha256:599a92da90695f0e4faa9fb764940af751d9b845206a31279b0a9cc00bb7425d` | real r23 red bytes |
| `.ufo/waves/round-24/quality/m23-5-red-green.txt` | `sha256:51c75e50bd211fd1fe4d0d2a09254186c738206ffc3ebc05d4b7ecfff9e22f61` | red/green receipt (commands, exact output, exit codes) |

## What the gate checks

`python3 -I check-receipt-provenance.py [--json] [--notes] RECEIPT...` exits 0 iff every receipt
passes both rules; otherwise it prints one `FAIL <receipt>:<line>: R<n> <reason>` per violation and
exits 1 (`verdict=fail reasons=<n>`).

- **R1 tool identity** — the receipt states the measured tool by `sha256:` plus 64 hex digits, or by a
  full 64-hex sha256, on a line that also names the tool (`--tool` value, a `*/tools/*` path, or a
  `*tool*.py`/`*tool*.sh` filename). A truncated digest never counts; a `sha256sum` call that pins
  nothing is reported with its line number.
- **R2 absolute result paths** — every result/data path the receipt writes or reads must be absolute:
  a literal starting with `/`, or a `$VAR`/`${VAR}` whose assignment in the same receipt is an
  absolute literal. Positions: shell redirections, `--out`/`-o`/`--result`/`--receipt`/`--write`,
  `cat`, Python `open(`/`Path(...).read_text|write_text`, and path-like positional arguments to the
  measurement harnesses (`probe.py`, `run.py`, `measure.py`, `deliver.py`, `drive.py`, `gen.py`,
  `tabulate.py`, `mkprobes*.py`, `mkfinal.py`). Staging commands (`cd`, `mkdir`, `cp`, `rm`,
  `git clone`) print only under `--notes` and never fail the gate.

The gate is text-only and deterministic; it never executes the receipt and writes nothing. Stated
boundaries: runtime-built paths are judged by their literal prefix; `cd` is not simulated (the
risky relative data paths fail on their own); and the gate proves the digest is *stated*, not that
it equals the tool's bytes — pairing it with `sha256sum` at run time stays the receipt's job.

## Evidence

Full captured output: `.ufo/waves/round-24/quality/m23-5-red-green.txt`. Summarised:

1. **Self-test** (`--selftest`), 8-case mutant matrix, `selftest=pass cases=8 mismatches=0`,
   exit 0: green sample passes; no-digest, relative-result, relative-variable, tilde-result,
   truncated-digest and unbound-digest mutants each fail; a bare full digest bound to a tool passes.
2. **RED**, real r23 artifact, exit 1, `verdict=fail reasons=5`:
   - R1: no `sha256:`<64hex> / full sha256; `sha256sum` at line 9 computes one at run time and the
     receipt never states it.
   - R2: relative `probes` (:18), `probes2` (:19), `../fixtures` (:20), and `$c.json` (:31, loop
     variable not pinned to an absolute value).
3. **GREEN**, corrected fixture, exit 0, `verdict=pass reasons=0`: digest pinned as
   `sha256:cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` on the measured-tool
   line, every result and data path absolute, result files removed before the run, and the pin
   re-checked with `sha256sum` at run time.

## Red artifact provenance — observation, then what it does not establish

- `git log --oneline --follow -- .ufo/waves/round-23/w1/out/L1/l1-attacks.sh` returns exactly two
  commits: `03227dd` (adds the file) and `3df1062` (withdraw).
- `git log -p --follow` shows the only change between them is `|| true` appended to the clone's
  `git commit` (blob `602ecd7` → `16610d4`).
- **Observation:** the pre-fix working-tree bytes the lesson names are not in git, so the exact
  relative-write line cannot be replayed from history. The red artifact is the first committed
  revision (`git cat-file -p 602ecd7`), which is the closest real artifact and still carries the
  shape's ingredients: probe data read through relative names (`probes`, `probes2`, `../fixtures`,
  `$c.json`) around a `cd` that changes cwd mid-receipt, while result files live under one hard-coded
  absolute scratch root.
- **Observation, diagnostic:** the later committed revision (the file as it stands in the lane) fails
  the gate with the same 5 reasons. The committed fix moved the *result* files to absolute paths but
  left the fixture/case reads relative and never states the digest, so the M23-5 repair as committed
  is not checkable by the receipt it leaves behind.
- **Inference, labelled:** a write through the relative branch of that shape resolving into the
  clone's `discovery/` directory while the read used `$D/../…` would reproduce the recorded stale
  read. The missing draft is not available, so this is inference from the surviving reads, not proof.
- **Not established [UNK]:** whether the stale read actually occurred in the lost draft; the host's
  behaviour is untouched and unmeasured here; the gate does not verify digest equality or run any
  receipt.

## Commands run (read-only; no installs, no git/jj writes, no host state changes)

```
python3 -I .ufo/waves/round-24/quality/check-receipt-provenance.py --selftest
python3 -I .ufo/waves/round-24/quality/check-receipt-provenance.py .ufo/waves/round-24/quality/red/r23-l1-attacks-first.sh
python3 -I .ufo/waves/round-24/quality/check-receipt-provenance.py .ufo/waves/round-24/quality/fixtures/l1-attacks-green.sh
git cat-file -p 602ecd7 > .ufo/waves/round-24/quality/red/r23-l1-attacks-first.sh
git log --oneline --follow -- .ufo/waves/round-23/w1/out/L1/l1-attacks.sh
git log -p --follow -- .ufo/waves/round-23/w1/out/L1/l1-attacks.sh
```

No subagents were spawned, no model parameter was passed, and no packages were installed.

## Verdict

Gate built and able to fail: exit 1 on the real r23 artifact (R1 unpinned digest; R2 relative
`probes`, `probes2`, `../fixtures`, `$c.json`) and exit 0 on the corrected green fixture; the 8-case
self-test holds. Residual reported, not hidden: the lane's committed revision of the same script also
fails the gate for the same reasons.
