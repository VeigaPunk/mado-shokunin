# RegistryCollision — S053/S054/S055 id and scope collision review

Seat: read-only reviewer. Date 2026-10-20. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, baseline
`32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.

Scope: `corpus/SOURCES.md` rows and the three reserved ids only — id
allocation, URL/scope duplication, anchor adequacy, `used-by` reciprocity.
No gate/selftest/measure/census run, no package or service operation, no
compositor/input/UI probe, no install. Raw source files were fetched
read-only for digest and line verification; findings below label
`[OBS]` (opened/measured this seat) versus `[INF]` (inference).

## 1. Id allocation — observed

`[OBS]` The registry now holds 55 rows, `S001`–`S055`, contiguous and
unique (no gaps, no duplicate ids): `S`+3 digits, the contract shape.
Histograms at read: tier `A=51 B=1 C=3`; status `mined=43 queued=8
rejected=4`; kind `docs=27 spec=9 code=6 own-work=9 book=1 dataset=1
community=2`. Against the round-15 closure (`rows 52`, `48/1/3`,
`40/8/4`) the delta is exactly the three new A/mined rows: one `docs`
(S053), one `code` (S054), one `own-work` (S055).

`[OBS]` `git diff 32c4fda… -- corpus/SOURCES.md` shows only: three appended
registry rows (`:65-67`), one appended `## Paths` bullet (`:95-98`), one
appended round-16 search-log paragraph (`:209-220`). No existing row cell
changed, so the lesson's "No existing SOURCES status/recheck/used-by
changes" is verified for the current bytes.

`[OBS]` All three rows have 11 cells (`NF=13` under the contract census),
valid kind/tier/status enums, and no `community`+`A` inflation.
**Next unused id is `S056`.** Ids are registry-local, so same-numbered ids
in other lanes are not collisions.

## 2. Collision A — `S053` is double-booked in prose across rounds

`[OBS]` `.ufo/waves/round-15/w1/reports/ReviewKeyboard.md:61-62` says
"No `S053` is reserved" and its accept condition allocates "a text-input
row (S053, to be allocated by L1)" for `text-input-unstable-v3.xml`;
combined acceptance item 6 (`:72`) repeats "S052 and S053 (text-input)".
Round 16 has now allocated `S053` to the Waybar manual. No text-input row
exists, so the table has **no duplicate id** — but a future U6/IME seat
following that filed acceptance condition would write a second `S053` or
cite the text-input reservation against the Waybar row.

Required reconciliation (L1 owns; do not edit the immutable round-15
report): one line in `corpus/lessons/round-16.md` § Gate or the round-16
search-log note stating `S053` was reassigned to the Waybar manual, that
the round-15 text-input proposal was never allocated, and that a future
text-input row must take the next unused id (`S056`+). Confidence: high
(both texts read).

## 3. Collision B — URL duplication: none; W04 set unchanged

`[OBS]` The two new URLs are unique in the registry; no existing row
points at `Alexays/Waybar`. The only other Waybar mention is S013, whose
source is local `/home/vgpnk/Projects/gkeep/install.sh` and whose scope is
operator installer mutation (copied config/CSS/reload), not module
semantics. Disjoint: no `supersedes`, no rejection.

`[OBS]` S053 and S054 are the same module but different artifacts
(upstream manual vs implementation) and therefore complementary, on the
S046/S043 (implementation vs spec) and S047/S048 (two protocol files)
pattern — not the rejected S045/S017 pattern (same URL, overlapping scope).
A merge or duplicate rejection here would be wrong.

`[INF]` The fleet census keys on URL, so S053/S054 add no W04 line; the
existing warning set `S030`, `S042`, `S045` should remain the complete
output of the census for these bytes.

## 4. Collision C — scope boundaries against existing Waybar knowledge

`[OBS]` `corpus/knowledge/waybar-walker-semantics.md:102` records "waybar
has **no IPC/query verb** in 0.15.0 (`waybar --help` …)", a measured
round-3 observation (MAN/RUN legend, `:9-12`), not a source-row claim.
The fetched tagged manual `man/waybar-custom.5.scd` is module-scoped and
contains **zero** `ipc`/`sway` matches, so S053/S054 cannot be cited for
the binary-wide IPC absence, and the older note must not be back-cited to
S053. This is a use-limit, not a row defect.

`[OBS]` S053 anchors the tagged upstream `.scd`; the installed page
`/usr/share/man/man5/waybar-custom.5.gz` is rendered roff dated
`2026-08-31` (decompressed sha256 `915dcb4c9118f0df53cfefc888b3b457a44127b5926619683ea27e9c6abed88e`).
Different artifact form, so no installed-man equivalence may be claimed
from S053 — the same boundary S050 states for tagged source vs installed
binary. The row's scope text does not overclaim.

`[OBS]` S055's own-work scope is distinct from the neighbouring rows:
S014 (gate script), S044 (gate maintenance rules), S001 (method lesson),
S015 (drift protocol). No other row records a closure/spotcheck lesson, so
this is new ground, not a duplicate.

## 5. Anchor adequacy — verified against fetched bytes

`[OBS]` Digests match the rows exactly:
`man/waybar-custom.5.scd` 6656 B `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82`;
`src/modules/custom.cpp` 8746 B `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f`.

- S053 line map: `DESCRIPTION` `:6`, `CONFIGURATION` `:11`, `RETURN-TYPE`
  `:148`, `FORMAT REPLACEMENTS` `:168`; keys `exec` `:15`, `return-type`
  `:33`, `interval` `:37`, `restart-interval` `:45`, `signal` `:52`; the
  loop-if-unset scheduling caveat `:42-43`; JSON form `:150-166` (class
  array `:157`), raw form `:163`, format tokens `{text}` `:170`,
  `{percentage}` `:172`, `{icon}` `:174`.
  Gap: the anchor names `interval`/`signal` but omits `restart-interval`
  (`:45-50`) although scope claims a "scheduling contract" and the wave
  brief requires the restart behavior. Recommend adding `restart-interval`
  and a range such as `:6-56, :148-174`.
