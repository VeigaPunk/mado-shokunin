# mado round-65 — claims declaration (FROZEN before landing; declared 2026-11-03)

Base revision (measured, all before-receipts at this rev): `524fa1f90b1f2de44b3019bacf833d54e0af13a0`.
Substrate fact: the omarchy Linux host returned (run 15); a live Hyprland 0.56.2 session
(instance `efb50993…_1793632040_1005787507`) is observable read-only. Rounds 57–64 ran on the
Windows host; their dated records stand; this round re-derives the returned-host state.

Axis posture: saturation 9.0 / window N=3, last capability r64 (gap 1 < 3) — stagnation nudge
does not apply. With the host returned, the two omarchy-host rubrics that were un-derivable
since r57/r58 (freshness "file-plane gate agreement"; operability "hermetic suite pass
fraction") are re-derivable; the register that anchors freshness's "surface-state audit
currency" is the record most factually wrong right now (7 rows dated 2026-10-31 say the
omarchy surfaces are ABSENT; on this host all are PRESENT). **The round works freshness
(C1) and operability (C2)** — the two axes whose records this host-return directly invalidates;
freshness is declared the lowest-non-retired-axis target of this round (its published 9.6552 is
stale and its register contradicts the live host). No axis is distinctly lowest while dormant;
this declaration names why freshness is the duty's target. Claims are causally separable: C1
lands without C2's script, C2 lands without C1's register block.

## C1 — freshness: the surface-state register re-derived on the returned host (SOURCED)

**Deficiency (before, at base):** PROVINCE.md's only dated surface-state register block is
2026-10-31 (Windows host): `grep -c 'absent (2026-10-31)' PROVINCE.md` → **7** rows that
contradict this host, and no receipt on this host re-derives any omarchy-era freshness rubric
(the live gate had not been run since the host returned).

**After-state (frozen predicate, one sentence):** PROVINCE.md carries an appended
`### Surface state register (2026-11-03` block whose table re-derives all eight surface groups
of the 2026-10-31 register for THIS host — each row a state cell observed 2026-11-03 plus a
read-only probe and a committed receipt pointer — and the named round-65 receipts (including a
live `MADO_VERIFY: CLEAN` gate run) exist at the landing revision.

**Counting command:** `python3 quality/counters/c1-r65-register.py --repo . --rev <landing>`
→ prints `MADO_R65_REGISTER: … verdict=TARGET_MET` exit 0 (rows=8, receipts resolved at rev,
gate-clean line present at rev); `TARGET_MISSED` exit 1 otherwise. The counter reads git
objects at `--rev` only; it never reads the worktree.

**Before:** verdict=TARGET_MISSED at base (no 2026-11-03 block; 7 stale rows; no round-65
receipts). **After:** verdict=TARGET_MET at the landing rev. **Kill rule:** if the block lands
but any of the eight groups' probe does not re-derive (probe output contradicts the row's
state cell), the row is corrected before landing; if a group is genuinely unobservable on this
host (e.g. the Windows desktop plane — no powershell here), its row records exactly that with
the probe that shows it, and that row still counts (the predicate is re-derivation with an
honest state cell, not presence).

**Rubric re-derivation (same claim, the freshness sub-axis number):** the omarchy freshness
rubric "file-plane gate agreement" re-derives from the committed gate receipts: file plane
`pass=29 fail=0 unknown=0` (29/29 → 10.0000) and full live run `pass=52 fail=0 unknown=0`
(52/52 → 10.0000), receipts `.ufo/waves/round-65/receipts/gate-fileplane-r65.txt` /
`gate-live-r65.txt`. Published value 9.6552 (2026-10-17 era) is superseded by a measured
10.0000 on the returned host; the scorecard row carries both with pointers.

**Sourced leg:** the re-derivation re-opens registry rows this round — S028 (Hyprland v0.56.2
release page) and S097 (omarchy v3.8.4 matte-black theme payload) — each with a Gate block in
`corpus/lessons/round-65.md` (URL, access date 2026-11-03, ≤25-word located quote), and the
rows' recheck cells log old→new (S028 2026-10-19 → 2026-11-03; S097 opened 2026-10-20-era →
2026-11-03). If the re-open shows upstream movement that contradicts a HELD pin, the finding
lands as an erratum and the register row names it (kill-rule correction path, never a silent
pin bump).

**Control (do-nothing, receipted before data):** the frozen counter run at base must MISS.
Receipt: `.ufo/waves/round-65/receipts/control-c1-base-r65.txt`
(`python3 quality/counters/c1-r65-register.py --repo . --rev 524fa1f9…` → TARGET_MISSED rc=1;
base greps: 2026-11-03 block absent, 7 stale rows).

