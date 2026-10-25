# ConnOverlap — does any other lane hold the idle-lock ground?

Seat: connector (leaf, no subagent dispatch). Round 35, wave 2 — falsify. Date: 2026-10-25.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only on the lane and on every
sibling: the only writes are this report and two artefacts under
`.ufo/waves/round-35/scratch/ConnOverlap/` (`scan.txt`, `sibling-sources-manifest.txt`).
No lane corpus file, counter, control, `SOURCES.md`, sibling lane, fleet file, jj state or
Git index was modified. **No installs and no upgrades: nothing was installed through any
channel and no pacman transaction was run (pacman is host-paused; nothing needed it).**

## Axes named

| Axis | What this seat can move | Round 35 carrier |
|---|---|---|
| **adjacency** | cross-domain awareness: another lane's ground reported, not absorbed (`AXES.md:16`) | `PRED-C2-r35-v1` calibration claim; `PROTOCOL.md:457-459` |
| **coverage** | `PROVINCE.md` lists every surface the lane's rows actually read (`AXES.md:11`) | `PRED-C1-r35-v1` closed_rows=8 |
| **calibration** | the claim's recheck trigger is decidable from the lane's own instruments | `PRED-C2-r35-v1` |

Claims C1 and C2 are the round's declared claims; the round shape maps C1→coverage and
C2→calibration. `freshness` is named below only where a move touches it second-order.

## Verdict in three lines

1. **No sibling lane holds a row or a note about `omarchy-toggle-idle`, the waybar
   idle indicator, `hypridle`, or `omarchy-first-run`.** Exact-term scan over all 21
   `corpus/SOURCES.md` (20 siblings + mado) returns hits **only inside mado's own file**;
   over the 20 sibling files the scan is empty, exit 1.
2. **`S203`–`S210` do not duplicate another lane's ground.** Three sibling declarations
   affirmatively *route* this ground to mado (tsukuroi `ADJ-03`/`OUT-004`, game-dev-3d
   `:75`, kotoba `:61`); none claims it.
3. **No contested-scope note is owed.** One *adjacency attribution* is worth one clause
   (§5) and one bounded move is proposed (§6) — neither is a contest.

## 1. Exact-term scan (the seat's literal ask)

Probe terms: `omarchy-toggle-idle`, `idle-indicator`, `hypridle`, `omarchy-first-run`.
Twenty sibling files, one command:

```sh
cd /home/vgpnk/Projects/shokunin
grep -rn --include=SOURCES.md -iE 'omarchy-toggle-idle|idle-indicator|hypridle|omarchy-first-run' \
  $(ls -d *-shokunin | grep -v mado-shokunin | sed 's|$|/corpus/SOURCES.md|')
# no output; rc2=1
```

| Lane | Exact-term rows | Notes rows | Verdict |
|---|---|---|---|
| audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mori, revenger, souji, tabi, tameshi, tsukuroi | **0** each | 0 | **NONE** |

All 21 files exist; the manifest with per-file sha256 of the 20 sibling files is
`scratch/ConnOverlap/sibling-sources-manifest.txt` (20 lines + header). Every name on the
fleet roster (`MANIFEST.json` → 13 lanes) is contained in the 21 scanned.

