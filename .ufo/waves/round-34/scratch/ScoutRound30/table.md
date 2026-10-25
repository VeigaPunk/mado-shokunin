# ScoutRound30 — round-30 seat reports: bytes before/after the d40b35f rewrite

Lane tip measured at `fa7ba11346116672352b5d41494141c5c4d738d0` (HEAD, worktree identical —
`git status` shows no modification under `.ufo/waves/round-30/`). "Bytes @69f7210" are the
post-`d40b35f` bytes: `d40b35f` is an ancestor of `69f72100bee31a60b811f8fbbe7796db883e17b3`,
and no commit between them touched these paths (`git log --follow` per file: only `d40b35f`
plus the round-30 commits below). Blob hashes confirm identity: `git rev-parse HEAD:<path>`
returns the same blob sha that `d40b35f` wrote.

Pre-rewrite sizes (`d40b35f^` = `9a46ccf`) included for provenance.

| File | Bytes @ 9a46ccf (pre-rewrite; 0 = absent) | Bytes @ 69f7210 | Bytes @ tip fa7ba11 | Provenance of current bytes |
|---|---|---|---|---|
| RevRecordsChain.md | 21687 | 19058 | 19058 | Rewrite of the round-30 committed file (committed 274f735, self-labeled earlier pass). Current text supersedes it: "This file's committed copies at `a0dd664`/`274f735` are earlier passes of the same seat; this revision is final." 1 shared unique nonblank line — full rewrite, not an edit. |
| RevTrendExpansion.md | 12100 | 12991 | 12991 | Rewrite of the round-30 committed file (committed 274f735, the seat's first pass). Current text: "This file supersedes my first pass, which commit `274f735` committed as `w1/reports/RevTrendExpansion.md`." 5 shared unique nonblank lines — full rewrite. |
| RevTrendDiscernment.md | 0 | 18207 | 18207 | Other source. Never committed during round 30 (absent at a0dd664, 274f735, 15ddd7d); first committed at d40b35f (diff entry `A`). Content is a finished round-30 seat report for registered seat `RevTrendDiscernment` (swarm-registry @274f735) — plausibly the seat's uncommitted working-tree file. Not a rewrite of any committed round-30 bytes. |
| SentScope.md | 15568 | 23730 | 23730 | Rewrite of the round-30 committed file (committed 15ddd7d). Current header re-bases the audit window to `d72243e1`–`a0dd664` plus "later commits exist (see §0)". 21 shared unique nonblank lines — heavy rewrite retaining the F-numbered finding skeleton. |
| SimplifierC2.md | 0 | 11431 | 11431 | Other source. Never committed during round 30; first committed at d40b35f (diff entry `A`). Content is a finished round-30 seat report for registered seat `SimplifierC2`, explicitly noting "worktree `M` entries below belong to the L1's in-flight addendum" — i.e. it was written while round 30 was still running and stayed uncommitted. Not a rewrite of any committed round-30 bytes. |

## Reality check lines (quoted verbatim from the tip bytes; each cites a finding, a command run, or an evidence pointer)

- **RevRecordsChain.md** (l.126): `I re-ran every predicate under every blob (base 41/43 exit 1; data and `d72243e` 43/43 exit 0; selftest 6/6 → 8/8 → 9/9; C2 28/40, 31/39 → 40/52, 40/40 at data,` — re-executed counters with per-revision scores.
- **RevTrendExpansion.md** (l.43): `| gate red at base, green at tip (pre-repair) | `git show 451e8b3c:quality/check-index.py` (sha256 `fc4a10a2…`, git blob `df01b20f…`): `--rev 8f51071b` → `indexed=41/43 missing=2 … coverage=9.5349/10` exit 1 …` — command + anchored output.
- **RevTrendDiscernment.md** (l.101): `UNRESOLVED criterion 1..5, 38..40`, `TARGET_MISSED`, exit 1 (I ran the frozen counter at …` — counter output observed at named revisions.
- **SentScope.md** (l.45): `| F2 `--root` symlinked `corpus` ancestor | **OPEN** | `/tmp/sentinel-anc/root` -> foreign tree: `indexed=1/1` exit 0 |` — adversarial repro with observed output.
- **SimplifierC2.md** (l.19): `count.py 446dc39` → `literal 40/52 fraction=0.7692`, `active=40 resolved_active=40 fraction=1.0000`, verdict TARGET_MET, exit 0; `count.py 8f51071b` → `28/40`, `31/39`, UNRESOLVED {1..5,38..40} all "no citation", TARGET_MISSED, exit 1.` — per-revision counter runs.
