# R81ConnSiblings — command log and evidence

Seat: `R81ConnSiblings`, round 81 w1, connector (sibling-overlap, read-only).
Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`; fleet root `/home/vgpnk/Projects/shokunin`;
staged assimilation package `/home/vgpnk/Projects/shokuknow/merge/mado`.
Report: `.ufo/waves/round-81/w1/R81ConnSiblings.md`. Captures: `.ufo/waves/round-81/w1/R81ConnSiblings/`.

No file outside this seat directory was written. No git or jj command of any kind was run. Nothing was
executed inside `/home/vgpnk/Projects/shokuknow/merge/mado` (read-only greps only). No subagent.

Scratch `/fast/scratch/hyaku/mado-r81/R81ConnSiblings` was created only as the working directory for the
two sweep scripts (so no relative path could land in the fleet root) and is removed at exit; nothing cited
here lives in it.

Reproduction: `sh .ufo/waves/round-81/w1/R81ConnSiblings/sweep.sh` and `…/sweep2.sh` regenerate every
`sweep-*.txt` capture verbatim (they `cd` to the fleet root or the package first, and redirect only into
the seat directory).

---

## Phase 1 — inventory and the first keyword sweeps

1. `ls -1 /home/vgpnk/Projects/shokunin/`
   → 27 entries; the lane set is 21 `*-shokunin` directories plus `kumitate-shokinin` (see cmd 76).

2. `ls -la /home/vgpnk/Projects/shokuknow/merge/mado/`
   → `MERGE-REPORT.json`, `MERGE-REPORT.md`, `SOURCES.append.md`, `amendments/`, `knowledge/`.

3. `mkdir -p /fast/scratch/hyaku/mado-r81/R81ConnSiblings /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/w1/R81ConnSiblings`
   → `ok`.

4. `for f in game-dev-3d-shokunin kotoba-shokunin kumitate-shokunin game-dev-2d-shokunin; do echo "=== $f ==="; ls -1 /home/vgpnk/Projects/shokunin/$f; done`
   → `game-dev-3d-shokunin`: `AGENTS.md LOG.md PROVINCE.md README.md SCORECARD.md SHONEN.md SKILL.md considerthese corpus reports`
   (no `tools/`); `kotoba-shokunin`: `… verifiers plans` (no `tools/`); `kumitate-shokunin`:
   `… scripts r8-in-tree-pollution.txt` (no `tools/`); `game-dev-2d-shokunin`: `… corpus reports`.

5. `ls -R /home/vgpnk/Projects/shokuknow/merge/mado/knowledge /home/vgpnk/Projects/shokuknow/merge/mado/amendments | head -60`
   → `knowledge/corpus/knowledge/` (many entries), `amendments/corpus/knowledge/` with four files:
   `dispatcher-semantics-r25.md dispatcher-surface-and-request-grammar-r26.md ipc-contract-r25.md waybar-module-text-route-r25.md`.

6. `ls -1 /home/vgpnk/Projects/shokunin/mado-shokunin/tools /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters | head -60`
   → `tools/` lists `mado-barfoot.py` among the lane instruments; `quality/counters/` lists
   `c1-r81-overflow-auto.py` and the earlier generation.

7. `cd /home/vgpnk/Projects/shokunin && for f in game-dev-3d-shokunin kotoba-shokunin kumitate-shokunin kumitate-shokinin game-dev-2d-shokunin; do echo "=== $f ==="; wc -l $f/PROVINCE.md; done`
   → `82 game-dev-3d-shokunin/PROVINCE.md`, `78 kotoba-shokunin/PROVINCE.md`,
   `58 kumitate-shokunin/PROVINCE.md`, `38 game-dev-2d-shokunin/PROVINCE.md`;
   `wc: kumitate-shokinin/PROVINCE.md: No such file or directory` (the stray directory — cmd 76).

8. `grep -rniE 'exclusive[ -]?zone|exclusive_zone|reserved[ -]?band|layer[ -]?shell|layer-surface|layer_surface' --include=*.md --include=*.py --include=*.sh --include=*.txt -l . | grep -v '^./mado-shokunin' | head -40`
   → only `./.ufo/reports/round-7{7,8,9}/mado.md`, `./.ufo/reports/round-80/mado.md`,
   `./kasegi-shokunin/.ufo/waves/round-24/wave1/ConnSibling.md`,
   `./kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt`,
   and tsukuroi package-list captures. No sibling *claim*.

9. `grep -rniE 'pgrep' --include=*.md --include=*.py --include=*.sh --include=*.txt -l . | grep -v '^./mado-shokunin' | head -40`
   → `./.ufo/...`, `./kasegi-shokunin/...`, `./tsukuroi-shokunin/.ufo/waves/round-{24,42}/...` — broad;
   narrowed in cmd 33 and the `sweep-c`/`sweep-d` captures.

10. `read /home/vgpnk/Projects/shokunin/kotoba-shokunin/PROVINCE.md`
    → `:72` the mado row, classification `none`:
    "`| mado | none | 62dd798bb08401a8697383552edcc36f109344fa | mado owns the Hyprland/waybar/walker/terminal config plane and display behavior read-only; … |`"

11. `read /home/vgpnk/Projects/shokunin/game-dev-3d-shokunin/PROVINCE.md`
    → `:75` "`- Desktop/compositor display behavior belongs to \`mado-shokunin\` (\`../mado-shokunin/PROVINCE.md:3-12\`).`"

