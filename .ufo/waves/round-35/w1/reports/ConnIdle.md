# ConnIdle — connect the three adopted entries to the lane's idle-lock notes

Seat: ConnIdle (round 35, wave 1). Read-only; no edits to either existing note.

## Inputs read

- Existing notes: `corpus/knowledge/idle-lock-plane.md` (MADO-R4-2, probe
  2026-10-14; E1 seed + E2 erratum) and `corpus/knowledge/idle-lock-route-r17.md`
  (documentary route, verified-at 2026-10-20).
- The three new entries (this round's adopted set, normalized copies under
  `.ufo/waves/round-35/controls/golden/corpus/knowledge/`):
  `idle-lock-never-asked-r12.md` (S203, S204), `idle-lock-chain-armed-r14.md`
  (S205), `idle-lock-offered-in-the-bar-r15.md` (S206, S207, S208, S209, S210).
- The round's own evidence: `.ufo/waves/round-35/fetch/S20{3..10}.receipt.txt`
  (host re-opens dated 2026-10-24).
- The merge-package originals under `~/Projects/shokuknow/merge/mado/…` for
  divergence (package ids S315/S316, S327, S335-S342 → lane ids S203-S210).

## Verdict at a glance

- `idle-lock-plane.md`: no statement is wrong. Two statements are dated point
  samples superseded by this round's measurement; one anchor drifted; several
  `[UNK]` items narrow. The sweep must append an E3 block.
- `idle-lock-route-r17.md`: no statement is wrong. Two `[UNK]` items are
  resolved or narrowed by this round's evidence. The sweep must append a
  dated resolution note.

## `idle-lock-plane.md` — per statement

| Statement in the note | Round-35 evidence | Verdict |
|---|---|---|
| §1 / §7: "hypridle is not running" (no process; unit inactive/disabled) | S205: `pgrep` → `1667 /usr/bin/hypridle`; journal `Started hypridle.` at 2026-10-23 13:25:00 and 22:14:11 | **Dated, not wrong.** True point sample of the 2026-10-14 window (ps/pgrep is independent of the unit artefact). State moved; now ARMED. |
| §7 / §11 item 1: cause of the daemon's absence `[UNK]`; toggle-off "would be traceless" | S205 journal start lines; S204: `journalctl --user \| grep -c omarchy-toggle` → 0; S210: `toggles/hypr/` holds `flags.conf`, `window-no-gaps.conf`, 0 idle files | **Narrowed, not closed.** Start leaves a journal trace (`systemd[1493]: Started hypridle.` — transient scope, matching E2's "session child"). File-tracelessness holds: no flag file exists to write. But S204's zero journal count does NOT clear a manual toggle — `omarchy-toggle-idle` kills via `uwsm-app`, which the journal would log only as a process stop, not an `omarchy-toggle` line. Cause of absence still `[UNK]`. |
| E2: "`systemctl`-only re-check cannot see it; only the `pgrep` half discriminates" | S205: `systemctl --user is-active hypridle` → `inactive` while `pgrep` → live pid, *simultaneously* | **Directly confirmed a third time.** The adopted r14 entry states the mechanism: transient scope unit, not the packaged service. |
| §8: "Waybar module `custom/idle-indicator` in `~/.config/waybar/config.jsonc:206-208`" | S206: same file now 6354 B, sha `a408a33d…`; block spans **lines 207-212** (open at 207, `on-click` at 208, closes 212); module listed at line 18 | **Anchor drifted, content right.** The `:206-208` line cite is stale; the `on-click = omarchy-toggle-idle` claim and `idle.sh:3-6` behavior (sha `6d8d2c11…` unchanged, S207) are confirmed. |
| §8: "`omarchy-menu` also references hypridle (menu wiring; not enumerated here)" | S208: `omarchy-menu:207` lists `Idle Lock`; `:212` dispatches `*Idle*) omarchy-toggle-idle` (sha `d196b086…`) | **Gap filled.** Enumeration now exists; no contradiction. |
| §8: "`toggles/` contains only `hypr/`" | S210: `toggles/hypr/` contains `flags.conf`, `window-no-gaps.conf`; 0 idle entries | **Dated point sample.** `hypr/` is no longer empty; the load-bearing claim (no idle flag exists) still holds. |
| §3 / §5: `hypridle.conf` timeouts 150/152, `lock_cmd`, `inhibit_sleep=3` | S205: conf digest `e7d3b8dd…` identical to §2 pin; timeout lines re-read identical | **Confirmed, no drift** since 2026-10-03 17:44:32. |
| §11 item 2: live idle transitions `[UNK]` | S205 measures armed state only; r14 §3 explicitly claims no transition observed | **Still open.** Armed ≠ fired. |
| §11 item 7: rendered waybar module matches `idle.sh` | S207 re-reads file only; no RTMIN+9, no screenshot | **Still open.** |

### What the corrections sweep must append to `idle-lock-plane.md`

An **E3 (2026-10-24)** block, append-only under "Errata (round 4)":

