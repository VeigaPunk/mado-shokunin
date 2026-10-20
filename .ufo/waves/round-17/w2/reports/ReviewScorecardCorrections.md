# ReviewScorecardCorrections — round-17 wave 2 (FALSIFY)

Seat: `MadoR17.ReviewScorecardCorrections` (reviewer, leaf).
Scope: `SCORECARD.md:867-895` (`### Round-17 pre-measurement corrections`)
against the commits and receipts named there. Lane HEAD
`988b858bd6049bc709807534fd725c05264f7e60`.
Read-only throughout; **install: none**. No pacman/yay/paru/sudo/systemctl/
hyprctl/loginctl/journalctl/libinput/evtest/compositor/input/screenshot
operation of any kind. Mutations: none — scratch only in `/tmp`.

## Findings (by severity)

### Low — F1: "baseline stays 2/6 under both (receipts)" is not bound by the two receipts

SCORECARD.md:880-881 says "Stricter only; baseline stays 2/6 under both
(`evidence/measure-before.json`, `measure-instrument.json`)." The
measurement itself is correct — I reran both instrument revisions against
the declared baseline and both give 2/6 (see E6). The defect is in the
evidence binding, not the number:

- The two receipts differ only in `rev`/`commit`:
  `measure-before.json` is rev `27cd06f`, `measure-instrument.json` is rev
  `f52f43f8ea44f60b3c52e5cc5b2e5ab76d77be59`. `diff` of the files differs
  on exactly lines 3-4.
- Neither file carries an instrument identity. Output keys are only
  `schema, rev, commit, c1, c2, c3`; there is no `measure.py` digest field.
- At both receipt revisions the **two instrument revisions emit byte-identical
  JSON** (`cmp` of old@27cd06f vs new@27cd06f; old@f52f43f vs new@f52f43f),
  and each receipt is byte-identical to *both* instruments' output at its
  rev (`measure-before.json` == old and == new @27cd06f;
  `measure-instrument.json` == old and == new @f52f43f, run with the full
  sha). The receipts therefore cannot attest that the tightened
  (`ab0bc9b`) instrument was run against the baseline; that property is
  only checkable by rerunning, which I did: both revisions give
  `c2.count 2`, `score 3.3333`, provinces `P1,P2`, `rejected []`,
  `u_routes 7`.

This is the same class of defect criterion 23 (the round's own new
QUALITY rule) targets: a receipt cited for a property it does not itself
record. Action: emit the generating instrument's sha256 in the output
(e.g. `instrument_sha256` = blob hash of `measure.py` at the running
revision), or cite the exact `measure.py` revision used per receipt.
Severity Low because the claim is true and reproducible, and because
`measure-instrument.json` is at `f52f43f`, whose corpus is byte-identical
to `27cd06f` (`git diff 27cd06f f52f43f -- corpus/knowledge corpus/SOURCES.md
corpus/QUALITY.md` is empty), so either reading of "under both" is
consistent with the bytes.

### Low — F2: "13 non-lane runs" — the count is exact, the actor label is an inference

SCORECARD.md:892-895: "`/var/log/pacman.log:2440-3152` shows 13 non-lane
runs on 2026-10-20 07:45-09:39 (including `pacman -Syu`), none after
round launch."

Verified exactly (`/var/log/pacman.log`, 3160 lines total):

- 13 `[PACMAN] Running` lines inside 2440..3152, at lines
  2440, 2448, 2454, 2461, 2462, 3064, 3085, 3091, 3092, 3125, 3126,
  3132, 3152. First `07:45:36-0300`, last `09:39:21-0300`; all on
  2026-10-20.
- `pacman -Syu --needed --noconfirm nvme-cli smartmontools fio xfsprogs
  pacman-contrib earlyoom iotop-c sysstat stress-ng btrbk linux-lts
  linux-lts-headers` at line 2462, `09:15:30-0300`.
