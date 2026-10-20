# CriticHonesty — round 18 honesty plan (mado)

Seat: `MadoR18.CriticHonesty` (critic, leaf). Review only; no judgment, edit or admission.
Inputs: SCORECARD.md:931-985 (d3a0000), round-17-verifier-spotcheck.md §2-6, lessons/round-17.md:140-176,
JjAuditMado.md §3-7, the drafts in `.ufo/waves/round-18/drafts/` as of 15:41Z.
Host facts come from file reads only: `/var/log/pacman.log`, `/proc/uptime`, and `~/.local/share/omarchy/.git` bytes.
No git command touched that checkout, and no package, service or compositor command ran.
No tool installs or updates.

## Observed facts this review relies on (2026-10-20T15:41:27Z)

| fact | evidence |
|---|---|
| pacman.log has had no transaction since 09:39 | `wc -l` 3160; sha256 `f34d34e72702c94e…5741e76`; mtime `2026-10-20 09:39:21 -0300`; last line `:3160` is a 09:39:21 hook line. Round 18 pre-registered at 12:34:53 -0300 (d3a0000). |
| host rebooted after the 09:15 `-Syu` | `/proc/uptime` 9870.55 s at 12:41:27 -0300 → boot ≈ 09:57 -0300. `uname` 7.2.11-arch1-1 matches the linux upgrade at pacman.log:2855. mkinitcpio 41.1→42.2 is at `:2539` (spot-check §6). |
| walker / elephant versions are log events | `:2929` `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`; `:3095` `upgraded elephant (2.21.0-1 -> 2.22.1-1)`; `:3142-3147` removed the elephant-*-debug 2.22.1-1 packages |
| SKILL.md still pins walker 2.17.0 | SKILL.md:22-23 "walker 2.17.0 … re-verified `hyprctl version`" |
| omarchy checkout identity (file bytes) | `.git/HEAD` = `ref: refs/heads/master`. packed-refs:2 has master = `8fcc9d60…`, and :508 has `refs/tags/v3.8.4` = `8fcc9d60…` (lightweight, no peel line). :321 has origin/master = `8fcc9d60…`. :509/:512 has `refs/tags/v4.0.0` `f0020448…` ^`13f18b2c…` (= `origin/v4-0-1` :433). |
| non-lane actor touched the checkout today | packed-refs mtime 09:14:47 -0300 (43 s before the `-Syu` at :2462). FETCH_HEAD and ORIG_HEAD mtime 09:49:22 -0300. FETCH_HEAD = `8fcc9d60…  branch 'master' of .`; ORIG_HEAD = `8fcc9d60…` (HEAD unmoved). `.git/index` mtime 2026-10-14. |
| `.gitignore` edit is uncommitted and preventive | `git show d3a0000:.gitignore` → only `.ufo/interactive-sessions/`. The worktree diff is +1 line (`.ufo/state/`). `git ls-files .ufo/state` → 0, and `.ufo/state` is absent from the lane. |
| tripwire worktree = landed tool | `sha256sum tools/mado-tripwire.py` = `962919ce…` (unchanged so far); `tools/mado-verify.sh` = `fba82a66…` |
| adversarial result | `.ufo/waves/round-17/evidence/tripwire-w2-adversarial.txt`: `SELFTEST_SUMMARY: 4/26 passed`, 22 failed, exit=1, under `962919ce…`. At least 18 of the 22 are total misses `got=(0, [])`, including `var-pacman-install`, `ssh-sudo-install`, `base64-pipe-sh`, `perl-system-install`, `at-now-install` and `eval-js-blind`. |
| installer channels unclassified | lessons/round-17.md M4: the tripwire does not classify `uv tool`, `npx`, `pip`, `npm -g` or `cargo install`, and the wave context itself authorized `uv tool`/`npx` |

## Counterexamples

### H1 — "host pause held / no host mutation this round" is not attestable by the planned instruments
**Counterexample.** One seat runs `bash -c "$CMD"` with `CMD='sudo pacman -S x'`, or `ssh localhost sudo pacman -S x`. The round-18 seat-transcript tripwire scan reports `clean` exit 0. The adversarial receipt shows exactly these forms return `got=(0, [])`. A seat that runs `uv tool install`, `npm -g` or `cargo install`, or drops a binary into `~/.local/bin`, is also invisible (M4). Under the operator directive those channels are *authorized*, so "no install" is not even the right predicate.
**Evidence.** Adversarial receipt (4/26), lessons/round-17.md M4, ScoreResultsDraft harm row "host pause … [PENDING: attestation with command list]", ReportSkeleton `<CONDUCT_RESULT>`.
**Axes.** Operability (false provenance of a gate verdict) and calibration.
**Smallest correction.** State the attestation as two bounded receipts:
- **Package plane (complete):** the pacman.log window. Start: line count 3160, sha `f34d34e7…`, mtime 09:39:21 -0300. End: the same three fields re-read at close. The lane has no round-start receipt yet; commit one now, labeled "first observed 15:41Z, after dispatch".
- **Seat plane:** the tripwire result over seat transcripts, restricted to its covered forms. Name the 22 adversarial misses and the unclassified installer channels. List every authorized `uv tool`/`npx`/`~/.local/bin` install by name, version and channel.
Never let `clean` stand in for the pause.

