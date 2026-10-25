# RevEntryR15 — entry `idle-lock-offered-in-the-bar-r15.md` vs receipts S206-S210 (round 35, wave 2)

Seat: RevEntryR15 (leaf reviewer, no dispatch). Lane: mado-shokunin. Date: 2026-10-25.
Target: `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` — re-taken at the current bytes
(2026-10-25T03:35:30, 102 lines, 5806 B, sha256 `82c08a4675863f69e0905b02810cae6299cdfe3038fb1255172f7b44f91fadfe`);
the 3428 B revision this seat first read was mutated mid-review and now carries Errata E1-E5.
Every quoted body passage below was re-read in the current bytes.
Substrates read-only: no bar started, no indicator executed, no menu opened, no toggle run.
Evidence locus: the Appendix below — a transcription of the 42 probes, durable because it lives in this
report, but **not** the bytes that were measured. The measured bytes are preserved: the round-35
`scratch/` tree was **relocated**, not deleted, into `.ufo/waves/round-35/scratch-evidence/` at
03:43-03:45: 235 files at commit `4efaf63`, 261 files at HEAD `1bb25c7`, 59 seat dirs. Quote a commit,
not a count — this seat's first measurement of the index read 240 and 26 files landed afterwards in
`b632f0b`, `ca870e9` and `1bb25c7`. Coverage is also not universal: `CritVacuous` and `RevTarget` sit in
neither the checkpoint nor the tree (seat RevShonen: `find -maxdepth 4 -name 'CritVacuous*' -o -name
'RevTarget*'` is empty), so "relocated, not deleted" holds for the 59 seat dirs that exist and not for
those two.
This seat's checkpoint copies are `findings.md` 3323 B sha256 `e5d010f3…9b165e` and `verify.log`
2049 B sha256 `61631900…c14a90`; that `verify.log` holds the re-take segment only (probes 28-37)
because this seat had replaced its own log with that segment before the checkpoint ran, so the
Appendix supersedes it for probes 1-27. At HEAD the directory carries both `verify.log` and
`verify.recovered.log` as one and the same git blob (`41ac5231`), so the truncated segment is all that
was ever preserved: probes 01-27 and 38-42 exist only in the Appendix, and no fuller original is
recoverable anywhere. That is a negative result worth stating, because it means nothing was lost by
the relocation — only by this seat's own earlier overwrite.
Locator to cite, commit-pinned: `git show 1bb25c7:.ufo/waves/round-35/scratch-evidence/RevEntryR15/verify.log`
(blob `41ac5231`) and `…/findings.md` (blob `c3e48109`). The worktree copy under `scratch-evidence/` is
not safe on its own — seat RevQuoteS205 found its own file there was a rebuild staged in the index while
HEAD held the measured original — so a reader must compare against the blob, not the path.
Checked for this seat specifically: working tree, `HEAD` and `4efaf63` carry the same sha256 for both
files (`61631900…` and `e5d010f3…`), so no post-move rebuild overwrote them here; other seats
(RevQuoteS204, RevQuoteS205, RevQuoteS207, ConnOverlap) were not so lucky, which is why the blob-pinned
form above is the one to cite.
`scratch/RevEntryR15/` was re-created twice during this seat
and is a convenience copy, never evidence; no verdict here depends on it.

## Axes

1. **A1 date fidelity** — the oldest-copy date the entry states equals a date its receipt carries.
2. **A2 count fidelity** — "2 files, 0 name the idle lock" and "four dated copies" equal receipt bytes.
3. **A3 gate legality** — exactly one `gate-quote:` per cited id, each 1-25 words, each a substring.
4. **A4 statement truth** — what the entry says the receipt means is what the cited source says.
5. **A5 citation closure** — every figure in the entry is carried by a cited receipt.

## Seat asks, answered

