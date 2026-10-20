# ScoutFrozenSchema — `--frozen` compares only (file,line,class,rule) plus exit/label; `evidence` is invisible to it and a lead row at r13-root:4 cannot move `frozen_match`, so keep round-19 frozen as is and do not re-pin

Observed HEAD: `e629f731172b8238caffe50f152217ce56535fb4` (refs/heads/master, detached HEAD same),
tool `tools/mado-tripwire.py` sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`
(`sha256sum`, worktree clean for that path). No lane write was made; every experiment ran on
copies under `/tmp/sfs/`.

## 1. What `--frozen` compares (and what it refuses)

`run_frozen` (`tools/mado-tripwire.py:1915-1976`) after digest-checking every pinned input:

```
1955  for f in hits: f["file"] = e["path"]            # the pin's own relative spelling
1960  def key(f):
1961      return (f["file"], f["line"], f["class"], f["rule"])
1963  got = Counter(key(f) for f in findings)
1964  expected = Counter(key(w) for w in pinned["findings"])
1965  missing = expected - got
1970  extra = got - expected
1973  mismatch = (scan_exit != pinned["exit"] or scan_label != pinned["label"]
1974              or bool(missing) or bool(extra))
```

So the compared facets are exactly: **exit code**, **label**, and the **multiset of
(file, line, class, rule)** in both directions. Nothing else on a row is read: not `evidence`,
not `argv0`, not `command`, not `timestamp`, not `tool_call_id`, not verdict count keys.

Shape rules that bound what a pin may contain:
- `expected.json` top-level keys are a closed set `FROZEN_KEYS` (`:1688-1689`, enforced `:1713-1716`):
  `schema, inputs, permit, expected_exit, expected_label, expected_findings, known_misses`.
- Each `expected_findings` entry is validated only for `file/line/class/rule`
  (`:1747-1756`); **unknown per-entry keys are accepted and ignored**.
- `(expected_exit, expected_label)` must be in `{(0,clean),(0,permitted_only),(1,findings)}`
  (`:1650`), so a lead-only run (still label `findings`) is representable.
- Every pinned input must be a regular non-symlink file inside DIR whose sha256 equals its pin
  (`frozen_snapshot`, `:1811-1893`); `:1936-1944` produce `snapshot_tampered`.
- `expected.json` is digested and echoed as `expected_sha256` but is not itself compared to any
  in-file pin; the digest binding is the committed receipt's job
  (`.ufo/waves/round-19/evidence/final/tripwire-frozen-r19.txt:1` names tool digest +
  `measured_commit`; the expected digest appears in the verdict line).

## 2. Does adding `evidence` to rows change `frozen_match`? No — tested both directions

- **Tool rows gaining the key.** Patched a `/tmp` copy at the single finding-dict site
  (`tools/mado-tripwire.py:1596-1606`, key added next to `"tool"`) to emit
  `"evidence": "lead"` on *every* row, then replayed the untouched round-19 pin:
  `MADO_TRIPWIRE_FROZEN: frozen_match`, exit 0, `extra_findings: []`, expected_sha256
  `50d2a45e…`. Even tagging all 11 rows contrary to expectation is invisible.
  Same patched tool: `--selftest .ufo/waves/round-19/tripwire/r19-helperfn` 34/34,
  `r19-frozen-f1f2` 13/13 (the selftest scan key at `:2055-2068` is `(class, rule, line[, file])`).
- **Expected rows gaining the key.** `/tmp` copy of the pin with `"evidence":"lead"` added to the
  `inputs/r13-root.jsonl:4` entry → `frozen_match`, exit 0 (expected.json digest moves to
  `a19aeac2…`). Per-entry extras are tolerated as shown above.
- **Top-level key.** Adding `"evidence"` at the spec top level → `frozen_error`, exit 2,
  `"unknown expected.json key(s): evidence"` (this is the one place the word is fatal).
- **Regenerator strips it anyway.** `frozen-repin.py` normalizes every row to four keys
  (`validate_source` `:140-228`, `parse_verdict` `:240-300` at `:273`, `rows()` `:309-312`).
  Evidence in a source pin cannot survive a re-pin.

[INFERENCE] Therefore the round-20 marker can be recorded only in the new precision suite and in
`--scan` output; a frozen pin is structurally evidence-blind.

## 3. Keeping `r13-root.jsonl:4` as a lead

Observed now: the line is `run_record('packages',['pacman','-Q','wayland-utils',…],0)` inside one
py eval cell (`frozen/inputs/r13-root.jsonl:4`), and no `def`, import or assignment of `run_record`
appears anywhere in the five lines (`grep -o "def run_record\|run_record *= *[^,(]"` over the file:
no match; `run_record` is called only at line 4). The tool's rule B
(`helper_argv_leads`, `:1379-1391`, caller `:1431-1433`) therefore emits
`package_query/pacman:-Q` at that line under tool `367be947…`, which is why the round-19 pin lists
it as an ordinary finding.

Under the round-20 contract E1 this becomes `lead` but **stays in `findings`** with the same
`class` (`package_query`) and `rule` (`pacman:-Q`), keeping exit 1 / label `findings`
(`contract: "Lead rows stay in \"findings\" (exit 1, label `findings`)"`). Because the frozen key
ignores `evidence` and both facets that do matter are unchanged, `frozen_match` is unaffected.
This is exactly the shape simulated in §2 (all rows tagged lead → still `frozen_match`).

Caveat: if the rule-B rewrite instead *dropped* the row or changed its class/rule, round-19 frozen
would go red. That red is the desired guard, not a reason to re-pin (§5).

## 4. Present state of the two pins (both replayed read-only)

| pin | expected.json sha256 | replay now (tool 367be947) |
|---|---|---|
| `round-19/frozen` | `50d2a45e2602cb430b94043f6c658204b0b1802e8c1931cb2a3eda167af02435` | `frozen_match`, exit 0, 5/5 input digests ok |
| `round-18/frozen` | `4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9` | `frozen_verdict_mismatch`, exit 1, extra: `r13-root.jsonl:4`, `r14-source-safety.jsonl:2`, `:3` (all `package_query/pacman:-Q`) |

The round-18 red is the documented expected red: its three `known_misses` became detected at
round 19, and round 19 re-pinned (`frozen/README.md` "dropped as now-detected: …"). Round 18's own
README requires dropping a known miss once detected, which is what the r19 pin records.

Trial re-pins (written only under `/tmp/sfs/`, current tool):
- from `round-19/frozen` → `/tmp/sfs/r20frozen`: `MADO_FROZEN_REPIN: written`, expected.json
  **byte-identical** to the r19 pin (`50d2a45e…`, `cmp` clean). Only README/provenance differ
  (lineage sentence, `repinned_from`).
- from `round-18/frozen` → `/tmp/sfs/r18pin`: also byte-identical to the r19 pin (`50d2a45e…`).
  A round-20 pin sourced from r18 is therefore indistinguishable from one sourced from r19.

## 5. Recommendation — keep `round-19/frozen` as is; do not create a round-20 pin

Reasons, each grounded above:
1. **No schema gain.** Evidence is not compared and cannot be stored in a pin that the official
   regenerator will accept unchanged (it strips it). A new pin would carry the same four-key rows.
2. **No informational gain.** With the current tool a re-pin reproduces the r19 expected.json
   byte-for-byte; from either source. It duplicates bytes, not knowledge.
3. **It is the only forward regression for the repair.** Keeping r19 frozen makes the fixed tool
   prove it still emits all 11 r19-detected rows with their classes/rules. Re-pinning regenerates
   expectations *from the fixed tool* — self-certification that would silently absorb exactly the
   regression the baseline exists to catch (a dropped rule-B row, or a re-ruling of
   `r13-root:4`).
4. **Consumers already assume it.** `round-19/harm-watch.sh:296-336` replays `--frozen round-18` as the recorded
   red and `--frozen round-19` (`:329-336`) under `run_pinned` (a match is required); the
   round-20 harm-watch spec repeats this (`.ufo/waves/round-20/gen_w1.py:95`). No tracked tool or gate invokes a round-20 pin
   (`git grep frozen` over `tools/ SKILL.md SCORECARD.md corpus/` shows only prose and the
   separate `mado-action-plan.py --frozen` mode). The round-20 counters never read r19 frozen:
   `tw-recall.py` and `tw-recall-split.py` pin `round-18/frozen` at `9c54c56` via `git show`
   (`tw-recall-split.py:17-18`), and `tw-precision.py:81` reads `evidence` from **scan** output
   with default `"observed"`.
5. **Receipt cost is real.** `frozen-repin.py` writes `RECEIPT tool=… tool_sha256=… utc=… argv=…`
   (`:316`) — **no `measured_commit`** — and hardcodes "round-19 regenerator"
   (`.ufo/waves/round-19/frozen-repin.py:323`), so a round-20 dir would ship a receipt that fails
   the lane's header rule and mislabels its own wave. This is the limit recorded at
   `corpus/lessons/round-19.md:114-115`; round 19 worked around it by re-cutting the replay
   receipt header-bound in `evidence/final/` (`tripwire-frozen-r19.txt:1`).

If L1 nevertheless decides a round-20 pin is required, the only defensible order is:
1. land the fixed tool and run `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-19/frozen`;
   it MUST print `frozen_match` first — a `missing_findings`/`extra_findings` list is a classifier
   finding to investigate, never a reason to regenerate;
2. then `python3 -I .ufo/waves/round-19/frozen-repin.py --from …/round-19/frozen --to …/round-20/frozen --tool …/tools/mado-tripwire.py`;
3. hand-edit or re-cut the README receipt with `measured_commit=<commit carrying the pin>` (the
   script will not), keeping the `expected_sha256` in the replay verdict body, exactly as
   `evidence/final/tripwire-frozen-r19.txt` does.

Do **not** extend the frozen comparison key with `evidence`. Under the counter's default
(`tw-precision.py:81`) every pre-round-20 expected row without the key reads as `observed`, so a
lead row like `r13-root:4` would turn the r19 baseline red — i.e. it would be a schema change
(`mado-tripwire-frozen-v2`) requiring every baseline (and `frozen-repin.py`'s normalizer) to be
re-pinned with explicit markers, with no gain to the regression signal.

## Limits

- [UNK] The round-20 fixed tool does not exist at `e629f73` (the worktree tool is still
  `367be947…`). §3's "same class/rule, still in findings" rests on contract E1 plus the current
  row's observed class/rule, not on running the fixed classifier. The r19 replay must be re-run
  once the fix lands; the first line is the check.
- [INFERENCE] `r14-source-safety.jsonl:2,3` are BashCVar rows (variable recipe run through
  `subprocess.run(['bash','-c',recipe])`), untouched by the pure/lead rewrite; even if the fix
  re-marks them `lead`, the frozen key cannot see it.
- Not checked: round-17 frozen-era baselines other than r18 (the question named r18/r19);
  `mado-action-plan.py --frozen` (separate schema); the live gate (paused and out of scope);
  whether `expected.json`'s own digest is bound anywhere beyond the `evidence/final` receipts.
- No LSP server applies: the question is about a Python CLI's runtime comparison, answered by
  reading the deciding code region and by replaying it; no symbol server is configured for this
  repo, so `lsp` was not used (recorded, not substituted with grep-as-proof: the findings above are
  backed by executed replays, and citations are to the exact lines read).

## Installs

none.
