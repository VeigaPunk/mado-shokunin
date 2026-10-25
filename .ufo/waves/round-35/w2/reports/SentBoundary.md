# SentBoundary — mado round-35 wave-2 boundary attack

Seat: sentinel (leaf, no dispatch). Read-only audit. Window: 2026-10-25 03:29–03:46 -0300.
Wave-2 was dispatched at 03:28 (`w2-spec.json` mtime); the wave was still in flight at every
snapshot below. Round 35 produced **seven** lane commits, **six during this wave**; the tree was at
`b632f0b` when last observed (03:46). The claim data under test — the three entries and the
`SOURCES.md` rows — has been byte-stable since `4f35c80` (03:42:04); only `lessons/round-35.md`
churned after that.

Raw command/output pairs: `.ufo/waves/round-35/scratch-evidence/SentBoundary/evidence.txt` (written
under `scratch/`, then relocated and committed as `scratch-evidence/` by `4efaf63` mid-wave).

**Concurrency warning first, because it shapes every verdict:** the lane HEAD moved six times
during this wave (`02088b4` 03:34:26, `4f35c80` 03:42:04, `7b745a1` 03:42:29, `4efaf63` 03:43:55,
`8889bdc` 03:45:15, `b632f0b` 03:46:02) and the six corpus files under test were rewritten between
the first two. A `git status` taken at 03:29 and the same command at 03:45 do
not describe the same tree, and neither matches every reviewer's input. Every number below is
stamped with its measurement time.

## Axes named

| # | Axis | Test |
|---|---|---|
| A | Claim closure | every lane-authored write is in the pre-registered claim set and pinned to a blob |
| B | Fleet containment | nothing written in `/home/vgpnk/Projects/shokunin` outside `.ufo/reports/round-35/` |
| C | Neighbour read-only | `/home/vgpnk/Projects/shokuknow` unchanged by this lane (`HEAD` + tree) |
| D | Sibling isolation | no sibling `*-shokunin` repo changed by this lane |

## Verdict

| Surface | Literal invariant | Attribution to mado r35 | Severity |
|---|---|---|---|
| A lane writes vs claims | **FAILS** — claim surface rewritten twice mid-wave; 7 lane-authored paths absent from the frozen claim ledger | lane commits authored `mado-shokunin` via jj export | **HIGH** (provenance) / MEDIUM (write scope) |
| B fleet repo | literal "no write" **fails**; **holds** for this lane | all 32 dirty paths + mid-audit commits are hyaku/other-lane | none for mado |
| C shokuknow | HEAD **unchanged**; tree already dirty, bulk-touched 23:26–23:33 | pipeline burst symmetric across ≥10 lanes; no mado-only path | none for mado / MEDIUM to shokuknow hygiene |
| D sibling lanes | **holds** — no sibling change attributable to this lane | 10 siblings committed, every commit authored by that lane or `protocol-shokunin` | none |

No escape from the lane repo was found. No seat wrote to the fleet repo, a sibling, or shokuknow
in any artifact that survives in the tree.

---

## (a) Lane-authored writes vs the round's claims — FAILS closure, then was retro-claimed

### What the round claims to have written

`registration.md` (frozen before data) enumerates exactly: the 3 knowledge entries; 8 rows in
`corpus/SOURCES.md`; 8 receipts `fetch/S203–S210`; `c1/` and `c2/` counters + `frozen.json`;
`c1/clauses.json`; 11 controls under `controls/`; `ledger/RevFrozenBlobs-r35.md`. The wave-2
context adds the seat write contract, verbatim: *"Read-only attacks. Write ONLY under
…/.ufo/waves/round-35/scratch/<YourSeatName>/ and your own report file. Never edit lane corpus
files, counters, controls, SOURCES.md, or the fleet repo, a sibling lane, the lane's jj state or
Git index."*

### Timeline, with commands and exit codes

1. **03:29 — wave start state.** `git -C mado-shokunin status --porcelain` (rc=0) read:
   ` M LOG.md`, ` M corpus/SOURCES.md`, `?? corpus/knowledge/idle-lock-{never-asked-r12,chain-armed-r14,offered-in-the-bar-r15}.md`.
   HEAD `19e4ab3` (2026-10-24 23:24:06). The three entries and LOG.md were **not committed** when
   the wave began, although the C1 counter scores them from the working tree (`--root`).
2. **03:34:26 — HEAD → `02088b4`** (`git reflog`, rc=0): *"round-35: the idle-lock control surface
   lands — three entries, eight rows S203-S210, errata, and the wave-1 evidence"*, 219 files
   (212 under `.ufo/waves/round-35`; `M corpus/{QUALITY,README,SOURCES}.md`; `A` the three entries
   and `corpus/lessons/round-35.md`).
