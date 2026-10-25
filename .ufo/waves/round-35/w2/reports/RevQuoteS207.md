# RevQuoteS207 — row S207 quote/anchor audit (round 35, wave 2)

Seat: RevQuoteS207 (leaf reviewer, no dispatch). Lane: mado-shokunin. Date: 2026-10-25.
Substrates read-only: no bar started, no indicator executed, no toggle run, no menu opened,
nothing written outside `scratch/RevQuoteS207/` and this report.
Machine log with per-command exit codes: `.ufo/waves/round-35/scratch/RevQuoteS207/verify.log`

## Axes

1. **A1 live-source identity** — the live `idle.sh` bytes today equal what the row's anchor records.
2. **A2 receipt fidelity** — the receipt embeds the live body and records live hashes/sizes/counts.
3. **A3 quote legality** — the entry's gate-quote is a contiguous, unique substring of receipt bytes.
4. **A4 statement truth** — the two facts the gate-quote asserts still hold on the host.
5. **A5 anchor identity** — receipt sha256 equals the anchor cell of row S207 and the frozen spec.

## Verdict: row S207 HOLDS. No divergence on (a), (b) or (c); the STOP clause is not triggered.

### (a) Live source re-opened

| check | command | result | exit |
|---|---|---|---|
| hash | `sha256sum /home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh` | `6d8d2c11d3c3b15fa0aa31a830410c98d9e630a7683a9cedffb888d10f0f1750` | 0 |
| size | `wc -c …` | `159` | 0 |
| lines | `wc -l …` | `7` | 0 |
| stat | `stat -c '%n type=%F nlink=%h mode=%A mtime=%y inode=%i uid=%u' …` | `…/idle.sh type=regular file nlink=1 mode=-rwxr-xr-x mtime=2026-10-03 17:42:32.308984887 -0300 inode=929 uid=1000` | 0 |
| resolve | `readlink -f …` | same path (not a symlink; `nlink=1`) | 0 |
| body | `cat …` | 7 lines, below | 0 |

```
#!/bin/bash

if pgrep -x hypridle >/dev/null; then
  echo '{"text": ""}'
else
  echo '{"text": "󱫖", "tooltip": "Idle lock disabled", "class": "active"}'
fi
```

159 B / sha `6d8d2c11…0f0f1750` are exactly the two values the anchor cell records
(`159 B, file sha256 6d8d2c11d3c3b15fa0aa31a830410c98d9e630a7683a9cedffb888d10f0f1750`).
Both branch payloads parse as JSON (`json.loads`, exit 0), so the emitted objects are well formed:

- line 4 `{"text": ""}` → keys `['text']`, `text=''`
- line 6 `{"text": "\U000f1ad6", "tooltip": "Idle lock disabled", "class": "active"}` → keys `['text','tooltip','class']`, `tooltip='Idle lock disabled'`, `class='active'`

The icon is one glyph, U+F1AD6. Checked against the host's installed fonts (fontTools 4.67.0,
ephemeral `uv run --with fonttools`): every JetBrainsMono Nerd Font face carries it as glyph
`md-timer_lock_open_outline` (96/96 Nerd Font files on the host carry it; 0 uncovered). This is corroboration of
"an icon", not part of the seat's required checks.

