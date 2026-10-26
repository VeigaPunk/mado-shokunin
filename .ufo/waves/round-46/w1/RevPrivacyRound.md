# RevPrivacyRound — round-46 privacy review (final)

Seat: RevPrivacyRound (leaf; no subagents, no background jobs). Scope:
`.ufo/waves/round-46/` (receipts/, l1-draft/, fetch/, ctl/, wave plumbing) and
the seat dirs under `w1/`, against SKILL.md rule 4 and the lane's mechanized
gate. Mirror of this file at `w1/RevPrivacyRound/report.md`.

## Rule basis applied

- SKILL.md:33-34 — secrets and session material (window titles, `hyprland.log`,
  instance signatures) are shape-only, never content-read.
- SKILL.md:343 (rule 4) — `clients` for length/tags, never titles; no
  `/proc/*/environ`; `HYPRLAND_INSTANCE_SIGNATURE` never printed in full.
- `quality/check-session-material.py:17-40` — gate rules R1 (clients dump with
  title), R2 (`ss` process-table rows), R3 (monitor serial + description/make/
  model), R4 (>10 bare `/home/...` lines).
- Operator round rule (goal + registration.md): allowed reads `hyprctl version |
  devices -j | monitors[-all] -j | getoption`; the host monitor's serial is never
  written anywhere ("the serial", file:line only).
- Precedent: M45-1 (`corpus/lessons/round-45.md:44-47`) — live titles tracked in
  round-43 were a violation; `ExecSessionTriage/triage.tsv` is the historical
  ledger (round-46 owns no row there yet).

## Findings by severity

### MEDIUM — F1: rule-4 letter breach: live `/proc/<pid>/environ` read, live PID committed

`w1/ExecXkbCompile` read the running compositor's environ for the XKB parity
check. Evidence:

- `w1/ExecXkbCompile/env-root-sensitivity.txt:1` — "environment names present in
  the compositor's process environment (names only, no values)"; lines 2-4 list
  `HOME=`, `XDG_CONFIG_HOME=`, `XKB_name_count=0`.