| ask | result | evidence |
|---|---|---|
| oldest-copy date = 2026-10-03? | **carried, and correct on the host** | S209 per-copy table row `2026-10-03 17:44 config.jsonc.bak.1791314470 handler=1`; host `2026-10-03 17:44:32.097653608 -0300` `exit=0`. **But** the receipt's own "oldest dated copy" block contradicts it (finding F4). |
| "2 files, 0 name the idle lock"? | **carried, exact, reproducible** | S210 `files in the directory: 2` / `files whose text names the idle lock: 0`; host `grep -ril idle ~/.local/state/omarchy/toggles/` → no match, `exit=1`. |
| one gate-quote per cited id? | **passes** | 5 `gate-quote:` lines; S206=1, S207=1, S208=1, S209=1, S210=1 (`exit=0`). |
| each 1-25 words? | **passes** | `quote.split()` lengths 13 / 15 / 14 / 13 / 15, all ≥1 and ≤25; each quote is a contiguous substring of its receipt bytes (`True` for all five). |

Harness cross-check: `python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json`
→ `PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`, `EXIT=0`.
The frozen gate passes. Everything below is outside its clauses: the gate proves each quote is a
*substring of the right length*, not that the paragraph built on it says what the receipt says.

## Re-take after the mid-review mutation

The entry changed under me at `03:35:30` (5806 B, Errata E1-E5 appended; a 4037 B intermediate at
`03:33:36` is reported by seat RevQuoteS210 and is not in the tree). Re-run on the current bytes:

| re-check | result |
|---|---|
| gate-quote lines | 5, one per id (S206=1 S207=1 S208=1 S209=1 S210=1) |
| word counts / substring | 13 / 15 / 14 / 13 / 15, all in 1-25, each substring with `occurrence=1` |
| C1 counter | `closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`, `EXIT=0` |
| receipt anchors | unchanged (receipts were not touched) |
| body §1-§5 | text of every passage cited below unchanged; the findings are not stale quotes |

All five errata were checked against the host, and all five are factually right:

- **E1** — `stat` on `config.jsonc.bak.1791314470` gives `Birth: 2026-10-06 16:21:10.082789105 -0300`
  and `Change: 2026-10-06 16:21:10.083846414 -0300`, exactly the epoch `1791314470`
  (`date -d` → `2026-10-06 16:21:10 -0300`). This confirms the two-clock reading in F3 outright.
- **E2** — journal window 2026-10-23 18:00-23:59 holds 4 `hypridle` lines:
  `app-Hyprland-hypridle-9408787a.scope: Consumed …` at `19:24:38-03:00` with no
  `Stopping`/`Stopped` pair, then `received: app -- hypridle` and `Started hypridle.` at `22:14:11`.
  Figure exact; the "who/which surface is unverified" hedge is correct.
- **E3** — `omarchy-toggle-idle` writes no file; `default/hypr/autostart.conf:1` carries
  `exec-once = uwsm-app -- hypridle`; `flags.conf` is byte-identical to the template (`cmp -s` 0).
- **E4** — `{"text": ""}` while running, tooltip only when absent; exactly one state carries words.
- **E5** — `notify-send` at lines 7 and 10; no notification history was read (mako config carries no
  persistence directive, `grep` `exit=1`).

So F1/F2/F3/F6 are *recorded* as withdrawn/corrected; what remains is where the correction lives and
what it is grounded in (N1-N4).

## Findings by severity

### F1 — HIGH — Section 3's mechanism is falsified, and one of its two facts is wrong against the receipt

Entry: *"The desktop keeps the state of its configuration toggles in one directory, and it holds
entries for other toggles - but not for the idle lock (S210)"*, INF *"the desktop was built not to
remember."*

S210 carries a listing of one path with two names and no contents. It carries neither "entries for
other toggles" nor a state-store scope. On the host:

- `~/.local/state/omarchy/toggles/hypr/flags.conf` is **byte-identical** to
  `/home/vgpnk/.local/share/omarchy/default/hypr/toggles/flags.conf` (`cmp -s`, `exit=0`), and its
  text is *"This directory is intended for permanent config toggle flags. / Do not remove this file
  (as the directory always needs at least one file)."* It is a mandatory placeholder, not a toggle
  entry.
