# R67ExecHarness — C2 landing-control harness

Round 67 / wave w1 / executor seat. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base rev measured: `0b28ffb4baac9586566d246c3f0986b2bb650a33`. Freeze: `061dc329`.

## Deliverable

`draft/quality/counters/c2-r67-landing-controls.py` (relative to this seat dir; L1 copies to
`quality/counters/c2-r67-landing-controls.py`).

- path: `.ufo/waves/round-67/w1/R67ExecHarness/draft/quality/counters/c2-r67-landing-controls.py`
- sha256: `a4376fa739405a213ccd59847620be02bec5fd2a70584aa59dfbc916022d9b58`
- size: 711 lines, 30,697 bytes; `ast.parse` ok; no non-stdlib imports (argparse, hashlib, os,
  re, shutil, subprocess, sys).

No tool installs; nothing needed (pacman paused host-wide, untouched). No network, no
compositor/service/session contact, no lane/fleet git mutation.

## Implemented contract (frozen C2 text)

```
python3 quality/counters/c2-r67-landing-controls.py --repo . --rev REV --scratch-root DIR
python3 quality/counters/c2-r67-landing-controls.py --selftest --scratch-root DIR
```

- Exit 0 iff the extracted instrument's own `--selftest` is rc 0 **and** `killed=2/2`;
  1 otherwise; 2 on setup/usage error (reason on stderr).
- Exact printed line (last line):
  `MADO_R67_LANDING_CONTROLS: selftest=<rc> mz=<pass|fail> mr=<pass|fail> killed=<n>/2 baseline=0/2 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>`
- Refuses `/tmp`, `/var/tmp`, `/dev/shm` and any lexical symlink component in the scratch
  root, before creating anything (verified: rc 2 on all four).
- One measurement, all writes under `<scratch>/r67-c2/`:

1. Resolve `--rev` and assert `--repo` is the repository root; extract with a fully explicit
   env (no inherited `GIT_*` at all) carrying `GIT_OPTIONAL_LOCKS=0` and
   `GIT_NO_REPLACE_OBJECTS=1`, via `git cat-file blob <sha>:<path>`:
   `quality/landing-counters.sh`, `quality/counters/c3-r56-used-by.py`,
   `quality/check-tool-ledger.py`, `tools/mado-receipt-citecheck.py`.
2. Run the extracted `quality/landing-counters.sh --selftest` (expected green).
3. **M-Z**: copy the tree; assert the exact clause `[ "$citations" -gt 0 ] && ` occurs
   exactly once; delete it once; require the mutant still passes `bash -n`; re-run its
   `--selftest`. Killed iff that selftest exits nonzero.
4. **M-R** (bound target = the citecheck child, per L1 steering of 2026-11-03; the seat
   prompt's used-by framing was superseded before construction — the citecheck child's
   explicit `env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")` is the guard, and its
   `ls-tree` read is exactly what a root-tree replacement rewrites): build a scratch fixture
   repo whose real tree lacks `corpus/cited.md` while a worktree receipt cites it, then plant
   `git replace <real_root_tree> <forged_root_tree>` adding the path (asserted visible
   unguarded and hidden under `GIT_NO_REPLACE_OBJECTS=1`); copy the child, assert exactly one
   `GIT_NO_REPLACE_OBJECTS` occurrence, delete the guard line (fallback: token rename only if
   deletion no longer compiles), and run both children on the same fixture with a scrubbed
   env that carries **no** `GIT_NO_REPLACE_OBJECTS` (printed verbatim, PATH summarized).
   Unmutated must read the real tree (rc 1, `TARGET_MISSED`, `missing=1`); the mutant must
   credit the forged tree (rc 0, `TARGET_MET`) — that pair is the kill.
5. `--selftest` is hermetic: 47 assertions, spawns nothing (asserted by patching
   `subprocess.run` to raise for the whole check body), writes only under the scratch root,
   removes its work dir.

Mutant evidence lines carry the exact removed unit (`removed=` / `removed_line=`), the
unmutated sha256 and the mutant sha256. No kill is claimed when a recipe is inapplicable.

## Measured dry runs

### Candidate bytes (the two sibling drafts committed in a scratch repo)

candidate repo rev `117dbf5a700bcd006b5f0b97d244a017cbdba95b`; exit 0

