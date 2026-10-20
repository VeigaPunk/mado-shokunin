# PtrCloseoutR11 — R18-V3 forward pointer appended to closeout-r11.md; prefix byte-identical

Scope: R18-V3 forward pointer for one note, `corpus/knowledge/closeout-r11.md`, sole writer this wave. Append-only.

## Findings

- Walker pins in the note: exactly one line contains `2.17.0`, line 43 (`| walker | 2.17.0; sockets stat'd 0 B, never connected; no reload path — restart is the apply path | consumer-side probe |`). Grep: `grep -n '2\.17\.0'`.
- Walker mentions overall (grep `(?i)walker`): lines 42–46 table, 152, 154, 174, 187, 201 (walker-deep notes and the exempted `walker ×3` live rows), 264 (2026-10-14 PID sample), 299–304 (the appended block). Only line 43 is a walker version pin.
- Appended block at the end of the note, `## Freshness pointer (round 19, 2026-10-20)`, lines 297–304 (8 content lines, under the 20-line cap):
  - line 299: first bullet, contains `2.17.2` and `S090` on one line (host move, `/var/log/pacman.log:2929`); routes to `corpus/knowledge/walker-route-r18.md`.
  - line 300: version-bound — the `2.17.0` version print on line 43 is dated 2026-10-14 and not re-asserted.
  - line 301: socket `stat` 0 B is a dated 2026-10-14 host-state point sample, session-dependent, not re-measured.
  - line 302: "no reload path" is a consumer-side reading against 2.17.0; walker-route-r18.md greps the v2.17.2 tag tree for `reload_config`/`set_config` in `src/` (source reading only); live 2.17.2 reload behaviour is `[UNK]`.
  - line 303: the other walker mentions (152, 154, 187, 201, 174, 264) are not version pins and are not affected by the move.
  - line 304: 2.17.2 binary behaviour stays `[UNK]`; not re-measured (host pause).
- No live value was re-asserted. No new fact beyond the note, S090 and walker-route-r18.md.
- S096 is not cited: `grep -n 'S096' corpus/SOURCES.md` returns no row (reserved id only). The block cites S090, which exists.

## Edit receipts

- Before: `sha256sum` `670b5a396ecb8789430709a8e490c93a5672399401e6a8209f26e93645d818a1`, 19,250 B, 294 newline-terminated lines (file ended without a trailing newline).
- Edit 1 (`PUT >$:`, tag `4FAF`): appended the block. Result tag `2635`. Prefix check: `head -c 19250 closeout-r11.md | sha256sum` = `670b5a39…818a1` — equal to the before-sha. File then 20,382 B, sha `64d8a95d77b223e6c1b83f1d6b6ea1308808b8d070ba15661d5f52fd782a9377`.
- Edit 2 (`PUT 303.=303`, tag `2635` → `5C73`): corrected my own appended bullet 303. The first draft said "no other line of this note names walker", which the grep above showed was false. Only the appended line changed; the pre-block bytes did not.
- After: `sha256sum` `dab87af80f32055b97ef3674d770cc5489bdf0b89da1e76bdd7b78554ed917ba`, 20,516 B. Prefix check `head -c 19250 | sha256sum` = `670b5a39…818a1` — still equal to the before-sha, so every pre-existing byte is unchanged.
- Caveat: no copy of the pre-edit file was saved, so the prefix check compares against the sha recorded before edit 1. That is the check the brief specifies and it passes.
- `grep -c '2\.17\.2'` = 4 (lines 299, 302, 303, 304). Line 299 carries both `2.17.2` and `S090`.

## Limits

- Not checked: `/var/log/pacman.log:2929` itself (not opened this round; the citation is from S090 as the brief directs). The host pause forbade pacman/hyprctl/live work, and none was run.
- Not checked: walker-route-r18.md's grep claims beyond reading the line that states them; the 2.17.2 tag tree was not re-fetched.
- Not checked: other owned files (only the one note was in scope).
- `corpus/knowledge/closeout-r11.md` lines 1–294 were not edited and their content was not re-audited.

## Installs

none
