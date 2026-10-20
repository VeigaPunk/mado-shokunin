# MadoR19.TwFrozenF2 — round-18 F2 closed: `--frozen` argument spellings are now judged by kernel resolution

Scope: round-18 carried finding **F2** (`--frozen DIR/.` launders a symlinked
frozen directory). Deliverables are the patch, the `f2-*` suite fragment and
this report. No git/jj write was issued in the lane (read-only `show`,
`ls-files -s`, `rev-parse`, `log` only). No package/service/compositor command,
no gate live run, nothing installed.

## Artifacts (all sha256)

| path (lane-relative) | sha256 |
|---|---|
| `.ufo/waves/round-19/drafts/TwFrozenF2.r19.patch` | `b6372f51b52235600d5bfa5092d3de1f495e4d84e82d0ef3901788aac045774f` |
| `.ufo/waves/round-19/tripwire/r19-frozen-f1f2/expected-f2.json` | `abcc3e060ffad4716f3505b19385a6bbd8ff8d6349f87efceb164c387e66dc1c` |
| `…/r19-frozen-f1f2/f2-target/expected.json` (also `f2-realdir-dot/`) | `2978b6786ef08fdda18f06b6f82c288a38b07b6ffe90b1cbbf6791de7d193409` |
| `…/r19-frozen-f1f2/f2-target/inputs/incident.jsonl` (also `f2-realdir-dot/`) | `cafde03a0290c1afef61f53b2e64b11f52b3bfa9251a0f2f247d46aedb011829` |
| tool at `9c54c56` / `17661e0` / lane worktree (base) | `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` |
| patched tool (`patch -p1` of the draft onto the base blob) | `5cc3924cf5d1f300eb8f9e0297f3f30bc4563ff14c75c394cf6cde142b261c9f` |

Base identity: `git show 9c54c56:tools/mado-tripwire.py | sha256sum` and
`git show 17661e0:tools/mado-tripwire.py | sha256sum` are both
`c1ae45a7…`, equal to `sha256sum tools/mado-tripwire.py` in the detached
worktree at HEAD `17661e0`. The draft is therefore a diff against the real
9c54c56 artifact, not a re-rendered file.

## 1. The defect, reproduced on the base blob

`run_frozen` gated on `os.path.islink(directory.rstrip("/") or directory)`, a
spelling test. With `f2-symlink-dir-dot -> f2-target` in the suite:

```
$ python3 -I base.py --frozen <suite>/f2-symlink-dir-dot/.          # c1ae45a7
MADO_TRIPWIRE_FROZEN: frozen_match                                   rc=0
$ python3 -I base.py --frozen <suite>/f2-symlink-dir-dot/./          rc=0 frozen_match
$ python3 -I base.py --frozen <suite>/f2-symlink-dir-inputs-dotdot/inputs/..   rc=0 frozen_match
$ python3 -I base.py --frozen <suite>/f2-symlink-dir-plain           rc=2 snapshot_tampered
```

The same run on the patched tool (5cc3924c…) returns `snapshot_tampered`
exit 2 for all four spellings.

## 2. Patch design (`b6372f51…`, 2 hunks + one helper, 50 diff lines)

- **DIR check.** `frozen_dir_symlinked(directory)` walks the *spelled* path
  component by component and returns true when any prefix is a symlink whose
  `realpath` equals `realpath(DIR)`. That is the kernel's own resolution, so
  `DIR`, `DIR/`, `DIR/.`, `DIR/./`, `DIR//`, `DIR/inputs/..` and
  `link/../evil` all reach the same verdict for the same directory. A symlink
  *above* DIR is deliberately not a rejection: it is host layout, not snapshot
  identity (round-18 N1b), and case `f2-ancestor-symlink-match` pins that.
- **DIR/inputs check.** `frozen_snapshot` now resolves the inputs directory
  against `real_dir` before the symlink test
  (`os.path.realpath(idir) != real_inputs`), so a symlinked `inputs/` is
  rejected independently of how DIR was spelled. The walk root stays the
  spelled path, which keeps `relpath` results relative to DIRECTORY (a first
  version that rooted the walk at `real_dir` broke ancestor-symlink paths;
  `f2-ancestor-symlink-match` guards exactly that regression).

Why not `normpath` + `islink`: a lexical `normpath` collapses `..` without
symlink awareness. Measured on a scratch variant (base + `islink(normpath(abspath(DIR)))`,
`lexical.py`, sha256 `69a43654…`):

```
$ python3 -I lexical.py --frozen <suite>/f2-symlink-dir-dot/.        snapshot_tampered
$ python3 -I lexical.py --frozen <suite>/f2-dotdot/link/../evil      frozen_match      <-- still a bypass
$ python3 -I patched.py  --frozen <suite>/f2-dotdot/link/../evil      snapshot_tampered
```

