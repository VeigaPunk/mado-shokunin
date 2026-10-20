# FrozenProvenanceCheck — mado round 18, wave 1

Executed 2026-10-20. Lane: mado-shokunin. No git/jj write, no pacman/system/host
command, no network fetch. Python stdlib only (`python3 -I`, Python 3.14.8). No
tool installed or upgraded.

## Deliverable

`.ufo/waves/round-18/frozen-provenance-check.py`

- sha256 `a55ba07ec7f2b034ab38197d7ff57326e42cf67ae43f1baada26da9a65d0ba2e`
- 469 lines, executable, `python3 -I` clean, no third-party imports.
- Reads `ROOT/provenance.json` (default `ROOT = <this script's dir>/frozen-tripwire`)
  and `ROOT/../../round-17/evidence/session-index.json` by default; `--root`,
  `--index`, `--provenance` override. Writes nothing.

### What it checks

For every provenance input (`inputs[].path`, optional declared `sha256`) and
source (`sources[].path`, optional `sha256`, `pairs: [[snapshot_line,
source_line], ...]`, 1-based):

1. input exists, is a regular non-symlink file; declared input digest equals
   the bytes on disk;
2. source exists as a regular file — if it is gone the verdict is
   `could_not_evaluate` with the explicit note *the frozen snapshot is now the
   only copy of these lines*;
3. source sha256 equals the `session-index.json` entry when the path is listed
   (an unlisted source is reported under `unindexed`, not failed);
4. every pair is compared **byte-exact, newline included** (`\n`-split only, so
   CRLF and 0x85 bytes are preserved; files are read as bytes, never decoded);
5. any `*.jsonl` under `ROOT/inputs` that provenance does not claim is reported
   `input_unclaimed`.

Exit precedence follows `tools/mado-tripwire.py`: unclaimed/missing/refused →
**2**, byte or digest difference → **1**, all equal → **0** (2 wins over 1).
First stdout line `MADO_FROZEN_PROVENANCE: match|mismatch|could_not_evaluate`,
second line one JSON verdict (`mado-frozen-provenance-verdict-v1`) with every
input/source digest, pair count, `diffs[]` (reason + first-divergence byte),
`unresolved[]`, `unindexed[]`, and the running tool's sha256. Paths that resolve
to `agent.db*` are refused with exit 2 (same rule as the tripwire's
`REFUSED_NAMES`).

Canonical schema it expects is exactly the one `TwFrozenSnapshot` confirmed and
landed (`schema: mado-tripwire-frozen-provenance-v1`); object-form pairs,
dict-keyed `inputs`, `source` as an object with `lines`, and `files`/`provenance`
aliases are also accepted so a shape change cannot silently disable the check.
`line_base: 0` is supported.

## Evidence

### 1. Real frozen snapshot — matched

`python3 -I .ufo/waves/round-18/frozen-provenance-check.py` (run from the lane
root, 2026-10-20T15:48:32Z, after the snapshot landed):

```
MADO_FROZEN_PROVENANCE: match
exit 0 · pairs 26 · diffs 0 · unresolved 0 · unindexed 0
provenance sha256 4fb06b6e42b52d5cb04e6ef8a19b36c2a8851a7bbd47e28e1c846f8941ff6310
index      sha256 06c259bcdd44785d93d846ca971257fdbb27d68ea70da7251448561423f70df5
tool       sha256 a55ba07ec7f2b034ab38197d7ff57326e42cf67ae43f1baada26da9a65d0ba2e
```

All five inputs (`r15-libinput-events`, `r13-global-capture`,
`r14-review-source-bar`, `r14-source-safety`, `r13-root`) declared digests equal
observed digests; all five sources are indexed and their current sha256 equals
the round-17 index; 26 pairs (5/5/5/6/5) compared byte-equal.

### 2. The check demonstrably fails

On a **/tmp copy** (`/tmp/fpc-real-mutant`, the lane snapshot untouched):

- one byte flipped in `inputs/r14-source-safety.jsonl` →

