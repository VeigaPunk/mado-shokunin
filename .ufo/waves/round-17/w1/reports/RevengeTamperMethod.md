# RevengeTamperMethod — how r16 produced `frozen-tampered.json`, and what `--frozen` checks first

Seat: `MadoR17.RevengeTamperMethod` (revenger, leaf). Target root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Baseline lane HEAD for this read:
`0175f13` (worktree clean for tracked files; round-17 wave files untracked).

Method: file-byte and git-object reading only. No gate, selftest, fixture,
measurement, test, lint or build was executed; no `pacman`/`sudo`/`systemctl`/
`hyprctl`/live probe; no tool installed. Every behavioural statement about the
gate below is **[INFERENCE]** from source, except the receipt fields, which are
observed committed JSON. `git show` was used read-only; no `jj`, no commit.

## 1. Axes

- **A1 provenance** — reconstruct who/when/how the receipt was produced from
  committed artifacts alone.
- **A2 ordering semantics** — establish what `--frozen` evaluates before the
  plan/policy digests, and before any verdict.
- **A3 defect localization** — explain the observed `frozen_error` precisely,
  not plausibly.
- **A4 discriminator** — specify the minimal tamper that isolates the digest
  check at current content, and what each alternative outcome would prove.
- **A5 non-execution honesty** — separate receipt observation from source
  inference, and name what is unrecoverable.

## 2. The receipt as committed

`.ufo/waves/round-16/evidence/frozen-tampered.json` (committed in `1e31681`,
the only commit that touches it; `git log --all --` returns just that commit):

| Field | Value |
|---|---|
| `measured_commit` | `9dcf248993a9622a5b016edec0003187141745d2` |
| `action_gate_sha256` | `13d86fb0b34c21bccde0a8314875d66deb287624a9d971e4f4ed287496dcdb73` |
| `command` | `["python3","-I","/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-action-plan.py","--frozen","/tmp/mado-r16-frozen-tamper-pt60l_e_"]` |
| `exit` / `expected_exit` / `matched_exit` | `2` / `2` / `true` |
| `stdout` | `MADO_PLAN: frozen_error` + `{"detail": "expected.json pair 1/'denied_executable:sudo' is unreachable", "exit": 2, "finding": "frozen_error", ...}` |

Digest binding checks (observed): `git show 9dcf248:tools/mado-action-plan.py |
sha256sum` = `13d86fb0…dcdb73`, exactly the receipt's `action_gate_sha256`; the
current `tools/mado-action-plan.py` hashes to `226220ae…ba5aea3` = the
`1e31681` blob = `committed-bindings.json`. So the receipt really was measured
against the pre-fix gate, and its recorded executable digest is honest.

## 3. How round 16 produced it

What the artifacts support:

1. L1 was at `9dcf248` (old gate, sha `13d86fb0…`).
2. A temporary directory `/tmp/mado-r16-frozen-tamper-pt60l_e_` was created as
   a copy of `.ufo/waves/round-16/frozen` with one input altered. This is the
   later L1 restatement in the round-17 dispatch: "its command used a /tmp copy
   of …/frozen with one input altered". The 8-character `[a-z0-9_]` suffix
   matches a `tempfile.mkdtemp(prefix="mado-r16-frozen-tamper-")`-style name
   rather than a hand path. **[INFERENCE]**
3. The gate was invoked exactly as recorded, with `python3 -I`.
4. The wrapper recorded `expected_exit: 2` and `matched_exit: true`, then the
   receipt was committed with the fix in `1e31681`.

What is **not** recoverable from lane records:

- **Which file was altered, at which byte, from what to what.** The receipt has
  no `tamper`/`mutation`/pre-run-digest field. No generator script for the
  receipts exists under `.ufo/waves/round-16` (only `measure.py` is present);
  no LOG entry names the mutation (`grep -n tamper LOG.md` → no match).
- The temp directory itself: `ls -la /tmp/mado-r16-frozen-tamper-pt60l_e_`
  → `No such file or directory` (observed). Nothing was preserved for audit.

Consequence: even if the verdict had been right, the control would not be
reproducible from the receipt. The round-17 recut should record the mutation
description and pre/post SHA-256 of the mutated file; the round-16 receipt
records neither.

## 4. Why the `9dcf248` receipt showed `frozen_error`