12. `read /home/vgpnk/Projects/shokunin/kumitate-shokunin/PROVINCE.md`
    → `:3` "`**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime`" —
    no display ground anywhere in 58 lines.

13. `grep -rniE 'omarchy-menu-keybindings|omarchy-menu' --include=*.md --include=*.py --include=*.sh --include=*.mjs --include=*.txt --include=*.c -l . | grep -v '^./mado-shokunin' | grep -v '^./.ufo' | head -20`
    → one hit, `./kotoba-shokunin/.ufo/waves/round-67/w1/SentScope.md` (a path mention of the older
    `shokuknow/lanes/mado/round15/fetch/omarchy-menu.sh`, not the keybindings payload).

14. `grep -rniE 'exclusive zone|exclusive_zone|reserved band|reserved_band|layer arrangement|layer-arrangement' --include=*.md --include=*.py --include=*.sh --include=*.mjs --include=*.c . | grep -v '^./mado-shokunin' | grep -v '^./.ufo' | grep -v '^./.scratch' | head -30`
    → three kasegi `ConnSibling.md` copies (package-id "reserved band"), nothing else.

15. `for d in */; do if [ -d "$d/tools" ]; then echo "HAS tools: $d"; fi; done; for d in */; do if [ -d "$d/scripts" ]; then echo "HAS scripts: $d"; fi; done`
    → tools: chousa kaidoku kama kotodama mado mori souji tameshi tsukuroi; scripts: kake kumitate tabi.

16. `grep -rniE 'waybar|layer[_-]?shell|exclusive|pgrep|reserved|runbook|hyprland' --include=* chousa-shokunin/tools kaidoku-shokunin/tools kama-shokunin/tools kotodama-shokunin/tools mori-shokunin/tools souji-shokunin/tools tameshi-shokunin/tools tsukuroi-shokunin/tools | head -40`
    → chousa `research-gate.sh` "exclusive flock(2)"; kaidoku `disposition: "exclusive"`; no layer/zone.

17. `read /home/vgpnk/Projects/shokunin/mado-shokunin/PROVINCE.md`
    → confirms mado's owned plane and the read-only rule; `tools/mado-verify.sh` row names `pgrep` among
    its live read-only probes (mado's own, not a sibling's).

---

## Phase 2 — the round's own anchors

18. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && ls -R .ufo/waves/round-81 | head -80`
    → `claims-declaration-r81.md`, `controls/{c1-cases-r81.json,c2-runbook-cases-r81.json}`, `fetch/{S478.bin,S479.bin}`,
    `receipts/`, `w1/{R81ConnSiblings,R81ExecC2Run,R81ScoutLive}`, `w1-dispatch.json`, `w1-spec.json`.

19. `read .ufo/waves/round-81/claims-declaration-r81.md`
    → `:27` "`**Claim.** The bar-footprint join models the four reachable classes round 80 recorded as`";
    `:93` "`now bound on the **action column** that \`omarchy-menu-keybindings --print\` prints with`";
    C2 predicate `executed=26, matched=26, shapes=21/21, anchors=26/26, rows=26/26, control_new=0/2, killed=23`.

20. `cd /home/vgpnk/Projects/shokunin/kumitate-shokunin && ls -R .ufo/waves/round-81 | head -50`
    → `plan.md`, `probe/`, `open/`, `close/`, `w1/`; no mado ground.

21. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -n 'cut -c36-\|pgrep -x waybar\|action_column\|pid_state' SKILL.md | head -20`
    → `:254` "`| \`pgrep -x waybar \\| head -n 1\` | bare integer in 1..4194304 | 2 / 2 |`";
    `:270` "`| \`omarchy menu keybindings --print \\| cut -c36-\` | action column: … | 3 / 6 |`";
    `:271` "`| \`pgrep -x waybar\` | one or more decimal PIDs in 1..4194304 with rc 0 while the bar runs, empty stdout with rc 1 while it does not — the state is read from the pair, never frozen | 3 / 6 |`".

22. `cd /home/vgpnk/Projects/shokunin && for f in game-dev-3d-shokunin/PROVINCE.md kotoba-shokunin/PROVINCE.md kumitate-shokunin/PROVINCE.md game-dev-2d-shokunin/PROVINCE.md kengaku-shokunin/PROVINCE.md; do echo "=== $f ==="; grep -niE 'waybar|hypr|layer|exclusive|pgrep|runbook|omarchy|compositor|desktop|bar' "$f" | head -12; done`
    → `game-dev-3d:75` (routing), `kotoba:72` (census row), `kumitate:12-13` ("origin script layer"
    / "origin runtime layer" — architecture layers), `game-dev-2d:17` (`TileMapLayer`),
    `kengaku:380` (sandbox note).

