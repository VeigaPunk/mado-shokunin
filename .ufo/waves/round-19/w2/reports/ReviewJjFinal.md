# ReviewJjFinal — partial

Seat `MadoR19.ReviewJjFinal` (reviewer, leaf). Target: final disposition of jj-audit
F6/F9/F16/F17 at `01b80946d92b26370d3012a7da655d00dd135154` (lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`, read-only). Source findings:
`/home/vgpnk/.ufo`-external `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMado.md:190,224,310,322`.
Attack result: **F6 fixed, F9 narrowed (not fixed), F16 fixed, F17 operator-owned.**
The assignment's "F6/F9 by the gate diff" is true mechanically (the diff changes both
preconditions) but F9's landed form is the exact shape the round-18 review rejected, and I
reproduced its failure mode on this host's layout. Everything else holds under independent
re-execution.

## Disposition table

| ID | Finding (audit, one line) | Landed change at `01b8094` | Verdict | Evidence |
|---|---|---|---|---|
| F6 | After `jj new`, git HEAD detaches onto an empty working-copy commit; tag row UNKNOWN, head row false FAIL | Gate reads the branch tip, rescuing detached HEAD **only** when `$tree/.jj` exists; plain-git detached keeps the HEAD reading | **fixed** | baseline `tools/mado-verify.sh:3456` (`rev-parse HEAD`) → tip `:3725` (`symbolic-ref -q HEAD`), `:3727` (`[ -d "$tree/.jj" ]`), `:3733` (`for-each-ref refs/heads`), tip describe `:3763`; selftests OM10A/OM10B/OM11/OM12/OM13/OM14 at tip `:874-967`; my independent selftest run below |
| F9 | `[ -d "$tree/.git" ]` precondition misses git worktrees (`.git` is a FILE) | Precondition replaced by `git -C "$tree" rev-parse --git-dir` | **narrowed** — worktree blindness fixed, but a `.git`-less tree under any ancestor repo is now read as that ancestor's checkout (false identity rows). Round-18 rejected this exact form (R3); the safe `[ -e "$tree/.git" ]` was not used | tip `tools/mado-verify.sh:3687`; probe below; `ReviewJjDispositionFinal.md:130` (round-18 `w2/reports/`) |
| F16 | No lane tool checks landedness; lane was 8 ahead of origin | `landed-check.sh` (read-only, live `ls-remote`, no fetch/write/jj) committed at the tip | **fixed** (tool works; independently reproduced) — with two caveats: no lane-produced receipt exists yet, and its repo test shares F9's upward-discovery shape (fail-safe: exits 2, never a false LANDED) | tip blob `fb4c732c` (mode 100755); runs below |
| F17 | The lane repo is already colocated and jj has been run in it | Colocation declared structural under `HYAKU_VCS=jj` (`.ufo/waves/round-19/w1/reports/JjIncidentScan.md`) | **operator-owned** (holds) — removal requires an operator change to `HYAKU_VCS` and the closure wrapper, both outside lane write scope; verified from primary bytes below | `scripts/hyaku/hyaku.env:10`; `scripts/hyaku/inline.sh:38,90,145`; `.jj` bytes |

## Attack, commands, outputs

### 1. Gate bytes and attribution

- Tip gate extracted to scratch: `git show 01b80946…:tools/mado-verify.sh` → sha256
  `1036d1004e63d80377faa4f905fd8dc1897eb29b64496cbfef647b47cec4f2af` (blob `45357874`).
- Baseline (9c54c56) gate: `:3412 [ -d "$tree/.git" ] && omtree=1`, `:3456 gh=$(… rev-parse HEAD …)`
  — the audit's F9/F6 code, confirming the gate diff is the vehicle for both.
- Tip F6/F9 block: `:3687 if have git && tmo git -C "$tree" rev-parse --git-dir >/dev/null 2>&1;`
  `:3725 symbolic-ref -q HEAD`, `:3727 [ -d "$tree/.jj" ] && jcol=1`, `:3733 for-each-ref
  --format='%(refname)' refs/heads`; plain-git detached keeps `tipref="HEAD"` (`:3752-3754`).
  Semantics check: a git-attached HEAD always equals its branch tip, so the tip-based read
  changes only the jj-detached case — no over-claim there.

### 2. Independent gate selftest (permitted mode)

```
$ /tmp/gate_tip.sh --selftest      # bytes of blob 45357874
MADO_SELFTEST: 443/443 assertions passed
exit=0        (12.9 s)
```
Matches the assignment's 443/443. The red-before in
`.ufo/waves/round-19/evidence/gate-swap-receipt.txt` (383 passed / 6 failed at `df84807`,
exit=2) is the hybrid old-gate fixture receipt and is consistent with SCORECARD:1043.

### 3. F9 — regression reproduced (the load-bearing finding)

Fixture mimicking `$HOME/.git` (this host has a real dotfiles repo at `/home/vgpnk/.git`,
verified `drwxr-xr-x 1 vgpnk vgpnk … /home/vgpnk/.git`), same filesystem, valid ancestor repo,
tree with **no** `.git`:

```
$ git init -q /tmp/r19f9/home/wt && git -C /tmp/r19f9/home/wt commit -q --allow-empty -m seed
$ mv /tmp/r19f9/home/wt/.git /tmp/r19f9/home/.git && mkdir -p /tmp/r19f9/home/tree
$ git -C /tmp/r19f9/home/tree rev-parse --git-dir ; echo rc=$?
/tmp/r19f9/home/.git
rc=0                                  ← tip gate :3687 accepts: omtree=1
$ [ -d /tmp/r19f9/home/tree/.git ]; echo rc=$?
rc=1                                  ← baseline gate correctly said "no git checkout"
```

Consequence on the real host: if the omarchy checkout (currently a normal `.git` directory at
`/home/vgpnk/.local/share/omarchy/.git`; no `.jj` there) ever loses its `.git`, the live rows
would evaluate **`~/.git`** (the dotfiles repo) and emit misattributed pins — a false
`MOVED: … != pin` naming the wrong repository. The OM13 no-repo selftest (`:951-954`) cannot
see this: its fixture lives under mktemp in `/tmp` with no ancestor repo, so 443/443 is green
while the hazard is live. Round-18's own review prescribed `[ -e "$tree/.git" ]`
(`.ufo/waves/round-18/w2/reports/ReviewJjDispositionFinal.md:130` "R3 REJECTED — upward
discovery to `~/.git`"); round 19 landed the rejected form and `corpus/lessons/round-19.md:61`
records "F9 `rev-parse --git-dir`" without noting the overridden rejection.

The same primitive is landed-check.sh's repo test:

```
$ .ufo/waves/round-19/landed-check.sh /tmp/r19f9/home/tree 01b80946…
landed-check.sh: git ls-remote origin refs/heads/master failed in /tmp/r19f9/home/tree
rc=2                                  ← passed "not a git checkout", failed later, wrong cause named
```

Fail-safe (exit 2; no false LANDED is reachable — a LANDED verdict additionally requires the
hash to be an ancestor of that repo's origin tip, i.e. essentially the same object store), but
the diagnostic names the wrong failure.

### 4. F16 — landed-check.sh independently exercised on the live lane

Read-only (per its header: no fetch, no write, no jj; `GIT_TERMINAL_PROMPT=0`,
`GIT_NO_LAZY_FETCH=1`, `GIT_OPTIONAL_LOCKS=0`, `timeout 60` on `ls-remote`).

```
$ .ufo/waves/round-19/landed-check.sh $M 01b80946d92b26370d3012a7da655d00dd135154
landed-check.sh: origin/master = 61eaa071161e401a370fbdc3000de1cfbf99e1cd (object present locally)
LANDED 01b80946d92b26370d3012a7da655d00dd135154

$ .ufo/waves/round-19/landed-check.sh $M 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d 61eaa071161e401a370fbdc3000de1cfbf99e1cd ; echo rc=$?
… LANDED 9c54c56a… / LANDED 61eaa071…
rc=0

$ BLOB=$(git -C $M rev-parse HEAD:SKILL.md); … $M "$BLOB" 0000000000000000000000000000000000000000
LOCAL_ONLY bbb8aa67… (object present but not a commit)
MISSING 0000000000000000000000000000000000000000
rc=1
```

Exit map matches the header doc (0 all landed / 1 any not-landed / 2 could-not-evaluate). My
first probe passed a bad 8-char prefix (`9c54c56b`) and got an honest `MISSING` — probe error,
not a tool defect. The remote tip moved between my two runs (`61eaa071` → `6963d34b`); the
tool re-resolves live each run, as designed. Caveats: (a) **no lane-produced landedness
receipt exists** — `ls .ufo/waves/round-19/evidence/` has none, and LOG.md at the tip has no
round-19 entry naming F16; the lane still owes one receipt at closure (round-18
CriticJjDisposition.md:177). (b) the repo-test misattribution in §3.

### 5. F17 — structural colocation re-verified from primary bytes

```
$ sed -n 10p /home/vgpnk/Projects/shokunin/scripts/hyaku/hyaku.env
HYAKU_VCS=jj
$ grep -n lane_vcs_init /home/vgpnk/Projects/shokunin/scripts/hyaku/inline.sh
38:lane_vcs_init() { # lane cwd — colocate an idle lane (dispatch/closure time only)
90:  lane_vcs_init "$lane" … || die "jj init failed for $lane"
145:  lane_vcs_init "$lane" … || die "jj init failed for $lane"
$ stat -c '%n %y' $M/.jj $M/.jj/repo/config-id $M/.jj/repo/store/git_target
.jj                              2026-10-20 12:18:08.072… -0300   (= 15:18:08Z)
.jj/repo/config-id               2026-10-20 12:18:08.082… -0300
.jj/repo/store/git_target        2026-10-20 12:18:08.062… -0300   → ../../../.git (colocated)
$ ls $M/.jj/repo/op_store/operations | wc -l
91
```

Matches JjIncidentScan's timeline (helper re-init at 15:18:08Z) and its invariants. Op store
is now 91 files vs the report's time-bounded "68 ops … to 16:59:54" — helper has kept writing
(the wave-2 commits); no contradiction with the report's bounded claim. Spot-check of the
scan's transcript citation, count-only, no line copied into the lane:
`…01a156ff…/MadoR14/MadoR14.AttackCoverage.jsonl` line 42 contains
`jj file annotate .ufo/waves/round-13/w1/globals.json …` — matches the scan's redacted
excerpt (1 hit).

Disposition confirmed: with `HYAKU_VCS=jj` and `inline.sh` re-initializing on every
dispatch/closure, a "remove `.jj`" remediation is unsatisfiable from the lane — operator/
fleet-owned. The enforceable residue is the scan's invariant set (no non-helper `jj` in the
lane, no direct git write verbs post-cutover, helper `commit` only on sanctioned paths,
`jj-lane.sh state` = read). One guardrail the scan itself states and I endorse: the current op
store cannot witness pre-15:18:08Z history; F17's audit-era evidence lives only in
JjAuditMado.md and the transcripts.

## Limits

- I did not re-run JjIncidentScan's full 3.5 GB transcript scan; "no non-helper jj/git write
  verb after 15:18:08Z" is accepted on its cited rows plus my byte-level corroboration of the
  structure that makes re-init automatic. Post-scan-window op-store growth (91 files) is
  consistent with helper-only commits but is not op-by-op verified [UNK].
- The F9 false-row end-to-end (gate actually emitting a MOVED row against `~/.git`) was not
  executed: running the gate outside `--selftest`/`--regression` is forbidden, and the
  live-arm fixture cannot point at `$HOME` from a selftest. The demonstration stops at the
  precondition primitive (`rev-parse --git-dir` rc=0 on a `.git`-less tree), which is the
  exact guard at `tools/mado-verify.sh:3687`.
- `landed-check.sh` was exercised on the live lane and on /tmp fixtures only; its
  shallow-clone warning path and the `refs/heads/master`-absent arm are code-read, not run.
- The omarchy checkout's `.git` health was checked by `ls -ld` only (host files read as bytes);
  its internal state was not opened.
- LOG.md at the tip carries no round-19 entry yet (wave 2 in flight), so the lane's own
  prose disposition of these four items does not exist as of `01b8094`; this report is the
  disposition source until integration writes it.

## Installs

none.
