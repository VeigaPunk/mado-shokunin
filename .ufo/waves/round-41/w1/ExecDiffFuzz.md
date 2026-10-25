# ExecDiffFuzz — differential fuzz: the C1 reference tool vs `PRED-C1-r41-v1`'s model

Round 41 (hyaku 7), inline v1 wave w1, lane `mado-shokunin`, base
`ab2bfaab661c846d1de9d58c01651cd156a13949`, freeze `60c3914154333180450d5da27ba222d5763cc56a`.
Seat dir: `.ufo/waves/round-41/w1/ExecDiffFuzz/`.

## What was run (exact commands)

```
# 1. the reference, copied byte-identically into the seat
cp .ufo/waves/round-41/c1/ctl-ref-tool.py.txt .ufo/waves/round-41/w1/ExecDiffFuzz/ref-tool.py
sha256 = 61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0   (both files)

# 2. the differential sweep (counter imported with importlib; main() never called)
cd .ufo/waves/round-41/w1/ExecDiffFuzz && python3 -I fuzz.py --jobs 8
#    -> fuzz-receipt.txt, fuzz-summary.json

# 3. contract-teeth probe: four re-implementations + the frozen counter's own score
cd .ufo/waves/round-41/w1/ExecDiffFuzz && python3 -I variants.py
#    -> variants/*.py, variants/*.counter.txt, variants/receipt.txt, variants/summary.json

# 4. harness sensitivity: the same sweep pointed at each variant (--tool)
python3 -I fuzz.py --quick --jobs 8 --tool variants/<name>.py
```

`fuzz.py` loads `quality/counters/c1-r41-globals.py` with
`importlib.util.spec_from_file_location(...); exec_module(...)` — `main()` is
`__main__`-guarded, so no counter code runs. It uses the counter's own
`model_out`, `model_sessions`, `gen_fixture`, `sample_journal`, `noise_lines`,
`advert`, `ts_of`, `MAX_BYTES`; the tool is always `python3 -I <tool> …` with a
minimal environment (`PATH`, `XDG_RUNTIME_DIR`), exactly as `run_sandboxed` does.

Seeds (13): the committed own-work journal `fetch/xdph-journal.txt` (19130 B,
sha256 `bf8fa91a…aaf7`), `gen_fixture(REV, NONCE, i)` for i=0..7 encoded exactly
as `score_gen` encodes them, `sample_journal` n=1,2,3, and a hand-built journal
holding every table name + `COMMON` in two sessions.

## Result 1 — tool vs model: **0 disagreements in 4843 mutants**

`fuzz: mutants=4843 disagreements=0`, `fuzz: live cases=26 disagreements=0`,
`fuzz: cli cases=23 contract-mismatches=0 ambiguous-mismatches=3`
(`fuzz-receipt.txt`). Mutation classes covered (each ≥ 12 variants unless noted;
the systematic sweeps are exhaustive over positions):

| class | how |
|---|---|
| byte flips / inserts / deletes | random offset, any byte, incl. 0x00 0xff 0xc3 0xed 0x80 0x0d 0x0a (156 each) |
| line deletion / duplication / swap | every line of 13 seeds (156 / 156 / 155) |
| CR / CRLF | one line, all lines, one CRLF in an LF file (156 each); plus a per-line CR sweep of a 75-line journal (76) |
| boot-line insertion | **every position** of the committed journal (154 split positions) and of the 75-line journal (76), plus duplicate boot ids (156) |
| pid flips | leading zero(s), trailing zero, digit substitution, strip trailing zeros (130) |
| version digits | `0`, `000001`, `999999`, `1000000`, `1234567`, `10`, Arabic-Indic `١` / `١٢` / `١٢٣٤٥٦` / `١٢٣٤٥٦٧` (156) |
| name length | 0, 1, 126, 127, 128, 129, 130 chars, with and without `--diff` (156 + 12) |
| invalid UTF-8 | lone `\xff`, `\xfe`, `\xc3`, CESU surrogate `\xed\xa0\x80`, truncated 4-byte `\xf0\x9f`, bare `\x80\x80` (156) |
| no trailing newline | last byte removed; a lone advert without `\n` (156 + 1) |
| boot-only files | 0..4 boot lines; upper-case id; 31-hex id; `-- Boot … ---` (156 + 4) |
| NUL bytes | inserted at every line of the 75-line journal (76), random offsets, space→NUL (156 + 156) |
| size boundary | exactly 8388608 B (parsed) and 8388609 B (`SETUP too_large`) |
| timestamp / host / spacing / prefix / suffix | `\d` vs ASCII, `Z` suffix, `+0300`, bad ranges, Unicode year, host with `[` `:` `é` `\x7f`, `[ERR]`, one/three spaces, `got`, trailing ` extra`, leading `x ` (156 each) |

