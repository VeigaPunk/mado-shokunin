# R100MScribeEntry -- round 100 w1 scribe (C1 knowledge entry + SOURCES row work)

Seat: `R100MScribeEntry` (scribe). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch
`master`, base revision `43309e6af9a3b57f1bc839a826bef1f8eb7495e4`. No commit, no push, no mutating
git/jj command, no subagent dispatch, no tool install. Scratch
`/fast/scratch/hyaku/mado-r100/R100MScribeEntry` deleted before this report was filed.

## 1. What this seat produced

| artifact | path | lines | state |
|---|---|---|---|
| the C1 knowledge-entry draft | `.ufo/waves/round-100/build/gio-launch-path-default-r100.md` | 396 | complete draft; ASCII-only (`LC_ALL=C grep -cP '[^\x00-\x7F]'` = 0) |
| the SOURCES row decision + the lesson's `## Gate` block | `.ufo/waves/round-100/build/sources-append-r100.md` | 214 | complete draft; ASCII-only |
| this seat's report | `.ufo/waves/round-100/w1/R100MScribeEntry.md` | - | this file |

Nothing under `corpus/`, `tools/`, `quality/`, `plans/` was written by this seat. The git index and
the jj state were not touched; the lane's `git status --porcelain` shows only this seat's two
untracked `build/` drafts plus the artifacts other seats and the L1 wrote.

## 2. Behaviour

### 2.1 The branch, as re-measured here (not inherited)

The L1's ground was re-measured by this seat before anything was written:

| fact | how this seat measured it | observed |
|---|---|---|
| `glib2` | `pacman -Q glib2` | `2.90.1-1` |
| the oracle | `sha256sum /usr/bin/gio` | `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` (equals the L1 pin and the round-99 case-file pin) |
| `gutils.c`, committed bytes | `sha256sum .ufo/waves/round-99/fetch/gutils.c` | `65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771`, 100534 B, 3245 L |
| `gutils.c`, live re-fetch | `curl -sSL -o live-gutils.c -w 'HTTP %{http_code} %{url_effective}' https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c` | `200 https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c`, sha256 identical to the committed bytes - the digest is confirmed twice |
| the round-99 oracle | `sha256sum .ufo/waves/round-99/controls/launchenv-probe-r99.py` | `cbfff7a4b64e63f3e6861d29d1c5639de2c25abe2f6875088918abb45d129199` (equals the L1 pin) |

The three located quotes the seat item named, each produced by `grep -n` on the fetched bytes
(round-99 M99-2's rule: a locator comes from the line the quote sits on, never from a function's
range):

| what | quote | line | words |
|---|---|---|---|
| the unset-PATH default | `path = "/bin:/usr/bin:.";` | `gutils.c:388` | 4 |
| the unset guard | `if (path == NULL)` | `gutils.c:376` | 4 |
| the empty-entry rule | `Two adjacent colons, or a colon at the beginning or the end of 'PATH' means to search the current directory.` | `gutils.c:472-473` | 20 |
| the absolute-or-slash short-circuit | `if (g_path_is_absolute (program) \|\| strchr (original_program, G_DIR_SEPARATOR) != NULL` | `gutils.c:332-333` | 9 |

**Finding (locator, for the L1):** the declaration's C1 cites the default literal as
"`gutils.c:370-382`" and the round's assignment repeats that range. **The literal is not inside
it**: `:371` reads the PATH source, `:376` is the guard, and the assignment is at **`:388`** (the
block runs `:376-389`). S533's own anchor cell is correct (`:370-389` covers the literal). This is
the round-99 M99-2 class (a locator inferred from the block) and it is a **locator** defect, not a
widening of the frozen predicate - the sentence's claim is confirmed by the bytes and by the L1's
own ground measurement. The L1's already-landed lesson `## Gate` row quotes `:388` correctly, so
the correction is applied there; the declaration's own parenthetical still needs an in-place
correction or an erratum.

### 2.2 The three separations, measured (21 rows, the entry's section 7)

Measured through the committed round-99 oracle (an **instrument**: it spawns the installed `gio`),
two runs per case, all labels agreeing, `cwd = the case root` unless the row says otherwise, child
environment `LC_ALL=C`, `HOME=<root>/h`, `PROBE_OUT=<root>/out` plus the case's own PATH entries
only - **never a host PATH**, so no host application and no terminal was ever started. The
candidate (`tools/mado-launchenv.py`) was never used to produce a label.

