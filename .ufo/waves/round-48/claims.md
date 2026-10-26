# mado round 48 — declared claims (intent; predicates freeze after wave w1)

Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585` (lane tip at round start = the round-47 closure commit). Round shape: two v1
waves — `w1` build, then `w2` falsify against the frozen instruments. No seat scores a frozen counter in `w1`; predicates,
counters, fixtures and controls freeze in `registration.md` after `w1` returns and before any data commit.

Lowest-axis rule: the published axis table sits tied at its maximum (round-47 tip receipt `.ufo/waves/round-47/receipts/axis-tip.txt`,
`checked=3 mismatched=0`), so no single axis is lowest. Trend furthest behind: **quality** (round-47 closure ruled it
`unprovable-but-better`, every other trend `improved`), so C1 is a quality-trend move (operability) and the routed round-47
defects D1-D4, R3, R4b are worked as non-claim items. C2 is the expansion move and the round's sourced claim.

- **C1 — operability (capability acquisition): the warm-cache path of `tools/mado-terminal.py`.** At base the tool models a
  cold cache only and declares the resolver's cache out of contract (`tools/mado-terminal.py:82-85`). The hotkey's resolver
  (`xdg-terminal-exec` v0.14.3) reads `$XDG_CACHE_HOME/xdg-terminal-exec` first and trusts it while an md5 over
  `XDG_CURRENT_DESKTOP` and `LANG=C ls -LRl` of the list/data paths still matches and the cached command resolves
  (`/usr/bin/xdg-terminal-exec:179-298`), so a stale-but-valid cache can make SUPER+RETURN start a different command than a
  cold run would. After: given the tree, environment and an existing cache file, the tool predicts the resolver's stdout and
  exit status (cache hit, miss, invalid, disabled), still starting no process and opening no socket; `explain` names the
  cache verdict. Judge: the real pinned script, primed in a sandbox, on fixtures where the warm answer differs from the cold
  one and fixtures where the cache is invalidated. Also in the same contract: HOME unset modelled as the pin (round-47 D1).
  Surface moved: the cache edge class, frontier → core (`corpus/README.md:110` lists "the warm-cache path" as still open).
- **C2 — coverage (sourced): `corpus/knowledge/xkb-keymap-compile-r48.md`.** Which `kb_rules/kb_model/kb_layout/kb_variant/
  kb_options` names compile into a keymap on this host (libxkbcommon 1.13.2, xkeyboard-config 2.48): rules → components,
  include-path order, which unknown names fail the compile and which are dropped with a warning, and how that maps onto
  Hyprland's fallback; rows S340.. opened this round; a live read-only `xkbcli compile-keymap` receipt for the host's names.
  Surface moved: the XKB compile, held open at base (`corpus/knowledge/hyprland-input-devices-r46.md:69`, "The XKB compile
  itself is not reproduced"; `corpus/README.md:112`).

Routed round-47 closure items (non-claim work, each with its own receipt): D1 contract-delta lesson line (and HOME unset in
C1's contract), D2 session-material receipt at a named revision, D3 readdir-order fixtures, D4 erratum on the round-47 entry,
R3 session-material synthetic marker, R4b round-45 errata in a form that keeps the frozen round-45 counter's verdict, M47-10
fixture schema v2, `w2/CritC1Explain.md` (explain `cmd=` compared), `w2/SentC1Sandbox.md` F1-F4.
