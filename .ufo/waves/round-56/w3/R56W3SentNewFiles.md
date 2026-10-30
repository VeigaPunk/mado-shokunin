# R56W3SentNewFiles — security scan of the round's surfaces at 0f3a5436

Scope attacked: (1) secret shapes over `corpus/knowledge/hyprland-config-autoreload-r56.md`,
`tools/mado-watchplan.py`, the w3 deliverable directories and `.ufo/waves/round-56/attempt2/`;
(2) the tool's output-injection escape table and the w2 budget fixes, re-derived at
`0f3a54361a9824484d0801679ceb1fd8ac7c32e1`.

Everything was read from the scored revision (`git archive 0f3a5436…` into scratch) and from the
filesystem; the lane working tree was never scored and no lane file was edited. Deliverables:
`.ufo/waves/round-56/w3/R56W3SentNewFiles/receipts/sentinel-a2.txt` (per-check verdicts, commands
and outputs) and `.ufo/waves/round-56/w3/R56W3SentNewFiles/probes/` (the six probe scripts).

Verdicts in one line each: **secret shapes — no credential material of any shape** (F1/F2 fixed
patterns 0 hits; generic op://, AKIA, private key, GitHub/Slack/JWT, PEM all 0; the 9,683 long-token
hits triaged into four benign classes with nothing unexplained). **Escape table — the w2-named
hostile inputs are closed, but a residual injection survives** (S5c below). **Budgets — the event and
read budgets hold; the watch-line output does not** (S6c below).

---

## F1 — UNESCAPED INJECTION via U+2028 / U+2029 / U+0085 (blocking the escape table)

**What I attacked.** The w2 F2 fix landed at the tip: `tools/mado-watchplan.py:81-92` adds
`esc()`, and every printed path goes through it (`Plan.show`, :204-207), as does every echoed
source text (`event_error`, :222); the `via=` field is escaped at creation (:281), `config=` uses
`show()` (:361), the watch lines use `show()` for `path=` and the pre-escaped `via=` (:366). Call-site
coverage is complete. I attacked the escape table's **character class** instead.

`esc()` escapes `o < 32`, `o == 127` and the surrogate-escape range `0xDC80..0xDCFF`. It leaves
everything else unchanged — including three characters that Python's `str.splitlines()` treats as
record separators: **U+2028** (LINE SEPARATOR), **U+2029** (PARAGRAPH SEPARATOR) and **U+0085** (NEL).
It also leaves the C1 control range `U+0080..U+009F` (including U+009B, CSI) and the bidi controls
(U+202E) raw.

**Exploit path.** A config line, or a file name reached by a `source =` glob, carrying U+2028 /
U+2029 / U+0085 followed by the text `MADO_WATCH: DONE watches=0 unsupported=0 errors=0 live=NONE`
is printed by the tool with the separator intact. The raw byte stream is still one physical record
(every `0x0a` in stdout is a record terminator, and every physical line starts with `MADO_WATCH`),
but any consumer that decodes stdout as text and splits with `str.splitlines()` — the ordinary
Python idiom, and the one the lane's own harnesses use elsewhere — reads back a **second, forged
`MADO_WATCH: DONE` record** with attacker-chosen counters.

**Input that shows it** (all outputs in `receipts/probe-injection.out`,
`receipts/unicode-residual.out`, `receipts/nel-forge.out`, `receipts/forged-done-refined.out`):

