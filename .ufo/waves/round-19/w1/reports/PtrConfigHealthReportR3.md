# PtrConfigHealthReportR3 — freshness pointer appended to config-health-report-r3.md; its one 2.17.0 pin (line 900) is now dated and bound to S090

Scope: R18-V3 forward pointer for `corpus/knowledge/config-health-report-r3.md` (sole writer this wave). Append-only.

## Findings

- `grep -n '2\.17\.0'` on the note (before write) returned exactly one line: `900: waybar --version; walker --version; swayosd-server --version; hyprlock --version   # v0.15.0 / 2.17.0 / 0.3.2 / v0.9.6`. That is the `walker --version` expectation in the round-4 R.4 command block (`## Reproduction package (round 4)`). Measurement date: 2026-10-14 (probe window, line 3; kit K2 runs, lines 951-953).
- Appended block `## Freshness pointer (round 19, 2026-10-20)` (8 lines) at the tail of the note. First bullet contains both `2.17.2` and `S090` on one line; it cites `/var/log/pacman.log:2929` (S090), the 2.17.0 window start at line 1943 (S090), and `walker-route-r18.md` as current routing.
- Bullets classify the walker-touching claims:
  - version-bound and dated: version print (line 900); help-text statement (line 249);
  - service/process state (lines 245-246, 896): dated, PID 1808 may be superseded by restart hooks at `/var/log/pacman.log:3062` and `:3123` (S090), current PID `[UNK]`;
  - version-independent file bytes, dated, not re-measured: walker config (lines 242-243, 645), autostart desktop (243-244, 657), theme `walker.css`/`style.css`/`layout.xml` (270, 915-916); 2.17.2 behaviour on them `[UNK]` per walker-route-r18.md;
  - launch path / PATH presence (lines 252-255, 902): omarchy-defined, not walker-version-bound.
- Not asserted anywhere in the block: any live 2.17.2 value. Behaviour of the 2.17.2 binary remains `[UNK]`.
- Template deviation: the operator template mentioned a binary compiled-in version literal "read as file bytes (S096)". No S096 row exists in `corpus/SOURCES.md` and no such measurement is in the note or S090/walker-route-r18.md, so that clause was omitted rather than asserted. The bullet cites S090 only.

## Receipts

- Before: `sha256` `acf59f9b06c63cec1ee1f15b97981ec5f55765bc6e386c73f5f3c5392e8fe5e9`, 62,249 B.
- After: `sha256` `7432f1dd245fca72230c249b61f90a6813bc3944b4f50561a24634bd2d3cde23`, 63,705 B (block 1,456 B).
- Prefix check: `head -c 62249 <new> | sha256sum` = `acf59f9b…8fe5e9` (equal to before); `cmp -n 62249` against a pre-write copy in `/tmp/r19-ptr/old.md`: IDENTICAL.
- Process note: the first append was followed by one rewrite of the appended suffix only (to add the routing sentence to bullet 1); the prefix was re-verified by `cmp` before and after that rewrite. No existing byte of the note was changed.
- Note's original last byte had no trailing newline; the block begins with a blank line so the boundary is clean.

## Limits

- Only `grep -n '2\.17\.0'` was used to find pins; I did not read the note's full 1,006 lines for other version-language (e.g. unversioned "walker" statements beyond the lines listed above were classified by reading only the walker grep hits).
- Host pause respected: no walker, pacman, systemctl, omarchy or any process/package query; host files read as bytes only (in fact, this task required no host reads; S090 and walker-route-r18.md were read as notes).
- Nothing re-measured live; no claim of 2.17.2 runtime behaviour.
- Pre-existing `S0xx` references in the note are not re-audited.

## Installs

none
