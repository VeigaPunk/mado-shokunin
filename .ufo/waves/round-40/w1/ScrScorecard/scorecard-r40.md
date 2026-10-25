## Round 40 — the option table meets the running compositor: native forms, angle inheritance, and the getoption ground (2026-10-25, attempt 1)

Registration `.ufo/waves/round-40/registration.md` (freeze `5e7e88525cc539563de7746361b2650802e81809`,
base `9fc511ddce708327377161202f358ce37dc266ba`): both counters, both control harnesses and their
receipts, the round-start receipts and the native capture committed before any round-40 data; the
delivered tool, the entry, the registry rows and every Gate line land after the freeze. Lowest-axis
rule: every published axis ties at its maximum at base (`receipts/axis-base.txt` — navigation
`published=56/56`, calibration `published=51/51`, operability `published=12/12`,
`MADO_AXIS: checked=3 mismatched=0`), so each is a lowest axis; C1 works operability, C2 works
coverage. The stagnation nudge does not apply: a capability row entered in round 39, inside the
window N=3. Round shape: one v2 wave `w1` of **64 seats**; round total `<<AFTER round total>>`
(residual calls: `<<AFTER residual calls>>`). The §3 planner seat is held by the L1.

| Claim / axis | Before → after | Counting command | Self-verdict |
|---|---|---|---|
| C1 **operability** (capability acquisition) — `tools/mado-options.py --live`: the option table merges the running compositor | `fixtures=0/13 tool=present verdict=TARGET_MISSED` exit 1 at base `9fc511d` (`receipts/c1-before-base.txt`; base has no `--live`, so every fixture run exits 2 on usage and only clauses a:1 g:1 hold) → `<<AFTER C1 fixtures=… tool=… verdict=…>>` exit `<<AFTER C1 exit>>` at the data commit `<<HASH C1 data commit>>` and the tip `<<HASH tip>>` (`<<AFTER C1 receipt paths>>`) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r40-live.py --repo . --rev <rev>` (`PRED-C1-r40-v1`) | `<<AFTER C1 self-verdict>>` — clause b needs the delivered `--selftest` at `k == n >= 79` (base: 71); the live host receipt (70 keys under the reference model, `w1`) is the out-of-distribution check, reported and not scored |
| C2 **coverage** (sourced) — `corpus/knowledge/hyprctl-getoption-native-forms-r40.md` + registry rows (held S162 and S173 re-opened; `<<AFTER new row count>>` new rows incl. one own-work census receipt) | `admitted=0/1 verdict=TARGET_MISSED` exit 1 at base `9fc511d` (`receipts/c2-before-base.txt`; the entry does not exist, every clause a–h:0) → `<<AFTER C2 admitted=… verdict=…>>` exit `<<AFTER C2 exit>>` at `<<HASH C2 data commit>>` (`<<AFTER C2 receipt path>>`) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r40-forms-entry.py --repo . --rev <rev>` (`PRED-C2-r40-v1`, clauses a–h; clause h binds the own-work receipt to the committed tool sha256 and to two count lines the entry repeats verbatim) | `<<AFTER C2 self-verdict>>` — residual declared: a fabricated self-consistent set passes (control P), committed bytes cannot prove what the location served or what the compositor answered |

Separable: C1 is judged by the tool and a stub compositor; C2 by entry/registry/receipt bytes and the
committed tool's sha, and its counter passes a dummy tool (control P) without C1's verdict; the two
claims share no file. Do-nothing and reachability controls (frozen at `5e7e885`):
`CTL_C1: controls=18 correct=18/18` — base tool `0/13`, the throwaway reference `13/13` on the
fixtures but `TARGET_MISSED` overall (clause b: its selftest is the base's 71, and the k clause needs
the capture), 16 one-defect mutants each `<13` (`receipts/ctl-c1.txt`, harness
`ctl/run-c1-controls.py`); `CTL_C2: controls=21 correct=21/21` — 20 mutants `0/1`, the fabricated
control P `1/1` (`receipts/ctl-c2.txt`, harness `ctl/run-c2-controls.py`).