23. `cd /home/vgpnk/Projects/shokuknow/merge/mado && grep -rliE 'waybar|exclusive|layer-shell|layer_shell|pgrep|runbook|barfoot|reserved' knowledge/corpus/knowledge amendments/corpus/knowledge`
    → 15 files, all `host-*`/`idle-lock*`/`waybar-module-text-route`/`event-delivery-limits`/
    `glyph-and-geometry`; nothing named `bar-footprint*`.

24. `cd /home/vgpnk/Projects/shokunin/kumitate-shokunin && head -40 .ufo/waves/round-81/plan.md`
    → `C1 … capability acquisition \`ready-handoff\``; `C2 … OMP shape receipt` — no mado ground.

25. `cd /home/vgpnk/Projects/shokuknow/merge/mado && for f in knowledge/corpus/knowledge/host-bar-and-idle-binding-r26.md knowledge/corpus/knowledge/host-bar-producers-r28.md knowledge/corpus/knowledge/host-producer-outputs-r29.md knowledge/corpus/knowledge/host-producer-current-outputs-r30.md amendments/corpus/knowledge/waybar-module-text-route-r25.md knowledge/corpus/knowledge/glyph-and-geometry-r31.md knowledge/corpus/knowledge/event-delivery-limits-r26.md; do echo "=== $f ==="; grep -niE 'exclusive|layer-shell|layer_surface|pgrep|runbook|anchor|margin|reserved|round|overflow' "$f" | head -8; done`
    → `host-bar-producers-r28.md:60` "`> "if pgrep -x hypridle >/dev/null; then"`" and
    `host-producer-outputs-r29.md:21` "`> "if pgrep -f \"^gpu-screen-recorder\" >/dev/null; then"`";
    no `exclusive`/`layer-shell`/`runbook` anywhere.

26. `cd /home/vgpnk/Projects/shokunin && grep -rniE 'pgrep' mori-shokunin/tools mori-shokunin/PROVINCE.md mori-shokunin/SKILL.md | head -25`
    → `mori-census.sh:231` "`#   MORI_PGREP_BIN       default pgrep`", `:315` "`PGREP_BIN=${MORI_PGREP_BIN:-pgrep}`",
    `:713` "`pids=$(printf '%s\n' "$CAP_OUT" | grep -E 'shokunin-watchdog' | grep -vF 'pgrep' || true)`",
    `:719` "`emit_finding WATCHDOG_PROBE_UNAVAILABLE info "pgrep unavailable — daemon liveness UNKNOWN, not absent"`".

27. `cd /home/vgpnk/Projects/shokuknow/merge/mado && grep -rniE 'barfoot|footprint|gtk-layer-shell|exclusive zone|reserved band' . | head -20`
    → no output, rc 0 (pipeline `head`); confirmed cleanly in cmd 72.

28. `cd /home/vgpnk/Projects/shokuknow/merge/mado && sed -n '45,80p' knowledge/corpus/knowledge/host-bar-producers-r28.md`
    → `### §2 The one producer coupled to the idle plane` … "`> "if pgrep -x hypridle >/dev/null; then"`",
    "`**INF** The bar's idle element is a *process probe*, not a compositor-state read`".

29. `cd /home/vgpnk/Projects/shokuknow/merge/mado && grep -rniE 'keybinding|omarchy-menu|action column|cut -c' . | head -20`
    → `SOURCES.append.md:141` S337 row for `/home/vgpnk/.local/share/omarchy/bin/omarchy-menu`;
    `idle-lock-offered-in-the-bar-r15.md:12` the same citation. No `keybindings --print`.

30. `cd /home/vgpnk/Projects/shokunin && grep -rniE 'exclusive|layer[_-]?shell|reserved' mado-shokunin/corpus/knowledge/*.md | head -20; ls mado-shokunin/corpus/knowledge/ | grep -iE 'bar|foot'`
    → `bar-footprint-composition-r80.md`, `bar-footprint-margins-r78.md`, `bar-footprint-r77.md`,
    `bar-footprint-reserve-r79.md`, `host-bar-producer-census-r40.md`, `waybar-*` — mado owns the ground.

31. `cd /home/vgpnk/Projects/shokunin && python3 -c "import json; d=json.load(open('kotoba-shokunin/verifiers/fixtures/compare-harness-independent/record-map-24-composition/live.json')); print(type(d), list(d)[:20])"`
    → `['observed', 'modes', 'verdicts', 'summary_paths', 'results']`; the `observed.omp` block carries
    `catalogue_total`, `offered_skills`, `dangling_entries`, `descriptions_over_cliff` — an omp
    skill-catalogue record map, not a bar artifact.

32. `cd /home/vgpnk/Projects/shokunin && grep -rn 'omarchy' kotoba-shokunin/verifiers/*.py | head -10; grep -n 'skills-root\|lane-absent\|drifted' kotoba-shokunin/verifiers/check_host_skill_surfaces.py`
    → the tool takes `--skills-root` and classifies `identical / drifted / lane-absent`; no hardcoded
    `omarchy`.

