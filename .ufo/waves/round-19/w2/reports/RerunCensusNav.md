# RerunCensusNav — holds

Seat: `MadoR19.RerunCensusNav` (leaf, attack only). Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`; integrated tip under attack
`01b80946d92b26370d3012a7da655d00dd135154`. I wrote only this report and
`/tmp` scratch; no lane file, bookmark, git or jj state changed.

## What I attacked

`SCORECARD.md:1142-1144` (Round 19 committed results, harm watch) claims:

> U 7/7, navigation 34/34, census exit 0 (W04 now also names S097/S094 sharing
> a URL; S094 is rejected). No owned axis harmed by lane action.
> Sources 95 → 98 (A 88 → 91; mined 80 → 81; rejected 7 → 9).

and the round-19 declared freshness/coverage block's instrument
(`python3 .ufo/waves/round-16/measure.py <rev>`) plus the fleet-round-1
navigation counting fence. Attack plan: (1) re-run every command verbatim at
the tip and at the named before-revisions; (2) cross-check the three
independent counters against each other; (3) mutate a `/tmp` clone of the lane
to prove each counter is red on a one-field defect — if a mutation cannot turn
it red, the counter is vacuous and the claim is false.

## Commands and verbatim outputs

### 1. Census validate (assignment: expect exit 0, W04 incl. S097)

```
$ cd /home/vgpnk/Projects/shokunin
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
EXIT=0
```

Matches the expectation: exit 0, four warnings, S097 present. Same output and
exit 0 from a pristine `/tmp` clone of `01b80946` (`--file <clone>/corpus/SOURCES.md`),
so this is not an artifact of the live worktree.

S094/S097 pairing (the W04 line itself names only S097):

```
$ grep -n '^| S094 \|^| S097 ' mado-shokunin/corpus/SOURCES.md | cut -c1-80
106:| S094 | omarchy v3.8.4 matte-black theme payload — https://raw.githubuser
109:| S097 | omarchy v3.8.4 matte-black theme payload (supersedes S094) — http
```

- `corpus/SOURCES.md:106` S094 status `rejected`; `:109` S097 status `mined`
  (awk `$9`).
- Normalized URL equality, computed independently with the manual's own
  normalization rules (strip scheme, lowercase host, strip trailing `/` and
  `#fragment`): both rows extract
  `raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml`.
- An independent duplicate sweep over all 98 rows found exactly three duplicate
  URL groups — `wayland.freedesktop.org/extras.html` (S006,S042),
  `wiki.hypr.land/Configuring/Basics/Window-Rules` (S017,S030,S045),
  the omarchy raw URL (S094,S097) — and the tool emitted one W04 per later
  member (`S042`, `S030`, `S045`, `S097`): complete, no missed group.

### 2. CORPUS.md manual census (frozen v1 block), run from the lane

```
== rows ==
98
== malformed ==
0
== tier ==
A=91 B=1 C=6
== status ==
mined=81 queued=8 rejected=9
== dup ids ==
== enum ==
== used-by existence ==
== done ==
```

(`used-by existence` prints nothing, i.e. every mined row's path resolves.
Leading-space row check: `0` rows with 1–3 leading spaces, `0` with ≥4, so the
frozen column-zero commands and the maintained 0–3-space parser agree.)

Baseline `9c54c56:corpus/SOURCES.md`, same commands:

```
rows=95  tier.A=88 tier.B=1 tier.C=6  status.mined=80 status.queued=8 status.rejected=7  malformed_base=0
```

Exactly the declared `95 → 98 (A 88 → 91; mined 80 → 81; rejected 7 → 9)`.
Cross-check: `sources-census.sh census --root … mado` emits the identical
`rows 98 / tier.A 91 / tier.B 1 / tier.C 6 / status.mined 81 / status.queued 8 /
status.rejected 9`, and `measure.py`'s `source_registry` reports the same
`rows 98, tiers {A:91,B:1,C:6}, statuses {mined:81,queued:8,rejected:9}`.

