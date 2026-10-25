# RevReadmeFrontier — corpus README frontier and index attack (round 35, wave 2)

Seat: `L1Mado35.RevReadmeFrontier` (leaf, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Mode: read-only falsification. Writes confined to `.ufo/waves/round-35/scratch-evidence/RevReadmeFrontier/` and
this file. No lane corpus file, counter, control, `SOURCES.md`, sibling lane, jj state or Git index was
modified. Installs/upgrades: none (coreutils, grep, python3 sufficed; pacman not touched).

**Audited snapshots (two, because the owner edited mid-report):**

- F1–F9 were written against sha256 `3bb9865fd12793f9adbb204175f33ca5ab69adb6103df2048bfc54300933694f`, 249 lines.
- The owner then shipped revision 4, sha256 `de5b885a793f5a773ab1dc69016ea38e185e8f77b920d2ad7b300bc7c6310ac6`, 254 lines.
  The "Revision-4 re-audit" section below gives each finding's current status and current line number; the
  F1–F9 bodies remain the record of what was wrong in the revision they cite.

Frozen copies, and how to read them after the scratch relocation:

```
git cat-file -p 4efaf63:.ufo/waves/round-35/scratch-evidence/RevReadmeFrontier/README.audited.md | sha256sum
→ 3bb9865fd12793f9adbb204175f33ca5ab69adb6103df2048bfc54300933694f   # 249 L, the audited revision
git cat-file -p 4efaf63:.ufo/waves/round-35/scratch-evidence/RevReadmeFrontier/README.audited.rev4.md | sha256sum
→ de5b885a793f5a773ab1dc69016ea38e185e8f77b920d2ad7b300bc7c6310ac6   # 254 L, the current bytes
```

Both carry 50 index rows over 50 notes. **On-disk hazard:** the worktree copy of `README.audited.md` is
sha `7547ccfe…` — this seat's partial 03:46 reconstruction, not the audited snapshot — because the second
sweep moved the rebuild over the relocated file. `…/scratch-evidence/RevReadmeFrontier/PROVENANCE.md`
records the mapping; cite the commit blob, never the on-disk `README.audited.md`.

**The file moved under me four times** (`7f348944…` 234 L → `a3769bef…` 246 L → `3bb9865f…` 249 L →
`de5b885a…` 254 L), by an unnamed seat that owns `corpus/README.md`. Peer `L1Mado35.RevIndex` is read-only on
the lane and did not edit it; this seat's first IRC note wrongly attributed the edits there and the report
carries the correction.

## Verdict

At the revision under attack (`3bb9865f…`) the frontier **did** deny the round's own measurement and carry a
withdrawn inference. At the current revision (`de5b885a…`, verified after peer `L1Mado35.RevIndex` reported the
same digest) the owner repaired four and **five remain open**:

| Finding | Claim | Status at `de5b885a…` |
|---|---|---|
| F1 `L101–103` | "No new consumer or transition measurement is claimed" | **REPAIRED** — `L103–105` now says "*here*", names the round-35 route and keeps only the transition half open |
| F2 `L241` | "leaving no state behind" | **REPAIRED** — `L243–246` now "no on-disk state behind (the toggle writes no file; its state is the daemon's process …; a `notify-send` may survive)" |
| F3 `L82` | surface route omits the round | **OPEN** (unchanged) |
| F4 `L246` | "hyprlock's own config" listed as open | **OPEN** at `L251` |
| F5 `L13` | daemon-absence row without a supersession pointer | **OPEN** (unchanged) |
| F6 `L60` | transient-scope INF stated as receipt content | **OPEN** (unchanged) |
| F7 `L242` | over-read quoted, carrier unnamed | **REPAIRED** — now "the package's round-12 framing" |
| F8 `L243` | "two inferences" undercount | **REPAIRED** — now "three inferences … and all are withdrawn" |
| F9 `L236` | heading names only the offer | **OPEN** at `L238` |

The index table is **complete and clean at both revisions**: three rows at `L59–61`, `50/50`, row fidelity
`0 errors`, `rc=0` on each.

**Tally:** of the original seven non-retracted findings, two prose defects and two wording defects are fixed;
F3 (route), F4 (r17 contradiction), F5 (pointer) and F6 (evidence class) stay open, plus the heading nit F9.
**F7's original premise is retracted** — it was this seat's error, see the retraction under F7. None of this
moves the index verdict.

## Revision-4 re-audit (current bytes)

Full diff of the owner's edit against the audited snapshot. The snapshot is reproducible from the checkpoint
commit, so this command survives any further scratch churn (first run used the on-disk copy before the
relocation: `diff .ufo/waves/round-35/scratch/RevReadmeFrontier/README.audited.md corpus/README.md`):

```
$ diff <(git cat-file -p 4efaf63:.ufo/waves/round-35/scratch-evidence/RevReadmeFrontier/README.audited.md) corpus/README.md
59c59   … recheck on-request → on-change
61c61   … recheck "on-change (S209, S210: 90d)" → "on-change (S210: 90d)"
103c103,105  "+ consumer or transition measurement is claimed *here*; round 35 moved the
              + consumer half onto measured ground (see the round-35 route below), and the
              + transition half stays open."
241,245c243,250  "leaving no state behind" → "leaving no on-disk state behind (… its state is the
                 daemon's process, re-armed at login from `autostart.conf`; a `notify-send` may
                 survive in notification history)"; "the earlier" → "the package's round-12 framing";
                 "two inferences" → "three inferences … and all are withdrawn", with
                 '"built not to remember" is replaced by the process-shaped mechanism'
exit=1   # expected: the files differ
```

Gates re-run on those bytes:

```
$ python3 -I quality/check-index.py --root /tmp/rr35-mirror
MADO_INDEX: root=/tmp/rr35-mirror indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0
# first run: --root …/scratch/RevReadmeFrontier/mirror4, same verdict, before the relocation
$ python3 -I quality/check-index-rows.py --root /home/vgpnk/Projects/shokunin/mado-shokunin
MADO_INDEX_ROWS: root=… rows=50 errors=0 warns=0
exit=0
```

What is still wrong, with current line numbers:

1. **`L82`** (F3) — the Screen/idle/lock route still lists only `idle-lock-plane` §§2–5, §§7–11 and
   `config-health-report-r3` F1. A reader entering by surface still cannot reach r12/r14/r15 or the round-35
   route at `L238`. **Fix:** link the three notes and the section.
2. **`L251`** (F4) — `Still open: … hyprlock's own config, …` still contradicts `L42` and
   `idle-lock-route-r17.md:72-73,95–105`; the open item is parse assurance (`idle-lock-plane.md:335–337`).
3. **`L13`** (F5) — `idle/lock: hypridle \`inactive\` + no PID (§8 unknowns kept unknown);` still carries the
   2026-10-14 absence with no pointer to r14's pid-1667 measurement, while `L6–8` tells the reader that
   inherited unknowns govern.
4. **`L60`** (F6) — `… the unit probe reads \`inactive\` only because the daemon runs inside a transient
   scope.` remains an unclassed INF that S205 does not carry (`grep -c "systemd-run\|uwsm\|scope"` on the
   receipt = **0**, exit 1); r14 errata E2 says "materially true but unlicensed by S205".
5. **`L238`** (F9) — `### Round-35 idle-lock offer route` still names only the offer while the section carries
   the setup-path negative, the daemon measurement and the withdrawal register.

Also checked in revision 4 and **not** a defect: the row-61 recheck narrowed from "(S209, S210: 90d)" to
"(S210: 90d)", which is faithful to `SOURCES.md` (S209 recheck = `on-change`, S210 recheck = `90d`, parsed from
the registry row tails). The observation that S209's gate-quote embeds a copy count (`four dated copies`) while
sitting on `on-change` is a registry cadence question, outside this row's text and outside this seat's scope.

## Assigned commands and gate results (quoted with exit codes)

```
# working tree copied outside the lane (the in-lane scratch mirrors were relocated away), then
$ rsync -a --exclude=.git --exclude=.ufo ./ /tmp/rr35-mirror/ && sha256sum /tmp/rr35-mirror/corpus/README.md
de5b885a793f5a773ab1dc69016ea38e185e8f77b920d2ad7b300bc7c6310ac6  /tmp/rr35-mirror/corpus/README.md
$ python3 -I quality/check-index.py --root /tmp/rr35-mirror
MADO_INDEX: root=/tmp/rr35-mirror indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
exit=0

# the same verdict was first obtained on scratch/RevReadmeFrontier/mirror2, again on …/mirror4, and a third
# time on /tmp after the relocation; all three ran on byte-identical corpus bytes. The first two mirrors
# were lost with the scratch move (see "Evidence artifacts (post-relocation)").

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

## Findings at `3bb9865f…` (audited record)

Statuses below are the `3bb9865f…` state; the table in "Verdict" and the "Revision-4 re-audit" section carry
the current status and current line numbers for each.

### F1 — HIGH — `L101–103`: the frontier still says the consumer measurement does not exist *(REPAIRED at `de5b885a`)*

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

### F2 — HIGH — `L241`: "leaving no state behind" is the withdrawn form of the claim *(REPAIRED at `de5b885a`)*

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
- **The file is a live edit target.** Four hash changes during this run (`7f348944` → `a3769bef` → `3bb9865f`
  → `de5b885a`). If the owner edits again, F1–F9's pinned line numbers shift; re-resolve against
  `de5b885a…`/`README.audited.rev4.md` or the earlier frozen copy.
- **F7 retraction, and its blast radius.** The first version of F7 printed a two-line summary as if it were
  the output of the quoted `grep`; the command in fact returns r15 `:32`, r12 `:36` and `SOURCES.md:206` as
  well. No other finding rested on it, and the corrected block above now reproduces the real output. Peer
  `L1Mado35.RevIndex` caught it; its anchors for F1/F2/F4 were re-checked here against the same bytes
  (r14 `:15–17` / `:36–37`, r15 `:78–84` / `:87–93` / `:100–102`, r17 `:72–73` / `:95–105`) and all hold.
- **I did not re-measure the host's live idle state** (no `pgrep hypridle` of my own): the process facts are
  taken from S205's receipt and the landed `RevQuoteS205`/`RevQuoteS204` reports. My own host reads were the
  two script bodies and the receipts' bytes.
- **Notification history was not read** (r15 E5 leaves it open); nothing in this report depends on it.
- **Scratch relocation, and why this report inlines its evidence.** `scratch/` was moved, not deleted, to
  `scratch-evidence/` (59 seat dirs, checkpoint `4efaf63`); a second sweep then moved this seat's 03:46 rebuild
  over its own relocated dir. Peer `RevEntryR15` warns the checkpoint can carry *older* segments for seats that
  rewrote files before 03:43; for this seat both snapshot blobs were hash-verified against digests the audit had
  already quoted (`3bb9865f…`, `de5b885a…`), so they are exact, not stale. The on-disk `README.audited.md` is
  `7547ccfe…` and is **not** the audited snapshot (see `PROVENANCE.md`). Nothing in F1–F9 reads from scratch:
  every audited sentence is quoted with its line number and every command with its exit code.
- **C2 was not run** by this seat; the README quotes only C1, and the C1 run above is context, not a verdict
  on the notes' truth.

## Evidence artifacts (post-relocation)

The `scratch/` tree was **moved** to `scratch-evidence/` at 03:43–03:45 (59 seat dirs; checkpointed in commit
`4efaf63`) and a second sweep then removed re-created `scratch/` dirs at 03:46, moving this seat's rebuild over
its own relocated directory. Current state of this seat's evidence:

| artifact | where | status |
|---|---|---|
| audited snapshot, 249 L, `3bb9865f…` | `git cat-file -p 4efaf63:.ufo/waves/round-35/scratch-evidence/RevReadmeFrontier/README.audited.md` | **canonical** — exact bytes |
| current snapshot, 254 L, `de5b885a…` | same commit, `…/README.audited.rev4.md`; also on disk at `scratch-evidence/RevReadmeFrontier/README.audited.rev4.md` | **canonical** — exact bytes, verified on disk |
| on-disk `…/README.audited.md`, `7547ccfe…` | `scratch-evidence/RevReadmeFrontier/` | **not evidence** — partial reconstruction, left as HEAD has it so the tree stays clean |
| three mirrors (`7f348944…`, `3bb9865f…`, `de5b885a…`) | gone with the relocation | verdict re-run on `/tmp/rr35-mirror` (`de5b885a…`, `50/50`, exit 0) |
| provenance map | `scratch-evidence/RevReadmeFrontier/PROVENANCE.md` | read this before citing any file above |

`scratch/` is not a stable store this round: 12+ seat dirs were re-created at 03:46 and at least one was deleted
again. **This report is the durable locus** — every finding quotes the audited sentence with its line number,
and every command is quoted with its exit code, so nothing depends on a surviving scratch file.
