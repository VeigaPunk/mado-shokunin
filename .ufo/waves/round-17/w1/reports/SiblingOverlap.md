# SiblingOverlap — round 17 (hyaku phase 2), wave 1

**Seat:** `MadoR17.SiblingOverlap` (connector, leaf; no subagent dispatch, no commits,
no git/jj mutation). **Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`.
**Baseline:** `27cd06f`; pre-registration `0175f13`. **Scan time:** 2026-10-20.
**Status:** report-only. No sibling file edited, no sibling gate run, no tool installed.
**Host pause honoured:** no `pacman`/`yay`/`paru` (not even `-Q`/`-Si`/`-Sp`/`-Fl`), no
`sudo`, no `systemctl`/`hyprctl`/`libinput`/`hypridle`/`hyprlock`/`alacritty`/`waybar`/
`walker`/`omarchy-*`, no `notify-send`, no screenshots, no input/device probes. Config
trees were read as bytes (`cat`, `grep`, `sha256sum`, `ls` metadata). The OMP session
transcript named in the round context was **not** opened: this item does not name it,
and the contract restricts transcript reads to seats whose item does.

---

## 1. Axes named

The round judges coverage, calibration and operability. This seat can only move
**adjacency** directly; the other axes are companions whose harm must be zero.

| Axis | This seat's contribution | Direction |
|---|---|---|
| **adjacency** | Name each sibling owner with a line anchor, and state what mado retains when its three claims touch that ground. No absorption, no borrowed authority. | primary, improvements only |
| **calibration** | Keep claim labels equal to receipt tokens and keep the two new notes' surface labels exact; flag one avoidable `[UNK]` and one source-id collision. | companion, improves |
| **operability** | One hermetic fixture pair that proves the tripwire's stated input scope (issued calls only), plus registry/handoff placement. | companion, improves |
| **coverage** | P6/P4 notes remain `surface: P6` / `surface: P4`; no new surface, no sibling surface claimed. | neutral, no harm |
| **freshness / depth** | No live probe added; no depth claim. | neutral |

---

## 2. Lane map — what MANIFEST actually declares

`MANIFEST.json` has **no top-level `lanes` key**. It has `roster` (13 entries) and
`rounds[]` (356 records at scan time), where a lane-round record carries
`lane`, `lane_round`, `lanes`, `verdict(s)`, `capabilities_added` and `report`.

- Rostered (13): `kasegi`, `kengaku`, `kake`, `kumitate`, `kotoba`, `kagi`, `kama`,
  `audio`, `game-dev-2d`, `game-dev-3d`, `lore`, `revenger`, `kaidoku`.
- Minted in probation with the roster row explicitly withheld (`rounds[]`, `type: "mint"`):
  `tameshi`, `mado`, `tsukuroi`, `tabi`, `mori`, `chousa` (all 2026-10-14) and `souji`
  (2026-10-18). The mado mint record reads "desktop & compositor craft
  (Hyprland/waybar/walker) … Probation >=3 verified rounds; **roster row withheld**."
- `rounds[]` carries real mado lane-round records through round 16 (`verdict: admitted`,
  capability `finite declared-action classifier …`). Round 17 is **not yet recorded**
  for mado at scan time. The six `round: 17` records present are other lanes' earlier
  numbered rounds (2026-09-29 kasegi/kake plus kumitate/kotoba/kagi in-flight, two
  2026-09-29 corrections, 2026-10-16 chousa, 2026-10-18 kotodama, 2026-10-19 chousa);
  they are not mado round-17 evidence and must not be cited as such.

**Consequence for this scan:** lane ownership is read from each lane's `PROVINCE.md`,
not from roster membership. Unrostered probation lanes still own declared ground.

### 2.1 Heading map actually read (`##`/`###`, line numbers)

