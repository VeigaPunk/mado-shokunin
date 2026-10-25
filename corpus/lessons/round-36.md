# Round 36 lesson — mado

Two claims, distinct axes, frozen at `dbf8b579aeac0f023aaf595770f1cb0049e4baa2`
before any round-36 data (`.ufo/waves/round-36/registration.md`):

- **C1 — calibration.** The two round-35 admission counters are repaired and shown
  to discriminate: `PRED-C1-r36-v1` (`quality/counters/c1-idle-lock.py`) binds the
  receipt digest to the bytes it read and adds the census E12 registry fence;
  `PRED-C2-r36-v1` (`quality/counters/c2-ledger.py`) pins the clause set, binds each
  clause to a measured control receipt and parses the blob ledger's own table at a
  computed tip. Measured by `quality/check-counter-discrimination.py` over the frozen
  25-control manifest: before 14/25, after 25/25.
- **C2 — operability.** The lane's own records pass an evidence-pointer durability
  gate: `PRED-PTR-r36-v1` (`quality/check-evidence-pointers.py`) re-derives every
  pointer, the inherited uncommitted set, the round-35 scratch disposition and the
  tip-revision axis transcript from committed bytes. Before `TARGET_MISSED`, after
  `TARGET_MET`.

## Gate

### Census before → after

Command, run at round start and round end:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

**Before** (round start at `dbf8b57`, 200 data rows), exit **0**:

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

**After** (round end, 201 data rows), exit **0** — the same seven pre-existing
`W04` warnings on old ids (S030…S121), no finding on the new row, and the same
`mado ok` trailer:

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

Rows 200 → 201. Rows added by tier: one, tier **A**. Rows touched old→new: **none**
— no existing row's `status`, `recheck` or `used-by` changed
(`git diff 7a068cb master -- corpus/SOURCES.md` is the audit; the round-35 tip's
`SOURCES.md` blob is byte-identical to `master` apart from this round's one
appended line).

### Sources opened this round

**Admitted — S211.** Negative controls in observational studies. URL
`https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/` (PMCID PMC3053408; free author
manuscript of *Epidemiology* 2010;21(3):383–388), opened **2026-10-25**, HTTP 200,
receipt `.ufo/waves/round-36/fetch/S211.receipt.txt` (1,037 B; the fetched HTML's
per-request sha256 is recorded in the receipt header but is *not* stable — see the receipt's
note on the extraction digest). Located quote, 17 words, contiguous in
the receipt:

> the protective effect was observed even in circumstances where the vaccine could not have caused the protection

Location: §S2 "Examples of the use of negative controls in epidemiology", paragraph
`#P15` (the Jackson et al. negative-control-outcome example) — the row's first anchor said
"Introduction"; a non-author re-open located the paragraph in S2 and the row's anchor cell
was corrected in place (old → new recorded under `## Gate`). It grounds exactly the rule this round's C1 instrument is built on — a claimed effect
that appears where the claimed cause is impossible is instrument failure, not
evidence — and it is what the reject half of the 25-control manifest applies to the
lane's own counters. It does **not** license anything about software counters
directly: the transfer is the method (find an input where the claimed work cannot
have happened, and require the instrument to say so), not the epidemiology.

**Considered, not opened, not a row.** `https://pmc.ncbi.nlm.nih.gov/articles/PMC12186581/`
(a 2025 commentary on imperfect negative control exposures) surfaced in the same
search and was **not** opened this round; per CORPUS.md rule 1 it cannot be a row
until it is read. Flip: open it if S211's own definition proves insufficient for a
future claim.

### Gate decisions for the round

- **Admit S211** — tier A for its scope (original peer-reviewed statement, author
  manuscript), cited by this lesson, `used-by` exactly
  `corpus/lessons/round-36.md`, status `mined`.
- **No other row** — this round admits no knowledge entry, so no other row is
  written; the campaign package still holds refused material from round 35 and
  nothing from it is re-adopted while its evidence chain is under repair
  (`Assimilation: none this round`, registered before data).
- **Spot-check duty** — the quote was re-opened by a non-author seat in this round's
  wave and its verdict is recorded in the round report; the independent closure
  spot-check still re-opens a sample.

## Mistakes

Six mistakes, named at section level so a citation check reading `#mistakes` sees
them: **M36-1** a fixture generator shipped with a dead branch (instrument) ·
**M36-2** a ledger drafted below its own frozen minimum (number-drift) ·
**M36-3** a control whose receipt says `TARGET_MISSED` does not prove which clause
killed it (instrument) · **M36-4** the before-measurement nearly passed fail-open
because a fixture lost its git context (vacuous) · **M36-5** record work crowded
out the domain and no round said so (stale-premise) · **M36-6** a frozen
registration carried a command that cannot run as written (reference-drift).

