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
| M1 | Receipt cited for a verdict token it does not record (R16-V1) | `round-16.md:131-132` at `27cd06f` vs `.ufo/waves/round-16/evidence/frozen-tampered.json` (measured `9dcf248`, exit 2 `frozen_error`); outside `round-16-verifier-spotcheck.md` R16-V1 | QUALITY 9 binds a verdict to a commit, not to the token a sentence attributes; it did not bite. A substring check would also have passed (the red selftest receipt carries `snapshot_tampered` got-side for other rows) | QUALITY 23 plus `.ufo/waves/round-17/label-check.py`: outcome-side tokens only, optional `measured_commit`. Red: `R16-V1-red` MISMATCH; mutants `want-side-only-mutant` and `superseded-commit-mutant` MISMATCH; greens ok; `EXPECT_SUMMARY: 7/7`, exit 1 (receipt `evidence/label-check.txt`). Append-only erratum at the end of `round-16.md`; recut receipt `evidence/frozen-tampered-recut.json` exit 2 `snapshot_tampered`, control exit 0 `frozen_match`. |
| M3 | Pre-registration internally inconsistent | `SCORECARD.md` round-17 declaration (`0175f13`): declared rubric V at 2/6 = 3.3333 while naming calibration 6.3636 the lowest; `measure.py` absent at `0175f13` and later stricter than the declared text | RevPreRegistration, CriticC2, RevRubricV (lane-dispatched advisers, not outside review) | SCORECARD correction (append-only): V is a new coverage sub-axis declared this round and is the lowest; both lowest rows (V and calibration) are worked, so the obligation holds under either reading. Instrument committed and bound before integration (`f52f43f`, tightened `ab0bc9b`, sha256 `4023124f…`); baseline 2/6 re-measured with identical bytes at both. Tightenings shown to bite: exact `surface: P<n>` line, pinned legacy paths, upstream-row surface relevance, facet floor. |
| M4 | Conflicting install instruction reached every seat | Each dispatched seat task ends with the appended tooling directive whose first channel is `sudo pacman -S --needed --noconfirm`; `w1/reports/SentinelHostPause.md` H1-H3 | Wave context pause sentence (prompt-level only) | L1 sent a binding reminder to all 70 seats at dispatch; wave-2 context states an explicit override (no installs by any channel this round). Whether any seat ran a package command is checked by the C3 tripwire over the round-17 transcripts, not asserted. |
| M5 | "Paused host-wide" stated as a host fact | `/var/log/pacman.log:2440-3152` (file read): 13 non-lane runs 07:45-09:39 on 2026-10-20, including a 09:15 `pacman -Syu` (mkinitcpio 41.1→42.2, kernel, hyprland 0.56.2-4); 0 lines from round launch 10:51 to measurement | CriticHonesty, CriticC3 | Report and SCORECARD say: the pause is an instruction to lanes; non-lane transactions ran before launch (actor unknown, operator-owned); R15-V1's current host state is `[UNK]`; the round-window count is re-measured at close. No lane remediation. |

M2 (recurring seat scope breaches) is recorded with the C3 capability below.

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
| S056 | https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md | README.md:166 "Each entry from the explicit selection list is checked for applicability:" (12 words) | `c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40` |
| S057 | https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec | xdg-terminal-exec:106 "set workdir of terminal." (4 words) | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` |
| S058 | https://raw.githubusercontent.com/alacritty/alacritty/v0.17.0/extra/man/alacritty.5.scd | alacritty.5.scd:35-37 "Imports are loaded in order, skipping all missing files, with the importing file being loaded last." (16 words) | `e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107` |
| S059 | host `~/.config/hypr/bindings.conf`, `~/.config/xdg-terminals.list`, `~/.config/alacritty/alacritty.toml` | bindings.conf:2 "bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir=" (10 words) | bindings `e574a1ed…0581`, list `d035da57…b71b`, toml `695301c8…24f8` (full in SOURCES) |
| S060 | host `/usr/share/xdg-terminal-exec/xdg-terminals.list` | line 3 "# i.e. /usr/share/xdg-terminal-exec/xdg-terminals" (3 words; bytes identical to upstream v0.14.3 list) | `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034` |
| S061 | https://wiki.archlinux.org/title/Alacritty (rejected) | line 24 "Versions before 0.13.0 used a YAML configuration file." (10 words) | `c39c563d…4600bb` (seat report `SrcTerminalAlternates`) |
| S062 | https://linuxjunkies.org/guides/configure-alacritty (rejected) | line 247 "Starting with 0.12, Alacritty switched to TOML" (7 words) — false against v0.13.0 CHANGELOG:36 | `08608a0b…bec2c653` |
| S063 | https://wiki.hypr.land/Hypr-Ecosystem/hypridle/ | [HW:6] "Configuration is done via the config file at ~/.config/hypr/hypridle.conf." (11 words) | `b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640` |
| S064 | https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/ | [LW:7] "If no config file is found in any of the searched paths, hyprlock exits with an error and your session will not be locked." (24 words) | `f69cff6bad5ee10c6e52fac08aca9a99473d8bbac5379ad1d47a92ba297eabf5` |
| S065 | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md | [HR:6] "support for dbus' loginctl commands (lock / unlock / before-sleep)" (9 words) | `f5b852eefe3c6d21ede9cef8b9b2dbf55d2e9423f1224b82592aa1b4759781f6` |
| S066 | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp | [HC:473] `if (MEMBER == "Lock") {` | `2dd4d73d4f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75` |
| S067 | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.hpp | [HH:23] `ignoreInhibit     = false;` | `f9e4e5587075fe34ae3279c4225b00661c686468035c4ad6cbe71e098fc0a2b8` |
| S068 | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/main.cpp | [HM:61] "No hypridle.conf file found in:" (5 words) | `379bf321a53edc56bde5f81fe070a2519a53bf17ca3b89937c1a027bad672a38` |
| S069 | https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/README.md | [LR:5] "Uses the ext-session-lock protocol" (5 words) | `83096def1a9760088ee6508d550f9498aab959176ae50f90720a57fe838f50f3` |
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