```
MADO_R67_EXTRACT path=quality/landing-counters.sh bytes=15658 sha256=4378fd8c278126111ad6d970ac20215c170238ffe1a796c5c7d03c9e5b3b93a9
MADO_R67_EXTRACT path=quality/counters/c3-r56-used-by.py bytes=21326 sha256=f54423eb8ab24eeb5a8cd51f2d38408fe02054797ba841c3940cde28d3903b3f
MADO_R67_EXTRACT path=quality/check-tool-ledger.py bytes=40636 sha256=1c96c4cfd69ad97fbfc9174c9fe4d27b1d157df69cbcbc2451067f1374febdfb
MADO_R67_EXTRACT path=tools/mado-receipt-citecheck.py bytes=10822 sha256=3b61fa42b77e9c8065ab05668247c330b537910b06f7209caba7afbd0b102ad0
MADO_R67_EXTRACT rev=117dbf5a700bcd006b5f0b97d244a017cbdba95b files=4
MADO_R67_SELFTEST instrument=quality/landing-counters.sh rc=0 assertions=62/62
MADO_R67_MUTANT M-Z path=quality/landing-counters.sh clause_count=1 recipe=clause-delete removed='[ "$citations" -gt 0 ] && ' from_sha256=4378fd8c...b93a9 rc=1 failed_assertions=3 assertions=59/62 killed=yes sha256=a6255a00262cc2f1790f813927dd5fa8ed9910e74d1ec19a8662e88df0fe0118
MADO_R67_GUARDS citecheck=1 usedby=1 ledger=1
MADO_R67_R_CONTROL fixture_rev=7a9457ed7b9afde074d77e1918658eddfb98dd89 real_tree=a82978be5fa20eb69fee0a6fbe51a99c37bc6a3e forged_tree=1b37d99db3872339180cf844ef9a05a3737bfb71 forged_visible=yes guarded_visible=no
MADO_R67_CHILD_ENV no_replace_objects=absent keys=GIT_CONFIG_GLOBAL,GIT_CONFIG_NOSYSTEM,GIT_CONFIG_SYSTEM,GIT_TERMINAL_PROMPT,HOME,LC_ALL,PATH,TMPDIR GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_SYSTEM=/dev/null GIT_TERMINAL_PROMPT=0 HOME=<scratch>/r67-c2/home LC_ALL=C PATH=<first>...(21 dirs) TMPDIR=<scratch>/r67-c2/home
MADO_R67_R_CHILD role=unmutated rc=1 verdict=TARGET_MISSED missing=1 control=green
MADO_R67_MUTANT M-R path=tools/mado-receipt-citecheck.py guard_count=1 recipe=line-delete removed_line='            env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"),\n' from_sha256=3b61fa42...ad0 rc=0 verdict=TARGET_MET missing=0 forged_credit=yes killed=yes sha256=414ca759232a3d31451f86060f4b0ba3382dd151f4bffe797793cb2ced5cee11
MADO_R67_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=117dbf5a700bcd006b5f0b97d244a017cbdba95b
```

M-Z red assertions are exactly the zero-citation guard semantics (no collateral):
`SELFTEST FAIL 43: citecheck zero citations refused want=2 got=0`,
`FAIL 45: zero-citation guard occurs exactly once want=1 got=0`,
`FAIL 46: zero-citation guard sits inside marker_valid want=1 got=0`.

M-R mutant is byte-identical to the pre-r67 citecheck (`414ca759…`), i.e. the mutation exactly
reverts the one-line guard. Guarded/unmutated child on the same fixture: `TARGET_MISSED`
`missing=1` rc 1; mutant: `TARGET_MET` rc 0.

### Base rev `0b28ffb4…` (lane, read-only) — reproduces the frozen baseline

exit 1

```
MADO_R67_MUTANT M-Z path=quality/landing-counters.sh clause_count=1 recipe=clause-delete ... rc=0 failed_assertions=0 assertions=58/58 killed=no sha256=8ab304938e12081b9ecca793f928aa4c079078da4b48f7958582d62d090abe69
MADO_R67_GUARDS citecheck=0 usedby=0 ledger=0
MADO_R67_R_CHILD role=unmutated rc=0 verdict=TARGET_MET missing=0 control=red
MADO_R67_MUTANT M-R path=tools/mado-receipt-citecheck.py guard_count=0 recipe=none ... killed=no sha256=absent note=guard absent at rev (count=0): recipe not applicable
MADO_R67_LANDING_CONTROLS: selftest=0 mz=fail mr=fail killed=0/2 baseline=0/2 verdict=TARGET_MISSED rev=0b28ffb4baac9586566d246c3f0986b2bb650a33
```

Matches `control-baseline-r67.txt` (`selftest_rc=0`, `zero_citation_case=0`,
`replace_ref_case=0`, base child reads the forged tree, killed 0/2).

