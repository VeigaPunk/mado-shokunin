# R56RevC1Contract — attack on PRED-C1-r56 (as frozen)

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, lane HEAD `2aa347b1` (freeze `3423ae28`). Contract read: `claims-frozen.md`, `registration.md` §C1 (and §harness, §seat boundaries), `frozen-tables.json` (`c1`), `receipts/witness.txt`, `receipts/freeze-verify.txt`. No frozen file was edited. No lane tracked file was written; the lane was read through `git archive`/`git ls-tree`/`git cat-file` only. Leaf member: no subagents, no background jobs of consequence.

## 1. What I did

1. Confirmed the pins are genuine upstream. `curl -sSL` of the pinned URLs at `efb50993780079460b0cbed1363e2166a2de1d9f` (man7: live page) and sha256 vs `frozen-tables.json` `c1.pin_sha256`: 8/8 equal (ConfigWatcher fetched separately: `8383b8ab…` = frozen). Receipt: `receipts/upstream-pin-check.txt`.
2. Built a scratch fixture repo per variant from `git archive 2aa347b1` (system `tar -x`, since the lane holds absolute symlink fixtures; Python `tarfile` refuses them), added the variant, one commit each (`git -C <D> rev-parse --show-toplevel` asserted equal to `<D>` before the first commit; identity `ctl`).
3. Wrote a minimal C1 checker from registration §C1 only (`c1check.py`, stdlib, `python3 -I`, git objects at `--rev` only, honours `--work`). It is not the lane counter: `quality/counters/c1-r56-autoreload-entry.py` and `quality/check-r56-controls.py` are absent at base and at `2aa347b1` (`receipts/before.txt`), so the lane predicate could not be run at all.
4. Generated the cheapest non-work entry (`make_variant.py --variant cheap`) and variants: honest sourced-style, falsified (3 false claims), junk placeholders, entry absent, false number, dropped row, edited quote, missing S390 row.

Commands (full output: `receipts/checker-runs.txt`; trimmed):

```
python3 -I make_variant.py --lane <lane> --rev 2aa347b1… --work <W> --variant cheap   -> fx-cheap head 5a344b1… (later re-run: d7e4805)
python3 -I c1check.py --repo <W>/fx-cheap --rev HEAD --work <W>/chk/cheap
MADO_AUTORELOAD_ENTRY: rev=HEAD rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none   rc=0
```

Results (my checker; full lines in `receipts/checker-runs.txt`):

| variant | verdict | missed |
|---|---|---|
| cheap (template propositions, whole-file anchors) | TARGET_MET rc=0 | none |
| honest (33 hand-written propositions, exact-line anchors) | TARGET_MET rc=0 | none |
| falsified (honest + K04, K13, K20 made false) | TARGET_MET rc=0 | none |
| junk placeholders (frozen control 2) | TARGET_MISSED | tok:K01…H03 (31 ids); content=1/33 |
| entry absent (control 1) | TARGET_MISSED | entry_absent |
| false-number (control 3) | TARGET_MISSED | num:K04 |
| dropped-row (control 7) | TARGET_MISSED | row:K17,source_cell:K17,tok:K17,num:K17 |
| edited-quote, K05 `watch.wd`→`watch.wx` (control 8) | TARGET_MISSED | row:K05,source_cell:K05 (no quote:K05) |
| H02 edited quote (`host` leg, row-carried quote) | TARGET_MISSED | row:H02,host:H02 |
| new-row-missing, S390 deleted (control 10) | TARGET_MISSED | prov,source_cell:K29,scope:K29,source_cell:K30,scope:K30,new_rows |
| lane freeze tree `2aa347b1`, no entry | TARGET_MISSED | entry_absent,index,new_rows |

So the detection controls I could build behave as the registration describes, except control 8 (§3.1).

## 2. The attack: TARGET_MET without a sourced entry

The cheap entry (`entries/NONWORK-cheap-entry.md`, `entries/NONWORK-cheap-registry-rows.md`, `entries/NONWORK-cheap-readme-line.txt`) is non-work and must not be placed in `corpus/`. What it contains:

- K rows: `Line <N> of the pinned file holds <first identifier of the quote>, which this row cites for the reload path.` H rows: `Host capture <id> records <identifier> on line <N> of the host pin.` Each passes tok (one shared identifier) and num (only its own line number, or nothing).
- Provenance trio: `source: S383, …, S390`, `verified-at: 2026-10-28`, `recheck: on-release`. These are text; nothing in the entry records a verification act.
- Registry rows S383–S390: real upstream URLs (so `source_cell` holds), `status mined`, `tier A`, `opened 2026-10-28`, `used-by` the entry, anchor `<basename>:1-<max line + 999>`. Scope and teaches cells are a generic sentence.