No harm: `bash tools/mado-verify.sh --selftest` `<<AFTER selftest line>>` (`<<AFTER selftest receipt>>`;
base `MADO_SELFTEST: 460/460 assertions passed`); `python3 -I tools/mado-options.py --selftest`
`<<AFTER options selftest line>>` (base 71/71; C1 clause b requires n ≥ 79);
`quality/check-index.py` `<<AFTER index line>>` (baseline `indexed=56/56`; only the C2 entry adds a
row); `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` exit
`<<AFTER census exit>>` (same seven W04 and one W01 as at base, `receipts/census-before.txt`);
`python3 -I quality/check-axis-scores.py` `<<AFTER axis line>>`; `hyprctl getoption -j` the only
compositor verb run (read-only), no config tree, compositor state, service, sibling lane or fleet-repo
path other than the report written.

### Capabilities (round 40)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| live option-table merge | label every declared key of a hyprlang config tree against the running compositor through the compositor's own read verb — one `hyprctl getoption -j KEY` per declared key and no other argv — comparing the native reply (`int`/`float`/`str`/`custom`, or the text `no such option`) after host-style conversion: hyprlang v0.6.8 `configStringToInt`, Hyprland v0.56.2 gradient/gap/font-weight handlers, gradient colours as lowercase unpadded ARGB words with the angle inherited from the previous declarer when a redeclaration carries no `deg` token; into the five labels `agreement` / `agreement*` / `mismatch` / `config-only` / `live-default` (the last for `--probe` keys with no declarer); a compositor failure exits 5 naming the key, a hostile probe key exits 2 before any program runs; standard library only, no write | `tools/mado-options.py` (selftest `<<AFTER options selftest line>>`); `quality/counters/c1-r40-live.py` `<<AFTER C1 fixtures>>` at `<<HASH C1 data commit>>`; host census `<<AFTER host census labels>>` (`.ufo/waves/round-40/fetch/<<AFTER live census receipt>>`, reported, not scored) | 40 |

### Sources, saturation, planned

Sources 214 → `<<AFTER source count>>` rows (S162 and S173 re-opened held; `<<AFTER new row count>>`
new, incl. one own-work census receipt; tier `<<AFTER tier>>`; `mined`; opened 2026-10-25); old→new in
`corpus/lessons/round-40.md`. Assimilation (rides inside §2b; no claim slot): package `merge/mado/`
(read-only), theme "the host's bar producers" — `host-bar-producers-r28.md` and
`host-producer-outputs-r29.md`: `<<AFTER assimilation: N admitted re-grounded, M refused, reasons>>`.
Domain-versus-meta ratio of the last 30 commits (criterion 60), measured at `<<HASH tip>>`:
`<<AFTER domain/meta ratio>>`. Saturation `<<AFTER saturation>>`; retired: `<<AFTER retired>>`.
Frontier step: the round-start census ran exit 0 with seven W04 and one W01
(`receipts/census-before.txt`); considerthese `2026-10-25.md` proposal 2 is mined as a lesson table
(`<<AFTER considerthese outcome>>`).

Axis table re-derived at `<<HASH tip>>`: navigation `<<AFTER navigation>>`; calibration resolved-active
`<<AFTER calibration>>`; operability selftest `<<AFTER operability>>`.

### Planned (round 41; intent only)

1. Close C1's declared residual: the fixture generator's value space is the reference model's own
   conversion tables, so a tool that hardcodes them passes the fixtures; add out-of-distribution
   fixtures (values outside those tables) or a clause that binds the live receipt — decided in the
   round-41 registration before any data.
2. The next shokuknow theme or considerthese proposal per the frontier (round 40 mines
   `considerthese/2026-10-25.md` proposal 2, the watchdog dead-attempt and dirty-closure table, as a
   lesson table; round 41 carries whichever item the frontier ranks next).
