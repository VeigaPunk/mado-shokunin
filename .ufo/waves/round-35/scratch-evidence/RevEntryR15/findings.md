# RevEntryR15 raw findings

F1 Section 3 mechanism falsified.
  Entry: "The desktop keeps the state of its configuration toggles in one directory, and it holds
  entries for other toggles - but not for the idle lock (S210)" + INF "built not to remember".
  Host: omarchy-toggle-idle is process-based (pkill/uwsm-app), writes no file.
  toggles/hypr 2 files: flags.conf == default/hypr/toggles/flags.conf (cmp exit 0) -> placeholder;
  window-no-gaps.conf == the ONE installed toggle. "entries" plural false.
  flags.conf text says the directory IS for permanent flags -> contradicts "built not to remember".
  autostart.conf:1 re-arms hypridle at login -> actual reason a choice does not persist.

F2 Section 2 heading false against its own source.
  idle.sh: running -> {"text": ""} (no tooltip/icon). Absent -> tooltip "Idle lock disabled".
  One state is named, the enabled state is silence. Heading + SOURCES row S207 repeat "names the two states".

F3 Date provenance.
  mtime .1791314470 = 2026-10-03 17:44:32; filename epoch 1791314470 = 2026-10-06 16:21:10.
  Package's 2026-10-06 == epoch suffix. Backup mtimes are content mtimes:
  live config.jsonc 17:02:56.289420985 vs .bak.1792267376 17:02:56.289334445 (same instant).
  Section 5 calls it a divergence and does not say the two figures measure different clocks.
  No cited receipt carries the literal "2026-10-06"; the compared artifact has no source id.

F4 S209 receipt self-contradiction on "oldest".
  "oldest dated copy" block lead path = config.jsonc.bak (2026-10-11 by its own table);
  min line = .1791314470 (2026-10-03). Entry silently takes the min line.

F5 "the desktop keeps the state of its configuration toggles in one directory" is a state-store
  claim S210 does not carry (S210 = one path, 2 filenames, no contents, no scope).

F6 "leaves no trace" heading unscoped: toggle runs notify-send (lines 7,10). No disk persistence
  (mako has no persist directive) but a session-visible trace exists.

F7 Section 4 OBS and Section 5 carry no source id (gate counts them closed; prose still open).

HOLDS: 2026-10-03 oldest mtime; four copies (host census = 4); 4/4 handler; 2 files / 0 naming idle;
gate-quote 1 per id, 13-15 words, all substrings; receipt anchors; line refs 207/208, 207/212.
Counter: TARGET_MET exit 0.

## Re-take 2026-10-25T03:35:30 (entry 5806 B, sha256 82c08a46...fadfe, Err E1-E5 appended)

E1 verified exactly: stat Birth 2026-10-06 16:21:10.082789105, Change .083846414 == epoch 1791314470.
E2 verified exactly: journal 2026-10-23 19:24:38 app-Hyprland-hypridle-9408787a.scope Consumed (no Stopping/
  Stopped); start at 22:14:11; 4 hypridle lines in 18:00-23:59.
E3/E4/E5 verified against host files.
Gate re-audit on new bytes: 5 quotes, 1/id, 13-15 words, substring occ=1; counter TARGET_MET EXIT=0.

N1 correction grounded in unregistered bytes (omarchy-toggle-idle, autostart.conf:1, template identity):
   no S-id, no receipt, no SOURCES row.
N2 append-only errata: five withdrawn sentences still printed in §2-§5.
N3 "entries for other toggles" survives E3; only window-no-gaps.conf is a real entry.
N4 E2 withdraws "Section 4's closing inference"/"title" — neither exists (grep only matches E2 itself).
N5 §2 "does more than toggle (S207)" — idle.sh has no toggle path; toggle is config.jsonc:208 (S206).
