# ExecC3Rerun — independent re-run of the C3 index gate

Item: runner (no writes beyond this report). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, worktree HEAD
`92d3c8676f4801b2ed2692cf45280796c166c88c`, clean except this wave's untracked
`.ufo/waves/round-30/w1/` report directory. Nothing in the lane, fleet repo,
git index, jj state, compositor or config tree was written; scratch trees live
only under `/tmp`.

## Verdict: C3 predicate REPRODUCES byte-for-byte; no kill rule triggers

- `--rev 8f51071b…` → `indexed=41/43 missing=2` exit 1 (K3 red at base).
- `--rev 446dc396…` → `indexed=43/43 missing=0 dangling=0 duplicates=0
  coverage=10.0000/10` exit 0.
- `--selftest` → `MADO_INDEX_SELFTEST: 6/6 assertions passed` exit 0.
- The three-invocation transcript is **byte-identical** (432 bytes,
  `sha256 bb18d52c4da299463b61bf5fc89b69fdbe5c03d5af0699b2639b2e9025025f3d`,
  `cmp` clean) to `.ufo/waves/round-30/evidence/c3-after-446dc396.txt`.

Reproduction used full 40-hex revisions, because the gate echoes the `--rev`
argument verbatim into its `rev=` tag: `--rev 446dc396` prints
`rev=446dc396` with the same counts. Short-hash runs are numerically
equivalent but not byte-comparable; the committed receipt correctly used full
hashes.

## Commands actually run (cwd = lane root)

```
python3 -I quality/check-index.py --rev 8f51071b5bc44c815eeb5da76bb7f1947994ffb8 --repo .
python3 -I quality/check-index.py --rev 446dc3966193c81e64896f4880a19a4bd249255b --repo .
python3 -I quality/check-index.py --selftest
```

Observed transcript (matches the receipt):

```
MADO_INDEX: rev=446dc3966193c81e64896f4880a19a4bd249255b indexed=43/43 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
EXIT=0
---base control---
MADO_INDEX: rev=8f51071b5bc44c815eeb5da76bb7f1947994ffb8 indexed=41/43 missing=2 dangling=0 duplicates=0 coverage=9.5349/10
missing: knowledge/mutation-testing-r28.md
missing: knowledge/workspace-rules-r27.md
EXIT=1
---selftest---
MADO_INDEX_SELFTEST: 6/6 assertions passed
EXIT=0
```

## `--root` mode against scratch copies (never the lane)

`cp -a` of the lane tree to `/tmp/c3-root-scratch` (227 MB, byte-faithful:
`corpus/README.md` sha256 `ea35d422…` identical on both sides, knowledge
listing identical, no non-regular members under `corpus/knowledge/`):

