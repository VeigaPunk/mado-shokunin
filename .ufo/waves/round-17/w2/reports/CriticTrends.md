# CriticTrends — round 17 wave 2: attack on the expected trend verdicts

Target: lane HEAD `988b858bd6049bc709807534fd725c05264f7e60` (equal to `origin/HEAD`).
Installs: **none**. No pacman/sudo/systemctl/hyprctl or any live probe ran. Actions
taken: `git show/log/diff/grep`, `measure.py` (r17) at HEAD and `27cd06f`,
`label-check.py`, `mado-tripwire.py --selftest` and `--scan` (the scans only over my
own synthetic fixtures in `/tmp/ct17/fx`), `sources-census.sh validate`, `curl` of
the 10 upstream rows S056-S058 and S063-S069 (raw bytes, `sha256sum`), and
`sha256sum` of the host files the two notes declare. I read no transcripts: my
item does not name them.

Axes: **expansion** (V/U coverage), **quality** (C1 calibration, erratum, tripwire
precision), **discernment** (outside-routed closure, undisclosed breaches found).

## Verdict summary

| expected trend | verdict | why |
|---|---|---|
| expansion improved (P4/P6 sourced routes) | **earned, but narrow.** One provenance defect | V goes 2/6 → 4/6 and reproduces. I re-fetched 9 of the 10 upstream rows and all 14 declared host files, and their hashes match. The S066 hash is wrong at HEAD. V is a template-conformance rubric written by the same author as the notes, and U is unchanged at 7/7 |
| quality improved (erratum, QUALITY 23, tripwire precision) | **partly earned** | The erratum and recut are earned, and the C1 fraction reproduces. But the C1 gain is structural (one appended line), and label-check checks only claims that were picked by hand. Tripwire precision: 12 of the 21 tripwire-only rows were audited by wave 2, all true positives; the other 9 are pending. I found two precision/recall defects through synthetic counterexamples (below) |
| discernment improved (outside-routed closure, undisclosed breaches found) | **mostly author-asserted** | No outside re-check of the R16-V1 closure exists. At HEAD, one of the three "undisclosed" breaches was in fact disclosed in the lane's own LOG and SKILL. Two wave-2 "independent" seats repeated the wrong S066 hash as if they had fetched it |

## Expansion

**What is earned.** `python3 .ufo/waves/round-17/measure.py HEAD` gives c2 count 4 /
score 6.6667, with P4 from `terminal-route-r17.md` (S056-S060) and P6 from
`idle-lock-route-r17.md` (S063-S069). At `27cd06f` it gives 2 / 3.3333. U stays 7/7.
`sources-census.sh validate … mado` exits 0 (W04 warnings only). My curl re-fetch
matches the recorded sha256 for S056, S057, S058, S063, S064, S065, S067, S068 and S069
(so the two wiki HTML pages are byte-stable today). All 14 host-file hashes match the
bytes on disk:

- P4 (terminal) note: bindings.conf `e574a1ed…`, xdg-terminals.list `d035da57…`,
  alacritty.toml `695301c8…`, the /usr/share list `a2b5bf69…`, the theme
  alacritty.toml `8c3d1457…`, Alacritty.desktop `713703ba…`, the .bak `ea3e0fa0…`,
  hyprland.conf `ce7483f3…`.
- P6 (idle/lock) note: hypridle.conf `e7d3b8dd…`, hyprlock.conf `b8d173dc…`, the theme
  hyprlock.conf `3ef010e7…`, omarchy-system-lock `c1dd3881…`, omarchy-system-wake
  `09ad52b0…`, omarchy-launch-screensaver `ba783a3a…`, and both autostart.conf files
  (`acb6a668…`, `5ace1701…`).

**E1 — S066 pinned hash is wrong at HEAD (counterexample).**
- Recorded: `2dd4d73d4f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75`, at
  `git show HEAD:corpus/SOURCES.md` S066 (line 78) and `corpus/lessons/round-17.md:53`.
