# mado round-4 record — scribe prep DRAFT (SCR-M)

Draft v2 window: 2026-10-14 16:19–16:34Z (local 13:19–13:34 −03:00). Lane SCR-M.
This file is scribe scratch product for the round-4 finalizer — **not the
record**. Nothing outside this file was written by this lane in the repo.
Working tree at v2 time (measured 16:28Z): ` M SKILL.md`,
` M corpus/knowledge/config-health-report-r3.md`,
` M corpus/knowledge/hyprctl-verification-layer.md`,
` M corpus/knowledge/waybar-walker-plane.md`,
` M corpus/knowledge/waybar-walker-semantics.md`,
`?? corpus/knowledge/idle-lock-plane.md`,
`?? corpus/knowledge/province-accuracy-selfaudit.md`,
`?? plans/round-4.plan.md`, `?? plans/round-5.plan.md`; HEAD
`f9f58c0efd5daedf7d29036478d17e5b42f26822`. Round-4 work is uncommitted —
landed-means-committed is the round commit's job.
All probes were read-only (hyprctl read verbs, pgrep/ps, systemctl/journalctl
`--user`, loginctl, file reads); scratch `/tmp/w4-scr-m/`.

Reading key: **⟨PENDING⟩** = must be resolved at finalization; every other
number names the command that produced it at v2 time. Counts on `.md` notes
here use `wc -l` (notes end without a trailing newline; editor view = +1).

## 0. Round-4 frame

- Plan: `plans/round-4.plan.md` (ufo-round-plan-v1, untracked at v2 time).
  Axis move: **calibration** — close the two open SHONEN boxes with NAMED
  NON-AUTHOR VERIFIERS (integrator-dispatched review seats count; self-attestation
  does not). Anti-claim: any non-reproduction or province violation keeps the
  box open and says why. Measure: 2 named verifier attributions in SHONEN.md
  with evidence pointers.