### M36-1 — a fixture generator shipped with a dead branch

**What happened.** The first `gen-mutants.py` carried, inside the
`receipt-unbound` branch, the line `receipts[dst] = Path(src).read_bytes() if False
else b""` and returned a string marker instead of the receipt map. The branch was
written, never read, and never run before the first end-to-end gate invocation.
The `--profile r36` run died on it with
`FileNotFoundError: .../receipts/c1-entry-symlink.txt` while the `--profile r35`
run had already scored 14/25.

**Evidence pointer.** `.ufo/waves/round-36/c2/gen-mutants.py` (the fixed branch);
the failure text is quoted in the round report's work-performed section.

**Captured-by.** `corpus/QUALITY.md` criterion 49 (a composite counter is smoke-run
once at freeze). It did not catch this because the generator cannot be smoke-run at
the freeze for its own reason — the round-36 ledger it mutates is the round's data
and does not exist yet. The freeze smoke could only exercise the `r35` profile.

**Fix.** The generator's first successful run is now part of the gate invocation, and
the gate fails closed (`error=mutant-generation-failed`, exit 2) rather than scoring
fixtures it did not build. Demonstrated able to fail: the pre-fix run exited 2 with
the `FileNotFoundError` text above; the post-fix run exits 0 and prints one
`mutant=<id>` line per fixture. The residual duty is recorded: a generator that
mutates data cannot be smoke-tested before the data exists, so its first real run is
the smoke test and must be run before the claim is scored.

### M36-2 — a ledger drafted below its own frozen minimum

**What happened.** The first `RevFrozenBlobs-r36.md` draft carried two tip-labelled
40-hex lines while the frozen spec requires at least three
(`tip_rule.min_tip_lines = 3`). The prose sentence that was supposed to be the third
line wrapped the hash onto a different line from the word `tip`, so the tip test
counted two. The counter refused to score tip_ok and the whole C2 leg read
`TARGET_MISSED` until the paragraph was rewritten.

**Evidence pointer.** `.ufo/waves/round-36/ledger/RevFrozenBlobs-r36.md` (the fixed
document, four tip lines); `.ufo/waves/round-36/c2/frozen.json`
(`min_tip_lines`).

**Captured-by.** none before the event — no criterion required the drafted document
to be scored against its own spec before commit. `corpus/QUALITY.md` criterion 38
(counter smoke-run) covers instruments, not the artifacts they read.

**Fix.** Run the counter over the drafted artifact before committing it. Demonstrated
able to fail: the pre-fix document prints `tip: 2 tip lines, minimum 3` and
`verdict=TARGET_MISSED`; the post-fix document prints
`tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived`.

### M36-3 — a control receipt does not name which clause it killed

**What happened.** Ten of the fourteen `c1` reject controls are the round-35 crib
trees, which carry the registry *table* without its `## Registry` heading. Under
`PRED-C1-r36-v1` every one of them dies at the `row-in-registry` fence before its
named clause is reached, so their receipts read `TARGET_MISSED` for the fence, not
for `entry-regular`, `row-unique`, `digest-match` and so on. A clause ledger that
pairs receipt to clause on the verdict token alone would therefore claim nine
clause consequences it has not shown — exactly the fail-open criterion 56 was
written to stop, one level up.

**Evidence pointer.** `.ufo/waves/round-36/receipts/clause-attribution.txt` — each
frozen crib re-scored from a `/tmp` copy with the heading restored; every one still
reads `TARGET_MISSED` with exactly one open cite (`closed_rows=7 open_cites=1`),
`c1-donothing` reading `open_cites=8`.

**Captured-by.** `corpus/QUALITY.md` criterion 56 requires every live clause to name
a control "for which that clause is the load-bearing check"; the round-35 receipt
form records only the verdict, so the requirement could not be checked from the
receipt.

**Fix.** Score each control twice — as frozen, and from a copy that removes only the
competing clause — and record both. The attribution receipt is the first half; the
wave's per-clause drop mutants (`MutC1NoDigest`, `MutC1NoFence`, `MutC1CheckAnchor`)
are the second: each drops one conjunct and shows which controls flip. Limit
recorded honestly: the restored-fence probe shows a crib dies with one cite open,
not which conjunct closed it, so the attribution is proven only together with the
drop mutants.

### M36-4 — the before measurement nearly passed fail-open

**What happened.** The eight `c2` controls are mutation fixtures of a *git-backed*
ledger. Before the gate exported `GIT_DIR` for the mutated fixture directories, each
mutant would have failed `tip_ok` simply because `git -C <mutant>` finds no
repository — so all eight reject controls would have read `TARGET_MISSED` for the
wrong reason and the accept control alone would have looked honest. A before score
inflated that way is not a baseline.