1. `hypridle` measured **running** at 2026-10-24 (S205: pid 1667; journal
   `Started hypridle.` 2026-10-23 13:25:00 and 22:14:11). §1/§7 "not
   running" remains a true point sample of 2026-10-14; record that the
   state moved. The chain is now armed (declared 150 s/152 s), no
   transition observed — UNK-2 stands.
2. `systemctl --user is-active` read `inactive` *while* `pgrep` returned a
   live pid: third confirmation of E2's discrimination note; mechanism
   named — daemon runs as a transient scope unit (`uwsm-app` child), never
   the packaged `hypridle.service`.
3. UNK-1 narrowed: daemon starts leave a journal trace; stop causes remain
   file-traceless (no flag file — S210 re-read `toggles/hypr/` =
   {flags.conf, window-no-gaps.conf}, 0 idle files; `omarchy-toggle-idle`
   writes nothing). Note S204's limit: zero `omarchy-toggle` journal lines
   does not exclude a manual kill, which is not logged under that name.
   The 2026-10-14 absence cause stays `[UNK]`.
4. §8 re-anchor: `custom/idle-indicator` module block now at
   `config.jsonc:207-212` (module list entry line 18); file 6354 B, sha
   `a408a33d…` (receipt S206). Enumerate the menu surface §8 deferred:
   `omarchy-menu:207` (`Idle Lock` option) and `:212` (`*Idle*)
   omarchy-toggle-idle`), receipt S208.
5. Optional precision: `toggles/` line in §8 — `hypr/` now non-empty
   (S210); the negative claim "no idle flag" unchanged.

## `idle-lock-route-r17.md` — per statement

| Statement | Round-35 evidence | Verdict |
|---|---|---|
| § Unexercised: "Why hypridle was not running at the 2026-10-14 probe … running state is not observed here" (`[UNK]`) | S205: running, pid 1667, two session start lines | **Resolved as of 2026-10-24.** The question it asked is answered for the present session; the 2026-10-14 cause stays `[UNK]` (see plane UNK-1). |
| Host declaration: "Declared start route only; whether hypridle is running is `[UNK]`" | S205 journal + pgrep | **Dated.** The autostart route is now observed to have fired (journal `Started hypridle.` under `systemd[PID]` user manager — transient scope, consistent with `exec-once = uwsm-app -- hypridle`). |
| hypridle.conf digest pin `e7d3b8dd…`, timeout anchors :9-12 / :15-19 | S205 identical digest and line reads | **Confirmed, no drift.** |
| `grace` note: host invokes `hyprlock` bare | S205 `hyprlock process: none`; nothing contradicts | Unaffected. |
| Remaining `[UNK]` items (transitions, lock-notify-v1, pidof guard race, PAM/faillock, multi-monitor, config parse, IdleHint writer, rendered indicator, binary version) | Not touched by S203-S210 | **Still open.** |

### What the corrections sweep must append to `idle-lock-route-r17.md`

A dated line in/near "Unexercised behavior":

1. Item "why hypridle was not running / running state not observed":
   **partially resolved 2026-10-24** — daemon live (pid 1667), journal
   start lines 2026-10-23 13:25:00 / 22:14:11, launched via the declared
   autostart route as a transient scope (S205). Amend to: "was not running
   at 2026-10-14 (plane §7) — resolved for present state; original cause
   remains `[UNK]`."
2. Header item "`hyprctl`/process probes not re-run here": note the
   running state is now observed (S205), so the note's "not re-run" caveat
   is historical.
3. No other line needs correction — route claims are documentary
   (upstream contract + file bytes) and every re-checked byte matches.

## Divergences inside the package originals the adopted entries already fixed

For the sweep's awareness (the adopted texts are correct; do not import the
package's errors):

- Package r14 claimed the plane's earlier "not running" was possibly "a
  probe artefact of exactly this kind" — overreach: the plane's process
  probes (`ps`, `pgrep`) are unit-independent. The adopted entry
  correctly reframes as "state that has moved, not a false record."
- Package r15 dated the oldest waybar config backup **2026-10-06**; this
  round's S209 sweep measures **2026-10-03 17:44**
  (`config.jsonc.bak.1791314470`). The adopted entry records the lane's
  measured figure and flags the divergence.
- Package r12's "the desktop never offers the choice" was scoped down to
  the **setup path** in the adopted entry — S206/S208 show the running
  interface offers it in two surfaces.

## Residual notes

- S209 receipt's "oldest dated copy" header line names `config.jsonc.bak`
  but the `stat` line beneath it correctly attributes 2026-10-03 17:44:32
  to `config.jsonc.bak.1791314470`; the adopted entry's date is right.
- The adopted entries' "the operator has never taken it" rests on S204's
  journal grep — see the caveat above: a `uwsm-app`-managed kill would not
  log an `omarchy-toggle` line, so "never toggled" is supported only to
  the extent the journal captures, which the entries' own UNK hedging
  already allows.
