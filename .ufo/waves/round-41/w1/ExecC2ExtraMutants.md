# ExecC2ExtraMutants — round-41 w1: extra mutants of the C2 admitted fixture

Status: **DONE**. 45 new mutants of the admitted set `G` (none in the frozen 41), scored in fixture
repos built exactly as the frozen `score()` builds them. **29 survive** (`admitted=1/1`), 16 are
killed, clause a's setup guard holds. Survivor list with the clause that should kill each:
`.ufo/waves/round-41/w1/ExecC2ExtraMutants/survivors.md`.

## Files (all new, all inside the seat directory)

| path | sha256 | what |
|---|---|---|
| `.ufo/waves/round-41/w1/ExecC2ExtraMutants/extra-mutants.py` | `ec96f11f…a14d5` | harness: 45 mutants, importlib of the frozen runner, frozen `score()` recipe |
| `.ufo/waves/round-41/w1/ExecC2ExtraMutants/survivors.md` | `7bf1c86a…41991` | deliverable: 29 survivors + clause + mechanism + 16 killed + root causes |
| `.ufo/waves/round-41/w1/ExecC2ExtraMutants/evidence.py` | `54b2d563…f2992` | mechanism facts (head/ids, journal parses, symlink mode, `norm()`) |
| `.ufo/waves/round-41/w1/ExecC2ExtraMutants/evidence.txt` | `38b031ee…3f0d3` | that run's output |
| `.ufo/waves/round-41/w1/ExecC2ExtraMutants/check-quotes.py` | `eb2f1d95…96cd8` | verifies every quote in survivors.md at its `file:line` |
| `.ufo/waves/round-41/w1/ExecC2ExtraMutants/results.txt` | `c1a0076b…30557` | full scoring run, one line per mutant |
| `.ufo/waves/round-41/w1/ExecC2ExtraMutants/results.json` | `3c7ab54e…c9486` | machine-readable verdicts |

No tracked lane file was touched (`git status --porcelain` shows 0 non-`??` entries). No counter,
control, registration, fetch receipt or reference file was edited.

## Method

`extra-mutants.py` imports `.ufo/waves/round-41/ctl/run-c2-controls.py` with
`importlib.util.spec_from_file_location` (its `main()` is `__main__`-guarded and never runs) and
reuses `base_files()`, `admitted()` (= `G`), `row()`, `gate_line()`, `set_receipt()`,
`with_journal()`, `journal()`, `QUOTES`, `FILLER`, `ADMIT`, `REFUSE`. Scoring is the frozen
`score()` recipe verbatim: `D=$(mktemp -d)`, `git -C D init -q`, `rev-parse --show-toplevel`
verified equal to `D` before the first commit, throwaway identity passed with `-c
user.name=ctl -c user.email=ctl@ctl.invalid`, then
`python3 -I quality/counters/c2-r41-focus-entry.py --repo D --rev A --base B`; the fixture is
removed in a `finally`. Only delta: an optional `links` mapping that creates git symlinks after the
regular files are written and before `git add -A` — M08 (a symlink receipt) cannot be expressed by
the frozen writer. One mutant (`M22`) needs a base with a second held row (`G2`) so that 4 distinct
citations can contain only 2 new ids; `G2` itself scores `1/1`.

Baselines in the same run: `G` `admitted=1/1` (matches control P), `G2` `admitted=1/1`.

## Result

```
CTL_C2_EXTRA: mutants=45 survivors=29/45
SETUP-entry-present-at-base rc=2 PRED-C2-r41-v1 SETUP precondition_failed
  entry_present_at_base corpus/knowledge/hyprland-focus-grab-r41.md
```

Survivors by severity (details and the counter line that lets each through are in `survivors.md`):

- **HIGH (11)** — a defective entry passes: `M01` citation past line 20; `M02` lowercase cited id;
  `M08` receipt is a symlink (532-byte path string, mode `120000`, sha matches); `M09` new row with
  `recheck: TBD`; `M10` new row with no location at all; `M14` self-admit; `M15` admit of a
  nonexistent package path; `M20` fenced `verified-at`/`recheck` shadowing the real front-matter;
  `M22` 2 new ids where the docstring says at least 3; `M27` `source:` inside a fence; `M28`
  `source:` moved to line 22 (leaves the id set, so no row/gate is required).
- **MED (13)** — `M04` one line serving two ids; `M05` quote assembled across two `<p>` blocks;
  `M11` `amgsk.dev` in the anchor cell; `M12` quotes distinct only in whitespace; `M13` 20 filler
  chars as a REFUSE reason; `M16` journal with no `-- Boot` line; `M17` one session block replayed
  3× (identical timestamps); `M18` quote only after `html.unescape` of a plain-text receipt; `M19`
  `recheck: 2026-99-99`; `M21` held row loses its pre-existing used-by item; `M23`/`M24` fenced
  ADMIT / GATE lines still count; `M25` REFUSE the package the ADMIT admits.
- **LOW (3)** — `M03` two entry lines per id; `M06` conflicting GATE line outside `## Gate`; `M26`
  location `…/a.xml#frag` beside `…/a.xml`.
- **BENIGN (2)** — `M29` same id cited twice ("distinct" is by design); `M30` quote split by a
  newline (normalization of wrapped text is by design).

