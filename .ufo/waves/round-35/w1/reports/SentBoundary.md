# SentBoundary — mado r35 w1 seat write-scope check

Seat: sentinel (leaf, no dispatch). Date: 2026-10-24. Snapshot window: wave
dispatched 23:25:23 local (w1 logs/prompts), check run 23:26–23:35 local. **The
wave is still in flight** (≈10 of 64 seats unreported at write time); this is a
mid-flight boundary audit, not a post-wave closure.

Write contract (w1-spec.json context, verbatim): "A seat may write ONLY (a) its
own report at the path named in its Report trailer, and (b) its own scratch
directory under …/.ufo/waves/round-35/scratch/<your seat name>/. Seats NEVER
mutate the fleet repo, sibling lanes, lane jj state, or the lane Git index."

## Verdict

**Hold, with two in-scope deviations.** No confirmed seat write under the fleet
root outside `mado-shokunin/`; no sibling lane repo touched by a mado seat; no
file-level jj or git mutation in the lane after dispatch; all writes inside the
lane sit under `.ufo/waves/round-35/`. Two deviations from the seat write
contract, both inside tolerated surfaces:

1. **Six seats wrote to `/tmp` instead of their scratch dirs.** All declared in
   their own reports/logs except two unattributed id files.
2. **Five probe mirrors sit at `scratch/<Probe*>/` root level** instead of
   under a `scratch/<SeatName>/` dir — a naming violation, same-time-stamped as
   `scratch/RevValidate`, almost certainly that seat's adversarial-probe trees.

## Commands run and observed output

### 1. Fleet root outside mado — files written since 23:00

```sh
cd /home/vgpnk/Projects/shokunin
find . -maxdepth 1 -type f -newermt '2026-10-24 23:00' -printf '%T+ %p\n' | sort
find . -maxdepth 2 -mindepth 2 -newermt '2026-10-24 23:15' ! -path './mado-shokunin/*' -printf '%T+ %y %p\n' | sort
find .ufo -maxdepth 3 -newermt '2026-10-24 23:15' -printf '%T+ %y %p\n' | sort
for d in *-shokunin tameshi-shokukin; do find "$d" -maxdepth 1 -newermt '23:15' -printf '%T+ %y %p\n'; done
```

Observed (full list): `MANIFEST.json` 23:05 (pre-dispatch, fleet driver);
`.ufo/watchdog.log` 23:17; `.ufo/prompts/closure/{kama-round-36,kotoba-round-68}.md`
23:17; `.ufo/reports/round-68/kotoba.md` 23:15, `round-43/mori.md` 23:21,
`round-60/kumitate.md` 23:22; `.tower/comms` 23:25; fleet `.git/HEAD`+`.git/objects`
23:31:12, `.git/index` 23:31:13, `.jj/working_copy/tree_state` 23:31:12 —
a fleet-repo jj snapshot/commit by the driver. Sibling lane writes: kumitate
`SKILL.md` 23:15, `PROVINCE.md` 23:19, `LOG.md` 23:19+23:41, `SCORECARD.md`
23:25; mori `SCORECARD.md` 23:18, `LOG.md` 23:19; kake `LOG.md` 23:23;
revenger `corpus/` 23:19, `reports/` 23:20. Sibling `.git` dir mtimes bumped
in a burst at 23:26:24–23:26:34 (audio, tameshi, chousa, kama, mori, kotoba,
revenger, kake), kumitate 23:30:36, kotodama 23:31:55 — consistent with the
fleet driver's jj-colocate sweep across live lanes, each of which had an
in-flight round this window (mori-r43, kumitate-r60, kotoba-r68, kama-r36
closure prompts above). `/tmp` corroborates: `mori-r43-*`, `kumitate-r60/*`,
`kama-r36-*`, `kake-r51-*` dirs are sibling seats' scratch (fleet seats use
`/tmp`; see deviation 1).

**Nothing matches a mado-r35 seat**: every named artifact names a sibling
lane/round; no write in any sibling lane's `corpus/`, `LOG.md`, `SCORECARD.md`,
`SKILL.md`, `sources`, or `.ufo/` names mado or carries a mado path. A full
recursive `find` of the fleet root timed out at 300 s (fleet tree is ~100 k+
files), so coverage is maxdepth-bounded: level-1 files, level-2 dirs, `.ufo`
to depth 3, sibling lane roots. A seat writing a file nested deeper inside a
sibling lane would evade this sweep — flagged as the one coverage gap.

`/home/vgpnk/Projects/shokuknow` (declared read-only in the context) received
2 804 writes since 23:15, including `lanes/mado/**` and `merge/mado/**` at
23:26:45–23:26:50 — but every file sits inside a bulk regeneration sweep that
touched `merge/` (1 761 files) and `lanes/` (985 files) for *all* lanes in the
same second, i.e. the campaign-side corpus-expansion packaging run, not a mado
seat. Command:

```sh
find /home/vgpnk/Projects/shokuknow -xdev -newermt '2026-10-24 23:15' \
  \( -path '*merge/mado*' -o -path '*lanes/mado*' \) -printf '%T+ %y %p\n' | sort
# 195 mado-area entries, all inside the 23:26:45–23:26:50 bulk-regen burst
```

### 2. Lane production surface — untouched

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
find . -xdev -newermt '2026-10-24 23:15' ! -path './.ufo/waves/round-35/*' \
  ! -path './.jj/*' ! -path './.git/*' -printf '%T+ %y %p\n' | sort
