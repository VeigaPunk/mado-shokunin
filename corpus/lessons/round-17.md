author: mado-shokunin (L1 + lane-dispatched L2 advice)

# Round 17 — receipt labels, P4/P6 sourced routes, post-hoc transcript tripwire

Date: 2026-10-20. Baseline `27cd06f5067c3d3540ab9aa7cc734eb8eee162cc`;
pre-registration `0175f13`. Motivation: the admitted round-16 closure
(`round-16-verifier-spotcheck.md`, routed R16-V1/V2), the post-ceiling
coverage gap named by round 16, and the recurring seat scope breaches of
rounds 13-16. Wave evidence under `.ufo/waves/round-17/`.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M1 | Receipt cited for a verdict token it does not record (R16-V1) | `round-16.md:131-132` at `27cd06f` vs `.ufo/waves/round-16/evidence/frozen-tampered.json` (measured `9dcf248`, exit 2 `frozen_error`); outside `round-16-verifier-spotcheck.md` R16-V1 | QUALITY 9 binds a verdict to a commit, not to the token a sentence attributes; it did not bite. A plain substring check on `frozen-tampered.json` would have caught this one (the token occurs 0 times there); the outcome-side rule matters for receipts that carry the token only want-side (see the `want-side-only-mutant` claim) | QUALITY 23 plus `.ufo/waves/round-17/label-check.py`: outcome-side tokens only, optional `measured_commit`. Red: `R16-V1-red` MISMATCH; mutants `want-side-only-mutant` and `superseded-commit-mutant` MISMATCH; greens ok; `EXPECT_SUMMARY: 7/7`, exit 1 (receipt `evidence/label-check.txt`). Append-only erratum at the end of `round-16.md`; recut receipt `evidence/frozen-tampered-recut.json` exit 2 `snapshot_tampered`, control exit 0 `frozen_match`. |
| M3 | Pre-registration internally inconsistent | `SCORECARD.md` round-17 declaration (`0175f13`): declared rubric V at 2/6 = 3.3333 while naming calibration 6.3636 the lowest; `measure.py` absent at `0175f13` and later stricter than the declared text | RevPreRegistration, CriticC2, RevRubricV (lane-dispatched advisers, not outside review) | SCORECARD correction (append-only): V is a new coverage sub-axis declared this round and is the lowest; both lowest rows (V and calibration) are worked, so the obligation holds under either reading. Instrument committed and bound before integration (`f52f43f`, tightened `ab0bc9b`, sha256 `4023124f…`); baseline 2/6 re-measured with identical bytes at both. Tightenings shown to bite: exact `surface: P<n>` line, pinned legacy paths, upstream-row surface relevance, facet floor. |
| M4 | Conflicting install instruction reached every seat | Each dispatched seat task ends with the appended tooling directive whose first channel is `sudo pacman -S --needed --noconfirm`; `w1/reports/SentinelHostPause.md` H1-H3 | Wave context pause sentence (prompt-level only) | L1 sent a binding reminder to all 70 seats at dispatch; wave-2 context states an explicit override (no installs by any channel this round). Whether any seat issued a package command in the covered forms is checked by the C3 tripwire over the round-17 transcripts (`evidence/tripwire-r17.txt`: 149 files, 1 `live_probe` `ps` by RevSeparability, 133 unparsed spawns); `clean` would not mean no seat ran one. |
| M5 | "Paused host-wide" stated as a host fact | `/var/log/pacman.log:2440-3152` (file read): 13 non-lane runs 07:45-09:39 on 2026-10-20, including a 09:15 `pacman -Syu` (mkinitcpio 41.1→42.2, kernel, hyprland 0.56.2-4); 0 lines from round launch 10:51 to measurement | CriticHonesty, CriticC3 | Report and SCORECARD say: the pause is an instruction to lanes; non-lane transactions ran before launch (actor unknown, operator-owned); R15-V1's current host state is `[UNK]`; the round-window count is re-measured at close. No lane remediation. |