- The only real toggle entry is `window-no-gaps.conf`, which also exists as a source template in
  `default/hypr/toggles/`. So the directory holds **one** entry for another toggle, not "entries",
  and the receipt's "2 files" counts a placeholder as content.
- The idle lock's state is not a config flag at all. `/home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle`
  (316 B, read-only `cat`) runs `pkill -x hypridle` or `uwsm-app -- hypridle`, sends a notification,
  and **writes no file**. Its state is process liveness, which S207 itself demonstrates (`pgrep -x hypridle`).
- The actual reason a choice does not persist across sessions is
  `/home/vgpnk/.local/share/omarchy/default/hypr/autostart.conf:1` → `exec-once = uwsm-app -- hypridle`,
  which re-arms the lock at login. That file appears in no cited source.

Independently corroborated by seat RevQuoteS210 (`.ufo/waves/round-35/w2/reports/RevQuoteS210.md`):
the same toggle script writes no store, and `find ~/.local/state/omarchy -maxdepth 2 -iname '*idle*'`
is empty; that seat reaches the same "structurally guaranteed, not unrecorded" reading and the same
plural defect in "holds entries for other toggles".

Consequence: "0 of them name the idle lock" is true, but the inference from it is a non-sequitur.
The desktop's own placeholder text says the directory *is* for permanent flags — the opposite of
"built not to remember" — and the idle toggle never used the flag mechanism. The entry's conclusion
(persistence of the choice is not recorded) can survive, but its stated evidence and mechanism
cannot: they are about config flags, and the idle lock is a process toggle.

### F2 — HIGH — Section 2's heading is false against the source it cites

Heading: *"The desktop names the two states itself."* The body is accurate; the heading is not.
S207 (`idle.sh`, 159 B, re-read on host): when `hypridle` runs it prints `{"text": ""}` — no icon,
no tooltip, **no name**; only the disabled state is named (`"tooltip": "Idle lock disabled"`).
One state is named and the other is silence. The same overstatement is baked into the registry
justification for S207 (`corpus/SOURCES.md` row S207: *"so the desktop names the two states
itself"*), so fixing the entry alone leaves the registry asserting the false form.
Knock-on: Section 4's *"shows which state is in force"* is true only for the disabled state; the
enabled state is inferred from absence.

### F3 — MEDIUM-HIGH — the 2026-10-03 / 2026-10-06 "divergence" is a two-clock artifact, presented as a correction

Section 5: *"The package's round-15 text dated the oldest dated copy 2026-10-06. This round's own
sweep ... dates the oldest 2026-10-03 ... The lane's measured figure is the one recorded here."*

Both figures are real and measure different things:

- mtime of `config.jsonc.bak.1791314470` = `2026-10-03 17:44:32.097653608 -0300` (content snapshot).
- the filename's epoch suffix decodes to `2026-10-06 16:21:10 -0300` (`date -d @1791314470`,
  `exit=0`) — **exactly** the package's 2026-10-06 (backup creation stamp).

That the `.bak` mtime is the copied content's mtime, not the copy time, is provable on the host:
live `config.jsonc` is `2026-10-17 17:02:56.289420985` and `config.jsonc.bak.1792267376` is
`2026-10-17 17:02:56.289334445` — the same instant, 86 µs apart. So no divergence exists to
"correct"; the package's date is the copy stamp and the lane's is the content mtime. Section 5
silently privileges mtime and omits the epoch, which is the only place the compared figure lives.
Separately (A5): **no cited receipt carries the literal `2026-10-06`**, and "the package's round-15
text" is named by no source id, so the compared artifact is outside the entry's source set.

### F4 — MEDIUM — the single S209 section the entry leans on is internally contradictory

`S209.receipt.txt`, `--- oldest dated copy ---`:

```
/home/vgpnk/.config/waybar/config.jsonc.bak
2026-10-03 17:44:32.097653608 -0300  /home/vgpnk/.config/waybar/config.jsonc.bak.1791314470
```

The lead path is `config.jsonc.bak`, which the same receipt's table dates `2026-10-11 10:36` (host
confirms `2026-10-11 10:36:07`). The receipt therefore prints two different files as "oldest", and
the entry takes the min line without disclosing that its section disagrees with itself. The entry's
date happens to be the correct one, which is why this is medium and not high — a reader cannot
verify the choice from the receipt alone.

### F5 — MEDIUM — a state-store scope claim S210 does not carry (A5)

*"The desktop keeps the state of its configuration toggles in one directory"* is a universal claim
about the desktop's storage design. S210 carries: one path, two filenames, and a count. It does not
carry file names, contents, or any statement that this directory is *the* store for *all* config
toggles. Three scripts do converge on the tree (`omarchy-toggle` → `toggles/<name>`;
`omarchy-hyprland-toggle` → `toggles/hypr/<name>.conf`), which makes the claim plausible, but the
entry cites none of them and S210 cannot support it.

Read at commit `4f35c80` — registry blob `28fd7e31`, content sha256 `0bf117e2…0d51`; HEAD `2909fea`
carries the same blob — where rows S206-S210 are byte-identical to the text this review quotes,
S210's `teaches` cell included. That pin matters, because the registry is not stable: seat
RevRowsUsedBy documents five in-place cell rewrites at 03:40:12 (S203/S204/S205 `teaches` and `scope`,
plus two `recheck` flips) that sit outside the columns `SOURCES.md:6-7` permits to change, and
`git diff --numstat 02088b4 4f35c80 -- corpus/SOURCES.md` reads `3 3` — the commit titled "as errata"
rewrites three row lines rather than appending. So F5 judges the cell as it stands at `0bf117e2…`; if
that cell is rewritten later, re-read the receipt before trusting either version, and note that C1
cannot see the change (see the row-truth bullet under residual risk).

### F6 — LOW-MEDIUM — "Why the choice leaves no trace" is unscoped

`omarchy-toggle-idle` lines 7 and 10 run `notify-send -u low "… Now locking computer when idle"`.
The choice therefore leaves a visible trace in the session's notification history (no on-disk
persistence: `~/.config/mako/config` has no `max-saved`/`persist`/`history` directive, `grep` `exit=1`).
Section 3's OBS sentence is correctly scoped to the directory; the heading and the INF are not.

### F7 — LOW — two OBS/claim blocks with no source id

Section 4's OBS (*"the desktop offers the choice in two surfaces, since at least 2026-10-03 on this
host, and shows which state is in force"*) and all of Section 5 carry no `(Sxxx)`. The counter still
reports `open_cites=0`, so this is a prose-completeness gap the frozen predicate cannot see. The
cross-entry link is present in one direction: `idle-lock-never-asked-r12.md:39` points at this file;
r15 does not name r12 or its ids.

## Status of F1-F7 against the errata

| finding | state after the errata |
|---|---|
| F1 | **partially adopted as E3** — the mechanism is correctly replaced. Residual: §3's INF *"built not to remember"* is still printed in the body, and *"holds entries for other toggles"* (plural) is not withdrawn and remains false (N3). |
| F2 | **adopted as E4** — the heading *"The desktop names the two states itself"* is still in the body; registry row S207 still asserts the same false form. |
| F3 | **adopted as E1, and independently confirmed by birth time** — §5's body is unchanged, so *"Divergence ... The lane's measured figure is the one recorded here"* still stands six lines above the erratum that refutes it (N2). |
| F4 | **not addressed** — the S209 receipt is unedited; the entry still cites the min line of a self-contradicting section. |
| F5 | **not addressed** — S210 still carries no storage-scope statement. |
| F6 | **adopted as E5** — the "leaves no trace" heading is unchanged. |
| F7 | **worsened** — the errata add prose with no source ids: E1 anchors to S209, E4 to S207, E2 only to a seat report, E3 and E5 to nothing. |

