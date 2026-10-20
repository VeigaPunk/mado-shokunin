author: mado-shokunin (L1 + lane-dispatched L2 advice)

# Round 18 — producer identity, mutant bite, producer status; P3/P5 sourced routes; tripwire frozen replay

Date: 2026-10-20. Baseline `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`;
pre-registration `d3a0000`. Motivation: the admitted round-17 closure
(`round-17-verifier-spotcheck.md` §6, routed R17-V1..V5) and the jj-migration
audit `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMado.md`
(F10, F14) plus `JjTrialMado.md` (`.ufo/state/` not ignored). Wave evidence
under `.ufo/waves/round-18/`; report `.ufo/reports/round-18/mado.md` (fleet).

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M1 | attribution (R17-V1); number-drift (R17-V2) | The six round-17 real-transcript receipts (`.ufo/waves/round-17/evidence/tripwire-r13.txt`..`r16.txt`, `tripwire-anchor-r15.txt`, `tripwire-pacmanlog-join.txt`) carry input digests (`files[].sha256`) but no producer identity: 0 hits for `tool_sha256`/`measured_commit`/`962919ce`/`7a98720e` (w1 `RevR17V1Facts`, `RevR17V2Facts`). The re-cut claimed at `round-17.md:175-176` **did run** (`MadoR17.jsonl` record 539, 15:17:25.987Z, after the P11 fix; w1 `RevengeR17Recut`), but it reproduced identical bytes, so git recorded nothing and no committed byte shows it ran — and `tripwire-pacmanlog-join.txt` is a hand-authored join, never tool output. R17-V2: report line 76 pairs `7a98720e…` (the `f71ccbe` tool) with `30/30`, a count that exists only at `0ab1ccc` (`962919ce…`): replaying `7a98720e` on the 30-case suite gives 28/30. | QUALITY 9 (commit binding) and 13 (committed path) are satisfied by input digests; 23 binds a `measured_commit` only "when the receipt records" one. None names the producer. | QUALITY 24 + `.ufo/waves/round-18/receipt-check.py`: red `MISSING_PROVENANCE` on the six receipts at `d9a5a18`; a stale fixture bound to the `f71ccbe` tool reads `SHA_MISMATCH`. Re-cut receipts with a `RECEIPT … tool_sha256= measured_commit=` first line: `.ufo/waves/round-18/evidence/tripwire-*.txt` (`recut-receipts.sh`). Erratum appended to `round-17.md`. |
| M2 | vacuous (R17-V5) | `round-17.md:156-158`: rubric-V tightenings "shown to bite" only in a seat `/tmp` lab; no committed mutant receipt at `d9a5a18`. | QUALITY 13 (commit evidence) — it rejects the `/tmp` location but does not say what a bite is. | QUALITY 25 + `.ufo/waves/round-18/measure-mutants.py` → `evidence/measure-mutants.json`: for each of six tightenings a committed-in-clone mutant that the loose instrument (`f52f43f`, `a280b3ab…`) credits and the tight one (`d9a5a18`, `de4c422b…`) rejects; 6/6 bite (M2 at entry level, M6 as a refusal), `no_bite []`. |
| M3 | vacuous (latent, outside audit) | `tools/mado-verify.sh:3406` at `d9a5a18`: `blob=$(tmo git … show … \| sha256sum \| cut …)` drops git's status; a failed read hashes empty input (`e3b0c442…`) and the row reads FAIL "local edit"; the `-z "$blob"` UNKNOWN arm is unreachable. The selftest git stub exits 0 for every verb (F14), so no scenario could see it. Never fired on this host (the checkout is plain git). | none (QUALITY 3 states the principle; nothing checks a producer status) | Gate: `pipefail` inside the substitution, `grc≠0` → UNKNOWN `rc=N`; stub rc knobs; scenarios OM9/OM10 (+17 assertions). Red before: `evidence/gate-rc-redbefore.txt` §1 (old gate, stub rc 128 → FAIL with `e3b0c44298fc…`). PIN re-cut 10/10 KILLED (`evidence/regression-recut.txt`). QUALITY 26. Census screen `pipe-rc-census.py` (9 sites at `d9a5a18`, one verdict-bearing). |
| M4 | stale-premise (this round, L1) | The wave-1 GateRcFix item (`.ufo/waves/round-18/gen_w1.py`, item text) told the seat to capture `${PIPESTATUS[0]}` "or read the blob to a variable first", copying `JjAuditMado.md:350/478` untested. Both are wrong: after `x=$(…)` `PIPESTATUS[0]` is the assignment's status (measured 0 while git exited 128; w1 `CriticC1`, `RevGateRcFixPlan`, `RevengePinRecut`, `SimplifyGateStub`), and hashing a variable via `printf` is byte-lossy on trailing newlines. | none — an outside fix recipe was passed on as a contract | The seat chose `set -o pipefail` inside the substitution; OM9/OM10 would fail under the literal recipe. Criterion 26 records the trap. Rule kept in this lesson: a fix recipe from an audit is a hypothesis until a failing stub shows it bites. |
| M5 | landing (seats) | Three seats first wrote their reports at the fleet root (`RevR17V1Facts`, `RevJjTrialFindings`, `SrcOmarchyBackground`) and moved them; seat `JjDisposition` ran one `git status --porcelain` in the lane; seat `SrcOmarchyBackground` ran one read-only `git cat-file` inside the omarchy checkout; seat `FrozenProvenanceCheck` deleted a sibling's `__pycache__`. All self-disclosed in their reports. | wave context (prompt-level only) | Misroot sweep before the report (fleet `git status --porcelain`); no lane byte changed by these acts (`git status` refreshes only the index stat cache). Carried, not fixed: fences are still prompt-level. |
| M6 | vacuous (R17-V3, carried) | Rubric V (`.ufo/waves/round-17/measure.py`) credits a row whose bytes were never fetched: w1 `RevPreReg18` and `CriticC2` reached 6/6 and 5/6 in `/tmp` clones with invented rows and notes. | none in the instrument | Not closed by the counter (unchanged by declaration). Every round-18 credited web row has a committed `mado-fetch-receipt-v1` line, with independent seats agreeing on the digest where more than one fetched it; `fetch-verify.py` re-hashes bodies and joins rows. A non-author can re-fetch the tag-pinned URL and compare sha256. |

## Gate

Candidates considered: tag-pinned upstream walker v2.17.2 / elephant v2.22.1 /
omarchy v3.8.4 / swaybg v1.2.2 raw files; the walker GitBook docs site
(unversioned); the Omarchy 3 manual (unversioned, legacy); docs.rs xdg
"latest"; GitHub tree HTML pages; the walker tag tarball; host file bytes;
third-party theme blogs and AUR pages (w1 `SrcThemeAlternates`).

Admit: tag-pinned raw files whose receipts agree across seats; host file
bytes as host rows. Reject or leave unrowed: HTML pages as sole support
(per-fetch tokens make the digest irreproducible), unversioned docs sites as
version-specific support, third-party blogs. A tag's source never proves the
host binary; `/var/log/pacman.log` upgrade lines are log lines, not running
binaries.

New rows S072–S095 (all opened 2026-10-20; receipts under
`.ufo/waves/round-18/fetch/<seat>/receipts.jsonl`; located quotes recorded
below after the wave-2 re-open). Existing rows: status/recheck/used-by
changes old→new: none.