| separation | verdict this seat measured |
|---|---|
| (1) unset != empty | **holds, two ways.** The `/usr/bin`-only arm: `TryExec=true` (the host's `/usr/bin/true`, and `/bin` symlinks to `usr/bin` here) resolves under an absent PATH (row P13) and is refused under `PATH=""` (P14). The success-region arm is **lexical only**: `{root}/./probe` (P1) against `{root}/probe` (P2) - same file, same launch count, same cwd, same env value. |
| (2) unset != the ambient search | **holds.** A program only in `{root}/bin` is refused under an absent PATH (P3) and found with `PATH={root}/bin` (P4, `argv[0]={root}/bin/probe`). |
| (3) the default's trailing `.` is real | **holds only in its lexical form; the declaration's found/not-found half does not reproduce.** With an absolute `Path=` the two PATH states agree in every fixture measured (P5/P6 both refuse; P7/P8 both launch with the identical `{root}/work/probe`). With a *relative* `Path=work` both states launch and the argv0 differs: `{root}/work/./probe` (P15) against `{root}/work/probe` (P16). With no `Path=` at all: `{root}/./probe` (P1) against `{root}/probe` (P2). |

This seat's independent measurement agrees with the wave's reviewer (`w1/R100MReviewC1.md` section 1a) and
critic (`w1/R100MCriticClaims.md` section 1.2-1.3), which reached the same conclusion from the other
side. **The declaration is frozen and this seat does not widen it**; the entry states the measured
behaviour and the sources draft names the narrowing as an L1 decision.

### 2.3 The load-time-gate consequence (cwd matters)

The load gate runs at **load** time, inside the `gio launch` process, so the resolving process's cwd
decides the `.` entry and the empty walk's current directory. Measured: the same desktop file, the
same program at the case root, the same absent PATH - launches with `argv[0]={root}/./probe` from
the case root (P18) and refuses with `Unable to load application information for '<desktop>'` from
another directory (P17). The `PATH=""` variant refuses from another cwd too (P20). The `/usr/bin`
arm is the one arm that is cwd-independent (P21). The refusal is the **load** refusal
(`gio-tool-launch.c:109`, exit 1), not the launch refusal (`:121`).

### 2.4 The tool and the one-line recheck

The model answers the branch read-only: with `--path` omitted and no `PATH` in its own environment
the model treats the state as **absent** (the `/bin:/usr/bin:.` default, `tools/mado-launchenv.py:121`
`DEFAULT_SEARCH_PATH`, `:177` `find_program`, `:207` the default branch), and `--path ""` as one
empty entry. Measured by this seat on the base-revision tool bytes (sha256 `a63c20c8...eb16`, the
committed `tools/mado-launchenv.py`): absent -> `ARGV[1][0]=<case>/./probe`; `--path ""` ->
`<case>/probe`; `--selftest` -> `MADO_LAUNCHENV_SELFTEST: checks=90 failed=0`. The round-100
candidate copy under `build/` answers the same two strings when `tools/mado-execargv.py` is beside
it, and answers `SETUP_ERROR execargv-missing` when it is not (the sibling is loaded by path).

The one-line recheck in the entry's section 6 re-derives the two answers from the installed `gio`
through the committed oracle: **wall time 6.84 s** for both cases together on this host (load
average 116-155 on 32 cores at the time of the run).

## 3. The SOURCES row decision (the L1's to land)

**Decision: no new row.** S533 already covers this scope - its scope cell names "the PATH source and
its default, the empty PATH entry" and its anchor names `:331-357`, `:370-389` and `:462-500`, which
is every `gutils.c` line the entry cites. CORPUS rule 4 says expansion is knowledge, not rows; the
declaration names S533 as the sourced claim "opened and quoted again this round"; and the round's
own precedent (96, 97) opens a row only for a new file or a genuinely new question of the same
file, giving re-opened rows a `used-by` append only.

The registry work is therefore **three `used-by` appends** (S528, S532, S533), each with its old and
new cell text in `.ufo/waves/round-100/build/sources-append-r100.md` section 2, each change logged
old -> new as CORPUS rule 2 requires. **Measured** over a scratch mirror of the lane's `corpus/`:
with the entry in place and the three cells set, `check-sources-readback.py` reports
`rows=469 entries=121 findings=0` (exit 0) and `sources-census.sh validate` reports exit 0 with no
`E` finding. Without the comma between the two paths the same gate reports `R3` (the whole cell is
read as one path) and `R4` - the cell text matters.

A fallback row is drafted in the same file (section 3, id `S535`, the next free id; `status=mined`;
`recheck` `2027-05-07` = `2026-11-08 + 180d`, an ISO date the census accepts; `used-by` naming only
the entry this round drafts) for the case where the L1 rules that the narrower branch deserves its
own scope row. **Measured**: with that row in a scratch registry copy, the census reports exit 0 and
exactly one new finding class, the `W04` duplicate-URL warning; a row whose `scope` cell were
*identical* to S533's would raise `E04` and make the census exit 1.

**Landing order (census E11, measured):** a `mined` row's `used-by` path must exist on disk, and the
entry file does not exist at the base revision - the entry lands **before or with** the registry
commit.

## 4. The lesson's `## Gate` block

Drafted in `.ufo/waves/round-100/build/sources-append-r100.md` section 4, in the round-99 lesson's
shape (`id | row | url | access | located quote (<=25 words) | decision`):

- **admit:** S533 re-opened, accessed 2026-11-08, HTTP 200, sha256 `65086c29...3771` (identical to
  the row's pin), quote `path = "/bin:/usr/bin:.";` at `:388` - plus two further located quotes the
  round's own claim needs (the empty-entry rule at `:472-473`, 20 words; the absolute-or-slash
  short-circuit at `:332-333`, 9 words).
- **reject:** the staged merge package's launch/exec-adjacent rows (`S205` and the seven other
  hits), with the reason (the sweep returns 9 hits, **0** for `/bin:/usr/bin`, **0** for `PATH
  default`, **0** for `per-leg`; every hit is round-6/7 session-lifecycle material) and the flip
  condition (a staged row that opens `gutils.c`'s default search path, or the harm panel's per-leg
  timing, becomes admissible).

