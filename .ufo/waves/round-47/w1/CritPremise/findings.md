# CritPremise — round 47 w1 findings (premise attack on C1/C2)

Seat: CritPremise (roster id CritPremise-3) · wave w1 BUILD (policy v1) · 2026-10-26.
Targets: C1 `tools/mado-terminal.py` (operability, claims.md:10-13) and C2
`corpus/knowledge/xdg-terminal-selection-r47.md` (coverage, claims.md:14-17).
Base verified read-only: `60edb66e2f1cb90acc6e9442fc93ded0ca42d750` via `jj -R <lane> log/file show`
(no mutation). Quotes ≤25 words, located by grep -n and verified (see appendix).

## Answers to the four review questions

1. **Is C1 a capability the lane lacks at base?** Yes. Base `tools/` has 14 files and none
   resolves xdg-terminal-exec selection (F5). The capability-acquisition premise holds.
2. **Is C2 coverage (new surface) or re-scoring held ground?** Mostly re-scoring; a thin new
   sliver. The "executed selection chain" surface the claim lists is already documented in
   `terminal-route-r17.md:24-59`; only print-mode semantics, action options, ShowIn/NotShowIn
   and exit-code detail are new (F3). The closure claim is mis-scoped (F1/F2/F4).
3. **Which exact selection rules are new?** Enumerated in F3: print-mode output semantics
   (`--print-id/--print-path/--print-cmd[=seq]/--print-delimiter`, action suffix, `/./`
   removal), `--hold/--app-id/--title` action composition with `X-TerminalArgAppId/Title`,
   ShowIn/NotShowIn validation, exit-status map/error paths, and (if opened) upstream
   test-suite artifacts. Everything else in the claim restates r17.
4. **Is the round-17 [UNK] really open at base?** Yes, verbatim (`terminal-route-r17.md:144-145`
   at the base rev), but it is already partially narrowed by the cache record
   (`r17:123-127`) and by round-23 process observations; the proposed live run cannot close it
   as worded (F1/F2/F4).
5. **Is 'answers the [UNK] with a live run' do-nothing-reachable?** The *selection* half yes:
   a receipt alone (the cache bytes at `r17:123-127` / `HostTerminalFiles.md:33`) reaches the
   same id/path/cmd conclusion without executing anything. The *launch* half no — but neither
   does the proposed print-mode run.

## F1 — C2 cannot close the round-17 [UNK] as worded: print modes never observe launch

Claim (claims.md:16-17): the round-17 [UNK] `terminal-route-r17.md:144-145` ("whether the
resolver actually picks that entry over the system one at launch") is "answered by a live
read-only receipt".

Evidence:
- `terminal-route-r17.md:144-145` (base rev): "[UNK] whether the resolver actually picks that
  entry over the system one at launch; no launcher ran."
- `terminal-route-r17.md:128-130`: "[UNK] Whether a terminal process actually started from that
  selection (test/print modes also write the cache) and who invoked it; no launcher ran in this
  round."
- Round-17 w2 `AttackP4Claims.md:61-65`: "What the cache does NOT show: That the process
  started. Test mode and `--print-cmd` also reach `save_cache`, at `:1457` before `:1460`."
- The proposed observation (w1-spec.json ExecLive item) runs `xdg-terminal-exec --print-id
  --print-path --print-cmd` variants; print branches (script 1328-1473) exit before any exec of
  the terminal binary. The L1 host facts concede the same: "the resolver ran no terminal; print
  modes write only the cache".

Verdict: fixable defect — the closure is overstated. **Fix:** re-word to "re-observes, live
and cold, the *selection* half of the round-17 [UNK] (which entry the resolver selects), not
the launch half"; the "at launch" clause stays `[UNK]` (uwsm-app environment and hotkey launch
remain unobserved; cf. RevengerUwsm).

## F2 — The selection fact is already recorded at base; a do-nothing control reaches it

