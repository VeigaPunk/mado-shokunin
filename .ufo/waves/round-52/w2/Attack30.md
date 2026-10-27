# Attack30 — C2 counter no-work control at base

Seat: `Attack30` (W2 attack #30, revenger). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Frozen base: `85d57a818c3707397e21c840b6498b105ba798aa` (lane `HEAD`; verified). Date: 2026-10-27.
Axes named: **coverage** (C2's target axis) and **operability** (the counter/control's own axis);
this seat attacks only the control's mechanics, not entailment, novelty or source truth.

Read before judging: `.ufo/waves/round-52/claims-frozen.md`, `registration.md`,
`controls/c2-do-nothing.md`, `w1/C2CounterDraft.md` + `w1/C2CounterDraft/receipts/*`,
`w1/C2CoverageCritic.md`, `w1/C2Novelty.md`, `w1/Falsify47.md`, and the two counter artifacts
named below. This is an attack wave, not a vote: verdicts below are per sub-clause, not an
admission decision.

## Attacked clause

- `claims-frozen.md:11` (C2, last third): "A new committed counter checks proposition count,
  row/pin/quote bindings and complete mapping; … **A no-work control at base must miss because
  target entry is absent.**"
- `registration.md:9`: "**Base entry absent → TARGET_MISSED.**"
- `registration.md:15`: "C2 no-work control is the frozen base revision, with the target new
  entry absent. … the new counter must name a separate target slug and **prove absent at base**."
- `controls/c2-do-nothing.md:1`: "at the frozen base revision, the claimed new corpus entry is
  absent, so the target predicate must report TARGET_MISSED. No source payloads are admitted and
  no source registry rows are appended by this control."

Attacked claim, in one sentence: *the counter's base-revision MISS is a sound, specific, and
discriminating no-work control for the claimed entry's absence and for the counter's own reach.*

## Instruments tested

| instrument | path | sha256 | size | committed? |
|---|---|---|---|---|
| W1 draft counter (the one whose receipts `w1/C2CounterDraft.md` presents) | `.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py` | `55452a3d6eab7cca2b20095f8678fbe936c8c65f241a561611a675defd8379fb` | 965 lines | no (seat draft) |
| current candidate at the claimed path | `quality/counters/c2-r52-proposition-entry.py` | `5c7fb820e43c7f6782b6ebfc90d018c25d74976d9e8ab2a90df5e4c82fb50c0a` | 47 lines | **no** (`git cat-file -e BASE:…` fails; `git status --short` shows `??`) |

These are **not byte-identical**. The W1 base receipt (`w1/C2CounterDraft/receipts/r-base.txt`)
was produced by the 965-line draft; the file now sitting at the integration path is a 47-line
rewrite (mtime 11:11 local, before the W2 registry at 11:16). Both were run for every case that
can change the verdict, so the report does not depend on which one the L1 blesses.

Claimed entry: the working tree holds `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`
(README row and S370–S373 in the modified `corpus/SOURCES.md`), while the 965-line draft's
`ENTRY_DEFAULT` (`:102`) and the 47-line counter's `--entry` default (`quality/counters/…:19`)
still name the **different** slug `corpus/knowledge/hyprland-synthetic-**key**-dispatch-r52.md`.
Both slugs are absent at base (below), but the default mismatch is itself a control defect (A5).

## Reproduction protocol

All commands are in `.ufo/waves/round-52/w2/Attack30/repro.sh`; its full transcript is
`.ufo/waves/round-52/w2/Attack30/receipts.txt`. Work happened in a scratch clone of the lane
(`git clone --no-hardlinks`), with `git rev-parse --show-toplevel` asserted as
`/fast/scratch/hyaku/mado-r52/Attack30/clone` before every mutation. The lane's own working tree
was read only (P3); no tracked lane file was written and no git/jj operation ran in the lane.

```
bash /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w2/Attack30/repro.sh
```

### P0 — base absence, independently of either counter

```
git cat-file -e 85d57a81…:corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md   # ABSENT
git cat-file -e 85d57a81…:corpus/knowledge/hyprland-synthetic-dispatch-r52.md       # ABSENT
git show 85d57a81…:corpus/SOURCES.md | grep -c '^| S37[0-3]'                        # 0
git show 85d57a81…:corpus/README.md  | grep -c 'hyprland-synthetic'                # 0
```

### P1 — W1 draft counter at base (both slugs)

`--repo clone --rev 85d57a81… [--entry corpus/knowledge/hyprland-synthetic{,-key}-dispatch-r52.md] --work <scratch>`

Both: `a ok=0 entry=absent`, `b..e skipped=entry-absent`, `clauses_met=0 admitted=0/1
verdict=TARGET_MISSED`, **exit 1**. The key-slug output is byte-identical to
`w1/C2CounterDraft/receipts/r-base.txt` except for the `--work` path.

### P2 — current candidate at base (both slugs)

Both: `C2_R52: entry=absent verdict=TARGET_MISSED rev=85d57a81…`, **exit 1**
(`quality/counters/…:23-25`).

### P3 — base run while the claimed entry exists untracked in the lane worktree

`--repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 85d57a81… --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md`

`entry=absent verdict=TARGET_MISSED`, exit 1. The counter reads `git show <rev>:<path>`, not the
filesystem, so the untracked integration work in the lane cannot leak into the base control.

### P4 — work-present revision (staged in the scratch clone, not the lane)

Copied the lane's working-tree `corpus/README.md`, `corpus/SOURCES.md` and the claimed entry into
the clone, committed as `597a9129bfeb8a95ef6282ac8157c1ac58ebb9c0`, then copied the lane's `.ufo/waves/round-52/fetch/` and
committed as `fd44ad4a4f57ed1f2cdc3444dad2a5538663b5d3`; `git cat-file -e
fd44ad4a4f57ed1f2cdc3444dad2a5538663b5d3:corpus/knowledge/hyprland-synthetic-dispatch-r52.md` = present.

| invocation | observed |
|---|---|
| candidate, `--entry <real slug>` | `props=0 rows=0 indexed=1 failures=1 verdict=TARGET_MISSED` (`miss=props`), exit 1 |
| candidate, default slug | `entry=absent verdict=TARGET_MISSED`, exit 1 |
| W1 draft, `--entry <real slug> --fetch-root .ufo/waves/round-52` | `a ok=1`; `b ok=1 propositions=18 ids=18`; `c ok=0 rows_bound=0/18 miss=P01..:anchor_no_fetch_root`; `d ok=0 quotes_bound=17/18 miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)`; `e ok=0 miss=P01..P04:id_not_referenced`; `clauses_met=2 admitted=0/1 verdict=TARGET_MISSED`, exit 1 |

### P5 — absence-signal specificity (present files, path variants)

At `fd44ad4a4f57ed1f2cdc3444dad2a5538663b5d3`, where the entry is present:

```
--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md/         -> entry=absent, exit 1
--entry :corpus/knowledge/hyprland-dispatcher-dispatch-r51.md        -> entry=absent, exit 1
--entry corpus/knowledge/../knowledge/hyprland-dispatcher-dispatch-r51.md -> entry=absent, exit 1
```

At base with a present, canonical path (`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`):
`props=0 rows=0 indexed=1 failures=1 verdict=TARGET_MISSED`, exit 1. The W1 draft shows the same
catch-all on a present file (`corpus/knowledge/hyprland-bind-key-match-r50.md/` → `a ok=0
entry=absent`), because its `show()` (`:156`) also maps every git failure to `None`.

### P6 — environment hermeticity

- candidate: `env GIT_DIR=/nonexistent` at base → `setup=error … not a git repository`, **exit 2**
  (the outer `except` at `quality/counters/…:46`).
- W1 draft: `env GIT_DIR=/nonexistent` at base → still the normal `0/5 TARGET_MISSED`, exit 1,
  because it freezes `ENV` with `GIT_*` stripped (`:120`).

### P7 — `--work` side effect

The candidate requires `--work` (`:19`) and refuses roots under `/tmp`/`/var/tmp`/`/dev/shm`
(`:21`), but never writes to it: `w-int-key`, `w-int-real`, `w-work-int-real`, `w-gitdir` are all
absent after the runs. No probe JSON exists for the base control on this counter. The W1 draft
writes `c2-r52-probe.json`.

## Verdicts

| # | attacked sub-clause | exact evidence | observed | verdict |
|---|---|---|---|---|
| A1 | "A no-work control at base must miss" (literal) | P1, P2; `git cat-file` P0 | `TARGET_MISSED`, exit 1, both counters, both slugs; base holds no S370–S373 row and no index row | **REPRODUCED** |
| A2 | "base revision … target entry is absent" is rev-based | P3 | base run still misses with the claimed entry untracked in the lane worktree | **REPRODUCED** (no worktree leakage) |
| A3 | "… **because** target entry is absent" — absence as the counter's own proof | P5 | the same `entry=absent` branch fires for files that **are present** under a trailing slash, leading `:`, or `..` spelling; both counters | **NOT REPRODUCED as a proof** — the signal is non-specific; absence was proven only by `git cat-file` (P0), outside the counter |
| A4 | the control discriminates no-work from work | P4 vs P1/P2 | at a revision that **contains** the claimed entry (and its README/SOURCES rows), candidate = `TARGET_MISSED`/exit 1 (`props=0`), draft = `TARGET_MISSED`/exit 1 (2/5). Same verdict and exit code as base | **NOT REPRODUCED as a discriminator** — a base MISS is achievable while the counter cannot accept the work |
| A5 | the counter names the claimed target slug | P4; `w1/…:102`; `quality/…:19` | default is `…synthetic-key-dispatch-r52.md`; landed entry is `…synthetic-dispatch-r52.md`; default run at the work rev = `entry=absent` | **NOT REPRODUCED** — the base control's default and the target's default are different files; `--entry` must be supplied for either to refer to the claim |
| A6 | the control proves "no work" (no rows opened) at base | P1/P2 (`b..e skipped`); `quality/…:19` (`--base` parsed, never referenced) | the entry-absent branch skips **all** row/pin/quote/mapping checks; the 47-line counter never compares `corpus/SOURCES.md` at base and has no base-already-holds guard (draft has one at `:951-953`) | **NOT REPRODUCED** — the base control tests file absence only; the "no source registry rows are appended" property is established by P0, not by the counter |
| A7 | a reproducible, auditable control receipt | P7 | candidate writes no `--work` artifact and prints one line; the W1 draft prints seven lines and a probe | **NOT REPRODUCED** for the candidate; only stdout is reproducible |
| A8 | the control is hermetic | P6 | candidate: a `GIT_DIR` override changes the run (setup error exit 2); draft: unaffected | **NOT REPRODUCED** for the candidate |
| A9 | "a new **committed** counter" | `git cat-file -e BASE:quality/counters/c2-r52-proposition-entry.py` fails; `git status --short` = `??`; P1/P2 sha | the base control is runnable only by supplying an **untracked** file; the W1-evidenced draft (965 lines) is not the file at the claimed path (47 lines) | **NOT REPRODUCED** at the tested revision; the W1 receipt certifies different bytes from the candidate |
| A10 | "must name a separate target slug" is enforced | P5 canonical base r51 entry; candidate has no r51 refusal | candidate scored `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` (`indexed=1`, `props=0`, MISS) instead of refusing it; only the draft refuses the r51 slug (`:947-948`) | **NOT REPRODUCED** for the candidate — the separation is caller discipline, not a check |
| A11 | base can yield MET for the claimed target | P1/P2; base corpus scan `^\| *P[0-9]+ *\| *S[0-9]+ *\|` = 0 hits | no base file supplies the candidate's four-row shape; both slugs absent; every base run misses | **REPRODUCED** (the claimed-slug control cannot flip green at base) |

Bottom line for the L1: the **literal control is reproduced** (A1, A2, A11) — at `85d57a81…`,
both counters report `TARGET_MISSED`/exit 1, both claimed-slug spellings are absent from the git
object store, and the lane's untracked integration work does not leak into the base run. The
**control is not probative** (A3–A10): its only base-specific observable is a catch-all
"show failed" branch, it is satisfied by the same verdict at a revision containing the claimed
work, it names the wrong default slug, and the candidate counter writes no probe and is not
committed. A W2 reading that treats the base MISS as evidence the target predicate is reachable
or that absence was proven *by the counter* is not supported by the artifacts.

## Collateral errors observed (other seats' claims; recorded, not my verdict)

These matter to C2 and to the L1's integration, but they are outside "no-work control at base".
They are reported because they surfaced in the same runs and are reproducible from
`receipts.txt`.

1. **Landed S370–S373 rows do not satisfy W1 draft clause (c).** Their `anchor` cells are
   `DispatcherTranslator.cpp:531-627 @ efb50993…; r52 fetch SHA256 …` (and the equivalents for
   S371–S373) — they do not contain the round fetch root `.ufo/waves/round-52` that
   `C2CounterDraft` clause (c) requires, and they name `DispatcherTranslator.cpp` rather than the
   pin basename `Hyprland-legacy-DispatcherTranslator.cpp`. Result at `fd44ad4a4f57ed1f2cdc3444dad2a5538663b5d3`:
   `rows_bound=0/18`, `anchor_no_fetch_root` on all 18.
2. **Landed P16 quote is a spliced span, not a contiguous one.** P16 cites
   `Hyprland-ConfigActions.cpp:1554-1558,1576` and quotes
   `sendKeyboardMods(...); sendKeyboardKey(...)` as one string, but source lines 1555–1557 sit
   between those two calls (`fetch/Hyprland-ConfigActions.cpp:1554-1558`); the draft's
   whitespace-collapsed containment correctly reports `P16:quote_not_at_pin(…:1554)`. The
   candidate counter does not inspect source bytes at all, only `len(quote.split())>25`.
3. **Landed P01–P04 are referenced only by their own map rows**; the draft reports
   `P01..P04:id_not_referenced` (padding under its clause (e)).
4. **The r51 base receipt context is confirmed.** `receipts/c2-base.txt` shows the old r51 counter
   already printing `admitted=1/1 verdict=TARGET_MET` at `85d57a81…` for the r51 entry — the
   registration's reason for demanding a separate slug and base absence. My P5 canonical-base run
   shows the *candidate* counter does not enforce that separation.
5. **W1 draft vs candidate divergence.** `w1/Falsify40.md` cites draft sha `298b8c07…`, the W1
   report and the file now on disk are `55452a3d…`; neither is the candidate `5c7fb820…`. Any L1
   copy step should re-run the base/green/mutant receipts against the bytes actually committed,
   not inherit the W1 receipt.

## Limitations

- I judge the control mechanics only. I did not judge source truth, entailment, novelty, wording
  reuse or whether the landed propositions are materially true; those are the outside non-author
  seats' work and are explicitly outside this counter and this attack.
- P4 stages the lane's current working-tree entry/README/SOURCES into a **scratch** commit
  (`fd44ad4a4f57ed1f2cdc3444dad2a5538663b5d3`) to create a "work present" revision. That commit is not a lane artifact and is not
  the claim's landing revision; it is a minimal test of whether the counter's verdict changes when
  the claimed bytes are present. If the final landing differs, the P4 result should be re-run on
  the landed commit.
- The absence-signal falsifier (A3) uses path-spelling variants, not a corrupted object store. A
  genuine entry with a canonical path is read correctly (P5 canonical base r51 and P4 canonical
  target), so the flaw is in the signal's specificity, not in routine reads.
- The base control cannot be flipped to MET by any base-resident content I could find (A11: zero
  base files match the candidate's `| Pn | Sn |` row shape), but I did not attempt to construct a
  base file, because base objects are immutable and constructing one would no longer be the
  frozen base.
- No installs, no package query, no network, no live/host reads, no screenshots, no producer
  execution. No git/jj mutation in the lane; all mutations were in the scratch clone, each after a
  `git rev-parse --show-toplevel` assertion. Scratch was removed after the receipts were copied
  into the seat directory (verify: `/fast/scratch/hyaku/mado-r52/Attack30` absent).

## Trailers

Report: `.ufo/waves/round-52/w2/Attack30.md`
Report: `.ufo/waves/round-52/w2/Attack30/repro.sh`
Report: `.ufo/waves/round-52/w2/Attack30/receipts.txt`
Counter (W1 draft, read-only): `.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py`
Counter (current candidate, read-only): `quality/counters/c2-r52-proposition-entry.py`
Control: `.ufo/waves/round-52/controls/c2-do-nothing.md`
