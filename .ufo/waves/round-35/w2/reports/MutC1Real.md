# MutC1Real — mutation test of PRED-C1-r35-v1 against the real tree

Seat: `L1Mado35.MutC1Real` (mutation-tester, leaf, no dispatch). Round 35, wave 2.
Lane repo (read-only): `/home/vgpnk/Projects/shokunin/mado-shokunin`
Scratch: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/scratch/MutC1Real/`
Target: `PRED-C1-r35-v1` — `.ufo/waves/round-35/c1/count.py`, `c1/frozen.json`, `c1/clauses.json`.
Installs/upgrades: **none** (Python 3.14.8 stdlib only; host kernel 7.2.11-arch1-1).

**One-line result.** All ten live clause ids are **verdict-dead when the real tree is the only
test**: 11/11 single-clause counter mutants still print `TARGET_MET` with unchanged counts
(exit 0). All ten are **individually live** when the real bytes are mutated instead: 10/10
one-clause data mutants are killed (`TARGET_MISSED`, exit 1). The real tree therefore witnesses
none of its own clauses — only the synthetic control trees do. Six further calibration defects
are reported in §6 (F2–F6, F9).

## 1. Isolated copy and baselines

Copy, no clone (the counter needs only `corpus/`, the receipts and `c1/`):

```
mkdir -p scratch/MutC1Real/root/.ufo/waves/round-35
cp -a corpus                      scratch/MutC1Real/root/corpus
cp -a .ufo/waves/round-35/fetch   scratch/MutC1Real/root/.ufo/waves/round-35/fetch
cp -a .ufo/waves/round-35/c1      scratch/MutC1Real/root/.ufo/waves/round-35/c1
```

Snapshot identity (`scratch/MutC1Real/lane-snapshot-v2.sha256`, taken 03:40:45, verified stable
across the copy — the copy loop retries if the lane moves mid-copy, and it did once):

```
0bf117e2f472ec4f80adec17d58fe50b4fbd4fa9568ffa8523a4bfc272950d51  corpus/SOURCES.md
7f27ced01e9edf627e2e4693ec57663fa14dd739cd8f9065cf177d0bfae4dd58  corpus/knowledge/idle-lock-never-asked-r12.md
583c708c338ecb063f8ef38071d415c79476088f27994551fd964384be1e0bf3  corpus/knowledge/idle-lock-chain-armed-r14.md
82c08a4675863f69e0905b02810cae6299cdfe3038fb1255172f7b44f91fadfe  corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
78c2589286a2d70c9b109672c85cd4e9bcb85438bc80ab888d10b73ad12abad6  .ufo/waves/round-35/c1/count.py
e18e7aef81e78fc385b3fa9d524a6c875182273517d65d97bb94c463b7743b30  .ufo/waves/round-35/c1/frozen.json
f0f1f8a09f62b80efd522d79b040f7c17a3f7df4e36876d3a271d8acaa1834e4  .ufo/waves/round-35/c1/clauses.json
1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646  fetch/S203.receipt.txt
4cd5ba6518e4a6d950fcb510d2482e33be78abb20d22bef41d21a66f7d1c54ad  fetch/S204.receipt.txt
f3387bfcbac79016034be38bab6548ae31df5860e5aafaa03105aca84b08ae1a  fetch/S205.receipt.txt
1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5  fetch/S206.receipt.txt
81c33e7926f0bad071d31e9fc67e1d06967e3142da40ea3c93b16510b0adec59  fetch/S207.receipt.txt
6e72f0db3d7bbfecf4096b0aa22f716f417c00caa50b6d3319106387d6ce4654  fetch/S208.receipt.txt
a170c7a50b9305b3448fc85ecddb0d7b1f1c3ff5e42c78cdc2d07718c3bdd27c  fetch/S209.receipt.txt
ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726  fetch/S210.receipt.txt
```

Fidelity: all 15 lane files above are byte-identical to their scratch copies (`sha256` compared;
the eight receipt digests also equal `frozen.json`'s `receipts[*].sha256`). The counter copied
verbatim as `counter-pristine.py` (`78c2589286a2d70c…`).

**Lane movement during the probe (not mine; two waves of sibling edits).**

1. 03:25:52 — my first copy. At 03:35:08/03:35:30 sibling wave-2 seats appended
   `### Errata (round 35, wave 2)` sections to all three knowledge entries. Appends only; no
   `gate-quote:` line touched; counter result unchanged. Snapshot v1 taken 03:35:49.