| Lane | File | Heading lines (as present) |
|---|---|---|
| kagi | `kagi-shokunin/PROVINCE.md` (62 L) | `:8` Surfaces · `:57` Core / Frontier / Adjacent (round 21) |
| tsukuroi | `tsukuroi-shokunin/PROVINCE.md` (106 L) | `:6` Core · `:35` Adjacent — finding-to-owner handoffs · `:54` Handoff checklist · `:75` Frontier |
| tameshi | `tameshi-shokunin/PROVINCE.md` (66 L) | `:22` Core / Frontier / Adjacent (fleet round 1) · `:49` Core — round 16 append |
| kumitate | `kumitate-shokunin/PROVINCE.md` (28 L) | `:8` Province bands · `:10` Core · `:17` Frontier · `:24` Adjacent |
| kama | `kama-shokunin/PROVINCE.md` (65 L) | no band headings (title only at `:1`); ownership read from Domain/Owns/Refuses/Write-boundary paragraphs |
| tabi | `tabi-shokunin/PROVINCE.md` (21 L) | no band headings (title only at `:1`); prose domain/owns/refuses |
| souji | `souji-shokunin/PROVINCE.md` (93 L) | `:6` Owns · `:19` Work surfaces · `:26` Refuses · `:38` Adjacency · `:47` Core / Frontier / Adjacent (r12) · `:72` Round 13 · `:82` Round 14 |
| kaidoku | `kaidoku-shokunin/PROVINCE.md` (162 L) | `:38` Core · `:73` Frontier · `:95` Adjacent · `:119` Round-4 additions to Core · `:133` Round-4 frontier |
| mado (self) | `mado-shokunin/PROVINCE.md` (18 L) | no band headings; Domain `:3`, Owns `:6-12`, Refuses `:14-16`, Out-of-province `:18` |

---

## 3. The four ownership questions

| Domain asked | Owner | Anchor (file:line) | Owner's own boundary |
|---|---|---|---|
| **Host package updates** | `tsukuroi-shokunin` | `PROVINCE.md:3-13` — domain "host operability & system repair … package state, systemd, drivers/firmware, boot health"; `:8` "pacman state"; `:13` "Update-safety questions: what an -Syu would touch, what pins/holds exist"; `:27` "Never installs, upgrades, or removes packages; never restarts services. Detection and report; the operator remediates." | Idle/desktop **config** diagnosis is routed *to mado* by `PROVINCE.md:48` (ADJ-03); tsukuroi retains "user-manager/unit, package and driver health". |
| **Secrets** | `kagi-shokunin` | `PROVINCE.md:3` domain "secrets & vault ops … credential hygiene evidence"; `:48` `corpus/transcript-scan.sh` — "transcript-leak gate over the durable DB" | `PROVINCE.md:63` treats other lanes' secret-shaped tripwires as "hygiene filters, not vault ops". Kagi owns custody/credential evidence; a lane filter is not merged into it. |
| **Test / mutation tooling** | `tameshi-shokunin` | `PROVINCE.md:3-5` "verification-fixture craft — … hermetic suites, mutation testing, fail-closed arms, verdict-line discipline"; `:7-12` owns the method, not product gates; `:14-16` "every lane's gate remains its own … Never edits a sibling's gate code" | mado `tools/mado-verify.sh` is a registered read-only primary surface at `PROVINCE.md:30-33`; tameshi observes, never edits. |
| **Orchestration transcripts** | `kumitate-shokunin` | `PROVINCE.md:3` "orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime"; `:17-19` Frontier "OMP harness contract (task batch, agent hub, agent discovery)" | `SKILL.md:97` names the "OMP transcript task-oracle" as one of four observation sources; `SKILL.md:275` says the harness captures "agent identities/transcripts/artifacts/failures/timing". Dispatch authority is kumitate's; a lane reader is not. |

Also adjacent, outside the eight named in the item: `chousa` owns the research method and
the source-admission bar (`MANIFEST.json` mint 2026-10-14; mado `corpus/SOURCES.md:4`
already says "research method stays chousa's"), and `mori` owns fleet/host observability
with an explicit refusal of OS state (`mori-shokunin/PROVINCE.md:12-14`).

