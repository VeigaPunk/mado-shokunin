# Draft — SCORECARD.md `## Round 41` section

Drafted by seat `ScrScorecardLog` (wave w2) for L1 integration. Place after the round-40 section (currently at `SCORECARD.md:2474-2493`). The axis-sentence numbers are left as placeholders (`A/B`, `C/D`, `E/F`) per the seat assignment; the L1 re-derives them.

---

## Round 41 — mado-globals and the focus-grab entry (2026-10-25, attempt 1)

Registration `.ufo/waves/round-41/registration.md` (v1 freeze `60c3914154333180450d5da27ba222d5763cc56a`, base `ab2bfaab661c846d1de9d58c01651cd156a13949`) and its re-registration `registration-v2.md` (v2 freeze `294c667901a8c7b7165ba849d03cba9a24c14fa4`, before any data): the 34-seat wave `w1` (dispatch `cd950ec`) falsified the v1 predicates — 8 of 12 cheats scored TARGET_MET on C1, 13 of 42 extra mutants survived, 9 of 9 C2 forgeries admitted, 29 of 45 extra C2 mutants survived (`CritC1Cheat`, `ExecC1ExtraMutants`, `CritC2Cheat`, `ExecC2ExtraMutants`, `RevC1Counter`, `RevC2Counter`, `RevRefTool`, `MutSelftestFixtures`). Lowest-axis rule: every published axis ties at its maximum at base (`receipts/axis-base.txt`: navigation 58/58, calibration 55/55, operability 12/12). Round shape: two v1 waves — `w1` of 34 seats (build + first falsifiers) and `w2` of 34 seats (falsify, dispatched after the data commit); no residual call; round total 68; the §3 planner seat is held by the L1.

| Claim / axis | Before → after | Counting command | Self-verdict |
|---|---|---|---|
| C1 **operability** (capability acquisition) — `tools/mado-globals.py` | v2 `fixtures=0/39 tool=absent verdict=TARGET_MISSED` exit 1 at base (`receipts/c1-v2-before-base.txt`) → `fixtures=39/39 tool=present verdict=TARGET_MET` exit 0 at the data commit `07f2641` and at the tip (`receipts/c1-v2-after-data.txt`) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r41-globals-v2.py --repo . --rev <rev>` (`PRED-C1-r41-v2`) | **TARGET_MET under v2**; the superseded v1 predicate reads `fixtures=6/24 … TARGET_MISSED` at the data commit because the contract changed — the delivered tool is the v2 reference, which the v1 counter was never written to judge (clause g:0; re-registration discloses both scores) |
| C2 **coverage** (sourced) — `corpus/knowledge/hyprland-focus-grab-r41.md` | v2 `admitted=0/1 verdict=TARGET_MISSED` exit 1 at base (`receipts/c2-v2-before-base.txt`) → `admitted=1/1 verdict=TARGET_MET` exit 0 at the data commit `07f2641` and the tip (`receipts/c2-v2-after-data.txt`) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r41-focus-entry-v2.py --repo . --rev <rev>` (`PRED-C2-r41-v2`) | **TARGET_MET under v2**; the v1 predicate also reads `admitted=1/1` at the data commit; residual: a fabricated self-consistent set passes (control P) |

Separable: `ConnCrossClaim` verified C1 reads only `tools/mado-globals.py` and C2 only the entry, registry, lesson, README and fetch receipts; no shared deliverable.

No harm: `ExecHarmChecks` baselines at `60c3914` — verify suite `MADO_SELFTEST: 460/460 assertions passed`, index `indexed=58/58`, census exit 0 with the same seven W04 + W01; the data commit adds only the tool, the entry, rows S283–S289 (+ S037 used-by), the README row, the lesson and the fetch receipt `xdph-installed-version.txt`; `receipts/census-after-data.txt` shows the same W04 set.

### Capabilities (round 41)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| compositor global advertisement census | read the desktop portal's user journal and report per session which Wayland globals the compositor advertised — interfaces, highest version, counts, class table — with `--diff`, `--expect NAME`, a bounded `--live` journalctl mode and a full selftest; sandboxed, reads only the journal, never connects | `tools/mado-globals.py` (byte-identical to the v2 reference, sha256 `286c051f…`); `quality/counters/c1-r41-globals-v2.py` 39/39 at `07f2641`; live host census: two sessions, 63 interfaces in the latest, `hyprland_focus_grab_manager_v1 ver=1 class=focus-grab` (`w1/ExecLiveHost/live-census.txt`) | 41 |

### Sources, saturation, planned

Sources 219 → 226 rows (S283–S289, tier A, opened 2026-10-25; S037 `used-by` extended to the entry); knowledge entries 58 → 59; the entry is indexed in `corpus/README.md` (one column-zero row). Assimilation: the focus-control theme admitted as the entry's successor (`ADMIT`); two staged candidates refused (`REFUSE`: `privileged-client-surface-r29.md`; `focus-control-surfaces-r28.md` §3 localized channel). Saturation 9.0 / N=3 unchanged; retired: none.

Axis table re-derived at `<rev>`: navigation A/B; calibration C/D; operability E/F.

### Planned (round 42; intent only)

1. The remaining package themes under PROVINCE (`ScoutMergeRest`: gkeep rendered geometry is the ranked successor; socket-client-contract residue).
2. An independent non-author re-run of both v2 counters with fresh nonces (round-41 lesson D3).
3. Route the w2 falsification findings (open predicate defects, if any).