28 random operators × 12 variants over 13 seeds = 4341 mutants, plus 502
systematic ones (every position, every line, the digit/length boundaries) =
**4843**.

Every mutant was compared on **rc + stdout bytes** against
`model_out(raw.decode("utf-8","replace"), expects, diff)`, with the
`--expect`/`--diff` argv drawn from 6 modes (none, `--diff`, present, present+
absent, duplicates, 128-char name), and stderr required empty on rc 0/1/3 —
i.e. exactly the counter's `judge`.

**Why zero is structural, not luck** (`fuzz-receipt.txt` line 4):
`advert-regex-identical=True boot-regex-identical=True table-identical=True` —
`ADVERT.pattern == ADV_RE.pattern`, `BOOT.pattern == BOOT_RE.pattern`,
`CLASS_OF == TABLE`, and the session loop, the `changed` flag, the `max()`
over versions, the `--diff` construction and the summary line read as the same
sentences in both files (checked: the two regex patterns and the two class
tables are equal; the rest is measured). The reference is a near-transliteration
of the model, so no input can separate them; the interesting question is
therefore whether the **contract text** the model encodes is itself pinned by the
fixture set.

## Result 2 — the contract text is under-determined in three places (measured)

`variants.py` builds four plausible re-implementations of the contract prose,
each differing in exactly one sentence, and scores each with the **frozen
counter itself** (`--repo . --rev 60c3914… --tool variants/<name>.py --nonce
difffuzzr41w1`; read-only, the counter writes only to its own tempfile):

| variant | one-line change | model vs variant on a 1–2 line journal | counter score |
|---|---|---|---|
| `ascii-digits` | `\d` → `[0-9]` (10 sites, ADV regex only) | model: `ver=12` from `(ver ١٢)`, rc 0 · variant: `NO_SESSIONS`, rc 3 | **fixtures=24/24 TARGET_MET** |
| `str-max` | `max(ent[1], ver)` → `if str(ver) > str(ent[1])` | model: `ver=10` · variant: `ver=9` | **fixtures=24/24 TARGET_MET** |
| `int-pid` | `cur["pid"] != pid` → `int(cur["pid"]) != int(pid)` | model: 2 sessions (`1952`, `01952`) · variant: 1 session, 2 interfaces | **fixtures=24/24 TARGET_MET** |
| `splitlines` | `text.split("\n")` → `text.splitlines()` | model: `NO_SESSIONS` on a CRLF advert · variant: 1 session | 22/24 MISSED (`gen3`, `nosess0`), selftest 46/47 |

Clause lines for the three admitted variants are `clauses=a:1 b:1 b2:1 g:1`
(`variants/*.counter.txt`), i.e. `TARGET_MET` by the counter's own final line.

**F1 (attacks `PRED-C1-r41-v1` discrimination, `str-max`).** Contract
(`quality/counters/c1-r41-globals.py:37`): "per distinct NAME: count and ver =
the highest N seen", and `:42` "MADO_GLOBAL: name=<name> ver=<max> …". The
model takes the *numeric* maximum; a lexicographic maximum is a defensible
reading of "highest" for a decimal string and is admitted. The fixture census
(`fuzz-summary.json` → `census`) shows why: every version the model accepts from
all 24 fixture journals (and from the committed journal) is a single digit —
`accepted_versions=[1..9], max_version_digits=1`. `gen4` is the "conflicting
versions" fixture and its versions are `randrange(1,10)`, so `max` on strings
and `max` on ints agree there. The 24 fixtures cannot tell the two apart.

**F2 (attacks `PRED-C1-r41-v1` discrimination, `int-pid`).** Contract
(`:34`): "its PID differs from the open session's PID". The model compares PID
*strings*, so `[1952]` and `[01952]` are two sessions. The census reports
`accepted_pids_with_leading_zero=[]`: the generators emit
`str(rng.randrange(100, 99999))`, so no fixture can distinguish string identity
from numeric identity.

