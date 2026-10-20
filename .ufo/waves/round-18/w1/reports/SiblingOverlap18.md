# SiblingOverlap18 — round 18 (hyaku phase 2), wave 1

**Seat** `MadoR18.SiblingOverlap18` (connector, leaf; no dispatch, no git/jj write, no commit).
**Target** `/home/vgpnk/Projects/shokunin/mado-shokunin`.
**Baseline** `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`; **pre-registration** `d3a0000`;
**HEAD at scan** `d3a0000` (detached). **Scan window** 2026-10-20T15:39–15:52Z.
**Status** report-only: no sibling file edited, no sibling gate run, no tool installed.
**Host pause honoured** — no `pacman`/`yay`/`paru`/`expac`/`pactree`/`checkupdates` (not even
`-Q`/`-Si`/`-Sp`/`-F`), no `sudo`/`systemctl`/`journalctl`/`loginctl`/`hyprctl`/`libinput`/
`wayland-info`/`walker`/`elephant`/`swaybg`/`hyprpaper`/`waybar`/`alacritty`/`hypridle`/
`hyprlock`/`omarchy-*`/`notify-send`, no screenshot or input probe. Config trees were read as
file bytes only; `~/.local/share/omarchy/.git/HEAD` and `packed-refs` were read as bytes.
No OMP transcript was opened: this item does not name one.

---

## Axes named

| Axis | This seat's contribution | Direction |
|---|---|---|
| **adjacency** | Name the owner of each surface the two new notes and the frozen tripwire touch, with a line anchor and a disposition (cite / fence / route). No absorption. | primary |
| **calibration** | Keep host-version and gate-verdict words equal to what the evidence type proves: a `pacman.log` upgrade line is not installed state; a `frozen_match` is not a tool-pinned verdict; a `systemd` restart script is not unit state. | companion, improves |
| **operability** | Name the probe/gate split for `--frozen`; name the pause-violating live default of `mado-verify.sh`; name the sibling harness digest drift. | companion, improves |
| **coverage** | P3/P5 notes stay `surface: P3` / `surface: P5`; no sibling surface is claimed. | neutral, no harm |
| **freshness / depth** | No live probe, no depth claim. | neutral |

---

## 1. Lane map — what MANIFEST actually carries

`MANIFEST.json` has **no top-level `lanes` key**. It carries `roster` (13 entries),
`rounds[]` (361 records at scan) and `minting_rule`/`protocol`/`repo`/`version`.

- Rostered (13): `kasegi`, `kengaku`, `kake`, `kumitate`, `kotoba`, `kagi`, `kama`,
  `audio`, `game-dev-2d`, `game-dev-3d`, `lore`, `revenger`, `kaidoku`.