```
P4, a file named "u<U+2028>sep<U+202E>rev<U+2029>end.conf":
    U+2028 (LINE SEPARATOR) rc=0 splitlines_pieces=5 bad_pieces=1
       BADPIECE 'sep.conf type=file mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW via=$ROOT/hyprland.conf:1'
    consumer_split_on_U+2028_pieces=2 (stdout lines=4)
unicode probe:
    U+0085 (NEL)  rc=0 splitlines_pieces=5 bad_pieces=1
       BADPIECE 'nel.conf type=file mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW via=$ROOT/hyprland.conf:1'
    U+202E (RLO)  rc=0 splitlines_pieces=4 bad_pieces=0   (raw in stdout)
    U+001C (FS)   rc=0 splitlines_pieces=4 bad_pieces=0   (escaped: <32)
    U+000B (VT)   rc=0 splitlines_pieces=4 bad_pieces=0   (escaped: <32)
refined forge, config line
  source = /nope/a<U+0085>MADO_WATCH: DONE watches=0 unsupported=0 errors=0 live=NONE<U+0085>X
    rc=0  physical_lines=4  splitlines_pieces=6  DONE-looking(splitlines)=2
       DONE 'MADO_WATCH: DONE watches=0 unsupported=0 errors=0 live=NONE'      <- forged
       DONE 'MADO_WATCH: DONE watches=1 unsupported=0 errors=1 live=NONE'      <- real
  (identical with U+2028 instead of U+0085; and the same shape through a file NAME)
```

**Impact.** A consumer that reads "the DONE line" or counts DONE records gets the wrong value —
the same consequence w2 F2 named, re-opened through a byte the escape table does not cover. The
C2 harness compares raw bytes and is not fooled; the committed fixtures cannot detect it (no
committed fixture name contains a control or non-ASCII byte:
`find .ufo/waves/round-56/fixtures/c2 -printf '%p\n' | LC_ALL=C grep -P "[^\x00-\x7f]"` → no match).
The tool's own selftest cannot detect it either: it asserts on the tool's internal `lines` list
(`check("every printed line starts MADO_WATCH", all(l.startswith("MADO_WATCH") for l in lines))`,
:434), which is the pre-split list, not a re-split of the rendered bytes.

**Severity: blocking the escape table.** Not blocking C1/C2/C3 themselves — the frozen predicates
and the byte-exact harness are unaffected (verified below) — but the w2 F2 remediation is
incomplete, and the item names an unescaped injection as blocking.

**Smallest remediation.** Widen `esc()` to the Unicode line/paragraph separators and the C1 range —
e.g. escape every `ch` for which `str.isprintable()` is False, or add `0x85`, `0x2028`, `0x2029` and
`0x80..0x9F` to the existing test — and add a selftest assertion that no rendered record splits
under `str.splitlines()`.

---

## F2 — watch-line output is not budgeted (weakens)

**What I attacked.** w2 F3 said the event and watch output were unbounded and the read budget was
absent. The tip added `MAX_EVENTS = 100000` and `MAX_TOTAL_BYTES = 64 MiB` (both enforced, both named
in the docstring's divergence list item (8)). The event half is closed; the **watch** half is not:
`MAX_EVENTS` bounds event lines only, the number of watch lines is bounded only by `MAX_ENTRIES`
(262144), and each watch line's length is unbounded (a glob match under a deep directory yields a
long path).

**Input that shows it** (`receipts/watchline-amplification.out`, `receipts/bigcap-measure.out`,
`receipts/nearcap-exact.out`):

```
50,001 entries, 3.7 KB paths: stdout 187.5 MB, peak RSS 735 MB, 8.4 s
   -> amplification stdout/config = 1011x   (config was 185,400 bytes)
243,001 entries, 3.7 KB paths: stdout 911.5 MB, peak RSS 3512 MB, 35.1 s, rc=0
   tail 'MADO_WATCH: DONE watches=243001 unsupported=0 errors=0 live=NONE'
252,901 entries (config 1,043,072 B, just under MAX_BYTES): stdout 948.7 MB, peak RSS 3655 MB, 59.0 s, rc=0
   -> at MAX_ENTRIES the same shape gives ~983 MB of stdout
```

**Impact.** A ~1 MB config still drives ~1 GB of stdout and ~3.6 GB of peak RSS from one tool
invocation — the same class w2 F3 reported, reduced but not closed. (For contrast, the event half is
now capped: 300 dirs × 400 source lines → `MADO_WATCH: SETUP too_large`, stdout 28 bytes, peak RSS
24.5 MB, where w2 measured 411.9 MB stdout and 1442 MB RSS.)

**Severity: weakens the claim** (cost / resource exhaustion, not a wrong answer). **Smallest
remediation:** count watch lines against a budget as well, or cap the printed path length, and fail
with `too_large`.

