# mado round 32 — registration (FROZEN before any data seat)

Lane: `mado-shokunin`. Round: 32 (attempt 1). Base: `master` at `256222890d935212874a09751ff9b7869943c2d7`
(round-31 lane tip). Driver: hyaku inline, in-session L1. Identity: `Kimi fresh L1`.

Axes owned: **coverage + operability** (prompt §1) — the lane's own scored axes
(`SCORECARD.md` round-31 table): coverage/navigation 43/43 = 1.0, calibration
resolved-active 39/40 = 0.9750 (**lowest**), sourced-art 1.0, operability selftest
9/9 = 1.0. Saturation line 9.0, stagnation window N=3; retired axes: none.
**Lowest-axis obligation:** calibration — C2 works it.

The round contract is 1–3 causally separable claims; this round declares **2**.

---

## C1 — coverage: the Hyprland IPC two-socket contract, frontier → core

**Surface moved.** The lane holds no entry on the compositor's IPC request-socket /
event-socket contract or its dispatcher surface. The coverage map
(`corpus/README.md`, 43 rows) mentions `socket2` only incidentally (the hyprctl
verification layer, the binds note); the Frontier lists "Waybar module text",
"dispatcher behavior" and "per-window rule effects" as unresolved. After this
claim the lane holds, on cited ground it did not hold:

- `corpus/knowledge/ipc-contract-r25.md` — the two sockets, the request grammar, the
  event framing (cites **S186**, **S187**, **S189**);
- `corpus/knowledge/dispatcher-semantics-r25.md` — dispatchers describe, they do not
  act (cites **S188**);
- `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` — the dispatcher
  surface on the host's own 0.56.x release line (cites **S196**);

plus **five** appended `corpus/SOURCES.md` registry rows (S186, S187, S188, S189, S196),
each re-grounded **in this round by the L1** (opened 2026-10-24, ≤25-word located
quote), normalized to the census 11-column schema, `status=mined`, `used-by` naming
exactly the admitted entries that cite the row, `recheck` a valid ISO date or
symbolic cadence (no prose recheck cells).

**Source of the material.** `/home/vgpnk/Projects/shokuknow/merge/mado/` — READ-ONLY.
Nothing is written, committed, fetched or pushed into that repo; the campaign tools
(`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py`)
all write there and are therefore **read, never run**. Adoption = read package bytes,
write only inside `mado-shokunin`.

**Frozen counter** (one command over committed bytes; no new instrument):

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
A=corpus/knowledge/ipc-contract-r25.md
B=corpus/knowledge/dispatcher-semantics-r25.md
C=corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md
e=0; for f in "$A" "$B" "$C"; do [ -f "$f" ] && e=$((e+1)); done
r=$(grep -cE '^\|[[:space:]]*S(186|187|188|189|196)[[:space:]]*\|' corpus/SOURCES.md)
c=$(grep -cE '^source:.*S(186|187|188|189|196)' "$A" "$B" "$C" 2>/dev/null | awk -F: '{s+=$2} END{print s+0}')
echo "entries=$e rows=$r cited_entries=$c"
```

**Target:** `entries=3 rows=5 cited_entries=3`. **Kill rule:** the claim is met iff the
counter prints exactly that triple at the tip; anything else is an honest stop and the
target is NOT narrowed after landing.

**Do-nothing controls (K1).** In scratch, on a copy of the lane tree:
(a) append only the five rows, no entries → `entries=0` → target unreachable;
(b) add only the three entries, no rows → `rows=0` → target unreachable.
Neither half alone reaches the target, so the counter cannot be met by a one-sided
commit. A control receipt is committed under `.ufo/waves/round-32/c1/controls/`.

**Item-10 gates this claim must pass (operator directive 2026-10-24).**
1. *ID collision, in scratch, before any append.* The lane registry keeps moving after
   the package was built. The extractor MUST accept 0–3 leading spaces (the census
   parser does), so the check is
   `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` on both the lane registry and
   `SOURCES.append.md`, then `comm -12`. **Guard proof required before the first
   append**: a scratch registry carrying an indented `  | S002 |` row that the staged
   set collides with MUST produce a non-empty `collisions` file; if it does not, the
   guard is broken and nothing appends.
2. *Per-entry gate*: PROVINCE.md scope check + `corpus/QUALITY.md` bar per entry.
   ≥1 admit and ≥1 reject with reason + flip condition in the lesson's `## Gate`.
3. *Transformation*: no staged row is appended as-is. Staged rows are campaign-schema:
   recheck becomes a valid ISO date / `NNd` / symbolic cadence with the stripped prose
   recorded in the lesson's Gate block; no cell contains a literal or escaped `|`;
   `used-by` lists exactly the admitted entries citing the row; status `mined`.
