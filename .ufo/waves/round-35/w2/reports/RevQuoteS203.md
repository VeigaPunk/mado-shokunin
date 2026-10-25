# RevQuoteS203 — wave 2 falsification of registry row S203

Seat: `L1Mado35.RevQuoteS203` (leaf reviewer). Round 35, wave 2.
Lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only attack; no lane corpus,
counter, control, `SOURCES.md`, jj/Git state, or `/home/vgpnk/Projects/shokuknow` byte was modified.
Scratch evidence — **original measured bytes**: git blob
`4efaf63:.ufo/waves/round-35/scratch-evidence/RevQuoteS203/evidence.log`, 4282 B / 87 lines, sha256
`b5cc5c04e890aa06052f95860ad650070779ea29457c3f68c59b73d741d249d9` (checkpoint commit
`4efaf639ffb6aeb1fed1adeea12350dbb2c38082`, 2026-10-25 03:43:55). The `scratch/` tree was **moved**
to `scratch-evidence/`, not deleted. The *working-tree* file at that path is a transcript
reconstruction (sha256 `c70cafb44c5bf5f5a9ae518738c6876f2bb7deb6df55547827ba9ae97b35a4ae`,
6531 B / 127 lines) written after the move — **a rebuild is not evidence**, so the committed blob is
the cited source. Its full content is inlined as Appendix A, which is the durable copy: this report
body is authoritative and needs neither path.
Host reads only (sha256sum/wc/ls/grep/python read); no first-run script was executed.
No tool installed or upgraded this seat.

## Verdict

**CONFIRM — no divergence.** The S203 gate quote is a contiguous substring of the receipt, the
facts it states still match the live host, and the receipt hash equals the anchor cell of row S203.
All three assigned checks pass; the claim survives attack intact.

