# R56CritControls — attack on the round-56 control design (w1, leaf critic)

Scope: `registration.md` controls only (C1 ×10, C3 ×6, C2 ×3 stubs, the harness expectation model, scratch-repo mutation rules).
Lane frozen at `3423ae285676c2a10273000f4519163472b443db`. Read-only: `git show`/`ls-tree`/`archive` of that rev into my scratch;
no lane file, index, ref or fleet file touched. Deliverables: this file and `w1/R56CritControls/` (probe scripts, outputs, sha).
No tool installed (`strace`, `unshare`, `bwrap` are present on the host; I did not use them). No hold-out path was read.

## 0. Bottom line

1. The registered harness cannot distinguish "the counter did the work" from "the counter printed a plausible verdict".
   Its only control check is `required leg ∈ missed ∧ no TARGET_MET`. Any counter that prints every leg as missed on a
   non-lane repo passes all 10 C1 and all 6 C3 controls, and the good-tree run is on the lane, so it is never exercised in
   scratch shape. This is the largest gap.
2. C2's hold-out does not test what its name says. A generic sibling-reader (open `expected.out` next to the argument
   paths) passes the 18 committed fixtures and a same-layout hold-out 100%, because the export ships `expected.*` next to the
   tree. Simulated: 18/18 committed; 0/18 once `expected.*`/`note.txt` are stripped from the export. No registered control
   catches it.
3. C1's counter, as defined lexically, is satisfiable by copy-the-quote entries (proposition = frozen quote + padding).
   Simulated over the lexical legs (`row`, `quote`, `tok`, `num`, length, uniqueness): 33/33 for quote-echo, 1/33 for the
   registered junk placeholders. The registration's declared limit covers "forged proposition reuses a quote identifier";
   this is the cheapest instance of it, and no control reports it.
4. C3's `missing` counts (entry, S) pairs where the entry text cites S. Deleting the citation from prose clears the pair
   without touching `used-by` (cannot be seen by any registered control). Nothing checks that the entry set, row set or
   citation set is monotone against base.
5. Several legs have no mutation control at all: `tables_sha`, `index`, `host:<id>` (structurally duplicate, see §4),
   `pin_hash` for the four host pins, and every sub-clause of `prov` and `source_cell` other than URL/sid/anchor.
6. Two controls have unfrozen parameters (which byte, which character, which pair) and one has an unlisted leg name
   (`content`). The harness cannot be reproduced from the registration alone.

## 1. Commands and what they showed (trimmed; full output in `w1/R56CritControls/*.out`)

```
git -C <lane> show 3423ae…:.ufo/waves/round-56/{registration.md,claims-frozen.md,frozen-tables.json,ctl/*.py}
git -C <lane> archive 3423ae… .ufo/waves/round-56 | tar -x -C <scratch>/x        (read-only export of the freeze tree)
sha256(frozen-tables.json) = d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af   (matches the registered sha)
git ls-tree -r --name-only 3423ae… -- quality tools | grep r56      -> no counter, harness or tool at the freeze commit
```
`probe1.py` (base 13f0acb, read-only): entries=70 ; first sorted entry = `corpus/knowledge/animation-table-r26.md`; its `source:` is a bare
line followed by YAML list items (`  - S175` …); S158 `used-by` already lists it (so C3 control 3 has a real target);
`window-rule-effects-getprop.md` line 3 is the `source:` header and is the first fenced-cite candidate (see D7). Registry max id `S381`/`S382`;
`S399` and `S999` absent (control 5/6 scratch ids are fresh).

`probe2.py`: `200` occurs in `Hyprland-ConfigValues.cpp` (3 lines) and in no ConfigWatcher line, so control 3 separates a
pin-wide digit allowance from a K04-pin allowance (not from the 0–3 or own-line allowances). Placeholder tokens overlap a
quote only for K23 (`source`). K07, K08, K10, K12, K14, K16, K20, K21, K28, K29 quotes are shorter than the 40-char K floor, so
the proposition must add text; the cheapest way to add text is the quote itself.