33. `cd /home/vgpnk/Projects/shokunin && grep -n 'liveness\|Liveness' mori-shokunin/PROVINCE.md mori-shokunin/SKILL.md | head -12`
    → `PROVINCE.md:6` "`**Owns (read-only probes):** shokunin watchdog liveness (pid, start time, log`";
    `:48` "`- **FR5 — Watchdog daemon identity and degraded-pgrep visibility** … Boundary: an unavailable pid probe is not absence, and argv-substring matches do not establish daemon identity.`";
    `SKILL.md:790` "`| \`pgrep\` exits 1, or exits 2 or 3, or the binary is missing | exit 1 is absence for that one query; exit 2 or 3 and a missing binary are \`unavailable\`, never absence | that a failed or blind probe proves the watchdog is gone |`".

34. `cd /home/vgpnk/Projects/shokunin && sed -n '1,25p' mori-shokunin/tools/mori-driver-liveness.py`
    → `"""Hyaku driver-liveness reader (round 56, C1 — coverage advance, frontier FR5).` … reads
    `.ufo/watchdog.log` launch/complete/dead lines. Log grammar, not a pgrep probe.

35. `cd /home/vgpnk/Projects/shokunin && sed -n '3040,3055p;3155,3165p;3200,3210p' mori-shokunin/tools/mori-census.sh`
    → `rc_of() { local f="$fx/stub/$1.rc"; … }`, `for c in pgrep journalctl df tmux git; do ln -s .dispatch "$bin/$c"; done`,
    `printf '1234 bash /path/scripts/shokunin-watchdog.sh\n' > "$d/stub/pgrep"` + `printf 0 > "$d/stub/pgrep.rc"`.

36. `cd /home/vgpnk/Projects/shokunin && grep -oE '"[^"]*waybar[^"]*"' kotoba-shokunin/verifiers/fixtures/compare-harness-independent/record-map-24-composition/live.json | head -5`
    → one long string: the `omarchy` skill `description`, containing `~/.config/waybar/`,
    `keybindings`, `layer rules`, `user-facing omarchy commands`, `Excludes Omarchy source development`.

37. `cd /home/vgpnk/Projects/shokunin && grep -niE 'waybar|layer.?shell|exclusive.?zone|reserved.?band|omarchy|pgrep|hyprctl|hyprland|compositor' */PROVINCE.md | grep -v '^mado-shokunin/' | head -30`
    → five lines total: `game-dev-3d:75`, `kengaku:380`, `kotoba:72`, `mori:48`, `tsukuroi:124`
    (the full set is `sweep-e-province.txt`).

38. `cd /home/vgpnk/Projects/shokunin && grep -niE 'pgrep -x|waybar|omarchy-menu|cut -c' */SKILL.md | grep -v '^mado-shokunin/' | head -20`
    → two lines: `mori-shokunin/SKILL.md:790`, `tabi-shokunin/SKILL.md:1343`
    ("`| daemon | no listener on 10086 (\`→ 0\`); no \`kimi-webbridge\` process (\`→ 0\`); … | \`ss -ltn | grep -c 10086; pgrep -x kimi-webbridge | wc -l\` |`").

39. `cd /home/vgpnk/Projects/shokuknow/merge/mado && sed -n '15,40p' MERGE-REPORT.md`
    → the entry table; the Waybar rows are S207/S208/S214/S224/S228/S231 (module text producers), no
    `bar-footprint`, no `runbook`.

40. `cd /home/vgpnk/Projects/shokunin && sed -n '44,52p' mori-shokunin/PROVINCE.md; sed -n '786,792p' mori-shokunin/SKILL.md`
    → FR5 boundary line; the five-row `Situation / What to conclude / What not to conclude` table whose
    fourth row is the exit-status rule quoted in cmd 33.

41. `cd /home/vgpnk/Projects/shokunin && sed -n '118,130p' tsukuroi-shokunin/PROVINCE.md`
    → `| OUT-004 | ADJ-03 | \`mado-shokunin/PROVINCE.md\` @ \`a4046a821608\` | … | Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and screen/idle behavior. |`

42. `cd /home/vgpnk/Projects/shokunin/kumitate-shokunin && ls -R .ufo/waves/round-81/w1/ 2>&1 | head -50; cat .ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt | head -30`
    → seat list incl. `K81ConnOverlap.md`, `K81ConnOverlap-captures/`; capture head:
    "`$ grep -rIn -iE 'attack.?share|connector|planner|band[^a-z]|admission|preflight|pre-dispatch|godspeed' kake-shokunin/scripts tabi-shokunin/scripts */tools`".

43. `cd /home/vgpnk/Projects/shokunin/kumitate-shokunin && grep -n 'mado' .ufo/waves/round-81/w1/K81ConnOverlap.md; grep -rln 'mado' .ufo/waves/round-81/w1/K81ConnOverlap-captures/`
    → `46:  \`kumitate\` 36. \`tools/\`: \`chousa\` 26, \`kaidoku\` 439, \`kama\` 141, \`kotodama\` 383, \`mado\` 26,`;
    three captures name mado: `grep-01-inventory.txt`, `grep-04-age-stale.txt`, `grep-05-admission.txt`.

