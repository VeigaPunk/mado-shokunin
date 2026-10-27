# R54W2Seat31 — item 31: C2 pin revision visibility

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (HEAD = master = `350d30e4ec5531f65ce99a57efeb8216f38e678a`).
Base: `e25149fec8152a3aabd2b18a0ee8663b23cf65aa` (parent of `350d30e4`).
Method: read-only git plumbing on the lane; one isolated fixture (`git init` in scratch, `git -C D` throughout, rev-parse toplevel checked before and after) fetching only the base closure, then only the freeze closure. No lane, source, registration, predicate or git-state mutation. No host reads, no network, no package queries, no tool installs, no subagents.

## Verdict

Round-54 C2 pins are **not in base `e25149fe`'s tree or closure**. They first become visible at freeze commit `350d30e4` (the lane HEAD). Any C2 scoring at a revision before `350d30e4` finds no pin bytes, so PRED-C2-r54 cannot pass there (it can only be TARGET_MISSED by absence). At `>= 350d30e4` the pins are present, byte-identical to their committed `SHA256SUMS.txt`, and reachable from `master`.

Two provenance statements in the frozen files are contradicted by git clocks: the registration's "committed before wave 1 dispatch" and the claims' unrecorded "Before" state for the pins.

## Frozen-contract lines (verbatim locations)

- `claims-frozen.md:3` — "Frozen 2026-10-27 before any wave dispatch; base `e25149fe`."
- `claims-frozen.md:55-56` — PRED-C2-r54 command and `MADO_UWSM_ENTRY:` line.
- `claims-frozen.md:60-62` — clause (b): rows S375–S377 carry a URL pinned at `0727985c…`, and the quote occurs "in the round-54 pin named by its source file".
- `claims-frozen.md:67-68` — "Before (base `e25149fe`)": entry absent, rows absent, predicate TARGET_MISSED by absence. **The pins are not named in this before-state.**
- `claims-frozen.md:82-84` — C2 causal separability reads `.ufo/waves/round-54/fetch/` (no `--rev` qualifier on the pin path).
- `registration.md:3-4` — "Frozen 2026-10-27T14:00-03:00 … committed before wave 1 dispatch."
- `registration.md:57-59` — pins at `.ufo/waves/round-54/fetch/`, sha256 in `SHA256SUMS.txt`, fetched 2026-10-27 at `0727985c…`.

## Commands and output (lane, read-only)

Toplevel and objects:
```
$ git -C L rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/mado-shokunin          exit 0
$ git -C L rev-parse 350d30e4
350d30e4ec5531f65ce99a57efeb8216f38e678a             exit 0
$ git -C L merge-base --is-ancestor e25149fe 350d30e4; echo $?
0
$ git -C L log --format='%h %P %ad %cd %s' -n 3 350d30e4
350d30e4 e25149fe… Tue Oct 27 13:42:45 2026 -0300 Tue Oct 27 14:11:10 2026 -0300 round-54: freeze claims, registration, source pins and wave one dispatch
```

Pin presence per revision (`git cat-file -e <rev>:<path>`):
```
e25149fe:…/fetch/uwsm-0.27.1-README.md        exit=128
e25149fe:…/fetch/uwsm-0.27.1-main.py          exit=128
e25149fe:…/fetch/uwsm-0.27.1-uwsm-app.1.scd   exit=128
e25149fe:…/fetch/SHA256SUMS.txt               exit=128
e25149fe:…/fetch/README.txt                   exit=128
350d30e4:…/fetch/uwsm-0.27.1-README.md        exit=0
350d30e4:…/fetch/uwsm-0.27.1-main.py          exit=0
350d30e4:…/fetch/uwsm-0.27.1-uwsm-app.1.scd   exit=0
350d30e4:…/fetch/SHA256SUMS.txt               exit=0
350d30e4:…/fetch/README.txt                   exit=0
```
`ls-tree`: base `…/round-54/fetch/` → 0 entries; `350d30e4` → 5 entries (README.txt, SHA256SUMS.txt, uwsm-0.27.1-README.md, uwsm-0.27.1-main.py, uwsm-0.27.1-uwsm-app.1.scd).

