# CritPremise2 — round 47 w2 report (leaf seat, falsify)

Target: the "Premise corrections from w1" section of
`.ufo/waves/round-47/registration.md:14-26` at lane base
`60edb66e2f1cb90acc6e9442fc93ded0ca42d750`. Findings detail:
`.ufo/waves/round-47/w2/CritPremise2/findings.md`; evidence receipt:
`.ufo/waves/round-47/w2/CritPremise2/evidence-receipt.txt`.

## Verdict

The registered premise corrections are mostly sound, but one premise is
over-read and the **drafted entry overclaims against the L1 freeze**. A hole
exists in `w1/ScrEntry/entry.md` (drawn data) that must be fixed before the data
commit.

## Findings

1. **Selection half was already recorded at base (premise overstates "answers").**
   `corpus/knowledge/terminal-route-r17.md:123-127` (base) records `[OBS, bytes]`:
   the resolver cache holds `alacritty`, user-local `Alacritty.desktop` path and
   the four `X-TerminalArg*` values — "the last fresh selection was the user-local
   entry". The `[UNK]` at `:144-145` is launch-scoped ("at launch; no launcher
   ran"). So C2's cold-cache capture re-derives a value already known at base;
   its genuine addition is the controlled, digest-pinned capture + script-line
   semantics, not first knowledge.

2. **Draft entry overclaims and contradicts the L1 freeze.**
   - `w1/ScrEntry/entry.md:7` says the resolver's choice "was unsourced at base
     (round-17 declared it `[UNK]` at terminal-route-r17.md:144-145 … answered by
     the live receipt …)" — false: round-17 recorded the choice at `:123-127`;
     the [UNK] is the launch-time pick.
   - `w1/ScrEntry/entry.md:68` says the live row answers the `:144-145` [UNK]
     "whose two halves" — but `registration.md:18-19` requires the launch half to
     stay `[UNK]` and the entry to say so. The receipt itself is print-only
     (`w1/ExecLive/receipts/live-host.txt` §[8]: "with the launch replaced by
     print-only invocation of the same code path").
   Fix: state the selection half is answered by the committed capture, the value
   was already observed at base, and the launch half remains `[UNK]`.

3. **Clause-i ground terms are real script units.** `read_config_paths` (script
   line 351), `check_entry_key` (802), `find_entry_paths` (754), `--print-delimiter`
   (127/1305) all exist in v0.14.3. Not invented spelling; but clause i only
   censuses strings (absent under corpus/ at base — verified rc=1 for all four,
   matching `receipts/c2-ground-base.txt`; ≥2 at REV). The new-ground work is in
   the entry's exposition, not in the census. The draft uses each term once,
   substantively.

4. **Some "new ground" items are already held elsewhere at base (outside corpus/):**
   `ReopenS057.md:30-36` (check_entry_key, execarg defaults, `-e` fallback,
   applicability), `AttackP4Claims.md:30` (cache-on), `HostTerminalFiles.md:66`
   (`--dir`/`cd`), `SrcXdgTerminalExec.md:112-113` (ShowIn), `terminal-route-r17.md:47-50`
   (duplicate last-wins), `:24-59` (order/format). Genuinely new: print
   composition/delimiters, exit map, tokenizer/field stripping, `command -v`
   over aliases/functions/builtins, find-based ID sanitization, carried-over keys.

5. **Premise-vs-data gap:** F3 promises new-ground items are "tied to the script
   lines and to the C1 fixtures"; the draft entry cites script lines but mentions
   no C1 fixtures (`grep -c fixture` = 0). The counter does not check this, so it
   is a premise/draft mismatch, not a counter hole.

6. **Context:** host cache bytes changed since round 17 (dd26ec4e… → f497ed057…,
   consistent with the w1 rewrite incident) but still record the same user-local
   selection. Base term presence outside corpus/ (`s057-xtd-script`,
   `ReopenS057.md:33`) shows "ground absent at base" means absent under corpus/,
   not absent from the lane.

## Reproducible commands

```
git -C mado-shokunin show 60edb66e…:corpus/knowledge/terminal-route-r17.md | sed -n '123,127p;144,145p'
git -C mado-shokunin grep -n -F read_config_paths 60edb66e… -- corpus        # rc=1; same for the other three terms
sha256sum mado-shokunin/.ufo/waves/round-18/fetch/FetchBackfillR17/s057-xtd-script \
          mado-shokunin/.ufo/waves/round-47/fetch/xdg-terminal-exec          # identical 89f2be9a…
grep -n 'unsourced\|two halves' mado-shokunin/.ufo/waves/round-47/w1/ScrEntry/entry.md
```

## Cleanup / handoff

- Seat dir contains `findings.md` + `evidence-receipt.txt` (quotes ≤25 words,
  locators computed). Scratch `/fast/scratch/hyaku/mado-r47/CritPremise2` (if
  used) deleted on exit.
- Main agent should (a) fix entry.md lines 7 and 68 per finding 2 before the
  data commit, (b) optionally add a C1-fixture tie or soften the F3 wording,
  (c) note in the entry that the selection value was already observed at base.
- No tools installed; no host mutation; no terminal launched; no repository
  mutation beyond this seat's report/findings files.