The pre-fix pair validator (`git show 9dcf248:tools/mado-action-plan.py`,
`run_frozen` lines 447–462) stored namespace prefixes **with a trailing colon**
and then appended another colon in the membership test:

```python
valid_pairs = {
    0: ("plan_safe",),
    1: ("blocked_action_kind:", "denied_executable:",
        "unknown_action_kind", "empty_argv"),
    2: ("plan_malformed", "policy_malformed"),
}
allowed = valid_pairs.get(want_exit)
ok_pair = allowed is not None and any(
    want_finding == a or want_finding.startswith(a + ":")
    for a in allowed)
```

For the committed expectation `denied_executable:sudo`/1:

- `want_finding == "denied_executable:"` → false;
- `want_finding.startswith("denied_executable::")` → false (double colon).

So **every** namespaced exit-1 finding — `denied_executable:*` and
`blocked_action_kind:*` — was rejected as "unreachable". Exactly two symptoms
follow, both observed:

- `action-selftest.json` at `9dcf248`: `frozen-denied-match` (expects
  `blocked_action_kind:package-install`/1) FAILs with `2/frozen_error`, while
  `frozen-tampered-plan` and `frozen-tampered-policy` PASS (their pair is the
  non-namespaced `plan_safe`/0). Summary `51/52`.
- `action-frozen.json` at `9dcf248`: the intact committed snapshot expects
  `denied_executable:sudo`/1 → `2 frozen_error`.

The fix (`1e31681`) replaced the prefix scan with an exact pair set built from
`PINNED_PAUSED_SCOPE` and `PINNED_DENY_EXECUTABLES` (current lines 447–455).
Current `52/52` and `frozen_match` receipts follow.

### The tamper was never exercised

The pair check is **before** the plan/policy digest loop. Therefore, at
`9dcf248`, the gate exited from `expected.json` alone. The decisive observation
is that the untampered and tampered receipts are byte-identical in verdict:

```text
action-frozen.json     exit 2  detail "expected.json pair 1/'denied_executable:sudo' is unreachable"
frozen-tampered.json   exit 2  detail "expected.json pair 1/'denied_executable:sudo' is unreachable"
```

Whatever byte was altered in the `/tmp` copy, `plan.json` and `policy.json`
were never opened. `snapshot_tampered` was unreachable for that snapshot even
with no tampering at all. The receipt's `matched_exit: true` is true only
because the wrapper compares **exit code**, not the finding token — both
`frozen_error` and `snapshot_tampered` are exit 2. That is the labeling defect
R16-V1, confirmed at source level.

Scope note: the digest path itself worked at `9dcf248`. The selftest's own
`frozen-tampered-plan`/`frozen-tampered-policy` cases passed there (append
`\n#tampered\n` to plan/policy with a valid `plan_safe`/0 pair → `2
snapshot_tampered`). The defect is confined to the standalone receipt and the
pair-first masking, not to a missing digest implementation.

## 5. What `--frozen` checks first: pairs, then digests

Current `tools/mado-action-plan.py`, `run_frozen` (lines 407–480), in order:

1. `_load_json(expected.json)` via `_read_regular` (line 413): regular file,
   `O_NOFOLLOW`, one bounded read, strict JSON (duplicate keys rejected).
2. `expected.json` shape: object, no unknown keys, optional schema, all four
   mandatory keys (`plan_sha256`, `policy_sha256`, `expected_finding`,
   `expected_exit`).
3. Pin shape (64 hex) and field types.
4. **Pair reachability** (lines 447–459): `(expected_exit, expected_finding)`
   must be one of the exact 21 verdicts derived from the pinned constants.
   **This precedes every input read.**
5. **Only then** the input loop (lines 460–471): read `plan.json`, hash it,
   compare to `plan_sha256`; then `policy.json`, hash, compare. Mismatch or
   unreadable input → `snapshot_tampered`, exit 2. Plan is checked first.
6. Classify the **same bytes** already hashed (lines 472–475) via
   `_evaluate_raw` (policy first, then plan, in-memory only).
7. Compare finding **and** exit (lines 476–480): match → `frozen_match` exit 0;
   otherwise `frozen_verdict_mismatch` exit 1.

So: **pairs before digests; digests before classification; classification
before verdict compare.** `expected.json` is not itself digest-pinned in-band
(only its internal shape/pair is validated); its authority is the committed
external binding, as round 16 stated.

At `9dcf248` the order was the same; only step 4's predicate was wrong.

