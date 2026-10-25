# Round 35 lesson — mado

Two claims, distinct axes, frozen at `19e4ab3171c1540c40d6b12097745af98053b07d`
before any round-35 data landed (`.ufo/waves/round-35/registration.md`):

- **C1 — coverage.** The idle-lock control surface: three admitted knowledge
  entries and eight registry rows, adopted from the shokuknow merge package
  (`merge/mado/`) and re-grounded in-round. Counter `PRED-C1-r35-v1`,
  target `closed_entries=3 AND closed_rows=8 AND open_cites=0`.
- **C2 — calibration.** The lane's own evidence ledger: the clause ledger,
  the retired dead clause, the TOCTOU split, the re-issued frozen-blob ledger.
  Counter `PRED-C2-r35-v1`, target
  `uncovered=0 AND retired=1 AND toctou_declared=1 AND ledger_tip_ok=1`.

Attempt 1 died without a report after dispatching its 64-seat wave 1; attempt 2
inherited `.ufo/waves/round-35/` and finished the round. Inherited material that
was **reused** (re-verified this attempt): the freeze commit and both counters,
the eleven control receipts, the eight fetch receipts, the golden tree, and the
wave-1 seat reports under `.ufo/waves/round-35/w1/`. Inherited material that was
**discarded** (never applied): nothing — no attempt-1 draft was applied to a
lane file, because attempt 1 died before any lane file was written. The only
inherited lane edit was two `LOG.md` seat-scratch entries, kept and cited below.

## Gate

### Census before → after

Command, run at round start and round end:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

**Before** (round start, registry 192 data rows), exit **0**:

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

**After** (registry 200 data rows), exit **0**:

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

Same seven `W04` warnings on old ids (S030…S121), none on S203–S210, same `mado ok`
line, `AFTER_RC=0`. Row count:
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → **192 → 200**.
Exit 0 at round end is the conformance requirement; it holds.

### Admit — eight rows, `corpus/SOURCES.md:205-212`

All eight are host-local `own-work` rows, tier A, `status=mined`, `opened
2026-10-24`; every one is cited by an admitted entry and by nothing else. The
authority for each quote is the entry's `gate-quote:` line; each quote was
re-derived as a contiguous substring of the committed receipt this round
(`.ufo/waves/round-35/fetch/S2NN.receipt.txt`), word counts by `awk '{print NF}'`.

| id | source (path) | opened | located quote (words) |
|---|---|---|---|
| S203 | `/home/vgpnk/.local/share/omarchy/bin/omarchy-first-run` | 2026-10-24 | `located: install/first-run/ lists 12 scripts; the omarchy-first-run body runs all 12; none is idle-lock` (14) |
| S204 | `.ufo/waves/round-35/fetch/S204.receipt.txt` | 2026-10-24 | `located: journalctl --user shows 0 omarchy-toggle invocations; the installer runs 12 first-run scripts` (13) |
| S205 | `.ufo/waves/round-35/fetch/S205.receipt.txt` | 2026-10-24 | `located: hypridle runs as pid 1667 and started in this session; hypridle.conf sets timeout 150 and 152` (17) |
| S206 | `/home/vgpnk/.config/waybar/config.jsonc` | 2026-10-24 | `located: waybar config.jsonc line 207 opens the custom/idle-indicator module; line 208 runs omarchy-toggle-idle` (13) |
| S207 | `/home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh` | 2026-10-24 | `located: idle.sh pgreps hypridle and prints the tooltip Idle lock disabled when it is absent` (15) |
| S208 | `/home/vgpnk/.local/share/omarchy/bin/omarchy-menu` | 2026-10-24 | `located: omarchy-menu line 207 lists Idle Lock among the toggles; line 212 dispatches omarchy-toggle-idle` (14) |
| S209 | `.ufo/waves/round-35/fetch/S209.receipt.txt` | 2026-10-24 | `located: four dated copies of the bar's configuration each carry the omarchy-toggle-idle handler` (13) |
| S210 | `.ufo/waves/round-35/fetch/S210.receipt.txt` | 2026-10-24 | `located: the toggles/hypr directory holds 2 files and 0 of them name the idle lock` (15) |

