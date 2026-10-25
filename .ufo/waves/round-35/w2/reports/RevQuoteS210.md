# RevQuoteS210 — attack on registry row S210 (round 35, wave 2)

Seat: `L1Mado35.RevQuoteS210` · leaf · read-only attack · 2026-10-25
Target row: `corpus/SOURCES.md:212` (S210, host toggle-state directory)
Attacked entry: `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md`
Receipt: `.ufo/waves/round-35/fetch/S210.receipt.txt`
Evidence (live path after the 03:45 relocation):
`.ufo/waves/round-35/scratch-evidence/RevQuoteS210/rederive.sh`
(3727 B, sha256 `468c54a6e2e2e2c79931ea416cadd4f027655199c4bcfb6e40174b90b6e675df`) →
`.ufo/waves/round-35/scratch-evidence/RevQuoteS210/rederive.out`
(2714 B, sha256 `4b7b77d6d3fd8bc661a61d5b02c53feebd4db68fbca3b8ad860649911c0a2026`);
re-run rc=0 with output discarded (no write).

**Evidence relocation (03:45), and why the citation is now durable.** The pre-03:43
`.ufo/waves/round-35/scratch/` content was moved to
`.ufo/waves/round-35/scratch-evidence/` (per-seat dirs, mtimes 03:43) and then
checked in: `scratch-evidence/RevQuoteS210/rederive.sh` and `rederive.out` are
**tracked at HEAD** (blobs `0ac004a4…` and `53d8daa6…`), and `git hash-object` of
the worktree files returns those same blob ids — so the bytes I pin above are the
bytes at HEAD, not a worktree chance. The tree holds **261 tracked paths across 59
seat dirs** at HEAD; the checkpoint commit `4efaf63` ("checkpoint the 235 seat
evidence files…") carries 235, with `b632f0b`, `ca870e9`, `1bb25c7` adding the rest
— pin the count to the revision you cite, not to the live index.

**Cite the commit, not the path.** Durable anchor for the two files:
`git show HEAD:.ufo/waves/round-35/scratch-evidence/RevQuoteS210/rederive.sh`
(HEAD = `1bb25c7`, blob `0ac004a4…`) and `…/rederive.out` (blob `53d8daa6…`).
`git hash-object` of both worktree files returns those same blob ids, and — the
decisive check — `git show HEAD:<path> | sha256sum` and
`git show 4efaf63:<path> | sha256sum` both print the pinned values
(`468c54a6…` / `4b7b77d6…`), with `git diff --name-only HEAD -- …/RevQuoteS210`
producing no output. Checkpoint, HEAD and worktree are therefore byte-identical at
this seat: the bytes I pin are the tracked bytes, and no rebuild was merged over
them. That check is not academic — six seats reported the trap materialising at the
same relative path: `RevEntryR14` restored its 8446 B measured log from `4efaf63`
after a rebuild overwrote it, `RevQuoteS203`/`S204` worktree logs are reconstructions
while their checkpoint blobs carry the measured bytes, `RevQuoteS207`'s copied file
now hashes `dffe5da6…` where the checkpoint has `64d433f9…`, `RevQuoteS205`'s
worktree file is a 9858 B rebuild against an 8205 B original, and `RevC2Tip`'s
`attack.py` differs from the checkpoint by four rebuild-header lines. Presence in
`scratch-evidence/` is not provenance: hash the file and compare it to the commit
before citing it.

Two cautions, both observed, neither affecting this seat:

- `scratch/` still churns. It has been re-created and re-swept repeatedly since the
  move (I saw 1 entry — `CritAxisClaims` — and no `RevQuoteS210`; peers saw 7 seat
  dirs, then none). A bare `scratch/<Seat>/` path therefore names a *different
  namespace* from the one measured, and can resolve to a transcript rebuild rather
  than the measured bytes. Cite `scratch-evidence/<Seat>/` with the shas above.
- The move carried **top-level files only** (reported by `RevRowsUsedBy`): whole
  subdirectories — snapshots, mutant trees — were dropped, so prepending `-evidence`
  recovers a `<Seat>/file` citation but never a `<Seat>/subdir/file` one. Checked
  here: `find …/scratch-evidence/RevQuoteS210 -mindepth 1 -type d | wc -l` → **0**,
  so this seat lost nothing to that limit, and both files still hash to the values
  pinned at the top.
- The move was **not complete for every seat**: `scratch-evidence/CritVacuous` and
  `scratch-evidence/RevTarget` are absent (found by `RevShonen`), so for those seats
  prepending `-evidence` does not recover anything. Here both cited peer files are
  present and sha-verified, so S210's chain is intact; the general rule is
  "check before assuming the move recovered it", not "prepend and trust".

A rebuilt file is not the measured bytes, so no transcript reconstruction was used
anywhere in this seat; the script is also reproduced inline in Appendix A, which
makes the report self-sufficient even if both trees vanish.

Axes attacked: (A1) gate-quote byte contiguity, (A2) host fact agreement,
(A3) receipt-digest vs row anchor, (A4) assertion mechanism support.

## Verdict

**AGREE on all three required checks. No falsification found.** The gate-quote is
byte-exact and contiguous, both stated facts still hold on the host, and the
receipt digest equals the row's anchor cell. Assertion-precision defects are
reported below (M1, L1, L2 on the row; L3 on a wave-1 report; A1 adjacent in the
r15 entry); none touches the quote, the digest, or the measured negative, and none
changes the C1 verdict. On the current 5806 B bytes, errata **E3/E4** record the M1
and A1 corrections, but the falsified body sentences remain live above them
(recorded, not repaired).

## (a) Live source re-opened

```
$ ls -la /home/vgpnk/.local/state/omarchy/toggles/hypr          # rc=0
-rw-r--r-- 1 vgpnk vgpnk 141 Oct  3 17:44 flags.conf
-rw-r--r-- 1 vgpnk vgpnk 135 Oct  3 17:53 window-no-gaps.conf

$ find /home/vgpnk/.local/state/omarchy/toggles/hypr -maxdepth 1 -type f   # rc=0
.../flags.conf
.../window-no-gaps.conf

$ ls -A /home/vgpnk/.local/state/omarchy/toggles/hypr | wc -l  # 2  (no hidden entries)

$ grep -ril idle /home/vgpnk/.local/state/omarchy/toggles/hypr # rc=1 (no match)
$ grep -ril idle ... | wc -l                                   # 0
$ per-file: flags.conf idle=0 lock=0 hypridle=0
            window-no-gaps.conf idle=0 lock=0 hypridle=0
```

**2 files, 0 of them naming the idle lock.** Matches the standing corpus
knowledge (`corpus/knowledge/config-health-report-r3.md:115-117`,
`hyprland-config-plane.md:141-146`, `remaining-planes-census.md:151-153`:
`flags.conf` 141 B comment-only, `window-no-gaps.conf` 135 B).

Entry-set stability (stronger than a point check): the directory mtime is
`2026-10-03 17:53:16.247826301`, byte-identical to `window-no-gaps.conf`'s mtime
— the directory has had no entry added or removed since 2026-10-03. The receipt's
2026-10-24 listing and this 2026-10-25 re-list therefore describe the same entry
set; the 2-file fact is not a sampling artifact.

Provenance discriminator (the receipt could only come from the state dir):
`default/hypr/toggles` holds **3** files (`flags.conf`,
`single-window-aspect-ratio.conf`, `window-no-gaps.conf`). A 2-file listing pins
the score to `~/.local/state/omarchy/toggles/hypr`, as the receipt header claims.

## (b) Gate-quote vs receipt bytes

`python3 -I` byte check over the raw receipt (no text normalisation):

| measure | value |
|---|---|
| receipt size | 385 bytes |
| quote size | 82 bytes |
| first index | 302 |
| occurrences | 1 |
| contiguous substring | **True** |
| bytes after quote | `b'\n'` (quote ends a line, no trailing fragment) |
| entry line 19 quote == receipt substring | **True** (byte equality, not paraphrase) |
| word count | 15 (inside the 1–25 window) |
| `gate-quote: S210` lines in entry | 1 |

The receipt's last line is exactly the gate-quote; the entry reproduces it with
no edit (`idle`/`lock` casing, the `2` and the `0` all verbatim).

Facts stated — re-measured on the host: 2 files ✓, 0 naming the idle lock ✓.

## (c) Receipt digest vs row anchor

```
$ sha256sum .ufo/waves/round-35/fetch/S210.receipt.txt                  # rc=0
ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726
$ stat -c '%n type=%F size=%s' .../S210.receipt.txt                     # rc=0
`.ufo/waves/round-35/fetch/S210.receipt.txt` type=regular file size=385
```

Row anchor cell (col 6) carries the same digest; `c1/frozen.json` `S210.sha256`
carries it too (1 occurrence in `corpus/`, 1 in frozen). Row shape checks, all
passing: exactly one `| S210 ` row, 11 cells, no literal or escaped pipe, status
`mined`, opened `2026-10-24`, recheck `90d`, used-by `[r15]` (exactly the one
admitted entry citing S210).

Context check: the C1 counter still returns
`PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`
(rc=0) with this row as written.

## Findings

### M1 — MEDIUM — assertion's causal framing is unsupported by the mechanism it names

Row cell 7 asserts: *"the idle lock has none - so the operator's choice leaves no
trace in the place where a choice about other toggles would have left one."*

The measured negative is true, but the counterfactual is false for this toggle.
`~/.local/share/omarchy/bin/omarchy-toggle-idle:1-14` (the very command S206/S208
route to) contains **no reference to the toggle store at all**: it `pgrep`s
`hypridle`, `pkill`s it or spawns it via `uwsm-app`, then signals waybar. It writes
no flag, in `toggles/hypr/` or anywhere else:

```
$ grep -rn "toggles" ~/.local/share/omarchy/bin/omarchy-toggle-idle   # no output
$ timeout 20 find ~/.local/state/omarchy -maxdepth 2 -iname '*idle*'  # rc=0, no output
$ grep -rn hypridle ~/.config/hypr/                                    # no output
```

So the idle lock is a *live-process* toggle, not a persisted-flag toggle: even had
the operator pressed it, no file in the store would appear. The absence is
structurally over-determined, not evidence about a choice.

The re-arm half of the mechanism is also uncited anywhere in S206–S210:
`/home/vgpnk/.local/share/omarchy/default/hypr/autostart.conf:1` is
`exec-once = uwsm-app -- hypridle` — every login starts the lock again, so the only
per-session record is process state (`pgrep -x hypridle` → **1667**, inside
`app-Hyprland-hypridle-d4bd7533.scope`; `systemctl --user is-active hypridle` →
`inactive`, **rc=3**). That record is a transient app scope, not a persisted unit or
a service state, which is why no file and no unit state survive the session. `grep -n
autostart` over `.ufo/waves/round-35/fetch/*.receipt.txt` and the entry returns no
hit for any of these ids (`corpus/SOURCES.md` hits at lines 100-107 are unrelated
rows). Cross-seat corroboration: `L1Mado35.RevEntryR15` reached the same mechanism
reading independently.

**Current-bytes status.** The entry now records this reading as errata **E3**
(`omarchy-toggle-idle` writes no file; `autostart.conf:1` re-arms; `flags.conf` is
the byte-identical template placeholder) and E3 explicitly says "Section 3's causal
reading is replaced by that mechanism". So the correction is recorded — but §3's
causal sentence is still live in the body above the errata (append-only divergence,
tracked as N2 by `RevEntryR15`), and the measurement clause "2 files, 0 naming idle"
is untouched, which is correct. **Scope limit I accept:** E5 notes the toggle calls
`notify-send`, so a notification may survive in session history; "no trace" holds for
on-disk state only, which is all my `find`/`grep` checks cover.

The row's own purpose cell ("whether the operator's choice ... could ever have been recorded") is still
answered "no" — but the answer rests on the toggle's design, not on the empty
directory, and the row currently credits the directory. As worded, a reader can
correctly object that the absence proves nothing, because the idle toggle does not
write there.

Suggested repair (does not touch the gate-quote or digest): append one sentence
citing `omarchy-toggle-idle` and say the store is where *flag* toggles
(`omarchy-hyprland-toggle` → `toggles/hypr/<flag>.conf`;
`omarchy-toggle` → `toggles/<flag>`; writer confirmed at
`omarchy-hyprland-toggle:18`, `omarchy-toggle:18`, creator at
`install/config/omarchy-toggles.sh:1-3`) record state, while the idle toggle
records nothing anywhere — hence "could never have been recorded" directly.

**The contradiction is now between two live artifacts.** The entry's errata E3
withdraws exactly the clause the row still teaches ("the place where a choice about
other toggles would have left one"), yet SOURCES.md pays no attention to errata: the
row is the version that survives into the registry, so the repair has to be made in
cell 7 (and in the entry's §3 sentence), not only in an appended block. Noted
independently by `SimplifyRows`.

### L1 — LOW — "holds entries for other toggles" is plural; only one is a toggle entry

Of the two files, `flags.conf` is explicitly not a toggle entry:

```
# This directory is intended for permanent config toggle flags.
# Do not remove this file (as the directory always needs at least one file).
```

It is copied unconditionally by `install/config/omarchy-toggles.sh:3` and is
byte-identical to the template (`cmp -s` rc=0, both
`sha256 4daee1c7…437c`), so its presence is installer behaviour, not an operator
choice. Only
`window-no-gaps.conf` is a live toggle entry; the top-level
`~/.local/state/omarchy/toggles/` holds **0** files. The corpus already knows this
(`config-health-report-r3.md:115` calls `flags.conf` "comment-only"), so the row's
plural reads as a contradiction with standing knowledge. Suggested wording:
"the placeholder `flags.conf` plus one enabled toggle file, `window-no-gaps.conf`".

**Status on current bytes (5806 B):** E3 records the placeholder identity, but body
line 48 still reads "and it holds entries for other toggles - but not for the idle
lock (S210)" unchanged. The correction exists only in errata; the live sentence is
still plural. Same append-only shape as A1 and as `RevEntryR15`'s N2/N3.

### L2 — LOW — receipt supports names/count/0-idle; the store's semantics are uncited

The receipt records only the path, two names, `files in the directory: 2`, and `0`.
It does not record file contents, and it names no writer. Therefore the row's
subject ("the desktop's own record of its configuration toggles") and cell 7's
"keeps the state" are supplied from outside the receipt (the scripts above, plus
the source glob `~/.config/hypr/hyprland.conf:23`). Grade A holds for the measured
fact (a direct, re-openable host measurement); the semantic half of the row needs
the writer citation to be self-supporting. Add
`omarchy-hyprland-toggle:18` / `install/config/omarchy-toggles.sh:1-3` to the
anchor cell.

### L3 — LOW (wave-1 artifact, not corpus) — `ScoutS210.md` swaps the two file sizes

`.ufo/waves/round-35/w1/reports/ScoutS210.md:13-14` gives `flags.conf` 135 B and
`window-no-gaps.conf` 141 B. Live values are the reverse (141 B / 135 B), as the
corpus files above already state. The receipt records no sizes, so nothing in
`SOURCES.md` or the entry inherits the error; the wave-1 report does.

### A1 — LOW (adjacent, S207's slice) — r15 §2 heading overstates its own body

`corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` §2 is headed "The desktop
names the two states itself", but its own OBS and the S207 receipt bytes say
otherwise: enabled → `{"text": ""}` (unnamed), disabled → `tooltip: "Idle lock
disabled"`. Exactly one of the two states is named. Verified against
`.ufo/waves/round-35/fetch/S207.receipt.txt` lines 4-6; the S207 gate-quote itself
("prints the tooltip Idle lock disabled when it is absent") is accurate and is
another seat's scope (`RevQuoteS207`). Suggested heading: "The desktop names the
off state". SOURCES.md row S207 repeats the same overstatement in its teaches cell.

**Status on current bytes (5806 B):** errata **E4** now records this exactly ("one
state is named, the other is silence"), yet the §2 heading is still live in the body.
Recorded, not repaired — `RevEntryR15`'s N2 covers the append-only pattern.

## Cross-seat corroboration (each item independently re-verified here)

`L1Mado35.RevEntryR15` reported the same conclusions by a different path. I
confirmed its two load-bearing additions rather than taking them on trust:

- **`flags.conf` is byte-identical to the template.** `cmp -s` against
  `default/hypr/toggles/flags.conf` → rc=0; both
  `sha256 4daee1c7f3cbbac4a2031f48c84265fdf9c36f688a6663bfeaa52405f61a437c`.
  So "2 files" = 1 installer placeholder + 1 real entry. Supports L1.
- **The non-persistence mechanism is the autostart line**, not the empty store —
  verified above and folded into M1.
- **Two-clock dating (r15 §5).** `date -d @1791314470` → `2026-10-06 16:21:10 -0300`,
  matching `config.jsonc.bak.1791314470` and the package's date, while its mtime is
  `2026-10-03`; the live `config.jsonc` and `config.jsonc.bak.1792267376` both carry
  mtime `2026-10-17 17:02`. The entry already records this as errata **E1**,
  attributed to `RevQuoteS209`; no action needed from this seat.
- **I do not adopt** the reading that `flags.conf`'s text "directly contradicts" the
  entry's INF. The file proves the store is *designed* for permanent flags, which
  tightens M1 (the idle toggle is absent from the persistence plane by construction);
  it does not bear on the separate INF about the idle lock being built not to
  remember, which the autostart re-arm supports.

**Entry mutated twice during wave 2.**
`corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` was written at
`2026-10-25 03:33:36 -0300` (4037 B, E1/E2) and again at `2026-10-25 03:35:30 -0300`
(**5806 B, sha256 `82c08a4675863f69e0905b02810cae6299cdfe3038fb1255172f7b44f91fadfe`,
errata E1–E5**). All three required checks were re-run against those current bytes:
`gate-quote: S210` lines = **1**, quote still a receipt substring (**True**,
occurrences 1), words 15, receipt sha unchanged `ef282e38…0b8726`, and the C1
counter still `TARGET_MET` (rc=0). My results are timestamped against the 5806 B /
`82c08a46…` state, not the pre-errata file. Because the file is still moving,
re-run `scratch-evidence/RevQuoteS210/rederive.sh` (rc=0) before quoting any of these
figures.

## Residual risk (not defects; each checked)

- **Brittle quote.** The gate-quote embeds the count `2`. Any toggle added or
  removed later makes the quote false; `90d` is the right cadence and the
  directory-mtime argument above shows it is stable today. Family-level note: every
  S206–S210 quote embeds a count or a dated copy sense, so this is not S210-specific.
- **No revision key — S210 is the odd row of the eight.** Its source is a mutable
  host path outside any checkout: `readlink -f ~/.local/state/omarchy/toggles/hypr`
  resolves to itself (no symlink), it is **outside** `~/.local/share/omarchy`, and
  that checkout versions **0** paths under `state/omarchy/toggles` (it is clean at
  `8fcc9d604`, `git status --porcelain` empty). So unlike S203/S207/S208 there is no
  commit to cite: the receipt sha plus the recheck trigger (`90d`, operator-action)
  are the only anchor, which is exactly why the re-derivation script is inlined in
  Appendix A and why the directory-mtime argument is load-bearing. Confirmed
  independently by `ConnOverlap`.
- **Registry moved under this seat, without touching the row.** `corpus/SOURCES.md`
  changed at `2026-10-25 03:40:12 -0300` (171446 B; S203/S204 `recheck`
  `on-request` → `on-change`). Re-verified after that write: S210 is still 1 row, 11
  cells, `mined` / `2026-10-24` / `90d` / used-by `[r15]`, anchor cell still carries
  `ef282e38…`, and the C1 counter returns `TARGET_MET` rc=0. Row S210 is also
  byte-identical (**832 B, `cmp` rc=0**) to its pre-repair form at `d2b6972`, so the
  in-place cell rewrites that landed in that commit did not reach this row.
  `RevRowsUsedBy` reports the ones that did — S203.teaches, S204.scope,
  S204.teaches, S205.teaches, outside the `{status, recheck, used-by}` set — which
  is a registry-governance finding for those rows, not this one; I verified only
  that S210 is unchanged.
- **Historical id reuse.** `corpus/lessons/round-33-verifier-spotcheck.md:110` and
  `round-34.md:88-91` record a then-staged literature file citing S210/S211 as CSDN
  posts. The current staged file
  (`…/shokuknow/…/two-literature-drift-r26.md`, 5670 B) cites
  S212/S215/S216/S217 and contains **0** occurrences of S210; the registry has
  exactly one S210 row and zero S211 rows. No live collision; only a merge hazard
  if an older staged revision resurfaces.
- **Peer convergence.** `.ufo/waves/round-35/scratch-evidence/SentProvenance/S210.rederive.txt`
  independently reached the same 2-file / 0-idle result;
  `.ufo/waves/round-35/scratch-evidence/SentProvenance/S210.semantics.txt`
  independently found that `omarchy-toggle-idle` never touches the store (M1). Two
  seats, same bytes.

## Verification gaps (stated, not passed)

- The receipt contains no command lines, so the exact command that produced it is
  unreproducible; only its output shape is re-derivable (done above).
- No `lsp` device is mounted in this seat's toolset (available: read, bash, edit,
  eval, glob, grep, task, wait, web_search, write), and the artifacts are
  `*.md`/`*.txt` with no semantic-symbol layer anyway, so byte-level comparison is
  the strongest available check. Caller/definition analysis was done by reading the
  actual producer scripts, not by text inference about them.
- I did not attempt to locate an idle preference outside omarchy state (shell
  history, editor session, operator memory) — out of scope for this row, which is
  scoped to the toggle store.
- Read-only throughout: no lane corpus file, counter, control, `SOURCES.md`, jj
  state, or Git index was modified; only `.ufo/waves/round-35/scratch/RevQuoteS210/`
  and this report were written (the scratch tree was later relocated wholesale to
  `scratch-evidence/` by the external sweep, not by me). No tool installs were
  needed (python3, coreutils, grep, find only).

## Bottom line

Required checks: **(a) pass, (b) pass byte-exact, (c) pass digest-equal**. Row S210
is not falsified. Recommended action: keep the gate-quote and digest as they are;
reword cell 7 to attribute "never recorded" to `omarchy-toggle-idle`'s lack of a
persistence mechanism, correct "entries" to the one real toggle entry, and cite the
writer scripts in the anchor cell.

## Appendix A — re-derivation script, inline

Reproduced verbatim so this report does not depend on either scratch tree. It is a
read-only script: it lists, greps and hashes; it writes nothing. Run it from any
directory. Its output against the 5806 B / `82c08a46…` entry is the `rederive.out`
pinned at the top (sha256 `4b7b77d6…a2026`), and the script itself hashes
`468c54a6…e675df`.

```bash
#!/bin/bash
# RevQuoteS210 — read-only re-derivation of row S210 (wave 2, round 35).
# Run from anywhere. Writes nothing outside this scratch directory.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
DIR=/home/vgpnk/.local/state/omarchy/toggles/hypr
REC=$LANE/.ufo/waves/round-35/fetch/S210.receipt.txt
ENTRY=$LANE/corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
ROW=$LANE/corpus/SOURCES.md

echo "## live directory: $DIR"
ls -la "$DIR"; echo "ls-rc=$?"
echo "--- regular files (includes dotfiles) ---"
find "$DIR" -maxdepth 1 -type f | sort; echo "find-rc=$?"
echo "--- entry count, hidden included ---"
ls -A "$DIR" | wc -l
echo "--- files whose text names the idle lock (case-insensitive) ---"
grep -ril idle "$DIR"; echo "grep-rc=$? (1 = no match)"
grep -ril idle "$DIR" 2>/dev/null | wc -l
echo "--- per-file keyword counts ---"
for f in "$DIR"/*.conf; do
  printf '%s idle=%s lock=%s hypridle=%s size=%s mtime=%s\n' \
    "$(basename "$f")" "$(grep -ci idle "$f")" "$(grep -ci lock "$f")" \
    "$(grep -ci hypridle "$f")" "$(stat -c %s "$f")" "$(stat -c %y "$f")"
done
echo "--- directory mtime vs window-no-gaps.conf mtime (entry-set stability) ---"
stat -c '%n %y' "$DIR" "$DIR/window-no-gaps.conf"

echo
echo "## receipt bytes and gate-quote contiguity"
python3 -I - "$REC" "$ENTRY" <<'PY'
import sys
rec_path, entry_path = sys.argv[1], sys.argv[2]
rec = open(rec_path, 'rb').read()
quote = b"located: the toggles/hypr directory holds 2 files and 0 of them name the idle lock"
print("receipt bytes:", len(rec))
print("quote bytes:", len(quote))
i = rec.find(quote)
print("first index:", i, "occurrences:", rec.count(quote))
print("contiguous_substring:", i != -1)
print("after-quote bytes:", None if i == -1 else repr(rec[i+len(quote):]))
line = [l for l in open(entry_path, 'rb').read().split(b'\n') if b'gate-quote: S210' in l][0]
prefix = b'gate-quote: S210 '
assert line.startswith(prefix), line
entry_quote = line[len(prefix):]
print("entry_quote_equal_to_receipt_substring:", entry_quote in rec)
print("entry_quote_words:", len(entry_quote.split()))
print("gate_quote_lines_for_S210:", sum(1 for l in open(entry_path, 'rb').read().split(b'\n') if b'gate-quote: S210' in l))
PY
echo "py-rc=$?"

echo
echo "## receipt sha256 vs row anchor"
sha256sum "$REC"; echo "sha-rc=$?"
stat -c '%n type=%F size=%s mtime=%y' "$REC"
grep -c "ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726" "$ROW"
python3 -I - "$ROW" <<'PY'
import sys
rows = [l for l in open(sys.argv[1], encoding='utf-8').read().split('\n') if l.startswith('| S210 ')]
print("S210 row count:", len(rows))
cells = [c.strip() for c in rows[0].strip().strip('|').split('|')]
print("cells:", len(cells))
print("status:", repr(cells[7]), "opened:", repr(cells[8]), "recheck:", repr(cells[9]))
print("used-by tokens:", cells[10].split(','))
print("escaped pipe in row:", '\\|' in rows[0])
print("sha in anchor cell (6):", 'ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726' in cells[5])
PY
echo "py-rc=$?"

echo
echo "## provenance discriminator: score runs on the state dir, not the default dir"
find /home/vgpnk/.local/share/omarchy/default/hypr/toggles -maxdepth 1 -type f | wc -l

echo
echo "## who writes the toggle store / does the idle toggle persist anything"
grep -n "toggles/hypr" /home/vgpnk/.config/hypr/hyprland.conf
sed -n '16,20p' /home/vgpnk/.local/share/omarchy/bin/omarchy-hyprland-toggle
sed -n '17,19p' /home/vgpnk/.local/share/omarchy/bin/omarchy-toggle
sed -n '1,14p' /home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle
echo "--- idle-named state anywhere under omarchy state (depth<=2) ---"
timeout 20 find /home/vgpnk/.local/state/omarchy -maxdepth 2 -iname '*idle*'; echo "find-rc=$?"
```

Its key lines on the measured revision, for a reader who runs nothing:
`receipt bytes: 385`, `first index: 302 occurrences: 1`,
`contiguous_substring: True`, `after-quote bytes: b'\n'`,
`entry_quote_equal_to_receipt_substring: True`, `entry_quote_words: 15`,
`gate_quote_lines_for_S210: 1`, `S210 row count: 1`, `cells: 11`,
`status: 'mined' opened: '2026-10-24' recheck: '90d'`,
`used-by tokens: ['corpus/knowledge/idle-lock-offered-in-the-bar-r15.md']`,
`escaped pipe in row: False`, `sha in anchor cell (6): True`.