2. ~03:39 — `corpus/SOURCES.md` rows S203–S205 were edited: S203 and S204 recheck cells
   `on-request` → `on-change`; S204's and S205's row-prose cells corrected (S205 now reads "one
   start line", was "two start lines"). None of the four cells the predicate inspects on those
   rows (anchor digest, status, used-by, and the recheck *validity class*) changed in a way that
   affects the verdict. Snapshot v2 taken 03:40:45; C1 on the live tree still `TARGET_MET`,
   exit 0.

**Every run reported below is against snapshot v2**, and the complete 28-run matrix was also run
against v1 with identical verdicts, counts and exits. v1 hashes are kept as
`lane-snapshot-v1.sha256`, my pre-errata copy as `lane-before.sha256`. The recheck mutant reads
its anchor token from the row at run time (it is `on-change` in v2), so the driver re-runs
against later lane states without silently mutating a stale string.

Detector invocations (one command, three baseline/recovery points):

```
$ python3 -I .ufo/waves/round-35/c1/count.py \
    --root /home/vgpnk/Projects/shokunin/mado-shokunin \
    --frozen /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET      (exit 0)  # live lane
$ python3 -I counter-pristine.py --root scratch/MutC1Real/root --frozen scratch/MutC1Real/root/.ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET      (exit 0)  # snapshot, before arms
# same command after all 28 mutant runs, pristine root untouched:
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET      (exit 0)  # restored
```

## 2. Method, and why the literal arm cannot decide anything

The assigned probe has two readings; both were run because only one of them can discriminate.

**Arm A (literal).** For each live clause id, drop exactly one clause in `count.py` — code only;
`PREDICATE` and `frozen.json` left untouched, so the `predicate-drift`/`target-drift` guards do
not fire and the mutant is a counter that is *weaker than its own frozen spec*. Run it against
the pristine real bytes.

**Arm B (data side).** For each live clause id, violate exactly that clause in a fresh copy of
the real bytes (one logical artifact changed per arm — verified in §7) and run the pristine
counter unchanged. This is the arm that can attribute a verdict to a clause: a failure here can
only come from the data violating the predicate, never from a weakened check.

**Why Arm A is degenerate here.** The baseline is `TARGET_MET`. Dropping a conjunct can only
turn a failing cite into a passing one; it can never turn a passing cite into a failing one, so
a clause drop on data that already satisfies every conjunct cannot change the verdict. The
measured result is exactly that: **11/11 Arm-A mutants print `TARGET_MET`, exit 0, counts
`[3,8,0]`** (the 11th, `entry-metric`, is the derived-metric probe of F2). Arm A therefore
reports every clause as "verdict-dead on this data" by construction — and that uniformity is
the finding: with the real tree as the sole test, no clause weakening is detectable.

**Arm C (2×2 attribution).** Each Arm-A counter is also run against the corresponding Arm-B
tree. If the data mutation failed only that clause, `A+B` must restore `TARGET_MET`. 8/10 do;
the two exceptions are themselves findings (§6, F6).

## 3. Result table

Requested polarity, quoted from the tasking: *"still TARGET_MET = clause is verdict-dead on this
data / TARGET_MISSED = live."* Column A is that literal probe; column B is the discriminating
complement.

| clause id | A: drop clause, real bytes | B: real bytes + 1 clause violation | A+B | requested label (A) | clause actually failable on real bytes? (B) |
|---|---|---|---|---|---|
| `entry-regular` | **TARGET_MET** `[3,8,0]` exit 0 | **TARGET_MISSED** `[2,6,2]` exit 1 | TARGET_MISSED | verdict-dead | **live** (needs 3 guards dropped, see F6) |
| `row-unique` | TARGET_MET `[3,8,0]` exit 0 | TARGET_MISSED `[2,7,1]` exit 1 | TARGET_MET | verdict-dead | **live** |
| `row-well-formed` | TARGET_MET `[3,8,0]` exit 0 | TARGET_MISSED `[2,7,1]` exit 1 | TARGET_MET | verdict-dead | **live** |
| `used-by-exact` | TARGET_MET `[3,8,0]` exit 0 | TARGET_MISSED `[2,7,1]` exit 1 | TARGET_MET | verdict-dead | **live** |
| `status-mined` | TARGET_MET `[3,8,0]` exit 0 | TARGET_MISSED `[2,7,1]` exit 1 | TARGET_MET | verdict-dead | **live** |
| `recheck-valid` | TARGET_MET `[3,8,0]` exit 0 | TARGET_MISSED `[2,7,1]` exit 1 | TARGET_MET | verdict-dead | **live but weak** (F5) |
| `digest-match` | TARGET_MET `[3,8,0]` exit 0 | TARGET_MISSED `[2,7,1]` exit 1 | TARGET_MET | verdict-dead | **live** |
| `gate-quote-substring` | TARGET_MET `[3,8,0]` exit 0 | TARGET_MISSED `[2,7,1]` exit 1 | TARGET_MET | verdict-dead | **live but weak** (F4) |
| `gate-quote-word-bound` | TARGET_MET `[3,8,0]` exit 0 | TARGET_MISSED `[2,7,1]` exit 1 | TARGET_MET | verdict-dead | **live** (26 vs 25) |
| `o-nofollow-open` (declared not-load-bearing) | TARGET_MET `[3,8,0]` exit 0 | TARGET_MISSED `[2,6,2]` exit 1 (via `st_nlink!=1`) | TARGET_MISSED | verdict-dead | dead as declared; **not inert** (F6) |

Reading: under the tasking's literal label, **10/10 live clauses are verdict-dead on the real
tree**, and §6 F1 reports them as such. The right-hand column shows this is a property of the
*test set* (one real tree, already all-green), not evidence that the clauses are vacuous: each is
individually killable with a one-artifact mutation of the same bytes.

Detector-run totals: 28 runs, 14 `MET` / 14 `MISSED`. Only three count triples ever occur —
`(3,8,0)`, `(2,7,1)`, `(2,6,2)` (F2).

## 4. Per-clause evidence

Every mutation below is one logical artifact (§7 manifests). Commands are
`python3 -I <counter> --root <tree> --frozen <tree>/.ufo/waves/round-35/c1/frozen.json`.

**`entry-regular`.** Arm A removes both path guards in `read_regular`
(`if stat.S_ISLNK(st.st_mode):` → `if False:`; `if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:`
→ `if False:`; counter `66e5b81c…`). Real bytes: `TARGET_MET`, exit 0. Arm B replaces the r12
entry with a symlink to a byte-identical `.real` copy → `TARGET_MISSED closed_entries=2
closed_rows=6 open_cites=2`, exit 1 (both its cites fail). A+B → **still MISSED**: `O_NOFOLLOW`
is what catches the symlink once the walk is gone (F6). Verdict-dead under A; live under B.

**`row-unique`.** Arm A: `rows[0] if len(rows) == 1 else None` → `rows[0] if rows else None`
(`682e8fab…`) → MET. Arm B duplicates the S205 row verbatim → `TARGET_MISSED [2,7,1]`, exit 1.
A+B → MET.

**`row-well-formed`.** Arm A: `nf_ok = len(cs) == 11` → `nf_ok = True` (`af5a2e12…`) → MET.
Arm B appends a 12th cell to the S206 row (`…r15.md | extra |`), leaving the used-by token set
intact, so only this clause fails → `TARGET_MISSED [2,7,1]`, exit 1. A+B → MET. The clause is
thus separable from `used-by-exact` on real data (the counter's `if nf_ok` guard does not force
a second failure).

**`used-by-exact`.** Arm A: `and used_by == citing` → `and True` (`352c083b…`) → MET. Arm B adds
`, corpus/knowledge/idle-lock-chain-armed-r14.md` to S207's used-by cell → `TARGET_MISSED
[2,7,1]`, exit 1. A+B → MET.

**`status-mined`.** Arm A: `and cs[7] == "mined"` → `and True` (`b48ef12e…`) → MET. Arm B sets
S203's status cell to `queued` → `TARGET_MISSED [2,7,1]`, exit 1. A+B → MET.

**`recheck-valid`.** Arm A: `and valid_recheck(cs[9])` → `and True` (`f2240ced…`) → MET. Arm B
sets S204's recheck cell (currently `on-change`) to `2026/Q1`; the anchor token is read from the
row at run time → `TARGET_MISSED [2,7,1]`, exit 1. A+B → MET. Note F5: the clause is live only
against tokens that begin with a non-letter or contain punctuation.

**`digest-match`.** Arm A: `and receipt["sha256"] in cs[5]` → `and True` (`20285091…`) → MET.
Arm B mutates S208's anchor digest (`…ce4654` → `…ce4650`, one hex digit, right length) →
`TARGET_MISSED [2,7,1]`, exit 1. A+B → MET. A wrong *but correct-length* digest is caught, so the
`in`-substring test is not merely a length test. (The row's other digest, the source file's
`d196b086…`, is left untouched — the mutation targets only the receipt digest.)

**`gate-quote-substring`.** Arm A: `and quote.encode() in blob` → `and True` (`48629166…`) → MET.
Arm B replaces the S209 quote with a 13-word plausible paraphrase absent from the receipt
(`four dated copies of the bar's configuration each carry the idle-lock handler`, verified absent
byte-wise) → `TARGET_MISSED [2,7,1]`, exit 1. A+B → MET.

