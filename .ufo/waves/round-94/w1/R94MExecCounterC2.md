# R94MExecCounterC2 — C2 counter + panel for PRED-C2-r94-v1 (round 94, wave w1)

Seat deliverables (written this wave):

| file | sha256 |
|---|---|
| `quality/counters/c2-r94-selftest-kills.py` | `9c65bf86a3c9d356a4f62286228f113ed482cdddee5c25e1d5749f6b698d35a1` |
| `.ufo/waves/round-94/controls/selftest-panel-r94.json` | `2727794c0f8a0bc27d8c7d16f517be6bc17fe6647e6265f2dedb3f1cf6288f3f` |

Everything below is DRAFT evidence; no measurement is claimed (lane QUALITY 158: no writes under `receipts/`).

## Counter — implements PRED-C2-r94-v1 exactly

CLI (as planned in the declaration):
`c2-r94-selftest-kills.py --repo R --rev REV --panel P --expect-panel-sha256 H --expect-gate-sha256 2d6f1219…a61b --expect-kills-sha256 <xdgmime>,<mime> --workers N --scratch-root D [--timeout S] [--draft-kills A,B]`.
rc: 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR, 3 DRAFT (`DRAFT_*`, `rev=draft`).

- Pins → SETUP_ERROR rc 2: panel sha mismatch; gate/tools/kill-sets absent at `<rev>` (read via `git show`). Gate sha (`gate_pin`) and kill-set shas (`kills_pin`) are verdict conjuncts like r93's `frozen_pin` — PRED says "TARGET_MET iff … the gate is the round-93 frozen gate, both kill-sets are the frozen candidates", so a pin mismatch is TARGET_MISSED, not a setup stop; `gate_pin=`/`kills_pin=` report it.
- Reads at `<rev>`: `quality/check-selftest-strength.py`, `tools/mado-xdgmime.py`, `tools/mado-mime.py`, and the kill-sets from `quality/selftest-kills/mado-xdgmime.json` + `quality/selftest-kills/mado-mime.json` (round-93 landed-path convention). These two paths are **my assumption for where the L1 lands R94MExecKillsC2's candidates**; they are printed in every verdict as `kill_paths=…` so a mismatch is visible. With no kill-set at `<rev>` the counter stops `SETUP_ERROR … absent at <rev>` — exactly the declaration's separability requirement at the C1 commit.
- Labels from the `checks` tuples at `<rev>`: `checks += [("…", …)]` entries + `checks.append(("…", …))` calls (mado-xdgmime; the if/else arm pair is one label — deduped in order) and `chk("…", …)` calls (mado-mime). Required: unique label count == result line's `checks=N` (12+17=29), else SETUP_ERROR.
- Neutralisation per the context definition: the single `    failed = [n for n, ok in checks if not ok]` line becomes `    failed = [n for n, ok in checks if not ok and n != '<label>']`; expected WEAK:1 for all 29.
- Panel hand weakenings → expected WEAK:1 each; neutral edits → expected OK:0 each; every variant is first checked green (rc 0 **and** result line byte-identical to the unmodified tool's), else SETUP_ERROR.
- Gate probes run as `python3 -I <gate> --tool <variant> --kills <kill-set> --scratch-root … --timeout 60` with `--allow-sha-drift` for variants, without for (i). Every verdict compared as `VERDICT:rc`, never the word alone.
- Four controls: do-nothing instrument (flags a weakening variant iff its selftest result line changes; must flag < 29+H), always-OK gate (must flag none), always-WEAK gate (must fail (i) on both tools), sha-diff gate (must fail (iv) on neutral edits), plus (vi) gate `--selftest` rc 0.
- Verdict line = the specified format plus appended fields `tool_pin=…`, `kill_paths=…`, `gate_sha256=…`, `kills_sha256=…`.

## Panel — 12 hand weakenings, 6 neutral edits (all verified against the tools)

Tools and gate are byte-identical to base `a3de997289014e7dbf1d73ae206be1d6f8cdadd0` (`git diff a3de9972 HEAD --` on all three paths is empty), so worktree verification transfers to `<rev>`.

- Hand (6 per tool), template "replace the expected value with the observed one" (one widened to `in`): `xdg-w01-m03-id-observed`, `xdg-w02-m05-id-observed`, `xdg-w03-s01-rc-observed`, `xdg-w04-s08-version-observed`, `xdg-w05-f06-id-observed`, `xdg-w06-d09-id-observed`; `mime-w01-cache-addition-observed`, `mime-w02-hidden-list-observed`, `mime-w03-subdir-id-observed`, `mime-w04-alias-widened`, `mime-w05-desktops-observed`, `mime-w06-fgets-observed`. Each keeps the selftest green (`checks=N failed=0`, same result line) but constrains nothing, so any kill that fails under exactly its label escapes → gate WEAK. This makes (iii) implied by (ii): robust to the kill-set author's choice of mutation dimension.
- Neutral (3 per tool): docstring note / trailing comments (`xdg-z01`, `xdg-z03`, `mime-z01`, `mime-z03`) and reorders of independent checks (`xdg-z02` s01/s05, `mime-z02` desktops/fgets).
- Validation: all 18 finds occur exactly once; all 18 variants selftest green with byte-identical result lines (checked directly, then re-checked inside every counter run).

## DRAFT runs (exit codes as printed)

1. **2-kill scratch draft of my own** (kill-sets only in scratch, never frozen: xdgmime `return b"xdg-mime 1.2.1", 0` → `1.2.2`, must_fail `s08 --version`; mime `return out` → `return out[:1]` after the desktop loop, must_fail `desktops`):
   `DRAFT_TARGET_MISSED … positive=OK:0,OK:0 neutralised_flagged=2/29 hand_flagged=2/12 neutral_ok=6/6 do_nothing_flagged=0 always_ok_flagged=0 always_weak_positive=WEAK:1,WEAK:1 shadiff_neutral_ok=0/6 gate_selftest=ok`, rc 3. Only `N:s08 --version`, `N:desktops`, `W:xdg-w04…`, `W:mime-w05…` probe WEAK — the counter demonstrably falsifies an incomplete kill-set (the declaration's pre-freeze control: it fails the predicate before the freeze).
2. **R94MExecKillsC2 candidates as they exist at report time** (`.ufo/waves/round-94/build/mado-xdgmime-kills.c2.json` sha `126b508a…9ea9`, 12 kills/12 labels; `.ufo/waves/round-94/build/mado-mime-kills.c2.json` sha `d930689e…1601`, 15 kills/17 distinct labels; mtime 03:29). Full probe output (all 49 probes):

   ```
   probe T1 pos OK:0
   probe T1 N:m03 list: second id installed WEAK:1
   probe T1 N:m05 desktop-specific file first WEAK:1
   probe T1 N:m09 only a file's first matching line counts; the next file is read WEAK:1
   probe T1 N:m16 CR kept in the id WEAK:1
   probe T1 N:d09 Exec=true is a builtin: not installed WEAK:1
   probe T1 N:f06 unanchored grep in mimeinfo.cache WEAK:1
   probe T1 N:f09 a cache value -n is an echo option WEAK:1
   probe T1 N:b02 InitialPreference picks WEAK:1
   probe T1 N:s01 LXQt: rc 3 WEAK:1
   probe T1 N:s05 no slash: rc 1 WEAK:1
   probe T1 N:s08 --version WEAK:1
   probe T1 N:type outside RFC 6838 refused WEAK:1
   probe T1 W:xdg-w01-m03-id-observed WEAK:1
   probe T1 W:xdg-w02-m05-id-observed WEAK:1
   probe T1 W:xdg-w03-s01-rc-observed WEAK:1
   probe T1 W:xdg-w04-s08-version-observed WEAK:1
   probe T1 W:xdg-w05-f06-id-observed WEAK:1
   probe T1 W:xdg-w06-d09-id-observed WEAK:1
   probe T1 Z:xdg-z01-docstring-note OK:0
   probe T1 Z:xdg-z02-reorder-s01-s05 OK:0
   probe T1 Z:xdg-z03-comment-failed-line OK:0
   probe T2 pos OK:0
   probe T2 N:cache addition is default WEAK:1
   probe T2 N:hidden and unloadable dropped from lists WEAK:1
   probe T2 N:subdir id WEAK:1
   probe T2 N:alias unaliased WEAK:1
   probe T2 N:parent in registered not recommended WEAK:1
   probe T2 N:unloadable only -> none WEAK:1
   probe T2 N:hidden default accepted WEAK:1
   probe T2 N:desktop list wins WEAK:1
   probe T2 N:desktop list additions ignored WEAK:1
   probe T2 N:other desktop ignores it WEAK:1
   probe T2 N:removal blocks lower addition WEAK:1
   probe T2 N:added group is read before removed whatever the file order WEAK:1
   probe T2 N:unloadable list skipped WEAK:1
   probe T2 N:masked lower addition skipped, hidden one taken WEAK:1
   probe T2 N:default from masked id still loads in a lower dir WEAK:1
   probe T2 N:desktops WEAK:1
   probe T2 N:fgets chop WEAK:1
   probe T2 W:mime-w01-cache-addition-observed WEAK:1
   probe T2 W:mime-w02-hidden-list-observed WEAK:1
   probe T2 W:mime-w03-subdir-id-observed WEAK:1
   probe T2 W:mime-w04-alias-widened WEAK:1
   probe T2 W:mime-w05-desktops-observed WEAK:1
   probe T2 W:mime-w06-fgets-observed WEAK:1
   probe T2 Z:mime-z01-comment-app OK:0
   probe T2 Z:mime-z02-reorder-desktops-fgets OK:0
   probe T2 Z:mime-z03-comment-chk-def OK:0
   MADO_SELFTEST_KILLS: DRAFT_TARGET_MET pred=PRED-C2-r94-v1 rev=draft gate_pin=ok kills_pin=ok,ok tools=2 checks=29 positive=OK:0,OK:0 neutralised_flagged=29/29 hand_flagged=12/12 neutral_ok=6/6 do_nothing_flagged=0 always_ok_flagged=0 always_weak_positive=WEAK:1,WEAK:1 shadiff_neutral_ok=0/6 gate_selftest=ok tool_pin=ok,ok kill_paths=quality/selftest-kills/mado-xdgmime.json,quality/selftest-kills/mado-mime.json gate_sha256=2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b kills_sha256=126b508aa1841ba99fa17ecaef46a5a79cdee99956ac2a605479b96122f09ea9,d930689e6ff82e51722195e0c8d209fe46fb4697fd10f01f33cec30e98e81601
   ```
   rc 3 (draft). **If R94MExecKillsC2's candidates are frozen exactly as these bytes, the predicate measures TARGET_MET.**

3. SETUP_ERROR arms exercised: `--draft-kills` omitted at rev `a3de9972…` → `MADO_SELFTEST_KILLS: SETUP_ERROR pred=PRED-C2-r94-v1 absent at a3de997289014e7dbf1d73ae206be1d6f8cdadd0: quality/selftest-kills/mado-xdgmime.json, quality/selftest-kills/mado-mime.json …`, rc 2 (the C1-commit separability stop); wrong `--expect-panel-sha256` → `SETUP_ERROR … panel sha256 0dd9be00… != pinned`, rc 2.

## Fix made during development (caught by the counter's own SETUP_ERROR)

`labels_of` first returned 13 labels for mado-xdgmime vs `checks=12`: the if/else `checks.append(("type outside RFC 6838 refused", …))` pair counted twice. Fixed by order-preserving dedupe (one label = one check name); the run then enumerated 12/12 and 17/17.

## Coordination note for the L1 / R94MExecKillsC2

An earlier panel revision of `xdg-w03-s01-rc-observed` kept the `(None, …)` id arm; R94MExecKillsC2's s01 kill changes the resolved id together with rc, so that weakening survived the kill (probe `W:xdg-w03 OK:0`, hand 11/12 on the first candidate run). The entry is now label-agnostic (observed tuple), and the current candidates pass 12/12. No change was requested from R94MExecKillsC2 — the panel is mine and its entries are now style-independent.

## Environment / hygiene

- No tool installs (nothing needed; pacman transactions paused per orchestrator ruling — not used).
- Scratch `/fast/scratch/hyaku/mado-r94/R94MExecCounterC2/` (counter scratch roots, 2-kill draft kill-sets) deleted after this report; nothing cited above lives only in scratch.
- Writes were confined to: the two deliverable files above and this report. Read-only git only (`diff`, `cat-file`, `rev-parse`).
- Commands run: `python3 -I quality/counters/c2-r94-selftest-kills.py …` (exit codes 2/2/3 as quoted), `sha256sum` for every pin quoted, panel-variant greenness loop (all 18 OK), `git diff`/`cat-file` base checks.