---

## 4. Claim-by-claim contact with sibling ground

### 4.1 C3 — `tools/mado-tripwire.py` (post-hoc OMP JSONL command classifier)

| Sibling | Their ground | Where C3 touches it | Disposition (report, not absorb) |
|---|---|---|---|
| **tsukuroi** | Package state, update-safety, systemd user units, boot (`PROVINCE.md:8-13`); never installs/restarts (`:27`) | `host_mutation` classifies `pacman -S*/-Sy/-Su/-U/-R/-D`, `systemctl` mutating verbs, `mkinitcpio`, `bootctl`; `package_query` classifies `pacman -Q*` etc. | A finding is **an issued argv observed in a transcript**, not landed host state. Evidence line and `tool_call_id` are the address; `/var/log/pacman.log` is the landed-transaction oracle and is explicitly clean to read in the tripwire interface. Do not read `pacman.log` in the same verdict and call it host verification; do not describe a finding as a partial upgrade. R15-V1 remains operator-owned. During the pause, `--permit package_query` must not appear in a real-transcript receipt (already flagged by `TripwireClassifierJoin.md:117-121`). |
| **kagi** | Credential hygiene evidence; transcript-leak gate over the durable DB (`PROVINCE.md:48`); gate is counts-only and never prints matched text (`SKILL.md:44`) | The verdict's `command` field is transcript-derived text, truncated to 240 chars with `[A-Za-z0-9_-]{32,}` runs replaced by `<redacted>`, and only for findings. | The tripwire is **not** a secret scanner. Its redaction is a bounded hygiene filter, not a credential gate; tokens with punctuation can survive it. Never copy a transcript into the lane; never echo non-finding commands; a secret-shaped hit routes to kagi. `FleetToolScan.md` §3 row 2 already records kagi's gate as shape-prior-art only (SQLite secret shapes, not argv), and §5.1 says do not cite it as a command-tripwire predecessor. |
| **kumitate** | OMP task/hub, dispatch, the OMP harness contract (`PROVINCE.md:3,17-19`); transcript task-oracle (`SKILL.md:97`) | The parser encodes a line-shape assumption (`type:"message"` → `message.role:"assistant"` → `content[].type:"toolCall"` → `name:"bash"|"eval"` → `arguments.command|code`). | The parse is a **format observation read from files**, not the harness contract. Shape drift must produce exit 2 `could_not_evaluate`, never a silent `clean` with `bash_calls: 0`. Do not claim dispatch correctness from a scan. `FleetToolScan.md` §3 rows 5a/5b and its id-reuse hazard (tool_call_id not unique; key on `(file, line)`) are the prior art to cite. |
| **tameshi** | Verification-fixture craft, mutation bar (`PROVINCE.md:3-16`); mado gate registered read-only (`:30-33`) | `--selftest DIR` with `expected.json` cases, per-case lines and a summary is hermetic-suite shape; C1 also uses a seeded red control. | Mado owns the tool and its gate; tameshi owns the reusable method. A case suite with frozen expectations is **not** a mutation sweep and must not borrow tameshi's kill-rate language. No tameshi edit is requested; its Core surface list is not amended by this round. |
| **souji** | Refuses operator config `~/.config/**` (`PROVINCE.md:32-33`); refuses live lane work products (`:36`); protected `.omp/agent` root convention (three souji tools, per `FleetToolScan.md` §3 row 4) | `--scan PATH` may be pointed at `~/.omp/agent/sessions/...`; reports are lane artifacts. | No transcript copy, no `.bak` cleanup proposal, no `~/.omp` write. `--scan` must take explicit caller paths and never default-walk the agent store. A scan finding is a file/line citation; the transcript stays operator state. |
| **kaidoku** | Evidence discipline: observation/inference/unknown separate (`PROVINCE.md:3-13,38`); a-provider-listed tool is available, not held | C3's red anchor and C1's label check both depend on a receipt token being quoted at its measured revision. | A finding is a **classification of observed text**, not a verdict on the host. Cite `measured_commit`, file, line, id; do not promote a tag/source fact to a host fact. No REA surface is involved, so no kaidoku artifact is absorbed. |
| **kama** | Hard write boundary: never writes `~/.config`, `~/.omp`, or systemd units (`PROVINCE.md:45-46`) | Tripwire reads `~/.omp/agent/sessions/**` only. | Read-only, no write. Kama is otherwise untouched (no endpoint, model or dispatch ground). |
| **mori** | Fleet/host observability; reads journal/cgroup as fleet evidence, "never owning OS state" (`PROVINCE.md:12-14`) | A `host_mutation` finding could be mistaken for a dated incident. | It is not an incident record: no timestamp correlation, no victim, no landed effect. Mori would need its own journal window. No mori claim is added. |
| **tabi** | Browser/CDP interaction; secrets shape-only (`PROVINCE.md:3-8`) | None beyond the shared no-secret-text posture. | No contact. |