**`gate-quote-word-bound`.** Arm A: `and 1 <= len(words) <= 25` → `and True` (`b78b976e…`) → MET.
Arm B sets S203's quote to the first **26** whitespace tokens of the receipt's 64-word body line
(`body-joined: #!/bin/bash  # omarchy:summary=Finish the installation of Omarchy with items that
can only be done after logging in. # omarchy:requires-sudo=true  set -e  FIRST_RUN_MODE=~/.local/state/om…`):
still a byte-contiguous substring, exactly 26 words → `TARGET_MISSED [2,7,1]`, exit 1. A+B → MET.
This is the sharp case the r34 predicate could not produce: the bound is **independently failable
on real receipt bytes** without also failing the substring test.

**`o-nofollow-open`.** Arm A: `os.O_RDONLY | os.O_NOFOLLOW` → `os.O_RDONLY` (`063d6654…`) → MET.
Arm B: no static witness exists for the flag alone — a symlinked entry is already rejected by the
`S_ISLNK` walk (measured: Arm-A-o-nofollow counter × the symlinked-entry tree → `TARGET_MISSED
[2,6,2]`, exit 1, same as the pristine counter), and a hardlinked entry (`nlink=2`) is rejected by
`st_nlink != 1` before `open()` (`TARGET_MISSED [2,6,2]`). The declaration in `clauses.json` is
therefore operationally correct. It is not inert, though: strip the walk and the flag alone
decides the verdict —