**Evidence pointer.** `quality/check-counter-discrimination.py` (the `env["GIT_DIR"]`
assignment and the comment-free `run()` helper); the before receipt
`.ufo/waves/round-36/receipts/before-discrimination.txt` already carries the
corrected invocation.

**Captured-by.** none — the registration named the mutants as "one committed input
changed", which is what caught it during design rather than after.

**Fix.** Every fixture must keep the accept control's ability to resolve whatever the
counter reads *besides* the mutated input. Demonstrated able to fail: with `GIT_DIR`
unset for fixtures, `c2-tip-stale` and `c2-blob-corrupt` both read
`TARGET_MISSED` on the *round-36* counter too (the fixture, not the mutation, is
what fails); with it set they read `TARGET_MISSED` only where the mutation is caught
and `TARGET_MET` where it is not (see the wave's `MutC2HardcodedTip` and
`MutC2NoTable` receipts for both directions).

### M36-5 — record work crowded out the domain and no round said so

**What happened.** Over the lane's last 30 commits, **3** touched a domain-facing
path (`tools/`, `corpus/knowledge/`, `PROVINCE.md`, `SKILL.md`) and **27** touched
only records (LOG, SCORECARD, lessons, wave evidence, `quality/`). The lane never
reported that ratio, so a reader of the round-35 report could not see that the
desktop plane had not moved since round 27's `tools/mado-wsrules.py`.
`considerthese/2026-10-24.md` proposal 1 named exactly this and was still
unimplemented.