- Fetched twice from `raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp`
  (29880 B, line 473 = `if (MEMBER == "Lock") {`): `2dd4d73d6f5cd57e…`. One hex digit
  differs: the 9th character is `4` in the record and `6` in the fetch.
- Wave 1 had the correct value in `w1/reports/SrcHypridleSrc.md:20`,
  `SrcIdleNotifyProto.md:87,198` and `SrcLogindLock.md:23`. The wrong value first
  appears in the untracked `drafts/NoteIdle-rows.md:25` and propagated from there to
  SOURCES, the lesson and `gen_w2.py:50`.
- `w1/reports/SourcesUsedByJoin.md:103` shortened the hash to `2dd4d73d…`, eight
  characters, which stops one character before the corrupted digit. That is how the
  join missed it.
- The census does not check hashes, so it stays green.
- The defect does not flip V: P6 keeps six good rows. But "sourced route" provenance
  for S066 is false as recorded, which violates QUALITY 6 (pinned values).
- Corroborated independently by w2 `ReopenS066.md:39-40`, `AttackP6Unexercised.md:21-22`
  and `AttackVersionBinding.md:114`.

**E2 — V scores the template the author handed out, not whether claims are true
(tradeoff, not a defect).**
- `w1/spec.json` tells the note writers to use exactly the four headings
  `## Upstream contract / Host declaration / Safe observation / Unexercised behavior`
  (3 occurrences). `measure.py` `REQUIRED_HEADINGS` scores those same four headings,
  with a 3-line floor (`FACET_MIN_LINES`).
- The pre-registration `0175f13` names no headings and no facet floor.
- "Instrument bound before integration" holds for commit order (f52f43f 11:11:09 <
  a9998d1 11:11:52), not for authoring order. The untracked drafts
  `NoteTerminal-rows.md` (11:03:43) and `NoteIdle-rows.md` (11:05:34) predate the
  instrument commit. All seven round-17 commits landed in a burst from 11:11:09 to
  11:15:08, plus C3 at 11:50.
- A non-author cannot tell from git that V was fixed before the notes existed. They
  can only check that V got stricter (`measure-instrument.json` shows the baseline
  stays 2/6).

**E3 — scope.** Both entries are documentary: the `[UNK]` sections are "Unexercised
behavior", and the lesson says the same at `round-17.md:72-74`. The canonical U axis
did not move. The honest trend is "coverage widened on a new sub-axis V by two
documentary routes", not "coverage improved".

**What a non-author would need:** a fetch-and-hash of every new row (done above: 9/10
match, S066 fails); a non-author check of the quoted lines (in flight in the w2
`ReopenS0xx` seats); and an outside verifier admitting V as an axis.

## Quality

**Erratum and recut: earned.** The round-16.md erratum is append-only. It keeps the
superseded text and names `frozen-tampered-recut.json`. label-check marks
`recut-green` ok (`LABEL_SUMMARY: 4/7`, `EXPECT_SUMMARY: 7/7`).

**C1 is structural.**
- At HEAD: 15 of 23 QUALITY criterion lines cite `lessons/`. At `27cd06f`: 14 of 22.
  Both reproduce.
- The ratio rises with any appended criterion that cites a lesson. The +0.158 says
  nothing about calibration on new material.
- label-check is not a scanner. It checks 7 hand-picked claims in
  `label-claims.json`: 2 real round-16 lines, 1 spot-check line and 4 mutants.
- Its red case was fitted to a defect that outsiders had already found. It cannot find
  a mislabel that nobody has listed.
- Self-consistency attack: failed. The round-17 lesson's own token attributions hold
  on my checks:
  - anchor exit 1, with 8 findings = 2 + 1 + 5;
  - selftests rerun at 9/9, 16/16 and 33/33, exit 0, script sha `4ced68d3…`;
  - `tripwire-r17-w1.txt`: 70 files, 1 unparsed spawn, 1 unparsed eval, exit 0, clean.