```
walk removed (S_ISLNK→False, S_ISREG/nlink guard→False), symlinked entry, O_NOFOLLOW kept:
PRED-C1-r35-v1 closed_entries=2 closed_rows=6 open_cites=2 verdict=TARGET_MISSED   exit=1
same counter with O_NOFOLLOW removed:
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET      exit=0
```

See F6 for the wording the round-36 declaration needs.

## 5. Extra probes (not in the assigned table)

| probe | mutation | detector | exit | meaning |
|---|---|---|---|---|
| undeclared clause: quote uniqueness | duplicate S203's `gate-quote:` line | `TARGET_MISSED [2,7,1]` | 1 | the predicate's "exactly one gate-quote line" is **live and load-bearing**, but has no clause id and no control (F3) |
| undeclared clause: receipt regularity | replace `S206.receipt.txt` with a symlink | `TARGET_MISSED [2,7,1]` | 1 | `blob is not None` is **live and load-bearing**, unnamed (F3) |
| evidence strength | S203 quote → the single word `the` | `TARGET_MET [3,8,0]` | 0 | **survivor**: both quote clauses are satisfied by one common word (F4) |
| symbolic cadence (`valid_recheck`, called directly) | — | `some day maybe`→True, `review whenever we feel like it`→True, `when the mood strikes`→True, `never`→True, `next sprint/when free`→False, `2026/Q1`→False, `TBD!`→False | — | prose passes; only punctuation or a non-letter first char fails (F5) |

