## 2026-10-20 — round 19: walker pin currency, tripwire recall, criteria 27+

Draft skeleton (L1 finalizes; `⟨after⟩` = value L1 fills from the after receipt; `⟨…⟩` = unresolved placeholder). Scores are 10 × ratio (the before receipts' convention).

Trigger: admitted round-18 closure (`corpus/lessons/round-18-verifier-spotcheck.md`, routed R18-V1..V4 and carried items) at baseline `9c54c56` (`refs/heads/master` at round start); claims pre-registered at `17661e0` (SCORECARD tail, "Round 19 — declared claims"). Baseline receipts: `.ufo/waves/round-19/evidence/{measure-before.json,fresh-pins-before,tw-recall-before,census-before}.txt`. Host pause carried: no package, service, compositor, input or screenshot operation; host files read as file bytes only. R15-V1 remains operator-owned, state `[UNK]`.

Motivating evidence (round-18 closure §6, re-shown at closure):
- R18-V1 (S094 anchor): the secondary anchor cites per-fetch GitHub HTML digests; two fetches gave `1a3ddca5…` and `4d001dc8…`, so `fetch-verify` exits 1 (4 `CONFLICT`s). Lesson M7. Fix: superseding row S097.
- R18-V2 (criterion 26 red-before): rests on `evidence/gate-rc-redbefore.txt`, which has no producer header, plus the w3 swap result 383/389 in `w3/reports/W3CriticC1Final.md`. Fix: header-bound receipt of the swapped-block run.
- R18-V3 (stale walker pins): eleven owned files still state `2.17.0` with no in-file pointer (13 files contain `2.17.0`; 2 already current). Host moved to walker 2.17.2 at `/var/log/pacman.log:2929` (`upgraded walker (2.17.0-1 -> 2.17.2-1)`, 09:16:46 -0300). Fix: S096 host walker bytes, dated in-file pointers or re-pins.
- R18-V4 (S084 durability): cites the unpinned docs.rs `latest` alias. Fix: S098 xdg crate tarball row replacing S084 as support.
- Carried: frozen F1/F2 (blank-line pin reads; `link/.` bypasses the symlinked-dir check); `measure-mutants.py` default `--out` into the lane; jj audit F6/F9/F16/F17 (`.ufo/waves/hyaku/jj-w1/reports/JjAuditMado.md`); tripwire drafts `TwMissBashCVar.patch` (sha256 `6911e949…`), `TwMissHelperFn.patch` (`6cf9ca69…`), `TwInstallerChannels.patch` (`1acb8549…`), diffs against the `d9a5a18` tool, fixtures `.ufo/waves/round-18/drafts/tripwire/r18-*`.

Claims (declared at `17661e0`; before values at `9c54c56`):

C1 calibration: lesson-cited append-only QUALITY criteria 27+, each with a runnable check shown red on a real `9c54c56` artifact (lessons `## Mistakes` of `round-19.md`, R18-V1..V4). Before: `python3 .ufo/waves/round-17/measure.py 9c54c56` → c1 `lesson_cited` 18 of `criteria` 26 = **6.9231** (instrument `de4c422b…`). After: ⟨after⟩ of ⟨after⟩ = ⟨after⟩; declared target ≥ 21/29.

C2 freshness (sourced): walker version-pin currency, `python3 -I .ufo/waves/round-19/fresh-pins.py REV`. Each of the 13 owned files containing `2.17.0` gains a line holding `2.17.2` plus an `S###` row token (in-file dated pointer or re-pinned value); the gate's `live.walker.version` pin moves with its selftest. Before: **2/13 = 1.5385** (tool `a094be01…`; current: `corpus/README.md:44`, `corpus/knowledge/walker-route-r18.md:1`). After: ⟨after⟩/13 = ⟨after⟩; declared target 13/13. Rows reserved: S096 (host walker binary + `pacman.log:2929`, file bytes only, live `walker --version` not run), S097 (supersedes S094), S098 (supersedes S084 as support).

C3 operability: tripwire recall on the 6 real incident lines, `python3 -I .ufo/waves/round-19/tw-recall.py REV`. Apply or reject the three round-18 drafts rebased on the current tool (`c1ae45a7…`), every existing suite still all-pass; re-pin a round-19 frozen baseline at the landed classifier. Before: **3/6 = 5.0000** (tool `c1ae45a7…`). After: ⟨after⟩/6 = ⟨after⟩; declared target 6/6. Drafts: TwMissBashCVar ⟨apply|reject⟩, TwMissHelperFn ⟨apply|reject⟩, TwInstallerChannels ⟨apply|reject⟩. Frozen baseline: round-18 baseline reads ⟨after⟩ (declared: `frozen_verdict_mismatch`); round-19 baseline digest ⟨after⟩.

Non-claim repairs (harm-watched, not scored): frozen F1/F2; `measure-mutants.py` `--out` default; gate F6 (`describe`/`rev-parse` on the tip, not `HEAD`), F9 (`rev-parse --git-dir` precondition), F16 (landedness check); PROVINCE path-root line for `~/.config/omarchy/**`. Outcome: ⟨after⟩.

Harm watch (before values as measured at `9c54c56`; ⟨after⟩ at the final commit):
- rubric V (P1–P6) 6/6 (`measure-before` c2 count 6, score 10.0): before 6/6, after ⟨after⟩.
- U-routes 7/7 (`u_routes` 7, seen U1–U7): before 7/7, after ⟨after⟩.
- census `scripts/sources-census.sh validate --root … mado`: before exit 0, historical W04 duplicates S030/S042/S045 only; after ⟨after⟩.
- gate selftest, classifier 52/52, tripwire suites (9/9, 16/16, 33/33, 30/30), frozen 31/31, failsafe 1/1, navigation: not re-measured in the before receipts; the round-18 closure reported them at `b7148a1` (gate 389/389). Before at `9c54c56`: ⟨UNK — L1 to take or cite⟩; after: ⟨after⟩.

Waves: w1 ⟨n⟩ seats (dead: ⟨after⟩), w2 ⟨n⟩ seats (dead: ⟨after⟩). Wave corrections: ⟨after⟩.

Host: no pacman, systemctl, journalctl or live gate run by L1; no installation or update evidenced. Installs: ⟨after⟩.

Verdicts: calibration ⟨after⟩; freshness ⟨after⟩; operability ⟨after⟩; coverage and adjacency ⟨after⟩. Admission not asserted.
