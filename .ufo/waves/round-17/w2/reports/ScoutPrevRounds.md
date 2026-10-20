# ScoutPrevRounds — prior-round disclosure anchors

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD `988b858bd6049bc709807534fd725c05264f7e60`.
Read-only: no edits outside this report, no delegation, no package query, no sudo, no
live probe. Installs this item: **none**.

Assigned question: does round 13 disclose its `wayland-utils` install, and does round 15
disclose `sudo -n true`? Each answered from file bytes only, with the grep quoted.

---

## Q1 — r13 `sudo pacman -S --needed --noconfirm wayland-utils` (pacman.log:2410)

### Q1a `corpus/lessons/round-13.md` — ABSENT

```
$ grep -n -i -E "install|sudo|tool install|pacman -S" corpus/lessons/round-13.md
(no output, exit 1)
$ grep -c "wayland-utils" corpus/lessons/round-13.md
1
```

The single hit is a source row, not an install record:

```
40:| S046 (new) | https://gitlab.freedesktop.org/wayland-utils/-/raw/1.3.0/wayland-info/wayland-info.c; tag 1.3.0 @ d01edd68961ca01779dcb96afe56c2d99ff79067 | :2744, colour-manager output query: `wp_color_manager_v1_get_output(` | mined after AttackCoverage A1; ... |
```

The 95-line lesson has no “Tool install” section and no host transaction sentence.
**Observation: the round-13 lesson does not disclose the install.**

### Q1b `LOG.md` round-13 entry — PRESENT, explicit

Entry heading is `LOG.md:769` (`## 2026-10-20 — round 13: protocol boundaries and named-set census`); next heading is `LOG.md:917`. Inside it, `LOG.md:798-801`:

```
798:**Tool install:** wayland-utils **1.3.0-1**, pacman extra,
799:`sudo pacman -S --needed --noconfirm wayland-utils`, to obtain the assigned
800:`wayland-info` diagnostic route; GlobalCapture read RULES.md first.
801:No partial upgrade or system update. Capture/replay: 72 advertisements,
```

This names package, version, repository, the exact `sudo pacman` argv, the reason and the
no-partial-upgrade claim. `grep -c "wayland-utils" LOG.md` = 2 (the two quoted lines; no
other mention).

### Q1c Counterexample to round-17 M2

`corpus/lessons/round-17.md:20` (M2 evidence cell) states:

> Undisclosed in the round's own lesson: r13 wayland-utils install **(only the r13 spot-check names it)**; r15 ReviewDocsEra:50 `sudo -n true`; ...

The first clause is true for `corpus/lessons/round-13.md`; **the parenthetical is false.**
At least five records name the install, not one:

| record | line | what it names |
|---|---|---|
| `LOG.md` | 798-799 | `wayland-utils 1.3.0-1`, pacman extra, full `sudo pacman -S --needed --noconfirm wayland-utils` |
| `.ufo/waves/round-13/w1/reports/GlobalCapture.md` | 15-18 | “`wayland-info` was absent; `wayland-utils 1.3.0-1` was installed … Tool record: wayland-utils 1.3.0-1, pacman extra, reason = assigned read-only globals probe” |
| `.ufo/waves/round-13/w1/reports/EvidenceChain.md` | 81, 167-168 | “installed via authorized channel `pacman -S --needed --noconfirm wayland-utils`” |
| `.ufo/waves/round-13/w1/reports/ReviewPhases.md` | 24 | host package + `pacman -Qi` Install Date `Tue 20 Oct 2026 01:06:49 AM -03` |
| `corpus/lessons/round-13-verifier-spotcheck.md` | 211 | “Lane installation verified from its record and installed package: **wayland-utils 1.3.0-1**” |

The only restricted reading under which the parenthetical survives is
[INFERENCE] “only among `corpus/lessons/*.md`”. The sentence as written — and as the
audit trail a later round would read — asserts exclusivity over all records, and `LOG.md`
is the round's own closure record. This is a factual overstatement inside the round-17
correction row itself; the r13 lesson omission it documents is real, the exclusivity
claim is not.

Note: `SCORECARD.md` has `grep -c "wayland-utils"` = 0, so the LOG is the only
top-level lane record outside the lesson/spot-check that carries it.

---

## Q2 — r15 `sudo -n true` at `MadoR15.ReviewDocsEra.jsonl:50`

File: `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR15/MadoR15.ReviewDocsEra.jsonl`
(75 lines; read only, per the item's named anchor).

### Q2a The anchor is real and was issued, not quoted

Line 50 is `type: message`, `message.role: assistant`, `timestamp: 2026-10-20T07:25:11.711Z`,
carrying five tool calls; index 4 is `toolCall bash` with:

```
{"command": "pacman -Qi hyprland | grep -E 'Depends|Required' ; ... ; sudo -n true 2>&1 | head -1 >/dev/null; echo ok", "i": "Checking dependents and install dates"}
```

So the probe is a deliberate non-interactive privilege check with its output discarded
(`2>&1 | head -1 >/dev/null`). The round-17 tripwire receipt independently classifies it:

```
$ python3 -c "... tripwire-r15.txt findings where class=='host_mutation' ..."
MadoR15.LibinputEvents.jsonl 54 sudo | sudo pacman -S --needed --noconfirm libinput libinput-tools
MadoR15.LibinputEvents.jsonl 54 pacman:-S | pacman -S --needed --noconfirm libinput libinput-tools
MadoR15.ReviewDocsEra.jsonl 50 sudo | sudo -n true 2
```

**Observation: the r15 anchor is exact (file, line 50, rule `sudo`).** The receipt's stored
`command` string is truncated at the redirect to `"sudo -n true 2"`; the line/rule identity
is correct, so the join file's `sudo -n true` wording is not overstated.

### Q2b Round-15 disclosure — ABSENT in every record tested

```
corpus/lessons/round-15.md                  : sudo -n = 0
corpus/lessons/round-15-verifier-spotcheck.md: sudo -n = 0   (also 0 hits for "ReviewDocsEra")
LOG.md                                      : sudo -n = 0   (also 0 hits for "ReviewDocsEra")
SCORECARD.md                                : sudo -n = 0
.ufo/waves/round-15/w1/reports/ReviewDocsEra.md : sudo -n = 0  (also 0 for sudo|privilege|elevat|root)
.ufo/waves/round-15/ (whole tree, recursive): 0 files contain "sudo -n"
```

Round 15 does disclose its *other* elevated action — `LOG.md:1093` quotes
`sudo pacman -S --needed --noconfirm libinput libinput-tools` and M2 owns it — but the
`sudo -n true` probe appears nowhere, including the seat's own report.

**Observation: `tripwire-pacmanlog-join.txt:11` (“undisclosed in round-15 lesson/LOG: grep
count 0”) is accurate.** This half of round-17 M2 stands.

---

## Verdict

| claim under attack | result |
|---|---|
| r13 lesson omits the install | **confirmed** (grep 0 for install/sudo/pacman argv; sole hit is S046 URL) |
| LOG r13 entry omits the install | **FALSIFIED** — `LOG.md:798-799` quotes the exact argv |
| “only the r13 spot-check names it” (`round-17.md:20`) | **FALSIFIED** — LOG plus 3 seat reports plus the spot-check |
| r15 `sudo -n true` exists at `ReviewDocsEra.jsonl:50` | **confirmed** (issued bash tool call, 07:25:11.711Z) |
| r15 leaves it undisclosed | **confirmed** (0 hits across lesson, LOG, spot-check, SCORECARD, wave tree, own report) |

Net: the round-17 M2 correction is directionally right that lessons undercounted
breaches, but its r13 parenthetical overstates the gap by one record class. The minimal
append-only fix is to drop “only” or add “LOG.md:798-799 and the r13 seat reports also
name it”. No rewrite of r13 history is warranted; the r15 half needs no change.

## Residual unknowns

- `MadoR13.GlobalCapture.jsonl:19` was not opened (outside this item's named read set);
  the join file's r13 anchor is therefore accepted as cited, not re-derived here.
- Whether QUALITY/SKILL defines “disclosure” as lesson-only is not codified: QUALITY 20/21
  govern install permission, not disclosure location (`corpus/QUALITY.md:72-92`). The
  exclusivity test above is therefore against record wording, not a written rule.
- `MadoR15.jsonl` (top-level orchestration transcript) and `agent.db*` were not read;
  the probe's absence there is untested and not claimed.