| Tree (scratch, /tmp only) | Command | Result | Exit |
|---|---|---|---|
| worktree copy (HEAD `92d3c86`) | `--root /tmp/c3-root-scratch` | `indexed=43/43 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | 0 |
| `git archive 446dc396 corpus` | `--root /tmp/c3-root-446` | `indexed=43/43 … coverage=10.0000/10` | 0 |
| `git archive 8f51071b corpus` | `--root /tmp/c3-root-8f51` | `indexed=41/43 missing=2` (both notes named) | 1 |

`--root` therefore agrees with `--rev` on all three byte-sets: the data
commit's tree is complete, the base tree is red by the same two notes, and the
worktree copy is complete. Default `--rev` (no argument) resolves
`rev-parse master` → HEAD, 43/43 exit 0.

## Gate semantics vs the frozen fence (S185)

Re-ran the SCORECARD "Counting command" block itself at both revisions
(`REV=… python3 - <<PY`): base `indexed=41/43`, tip `indexed=43/43`, same
missing names, same exit codes. The gate is the same algorithm
(`git ls-tree --name-only REV:corpus/knowledge` + `git show REV:corpus/README.md`,
`Counter` over `^\| …knowledge/([^`]+\.md)``, `covered = count==1`,
`10*covered/len(notes)`, exit 1 on any of missing/dangling/duplicates).
Only difference: the gate's row regex allows `\s*` after the leading pipe
where the fence requires one literal space — a superset that changes nothing
on current bytes (both match exactly 43 rows; the README has no line-start
`| `knowledge/…`` occurrence outside the coverage table, and mid-line link
mentions such as `[plane](knowledge/…)` on rows 70–76 are correctly not
counted).

S185's digest pin is correct: the fence block body at `master:SCORECARD.md`
hashes to `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`,
matching `SCORECARD.md:194` and the S185 row.

## Non-vacuity probes (mutations on /tmp copies only)

| Probe | Result | Exit |
|---|---|---|
| delete the real `workspace-rules-r27.md` row from a copy of the data tree | `indexed=42/43 missing=1`, names the note | 1 |
| duplicate the real `mutation-testing-r28.md` row | `indexed=42/43 duplicates=1`, names the note | 1 |
| symlinked `corpus/README.md` | `REFUSED: non-regular member …` | 1 |
| symlinked note in `corpus/knowledge/` | `REFUSED: non-regular member …` | 1 |
| `--rev deadbeef` | `SETUP_ERROR: fatal: Not a valid object name …` | 2 |
| `--rev` and `--root` together | `SETUP_ERROR: choose --rev or --root, not both` | 2 |
| nonexistent root, and fleet root (no `corpus/README.md`) | `SETUP_ERROR: … not a regular file` | 2 |

The gate is red on real-byte regressions and on non-regular members, and it
fails closed (exit 2) on setup errors rather than printing a score.

## Artifact identity / freeze

`quality/check-index.py` is one immutable blob across the round:
`df01b20fa2c45ddee954da1841e2519f7e7abd4d` at `451e8b3` (freeze commit),
`446dc396` (data commit), `92d3c86` (HEAD), and the worktree
(`git hash-object` agrees). 219 lines / 7889 bytes, mode 100755. Selftest
runs from a foreign cwd (`/tmp`) → 6/6 exit 0 and leaves no `/tmp/mado-index-*`
residue; source has 6 `check(...)` call sites (7 matches of `check(` include
the `def`). Freeze control: gate red at `451e8b3` (`41/43`), matching
`evidence/freeze-smoke-451e8b3c.txt`; green at HEAD `92d3c86`.

## Residual risks / observations (routed, not fixed here)

1. **Vacuous-green `--root` shape.** A tree that has `corpus/README.md` but no
   `corpus/knowledge/` directory prints `indexed=0/0 … coverage=0.0000/10`
   exit 0 (`/tmp/c3-noknow`). This is the declared "empty knowledge dir is a
   0-note clean state" selftest case, but it means a mistyped `--root` that
   still carries a README is indistinguishable from a legitimately empty
   corpus. Roots lacking the README (fleet root, nonexistent path) do exit 2,
   so the registered misroot sweep is not at risk; a future hardening could
   require the knowledge directory to exist, or gate the 0/0 case behind an
   explicit flag.
2. **Pre-existing malformed coverage row.** `corpus/README.md:52`
   (`knowledge/animation-table-r26.md`) has 3 pipes / 2 cells in a 3-column
   table, at base and tip alike. The gate counts it as a valid route because
   it scores route presence, not row shape (its docstring says so). Outside
   C1's two rows and outside the C3 predicate; no kill rule touches it.
   Worth a row-shape check in a later round.
3. **No registry row / no suite wiring.** `grep -n 'check-index' SKILL.md` is
   empty and `tools/mado-verify.sh` does not invoke the gate: the capability
   is re-runnable but not registered at the lane's gate home nor in the
   hermetic suite. This matches the already-routed round-31 item in
   `corpus/lessons/round-30-verifier-spotcheck.md`; `SKILL.md` is
   harm-watch-frozen this round, so it cannot be closed here.
4. **Doc-only discrepancy in a prior receipt.** That same spotcheck lesson
   says the S185 digest is "pinned in … `check-index.py`'s docstring"; the
   gate's docstring contains no digest (`grep 8b59b503 quality/check-index.py`
   → none). The pin in `SCORECARD.md`/`SOURCES.md` is correct (recomputed
   above); only the lesson's description is loose. Corpus bytes are L1-owned
   and were not touched.

## Harm watch / hygiene

- Lane `git status --porcelain` at the end of this item's runs (04:05): only
  `?? .ufo/waves/round-30/w1/` (this wave's reports). No `__pycache__`
  created; no lane byte changed by this item; no jj or index mutation.
- **Post-run out-of-scope change (not mine).** At 04:06:46 — after this
  item's last lane-touching command — the worktree gained
  `M quality/q36-successor-receipts.txt` (reported by `RevC1Fence`; verified
  by re-reading `git diff`). The delta is 4 lines and purely ephemeral run
  tokens (`/tmp/mado-r28-q36-ge5zx30t` → `g3nfq53x`,
  `run.gR7SQoLa` → `run.Kv8n49Ha`); every `rc=`, `expected=` and `PASS`
  token is unchanged, so no verdict moved. This item ran only
  `check-index.py` (writes nothing), `cp -a` from the lane, and read-only
  git/grep/awk/sed, so it cannot have produced that write; it is left in
  place for the L1/orchestrator to route, not restored here.
- No tool installs performed or needed (python3, git, bash pre-existing);
  pacman untouched under the host-wide pause.
- Scratch artifacts left for audit under `/tmp`: `c3-root-scratch` (227 MB),
  `c3-root-446`, `c3-root-8f51`, `c3-mut-missing`, `c3-mut-dup`,
  `c3-sym-readme`, `c3-sym-note`, `c3-noknow`, plus the transcripts
  `/tmp/c3-repro.txt`, `/tmp/c3-rev-{base,tip}.txt`, `/tmp/c3-selftest.txt`
  (safe to delete).

## Retained evidence

- Receipt `.ufo/waves/round-30/evidence/c3-after-446dc396.txt` is unchanged and
  byte-reproducible (`cmp` clean, sha256 `bb18d52c…`).
- Freeze receipt `.ufo/waves/round-30/evidence/freeze-smoke-451e8b3c.txt`
  independently corroborated (gate red at `451e8b3`).
- Full command/output transcripts quoted above; all numbers re-derived from
  committed bytes (`git ls-tree`/`git show`/`git archive`), never from the
  worktree, except the explicitly labeled `--root` worktree-copy run.