### 3. Fleet-round-1 navigation counting fence, verbatim from `SCORECARD.md:70-89`

```
$ REV=<rev> bash /tmp/navblock.sh          # fence extracted byte-exact, lines 70-89
baseline bb08dd57: revision=bb08dd57f4b48bfb001a178e57b9c25e7040447f indexed=8/22 missing=14 dangling=0 duplicates=0 coverage=3.6364/10   (EXIT=1)
historical 7cd7f331: revision=7cd7f331ae151845ebff7bd100c1073ebad49351 indexed=22/22 missing=0 dangling=0 duplicates=0 coverage=10.0000/10 (EXIT=0)
tip 01b80946: revision=01b80946d92b26370d3012a7da655d00dd135154 indexed=34/34 missing=0 dangling=0 duplicates=0 coverage=10.0000/10 (EXIT=0)
```

The baseline reproduces the scorecard's recorded `8/22, missing 14, dangling 0,
duplicates 0, exit 1` exactly; the tip reproduces `navigation 34/34`.

### 4. `measure.py` at the tip

```
$ python3 .ufo/waves/round-16/measure.py 01b80946d92b26370d3012a7da655d00dd135154
… "revision": "01b80946…", "revision_sha": "01b80946…"
… "source_registry": {"rows": 98, "tiers": {"A":91,"B":1,"C":6}, "statuses": {"mined":81,"queued":8,"rejected":9}}
… "coverage": {"items": ["U1"…"U7"], "count": 7, "score": 10.0, …}
… "navigation": {"notes": 34, "indexed": 34, "missing": [], "extra": [], "duplicates": []}
… "calibration": {"criteria_total": 28, "lesson_grounded": 20, "fraction": 0.7143, "score": 7.1429}
… "measure_inputs": {"gate_sha256": "1036d1004e63d80377faa4f905fd8dc1897eb29b64496cbfef647b47cec4f2af", "gate_executed": false}
EXIT=0
```

At `9c54c56` the same probe reports `calibration 18/26 = 0.6923` and
`gate_sha c9fb0cef3e08…`, proving the revision binding is real (gate bytes move
with the rev); U stays 7 and navigation 34/34 there because no note was added in
round 19.

The seven joins: U1 window-rule-effects-getprop, U2 hyprland-config-era-r12,
U3 xdg-portal-routing-r12, U4 wayland-protocol-boundaries-r13 (phase/advert/
unexercised all true), U5 output-colour-boundaries-r14 (facets + reserved
S047/S048 + inverse), U6 input-debugging-boundaries-r15 (S051/S052), U7
waybar-observation-boundaries-r16 (S053/S054). I re-read U7 from the committed
bytes: `covers: U7` exactly once, `## Producer contract` / `## Renderer
boundary` / `## Safe observation` at :13/:35/:58, `## Unexercised rendering` at
:77 with `[UNK]` at :79-80; S053/S054 are `mined`, tier A, and their `used-by`
cell is `corpus/knowledge/waybar-observation-boundaries-r16.md`; no third mined
row names the note.

## Mutation matrix (all in `/tmp/mado-clone`, a `--no-hardlinks` clone of the lane; lane untouched)