**Scope caveat — this verdict covers row S203's evidence only.** Entry `idle-lock-never-asked-r12.md`,
the entry this row gates, is **not** clean: its second conjunct ("the operator never toggled it
afterwards", gated on S204) is unsupported and now positively contradicted. See
"Entry-level defect inherited through S204". Mid-review the entry gained an Errata section whose E1
withdraws exactly that conjunct, while the title and §1/§2 still assert it unmarked — and
`SOURCES.md` was rewritten too (see "Concurrent mutation of the artifacts"). C1 still reports
`TARGET_MET` because its frozen predicate tests quote-contiguity and registry hygiene, **not** the
truth of the entry's prose — that gap is reported below as the round's main residual risk.

Axes named: **A1** quote-contiguity · **A2** live-fact fidelity · **A3** hash-anchor fidelity ·
**A4** claim honesty/scope.

## A1 — quote contiguity (PASS)

Entry-side gate quote, `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/idle-lock-never-asked-r12.md:12`:

```
gate-quote: S203 located: install/first-run/ lists 12 scripts; the omarchy-first-run body runs all 12; none is idle-lock
```

Quoted portion checked against receipt bytes:

```
python3 -I -c "q='located: install/first-run/ lists 12 scripts; the omarchy-first-run body runs all 12; none is idle-lock'; b=open('.ufo/waves/round-35/fetch/S203.receipt.txt','rb').read(); qb=q.encode(); print('count',b.count(qb),'offset',b.find(qb),'words',len(q.split()))"
→ count 1 offset 3033 words 14          EXIT=0
```

- Contiguous: yes, exactly **1** occurrence, at byte offset **3033** of a **3137**-byte receipt
  (`wc -c` → 3137, EXIT=0), i.e. the final line; the only tail after it is the single `\n`.
- Word count **14**, inside the frozen predicate's 1–25 word window
  (`.ufo/waves/round-35/c1/frozen.json` → `"a contiguous substring of the receipt bytes and is 1-25 words long"`).
- Receipt is LF-only (`\r\n` absent) and newline-terminated, so the quote is not an artifact of
  normalization.

## A2 — live-fact fidelity (PASS, all three clauses)

Re-opened `/home/vgpnk/.local/share/omarchy/bin/omarchy-first-run` on the host:

| Fact asserted by the quote | Live observation | Command / exit |
|---|---|---|
| file identity | `20508471d8237a60e630baf58f87c0b5a4391e34196ce11e5034745f6a062630` — equal to receipt and to the row's file hash | `sha256sum …/omarchy-first-run` → EXIT=0 |
| size | `1089` B — equal to receipt | `wc -c …` → EXIT=0 |
| "install/first-run/ lists 12 scripts" | dir holds **13** entries, of which **12** are `*.sh`; the 13th is `install-voxtype.hook` | `ls -1 …/install/first-run \| wc -l` → 13 EXIT=0; `ls -1 …/*.sh \| wc -l` → 12 EXIT=0 |
| "the omarchy-first-run body runs all 12" | body contains **12** `install/first-run/*.sh` invocations; invocation set is **exactly equal** to the dir's `*.sh` set (body∖dir = ∅, dir∖body = ∅) | `grep -c 'install/first-run/.*\.sh' …` → 12 EXIT=0; python set-diff → `SET_EQUAL True` |
| "none is idle-lock" | no `idle`/`lock` match anywhere under `install/first-run/`; likewise no match in the installer body | `grep -rq -i 'idle' …/install/first-run/` → `IDLE_ABSENT` EXIT=0 |

Supporting checks, all exit 0:

- Receipt-embedded body is **byte-identical** to the live body (28/28 lines, `EMBEDDED_EQ_LIVE: True`) —
  the receipt is not a paraphrase of a drifted file.
- `nl -ba` confirms the row's cited range `body lines 3 and 8-27`: line 3 is the
  `omarchy:summary=Finish the installation of Omarchy …` comment; lines 8–27 are the mode-file gate,
  the 12 invocations, the hook registration and the sudoers cleanup.
- `install-voxtype.hook` is *registered*, not `bash`-run (`omarchy-hook-install post-update …`, line 23),
  which is why "12 scripts" and "runs all 12" are consistent with a 13-entry directory.
- Hidden-file test: `ls -A1` = 13 and `find -mindepth 1 -maxdepth 1` = 13 — no suppressed entries.

### Homonym disarmed (recorded so no later seat re-raises it)

`install/login/default-keyring.sh:12` contains `lock-on-idle=false`. This is a **GNOME-keyring**
setting (`[keyring]` section of `Default_keyring.keyring`), invoked from `install/login/all.sh:2` —
it is **not** the desktop idle lock and therefore **not** a counterexample to "none is idle-lock".
The only other `idle` hit in the install tree is `hypridle` in `install/omarchy-base.packages:53`.

## A3 — hash-anchor fidelity (PASS)

```
sha256sum .ufo/waves/round-35/fetch/S203.receipt.txt
→ 1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646   EXIT=0
awk -F'|' '$2 ~ /S203/ {print $7}' corpus/SOURCES.md   → 1b7fa87…1646   EXIT=0
```

Row S203 (`corpus/SOURCES.md:205`; 950 B at first read, **990 B after the 03:40:12 rewrite** — see
"Concurrent mutation of the artifacts") anchor cell:
`…; receipt .ufo/waves/round-35/fetch/S203.receipt.txt sha256 1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646`.

- **Equal.** No divergence to report. Re-verified against the post-rewrite file: the anchor cell is
  byte-identical and still the unique match.
- The hash is **unique** in the registry (`grep -c <hash> corpus/SOURCES.md` → 1), so the anchor is
  not a copy-paste placeholder shared across rows.
- Cell hygiene matches the frozen predicate: exactly one well-formed S203 row, no literal/escaped
  pipe inside any cell (12 pipes → 11 content cells: id, description, origin, admit, axis,
  evidence, note, status, date, recheck, used-by; `escaped_pipe False`), status `mined`, used-by
  `corpus/knowledge/idle-lock-never-asked-r12.md`. Recheck cell changed from `on-request` (first read)
  to `on-change` (post-rewrite); both are cadence tokens, and the frozen predicate only requires a
  valid token, so C1 is unaffected — recorded because it proves the registry moved under this review.
- `frozen.json` receipt entry for S203 carries the same sha256, so anchor and frozen target agree.
- Corroboration the claim is still load-bearing (read-only run):
  `python3 -I .ufo/waves/round-35/c1/count.py --root … --frozen …` →
  `PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`, **EXIT=0**.

## Findings by severity

### BLOCKING / HIGH — none

No divergence in quote, facts, or hash. Nothing here supports reopening C1.

### MEDIUM-1 — the post-rewrite row note asserts the hook was *executed*; refuted

After the 03:40:12 rewrite, row S203's note reads: "The post-login questionnaire runs **thirteen
items, twelve of them first-run scripts** … **none of the thirteen executed items** asks about the
idle lock".

The first half is an improvement (13 items, 12 of them scripts). The second half is not: it calls all
thirteen items *executed*, and the thirteenth item is `install-voxtype.hook`. Refuted by:

- `omarchy-first-run:23` runs `omarchy-hook-install post-update …/install-voxtype.hook`, and that
  command only copies and chmods (`bin/omarchy-hook-install:27-29`) — it does not execute the hook.
- The hook self-deletes on run (`install-voxtype.hook:6` → `rm -f "$0"`) and is still on disk at
  `~/.config/omarchy/hooks/post-update.d/install-voxtype.hook` (174 B, mode 755) ⇒ it has never
  executed, on this host, at any point.

Correct wording: "thirteen commands — twelve run first-run scripts, one installs a hook that does not
run during first-run". The substantive claim ("none asks about the idle lock") survives either way;
only the word "executed" misapplied to the hook is wrong. Note the entry's Errata E2 uses the
defensible form ("executes 13 items: 12 `bash …/*.sh` plus `omarchy-hook-install …`"), so row and
entry currently disagree in precision on the same point.

A statement census of the body settles the arithmetic. Executable actions are **15**: 12
`bash …/first-run/*.sh`, 1 `omarchy-hook-install` (line 23), 1 `sudo rm -f /etc/sudoers.d/first-run`
(line 24), 1 `rm -f "$FIRST_RUN_MODE"` (line 11); **14** excluding the guard's own cleanup, and
**12** of them are scripts. Hence "thirteen items" is coherent only as "the 13 files in
`install/first-run/`" (12 `*.sh` + 1 `*.hook`) — and under that reading "the thirteen **executed**
items" is precisely the wrong word. Any command-centred reading of "thirteen" additionally drops
`sudo rm -f /etc/sudoers.d/first-run`. E2's own bullet mixes the two itemizations: its heading counts
files (13, twelve scripts) while its body counts commands. Recommended wording, true under both
readings: "thirteen first-run artifacts — twelve scripts that run, one hook that is installed and does
not run; the body also clears `/etc/sudoers.d/first-run`".

### LOW-1 — receipt's own enumeration is count-vs-names inconsistent

`S203.receipt.txt` prints `12` under `--- first-run scripts on this host ---` and then lists
**13** filenames (the 13th being `install-voxtype.hook`). The gate quote inherits the word "scripts",
which is only true under `scripts ≡ *.sh`. This is not a false statement — the hook is *installed*,
not executed — but the receipt section title ("first-run scripts") presents 13 names under a
12-count heading, so a future seat re-deriving "12" from the filenames gets 13 and must repeat the
`*.sh` reasoning. Suggest the receipt label the block `*.sh` / note the hook, at next re-mint.

The `*.sh` boundary is the *correct* one, proven rather than assumed:

- `omarchy-hook-install` (`bin/omarchy-hook-install`) only materialises the file — `mkdir -p
  "$HOOK_DIR"`, `cp "$HOOK_FILE" "$HOOK_PATH"`, `chmod 755` (lines 27–29). It never `bash`es or
  `source`s it; the hook is dispatched later by `omarchy-hook` (`bin/omarchy-hook:3`), outside
  `omarchy-first-run`.
- The hook self-deletes on first run (`install-voxtype.hook:6` → `rm -f "$0"`). It is **still
  present** at `~/.config/omarchy/hooks/post-update.d/install-voxtype.hook` (174 B, mode 755,
  mtime 17:48), which proves it has **never executed** on this host.

Therefore "the omarchy-first-run body runs all 12" is exactly right: 12 `bash *.sh` lines, set-equal
to the directory's 12 scripts. Only the receipt's *label* for the 13 listed names is loose.

### Cross-row resolution — S204 peer's "executes 13 items" is refuted

Peer `L1Mado35.RevQuoteS204` reported (and asked me to confirm on my row) that the count "12" is
wrong because `ls …/install/first-run/ | wc -l` = 13 and `omarchy-first-run` "executes 13 items:
12 `bash *.sh` lines plus `omarchy-hook-install post-update …/install-voxtype.hook`".

Resolved as follows, with the evidence above:

- **`wc -l` = 13 is correct but counts files, not scripts.** 13 files = 12 `*.sh` + 1 `*.hook`.
  "12 first-run scripts" is true of the directory's script population; the assertion that it is
  "wrong" rests on equating "files in the directory" with "scripts".
- **"Executes 13 items" is false.** `omarchy-hook-install` is a copy-and-chmod installer, and the
  installed hook is still on disk with a self-delete on line 6 — it never ran. First-run executes
  12 items; it *installs* a 13th artifact for a later `omarchy-hook post-update` dispatch.
- **The substantive leg survives on my reading too**, independent of the peer's grep: `idle`/`lock`
  absent from both the directory and the installer body (`IDLE_ABSENT`).
- **Neither point is a C1 falsifier.** C1's frozen predicate is quote-contiguity (contiguous
  substring, 1–25 words) plus registry/anchor hygiene; it does not adjudicate the truth of the
  quote's prose. The quote remains a legitimate contiguous receipt substring, and the anchor hash
  matches. LOW-1 stays a presentation defect for the receipt/row, to be fixed at re-mint — it does
  **not** reopen C1 and does not support an entry correction beyond clarifying the hook.