`f2-dotdot/link -> ../f2-outside/deep` and `f2-outside/evil -> ../f2-target`
make the kernel path `<suite>/f2-outside/evil` (a symlink to the frozen dir)
while the lexical path `<suite>/f2-dotdot/evil` does not exist. The prefix
walk closes it; case `f2-symlink-dotdot-launder` pins it.

No other behavior changes: the frozen path/containment/regular-file/digest,
reachability, unknown-key, duplicate-key and verdict logic is untouched, and
`--scan` is byte-identical (the diff is confined to the frozen section).

## 3. Fixtures and `expected-f2.json`

```
r19-frozen-f1f2/
  f2-target/                       real frozen dir: expected.json + inputs/incident.jsonl
  f2-realdir-dot/                  identical bytes, used as the real-dir `/.` control
  f2-symlink-dir-dot -> f2-target
  f2-symlink-dir-dot-slash -> f2-target
  f2-symlink-dir-inputs-dotdot -> f2-target
  f2-symlink-dir-plain -> f2-target
  f2-dotdot/link -> ../f2-outside/deep      (real dir with a placeholder file)
  f2-outside/evil -> ../f2-target
  f2-ancestor-symlink -> .                  (symlinked ancestor control)
  expected-f2.json  (7 cases; L1 merges with expected-f1.json, sha256 246b8cd5…, untouched)
```

Seven cases, all `mode: "frozen"`, all with `want_missing`/`want_extra` 0:
`f2-symlink-dir-dot` (2/snapshot_tampered), `f2-symlink-dir-dot-slash`
(2/snapshot_tampered), `f2-symlink-dir-inputs-dotdot` (2/snapshot_tampered),
`f2-symlink-dotdot-launder` (2/snapshot_tampered), `f2-symlink-dir-plain`
(2/snapshot_tampered, canonical spelling kept), `f2-realdir-dot-match`
(0/frozen_match, no over-rejection), `f2-ancestor-symlink-match`
(0/frozen_match, ancestor symlink allowed).

The harness passes `os.path.join(directory, case["args"][0])` unchanged, so
`args` carry the `/.`, `/./` and `/inputs/..` spellings verbatim (verified on a
relative suite path and from a foreign cwd).

**Symlink carriage.** Git carries the fixtures directly; no setup note is
needed. Precedent in this repository:

```
$ git ls-files -s .ufo/waves/round-18/tripwire/frozen/symlinked-frozen-dir \
      .ufo/waves/round-18/tripwire/frozen/symlinked-inputs-dir/inputs \
      .ufo/waves/round-18/tripwire/frozen/symlink-input/inputs/link.jsonl
120000 f0f14de6… 0  .ufo/waves/round-18/tripwire/frozen/symlinked-frozen-dir
120000 f7b7a40f… 0  .ufo/waves/round-18/tripwire/frozen/symlinked-inputs-dir/inputs
120000 ab892e34… 0  .ufo/waves/round-18/tripwire/frozen/symlink-input/inputs/link.jsonl
```

All seven fixture links are relative (`f2-target`, `../f2-target`,
`../f2-outside/deep`, `.`), so they survive a copy of the tree. Empty helper
directories carry a `placeholder.txt` so git can track them.

## 4. Red-before / green-after (the acceptance check)

Suite assembled for execution as `/tmp/tf2/r19suite` (`cp -a` of the lane
directory, `expected-f2.json` → `expected.json`):

```
$ python3 -I /tmp/tf2/base.py --selftest /tmp/tf2/r19suite      # base c1ae45a7, 9c54c56 bytes
CASE f2-symlink-dir-dot FAIL want=(2, 'MADO_TRIPWIRE_FROZEN: snapshot_tampered', 0, 0)
     got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match', ('frozen_match', 0, 0, 0))
CASE f2-symlink-dir-dot-slash FAIL  (same)
CASE f2-symlink-dir-inputs-dotdot FAIL  (same)
CASE f2-symlink-dotdot-launder ok
CASE f2-symlink-dir-plain ok
CASE f2-realdir-dot-match ok
CASE f2-ancestor-symlink-match ok
SELFTEST_SCRIPT_SHA256: c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd
SELFTEST_SUMMARY: 4/7 passed failed=['f2-symlink-dir-dot', 'f2-symlink-dir-dot-slash',
 'f2-symlink-dir-inputs-dotdot']                                                      rc=1

$ python3 -I /tmp/tf2/patched.py --selftest /tmp/tf2/r19suite   # patched 5cc3924c…
SELFTEST_SCRIPT_SHA256: 5cc3924cf5d1f300eb8f9e0297f3f30bc4563ff14c75c394cf6cde142b261c9f
SELFTEST_SUMMARY: 7/7 passed failed=[]                                                 rc=0
```

