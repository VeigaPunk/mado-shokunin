# R80ScribeLesson — round-80 `## Mistakes` draft (seat report)

Report trailer for the runner. Canonical copy: `.ufo/waves/round-80/w1/R80ScribeLesson/findings.md`
(identical bytes below this line apart from this pointer paragraph).

Seat: scribe, round mado 80, wave w1 (14 seats). Role: prose only — draft the round lesson's
`## Mistakes` section for the L1 to land. This seat edited no lane file, ran no mutating git or jj
command, and touched no frozen instrument.

## Produced

- `mistakes-r80.md` (this directory) — the adoptable `## Mistakes` section: house header plus five
  rows M80-1…M80-5, the sixth-mistake TODO/FIXME/XXX sweep, and a fenced block carrying every fix
  command verbatim with its observed exit code on the pre-fix and post-fix bytes.
- This file — the seat report, ending in a `STATUS:` line.
- `../R80ScribeLesson.md` — the runner's `Report:` trailer path (outside this directory; the seat
  bounds name this directory only, so the write is disclosed here as the one exception the
  assignment itself names). It carries the same content.

## Axes touched

- operability: the five fix commands are runnable, not prose; each has a red side and a green side
  observed on committed bytes (table below). The r80 wave can close on four of them directly.
- calibration: two of the provisional rows landed in `b65f3227` overstate their own evidence; the
  draft corrects the wording and keeps the limit named rather than smoothing it.
- coverage / depth / freshness / adjacency: unchanged by this seat (no claim, no source opened
  freshly — the sources here are already-committed fetches re-read at their pins).

## What was opened (read-only)

