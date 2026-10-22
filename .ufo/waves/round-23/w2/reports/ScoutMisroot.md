# ScoutMisroot — misroot sweep (wave 2, read-only)

Observed 2026-10-22 08:54–09:05 -03. Fleet root `shokunin` at `080ea43` (2026-10-22 08:59:39 -03);
lane `mado-shokunin` at `2f1134f3` (= `2f1134f38930fc8b067d2d7f5bba126338faabdd`). No file was
deleted, no lane file was written except this report, no tool was installed, no pacman transaction
was attempted (`pacman -Q` was not even run).

## Commands actually run (condensed)

```
git -C /home/vgpnk/Projects/shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all
git -C /home/vgpnk/Projects/shokunin ls-files -o --exclude-standard
git -C /home/vgpnk/Projects/shokunin ls-files -o -i --exclude-standard
git -C /home/vgpnk/Projects/shokunin status --porcelain=v1 | cat -A
git -C /home/vgpnk/Projects/shokunin ls-files --stage --debug -- <paths>
git -C /home/vgpnk/Projects/shokunin diff --cached --stat ; git diff --stat -- <paths>
git -C /home/vgpnk/Projects/shokunin check-ignore -v 'bash: '
git -C /home/vgpnk/Projects/shokunin ls-tree HEAD -- <paths> ; git ls-files -s -- <paths>
git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain --untracked-files=all
git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain --hash --ignored=matching --untracked-files=all
find .../mado-shokunin/tools .../mado-shokunin/.ufo/waves/round-23 -type d -name __pycache__
find .../mado-shokunin/.ufo/waves/round-23 -name '*.pyc' -printf ...
python3 -I - <<'EOF'  (marshal.loads of each pyc header+body to read the recorded source stat; nothing executed)
grep -lI -E 'MadoR23|mado...r23' over untracked path lists (literal text fallback; no LSP server
   applies to this question — it is a filesystem/git-state question, not a symbol question)
sha256sum / stat over the lane tool, its pyc, and every /fast/scratch/hyaku/mado-r23/*/tools/mado-tripwire.py
```

One broad `grep -rI MadoR23` over *all* untracked-ignored fleet-root paths (including the `.jj/repo`
object store) was backgrounded and killed at the 300 s cap without finishing. It was replaced by a
completed scan of the 199 untracked paths outside `.jj/` and outside `mado-shokunin/` (every regular
file in that list grepped); result: 0 hits. The `.jj` store itself was excluded by design.

## 1. Fleet-root untracked inventory

`git status --porcelain` (09:04):

```
 A .scratch/goal-20261022-hyaku-12h.md
 M .ufo/state/chousa.report-baseline        (also kagi, kaidoku, kake, kama, kengaku,
 M ..                                        kumitate, mado, mori, tameshi, tsukuroi)
 A .ufo/state/kotoba.report-baseline
 A .ufo/state/kotodama.report-baseline
 A .ufo/state/revenger.report-baseline
 M .ufo/watchdog.log
 A scripts/hyaku/__pycache__/append-closure.cpython-314.pyc
 A write
?? .ufo/waves/round-49/
```

The seven ` A` lines are **intent-to-add, not committed**: each index entry is the empty blob
`e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`, `git ls-files --stage --debug` shows flags `0x20004000`
(CE_INTENT_TO_ADD), `git diff --cached` is empty, and `git diff` presents the whole file as new.
So these files exist only in the worktree and are untracked with respect to HEAD.

Non-ignored untracked (`??`), exactly one path:

- `.ufo/waves/round-49/falsify/RowGameDev2d.md` — 97 lines, kotoba `game-dev-2d` census
  falsification. Contains no `mado`, no `round 23`, no `MadoR23`.

Ignored-untracked at the fleet root: 320 status entries (git collapses wholly ignored directories).
Grouped: `.jj/repo` 116, `.tower/comms` 96, `.tower/quarantine` 41, `.ufo/waves` 36,
`.jj/working_copy` 3, `.tower/jj-probe` 2, one collapsed entry per `*-shokunin/` lane repo.

Empty directory `bash: ` (literal name, trailing space) with nested `bash: /home/vgpnk` — all
directories, no files, so git cannot represent it and it appears in no status output; mtime
2026-10-18. It carries no `mado`/`round 23` content. Reported as a pre-existing root artifact,
not a round-23 one.

## 2. Fleet-root untracked files naming mado + round 23 (or a MadoR23 seat)

**One match: `.scratch/goal-20261022-hyaku-12h.md`** — 247 lines, 17 367 B, intent-to-add.
Evidence:

```
109:| D11 | mado (r23) | Recovery round under the operator ruling below. |
214:- **Rejection-streak holds (mado, kumitate).** Each gets ONE repair-first recovery round, at D10
216:  mado r22). The round's first claim repairs its routed harms. If that round is rejected, restore
```

It names `mado (r23)` and the r23 recovery policy, but contains no literal `MadoR23` seat id.
That is a fuzzy-content match on "mado" + "round 23", not a seat-name leak.

No other fleet-root untracked file matches:

- `write` (25 B, exact bytes `agent://U100N079H334f935b`, no trailing newline; od-verified) is a
  stray write-tool artifact, and the URI is **not** a MadoR23 seat: `.ufo/waves/hyaku/s3-unjoined100/
  dispatch.json:884` records it as `"role": "scout"` and the payload at line 1532 carries
  `"lane": "kotodama"`. `kaidoku-shokunin/.ufo/waves/round-25/a3/w1/FleetMisrootPrecheck.md:73-78`
  already adjudicated it: "stray, not kaidoku round 25 ... a seat ... passed a message id as a file
  path named `write`." So it does not satisfy the "MadoR23 seat" branch either.
- `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` — bytecode of
  `scripts/hyaku/append-closure.py` (strings: "hyaku append-closure", "append one closure entry to
  MANIFEST.json"); no `mado`/`round 23`/`MadoR23` bytes.
- `.ufo/state/kotoba.report-baseline`, `.ufo/state/revenger.report-baseline` — no match.
- `.ufo/waves/round-49/**` — no match.
- No untracked file outside the lane names `MadoR23` or a `MadoR23.*` seat (completed scan above).
  The only untracked files that do are the lane's own round-23 reports under
  `mado-shokunin/.ufo/waves/round-23/`, which is expected, not misroot.

## 3. Lane untracked files outside `.ufo/waves/round-23/`

- Strict non-ignored untracked (`??`): **0**.
- Ignored-untracked status entries: **312**, none created by round 23 except one:
  - `.ufo/waves` 307 entries (round-20 167, round-18 103, round-19 31, round-22 3, round-21 3) —
    fetch caches and older `__pycache__` from rounds 18–22;
  - `tools/__pycache__` 1 entry — **created 08:51, i.e. during round 23** (see §4);
  - `.ufo/interactive-sessions` 1, `.jj/.gitignore` 1, `.jj/repo` 1, `.jj/working_copy` 1 — jj
    colocated-store internals, not seat output.
- Entries whose path mtime is 2026-10-22 (today): `.jj/repo` (08:49), `.jj/working_copy` (08:49),
  `tools/__pycache__` (08:51→09:00). Nothing else.

No round-23 seat wrote a report or scratch file outside `round-23/` except the
`tools/__pycache__` directory below.

## 4. `__pycache__` directories under `tools/` and `.ufo/waves/round-23/`

Current set (the set is growing while wave 2 runs; snapshot 09:04:02):

| dir (created) | file | size | recorded source (pyc header) | verdict |
|---|---|---|---|---|
| `.ufo/waves/round-23/w1/out/CritFrameNeighbour/__pycache__` (08:03) | `base-mado-tripwire.cpython-314.pyc` | 232 648 | 162 432 B @ 08:03:08 | header matches `base-mado-tripwire.py` (162 432 B @ 08:03:08) |
| `.ufo/waves/round-23/c2/__pycache__` (08:44) | `count.cpython-314.pyc` | 7 353 | 3 870 B @ 08:11:35 | header matches `c2/count.py` (3 870 B @ 08:11:35) |
| `.ufo/waves/round-23/evidence/__pycache__` (08:57) | `tool-base-cd9da20c.cpython-314.pyc` | 232 631 | 162 432 B (base copy) | base-classifier bytecode beside the evidence copy |
| `.ufo/waves/round-23/w2/out/AttackPerf/__pycache__` (08:58) | `tool-base.cpython-314.pyc`, `tool-tip.cpython-314.pyc` | 232 631 / 245 876 | 162 432 B / 173 707 B @ 08:55:42 | both headers match their `tool-base.py` / `tool-tip.py` copies |
| `tools/__pycache__` (08:51, rewritten 09:00:32) | `mado-tripwire.cpython-314.pyc` | 249 423 | **175 636 B @ 08:59:14** | **MISMATCH** vs current `tools/mado-tripwire.py` 176 289 B @ 09:04:12 |

Everything above is covered by the lane `.gitignore` rule `__pycache__/`, so none of it is
untracked-non-ignored. A file run as `__main__` does not get a cache entry, so a `__pycache__`
beside a source implies a module import or an explicit compile (the w1 BaseCorpus seat's
`06-pyc-stale-probes.txt` established that `python3 -I` will still create and then *use* a stale
cache for an import).

The `tools/__pycache__` entry is the interesting one: at 08:49 the worktree tool was the tip bytes
(173 707 B, sha256 `41489991…`) and the pyc matched them; by 08:59:14 a 175 636-byte state existed;
by 09:00:32 the pyc had been regenerated against it (249 423 B, header source 175 636 B). It is now
stale against a source that has moved on twice (§5). Its creation is inside the lane and outside
`round-23/`, i.e. lane-side build residue rather than an evidence artifact.

## 5. Live, unowned mutation of the judged artifact (outside the untracked scope, calibration-critical)

`tools/mado-tripwire.py` is **not** at tip in the working tree, and it is being rewritten while
wave 2 runs. Observed states:

| time | size | sha256 | diff vs tip | notes |
|---|---|---|---|---|
| 08:49:30 (tip bytes) | 173 707 | `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009` | — | equals `git cat-file` of `2e592af`, `2f1134f3` and HEAD blob `3f6e1766…` |
| 09:01:03 | 174 005 | `82d5ffa81c558ccc9a855d9ced7f50a2c97e31e647cbb2e7aa1f5957f8862a57` | +72/−33 | equals `/fast/scratch/hyaku/mado-r23/L1-fix3/tools/mado-tripwire.py` (same bytes, 09:01:12) |
| 09:03:40 | 175 765 | `4a2e92a00b810ec0d727f25d714bf336164bad610d76c7a3fff011d3a7387ba4` | +87/−49 | no scratch copy with these bytes among `mado-r23/*/tools/` at 09:04:20 |
| 09:04:12 | 176 289 | `eeb6f515bf68ecdd11b16f03a0b622e90fac9aec3182c79f94a6fba7c0573bad` | +97/−51 | still moving at report time |

The diff is the `parameter_escapes` rewrite to an allowlist whose docstring cites "round-23 wave-2
counterexamples"; `/fast/scratch/hyaku/mado-r23/L1-fix2/tools/mado-tripwire.py` holds the
intermediate 175 636-byte state (sha256 `8975a4da…`, 08:59:21) that the pyc header records.
So the writer is the L1's own fix line (`L1-fix2` → `L1-fix3` → …) — not an executor clone — and it
is applying those bytes to the lane working tree in place.

Why this matters for calibration: receipt `evidence/repair-after-2f1134f3.json` records
`tool_sha256: 41489991…`, and every wave-2 report I read (e.g. `AttackFrameScopes.md:7`,
`ReFrameNeighbour.md:5`) extracts the tip with `git show 2f1134f3:tools/mado-tripwire.py`. Those are
sound. But any check that reads `tools/mado-tripwire.py` from the working tree after 09:01 measures
unmounted bytes, and the w1 BaseCorpus lane-state receipts (`02-lane-pre-state.txt` /
`09-lane-final-state.txt`, both recording pyc sha256 `d6f3ef21…`) no longer describe the current
tree. Two wave-2 reports that expressly disclaim lane edits (`ReRepair.md:109` "No lane files were
modified other than this report"; `AttackEscapeGate.md:135` "I edited no lane file") are not the
source, but the lane is not "clean at tip" either.

Tracked-but-dirty outside `round-23/` (not untracked; reported because it bears on tip-vs-worktree):
`SKILL.md` +8 lines @ 08:51:24 and `corpus/README.md` +13 lines @ 08:51:13, both after the three
C-commits (08:49:38 / 08:49:46 / 08:49:48), so those doc additions are **not** in tip.

## 6. Unresolved

- The lane tool kept changing during the sweep (last observed 09:04:12); the table in §5 is a
  window, not a final state.
- The broad all-untracked ignored-content scan over `.jj/repo` timed out; the completed replacement
  scan covered every untracked path outside `.jj/` and `mado-shokunin/`.
- Other `*-shokunin` lane repos were treated as out of scope (they are separate repositories, and
  the fleet root lists each as one ignored directory); no cross-lane write was observed in the
  fleet-root scan, but their own untracked sets were not enumerated.
- A walk of regular files outside the lane with mtime after 06:00 today was cut off by a 120 s cap
  after listing 2671 paths (an earlier attempt printed 2680 before the 300 s cap). Grepping that
  partial list for `MadoR23` found exactly one file: `.ufo/waves/hyaku/PHASE3.md` — tracked, clean
  at HEAD (index blob `3408d55e`), whose line 308 records "Dispatch mado r23 attempt 1 (recovery)
  ... L1 `MadoR23`". That is a coordinator log entry, not a misroot. The "no MadoR23 outside the
  lane" result therefore holds for untracked paths (the assigned scope); the only tracked
  out-of-lane mention seen is this expected file, and the truncated remainder of the tracked set
  was not scanned.
- No copy direction is proven for the 09:01:03 bytes shared by the lane and `L1-fix3` (identical
  content, mtimes 9 s apart).

## Verdict

Fleet-root untracked files naming mado + round 23: **one**, `.scratch/goal-20261022-hyaku-12h.md`
(intent-to-add, content-only, `mado (r23)` policy text; no `MadoR23.*` seat id in any untracked
path outside the lane — the sole `MadoR23` mention outside it is the tracked hyaku coordinator log
at `.ufo/waves/hyaku/PHASE3.md:308`; the stray `write` file belongs to a kotodama hyaku scout, not
MadoR23). Lane untracked
files outside `.ufo/waves/round-23/`: **0** strict, 312 ignored entries of which only
`tools/__pycache__` (08:51, regenerated 09:00:32) is round-23 residue. `__pycache__` under
`tools/` and `round-23/`: **five** directories (tools, evidence, c2, w1/out/CritFrameNeighbour,
w2/out/AttackPerf), all header-matched to their sources except `tools/`, which is stale against a
working-tree classifier that was itself rewritten three times after the tip commit and is still
moving. Nothing deleted; nothing fixed.
