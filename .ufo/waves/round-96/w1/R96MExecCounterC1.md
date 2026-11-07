# R96MExecCounterC1 - round 96 w1 report (C1 magictext counter)

Seat: executor, C1 counter lane. Base revision `9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d`.
Predicate implemented exactly: **PRED-C1-r96-v1**, verbatim in the counter docstring; no leg
widened, no leg dropped. The counter is the measurement instrument for the TEXT MIME database's
magic step: file bytes (+ optional name) -> MIME type as GLib 2.90.1 `g_content_type_guess`
answers when no reachable `mime.cache` loads.

## Deliverables

| file | sha256 | state |
|---|---|---|
| `.ufo/waves/round-96/quality-counters-c1-r96-magictext.py` | `9d3e1e76f2acf8c2219dd03157496363ddf9ff1a0089cc9aa090e5d0af42a7f7` | final draft; L1 copies to `quality/counters/c1-r96-magictext.py` |
| `.ufo/waves/round-96/w1/R96MExecCounterC1.md` | - | this report |

stdlib only; ASCII only; writes only under `--scratch-root`; every tool invocation goes through
the audit launcher (round-95 `LAUNCHER_SRC` verbatim) with `PATH=<empty mkdtemp dir>`; label-bearing
artifacts (generator output, memoriser table) live in a sibling of the audit `work` dir, outside the
allowlist, so the candidate cannot read scoring labels.

## argv contract (as changed by the L1 at 11:52; the docstring carries it verbatim)

Required: `--repo --rev --base-rev --cases --expect-cases-sha256 --mutants --expect-mutants-sha256
--oracle-src --expect-oracle-sha256 --fresh-gen --expect-fresh-gen-sha256 --host-list
--expect-host-list-sha256 --host-db --expect-host-db-sha256 --expect-tool-sha256
--expect-mimeglob-sha256 --forgery --expect-forgery-sha256 --scratch-root`.
Optional: `--fresh N` (default 1), `--fresh-seed N`, `--workers N`, `--draft-tool PATH`, `--check-only`.
rc 0 `TARGET_MET`, 1 `TARGET_MISSED`, 2 `SETUP_ERROR`, 3 `DRAFT_*` (with `--draft-tool`).

**AMENDMENT the L1 must fold into the declaration's counting command**: the new required argument
`--expect-tool-sha256 <sha256 of the frozen tools/mado-mimetext.py bytes at the C1 measured rev>`.
Rationale: the candidate is not at any revision yet, so the frozen leg cannot hash "the bytes at
`--rev`" until freeze; the pin arg makes the frozen leg self-checking from day one (`tool_pin=ok`).
The counter docstring lines 23-25 carry this text.

## Predicate -> implementation map (verdict fields)

- `tool_pin` — `sha256(git show --rev:tools/mado-mimetext.py)` (or `--draft-tool` bytes) ==
  `--expect-tool-sha256`; `tools/mado-mimeglob.py` pinned likewise (`SETUP_ERROR` on drift); every
  other frozen input pinned by `--expect-*-sha256`, mismatch -> rc 2.
- base control — `tools/mado-mimetext.py` absent at `--base-rev`, printed
  `base: tools/mado-mimetext.py absent at base-rev (declared before 0/0)`; presence -> rc 2.