```

Output: only `.ufo/waves` (dir mtime, round-35 creation), `.ufo/waves/round-35`,
`.git` (dir mtime, transient lock — see §3). **Zero file writes** to `corpus/`,
`considerthese/`, `quality/`, `tools/`, `LOG.md`, `SCORECARD.md`, `SKILL.md`,
`PROVINCE.md`, `SHONEN.md`, `plans/`, `reports/`, `README.md`, `MINT.md` since
23:15. LOG.md/SCORECARD.md last modified 22:4x (round-34 lead), before the wave.

### 3. Lane jj state and Git index — no content mutation post-dispatch

```sh
find .git -xdev -newermt '2026-10-24 23:25:10' \( -type f -o -type l \) -printf '%T+ %s %p\n'
find .jj -xdev -newermt '2026-10-24 23:25:10' -printf '%T+ %y %p\n'
find .git/objects .git/refs .git/logs -xdev -newermt '2026-10-24 23:24:10' -printf '%T+ %y %p\n'
find .jj -type f -newermt '2026-10-24 23:24:10'
find .git .jj -name '*lock*'
```

Observed:

- `.git/index` rewritten 23:25:56 (1 294 896 B — index refresh; could be a
  stat-cache refresh by a read-only `git status`, or a harmless `git add` of
  unchanged content). **No objects, refs, or reflog entries written** after
  23:24:10 — nothing was staged that differs, committed, or pushed.
- `.git` dir mtime 23:28:03 — transient `index.lock` create/remove.
- `.jj/repo` and `.jj/working_copy` dir mtimes 23:28:43 — transient lock files;
  **zero file-level writes under `.jj/` after 23:24:07**. Last real ops
  (`op_store`, `tree_state`, `checkout`) are the L1's pre-dispatch freeze
  commit at 23:24:06–23:24:07.
- No `*.lock` residue present at check time.

Attribution: the actor is unidentified (seat or L1 running `git status`/`jj
st` in-lane). Effect is confined to stat-cache refresh + lock-file churn; the
jj operation log and git object store carry no post-dispatch writes, so no
mutation landed. Host probed paths seats were told are read-only
(`~/.local/share/omarchy`, `~/.config/waybar`, `~/.local/state/omarchy`) —
`find` since 23:15 returned **zero writes**.

### 4. Inside the wave dir — every write is allowed or attributed

```sh
find c1 c2 controls fetch ledger registration.md w1-spec.json w1-taskcall.json \
  dispatch-w1.sh dispatch.out -newermt '2026-10-24 23:25:10' -printf '%T+ %y %p\n' | sort
# only w1-taskcall.json 23:25:14, dispatch-w1.sh 23:25:20, dispatch.out 23:25:23 (dispatcher)
```

```sh
python3 - <<'PY'
import os
plan={l.split('\t')[0] for l in open('w1/seat-plan.tsv') if l.strip()}
reps={f[:-3] for f in os.listdir('w1/reports') if f.endswith('.md')}
print('reports not in plan:', sorted(reps-plan))
print('scratch dirs not in plan:', sorted(set(os.listdir('scratch'))-plan))
PY
# reports not in plan: []
# scratch dirs not in plan: ['ProbeEscPipe','ProbeProseLine','ProbeRecheckAlpha',
#                            'ProbeRecheckPunct','ProbeTailAppend']
```

- `w1/reports/` contains only planned `<Seat>.md` files plus the fleet's
  `swarm-registry.json`. No stray report names.
- `w1/logs/` and `w1/prompts/` hold only dispatcher-owned seat files.
- Frozen surfaces (`c1/`, `c2/`, `controls/`, `fetch/`, `ledger/`,
  `registration.md`, `w1-spec.json`) carry **no writes after 23:25:10** —
  every file there predates dispatch.

## Deviation detail

**(a) `/tmp` writes by seats** — seat-declared unless noted:

| Path | mtime | Seat |
|---|---|---|
| `/tmp/rr35/{recheck.sh,fresh/}` | 23:28:39 | ExecRecheck (report: "rebuilt into `/tmp/rr35/fresh/`") |
| `/tmp/r35-rev/*.stderr` | 23:27:27 | RevReceipts (control-receipt stderr captures) |
| `/tmp/revenge-r35/count-*.py` | 23:31:14 | RevengerRepair (report: "counters built in `/tmp/revenge-r35`") |
| `/tmp/r35-scribe/r34tree/` | 23:29:18 | a Scribe* seat's r34 mirror (declared pattern, seat name unconfirmed) |
| `/tmp/revdedup-lane/` | 23:29:14 | RevDedup (report: "scratch mirror at `/tmp/revdedup-lane` (symlinked lane root)") |
| `/tmp/mado-registry.ids`, `/tmp/mado-staged.ids` | 23:25:41 | unattributed; contents = S001–S202 and S197+ id lists → ScoutReg / ScoutStaged work product |

`/tmp/revdedup-lane` is a symlink forest pointing **into** the lane — reads
through it hit lane files; harmless (read path only) but it is a live alias to
the production tree.

**(b) `scratch/Probe*` trees** — `ProbeEscPipe`, `ProbeProseLine`,
`ProbeRecheckAlpha`, `ProbeRecheckPunct`, `ProbeTailAppend`, all mtime
`23:29:44.992411798`, identical nanoseconds to `scratch/RevValidate`. They are
full lane mirrors whose mutations match RevValidate's five published probe
rows (escaped pipe, prose-line, alphabetic recheck, punctuated recheck,
tail-append). Content attribution: high confidence RevValidate. Contract text
says `scratch/<your seat name>/` — these sit one level up. No file outside
`scratch/` was touched by them.

## Caveats

- Wave in flight; ten seats had not reported. A late seat can still violate.
- The fleet sweep is depth-bounded (see §1); a deep-file write inside a
  sibling lane would not be caught.
- `/tmp` id-file attribution is inferred from contents, not declared.
- Nothing was cleaned up, per seat instructions.