- `rounds[]` names **23** lane ids: the 13 above plus `chousa`, `kotodama`, `mado`,
  `mori`, `protocol`, `souji`, `tabi`, `tameshi`, `tsukuroi`, `aggregator`.
  The extra lanes are probation mints whose roster row is withheld, plus the two main-repo
  lanes `protocol` and `aggregator`. `mado`
  is one of the probation mints (mint record: "desktop & compositor craft (Hyprland/waybar/walker) …
  Probation >=3 verified rounds; roster row withheld").
- **Delta vs round 17:** `mado` round 17 **is now recorded** (`closure`, `admitted`,
  capability "post-hoc transcript tripwire … probe"). The round-17 SiblingOverlap report
  said it was unrecorded; that statement is now stale. Round 18 is not recorded at scan.
- Ownership is therefore read from each lane's `PROVINCE.md`, never from roster membership;
  an unrostered probation lane still owns declared ground.

**R18 seats whose ground this report maps** (from `.ufo/waves/round-18/w1/spec.json`, 88 items):
`NoteWalker`, `NoteTheme` (scribes), `TwFrozenMode`, `TwFrozenSnapshot`, `TwFrozenSelftest`,
`ReceiptCheck`, `FrozenProvenanceCheck`, `GateRcFix`, `MeasureMutants` (executors),
`SentinelFrozenPrivacy`, `SentinelHostPause`, `SentinelFetchBodies` (sentinels).

---

## 2. PROVINCE heading map actually read

| Lane | File | Headings (lines) | Clause used here |
|---|---|---|---|
| tsukuroi | `tsukuroi-shokunin/PROVINCE.md` (106 L) | `:6` Core · `:35` Adjacent · `:54` Handoff checklist · `:75` Frontier | `:8-13` package/systemd/update-safety; `:27` never installs; `:48` ADJ-03 routes desktop/menu/idle *configuration* to mado |
| tameshi | `tameshi-shokunin/PROVINCE.md` (≈80 L) | `:22` Core/Frontier/Adjacent · `:49` Core r16 append | `:3-16` method + never edits sibling gates; `:30-35` mado `tools/mado-verify.sh` is a read-only primary surface |
| kumitate | `kumitate-shokunin/PROVINCE.md` (28 L) | `:8` Province bands · `:10` Core · `:17` Frontier · `:24` Adjacent | `:3` OMP task/hub + ufo-fsd scripts/runtime; `:17-19` OMP harness contract |
| kagi | `kagi-shokunin/PROVINCE.md` (62 L) | `:8` Surfaces · `:57` Core/Frontier/Adjacent | `:48` `corpus/transcript-scan.sh`; `:44` in SKILL the gate is counts-only |
| souji | `souji-shokunin/PROVINCE.md` (93 L) | `:6` Owns · `:19` Work surfaces · `:26` Refuses · `:38` Adjacency · `:47` Core/Frontier/Adjacent | `:33-35` refuses `~/.config/**`, driver `.ufo/state/`, `.ufo/watchdog.log`; `:36` refuses live lane work products |
| kotoba | `kotoba-shokunin/PROVINCE.md` (≈40 L) | `:8` Core · `:16` Frontier · `:23` Adjacent | skill craft only; `SKILL.md:397` surveys `~/.agents/skills/omarchy/SKILL.md` as a document, not as owned ground |
| chousa | `chousa-shokunin/PROVINCE.md` (≈12 L) | title only | `:3-8` research method, source hierarchy, claim-vs-source verification |
| mado (self) | `mado-shokunin/PROVINCE.md` (18 L) | title only | `:6-12` Owns; `:10-11` omarchy skill is documentation surface, read-only; `:14-16` Refuses |

---

## 3. The three ownership questions

### 3.1 Who owns "omarchy itself"?

**No lane owns the upstream project or the checkout as a product.** Ownership is split by
*facet*, and the split is stable across the fleet:

| Facet | Owner | Anchor |
|---|---|---|
| omarchy **skill documentation surface** `~/.agents/skills/omarchy/` (read-only) and the desktop config plane that sources omarchy defaults | **mado** | `mado-shokunin/PROVINCE.md:6-11`; the gate pins checkout tag/HEAD and skill-vs-HEAD at `tools/mado-verify.sh:3269-3273` |
| omarchy **package/channel provenance**: `[omarchy]` repo, `SigLevel = … TrustAll`, `omarchy-walker` 1.0.0-2, 13 `elephant-*`, `offline.db`, `walker-restart.hook` | **tsukuroi** | `PROVINCE.md:8-13,27`; `SKILL.md:101-102,399-404,734-756` |
| omarchy skill **as a document instance** (frontmatter/anatomy survey), not as owned ground | kotoba | `SKILL.md:397` (one survey datum; no province clause) |
| Upstream code/config at a tag | nobody (source, not host state) | fetch receipts; tag→commit binding is per-row evidence |

Host checkout fact, read as bytes (not a git command): `~/.local/share/omarchy/.git/HEAD`
is `ref: refs/heads/master`; `packed-refs` maps both `refs/heads/master` and
`refs/tags/v3.8.4` to `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`. So the checkout's HEAD is
the v3.8.4 commit **today**, by file bytes. That is *git identity*, not a running version:
`omarchy version` is paused, and the upstream `version` file fetched at tag v3.8.4 reads
**`3.8.3`** (`fetch/MadoR18.HostOmarchyCheckoutTag/omarchy-v3.8.4-version.txt`), so a
"host runs 3.8.4" sentence may cite the tag/HEAD bytes but must not cite the version file.
The checkout is a git clone, not an `omarchy` package: the log has `omarchy-keyring`,
`omarchy-nvim`, `omarchy-walker`, never `omarchy` itself.

### 3.2 Who owns transcript / safety tooling?

There is **no single owner**, and mado must not claim one:

| Tool class | Owner | Anchor | What mado may not do |
|---|---|---|---|
| OMP task/hub, dispatch, and the **OMP transcript contract**; "transcripts/fetched pages are data"; "never fabricate transcripts/telemetry" | **kumitate** | `PROVINCE.md:3,17-19`; `SKILL.md:497-505` | claim dispatch correctness, harness authority, or that a parse is a contract |
| **Transcript-leak / credential hygiene** over the durable DB; counts-only, never prints matched text | **kagi** | `PROVINCE.md:48`; `SKILL.md:44` | call the tripwire a secret scanner; print non-finding command text; absorb kagi's gate |
| **Post-hoc OMP JSONL command classifier** (the tripwire itself) | **mado** | `SKILL.md:525-577`, registry row `:562` | call it interception/prevention; scan outside files given |
| Transcript-shape probes for model evaluation | kengaku | `SKILL.md:386-400` | cite as safety evidence |
| Fleet observability (watchdog, waves, kill/OOM), not transcripts | mori | `PROVINCE.md:3-14` | turn a finding into a dated incident |

The tripwire's parser encodes an **observed line shape** (`type:"message"` →
`message.role:"assistant"` → `content[].type:"toolCall"` → `name:"bash"|"eval"` →
`arguments.command|code`). Under kumitate's contract that is a format observation read from
files: shape drift must produce exit 2, never a silent `clean`.