3. **03:35:08–03:39:28 — the corpus files were rewritten again by an unattributed writer.**
   `find … -newermt '2026-10-25 03:34:26'` (rc=0) lists, in the lane outside `scratch/`:
   `corpus/knowledge/idle-lock-never-asked-r12.md` 03:35:08, `…chain-armed-r14.md` 03:35:30,
   `…offered-in-the-bar-r15.md` 03:35:30, `corpus/README.md` 03:35:43, `corpus/QUALITY.md` 03:39:15,
   `corpus/lessons/round-35.md` 03:39:28, and a new `controls-content/` tree 03:39:08 (24 files).
   Reviewers recorded the mutation as it happened: `RevEntryR14.md:4` — *"the file changed under me
   mid-review (1789 B → 2505 B at 03:33:57)"*; `RevEntryR15.md:36` — *"changed under me at 03:35:30"*;
   `RevIndex.md:112` — `corpus/README.md` sha changed under it (`7f348944b0e7…` → `a3769befe355…`).
4. **03:42:04 — HEAD → `4f35c80`** *"round-35: wave-2 falsifications as errata — the shape-scored
   counter"*, 71 files: `M LOG.md, SCORECARD.md`, all six corpus files, `A controls-content/**` (24),
   `A w2/reports/*.md` (39).
5. **03:42:29 — HEAD → `7b745a1`** *"round-35: republish the axis table in the gate's own format,
   plus the wave-2 rep…"* — `M SCORECARD.md` + 5 round-35 paths.
6. **03:43:55 — HEAD → `4efaf63`** *"round-35: checkpoint the 235 seat evidence files and drop the
   3.2 GB mutant tree"* — the seats' `scratch/` tree is renamed to `scratch-evidence/` and committed,
   so the very path the wave-2 contract names as the only allowed write target ceased to exist
   mid-wave. At **03:45** the lane tree is clean except `?? .ufo/waves/round-35/w2-plan.err` and
   reports the seats are still editing.
7. **03:45:15 — HEAD → `8889bdc`** *"point the digest-repair receipt at the commit that keeps it
   (the working tree was cleaned)"* — `M corpus/lessons/round-35.md` only; the three entries and
   `SOURCES.md` are untouched here.
8. **03:46:02 — HEAD → `b632f0b`** *"the last two seat reports, the seats' revised reports, and the
   scratch-evi…"* — reports/evidence only.

Verified at 03:46: `git diff --numstat 4f35c80..HEAD -- corpus/knowledge corpus/SOURCES.md` → empty
(rc=0), and `git diff --stat 4f35c80..HEAD -- corpus` → `corpus/lessons/round-35.md | 3 ++-`.
So **the claim data is pinned at `4f35c80`** while the tree keeps moving.

### The reproducible defect

Any reviewer that read the entries before 03:42:04 reviewed bytes that exist in no commit. For the
`02088b4` snapshot the scored blobs differ from the working tree (sha256, first 16):

| path | at `02088b4` | working tree (pre-`4f35c80`) |
|---|---|---|
| `idle-lock-never-asked-r12.md` | `21c1d06db35d189b` | `7f27ced01e9edf62` |
| `idle-lock-chain-armed-r14.md` | `31275b4d84f7b34f` | `583c708c338ecb06` |
| `idle-lock-offered-in-the-bar-r15.md` | `1594a36fbfc57f43` | `82c08a4675863f69` |
| `corpus/README.md` | `a3769befe3558c54` | `3bb9865fd12793f9` |

C1 is scored with `--root` against the live tree, so the claim is evaluated against a surface that
mutated mid-attack. A verdict that does not pin a commit is not reproducible.

### Files lane-authored but not claimed by the frozen ledger

All are now committed, and all are absent from `registration.md`'s enumerated set; they are claimed
only retroactively, by the `4f35c80` message and by the new QUALITY criteria 55–56:

1. `LOG.md` — +36 lines, the `SimplifyCounter` wave-1 block (mtime 2026-10-24 23:31:34). `ScribeLog.md:4`
   states *"The lane `LOG.md` was NOT"* modified, and `SimplifyCounter.md` never mentions it.
2. `SCORECARD.md` — +2 lines (committed in `4f35c80`).
3. `corpus/README.md` — 28-line diff in `4f35c80`; `ExecIndex.md` only *proposed* the three rows.
4. `corpus/QUALITY.md` — criteria 55–56 added (committed `02088b4`), then edited again 03:39:15.
5. `corpus/lessons/round-35.md` — 126-line diff in `4f35c80`; `RevLessonGate.md:16` tracks three
   versions of it but no seat declares the write.
