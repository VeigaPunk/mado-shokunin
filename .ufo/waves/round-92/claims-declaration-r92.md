# mado round 92 — claims declaration (frozen at the freeze commit that carries this file)

L1 `MadoR92`, hyaku run 15, attempt 1. Base revision `d992ef7494b054591ee9104df1da49264678df5d` (round-91 closure tip,
`master`). Lowest-axis duty: every owned axis stands at 10 (SCORECARD rounds 88–91), so the duty is a tie; the
stagnation nudge is not claimed (capabilities entered at rounds 88–91). Sourced claim: C1 (rows S508–S510 opened this
round by the L1, `.ufo/waves/round-92/receipts/sources-open-r92.txt`).

The w1 wave (13 seats) attacked the drafts before this freeze; every change it caused is listed in
`corpus/lessons/round-92.md` "Wave findings routed". The draft that w1 attacked is not the frozen bytes.

## C1 — coverage (capability acquisition): what `xdg-open` launches on Hyprland

**Surface moved.** On a session whose `XDG_CURRENT_DESKTOP` xdg-utils does not recognise (Hyprland), `xdg-open` maps
the desktop to `generic` (xdg-open.in:595-596) and asks `xdg-mime query default TYPE` (`open_generic_xdg_mime`,
:392-410), and xdg-mime answers with its own shell resolver `defapp_generic` — not GLib's. Before: no lane tool or
knowledge entry models it (`git grep -l defapp_generic d992ef74 -- tools corpus` empty; `tools/mado-xdgmime.py`
absent at `d992ef74`), and the round-91 entry wrongly says `xdg-open` reduces to GLib. After: `tools/mado-xdgmime.py`,
read-only, replays xdg-utils 1.2.1 `query default` over files only: `defapp_generic`, `check_mimeapps_list`,
`desktop_file_to_binary`, the `defaults.list`/`mimeinfo.cache` grep, `defapp_fallback`, the session dispatch.