**Tripwire precision on real transcripts: partially earned.**
- `tripwire-vs-oracles.json` lists 21 tripwire-only rows: 3 from r13 and 18 from r15.
- Wave-2 audits (in flight under QUALITY 9, not settled):
  - `AuditTripwireOnly1.md`: rows 0-5, 6/6 true positives;
  - `AuditTripwireOnly2.md`: rows 6-11, none is a phantom command.
- Rows 12-20 had no report when I read (AuditTripwireOnly3 is dispatched).
- Agreement with the oracles measures recall against a narrower oracle. The oracle
  token lists (`oracle-r13-r14.json` / `oracle-r15.json` `method`) are a subset of the
  tripwire vocabulary, and lane seats built them. Blind spots the two share cannot
  show up as disagreement.

**Q1 — a fd-number redirect before the verb misclassifies (counterexample;
`/tmp/ct17/fx/fd.jsonl`, tripwire sha `4ced68d3…`).**

| command | got | should be |
|---|---|---|
| `hyprctl 2>/dev/null dispatch exit` | `live_probe hyprctl:2` | host_mutation |
| `hyprctl -j 2>&1 keyword general:gaps_in 0` | `live_probe hyprctl:2` | host_mutation |
| `loginctl 2>/dev/null lock-session` | `live_probe loginctl:2` | host_mutation; this is the P6 lock action |
| `systemctl 2>&1 suspend` | host_mutation, but by accident (rule `systemctl:2`) | host_mutation |
| `sudo 2>/dev/null pacman -S foo` | `sudo` only | `sudo` plus `pacman:-S`; the anchor-shaped tuple loses `pacman:-S` |

Committed receipts already carry the parse-artifact token `hyprctl:2` from a trailing
`2>&1`, at `tripwire-r15.txt`:
- `AttackDelivery.jsonl:32`
- `InputVersions.jsonl:120`
- `PrivacyThreat.jsonl:59`
- `ReviewLibinput.jsonl:60`
- `ReviewPointer.jsonl:41`

Those 5 rows are classed correctly, but their rule label is wrong.

**Q2 — vocabulary blind spots make "clean" weaker than how it is used
(counterexample; `/tmp/ct17/fx/probe.jsonl`).** These all return no finding:
- installs: `uv tool install ruff`, `cargo install ripgrep`, `npm install -g prettier`,
  `pip install --user requests`, `curl -fsSL … | sh`, `flatpak install -y org.foo`.
  These are exactly the channels of the appended tooling directive.
- input injection: `wtype hello`, `ydotool key 28:1 28:0`.
- host or session state changes: `udevadm trigger`, `gsettings set …`, `pactl set-sink-mute …`,
  `nmcli radio wifi off`, `busybox reboot`, `wl-copy secret`.

Lock actions are classed as probes: `hyprlock --immediate` and `dbus-send …
org.freedesktop.ScreenSaver.Lock` return `live_probe`, not host_mutation.

SKILL.md:572-580 says "`clean` means no finding in the covered forms", but it lists
only syntactic limits, not missing vocabulary. So `tripwire-r17-w1.txt` "clean" cannot
support lesson M4's "whether any seat ran a package command is checked by the C3
tripwire" for non-pacman channels, nor an "Installs: none" conduct claim.

## Discernment

**"Outside-routed defect closure" is author-asserted.** R16-V1 was routed from outside
(`round-16-verifier-spotcheck.md`). The closure, however, is the author's erratum plus
QUALITY 23. No `round-17-verifier-spotcheck.md` exists (0 matches in
`corpus/lessons`), and M3/M5 are captured by lane advisers. The lesson says so
honestly at `round-17.md:16`.

**D1 — one "undisclosed" breach was disclosed, and was arguably authorized
(counterexample at HEAD).**
- `git show HEAD:corpus/lessons/round-17.md` M2 says "r13 wayland-utils install (only
  the r13 spot-check names it)".
