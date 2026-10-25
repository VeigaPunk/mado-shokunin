# CritC1Overfit — shape audit of the round-34 C1 coverage claim

Read-only audit. Scope: `.ufo/waves/round-34/registration.md` C1 section,
`.ufo/waves/round-34/c1/{count.py,frozen.json}`, the landed entry
`corpus/knowledge/waybar-module-text-route-r25.md`, the corpus frontier table
(`corpus/README.md`), the source registry (`corpus/SOURCES.md` rows S201/S202),
and the round-34 control receipts.

## What the predicate actually counts

PRED-C1-r34-v1 passes iff three hard numbers hold — `closed_entries=1`,
`closed_rows=2`, `open_cites=0` — over a spec that names exactly one file
(`frozen.json:5-7`). A "closed cite" requires five conjunctions
(`count.py:150-158`): regular file inside root with nlink=1, fetch bytes read
with O_NOFOLLOW sha256-equal to the frozen digest, a 1–25-word `gate-quote:`
line equal to the frozen quote *and* a contiguous substring of the blob,
exactly one SOURCES row for the id, and that row's last cell equal to exactly
`{entry path}`.

So the predicate verifies **citation closure over one named file**: the file
exists, its two frozen quotes appear verbatim in two sha-pinned upstream
blobs, and the registry bookkeeping points back at it. Controls confirm the
counter is real, not a tautology — do-nothing, symlink-crib, and
used-by-prefix trees each print `closed_entries=0 … TARGET_MISSED` exit 1;
only the golden tree prints `TARGET_MET` (`.ufo/waves/round-34/controls/
c1-donothing.txt`, `c1-symlink-crib.txt`, `c1-used-by-prefix.txt`,
`c1-golden.txt`).

## Where the shape overfits the axis

1. **One file is the entire denominator.** `frozen.json` enumerates the
   surface as `{this entry: [S201, S202]}`. The counter can only ever output
   0/0/2 or 1/2/0 on a real tree — it is an existence-plus-integrity check on
   a single artifact, repackaged as a coverage measurement. Coverage per
   `AXES.md` is "fraction of the domain's real surfaces the skill governs";
   a predicate whose universe is one pre-named file does not measure a
   fraction, it measures that file.

2. **The probe is shape-only, not semantic.** A passing entry needs only the
   two `gate-quote:` lines plus the SOURCES back-pointer. Nothing checks for
   OBS/UNK content, a source-summary row, index landing in `README.md`, or
   that the file describes the named surface at all — a two-line stub with
   verbatim quotes passes identically. `count.py` never reads the entry's
   prose.

3. **The "frontier → core" bookkeeping is outside the predicate.** Nothing in
   the counter touches `corpus/README.md` frontier prose — which as of this
   audit still lists "Waybar module text" as unresolved (first Frontier
   bullet, and the round-12/round-16 bullets' "actual module text stays
   unmeasured"). The claim's own wording — "surface moved from frontier to
   core" — names a move the predicate does not verify happened; the README
   gained only an index row (line 58), no frontier amendment.

4. **Extra citations are invisible.** The counter iterates `spec["entries"]`
   only; an entry that also cites a fabricated S999 would still print
   `open_cites=0` (round-33's controls demonstrated this — `c1-extra-source`
   printed TARGET_MET; no equivalent control exists in round-34's suite).

5. **Scope shrank after the miss.** Round-33's C1 froze `closed_entries=2,
   closed_rows=4` over this same file plus `event-delivery-limits-r26.md` and
   missed; round-34 retries this file alone with new ids (S201/S202 vs
   S190/S191). The registration is candid that C1 is the round-33-missed
   axis, but halving the target to clear it is a calibration smell the
   coverage score will inherit.

## Is the substantive move coverage?

Partially yes. The entry lands two sha-pinned upstream Waybar sources
(`backend.cpp:38`, `window.cpp:27` at tag 0.15.0) describing how the Hyprland
modules consume the event socket — ground the corpus did not hold (round 16
covered the custom-module producer→render route; round 32 covered the
compositor's socket contract; neither covered the Waybar Hyprland-module
client path). Under lane convention (rounds 15–18, 24) a documentary route
onto sourced ground is a legitimate coverage increment.

But the move is smaller than "frontier → core" implies: the entry's own UNK
states "whether this host's bar uses the Hyprland window module is
unverified," and the long-standing frontier item — reading *actual* module
text — stays open. What moved is a bounded upstream-documentary subset, not
the frontier item.

## Verdict

**Neither pure coverage claim nor tautology — a shape-only proxy over a real
but narrow increment.** The counter is killable (controls prove it), and a
genuine documentary-route landing exists behind it, so the claim is not an
empty file-count. But the predicate hard-codes its entire universe (one
file, two cites), verifies integrity and bookkeeping rather than any content
or surface property, and cannot observe the frontier amendment the claim's
"frontier → core" phrasing asserts. A content-free stub scores identically.

**Axis match: yes, with a scoping caveat.** Coverage is the right axis for a
new sourced corpus entry — that is what the axis measures. The mismatch is
not the axis but the *magnitude* the claim language implies: "surface moved"
should read "bounded documentary route added, live module text still open."
The entry itself is honestly scoped; the registration headline overshoots
what both the predicate and the note support.

Admissible as a coverage claim under `AXES.md`'s minimal "citation resolves"
rule; weak as a coverage *measurement*. Recommend the round report score it
as a narrow documentary-route increment and record the frontier item as
still-open, matching round-16's own convention.
