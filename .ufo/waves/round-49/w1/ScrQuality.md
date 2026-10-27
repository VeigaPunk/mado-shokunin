# ScrQuality — candidate QUALITY criteria 100+ (mado round 49, wave w1)

Status: **DONE**. Draft only: this seat lands no criterion and edits no tracked file. Base
`03e4ae76aff7a4be59cb69970dd553baa319695a`; QUALITY.md ends at 99
(`grep -oE '^[0-9]+\. ' corpus/QUALITY.md | tr -d '. ' | sort -n | tail -1` → `99`), so the numbers
below are the next five and are the L1's to reassign.

Deliverable: `.ufo/waves/round-49/w1/ScrQuality/criteria.md` — five criteria, one per uncaptured class the
dispatch names (host-write by a mutant; a receipt field whose name misdescribes its value; a text receipt that
drops rows its summary holds; an instrument's coverage envelope narrower than its registry wording), plus M48-13
(a dispatched cap must survive the recipe it caps, extending criterion 98). Each carries the lesson locator, a
runnable `Check:` and a red state **observed in this seat**, not asserted.

## 1. Result per criterion

| # | class | attacked / supported | red state observed |
|---|---|---|---|
| 100 | host-write by a wave writer | `corpus/lessons/round-48.md:263` (M48-10); `mkmutants.py:31` builds a target from ambient `HOME` and `:39`/`:40` write it | `WRITE_OUTSIDE_SANDBOX … path=<operator cache>` → `CHECK100: modes=1 violations=1 verdict=FAIL` (receipt `:10`); the source screen reads `AMBIENT_HOME_WRITE_SITE … home_read=27 write=38` (`:34`) |
| 101 | receipt field whose name misdescribes its value | `lessons/round-48-verifier-spotcheck.md:178` (N2); `receipts/live-terminal-cache-r48.txt:4` | `STATE_FIELD … name=host_cache_untouched_sha256 token=untouched comparator=none`, `FIELD_VALUE_IS_PAYLOAD … sha256=c8b104e6…` → `verdict=FAIL` (`:46`); that digest is `sha256('r48-w2\n')`, recomputed here |
| 102 | a text receipt that drops rows its summary holds | `lessons/round-48-verifier-spotcheck.md:185` (N4) | `TEXT_DROPPED id=a-rev-base-direct`, `TEXT_DROPPED id=a-entry-at-base`, `TRAILER_COUNT text=98 json=98` → `json_ids=98 text_rows=96 … verdict=FAIL` (`:68`) |
| 103 | envelope narrower than registry wording | `corpus/lessons/round-48.md:259` (M48-8); `SKILL.md:770`; `quality/check-session-material.py:1606` (`default="ufo"`) | `SCOPE_UNSTATED … gate_default=ufo wording=repo` (`:79`), `ENVELOPE: … shapes=21 caught=3 missed=18 blind=18 verdict=NARROWER` (`:105`) |
| 104 | a dispatched cap vs the recipe it caps | `corpus/lessons/round-48.md:269` (M48-13); `.ufo/waves/round-48/a4r1-results.json:40` | `CAP_RECIPE: cap=1048576 recipe=clone blobs=22278 blobs_over=24 max_blob=4207542 … verdict=INCOMPATIBLE` (`:163`); probe receipt rc=128 |

Green arms exist for all five (receipt lines `:16`, `:29`, `:52`, `:60`, `:74`, `:110`, `:132`, `:169`): a real
strace of a scratch-only writer, an unchanged operator-state pair, a corrected field name, a state field that
carries its before pair, a total projection generated from the same summary, a registry row that states
`--scope` and declares `blind-spots=`, and a cap above every tracked blob with a `PROBE rc=0` receipt.

Each criterion carries a "not a restatement of" line with the existing criterion's computed locator — 89 vs 100
(89 bounds the *scored tool inside* the counter; M48-10's write came from a seat's own unsandboxed mutant run),
19/63 vs 101, 37/78/87 vs 102 (both artifacts are internally consistent), 93/30/33 vs 103, 98/61/64 vs 104 (the
round-48 cap *was* executed and still broke the recipe).

## 2. Gates run in this seat

| gate | command | observation |
|---|---|---|
| instrument battery, 14 runs | `bash .ufo/waves/round-49/w1/ScrQuality/run-instruments.sh` | `exit=1` at receipt lines 11, 24, 37, 47, 69, 106, 164; `exit=0` at 17, 30, 53, 61, 75, 133, 170 — every red/green pair has the polarity its criterion predicts |
| quote verification (self-applied, criterion-77 shape) | `python3 -I …/verify-quotes.py --criteria …/criteria.md --receipt …/receipts/criteria-red.txt` | `VERIFY_QUOTES: checked=15 supported=15 verdict=OK`, exit 0 (`receipts/verify-quotes.txt`) |
| locator verification | `python3 -I …/verify-locators.py --lane .` | `VERIFY_LOCATORS: checked=29 missed=0 verdict=OK`, exit 0 (`receipts/locators.txt`) |
| current criterion ceiling | `grep -oE '^[0-9]+\. ' corpus/QUALITY.md | tr -d '. ' | sort -n | tail -1` | `99` |
| peer numbering collision | `grep -rln 'criterion 10[0-9]\|^10[0-9]\. ' .ufo/waves/round-49/` (excluding this seat), 2026-10-27T01:45:28-03:00 | no match: no other round-49 seat had drafted a 100+ criterion at that time |
| N4 cross-check against a peer | `.ufo/waves/round-49/w1/ExecN4Matrix.md:9-10` | independent seat reports the same pair: frozen text 96 rows, summary 98, the same two ids missing — agreement, not shared bytes |

## 3. Touched surfaces

Written, all inside `.ufo/waves/round-49/w1/ScrQuality/` (untracked; the L1 commits) plus this report:

- `criteria.md` (18 016 B) — the deliverable;
- `check100-hostwrite.py` (8 541 B), `check101-fieldname.py` (4 944 B), `check102-textprojection.py` (4 312 B),
  `check103-envelope.py` (5 198 B), `check104-caprecipe.py` — seat prototypes of the lane instruments the criteria
  name, each with `--help` / docstring limits;
- `run-instruments.sh` (5 759 B) — the battery; derives the lane root with `git rev-parse --show-toplevel`, so no
  absolute lane path is committed;
- `verify-quotes.py`, `verify-locators.py` — the two self-checks above;
- `fixtures/` — `trace-incident.txt` (synthetic, reconstructed from M48-10, labelled as such), `trace-scratch-writer.txt`
  (real strace, 38 lines, masked to `<SCRATCH>`, zero `/home/` matches), `opstate-{before,after,same}.txt`,
  `receipt-fixed-field.txt`, `receipt-backed-state.txt`, `matrix-total.txt`, `probe-{ok,fail}.txt`. Every fixture carries
  `<OPHOME>`/`<SCRATCH>` placeholders; the only `/home` token in the seat dir is the shape `/home/U`;
- `receipts/criteria-red.txt` (14 289 B), `receipts/verify-quotes.txt`, `receipts/locators.txt`.

Largest file produced: `criteria.md`, 18 016 B (criterion 98's bound is 64 MiB; the largest produced anywhere in
this seat is the 14 289 B receipt).

Not touched: no tracked file, no `quality/` instrument, no `corpus/`, no `SKILL.md`, no `QUALITY.md`, no git/jj
index, no `.ufo/state/`, no watchdog log, no fleet-root file. No `hyprctl` read, no compositor verb, no `xkbcli`
run, no process launched except `bash`/`git`/`python3`/`strace` inside this seat's own scratch.

## 4. Host safety and scratch

- The operator cache still reads `ddd94f6bca4bcd42c426da9bbeb9955ca5d77b8778b4e290fcfffcc984a1b3d5` after every
  run — the round-49 before digest (`.ufo/waves/round-49/receipts/operator-state-before.txt:3`), so nothing I ran
  wrote it. The mutant-source read under `/home/U` is a fixture *class*, never the real path.
- Scratch `/fast/scratch/hyaku/mado-r49/ScrQuality` was created, used for the real trace and the `check103` fixture
  repo (toplevel asserted before the only commit), and **removed** (`trap` plus an explicit check: the directory is
  gone; sibling seats' scratch dirs were untouched).
- Every writer shell ran under `ulimit -f 65536`; `HOME`, `XDG_CACHE_HOME`, `XDG_CONFIG_HOME`, `XDG_DATA_HOME`,
  `XDG_STATE_HOME` pointed inside scratch for the instrument runs; the real trace was taken with `env -i`.
- No tool was installed or upgraded this seat (nothing was needed: `python3` 3.14.8, `git`, `strace` and `bwrap`
  were already present).

## 5. Out of scope / not claimed

- No lane instrument landed (`quality/check-*.py` do not exist); criterion 64's pre-dispatch path check applies to
  whichever the L1 lands.
- No discovery attack frozen before the instruments were written — criterion 33 is w2's work; the fixture populations
  here were authored by the same seat as the criteria, so these are seat instruments (provenance, not credit under 25).
- No counter, no predicate, no score: this seat ran no frozen instrument and does not claim any axis.
- `104` is offered as an extension; if the L1 reads it as the same class as 98 the remedy is an appended sentence,
  not a new number.

## 6. Findings that outlive the criteria

1. **N2 reproduces mechanically** — the field name asserts a state the value contradicts, and the value is the
   mutant's own 7 bytes. The receipt is 36 lines and carries no before field, so a reader had nothing to compare.
2. **N4 reproduces exactly** — 98 summary ids, 96 text rows, trailer 98; the two dropped ids are the two the
   round-48 spot-check named. A peer seat repaired the artifact the same round; the criterion is the general rule.
3. **M48-8 reproduces larger than reported** — the attacking JSONL holds 21 shape rows (19 scanned + 2 outside
   `.ufo/`), the gate catches 3, and the registry row declares none of the 18 it misses and omits `--scope`.
4. **M48-13 is a compatibility defect, not a discipline lapse** — 24 tracked blobs exceed 1 MiB at the round-48 base,
   the largest 4 207 542 B (`.ufo/waves/round-20/w2/CorpusRuntime/full-sweep.jsonl`), so a clone under the a4r1 cap
   could not complete for any seat that checked out a worktree.
5. **The two failure classes are separable** — N2's artifact is internally consistent and N4's text is internally
   consistent; both escaped the criteria that recompute *inside* one receipt. That is the reason 101 and 102 are
   cross-artifact rules.

## 7. Conflicts for the judge

- Numbering: I propose 100-104 in the dispatch's class order; no other round-49 draft used those numbers at
  01:45:28, but seats were still live.
- 104 vs 98: recorded as an extension with its reason; the L1 may fold it into 98.
- The `103` blind-spot count (18) exceeds SentPrivacy's prose (16 of 19) [inference: the JSONL adds the two
  out-of-scope comparison rows to the 19 scanned files; its own non-row line prints `files=19 missed=16`].
