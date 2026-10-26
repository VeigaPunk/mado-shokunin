# mado round 46 — registration (frozen BEFORE wave w1 and before any round-46 data commit)

Base: `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe` (lane `master` at round start; `ahead=0 behind=0`). Date 2026-10-26.
Host: Hyprland 0.56.2 (`efb50993`), hyprlang 0.6.8-5, libxkbcommon 1.13.2-1, xkeyboard-config 2.48-1; 10 keyboards and 4
pointers in `hyprctl devices -j`; `~/.config/hypr/input.conf` holds one `input` block and no `device` block.

Surface the round changes: the **input-device plane** — how the `input` and `device` config of Hyprland 0.56.2
becomes the XKB names a keyboard stores and the scroll factor a pointer reports. At base the lane holds point
readings of `input:kb_layout` only (ground grep `receipts/c2-ground-base.txt`, exit 1 for the per-device chain).

Lowest-axis rule: every published axis ties at its maximum at base (`receipts/axis-base.txt`: `MADO_AXIS:
checked=3 mismatched=0`), so each is a lowest axis; the claims' after-states are their counters' lines.

## C1 — operability (capability acquisition): `tools/mado-devices.py` — `PRED-C1-r46`

- **Contract:** the docstring of `.ufo/waves/round-46/l1-draft/mado-devices.py` (the reference; selftest 48/48; live
  host run `receipts/live-devices-host-l1.txt`: 9 AGREE, 1 VIRTUAL, 4 pointers AGREE, `verdict=OK`, exit 0).
- **Predicate:** the docstring of `quality/counters/c1-r46-devices.py`: clauses a (tool present), s (selftest N/N,
  N >= 30), f (90 fixtures of `quality/counters/c1-r46-fixtures.json`, pinned by sha256, each in three runs: seed 46
  env A, seed 46 env B, nonce env A), i (bubblewrap isolation; repository, the counter's lane and its parent hidden),
  r (no `hyprctl`/`libinput`/`journalctl`/`udevadm` run), g (150 nonce-generated cases judged by the reference pinned
  by sha256 and loaded from the counter's own lane).
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r46-devices.py --repo . --rev <rev> --work <scratch outside /home/vgpnk/Projects/shokunin> [--nonce N]`
- **Before** (base): `fixtures=0/90 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED`,
  exit 1 (`receipts/c1-before-base.txt`). **Target:** `fixtures=90/90 generated=150/150 selftest=ok readonly=ok
  tool=present verdict=TARGET_MET`, exit 0, at the data commit and the round tip, under any nonce.
- **Kill rule:** anything else at the data tip is a miss, reported as an honest stop; no narrowing, no
  re-registration after data. A hole wave `w1` finds before any data commit may re-register as v2 with a new freeze
  and new controls.
- **Controls** (`ctl/run-c1-controls.py` → `receipts/ctl-c1.txt`): the reference must be MET; the base, a stub, the
  round-45 `mado-monitors.py` copied and 20 reference variants V01-V20 (each undoes one modelled semantic: fallback
  verdict, global scroll factor, exact names, brackets, continuation, `##`, virtual, stale, clamp, device-first,
  empty marker, default layout, float32, unsupported, block close, flat device key, variables, tablet owner, verdict
  order, stof prefix) must all be MISSED. A pre-freeze run met V03 (case-insensitive names); fixture
  `case-exact-dump-name` was added before this freeze to separate it.
- **Residuals (declared):** a tool holding a model of the contract is an implementation of it; a tool may detect the
  sandbox by means not varied in environment B; clause g's oracle is the reference, so a contract error shared by
  reference and tool is invisible to it (the non-author reading of the contract against the pins covers it); clause s
  is a printed line.

## C2 — coverage (sourced): `corpus/knowledge/hyprland-input-devices-r46.md` — `PRED-C2-r46`

- **Predicate:** the docstring of `quality/counters/c2-r46-input-device-entry.py` (the round-45 v2 entry counter,
  clauses a-j with T1-T5, re-cut: ten pins under `fetch/` opened 2026-10-26, sha256 in `receipts/fetch-sha256.txt`;
  census line `hyprland input-device default_layout=us fallback_layout=us device_keys=47 scroll_factor_max=100
  json_scroll_decimals=2 virtual_prefix=hl-virtual-keyboard`; 28 surfaces; locator width <= 30).
- **Sources:** new rows S316-S325 (the registry tops at S315 at base). The two cross-scope URL repeats (S317 with
  S162/S303 legacy ConfigManager.cpp, S320 with S158/S307 HyprCtl.cpp) stay W04 census warnings, as in round 45.
- **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r46-input-device-entry.py --repo . --rev <rev>`
- **Before** (base): `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-before-base.txt`). **Target:**
  `admitted=1/1 verdict=TARGET_MET`, exit 0, at the data commit and the tip. **Kill rule:** as C1.
- **Controls** (`ctl/run-c2-controls.py` → `receipts/ctl-c2.txt`): P (`l1-draft/build-pos.py` on a clone of this
  freeze) admitted; C2-BASE, R45-COPY, SHELL, WIDE-RANGE, HIDDEN-LINE, FORGED-PIN, FALSE-URL, PROSE-CENSUS,
  ANCHOR-PAST-EOF, PROSE-CENSUS-SPACED, ROW-SUPERSEDES, FENCE-TABLE, RECEIPT-CONTRADICT, README-IDS all rejected. P is a
  control, not the data.
- **Residuals (declared):** claim-to-quote binding, word-form census contradictions and registry prose cells are the
  non-author reading; clause j binds a locator and a keyword per surface, not the truth of the sentence.

## Separability

C1's counter reads only `tools/mado-devices.py` at REV plus its own frozen fixtures and reference; C2's reads only the
entry, registry, lesson, README and pins. A tool-only tree meets C1 and misses C2; a data-only tree misses C1 and meets
C2 (to be shown by a w1 seat on scratch trees).

## Routed non-claim work (no claim slot; recorded, not scored by C1/C2)

- Round-45 closure (`corpus/lessons/round-45-verifier-spotcheck.md` §6): D1 run the w2 falsification of the round-45
  data inside this round's wave (tool `ee6659b`, entry, gate); D2 correct M45-2's undercount and teach the
  session-material gate a prose serial rule; D3 add the `check-session-material` registry row, triage the 48
  pre-existing findings and mark the synthetic fixtures; D4 the untracked `MutC1Counter/results.json`; D5 the
  `output: null` results note; D6 S290-S297 supersession and the round-44 `w2/ConnCalibration` errata.
- Frontier step: rows S316-S325, census before/after, mined mistakes, sourced claim = C2. Assimilation: a `merge/mado/`
  theme on the input-device plane is checked by a w1 seat; adopted only under §10 gates. considerthese
  `2026-10-26.md` proposal 3 (age count per routed defect) mined into the lesson.

## Wave shape

One v2 wave `w1` (policy v2, band 64-128) carrying build and attack items, >= 25 % attack roles; the L1 holds the
planner seat.