| M2 | Seat scope breaches recurred and lessons undercounted them; fences were prompt-only | `tools/mado-tripwire.py` receipts `.ufo/waves/round-17/evidence/tripwire-r13..r16.txt`; join `tripwire-pacmanlog-join.txt`: 4/4 mado-window package transactions (pacman.log:2410, 2422, 2423, 2429) each match one issued `sudo pacman` call (r13 GlobalCapture:19 wayland-utils; r14 ReviewSourceBar:41 `-Sw` and OutputSpec:65 `-S` wlr-protocols; r15 LibinputEvents:54 libinput). Undisclosed in the round's own lesson: r13 wayland-utils install (disclosed in LOG.md:798-799 and seat reports, absent from `round-13.md`); r15 ReviewDocsEra:50 `sudo -n true`; r16 CustomMan:24 second `pacman -Q waybar` (round-16 M5 says one). Package-query findings r13/r14/r15/r16 = 19/46/177/2 | QUALITY 21 and wave-context pause text (prompt-level); seat self-disclosure | Post-hoc tripwire (C3) run over every wave before any conduct sentence (SKILL "Post-hoc transcript tripwire (round 17)"). Shown able to fail: the round-15 anchor file exits 1 with 2 host_mutation findings on line 54; synthetic suites 9/9, 16/16, 33/33 including newline, heredoc, eval-spawn and multi-call cases. Detection only; it cannot prevent a call. Earlier lessons are not rewritten here; these counts supersede their "one query"/silence by reference. |

## Gate

Candidates considered: tag-pinned upstream hypridle/hyprlock and
xdg-terminal-exec/Alacritty sources; the two Hypr wiki pages; host file
bytes; Arch Wiki pages; third-party blogs; snippet-only results; the
protocol XMLs (ext-idle-notify, ext-session-lock) and logind docs.

Admit: documentary P6 and P4 routes from rows opened this round, joined to
host bytes. Reject: tier-C restatements as sole support; any source read only
as a search snippet (two drafted snippet rows were replaced before landing);
any claim that a tag or a pacman.log pkgver proves the running binary; any
claim that a listed terminal or a declared listener is observed behaviour.
Protocol XMLs and logind docs were opened by seats (reports
`SrcIdleNotifyProto`, `SrcHyprlockLockProto`, `SrcLogindLock`) but are not
cited by an admitted entry this round, so they get no row (row-only-for-use
is not required by the contract, but rows here stay tied to what landed).

New rows (all opened 2026-10-20; quote ≤25 words; raw SHA-256):

