# Sources & frontier — round 36

## Census before → after

Command, run at round start and round end (the same invocation as round 35:

`sources-census.sh validate`):

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

**Before** (round start at the freeze commit `dbf8b57`, 200 data rows), exit **0**.
Output quoted from `corpus/lessons/round-35.md` §Gate "Census before → after"
(lines 49–57 — round 35's after-block; see below for the re-run):

```text
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

**After** (round end at the tip, 201 data rows), exit **0**. Re-run by this seat
at the tip, with the row count by the census clause:

```sh
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
$ echo $?
0
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
201
```

Row count by the census clause: **200 → 201**. The same seven pre-existing `W04`
warnings on old ids (S030…S121), no finding on the new row, same `mado ok`
trailer, exit 0. The round-35 lesson's *after*-block is quoted as the before-state
because the freeze commit's `SOURCES.md` blob is byte-identical to the round-35
tip's (`git diff 7a068cb dbf8b57 -- corpus/SOURCES.md` is empty — `RevCensusNow`
verified the worktree at the freeze matched the lesson's after-block byte-for-byte,
including the row count of 200).

## Rows added by tier

One row, tier **A**: `S211` (`corpus/SOURCES.md:213`) — *Negative controls: a tool
for detecting confounding and bias in observational studies* (Lipsitch, Tchetgen
Tchetgen, Cohen; PMC3053408 author manuscript, *Epidemiology* 2010;21(3):383–388),
`status=mined`, opened 2026-10-25, `used-by` exactly `corpus/lessons/round-36.md`
(`git log -S 'S211' -- corpus/SOURCES.md` → `a3094c9`).

## Rows touched old → new

**None.** No existing row's `status`, `recheck` or `used-by` cell changed; the
only `SOURCES.md` diff from the round-35 tip is the one appended S211 line
(`git diff 7a068cb master -- corpus/SOURCES.md`).

## Which rows this round opens

The round opens **no new registry row** beyond S211. Neither claim cites an
existing source row: C1 is instrument work (`quality/counters/`), C2 is record
work (`LOG.md`, `SCORECARD.md`, `corpus/lessons/round-36.md`), and neither frozen
claim names a registry row. The one source opened this round, S211, is admitted by
the round's lesson (its `## Gate`), not by a claim.

## Frontier rows advanced

The frontier bullets in `corpus/README.md` §Frontier are unchanged: the round adds
no frontier bullet. The two instrument surfaces (the repaired counters
`quality/counters/c1-idle-lock.py`, `quality/counters/c2-ledger.py` and the
discrimination manifest) and the pointer gate (`quality/check-evidence-pointers.py`)
are **lane instruments, not domain frontier** — they are meta-process, not desktop
surface work, and they advance the lane's record-keeping, not any unresolved
surface. No domain frontier row is advanced this round.

## Assimilation

**Assimilation: none this round.** Registered before any round-36 data
(`.ufo/waves/round-36/registration.md`): round 35 adopted the `merge/mado/` core
theme (three entries, eight rows) and its counter is the instrument this round
repairs; §10 of the round-36 prompt's Assimilation contract allows a round to
declare `Assimilation: none` without penalty. The package is not re-adopted while
its evidence chain is under repair. The round's lesson confirms the same: no
knowledge entry is admitted this round, so no other row is written; the campaign
package's refused material from round 35 stays refused (`corpus/lessons/round-36.md`
§Gate decisions).
