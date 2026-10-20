# ReviewGateF6F9 — partial

Seat `MadoR19.ReviewGateF6F9`, round 19 wave 2, 2026-10-20. Attacked item: the gate's omarchy
git rows (F6 rescue / F9 worktree) and the residual false-PASS surface.

Targets reviewed, both extracted with `git show` and re-hashed:

| bytes | sha256 | role |
|---|---|---|
| `01b80946d92b26370d3012a7da655d00dd135154:tools/mado-verify.sh` | `1036d1004e63d80377faa4f905fd8dc1897eb29b64496cbfef647b47cec4f2af` (4,097 L) | the assigned integrated tip under attack |
| `c7693eb29c1a1969087282aa0601e186e0ae488d:tools/mado-verify.sh` | `071d39d99aa94d9e3d0c0a8c9d9e9e98b4bc79b51af0703e4dba774f85f7c75d` (4,161 L) | current tip (wave-2 integration `61eaa07` landed mid-review and revised exactly these rows; `c7693eb` follows it; worktree clean against it) |

All line numbers below are per-version: `o:` = 01b8094 bytes, `n:` = current bytes.

## Verdict per claim

| claim | verdict |
|---|---|
| "F6 rescue only with `.jj`" | **holds literally at both tips** (`o:3722-3723` / `n:3779`), but at the assigned tip the `.jj` test is presence-only and a bare `mkdir .jj` in a plain-git tree flips the rescue on (F1) — the marker proves nothing about jj management |
| "plain-git detached HEAD reports MOVED" | **false as stated at 01b8094** (F1, measured: detached at an unpinned commit + empty `.jj` dir → both rows PASS); **true at current tip** except for a content-identical detached HEAD under a stale `.jj` (F2, measured) |
| "F9 worktree `.git` file evaluates" | **holds**, verified with REAL git worktrees, not only the stub (F5) |
| "any remaining false PASS path?" | **yes — two**, both measured (F2, F3) |

## Findings

### F1 (HIGH at 01b8094; CLOSED at 61eaa07) — `.jj` presence alone rescued a real MOVED

