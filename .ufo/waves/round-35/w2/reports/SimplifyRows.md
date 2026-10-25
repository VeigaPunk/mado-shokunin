# SimplifyRows — YAGNI attack on the eight round-35 rows (S203–S210)

Seat: `L1Mado35.SimplifyRows`. Read-only attack; every write was under
`.ufo/waves/round-35/scratch/SimplifyRows/` — relocated by an external mover to
`.ufo/waves/round-35/scratch-evidence/SimplifyRows/` mid-task — plus this report,
which is the durable artifact.

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

## Concurrent edits during this attack (adaptation)

This lane was being written by sibling wave-2 seats while I read it. Observed with
`stat`/`diff` against the then-live scratch mirror of my starting snapshot (the
prefix is now relocated to `scratch-evidence/SimplifyRows/`):

| when (host) | what changed | by whom |
|---|---|---|
| 2026-10-25 03:35:30 | `corpus/knowledge/idle-lock-chain-armed-r14.md` and `idle-lock-offered-in-the-bar-r15.md` grew `### Errata (round 35, wave 2)` sections | sibling seats (r14 E1 names `RevQuoteS205`, r15 E1 `RevQuoteS209`, r12 E1/E2 `RevQuoteS204`) |
| 2026-10-25 03:40:12 | `corpus/SOURCES.md`: exactly three rows rewritten — S203, S204, S205 (6 diff lines, no other row touched) | sibling seat |
| 2026-10-25 03:41:38 | `corpus/knowledge/idle-lock-never-asked-r12.md` grew errata E1-E3 | sibling seat |

Consequence for this report: **the entries now carry most of the semantic
corrections; the rows mostly do not.** r12 E1 withdraws "never toggled" (null
channel + a `Consumed`-scope window that shows a daemon-down period), E2 fixes the
13-vs-12 item count, E3 withdraws "two independent negatives" and "built not to
remember"; r14 E1 says the transient-scope inference is "unlicensed by S205" and
names the uwsm scope line, E2 withdraws "both fire the lock command"; r15 E1
explains the dating clock, E2 withdraws "never taken it", E3 supplies the
`omarchy-toggle-idle` mechanism, E4 says one state is named and the other is
silence, E5 narrows "leaves no trace" to on-disk state. The S203/S204/S205 row
edits absorbed only the count, the null-channel label and the boot count. They did
not land consistently: S203's teaches now says "thirteen items, twelve of them
first-run scripts" while S204's still says "(12 first-run scripts, none about idle)";
S204's teaches still opens "Two independent negatives agree" and ends "which is a null
channel rather than a negative".

Re-verified after the edits, on the current bytes: C1 and C2 still exit 0
TARGET_MET; `e0-base`/`e1-drop-s204`/`e2-drop-s210` rebuild from the current tree and
give the same `MET` / `7 closed, 1 open` / `7 closed, 1 open`; `source_audit.py` and
`propose_strict.py` still report 5/8 document-anchored. The deletion proof is
structural and does not depend on cell text: the target is `closed_rows=8` and the
spec admits eight sids.