Evidence:
- `terminal-route-r17.md:123-127` [OBS, bytes]: the resolver's cache `~/.cache/xdg-terminal-exec`
  (190 B, sha256 `dd26ec4e…`, mtime 2026-10-20 09:57:18) "records `alacritty`,
  `/home/vgpnk/.local/share/applications/./Alacritty.desktop` and the four `X-TerminalArg*`
  values: the last fresh selection was the user-local entry."
- Round-17 `HostTerminalFiles.md:32-33`: cache bytes: l.2 `alacritty`, l.3
  `…/.local/share/applications/./Alacritty.desktop`, l.4 `Alacritty.desktop`, l.6-9 `-e`,
  `--class=`, `--title=`, `--working-directory=`.
- The L1 host facts print exactly this triple (id=`Alacritty.desktop`, the override path,
  cmd=`alacritty`) modulo the `/./` removal `--print-path` performs (script 1340-1341).
- Control: reading the existing cache file (a file-byte receipt, already produced in round 17)
  yields the same id/path/cmd conclusion without executing anything. Nothing in the live run
  adds a fact beyond freshness; the host selection state is unchanged per the L1 facts.

Verdict: do-nothing-reachable conclusion; the live run's novelty is limited to a cold,
dated re-derivation. **Fix:** C2 must state "confirms (cold, dated) the selection first
recorded in `terminal-route-r17.md:123-127`"; it must not claim first observation or closure.

## F3 — Most of the described C2 surface is held ground; enumerate what is actually new

Already documented in `terminal-route-r17.md` (base rev):
- selection-file naming `${desktop}-xdg-terminals.list` vs `xdg-terminals.list` (:24-27);
- lookup order config-home → config-dirs → data-dir copies, system lowest (:28-32);
- format and `#` comments (:33-34);
- applicability check incl. `Categories`/`TryExec`/`Hidden`/`TerminalArgDir` (:40-46);
- duplicate entries, `XDG_DATA_HOME`-last-wins shadowing (:47-50);
- cache read-first / save-after-fresh-selection (:51-53);
- execarg defaults `execarg_default:` (:58-60);
- host declared chain and user-local desktop keys (:81-87, :103-107, :140-143).

Actually new (absent from r17):
- print-mode output semantics: `--print-id/--print-path/--print-cmd[=seq]/--print-delimiter`
  formatting, action suffix, `/./` removal (script 1328-1473);
