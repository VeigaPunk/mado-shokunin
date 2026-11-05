# R88MExecForgery — forgery rejection through both round-88 counter CLIs

Seat: executor (leaf), round mado 88 wave w1. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base revision `24ba2a9ddac21c1211579231e6ee1d98963f9988`.

Scratch: `/fast/scratch/hyaku/mado-r88/R88MExecForgery` — **removed on exit** (verified below).
No tool installs; no pacman transaction; no host file read outside the named sources.

## 1. Fixture and pins

Fixture repo `D=/fast/scratch/hyaku/mado-r88/R88MExecForgery/tmp.Er3IE0BpcN`, created with
`git -C "$D" init -q`; `git -C "$D" rev-parse --show-toplevel` printed exactly `$D` before the first
commit. All commits are inside `$D`; no mutating git command ran in the lane.

The lane's control files were revised mid-wave (declaration draft revisions 1–5, timestamps 16:12–16:14),
so the fixture was rebuilt on the current bytes. Final commit chain:

| commit | content | `tools/mado-mako.py` sha256 |
|---|---|---|
| `866f6e95f991f7a56364b326cb4b3181d2e25b17` | **base tool** + revision-5 controls | `67a955a5fa06135c2748855b7e452bd3f0792c540002009ec90842ee5c986698` |
| `968327f60cee97a735f6cb57eca2a74503efd9f4` | forgery (b) echo-defaults | `577cb54dd97760e67528a0ebf2409e4962e4bf6b67b22057e4349690ef4d7e34` |
| `1e8dfaf782d584dee571d9beea047e65d15c31a6` | forgery (c) refuse-everything | `3e33d0ad1ba3eefebe311766ae9553a1cb710b0179d35d0e85273f4414a360b8` |
| `641cc68924d5f8b92bbe7e652ab2b597e1752114` | forgery (e) refuse-every-include | `06c15649c1a205ce5a7b2efc18e68e2c3d1d398551ce1ea8154afb562befea32` |
| `7b8a6b4254c9f9f782230841c25ce3d945cea0c0` | forgery (f) read-every-include | `3683878bca1ce19fa43074249d9441e643857ab25e239415805eb090ad5718ac` |
| `36f246093db22250e0187707c54d0359ec64a078` | diagnostic: echo-defaults + anchors | `f74b19cee20911203c7a31b266ad21ddbc29443f495e5696bda39874b4293350` |
| `147b1344a18fb26afdb8f9acb816498948fd37a2` | diagnostic: refuse-every-include + anchors | `3f9ed28cd81ae2207b7f79ed749b4c713054c0988fdc7ff6a7590ed97620237c` |

Control bytes committed in every commit above (read back with `git show <commit>:<path> | sha256sum`):

- `.ufo/waves/round-88/controls/mako-mutants-r88.json` — `2a569770aa255cfaf0afc15c63136e8c261396ca280d5646c51171e9009864a1` (M=22)
- `.ufo/waves/round-88/controls/containment-mutants-r88.json` — `ff76cd698875cfc1eff6f36d5997e3df79e3ef694c22c4feb720885179403616` (M=7)
- `.ufo/waves/round-87/controls/mako-cases-r87.json` — `0a9558743a721f70bb64b48d188b375f1468a140b00ca75ac93ab59c316d5fe3`

Case files copied into `$S` and used from there:

- `mako-cases-r88.json` — `818b2bfce97b5f5c4f98ad1afc69775608af4ffd1ee4c272f0619cc4e0886ff1` (59 cases, `mako-cases-r88-v1`)
- `containment-cases-r88.json` — `8b16c0cb0d73eb2e245b4b543db0a0396c824314cb8dbd26e5ad26214f20d039` (26 cases, `mako-containment-r88-v1`)

Counters actually executed (lane path, current revision at run time):

- `quality/counters/c1-r88-mako-fields.py` — sha256 `3678425addb5f661d3f284ef423e3566446b54714cb2148c5696a8cdfe11cc1f`
- `quality/counters/c2-r88-include-containment.py` — sha256 `f8e18b7c915fe831e6eaafcd09fad0af9ac23d89514317f131fb1ed409e96767`

The counters were revised during the wave (draft revisions 1–5): they now require every mutant anchor
and their own derived-control anchor to occur exactly once in the measured tool, and refuse otherwise
with exit 2. That changes the expected outcome for tools that are not candidate-derived (see §3).

## 2. Required forgeries — table

Command shape (lane root; `D` = fixture, `S` = scratch):

