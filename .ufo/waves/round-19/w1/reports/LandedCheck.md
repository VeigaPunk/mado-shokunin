# LandedCheck — read-only landedness gate implemented; hermetic matrix fully green and both lane hashes LANDED at origin/master 17661e0

Seat: `MadoR19.LandedCheck` (jj audit F16 / recommendation R4). Date: 2026-10-20.
Deliverable: `.ufo/waves/round-19/landed-check.sh` only (plus this report). No other lane file was written.

## 1. Deliverable

```
$ sha256sum .ufo/waves/round-19/landed-check.sh
e6f48348cfd4a3ccdbe681824cff0a1aff1de91e48d0e819f6a3172f6884a07b  .ufo/waves/round-19/landed-check.sh
$ wc -l .ufo/waves/round-19/landed-check.sh
189
$ bash -n .ufo/waves/round-19/landed-check.sh && echo SYNTAX_OK
SYNTAX_OK
```

Executable (`chmod +x` applied on write). Bash 5 + git 2.56.0; no new dependency.

## 2. Contract as implemented

Usage `landed-check.sh LANE_DIR HASH...`; each HASH must be 4–64 hex chars (`:57-64`), so
rev-syntax like `HEAD~1` is a usage error rather than a surprise resolution.

Remote tip, exactly the assigned call, bounded and prompt-free (`:71-80`, `:87`):

```
GIT_TERMINAL_PROMPT=0 GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0
lsr=$(tmo git -C "$LANE" ls-remote origin refs/heads/master 2>/dev/null)   # tmo = timeout 60
```

The tip is resolved to a local commit (`:104`); if its object is absent locally the tool
reports that per hash and still refuses to fetch. Local `refs/heads/master` is resolved at
`:110`. `HEAD` is never consulted (the lane's HEAD is detached — `symbolic-ref -q HEAD` rc=1 —
and detached HEAD is precisely what F16/R3 warns about).

Per hash (`:127-183`):

- `LANDED <full-hash>` — commit resolves locally and `git merge-base --is-ancestor HASH <resolved remote tip>` exits 0 (`:142`).
- `LOCAL_ONLY <full-hash> (reason)` — present locally, not landed, with the reason: ancestor of master but not of the remote tip; remote tip object absent locally (ancestry untestable, no fetch); ancestor of neither; master ref absent; object present but not a commit; ancestry test errored rc=N.
- `MISSING <hash>` — object absent locally (abbreviated input echoed as given).

Exit map: `0` all LANDED, `1` any LOCAL_ONLY/MISSING, `2` usage or could-not-evaluate
(not a repo, no `origin`, `ls-remote` failure, no `refs/heads/master` there, ancestry test
error). A shallow clone additionally gets a stderr warning because ancestry is bounded by the
shallow boundary (`:113-116`).

Commands invoked (full list from `grep -n 'git -C'`): `rev-parse --git-dir`,
`ls-remote origin refs/heads/master`, `rev-parse --verify --quiet`, `rev-parse --git-path`,
`cat-file -e`, `merge-base --is-ancestor` (`:84,87,104,110,113,129,133,142,162,175`).
No `fetch`, `pull`, `push`, `status`, `diff`, `checkout`, `reset`, ref update, worktree touch,
index read, or `jj` invocation appears in any executed command; a token scan finds the words
"fetch"/"checkout" only inside stderr message strings (`:121`, `:85`, `:176`) and comments.

## 3. Hermetic test matrix — bare /tmp remote, /tmp clones only

Harness `/tmp/landed-test.sh`, fixtures under `/tmp/landed-test.7tUvcb` (bare
`/tmp/.../remote.git`; no lane repo used as a remote). Fixture graph:

```
A (seed) -> C (seed) -> E (seed, remote tip)
stale   = clone at A, never fetched
fresh   = clone at C, local-only D on top
ahead   = clone at E, local-only G on top; side branch H off C (never on master, not pushed)
behind  = clone at E, master reset back to C (tip object present)
A=b229508d C=aeebfdf9 D=a21fd98d E=f6ff2397 G=c7c0ec02 H=f5494862
BLOB=4bcfe98e (HEAD:d in fresh)   UNKNOWN=deadbeef... (absent)
```

