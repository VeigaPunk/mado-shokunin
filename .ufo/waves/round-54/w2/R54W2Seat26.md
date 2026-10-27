# R54W2Seat26 — w2 falsification, item 26: Autostart range conflict

Seat: mutation-tester (leaf, no subagent dispatch). Wave w2, round 54, lane mado-shokunin.
Base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`; lane HEAD `350d30e4ec5531f65ce99a57efeb8216f38e678a`
(the freeze commit, which contains `claims-frozen.md`, `registration.md`, `fetch/` — all cites
below are to bytes committed at HEAD). No host reads; no live host state is asserted anywhere
in this report. Prior w1 report: `.ufo/waves/round-54/w1/R54Seat26.md`.

## 1. Attacked invariant (item 26)

**Claimed invariant:** the frozen C2 host set (`registration.md:73-76`) and its L1 provenance
(`fetch/README.txt:18`) describe the omarchy default autostart file's lines **1–6** as six
`exec-once = uwsm-app -- …` launcher lines, with `omarchy-hyprland-monitor-watch` inside that
range — i.e. every `autostart.conf:N` member of the frozen set for N∈1..6 is an owned-chain
launch surface (the C2 narrative, `claims-frozen.md:48-50`).

**Plausible defect (one):** the range endpoint `:6` is false. The lane's own committed byte
record shows `:6` is the **polkit-gnome authentication agent** (not a `uwsm-app` line) and the
monitor watcher sits at **`:9`** — outside the frozen set entirely. The registration inherited
the range from the L1 prose, and the prose itself contradicts the lane's committed copies.

## 2. Frozen contract lines (verbatim, exact spans)

- `claims-frozen.md:48-50` — surface narrative: "the omarchy/Hyprland `exec-once`/`bindd`
  lines launch every autostart app, the terminal binding and the idle re-arm through
  `uwsm-app`".
- `claims-frozen.md:63-64` — clause (c): "(c) the entry carries at least two host join
  citations among the frozen host set of `registration.md`".
- `claims-frozen.md:70-71` — C2 kill rule: "any real row/quote/host-join mis-verified →
  `verdict=TARGET_MISSED`".
- `registration.md:73-76` — the frozen host set:
  `~/.local/share/omarchy/default/hypr/autostart.conf:1`, `:2`, `:3`, `:4`, `:5`, `:6`;
  `~/.config/hypr/bindings.conf:2`; `~/.local/share/omarchy/bin/omarchy-toggle-idle:9`.
- `registration.md:87` — C2-CTL-6: "entry text carries none of the frozen host set" (an
  absence test only).
- `fetch/README.txt:17-19` — the pinned L1 prose (the only in-repo record of the host joins):
  > Host join points read-only at the same time:
  > `~/.local/share/omarchy/default/hypr/autostart.conf:1-6` (six `exec-once = uwsm-app -- …`
  > lines: hypridle, mako, waybar, fcitx5, swaybg, omarchy-hyprland-monitor-watch),
  > `~/.config/hypr/bindings.conf:2` (`SUPER, RETURN` → `uwsm-app -- xdg-terminal-exec …`),
  > `~/.local/share/omarchy/bin/omarchy-toggle-idle:9` (`uwsm-app -- hypridle`).

## 3. The lane's committed byte record (no host reads)

Seven tracked copies of `~/.local/share/omarchy/default/hypr/autostart.conf` (round-18 and
round-39 capture waves) are byte-identical:

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ for f in $(git ls-files | grep -i autostart); do sha256sum "$f"; done   # default copies only shown
acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441  .ufo/waves/round-18/fetch/NoteTheme/omarchy-autostart-v3.8.4.conf
acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441  .ufo/waves/round-18/fetch/ReopenS093/autostart.conf
acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441  .ufo/waves/round-18/fetch/ReviewThemeUpstream/omarchy-autostart-v3.8.4.conf
acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441  .ufo/waves/round-18/fetch/SrcOmarchyBackground/default_hypr_autostart.conf
acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441  .ufo/waves/round-18/fetch/SrcOmarchyThemeHooks/default_hypr_autostart.conf
acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441  .ufo/waves/round-39/w1/ExecOptionsRealTree/host-tree/.local/share/omarchy/default/hypr/autostart.conf
acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441  .ufo/waves/round-39/w1/SctHostTree/real-tree/.local/share/omarchy/default/hypr/autostart.conf
```

Lines 1–14 of the byte record (`sed -n '1,14p' <copy> | cat -A`, exit 0):

```
exec-once = uwsm-app -- hypridle$                                          <- :1
exec-once = uwsm-app -- mako$                                              <- :2
exec-once = ! omarchy-toggle-enabled waybar-off && uwsm-app -- waybar$     <- :3 (guarded, still uwsm-app)
exec-once = uwsm-app -- fcitx5 --disable notificationitem$                 <- :4
exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill$   <- :5
exec-once = /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1$     <- :6  POLKIT, not uwsm-app
exec-once = omarchy-first-run$                                             <- :7
exec-once = omarchy-powerprofiles-init$                                    <- :8
exec-once = uwsm-app -- omarchy-hyprland-monitor-watch$                    <- :9  WATCHER, outside 1-6
$
# Slow app launch fix -- set systemd vars$
exec-once = systemctl --user import-environment $(env | cut -d'=' -f 1)$
exec-once = dbus-update-activation-environment --systemd --all$
```