| Counter | Mutation | Result |
|---|---|---|
| nav fence | delete the `waybar-observation-boundaries-r16.md` index row | `indexed=33/34 missing=1`, exit 1 |
| nav fence | duplicate that row | `duplicates=1`, exit 1 |
| nav fence | add row `knowledge/ghost-note.md` | `dangling=1`, exit 1 |
| measure.py | S053 `mined`→`queued` | U 7→6, U7 candidate `reserved S053 false` |
| measure.py | S053 `used-by`→`—` (still mined) | U 7→6 |
| measure.py | S053 tier A→C | U 7→6 |
| measure.py | S054 `mined`→`rejected` | U 7→6 |
| measure.py | second `covers: U7` line in the note | U 7→6 (zero U7 candidates) |
| measure.py | S055 mined and its `used-by` names the U7 note (note does not cite S055) | U 7→6, `inverse false` |
| measure.py | S051 queued / S047 rejected / S005 queued | U 7→6 with U6 / U5 / U4 respectively missing |
| census validate | S096 status→`watch` | `E07 S096 status=watch`, exit 1 |
| census validate | S053 used-by→`corpus/knowledge/nope.md` | `E11 S053 missing used-by …`, exit 1 |
| census validate | S097 drop one cell | `E01 S097 fields=10`, exit 1 |
| census validate | duplicate id S098→S097 | `E03 S097 duplicate id`, exit 1 |
| census validate | clean symlinked copy (SKILL.md/tools symlinked, corpus copied) | identical four W04 + `ok`, exit 0 |

`bash scripts/sources-census.sh selftest` also ends `selftest ok` (exit 0) with
its mutants `killed`, including `W04-scope-sensitive-mutant`,
`W04-does-not-fail-validation`, `E04-rejected-pair-exemption-mutant`,
`gated-failure-is-error-not-ok`.

## Verdict

Every substantive clause holds: census validate exit 0 with the four W04 and
S097; S094 rejected and URL-identical to S097; manual census 98 rows / 0
malformed / A91 B1 C6 / mined81 queued8 rejected9; nav 34/34 exit 0 at the tip
and 8/22 exit 1 at the named baseline; measure U 7/7 with a revision-bound
gate hash. Each counter is demonstrably falsifiable — the one-field mutants
above each turn it red.

The only overreach is verbal: `SCORECARD.md:1142-1143` says the W04 "names
S097/S094"; the tool's line names only S097 (`sources-census.sh:645` prints the
later row's id). The pairing is established by the rows at
`corpus/SOURCES.md:106,109`, not by the warning text. Not a false measurement.

## Limits

- `sources-census.sh` is worktree-bound, not revision-bound: it reads
  `<dir>/corpus/SOURCES.md` from disk (`sources-census.sh:708-717`) and never
  `git show`. The claim was therefore checked twice — worktree and pristine
  clone — and the worktree copy is byte-identical to tip
  (`corpus/SOURCES.md` sha256 `3a85abc5ac0bd03f67696eaf91d48824951b320d6729f8930b8670ab25159b31`,
  equal to `git show 01b80946:corpus/SOURCES.md | sha256sum`). If this file ever
  diverges from tip, the command cannot prove the committed claim.
- The navigation fence's denominator is non-recursive (`git ls-tree --name-only`)
  while `measure.py:208,316` uses `ls-tree -r` and collapses to basenames. Both
  report 34/34 today because `corpus/knowledge` has no subdirectories (checked:
  zero `tree` entries). Latent divergence, not a current falsehood.
- The fleet-round-1 rubric scores index-row presence, not link truth or note
  freshness; 10.0000 is saturation on the 34-note denominator (the scorecard
  says this itself).
- `measure.py` prints a `SyntaxWarning` for the invalid escape `\.` at line 41
  on stderr; stdout JSON is valid and exit 0.
- Live worktree during this run had sibling wave-2 edits (`git status`:
  SCORECARD, QUALITY, `tools/mado-verify.sh`, 7 `corpus/knowledge` notes, three
  `.ufo` files). Those are outside my read set. `corpus/SOURCES.md` was
  unmodified throughout (digest above). `corpus/README.md` was byte-identical
  to tip when measured, then a sibling added four prose lines at
  `corpus/README.md:134-150` (S096 word order, hyprtoolkit/scanner moves); the
  index rows are untouched — the worktree still has 34 index rows beginning
  with the knowledge/ path cell —
  and both navigation counters read committed bytes, so no number here moves.
- No claim here covers the truth of a note's content, live walker behaviour,
  C2 freshness or C3 tripwire recall; those are other seats' items.

## Installs

None.
