# R95MExecCounterC1 — round-95 C1 counter (mimesniff)

Seat item: write `quality/counters/c1-r95-mimesniff.py` implementing PRED-C1-r95-v1 of the
declaration draft, adapt round-94 `c1-r94-mimeglob.py`, prove in DRAFT, write this report.

## Files written

- `quality/counters/c1-r95-mimesniff.py` (new, ~950 lines, stdlib only) — the C1 counter.
- `.ufo/waves/round-95/w1/R95MExecCounterC1-cases-draft.json` — my 21-case draft case file
  (one case per frozen class + one extra prio case; labels produced by the compiled oracle,
  one oracle run per case exactly like the counter's drift check).
- `.ufo/waves/round-95/w1/R95MExecCounterC1-draft.log` — the DRAFT counter run (rc 3).
- `.ufo/waves/round-95/w1/R95MExecCounterC1-drift.log` — the tampered-label SETUP_ERROR run (rc 2).
- This report.

## What the counter does (PRED-C1-r95-v1)

Takes `--repo --rev --base-rev --cases --expect-cases-sha256 --mutants
--expect-mutants-sha256 --oracle-src --expect-oracle-sha256 --fresh-gen
--expect-fresh-gen-sha256 --host-files --expect-host-files-sha256 --expect-tool-sha256
--expect-mimeglob-sha256 --fresh N --workers N --scratch-root DIR [--fresh-seed S]
[--draft-tool PATH] [--check-only]`.

- Pins every frozen input by sha256 (SETUP_ERROR rc 2 on mismatch); validates the case envelope
  (version 1, oracle_src_sha256, class ∈ the enumerated 20, labels well-formed, XDG_DATA_DIRS
  never unset in a case — it would reach the host DBs).
- Reads tool bytes with `git show <rev>:tools/mado-mimesniff.py` (or `--draft-tool`), reads the
  pinned `tools/mado-mimeglob.py` at `<rev>` (sha must equal `--expect-mimeglob-sha256`), places
  both in a fresh `<scratch>/tools/` dir so the tool's own-directory `spec_from_file_location`
  load finds the pinned file; `tool_pin=ok` iff both pins match.
- Compiles the oracle once (`cc -O1 … $(pkg-config --cflags --libs gio-2.0)`) from the pinned
  source; prints binary sha256 and `pacman -Q glib2 shared-mime-info`.
- (i) Re-runs the oracle on every frozen case — ONE oracle invocation per case carrying every
  input as a `(0|=NAME, datafile)` pair, 10 s timeout; crash/hang/malformed ⇒ all labels
  UNSUPPORTED — and SETUP_ERRORs (`oracle_drift=<ids>`) on any mismatch with the recorded
  labels. Scores the tool per case grouping inputs by name (`--name=` for a shared name, no
  `--name` for NULL; UNSUPPORTED-labelled inputs run in their own invocations so a refusal
  cannot mask supported answers): ok / wrong / crash, wrong dominating crash.
- (i) classes: the enumerated 20 with ≥ 6 cases each (`classes=K/20` printed per-class).
- (ii) fresh leg: runs the frozen generator (`--seed --n --out --scratch-root`, round-94 CLI
  convention), labels every fresh case with the live oracle, scores the tool; default `--fresh 120`.
- (iii) host leg: every readable file of the frozen list, first 4096 bytes, data-only (NULL name,
  chunked) and with its own path as the name (one invocation per file, `--name=<path>`), under
  the counter's HOME/XDG environment; prints `host_db` sha256 digests for every mime.cache/globs2
  under the resolved dirs.
- (iv) mutant leg: every counted mutant (`find` occurring exactly once in the tool source, else
  SETUP_ERROR) is applied and scored on the frozen cases; killed / crashed_not_killed / survived
  with round-94's attribution rules.
- (v) four controls, all implemented inside the counter: do-nothing (`application/octet-stream`,1);
  name-only (the pinned mado-mimeglob `Resolver.guess`, data ignored; NULL name ⇒
  `(application/octet-stream,1)` = g_content_type_guess(NULL,NULL,0)); naive sniff (first
  matching top-level matchlet value at its range start, cache order, no
  priority/mask/children/subclass — see "interpretation" below); base revision (no tool ⇒ 0).
  Each must have correct < N.
- (vi) `static_no_external_resolver` by `ast` parse: no subprocess/socket/multiprocessing/pty/
  urllib/http/xmlrpc/ctypes import, no os.system/popen/exec*/spawn*/posix_spawn*/fork*, no
  eval/exec/compile/__import__/import_module/reload call, importlib limited to
  spec_from_file_location/module_from_spec/exec_module, and the module must reference `__file__`
  and the literal `mado-mimeglob.py`. Every tool run gets `env={"PATH": <empty scratch dir>}`.
- Prints the exact `MADO_MIMESNIFF_COUNT: <VERDICT> pred=PRED-C1-r95-v1 rev=… tool_pin=…
  cases=N correct=C classes=K/20 fresh=a/b host=a/b mutants=M killed=K crashed_not_killed=X
  static_no_external_resolver=… controls do_nothing=… name_only=… naive=… base=…` line (plus
  sha256 detail fields, as round 94 did). rc 0/1/2/3 = TARGET_MET/TARGET_MISSED/SETUP_ERROR/DRAFT.
- `--check-only` validates pins + inputs and exits (verified: `CHECK_ONLY ok … rc 0`).

## DRAFT proof (all runs labelled DRAFT; nothing written under receipts/)

Draft inputs (all in my scratch, shas pinned per-run): cases = my 21-case file
(sha 5599db0d…), mutants = 5 draft find/replace mutants (55b4a71c…), fresh-gen = my draft
generator (7540f984…), host-files = first 40 lines of the frozen host list (bda80dfa…),
oracle-src = the frozen oracle source (99df35f8…), tool = the draft candidate (a13b6e0e…),
mimeglob = round-94 bytes at base rev (65f80a6c…, verified `git show 4a2af681:tools/mado-mimeglob.py`).

`--check-only`: `MADO_MIMESNIFF_COUNT: CHECK_ONLY ok pred=PRED-C1-r95-v1 cases=21 mutants=5 tool_pin=ok classes=20`, rc 0.

Full DRAFT run (`R95MExecCounterC1-draft.log`), rc 3:

```
MADO_MIMESNIFF_COUNT: DRAFT_TARGET_MISSED pred=PRED-C1-r95-v1 rev=draft:…/mado-mimesniff.py tool_pin=ok
cases=21 correct=20 classes=0/20 fresh=6/6 host=80/80 mutants=5 killed=5 crashed_not_killed=0
static_no_external_resolver=ok controls do_nothing=0 name_only=0 naive=12 base=0 …
```

- `classes=0/20` and `mutants=5`, `fresh=6/6`, `host=80/80` are the expected draft-input
  shortfalls (1 case/class < 6, 5 < 40 mutants, 6 < 120 fresh); the verdict is MISSED by design.
- **Each control misses (i)**: do_nothing 0/21, name_only 0/21, naive 12/21, base 0/21 — all < 21. ✓
- Mutant leg: all 5 draft mutants killed (m03 by fallback-01-bin; the other four "killed by
  lltext-01-vt" — see the caveat below).
- Static check on the candidate: `static_findings=none`.

Drift SETUP_ERROR (`R95MExecCounterC1-drift.log`): one label flipped in a copy of the draft
cases file ⇒ `MADO_MIMESNIFF_COUNT: SETUP_ERROR pred=PRED-C1-r95-v1 oracle_drift=zerosize-01-empty`, rc 2. ✓

UNSUPPORTED scoring unit check (counter's `score_case` imported directly): text-mode case
(tool exit 3) + UNSUPPORTED label ⇒ `ok`; cache-mode case + UNSUPPORTED label ⇒ `wrong`;
cache-mode + correct label ⇒ `ok`; cache-mode + wrong label ⇒ `wrong`. ✓ (A real oracle crash
could not be crafted cheaply — see risks.)

## Finding for the L1: the draft candidate diverges from the oracle on VT (0x0B)

The draft run's single WRONG case is `lltext-01-vt`. Reproduced directly:

- data `b"ab\x0bcd"` (VT): oracle `application/octet-stream\t1`; candidate `text/plain,0`.
- data `b"ab\x0ccd"` (FF): oracle `text/plain\t0`; candidate `text/plain,0` (agree).

Root cause: GLib 2.90.1 `looks_like_text` (gcontenttype-fdo.c:533-548) rejects a byte when
`g_ascii_iscntrl(c) && !g_ascii_isspace(c) && c != '\b'`; the installed glib's
`g_ascii_isspace('\v')` is **false** (verified with a 6-line C program against the installed
glib: cntrl/space for 8..13 = (1,0)(1,1)(1,1)(1,0)(1,1)(1,1)), so VT is NOT text and the guess
stays `application/octet-stream` uncertain. The candidate's `looks_like_text`
(`b < 8 or 14 <= b < 32 or b == 127`) treats 0x0B as text; its selftest s10 ("VT passes
looks_like_text", expects `text/plain`) enshrines the wrong expectation, so `--selftest`
23/23 does not catch it. The frozen `lltext` class (≥ 6 cases) will catch it at measurement if
it contains a VT-bearing input; the L1's 7240-input host probe did not (host files with VT but
no other binary control byte in the first 4096 bytes are evidently absent from the sample).
This is a candidate defect, not a counter defect: the counter's job is to score it wrong, which
it does. The frozen candidate may be revised before the freeze; the counter needs no change.

## Interpretation decisions (for L1 review)

1. **Oracle labeling granularity (R2)**: one oracle run per case with all inputs as pairs;
   crash/hang(>10 s)/malformed ⇒ every label of the case UNSUPPORTED. This matches the schema
   sentence "a case whose oracle run crashes … is labelled [UNSUPPORTED,null]" and round-94's
   per-case oracle run. If R95MExecCasesC1 labels per-input instead, my drift check will
   SETUP_ERROR on mixed cases — the generator must align with this reading.
2. **Naive control**: full guess pipeline with round-94's name step (Resolver), naive magic
   (first match in cache order, value at range_start only, no mask/children, no cross-cache
   priority), and resolution without the prio≥80 rule and without subclass (any non-UNKNOWN
   sniff wins; else first name type uncertain). Documented in the counter docstring. It misses
   9/21 draft cases.
3. **Mutant kill attribution** follows round-94 exactly (any frozen case wrong ⇒ killed). At a
   passing measurement (`correct == N`) candidate-shared wrongs cannot exist, so kills are
   attributable; in draft (candidate fails lltext-01-vt) four mutants show "killed by
   lltext-01-vt", which is not attributable — informational only, MET already false.
4. **XDG_DATA_DIRS unset in a frozen case ⇒ SETUP_ERROR** (schema forbids it; it reaches host DBs).
5. Fresh generator CLI assumed identical to round-94 (`--seed --n --out --scratch-root`); if
   mimesniff-fresh-r95.py differs, the fresh leg SETUP_ERRORs loudly.

## Verification commands run (all in scratch $S=/fast/scratch/hyaku/mado-r95/R95MExecCounterC1)

- `python3 -m py_compile quality/counters/c1-r95-mimesniff.py` → ok.
- `--check-only` draft → rc 0 (`CHECK_ONLY ok`).
- Full DRAFT run ×3 (after two counter fixes) → rc 3, log above.
- Tampered-label run → rc 2 `SETUP_ERROR oracle_drift=zerosize-01-empty`.
- `score_case` UNSUPPORTED unit checks ×4 → ok/wrong/ok/wrong as expected.
- Candidate `--selftest` → `checks=23 failed=0` rc 0; candidate/mimeglob sha256 match the pins.
- `git show 4a2af681:tools/mado-mimeglob.py | sha256sum` = 65f80a6c…2453 ✓;
  `tools/mado-mimesniff.py` absent at base rev ✓ (base control ⇒ 0).

Counter bugs found and fixed during the draft proof: `git_show` arity on the base-rev lookup
(rc 1 TypeError), and a host_leg signature/call mismatch (caught by py_compile + rerun).

## Risks / blockers

- Frozen cases/fresh-gen/mutants were not yet present in `controls/` at proof time; the counter
  is written to the schema in the item and validated on my draft inputs. The fresh-gen CLI and
  the per-case oracle-labeling reading are the two alignment points (see interpretation 1 & 5).
- Crafting a real oracle crash (for an end-to-end UNSUPPORTED case) was not done; the scoring
  path is unit-verified instead. Nest>100000 is the likely generator route (build_cache cannot
  emit it — its `values()` recurses; the generator must hand-craft or iterate).
- Host leg at measurement: 3528 files ⇒ ~7056 oracle pairs + 3528 own-path tool invocations;
  estimated well under the leg timeouts with `--workers 8`.

## Installs

None.

## Scratch

Deleted on exit (evidence copied to `w1/` first).
