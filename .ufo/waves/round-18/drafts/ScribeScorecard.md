## Round 18 — committed results and bounded author verdicts

Measured at `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98` (baseline) and
`4c103b55b1ea5c3c555884afe3eb69b5189701b7` (integration). Receipts under
`.ufo/waves/round-18/evidence/`. C1 and C2 use the unchanged instrument
`python3 .ufo/waves/round-17/measure.py REV` (tool sha256 `de4c422b…`); C3 uses
`tools/mado-tripwire.py` (`962919ce…` at baseline, `c87a31ef…` at integration).

| Claim / axis | Before → after | Command / commit | Verdict / evidence |
|---|---|---|---|
| C1 calibration, literal lesson-citation fraction | 15/23 = 6.5217 (d9a5a18) → 18/26 = 6.9231 (4c103b55), +0.4014 | `python3 .ufo/waves/round-17/measure.py d9a5a18…`; `… 4c103b55…` (`evidence/measure-before.json.txt`, `measure-after.json.txt`) | met the declared target ≥18/26 exactly. Criteria 24 (producer identity), 25 (mutant bite) and 26 (producer status through pipes) added with lesson rows M1-M6. Bounded: the literal counter credits citation text, not the fix's effect. QUALITY 25 bite evidence: `evidence/measure-mutants.json`, 6 of 6 tightenings bite, `no_bite []`, baselines agree (mutants were run in `/tmp` clones and recorded). |
| C2 coverage, rubric V (same instrument) | 4/6 = 6.6667 (d9a5a18) → 6/6 = 10.0 (4c103b55) | same command at both revisions | P3 via `corpus/knowledge/walker-route-r18.md` (S072-S091) and P5 via `corpus/knowledge/theme-route-r18.md` (S092-S095); S090, S091, S095 are host rows (file bytes and `/var/log/pacman.log`, not fetched). Fetch receipts `mado-fetch-receipt-v1`: 303 lines at HTTP 200 and 5 at HTTP 404 across the fetch directories. Every fetched URL behind a credited row S072-S089 and S092-S094 has at least two HTTP-200 receipt lines with a matching sha256 prefix, from different seats. The five 404 lines are not cited by any row. Bounded: the counter still cannot tell a fetched row from an invented one (M6 is carried, not closed by the counter); 15 fetch directories (14 `ReopenS*` and `MadoR18.RevengeTarballRepro`) hold no `receipts.jsonl`; host binaries and runtime behaviour stay `[UNK]`. |
| C3 operability, frozen replay of committed incident lines | absent → present. Baseline `--frozen` is a usage error (exit 2); integration: `frozen_match` exit 0, tampered copy `snapshot_tampered` exit 2 | `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen` (`evidence/tripwire-frozen-match.txt`); `python3 -I <d9a5a18 tool> --frozen …` (`evidence/tripwire-frozen-before.txt`); tampered copy (`evidence/tripwire-frozen-tampered.txt`) | capability acquired; frozen selftest 17/17 (`evidence/harm-tripwire-round-18-frozen.txt`). Registry row `mado-tripwire-frozen` moves to `gate` in `SKILL.md`; the `--scan` probe row is unchanged. Bounded: replays five committed input files (rounds 13-15) and pins their verdict; it does not detect new misses, and the round-17 adversarial misses remain pinned as known limits. |

### Harm watch (integration `4c103b55`)

`evidence/harm-watch-summary.txt`: `HARM_WATCH: PASS`, 10 of 10 commands `OK`,
pins in `evidence/harm-watch-pins.txt`. Hermetic gate selftest 389/389 assertions
(`harm-gate-selftest.txt`, tool sha `c9fb0cef…`, up from 372/372 at round 17
because of the F10/F14 fix); action-plan classifier 52/52; tripwire round-17
suites core 9/9, compound 16/16, hardening 33/33, w2-regressions 30/30 and the
new frozen 17/17; U coverage 7/7, score 10.0 (`harm-measure-u.txt`); navigation
34/34 indexed, coverage 10.0000 (`harm-nav-fleet-round-1.txt`); census validate
exit 0 with three historical W04 duplicate-URL notes (`harm-census-validate.txt`).
Freshness: file-plane 29/29 was not re-measured this round. Operability carries
R15-V1 (operator-owned, host state `[UNK]`). No axis was harmed by lane action.

### Capabilities (round 18)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| digest-pinned frozen replay of the tripwire | Re-run the classifier on five committed input files, fail closed on a changed byte (`snapshot_tampered`, exit 2), and compare the verdict and (file, line, class, rule) multiset with `expected.json` (`frozen_match`, exit 0) | `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen`; `evidence/tripwire-frozen-match.txt`, `tripwire-frozen-tampered.txt`, `harm-tripwire-round-18-frozen.txt` (17/17) | 18 |

### Planned (round 19; intent only)

1. Tripwire misses: apply or reject the three drafts that were not applied this
   round, `drafts/TwMissBashCVar.patch`, `drafts/TwMissHelperFn.patch` and
   `drafts/TwInstallerChannels.patch` (`drafts/tripwire/r18-bashcvar`,
   `r18-helperfn`, `r18-installers` hold their fixtures).
2. Freshness: re-anchor the present-tense pins moved by the 2026-10-20 `-Syu`
   (walker 2.17.2, hyprland 0.56.2-4) by file bytes and `/var/log/pacman.log`
   lines only.
3. Remaining adversarial misses of the transcript tripwire (round-17 pins
   4/26 known limits) that recur in real transcripts, or record them as
   permanent limits.
4. F6 tree-compare: the colocated-tree arms at `tools/mado-verify.sh:3382` and
   `:3391` resolve `HEAD`, which can be an empty working-copy commit after
   `jj new`; resolve the tip with `refs/heads/master` instead, then test it
   (`JjAuditMado.md` F6, lines 190 and 348-349).