Three cases are red on the real 9c54c56 artifact and green on the patch. The
other four are controls: `f2-symlink-dir-plain` and `f2-realdir-dot-match`
are green both ways by design; `f2-symlink-dotdot-launder` is green on the
base tool only because the base checked the *given* path with `lstat` (the
lexical variant shown in §2 is red on it, which is why the patch is not
`normpath`-based); `f2-ancestor-symlink-match` pins the no-over-rejection
property that a `realpath == abspath` fix would have broken.

## 5. Regression battery on the patched tool

Run from the lane root against the committed suite bytes (read-only):

```
$ for s in round-17/tripwire/{core,compound,hardening,w2-regressions} \
           round-18/tripwire/{frozen,r18-failsafe}; do
      python3 -I /tmp/tf2/patched.py --selftest .ufo/waves/$s; done
core             9/9 passed failed=[]        rc=0
compound        16/16 passed failed=[]       rc=0
hardening       33/33 passed failed=[]       rc=0
w2-regressions  30/30 passed failed=[]       rc=0
frozen          31/31 passed failed=[]       rc=0
r18-failsafe     1/1 passed failed=[]        rc=0
$ python3 -I /tmp/tf2/patched.py --frozen .ufo/waves/round-18/frozen
MADO_TRIPWIRE_FROZEN: frozen_match           rc=0
```

Identical to the base-tool run of the same six suites (9/9, 16/16, 33/33,
30/30, 31/31, 1/1). Plus the round-19 fragment 7/7 above. 120/120 + 1/1 + 7/7,
no suite regression.

**Receipt parity.** On a `/tmp` copy of `.ufo/waves/round-18/frozen`:

- pristine: `frozen_match`/0; payload equals
  `evidence/final/tripwire-frozen-match.txt` line 3 **modulo `tool_sha256`**
  (patched digest `5cc3924c…` vs receipt `c1ae45a7…`), all input digests and
  `expected_sha256 4f3534ae…` equal.
- one byte appended to `inputs/r15-libinput-events.jsonl`:
  `snapshot_tampered`/2, `error` `snapshot does not match its pin`, and the
  full `inputs` report (one `ok:false`, four `ok:true`) equals
  `evidence/final/tripwire-frozen-tampered.txt` line 3 exactly. The
  `frozen_snapshot` edit therefore did not disturb the tamper path or its
  report shape.

## 6. Merge notes for L1

- `TwFrozenF1.r19.patch` and `TwFrozenF2.r19.patch` apply to the same base in
  that order without conflict (`patch` reports `Hunk #1/#2 succeeded at
  1053/1106 (offset 2 lines)`); F1 touches `validate_reachable`, F2 touches
  `frozen_snapshot` and `run_frozen`, >25 lines apart. The combined tool
  passes the whole `r19-frozen-f1f2` fragment (7/7), the round-18 frozen
  suite (31/31), and the F1+F2 cases concatenated into one `expected.json`
  (13/13, no duplicate names).
- `expected-f1.json` was read only to assemble a `/tmp` merged suite and was
  not modified; the F2 fragment lists only `f2-*` cases.
- The patched tool digest after applying both drafts is
  `7eb41bb1c81b2ef1b73fe6f24d79cb495ae2c00c88d74ecb32026788af53e130`
  (measured; F2-only is `5cc3924c…`).
- Nothing in the patch changes `--scan`; the round-19 C3 baseline re-pin is
  unaffected by it.

## Limits

- I did not run the live gate (`bash tools/mado-verify.sh` without
  `--selftest`/`--regression`), per the host pause; only hermetic selftests
  and `--frozen` on a scratch baseline copy.
- I did not re-run `.ufo/waves/round-18/receipt-check.py` or the provenance
  checker; parity with the final receipts was checked by hand on lines 1-3.
- The prefix walk defends spellings of DIR; it does not attempt to defend a
  coordinated rewrite of a frozen snapshot (round-18 A1/A1c, inherent) or
  permit-waiver designs (A2b/A2c).
- The `f2-dotdot`/`f2-outside` layout, like the round-18 `-target` dirs, is
  fixture substrate rather than a case; it is untested directly.
- Whether `jj` snapshots the new mode-120000 fixtures is asserted from git's
  behaviour and round-18 precedent, not from a jj command (any jj invocation
  snapshots the lane and is forbidden here).

## Installs

none.
