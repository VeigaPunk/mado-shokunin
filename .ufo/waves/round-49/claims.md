# mado round 49 — declared claims (intent; predicates freeze after wave w1)

Base `03e4ae76aff7a4be59cb69970dd553baa319695a` (lane tip at round start = the round-48 closure commit). Round shape: two v1
waves — `w1` build, then `w2` falsify against the frozen instruments. No seat scores a frozen counter in `w1`; predicates,
counters, fixtures and controls freeze in `registration.md` after `w1` returns and before any data commit.

Lowest-axis rule: the published axis table sits tied at its maximum (round-48 tip receipt
`.ufo/waves/round-48/receipts/axis-tip-final.txt`, `checked=3 mismatched=0`), so no single axis is lowest. All three trends
were ruled `improved` by the round-48 closure (`corpus/lessons/round-48-verifier-spotcheck.md` §5), so no trend is furthest
behind; C1 is the quality-trend move (operability), C2 the expansion move and the round's sourced claim. The round-48 closure's
routed items (N1-N5, M48-8, M48-10, M48-13, `w2/SentScratch`, the `registration-v2.md` residuals) and the 47 untracked
`*.synthetic` sidecars are worked as non-claim items, each with its own receipt.

- **C1 — operability (capability acquisition): `tools/mado-keysym.py`, which key and modifiers type a keysym.** Binds on this
  host name keysyms (`bind = SUPER, SLASH, ...`; `corpus/knowledge/keybind-rule-semantics.md` §2.3), but nothing in the lane
  says which physical key and which modifiers produce a keysym under the compiled keymap: the round-48 entry compiles the
  keymap (`corpus/knowledge/xkb-keymap-compile-r48.md`) and stops there, and the round-46 entry's Limits leave bind resolution
  out (`corpus/knowledge/hyprland-input-devices-r46.md:71`). After: given a compiled keymap file (the output of
  `xkbcli compile-keymap`, libxkbcommon 1.13.2, xkeyboard-config 2.48) and a keysym, the tool prints exactly what
  `xkbcli how-to-type --keymap=FILE --disable-compose --keysym ARG` prints on stdout and exits with its exit status
  (keycode, key name, layout index and name, level, every modifier mask for that level), Python 3 stdlib only, starting no
  process, opening no socket, writing nothing. Judge: the real pinned `/usr/lib/xkbcommon/xkbcli-how-to-type`
  (sha256 `f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54`) on keymaps compiled at count time from
  xkeyboard-config 2.48 RMLVO names. Surface moved: keysym-to-key resolution, frontier → core.
- **C2 — coverage (sourced): `corpus/knowledge/hyprland-bind-key-match-r49.md`.** How Hyprland 0.56.2 turns the key field of
  a `bind` line into something a key press can match — key name to keysym (case handling, `code:` keycodes, the other key
  forms), which keysym of a pressed key is compared (the layout used, `input:resolve_binds_by_sym`), how modifiers are
  compared — grounded on rows S352.. opened this round (Hyprland at `efb50993`, libxkbcommon 1.13.2, the Hyprland wiki at a
  pinned commit) and a read-only `hyprctl binds -j` / `hyprctl getoption input:resolve_binds_by_sym -j` capture. Ground held
  open at base: `keybind-rule-semantics.md` §2.3 states the key forms at `[INF-docs]` level only ("use the segment after
  `XKB_KEY_`"), and `hyprland-input-devices-r46.md:71` names bind resolution as outside its join.

Separable: C1's counter reads only the tool, its fixtures and the judge; C2's counter reads only the entry, registry, lesson,
README, pins and the live receipt.

Routed round-48 closure items (non-claim work, each with its own receipt; `corpus/lessons/round-48-verifier-spotcheck.md` §6):
N1 (untracked count is 47, with its command), N2 (the `host_cache_untouched` digest is the w2 mutant's bytes: lesson line, and
an operator-owned before/after digest pair this round — `receipts/operator-state-before.txt`), N3 (stale "five gate decisions"
line), N4 (all 98 variant rows in a text receipt), N5 (GitLab files-API fallback note), M48-8 (session-material gate: the 16
synthetic `/home/<user>` shapes and scopes beyond `.ufo/`), M48-10 (mutants run with HOME/XDG_* in scratch; operator-owned paths
digested before/after), M48-13 (seat clone recipe under a 1 MiB file cap; the owed clause-r mutant attack and the gate
both-ways demonstration), `w2/SentScratch` (counters refuse a `/tmp` work dir), the `registration-v2.md` residuals.