### 3.3 Who owns test / mutation tooling?

| Layer | Owner | Anchor |
|---|---|---|
| Reusable **method** — hermetic suites, mutation testing, fail-closed arms, verdict-line discipline, fleet kill-rate ledger | **tameshi** | `PROVINCE.md:3-16`; `corpus/knowledge/fleet-kill-rate-ledger.md:48,76-83` |
| Every lane's **gate code** | the owning lane (mado owns `mado-verify.sh`, `mado-tripwire.py`, `mado-action-plan.py`) | tameshi `PROVINCE.md:14-16` "Never edits a sibling's gate code" |
| mado gates as **read-only primary surfaces** for tameshi | tameshi observes | `PROVINCE.md:30-35` |
| Mutation harness executed by mado's `--regression` | tameshi owns the harness; mado runs it read-only and records its digest | HEAD `tools/mado-verify.sh:1641,1854-1866` |

Two consequences for R18:

1. Tameshi's mado leg is **historical**: `fleet-kill-rate-ledger.md:48` records the sweep at
   `d7edaab4…` (1,098 L), the repair at `c4c1afb7` (28 → 53 assertions, 10/10). The current
   `mado-verify.sh` is ~3.4k lines. Do not cite "10/10" or `c4c1afb7` as current; a new
   selftest count must be stated as this round's measurement.
2. `HARNESS_SHA_RECORDED='b56c6e57…'` (HEAD `mado-verify.sh:1641`) no longer equals the live
   sibling harness: `sha256sum tameshi-shokunin/tools/mutate-and-run.sh` =
   `0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa`. The line is labelled
   "provenance, not gated" (HEAD `:1866`), so nothing turns red — but any R18 regression receipt
   must record the digest it actually executed. Do not edit the harness or its ledger.

---

## 4. Walker route note (`corpus/knowledge/walker-route-r18.md`, P3)

The note is not landed at scan; the fetch bodies under `fetch/NoteWalker/` (27 receipts) and
`fetch/SrcOmarchyWalker/` are. Predicted contact `[INF]` from those bodies and the item:

| Sibling | Their ground | Where the P3 note touches it | Disposition |
|---|---|---|---|
| **tsukuroi** | package state and update-safety (`PROVINCE.md:8-13`); never installs (`:27`) | Host versions are read as **`pacman.log` upgrade records**: `:2929` `upgraded walker (2.17.0-1 -> 2.17.2-1)` at 09:16:46, `:3095` `upgraded elephant (2.21.0-1 -> 2.22.1-1)` at 09:31:03. A log line proves a transaction, not the installed set; `pacman -Q` is paused. Phrase as "log record at :2929; installed set `[UNK]`", never "host runs 2.17.2". | cite the log line as a log record; do not interpret channel/provenance |
| **tsukuroi** | `walker-restart.hook` root-exec of a user-owned script, reported to kagi/operator (`SKILL.md:404,427,842`) | `walker-restart.hook` ran at `:3062` (after the walker upgrade) and `:3123` (after elephant). The hook, its packaging, and its privilege question are tsukuroi's finding. | cite as pointer only; never re-own, never run |
| **tsukuroi** | systemd user units and timers (`PROVINCE.md:8`) | `omarchy-restart-walker` calls `systemctl --user is-enabled/restart` on `elephant.service` and `app-walker@autostart.service` (`fetch/NoteWalker/omarchy-v3.8.4-bin-omarchy-restart-walker:6-11`); `omarchy-refresh-walker:5-12` writes `~/.config/autostart/walker.desktop` and `~/.config/systemd/user/app-walker@autostart.service.d/restart.conf`, then calls `daemon-reload` (`:12`). Unit liveness/enablement is tsukuroi's plane. | document the script's route, fenced; no unit-state claim |
| **tsukuroi** | package `swaybg`/walker binaries, `[omarchy]` TrustAll, `omarchy-walker` foreign | The note may describe `walker`/`elephant` upstream at tags v2.17.2/v2.22.1; the installed package, its channel, and the foreign `omarchy-walker` meta are tsukuroi's. | upstream tags are sources, not host facts |
| **kagi** | credential hygiene; the hook privilege question was routed to kagi/operator by tsukuroi (`SKILL.md:427`) | No secret material in walker configs; the hook/TrustAll question is already routed. | no restatement; no claim |
| **chousa** | research method and source hierarchy (`PROVINCE.md:3-8`); mado `SOURCES.md:4` "research method stays chousa's" | The 11-column rows and `used-by` handshake are mado's registry; the method is chousa's. | cite method, own the rows |
| **mado internal** | PROVINCE Owns list (`PROVINCE.md:6-12`) | The walker route reads `~/.config/elephant/` (menus symlinks, provider config) and `~/.config/autostart/walker.desktop`; **neither is enumerated** in Owns. | phrase as read-only joins, or L1 appends to PROVINCE; no sibling claims them |

Two precision traps for the scribe:

1. **Old live note vs new log line.** `corpus/knowledge/walker-live-surface.md:19-24,37-40` records
   `walker 2.17.0-1`, binary sha `64826a85…`, PID/unit `[OBS]` on 2026-10-14 — a pre-pause live
   measurement. The R18 note's `2.17.2-1` is a log record eight days later. Neither proves the
   current installed binary or its sha; keep the old note's tag `[OBS]` historical and the new
   line `[OBS]`-as-log, not as installed state.
2. **Upstream tag ≠ host bytes.** The note fetches walker v2.17.2 sources; the host's
   `/usr/bin/walker` may be 2.17.2 by log but its bytes are unmeasured under the pause. Do not
   carry the R7 sha forward as current.

---

## 5. Theme route note (`corpus/knowledge/theme-route-r18.md`, P5)

Predicted contact `[INF]` from `fetch/NoteTheme/` (17 receipts) and the fetched scripts:

| Sibling | Their ground | Where the P5 note touches it | Disposition |
|---|---|---|---|
| **tsukuroi** | package state; user units; process/service liveness (`PROVINCE.md:8-13`) | `omarchy-theme-set` rewrites `~/.config/omarchy/current/theme`, writes `theme.name` (`fetch/NoteTheme/omarchy-theme-set-v3.8.4.sh:41-45`), calls `omarchy-theme-bg-next` (`:49`), then `omarchy-restart-waybar|swayosd|terminal|hyprctl|btop|opencode|mako|helix` (`:54-62`), then `omarchy-hook theme-set` (`:73`). `omarchy-theme-bg-set` and `-bg-next` run `pkill -x swaybg` and relaunch `setsid uwsm-app -- swaybg …`. These are live process/compositor operations. | document the route, all fenced; no "swaybg is running", no "theme X is live", no restart claim |
| **kagi** | credential hygiene; shape-only | `omarchy-hook theme-set` executes `~/.config/omarchy/hooks/theme-set` and `.d/*` (`fetch/SrcOmarchyThemeSet/omarchy-hook:14-26`). A hook body can contain credential-shaped text. | fence execution; if hooks are read, shape-only and route a hit to kagi; never copy hook bytes into the note |
| **souji** | refuses operator config `~/.config/**` (`PROVINCE.md:33-35`); live lane work products (`:36`) | `~/.config/omarchy/backgrounds/`, `themes/`, unreferenced files are operator config. | no cleanup proposal, no removal; cite paths/modes only |
| **tameshi / kumitate** | none | No gate, harness, or transcript contact in the theme route. | no contact |
| **mado internal** | PROVINCE Owns (`PROVINCE.md:6-12`) | Owns says "themes/wallpapers as declared files", but the route reads `~/.config/omarchy/current/**`, `~/.config/omarchy/backgrounds/**`, and consumer trees `~/.config/{btop,mako,swayosd,helix,opencode}` — **none enumerated**. The item itself asks for the btop/mako/swayosd grep. | join wording ("consumed by …"), or L1 appends; not a sibling claim |

Three precision traps:

1. **The applied theme is a copy, not the upstream theme.** `omarchy-theme-set` copies
   `themes/<name>/*` into `current/next-theme`, then moves it to `current/theme`. An upstream
   theme file's bytes do not prove the host's `current/theme` bytes; the host listing must be
   read separately (the item does).
2. **Waybar restart is conditional.** `:53-54` restarts waybar only `if pgrep -x waybar`; the
   other seven restart calls are unconditional. A sentence "theme set restarts waybar" is
   false as written.
3. **`swaybg` tag v1.2.2 is a source, not an installed version.** One fetch to
   `github.com/swaywm/swaybg/tree/v1.2.2/doc` returned **404** (17-receipt file records
   `http_status:404`); a 404 body is a failed open, not a source. The retried
   `swaybg-v1.2.2-1.scd`/`swaybg-v1.2.2-swaybg.1.scd` bodies are the usable ones.

---

## 6. Frozen tripwire (`tools/mado-tripwire.py --frozen`, C3)

### 6.1 Fleet protocol — the design is protocol-mandated, the registry row is not yet clean

`PROTOCOL.md:375-410` §Gate standard says: a gate's verdict must be re-runnable against
persisted expected values; **two evidences** — a self-test is capability, and a gate whose
verdict depends on a mutable fleet artifact must also ship a run over a committed input
snapshot with a committed expected verdict (`:390-397`); the same bullet requires a frozen
baseline's `expected.json` to pin every input digest, and a tampered input is
`snapshot_tampered` (could-not-evaluate), a baseline without digests `unpinned (legacy)`
(`:395-397`); the registry row fields include one entry command and a pinned-value path
(`:398-406`). The
`--frozen` interface in the R18 contract implements exactly this.

But the declared claim says "the registry row moves `probe` → `gate`", and the current
registry has **one** row:

- `SKILL.md:562` `mado-tripwire` = **probe**, entry `--scan PATH…`, verdict map over mutable
  transcripts. That entry cannot be a gate: a scan over a moving transcript has no persisted
  expected verdict and no digest pin.
- The frozen mode *is* gate-shaped: committed `expected.json`, per-input sha256,
  `frozen_match` 0 / `frozen_verdict_mismatch` 1 / `snapshot_tampered|frozen_error|unpinned_legacy` 2,
  `--selftest` with frozen cases.