44. `cd /home/vgpnk/Projects/shokunin && grep -n 'omarchy' kotoba-shokunin/.ufo/waves/round-67/w1/SentScope.md | head -5; grep -n 'mado' .ufo/reports/round-81/kumitate.md | head -10`
    → `657:/home/vgpnk/Projects/shokuknow/lanes/mado/round15/fetch/omarchy-menu.sh`;
    no `mado` line in kumitate's r81 report.

45. `cd /home/vgpnk/Projects/shokunin/kumitate-shokunin && head -45 .ufo/waves/round-81/w1/K81ConnOverlap.md`
    → the seat's own scope statement and its command table (`ready-handoff`, `omp-census`, probes) — a
    lane-local overlap scan of *tooling*, not of the compositor ground.

46. `ls -d /home/vgpnk/Projects/shokuknow/lanes/mado; ls /home/vgpnk/Projects/shokuknow/lanes/mado | head; ls /home/vgpnk/Projects/shokuknow/lanes/mado/round15/fetch | head -20`
    → the older `lanes/` tree exists beside `merge/`; its `round15/fetch/` holds
    `omarchy-menu.sh`, `host-omarchy-toggles-state-sweep.txt`, `host-waybar-dated-backups-sweep.txt`, …
    (a different tree from the staged package — named in H7).

47. `cd /home/vgpnk/Projects/shokuknow/merge/mado && grep -cE '^\| S[0-9]+' SOURCES.append.md; grep -nE '^\| S[0-9]+' SOURCES.append.md | grep -iE 'waybar|bar |layer|exclusive|omarchy-menu|keybind' | head -10`
    → `147`; the filtered rows are S205, S207, S208, S209, S211, S212, S214, S224, S228, S231 — all
    dispatcher/module-text producers.

48. `cd /home/vgpnk/Projects/shokunin/kumitate-shokunin && cat .ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-01-inventory.txt`
    → `21` `*-shokunin/` dirs; scripts: `kake 38`, `kumitate 36`, `tabi 64`; tools:
    `chousa 26`, `kaidoku 439`, `kama 141`, `kotodama 383`, `mado 26`, `mori 130`, `souji 156`,
    `tameshi 75`, `tsukuroi 121`.

---

## Phase 3 — the frozen C2 set and the two matcher kinds

49. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -n 'action_column\|pid_state' quality/counters/c2-r81-runbook.py | head -20`
    → `:344 if kind == "action_column":`, `:408 if kind == "pid_state":`, plus the six mutant anchors at
    `:105-109`, `:142`.

50. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -c "import json; d=json.load(open('.ufo/waves/round-81/controls/c2-runbook-cases-r81.json')); cs=d['cases']; print(len(cs)); …"`
    → `26`; `{"argv": ["/bin/sh", "-c", "omarchy menu keybindings --print | cut -c36-"], "kind": "action_column", "name": "keybindings-actions", … 6 negatives …}`
    and `{"argv": ["/bin/sh", "-c", "pgrep -x waybar"], "kind": "pid_state", "name": "waybar-pgrep", "negatives": [{"out": "", "rc": 0}, {"out": "1720\n", "rc": 1}, {"out": "0\n", "rc": 0}, {"out": " 1720\n", "rc": 0}, {"out": "", "rc": 2}, {"out": "1720x\n", "rc": 0}], "samples": [{"out": "1720\n", "rc": 0}, {"out": "1720\n1721\n", "rc": 0}, {"out": "", "rc": 1}]}`.

51. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && head -25 .ufo/waves/round-80/fetch/S473.txt; grep -n 'PRINT\|--print\|print)' .ufo/waves/round-80/fetch/S473.txt | head -8`
    → `# omarchy:summary=Display Hyprland keybindings defined in your configuration using walker for an interactive search menu.`;
    `243:if [[ $1 == "--print" || $1 == "-p" ]]; then`.

52. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -c "… negatives summary …"`
    → five negatives carry 100 lines, one carries 99, one has `rc=1`.

53. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && cat .ufo/waves/round-81/receipts/measurement-c2-r81.txt | head -40`
    → `MADO_R81_PROBE: name=keybindings-actions row=24 kind=action_column match=yes rc=0 out=' → Terminal\n → Tmux\n → Browser\n → File manager\n → Launch apps\n → Omarchy menu\n → …'`;
    `MADO_R81_PROBE: name=waybar-pgrep row=25 kind=pid_state match=yes rc=0 out='1720'`;
    `MADO_R81_PROBE: name=waybar-process row=8 kind=int_range match=yes rc=0 out='1720'`.

54. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -c "… per-negative structural diff …"`
    → negatives 2/3 look conforming to a crude check; cmd 56 resolved them.

55. `read .ufo/…/counters/c2-r81-runbook.py:340-420`
    → `if kind == "action_column": prefix = value.get("prefix", " → "); lines = text.splitlines(); floor = value.get("min_lines", 1); … if not line.startswith(prefix): return False; action = line[len(prefix):]; if not action or action != action.strip(): return False; if "→" in action: return False`;
    `if kind == "pid_state": … if rc == 0: … numeric … in_range … return bool(lines) and numeric and in_range; if rc == 1: return text == ""; return False`.

56. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -c "… exact violation per negative using value={'min_lines':100,'prefix':' → '} …"`
    → `NEG [(50, 'prefix', "'→ Action 50'")]`, `NEG [(50, 'action-empty-or-pad', "' → '")]`,
    `NEG [(50, 'action-empty-or-pad', "' → Action 50 '")]`, `NEG [(50, 'arrow-inside', "' → Action 50 → tail'")]`,
    `NEG ['floor']`, `NEG []` (the last fails on `rc=1`), and all three samples clean.
    This reproduces the claim's six negative shapes exactly.