### H2 — R15-V1 "unchanged" asserts a state the lane cannot observe
**Counterexample.** ScoreResultsDraft says "R15-V1 libinput partial upgrade | operator-owned, `[UNK]` | unchanged". Since R15-V1 opened (07:25, `:2429`), the host ran 13 unattributed pacman runs, including a full `-Syu` (`:2462`) that may have completed the partial upgrade. It also changed the boot chain (mkinitcpio 42, `:2539`) and rebooted ≈09:57. "Unchanged" is a present-tense host fact the lane is forbidden to measure (no `-Q`). The successful reboot invites a second false claim: "the mkinitcpio-42 / `/new_root` risk did not materialize, so the -Syu was safe."
**Axes.** Freshness and calibration (a hidden identity change of the host baseline).
**Smallest correction.** Write: "R15-V1: operator-owned. State `[UNK]` to the lane, which did not act on it. Since it opened, pacman.log records a full `-Syu` (`:2462`, actor unrecorded) and `/proc/uptime` shows a reboot ≈09:57 -0300. Neither is lane evidence of remediation or of boot-chain safety."

### H3 — Moving the tripwire row probe→gate upgrades the scan mode by association
**Counterexample.** SkillRegistryDraft §A puts `--frozen` and `--scan` in a single row with `gate/probe = gate`. A reader of the registry then takes a scan `clean` exit 0 as a gate verdict. Yet the scan still misses 22/26 adversarial forms and every installer channel.
`frozen_match` itself is a regression pin over committed bytes. It also exits 0 while `known_misses` asserts that real incident lines produce *no* finding. So "frozen_match" can certify a miss.
**Evidence.**
- Precedent for separate rows: SKILL.md registry `mado-action-plan` / `mado-action-plan-frozen` and `mado-frozen-regression` / `-r14`.
- The SKILL.md:562 row text "known misses pinned in … adversarial (4/26 by design)" reads as if 4 forms are missed. In fact 4 pass and 22 miss.
- The frozen limit paragraph in the draft is good, but it is appended away from the row.
**Axes.** Operability (duplicate authority: one row, two verdict semantics).
**Smallest correction.**
- Preferred: add a row `mado-tripwire-frozen | gate` and keep `mado-tripwire` (scan) as `probe`.
- If the pre-registered single-row move is kept, write inside the row's verdict map: "gate status attaches to `--frozen` only; scan exit 0 is a covered-forms observation (adversarial 4/26 pass, 22 pinned misses; installer channels unclassified)."
- Fix "4/26 by design" to "4/26 pass, 22 known misses".
- Report the frozen result as "replays the pinned verdict, including K pinned misses". Never write "detects the incident".

### H4 — "Capability acquisition" double-counts the round-17 tripwire capability
**Counterexample.** The round-17 closure already admitted "post-hoc transcript tripwire" as a capability (spot-check §2 C3, §5). Round 18 adds a frozen-replay entry to the *same* tool. Mado acquired the same pattern in rounds 13, 14 and 16. If the report says "new capability acquired: transcript tripwire", the capability table gets a second row for one identity.
**Axes.** Operability (premature saturation / identity change).
**Smallest correction.** Phrase it as "the round-17 tripwire capability gains a digest-pinned frozen regression gate (R17-V4)". Update the existing capability row in place, citing the first-working round 17 and a gate-entry round 18. Whether this is "acquisition" or "hardening" is a tradeoff for the canonical judge; the report must not pre-decide it.

### H5 — Concurrent classifier edits are unregistered improvements and re-open R17-V1 in the same round
**Counterexample.** Seats `TwMissBashCVar`, `TwMissHelperFn` and `TwInstallerChannels` are running. Any classifier change after the frozen pin is cut makes the following stale:
- the `962919ce…` suite receipts (9/16/33/30);
- the adversarial 4/26;
- the round-17 real-transcript receipts;
- the frozen expected verdict.