**Recommended shape (bounded, L1 decides):** two rows —
`mado-tripwire` (probe, unchanged) and `mado-tripwire-frozen` (gate,
`python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen-tripwire`). If a single
row is preferred, its entry must be the `--frozen` form and its verdict map must say the live
`--scan` usage remains a probe. Moving the existing `--scan` row to `gate` without that split
would misdescribe the instrument.

### 6.2 Sibling contact

| Sibling | Their ground | Contact | Disposition |
|---|---|---|---|
| **tameshi** | mutation method and kill-rate language (`PROVINCE.md:3-16`) | `--frozen` is a **frozen replay**, not a mutation sweep. The suite's missing/extra/tampered cases are controls, not mutations of the classifier. R17-V5's "committed mutant receipt" is a separate bar (the `MeasureMutants` seat). | do not borrow kill-rate; a committed mutant receipt must name the mutant and the killed assertion |
| **kumitate** | OMP transcript contract; transcripts are data (`SKILL.md:497-505`) | The tool parses a line shape; the snapshot pins that shape at copy time. Live shape drift must be exit 2. | no dispatch/harness claim; a scan says nothing about dispatch |
| **kagi** | transcript-leak gate is counts-only, never prints matched text (`SKILL.md:44`) | Snapshot inputs are **byte-exact** transcript lines committed into the lane repo; mado's verdict prints redacted command text for findings (240 chars, `tools/mado-tripwire.py:107,124-126`). Kagi's posture is the opposite for output. | SentinelFrozenPrivacy should confirm no credential-shaped run and no `toolResult`/result payload in the selected lines; a secret-shaped hit routes to kagi, never a redaction inside the input (byte-exactness would break) — reselect the line and document |
| **souji** | refuses driver `.ufo/state/`, `.ufo/watchdog.log` (`PROVINCE.md:33-35`); committed artifacts are lane-owned | Snapshot lives under `.ufo/waves/round-18/`; committed. `.gitignore` `.ufo/state/` is separate (see §7.3). | no cleanup/deletion proposal |
| **kaidoku** | evidence ids, observation/inference/unknown separation (`PROVINCE.md:38`) | `provenance.json` maps each input to source path, source sha256 (equal to the round-17 `session-index.json` where listed) and `[snapshot_line, source_line]`. | cite file/line/digest; a `frozen_match` is a comparison, not a host verdict |
| **mado internal** | prior frozen gates: `mado-frozen-regression` (r13), `…-r14`, `mado-action-plan-frozen` (r16) | The new mode follows the same shape; no shared verifier is reused. | maintainability note only; not a sibling issue |

### 6.3 The residual the frozen contract does not close