**The L1 has already landed this block**: `corpus/lessons/round-100.md` (mtime 02:32:09) carries
the same admit row (S533, the `:388` quote) and the same reject row (the staged `S205` with its flip
condition), citing the same sweep
(`.ufo/waves/round-100/assimilation/connector-sweep-r100.txt`). This seat's draft is therefore a
second copy of a block that already exists; the L1 does not need to paste it.

## 5. Gates and instruments this seat ran

| check | command | observed |
|---|---|---|
| the base registry validates | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | exit 0; warnings only (W01/W04); no `E` finding |
| the base registry reads back clean | `python3 -I quality/check-sources-readback.py --repo <lane>` | `rows=469 entries=120 findings=0`, exit 0 |
| the L1's landed registry reads back clean | the same command against the lane | `rows=469 entries=121 findings=0`, exit 0; census exit 0, no `E` finding |
| the drafted row shape is census-legal | a scratch registry copy with the section 3 row, validated over a scratch mirror of the lane's `corpus/` | exit 0; one new finding class only, `W04 S535 duplicate url ... across scopes`; zero `E01`-`E11` |
| the primary path (no new row, three appends) is clean | the same mirror without the `S535` row, with the three `used-by` cells set and the entry in place | read-back `rows=469 entries=121 findings=0`, exit 0; census exit 0, zero `E` findings |
| the entry draft is ASCII-only | `LC_ALL=C grep -cP '[^\x00-\x7F]'` on both drafts | `0` on each |

The lane's own counters were **not** run by this seat (they are the executor seats' and the L1's
instruments, and the round's C2 leg is a 28-leg panel whose wall time is long under this host's
load).

## 6. Touched surfaces