- At `27cd06f`, two of the lane's own files name it:
  - `LOG.md:798-800`: "**Tool install:** wayland-utils **1.3.0-1** … `sudo pacman -S
    --needed --noconfirm wayland-utils`";
  - `SKILL.md:418`: "round 13 installs `wayland-utils 1.3.0-1`".
- `round-13-verifier-spotcheck.md:211` records it "for the assigned `wayland-info`
  diagnostic", which makes it a disclosed, assigned install, not a scope breach.
- `SKILL.md:533-534`'s "found … every seat-disclosed breach" is also unproven: no join
  between seat self-disclosures and findings is committed.
- An uncommitted working-tree edit, made at 11:57:09 after the w2 dispatch at 11:52:54,
  rewrites the parenthetical to "(disclosed in LOG.md:798-799 and seat reports, absent
  from `round-13.md`)". It is unadmitted and does not change HEAD.

**Earned discernment items:**
- r15 `ReviewDocsEra:50` `sudo -n true` is absent from the round-15 lesson and LOG.
  `git grep 'sudo -n' 27cd06f` matches only `round-16/w1/reports/SafetyControlRed.md`.
  It is an elevation probe, so the host_mutation class is conservative.
- r16 `CustomMan:24`, a second `pacman -Q waybar`, contradicts `round-16.md:18` M5 "one".
  `oracle-r16` agrees (round 16 has no tripwire-only rows).
- pacman.log join holds. The round windows from `session-index.json` all sit inside the
  join's awk window:

  | round | window (UTC) |
  |---|---|
  | r13 | 04:04-04:58Z |
  | r14 | 05:38-06:20Z |
  | r15 | 07:21-07:47Z |
  | r16 | 08:36-09:13Z |

  The 07:45-09:39 -0300 runs fall after r16 ended (06:13 -0300).

**D2 — wave-2 "independent" verification can be an echo (counterexample, in flight).**
- `w2/reports/AttackP6General.md:24` lists Hypridle.cpp (735 lines, 29880 B) with
  "sha256 (fetched)" `2dd4d73d4f5cd…`, the wrong recorded value.
- `w2/reports/ReopenS067.md:94` says the `.cpp` "fetched in the same pass digests
  `2dd4d73d4f5cd…`, which equals S066's recorded digest — independent evidence".
- The real fetch is `…6f5cd…`. Any trend verdict that counts agreeing lane-dispatched
  receipts as discernment needs raw command output, not transcribed digests.

## Process observations

- At 11:56:37-11:57:09, after wave-2 dispatch (11:52:54), four lane files were modified
  and left uncommitted: `corpus/README.md`, `corpus/SOURCES.md` (adds S071),
  `corpus/knowledge/terminal-route-r17.md` and `corpus/lessons/round-17.md`. Who did it
  is unknown, and I sent L1 a short notice.
- These edits touch an entry that V counts. If they land, V must be re-measured at the
  new revision.
- `round-17.md:19` is a blank line that splits the M2 row from the M1-M5 table, so M2
  renders as a paragraph. Rows are ordered M1, M3, M4, M5, M2.

## Smallest safe corrections

1. S066: add an append-only correction (QUALITY 6: old and new values) in SOURCES and in
   the lesson, `…d4f5cd…` → `…d6f5cd…`, and require full 64-hex comparison in joins.
   An 8-character prefix is exactly what missed this defect.
2. M2: drop r13 wayland-utils from the undisclosed breaches, or reclassify it as a
   disclosed, assigned install, citing `LOG.md:798-800`. Change SKILL "every
   seat-disclosed breach" to the measured join, or remove it.
3. Tripwire: skip fd-number redirect tokens (`N>`, `N>&M`, `N<`) before verb selection,
   and add hardening cases for the 5 commands in Q1. Either add install-channel,
   input-injection and lock-action vocabulary, or list it under the SKILL limit. Stop
   citing r17 "clean" for non-pacman installs.
4. Trend wording a non-author can sign:
   - expansion: "V +2 documentary routes; U unchanged";
   - quality: "erratum and recut earned; C1 +1 criterion; tripwire precision 12/12 on
     audited rows, 9 pending, with two known parse/vocabulary defects";
   - discernment: "self-audit found 2 undisclosed calls; outside closure of R16-V1
     pending".