```
MADO_FROZEN_PROVENANCE: mismatch          exit 1
diffs: input_sha_mismatch (declared 8635cca2… observed e7c67d70…)
       line_bytes_differ snapshot_line 1 / source_line 130, "first divergence at byte 10"
```

- provenance rewritten to point an input at a vanished source →

```
MADO_FROZEN_PROVENANCE: could_not_evaluate exit 2
unresolved: source_missing — "the frozen snapshot is now the only copy of these lines"
```

### 3. Fixture suite — 21/21 pass

`/tmp/fpc-lab/build.py` + `/tmp/fpc-lab/run_all.py` (ephemeral; commands below).
Each case asserts the exact exit code, outcome word and reason needle:

| group | cases |
|---|---|
| match | clean; object-pair/dict-input shape; unindexed source; CRLF; no trailing EOL; 300 KiB line; `line_base: 0` |
| exit 1 | snapshot byte differs; source digest stale vs index; mapped source line missing; declared input digest wrong; missing-EOL line snapshotted with EOL |
| exit 2 | source gone; provenance not JSON; `agent.db` path refused; unclaimed extra input; diff + missing source together (2 wins); symlinked input; empty `pairs`; no snapshot yet (`"snapshot not built yet"`) |

Run them with:

```
python3 /tmp/fpc-lab/build.py && python3 /tmp/fpc-lab/run_all.py   # failures: 0
```

### 4. Cross-checks against the snapshot builder's own artifacts

- `expected.json` input digests equal `provenance.json` digests and the bytes on
  disk for all five inputs; `inputs/` contains exactly the five claimed files
  (no unclaimed input).
- Every `expected_findings` and `known_misses` line is a snapshot line carried by
  a provenance pair: 11/11 covered (last read: 8 findings, 3 misses).
- Preflight, before the snapshot landed: the five planned sources were already
  present, listed in the round-17 index, and sha-matching (228 indexed files);
  an end-to-end run built from the announced five-input plan against the real
  transcripts and real index returned `match`, 6 pairs.
- Mid-run the builder rewrote `expected.json` (`expected_findings` 10 → 8), so
  the report's counts are from the last read; the provenance check itself
  returned `match` both before and after.

## Reproduce

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-18/frozen-provenance-check.py            # 0 match
cp -a .ufo/waves/round-18/frozen-tripwire /tmp/frozen-mutant
# flip one byte in any inputs/*.jsonl, then:
python3 -I .ufo/waves/round-18/frozen-provenance-check.py --root /tmp/frozen-mutant   # 1 mismatch
```

## Risks and limits (stated, not hidden)

- **Read-after-hash window.** Inputs and sources are hashed and then re-read for
  line comparison; a source appending between the two reads would be reported as
  digest mismatch (exit 1) or line diff, not silently pass. Transcripts in this
  lane are append-only; the snapshot is static.
- **Declared pairs only.** The tool verifies the mapping provenance declares; it
  does not infer source lines provenance omits. `input_unclaimed` covers whole
  files, not missing pairs within a claimed file.
- **`provenance.json`'s `index` key is not honored** as a path; the default
  index resolves to the same file today (`06c259bc…`). If the index moves, pass
  `--index`.
- Whole files are read into memory (largest source here 3.8 MB); a source line
  over memory budget would fail as `could_not_evaluate`, never as a pass.
- `TwFrozenSnapshot` confirmed `provenance.json` final at `4fb06b6e…` before
  this report was written; L1 should still re-run the one-line reproduce
  command after integration. If a re-pin changes `provenance.json`, the
  recorded provenance sha256 no longer describes it and the check must be
  re-run (it will say so, not silently pass the old digest).

## Handoff for L1

The runnable check for lesson criteria 24–26 can cite exactly:

```
python3 -I .ufo/waves/round-18/frozen-provenance-check.py
```

— `match`/exit 0 on the committed snapshot, and exit 1 on a one-byte mutation of
a /tmp copy (shown above). Files written by this seat: this script and this
report only.