`probe3.py` (C2, simulated harness over the committed 18, `ctl/` stubs unchanged):
```
const-host.py        committed pass 1 / 18   passing: ['F02']
empty.py             committed pass 0 / 18   passing: []
lookup-committed.py  committed pass 18 / 18
```
`probe4.py` (C2, my sibling-reader `w1/R56CritControls/sib-expected.py`, not a lane file; hold-out simulated by a copy of F01
under a scratch `c2-holdout/H01` only to show layout equivalence; the sealed set was not touched):
```
sibling-reader strip=False: committed 18/18, synthetic-layout-twin 1/1
sibling-reader strip=True : committed 0/18,  synthetic-layout-twin 0/1
```
`probe4.py` (C1 lexical legs only: row grammar, quote substring, tok, num, length, uniqueness; source_cell/scope/prov not modelled):
```
placeholder (control 2 text) : row 33/33 quote 33/33 tok 1/33  num 33/33 len 33/33
quote-echo (quote + padding) : row 33/33 quote 33/33 tok 33/33 num 33/33 len 33/33
```
`probe5.py`/`probe6.py` (base source headers, first 15 lines): 44 entries with ids on the `source:` line, 6 bare `source:` with YAML
list items (3 carry ids there, all registry ids today), 20 entries with no `source:` line in the first 15.

## 2. Channel table

Legend. "Passes" = a channel that gives a green verdict without the work. "Registered catch" = a registered control that would
make the channel fail. "Would catch" = control I recommend. "Declared" = the registration already names the limit.

### 2a. Shared channels (C1 and C3 counters, harness mechanics)

| # | channel | passes registered harness? | registered catch | would catch | declared? |
|---|---|---|---|---|---|
| K1 | **Flood**: on any repo that is not the lane (scratch shape), print every leg as missed, exit 1 | **yes** (C1 10/10, C3 6/6: `contains` + exit 1 + no TARGET_MET); good run on lane is honest | none | (a) `missed ⊆ allowed(control)` with the allowed set held by the harness per mutation; (b) null-shape control: good tree re-committed as a fresh single-commit repo, neutral author, neutral path, must print TARGET_MET | no |
| K2 | **Scratch-shape detection**: the registration fixes the scratch identity (`-c user.name=ctl -c user.email=ctl@ctl`), the scratch path (`mktemp -d -p <work>`), the single-commit history (`git init -q`, no base ancestor). A counter can test `git cat-file -e 13f0acb…` or the author and branch on it | **yes** | none (the good run is never in scratch shape) | identity/path randomisation per run; null-shape control (above) | no |
| K3 | **Tree-sha memo**: every scratch tree is determined by the public registration (good tree + one published mutation), so the 11 tree shas are precomputable; a counter can carry a table tree-sha → output | **yes** | none | fresh, randomised mutation parameters (new tree shas); equivalence-preserving null mutations (add an unrelated file, reword a README line) must keep TARGET_MET | yes, as "caches runs / forges a consistent tree" (registration l.18–20); the controls do not defend it |
| K4 | **Mutation-text keying**: literal strings from the registration (`placeholder proposition text`, `capped at 200`, `S999`, `S399`, `no-such-entry.md`, `ConfigWatcher.cpp:1-10`) | **yes** | none | parameterised controls: ids, numbers, S-ids, filler and positions drawn per run; the verdict must not change | no |
| K5 | **Harness-expectation read**: `quality/check-r56-controls.py` is committed in the good tree, so every scratch commit contains it; a counter can `git show` the control table and answer with the expected leg | **yes** (the expected legs are in the tree) | none | keep expectations out of tree; run counters under `strace -f -e trace=openat,execve` and allow only git + registered paths; any read of `quality/check-r56-controls.py` fails | no |
| K6 | **Partial echo of frozen tables**: print `rows=30/30 hosts=3/3 …` from `frozen-tables.json` without evaluating legs with no control | **yes** for the uncontrolled legs (`tables_sha`, `index`, `host:`, `pin_hash` for host pins, `prov` sub-clauses, `source_cell` sub-clauses) | a full echo prints TARGET_MET on every control tree and fails all 10; a partial echo passes | one control per uncontrolled leg (see §4) | partly (registration says "counter that prints green without work" is evidence against it, but the controls do not cover these legs) |
| K7 | **Time / environment sniffing**: no date-dependent leg exists (`verified-at` is a literal); good and control runs have identical env (`TMPDIR`=work, `GIT_*` scrubbed) | no difference to exploit | n/a | path/identity randomisation (K2) is the only effective probe; an env canary | yes ("sniffs its environment") |
| K8 | **Caching**: per-rev or per-tree cache in `--work` or `$HOME`. Scratch trees differ, so a stale hit is unlikely; a cache that stores answers is K3 | yes for stale hits, low harm | none; the registration says the counter "writes nothing" but nothing checks it | `--work` empty before and after each run; `strace` for `O_CREAT`/`O_WRONLY` | yes ("caches runs") |
| K9 | **Read beyond the commit**: C1/C3 are restricted to `--rev` git objects; a counter can read the lane working tree or `.git` by absolute path (the working tree at a later integration holds `fixtures/c2-holdout/`) | yes | none | `strace` read-set audit; `bwrap`/`unshare -m` with only the export and the git object store visible | no (registration states the rule, nothing enforces it) |