**Precision worth having, because the brief's probe list would hide it on a re-run:** the
literal command string `omarchy-toggle-idle` occurs **0 times in every `SOURCES.md`,
mado's included** — the rows word it as "the idle-lock toggle". It occurs only in the
entries and three receipts:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
grep -c 'omarchy-toggle-idle' corpus/SOURCES.md corpus/knowledge/idle-lock-*.md
# corpus/SOURCES.md 0 | -never-asked-r12 1 | -chain-armed-r14 0 | -offered-in-the-bar-r15 8
grep -l 'omarchy-toggle-idle' .ufo/waves/round-35/fetch/*.receipt.txt
# S206.receipt.txt, S208.receipt.txt, S209.receipt.txt  (3 of 8)
```

So a `SOURCES.md`-only scan proves *no sibling registry row* and nothing more; that is why
§2 also scans sibling `corpus/knowledge/`, sibling `corpus/` trees, sibling `PROVINCE.md`,
and the fleet `.ufo/`.

mado's own file is the only one that matches any of the probe terms (three of the four —
`idle-indicator`, `hypridle`, `omarchy-first-run` — plus the wider prefix `omarchy-toggle`),
which is the point: the rows are mado's own ground, not a copy of a sibling's:

```sh
cd /home/vgpnk/Projects/shokunin
for f in *-shokunin/corpus/SOURCES.md; do for t in omarchy-toggle-idle idle-indicator hypridle omarchy-first-run omarchy-toggle; do
  n=$(grep -ci -- "$t" "$f"); [ "$n" -gt 0 ] && echo -e "$t\t$n\t$f"; done; done
# idle-indicator 1  mado-shokunin/corpus/SOURCES.md
# hypridle      12  mado-shokunin/corpus/SOURCES.md
# omarchy-first-run 1 mado-shokunin/corpus/SOURCES.md
# omarchy-toggle   1 mado-shokunin/corpus/SOURCES.md
# rc_of_loop=1        (scratch/ConnOverlap/scan.txt)
```

## 2. Wider corroboration (rows, notes, declarations)

Cheap second and third passes, so a lane that words the ground differently cannot hide:

| Probe | Command | Result |
|---|---|---|
| sibling `corpus/knowledge/` notes | `grep -rliE 'hypridle\|omarchy-toggle\|idle-indicator' <lane>/corpus/knowledge` over 20 lanes | **0 files** |
| sibling `corpus/` trees for `toggle-idle\|idle-indicator\|idle\.sh\|omarchy-first-run\|idle lock\|idle-lock` | `grep -rniE …` over 20 lanes, mado excluded | **12 lines, all tabi**: `corpus/evidence/tabi-r4-1-network/**/step-5-async-idle.shape.txt` plus its `journey.json`/`MANIFEST.txt`/`.check` references — a network-run fixture named `async-idle`. Unrelated subject, no claim. Filtering tabi away: **rc=1, no output**. |
| `waybar` anywhere in sibling `corpus/knowledge/` | `grep -rli wordbar` over 20 lanes | kaidoku `2026-10-13-crash-evidence.md`, `2026-10-13-r2-crash-inspect-probe.md` (crash-scope process listing); kotoba `sibling-overlap-census-round49.md` (assigns the *config plane* to mado); tameshi `mutation-case-mado-verify.md` (mutates mado's verifier); tsukuroi `degraded-triage-r4.md:481,500`, `kill-event-deep-r8.md:141` (waybar as an OOM/kill scope member), `adjacency-anchors-r19.{md,json}`. **None claims the bar or its indicator.** |
| tsukuroi `corpus/SOURCES.md` `omarchy` rows | 22 hits, ids **S036 S037 S042 S043 S045 S100 S101 S102 S103 S113 S114** | boot chain, snapshot/rollback, stable-mirror headers, installer `pacman.sh`, update helpers — **omarchy as an OS substrate object**, not the desktop's idle toggle. No `hypridle`/`idle-indicator`/toggle row. |
| tsukuroi's instrument | `grep -n -iE 'hypridle\|hyprlock\|idle' tsukuroi-shokunin/tools/tsukuroi-census.sh` | no output, **rc=1** — tsukuroi's census does not even probe the daemon, so no duplicate measurement instrument exists. |
| sibling `PROVINCE.md` for `omarchy\|waybar\|hypridle\|idle` | `grep -niE … */PROVINCE.md` | only: game-dev-3d `:75`, kotoba `:61`, tsukuroi `:48,:124` (all routing *to* mado, §3), mado's own. **`~/.local/share/omarchy` appears in no sibling province at all.** |

## 3. Sibling declarations that route the ground here (corroboration, not contest)

- **tsukuroi `PROVINCE.md:48` (ADJ-03).** "Desktop rendering, bindings, menu or idle
  behavior needs configuration-level diagnosis | Tsukuroi retains: User-manager/unit,
  package and driver health; an active unit does not prove the UI works | mado".
- **tsukuroi `PROVINCE.md:124` (OUT-004)** and `corpus/knowledge/adjacency-anchors-r19.md:84`:
  "Mado owns the Hyprland, waybar, walker and terminal configuration plane,
  themes/wallpapers and screen/idle behavior." Pinned quote, `true`, from `mado/PROVINCE.md:3-16`.
- **game-dev-3d `PROVINCE.md:75`.** "Desktop/compositor display behavior belongs to
  `mado-shokunin`".
- **kotoba `PROVINCE.md:61`.** Records mado's scope as "desktop and compositor craft";
  records no competing claim on mado's surfaces ("no split on its scope surfaces").
- **souji `PROVINCE.md:38`, under **Refuses**.** "Operator config (`~/.config/**`, …)" —
  souji's receipt-gated removal explicitly does not reach `~/.config/waybar/`, so `S206`'s
  file and `S209`'s four `.bak*` copies are not in another lane's removal authority even
  though `souji`'s domain names the class "superseded config snapshots" (those are the
  *fleet root repo's* hygiene surfaces, `PROVINCE.md:8-9`).

## 4. Does mado's province cover the eight rows? (row by row)

`PROVINCE.md:6-10` owns `~/.config/hypr/`, `~/.config/waybar/`, `~/.config/walker/`,
terminal configs, "themes/wallpapers as declared files, screen/idle behavior
(hypridle/hyprlock where present)"; `PROVINCE.md:18` adds the omarchy **theme** plane
(`~/.config/omarchy/**`) and the read-only `~/.local/share/omarchy/themes` checkout.

| Row | Surface actually read (from the receipt) | Named in `Owns (surfaces)`? | Coverage verdict |
|---|---|---|---|
| S203 | `~/.local/share/omarchy/bin/omarchy-first-run` | **no** | undeclared surface |
| S204 | `.ufo/waves/round-35/fetch/S204.receipt.txt` (in-lane artefact; journal grep inside) | n/a (lane artefact) | evidence *mechanism* adjacent to tsukuroi, §5 |
| S205 | `hypridle.conf` (+ in-lane receipt: pgrep, `systemctl --user is-active`, `journalctl --user`) | config **yes**; probes **no** | mechanism adjacent to tsukuroi, §5 |
| S206 | `~/.config/waybar/config.jsonc` | **yes** (`~/.config/waybar/`) | covered |
| S207 | `~/.local/share/omarchy/default/waybar/indicators/idle.sh` | **no** (only `~/.config/waybar/` is named) | undeclared surface |
| S208 | `~/.local/share/omarchy/bin/omarchy-menu` | **no** | undeclared surface |
| S209 | `~/.config/waybar/config.jsonc.bak{,.1791314470,.1792203278,.1792267376}` | **yes** (`~/.config/waybar/`) | covered; souji refuses this tree (§3) |
| S210 | `~/.local/state/omarchy/toggles/hypr` | **no** | undeclared surface |

So four of eight rows (S203, S207, S208, S210) read **omarchy install/state trees that
`PROVINCE.md` does not name**, and S205's decisive probes are a systemd/journal reading.
This is *not* bleed — no sibling wants the ground — but it is exactly the coverage axis's
signal ("`PROVINCE.md` lists every surface; none unexplored without reason", `AXES.md:11`).
Precedent already exists inside the lane for reading the install tree without a province
line (S020 reads `~/.local/share/omarchy/default/hypr/*`; `config-health-report-r3.md:343,678-695,905,908`;
`idle-lock-plane.md:38,78,89`; `idle-lock-route-r17.md:74-75`; `executor-test-sufficiency.md:51`).

## 5. Is a contested-scope note owed? **No.** One adjacency attribution is owed.

`PROTOCOL.md:457-459`: "One domain per shokunin; a domain belongs to one shokunin. Contested
scope — evidence or work is reported in the lane report; the integrator arbitrates by
refining `PROVINCE.md` … silence is not a ruling and must never default scope to whichever
lane wrote first." A contest needs a second claimant. There is none: zero sibling rows, zero
sibling notes, zero sibling province lines, zero sibling instruments.

What *is* true is the weaker, adjacent relation — **evidence mechanic, not ownership** —
which tsukuroi itself separates at `PROVINCE.md:40-41`:
"Shared evidence is not shared ownership; unresolved ownership goes to the protocol
integrator, never to whichever lane answered first."

- **S205's unit reading.** `journalctl --user` + `systemctl --user is-active` is tsukuroi's
  declared Core surface ("systemd user units & timers … journal/boot triage",
  `tsukuroi-shokunin/PROVINCE.md:8-14`), and ADJ-03 says tsukuroi retains "User-manager/unit …
  health". The row's *question* (is the idle lock armed?) is mado's; the *unit-model
  explanation* ("the daemon runs inside a transient scope") is tsukuroi's retained
  mechanism. The lane has already demoted the explanation on evidence grounds — errata
  **E2** of `idle-lock-chain-armed-r14.md` says the inference is "materially true but
  **unlicensed by S205**", found by seats `RevEntryR14`/`RevQuoteS205` — but it does not yet
  say *whose ground the explanation is*. That is one clause, not a contest.
- **S204's journal negative.** Same mechanic, and w1's `ConnIdle.md` already recorded its
  limit ("S204's zero journal count does NOT clear a manual toggle — `omarchy-toggle-idle`
  kills via `uwsm-app`, which the journal would log only as a process stop"). Again: the
  limit is a journal-triage statement, i.e. tsukuroi's plane stating what a journal query can
  and cannot see.

Neither item needs integrator arbitration, and neither is a reason to change a verdict.

## 6. The one bounded move (proposal — not executed; this seat is read-only)

**Move: declare the omarchy desktop plane as a read-only surface, keyed to its checkout
revision, so the four undeclared rows stop resting on an unnamed tree and their `on-change`
recheck becomes decidable from mado's own instruments.**

The non-obvious part, and why it is worth one move rather than a wave:

1. `~/.local/share/omarchy` **is a git checkout and is not package-owned** —
   `git -C ~/.local/share/omarchy rev-parse HEAD` → `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`;
   `pacman -Qo …/bin/omarchy-menu` → `error: No package owns …`; worktree clean
   (`git status --porcelain` → 0 lines). So mado can observe the change event itself; **my
   first hypothesis — that `S207`/`S208`'s `on-change` trigger needs tsukuroi's update plane —
   is refuted.** No tsukuroi handoff is needed for change detection.
2. All three install-tree rows are tracked, with stable content commits:
   `bin/omarchy-first-run` → `f1fa7f694` (2026-07-12), `bin/omarchy-menu` → `1537547f9`
   (2026-05-08), `default/waybar/indicators/idle.sh` → `bf962f004` (2026-02-20).
3. `S210`'s `~/.local/state/omarchy/toggles/hypr` is **outside** the checkout (`readlink -f`
   is itself, 0 versioned paths) — its trigger stays operator action; do not revision-key it.
4. `PROVINCE.md` already permits the instrument: `mado-verify.sh` runs "read-only git on the
   omarchy checkout" (`PROVINCE.md:24-28` table row). No new privilege, no new tool.

**Realisation, in the only two places the corpus contract allows** (see §7 risks):
(a) an errata block in `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` recording
    "read-time HEAD `8fcc9d604`, clean worktree at read time" plus the three per-file
    commits, with the recheck recipe above; and
(b) one append-only refinement paragraph in `PROVINCE.md` naming
    `~/.local/share/omarchy/{bin,default}/**` and `~/.local/state/omarchy/toggles/**` as
    read-only evidence surfaces for desktop-config claims, **excluding** package/update
    diagnosis (tsukuroi) and secret-shaped content (kagi), citing tsukuroi `ADJ-03`/`OUT-004`
    as the routing precedent;
(c) one clause in the r14 errata naming the unit-scope reading as tsukuroi-adjacent (ADJ-03)
    rather than mado's own mechanism.

**Why this improves an axis without harming another.** It closes four undeclared surfaces
(*coverage*), makes the `on-change` rows' trigger determinate and re-derivable
(*calibration*/*freshness*), and names the borrowed mechanism (*adjacency*). It touches no
counter input: neither counter reads `PROVINCE.md`
(`grep -n 'PROVINCE\|province' c1/count.py c2/count.py` → no output, **rc=1**), and entry
prose is not digested by `c1/frozen.json` (which pins `receipts[sid].sha256` and the
entry→row map only). A live entry edit of exactly this kind has already been made this wave
and the counter still passes (see `RevRowsUsedBy.md` §"Observation window").