### N1 — MEDIUM — the correction is grounded in bytes the entry does not cite

E3 restates the mechanism from `bin/omarchy-toggle-idle`, `default/hypr/autostart.conf:1`, and the
`flags.conf` template identity. None of those is a source of this entry: no `Sxxx` id, no receipt, and
no row in `corpus/SOURCES.md` (`grep -n 'toggle-idle\|toggles/hypr' corpus/SOURCES.md` returns only
unrelated S088/S089/S093/S095 walker/theme rows). The errata therefore discharge the old claim with
evidence that is itself unregistered — the same A5 gap as F3, now load-bearing. E5 is the same shape:
`notify-send` is quoted with no id.

### N2 — MEDIUM — append-only errata leaves the withdrawn sentences live in the body

Every erratum says a body claim is withdrawn, and every one of those sentences is still printed
above it. Line numbers on the current bytes: §2's heading (line 35, E4), §2's *"does more than
toggle"* (line 37, no erratum), §3's INF *"built not to remember"* (line 52, E3), §4's *"shows which
state is in force"* (line 57, E4), §5's *"Divergence ... the lane's measured figure"* (lines 62-66, E1).
A reader who stops at §5 — the natural stopping point, since the errata are an appendix — reads the
version the entry itself now calls false. `idle-lock-never-asked-r12.md` handles the same situation
in-body (§3, "The scope of this entry"), so the corpus has a precedent for fixing rather than
appending.