### 2b. C2 channels (`ctl/` stubs and hold-out)

| # | channel | passes? | registered catch | would catch | declared? |
|---|---|---|---|---|---|
| C2-a | **Sibling expected reader**: for each argument, walk the path and its ancestors for `expected.out`/`expected.rc`, print and exit | **yes**: 18/18 committed (`probe4`); the hold-out has the same layout (`fixtures/c2-holdout/H##/{args.json,expected.*,tree/}`), so it passes the hold-out too | none (`lookup-committed` keys on `F##` name only; the hold-out is name-keyed too) | export without `expected.*` and `note.txt` (0/18 in `probe4`); add `ctl/sib-expected.py` with `0/…` expectation | no |
| C2-b | F-name lookup | no (hold-out 0/8) | `ctl/lookup-committed.py` 0/8 hold-out | — | — |
| C2-c | Constant output / empty output | no (1/26, 0/26) | `ctl/const-host.py`, `ctl/empty.py` | — | — |
| C2-d | Hard-coded reads of the lane or host tree (`fixtures/c2-holdout` after integration; host `~/.config/hypr`) | yes if the path is known | none | `bwrap`/`unshare` mount namespace with only the export; `strace` openat audit against the registered read set (argv paths, `os.stat`, `source =` closure) | no; the "reads only" rule is stated and unchecked |
| C2-e | Rule fitting to the 18 visible fixtures and their notes (`note.txt` names the case) | the 8 hold-out cases are the only check; power is low | hold-out only | independent property-based generator with an independent (non-author) reference implementation | no |
| C2-f | Dictionary match on `c2.fixture_files` sha256 (committed `expected.out` hashes are in `frozen-tables.json`). Only short setup outputs (F12, F17, F18: 24–27 bytes; F12 and F18 share a sha) are guessable | yes for 3 setup fixtures | none | none needed for impact; note only | no |

### 2c. C3 channels (registry back-references)