```
python3 -I quality/counters/c1-r88-mako-fields.py --repo "$D" --rev <forgery> --base-rev 866f6e9… \
  --cases "$S/mako-cases-r88.json" --expect-cases-sha256 818b2bfc… \
  --expect-mutants-sha256 2a569770… --expect-r87-cases-sha256 0a955874… --scratch-root "$S"

python3 -I quality/counters/c2-r88-include-containment.py --repo "$D" --rev <forgery> --base-rev 866f6e9… \
  --cases "$S/containment-cases-r88.json" --expect-cases-sha256 8b16c0cb… \
  --expect-mutants-sha256 ff76cd69… --scratch-root "$S"
```

| # | forgery (commit) | counter / cases | final verdict line | rc |
|---|---|---|---|---|
| a | base tool (`866f6e9`) | C1 / authored `818b2bfc…` | `MADO_MAKO_FIELDS: SETUP_ERROR c51-boolean-mismatching-flag.args: unknown or non-object args` | 2 |
| b | echo-defaults (`968327f`) | C1 / authored `818b2bfc…` | same line (case-file defect, §4) | 2 |
| c | refuse-everything (`1e8dfaf`) | C1 / authored `818b2bfc…` | same line (case-file defect, §4) | 2 |
| a′ | base tool (`866f6e9`) | C1 / diagnostic copy `a00d50c3…` | `MADO_MAKO_FIELDS: SETUP_ERROR mutant M11-string-mismatch-ignored: anchor occurs 0 times in the measured tool` | 2 |
| b′ | echo-defaults (`968327f`) | C1 / diagnostic copy `a00d50c3…` | `MADO_MAKO_FIELDS: SETUP_ERROR mutant M01-criteria-setdefault: anchor occurs 0 times in the measured tool` | 2 |
| c′ | refuse-everything (`1e8dfaf`) | C1 / diagnostic copy `a00d50c3…` | same M01 line | 2 |
| d | base tool (`866f6e9`) | C2 / authored `8b16c0cb…` | `MADO_MAKO_CONTAINMENT: SETUP_ERROR forgery anchor 'if not self.within_roots(real):' occurs 0 times` | 2 |
| e | refuse-every-include (`641cc68`) | C2 / authored `8b16c0cb…` | `MADO_MAKO_CONTAINMENT: SETUP_ERROR mutant K3-prefix-without-separator: anchor occurs 0 times in the measured tool` | 2 |
| f | read-every-include (`7b8a6b4`) | C2 / authored `8b16c0cb…` | same K3 line | 2 |

No run produced `TARGET_MET`. Every required forgery was rejected (rc 2, never a verdict). Rows a′–c′
are the same forgery bytes scored against a scratch copy of the authored case file with only the §4
typo corrected; they show the forgery-specific anchor rejection that the authored file's load failure
masks.

### Why each setup error is the correct rejection

- (a) base tool: the C1 counter checks the 22 mutant anchors in order. M01–M10 are carried from r87 and
  are present in the r87 resolver; the first new anchor, `M11-string-mismatch-ignored`
  (`mismatch = mismatch or have != value`), occurs 0 times → setup error. Reproduced with the
  diagnostic case copy (§3): `SETUP_ERROR mutant M11-string-mismatch-ignored: anchor occurs 0 times in
  the measured tool`, rc 2.
- (b)/(c): the C1 counter requires the 22 mutant anchors and the two `inputs-ignored` anchors
  (`self.inputs = dict(inputs or {})`, `self.flags = dict(flags or {})`) exactly once; a standalone
  echo/refuse tool carries none of them → `SETUP_ERROR mutant M01-criteria-setdefault: anchor occurs 0
  times`, rc 2 (diagnostic copy).
- (d) base tool: the C2 counter first requires the derived-control anchor
  `if not self.within_roots(real):` exactly once; the r87 resolver has no containment code → 0 times,
  rc 2.
- (e)/(f): the C2 counter next requires all 7 containment mutant anchors exactly once. Both forgeries
  carry K1's anchor (`if not self.within_roots(real):`) and K2's
  (`real = os.path.realpath(target)`), but not K3's
  (`if real == root or real.startswith(prefix):`) → `SETUP_ERROR mutant K3-prefix-without-separator:
  anchor occurs 0 times in the measured tool`, rc 2.

## 3. Diagnostic: a forgery that passes the anchor gate is scored and rejected

To show the scoring path itself (not only the setup gate) rejects a forgery, the same two tools were
re-committed with the required anchor strings carried as comments only (no behaviour change):
`36f2460` (echo-defaults + 24 anchor comments) and `147b134` (refuse-every-include + 2 anchor comments).

| forgery | counter | final verdict line | rc |
|---|---|---|---|
| echo-defaults + anchors (`36f2460`) | C1 | `MADO_MAKO_FIELDS: TARGET_MISSED rev=36f2460… cases=59 correct=5 carried=22/22 mutants=22 killed=0 naive_correct=13 globals_include_correct=14 base_tool_correct=33 inputs_ignored_correct=5 score=0.8475 tool_sha256=f74b19ce… cases_sha256=a00d50c3…` | 1 |
| refuse-every-include + anchors (`147b134`) | C2 | `MADO_MAKO_CONTAINMENT: TARGET_MISSED rev=147b134… cases=26 correct=14 mutants=7 killed=1 base_tool_correct=11 refuse_all_includes_correct=14 score=5.3846 tool_sha256=3f9ed28c… cases_sha256=8b16c0cb…` | 1 |