`--frozen` output carries `tool_sha256` (sha256 of the running tool file) and
`expected_sha256` (sha256 of `expected.json`), but **no `measured_commit`**:
`tools/mado-tripwire.py:861-866`. A different classifier revision that yields the same
findings can therefore print `frozen_match`, and the frozen baseline does not pin the tool.
This is exactly the R17-V1/V2 gap one layer down ("receipts without tool sha or measured
revision"). Two bounded mitigations, both lane-side:

1. Every frozen receipt must carry `tool_sha256` **and** `measured_commit`, checked by the
   `ReceiptCheck` seat's `receipt-check.py` (the R18 criterion-24 wrapper). Do not treat a bare
   `frozen_match` line as a closure receipt.
2. The gate row's pinned-value path must name both `frozen-tripwire/expected.json` and the
   measured tool revision, so a later reader sees the tool pin and the input pin together.

The tripwire selftest is pure and hermetic: it invokes the tool over fixture
directories and asserts exit/outcome, with no live gate and no host command. That is correct
for this round.

---

## 7. Routed jj-migration fixes — sibling contact

### 7.1 `tools/mado-verify.sh:3406` (JjAuditMado F10) — in flight

At HEAD `d3a0000` the row is:

```
blob=$(tmo git -C "$tree" show "HEAD:$OMARCHY_SKILL_REL" 2>/dev/null | sha256sum | cut -d' ' -f1)
```

with the `-z "$blob"` UNKNOWN arm unreachable because the empty-input digest is non-empty.
The worktree now carries the fix (`git diff tools/mado-verify.sh`): `grc` capture, `pipefail`,
an `OM9` scenario with `STUB_GIT_SHOW_RC=128` asserting UNKNOWN + the path + rc and asserting
**no "local edit"**, and `OM10` for `describe`/`rev-parse` rc≠0 (F6/F14), plus per-verb stub rc
knobs. It also raises the selftest count.

Sibling contact:

- `tools/mado-verify.sh` is a **tameshi read-only primary surface** (`PROVINCE.md:30-35`).
  Tameshi does not edit it and is not asked to re-run its ledger. The mado mutation leg
  (`fleet-kill-rate-ledger.md:48`) is historical at `d7edaab4…`/`c4c1afb7`.
- The fix changes the gate's selftest count and its UNKNOWN semantics. Any external text that
  says "372/372" must be re-cut by mado to this round's measured count; do not pin tameshi's
  old count.
- The `OM9` assertion `st_not_has "local edit"` is the right falsifier; without it the scenario
  would pass on the old wording.

### 7.2 Sibling harness digest

`HARNESS_SHA_RECORDED='b56c6e57…'` vs live `0673d2e5…` (§3.3). It is printed as provenance,
not gated (HEAD `:1866`). A receipt that cites the gate without the executed harness digest is
not reproducible; record both. No sibling edit.

### 7.3 `.ufo/state/` into `.gitignore` (L1)

Already applied in the worktree (`git diff .gitignore` adds `.ufo/state/`; HEAD has only
`.ufo/interactive-sessions/`). Fleet protocol agrees: `PROTOCOL.md:476-478` — `.ufo/state/`
is driver runtime, no lane commit may include it; `PROTOCOL-APPENDIX.md:32` records the past
defect where it was tracked at the fleet root. Lane precedent: `kama-shokunin/.gitignore` and
`kotodama-shokunin/.gitignore` already carry it. Souji refuses the **driver** runtime
`.ufo/state/` and operator config; a lane's own `.gitignore` is the lane's file, so there is
no absorption conflict. No sibling edit.

### 7.4 `scripts/hyaku/jj-lane.sh`

Operator-side fleet script (`PROTOCOL.md:216`: "`scripts/` … remain operator-side"), not a
sibling lane. No seat edits it. Its pathspec-limited commit is the enforcement that keeps
`.ufo/state` out; the ignore line is defence in depth, not a replacement.

### 7.5 Trip hazard: the gate defaults live

`mado-verify.sh` resolves `MADO_VERIFY_LIVE=auto` (`:87`); its live plane depends on `hyprctl`
(`have hyprctl` gate at `:3018`) and calls `omarchy theme current` (`:3284`). Both commands are
pause-forbidden. The round already declares "the existing verifier defaults live and is not run in that mode this
round"; that sentence must be honoured by every seat: use `--selftest` (stubbed `PATH`) or
`--no-live` against isolated roots. A default `bash tools/mado-verify.sh` is a pause breach,
not a harm-watch run.

---

## 8. Contradictions stated, not smoothed

1. **tsukuroi's static package table vs today's log.** Tsukuroi records `offline-exile`
   14 packages at `elephant-* 2.21.0-1` + `omarchy-walker 1.0.0-2`
   (`tsukuroi-shokunin/SKILL.md:734-756`). Today's `pacman.log:3095` upgrades the elephant set
   2.21.0-1 → 2.22.1-1 through a `pacman -U` of yay-cache zst archives (`:3092`), a different
   channel class from `offline.db`; `walker` moves 2.17.0-1 → 2.17.2-1 at `:2929`. Mado must
   not resolve this: the version lines are citeable as log records; the channel/provenance
   classification is tsukuroi's next-round re-derivation.
2. **mado's own walker note vs the log.** `walker-live-surface.md:19-24,37-40` says 2.17.0-1 with a
   binary sha (2026-10-14 live). The R18 note's 2.17.2-1 is a 2026-10-20 log record. Neither is
   current installed state under the pause.
3. **Live gate vs host pause.** The gate defaults live and calls `omarchy theme current` and
   `hyprctl`; the round forbids both. The declared "not run in that mode" is the only
   reconciliation; it must be repeated in the seat handoffs.
4. **Frozen `frozen_match` vs tool identity.** The verdict names `tool_sha256` but not a
   commit; an unpinned tool can produce the same findings. Pair every receipt with
   `tool_sha256` + `measured_commit` (ReceiptCheck).
5. **PROVINCE Owns vs the new routes.** `~/.config/omarchy/**`, `~/.config/elephant/**`,
   `~/.config/autostart/walker.desktop`, and the theme consumers `btop|mako|swayosd|helix|
   opencode` are read by the two routes but not enumerated in `PROVINCE.md:6-12`. No sibling
   claims them; the choice is join wording (like the terminal route's `xdg-terminals.list`) or
   an L1 append.
6. **Tameshi's mado leg is historical.** `d7edaab4…`/`c4c1afb7` (28 → 53 assertions, 10/10)
   describes the round-6 gate; the current gate is ~3.4k lines and the R18 selftest adds OM9/
   OM10. Do not cite 10/10 as current.
7. **omarchy tag vs version file.** The checkout HEAD equals the v3.8.4 tag commit by
   `packed-refs` bytes, while upstream's `version` file at that tag reads `3.8.3`. A host
   "3.8.4" sentence must cite tag/HEAD, not the version file.

---

## 9. Recommendations (report-only; L1 decides)

1. **Notes.** Write host versions as `pacman.log` records with line anchors and keep the
   installed set `[UNK]`; cite `walker-restart.hook` and the `systemctl --user` restart route
   as tsukuroi pointers, never as mado findings. Fence `omarchy-theme-set` /
   `omarchy-theme-bg-*` / `omarchy-restart-*` / `omarchy-hook` / `omarchy-refresh-walker`.
2. **Province.** If the theme route's `~/.config/omarchy/**` and consumer trees are to be
   owned rather than joined, L1 appends them to `PROVINCE.md`; do not silently widen a seat's
   write scope this round.
3. **Tripwire registry.** Split `mado-tripwire` (probe, `--scan`) from
   `mado-tripwire-frozen` (gate, `--frozen`) or make the single row's entry the frozen form
   and declare live scan a probe. Keep the round-17 limits paragraph verbatim beside it.
4. **Receipts.** Every R18 gate receipt must carry `tool_sha256` **and** `measured_commit`;
   `ReceiptCheck` is the mechanical check. A bare `frozen_match` is not a closure receipt.
5. **Privacy.** SentinelFrozenPrivacy checks the selected lines for credential shapes and for
   result payloads before commit; no redaction inside the snapshot (would break the digest).
6. **Run discipline.** Harm watch uses `--selftest`/`--no-live`; no default live gate, no
   `omarchy-*`, no `git` in the omarchy checkout. No sibling gate is run by this lane.
7. **Source rows.** `S0xx-pending` in `FrontierDraft.md` must be replaced with L1-assigned ids
   (S072-S099) before integration, and every credited row's `used-by` must name the note path.
   A 404 fetch (`swaybg/doc`) is not a source.

---

## 10. Limits

- No OMP transcript was read: this item does not name one. The snapshot/privacy findings are
  structural (from the contract, the tool's output fields and the fetch names), not line
  content.
- No sibling gate was executed; no `mado-verify.sh` live mode; no `pacman`/`systemctl`/
  `hyprctl`/`omarchy-*`; no package, unit, process or compositor state was measured.
- The two route notes do not exist at scan; §4/§5 are predicted from the seat prompts, the
  landed fetch bodies and the existing notes, and are marked `[INF]` where they go beyond a
  file byte.
- `tools/mado-tripwire.py` and `tools/mado-verify.sh` are modified in the worktree while this
  report was written (HEAD shas `962919ce…` and the HEAD gate; worktree `593b3aaf…` and the
  OM9/OM10-bearing gate). Final line numbers and tallies must be re-read after landing; this
  report cites HEAD anchors where the worktree is in flight.
- No tool was installed or updated. No file other than this report was written.
