# CapLandednessCheck1158 — C2 row re-run: `SCORECARD.md:1158` (`landedness check`)

Seat: `MadoR25A3.CapLandednessCheck1158` (C2 executor, wave `a3w1`). Date: 2026-10-23.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (read-only throughout; no lane run of the tool, no lane git write).
Base for the row: `41cc04c8d593837a0d5078bffaacdaa163d12897`.

## 1. The row read at base

Extracted base bytes (read-only):

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 41cc04c8:SCORECARD.md
  -> 1618 lines, sha256 6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08
```

- Row: `SCORECARD.md:1158`, under `### Capabilities (round 19)` (heading at `:1155`) of the
  "Round 19 — results and author verdicts" section.
- Capability: **landedness check** — "Say whether each cited lane hash is an ancestor of the live remote
  tip (`LANDED`/`LOCAL_ONLY`/`MISSING`) without fetching or writing".
- Demonstration command named by the row: `bash .ufo/waves/round-19/landed-check.sh LANE HASH...`.
- Evidence pointer named by the row: w1 `LandedCheck.md` (T1–T9 matrix), i.e.
  `.ufo/waves/round-19/w1/reports/LandedCheck.md`.

## 2. Sandbox clone and re-run (per C2 contract)

Commands (GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset, clone only under `/fast/scratch/hyaku/mado-r25a3/`):

```
mkdir -p /fast/scratch/hyaku/mado-r25a3/c2
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q \
  /home/vgpnk/Projects/shokunin/mado-shokunin \
  /fast/scratch/hyaku/mado-r25a3/c2/CapLandednessCheck1158
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C \
  /fast/scratch/hyaku/mado-r25a3/c2/CapLandednessCheck1158 checkout -q --detach 41cc04c8
```

Observed clone state: `HEAD = 41cc04c8d593837a0d5078bffaacdaa163d12897`;
`origin = /home/vgpnk/Projects/shokunin/mado-shokunin (fetch/push)` (a local-path remote, so the sandbox
`ls-remote` is a local ref read, not a network read); script bytes at base:
`sha256 ca1f76b4c19563f44d919b06ee815c3e18e5dd6598304d420d84ec64974ae63c`, 189 lines,
64-hex.

The row's command is not runnable without its two argument classes; the nearest documented form is the
script's own usage `landed-check.sh LANE_DIR HASH...` with the sandbox clone as `LANE_DIR` and hashes from
the lane as `HASH...` (the exact form the round-24 C2 manifest froze: `{TREE}/.ufo/waves/round-19/landed-check.sh
{LANE} {REV}`). Run with `timeout 600` and `prlimit --as=4000000000`, cwd = the sandbox clone.

### Receipt A — LANDED, exit 0

```
$ cd /fast/scratch/hyaku/mado-r25a3/c2/CapLandednessCheck1158
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 \
    bash .ufo/waves/round-19/landed-check.sh \
    /fast/scratch/hyaku/mado-r25a3/c2/CapLandednessCheck1158 41cc04c8 1ed41fa 2896dc4
landed-check.sh: origin/master = 2896dc4a009ef68f3ef50f0bdcafd6f4aee82a5f (object present locally)
LANDED 41cc04c8d593837a0d5078bffaacdaa163d12897
LANDED 1ed41fa8301a4562d125503e5b881ec8eb5a1908
LANDED 2896dc4a009ef68f3ef50f0bdcafd6f4aee82a5f
exit=0
```

### Receipt B — LOCAL_ONLY, exit 1 (sandbox-only probe commit)

A disposable empty commit was made **in the sandbox clone only** (no lane write), on top of the clone's
master, then the tool was pointed at it:

```
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -c user.name=C2Probe \
    -c user.email=c2@example.invalid checkout -q -B probe-master 2896dc4
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -c user.name=C2Probe \
    -c user.email=c2@example.invalid commit -q --allow-empty -m "c2 probe: local-only commit"
$ git update-ref refs/heads/master 559a55dbe53ecc84b39039d9b64f1658584f79c7
LOCAL=559a55dbe53ecc84b39039d9b64f1658584f79c7

$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 \
    bash .ufo/waves/round-19/landed-check.sh \
    /fast/scratch/hyaku/mado-r25a3/c2/CapLandednessCheck1158 559a55dbe53ecc84b39039d9b64f1658584f79c7
landed-check.sh: origin/master = 2896dc4a009ef68f3ef50f0bdcafd6f4aee82a5f (object present locally)
LOCAL_ONLY 559a55dbe53ecc84b39039d9b64f1658584f79c7 (ancestor of refs/heads/master, not of origin/master 2896dc4a009ef68f3ef50f0bdcafd6f4aee82a5f)
exit=1
```

### Receipt C — MISSING / usage, exit 1 / exit 2

```
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 \
    bash .ufo/waves/round-19/landed-check.sh \
    /fast/scratch/hyaku/mado-r25a3/c2/CapLandednessCheck1158 deadbeef
landed-check.sh: origin/master = 2896dc4a009ef68f3ef50f0bdcafd6f4aee82a5f (object present locally)
MISSING deadbeef
exit=1

$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 \
    bash .ufo/waves/round-19/landed-check.sh \
    /fast/scratch/hyaku/mado-r25a3/c2/CapLandednessCheck1158 HEAD
landed-check.sh: not a hex object name: HEAD
exit=2
```

### Receipt D — live-LANE variant (read-only), exit 0

To exercise the row's literal "live remote tip" wording (the sandbox clone's origin is a local path),
the same base-`41cc04c8` bytes were run once with the lane as `LANE_DIR`. The script only reads
(`rev-parse`, `ls-remote`, `cat-file -e`, `merge-base --is-ancestor`; no fetch/push/index/ref write in its
bytes), so this is a read-only invocation against the lane:

```
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 \
    bash .ufo/waves/round-19/landed-check.sh \
    /home/vgpnk/Projects/shokunin/mado-shokunin 41cc04c8
landed-check.sh: origin/master = 2896dc4a009ef68f3ef50f0bdcafd6f4aee82a5f (object present locally)
LANDED 41cc04c8d593837a0d5078bffaacdaa163d12897
exit=0
```

Independent lane-side read: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-remote origin
refs/heads/master` → `2896dc4a009ef68f3ef50f0bdcafd6f4aee82a5f refs/heads/master` (lane origin
`https://github.com/VeigaPunk/mado-shokunin.git`); lane `refs/heads/master` resolves to the same id.

## 3. Ledger line

| SCORECARD.md:1158 | landedness check | Say whether each cited lane hash is an ancestor of the live remote tip (LANDED/LOCAL_ONLY/MISSING) without fetching or writing | works at 41cc04c8: exit 0 `LANDED 41cc04c8d593…` (also 1ed41fa8, 2896dc4a); exit 1 `LOCAL_ONLY 559a55db… (ancestor of refs/heads/master, not of origin/master 2896dc4a…)` and `MISSING deadbeef`; exit 2 `not a hex object name: HEAD`; stderr names origin/master = 2896dc4a | `bash .ufo/waves/round-19/landed-check.sh /fast/scratch/hyaku/mado-r25a3/c2/CapLandednessCheck1158 41cc04c8 1ed41fa 2896dc4` (base-41cc04c8 bytes, cwd = clone) | `SCORECARD.md:1581` (round-24 re-demonstration table: "landedness check | works", which by its own text supersedes the implied `works` of earlier rows) and `SCORECARD.md:1151` (scope narrowing: "landed-check.sh (F16 narrowed: a probe, not a gate row)"); no contradicting text found |

## 4. Supersede/contradiction grep of SCORECARD.md at 41cc04c8

Whole-file grep (case-insensitive) for `landed` / `landedness` / `landed-check` / `F16`:

- `:1118` — round-19 intro enumerating the carried jj-audit findings; names "landedness check (F16)" in a list. No status.
- `:1151` — round-19 non-claim repairs: "`landed-check.sh` (F16 narrowed: a probe, not a gate row)". Scope narrowing, not a contradiction: the row claims a classifier, not gate integration.
- `:1158` — the row under test.
- `:1581` — round-24 "Capability status (round 24 re-demonstration)" row: `| landedness check | works | `LANDED <rev>`, at `8e5d9369` |`. The section states it "supersedes the implied `works` of every earlier row". Same observed status as this re-run; no conflict.
- `:1063` — round-19 carried-items list naming F16 among audit findings; no status.
- No later row or sentence says the landedness check is stale, broken, or narrowed away.

Also checked the frozen round-24 C2 manifest (`.ufo/waves/round-24/c2/manifest.json` at `41cc04c8`):
its `landedness check` entry freezes exactly the `bash {TREE}/.ufo/waves/round-19/landed-check.sh {LANE} {REV}`
invocation, `exit_ok [0,1]`, regex `^(LANDED|LOCAL_ONLY|MISSING) {REV}\b`, and its `why` notes the row
"is network-dependent by its own ls-remote contract". Receipts A–D satisfy that rule.

## 5. Risks / drift (reported, not repaired; outside this seat's write scope)

1. **Evidence-pointer sha drift (documentation, not the row's claim).** The cited w1 report
   `LandedCheck.md` §1 records `sha256 e6f48348cfd4a3ccdbe681824cff0a1aff1de91e48d0e819f6a3172f6884a07b`
   (189 lines). That hash matches the script bytes at `df84807` (round-19 w1). The bytes at the row's base
   `41cc04c8` are `sha256 ca1f76b4c19563f44d919b06ee815c3e18e5dd6598304d420d84ec64974ae63c` (also 189
   lines): commit `61eaa07` (round-19 w2) changed one line,
   `rev-parse --git-path shallow` → `rev-parse --path-format=absolute --git-path shallow`, on the
   shallow-clone warning path. The row cites no sha and its behaviour is unchanged; the drift is inside the
   evidence artifact, so a reader who checks §1's sha against base bytes sees a mismatch. A future ledger
   should cite the base-byte sha.
2. **"Without writing" is observed statically.** The script's executed command set at base
   (`git -C … rev-parse [--verify|--git-path]`, `ls-remote`, `cat-file -e`, `merge-base --is-ancestor`)
   contains no fetch/push/ref-update/index/worktree verb and exports `GIT_TERMINAL_PROMPT=0`,
   `GIT_NO_LAZY_FETCH=1`, `GIT_OPTIONAL_LOCKS=0`. I did not re-do a `.git` metadata before/after snapshot in
   this sandbox (the round-19 T9 did). No write was printed; treat read-only as verified at the command level,
   not byte-snapshot level, in this re-run.
3. **Sandbox origin is a local path.** Receipts A–C exercise the three verdicts but their `ls-remote` reads the
   lane's refs, not the GitHub remote. Receipt D performs the network read named by the row (tip
   `2896dc4a…`, equal to lane master), so the "live remote tip" wording is exercised at least once, read-only.
4. **Runnable only with arguments.** `bash .ufo/waves/round-19/landed-check.sh` alone is a usage error
   (`usage: landed-check.sh LANE_DIR HASH...`, exit 2). The row writes `LANE HASH...` as placeholders, and the
   round-24 manifest supplies the same concrete form; the re-run used that documented form.

## 6. Cleanup

```
rm -rf /fast/scratch/hyaku/mado-r25a3/c2/CapLandednessCheck1158
```

Verified: the clone path is gone (`ls /fast/scratch/hyaku/mado-r25a3/c2/` lists only sibling seats' dirs and
the shared `SCORECARD-41cc04c8.md`). No process was started by this seat (the tool runs no long-lived
process); no nested compositor, no network fetch beyond the read-only `ls-remote` in Receipt D.

## 7. Installs

None. No package, tool or config change was needed or made; no pacman transaction was attempted.