| # | channel | passes? | registered catch | would catch | declared? |
|---|---|---|---|---|---|
| C3-a | **Prose citation deletion**: remove the `S###` token from the entry text for each missing pair. `missing` counts CITE pairs, so the pair vanishes; `extra` and `dangling` are unaffected | **yes**, by the definitions (CITE is read from the entry text) | none | harness-side monotonicity: CITE(rev) ⊇ CITE(base) on the base entries (C1's additions allowed) | no; the claim says "used-by edits only" but nothing checks it |
| C3-b | **Registry row deletion** for ids cited only in prose: `missing` falls, `rows` falls | yes | none | harness-side: rows(rev) ⊇ rows(base) and every non-`used-by` cell byte-identical to base | no |
| C3-c | **Entry deletion** (with its README row, which keeps index parity): `entries` falls and its citations stop counting | yes | none | harness-side: entries(rev) ⊇ entries(base) | no |
| C3-d | **List-form blind spot**: `dangling` reads only the `source:` line. A YAML list item `  - S999` under a bare `source:` is invisible. 6 base entries use the list form | yes for list-form dangling | control 4 appends to the bare line, so the list form is untested | a control that appends `  - S999` as a list item under `source:` | no |
| C3-e | Entries with no `source:` in the first 15 lines (20 at base) are outside `SRC` | yes for dangling in those entries | none | define SRC over the whole header or state the exclusion | no |

## 3. Per-control assessment (can it fail; what does it actually test)

### C1 (registration §C1, 10 controls)

| ctl | mutation | required leg | can fail? | what it tests / caveat |
|---|---|---|---|---|
| 1 entry-absent | delete entry | `entry_absent` | yes | fine |
| 2 junk-placeholders | replace all K/H propositions | "`tok:` and `content` shortfall" | yes | **`content` is not a missed-leg name** (the registration prints `content=e/33` as a count field, and the leg table has no `content`). The harness target is undefined (D1). It tests only the placeholder form; `tok` overlaps only K23. |
| 3 false-number | append "capped at 200" to K04 | `num:K04` | yes | `200` is absent from ConfigWatcher.cpp and present in ConfigValues.cpp: this discriminates a digit allowance drawn from the whole pin set and from K04's own pin. It tests one number only; the 0–3 allowance and the own-line allowance are not probed. |
| 4 cross-pin-source | K10 cites S385 | `source_cell:K10` | yes | fine |
| 5 scope-swap | add S399 (same URL, anchor `ConfigWatcher.cpp:1-10`), K10 cites it | `scope:K10` | yes | fine; also trips `prov` and `source_cell`, required leg still listed |
| 6 provenance-dangling | append `, S999` to `source:` line | `prov` | yes | bare-line form only; list-form `- S999` passes (C3-d analogue, D6) |
| 7 dropped-row | delete K17 | `row:K17` | yes | fine |
| 8 edited-quote | change one character of K05 quote | `quote:K05` | yes | the character is unspecified; a replacement that creates a `|` or non-ASCII byte changes `row:` as well (D3) |
| 9 pin-byte | change one byte of `fetch/Hyprland-ConfigWatcher.cpp` | `pin_hash` | yes | byte and value unspecified; a non-UTF-8 byte makes a strict counter exit 2 (setup), which fails the control for an unrelated reason (D3). Only the ConfigWatcher pin is probed; the four host pins are not (D9). |
| 10 new-row-missing | delete S390 row | `new_rows` | yes | fine; also `source_cell:K29/K30` and `prov` |

Controls cannot be made inert by the good tree: all 10 mutations change an input read by a registered leg (verified against the frozen rows, pins and registry at the freeze commit; the counters themselves are absent, so no run is possible).

### C3 (registration §C3, 6 controls)

| ctl | mutation | required leg | can fail? | caveat |
|---|---|---|---|---|
| 1 base-registry | SOURCES.md → base bytes | `missing` | yes | base has no S383–S390, so `dangling` also fires; `claims-frozen` says "scores 65", which the harness does not check (D10) |
| 2 fill-all | every used-by = all entries | `extra` | yes | fine |
| 3 drop-one | remove animation-table-r26 from S158 | `missing` | yes | target exists (S158 lists it at base; good tree keeps it because the pair is a citation) |
| 4 dangling-source | append ` S999` to the bare `source:` line of animation-table-r26 | `dangling` | yes, on this form | the entry's source is a YAML list; the mutation is a form the list-form entries do not use (C3-d) |
| 5 ghost-path | add `no-such-entry.md` to S001 | `extra` | yes | fine |
| 6 fenced-cite | wrap the first exactly-once citation pair in a fence | `extra` | yes | the first candidate by (S, entry) is `S002` on line 3, which is the `source:` header. `SRC` is not fence-aware, so `SRC` still reads S002 while `CITE` drops it (D7) |

Every control can fail on the good tree. None is inert. But none of the six detects K1, K3, C3-a, C3-b or C3-c.

### C2 (registration §C2, 3 stubs)

- `ctl/const-host.py`: passes 1/18 committed (F02 only); can fail if another fixture's `expected.out` equals F02's. Hold-out count unknown.
- `ctl/empty.py`: passes 0/18; can fail only if a hold-out expects empty stdout with rc 0.
- `ctl/lookup-committed.py`: passes 18/18 committed (`probe3`). On the hold-out it is 0/8 only because the hold-out names are `H##`; a hold-out with a path component `F##` would pass. The stub's behaviour on the hold-out is therefore a naming test, not a content test.
- The stubs' pass rules are not defined. "at most 1 of 26" and "passes 18/18 committed and 0/8 hold-out" are expectations, not a formula; the harness decides `controls=3/3` by a rule the registration does not state (D4).
- No control covers C2-a (sibling reader), C2-d (absolute-path reads), or the write/process rules ("writes nothing", "starts no process").

## 4. Uncovered legs (no registered mutation changes the input)

- C1 `tables_sha`: no control mutates `frozen-tables.json`.
- C1 `index`: no control removes the `corpus/README.md` row.
- C1 `pin_hash` for `host-getoption.json`, `host-sources.txt`, `host-version.json`, `host-watched-lstat.txt`: only the ConfigWatcher pin is mutated (control 9).
- C1 `host:<id>`: by the row grammar the row's quote cell must equal the frozen quote, so `host:` reads the same bytes as `quote:` against the same host line (the registration calls it "independent of `quote:`", but under the grammar it is not). No control can make it fail without also failing `row:`. A counter that skips it passes all 10 controls (D5).
- C1 `prov` sub-clauses: `verified-at` line, `recheck:` line, their order, the 30-line window, and the source set cover K-cited ids beyond S999.
- C1 `source_cell` sub-clauses: `status mined`, `tier A|B`, `opened 2026-10-28`, `rev_rule` token in URL, `used-by` naming the entry. Controls 4, 5, 10 test only URL-suffix, sid and registry presence.
- C1 `num` allowed set: 0–3, the row's own line, another row's line on the same pin. Control 3 probes one number.
- C1 `scope` boundary: range end inclusivity and the `N` singleton form are not probed.
- C1 `content` for H rows; `tok` beyond the placeholder text.
- C3 `used-by` cell parsing outside cell 11, the `S`-token regex in `SRC`, the `dangling` check on list-form sources.

## 5. Defects and ambiguities (input that shows each)

- **D1** Control 2 names leg `content`, which the leg table and the output grammar do not define (`registration.md` §C1 table vs §C1 control 2; output `content=<e>/33` is a count). The harness target is undefined.
- **D2** The claim "control 2 is the cheapest entry that copies the frozen quotes and fills placeholder propositions" (`claims-frozen.md` §C1, "Do-nothing controls") is false: quote-echo passes all lexical legs 33/33 (`probe4`). The registration's declared limit covers the forged-proposition case, but the "do-nothing controls score TARGET_MISSED" statement does not cover quote-echo.
- **D3** Unfrozen mutation parameters: control 8 (which character, which replacement), control 9 (which byte, which value; a non-UTF-8 byte gives exit 2 not 1), control 3 (position of the appended text), control 6 (which `source:` line). Two runs of the same control can differ.
- **D4** The C2 stub pass rule (`controls=k/3`) is not defined for stubs whose expected score is a range (`at most 1`) or a pair (`18/18 committed and 0/8 hold-out`).
- **D5** `host:<id>` is not independent of `quote:`/`row:` under the row grammar (see §4), contrary to "(independent of quote:<id>)".
- **D6** `SRC` / `prov` read `source:` lines only. The base corpus has a bare `source:` with list items in 6 entries and no `source:` in the first 15 lines in 20. A counter following the text sees zero ids for list-form headers. The C1 entry's header form is not frozen, so `prov` may fail for a correct list-form entry or pass for a list-form forgery.
- **D7** C3 control 6's first candidate (S002, `window-rule-effects-getprop.md` line 3) is the `source:` header. `SRC` is not fence-aware; the fence is not described for header lines.
- **D8** The good-tree run uses `--repo .` on the lane. The controls use fresh scratch repos. No control runs the good tree in scratch shape (K1/K2).
- **D9** `pin_hash` is registered for "every pin blob"; control 9 mutates one K pin. The four host pins are untested.
- **D10** `claims-frozen.md` §C3 says the unchanged registry "scores 65"; `registration.md` §C3 requires only that `missing` be in `missed`. Disagreement between the two texts; registration wins per the rule. The exact 65 is not checked.
- **D11** `claims-frozen.md` §C3 target "used-by edits only" and registration "Cells other than used-by are never touched by the fix" are rules with no control (C3-a/b/c).
- **D12** Registration §C2 "reads only the files named by its arguments … starts no process … writes nothing" has no audit.
- **D13** The hold-out tests name-keyed lookup but not content-keyed lookup. Sibling reader passes a same-layout hold-out identically (`probe4`, synthetic twin).
- **D14** `claims-frozen.md` §C3 says C1 and C3 each "verify without the other having landed"; C3's good-tree run includes C1's entry (its citations must be listed), so the separability holds only if C3 is evaluated on the base entries plus whatever exists. Not a defect in the counts; noted for the ledger.

## 6. Recommended corrections (smallest safe set; each one is a pre-data re-registration in a NEW versioned file, since `registration.md` is frozen)

1. **Two-sided control check.** For each control: `required ∈ missed ⊆ allowed(control)` with `allowed` a harness-held set, plus no TARGET_MET. Kills K1.
2. **Null and equivalence controls.** (a) good tree re-committed as a fresh single-commit repo under a neutral path with a neutral author, must be TARGET_MET; (b) add an unrelated file; (c) reword a commit message. Kills K1, K2, K3 (partially), K4.
3. **Parameterised mutations.** Draw ids, numbers, S-ids, filler text, byte/char positions per run from a seed published with the harness. Kills K4 and the D3 non-reproducibility.
4. **Out-of-tree expectations plus a read-set audit.** Expectations not in the tree; counters under `strace -f -e trace=openat,execve`; allowed set = git and registered paths; `--work` empty before and after. Kills K5, K8, K9, C2-d, D12.
5. **Controls for uncovered legs** (§4): `tables_sha` (mutate the tables file), `index` (drop the README row), each host pin (`pin_hash`), `host:` (cannot be made independent; either drop the leg or re-register it as duplicate), each `prov` clause, each `source_cell` clause, the `num` allowed set, `content`.
6. **C2:** strip `expected.*` and `note.txt` from the export; add `ctl/sib-expected.py` with the committed expectation of 0 on the stripped export and 18/18 unstripped; run the hold-out in the same way; run the tool under a mount namespace that hides the lane and host.
7. **C3 monotonicity (harness side):** CITE(rev) ⊇ CITE(base) on base entries; entries(rev) ⊇ base; rows(rev) ⊇ base; every non-`used-by` cell byte-identical to base. Kills C3-a, C3-b, C3-c.
8. **C1 quote-echo:** add a leg `echo:<id>` (the proposition must not contain the frozen quote verbatim) with a control. Without it, the 33/33 quote-echo entry is accepted, and the declared limit must say so in the closure.
9. **Define C2 stub pass rules** and the `content`/`missed` grammar (D1, D4).
10. **Fix the mutation-target choices**: control 6 picks a non-header pair; control 4 gets a list-form twin; `SRC` read rule stated for list items.

## 7. Could not verify (declared)

- No counter, harness or tool exists at the freeze commit (`quality/counters/c1-r56-*`, `quality/check-r56-controls.py`, `quality/counters/c3-r56-used-by.py`, `tools/mado-watchplan.py` absent). No registered control was executed; every verdict above is from the written rules, the frozen data, or my lexical/stub simulations.
- The C2 simulation used the committed `ctl/` stubs and my own copy of the harness rule (`probe3`, `probe4`). It is not the lane's harness.
- The C1 lexical simulation (`probe4`) excludes `source_cell`, `scope` and `prov`, which depend on registry rows and headers the wave will write. The quote-echo verdict on those legs is a derived claim, not observed.
- The C3 counts at the final content revision are not available (no wave output). Control-target existence was checked at base, not in the wave's good tree.
- The hold-out is sealed; I did not look for it. `fixtures/c2-holdout/H01` in my scratch is a copy of F01 for layout only. I read the hold-out commitment value from `frozen-tables.json` and did not check it.
- Scratch-repo shape (single commit, no base ancestor, `ctl` identity) is derived from the registration's description of `git init -q`; I did not construct a harness scratch repo.
- No tool was installed or upgraded. Host reads: none beyond `command -v` for `strace`, `unshare`, `bwrap`, `python3`.

## 8. Receipts (in `w1/R56CritControls/`)

`probe1.py … probe6.py` with `probe1.out … probe6.out`; `sib-expected.py` (scratch stub); `frozen-tables.sha256` (`d50d2b7b…`, matches the registered sha).