The honest and falsified variants show the counter has no sensitivity to the content of a proposition: honest and falsified both reach TARGET_MET, and the falsified one admits three claims contradicted by the pins (K04 "drops every sourced file", K13 "writable source", K20 "keeps the sourced paths").

### Gap between TARGET_MET and a sourced entry (quantified)

| metric | cheap | honest | falsified |
|---|---|---|---|
| counter verdict | TARGET_MET | TARGET_MET | TARGET_MET |
| K/H propositions stating what their quote says (my reading, not independent) | 0/33 | 33/33 (K30 adds an unsourced "because" clause) | 30/33 |
| false claims admitted | n/a | 0 | 3/33 (K04, K13, K20) |
| anchors that run past the pinned file's end | 7/8 (S383 1104>111; S384 1491>734; S385 1148>159; S386 1127>282; S387 2843>2184; S388 1067>844; S390 1261>919) | 0/8 | 0/8 |

The counter's verdict is identical across 0/33 and 33/33 content judgments. The gap in the measured predicate is zero; the gap in entailed content is the full 33 of 33 K/H rows, and the falsified variant shows 3 false claims passing. The lane's own declared limit (`registration.md` §C1 "what the counter proves") concedes this; the consequence is that TARGET_MET is not evidence of a sourced entry.

### What a human reviewer would reject in the cheap entry

- All 30 K propositions are one template; none states the quoted content. "which this row cites for the reload path" is an unsupported use claim.
- All three H propositions only restate an identifier from the host quote.
- The provenance trio is asserted, not recorded: `verified-at` and `recheck` carry no method.
- Anchors `1-1104` on a 111-line file (and 6 others past EOF) locate nothing; the scope leg accepts them.
- Scope and teaches cells are boilerplate.
- Note: the URLs and pins in this variant are genuine (§1.1). The counter cannot distinguish a genuine URL from a fabricated one with the same path suffix; that is the non-counted part.

## 3. Sentences of registration §C1 that are unsatisfiable as written

### 3.1 Control 8 (`edited-quote` → `quote:K05`) is unsatisfiable under the frozen `quote:<id>` definition — round-55 class

Registration §C1 defines `quote:<id>` as "the **frozen** quote is a substring of line `<line>` of the pin blob at `--rev`", with inputs the frozen table and the pin blob. Control 8 changes "one character inside the K05 quote cell" of the **entry row**. Neither input of `quote:K05` changes, so `quote:K05` holds on the mutated tree exactly as on the good tree. The required leg therefore cannot appear in `missed` for that mutation under any implementation of the text as written. The registered row grammar only catches the edit as `row:K05`, which is what my checker reports (`receipts/checker-runs.txt`, variant `edited-quote`: `missed=row:K05,source_cell:K05`).

Consequence: `check-r56-controls.py --claim c1` cannot print `controls=10/10` with any counter that implements §C1 as written, even on the good tree (which passes), so `MADO_AUTORELOAD_ENTRY` cannot reach the predicate's second leg. This is an impossibility, not a counter defect.

Witness under a different reading (not the frozen text): if `quote:<id>` tests the quote **the row carries** (as §C1 already does for `host:<id>`, whose text explicitly says "the quote the ROW carries … independent of quote:<id>"), control 8 is satisfied: `python3 -I c1check.py --repo <W>/fx-edited-quote --rev HEAD --work <W>/chk --quote-leg carried` → `missed=row:K05,quote:K05,source_cell:K05`. The asymmetry between `quote:` (frozen) and `host:` (carried) is itself the defect: the author used "frozen" for K and "carried" for H. Required fix: a pre-data re-registration of §C1 (`quote:` on the carried quote, or control 8 expecting `row:K05`).

I checked the other ten harness expectations for the same invariance problem (each control must change an input of its expected leg): control 1 (entry), 2 (propositions → tok:), 3 (K04 text → num:K04), 4 (K10 src → source_cell:K10), 5 (K10 src → scope:K10 via S399 anchor), 6 (source line → prov), 7 (row → row:K17), 9 (ConfigWatcher bytes → pin_hash), 10 (registry row → new_rows). All are satisfiable: each of these reproduced as written in my variants or follows directly from the legs' inputs.

### 3.2 Sentences that are satisfiable but narrower than they read