Admitted entries: `corpus/knowledge/idle-lock-never-asked-r12.md` (S203, S204),
`corpus/knowledge/idle-lock-chain-armed-r14.md` (S205),
`corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` (S206–S210).

### Refuse — the rest of the assimilation set, with reason and flip

Package census: 147 staged rows and 69 knowledge items (`65` new files under
`merge/mado/knowledge/corpus/knowledge/` + `4` amendments under
`merge/mado/amendments/`; `MERGE-REPORT.md`). **Refused: 139 staged rows and 66
knowledge items**, because the frozen predicate counts exactly
`closed_rows=8, open_cites=0` and only these eight documents are cited by the
three admitted entries. Rows no admitted entry cites are not appended
(CORPUS.md rule 4: expansion is knowledge, not rows).

Two named refusals, so the reason is reviewable rather than a sweep:

- `corpus/knowledge/chinese-article-revision-r30.md` (package, tier-B
  Chinese-wiki revision material) — refused: a documentation-localization
  surface, outside `PROVINCE.md`, the same rule that refused
  `two-literature-drift-r26.md` in round 33 and four register rows in round 34.
  Flip: a desktop/compositor surface cited only from a tier-A or tier-B document
  this lane opens itself.
- Staged row `S203` (Hyprland IPC page, upstream wiki) — refused for this round:
  a compositor-IPC document with no claim over it in round 35; it is also the
  id the lane allocated to the omarchy installer (see the collision note below).
  Flip: a later round freezes a claim over the IPC surface and appends the row
  under a lane id derived by document, not adopted by arithmetic.

The register slice (`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`)
was re-derived this round: 13 mado data rows (6 `payload-absent` + 7
never-checked), matching wave 1's `ScoutQuar`. **Nothing from the slice was
adopted**: the round's theme reaches none of its documents, so each row stays
refused/unverifiable for now and no row was hand-checked into the registry.

### Id remap — by document, not by arithmetic

Derived this round from the adopted entries' own `source:` lines under
`merge/mado/knowledge/corpus/knowledge/`:

| package id | document | lane id |
|---|---|---|
| S315 | `omarchy-first-run` (round-12 fetch of the installer) | S203 |
| S316 | the paired negative (script list + journal count) | S204 |
| S327 | the idle-lock chain state (round-14 fetch) | S205 |
| S335 | `~/.config/waybar/config.jsonc` | S206 |
| S336 | `omarchy/default/waybar/indicators/idle.sh` | S207 |
| S337 | `omarchy/bin/omarchy-menu` | S208 |
| S340 | the dated bar-config copies sweep | S209 |
| S342 | the omarchy toggles-state sweep | S210 |

**Erratum, recorded not rewritten.** `registration.md` names the package's ids
for these documents as `S309, S310, S321, S329, S330, S331, S334, S336`. Seven
of the eight are wrong: in the staged registry those ids name the systemd
journal, the gkeep rule file, the Chinese wikitext, the portal registry handler,
Quickshell, `hyprland-protocols` and a Japanese Wayland article. Only S336
matches. The registration is frozen text and was not edited; this table is the
authoritative remap and the mistake is recorded as M35-1.

### Id-collision check

Parser accepts 0–3 leading spaces (the census clause), so an indented row cannot
false-green. Lists, counts and the guard-can-fail proof are committed under
`.ufo/waves/round-35/assimilation/`:

- **Pre-append** (the state the append was validated against,
  `git show 19e4ab3:corpus/SOURCES.md`): 192 registry ids vs 147 staged ids →
  **collisions = 0**.
- **Post-append**: 200 vs 147 → **collisions = 8**, exactly S203–S210 — the
  package's own staged S203–S210 name different documents (Hyprland IPC pages,
  Waybar C++ sources, a Japanese ArchWiki page, a Chinese blog post). The lane
  now owns S203–S210; the campaign must renumber its staged S203–S210 past S210
  before any future append, or the next adoption collides for real.