**F3 (attacks the contract *text*, `ascii-digits`).** The contract writes the
timestamp as `TS = \d{4}-…` (`:29`) and the version as `\d{1,6}` (`:30-31`); in
Python `\d` is Unicode-aware, so `(ver ١٢)` is an advert with `ver=12` and
`٢٠٢٦-10-25T13:36:24-03:00` is a valid timestamp. Every NAME field in the same
contract is spelled `[A-Za-z0-9_]{1,128}` (`:20`, `:30`), i.e. ASCII — the text
is internally inconsistent about whether "digit" means ASCII. A tool written
with `[0-9]` (the natural ASCII reading, and the only thing `journalctl` output
can contain) passes 24/24 but reports `NO_SESSIONS` where the model reports a
session. No fixture contains a non-ASCII digit. A second consequence, from the
sweep (`fuzz-receipt-ascii-digits.txt`): a Unicode-digit *timestamp* is accepted
by the model and echoed verbatim into the report —
`first=٢٠٢٦-10-25T13:36:24-03:00` — so the model's stdout can carry bytes
outside ASCII, which `TS = \d{4}-…` never says and the tool's own docstring
("short-iso") excludes.

**F4 (positive: the CR rule *is* pinned).** `splitlines()` is killed by
`gen3` (noise-heavy: `advert + "\r"` lines) and `nosess0` (noise-only), and by
the tool's own selftest (46/47). The sentence "Lines are split on `\n`" (`:26`)
and "CR endings" in the ignored list (`:32`) have teeth.

## Repro (all three demos re-run for this report; from the seat dir)

```
T=$(mktemp -d)
# ascii-digits: version written with an Arabic-Indic digit (UTF-8 d9 a1)
printf '2026-10-25T13:36:24-03:00 h xdg-desktop-portal-hyprland[1952]: [LOG]  | Got interface: wl_seat (ver \xd9\xa1)\n' > $T/j1
python3 -I ref-tool.py               --journal-file $T/j1   # rc 0, "name=wl_seat ver=1 … verdict=OK"
python3 -I variants/ascii-digits.py  --journal-file $T/j1   # rc 3, "sessions=0 … verdict=NO_SESSIONS"

# str-max: 9 then 10 on the same name in one session
printf '…[1]: [LOG]  | Got interface: wl_seat (ver 9)\n…[1]: [LOG]  | Got interface: wl_seat (ver 10)\n' > $T/j2
python3 -I ref-tool.py        --journal-file $T/j2   # "name=wl_seat ver=10 count=2"
python3 -I variants/str-max.py --journal-file $T/j2   # "name=wl_seat ver=9 count=2"

# int-pid: 1952 then 01952
printf '…[1952]: … wl_seat (ver 1)\n…[01952]: … wl_shm (ver 1)\n' > $T/j3
python3 -I ref-tool.py        --journal-file $T/j3   # 2 sessions (pid=1952, pid=01952)
python3 -I variants/int-pid.py --journal-file $T/j3   # 1 session, interfaces=2
rm -rf $T
```

Observed diffs (verbatim `diff` hunks) are in the run that produced this
report; `variants/receipt.txt` carries the same three comparisons.

## Result 3 — CLI surface: 3 ambiguities the text does not decide, 0 hard violations

`fuzz-receipt.txt` → `CLI-AMBIGUOUS` (the first two rc 2 with one stdout line;
the third rc 0 with a census):

| argv | contract reading | reference |
|---|---|---|
| `--journal-file J --expect -x` | `:20` "a NAME must fully match `[A-Za-z0-9_]{1,128}`" → `SETUP bad_expect` | `SETUP usage` (argparse treats `-x` as an option) |
| `--journal-file ""` | flag given, path empty → `SETUP unreadable` | `SETUP usage` (`bool("")` is false) |
| `--journal-file "" --live --journalctl S` | `:19` "Exactly one of --journal-file/--live" → both given → `SETUP usage` | runs the live path and prints a census |

The third is the only one with a behavioural consequence: an empty
`--journal-file` value is treated as *absent*, so `--journal-file "" --live`
executes `journalctl` although the text says both flags were supplied. Nothing
in the 24 fixtures reaches any of the three (`usage0` and `badexpect0` use
`--expect=a b`, `--expect=`, a 129-char name, `a;b`, `a/b` and abbreviated
flags only).

## Result 4 — what the reference does *not* violate

Measured, not assumed (`fuzz-receipt.txt`, 23 CLI + 26 live cases):

- size: exactly 8388608 B parses, 8388609 B → `SETUP too_large` rc 2; the same
  boundary in `--live` (exactly 8 MiB parses, +1 → `SETUP journalctl_too_large` rc 5).
