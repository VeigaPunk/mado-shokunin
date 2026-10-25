## Round 40 — the option table meets the running compositor; the getoption ground admitted (2026-10-25, attempt 1)

- Attempt 1 (L1 `MadoR40`) froze `5e7e885` before any round-40 data and dispatched v2 wave `w1`
  (64 seats; spec `.ufo/waves/round-40/w1-spec.json`, dispatch `w1-dispatch.json`).
- Motivating evidence: round-39 planned item 1 — take one live `hyprctl getoption` dump (read-only)
  and merge it into the table; the round-39 tool labels a `getoption` dump file (`--getoption FILE`
  in the base usage string, `receipts/c1-before-base.txt`) and never queries the compositor itself;
  `considerthese/2026-10-24.md` proposal 4.
- Freeze `5e7e885` (before any round-40 data): registration, `PRED-C1-r40-v1` and `PRED-C2-r40-v1`
  with their control harnesses and receipts (`CTL_C1: controls=18 correct=18/18`,
  `CTL_C2: controls=21 correct=21/21`), the base receipts (`c1-before-base.txt` `fixtures=0/13`,
  `c2-before-base.txt` `admitted=0/1`, `MADO_SELFTEST: 460/460`, axis 56/56 + 51/51 + 12/12
  `mismatched=0`, census exit 0) and the native capture `c1/native-capture.jsonl` (70 host keys;
  forms int 44, float 5, custom 13, str 8).
- Wave `w1`: 64 seats, dispatched at `e2b51d3` (spec + dispatch); `<<AFTER wave reports>>`.
- C1 data `<<HASH C1 data commit>>`: `tools/mado-options.py` gains `--live` (`--hyprctl PATH`,
  `--probe KEY`) — one `hyprctl getoption -j KEY` per declared key, native replies converted per
  hyprlang v0.6.8 `configStringToInt` and the Hyprland v0.56.2 gradient/gap/font-weight handlers,
  exit 5 on a compositor failure naming the key, exit 2 on a hostile probe key →
  `<<AFTER C1 fixtures=… tool=… verdict=…>>` at the data commit and the tip
  (`<<AFTER C1 receipt paths>>`).
- C2 data `<<HASH C2 data commit>>`: `corpus/knowledge/hyprctl-getoption-native-forms-r40.md` + the
  registry rows (held S162 `ConfigManager.cpp` gradient handler and S173 hyprlang `config.cpp`
  `configStringToInt` re-opened; `<<AFTER new row count>>` new rows incl. Hyprland
  `ComplexDataTypes.hpp` at the pinned commit and one own-work census receipt) →
  `<<AFTER C2 admitted=… verdict=…>>` (`<<AFTER C2 receipt path>>`).
- Host finding (angle inheritance; provisional values from the registration's §Provisional facts,
  re-derived by `<<AFTER re-derivation seat / receipt>>`): the theme `hyprland.conf` declares
  `$activeBorderColor = rgb(e68e0d)` and `col.active_border = $activeBorderColor`; the defaults tree
  declared the same key earlier with `rgba(33ccffee) rgba(00ff99ee) 45deg`; the live read is
  `ffe68e0d 45deg` — the redeclaration carries no angle token, so the angle is inherited from the
  earlier declarer. Under that model the reference tool labels all 70 keys
  `<<AFTER host census labels>>` (`<<AFTER live census receipt>>`); the reference tool is a CONTROL
  and is never delivered.
- Assimilation (`<<AFTER assimilation commit>>`): package `merge/mado/`, theme "the host's bar
  producers" — `host-bar-producers-r28.md` and `host-producer-outputs-r29.md` re-grounded;
  `<<AFTER assimilation: N admitted, M refused with reason>>`; no staged row appended as-is; the
  id-collision guard and the quarantine slice re-derived in scratch.
- considerthese `2026-10-25.md` proposal 2 (count dead attempts and dirty closures from the watchdog
  digests) mined as a lesson table: `<<AFTER considerthese outcome>>`.
- Errata (D2, round-39 non-author closure): `corpus/lessons/round-39.md` labels the quarantined S224
  "refused (fabrication class)"; the seat evidence says a rotated volatile timestamp. Corrected by an
  appended note in `corpus/lessons/round-40.md` (append-only); the round-39 text is untouched.
- Records: lesson `corpus/lessons/round-40.md` (Gate, mistakes), SCORECARD round-40 section
  (`<<AFTER records commit>>`).