## C2 — operability: the landing-counters standing instrument (capability acquisition)

**Deficiency (before, at base):** no committed single-command landing-counters leg exists
(`ls quality/landing-counters.sh` → absent, rc=2); every round since r55 re-types 4+ ad-hoc
counter commands per landing (r64's landing-counters receipt was a hand-orchestrated run whose
in-receipt rc was even wrong once — ledger-red-leg-rc.txt, QUALITY 26), and the r64 planned
item asked for exactly this standing leg.

**After-state (frozen predicate, one sentence):** `quality/landing-counters.sh` exists at the
landing revision and — run from committed bytes extracted at that revision — prints one
`MADO_LANDING_COUNTERS: GREEN` verdict with all four legs green (navigation indexed=N/N exit 0;
used-by TARGET_MET; ledger TARGET_MET; citecheck missing=0 TARGET_MET over
`.ufo/waves/round-65/receipts`), after its own `--selftest` exits 0.

**Counting command:** `python3 quality/counters/c2-r65-landing-instrument.py --repo . --rev
<landing> --scratch-root <scratch>` → extracts the instrument and its named dependencies at
`--rev` into scratch, runs `bash landing-counters.sh --selftest` then the landing run
(`--repo <lane> --rev <rev> --scratch-root <scratch>/run`), prints
`MADO_R65_INSTRUMENT: … verdict=TARGET_MET` exit 0 only when selftest rc=0 AND all four legs
rc=0. Reads git objects at `--rev`; scratch under the caller's `--scratch-root` only; refuses
`/tmp`, `/var/tmp` and symlinked scratch roots.

**Before:** verdict=TARGET_MISSED at base (instrument absent at rev). **After:** TARGET_MET at
the landing rev. **Kill rule:** if any leg cannot run green at the landing (e.g. a counter
counts round-65-specific bytes it cannot see), the instrument's scope is corrected before
landing — the legs stay exactly the four named here; no fifth leg is added to make it pass.

**Instrument policy (frozen with the claim):** honors `--scratch-root` (required), refuses
`/tmp`-family roots, honors `TMPDIR` for any temp needs, captures every producer's own rc
(QUALITY 26), spawns nothing beyond the four counter children, no network, writes only under
its scratch root. SCORECARD capabilities table row enters this round.

**Control (do-nothing, receipted before data):** the frozen counter run at base must MISS.
Receipt: `.ufo/waves/round-65/receipts/control-c2-base-r65.txt` (TARGET_MISSED rc=1 at
`524fa1f9…` — instrument absent at that rev).

## Harm watch (every claim, re-run at the landing)

navigation counter exit 0 (N/N); used-by TARGET_MET; ledger TARGET_MET; census validate exit 0
at round end; both fail-closed checkers' selftests green with caller-declared scratch roots;
`tools/mado-verify.sh` bytes untouched (sha prefix `050efc720599345a` re-measured); the live
gate re-run ends CLEAN or its diff is an erratum, never a silent rubric bump; every record
edit is an append (head-prefix cmp discipline); no config tree, compositor state or sibling
repo written; no r56-era material opened (security boundary); no credential-shaped capture
(the r56 rule).

## Sources & frontier (§2b)

- Census start exit 0 receipted (`census-start-r65.txt`); census re-run at round end, exit 0
  required.
- Sourced claim: C1 (S028 + S097 re-opened 2026-11-03, Gate blocks in the lesson, recheck
  cells logged old→new).
- Mistake mining: `corpus/lessons/round-65.md` `## Mistakes` — candidates carried in: the r64
  spot-check §8's two report-prose drifts (mined if not already in round-64.md), plus any
  in-round defect.
- Assimilation: screen `merge/mado/` (shokuknow reachable on this host — to verify); adopt one
  theme only if it fits C1/C2, else report `Assimilation: none` with the reason.
- Considerthese: re-screen; at most one adoptable proposal.

## Wave plan (L2 floor)

ONE v1 wave `w1`, 12 seats (band 8–16, policy `/home/vgpnk/Projects/shokunin/scripts/hyaku/
ufo-wave-policy.json`), attack share 4/12 = 33 % (reviewer ×2, critic, mutation-tester),
connectors 1, scouts 2 (route decides the model; never passed). Dispatch via the inline spawn
handoff: spec → validate (`ufo-swarm-wave.mjs run`) → `<wave>.ready` → orchestrator spawns →
WAVE-DONE. Seats write only inside their own seat dir
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-65/w1/<SeatName>/`; scratch
`/fast/scratch/hyaku/mado-r65/w1/<SeatName>/`, removed at exit.

Frozen 2026-11-03 before any seat scored. No predicate changes after scoring (kumitate r42).
