# RevReadmeFrontier — corpus README frontier and index attack (round 35, wave 2)

Seat: `L1Mado35.RevReadmeFrontier` (leaf, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Mode: read-only falsification. Writes confined to `.ufo/waves/round-35/scratch/RevReadmeFrontier/` and this
file. No lane corpus file, counter, control, `SOURCES.md`, sibling lane, jj state or Git index was modified.
Installs/upgrades: none (coreutils, grep, python3 sufficed; pacman not touched).

**Audited snapshot:** `corpus/README.md`, sha256 `3bb9865fd12793f9adbb204175f33ca5ab69adb6103df2048bfc54300933694f`,
249 lines, 50 index rows, 50 `corpus/knowledge/*.md` notes. Every line number below is pinned to that hash.
Frozen copy: `.ufo/waves/round-35/scratch/RevReadmeFrontier/README.audited.md` (same digest).

**The file moved under me three times** during the attack (`7f348944…` 234 L → `a3769bef…` 246 L →
`3bb9865f…` 249 L), by the README-owning sibling. Findings below are stated against the final snapshot; where
the earlier snapshots carried an additional defect that has since been repaired, it is recorded in
"Already repaired" so the verdict is not read as stale.

## Verdict

The frontier **does still deny the round's own measurement, and it also carries one withdrawn inference**:

- `L101–103` denies that any new consumer measurement exists, while `L238–249` of the same file announces it.
- `L241` keeps the unqualified phrase "leaving no state behind", which the round's own errata withdraw.
- `L82` (the surface route) never leads to any of the three round-35 notes or the new section.
- `L246` lists `hyprlock`'s config as open, contradicting the r17 row at `L42`.

The index table itself is **complete and clean**: three rows at `L59–61`, `50/50`, row fidelity `0 errors`.

**Tally after peer review:** three prose inconsistencies (F1, F2, F4) plus one route gap (F3), one missing
supersession pointer (F5) and one evidence-class drop (F6). **F7's original premise is retracted** — it was
this seat's error, see the retraction under F7; F8–F9 are wording nits. Peer `L1Mado35.RevIndex` independently
confirmed F1/F2/F4 against the same bytes and independently found the F7 premise wrong. None of this moves
the index verdict.

## Assigned commands and gate results (quoted with exit codes)

```
# working tree mirrored to scratch (rsync, .git and .ufo excluded), then
$ python3 -I quality/check-index.py --root …/.ufo/waves/round-35/scratch/RevReadmeFrontier/mirror2
MADO_INDEX: root=…/scratch/RevReadmeFrontier/mirror2 indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0

# the assigned rev-mode command, at master
$ python3 -I quality/check-index.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev $(git -C … rev-parse master)
MADO_INDEX: rev=19e4ab3171c1540c40d6b12097745af98053b07d indexed=47/47 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0

# row fidelity (run on the lane root because the citations live under .ufo/)
$ python3 -I quality/check-index-rows.py --root /home/vgpnk/Projects/shokunin/mado-shokunin
MADO_INDEX_ROWS: root=… rows=50 errors=0 warns=0
exit=0

# context only (not this seat's claim): the frozen C1 counter still lands
$ python3 -I .ufo/waves/round-35/c1/count.py --root … --frozen …/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0
```

The `--rev master` run is a correct count of a **different universe**: the three round-35 notes are untracked
and their rows uncommitted at master, so rev mode sees 47/47 and cannot test this wave. `--root` on the
byte-identical mirror is the only valid working-set assay, and it is `50/50`.

## Findings

### F1 — HIGH — `L101–103`: the frontier still says the consumer measurement does not exist

> `- Idle/lock transitions and daemon stop-cause: [idle/lock unknowns](knowledge/idle-lock-plane.md)`
> `  §11 and [terminal dispositions](knowledge/closeout-r11.md) §5. No new`
> `  consumer or transition measurement is claimed.`

This round holds exactly that measurement. `corpus/knowledge/idle-lock-chain-armed-r14.md` §1 (`:15–17`)
records `hypridle` live as pid 1667 from a process probe; `.ufo/waves/round-35/fetch/S205.receipt.txt` records
`1667 /usr/bin/hypridle` plus the boot-0 start line `Oct 23 22:14:11 … Started hypridle.`; and r14's own
errata E1 pins it to the current boot. The same README announces it at `L238–239` ("the chain is armed on
this host"), so the file contradicts itself inside one screen. The transition half is genuinely open —
r14 `:36–37` UNK: *"No lock, screensaver or suspend transition was triggered or observed."*

The pointer is stale too: `idle-lock-plane.md` §11 item 1 is *"Why hypridle is not running"* (`:329`), a
premise r14 §2 and errata E1 replace with a moved state, not a false record.

**Superseded by:** `knowledge/idle-lock-chain-armed-r14.md` §§1–2 + errata E1/E2; S205 receipt;
README `L238–249`.
**Minimal fix:** split the sentence: *consumer presence measured 2026-10-24 (pid 1667, one start line in the
current boot); transitions, lock success and stop-cause still unobserved.* The "transition" half of the
current sentence is correct and survives.

### F2 — HIGH — `L241`: "leaving no state behind" is the withdrawn form of the claim

> `  surfaces while leaving no state behind ([offered in the bar](knowledge/idle-lock-offered-in-the-bar-r15.md)).`

The round's own errata withdrew this reading:

- r15 **E3** withdraws "built not to remember" — `omarchy-toggle-idle` stops/starts the `hypridle` process and
  writes no file, and `default/hypr/autostart.conf:1` (`exec-once = uwsm-app -- hypridle`) re-arms it at login.
- r15 **E5** scopes "leaves no trace" to on-disk state only; the toggle calls `notify-send`, so a notification
  may survive.
- r15 **E2** keeps the narrow claim: *"the choice leaves no state in the toggles directory"*.

The state is in fact readable, in two channels I re-read read-only:

```
$ cat -n ~/.local/share/omarchy/default/waybar/indicators/idle.sh
     3  if pgrep -x hypridle >/dev/null; then
$ sha256sum ~/.local/share/omarchy/bin/omarchy-toggle-idle ~/.local/share/omarchy/default/waybar/indicators/idle.sh
11979b4d4198526445ee124a66ce1d2b5607b9f62ad01a516f22bba66256b284  …/omarchy-toggle-idle
6d8d2c11d3c3b15fa0aa31a830410c98d9e630a7683a9cedffb888d10f0f1750  …/idle.sh
```

`idle.sh` derives the displayed state from `pgrep -x hypridle`, and the journal records the transition
(scope `Consumed` 2026-10-23 19:24:38, restart 22:14:11 — r12 E1 / r15 E2). "No state behind" also collides
with the same file's `L246` line, which correctly keeps "rendered bar pixels" and "the transient-scope unit
name" open.

**Superseded by:** r15 errata E2/E3/E5; r12 errata E1; `RevEntryR15` F1 (HIGH) and `RevQuoteS210` M1.
**Minimal fix:** *"leaving no persisted entry in the toggles directory; the state is whether `hypridle` runs,
re-armed at login by `autostart.conf`."*

### F3 — MEDIUM-HIGH — `L82`: the surface route does not lead to this round

> `| Screen / idle / lock | [idle/lock plane](knowledge/idle-lock-plane.md) §§2–5, §§7–11; [health register](knowledge/config-health-report-r3.md) F1 | Configs and actuator declarations; dated consumer/session snapshots and turnover errata | No idle/lock transition was exercised; consumer presence and stop-cause are dated observations/unknowns, not a new live verdict. |`

The table's stated purpose is "choose a surface". A reader entering by that route reaches only the
2026-10-14 plane and the round-3 health register: none of `idle-lock-never-asked-r12`,
`idle-lock-chain-armed-r14`, `idle-lock-offered-in-the-bar-r15`, and not the `L236` section, is linked. The
Limit cell also still frames consumer presence as an unknown with no mention of the 2026-10-24 pid-1667
measurement. This is the same defect as F1, one table earlier.

**Fix:** add the three notes to "Start here" and say consumer presence was re-measured 2026-10-24 while no
transition was fired.

### F4 — MEDIUM — `L246`: `hyprlock`'s config is not open

> `  Still open: idle/lock *transitions* (nothing was fired), lock success, hyprlock's own config,`
> `  rendered bar pixels and tooltip rendering, the transient-scope unit name, notification history, and the`

`L42` says the opposite: the r17 note joins "the host's declared files by sha256", explicitly including
`hyprlock.conf` — `idle-lock-route-r17.md:72-73` carries the digests (`b8d173dc…`, 742 B / 43 L for
`~/.config/hypr/hyprlock.conf`; `3ef010e7…` for the theme file it sources) — and `:95–105` reads its keys.
`idle-lock-plane.md` §11 item 4 (`:335–337`) states what is actually open — *"Whether `hyprlock.conf`/
`hypridle.conf` parse cleanly"* (no read-only check exists; loading them would mutate the session). As
written, `L246` contradicts `L42` and understates r17.

**Fix:** replace "hyprlock's own config" with "hyprlock/hypridle config **parse assurance**".

### F5 — MEDIUM — `L13` still asserts daemon absence with no supersession pointer

> `… idle/lock: hypridle \`inactive\` + no PID (§8 unknowns kept unknown); …`

r14 §2 deliberately refused to call the 2026-10-14 record false ("a state that has moved, not a false
record"), so the row is not a lie — but the README preamble (`L6–8`) says inherited "unknowns still govern",
and this row now directs a rechecking reader to the opposite of the current measurement. The round-35
section exists but the row does not point at it.

**Fix:** append "superseded for presence by r14 (pid 1667, 2026-10-24); see §Round-35".

### F6 — MEDIUM-LOW — `L60`: the transient-scope explanation is stated as receipt content

> `… and the unit probe reads \`inactive\` only because the daemon runs inside a transient scope.`

r14 §2 classes that explanation **INF**, and r14 errata E2 records that it is "materially true but
**unlicensed by S205**": the proving `uwsm … systemd-run --user --scope --unit=app-Hyprland-hypridle-…`
line is not in the receipt, and `is-active` does not distinguish rc=3 from rc=4.

```
$ grep -c "systemd-run\|uwsm\|scope" .ufo/waves/round-35/fetch/S205.receipt.txt
0        # exit 1
```

The row should carry the class (or cite the errata), not assert the mechanism as measured. The rest of the
row is now correct and matches E1 (one start line in the current boot).

### F7 — LOW — `L242`: the superseded claim is quoted but its carrier is not named

> `  This supersedes the earlier "the desktop never offers the choice" over-read, which was true of the setup`

**RETRACTED PREMISE (this seat's error, corrected by peer `L1Mado35.RevIndex`).** The first version of this
finding said the quoted phrase "occurs nowhere in `corpus/`". That is false, and the grep printed in that
version was an abridged two-line summary, **not** the command's output. The real result:

```
$ grep -rnF 'the desktop never offers the choice' corpus/
corpus/knowledge/idle-lock-offered-in-the-bar-r15.md:32:lock should be on. The premise that the desktop never offers the choice was drawn
corpus/README.md:242:  This supersedes the earlier "the desktop never offers the choice" over-read, which was true of the setup

$ grep -rn "never offers the" corpus/
corpus/knowledge/idle-lock-never-asked-r12.md:36:The package's round-12 text framed the finding as "the desktop never offers the
corpus/knowledge/idle-lock-offered-in-the-bar-r15.md:32: …
corpus/README.md:242: …
corpus/SOURCES.md:206: … (the idle lock was never asked about and never toggled …)
```

The phrase is present and locatable: r15 `:31–32` states it as the premise the running interface corrects,
and r12 `:36–37` carries it line-wrapped while naming its carrier — *"The package's round-12 text framed the
finding as …"*. Only the single-line `grep` could have made it look absent.

What survives is attribution imprecision: README `L242` says "the earlier … over-read" without naming the
package's round-12 text that r12 §3 `:36` names, even though the reader cannot tell from `L242` alone which
text was wrong. This is a wording nit, not a missing artifact.

**Fix:** append "the package's round-12 framing, per `knowledge/idle-lock-never-asked-r12.md` §3".

### F8 — LOW — `L243`: "two inferences" undercounts and mislabels

> `  path only. Wave-2 attacks falsified two inferences in the admitted text and both are withdrawn by errata:`

The errata withdraw at least three distinct claims — (a) "never toggled / never taken it" (r12 E1, r15 E2),
(b) "both fire the desktop's own lock command", plus the title's "the chain will fire" (r14 E2), (c) "built
not to remember" (r15 E3). The sentence's second example ("the 150 s step is a screensaver with no lock
call") is a factual OBS correction, not an inference. The register is presented as complete when it is not.

### F9 — LOW — `L236`: the heading names only the offer

> `### Round-35 idle-lock offer route`

The section carries the non-offer material that resolves F1 (setup-path negative, daemon presence, the
withdrawal register). Renaming to "Round-35 idle-lock surface route" would let a frontier reader find the
measurement.

## Checked and not defective (falsified hypotheses recorded)

- **"The frontier still says the idle-lock offer is unknown" — false as stated.** No README sentence claims
  the offer is unknown. The phrase "never offers the choice" exists only in the newly added `L242` and in the
  notes' own correction text. The offer is asserted at `L240–241` and in `L61`. The stale material is the
  *measurement disclaimer* (F1) and the *trace claim* (F2), not the offer's existence.
- **`L59` (r12 row)** now matches the note's errata: 13 executed items (12 `*.sh` + hook install), and the
  withdrawn "never toggled" is stated as withdrawn with the 19:24:38/22:14:11 journal facts. Correct as
  written; the note's E1/E2 are faithfully summarised.
- **`L60` (r14 row)**, apart from F6: "one start line in the current boot's journal", pid 1667, the 150 s
  screensaver-without-lock-call and 152 s lock are all errata-consistent.
- **`L61` (r15 row)** now states the one-state-named asymmetry (`E4`), "toggle writes no file", and the
  `autostart.conf` re-arm (`E3`), and dual-dates the copy (`E1`) — no overclaim found.
- **`L20` (idle-lock-plane row)** — "live timing, timer-reset behavior and parser assurance remain UNKNOWN.
  Initial daemon absence is a point sample … not current health." Still true; r14 explicitly preserves it.
- **`L42` (r17 row)** — "transitions and lock success stay `[UNK]`" holds; nothing in round 35 fired a
  transition.
- **Index universe** — 50 notes / 50 rows, no duplicates, no dangling, three rows inside the coverage-map
  table before `## Quality bar`; violations of all three modes fire in `RevIndex`'s negative controls.
- **C1 context** — the counter's `TARGET_MET` is shape-scored (lesson M35-2; `count.py:174,192` computes the
  digest without comparing it to the bytes read). `L248–249` states this correctly and correctly declines to
  rest the notes on it; all eight receipt reports have now landed (`RevQuoteS203…S210`).

## Already repaired mid-attack (recorded so the verdict is not overstated)

At `a3769bef…` the three draft rows carried the pre-errata claims (`twelve first-run scripts`, `two start lines
in the session journal`, `renders … displayed … never recorded`) and `L249` asserted "these three notes rest on
re-opened receipts" while `RevQuoteS204` was still pending and `RevQuoteS207` had not landed. An unnamed
sibling seat rewrote rows and section; the final snapshot fixes those. That earlier state is why the row text
must stay tied to the notes' errata blocks rather than to the notes' titles.

**Ownership correction.** This seat's first IRC note routed the four remaining prose defects to
`L1Mado35.RevIndex` as "the file you edited". That attribution was wrong: `RevIndex` states it is read-only on
the lane and wrote only `scratch/RevIndex/` and `w2/reports/RevIndex.md`; it independently re-verified the
`50/50` index result on the same bytes. The README edit target remains an unnamed seat — F1–F9 must be routed
to whoever owns `corpus/README.md`, not to `RevIndex`.

## Residual risk and verification gaps

- **No semantic LSP applies.** The artifacts are markdown/text; the strongest available check is byte,
  hash, grep and gate execution. Caller/definition analysis here means reading the producer scripts directly,
  which I did (`idle.sh`, `omarchy-toggle-idle` — read-only `cat`, sha256 above).
- **The file is a live edit target.** Three hash changes during this run. If the README owner edits again,
  F1–F9 line numbers shift; re-resolve against `3bb9865f…` or the frozen copy.
- **F7 retraction, and its blast radius.** The first version of F7 printed a two-line summary as if it were
  the output of the quoted `grep`; the command in fact returns r15 `:32`, r12 `:36` and `SOURCES.md:206` as
  well. No other finding rested on it, and the corrected block above now reproduces the real output. Peer
  `L1Mado35.RevIndex` caught it; its anchors for F1/F2/F4 were re-checked here against the same bytes
  (r14 `:15–17` / `:36–37`, r15 `:78–84` / `:87–93` / `:100–102`, r17 `:72–73` / `:95–105`) and all hold.
- **I did not re-measure the host's live idle state** (no `pgrep hypridle` of my own): the process facts are
  taken from S205's receipt and the landed `RevQuoteS205`/`RevQuoteS204` reports. My own host reads were the
  two script bodies and the receipts' bytes.
- **Notification history was not read** (r15 E5 leaves it open); nothing in this report depends on it.
- **C2 was not run** by this seat; the README quotes only C1, and the C1 run above is context, not a verdict
  on the notes' truth.

## Scratch artifacts

- `.ufo/waves/round-35/scratch/RevReadmeFrontier/README.audited.md` — frozen 249-line snapshot (`3bb9865f…`).
- `…/mirror/` — first mirror (`7f348944…`, 234 L, rows present, no round-35 section).
- `…/mirror2/` — final mirror (`3bb9865f…`) used for the `50/50` run.