F5 cross-check against the committed control: `controls/c1-recheck-prose.txt` records
`TARGET_MISSED` via S209's cell `90d - re-verify the fetch` — which fails because it **starts
with a digit** and carries ` - `, not because it is prose. The control name overstates what it
covers.

## 6. Findings for round 36

**F1 — every live clause is verdict-dead on the real tree; the acceptance criterion has no
discriminating power.** Dropping any one of the ten live clauses (Arm A) leaves the command
printing `closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`, exit 0 — 11/11
mutants survive. The ten are `entry-regular`, `row-unique`, `row-well-formed`, `used-by-exact`,
`status-mined`, `recheck-valid`, `digest-match`, `gate-quote-substring`,
`gate-quote-word-bound`, `o-nofollow-open`. The mechanism is worth stating because it also
weakens the drift guard: `predicate-drift` compares `frozen.json`'s `predicate` string against a
hand-copied `PREDICATE` constant, so a counter whose `ok`/`read_regular` logic has been weakened
still passes the drift check and still reports `TARGET_MET`. Round 36 must keep the per-clause
control receipts as the *only* clause witnesses and must not describe the real-tree run as
exercising them; if the gate wants the real run to carry clause evidence, it needs per-clause
counters printed (see F2), not one aggregate verdict.

**F2 — the target triple is arithmetically one-dimensional.** Each of the 8 cites increments
exactly one of `closed_rows`/`open_cites`, so `closed_rows + open_cites ≡ 8` on every run; and
for this frozen spec (each entry carries ≥1 cite, and an unreadable entry fails its own quotes)
`closed_entries == 3 ⟺ open_cites == 0`. Consequence: `closed_rows == 8 ⟺ open_cites == 0` and
`closed_entries == 3 ⟺ open_cites == 0`, so the conjunction carries **one bit**, and the printed
triple reports only *how many* cites failed, never *which clause*. Measured over all 28 runs:
`rows+open=8` always, `entries==3 ⟺ open==0` always, `verdict == (open==0)` always, and only
`{(3,8,0),(2,7,1),(2,6,2)}` occur. A review gate that reads the triple as three independent
checks is reading noise. Either print per-clause failure counts / failed cite ids, or replace
the derived counters with independent ones.

**F3 — two live, load-bearing behaviours are not enumerated in `clauses.json`.** (i) *exactly one
`gate-quote:` line per id* — duplicating the S203 line flips the verdict to `TARGET_MISSED`
(measured); the predicate text states it, no clause id or control does. (ii) *receipt
regularity/readability* — `blob is not None`; a symlinked `S206.receipt.txt` flips the verdict
(measured); the predicate text does not state it at all. Add both as clause ids with controls
(or delete the requirement). This matters for the C2 census: an `uncovered=0` reading that walks
`clauses.json` cannot see either, so `uncovered=0` does not mean "every enforced check has a
witness".