- `unreadable`: absent path, a directory, and a mode-000 file all → `SETUP unreadable` rc 2.
- a symlink to a journal parses (contract says "missing/unreadable", not "not a symlink").
- `--journal-file` mode spawns nothing: with a `journalctl` stub earlier on
  `PATH` that `touch`es a marker, the marker never appears.
- `--live` with a non-zero stub → `SETUP journalctl_failed` rc 5; group-writable
  stub → `SETUP journalctl_unusable` rc 5 and the stub is not run.
- stderr is empty on every rc 0/1/3 case in the sweep.

## Harness teeth (the negative is a measurement)

`fuzz.py --tool <variant>` re-runs the identical sweep against a known-wrong
tool; the disagreement counts and minimised inputs are in
`fuzz-receipt-<variant>.txt` / `fuzz-summary-<variant>.json`:

| tool under test | quick corpus | disagreements | one minimised input (bytes) |
|---|---|---|---|
| `ref-tool.py` (full corpus) | 4843 | **0** | — |
| `variants/splitlines.py` | 2673 | 438 | `…Got interface: wl_seat (ver 1)\r` (no `\n`) → want `NO_SESSIONS` rc 3, got 1 session rc 0 |
| `variants/ascii-digits.py` | 2673 | 27 | `…Got interface: wl_seat (ver \xd9\xa1)` (Arabic-Indic 1) → want `ver=1` rc 0, got `NO_SESSIONS` rc 3 |
| `variants/str-max.py` | 2673 | 6 | `(ver 9)` then `(ver 10)` → want `ver=10`, got `ver=9` |
| `variants/int-pid.py` | 2673 | 32 | `[1952]` then `[01952]` → want 2 sessions, got 1 |

So the sweep is sensitive to exactly the four sentences the variants change, and
it is silent on the reference over the same corpus. The 0 is a measured
negative, not a vacuous pass.

## Observation on the in-flight `PRED-C1-r41-v2` (not my scope, snapshot only)

While this seat ran, `quality/counters/c1-r41-globals-v2.py` appeared in the lane
(untracked, mtime 2026-10-25 20:26, sha256
`59e117d88c30fb7de44aa08e30d0d7ac5d4f7bcdeeacf3463b701871df4c3a63`) together with
`.ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt`. I fuzzed only the **frozen v1**
above; this paragraph is a read-only snapshot for the L1, and the file may change
under it. Importing v2 and calling its `model_out` on the three minimal journals
of Result 2:

- F3 is **closed** in v2: `(ver ١)` now yields
  `… ignored=1 verdict=UNRECOGNIZED` rc 4 (v1: `ver=1`, `verdict=OK` rc 0), i.e.
  v2 makes "digit" ASCII and counts the near-miss line.
- F1 and F2 are **unchanged** on those inputs: v2 still reports `ver=10` for
  `(ver 9)` then `(ver 10)`, and still reports two sessions for `[1952]` then
  `[01952]`; only the summary line differs from v1, by the new `ignored=` field.

Whether v2's *fixture set* pins F1/F2 is not something this snapshot answers; the
two variants (`variants/str-max.py`, `variants/int-pid.py`) are the direct probe
if v2 keeps a `--tool` path.

## Files written (all inside the seat dir)

- `fuzz.py` — the harness (`--tool`, `--quick`, `--jobs`).
- `ref-tool.py` — the reference, sha256 `61f101ae…30f0` (identical to `c1/ctl-ref-tool.py.txt`).
- `fuzz-receipt.txt`, `fuzz-summary.json` — the reference sweep (4843 mutants, 26 live, 23 CLI).
- `variants.py`, `variants/` — the four variants, their minimal demos, their
  frozen-counter transcripts (`variants/<name>.counter.txt`), `variants/receipt.txt`,
  `variants/summary.json`.
- `fuzz-receipt-splitlines.txt`, `fuzz-receipt-ascii-digits.txt`,
  `fuzz-receipt-str-max.txt`, `fuzz-receipt-int-pid.txt` (+ the matching
  `fuzz-summary-*.json`) — sensitivity runs.
- `verify_quotes.py`, `quotes-receipt.txt` — 15/15 quotations verified in place
  (file, line window, ≤ 25 words).

No file outside this seat dir was written. Tool installs: none (system
`python3` 3.14.8; `bwrap` was used only by the frozen counter's own sandbox).
The four `--tool` counter invocations are read-only measurements: the counter
writes only to its own `tempfile.mkdtemp` and reads the lane through
`git show`/`rev-parse`; the official counter run stays with the L1.
