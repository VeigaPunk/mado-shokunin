# SentinelScope — wave-1 scope & safety sweep (round 32)

Seat: sentinel. Lane `mado-shokunin`. Read-only sweep; this seat wrote only this
report — no lane file, index, or jj state touched. Sweep ran ~20:07–20:12 local
while the wave was mid-flight (first seat artifacts 20:03:38, latest observed
report 20:07:01).

## 1. Permitted-write envelope — IN SCOPE

The wave permits writes to exactly these trees, all inside the lane:

- `.ufo/waves/round-32/w1/reports/` — each seat's own `Report:` file
  (`w1-spec.json` context: "a seat may write ONLY (a) its own report file … and
  (b) the scratch directory its item names").
- `.ufo/waves/round-32/scratch/<SeatName>/` — per-seat scratch (5 scout fetch
  dirs + `ScribeEntry*/`, `ExecCensusManual/`, `ScribeLessonDraft/` observed).
- `.ufo/waves/round-32/assimilation/` — shared executor scratch
  (`append-block.md`, `recheck-prose-stripped.md`, `reg-ids.txt`,
  `staged-ids.txt`, `collisions.txt`, `guard-proof-*`, `quarantine-slice`,
  `validate/` mirror).
- `.ufo/waves/round-32/c1/controls/` and `.ufo/waves/round-32/c2/controls/` —
  the K1/K2 control-receipt dirs (registration §C1 K1, §C2 K2; CriticC1Predicate's
  scratch lands under `c2/controls/` per its item text — odd naming, still in
  the round-32 envelope).

I extracted every declared write target from all 32 spec items (`write/draft/
working dir/into scratch/committed under/Report:` phrases): **zero resolve
outside `/home/vgpnk/Projects/shokunin/mado-shokunin/`**. The corpus paths named
in scribe items (`corpus/knowledge/*.md`, `corpus/`) are read targets / L1
landing targets — each item says "DRAFT (scratch only)". External trees named
(`/home/vgpnk/Projects/shokuknow/…`, sibling `*-shokunin/corpus/`) are
read-only per spec and per registration.

## 2. Fleet-root misrooted-write sweep — CLEAN

`git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec) printed
12 modified + 16 untracked entries. Modified entries are all
`.ufo/state/*.report-baseline` + `.ufo/watchdog.log` — driver runtime, expected
churn, not files. Every untracked file was grepped for `mado|round-32|round_32`:

- `.omp/mcp.json`, `bm.json`, `live.html`, `live_s228.html`, `nama.html`,
  `s395.txt`, `tf_bavelas.html`, `unblob.log`, `wb2.html`, `write`, `xc.xml`,
  `scripts/hyaku/*.bak-20261023T040735Z`, `.ufo/state/{kotoba,kotodama,
  revenger}.report-baseline` — **no hits**.
- `.ufo/waves/round-37/` — one file, `residual/ResCorrections.md`; grep for
  `mado|round-32` → no hits. A sibling wave's fleet-level artifact, not a
  misrooted mado write.

**No misrooted round-32 writes at the fleet root.** Nothing deleted (L1's job).

## 3. jj state / Git index — UNMUTATED BY SEATS

```
$ git -C …/mado-shokunin status --porcelain   → no staged entries (no
  A/D/R/M in column 1); `git diff --cached --name-only` → empty. Index clean.
$ jj --ignore-working-copy -R …/mado-shokunin log -n 3 --no-graph →
  poywspzz  571e178b  2026-10-24 04:29:33  (no description — working-copy commit)
  ttznzsrq  91862344  2026-10-24 04:29:33  master  "round-31 verifier spot-check…"
```

- `git rev-parse HEAD` = `91862344b9fd…` = `master`; registered base
  `256222890d93…` verified ancestor (`git merge-base --is-ancestor` → true).
- The `@` working-copy commit `571e178b` is the standard jj placeholder sitting
  on the round-31 tip; its timestamp (04:29:33) **predates** wave-1 seat
  activity by ~16 h. `--ignore-working-copy` means my reads did not re-snapshot
  it. No mutating `jj`/`git` command appears in any of the 32 seat logs
  (grep over `w1/logs/` for `git commit|push|add|reset|checkout -|restore|
  apply|jj describe|new|edit|abandon|squash|bookmark|git` → zero hits).

Working-tree residue predating this wave, **not** attributable to r32 seats:
`M .ufo/waves/round-30/w1/reports/{RevRecordsChain,RevTrendExpansion,SentScope}.md`
+ untracked `{RevTrendDiscernment,SimplifierC2}.md`, all mtime 04:15–04:17 —
the round-30/31 verifier closeout rewrote those reports (diff shows a "final
pass" revision to `274f735`). Uncommitted since then.

## 4. Protected paths vs lane tip — CLEAN

```
$ git diff --stat HEAD -- corpus/ SCORECARD.md corpus/SOURCES.md  → (empty)
$ git status --porcelain -- corpus/ SCORECARD.md corpus/SOURCES.md → (empty)
```

No seat mutation of `corpus/`, `SCORECARD.md`, or `corpus/SOURCES.md` in the
working tree against the tip (`91862344`). Seat drafts of knowledge entries
exist only under `scratch/`, as designed.

## 5. Compositor / host config — NO EXPOSURE

- Spec: only compositor-relevant tokens are documentation literals
  (`.socket.sock`, `.socket2.sock`, `hyprctl dispatch` inside a **grep
  pattern** in ConnectorSiblingOverlap's item). No item invokes `hyprctl`
  against the live socket, `systemctl`, `busctl`, or touches
  `~/.config/hypr`, `/etc`, waybar/hyprpaper, or any host service. Network
  access is read-only fetches of pinned wiki/GitHub URLs into scratch.
- Seat logs (`w1/logs/*.log`, all 32): two `hyprctl dispatch` strings — both in
  `ConnectorSiblingOverlap.log` as the quoted grep-pattern text, not a
  command. Zero writes outside the lane (redirect/`tee`/`curl -o` sweep).
- Pacman/sudo: no occurrence.

## Observations (not defects; for the L1's awareness)

- `quality/check-axis-scores.py` — untracked (`??`), mtime 20:04:55, **outside
  seat write scope** (`quality/` is not a seat dir). It is the registration's
  named C2 counter (`registration.md:124`); ConnectorInstrumentReuse's report
  documents it as a pre-existing uncommitted draft it *found*, not created
  ("present only as an uncommitted worktree file"). Attribution: L1 staging,
  mid-wave. Flagging because it sits inside the wave window — a seat could not
  have written it in-scope, and none claims it.
- `fetch/S186..S196.bin` under `round-32/` — pre-staged source mirrors, mtime
  20:03:38–41 (wave start), inside the permitted round-32 envelope.
- `assimilation/validate/` mirror files carry mtimes 02:57–04:29 — L1
  groundwork inside the permitted assimilation dir.

## Verdict

**Clean.** Write scope fully inside the lane; zero misrooted fleet-root writes
naming mado/round-32; lane jj state and Git index unmutated; protected paths
(`corpus/`, `SCORECARD.md`, `corpus/SOURCES.md`) clean against the tip; no
command in the wave can reach the live compositor or host config trees.

Commands run (all read-only): `git status --porcelain` (fleet + lane),
`git diff --cached`, `git diff HEAD -- corpus/ SCORECARD.md corpus/SOURCES.md`,
`git merge-base --is-ancestor`, `git rev-parse HEAD`,
`jj --ignore-working-copy -R <lane> log -n 3 --no-graph`, per-file
`grep -niE 'mado|round-32|round_32'` over every untracked fleet-root file,
write-target extraction over all 32 spec items, mutating-command grep over all
32 seat logs. Nothing was deleted, staged, or snapshotted.