## 4. The three-way conflict

| source | span claim | watcher line |
|---|---|---|
| `registration.md:73-76` (frozen) | `autostart.conf:1`,`:2`,`:3`,`:4`,`:5`,`:6` are acceptable joins | not in the set (watcher range unaddressed) |
| `fetch/README.txt:18` (L1 prose) | `:1-6` = **six** `exec-once = uwsm-app -- …` lines | named **last of six** ⇒ at `:6` |
| lane byte record (7 copies, `acb6a668…`) | `:1-5` are `uwsm-app` lines; `:6` is polkit-gnome | **`:9`** |

`registration.md:73-76` and `fetch/README.txt:18` agree with each other (the registration
enumerates exactly the prose's six-line range) and both disagree with every committed copy of
the file in the lane. The conflict is inside the round's own documents; the live host file was
NOT read (seat fence) and is not claimed either way — same scoping as R54Seat30 already drew
(`w1/R54Seat30.md:421-425`: "this is reported as a **conflict**").

## 5. Relevant w1 record

- `w1/R54Seat26.md:63-98` (my w1 report, S26-2): the landed entry's only autostart span is the
  phrase "lines 1–6"; 0/8 frozen host strings matched literally; the entry's host facts are
  transcriptions of `fetch/README.txt` (the six app names appear verbatim there), so the entry
  inherits the prose's range error.
- `w1/R54Seat07.md:137-153`: byte listing of a committed copy; "`:6` is the polkit agent —
  **not a uwsm-app line at all**; `omarchy-hyprland-monitor-watch` is at `:9`, not within
  `:1-6`."; `:311` (F5, High): the `:1-6`/`:6` claim is "contradicted by every committed copy
  of that file (hash `acb6a668…`, rounds 18 and 39)"; `:312` (F6): `omarchy-toggle-idle:9` has
  "no registry row, hash or committed copy" — unverifiable from lane bytes.
- `w1/R54Seat27.md:219-230`: measured on the seven copies — "the frozen `:6` mapping is wrong
  and entry line 19 is right. This does not sink C2: clause (c) needs two joins and `:1`, `:2`
  are genuine `uwsm-app` lines"; `:302-306`: the exact command loop (`git cat-file -p` + sha256)
  and `git ls-files | grep -i toggle-idle` → empty.
- `w1/R54Seat30.md:421-425`: if the measured reading is right, "frozen host-set members
  `autostart.conf:6` and the `:1-6` range are **false joins**"; freeze is source-only, so
  reported as a conflict, not resolved.
- `w1/R54Seat33.md:175-177`: a naive matcher counts the entry's range citation as the `:1`
  member "while the entry's own prose says `:6` is the polkit agent and the monitor watcher is
  at `:9`, not `:6`".

## 6. Finding (verdict on item 26: CONFIRMED)

The autostart range conflict is real and lives in the frozen bytes themselves:

1. **`registration.md:73-76` admits a false join.** Clause (c) (`claims-frozen.md:63-64`)
   counts a citation of `autostart.conf:6` toward the ≥2 host-join floor; per the lane's own
   byte record that line launches `polkit-gnome-authentication-agent-1` — evidence about
   nothing in `uwsm-app`'s environment. C2-CTL-6 (`registration.md:87`) only rejects an entry
   citing **none** of the set, so it cannot catch a `:6`-based join.
2. **The true watcher line is excluded.** `omarchy-hyprland-monitor-watch` is at `:9` in every
   committed copy and is not a member of the frozen set; an honest entry citing the
   autostart half of the idle re-arm chain (`claims-frozen.md:49-50`) cannot book it. The set's
   only idle-re-arm member is `omarchy-toggle-idle:9`, a file with zero committed bytes
   (R54Seat07.md:312, R54Seat27.md:306) — unverifiable in-round.
3. **The L1 provenance is contradicted by committed bytes.** `fetch/README.txt:18` asserts
   `:1-6` = six `uwsm-app` lines; the byte record says five (`:1-5`, with `:3` guarded). The
   entry's provenance trio (`claims-frozen.md:57-59`) therefore certifies a manifest whose
   host paragraph is wrong at `:6`, and w1's landed entry transcribed that error before
   correcting it (R54Seat07.md:315, R54Seat26.md:71-78).
4. **Non-fatal scope** (R54Seat27.md:229-230): `:1` and `:2` remain genuine `uwsm-app` lines,
   so clause (c)'s ≥2 floor is still reachable honestly (`:1`/`:2` + `bindings.conf:2`, the
   byte-backed join). The defect is the `:6` member, the `:1-6` endpoint, and the watcher
   placement — not the whole set.

