# PtrArcSynthesis — round-19 freshness pointer appended to arc-synthesis.md; the one walker pin (line 229) is dated and bound to 2.17.0

Scope: R18-V3 forward pointer for `corpus/knowledge/arc-synthesis.md` (sole writer this wave). Append-only.

## Lines containing `2.17.0` (before edit)

- Only one line: `corpus/knowledge/arc-synthesis.md:229` (the §3 walker row: version `2.17.0`, binary identity sha256 `64826a85…`, BuildID `a22452d1…` (r9)). Measured with `grep -n "2.17.0"` before the edit.

## Hashes and prefix check

- Before: sha256 `a5b48331414618108cdc9596cf6c7cc0dc78994ebcf61141c3e6d80428419d50`, 30,796 B (copy kept at /tmp/arc-synthesis.before.md, scratch).
- After: sha256 `8278b77a84105dbf1a22ee9efb8cc8bb1ba0b6b079dc5571889e389cfd245e05`, 32,331 B (+1,535 B).
- Prefix check: `head -c 30796 corpus/knowledge/arc-synthesis.md | sha256sum` = `a5b48331…9d50` (equal to before); `cmp -n 30796` against the before copy: identical.
- Appended block: lines 389–397 (heading at 390, bullets 392–397). The file had no trailing newline before; the block begins after `gate.` on line 388 with a blank line.

## Appended block (summary)

- Heading `## Freshness pointer (round 19, 2026-10-20)`.
- Bullet 1 (carries `2.17.2` and `S090`): line 229 pins are dated 2026-10-14 (the note's verified-at; identity r9) and describe 2.17.0; host moved to 2.17.2 at `/var/log/pacman.log:2929` (S090); routing to `corpus/knowledge/walker-route-r18.md`.
- Bullet 2 (version-bound): version string, binary sha `64826a85…`, BuildID `a22452d1…`; current host binary sha `25240650…` cited from walker-route-r18.md § Host declaration, not re-measured.
- Bullet 3 (host-state, dated, not re-measured): config parse, theme package, unit active states, socket mode/size, D-Bus owner; post-restart process state `[UNK]` (S090 rows 3062/3123).
- Bullet 4 (version-independent, kept): consumer-probe method and the UNKNOWN constraint on socket protocol and rendered UI.
- Bullet 5 (version-bound behaviour): "no reload path — restart is the apply path (r9)" dated to 2.17.0; 2.17.2 binary apply behaviour `[UNK]`.
- Bullet 6: not re-measured live this round; 2.17.2 binary behaviour stays `[UNK]`.

## Findings

- F1: The note's only 2.17.0 pin is line 229; it is now dated and bound, not re-asserted. No other content in the note was edited.
- F2: S096 is not cited: no S096 row exists in `corpus/SOURCES.md` at this time (only S090 matched `grep -n "S090\|S096"`), and the block must not point at a nonexistent row. The pointer uses S090 as instructed.
- F3: No live value was re-asserted. The host was not queried (host pause); all host facts are file-byte facts from S090 and walker-route-r18.md.

## Limits

- Only `grep -n` and `sha256sum`/`cmp`/`head -c`/`stat`/`wc`/`od`/`sed` were run on the note; no walker, elephant, pacman, systemctl, or omarchy command ran.
- The 2.17.2 binary's compiled-in version literal was not read by me; S096 is reserved and not in SOURCES.md, so nothing from it is cited.
- No SOURCES.md, README, QUALITY, LOG or SCORECARD edit: those are L1-owned.
- Note's own measurement date taken as 2026-10-14 from its `verified-at` header; the r9 identity date is the round-9 record, not re-checked.

## Installs

none