### LOW-2 — row gloss "post-login questionnaire" is unsupported by the body

Row S203's description calls the installer "the desktop's post-login questionnaire".
`grep -rn 'gum confirm\|gum choose\|read -\|read -r' install/first-run/` → `NO_INTERACTIVE_PROMPTS`
(EXIT=0). `omarchy-first-run` asks the operator **nothing**; it is a one-shot bootstrap.
No factual error propagates into the entry (r12 correctly says "runs a fixed list of twelve
first-run scripts"), but the row's noun overstates interactivity and should be narrowed to
"post-login bootstrap" to avoid implying the choice existed and was declined rather than never offered.

### LOW-3 — frozen evidence is narrower than the row's stated axis (scope boundary, material)

The row's axis reads "Whether **the desktop's setup path** asks the operator about the idle lock…
whether an intent could have been recorded at setup", but S203's evidence covers only
`install/first-run/` plus the `omarchy-first-run` body. The wider setup path does more than nothing:

- `install/config/config.sh:3` → `cp -R ~/.local/share/omarchy/config/* ~/.config/`
- ships `config/hypr/hypridle.conf` (765 B), whose live copy at `~/.config/hypr/hypridle.conf`
  enables locking by default (`on-timeout = omarchy-system-lock` after ~5 min, plus
  `before_sleep_cmd`), and `hypridle` is installed via `install/omarchy-base.packages:53`.

So the setup path **silently sets the idle lock to ON** while asking nothing. That **confirms**
rather than contradicts "never offered as a choice" (no intent could be recorded because no
question was posed), and the entry's own scope section is careful. The risk is reader over-read:
"the setup path asks nothing about the idle lock" can be mis-read as "setup never touches the idle
lock". Recommend the entry add one sentence stating that setup installs an idle-lock **default**
(ON) without asking; this is the one place where the frozen claim's coverage is narrower than its
axis wording.

## Entry-level defect inherited through S204 (escalation) — C1 passes, claim fails

Entry r12's title is "The idle lock was never offered as a choice at setup, **and the operator never
toggled it afterwards**". S203 supports only the first conjunct (A1–A3 above). The second conjunct
rests entirely on S204, and verified independently it does **not** hold.

### 1. The S204 counter cannot measure toggle usage (vacuous instrument)

`journalctl --user --no-pager | grep -c 'omarchy-toggle'` → `0`, **grep EXIT=1** (zero matches),
reproducing the receipt. But `bin/omarchy-toggle-idle` (13 lines) contains **no journal primitive**:
`grep -n 'logger\|systemd-cat\|journal\|echo'` → `NO_LOGGING_PRIMITIVE`. Its entire body is
`pgrep -x hypridle` → `pkill -x hypridle` (OFF path) / `uwsm-app -- hypridle &` (ON path), two
`notify-send`, and `pkill -RTMIN+9 waybar`.

- The OFF path writes **nothing** anywhere.
- The ON path writes `uwsm_app-daemon: received: app -- hypridle`, which does **not** contain the
  string `omarchy-toggle`.

Therefore the count is `0` **whether or not** the operator used the toggle. The receipt's sentence
is literally true and measures nothing; the entry's move from "0 journal hits" to "never exercised"
is invalid.

### 2. A positive event carries the toggle's exact signature

`journalctl --user -g hypridle`:

```
Oct 23 13:21:39 systemd[1490]: Stopping hypridle...
Oct 23 13:21:39 systemd[1490]: Stopped hypridle.
Oct 23 13:21:39          app-Hyprland-hypridle-59197064.scope: Consumed 22.796s CPU time over 1d 8h 25min 52s
-- Boot e55f9cd9ec4e4dd5bf0ce775977af5a5 --
Oct 23 13:25:00 uwsm_app-daemon[1838]: received: app -- hypridle
Oct 23 13:25:00 systemd[1529]: Started hypridle.
Oct 23 19:24:38 systemd[1529]: app-Hyprland-hypridle-9408787a.scope: Consumed 2.783s CPU time over 5h 59min 38.213s   <-- no Stopping/Stopped
-- Boot 0a3785aac7104585a914f6cda41795a7 --
Oct 23 22:14:11 uwsm_app-daemon[1805]: received: app -- hypridle
Oct 23 22:14:11 systemd[1493]: Started hypridle.
```

Every alternative cause is excluded, each by its own command (all EXIT=0 unless noted):

| Hypothesis | Evidence | Ruled out |
|---|---|---|
| session boundary | boot heading `0a3785…` precedes 22:14:11; 19:24:38 sits inside the 13:22:32 boot, unlike the 13:21:39 stop which has Stopping/Stopped | yes |
| crash | `coredumpctl list \| grep -i hypridle` → `NO_COREDUMP` | yes |
| OOM / earlyoom | at 19:24:59 earlyoom reports `19479 of 21438 MiB (90.86%)`, swap `92.30%` free; the 8 "kill/SIG" matches that day are earlyoom's startup policy lines (13:24:57, 22:14:08) — no kill records | yes |
| package update | pacman.log per-day 10-21:20, 10-22:2, **10-23:0**, 10-24:22, 10-25:31 | yes |
| Hyprland restart | 19:20–19:30 contains one DEBUG heartbeat (19:23:53) plus the scope line | yes |
| config edit / refresh | `hypridle.conf` sha256 `e7d3b8dd…` identical to the shipped default; mtime `2026-10-03 17:44:32` | yes |

Only two code paths `pkill -x hypridle`: `omarchy-toggle-idle:6` (kill, **no** relaunch) and
`omarchy-restart-app:6` used by `omarchy-restart-hypridle` (kill **plus** immediate
`uwsm-app -- hypridle`). The restart path is excluded because its ON write would emit
`received: app -- hypridle`, and no such line follows until the next boot. The one
evidence-compatible cause left is the toggle's OFF path.

**Conclusion.** "The operator never toggled it afterwards" is dead. Proven: a mid-session hypridle
kill with no relaunch. Not proven: who sent the signal. The entry may say at most "no journal trace
of a toggle exists, and this journal could not record one" — which is no evidence at all.

### 3. Effect on the frozen targets — and why TARGET_MET must not be over-read

- **C1 is unaffected in its own terms.** Its frozen predicate (quoted from `frozen.json`) is
  quote-contiguity (contiguous receipt substring, 1–25 words) plus registry/anchor hygiene. r12's
  S204 gate-quote is also a clean contiguous substring of `S204.receipt.txt` (count 1, offset 351,
  12 words, EXIT=0). `c1/count.py` → `closed_entries=3 closed_rows=8 open_cites=0 TARGET_MET`, EXIT=0.
- **But `TARGET_MET` is not a truth verdict** and must not be reported as one. In this entry the two
  legs differ in kind: S203 verified clean (A1/A2/A3 above); S204 a vacuous counter plus a
  contradicted inference. Recommend r12's title and Section 2 be corrected before the round treats
  it as established knowledge.

**The withdrawal propagated to neither the headline nor the registry.** On current `SOURCES.md`
(`0bf117e2…`, 171446 B) row **S204** still asserts, in its own cells:

- PURPOSE: "…the idle lock was **never asked about and never toggled** — the installer's script count
  and the journal's **absence of any omarchy-toggle invocation**"; and
- NOTE: "**Two independent negatives agree**: the setup path offers no idle-lock question (12
  first-run scripts, none about idle) and the user journal holds zero omarchy-toggle invocations,
  **which is a null channel rather than a negative**".

