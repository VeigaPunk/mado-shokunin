# ConnSiblings — sibling-overlap scan (round-48 w1, mado C1/C2)

Seat: ConnSiblings (leaf; no subagent dispatch). Date 2026-10-26. Lane: mado-shokunin, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Claims scanned: C1 (xdg-terminal-exec v0.14.3 warm-cache path) and C2 (XKB compile ground, kb_* names). Full seat report: `.ufo/waves/round-48/w1/ConnSiblings/report.md`.

## Method

Scanned all 20 sibling lanes under `/home/vgpnk/Projects/shokunin/{audio,chousa,game-dev-2d,game-dev-3d,kagi,kaidoku,kake,kama,kasegi,kengaku,kotoba,kotodama,kumitate,lore,mori,revenger,souji,tabi,tameshi,tsukuroi}-shokunin`, read-only, for (a) XKB/keymap/input-method ground and (b) xdg-terminal-exec/terminal-cache ground. Files per lane: `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` (60 explicit paths, two 30-file grep batches; globbed path patterns are not expanded by the grep tool — verified). Corroborated by a filename listing of `corpus/knowledge` and `tools` per lane and a content grep across all 20 knowledge trees. No lane file was modified.

## Evidence

- `(?i)xkb|keymap|kb_layout|rmlvo|kcgst|kb_rules|kb_model|kb_variant|kb_options` over all 60 sibling files: **0 hits** (all 20 lanes).
- `xdg-terminal-exec|terminal-exec|xte_|warm-cache|save_cache|terminal-route|mado-terminal` over all 60 sibling files: **0 hits**. Sole near-term hit is a different concept: `tabi-shokunin/corpus/README.md:18` "two preserved warm-cache runs" — browser bfcache loopback evidence, not the resolver's cache.
- Precise input-method re-scan (`fcitx|ibus|uim|xim|kime|anthy|mozc|scim|gcin|compose:caps|input method|keyboard layout`) over all 60 sibling files: **no field hit**.
- Knowledge-content grep across all 20 `corpus/knowledge` trees: the only `xdg-terminal-exec` occurrences are host-state/liveness records, not selection or cache behavior:
  - tsukuroi package-state rows: `tsukuroi-shokunin/corpus/knowledge/aur-risk-plane-ver-s6.md:72` — "typora tzupdate ufw-docker walker xdg-terminal-exec yaru-icon-theme yay` [observed]." (foreign/AUR census); `aur-risk-plane.md:199` lists `xdg-terminal-exec` among the foreign "Packager: Unknown Packager" set.
  - tsukuroi boot/journal planes: `boot-plane.md:101` — "`app-Hyprland-xdg-terminal-exec-…scope` | `Failed with result 'oom-kill'` (pid 1573)"; `oom-event-plane.md:71` — "'--unit=app-Hyprland-xdg\x2dterminal\x2dexec-dd9e67bd.scope' … xdg-terminal-exec".
  - mori liveness: `mori-shokunin/corpus/knowledge/observability-census-r1.md:94` — "(`app-Hyprland-xdg-terminal-exec-dd9e67bd.scope: Failed with result 'oom-kill'`)".
- No sibling knowledge filename matches `*xkb*`, `*keymap*`, `*fcitx*`, `*ibus*`, `*terminal*` (resolver sense), `*xdg*`. The three terminal-named sibling files are unrelated to both claims: `mori-shokunin/tools/mori-seat-terminal.py` (OMP transcript seat classification), `kasegi-shokunin/corpus/knowledge/terminal-classes.md` (mission-end classes of bounty research, base absent), `tameshi-shokunin/tools/trace-inputs.py` (mutation-tester input tracking).
- `kotoba-shokunin/PROVINCE.md:69` census row confirms mado's declared plane with no sibling split: "mado owns the Hyprland/waybar/walker/terminal config plane and display behavior read-only".
- `tsukuroi-shokunin/PROVINCE.md:48` (ADJ-03) already routes configuration-level desktop diagnosis to mado while tsukuroi retains package/unit health, and `:124` (OUT-004) pins mado's config-plane half at `a4046a821608`.

## Contested scope

**None** on either claim's ground. No sibling claims XKB/keymap/input-method knowledge or xdg-terminal-exec selection/cache behavior. Per the seat contract (report, never absorb): there is nothing to absorb; the adjacencies below are reported for the freeze.

## Adjacent surfaces (not contested) to keep distinct

1. `tsukuroi` — package provenance and boot/journal OOM-scope records of the resolver (`app-Hyprland-xdg-terminal-exec-…scope`): host state. C1 models the resolver's behavioral output (cache verdict, stdout, exit), which is a different surface; C1 must not borrow tsukuroi's event records as resolver behavior, and tsukuroi's rows stay package/health-only.
2. `mori` — the same scope's OOM kill as fleet liveness (`observability-census-r1.md:94`).
3. `tabi` — the word "warm-cache" denotes browser bfcache evidence there; terminology collision only.

## Proposed PROVINCE.md refinement line for mado (append-only; one line)

> Round-48 refinement (append-only; resolved sibling-overlap scan; no new write surface): the terminal-selection route's executable half now covers the resolver's warm-cache path (`tools/mado-terminal.py`, round-47 tool) and the input-device plane's knowledge continuation covers the XKB compile acceptance of `kb_*` names (libxkbcommon/xkeyboard-config, live `xkbcli compile-keymap` receipt). Sibling scan (round-48 w1 ConnSiblings): no other lane claims resolver-selection/cache behavior or XKB compile knowledge; tsukuroi's package/OOM-scope records and mori's liveness events for the `xdg-terminal-exec` scope stay theirs (host state), and tabi's "warm-cache" term denotes browser bfcache evidence, not this resolver's cache.

## Verification

- Greps over 60 explicit sibling files (3 per lane × 20 lanes), the precise input-method re-scan, the knowledge-tree content grep, and the `find`-based filename listing of knowledge/tools; locators computed with `grep -n`. All read-only.
- No tool installed or updated; pacman untouched; no host-service or compositor mutation; no xdg-terminal-exec run; no xkbcli run.
- Risk note for w2: if a falsifier cross-references `xdg-terminal-exec` host events, the tsukuroi/mori OOM-scope records are liveness/package evidence, not resolver-selection evidence — keeping that distinction avoids an invalid cross-lane citation.