**The one C2/C3 collision worth naming.** The P6 host bytes contain `omarchy-system-lock`,
`omarchy-system-wake` and `omarchy-launch-screensaver` as **config values**
(`~/.config/hypr/hypridle.conf:2-4,11,15-19`; measured in
`HostOmarchyLockScripts.md` §1 and `HostIdleFiles.md` §1). Under the tripwire interface,
`omarchy-*` whose name contains `launch` is `host_mutation`, and bare `hypridle`/`hyprlock`
are `live_probe`. If any of those strings ever appear as an issued bash/eval command, the
tripwire must flag them; as config bytes they are data and the scanner never reads config
files. The fence is the input scope, not an exception list. Proposal §6(a) makes that
fence fail-able with a red/green pair.

### 4.2 C2 P6 — `corpus/knowledge/idle-lock-route-r17.md`

The note is already careful: `source:` on line 1, `surface: P6` on line 4, no execution,
installed versions `[UNK]` (`:109`), and `:120` lists `pidof`, `systemctl status`,
`loginctl`, `journalctl`, any `omarchy-*` as "not safe under the current pause, and not
used". It does **not** claim a running lock chain.

Where it touches sibling ground:

1. **tsukuroi `PROVINCE.md:48` (ADJ-03)** routes "menu or idle behavior [that] needs
   configuration-level diagnosis" to mado while tsukuroi retains "user-manager/unit,
   package and driver health". The P6 note's autostart fact — `uwsm-app -- hypridle` at
   `~/.local/share/omarchy/default/hypr/autostart.conf:1` — is a **unit/launcher**
   statement. Unit liveness and package version stay tsukuroi's plane.
2. **Historical live observation, not to be restated.** `hyprland-config-plane.md:187-190`
   records a 2026-10-14 probe: `ps` no match and `systemctl --user is-active hypridle` →
   `inactive`, with `/usr/lib/systemd/user/hypridle.service` present. That was a live
   measurement on tsukuroi's plane, made before this round's pause. It may be cited as
   historical `[OBS]` context only; it is **not** current state, and the new note correctly
   leaves "whether hypridle/hyprlock are running now" `[UNK]` (`:124-129`).
3. **P1/P3/P2 package boundary.** `~/.config/hypr/hyprland.conf:4` sources
   `~/.local/share/omarchy/default/hypr/autostart.conf`, which is package-shipped omarchy
   content; `~/.config/systemd/user/app-walker@autostart.service.d` exists, and tsukuroi
   already tracks `omarchy-walker`, its `elephant-*` deps and the `walker-restart.hook`
   root-exec question (`tsukuroi-shokunin/SKILL.md:101,404,427,734-756`). The P6 note does
   not mention walker; the existing P2/P3 notes must not pull tsukuroi's recorded versions
   (`walker 2.17.0-1`, `omarchy-walker 1.0.0-2`) into current claims, because mado's round
   rule keeps host versions `[UNK]` under the pause.