- Box mapping (prevents misgrade): the plan numbers boxes 3 = e2e task and
  4 = PROVINCE accuracy; in SHONEN.md order these are item 2 ("At least one
  end-to-end domain task executed and logged in LOG.md") and item 4 ("No
  cross-domain bleed (PROVINCE.md still accurate)").
- Verifier seats: **VER-M3** closes the e2e box (verdict filed 16:23Z —
  REPRODUCES, §3); **VER-M4** closes the PROVINCE box (audit seat; its input
  `corpus/knowledge/province-accuracy-selfaudit.md` landed ~16:25–27Z; its
  verdict ⟨PENDING⟩ at v2).
- Current SHONEN.md (unchanged in tree; 12 L by `wc -l`, sha256 `f6495fe68f42…`):
  boxes 1 & 3 `[x]` via MADO-R3-4; boxes 2 & 4 `[~]` lane-asserted.
- Adjacent (not this round's content): `plans/round-5.plan.md` (69 L,
  untracked; written 16:22Z by a concurrent lane) plans the operability move —
  a committed, self-testing census gate `corpus/scripts/verify-plane.sh`; its
  companion errata list is mostly applied already by ERR-M (§1 D6).

## 1. Deliverables measured at v2 time

D1 — MADO-R4-2, idle-lock plane note: `corpus/knowledge/idle-lock-plane.md`
- As authored: `wc -l` → 355 (editor 356; no trailing newline); 21,540 B;
  sha256 `a8f9cf4d7d81e97…`; mtime 16:10:07Z.
- ERR-M sweep appended an E2 block at ~16:26Z: current `wc -l` → **381**;
  sha256 `a0597be96c107799…` (still no trailing newline; append diff
  `/tmp/w4-err-m-sweep/append-idle-lock-plane.diff`). Record the authored
  measure as the lane's deliverable and the appended block as ERR-M's.
- 14 `##` sections; tables `grep -c '^|'` → 39 = 4×(header+separator) + 31
  data rows (§2 file table 3; §2b actuator table 11; §5 chain table 10;
  §6 hyprctl option table 7); §11 8 unknowns; §12 3 spot-checks.
- Content anchors: three config files (765 B/19 L `hypridle.conf`,
  742 B/43 L `hyprlock.conf`, 176 B/5 L theme `hyprlock.conf`) byte-identical
  to the shipped Omarchy payload by sha256 identity (provenance without
  executing the refresh script); 11 actuator scripts + 2 payload files
  measured (§2b); line-anchored declared chain 150 s screensaver / 152 s lock,
  ≈302 s effective per the file's own reset rationale (§5); lock/wake
  side-effects script-defined (DPMS ≈3 s after lock; wake restores); §6 seven
  Hyprland option semantics (only wake half + session-lock protocol live in
  the compositor; no idle timer); §7 runtime snapshot with **live idle-state
  transitions UNKNOWN by constraint** (§0 operator-presence margin);
  §8 toggle/indicator surface (stateless process toggle; screensaver flag
  absent → enabled); §9 hardware deps (no backlight devices; kbd-brightness
  steps inert; DPMS half works); §10 errata; probe scratch
  `/tmp/mado-r4-2-probe/`.
- Boundary: probe window 16:00–16:08Z; writes = note + scratch only; no
  hypridle/hyprlock start/stop, no DPMS, no idle interval waited.

D2 — MADO-R4-1, reviewer pack: `/tmp/mado-r4-1-probe/repro-r3.sh` (scratch, ephemeral)
- `wc -l` → 389; 23,743 B; sha256 `70dff755278d1dc3`; read-only; embeds
  `expected.tsv` (57 data rows); `D=` redirect.
- **VER-M3 found 3 defects in it** (§3): D1 fatal awk escape (line 261
  `print \$1` in an ordinary shell line → `options.list` empty → false
  "checked 57; mismatches/missing: 57"); D2 `summary.txt` binds line reads
  the workspaces `n= 1`; D3 the `.config/autostart/walker.desktop` pin is a
  16-char prefix compared against full 64-char hashes → guaranteed
  PIN-DIFF. Fixed copies exist: `/tmp/w4-ver-m3-repro/repro-r3.fixed.sh`
  (run2 → 57/0) and the M4-1 repro lane's fixed run `/tmp/w4-m4-1-repro/`
  (`summary.txt`; `summary.buggyrun.txt` keeps the buggy run). **Do not
  quote the pack's as-delivered summary as reproduction evidence — quote
  the fixed run.**
- Durable half (per SKILL §"Reproduction package"): the notes themselves —
  `corpus/knowledge/config-health-report-r3.md` §0–§11 + Appendix A.

D3 — MADO-R4-4, the lane's own re-run: `/tmp/mado-r4-4-repro/` (scratch)
- `run.log`: full chain rc 0; "options in expected.tsv: 57"; class census
  `{'agreement*': 6, 'agreement': 46, 'live-default': 4, 'extra': 1}`;
  **"checked 57; mismatches/missing: 0"**. 21 entries incl. `getoption/`
  (57 captures). Stamp 16:09Z (SKILL :324) — **before** the 16:11Z session
  restart (§2).

D4 — audit support (PROVINCE), v2 — the input has landed:
- `/tmp/mado-r4-3-1-prov/`: `probe.log` (round commit timestamps: `74d3b7b`
  09:50:45, `65a2254` 10:36:02, `e1e1bb7` 11:19:13, `f9f58c0` 12:52:00 local)
  + `animations.json` (5,327 B, live `hyprctl -j animations` capture).
- `/tmp/w4-m4-3/`: audit-support logs (12 files incl. `sweep.log`,
  `live-checks.log`, `boundary-mtimes.log`, `r3-attribution.log`,
  `surfaces-extra.log`, `repo-scope.log`, `omarchy-probe.log`,
  `logs-and-id.log`, `final-live.log`, `state-and-toggles.log`,
  `verify-deliverable.log`, `gitmech/`).
- **`corpus/knowledge/province-accuracy-selfaudit.md` LANDED** (found by
  VER-M4's poll at elapsed=361s of its 25-min cap): 17,190 B; sha256
  `f81f19dbad6fdf63…`. ⟨PENDING: VER-M4's verdict after auditing it;
  finalizer adds a README coverage row for this file and resolves the lane
  attribution (audit lane's product vs audit seat's input — both readings
  agree it is the box-4 evidence object).⟩

D5 — SKILL.md round-4 edits (authoring lanes not self-labeled; ≥2 editors)
- v1 measure (16:22Z): +32/−4 → 424 L by `wc -l`, sha `05969025dc82…`.
- v2 measure (16:28Z): **+57/−5** → **448 L**, sha `46c7c5261f9c02b4…`;
  6 hunks. New since v1: "## Promotion-box status — what remains"
  (SKILL ≈:426-447, "State measured 2026-10-14 16:25Z") pinning the verifier
  inputs — box e2e: reviewer re-run scratch `/tmp/w4-m4-1-repro/`
  (16:21/16:24Z, 57/0) + the pack pointers; box PROVINCE: `PROVINCE.md`
  (18 L) + audit scratch `/tmp/w4-m4-3/*.log` + the awaited
  `province-accuracy-selfaudit.md`.
- v1 contents stand: idle-timings row updated (F1 + MADO-R4-2 refs); tray
  bus name fixed `fr.arrouillard…` → `fr.arouillard…` (round-3 observation
  (b) applied — `grep -c arrouillard` → 0, `arouillard` → 2); idle/lock row
  rewritten + sunset/xdph row split; "Reproduction package — re-run the
  round-3 end-to-end pass" section (both packages + epoch caveat); new trap
  row "Will the session lock after idle?".
- ⟨PENDING: freezing sha at the round commit; authoring lanes.⟩

D6 — ERR-M, round-4 errata sweep (concurrent lane; "ERR-M" self-label)
- Applied the long-pending errata as append-only blocks; read-only probes
  16:20–16:25Z; scratch `/tmp/w4-err-m-sweep/`: `config-health-report-r3.md`
  (E2 tally corrigendum 6×→7× S3 + E3 environment turnover; 550 → 587 L),
  `hyprctl-verification-layer.md` (E2 — closes §9's orphan-`envs.conf`
  candidate; 280 → 302 L), `waybar-walker-plane.md` (R4-E1–R4-E7 = the 7
  R3-1 §8 candidates + R4-E8 provenance corrigendum; 364 → 474 L),
  `waybar-walker-semantics.md` (E1 pointer to the application; 455 → 462 L),
  `idle-lock-plane.md` (E2 post-probe turnover; 355 → 381 L).
- `git diff --stat` at 16:27Z: 5 files, +192/−9 (includes SKILL's share by
  a different lane).

## 2. Live-substrate drift during round 4 (v2 — corroborated by three lanes)

`[OBS]` **The Hyprland session was replaced at 16:11:06–07Z (local 13:11), mid-round.**

- New runtime dir `…efb50993…_1791994267_1144437716` (hyprland.lock mtime
  16:11:08Z) beside the old `…_1791900126_343764660` (lock mtime 2026-10-13
  11:02:08 local); `hyprctl -j instances` → one instance, pid 1203316,
  `wl_socket wayland-1`; system boot unchanged (2026-10-13 11:02) — a
  session restart, not a reboot.
- New PIDs (all `ps -o lstart` 13:11:06–07 local): Hyprland 1203316,
  waybar 1203352, swaybg 1203358; mako 1203350, walker 1203471, swayosd
  1203475 (VER-M3). Old-session PIDs (rounds 1–3 and the idle note's §7
  window): Hyprland 1671, waybar 1707, wallpaper 1710.
- `[OBS]` **hypridle started at session start via the declared autostart**:
  journal (local) `uwsm_app-daemon[1203477]: received: app -- hypridle` /
  `sent: exec systemd-run … --unit=app-Hyprland-hypridle-87ed9048.scope …
  -- hypridle` / `systemd[1203171]: Started hypridle.` at 13:11:08; PID
  1203349, ppid = 1203316 (Hyprland) — a session app-scope child, never the
  systemd unit. Live confirmation of `default/hypr/autostart.conf:1`
  `exec-once = uwsm-app -- hypridle` (note §3).
- `[OBS]` hypridle present 16:21:49Z (ERR-M) and 16:22:53Z (this lane),
  **absent by 16:23:19Z** (ERR-M) / 16:23:41Z (this lane): `pgrep -x
  hypridle` rc=1; `ps -p 1203349` empty; scope unit GC'd (`--collect`);
  `systemctl --user is-active` `inactive` / `disabled` throughout — only the
  `pgrep` half discriminates. `flap.log`'s scope list at 16:23:34–38Z shows
  no hypridle scope. Exit cause `[UNK]`; silent in the journal.
- `[OBS]` clients 3 → 2 (Alacritty 1204373/1205237), both still carrying
  `['default-opacity*','terminal*']` — F2 reproduces on the new session's
  windows (the old clean-tag window is simply gone; window set is
  epoch-varying); `hyprctl -j layers` → no lock surface; `pidof hyprlock`
  rc=1; sessions now 4 (user, tty2) + 5 (manager) — old session gone.
- `[OBS]` Config bytes unchanged across the restart: VER-M3's §A sweep
  29/29 OK; `hyprland.conf` sha256 `4f52854a3c143dcf` still holds; ERR-M
  re-hashed the idle/lock pins equal.
- Cause of the restart: `[UNK]` (unattributed `__cxa_call_terminate` traces
  13:09–13:11 local near the boundary; not investigated further).

Implications for the record:
1. `idle-lock-plane.md` §7's snapshot is era-correct for its 16:00–16:08Z
   window; the absent state is **transient-but-recurring** (old session:
   rounds 1–3; new session: present ~12 min after start, then absent again).
   Draft v1's E2 candidate is **moot — ERR-M applied its own E2 block**
   (`/tmp/w4-err-m-sweep/append-idle-lock-plane.diff`); the record should
   reference that block, not restate it.
2. F1 (S1, R3-2 §6) text must be era-scoped; VER-M3's verdict states it
   correctly ("the F1 absence observation cannot be re-observed in this
   session — the state changed by design — but the mechanism F1 named is
   confirmed"). Do not grade a naive "does not reproduce".
3. Reproduction semantics held across the restart: stable pins + the
   57-row check (VER-M3 §A/§B; corrected pack runs 57/0). Epoch values
   changed — exactly the SKILL's caveat.
4. Second data point for the daemon pattern: boot-start Oct 13 11:02:09 →
   absent by round 1; start 16:11:08Z → absent by ~16:23:20Z.
5. Three independent recorders (this lane, VER-M3, ERR-M; AUD-M1's verdict
   referenced by ERR-M) agree on the turnover and PIDs.

## 3. SHONEN box attributions VER-M3 / VER-M4 will earn (v3 — both verdicts filed)

Mark rules (PROTOCOL.md:419-431): marks confined to the box character plus
ONE indented evidence line per box; `[x]` only with a named non-author
verifier.

State as of v3.1 (16:36Z) — **both boxes close on named non-author verdicts**:

```
- [x] At least one end-to-end domain task executed and logged in LOG.md
  VER-M3 (non-author reviewer seat) — REPRODUCES (final §7.3 of its verdict; criterion: P1+P2 clean and every finding REPRODUCED or STATE-MOVED with a documented move): P1 29/29 pins clean + stock-6 sha match; P2 57/57 getoption rows 0 mismatch + binds 192 with the full flag/modmask census + animations 35/19/6 + sources 17 + rules 4+69+2+4 + bind sources 25+23+4+90+50; P3 F1–F10 all reproduced (F1 via the documented E3 turnover move, independently witnessed by the seat); §7.4 additionally executed the kit's late addendum (waybar backups 4; backup bytes 65|5892 5114 1458 1458|873 513 953 1322; font 9→12.5 ×4; hooks 5; palette 20 — every expectation holds) — evidence `/tmp/w4-ver-m3/VERDICT.md` (284 L by `wc -l`; sha256 `69ca88ce4d1ac66b…`; ephemeral). Lane errata it filed (box unaffected): note §2.3 dispatcher-tail prose is wrong (five ×4 incl. `swapwindow`, five ×2); the corrected runner still prints `binds: n= 1` and still carries the 16-char pin (`28 / 1`); the note's "29/29" receipt holds for the kit path, not the runner artifact
- [x] No cross-domain bleed (PROVINCE.md still accurate)
  VER-M4 (non-author audit seat) — CLOSES on its named verdict: all 15 province claims reproduce (C1–C15 + §2–§6 details; 22/22 pins; boundaries: repo scope, declared trees, secrets shape-only with 0 key-shaped hits, no network); no cross-domain bleed; all four declared refusals held; the one falsified claim (the self-audit's count-convention line, false at v1/v2) was corrected in v3 to the measured truth ("no trailing newline; `wc -l` = editor view − 1", re-measured TRUE) on an uncommitted in-flight file — no filed record was rewritten, nothing remains open; closure needs no erratum append (its §3; the record MAY optionally note the convention fix) — evidence `/tmp/w4-ver-m4-scratch/VERDICT.md` (120 L by `wc -l`; sha256 `1101c7bff5e6f6ee…`; ephemeral) + `verify-run.log` (~9.7 KB)
```

Caveats for the finalizer: both verdict files live in scratch and were re-filed
during 16:23–16:33Z (VER-M3 grew 11,557 → 18,006 → 19,930 B; VER-M4 10,724 →
9,134 B), so re-hash both at commit time and cite the hashes actually read;
their full evidence does not survive /tmp reaping — the SHONEN/LOG lines carry
the load-bearing hashes. The self-audit's close was on v3
(sha `3014a84060c95710…`, 264 L by `wc -l`); a later revision re-opens only
the delta.

## 4. Record text to apply (draft blocks — v3)

### 4a. LOG.md round-4 entry (append after the round-3 entry, LOG.md line 293)

```
- 2026-10-14 — round 4: calibration — close the two open SHONEN boxes with
  named non-author verifiers (dispatch per `plans/round-4.plan.md`;
  anti-claim: any non-reproduction or province violation keeps the box open).
  Round-4 work sat uncommitted in the working tree; this scribe re-verified
  the claims it records and lands the round commit with this entry
  (landed-means-committed). Deliverables:
  MADO-R4-2 → `corpus/knowledge/idle-lock-plane.md` (355 L by `wc -l`;
  editor 356, no trailing newline; + the ERR-M round-4 E2 append → 381 L
  current, sha256 `a0597be96c10…`): idle/lock plane measured — 3 config
  files (765/742/176 B) byte-identical to the shipped Omarchy payload by
  sha256 identity; 11 actuator scripts + 2 payload files; line-anchored
  declared chain (150 s screensaver / 152 s lock, ≈302 s effective per the
  file's own reset rationale; DPMS off ≈3 s after lock via script, wake
  restores); 7 Hyprland option semantics (§6); runtime snapshot §7 with live
  idle transitions UNKNOWN by constraint (§0 operator-presence margin);
  stateless process-toggle surface §8; hardware no-ops §9; 8 unknowns (§11);
  3 spot-checks (§12).
  MADO-R4-1 → reviewer pack `/tmp/mado-r4-1-probe/repro-r3.sh` (389 L,
  23,743 B, sha256 `70dff755278d…`; scratch, ephemeral): read-only one-pass
  driver of the round-3 sweep, embeds 57-row `expected.tsv`, `D=` redirect.
  VER-M3 found 3 defects in it (D1 fatal awk escape → false "57 missing";
  D2 binds summary reads `n= 1`; D3 16-char pin vs 64-char comparator) —
  fixed runner sha256 `389a1bb7…`; M4-1's fixed run `/tmp/w4-m4-1-repro/`
  → 57/0. Durable half = SKILL "Reproduction package" section.
  MADO-R4-4 → re-run evidence `/tmp/mado-r4-4-repro/`: full chain rc 0 —
  "checked 57; mismatches/missing: 0"; census 46 `agreement` + 6
  `agreement*` + 4 `live-default` + 1 `extra`; ran 16:09Z (pre-restart).
  MADO-R4-3 / M4-3 → audit support `/tmp/mado-r4-3-1-prov/` (commit-
  timestamp log; `animations.json` 5,327 B) + `/tmp/w4-m4-3/` (12 logs);
  product → `corpus/knowledge/province-accuracy-selfaudit.md` (in-repo;
  v1 17,190 B → current 264 L/17,856 B by `wc -l`, sha256 `3014a84060c9…`;
  edited in place twice during the round — v2/v3 deltas inspected by
  VER-M4).
  ERR-M → round-4 errata sweep (5 append-only blocks, read-only re-measured
  16:20–16:25Z, scratch `/tmp/w4-err-m-sweep/`): `config-health-report-r3.md`
  E2 (6×→7× S3 corrigendum) + E3 (turnover) 550→587 L; `hyprctl-
  verification-layer.md` E2 (orphan-envs closure) 280→302 L;
  `waybar-walker-plane.md` R4-E1–E8 (R3-1 §8's 7 candidates + provenance
  corrigendum) 364→474 L; `waybar-walker-semantics.md` E1 pointer 455→462 L;
  `idle-lock-plane.md` E2 355→381 L. Carried errata: clean after this.
  SKILL.md round-4 edits (authoring lanes not self-labeled; `git diff
  --numstat` +57/−5): 396 → 448 L by `wc -l`, sha256 `46c7c5261f9c…`;
  idle/lock row rewritten + sunset/xdph split; tray bus name typo
  `arrouillard`→`arouillard` fixed; "Reproduction package" section;
  "Promotion-box status" section pinning the verifier inputs; new idle-lock
  trap row. SKILL sha `⟨frozen at this commit⟩`.
  Verifier attributions (SHONEN): VER-M3 — REPRODUCES (final §7.3; P1/P2
  clean, P3 all findings reproduced; pack defects + note §2.3 dispatcher-tail
  erratum + runner receipts filed for lane errata). VER-M4 — all 15 PROVINCE
  claims reproduce and no cross-domain bleed; box kept OPEN on ONE falsified
  self-audit claim (its count-convention line); close = append E1 (quoted in
  its verdict §6) to `province-accuracy-selfaudit.md`. SHONEN.md → box 2
  `[x] VER-M3`; box 4 `[~]` (or `[x] VER-M4` if E1 is verified in this
  commit's tree — §3 of the draft).
  Scribe verification (this entry; commands re-run at finalization, raw log
  `/tmp/w4-scr-m/`): `wc -l corpus/knowledge/idle-lock-plane.md` → 355 (or
  381 post-ERR-M); table census `grep -c '^|'` → 39 = 4×(h+s)+31;
  `git diff --numstat HEAD -- SKILL.md` → 57/5; `wc -l SKILL.md` → 448;
  corrected-runner re-run from a copy → `checked 57; mismatches/missing: 0`;
  live read-only spot-checks — `hyprctl version` 0.56.2 `efb5099…`,
  `sha256sum ~/.config/hypr/hyprland.conf | cut -c1-16` → `4f52854a3c143dcf`,
  `pgrep -x hypridle` (era-dependent), `hyprctl -j layers` no lock surface.
  Observations (draft §6): ⟨fill: (b) errata applied by ERR-M incl. the
  R3 lines; (f) mid-round session restart headlines; (h) self-audit is a
  moving target and one count-convention claim was falsified; (g) VER-M3
  verdict + follow-ups⟩.
  Unknowns (draft §7): ⟨fill: E1 branch; SKILL authoring lanes; restart /
  hypridle-exit causes; /tmp pointer durability⟩.
  Falsifiable next-iterations (draft §8): ⟨fill: append E1 → close box 4 →
  promo gate; fix runner V2/V3 + note §2.3; lessons/round-4.md; the
  committed census gate (round-5 plan)⟩.
```

### 4b. corpus/README.md — coverage map rows

Append after the round-3 row (line 14):

```
| `knowledge/idle-lock-plane.md` (MADO-R4-2, round 4) | Depth extension for the idle/lock surface named in PROVINCE ("screen/idle behavior"): three configs (`hypridle.conf` 765 B/19 L, `hyprlock.conf` 742 B/43 L, theme `hyprlock.conf` 176 B/5 L) and 11 actuator scripts + 2 payload files byte-measured (provenance by sha256 = shipped payload, not by naming); line-anchored declared chain 150 s screensaver → 152 s lock → DPMS ≈3 s (`omarchy-system-lock`) → wake restores, ≈302 s effective per the file's own reset rationale; lock behavior script-defined (§5); 7 Hyprland option semantics — compositor provides wake half + session-lock protocol only (§6); §7 runtime snapshot incl. the live idle-transition UNKNOWN (operator-presence constraint §0); §8 stateless toggle/indicator; §9 hardware no-ops (no backlight devices); §11 8 unknowns; §12 3 spot-checks. Round-4 addendum (ERR-M block E2): post-probe session turnover — autostart start of hypridle 16:11:08Z, present 16:21:49Z, absent ≤16:23:20Z, silent exit; authoring measure 355 L by `wc -l` → 381 L current, sha256 `a0597be96c10…` | file reads (`wc`/`stat`/`sha256sum`/`diff`/`grep -n`) + read-only probes (`hyprctl` getoption/monitors/layers/devices/clients/systeminfo/version, `pgrep`/`pidof`, `systemctl --user`, `loginctl`, `pacman -Q`, `journalctl --user`); scratch `/tmp/mado-r4-2-probe/`; probe window 2026-10-14 16:00–16:08 UTC (note header) |
| `knowledge/province-accuracy-selfaudit.md` (MADO-R4-3 product; box-4 evidence, round 4) | Province-accuracy self-audit — the artifact VER-M4 audited (non-author): PROVINCE.md claim-by-claim (C1–C15) + boundaries + §8 counts; 264 L by `wc -l`; sha256 `3014a84060c9…` current (v1 `f81f19db…` 17,190 B landed ~16:25Z, edited in place to v2 `2d8d527c…` and v3 during the round). VER-M4 verdict: all 15 province claims reproduce (22/22 pins; boundaries; secrets shape-only 0 key-shaped hits; no network); box kept open on ONE falsified self-audit claim — its own count-convention line ("trailing newline; `wc -l` equals editor view" — measured false); close = append E1 (`/tmp/w4-ver-m4-scratch/VERDICT.md` §6, ephemeral; fold the text in before /tmp is reaped) | file bytes + read-only live probes by the audit lane (scratch `/tmp/w4-m4-3/`); VER-M4's independent re-execution `/tmp/w4-ver-m4-scratch/verify-run.log`; 2026-10-14 (round 4) |
```

Round-4 addenda to the four ERR-M-appended rows (append one bracketed sentence to each row, round-2 style): `config-health-report-r3.md` (E2 6×→7× corrigendum + E3 turnover; 550→587 L), `hyprctl-verification-layer.md` (E2 closure; 280→302 L), `waybar-walker-plane.md` (R4-E1–E7 applied + R4-E8; 364→474 L), `waybar-walker-semantics.md` (E1 pointer; 455→462 L) — each citing `/tmp/w4-err-m-sweep/` and the block header `Errata (round 4) — appended 2026-10-14 (ERR-M)`.

### 4c. SCORECARD.md — move-log rows (append after the round-3 rows)

```
| 4 | calibration | after round 3: SHONEN 2/4 — `[x]` SKILL tables + no-oral-context (MADO-R3-4); `[~]` e2e task + PROVINCE accuracy, both lane-asserted, no non-author verdict in-repo | named non-author verdicts land: VER-M3 — REPRODUCES (final §7.3) → box 2 `[x]`; VER-M4 — 15/15 province claims reproduce, no cross-domain bleed, box 4 OPEN one erratum wide (falsified self-audit count-convention line; close = append E1) → `[~]`/`[x]` per E1; round-3 pass now has an executable reviewer pack (MADO-R4-1 + corrected runner) + a fixed-run re-run | `wc -l /tmp/mado-r4-1-probe/repro-r3.sh` → 389; pack sha `70dff755278d…`, corrected runner sha `389a1bb7…`; fixed run → `checked 57; mismatches/missing: 0`; VER-M3 verdict sha256 `31d40550c8dee977…`; VER-M4 verdict sha256 `0f8c944713893b56…` |
| 4 | depth | round-3 corpus: the idle/lock surface held only scattered file-byte mentions (MADO-1 §8/§10, MADO-2 §5; hypridle absent, cause `[UNK]`) | `idle-lock-plane.md` (MADO-R4-2, 355 L by `wc -l` → 381 after ERR-M E2): 4 tables / 31 data rows (§2 3 configs; §2b 11 actuators; §5 10 chain steps; §6 7 options); provenance by sha256 identity; declared chain incl. script-defined lock/wake side-effects; runtime snapshot + live-idle UNKNOWN; mid-round session restart recorded (autostart start 16:11:08Z; silent exit ≤16:23:20Z) | `grep -c '^|'` → 39 = 4×(header+separator)+31; `sha256sum ~/.config/hypr/hypridle.conf` → `e7d3b8dd…` = shipped payload; journal quotes for the autostart start; `wc -l` → 355 → 381 |
| 4 | freshness | pending errata carried since rounds 2–3 (R3-1 §8 ×7 on the waybar note; F8/envs closure; R3-2 §0 tally 6×→7×; SKILL typo already fixed) | ERR-M sweep applied all as append-only blocks in 5 files (list in LOG entry), each re-measured read-only 16:20–16:25Z; new owed errata identified by the verifier seats: note §2.3 dispatcher-tail prose, runner V2/V3 receipts, self-audit E1 | `git diff --stat` (5 files, +192/−9 at 16:27Z); per-file `wc -l` 587/302/474/462/381; `grep -c 'Errata (round 4)' corpus/knowledge/*.md` → one per touched file |
```

⟨Finalizer may fold freshness into calibration if the round counts one move.⟩

### 4d. SHONEN.md regeneration

Apply §3's lines; keep boxes 1 & 3 byte-identical (round-3 attributions
stand); header and remaining seed text unchanged.
- With E1 NOT landed: box 2 → `[x] VA-M3…` (as in §3); box 4 keeps `[~]`
  but its evidence line is updated to the VER-M4 verdict + close condition.
- With E1 verified: box 4 → `[x]` with the same line + "E1 applied
  <file:line>, <sha>".
Mechanical check at finalization: extract the seed from PROTOCOL.md:419-431,
substitute `mado-shokunin`, diff — only changed box chars and the two
evidence lines may differ.

### 4e. Errata status

- `idle-lock-plane.md` E2 (draft-v1 candidate): **applied by ERR-M** —
  `/tmp/w4-err-m-sweep/append-idle-lock-plane.diff`; do not restate (record
  references that block).
- Owed: **E1 on `province-accuracy-selfaudit.md`** — text quoted in
  VER-M4's verdict §6 (`/tmp/w4-ver-m4-scratch/VERDICT.md`); owner = the
  audit lane; this is box 4's close condition.
- Owed (VER-M3's filed items, lane errata): note §2.3 dispatcher-tail prose
  (five ×4 incl. `swapwindow`, five ×2); corrected runner V2/V3 (binds
  summary, 16-char pin); K2's "29/29" scope wording.

## 5. Scribe verification plan (execute at finalization)

1. Counts/pins: `wc -l corpus/knowledge/idle-lock-plane.md` (355; 381 if
   ERR-M's E2 counted in), `grep -c '^|'` → 39; `wc -l
   corpus/knowledge/province-accuracy-selfaudit.md` → 264; `git diff
   --numstat HEAD -- SKILL.md` → 57/5; `wc -l SKILL.md` → 448; `sha256sum`
   on each frozen value.
2. Pack re-run from a fresh copy — use the **corrected** runner
   (`/tmp/w4-m4-1-repro/repro-r3.sh`, sha `389a1bb7…`) or apply VER-M3's D1
   one-line fix; as delivered the original pack reports a false
   "mismatches/missing: 57". Expect `checked 57; mismatches/missing: 0` +
   census 46/6/4/1; ignore epoch values (PIDs, window set).
3. Live read-only spot-checks: `pgrep -x hypridle` (record era state + time;
   systemctl halves do not discriminate — the daemon is a session scope
   child), `hyprctl -j layers` no lock surface, `hyprctl version` 0.56.2
   `efb5099…`, `sha256sum ~/.config/hypr/hyprland.conf | cut -c1-16` →
   `4f52854a3c143dcf`.
4. Resolve ⟨PENDING⟩: E1 branch (§3/§4d); SKILL authoring lanes; row
   choices in 4b/4c.
5. SHONEN.md seed diff (4d) + marks-only check.
6. Commit the round with the lane identity; freeze the SKILL sha after the
   final write; re-check the frozen sha appears in the entry.

## 6. Observations at draft time (anchored)

(a) SKILL.md round-4 edits carry no lane self-label (no diff header) — at
    least two editors touched it between 16:10 and 16:28 (424→448 L); the
    authoring lanes are unknown to this scribe (same defect class as
    rounds 2–3).
(b) Errata: the round-3 carry was **applied by ERR-M** during round 4 —
    R3-1 §8's 7 candidates (waybar note R4-E1–E7 + R4-E8), F8/envs closure,
    R3-2 §0 tally 6×→7×, SKILL typo (already fixed). New owed items: the
    self-audit E1 (box-4 close) and VER-M3's three filed follow-ups (§4e).
(c) `corpus/lessons/` still empty (4th round); committed verdict gate still
    absent (`find corpus -name '*.sh'` → 0; round-5 plan claims it next).
(d) Count convention: all notes here end without a trailing newline; every
    count names its command. The self-audit's own claim to the contrary was
    VER-M4's sole falsification — worth a sentence in the LOG entry.
(e) `plans/round-4.plan.md` and `plans/round-5.plan.md` are both untracked;
    landed-means-committed for them is this round's commit.
(f) Headline: mid-round session restart (16:11:06–08Z; §2) — now recorded
    independently by four parties (this lane, VER-M3, VER-M4, ERR-M; AUD-M1
    referenced). Any replay of round-4 live checks spans two sessions;
    process-state claims need era stamps.
(g) VER-M3 final verdict REPRODUCES, with follow-ups: note §2.3
    dispatcher-tail prose wrong; corrected runner still prints `binds: n= 1`
    and still carries the 16-char pin; "29/29" receipt scope.
(h) VER-M4: ALL province claims reproduce; box 4 open on exactly one
    falsified claim in the self-audit file; the file was edited in place
    twice during the round (v1→v2→v3; 17,190→17,856 B) — a moving target
    the finalizer must re-hash at commit time.
(i) Boundary of this lane: read-only probes only; writes = this draft +
    `/tmp/w4-scr-m/` scratch. No substrate file under `~/.config` or
    `~/.local` was written.
(j) The reviewer pack's defects (D1–D3) were found by VER-M3 — a
    reviewer-of-the-reviewer effect worth one line in the record: the
    seat's own harness caught what the lane's own re-run (16:09Z, clean)
    could not, because both used the same broken runner.

## 7. Unknowns

1. Whether E1 lands before the round commit → box 4 `[~]` vs `[x]`.
2. SKILL.md round-4 authoring lanes (≥2, unlabeled).
3. Self-labels/scope of MADO-R4-3 / `w4-m4-3` / AUD-M1 (artifact-based
   descriptions only here).
4. Cause of the 16:11Z session restart (unattributed traces near the
   boundary); cause of hypridle's silent exit ≤16:23:20Z (no journal line).
5. Durability of the two verdict files (scratch; fold key hashes into the
   record — done in §3/§4a — but the full evidence does not survive /tmp).
6. Whether the finalizer keeps the depth + freshness rows (4c).
7. Any post-v3 edit to the self-audit reopens VER-M4's delta question.

## 8. Falsifiable next-iterations (carry + new)

- Append E1 (audit lane) → close box 4 → SHONEN 4/4 → promotion gate
  (operator/integrator decision per PROTOCOL).
- Fix the corrected runner's V2/V3 (binds summary; 64-char pin) and apply
  VER-M3's note §2.3 dispatcher-tail erratum + K2 scope wording.
- `corpus/lessons/round-4.md` (ledger owed for rounds 1–4).
- Commit the executable census gate (`corpus/scripts/verify-plane.sh` +
  selftest) — the round-5 plan's operability move; retires the round-1
  ceiling.
- Durability convention for verifier evidence (fold verdict hashes into
  SHONEN/LOG — this round does; consider copying verdicts into the repo
  where write scope allows).
- Watch the daemon pattern: hypridle started at session start, exited
  silently within ~12 min; if it recurs, capture hypridle's own log surface
  or a journal-scope deactivation line.

## 9. Finalization checklist (mechanical, ordered)

1. Read both verdict files (`/tmp/w4-ver-m3/VERDICT.md`,
   `/tmp/w4-ver-m4-scratch/VERDICT.md`); confirm the §3 lines still match
   (sizes/shas); copy the E1 text from VER-M4 §6.
2. Check whether E1 landed in `province-accuracy-selfaudit.md`; branch §3/§4d
   accordingly; re-hash the self-audit at commit time.
3. Run §5's commands (corrected runner); pin results into the LOG entry.
4. Append 4a to LOG.md; 4b rows to corpus/README.md; 4c rows to
   SCORECARD.md; regenerate SHONEN.md per §4d (seed diff check).
5. Commit the round under the lane identity; freeze the SKILL sha after the
   final write; re-check it appears in the entry.
6. If box 4 stays open at commit, keep this draft as the record's ancestry
   and state the unresolved E1 in the LOG entry's unknowns (box 4 stays
   `[~]`).

## 10. v3.1 update (16:36Z) — both boxes close; supersedes stale wording above

- §0/§3: both boxes now CLOSE on named non-author verdicts — box 2 `[x]`
  VER-M3 (REPRODUCES; final verdict file 284 L by `wc -l`, sha
  `69ca88ce4d1ac66b…`; §7.4 also executed the kit's late addendum, every
  expectation holds); box 4 `[x]` VER-M4 (v3 in-place correction of the
  count-convention claim accepted — "no erratum append is required for
  closure"; verdict file 120 L, sha `1101c7bff5e6f6ee…`). §3's earlier
  `[~]`/"E1 close condition" wording is superseded by §3 v3.1; §9 step 2
  becomes "re-hash both verdicts + the self-audit at commit time; if any
  moved, re-check the cited text still matches".
- §4a: use the §3 v3.1 lines for "Verifier attributions"; SHONEN.md → 4/4
  `[x]`; keep one sentence of defect history on the self-audit episode
  (v1/v2 count-convention claim falsified → corrected in v3 pre-filing,
  accepted by VER-M4 §3).
- §4d: regeneration is unconditional 4/4 — no branch.
- §4e: E1 is RESOLVED (v3 correction on the uncommitted file). Remaining
  owed errata = VER-M3's three items (note §2.3 dispatcher-tail; runner
  V2/V3; K2 scope wording) — lane errata, box-unaffected.
- §6(h) / §7: moving-target caveat stands (v1→v3; 17,190 → 17,856 B) but
  the defect is resolved, not open; drop the "E1 branch" unknown; keep the
  re-hash-at-commit duty.
- §8 first bullet: now simply "SHONEN 4/4 → promotion gate
  (operator/integrator decision)" — no erratum append first.
- Boundary note: this lane wrote only this file in the repo (+
  `/tmp/w4-scr-m/` scratch); no substrate or lane file touched.