The C1 diagnostic run used the corrected case copy `mako-cases-r88.diag-fixed.json`
(sha256 `a00d50c3dfa9e0b87b54a70fe5236477eb19f8f8875057dea4c67592fd86e016`), because the authored file
does not load (§4). Both forgeries score far below N/K, kill no/few mutants, and are `TARGET_MISSED`.

## 4. Finding — the authored C1 case file does not load (blocks the real C1 forgery run)

- File: `.ufo/waves/round-88/controls/mako-cases-r88.json:1021`
- Case `c51-boolean-mismatching-flag` has `"exiring": "false"` where the schema allows only
  `app-name, app-icon, summary, body, category, desktop-entry, urgency, actionable, expiring, mode`.
- Reproducing input: the C1 counting command above with `--cases …/mako-cases-r88.json`
  (`--expect-cases-sha256 818b2bfc…`). Output:
  `MADO_MAKO_FIELDS: SETUP_ERROR c51-boolean-mismatching-flag.args: unknown or non-object args` (rc 2).
- Consequence: no C1 forgery can be scored against the authored file until the typo is fixed. With a
  scratch copy that renames only that key (`exiring` → `expiring`), the same file loads with
  `cases=59 carried=22/22` and the three C1 forgeries reach their anchor checks (§2). The fix belongs
  to the case author / L1; this seat did not edit the lane file.
- The other 58 cases pass the counter's argument-name scan (checked with a local Python scan).

## 5. Selftests (current counters, `--scratch-root "$S"`)

```
$ python3 -I quality/counters/c1-r88-mako-fields.py --selftest --scratch-root "$S"
SELFTEST: passed=40/40          # rc 0
$ python3 -I quality/counters/c2-r88-include-containment.py --selftest --scratch-root "$S"
SELFTEST: passed=28/28          # rc 0
```

## 6. Superseded runs (recorded, not the current evidence)

Before the 16:14 counter revision, the C2 counter (sha256 `0a08978d4b9f48ca48b01fe1585bb746f2628a5fc1761e5d440e420b856f9bbb`)
on the then-current 17-case file (sha256 `3ee0dc9b…`) gave:

| forgery | verdict line | rc |
|---|---|---|
| base tool | `MADO_MAKO_CONTAINMENT: SETUP_ERROR forgery anchor 'if not self.within_roots(real):' occurs 0 times` | 2 |
| refuse-every-include | `MADO_MAKO_CONTAINMENT: TARGET_MISSED … cases=17 correct=8 mutants=5 killed=1 base_tool_correct=8 refuse_all_includes_correct=8 score=4.7059` | 1 |
| read-every-include | `MADO_MAKO_CONTAINMENT: TARGET_MISSED … cases=17 correct=10 mutants=5 killed=0 base_tool_correct=8 refuse_all_includes_correct=8 score=5.8824` | 1 |

Those bytes are superseded by draft revisions 2 and 5; they are kept only as evidence that when a
forgery gets past the setup gate the scoring path rejects it.

## 7. Dead step and correction

First fixture build committed the working-tree tool (the last forgery) into the "base" commit, so the
base run measured `tool_sha256=3683878b…` instead of the base tool. Fixed by restoring
`git show ec3184b:tools/mado-mako.py` (sha `67a955a5…`) into a new commit `866f6e9`; every run in §2–§3
uses `--base-rev 866f6e9…`. The erroneous runs are `run2-c2-*.log` in scratch (now deleted) and are not
cited as evidence.

## 8. Scratch removal

`rm -rf -- "$S"` was executed after the receipts above were transcribed; `test -e "$S"` reports absent.

## 9. Commands and exit codes (summary)

- `git -C "$D" init -q`, `git -C "$D" rev-parse --show-toplevel` → 0 (printed `$D`)
- `git -C "$D" add -A && git -C "$D" commit -q …` (7 commits) → 0
- C1 forgery runs (a)(b)(c) on authored cases → rc 2 each
- C1 forgery runs (a)(b)(c) on diagnostic corrected copy → rc 2 each
- C1 anchored diagnostics → rc 1 each
- C2 forgery runs (d)(e)(f) → rc 2 each
- C2 anchored diagnostic → rc 1
- C1 selftest → rc 0 (`passed=40/40`)
- C2 selftest → rc 0 (`passed=28/28`)
- `rm -rf -- "$S"` → 0; `test -e "$S"` → 1 (absent)
