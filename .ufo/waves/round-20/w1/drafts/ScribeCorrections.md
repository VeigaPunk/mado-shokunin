# ScribeCorrections — draft correction blocks (round 20, append-only)

Status: DRAFT for L1 integration. Not applied. `corpus/lessons/round-19.md`, `corpus/lessons/round-19-verifier-spotcheck.md` and the round-19 part of `SCORECARD.md` are closure or lane-authored and are not edited here. Corrections land as (A) a new `## Round 20 — corrections to round 19 (append-only)` section in `SCORECARD.md`, and (B) a `## Corrections to round 19` section in the round-20 lesson (`corpus/lessons/round-20.md`, not yet present at this tip).

Every locator below is relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`. Checks run by this seat are read-only (`git show`, `git ls-tree`, python reads of committed bytes, `json.load` on receipts). Nothing was executed from fixtures, and no host probe, package query, or live gate was run.

---

## (A) SCORECARD.md — new section, to append at end of file

```markdown
## Round 20 — corrections to round 19 (append-only)

Recorded in round 20 by the scribe seat (ScribeCorrections). Each item quotes the
round-19 statement, the measurement that contradicts or qualifies it, and the
disposition. Round-19 text above is not rewritten. Closure reference:
`corpus/lessons/round-19-verifier-spotcheck.md` (`rejected-harmed`).

### R19-V1 — C1 miss stays a miss (no redefinition)

- Round-19 text (SCORECARD, `Round 19 — committed results`, C1 row): "pre-registered target ≥ 21/29 missed by decision: R18-V2 is recorded as an application of criterion 24, not a criterion 29".
- Measured: counter `measure.py` 18/26 → 20/28 (closure census, `corpus/lessons/round-19-verifier-spotcheck.md:47`). Target ≥ 21/29 not reached.
- Correction: the ≥ 21/29 target is **missed**. Re-classifying R18-V2 under criterion 24 does not turn the miss into a hit, and the target is not retroactively redefined. Next calibration claim needs a fresh pre-registration with grounded failure evidence.

### R19-V2 — C2 S096 tally (any-line 8/13, first-line 6/13; five S090-only files; provenance, not behaviour)

- Round-19 text: "5/13 name S096 on the crediting line" (SCORECARD `Round 19 — wave-2 corrections`, C2 bullet; source `.ufo/waves/round-19/w2/reports/RerunC2.md:71`). That count was taken at the `01b80946` snapshot.
- Measured at the tip (`b435568`, and unchanged at `7b4839d` and `e629f73`). Fixed set = the 13 baseline files at `9c54c56` that contain `2.17.0` (SKILL.md, corpus/README.md, corpus/knowledge/{arc-synthesis, closeout-r11, config-health-report-r3, remaining-planes-census, walker-deep-r9, walker-deep, walker-live-surface, walker-route-r18, waybar-walker-plane, waybar-walker-semantics}.md, tools/mado-verify.sh). Recomputed by `/tmp/scribe-cc/s096.py` (read-only `git show` of committed bytes; output identical at all three revisions):
  - any-line: a line matching `2\.17\.2` and `\bS\d{3}\b` that also contains `\bS096\b` → **8/13** (SKILL.md, corpus/README.md, remaining-planes-census, walker-deep-r9, walker-deep, walker-live-surface, walker-route-r18, tools/mado-verify.sh).
  - first-line: only the first qualifying line decides → **6/13**.
  - No qualifying S096 line in five files, each cites only the round-18 row S090 (`/var/log/pacman.log:2929`) on its dated pointer: `corpus/knowledge/arc-synthesis.md:392`, `closeout-r11.md:299`, `config-health-report-r3.md:1009`, `waybar-walker-plane.md:479`, `waybar-walker-semantics.md:467`.
- Correction: "5/13" is not the tip figure. The tip figures are **8/13 any-line** and **6/13 first-line**. The pre-registered C2 promise that every file cite the new host-byte row (S096) is **not met**; the 13/13 result is a pointer count (supersede-sweep `pointed=13`), not an all-file S096 citation.
- Scope of the claim: S096 is a host-byte provenance pin (`/usr/bin/walker` sha256 `25240650…`, one literal `2.17.2` at offset 856,302, no `2.17.0`, read as bytes 2026-10-20; closure table row S096). It is **not** a walker behaviour re-measurement. `walker --version` and 2.17.2 behaviour remain `[UNK]`.

### R19-V4 — fail-open isolation, the 154-file receipt, and scan blindness (self-report, not detection)