Per the freeze rules this is a coverage finding, not a license to edit: no predicate,
registration, pin or source file was changed; remediation, if accepted, belongs in a
pre-data re-registration (`claims-frozen-v2.md`), e.g. re-scoping the autostart members to the
committed-byte spans (`:1-5`, `:9`) with a committed host-join capture as the evidence base
(R54Seat26.md:96-99 remediation shape).

## 7. Mutation probe (role protocol)

Invariant I = "the pinned README span claim agrees with the lane's committed autostart bytes".
Defect carrier = the span token + watcher placement in `fetch/README.txt:18`. Detector D =
`det.py` (scratch-only; parses the README span claim — range, count word, parenthetical app
enumeration only — and checks each claimed line against the committed copy's bytes; exit 0 =
CONSISTENT, 1 = CONFLICT). Fixture: copies only, under
`/fast/scratch/hyaku/mado-r54/R54W2Seat26/fxt.g3nCbh` (autostart copy =
`round-39/w1/ExecOptionsRealTree/.../default/hypr/autostart.conf`, `acb6a668…`).

```
== RUN1 pristine ==  sha256 daff1f8671ee85d7f3ad9cc96a9f7b33abc8e2722b67afd53ee225fe62d78bbe
claim: autostart.conf:1-6 = 6 'exec-once = uwsm-app --' lines [hypridle, mako, waybar, fcitx5, swaybg, omarchy-hyprland-monitor-watch]
committed bytes: 'uwsm-app --' lines at [1, 2, 3, 4, 5, 9]
committed line 6 = 'exec-once = /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1'; monitor-watch at line [9]
VERDICT: CONFLICT
  - line 6 is not a 'uwsm-app --' line: 'exec-once = /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1'
  - app 'omarchy-hyprland-monitor-watch' sits at line(s) [9], outside claimed span 1-6
exit=1

== RUN2 mutated ==  (smallest point: ':1-6 (six … monitor-watch)' → ':1-5 (five …)' + 'with omarchy-hyprland-monitor-watch at :9', README copy only)
claim: autostart.conf:1-5 = 5 'exec-once = uwsm-app --' lines [hypridle, mako, waybar, fcitx5, swaybg]
committed bytes: 'uwsm-app --' lines at [1, 2, 3, 4, 5, 9]
VERDICT: CONSISTENT
exit=0

== RUN3 restored ==  cp pristine over work copy
daff1f8671ee85d7f3ad9cc96a9f7b33abc8e2722b67afd53ee225fe62d78bbe  README.work.txt
daff1f8671ee85d7f3ad9cc96a9f7b33abc8e2722b67afd53ee225fe62d78bbe  README.pristine.txt
cmp: identical
VERDICT: CONFLICT   (same two bullet lines as RUN1)
exit=1
```

Verdicts: pristine **conflict detected** (invariant falsified — the defect is in the frozen
bytes, not introduced by the probe); the corrected-span mutant is **killed** by the same
detector (distinguished, exit 0 vs 1), pinpointing the span token + watcher placement as the
discriminating point; restoration **exact** (hash equality + `cmp`). Detector note recorded
honestly: v1 matched app names across the whole claim line (double-counted `hypridle` from the
toggle-idle clause and rejected the legitimately-corrected mutant); v2 restricts the
enumeration to the parenthetical. Only v2's runs are quoted above. Lane bytes untouched
throughout — the mutation lived only in the scratch fixture copy.

## 8. Pinned commands re-run / NOT RUN

- `python3 -I quality/counters/c2-r54-uwsm-entry.py …` — **NOT RUN, absent**:
  `ls /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters | grep -c r54` → `0`,
  exit 1 (no r54 counter exists; same for C1).
- `sha256sum -c SHA256SUMS.txt` (in `.ufo/waves/round-54/fetch/`) — re-run: 3/3 OK, exit 0.
- `git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD` →
  `350d30e4ec5531f65ce99a57efeb8216f38e678a`; base `e25149fe…` is its parent lineage
  (`git cat-file -t` → commit).
- Worktree note for reproducibility: `git status --porcelain` shows ` M corpus/SOURCES.md`,
  `?? corpus/lessons/round-54.md` plus wave-dir files; the w1-era
  `corpus/knowledge/uwsm-app-environment-r54.md` is no longer in the worktree
  (`ls corpus/knowledge | grep -c r54` → 0, exit 1), so entry cites in §5 refer to the
  14:07/14:12 snapshots recorded in R54Seat07.md:315 and R54Seat26.md:71-78.

## 9. Fence attestation

Writes: this report only. Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat26` (det.py +
fxt.g3nCbh fixture) **removed before yield** — nothing remaining, no ENOSPC observed
(`/fast` at 28% use). No lane/fleet/sibling/source edit, no predicate/registration change, no
git/jj mutation, no host/config/service/compositor read or write, no package query, no tool
install, no live-host verification of the autostart file. No scratch or disk failure to report.

Report: .ufo/waves/round-54/w2/R54W2Seat26.md
