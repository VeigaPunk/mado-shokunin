# SimplifyRows — YAGNI attack on the eight round-35 rows (S203–S210)

Seat: `L1Mado35.SimplifyRows`. Read-only attack; every write is under
`.ufo/waves/round-35/scratch/SimplifyRows/` plus this report.

## Verdict

**No deletion is admissible, and none is proposed.** The frozen predicate pins the
deletion question shut: `PRED-C1-r35-v1` requires `closed_rows=8`, and the frozen
spec admits exactly eight sids. Deleting any row costs one closed row and one open
cite, in every variant I could build — including deleting the row *and* its
gate-quote *and* its `source:` line, and including deleting the sid from a copy of
the frozen citation set (experiments below). So the YAGNI axis cannot be walked by
removing rows this round.

What the attack did find is where the weight actually is: **three of the eight rows
name no document at all** (S204, S209, S210 — pure fetch transcripts), and **two of
those three cite a witness that cannot witness the proposition it is filed for**
(S204, S210). Those are row-level defects that a deletion cannot fix and that the
counter cannot see.

## Axes (named before touching anything)

| axis | test | instrument |
|---|---|---|
| distinct document | does the row's `source` tail resolve to a regular file outside the fetch tree? | `scratch/SimplifyRows/source_audit.py` (exit 0) |
| distinct proposition | does the entry cite this sid for a sentence no sibling row supports? | the three admitted entries, read in full |
| tier fit | is tier A justified *for the row's scope*, per `CORPUS.md:93-97` ("tier — scoped to `scope`, never global")? | contract text + host bytes |
| anchor support | does the receipt carry the tokens the anchor attributes to it? | receipts re-read against host files |
| frozen-target compatibility | can the redundancy be removed and C1 still print TARGET_MET? | `scratch/SimplifyRows/harness.py` against the unmodified counter |

## Row table

`doc` = source is a document a reader can open; `tr` = source is this round's own
fetch transcript. "Anchor supported" is judged against the cited receipt only.

| id | source class | distinct proposition in the entry | tier A for the row's scope? | anchor supported by receipt? | YAGNI verdict |
|---|---|---|---|---|---|
| S203 | doc `bin/omarchy-first-run` | the setup path's 12-script list contains no idle question (r12 §1) | yes for the file list; **no** for "whether an intent could have been recorded" | partly — "questionnaire" and the record clause are not in the receipt (F3) | keep; source, scope and anchor each over-claim (F3) |
| S204 | **tr** `fetch/S204.receipt.txt` | the journal holds zero `omarchy-toggle` invocations (r12 §2) | **no** — non-diagnostic instrument, past window (F2) | the count is literal, the inference is not | **weakest row**: null instrument, duplicated measurement |
| S205 | **tr** (anchor names `hypridle.conf`) | the daemon is live and the chain declared (r14 §1-§2) | yes for liveness/timeouts; the causal clause needs a probe the receipt lacks (F4) | process, conf digest, timeouts, journal lines: yes; "transient scope": **no** | keep; anchor one clause short |
| S206 | doc `~/.config/waybar/config.jsonc` | the bar offers the choice via `custom/idle-indicator` (r15 §1) | yes | yes, lines 18-19 and 207-212 verified | keep |
| S207 | doc `default/waybar/indicators/idle.sh` | the desktop renders the off state itself (r15 §2) | yes | yes; scope says "two-state vocabulary" but one state is an empty string (F6) | keep; scope word too wide |
| S208 | doc `bin/omarchy-menu` | the menu is the second surface (r15 §1) | yes | yes, lines 207/212 verified | keep |
| S209 | **tr** `fetch/S209.receipt.txt` | the offer dates back at least to the oldest copy (r15 §2) | yes for "each copy carries the handler"; the date needs its field named (F5) | handler counts yes; "oldest dated 2026-10-03" is mtime, not the filename date | keep; one field ambiguity |
| S210 | **tr** `fetch/S210.receipt.txt` | no recorded entry, so the choice leaves no trace (r15 §3) | **no** — the directory cannot record the idle lock at all (F1) | the listing yes; "the place where a choice about other toggles would have left one" is **false** | **vacuous row**: witness cannot witness |

Distinctness details:

- **S204 vs S203.** S204's `source` string re-states S203's measurement ("the
  installer's script count"), and its receipt re-measures it (`count: 12`). The
  unique payload is one journal count. Not a restatement as a *claim*, but the
  duplicated count is dead weight.
- **S210 vs S204.** Two "no record" negatives over two record classes. Neither can
  distinguish "the operator chose" from "the operator never chose" (F1, F2). The
  entry's real support for "built not to remember" is `omarchy-toggle-idle`, which
  no row names.
- **S206 / S207 / S208.** Three different files, three different propositions
  (click path, rendering, menu surface). None is removable: r15's claim is about
  *two surfaces plus a display*, and each row carries one of the three.
- **S209 vs S206.** Same handler, new dimension (time). Distinct.
- **S205.** Sole row of its entry. Distinct.

## Findings

**F1 — S210's witness cannot witness (strongest hit).** The row's scope is
"whether the operator's choice about the idle lock could ever have been recorded",
and its teaches says the directory is "the place where a choice about other toggles
would have left one". On the host, that place does not exist for the idle lock:

```
$ cat /home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle
#!/bin/bash
# omarchy:summary=Toggle hypridle idle locking
if pgrep -x hypridle >/dev/null; then
  pkill -x hypridle
  notify-send -u low "󱫖    Stop locking computer when idle"
else
  uwsm-app -- hypridle >/dev/null 2>&1 &
  notify-send -u low "󱫖    Now locking computer when idle"
fi
pkill -RTMIN+9 waybar
```
`grep -n 'state\|toggle' omarchy-toggle-idle` → no match (exit 1). The only writers
to `~/.local/state/omarchy/toggles/` are the generic `omarchy-toggle`
(`FLAG="$HOME/.local/state/omarchy/toggles/$FLAG_NAME"`) and
`omarchy-toggle-touchpad` / `omarchy-toggle-touchscreen`
(`toggles/hypr/touchpad-disabled.conf`, `touchscreen-disabled.conf`). So a
`files whose text names the idle lock: 0` count was guaranteed before the command
ran: the idle toggle writes nowhere. The zero carries no information, and the
sentence the entry needs is warranted by an **uncited** document. Under YAGNI this
row is a document a reader would not need — but it cannot be deleted, and rule 2
(append-only) forbids re-pointing its source in place.

**F2 — S204 measures a string no code path emits, over a window that starts after
setup.** `omarchy-toggle-idle` contains no `echo`/`logger`/journal write (grep above;
exit 1), and the journal holds no line naming *any* omarchy bin path:

```
journalctl --user | grep -c 'omarchy-toggle'   → 0   (exit 1)
journalctl --user | grep -c 'bin/omarchy'      → 0
journalctl --user | grep -c 'omarchy-menu'     → 0
journalctl --user | grep -c 'omarchy-launch'   → 0
journalctl --user | grep -c 'pkill'            → 0
journalctl --user | grep -c 'uwsm-app'         → 2   (elephant config lines only)
journalctl --user | grep -c 'omarchy'          → 31565
```
So `grep -c 'omarchy-toggle'` returns 0 whether or not the toggle ran. Second
defect: the retained user journal starts **after** the setup it is filed against.

```
journalctl --user -o short-iso | head -1  → 2026-10-23T07:18:30-03:00
journalctl --user -o short-iso | tail -1  → 2026-10-25T03:34:39-03:00
journalctl --user --since 2026-10-01 | wc -l → 165788   (= the whole retained journal)
stat install/first-run                          → 2026-10-03 17:42
```
The row's scope says "the operator never made it afterwards either"; the instrument
covers 2026-10-23 onward. The entry is careful in §2 ("in any session the journal
still keeps"); the **row** is not. Under `CORPUS.md:93` tier A is scoped to the
`scope`, so tier A cannot be granted here: the source cannot bear on the scope.

**F3 — S203's "post-login questionnaire" is not a questionnaire.** The installer's
own summary is "Finish the installation of Omarchy with items that can only be done
after logging in". No prompt exists anywhere in the path:

```
grep -nE 'read |whiptail|gum |question' bin/omarchy-first-run   → no match (exit 1)
grep -lE 'read -[pr]|read -p|whiptail|gum ' install/first-run/*.sh | wc -l → 0
sed -n 1,40p install/first-run/welcome.sh → one notify-send line
```
The receipt shows a filename list, and a filename list cannot show that a prompt is
absent — only the script bodies can, and the receipt does not carry them. Second
overreach: the anchor line 3 is an `# omarchy:summary=` comment, not body; the body
starts at line 8. Third: the row's scope adds "and therefore whether an intent could
have been recorded at setup", but the installer touches only
`~/.local/state/omarchy/first-run.mode` (read, then `rm -f`). No record surface is
named by source or receipt.

**F4 — S205's causal clause is true but not in the receipt.** Host verification:

```
pgrep -x hypridle → 1667
cat /proc/1667/cgroup → 0::/…/app-Hyprland-hypridle-d4bd7533.scope
systemctl --user list-units --type=scope | grep hypridle → app-Hyprland-hypridle-d4bd7533.scope … active running hypridle
systemctl --user is-active hypridle → inactive
```
So "the daemon runs inside a transient scope" is correct — and `S205.receipt.txt`
contains only `process probe`, `unit probe`, `journal start lines`, `declared
timeouts`, `hypridle.conf digest`. The anchor cites receipt sections and
`hypridle.conf`; the cgroup/scope probe that settles the INF was dropped. A one-line
anchor fix (add the `/proc/1667/cgroup` or scope-listing line) closes it.

**F5 — S209's "dated" is two different timestamps.** The oldest copy's **mtime** is
2026-10-03; its **filename epoch** is 2026-10-06:

```
stat .../config.jsonc.bak.1791314470 → 2026-10-03 17:44:32
date -d @1791314470                  → Tue 06 Oct 2026 16:21:10 -03
```
The receipt's own `--- oldest dated copy ---` section prints the path
`config.jsonc.bak` (mtime 2026-10-11) and then the `stat` line of
`.1791314470` (2026-10-03) — internally inconsistent. Row S209 says "the oldest
dated 2026-10-03" without naming the field; entry r15 §5 then calls the package's
2026-10-06 "divergence" — that is a field comparison, not a correction. The row's
tier A survives for the handler counts; the date claim needs `mtime` in the cell.

**F6 — S207's "two-state vocabulary" is one label plus an empty string.** The
receipt shows `{"text": ""}` for the running state and one tooltip
`Idle lock disabled` for the other. The entry states this exactly; the row's scope
does not.

**F7 — the S203 receipt prints 13 names under a `12` count.** The 13th is
`install-voxtype.hook`; the count is right for `.sh` files and for `bash`
invocations (12), but a reader counting the printed list gets 13. `ls
install/first-run | wc -l` → 13; `ls install/first-run/*.sh | wc -l` → 12. The
rows' "twelve first-run scripts" is correct under the `.sh` reading; the anchor
should say so. (S204's receipt prints only `count: 12`, no names.)

**F8 — S210's "entries for other toggles" is one toggle.** The directory holds
`flags.conf` and `window-no-gaps.conf`; `flags.conf` is a flags file, not a toggle
record. Teaches' plural is generous.

## Deletion proofs (scratch, unmodified counter)

Harness: `scratch/SimplifyRows/harness.py` builds a root containing only what C1
reads (`corpus/` + `.ufo/waves/round-35/fetch/`), applies one mutation, then runs the
lane's counter with `python3 -I`. Command shape:

```
python3 -I harness.py <experiment>
  → python3 -I <lane>/.ufo/waves/round-35/c1/count.py \
      --root <scratch>/exp/<experiment>/root --frozen <frozen>
```

| experiment | mutation | exit | counter output | verdict |
|---|---|---|---|---|
| e0-base | none | 0 | `closed_entries=3 closed_rows=8 open_cites=0 TARGET_MET` | control: the scratch mirror reproduces MET |
| e1-drop-s204 | drop S204 row | 1 | `closed_entries=2 closed_rows=7 open_cites=1 TARGET_MISSED` | no |
| e2-drop-s210 | drop S210 row | 1 | `2/7/1 MISSED` | no |
| e3-drop-s203 | drop S203 row | 1 | `2/7/1 MISSED` | no |
| e4-drop-s204-and-quote | drop S204 row + its gate-quote | 1 | `2/7/1 MISSED` | no |
| e5-drop-s204-s210-full | drop S204+S210 rows, quotes and `source:` lines | 1 | `1/6/2 MISSED` | no |
| e6-drop-sid-from-frozen | drop S204 from a frozen copy **and** the row | 1 | `3/7/0 MISSED` | the target is a constant 8; a 7-sid spec cannot reach it |
| e7-substitute-source | S204 source → `omarchy-toggle-idle`, receipt digest kept | 0 | `3/8/0 MET` | predicate is blind to source distinctness |
| e8-anchor-lie | S206 anchor → `lines 999-1000 … file sha256 deadbeef`, receipt digest kept | 0 | `3/8/0 MET` | predicate is blind to anchor content beyond the receipt digest |
| e9-teaches-lie | S210 teaches → "The idle lock has a recorded entry" | 0 | `3/8/0 MET` | predicate does not score teaches |
| e11-s210-source-rewrite | S210 source → `omarchy-toggle-idle` in place | 0 | `3/8/0 MET` | passes C1, but `CORPUS.md` rule 2 forbids editing `source` in place |
| e12-s204-rescope | S204 scope → "within its retained window (2026-10-23T07:18 …)" | 0 | `3/8/0 MET` | cell correction is C1-neutral |
| e13-supersede-append | append well-formed `S211` (`supersedes S210 — …`), S210 untouched | 0 | `3/8/0 MET`; census `malformed=0` | the only rule-2-compliant instrument |
| e14-supersede-and-uncite | S211 appended **and** S210's `source:` + gate-quote dropped | 1 | `2/7/1 MISSED` | no retirement path exists |

Baseline on the untouched lane, same commands:

```
python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json
→ exit 0  PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json
→ exit 0  PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
```

C2 is unaffected by any row edit by construction: it reads the clause ledger, control
receipts and the frozen-blob ledger only (`c2/count.py`), never `corpus/SOURCES.md`.

## Proposals (no deletions; for round 36, when the target is not frozen)

1. **Re-target the row count to distinct documents.** `closed_rows=8` currently
   equals `len(frozen sids)`, so the predicate is a bijection over sids and every row
   is load-bearing by arithmetic. A round-36 row test of the form *"a row is closed
   only when it names a document (source path or verified digest) outside the fetch
   tree"* makes redundancy measurable. Working checker:
   `scratch/SimplifyRows/propose_strict.py` (adds source-document, file-digest and
   line-span checks to C1's row test). On the lane it prints
   `document_anchored_rows=5/8`, exit 1 —

   ```
   S203 PASS   S204 FAIL (no document)   S205 PASS (hypridle.conf digest)
   S206 PASS   S207 PASS   S208 PASS
   S209 FAIL (no document)   S210 FAIL (no document)
   ```
   The four document-source rows' digests and line spans all verify against live
   bytes, as does S205's `hypridle.conf` digest (`sha256sum` matches; 28/260/7/891/19
   lines cover anchors 3/207/3/207/10).
2. **Supersede S210** with a row whose document is
   `/home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle`: the no-record property
   is in that script, not in the directory listing. Keep the toggles-directory
   receipt as the digest only.
3. **Supersede S204** with a row that names the query **and its window**
   (`journalctl --user --since 2026-10-23T07:18:30 | grep -c omarchy-toggle`) and
   states the result as a null ("no matching line in the retained window; the toggle
   emits no journal line, so the null is not evidence of non-use"). Tier A then fits
   the narrower scope or is honestly dropped to B.
4. **Correct S203's** `source`/`scope`: "post-login finisher", drop "intent could have
   been recorded", anchor line 8-27 only. **S209:** name the field (`mtime`) and the
   four `.bak` paths, so r15 §5's "divergence" can be withdrawn. **S205:** add the
   `/proc/1667/cgroup` (or scope-listing) line to the anchor. **S207:** scope says
   one label, not "two-state vocabulary".
5. Do none of these by editing the rows in place: rule 2 permits only
   `status`/`recheck`/`used-by`, and a correction must be a new row opening
   `supersedes S0NN —`. e13 proves an appended correction row leaves C1 at MET; e14
   proves retiring the old row cannot.

## Preserved contract

- Lane tree untouched: I read only. Lane digests at close (for the next seat to
  compare): `corpus/SOURCES.md` `848a7680…e78d4fe80`, r12 entry
  `7f27ced0…e4dd58`, r14 entry `583c708c…e0bf3`, r15 entry `82c08a46…f91fadfe`.
- Census on the lane: `rows=200 malformed=0 dups=(none) tier A=193 B=1 C=6`.
  S203–S210 are 8 of the 200; four of those eight name a fetch transcript as their
  source (S204, S205, S209, S210), and three of those four (S204, S209, S210) name
  no document anywhere in the row.
- C1 and C2 both exit 0 TARGET_MET before and after this attack; every mutation was
  applied to a copy under `scratch/SimplifyRows/exp/`.
- No tool installed or upgraded (nothing was needed); no pacman transaction; nothing
  written under `/home/vgpnk/Projects/shokuknow`.

## Tradeoff

Making the row count document-based would drop the scored set to 5 closed rows today
and would need the three transcript-only rows (S204, S209, S210) replaced before the
target could be met again — a real cost in a round whose job is to prove C1, not to
grow it. The alternative (keep the sid-based target) keeps C1 green and keeps two
rows whose evidence cannot move the needle (S204, S210) inside the scored set. I
recommend the first only in a round that is allowed to re-target, and the cell
corrections in `S203/S205/S207/S209` regardless: they are C1-neutral (e12) and fix
statements that are currently stronger than their receipts.

## Not verified

- Whether the operator ever toggled the idle lock. Unobservable from these sources:
  the toggle emits nothing, and the journal begins after setup. I ran no toggle.
- Whether S209's four `config.jsonc.bak*` copies are the complete backup set; I
  re-`stat`ed only those four files.
- C2's clause ledger content beyond running its counter.
- The four superseding rows proposed above are sketched, not built; only the
  mechanical shape was tested (e13/e11).