I verified the errata's central new fact (read-only):
`journalctl --user | grep 'app-Hyprland-hypridle-9408787a'` → two lines, the
`Consumed … 19:24:38` line and the 13:25:00 uwsm `systemd-run --scope --unit=…`
line; `coredumpctl list hypridle` → `No coredumps found.`;
`default/hypr/autostart.conf:1` → `exec-once = uwsm-app -- hypridle`;
`toggles/hypr/flags.conf` → the two-line placeholder text. So the journal *does*
record the daemon's lifecycle. That makes S204's new scope ("the daemon's
stop/start is consistent with a toggle-off") true on the host — and still absent
from S204's own anchor (F2).

## Artifact relocation and what is durable (03:43–03:47)

The lane moved its scratch tree while this report was being written:
`.ufo/waves/round-35/scratch/<Seat>/` became
`.ufo/waves/round-35/scratch-evidence/<Seat>/` (an external mover, ~03:43–03:45;
sibling seats report byte-intact arrivals). `scratch/` is not stable — a second sweep
re-created and deleted seat directories at ~03:46, and my own re-created directory was
moved out again.

What survived for this seat, and what did not:

| artifact | where | status |
|---|---|---|
| `harness.py` (8068 B, `2c5cf6ee…cacd8`) | `scratch-evidence/SimplifyRows/` | **rebuild**, 03:46, not the bytes measured at 03:2x |
| `source_audit.py` (1879 B, `24fb92e8…7aa8b8ea`) | `scratch-evidence/SimplifyRows/` | **rebuild**, 03:46 |
| `propose_strict.py` (4811 B, `f3d4f142…8e9249`) | `scratch-evidence/SimplifyRows/` | **rebuild**, 03:46 |
| `exp/` mirrors (incl. the pre-edit `SOURCES.md` snapshot) | — | **lost**; no `exp/` in the relocated dir |
| `simplifyrows_repro.py` (3291 B, `c139251d…98ed06`) | `scratch-evidence/SimplifyRows/` | moved there ~03:48, byte-identical to Appendix A (diffed); the appendix is the durable copy |

A rebuild is not evidence, so this report does not lean on those files. The
load-bearing proof — the deletion impossibility and the transcript-only audit — is
**inlined as Appendix A** and was re-run at 03:48 against the current lane bytes:

```
[baseline] exit=0 PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
[drop S204] exit=1 PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED
[audit] transcript-only rows: S204 S209 S210
REPRO PASS
```

The pre-edit `SOURCES.md` snapshot (sha256 `848a7680…`) was diffed at 03:40 — 6 lines
over S203/S204/S205 — but it did not survive the relocation; the diff result stands as
recorded, the baseline bytes do not.

## Axes (named before touching anything)

| axis | test | instrument |
|---|---|---|
| distinct document | does the row's `source` tail resolve to a regular file outside the fetch tree? | `source_audit.py` (relocated; its logic is inlined in Appendix A) — exit 0 |
| distinct proposition | does the entry cite this sid for a sentence no sibling row supports? | the three admitted entries, read in full |
| tier fit | is tier A justified *for the row's scope*, per `CORPUS.md:93-97` ("tier — scoped to `scope`, never global")? | contract text + host bytes |
| anchor support | does the receipt carry the tokens the anchor attributes to it? | receipts re-read against host files |
| frozen-target compatibility | can the redundancy be removed and C1 still print TARGET_MET? | `harness.py` (relocated) against the unmodified counter; Appendix A reproduces the decisive case |

## Row table

`doc` = source is a document a reader can open; `tr` = source is this round's own
fetch transcript. "Anchor supported" is judged against the cited receipt only.

| id | source class | distinct proposition in the entry | tier A for the row's scope? | anchor supported by receipt? | YAGNI verdict |
|---|---|---|---|---|---|
| S203 | doc `bin/omarchy-first-run` | the setup path's item list contains no idle question (r12 §1) | yes for the item list; **no** for "whether an intent could have been recorded" | partly — the current teaches says "thirteen items, twelve of them first-run scripts"; "questionnaire" and the record clause are still not in the receipt (F3) | keep; source and scope over-claim; r12 E2 fixed the count |
| S204 | **tr** `fetch/S204.receipt.txt` | the journal holds zero `omarchy-toggle` invocations — now labelled a null channel (r12 §2) | **no** — the row's own teaches calls its payload "a null channel rather than a negative" | count yes; the new scope clause "the daemon's stop/start is consistent with a toggle-off" is not in the receipt | **weakest row**: self-refuting instrument; teaches still says "two independent negatives agree" |
| S205 | **tr** (anchor names `hypridle.conf`) | the daemon is live and the chain declared (r14 §1-§2) | yes for liveness/timeouts; the causal clause needs a probe the receipt lacks (F4) | process, conf digest, timeouts, journal lines: yes; "transient scope": **no**, and r14 E1 says so | keep; anchor one clause short (row now says one start line in the boot) |
| S206 | doc `~/.config/waybar/config.jsonc` | the bar offers the choice via `custom/idle-indicator` (r15 §1) | yes | yes, lines 18-19 and 207-212 verified | keep |
| S207 | doc `default/waybar/indicators/idle.sh` | the desktop renders the off state itself (r15 §2) | yes | yes; scope says "two-state vocabulary" but one state is an empty string (F6) | keep; scope word too wide |
| S208 | doc `bin/omarchy-menu` | the menu is the second surface (r15 §1) | yes | yes, lines 207/212 verified | keep |
| S209 | **tr** `fetch/S209.receipt.txt` | the offer dates back at least to the oldest copy (r15 §2) | yes for "each copy carries the handler"; the date needs its field named (F5) | handler counts yes; "oldest dated 2026-10-03" is mtime, not the filename date | keep; one field ambiguity |
| S210 | **tr** `fetch/S210.receipt.txt` | no recorded entry, so the choice leaves no trace (r15 §3) | **no** — the directory cannot record the idle lock at all (F1); subject also unversioned | the listing yes; "the place where a choice about other toggles would have left one" is **false**, and r15 E3 now denies it | **vacuous row**: witness cannot witness; contradicts its own entry's E3 |

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
So `grep -c 'omarchy-toggle'` returns 0 whether or not the toggle ran. That does not
mean the journal is silent about the daemon: it records the scope lifecycle, and a
sibling errata (r12 E1) is built on exactly that —

```
journalctl --user | grep 'app-Hyprland-hypridle-9408787a'
→ Oct 23 13:25:00 uwsm_app-daemon: sent: exec systemd-run --user --scope … --unit=app-Hyprland-hypridle-9408787a.scope … -- hypridle
→ Oct 23 19:24:38 systemd[1529]: app-Hyprland-hypridle-9408787a.scope: Consumed 2.783s CPU … 5h 59min 38.213s wall clock
coredumpctl list hypridle → No coredumps found.
```
So a competent probe exists (scope `Consumed` with no `Stopping`/`Stopped`, then a
new start at 22:14:11) and S204's receipt did not run it. **The defect is the chosen
statistic, not the journal's capacity** — and the row's 03:40 scope edit now asserts
that very lifecycle fact while its anchor still cites only the count and the grep.

Second defect: the retained user journal starts **after** the setup it is filed
against, so "never afterwards" outruns the window even for a competent probe.

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

**Status at 03:41.** r12 E1 now withdraws "never toggled" in the entry and r12 E3
withdraws "two independent negatives"; the row's 03:40 edit labels its payload "a
null channel rather than a negative" but keeps the sentence "Two independent
negatives agree … which is a null channel rather than a negative" — an internal
contradiction and a direct conflict with its own entry's E3. The row is now
self-refuting; it is not corrected.

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

**Status at 03:41.** r12 E2 fixes the 13-vs-12 count (F7 below is resolved in the
entry and in the row's teaches) and r12 E3 withdraws the licensing of "none asks"
on the ground that S203/S204 carry no script bodies. The row still calls the path a
"post-login questionnaire" and still claims to scope "whether an intent could have
been recorded at setup"; neither is in the receipt.

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

**Status at 03:41.** r14 E1 now says the transient-scope inference is "materially
true but **unlicensed by S205**" and names the uwsm `systemd-run --scope` line as its
warrant. The row's teaches still asserts the inference with an anchor that does not
carry it.

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

**Status at 03:41.** r15 E1 landed exactly this explanation ("the dated copy preserved
the source file's older mtime, so the creation clock and the content clock
disagree"); the row's cell is unchanged.

**F6 — S207's "two-state vocabulary" is one label plus an empty string.** The
receipt shows `{"text": ""}` for the running state and one tooltip
`Idle lock disabled` for the other. The entry states this exactly; the row's scope
does not.

**Status at 03:41.** r15 E4 landed the same sentence ("exactly one state carries
words"); the row's scope is unchanged.

**F7 — (resolved concurrently by r12 E2) the S203 receipt prints 13 names under a
`12` count.** Reached independently here; r12 E2 now records the same 13/12
distinction, the S203 and S204 row teaches cells were edited to "thirteen items,
twelve of them first-run scripts", and `ls install/first-run/*.sh | wc -l` → 12
still supports the `.sh` reading.

**F8 — S210's "entries for other toggles" is one toggle.** The directory holds
`flags.conf` and `window-no-gaps.conf`; `flags.conf` is a flags file, not a toggle
record. Teaches' plural is generous.

**Status at 03:41.** r15 E3 supplies the mechanism (`omarchy-toggle-idle` stops or
starts the process and writes no file; `autostart.conf:1` re-arms it at login) and
reads `flags.conf` as the template placeholder — both verified in the adaptation
section. The row's teaches still says the toggles directory "is the place where a
choice about other toggles would have left one", which is exactly what the entry now
denies for the idle lock.

**Status at 03:52 — the contradiction is now between two live artifacts.** `SOURCES.md`
reads no errata: cell 7 and r15 §3 are what a reader or a counter sees. E3 withdraws
exactly the clause the row still teaches, so the repair cannot live only in the
appended block; it has to land in the teaches cell (and §3). Independently, the
measured subject has no revision key to anchor: `~/.local/state/omarchy/toggles/hypr`
is outside the omarchy checkout (HEAD `8fcc9d6048af`, clean) and is ignored by the
home repo — `git check-ignore` → `.gitignore:23:/.local/*`, 0 tracked files. So S210's
anchor is section + receipt digest only; the `CORPUS.md:99` requirement of a revision
(version, commit, or publication date) for the subject is met by neither. Peer
`RevQuoteS210` reports the same contradiction; the git facts above are re-derived here.

## Deletion proofs (scratch, unmodified counter)

Harness: `harness.py` builds a root containing only what C1 reads (`corpus/` +
`.ufo/waves/round-35/fetch/`), applies one mutation, then runs the lane's counter with
`python3 -I`. The relocated copy at `scratch-evidence/SimplifyRows/harness.py` is a
03:46 rebuild (sha256 `2c5cf6ee…cacd8`); the `exp/` trees the original made did not
survive the relocation. The decisive case is reproduced by Appendix A. Command shape:

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

Baseline on the lane, re-run after the concurrent edits (03:41), same commands:

```
python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json
→ exit 0  PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json
→ exit 0  PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
```

`e0-base`, `e1-drop-s204` and `e2-drop-s210` were rebuilt from the post-edit tree and
return `MET`, `7 closed / 1 open`, `7 closed / 1 open` — the deletion result is
independent of the cell text.

C2 is unaffected by any row edit by construction: it reads the clause ledger, control
receipts and the frozen-blob ledger only (`c2/count.py`), never `corpus/SOURCES.md`.

## Proposals (no deletions; for round 36, when the target is not frozen)

1. **Re-target the row count to distinct documents.** `closed_rows=8` currently
   equals `len(frozen sids)`, so the predicate is a bijection over sids and every row
   is load-bearing by arithmetic. A round-36 row test of the form *"a row is closed
   only when it names a document (source path or verified digest) outside the fetch
   tree"* makes redundancy measurable. Working checker:
   `scratch-evidence/SimplifyRows/propose_strict.py` (03:46 rebuild, sha256
   `f3d4f142…8e9249`; adds source-document, file-digest and line-span checks to C1's
   row test; re-run after the relocation prints the same numbers). On the lane it
   prints `document_anchored_rows=5/8`, exit 1 —

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
3. **Supersede S204** with a row that names a journal probe with diagnostic power —
   the scope lifecycle, not the toggle's name — **and its window**, e.g.
   `journalctl --user --since 2026-10-23T07:18:30 | grep 'app-Hyprland-hypridle-'`
   plus `systemctl --user list-units --type=scope`. State the result as what it is
   (`Consumed … 19:24:38` with no `Stopping`/`Stopped`, next start 22:14:11 → a
   daemon-down window; a toggle-off is `[INFERENCE-STRONG]`, the surface is unknown)
   and record that `grep omarchy-toggle` is a null channel. Tier A then fits the
   narrower scope or the row is honestly dropped to B.
4. **Carry these content corrections into the superseding rows** (never in place):
   S203 "post-login finisher", drop "intent could have been recorded", anchor line
   8-27 only; S209 name the field (`mtime`) and the four `.bak` paths, so r15 §5's
   "divergence" can be withdrawn; S205 add the `/proc/1667/cgroup` (or scope-listing)
   line to the anchor; S207 scope says one label, not "two-state vocabulary".
5. Do none of these by editing the rows in place: rule 2 permits only
   `status`/`recheck`/`used-by`, and a correction must be a new row opening
   `supersedes S0NN —`. e13 proves an appended correction row leaves C1 at MET; e14
   proves retiring the old row cannot.

## Preserved contract

- This seat wrote nothing into the lane's corpus, counters, controls or entries. All
  writes were under `.ufo/waves/round-35/scratch/SimplifyRows/` — relocated by the
  external mover to `scratch-evidence/SimplifyRows/` — plus this report. The relocated
  scripts are 03:46 rebuilds, pinned by sha256 in the relocation section.
- Lane state at close (03:45:24; the lane was edited three times during this attack
  and may move again), with the concurrent-edit provenance recorded above:

  ```
  SOURCES.md                0bf117e2f472ec4f80adec17d58fe50b4fbd4fa9568ffa8523a4bfc272950d51  2026-10-25 03:40:12
  idle-lock-never-asked-r12 0bcef21fc93fe32f5f926b21d4f6f9655ffb32bd41f49280b0c074fb4469c504  2026-10-25 03:41:38
  idle-lock-chain-armed-r14 583c708c338ecb063f8ef38071d415c79476088f27994551fd964384be1e0bf3  2026-10-25 03:35:30
  idle-lock-offered-in-bar  82c08a4675863f69e0905b02810cae6299cdfe3038fb1255172f7b44f91fadfe  2026-10-25 03:35:30
  ```
  The three fetch receipts and the other five rows were not touched by the siblings
  (receipts still hash to the frozen digests: C1 closes them).
- My analysis started on `SOURCES.md` sha256 `848a7680…`. I diffed the live mirror
  against that snapshot at 03:40: 6 lines over S203/S204/S205 only. Both the snapshot
  and the mirror were lost in the relocation; the diff result is what stands, not the
  baseline bytes.
- Census on the lane: `rows=200 malformed=0 dups=(none) tier A=193 B=1 C=6`.
  S203–S210 are 8 of the 200; four of those eight name a fetch transcript as their
  source (S204, S205, S209, S210), and three of those four (S204, S209, S210) name
  no document anywhere in the row.
- C1 and C2 both exit 0 TARGET_MET at open (pre-edit), mid-attack and at close
  (post-edit); every mutation was applied to a throwaway mirror. The `exp/` trees did
  not survive the relocation, so Appendix A regenerates the two decisive cases in a
  `tempfile` and leaves the lane untouched.
- No tool installed or upgraded (nothing was needed); no pacman transaction; nothing
  written under `/home/vgpnk/Projects/shokuknow`.

## Tradeoff

Making the row count document-based would drop the scored set to 5 closed rows today
and would need the three transcript-only rows (S204, S209, S210) replaced before the
target could be met again — a real cost in a round whose job is to prove C1, not to
grow it. The alternative (keep the sid-based target) keeps C1 green and keeps two
rows whose evidence cannot move the needle (S204, S210) inside the scored set. I
recommend the first only in a round that is allowed to re-target, and the content
corrections (carried by superseding rows) for `S203/S205/S207/S209` regardless: they
are C1-neutral (e12) and fix statements that are currently stronger than their
receipts.

The concurrent edits add a second cost that this round cannot pay down. The entries
now carry errata that withdraw four claims (S204's negative, "two independent
negatives", "built not to remember", S205's "both fire the lock"), while the rows
keep text that asserts them: S204's teaches still opens "Two independent negatives
agree" and then calls its payload a null channel; S210's teaches still names the
toggles directory as the place the idle choice would have left a mark; S205's teaches
still asserts the transient scope its own entry now calls unlicensed; S207's scope
still says "two-state vocabulary". So the registry is now a stale second authority
for the same claims. YAGNI would retire those rows; the frozen target forbids it
(e14), and rule 2 forbids rewriting them in place (e11/e12 pass C1 but are contract
violations). The only compliant move is to append superseding rows (e13) — which
raises weight while leaving the stale rows scored. Note what makes this worse than
duplication: **`SOURCES.md` reads no errata**. A reader or a counter sees cell 7 and
the entry body, never the appended correction, so an errata-only repair cannot fix a
scored row — the repair has to land in the teaches cell (and in the section it
supports), which rule 2 forbids doing in place. I recommend the superseding rows *and*
a round-36 target that scores document-anchored rows, so the stale text stops being
load-bearing instead of being contradicted in place.

## Not verified

- Whether the operator ever toggled the idle lock. What I verified is narrower: the
  journal's scope `app-Hyprland-hypridle-9408787a` line exists with a `Consumed`
  timestamp and a later start, and there is no hypridle coredump. That is consistent
  with a toggle-off; who did it and by which surface is not established here.
- The errata written by sibling seats beyond the four facts I re-read in the
  adaptation section: r12 E1's earlyoom/memory figures, r14 E2's screensaver-script
  scan, r15 E3's byte-identity of `flags.conf` to the template file, and r15 E5's
  notification-history caveat. I read the placeholder text and `autostart.conf:1`, not
  those arguments in full.
- Whether S209's four `config.jsonc.bak*` copies are the complete backup set; I
  re-`stat`ed only those four files.
- C2's clause ledger content beyond running its counter.
- The four superseding rows proposed above are sketched, not built; only the
  mechanical shape was tested (e13/e11).

## Appendix A — self-contained reproducer

Durable copy of the load-bearing proof (the original `harness.py`/`exp/` trees were
lost in the scratch relocation). Drop this in any file, run it **from the lane root**
with `python3 -I`, and it prints the C1 baseline, the deletion proof and the
source-class audit. It writes only under a `tempfile` and leaves the lane untouched.
Reference copy: `scratch-evidence/SimplifyRows/simplifyrows_repro.py` (3291 B, sha256
`c139251dd8e38697c9b87b3585e89620ef4545edae39f5e237e2e6802098ed06`, byte-identical to
the block below — the extracted block was diffed against it). Because `scratch*` has
been moved twice during this task, treat the block as the durable copy. Verified output
(extracted to `/tmp/appendix_repro.py`, run from the lane root, exit 0) follows the code.

```python
#!/usr/bin/env python3
"""Standalone reproducer for the SimplifyRows findings (round 35, wave 2).

Run from the lane root:   python3 -I simplifyrows_repro.py
Prints: (1) the frozen C1 baseline, (2) a deletion proof, (3) a source-class
audit of the eight scored rows. Exit 0 iff every expectation holds.
Writes only under a tempdir; the lane is read-only.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path.cwd()
C1 = LANE / ".ufo/waves/round-35/c1/count.py"
FROZEN = LANE / ".ufo/waves/round-35/c1/frozen.json"
SRC = "corpus/SOURCES.md"
ROW = re.compile(r"^ {0,3}\|\s*(S[0-9]+)\s*\|")
DIGEST = re.compile(r"([\w./-]+) sha256 ([0-9a-f]{64})")


def cells(line: str) -> list[str]:
    parts = line.split("|")
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def run(root: Path) -> tuple[str, int]:
    proc = subprocess.run(
        [sys.executable, "-I", str(C1), "--root", str(root), "--frozen", str(FROZEN)],
        capture_output=True, text=True,
    )
    return (proc.stdout.strip() + proc.stderr.strip()).strip(), proc.returncode


def main() -> int:
    ok = True

    out, rc = run(LANE)
    print(f"[baseline] exit={rc} {out}")
    ok &= rc == 0 and "closed_rows=8" in out and "TARGET_MET" in out

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        shutil.copytree(LANE / "corpus", root / "corpus")
        shutil.copytree(LANE / ".ufo/waves/round-35/fetch", root / ".ufo/waves/round-35/fetch")
        p = root / SRC
        lines = p.read_text().splitlines(keepends=True)
        p.write_text("".join(l for l in lines if not l.lstrip().startswith("| S204 |")))
        out2, rc2 = run(root)
        print(f"[drop S204] exit={rc2} {out2}")
        ok &= rc2 == 1 and "closed_rows=7" in out2 and "open_cites=1" in out2

    rows: dict[str, list[str]] = {}
    for line in (LANE / SRC).read_text().splitlines():
        m = ROW.match(line)
        if m:
            rows.setdefault(m.group(1), []).append(cells(line))
    sids = [sid for ids in json.loads(FROZEN.read_text())["entries"].values() for sid in ids]
    transcript_only = []
    for sid in sids:
        cs = rows[sid][0]
        src, anchor = cs[1], cs[5]
        tail = src.rsplit(" - ", 1)[-1].strip()
        is_transcript = "/fetch/" in tail and tail.endswith(".receipt.txt")
        doc_digest = [
            n for n, _ in DIGEST.findall(anchor)
            if not n.endswith(".receipt.txt") and n != "receipt"
        ]
        doc_source = (not is_transcript) and (
            Path(tail).is_file() if tail.startswith("/") else (LANE / tail).is_file()
        )
        if not (doc_source or doc_digest):
            transcript_only.append(sid)
        print(
            f"[audit] {sid} source={'transcript' if is_transcript else 'document'} "
            f"document_digest={int(bool(doc_digest))}"
        )
    print(f"[audit] transcript-only rows: {' '.join(transcript_only)}")
    ok &= transcript_only == ["S204", "S209", "S210"]

    print("REPRO", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

Verified output (exit 0):

```
[baseline] exit=0 PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
[drop S204] exit=1 PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED
[audit] S203 source=document document_digest=1
[audit] S204 source=transcript document_digest=0
[audit] S205 source=transcript document_digest=1
[audit] S206 source=document document_digest=1
[audit] S207 source=document document_digest=1
[audit] S208 source=document document_digest=1
[audit] S209 source=transcript document_digest=0
[audit] S210 source=transcript document_digest=0
[audit] transcript-only rows: S204 S209 S210
REPRO PASS
```

The other twelve experiments in the table above (e2–e14) were run against the mirror
at 03:2x–03:43 and are recorded there; only e0 and e1 are regenerated here, because
they carry the deletion verdict. `propose_strict.py` (5/8 document-anchored) is a
rebuild at `scratch-evidence/SimplifyRows/propose_strict.py`, sha256 `f3d4f142…8e9249`.
