# RcDigestPinnedFrozenRegres438 — C2 ledger attack on CapDigestPinnedFrozenRegres438

Seat: `MadoR25A3.RcDigestPinnedFrozenRegres438` (leaf reviewer, C2 ledger recheck). Wave: round-25 attempt 3,
`a3w2` (data + falsify). Target: `.ufo/waves/round-25/a3w1/reports/CapDigestPinnedFrozenRegres438.md`, the a3w1
seat's re-run of `SCORECARD.md:438` (`digest-pinned frozen regression`, round-13 repertoire row) at base
`41cc04c8d593837a0d5078bffaacdaa163d12897`. Read-only in the lane; all git work in my own sandbox clone; clone
deleted before returning.

## Re-derivation (what I ran)

```
mkdir -p /fast/scratch/hyaku/mado-r25a3/rc
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 280 git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/rc/CapDigestPinnedFrozenRegres438
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C …/CapDigestPinnedFrozenRegres438 checkout -q --detach 41cc04c8d593837a0d5078bffaacdaa163d12897
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C …/CapDigestPinnedFrozenRegres438 rev-parse HEAD
```
→ `41cc04c8d593837a0d5078bffaacdaa163d12897`. `df -h /fast` before clone: 215 G available.
`git -C <lane> show 41cc04c8:SCORECARD.md | sha256sum` = `6b6995ff…08`, identical to the clone worktree file, so
the file I reviewed is byte-identical to the base blob.

Commands run inside the clone (clone root as cwd):

- `timeout 600 prlimit --as=4000000000 python3 .ufo/waves/round-13/frozen/verify.py` — wall 107.38 s
- `timeout 600 prlimit --as=4000000000 python3 .ufo/waves/round-13/frozen/verify.py --selftest`
- Tamper leg (my own probe, as the a3w1 seat did): `cp` the four frozen files to `mktemp -d
  /tmp/rc-frozen-tamper.XXXXXX`, append one line to `gate.sh`, `timeout 120 prlimit --as=4000000000 python3
  $d/verify.py` — valid because `verify.py:197` resolves its inputs via `Path(__file__).resolve().parent`.

## Comparison against the a3w1 report

