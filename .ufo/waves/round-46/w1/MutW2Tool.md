# MutW2Tool — round-45 w2 falsification: mutation-test tools/mado-monitors.py @ 4d22eeb66c2835af8aaa3fac6ad838fa616aa663

## What was attacked
The round-45 w2 falsification (closure D1: the w2 never ran) — the adequacy of the frozen counter
`quality/counters/c1-r45-monitors-v2.py` (PRED-C1-r45-v2) as the sole detector for the landed tool
`tools/mado-monitors.py` at 4d22eeb66c2835af8aaa3fac6ad838fa616aa663 (sha256 2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609,
byte-identical to the current lane file and to the counter's MODEL_SHA256).

## Method
- 100 anchored single-site mutants (one behavior-bearing token each; full old→new table with per-mutant sha256 in
  `w1/MutW2Tool/mutants.json`), all compile-checked; 1 anchor initially ambiguous (M03) was re-anchored, 100/100 generated.
- Detector = the counter's own code replayed in-process (sanctioned by the tasking): `run_fixture` (bwrap sandbox
  `--ro-bind / / --dev /dev --proc /proc --unshare-pid --unshare-net --die-with-parent`, tmpfs over the lane and its parent,
  fakebin hyprctl/journalctl/wlr-randr/wayland-info marker) over all 81 fixtures (49 of PRED-C1-r45 + 32 v2) × 3 variants
  (seed-45 env A, seed-45 env B, nonce-45 env A), then `--selftest`, the clause-r marker check, and for fixture-survivors
  `run_generated` (150 cases, --nonce 45, judged in-process by the pinned v2 reference `.ufo/waves/round-45/v2/mado-monitors.py`).
- Baseline: pristine passes everything — fixtures 81/81 ×3, selftest ok, marker absent, generated 150/150 → detector sound.
- Cross-check with the REAL counter invocation on scratch clones (`git clone -q --shared --no-checkout` + detach 4d22eeb,
  `rev-parse --show-toplevel` asserted = clone) at `--nonce 45`:
  - pristine: rc=0 `PRED-C1-r45-v2: fixtures=81/81 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=4d22eeb66c2835af8aaa3fac6ad838fa616aa663 seeds=45,45`
  - mutant M01: rc=0 `... verdict=TARGET_MET rev=b2a8acc05b9a375fae87f8b5171f96ba4976e827 seeds=45,45` — the real counter
    scores a mutated tool TARGET_MET (end-to-end coverage-gap proof)
  - mutant M39: rc=1 `... fixtures=80/81 ... verdict=TARGET_MISSED rev=47803750ad94c60d0fd3a8e4f849146e881b49e5 seeds=45,45`
  Receipts: `w1/MutW2Tool/real/{pristine,M01-survivor,M39-killed}.txt`.

## Result
**100 mutants → 68 KILLED, 32 fixture-survivors; 31 survive the ENTIRE counter battery** (81 fixtures × 3 variants +
generated 150/150 + selftest ok + marker absent) — the real counter prints `verdict=TARGET_MET` for those mutated tools
(proven for M01). M44 survives all fixtures but is killed by the generated battery (146/150).

- 6 true equivalents (dead/masked code): M02, M03 (MAX+1-len read-ahead masks the loop bound), M09 (INT_RE {1,9} immaterial —
  any ≥2-digit transform value exceeds 0-7 either way), M15 (match == fullmatch for `monitor[ \t]*=(.*)`), M32 (lower()
  immaterial — case-variant modeline still Unsupported via MODE_RE), M90 (`new_rule`'s `rate: 60.0` is write-only).
- 26 genuine coverage gaps (untested input classes), each with the nearest-target fixture the mutant passes:
  M01/M04 size boundary at exactly 1048576 bytes (`setup-config-too-large`); M07 5-digit dims (`host`); M08 6-digit coords
  (`position`); M10 10-digit addreserved field (`addreserved-stoi-prefix`); M11 10-digit transform value
  (`transform-key-overflow`); M12 `monitorv2{`/`monitorv2=` forms (`monitorv2`); M14 `monitor=` without space (`host`);
  M16 \v\f-padded line ends (`isspace-trim`); M19 `##` in body (`comments`); M20 backslash in body (`variable`);
  M27 bad 5th addreserved field (`addreserved-bad-fields`); M34 `0xH`/`Wx0` modes (`zero-mode-is-preferred`); M41 float
  width/height (`wrong-types`); M43 scale delta exactly 0.0001 (`scale-1.3-as-written`); M45 half-up k boundary
  (`scale-1.3-corrected`); M46 search steps 88-89 (`scale-1.3-corrected`); M48 rule mirror names an output ABSENT from the
  dump — mutant IndexError-crashes where pristine DIFFERs (`mirror-missing`); M51 bare `desc` selector (`desc-empty`);
  M60 zero dims (`scale-clean`); M61 bool transform equal to rule value (`wrong-types`); M78 odd-length argv (`setup-usage`);
  M79 double `--monitors` (`setup-usage`); M82 non-UTF-8 config (`setup-bad-utf8`); M96 trailing empty fields (`ignored-keys`).

Full per-mutant table (site with computed `grep -n` locators, mutation, verdict, killing fixture / nearest fixture):
`w1/MutW2Tool/MutW2Tool-full.md`. Per-mutant first-failure output excerpts: `w1/MutW2Tool/results.json`.

## Findings
1. The counter's fixture+generated battery has real teeth on the tested classes (68/100 killed, several by fixtures alone
   with selftest still passing: M17, M23, M28, M29, M31, M38, M42, M47, M52, M64-M68, M74, M75, M81, M87, M94, M97, M99).
2. But it leaves ≥ 26 behavior classes unobserved; a tool mutated at those sites still scores TARGET_MET end-to-end.
3. Dead/masked code the battery cannot see: `new_rule` rate write-only; INT_RE bound immaterial; read-loop bounds masked by
   read-ahead; `lower()` immaterial; match == fullmatch here.
4. A surviving mutant is a coverage finding, not a defect of the tool: the landed tool's behavior at these sites matches its
   contract; the contract's test battery is what leaves them unobserved. This supports closure D1: the round-45 w2 mutation
   falsification never ran, and the counter it would have exercised has substantial survivor surface.

## Evidence & restoration
- Pristine bytes from `git show 4d22eeb66c2835af8aaa3fac6ad838fa616aa663:tools/mado-monitors.py` → sha256
  2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609; lane `tools/mado-monitors.py` re-verified to the same
  sha256 after the campaign (never written).
- Mutants lived only under /fast/scratch/hyaku/mado-r46/MutW2Tool/ (mutants/, work/, real/ clones); receipts copied to the
  seat dir first; scratch deleted before finish. No lane writes outside `w1/MutW2Tool/` + this Report file.
- No pacman transaction (paused host-wide; none attempted), no tool installs, no host-service or compositor mutation, no
  input injection, no Wayland client of my own; no subagent dispatch; no background jobs (all cells synchronous).