**Evidence pointer.** `considerthese/2026-10-24.md` (proposal 1, "track a
domain-versus-meta ratio per window"); the ratio re-derived this round with
`git log -30 --format=%H --name-only` and the path classes above — 3 / 27 at
`dbf8b579`.

**Captured-by.** none — no criterion required the report to state where the round's
work sat relative to the domain.

**Fix.** `corpus/QUALITY.md` criterion 60: every round report states the ratio with
its command, and a lane two or more rounds without a domain-facing change says so.
Demonstrated able to fail: the round-35 report carries no ratio line
(`grep -c 'domain-versus-meta'` on the round-35 report is 0), while this round's
report and this lesson carry one with the command.

### M36-6 — a frozen registration carried a command that cannot run as written

**What happened.** The registration's harm-watch line named
`python3 quality/check-index.py --repo .`. That invocation exits 2
(`SETUP_ERROR: --rev or --root is required`): `--repo` only qualifies `--rev` mode.
A wave seat ran it verbatim, hit the setup error and reported it; the lane's own
harm-watch used the working form `--rev <rev> --repo .` throughout. A command in a
freeze document is read as runnable, so the defect would have been inherited by any
reader re-running the round.

**Evidence pointer.** `.ufo/waves/round-36/registration.md` (the harm-watch line);
the seat's verbatim run and `SETUP_ERROR` text are quoted in
`.ufo/waves/round-36/w1/reports/RevIndexGate.md`.

**Captured-by.** none — criteria 38 and 49 require a counter to be smoke-run at the
freeze, but nothing requires the *prose commands* in a registration to be executed
once before the freeze.

**Fix.** `corpus/QUALITY.md` criterion 61: every command a registration names is run
verbatim at the freeze and its output committed, or it is written with its required
arguments. Demonstrated able to fail: the verbatim run exits 2 with `SETUP_ERROR`,
the corrected form exits 0 with `MADO_INDEX: rev=… indexed=50/50 missing=0
dangling=0 duplicates=0`.

## Scratch disposition

`.ufo/waves/round-35/scratch` is **retained** as round-35 evidence: tracked paths=124
(`git ls-tree -r --name-only master .ufo/waves/round-35/scratch | wc -l`), the
seat mutation and mutation-run trees the round-35 lesson's M35-2 receipts cite. Size, measured
after the round: 1,962,263 bytes ≈ 1.87 MiB (`git ls-tree -rl`), not the ~2.2 MB the round-35
records carry — same order, corrected here. It is
not deleted because deleting it would orphan those receipts, and it is not extended:
this round writes its fixtures under `/tmp` from the committed generator instead.
Round-36 scratch lives under `.ufo/waves/round-36/scratch/` per seat and is committed
only where a report cites it.

## What this lesson does not license

The discrimination score is a statement about **two instruments over one frozen
control set**, not a proof that the round-35 corpus claim is true. The 25 controls
exercise the counters' decision paths; they say nothing about whether the idle-lock
receipts describe the host. The idle-lock surface's remaining unknown — whether the
operator wants the idle lock off — is unchanged and answerable only by the operator.
C2's gate scores the lane's paperwork, never the truth of the facts the paperwork
reports.

## D9 — the provenance convention, counted

Two wave seats settled D9 from the bytes. The **refusal boundary** is now stated once in
`PROVINCE.md` (round-36 refinement: the localized documentation channel is out, the English
config-plane channels are in, the omarchy skill's own files stay read-only documentation
surface) — it decides the r28/r29/r30 package entries and the round-16 Chinese config guide
the same way, which is what the spot-check asked for.

The **provenance-trio convention** is counted, not asserted: **29 of 50** knowledge notes
carry `source:`, `verified-at:` and `recheck:` within their first 15 lines; **21** do not,
and **20 of those 21** carry no trio member anywhere in the file (the 2026-10-14 arc notes
plus `bind-table-r25.md`); `animation-table-r26.md` is the only partial. Command: a
per-file `head -15 | grep -q '^<key>:'` loop plus a full-file anchored grep, both recorded
in `.ufo/waves/round-36/w1/reports/ScoutD9Provenance.md`.

Ruling, append-only: a **new** entry opens with the trio (CORPUS.md's rule); an **existing**
entry is normalized by an appended `## Provenance (normalized)` trailer restating the trio
as anchored lines, never by rewriting its committed bytes. This round admits no knowledge
entry, so the ruling lands with no entry to apply it to; it binds from round 37.

## Gate — corroboration of S211 by a second non-author seat

`ScoutPriorArt` re-opened the same document independently and located the definitional
sentence rather than the example this lesson quotes: anchor `#S1` §"Experimental biology:
threats to causal inference and the use of negative controls", paragraph `#P8`, quote
(22 words) "under conditions in which it is expected to produce a null result and verify
that it does indeed produce a null result". Two independent openings of one URL, two
different located anchors, both supporting the row's `teaches`; the registry's own quote
stays the Jackson-example sentence recorded above, which is the one this lesson's receipt
carries. The seat's guess at a first PMCID (`PMC2833407`) resolved to a proteomics paper
and was rejected before citation — kept here because a wrong-id guess that is checked is
the behaviour the row wants.

## Gate — S211 anchor correction (old → new)

`ScoutPriorArt` reported that the row's anchor cell was loose ("Introduction, the Jackson
example"): the quoted paragraph is `<p id="P15">` under the section heading "Examples of the
use of negative controls in epidemiology" (§S2), not in the Introduction. The anchor cell was
corrected in place — `Introduction, the Jackson et al. negative-control-outcome example` →
`#S2 section Examples of the use of negative controls in epidemiology, paragraph #P15 (the
Jackson et al. negative-control-outcome example)`. No other cell changed; the quote, tier,
scope, status, `recheck` and `used-by` stand. This is the same in-round cell-correction
discipline round 35 applied to S203–S205, and it is counted here rather than left silent.

## Limits the wave left on the instruments (recorded, routed to round 37)

1. **Pointer extraction is prefix-scoped.** `PRED-PTR-r36-v1` counts a token as a pointer only
   when it starts with a repo-root path prefix, so four evidence pointers written bare in the
   round-35 entry (`c1/clauses.json`, `ledger/RevFrozenBlobs-r35.md`, and two knowledge-entry
   names) are invisible to it. None of them dangles, so the verdict stands; the *coverage* is
   narrower than the record (`w1/reports/RevPtrBefore.md`).
2. **A duplicated live clause id passes.** The clause-set pin compares sorted sets, so a
   duplicated id in `clauses.json` reports `extra` in the detail line yet scores `uncovered=0`
   under both the pinned and the unpinned counter; the manifest has no control for that kind
   (`w1/reports/MutC2NoClausePin.md`).
3. **The digest clause's anchor half is unexercised by the frozen manifest** (every `c1` crib
   dies at the registry fence first) and **the tip transcript is a three-substring test**; both
   are proven only by fence-restored probes (`w1/reports/MutC1CheckAnchor.md`,
   `w1/reports/RevAxisTranscriptAsk.md`).
4. **Control order is load-bearing** — the `c2` fixtures embed the gate's own `c1` receipts —
   and that dependency is undocumented in the gate (`w1/reports/ConnGateReuse.md`).
5. **The axis publication's anchor commit is never checked**, and the gate reads the committed
   card, so a dirty tree is invisible to it (`w1/reports/MutPublication.md`).
6. **`quality/check-index-rows.py`'s rev-mode glob check is dead** on host git 2.56.0
   (`--name-only` with `--format`), so every glob citation warns spuriously in rev mode
   (`w1/reports/RevIndexGate.md`). Routed as its own repair, not patched here (criterion 52).