- action options `--hold/--app-id/--title` and `X-TerminalArgAppId/Title` composition (r17
  records the keys' existence in the Host declaration table, not their composition);
- ShowIn/NotShowIn validation rules;
- exit-status map and error paths of the resolver;
- upstream test-suite artifacts (`.bats`, Makefile, man page — cf. ScoutSpecs pins) if opened
  as S326..

Note: if S326.. re-fetch script/README bytes already pinned as S057/S056, that risks
duplicate-source admission (W04-class); pin the new artifacts (tests/manpage) instead.

## F4 — The [UNK] is open at base but already narrowed; "closing" mis-assigns credit

- Verified at base: `terminal-route-r17.md:144-145` present at `60edb66…` (`jj file show`).
- Already narrowed before this round: cache bytes (`r17:123-127`) narrow "which entry the
  resolver selects"; round-23 `HostFoot.md:127,151` (`pgrep -x alacritty` → pid 2487; "the
  running terminal is `alacritty` (pid 2487)") and `SKILL.md:218` (3x alacritty running)
  narrow the launch side observationally.
- Round-17 `drafts/FrontierDraft.md:8` already states: "which terminal actually launches (the
  list's first valid entry is a documented rule, not an observed launch)".

A freeze crediting C2 with closing the [UNK] would attribute closure to work that partly
predates the round and partly is not performed by it.

## F5 — C1 capability-at-base: confirmed absent (premise holds)

- Base `tools/` listing (`jj file list -r 60edb66…`): mado-action-plan.py, mado-anims.py,
  mado-assessment.py, mado-binds.py, mado-devices.py, mado-eventq.py,
  mado-evidence-audit.py, mado-geometry.py, mado-globals.py, mado-monitors.py,
  mado-options.py, mado-tripwire.py, mado-verify.sh, mado-wsrules.py — no mado-terminal.py,
  no desktop-file resolver.
- `tools/mado-binds.py:2-10`: static resolver for the bind table (prints hyprctl-binds-shaped
  JSON); its dispatcher set includes `exec` (:56-69), so it knows the launch command string,
  not the terminal selection.
- `tools/mado-verify.sh:3261-3316`: terminals plane checks TOML parse, theme import,
  font/padding — not selection.
- `SKILL.md:121-127`: routes terminal questions to knowledge entries; no tool executes
  resolution.

Conclusion: C1 is a genuine new capability; no claim fix needed except wording (see F6).

## F6 — C1 wording overreaches the modeled surface ("which terminal does SUPER+RETURN launch")

- Hotkey: `bindings.conf:2` = `bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec
  --dir="$(omarchy-cmd-terminal-cwd)"` (`terminal-route-r17.md:81`).
- The tool models xdg-terminal-exec selection only — not the `uwsm-app` wrapper environment nor
  the `omarchy-cmd-terminal-cwd` value. Selection under the hotkey could differ from a shell-run
  print if `uwsm-app` alters the environment (exactly the RevengerUwsm question).

**Fix:** word the capability as "which terminal the host's xdg-terminal-exec resolver selects for
the SUPER+RETURN binding command", and document the uwsm-app / `--dir` seam as outside the
model; otherwise a future divergence becomes a predicate failure the tool cannot explain.

## F7 — C2 sequencing ambiguity: "receipt of the landed tool"

`claims.md:17` says the [UNK] is "answered by a live read-only receipt of the landed tool". If
"landed tool" means mado-terminal.py (C1), C2 becomes conditional on C1's counter success — unsafe
for a freeze whose instruments freeze before w2. The ExecLive seat spec runs the pinned real
script (print modes), not mado-terminal.py. **Fix:** pin the phrase to "receipt of the pinned
xdg-terminal-exec v0.14.3 script (print modes)"; state explicitly that mado-terminal.py is not
the observation source.

## Implementation-risk notes (not premise defects)

- C1 byte-identity requires emulating shell `printf %b` semantics, `find -L` symlink traversal,
  `awk` usage, and option-parsing quirks (`--print-delimiter='\n\n'`); the fixture grammar in
  make-w1-spec.py already covers these.
- C1 `explain` output is self-authored and unjudged; only print-mode stdout/rc byte-identity is
  judged — fine, but the "why" trace is documentation, not counter-verified.

## Appendix — quote locator verification (grep -n / python)

| quote | file:line |
|---|---|
| "whether the resolver actually picks" | terminal-route-r17.md:144 |
| "over the system one at launch" | terminal-route-r17.md:145 |
| "Whether a terminal process actually started from that selection" | terminal-route-r17.md:128 |
| "the last fresh selection was the user-local entry" | terminal-route-r17.md:127 |
| "Narrowed in round 17 (bytes, not behaviour)" | terminal-route-r17.md:140 |
| "bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir=" | terminal-route-r17.md:81 |
| "What the cache does NOT show: That the process started" | round-17/w2/reports/AttackP4Claims.md:62 |
| "resolver cache, mtime 2026-10-20 09:57" | round-17/w1/reports/HostTerminalFiles.md:33 |
| "the running terminal is `alacritty` (pid 2487)" | round-23/w1/reports/HostFoot.md:151 |
| "which terminal actually launches" | round-17/drafts/FrontierDraft.md:8 |
| "no lane tool resolves the terminal at" | round-47/claims.md:12 |
| "answered by a live read-only receipt of the landed tool" | round-47/claims.md:17 |
| "Static resolver for the bind table" | tools/mado-binds.py:2 |
| "plane: terminals (file)" | tools/mado-verify.sh:3261 |
| "Which terminal tree is live on this host" | SKILL.md:121 |