- S054 line map: `Custom::update` `:162-220`; empty-buffer/nonzero-exit
  hide `:164-167`; `hide-empty-text` hide `:178-179`; `set_markup` `:181`;
  tooltip branches `:182-193`; class churn `:197-205`; `show` `:207`;
  `parseOutputRaw` `:222`; `parseOutputJson` `:257-290`. The scope's "hide
  conditions" is genuinely anchored; adding `:162-207, :222-290` makes it
  falsifiable in the row itself.
- S055 line map: `## Gate and correction evidence` `:131`, R15-V1 `:254`,
  R15-V2 `:268`; the file exists at baseline (`git cat-file -e 32c4fda:…`
  exit 0). Anchor wording "closure at baseline 32c4fda" is ambiguous: the
  lesson's own reviewed revisions are `ea0446f…`, `5f13870…`, `9ebd737…`,
  `745f1a9…` (`:8-9, :42`) and it never names `32c4fda`. Rewrite as "read
  at R16 baseline `32c4fda`; `:131`, `:254-296`", or cite the lesson's own
  commit — not both readings at once.
- Tag pinning: `0.15.0` ref plus raw sha256 matches in-lane practice
  (S046, S051). Git tags are mutable; any re-fetch after a tag rewrite must
  re-anchor per S015, never silently reuse these digests.

## 6. `used-by` and reciprocity — current blocking gap

`[OBS]` S053/S054 `used-by` = `corpus/knowledge/waybar-observation-boundaries-r16.md`,
which is **absent**: `corpus/knowledge/` holds only
`waybar-walker-plane.md` and `waybar-walker-semantics.md`. The contract
census line "mined rows whose used-by paths do not exist — must print
nothing" would therefore emit
`missing: corpus/knowledge/waybar-observation-boundaries-r16.md` twice for
these bytes. QuoteAdmission.md:15 independently reports the same absence;
fix ownership is L1's, not this seat's.

`[OBS]` S055 `used-by` = `corpus/lessons/round-16.md`, which exists and
contains the S055 Gate record.

`[OBS]` The reciprocity that SCORECARD.md:696-699 and `measure.py` require
("reciprocal mined A/B S053/S054") is the S047/S048 and S051/S052 pattern:
both rows `mined`, both `used-by` the same knowledge note (the rows do not
cite each other). That holds only once the note lands. The note must land
at **exactly** that path and be indexed by `corpus/README.md`; renaming it
breaks the join, the README extraction, and the measure.

`[INF]` Row status is truthful relative to the integration commit, not to
the current working tree. If the note cannot land in the same commit, the
rows cannot remain `mined`; but `queued` would fail the C1 reciprocal-mined
check, so the only coherent order is note + rows landing together, with
the census run after both exist.

## 7. Recheck values

`[OBS]` S053/S054 `on-release` is consistent with S046/S047/S048/S050.
S055 introduces a sixth novel event key `on-operator-recovery-decision`
(prior extensions: `on-change`, `on-gate-change`, `on-session-change`,
`on-capture-change`, `on-compositor-release`). The contract allows an ISO
date or cadence and the in-lane precedent permits event keys, so it is not
a shape violation, but it is undefined: no record says what event flips it
or who writes it. Recommend a one-line definition in `round-16.md` § Gate
(trigger: operator L0 recovery decision; effect: re-read R15-V1/V2
status), or `180d` if no such event will be recorded. The source file is a
fixed historical lesson, so a file-change cadence would be vacuous — the
novel key is defensible only if defined as debt-state, not source-state.

## 8. Adjacent grounding defect — S055 lesson quote record

`[OBS]` `corpus/lessons/round-16.md` § Gate reports "Thirteen whitespace
words" for the S055 quote, but the quoted span
"These are explicitly hard-coded in-memory controls, not real pacman
dry-run output" is **11** words, and the source sentence continues
(`:161-163`: "…, an installed-host census, operational installation
prevention or host remediation") without an ellipsis. S053's 13-word count
and S054's one-token quote are exact by the same method. Quote policy is
QuoteAdmission's ownership; recorded here because the row's `teaches`
stands on that Gate record.

## 9. Verdict and limits

- Ids: correctly allocated as reserved; no duplicate row; next unused
  `S056`. Append-only compliance verified against baseline.
- Collisions: no URL or scope duplication. S053/S054 complementary, not
  duplicates of S013 or the round-3 inventory. One cross-document
  id-meaning collision (round-15 `ReviewKeyboard` F10) needs the one-line
  reconciliation in §2. One anchor omission (S053 `restart-interval`) and
  one anchor ambiguity (S055 baseline wording) should be tightened.
- Blocking item for L1: the `used-by` note does not exist yet; the rows
  are `mined` ahead of their cited artifact and the contract census would
  flag both.
- S055's novel recheck key needs a definition, and its Gate quote count is
  wrong (11, not 13).
- This seat changed no shared file, ran no gate/measure/test, installed
  nothing and probed no live surface.

Confidence: high for ids, row shape, URLs, digests and line numbers
(opened and hashed 2026-10-20); medium for whether the note will land
before the integration commit (absent at read time).

Remaining unknowns: the final on-disk filename of the new knowledge note;
whether the installed `waybar 0.15.0-3` manual content equals the tagged
`.scd` (different artifact forms, not compared); whether the operator will
ever record the recovery decision that S055's recheck key names.
