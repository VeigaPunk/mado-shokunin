# AtkCarry — attack on routed defect 6 (round-24 carry population)

**Attacked:** `.ufo/waves/round-24/carry/` — the claim that the round-23 wave-2
fixture population is frozen byte-exact as a registered population (28 fixtures in
5 report populations), and that the base classifier `tools/mado-tripwire.py` is
unchanged (pre-C1 bytes).

## Checks performed

### 1. Re-hash every fixture against manifest.json
All 28 entries in `manifest.json` (schema `mado-r24-carry-population-v1`) were
re-hashed and size-checked against `entries[].sha256` / `entries[].bytes`:
`sha256(copy) == manifest.sha256` and `size == manifest.bytes` for 28/28 — **0 mismatches**.
`fixture_count` field (28) equals actual entry count; population counts in the
manifest match the entries (`AttackLateCell` 5, `AttackRecallRegress` 4,
`AttackFrameScopes` 4, `AttackEscapeGate` 5, `ReClosureNeighbour` 10).

### 2. Re-hash every fixture against its origin path
All 28 `origin_path` files exist and are byte-identical to the carry copy and to
the manifest sha256 — **0 mismatches, 0 missing origins** (19 lane origins under
`.ufo/waves/round-23/w1/out/...` and `w2/out/...`; 9 scratch origins under
`/fast/scratch/hyaku/mado-r23/w2/...` are still present and match).

### 3. Classifier identity / "no tools change"
- Current `tools/mado-tripwire.py` sha256 = `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`
  = manifest `base_classifier.sha256` = `.ufo/waves/round-23/evidence/tool-base-cd9da20c.py`
  (byte-identical). Tool unchanged.
- Running `python3 --version` = 3.14.8, matching manifest `base_classifier.python`.
- `base-run.txt` sha256 = `a4f27aa772d1ae8be36942eceb71e09f9429150c98ef885c94834263bb9e5337`
  = manifest `base_run.sha256`.

### 4. Re-run of the base classifier on 5 fixtures
Ran `timeout 60 python3 -I tools/mado-tripwire.py --scan <fixture>` from the carry
dir, one fixture at a time, `ulimit -v 393216` (384 MiB) per child. All five match
`base-run.txt` exactly (exit code, findings class/command/evidence, lead/observed
counts, `unparsed_spawns`, and the tool's own reported fixture sha256):

| fixture | rerun exit | base-run row | verdict |
|---|---|---|---|
| `AttackLateCell/LateEnclosingLocalViaRelay.jsonl` | 1 (observed `pacman -S r23w2-relay-foreign`, unparsed 0) | 1 | identical |
| `AttackRecallRegress/RecallClosureStoredInDict.jsonl` | 1 (lead `pacman -S r23x-closure-dict`) | 6 | identical |
| `AttackFrameScopes/MatchCaptureBinderNotOwned.jsonl` | 0 (clean, unparsed 1) | 12 | identical |
| `AttackEscapeGate/EscapeNonlocalHook.jsonl` | 1 (lead `pacman -S r23w2-nonlocal-hook`) | 16 | identical |
| `ReClosureNeighbour/W2e-1-subscript-store-rebind-after-handoff-direct-call.jsonl` | 1 (observed `pacman -Q w2e-direct-final`, unparsed 1) | 26 | identical |

Tool sha256 after the runs: unchanged (`cd9da20c...`); no file under `tools/` was
written.

### 5. Internal consistency of the reference log
All 28 JSON blocks in `base-run.txt` match `entries[].base_scan` exactly (exit,
lead_findings, observed_findings, unparsed_spawns, eval_unparsed, findings tuples,
and the fixture sha256 the tool printed). The summary table is self-consistent:
18 exit-1, 10 exit-0, 0 errors/timeouts, as the README states.

## Findings

No actionable findings. No mismatch in any hash, size, origin, tool identity, or
classifier rerun; no change to `tools/`; the population is 28/28 byte-exact and
the reference run is reproducible.

## Residual risk / verification gaps

- Execution truth (`[UNK]` host behaviour, recording fake-subprocess children) is
  not re-derived here; this attack verifies the frozen transcript bytes and the
  base-classifier CLI verdicts, which is the scope of defect 6.
- The seven `ReClosureNeighbour` regressions and three critic fixtures remain
  "not measured" at the r23 close tip per the README — that is declared, not a
  defect of the freeze.
- No tool installs were needed; nothing was installed or updated this run.

VERDICT: holds