Path history: `git log --all --oneline -- .ufo/waves/round-54/fetch/` → only `350d30e4 round-54: freeze claims, registration, source pins and wave one dispatch`.

Same test on the other frozen files: `claims-frozen.md` and `registration.md` are `exit=128` at base and `exit=0` at `350d30e4`.

Blob identity at freeze (committed blob bytes vs `SHA256SUMS.txt` vs working tree; `git status --porcelain` on the pin paths empty):
```
uwsm-0.27.1-README.md     blob e50e5072…  bytes 49717   sha256 1874fb83…97b597a  == SHA256SUMS.txt == worktree
uwsm-0.27.1-main.py       blob 0ea69fda…  bytes 199361  sha256 7dd63632…a976c72  == SHA256SUMS.txt == worktree
uwsm-0.27.1-uwsm-app.1.scd blob a983a51c… bytes 2309    sha256 3982503d…8a6f5eb  == SHA256SUMS.txt == worktree
```
`git show 350d30e4:…/SHA256SUMS.txt` lists those three digests; the round-52 pins are tracked at base (`git ls-tree e25149fe .ufo/waves/round-52/fetch/` → 6 entries, e.g. `Hyprland-ConfigActions.cpp` exit 0), which is the contrast the registration relies on for C1.

Object DB note: `git hash-object --no-filters` (no `-w`) of the three working-tree pins returns the blob ids above, and `git cat-file -e` on them exits 0 **in the lane**, because the lane object DB contains the freeze closure via `master`. That shows presence in the shared store, not presence at base; the fixture below separates the two.

## Isolated fixture (object visibility per revision)

`D=$(mktemp -d /fast/scratch/hyaku/mado-r54/R54W2Seat31/fx.XXXXXX)`; `git init -q "$D"`; `git -C "$D" rev-parse --show-toplevel` = `$D` (checked before and after fetch/checkout).

Base closure only (`git -C "$D" fetch -q "$L" e25149fe…`, exit 0; `checkout -q`, exit 0):
```
fetch-dir files at base closure: 0
blob e50e5072… in D  exit=1
blob 0ea69fda… in D  exit=1
blob a983a51c… in D  exit=1
ls …/fx/.ufo/waves/round-54/fetch → No such file or directory
```

Freeze closure (`git -C "$D" fetch -q "$L" 350d30e4ec5531f65ce99a57efeb8216f38e678a`, exit 0; `checkout -q`, exit 0):
```
fetch-dir files at freeze: 5 (README.txt, SHA256SUMS.txt, uwsm-0.27.1-README.md, uwsm-0.27.1-main.py, uwsm-0.27.1-uwsm-app.1.scd)
blob e50e5072… in D  exit=0
blob 0ea69fda… in D  exit=0
blob a983a51c… in D  exit=0
```
(First attempt used the abbreviated `350d30e4` and failed with `fatal: couldn't find remote ref 350d30e4` exit 128; retried with the full id. Recorded, not hidden.)

Counter presence: `ls-tree -r --name-only {e25149fe,350d30e4} -- quality/counters | grep -c r54` → `0` and `0`; `git -C L cat-file -e 350d30e4:quality/counters/c2-r54-uwsm-entry.py` → exit 128 (absent). So no C2 counter is runnable at either revision; no `--rev` result was produced and none is claimed here.

## Timeline (git clock vs dispatch)

- `e25149fe` committer 13:42:45 (round-53 spot-check); parent of freeze.
- Pin files mtime 13:54 (`fetch/`), `fetch/README.txt` 13:58, `registration.md` 14:00 — working-tree stamps only.
- `w1-spec.json` mtime 14:05:17; `w1.ready` 14:05:28; `w1.ready.dispatched` 14:06:21.
- `350d30e4` author date 13:42:45, **committer date 14:11:10** — after dispatch. The commit diff (`git diff --stat e25149fe 350d30e4`, 11 files, 7494 insertions, all under `.ufo/waves/round-54/`) includes `w1-spec.json` and `w1-dispatch.json`, which are dispatch artifacts.