4. **One avoidable `[UNK]`.** `idle-lock-route-r17.md:129` says "which file sources the
   omarchy default autostart is not read here." The lane already holds the answer:
   `hyprland-config-plane.md:42` (`L4 source default autostart.conf`) and the host byte
   `hyprland.conf:4`. This is a cross-note join, not a new source and not a live probe.

### 4.3 C2 P4 — `corpus/knowledge/terminal-route-r17.md`

- **No sibling claims terminal-emulator configuration ownership.** A fleet grep over every
  `*/PROVINCE.md` and `*/SKILL.md` for `terminal` returns prose only: benchmark names
  (kengaku `SKILL.md:36`), tmux/terminal-outcome vocabulary (kumitate, tsukuroi), a
  foreground-terminal diagnostic (kagi `SKILL.md:42`), and a terminal-state section
  (tabi). None declares `~/.config/alacritty|foot|kitty|ghostty`. mado `PROVINCE.md:7-9`
  is the only owner.
- The note already phrases the route as a **join**, not a surface grab: "joined to this
  host's declarations by file bytes" (`:9`), with `~/.config/xdg-terminals.list:3`
  naming `Alacritty.desktop` and `~/.config/alacritty/alacritty.toml:1` as the covered
  config (`:59-70`). The covered surface is the alacritty tree; the selection list is the
  route. `~/.config/xdg-terminals.list` and `/usr/share/xdg-terminal-exec/xdg-terminals.list`
  are **not enumerated** in `PROVINCE.md:7-9`; the note's join wording keeps that honest.
  Recommended: no PROVINCE edit; optional one-clause amendment only if L1 prefers the list
  declared, and it is not another lane's ground either way.
- `.config/alacritty/alacritty.toml.bak.20261003-190229` is present and unreferenced. Souji
  refuses operator config `~/.config/**` (`PROVINCE.md:32-33`), so no removal proposal is
  made or implied. The note already marks it "not referenced by the live file; not read".
- Alacritty package/version remains tsukuroi's package plane; the note keeps the installed
  version `[UNK]` (`:108`). Correct; do not import a version from a source tag.

### 4.4 C1 — calibration / label check

- The label check (`label-check.py`, `ReceiptLabelCheck.md`) is a **probe owned by mado**;
  its shape (seeded red claim + green control, `0/1/2`, per-claim `MISMATCH`) follows
  tameshi's method without requesting tameshi's mutation bar, and follows kaidoku's
  observation/inference separation without claiming its evidence-id discipline. No
  absorption either direction.
- The seeded red claim is correct in kind: `.ufo/waves/round-16/evidence/frozen-tampered.json`
  records `exit: 2` at `measured_commit: 9dcf248993a9622a5b016edec0003187141745d2`; the
  lesson's `snapshot_tampered` sentence is at `corpus/lessons/round-16.md:131-132`. The
  checker needs `line_end: 132` because the basename lands on 132; `ReceiptLabelCheck.md`
  already records that.

---

## 5. Contradictions stated, not smoothed

1. **tsukuroi's recorded host versions vs mado's `[UNK]`.** Tsukuroi's package plane holds
   dated `walker`/`omarchy-walker`/`elephant-*` rows (`SKILL.md:734-756`). Mado's round-17
   pause forbids package queries, so mado must leave host versions `[UNK]`. This is a
   **claim-scope** difference, not a factual conflict: tsukuroi's rows are historical
   measurements; mado may not restate them as current.
2. **kagi's transcript gate vs mado's tripwire.** Kagi's gate is counts-only over an
   SQLite DB and never prints matched text; mado's verdict prints up to 240 chars of a
   finding's command. They share posture, not contract. Merging them would either add a
   SQLite dependency to a stdlib tool or import a command taxonomy into a secret gate.
   `FleetToolScan.md` §3/§5 already reaches this; this report adds only the province line.
3. **`--permit` invertibility.** `--permit host_mutation` or `--permit package_query` can
   make a real-transcript scan exit 0. `TripwireClassifierJoin.md:103-121,165-175` flags
   this. A permitted verdict is not a no-harm clearance, and the `permitted` array exists
   precisely so a reader can see the waiver. Keep permits in fixtures, not in receipts.