## 6. Minimal tamper at current content that isolates the digest check

Current committed snapshot (observed hashes): `expected.json`
`e76090a3…be535`, `plan.json` `82bc7652…febc3`, `policy.json` `fb134d8f…8b7fc`.
The pair `(1, "denied_executable:sudo")` is in the current valid set, and
`plan.json` is the red `sudo pacman -S … libinput` plan.

**Control A — pure digest isolation (recommended primary).** Copy the three
files to a fresh temp dir unchanged; append exactly one byte, `\n`, to
`plan.json`; leave `expected.json` and `policy.json` untouched. The new plan
digest is `c0288ff68e06c6624354fcf3a9b370e216ced6fdbccf45635e4106b32b603e9d`
(computed over the stream; the plan still parses and still classifies to
`denied_executable:sudo`/1). Run the gate. Expected: exit 2,
`snapshot_tampered`, detail `plan.json sha256 <new> != pinned 82bc…`.
Why this isolates the digest check: pair is valid, policy is intact, and the
parsed plan and its verdict are literally unchanged — if the digest compare
were skipped the gate would print `frozen_match`, exit 0. The **only** gate
that can produce exit 2 here is the plan digest check.

**Control B — digest before classification/verdict.** Copy unchanged; replace
one byte in `plan.json`, `sudo` → `sud0` (argv[0]). New digest
`d5bb6f2342f20f03835a815cb46cfa50300638e4197ff9b1c3618d4ddd6539e2`; the plan
still parses, but `_classify` would now return `plan_safe`/0 because basename
`sud0` is not in `PINNED_DENY_EXECUTABLES`. Expected with the digest check:
exit 2, `snapshot_tampered`. If the digest check were absent or ordered after
classification, the result would be `frozen_verdict_mismatch`, exit **1**.
Observing 2 rather than 1 proves digests run before classify/compare.

Do **not** tamper `expected.json` in the recut control: any edit there can trip
the expected-file structure or pair check first and reproduce the same masking
error. Do **not** mutate plan and policy together if the ordering (plan first)
is to be shown. The recut receipt should carry: mutation file, byte offset,
old→new byte, pre-tamper sha256, post-tamper sha256, finding token, and exit —
all of which the round-16 receipt omitted.

## 7. Divergences named

1. **Label vs finding (R16-V1, confirmed):** round-16 lesson line 131–132 says
   "Input tamper control returns **2 snapshot_tampered**, retained in
   `frozen-tampered.json`"; the retained receipt's finding is `frozen_error`.
   The fleet report line 64 repeats "Tampered frozen input returns2
   `snapshot_tampered`; original receipt retained."
2. **Vacuous control:** at `9dcf248` the tampered and untampered runs emitted
   identical stdout; the tamper was never read because the pair check fired
   first. The valid evidence for the digest path at that commit is the selftest
   fixtures, not this receipt.
3. **Exit-only receipt matching:** `matched_exit` compares 2 to 2 and cannot
   distinguish `frozen_error` from `snapshot_tampered`. Any recorder reused for
   the recut must compare the finding token too.
4. **Unrecorded mutation:** the temp dir is gone and no mutation record exists;
   the receipt cannot be replayed to show which bytes were altered.

## 8. Confidence and limits

- Receipt fields, file hashes, git blob hashes, exit-map text and code order:
  **high** (directly observed).
- Pair-before-digest as the cause of the `9dcf248` `frozen_error`: **high** —
  the error string names the pair, the pair block precedes the digest loop in
  the exact measured blob, and the selftest failure pattern matches the
  double-colon predicate exactly.
- The `tempfile.mkdtemp` origin of the `/tmp` name: **medium** (name shape
  only; no producer retained).
- Which byte round 16 actually altered: **unknown / unrecoverable**.
- The minimal-tamper outcomes in §6 are **[INFERENCE]** from source; this seat
  ran no gate. They are the recut executor's acceptance expectations, not
  observations.
- Residual, out of scope here: `expected.json` is not in-band authenticated
  (E1/E2 in the round-16 design), so a consistent rewrite of all three files
  remains undetectable by `--frozen` alone; the committed binding is the only
  anchor.

Tooling: none installed or updated. Commands issued were read-only
(`git show`, `sha256sum`, `grep`, `sed`-to-stdout, `od`, `jq`, `ls`); no host
mutation, package query, service/compositor operation, input probe or test run.