---

## F3 — wave-3 evidence re-publishes a real host monitor serial (weakens, privacy)

**What I attacked.** The lane's own privacy gate over the wave-3 deliverable tree.

```
python3 -I quality/check-session-material.py --repo <staged w3 repo> --rev HEAD --scope ufo
FINDING file=.ufo/waves/round-56/w3/R56W3RevLiveBoundary/receipts/boundary-a2.txt rule=R5_SERIAL_PROSE count=8 detail=tokens=8 shapes=9x3+Ax5+9x4
SESSION_MATERIAL: files=147 findings=1 rev=5f12a518...
```

The token is the host's real LG ULTRAWIDE monitor EDID serial (shape 7 digits + 5 capitals + 4
digits; the value is not reproduced here), copied verbatim 8 times into
`R56W3RevLiveBoundary/receipts/boundary-a2.txt` from `corpus/knowledge/hyprctl-verification-layer.md`
— which the same gate already flags at the tip
(`FINDING file=corpus/knowledge/hyprctl-verification-layer.md rule=R5_SERIAL_PROSE count=1`). The
gate's own rule text (`quality/check-session-material.py:158`) says a real serial "can never be
waived — only removed or redacted", and `--no-waivers` gives the identical one finding.

**Severity: weakens** (privacy). **Pre-existing condition, not a w3 novelty:** the same serial is
already committed in the corpus at the tip and is already flagged there — the tip's own gate run is
`findings=274` (323 without waivers), exit 1, with 52 R5 findings. The w3 file adds 8 fresh
occurrences. **Smallest remediation:** redact or drop the serial from the w3 receipt before it is
committed, and separately address the corpus copy.

---

## F4 — host identity in wave-3 receipts, outside the gate's rules (weakens, privacy/low)

The gate's `R8_ACCOUNT_COLUMN` rule only matches `ls -l` data rows, so host identity carried in
other shapes is invisible to it. Measured in the w3 tree:

* `R56W3RevWatchTable/receipts/journal-pid1622.txt` (52 lines) and
  `journal-hypr-filtered.txt` (41 lines) — the host's own systemd journal, every line carrying the
  account name and the live Hyprland instance signature
  `efb50993780079460b0cbed1363e2166a2de1d9f_1793027319_436109330` (build pin + start time +
  compositor PID).
* `R56W3RevProcFdinfo/sample.json` — `summary.identity` is the compositor's `ps` row
  (`  1622  1000 Mon Oct 26 12:08:38 2026  3-13:55:21 Hyprland`), plus 40 watched paths with their
  inode and device numbers, plus the kernel inotify `f_handle` hex strings.

No window titles, no client dumps, no foreign host's instance signature. **Severity: weakens**
(privacy, low) — and **pre-existing lane-wide**, not a w3 novelty: the same instance signature is
already in 7 tracked files at the tip (`git grep -l "1793027319_436109330" 0f3a5436`), and the
account name in 232 (`git grep -l "plazir27" 0f3a5436`).

---

## F5 — text outside the display root is echoed (low, pre-existing; w2 F8 unchanged)

```
config sources a file OUTSIDE --display-root; that file's own `source =` RHS is echoed:
  MADO_WATCH: ERROR via=/fast/.../outside.conf:1 source=TOKEN-XYZ-outside-root reason=nomatch
  token echoed: True
```

Only the RHS of a `source =` line is printed, so no credential leaks; but it is text from outside the
declared root. Unchanged from w2 F8. **Severity: low. Smallest remediation:** print the RAW only for
`bogus`/`nomatch` on lines of the config tree itself, or drop RAW from ERROR lines.

---

## Checked, no defect found (null results, with the command that found nothing)

* **The lane's three fixed secret patterns** (`tools/mado-tripwire.py:301-305`): URL-userinfo **0**,
  AWS-AKIA **0** over all four surfaces (462 files). The long-token pattern fired 9,683 times and
  was triaged, not counted: every distinct value resolves to a lane git object id, a sha256/sha1 of a
  tracked blob, a context-labelled digest, a public upstream project commit, or a kernel hex handle —
  **nothing left unexplained** (`receipts/hex-classification.out`).
