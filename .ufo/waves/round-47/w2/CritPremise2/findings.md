# CritPremise2 — findings (round 47 w2, falsify, leaf seat)

Attacks the "Premise corrections from w1" section of
`.ufo/waves/round-47/registration.md:14-26`. Lane base
`60edb66e2f1cb90acc6e9442fc93ded0ca42d750`. All locators computed
(`git grep -n` / `grep -n`) and verified; every quote ≤25 words. Evidence
receipt: `evidence-receipt.txt` in this seat dir.

## F1: the "selection half" of the round-17 [UNK] was already recorded at base

Registration premise (`.ufo/waves/round-47/registration.md:16-19`) says C2
"answers only the selection half of the round-17 [UNK] at `:144-145`" by a
cold-cache capture, implying the selection half was open. Base bytes show the
selection fact was already on record:

- `corpus/knowledge/terminal-route-r17.md:123-127` (base rev), `[OBS, bytes]`:
  "The resolver's cache `~/.cache/xdg-terminal-exec` (190 B, sha256
  `dd26ec4e...`, mtime 2026-10-20 09:57:18 -0300) records `alacritty`,
  `/home/vgpnk/.local/share/applications/./Alacritty.desktop` and the four
  `X-TerminalArg*` values: the last fresh selection was the user-local entry."
- The `[UNK]` at `:144-145` is explicitly launch-scoped: "whether the resolver
  actually picks that entry over the system one **at launch**; no launcher ran."

So the premise's F1/F2 correction is half-right: print modes never observe a
launch (true), and a cold-cache capture is a stronger evidence class than the
ambient cache bytes (true). But the framing that C2 "answers the selection
half" overstates: the value was already answered at base as observed bytes. The
actual new content is (a) a controlled, env-pinned capture of the resolver's
print path (tag v0.14.3 digest, XDG_* pins), and (b) tying the outcome to
script lines/fixtures. The selection half was *recorded*, not *unknown*.

**Where this bites (drafted data):**

- `w1/ScrEntry/entry.md:7` (ground): "the resolver's *choice* was unsourced at
  base (round-17 declared it `[UNK]` at terminal-route-r17.md:144-145 … answered
  by the live receipt …)". False: round-17 did not declare the choice [UNK];
  it recorded the choice at `:123-127` as `[OBS, bytes]` and declared only the
  *launch-time pick* [UNK] at `:144-145`.
