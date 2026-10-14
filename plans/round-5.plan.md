# WWKD plan — mado round 5 (ufo-round-plan-v1)

Post-verifier frame: round 4 closes SHONEN boxes 3/4 with named non-author
verifier seats (`plans/round-4.plan.md`) and lands the idle/lock plane
(`corpus/knowledge/idle-lock-plane.md`, MADO-R4-2, 355 L by `wc -l`) plus the
reproduction-package section (SKILL.md 424 L in the round-4 tree, uncommitted
at HEAD `f9f58c0`; design-time reads 2026-10-14 16:20 UTC). Round 5 spends
the cleared budget on the lane's oldest named ceiling, not on re-litigating
the boxes; any verifier non-reproduction is applied first as errata
(companion below).

Axis set: operability (move), freshness (fold-in only), depth (deferred).
Axis move: operability — a committed, self-testing config-plane census gate
(`corpus/scripts/`).

Claim: the scratch reproduction packages (`/tmp/mado-r3-2-probe/`,
`/tmp/mado-r4-1-probe/repro-r3.sh`; SKILL.md "Reproduction package") can
become one committed read-only gate — `corpus/scripts/verify-plane.sh` plus
its `expected.tsv` and `check-getoptions.py` — that reproduces the lane's
headline censuses as verdicts:
  (a) 57/57 `getoption` re-check, 0 mismatch (census 46 agreement + 6
      agreement* + 4 live-default + 1 extra — MADO-R3-2 Appendix A);
  (b) 192/192 bind reconciliation + flag counters d190/e14/l26/m2/r1
      (MADO-R2-2; re-measured green in R3-2);
  (c) sha256 drift pins (hyprland.conf `4f52854a3c14…`; the 37-check chain
      of MADO-R3-2 §0);
  (d) omarchy two-pin drift row (`omarchy version` 3.8.3 vs checkout tag
      v3.8.4 — MADO-R3-1 §8.4) — the version-drift watch folded in as the
      pin class, not a second axis move.
Exit-code map declared in the script header (0 pass / 1 census fail /
2 unverifiable-env / 3 pin-drift only); `--selftest` feeds a tampered
expectation and must exit non-zero naming that row (exit+expected-id depth;
fleet gate standard — PROTOCOL-APPENDIX.md §Gate standard; cf. kengaku
`grader.py:5522` `run_selftest()`, kumitate `scripts/round-gate.mjs
--selftest`). When red-detection is proven and a full run is green on this
host, the round-1 ceiling — "0 committed verdict gates", `find corpus -name
'*.sh' | wc -l` → 0 (re-measured 2026-10-14 16:20 UTC) — is retired.

Gate runtime contract: read verbs only (R2-1 §0 whitelist + `layers`), no
`dispatch`/`keyword`/service start-stop, no network, substrate sha256
before/after equal, scratch outside the substrate, secrets shape-only.

Anti-claim: missing tool or read verb at gate time (no live session, no
`jq`/`python3`) → the gate prints `unverifiable` (code 2) and never passes;
the round records the move `unproved`, not claimed. Reaped scratch → rebuild
the expected set from MADO-R3-2 Appendix A (durable) + SKILL.md's recipe,
and record that the committed gate is a rebuild, not a copy.

Deferred (kept as rejections, trigger named):
- walker deep-module semantics — depth already moved rounds 2–3 (R3-1 §6.2
  key-by-key, §6.7 launch paths; SCORECARD depth rows); un-defer trigger: a
  green gate run, then round 6's depth candidate.
- omarchy skill version-drift watch standalone — covered by (d) above; if it
  does not fit the gate's read-only runtime, it defers named to round 6.

Companion (non-move, before pins freeze): pending errata at design time
(2026-10-14 16:20 UTC) — `config-health-report-r3.md:58` still says "6× S3"
while the register holds 7 (LOG round-3 obs (a)); R3-1 §8's 7 divergence
candidates on `waybar-walker-plane.md` still unapplied (no R3-E block;
`grep` → 0). The SKILL `arrouillard` typo is already fixed in the round-4
tree (`grep -c arrouillard SKILL.md` → 0).

SHONEN: no new box claims; the gate is operability evidence only.

Measure: `corpus/scripts/verify-plane.sh` exists (`wc -l`); `--selftest` red
on the tampered fixture with the injected row named; a full run green on this
host with transcript path recorded; SCORECARD.md operability row before→after
with the counting commands; LOG.md round-5 entry. Move counted only when the
full run is green on this host.