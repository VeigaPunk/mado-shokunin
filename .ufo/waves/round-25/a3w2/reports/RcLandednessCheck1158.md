# RcLandednessCheck1158 — C2 ledger attack on a3w1 `CapLandednessCheck1158`

Seat: `MadoR25A3.RcLandednessCheck1158` (reviewer, wave `a3w2`). Date: 2026-10-23.
Target under review: `.ufo/waves/round-25/a3w1/reports/CapLandednessCheck1158.md` — a3w1's re-run
of `SCORECARD.md:1158` ("landedness check") at base `41cc04c8d593837a0d5078bffaacdaa163d12897`.
Assignment: independently re-derive its ledger line; flag copied-not-run evidence, wrong revision,
overclaim, or missed superseding text. Leaf member; no subagents dispatched.

## 1. Row re-read at base (independent)

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 41cc04c8:SCORECARD.md
  -> 1618 lines, sha256 6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08
```

Byte-count and sha match the report's claim exactly. `:1158` is under
`### Capabilities (round 19)` (heading `:1155`) and reads verbatim:

```
| landedness check | Say whether each cited lane hash is an ancestor of the live remote tip (`LANDED`/`LOCAL_ONLY`/`MISSING`) without fetching or writing | `bash .ufo/waves/round-19/landed-check.sh LANE HASH...`; w1 `LandedCheck.md` (T1-T9 matrix) | 19 |
```

Same row text, same command placeholder form, same evidence pointer as the report quotes.
Script at base: `.ufo/waves/round-19/landed-check.sh`, sha256
`ca1f76b4c19563f44d919b06ee815c3e18e5dd6598304d420d84ec64974ae63c`, 189 lines — matches report §2.
Static read of the script's executed git verbs: `rev-parse [--verify|--path-format … --git-path]`,
`ls-remote`, `cat-file -e`, `merge-base --is-ancestor`; exports `GIT_TERMINAL_PROMPT=0`,
`GIT_NO_LAZY_FETCH=1`, `GIT_OPTIONAL_LOCKS=0`. No fetch/push/ref-update/index verb — consistent with
the row's "without fetching or writing" and the report's risk-2 disclosure.

## 2. Own sandbox re-run (GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset; `timeout 600`, `prlimit --as=4000000000`)

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q \
  /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/rc/CapLandednessCheck1158
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C … checkout -q --detach 41cc04c8   # HEAD = 41cc04c8…
```

All runs `cwd =` the sandbox clone, command form `bash .ufo/waves/round-19/landed-check.sh <LANE> <HASH…>`
— the manifest-frozen form (`{TREE}/.ufo/… {LANE} {REV}`, `exit_ok [0,1]`,
regex `^(LANDED|LOCAL_ONLY|MISSING) {REV}\b`, verified at `41cc04c8:.ufo/waves/round-24/c2/manifest.json`,
entry text matching report §4 verbatim).

### A — LANDED (report's exact hashes), exit 0 — REPRODUCED

```
landed-check.sh: origin/master = fa466833d62d9ddb911cda4243db973511199cad (object present locally)
LANDED 41cc04c8d593837a0d5078bffaacdaa163d12897
LANDED 1ed41fa8301a4562d125503e5b881ec8eb5a1908
LANDED 2896dc4a009ef68f3ef50f0bdcafd6f4aee82a5f
exit=0
```

### B — LOCAL_ONLY (own sandbox-only probe commit), exit 1 — REPRODUCED

Sandbox-only empty commit `9112e1f9e912cb7691d85ccca0652172294947bf` on `master` (clone's
`refs/heads/master` updated; lane untouched):

```
landed-check.sh: origin/master = fa466833d62d9ddb911cda4243db973511199cad (object present locally)
LOCAL_ONLY 9112e1f9e912cb7691d85ccca0652172294947bf (ancestor of refs/heads/master, not of origin/master fa466833d62d9ddb911cda4243db973511199cad)
exit=1
```

Reason-string shape identical to the report's receipt B.

### C — MISSING / non-hex usage, exit 1 / exit 2 — REPRODUCED

```
landed-check.sh: origin/master = fa466833d62d9ddb911cda4243db973511199cad (object present locally)
MISSING deadbeef                       -> exit=1
landed-check.sh: not a hex object name: HEAD   -> exit=2
```

### D — live-lane variant (read-only), exit 0 — REPRODUCED

```
bash .ufo/waves/round-19/landed-check.sh /home/vgpnk/Projects/shokunin/mado-shokunin 41cc04c8
landed-check.sh: origin/master = fa466833d62d9ddb911cda4243db973511199cad (object present locally)
LANDED 41cc04c8d593837a0d5078bffaacdaa163d12897          -> exit=0
```

Independent lane-side read: `git -C <lane> ls-remote origin refs/heads/master` →
`fa466833d62d9ddb911cda4243db973511199cad` (lane origin `https://github.com/VeigaPunk/mado-shokunin.git`);
clone `origin/master` and `refs/heads/master` resolve to the same id. Bare invocation →
`usage: landed-check.sh LANE_DIR HASH...`, exit 2 — matches report risk-4.