* **Generic shapes**: `op://` **0**, `AKIA` **0**, `BEGIN … PRIVATE KEY` **0**, GitHub PAT **0**,
  Slack token **0**, JWT **0**, PEM certificate **0**. Credential-shaped *assignments* with
  non-placeholder values: **2**, both inspected and both false positives (a harness token variable
  and the word "pass" in a docstring) — `receipts/cred-assign.out`.
* **The w2-named injection input** (ASCII newline in a file name forging a `MADO_WATCH: DONE` line)
  is closed at the tip: `DONE_lines=1`, `lines_not_starting_MADO_WATCH=0`, newline shown as `\x0a`;
  ESC, BEL and non-UTF-8 bytes likewise escaped.
* **The w2-named over-long path** is bounded, not truncated mid-record: a 200,000-character source
  path echoes whole (max stdout line 200,079 bytes), and the 1 MiB worst case stays at
  `max_line=1,000,072` because `MAX_BYTES` caps the config at 1 MiB. The source-text echo cannot
  exceed the read budget (a 1 MiB file sourced 100 times → `SETUP too_large`, stdout 0.0 MB).
* **Event budget** (`MAX_EVENTS`): 300 dirs × 400 source lines → `SETUP too_large`, 28 bytes stdout,
  24.5 MB peak RSS.
* **Read budget** (`MAX_TOTAL_BYTES`): 80 matched 1 MiB files → `SETUP too_large`; a 60 MiB total
  completes normally.
* **The tool's own selftest at the tip**: `MADO_WATCH_SELFTEST: 86/86 assertions passed`, rc 0.
* **Fixture replay**: byte-exact against all 26 committed and hold-out fixtures with the tip tool —
  `committed 18/18, holdout 8/8` (`receipts/c2-fixture-replay.out`); the escaping and budget fixes
  changed no frozen output.
* **The lane's C2 harness at the tip** (read-only scratch clone):
  `sandbox=bwrap fixture_commit=ok control_scores={'const-host': (1, 0), 'empty': (0, 0),
  'sibling-reader': (0, 0), 'lookup-committed': (18, 0)}` →
  `MADO_R56_C2: … fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET`, rc 0.
* **w2's blocking F1 is closed**: with the harness copy patched to `_BWRAP = None` it now fails
  closed — `r56_ctl_c2: setup error: bwrap is not installed: the staged layout alone does not hide
  the answer key; pass --no-sandbox to run anyway`, rc 2 (the lane file was not modified).
* **Frozen-table digests re-verified at the tip, no drift**: `frozen-tables-v2.json`
  `9511151a…795e2` and `c3-name-only.tsv` `70653e09…48ee` both equal their declared values; the
  attempt-2 draft's two fetched-byte digests
  (`98fe7feb…d6d` = 11,345 B, `f9e12387…d8a1` = 14,694 B) match the bytes in
  `.ufo/waves/round-56/fetch/` on disk.
* **No credential material in any file this seat wrote** (the receipt redacts every token value).

## Could not verify

* The no-bwrap path on a real host without bwrap — F1's remediation was checked by patching a
  **copy** of the harness in scratch, not by hiding bwrap on the host.
* F2's ~983 MB figure at exactly `MAX_ENTRIES` is an extrapolation; the measured points are
  911.5 MB / 3512 MB at 243,001 entries and 948.7 MB / 3655 MB at 252,901 entries.
* Whether a real operator config tree reaches these fan-out scales — all my fixtures are synthetic.
* The gate's own classification of the R5 serial is inherited from the lane's rule; I did not
  re-derive whether that serial is genuinely the host's live monitor (the shape and the source file
  are established; the value was not read out).

## Tools installed or updated

None. No pacman, uv, npm or cargo transaction was attempted; the host-wide pacman pause was
respected. Everything ran on the pre-existing `/usr/bin/python3` (3.14.8) with `python3 -I`.