At the assigned bytes the rescue's only gate is `[ -d "$tree/.jj" ]` (`o:3722-3723`). The gate's
own fixture admits the marker is content-free — `build_fixture` creates it with bare
`mkdir -p … "$OMR/.local/share/omarchy/.jj"` (`o:655`, comment `o:656-658`: "`.jj` marks the
checkout as jj-colocated"). Measured consequence, running the gate's exact extracted block
(`o:3722-3776`, mechanically sed-extracted, not transcribed) against a real plain-git repo
(master/tag v3.8.4/pin at C1=`4c28c21d`, HEAD detached at C2=`60902b09`, leaf unchanged):

```
(a) detached at C2, NO .jj:
  omarchy  omarchy.git.tag   UNKNOWN  git describe failed (rc=128) — tag pin unverified
  omarchy  omarchy.git.head  FAIL     MOVED: HEAD → '60902b09b7e4508c1596d416e02673c3a9f46172' != pin 4c28c21d…
(b) SAME detached state, EMPTY .jj dir only:
  omarchy  omarchy.git.tag   PASS     HELD: v3.8.4 exactly at refs/heads/master (P3 pin)
  omarchy  omarchy.git.head  PASS     HELD: 4c28c21d at refs/heads/master (P3 pin)
```

Case (b) is a silent false PASS: HEAD/worktree sit on an unpinned commit, both identity rows
read HELD. The jj-w1 incident produced exactly this artifact class in the fleet root (leftover
`.jj` after jj removal; JjAuditMado §0.2-§0.4 repaired it with `rm -rf .jj`) — so a stale marker
is not hypothetical. `61eaa07` closes this: the rescue is now double-gated on
`HEAD^{tree} == <tip>^{tree}` (`n:3793-3800`, comment `n:3787-3792` cites CriticAdmission), and
my re-run of the identical scenario against the current bytes reads MOVED:

```
(1) stale .jj, detached at NON-empty C2=16c5df2b  →
  omarchy  omarchy.git.head  FAIL  MOVED: HEAD → '16c5df2bff8d4a0ac50f12f760e5e0afd7906735' != pin 4354e29a…
```

The stub also gained per-verb rc knobs (`n:689-741`) and OM16/OM17 pin both directions
(`n:1003-1025`, `n:1027-1050`); selftest on current bytes: `MADO_SELFTEST: 452/452 assertions
passed`, rc 0. On the assigned bytes: `MADO_SELFTEST: 443/443 assertions passed`, rc 0.

### F2 (LOW, OPEN at current tip) — stale `.jj` + content-identical detached HEAD still reads HELD

The new tree-equality gate compares trees, not ancestry or commit identity. A detached HEAD at
an EMPTY commit (tree byte-identical to the branch tip's tree) plus any `.jj` directory — a
state plain git produces with `git commit --allow-empty` and a leftover marker — still rescues:

```
(2) stale .jj, detached at EMPTY E=365745a5 on tip; tree(HEAD)=tree(master)=91ef90149e0d  →
  omarchy  omarchy.git.tag   PASS  HELD: v3.8.4 exactly at refs/heads/master (P3 pin)
  omarchy  omarchy.git.head  PASS  HELD: 4354e29a at refs/heads/master (P3 pin)
```

HEAD=`365745a5` ≠ pin `4354e29a`, yet the head row reads HELD at refs/heads/master. The gate's
own comment declares exactly this shape "allowed" (`n:3787-3792`: "only for an EMPTY
working-copy commit on top of the single branch tip, proven by HEAD^{tree} == <tip>^{tree}") —
so for a genuinely jj-managed tree it is by design. What the design cannot do is distinguish a
jj-owned `.jj` from a stale one: the marker test is unchanged and content-free (`n:3779`).
Consequences are bounded: the worktree is byte-identical to the pin, so `omarchy.skill.sha`
(P4) and `omarchy.skill.vs_head` stay true; the residual exposure is commit-identity semantics —
"a real MOVED is never hidden" (`n:3791-3792`) holds only under a content definition of MOVED,
not the commit-sha definition the pre-round-19 rows used. Ancestry is also never checked: E
need not descend from the tip (two diverged empty-commit chains with equal trees rescue
identically). Fix direction, if wanted: require `git merge-base --is-ancestor HEAD <tip>` (or
`HEAD^ == <tip>`) in addition to tree equality — still read-only — or verify `.jj` is a real jj
store (e.g. `.jj/repo/store` exists) instead of any directory.

### F3 (LOW, OPEN at both tips) — identity rows read HELD on a bare repository (no working tree)

F9's fix replaced `[ -d "$tree/.git" ]` with `git rev-parse --git-dir` (`o:3347` → `n:3740-3741`).
That probe returns rc 0 for a BARE repository too, and `symbolic-ref HEAD` works there, so both
identity rows evaluate — and can read HELD — on a repo with no working tree at all:

```
(4) bare clone (no worktree, .git not even a subdir; rev-parse --git-dir rc=0)  →
  omarchy  omarchy.git.tag   PASS  HELD: v3.8.4 exactly at refs/heads/master (P3 pin)
  omarchy  omarchy.git.head  PASS  HELD: 4354e29a at refs/heads/master (P3 pin)
```

No plane-level false PASS results: the vs_head guard `[ ! -f "$leaf" ]` reads UNKNOWN
(`n:3842-3843`) and the link/leaf rows FAIL on a missing checkout, so the plane verdict stays
DIVERGED. The overclaim is confined to the two rows' "checkout identity" wording reading
refs of a worktree-less repo. The pre-F9 code read a bare repo as "no git checkout" (UNKNOWN).
Plausibility of `$ROOT/.local/share/omarchy` being bare is low [INFERENCE]; recorded because the
item asks for remaining false-PASS paths in these rows.

### F4 (NOTE) — vs_head still anchors on `HEAD:`, not the resolved `$tip`; dead guard arm

`omarchy.skill.vs_head` hashes `git show HEAD:$OMARCHY_SKILL_REL` (`n:3852-3853`) while the
identity rows now read the branch tip. Under jj colocation git HEAD is the working-copy commit
`@`, so "worktree == HEAD blob (… no local edit)" is relative to `@`, not to the pin; a
colocated in-progress edit rides in `@` and vs_head reads PASS — caught instead by
`omarchy.skill.sha` (P4), so the plane stays honest. On a plain-git tree the HEAD anchor is the
correct, stricter reading. Separately, the `elif [ -z "$blob" ]` arm (`n:3856-3857`) is dead
code: with `set -o pipefail` any producer failure sets rc≠0 (first arm), and rc=0 implies a
64-hex digest, never empty. Cosmetic. F10 itself is properly fixed: measured via the stub rc
knob, `STUB_GIT_SHOW_RC=128` → UNKNOWN "cannot read HEAD:default/omarchy-skill/SKILL.md
(rc=128)" with no "local edit" text (fixture OM9, `n:863-878`).

### F5 — F9 verified with real git worktrees (beyond the stub OM12)

```
$ git worktree add -b wtbranch …/linked <pin>      # .git is a FILE there (isfile=True, isdir=False)
$ git -C …/linked rev-parse --git-dir              # rc=0
  omarchy  omarchy.git.tag   PASS  HELD: v3.8.4 exactly at refs/heads/wtbranch (P3 pin)
  omarchy  omarchy.git.head  PASS  HELD: 79508cf9 at refs/heads/wtbranch (P3 pin)
$ git worktree add --detach …/linked2 HEAD         # detached at unpinned C2
  omarchy  omarchy.git.head  FAIL  MOVED: HEAD → 'a8d637bd26add925ef8ed20879dfe0106f53db52' != pin 79508cf9…
```

Attached worktree evaluates and names the branch it read; detached worktree keeps the honest
MOVED (no `.jj` in a linked worktree, so no rescue). Matches and extends JjAuditMado F9.

## Comparison with JjAuditMado (hyaku/jj-w1)

| old finding | status at current tip |
|---|---|
| F6 (colocated empty `@` → tag UNKNOWN + false head MOVED) | fixed; rescue double-gated, OM11/OM16/OM17 pin all three directions (`n:967-1050`) |
| F9 (`.git`-file worktree blinded) | fixed (`n:3740-3741`); verified with real worktrees (F5) + OM12/OM13 |
| F10 (vs_head rc discarded → false "local edit") | fixed (pipefail, `n:3852-3853`; OM9) |
| F14 (stub cannot fail → UNKNOWN arms untested) | fixed (per-verb `STUB_GIT_*_RC`/DETACHED/BRANCHES knobs, `n:689-741`; OM9/OM10A/OM10B/OM13/OM14/OM15) |
| — (new surface introduced by the fix) | F2 and F3 above — not present in the old report |

## Verification performed

- Extracted both gate versions with `git show` (shas above); no lane edits, no git/jj writes in
  the lane, no jj commands anywhere.
- `bash <bytes> --selftest` on both versions: 443/443 (01b8094) and 452/452 (c7693eb), rc 0.
- F6/F9/rescue matrix: real-git sandbox repos driven through the gate's exact block, sed-
  extracted by line range from the committed bytes (harness + block under `/tmp/r19f6f9-demo*`,
  `/tmp/r19f6f9-wt`); outputs quoted above. The ad-hoc root path through the gate binary was NOT
  exercised (forbidden without `--selftest`/`--regression`); the block is the entire tag/head
  decision surface (`n:3774-3840`), and `row`/`tmo`/pins were the only harness-supplied values.
- jj working-copy shapes were simulated by git states (detached HEAD, empty commits, a `.jj`
  directory) because jj itself is forbidden to me. That simulation is exact for the gate's
  observations — which is F2's point: nothing the gate reads distinguishes the two.

## Limits

- The `.jj`-owned-vs-stale distinction (F2) is untestable without jj in a live repo (forbidden);
  the residual hole is bounded by tree equality and measured, not conjectured.
- The lane moved under me (`61eaa07` wave-2 integration, then `c7693eb`); findings are labeled
  per byte-version and the two open items were confirmed against the current tip.
- LFS/filter interaction with `git show HEAD:…` (JjAuditMado §6) untouched here — no
  `.gitattributes` exists to trigger it [INFERENCE].

## Installs

None.
