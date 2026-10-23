# C2 — capability table vs frozen re-demonstration (round 24, mado-shokunin)

MISMATCH: a capability named in a SCORECARD.md capability table at REV whose self-assessed status (its row in a `Capability status (round 24 re-demonstration)` table at REV if present, else `works`) differs from the observed status of its frozen manifest command run on the REV tree; a manifest capability absent from REV's capability tables also counts as MISMATCH.

## Usage

    python3 -I .ufo/waves/round-24/c2/count.py REV [--json] [--keep]

- REV is resolved to a full commit and archived (`git -C MADO_LANE archive REV | tar -x`) into a fresh mkdtemp under /fast/scratch/hyaku/mado-r24/c2/; the tree is deleted on exit unless --keep.
- MADO_LANE (default /home/vgpnk/Projects/shokunin/mado-shokunin) is the read-only repo behind {LANE} and the git-reading counters; {TREE} is the extracted tree, {FLEET} the fleet root, {CENSUS_ROOT} a scratch root holding `mado-shokunin -> {TREE}` plus a scratch shokunin.conf.
- Text mode prints one line per capability: `name stated=.. observed=.. OK|MISMATCH exit=n`, then `mismatches=k/population revision=.. manifest_sha256=.. counter_sha256=..`. --json prints the same record as one object (argv/cwd/reason included).
- Exit: 0 k==0 · 1 k>0 · 2 setup error (usage, unreadable manifest/SCORECARD, bad REV, extraction).

## Frozen rules

Each manifest row has argv/cwd/env (placeholders above), timeout_s <= 600, exit_ok, regex (re.MULTILINE; inline (?s) allowed), optional min_matches, regex_all, forbid_regex, requires (TREE-relative; missing => observed=fails, exit 125), and why.

Observed is `works` iff exit_ok and every regex condition holds; a timeout SIGKILLs the child group and reads fails/exit 124. Identical argv/cwd/env/timeout run once per invocation (the two a2-guards rows share a run).

Population = names of every data row of every markdown table under a heading matching `^#{2,3} Capabilities` (header, separator and `— none yet —` skipped; first name wins), union the manifest names. Stated = the row in a `Capability status (round 24 re-demonstration)` table (last row wins) else `works`. A manifest capability absent from REV's tables, or a REV capability with no manifest command, is MISMATCH.

## Why the unusual rows

- git-reading counters (tw-precision.py, a2-guards.py) derive their repo root from their own path and call `git show`, so they run with cwd {LANE} while `requires` pins their presence at REV; their revision argument is {REV}.
- `bash tools/mado-verify.sh --no-live` replaces the live pointer with the read-only form; a verdict line (CLEAN or DIVERGED, exit 0/1) is the claim, host cleanliness is not.
- `landed-check.sh LANE HASH` keeps its three-way answer (LANDED/LOCAL_ONLY/MISSING); it is network-dependent by its own ls-remote contract.
- The r17 tripwire pointer is brace shorthand but the CLI accepts one --selftest DIR, so the frozen command runs the four dirs in sequence.
- The r20 detector row's pointer is evidence files only; its producing script exists at REV, so the row is re-demonstrated by running a2-guards.py.

## Smoke

`smoke/base-8e5d9369.txt` records the exact command, stdout and exit at base 8e5d9369. SCORECARD.md was not edited.

## Pre-freeze fixes

No manifest invocation error surfaced before the smoke, and no manifest rule or threshold changed after it. Pre-smoke count.py fixes were internal only (placeholder substitution in regex evaluation, strict manifest validation, section-end cleanup); they changed no rule.