| item | bytes | result |
|---|---|---|
| `corpus/lessons/round-79.md` | rows M79-1…M79-8 at lines 15-22 | eight rows; M79-6 cites `S469.bin:92-101` |
| `corpus/lessons/round-79-verifier-spotcheck.md` | §1, §4, §6 | five routed defects D1–D5, matching M80-1…M80-5 |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-79/mado.md` | line 95 (Before→after) | after-cell `44/44` at `d6be05ef`, citing `measurement-final-r79.txt` |
| `.ufo/waves/round-79/receipts/measurement-final-r79.txt` | line 41 | `tool_selftest=50/50 … rev=999a4a3f` |
| `.ufo/waves/round-79/receipts/measurement-c1-r79-repair.txt` | line 38 | `tool_selftest=44/44 … rev=d6be05ef` |
| `.ufo/waves/round-45/fetch/wiki-Monitors.md` | `:179`, `:183` | syntax line and "This does stack on top of the calculated reserved area" |
| `corpus/SOURCES.md` | S467, S470–S475 | S475 present, `teaches` opens `supersedes S467 —` |
| `LOG.md` | 3928, 3955 | "Seven mined"; the append-only correction naming the eight |
| `.ufo/waves/round-79/fetch/` + `sha256-r79.txt` | 12 stems, 10 entries | `S468`/`S469` have neither a row nor a manifest line |
| `.ufo/waves/round-80/fetch/` + `sha256-r80.txt` | 5 stems, 5 entries | `sha256sum -c` 5/5 OK, no self-entry |
| `.ufo/waves/round-79/w1/` and `round-80/w1/` | seat dirs and reports | r79: 13 of 14 filed, `R79ExecC1Tool` has none; r80 at 08:46: 2 filed, 12 pending (the count falls as seats file; 9 pending at the 08:47 re-run) |
| `tools/mado-barfoot.py`, the two r80 counters | sha256 | match the pins `c3eb5fbe…`, `6268667c…`, `462287fb…` |

## Probe matrix (red side / green side, exit codes observed)

| row | probe | red bytes → rc | green bytes → rc |
|---|---|---|---|
| M80-1 | citation probe: the cell that cites `measurement-final-r79.txt` must carry that receipt's tally and `rev` prefix | filed r79 report → **1** (`cell=44/44@d6be05ef receipt=50/50@999a4a3f`) | copy with the after-cell reading `50/50` at `999a4a3f` → **0** (scratch fixture; the erratum lands with the r80 report) |
| M80-2 | exactly one row opening `supersedes S467 —`, three narrowed clauses, `:183` anchor, no "line syntax only" | `git show 6c302a53:corpus/SOURCES.md` → **1** (`supersede-rows=0`) | landed `corpus/SOURCES.md` → **0** (`narrowed`) |
| M80-3 | eight lesson rows and a later LOG correction naming them | `git show 6c302a53:LOG.md` → **1** (`rows=8 correction=no`) | `LOG.md` at `b65f3227` → **0** (`rows=8 correction=yes`) |
| M80-4 | every fetch stem of a wave is registered or manifested, and `S468`/`S469` never gain a row | r79 wave → **1** (`unlisted=['S468', 'S469']`) | r80 wave → **0** (`unlisted=[]`, 5/5) |
| M80-5 | every seat has a report, canonical `findings.md` first, with a `STATUS:` line | r79 wave, report-presence only → **1** (`missing R79ExecC1Tool`, one line); r80 mid-wave → **1** (12 pending) | not yet observable: the wave has not closed |

The fenced block in `mistakes-r80.md` is the executable copy of these five probes. I extracted it
from the draft and ran each chunk from the lane root: `rc` = 1, 0, 0, 0, 1 as tabulated, with the
r79 report-presence control printing exactly one line. The sixth sweep
`grep -n 'TODO\|FIXME\|XXX'` over `tools/mado-barfoot.py`, `quality/counters/c1-r80-multisurface.py`
and `quality/counters/c2-r80-runbook.py` printed nothing (`rc=1`).

## Findings against the landed round-80 artifacts (adapt, do not revert)

1. **The provisional M80-5 row overstates its carrier.** It says "every r80 seat prompt names
   `findings.md` and a final `STATUS:` line". Measured: 12 of 14 task bodies name `findings.md`,
   1 names `STATUS`; the requirement actually travels in the shared `context` block of
   `w1-spec.json` ("Your findings file is …/w1/<your-name>/findings.md" and "- End your
   findings.md with `STATUS: ok …, partial … blocked` …"). The draft names that carrier instead.
2. **The wave carries two report paths.** The runner's `Report:` trailer is `w1/<name>.md`; the seat
   bounds name `w1/<name>/findings.md`. At 08:46 `R80ScoutLive` had both and `R80ConnSiblings` had
   only the trailer, so a landing check over either path alone can miss a filed seat or accept one
   without `STATUS`. The draft makes `findings.md` canonical and the trailer a pointer, and this
   seat satisfies both paths itself.
3. **Two provisional fixes state the fixed state, not a red/green pair.** The landed M80-1 fix
   ("every cell copies its tally…") and M80-4 fix ("`S468` is still unregistered, manifest 5/5")
   describe the invariant but name no command that failed before it. The draft keeps both and adds
   the probes above, which are red on the pre-fix bytes by construction.
4. **State moved during the seat.** HEAD advanced `6c302a53` (freeze) → `b65f3227` (landing) while
   I read: the landing added `corpus/lessons/round-80.md` with the provisional rows, the S470–S475
   registry rows, the LOG corrections block and the knowledge entry. All red sides above therefore
   cite `git show 6c302a53:…` or the r79 wave, never "what used to be in the working tree".
5. **Recorded as a named limit, not a defect**: `R79ScoutHost` also has no `.md` inside its seat
   directory, but it did file `w1/R79ScoutHost.md`; the single genuine r79 landing gap is
   `R79ExecC1Tool` (13/14).

## Bounds

No commit, no push, no mutating git/jj. No write to the frozen instruments, control sets, `SKILL.md`,
`SCORECARD.md`, `LOG.md`, `corpus/`, the fleet repo or a sibling lane. No host probe, no package
transaction, no service restart. Scratch `/fast/scratch/hyaku/mado-r80/R80ScribeLesson/` was used for
the probe fixtures and the `git show` dumps and is removed before this seat ends; every evidence
path above is a committed or lane file, not scratch.

STATUS: ok — nothing missing; the only unobservable side is M80-5's green (the wave has not closed),
which is stated as pending rather than claimed.