**F4 — the gate-quote clauses bound length, not evidentiary content.** With S203's quote replaced
by the single word `the` (1 word, byte-present in the receipt) the counter prints `TARGET_MET`,
exit 0. The observed legitimate quotes are 13–17 words (S203 14, S204 13, S205 17, S206 13,
S207 15, S208 14, S209 13, S210 15), so the `1..25` window lets a near-vacuous quote through
with 24 words of headroom. Round 36 should raise the lower bound (the corpus's own floor is 13)
and/or require the quote to contain the id's distinguishing token (`S203`/`S204`/… does not
appear in the quote, so the token must come from the row).

**F5 — `recheck-valid`'s symbolic branch accepts arbitrary prose.** `valid_recheck` returns True
for `some day maybe`, `review whenever we feel like it`, `when the mood strikes`, and `never`;
it returns False only for non-letter-leading or punctuated tokens (`2026/Q1`, `TBD!`,
`next sprint/when free`). The rule is documented as "the census's own rule
(`scripts/sources-census.sh: E09`)" — if that is intended, the clause name and the control name
(`c1-recheck-prose`) overstate what is enforced. Either enumerate the symbolic vocabulary as a
closed set (the lane's rows use `on-change`, `on-release`, `on-request`, `on-gate-change`,
`on-session-change`, `on-capture-change`, `on-compositor-release`,
`on-operator-recovery-decision` and `NNd`/ISO) or rename the clause.

**F6 — `entry-regular` is a three-point enforcement, and `o-nofollow-open` is its redundant
half, not a separate TOCTOU-only concern.** The `entry-regular` property is enforced by the
`S_ISLNK` component walk, the `S_ISREG or st_nlink != 1` final-component test, and the
`O_NOFOLLOW` open. The Arm-A drop of the two `lstat` tests still leaves the symlink caught by
`O_NOFOLLOW` (`A+B` for `entry-regular` is `TARGET_MISSED` `[2,6,2]`). The `clauses.json`
declaration's operational claim holds — with the walk in place, dropping the flag changes no
verdict (measured) — but "TOCTOU-only defence in depth" is the wrong description: the flag is the
static backstop for the *same* symlink, and it alone flips the verdict once the walk is removed
(§4, `walk removed` pair). Round 36 can keep the not-load-bearing accounting, but should record
it as "redundant with the S_ISLNK walk on static trees; race-relevant only for TOCTOU", and must
not delete either guard believing the other covers a different attack. Also note
`st_nlink != 1` — part of this clause's enforcement — is unnamed in `clauses.json` (F3).

**F7 — the bound and the substring test are separable on real bytes (positive result).** The
26-word quote built from S203's 64-word body line is a byte-contiguous receipt substring and
fails only `gate-quote-word-bound` (`TARGET_MISSED [2,7,1]`, A+B → `MET`). The r34 complaint that
the bound was dead code does not recur in r35.

**F8 — no finding against the one-clause-per-artifact arms.** Each of the 13 data mutants changes
exactly one logical artifact (§7), and 8/10 clause mutants are fully explained by their own
clause (A+B restores `MET`); the two exceptions are F6, not contamination.

**F9 — C1 constrains identity metadata, not the row's claim.** `ok` reads only `cs[5]` (contains
the receipt digest), `cs[7]` (status), `cs[9]` (recheck class) and `cs[10]` (used-by); cells 1–4,
6 and 8 (description, source kind, grade, relevance, claim/quote text, date) are never read. A
material correction to a row's own prose is therefore invisible to C1: during this wave sibling
seats changed S205's row from "two start lines" to "one start line" and rewrote S204's relevance
and claim cells, and the counter still printed `TARGET_MET` both before and after
(`corpus/SOURCES.md` `848a7680…` → `0bf117e2…`, same verdict). So `TARGET_MET` must not be read as
"each row's claim agrees with its receipt": that leg rests on the entry's single `gate-quote`
line per cite, and the row's own prose and date are uncertified. Round 36 should either certify
the claim cell (e.g. the existing row→receipt substring discipline) or state explicitly that C1
covers identity metadata only.