This is the R17-V1/V2 failure: receipts and report quoting a tool sha that is not the landed one. If a fixed form appears in the snapshot as a `known_miss`, the replay goes `frozen_verdict_mismatch`. Editing expected.json to match would then be blessing, not measurement. An "adversarial 4/26 → n/26" or "installer channels now classified" line would also be an unregistered claim, because SCORECARD says "No exploratory claim." A new installer class would also flag `uv tool`/`npx` installs that the operator authorized, labeling compliant seats as violators.
**Axes.** Calibration and operability.
**Smallest correction.**
- Freeze the classifier before cutting the frozen pin, or re-cut by measurement at the landed tool.
- Every receipt (suites, adversarial, frozen, real-transcript re-scans) carries `tool_sha256=<landed>` and `measured_commit=<rev>`.
- Report classifier changes under "harm watch / unclaimed observations", never as a C3 credit.
- Any installer class must be distinct from `host_mutation` and permit-able, and the report must say authorized channels are not violations.

### H6 — "Non-claim" jj fixes are load-bearing for C1 and move gate pins
**Counterexample.**
1. C1's F10 criterion is "runnable check shown able to fail", and that check *is* the failing-git-stub scenario added to `tools/mado-verify.sh`. SCORECARD's "Separable: C1 counts QUALITY text only" holds for the counter but not for the criterion's validity. If GateRcFix is rejected, criterion 26 cites a control that does not exist.
2. Editing `mado-verify.sh` moves its sha `fba82a66…`, the hermetic denominator (372 → 372+k), `PIN_MADO` (`cd1d73d7…`, SKILL "mado-regression" gate) and `TABLE_MADO`. "Harm watch unchanged, 372/372" would be false. The before row in ScoreResultsDraft ("gate sha `fba82a66…` 372/372") must not be reused as the after row.
3. The fix covers only `:3406`. The same F10 pattern ("piped `sha256sum` without rc repeats F10") is documented by JjAuditMado §5 at SKILL.md guidance lines 1056, 1259, 1278, 1632 and 1689. JjAuditMado R2/F6 (`:3382`, `:3391`, HEAD = `@-`, false DIVERGED) stays armed.
4. The round's own drafts repeat the pattern. ErratumR17 cites "verified by `git show 0ab1ccc:tools/mado-tripwire.py | sha256sum`". The ReportSkeleton C1 row counts with `git show REV:corpus/QUALITY.md | grep -c …`, where a failed read yields `0`.
5. `.ufo/state/` ignores no present or tracked path (`git ls-files` → 0; dir absent). It is preventive, not a repair.

**Axes.** Calibration (C1 independence) and operability (gate re-pin).
**Smallest correction.**
- Report C1 criterion 26 as dependent on the GateRcFix commit, and give its red control as a committed receipt: the baseline `fba82a66…` gate under the stub prints the false "local edit" FAIL, and the fixed gate prints UNKNOWN.
- Re-cut `PIN_MADO`/`TABLE_MADO` from a measured table with before/after values, and state the new hermetic N/N as a denominator change.
- Write "F10 site `:3406` repaired". Do not write "jj-migration defects fixed" or "gate jj-safe". List F6/R2 and the SKILL.md F10-pattern sites as open, or as dispositioned by PipeRcCensus.
- Replace evidence pipelines with `git show … > f && sha256sum f` (or `set -o pipefail`).
- Call `.gitignore` "preventive".

### H7 — C1's R17-V5 criterion can repeat R17-V5
**Counterexample.** Criterion 25 routes "tightenings shown to bite only in a `/tmp` lab". If its "shown able to fail" comes from MeasureMutants running in `/tmp` without a committed `evidence/measure-mutants.json` (and a red mutant that the instrument catches), the criterion repeats its own lesson. More generally, the literal counter (`^[0-9]+\. .*lessons/`) reaches 18/26 from any three lines containing `lessons/`.
**Axes.** Calibration.
**Smallest correction.** For each of criteria 24-26, cite a committed receipt in which the check *fails* on a named red input and passes on the landed state. Report "literal counter 15/23 → n/26". Do not write "calibration improved" without the three committed red receipts.

### H8 — C2 host declarations: version and identity phrasing
**Counterexamples.**
- (a) "walker 2.17.2 installed / host runs walker 2.17.2" or "elephant 2.22.1 running" overstates the evidence. pacman.log records an upgrade *event*; no `-Q` was run and nothing was executed. Upstream tag `v2.17.2` ↔ Arch `2.17.2-1` is `[INF]` (pkgrel), and a tag's source never proves the binary.
- (b) The note says 2.17.2 while SKILL.md:22 says 2.17.0 "re-verified `hyprctl version`". That makes two authorities for one pin, and freshness is not re-measured.
- (c) "omarchy v3.8.4 installed / clean / latest". By file bytes, HEAD → master `8fcc9d60…` = lightweight tag v3.8.4, so the identity holds. But "clean" (SKILL.md:24) cannot be re-verified without `git status`, and the index has been stale since 10-14. packed-refs also carries `v4.0.0` (`13f18b2c…`), so "latest" is false. A non-lane actor wrote packed-refs (09:14) and FETCH_HEAD/ORIG_HEAD (09:49) today, so "checkout untouched" is false. Theme/walker docs fetched from master or v4.0.0 do not describe this host.