| path | what | who lands it |
|---|---|---|
| `.ufo/waves/round-100/build/gio-launch-path-default-r100.md` | the entry draft (this seat's) | the L1 |
| `.ufo/waves/round-100/build/sources-append-r100.md` | the row decision, the `used-by` old->new table, the fallback row, the `## Gate` draft (this seat's) | the L1 |
| `.ufo/waves/round-100/w1/R100MScribeEntry.md` | this report (this seat's) | - |

Nothing else was written. No commit, no push, no mutating git or jj command, no host service, no
pacman transaction, no tool install (so nothing to record from `/home/vgpnk/.omp/agent/RULES.md`'s
tooling log).

## 7. Out of scope for this seat

- The C1 **case file**, the counter and the mutant set (the executor and mutation seats' surfaces).
- The C2 harm-watch panel, the timing receipt and the per-leg `elapsed_ms` (the other executor's).
- The claim's wording, the predicate and any narrowing of them (the L1's, under
  `plans/round-100.md`'s pre-file amendment process).
- `corpus/SOURCES.md`, `corpus/lessons/round-100.md` and `corpus/knowledge/` - the L1's to land.

## 8. Findings the L1 must rule on

**F100-1 -- the declaration's default-literal locator is off by the block's tail.** C1 cites
`gutils.c:370-382` for the literal `/bin:/usr/bin:.`; the assignment is at **`:388`** (`:371` is
the PATH source, `:376` the guard). S533's anchor (`:370-389`) is right; the declaration's
parenthetical is not. *Fix:* correct the declaration's locator in place or in an append-only
erratum, and keep the sentence's claim (the bytes and the L1's own measurement confirm it). This
is the round-99 M99-2 class, caught before the fact rather than by an outside spot-check. **Not a
widening** - no conjunct moves.

**F100-2 -- C1's separation (3) is not reproducible as written, and its true content is lexical.**
The declaration's sentence says a program present only in the launch working directory "is not found
by the same fixture under `PATH=""` when the working directory differs from the process cwd". This
seat measured six shapes (P1-P8, P15-P16) and found no geometry where that holds: with an absolute
`Path=` the two states agree in every fixture, and with a relative `Path=` both states launch and
the argv0 differs by the `./` alone. The branch's reality is that the trailing `.`'s contribution is
the extra `./` in the returned path, and the class can only witness that lexically. The wave's
reviewer and critic reached the same conclusion independently. *This seat does not widen or narrow
the frozen predicate*; the entry states the measured behaviour and names the narrowing as the L1's
decision under the round-98/99 pre-file amendment process. **The risk is a frozen case set whose
expectation the declaration's prose cannot be derived from.**

**F100-3 -- the success-region separation is lexical, so the frozen expectations must carry the argv
vector verbatim.** `{root}/./probe` and `{root}/probe` name the same file. A counter that normalises
(`normpath`/`realpath`) the argv, or an oracle that canonicalises the `./` away, erases the only
difference the success region carries. The L1's landed case file does carry it verbatim
(`pd-dot-root` expects `{root}/./probe`, `pd-empty-root` expects `{root}/probe`), and this seat
re-measured both against the installed `gio` - they hold. *Note for the L1:* the oracle's
canonicalisation replaces the probe file's own path first, so a case built on the oracle's default
`probe.sh` prints `{probe}` where the unset case prints `{root}/./probe.sh` - the difference between
the two printed forms is the branch, not a naming accident.

**F100-4 -- the entry's `used-by` set must match the entry's `source:` block, or the read-back gate
fails.** The L1's landed entry names **S533 alone** and the landed registry appends S533 - complete
and green (`findings=0`). This seat's entry draft names **S528, S532 and S533**, so landing it
needs the two further `used-by` appends (drafted with old->new cell text in the sources draft
section 2); without them the read-back gate reports two `R4` findings and exits 1. Measured both
ways.

**F100-5 -- `Path=` is the lookup's `working_dir`, not the cwd, and the distinction is measurable.**
A program present only in the **process** cwd is not found under either PATH state once `Path=` is
set (P5, P6), because the walk's `.` candidate is joined to `Path=` first (`gutils.c:480-484`); a
*relative* `Path=` is itself resolved against the process cwd (P15 launches, P19 refuses). Any entry
sentence that says "the `.` entry means the launch working directory" without this caveat is wrong
in the direction that matters.

## 9. Recheck

- **Source:** `curl -sSL -o live-gutils.c -w '%{http_code} %{url_effective}'
  https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c` -> HTTP 200; sha256 must equal
  `65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771`. Then
  `grep -n 'path = "/bin:/usr/bin:."' gutils.c` -> `388:`,
  `grep -n 'if (p == path)' gutils.c` -> `471:`,
  `grep -n 'if (g_path_is_absolute (program)' gutils.c` -> `332:`.
- **Behaviour:** the two-line oracle recheck in the entry's section 6 (wall time 6.84 s for both
  cases on this host); the model side is
  `python3 -I tools/mado-launchenv.py <case>.desktop` (absent) against
  `python3 -I tools/mado-launchenv.py <case>.desktop --path ""` (empty), and
  `python3 -I tools/mado-launchenv.py --selftest` -> `MADO_LAUNCHENV_SELFTEST: checks=90 failed=0`
  on the base bytes.
- **Registry:** `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
  and `python3 -I quality/check-sources-readback.py --repo <lane>`; both exit 0 at the landed state.