6. `.ufo/waves/round-35/assimilation/**` — 10 files committed in `02088b4`, no ledger entry.
7. `.ufo/waves/round-35/controls-content/**` — 24 files committed in `4f35c80`, outside the frozen
   `controls/` directory that the registration table enumerates.

Verified **stable** (claimed and byte-unchanged): the 8 receipts (mtime 23:21), `c1/c2 count.py` and
`frozen.json` (23:22–23:23), and `SOURCES.md` rows `S203`–`S210` (`grep -c '^\| S2(0[3-9]\|10) '` → 8, rc=0).

### Exploit path (not executed, derived from tree state)

C1 scores *shape*: entry regular-file, exactly one well-formed row, digest-anchored quote. The round's
own new criterion 55 names the gap — a shape-only tree with present rows and gate-quote lines and
absent prose still passes. The 03:35–03:39 window is a live proof that `corpus/` is writable during
the wave: a writer can append prose-withdrawing errata (as happened) and keep `closed_entries=3
closed_rows=8 open_cites=0` intact. The committed `controls-content/c1-fabricated-payload/` tree now
ships eight receipt files with the real `S203..S210` names and wrong payloads; it is one
breadth-first `**/fetch/S20*.receipt.txt` away from poisoning a copied root or a glob census.

### Impact

- Reviewer verdicts keyed to pre-03:42 bytes are unreproducible from HEAD; the "frozen data" was not frozen.
- A fabricated-receipt tree is now tracked inside the lane.
- Claim ledger and artifact set disagree: 7 committed paths are unclaimed.

### Smallest remediation

1. Pin the claim data to `4f35c80` — the three entries and the `SOURCES.md` rows are byte-identical
   from `4f35c80` through `b632f0b` (`git diff --numstat 4f35c80..HEAD -- corpus/knowledge
   corpus/SOURCES.md` empty, rc=0) — record the three entry blob ids, and re-run both counters
   against an export of a named commit, not the mutable worktree.
2. Move `controls-content/` under the seat evidence dir (`.ufo/waves/round-35/scratch-evidence/CritControls/`)
   **or** add it to the registration control table; then re-run the receipt census to prove no forged
   receipt is reachable from the scored root.
3. Add the seven paths above to the round ledger, or revert `LOG.md` and `SCORECARD.md`.

---

## (b) Fleet repo containment — holds for this lane

```sh
$ git -C /home/vgpnk/Projects/shokunin status --porcelain -uall | grep -c '\.ufo/reports/round-35/'
0                       # rc=1 (grep, no match)
$ git -C /home/vgpnk/Projects/shokunin status --porcelain -uall | grep -vc '\.ufo/reports/round-35/'
32                      # rc=0
```

- `.ufo/reports/round-35/` exists with **8** files (chousa, kake, kama, kotodama, kumitate, mori,
  tameshi, tsukuroi); newest `kama.md` 2026-10-24 21:32. `find .ufo/reports/round-35 -newermt
  '2026-10-24 22:00'` → empty (rc=0). **No file written by this round**, and no mado report in it.
- mtimes of all 32 dirty entries: 17 at 2026-10-24 18:07; then `scripts/hyaku/hyaku.env` 03:22:37,
  `.scratch/goal-20261025-hyaku-12h.md` 03:22:48, `scripts/hyaku/lane-addendum.md` 03:23:06, six
  `.ufo/state/*.report-baseline` + `.ufo/watchdog.log` 03:23:32–03:23:48. All precede the 03:28
  wave-2 dispatch and are hyaku dispatch prep (the `hyaku.env` diff pins `L1_MODEL`/`JUDGE_MODEL`
  to `@m_flash` per the operator directive).
- The fleet HEAD is *not* quiescent: it moved during the audit (`04411e8` → `8052650d` 03:33:51 →
  `3f8b0d1` 03:40:22), every commit a hyaku closure for another lane (kama r36, kaidoku r34, tabi
  r22). `MANIFEST.json` is content-identical to HEAD (`git diff` empty).
- Grep of mado w1/w2 reports for write redirections into the fleet root: 0 hits.

**Verdict:** the literal "no write landed outside `.ufo/reports/round-35/`" is false because the
fleet repo is a shared, live commit target for all lanes; **no write is attributable to mado round 35**.

---

## (c) `shokuknow` read-only — HEAD unchanged, tree was already dirty and bulk-touched

