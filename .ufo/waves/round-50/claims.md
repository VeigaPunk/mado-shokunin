# mado round 50 — declared claims (intent; predicates freeze after wave w1, before any data commit)

Base `8ae47b957034ae21012bbf09173cca2c48be345e` (lane tip at round start = the round-49 closure commit). Round shape: two v1
waves — `w1` build + attack of the round-49 instruments (it carries the 38 never-dispatched items of
`.ufo/waves/round-49/w2-items.json`, retargeted, plus round-50 build items), then `w2` falsify against the round-50 freeze. No
seat scores a round-50 frozen counter in `w1`; predicates, counters, fixtures and do-nothing controls freeze in
`registration.md` after `w1` returns, and each control is scored with the frozen counter (round-49 D4).

Lowest-axis rule: the published axis table sits tied at its maximum at base (`receipts/axis-base.txt`: navigation 65/65,
calibration 86/86, operability 12/12, `checked=3 mismatched=0`), so no single axis is lowest. The round-49 closure ruled
coverage `unchanged` (C2 honest stop) and expansion improved only through a capability row, so C1 is the expansion move and the
round's sourced claim; C2 is the quality-trend move.

- **C1 — coverage (sourced): `corpus/knowledge/hyprland-bind-key-match-r50.md`.** The round-49 C2 carry. How Hyprland 0.56.2
  (`efb50993`) turns the key field of a `bind` line into something a key press matches: key name to keysym (case handling,
  `code:` keycodes, the other key forms), which keysym of a pressed key is compared (the xkb state used,
  `input:resolve_binds_by_sym`), how modifiers are compared — grounded on registry rows opened and appended this round (S352..,
  Hyprland at `efb50993`, libxkbcommon 1.13.2, the Hyprland wiki at a pinned commit, re-fetched this round and compared
  byte-for-byte with the round-49 pins) and a read-only `hyprctl binds -j` / `hyprctl getoption input:resolve_binds_by_sym -j`
  capture taken this round. Ground held open at base: `corpus/knowledge/keybind-rule-semantics.md` §2.3 states the key forms
  at `[INF-docs]` level only, and `corpus/knowledge/hyprland-input-devices-r46.md:71` names bind resolution as outside its join.
  Counter: the round-49 `PRED-C2-r49` instrument re-pointed to round 50 (base, lesson, fetch and receipt paths) and repaired
  for whatever `w1` breaks, frozen as `PRED-C1-r50`. Surface moved: bind key matching, frontier → core.
- **C2 — operability: the session-material gate v3 installed at `quality/check-session-material.py`.** At base the installed
  gate (v2, sha256 `82c9053a…`) scans `.ufo/` only and reports 0 findings on the round-48 receipt shapes that carry a host
  home path or the account name structurally (`.ufo/waves/round-49/w1/ExecSessionShapes/receipts/e2e-v2-blind-v3-red.txt`:
  `v2 --scope all rc=0 files=5 findings=0`). After: the installed gate detects every red instance of the frozen shape set
  (structural home-path prefix forms, account owner/group column, exec-cache record fields, material outside `.ufo/`) in
  nonce-generated fixture repositories and flags none of the green counter-shapes (`~`/`$HOME` forms, paths in prose, numeric
  ids), with its selftest passing and every v2 selftest case name kept. Counter frozen as `PRED-C2-r50` after `w1`. Surface
  moved: the lane's evidence-privacy gate (round-48 M48-8, routed by the round-48 and round-49 closures).

Separable: C1's counter reads only the entry, registry, lesson, README, pins and the live receipt; C2's counter reads only
`quality/check-session-material.py` at the revision and its own generated fixtures.

Non-claim routed items (round-49 closure `corpus/lessons/round-49-verifier-spotcheck.md` §6), each with its own receipt:
D1 (round size and the 38 w2 items: run in `w1`), D2 (final state of the 7 unsettled round-49 seats; this report only after
WAVE-DONE of every wave), D3 (the 57,865-pair figure: receipt or correction), D4 (do-nothing control on the frozen round-49 C1
counter), D5 (= C1), D6 (QUALITY criteria for M49-1 and M49-3), D7 (host guard M48-10 installed with a both-ways receipt; gate
= C2), D8 (lesson gate-count correction with its command).