## 3. Comparison against the a3w1 ledger line

| field | a3w1 report | this re-derivation | verdict |
|---|---|---|---|
| observed status | works (`LANDED`/`LOCAL_ONLY`/`MISSING` all demonstrated) | same four outcomes, same text shapes | agree |
| exit codes | 0 / 1 / 1 / 2 (+ bare usage 2) | identical | agree |
| key output | `LANDED 41cc04c8d593…` etc.; `LOCAL_ONLY …(ancestor of refs/heads/master, not of origin/master …)`; `MISSING deadbeef`; `not a hex object name: HEAD` | byte-identical message shapes; only the `origin/master` value differs (see §4) | agree |
| command form | `bash .ufo/waves/round-19/landed-check.sh <clone-path> 41cc04c8 1ed41fa 2896dc4`, cwd = clone, base-`41cc04c8` bytes | identical form, identical script sha `ca1f76b4…` | agree |
| superseding pointers | `SCORECARD.md:1581` round-24 re-demonstration row `\| landedness check \| works \| LANDED <rev>, at 8e5d9369 \|` plus supersession sentence; scoped-correction note (12 counted rows) | `:1581` verified verbatim; supersession sentence "supersedes the implied `works` of every earlier row" verified at `:1570` | agree |
| revision | base `41cc04c8`, script sha `ca1f76b4…` | identical | agree |

## 4. Delta found (not a defect): remote-tip drift

The report's stderr lines show `origin/master = 2896dc4a009ef68f3ef50f0bdcafd6f4aee82a5f`; mine show
`fa466833d62d9ddb911cda4243db973511199cad`. Both are true observations at their run time: the lane
master moved between a3w1 and this re-check (`git merge-base --is-ancestor` confirms `2896dc4a` is an
ancestor of `fa466833`). The report explicitly dates its observation and its independent `ls-remote`
receipt matches `2896dc4a` at that time. Drift does not change any verdict (`41cc04c8`, `1ed41fa8`,
`2896dc4a` are all still ancestors of the new tip) — and it confirms the tool resolves the tip live
via `ls-remote` rather than a stale tracking ref, which is the row's core claim. Honest saturation:
the tool prints the tip it read; the report did not freeze-claim the tip.

## 5. Non-defect notes

- **Receipt D lane invocation**: the a3w1 seat ran the script once with the lane as `LANE_DIR`. I
  re-verified the script's executed verb set is read-only (no fetch/push/ref/index write,
  `GIT_OPTIONAL_LOCKS=0`), and my own read-only re-run printed no write. The bound forbids lane
  writes, not read-only probes; the justification in report §receipt-D holds.
- **Report risk-1 sha claims verified independently**: w1 `LandedCheck.md` §1 records sha
  `e6f48348cfd4a3ccdbe681824cff0a1aff1de91e48d0e819f6a3172f6884a07b` = script bytes at `df84807`;
  `git show 61eaa07` diffs exactly one line (`--git-path` → `--path-format=absolute --git-path`)
  producing base sha `ca1f76b4…`. Reported accurately as evidence-artifact drift, not row drift.
- **No copied-not-run indicators**: receipts carry run-specific artifacts (the probe-commit hash
  `559a55db…` is that sandbox's, mine is `9112e1f9…`; both produce identical reason text). Output
  shapes, exit codes and stderr line format all reproduce from live runs, not transcription.
- **No missed superseding text**: case-insensitive whole-file grep at base for `landed|landedness|
  landed-check|F16` lands on `:1063`, `:1118`, `:1151`, `:1158`, `:1581` — the same five the report
  lists, with `:1151`'s F16 narrowing correctly classed as scope-narrowing, not contradiction.

## 6. Cleanup

`rm -rf /fast/scratch/hyaku/mado-r25a3/rc/CapLandednessCheck1158` — clone deleted; `/usr/bin/ls` of
the parent shows it gone (only sibling seats' dirs remain). No process left running; no lane file
written; the only lane-touching command was the read-only `ls-remote`/tool run of receipt D.
Installs: none.

## Verdict

RECHECK CapLandednessCheck1158: agree — all four verdict classes, exit map, reason strings and the
`:1581` superseding pointer re-derive from live runs at base `41cc04c8`; only delta is remote-tip
drift `2896dc4a → fa466833` (lane master moved; report dated its observation correctly; verdicts
unchanged).
