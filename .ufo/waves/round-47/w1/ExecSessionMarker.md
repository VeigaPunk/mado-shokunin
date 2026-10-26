# ExecSessionMarker — round-47 w1 R3: the synthetic-fixture marker, installed and shown able to fail both ways

Seat: `ExecSessionMarker` (leaf, no subagents). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Measured at base **`60edb66e2f1cb90acc6e9442fc93ded0ca42d750`** (round-46 verifier spot-check; lane tip at
round-47 start). Lane HEAD while this seat ran: `c24adef2632672325a4eef3e3492f6716ccb6d14` (round-47 dispatch only).
Nothing in the lane was written outside `.ufo/waves/round-47/w1/ExecSessionMarker/` and this report.

Routed item: round-46 spot-check §6 **R3** — *"`mado-session-material` is red at the data commit (`findings=115`,
exit 1; 18 in round-46 seat files): install the drafted synthetic-fixture marker (`w1/ExecSessionTriage/`) and the
prose serial rule (`w1/ExecSerialRule/`), shown able to fail both ways"*
(`corpus/lessons/round-46-verifier-spotcheck.md:113-116`).

## 1. What landed

| path | what | sha256 |
|---|---|---|
| `.ufo/waves/round-47/w1/ExecSessionMarker/check-session-material.py` | the tracked gate + the marker layer + the prose serial rule, one file, 1599 lines; selftest **63/63** | `a4a0a084e745f511048d5be445bed4959a18b5d64798a55da06c74cc0d08e9c9` |
| `demo/registry-round47.txt` | **the install set**: 49 rows (48 `fixture` + 1 `gate-copy` for this seat's own gate file) | — |
| `demo/sidecars/` | the 49 `<path>.synthetic` sidecars those rows name, lane-relative | — |
| `demo/registry-round47-refreshed.txt` | the same set after the two stale gate copies are refreshed: 51 rows | — |
| `demo/sidecars-refreshed/` | the 2 extra sidecars that upgrade the above | — |
| `demo/skill-row.md` | the `SKILL.md` gate-registry row, replacing `SKILL.md:770` | — |
| `demo/triage.py` | the generator: lets the gate decide what is synthetic (two passes) | — |
| `demo/mark.py` | demo helper: writes one marker pair into a scratch clone | — |
| `demo/run-demo.sh` | rebuilds every number in this report from three scratch clones | — |
| `demo/triage-as-is.tsv`, `triage-round47.tsv`, `triage-refreshed.tsv` | every remaining finding, one line each: path, rule, class | — |
| `receipts/00…17` | gate output and exit status, one receipt per measurement (`17` re-checks every number this report quotes) | — |

Parents, for provenance: tracked gate `quality/check-session-material.py` sha256 `889f8f05…` (682 lines);
marker-gate copy `.ufo/waves/round-46/w1/ExecSessionTriage/check-session-material.py` sha256 `3fc480a4…` (1211 lines);
prose-serial copy `.ufo/waves/round-46/w1/ExecSerialRule/gate.py` sha256 `a36224e2…` (991 lines). The delivered file
contains every one of the 22 selftest cases of the tracked gate (checked by case-name set difference: 0 missing),
the 12 marker cases of the round-46 copy, the 23 serial cases of the round-46 serial copy, plus 6 new cases for the
marker×serial interaction — 63 total.

## 2. The contract as installed

A marker is a **pair**, both read from the scanned revision:

1. a tracked sidecar `<path>.synthetic`, whose first line is exactly
   `SYNTHETIC-MATERIAL v1 kind=<fixture|gate-copy> rules=<R1-R4 csv> sha256=<64 hex>`;
2. one line `<path> <sha256> <rules> kind=<kind>` in `quality/session-material-waivers.txt` (outside `.ufo/`).

A `(file, rule)` finding is waived only when all of W1-W4 hold:

| condition | what it stops |
|---|---|
| W1 path under `.ufo/waves/`, registry outside `.ufo/` | a wave issuing its own waiver; the waiver is one reviewable lane diff |
| W2 sidecar tracked, grammar exact, `sha256` = sha256 of the target blob | appending anything to a waived file voids the waiver (`sha-mismatch`) |
| W3 the registry line repeats path, sha256, rule list and kind | writing a fixture does not write the waiver (`unregistered`, `registry-*-mismatch`) |
| W4a `kind=gate-copy` ⇒ target byte-identical to `quality/check-session-material.py` | borrowing `gate-copy` for anything but a copy of this gate (`gate-source-mismatch`) |
| W4b `kind=fixture` ⇒ every matched value inside a reserved namespace | a real title, serial, process row, vendor string or home user (`value-not-synthetic:<what>`) |

What this seat added on top of the round-46 drafts, and why:

- **The serial rules are outside the waiver surface, structurally.** The sidecar grammar
  (`MARKER_RE`) accepts `R[1-4]_…` only, so a sidecar naming `R5_SERIAL_PROSE`/`R6_SERIAL_EXACT` is
  `marker-malformed`; and `apply_waivers()` refuses a serial finding on a *marked* file with
  `reason=serial-rule-not-waivable` **before** it parses the marker. A serial has no reserved namespace —
  its identity is the value — so no marker can ever launder one. Registry rows are validated the same way
  (`WAIVABLE_RULES`), so a hand-written `R5` row is ignored rather than trusted.
- **No flag can drop a rule.** The round-46 serial copy carried `--rules` for incremental gating; installed
  here that is a knob that silently hides the prose-serial leak. It is gone: R1-R4 and R5 are always scored,
  R6 contributes only when `--serial-from-host` supplies values. New selftest case
  `e2e-no-rule-can-be-dropped` asserts argparse rejects `--rules` with exit 2.
- **`--scope ufo|all`** (default `ufo`, the historical behaviour) and **`--serial-from-host`** (one
  `hyprctl monitors all -j` read, counts only) come across from the round-46 serial copy unchanged.
- **`WAIVABLE_RULES + SERIAL_RULES == RULES`** is asserted in the selftest, so no future rule can be added
  outside one of the two bands by accident.

## 3. The five demonstrations (required), measured

Clones `c1` and `c3` are `git clone -q --shared --no-checkout` of the lane at `60edb66`, checked out detached;
`c4` is a shared clone of `c3` with the two gate copies refreshed. Every clone asserts
`git rev-parse --show-toplevel` equal to its own directory before any commit; commits use a scratch identity only.

| # | state | measurement | exit | receipt |
|---|---|---|---|---|
| 1 | base `60edb66`, **tracked gate untouched** | `SESSION_MATERIAL: files=18371 findings=115` (R1=29 R2=31 R3=53 R4=2) | **1** | `01-baseline.txt:117` |
| 2 | gate installed, **no markers** | `findings=136` (+21 `R5_SERIAL_PROSE`), same 18371 files | **1** | `02-new-gate-no-markers.txt:138` |
| 2′ | + the install set (`registry-round47.txt`, 49 sidecars) | `SESSION_MATERIAL_WAIVED: findings=55 files=49`; `findings=84`; R1=26 R2=29 R3=6 R4=2 R5=21 | **1** | `13-seat-tree-with-markers.txt:141-142` |
| 3 | a **real dump planted, unmarked** (`.ufo/waves/round-47/w1/PlantedSeat/live-monitors.json`) | two new findings on that file (`R3_MONITOR_IDENT count=1`, `R5_SERIAL_PROSE count=2 shapes=9x3+Ax5+9x4`); total 84 → **86** | **1** | `05-planted-real-dump.txt` |
| 4 | the same **real dump appended inside a waived fixture** (`.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C00_shipped/mons.json`) | `WAIVER_REJECTED … reason=sha-mismatch`, waived 52 → **51**, `FINDING … R3_MONITOR_IDENT count=2` returns, total → **88** | **1** | `06-real-dump-in-marked-file.txt` |
| 5 | the **registry names a file with a real serial** (valid sidecar + valid row + correct sha256, `kind=fixture rules=R3_MONITOR_IDENT`) | `WAIVER_REJECTED … rule=R3_MONITOR_IDENT reason=value-not-synthetic:serial-not-synthetic`; `rule=R5_SERIAL_PROSE reason=serial-rule-not-waivable`; `rule=R6_SERIAL_EXACT reason=serial-rule-not-waivable`; all three findings kept | **1** | `07-registry-names-real-serial.txt` |

The two directions the routed item asks for are therefore both shown on the same tree:

- **synthetic findings disappear**: 136 → 84 at the seat-tree state, of which 55 findings in 49 files are
  counted on the `SESSION_MATERIAL_WAIVED` line, and `--no-waivers` returns the pre-marker findings line for
  line (`15-no-waivers-parity.txt`: identical `FINDING` and `SESSION_MATERIAL_RULES` sets), so the drop is the
  marker layer's, not changed content.
- **a real value never disappears**: cases 3, 4 and 5 each keep their finding with a named reason.

Supporting measurements on the same run:

- **the exact-value rule works on the same tree**: `--serial-from-host` adds `R6_SERIAL_EXACT=23` findings
  (21 prose carriers + the planted dump + the tampered fixture) and prints counts only — `08-r6-exact-host-serial.txt`.
- **a serial can never be waived through the marker**: every `R5`/`R6` line in
  `07-registry-names-real-serial.txt` carries `serial-rule-not-waivable`, including the two files that do
  have valid markers.
- **a stale gate copy is not waivable**: the two copies (`round-45/w1/ExecPrivacyGate`,
  `round-46/w1/ExecSessionTriage`) are copies of *older* gate bytes, so `kind=gate-copy` cannot apply and
  W4b refuses them as fixtures. Refreshing them to the installed bytes closes exactly those six findings and
  nothing else: refused 63 → 57, waived 55 → **61** in 51 files, remaining 84 → **78**, with an identical real
  set (`09-triage-refreshed-copies.txt`, `10-refreshed-with-markers.txt`).

## 4. What remains, and why it must

At the seat-tree state (`12-triage-seat-tree.txt`, `13-seat-tree-with-markers.txt`) the gate is red with
**84 findings in 75 files**. The gate classified each one itself; the classes are exhaustive:

| class | findings | what it is | who owns it |
|---|---|---|---|
| `real:identity:program-not-synthetic` | 27 | process-table rows naming real programs (the round-37/38/39 socket-table receipts and the reports quoting them) | the evidence-owning seats: redact or retain deliberately |
| `real:identity:title-not-synthetic` | 24 | client dumps whose titles are not in a reserved namespace (the round-43 `gkeep-oracle-probe` fixtures, the round-44 lesson demo, the round-46 gate-fixture copies) | the owning seats: retitle into a reserved namespace, or accept as real |
| `real:identity:serial-not-synthetic` | 3 | monitor dumps whose serial is a literal | owning seats |
| `real:identity:home-user-not-synthetic` | 2 | `/home/<real user>` listings | owning seats |
| `real:identity:vendor-not-synthetic` | 1 | a monitor `make`/`description` outside the reserved vendor words | owning seats |
| `real:serial` (`R5_SERIAL_PROSE`) | 21 | **the host monitor serial in prose** — 18 round-32/37 wave copies of the three held entries | **operator** (removal from pushed history is their decision, as the spot-check recorded) |
| `synthetic:stale-gate-copy` | 6 | the two older gate copies × R1/R2/R3 | integrator: refresh the copies (below) or accept |

With `--scope all` two pre-existing classes join (`16-scope-all.txt`: 92 findings = 84 + 8):
the three held `corpus/knowledge/` serial carriers (R5 21 → **24**, matching
`.ufo/waves/round-46/w1/ExecSerialRule/`'s count) and five non-serial findings outside `.ufo/` — three on
the installed gate's own selftest constants and two on the round-37/38 socket-table counters. That is a triage
budget, not a new leak: the entry command pins `--scope ufo`, and the wider scope is a deliberate reading, not
the gate's default.

**The marker cannot and must not close these.** Each one is either a real value the policy exists to catch, or
synthetic content that carries a real value inside it — the redaction gap ExecSessionTriage declared
(`.ufo/waves/round-46/w1/ExecSessionTriage.md` §6). The remedy there is at source: reserved pids/programs/titles,
not a waiver.

## 5. Exact registry content and the SKILL.md row

`demo/registry-round47.txt` — the exact file, 49 rows under one header line, to be committed as
`quality/session-material-waivers.txt`:

```
# path sha256 rules kind — see quality/check-session-material.py
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C00_shipped/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C01_shipped_scale2_live/mons.json 4762275d80af15cbc9a4f71543fd80727fc1be99c9b1b3baa2966726901b735c R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C02_fractional_1.6/mons.json 0700e0453cb59eab369bcbff3a3f9e55caf9908caf2abedbc968631746437125 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C03_fractional_correction_1366/mons.json f103664f4340ba6dc4486ab24c5c81d58d987905f77e4645c35a460df50475ce R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C04_1x_preset_live2/mons.json 4762275d80af15cbc9a4f71543fd80727fc1be99c9b1b3baa2966726901b735c R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C05_1x_preset_live1/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C06_portrait_transform0/mons.json 12998ad0a205b57520b1ec79a14cd943226aff5ca9c97ba8148339e2534e4152 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C07_portrait_transform1/mons.json 30b6439521c68be3e2094c3fa88651e11647aa6240ad6de43e6940bd43ceaf87 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C08_apple_pair/mons.json 1ca2202f023d318f0bb665a47190ba829f40fbc3ae865b2e23596dda8e635fc8 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C09_apple_pair_only_DP1/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C10_ghost_alone_live/mons.json 88734d6ef2117ef96a2a4fede913d055da9f40c1bb5c35501d9639965eb7018f R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C11_ghost_plus_default/mons.json 58fc0beab150124def46894ce79e3fe2194af38d26eaf1a34f6a9d4083393f1a R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C12_ghost_plus_default_live/mons.json c577659f969139a19e920c19d2fed2b82d40745d19602dff9d0f18fe232d2a80 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C13_mirror_agree/mons.json 9b98e80a68420d5490ca88f64eb3f0d4ce23f32b3937dbb13853e87f35e63b72 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C14_mirror_none/mons.json fe8c254b55e508ab4bf619d12c637afa93b86510d738bf83aca6c76559ab40b9 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C15_vrr_leftover/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C16_five_decimal_mode/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C17_scaling_cycle_keyword/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C18_two_catchalls/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C19_env_only/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C20_commented_all/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w2/D01_disable_toggle_applied/mons.json 21a2f13395db34ed5a2d791a2630d66e60a39e8a26918cd70eaf4d010a8fe3cd R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w2/D02_disable_toggle_not_applied/mons.json 76fbdd8031de412b34d210baaf229e7286769f3ee2dbbdd9e5b97cee31b349e3 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w2/D03_erase_on_add_selector/mons.json 21a2f13395db34ed5a2d791a2630d66e60a39e8a26918cd70eaf4d010a8fe3cd R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w2/D04_monitors_conf_only_mirror/mons.json 4e3e287aa2298f443eaf85ccf005e70cea5289c22fbb4b4e80b3827163e6fc2b R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w2/D05_host_conf/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w2/D06_catchall_transform_rotated/mons.json 66a25b85b95d1aa432478fb4ca206ba088f9603d4d0661a17d06d047f71aa86a R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w2/D07_1.6_vs_auto_1.5/mons.json 072f9763b3d6843ba833e2ed502d136a7277e6e883b8988ba113871e495d241e R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w2/D08_five_decimals_59.95055/mons.json 5fef18346d21e3022d5aac9750670eb7a3fe873330a0c3b6f77d7807cec3e895 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w3/E01_both_fractional/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w3/E02_both_1x/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w3/E03_ghost_shipped_way/mons.json 58fc0beab150124def46894ce79e3fe2194af38d26eaf1a34f6a9d4083393f1a R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w3/E04_apple_plus_default/mons.json 1ca2202f023d318f0bb665a47190ba829f40fbc3ae865b2e23596dda8e635fc8 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w3/E05_portrait_plus_default/mons.json 56daea08a91ea55fd581340c410d7bd5f33c1ad1e04a3530a3e768268b4a43fe R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w3/E06_fractional_pair_full/mons.json ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w4/F01_1366_rule_2.0.json 4b12bfa366c1b000699572e5aadc4a6ce258ed95d7578b5c1b77c9437ede1e98 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w4/F02_1366_rule_1.6.json 4b12bfa366c1b000699572e5aadc4a6ce258ed95d7578b5c1b77c9437ede1e98 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w4/F03_position_after_cycle.json 175d81e95477a7671463f870f264a237a6f441682420900d1b64076f691b2989 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w4/F04_auto15_vs_rule1.json 072f9763b3d6843ba833e2ed502d136a7277e6e883b8988ba113871e495d241e R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w4/F05_rule15.json 072f9763b3d6843ba833e2ed502d136a7277e6e883b8988ba113871e495d241e R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w4/G01_rule1.5_live2.0.json 4b12bfa366c1b000699572e5aadc4a6ce258ed95d7578b5c1b77c9437ede1e98 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w4/G02_rule1.5_live1.0.json 6f008e870b84def1958ec8405022e45a2cd3a8dcbb21a6e87fbfc0c6402b3be6 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w4/G03_rule1.6_live2.0.json 4b12bfa366c1b000699572e5aadc4a6ce258ed95d7578b5c1b77c9437ede1e98 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w4/G04_position_clean.json 134080c944f95fb52f0934273f5c639cee96be0a62de18335995907afde71838 R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w4/H01.json 4efab09734c4b10e92f8618a79b1170133aeba5321a05e96f0f74c734f71d3ae R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-45/w1/ScrMistakes/mutants.sh 9ceaced57711238275b6f4e982841e1e0593e42ebf54d789ccd5c67a30f15d1e R1_CLIENT_DUMP kind=fixture
.ufo/waves/round-46/w1/CritW2Gate.md fb43aca9b3d872f05a168170cb82be33fad48a77e8b4b1f6eb786e12e185b003 R1_CLIENT_DUMP,R2_PROC_TABLE,R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-46/w1/CritW2Gate/report.md fb43aca9b3d872f05a168170cb82be33fad48a77e8b4b1f6eb786e12e185b003 R1_CLIENT_DUMP,R2_PROC_TABLE,R3_MONITOR_IDENT kind=fixture
.ufo/waves/round-47/w1/ExecSessionMarker/check-session-material.py a4a0a084e745f511048d5be445bed4959a18b5d64798a55da06c74cc0d08e9c9 R1_CLIENT_DUMP,R2_PROC_TABLE,R3_MONITOR_IDENT kind=gate-copy
```

`wc -l` = 50; each row's sidecar is the file of the same name plus `.synthetic` under `demo/sidecars/`
(the 50th row of `demo/registry-round47-refreshed.txt` is the `round-46/w1/ExecSessionTriage` copy, the
51st the `round-45/w1/ExecPrivacyGate` one, both `kind=gate-copy` at the same sha). Install: (1) the gate over `quality/check-session-material.py`;
(2) `demo/sidecars/` into the lane at its lane-relative paths; (3) `demo/registry-round47.txt` over
`quality/session-material-waivers.txt`; (4) run the gate — the expected output is
`SESSION_MATERIAL_WAIVED: findings=55 files=49` and `findings=84` with the classes of §4
(`13-seat-tree-with-markers.txt` is exactly that run).

`demo/skill-row.md` holds the replacement `SKILL.md` row (same seven columns as `mado-axis-scores`,
`SKILL.md:769`): name `mado-session-material`, the entry command, the exit map 0/1/2, the self-test spelling
`SELFTEST: passed=N/N failed=N`, and the pinned values (summary line, six rule names, marker grammar + registry
row grammar, and `serial-rule-not-waivable`).

## 6. Selftest

`receipts/00-selftest.txt`: **`SELFTEST: passed=63/63 failed=0`**, exit 0. 22 cases are the tracked gate's
(unchanged and all passing), 12 the marker layer's, 23 the serial rule's, 6 new:

| case | what it pins |
|---|---|
| `waiver-serial-rule-not-waivable` | R3 on a marked file is waived, R5 on the *same* file is refused with `serial-rule-not-waivable`, exit 1 |
| `waiver-serial-rejection-is-printed` | the refusal reason reaches stdout, not just the return value |
| `waiver-marker-cannot-name-serial-rule` | a sidecar naming `R3,R5` is `marker-malformed` and R5 still refused |
| `waiver-real-serial-marked-file-kept` | a serial-shaped value outside the reserved namespace keeps R3 (`serial-not-synthetic`) and R5 |
| `prose-serial-unmarked-kept` | the prose rule fires with no waiver system in play at all |
| `e2e-no-rule-can-be-dropped` | `--rules` is an argparse error (exit 2) |

The serial fixtures are assembled from parts at run time, and the selftest asserts on itself that its own bytes
trip neither R5 nor R6 (`self-source-serial-rules-clean`) — so the gate's file can be pasted into a receipt
without carrying a serial.

## 7. Risks, limits, what this seat did not do

- **A marker is a review surface, not a proof.** W1/W3 make abuse visible as a diff in a non-`.ufo` file and W4b
  blocks real values, but a reviewer still has to read the registry row. Declared residual, unchanged from
  round 46: an author who retitles a real window `redacted` and registers the file in `quality/` can waive that
  file's *title* rule — the outcome the policy wants for R1 — while R2/R3/R4/R5 have no equivalent escape
  because identity there *is* the value.
- **R5 is a shape rule** with the round-46 blind spots (lowercase, separators, a capital run of ≤2, a trailing
  run of <3 digits); R6 under `--serial-from-host` is the backstop and needs the host, so an offline run gets
  R5 only. R5 can also flag a non-serial token of that shape (none in this tree: the whole-tree measurement is
  the round-46 serial copy's, re-used unchanged because the pattern is identical).
- **The 6 stale-copy findings are real red at any revision that still holds the old copies.** Refreshing them is
  an integrator decision (it overwrites a round-45/46 artefact that is a copy of the gate, not evidence in its
  own right); both states are measured and both registries delivered. This seat did not touch them.
- **`--serial-from-host` starts one process** (`hyprctl`). It is off by default; the demo uses it only in
  measurements 5 and 8, and the entry command in the SKILL row does not use it at all.
- **The install set is a snapshot**: it names 49 exact blobs at `60edb66`. Any later edit to those files voids
  the waiver by design (`sha-mismatch`), and any new round-47 file that trips a rule needs its own row —
  `demo/triage.py` regenerates the whole set in two passes and refuses to finish unless pass B waives and keeps
  exactly what pass A did.
- This seat did not touch the tracked gate, the counters, the registration, `SKILL.md`, `SCORECARD.md`, the
  lane index or any other seat's file. No judgement on whether the 84 should be redacted or waived by someone
  else — that is the L1's and the owning seats' call.

## 8. Tooling

No installs, no version changes, no pacman. Python 3.14.8 stdlib (`argparse`, `hashlib`, `json`, `os`, `re`,
`shutil`, `subprocess`, `sys`, `tempfile`) and git. Compositor access: exactly one `hyprctl monitors all -j`
read per demo run (the live dump), never a write verb, never a terminal, never a GUI program. Scratch
`/fast/scratch/hyaku/mado-r47/ExecSessionMarker/` (three clones, `$TMPDIR` for the selftest) is deleted at the
end; no receipt cites a `/tmp` or scratch path as evidence — receipts are the gate's own stdout.

## 9. Verification of this seat's own artefacts

- `11-seat-scan.txt`: every serial, description, make and model value from the live dump is counted as a plain
  substring across every file in this seat dir — `hits=0` (the values themselves are never printed).
- `15-no-waivers-parity.txt`: `PARITY ok` — the marker gate with `--no-waivers` prints the same `FINDING` and
  `SESSION_MATERIAL_RULES` lines as the same tree before any marker existed.
- `00-selftest.txt`: **`SELFTEST: passed=63/63 failed=0`**, exit 0.
- `17-claims-check.txt`: **`CLAIMS_CHECK passed=49 failed=0`** — `demo/verify-claims.py` asserts, against the
  receipts themselves, every count and reason text this report quotes, plus the install set's shape (49 rows,
  49 sidecars, the refreshed registry a 51-row superset, every sidecar's sha equal to its row's sha).
- Every locator and number in this report is a line of a receipt named beside it.