One sentence affirming agreement *and* nullity in the same breath; the 12-count survives in the NOTE
while the entry's own E3 concedes it is a re-count, not an independent confirmation. Row 206's
evidence cell meanwhile says the daemon stop/start is merely "consistent with a toggle-off". So the
registry contradicts itself across three cells, and the entry contradicts itself across four sites —
the errata withdrew the claim in prose only. Verdict: the *artifact of record* still carries the
withdrawn assertion in five places (entry H1/§1/§2, row PURPOSE, row NOTE), which is why
`TARGET_MET` cannot be read as endorsement of content.

## Concurrent mutation of the artifacts (observed during this review)

Both scored artifacts changed under me mid-wave. Recorded with hashes and times, because a review
that quotes stale bytes is worthless:

| Artifact | First read | After mutation | Evidence |
|---|---|---|---|
| `corpus/SOURCES.md` | sha256 `848a7680c175f1ac64ffa4c63673adab19edc7963393d3b24b8b189e78d4fe80`; row 950 B; note "runs **twelve** first-run scripts"; recheck `on-request` | sha256 `0bf117e2f472ec4f80adec17d58fe50b4fbd4fa9568ffa8523a4bfc272950d51`; row 990 B; note "**thirteen** items … thirteen executed items"; recheck `on-change` | `stat` mtime `2026-10-25 03:40:12 -0300`, 171446 B |
| `corpus/knowledge/idle-lock-never-asked-r12.md` | sha256 `21c1d06db35d189b62f0ecaa098f97ac0d282e39422d5d19662caf83c05dd2e1`, 2078 B | **two further edits:** `7f27ced0…4dd58`, 3586 B, 60 lines, E1/E2 at line 42 → `0bcef21fc93fe32f5f926b21d4f6f9655ffb32bd41f49280b0c074fb4469c504`, 4344 B, **69 lines**, E3 at line 61, mtime `2026-10-25 03:41:38` | `wc -lc` / `sha256sum` / `stat` |
| `.ufo/…/fetch/S203.receipt.txt` | sha256 `1b7fa87…1646`, 3137 B | **unchanged** | `sha256sum` = anchor cell |