- Round-19 text, lesson `corpus/lessons/round-19.md:124`: "155 round-19 transcripts". Committed receipt `.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt` (merged tool `367be947…`): its JSON `files` array has **154** entries (`json.load`, `len(files)=154`; counts `host_mutation 0, live_probe 3, package_query 0, tool_install 0, vcs_write 164`, exit 1). Correction: **154 files**. The "155" is a prose error.
- Incident (SentinelGatePath, `.ufo/waves/round-19/w2/reports/SentinelGatePath.md:75-79`): the first harness `unshare --user --map-current-user --mount` was refused by `mount` ("must be superuser"); the script's `[ -e ] && mount && echo` chain does not trip `set -e`; therefore `/usr/bin/hyprctl probe` ran against the real binary (output `unknown request`, rc=0). Correction: this was a **fail-open** isolation harness. Setup failure did not abort before the payload. Host state change was not independently measured (closure `corpus/lessons/round-19-verifier-spotcheck.md:124`).
- Detection: the post-wave scan did **not** see the real probe. It ran inside a script the seat wrote and executed; the tool documents that form as unanalysed (`corpus/lessons/round-19.md:127-129`). The incident's captured-by is therefore `none (seat self-report)`. Correction: the self-report must not be recorded as tripwire detection.
- Record note: `SentinelGatePath.md:32` shows the later `--map-root-user` form, and its `inns.sh` fix (exit 99/98 unless every bind succeeds, `:79`) was applied after the incident. Which exact command ran first is taken from the transcript, not the later report; `[UNK]` beyond the report text.

### R19-V5 — OM10 count: nine labeled occurrences, eight distinct (not ten)

- Round-19 text (SCORECARD, `Round 19 — final state`, final paragraph): "the ten old OM10 assertions were replaced by OM10A/B".
- Measured (`git show 9c54c56:tools/mado-verify.sh`, labeled OM10 assertions at lines 839–848): **9 labeled occurrences**, **8 distinct** labels (`OM10: the UNKNOWN names the rc` appears at 841 and 842). Replacement at `b435568`: **OM10A six** (lines 900–906) and **OM10B eight** (lines 913–922); closure reports these as counted in `corpus/lessons/round-19-verifier-spotcheck.md:88`. Neither count is ten.
- Correction: "ten" → **nine labeled occurrences (eight distinct)**, all OM10, replaced by OM10A six + OM10B eight. The "no other prior assertion lost" statement stands as the closure states it.

### R19-V6 — misroot and dead-seat accounting

- Misroot (lesson `corpus/lessons/round-19.md:23`, M8): seat QualityDraft wrote at the fleet root by a relative path. The lane copies `.ufo/waves/round-19/drafts/QualityDraft.md` and `.ufo/waves/round-19/w1/reports/QualityDraft.md` are present (both 14:07, verified). Correction: every seat item uses absolute lane paths; relative fleet-root writes are a recorded misroot, not a silent slip.
- Dead seats: round-19 registry `.ufo/waves/round-19/w1/reports/swarm-registry.json` has **86** members (verified). Report files in `w1/reports/`: **62 `.md`** plus the registry JSON (63 entries). The closure's "25 lacking reports" is **not reproduced**: the registry's `item` and `agentId` fields are null/absent for the join, so membership cannot be matched to reports by file. Under a one-report-per-member reading the arithmetic gives 86 − 62 = 24, not 25. Disposition: **[UNK]**, dead seats remain uncredited, and the join key must be recorded before the count is cited again.
- Provider failure (zai 429 retry exhaustion, closure) is not claim evidence and is not credited.

---

Limits of these corrections: the S096 recomputation covers the 13-file fixed set at the three revisions named; first-line semantics follow the closure's definition; the OM10 counts use exact `OM10` label text in the gate; the dead-seat count is [UNK] for the reason above.
```

## (B) corpus/lessons/round-20.md — section to add (round-20 lesson; file to be created by L1)

```markdown
## Corrections to round 19 (append-only)

- The C1 target ≥ 21/29 was missed (20/28). A criterion re-classification does not convert the miss (R19-V1).
- S096 tally at the tip: 8/13 any-line, 6/13 first-line; five files cite only S090 (`arc-synthesis.md:392`, `closeout-r11.md:299`, `config-health-report-r3.md:1009`, `waybar-walker-plane.md:479`, `waybar-walker-semantics.md:467`). The "all files cite S096" promise is unmet. The S096 row is a provenance pin, not a walker behaviour measurement (R19-V2).
- The round-19 post-wave scan receipt has 154 files, not 155 (`corpus/lessons/round-19.md:124`). The `inns.sh` harness with a `[ -e ] && mount && echo` chain failed open and executed `/usr/bin/hyprctl probe`; the tripwire did not detect it, so the captured-by is self-report only (R19-V4).
- OM10: nine labeled occurrences (eight distinct) at `9c54c56`, replaced by OM10A six + OM10B eight; not "ten" (R19-V5).
- Misroot QualityDraft (relative path) is recorded; all round-20 seat items carry absolute lane paths. The round-19 dead-seat count of 25 is not reproduced from the registry (86 members, 62 reports, join key null) and remains [UNK] (R19-V6).
```

## Routing for L1

- Place block A at the end of `SCORECARD.md` (append-only).
- Place block B in the round-20 lesson when it is created.
- Round-19 lesson, round-19 SCORECARD text, and closure file: unchanged.
- Reserved SOURCES ids S099–S110 are not used by these corrections.