| case | invocation target | observed stdout (stderr tip elided) | exit |
|---|---|---|---|
| T1 behind | `behind C E` | `LANDED C`, `LANDED E` | 0 |
| T2 ahead | `ahead E G H D` | `LANDED E`; `LOCAL_ONLY G (ancestor of refs/heads/master, not of origin/master f6ff2397…)`; `LOCAL_ONLY H (ancestor of neither …)`; `MISSING D` | 1 |
| T3 tip absent | `fresh D C E` | `LOCAL_ONLY D (… remote tip f6ff2397… is absent locally, ancestry untestable without a fetch)`; same for `C`; `MISSING E` | 1 |
| T4 stale/behind | `stale A` | `LOCAL_ONLY A (ancestor of refs/heads/master; remote tip … absent locally …)` | 1 |
| T5 unknown | `behind deadbeef…` | `MISSING deadbeef…` | 1 |
| T6 non-commit | `fresh BLOB` | `LOCAL_ONLY 4bcfe98e… (object present but not a commit)` | 1 |
| T7 abbrev + upper | `behind f6ff2397 F6FF2397…` | `LANDED` twice, both printed full canonical `f6ff2397…` | 0 |
| T8a no args | — | `usage: landed-check.sh LANE_DIR HASH...` | 2 |
| T8b dir only | — | usage | 2 |
| T8c nonexistent dir | — | `not a directory` | 2 |
| T8d plain dir | — | `not a git checkout` | 2 |
| T8e repo without origin | — | `git ls-remote origin refs/heads/master failed` | 2 |
| T8f origin without master | — | `origin has no refs/heads/master` | 2 |
| T8g non-hex arg | `HEAD` | `not a hex object name: HEAD` | 2 |
| T9 read-only | `fresh D C` | full `.git` tree snapshot (all depths) byte-identical before/after; `FETCH_HEAD=absent` | — |
| T10 token scan | — | no forbidden subcommand in executed code (message-string hits only) | — |

Harness result: `RESULT: PASS`, exit 0. The one deliberately conservative case is T4: a lane
that is behind and has never fetched cannot prove ancestry, so an actually-landed commit reads
`LOCAL_ONLY (remote tip absent locally …)` with the reason spelled out — per the assigned
contract ("remote tip object absent locally → say which"), never a false LANDED.

## 4. Live run against the lane (read-only)

```
$ .ufo/waves/round-19/landed-check.sh /home/vgpnk/Projects/shokunin/mado-shokunin \
    9c54c56 17661e0fa83f978fb659f5bb8fef47f0969f6945
landed-check.sh: origin/master = 17661e0fa83f978fb659f5bb8fef47f0969f6945 (object present locally)
LANDED 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
LANDED 17661e0fa83f978fb659f5bb8fef47f0969f6945
EXIT=0
```

Independent confirmation: `git -C <lane> ls-remote origin refs/heads/master` →
`17661e0fa83f978fb659f5bb8fef47f0969f6945	refs/heads/master`; local `refs/heads/master` and
frozen baseline `9c54c56` both read LANDED. Negative live check:
`deadbeef… → MISSING`, exit 1; abbreviated `9c54c56 → LANDED 9c54c56a6a75…`, exit 0.

Read-only proof on the live lane: full `.git` tree snapshot (`find .git -printf '%p %y %s %T@'`,
2,558 entries, all depths) taken before and after the two-hash invocation is identical —
sha256 `78789adbbf852dd3d464232e92b2a019885012e7d4219914719480b4357c9af4` both sides;
`FULL_GIT_TREE_UNCHANGED`.

Observation vs audit F16: the audit's 14:16:37Z snapshot had `origin/master=27cd06f5`,
`master=3e9848a5`, ahead=8. The lane now has `master=origin/master=17661e0` (pre-registration)
with `9c54c56` beneath it, so that snapshot is superseded by a later push. I performed no git
write in the lane; `git`'s HEAD is detached (`symbolic-ref -q HEAD` rc=1) but points at
`17661e0`, equal to `refs/heads/master`, and the tool ignores HEAD by design.

## 5. Risks and integration note

- The only network operation is the assigned `ls-remote`; it is bounded by `timeout 60`,
  promptless (`GIT_TERMINAL_PROMPT=0`), and any failure is exit 2, never a silent LANDED.
- `[INFERENCE]` `GIT_NO_LAZY_FETCH=1` (git ≥2.45) prevents a promisor/partial clone from
  lazily fetching objects during resolution; if an older git ignores it, the only exposure is
  that `rev-parse`/`cat-file` could contact the promisor remote. Not exercised here (no
  partial-clone fixture).
- Integration into `tools/mado-verify.sh` was **not** done: this assignment names one new file
  and L1 owns gate wiring/verdict semantics. A future row can call this script; note its exit 2
  is "could-not-evaluate", which a gate should map to UNKNOWN, not DIVERGED.

## Limits

- Did not test the ancestry-error branch (`rc>1` from `merge-base --is-ancestor`) — requires
  corrupt/replaced objects; the branch exists (`:144-153`) but is untested.
- Did not test a SHA-256 object-format repository (64-hex tip/inputs are accepted but
  unexercised) nor a genuinely shallow clone (warning path unexercised).
- Did not test an unreachable/credential-demanding network remote end-to-end; only `ls-remote`
  failure with no `origin` and with an empty bare remote were exercised (both exit 2).
- Did not modify or re-verify `tools/mado-verify.sh`; no gate, suite or selftest was changed,
  so no lane gate was run (out of scope and not assigned).
- Test fixtures live in `/tmp/landed-test.7tUvcb` (ephemeral); nothing was created under the
  lane except the deliverable and this report.

## Installs

none — `git 2.56.0`, coreutils `timeout` and bash were already present; no package manager,
network fetch of tooling, or update was run.