Killed (16, teeth confirmed): `M07` `./` receipt path, `K01` 10-cell row, `K02` quote case,
`K03` GATE extra field, `K04` 19-char reason, `K05` `verified-at` at line 21, `K06` two sources at
line 21, `K07` `[LOG] |` single space, `K08` focus-grab advert only in an earlier session, `K09`
4-space row indent, `K10` two README rows, `K11` two own-work rows, `K12` double-spaced census
line, `K13` ADMIT path with spaces, `K14` `..` receipt path, `K15` README row for another name.

## Retained evidence (exact)

- `results.txt` line per mutant, e.g.
  `M08-receipt-symlink expect=admit verdict=SURVIVOR rc=0 PRED-C2-r41-v1: admitted=1/1
  clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`.
- `evidence.txt` §A — clause b's raw head: `M20 … L4 'verified-at: 2026-10-25'` before
  `L13 'verified-at: 2026-10-23'`; `M28 … ids=['S050','S301','S302','S303'] tail citations:
  ['source: S304 - docs']`; `M02 … L7 'source: s304 - docs'`.
- `evidence.txt` §B — `M22 cited=['S050','S051','S301','S302'] new=['S301','S302']`.
- `evidence.txt` §C — `M16-no-boot counts(S,A,D,F)=(3, 72, 24, 1) bootlines=0`;
  `M17-replayed counts=(3, 72, 24, 1) … first_ts=…13:10:00 last_ts=…13:10:00`.
- `evidence.txt` §D — `ls-tree: 120000 blob fd8e885c… .ufo/waves/round-41/fetch/S301.link.txt`,
  `show bytes=532 sha256=562be874…`, `gate sha256 in lesson: 562be874…`.
- `evidence.txt` §E — `norm(M05 html) contains quote: True (raw contains: False)`, likewise for the
  entity-encoded and newline-split receipts; §F `raw distinct=True norm equal=True`; §G held-row
  used-by before/after; §H `M10 loc_token='surfaces'`, `M11 anchor='https://amgsk.dev/…'`.
- `check-quotes.py` → `quote check: 25/25` (every quote <= 25 words, each found verbatim at its
  cited `quality/counters/c2-r41-focus-entry.py:<line>`).
- Path-traversal probe (before the run, in `/tmp`): `git show REV:f/./real.txt` and
  `REV:f/../f/real.txt` both fail (`fatal: path … exists on disk, but not in …`) — M07/K14 are killed
  by git, not by the counter.
- The real host receipt `.ufo/waves/round-41/fetch/xdph-journal.txt`
  (sha256 `bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7`) uses `[LOG]  | ` with
  two spaces and carries 1 `-- Boot` line, 2 PIDs, 78 adverts — so a ">= 1 BOOT line" or
  timestamp-monotonicity rule would not break the actual receipt.

## Root causes (what a v2 predicate would have to add)

1. `head = text.splitlines()[:20]` (line 188) is raw, contradicting the counter's own preamble
   (lines 6-7) and ignoring line 21+ — M20, M27, M28, M01; case-sensitive ids — M02.
2. Receipts are read as blobs with no mode check (lines 243-244) — M08.
3. Clause c stops at status/used-by/opened for new rows (lines 221, 225) and excludes used-by from
   the held-row comparison (line 218) — M09, M21, M22.
4. `norm()` strips tags and decodes entities for every receipt (line 119) — M05, M18.
5. Clause i is two regexes (lines 89-90, 306-307): no package existence, no self-admit, no
   admit/refuse distinctness, filler reason — M13, M14, M15, M25.
6. Clause h has no provenance floor (lines 160, 167, 283): BOOT optional, no monotonicity — M16, M17.
7. The lesson is never unfenced (lines 228, 306-307) — M23, M24; raw-string comparisons at
   lines 248/268 — M12, M26.
8. Clause g is `any()` (line 298) and `BAD_LOC` reads one cell (line 312) — M03, M04, M11.

## Risks / limits

- These are blind spots of the **predicate**, not evidence that the real C2 entry is defective. A
  survivor means the counter cannot distinguish the mutant from a sound entry; the L1 decides
  whether that is a v2 re-registration (registration.md §"Residuals" already anticipates this) or a
  disclosed residual.
- Fixtures are synthetic, and `G` is the frozen control's admitted set, not the real lane data.
  Scoring is byte-exact but the mutants do not re-open the real journal/sources.
- `M22` uses a modified base (`G2`, a second held row). It is a mutant of the id mix, not of the
  base; `G2` alone scores `1/1`.
- `M08` needs the symlink writer delta described above; every other mutant runs on the frozen writer.
- `M13` (20 filler chars) and `M29`/`M30` are within the letter of the contract; they are listed as
  contract-level weaknesses, not counter bugs.

## Process notes

- No tool installs, no package transactions (pacman paused; nothing was needed). No `journalctl`
  invocation, no compositor/Wayland contact: the journal was read from the L1's fetched receipt.
  Git ran only in `/tmp` fixture repos plus read-only `status`/`log` in the lane.
- Two two-token fixes inside my own harness scripts were applied with a `python3` heredoc before I
  switched back to the `edit` tool; no lane file was involved. The final file contents are the ones
  hashed above.
- No blockers.