- **`num` admits numbers by coincidence.** The leg accepts any digit run equal to the line of another frozen row of the same pin. The K04 sentence `Hyprland 0.56.2 builds the watch list …` passes `num:K04` only because line 56 is K08's line; the `0` / `2` pass as 0–3. The H03 row cannot state version `0.56.2` at all (`56` is not allowed on the host-version pin), and the `num` probe rejected natural sourced phrases: `inotify(7)` (K29, `7` not allowed), `reads at most 1048576 bytes` (K24), `bit 8 of the mask` (K07). Probe: 5/8 pass (`num-probe`, §4). Satisfiable by avoiding such numbers; the cost is that `num` blocks correct citations.
- **`scope` is satisfied by any range that covers the line**, including ranges past the pinned file's end (§2 table). The M56-1 fix therefore cannot distinguish a tight anchor from a whole-file one.
- **`tok` needs one identifier of length ≥ 4** shared with the quote. A single shared identifier suffices.

### 3.3 Ambiguities (satisfiable; the lane counter must decide)

- `entry_absent` is named as a miss but holds when the entry is present (`registration.md` §C1 table). Control 1 reads it literally (`missed` contains `entry_absent` when absent). Consistent, but the name is inverted.
- When the entry is absent, §C1 says "rows/hosts/sources/scope/content print 0"; I followed that for `scope` (scope is registry-based but printed 0). `new_rows` and `index` are evaluated; the text is silent.
- Control 2 expects "`tok:` and `content` shortfall", but `content` is never a leg name in `missed`; I treated the `tok:` prefix as the required token.
- `prov`: "one `verified-at: 2026-10-28`" — I required an exact line match after trimming; the text does not say.
- Pin blob path: the text says "`fetch/`"; I read `.ufo/waves/round-56/fetch/<pin>`.
- `num`: "a digit run of the quote" — I used the same maximal-run regex on the quote; a substring reading would admit more.

### 3.4 Disagreement between frozen text and the receipt

`claims-frozen.md` (lines 9–10) says the C1 grammar was "shown satisfiable as written by an L1 witness (every row, `tok`, `num`, `scope` leg)". `receipts/witness.txt` contains one line: `witness K rows 30 failures []`. It does not cover H rows, `tok`, `num`, `scope`, `source_cell`, `prov`, `index` or `new_rows`. My own witness (the honest variant) does cover all of them under my checker; the receipt overstates the L1 evidence.

## 4. Other checks

- `num`-probe (independent regex on natural sentences): 5/8 pass (`K04` "0.56.2" passes only by the line-56 coincidence above).
- Quote hazards: no frozen quote contains `|`, a backtick or a backslash (checked 33/33).
- The frozen-tables sha `d50d2b7b…` equals the registration constant; the 8 fetch pins match their frozen sha256 both locally and upstream (§1.1); the 4 host pins match their frozen sha256 locally only (host reads, no upstream).
- Not checked: `bash tools/mado-verify.sh --selftest`, `scripts/sources-census.sh`, the C3 counter, host reads (`hyprctl`). Out of seat scope; not run.

## 5. Deliverables

Directory `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56RevC1Contract/`:

- `c1check.py` — independent checker from §C1 (`--quote-leg frozen|carried`; default frozen = registration text).
- `make_variant.py` — variant generator (`git archive` read-only; writes only under `--work`).
- `receipts/checker-runs.txt` — every run above with rc.
- `receipts/upstream-pin-check.txt` — upstream sha256 vs frozen.
- `entries/NONWORK-{cheap,honest,falsified}-entry.md`, `entries/NONWORK-cheap-registry-rows.md`, `entries/NONWORK-cheap-readme-line.txt` — NON-WORK artefacts, not knowledge claims.

## 6. Not verified / limits

- The lane predicate scripts do not exist at `2aa347b1`; my checker is my reading of §C1, so "my checker says TARGET_MET" is evidence about the text, not about the lane counter.
- Entailment of the honest set is my own judgement (not independent). K30 carries an unsourced "because" clause.
- Upstream pin fetch is a one-time GET on 2026-10-28; the man7 page is live and matched the frozen sha, but the page can change.
- No host state was read or changed. No hold-out path was looked for or opened.
- Tools: none installed. Used `python3` (3.14, stdlib), `git`, `curl`, `tar`, `sha256sum`, all already present.
- Scratch `/fast/scratch/hyaku/mado-r56/R56RevC1Contract/` removed after copying the deliverables above.