**Axes.** Coverage (route honesty) and freshness (duplicate authority).
**Smallest correction.**
- Write "pacman.log:2929 records `upgraded walker (2.17.0-1 -> 2.17.2-1)` at 09:16:46 -0300; installed binary `[UNK]`".
- Fetch only tag-pinned `v3.8.4` omarchy sources.
- Name the SKILL.md:22 walker pin as stale per pacman.log, as freshness debt that is not re-anchored this round.
- Say "omarchy HEAD resolves to `8fcc9d60…` = tag v3.8.4 (file bytes); worktree state `[UNK]`; upstream v4.0.0 tag present locally".

### H9 — Factual error in a draft
ScoreResultsDraft "Planned" item 2 says "Round 17 pinned 4/26 adversarial misses as known limits". The receipt says 4/26 *passed* and 22 missed. Fix this before integration.

## Phrasing the report must avoid → bounded replacement

| avoid | use |
|---|---|
| "host pause held" / "no host mutation by any seat" / "seats clean" | "pacman.log unchanged across the round window (3160 lines, `f34d34e7…`, start/end receipts). Tripwire over seat transcripts: `<label>` for covered forms only (22/26 adversarial forms and installer channels not detected)." |
| "R15-V1 unchanged" / "resolved" / "superseded by the -Syu" / "boot chain safe" | "R15-V1 operator-owned, state `[UNK]` to the lane; `-Syu` `:2462` (actor unrecorded) and reboot ≈09:57 are not lane evidence of remediation" |
| "tripwire is now a gate" (unqualified) / "tripwire detects the round-15 incident" | "`--frozen` is a digest-pinned regression gate over a selected snapshot, replaying the pinned verdict including K known misses; scan mode remains probe-grade" |
| "new capability acquired" | "round-17 tripwire capability gains a frozen gate entry (R17-V4)" |
| "adversarial coverage improved" / "installer channels now covered" (as credit) | "unclaimed observation: adversarial n/26 at tool `<landed sha>`, receipt `<path>`; not a round-18 claim" |
| "jj-migration fixes" (plural, unqualified) / "gate is jj-safe" | "F10 site `:3406` repaired; F6/R2 and SKILL.md F10-pattern sites open/dispositioned" |
| "harm watch unchanged 372/372" after the gate edit | "hermetic N/N at gate sha `<new>`, denominator 372 → N (+k stub scenarios); PIN_MADO re-cut `cd1d73d7…` → `<new>` by measured table" |
| ".gitignore fix" | "preventive ignore of `.ufo/state/` (no tracked or present path)" |
| "calibration improved" from the counter alone | "literal counter 15/23 → n/26; criteria 24-26 each with a committed red receipt `<path>`" |
| "walker 2.17.2 / elephant 2.22.1 installed" / "omarchy v3.8.4 clean/latest" | "pacman.log:2929 / :3095 record the upgrade events; binary `[UNK]`; omarchy HEAD = `8fcc9d60…` = tag v3.8.4 by file bytes, worktree `[UNK]`, upstream v4.0.0 tag present" |
| "freshness re-anchored" | "freshness not re-measured; SKILL.md:22 walker pin stale per pacman.log:2929 (debt)" |
| "all receipts re-cut" | list each receipt path with its `tool_sha256` and `measured_commit` |
| "admitted" / "gate" decided by the lane | "registered by L1; non-author closure required" |

## Checks for L1 after integration
1. Run `wc -l`, `sha256sum` and `stat` on `/var/log/pacman.log` at close; compare with 3160 / `f34d34e7…` / 09:39:21.
2. `sha256sum tools/mado-tripwire.py`. Every round-18 tripwire receipt and the report must quote that value. If it is ≠ `962919ce…`, re-cut all four suites, the adversarial suite and the frozen pin under it.
3. `grep -n '| sha256sum' .ufo/waves/round-18 corpus/lessons/round-18.md` (or the PipeRcCensus probe) on the evidence commands themselves.
4. Confirm `evidence/` holds the committed red receipts for criteria 24-26 and the baseline-gate stub FAIL receipt.