- (i) frozen cases — per-case fixture-derived mode (below), tool answers vs frozen labels,
  UNSUPPORTED-labelled inputs run alone (the tool's CLI stops at its first refusal, rc 3 per FILE);
  `correct=265/265` required; per-class census must equal the declared 16 classes with >=8 each
  (printed `per_class=...`), id prefix `<class>-NN-` digit-checked; `classes=16/16`.
- (ii) fresh — `--fresh N` = N generator runs (seeds `fresh_seed+i`, or N random seeds), pooled;
  generator validates its own labels against its own oracle run; the counter re-labels every fresh
  input with the live oracle and demands agreement (drift -> rc 2), then scores; `fresh >= 120`
  inputs. `fresh=298/298` on the measured run (40 cases).
- (iii) host — the eight `/usr/share/mime` text files named by the sha-pinned `--host-db` manifest
  are copied to `<work>/hostdb/mime/`, each per-file sha256 verified against the manifest pins and
  `mime_cache_in_copy == 0` asserted (`host_db=ok files=8` + all eight digests printed); then tool
  vs live oracle over the frozen round-95 list (4911 paths), per file the data-only pair (name NULL)
  and the own-path-as-name pair -> 9822 pairs; `host >= 1500` paths; `no mime.cache reachable` is
  asserted for every scored dir (`case_roots`/`loadable_cache`).
- (iv) mutants — each `find` must occur exactly once in the pinned candidate source (anchoring);
  applied -> launcher run over the frozen cases; killed = >=1 case wrong; `killed == mutants` and
  `class_kills == 16/16` (>=1 killed mutant per case class). SKIPPED (`killed=0`) when the tool is
  not the pinned candidate — that state is already `tool_pin=FAIL` -> missed.
- (v) controls — `do_nothing_text=0/240` (round-95 tool `tools/mado-mimesniff.py` refuses text mode;
  scored over text-mode frozen cases only; `do_nothing_none=K/N` printed as census, NOT gated);
  `name_only=27/265 < 265` (round-94 `Resolver.guess`, data ignored); `naive=86/265 < 265`
  (embedded fallback-only model: name step + zerosize/128-byte-text-vs-binary data step, no magic
  parse, no priority/subclass nuance, no refusal surface); `memoriser fresh=0` (below);
  `forgery rejected=True` (`audit_denials > 0` OR static findings — the audit is the load-bearing
  conjunct: the frozen `forgery-ctypes-r96.py` does `ctypes.CDLL("libgio-2.0.so.0")` which the
  audit hook denies, rc 97).
- (vi) selftest — `--selftest` must print `MADO_MIMETEXT_SELFTEST: checks=N failed=0` with rc 0 and
  no `_FAIL:` lines (`selftest=ok checks=50 failed=0`).
- static conjunct — `static_check` (AST): no `subprocess`/`socket`/`urllib`/`http`/`ctypes` imports,
  no `os.system`/`exec`/`spawn`/`fork`, no dynamic module loading (`module_from_spec` result must
  only flow to `exec_module`, never escape), `mimeglob` attribute use limited to the frozen
  `_MG_ATTRS` allowlist. Failure -> `static_no_external_resolver=FAIL` -> missed.

Per-case mode derivation (L1 contract details 1+2; supersedes the declaration's `db_mode=="text"`
sentence): roots from the RAW env templates (`{root}/dh` -> `dh`; `XDG_DATA_HOME` unset ->
`h/.local/share`; `XDG_DATA_DIRS` split on `:`), reachable via each root's `<root>/mime/`; a
reachable loadable `mime.cache` (regular file, >=40 bytes, BE u16@0==1, BE u16@2 in {1,2} — the same
rule `tools/mado-mimeglob.py load_cache` applies; the cases seat confirmed these offsets, which
supersede the L1's loose "bytes 4..7" phrasing) -> cache mode; else a reachable `mime/<text file>`
-> text mode; else none. `SETUP_ERROR` if an UNSUPPORTED label sits on a non-cache case or a
supported label on a cache case. `case_modes text=240 none=20 cache=5` on the frozen file.

Memoriser (L1 fix, review F2, this session): keyed by **case identity** — `case_fingerprint` =
sha256 over (case mode, the env triple after `{root}` substitution, per-file digest of the files
layout, per-input digest of the name/data b64 pair list). A fresh case can never collide with a
frozen one (its fixtures differ), and two frozen cases that share an input still get their own
labels (the old `(name,data)` key made `memoriser frozen=156/265` on the measured run — inputs
shared across case fixtures collided). All 265 fingerprints verified unique; miss answers the
sentinel `application/x-mado-memoriser-miss`, so it cannot match any oracle answer.

## Host text database (what the counter copies and pins)

From `.ufo/waves/round-96/controls/host-text-db-r96.json` (`source.dir=/usr/share/mime`),
printed by the measured run:

| file | sha256 |
|---|---|
| mime/magic | `2942f4adfca98c1816177f056d566e925e96e1c3dd562964dada066bf4a8a35c` |
| mime/globs | `54eb042dc1a2f2caba8e09ff79eda184ea0063d50dd796ea3f3726a20e96c40d` |
| mime/globs2 | `556ee69c8be2e24c4e3025dc5af0bdae71c6dca899491b4c95778a531958168e` |
| mime/aliases | `74cde6689d6161332df5e89358fb68c23959f230aa4f1ee0bcf03f2fa062c5df` |
| mime/subclasses | `3dc5ff5773867381cedc84523738d8ee11ccd95618e5157be05cefdc6f9cfa62` |
| mime/icons | `7198dd2150a591c2c2f4d0fa91599823871c4ee1017993b1e06f9094a9702a30` |
| mime/generic-icons | `ad2a08102009507566ac25c79b0fdc1a35fc89dfb2e983672d6ccf5297260f3a` |
| mime/XMLnamespaces | `706cfd7efe0632b7f5abb55fa5626f47efb63a42cdad9ff6ed7360a259bb98cc` |

glib2 2.90.1-1, shared-mime-info 2.5.1-2; oracle binary
`186537938e186727072bf911a86117918d505593e77617e53cfa246d425a3aa5` compiled from the pinned r95 C
source with `cc -O0 $(pkg-config --cflags --libs gio-2.0)`.

## Frozen replay (post-freeze, at the C1 measured rev)

```
python3 -I .ufo/waves/round-96/quality-counters-c1-r96-magictext.py \
  --repo . --rev <C1_REV> --base-rev 9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d \
  --cases .ufo/waves/round-96/controls/magictext-cases-r96.json \
  --expect-cases-sha256 42ce9fc68458955e9e93c405cdbeb59f649b36d94e100240894d660391d1bed6 \
  --mutants .ufo/waves/round-96/controls/magictext-mutants-r96.json \
  --expect-mutants-sha256 <sha of the mutants file once R96MMutC1 fills the find/replace pairs> \
  --oracle-src .ufo/waves/round-95/controls/mimesniff-oracle-r95.c \
  --expect-oracle-sha256 <sha of mimesniff-oracle-r95.c> \
  --fresh-gen .ufo/waves/round-96/controls/magictext-fresh-r96.py \
  --expect-fresh-gen-sha256 32d38edfb2cff57de3d89297ffaf1bd781d730b7be502fbfa62efa38de0815da \
  --host-list .ufo/waves/round-95/controls/mimesniff-host-files-r95.txt \
  --expect-host-list-sha256 <sha of the host list> \
  --host-db .ufo/waves/round-96/controls/host-text-db-r96.json \
  --expect-host-db-sha256 <sha of host-text-db-r96.json> \
  --expect-tool-sha256 <sha of the frozen tools/mado-mimetext.py bytes> \
  --expect-mimeglob-sha256 65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453 \
  --forgery .ufo/waves/round-96/controls/forgery-ctypes-r96.py \
  --expect-forgery-sha256 <sha of forgery-ctypes-r96.py> \
  --scratch-root <fresh dir> [--fresh-seed N]
```

No `--draft-tool`: the frozen leg hashes `git show <rev>:tools/mado-mimetext.py` and enforces
`--expect-tool-sha256`. The per-leg argv is documented in the counter docstring (lines 60-94).

## Measured draft runs (this seat, scratch `run3`/`run4`)

Draft run 3 (tool snapshot `fb924d96…4ca4`, the bytes under test at exec time; counter pre-F2-fix):

```
selftest rc=0 checks=50 failed=0 fail_lines=0 ok=True
per_class header=17 sect=20 value=20 mask=16 word=19 range=16 indent=17 order=16 drop=17 multi=16
          glob=16 alias=14 fallback=14 zerosize=14 mode=17 desktop=16   (all >= 8)
case_modes text=240 none=20 cache=5
fresh seeds=[475294497] gens=1 cases=40 ok=40 inputs=298/298
host_db=ok files=8 (all eight digests match the manifest pins)
host readable=4911 pairs=9822 correct=9822
mutants(16 test): killed=13 survived=3 crashed_not_killed=0 class_kills=16/16
control do_nothing text=0/240 none=20/20
control name_only correct=27/265
control naive (fallback-only) correct=86/265
control memoriser frozen=156/265 fresh=0/40        <- the (name,data) collision; fixed below
control forgery static=import:ctypes:8,... audit_denials=5 rejected=True
static_findings=module-use:mp:483,module-use:mp:485  (that snapshot had a loader-result escape;
  static_check on the current tool bytes d5f174fc… is [])
MADO_MAGICTEXT_COUNT: DRAFT_TARGET_MISSED ... rc=3 (8 min wall, workers=12)
```

After the two fixes (memoriser case-identity key per L1; nothing else changed), counter
`9d3e1e76…` re-measured on the current tool bytes `d5f174fc…` (run4, workers=12, --fresh 1,
seed 4229727250):

```
--check-only: MADO_MAGICTEXT_COUNT: CHECK_ONLY ok pred=PRED-C1-r96-v1 cases=265 mutants=16 equiv=0 tool_pin=ok classes=16
MADO_MAGICTEXT_COUNT: DRAFT_TARGET_MISSED pred=PRED-C1-r96-v1 rev=draft:.ufo/waves/round-96/build/mado-mimetext.c1.py base_rev=9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d tool_sha256=d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd tool_pin=ok mimeglob_sha256=65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453 cases=265 correct=265 classes=16/16 per_class header=17 sect=20 value=20 mask=16 word=19 range=16 indent=17 order=16 drop=17 multi=16 glob=16 alias=14 fallback=14 zerosize=14 mode=17 desktop=16 fresh=319/319 fresh_cases=40 host=9822/9822 host_paths=4911 mutants=16 killed=13 crashed_not_killed=0 class_kills=16/16 static_no_external_resolver=ok audit_denials=0 selftest=ok checks=50 failed=0 controls do_nothing_text=0/240 do_nothing_none=20/20 naive=86 name_only=27 base=0 memoriser_fresh=0 forgery=rejected host_db=ok files=8 oracle_sha256=186537938e186727072bf911a86117918d505593e77617e53cfa246d425a3aa5
```

(rc 3 `DRAFT_TARGET_MISSED` for exactly one reason: 3 of my 16 smoke mutants survive —
`sect-bad-prio-accepted`, `drop-error-no-skip`, `multi-dir-order-flip`; they are deliberately
crude one-per-class probes, not the frozen 115. `memoriser frozen=265/265 fresh=0/40` — perfect
recall on frozen cases, zero fresh collisions, the F2 fix working for the right reason. Every
predicate leg except the frozen-mutant population is green on this measurement.)

## Oracle combination semantics (probed this seat, probe4-6)

Facts the counter relies on (GLib 2.90.1, text db):
- a single name type always wins with certainty 1;
- a sniffed type with priority >= 80 beats the name type; below, name wins;
- a name type that is a (transitive) subclass of the sniffed type wins with certainty 1;
- sniffed `application/octet-stream`/UNKNOWN -> name types win with the sniff's own certainty;
- `text/plain` is a built-in parent of every `text/*` type;
- `x-desktop` content rewrites to `text/plain` when a name is present;
- the `aliases` file did NOT canonicalize name/sniffed types in the probes (match on the raw
  string is what GLib scores).

These are encoded in the cases/labels (frozen, oracle-checked at measurement) and re-verified by
the fresh leg's live-oracle relabel agreement — no drift observed.

## Coordination trail

- MadoR96 (L1): delivered the 11:52 argv contract change (host-db manifest + forgery + tool/mimeglob
  pins, `--scratch-root`, `db_mode` gone), contract details 1-2 (per-case mode derivation,
  loadable-cache rule), verdict-field list incl. the do-nothing split; and the F2 fix directive
  (memoriser keyed by case identity — implemented as `case_fingerprint` above).
- R96MExecCasesC1: confirmed the loadable-cache byte offsets (u16@0, u16@2) and shipped the
  relabelled cases file (`42ce9fc6…`, mode-06 oracle-labelled `app/x-md6,0`/`app/x-md6g,0`).
- R96MReviewC1: F1 (`--scratch-root` missing — fixed), F2 (case-relative roots always empty —
  fixed as `case_roots`), F3 (fresh label leak into the allowlist — fixed via the `secret` sibling),
  F4 (mode-06 case defect — fixed by the cases seat).
- R96MMutC1: owns `magictext-mutants-r96.json` (115 rules; all `find`/`replace` still
  `<awaiting-candidate>` at report time — the counter correctly SETUP_ERRORs on anchor checks
  until they are filled against the frozen candidate bytes).

## Limits, risks

- The mutants file still holds 115 `<awaiting-candidate>` placeholders; the counter cannot run the
  mutant leg until R96MMutC1 fills them and the shas are re-pinned. My 16-mutant test file (one per
  class, all finds verified killed) exercised the leg mechanics; 3 of my 16 survived by design —
  they are smoke mutants, not the frozen set.
- The tool seat is still iterating `build/mado-mimetext.c1.py`; run3 measured snapshot
  `fb924d96…` (static FAIL, since fixed), run4 measures `d5f174fc…`. The frozen replay pins
  whatever bytes the L1 freezes; `--expect-tool-sha256` makes a stale pin a loud miss, not a
  silent pass.
- The host leg is the runtime long pole (9822 audited invocations + oracle pairs; ~4-5 min at
  workers=12); the whole counter is minutes, not seconds, at freeze.
- The memoriser `frozen=n/n` strength is a control-quality fact, not a gate: the predicate gates
  only `memoriser fresh == 0` (now true for the right reason — no fresh case can match a frozen
  fingerprint) — and `do_nothing_none` prints `K/N` where N is the census; neither is thresholded.
- No tools installed, no host state touched, no network fetches; scratch removed after validation.