- `w1/ExecXkbCompile/report.md:86` — "The compositor's `/proc/1622/environ` is
  readable" — the receipt names a live process identity (the host Hyprland PID).
  Lane precedent treats the host Hyprland PID as a redaction gap
  (`w1/ExecSessionTriage/triage.tsv` round-37 rows: "the host Hyprland pid ...
  reused (redaction gap)").

SKILL.md:343 says "no `/proc/*/environ`" — the file was read; the rule has no
names-only carve-out. Mitigations observed: names-only projection, zero values
retained, and the seat itself sets the correct forward boundary
(`report.md:93`, `:125`: a future `--xkb` mode "must not read the compositor's
/proc environment"). No secret content and no environ value is in the tree
(verified: `HOME=/`, `XDG_RUNTIME_DIR=`, `WAYLAND_DISPLAY=` sweeps hit only
`/fast/scratch/...` paths). Recommended disposition: L1 appends one erratum/lesson
line (read was rule-barred; names-only; PID to be cited as "the compositor
process"); no data mutation needed; do not re-read the file.

### RULING — F2: input device product names and the IME process name in `hyprctl devices -j`

**Ruling: not session material under the lane's own rule. Retaining them in
round-46 receipts is authorized. One lane-document tension to record.**

1. Text and machinery. SKILL.md:343 and gate R1-R4 enumerate: clients titles,
   hyprland.log content, `/proc/*/environ`, HIS, `ss` process rows, monitor
   serial+identity, home listings. Device names appear in none.
2. Category. `hyprctl devices -j` names are static hardware inventory
   (lower-cased, punctuation-normalized kernel/HID strings — entry.md step 7,
   `Hyprland-MiscFunctions.cpp:777-789`). They do not vary with use, reveal
   current activity (contrast R1 titles), carry pids (contrast R2), or identify
   the session instance (contrast HIS).
3. The IME case. `hl-virtual-keyboard-fcitx5` embeds the input-method client's
   process name because the virtual-keyboard protocol names the device that way
   (entry.md step 6, `Hyprland-protocols-VirtualKeyboard.cpp:11-30`). The device
   name is inventory; the IME's process row (pid, environ) would be barred R2 /
   rule-4 material. Verified absent: no fcitx5 pid or process row anywhere in
   round-46.
4. Precedent and authorization. Device names have been tracked in the lane since
   round 3 (`config-health-report-r3.md:413` records `power-button ×2,
   hl-virtual-keyboard-fcitx5`, quoted by `w1/CritPremise/receipt.txt:6`), the
   gate has never flagged them, and the freeze itself (commit 8c5434c, verified
   via `git ls-tree`) committed `receipts/live-devices-host-l1.txt` with the
   full 14-name inventory. The entry draft grounds its route in the r15 lesson's
   own verdict line (`input-debugging-boundaries-r15.md:73`: "Policy/inventory
   evidence, not input delivery" — `w1/CritPremise/receipt.txt:8-9`).
5. Tension to record, not a finding against round-46. The same r15 row says
   "omit device identity and all session material before retaining any future
   result" — round 46 retained device identity under explicit operator
   authorization (registration C1 contract + allowed-verb list). The L1 should
   reconcile r15:73 with this round's practice (one sentence in the lesson or
   entry), so the lane's documents do not contradict.
6. Residual (recommendation only). The retained inventory is host-fingerprint
   material: it reveals a hardware security key is present
   (`yubico-yubikey-otp+fido+ccid`), specific peripherals (Razer DeathAdder V2,
   HyperX Alloy Origins Core), and the IME framework in use (fcitx5). None of it
   is activity data; all of it is stable across sessions and hotplug-sensitive
   (SKILL.md:467). Acceptable here; future non-input rounds should keep r15's
   omit-identity default.

### LOW / no action — F3: user config-path enumerations

`w1/ExecLiveHost/runs.txt:286-304` (19 rows of `/home/vgpnk/...` config paths
with per-file exit/verdict), `w1/ScrSkill/receipts/host-runs.txt:47-49`, and
ScoutOmarchyInput's report enumerate which host config files exist. These are
decorated table rows, not R4 bare-path listings; the paths are the lane's
declared read-only substrate and already canonical in SKILL.md. No action.

### CLEAN — F4: negative sweeps over the whole round-46 tree

Sweep patterns and results (scan horizon: 2026-10-26, before this report):

- `"title": "` / `"initialTitle": "` → only upstream pin format strings
  (`fetch/Hyprland-HyprCtl.cpp:403,405`) and synthetic fixtures/gate selftests
  (`w1/CritW2Gate/repro.py`, `w1/ExecSessionTriage/check-session-material.py`,
  `w1/ExecSerialRule/gate.py`, `w1/ExecSessionTriage/demo/run-demo.sh:55` —
  planted fake "inbox (3) - mail", pid 4242, in a scratch clone script). No real
  title anywhere.
- `"serial"` → only pins, synthetic monitor fixtures (`"SN9"`, `"SERIAL0123456"`,
  `"SN00000"`), and gate code. ExecW2Monitors verified compliant: the live
  receipt projects the host output to nine fields with an explicit no-serial
  header (`w1/ExecW2Monitors/live-runs.txt:4-5`), adversarial dumps are synthetic
  with a privacy header (`adversarial.txt:1-3`); its claim to me by message
  matches the files. The known real serial copies are pre-existing round-32/37
  history owned by the D2 route/operator note
  (`corpus/lessons/round-45-verifier-spotcheck.md:105-109`).
- `users:((` / `/proc/` / `HYPRLAND_INSTANCE_SIGNATURE` → only the F1 hit and
  synthetic constants (fixture HIS `mado-r46-fixture`,
  `w1/ExecDoNothingC1/A-lookup-verify.py:68` — good practice). `B-readoracle.py`
  prints env values at runtime but its output is receipted nowhere in the lane.
- `^/home/` / `^total` / `^drwx` → no bare home listing; the one `ls -l` receipt
  (`w1/ScrErrata/receipts/d4-results-retention.txt:3-7`) lists three lane-repo
  files (D4 bookkeeping), not a home directory.
- Credential shapes (`ghp_`, `github_pat_`, `AKIA`, `xox[abp]-`, `PRIVATE KEY`,
  `hf_…`) → zero hits.
- `fetch/` pins: zero `/home/` paths.
- Raw `hyprctl devices -j` dumps: never committed — every `"keyboards": [`
  occurrence is a synthetic fixture (addresses `0x1`, names `kbd-1`, or generated
  vendor/model universes, e.g. `w1/ExecIndepA/gen-fixtures-receipt.py:10-13`);
  `w1/ExecLiveHost/` holds four files, all projections (`dup-main.txt` works from
  scratch-resident dumps by name only).

## Residual risk and verification gaps

- Live wave: seats were still writing during the scan (ExecSeedSweep-3,
  CritC1Cheat-3, ExecHyprlangOracleB, ExecSerialRule-2, ExecDataRehearsal,
  ExecW2Monitors finalization). Everything present at scan time is covered;
  receipts landing after this report are not.
- Historical REAL material outside round-46 (round-35 R4, round-37/38 R2 ss
  tables, round-43 R1/R4) is owned by the D3 triage route
  (`w1/ExecSessionTriage/triage.tsv`), not re-litigated here.
- One tool anomaly, reported to `xd://report_issue`: a grep with an explicit
  `fetch/` root returned three files that do not exist under it
  (MERGE-REPORT.md, absent-defect-register.md, registration.md elsewhere);
  re-verification (narrowed pattern + globs) confirmed the fetch pins clean.
- No installs were made; no host service, compositor state, or config tree was
  touched; all work was read-only scanning plus these two report files.