- No `[PACMAN] Running` line after 3152 anywhere in the file; the file's
  last timestamp is also `09:39:21-0300` (lines 3153-3160 are that
  transaction's hooks). Round launch is `0175f13` at
  `2026-10-20T10:56:28-03:00` (the round session directory starts
  `2026-10-20T12-57-31-587Z` = `09:57:31-0300`); the last run is before
  both. So "none after round launch" holds under either launch reading.

The label "non-lane" is not a fact the log carries: pacman.log records no
actor. The corroborating material is Mado-only and does not cover the
label as stated:

- `tripwire-pacmanlog-join.txt:2`'s window is
  `awk '/^\[2026-10-(19T2|20T0[0-6])/ && /\[PACMAN\] Running/'` — it
  excludes 07:45-09:39 entirely; its "0 tripwire pacman transactions
  without a log line" applies to the four pre-07:45 transactions only
  (lines 2410, 2422, 2423, 2429).
- `tripwire-r16.txt` scans 97 files, 97/97 named `MadoR16*`; counts
  `host_mutation 0, package_query 2`. `tripwire-r17-w1.txt` scans 70
  files, 70/70 `MadoR17*`; `host_mutation 0, package_query 0`. So the
  byte evidence shows no *mado* lane ran these; sibling-lane attribution
  is outside the scanned corpus (the join receipt itself records a
  MoriR13/MoriR14 mention for the 01:07 man-pages run).

Action: say "13 runs with no host_mutation finding in the scanned Mado
r16/r17-wave-1 transcripts" (or "non-mado-lane"), or append an erratum.
Severity Low: it does not touch the load-bearing host-pause conclusion
(none after launch), and the 07:45-09:39 command set (yay elephant
packages, `-Syu`, `fwupd`, `go`, removals) is consistent with operator
work.

### Info — F3: "the red anchor is the single file" wording

The anchor tuple is verified: `tripwire-anchor-r15.txt` scans one file
(`MadoR15/MadoR15.LibinputEvents.jsonl`, sha256
`78388d42…a7c74f`), exit 1, two `host_mutation` findings both at line 54
(rules `sudo` and `pacman:-S`), timestamp `2026-10-20T07:25:16.905Z`;
my independent `--scan` of that file reproduces the receipt byte-for-byte.
The independent oracle confirms the tuple, including `call_38165`
(`oracle-r15.json` → `red_anchor.hit`).

But the round-15 directory scan has a second `host_mutation` file:
`MadoR15.ReviewDocsEra.jsonl:50` (`sudo -n true`, rule `sudo`;
`tripwire-r15.txt` counts `host_mutation 3`). So "the single file" must be
read with the finding-tuple qualifier; it is not uniqueness across round
15. Suggested wording: "single-file anchor scan". Info only.

### Info — F4: "2/6 = 3.3333"

`2/6 = 0.3333`; `3.3333` is `10*count/6`, the instrument's score field.
The convention is used consistently elsewhere in SCORECARD, but the
sentence conflates fraction and score. Info.

## Attacks attempted and outcome

| # | Attack | Result |
|---|---|---|
| E1 | Instrument digests | **Failed to falsify.** `git show f52f43f:.ufo/waves/round-17/measure.py \| sha256sum` = `a280b3ab7c4dc21a25a954056f6a0c55187fd84dc06cfcddcb28e7f897d3508e`; `git show ab0bc9b:… \| sha256sum` = `4023124fa40931f630197920e2534f468dc2b1cacfe010826b52032db846466b`. Prefixes `a280b3ab…` / `4023124f…` are exact; HEAD's file is the `4023124f…` blob. |
| E2 | `measure.py` absent at `0175f13` | **Failed to falsify.** `git cat-file -e 0175f13:.ufo/waves/round-17/measure.py` → `fatal: path … exists on disk, but not in '0175f13'`; the commit's tree only carries `SCORECARD.md` and `evidence/census-start.txt`. |
| E3 | "bound before any note integration" | **Failed to falsify.** Note commits `0175f13..HEAD -- corpus/knowledge` = only `a9998d1`; commit times `f52f43f 11:11:09`, `ab0bc9b 11:11:36`, `a9998d1 11:11:52`, `fc6f960 11:12:41` (all -0300). `git diff 0175f13 f52f43f -- corpus/knowledge corpus/QUALITY.md corpus/SOURCES.md` is empty. |
| E4 | Tightening description | **Failed to falsify.** `git diff f52f43f ab0bc9b -- …/measure.py` shows exactly T2 exact `surface:` fullmatch + MALFORMED reject, T3 `LEGACY_PATHS` pin, T4 `SURFACE_KEYWORDS` relevance on source+scope cells, T5 `FACET_MIN_LINES=3`. Registry indices check out (`row[4]=tier`, `row[8]=status`, `row[11]=used-by`, 13-cell split). |
| E5 | "Stricter only" | **Failed to falsify.** Statically each change adds a rejection on the same per-entry path, so new-accepted ⊆ old-accepted. Empirically `python3 -I` old and new instruments over `27cd06f,0175f13,f52f43f,ab0bc9b,a9998d1,fc6f960,3722ba4,245fd11,3e9848a,988b858`: every revision identical between instruments (counts 2,2,2,2,4,4,4,4,4,4; sets `P1,P2` then `P1,P2,P4,P6`; `rejected []` everywhere). New never exceeds old. |
| E6 | Baseline 2/6 under both | **Failed to falsify.** old@27cd06f and new@27cd06f both: `c2.count 2`, `score 3.3333`, `P1,P2`, `rejected []`, `u_routes 7`; `c1 22/14 6.3636`; `c3` absent. `measure-before.json` is byte-identical to both outputs. |
| E7 | Receipt reproduction | **Passed.** `measure-c1.json` (rev `3722ba4…`, 23/15), `measure-c2.json` (rev `a9998d1…`, 4/6), `measure-c3.json` (rev `HEAD`) reproduce byte-for-byte from HEAD's instrument; `measure-before.json` reproduces from both instruments; `measure-instrument.json` reproduces from both at its full-sha rev. |
| E8 | pacman.log 2440-3152 | **Count/window/-Syu/none-after-launch exact; "non-lane" not falsified but not log-carried** — see F2. |
| E9 | C3 pins | **Failed to falsify.** `--selftest core` 9/9 exit 0, `compound` 16/16 exit 0, `hardening` 33/33 exit 0. Anchor `--scan` reproduces `tripwire-anchor-r15.txt` byte-for-byte: exit 1, `host_mutation 2` at line 54, rules `sudo` and `pacman:-S`, ts `07:25:16.905Z`; oracle `red_anchor` confirms `call_38165`. `/var/log/pacman.log:2429` = `04:25:16-0300` `pacman -S --needed --noconfirm libinput libinput-tools`, transaction completes at 2437; `07:25:16Z` conversion is right. |
| E10 | C1 attribution | **Failed to falsify.** `git diff 27cd06f 3722ba4 -- corpus/QUALITY.md` = 15 insertions, 0 deletions; exactly one new `^[0-9]+\. ` line (criterion 23, lesson citation on the numbered line); `grep -n tripwire corpus/QUALITY.md` empty; no QUALITY change after 3722ba4 (`git log 3722ba4..988b858 -- corpus/QUALITY.md` empty). Literal 15/23 reproduces; block counter (17/22→18/23) is reported in `w2/reports/ReMeasureC1.md` §4 (peer, non-canonical). |
| E11 | U-route 7/7 unchanged | **Failed to falsify.** round-17 instrument `u_routes 7` at 27cd06f and 988b858; round-16 instrument `coverage.count 7` at 988b858. |

## Residual risk and verification gaps

1. **The tightening has zero differential coverage.** Both instrument
   revisions emit byte-identical JSON on every committed round revision,
   and `rejected` is `[]` at all of them — no corpus entry triggers any of
   the four new gates. "Stricter only" is therefore a code-level subset
   property (which I checked), not a demonstrated red/green behavior. If
   the round wants a falsifiable test in the same style as the R16-V1
   label check, add a fixture the old instrument accepts and the new one
   rejects (e.g. `surface: P4 (terminal)` → MALFORMED, or a section with
   two body lines → facet floor).
2. **No instrument identity in any measure receipt** (F1). A reader must
   rerun to distinguish instrument revisions; the claims survive that
   rerun, but the receipts are not self-identifying.
3. **"non-lane" is not evidenced for sibling lanes** (F2). The scanned
   tripwire corpus is Mado-only by construction (97/97 `MadoR16*`, 70/70
   `MadoR17*`), and the join window ends at `T06`. The host-pause
   conclusion rests on "none after launch", which does hold.
4. **Host state.** `R15-V1` current state remains `[UNK]`; nothing in the
   readable bytes settles it, and I did not probe the host.
5. **Transcript provenance.** My item does not name the MadoR17 session
   transcripts, so I did not read them; which receipt was generated by
   which instrument revision is inferred from commit times,
   `w1/reports/MeasureBuild.md`, and byte equality — not from the
   authoring transcript.
6. Nits: "single file" anchor phrasing (F3); `2/6 = 3.3333` notation (F4).

No frame-breaking counterexample was found in the corrections block: the
digests, the absence claim, the binding order, the tightening description,
the 2/6 baseline under both instrument revisions, the 13-run log window,
the -Syu line, "none after round launch", the selftest counts, the anchor
tuple and the 2429-2437 join all reproduce exactly.