```sh
$ git -C /home/vgpnk/Projects/shokuknow rev-parse HEAD
8b94c5c12c0521e4cd9ed8e5b6939afd8518c715        # rc=0
$ git -C /home/vgpnk/Projects/shokuknow reflog -3
8b94c5c1 HEAD@{2026-10-24 11:02:02 -0300}: commit: Stage wave 13: …
$ git -C /home/vgpnk/Projects/shokuknow status --porcelain -uall | wc -l
5217                                            # rc=0
$ git -C /home/vgpnk/Projects/shokuknow diff --shortstat
 1429 files changed, 20904 insertions(+), 14907 deletions(-)   # rc=0
```

- **No commit since 11:02:02** — the branch tip is unchanged by this round.
- The working tree was already dirty before round 35 (oldest changed path 16:47:38; `HEAD` is 11:02).
- 1999 changed paths carry mtime > 2026-10-24 23:18, in a single 23:26:45–23:33:21 burst that is
  **symmetric across lanes**: lanes/mado 116, mori 109, kake 107, kotoba 106, kumitate 105, chousa
  103, revenger 99, kama 97, tameshi 96; `merge/*` mirrors each lane; `shokuknow/MANIFEST.json`
  23:33:21. The writer is the repo's own corpus-expansion pipeline
  (`.ufo/waves/corpus-expansion-1/{audit-wave.py,build-wave3.py,quote-lint.py}`, mtimes 23:2x–23:33).
- Only non-symmetric post-wave write: `lanes/tabi/round8/.work/ratelimit-series.tsv` 03:38:09 (tabi's
  own round 8).
- `lanes/mado/**` newest = 23:26:45 (the bulk); no mado-only path after it.
- Mado artifacts contain **zero** write redirections into shokuknow; `MutC2Real.md:199` and
  `ScribeLesson.md:9` both affirm it was not written or executed against.

**Verdict:** "unmodified" fails literally (dirty tree + bulk mtime burst); **"unmodified by this
lane" holds** on the available evidence — symmetry across ten-plus lanes, no mado-only path, no
write reference. [INFERENCE: mtime symmetry cannot exclude a mado read that triggered a pipeline
write; no such invocation appears in any seat artifact.]

---

## (d) Sibling lanes — no change attributable to this lane

21 sibling repos, each its own git. Dirty counts at 03:43 (`status --porcelain -uall | wc -l`):
kagi 770810 (fixture churn), kama 821, souji 186, kake 90, kumitate 85, tameshi 28, kasegi 27,
kotoba 24, kotodama 23, audio 12, kengaku 4, chousa 3, revenger 2, and 0 for game-dev-2d/3d,
kaidoku, lore, mori, tabi, tsukuroi; mado's own 6832 is this round's scratch.

Commits since 2026-10-24 23:18 (`rev-list --count --since … HEAD`, rc=0):
kake 3, kasegi 1, kengaku 1, kotoba 1, kotodama 3, kumitate 1, mori 3, revenger 5, tabi 3,
tameshi 1; mado 2. Authors are the lane itself or `protocol-shokunin` (hyaku integrator), e.g.
`1429c791 protocol-shokunin | round-43 verifier spot-check (integrator, hyaku)`.

```sh
$ for d in …/*-shokunin; do git -C "$d" log --all --author=mado --format=x; done
# no output, rc=1 — zero mado-authored commits in any sibling
```

Grep of mado artifacts for write redirections into any `*-shokunin` path: 0 hits. The 21 siblings
are independently active in the same window (their own rounds 22–69), which is normal fleet
behaviour, not an overlap.

**Verdict:** **holds** — no sibling lane changed by this round.

---

## Notes

- No installs and no package transactions were attempted; the host-wide PACMAN pause was irrelevant
  to this audit (no tooling needed beyond git/find/stat).
- One `/tmp` buffer (70-line status snapshot) was created by this seat and removed at 03:44; nothing
  else was written outside `.ufo/waves/round-35/scratch-evidence/SentBoundary/` and this report.
  Note the path move: this seat wrote `scratch/SentBoundary/evidence.txt`, and commit `4efaf63`
  renamed the whole `scratch/` tree to `scratch-evidence/` and committed it at 03:43:55.
- At ~03:45 an external sweep deleted the `scratch/` directories the contract names as the only
  allowed write target; twelve seats have since recreated directories there. This seat's evidence
  survived only because `4efaf63` had committed a copy to `scratch-evidence/` shortly before the
  sweep. The allowed write target was mutated out from under the wave, twice (`scratch` →
  `scratch-evidence` → deleted).
- `git status` may refresh `.git/index` stat data; that is a read-side cache touch, not a content write.
- This report does **not** re-score C1/C2 — that is the mutation seats' surface. It records only that
  the bytes those counters read were committed twice during the wave (03:34:26, 03:42:04) and the
  claim data is stable from `4f35c80` onward.