4. *Validate before append*: mirror the lane in scratch (copy of `corpus/` + the append
   block + the admitted knowledge files at their repo-relative paths) and gate on
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file
   "$A/validate/corpus/SOURCES.md"` → exit 0 (warnings allowed) BEFORE the first append.
5. *Quarantine*: the lane's slice of the campaign absent-defect register
   (`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`)
   is hand-checked row by row this round (fetch the cited source, locate the quote).
   A row whose payload is absent → refuse (fabrication class); a prose-class row →
   unverifiable, not fabrication. The register is never edited.
6. *considerthese*: mine at most ONE still-unimplemented proposal from the latest file
   (`considerthese/2026-10-23.md`); the reflection is a pointer, not evidence — open
   what it points at.

---

## C2 — calibration: the lane's published self-assessment must not be stale

**Surface moved.** AXES.md defines calibration as "SHONEN.md/SCORECARD entries match
observed repo state". The lane publishes an axis table per round in prose. The round-31
publication (`SCORECARD.md:2015`, "Axis table re-derived at base (criterion 22):
navigation 43/43 = 1.0; calibration resolved-active 39/40 = 0.9750 (lowest …);
sourced-art 1.0; operability selftest 9/9 = 1.0") is **stale against the repo it
describes**: at the r31 tip the lane's own frozen counter v2 prints `resolved_active=41
active=41` and the hardened gate's selftest prints `12/12 assertions passed`. The
published fractions (39/40, 9/9) are the base-state numbers. The lane never republished
its axis table after its own commits moved the counters.

**Frozen predicate.** The gate reads the **last** `Axis table re-derived` line in
`SCORECARD.md` (the lane's live publication — history is not rewritten) and re-derives
each axis it can re-derive, at the revision under test, by running that axis's own
committed instrument. The published fraction must equal the re-derived fraction.

- `navigation` → `python3 -I quality/check-index.py --rev <rev> --repo .` → `indexed=A/B`
- `calibration` → `python3 -I .ufo/waves/round-31/c2/count.py <rev>` → `resolved_active=A active=B`
- `operability` → `python3 -I quality/check-index.py --selftest` → `A/B assertions passed`

Axes the gate cannot re-derive from a committed instrument (`sourced-art`) are **not
checked and not claimed** — the gate prints which axes it checked. No universal clause.

**Frozen counter** (one command):

```sh
python3 -I quality/check-axis-scores.py --rev <rev> --repo .
```

It prints `MADO_AXIS: checked=A mismatched=M` and exits 1 iff `M>0`.

**Target:** `mismatched=0` at the tip. **Kill rule:** met iff the counter prints
`mismatched=0`; a non-zero count is an honest stop and the rule is NOT relaxed.

**Do-nothing control (K2).** In scratch: (a) a copy whose SCORECARD axis line is left
at the r31 text → the gate must still print `mismatched>=1` (the stale publication is
detected); (b) a copy whose axis line is replaced by the re-derived values → the gate
must print `mismatched=0`; (c) a copy whose calibration fraction is perturbed
(41/41 → 40/41) with no other change → the gate must print `mismatched=1`. (c) proves
the gate is not vacuous. The receipt is committed under
`.ufo/waves/round-32/c2/controls/`.

**Fix.** Append (never rewrite) the round-32 axis table to `SCORECARD.md`, re-derived at
the tip by the commands above, and append the correction to the lane's correction
ledger. History stays.

---

## Frontier step (rides inside the cap; no third claim)

- `corpus/SOURCES.md` census before → after, command and exit codes pasted.
- `corpus/lessons/round-32.md` carries `## Gate` (≥1 admit, ≥1 reject with reason and
  flip, the quarantine verdicts) and `## Mistakes` (class · evidence · captured-by ·
  fix, each fix shown able to fail).
- **Sourced claim:** C1 rests on S186/S187/S188/S189/S196 — rows opened and re-grounded
  this round.
- Source census at round end must exit 0:
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin mado`.

## Wave

One v1 wave, 32 seats, band 32–64, policy
`/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`, spec
`.ufo/waves/round-32/w1-spec.json`, reports `.ufo/waves/round-32/w1/reports/`.
Seat roles: scout 7, executor 5, scribe 4, reviewer 6, critic 4, connector 2,
revenger 1, sentinel 1, mutation-tester 1, simplifier 1 — **13 of 32 (40.6%) attack
roles** (reviewer 6 + critic 4 + revenger 1 + mutation-tester 1 + sentinel 1).
`planner` is a frozen-topology seat the validator rejects: the L1 holds it; the bounded
planning data-walk rides the scout/connector items. Routing is the operator's
`task.agentModelOverrides` table in `~/.omp/agent/config.yml` (read-only here) — the
role decides the route; no model literal is written into the lane repo.

**Kill rule for the round:** if a claim's counter is not met at the tip, it is reported
as not met. No target is narrowed after any seat has scored.