Every check was re-run against the current bytes after the rewrite: the S203 gate-quote is still
**exactly one** line, still the exact receipt tail (`line_matches_receipt_tail True`,
`receipt_has_quote 1`); the receipt sha still equals the anchor cell; `c1/count.py` →
`TARGET_MET`, EXIT=0. So A1/A3 survive the mutation and this report's verdict is against live bytes,
not the first snapshot.

**The errata did not propagate.** E1 withdraws "never toggled", yet the same file still asserts it in
three *unmarked* places:

- line 1 (H1): "…and the operator never toggled it afterwards"
- line 23 (§1 OBS): "And the operator never exercised the toggle afterwards (S204)…"
- line 29 (§2): "…and the toggle was never run in any session the journal still keeps."

By its own errata the entry's headline is false, and the headline is what downstream citations copy.
Fix in place (edit the three sites, or mark them withdrawn inline and move the errata to the top);
an append-only errata leaves a false title as the artifact of record.

**E3 makes this explicit rather than accidental.** The third edit (03:41:38) adds E3, which states in
its own words: "This entry's title reads '…and the operator never toggled it afterwards'; that clause
is withdrawn for the same reason as E1, and **the title is kept as landed rather than rewritten.**"
So the entry now *knowingly* carries a false H1 plus two unmarked false sentences (§1 line 23, §2
line 29), with the correction 40+ lines below. For an artifact of record that is the worst
arrangement: anything quoting the title, or reading only to line 29, inherits a withdrawn claim.
Require inline withdrawal markers at lines 1/23/29, or a status banner above H1.

