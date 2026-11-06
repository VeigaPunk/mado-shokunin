# mado round 90 — lessons

Round 90, hyaku run 15 (attempt 1 `MadoR90` declared and ran the wave; attempt 2 `MadoR90a2` froze, landed and measured). Two frozen claims from `.ufo/waves/round-90/claims-declaration-r90.md`: C1 coverage
capability (a read-only resolver of which xdg-desktop-portal backend serves each of the 21 impl interfaces, modelled on
xdg-desktop-portal 1.22.1 `src/xdp-portal-config.c` and scored against the installed binary's own decisions) and C2
operability (a runnable receipt-presence check over the lane's records changes, routed by round 89's spot-check D1).

## Mistakes

**M90-1 — six C1 fixtures appended a key to a host file that has no final newline, so the key merged into the host's last line.**
Class: fixture-construction — a case built by byte concatenation tested a different input than its id says.
Evidence: `/usr/share/xdg-desktop-portal/hyprland-portals.conf` is 32 bytes with no trailing newline (`[preferred]\ndefault=hyprland;gtk`).
The L1's first generator (`.ufo/waves/round-90/build/gen-c1-cases-r90.pre-M90-1.py`, the pre-fix bytes kept as evidence) built
k01, n02, n06, a01, a02 and a03 as `hostconf + I + "<Iface>=<value>\n"`, which yields one line
`default=hyprland;gtkorg.freedesktop.impl.portal.FileChooser=kde` — a default list whose second entry is a nonexistent backend
name, and no interface key at all. The oracle labelled those six cases truthfully (it parsed the merged line), so every label
was correct and every case was useless for the rule it was named after: `n06-iface-none-with-backend-first` could not see
`none`, which is why mutant M06 (`none` recognised only as the first entry) survived the first draft run.
Captured-by: the draft mutation run (M06 survived, its intended killer was n06) — no rule checked fixture bytes against the
case's intent; the oracle cannot, because a well-formed but unintended input still gets a true label.
Fix: the generator terminates the host bytes before appending (`hostconf = hostconf_raw + "\n"` when missing; replica cases
d01–d05 keep the raw bytes), and `.ufo/waves/round-90/controls/check-fixture-lines-r90.py` flags any `*portals.conf` line whose
value carries a second `org.freedesktop.impl.portal.<X>=` key. Shown able to fail: on the pre-fix generator's output it prints
six `merged …` lines and `FIXTURE_LINES: cases=89 merged=6 verdict=MERGED` (rc 1); on the frozen case file `merged=0`, rc 0.
The pre-fix bytes were re-run by attempt 2: `.ufo/waves/round-90/receipts/m90-1-fixture-lines-r90.txt` (pre-fix `merged=6`
rc 1; frozen file `merged=0` rc 0). Criterion: `QUALITY.md` 150.

**M90-2 — rounds 88 and 89 cited receipts their records commit did not carry (third occurrence of the class).**
Class: records-before-receipts — a records commit names `receipts/<x>` that only a later commit adds, so the cited
revision does not hold its own evidence.
Evidence: `python3 -I quality/check-receipt-presence.py --repo . --rev 498855cb` → `missing receipts/harm-final-r88.txt …
SCORECARD.md:5140`, `verdict=MISSING`; `--rev 51bf076f` → `harm-final-r89.txt` and `census-end-r89.txt` missing,
`verdict=MISSING`; `--rev 16ee97b5` (the later commit) → `verdict=OK`. Round-89 spot-check D1 and round-88 R4 routed it;
lesson M89-4 promised a check and none landed until now.
Captured-by: none before this round — `quality/check-deliverables.py` reports `CHECK101 … verdict=OK` and
`quality/check-evidence-pointers.py` is round-36 scoped (`.ufo/waves/round-90/receipts/c2-existing-checks-prefreeze-r90.txt`).
Fix: `quality/check-receipt-presence.py` (C2) gates the records commit in `--worktree` mode; this round's records commit
carries its own gate run (`.ufo/waves/round-90/receipts/c2-gate-records-r90.txt`). Shown able to fail: the two `MISSING`
verdicts above, and C2's 28/28 killed mutants. Criterion: `QUALITY.md` 151.

**M90-3 — attempt 1 wrote a pre-freeze control receipt that held only its argv, then ended before any commit.**
Class: receipt-without-output — a receipt file whose command ran (or was about to) but whose output was never written is
indistinguishable, to a reader, from a run that was never made.
Evidence: `.ufo/waves/round-90/receipts/c1-controls-prefreeze-r90.txt` was 863 B at attempt-2 start (header + `$ …` line
only; mtime 19:24:21, the declaration's mtime 19:24:09); `.ufo/watchdog.log` `lane-dead-no-report mado round=90` at
20:22:51; lane remote still `5041acf9`. Attempt 2 re-ran the identical argv and appended the output with a note
(`DRAFT_TARGET_MET … cases=229 correct=229`).
Captured-by: none — no lane check requires a receipt to end with a verdict line and an `rc=` line.
Fix: route, not land — a receipt-completeness check (last two lines are a verdict line and `rc=N`) is a candidate for a
later round; this round names it and does not claim it.

**M90-4 — two scout seats returned their findings only as final text, and the text was lost.**
Class: seat evidence held only in transport — R90MScoutSources and R90MScoutCases wrote no report file in the wave dir;
`w1-results.json` records `output: null` for every seat ("orchestrator kernel restarted mid-wave; seat output was … not
retained").
Evidence: `.ufo/waves/round-90/w1/` holds reports for 11 of 13 seats; the 66 `bl-` cases survive in the frozen case file
because attempt 1 merged them before the restart; S501–S503 were therefore re-opened by the L1 (Gate below).
Captured-by: none — the wave context asked seats to write reports, but nothing checked that a read-only seat did.
Fix: route — the next wave context names a report path for every seat, scouts included; this round does not claim it.

## Wave findings routed (instruments frozen or named as limits)

The w1 findings that changed the draft before the freeze are listed in the declaration's "Draft revisions" (R90MCritic
F1–F15, R90MReviewC1 O1/CAND-1–6, R90MReviewC2 G1–G3/W1/W2, R90MMutC1 X-mutants, R90MMutC2 P1–P4, R90MExecFuzz 24
minimised disagreements, R90MExecForgery label-lookup and oracle-shell-out forgeries, R90MConnector §4.1). Named limits
are carried unchanged in `SCORECARD.md` round 90.

## Gate

### Registry rows added (opened 2026-11-06 by R90MScoutSources in attempt 1; re-opened by the L1 `MadoR90a2` at 20:28 -03:00)

| id | locator | access | located quote (≤25 words) | line |
|---|---|---|---|---|
| S501 | https://codeload.github.com/flatpak/xdg-desktop-portal/tar.gz/refs/tags/1.22.1 (sha256 5afeda953c3743efaa1160e73d62c5bfcac2ceca60e0e134e9b48ed651783625) | 2026-11-06 | src/xdp-portal-config.c: "As a last resort, if nothing was selected for this desktop by ${desktop}-portals.conf or portals.conf, and no portal volunteered itself" | 827-829 |
| S502 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gkeyfile.c (sha256 e1d1270f6c9881daf8a9f49b41395cbdd8e99fa290212e8530e0bd3df23ff656) | 2026-11-06 | "if (key_file->start_group == key_file->current_group && strcmp (key, \"Encoding\") == 0)" | 1768-1769 |
| S503 | file:///usr/share/man/man5/portals.conf.5.gz (sha256 01eba9b4c14ce2e649e8451f722fb3af7d9b43dd15cd106f8ea33e81bd5fad51) | 2026-11-06 | "none — Do not provide a portal implementation for this interface." / "* — Use the first portal implementation found, in lexicographical order." | rendered 92-96 |

Re-open commands (L1, 2026-11-06): `curl -sSL <url> | sha256sum` for S501/S502 (tarball and the three `src/` files:
2da4fd83…, 6b38de15…, 2c009356…, all equal to the entry's pins), `sha256sum` of the S503 container, `pacman -Q
xdg-desktop-portal glib2` → `1.22.1-2`, `2.90.1-1`; quotes located with `sed -n` on the extracted files and
`man -l` on the page. R90MScoutSources' own report was not retained (M90-4), so these rows rest on the L1's re-open.

### Registry rows touched (old → new)

None.

### Candidates considered (round 90)

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/xdg-portal-routing-resolver-r90.md` (21-interface resolver, decision table, error signatures, host answers) | **admit** | every rule cites S501/S502 at a line; every decision-table row names a frozen case the installed binary labelled; the host run is a committed receipt | a 1.22.x release that changes `xdp-portal-config.c` |
| treating `portals.conf(5)` "lexicographical order" as the `*` rule | **reject** | S501's `*` takes the first *sorted* backend, and the sort ranks UseIn hits for the first desktop ahead of source-name order (`sort_impl_by_use_in_and_name` `:267-268`, applied at `:389-390`; `*` at `:693-711`, `:749-753`); case p08 and the host's sorted list `hyprland,gnome-keyring,gtk,kwallet` | a release whose sort is plain name order |
| re-using the round-12 hand table as the C1 baseline rule | **reject** (kept as a control) | the r12-rule control scores 70/229 on the frozen set (`receipts/c1-measured-r90.txt`) | none: it is a control |
| assimilating a `merge/mado/` theme | **reject** (`Assimilation: none`) | R90MConnector §keyword scan: the package's one portal-adjacent row (S329) is an unpinned master URL already held tag-pinned as S286; nothing on portals.conf, GKeyFile or receipts; collision check `.ufo/waves/round-90/assimilation/collisions` holds 94 ids (435 registry ids vs 147 staged) | a staged entry on portal routing with a pinned locator |

### Spot-check

Round-89 spot-check (`corpus/lessons/round-89-verifier-spotcheck.md`) routed D1 (records cite receipts committed later)
→ C2 + M90-2 + `QUALITY.md` 151; D2 (`SKILL.md` registry stops at `mado-r86-*`) → ten rows `mado-r87-*` through
`mado-receipt-presence` added after `mado-r86-clause-observations`; D3 (RS01/RS05/RS12 survive) → three selftest checks in
`tools/mado-mako.py` (59 → 62), each reconstructed mutant survives the base selftest and fails the new one
(`.ufo/waves/round-90/receipts/d3-mako-survivors-r90.txt`). Round 90's own non-author closure is pending (LEARNING.md).

### Census

- Start: `.ufo/waves/round-90/receipts/census-start-r90.txt` — `mado ok`, rc 0, 55 W04 warnings; 435 rows at the base.
- End: `.ufo/waves/round-90/receipts/census-end-r90.txt` — `mado ok`, rc 0, 55 W04 warnings; 438 rows (S501–S503, tier A 3).

## Considerthese

`considerthese/2026-11-06.md` proposal 4 — "Widen desktop coverage past bar + mako … xdg-desktop-portal / screen-share
(`xdph.conf`) …" — is what C1 does for the routing half: the lane now resolves, for the host's real configuration, which
backend serves each portal interface (gtk 11, hyprland 4, none 6). Still open from the same proposal: screen-share runtime
(`xdph.conf`, a live ScreenCast session), clipboard, hypridle volatility.

## Domain share

New or changed artifacts: one knowledge entry (desktop-facing), two tools (`tools/mado-portals.py` desktop-facing,
`tools/mado-mako.py` selftest-only), one records gate and two counters (lane-internal). Desktop-facing: 2 of 6.