**Scope (declared in the tool's docstring; frozen cases respect it, `controls/merge-c1-cases-r92.py`).** Asked types
are RFC 6838 restricted-name bytes (`[A-Za-z0-9!#$&^_.+-]` and `/`); the tool refuses (rc 2) other types, `--help`/
`--manual` as the type, PATH unset, XDG_UTILS_REALPATH_BACKEND/XDG_UTILS_DEBUG_LEVEL set, files holding NUL bytes, an
LXQt `qtxdg-mat` or KDE trader on PATH; it assumes PATH reaches GNU coreutils/grep/gawk and that no GNOME session
manager owns D-Bus. The w1 seats found the regex-engine behaviour of grep/gawk on non-RFC types (stacked quantifiers,
intervals, collating classes, unknown gawk escapes) — 36 seat cases fall under the type rule and are not frozen.

**Premise, measured on the frozen set before the freeze.** The round-91 GLib resolver answers what xdg-mime answers on
139 of 270 frozen cases (control `glib_resolver_correct`), and on the operator's host xdg-mime and gio give
different defaults for 378 of 1133 types (`w1/R92MExecHost-host-run.txt`, `glib_disagree=378`).

**Predicate `PRED-C1-r92-v1`** (same sentence as the counter `quality/counters/c1-r92-xdgmime-default.py` docstring;
the receipt line starts `MADO_XDGMIME_DEFAULT:` and carries `pred=PRED-C1-r92-v1`): TARGET_MET iff
`<rev>:tools/mado-xdgmime.py`, run on every frozen case (fixture tree + whole environment + working directory = the
fixture root + the MIME types asked) inside a sandbox that hides /usr/bin/xdg-mime, /usr/bin/xdg-open,
/usr/bin/xdg-settings, every host shell binary and the lane repository, prints for every asked type the same line and
exit status as the installed xdg-mime labelled (correct == cases); does the same on every fresh case the frozen fuzz
generator makes from seed = the first 8 hex digits of the measured tool's sha256, labelled by xdg-mime at measurement
time (fresh_correct == fresh, fresh = 120); every frozen mutant returns a well-formed wrong answer on at least one
frozen case (killed == mutants; a mutant that only crashes is crashed-not-killed, QUALITY 148); each control scores
fewer than the case count (do-nothing, naive user-mimeapps reader with no install check, the base revision's GLib
resolver `tools/mado-mime.py`, the base revision's `tools/mado-xdgmime.py` — absent = 0); xdg-mime, bash, grep, gawk,
realpath and basename are the pinned binaries and still give every stored label (oracle_agree == cases); and the
measured tool's bytes pass the bytes clause (≤ 65536 bytes, no ELF/PE/Mach-O magic, no base64/hex run > 8192 bytes).

The sandbox hides the host's shells and xdg-utils, not a copy a tool carries: R92MCritic's bundled-interpreter forgery
(1.66 MB, bash + xdg-mime's text) scored every frozen and fresh case. The bytes clause refuses that class; the frozen
mutant anchors (each must occur once in the measured bytes and flip a modelled rule) are the semantic defence.

**Kill rule.** Any conjunct false at the measured C1 commit → `TARGET_MISSED`, reported as such; no case, mutant,
control, pin or clause changes after this freeze.

**Count.** MIME types a lane tool answers `xdg-open`'s (xdg-mime's) default for: 0 at `d992ef74` (tool absent) →
every RFC 6838 type, gated by the predicate above.

## C2 — operability: the seat-report gate closes the round-91 residual defects F1–F5

**Surface moved.** `quality/check-seat-reports.py` (round 91) had five defects reproduced by R91MResidC2 and routed by
the round-91 spot-check (defect 2): F1 a dispatch stored as a symlink skipped in `--rev` (verdict OK with a wave
unchecked) — w1 widened it to a directory or gitlink at a dispatch path in either mode (R92MReviewC2 findings 1–2);
F2 a seat name or path printed raw (spaces/newlines split records, non-UTF-8 bytes crash the round-91 counter);
F3 a repeated `--round` double-counted; F4 a FIFO at a dispatch path hangs `--worktree`; F5 a report reached through a
parent-directory symlink leaving the repository counted as present in `--worktree`. F6 (`counts.total` vs tasks) is a
new rule, not a defect of these bytes: not claimed.

**Predicate `PRED-C2-r92-v1`** (counter `quality/counters/c2-r92-gate-defects.py`; receipt line `MADO_GATE_DEFECTS:`):
TARGET_MET iff `<rev>:quality/check-seat-reports.py`, run inside a sandbox that hides the lane repository, meets every
fixture of the frozen battery (rc, SR-id multiset, named substrings, summary fields, token/line counts, ASCII-only
stdout, finished within 20 s) and every fresh fixture the counter generates over the F1–F5 vocabulary from seed = the
first 8 hex digits of the measured check's sha256 (fresh = 60, expectations from the generator's own choices); its
`--selftest` exits 0 with `failed=0`; every frozen mutant meets fewer battery or fresh fixtures or changes the selftest
line (killed == mutants); each control (base revision's check, always-OK, always-refuse-as-symlink) meets fewer battery
fixtures than the battery holds; and the round-91 frozen counter, read from `<rev>` and pinned by sha256
(`c74f5baa…`), prints TARGET_MET for the same revision (a SETUP_ERROR of that leg is a setup error, not a miss).

**Count.** Battery fixtures met by the lane's gate: base `d992ef74` 19/45 → 45/45 (the C2 controls receipt).

## Do-nothing and forgery controls (executed before this freeze; `receipts/c1-controls-prefreeze-r92.txt`,
`receipts/c2-controls-prefreeze-r92.txt`)

- C1: do-nothing, naive reader, GLib resolver, absent base tool (inside the predicate); outside it: a shell-out
  forgery (execs `/usr/bin/xdg-mime`, falls back to host shells), a label-table forgery (frozen answers keyed by the
  fixture bytes; `None` otherwise — the fresh leg defeats it), a bundled-interpreter forgery (the bytes clause defeats
  it).
- C2: base check, always-OK, always-refuse (inside the predicate).

## Separability

C1 touches `tools/mado-xdgmime.py`, a knowledge entry and registry rows; C2 touches `quality/check-seat-reports.py`.
Each counter reads its own file at the measured revision (C2 also reads the round-91 counter from that revision,
pinned, and the round-91 pinned set/mutants); neither reads the other's file. Each counter is run at the other's commit.

## Frozen pins and argv (REV = the measured commit; run from the lane root)

- C1 candidate `.ufo/waves/round-92/build/mado-xdgmime.c1.py` sha256 `4e7fff9efbd32d101d1383099566008fc49ba626be5bcc53a20766d71bc7fd88` (lands byte-identical as `tools/mado-xdgmime.py`);
  cases `.ufo/waves/round-92/controls/xdgmime-cases-r92.json` (270) `3cb0cf4556171845af21b75ee50f62de64af91e9eefd948d27957010d3031594`; mutants `.ufo/waves/round-92/controls/xdgmime-mutants-r92.json` (81)
  `f0d934f2dca4c6a9a8d442b20569cb9d8b226eff792c6eed1c462208185ab524`; oracle `e51603991450305d6c6168624d7f635a67a3906e512851f3542896b8ef32f87b`; fuzz `891704bf7cb42e44b89066210eec5227174597e4f76c6309d1114ddcbd6c5c01`;
  counter `quality/counters/c1-r92-xdgmime-default.py` `634771678695ad19bbe90b0cccc1279019b287803188922d530cd36ad6a81648`.

      python3 -I quality/counters/c1-r92-xdgmime-default.py --repo . --rev REV --base-rev d992ef7494b054591ee9104df1da49264678df5d \
        --cases .ufo/waves/round-92/controls/xdgmime-cases-r92.json --mutants .ufo/waves/round-92/controls/xdgmime-mutants-r92.json \
        --oracle .ufo/waves/round-92/controls/xdgmime-oracle-r92.py --fuzz-gen .ufo/waves/round-92/controls/fuzz-gen-r92.py \
        --expect-cases-sha256 3cb0cf4556171845af21b75ee50f62de64af91e9eefd948d27957010d3031594 \
        --expect-mutants-sha256 f0d934f2dca4c6a9a8d442b20569cb9d8b226eff792c6eed1c462208185ab524 \
        --expect-oracle-sha256 e51603991450305d6c6168624d7f635a67a3906e512851f3542896b8ef32f87b \
        --expect-fuzz-sha256 891704bf7cb42e44b89066210eec5227174597e4f76c6309d1114ddcbd6c5c01 \
        --expect-bin-sha256 a587107ff995a5f907ab1b731316a169348c6b0383caf8fd151ff21f89615f3f,c14c8f498f3be96f076ceb07d65dba584a86dca3c86b5dce65ed0f6cae73358d,19280b0e0714dadf0c100cdbc7f4823d254dd8facba64deeff5ec50d39fecf84,3ac64468ec05bde58b4294771f0afd9c626d4e95cc7a97efd7e7f7a55230febd,5f6c63c5105c0ec3f0e50a31f225be8dc95fbd7b8af0e7f0dd14867f345cc7f7,a21add5faf3a48efe8f4ff8e193216f4273d0842770a913171df5d4522648e06 \
        --fresh 120 --scratch-root DIR

- C2 candidate `.ufo/waves/round-92/build/check-seat-reports.c2.py` sha256 `176fc066b49334921e4fd746de55db8106709c29dfe225430224c9d46ed1663a` (lands byte-identical as
  `quality/check-seat-reports.py`); battery `.ufo/waves/round-92/controls/gate-defects-battery-r92.json` (45) `a0cfaeb36c5423678696629569019dece0d2138dc5e980df0ba7a9ad7ef2fdd6`;
  mutants `.ufo/waves/round-92/controls/gate-defects-mutants-r92.json` (37) `fe931e76f778e318771486458336d53dbf8933dd5444fa0beba07d53196f1e26`; counter
  `quality/counters/c2-r92-gate-defects.py` `0aa4d1f18c3f309a8ef5a7575f1a4bde84681d9f7843dea03fdca723de30945c`.

      python3 -I quality/counters/c2-r92-gate-defects.py --repo . --rev REV --base-rev d992ef7494b054591ee9104df1da49264678df5d \
        --battery .ufo/waves/round-92/controls/gate-defects-battery-r92.json --mutants .ufo/waves/round-92/controls/gate-defects-mutants-r92.json \
        --expect-battery-sha256 a0cfaeb36c5423678696629569019dece0d2138dc5e980df0ba7a9ad7ef2fdd6 \
        --expect-mutants-sha256 fe931e76f778e318771486458336d53dbf8933dd5444fa0beba07d53196f1e26 \
        --r91-argv .ufo/waves/round-92/controls/r91-c2-argv-r92.json --expect-r91-argv-sha256 d21b1979b8b42203c8d9c8d033ec71af8027ff79911adc348cddb9685df4b604 \
        --expect-r91-counter-sha256 c74f5baae915a4669ece5033a35ba16f5db0131a2db9a6e83a702de9e932d486 \
        --fresh 60 --scratch-root DIR