---

## Phase 4 — the four-family sweeps (the captures)

57. `cd /home/vgpnk/Projects/shokunin && for fam in 'layer[-_]?shell|exclusive[ _-]?zone|reserved[ _-]?band|arrangeLayerArray|zwlr_layer' 'omarchy-menu-keybindings|omarchy menu keybindings|cut -c36-|action column' 'pgrep[^|]{0,30} -x|pgrep -x'; do echo "### FAMILY: $fam"; grep -rniE "$fam" … ; done`
    → the exploratory form of sweeps A/B/D; superseded by the scripted captures.

58. `cd /home/vgpnk/Projects/shokunin && grep -rniE 'pgrep +-x' --include=*.md --include=*.py --include=*.sh --include=*.mjs . | grep -v '^./mado-shokunin/' | awk -F: '{print $1}' | sort | uniq -c | sort -rn | head -20`
    → per-file counts dominated by tabi (`corpus/knowledge/webbridge-revival-assessment.md` 3,
    `corpus/evidence/w4-t4-3-sweep/procs.sh` 3), mori `round-31/w1/LiveArgvProbe.md` 6, kama
    `round-50/w1/out/X17Cleanup/hygiene.md` 6.

59. `cd /home/vgpnk/Projects/shokunin && sed -n '1335,1350p' tabi-shokunin/SKILL.md`
    → the `### T1 — Terminal state` table; the daemon row quoted in cmd 38.

60. `cd /home/vgpnk/Projects/shokunin && sed -n '205,230p' kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt`
    → the mado block, lines 216-227, quoted in the report §4.1.

61. `cd /home/vgpnk/Projects/shokunin && sed -n '1,20p' tabi-shokunin/PROVINCE.md`
    → tabi owns "`the kimi-webbridge plugin … browser inventory … CDP session discipline`" — the
    `kimi-webbridge` subject of its pgrep row.

62. `cd /home/vgpnk/Projects/shokunin && python3 -c "… MANIFEST.json lines 44430-44440 …"`
    → `44437: "multi-surface reserved-band composition",` `44438: "chord-grammar and state/exit-status runbook matchers"`.

63. `cd /home/vgpnk/Projects/shokunin && ls -la .tower/quarantine/fleet-root-strays-20261026T2055/; python3 -c "import json; d=json.load(open('.tower/quarantine/fleet-root-strays-20261026T2055/tree.json')); print(type(d), list(d)[:6])"`
    → `SHA256SUMS`, `tree.json` (347495 B); `['sha', 'url', 'tree', 'truncated']`.

64. `cd /home/vgpnk/Projects/shokunin && grep -rn 'omarchy' kotoba-shokunin/.ufo/waves/round-82 kotoba-shokunin/.ufo/waves/round-84 | head -5`
    → one hit in a round-82 probe file; no `omarchy` in either census receipt.

65. `cd /home/vgpnk/Projects/shokunin && python3 -c "… MANIFEST.json lines 44420-44440 …"`
    → the r80 mado record: `"lane": "mado"`, `"lane_round": 80`, `"report": ".ufo/reports/round-80/mado.md"`.

66. `cd /home/vgpnk/Projects/shokunin && grep -n 'mado-shokunin' kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt | head -5; … | tail -3; head -3 …`
    → first hit `216:`, 36 hits total; the file's first line is the `band[^a-z]` grep.

67. `cd /home/vgpnk/Projects/shokunin && python3 -c "… MANIFEST.json lines 44385-44422 …"`
    → shows the record that *precedes* the mado one (mori round 85 at `44386-44408`), so the mado record
    begins at `44409` — the block quoted in `sweep-h-fleet-root.txt`.

68. `cd /home/vgpnk/Projects/shokunin && ls kotoba-shokunin/.ufo/waves/round-82/receipts kotoba-shokunin/.ufo/waves/round-84/receipts | head -20; grep -rn 'omarchy' …/receipts`
    → receipts exist; no `omarchy` line in them.

69. `cd /home/vgpnk/Projects/shokunin && grep -n 'omarchy' kotoba-shokunin/.ufo/waves/round-82/receipts/after-host-skill-census-ledger.txt; head -12 …`
    → `grep` rc 1 (no line); head:
    "`# command: python -B verifiers/check_host_skill_surfaces.py --skills-root C:/Users/jpvei/.zcode/skills --fleet-root <workspace>/fleet`",
    then `DRIFT kagi-shokunin …`, `LANE-ABSENT kimicu-bridge …`, `LANE-ABSENT phone-bridge …`, `LANE-ABSENT shokunin …`.

70. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -n 'omarchy menu keybindings\|omarchy-menu-keybindings' SKILL.md corpus/knowledge/*.md | head -6`
    → `SKILL.md:73`, `:74`, `:216`, `:267`, `:268`, `:270` — the row ladder; the dispatcher form is
    `omarchy menu keybindings --print`, the payload cited in the declaration is `omarchy-menu-keybindings`.

---

## Phase 5 — the scripted captures

71. `cd /fast/scratch/hyaku/mado-r81/R81ConnSiblings && sh /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/w1/R81ConnSiblings/sweep.sh`
    → first run wrote 11 captures. **Two defects, both found and fixed before anything was cited:**
    - `sweep-b` was flooded by the homonym `action column` (kaidoku, 233 files) → narrowed to the
      `omarchy…|cut -c36-` token family plus a per-lane *count* of the homonym.
    - `sweep-g` never `cd`'d into the package (`ls: cannot access 'knowledge/corpus/knowledge': No such
      file or directory`, `rc(no-match forms)=2`), so its empty result was vacuous → added
      `cd "$K" || { printf 'CD FAILED\n'; exit 1; }` and `pwd`.

72. `cd /fast/scratch/hyaku/mado-r81/R81ConnSiblings && sh …/sweep.sh >/dev/null 2>&1; echo "rc=$?"`
    → `rc=0`; re-read `sweep-g-merge-package.txt`:
    `$ pwd` → `/home/vgpnk/Projects/shokuknow/merge/mado`;
    `65` knowledge entries, `4` amendments;
    the `\bexclusive\b|gtk-layer-shell|barfoot|footprint|reserved band|arrangeLayerArray` grep → **no output**;
    `omarchy-menu-keybindings` → **no output**;
    `omarchy-menu|keybindings --print|menu keybindings` → one line (`idle-lock-offered-in-the-bar-r15.md:12`);
    `pgrep` → 16 result lines in 7 entries (all `hypridle` / `^gpu-screen-recorder`; the capture's
    `grep -c pgrep` reads 17 because it also counts the echoed command line);
    `runbook` → no output, `rc(no-match forms)=1`.

73. `cd /fast/scratch/hyaku/mado-r81/R81ConnSiblings && sh …/sweep2.sh`
    → wrote `sweep-l1…l5`. `sweep-l2-instrument-families.txt` is a one-line file
    (`kama-shokunin/tools/round64-c2-counter.py:264`) plus `rc=0 (1 = no hits)` — note `rc` here is
    `grep -v`'s, so read the line, not the rc label.

74. `cd /home/vgpnk/Projects/shokunin && sed -n '250,300p' kama-shokunin/tools/round64-c2-counter.py`
    → `def pgrep_set():` "`"""Live llama-server pids (`pgrep -x llama-server`), zombies dropped through /proc/<pid>/stat as the context-capacity tool does."""`",
    `p = subprocess.run(['pgrep', '-x', 'llama-server'], capture_output=True, text=True)`.

75. `cd /home/vgpnk/Projects/shokunin && ls -la .ufo/reports/round-81/ | head -14; head -30 .ufo/reports/round-81/mado.md`
    → `-rw-r--r-- 1 vgpnk vgpnk 15444 Nov  4 09:49 mado.md` (it was absent at 09:44 — a concurrent L1
    write); its head carries both grounds and `:14` "`… models the three reachable`".

76. `cd /home/vgpnk/Projects/shokunin && head -30 tabi-shokunin/.ufo/waves/round-34/w2/ConnSiblingDrift/mado.diff; wc -l …`
    → `diff --git a/SKILL.md b/SKILL.md`; `126` lines.

77. `cd /home/vgpnk/Projects/shokunin && grep -nE 'applyExclusive|arrangeLayerArray|arrangeLayersForMonitor|CReservedArea|addreserved|reserved' tabi-shokunin/.ufo/waves/round-34/w2/ConnSiblingDrift/mado.diff | head -8`
    → `59:+**OBS** S303 - … \`addreserved\` changes the same-selector rule's reserved area, …`
    — mado's round-45 prose inside a tabi file.

78. `cd /home/vgpnk/Projects/shokunin && grep -n 'reachable classes\|NOT_MODELLED' mado-shokunin/.ufo/waves/round-81/claims-declaration-r81.md .ufo/reports/round-81/mado.md mado-shokunin/corpus/knowledge/bar-footprint-composition-r80.md | head -12`
    → `claims-declaration-r81.md:27` "four reachable classes"; `.ufo/reports/round-81/mado.md:155`
    "`§11 items 1–3`"; r80 `:11` "the second *dynamic* consumer `NOT_MODELLED`".

79. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && sed -n '180,196p' corpus/knowledge/bar-footprint-composition-r80.md; sed -n '14,22p' /home/vgpnk/Projects/shokunin/.ufo/reports/round-81/mado.md`
    → r80 `:188-190` "`four classes are wrong, all outside the frozen 33's declared shapes`";
    r81 report `:14-15` "`models the three reachable / classes round 80 recorded as \`NOT_MODELLED\``".

80. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -n '"exclusive"' tools/mado-barfoot.py | head -12; sed -n '38,52p' tools/mado-barfoot.py`
    → `633:        exclusive = item.get("exclusive", "auto")`;
    `749:        "exclusive": "auto" if bar["exclusive"] else 0,`.

81. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -n 'exclusive' tools/mado-barfoot.py | sed -n '1,30p'`
    → the full list, incl. `31: (src/layer-surface.c layer_surface_update_auto_exclusive_zone)`,
    `94: # first match; the match is (exclusiveEdge == singular) or (anchor == singular)`,
    `276: raise Unmodelled("a negative margin can void or invert the exclusive band; not modelled")`.

82. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -c "… walk c1-cases-r81.json for surface dicts with layer+anchor and no exclusive …"`
    → `cases 39` / `surfaces declared without an exclusive key: 0`.

83. `cd /home/vgpnk/Projects/shokunin && grep -nE 'applyExclusive|addreserved|arrangeLayerArray|CReservedArea|exclusive' kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt | head -12`
    → `223:… addreserved …`, `226:… exclusive band …` (the other ground phrases are at 216/225).

84. `cd /home/vgpnk/Projects/shokunin && grep -nE 'applyExclusive|addreserved|CReservedArea' MANIFEST.json | head -5; grep -n '^diff --git' tabi-shokunin/.ufo/waves/round-34/w2/ConnSiblingDrift/mado.diff`
    → `44123:` the r79 mado capability note "`static-reserve composition over the usable box (mado r79 C1: the monitor addreserved reserve …)`";
    the diff touches exactly two files (`SKILL.md`, `corpus/knowledge/hyprland-monitor-rule-r45.md`).

85. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -n '^[0-9]\. \*\*' corpus/knowledge/bar-footprint-composition-r80.md | sed -n '1,8p'; sed -n '186,190p' …`
    → that pattern hit a *different* numbered list (§10); cmd 86 re-located §11.

86. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -n 'Centring past a negative tie\|auto` zone on a dynamic\|auto` on a corner\|A declared surface with no' corpus/knowledge/bar-footprint-composition-r80.md; sed -n '205,216p' …`
    → `192:` item 1, `197:` item 2, `203:` item 3, `205:` item 4
    ("`4. **A declared surface with no \`exclusive\` key.** The declaration grammar defaults it to \`"auto"\` … while the protocol's default is \`0\` (\`S460:183\`)`"),
    and `:210-211` "`Also unpinned but *correct* in the tool (probed, no case): … a left/right attribution vector …`".

87. `cd /home/vgpnk/Projects/shokunin && grep -n 'three reachable' .ufo/reports/round-81/mado.md; sed -n '14,16p' .ufo/reports/round-81/mado.md`
    → `14:- **C1 — coverage (capability acquisition).** The bar-footprint join models the three reachable`
    `15:  classes round 80 recorded as \`NOT_MODELLED\` (…bar-footprint-composition-r80.md`.

---

## Phase 6 — writes

88. `write .ufo/waves/round-81/w1/R81ConnSiblings/sweep.sh` (then two `edit`s: narrow sweep B, fix the
    `printf '--'` option error in sweep D, add the package `cd` and restore the fleet `cd` before sweep H).
89. `write .ufo/waves/round-81/w1/R81ConnSiblings/sweep2.sh`.
90. `write .ufo/waves/round-81/w1/R81ConnSiblings.md` (the report; 30430 B).
91. `write .ufo/waves/round-81/w1/R81ConnSiblings/findings.md` (this file).

Read-only `read` calls not itemised above, all by path and range:
`kotoba/province`, `game-dev-3d/province`, `kumitate/province`, `mado/province`,
`bar-footprint-composition-r80.md:190-245`, `c2-r81-runbook.py:340-420`,
`claims-declaration-r81.md`, `sweep-*` captures.

---

## The lines that decide the three answers

- **Q1.** `sweep-l2-instrument-families.txt` is one hit, and it is `kama`'s `llama-server` PID reader;
  `sweep-b-omarchy-output.txt` first block is empty; `sweep-e-province.txt` is five lines, three of which
  route the ground *to* mado. No sibling claims either ground.
- **Q2.** `sweep-g-merge-package.txt`: 65 + 4 entries; zero lines for
  `\bexclusive\b|gtk-layer-shell|barfoot|footprint|reserved band|arrangeLayerArray`; zero for
  `omarchy-menu-keybindings`; one line for `omarchy-menu` (S337, a different payload); 16 `pgrep` lines
  across 7 entries, all the `hypridle` producer probe; zero `runbook`.
- **Q3.** Four artifacts carry mado's words or the round's own pinned source while living outside mado:
  `kumitate…/K81ConnOverlap-captures/grep-05-admission.txt` (36 mado lines, incl. `reserved band`,
  `gtk-layer-shell's auto zone`, `exclusive band`), `tabi…/ConnSiblingDrift/mado.diff` (`addreserved`,
  126 lines), `.tower/quarantine/…/tree.json` (Hyprland at `efb5099378…` with `LayerShell.cpp`), and
  `kotoba…/record-map-24-composition/live.json` (the `omarchy` skill description with `waybar`,
  `keybindings`, `layer rules`). Prevention: merge on subject + mechanism, and attribute by directory,
  never by the lane name inside a file.

STATUS: ok