- `w1/ScrEntry/entry.md:68`: "That is the round-17 `[UNK]` at
  terminal-route-r17.md:144-145 - whose two halves … the live row above answers".
  The L1 freeze requires the launch half to stay `[UNK]` and the entry to say so
  (`registration.md:18-19`). The draft claims the live row answers the [UNK]
  (both halves). The receipt itself is print-only (`w1/ExecLive/receipts/live-host.txt`
  section [8] says "with the launch replaced by print-only invocation of the
  same code path") — the entry text overclaims what the receipt can support.

Fix (entry data): state the selection half is answered by the committed
cold-cache print capture, the value was already observed at base
(`terminal-route-r17.md:123-127`), and the launch half remains `[UNK]`
(no launcher ran) — matching `registration.md:18-19`.

## F2: the four clause-i ground terms are real script units, not invented spelling

Terms `read_config_paths`, `check_entry_key`, `find_entry_paths`,
`print-delimiter` (counter `quality/counters/c2-r47-terminal-entry.py:117`):

- `read_config_paths()` — v0.14.3 script line 351 (call 1198).
- `check_entry_key()` — line 802 (call 997).
- `find_entry_paths()` — line 754 (call 1200).
- `--print-delimiter=` — line 127 (parse 1305); `XTE__PRINT_DELIMITER`
  variable lines 1222/1307.

So they name actual executable code in the pinned resolver; they are not bare
new spelling. However clause i only censuses the strings (absent under corpus/
at base, ≥2 present at REV). It cannot measure whether the entry *documents*
the semantics. The "new ground" claim is carried by the entry's exposition
(steps 1–7, each with script locators), not by clause i. The draft uses all
four terms once each, substantively (step 2 `read_config_paths`; step 3
`find_entry_paths`; step 4 `check_entry_key`; step 7 `print-delimiter`), so
clause i would be satisfied — but a token mention would pass equally.

Also note: the same script bytes were already committed at base at
`.ufo/waves/round-18/fetch/FetchBackfillR17/s057-xtd-script`
(sha256 `89f2be9a…` = identical to the round-47 pin
`.ufo/waves/round-47/fetch/xdg-terminal-exec`). The functions' *code* was
in-lane at base; what is new is documenting them under corpus/ and proving
behavior via the C1 fixtures/capture. Clause i is a corpus-scoped term census,
not a lane-wide novelty proof (as its declared residual admits).

## F3: some "new ground" items are already held elsewhere at base

Base greps (`60edb66e…`) show these executed-semantics are already documented in
the lane (outside corpus/):

- `check_entry_key()` key reads, `/execarg_default` consumption,
  `get_default_execarg` (1113–1130), built-in `-e` fallback (1128), applicability
  checks 816–821 enforced at 1088–1090, `X-TerminalArgExec` read at 885 →
  `.ufo/waves/round-17/w2/reports/ReopenS057.md:30-36`.
- Cache-on-by-default (`:1172`) → `.ufo/waves/round-17/w2/reports/AttackP4Claims.md:30`.
- `--dir=` parse (`:1252`), `cd "$XTE__DIRVAL"` before exec (`:1494-1497`) →
  `.ufo/waves/round-17/w1/reports/HostTerminalFiles.md:66` + `ReopenS057.md:34-36`.
- ShowIn/NotShowIn honoured in fallback only →
  `.ufo/waves/round-17/w1/reports/SrcXdgTerminalExec.md:112-113`.
- Duplicate-ID "last found wins" (`:779-781`) → `terminal-route-r17.md:47-50` (base).
- Lookup order/format/applicability/execarg defaults → `terminal-route-r17.md:24-59`
  (explicitly conceded by F3).

Genuinely new at base (no corpus/ hits, no report hits): print composition order
and delimiters, exit map, tokenizer/de_tokenize_exec and field stripping detail,
`command -v` over aliases/functions/builtins (as a resolver-semantics claim),
find-based ID character-class filter, carried-over-key/reset-globals details.
That core matches F3's narrowing; the list in registration is accurate once the
"held at base" items above are subtracted.

One premise-vs-data gap: F3 says the new-ground items are "each tied to the
script lines and to the C1 fixtures that exercise it". The entry ties every step
to script lines but never mentions the C1 fixtures (`grep -c fixture` on
`w1/ScrEntry/entry.md` = 0). The counter does not require it (clause e requires
script locators; clause i term census), so it is not a counter hole — but the
premise's characterization is not realized in the draft.

## F4: base ground-absent receipt is correct but narrower than "absent from lane"

`receipts/c2-ground-base.txt` (`exit=1`) matches re-run `git grep -F <term>
60edb66e… -- corpus` for all four terms. But at base the terms *do* occur
outside corpus/: `s057-xtd-script` (read_config_paths:351/357/1198;
check_entry_key:802/997; find_entry_paths:754/1200; print-delimiter:127/1305),
`s056-xtd-readme:230`, and `ReopenS057.md:33` (check_entry_key). So "ground
absent at base" means "absent under corpus/", not "absent from the lane".

## Reproducible commands

- Selection-half evidence:
  `git -C <lane> show 60edb66e…:corpus/knowledge/terminal-route-r17.md | sed -n '123,127p;144,145p'`
- Term census at base:
  `git -C <lane> grep -n -F read_config_paths 60edb66e… -- corpus` (rc=1, same
  for the other three terms)
- Term existence in the pinned script (works at base and round-47):
  `git -C <lane> grep -n -F check_entry_key 60edb66e… -- .ufo/waves/round-18/fetch/FetchBackfillR17/s057-xtd-script`
- Pin identity:
  `sha256sum <lane>/.ufo/waves/round-18/fetch/FetchBackfillR17/s057-xtd-script <lane>/.ufo/waves/round-47/fetch/xdg-terminal-exec`
- Draft overclaim lines:
  `grep -n 'unsourced\|two halves' <lane>/.ufo/waves/round-47/w1/ScrEntry/entry.md`