| Axis | a3w1 claim | My independent observation | Agrees |
|---|---|---|---|
| Row location/bytes | `SCORECARD.md:438` under `### Sources and demonstrated repertoire` (:425), `## Round 13 — committed measurements` (:367) | `grep -n` on base bytes: heading at :367 and :425; row at :438 byte-for-byte as quoted | yes |
| Frozen-file digests | gate `037b05dc…`, harness `75ed934d…`, `verify.py` `094bf3a4…` (197 lines), `expected.json` `761a0c91…` | `sha256sum` on clone files: all four identical; `wc -l verify.py` = 197 | yes |
| `expected.json` content | pins `gate.sh`, `harness.sh`, `expected_exit: 0`, `expected_marker: MADO_REGRESSION: PASS` | `cat` output identical | yes |
| Main leg | both `FROZEN_INPUT … verified` before `FROZEN_RUN`; spec `c7ee75b9…` pin match; target `87910c39…` pin match; 10/10 killed, flips 0, control green; `MADO_REGRESSION: PASS`; `MADO_FROZEN: MATCH`; `FROZEN_ID: frozen_match`; `exit=0`; workdir removed on PASS | Identical line-for-line except run-specific values: my tmpdir `/tmp/mado-verify-regression.MXLE9T`, `REGRESSION_DATE 2026-10-23T07:41:21Z`, rc-path prefixes | yes |
| Selftest | `12/12` exit 0 | `MADO_FROZEN_SELFTEST: 12/12 assertions passed`, `exit=0` | yes |
| Tamper refusal | appended byte → `snapshot_tampered` exit 2, `mismatch gate.sh … actual=7b5a96c1…`, no `FROZEN_RUN` | Reproduced exactly — same tampered sha `7b5a96c1…` (deterministic append), no gate execution | yes |
| Command form | `python3 .ufo/waves/round-13/frozen/verify.py` relative path, clone-root cwd | Runnable as written; script-dir resolution makes the cwd non-essential, but row form is honored and the row's own evidence command matches | yes |
| Superseding pointers | `:1588–1594` (outside the 12-row counted population; wave-2 re-ran at `39c59630` → `MADO_FROZEN: MATCH`, exit 0 — corroborates, does not supersede); `:1570` scope caveat applies only to the 12 counted rows; `:406–408` harm-watch corroboration; **no contradiction** | My own grep sweep over every `frozen`/`FROZEN`/`digest-pinned`/`MADO_REGRESSION` hit in base SCORECARD.md confirms all cited lines and finds no missed superseding or contradicting text; all other hits are different rounds/capabilities (:546 r14 pair, :782 r16 classifier, :998/:1020/:1580 r18 tripwire, :1134+ tripwire baselines) | yes |
| Scratch claim | gate writes only under `/tmp/mado-verify-regression.*` (gate header line 1402) | `gate.sh:1402` reads "Scratch only under /tmp/mado-verify-regression.*"; workdir created at `:1651`; my workdir was removed on PASS | yes |
| Scope caveat | runner pins gate/harness against `expected.json` but not `expected.json`/`verify.py` themselves (coordinated-rewrite hole; same caveat as round-16's `:786–788`) | Correct per source: `FILES=("gate.sh","harness.sh")` (`verify.py:24`); `load()` trusts the pin file; row wording "both committed gate/harness input digests" is accurate to that scope | yes |

## Provenance check (copied-not-run test)

- a3w1 output carries their clone paths (`/fast/scratch/hyaku/mado-r25a3/c2/…`), their tmpdir
  `/tmp/mado-verify-regression.Lia8ih`, and `REGRESSION_DATE 2026-10-23T07:22:49Z`. The committed round-13 receipt
  `round-13/evidence/frozen-regression.txt` has lane paths, tmpdir `SEeHDw`, and date `2026-10-20T04:38:34Z`.
  Their quoted output could not have been copied from the committed receipt; it is a fresh run at the current
  wave. My run reproduces the same semantics with independent tmpdir/date. Not copied-not-run.
- Their disclosed capture wrapper (`----- CMD -----`, `[wall 153.96 s]`) is clearly marked as wrapper, not
  command output. Their ad hoc tamper leg is disclosed as beyond the row's literal command and is within scope of
  the row's "tamper refusal" clause.

## Flags

- **Copied-not-run evidence:** none. Output is a genuine fresh run (see provenance).
- **Wrong revision:** none. `rev-parse HEAD` at base; `git show` blob sha == worktree file sha.
- **Overclaim:** none. The ledger line claims `works` — observed — and accurately scopes the pin to gate/harness
  inputs. Round-24's counted population is correctly described as excluding this row.
- **Missed superseding text:** none. The operative present-tense declaration is the wave-2 append `:1588–1594`
  (`MADO_FROZEN: MATCH`, exit 0 at `39c59630`), cited. The sibling row `:437`'s stale flag is correctly not
  imputed to `:438`.

Residual risk: single-run evidence per leg at base (same as theirs); tamper leg is one append shape of one input
(their + my appended-line tamper produce identical output; other mutation shapes are covered by the selftest's
fixed-fixture assertions, which never recompute fixture digests — verified in source).

## Cleanup

- Clone `/fast/scratch/hyaku/mado-r25a3/rc/CapDigestPinnedFrozenRegres438` deleted (`test -d` confirms absent).
- My tamper dir `/tmp/rc-frozen-tamper.Snou1l` deleted by the same command. My workdir `.MXLE9T` removed on PASS.
- `pgrep -af 'mado-verify|round-13/frozen'` after my runs: no processes. A pre-existing
  `/tmp/mado-verify-regression.fH0yy8` (mtime Oct 23 01:06, another seat's) was left untouched.
- No `__pycache__` risk: `verify.py` runs as `__main__` (no bytecode written for the main script); no lane file
  touched except this report. No tool install needed or performed.

## Verdict

RECHECK CapDigestPinnedFrozenRegres438: agree — re-ran all three legs in my own clone at 41cc04c8; row bytes, digests, exit codes (0/0/2), `frozen_match`/`snapshot_tampered` semantics, command form, and superseding pointers all reproduce; evidence is a genuine fresh run, not copied; no overclaim or missed supersession.