- **Guard proof**: an indented `  | S203 |` scratch registry plus a staged `S203`
  yields `collisions = S203` (`assimilation/guard/collisions`), so the guard can
  fail and is not a formality. Wave-2 seat `RevCollision` reported the opposite
  ("the `^ {0,3}` prefix carries the indent into the comparison key"). Reproduced
  both pipelines by hand: the spec pipeline extracts the bare id before `comm`
  (`grep -oE '^ {0,3}\|…' | grep -oE 'S[0-9]+'`) and reports `S203`, count 1; the
  seat's variant dropped that second stage and reported 0. The seat's measurement
  is wrong about the specified command, right about the variant it wrote. Its
  other claim stands and is the more important one: the eight real collisions are
  a genuine double allocation of S203–S210 (merge package from a 192-row
  snapshot, wave 1 minting the same ids), unresolved and campaign-owned.

### Scratch validation before the append

The append block was built in scratch and validated on a full mirror before the
real append, per the item: normalized to the 11-column schema (no literal or
escaped pipe, `recheck` a cadence token, `status=mined`, `used-by` exactly the
admitting entries), then
`sources-census.sh validate --file <mirror>/corpus/SOURCES.md` → exit 0
(wave-1 `RevValidate`, re-proved by this round's own run). The real append then
re-ran the root census → exit 0.

## Wave-2 falsifications applied as errata

The wave-2 seats were assigned to falsify the landed text, and two did. Their findings
are applied as append-only errata blocks (criterion 44), not as rewrites:

- `idle-lock-never-asked-r12.md` E1 — the "never toggled" inference is withdrawn: the
  journal's zero `omarchy-toggle` count is a null channel, and the daemon's scope was
  consumed at `2026-10-23T19:24:38-03:00` and restarted at `22:14:11`, a 2h50m window
  with the idle lock down, with no coredump and no OOM. E2 — thirteen executed items,
  twelve of them `*.sh`.
- `idle-lock-chain-armed-r14.md` E1/E2 — the two start lines are two boots' first starts,
  not a restart; the 150 s step calls no lock (`omarchy-launch-screensaver` has no
  `hyprlock`/`omarchy-system-lock`); the title's "the chain will fire" is withdrawn; the
  transient-scope inference is materially true but unlicensed by its own receipt.
- `idle-lock-offered-in-the-bar-r15.md` E1–E5 — the dating clock (mtime vs creation),
  "never taken it" withdrawn, "built not to remember" replaced by the actual mechanism
  (`omarchy-toggle-idle` is process-shaped and `autostart.conf` re-arms the daemon), the
  indicator names one state and is silent for the other, and "leaves no trace" scoped to
  on-disk state.

`PRED-C1-r35-v1` is unchanged at `closed_entries=3 closed_rows=8 open_cites=0` after every
errata append, because the predicate scores shape, quote legality and digest presence —
not truth. That gap is the round's central finding (M35-2) and the reason the counters
are reported with their limits rather than as evidence of correctness.

## Mistakes

Four mistakes, named here at section level so a citation check that reads `#mistakes`
sees them: **M35-1** id-space citation (the registration's package-id list was copied,
not derived) · **M35-2** instrument vacuity (the C1 counter's digest clause is dead and
a shape-only tree passes) · **M35-3** misrooted seat output (swept clean — no lane file
at the fleet root) · **M35-4** a repaired label is still a dead observable (C2's
`ledger_tip_ok` cannot separate the defect it repairs from the fix).

### M35-1 — id-space citation (class: id-space)

**What happened.** `registration.md` lists the merge package's ids for the eight
adopted documents as `S309, S310, S321, S329, S330, S331, S334, S336`. The
package's own entries cite `S315, S316, S327, S335, S336, S337, S340, S342`.
Seven of eight are wrong documents. The error was invisible while the lane's ids
were the only ones the counters read — the C1 counter never looks at package ids
— so it would have surfaced only during the campaign's reconciliation.

**Evidence pointer.** `.ufo/waves/round-35/registration.md` §"The two routed r34
defects", item 4; the true map is the table above and in
`.ufo/waves/round-35/w1/reports/ScribeFrontier.md`;
`.ufo/waves/round-35/w2/reports/RevIdRemap.md` attacks it directly.

**Captured-by.** `lessons/round-34.md#gate` — "every adopted entry's citation is
re-pointed **by document**, not by arithmetic". The rule existed and was
followed for the *adopted* ids; what it did not require was that an id list
written into a **frozen registration** be derived from the cited document's own
`source:` lines. A prose list in a freeze document reads as evidence because
everything around it was measured.

**Fix.** Criterion 56's sibling requirement in practice: any id list a round
writes down is derived by opening the cited document and reading its own
`source:` line, and the derivation is committed as a seat artifact. Demonstrated
able to fail: run the derivation against the registration's list and the diff is
nonempty —

```sh
comm -3 <(echo "S309 S310 S321 S329 S330 S331 S334 S336" | tr ' ' '\n' | sort) \
  <(grep -h '^source: S' /home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/idle-lock-never-asked-r12.md \
      /home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/idle-lock-chain-armed-r14.md \
      /home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/idle-lock-offered-in-the-bar-r15.md \
    | sed -E 's/^source: (S[0-9]+).*/\1/' | sort)
```

→ **14 lines**: 7 left-only (S309, S310, S321, S329, S330, S331, S334 — ids the
registration claims that no adopted entry cites) and 7 right-only (S315, S316,
S327, S335, S337, S340, S342 — the ids the entries do cite); S336 is the single
shared id. The check passes only on a derived list; it fails on the copied one.
Wave-2 seat `RevIdRemap` then found the mechanism: the claimed list is exactly
the `was` column of the package's own `lanes/mado/ID-REMAP.md`, uniformly +6
(S309→S315 … S336→S342), i.e. staging ids read from a superseded base.

### M35-2 — instrument vacuity (class: instrument)

**What happened.** `PRED-C1-r35-v1` reaches `TARGET_MET` on a tree with the
right *shape* and no evidentiary payload: eight junk rows with a digest
substring in the anchor cell, three entries that are only `gate-quote:` lines,
and — worse — receipt files fabricated at the frozen paths with different bytes.
The counter pins `receipts[<id>].sha256` (C1 `count.py` `digest-match`) but never
compares it to the bytes it read; the variable is computed and discarded. So the
target was reachable by shape-only work, and the do-nothing control alone did not
catch it.

**Evidence pointer.** `.ufo/waves/round-35/w1/reports/CritVacuous.md` (junk tree,
`TARGET_MET` exit 0), `.ufo/waves/round-35/w1/reports/RevTarget.md`
(`fake-all`: fabricated receipts, still `TARGET_MET`), `.ufo/waves/round-35/w1/reports/CritVacuous2.md`
and `RevDoNothing.md` (the same shape problem on C2's worktree-trusting
observables).

**Captured-by.** `QUALITY.md` criterion 36 (the do-nothing / all-false / junk /
echo crib list) required a tree that *skips* the claimed work. It did not
require a tree that *fakes* the result. The round-35 freeze added eleven
controls, all of which skip; none fabricates.

**Fix.** Criteria 55 and 56 (appended this round, `corpus/QUALITY.md:361-362`):
every shape counter names its indirection and content cribs, with a committed
`TARGET_MISSED` receipt each, and every live clause is accounted controlled or
declared. Applied to the round-35 counter the fix *fails it* — that is the
demonstration:

```sh
python3 -I .ufo/waves/round-35/c1/count.py --root .ufo/waves/round-35/scratch/CritVacuous \
  --frozen .ufo/waves/round-35/c1/frozen.json
# PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET, exit 0
```

A criterion that cannot fail on the artifact that produced it is decoration. The
round-35 predicate was frozen before data and is not amended; the repair is a
round-36 claim: bind the digest to the bytes read, and add the content cribs as
committed controls. **The repair is demonstrated on a scratch copy** —
`.ufo/waves/round-35/scratch/L1DigestFix/count-fixed.py` (committed at `4f35c80`; its
working-tree copy was dropped with the mutant trees), one added conjunct
`and digest == receipt["sha256"]`:

```text
--root .                     -> closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   rc=0
--root controls/golden       -> closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET   rc=0
--root scratch/CritVacuous   -> closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED rc=1
```

So the round's data survives its instrument's repair while the fabrication does
not; the two cribs are committed as `controls-content/c1-shape-only/` and
`controls-content/c1-fabricated-payload/`, each printing `TARGET_MET` on the
frozen counter.

### M35-3 — misrooted seat output (class: hygiene)

**What happened.** A wave-2 seat wrote its report into the **fleet** root at
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-35/w2/reports/RevLogEvidence.md`
(seat `RevLogEvidence`), because seat tools start at the fleet root and the
renderer's `Report:` trailer is lane-relative. The lane copy did not exist.

**Evidence pointer.** `find /home/vgpnk/Projects/shokunin/.ufo/waves/round-35 -type f`
→ 1 file before the sweep, 0 after; `cmp` between the fleet copy and
`mado-shokunin/.ufo/waves/round-35/w2/reports/RevLogEvidence.md` → identical;
fleet-root `git status --porcelain | grep round-35` → empty after the sweep.

**Captured-by.** the item's misroot rule, applied at round end — but the wave
`context` already carried the sentence "Any `Report:` trailer path the renderer
gives you is RELATIVE to …", and this seat still resolved it from the fleet root.
The context sentence is necessary and was not sufficient.

**Fix.** The sweep procedure was run as specified: copy byte-exact into the lane,
`cmp`, delete the fleet copy. Demonstrated able to fail: with the file planted at
the fleet root the sweep's `git status` finds it (it did, at 03:41); after the
repatriation the same command prints nothing (`no round-35 at fleet root`). The
sweep, not the context sentence, is the control.

### M35-4 — a repaired label is still a dead observable (class: instrument)

**What happened.** The round-34 spot-check routed a stale tip label: `RevFrozenBlobs.md`
named `fa7ba113` the lane tip when the round-34 tip is `dff3941`. Round 35 repaired it
by re-issuing the ledger at the real tip and made `ledger_tip_ok` an observable of
`PRED-C2-r35-v1`. Wave-2 seat `MutC2Real` then mutated the re-issued ledger: changing
**one** of its six copies of the tip hash leaves `ledger_tip_ok=1` and the verdict
`TARGET_MET`; so does a fully stale label wherever the hash survives in a fenced repro
block; so does corrupting one blob id in the ledger's own table. Only deleting *all*
tip tokens kills it. The observable tests `spec["r34_tip"] in text` (`c2/count.py:106`)
and re-derives the blob ids from `frozen.json` and git — it never parses the document's
table, so the document's own claims are unobserved.

**Evidence pointer.** `.ufo/waves/round-35/w2/reports/MutC2Real.md` (seven mutants,
M3a/M3c/M3d survive, M1/M2/M3b/M4 killed; every mutant restored byte-identical).

**Captured-by.** criterion 56 (appended this round) requires every live clause to be
*controlled* — a named control whose committed receipt records a `TARGET_MISSED`
verdict for which that clause is the load-bearing check. M3a is exactly that clause's
failing case and no such control existed before data.

**Fix.** C2's predicate is frozen and `TARGET_MET` as written; the verdict is reported
with its limit rather than upgraded. Round-36 claim: make `ledger_tip_ok` parse the
ledger's own table and require every row to name the tip and a re-verifying blob id,
with `MutC2Real`'s M3a/M3c/M3d as committed controls. Demonstrated able to fail on the
*proposal's* evidence, not on a built counter — no proposed counter exists this round,
so by the fix-counts-only-once-shown-able-to-fail rule this is a routed claim, not a
landed fix. What the round does show: the current counter prints `TARGET_MET` on M3a
(the receipt in `MutC2Real.md`), which is the failing case a future control must turn
to `TARGET_MISSED`.

Two further fail-open paths on the same counter, found by wave-2 seat `RevC2Tip` and
recorded, not repaired: deleting a live clause **together with its control** from
`c1/clauses.json` leaves `uncovered=0` and the verdict `TARGET_MET`, because nothing
cross-checks the ledger against the counter's own clause set; and a covered clause's
receipt is a token grep, so pointing a clause at any file containing
`verdict=TARGET_MISSED` (including a one-line file) leaves the clause "covered". The
ledger's `retired` entry is likewise an unbound string set.

## What this lesson does not license

The C1 counter is a *shape* counter with a dead digest clause (M35-2). Its
`TARGET_MET` on this round's real tree is evidence that the three entries and
eight rows are present and mutually consistent — not that the receipts are the
bytes the digest names. The receipts themselves were re-opened and re-derived
this round by wave-2 seats, and the report says which of those verdicts landed.
The entries' remaining unknown — whether the operator wants the idle lock off —
is unchanged and answerable only by the operator.