So `registration.md:4` "committed before wave 1 dispatch" is not supported by the commit clock: the first git-visible copy of the frozen files is a commit made 5 minutes after dispatch and containing dispatch artifacts. The author timestamp (13:42:45) predates the dispatch, but it is not evidence that the freeze content was final before dispatch.

## Relevant w1 reports (cited, not re-run)

- `R54Seat08.md` lines 36–40, 66–70 (base `git cat-file -e` exit 128 / freeze exit 0), line 342 F1 (high): pins, registration and claims untracked at base; committed 14:11:10 after dispatch; "committed before wave 1 dispatch" false by commit timestamp. Line 310 F4 (downgraded to medium provenance).
- `R54Seat29.md` lines 92–95 (C2 pins tracked only at ≥ `350d30e4`; base-rev counter cannot read them), line 302 B29-1 (HEAD moved `e25149fe`→`350d30e4` at 14:11:10 during the wave).
- `R54Seat07.md` lines 52–55, 64–69 (ABSENT AT BASE; `git log --all -- .ufo/waves/round-54/fetch/` empty at its snapshot; committed at `350d30e4`); line 68 notes nothing in-repo binds a filename to commit `0727985c…` except `fetch/README.txt` prose.
- `R54Seat02.md` lines 17–18 (base `git ls-tree` for round-52 pins), F1/F4 (pins worktree-only at 14:10:33).
- `R54Seat15.md` line 73–74 (F6): C2 verdict path cannot read pins from any rev predating the commit.
- `R54Seat09.md` line 57 says "Pins are **not committed**: `git ls-files .ufo/waves/round-54` → 0" — true at that seat's snapshot, **superseded** now: `git ls-files`/`ls-tree` at `350d30e4` shows 5 pin files.

## Attack result

| # | Claim tested | Result |
|---|---|---|
| A1 | Round-54 pins are in base `e25149fe` git objects (tree or closure) | **Falsified.** Absent from base tree (exit 128) and from a base-only fixture (blob lookups exit 1). |
| A2 | Pins are in the freeze commit `350d30e4` | **Confirmed.** Present (tree exit 0, fixture exit 0), digests equal `SHA256SUMS.txt` and worktree. |
| A3 | Pins are visible via `--rev` for any rev before `350d30e4` | **Not visible.** A C2 counter at such a rev reads nothing; the frozen before-state (`claims-frozen.md:67-68`) does not record this. |
| A4 | "committed before wave 1 dispatch" (`registration.md:4`) | **Contradicted by commit clock** (14:11:10 vs dispatch 14:05:17–14:06:21); the commit contains dispatch artifacts. Author date alone is not evidence. |
| A5 | C2 counter exists at base or freeze | **Absent** (`ls-tree … | grep -c r54` → 0 at both). Predicate not runnable at either rev. |

Residual limit (unchanged from w1): the pins are committed, but `0727985c…` is still asserted only by `fetch/README.txt` prose and URL strings; this seat did not network-check the tag identity (out of fence).

## Scratch and fences

- Scratch: `/fast/scratch/hyaku/mado-r54/R54W2Seat31`. Fixtures `fx.AiJsBW` (base test, removed) and `fx.rWJfrZ` (freeze test, removed). Scratch directory is removed before yield.
- No ENOSPC observed (`/fast` 580G available; `/tmp` untouched).
- No lane, source, registration, predicate, lane-root tracked-file or git-state mutation; `git` on the lane was read-only (`rev-parse`, `log`, `cat-file`, `ls-tree`, `diff --stat`, `status --porcelain`, `hash-object` without `-w`, `branch --contains`, `for-each-ref`, `merge-base`). Fixture git was `init`/`fetch`/`checkout` in scratch only.
- No installs or updates; no host, package, network, or subagent use.

Report trailer: `.ufo/waves/round-54/w2/R54W2Seat31.md`