4. **The round-17 MANIFEST records are not mado's.** Six `round: 17` records exist for
   other lanes' lane-round counters; mado round 17 is unrecorded. Do not cite them.

---

## 6. Proposed move (one bounded synthesis)

**Name: the action-provenance fence.** Three cheap changes that make the C2/C3 boundary
fail-able instead of asserted, plus one cross-note join. It composes with
`TripwireFixturesCore`/`TripwireFixturesCompound`, `SkillRegistryDraft` and
`FleetToolScan` rather than replacing them.

**(a) Three hermetic selftest cases for `tools/mado-tripwire.py`** (fixtures are JSONL in
the selftest DIR; nothing is executed):

| Case | Fixture content | Want |
|---|---|---|
| `toolresult-text-is-not-a-command` | a `toolResult`/user line whose text carries `sudo pacman -S --needed --noconfirm libinput libinput-tools` | exit 0, no findings — proves only issued tool calls count |
| `quoted-config-name-is-data` | assistant bash call `grep -n 'omarchy-launch-screensaver' ~/.config/hypr/hypridle.conf` | exit 0, no findings — proves a quoted config value is not an issued command |
| `issued-omarchy-launch-is-host-mutation` | assistant bash call `omarchy-launch-screensaver` | exit 1, finding `host_mutation` / `omarchy-launch-screensaver` / line 1 — the red partner of the previous case |

The pair is the point: the same string is clean as data and a finding as argv. This is the
exact collision between P6's config evidence and C3's class vocabulary. It also gives the
"classifies only commands actually issued" sentence in SCORECARD a fail-able control,
which no existing case covers (the round-16 classifier tested a declared plan, not a
transcript envelope).