## 7. Risks, and the trap this move must not fall into

1. **Do NOT put the revision token in a `SOURCES.md` cell.** The lane's own contract says
   "Only `status`, `recheck` and `used-by` change in place, each logged old→new in that
   round's lesson" (`corpus/SOURCES.md:6-7`). The counter *would* tolerate extra text
   (`receipt["sha256"] in cs[5]` is a substring test, `c1/count.py:192`; the 1–25-word bound
   applies to the entry's `gate-quote:` line, `count.py:128,176`, not to the row cell), but
   the corpus contract forbids it. This is the cheap-looking edit a later seat will reach
   for; it is wrong for contract reasons, not counter reasons.
2. **Do NOT edit a receipt** to record the revision — `c1/frozen.json` pins all eight
   receipt sha256s; an edit flips `closed_rows` and `open_cites`.
3. **Seat collision.** Three seats read these rows (RevQuoteWords, RevRowsDigest,
   RevRowsUsedBy) and a sibling edited the three entries at ~03:35 this wave. Land (a) after
   those seats report, and do not restate or contradict E1/E2.
4. **Do not record a moving HEAD as a content pin.** HEAD moves on any omarchy update; the
   content pin stays the file sha256 already in each row. The revision is the *trigger*
   identity, and "clean worktree at read time" is what makes the per-file commit determine
   the content.
5. **Province scope creep.** A paragraph that names the whole install tree can read as
   claiming package/update ground. Keep it to read-only evidence use for desktop-config
   claims and name tsukuroi's ADJ-03 explicitly.
6. **`S209`'s evidence class.** The four `.bak*` files *are* "superseded config snapshots";
   only souji's `Refuses` line (`PROVINCE.md:38`) keeps them safe from a future re-scope of
   souji's removal authority. Worth one sentence in the errata so a later reader knows the
   evidence is operator-owned and not prunable by a lane.

## 8. Verification (what must be re-run after any landing)

Baseline captured this session, before any proposal:

| check | command | result |
|---|---|---|
| C1 | `python3 -I .ufo/waves/round-35/c1/count.py --root /home/vgpnk/Projects/shokunin/mado-shokunin --frozen .ufo/waves/round-35/c1/frozen.json` | `closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` **exit 0** |
| C2 | `python3 -I .ufo/waves/round-35/c2/count.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --frozen .ufo/waves/round-35/c2/frozen.json` | `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET` **exit 0** |
| counters do not read the proposed file | `grep -n 'PROVINCE\|province' c1/count.py c2/count.py` | no output, **rc=1** |
| rows still 11 cells | `awk -F'\|' '/^ *\| S20[3-9] \|\|^ *\| S210 /{print $2,"nf="NF-2}' corpus/SOURCES.md` | S203–S210 each `nf=11` |
| one gate-quote per id survives the errata append | `grep -c 'gate-quote: S207 ' corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | must stay `1` (append prose only) |
| revision keys reproduce | `git -C ~/.local/share/omarchy rev-parse HEAD`; `git -C ~/.local/share/omarchy log -1 --format=%h -- <file>` | `8fcc9d604…`, `f1fa7f694`, `1537547f9`, `bf962f004` |

The exact-term scan itself is re-runnable from `scratch/ConnOverlap/scan.txt`; the sibling
file digests are in `scratch/ConnOverlap/sibling-sources-manifest.txt`.

## 9. Residual / what this seat did not verify

- Sibling **live branches** were read at their working-tree state, not at pinned commits; the
  scan is a point sample of 2026-10-25. A sibling could add a row after this read.
- Only `*-shokunin` directories on disk were scanned (21 = superset of the 13-name roster).
  A lane without a directory would be invisible to this probe.
- Sibling `.ufo/` trees were probed only for the four exact terms
  (`grep -rniE 'toggle-idle|idle-indicator|omarchy-first-run' .ufo` → no output); sibling
  scratch/report prose was **not** exhaustively read. A sibling could hold round scratch
  prose about the idle lock that this scan did not open — no such claim was found, but the
  negative is bounded by those terms.
- I did **not** re-measure S205's claim as a verdict (that is `RevQuoteS205`/`RevEntryR14`'s
  seat). One read-only corroboration was run and is reported only as mechanism evidence:
  `/proc/1667/cgroup` → `…/app-Hyprland-hypridle-d4bd7533.scope`;
  `systemctl --user is-active hypridle` → `inactive`, **rc=3** (unit exists, stopped —
  distinguishing rc=3 from rc=4, which S205 did not record).
- The proposal in §6 is **not executed**. Any or all of it may be refused without changing
  §1–§5.

## Scope executed (commands, in order)

`ls -d *-shokunin`; per-file `wc -l`; `grep -ci` term loop over 21 `corpus/SOURCES.md`
(`scratch/ConnOverlap/scan.txt`); sibling-only `grep -rn --include=SOURCES.md` (rc=1);
`grep -ciE 'idle|waybar|omarchy|hypr'` per lane; `grep -rniE 'toggle-idle|idle-indicator|idle\.sh|omarchy-first-run|idle lock|idle-lock'` over 20 sibling `corpus/` trees and over
`.md`-only non-`.ufo` trees; `grep -rliE` over 20 sibling `corpus/knowledge/`; `grep -niE` over
all `*/PROVINCE.md`; reads of `mado/PROVINCE.md`, `souji/PROVINCE.md:1-42`,
`tsukuroi/PROVINCE.md:1-14,40-52,118-132`, `game-dev-3d/PROVINCE.md:75`,
`kotoba/PROVINCE.md:61`, `tsukuroi/corpus/knowledge/adjacency-anchors-r19.md:1-4,84`;
`grep -n -iE 'hypridle|hyprlock|idle' tsukuroi-shokunin/tools/tsukuroi-census.sh` (rc=1);
`sha256sum` of the 20 sibling `SOURCES.md`; row extraction via `python3` over
`corpus/SOURCES.md:205-212` (11 cells each); `cat` of `fetch/S205.receipt.txt`,
`head` of `S206`, `S209`, `S210`; `python3 -I` runs of both frozen counters (both exit 0);
`grep -n` of `c1/count.py` constraints and `c2/count.py` docstring; `diff`/`grep -c '^| S'`
of `controls/golden/corpus/SOURCES.md` (8 rows) vs live (200 rows); read-only host probes
`git -C ~/.local/share/omarchy rev-parse HEAD|status --porcelain|ls-files|log -1`,
`pacman -Qo`, `ls -ld`/`readlink -f` of `~/.local/state/omarchy`, `cat /proc/1667/cgroup`,
`systemctl --user is-active hypridle` (rc=3), `systemctl --user list-units --type=scope`.
No write outside `scratch/ConnOverlap/` and this report; no package, service, unit, lock,
toggle or compositor action.