### Extraction hardening measured

Scratch copy of the candidate repo with `git replace <real landing blob> <forged blob>`:
unguarded `git show` returned `924028e388e6d292cd90db9dad7dd72a3b734792887c2a7dc4ed728a3bb217b0`,
guarded read and the harness extraction both returned the real
`4378fd8c278126111ad6d970ac20215c170238ffe1a796c5c7d03c9e5b3b93a9`; full run still
`killed=2/2`, exit 0.

## Exact commands and exit codes

Run from the lane root unless noted (scratch root under `/fast/scratch/hyaku/mado-r67/R67ExecHarness/`):

| command | exit |
|---|---|
| `python3 <draft> --selftest --scratch-root <S>/st` | 0 (`47/47 assertions passed`) |
| `python3 <draft> --repo <S>/candrepo --rev HEAD --scratch-root <S>/cand` | 0 |
| `python3 <draft> --repo <lane> --rev 0b28ffb4baac9586566d246c3f0986b2bb650a33 --scratch-root <S>/base` | 1 |
| `python3 <draft> --repo <S>/replrepo --rev HEAD --scratch-root <S>/repl` (planted landing blob replace) | 0 |
| `--selftest --scratch-root /tmp/…`, `/var/tmp/…`, `/dev/shm/…`, `<symlink>/child` | 2 each |
| `--repo <lane> --rev deadbeef …` / `--repo /fast/scratch --rev HEAD …` / `--selftest` (no root) | 2 each |

`<S>` = `/fast/scratch/hyaku/mado-r67/R67ExecHarness` (removed before yield).
The candidate repo is a scratch fixture holding the validated sibling bytes:
landing `4378fd8c…`, used-by `f54423eb…`, ledger `1c96c4cf…`, citecheck `3b61fa42…`
(all four identical to the sibling drafts on disk at report time).

## Invariants / stability

- Fixture tree oids are content-stable across runs: real `a82978be5fa20eb69fee0a6fbe51a99c37bc6a3e`,
  forged `1b37d99db3872339180cf844ef9a05a3737bfb71`; only the fixture commit sha varies
  (commit timestamp), which is why it is recorded, never asserted.
- Re-running on the same scratch root wipes `<scratch>/r67-c2/` first; results are identical
  apart from `fixture_rev`.
- `--selftest` covers: frozen extract list, frozen tokens, clause recipe (absent/duplicate/
  deterministic), guard line-delete + non-deletable fallback, marker parsing, control and
  forged-credit predicates, exit/verdict aggregation, exact contract line shape, scratch
  refusals (tmp-family, root, empty, symlink), env scrub against a hostile `GIT_DIR`/
  `GIT_CONFIG_COUNT`/`GIT_REPLACE_REF_BASE`, child-env key set and guard absence, sha256
  helper, and no-spawn enforcement.

## Coverage limits / unverified legs (stated, not claimed)

- M-R is bound to `tools/mado-receipt-citecheck.py`, not `quality/counters/c3-r56-used-by.py`
  as the seat sketch said, per L1 steering ("M-R binds the citecheck child's explicit
  GIT_NO_REPLACE_OBJECTS guard (tree-replacement fixture), not used-by"). The used-by and
  ledger children also carry the guard (`MADO_R67_GUARDS usedby=1 ledger=1` on the candidate)
  but are **not** exercised as the M-R mutant; no kill is claimed for them.
- The R control's "real defect" is a cited path absent from the real tree (the citecheck
  child's own leg). It is not the used-by pair defect the seat sketch named.
- The harness reads git objects only. It cannot measure uncommitted working-tree drafts: L1
  must integrate the drafts (or measure a committed candidate rev). The candidate run above
  is that shape reproduced in a scratch repo, not a claim about the lane.
- Base: M-Z is mechanically applicable but not killed (the base selftest has no
  zero-citation case), and M-R has no guard to remove — both reported as `fail`, never as
  kills. A universal fault-coverage claim is not made: exactly these two mutants, these two
  controls.
- Not measured: any lane-level `quality/landing-counters.sh --repo … --rev …` run (needs the
  integrated candidate and the round receipts); no claim of the axis score beyond the two
  frozen control counters.

## Scratch

`/fast/scratch/hyaku/mado-r67/R67ExecHarness/` removed with delete-on-exit
(`trap 'rm -rf -- "$S"' EXIT`); verified absent after the run. No files written to `/tmp`,
`/var/tmp`, `/dev/shm`, the fleet repo, other lanes, `MANIFEST.json`, `.ufo/state`, or operator
config.