## 7. Integrity, scope and reproduction

- **Restoration and concurrent lane edits.** I never wrote to the lane: every write of mine is
  under `scratch/MutC1Real/` plus this report. The 15 artifacts under attack were identical to
  `lane-snapshot-v2.sha256` at the end of the run series. After that, sibling seats kept editing
  the lane (03:43:18 check: 14/15 still match; `corpus/knowledge/idle-lock-never-asked-r12.md`
  grew 3586 → 4344 bytes by appending errata, last write 03:41:38). The live predicate state was
  re-checked at 03:43:18: `PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0
  verdict=TARGET_MET`, exit 0. The appended bytes start with the snapshot bytes verbatim and the
  two `gate-quote:` lines are byte-identical, so the v2 matrix still describes the
  predicate-relevant live state.
  Scratch contents (2002 files, 37 MB): `root/` (pristine v2 snapshot), `arms/A-*/count.py`
  (11 mutants), `arms/B-*` and `arms/C-*` (13+2 data trees), `counter-pristine.py`, `driver.py`,
  `run.log`, `results.json`, `verify-deltas.json`, `lane-before.sha256`,
  `lane-snapshot-v1.sha256`, `lane-snapshot-v2.sha256`. No `git`/`jj` command was run against the
  lane; the Git index and jj state are untouched.
- **One artifact per mutant (verified by full-tree manifest diff).** Of the 13 B arms, 11 change
  exactly one path; the two symlink arms change two paths each (a byte-identical `.real` copy plus
  the link) — one logical artifact. Both C arms carry the same single entry-symlink change. The
  hardlink arm is content-identical to the original entry (`sha256 7f27ced0…` both sides) and is
  identified by `nlink=2` — recorded as `hardlink (nlink=2)` in `results.json`.
  Mutated-artifact and counter digests are stored per arm in `results.json`; Arm-A counter
  digests: `entry-regular 66e5b81c…`, `entry-metric ade0e252…`, `row-unique 682e8fab…`,
  `row-well-formed af5a2e12…`, `used-by-exact 352c083b…`, `status-mined b48ef12e…`,
  `recheck-valid f2240ced…`, `digest-match 20285091…`, `gate-quote-substring 48629166…`,
  `gate-quote-word-bound b78b976e…`, `o-nofollow-open 063d6654…`.
- **Reproduce.** `python3 -I driver.py` in the scratch directory rebuilds every arm from `root/`
  and rewrites `results.json` + `run.log` (exit 0; seconds, longer under sibling load). Arm order:
  11 A counters → 13 B trees → 2 C TOCTOU pair → 10 A×B cross runs → 2 X attribution runs.
- **Installs.** None. Detector, driver and probes are Python 3.14.8 stdlib (`hashlib`, `re`,
  `stat`, `os`, `pathlib`, `shutil`, `importlib`). No network access, no pacman transaction, no
  `uv`/`cargo`/`npm` install.

## 8. Verdict on the assignment's question

**Ten of ten live clauses are verdict-dead on the real tree** (Arm A: all `TARGET_MET`, exit 0)
and each is reported above as a round-36 finding under F1. The complement is equally strong:
**ten of ten are individually live** when the real bytes are mutated one clause at a time (Arm B:
all `TARGET_MISSED`, exit 1), with `A+B` restoring `MET` for eight of ten. So the C1 gates are
real but the *real-tree run* does not exercise them; it is a one-bit fingerprint of
`open_cites == 0` (F2). F3–F5 and F9 add four calibration defects that a round-36 reader of
`uncovered=0` would otherwise not see: two unnamed load-bearing checks, a vacuous-quote survivor,
a prose-accepting cadence regex, and six unchecked row cells.