Line 57 carries two clauses and they fail differently. The *state* half ("shows which state is in
force") is weak on E4's own standard: exactly one state carries words. The *date* half ("since at
least 2026-10-03") is sound, but only on the content clock, and the entry never labels the clock:
mtime `2026-10-03 17:44:32.097653608` is 119.801 s after the omarchy package stamp
`2026-10-03 17:42:32` (measured against `config/waybar/config.jsonc` at `17:42:32.296286539`), so it is not the
package's stamp; and `omarchy-refresh-config:23` makes `.bak.$(date +%s)` with `cp -f`, which does
not preserve mtime (the other three copies carry `mtime ≈ btime`), so the one copy that preserved
10-03 was made by a preserving path whose invocation is inferred, not demonstrated. A creation-clock
objection to this bound is a category error: 10-06 is when the copy was written, not when the offer
began.

### N3 — MEDIUM-LOW — "entries for other toggles" survives E3 and is false

E3 withdraws the causal reading but not this clause (lines 47-48). The directory holds two files: `flags.conf`,
byte-identical to the template placeholder, and `window-no-gaps.conf`. Exactly **one** entry exists
for another toggle. The clause needs the singular, or the sentence needs the placeholder named.

### N4 — LOW-MEDIUM — E2 withdraws a claim that is not in the file, and should re-point at §4's UNK

E2 (lines 78-79) targets *"Section 4's closing inference and this entry's title"* for saying "never
taken it". Neither is present: §4 closes with the UNK *"The operator's preference. No source can
answer it"* (lines 59-60), and the title is *"The desktop does offer the idle-lock choice - in the
bar and in the menu"*. `grep -in 'never taken'` and `grep -in 'title'` each return exactly one hit,
and both are E2's own text. The phrase E2 is actually in conflict with — *"built not to remember"*
(line 52) — is already E3's target (line 87), so E2 duplicates E3 while naming text the entry never
held. Written against the 4037 B intermediate is the consistent explanation.

The useful form of E2 is a re-point, not a withdrawal: its journal evidence bears on §4's UNK at
lines 59-60. A toggle-off inside the retained window means the journal *does* answer that a
toggle-off happened, though not who performed it or through which surface — so *"No source can
answer it"* is too strong for the action and still right for the preference.

### N5 — MEDIUM — "does more than toggle (S207)" misattributes the toggle to the indicator

§2's first OBS (line 37): *"The indicator does more than toggle (S207): it asks whether `hypridle` is running,
renders nothing when it is…"*. `idle.sh` has no toggle path — seven lines, `pgrep -x hypridle` and
one of two `echo`s. The toggle is `"on-click": "omarchy-toggle-idle"` at `config.jsonc:208`, i.e.
**S206**. So the sentence borrows S206's capability and cites S207 for it, then measures S207
against that borrowed capability. E4 corrected the "two states" wording but not this presupposition.
Independently found by seat RevQuoteS207 (`.ufo/waves/round-35/w2/reports/RevQuoteS207.md`).

## Figures the receipt does not carry

1. `2026-10-06` — absent from S206-S210 bytes; recoverable only by decoding filename epoch `1791314470` (F3).
2. "entries for other toggles" — S210 carries no filenames or contents; host shows one placeholder + one entry (F1).
3. "the desktop keeps the state of its configuration toggles in one directory" — S210 carries a listing, not a storage-design statement (F5).
4. "shows which state is in force" — beyond S207, which emits nothing for the enabled state (F2).
5. "in the interface they use every session" — INF, no receipt.
6. "the package's round-15 text" (2026-10-06 comparison) — no cited source id and no receipt (F3).
7. `omarchy-toggle-idle` body, `autostart.conf:1`, `flags.conf` template identity (E3) — no id, no receipt, no SOURCES row (N1).
8. the journal line `app-Hyprland-hypridle-…scope: Consumed` at 2026-10-23T19:24:38 (E2) — verified true on the host, carried by no S206-S210 receipt; E2 cites only a seat report.
9. "does more than toggle" (S207) — the receipt shows no toggle path; the capability belongs to S206 (N5).

## What holds (verified, not assumed)

- **Oldest date 2026-10-03**: receipt row and host mtime agree (`exit=0`).
- **Four dated copies**: receipt table 4 rows; host census `find … -name 'config.jsonc.bak*' | wc -l` → `4`, `exit=0`; no copy omitted.
- **Each carries the handler**: independent `grep -c omarchy-toggle-idle` → `1 1 1 1` on the four copies (live config also `1`), `exit=0`.
- **2 files, 0 name the idle lock**: exact against S210 and reproduced on the host (`grep -ril idle` → no match, `exit=1`).
- **Line references**: 207/208 in `config.jsonc` and 207/212 in `omarchy-menu` re-read on the host, `exit=0`.
- **S207 behaviour**: `pgrep -x hypridle` gate, empty text when running, `Idle lock disabled` tooltip when absent; 159 B.
- **Registry anchors**: receipt sha256 for S206-S210 equal the anchor cells of `corpus/SOURCES.md` rows 208-212 (`sha256sum`, `exit=0`).
- **Gate legality and harness verdict**: 5 quotes / 5 ids / 13-15 words / all substrings, re-run on the post-errata bytes (sha `82c08a46…`) after the 03:35:30 mutation; counter `closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`, `EXIT=0`.
- **Errata E1-E5 are factually right**: E1 confirmed to the second by `stat` Birth/Change; E2 confirmed against the user journal (4 `hypridle` lines, `Consumed` at 19:24:38, start at 22:14:11); E3, E4, E5 confirmed by host file reads.
- Not contradicted: `hypridle` is running (`pgrep -ax hypridle` → `1667`, `exit=0`), consistent with r14; the entry's UNK on the operator's preference remains open and correctly marked.

## Residual risk and verification gaps

Verified against entry sha256 `82c08a4675863f69e0905b02810cae6299cdfe3038fb1255172f7b44f91fadfe`
(5806 B, mtime 2026-10-25T03:35:30). The artifact is still moving under wave 2, so that sha travels
with every claim in this report; if the entry changes again, the gate-quote and F/N checks were run
against this revision, not the next one.

- **One ask, two closures.** Seat RevQuoteS210 keeps L2 open on the S210 side: the receipt carries
  names/count/0 only, and the "record of its configuration toggles" reading comes from uncited
  scripts (`omarchy-toggle:18`, `omarchy-hyprland-toggle:18`, `install/config/omarchy-toggles.sh:1-3`,
  `hyprland.conf:23`). Registering those four in S210's anchor cell, together with
  `bin/omarchy-toggle-idle`, `default/hypr/toggles/` and `default/hypr/autostart.conf` for E3, closes
  N1 and L2 in one edit rather than two separate errata.
- **Closure is formal, not semantic.** `corpus/SOURCES.md` moved at 03:40:12 (`02088b4` → `4f35c80`,
  content `848a7680…` → `0bf117e2…`, `git diff --numstat … 3 3`) with five cells rewritten in place
  outside the permitted columns (seat RevRowsUsedBy), and seat RevQuoteS205
  caught row S205's `teaches` changing wording while C1 stayed `TARGET_MET` rc=0. C1 checks identity,
  digest containment, status, cadence, used-by and the gate-quote substring — never the `teaches` cell.
  So `closed_rows=8` certifies well-formedness and anchoring, not row truth, which is exactly why F5's
  defect survives the gate; binding `teaches` to a hashed freeze-time snapshot would close it.
- The errata are correct but appended: five body sentences the entry now calls false are still
  readable above them (N2). Fixing the body is the only way a reader who stops at §5 gets the true
  version; `idle-lock-never-asked-r12.md` §3 is the in-body precedent.
- The correction's own evidence is unregistered (N1): `bin/omarchy-toggle-idle`,
  `default/hypr/autostart.conf:1` and the `flags.conf` identity need a source id and a receipt, or
  E3 is as uncited as the claim it replaces.
- S209's "oldest" section still needs a one-line fix (name the file the min line names); the entry's
  date is right by luck of the second line, and E1 does not repair the receipt.
- E2 points at text that is not in this file (N4); it should be re-pointed or dropped.
- §2's *"does more than toggle (S207)"* is still wrong about which surface toggles (N5), and
  "holds entries for other toggles" is still plural for a directory with one real entry (N3).
- I did not execute the bar, the indicator, the menu entry or the toggle, so the *offer's*
  behaviour is established by file reads only — the same limit the entry declares.
- No install or upgrade was performed; no package manager was invoked (pacman paused host-wide).

## Appendix — probe log (transcription of 42 probes; not the measured artifact)

Transcribed from the seat transcript after `scratch/` was relocated. It records what was run and what
came back; the measured originals are the checkpoint files named above. A reader comparing hashes
should treat this appendix as a re-derivation, not as evidence bytes.

Reads only. `R` = result, `x` = exit code. Entry revision throughout: sha
`82c08a4675863f69e0905b02810cae6299cdfe3038fb1255172f7b44f91fadfe`, 5806 B, mtime 03:35:30.

```
01 date -d @1791314470 -> 2026-10-06 16:21:10 -0300                                  x0
02 date -d @1792203278 -> 2026-10-16 23:14:38 -0300                                  x0
03 date -d @1792267376 -> 2026-10-17 17:02:56 -0300                                  x0
04 ls --time-style=full-iso config.jsonc* -> 5 files:
   config.jsonc 6354 10-17 17:02:56.289420985 | .bak 5892 10-11 10:36:07.023252903
   .1791314470 5114 10-03 17:44:32.097653608 | .1792203278 6068 10-16 23:14:38.105347715
   .1792267376 6068 10-17 17:02:56.289334445                                          x0
05 grep -c omarchy-toggle-idle per copy -> 1 1 1 1                                     x0
06 grep -c omarchy-toggle-idle live config.jsonc -> 1                                  x0
07 find ~ -maxdepth 5 -name 'config.jsonc.bak*' | wc -l -> 4                           x0
08 grep -c '^gate-quote:' -> 5; per-id S206=1 S207=1 S208=1 S209=1 S210=1              x0
09 quote.split() + q in receipt bytes -> S206 13w S207 15w S208 14w S209 13w S210 15w;
   all 1-25, all substring True                                                         x0
10 c1/count.py --root . --frozen c1/frozen.json
   -> PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET     x0
11 sha256sum fetch/S20[6-9].receipt.txt S210.receipt.txt -> equal registry anchors     x0
   S206 1d30e4a9… S207 81c33e79… S208 6e72f0db… S209 a170c7a5… S210 ef282e38…
12 cat bin/omarchy-toggle-idle -> pkill/uwsm-app hypridle + notify-send + waybar signal;
   no file write                                                                        x0
13 grep -n hypridle default/hypr/autostart.conf -> 1:exec-once = uwsm-app -- hypridle  x0
14 cat state toggles/hypr/flags.conf -> "…permanent config toggle flags… always needs at
   least one file"                                                                      x0
15 cat default/hypr/toggles/flags.conf -> identical text                                x0
16 cmp -s state flags.conf template flags.conf -> 0                                     x0
17 ls default/hypr/toggles/ -> flags.conf, single-window-aspect-ratio.conf,
   window-no-gaps.conf (state dir installs only window-no-gaps)                         x0
18 grep -ril idle state toggles/ -> no match                                            x1
19 cat indicators/idle.sh; wc -c -> 159 B, 7 lines, pgrep gate + two echoes             x0
20 pgrep -ax hypridle -> 1667 /usr/bin/hypridle                                         x0
21 sed -n '200,215p' config.jsonc -> 207 module, 208 on-click                           x0
22 grep -in 'max-saved|persist|history|on-notify' mako/config -> none                   x1
23 grep -n notify-send omarchy-toggle-idle -> lines 7, 10                               x0
24 S209 '--- oldest dated copy ---': line1 = config.jsonc.bak (table 10-11),
   line2 = 2026-10-03 17:44:32.097653608 -0300 .1791314470                              x0
25 grep -n '^| *S206…S210' SOURCES.md -> rows 208-212; S210(212) "holds entries…"      x0
26 grep -rn offered-in-the-bar corpus/knowledge -> r12:39 links r15                     x0
27 wc -lc entry (first read) -> 66 3428                                                 x0
28 stat entry -> 5806 2026-10-25 03:35:30.276175284                                     x0
29 sha256sum entry -> 82c08a46…fadfe                                                    x0
30 gate re-audit on new bytes -> 5 lines, counts 1 each, 13/15/14/13/15, occ=1          x0
31 c1 counter on current tree -> TARGET_MET                                             x0
32 stat .1791314470 -> Birth 2026-10-06 16:21:10.082789105,
   Change .083846414, Modify 2026-10-03 17:44:32.097653608                             x0
33 journalctl --user 2026-10-23 18:00-23:59 | grep hypridle -> 4 lines:
   app-Hyprland-hypridle-9408787a.scope: Consumed 19:24:38 (no Stopping/Stopped);
   uwsm received/sent at 22:14:11; Started hypridle. 22:14:11                             x0
34 grep -n 'never taken|never toggled|taken it|title' entry -> only E2 lines 78-79    x0
35 errata ids -> S204 x1 (report name), S207 x1 (E4), S209 x3 (E1); E3/E5 none         x0
36 grep -n 'toggle-idle|toggles/hypr' SOURCES.md -> no idle-toggle row                  x0
37 idle.sh re-read -> no toggle path; toggle is config.jsonc:208 (S206)                 x0
38 stat -c '%w|%y|%z' four copies -> only .1791314470 has mtime < btime;
   others mtime≈btime≈ctime                                                             x0
39 omarchy-refresh-config:23-24 -> .bak.$(date +%s) then cp -f (no -p)                  x0
40 stat omarchy package files -> all 2026-10-03 17:42:32 (config.jsonc .296286539);
   backup mtime 17:44:32.097653608 = +119.801 s -> preserved stamp is NOT the package stamp  x0
41 type -a cp -> /usr/bin/cp, GNU coreutils 9.12                                       x0
42 grep -c omarchy-toggle-idle default config/waybar/config.jsonc -> 1                  x0
```