E3 does earn two credits, both of which my own checks corroborate: it concedes that S204's `count: 12`
is a **re-count of S203's list, not an independent confirmation** (so "two independent negatives" was
never two), and it flags that §1's host fact "None of the twelve asks about the idle lock" is not
licensed by S203/S204 — neither receipt carries any script body — crediting wave-2 seat
`RevEntryR12`'s 13-file scan. My A2 independently reproduces that scan (`IDLE_ABSENT` across all 13
files), so the fact is true; only its provenance was missing.

**Why C1 cannot see any of this:** `frozen.json` has keys `id, predicate, target, entries, receipts`
only — there is **no registry hash and no entry hash**. Receipts are pinned by sha256; the registry
and the entries are not. The counter therefore recomputes `TARGET_MET` against whatever bytes are on
disk, so a scribe rewriting a row note or appending errata (including a new false "thirteen executed
items" clause) leaves the verdict untouched. That is precisely why `TARGET_MET` must be reported as a
quote/hygiene result and never as "the entries are true".

## Residual risk

- Drift is no longer only host-side. The host tree can change independently
  (`omarchy-first-run` @ sha256 `20508471…`), and the lane artifacts themselves moved during this
  review (S203 now `recheck: on-change`). Every live value is recorded above with its hash, so both
  are detectable by re-running the A1–A3 blocks.
- **Registry and entries are unpinned.** `frozen.json` pins receipt sha256 only (keys `id, predicate,
  target, entries, receipts`); there is no registry hash and no entry hash. `TARGET_MET` therefore
  follows mutable registry and entry bytes, which is why a sibling rewrite at 03:40:12 (including a
  new false "thirteen executed items" clause) left the verdict unchanged. Pin registry and entry
  hashes if the round needs C1 to certify anything beyond quote-contiguity.
- Low-3 means the S203 receipt cannot alone support any future sentence about "setup never
  configured the idle lock"; only about "setup never asked". Any later entry asserting the stronger
  form would be unsupported by S203's evidence.
- **Predicate-vs-truth gap (the round's main risk).** `c1/count.py` → `TARGET_MET` means "the three
  entries' gate-quotes are contiguous receipt substrings and the eight rows are registry-clean". It
  says nothing about whether the entries' claims are true. Entry r12's second conjunct is now
  contradicted (section above). Any wave-2 conclusion of the form "C1 met, so the idle-lock story
  holds" is unsupported by C1's own predicate.
- **Sender of the 19:24:38 SIGTERM is unrecoverable.** `systemctl is-active auditd` → `inactive`;
  no psacct/`/var/log/account/pacct`; zero audit records around the event; `~/.bash_history` is
  only 4572 B with 0 hits (an uninformative negative). So the *attribution* to the toggle is an
  inference from an exhaustive-exclusion signature, not direct proof. It is enough to destroy a
  "never" claim; it is not enough to assert the toggle was used.

## Verification gaps

- None of the three assigned checks is unverified; every verdict above quotes its command and exit code.
- `lsp` device not used: this seat performs byte/hash/grep verification of a text receipt against a
  host shell script, where no language server answers the artifact (no server registered for
  `.ufo/**` or `corpus/**`); text grep is the correct primitive here, and set-equality of the
  script sets was proven in python rather than asserted from grep counts alone.
- Not in scope, therefore not run: C2 (`c2/count.py`), the other seven rows, and the other two entries.
  The three entries' own internal consistency is other seats' assignment; this seat verified r12's
  S203 gate-quote line as the exact receipt substring, and additionally r12's S204 leg (contiguity +
  the truth of its inference) because that conjunct sits in the entry my row gates. Row S204's own
  receipt/anchor hygiene remains `L1Mado35.RevQuoteS204`'s assignment.
- The 19:24:38 attribution is an exclusion argument, not direct attribution; with auditd and psacct
  both inactive there is no process-accounting instrument that could close it. Reported as an
  inference, never as observed fact.
- **Scratch provenance.** The pre-sweep log was briefly lost (the `scratch/` tree moved to
  `scratch-evidence/` at ~03:45; the working-tree copy there is my later reconstruction) and was
  recovered from checkpoint `4efaf63`, blob sha256 `b5cc5c04…`, 4282 B / 87 lines. It is inlined
  verbatim in Appendix A, so no conclusion in this report depends on a file path surviving.

## Appendix A — evidence log (original measured bytes, inlined)

Source: `git show 4efaf63:.ufo/waves/round-35/scratch-evidence/RevQuoteS203/evidence.log`
(4282 B, 87 lines, sha256 `b5cc5c04e890aa06052f95860ad650070779ea29457c3f68c59b73d741d249d9`).
Verbatim; nothing edited.

```text
### A3 anchor
1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646  .ufo/waves/round-35/fetch/S203.receipt.txt
EXIT=0
1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646
EXIT=0
### A1 contiguity
count 1 offset 3033 words 14
EXIT=0
### A2 live facts
20508471d8237a60e630baf58f87c0b5a4391e34196ce11e5034745f6a062630  /home/vgpnk/.local/share/omarchy/bin/omarchy-first-run
EXIT=0
1089 /home/vgpnk/.local/share/omarchy/bin/omarchy-first-run
EXIT=0
13
EXIT=0
12
EXIT=0
12
EXIT=0
IDLE_ABSENT
EXIT=0
### C1 counter
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
EXIT=0

### CROSS-ROW S204: hook execution semantics
-- omarchy-hook-install body (27-29) --
mkdir -p "$HOOK_DIR"
cp "$HOOK_FILE" "$HOOK_PATH"
chmod 755 "$HOOK_PATH"
-- hook self-delete line 6 --
rm -f "$0"
-- installed hook still present --
-rwxr-xr-x 1 vgpnk vgpnk 174 Oct  3 17:48 /home/vgpnk/.config/omarchy/hooks/post-update.d/install-voxtype.hook
-- who dispatches --
# omarchy:summary=Run a named hook from ~/.config/omarchy/hooks/<name> and ~/.config/omarchy/hooks/<name>.d/.
RESULT: first-run executes 12, installs 1 hook; hook never ran

### ENTRY r12 SECOND LEG (S204) — vacuity + positive event
-- counter --
0
grep EXIT=1
-- toggle script has no journal primitive --
NO_LOGGING_PRIMITIVE
-- kill paths --
/home/vgpnk/.local/share/omarchy/bin/omarchy-restart-app:6:pkill -x $1
/home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle:6:  pkill -x hypridle
-- hypridle journal --
Oct 23 13:21:39 plazir27 systemd[1490]: Stopping hypridle...
Oct 23 13:21:39 plazir27 systemd[1490]: Stopped hypridle.
Oct 23 13:21:39 plazir27 systemd[1490]: app-Hyprland-hypridle-59197064.scope: Consumed 22.796s CPU time over 1d 8h 25min 52.144s wall clock time, 189.2M memory peak, 460K memory swap peak.
-- Boot e55f9cd9ec4e4dd5bf0ce775977af5a5 --
Oct 23 13:25:00 plazir27 uwsm_app-daemon[1838]: received: app -- hypridle
Oct 23 13:25:00 plazir27 uwsm_app-daemon[1838]: sent: exec systemd-run --user --scope --slice=app-graphical.slice --unit=app-Hyprland-hypridle-9408787a.scope --description=hypridle --quiet --collect --same-dir -- hypridle
Oct 23 13:25:00 plazir27 systemd[1529]: Started hypridle.
Oct 23 19:24:38 plazir27 systemd[1529]: app-Hyprland-hypridle-9408787a.scope: Consumed 2.783s CPU time over 5h 59min 38.213s wall clock time, 525.7M memory peak, 384K memory swap peak.
-- Boot 0a3785aac7104585a914f6cda41795a7 --
Oct 23 22:14:11 plazir27 uwsm_app-daemon[1805]: received: app -- hypridle
Oct 23 22:14:11 plazir27 uwsm_app-daemon[1805]: sent: exec systemd-run --user --scope --slice=app-graphical.slice --unit=app-Hyprland-hypridle-d4bd7533.scope --description=hypridle --quiet --collect --same-dir -- hypridle
Oct 23 22:14:11 plazir27 systemd[1493]: Started hypridle.
-- exclusions --
0
coredump_hits=1
pacman 2026-10-21 20
pacman 2026-10-22 2
pacman 2026-10-23 0
pacman 2026-10-24 22
pacman 2026-10-25 31
inactive
inactive

### CONCURRENT MUTATION OBSERVED
2026-10-25 03:40:12.893966805 -0300 171446 corpus/SOURCES.md
0bf117e2f472ec4f80adec17d58fe50b4fbd4fa9568ffa8523a4bfc272950d51  corpus/SOURCES.md
0bcef21fc93fe32f5f926b21d4f6f9655ffb32bd41f49280b0c074fb4469c504  corpus/knowledge/idle-lock-never-asked-r12.md
1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646  .ufo/waves/round-35/fetch/S203.receipt.txt
-- withdrawn claims still in place --
1:# The idle lock was never offered as a choice at setup, and the operator never toggled it afterwards
23:**OBS** And the operator never exercised the toggle afterwards (S204): the user
29:and the toggle was never run in any session the journal still keeps.
44:- **E1 - "never toggled" withdrawn.** Section 2's inference that the operator never
62:  reads "…and the operator never toggled it afterwards"; that clause is withdrawn for the
-- row 205 new note --
 The post-login questionnaire runs thirteen items, twelve of them first-run scripts - battery monitor, internal monitor, sudoers cleanup, firewall, DNS resolver, GNOME theme, swayosd, primary paste, text scaling, elephant, welcome and wifi - and none of the thirteen executed items asks about the idle lock 
recheck ' on-change '
-- C1 after mutation --
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
```

**Reading note on `coredump_hits=1`** (log line 63): that is the *exit status* of a
`grep -ci hypridle` that matched **0** lines, not a count of coredumps. The clean re-run in A2 prints
`NO_COREDUMP` for `coredumpctl list | grep -i hypridle`. Zero hypridle coredumps exist.