**(b) One cross-note join in `corpus/knowledge/idle-lock-route-r17.md`.** Replace the
avoidable `[UNK]` at `:129` ("which file sources the omarchy default autostart is not read
here") with: `hyprland.conf:4` sources `~/.local/share/omarchy/default/hypr/autostart.conf`
as recorded in `corpus/knowledge/hyprland-config-plane.md` §3 `L4`. Keep "whether hypridle
is running now" `[UNK]`. No new source row, no live probe, no tsukuroi claim.

**(c) Integration order for the reserved source ids (L1).** The two rows drafts consume
the range exactly, and only in one order:

- P4 `NoteTerminal-rows.md`: `S056`-`S060` mined + `S061`/`S062` rejected = 7 ids.
- P6 `NoteIdle-rows.md`: seven mined rows (`S0xx-pending`) = `S063`-`S069`.

Assigning P6 first would collide with P4's already-hardcoded `S056`-`S060`; each row's
`used-by` must name its note. This is an assignment fact, not a preference.

**(d) Optional, one four-row handoff block** for the round-17 lesson or SCORECARD (L1
owns both). Each row names what mado retains and the forbidden inference:

| Contact | Mado retains | Sibling retains | Forbidden inference |
|---|---|---|---|
| finding vs host state | file/line/id + classified argv | tsukuroi: package, unit, boot state; `/var/log/pacman.log` window | a finding proves a transaction landed |
| verdict text vs secrets | ≤240 chars, 32+ alnum redacted, findings only | kagi: credential hygiene, transcript-leak scanning | tripwire output is a secret scan |
| OMP JSONL read | observed line shape; exit 2 on drift | kumitate: the OMP harness contract | the parse is the contract |
| selftest vs mutation | hermetic cases and count | tameshi: reusable method and mutation bar | a case suite is a mutation sweep |

**Affected axes.** adjacency improved (explicit, testable fence; no absorption);
calibration improved (one fewer avoidable `[UNK]`, exact source-id order, label remains
receipt-bound); operability improved (three cases, no new dependency, exit 2 preserved);
coverage neutral (P6/P4 labels unchanged); freshness/depth neutral. No axis harmed.

---

## 7. Risks

1. The fixtures contain live command names (`omarchy-launch-screensaver`, the round-15
   `sudo pacman -S` string). They must stay **inside JSONL data**; never copy a fixture
   line into a shell. The selftest invokes only the scanner.
2. `--permit` can hide the red anchor. Keep `permit` out of real-transcript evidence; a
   `clean` with `permitted: ["host_mutation"]` is not a clean receipt.
3. The 240-char truncation and 32+ alnum redaction are not a secret gate. Do not put a
   credential-bearing command in a fixture or a report.
4. Adding cases changes the selftest tally; the SCORECARD/SKILL row must cite the new
   `n/n`, not the old 52/52 (`mado-action-plan`'s count, a different tool).
5. The P6 `[UNK]` closure must cite the P1 note's measured line and its round; it must
   not be written as a fresh host measurement.
6. The historical `hypridle inactive` observation is 2026-10-14 and used a `systemctl`
   query this round forbids. Cite as historical only.
7. `~/.config/xdg-terminals.list` is outside `PROVINCE.md:7-9`'s enumeration. Keep the
   note's join wording; do not silently widen the declared surface.
8. Do not copy any OMP transcript into the lane, and do not propose removing
   `~/.config/**` backups: souji refuses operator config.

---

## 8. Verification for L1 (once, after integration)

All read-only; no `pacman`, `sudo`, `systemctl`, `hyprctl`, no transcript copy.

1. `python3 -I tools/mado-tripwire.py --selftest DIR` → `SELFTEST_SUMMARY: n/n passed
   failed=[]`, exit 0; output contains the three case names above and the red partner's
   `host_mutation` / `omarchy-launch-screensaver`.
2. `python3 -I .ufo/waves/round-17/label-check.py` → seeded red `MISMATCH`, green `ok`
   (already produced by `ReceiptLabelCheck.md`; re-run only if the claims file changes).
3. `grep -nE '^(source|surface):' corpus/knowledge/idle-lock-route-r17.md
   corpus/knowledge/terminal-route-r17.md` → `surface: P6` / `surface: P4`, source lines
   inside the first 15 lines.
4. `grep -nE '^\| S0(5[6-9]|6[0-9]) ' corpus/SOURCES.md` → 14 rows, all `A` + `mined`
   (or explicitly `rejected`), each `used-by` naming its note; P4 rows first.
5. `python3 .ufo/waves/round-17/measure.py REV` → 4/6 for rubric V; U stays 7/7.
6. `grep -nE 'omarchy-(system-lock|system-wake|launch-screensaver)' corpus/knowledge/idle-lock-route-r17.md`
   → only config-value/table contexts, no imperative sentence.
7. `grep -nE 'app-walker|walker-restart|walker 2\.' corpus/knowledge/*.md` → 0 new hits in
   round-17 notes (no unit/version claim imported from tsukuroi).
8. `git status --porcelain` on the lane only; no sibling repo touched.

---

## 9. Scope and tooling record

- Wrote only this report. No sibling file, no lane product file, no draft, no commit, no
  `jj`. No subagent.
- Read: `MANIFEST.json` (roster, mint and lane-round records), the eight sibling
  `PROVINCE.md` files plus `mori`/`chousa` headings, the named sibling `SKILL.md` ranges,
  mado `PROVINCE.md`/`SCORECARD.md`/`SKILL.md`/`SOURCES.md`/`QUALITY.md`, the round-16
  lesson and verifier closure, the round-16 tamper receipt, the round-17 spec/items and
  the wave-1 peer reports named above, and host config bytes under `~/.config/hypr`,
  `~/.config/alacritty`, `~/.config/xdg-terminals.list`, `~/.local/share/omarchy/default/hypr`
  and the `~/.config/systemd/user` file list.
- Not read: the OMP session transcript (item does not name it), `~/.omp/agent/agent.db*`,
  any credential/auth/oauth file.
- Tools installed or updated: **none**.