Liveliness of the cited path (beyond the seat; corroborates cell 1's "the idle indicator"):
`~/.config/waybar/config.jsonc` lines 207-212 define `custom/idle-indicator` with
`"exec": "$OMARCHY_PATH/default/waybar/indicators/idle.sh"` and `"return-type": "json"`, and line 18
lists the module in `modules-center`. `OMARCHY_PATH=$HOME/.local/share/omarchy` in
`~/.config/uwsm/env:4` and in `systemctl --user show-environment`, so the exec target is exactly
the audited file; `find $HOME -maxdepth 7 -name idle.sh -path '*waybar*'` returns this one copy only.

### (b) Gate-quote vs receipt bytes, and vs the host

The quote was **extracted from the entry file's bytes**, not retyped — the `gate-quote: S207 ` line
(`corpus/knowledge/idle-lock-offered-in-the-bar-r15.md:16`, exactly one such line):

```
located: idle.sh pgreps hypridle and prints the tooltip Idle lock disabled when it is absent
```

| measurement | value | exit |
|---|---|---|
| quote length | 92 B, **15 words** (frozen clause: 1-25) | 0 |
| `q in receipt_bytes` | **True**, offset **612**, ends 704 of 705 | 0 |
| occurrences | **1** | 0 |
| bytes after quote | `b'\n'` (quote is the receipt's final line) | 0 |
| receipt shape | 705 B, 15 LF-terminated lines, **no CR** | 0 |

The receipt is not merely an assertion about a file — it embeds the file. Reconstructing the
numbered body (`\t`-separated, lines 1-7) yields **159 B** whose sha256 is
`6d8d2c11…0f0f1750`, **byte-identical** to the live script (`embedded == live: True`, exit 0).
So the receipt and the host still describe the same bytes two days after `verified-at: 2026-10-24`.
Cross-entry check (beyond this row's requirement, run because the same entry carries all five
quotes): the identical extraction over every id the entry cites yields exactly one `gate-quote:`
line per id, each a unique contiguous substring of its own receipt —
S206 111 B / 13 words, S207 92 B / 15, S208 105 B / 14, S209 96 B / 13, S210 82 B / 15
(all occurrence 1, all followed only by a newline), reproducing RevEntryR15's table.
The receipt's own `--- tooltip count --- 1` also checks out: the live file contains exactly one
`Idle lock disabled` and one `tooltip` key.

Do the quote's facts still hold on the host? Both are structural claims about the script, read here
from live bytes:

| gate-quote fact | live evidence | verdict |
|---|---|---|
| `idle.sh` pgreps `hypridle` | line 3: `if pgrep -x hypridle >/dev/null; then` | holds |
| prints tooltip `Idle lock disabled` when it is absent | line 6, the `else` (pgrep-failed) branch: `"tooltip": "Idle lock disabled"` | holds |

Process state now: `pgrep -x hypridle` → `1667`, exit 0; `pgrep -af hypridle` → `1667 /usr/bin/hypridle`.
The daemon is running, so the *then* branch (`{"text": ""}`) is the one currently in force; the
quote's "when it is absent" branch is a conditional that was verified by reading bytes, not by
observing output (the script was not executed — lane rule).

### (c) Receipt sha256 vs the row's anchor cell

| value | measured | anchor cell, SOURCES.md row S207 | frozen spec | match |
|---|---|---|---|---|
| receipt sha256 | `81c33e7926f0bad071d31e9fc67e1d06967e3142da40ea3c93b16510b0adec59` | same | `c1/frozen.json` `receipts.S207.sha256` same | **equal** |
| receipt size | `705` | (not claimed in the row) | — | n/a |
| file sha256 | `6d8d2c11…0f0f1750` | `6d8d2c11…0f0f1750` | — | **equal** |
| file size | `159` | `159 B` | — | **equal** |

```
sha256sum .ufo/waves/round-35/fetch/S207.receipt.txt
81c33e7926f0bad071d31e9fc67e1d06967e3142da40ea3c93b16510b0adec59   exit=0
```

Row shape: exactly **one** S207 row (`grep -cE '^ {0,3}\|[[:space:]]*S207[[:space:]]*\|'` → `1`,
exit 0), **11 cells**, no literal or escaped pipe. Status `mined`, recheck `on-change`, used-by
`corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` — the same entry that carries the quote, so
the counter's used-by/citing equality is satisfied by content, not by coincidence.

Counter state at attack time (read-only runs, both exit 0):

```
python3 -I .ufo/waves/round-35/c1/count.py --root $PWD --frozen $PWD/.ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET          rc=0
python3 -I .ufo/waves/round-35/c2/count.py --repo $PWD --frozen $PWD/.ufo/waves/round-35/c2/frozen.json
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET  rc=0
```

### Concurrent change observed during this audit

The entry changed under this seat between first read (`a6c3d54b42fea483b09254b898e16b86c6fa388944e9aa3cf20d2a946100ac03`)
and close (`82c08a4675863f69e0905b02810cae6299cdfe3038fb1255172f7b44f91fadfe`): seat
RevEntryR15 (authorship confirmed in its message to this seat) appended a 36-line
`### Errata (round 35, wave 2)` block below line 64
(E1 S209 dating clock, E2 "never taken it" withdrawn, E3 "built not to remember" withdrawn,
**E4 "one state is named, the other is silence" — S207**, E5 notification history). Nothing
above line 64 moved. Re-verified against the **current** bytes: the S207 gate-quote line (16)
is byte-identical and still unique (`grep -c 'gate-quote: S207 '` → `1`, exit 0), 92 B /
15 words, contiguous in the receipt at offset 612, count 1; the prose line cited in LOW-1 (37)
still reads "The indicator does more than toggle (S207)…"; and PRED-C1 still prints
`closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET` (rc=0), PRED-C2
`uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET` (rc=0) after the
edit. The certification below therefore applies to the current entry hash, not a stale one.

## Findings by severity

**None blocking. No divergence, so the STOP clause was not reached.**

**LOW-1 — entry prose attributes the toggle to S207.** Entry line 37 reads
"The indicator does more than toggle (S207): it asks whether `hypridle` is running…". `idle.sh`
contains no toggle path at all; the toggle lives in the waybar module's `on-click`
(`config.jsonc:208`, cited by S206). The sentence's presupposition ("does more than toggle") is
imported from S206, while its evidential clause is exactly S207. Severity is low because the
registry cell for S207 (cell 6) does **not** carry the toggle presupposition — it states only the
two-state behaviour, which the file supports — so no counted claim is affected. Suggested
minimal wording: "The indicator also reports state (S207): …". Status at close: the appended
errata (E4) corrects Section 2's heading wording but not this presupposition — line 37 is
unchanged, so LOW-1 is still open at the entry level.
Cross-check with RevEntryR15's N5 (independently reproduced here): the sentence is
**self-undercutting** — its colon-clause enumerates only rendering ("asks whether `hypridle` is
running, renders nothing when it is, and renders an icon whose tooltip reads `Idle lock
disabled`"), i.e. the evidence supplied contradicts the "does more than toggle" presupposition
inside one line. Shown by the live bytes: line 37 still reads that sentence verbatim, and
`grep -c 'does more than toggle'` → 1 (exit 0).

**INFO-1 — "renders nothing" is a rendering-layer wording for `{"text": ""}`.** Both cell 6 and
entry §2 say the indicator "renders nothing when it is [running]". The script prints a JSON object
with an empty `text`; the module sets no `format` and no `hide-empty-text` (block 207-212),
so the default `{text}` renders empty. `man 5 waybar-custom` documents `hide-empty-text` as the
opt-in that *disables* a module on empty output, so default behaviour is "present but empty", not
"no module". No execution was performed to observe pixels; the claim is accurately scoped to a
file read and does not overreach materially. Convergence: the appended errata item **E4** makes
exactly this correction at the entry level ("one state is named, the other is silence"), so the
only place still carrying the unqualified "renders nothing" phrasing is SOURCES cell 6 — the
counted claim, which remains supportable.

**INFO-2 — the counted predicate does not verify the anchor's file-sha claim (S207 is honest anyway).**
`c1/count.py` opens only `corpus/SOURCES.md` (line 162), the entry (168) and the named receipt (173);
it never opens the source path named in the row. Its anchor clause is
`receipt["sha256"] in cs[5]` (line 192) — a **substring** test of the frozen receipt digest against
the whole anchor cell, so the row's `file sha256 6d8d…` assertion, and the file's existence, sit
entirely outside the counted predicate. For S207 this gap is closed by hand here: the file exists,
is 159 B, and its digest equals the anchor to all 64 hex digits. Relatedly, the gate-quote clause
`quote.encode() in blob` (line 195) is satisfiable by construction whenever the receipt's final line
is the summary the entry copies — as it is (offset 612, the last line). Contiguity therefore proves
provenance, not host agreement; A4 is the clause that actually binds the receipt to reality, and it
holds. Reported as predicate hygiene for the counter's owners, not as a defect of S207.

**INFO-3 — the golden control's S207 row is not byte-identical to the live row (both pass).**
`.ufo/waves/round-35/controls/golden/corpus/SOURCES.md` carries an 8-row fixture (S203-S210 only)
whose S207 row differs from live in two non-semantic tokens: golden `159 B, sha256 …` vs live
`159 B, file sha256 …`, and golden `tooltip "Idle lock disabled"` vs live `tooltip Idle lock disabled`
(quotes stripped). Both have 11 cells and no pipes, and
`c1/count.py --root controls/golden` prints `verdict=TARGET_MET` rc=0. The same caveat holds for
the entry: the golden copy equals the pre-errata live entry (`a6c3d54b…`) and now lags live by the
appended errata block, while still passing. The live rows/files are the measured artifact and are
what this report certifies; the fixture drift is noted so nobody reads the golden as a byte-copy of
the tree.

**INFO-4 — cross-check of the entry's own errata (sibling corroboration, not a row-S207 defect).**
While re-verifying after the concurrent edit I reproduced RevEntryR15's two observations on the
current bytes (entry sha `82c08a46…`, 5806 B): (i) E4's S207 correction is accurate — it names the
two branches correctly — but the §2 heading it corrects (line 35, "The desktop names the two
states itself") and the body sentence (line 37) are still printed above it; (ii) E2 labels text the
entry does not contain: `grep -in 'never taken'` → **1** hit, line 78 (E2's own label);
`grep -in 'title'` → **1** hit, line 79 (E2 itself); the phrase E2 actually conflicts with is
`built not to remember`, which occurs at line 52 (body §3 INF) and line 87 (E3, which does target
it). So the errata's self-description cannot be taken at face value when reading §2 — the S207
correction (E4) happens to be sound, and LOW-1's line 37 is not among the texts any erratum
addresses. Reconciliation with RevEntryR15's **N4**, which we reached independently: the split is
facts vs referents — the journal facts E2 states are right, the referents it names (title, §4
closing inference) are absent from the file and overlap E3's real target (line 52), so the repair
is to re-point E2 at §4's **UNK** (lines 59-60), which the journal does answer ("that a toggle-off
happened"). Agreed; that fix is entry-level and outside row S207.

**INFO-5 — line 57's state clause is weak; my date objection is WITHDRAWN after measurement.**
Entry §4 OBS (lines 56-57) reads "The premise is corrected: the desktop offers the choice in two
surfaces, since at least 2026-10-03 on this host, and **shows which state is in force**."
(i) The S207 half survives only weakly: the display differs between states (icon+tooltip vs
`{"text": ""}`), but under E4's own standard ("exactly one state carries words") the armed state is
silence, so the reader gets one named state and one inferred one — overstated, not false.
(ii) **Retraction.** I first recorded the "since at least 2026-10-03" half as unsupported on the
creation clock. RevEntryR15's rebuttal is correct and I reproduced it: the copy's birth time cannot
refute a content bound. Measured here — `config.jsonc.bak.1791314470` is 5114 B and **byte-identical
to the shipped default** `~/.local/share/omarchy/config/waybar/config.jsonc`
(`ff387b21ab51f4d5c4752142de31d1cfb2e8a459647a8f84849a522aee57c061` both, handler=1 both); its
btime is `2026-10-06 16:21:10.082789105` while its mtime is `2026-10-03 17:44:32.097653608`
(mtime < btime ⇒ inherited), which is **119.801 s** after the omarchy install stamp
`17:42:32.296286539` — so that mtime is not the package stamp but a distinct local write; and the
default itself carries mtime `17:42:32.296286539` == btime `17:42:32.296177350` (ctime 17:42:36.944),
a **non-inherited** local write at 10-03. The content therefore existed on the host from
2026-10-03, and the literal bound holds. What survives is narrower: the entry does not say which
clock the bound uses, and the preserving copy's creator is inferred — `omarchy-refresh-config:23` is
a plain `cp -f` (no `-p`), which cannot preserve an mtime, and the other three backups show exactly
the plain-copy signature (`.bak` 10-11: btime==mtime==ctime; `.1792203278`: all three identical;
`.1792267376`: btime .289181525 / mtime .289334445). So: unlabelled clock plus inferred provenance,
not an unsupported bound. RevEntryR15 has adopted the state half as its N2 item; the date half is
not a defect.

## Residual risk

- The receipt proves content identity, not display: `modules-center` membership and font coverage are
  necessary, not sufficient (no bar was started; a theme/CSS gate would not be visible from files).
  The entry's OBS is correctly scoped and says so in its header.
- The "absent" branch was proven by bytes; with hypridle running (pid 1667) the live behaviour would
  show nothing today. This is a property of the script, so the claim stands, but it was not observed.
- Cross-row consistency (S206's click handler, S209's four copies, S210's empty toggles dir) is out
  of this seat's scope and was not adjudicated here.
- `verified-at: 2026-10-24` vs attack 2026-10-25: content hashes match and the file mtime is
  2026-10-03, so the day difference carries no content drift.

## Verification gaps

- Nothing was executed from the substrate (no bar start, no indicator run, no toggle) — by design.
- No LSP server applies to a shell script, a receipt text file, or a markdown registry: `read xd://lsp`
  returns `No such tool: xd://lsp` (this seat mounts no LSP device), and no LSP server targets this
  lane's artifacts anyway. The proofs here are byte/hash/process measurements, which are the
  appropriate evidence for anchoring claims.
- The glyph check establishes font coverage, not that the running bar draws it.

## Installs

- `fontTools 4.67.0` (with Python 3.15.0) — channel: `uv run --with fonttools` (uv 0.13.0, PyPI,
  ephemeral; pacman is paused host-wide and no pacman transaction was run). Reason: verify that
  U+F1AD6 (`md-timer_lock_open_outline`) is covered by the installed Nerd Font faces. Note: uv 0.13
  rejects the older `uv run -c` shape; the working form is `uv run --with fonttools python -c …`.
  Nothing else installed.
