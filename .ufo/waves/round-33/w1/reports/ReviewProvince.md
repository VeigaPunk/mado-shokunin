# ReviewProvince — round 33, wave 1

Reviewer: mado leaf (province review, no edits to PROVINCE.md).
Inputs: `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/waybar-module-text-route-r25.md` (r25) and `.../event-delivery-limits-r26.md` (r26), judged against `PROVINCE.md` (domain: desktop & compositor craft — Hyprland/waybar/walker config plane and display behavior on this host).

## Verdicts

### r25 — waybar-module-text-route-r25.md — **IN** (desktop/compositor craft)

- Subject is the lane's owned bar surface: the route from compositor event socket (`.socket2.sock`) through the Waybar Hyprland backend to `label_.set_markup` (r25 §1, citing S190:17-33/:77-99/:88/:140, S191:25-26/:54-64). Waybar is an owned surface (`~/.config/waybar/` plane; built-in Hyprland modules produce the bar text).
- It extends, not replaces, existing ground: it positions itself next to the lane's custom-module path (S053/S054) and renderer-boundary note `waybar-observation-boundaries-r16.md` (r25 §2).
- Refuse check: no secrets, no model endpoints, no model quality. Substrates read-only — no bar started, no producer executed, no host config read this round (r25 header). Host-unverified claims are correctly fenced as UNK (r25 §3), so nothing in-province is overstated.
- No flip condition applies (no refuse).

### r26 — event-delivery-limits-r26.md — **IN** (desktop/compositor craft)

- Subject is compositor display behavior on this host: the event-manager queue cap (`MAX_QUEUED_EVENTS = 64`, overflow → client removal, partial-write resume, shutdown drop; r26 §1, S187 `src/managers/EventManager.cpp` v0.56.2) and the client-side match (Waybar backend 1024-byte read, r26 §2). The lane already owns static prediction of this compositor's observable behavior (round-25/26 `mado-binds.py` / `mado-anims.py` rows in PROVINCE.md); the socket contract is the delivery mechanism of the same bar-text ground (F1).
- The consequence claim (§2) stays inside the lane's display plane — a stalled custom-module producer can cost the bar its event feed, with the failure logged compositor-side — and is labeled INF with basis, not asserted as observed.
- Refuse check: none triggered — no secrets, no model endpoints/quality, no mutation ("no socket was connected and no event was observed", r26 header). The `UNK` (cap never observed on this host) correctly bounds the entry.
- No flip condition applies (no refuse).

## Notes for merge (non-blocking, in-file housekeeping, not province defects)

- r26's merge note asks wave-1 rows S187 and S188 to be appended to its source list when merged; r25 cites S190/S191 which are the S188 half's constituents. Merge mechanics for the corpus steward, not a province question.
- Both entries pin upstream tag `0.15.0` with sha256 recheck expectations dated 2026-10-23 (90d recheck); the lane's live waybar version is checked by `tools/mado-verify.sh`, so a version drift on this host is the recheck trigger, not a province breach.

## Scope statement

This report judges province membership only. Corpus accuracy, evidence-label arithmetic, and promotion are other reviewers' seats. PROVINCE.md untouched.