| id | URL / path | located quote | sha256 |
|---|---|---|---|
| S056 | https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md | README.md:166 "Each entry from the explicit selection list is checked for applicability:" (11 words) | `c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40` |
| S057 | https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec | xdg-terminal-exec:106 "set workdir of terminal." (4 words) | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` |
| S058 | https://raw.githubusercontent.com/alacritty/alacritty/v0.17.0/extra/man/alacritty.5.scd | alacritty.5.scd:35-37 "Imports are loaded in order, skipping all missing files, with the importing file being loaded last." (16 words) | `e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107` |
| S059 | host `~/.config/hypr/bindings.conf`, `~/.config/xdg-terminals.list`, `~/.config/alacritty/alacritty.toml` | bindings.conf:2 "bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir=" (10 words) | bindings `e574a1ed…0581`, list `d035da57…b71b`, toml `695301c8…24f8` (full in SOURCES) |
| S060 | host `/usr/share/xdg-terminal-exec/xdg-terminals.list` | line 3 "# i.e. /usr/share/xdg-terminal-exec/xdg-terminals" (3 words; bytes identical to upstream v0.14.3 list) | `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034` |
| S061 | https://wiki.archlinux.org/title/Alacritty (rejected) | line 24 "Versions before 0.13.0 used a YAML configuration file." (8 words) | `c39c563d…4600bb` (seat report `SrcTerminalAlternates`) |
| S062 | https://linuxjunkies.org/guides/configure-alacritty (rejected) | line 247 "Starting with 0.12, Alacritty switched to TOML" (7 words) — false against v0.13.0 CHANGELOG:36 | `08608a0b…bec2c653` |
| S063 | https://wiki.hypr.land/Hypr-Ecosystem/hypridle/ | [HW:6] "Configuration is done via the config file at ~/.config/hypr/hypridle.conf." (9 words) | `b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640` |
| S064 | https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/ | [LW:7] "If no config file is found in any of the searched paths, hyprlock exits with an error and your session will not be locked." (24 words) | `f69cff6bad5ee10c6e52fac08aca9a99473d8bbac5379ad1d47a92ba297eabf5` |
| S065 | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md | [HR:6] "support for dbus' loginctl commands (lock / unlock / before-sleep)" (10 words) | `f5b852eefe3c6d21ede9cef8b9b2dbf55d2e9423f1224b82592aa1b4759781f6` |
| S066 | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp | [HC:473] `if (MEMBER == "Lock") {` | `2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75` |
| S067 | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.hpp | [HH:23] `ignoreInhibit     = false;` | `f9e4e5587075fe34ae3279c4225b00661c686468035c4ad6cbe71e098fc0a2b8` |
| S068 | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/main.cpp | [HM:61] "No hypridle.conf file found in:" (5 words) | `379bf321a53edc56bde5f81fe070a2519a53bf17ca3b89937c1a027bad672a38` |
| S069 | https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/README.md | [LR:5] "Uses the ext-session-lock protocol" (4 words) | `83096def1a9760088ee6508d550f9498aab959176ae50f90720a57fe838f50f3` |
| S070 | https://flarexes.com/hyprland-getting-started-configure-screen-lock-brightness-volume-authentication-and-more (rejected) | 0 version tokens in 339 extracted lines; restates the wiki ("You can learn more about … at Hyprland Wiki") | `bf875a25…350ab90a` |

Status/recheck/used-by changes to existing rows: none (old→new: none).
Rows before→after: 55 → 70; tier A 51 → 63, C 3 → 6; mined 43 → 55,
rejected 4 → 7, queued 8 unchanged. Two drafted rows built from unopened
search snippets (Ubuntu manpage, GitHub master blob) were replaced before
landing by opened rejections (S061, S062) — row-only-after-opening.

Version binding: `/var/log/pacman.log` (file read, no package query) last
logs hypridle 0.1.8-2 (:1792), hyprlock 0.9.6-3 (:1798), alacritty
0.17.0-1 (:639), xdg-terminal-exec 0.14.3-2 (:2935); the tags read match
those pkgvers. A log line is not a running-binary fact.

## Boundaries and handoff

Both notes are documentary routes (`surface: P6`, `surface: P4`): no lock,
suspend, listener, terminal launch or reload was performed or observed.
P3 Walker and P5 themes remain without a sourced route. R15-V1 stays
operator-owned; this round does not readmit round 15.

## Capability (C3) — post-hoc transcript tripwire

`tools/mado-tripwire.py` (written by L1 after seat TripwireCore died on an
m_swe rate limit). Receipts in `.ufo/waves/round-17/evidence/`:
selftests `tripwire-selftest-{core,compound,hardening}.txt` (9/9, 16/16,
33/33, exit 0); anchor `tripwire-anchor-r15.txt` (exit 1; line 54
`call_38165` host_mutation `sudo` + `pacman:-S`; 8 findings over 7 calls);
rounds `tripwire-r13..r16.txt`; independent-oracle comparison
`tripwire-vs-oracles.json` (every oracle non-clean row is also a tripwire
finding; 21 tripwire-only rows listed for wave-2 audit); round-17 wave 1
`tripwire-r17-w1.txt` (70 seat files, `clean`, 1 unparsed spawn, 1
unparsed eval cell). Transcript digests: `session-index.json`.

## Wave-2 corrections (append-only, 2026-10-20)

Falsify wave (78 seats, reports `.ufo/waves/round-17/w2/reports/`). Same-round
rows corrected in place before closure, each logged old→new here:

- S066 anchor digest `2dd4d73d4f5c…` → `2dd4d73d6f5c…` (transcription nibble
  in the draft; wave-1 SrcHypridleSrc had it right; ReopenS066, AttackSourcesRows,
  AttackGateQuotesP6). Two w2 reports that echoed the wrong value as "fetched"
  (AttackP6General:24, ReopenS067:94) are not independent evidence.
- S059 anchor `alacritty.toml:1-27` → `1-28` (28-line file).
- S061 anchor: abbreviated digest → full digest, bound to the
  `action=raw` wikitext it was computed on; S062 anchor: line 247 bound to the
  `<article>` extraction (raw HTML has 145 lines); S070 anchor: recorded digest
  is not reproducible (per-fetch CDN token), verdict rests on extracted text.
- S071 added (user-local `Alacritty.desktop` bytes): the P4 note cited its
  digest without a row (ReopenS059S060, AttackReadmeRows). Gate: URL/path
  `~/.local/share/applications/Alacritty.desktop`, located quote `:7`
  "Categories=System;TerminalEmulator;" (1 word), sha256 `713703ba…d057683`.
  Rows 70 → 71; mined 55 → 56.
- Gate word counts S056 12→11, S061 10→8, S063 11→9, S065 9→10, S069 5→4.
- M2: the r13 wayland-utils install was disclosed in LOG.md:798-799 and seat
  reports (ScoutPrevRounds); only the round-13 lesson omits it.
- P6 note: `inhibit_sleep` mode-3 wording re-anchored to [HC:128]; `grace`
  removed as a config key (CLI-only); host `pam_faillock deny=10
  unlock_time=120` recorded against the wiki's 3/10-min example; §11 items 3,
  4, 5, 7 given explicit `[UNK]` dispositions; mode-3 fallback stated as
  undefined without lock-notify; `/bin/sh -c` [HC:289] and `uwsm/env:5` cited.
- P4 note: `scope:` line (Alacritty-only); applicability anchors corrected
  (:816-822, :885, :933-942, :1088-1090); shadowing anchored (:165-168,
  :779-781); resolver cache added as `[OBS, bytes]` (last fresh selection was
  the user-local entry; launch still `[UNK]`); version binding completed
  (:1214, :1946; script byte-identical to the tag); `uwsm-app` step named;
  "host-authored comments" corrected to Omarchy template text.
- C3 tripwire: fixed fd-before-command/verb redirections, mid-word `#`,
  glued `);` separators, `env -S`/`--chdir`, `flock -w`/`-c`, `stdbuf`/
  `exec -a`, `nice -n10`, `time -p`, xargs long options, `kill` exemption
  only for a first `-0`/`-l`, `loginctl -H`, `omarchy` dispatcher and more
  mutating helper names, `ps`/`dmesg`/`wl-paste`, `pacman -Fy`, attached
  `-b/path`, abbreviated long ops, eval import aliases and from-imports,
  non-literal `shell=`, MemoryError in eval, nested unparsed counters,
  `~/.omp/agent` boundary inversion, over-broad name refusal, duplicate scan
  roots, non-string timestamps, internal-error schema. Regression suite
  `tripwire/w2-regressions` 26/26. Still missed (honest limits, receipt
  `evidence/tripwire-w2-adversarial.txt` 4/26): variable/`$'..'` argv0,
  ssh/find -exec/watch/script/tmux/parallel/at/perl, base64-to-sh, chroot
  payloads, non-literal or getattr/exec Python spawns, JS eval cells.
  Real-transcript misses found by RevengeUnparsed: `MadoR14.SourceSafety:152,
  155` (`bash -c recipe` → `pacman -Q`) and `MadoR13.jsonl:470` (helper
  `run_record`) — three executed package queries the tool cannot see.
- C3 join: 4/4 holds by call start (`custom/tool_execution_start`), 3/4 by
  record timestamp; `MadoR14.OutputSpec.jsonl:65` is a cursor provider-history
  record (34 turns, 50 calls) whose line timestamp is write time
  (RevengeMultiCallRecord, AuditR14Join). The fifth in-window transaction
  (`pacman.log:2416` man-pages) was issued by sibling lane mori
  (`MoriR13.PipeSource.jsonl:28`, ConnectSiblings) — reported, not absorbed.
- Rubric V instrument: rows parsed only inside `## Registry`, duplicate ids
  fail (AttackRubricGaming E2). E1 (an invented row) cannot be closed by a
  counter without committed fetch receipts: V is "declared, joined sourcing";
  the non-author judge must re-open newly counting rows.
- label-check: `doc_text` only for `doc: mutant`; want-side containers
  ignored; exit code is the expectation verdict when every claim declares
  one; want-side mutant pinned to `245fd11`.


### Late wave-2 residuals (AttackLessonM1M3, append-only)

- M3: the instrument tightenings were shown to bite only in a wave-2 seat's
  `/tmp` lab (AttackLessonM1M3, AttackRubricGaming), not by a committed
  mutant receipt; "shown to bite" is seat-attested, not lane-receipted.
- M4: the binding reminder went to all 70 seats immediately after the
  dispatch call returned, i.e. while seats were already running, not before.
  The tripwire does not classify `uv tool`, `npx`, `pip`, `npm -g` or
  `cargo install`; the wave-1 context itself allowed `uv tool`/`npx`, so a
  `clean` round-17 scan says nothing about those installer channels.
- M5: the report referent is `.ufo/reports/round-17/mado.md` (fleet `fb81be5`);
  the close re-measure is `evidence/pacmanlog-round-window.txt` (0 runs from
  10:51). The cited range 2440-3152 starts the 09:39:21 transaction, whose
  completion lines run to 3160.
- M1's "exit 1" describes the checker before the wave-2 exit-code change; the
  hardened checker exits 0 when all 7 expectations are met
  (`evidence/label-check-final.txt`).
